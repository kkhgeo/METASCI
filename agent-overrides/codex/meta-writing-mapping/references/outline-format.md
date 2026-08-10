# Portable outline.md specification

Keep the complete composition map in one `outline.md`. It must remain usable on
another computer without access to the development kernel or the original skill
workspace.

## File structure

```markdown
# Outline — {working title}

- Core message: {one defensible sentence}
- Manuscript language: {language}
- Target venue: {venue or unknown}
- Last updated: YYYY-MM-DD

## Composition map

### Introduction

| ID | Function | Claim / question | Relation | Evidence | Core-message role |
|---|---|---|---|---|---|
| I1 | Background | ... | Start | ... | ... |

### Methods
...

## Evidence ledger

| ID | Direct support | Original location | Limits | Allocation | State |
|---|---|---|---|---|---|
| Fig. 2 | ... | figures/fig2... | ... | Results R2 | verified-original |

## Cross-section checks

- Question → answer:
- Methods ↔ Results:
- Abstract ↔ body:
- Scope discipline:

## Excluded material

| Item | Reason |
|---|---|

## Unresolved / Author decisions

| ID | Decision | Options | Consequence | Rule or constraint | Status |
|---|---|---|---|---|---|
```

## Paragraph-map fields

Every planned paragraph needs six fields:

- **ID**: stable section-prefixed identifier.
- **Function**: a functional tag, not a topic label.
- **Claim / question**: one sentence in the manuscript's target language.
- **Relation**: its logical relation to the preceding paragraph.
- **Evidence**: figure, table, dataset, source, or `⚠ no evidence`.
- **Core-message role**: how it advances, qualifies, or tests the core message.

Useful functional tags include:

- Introduction: `Background`, `Prior-work`, `Gap`, `Question`, `Purpose`,
  `Contribution`, `Scope`
- Methods: `Design`, `Setting`, `Sample`, `Procedure`, `Instrument`,
  `Analysis`, `Quality`, `Ethics`
- Results: `Overview`, `Finding`, `Comparison`, `Trend`, `Pattern`,
  `Robustness`, `Anomaly`
- Discussion: `Answer`, `Interpretation`, `Mechanism`, `Literature-context`,
  `Limitation`, `Implication`, `Future-work`, `Synthesis`

Useful relations include `Continuation`, `Contrast`, `Cause–effect`,
`Specification`, `Generalization`, `Sequence`, `Concession`,
`Problem–solution`, `Evidence–claim`, and `Question–answer`.

## Evidence states

- `verified-original`: checked against the original data, full text, or official
  metadata appropriate to the claim.
- `navigation-note`: derived from an extraction or summary and useful for locating
  evidence, but not yet authoritative.
- `unverified`: not checked or not available.

Never upgrade `navigation-note` to `verified-original` because it appears in
several derived notes. Reopen originals for load-bearing claims, quotations, scope
changes, or ambiguous summaries.

## Portability

Use relative paths where possible. Do not write machine-specific development
paths. Record enough source location information that another computer can
reconnect the outline to its project files.
