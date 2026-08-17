---
name: metasci-style-extraction
description: |
  META-SCI series. Build a reusable STYLE CORPUS from reference papers: one folder per
  paper containing normalized text, per-section splits, an exhaustive sentence-frame
  catalog, a measured style vocabulary, a lean Style Card, and a machine-readable
  manifest. Runs three lenses over shared, pre-normalized text —
  A (architecture + sentence frames), W (style vocabulary, measured by section),
  C (Style Card: V/L/P indicators + red flags).
  Use whenever the user wants to "extract style", "스타일 추출", "문체 추출",
  "이 논문들 스타일 뽑아줘", capture a journal's writing conventions, or build a style
  reference for later rewriting with meta-styling.
  NOT for domain knowledge or claims ("지식 추출" → extraction-knowledge), NOT for an
  exhaustive proofreading lexicon or argument map (→ extraction-vocab / extraction-logic),
  NOT for applying a style to a draft (→ meta-styling).
---

# META-SCI · Style Extraction (corpus build)

Produce a **style corpus**: one folder per paper, always the same files, always the same
names, so a downstream skill can find things by path instead of by reading.

```
Stage 0  prep.py         PDF → body.txt + sections/ + manifest.json   (deterministic)
Lens A   architecture    structure · paragraph logic · frame catalog  → logic.md, anchors.txt
Lens W   vocabulary      style-bearing lexicon, measured by section   → style-vocab.md, wordlist.tsv
Lens C   card            V/L/P selection + red flags                  → card.md
Stage 4  manifest        fill the null fields                         → manifest.json
```

A and W are independent and may run in parallel. **C runs last** and cites A and W rather
than re-deriving them — this ordering is not cosmetic, see *Why C is last* below.

## What this skill does NOT collect

**Domain terminology and knowledge claims.** Not the technical glossary, not the topic
nouns, not what the paper argues or cites. Those belong to `extraction-knowledge`
(5 epistemological categories, APA references) and `extraction-vocab` (exhaustive lexicon).

This boundary is measured, not a matter of taste. On a representative paper, of the 535
content types occurring twice or more, **474 (89%) are topic-bound** — *nitrate*(158),
*groundwater*(92), *manure*(53) — and travel to no other manuscript. Only 61 (11%) are
general academic words a reviser can actually reuse. Carrying the other 89% into a style
corpus adds bulk, duplicates `extraction-knowledge`, and buries the usable part.

**Lean on the topic axis, complete on the style axis.** Function words, connectives,
reporting verbs, hedges, stance markers, sentence frames and section architecture go in
*in full*. Domain nouns stay out.

| Job | Skill |
|-----|-------|
| Knowledge claims, citations, research questions | `extraction-knowledge` |
| Exhaustive lexicon incl. technical glossary | `extraction-vocab` |
| Exhaustive argument map for proofreading | `extraction-logic` |
| **Style corpus for reuse** | **this skill** |
| Apply a corpus to a draft | `meta-styling` |

`extraction-knowledge` may reuse this skill's `body.txt` — it faces the same ligature
problem and its quality bar is verbatim quotation, so it benefits most.

## Inputs

- **Sources**: reference papers, PDF or text. One paper produces one folder.
- **corpus root** (required): where `papers/` lives. Ask; never invent a location outside
  the project. There is no global default — some users keep one library per project.
- **slug** (required): ASCII lowercase-hyphen, `author-year-topic`
  (`kim-2015-nitrate-iso`).
- **Korean documents (EXPERIMENTAL)**: read `references/lens-korean.md` on top of the
  lens files; it redefines what each lens collects. Never mix languages in one corpus.
- **Scanned PDFs**: if a PDF has almost no text layer, STOP and warn. Style cannot be read
  from an image and fabricating it corrupts the corpus.

## The contract

Every paper folder looks exactly like this. Downstream code path-constructs against it.

```
<corpus>/
├── index.md                     human-readable list of papers
└── papers/<slug>/
    ├── source.pdf
    ├── body.txt                 NFKC-normalized, dehyphenated, back matter cut
    ├── sections/
    │   ├── A.txt                front matter + abstract  (never part of a band)
    │   ├── I.txt M.txt R.txt    Introduction · Methods · Results
    │   ├── D.txt                only when the paper separates Discussion
    │   └── C.txt                only when the paper has Conclusions
    ├── logic.md                 Lens A
    ├── anchors.txt              Lens A — frame anchors, one per line
    ├── style-vocab.md           Lens W
    ├── wordlist.tsv             Lens W — every content type × section, the audit layer
    ├── card.md                  Lens C
    └── manifest.json            the entry point
```

Section IDs are **A I M R D C** everywhere — file names, table columns, manifest keys.
Prose may say "Results and discussion"; machine-readable fields may not.

## Workflow

### Stage 0 — prep (REQUIRED, always first)

```bash
py -3.10 scripts/prep.py <paper.pdf> --slug <slug> --out <corpus-root>
```

Read `references/stage0-prep.md`. Never skip this and never let a lens read the PDF
directly. Journal PDFs carry printer's ligatures (ﬁ ﬂ); against the raw PDF
`quant_check count` silently returns **0** for every word containing them — measured on
one Elsevier paper: *fitted* 0/21, *significant* 0/17, *confidence* 0/15, *first* 0/13,
*difficult* 0/7. Those are core terms and nothing warns you.

If prep stops because it cannot find a section, it prints the paper's numbered headings.
Re-run with `--marks`. **Do not work around it by guessing offsets** — a wrong split
silently corrupts every per-section band downstream.

### Lens A — architecture and frames → `logic.md`, `anchors.txt`

Read `references/lens-architecture.md`. Produces the structure tree, per-paragraph
function tags and relations, representative intra-paragraph chains, and an **exhaustive**
sentence-frame catalog with `[P#-S#]` addresses, then validates recurrence by measuring
frame anchors. The anchor gate is not optional: on a test run it caught **five verbatim
errors in 219 sentences** that reading alone had produced.

### Lens W — style vocabulary → `style-vocab.md`, `wordlist.tsv`

```bash
py -3.10 scripts/wordlist.py <corpus-root>/papers/<slug>     # the count layer, first
```

Read `references/lens-vocabulary.md`. `wordlist.py` builds the complete count layer with a
frozen stop list and a frozen general-academic list, so type counts and the
academic/topic split are reproducible between runs rather than re-decided each time. It
also writes `wordlist.stats.json` — quote those numbers, do not recount them.

Then measure the style-bearing lexicon per section: reporting verbs, hedges, boosters,
stance, connectives, general academic nouns. Domain nouns stay in `wordlist.tsv` and are
**not** classified or contextualized in `style-vocab.md`.

### Lens C — Style Card → `card.md`

Read `references/lens-card.md`. Selects from A and W and adds the P indicators the other
two cannot see (tense, person, citation integration, display-item form, absences).

**Why C is last.** The card's two most useful findings on the test paper could only come
from the other lenses: the reporting-verb hierarchy (*report** for prior work,
*indicat*/suggest** for the author's own inference, *show** only for display items) came
from W's per-section measurement, and the rule *"imitate the frame type, never the
wording"* came from A's anchor test (190 of 193 frames occur exactly once). A card written
first would have contained neither.

**The card stays lean.** Bulk lives in `logic.md` and `wordlist.tsv`; the card selects.
A previous version of this skill pushed a 145-line measurement block *into* the card and
the sentence-frame section shrank from 40 lines to 26 to make room — the card grew 2.4×
while the part a reviser could act on shrank. Put nothing in the card that has a home in
another file.

### Stage 4 — manifest

Read `references/manifest.md`. `prep.py` already filled every deterministic field and left
the judgment fields `null`. Fill them. **A manifest still containing `null` is an
incomplete extraction** — that is the completeness check, and it is meant to be cheap.

Then update `<corpus>/index.md`. Fixed format — one row per paper, numbers lifted from the
manifests, nothing re-derived:

```markdown
# Style Corpus: <name>

| slug | source | venue / year | scheme | frames (Sing./Tot.) | Z rate | card |
|------|--------|--------------|--------|--------------------|--------|------|
| kim-2015-nitrate-iso | kkh_nitrate_iso.pdf | Agric. Ecosyst. Environ. 199 (2015) | IMRC | 190/193 | 30% | [card](papers/kim-2015-nitrate-iso/card.md) |

## Measured bands by section
One table per section, one row per paper. A band needs three or more papers;
with fewer, print the values and say so rather than calling them a band.

### Methods
| slug | avg_sent_len | hedges/1k | passive/1k |
|------|--------------|-----------|------------|
| kim-2015-nitrate-iso | 33.1 | 8.9 | 21.3 |

## Notes
- Counting basis: `sections/*.txt` per paper (never body.txt — it includes the abstract).
- Papers extracted under different skill versions are not comparable; record the version.
- Nothing here is merged. Downstream applies 2-3 cards side by side.
```

`scheme` is the section string from `manifest.prep.section_scheme` (`IMRC`, `IMRDC`…) and
tells a consumer at a glance whether a paper fuses Results and Discussion.

### Multiple papers

Dispatch one subagent per paper. Paper bodies are the largest thing this skill touches and
none of it needs to reach the main conversation. Each subagent runs Stage 0 → A, W → C →
manifest for its own paper and returns only the manifest summary.

Cards are per-paper and are never merged. Downstream applies two or three side by side and
lays out candidates. For a deliberate corpus consensus — and only then — read
`references/aggregate.md`.

## Lens division of labor

| Lens | Owns | Must NOT re-emit |
|------|------|------------------|
| **A** | structure, paragraph logic, sentence frames, anchors | word frequencies, aggregate rates |
| **W** | measured lexicon by section, POS, collocates | frames, structure |
| **C** | selection + P indicators + red flags | the full catalogs it draws from |

## Two rules to carry into every card

1. **Imitate the frame TYPE, never the anchor WORDING.** Frame types recur heavily
   (passive-procedure 17×, results-suggest 13×); exact wordings almost never do. Copying an
   anchor verbatim produces a repetition the author does not commit.
2. **Numbers diagnose; they do not set targets.** Report a measured rate as an observation,
   never as a value a draft should be edited toward. A rate is the result of other choices,
   not a handle. Compare a draft section to its own section row — never to a whole-paper
   figure, and never to `body.txt`, which includes the abstract.

## Notes

- Preserve quoted sentences verbatim, tagged `[P#-S#]`, in **every** file including the
  card — that address is what joins the three documents.
- Record the `quant_check` version on anything measured. Bands from different versions are
  not comparable.
- Symbols (δ¹⁵N, Cl⁻) do not survive PDF text extraction. Take symbols from the page
  images, word content from the text layer, and never anchor a frame on a symbol.

---
**Version**: 3.0.0 (corpus build: Stage 0 prep, fixed folder contract, manifest;
absorbs measured frame-recurrence and section-scoped vocabulary; domain terminology
delegated to extraction-knowledge)
**Skill**: Meta_researcher / metasci-style-extraction
