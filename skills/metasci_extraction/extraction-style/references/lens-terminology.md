# Lens T — Technical-term glossary

**Output**: `glossary.md`
**Reads**: `wordlist.tsv` (`class = other`), `phrases.tsv` (`topic = yes`), `sections/*.txt`,
and the page images for symbols. Never the PDF text layer.

This lens is the one function of the retired `extraction-vocab` skill that nothing else
covered: a glossary of the paper's domain terms, typed and defined from context. It sits in
the style corpus because the counting it needs already happens here; it stays out of
`style-vocab.md` and `card.md` because domain terms do not travel to another manuscript.

Lens T is optional. Run it when the user wants terminology ("용어 추출", "전문용어",
"용어집", "glossary", "단어 최대한 추출"), or when a downstream skill needs to check term
accuracy (`meta-review` B4, `meta-proofreading` terminology). It runs after Stage 0,
`wordlist.py` and `phrases.py`, and is independent of Lenses A, W and C.

---

## T.1 Candidates — counted, not recalled

The candidate list is the union of two script outputs. Do not add terms from memory of the
paper; if a term is missing from both files, check `sections/*.txt` before believing it is
there.

1. **Single words**: every row of `wordlist.tsv` with `class = other`, **at any frequency**.
   The glossary is exhaustive on terminology. A term used once (*anoxic*, *ICP-MS* in one
   Methods sentence) is still a term; the Freq ≥ 2 gate of Lens W is a register gate and
   does not apply here.
2. **Multi-word units**: every row of `phrases.tsv` with `topic = yes`, n = 2–4. Keep the
   longest sequence that names one concept (*dissolved organic carbon*, not *dissolved
   organic* and *organic carbon*). `nested_in` points at the longer candidate.

Then screen. A candidate is a technical term if any of these holds:

- it names a domain concept a general academic reader would need defined
- it is a noun phrase functioning as a single concept
- it is an abbreviation or acronym
- it is a chemical formula, isotope notation or unit
- it names a method, test, instrument, software, taxon, formation or site

Everything else in `class = other` (ordinary verbs and adjectives that the frozen academic
list does not happen to contain, author names, place names used only as locations) stays in
`wordlist.tsv`. Proper names enter the glossary only when they are themselves technical (a
formation, a standard, a named model).

## T.2 Types

| Type | Covers | Examples |
|------|--------|----------|
| `Domain` | field concepts and entities | aquifer, baseflow, recharge zone |
| `Methodological` | methods, techniques, protocols | ion chromatography, principal component analysis |
| `Statistical` | statistical terms and tests | ANOVA, correlation coefficient, R² |
| `Chemical` | species, formulas, isotope notation | δ¹⁸O, NO₃⁻, dissolved organic carbon |
| `Instrument` | equipment and software | ICP-MS, ArcGIS |
| `Taxonomic` | species, geological formations, named units | Quaternary alluvium |
| `Coined` | a term the paper defines for itself | "hereafter referred to as sample uncertainty" |

A term that fits none of these gets a new type, named in the file header.

`Coined` matters to style as well as content: a paper that names its own construct and then
reuses it is making a move Lens C may record as distinctive. Cite the defining sentence.

## T.3 POS codes

`N` noun · `NP` noun phrase · `N(abbr)` abbreviation or acronym · `N(symbol)` formula or
symbol · `Adj` adjective (*anoxic*, *isotopic*) · `V` verb (*denitrify*).

When `wordlist.tsv` carries a spaCy `pos` column, start from it and correct it only where
the term's use contradicts it, noting the correction.

## T.4 Counts and sources

- **Freq and Sections come from the TSV row, never from reading.** For a multi-word term
  use its `phrases.tsv` row; for a term family (*nitrate*, *nitrates*) sum the rows of one
  `family` and say so.
- **Symbols** (δ¹⁵N, Cl⁻, ¹⁸O) do not survive PDF text extraction. Take their form from the
  page images, mark the frequency `(reading count)`, and never anchor anything on them.
- **Definition** is inferred from the paper's own use, in one line. When the paper defines
  the term explicitly, quote that sentence instead and tag it.
- **Source** is the `[P#-S#]` address of the first defining or most informative use.
- **Top collocates** for the key terms only (high frequency or `Coined`):

  ```bash
  py -3.10 scripts/quant_check.py collocates --node "recharge" --window 4 sections/*.txt
  ```

## T.5 Output — `glossary.md`

```markdown
# Technical-term glossary: <Author> <Year>

**Counting source**: sections/*.txt · wordlist.py v2.x · phrases.py v1.x
**Candidates screened**: <n single words> + <n multi-word> → **<n> terms**

| # | Term | Type | POS | Definition (from context) | Sections | Freq | Top collocates | Source |
|---|------|------|-----|---------------------------|----------|------|----------------|--------|
| 1 | aquifer | Domain | N | Geological formation that stores and transmits groundwater | I,M,R,C | 18 | shallow, recharge | [P1-S2] |
| 2 | dissolved organic carbon | Chemical | NP | Organic carbon passing a 0.45 μm filter | M,R | 8 | concentrations | [P9-S3] |
| 3 | ICP-MS | Instrument | N(abbr) | Inductively coupled plasma mass spectrometry | M | 1 | — | [P11-S2] |
| 4 | δ¹⁸O | Chemical | N(symbol) | ¹⁸O/¹⁶O ratio relative to VSMOW | I,M,R | 31 (reading count) | values, depleted | [P1-S4] |

## Summary
| Type | Terms | Tokens | Share of content tokens |
| Section | Term tokens | per 1k tokens |     ← term density, from the TSV counts
```

Sort by Type, then by Freq descending. The density table is the one cross-section view this
lens adds: Methods usually carries the most `Methodological` and `Instrument` terms, and a
draft Methods section far below that density is often missing its procedural specifics.

## T.6 Relation to the other files

| file | holds | Lens T uses it as |
|------|-------|-------------------|
| `wordlist.tsv` | every content type | single-word candidates and counts |
| `phrases.tsv` | every recurrent 2–4-word sequence | multi-word candidates and counts |
| `style-vocab.md` | the transferable 11% | nothing — no overlap allowed |
| `card.md` | the selected style layer | nothing — no glossary on the card |
| `extraction-knowledge` output | cited knowledge claims | the definitions there may be fuller; this glossary records the paper's own usage |

Then fill `manifest.glossary`.
