#!/usr/bin/env python3
"""wordlist.py — Lens W step 1: the complete, deterministic count layer.

Writes <paper>/wordlist.tsv: every content type in the paper with its frequency
in each section, its range across sections, an inflection family, a part-of-speech
column when a tagger is installed, and a class column marking whether the type is
transferable style vocabulary or topic-bound.

Since v2.0.0 this file is the corpus's complete single-word inventory. It replaced
the retired extraction-vocab skill, whose LLM-written word lists duplicated these
counts and broke on ligatures. Nothing is curated here: every type that survives
the frozen stop list is written, Freq 1 included.

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

The `other` slice is not discarded: Lens T (glossary.md) reads it, together with
the topic-flagged rows of phrases.tsv, to build the technical-term glossary.

COLUMNS (v2.0.0)
----------------
type     lowercased surface form, as quant_check.tokenize produces it
A..C     frequency per section present in the paper
total    sum over sections
range    number of sections the type occurs in
family   the inflection family head: the shortest attested form that this type
         reduces to by a regular English suffix (-s, -es, -ies, -ed, -ing). A
         reduction is accepted only when the base form itself occurs in the
         paper, so `samples` -> `sample` but `basis` is left alone. With spaCy
         installed, spaCy's lemma is used instead.
pos      dominant Universal POS tag (NOUN, VERB, ADJ, ADV, PROPN ...), with a
         second tag after "/" when it covers >= 25% of the occurrences. Empty when
         no tagger is installed; stats record which tagger ran.
class    academic | other
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

__version__ = "2.0.0"
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


def inflection_family(types: set[str]) -> dict[str, str]:
    """Map each type to the shortest attested base reachable by a regular English
    inflection. Conservative by construction: the base must itself be a type."""
    def candidates(w: str) -> list[str]:
        out = []
        if w.endswith("ies") and len(w) > 4:
            out.append(w[:-3] + "y")
        if w.endswith("es") and len(w) > 3:
            out.append(w[:-2])
        if w.endswith("s") and not w.endswith("ss") and len(w) > 3:
            out.append(w[:-1])
        if w.endswith("ied") and len(w) > 4:
            out.append(w[:-3] + "y")
        if w.endswith("ed") and len(w) > 4:
            out += [w[:-2], w[:-1]]
            if len(w) > 5 and w[-3] == w[-4]:
                out.append(w[:-3])          # controlled -> control
        if w.endswith("ing") and len(w) > 5:
            out += [w[:-3], w[:-3] + "e"]
            if w[-4] == w[-5]:
                out.append(w[:-4])          # mapping -> map
        return out

    fam: dict[str, str] = {}
    for w in types:
        base = next((c for c in candidates(w) if c in types and c != w), w)
        fam[w] = base
    # one more hop, so `studies` and `studied` both land on `study`
    return {w: fam.get(b, b) for w, b in fam.items()}


def spacy_tags(texts: list[str]):
    """Return ({lower_token: Counter(pos)}, {lower_token: lemma}, tagger_name) or
    None when spaCy or an English model is not installed."""
    try:
        import spacy  # type: ignore
    except Exception:
        return None
    nlp = None
    for name in ("en_core_web_sm", "en_core_web_md", "en_core_web_lg"):
        try:
            nlp = spacy.load(name, disable=["ner", "parser"])
            break
        except Exception:
            continue
    if nlp is None:
        return None
    nlp.max_length = max(nlp.max_length, max((len(t) for t in texts), default=0) + 1)
    pos: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    lemma_votes: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for doc in nlp.pipe(texts):
        for tok in doc:
            key = tok.text.lower()
            pos[key][tok.pos_] += 1
            lemma_votes[key][tok.lemma_.lower()] += 1
    lemmas = {k: c.most_common(1)[0][0] for k, c in lemma_votes.items()}
    return pos, lemmas, f"spacy {spacy.__version__} / {nlp.meta.get('name', '?')}"


def pos_label(c: collections.Counter | None) -> str:
    if not c:
        return ""
    (top, n1), *rest = c.most_common(2)
    total = sum(c.values())
    if rest and rest[0][1] / total >= 0.25:
        return f"{top}/{rest[0][0]}"
    return top


def main() -> None:
    ap = argparse.ArgumentParser(description="Build wordlist.tsv for one paper folder.")
    ap.add_argument("paper", help="<corpus>/papers/<slug>")
    ap.add_argument("--min-len", type=int, default=1,
                    help="drop tokens of this length or shorter (default 1: only "
                         "single letters go; v1 used 3 and lost pH, ion, age, map)")
    ap.add_argument("--pos", choices=["auto", "off"], default="auto",
                    help="auto: tag with spaCy when installed (default); off: skip")
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
    texts: dict[str, str] = {}
    for sid in present:
        text = (sections_dir / f"{sid}.txt").read_text(encoding="utf-8", errors="replace")
        texts[sid] = text
        toks = tokenize(text)
        raw_tokens[sid] = len(toks)
        counts[sid] = collections.Counter(
            w for w in toks
            if w not in STOPLIST and len(w) > args.min_len and not w.isdigit()
        )

    all_types = sorted(set().union(*[set(c) for c in counts.values()]))
    total_of = {w: sum(counts[s][w] for s in present) for w in all_types}
    range_of = {w: sum(1 for s in present if counts[s][w]) for w in all_types}
    ordered = sorted(all_types, key=lambda w: (-total_of[w], w))

    tagged = spacy_tags([texts[s] for s in present]) if args.pos == "auto" else None
    if tagged:
        pos_of, lemma_of, tagger = tagged
        family = {w: lemma_of.get(w, w) for w in all_types}
    else:
        pos_of, tagger = {}, "none"
        family = inflection_family(set(all_types))

    out = Path(args.out) if args.out else paper / "wordlist.tsv"
    with out.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write("type\t" + "\t".join(present)
                 + "\ttotal\trange\tfamily\tpos\tclass\n")
        for w in ordered:
            row = [w] + [str(counts[s][w]) for s in present]
            row += [str(total_of[w]), str(range_of[w]), family[w],
                    pos_label(pos_of.get(w)), classify(w)]
            fh.write("\t".join(row) + "\n")

    # summary — the numbers Lens W quotes
    ge2 = [w for w in all_types if total_of[w] >= 2]
    acad = [w for w in ge2 if classify(w) == "academic"]
    hapax = [w for w in all_types if total_of[w] == 1]

    print(f"# wordlist.py v{__version__}"
          f"  stoplist v{STOPLIST_VERSION}  academic-list v{ACADEMIC_VERSION}")
    print(f"wrote {out}")
    print(f"  sections            {' '.join(present)}")
    print(f"  pos tagger          {tagger}"
          + ("" if tagged else "  (pip install spacy && python -m spacy download "
                               "en_core_web_sm to fill the pos column)"))
    print(f"  families            {len(set(family.values())):,}")
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
        "pos_tagger": tagger,
        "family_method": "spacy-lemma" if tagged else "suffix-attested",
        "sections": present,
        "content_types": len(all_types),
        "families": len(set(family.values())),
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
    print(f"\n  wordlist.stats.json written (quote these numbers in style-vocab.md and glossary.md)")


if __name__ == "__main__":
    main()
