---
name: init-research-principles
description: >
  Use when a research folder — data analysis, modelling, figures, or a
  manuscript — should carry the top-level working rules that every other
  workspace rule specialises: the author says "연구 원칙 설치", "연구 원칙
  깔아줘", "카파시 규칙 넣어줘", "init research principles", or starts a new
  analysis or modelling folder that has no CLAUDE.md yet. Also use to
  refresh the block to the current version or to remove it. Sibling of
  init-writing-workspace, whose block sits below this one in the same
  CLAUDE.md.
---

# Init Research Principles

Installs the top layer of a research workspace: one marker-delimited block
at the head of `CLAUDE.md`, mirrored in `AGENTS.md`, holding the rules that
apply to every kind of research work — assumptions first, the simplest
sufficient approach, surgical changes, verifiable completion, and the
general rules for dealing with the author and with files. Blocks installed
by sibling skills (init-writing-workspace today) sit below it and specialise
it for one kind of work.

Canonical content lives in `assets/CLAUDE.md`. **Never rewrite it from
memory** — copy it verbatim, marker comments included. On its own it is a
complete `CLAUDE.md`; next to other blocks it is the first of them.

## How blocks share one file

`CLAUDE.md` is made of blocks, each owned by one skill and delimited by
`<!-- metasci:<name> vN -->` … `<!-- /metasci:<name> -->`. A skill creates,
replaces, or removes only its own block. It never edits another skill's
block, and never edits anything outside the markers — the author's own
text, including a `## Project-Specific` section at the end. Because of
this, the order in which the skills are run does not change the result:
this block always lands first, the writing block after it.

## Procedure

1. Identify the target project root. If unclear, ask — do not guess.
2. **`CLAUDE.md`.**
   - Absent: write `assets/CLAUDE.md` as the file.
   - Present, this block absent: insert the asset at the very top of the
     file, followed by one blank line, and leave the rest untouched.
   - Present as the pre-block writing text — first line
     `# CLAUDE.md — Academic Manuscript Workspace` and no `<!-- metasci:`
     marker anywhere — this is init-writing-workspace v1, which already
     states most of these rules in its own words. Do not insert above it;
     that duplicates them. Hand the file to `init-writing-workspace`, whose
     procedure replaces the v1 text with both blocks, and say so. If that
     skill is not installed, show the diff between the v1 text and this
     asset, recommend replacing the v1 text with this block and installing
     `init-writing-workspace` for the second, and wait. A
     `## Project-Specific` section, if present, stays below exactly as
     written.
   - Present, this block present, same version: leave it.
   - Present, this block present, older version: replace what lies between
     the markers, markers inclusive, with the asset. If the block was
     hand-edited, show the diff first and wait for the decision.
3. **`AGENTS.md`.** Make it identical to `CLAUDE.md`. Absent: create it as
   a copy. Present and differing outside this block: apply the same block
   change only, then show the remaining difference and recommend which
   file to align to; the two must not drift.
4. Confirm: list the files created or changed, and say in one sentence
   that the folder now carries the research principles as its first rules
   and that a manuscript folder also needs `init-writing-workspace`.

## Removing

Delete the block, markers inclusive, from both files. If nothing but blank
lines is left in a file, delete the file. Touch nothing else.

## Updating the canonical content

Edit `assets/CLAUDE.md`, bump the version in its opening marker, rebuild
the generated trees (`node tools/build-agent-skills.mjs`), then offer to
re-run the skill on active folders. Re-running replaces only this block.
