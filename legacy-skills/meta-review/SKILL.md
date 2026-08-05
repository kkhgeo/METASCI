---
name: meta-review
description: |
  Review and improve user's draft (paragraph/section) against multiple reference paper
  extraction files (logic + vocab). Per-paper Reviewer subagents evaluate the draft
  using four academic writing principles (with extraction files as evidence),
  then Orchestrator synthesizes findings and produces a holistic rewrite.
  Triggers: "초고 점검", "단락 개선", "리뷰해줘", "draft review".
  **MUST read references/review_template.md before starting!**
allowed-tools: [Read, Write, Edit, Bash, Task, Glob, Grep]
---

> **REQUIRED**: Read `references/review_template.md` before execution.
> The template is the **authoritative source** for all detailed procedures and output formats.

# Draft Review Skill

## Overview

Review a user's academic draft (paragraph or section) by comparing it against pre-extracted reference paper analysis files (`_logic.md`, `_vocab.md`), then produce an improved version through holistic rewrite.

**Core Architecture:**
```
User's draft text
    ↓
[Phase 1] Input parsing & extraction file discovery
    ↓
[Phase 2] Reviewer-1 ~ Reviewer-N: 4-principle holistic evaluation (one subagent per paper)
    ↓
[Phase 3] Orchestrator: synthesis + conflict resolution + holistic rewrite
    ↓
Output: Review_{timestamp}/ folder with all reports + improved draft
```

**Key Design Decisions:**
- Each Reviewer evaluates ALL four academic principles (not just pattern matching)
- Extraction files serve as **evidence** for principle-based evaluation (not checklists)
- Orchestrator focuses on **synthesis + holistic rewrite** (not principle application)
- Improved draft is a **complete rewrite**, not patchwork of individual changes

**Relationship to Other Skills:**
- **Downstream consumer** of `extraction-logic` and `extraction-vocab` outputs
- **Complementary** to `meta-styling Mode B`: meta-styling uses style databank; meta-review uses logic+vocab extraction files

---

## Triggers

### Korean
- "이 단락 리뷰해줘"
- "초고 점검해줘"
- "이 문단 개선해줘"
- "논리랑 용어 점검해줘"
- "extractions 기반으로 수정해줘"
- "참조 논문 기준으로 고쳐줘"

### English
- "review this draft"
- "draft review"
- "check logic and terminology"
- "improve this paragraph"
- "review against extractions"

---

## Input Requirements

### Required
1. **Draft text**: Paragraph or section to review (inline text or file path)
2. **Section type**: Introduction / Methods / Results / Discussion (explicit or auto-detected)

### Optional
- **Extraction directory**: Path to folder containing `_logic.md` and `_vocab.md` files (default: `./extractions/` or current directory)
- **Reference papers**: All (default) or specific papers only
- **Focus**: logic / vocab / both (default: both)
- **Intensity**: Light (flag only) / Standard (flag + rewrites, default) / Deep (full rewrite)

### Intensity Definitions

| Intensity | Scope | Description |
|-----------|-------|-------------|
| **Light** | Flag issues only | Identify problems without providing rewrites. Diagnostic report only. |
| **Standard** | Flag + rewrite Critical/Major | Provide concrete rewrites for Critical and Major issues. Minor issues flagged only. |
| **Deep** | Full rewrite | Rewrite all issues + suggest structural reorganization. Four principles fully applied. |

### Severity Definitions

| Severity | Criteria | Examples |
|----------|----------|----------|
| **Critical** | Logical fallacy, factual term error, overclaim | Missing evidence for a claim; incorrect technical term; unsupported assertion |
| **Major** | Missing transition, terminology inconsistency, register violation | No connector between paragraphs; synonym switching; informal verb in Methods |
| **Minor** | Suboptimal phrasing, slight rhythm issue, style preference | Sentence too long; repetitive opening; could use stronger verb |

### Input Examples
```
> "Review this Introduction paragraph. Use all files in the extractions folder."

> "Improve this Discussion paragraph. Only reference ngeo1617 and Review_urban."

> "Check logic flow only. Light mode."

> "Deep rewrite this Methods section using all reference papers."

> "Review this paragraph using extractions from Z:\other_project\extractions."
```

---

## Workflow

**MUST read `references/review_template.md` first and follow it exactly!**

### Phase 1: Input Parsing & Extraction File Discovery

```
1. Acquire draft text
   → Inline text: capture directly
   → File path: read the file

2. Determine section type
   → Explicit: user states "Introduction", "Methods", etc.
   → Auto-detect heuristics:
     - "previous studies", "remains unknown" → Introduction
     - "was performed", "were collected" → Methods
     - "Figure X shows", "Table X presents" → Results
     - "suggests that", "consistent with" → Discussion

3. Scan extraction directory
   → Find *_logic.md and *_vocab.md files
   → Match file pairs by paper name (e.g., ngeo1617_logic.md + ngeo1617_vocab.md)

4. Confirm reference paper list
   → Display discovered papers to user
   → Ask: use all or select specific ones?

5. Set parameters & output task specification
```

### Phase 2: Parallel Review (Reviewer-1 ~ Reviewer-N)

Assign **one subagent per reference paper**.

Each Reviewer evaluates the draft against **all four academic writing principles**, using extraction files as evidence (see `review_template.md` Phase 2 for detailed procedures):

```
FOR EACH reference paper (i = 1 to N):
    → Launch Task (Subagent): Reviewer-{i}
    → Input: draft text + paper's _logic.md + _vocab.md

    Step A: Read Extraction Files
        - Read _logic.md: structure, argument flow, sentence frames
        - Read _vocab.md: terminology, register, POS patterns
        - Internalize the reference paper's patterns

    Step B: Four-Principle Holistic Evaluation
        - B1. Argument Architecture (using _logic.md)
              Claim-Evidence-Warrant integrity, Given-New flow,
              transitions, sentence frames
        - B2. Prose Rhythm (using both files)
              Sentence length variation, monotony, end-focus,
              parallel structure — with quantitative metrics
        - B3. Cohesion & Coherence (using both files)
              Lexical chains, thematic progression, reference
              expressions, conjunctive ties
        - B4. Academic Register (using _vocab.md)
              Hedging, active/passive voice, nominalization,
              term accuracy — section-appropriate calibration

    Step C: Consolidated Recommendations
        - Integrate findings across all four principles
        - Classify severity: Critical / Major / Minor
        - One unified table with extraction evidence
```

**Output**: Narrative assessment + single consolidated table → see `review_template.md` Reviewer Output Template.

### Phase 3: Orchestrator Synthesis & Output

Collect all Reviewer reports, synthesize findings, resolve conflicts, and produce a **holistic rewrite**.

```
Step 1: Collection & Classification
    → Parse all Reviewer reports
    → Classify findings: CONSENSUS (2+ Reviewers) vs. UNIQUE (1 Reviewer only)
    → Identify CONFLICTS (contradictory suggestions)

Step 2: Conflict Resolution & Priority Ordering
    → Critical + Consensus > Critical + Unique > Major + Consensus > Major + Unique > Minor
    → Section-specific preferences (Discussion → prefer hedged; Methods → prefer precise)
    → Content preservation: NEVER alter scientific meaning

Step 3: Integrated Improvement Strategy
    → Merge consensus/unique findings into per-paragraph improvement plan
    → Ensure all four principles are addressed (already evaluated by Reviewers)
    → Section-specific calibration adjustments

Step 4: Holistic Rewrite
    → Internalize original draft content (meaning, claims, data)
    → Internalize all Reviewer findings and improvement strategy
    → Rewrite paragraph by paragraph:
       "How would I express this content, incorporating all findings,
        while maintaining the four academic principles?"
    → Post-rewrite verification: principle compliance + content preservation
    → Final flow check: read entire improved text as a whole

Step 5: Write Output Files
    → Write all files to Review_{timestamp}/ folder
    → Validate against checklist (see review_template.md VALIDATION CHECKLIST)
```

---

## Output Structure

```
Review_{YYYYMMDD_HHMMSS}/
├── input.md                 # Original draft + metadata
├── reviewer_1.md            # Reviewer-1 report (paper A)
├── reviewer_2.md            # Reviewer-2 report (paper B)
├── ...
├── reviewer_N.md            # Reviewer-N report (paper N)
├── synthesis.md             # Cross-reviewer synthesis + principle evaluation
└── improved_draft.md        # Final improved text + change log
```

### File Summaries

| File | Key Sections | Details |
|------|-------------|---------|
| `input.md` | Metadata + original draft | Date, section type, focus, intensity, full draft text |
| `reviewer_{i}.md` | A. Paper Info → B. Principle Assessment (B1-B4 narrative) → C. Consolidated Recommendations (1 table) → D. Summary | Narrative + single integrated table per paper |
| `synthesis.md` | A. Consensus Findings → B. Unique Findings → C. Conflicts & Resolutions → D. Integrated Improvement Strategy | Lightweight cross-reviewer synthesis |
| `improved_draft.md` | A. Before → B. After → C. Change Log → D. Principle Summary → E. Quality Metrics | Holistic rewrite with per-sentence rationale |

**For complete output templates with exact table columns and formats**, see `references/review_template.md` Step 3.6: Output Generation.

---

## Parallel Processing (Subagent)

### Reviewer Parallel Execution

```
N reference papers found
→ Launch N Task (Subagent) calls concurrently
→ Each Subagent:
    1. Read references/review_template.md
    2. Read assigned paper's _logic.md + _vocab.md
    3. Compare against user's draft
    4. Output structured review report
→ After ALL Subagents complete → run Orchestrator (Phase 3)
```

### Subagent Prompt Template

```
You are Reviewer-{i}. Your task is to evaluate the user's draft text
against four academic writing principles, using extraction files from
a reference paper as evidence.

**MUST READ FIRST**: {skill_path}/references/review_template.md

**Draft text**: {draft_text}
**Section type**: {section_type}
**Logic file**: {logic_file_path}
**Vocab file**: {vocab_file_path}
**Focus**: {logic/vocab/both}
**Intensity**: {Light/Standard/Deep}

Evaluate all four principles (Argument Architecture, Prose Rhythm,
Cohesion & Coherence, Academic Register) using extraction files as evidence.
Produce narrative assessments + one consolidated recommendations table.
Follow the Reviewer Output Template in review_template.md exactly.
```

---

## Quality Standards

1. **Evidence-based**: Every suggestion must cite a specific pattern/term/template from extraction files. No generic advice.
2. **Content preservation**: NEVER alter scientific meaning, claims, or data — expression only
3. **Holistic assessment**: Evaluate at paragraph level, not sentence-by-sentence pattern matching
4. **Principle-grounded**: Every finding must specify which of the four principles it serves
5. **Natural prose**: Improved draft must read as natural academic writing, not mechanical substitution
6. **Traceable**: Every change must trace back to a specific Reviewer's finding + extraction evidence
7. **Prioritized**: Changes ordered Critical > Major > Minor
8. **Rhythm-verified**: Improved draft must show sentence length variation (CV > 0.3)

---

## Error Handling

| Situation | Response |
|-----------|----------|
| No extraction files found | Guide user to run `extraction-logic` / `extraction-vocab` first |
| Only logic files (no vocab) or vice versa | Proceed with available files + warn about limited scope |
| Section type unclear | Ask user to specify |
| Draft too short (< 2 sentences) | Warn: "Paragraph-level or longer text recommended" |
| Only 1 reference paper available | Warn: "Single reference — cross-validation limited" |
| Extraction file format unexpected | Attempt best-effort parsing, flag issues |
| Subagent failure | Skip failed Reviewer, synthesize from remaining reports |

---

## Usage Examples

### Example 1: Basic usage
```
> "Review this Introduction paragraph."
→ Auto-scan extractions/ folder
→ All discovered reference papers → parallel review
→ Standard intensity → improved draft output
```

### Example 2: Specific papers only
```
> "Improve this Discussion paragraph. Only use ngeo1617 and Review_urban."
→ Reviewer-1 (ngeo1617) + Reviewer-2 (Review_urban) only
```

### Example 3: Logic-only check
```
> "Check logic flow only. Light mode."
→ Read _logic.md files only, flag issues without rewrites
```

### Example 4: Full rewrite
```
> "Deep rewrite this Methods section."
→ All reference files, all four principles fully applied, structural reorganization
```

### Example 5: External directory
```
> "Review this paragraph using Z:\other_project\extractions."
→ Use extraction files from specified path
```

---

**Version**: 2.0.0
**Skill by**: Meta_researcher / meta-review
