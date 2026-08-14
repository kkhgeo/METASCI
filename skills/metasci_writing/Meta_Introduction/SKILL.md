---
name: Meta_Introduction
description: "Meta-workflow skill for designing, generating, and evaluating Introduction sections of environmental science papers. Builds a structural Blueprint from Results/Discussion or research topic, writes publication-ready Introductions using Knowledge files (literature), and evaluates quality using the CARS model. Activate on requests like: 'write Introduction', 'create Introduction blueprint', 'generate scientific Introduction', or when both research context and Knowledge folder are provided."
---

# Meta Introduction — Environmental Science Paper Introduction Architect

## Overview

A 3-stage meta-workflow for constructing environmental science paper Introductions:
Blueprint (structural design) → Generation (writing) → Evaluation (quality assessment).
User approval checkpoints are placed between stages.

## When to Activate

- User requests writing an Introduction for an environmental science paper
- Results/Discussion + Knowledge folder, OR research topic + Knowledge folder are provided
- Keywords: Introduction, blueprint, CARS, scientific writing, environmental science, paper introduction

## Workflow

```
Stage 0 (Intake) → Stage 1 (Blueprint) → ★ User Approval ★ → Stage 2 (Generation) → Stage 3 (Evaluation)
```

---

## Stage 0: Intake (Specification Collection)

At skill start, collect the following specifications using AskUserQuestion.

### Question 1: Input Mode
```
□ Mode A: Results/Discussion provided → Reverse-engineer structure from R&D
□ Mode B: Research topic + objectives described directly → Design structure from user input
```

### Question 2: Settings
```
□ Introduction length: [Concise: 500-700 words] [Standard: 900-1300] [Extended: 1500-2000]
□ Journal tier: [Nature/Science/PNAS] [Field-top] [Specialized]
□ Primary novelty axis: [Method] [Scale/Data] [Theory] [Application]
□ Output language: [English] [Korean] [Both]
```

### Required Input Collection
- **Mode A**: Request Results/Discussion file path
- **Mode B**: Request research topic, core hypotheses/objectives, methodology as text
- **Common**: Request Knowledge folder path (folder containing literature files)

Proceed to Stage 1 once specifications are collected.

---

## Stage 1: Blueprint (Structural Design)

### Execution Procedure
1. Read `references/core/stage1_blueprint.md` **completely** (no line limits)
2. Read `references/domain/enviro_scales.md`
3. **Mode A**: Read user's Results/Discussion file → Reverse-engineer topics, gaps, frameworks
4. **Mode B**: Analyze user-provided topic/objectives/methodology + scan 2-3 key files from Knowledge folder → Design structure
5. Generate Blueprint in XML-augmented markdown format

### Blueprint Output Format (mandatory)

```markdown
# INTRODUCTION BLUEPRINT

<blueprint_metadata>
- Input Mode: [A/B]
- Target Length: [selected value]
- Journal Tier: [selected value]
- Primary Novelty: [selected value]
- Spatiotemporal Scale: [spatial] / [temporal]
- Policy Connection: [relevant policy/SDGs/agreements]
</blueprint_metadata>

<topic_architecture>
├── Domain Context: [core domain]
├── Theoretical Frameworks: [theoretical foundations]
├── Methodological Background: [methodological context]
├── Knowledge Gap Area: [gap domain]
└── Application Context: [application context]
</topic_architecture>

<blueprint_p1>
## P1: BROAD CONTEXT
- Topic Focus: [grand challenge/system]
- Key Concepts: [3-5 concepts requiring external literature]
- Scope: [Global/Regional/System-specific]
- Literature Type Needed: [review papers, landmark studies, etc.]
</blueprint_p1>

<blueprint_p2>
## P2: DOMAIN NARROWING
- Topic Focus: [specific system/process]
- Background Elements: [existing understanding to establish]
- Current Knowledge: [what is known that sets up the gap]
- Literature Type Needed: [mechanistic studies, observational work, etc.]
</blueprint_p2>

<blueprint_p3>
## P3: KNOWLEDGE GAP
- Gap Type: [Empirical/Methodological/Theoretical/Scale]
- Why Gap Exists: [technical limitations/access/conceptual]
- Consequences: [what cannot be understood/predicted/managed due to this gap]
- Bridge Needed: [what would fill this gap]
</blueprint_p3>

<blueprint_p4>
## P4: THIS STUDY'S APPROACH
- Innovation Angle: [how the gap is addressed differently]
- Unique Capabilities: [what this approach enables]
- Positioning: [relationship to existing work — complementary/challenging/extending]
</blueprint_p4>

<blueprint_p5>
## P5: OBJECTIVES & STRUCTURE
- Research Questions: [core research questions]
- Hypothesis Space: [what is tested/explored]
- Scope Boundaries: [what is/is not examined]
</blueprint_p5>

<gap_framing_options>
- Option A: [problem-focused gap framing]
- Option B: [contradiction/resolution-focused gap framing]
- Option C: [scale-transfer gap framing]
</gap_framing_options>
```

### ★ User Approval Checkpoint ★

After outputting the Blueprint, **stop and request user confirmation**:
- "Please review the Blueprint. Let me know if any modifications are needed. Once approved, I will proceed to write the Introduction."
- If the user requests changes, revise the Blueprint and request approval again
- Proceed to Stage 2 only after user approval

---

## Stage 2: Generation (Introduction Writing)

### Execution Procedure
1. Read `references/core/stage2_generator.md` **completely**
2. Read **all files in the Knowledge folder**:
   - Use Glob to list files in the folder
   - Read each file with the Read tool (PDF files are supported natively)
   - Only if context is insufficient, switch to per-file summary then synthesis approach
3. Use the approved Blueprint as structural guide
4. Write the Introduction using only real citations extracted from Knowledge files
5. Apply environmental science-specific elements: refer to `references/domain/` files as needed

### Generation Output Format

```markdown
# INTRODUCTION

[Paragraph 1: Global Context — 4-6 sentences, CARS Move 1]

[Paragraph 2: Domain Synthesis — 5-7 sentences, CARS Move 1→2 transition]

[Paragraph 3: Knowledge Gap — 4-5 sentences, CARS Move 2]

[Paragraph 4: Study Approach — 4-5 sentences, CARS Move 3]

[Paragraph 5: Objectives — 3-4 sentences, CARS Move 3]

---
## Citation List
- [Actual citations extracted from Knowledge files]

## Blueprint Compliance
- P1 reflected: [Yes/Partial/No]
- P2 reflected: [Yes/Partial/No]
- P3 reflected: [Yes/Partial/No]
- P4 reflected: [Yes/Partial/No]
- P5 reflected: [Yes/Partial/No]
```

### User Review (optional)
- Present the Introduction to the user
- If the user wants immediate evaluation, proceed to Stage 3
- If revisions are requested, revise and re-present

---

## Stage 3: Evaluation (Quality Assessment)

### Mode Selection
Ask the user to select evaluation mode:

```
□ Quick evaluation: Core diagnostics only (Verdict + Rubric + Gap Test)
□ Full evaluation: Detailed diagnostics + structural revision plan + improved version
```

### Execution Procedure
1. Read `references/core/stage3_evaluator.md` **completely**
2. Use the Introduction generated in Stage 2 as the evaluation target
3. Perform evaluation according to the selected mode

### Quick Evaluation Output

```markdown
# EVALUATION — Quick

## A) Executive Verdict
- Judgment: [pass / borderline / revise-major]
- Gap summary: [1 sentence]
- Top 3 issues: [blocking issues]

## B) Diagnostic Rubric (0-5)
| Criterion | Score | Evidence |
|-----------|-------|----------|
| CARS Move 1 (territory) | | |
| CARS Move 2 (niche/gap) | | |
| CARS Move 3 (aims) | | |
| Funnel logic | | |
| Citation sufficiency | | |
| Gap clarity | | |

## C) Gap & Aim Quality
- Current gap statement (verbatim extract)
- Improved gap suggestions (2 variants)
- Current aim/hypothesis assessment
- Improved aim suggestions
```

### Full Evaluation Output
Quick evaluation content + the following additions:

```markdown
## D) Structure Surgery
- Keep / Cut / Move list
- Bridge sentences to add
- Revised paragraph structure proposal

## E) Content to Add
- 5-10 missing micro-content items (with placement, purpose, sentence templates)
- Evidence shopping list (search terms, study types)

## F) Improved Version
- Full improved Introduction (with structural fixes + gap strengthening + transition improvements)
```

### Follow-up Action Guidance
After evaluation, offer the user:
- "Shall I revise the Introduction based on the evaluation?" (re-run Stage 2)
- "Would you like to add more Knowledge files and regenerate?"
- "Shall we redesign from the Blueprint?" (re-run Stage 1)

---

## Quality Assurance

Requirements across all stages:
- Read reference prompts completely (no line limits)
- Use only real citations from Knowledge files (fabricated citations strictly prohibited)
- Follow CARS model (Swales, 1990) Move 1-2-3 structure
- Apply environmental science-specific elements (spatiotemporal scale, policy connection)
- Maintain XML tag format for inter-stage handoffs
- Always wait for user approval at checkpoints
- Use formal academic style, third person, appropriate hedging

## Resources

### references/core/
- `stage1_blueprint.md` — Stage 1 structural design core instructions
- `stage2_generator.md` — Stage 2 writing core instructions
- `stage3_evaluator.md` — Stage 3 evaluation core instructions

### references/templates/ (load on demand)
- `gap_statements.md` — Gap statement templates
- `opening_formulas.md` — Opening sentence formulas
- `objective_patterns.md` — Objective articulation patterns

### references/domain/ (environmental science specialization)
- `enviro_scales.md` — Spatiotemporal scale guide
- `policy_frameworks.md` — Policy & SDGs connection guide
- `journal_profiles.md` — Major environmental science journal profiles
