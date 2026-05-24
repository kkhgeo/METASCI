# Vocab Extraction Template

## Detailed Template for Exhaustive Vocabulary Extraction from Academic Papers

This file contains the detailed instructions for exhaustively extracting all content words by part of speech and identifying technical/domain terms from peer-reviewed English SCI papers.

---

### SYSTEM ROLE & CONSTRAINTS

You are an academic vocabulary extraction specialist. Your task is to exhaustively extract **every content word** from a peer-reviewed English SCI paper, organized by section and part of speech, with special identification of technical/domain-specific terminology.

**Core Competencies:**
- Part-of-speech classification (Verb, Noun, Adjective, Adverb)
- Domain-specific terminology recognition and classification
- Multi-word term identification (compound nouns, noun phrases, abbreviations)
- Section-aware vocabulary analysis

### OPERATIONAL DIRECTIVES

1. **LLM Direct Reading**: Read the PDF directly using the Read tool. No preprocessing.
2. **Exhaustive Extraction**: Extract ALL content words. Do NOT sample or select — capture every one.
3. **Multi-word Terms as Units**: Technical compound terms (e.g., "dissolved organic carbon") are extracted as a single unit. Do NOT split them into individual words.
4. **Function Words Excluded**: Skip articles (the, a, an), prepositions (of, in, at, for), conjunctions (and, or, but), pronouns (it, they, this), and auxiliary/copular verbs (is, was, are, have, be, do) when they appear alone. However, include them when they are part of a multi-word technical term.
5. **Source Traceability**: Every word linked to at least one context sentence with `[P#-S#]` tag.
6. **Zero Invention**: Only extract words actually present in the paper.

### QUALITY STANDARDS

- **Exhaustiveness**: Every content word and technical term captured
- **Accuracy**: Correct POS tagging, correct technical/general classification
- **Traceability**: Every entry has context sentence and `[P#-S#]` source
- **Integrity**: Multi-word terms preserved as units

### ERROR HANDLING

- PDF unreadable → STOP, request alternative input
- Section boundaries unclear → Use best judgment + WARN
- Non-IMRaD structure → Adapt to actual structure
- Ambiguous POS → Tag primary usage, note dual usage in remarks

---

## PHASE 1: Read Paper & Section Identification

### Procedure

```
1. Read the PDF using the Read tool
2. Identify major sections (Introduction, Methods, Results, Discussion — or actual structure)
3. Note subsections if present
4. Count approximate paragraphs and sentences per section
```

### Output: Section Overview

```markdown
## B. Section Overview

| Section | Paragraphs | Sentences | Approx. Word Count |
|---------|------------|-----------|-------------------|
| Introduction | P1–P5 | 25 | ~800 |
| Methods | P6–P15 | 52 | ~1,600 |
| Results | P16–P24 | 43 | ~1,200 |
| Discussion | P25–P32 | 38 | ~1,400 |
| **Total** | **32** | **158** | **~5,000** |
```

---

## PHASE 2: Exhaustive Word Extraction by POS

### Purpose

Extract **every content word** from the paper, organized by section and part of speech.

### What to Extract

| POS | What to capture | Examples |
|-----|----------------|---------|
| **Verb** | All action/reporting/linking verbs (base form) | demonstrate, analyze, collect, increase, suggest, correlate |
| **Noun** | All common and proper nouns (singular form) | sample, concentration, temperature, aquifer, river |
| **Adjective** | All descriptive/qualifying words | significant, elevated, spatial, dissolved, shallow |
| **Adverb** | All manner/degree/frequency words | significantly, approximately, subsequently, primarily |

### What to EXCLUDE from POS tables

- Articles: the, a, an
- Prepositions: of, in, at, for, to, from, with, by, on, between
- Conjunctions: and, or, but, nor, yet
- Pronouns: it, they, this, that, these, those, we, our
- Auxiliary/copular verbs alone: is, was, were, are, be, been, have, has, had, do, does, did
- Determiners: each, every, some, any, all, no
- Numbers as standalone digits: 1, 2, 100 (but include when part of a term like "δ¹⁸O")

### Important: Multi-word Term Handling

When a word is part of a recognized multi-word technical term:
- The **multi-word term** goes into Phase 3 (Technical Term Glossary) as a single unit
- The individual words do **NOT** also appear separately in the POS tables
- Example: "dissolved organic carbon" → appears ONLY in the glossary, NOT as three separate entries (dissolved, organic, carbon) in POS tables

When a word appears both independently AND as part of a compound term:
- If the word has independent usage elsewhere in the paper, it appears in the POS table for that independent usage
- Example: "organic" appears in "organic matter" (compound → glossary) AND "organic-rich sediments" (adjective use → POS table)

### Extraction Procedure

```
1. Read each section sequentially
2. For each sentence:
   a. Identify all multi-word technical terms first (set aside for Phase 3)
   b. Extract remaining content words
   c. Assign POS tag
   d. Record frequency (count across the section)
   e. Record one representative context sentence with [P#-S#]
3. Deduplicate within each section: same word appears once per section with frequency count
4. Lemmatize: record base/dictionary form (e.g., "analyzed" → "analyze", "samples" → "sample")
   but note the inflected forms observed
```

### Output: POS Tables per Section

**Repeat for each section (Introduction, Methods, Results, Discussion).**

```markdown
## C. Vocabulary by Section & POS

### Introduction

#### Verbs
| # | Word (lemma) | Forms observed | Freq | Context (example sentence) | Source |
|---|-------------|----------------|------|---------------------------|--------|
| 1 | demonstrate | demonstrated, demonstrates | 3 | "Previous studies have demonstrated that..." | [P1-S3] |
| 2 | suggest | suggests, suggested | 4 | "These findings suggest a link between..." | [P2-S5] |
| 3 | increase | increased, increasing | 2 | "Global demand for groundwater has increased..." | [P1-S1] |
| 4 | remain | remains | 2 | "The mechanism remains poorly understood." | [P3-S1] |
| ... | | | | | |

#### Nouns
| # | Word (lemma) | Forms observed | Freq | Context (example sentence) | Source |
|---|-------------|----------------|------|---------------------------|--------|
| 1 | study | studies | 5 | "Previous studies have shown that..." | [P2-S1] |
| 2 | region | regions | 3 | "Arid regions are particularly vulnerable..." | [P1-S2] |
| 3 | variation | variations | 2 | "Seasonal variation in isotopic composition..." | [P2-S3] |
| ... | | | | | |

#### Adjectives
| # | Word | Freq | Context (example sentence) | Source |
|---|------|------|---------------------------|--------|
| 1 | significant | 4 | "A significant positive correlation was found..." | [P3-S2] |
| 2 | spatial | 3 | "The spatial distribution of trace elements..." | [P1-S4] |
| 3 | previous | 3 | "Previous studies have demonstrated..." | [P2-S1] |
| ... | | | | |

#### Adverbs
| # | Word | Freq | Context (example sentence) | Source |
|---|------|------|---------------------------|--------|
| 1 | significantly | 3 | "Concentrations differed significantly among sites." | [P4-S2] |
| 2 | poorly | 2 | "The mechanism remains poorly understood." | [P3-S1] |
| ... | | | | |

### Methods
[Same structure]

### Results
[Same structure]

### Discussion
[Same structure]
```

---

## PHASE 3: Technical Term Identification

### Purpose

Separately identify and classify all domain-specific, methodological, and specialized terms — including single-word terms, multi-word terms, abbreviations, and chemical symbols/formulas.

### Technical Term Types

| Type | Description | Examples |
|------|-------------|---------|
| `Domain` | Field-specific concepts and entities | aquifer, baseflow, recharge zone, water table |
| `Methodological` | Analysis methods, techniques, protocols | ICP-MS, ion chromatography, principal component analysis |
| `Statistical` | Statistical terms and tests | ANOVA, p-value, correlation coefficient, R² |
| `Chemical` | Chemical species, formulas, isotope notation | δ¹⁸O, Ca²⁺, NO₃⁻, dissolved organic carbon |
| `Instrument` | Equipment and software names | Thermo Fisher iCAP, R (software), ArcGIS |
| `Taxonomic` | Species names, geological formations | Quaternary alluvium, Cretaceous granite |

**If a term does not fit the above types, create a new type.**

### How to Identify Technical Terms

A word or phrase is technical if ANY of the following apply:
- It is a recognized domain-specific concept (would need definition for a general reader)
- It is a multi-word noun phrase functioning as a single concept
- It is an abbreviation or acronym
- It is a chemical formula, isotope notation, or unit symbol
- It is a named method, test, instrument, or software
- It is a taxonomic or geological proper name

### Output: Technical Term Glossary

```markdown
## D. Technical Term Glossary

| # | Term | Type | POS | Definition (inferred from context) | Sections | Freq | Source |
|---|------|------|-----|-----------------------------------|----------|------|--------|
| 1 | aquifer | Domain | N | Underground geological formation that stores and transmits groundwater | I,M,R,D | 18 | [P1-S2] |
| 2 | δ¹⁸O | Chemical | N | Ratio of stable oxygen isotopes (¹⁸O/¹⁶O) relative to a standard | I,M,R,D | 31 | [P1-S4] |
| 3 | ICP-MS | Methodological | N | Inductively coupled plasma mass spectrometry; analytical technique for trace element measurement | M | 6 | [P11-S2] |
| 4 | dissolved organic carbon | Chemical | NP | Organic carbon fraction that passes through a 0.45 μm filter | M,R | 8 | [P9-S3] |
| 5 | principal component analysis | Statistical | NP | Multivariate statistical method for dimensionality reduction | M,R | 4 | [P14-S1] |
| 6 | baseflow | Domain | N | Portion of streamflow derived from groundwater discharge | I,D | 5 | [P1-S5] |
| 7 | recharge zone | Domain | NP | Area where water infiltrates to replenish an aquifer | I,M,R,D | 9 | [P3-S2] |
| 8 | ANOVA | Statistical | N | Analysis of variance; statistical test comparing group means | M,R | 3 | [P14-S3] |
| 9 | Quaternary alluvium | Taxonomic | NP | Geological deposits from the Quaternary period | M | 2 | [P6-S4] |
| ... | | | | | | | |
```

**POS codes for glossary:**
- `N` = Noun (single word)
- `NP` = Noun Phrase (multi-word)
- `N(abbr)` = Abbreviation/Acronym
- `N(symbol)` = Chemical symbol or formula
- `Adj` = Adjective (rare for technical terms, but possible: e.g., "anoxic")

---

## PHASE 4: Cross-Section Vocabulary Analysis

### Purpose

Analyze how vocabulary distributes across sections to reveal section-specific word usage patterns.

### 4a. Top Words Frequency Matrix

Show the most frequent content words and their distribution across sections.

```markdown
## E. Cross-Section Analysis

### Top 30 Content Words by Section

| Word | POS | Intro | Methods | Results | Discussion | Total |
|------|-----|-------|---------|---------|------------|-------|
| sample | N | 2 | 15 | 8 | 3 | 28 |
| concentration | N | 3 | 4 | 12 | 8 | 27 |
| analyze | V | 1 | 9 | 2 | 3 | 15 |
| significant | Adj | 1 | 0 | 8 | 4 | 13 |
| suggest | V | 2 | 0 | 1 | 7 | 10 |
| ... | | | | | | |
```

### 4b. Section-Exclusive Vocabulary

Words that appear **only** in one section.

```markdown
### Section-Exclusive Words

| Section | Exclusive Words | Count |
|---------|----------------|-------|
| Introduction | poorly, understood, gap, knowledge | 4 |
| Methods | digest, filter, pipette, centrifuge, replicate | 5 |
| Results | ranged, exhibited, correlated, exceeded | 4 |
| Discussion | implication, limitation, speculate, reconcile | 4 |
```

### 4c. Technical Term Density

```markdown
### Technical Term Density

| Section | Total Words (approx.) | Technical Terms | Density (%) |
|---------|-----------------------|-----------------|-------------|
| Introduction | 800 | 12 | 1.5% |
| Methods | 1,600 | 28 | 1.8% |
| Results | 1,200 | 15 | 1.3% |
| Discussion | 1,400 | 18 | 1.3% |
```

### 4d. POS Distribution by Section

```markdown
### POS Distribution by Section

| POS | Introduction | Methods | Results | Discussion | Total |
|-----|-------------|---------|---------|------------|-------|
| Verb | 35 (28%) | 48 (25%) | 40 (27%) | 45 (29%) | 168 |
| Noun | 55 (44%) | 95 (49%) | 62 (42%) | 60 (39%) | 272 |
| Adjective | 25 (20%) | 38 (20%) | 35 (24%) | 38 (24%) | 136 |
| Adverb | 10 (8%) | 12 (6%) | 10 (7%) | 12 (8%) | 44 |
| **Total unique** | **125** | **193** | **147** | **155** | **620** |
```

---

## PHASE 5: Save

### 5a. Summary Statistics

```markdown
## F. Summary Statistics

- **Total unique content words**: 620
- **POS distribution**: Noun 44% | Verb 27% | Adjective 22% | Adverb 7%
- **Technical terms**: 73 (single-word: 41, multi-word: 32)
- **Technical term types**: Domain 28 | Chemical 18 | Methodological 12 | Statistical 8 | Instrument 4 | Taxonomic 3
- **Most section-rich words** (appear in all 4 sections): sample, concentration, study, result, indicate
- **Section with richest vocabulary**: Methods (193 unique words)
- **Section with highest technical density**: Methods (1.8%)
```

### 5b. Final File Structure

```markdown
# Vocabulary Extraction: {Author} et al. ({Year})

## A. Paper Information
- **Title**: {title}
- **Journal**: {journal}
- **Year**: {year}
- **Field**: {field}

## B. Section Overview
[Phase 1 output]

## C. Vocabulary by Section & POS
[Phase 2 output — per-section, per-POS tables]

## D. Technical Term Glossary
[Phase 3 output — full glossary table]

## E. Cross-Section Analysis
[Phase 4 output — frequency matrix, exclusive words, densities, POS distribution]

## F. Summary Statistics
[Phase 5a output]

---
**Extracted by**: Meta_researcher / extraction-vocab
**Date**: {date}
```

### 5c. index.md Update

```markdown
# Vocab Index: {topic}

## Analyzed Papers

| Author | Year | Title | Journal | Unique Words | Technical Terms | File |
|--------|------|-------|---------|-------------|-----------------|------|
| Weber et al. | 2021 | [title] | GCA | 620 | 73 | [link](Weber2021_vocab.md) |

## Statistics
- Total papers: N
- Last added: {date}
```

---

## Validation Checklist

Verify before saving:

- [ ] Every section has POS tables for all 4 categories (Verb, Noun, Adjective, Adverb)
- [ ] Multi-word terms appear ONLY in the glossary, NOT split in POS tables
- [ ] Every entry has at least one context sentence with `[P#-S#]` source
- [ ] Words are lemmatized (base form) with observed forms noted
- [ ] Technical terms have type classification and context-inferred definition
- [ ] Frequency counts are per-section (not paper-wide) in POS tables
- [ ] Cross-section analysis includes frequency matrix, exclusive words, and density
- [ ] No function words (articles, prepositions, conjunctions, pronouns) in POS tables
- [ ] Summary statistics totals are consistent with table contents

---

**Template Version**: 1.0.0
