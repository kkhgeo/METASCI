#!/usr/bin/env python3
"""Deterministically verify a Korean style revision.

The gate checks change rate, protected content, structure, register consistency,
selected Korean humanization signals, and sentence touch rate. It does not infer
whether a person or an AI authored the text.

Design adapted from epoko77-ai/im-not-ai (MIT), commit
53e24e8f92cf344efcb812103f7c2b203e7efffc. This implementation is rewritten as a
self-contained, Windows-safe verifier for meta-mywriting-korean.
"""

from __future__ import annotations

import argparse
from collections import Counter
from difflib import SequenceMatcher
import json
from pathlib import Path
import re
import sys
from typing import Iterable


WARN_RATE = 0.30
ABORT_RATE = 0.50

NUMBER_RE = re.compile(r"(?<![A-Za-z])\d[\d,]*(?:\.\d+)?")
DIRECT_QUOTE_RES = (
    re.compile(r'"([^"\n]{1,1000})"'),
    re.compile(r"“([^”\n]{1,1000})”"),
    re.compile(r"'([^'\n]{1,1000})'"),
    re.compile(r"‘([^’\n]{1,1000})’"),
)
FOOTNOTE_MARK_RE = re.compile(r"\[\^[^\]]+\]")
FOOTNOTE_DEF_RE = re.compile(r"^\[\^([^\]]+)\]:\s*(.+)$", re.MULTILINE)
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)
FIGURE_REF_RE = re.compile(
    r"(?:그림|표|Figure|Fig\.|Table)\s*[A-Za-z가-힣]?\d+(?:[-–]\d+)?",
    re.IGNORECASE,
)
CITATION_PAREN_RE = re.compile(
    r"\((?P<authors>[^()\n]{1,100}?[A-Za-z가-힣][^()\n]{0,80}?),?\s*"
    r"(?P<year>(?:19|20)\d{2}[a-z]?)\)"
)
CITATION_NARRATIVE_RE = re.compile(
    r"(?P<authors>(?:[A-Z][A-Za-z-]+(?:\s+(?:and|&)\s+[A-Z][A-Za-z-]+)*|"
    r"[가-힣]{2,4}(?:(?:·|,|\s+(?:및|와|과))\s*[가-힣]{2,4})*(?:\s*외)?))"
    r"\s*\((?P<year>(?:19|20)\d{2}[a-z]?)\)"
)
CORNER_BRACKET_RE = re.compile(r"[「『]([^」』\n]{1,300})[」』]")
SENTENCE_RE = re.compile(r"[^.!?。！？\n]+[.!?。！？]?", re.MULTILINE)

HAPSYOCHE_RE = re.compile(r"(?:습니다|ㅂ니다|입니다|합니다|됩니다|하십시오|하세요)(?:[.!?]|$)")
HAERACHE_RE = re.compile(
    r"(?:이다|한다|있다|된다|필요하다|요구된다|않는다|나타난다|하였다)(?:[.!?]|$)"
)

STYLE_SIGNALS: tuple[tuple[str, str, re.Pattern[str]], ...] = (
    ("H1", "S1", re.compile(r"되어졌|되어진|되어지(?:다|며|고|는)")),
    ("H2", "S1", re.compile(r"(?:지만|는데|으며|하며|하고|하여|해서|므로|기에),")),
    ("H3", "S1", re.compile(r"(?:에서의|에로의|으로부터의|로부터의|에의|으로의)")),
    ("H4-about", "S2", re.compile(r"(?:에\s*대하여|에\s*대해서|에\s*있어서)")),
    ("H4-through", "S2", re.compile(r"(?:을|를)\s*(?:통하여|통해)")),
    ("H5", "S2", re.compile(r"(?:가지고\s+있|에\s+의해|이루어지(?:다|며|고|는))")),
    (
        "H10",
        "S2",
        re.compile(r"할\s+수\s+있을\s+것으로\s+(?:판단|기대|예상|추정)(?:된다|된다\.)"),
    ),
    (
        "H13",
        "S2",
        re.compile(
            r"(?<![가-힣A-Za-z0-9])(?:이|그|저|이러한|그러한|저러한)\s+"
            r"(?:과정|결과|한계|상황|관점|맥락|고정성|구조|방식|문제|현상|특성|점|측면)"
            r"(?:에서|은|는|이|가|을|를|으로|로|과|와|도|의)?"
        ),
    ),
)


def _configure_utf8_stdout() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass


def _read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8").replace("\r\n", "\n")


def _plain(text: str, ignore_markup: bool) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    if ignore_markup:
        text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
        text = re.sub(r"[*_`~]", "", text)
        text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    return re.sub(r"\s+", " ", text).strip()


def _change_rate(before: str, after: str, ignore_markup: bool) -> float:
    left = _plain(before, ignore_markup)
    right = _plain(after, ignore_markup)
    if not left:
        return 0.0 if not right else 1.0
    return 1.0 - SequenceMatcher(None, left, right, autojunk=False).ratio()


def _number_set(text: str) -> set[str]:
    return {match.replace(",", "") for match in NUMBER_RE.findall(text)}


def _direct_quotes(text: str) -> set[str]:
    found: set[str] = set()
    for pattern in DIRECT_QUOTE_RES:
        found.update(re.sub(r"\s+", " ", item).strip() for item in pattern.findall(text))
    return found


def _author_key(raw: str) -> str:
    raw = raw.lower()
    raw = re.sub(r"\b(?:and|et\s+al)\b|(?:및|와|과|외)", "", raw)
    return re.sub(r"[^a-z가-힣]", "", raw)


def _citation_keys(text: str) -> set[str]:
    keys: set[str] = set()
    for pattern in (CITATION_PAREN_RE, CITATION_NARRATIVE_RE):
        for match in pattern.finditer(text):
            author = _author_key(match.group("authors"))
            if author:
                keys.add(f"{author}|{match.group('year').lower()}")
    return keys


def _sentences(text: str) -> list[str]:
    return [re.sub(r"\s+", " ", item).strip() for item in SENTENCE_RE.findall(text) if item.strip()]


def _touch_rate(before: str, after: str) -> tuple[float, int, int]:
    sentences = _sentences(before)
    if not sentences:
        return 0.0, 0, 0
    after_flat = re.sub(r"\s+", " ", after)
    touched = sum(sentence not in after_flat for sentence in sentences)
    return touched / len(sentences), touched, len(sentences)


def _counter_diff(before: Iterable[str], after: Iterable[str]) -> tuple[list[str], list[str]]:
    left = Counter(before)
    right = Counter(after)
    removed = sorted((left - right).elements())
    added = sorted((right - left).elements())
    return removed, added


def _style_counts(text: str) -> dict[str, dict[str, int | str]]:
    scan_text = text
    for pattern in DIRECT_QUOTE_RES:
        scan_text = pattern.sub("", scan_text)
    counts = {
        signal_id: {"severity": severity, "count": len(pattern.findall(scan_text))}
        for signal_id, severity, pattern in STYLE_SIGNALS
    }
    middle_dot_overuse = 0
    middle_dot_group_re = re.compile(r"[가-힣A-Za-z0-9]+(?:·[가-힣A-Za-z0-9]+)+")
    for sentence in _sentences(scan_text):
        group_count = len(middle_dot_group_re.findall(sentence))
        dot_count = sentence.count("·")
        if group_count >= 2 or dot_count >= 3:
            middle_dot_overuse += 1
    counts["H14"] = {"severity": "S2", "count": middle_dot_overuse}
    return counts


def verify(before: str, after: str, ignore_markup: bool = False) -> tuple[int, dict[str, object]]:
    issues: list[dict[str, object]] = []
    rate = _change_rate(before, after, ignore_markup)
    if rate >= ABORT_RATE:
        issues.append({"gate": "P0", "level": "abort", "message": "변경률이 50% 이상입니다."})
    elif rate >= WARN_RATE:
        issues.append({"gate": "P0", "level": "warn", "message": "변경률이 30% 이상입니다."})

    before_numbers = _number_set(before)
    after_numbers = _number_set(after)
    removed_numbers = sorted(before_numbers - after_numbers)
    added_numbers = sorted(after_numbers - before_numbers)
    if removed_numbers or added_numbers:
        issues.append(
            {
                "gate": "P1-numbers",
                "level": "abort",
                "message": "수치가 추가되거나 제거되었습니다.",
                "removed": removed_numbers,
                "added": added_numbers,
            }
        )

    removed_quotes, added_quotes = _counter_diff(_direct_quotes(before), _direct_quotes(after))
    if removed_quotes or added_quotes:
        issues.append(
            {
                "gate": "P1-quotes",
                "level": "abort",
                "message": "직접 인용 내용이 변경되었습니다.",
                "removed": removed_quotes,
                "added": added_quotes,
            }
        )

    before_citations = _citation_keys(before)
    after_citations = _citation_keys(after)
    removed_citations = sorted(before_citations - after_citations)
    added_citations = sorted(after_citations - before_citations)
    if removed_citations or added_citations:
        issues.append(
            {
                "gate": "P1-citations",
                "level": "warn",
                "message": "저자-연도 인용 키가 변경되었습니다. 형식 정규화인지 확인해야 합니다.",
                "removed": removed_citations,
                "added": added_citations,
            }
        )

    before_bracketed = set(CORNER_BRACKET_RE.findall(before))
    after_bracketed = set(CORNER_BRACKET_RE.findall(after))
    missing_bracketed = sorted(item for item in before_bracketed if item not in after)
    introduced_bracketed = sorted(item for item in after_bracketed if item not in before)
    if missing_bracketed or introduced_bracketed:
        issues.append(
            {
                "gate": "P1-named-spans",
                "level": "abort",
                "message": "법령명·서명 등 괄호 보호 항목의 내용이 변경되었습니다.",
                "removed": missing_bracketed,
                "added": introduced_bracketed,
            }
        )

    protected_patterns = {
        "footnote_markers": FOOTNOTE_MARK_RE,
        "footnote_definitions": FOOTNOTE_DEF_RE,
        "figure_table_refs": FIGURE_REF_RE,
    }
    protected_report: dict[str, object] = {}
    for name, pattern in protected_patterns.items():
        removed, added = _counter_diff(pattern.findall(before), pattern.findall(after))
        protected_report[name] = {"removed": removed, "added": added}
        if removed or added:
            issues.append(
                {
                    "gate": f"P1-{name}",
                    "level": "abort",
                    "message": f"보호 항목이 변경되었습니다: {name}",
                    "removed": removed,
                    "added": added,
                }
            )

    before_headings = set(HEADING_RE.findall(before))
    after_headings = set(HEADING_RE.findall(after))
    removed_headings = sorted(before_headings - after_headings)
    added_headings = sorted(after_headings - before_headings)
    if removed_headings or added_headings:
        issues.append(
            {
                "gate": "P2-headings",
                "level": "warn",
                "message": "헤딩 구성이 변경되었습니다.",
                "removed": removed_headings,
                "added": added_headings,
            }
        )

    register = {
        "hapsyoche": len(HAPSYOCHE_RE.findall(after)),
        "haerache": len(HAERACHE_RE.findall(after)),
    }
    if register["hapsyoche"] > 0 and register["haerache"] > 0:
        issues.append(
            {"gate": "P3-register", "level": "warn", "message": "최종본에 종결체가 혼용되었습니다."}
        )

    before_signals = _style_counts(before)
    after_signals = _style_counts(after)
    for signal_id, after_item in after_signals.items():
        before_count = int(before_signals[signal_id]["count"])
        after_count = int(after_item["count"])
        severity = str(after_item["severity"])
        if after_count > before_count or (severity == "S1" and after_count > 0):
            issues.append(
                {
                    "gate": "P4-signals",
                    "level": "warn",
                    "message": f"고신뢰 문체 신호가 남거나 증가했습니다: {signal_id}",
                    "before": before_count,
                    "after": after_count,
                    "severity": severity,
                }
            )

    touch_rate, touched, sentence_count = _touch_rate(before, after)
    levels = {str(issue["level"]) for issue in issues}
    exit_code = 2 if "abort" in levels else 1 if "warn" in levels else 0
    verdict = "ABORT" if exit_code == 2 else "WARN" if exit_code == 1 else "PASS"
    report: dict[str, object] = {
        "verdict": verdict,
        "exit_code": exit_code,
        "change_rate": round(rate, 6),
        "sentence_touch_rate": round(touch_rate, 6),
        "sentences_touched": touched,
        "sentence_count": sentence_count,
        "numbers": {"removed": removed_numbers, "added": added_numbers},
        "direct_quotes": {"removed": removed_quotes, "added": added_quotes},
        "citations": {"removed": removed_citations, "added": added_citations},
        "named_spans": {"removed": missing_bracketed, "added": introduced_bracketed},
        "protected": protected_report,
        "headings": {"removed": removed_headings, "added": added_headings},
        "register": register,
        "style_signals": {"before": before_signals, "after": after_signals},
        "issues": issues,
        "authorship_inference": "not_performed",
    }
    return exit_code, report


def main(argv: list[str] | None = None) -> int:
    _configure_utf8_stdout()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before", required=True, help="UTF-8 file containing only the original body")
    parser.add_argument("--after", required=True, help="UTF-8 file containing only the revised body")
    parser.add_argument("--json-out", help="Write the complete JSON report to this path")
    parser.add_argument("--ignore-markup", action="store_true", help="Ignore basic Markdown in change rate only")
    args = parser.parse_args(argv)

    try:
        before = _read(args.before)
        after = _read(args.after)
        exit_code, report = verify(before, after, args.ignore_markup)
        if args.json_out:
            target = Path(args.json_out)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(
            f"{report['verdict']}: 변경률 {float(report['change_rate']) * 100:.1f}% / "
            f"문장 터치율 {float(report['sentence_touch_rate']) * 100:.1f}% / "
            f"이슈 {len(report['issues'])}건"
        )
        for issue in report["issues"]:
            print(f"- [{str(issue['level']).upper()}] {issue['gate']}: {issue['message']}")
        return exit_code
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"ERROR: 결정적 게이트를 실행하지 못했습니다: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
