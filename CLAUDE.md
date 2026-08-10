# METASCI — Claude Code Project Instructions

## Project Overview

A personal Claude Code skill collection in two domains:
- **Academic research** — extracting knowledge, analyzing structure/logic/vocabulary/style from research papers (PDF), academic writing, and multi-reviewer proofreading.
- **Dialogue personas** — guided explanation (Virgil, Beatrice, Socrates), creative visual direction (Picasso), and teach-back comprehension (Feynman digest).

Distributed as a Claude Code plugin named `metasci` (see `.claude-plugin/plugin.json`).

## Skill Architecture

Skills live under `skills/` in four packs. Each skill is a directory with `SKILL.md` plus optional `references/`, `scripts/`, `templates/`.

```
skills/
├── persona/             # dialogue / explanation personas
│   ├── virgil/              # adaptive incremental explanation (segment-by-segment)
│   ├── beatrice/            # one-shot complete explanation (sister to virgil)
│   ├── socrates/            # Socratic maieutic dialogue
│   ├── picasso/             # visual director → image-generation prompts
│   └── feynman-digest/      # Teach-Back comprehension digest
├── metasci_writing/     # academic writing, rewriting, multi-reviewer proofreading
│   ├── meta-writing/
│   ├── meta-writing-mapping/
│   ├── meta-writing-blog/
│   ├── meta-mywriting-korean/
│   ├── meta-rewriting/
│   ├── meta-proofreading/
│   └── meta-proofreading-evidence/
├── metasci_extraction/  # PDF → structured analysis layers, style transfer
│   ├── extraction-knowledge/
│   ├── extraction-logic/
│   ├── extraction-vocab/
│   ├── metasci-style-extraction/
│   └── meta-styling/
└── metasci_slide/       # talk narrative → house-style deck
    ├── meta-slide-content/
    └── meta-slide-design/

codex-skills/            # GENERATED Codex build — do not hand-edit
hermes-skills/           # GENERATED Hermes build — do not hand-edit
agent-overrides/         # the few places a build must differ beyond vocabulary
legacy-skills/           # superseded; NOT in the manifest, never loaded
```

The plugin manifest registers the four `skills/` packs in its `skills` array, so each skill loads as `skills/<pack>/<name>/SKILL.md`. `legacy-skills/` and the generated builds are deliberately outside that array.

## Per-runtime builds

`skills/` is the only hand-written copy. The other sets are produced from it:

```
node tools/build-agent-skills.mjs           rebuild both
node tools/build-agent-skills.mjs --check   exit 1 if a committed build is stale
```

Each profile translates the runtime's tool vocabulary, drops the Claude-only `allowed-tools` frontmatter key, and adds a short "runtime notes" block to any SKILL.md that needs one. The tool names were read off the installed runtimes, not assumed:

| in `skills/` | codex | hermes |
|---|---|---|
| `Agent tool` / `Task tool` | `spawn_agent` | `delegation` toolset |
| `WebSearch` / `WebFetch` | web search / HTTP fetch | `web` toolset |
| `AskUserQuestion` | no equivalent — numbered list in the message | `clarify` toolset |
| `Claude Code` | Codex CLI | Hermes |
| `agents/openai.yaml` | generated if absent | dropped (Codex-only) |

`AskUserQuestion` is never substituted inline. It reads as a proper noun, so a noun phrase in its place breaks the surrounding sentences ("offered as a numbered decision prompt options"). The runtime-notes block carries it instead.

This replaced a hand-maintained `meta-proofreading-codex`. Comparing that fork against its source found 18 differing files of which only 2 differed for runtime reasons — the rest had simply gone stale, and the fork was missing `agents/agent_j.md` (the judge) and a whole writing-manual chapter. Generation is what keeps that from recurring.

Anything the vocabulary table cannot express belongs in `agent-overrides/<profile>/<skill>/<file>.replace.json` as `[{from, to}]`. Each `from` must match exactly once or the build fails, so an override cannot rot silently when the source moves on. A whole file at `agent-overrides/<profile>/<skill>/<file>` replaces the generated path, or adds a runtime-only path when the shared source has none.

## Installing on a machine

`tools/install-skills.mjs --apply` points each runtime at its own build: symlinks into `~/.claude/skills` and `~/.codex/skills`, and Hermes' `skills.external_dirs` config. Links mean `git pull` is the whole update path. `--replace` additionally converts shadowing real directories into links, backing them up under `~/.metasci/replaced-skills/` first.

## Key Conventions

- **Manifest**: the only manifest Claude Code reads is `.claude-plugin/plugin.json`. There is no top-level `plugin.json`. When adding a new skill under a new category folder, add that folder to the manifest `skills` array.
- **References**: research skills carry a `references/` folder with detailed templates — MUST be read before execution.
- **Output folders** (research skills): `{SkillType}_{topic}/` (e.g. `Knowledge_isotopes/`, `Style_geochemistry/`, `Logic_ecology/`).
- **Source tracing**: extracted items carry source tags (`[EX#N-SECTION]` for meta-styling, `[P#-S#]` for logic/vocab).
- **PDF reading**: the LLM reads PDFs directly — no preprocessing pipelines.
- **Language**: skill instructions are in English for LLM accuracy; user-facing triggers and output include Korean.
- **Parallel processing**: multiple papers can be processed concurrently via Task (Subagent).

## Analysis Layer Separation (extraction skills)

```
extraction-vocab      → WHAT words are used        (lexical inventory)
meta-styling          → HOW words are used          (stylistic patterns)
extraction-logic      → HOW arguments are structured (rhetorical flow)
extraction-knowledge  → WHAT knowledge is cited      (epistemic content)
```

## Typical Workflows

### Full paper analysis
1. `extraction-knowledge` → extract cited knowledge
2. `extraction-vocab` → build word inventory + technical glossary
3. `extraction-logic` → map argument structure + sentence frames
4. `meta-styling` (Mode A) → extract stylistic patterns

### Academic writing
1. `meta-writing` → draft sections using Knowledge + PDF + Web
2. `meta-review` / `paper-proofreader*` → multi-reviewer improvement and proofreading
3. `meta-styling` (Mode B) → revise draft to match target journal style
4. `meta-rewriting` → one-shot style transfer from reference paper

### Data-driven discovery
1. `agentic-research` → iterative cycles of data analysis + literature search
2. World model tracks hypotheses, findings, and evidence across cycles
3. Final traceable report with code/literature citations

### Explanation & comprehension (persona)
- `virgil` for step-by-step guidance, `beatrice` for a complete one-shot answer, `socrates` for question-driven inquiry, `feynman-digest` to verify understanding via teach-back, `picasso` for visual/image-prompt direction.
