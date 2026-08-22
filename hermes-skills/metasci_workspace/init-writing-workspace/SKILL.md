---
name: init-writing-workspace
description: >
  Initialize an academic writing/manuscript project folder by generating
  CLAUDE.md and AGENTS.md instruction files that configure any AI agent
  (Hermes, Codex, Cursor, etc.) as a scholarly manuscript reviewer
  rather than a coding agent. Use this whenever the user starts a new
  writing or manuscript project, asks to "set up a writing workspace",
  "글쓰기 작업폴더 초기화", "이 폴더에 클로드 엠디 만들어줘", "원고 프로젝트
  세팅", "writing CLAUDE.md", or begins working on a paper/report in a
  folder that has no CLAUDE.md yet. Also use it to refresh or upgrade an
  existing writing-project CLAUDE.md to the current canonical version.
---

# Init Writing Workspace

Generates the canonical instruction files for an academic manuscript
workspace, so every writing project starts with the same reviewed-and-settled
agent configuration instead of a hand-copied, drifting one.

The canonical content lives in `assets/CLAUDE.md`. **Never rewrite its
content from memory** — always copy from the asset so all projects stay in
sync with the single source of truth.

## What it creates

In the target project root:

1. **`CLAUDE.md`** — copied verbatim from `assets/CLAUDE.md`.
2. **`AGENTS.md`** — same content, for agents that read the AGENTS.md
   convention (Codex, Cursor, and others). Generate it as an exact content
   copy of CLAUDE.md with one substitution: in prose, replace
   Claude-specific self-reference if any (the canonical text is already
   agent-neutral, so normally this is a pure copy).

The canonical text tells the agent to read `AGENT_communication.md` if that
file is present, but this skill never writes it. The author-dialogue rules
are owned by the sibling skill `init-communication-rules`; regenerating the
workspace leaves that file untouched.

Both files must be byte-identical in their instruction content. Do not let
them diverge; if the user asks for a project-specific rule, add it to BOTH
files in a clearly marked `## Project-Specific` section at the end, leaving
the canonical sections untouched.

## Procedure

1. Identify the target project root. If the user did not specify, ask —
   do not guess between candidate folders.
2. Check whether `CLAUDE.md` / `AGENTS.md` already exist there.
   - If neither exists: copy `assets/CLAUDE.md` to both filenames.
   - If either exists: show the user a diff between the existing file and
     the canonical asset, recommend whether to overwrite, merge, or keep
     (with your reasoning), and wait for the decision. If the existing file
     has a `## Project-Specific` section, always preserve it in the merge.
3. Do NOT create manuscript folders, archive folders, or any other
   structure — folder layout is decided per project by the user. The
   instruction files themselves tell the agent to create a `_review/`
   folder at review time; that is sufficient.
4. Confirm completion by listing the files created and reminding the user
   in one sentence what the configuration does (scholarly reviewer mode,
   ledger-based completeness, recommendation-with-approval).

## Updating the canonical content

If the user wants to change the shared rules themselves (not a
project-specific addition), edit `assets/CLAUDE.md` inside this skill,
then offer to re-run the init on their active projects so they pick up
the new version.
