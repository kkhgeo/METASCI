# legacy-skills

Retired skills. Kept for reference, **not loaded by anything** — this folder is
deliberately absent from `.claude-plugin/plugin.json`, so Claude Code ignores it.

These were the `skills/writing/` and `skills/research/` packs.

From `writing/` — the `metasci_*` packs replaced it:

| skill | status |
|---|---|
| `meta-writing` | superseded by `skills/metasci_writing/meta-writing` |
| `meta-rewriting` | superseded by `skills/metasci_writing/meta-rewriting` |
| `paper-proofreader` | superseded by `skills/metasci_writing/meta-proofreading` |
| `paper-proofreader_evidence` | superseded by `skills/metasci_writing/meta-proofreading-evidence` |

**Un-retired 2026-08-10** — `meta-review`, `meta-rewriting-antiai`, and
`meta-rewriting-loop` moved back into `skills/metasci_writing/`. The shipped
skills route to them by name (`meta-rewriting` sends multi-reference work to
`meta-review`, AI-trace removal to `meta-rewriting-antiai`, Monte Carlo
optimisation to `meta-rewriting-loop`), so leaving them here made those routes
dead on any machine that installed from this repo.

From `research/`:

| skill | status |
|---|---|
| `agentic-research` | retired — autonomous data-driven research loop |

`agentic-research` also has unresolved internal references
(`references/domain_materials.md`, `references/domain_omics.md`,
`scripts/validate_claims.py`), so it would not have run end to end as shipped.

The first two share a name with their successors. Anything that flattens packs
into one directory must prefer the `skills/` copy — that is why this folder sits
outside `skills/` rather than inside it as another pack.

To bring one back, `git mv` it into a pack under `skills/` and add that pack to
the manifest if it is not already listed.
