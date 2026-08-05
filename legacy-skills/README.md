# legacy-skills

Retired skills. Kept for reference, **not loaded by anything** — this folder is
deliberately absent from `.claude-plugin/plugin.json`, so Claude Code ignores it.

These were the `skills/writing/` pack before the `metasci_*` packs replaced it.

| skill | status |
|---|---|
| `meta-writing` | superseded by `skills/metasci_writing/meta-writing` |
| `meta-rewriting` | superseded by `skills/metasci_writing/meta-rewriting` |
| `meta-review` | no successor — draft review against reference extractions |
| `meta-rewriting-antiai` | no successor — strips AI writing tells |
| `meta-rewriting-loop` | no successor — Monte Carlo multi-reference rewriting |
| `paper-proofreader` | superseded by `skills/metasci_writing/meta-proofreading` |
| `paper-proofreader_evidence` | superseded by `skills/metasci_writing/meta-proofreading-evidence` |

The first two share a name with their successors. Anything that flattens packs
into one directory must prefer the `skills/` copy — that is why this folder sits
outside `skills/` rather than inside it as another pack.

To bring one back, `git mv` it into a pack under `skills/` and add that pack to
the manifest if it is not already listed.
