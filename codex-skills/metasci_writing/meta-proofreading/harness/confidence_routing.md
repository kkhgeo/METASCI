# Confidence Routing — Adaptive Workflow Based on Reviewer Confidence

## Purpose

Define how reviewer confidence levels affect the workflow:
what to show, how much detail, and when to trigger additional actions.

---

## Confidence Levels (per issue)

Each reviewer assigns confidence to every issue they raise:

| Level | Meaning | Basis |
|---|---|---|
| **HIGH** | Clear problem, well-grounded fix | Writing-manual rule clearly violated, OR strong knowledge-based evidence |
| **MEDIUM** | Likely problem, reasonable fix | Pattern seems off but domain conventions may differ |
| **LOW** | Uncertain, needs more evidence | Domain-specific issue, reviewer lacks sufficient knowledge to judge |

---

## Routing Rules

### After Deliberation — Aggregate Confidence

Combine individual reviewer confidences for each issue:

```
Aggregate confidence:
  - All reviewers HIGH → Issue confidence: HIGH
  - Mix of HIGH and MEDIUM → Issue confidence: HIGH
  - All MEDIUM → Issue confidence: MEDIUM
  - Any LOW (even one) → Issue confidence: LOW
  - Single reviewer only → use that reviewer's confidence
```

All three routing levels follow the `config/output_format.md` content
contract (원문 → 문제 → 수정안 → 근거 → 발견자). Confidence routing
controls **how much detail** goes into the issue and **which actions**
are offered — never the visual layout itself.

### Selection Confidence (candidate units)

Candidate units (sentence/paragraph rewrites) do not use aggregate reviewer
confidence — they carry the judge's `selection_confidence` from Agent J
(`agents/agent_j.md`). Route by that value instead:

- **HIGH → 추천 우선 뷰.** Present the optimal as the recommendation +
  1–2 runner-ups, expect a quick decision. The full ranked slate stays
  one command away (`"대안들 보여줘"`).
- **MEDIUM → 메뉴 뷰 자동 펼침.** The judge did not settle the choice
  cleanly, so do not push a single recommendation — show Agent J's full
  ranked candidate menu (scores + one-line each, ★ on the top-ranked,
  ORIGINAL included) and let the user pick a number.
- **LOW → 메뉴 뷰 + 검색 제안.** Show the ranked menu as in MEDIUM, and
  additionally offer the web-search supplement before the user decides:
  `"이 표현이 분야 관례상 맞는지 유사 논문에서 확인할까요?"`

This adaptive default is `config/output_format.md` 6b. Regardless of
confidence, the user can expand the menu with `"대안들 보여줘"` or collapse
to recommend-first with `"추천만"`.

The rest of this file (issue-level HIGH/MEDIUM/LOW routing) governs the
ISSUES track.

### HIGH Confidence Routing

```
Display:
  - Issue + suggestion (concise)
  - Brief Korean explanation (≤1 sentence in 문제)
  - Evidence source (if any) in 근거

User interaction (a numbered decision prompt options or typed):
  - Expect quick decision: "적용" / "다음" / "건너뛰기"
  - No automatic expansion
```

### MEDIUM Confidence Routing

```
Display:
  - Issue + suggestion with detailed rationale
  - Full Korean explanation with original-vs-suggestion comparison
    (2 sentences in 문제)
  - Evidence source with context in 근거
  - 발견자 line notes which reviewers flagged it

User interaction (a numbered decision prompt options or typed):
  - "적용" / "수정해서 적용" / "건너뛰기" / "자세히"
```

### LOW Confidence Routing

```
Display:
  - Issue flagged as uncertain — add one plain line below 근거:
    **리뷰어들의 확신이 낮습니다** + 불확실한 이유 한 줄
  - All available reviewer perspectives shown

Automatic action:
  - Offer web search: "이 부분에 대해 유사 논문의 표현을 검색할까요?"
  - If user agrees → run targeted web search
  - Present search results alongside reviewer suggestions

User interaction (a numbered decision prompt options or typed):
  - "검색해봐" / "이대로 괜찮아" / "건너뛰기" / "직접 수정"
```

---

## Web Search on LOW Confidence

When triggered (automatically or by user request):

1. Extract the problematic text span
2. Identify the rhetorical function (interpretation, comparison, etc.)
3. Construct focused search query:
   ```
   "[domain term] [rhetorical context] [section type]"
   ```
4. Search Google Scholar / Semantic Scholar
5. Find 2-3 comparable sentences from published papers
6. Present as additional evidence:

```markdown
### 추가 검색 결과

**검색어** — [query]

**유사 표현**
1. [sentence from Paper A] — Author (Year), Journal
2. [sentence from Paper B] — Author (Year), Journal

**보강된 수정안** — [improved suggestion based on evidence]
[왜 이 표현이 더 적절한지 한국어 설명]
```

---

## Session-Level Confidence Tracking

```
confidence_summary = {
    high_count: int,       // issues resolved quickly
    medium_count: int,     // issues requiring explanation
    low_count: int,        // issues requiring search
    searches_triggered: int,
    searches_helpful: int  // user accepted search-informed suggestion
}
```

This helps evaluate whether the Knowledge Bank was sufficient
for the review session.
