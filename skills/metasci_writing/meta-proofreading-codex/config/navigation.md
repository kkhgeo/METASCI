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
Phase B: 리뷰어 패널 1회전 (단락 + 모든 문장 동시 검토)
  → 단락 수준 결과 제시
  → 지적이 있는 문장만 하나씩 워크스루 (리뷰어 재호출 없음)
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

Decisions are normally offered as numbered options; these typed
commands are always honored as well:

| User says | Action |
|---|---|
| "적용" | Apply consensus/single suggestion |
| "수정안 A" / "수정안 B" | Choose between alternatives |
| "직접 수정" | User provides own revision |
| "다음" / "ok" | Approve as-is, next sentence |
| "건너뛰기" / "스킵" | Skip without approval |
| "검색해봐" / "다른 논문에서는?" | Trigger web search for comparable expressions |
| "자세히" / "왜?" | Expand explanation |
| "이 단락 다시" | Restart current paragraph |

### Batch commands (paragraph walkthrough)

| User says | Action |
|---|---|
| "전부 적용" | Apply every consensus suggestion in this paragraph at once (multi-alternative issues take the recommended option) |
| "합의만 적용" | Apply consensus items; continue walkthrough for unique findings and conflicts only |
| "나머지 건너뛰기" | Skip all remaining decisions in this paragraph |

---

## Section Change Behavior

When switching to a different section:
1. Knowledge files re-matched to new section keywords
2. Knowledge distribution updated (if different files match)
3. Writing-manual section file swapped
4. User notified: "Knowledge Bank을 [섹션]에 맞게 업데이트합니다"
