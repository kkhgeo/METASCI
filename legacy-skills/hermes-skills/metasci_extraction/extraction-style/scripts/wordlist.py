#!/usr/bin/env python3
"""wordlist.py — Lens W step 1: the complete, deterministic count layer.

Writes <paper>/wordlist.tsv: every content type in the paper with its frequency
in each section, plus a class column marking whether the type is transferable
style vocabulary or topic-bound.

    py -3.10 wordlist.py <corpus>/papers/<slug>

WHY THIS IS A SCRIPT AND NOT AN INSTRUCTION
-------------------------------------------
"Tokenize the section files and drop the function words" is not reproducible
prose: the stop list, the minimum length and the digit rule all have to be
decided, and deciding them freshly each run means the type counts never match
between runs. Both lists below are frozen here and versioned, so `1,111 types`
means the same thing next month as it does today.

THE CLASS COLUMN
----------------
`academic`  general scholarly nouns and their kin — travel to another manuscript
`other`     topic terms, proper nouns, technical vocabulary — travel nowhere

Lens W classifies and contextualizes only the `academic` slice; `other` is
counted here and left alone. On the reference paper the split was 61 / 474
(11% / 89%), which is the measured argument for that boundary. Because the two
lists are frozen, that ratio is reproducible rather than an impression.

Domain terminology belongs to extraction-knowledge, not to a style corpus.
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

__version__ = "1.0.0"
STOPLIST_VERSION = "1.0.0"
ACADEMIC_VERSION = "1.0.0"

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

SECTION_ORDER = ["A", "I", "M", "R", "D", "C"]

# Closed-class and near-closed-class items. Excluded from wordlist.tsv because
# they are Lens A/W's business as *frames and connectives*, not as lexicon
# entries. FROZEN — changing this changes every type count in the corpus.
STOPLIST = set("""
a an the of in at for to from with by on onto into over under above below between among
against through during after before since until within without upon across per toward towards
and or but nor yet so if while as than then because although though whether
is was were are be been being am have has had do does did having
this that these those it its they them their we our us you your he she his her him
which who whom whose what when where how why
not no nor none neither either both each every some any all one two three four five
more most other others another same such very much many few several own
can could may might must shall should will would
here there now thus hence therefore however moreover furthermore nevertheless nonetheless
additionally specifically particularly generally usually often always never still already just
even also only ever almost quite rather too very well
i ii iii iv et al fig figs table tables eq eqs section sections appendix
""".split())

# General academic vocabulary: words that carry scholarly register rather than
# subject matter. Deliberately conservative — a word only belongs here if it
# would be at home in a paper from a different field. FROZEN.
GENERAL_ACADEMIC = set("""
study studies research approach approaches method methods methodology methodologies
procedure procedures process processes technique techniques framework frameworks
model models analysis analyses result results finding findings outcome outcomes
evidence data dataset datasets value values parameter parameters variable variables
measure measures measurement measurements observation observations factor factors
effect effects influence impact impacts range ranges level levels case cases
context contexts condition conditions basis criterion criteria assumption assumptions
uncertainty uncertainties limitation limitations implication implications
contribution contributions difference differences similarity relationship relationships
pattern patterns trend trends distribution distributions estimate estimates
estimation calculation calculations comparison comparisons interpretation interpretations
information knowledge literature reference references source sources
summary conclusion conclusions objective objectives purpose aim aims goal scope
significance quality type types number total mean median average
statistic statistics error errors interval intervals fraction fractions ratio ratios
proportion proportions percentage percentages term terms concept concepts
principle principles feature features characteristic characteristics property properties
issue issues problem problems solution solutions alternative alternatives
option options step steps stage stages phase phases aspect aspects
question questions hypothesis hypotheses theory theories
evaluation assessment application applications development
validation verification performance accuracy precision reliability
""".split())


def load_quant_check_tokenizer():
    """Use quant_check's tokenizer so wordlist counts and count/keyness counts
    can never disagree about what a token is."""
    sys.path.insert(0, str(Path(__file__).parent))
    try:
        import quant_check  # type: ignore
        return quant_check.tokenize
    except Exception as exc:
        sys.exit(f"wordlist.py: cannot import quant_check.py ({exc})")


def classify(word: str) -> str:
    return "academic" if word in GENERAL_ACADEMIC else "other"


def main() -> None:
    ap = argparse.ArgumentParser(description="Build wordlist.tsv for one paper folder.")
    ap.add_argument("paper", help="<corpus>/papers/<slug>")
    ap.add_argument("--min-len", type=int, default=3,
                    help="drop tokens of this length or shorter (default 3)")
    ap.add_argument("--out", default=None, help="override output path")
    args = ap.parse_args()

    paper = Path(args.paper)
    sections_dir = paper / "sections"
    if not sections_dir.is_dir():
        sys.exit(f"wordlist.py: no sections/ under {paper} — run prep.py first")

    tokenize = load_quant_check_tokenizer()

    present = [s for s in SECTION_ORDER if (sections_dir / f"{s}.txt").exists()]
    if not present:
        sys.exit(f"wordlist.py: sections/ is empty in {paper}")

    counts: dict[str, collections.Counter] = {}
    raw_tokens: dict[str, int] = {}
    for sid in present:
        text = (sections_dir / f"{sid}.txt").read_text(encoding="utf-8", errors="replace")
        toks = tokenize(text)
        raw_tokens[sid] = len(toks)
        counts[sid] = collections.Counter(
            w for w in toks
            if w not in STOPLIST and len(w) > args.min_len and not w.isdigit()
        )

    all_types = sorted(set().union(*[set(c) for c in counts.values()]))
    total_of = {w: sum(counts[s][w] for s in present) for w in all_types}
    ordered = sorted(all_types, key=lambda w: (-total_of[w], w))

    out = Path(args.out) if args.out else paper / "wordlist.tsv"
    with out.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write("type\t" + "\t".join(present) + "\ttotal\tclass\n")
        for w in ordered:
            row = [w] + [str(counts[s][w]) for s in present]
            row += [str(total_of[w]), classify(w)]
            fh.write("\t".join(row) + "\n")

    # summary — the numbers Lens W quotes
    ge2 = [w for w in all_types if total_of[w] >= 2]
    acad = [w for w in ge2 if classify(w) == "academic"]
    hapax = [w for w in all_types if total_of[w] == 1]

    print(f"# wordlist.py v{__version__}"
          f"  stoplist v{STOPLIST_VERSION}  academic-list v{ACADEMIC_VERSION}")
    print(f"wrote {out}")
    print(f"  sections            {' '.join(present)}")
    print(f"  content types       {len(all_types):,}")
    print(f"  hapax (Freq 1)      {len(hapax):,}  ({100*len(hapax)/len(all_types):.0f}%)")
    print(f"  types at Freq >= 2  {len(ge2):,}")
    print(f"    academic          {len(acad):,}  ({100*len(acad)/len(ge2):.0f}%)  <- Lens W classifies these")
    print(f"    other             {len(ge2)-len(acad):,}  ({100*(len(ge2)-len(acad))/len(ge2):.0f}%)  <- counted only; topic-bound")
    print()
    print("  type/token by section (texture; higher = says each thing once):")
    for sid in present:
        tt = len(counts[sid]) / raw_tokens[sid] if raw_tokens[sid] else 0
        print(f"    {sid}  types {len(counts[sid]):5,}  tokens {raw_tokens[sid]:6,}  ratio {tt:.3f}")

    stats = {
        "wordlist_version": __version__,
        "stoplist_version": STOPLIST_VERSION,
        "academic_list_version": ACADEMIC_VERSION,
        "min_len": args.min_len,
        "sections": present,
        "content_types": len(all_types),
        "hapax": len(hapax),
        "types_freq_ge2": len(ge2),
        "academic_freq_ge2": len(acad),
        "type_token_by_section": {
            s: round(len(counts[s]) / raw_tokens[s], 4) if raw_tokens[s] else None
            for s in present
        },
    }
    (paper / "wordlist.stats.json").write_text(
        json.dumps(stats, indent=2), encoding="utf-8")
    print(f"\n  wordlist.stats.json written (quote these numbers in style-vocab.md)")


if __name__ == "__main__":
    main()
