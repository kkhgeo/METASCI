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

### HIGH Confidence Routing

```
Display:
  - Issue + suggestion (concise)
  - Brief Korean explanation
  - Evidence source (if any)

User interaction:
  - Expect quick decision: "적용" / "다음" / "건너뛰기"
  - No automatic expansion

Formatting:
  #### [합의] Issue title
  `[간결한 설명]`
  **수정안:** `[suggestion]`
```

### MEDIUM Confidence Routing

```
Display:
  - Issue + suggestion (with detailed rationale)
  - Full Korean explanation with comparison
  - Evidence source with context
  - Note which reviewers flagged it

User interaction:
  - Present options clearly
  - "적용" / "수정해서 적용" / "건너뛰기" / "자세히"

Formatting:
  #### [합의/발견] Issue title
  `[상세한 설명: 원문의 문제점과 수정안의 차이를 구체적으로]`
  **수정안:** `[suggestion]`
  **근거:** `[what rule or evidence supports this]`
```

### LOW Confidence Routing

```
Display:
  - Issue flagged as uncertain
  - All available perspectives shown
  - Explicit uncertainty acknowledgment

Automatic action:
  - Offer web search: "이 부분에 대해 유사 논문의 표현을 검색할까요?"
  - If user agrees → run targeted web search
  - Present search results alongside reviewer suggestions

User interaction:
  - "검색해봐" / "이대로 괜찮아" / "건너뛰기" / "직접 수정"

Formatting:
  #### [불확실] Issue title
  `[상세 설명 + 불확실한 이유]`
  **R1 수정안:** `[suggestion]`
  **R4 수정안:** `[suggestion]`
  ⚠️ 리뷰어들의 확신이 낮습니다.
  *"검색해봐" / "이대로 괜찮아" / "건너뛰기"*
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
#### 추가 검색 결과
**검색어:** `[query]`

**유사 표현:**
1. `[sentence from Paper A]` — Author (Year), Journal
2. `[sentence from Paper B]` — Author (Year), Journal

**보강된 수정안:** `[improved suggestion based on evidence]`
`[왜 이 표현이 더 적절한지 한국어 설명]`
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
