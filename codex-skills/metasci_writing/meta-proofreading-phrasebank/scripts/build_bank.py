#!/usr/bin/env python3
"""Rebuild references/bank/*.md and references/function_index.md from
data/Academic_phrasebank.md, then fail if any source line went missing.

Run: python scripts/build_bank.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "Academic_phrasebank.md"
BANK = ROOT / "references" / "bank"
INDEX = ROOT / "references" / "function_index.md"

PARTS = {
    "Introducing work": ("INT", "서론"),
    "Referring to sources": ("SRC", "선행연구 인용"),
    "Describing methods": ("MTH", "방법"),
    "Reporting results": ("RES", "결과"),
    "Discussing findings": ("DIS", "논의"),
    "Writing conclusions": ("CCL", "결론"),
    "Being cautious": ("CAU", "신중한 표현"),
    "Being critical": ("CRI", "비판"),
    "Classifying and listing": ("CLS", "분류·나열"),
    "Compare and contrast": ("CMP", "비교·대조"),
    "Defining terms": ("DEF", "용어 정의"),
    "Describing trends": ("TRD", "추세"),
    "Describing quantities": ("QTY", "수량"),
    "Explaining causality": ("CAS", "인과"),
    "Giving examples": ("EXA", "예시"),
    "Signalling transition": ("TRN", "전환"),
    "Writing about the past": ("PST", "과거·시제"),
}
FOOTER = {
    "Contact Us", "Connect With Us", "Find Us", "Oxford Rd", "Manchester",
    "M13 9PL", "The University of Manchester", "+44 (0) 161 306 6000",
}
TERMINAL = ("…", ".", "?", "…’", ".’")


def is_blank(line):
    return not line.replace(" ", " ").strip()


def clean(line):
    return re.sub(r"\s+", " ", line.replace(" ", " ")).strip()


def stem_start(bullets):
    """Index where the first table column begins inside a leading bullet run.

    The export kept full sentences and a table's first column in one run, so
    the column is the trailing stretch of items that do not end a sentence.
    """
    start = len(bullets) - 1
    while start > 0:
        prev, cur = bullets[start - 1], bullets[start]
        too_long = len(prev.split()) > max(6, 2 * len(cur.split()))
        if prev.endswith(TERMINAL) or too_long:
            break
        start -= 1
    return start


def parse_block(lines):
    """Turn one blank-delimited block into sentences and at most one frame."""
    cols, current = [], []
    for line in lines:
        if line.startswith("- "):
            current.append(line[2:].strip())
        else:
            if current:
                cols.append(current)
            current = [line]
    cols.append(current)

    leading_bullets = lines[0].startswith("- ")
    if len(cols) == 1:
        return cols[0], None
    sentences = []
    if leading_bullets:
        start = stem_start(cols[0])
        sentences, cols[0] = cols[0][:start], cols[0][start:]
    return sentences, cols


def parse_section(lines):
    items, block = [], []

    def flush():
        if block:
            sentences, frame = parse_block(block)
            items.extend(("S", s) for s in sentences)
            if frame:
                items.append(("F", frame))
            block.clear()

    # "- break" is a line break inside a table cell, not a separator.
    kept = [r for r in lines if clean(r) not in ("- break", "-")]
    for i, raw in enumerate(kept):
        if not is_blank(raw):
            block.append(clean(raw))
            continue
        # A plain empty line before a lowercase or numeric cell sits inside a
        # table; tables themselves are separated by NBSP or capitalised starts.
        following = next((r for r in kept[i + 1:] if not is_blank(r)), "")
        inside_table = " " not in raw and re.match(r"[a-z0-9]", clean(following))
        if not inside_table:
            flush()
    flush()
    return items


def render_item(kind, value):
    if kind == "S":
        return f"- {value}"
    columns = [list(dict.fromkeys(c)) for c in value]
    slots = [c[0] if len(c) == 1 else "{" + " | ".join(c) + "}" for c in columns]
    return "- " + " ".join(slots)


def parse_source(text):
    parts, part, section = [], None, None
    for raw in text.split("\n"):
        line = clean(raw)
        if line.startswith("# ") or line == "---":
            continue
        if line.startswith("## "):
            part = {"title": line[3:], "url": "", "notes": [], "sections": []}
            parts.append(part)
            section = None
        elif line.startswith("### "):
            section = {"title": line[4:], "lines": []}
            part["sections"].append(section)
        elif part is None or line.strip("_") in FOOTER:
            continue
        elif line.startswith("<http"):
            part["url"] = line.strip("<>")
        elif line.startswith("* ") or (section and line.startswith("_")):
            part["notes"].append(line.strip("_"))
        elif section:
            section["lines"].append(raw)
        elif line:
            part["notes"].append(line.strip("_"))
    return parts


def write_outputs(parts):
    BANK.mkdir(parents=True, exist_ok=True)
    rows = ["# Function index", "",
            "문장 기능을 판별한 뒤 ID로 조회한다: "
            "`python scripts/lookup.py INT-09 DIS-03`", ""]
    total_s = total_f = 0
    for part in parts:
        code, korean = PARTS[part["title"]]
        out = [f"# {part['title']} ({code})", ""]
        if part["url"]:
            out += [f"Source: {part['url']}", ""]
        out += [f"> {note}" for note in part["notes"]]
        rows += [f"## {code} {part['title']} / {korean}", ""]
        for n, section in enumerate(part["sections"], 1):
            sid = f"{code}-{n:02d}"
            seen, body = set(), []
            for kind, value in parse_section(section["lines"]):
                text = render_item(kind, value)
                if text not in seen:
                    seen.add(text)
                    body.append(text)
                    total_s += kind == "S"
                    total_f += kind == "F"
            out += ["", f"## {sid} {section['title']}", ""] + body
            rows.append(f"- {sid} {section['title']} ({len(body)})")
        rows.append("")
        (BANK / f"{code}.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    INDEX.write_text("\n".join(rows), encoding="utf-8")
    return total_s, total_f


def check_coverage(text):
    """Every content line of the source must survive verbatim somewhere."""
    built = " ".join(p.read_text(encoding="utf-8") for p in BANK.glob("*.md"))
    built = clean(built)
    missing = []
    for number, raw in enumerate(text.split("\n"), 1):
        line = clean(raw)
        if not line or line in ("---", "- break", "-"):
            continue
        if line.startswith(("# ", "## ", "### ")):
            continue
        if line.strip("_") in FOOTER:
            continue
        body = line[2:].strip() if line.startswith("- ") else line
        body = body.strip("_<>")
        if body not in built:
            missing.append((number, body))
    return missing


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    text = SOURCE.read_text(encoding="utf-8")
    parts = parse_source(text)
    unknown = [p["title"] for p in parts if p["title"] not in PARTS]
    if unknown:
        sys.exit(f"Unknown parts: {unknown}")
    sentences, frames = write_outputs(parts)
    missing = check_coverage(text)
    sections = sum(len(p["sections"]) for p in parts)
    print(f"parts={len(parts)} sections={sections} "
          f"sentences={sentences} frames={frames} missing={len(missing)}")
    for number, body in missing[:20]:
        print(f"  MISSING line {number}: {body}")
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
