<!-- owner: codex; generated: true; do-not-edit: true -->
# Codex Writing Rules — meta-rewriting

This skill-facing projection was generated from `codex_scientific_writing_kernel`.
Do not edit it directly. Update `rules/` or `routing/skill-routes.yaml`, then rebuild.

## Role and boundary

- **Role:** Diagnose and rewrite existing paragraphs for logic and clarity while preserving meaning.
- **Boundary:** Do not invent facts or guarantee factual fidelity without verification tools; return unverified items to the author.

## Conditional loading

Read only the files relevant to the requested operation and section. Do not load every rule at once.
Apply each rule together with its conditions and exceptions. Use `conflicts/conflicts.yaml` to resolve conflicts.

| Domain | File | Rules |
|---|---|---:|
| process | [codex-process.md](codex-process.md) | 1 |
| paragraph-logic | [codex-paragraph-logic.md](codex-paragraph-logic.md) | 6 |
| section-structure | [codex-section-structure.md](codex-section-structure.md) | 6 |
| ai-era | [codex-ai-era.md](codex-ai-era.md) | 1 |
