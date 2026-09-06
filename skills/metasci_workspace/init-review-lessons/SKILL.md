---
name: init-review-lessons
description: >
  Install a review-lessons ledger into a manuscript workspace: drops one
  standalone `REVIEW_LESSONS.md` that tells the agent, whenever the author
  pastes another AI's review of the manuscript (comments or suggested
  rewrites), to judge each finding as usual and then record one generalized
  lesson per finding — accepted points as checks to run next time, declined
  proposals with the reason — in the local file and in the global copy at
  Z:\KKH_Research\META_SCI\REVIEW_LESSONS.md, so the same point is not missed
  or re-argued in later work. Adds one pointer line to AGENTS.md/CLAUDE.md
  that keeps the file out of context until a review comes in or the author
  asks for the lessons.
  Use when the user says "리뷰 교훈 파일 만들어줘", "리뷰 학습 설정", "외부
  리뷰 학습 켜줘", "리뷰 교훈 초기화", "init review lessons", or wants
  lessons from outside reviews kept for later. Sibling of
  init-writing-workspace, init-communication-rules, and init-figure-rules.
  Also use to refresh the instruction block to the current version, to pull
  new global lessons into a folder, or to remove the file.
---

# Init Review Lessons

Installs the review-lessons layer of a manuscript workspace. The agent
already judges outside-AI review findings one by one when the author asks
whether to reflect them; this layer makes each judgment leave one
generalized line behind, and keeps those lines available on request
without loading them into every session.

Canonical content lives in `assets/REVIEW_LESSONS.md`. **Never rewrite it
from memory** — copy it verbatim, version comment included.

## Why a separate file, and two copies

The instruction block would double CLAUDE.md, and the lessons list grows
every time a review comes in; `init-writing-workspace` regenerates
CLAUDE.md from its own asset and would wipe both. So the rules and the
lessons live together in one standalone file, reached through a single
pointer line. The file is not read by default: a growing lessons list
loaded every session would crowd the context, so the pointer line opens
it only when a review comes in (to record) or when the author asks for
the lessons (to apply).

Lessons that hold for every manuscript are worth more than one folder.
The global copy at `Z:\KKH_Research\META_SCI\REVIEW_LESSONS.md` collects
them; a new manuscript folder is seeded from it, and every 전역 line is
appended to both copies at once, so there is no separate sync step to
forget. Manuscript-specific lines (이논문) stay local.

**Do not append the rules into CLAUDE.md or AGENTS.md.** One pointer line
only.

## File anatomy

```
<!-- metasci:review-lessons v1 -->      ← version marker, start of instruction block
# Review Lessons
...                                      instruction block (replaced on update)
<!-- /metasci:review-lessons -->        ← end of instruction block
## 확인할 것 (반영한 지적에서)            ← lessons: never touched by this skill except seeding
## 받지 않는 제안 (거부한 지적에서)
```

Everything below the closing marker is the author's accumulated data.
Updating replaces only what lies between the markers.

## Procedure

1. Identify the target project root. If unclear, ask — do not guess.
   `CLAUDE.md` does not need to exist; the file stands on its own.
2. **Global copy** — `Z:\KKH_Research\META_SCI\REVIEW_LESSONS.md`.
   - Drive unreachable: say so, continue with the local install, and note
     that 전역 lines will carry `[전역 미반영]` until it is reachable.
   - Absent: write the asset verbatim.
   - Present, same version: leave it.
   - Present, older version: replace the instruction block between the
     markers; leave every line below the closing marker untouched. Report
     the version change.
3. **Local copy** — `<root>/REVIEW_LESSONS.md`.
   - Absent: write the asset verbatim, then seed it: copy every lesson
     line from the global copy's two lists into the matching lists.
     Report the number of lines seeded.
   - Present, same version: leave the instruction block. Then add any
     전역 line present in the global copy but missing locally (same lesson
     text), under the matching heading. Report the number added; if none,
     report "already current".
   - Present, older version: replace the instruction block between the
     markers, keep the lessons, then do the same 전역 top-up. If the block
     was hand-edited, show the diff first and wait for the decision.
4. **Pointer line.** Check `AGENTS.md`, then `CLAUDE.md`. **If either
   already mentions `REVIEW_LESSONS.md`, change nothing.** Otherwise append
   to the first one that exists:

   ```
   If REVIEW_LESSONS.md exists in this folder, do not read it by default. Read and follow it only when another AI's review of the manuscript is brought in, or when the author asks for the lessons.
   ```

   If neither file exists, say so and suggest `init-writing-workspace`;
   still install the file.
5. Confirm: list the files created or updated and the seed count, and say
   in one sentence that from now on each outside-AI review of this
   manuscript leaves one lesson line per finding here and, for 전역 lines,
   in the global copy — and that the file is otherwise read only when the
   author asks for the lessons.

## Removing

Delete `<root>/REVIEW_LESSONS.md` and the pointer line added in step 4.
Touch nothing else — the global copy stays, since other manuscripts share
it.

## Updating the canonical content

Edit `assets/REVIEW_LESSONS.md`, bump the version in its opening
`<!-- metasci:review-lessons vN -->` comment, rebuild the generated trees
(`node tools/build-agent-skills.mjs`), then offer to re-run the skill on
the global copy and on active projects. Re-running replaces only the
instruction block; the lessons survive.
