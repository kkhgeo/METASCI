#!/usr/bin/env python3
"""preservation_inventory.py — mechanical content-preservation gate (meta-styling Gate 1).

Compares two prose-only files, the original and a revision, on four inventories:

  figure / table / equation   display-item references; panels, supplements and ranges
                              are expanded ("Fig. 1B–D" -> 1b, 1c, 1d)
  citation                    author-year keys ("smith et al.:2020") or numeric bracket
                              keys ("[3–5]" -> 3, 4, 5), one per cited source
  number                      numeric expressions with sign, decimals, exponent, range,
                              uncertainty and percent kept intact
  identifier                  letter-digit tokens that are neither of the above:
                              δ15N, NO3-N, Ca2+, PC1, 10th, A-02, 10⁻³, km2

Every item's occurrence count must be equal on both sides.

  exit 0  PASS     every count equal
  exit 1  FAIL     a count differs (an item was lost, added or changed)
  exit 2  BLOCKED  the notation could not be identified reliably, or an input is unusable

PASS is a mechanical result. It does not certify meaning (that is Gate 2) and it does
not prove parser coverage: inspect the extracted keys in the TSV against the prose.
"note" rows are for inspection only and never change the result.

Usage:
  python preservation_inventory.py --before 0-draft.prose.txt --after revision.txt \
      --citation-style author-year|numeric|none --output inventory.tsv

No dependencies beyond the standard library. Standalone: quant_check.py is not touched.
Version: 1.0.0 (2026-09-14)
"""
import argparse
import csv
import io
import re
import sys
from collections import Counter
from pathlib import Path

SUP = "²³¹⁰-₟"          # superscript/subscript digits and signs
DASH = r"\-–−"                           # hyphen, en dash, minus sign (class-safe)
DASH_CHARS = "-–−"

# --- display-item references -------------------------------------------------------
REF_WORD = r"(?:Figures?|Figs?\.?|Tables?|Eqs?\.?|Equations?)"
NUM_ITEM = r"\(?S?\d+(?:\.\d+)?(?:\([A-Za-z]\)|[A-Za-z])?\)?"   # 2  S1  4A  2(a)  (2)  3.4
LET_ITEM = r"\([A-Za-z]\)|[A-Z](?![A-Za-z])|(?<=[" + DASH + r"])\s*[a-z](?![A-Za-z])"
ITEM = r"(?:" + NUM_ITEM + r"|" + LET_ITEM + r")"
CONN = r"\s*(?:[" + DASH + r"]|,|;?\s*and\b|&)\s*"
REF = re.compile(r"\b(" + REF_WORD + r")\s*(" + NUM_ITEM + r"(?:" + CONN + ITEM + r")*)", re.I)
REF_MARK = re.compile(r"\b" + REF_WORD + r"\b\s*\(?(?=S?\d)", re.I)
SINGULAR = {"figure", "fig", "fig.", "table", "eq", "eq.", "equation"}

# --- citations ---------------------------------------------------------------------
NAME = r"[A-ZÀ-ÖØ-Þ][\w’'\-]+"
AUTHOR = NAME + r"(?:\s+et\s+al\.?|\s+(?:and|&)\s+" + NAME + r")?"
YEAR = r"(?:18|19|20|21)\d{2}[a-z]?"
CITE = re.compile(r"(?P<author>" + AUTHOR + r")(?:\s*,\s*|\s*\(\s*)(?P<years>" + YEAR
                  + r"(?:\s*,\s*" + YEAR + r")*)\s*\)?")
PARTICLE = r"(?i:van|von|de|del|da|der|den|di|la|le|du|le)"   # name particles only

# --- numbers -----------------------------------------------------------------------
ATOM = r"[+\-−]?(?:\d{1,3}(?:,\d{3})+|\d+|\.\d+)(?:\.\d+)?(?:[eE][+\-−]?\d+)?"
NUMBER = re.compile(
    r"(?<![\w." + DASH + SUP + r"])" + ATOM
    + r"(?:\s*(?:×|x)\s*10\s*\^\s*[+\-−]?\d+)?"
    + r"(?:\s*(?:–|—|to|±|\+/-|-)\s*" + ATOM + r")*"      # ranges and chains: 2–5, 11–12–10
    + r"(?:\s*%)?(?![\w" + SUP + r"]|\.\d)")

TOKEN = re.compile(r"[^\s,;:()\[\]{}\"“”'’]+")


def normal(text):
    text = re.sub(r"\s+", "", text)
    for ch in "–—−":
        text = text.replace(ch, "-")
    return text


def snippet(text, limit=80):
    """One-line, bounded excerpt for issue/note messages (keeps the TSV one row per line)."""
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= limit else text[:limit] + "…"


def has_digit(text):
    return any(ch.isdigit() for ch in text)


def expand_reference(word, body, issues):
    """Turn 'Fig. 1B–D', 'Figures 2–4', 'Eqs. (6) and (7)' into a list of identifiers."""
    kind = ("figure" if word.lower().startswith("fig") else
            "table" if word.lower().startswith("tab") else "equation")
    parts = re.split(r"(\s*(?:[" + DASH + r"]|,|;?\s*and\b|&)\s*)", body)
    items, last_num, last_conn = [], None, ""
    for i, part in enumerate(parts):
        if i % 2:                                       # a connector
            last_conn = "-" if re.search(r"[" + DASH + r"]", part) else ","
            continue
        raw = re.sub(r"[()]", "", part.strip())
        if not raw:
            continue
        m = re.fullmatch(r"(S?)(\d+(?:\.\d+)?)([A-Za-z]?)", raw, re.I)
        if m:
            prefix, num, panel = m[1].upper(), m[2], m[3].lower()
            if word.lower() in SINGULAR and items:
                issues.append("ambiguous singular reference followed by a numeric list: "
                              + snippet(word + " " + body))
            item = (prefix, num, panel)
        elif re.fullmatch(r"[A-Za-z]", raw) and last_num:
            item = (last_num[0], last_num[1], raw.lower())   # bare panel letter
        else:
            issues.append("unsupported reference item: " + snippet(word + " " + body))
            return kind, []
        if last_conn == "-" and items:
            items.extend(expand_range(items.pop(), item, issues, snippet(word + " " + body)))
        else:
            items.append(item)
        last_num = item
        last_conn = ""
    return kind, [p + n + l for p, n, l in items]


def expand_range(lo, hi, issues, text):
    if lo[0] != hi[0] or "." in lo[1] or "." in hi[1]:
        issues.append("unsupported reference range: " + text)
        return [lo, hi]
    if lo[1] == hi[1] and lo[2] and hi[2]:                     # 2a–c  1B–D
        a, b = ord(lo[2]), ord(hi[2])
        if b < a or b - a > 25:
            issues.append("unsupported panel range: " + text)
            return [lo, hi]
        return [(lo[0], lo[1], chr(c)) for c in range(a, b + 1)]
    if not lo[2] and not hi[2]:                                # 2–4
        a, b = int(lo[1]), int(hi[1])
        if b < a or b - a > 50:
            issues.append("unsupported reference range: " + text)
            return [lo, hi]
        return [(lo[0], str(n), "") for n in range(a, b + 1)]
    issues.append("unsupported reference range: " + text)
    return [lo, hi]


def extract(text, style):
    counts, notes, issues, spans = Counter(), [], [], []
    text = text.replace("\x00", "")
    if not text.strip():
        issues.append("empty prose")
    if re.search(r"(?im)^\s*(?:applied:|---\s*$|```|\(unchanged from (?:the )?draft\))", text):
        issues.append("metadata, delimiter, code fence, or placeholder in prose input")

    def mask():
        chars = list(text)
        for start, end in spans:
            chars[start:end] = " " * (end - start)
        return "".join(chars)

    for m in REF.finditer(text):
        kind, idents = expand_reference(m[1], m[2], issues)
        for ident in idents:
            counts[(kind, ident.lower())] += 1
        spans.append(m.span())
    for m in REF_MARK.finditer(mask()):
        issues.append("unparsed reference near: " + snippet(text[m.start():m.start() + 30]))

    if style == "author-year":
        for m in CITE.finditer(mask()):
            if re.search(r"\b" + PARTICLE + r"\s+$", text[:m.start()]):
                issues.append("possibly truncated multiword author near: " + snippet(m[0]))
            author = re.sub(r"\s+", " ", m["author"].lower().replace("&", "and")).rstrip(".")
            for year in re.findall(YEAR, m["years"]):
                counts[("citation", author + ":" + year)] += 1
            spans.append(m.span())
        loose = re.findall(r"(?<![\w" + DASH + r"])" + YEAR + r"(?![\w" + DASH + r"])", mask())
        if loose:
            notes.append("years outside recognised citations, counted as numbers: "
                         + ", ".join(sorted(set(loose))))
        if re.search(r"\[\s*\d", mask()):
            issues.append("numeric bracket citation in author-year mode")
    elif style == "numeric":
        for m in re.finditer(r"\[([^\]]*)\]", mask()):
            if not re.fullmatch(r"\s*\d+(?:\s*(?:,|;|[" + DASH + r"])\s*\d+)*\s*", m[1]):
                # Brackets are also used for concentrations ([NO3-]) and matrices; only a
                # bracket that looks like a citation attempt is a blocking problem.
                if re.search(r"\bet al|" + YEAR, m[1]):
                    issues.append("unsupported bracket citation: " + snippet(m[0]))
                continue
            keys = []
            for part in re.split(r"[,;]", m[1]):
                nums = re.split(r"[" + DASH + r"]", part.strip())
                lo, hi = int(nums[0]), int(nums[-1])
                if len(nums) > 2 or hi < lo or hi - lo > 200:
                    issues.append("invalid numeric citation range: " + snippet(part))
                else:
                    keys.extend(range(lo, hi + 1))
            counts.update(("citation", str(key)) for key in keys)
            spans.append(m.span())
        if CITE.search(mask()):
            issues.append("author-year citation in numeric mode")
    elif CITE.search(mask()) or re.search(r"\[\s*\d", mask()):
        issues.append("citation detected in none mode")

    for m in NUMBER.finditer(mask()):
        counts[("number", normal(m[0]))] += 1
        spans.append(m.span())

    for m in TOKEN.finditer(mask()):
        token = m[0].strip(".,;:" + DASH_CHARS + "—")
        if has_digit(token):
            counts[("identifier", normal(token))] += 1
            spans.append(m.span())

    if has_digit(mask()):
        issues.append("unparsed digit remains: extractor extension required")
    return counts, notes, issues


def run(args):
    out = Path(args.output).resolve()
    if out in {Path(args.before).resolve(), Path(args.after).resolve()}:
        print("BLOCKED: output must not overwrite either prose input")
        return 2
    rows, notes, issues = [], [], []
    try:
        before, n1, i1 = extract(Path(args.before).read_text(encoding="utf-8-sig"), args.citation_style)
        after, n2, i2 = extract(Path(args.after).read_text(encoding="utf-8-sig"), args.citation_style)
        notes = ["before: " + x for x in n1] + ["after: " + x for x in n2]
        issues = ["before: " + x for x in i1] + ["after: " + x for x in i2]
        for kind, key in sorted(before.keys() | after.keys()):
            a, b = before[(kind, key)], after[(kind, key)]
            rows.append([kind, key, a, b, "PASS" if a == b else "FAIL"])
        status = "BLOCKED" if issues else "FAIL" if any(r[-1] == "FAIL" for r in rows) else "PASS"
    except (OSError, UnicodeError, ValueError) as exc:
        issues, status = [str(exc)], "BLOCKED"
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, delimiter="\t", lineterminator="\n")
    writer.writerow(["kind", "item", "before", "after", "result"])
    writer.writerows(rows)
    for note in notes:
        writer.writerow(["note", note, "", "", ""])
    for issue in issues:
        writer.writerow(["issue", issue, "", "", "BLOCKED"])
    writer.writerow(["overall", "mechanical inventory", "", "", status])
    report = buffer.getvalue()
    sys.stdout.write(report)
    try:
        out.write_text(report, encoding="utf-8")
    except OSError as exc:
        print("BLOCKED: could not save inventory: " + str(exc))
        status = "BLOCKED"
    return {"PASS": 0, "FAIL": 1, "BLOCKED": 2}[status]


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--before", required=True, help="original prose-only file")
    p.add_argument("--after", required=True, help="revised prose-only file")
    p.add_argument("--citation-style", required=True, choices=["author-year", "numeric", "none"])
    p.add_argument("--output", required=True, help="TSV audit path (also printed)")
    args = p.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(run(args))


if __name__ == "__main__":
    main()
