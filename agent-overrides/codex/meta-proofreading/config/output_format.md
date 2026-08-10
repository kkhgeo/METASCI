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

1. **Language** — explain in the user's language. Preserve the manuscript's
   original language. When the user works in Korean on an English manuscript,
   show the English review target with a Korean translation where it helps the
   decision; do not force Korean output for users working in another language.
2. **Tier discipline** — default view shows the Top-3 priorities only.
   Expand one item on `"[N]번"` / `"[N]번 자세히"`; full list on
   `"다 보여줘"`. Never dump all findings unprompted.
3. **Severity labels** — internal values are **CRITICAL / HIGH / MEDIUM / LOW**.
   Localize them consistently for the user's language; in Korean use
   **치명 / 높음 / 중간 / 낮음**. No symbols or emoji are required.
4. **Reference status labels** — internal values are
   **verified / partial / unverified**. In Korean display
   **확인됨 / 부분 확인 / 미확인**.
5. **Plain explanations** — use plain language in the user's language and explain
   untranslated jargon ("Given-New", "nominalization") through reader experience,
   normally in no more than two sentences per issue.
6. **Issue detail order** — every expanded ISSUE (a problem a rewrite
   cannot fix: citation, placement, numeric, cross-section) contains, in
   order: 원문 → 문제 → 조치(directive) → 근거 → 발견자 (합의 / 단독 / 충돌).
6b. **Candidate selection output** (adaptive by selection confidence) —
   for any sentence/paragraph unit that went through the judge round
   (Agent J). Two hard rules govern EVERY candidate view, because the user
   decides only from what is on screen:
   (i) **Show every candidate's FULL text, verbatim.** Never abbreviate a
       candidate with "…", never show only the changed fragment or a bare
       diff — the user must read each complete rewritten sentence without
       reconstructing it. Show the original in full too, with its Korean
       translation, and give a Korean translation (or at least a one-line
       Korean gloss of what changed in meaning) for any candidate that
       alters meaning.
   (ii) **Explain enough to choose.** For each candidate give: what it
        changes (concretely, against the original), why that matters, and
        the trade-off — what you gain and what you give up. A few
        sentences, not a single clause. Terse one-liners are a defect
        here; the user has told us sparse explanation makes choosing hard.
   All of this lives in the MESSAGE BODY. An interactive choice tool, when
   available, is only the decision mechanism: its option labels are short pointers
   (`"1번"`, `"원문 유지"`, `"직접 수정"`), NEVER the place the candidate
   text or its reasoning is conveyed.
   Presentation by confidence:
   - **HIGH → 추천 우선 뷰.** 이전 문장(맥락) → 원문(전문 + 한국어 번역) →
     **최적안(추천)**: 전문 + 무엇이 바뀌나 + 왜 최적인지 + 트레이드오프 →
     대안 1–2개: 각 전문 + 설명 → 근거(writing-manual / 지식 / 판단) →
     선정 신뢰도.
     Decision: `"최적안 적용"` / `"대안들 보여줘"` / `"원문 유지"` /
     `"직접 수정"`.
   - **MEDIUM / LOW → 메뉴 뷰 (자동 펼침).** 이전 문장(맥락) → 원문(전문 +
     번역) → 심사관이 순위 매긴 **전체 후보 목록**: 각 항목마다 점수 +
     ★(최적 표시) + **후보 전문** + 무엇이 바뀌나·트레이드오프 설명 +
     (의미가 바뀌면) 번역, 원문도 한 항목으로 포함 → 왜 신뢰도가 낮은지 +
     심사관 종합 한두 문장.
     번호 또는 평문으로 선택: `"N번 적용"` / `"원문 유지"` /
     `"직접 수정"` (LOW면 `"검색해봐"` 포함).
   Any confidence: `"대안들 보여줘"` / `"후보 전부"` expands the full ranked
   menu; `"추천만"` collapses back to the recommend-first view. When the
   optimal is the ORIGINAL, state "원문이 최적 — 수정 불필요" and still show
   the strongest explored alternative in full for transparency.
7. **Navigation** — every screen ends with one line listing the next
   actions the user can take.
8. **Decision points may use an available interactive choice tool** (2-4 options;
   free-text alternatives must remain available).
   Use it for: knowledge-distribution approval, intent confirmation,
   per-sentence apply decisions, conflict resolution. Typed commands
   from `config/navigation.md` must still be honored when the user
   prefers typing. The tool carries the DECISION, not the
   information: never rely on its option labels to convey the text under
   review or the reasoning — those belong in the message body.
9. **No truncation of anything the user judges from.** Never replace part
   of a review target, an original sentence, or a candidate rewrite with
   "…" or a diff-only fragment. Show full text. Abbreviating what the user
   is being asked to choose between defeats the review.

## Session summary (end of session)

Show: scope (modes / units / reviewer count), issue counts
(합의 / 단독 / 충돌), user decisions (적용 / 승인 / 건너뛰기),
Agent B integrity counts (레퍼런스 미확인 / 수치 불일치 / 2차 인용 경고),
and a revision-history table (원문 / 수정문 / 근거).
