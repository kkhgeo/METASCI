---
name: meta-writing
description: |
  Multi-source academic paper section writing skill.
  Clearly separates original research data (My Data: figures, tables, data files) from
  prior literature knowledge (Knowledge, PDF, Web) to perform IMRaD section-specific writing.
  Uses a 5-Loop process: source exploration -> data analysis -> gap filling -> writing -> verification,
  with bilingual (English + Korean) output and APA 7 citations.
  Trigger phrases: "글쓰기", "섹션 작성", "선행연구 정리", "Results 써줘", "Discussion 작성",
  "이 그림 기반으로 써줘", "Knowledge 기반으로 글써줘", "Figure 해석해줘" — activate this skill upon these requests.
allowed-tools: [Read, Write, Edit, Glob, Task, Agent, WebSearch, WebFetch]
---

# Meta Writing Skill

## Overview

Combines original research data (My Data) with prior literature knowledge (Knowledge Sources)
to write academic paper sections.

**Two types of information are clearly distinguished:**

| Category | My Data (Original Research) | Knowledge Sources (Prior Literature) |
|----------|---------------------------|--------------------------------------|
| Identity | Data produced by the researcher | Knowledge drawn from prior studies |
| Examples | Figure, Table, CSV | Knowledge MD, PDF, Web |
| Role in text | Subject of description/interpretation | Basis for comparison/evidence |
| Results | "This study showed ~ (Figure 1)" | "Similar to (Chen et al., 2024)" |
| Discussion | "The observed pattern suggests ~" | "Explained by Chen (2024)'s model" |

**Knowledge Sources Priority:**
1. Knowledge folder (markdown) — Already structured knowledge, always first priority
2. PDF folder — Supplements papers not covered by Knowledge
3. Web search — Latest information or gap filling

---

## Project Settings Load

Before starting, search for `writing.local.md` in the current directory.

- **If found**: Load settings and present a summary to the user for confirmation.
- **If not found**: Guide the user to copy `writing.local.template.md` to create `writing.local.md`. If the user declines, ask for source paths directly.
- **If the user explicitly specifies paths**: These take priority over writing.local.md.

---

## Input Parsing (Phase 1)

Analyze the user request to determine the items below.
After parsing, confirm with the user before proceeding.

```xml
<task_spec>
Core topic: [topic]
Section: [Introduction/Methods/Results/Discussion]
Scope: [full section/specific part]
Focus: [perspective/objective]
Request type: [topic/figure/table]

My Data:
  figures: [file path list, section placement]
  tables: [file path list, section placement]
  data_files: [file path list]

Knowledge Sources:
  knowledge_folder: [path or "none"]
  pdf_folder: [path or "none"]
  web_search: [allowed/not allowed]

Settings:
  min_citations: [number, default 5]
  paragraphs: [1-3, default 2]
  words_per_paragraph: [150-250]
  citation_style: APA 7
  language: [bilingual/english/korean]
</task_spec>
```

### Section Reference

| Section | Content | My Data Role | Knowledge Role |
|---------|---------|-------------|----------------|
| Introduction | Background, prior research, gap, objectives | Minimal | Primary (synthesis of prior research) |
| Methods | Methods, techniques, samples | Sample/instrument information | Methodology references/citations |
| Results | Data presentation, comparison | **Primary** (subject of description) | Comparison target |
| Discussion | Interpretation, implications, limitations | **Primary** (subject of interpretation) | Basis for interpretation |

---

## Knowledge Exploration and Analysis (Phase 2)

Explore and analyze sources using the 5-Loop process.

> **Detailed procedure**: Read and follow the Loop 1-4 sections of `references/writing_template.md`.

### Loop Summary

```
Loop 1: Source Scan and Planning
  - Load writing.local.md (if available)
  - Check My Data folder (list figures/tables/data)
  - Check Knowledge folder (index.md, select relevant files)
  - Check PDF folder
  - Establish exploration plan

Loop 2: Knowledge Reading
  - Read selected Knowledge markdown files (up to 5)
  - Extract Claim + Citation pairs
  - Intermediate Result A

Loop 3: My Data Analysis + Additional Sources
  - Analyze My Data figures/tables (extract patterns, values)
  - Generate comparison pairs between My Data and Knowledge
  - Read additional Knowledge/PDF files
  - Intermediate Result B

Loop 4: Gap Check + Web Search
  - Verify citation count, topic coverage, recent research, comparison data
  - If insufficient, supplement with Web search (if allowed)
  - Intermediate Result C + Gap Report
```

### Gap Check Criteria

| Gap Type | Judgment Criteria | Response |
|----------|------------------|----------|
| Insufficient citations | Below minimum citation count | Additional PDF/Web search |
| Insufficient comparison data | No prior studies matching My Data patterns | Web search |
| Insufficient recent research | No studies after 2023 | Web search |
| Insufficient interpretation basis | No theories/mechanisms to cite in Discussion | PDF/Web search |

---

## Writing (Phase 3)

> **5-Loop details**: Follow the Loop 5 section of `references/writing_template.md`.
> **Section-specific structure, transitions, examples**: Read the corresponding section in `references/section_guides.md`.

### Core Rules

**My Data vs Knowledge Distinction Principle:**
- My Data is described directly without citations. Reference as "(Figure 1)", "(Table 2)".
- Knowledge Sources must always be cited in (Author, Year) format.
- When mixing My Data and Knowledge in a single sentence, clearly indicate which is original research and which is prior literature.

**Paragraph Writing Rules:**
1. Topic sentence: Begin with the central claim
2. Evidence: Support with at least 3 citations (Knowledge Sources)
3. Transitions: Use natural connectors (refer to section_guides.md)
4. Concluding sentence: State implications or connect to the next paragraph
5. Source diversity: Mix different source types when possible

**Bilingual Output:**
- English first, followed by Korean translation
- Maintain consistency of academic terminology
- Keep (Author, Year) citations in English even in Korean text

---

## Verification (Phase 4)

> **Detailed procedure**: Read and follow `references/citation-and-verification.md` in its entirety.

### Verification Summary

```
Step 1: Citation-Reference matching (in-text citations <-> References)
Step 2: APA 7 format verification (required fields, formatting)
Step 3: Source-specific verification (Knowledge original cross-check, PDF metadata, Web URL)
Step 4: Generate verification report (including Quality Score)
```

### Verification Checklist
- [ ] All in-text citations exist in References
- [ ] No orphan references
- [ ] APA 7 format compliance
- [ ] My Data references (Figure/Table) match actual files
- [ ] No fabrication of DOI/URL/year/author

---

## Output Format

> **Detailed template**: Refer to the "Output Format Details" section in `references/writing_template.md`.

All output consists of the following 6 sections:

| Section | Content |
|---------|---------|
| A) Approach Checklist | 3-8 step task summary (English + Korean) |
| B) Source Summary | Summary by source type + gap report |
| C) Main Text | English paragraphs + Korean translation |
| D) References | APA 7, organized by source type |
| E) Self-Assessment | Quality checklist |
| F) Verification Report | Reference verification report |

---

## Parallel Processing (Subagent)

소스가 많을 때 Loop 2-4를 병렬로 실행하여 속도를 높인다.

### 병렬 가능 작업

| 작업 | 병렬화 | 방법 |
|------|--------|------|
| Knowledge 파일 여러 개 읽기 | Yes | 파일당 Subagent 동시 실행 |
| PDF 여러 개 읽기 | Yes | 파일당 Subagent 동시 실행 |
| My Data 분석 (Figure + Table) | Yes | 유형별 Subagent 동시 실행 |
| Web 검색 (쿼리 여러 개) | Yes | 쿼리당 Subagent 동시 실행 |
| 글쓰기 (Loop 5) | No | 소스 통합 후 순차 |
| 검증 (Phase 4) | No | 글쓰기 결과 의존 |

### 병렬 실행 조건

- Knowledge 파일 3개 이상 → 병렬 읽기 권장
- PDF 2개 이상 → 병렬 읽기 권장
- Figure + Table 동시 존재 → 병렬 분석 권장
- 소스 1-2개 → 순차 실행 (오버헤드 불필요)

### Subagent Prompt Template (Knowledge Reading)

```
당신은 학술 Knowledge 파일 분석 전문가입니다.

다음 Knowledge 마크다운 파일에서 주제 "[topic]"과 관련된
Claim + Citation 쌍을 추출하세요.

카테고리 분류:
- Theoretical Foundations
- Empirical Precedents
- Methodological Heritage
- Contextual Knowledge
- Critical Discourse

파일:
[파일 내용 삽입]

출력 형식:
| Claim | Citation | Category | Source |
|-------|----------|----------|--------|
```

---

## Constraints

### Citation Strictness
- Absolutely no fabrication of DOI/URL/year/author
- Uncertain fields: Mark as `[missing: field]`
- Web search results must include source and access date

### Quality Standards
- Minimum 3 Knowledge citations per paragraph
- No over-reliance on a single source
- Mix different source types when possible

### My Data Handling
- Do not cite original data as if it were prior literature
- Maintain accurate Figure/Table numbers
- Do not arbitrarily alter data values

---

## References File Guide

| File | When to Reference | Content |
|------|-------------------|---------|
| `references/writing_template.md` | Phase 2-3 | 5-Loop detailed procedure, source-specific handling, output format details |
| `references/section_guides.md` | Phase 3 | IMRaD section-specific structure, transitions, examples, figure/table interpretation |
| `references/citation-and-verification.md` | Phase 4 | Citation formatting, APA 7, verification procedure, report template |

---

**Version**: 1.0.0
