# Rule routing for meta-writing-mapping

This file is the application layer between the bundled Codex kernel and the
mapping workflow. All paths are local to this skill; no other installed skill and
no development directory is required at runtime.

## Load order

1. `codex-kernel-index.md` — enabled rule inventory and provenance.
2. `codex-process.md` — evidence-first workflow and scope control.
3. `codex-paragraph-logic.md` — paragraph function and progression.
4. `codex-section-structure.md` — section-specific architecture.
5. `structural-integrity.md` and `section-checklists.md` — local diagnostic detail.
6. `outline-format.md` — persistent output contract.

## Decision routing

| Decision | Primary reference | Secondary reference |
|---|---|---|
| What can be claimed from available material? | `codex-process.md` | evidence ledger in `outline-format.md` |
| What function does each paragraph serve? | `codex-paragraph-logic.md` | `section-checklists.md` |
| Which moves belong in a named section? | `codex-section-structure.md` | `section-checklists.md` |
| Do sections answer one another? | `structural-integrity.md` | cross-section checks in `SKILL.md` |
| How is the decision saved? | `outline-format.md` | — |

## Conflict resolution

Apply, in order:

1. source fidelity and research integrity;
2. current official venue requirements;
3. explicit study design and available evidence;
4. Codex kernel rules;
5. local heuristics and examples;
6. author preference.

A venue-specific limit overrides a generic word-count example. A reporting
guideline may require a move that a generic section model omits. Examples are
illustrations, not templates or quotas.

Author preference may select among defensible rhetorical options. It does not turn
an unsupported claim into a supported one. Record a deliberate exception and its
reason rather than silently changing the rule.

## Diagnostic language

Name the rule and the observable consequence.

Good: “The Introduction lacks an explicit gap move, so the purpose paragraph has no
demonstrated necessity.”

Weak: “The flow could be improved.”

Report at most three active issues. Save the remainder in the unresolved ledger.
