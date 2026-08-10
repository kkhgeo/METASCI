---
name: meta-writing-mapping
description: >
  Diagnose and design an academic manuscript's composition before prose drafting:
  sections, paragraph functions, order, transitions, and evidence allocation.
  Use with no draft, an existing draft, or one named section. Triggers include
  "구성 잡아줘", "구조 잡아줘", "문단 배치", "목차 짜자", "구성 매핑",
  and "outline". Do not use for sentence correction, paragraph rewriting,
  style transfer, or full prose drafting.
---

# Meta Writing Mapping

Design the manuscript's argument architecture. Produce or revise one portable
`outline.md`; do not draft manuscript prose.

## Runtime contract

- Work from the files the user placed in scope. Inspect the workspace before asking
  for information that can be discovered locally.
- Do not depend on an external development-kernel directory during use.
  The operative kernel rules are bundled under `references/codex-*.md`.
- Explain findings in the user's language. Keep manuscript-language topic sentences
  in the manuscript's target language.
- If a source or venue instruction is time-sensitive, verify the current official
  source before treating it as binding.
- Ask only one material decision at a time. If an interactive choice tool is
  unavailable, state the decision plainly and wait; do not hide substantive
  content inside numbered choices.

## Scope boundary

| This skill does | Route elsewhere |
|---|---|
| Select section and paragraph functions | Draft prose: `meta-writing` |
| Allocate figures, tables, data, and literature | Rewrite a paragraph: `meta-rewriting` |
| Diagnose missing or misplaced moves | Correct sentences: `meta-proofreading` |
| Record unresolved structural decisions | Apply style: `meta-styling` |

## Required references

Read before analysis:

1. `references/codex-kernel-index.md`
2. `references/rule-routing.md`
3. `references/outline-format.md`

Then read only the relevant portion of:

- `references/codex-process.md`
- `references/codex-paragraph-logic.md`
- `references/codex-section-structure.md`
- `references/section-checklists.md`
- `references/structural-integrity.md`

## Precedence

Apply constraints in this order:

1. source fidelity, research integrity, and non-fabrication;
2. current official venue or reporting requirements;
3. explicit study design and available evidence;
4. bundled Codex kernel rules;
5. local structural heuristics and examples;
6. author preference.

Author preference may override a rhetorical default, but never silently justify
invented evidence, unsupported claims, or a venue violation. Record any deliberate
exception in `outline.md` under **Unresolved / Author decisions**.

## Workflow

### 1. Inspect and classify

Inspect `outline.md`, drafts, figures, tables, data, literature folders, and venue
instructions. Infer one of three modes without asking the user to name it:

- **Blank map**: evidence exists but no usable draft.
- **Draft diagnosis**: prose exists and its architecture must be reconstructed.
- **Section repair**: one section is named; load the whole outline for context, then
  edit only that section unless a cross-section dependency requires more.

### 2. State the first diagnosis

Lead with:

- what is present;
- what is missing, duplicated, or misplaced;
- the single decision that would most change the map.

Tie each diagnosis to a named rule or observable evidence. Do not offer vague advice.

### 3. Establish the core message

Write one defensible sentence stating what the manuscript can claim from the
available evidence. If evidence supports several materially different messages,
present the alternatives and obtain the author's choice before building the map.

### 4. Build the evidence ledger

For each figure, table, dataset, and load-bearing literature source, record:

- what it directly supports;
- its location or identifier;
- limits on interpretation;
- candidate section and paragraph;
- verification state: `verified-original`, `navigation-note`, or `unverified`.

Extraction notes help navigation but are not evidence authority. Reopen the original
source for load-bearing claims, scope changes, quotations, or when notes are
incomplete or ambiguous.

### 5. Map paragraph functions

For every planned paragraph specify:

- functional tag;
- one-sentence claim or question;
- relation to the previous paragraph;
- evidence allocation;
- contribution to the core message.

No paragraph is justified solely by topic. Missing evidence is a structural defect:
mark it `⚠ no evidence`; do not fill it with plausible prose.

### 6. Run cross-section checks

At minimum verify:

- the Introduction's question is answered by the Results and Discussion;
- every reported result has a corresponding method, and vice versa;
- the Abstract contains no claim absent from the body;
- Results reports findings without literature comparison or interpretation;
- Discussion interprets results without becoming a second Results section;
- Conclusion introduces no new evidence;
- claim breadth matches the study population, design, and data.

### 7. Resolve by impact

Surface at most three issues at a time, ordered by downstream impact. When more
issues remain, store them in `outline.md` and report the count. Do not mistake
search effort or reviewer agreement for evidence strength.

### 8. Write and verify `outline.md`

Use `references/outline-format.md`. Before completion confirm:

- every paragraph has a function, claim, relation, evidence, and core-message role;
- every major evidence item is allocated or explicitly excluded;
- all exceptions and unresolved decisions are recorded;
- the file is self-contained and portable.

## Output behavior

Return a compact summary of the structural change, the most consequential unresolved
decision, and the path to `outline.md`. Do not draft manuscript sentences unless
the user explicitly switches to a prose-writing skill.
