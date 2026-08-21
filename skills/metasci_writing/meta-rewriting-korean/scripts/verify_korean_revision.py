#!/usr/bin/env python3
"""Mechanically verify preservation in a Korean revision.

The verifier has two modes:

- light: conservative editing; large string changes can warn or abort.
- deep: structural rewriting; change rate is reported but never blocks.

It checks numeric expressions (including signs, comparators, uncertainty, units,
and duplicate counts), likely value-anchor bindings, citations, direct quotes,
figure/table references, named spans, footnotes, headings, register consistency,
and selected Korean style signals.

A successful result is MECHANICAL_PASS, not semantic or factual validation.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from difflib import SequenceMatcher
import json
from pathlib import Path
import re
import sys
from typing import Iterable, Iterator, Sequence


WARN_RATE = 0.30
ABORT_RATE = 0.50

# Number + optional comparator/sign/range/uncertainty/unit.  It intentionally
# includes citation years and table numbers; those are load-bearing too.
NUMBER_CORE = r"(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:[eE][+\-−]?\d+)?"
COMPARATOR = r"(?:(?:[pP]\s*)?(?:<=|>=|<|>|≤|≥|=|~|≈)\s*)?"
SIGN = r"(?:[+\-−]\s*)?"
RANGE = rf"(?:\s*(?:-|–|—|~)\s*{SIGN}{NUMBER_CORE})?"
UNCERTAINTY = rf"(?:\s*±\s*{NUMBER_CORE})?"
UNIT_ATOM = r"(?:%|‰|℃|°\s*C|[A-Za-zµμΩ][A-Za-z0-9µμΩ·⋅/^*+\-−⁻⁺¹²³⁴⁵⁶⁷⁸⁹]*)"
UNIT = rf"(?:\s*{UNIT_ATOM}(?:\s+{UNIT_ATOM}){{0,2}})?"
NUMERIC_EXPR_RE = re.compile(
    rf"(?<![A-Za-z0-9])(?P<expr>{COMPARATOR}{SIGN}{NUMBER_CORE}{RANGE}{UNCERTAINTY}{UNIT})"
)

DIRECT_QUOTE_RES = (
    re.compile(r'"([^"\n]{1,2000})"'),
    re.compile(r"“([^”\n]{1,2000})”"),
    re.compile(r"'([^'\n]{1,2000})'"),
    re.compile(r"‘([^’\n]{1,2000})’"),
)
FOOTNOTE_MARK_RE = re.compile(r"\[\^[^\]]+\]")
FOOTNOTE_DEF_RE = re.compile(r"^\[\^([^\]]+)\]:\s*(.+)$", re.MULTILINE)
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)
FIGURE_REF_RE = re.compile(
    r"(?:그림|표|Figure|Fig\.|Table)\s*[A-Za-z가-힣]?\s*\d+(?:[-–]\d+)?",
    re.IGNORECASE,
)
CORNER_BRACKET_RE = re.compile(r"[「『]([^」』\n]{1,300})[」』]")
SENTENCE_RE = re.compile(r"[^.!?。！？\n]+[.!?。！？]?", re.MULTILINE)
WORD_RE = re.compile(r"[A-Za-z]+|[가-힣]+")
YEAR_RE = r"(?:19|20)\d{2}[a-z]?"

PAREN_BLOCK_RE = re.compile(r"\(([^()\n]{1,300})\)")
AUTHOR_YEAR_IN_BLOCK_RE = re.compile(
    rf"(?P<author>[A-Za-z가-힣][A-Za-z가-힣 .,&·\-]*?)(?:,|\s)\s*(?P<year>{YEAR_RE})",
    re.IGNORECASE,
)
NARRATIVE_CITATION_RE = re.compile(
    rf"(?P<author>(?:[A-Z][A-Za-z\-]+(?:\s+(?:et\s+al\.|and|&)\s*[A-Z]?[A-Za-z\-]*)*|"
    rf"[가-힣]{{1,8}}(?:\s*(?:등|외))?))\s*\(\s*(?P<year>{YEAR_RE})\s*\)",
    re.IGNORECASE,
)

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
        re.compile(r"할\s+수\s+있을\s+것으로\s+(?:판단|기대|예상|추정)(?:된다|되었다)"),
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

STOPWORDS = {
    "은", "는", "이", "가", "을", "를", "의", "에", "에서", "로", "으로", "와", "과",
    "도", "만", "및", "또는", "그리고", "이며", "이고", "이다", "있다", "하였다", "한다",
    "the", "a", "an", "of", "in", "on", "and", "or", "to", "for", "was", "were", "is", "are",
}
PARTICLE_SUFFIXES = (
    "으로부터", "에서부터", "에게서", "으로써", "으로서", "에서는", "으로는", "까지", "부터",
    "에서", "에게", "한테", "으로", "로", "과", "와", "은", "는", "이", "가", "을", "를", "의", "도", "만",
)


@dataclass(frozen=True)
class NumericOccurrence:
    normalized: str
    raw: str
    start: int
    end: int
    anchor: str | None


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


def _normalize_numeric(raw: str) -> str:
    value = raw.strip()
    value = value.replace(",", "")
    value = value.replace("−", "-").replace("–", "-").replace("—", "-")
    value = value.replace("℃", "°C").replace("μ", "µ")
    value = re.sub(r"\s+", "", value)
    return value.lower()


def _strip_particle(token: str) -> str:
    lower = token.lower()
    for suffix in PARTICLE_SUFFIXES:
        if len(lower) > len(suffix) + 1 and lower.endswith(suffix):
            lower = lower[: -len(suffix)]
            break
    return lower


def _meaningful_tokens(text: str) -> list[str]:
    result: list[str] = []
    for raw in WORD_RE.findall(text):
        normalized = _strip_particle(raw)
        # Preserve single-letter labels such as A/B even though ``a`` is an
        # English stopword.
        if len(raw) == 1 and raw.isascii() and raw.isalpha() and raw.isupper():
            result.append(normalized)
        elif normalized and normalized not in STOPWORDS:
            result.append(normalized)
    return result


def _anchor_for(sentence: str, start: int, end: int) -> str | None:
    # Prefer the nearest meaningful token on the left within the current clause.
    left = sentence[max(0, start - 60):start]
    left = re.split(r"[,;:()\[\]{}]|(?:그리고|그러나|반면|한편)", left)[-1]
    tokens = _meaningful_tokens(left)
    if tokens:
        return tokens[-1]

    # If the value starts a clause, use the nearest meaningful token on the right.
    right = sentence[end:min(len(sentence), end + 60)]
    right = re.split(r"[,;:()\[\]{}]|(?:그리고|그러나|반면|한편)", right)[0]
    tokens = _meaningful_tokens(right)
    return tokens[0] if tokens else None


def _numeric_occurrences(sentence: str) -> list[NumericOccurrence]:
    items: list[NumericOccurrence] = []
    for match in NUMERIC_EXPR_RE.finditer(sentence):
        raw = match.group("expr")
        items.append(
            NumericOccurrence(
                normalized=_normalize_numeric(raw),
                raw=raw,
                start=match.start(),
                end=match.end(),
                anchor=_anchor_for(sentence, match.start(), match.end()),
            )
        )
    return items


def _numeric_counter(text: str) -> Counter[str]:
    return Counter(item.normalized for sentence in _sentences(text) for item in _numeric_occurrences(sentence))


def _direct_quotes(text: str) -> Counter[str]:
    found: list[str] = []
    for pattern in DIRECT_QUOTE_RES:
        found.extend(re.sub(r"\s+", " ", item).strip() for item in pattern.findall(text))
    return Counter(found)


def _author_key(raw: str) -> str:
    raw = raw.lower()
    raw = re.sub(r"\b(?:and|et\s+al)\b|(?:및|와|과|등|외)", "", raw)
    return re.sub(r"[^a-z가-힣]", "", raw)


def _citation_keys(text: str) -> Counter[str]:
    keys: list[str] = []

    for block in PAREN_BLOCK_RE.findall(text):
        for match in AUTHOR_YEAR_IN_BLOCK_RE.finditer(block):
            author = _author_key(match.group("author"))
            if author:
                keys.append(f"{author}|{match.group('year').lower()}")

    for match in NARRATIVE_CITATION_RE.finditer(text):
        author = _author_key(match.group("author"))
        if author:
            keys.append(f"{author}|{match.group('year').lower()}")

    return Counter(keys)


def _sentences(text: str) -> list[str]:
    return [re.sub(r"\s+", " ", item).strip() for item in SENTENCE_RE.findall(text) if item.strip()]


def _content_tokens(sentence: str) -> set[str]:
    scrubbed = NUMERIC_EXPR_RE.sub(" ", sentence)
    return set(_meaningful_tokens(scrubbed))


def _sentence_similarity(left: str, right: str) -> float:
    lt = _content_tokens(left)
    rt = _content_tokens(right)
    if not lt and not rt:
        return 1.0
    jaccard = len(lt & rt) / max(1, len(lt | rt))
    sequence = SequenceMatcher(None, " ".join(sorted(lt)), " ".join(sorted(rt)), autojunk=False).ratio()
    return 0.65 * jaccard + 0.35 * sequence


def _numeric_binding_counter(sentence: str) -> Counter[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for item in _numeric_occurrences(sentence):
        if item.anchor:
            pairs.append((item.anchor, item.normalized))
    return Counter(pairs)


def _numeric_binding_issues(before: str, after: str) -> list[dict[str, object]]:
    before_sentences = [s for s in _sentences(before) if _numeric_occurrences(s)]
    after_sentences = [s for s in _sentences(after) if _numeric_occurrences(s)]
    issues: list[dict[str, object]] = []
    used_after: set[int] = set()

    for before_index, before_sentence in enumerate(before_sentences, start=1):
        candidates = [
            (idx, _sentence_similarity(before_sentence, after_sentence))
            for idx, after_sentence in enumerate(after_sentences)
            if idx not in used_after
        ]
        if not candidates:
            issues.append(
                {
                    "gate": "P1b-binding",
                    "level": "warn",
                    "message": "수치가 포함된 원문 문장의 대응 문장을 찾지 못했습니다.",
                    "before_sentence": before_sentence,
                }
            )
            continue

        best_idx, score = max(candidates, key=lambda item: item[1])
        after_sentence = after_sentences[best_idx]
        if score < 0.28:
            issues.append(
                {
                    "gate": "P1b-binding",
                    "level": "warn",
                    "message": "수치-대상 결합을 기계적으로 대응시키기 어렵습니다. 수동 검토가 필요합니다.",
                    "similarity": round(score, 4),
                    "before_sentence": before_sentence,
                    "candidate_after_sentence": after_sentence,
                }
            )
            continue

        used_after.add(best_idx)
        before_pairs = _numeric_binding_counter(before_sentence)
        after_pairs = _numeric_binding_counter(after_sentence)
        if before_pairs and after_pairs and before_pairs != after_pairs:
            issues.append(
                {
                    "gate": "P1b-binding",
                    "level": "abort",
                    "message": "유사 문장 안에서 수치와 연결 대상의 결합이 변경되었습니다.",
                    "similarity": round(score, 4),
                    "before": [list(item) for item in before_pairs.elements()],
                    "after": [list(item) for item in after_pairs.elements()],
                    "before_sentence": before_sentence,
                    "after_sentence": after_sentence,
                }
            )

    return issues


def _touch_rate(before: str, after: str) -> tuple[float, int, int]:
    sentences = _sentences(before)
    if not sentences:
        return 0.0, 0, 0
    after_flat = re.sub(r"\s+", " ", after)
    touched = sum(sentence not in after_flat for sentence in sentences)
    return touched / len(sentences), touched, len(sentences)


def _counter_diff(before: Counter[str] | Iterable[str], after: Counter[str] | Iterable[str]) -> tuple[list[str], list[str]]:
    left = before if isinstance(before, Counter) else Counter(before)
    right = after if isinstance(after, Counter) else Counter(after)
    return sorted((left - right).elements()), sorted((right - left).elements())


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


def _counter_report(counter: Counter[str]) -> list[str]:
    return sorted(counter.elements())


def verify(
    before: str,
    after: str,
    mode: str = "deep",
    ignore_markup: bool = False,
) -> tuple[int, dict[str, object]]:
    if mode not in {"light", "deep"}:
        raise ValueError(f"unsupported mode: {mode}")

    issues: list[dict[str, object]] = []
    rate = _change_rate(before, after, ignore_markup)

    if mode == "light":
        if rate >= ABORT_RATE:
            issues.append({"gate": "P0", "level": "abort", "message": "light 모드 변경률이 50% 이상입니다."})
        elif rate >= WARN_RATE:
            issues.append({"gate": "P0", "level": "warn", "message": "light 모드 변경률이 30% 이상입니다."})

    before_numeric = _numeric_counter(before)
    after_numeric = _numeric_counter(after)
    removed_numeric, added_numeric = _counter_diff(before_numeric, after_numeric)
    if removed_numeric or added_numeric:
        issues.append(
            {
                "gate": "P1-numeric-expressions",
                "level": "abort",
                "message": "부호·비교연산자·값·불확도·단위를 포함한 수치표현이 변경되었습니다.",
                "removed": removed_numeric,
                "added": added_numeric,
            }
        )

    # Run binding checks even when the global multiset matches; this catches
    # A=10/B=20 -> A=20/B=10 swaps.
    issues.extend(_numeric_binding_issues(before, after))

    before_quotes = _direct_quotes(before)
    after_quotes = _direct_quotes(after)
    removed_quotes, added_quotes = _counter_diff(before_quotes, after_quotes)
    if removed_quotes or added_quotes:
        issues.append(
            {
                "gate": "P2-direct-quotes",
                "level": "abort",
                "message": "직접 인용 내용 또는 반복 횟수가 변경되었습니다.",
                "removed": removed_quotes,
                "added": added_quotes,
            }
        )

    before_citations = _citation_keys(before)
    after_citations = _citation_keys(after)
    removed_citations, added_citations = _counter_diff(before_citations, after_citations)
    if removed_citations or added_citations:
        issues.append(
            {
                "gate": "P2-citations",
                "level": "abort",
                "message": "저자-연도 인용 또는 반복 횟수가 변경되었습니다.",
                "removed": removed_citations,
                "added": added_citations,
            }
        )

    before_bracketed = Counter(CORNER_BRACKET_RE.findall(before))
    after_bracketed = Counter(CORNER_BRACKET_RE.findall(after))
    removed_bracketed, added_bracketed = _counter_diff(before_bracketed, after_bracketed)
    if removed_bracketed or added_bracketed:
        issues.append(
            {
                "gate": "P2-named-spans",
                "level": "abort",
                "message": "법령명·서명 등 보호 항목이 변경되었습니다.",
                "removed": removed_bracketed,
                "added": added_bracketed,
            }
        )

    protected_patterns: dict[str, re.Pattern[str]] = {
        "footnote_markers": FOOTNOTE_MARK_RE,
        "footnote_definitions": FOOTNOTE_DEF_RE,
        "figure_table_refs": FIGURE_REF_RE,
    }
    protected_report: dict[str, object] = {}
    for name, pattern in protected_patterns.items():
        before_items = Counter(pattern.findall(before))
        after_items = Counter(pattern.findall(after))
        removed, added = _counter_diff(before_items, after_items)
        protected_report[name] = {"removed": removed, "added": added}
        if removed or added:
            issues.append(
                {
                    "gate": f"P2-{name}",
                    "level": "abort",
                    "message": f"보호 항목이 변경되었습니다: {name}",
                    "removed": removed,
                    "added": added,
                }
            )

    before_headings = Counter(HEADING_RE.findall(before))
    after_headings = Counter(HEADING_RE.findall(after))
    removed_headings, added_headings = _counter_diff(before_headings, after_headings)
    if removed_headings or added_headings:
        issues.append(
            {
                "gate": "P2-headings",
                "level": "warn",
                "message": "헤딩 구성이 변경되었습니다. 의도된 구조 변경인지 확인해야 합니다.",
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
                    "message": f"문체 신호가 남거나 증가했습니다: {signal_id}",
                    "before": before_count,
                    "after": after_count,
                    "severity": severity,
                }
            )

    touch_rate, touched, sentence_count = _touch_rate(before, after)
    levels = {str(issue["level"]) for issue in issues}
    exit_code = 2 if "abort" in levels else 1 if "warn" in levels else 0
    verdict = "ABORT" if exit_code == 2 else "WARN" if exit_code == 1 else "MECHANICAL_PASS"

    report: dict[str, object] = {
        "verdict": verdict,
        "exit_code": exit_code,
        "mode": mode,
        "change_rate": round(rate, 6),
        "change_rate_is_blocking": mode == "light",
        "sentence_touch_rate": round(touch_rate, 6),
        "sentences_touched": touched,
        "sentence_count": sentence_count,
        "numeric_expressions": {
            "before": _counter_report(before_numeric),
            "after": _counter_report(after_numeric),
            "removed": removed_numeric,
            "added": added_numeric,
        },
        "direct_quotes": {"removed": removed_quotes, "added": added_quotes},
        "citations": {"removed": removed_citations, "added": added_citations},
        "named_spans": {"removed": removed_bracketed, "added": added_bracketed},
        "protected": protected_report,
        "headings": {"removed": removed_headings, "added": added_headings},
        "register": register,
        "style_signals": {"before": before_signals, "after": after_signals},
        "issues": issues,
        "semantic_validation": "not_performed",
        "factual_validation": "not_performed",
        "authorship_inference": "not_performed",
    }
    return exit_code, report


def main(argv: list[str] | None = None) -> int:
    _configure_utf8_stdout()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before", required=True, help="UTF-8 file containing the original body")
    parser.add_argument("--after", required=True, help="UTF-8 file containing the revised body")
    parser.add_argument("--mode", choices=("light", "deep"), default="deep")
    parser.add_argument("--json-out", help="Write the complete JSON report to this path")
    parser.add_argument("--ignore-markup", action="store_true", help="Ignore basic Markdown in change-rate calculation")
    args = parser.parse_args(argv)

    try:
        before = _read(args.before)
        after = _read(args.after)
        exit_code, report = verify(before, after, mode=args.mode, ignore_markup=args.ignore_markup)
        if args.json_out:
            target = Path(args.json_out)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(
            f"{report['verdict']}: mode={report['mode']} / "
            f"변경률 {float(report['change_rate']) * 100:.1f}% / "
            f"문장 터치율 {float(report['sentence_touch_rate']) * 100:.1f}% / "
            f"이슈 {len(report['issues'])}건"
        )
        for issue in report["issues"]:
            print(f"- [{str(issue['level']).upper()}] {issue['gate']}: {issue['message']}")
        if exit_code == 0:
            print("- 의미·논리·사실 검증은 수행되지 않았습니다. 수동 감사를 계속하십시오.")
        return exit_code
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"ERROR: 기계 보존 게이트를 실행하지 못했습니다: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
