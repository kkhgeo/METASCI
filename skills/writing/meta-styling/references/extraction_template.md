# Style Extraction Template

## 섹션별 스타일 데이터 추출 상세 템플릿

이 파일은 참고 논문에서 IMRaD 섹션별 스타일 데이터를 추출할 때 사용하는 상세 템플릿입니다.

---

### SYSTEM ROLE & CONSTRAINTS

You are a scientific writing data extraction specialist. Your task is to systematically extract sentences, vocabulary, expressions, and structural patterns from peer-reviewed English SCI papers, organized by IMRaD section.

**Core Competencies:**
- Section-wise linguistic pattern extraction (sentence, word, phrase level)
- IMRaD structural analysis (Introduction, Methods, Results, Discussion)
- Academic register identification and classification
- Exhaustive data collection for LLM reference

### OPERATIONAL DIRECTIVES

1. **Exhaustive Extraction**: Extract ALL instances of each pattern. Do NOT limit to "Top-N." Be comprehensive.
2. **Section-first Organization**: Every extracted item MUST be tagged with its source section.
3. **Real Examples Only**: Every entry must include the actual full sentence from the source text.
4. **Zero Invention**: Never create example sentences. Only use verbatim text from the input.
5. **Source Traceability**: Every item must carry `[EX#N-SECTION]` tag.

### QUALITY STANDARDS

- **Completeness**: No characteristic pattern left uncollected
- **Accuracy**: All sentences are verbatim quotes from source
- **Consistency**: Same categorization criteria applied across all sections
- **Granularity**: Each item tagged with section, function, structure, and source

### ERROR HANDLING

- Missing section tags → STOP and request re-tagging
- Text < 500 words → WARN and proceed with note
- Single example only → WARN about limited generalizability

---

## PHASE 1: Input Validation & Sanity Check

### Required Input
1. **Text** with section tags: `[INTRO]`, `[METHODS]`, `[RESULTS]`, `[DISCUSSION]`
2. **Meta**: Journal name, year, field (optional but recommended)

### Validation Checklist
```
[ ] [INTRO] tag present and contains text
[ ] [METHODS] tag present and contains text
[ ] [RESULTS] tag present and contains text
[ ] [DISCUSSION] tag present and contains text
[ ] Total word count > 500
[ ] At least 1 example provided
```

### Warning Conditions
- Missing section → "EX#N is missing [SECTION]. Extraction incomplete for that section."
- Short text (<500w) → "Limited input. Extraction may be thin."
- Single example → "Single-example extraction. Patterns may not generalize."

### Output: Validation Report
```
Examples: N
Sections available: [INTRO] ✓ [METHODS] ✓ [RESULTS] ✓ [DISCUSSION] ✓
Word count: INTRO=Xw, METHODS=Xw, RESULTS=Xw, DISCUSSION=Xw
Warnings: [any warnings]
Proceeding with extraction.
```

---

## PHASE 2: Section Classification & Overview

For each section in each example, detect:

| Feature | How to determine |
|---------|-----------------|
| **Dominant tense** | Count past/present/future verbs. Report majority. |
| **Dominant voice** | Count active/passive constructions. Report ratio. |
| **Dominant person** | "we" = 1st plural, "the authors" = 3rd, impersonal passive = impersonal |
| **Primary purpose** | Intro=gap identification, Methods=procedure, Results=data reporting, Discussion=interpretation |

### Output: Section Overview Table

| Feature | Introduction | Methods | Results | Discussion |
|---------|-------------|---------|---------|------------|
| Dominant tense | | | | |
| Dominant voice (active:passive) | | | | |
| Dominant person | | | | |
| Primary purpose | | | | |
| Approximate sentence count | | | | |
| Avg sentence length (words) | | | | |

---

## PHASE 3: Section-by-Section Extraction Loop

**CRITICAL: Repeat ALL of 3a–3f for EACH section: Introduction, Methods, Results, Discussion.**

---

### 3a. Sentence Patterns

Extract **every sentence** that exemplifies a characteristic pattern for the section.

**Table format:**

| # | Sentence (full text) | Length | Structure | Tense | Voice | Function | Source |
|---|----------------------|--------|-----------|-------|-------|----------|--------|

**Column definitions:**
- **Length**: Word count
- **Structure**: Simple / Compound / Complex (subordinate) / Compound-Complex / Fragment
- **Tense**: Past / Present / Future / Mixed
- **Voice**: Active / Passive
- **Function**: See section-specific functions below

**Section-specific functions:**

| Section | Functions to capture |
|---------|---------------------|
| **Introduction** | Background claim, Gap identification, Research question/hypothesis, Scope statement, Literature bridge, Significance statement |
| **Methods** | Procedure description, Sample/data description, Statistical method, Software/tool reference, Study area description, Quality assurance |
| **Results** | Finding statement, Statistical report, Comparison, Trend description, Reference to figure/table, Pattern description |
| **Discussion** | Interpretation, Comparison with literature, Limitation acknowledgment, Implication, Future direction, Mechanism explanation, Alternative explanation |

---

### 3b. Vocabulary Extraction

Extract **all characteristic verbs, adverbs, adjectives, and nouns** in their actual context.

**Table format:**

| Term | POS | Usage Context | Full Sentence | Source |
|------|-----|---------------|---------------|--------|

**POS tags**: Verb, Adverb, Adjective, Noun

**What counts as "characteristic":**
- Academic register (not everyday vocabulary)
- Section-specific (appears predominantly in one section)
- Field-specific terminology
- Reporting verbs (demonstrate, reveal, suggest, indicate)
- Hedging vocabulary (may, could, likely, approximately)
- Intensifiers/quantifiers (significantly, substantially, markedly)

**Do NOT limit to a fixed number. Extract every characteristic term found.**

---

### 3c. Transitions & Connectors

Extract **every transition word/phrase** with surrounding context.

**Table format:**

| Transition | Category | Full Sentence | Position | Source |
|------------|----------|---------------|----------|--------|

**Categories:**
- **Cause/Effect**: because, therefore, thus, consequently, as a result, hence, due to
- **Contrast**: however, nevertheless, in contrast, whereas, although, despite, on the other hand
- **Addition**: furthermore, moreover, in addition, additionally, also, similarly
- **Example**: for example, for instance, such as, specifically, in particular
- **Sequence**: first, subsequently, then, finally, following, prior to
- **Summary/Conclusion**: in summary, overall, taken together, collectively, in conclusion
- **Concession**: although, while, despite, notwithstanding, albeit
- **Comparison**: compared to, relative to, consistent with, in agreement with, similar to

**Position tags**: Sentence-initial / Mid-sentence / Clause-initial

---

### 3d. Hedging & Stance Markers

Extract **every hedging expression and stance marker**.

**Table format:**

| Expression | Type | Strength | Full Sentence | Source |
|------------|------|----------|---------------|--------|

**Types and strength:**

| Type | Strength levels | Examples |
|------|----------------|---------|
| **Modal hedge** | Weak: may, might, could | "This may indicate..." |
| **Epistemic hedge** | Medium: appears, seems, suggests | "It appears that..." |
| **Probability marker** | Medium: likely, probably, possibly | "...is likely due to..." |
| **Approximator** | Weak: approximately, roughly, about | "...approximately 30%..." |
| **Assertive stance** | Strong: demonstrate, show, reveal, confirm | "Our results demonstrate..." |
| **Tentative stance** | Medium: suggest, indicate, imply | "These findings suggest..." |
| **Attribution shield** | Medium: according to, based on | "According to Smith (2020)..." |

---

### 3e. Quantitative Expressions & Statistical Reporting

Extract **every instance** of numerical/statistical reporting.

**Table format:**

| Expression | Type | Full Sentence | Source |
|------------|------|---------------|--------|

**Types:**
- **Metric report**: FST = 0.46, R² = 0.85
- **Significance test**: P < 0.001, P = 0.03
- **Sample size**: N = 180, n = 30
- **Measurement + uncertainty**: 8.8 ± 0.9 days, 25.3 ± 2.1 mg/L
- **Percentage**: 45%, 12.3%
- **Ratio/proportion**: 3:1, two-thirds
- **Range**: 0.1–0.5, between 10 and 50
- **Comparison statistic**: 2.5-fold increase, three times higher
- **Correlation**: r = 0.78, rho = 0.65

---

### 3f. Citation Integration Patterns

Extract **every citation** and classify integration style.

**Table format:**

| Pattern | Type | Full Sentence | Source |
|---------|------|---------------|--------|

**Types:**
- **Integral (author-prominent)**: "Smith et al. (2020) demonstrated that..."
- **Non-integral (information-prominent)**: "Previous studies have shown that... (Smith et al., 2020)"
- **Parenthetical cluster**: "(1–3)", "(reviewed in (12))"
- **Comparative citation**: "Unlike Smith (2020), our study..."
- **Self-citation**: "In our previous work (Author, Year), we..."
- **Methodological citation**: "...following the protocol of Smith (2020)"
- **Supporting cluster**: "...has been widely reported (A, 2019; B, 2020; C, 2021)"

---

## PHASE 4: Cross-Section Comparison

After completing the extraction loop, produce a comparison matrix.

### Feature × Section Matrix

| Feature | Introduction | Methods | Results | Discussion |
|---------|-------------|---------|---------|------------|
| Dominant tense | | | | |
| Active:Passive ratio | | | | |
| Avg sentence length | | | | |
| Dominant structure | | | | |
| Hedging density | | | | |
| Citation density | | | | |
| Top 3 transitions | | | | |
| Dominant function | | | | |

### Section-specific Vocabulary
Terms that appear **exclusively or predominantly** in one section:

| Section | Exclusive/Dominant terms |
|---------|------------------------|
| Introduction | |
| Methods | |
| Results | |
| Discussion | |

### Top 3 Most Distinctive Cross-section Shifts
1. [Feature]: [How it changes from section to section]
2. [Feature]: [How it changes]
3. [Feature]: [How it changes]

---

## PHASE 5: Style Rules & Templates

### 5a. Do / Don't Rules (per section)

| Section | Do | Don't |
|---------|----|-------|
| Introduction | [derived from data] | [derived from data] |
| Methods | | |
| Results | | |
| Discussion | | |

**Each rule must cite a specific extracted example as evidence.**

### 5b. Sentence Templates (per section, minimum 5 each)

Derive reusable sentence frames from extracted patterns. Use `[SLOT]` markers.

**Format:**
```
[Section] Template: "[Frame with SLOT markers]"
  Based on: "[Original sentence from extraction]" [Source]
```

### 5c. Substitution Dictionary

| Generic | Scientific | Section | Usage Note |
|---------|-----------|---------|------------|
| | | | |

**Each substitution must be grounded in actual extracted examples.**

---

## PHASE 6: Save & Output

### File Structure
```
Style_{주제}/
├── index.md
├── {저자}{연도}_style.md       ← 마크다운 데이터뱅크
├── {저자}{연도}_style.json     ← JSON 데이터뱅크
└── cross_section_matrix.md     ← 섹션 간 비교
```

### JSON Data Bank Schema

```json
{
  "$schema": "style-data-bank-v1.0",
  "meta": {
    "title": "",
    "authors": "",
    "journal": "",
    "year": 0,
    "field": "",
    "extracted_by": "Meta_researcher/meta-styling",
    "extracted_date": ""
  },
  "sections": {
    "introduction": {
      "overview": {
        "dominant_tense": "",
        "dominant_voice": "",
        "active_passive_ratio": "",
        "dominant_person": "",
        "avg_sentence_length": 0,
        "hedging_density": "",
        "citation_density": ""
      },
      "sentence_patterns": [
        {
          "text": "",
          "length": 0,
          "structure": "",
          "tense": "",
          "voice": "",
          "function": "",
          "source": ""
        }
      ],
      "vocabulary": [
        {
          "term": "",
          "pos": "",
          "usage_context": "",
          "sentence": "",
          "source": ""
        }
      ],
      "transitions": [
        {
          "term": "",
          "category": "",
          "sentence": "",
          "position": "",
          "source": ""
        }
      ],
      "hedging": [
        {
          "expression": "",
          "type": "",
          "strength": "",
          "sentence": "",
          "source": ""
        }
      ],
      "quantitative": [
        {
          "expression": "",
          "type": "",
          "sentence": "",
          "source": ""
        }
      ],
      "citations": [
        {
          "pattern": "",
          "type": "",
          "sentence": "",
          "source": ""
        }
      ],
      "templates": []
    },
    "methods": { "...same structure..." },
    "results": { "...same structure..." },
    "discussion": { "...same structure..." }
  },
  "cross_section": {
    "tense_shift": {},
    "voice_ratio": {},
    "hedging_density": {},
    "citation_density": {},
    "distinctive_shifts": []
  },
  "style_rules": {
    "do_dont": {
      "introduction": { "do": [], "dont": [] },
      "methods": { "do": [], "dont": [] },
      "results": { "do": [], "dont": [] },
      "discussion": { "do": [], "dont": [] }
    },
    "substitutions": [
      {
        "generic": "",
        "scientific": "",
        "section": "",
        "usage_note": ""
      }
    ]
  }
}
```

### Validation Checklist (Phase 6)

Before saving, verify:
- [ ] Every extracted item has `[EX#N-SECTION]` source tag
- [ ] All 4 sections have extraction data (or noted as "Not available")
- [ ] No category is empty without explanation
- [ ] Templates are derived from actual extracted patterns
- [ ] Cross-section comparison table is complete
- [ ] JSON is valid and parseable
- [ ] Substitution dictionary includes section-specific usage notes

---

**Template Version**: 1.0.0
