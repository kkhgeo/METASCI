# 규칙 라우팅 — 무엇을 판단할 때 무엇을 읽나

기존 META-SCI 구조 규범을 근거로 판단하고 `decision-protocol.md`에 따라 사용자가
결정할 수 있는 형태로 바꾼다.

## 라우팅 표

| 판단하려는 것 | 읽을 파일 | 위치 |
|---|---|---|
| 섹션끼리 아귀가 맞나 | `structural-integrity.md` | 이 폴더 |
| 이 섹션에 무슨 단락이 있어야 하나 | `section-checklists.md` | 이 폴더 |
| 단락 순서·연결이 자연스러운가 | `cohesion_flow.md` | Glob `**/meta-proofreading/writing-manual/cross_section/cohesion_flow.md` |
| 섹션 골격과 전환 | `section_guides.md` | Glob `**/meta-writing/references/section_guides.md` |
| 단락 하나가 논지로 성립하나 | `principles.md` | Glob `**/meta-rewriting/references/principles.md` |
| 전체·부분 범위를 어떻게 읽나 | `scope-projection.md` | 이 폴더 |
| 무엇부터 묻고 어떻게 승인받나 | `decision-protocol.md` | 이 폴더 |
| 규범 근거·출처가 필요함 | `claude_writing_manual/` — `INDEX.md`, `00_universal.md` + 해당 섹션 | `../../meta-writing/references/claude_writing_manual/` |
| 답이 정해지지 않은 것 | `decision-protocol.md` — 선택지를 비교하고 추천 후 사용자 결정 | 이 폴더 |

Glob 결과가 여러 개면 `skills_archive/`를 버리고 `skills/` 아래 최신 파일을 읽는다.
`structural-integrity.md`와 `section-checklists.md`는 설계 단계용으로 줄여 쓴 파일이므로
교정용 원본으로 덮어쓰지 않는다.

## 전체 조망

1. **질문 체인** — Introduction 질문을 Discussion이 답하고 Conclusion이 되짚는가.
2. **Methods ↔ Results 1:1** — 방법마다 결과가 있고 결과마다 방법이 있는가.
3. **가설 → 분석 → 해석 평행성** — 세 위치의 순서가 같은가.
4. **Abstract ↔ 본문** — 한쪽에만 있는 핵심 주장이 있는가.
5. **Scope Discipline** — 표본·시기·공간보다 넓은 결론을 설계하는가.

부분 범위에서는 전체 통과 판정을 하지 않고 내부 구조와 경계 간선만 판정한다.

## 섹션 단위

- Introduction에 Gap이 없어 목적이 서지 않음
- Discussion이 Results를 반복하고 해석·기작이 없음
- Results에 문헌 비교가 섞여 Discussion과 중복
- Conclusion이 요약만 하고 함의가 없음
- Methods 절차가 Results에 나타나지 않음

학위논문 장이나 연구계획서는 `section-checklists.md`의 해당 부분만 읽는다.

## 단락 순서

`cohesion_flow.md`에서는 Paragraph Architecture와 주제 전개 패턴(Daneš)만 쓴다.
Linear / Constant / Derived / Split Rheme 가운데 어느 패턴이 어디서 깨졌는지
설명한다. 문장 수준 Given-New는 mapping에서 판정하지 않는다.

## 설계 단계에서 보지 않는 것

명사화·태·시제, 문장별 헤징, 군더더기·연어·관사, 문장 리듬, 표기 정밀도는
proofreading·rewriting 소관이다. 단 Figure·Table 모순이나 Ledger first-report
중복은 구조 결함이므로 mapping에서 다룬다.

## 문제를 결정으로 바꾸기

1. 규칙 이름과 문제 결과를 한 줄로 적는다.
2. 영향 범위와 되돌리기 비용으로 우선순위를 정한다.
3. 추천안과 대안 비용을 만든다.
4. `D-###`로 결정 대장에 등록한다.
5. 현재 범위의 최고 우선순위 결정 하나만 질문한다.

좋음:

```text
[Gap · high · INTRO]
Gap 단락이 없어 목적 단락이 왜 필요한지 서지 않습니다.
추천은 P2 마지막 주장과 Chen2024의 한계를 분리해 P3 Gap으로 두는 것입니다.
```

나쁨: `서론 흐름이 조금 어색합니다. 어떻게 할까요?`

## 발화 상한과 배출·은퇴

- 한 응답의 구조 문제 요약은 최대 3개
- 질문은 결정 하나
- 네 번째 이후는 `detected` 결정으로 등록
- "이 밖에 N개는 대기열에 등록했습니다" 한 줄이면 충분
- 해결 항목은 `resolved`로 바꾸고 활성 대기열에서 제외
- 결번은 정상이며 ID를 당기지 않음

상한은 지금 말할 개수이고 결정 생명주기는 보이지 않는 적체를 막는 하수구다.

## 부분 mapping 발화

다음만 말한다.

1. 대상 범위를 막는 상위 blocker
2. 현재 범위 내부 핵심 문제
3. 현재 변경의 범위 밖 파급

관련 없는 섹션의 low·mechanical 항목은 숨긴다. 범위 밖 수정은 자동으로 하지 않고
결정을 `reopened` 또는 신규 등록한다.

## 사용자 판단과 규칙 충돌

규칙 근거를 대고 한 번 반대한다. 재확인하면 따르고 사용자가 택한 안, 충돌,
선택 이유, 영향 범위, 재개방 조건을 결정 이력에 남긴다.
