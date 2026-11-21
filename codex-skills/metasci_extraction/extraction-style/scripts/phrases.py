#!/usr/bin/env python3
"""phrases.py — Lens W step 1b: the exhaustive multi-word layer.

Writes <paper>/phrases.tsv: every contiguous 2-, 3- and 4-word sequence that
occurs at least twice in the paper's section files, with its frequency in each
section, its range across sections, a lexical-bundle flag, a topic flag, a
nesting pointer, and two empty columns for the functional classification.

    py -3.10 phrases.py <corpus>/papers/<slug>
    py -3.10 phrases.py <corpus>/papers/<slug> --functions functions.tsv

The first call counts. The second merges the LLM's classification back in; it is
the only place judgment enters the file, and the merge validates it.

WHY THIS IS A SCRIPT
--------------------
Lexical bundles are defined by frequency and dispersion, both of which are
counts. Asking a reader to list "recurrent phrases" yields the memorable ones and
misses the frequent ones; the frequent ones are usually function-word frames
(*in the case of*, *as well as the*) that nobody notices reading. Counting finds
them all, the same way every run.

SELECTION CRITERIA
------------------
Biber et al. (1999, Longman Grammar of Spoken and Written English, ch. 13) define
lexical bundles as recurrent sequences of three or more words, retained above a
frequency cut-off (10 per million words) and a dispersion cut-off (five or more
texts). Hyland (2008, English for Specific Purposes 27: 4-21) uses 4-word bundles
at 20 per million and occurrence in at least 10% of the texts.

Those per-million floors are corpus-scale. One paper is ~5-10k tokens, where
20 per million is 0.2 occurrences, so they cannot be applied as written. This
script makes the single-paper analogue explicit:

  frequency floor   --min-freq   raw occurrences in the paper   (default 2)
  dispersion floor  --min-range  sections that contain it       (default 2)
  length            n = 3 or 4 for `bundle`; n = 2 is kept as a
                    collocation layer and never flagged as a bundle

Sections stand in for texts. `per_million` is written anyway, so a corpus-level
aggregate (references/aggregate.md) can apply the published thresholds across
papers, where they mean what Biber and Hyland meant.

Sequences never cross a sentence, a clause punctuation mark, a number, or a
symbol: "of 5 mg" is not the bundle "of mg".

THE TOPIC FLAG
--------------
`topic = yes` when the sequence contains a content word that is in neither the
frozen stop list, the frozen general-academic list (both from wordlist.py), nor
the frozen phrasal list below. *the nitrate concentrations* is topic; *the results
of the* and *it was found that* are not. This is a deterministic first pass:
the reader may still classify a topic-flagged row, and the merge reports it.

FUNCTION COLUMNS
----------------
Hyland's (2008) taxonomy, which the LLM fills for bundle rows:

  research     location, procedure, quantification, description, topic
  text         transition, resultative, structuring, framing
  participant  stance, engagement

`function` holds the top category, `subfunction` the sub-category. The merge file
is TSV: phrase <TAB> function[:subfunction]. Unknown labels, unknown phrases and
duplicates make the merge fail rather than write a half-classified file.
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

__version__ = "1.0.0"
PHRASAL_VERSION = "1.0.0"

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.insert(0, str(Path(__file__).parent))
try:
    import quant_check  # type: ignore
    from wordlist import GENERAL_ACADEMIC, SECTION_ORDER, STOPLIST  # type: ignore
except Exception as exc:  # pragma: no cover
    sys.exit(f"phrases.py: cannot import quant_check.py / wordlist.py ({exc})")

# Non-topic content words that build bundles: reporting, procedure, comparison,
# quantity and evaluation words that would be at home in any empirical paper.
# Extends GENERAL_ACADEMIC for the topic test only. FROZEN.
GENERAL_PHRASAL = set("""
based base using used use uses usage due respect regard regards order addition
account accordance according terms part parts basis means way ways extent degree
show shows shown showed indicate indicates indicated indicating suggest suggests
suggested suggesting found find finds reported report reports observed observe
obtained obtain considered consider described describe presented present presents
determined determine calculated calculate estimated estimate measured measure
applied apply performed perform conducted conduct compared compare comparing
associated related relative relatively consistent similar different differ
increase increases increased increasing decrease decreases decreased decreasing
higher lower high low large larger small smaller greater less least lowest highest
first second third last final previous previously following follows given total
overall main major minor important significant significantly possible potential
likely unlikely specific respectively present current recent new known well
example instance case cases fact point time times period periods
result resulted resulting results lead leads leading led cause caused causing
provide provides provided providing allow allows allowed required require
expected expect explain explained related relation contrast compared comparison
because therefore whereas whether although
""".split())

LABELS = {
    "research": {"location", "procedure", "quantification", "description", "topic"},
    "text": {"transition", "resultative", "structuring", "framing"},
    "participant": {"stance", "engagement"},
}

# Word tokens exactly as quant_check counts them; anything else that is not
# whitespace (digits, punctuation, symbols) is a boundary.
WORD = quant_check.TOKEN_RE.pattern
SCAN_RE = re.compile(rf"{WORD}|[^\s]")
WORD_RE = re.compile(rf"^(?:{WORD})$")


def segments(text: str):
    """Yield runs of consecutive word tokens, lowercased, broken at any non-word
    token. Line breaks inside a sentence do not break a run."""
    run: list[str] = []
    for m in SCAN_RE.finditer(text):
        tok = m.group(0)
        if WORD_RE.match(tok):
            run.append(tok.lower())
        else:
            if run:
                yield run
            run = []
    if run:
        yield run


def is_topic(words: tuple[str, ...]) -> bool:
    for w in words:
        if w in STOPLIST or w in GENERAL_ACADEMIC or w in GENERAL_PHRASAL:
            continue
        if len(w) <= 1:
            continue
        return True
    return False


def parse_label(raw: str) -> tuple[str, str]:
    top, _, sub = raw.strip().lower().partition(":")
    if top not in LABELS:
        raise ValueError(f"unknown function '{top}' (use {', '.join(LABELS)})")
    if sub and sub not in LABELS[top]:
        raise ValueError(f"unknown subfunction '{sub}' for {top} "
                         f"(use {', '.join(sorted(LABELS[top]))})")
    return top, sub


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    header = lines[0].split("\t")
    return header, [dict(zip(header, ln.split("\t"))) for ln in lines[1:] if ln]


def write_rows(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write("\t".join(header) + "\n")
        for r in rows:
            fh.write("\t".join(r.get(h, "") for h in header) + "\n")


def merge(paper: Path, out: Path, functions: Path) -> None:
    if not out.exists():
        sys.exit(f"phrases.py: {out} not found — run without --functions first")
    header, rows = read_rows(out)
    index = {r["phrase"]: r for r in rows}
    seen: set[str] = set()
    errors: list[str] = []
    topic_classified: list[str] = []
    non_bundle: list[str] = []
    for n, ln in enumerate(functions.read_text(encoding="utf-8").splitlines(), 1):
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        parts = ln.split("\t")
        if len(parts) < 2:
            errors.append(f"line {n}: expected 'phrase<TAB>function[:sub]'")
            continue
        phrase = " ".join(parts[0].lower().split())
        if phrase in seen:
            errors.append(f"line {n}: duplicate '{phrase}'")
            continue
        seen.add(phrase)
        row = index.get(phrase)
        if row is None:
            errors.append(f"line {n}: '{phrase}' is not in phrases.tsv")
            continue
        try:
            top, sub = parse_label(parts[1])
        except ValueError as exc:
            errors.append(f"line {n}: {exc}")
            continue
        row["function"], row["subfunction"] = top, sub
        if row["topic"] == "yes":
            topic_classified.append(phrase)
        if row["bundle"] != "yes":
            non_bundle.append(phrase)
    if errors:
        print("phrases.py: merge refused, nothing written", file=sys.stderr)
        for e in errors:
            print("  " + e, file=sys.stderr)
        sys.exit(1)
    write_rows(out, header, rows)

    bundles = [r for r in rows if r["bundle"] == "yes" and r["topic"] == "no"]
    pending = [r["phrase"] for r in bundles if not r["function"]]
    dist = collections.Counter(r["function"] for r in rows if r["function"])
    print(f"merged {len(seen)} labels into {out}")
    print("  function distribution  "
          + "  ".join(f"{k} {dist.get(k, 0)}" for k in LABELS))
    if topic_classified:
        print(f"  note: {len(topic_classified)} topic-flagged rows were classified "
              f"(allowed; check them): {', '.join(topic_classified[:8])}")
    if non_bundle:
        print(f"  note: {len(non_bundle)} non-bundle rows were classified: "
              f"{', '.join(non_bundle[:8])}")
    if pending:
        print(f"  {len(pending)} non-topic bundles still unclassified: "
              f"{', '.join(pending[:10])}" + (" ..." if len(pending) > 10 else ""))
    else:
        print("  every non-topic bundle is classified")

    stats_path = paper / "phrases.stats.json"
    if stats_path.exists():
        stats = json.loads(stats_path.read_text(encoding="utf-8"))
        stats["functions"] = {k: dist.get(k, 0) for k in LABELS}
        stats["bundles_unclassified"] = len(pending)
        stats_path.write_text(json.dumps(stats, indent=2), encoding="utf-8")


def build(paper: Path, out: Path, ns: list[int], min_freq: int, min_range: int) -> None:
    sections_dir = paper / "sections"
    present = [s for s in SECTION_ORDER if (sections_dir / f"{s}.txt").exists()]
    if not present:
        sys.exit(f"phrases.py: no sections/*.txt under {paper} — run prep.py first")

    counts: dict[tuple[str, ...], collections.Counter] = collections.defaultdict(
        collections.Counter)
    tokens_by_section: dict[str, int] = {}
    for sid in present:
        text = (sections_dir / f"{sid}.txt").read_text(encoding="utf-8", errors="replace")
        if quant_check.HANGUL_RE.search(text) and \
                len(quant_check.HANGUL_RE.findall(text)) > len(text) * 0.2:
            print(f"  warning: {sid}.txt is predominantly Hangul; eojeol n-grams are "
                  "not lexical bundles — see references/lens-korean.md", file=sys.stderr)
        tokens_by_section[sid] = len(quant_check.tokenize(text))
        for run in segments(text):
            for n in ns:
                for i in range(len(run) - n + 1):
                    counts[tuple(run[i:i + n])][sid] += 1

    corpus_tokens = sum(tokens_by_section.values())
    kept = {g: c for g, c in counts.items() if sum(c.values()) >= min_freq}
    total = {g: sum(c.values()) for g, c in kept.items()}

    # nesting: a shorter sequence whose every occurrence is inside one longer
    # kept sequence (equal total) is a fragment of it, not a bundle of its own.
    nested_in: dict[tuple[str, ...], tuple[str, ...]] = {}
    for g in sorted(kept, key=len, reverse=True):
        if len(g) < 2:
            continue
        for sub in (g[:-1], g[1:]):
            if sub in kept and total[sub] == total[g] and sub not in nested_in:
                nested_in[sub] = nested_in.get(g, g)

    rows = []
    for g, c in kept.items():
        rng = sum(1 for s in present if c[s])
        topic = is_topic(g)
        bundle = (len(g) >= 3 and rng >= min_range and g not in nested_in)
        rows.append({
            "phrase": " ".join(g), "n": str(len(g)),
            **{s: str(c[s]) for s in present},
            "total": str(total[g]),
            "per_million": f"{total[g] / corpus_tokens * 1e6:.0f}" if corpus_tokens else "",
            "range": str(rng),
            "bundle": "yes" if bundle else "no",
            "topic": "yes" if topic else "no",
            "nested_in": " ".join(nested_in[g]) if g in nested_in else "",
            "function": "", "subfunction": "",
        })
    rows.sort(key=lambda r: (r["bundle"] != "yes", -int(r["n"]),
                             -int(r["total"]), r["phrase"]))

    header = (["phrase", "n"] + present
              + ["total", "per_million", "range", "bundle", "topic", "nested_in",
                 "function", "subfunction"])
    write_rows(out, header, rows)

    by_n = collections.Counter(int(r["n"]) for r in rows)
    bundles = [r for r in rows if r["bundle"] == "yes"]
    style_bundles = [r for r in bundles if r["topic"] == "no"]
    topic_bundles = [r for r in bundles if r["topic"] == "yes"]

    print(f"# phrases.py v{__version__}  phrasal-list v{PHRASAL_VERSION}")
    print(f"wrote {out}")
    print(f"  sections               {' '.join(present)}  ({corpus_tokens:,} tokens)")
    print(f"  criteria               freq >= {min_freq}, range >= {min_range} sections, "
          f"n = 3-4 for bundles")
    for n in ns:
        print(f"  {n}-grams at freq >= {min_freq}  {by_n.get(n, 0):,}")
    print(f"  lexical bundles        {len(bundles):,}")
    print(f"    non-topic            {len(style_bundles):,}  <- classify these "
          f"(research / text / participant)")
    print(f"    topic-bound          {len(topic_bundles):,}  <- Lens T term candidates")
    print(f"  nested fragments       {len(nested_in):,}  (excluded from bundles)")

    stats = {
        "phrases_version": __version__,
        "phrasal_list_version": PHRASAL_VERSION,
        "criteria": {
            "n": ns, "min_freq": min_freq, "min_range": min_range,
            "bundle_n": [3, 4], "range_unit": "sections",
            "basis": "Biber et al. 1999; Hyland 2008 (single-paper analogue)",
        },
        "sections": present,
        "tokens": corpus_tokens,
        "ngrams_by_n": {str(n): by_n.get(n, 0) for n in ns},
        "bundles": len(bundles),
        "bundles_non_topic": len(style_bundles),
        "bundles_topic": len(topic_bundles),
        "nested_fragments": len(nested_in),
        "functions": None,
        "bundles_unclassified": len(style_bundles),
    }
    (paper / "phrases.stats.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")
    print("\n  phrases.stats.json written (quote these numbers in style-vocab.md)")


def main() -> None:
    ap = argparse.ArgumentParser(description="Build or classify phrases.tsv for one paper.")
    ap.add_argument("paper", help="<corpus>/papers/<slug>")
    ap.add_argument("--n", default="2,3,4", help="sequence lengths (default 2,3,4)")
    ap.add_argument("--min-freq", type=int, default=2,
                    help="frequency floor, raw occurrences (default 2)")
    ap.add_argument("--min-range", type=int, default=2,
                    help="dispersion floor, sections containing it (default 2)")
    ap.add_argument("--functions", default=None,
                    help="merge an LLM classification file (phrase<TAB>function[:sub])")
    ap.add_argument("--out", default=None, help="override output path")
    args = ap.parse_args()

    paper = Path(args.paper)
    out = Path(args.out) if args.out else paper / "phrases.tsv"
    if args.functions:
        merge(paper, out, Path(args.functions))
        return
    ns = sorted({int(x) for x in args.n.split(",") if x.strip()})
    if not ns or min(ns) < 2:
        sys.exit("phrases.py: --n takes lengths of 2 or more")
    build(paper, out, ns, args.min_freq, args.min_range)


if __name__ == "__main__":
    main()
