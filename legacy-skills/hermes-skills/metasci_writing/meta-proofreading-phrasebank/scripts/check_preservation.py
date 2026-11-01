#!/usr/bin/env python3
"""Fail if a revision changed numbers, citations, names, or hedging strength.

Run: python scripts/check_preservation.py original.txt revised.txt
"""
import re
import sys
from collections import Counter
from pathlib import Path

CHECKS = {
    "numbers": r"(?<![\w.])\d+(?:[.,]\d+)*\s?%?",
    "citations": r"\([^()]*\b(?:19|20)\d{2}[a-z]?[^()]*\)|\[\d+(?:\s*[-–,]\s*\d+)*\]",
    "hedges": r"\b(?:may|might|could|would|can|cannot|likely|possibly|perhaps"
              r"|probably|suggests?|suggested|appears?|seems?|indicates?"
              r"|indicated)\b",
    "boosters": r"\b(?:proves?|proved|demonstrates?|demonstrated|shows?|showed"
                r"|confirms?|confirmed|clearly|certainly|undoubtedly)\b",
    "negation": r"\b(?:not|no|never|neither|nor|without|cannot|little|few)\b",
}
# "not much is known" and "little is known" are the same claim, so negation is
# compared by count; a dropped negation still fails.
COUNT_ONLY = {"negation"}


def tokens(text, pattern):
    found = re.findall(pattern, text, flags=re.IGNORECASE)
    return Counter(re.sub(r"\s+", " ", t).strip().lower() for t in found)


def names(text):
    """Capitalised words and acronyms, ignoring ordinary sentence openers."""
    body = re.sub(r"(^|[.!?]\s+)[A-Z][a-z]+\b", r"\1", text)
    return Counter(re.findall(r"\b[A-Z][\w-]*", body))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    original = Path(sys.argv[1]).read_text(encoding="utf-8")
    revised = Path(sys.argv[2]).read_text(encoding="utf-8")
    failed = False
    for name, pattern in CHECKS.items():
        before, after = tokens(original, pattern), tokens(revised, pattern)
        removed = list((before - after).elements())
        added = list((after - before).elements())
        same_count = sum(before.values()) == sum(after.values())
        if name in COUNT_ONLY and same_count:
            print(f"PASS {name}")
        elif removed or added:
            failed = True
            print(f"FAIL {name}: removed={removed} added={added}")
        else:
            print(f"PASS {name}")
    before, after = names(original), names(revised)
    if before == after:
        print("PASS names")
    else:
        failed = True
        print(f"FAIL names: removed={list((before - after).elements())} "
              f"added={list((after - before).elements())}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
