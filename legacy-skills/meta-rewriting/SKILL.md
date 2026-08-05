---
name: meta-rewriting
description: |
  Reverse-engineers the writing style of a reference paper (or journal / existing Style databank)
  to generate a Style Blueprint, then applies it to the user's draft in a one-shot End-to-End
  style transfer pipeline.
  Reference source input → Blueprint extraction → Draft receipt → Gap Analysis → Rewriting,
  all completed within a single session.
  Trigger phrases: "이 논문처럼 써줘", "이 저널 스타일로 맞춰줘", "내 초고 리라이팅",
  "스타일 전이", "rewrite in the style of", "match this journal style",
  "write like this paper", "style transfer", "문체 전이", "글투 맞춰줘".
  **You MUST read references/ files at the corresponding Phase!**
allowed-tools: [Read, Write, Edit, Glob, Task, WebSearch, WebFetch]
---

> **REQUIRED**: Before starting each Phase, you MUST read the corresponding reference file.
> - PHASE 2: `references/blueprint-template.md`
> - PHASE 1 (journal name only): `references/journal-styles.md`
> - PHASE 4 & 5: `references/output-formats.md`

# Meta-Rewriting Skill

## Overview

Reverse-engineers the writing style of a reference paper to generate a **Style Blueprint**,
then immediately applies it to the user's draft via a **one-shot style transfer pipeline**.

**Core rule:** Extract only the style from the reference source. Never copy ideas, data, or claims.

### Relationship to Other Skills

| Skill | Role | Difference |
|-------|------|------------|
| `meta-styling Mode A+B` | Deep extraction → permanent databank → manual application (2-step) | meta-rewriting completes in **one shot** without a databank |
| `meta-review` | 4-principle evaluation + improvement based on logic+vocab extractions | meta-rewriting focuses on **reference paper style** transfer |
| `meta-writing` | Knowledge sources → writing from scratch | meta-rewriting performs **rewriting of an existing draft** |

**Combined usage:**
- If an existing databank created by `meta-styling Mode A` is available, it can be used directly instead of generating a Blueprint
- Combining with `meta-review` results enables simultaneous logic + style improvement

---

## Pipeline

```
PHASE 1 → Accept reference source input
PHASE 2 → Extract Style Blueprint → Display to user
PHASE 3 → [AUTO-TRANSITION] Receive user's draft
PHASE 4 → Gap Analysis (Blueprint vs draft)
PHASE 5 → Apply rewriting → Output
```

Auto-transition rule: After displaying the Blueprint card in PHASE 2, immediately transition to
PHASE 3 and request the draft. Do not wait for the user to explicitly ask.

---

## Triggers

### Korean
- "이 논문처럼 써줘"
- "이 저널 스타일로 맞춰줘"
- "내 초고 리라이팅해줘"
- "스타일 전이해줘"
- "문체 전이", "글투 맞춰줘"
- "Nature 스타일로 고쳐줘"
- "이 논문 문체로 다시 써줘"

### English
- "rewrite in the style of [paper/journal]"
- "match this journal style"
- "write like this paper"
- "style transfer"
- "rewrite my draft to match [reference]"

---

## PHASE 1: Accept Reference Input

Detect the input type and route accordingly.

| Input type | Action |
|------------|--------|
| PDF file path/upload | Extract full text → PHASE 2 |
| Text pasted directly | Use as-is → PHASE 2 |
| Journal name only | Load `references/journal-styles.md` → PHASE 2 (Confidence: Low) |
| Paper title/author | Web search to obtain abstract + style info → PHASE 2 |
| Multiple past papers by the user | Analyze each → Merge common patterns → Master Blueprint |
| Existing Style databank path | Load `Style_{topic}/` → Convert to Blueprint → PHASE 2 |

**When only a journal name is provided:**
- If the journal exists in `references/journal-styles.md`, use it
- If not, attempt Web search to collect recent abstracts + style information from that journal
- Mark Confidence as Medium or lower, and recommend providing an actual paper

**Using an existing databank:**
- If a `_style.md` or `_style.json` file exists in the `Style_{topic}/` folder, use it directly
- Map the databank's 6 categories to the Blueprint's 6 dimensions

Detect and proceed without clarifying questions. Only confirm if the input is genuinely ambiguous.

---

## PHASE 2: Extract Style Blueprint

Analyze the reference source across **6 dimensions** to generate a Blueprint card.

**You MUST read `references/blueprint-template.md` first and follow it!**

### 6 Analysis Dimensions

| # | Dimension | Extraction Target |
|---|-----------|-------------------|
| 1 | Tone & Stance | Register, active/passive ratio, hedging frequency & expressions |
| 2 | Sentence Architecture | Average sentence length, complex sentence ratio, syntactic patterns, paragraph size |
| 3 | Logical Flow | Macro argumentation structure, paragraph organization, section transitions, counterargument handling |
| 4 | Transition Expressions | Functional expressions (addition/contrast/causation/emphasis/summary) for connectives & transitions |
| 5 | Vocabulary & Terminology | Domain noun phrases, preferred verbs, nominalization tendency, numerical notation |
| 6 | Citation & Evidence Style | Narrative/parenthetical citation, data reporting format, figure/table referencing |

### Extraction Rules
- For each dimension, quote 2-3 actual sentences from the source text (no abstract descriptions)
- Quantify where possible: average sentence length, passive voice ratio, hedging frequency
- Generate 3-5 reusable fill-in-the-blank templates per dimension

### Output
- Display the Blueprint card to the user (format: see `references/blueprint-template.md`)
- Immediately transition to PHASE 3

---

## PHASE 3: Request User's Draft (AUTO-TRANSITION)

Immediately after displaying the Blueprint card, output the following prompt and wait:

```
---
Style Blueprint complete.

Please paste your text or upload your draft.

  Scope: a single paragraph, a full section, or the entire paper.
  Section type (optional): Introduction / Methods / Results / Discussion / Abstract

  Mode:
    [A] Sentence-level feedback — keep original, suggest targeted edits
    [B] Full rewrite — apply Blueprint style throughout
---
```

Default when Mode is not specified: **[A]**

### Input Parsing

When the user's draft is received:
1. Check text length (word count)
2. Determine section type (explicit or auto-detected)
3. Confirm Mode (A/B)
4. Proceed to PHASE 4

---

## PHASE 4: Gap Analysis

Compare the user's draft against the Blueprint across all 6 dimensions.

**Follow the Gap Analysis card format in `references/output-formats.md`.**

### Analysis Procedure
1. Diagnose the current state of the draft for each dimension
2. Identify discrepancies from the Blueprint standard
3. Score each dimension 1-10
4. Prioritize the lowest-scoring dimensions for PHASE 5

### Scoring Guide

| Score | Meaning | Recommended Mode |
|-------|---------|------------------|
| 8-10 | Well aligned with Blueprint | Mode A (targeted edits) |
| 5-7 | Noticeable gaps, targeted edits sufficient | Mode A |
| 1-4 | Large differences, full rewrite recommended | Mode B (full rewrite) |

Overall 7 or above → suggest Mode A; Overall below 7 → suggest Mode B.
If the user has already selected a Mode, proceed with that choice.

---

## PHASE 5: Apply Improvements

**Follow the Mode A / Mode B format in `references/output-formats.md`.**

### Mode A — Sentence-Level Feedback

Process the draft paragraph by paragraph. For each problematic sentence:

```
[ORIGINAL] "Original text as-is"
[REVISION] "Revised version"
[RATIONALE] Which Blueprint rule was applied, in 1-2 lines
```

- For well-written sentences, briefly acknowledge and move on
- Do not rewrite sentences that need no revision
- Prioritize dimensions with the lowest scores

### Mode B — Full Rewrite

Rewrite the entire input. Apply all 6 Blueprint dimensions.

**Preservation principles:**
- Preserve all claims, data, and citations from the original — only transform the style
- Maintain Figure/Table reference numbers
- Never alter scientific meaning

After rewriting, attach a Change Summary table (format: see `references/output-formats.md`).

---

## Output Structure

All outputs are saved to the `Rewrite_{topic}/` folder.

```
Rewrite_{topic}/
├── blueprint.md          # Style Blueprint card
├── gap_analysis.md       # Gap Analysis results
├── rewritten_draft.md    # Rewritten draft + Change Summary
└── session_log.md        # Input metadata (reference source, draft origin, Mode, settings)
```

- `{topic}` is specified by the user or automatically derived from the reference paper/journal name
- If the user does not want files saved, screen output alone is sufficient

---

## Parallel Processing (Subagent)

### Analyzing multiple reference papers simultaneously
```
사용자: "이 3편 논문 스타일 분석해서 리라이팅해줘"
→ Create a Task (Subagent) for each paper → Extract Blueprints independently
→ Merge common patterns → Generate Master Blueprint
→ Rewrite draft using Master Blueprint
```

### Rewriting multiple sections simultaneously
```
사용자: "Introduction이랑 Discussion 둘 다 리라이팅해줘"
→ Create a Task (Subagent) for each section
→ Same Blueprint, independent rewriting per section
```

---

## Quality Standards

1. **Style transfer only**: Never copy ideas, data, or claims from the reference source
2. **Content preservation**: Do not alter the scientific meaning, citations, or data in the draft
3. **Evidence-based**: Use actual example sentences from the Blueprint as justification for edits (no abstract advice)
4. **Quantitative diagnosis**: Provide numerical scoring in the Gap Analysis
5. **Traceable**: Specify the applied Blueprint dimension and rule for every edit
6. **Natural prose**: Aim for natural academic writing, not mechanical substitution
7. **Confidence transparency**: Clearly state the Blueprint's confidence level (High/Medium/Low)

---

## Error Handling

| Situation | Response |
|-----------|----------|
| Reference source text too short (<200w) | Warning: "Blueprint accuracy may be low", Confidence: Low |
| Reference source text >500w, multiple sections | Confidence: High |
| Journal name only + not in journal-styles.md | Attempt Web search; if unavailable, warn + request actual paper |
| User's draft too short (<2 sentences) | Warning: "Paragraph-length or longer text recommended" |
| Existing Style databank format mismatch | Best-effort parsing, flag problematic items |
| Section type cannot be determined | Ask the user to confirm |
| Reference source and draft are from different fields | Display warning, then proceed (style transfer is field-independent) |

---

## Usage Examples

### Example 1: PDF reference + draft rewriting
```
> "이 GCA 논문처럼 내 Introduction 써줘"
→ Read PDF → Extract Blueprint → Request draft → Gap Analysis → Rewrite
```

### Example 2: Journal name only
```
> "Nature Geoscience 스타일로 맞춰줘"
→ Load journal-styles.md (Confidence: Low~Medium)
→ Generate Blueprint → Request draft → Rewrite
```

### Example 3: Using an existing databank
```
> "Style_지화학/ 데이터뱅크 기반으로 리라이팅해줘"
→ Style databank → Convert to Blueprint → Request draft → Rewrite
```

### Example 4: Master Blueprint from multiple papers
```
> "이 3편 논문 스타일 분석해서 내 Discussion 리라이팅해줘"
→ Parallel Blueprint extraction → Merge common patterns → Master Blueprint → Rewrite
```

### Example 5: Mode B full rewrite
```
> "이 Methods 섹션 전체를 ES&T 스타일로 다시 써줘"
→ Blueprint + draft → Gap Analysis → Mode B full rewrite + Change Summary
```

---

## References

| File | Read when | Content |
|------|-----------|---------|
| `references/blueprint-template.md` | PHASE 2 — Before Blueprint extraction | Extraction guidelines for each of the 6 dimensions, Blueprint card output format |
| `references/journal-styles.md` | PHASE 1 — When only a journal name is provided | Style profiles for major journals |
| `references/output-formats.md` | PHASE 4 & 5 — Gap Analysis and rewriting output | Gap Analysis card, Mode A/B output format, Change Summary |

---

**Version**: 1.0.0
**Skill by**: Meta_researcher / meta-rewriting
