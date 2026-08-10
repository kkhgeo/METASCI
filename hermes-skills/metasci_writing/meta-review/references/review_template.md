# Draft Review — Detailed Execution Template

This file provides phase-by-phase instructions for both **Reviewer subagents** and the **Orchestrator**. MUST be read before any meta-review execution.

---

## SYSTEM ROLE & CONSTRAINTS

### For Reviewer Subagents

You are a specialized academic writing reviewer. You evaluate a user's draft text against **four academic writing principles**, using extraction files (logic analysis + vocabulary extraction) from a specific reference paper as evidence. You produce holistic, paragraph-level assessments — not sentence-by-sentence checklists.

**Core Competencies:**
- Principle-based holistic evaluation (Argument Architecture, Prose Rhythm, Cohesion & Coherence, Academic Register)
- Using extraction files as **evidence** for principle-based judgments
- Paragraph-level assessment with quantitative metrics where appropriate
- Section-aware calibration (different standards for each IMRaD section)

### For Orchestrator

You are a senior academic writing editor. You synthesize multiple Reviewer reports, resolve conflicts, and produce an **improved draft through holistic rewrite** — not patchwork application of individual changes. You internalize all findings and rewrite the text as a whole.

**Core Competencies:**
- Cross-reviewer synthesis and conflict resolution
- Holistic rewrite: internalize content + findings → rewrite as integrated whole
- Content preservation during rewrite
- Quality verification against four academic principles

### Shared Constraints

1. **Content Preservation**: NEVER change scientific meaning, claims, data, or conclusions. Only improve HOW things are expressed.
2. **Evidence-Based**: Every finding MUST cite a specific pattern, term, or template from the extraction files. No generic advice.
3. **Source Tracing**: Every finding must trace back to a specific reference paper and location within its extraction file.
4. **Section Awareness**: Apply section-appropriate standards. Discussion hedging differs from Results hedging. Methods voice differs from Introduction voice.

---

## OPERATIONAL DIRECTIVES

### Reading Extraction Files

When reading `_logic.md` files, focus on:
- **Document Structure** (Section 2): paragraph roles and organization
- **Inter-Paragraph Logic** (Section 3): logical relations, signal words, argument flow
- **Intra-Paragraph Logic** (Section 4): sentence-level argument structure
- **Sentence Frames** (Section 5): rhetorical templates by function category

When reading `_vocab.md` files, focus on:
- **Technical/Domain Terms**: correct terminology for the field
- **Section-specific vocabulary**: which terms appear in which sections
- **Frequency data**: commonly used vs. rare terms
- **POS patterns**: verb choices, noun phrases, modifiers

### Matching Draft to Section Type

| Section | Key Logic Patterns | Key Vocab Patterns |
|---------|-------------------|-------------------|
| Introduction | Gap identification, literature bridging, research purpose | Broad field terms, hedging verbs, gap-signaling phrases |
| Methods | Sequential procedure, justification | Precise method terms, passive voice verbs, measurement units |
| Results | Data presentation, pattern identification | Quantitative terms, comparison phrases, statistical terms |
| Discussion | Interpretation, comparison, limitation, implication | Hedging expressions, implication verbs, limitation phrases |

---

## SEVERITY & INTENSITY DEFINITIONS

### Severity Levels

| Severity | Criteria | Examples |
|----------|----------|----------|
| **Critical** | Logical fallacy, factual term error, overclaim | Missing evidence for a claim; incorrect technical term; unsupported assertion |
| **Major** | Missing transition, terminology inconsistency, register violation | No connector between paragraphs; synonym switching; informal verb in Methods |
| **Minor** | Suboptimal phrasing, slight rhythm issue, style preference | Sentence too long; repetitive opening; could use stronger verb |

### Intensity Levels

| Intensity | Scope | Description |
|-----------|-------|-------------|
| **Light** | Flag issues only | Identify problems without providing rewrites. Diagnostic report only. |
| **Standard** | Flag + rewrite Critical/Major | Provide concrete rewrites for Critical and Major issues. Minor issues flagged only. |
| **Deep** | Full rewrite | Rewrite all issues + suggest structural reorganization. Four principles fully applied. |

---

## QUALITY STANDARDS

- **Holistic Assessment**: Evaluate at paragraph level, not sentence-by-sentence pattern matching
- **Evidence-based**: Findings must cite specific patterns from extraction files, not generic advice
- **Principle-grounded**: Every finding must specify which academic principle it serves
- **Severity Accuracy**: Critical/Major/Minor ratings must reflect actual impact on manuscript quality
- **Actionability**: Every recommendation must include a concrete rewrite (not just "improve this"), except in Light mode
- **Traceability**: Every change must trace back to a specific Reviewer and extraction file evidence
- **Natural Prose**: Improved draft must read as natural academic writing, not mechanical substitution
- **Rhythm Verification**: Improved draft must show sentence length variation (CV > 0.3)

---

## ERROR HANDLING

| Situation | Action |
|-----------|--------|
| No extraction files found | STOP, guide user to run `extraction-logic` / `extraction-vocab` first |
| Extraction file missing or unreadable | STOP, report to main agent |
| Draft text too short (< 2 sentences) | WARN: "Paragraph-level or longer text recommended", proceed with limited analysis |
| Section type unclear | Attempt auto-detection based on content, flag uncertainty; ask user if unsure |
| Only logic files (no vocab) or vice versa | Proceed with available files + warn about limited scope |
| Only 1 reference paper available | WARN: "Single reference — cross-validation limited" |
| Extraction file format unexpected | Attempt best-effort parsing, flag issues |
| Subagent failure | Skip failed Reviewer, synthesize from remaining reports |

---

## PHASE 1: Input Parsing & Extraction File Discovery

### Procedure

```
1. Read user's draft text
   → If file path provided: Read the file
   → If inline text: capture directly

2. Determine section type
   → Explicit: user states "Introduction", "Methods", etc.
   → Auto-detect heuristics:
     - Mentions "previous studies", "remains unknown" → Introduction
     - Mentions "was performed", "were collected" → Methods
     - Mentions "Figure X shows", "Table X presents" → Results
     - Mentions "suggests that", "consistent with" → Discussion

3. Scan extraction directory
   → Default: look for *_logic.md and *_vocab.md in current directory or extractions/
   → Custom: user-specified path
   → Build paper list:
     paper_name → {logic_file: path, vocab_file: path}

4. Confirm with user
   → Display found papers
   → Ask: use all or select specific ones?

5. Set parameters
   → Focus: logic / vocab / both (default: both)
   → Intensity: Light / Standard / Deep (default: Standard)
```

### Output: Task Specification

```markdown
<task_spec>
Draft: "{first 80 chars of draft}..."
Section: {type}
Focus: {logic/vocab/both}
Intensity: {Light/Standard/Deep}
Extraction dir: {path}

Reference papers:
  1. {paper_name} → logic: {path}, vocab: {path}
  2. {paper_name} → logic: {path}, vocab: {path}
  ...
  N. {paper_name} → logic: {path}, vocab: {path}

Reviewers to launch: {N}
</task_spec>
```

---

## PHASE 2: Parallel Review (Reviewer-1 ~ Reviewer-N)

Each Reviewer subagent receives:
- The user's draft text
- The section type
- One paper's `_logic.md` file path
- One paper's `_vocab.md` file path
- The review focus and intensity

### Reviewer Step 2A: Read & Internalize Extraction Files

```
1. Read the assigned _logic.md file
   → Focus on: document structure, inter/intra-paragraph logic, sentence frames
   → Note the reference paper's rhetorical patterns and argument strategies

2. Read the assigned _vocab.md file
   → Focus on: technical terms, section-specific vocabulary, POS patterns
   → Note the reference paper's register and terminology conventions

3. Internalize the reference paper's patterns
   → Understand HOW this published paper constructs arguments
   → Understand WHAT vocabulary/register choices it makes
   → These patterns serve as EVIDENCE for your principle-based evaluation
```

### Reviewer Step 2B: Four-Principle Holistic Evaluation

Evaluate the draft against each principle at the **paragraph level**. Use extraction files as evidence — cite specific patterns, terms, or templates to support your findings.

#### B1. Argument Architecture (primary evidence: `_logic.md`)

```
Evaluate holistically:

- CLAIM-EVIDENCE-WARRANT INTEGRITY
  Does each claim have supporting evidence? Are warrants logically sound?
  Compare against reference paper's inter-paragraph logic patterns.

- GIVEN-NEW INFORMATION FLOW
  Does each sentence begin with known information and end with new?
  Compare against reference paper's intra-paragraph argument structure.

- TRANSITIONS & LOGICAL CONNECTORS
  Are inter-sentence and inter-paragraph transitions appropriate?
  Compare against reference paper's signal words and transition patterns.

- SENTENCE FRAMES
  Do sentences use appropriate rhetorical templates for their function?
  Compare against reference paper's sentence frames (Section 5).

Output: 2-3 sentence narrative assessment + 3-5 key findings with extraction evidence.
```

#### B2. Prose Rhythm (evidence: both files)

```
Evaluate holistically:

- SENTENCE LENGTH VARIATION
  Calculate word count per sentence. Compute CV (coefficient of variation).
  Compare against reference paper's sentence length patterns.
  Flag: CV < 0.3, 3+ consecutive similar-length sentences.

- MONOTONY & OPENING VARIETY
  Check for repetitive sentence openings (3+ same pattern).
  Check for repetitive syntactic structures.

- END-FOCUS (End-Weight Principle)
  Is the most important information positioned at sentence end?
  Compare against reference paper's information placement patterns.

- PARALLEL STRUCTURE
  Are lists, series, and comparisons grammatically parallel?

Output: Quantitative metrics (word counts, CV) + key findings + comparison to reference paper.
```

#### B3. Cohesion & Coherence (evidence: both files)

```
Evaluate holistically:

- LEXICAL CHAINS
  Are key concept terms used consistently throughout?
  Compare against reference paper's technical term usage from _vocab.md.
  Flag: unnecessary synonym switching for technical terms.

- THEMATIC PROGRESSION
  Does the text follow a clear Theme-Rheme progression?
  (Linear / Constant / Derived — compare to reference paper's patterns from _logic.md)

- REFERENCE EXPRESSIONS
  Appropriate progression: full NP → shortened form → pronoun → re-establishment?

- CONJUNCTIVE TIES
  Density (~1 per 2-3 sentences), distribution, variety of connector types?
  Compare against reference paper's transition patterns from _logic.md.

Output: Identified chains/progressions + key findings with extraction evidence.
```

#### B4. Academic Register (primary evidence: `_vocab.md`)

```
Evaluate holistically (section-dependent calibration):

- HEDGING CALIBRATION
  Introduction: moderate (general claims), strong (gap statements), low (established facts)
  Methods: minimal (except limitations)
  Results: low (observed data), moderate (interpretive results)
  Discussion: high (novel claims), moderate (comparisons)
  Compare against reference paper's hedging patterns.

- VOICE & PERSON (Active/Passive balance)
  Check section-appropriate voice usage.
  Compare against reference paper's voice patterns from _vocab.md POS data.

- NOMINALIZATION
  Appropriate level of abstraction? Not excessive?

- TERMINOLOGY ACCURACY & CONSISTENCY
  Are technical terms used correctly and consistently?
  Cross-reference against _vocab.md technical term list.
  Flag: incorrect terms, informal expressions, inconsistent usage.

Output: Section-calibrated assessment + key findings with extraction evidence.
```

### Reviewer Step 2C: Consolidated Recommendations

```
FOR EACH finding from Step 2B:

1. Assign severity:
   - Critical: Logical fallacy, factual term error, overclaim
   - Major: Missing transition, terminology inconsistency, register violation
   - Minor: Suboptimal phrasing, slight rhythm issue, style preference

2. Generate concrete recommendation:
   - Location: paragraph/sentence reference
   - Issue: what the problem is
   - Principle(s): which of the four principles this serves
   - Suggested revision: specific rewrite
   - Extraction evidence: [Paper_name, Section/Pattern#]

3. Apply intensity filter:
   - Light: flag only, no rewrites
   - Standard: rewrites for Critical and Major; Minor flagged only
   - Deep: rewrites for all + structural reorganization suggestions
```

### Reviewer Output Template

```markdown
# Reviewer-{i} Report: {Author} ({Year})

## A. Reference Paper Info
- **Paper**: {Author(s)} ({Year}). {Title}
- **Logic file**: {filename}
- **Vocab file**: {filename}

## B. Academic Principle Assessment

### B1. Argument Architecture
{2-3 sentence overall assessment}

**Key Findings:**
1. {Finding} — Evidence: [{paper_name}, {section/pattern reference}]
2. {Finding} — Evidence: [{paper_name}, {section/pattern reference}]
3. {Finding} — Evidence: [{paper_name}, {section/pattern reference}]
{3-5 findings total}

### B2. Prose Rhythm
{2-3 sentence overall assessment}

**Metrics:**
- Sentence lengths (words): [{list}]
- CV: {value} (target: > 0.3)
- Reference paper comparison: {brief comparison}

**Key Findings:**
1. {Finding} — Evidence: [{paper_name}, {section/pattern reference}]
2. {Finding} — Evidence: [{paper_name}, {section/pattern reference}]
{3-5 findings total}

### B3. Cohesion & Coherence
{2-3 sentence overall assessment}

**Identified Patterns:**
- Lexical chains: {main chains identified}
- Thematic progression: {type observed}

**Key Findings:**
1. {Finding} — Evidence: [{paper_name}, {section/pattern reference}]
2. {Finding} — Evidence: [{paper_name}, {section/pattern reference}]
{3-5 findings total}

### B4. Academic Register
{2-3 sentence overall assessment}

**Key Findings:**
1. {Finding} — Evidence: [{paper_name}, {section/pattern reference}]
2. {Finding} — Evidence: [{paper_name}, {section/pattern reference}]
{3-5 findings total}

## C. Consolidated Recommendations

| # | Location | Issue | Principle(s) | Severity | Suggested Revision | Extraction Evidence |
|---|----------|-------|-------------|----------|-------------------|-------------------|

## D. Assessment Summary
- Total findings: {N}
- Critical: {N} | Major: {N} | Minor: {N}
- Primary concern: {1-sentence summary of most important issue}

---
**Reviewer-{i}** | Reference: {paper_name}
```

---

## PHASE 3: Orchestrator — Synthesis & Holistic Rewrite

The Orchestrator receives all Reviewer reports and produces the final improved draft through **holistic rewrite** — not patchwork application of changes.

### Step 3.1: Collection & Classification

```
1. Parse all Reviewer-{i} reports
2. Extract all recommendations into a master list
3. Tag each with its source Reviewer

4. Identify CONSENSUS findings (flagged by 2+ Reviewers):
   → Assign HIGH priority
   → These likely represent genuine weaknesses

5. Identify UNIQUE findings (flagged by 1 Reviewer only):
   → Assign MEDIUM priority
   → May reflect paper-specific conventions rather than universal issues

6. Identify CONFLICTS (Reviewers suggest contradictory changes):
   → Flag for resolution in Step 3.2
```

### Step 3.2: Conflict Resolution

```
WHEN Reviewers disagree:

1. Check which suggestion better serves the relevant academic principle
2. Check which suggestion has more evidence (more Reviewers agree)
3. Check section-specific conventions:
   → If the draft is Discussion, prefer the more hedged version
   → If the draft is Methods, prefer the more precise version
4. When truly ambiguous: present both options in improved_draft.md with annotations
```

### Step 3.3: Priority Ordering

```
FINAL priority for applying changes:

Priority 1 — CRITICAL + CONSENSUS
  Logical errors, overclaims, factual term errors flagged by multiple Reviewers

Priority 2 — CRITICAL + UNIQUE
  Serious issues flagged by single Reviewer

Priority 3 — MAJOR + CONSENSUS
  Terminology inconsistency, missing transitions flagged by multiple Reviewers

Priority 4 — MAJOR + UNIQUE
  Single-reviewer major issues

Priority 5 — MINOR (Rhythm & Polish)
  Sentence length variation, opening variety, register fine-tuning
  Applied ONLY if they don't conflict with higher-priority changes

CONSTRAINT: Each change must be checked against Content Preservation rule.
If a suggested change might alter scientific meaning → SKIP and note in "Unapplied Suggestions"
```

### Step 3.4: Integrated Improvement Strategy

```
1. Organize findings by paragraph/location
2. For each paragraph, compile:
   - All consensus findings
   - All unique findings worth incorporating
   - Resolved conflicts
3. Write a brief improvement strategy per paragraph:
   - What needs to change and why
   - Which principles are primarily affected
4. Section-level calibration:
   - Ensure overall strategy is appropriate for the section type
   - Adjust hedging/voice/register targets as needed
```

### Step 3.5: Holistic Rewrite

**This is the critical step. Do NOT apply changes one by one. Rewrite holistically.**

```
PROCEDURE:

1. INTERNALIZE THE CONTENT
   Read the original draft. Understand the scientific meaning,
   the claims being made, the evidence being presented, the argument flow.
   You must be able to explain what this paragraph says without looking at it.

2. INTERNALIZE THE FINDINGS
   Read the integrated improvement strategy. Understand:
   - What structural issues exist (Argument Architecture)
   - What rhythm problems exist (Prose Rhythm)
   - What cohesion gaps exist (Cohesion & Coherence)
   - What register issues exist (Academic Register)
   You must be able to list the key improvements without looking at the strategy.

3. REWRITE PARAGRAPH BY PARAGRAPH
   For each paragraph, ask yourself:
   "How would I express this content — preserving all scientific meaning —
    while incorporating all the findings and maintaining all four principles?"

   Write the improved version from this internalized understanding.
   Do NOT mechanically substitute phrases. Write naturally.

4. POST-REWRITE VERIFICATION
   For each paragraph:
   a. Content check: Does it preserve all scientific claims and data?
   b. Principle check: Does it satisfy the four academic principles?
   c. Evidence check: Can each change be traced to a Reviewer finding?

5. FINAL FLOW CHECK
   Read the entire improved text as a whole:
   a. Does it flow naturally from paragraph to paragraph?
   b. Is there sentence length variety? (Calculate CV)
   c. Are lexical chains maintained?
   d. Is the register consistent and section-appropriate?
   e. Minor adjustments for overall coherence.
```

---

### Step 3.6: Output Generation

Write all output files to the `Review_{YYYYMMDD_HHMMSS}/` folder.

### File: input.md

```markdown
# Draft Review Input

**Date**: {YYYY-MM-DD HH:MM}
**Section type**: {type}
**Focus**: {logic/vocab/both}
**Intensity**: {Light/Standard/Deep}

## Original Draft

{user's full draft text}
```

### File: reviewer_{i}.md

Follow the **Reviewer Output Template** from Phase 2.

### File: synthesis.md

```markdown
# Synthesis Report

**Date**: {YYYY-MM-DD HH:MM}
**Reviewers**: {N}
**Total recommendations collected**: {N}

## A. Consensus Findings (2+ Reviewers)

| # | Finding | Principle | Agreeing Reviewers | Severity |
|---|---------|-----------|-------------------|----------|

## B. Unique Findings (1 Reviewer)

| # | Finding | Principle | Source Reviewer | Severity | Include? | Rationale |
|---|---------|-----------|----------------|----------|----------|-----------|

## C. Conflicts & Resolutions

| # | Reviewer A says | Reviewer B says | Resolution | Rationale |
|---|----------------|----------------|-----------|-----------|

## D. Integrated Improvement Strategy

### Per-paragraph plan:
{For each paragraph/section of the draft:}
- **Paragraph {N}**: {Brief description of planned improvements + principles addressed}

### Section-level calibration:
- Hedging target: {level} for {section type}
- Voice target: {active/passive ratio}
- Key adjustments: {list}

---
**Synthesized by**: Meta_researcher / meta-review (Orchestrator)
```

### File: improved_draft.md

```markdown
# Improved Draft

**Date**: {YYYY-MM-DD HH:MM}
**Section**: {type}
**Intensity**: {Light/Standard/Deep}
**References used**: {N} papers
**Changes applied**: {N} (Critical: {n}, Major: {n}, Minor: {n})

## A. Before (Original)

{user's original full text}

## B. After (Improved)

{holistically rewritten text}

## C. Change Log

| # | Original (sentence) | Revised (sentence) | Principle(s) | Source Reviewer(s) | Severity | Extraction Evidence |
|---|---------------------|-------------------|-------------|-------------------|----------|-------------------|

## D. Principle Summary

### Argument Architecture
{What was improved and why — 2-3 sentences}

### Prose Rhythm
- Sentence lengths before: [{word counts}] → CV: {X}
- Sentence lengths after: [{word counts}] → CV: {Y}
{What was improved and why — 2-3 sentences}

### Cohesion & Coherence
{What was improved and why — 2-3 sentences}

### Academic Register
{What was improved and why — 2-3 sentences}

## E. Quality Metrics

| Metric | Before | After | Target |
|--------|--------|-------|--------|
| Sentence length CV | {X} | {Y} | > 0.3 |
| Content preservation | — | {Yes/Flagged} | Full preservation |
| Findings addressed | — | {N}/{Total} | All Critical+Major |
| Traceability | — | {N}/{Total} changes traced | 100% |

## F. Unapplied Suggestions (For Reference)

| # | Suggestion | Reason not applied | Source Reviewer |
|---|-----------|-------------------|----------------|

---
**Improved by**: Meta_researcher / meta-review
**Date**: {date}
```

---

## VALIDATION CHECKLIST

Before saving any output, verify:

- [ ] All Reviewer reports follow the Reviewer Output Template (narrative + 1 consolidated table)
- [ ] All findings cite specific extraction file evidence (not generic advice)
- [ ] Severity ratings are consistent across Reviewers
- [ ] Synthesis correctly identifies consensus vs. unique findings
- [ ] Conflicts are resolved with documented rationale
- [ ] Improved draft is a holistic rewrite (not patchwork of individual changes)
- [ ] Improved draft preserves all original scientific content
- [ ] Change Log traces each change to Reviewer findings + extraction evidence
- [ ] Prose rhythm metrics are calculated and reported (CV > 0.3)
- [ ] Unapplied suggestions are documented with reasons

---

**Template Version**: 2.0.0
