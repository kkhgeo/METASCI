---
name: init-review-lessons
description: >
  Use when a manuscript folder should keep what outside-AI reviews (ChatGPT,
  Gemini, a browser Claude) taught, so accepted points are checked next time
  and declined proposals are not re-argued — the author says "리뷰 교훈 파일
  만들어줘", "리뷰 학습 설정", "외부 리뷰 학습 켜줘", "리뷰 교훈 초기화",
  "init review lessons", or asks for a review's lessons to be remembered.
  Also use to refresh the instruction file to the current version, to pull
  new global lessons into a folder, to migrate an older single-file
  REVIEW_LESSONS.md into the split layout, or to remove the layer. Sibling
  of init-writing-workspace, init-communication-rules, and init-figure-rules.
---

# Init Review Lessons

Installs the review-lessons layer of a manuscript workspace: one instruction
file, `AGENT_review_lessons.md`, and one data folder, `review_lessons/`, with
the lessons split into one file per manuscript section. The agent already
judges outside-AI review findings one by one when the author asks whether
to reflect them; this layer makes each judgment leave one generalized line
behind, and keeps those lines available on request without loading them
into every session.

Canonical content lives in `assets/`. **Never rewrite it from memory** —
copy it verbatim, version comment included.

```
assets/
├── AGENT_review_lessons.md   the instruction file (read when a review comes in)
└── review_lessons/
    └── general.md            the empty two-heading file every section file starts from
```

## Why a folder, and two copies

One file holding every lesson grows with every review, and the whole of it
enters context each time it is opened. Split by section, a review touching
Results opens `general.md` and `results.md`, nothing else. The instruction
file stays fixed in size and separate from the data, so updating the rules
never touches a lesson line.

Lessons that hold for every manuscript are worth more than one folder. The
global folder at `Z:\KKH_Research\META_SCI\review_lessons\` collects them in
the same per-section files; a new manuscript folder is seeded from it, and
every 전역 line is appended to both copies at once, so there is no separate
sync step to forget. Manuscript-specific lines (이논문) stay local.

**Do not append the rules into CLAUDE.md or AGENTS.md.** One pointer line
only.

## Procedure

1. Identify the target project root. If unclear, ask — do not guess.
   `CLAUDE.md` does not need to exist; the layer stands on its own.
2. **Global folder** — `Z:\KKH_Research\META_SCI\review_lessons\`.
   - Drive unreachable: say so, continue with the local install, and note
     that 전역 lines will carry `[전역 미반영]` until it is reachable.
   - Absent: create it with `general.md` from the asset. Present: leave it.
   - Then, if the pre-split file `Z:\KKH_Research\META_SCI\REVIEW_LESSONS.md`
     sits beside it: migrate its lines into the folder (see below) and
     delete that file — the instruction block is not kept globally any more.
3. **Local folder** — `<root>/review_lessons/`.
   - Absent: create it with `general.md` from the asset, then seed it: copy
     every lesson line from each global section file into the local file of
     the same name, under the same heading, creating files from
     `general.md`'s two headings as needed. Report the number of lines seeded.
   - Present: for each global section file, add any 전역 line missing
     locally (same lesson text — the 교훈 field alone, ignoring date, scope,
     and `×n`) under the matching heading of the local
     file of the same name, creating that file from the two headings if it
     does not exist. Report the number added; if none, report "already
     current".
   - Then, if the pre-split file `<root>/REVIEW_LESSONS.md` is present:
     migrate its lines into the folder (see below). Seeding comes first so
     that a migrated line whose lesson text is already in the target file
     is skipped rather than duplicated.
4. **Local instruction file** — `<root>/AGENT_review_lessons.md`.
   - Absent: write the asset verbatim.
   - Present, same version: leave it.
   - Present, older version: replace the whole file. If it was hand-edited,
     show the diff first and wait for the decision.
   - The pre-split file `<root>/REVIEW_LESSONS.md` present: its lines were
     moved in step 3, so delete the old file; `AGENT_review_lessons.md`
     itself follows the three bullets above.
5. **Pointer line.** Check `AGENTS.md`, then `CLAUDE.md`. **If either
   already mentions `AGENT_review_lessons.md`, change nothing.** If a bullet
   mentions the old name `REVIEW_LESSONS.md`, replace that whole bullet,
   however many lines it wraps over, with the text below as one bullet
   (`- ` marker in front).
   Otherwise append the text as a new line to the first file that exists:

   ```
   If AGENT_review_lessons.md exists in this folder, do not read it or the review_lessons/ folder by default. Read and follow it only when another AI's review of the manuscript is brought in, or when the author asks for the lessons.
   ```

   If neither file exists, say so and suggest `init-writing-workspace`;
   still install the layer.
6. Confirm: list the files and folders created or updated, the seed count
   (or the top-up count), and the migration count per file if a pre-split
   file was migrated; then say in one sentence that from now on each
   outside-AI review of this manuscript leaves one lesson line per finding
   in `review_lessons/`, one file per section, and for 전역 lines in the
   global folder too — and that nothing here is read unless a review comes
   in or the author asks for the lessons.

## Migrating a pre-split file

`REVIEW_LESSONS.md` (v1) held the instruction block and the lessons in one
file. Everything below its `<!-- /metasci:review-lessons -->` line is data:
lesson lines under the two headings. Move each line into
`review_lessons/<section>.md`, where the section is the third field of the
line (`전체` → `general.md`, otherwise the label in lower case with spaces
as `_`), under the same heading it sat under, at the end of that block,
creating files from the two headings as needed. Keep every line exactly as
written; the `×n` markers and dates travel with the lines. A line whose
lesson text is already in the target file (seeded from the global folder)
is skipped. Report the line count moved per file.

## Removing

Delete `<root>/AGENT_review_lessons.md`, `<root>/review_lessons/`, and the
pointer line added in step 5. Touch nothing else — the global folder stays,
since other manuscripts share it.

## Updating the canonical content

Edit the files under `assets/`, bump the version in the instruction file's
opening `<!-- metasci:review-lessons vN -->` comment, rebuild the generated
trees (`node tools/build-agent-skills.mjs`), then offer to re-run the skill
on active projects. Re-running replaces only the instruction file; the
lessons in `review_lessons/` survive.
