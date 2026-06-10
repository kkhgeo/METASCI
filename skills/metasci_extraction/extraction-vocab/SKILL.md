---
name: extraction-vocab
description: |
  Exhaustively extract ALL content words from academic paper PDFs,
  organized by section and part of speech. Technical/domain terms
  are separately identified and classified.
  Triggers: "단어 추출", "어휘 추출", "용어 추출", "품사별 추출",
  "vocabulary extraction", "term extraction".
  **MUST read references/extraction_template.md before starting!**
allowed-tools: [Read, Write, Edit, Bash, Task, Glob, Grep]
---

> **REQUIRED**: Before executing this skill, ALWAYS read `references/extraction_template.md` first and follow it precisely.

# Vocab Extraction Skill

## Overview

Exhaustively extracts **every content word** from an academic paper, organized by IMRaD section and part of speech (POS). Technical/domain-specific terms are separately flagged and classified.

**Difference from meta-styling**: meta-styling selectively extracts "characteristic" academic vocabulary. extraction-vocab captures **every content word** exhaustively, with special attention to domain terminology.

**Difference from extraction-logic**: extraction-logic focuses on sentence-level frames and argument flow. extraction-vocab focuses on **individual words and multi-word terms** at the lexical level.

---

## Triggers

- "이 논문 단어 추출해줘"
- "어휘 분석해줘"
- "품사별로 단어 뽑아줘"
- "전문용어 추출해줘"
- "용어 목록 만들어줘"
- "extract vocabulary from this paper"

---

## Input Requirements

**Required:**
1. Paper PDF path (or pasted text)

**Optional:**
- Journal name, field (helps technical term identification)
- Specific section only (e.g., Methods only)
- Output folder name

---

## Workflow

**MUST read `references/extraction_template.md` first and follow it!**

```
Phase 1: Read Paper & Section Identification
  → LLM reads the PDF directly (no preprocessing)
  → Identify IMRaD sections (or actual structure)
  → Brief section overview

Phase 2: Exhaustive Word Extraction by POS
  → Extract ALL content words per section
  → Classify by POS: Verb, Noun, Adjective, Adverb
  → Record context sentence and frequency

Phase 3: Technical Term Identification
  → Flag domain-specific terms (single-word and multi-word)
  → Classify term type: domain-specific, methodological, statistical, etc.
  → Build a technical glossary with definitions from context

Phase 4: Cross-Section Vocabulary Analysis
  → Word frequency distribution across sections
  → Section-exclusive vocabulary
  → Technical term density per section

Phase 5: Save
  → Save to Vocab_{topic}/ folder as markdown
```

---

## Output Structure

### Folder Structure
```
Vocab_{topic}/
├── index.md                           # List of analyzed papers
├── {Author}{Year}_vocab.md            # Individual paper vocabulary
└── cross_paper_vocabulary.md           # Cross-paper comparison (when multiple papers)
```

### Individual Paper File Structure

```markdown
# Vocabulary Extraction: {Author} et al. ({Year})

## A. Paper Information
- **Title**:
- **Journal**:
- **Year**:
- **Field**:

## B. Section Overview
| Section | Paragraphs | Sentences | Approx. Word Count |

## C. Vocabulary by Section & POS

### Introduction
#### Verbs
| # | Word | Frequency | Context (example sentence) | Technical | Source |
#### Nouns
[Same format]
#### Adjectives
[Same format]
#### Adverbs
[Same format]

### Methods / Results / Discussion
[Same structure repeated]

## D. Technical Term Glossary
| # | Term | POS | Type | Definition (from context) | Sections Found | Frequency |

## E. Cross-Section Analysis
- Word frequency matrix (top words × sections)
- Section-exclusive words
- Technical term density

## F. Summary Statistics
- Total unique words, POS distribution, technical term ratio

---
**Extracted by**: Meta_researcher / extraction-vocab
**Date**: {date}
```

---

## Parallel Processing (Subagent)

```
User: "Analyze vocabulary of these 3 papers"
→ Create a Task (Subagent) for each paper
→ Each Subagent extracts independently
→ Results saved to Vocab_{topic}/ folder
→ cross_paper_vocabulary.md for shared/unique term comparison
```

---

## Quality Standards

1. **Exhaustiveness**: Every content word captured, no omissions
2. **Accuracy**: Correct POS tagging, correct technical term flagging
3. **Traceability**: Every word linked to at least one context sentence with `[P#-S#]` source
4. **Completeness**: Multi-word technical terms captured as units, not split

---

## Error Handling

| Situation | Response |
|-----------|----------|
| PDF not found | STOP, request file |
| Section structure unclear | Use best judgment + WARN |
| Non-IMRaD structure | Adapt to actual structure |
| Ambiguous POS (e.g., noun/verb) | Tag primary POS, note dual usage |

---

## Usage Examples

```
# Single paper
> "이 논문 단어 추출해서 Vocab_지구화학에 저장해줘"

# Technical terms only
> "이 논문에서 전문용어만 뽑아줘"

# Specific section
> "Methods 섹션 어휘만 추출해줘"

# Multiple papers
> "papers 폴더의 논문 3편 어휘 추출해줘"
```

---

## Integration with Other Skills

```
extraction-vocab → Exhaustive word inventory + technical glossary (WHAT words are used)
meta-styling      → Characteristic expressions + hedging + transitions (HOW words are used)
extraction-logic → Argument structure + sentence frames (HOW sentences are organized)

Combined workflow:
1. extraction-vocab: build complete word inventory and technical glossary
2. extraction-logic: understand argument structure and sentence templates
3. meta-styling: understand stylistic patterns
4. When writing: use glossary (vocab) + structure (logic) + style (meta-styling)
```

---

**Version**: 1.0.0
**Skill**: Meta_researcher / extraction-vocab
