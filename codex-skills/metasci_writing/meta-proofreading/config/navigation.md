# Navigation — Mode Switching and User Input Mapping

## 3-Mode Structure

```
Mode 1: Paper (논문 전체)
Mode 2: Section (섹션)
Mode 3: Paragraph (단락 + 문장)
```

---

## Entry Points

The user can start from any mode:

| User says | Entry mode |
|---|---|
| "전체 초고 봐줘" / "논문 전체 검토" / "full draft" | Mode 1 |
| "Discussion 교정" / "[섹션] 검토해줘" / "이 섹션 봐줘" | Mode 2 |
| "이 단락 봐줘" / "3번 단락" / [텍스트 붙여넣기] | Mode 3 |
| "이 문장 하나만" / [한 문장 붙여넣기] | Mode 3 (문장 단계 직행) |

---

## Mode Transitions (during session)

### Going deeper (down)

| From | User says | To |
|---|---|---|
| Mode 1 | "[섹션] 검토" / "Discussion으로" | Mode 2 |
| Mode 2 | "단락 [N] 검토" / "문장 검토 시작" | Mode 3 |
| Mode 2 | "첫 단락부터" / "진행" | Mode 3 (단락 1부터) |

### Going broader (up)

| From | User says | To |
|---|---|---|
| Mode 3 | "섹션으로" / "위로" / "섹션 보기" | Mode 2 |
| Mode 2 | "전체 보기" / "위로" / "논문 전체" | Mode 1 |
| Mode 3 | "전체 보기" | Mode 1 (2단계 점프) |

### Lateral movement (same level)

| From | User says | To |
|---|---|---|
| Mode 2 | "다음 섹션" / "Methods로" | Mode 2 (다른 섹션) |
| Mode 3 | "다음 단락" / "이전 단락" | Mode 3 (다른 단락) |
| Mode 3 | "다음" / "다음 문장" | Mode 3 (다음 문장) |
| Mode 3 | "단락 [N]으로" | Mode 3 (점프) |

---

## Within Mode 3: Paragraph Flow

Mode 3 flows in three phases (one reviewer round total):

```
Phase A: 의도 확인 (사용자 승인)
  ↓
Phase B: 리뷰어 패널 1회전 (단락 + 모든 문장 대안 후보 생성)
  → 심사 라운드 1회 (Agent J: 후보 채점 → 문장·단락별 최적안 선정)
  → 단락 수준 결과 제시
  → 최적안이 원문이 아니거나 이슈가 있는 문장만 워크스루 (재호출 없음)
  ↓ 모든 결정 완료
Phase C: Reference verification (Agent B)
  ↓ 자동
Completion summary
  ↓
다음 단락 or 사용자 선택
```

The user can skip steps:

| User says | Action |
|---|---|
| "바로 문장 검토" | Skip Phase A (intent inferred, not confirmed) |
| "단락만 봐줘" | Present paragraph-level results only, skip sentence walkthrough |
| "레퍼런스 생략" | Skip Phase C |

---

## Common Actions (available in all modes)

| User says | Action |
|---|---|
| "오늘 여기까지" / "종료" / "done" | Session summary → end |
| "저장해줘" | Save session state |
| "요약 보여줘" | Show current session summary |
| "Knowledge Bank 보여줘" | Display knowledge bank contents |
| "분배 보여줘" | Show reviewer knowledge distribution |
| "파일 추가: [경로]" | Add knowledge file mid-session |
| "리뷰어 [N]명만" | Adjust reviewer count |
| "웹검색 해줘" | Trigger web search supplement |
| "웹검색 없이" | Disable web search for session |

---

## Sentence-Level Actions

Decisions are normally offered as a numbered decision prompt options; these typed
commands are always honored as well:

| User says | Action |
|---|---|
| "최적안 적용" / "적용" | Apply the judge-selected optimal rewrite |
| "대안들 보여줘" / "후보 전부" | Expand the full ranked candidate menu (all surviving candidates + scores, original included) |
| "추천만" | Collapse the menu back to the recommend-first view |
| "N번 적용" / "2번" | In the menu view, apply the numbered candidate |
| "대안 적용" / "대안 A" / "대안 B" | Apply a runner-up instead of the optimal (recommend-first view) |
| "원문 유지" | Keep the original (judge's ORIGINAL selection or user override) |
| "직접 수정" | User provides own revision |
| "다음" / "ok" | Approve current, next sentence |
| "건너뛰기" / "스킵" | Skip without deciding |
| "검색해봐" / "다른 논문에서는?" | Trigger web search (offered when 선정 신뢰도 is LOW) |
| "자세히" / "왜?" | Expand the judge's reasoning / issue explanation |
| "이 단락 다시" | Restart current paragraph |

### Batch commands (paragraph walkthrough)

| User says | Action |
|---|---|
| "최적안 전부 적용" | Apply the judge's optimal for every sentence at once (ORIGINAL selections stay unchanged) |
| "이슈만 처리" | Resolve flagged issues only; still walk through rewrite selections |
| "나머지 건너뛰기" | Skip all remaining decisions in this paragraph |

---

## Section Change Behavior

When switching to a different section:
1. Knowledge files re-matched to new section keywords
2. Knowledge distribution updated (if different files match)
3. Writing-manual section file swapped
4. User notified: "Knowledge Bank을 [섹션]에 맞게 업데이트합니다"
