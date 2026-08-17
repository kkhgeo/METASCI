# Lens W — Style Vocabulary

**Output**: `style-vocab.md`, `wordlist.tsv`
**Reads**: `sections/*.txt` (never the PDF)

Measure the words that carry *voice*, per section. This is the lexical half of style;
Lens A covers structure.

---

## The boundary, and why it is drawn here

`extraction-vocab` collects every content word with special attention to domain
terminology. That is the right job for proofreading and the wrong job here.

Measured on the test paper, of 535 content types occurring twice or more:

| | types | share |
|---|-------|-------|
| general academic — travels to another manuscript | 61 | **11%** |
| topic, proper nouns, technical terms — travels nowhere | 474 | **89%** |

The 89% is *nitrate*(158), *groundwater*(92), *manure*(53), *fertilizers*(34). A reviser
writing about something else can use none of it, and the technical glossary duplicates
`extraction-knowledge`, which does it better — with definitions, APA references and
translations.

**So: classify the 11%. Count the 89% into `wordlist.tsv` and stop there.**

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

**Do not collect**: domain nouns, chemical species, instrument names, place names, author
names, a technical glossary.

## W.2 How to measure

### Step 1 — the complete count layer

Tokenize each section file, drop function words and tokens ≤ 3 characters, and write every
remaining type with its per-section frequency:

```
wordlist.tsv
type	A	I	M	R	D	C	total
nitrate	3	29	12	101	0	16	161
```

This is mechanical. Generate it, do not curate it.

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

## W.6 Output file

```
style-vocab.md
  A. Paper information + counting source + declared scope
  B. Section overview (tokens · types · type/token · measured rates from the manifest)
  C. Style lexicon by section
       Reporting verbs (with the reserved-for table)
       Hedges · Boosters/stance · Attitude markers · Connectives · Self-mention
       General academic nouns · Register habits · Caption verbs
       — each with measured Freq, per-section split, and one verbatim context [P#-S#]
  D. Cross-section observations (skews, zeros, exclusives, type/token)
  E. Summary statistics
```

State the counting source and the ligature note at the top of the file. Every quoted
context carries its `[P#-S#]` address — that is what links this file to `logic.md`.

Then fill `manifest.vocabulary`.

## What belongs elsewhere

| You find yourself writing | It belongs in |
|---------------------------|---------------|
| a definition of a technical term | `extraction-knowledge` |
| a table of every noun in the paper | `wordlist.tsv`, unclassified |
| a sentence template | `logic.md` (Lens A) |
| an aggregate rate as a target | nowhere — rates diagnose, they do not set targets |
