# 매뉴얼 인덱스 — 층별 라우팅

## 무엇을 판단할 때 무엇을 읽나

| 판단 대상 | 읽을 파일 | 층 | 판정 권한 |
|---|---|---|---|
| 문장 규칙·번역투·피동·호응·간결성 | `L1_sentence_rules.md` | L1 | **결정적** |
| 단락 길이·주제·두괄식·접속어 상한 | `L1_paragraph_rules.md` | L1 | **결정적** |
| 수치 일관성·백분율·유효숫자·2차 출처 | `L1_quantitative_integrity.md` | L1 | **결정적** |
| 논거 개수·반론 대응·통일성·구조 | `L2_argument_rubric.md` | L2 | **패널 과반** |
| 섹션 간 정합(질문 사슬·초록↔본문) | `L2_structural_integrity.md` | L2 | **패널 과반** |
| 응집성·어휘 선택·문체·주제 전개 | `L3_style_cohesion.md` | L3 | **판정 없음** |
| 지적에 출처를 붙일 때 | `sources.md` | — | — |

---

## 로딩 순서

```
PHASE 2 (L1)  L1_sentence_rules.md
              L1_paragraph_rules.md
              L1_quantitative_integrity.md   ← 수치·인용이 있을 때만
PHASE 3 (L2)  L2_argument_rubric.md
              L2_structural_integrity.md     ← Mode 1·2만
PHASE 4 (L3)  L3_style_cohesion.md
전 구간       sources.md                      ← 출처 표시할 때마다
```

**L1을 먼저 도는 이유**: L1에서 걸린 문장은 L3 후보 생성 대상에서 뺀다.
곧 교정될 문장의 문체 대안을 만드는 것은 낭비다.

---

## 모드별 실행 가능 범위

| | Mode 1 원고 전체 | Mode 2 섹션 | Mode 3 단락 |
|---|---|---|---|
| L1 문장·단락 | ○ 전량 | ○ | ○ |
| L1 수치 정합 | ○ | ○ | △ 단락 내부만 |
| L2 논증 준거 | ○ | ○ 섹션 내부 | △ 단락 수준만 |
| **L2 섹션 간 정합** | ○ | △ 인접 섹션만 | **× 판정 불가** |
| L3 문체·응집성 | ○ 표본 | ○ | ○ |

**Mode 3에서 `L2_structural_integrity.md`의 섹션 간 판정은 할 수 없다.**
질문 사슬, Abstract↔본문, 명제 일관성은 양쪽 섹션이 다 있어야 판정된다.
**못 한다고 말하지, 통과한 것처럼 굴지 않는다.**

---

## 층 표기 — 출력에 반드시 구별되게

```
[L1 · 확정]   규칙 위반. 교정형 + 출처·쪽수
[L2 · 확정]   리뷰어 과반 지적. 준거명 + 배점
[L2 · 소수]   1인 지적. 확정 아님
[L3 · 선택]   후보 N개. 최적 없음. 저자 결정
[L3 · 충돌]   Blueprint(기술적) vs 매뉴얼(처방적). 판정 안 함
[판정 불가]   모드 제약
```

---

## 두 개의 빌려온 파일

`L1_quantitative_integrity.md`와 `L2_structural_integrity.md`는 `meta-proofreading`
(영문판)에서 가져왔다. **언어와 무관한 층위**이기 때문이다 — 수치가 맞는가,
섹션끼리 아귀가 맞는가는 한국어든 영어든 같은 판정이다.

영어 특정 파일 — `sentence_craft.md`(명사화·태·시제), `stance_hedging.md`(hedge·
booster·self-mention), `cohesion_flow.md`(Given-New·acronym discipline),
`advanced_nns_issues.md`(collocation·**관사**) — 은 가져오지 않았다.
특히 마지막은 비원어민의 **영어** 잔여 결함을 다루며, 한국어에는 관사가 없다.

그 자리를 `L1_sentence_rules.md`(번역투·피동·조사 호응)와
`L3_style_cohesion.md`(응집성·어휘)가 대신한다.
