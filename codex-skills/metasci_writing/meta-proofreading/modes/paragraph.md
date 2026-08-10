# Mode 3: Paragraph — Paragraph + Sentence Review

Entered from `SKILL.md` §5 after Step 0 completes, or by drill-down from Mode 2.
This is one panel round per paragraph, then one judge round, then a walkthrough.

**Entry:** User says "단락 [N] 검토", "이 단락 봐줘", or drills down from Mode 2.

**Context loading:** Follow `harness/context_loading.md` Mode 3 rules.
- Target paragraph + prev/next paragraph for context
- All cross-section files (including `sentence_craft.md`, `advanced_nns_issues.md`)
- Knowledge narrowed to paragraph-relevant entries

### 7a. Intent Confirmation

Display the paragraph with its Korean translation. Present the orchestrator's
interpretation of the paragraph's intent:

```markdown
### 단락 [N]

**[EN]** `[paragraph text]`
**[KR]** `[번역]`

### 의도 확인
이 단락의 의도를 이렇게 파악했습니다:

**핵심 메시지:** [요약]
**섹션 내 역할:** [기능]
**핵심 주장:** [중심 주장]

맞나요? 다르면 말씀해주세요.
```

Confirm via AskUserQuestion (options: "맞아요" / "다름 — 직접 설명").
Store the result as `{confirmed_intent}`.

### 7b. Single Panel Round — Paragraph AND All Sentences

Launch all active reviewers in parallel (one `spawn_agent` call each) with:
- `{mode}` = `paragraph`
- `{target_text}` = full paragraph (with prev/next paragraph context),
  with sentences pre-numbered per the splitting rules in
  `config/session_management.md`
- `{confirmed_intent}` = user-confirmed intent
- `{allocated_knowledge}` + `{writing_manual_content}` per distribution

Each reviewer reports, in one pass:
- **CANDIDATE sets** (the core output) — a complete rewrite set for the
  paragraph as a whole AND for EVERY sentence, each candidate optimizing a
  distinct objective, with self-scores and a nomination. Even a clean
  sentence gets a best-effort rewrite or an explicit ORIGINAL nomination —
  reviewers never "just think, no output"
  (`agents/agent_reviewer.md` CANDIDATE GENERATION).
- **Paragraph-level findings** — does the paragraph deliver the
  confirmed intent? Structure, flow (location: `"Paragraph N (whole)"`)
- **ISSUES** — only problems a same-unit rewrite cannot fix (citation,
  placement, numeric, cross-section), location `"Sentence M"` /
  `"Paragraph N (whole)"`.

This is ONE panel round per paragraph. Do NOT launch a new panel per
sentence — the judge round and per-sentence walkthrough below work
entirely from this round's results.

### 7c. Judge Round + Sentence Walkthrough

1. **Judge round.** Run Agent J (`agents/agent_j.md`) **once** for the
   whole paragraph, passing the pooled candidate sets, the original
   paragraph + numbered sentences, the confirmed intent, and the
   writing-manual rubric. It returns the optimal rewrite + runner-ups for
   the paragraph-whole unit and each sentence. In the same synthesis, run
   the ISSUES classification (`harness/deliberation.md`) grouped by unit.

2. **Present the paragraph-whole result first** — judge's optimal (or
   "원문이 최적") + alternatives, plus any paragraph-level issues.

3. Walk through, one at a time, **only the sentences that either got a
   non-ORIGINAL optimal from the judge OR carry an issue**. For each,
   present **adaptively by the judge's selection confidence** (the full
   contract is `config/output_format.md` 6b, routing in
   `harness/confidence_routing.md`):
   - display: previous sentence (context) → current sentence → Korean
     translation, then present per the `config/output_format.md` 6b
     rules — **every candidate shown in FULL (no "…", no diff-only), each
     with a substantive explanation (what changes, why, trade-off) in the
     message body**, not compressed into AskUserQuestion labels:
   - **선정 신뢰도 HIGH → 추천 우선.** Show 최적안(추천) — 전문 + 왜 최적 +
     트레이드오프 — plus 대안 1–2개 (each in full) + any issues.
     AskUserQuestion: "최적안 적용" / "대안들 보여줘" / "원문 유지" /
     "직접 수정".
   - **선정 신뢰도 MEDIUM/LOW → 메뉴 자동 펼침.** Show Agent J's full
     ranked candidate menu — each entry = 점수 + ★(최적) + **후보 전문** +
     무엇이 바뀌나·트레이드오프 설명 + (의미 변화 시) 번역, 원문 포함 —
     plus why confidence is low. AskUserQuestion: "N번 적용" / "원문 유지" /
     "직접 수정" (add "검색해봐" when LOW).
   - At any confidence the user may say "대안들 보여줘" to expand the full
     menu, or "추천만" to collapse.

4. Sentences whose optimal is ORIGINAL and that carry no issues are NOT
   stepped through. Summarize in one line: "문장 2, 5, 7 — 원문이 최적,
   수정 불필요."

5. Batch commands are honored at any point during the walkthrough
   (see `config/navigation.md`):
   - `"최적안 전부 적용"` — apply the judge's optimal for every sentence
     in this paragraph at once (ORIGINAL selections stay unchanged).
     **Confirm once before applying**, stating how many sentences will
     change and that they are AI proposals the author has not read
     individually: *"문장 [N]개가 한 번에 교체됩니다. 개별 검토 없이
     적용하시겠습니까? (적용 후 `"되돌리기"`로 취소 가능)"*
   - `"이슈만 처리"` — resolve flagged issues; still walk through rewrites
   - `"나머지 건너뛰기"` — skip all remaining decisions in this paragraph

6. Record every decision in session state.

### 7d. Post-Paragraph: Agent B Reference Verification

After all sentences in the paragraph are reviewed, automatically run
Agent B following `agents/agent_b.md`:

1. Collect all citations from the paragraph
2. Check `knowledge_bank.sources[]` first — auto-FOUND for matches
3. Check `session.ref_cache` — use cached results
4. Web search remaining unverified citations
5. Cache all results in `session.ref_cache`
6. Present reference verification table

### 7e. Paragraph Completion Summary

```markdown
---
### 단락 [N] 검토 완료
- 수정 적용: [X]건 (최적안 [a], 대안 [b])
- 원문 유지: [Y]건
- 건너뛰기: [Z]건

#### 레퍼런스 확인
| REF | 상태 | 제목 | DOI |
|---|---|---|---|
| Author (Year) | 확인됨 / 추정 / 미확인 | [...] | [...] |

---
*"다음 단락" / "이 단락 다시" / "섹션으로"*
```

Advance to next paragraph or follow user navigation.

