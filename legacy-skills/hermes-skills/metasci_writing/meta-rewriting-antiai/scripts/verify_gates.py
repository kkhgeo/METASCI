#!/usr/bin/env python3
"""meta-rewriting-antiai 결정적 사후 게이트 (LLM 콜 0, stdlib 전용).

epoko77-ai/im-not-ai(MIT) humanize-korean v2.3의 verify_gates.py 설계를
이 스킬에 맞게 축소 이식. LLM 자가 채점은 참고값이고, 과윤문·수치 훼손의
확정 판정은 이 스크립트가 한다. 문자 diff는 구조 편집에 눈이 없으므로
(원본 실측: 문자율 2.77% 뒤에 문장 터치율 29.7%·대구 -75% 은닉),
문자율에 수치 보존·대구 전멸·터치율 축을 더해 사각지대를 보완한다.

축:
    P0 변경률   — 공백 정규화 후 문자 단위 diff. WARN 30% / ABORT 50%.
    P1 수치보존 — 원문의 숫자 토큰 소실(경고)·신규 주입(경고 — 날조 위험).
    P2 대구전멸 — C-8 대구가 원문 5회+인데 0으로 전멸하면 경고(과교정).
    P3 터치율   — 원문 문장 중 결과에 그대로 없는 비율. 보고 전용.

Exit code:
    0 — 수렴 / 1 — 경고(사용자 고지 필요) / 2 — 중단(변경률 >= 50%,
    교정본 채택 금지) / 3 — 실행 오류(판정 불가. 게이트를 건너뛰지 않는다)

CLI:
    python3 scripts/verify_gates.py --before original.md --after naturalized.md
    옵션: --json (구조화 출력 병기)
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys

# Windows 콘솔(cp949)에서 한국어·대시 출력이 깨지지 않도록 UTF-8 강제
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

CHANGE_RATE_WARN = 0.30
CHANGE_RATE_ABORT = 0.50
ANNIHILATION_MIN_BEFORE = 5

_WS_RE = re.compile(r"\s+")
# 숫자 토큰: 정수·소수·천단위 콤마·백분율 등 ("1,234", "3.14", "95%")
_NUM_RE = re.compile(r"\d[\d,.]*%?")
# C-8 대구 시그니처 (한국어 + 영어 부정 병렬)
_ANTITHESIS_RES = (
    re.compile(r"[가이]\s?아니라"),
    re.compile(r"[가이]\s?아닌"),
    re.compile(r"인가[,?]"),
    re.compile(r"\bnot\s+(?:just|only|merely|simply)\b", re.IGNORECASE),
)
_SENT_SPLIT_RE = re.compile(r"(?<=[.!?다])\s+")


def _read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _norm(text: str) -> str:
    return _WS_RE.sub(" ", text).strip()


def change_rate(before: str, after: str) -> float:
    sm = difflib.SequenceMatcher(None, _norm(before), _norm(after), autojunk=False)
    return 1.0 - sm.ratio()


def number_tokens(text: str) -> list[str]:
    return [t.rstrip(".,") for t in _NUM_RE.findall(text)]


def _multiset_diff(a: list[str], b: list[str]) -> list[str]:
    remain = list(b)
    out = []
    for t in a:
        if t in remain:
            remain.remove(t)
        else:
            out.append(t)
    return out


def antithesis_count(text: str) -> int:
    return sum(len(r.findall(text)) for r in _ANTITHESIS_RES)


def sentence_touch_rate(before: str, after: str) -> tuple[float, int, int]:
    before_sents = [_norm(s) for s in _SENT_SPLIT_RE.split(before) if _norm(s)]
    if not before_sents:
        return 0.0, 0, 0
    after_set = {_norm(s) for s in _SENT_SPLIT_RE.split(after)}
    touched = sum(1 for s in before_sents if s not in after_set)
    return touched / len(before_sents), touched, len(before_sents)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="anti-AI 교정 결정적 게이트")
    p.add_argument("--before", required=True, help="원문 경로")
    p.add_argument("--after", required=True, help="교정본 경로")
    p.add_argument("--json", action="store_true", help="구조화 JSON 출력 병기")
    args = p.parse_args(argv)

    try:
        before = _read(args.before)
        after = _read(args.after)
    except OSError as e:
        print(f"error: 파일 읽기 실패: {e}", file=sys.stderr)
        return 3

    report: dict = {}
    warn = False

    # P0 변경률
    rate = change_rate(before, after)
    abort = rate >= CHANGE_RATE_ABORT
    if CHANGE_RATE_WARN <= rate < CHANGE_RATE_ABORT:
        warn = True
    p0 = ("ABORT — 교정본 채택 금지" if abort
          else "WARN — 과교정 경고" if rate >= CHANGE_RATE_WARN else "OK")
    report["change_rate"] = {"rate": round(rate, 4), "verdict": p0}
    print(f"[P0 변경률] {rate * 100:.1f}% — {p0} "
          f"(경고 {CHANGE_RATE_WARN * 100:.0f}% / 중단 {CHANGE_RATE_ABORT * 100:.0f}%)")

    # P1 수치 보존
    nums_before = number_tokens(before)
    nums_after = number_tokens(after)
    dropped = _multiset_diff(nums_before, nums_after)
    injected = _multiset_diff(nums_after, nums_before)
    if injected:
        warn = True  # 원문에 없던 수치 = 날조 위험. 반드시 사람 확인.
    if dropped:
        warn = True
    report["numbers"] = {"dropped": dropped, "injected": injected}
    if dropped or injected:
        print(f"[P1 수치보존] WARN — 소실 {dropped or '없음'} / 주입 {injected or '없음'} "
              f"(주입은 날조 위험 — 반드시 원문 대조)")
    else:
        print(f"[P1 수치보존] OK ({len(nums_before)}개 토큰 전체 보존)")

    # P2 대구 전멸
    anti_before = antithesis_count(before)
    anti_after = antithesis_count(after)
    annihilated = anti_before >= ANNIHILATION_MIN_BEFORE and anti_after == 0
    warn = warn or annihilated
    report["antithesis"] = {"before": anti_before, "after": anti_after,
                            "annihilated": annihilated}
    p2 = ("FAIL — 전멸(과교정)" if annihilated
          else "OK" if anti_before >= ANNIHILATION_MIN_BEFORE
          else f"스킵 (원문 대구 {anti_before} < {ANNIHILATION_MIN_BEFORE})")
    print(f"[P2 대구] {anti_before} → {anti_after} — {p2}")

    # P3 터치율 (보고 전용)
    touch, touched, total = sentence_touch_rate(before, after)
    report["sentence_touch"] = {"rate": round(touch, 4),
                                "touched": touched, "total": total}
    print(f"[P3 터치율] {touch * 100:.1f}% ({touched}/{total} 문장) — 보고 전용")

    if abort:
        verdict, code = "ABORT — 중단. 교정본 채택 금지", 2
    elif warn:
        verdict, code = "WARN — 경고. 사용자 고지 필요", 1
    else:
        verdict, code = "OK — 수렴", 0
    report["gate"] = {"verdict": verdict, "exit_code": code}
    print(f"gate: {verdict}")

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
