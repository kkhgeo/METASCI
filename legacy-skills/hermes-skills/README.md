# hermes-skills

**Generated — do not edit by hand.** Every file here comes from `skills/` via
`node tools/build-agent-skills.mjs`. Edit the skill in `skills/`, then rebuild.

Claude Code reads `skills/`; Hermes reads this. They stay in step because only
one of them is written by a person.

## What the build changes

| in `skills/` | here |
|---|---|
| `one **Agent tool** call per reviewer` | one **`delegation`** call per reviewer |
| `Agent tool` | the `delegation` toolset |
| `Task tool` | the `delegation` toolset |
| `WebSearch tool` | the `web` toolset |
| `WebFetch tool` | the `web` toolset |
| `WebSearch` | web search |
| `WebFetch` | web fetch |
| `Claude Code` | Hermes |
| `allowed-tools:` frontmatter | removed (Claude-only key) |
| `agents/openai.yaml` | dropped (Codex-only) |

`AskUserQuestion` is **not** substituted. It reads as a proper noun in the source, so
swapping in a noun phrase breaks the sentences around it. Instead each SKILL.md that
needs one gets a short "Hermes runtime notes" block after its frontmatter.

## Real runtime differences

Anything the table above cannot express goes in `agent-overrides/hermes/<skill>/`:

- `<file>.replace.json` — `[{"from": "...", "to": "..."}]`, applied to that file.
  Each `from` must match **exactly once** or the build fails, so an override cannot
  rot silently when the source changes.
- `<file>` — replaces the file outright. Use sparingly; a whole-file override is a
  fork by another name.
