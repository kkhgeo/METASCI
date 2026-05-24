---
name: extraction-logic
description: |
  Systematically extract structure (sections/paragraphs), argument logic
  (inter-paragraph and intra-paragraph), and sentence frames (rhetorical templates)
  from academic paper PDFs. Saves results as structured markdown.
  Triggers: "논리 분석", "구조 분석", "문장 형식 추출", "논문 구조 파악",
  "logic analysis", "structure analysis", "sentence frame extraction".
  **MUST read references/extraction_template.md before starting!**
allowed-tools: [Read, Write, Edit, Bash, Task, Glob, Grep]
---

> **REQUIRED**: Before executing this skill, ALWAYS read `references/extraction_template.md` first and follow it precisely.

# Logic Extraction Skill

## Overview

Extracts three layers of analysis from academic papers:

- **Structure Mapping**: Identify sections and paragraphs, build a hierarchical structure tree
- **Logic Extraction**: Map argument flow between paragraphs (inter-paragraph) and between sentences within paragraphs (intra-paragraph)
- **Sentence Frame Extraction**: Abstract reusable rhetorical templates from every sentence — capturing the **form/shape** of sentences, not specific words

**Difference from meta-styling**: meta-styling extracts *"which words and expressions are used"* (surface). extraction-logic extracts *"how the argument is structured and flows"* (deep).

---

## Triggers

- "이 논문 구조 분석해줘"
- "논리 흐름 추출해줘"
- "문장 형식 분석해줘"
- "단락 구조 파악해줘"
- "논증 구조 분석해줘"
- "sentence frame 추출해줘"
- "analyze the logic structure of this paper"

---

## Input Requirements

**Required:**
1. Paper PDF path (or pasted text)

**Optional:**
- Journal name, field
- Specific section only (e.g., Introduction only)
- Output folder name

---

## Workflow

**MUST read `references/extraction_template.md` first and follow it!**

```
Phase 1: Read Paper & Structure Mapping
  → LLM reads the PDF directly (no preprocessing)
  → Identify sections (IMRaD + subsections)
  → Identify paragraph boundaries and assign numbers
  → Output: Structure tree

Phase 2: Inter-Paragraph Logic Extraction
  → Assign a function tag to each paragraph
  → Classify logical relations between adjacent paragraphs
  → Output: Logic flow diagram per section

Phase 3: Intra-Paragraph Logic Extraction
  → Assign a role tag to each sentence
  → Classify logical relations between adjacent sentences
  → Output: Logic chain per paragraph

Phase 4: Sentence Frame Extraction
  → Extract the rhetorical frame of every sentence
  → Abstract specific content into [SLOT] placeholders
  → Collect ALL frames: reference taxonomy + uncategorized
  → Output: Sentence frame catalog per section

Phase 5: Synthesis & Save
  → Summarize overall logic structure
  → Compare patterns across sections
  → Save to Logic_{topic}/ folder as markdown
```

---

## Output Structure

### Folder Structure
```
Logic_{topic}/
├── index.md                          # List of analyzed papers
├── {Author}{Year}_logic.md           # Individual paper analysis
└── cross_paper_patterns.md           # Cross-paper pattern comparison (when multiple papers)
```

### Individual Paper File Structure

```markdown
# Logic Analysis: {Author} et al. ({Year})

## A. Paper Information
- **Title**:
- **Journal**:
- **Year**:
- **Field**:

## B. Structure Map

### Structure Tree
Section → Subsection → Paragraph hierarchy

### Structure Overview Table
| Section | Subsections | Paragraphs | Total Sentences | Core Function |

## C. Inter-Paragraph Logic

### Introduction
| P# | Function Tag | Summary (first sentence) | → Relation to next | Signal |
Flow diagram: P1[Background] →(However)→ P2[Gap] →(Therefore)→ P3[Purpose]

### Methods / Results / Discussion
[Same structure]

## D. Intra-Paragraph Logic

### Per-paragraph analysis
| S# | Sentence Role | → Relation to next | Original text |
Logic chain: S1[Topic] →(Support)→ S2[Evidence] →(Therefore)→ S3[Claim]

## E. Sentence Frame Catalog

### Per-section frame collection
| # | Frame Type | Abstracted Template | Original Sentence | Source |
Exhaustive collection of ALL sentence forms

## F. Analysis Summary
- Structure statistics
- Logic pattern summary
- Sentence frame distribution

---
**Extracted by**: Meta_researcher / extraction-logic
**Date**: {date}
```

---

## Parallel Processing (Subagent)

Multiple papers analyzed concurrently:
```
User: "Analyze logic structure of these 3 papers"
→ Create a Task (Subagent) for each paper
→ Each Subagent analyzes independently
→ Results saved to Logic_{topic}/ folder
→ cross_paper_patterns.md for pattern comparison
```

---

## Quality Standards

1. **Completeness**: Every paragraph and every sentence analyzed without omission
2. **Accuracy**: Original text quoted verbatim, logical relations correctly classified
3. **Traceability**: Every item tagged with `[P#-S#]` (paragraph number - sentence number)
4. **Comprehensiveness**: Sentence frames are NOT a closed list — collect ALL forms found

---

## Error Handling

| Situation | Response |
|-----------|----------|
| PDF not found | STOP immediately, request file |
| Section structure unclear | LLM uses best judgment + WARN in output |
| Non-IMRaD structure | Adapt to actual structure (Review, Letter, etc.) |
| Ambiguous paragraph boundary | Split by semantic unit + WARN |

---

## Usage Examples

```
# Single paper
> "Weber2021.pdf의 논리 구조 분석해줘"

# Specific section only
> "Analyze the Discussion logic flow of this paper"

# Multiple papers (parallel)
> "papers 폴더의 논문 3편 논리 구조 분석해줘"

# Sentence frames only
> "Extract sentence frames from this paper"
```

---

## Integration with meta-styling

```
extraction-logic → Argument structure + sentence frames (HOW the argument flows)
meta-styling      → Vocabulary + expressions + tense/voice (HOW the words sound)

Combined workflow:
1. extraction-logic: understand argument structure and sentence templates
2. meta-styling: understand lexical and stylistic patterns
3. When writing: reference logic structure (logic) + expression style (style) together
```

---

**Version**: 1.0.0
**Skill**: Meta_researcher / extraction-logic
