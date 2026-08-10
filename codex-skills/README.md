# codex-skills

**Generated — do not edit by hand.** Files here come from `skills/` plus any
runtime-specific `agent-overrides/codex/`, via `node tools/build-agent-skills.mjs`.
Edit those sources, then rebuild.

Claude Code reads `skills/`; Codex CLI reads this. They stay in step because only
one of them is written by a person.

## What the build changes

| in `skills/` | here |
|---|---|
| `one **Agent tool** call per reviewer` | one **`spawn_agent`** call per reviewer |
| `Agent tool` | `spawn_agent` |
| `Task tool` | `spawn_agent` |
| `WebSearch tool` | web search |
| `WebFetch tool` | HTTP fetch |
| `WebSearch` | web search |
| `WebFetch` | HTTP fetch |
| `Claude Code` | Codex CLI |
| `allowed-tools:` frontmatter | removed (Claude-only key) |
| no `agents/openai.yaml` | one is generated |

`AskUserQuestion` is **not** substituted. It reads as a proper noun in the source, so
swapping in a noun phrase breaks the sentences around it. Instead each SKILL.md that
needs one gets a short "Codex CLI runtime notes" block after its frontmatter.

## Real runtime differences

Anything the table above cannot express goes in `agent-overrides/codex/<skill>/`:

- `<file>.replace.json` — `[{"from": "...", "to": "..."}]`, applied to that file.
  Each `from` must match **exactly once** or the build fails, so an override cannot
  rot silently when the source changes.
- `<file>` — replaces the file outright, or adds a runtime-only file when the path
  does not exist in `skills/`. Use sparingly; replacement is a fork by another name.
