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
  language. Explain edits in the user's language. A Korean passage is rewritten in
  Korean and diagnosed against the Korean register, not against English norms.
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
- `references/section-checklists.md` when the manuscript section is known. Its
  `문장 스타일 공통` and `인용·참고문헌 규범` blocks are section-independent and
  apply even when the section cannot be identified.
- `references/korean-register.md` **only when the source passage is Korean**. It
  names the English-only checks to drop, gives the Korean surface forms of the
  same diagnoses, and bars over-correcting the Korean academic register. Do not
  open it for an English passage: its "normal range" statements are false for
  English prose.

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

Cutting is not the only repair. Where the diagnosis finds a logical gap, an
unsupported claim, or a missing element the section requires, the revision may
**add** the sentence that closes it. Two limits, both absolute: never invent a
data point, a citation, a figure or table number, or a numeric magnitude; and
where the added sentence needs evidence the passage does not contain, write it
with an explicit `[author confirm: …]` marker in place of that evidence rather
than supplying it. An addition is a substantive change — disclose it under
consequential edits, and classify it `unsupported` until the author verifies it.

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
- remove redundancy, throat-clearing, and empty metadiscourse;
- reduce nominalization where a concrete actor and verb are available, subject to
  the register brake below;
- keep parallel structures parallel;
- repair reference chains and given-to-new progression;
- vary sentence form only where it improves reading;
- avoid polishing that erases the author's technical distinctions or voice.

**Over-correction brakes.** These are refuted as general rules; do not apply them:

- *"Subject and verb must be adjacent; any intervening material is a burden."*
  Short interruptions cost the reader nothing. Flag long ones only.
- *"Add connectives to improve flow."* Cohesion is not coherence. Cohesive ties
  are surface devices and do not make an incoherent argument coherent. Repair the
  logic first; add a connective only where the relation it names is already true.
- *"Correct the sentence to standard form."* Two equally grammatical sentences
  carry different value depending on placement and information structure. Judge a
  sentence in its discourse context, not by grammar in isolation.
- *"Prefer the active voice."* Not when the passive puts established information
  first. For a Korean passage, see `korean-register.md` §A — passive share,
  nominalization, Sino-Korean vocabulary and complex sentences all sit inside the
  normal range of that register and must not be flagged against English norms.

These matter more, not less, as the target moves toward a maximally polished
paragraph. A reviewer pushed toward perfection over-corrects, and over-correction
is the one defect the author cannot see.

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
5. **Checks run** — name the checklist blocks actually applied and their result, so
   that a block skipped for lack of section context is visible rather than silently
   absent. A check that cannot be settled from the supplied passage alone is marked
   unresolved with the reason; it is never reported as passed. For a Korean passage
   this list comes from `korean-register.md` §B and carries one further entry: that
   §A was respected.

### Alternatives

Label the difference, not quality tiers. When alternatives are warranted, order
them on one axis — **how much of the original survives** — and take as many
consecutive rungs as the request needs, starting from the top:

| Rung | Changes | Survives from the original |
|---|---|---|
| `Minimal` | wording, referents, hedging | the sentences and their order |
| `Reordered` | sentence order, merges, splits | the sentences |
| `Restructured` | the argument's structure | the content elements |
| `Rewritten` | everything | the intended meaning |

One axis beats mixed labels: `Claim-first` and `More cautious` answer different
questions, so a reader cannot tell which is the more conservative choice. Do not
let adjacent rungs collapse into each other — if `Reordered` reads as `Minimal`
with two commas moved, the set offers one option twice.

Each version must independently pass the preservation check. This does not make
alternatives mandatory: the Modes section still governs whether to produce any.

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
