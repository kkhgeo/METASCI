# codex-skills

**Generated — do not edit by hand.** Every file here comes from `skills/` via
`node tools/build-codex-skills.mjs`. Edit the skill in `skills/`, then rebuild.

Claude Code reads `skills/`; Codex reads this. They stay in step because only one
of them is written by a person.

## What the build changes

| in `skills/` | here |
|---|---|
| `Agent tool` / `Task tool` | `spawn_agent` |
| `WebSearch` / `WebFetch` | web search / HTTP fetch |
| `AskUserQuestion` | a numbered decision prompt |
| `Claude Code` | Codex CLI |
| `allowed-tools:` frontmatter | removed (Claude-only key) |
| no `agents/openai.yaml` | one is generated |

## Real runtime differences

Anything the table above cannot express goes in `codex-overrides/<skill>/`:

- `<file>.replace.json` — `[{"from": "...", "to": "..."}]`, applied to that file.
  Each `from` must match **exactly once** or the build fails, so an override
  cannot rot silently when the source changes.
- `<file>` — replaces the file outright. Use sparingly; a whole-file override is
  a fork by another name.
