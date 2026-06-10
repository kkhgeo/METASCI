---
name: extraction-knowledge
description: |
  Extract core knowledge from paper PDFs and save as structured markdown.
  Classify into 5 epistemological categories (Theory, Empirical, Methodology, Context, Critique).
  Supports parallel processing via Subagent. Automatically invoked on requests like
  "논문 분석", "지식 추출", "Knowledge 저장".
  **Must follow the format in references/extraction_template.md!**
allowed-tools: [Read, Write, Edit, Bash, Task]
---

> **Warning — Mandatory**: Before executing this skill, you MUST read `references/extraction_template.md` and strictly follow its format (Phase 1~5).

# Knowledge Extraction Skill

## Overview

Extract citation-based Knowledge Units from paper PDFs and save them as
structured markdown files in topic-specific Knowledge folders.

## Usage Triggers

This skill is automatically invoked on the following requests:
- "이 논문 분석해줘"
- "Knowledge 폴더에 저장해줘"
- "논문에서 지식 추출해줘"
- "papers 폴더의 PDF 처리해줘"

## Workflow

**Warning — Important: You MUST read `references/extraction_template.md` first and follow its format!**

```
0. Load Template (Mandatory!)
   - Read references/extraction_template.md
   - Confirm Phase 1~5 structure
   - Familiarize with the output format

1. Input Verification (Phase 1)
   - PDF file path
   - Target sections (entire paper if unspecified)
   - Knowledge folder name for saving

2. Read Paper + Summarize (Phase 2)
   - Claude reads the PDF directly
   - Identify section-level structure
   - Write Paper Information and Research Summary

3. Knowledge Extraction (Phase 3) — 5 Categories
   - Theoretical Foundations
   - Empirical Precedents
   - Methodological Heritage
   - Contextual Knowledge
   - Critical Discourse

   **Table format is mandatory for each category:**
   | Knowledge Claim | 한국어 번역 | Citation Context | Reference (APA) | Section |

4. Extraction Summary (Phase 4)
   - Knowledge distribution statistics
   - Citation count, median citation year

5. Research Question Generation (Phase 5)
   - Level 1: Sentence-level questions
   - Level 2: Paragraph-level questions
   - Level 3: Research-level questions

6. Save as Markdown
   - Save to Knowledge_{topic}/ folder
   - Filename: {Author}{Year}.md (e.g., Chen2024.md)
   - Automatically update index.md
```

### How to Reference the Template

```
# When running in a Subagent or new session:
1. First read this SKILL.md
2. Read references/extraction_template.md
3. Follow the template's Phase 1~5 structure exactly for output
```

## Output Structure

### Folder Structure
```
Knowledge_{topic}/
├── index.md              # Paper list (auto-generated/updated)
├── Chen2024.md           # Individual paper knowledge
├── Kim2023.md
└── Park2022.md
```

### Individual Paper File Structure

```markdown
# {Author} et al. ({Year}) - {Short Title}

## A. Paper Information
- **Title**:
- **Authors**:
- **Year**:
- **Journal**:
- **DOI**:
- **Full Citation (APA 7th)**:

## B. Research Summary
### Research Objective
[Write in Korean]

### Key Findings
1. [Primary finding]
2. [Secondary finding]

### Major Contributions
- **Theoretical contribution**:
- **Empirical contribution**:
- **Methodological contribution**:

## C. Knowledge Extraction

### 1. THEORETICAL FOUNDATIONS
Core theories, conceptual frameworks, hypotheses, and models cited in this paper.

| Knowledge Claim | 한국어 번역 | Citation Context | Reference (APA) | Section |
|-----------------|-------------|------------------|-----------------|---------|
| [content] | [translation] | [context] | [citation] | [location] |

**References:**
- [Full APA citations]

### 2. EMPIRICAL PRECEDENTS
Data, measurements, observations, and experimental results from prior studies.

| Knowledge Claim | 한국어 번역 | Citation Context | Reference (APA) | Section |
|-----------------|-------------|------------------|-----------------|---------|
| [content] | [translation] | [context] | [citation] | [location] |

**References:**
- [Full APA citations]

### 3. METHODOLOGICAL HERITAGE
Research methods, analytical techniques, measurement tools, and experimental protocols.

| Knowledge Claim | 한국어 번역 | Citation Context | Reference (APA) | Section |
|-----------------|-------------|------------------|-----------------|---------|
| [content] | [translation] | [context] | [citation] | [location] |

**References:**
- [Full APA citations]

### 4. CONTEXTUAL KNOWLEDGE
Geographic, temporal, policy, and social context information of the research.

| Knowledge Claim | 한국어 번역 | Citation Context | Reference (APA) | Section |
|-----------------|-------------|------------------|-----------------|---------|
| [content] | [translation] | [context] | [citation] | [location] |

**References:**
- [Full APA citations]

### 5. CRITICAL DISCOURSE
Academic debates, conflicting findings, acknowledged limitations, and unresolved issues.

| Knowledge Claim | 한국어 번역 | Citation Context | Reference (APA) | Section |
|-----------------|-------------|------------------|-----------------|---------|
| [content] | [translation] | [context] | [citation] | [location] |

**References:**
- [Full APA citations]

## D. Extraction Summary
- **Processing date**:
- **Knowledge distribution**: Theory (X%) | Empirical (X%) | Method (X%) | Context (X%) | Discourse (X%)
- **Total citations**:
- **Median citation year**:

## E. Generated Research Questions

### Level 1: Sentence-level Questions
1. [question]
2. [question]

### Level 2: Paragraph-level Questions
1. [question]
2. [question]

### Level 3: Research-level Questions
1. [question]

## F. My Notes
[Space for the user to add notes later]

---
**Keywords**: #keyword1 #keyword2 #keyword3
**Extracted by**: Meta_researcher / extraction-knowledge
**Last Updated**: {date}
```

## Automatic index.md Update

When a new paper is added, append to index.md in the following format:

```markdown
# Knowledge Index: {topic}

## Paper List

| Author | Year | Title | Journal | Keywords | File |
|--------|------|-------|---------|----------|------|
| Chen et al. | 2024 | [title] | GCA | isotopes, groundwater | [link](Chen2024.md) |
| Kim et al. | 2023 | [title] | EPSL | ... | [link](Kim2023.md) |

## Statistics
- Total papers: N
- Last added: {date}
- Key keywords: ...
```

## Parallel Processing (Subagent)

When processing multiple PDFs:

```
User: "papers 폴더의 모든 PDF를 Knowledge_동위원소에 저장해줘"

Execution:
1. Scan papers/ folder -> identify PDF list
2. Create a Task (Subagent) for each PDF
3. Each Subagent independently extracts knowledge
4. Save results to Knowledge_{topic}/ folder
5. Consolidate and update index.md
```

## Quality Criteria

1. **Accuracy**: All citations must be verbatim from the source
2. **Completeness**: Capture all claims that have citations
3. **Consistency**: Maintain uniform classification criteria
4. **Traceability**: Every knowledge unit must indicate its source location

## Error Handling

- PDF not found -> Abort immediately, request the file
- Section unclear -> Confirm whether to analyze the entire paper
- Save folder missing -> Confirm whether to create the folder

## Geochemistry-Specific Fields (Optional)

For geochemistry papers, extract additional information:
- Isotope data ranges (e.g., delta-18O, 87Sr/86Sr)
- Sample types and counts
- Analytical instruments (MC-ICP-MS, TIMS, etc.)
- Reference materials used
- Analytical precision (2-sigma)

## Usage Examples

```
# Single paper
> "Chen2024.pdf를 읽고 Knowledge_동위원소에 저장해줘"

# Specific section only
> "이 논문의 Introduction만 분석해줘"

# Multiple papers (parallel)
> "papers 폴더의 모든 PDF를 Knowledge_환경모니터링에 저장해줘"

# Update existing Knowledge
> "새 논문 Park2024.pdf를 기존 Knowledge에 추가해줘"
```
