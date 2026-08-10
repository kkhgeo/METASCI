<!-- owner: codex; generated: true; do-not-edit: true -->
# Codex Writing Rules — meta-writing-mapping

This skill-facing projection was generated from `codex_scientific_writing_kernel`.
Do not edit it directly. Update `rules/` or `routing/skill-routes.yaml`, then rebuild.

## Role and boundary

- **Role:** Design the argumentative structure of manuscripts and sections.
- **Boundary:** Do not load lexical, grammatical, or surface-style rules that require finished sentences.

## Conditional loading

Read only the files relevant to the requested operation and section. Do not load every rule at once.
Apply each rule together with its conditions and exceptions. Use `conflicts/conflicts.yaml` to resolve conflicts.

| Domain | File | Rules |
|---|---|---:|
| process | [codex-process.md](codex-process.md) | 2 |
| paragraph-logic | [codex-paragraph-logic.md](codex-paragraph-logic.md) | 2 |
| section-structure | [codex-section-structure.md](codex-section-structure.md) | 5 |
