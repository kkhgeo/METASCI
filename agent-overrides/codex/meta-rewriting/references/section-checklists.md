# 섹션별 구조 체크리스트 — 근거 기반 규범

2026-07-16 최초 작성 · 2026-07-23 개정 | 근거 등급: 각 항목에 [1차: 출판 문헌] / [보조: @ScholarshipfPhd 커뮤니티 공명도(조회·북마크)] 표기.
1차 문헌 전문은 원래 프로젝트의 `papers/` 및 `books_guides/`에 보관되었다. 이 스킬의 런타임은 해당 개발 경로에 의존하지 않는다.

**사용 규칙 (SKILL.md ②에서 호출) — 두 층위를 구분한다:**
- **항상 적용**: `문장 스타일 공통`과 `인용·참고문헌 규범`은 섹션 유형과 무관하게 성립하므로, 섹션을 식별하지 못한 단락에도 적용한다.
- **섹션 식별 시에만 적용**: 각 섹션 전용 블록은 단락의 섹션 유형이 명시되었거나 확실히 식별될 때만 대조한다. 불확실하면 추측하지 말고 건너뛴다.
- 체크 항목 위반은 ③ 진단표에 포함한다. 구조 위반의 기본 심각도: 섹션 필수 요소 누락 = 高, 요소 순서·배치 문제 = 中, 관례 이탈 = 低.
- principles.md의 일반 원칙(정보구조·지시어·hedging)이 항상 우선하며, 이 파일은 섹션 특이적 추가 기준만 제공한다.

> **2026-07-23 개정 근거.** `Writing_Principles_Extraction` 원리 은행(27개 소스, 대표 원리 185개)과 대조해 회수분을 반영했다. 은행은 모든 소스를 동등 취급하고 **수렴 수**로 신뢰를 표현하지만, 이 파일은 **권위 등급제**를 유지한다 — 추가된 항목이 전부 출판 문헌 지지를 갖고 있어 무손실로 번역되었고, 트윗만 지지하는 항목은 0건이었다. 수렴 수는 본문에 넣지 않는다: 이 파일 안에서는 수렴이 높을수록 이미 반영되어 있어 진단 가치와 역상관이기 때문이다(수렴 최상위 "저널 지침 준수"는 단락 진단 가치 0, 이번 최대 수확인 Methods 통계 블록은 수렴 1).

---

## Title / 제목 (사용자가 제목을 제시했을 때)

체크 [1차: Tullu 2019, *Saudi J Anaesth* 13(S1):S12-S17 — 원문 대조 완료 2026-07-16; 보조: Scholar 제목 가이드 2025-06-16]:
- [ ] 핵심 속성 충족 — "descriptive, direct, accurate, appropriate, concise, precise, unique, **not misleading**" (Tullu의 명시 목록)
- [ ] **약어·두문자어 금지** — 비전문 독자가 건너뛰게 만들고 비표준 약어는 혼동 유발
- [ ] 임상·실증 연구는 **PICO 요소 포함 시도** (Patients/대상, Intervention, Comparison, Outcome)
- [ ] **검색용 키워드가 제목에 포함**되어 있는가 — 색인·검색엔진 회수 목적
- [ ] 길이 최적화 — 긴 제목은 산만("boring and unfocused"), 극단적으로 짧으면 내용 대표성 상실; 저널 규정 준수
- [ ] 내용과의 정합 — 본문이 입증하지 않는 범위를 제목이 약속하지 않는가 (misleading = 高)
- 참고: 제목 유형은 descriptive / declarative / interrogative 3종 — 유형 자체는 선택이나 분야 관례 확인

## Literature Review / 문헌고찰

텍스트에서 진단 가능한 규칙 [1차: Pautasso 2013 Rules 5·6·7·9·10 — 원문 대조 완료 2026-07-16; 1차 보강: Koons et al. 2019 *Ann Biomed Eng* 47(11) (PDF 보유); 보조: Paul & Criado 2020 (closed, DOI만), Scholar 문헌고찰 21건]:
- [ ] **비판적 스탠스** — 단순 요약 나열("A는 X를 발견했다. B는 Y를 발견했다...")이 아니라 평가·종합이 있는가 (Rule 6 "Be Critical and Consistent") — 나열형 = 高
- [ ] **논리적 구조** — 연대순/주제별/방법론별 등 식별 가능한 조직 원리가 있는가 (Rule 7)
- [ ] **공백 도출로 수렴** — 리뷰가 "그래서 무엇이 미해결인가"를 향해 서사적으로 진행하는가
- [ ] **초점 유지 + 폭넓은 관심** — 리뷰 대상이 명확히 한정되면서도 인접 독자에게 유의미한가 (Rule 5)
- [ ] **자기 연구의 객관적 취급** — 저자 자신의 선행연구를 과대 비중 없이 다루는가 (Rule 9)
- [ ] **최신성과 고전의 균형** — 최근 문헌만도, 낡은 문헌만도 아닌가 (Rule 10 "Be Up-to-Date, but Do Not Forget Older Studies")
- [ ] (체계적 고찰·메타분석 한정) **검색 전략이 본문에 명시**되어 있는가 — 데이터베이스, 검색어, 기간, 포함·배제 기준. 재현 불가능한 리뷰는 서사일 뿐 (누락 = 高) [1차: Koons et al. 2019; Pautasso 2013 Rule 3]

## Abstract / 초록

5요소 구조 — 각 요소 1-3문장 [1차: Nature Summary Paragraph 공식 주석 템플릿(B7); 보조: Scholar 초록 스레드 다수, 조회 5만+]:

1. **Background** — 연구 대상과 맥락
2. **Justification/Gap** — 왜 지금 이 연구인가
3. **Methods** — 핵심 접근법만 (파라미터 수준 세부 금지)
4. **Results** — 주요 결과 (핵심 수치 포함)
5. **Conclusion/Implication** — 독자가 가져갈 한 문장

체크:
- [ ] 5요소가 모두 존재하고 이 순서인가
- [ ] **초록에 참고문헌 인용 없음** [1차: Ecarnot 2015 — "There should be no references in an abstract"]
- [ ] 결론이 결과를 단순 반복하지 않고 함의를 진술하는가
- [ ] 저널 단어 수 제한 준수 (일반 150-300w) [1차: Perneger 2004, 저널 지침 준수]
- [ ] **"in this paper" 류 자기지시 회피** + 일반론적 동기 서술 금지("인터넷의 중요성을 정당화할 필요 없다") [1차: Schulzrinne]
- [ ] **자기완결성 — 본문을 가리키는 표현 금지** ("as described above", "in Figure 2", "아래에서 논의하듯이"). 초록은 서지 DB에서 단독 유통되므로 전문 없이 홀로 읽혀야 한다 (본문 참조 = 高) [1차: Ecarnot 2015 — "should form an independent unit that is comprehensible as a stand-alone text"]
- [ ] **결과의 제시 순서** — 1차 평가변수(주 결과) 먼저, 2차 결과 뒤. 방법에 언급한 항목에 대응 결과가 있는가 [1차: Ecarnot 2015 Table 4]
- [ ] **배제 항목** — 비표준 약어, 평가적 진술("Surprisingly, we observed…"), 표·그림·삽화 [1차: Ecarnot 2015 Table 4 — "no discussion, or no judgemental statements"]
- [ ] 첫 1-2문장이 인접 분야 밖 독자에게도 읽히는가 — 도입부 전문용어 밀도 (低~中) [1차: Nature Summary Paragraph 템플릿(B7) — 첫 문장은 넓은 독자 대상]

## Introduction / 서론

3-move 구조 [1차: Perneger 2004 Table 1]:

1. **중요성** — 다루는 문제가 왜 중요한가
2. **공백** — 현재 지식에서 무엇이 결여되어 있는가
3. **목적** — 연구 질문/목표의 명시적 진술

체크:
- [ ] **연구 질문이 명시적으로 문장화**되어 있는가 — 독자가 추측하게 두는 것은 결격 (高) [1차: Perneger 2004 — "The research question should always be spelled out, and not merely left for the reader to guess"]
- [ ] 연구 질문의 3속성: specificity / originality / relevance [1차: Perneger 2004]
- [ ] 목적 진술이 동어반복("we describe what we did")이나 모호("we explored issues related to X")하지 않은가 — Perneger Table 2의 흔한 실수 (高)
- [ ] 서론이 문헌 종합 리뷰로 비대해지지 않았는가 — "neither necessary nor desirable" [1차: Perneger 2004]
- [ ] 문제 진술(problem statement): 공백의 실재 + 중요성 + 검증 가능성을 갖추었는가 [보조: Scholar 문제진술 스레드, 5회 재게시·누적 조회 10만+]

- [ ] **공백 진술의 구체성** — "연구가 부족하다/알려진 바 없다" 류 추상 공백이 아니라, 공백이 초래하는 구체적 결과·수치로 중요성을 입증하는가 [1차: IUFRO pp.58-60 — 계획서 규칙이나 서론 공백 진술에 동일 적용]
- [ ] (학위논문·긴 논문 한정) 서론 말미 로드맵 문장 — 이후 구성 예고 [보조: Scholar]
- [ ] **마무리 순서** — 공백 진술 → 작업가설 → 목적 → (한 줄) 목적 달성 전략. 가설을 세우는 분야인데 가설 없이 목적으로 건너뛰면 결격 (순서 이탈 = 中) [1차: Ecarnot 2015 — "clearly state your working hypothesis, followed by your objective(s), and very briefly, the strategy"]

서론 시제 규칙 [1차: Ecarnot 2015 Table 2 — 원문 대조 완료]:
- 확립된 지식 → **현재** ("Cancer is a common disease")
- 타인의 선행 관찰 → **과거** ("Smith et al. showed that...")
- 과거 시작·미완의 흐름 → **현재완료** ("Several researchers have investigated...")
- 가설 정식화 → **첫 동사 과거 + 둘째 동사 현재** ("We hypothesized that drug A increases...")
- 목적 진술 → **과거** ("We aimed to measure...")

## Methods / 연구 방법

체크 [1차: Perneger 2004 Table 1 — 8요소]:
- [ ] 맥락·세팅 / 연구 설계 / 대상 집단 / 표집 전략 / 개입(해당 시) / 주요 변수 / 자료수집 도구·절차 / 분석 방법
- [ ] **재현 가능 수준의 구체성** — "specific, concrete, technical, and fairly detailed" [1차: Perneger 2004]
- [ ] 시제: 수행한 일은 **과거시제** [1차: Ecarnot 2015 시제 표]
- [ ] **설계 명시로 시작** — 관측/실험, 전향/후향, 무작위 여부, 대조·눈가림 등 [1차: Ecarnot 2015]
- [ ] **비통상적 방법 선택의 정당화** — 관례에서 벗어난 설계·기법에 참고문헌·지침 또는 그 선택을 요구한 구체적 맥락이 붙어 있는가. 절차만 나열되고 근거가 전무하면 결함 (中) [1차: Ecarnot 2015 — "Any choices of unusual methodology... should be justified"]
- [ ] **왜 그 방법이 그 결과를 주는가** — 무엇을 했는지만 있고 그 절차가 어떻게 답을 산출하는지 연결이 없는가 (中) [1차: Schulzrinne; Lund Module 4]
- [ ] (해당 분야) **1차·2차 평가변수와 각각의 측정 방법 명시** — 무엇이 주 결과인지 불명확하면 결과 해석 전체가 흔들린다 [1차: Ecarnot 2015 — "the choice of the primary endpoint is critical"]

통계 서술 블록 [1차: Ecarnot 2015 — 방법의 마지막 단락]:
- [ ] **데이터 제시 형식** 선언 — 평균±SD / 중앙값[IQR] / n(%) 중 무엇을 쓰는가
- [ ] **변수 유형별 검정** 명시 — 어떤 변수에 어떤 검정을 적용했는가
- [ ] 다변량 분석 시 **투입 변수** 명시
- [ ] **표본수 산정 근거**(해당 시), **유의수준**, **다중비교 보정** 여부
- [ ] **소프트웨어·버전** 명시
- [ ] **하위집단 분석은 사전 명시** — 사후 분석을 사전 계획인 것처럼 서술하지 않는가 (高)

윤리 진술 블록 [1차: Ecarnot 2015 — "A short note regarding ethical considerations must be included"]:
- [ ] 인간·동물 대상 연구에 **윤리위원회 승인**(또는 미해당 사유) 진술이 있는가
- [ ] **서면 동의** 취득 진술 (해당 시)
- [ ] 임상시험이면 **등록번호** 기재
- 주의: 승인번호·등록번호는 사실 정보다. 초고에 없으면 결손으로 지적하되, 리라이팅에서 만들어 넣지 않는다.
- [ ] **Methods–Results 짝 규칙**: Results에 제시될 모든 결과에 대응하는 방법 서술이 존재하는가 — "you cannot present the results of a test or analysis that was not mentioned in the methods" (짝 없는 결과 = 高) [1차: Ecarnot 2015 — 원문 대조 완료]

## Results / 연구 결과

- principles.md **원칙 8** (question–data–answer 템플릿, C-C-C)이 1차 기준 — 중복 기재하지 않음.
- 추가 체크 [1차: Perneger 2004]:
  - [ ] 연구 질문 관련 결과는 빠짐없이, **백분율에는 빈도 동반, P값에는 효과크기 동반** (Table 2의 선택적 보고 실수)
  - [ ] **수치 보고 완전성** — 값에 n과 산포(SD/SEM/IQR)가 동반되는가, 추정치에 신뢰구간이 있는가. 중심경향만 단독 제시 = 中 [1차: Fisher et al. (Liebert); Perneger 2004의 선택적 보고 원리 연장]
  - [ ] **본문/표/그림 배분** — 1-2줄로 서술되는 결과는 본문, 둘 이상 집단의 동일 변수 비교는 표, 복잡하거나 해석이 어려운 원자료·추세는 그림. 표로 갈 것이 본문에 풀어 쓰여 있지 않은가 (中) [1차: Ecarnot 2015]
  - [ ] **불리·무의미한 결과의 은폐** — 기대와 다르거나 유의하지 않은 결과가 완곡화·누락되지 않았는가 (高) [1차: Ecarnot 2015 — 음성 결과도 유효한 기여]
  - [ ] 같은 결과를 표와 본문에 중복 제시하지 않음 (中)
  - [ ] 연구 질문과 무관한 표·비필수 결과 나열 금지 — "resist the temptation" (中)
  - [ ] 해석·논평은 Discussion으로 — Results는 사실 보고
  - [ ] 시제: 관찰·수행 보고는 과거 [보조: Scholar 시제 가이드 — 관례 등급, Ecarnot Table 2의 원리 연장]
  - [ ] **그림·표 캡션 자기완결성** — 본문 없이 캡션만으로 이해 가능해야; 그래프 서술은 시각적으로 자명한 것("부하가 늘면 지연이 는다")의 반복이 아니라 관계의 설명이어야 [1차: Schulzrinne]

## Discussion / 논의

5-move 구조 [1차: Perneger 2004 Table 1]:

1. 주요 발견 요약 → 2. 선행연구 대비 해석 → 3. 함의(정책·실무) → 4. 강점·한계 분석 → 5. 향후 연구 전망

체크:
- [ ] 첫 단락이 연구 질문에 대한 답으로 시작하는가
- [ ] 한계 절이 존재하고 방어적 최소화로 흐르지 않는가
- [ ] hedging 보정 — principles.md 원칙 6 적용 (결과의 인식론적 강도에 맞는 동사 선택)
- [ ] Discussion이 결과 재나열로 채워지지 않았는가
- [ ] **서론의 공백을 되짚는가** — 서론이 주장한 지식 공백을 이 연구가 실제로 메웠는지, 무엇을 새로 더하고 무엇을 반박하는지 명시 진술이 있는가. 없으면 "또 한 편"으로 읽힌다 (中) [1차: Ecarnot 2015 — "you can discuss whether or not your paper has succeeded in filling the gap"]
- [ ] **범위 이동(scope creep) 검출** — 표본에서 관찰한 것이 모집단 진술로 확대되지 않았는가. "25개 중 20개에서 관찰" → "80%가 그렇다"는 원자료를 배신하는 미묘한 도약 (高) [1차: Ecarnot 2015 — "a subtle shift in interpretation that belies that original data"]
- [ ] **선행연구 비판의 어조** — 타인 연구의 약점을 직접 지적하는 대신("X et al. failed to…") 자기 연구의 강점 진술로 함의를 전달하는가 (低~中) [1차: Ecarnot 2015 — "it pays to be diplomatic when criticizing the work of others"]

## Conclusion / 결론

Discussion과 별개의 결론 절을 둔 원고에 적용. Discussion 단락이면 위 항목을 쓴다.

체크 [1차: Ecarnot 2015; Hon (UF); Fisher et al. (Liebert)]:
- [ ] **새 정보 도입 금지** — 본문에 없던 데이터·결과·인용이 결론에서 처음 등장하지 않는가 (高)
- [ ] 결과의 재나열이 아니라 **종합**인가 — 개별 수치가 아니라 전체가 무엇을 뜻하는지
- [ ] 서론의 연구 질문에 대한 **답이 명시**되어 있는가 (서론 공백 진술과 대응)
- [ ] 이론적·실용적 **기여 진술**이 있는가
- [ ] hedging 유지 — 결론에서 갑자기 주장 강도가 올라가지 않는가 (principles.md 원칙 6) (高)
- [ ] 인용 최소 (0-2개, 맥락 설정 시에만)

## 학위논문 장 단위 (Thesis/Dissertation)

5장 표준 구조 [1차: Hon (UF) Guidelines; Fisher et al. (Liebert) 가이드북; 보조: Scholar 5장 구조 스레드, 조회 2.4만]:

1. Introduction · 2. Literature Review · 3. Methodology · 4. Results · 5. Conclusion & Recommendations

체크:
- [ ] 장별 역할 침범 없음 (예: 방법 서술이 결과 장에 등장 = Perneger Table 2 "chaotic structure")
- [ ] 문헌고찰이 나열이 아니라 공백 도출로 수렴하는가 [1차: Pautasso 2013 Rule 10 — 리뷰는 서사가 있어야]

## Research Proposal / 연구계획서

구조 — 9구성요소 [1차: IUFRO 핸드북 Ch.7 (PDF 보유, pp.52-63); 보조: Scholar 계획서 스레드 다수(최대 6.8만 조회)]:
Summary → Introduction → **Statement of Problem/Need** → Project Description(Objectives·실험계획·결과확산·시설·인용문헌) → Budget → Budget 정당화 → 특별 고려사항 → CV → 부록

체크:
- [ ] **Summary 필수 6문장** — 신뢰성·문제/필요·연구목표·방법·자원 수요·기대 성과 각 1문장 이상, 1쪽(300-500단어) 이내
- [ ] **문제 진술 금지 문구** — "little is known about...", "there is a general lack of information...", "no research has dealt with..." 금지 → **구체적 결과·통계로 대체** ("1만 헥타르 낙엽 피해로 Y의 경제 손실" 식) (금지 문구 사용 = 高)
- [ ] Objectives: **1-2문장, 측정·검증 가능한 성과**, 페이지에서 눈에 띄게; 능동 동사(to increase/reduce) 우선, to provide/establish 회피
- [ ] Objectives(무엇을·언제) ≠ Methods(어떻게) ≠ Goals(추상 지향) — 세 층위 혼동 금지 (中)
- [ ] 통계적 영가설을 목표로 진술하지 말 것

## 문장 스타일 공통 (모든 섹션 — ② 논의에서 문장 수준 진단 시 적용)

간결성 — 4결함 유형 [1차: Lund 가이드 12항 퇴고 체크리스트(pp.144-145)·클리셰 목록(p.125); Schulzrinne; Williams & Bizup *Concision*; 보조: Scholar 다수(최대 4.2만 조회)]:
- [ ] **무의미 강조부사** — very, really, just, clearly, actually: 삭제하거나 더 강한 단어로 대체 (低)
- [ ] **클리셰·상투구** — at the end of the day, in this day and age, last but not least, part and parcel 등: "자리만 차지하고 기여하지 않음" (低)
- [ ] **메타담화 과잉** — "It is important to note that...", "in this paper"(초록에서 특히: "여기서 다른 논문 얘기를 하겠는가") (低~中)
- [ ] **장황 구문** — "due to the fact that"→because, "a majority of"→most (低)

문장 운용 [1차: FESS pp.31-33; Lund p.123]:
- [ ] **만연체 수치 테스트** — 등위접속사(and/but/so)가 한 문장에 2개 초과면 만연체 의심; "and"-체이닝(...and...and...and) = 中
- [ ] **문장 길이 변주** — 단문만 연속 = 단조/유아적, 복문만 연속 = 난독; 혼합이 정답
- [ ] run-on(융합문)·comma splice·fragment — 두 주절은 세미콜론/접속사/마침표로만 연결, 종속절 단독 사용 금지 (中~高) [1차: Lund pp.135-138]
- [ ] 제한적 vs 비제한적 관계절의 콤마 — 의미가 달라짐 ("All the students who..." 부분집합 vs "All the students, who..." 전체); that 앞 콤마 금지 [1차: Lund pp.132-134]

격식 레지스터 [1차: Lund p.117, pp.120-125; FESS pp.9-11; 보조: Scholar]:
- [ ] **축약형 금지** — don't → do not (아포스트로피 스캔으로 즉시 검출) (低)
- [ ] 비격식어 치환 — a lot of→many/numerous, get→obtain, 문두 And/But 회피, 모호어(thing/stuff) 금지
- [ ] 느낌표 사용 금지(생략부호 …는 생략 표시로만), 허세어 회피(vociferate→shout: 이유 없는 현학은 "pompous")
- [ ] **객관 톤** — 가치판단("greatest of all time"→"most productive of his time"), 빈정거림 따옴표('evidence') 제거 [1차: Lund pp.120-121 수정 예문]
- [ ] 포괄적 언어 — 총칭 he→singular they, policeman→police officer [1차: Lund pp.121-122]

기타 [보조 등급 — 관례로서 견고]:
- [ ] **능동태 기본값** — "We conducted..." > "The experiment was conducted..." — 단, **old 정보를 문장 앞으로 보내는 수동태는 정당** (principles.md 원칙 1이 우선; "수동태 금지"를 기계 적용하지 말 것)
- [ ] 약어는 본문 첫 등장 시 풀어쓰기 정의 (표준 약어 제외)
- [ ] 인용동사 다양화 — shows/found만 반복하지 말고 저자 태도를 담은 동사(argues, demonstrates, contends, suggests) 선별 [보조: Scholar 최고 참여 트윗(11.3만 조회); Hyland의 stance 연구와 인접]
- [ ] **논리 층위 병렬** — principles.md 원칙 8의 Parallelism은 *문법 형태*를 다룬다. 여기에 *개념 차원*을 더한다: 나열된 항목이 서로 같은 차원의 범주인가. 문법이 완벽해도 차원이 섞이면 결함이다 (예: "온도, 강수, 그리고 정책 수용 장벽" — 앞 둘은 물리 변수, 셋은 제도 요인) (中) [1차: Lund Module 4; FESS pp.31-33]
- [ ] **미수치화된 크기 진술** — "significant improvements", "substantially higher"처럼 정도를 주장하면서 수치가 없는가. principles.md 원칙 6이 다루는 *확실성* 축과 별개인 *정밀도* 축이다. **플래그 전용** — 진단표에 올리되 리라이팅에서 수치를 만들어 넣지 않는다 (中) [1차: Fisher et al. (Liebert); Schulzrinne]

## 인용·참고문헌 규범 (모든 섹션 공통)

체크 [1차: Perneger 2004 — 원문 대조 완료]:
- [ ] **핵심 주장(key assertions)에 인용이 붙어 있는가** — 방법·도구 출처 포함 ("Key assertions should be referenced, as well as the methods and instruments used")
- [ ] **그레이 문헌 회피** — 미출판 자료, 기술보고서, 독자가 찾기·이해하기 어려운 출처 인용 금지 (中)
- [ ] **망라적 인용 불필요** — 종설이 아닌 한 모든 문헌을 인용할 필요 없음; 인용 과밀은 초점 상실 신호 (低)
- [ ] 직접인용 과다 회피 — 학술 산문에서는 패러프레이즈가 기본, 인용부호 남용 시 종합 부재 신호 [보조: Scholar 40 Tips]
- [ ] 초록에는 인용 금지 [1차: Ecarnot 2015 — 초록 섹션에 기재됨]
- [ ] **When NOT to cite** — 분야 상식, 본인의 아이디어·실험 결과, 논쟁 없는 배경 지식, 공용 지식에는 인용 불필요; 과잉 인용은 종합 능력 부재 신호 [보조: Scholar (1.3만 조회, 10항목)]

---

## 부록 A — AI 사용 규범 (사용자가 AI 보조 작성을 언급할 때만 적용)

- **AI 감지기 결과를 표절/부정의 확정 증거로 취급하지 말 것** — 낮은 유병률 하에서 오탐률 급증 [1차: Tsigaris & Teixeira da Silva 2026, *Next Research* 7:101396]
- **AI 출력은 비판적 평가·수정·통합을 동반할 때만 연구역량에 유익** — 수동 수용은 무익 [1차: Zhu & Yang 2026, *Behav Sci* 16(2):304]
- **비원어민의 언어 장벽 제거는 정당하고 효과적인 사용** — 비원어민 성취 87.5→95.8%로 원어민과 동등 [1차: Connell Pensky et al. 2025, *IJAIED*]
- 허용: 문법·명확성 개선, 개요 생성, 문헌 요약, 언어 다듬기 / 금지: 인용 조작, 무검토 전체 생성, 가짜 참고문헌, AI 정책 우회 [보조: Scholar AI 윤리 스레드 2026-06-15, 조회 1.4만; Huang & Tan 2023 *Am J Cancer Res* 13(4)와 합치]
- 비원어민 저자 권고: 원어민/에디터 검토 병행 [1차: Perneger 2004 — "do have a native speaker edit the manuscript"]

## 부록 B — 투고 직전 공통 점검 (사용자가 "투고 전 점검" 요청 시)

Perneger 2004 Table 2의 흔한 실수 중 단락 수준에서 검출 가능한 것:
- 연구 질문 미명시 / 동어반복적 목적 진술 / 섹션 역할 침범 / 선택적 결과 보고(빈도 없는 %, 효과크기 없는 P) / 표-본문 중복

---

## 출처 (전문 보관 위치: X_ScholarshipfPhd_KnowledgeDB)

- Perneger & Hudelson (2004). *Int J Qual Health Care* 16(3):191-192. — `papers/Perneger_2004_...pdf` (원문 대조 완료 2026-07-16)
- Ecarnot et al. (2015). *Eur Geriatr Med* 6(6):573-579. — `papers/Ecarnot_2015_...pdf` (원문 대조 완료 2026-07-16 · **전문 재채굴 2026-07-23** — 통계·윤리 블록, 초록 자기완결성, 범위 이동 등 이번 증분의 대부분이 이 논문에서 나왔다)
- Nature Summary Paragraph 공식 템플릿 — `books_guides/B7_Nature_summary-paragraph.pdf`
- Hon, L.C. Guidelines for Writing a Thesis or Dissertation (UF) — `papers/Hon_...pdf`
- Fisher et al. Guidelines for Writing a Research Paper for Publication (Liebert) — `papers/Fisher_2013_...pdf`
- Pautasso (2013). *PLoS Comput Biol* 9(7):e1003149 — `papers/Pautasso_2013_...pdf`
- Tsigaris & Teixeira da Silva (2026); Zhu & Yang (2026); Connell Pensky et al. (2025); Huang & Tan (2023) — `papers/` (P1은 PDF 미확보, DOI: 10.1016/j.nexres.2026.101396)
- Tullu, M.S. (2019). Writing the title and abstract for a research paper. *Saudi J Anaesth* 13(S1):S12-S17. — `papers/Tullu_2019_...pdf` (원문 대조 완료 2026-07-16)
- Koons, G.L., Schenke-Layland, K., & Mikos, A.G. (2019). Why, When, Who, What, How, and Where for Trainees Writing Literature Review Articles. *Ann Biomed Eng* 47(11):2334-2340. — `papers/Koons_2019_...pdf`
- Paul, J., & Criado, A.R. (2020). The art of writing literature review. *Int Business Review* 29(4):101717. — PDF 미확보(구독 전용), DOI: 10.1016/j.ibusrev.2020.101717
- Lund University (2020). *Writing in English at University: A Guide for Second Language Writers*. — `books_guides/B3_...pdf` (Module 4 채굴 완료 2026-07-16)
- FESS. *Academic Writing: A Handbook for Learners in the FET Sector*. — `books_guides/B6_...pdf` (pp.9-38 채굴 완료)
- Schulzrinne, H. *Writing Technical Articles* (Columbia). — `books_guides/B5_...html`
- IUFRO. *Handbook for Preparing and Writing Research Proposals*. — `books_guides/B1_...pdf` (Ch.7 채굴 완료)
- @ScholarshipfPhd 트윗 코퍼스 (1,051건, 2023-02~2026-07) — `tweets/tweets_raw_1051.json`
- 원리 은행 (2026-07-23 대조) — 개발 프로젝트의 `Writing_Principles_Extraction/bank/` (27개 소스, 대표 원리 185개)

---

**Version**: 1.1.0
