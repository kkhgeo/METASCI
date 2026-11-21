---
name: extraction-style
description: |
  Build a reusable STYLE CORPUS from reference papers — one folder per paper holding
  normalized text, per-section splits, an exhaustive sentence-frame catalog, an
  exhaustive word list and phrase list (2–4-word n-grams, lexical bundles) counted by
  script, a measured style vocabulary, an optional technical-term glossary, a lean Style
  Card, and a machine-readable manifest.
  Lenses over shared, pre-normalized text — A (architecture + sentence frames),
  W (word and phrase layers + style vocabulary, measured by section),
  T (technical-term glossary, optional), C (Style Card: V/L/P indicators + red flags).
  Use whenever the user wants to "extract style", "스타일 추출", "문체 추출",
  "이 논문들 스타일 뽑아줘", capture a journal's writing conventions, or build a style
  reference for later rewriting with meta-styling. Also the home of word, phrase and
  term extraction: "단어 추출", "어휘 추출", "구 추출", "표현 추출", "용어 추출",
  "용어집", "lexical bundle", "n-gram", "vocabulary extraction", "term extraction".
  NOT for domain knowledge or claims ("지식 추출" → extraction-knowledge), NOT for an
  exhaustive argument map (→ extraction-logic), NOT for applying a style to a draft
  (→ meta-styling).
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, Agent]
---

# META-SCI · Style Extraction (corpus build)

Produce a **style corpus**: one folder per paper, always the same files, always the same
names, so a downstream skill can find things by path instead of by reading.

```
Stage 0  prep.py         PDF → body.txt + sections/ + manifest.json   (deterministic)
Lens A   architecture    structure · paragraph logic · frame catalog  → logic.md, anchors.txt
Lens W   vocabulary      every word + every recurrent phrase, counted;
                         style-bearing lexicon + bundle functions      → wordlist.tsv, phrases.tsv,
                                                                         style-vocab.md
Lens T   terminology     technical-term glossary (optional)           → glossary.md
Lens C   card            V/L/P selection + red flags                  → card.md
Stage 4  manifest        fill the null fields                         → manifest.json
```

A and W are independent and may run in parallel. T needs only W's two scripts. **C runs last** and cites A and W rather
than re-deriving them — this ordering is not cosmetic, see *Why C is last* below.

## Count everything, classify selectively

**The counting is exhaustive.** `wordlist.tsv` holds every content word of the paper,
hapaxes included, with section counts, range, inflection family and POS. `phrases.tsv`
holds every 2–4-word sequence that occurs twice or more, with the lexical-bundle,
topic and nesting flags. Both are written by scripts over the NFKC-normalized section
files, so they are complete, reproducible and immune to ligatures. They replace the
retired `extraction-vocab` skill (now in `legacy-skills/`), whose LLM-written word lists
duplicated these counts and broke on ligatures.

**What the paper argues or cites** is not collected here; that is `extraction-knowledge`.

**The style layers are selective.** `style-vocab.md` and `card.md` carry what travels to
another manuscript. Domain terms are counted, and Lens T can turn them into a glossary, but
they never enter the style layers. This boundary is measured, not a matter of taste. On a
representative paper, of the 535 content types occurring twice or more (wordlist v1),
**474 (89%) are topic-bound** — *nitrate*(158), *groundwater*(92), *manure*(53) — and
travel to no other manuscript. Only 61 (11%) are general academic words a reviser can
actually reuse. Carrying the other 89% into a style layer adds bulk and buries the usable
part.

**Complete in the count layers, lean in the style layers.** Function words, connectives,
reporting verbs, hedges, stance markers, bundles, sentence frames and section architecture
go into the style layers *in full*. Domain nouns stay in `wordlist.tsv`, `phrases.tsv` and
`glossary.md`.

| Job | Skill |
|-----|-------|
| Knowledge claims, citations, research questions | `extraction-knowledge` |
| Exhaustive argument map for proofreading | `extraction-logic` |
| **Style corpus for reuse** | **this skill** |
| **Every word, every recurrent phrase, technical glossary** | **this skill** — Lens W scripts + Lens T |
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
    ├── phrases.tsv              Lens W — every 2–4-gram at Freq ≥ 2, bundle/topic flags
    ├── phrase-functions.tsv     Lens W — the LLM's bundle labels, merged into phrases.tsv
    ├── glossary.md              Lens T — technical terms (only when Lens T ran)
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

### Lens W — words, phrases, style vocabulary → `wordlist.tsv`, `phrases.tsv`, `style-vocab.md`

```bash
py -3.10 scripts/wordlist.py <corpus-root>/papers/<slug>     # every word, first
py -3.10 scripts/phrases.py  <corpus-root>/papers/<slug>     # every recurrent 2–4-gram
```

Read `references/lens-vocabulary.md`. `wordlist.py` builds the complete word layer with a
frozen stop list and a frozen general-academic list, so type counts and the
academic/topic split are reproducible between runs rather than re-decided each time.
`phrases.py` builds the phrase layer and flags lexical bundles by the frequency and
dispersion criteria of Biber et al. (1999) and Hyland (2008), adapted to one paper
(Freq ≥ 2, range ≥ 2 sections, n = 3–4), and flags topic-bound sequences. Both write a
`*.stats.json` — quote those numbers, do not recount them.

The only judgment in the phrase layer is the bundle function: label each non-topic bundle
research-, text- or participant-oriented in `phrase-functions.tsv` and merge it with
`phrases.py --functions`. The merge validates every label.

Then measure the style-bearing lexicon per section: reporting verbs, hedges, boosters,
stance, connectives, general academic nouns. Domain nouns stay in `wordlist.tsv` and are
**not** classified or contextualized in `style-vocab.md`.

### Lens T — technical-term glossary → `glossary.md` (optional)

Read `references/lens-terminology.md`. Run it when the user asks for terms ("용어 추출",
"용어집", "전문용어") or for words "as fully as possible", or when a downstream review will
check term accuracy. Candidates come only from the scripts: every `class = other` row of
`wordlist.tsv` at any frequency, and every `topic = yes` row of `phrases.tsv`. The lens
screens them, types them (Domain, Methodological, Statistical, Chemical, Instrument,
Taxonomic, Coined), and defines each from the paper's own use with a `[P#-S#]` source.
Counts come from the TSVs, never from reading. Skipped, it leaves
`manifest.glossary = {"run": false}`.

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
| **W** | word and phrase layers, measured lexicon by section, bundle functions | frames, structure |
| **T** | technical terms: type, POS, definition, counts from the TSVs | style lexicon, frames |
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
**Version**: 3.1.0 (exhaustive word layer v2 and phrase layer — n-grams, lexical bundles,
Hyland functions; Lens T glossary absorbed from the retired extraction-vocab;
manifest schema 1.1.0)
Earlier: 3.0.0 (corpus build: Stage 0 prep, fixed folder contract, manifest; measured
frame-recurrence and section-scoped vocabulary)
**Skill**: Meta_researcher / extraction-style
