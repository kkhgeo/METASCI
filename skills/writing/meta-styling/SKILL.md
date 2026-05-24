---
name: meta-styling
description: |
  Build a data bank by exhaustively extracting sentence/vocabulary/expression patterns per IMRaD section from reference papers (Mode A),
  and revise user drafts based on the data bank for style correction (Mode B).
  Trigger when: "스타일 추출", "톤 분석", "문체 교정", "스타일 맞춰줘" requests.
  **Always read references/extraction_template.md or revision_guide.md first!**
allowed-tools: [Read, Write, Edit, Bash, Task, Glob, Grep]
---

> **Prerequisite**: This skill operates in two modes.
> - **Mode A (Extraction)**: Read `references/extraction_template.md` first
> - **Mode B (Revision)**: Read `references/revision_guide.md` first

# Meta-Styling Skill

## Overview

A skill that **extracts writing style per section** from academic papers and **revises user drafts** based on the extracted data.

**Core Principle: The goal is not scoring — it is collecting as many actual sentences, vocabulary items, and expressions as possible.**

### 2-Mode Structure

```
Mode A: Style Extraction
  Reference papers → Build per-IMRaD-section data bank → Save to Style_{topic}/

Mode B: Style Revision
  User draft + Data bank → Per-section style matching → Output revised text
```

---

## Usage Triggers

### Mode A (Extraction)
- "이 논문 스타일 추출해줘"
- "톤 분석해줘"
- "스타일 데이터뱅크 만들어줘"
- "문체 패턴 추출해줘"
- "Science Advances 스타일 분석해줘"

### Mode B (Revision)
- "이 글 스타일 맞춰줘"
- "문체 교정해줘"
- "스타일 데이터뱅크 기반으로 수정해줘"
- "Introduction 톤 맞춰줘"
- "이 단락 고져줘" (+ data bank path)

---

## Mode A: Style Extraction

### Input Requirements

**Required:**
1. Reference paper text (PDF or text)
2. Text must have **section tags**: `[INTRO]`, `[METHODS]`, `[RESULTS]`, `[DISCUSSION]`

**Optional:**
- Journal name, field
- Specific categories of interest (e.g., hedging-focused, statistical reporting-focused)
- Mode: Detailed (default) / Lite

### Workflow

**Always read `references/extraction_template.md` first and follow it!**

```
Phase 0: Load Template
  → Read references/extraction_template.md

Phase 1: Input Validation (Sanity Check)
  → Check for section tag presence
  → Validate text length
  → Handle warnings

Phase 2: Section Classification & Overview
  → Identify tense/voice/person/purpose for each section

Phase 3: Per-Section Extraction Loop (Core)
  → For each of Introduction / Methods / Results / Discussion:
    3a. Sentence Patterns (exhaustive collection)
    3b. Vocabulary (exhaustive collection of distinctive expressions)
    3c. Transitions & Connectors (exhaustive collection)
    3d. Hedging & Stance Markers (exhaustive collection)
    3e. Quantitative Expressions (exhaustive collection)
    3f. Citation Integration Patterns (exhaustive collection)

Phase 4: Cross-Section Comparison
  → Change matrix for tense/voice/hedging density/citation density

Phase 5: Style Rule Derivation
  → Per-section Do/Don't
  → Per-section Sentence Templates
  → Substitution Dictionary

Phase 6: Save
  → Save to Style_{topic}/ folder
  → Include JSON data bank
```

### Output Structure (Mode A)

```
Style_{topic}/
├── index.md                    # List of analyzed papers
├── {Author}{Year}_style.md     # Individual paper style data bank
├── {Author}{Year}_style.json   # JSON data bank (for LLM reference)
└── cross_section_matrix.md     # Cross-section comparison matrix
```

### Individual Data Bank File Structure

```markdown
# Style Data Bank: {Author} et al. ({Year})

## A. Paper Information
- **Title**:
- **Journal**:
- **Year**:
- **Field**:

## B. Section Overview
| Feature | Introduction | Methods | Results | Discussion |
|---------|-------------|---------|---------|------------|
| Tense | | | | |
| Voice | | | | |
| Person | | | | |
| Hedging density | | | | |

## C. Introduction Data Bank
### Sentence Patterns
| # | Sentence | Length | Structure | Tense | Voice | Function | Source |
### Vocabulary
| Term | POS | Usage Context | Full Sentence | Source |
### Transitions
| Transition | Category | Full Sentence | Position | Source |
### Hedging & Stance
| Expression | Type | Strength | Full Sentence | Source |
### Quantitative Expressions
| Expression | Type | Full Sentence | Source |
### Citation Patterns
| Pattern | Type | Full Sentence | Source |

## D. Methods Data Bank
[Same structure repeated]

## E. Results Data Bank
[Same structure repeated]

## F. Discussion Data Bank
[Same structure repeated]

## G. Style Rules
### Do / Don't (per section)
### Sentence Templates (5+ per section)
### Substitution Dictionary

---
**Extracted by**: Meta_researcher / meta-styling (Mode A)
**Last Updated**: {date}
```

---

## Mode B: Style Revision

### Input Requirements

**Required:**
1. Text to revise (section, paragraph, or sentence)
2. **Section type** of the text (Introduction / Methods / Results / Discussion)
3. **Style data bank path** to reference (Style_{topic}/ folder)

**Optional:**
- Revision intensity: Light (expressions only) / Standard (structure + expressions) / Deep (full rewrite)
- Specific category focus: hedging, transitions, sentence structure, etc.

### Workflow

**Always read `references/revision_guide.md` first and follow it!**

```
Phase 0: Load Template
  → Read references/revision_guide.md

Phase 1: Input Analysis
  → Confirm section type of user text
  → Load data bank (for the relevant section)
  → Confirm revision intensity

Phase 2: Diagnosis
  → Compare user text against data bank:
    2a. Sentence Structure comparison
    2b. Vocabulary comparison
    2c. Transitions comparison
    2d. Hedging/Stance comparison
    2e. Quantitative Reporting comparison
    2f. Citation Style comparison
  → List mismatches per category

Phase 3: Prescription
  → Specific revision suggestions per mismatch item
  → Cite reference examples from data bank
  → Explain rationale for each revision

Phase 4: Revision Execution
  → Generate revised text (in English)
  → Highlight changes
  → Before/After comparison

Phase 5: Verification
  → Re-check that revised text matches data bank patterns
  → Generate revision report
```

### Output Format (Mode B)

```markdown
## Style Revision Report

### A. Diagnosis Summary
| Category | Match Rate | Key Mismatches | Revisions Needed |
|----------|-----------|----------------|-----------------|
| Sentence Structure | 60% | Sentences too short | 3 places |
| Vocabulary | 70% | Non-academic verb usage | 5 places |
| Transitions | 40% | Insufficient transition words | 4 places |
| Hedging | 50% | Excessive assertions | 6 places |

### B. Detailed Diagnosis & Prescription

#### [Revision 1] Sentence Structure
- **Original**: "We tested the samples."
- **Issue**: Too short and simple. Mismatches Methods section patterns.
- **Reference**: "Samples were analyzed using [method] following [protocol] (ref)." [EX#1-METHODS]
- **Revised**: "The collected samples were analyzed using ICP-MS following the protocol established by Smith et al. (2020)."

#### [Revision 2] Hedging
- **Original**: "This proves that..."
- **Issue**: Overclaim in Discussion. Data bank patterns use hedging.
- **Reference**: "Our findings suggest that..." [EX#1-DISCUSSION]
- **Revised**: "These results suggest that..."

[...all revision items...]

### C. Revised Text

**[Before]**
Original text

**[After]**
Revised text (changes shown in **bold**)

### D. Change Summary
- Total revisions: N places
- Sentence Structure: N places
- Vocabulary: N places
- Transitions: N places
- Hedging: N places
- Style match rate after revision: X% → Y%

---
**Revised by**: Meta_researcher / meta-styling (Mode B)
```

---

## Linking the Two Modes

```
┌──────────────────────────────────────────────────────────────────┐
│  Mode A: Reference papers → Style extraction → Save to Style_{topic}/  │
│                                                  │                      │
│                                                  ▼                      │
│  Mode B: User draft + Style_{topic}/ → Style revision                  │
└──────────────────────────────────────────────────────────────────┘
```

**Typical Workflow:**
1. Run Mode A on 2–3 papers from the target journal → Build data bank
2. Run Mode B on each section of your draft → Style revision
3. If needed, reinforce with additional papers via Mode A → Re-run Mode B

---

## Parallel Processing (Subagent)

### Mode A Parallel
Extract from multiple papers simultaneously:
```
사용자: "이 3개 논문 스타일 추출해줘"
→ Create a Task (Subagent) for each paper
→ Each Subagent extracts independently
→ Results saved collectively to Style_{topic}/ folder
```

### Mode B Parallel
Revise multiple sections simultaneously:
```
사용자: "Introduction과 Discussion 교정해줘"
→ Create a Task (Subagent) for each section
→ Each Subagent references the relevant section data bank for revision
```

---

## Quality Criteria

### Mode A
1. **Completeness**: Collect all distinctive expressions without omission
2. **Accuracy**: Quote original text verbatim; section tags must be correct
3. **Structure**: All 24 tables (6 categories × 4 sections) must be filled
4. **Traceability**: Every example must have an `[EX#N-SECTION]` source tag

### Mode B
1. **Evidence-based**: Every revision must include a reference example from the data bank
2. **Content preservation**: Do not alter the academic content of the original (style changes only)
3. **Explainability**: State why each revision was made
4. **Comparability**: Provide clear Before/After contrast

---

## Error Handling

| Situation | Response |
|-----------|----------|
| No section tags (Mode A) | Request tagging or attempt auto-classification + warning |
| Text too short (<500w) | Warning: "Extraction results may be thin" |
| No data bank found (Mode B) | Guide user to run Mode A first |
| Section type mismatch | Request confirmation of the correct section |
| Only 1 reference paper provided | Warning: "Single-paper pattern; limited generalizability" |

---

## Usage Examples

### Mode A Examples
```
# Single paper extraction
> "이 논문 스타일 추출해서 Style_생태학에 저장해줘"

# Multiple papers (parallel)
> "papers 폴더의 논문 3편 스타일 추출해줘"

# Specific category focus
> "이 논문에서 hedging 패턴만 추출해줘"
```

### Mode B Examples
```
# Paragraph revision
> "이 Introduction 단락을 Style_생태학 기반으로 교정해줘"

# Full section revision
> "Discussion 전체를 Science Advances 스타일로 맞춰줘"

# Light revision
> "이 문장들만 톤 맞춰줘 (Light 모드)"
```

### Combined Usage
```
# Step 1: Extraction
> "Weber2021.pdf 스타일 추출해서 Style_진화생물학에 저장해줘"

# Step 2: Revision
> "내가 쓴 Introduction을 Style_진화생물학 기반으로 교정해줘"
```

---

**Version**: 1.0.0
**Extracted by**: Meta_researcher / meta-styling
