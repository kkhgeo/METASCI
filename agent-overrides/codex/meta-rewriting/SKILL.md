---
name: meta-rewriting
description: >
  Review and rewrite academic paragraphs for logic, clarity, concision, cohesion,
  claim calibration, and source fidelity. Use when the user provides a paragraph
  or passage and asks to rewrite it, improve its logic, or reduce academic/AI
  awkwardness. Preserve the author's meaning, data, citations, and language unless
  the user explicitly authorizes a change. Not for full-manuscript proofreading,
  composition mapping, style transfer, or drafting from evidence.
---

# Meta Rewriting

Improve an existing academic passage without changing what the evidence can support.

## Runtime contract

- Work only within the scope the user identifies. If the user supplies several
  paragraphs and asks to revise all of them, do not silently process only the first.
- Use the source language unless the user asks for translation or a different target
  language. Explain edits in the user's language.
- Do not depend on an external kernel directory. The operative Codex rules are
  bundled in `references/codex-*.md`.
- Preserve citation strings, numerical values, variable names, defined terms, and
  cross-references exactly unless a correction is explicitly authorized.
- Do not claim that a fact or citation was verified unless it was checked against
  an appropriate original or official source.

## Required references

Read before rewriting:

1. `references/codex-kernel-index.md`
2. `references/rule-routing.md`
3. `references/principles.md`

Then read the relevant parts of:

- `references/codex-process.md`
- `references/codex-paragraph-logic.md`
- `references/codex-section-structure.md`
- `references/codex-ai-era.md`
- `references/section-checklists.md` when the manuscript section is known.

## Precedence

Apply constraints in this order:

1. source fidelity, research integrity, and the author's intended meaning;
2. current official venue or reporting requirements;
3. explicit user instructions for this passage;
4. Codex kernel rules;
5. local rewriting principles and examples;
6. stylistic preference.

A fluent sentence is not an improvement if it strengthens a claim, changes a causal
relation, alters a number, invents a source, or obscures uncertainty.

## Modes

Infer the mode from the request:

- **Direct rewrite**: return the best defensible revision with minimal commentary.
- **Review + rewrite**: diagnose the passage, revise it, and explain consequential
  edits.
- **Alternatives**: provide distinct versions only when the user requests them or
  when two or more materially different rhetorical choices are genuinely useful.
- **Diagnosis only**: explain problems without changing the text.

Do not force three alternatives. The original may be the best version.

## Workflow

### 1. Freeze protected content

Before editing, identify:

- the passage's main claim and intended rhetorical function;
- data, numbers, units, signs, ranges, and statistical notation;
- citations and source-attribution boundaries;
- hedges, limitations, and uncertainty;
- terminology, variable names, and cross-references;
- meaning-changing ambiguities that require author confirmation.

If the intended meaning is ambiguous and competing interpretations would produce
different claims, ask one focused question before rewriting. Otherwise choose the
narrowest defensible interpretation and flag it.

### 2. Diagnose globally before locally

Read the whole supplied scope before editing sentences. Check:

1. Is there one controlling point or a justified sequence of points?
2. Does each sentence perform a necessary function?
3. Are claim, evidence, reasoning, and qualification connected?
4. Does information progress from established context to new information?
5. Are paragraph boundaries and transitions earned?
6. Is claim strength proportional to the evidence stated in the passage?

Use the deletion test: if removing a sentence loses no claim, evidence, reasoning,
qualification, or transition, remove or merge it.

### 3. Audit source and verification status

Classify load-bearing content as:

- `verified-original`: checked against original data, full text, or official
  metadata appropriate to the claim;
- `provided-unverified`: supplied by the user but not independently checked;
- `navigation-note`: derived from a summary or extraction;
- `unsupported`: introduced without an identifiable basis.

Rewriting alone does not upgrade verification status. Never invent a citation or
fact to make a paragraph sound complete. If verification is outside the request,
preserve provided content and mark any consequential uncertainty briefly.

### 4. Revise in two passes

**Pass A — logic**

- select or preserve a clear controlling sentence;
- order sentences by rhetorical function;
- connect evidence to the exact claim it supports;
- separate observation, interpretation, and implication;
- calibrate causal, universal, novelty, and certainty language;
- split or merge paragraphs only when the argument requires it.

**Pass B — expression**

- prefer precise verbs and concrete subjects;
- remove nominalization, redundancy, throat-clearing, and empty metadiscourse;
- keep parallel structures parallel;
- repair reference chains and given-to-new progression;
- vary sentence form only where it improves reading;
- avoid polishing that erases the author's technical distinctions or voice.

### 5. Run the preservation diff

Compare original and revision for:

- claim scope and direction;
- causal versus associative wording;
- numbers, units, and statistical notation;
- citation placement and attribution;
- negation, modality, and hedging;
- technical terms and referents;
- added or deleted substantive content.

Any substantive change must be either reverted or explicitly disclosed. If it
requires author judgment, do not bury it inside the rewritten paragraph.

### 6. Decide whether rewriting helped

Prefer the revision only if it improves logic or readability without a preservation
failure. Otherwise keep the original and say why. Do not create churn merely to
demonstrate activity.

## Output contracts

### Direct rewrite

Return the revised passage first. Add a short note only for an unresolved ambiguity,
unverified load-bearing claim, or authorized substantive change.

### Review + rewrite

Use the smallest useful structure:

1. **Diagnosis** — the one or two highest-impact issues.
2. **Revision** — the best defensible passage, or **Keep original**.
3. **Consequential edits** — only meaning, scope, verification, or structure changes.
4. **Preservation check** — numbers/citations/claim scope preserved or exceptions named.

### Alternatives

Label the rhetorical difference, not quality tiers. Examples: `Claim-first`,
`Evidence-first`, or `More cautious`. Each version must independently pass the
preservation check.

### Diagnosis only

Name the passage's controlling point, sentence functions, and highest-impact defect.
Do not supply a rewrite unless requested.

## Boundaries

- For several manuscript sections or a full paper, use `meta-proofreading`.
- For deciding paragraph order before prose exists, use `meta-writing-mapping`.
- For drafting claims from figures, tables, data, and literature, use
  `meta-writing`.
- For transferring a measured style profile, use `meta-styling`.
- For external phrase attestation or citation checking, use
  `meta-proofreading-evidence`.
