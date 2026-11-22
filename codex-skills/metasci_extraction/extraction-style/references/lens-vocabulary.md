# Lens W — Style Vocabulary

**Output**: `style-vocab.md`, `wordlist.tsv`, `phrases.tsv`, `phrase-functions.tsv`
**Reads**: `sections/*.txt` (never the PDF)

Measure the words that carry *voice*, per section. This is the lexical half of style;
Lens A covers structure.

---

## The boundary, and why it is drawn here

**Count everything; classify selectively.** The two count layers are exhaustive:
`wordlist.tsv` holds every content type, Freq 1 included, and `phrases.tsv` holds every
2–4-word sequence that occurs twice or more. They are written by scripts, so they are
complete and identical between runs. What is selective is the *classification and
contextualization* in `style-vocab.md`.

These layers replaced the retired `extraction-vocab` skill (now in `legacy-skills/`). Its
LLM-written lists of every content word duplicated `wordlist.tsv`, and its counts ran
against the raw PDF, where words containing printer's ligatures (ﬁ ﬂ) return zero. The one
function it had that nothing else did, the technical-term glossary, moved to Lens T
(`references/lens-terminology.md`).

Measured on the test paper, of 535 content types occurring twice or more:

| | types | share |
|---|-------|-------|
| general academic — travels to another manuscript | 61 | **11%** |
| topic, proper nouns, technical terms — travels nowhere | 474 | **89%** |

The 89% is *nitrate*(158), *groundwater*(92), *manure*(53), *fertilizers*(34). A reviser
writing about something else can use none of it in a style revision.

**So: Lens W classifies the 11%. The 89% is counted into `wordlist.tsv`, and Lens T reads
it from there for the glossary.** Neither lens re-lists it in `style-vocab.md`.

`wordlist.tsv` is machine-generated, costs nothing, and is the audit trail that lets anyone
re-derive or dispute a number later. It is not a failure of leanness to keep it; it is a
failure of leanness to *classify and contextualize* it.

## W.1 What to collect

Per section (I, M, R, D, C), measured — never estimated:

1. **Reporting verbs** — how findings and claims are introduced. Record which section each
   concentrates in; the skew is the finding, not the total.
2. **Hedges** — modal and lexical: *can be, may, might, likely, possibly, generally,
   usually, often, appears, seems, assuming, partially, relatively, approximately*.
3. **Boosters / stance** — *significantly, clearly, markedly, largely, mainly, highly,
   demonstrably*. Note whether they are statistical or evaluative; *significant* attached to
   a p-value is not stance.
4. **Attitude markers** — *interestingly, surprisingly, unfortunately, remarkably*.
   Usually zero in this genre. **Zero is a result** and becomes a red flag.
5. **Connectives** — *however, therefore, thus, moreover, furthermore, nevertheless,
   in contrast, additionally, specifically*. Record position (sentence-initial vs mid) and
   **per-section counts**, including the zeros.
6. **Self-mention** — *we, our, this study, the present study*. Count and note what the
   author reserves it for.
7. **General academic nouns** — *approach, framework, procedure, evidence, uncertainty,
   dataset, parameter, assumption, implication*. The transferable 11%.
8. **Register habits** — recurring non-technical set phrases: *regardless of, according to,
   with relation to, at first glance, it is noted that, it was found that*.
9. **Caption / display verbs** — *shows, presents, summarizes, illustrates, comparing*.
   Gate-exempt: a paper with two figures cannot produce Freq ≥ 2.
10. **Lexical bundles** — the 3- and 4-word sequences of `phrases.tsv` with `bundle = yes`
    and `topic = no`, classified by function (W.6).

**Do not collect in `style-vocab.md`**: domain nouns, chemical species, instrument names,
place names, author names. They are counted in `wordlist.tsv` and `phrases.tsv`, and Lens T
turns the technical ones into `glossary.md`.

## W.2 How to measure

### Step 1 — the complete count layer

Tokenize each section file, drop the frozen stop list and single letters, and write every
remaining type with its per-section frequency, range, inflection family and POS:

```bash
py -3.10 scripts/wordlist.py <corpus-root>/papers/<slug>
```

```
wordlist.tsv
type	A	I	M	R	C	total	range	family	pos	class
nitrate	3	29	12	101	16	161	5	nitrate	NOUN	other
samples	0	2	31	9	1	43	4	sample	NOUN	other
```

This is mechanical. Generate it, do not curate it. Every type is written, hapaxes included;
only single letters and the frozen stop list are dropped (v2.0.0; v1 also dropped every
token of three letters or fewer and so lost *pH*, *ion*, *age*, *map*).

- `range` is the number of sections containing the type.
- `family` folds regular inflections onto an attested base (*samples* → *sample* only
  when *sample* itself occurs). With spaCy installed it is spaCy's lemma instead.
- `pos` is filled by spaCy (`pip install spacy`, `python -m spacy download
  en_core_web_sm`). Without it the column is empty and `wordlist.stats.json` records
  `pos_tagger: none`. Do not fill it by hand: a hand-tagged column is exactly the
  unreproducible layer this script exists to replace.

### Step 1b — the multi-word layer

```bash
py -3.10 scripts/phrases.py <corpus-root>/papers/<slug>
```

Writes every 2-, 3- and 4-word sequence at Freq ≥ 2, per section, to `phrases.tsv`, plus
`phrases.stats.json`. Sequences never cross punctuation, a number or a symbol.

```
phrase	n	A	I	M	R	C	total	per_million	range	bundle	topic	nested_in	function	subfunction
in the case of	4	0	2	3	4	1	10	1293	4	yes	no		text	framing
the nitrate concentrations of	4	0	1	0	3	0	4	517	2	yes	yes
```

The selection follows the lexical-bundle definition of Biber et al. (1999, ch. 13) and
Hyland (2008, *ESP* 27: 4–21) — a frequency floor and a dispersion floor — adapted to one
paper:

| criterion | Biber 1999 / Hyland 2008 (corpus) | here (one paper) |
|-----------|-----------------------------------|------------------|
| length | 3+ words / 4 words | `bundle` at n = 3–4; n = 2 kept as a collocation layer |
| frequency | 10 / 20 per million words | `--min-freq 2` raw occurrences |
| dispersion | 5 texts / 10% of texts | `--min-range 2` sections |

The per-million floors cannot be applied to one paper: at 8,000 tokens, 20 per million is
0.16 occurrences. `per_million` is still written so that `aggregate.md` can apply the
published thresholds across a corpus, where they mean what their authors meant.

Two further columns are deterministic:

- `topic = yes` when the sequence contains a content word outside the frozen stop,
  general-academic and phrasal lists. These rows are topic-bound: they go to Lens T as
  term candidates (*dissolved organic carbon*) and never onto the card.
- `nested_in` names the longer sequence a shorter one always occurs inside (equal
  frequency). Nested fragments are not counted as bundles of their own, so
  *was found that the* does not double-count *it was found that*.

### Step 2 — lemma families

Surface forms fragment a lemma (*report / reports / reported*), so counting them
separately understates every verb. Build an items file with suffix wildcards and measure
per section:

```bash
py -3.10 scripts/quant_check.py count --items items.txt --per-file sections/*.txt
```

`report*` covers the family. `show*` also catches *shown*, which a bare `show` misses.

### Step 3 — evidence gate

An item enters `style-vocab.md` only at measured **Freq ≥ 2**. One use is not a register.
Exception: an item may stay at Freq 1 flagged `(rare-but-marked)` when it is a genuinely
unusual move — at most one or two per paper. On the test paper *successfully* (1) and
*convincingly* (1) qualified: they are the only evaluative adverbs the author ever applies
to the study's own performance, and they sit four words apart.

**The measurement wins.** If the script returns 0 for a word you are sure you read, check
`sections/*.txt` before claiming a counting artifact. In testing, such disputes were the
reading impression being wrong.

### Step 4 — collocates for the register habits

```bash
py -3.10 scripts/quant_check.py collocates --node "uncertainty" --window 4 body.txt
```

Use for set phrases and coined terms, not for domain nouns.

## W.3 The reporting-verb hierarchy

This is the single most transferable output of the lens. Totals alone are useless; the
**reservation** is the instruction. Measured on the test paper:

| verb | total | I | M | R | C | reserved for |
|------|-------|---|---|---|---|--------------|
| show* | 23 | 3 | 2 | **16** | 2 | display items — "Fig. 3 shows…" |
| indicat* | 15 | 1 | **0** | **12** | 2 | the author's own inference |
| suggest* | 10 | 0 | 1 | **8** | 1 | the same inference, weaker |
| report* | 10 | **4** | 2 | 4 | 0 | **prior literature only** |
| reveal* | 7 | 1 | 1 | **5** | 0 | what an analysis uncovered |
| demonstrat* | 4 | **2** | 0 | 2 | 0 | rationed — 4 uses in 7,733 tokens |

Always emit this table with a `reserved for` column. "show* 23" tells a reviser nothing;
"show* 23, display items only" is directly actionable.

## W.4 Read the zeros

A zero in a section is as informative as a large number and is easy to miss because nothing
draws the eye to it.

On the test paper `however` = **0 across all 1,688 tokens of Methods**. That corroborates,
from the lexical side, what Lens A found structurally — Methods contains no contrast
relation at all. Two independent lenses reaching the same conclusion is the strongest
evidence this skill produces. Look for such agreements and state them.

## W.5 Type/token texture

Report unique types and tokens per section. On the test paper the Introduction ran a
type/token ratio of 0.319 against 0.156 in Results — the Introduction says each thing once,
the Results section hammers its subject. That is a rhythm a reviser can hear, and it comes
free from Step 1.

## W.6 Bundle function — the only judgment in the phrase layer

Classify every row with `bundle = yes` and `topic = no` by Hyland's (2008) functional
taxonomy. Read each in its contexts (`quant_check.py collocates` or a grep of
`sections/*.txt`), not from the phrase alone: *as a result of* is a resultative signal in
one paper and a procedure in another.

| function | subfunction | examples |
|----------|-------------|----------|
| `research` — the real world of the study | `location` · `procedure` · `quantification` · `description` · `topic` | *at the end of*, *the use of the*, *a wide range of*, *the structure of the* |
| `text` — the organisation of the text | `transition` · `resultative` · `structuring` · `framing` | *on the other hand*, *as a result of*, *as shown in Fig*, *in the case of* |
| `participant` — writer and reader | `stance` · `engagement` | *it is likely that*, *it should be noted that* |

Write the labels to `phrase-functions.tsv` in the paper folder, one row per bundle:

```
in the case of	text:framing
it was found that	participant:stance
```

and merge:

```bash
py -3.10 scripts/phrases.py <corpus-root>/papers/<slug> --functions <corpus-root>/papers/<slug>/phrase-functions.tsv
```

The merge refuses the whole file on an unknown phrase, an unknown label or a duplicate, and
reports any non-topic bundle still unclassified. Keep `phrase-functions.tsv`: re-running
the count step rewrites `phrases.tsv` with empty function columns, and the merge restores
them. A topic-flagged row may be classified when reading shows it is not topic-bound; the
merge allows it and lists it.

What goes into `style-vocab.md` is the result, not the table: the function distribution,
the bundles that concentrate in one section (the skew is the finding, as with reporting
verbs), and the participant-oriented bundles in full, because they carry stance. The full
table stays in `phrases.tsv`.

## W.7 Output file

```
style-vocab.md
  A. Paper information + counting source + declared scope
  B. Section overview (tokens · types · type/token · measured rates from the manifest)
  C. Style lexicon by section
       Reporting verbs (with the reserved-for table)
       Hedges · Boosters/stance · Attitude markers · Connectives · Self-mention
       General academic nouns · Register habits · Caption verbs
       Lexical bundles — function distribution, section skews, stance bundles
       — each with measured Freq, per-section split, and one verbatim context [P#-S#]
  D. Cross-section observations (skews, zeros, exclusives, type/token)
  E. Summary statistics
```

State the counting source and the ligature note at the top of the file. Every quoted
context carries its `[P#-S#]` address — that is what links this file to `logic.md`.

Then fill `manifest.vocabulary`, including `vocabulary.bundles`.

## What belongs elsewhere

| You find yourself writing | It belongs in |
|---------------------------|---------------|
| a definition of a technical term | `glossary.md` (Lens T) |
| a table of every noun in the paper | `wordlist.tsv`, unclassified |
| a table of every recurrent phrase | `phrases.tsv` |
| a sentence template | `logic.md` (Lens A) |
| an aggregate rate as a target | nowhere — rates diagnose, they do not set targets |
