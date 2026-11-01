#!/usr/bin/env python3
"""Print phrasebank sections by ID, or search them.

  python scripts/lookup.py INT-09 DIS-03     # whole sections
  python scripts/lookup.py --grep "gap in"   # matching items with their IDs
"""
import argparse
import re
import sys
from pathlib import Path

BANK = Path(__file__).resolve().parent.parent / "references" / "bank"


def load_sections():
    sections = {}
    for path in sorted(BANK.glob("*.md")):
        current = None
        for line in path.read_text(encoding="utf-8").splitlines():
            match = re.match(r"## ([A-Z]{3}-\d{2}) (.*)", line)
            if match:
                current = match.group(1)
                sections[current] = [line]
            elif current and line.strip():
                sections[current].append(line)
    return sections


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("ids", nargs="*")
    parser.add_argument("--grep")
    args = parser.parse_args()
    sections = load_sections()

    unknown = [i for i in args.ids if i not in sections]
    if unknown:
        sys.exit(f"Unknown IDs: {', '.join(unknown)}")
    for sid in args.ids:
        print("\n".join(sections[sid]), end="\n\n")
    if args.grep:
        pattern = re.compile(args.grep, re.IGNORECASE)
        for sid, lines in sections.items():
            for line in lines[1:]:
                if pattern.search(line):
                    print(f"{sid}: {line[2:]}")


if __name__ == "__main__":
    main()
