# Provenance

This folder ships with the `meta-writing` skill so the manual travels with the
skills and resolves on any machine.

**Editing source:** `Z:\KKH_Research\META_SCI\claude_writing_manual\` — the build
directory where the corpus work happens (`Writing_Principles_Extraction/by-source/`
→ `bank/` → here). Edit there, then copy the folder over this one.

Nothing else in the skills reads the `Z:` path. Reach this folder by relative path:

| From | Path |
|---|---|
| `meta-writing/SKILL.md` | `references/claude_writing_manual/` |
| `meta-writing/references/*.md` | `claude_writing_manual/` |
| `meta-writing-mapping/references/rule-routing.md` | `../../meta-writing/references/claude_writing_manual/` |
| `meta-proofreading/writing-manual/INDEX.md` | `../../meta-writing/references/claude_writing_manual/` |

**Co-installation requirement:** the two skills above resolve the manual only
when `meta-writing` is installed beside them. Installing either alone breaks
the reference — install `meta-writing` with them.

`meta-rewriting` no longer reads this folder — since 2.3.0 (2026-08-18) it
bundles its own subset copy (`meta-rewriting/references/manual/`, files 00–07 +
DECISIONS). When this folder is refreshed from the editing source, re-copy that
subset too (its `_SOURCE.md` records the rule).

Those hold in the repo layout (`skills/metasci_writing/<skill>/`) and in the
installed layout (`~/.claude/skills/<skill>/`) alike.
