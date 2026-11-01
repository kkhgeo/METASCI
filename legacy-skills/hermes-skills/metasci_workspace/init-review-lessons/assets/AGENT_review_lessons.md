<!-- metasci:review-lessons v2 -->
# Review Lessons

This file turns outside reviews into standing rules. When the author brings
in a review of this manuscript written by another AI (ChatGPT, Gemini, a
browser Claude, any model outside this workspace) — reviewer comments,
suggested rewrites, or both — the findings are judged as usual, and every
judgment leaves one line in the `review_lessons/` folder next to this file,
so the same point is not missed, and the same declined proposal is not
re-argued, the next time.

## Where the lessons live

The lessons are not in this file. They sit in `review_lessons/`, one file
per manuscript section, so that reading the lessons for one section costs
one small file, never the whole history:

```
review_lessons/
├── general.md        lessons that hold for the whole manuscript (섹션 = 전체)
├── introduction.md   lessons filed under that section
├── methods.md
├── results.md
├── discussion.md
└── <section>.md      any other section, named as the manuscript names it
```

Each file has the same two headings, and nothing else. Lines sit directly
beneath their heading, and one blank line separates the two blocks:

```
## 확인할 것 (반영한 지적에서)
## 받지 않는 제안 (거부한 지적에서)
```

File name = the section label in lower case with spaces replaced by `_`;
전체 is `general.md`. Use `abstract`, `introduction`, `methods`, `results`,
`discussion`, `conclusion`, `figures`, `references` when the manuscript's
section maps onto one of them, so the same lesson never ends up under two
spellings. A file is created the first time a line is filed under its
section, with the two headings and nothing else.

Two copies exist. The local `review_lessons/` folder holds every line that
applies to this manuscript. The global folder at
`Z:\KKH_Research\META_SCI\review_lessons\` holds only the lines that apply to
every manuscript, in the same per-section files. A new manuscript folder is
seeded from the global folder.

## When to act

Act without being asked when the prompt contains another AI's review of
this manuscript's text and the author wants it checked or reflected —
pasted comments, a proposed version, "반영할 수 있는지 봐줘", "이 지적 맞아?".
"리뷰 반영" is the explicit trigger. A review of something other than the
manuscript (code, a slide deck, a figure) is out of scope.

## Procedure

1. **Judge each finding as you normally would** — 반영 / 부분 반영 / 거부,
   one-line reason each — and apply accepted changes through the usual
   approval flow: show before/after, wait for the decision, then edit.
   Nothing here changes how a finding is judged. This file only records
   what the judgment taught. Do not cross-check the finding against the
   writing skills' checklists or against earlier sessions; the judgment
   already made is the whole input.
2. **Write one lesson per finding.** Generalize it: a rule you could apply
   to a paragraph you have never seen, not a note about this paragraph.
   No sentence quotes, no paragraph numbers. Korean, one line.
   - 반영 or 부분 반영 → a check to run next time ("...를 확인한다").
   - 거부 → the proposal and why it is not taken ("...는 받지 않는다 — 이유").
   A finding that teaches nothing general — a typo, a one-off slip — gets
   no line.
3. **Decide the scope.** Terminology, journal format, this study's design,
   a reviewer's stated preference for this paper → 이논문. Anything that
   would hold for another manuscript → 전역. The 섹션 field names where the
   rule applies, not where the reviewer found it: a rule that holds anywhere
   in the manuscript (intensifiers, hedges, tense, units) is 전체 and goes
   to `general.md`, even when the finding was tagged with a section.
4. **Check for a duplicate before appending.** Open `general.md` and the
   file for the finding's section — those two, not the whole folder. If a
   line already states the same check or the same declined proposal — a
   shared reason alone does not make a duplicate — do not add another:
   raise its count marker (`×2`, `×3`) and replace its date with today's,
   in both copies for a 전역 line.
   A rising count means a rule keeps being missed; say so to the author
   when a count reaches 3.
5. **Append.** 이논문 lines go to the local file for their section only.
   전역 lines go to the local file **and** the global file of the same
   name, identically. Append under the matching heading. Never rewrite or
   delete existing lines on your own. If the global folder is unreachable
   (drive not mounted), append locally, add `[전역 미반영]` at the end of
   the line, and tell the author; on a later run, push those lines to the
   global folder and drop the mark.
6. **Report** the lines added or bumped, in one short list, naming the file
   each went to.

## Line format

The 섹션 field decides the file, and keeps a line meaningful if it is ever
moved, so it stays in the line even though the file name repeats it.

```
- YYYY-MM-DD · 전역|이논문 · 섹션(있으면, 없으면 전체) · 교훈 한 줄 · ×n
```

```
- 2026-09-05 · 전역 · Results · 효과 크기를 보고할 때 신뢰구간이 빠졌는지 확인한다 · ×1
- 2026-09-05 · 전역 · Discussion · 첫 문장이 결과 요약 없이 해석으로 바로 들어가는지 확인한다 · ×2
- 2026-09-05 · 이논문 · 전체 · 'catchment'는 이 원고에서 'basin'으로 통일한다 · ×1
- 2026-09-05 · 전역 · 전체 · 'appears'·'suggests' 같은 hedge를 걷어내라는 제안은 받지 않는다 — 주장 강도가 무단 상승한다 · ×1
```

## When this file is read

Not at session start, and not before writing work — by default this file
and the `review_lessons/` folder stay out of context. They are opened in
two cases only:

- **A review comes in.** Read this file, then `general.md` and the section
  files the review's findings fall under; the duplicate check in step 4
  needs those lines. Do not open the other section files.
- **The author asks for the lessons** — "교훈 봐줘", "리뷰 교훈 적용해서",
  `@AGENT_review_lessons.md`, or similar. Read `general.md` and the file
  for the section being worked on, and apply both lists, alongside the
  writing skills' own checklists, to the piece of work at hand. Open the
  whole folder only when the author asks for all of it. 확인할 것 is the
  set of checks past reviews found missing. 받지 않는 제안 is the set of
  proposals already declined, with the reason.

## Maintenance

When any one file passes about 50 lines, say so and offer to merge
near-duplicates. Merging is the author's call; never prune on your own.
