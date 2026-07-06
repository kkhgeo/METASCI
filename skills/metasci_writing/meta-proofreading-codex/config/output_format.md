# Output Contract (v13 — content rules only, no rendering rules)

## Why there are no rendering rules

v3–v12 tried to hand-draw terminal typography: boxes, horizontal rules,
manual width math, hard-wrapped prose. Twelve revisions taught one
lesson — hand-drawn alignment breaks under Korean text and renderer
changes, and a long typography spec competes with the review-quality
instructions for the model's attention.

v13 deletes the typography layer entirely. **Visual presentation
(headings, tables, bold, lists) is at the model's discretion, within
standard Markdown.** The renderer is responsible for alignment.

## The one visual rule

Do NOT hand-draw structure:
- no box-drawing characters (`┌ ─ ┐ │ └ ┘`)
- no horizontal rules built from `─` / `═` characters
- no manual column padding or width counting
- no hard-wrapping prose at a fixed column width

Use native Markdown primitives and let the renderer align them.

## Content contract (mandatory)

1. **Language** — all user-facing output in Korean. English original
   text is always shown alongside, with a Korean translation for
   review targets.
2. **Tier discipline** — default view shows the Top-3 priorities only.
   Expand one item on `"[N]번"` / `"[N]번 자세히"`; full list on
   `"다 보여줘"`. Never dump all findings unprompted.
3. **Severity labels** — exactly three: **높음 / 중간 / 낮음**.
   Agent B integrity findings may additionally use **치명**.
   Same words everywhere; no symbols or emoji required.
4. **Reference status labels** — exactly three: **확인됨 / 추정 / 미확인**.
5. **Plain explanations** — plain Korean, no untranslated jargon
   ("Given-New", "nominalization" → 풀어서 설명), framed as reader
   experience ("이 문장을 읽으면…"), ≤2 sentences per issue.
6. **Issue detail order** — every expanded issue contains, in order:
   원문 → 문제 → 수정안(들) → 근거 → 발견자 (합의 / 단독 / 충돌).
   Multi-alternative suggestions are labeled A/B/C with a one-line
   rationale each and a recommendation.
7. **Navigation** — every screen ends with one line listing the next
   actions the user can take.
8. **Decision points present 2-4 numbered options in plain text** (the
   user can always type a free-form answer instead).
   Use them for: knowledge-distribution approval, intent confirmation,
   per-sentence apply decisions, conflict resolution. Typed commands
   from `config/navigation.md` must still be honored when the user
   prefers typing.

## Session summary (end of session)

Show: scope (modes / units / reviewer count), issue counts
(합의 / 단독 / 충돌), user decisions (적용 / 승인 / 건너뛰기),
Agent B integrity counts (레퍼런스 미확인 / 수치 불일치 / 2차 인용 경고),
and a revision-history table (원문 / 수정문 / 근거).
