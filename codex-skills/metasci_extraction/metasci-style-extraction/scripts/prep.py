#!/usr/bin/env python3
"""prep.py — Stage 0 of metasci-style-extraction.

Turns one paper into the fixed on-disk layout every downstream lens reads:

    <corpus>/papers/<slug>/
        source.<ext>        copy of the input
        body.txt            NFKC-normalized, dehyphenated, references stripped
        sections/I.txt      Introduction
        sections/M.txt      Methods
        sections/R.txt      Results (or fused Results-and-Discussion)
        sections/D.txt      Discussion  (only when the paper separates it)
        sections/C.txt      Conclusions (only when the paper has one)
        prep.json           what was detected, what was measured, which version ran

WHY THIS EXISTS
---------------
Every lens used to read the PDF itself. That meant meeting the same text-layer
problems three times, and the worst of them is silent:

    Elsevier PDFs carry printer's ligatures (U+FB01 'fi', U+FB02 'fl').
    Against the raw PDF, `quant_check count` returns 0 for EVERY word
    containing them.  Measured on kkh_nitrate_iso.pdf (159 ligatures):
        fitted 0/21 · significant 0/17 · confidence 0/15 · first 0/13
        field 0/13 · difficult 0/7
    Those are core terms.  A style card built on the raw PDF is wrong and
    gives no sign of it.

NFKC normalization here fixes it once, for every lens, forever.

SECTION DETECTION
-----------------
Auto-detected from headings, then REPORTED.  If the paper's structure is not
found, prep.py stops and prints what it did see rather than guessing — a wrong
section split silently corrupts every per-section band downstream.
Override with --marks when auto-detection is wrong.

USAGE
-----
    py -3.10 prep.py paper.pdf --slug kim-2015-nitrate-iso --out Z:/.../SCI_kkh
    py -3.10 prep.py paper.pdf --slug s --out . --marks "M=Materials and methods,R=Results and discussion,C=Summary and conclusions"
    py -3.10 prep.py paper.pdf --slug s --out . --dry-run      # detect and report only
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

__version__ = "1.0.0"

# Windows consoles default to a legacy codepage (cp949/cp1252) that cannot encode
# the punctuation used below. Reconfigure rather than restrict the vocabulary.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Section IDs, in document order. D is optional (fused Results-and-Discussion is
# common); C is optional (some papers end on Discussion).
SECTION_ORDER = ["A", "I", "M", "R", "D", "C"]

# A is front matter (title, authors, abstract, keywords). It is written out so the
# abstract is available for its own analysis, but it is NEVER part of an IMRDC
# band: an abstract is a different genre and would skew every per-section rate.
BODY_SECTIONS = ["I", "M", "R", "D", "C"]

SECTION_NAMES = {
    "A": "Front matter / abstract",
    "I": "Introduction",
    "M": "Methods",
    "R": "Results",
    "D": "Discussion",
    "C": "Conclusions",
}

# Heading patterns, tried in order. Anchored to a line start so a mention of
# "the Discussion" inside a sentence never triggers a split.
HEADING_PATTERNS = {
    "I": [
        r"^\s*\d?\.?\s*Introduction\s*$",
        r"^\s*\d?\.?\s*INTRODUCTION\s*$",
    ],
    "M": [
        r"^\s*\d?\.?\s*Materials?\s+and\s+methods?\s*$",
        r"^\s*\d?\.?\s*Methods?\s+and\s+materials?\s*$",
        r"^\s*\d?\.?\s*(Materials?|Methods?|Methodology|Experimental)\s*$",
        r"^\s*\d?\.?\s*(MATERIALS AND METHODS|METHODS)\s*$",
        r"^\s*\d?\.?\s*Study\s+area\s+and\s+methods?\s*$",
    ],
    "R": [
        r"^\s*\d?\.?\s*Results?\s+and\s+discussions?\s*$",
        r"^\s*\d?\.?\s*Results?\s*$",
        r"^\s*\d?\.?\s*(RESULTS AND DISCUSSION|RESULTS)\s*$",
    ],
    "D": [
        r"^\s*\d?\.?\s*Discussions?\s*$",
        r"^\s*\d?\.?\s*DISCUSSION\s*$",
    ],
    "C": [
        r"^\s*\d?\.?\s*Summary\s+and\s+conclusions?\s*$",
        r"^\s*\d?\.?\s*Conclusions?\s+and\s+(outlook|implications?|recommendations?)\s*$",
        r"^\s*\d?\.?\s*Conclusions?\s*$",
        r"^\s*\d?\.?\s*Concluding\s+remarks\s*$",
        r"^\s*\d?\.?\s*(SUMMARY AND CONCLUSIONS|CONCLUSIONS?)\s*$",
    ],
}

# Everything from here on is back matter and is cut before splitting.
TAIL_PATTERNS = [
    r"^\s*Acknowledge?ments?\s*$",
    r"^\s*ACKNOWLEDGE?MENTS?\s*$",
    r"^\s*References\s*$",
    r"^\s*REFERENCES\s*$",
    r"^\s*Bibliography\s*$",
    r"^\s*Literature cited\s*$",
    r"^\s*Supplementary\s+(material|data|information)\s*$",
    r"^\s*Declaration of competing interest\s*$",
    r"^\s*CRediT authorship\s*$",
]


# --------------------------------------------------------------------------- #
# text pipeline
# --------------------------------------------------------------------------- #

def dehyphenate(text: str) -> str:
    """Repair words split by PDF line-break hyphenation.

    Same three rules as quant_check.dehyphenate — kept byte-identical in
    behaviour so prep output and quant_check counts never disagree."""
    text = re.sub(r"([a-z]) *-[ \t]*\n\s*([a-z])", r"\1\2", text)
    text = re.sub(r"([a-z])- +([a-z])", r"\1\2", text)
    text = re.sub(r"([a-z]) +- +([a-z])", r"\1\2", text)
    return text


def read_source(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError:
            try:
                from PyPDF2 import PdfReader  # type: ignore
            except ImportError:
                sys.exit(
                    f"prep.py: pypdf is not installed for {sys.executable}\n"
                    f"  install it with:  \"{sys.executable}\" -m pip install pypdf"
                )
        reader = PdfReader(str(path))
        raw = "\n".join(page.extract_text() or "" for page in reader.pages)
        return dehyphenate(raw)
    return path.read_text(encoding="utf-8", errors="replace")


def count_ligatures(text: str) -> int:
    return sum(1 for ch in text if 0xFB00 <= ord(ch) <= 0xFB06)


def normalize(text: str) -> str:
    """NFKC folds printer's ligatures (ﬁ ﬂ ﬃ ﬄ), full-width forms and
    compatibility characters into their plain equivalents. This is the single
    most important line in this file."""
    return unicodedata.normalize("NFKC", text)


def cut_tail(text: str) -> tuple[str, str | None]:
    """Remove back matter. Returns (body, heading that was cut at)."""
    best, label = None, None
    for pat in TAIL_PATTERNS:
        for m in re.finditer(pat, text, re.MULTILINE):
            # Take the EARLIEST acknowledgements/references heading that still
            # sits in the last third of the document — guards against a paper
            # that mentions "References" in a figure caption early on.
            if m.start() > len(text) * 0.5 and (best is None or m.start() < best):
                best, label = m.start(), m.group().strip()
    if best is None:
        return text, None
    return text[:best], label


# --------------------------------------------------------------------------- #
# section detection
# --------------------------------------------------------------------------- #

def find_headings(text: str) -> dict[str, list[int]]:
    """All heading offsets per section id, in document order."""
    hits: dict[str, list[int]] = {}
    for sid, pats in HEADING_PATTERNS.items():
        found = []
        for pat in pats:
            for m in re.finditer(pat, text, re.MULTILINE):
                found.append(m.start())
        hits[sid] = sorted(set(found))
    return hits


def detect_sections(text: str) -> tuple[dict[str, int], list[str]]:
    """Pick one start offset per section id. Returns (starts, notes)."""
    hits = find_headings(text)
    notes: list[str] = []
    starts: dict[str, int] = {}
    cursor = 0
    for sid in SECTION_ORDER:
        if sid == "A":
            continue  # derived after the fact: everything before the Introduction
        candidates = [h for h in hits.get(sid, []) if h >= cursor]
        if not candidates:
            if sid in ("D", "C"):
                notes.append(f"{sid} ({SECTION_NAMES[sid]}): not present")
            else:
                notes.append(f"{sid} ({SECTION_NAMES[sid]}): NOT FOUND")
            continue
        starts[sid] = candidates[0]
        cursor = candidates[0] + 1
        if len(candidates) > 1:
            notes.append(
                f"{sid}: {len(candidates)} heading matches, used offset {candidates[0]}"
            )
    # A fused "Results and discussion" means R is present and D is not — that is
    # a real structural fact about the paper, so record it rather than repair it.
    if "R" in starts and "D" not in starts:
        notes.append("R and D appear fused (no standalone Discussion heading)")
    return starts, notes


def parse_marks(spec: str, text: str) -> tuple[dict[str, int], list[str]]:
    """--marks 'M=Materials and methods,R=Results and discussion' -> offsets."""
    starts, notes = {}, []
    for pair in spec.split(","):
        if "=" not in pair:
            sys.exit(f"prep.py: bad --marks entry {pair!r}; expected ID=heading text")
        sid, needle = (p.strip() for p in pair.split("=", 1))
        if sid not in SECTION_ORDER:
            sys.exit(f"prep.py: unknown section id {sid!r}; use one of {SECTION_ORDER}")
        idx = text.find(needle)
        if idx < 0:
            sys.exit(f"prep.py: --marks text not found in body: {needle!r}")
        starts[sid] = idx
        notes.append(f"{sid}: manual mark at offset {idx} ({needle!r})")
    return starts, notes


def slice_sections(text: str, starts: dict[str, int]) -> dict[str, str]:
    ordered = [(sid, off) for sid, off in sorted(starts.items(), key=lambda kv: kv[1])]
    out = {}
    for i, (sid, off) in enumerate(ordered):
        end = ordered[i + 1][1] if i + 1 < len(ordered) else len(text)
        out[sid] = text[off:end].strip()
    return out


# --------------------------------------------------------------------------- #
# measurement (delegated to quant_check so numbers never diverge)
# --------------------------------------------------------------------------- #

def run_profile(files: list[Path]) -> list[dict]:
    script = Path(__file__).with_name("quant_check.py")
    if not script.exists():
        return []
    try:
        res = subprocess.run(
            [sys.executable, str(script), "profile", *[str(f) for f in files]],
            capture_output=True, text=True, encoding="utf-8", timeout=300,
        )
    except Exception as exc:                                   # pragma: no cover
        print(f"  ! quant_check profile failed: {exc}", file=sys.stderr)
        return []
    if res.returncode != 0:
        print(f"  ! quant_check profile exited {res.returncode}", file=sys.stderr)
        return []
    lines = [l for l in res.stdout.splitlines() if l.strip()]
    if len(lines) < 2:
        return []
    hdr = lines[0].split("\t")
    rows = []
    for l in lines[1:]:
        cells = l.split("\t")
        if len(cells) == len(hdr):
            rows.append(dict(zip(hdr, cells)))
    return rows


# --------------------------------------------------------------------------- #

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Stage 0: normalize a paper and split it into fixed section files."
    )
    ap.add_argument("source", help="paper PDF (or a plain .txt)")
    ap.add_argument("--slug", required=True,
                    help="ASCII lowercase-hyphen paper id, e.g. kim-2015-nitrate-iso")
    ap.add_argument("--out", required=True,
                    help="corpus root; the paper lands in <out>/papers/<slug>/")
    ap.add_argument("--marks", default=None,
                    help="manual section starts, e.g. 'M=Materials and methods,R=Results'")
    ap.add_argument("--dry-run", action="store_true",
                    help="detect and report; write nothing")
    ap.add_argument("--force", action="store_true",
                    help="overwrite an existing paper folder")
    args = ap.parse_args()

    src = Path(args.source)
    if not src.exists():
        sys.exit(f"prep.py: source not found: {src}")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", args.slug):
        sys.exit(f"prep.py: slug must be ASCII lowercase-hyphen, got {args.slug!r}")

    dest = Path(args.out) / "papers" / args.slug
    if dest.exists() and not args.force and not args.dry_run:
        sys.exit(f"prep.py: {dest} already exists; pass --force to overwrite")

    print(f"# prep.py v{__version__}")
    print(f"source : {src}")

    raw = read_source(src)
    lig = count_ligatures(raw)
    body = normalize(raw)
    print(f"read   : {len(raw):,} chars · {lig} ligature chars folded by NFKC")
    if lig:
        print("         ^ counting against the raw PDF would have returned 0 for every")
        print("           word containing them. This is why body.txt exists.")

    body, tail_at = cut_tail(body)
    print(f"body   : {len(body):,} chars"
          + (f" (back matter cut at {tail_at!r})" if tail_at else " (no back matter heading found)"))

    if args.marks:
        starts, notes = parse_marks(args.marks, body)
    else:
        starts, notes = detect_sections(body)

    print("sections detected:")
    for sid in SECTION_ORDER:
        if sid in starts:
            print(f"  {sid}  {SECTION_NAMES[sid]:<13} offset {starts[sid]:,}")
    for n in notes:
        print(f"  · {n}")

    missing = [s for s in ("I", "M", "R") if s not in starts]
    if missing:
        print()
        print(f"STOP: required section(s) not found: {', '.join(missing)}")
        # Numbered headings are the reliable signal in a journal PDF. An
        # unfiltered dump is mostly table cells and figure labels, which buries it.
        lines = [l.strip() for l in body.split("\n")]
        numbered = [l for l in lines
                    if re.match(r"^\d+\.\s+[A-Z]", l) and len(l) < 80]
        if numbered:
            print("      Numbered headings found in the body:")
            for l in dict.fromkeys(numbered):
                print(f"        {l}")
        else:
            print("      No numbered headings. Short Title-Case lines (first 30):")
            loose = [l for l in lines
                     if 4 < len(l) < 45
                     and re.match(r"^[A-Z][a-z]", l)
                     and not re.search(r"[0-9=(),;:]", l)]
            for l in list(dict.fromkeys(loose))[:30]:
                print(f"        {l}")
        print()
        print("      Re-run with --marks, e.g.")
        print("        --marks \"I=Introduction,M=Materials and methods,R=Results and discussion\"")
        sys.exit(2)

    # A is derived: everything before the Introduction heading.
    if starts.get("I", 0) > 0:
        starts["A"] = 0

    chunks = slice_sections(body, starts)

    if args.dry_run:
        print()
        print("dry run — nothing written. Section sizes would be:")
        for sid in SECTION_ORDER:
            if sid in chunks:
                print(f"  {sid}.txt  {len(chunks[sid]):,} chars")
        return

    (dest / "sections").mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest / f"source{src.suffix.lower()}")
    (dest / "body.txt").write_text(body, encoding="utf-8")
    written = []
    for sid in SECTION_ORDER:
        if sid in chunks:
            p = dest / "sections" / f"{sid}.txt"
            p.write_text(chunks[sid], encoding="utf-8")
            written.append(p)

    section_files = written
    profile_rows = run_profile([dest / "body.txt"] + section_files)

    # ------------------------------------------------------------------ #
    # manifest.json — the corpus entry point.
    #
    # Downstream (meta-styling) reads THIS, not the 100 KB markdown files, to
    # answer "which band applies to a Methods paragraph?" and "what must this
    # draft never do?".  prep.py fills every deterministic field and leaves the
    # judgment fields as null; the lenses fill the nulls.  A manifest that still
    # contains null after extraction is an incomplete extraction, and that is
    # exactly the check we want to be cheap.
    # ------------------------------------------------------------------ #
    by_file = {Path(r["file"]).name: r for r in profile_rows}

    def measured(sid: str):
        r = by_file.get(f"{sid}.txt")
        if not r:
            return None
        return {
            "tokens": int(r["tokens"]),
            "sentences": int(r["sentences"]),
            "avg_sent_len": float(r["avg_sent_len"]),
            "hedges_per_1k": float(r["hedges_per_1k"]),
            "passive_per_1k": float(r["passive_per_1k"]),
        }

    manifest = {
        "schema": "metasci-corpus/manifest",
        "schema_version": "1.0.0",
        "slug": args.slug,

        "paper": {                      # filled by the lenses from the front matter
            "title": None, "authors": None, "journal": None,
            "year": None, "doi": None,
        },

        "prep": {
            "prep_version": __version__,
            "source_file": src.name,
            "source_chars_raw": len(raw),
            "ligatures_folded": lig,
            "back_matter_cut_at": tail_at,
            "body_chars": len(body),
            "front_matter_chars": len(chunks.get("A", "")),
            "section_scheme": "".join(s for s in BODY_SECTIONS if s in chunks),
            "detection_notes": notes,
        },

        "files": {
            "body": "body.txt",
            "sections": {s: f"sections/{s}.txt"
                         for s in SECTION_ORDER if s in chunks},
            "logic": "logic.md",
            "style_vocab": "style-vocab.md",
            "wordlist": "wordlist.tsv",
            "card": "card.md",
            "anchors": "anchors.txt",
        },

        "measured": {
            "source": "sections/*.txt",
            "warning": ("Never use body.txt for a band: it includes the front "
                        "matter (A), which is a different genre. Compare a draft "
                        "section against its own section row."),
            "sections": {s: measured(s)
                         for s in SECTION_ORDER if s in chunks},
        },

        # ---- filled by the lenses -------------------------------------- #
        "frames": {
            "total": None, "recurrent": None, "singleton": None,
            "uncategorized_rate": None,
            "rule": ("Imitate the frame TYPE and its position; never copy the "
                     "anchor WORDING."),
        },
        "vocabulary": {
            "reporting_verbs": None,     # {lemma: {total, by_section, reserved_for}}
            "modality_workhorse": None,  # e.g. "can be (21), not may (9)"
            "connectives": None,
        },
        "red_flags": None,               # list of absent patterns to strip from a draft
        "distinctive_moves": None,       # 1-3 notable moves
        "provenance": {
            "extracted_at": None,
            "quant_check_version": None,
            "verbatim_errors_caught": None,
            "notes": None,
        },
    }
    (dest / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    print()
    print(f"written to {dest}")
    print(f"  body.txt              {len(body):,} chars")
    for sid in SECTION_ORDER:
        if sid in chunks:
            print(f"  sections/{sid}.txt        {len(chunks[sid]):,} chars")
    pending = [k for k in ("paper", "frames", "vocabulary", "red_flags",
                           "distinctive_moves", "provenance")
               if manifest[k] is None
               or (isinstance(manifest[k], dict)
                   and all(v is None for v in manifest[k].values()))]
    print(f"  manifest.json         scheme={manifest['prep']['section_scheme']}"
          + (f", measured {len(profile_rows)} files" if profile_rows else ", profile NOT run"))
    if not profile_rows:
        print("  ! quant_check profile produced no rows — the manifest's measured"
              " bands must be filled in by hand.")
    print()
    print("next: run the lenses, then fill these manifest fields (currently null):")
    print(f"  {', '.join(pending)}")
    print("a manifest that still contains null is an incomplete extraction.")


if __name__ == "__main__":
    main()
