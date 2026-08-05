# CHANGELOG — meta-proofreading

버전 표기가 없던 스킬이다. `meta-writing`·`meta-rewriting`과 맞추기 위해 이번에 도입하고,
직전 GitHub 상태를 **1.0.0**으로 소급 지정한다.

## 1.1.0 (2026-07-23)

`Writing_Principles_Extraction` 원리 은행(27개 소스, 대표 원리 185개)과 대조했다.
네 번째 대조 검토이며, **이미 커버된 비율이 가장 높았다**(70개, 38%).

| 판정 | meta-proofreading | mywriting-korean | meta-rewriting | meta-writing |
|------|------------------|------------------|----------------|--------------|
| 적용 가능 | 36 (19%) | 12 (6%) | 25 (14%) | 52 (28%) |
| 이미 커버됨 | **70 (38%)** | 21 (11%) | 65 (35%) | 46 (25%) |
| 충돌 | 7 (4%) | 36 (19%) | 7 (4%) | 7 (4%) |

writing-manual이 Swales CARS·Hyland metadiscourse·Gopen & Swan·Daneš·Williams &
Bizup에 기반해 은행보다 이론적으로 정교하다. 은행의 "signpost 표현"은 여기선 Hyland의
frame/endophoric marker로, "보고 동사 다양화"는 evidential 분석으로 이미 세분화돼 있다.
앞선 두 스킬에서 순증분이었던 항목 대부분이 여기엔 이미 있다 — 2차 인용 추적은
`quantitative_integrity.md`의 Telephone Game 감사 + Agent B의 2차성 점수표로 은행보다
정교하고, 초록 자기완결성·Conclusion 새 정보 금지·Results 수치 완전성도 전부 존재한다.

**따라서 이번 개정의 대부분은 은행에서 가져온 것이 아니라, 대조가 강제한 검토에서 드러난
스킬 자체의 설계 결함을 고친 것이다.**

### 설계 결함 수정

**1. 합의 가산점이 심각도를 압도했다.**
`deliberation.md`의 `impact_score`에서 `reviewer_agreement`가 최대 5점이었다 —
severity 최댓값(4)보다 크다. 다섯이 동의한 사소한 지적이 하나가 발견한 치명적 문제를
이길 수 있었다. 그런데 R1–R5는 **동일 모델·동일 지시**이고 지식 배분과 페르소나만
다르므로, 합의는 독립 검증이 아니라 하나의 사전분포에서 반복 샘플링한 결과다.
상한을 2로 낮추고 근거를 명시했다. Presentation Order의 "Consensus first
(most reliable)"도 "hardest to miss — not necessarily most important"로 고쳤다.

같은 스킬 안에서 두 트랙이 상반된 인식론을 쓰고 있었다는 점이 핵심이다 — CANDIDATES
트랙의 `agent_j.md` 규칙 5는 이미 "Merit, not popularity. 한 리뷰어의 후보가 합의안을
이길 수 있다"로 정확했다. 이제 ISSUES 트랙이 그쪽에 맞춰졌다.

**2. Agent J의 자기선호 편향이 무방비였다.**
`agent_j.md`에 self-preference 언급이 0건이었다. 그런데 Process 5는 Agent J가
SYNTHESIZED 후보를 **직접 구성해 자기가 채점**하게 한다 — 편향의 정확한 노출 지점인데,
리뷰어의 self_score는 "advisory only"라며 불신하면서 자기 산출물에는 같은 불신을
적용하지 않았다.
- SYNTHESIZED 후보는 최상위 비합성 후보를 **≥3점** 차로 이겨야 선택되도록 마진 상향
- 선택 시 `why_optimal`에 심판 자작안임을 명시하도록 요구
- 규칙 6 신설 — "이 후보가 높은 점수를 받은 이유가 실제로 더 명확해서인가, 아니면
  일반적 학술 관용구에 더 가까워서인가. 저자의 개성적이지만 타당한 표현을 매끄러운
  관용구로 바꾸는 것은 개선이 아니다"
- "원문이 이길 수 있다"가 편향을 상쇄하지 못한다는 점도 명시했다. 이 워크플로에서
  원문은 흔히 상류 AI 스킬의 산출물이므로, ORIGINAL 선택이 인간 기준선 확인이 아니다.

**3. 저자 책임 고지가 전무했다.**
"저자 책임"·"초안"·"최종 검토" 류 문구가 전 파일 0건이었다. 완성 원고에 직접 반영될
텍스트를 생산하는 스킬로서 가장 비용이 큰 누락이다. 세션 요약(§8)에 고지 블록을
신설했다 — 산출물은 초안이며, 최적안 선정은 AI 단독 판정이고, 인용의 실재는 확인하지만
내용 일치는 확인하지 않으며, 투고 전 저널 AI 정책을 확인할 것.
`"최적안 전부 적용"`에는 1회 확인 프롬프트를 붙였다. 이 배치 명령이 문장별 검토 없는
일괄 수락을 명시적으로 지원해, 스킬 전체 설계(문장별 a numbered decision prompt, 후보 전문 표시)를
우회하는 문이었다.

**4. Agent J rubric이 균등 가중이었다.**
LOGIC과 ECONOMY가 둘 다 ×1이라 논리 결함 개선과 어휘 다듬기가 등가였다. 같은 스킬의
`deliberation.md` category_weight는 논리 +2 / 문장다듬기 +0을 쓰고 있어 **내부 불일치**
상태였다. LOGIC을 ×1.5로 올려 두 트랙의 위계를 맞췄다.

**5. 리뷰어 독립성 착시.**
`distribution_strategy.md`는 동일 지시라는 사실을 정직하게 서술하면서도 페르소나 다양성을
장점으로만 기술했다. 상관 오류 위험을 주석으로 명시했다 — 패널은 **coverage device이지
verification device가 아니다.**

### 내용 순증분

**Methods 윤리·설계·통계 블록** (`sections/03_methods.md`). writing-manual 전체에
`ethic/consent/IRB/registration` grep 0건이었다. 신설 항목: 연구 설계 선언, 비통상적
방법의 정당화, 1차·2차 평가변수, 통계 보고 완전성(제시 규약·검정 대응·다변량 투입 변수·
유의수준·다중비교 보정·**하위집단 분석 사전 명시**), 윤리위 승인·동의·등록번호.
계산·기기·2차자료 연구에는 발동하지 않도록 조건을 달았고, 승인번호 등은 사실 정보이므로
리라이팅에서 생성 금지를 명시했다.

**`cross_section/structural_integrity.md` 신설 — 이번 최대 증분.**
Mode 1이 "cross-section coherence, coverage gaps"를 primary focus로 선언해 놓고 정작
그 검사 목록이 없었다. `sections/` 7개는 각 섹션 **내부** 규범만, `cross_section/` 6개는
문장·수치 규범만 다뤘고, 섹션 간 정합성은 `quantitative_integrity.md`의 수치 대조가
유일했다. 신설 파일이 다루는 것: 질문 사슬(서론→논의→결론), Methods↔Results 일대일,
가설→분석→해석 평행 순서, 초록↔본문 대응, 명제 수준 일관성·자기모순·순환논증,
표본→모집단 범위 이동, 초점 프루닝. INDEX Step 4에 Mode 1 상시 라우팅으로 추가했다.

**진단 축 2개** — 병렬 구조의 형태·범주 동질성(`sentence_craft.md` §7; 매뉴얼 전체에
"parallel"이 0회 등장했다), 지시 표현의 실패 조건(`cohesion_flow.md` §6d; §3이 reference를
장치로 나열만 하고 실패 조건을 진단하지 않았다).

### 채택하지 않은 것 (충돌 7건)

가장 위험한 것은 **동의어 변주**다. `cohesion_flow.md`의 Banana Rule("바나나를 길쭉한
노란 과일이라 부르지 마라 — 독자는 동의어 변주를 새 범주 신호로 읽는다")의 정확한 반대
명제여서, 넣으면 리뷰어가 규칙 위반을 능동적으로 생산한다. 지지 소스 5개짜리 항목이라
무비판적 병합 시 유입 가능성이 높았다.

그 밖에 능동태 기본값(매뉴얼은 "voice는 topic position이 결정한다"며 규칙화를 거부),
전환어 추가(매뉴얼은 "flow의 주 수단은 어휘 반복이지 전환어 삽입이 아니다"),
jargon 회피(Banana Rule 및 expert-level 보정과 충돌), 기본 문법 교정(INDEX가 의도적으로
배제한 층위), Nature식 광역 도입부(매뉴얼의 "start one level above the actual topic"과
정반대).

조건부로만 반영 가능한 것들도 배제했다 — 임상 관례(1차 평가변수 우선, 초록 평가어 금지)를
환경·지구과학 원고에 무조건 적용하면 대량 오탐이 나고, INDEX의 "Do not over-flag"·
"Respect disciplinary conventions"를 직접 위협한다.

### 통합 경로 판정

이 스킬은 로컬 지식 파일을 자동 발견해 리뷰어에게 분배한다(`content_files` /
`writing_files`). 은행을 그 채널로 넣는 방안을 검토했으나 **범주 오류**로 판정했다 —
지식 분배는 *프로젝트별* 자료용이고, 은행은 *규범적·프로젝트 독립*이다. 규범은
writing-manual에 속한다. 따라서 채택 항목은 전부 매뉴얼 파일에 직접 이식했다.

> ⚠️ 이 버전부터 GitHub `kkhgeo/METASCI` 의 `skills/metasci_writing/meta-proofreading`과
> 내용이 갈라진다. 직전 상태는
> `~/.claude/skills_backup/meta-proofreading_pre-principles_2026-07-23/` 에 보관되어 있다.

## 1.0.0 (소급 지정)

다중 리뷰어 심의 오케스트레이터. Agent E(지식 발견·분배) / R1–R5(병렬 검토 + 후보 생성) /
Agent J(후보 채점·최적안 선정) / Agent B(레퍼런스 검증), Mode 1·2·3,
writing-manual(sections 7 + cross_section 6).
