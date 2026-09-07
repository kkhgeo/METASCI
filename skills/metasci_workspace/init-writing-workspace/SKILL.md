---
name: init-writing-workspace
description: >
  Initialize an academic writing/manuscript project folder by generating
  CLAUDE.md and AGENTS.md instruction files that configure any AI agent
  (Claude Code, Codex, Cursor, etc.) as a scholarly manuscript reviewer
  rather than a coding agent. Use this whenever the user starts a new
  writing or manuscript project, asks to "set up a writing workspace",
  "글쓰기 작업폴더 초기화", "이 폴더에 클로드 엠디 만들어줘", "원고 프로젝트
  세팅", "writing CLAUDE.md", or begins working on a paper/report in a
  folder that has no CLAUDE.md yet. Also use it to refresh or upgrade an
  existing writing-project CLAUDE.md to the current canonical version.
---

# Init Writing Workspace

Installs the manuscript layer of a research workspace: one marker-delimited
block in `CLAUDE.md`, mirrored in `AGENTS.md`, that turns the agent into a
scholarly manuscript reviewer — manuscript-order findings, ledger-based
completeness, `_review/` discipline. The block specialises the
research-principles block installed by `init-research-principles` and sits
directly below it; a folder that has no principles block gets one from that
skill's asset as part of this install.

Canonical content lives in `assets/CLAUDE.md`. **Never rewrite it from
memory** — copy it verbatim, marker comments included.

The two blocks point at companion files if they are present
(`AGENT_communication.md` and `AGENT_figures.md` from the principles block,
`AGENT_review_lessons.md` from this one) but this skill writes none of them.
They are owned by `init-communication-rules`, `init-figure-rules`, and
`init-review-lessons`; regenerating the workspace leaves them untouched.

## How blocks share one file

`CLAUDE.md` is made of blocks, each owned by one skill and delimited by
`<!-- metasci:<name> vN -->` … `<!-- /metasci:<name> -->`. A skill creates,
replaces, or removes only its own block. It never edits another skill's
block, and never edits anything outside the markers — the author's own
text, including a `## Project-Specific` section at the end. Because of
this, the order in which the skills are run does not change the result:
the principles block always lands first, this block after it.

## Procedure

1. Identify the target project root. If the user did not specify, ask —
   do not guess between candidate folders.
2. **Principles block first.** Check `CLAUDE.md` for
   `<!-- metasci:research-principles`. If it is missing, install it from
   the sibling skill's asset, `../init-research-principles/assets/CLAUDE.md`
   relative to this skill's folder, following that skill's procedure (top
   of the file). If the sibling skill is not installed, say so, continue
   with this block alone, and recommend installing `init-research-principles`.
3. **`CLAUDE.md`.**
   - Absent: write the principles asset, one blank line, then this asset.
   - Present, this block absent: insert this asset directly after the
     principles block — one blank line after its closing marker — and
     before anything else. Leave the rest untouched.
   - Present, this block present, same version: leave it.
   - Present, this block present, older version: replace what lies between
     the markers, markers inclusive, with the asset. If the block was
     hand-edited, show the diff first and wait for the decision.
   - Present as the pre-block canonical text — first line
     `# CLAUDE.md — Academic Manuscript Workspace` and no `<!-- metasci:`
     marker anywhere — this is v1. Show the diff between that text and the
     two blocks, recommend replacing the whole canonical text with the two
     blocks, and wait. A `## Project-Specific` section, if present, stays
     below the blocks exactly as written.
4. **`AGENTS.md`.** Make it identical to `CLAUDE.md`. Absent: create it as
   a copy. Present and differing outside the blocks: apply the same block
   changes only, then show the remaining difference and recommend which
   file to align to; the two must not drift.
5. Do NOT create manuscript folders, archive folders, or any other
   structure — folder layout is decided per project by the user. The block
   itself tells the agent to create `_review/` at review time.
6. Confirm completion by listing the files created or changed and
   reminding the user in one sentence what the configuration does
   (research principles first, then scholarly reviewer mode with
   ledger-based completeness and recommendation-with-approval).

## Project-specific rules

Anything the author wants for one project goes in a `## Project-Specific`
section at the end of both files, outside every marker block, added to
BOTH files. Skills never touch it.

## Updating the canonical content

If the user wants to change the shared rules themselves (not a
project-specific addition), edit `assets/CLAUDE.md` inside this skill,
bump the version in its opening marker, rebuild the generated trees
(`node tools/build-agent-skills.mjs`), then offer to re-run the init on
their active projects so they pick up the new version. Rules that hold for
analysis and modelling folders too belong in `init-research-principles`,
not here.
