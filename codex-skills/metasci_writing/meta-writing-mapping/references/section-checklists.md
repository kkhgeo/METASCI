# 섹션별 구조 규범 — 설계 단계 발췌

교정용 매뉴얼(`meta-proofreading`)에서 **설계 단계에 판정 가능한 항목만** 추린
것이다. 문장이 존재해야 판단할 수 있는 것 — 시제, 문장 스타일, 헤징 강도, 인용
형식, 축약형 — 은 전부 뺐다. 그건 집필 후 `meta-proofreading` 몫이다.

각 항목은 **어떤 단락이 있어야 하는가**, **어떤 순서여야 하는가**를 묻는다.
문장의 좋고 나쁨은 여기서 묻지 않는다.

**읽는 법**
- 지금 논의 중인 섹션 항목만 읽는다. 섹션이 불확실하면 추측하지 말고 건너뛴다.
- **★는 먼저 꺼낼 것.** `rule-routing.md`의 "한 번에 3개까지"에서 무엇을
  고를지의 기준이다.
- 근거 표기는 판정할 때 규칙 이름과 함께 댄다. 표기 없는 항목은 분야 관례다.

---

## Title / 제목

Core message와 직결되므로 설계 단계 사안이다 [Tullu 2019].

- 본문이 입증하지 않는 범위를 제목이 약속하는가 ★ — misleading
- 약어·두문자어 없이 읽히는가
- 검색용 키워드가 들어 있는가
- 임상·실증 연구면 PICO 요소(대상/개입/비교/결과)를 담을 수 있는가

## Abstract / 초록

5요소 구조 — 각 1–3문장 [Nature Summary Paragraph 템플릿]:

1. **Background** 대상과 맥락 → 2. **Justification/Gap** 왜 지금인가 →
3. **Methods** 핵심 접근법만 → 4. **Results** 주요 결과 → 5. **Conclusion** 한 문장

- 5요소가 다 있고 이 순서인가
- **자기완결성** ★ — 본문을 가리키는 표현("아래에서 논의하듯이", "Figure 2 참조")
  없이 홀로 읽히는가. 초록은 서지 DB에서 단독 유통된다 [Ecarnot 2015]
- 결론이 결과의 반복이 아니라 함의를 진술하는가
- 결과 제시 순서 — 1차 평가변수 먼저, 2차 뒤 [Ecarnot 2015]
- 초록에 인용 없음 [Ecarnot 2015]
- 첫 1–2문장이 인접 분야 밖 독자에게도 읽히는가
- 저널 단어 수 제한(일반 150–300단어) 안에 이 배치가 들어가는가

## Introduction / 서론

3-move 구조 [Perneger 2004]: **중요성 → 공백 → 목적**

- **연구 질문이 문장으로 있는가** ★ — 독자가 추측하게 두면 결격
  [Perneger 2004: "should always be spelled out, and not merely left for the
  reader to guess"]
- 목적 진술이 동어반복("우리가 한 일을 기술한다")이거나 모호("X 관련 쟁점을
  탐색했다")하지 않은가 ★ [Perneger 2004 Table 2의 흔한 실수]
- **공백 진술이 구체적인가** ★ — "연구가 부족하다", "알려진 바 없다" 류 추상
  공백이 아니라 공백이 초래하는 구체적 결과·수치로 중요성을 세우는가 [IUFRO]
- 마무리 순서 — 공백 → (가설을 세우는 분야면) 작업가설 → 목적 → 목적 달성
  전략 한 줄. 가설 분야인데 가설 없이 목적으로 건너뛰면 결격 [Ecarnot 2015]
- 서론이 문헌 종합 리뷰로 비대해지지 않았는가 — "neither necessary nor
  desirable" [Perneger 2004]
- (학위논문·장문 한정) 서론 말미 로드맵 문장

## Methods / 연구 방법

8요소 [Perneger 2004 Table 1]: 맥락·세팅 / 연구 설계 / 대상 집단 / 표집 전략 /
개입(해당 시) / 주요 변수 / 자료수집 도구·절차 / 분석 방법

- **설계 명시로 시작하는가** — 관측/실험, 전향/후향, 무작위, 대조·눈가림 [Ecarnot 2015]
- 재현 가능한 수준으로 쪼개져 있는가 — "specific, concrete, technical, and
  fairly detailed" [Perneger 2004]
- **비통상적 방법 선택에 정당화 단락이 배정되어 있는가** — 관례를 벗어난
  설계·기법에 참고문헌·지침 또는 그 선택을 요구한 맥락이 붙는가 [Ecarnot 2015]
- **왜 그 방법이 그 답을 주는가**가 어딘가에 있는가 — 무엇을 했는지만 있고
  그 절차가 어떻게 답을 산출하는지 연결이 없는 배치 [Schulzrinne]
- 1차·2차 평가변수와 각각의 측정 방법이 구분되어 있는가 [Ecarnot 2015]
- **통계 서술 블록**이 마지막 단락으로 배정되어 있는가 [Ecarnot 2015] — 제시
  형식(평균±SD / 중앙값[IQR] / n(%)) · 변수별 검정 · 다변량 투입 변수 ·
  표본수 산정 근거 · 유의수준 · 다중비교 보정 · 소프트웨어와 버전
- 하위집단 분석이 **사전 명시**로 배치되어 있는가 ★ — 사후 분석을 사전 계획인
  것처럼 배치하지 않는다
- **윤리 진술 블록** — 윤리위 승인(또는 미해당 사유), 서면 동의, 임상시험
  등록번호 [Ecarnot 2015]. 승인번호는 사실 정보다. 없으면 결손으로 짚되
  지어내지 않는다.
- **Methods–Results 짝** ★ — Results에 올 모든 결과에 대응 방법이 있는가.
  전체 조망이면 `structural-integrity.md` 2번으로 표를 만들어 확인한다.

## Results / 연구 결과

`principles.md` 원칙 8(question–data–answer, C-C-C)이 1차 기준 — 중복하지 않는다.
설계 단계에서 더 볼 것:

- **본문 / 표 / 그림 배분** ★ — 1–2줄로 서술되는 결과는 본문, 둘 이상 집단의
  동일 변수 비교는 표, 복잡하거나 해석이 어려운 원자료·추세는 그림.
  표로 갈 것이 본문에 풀어 써져 있지 않은가 [Ecarnot 2015]
- 같은 결과가 표와 본문에 중복 배치되지 않았는가
- **불리하거나 유의하지 않은 결과가 빠지지 않았는가** ★ — 음성 결과도 유효한
  기여다 [Ecarnot 2015]
- 연구 질문과 무관한 표·결과가 들어 있지 않은가 — "resist the temptation"
- 해석·논평 단락이 Results에 섞여 있지 않은가 — Results는 사실 보고,
  선행연구 대조는 Discussion
- 백분율에 빈도, P값에 효과크기가 동반되도록 배치되어 있는가 [Perneger 2004]
- 그림·표 캡션이 본문 없이 홀로 이해되는가 [Schulzrinne]

## Discussion / 논의

5-move [Perneger 2004 Table 1]: 주요 발견 요약 → 선행연구 대비 해석 →
함의 → 강점·한계 → 향후 연구

- **첫 단락이 연구 질문에 대한 답으로 시작하는가** ★
- **Discussion이 Results 재나열로 채워지지 않았는가** ★ — 해석·기작 단락이
  실제로 배정되어 있는가
- **서론의 공백을 되짚는 단락이 있는가** — 이 연구가 그 공백을 메웠는지,
  무엇을 더하고 무엇을 반박하는지. 없으면 "또 한 편"으로 읽힌다 [Ecarnot 2015]
- 한계 절이 존재하고 방어적 최소화로 흐르지 않는가
- 범위 이동은 `structural-integrity.md` 6번에서 함께 본다
- 선행연구 비판은 타인 약점 지적("X et al. failed to…")이 아니라 자기 연구
  강점 진술로 전달되게 배치 [Ecarnot 2015]

## Conclusion / 결론

Discussion과 별개의 결론 절을 둔 원고에만 적용한다.

- **새 정보 도입 금지** ★ — 본문에 없던 데이터·결과·인용이 결론에서 처음
  등장하는 배치 [Ecarnot 2015]
- 결과의 재나열이 아니라 **종합**인가 — 개별 수치가 아니라 전체가 무엇을 뜻하는지
- 서론의 연구 질문에 대한 **답이 명시**되어 있는가
- 이론적·실용적 **기여 진술**이 있는가
- 인용 최소(0–2개, 맥락 설정 시에만)

## 학위논문 장 단위

5장 표준 [Hon (UF); Fisher et al.]: Introduction · Literature Review ·
Methodology · Results · Conclusion & Recommendations

- 장별 역할 침범 없음 — 방법 서술이 결과 장에 등장하는 식 [Perneger 2004
  Table 2 "chaotic structure"]
- 문헌고찰이 나열이 아니라 **공백 도출로 수렴하는가** ★ — "A는 X를 발견했다,
  B는 Y를 발견했다…" 나열형은 결격 [Pautasso 2013 Rule 6]
- 문헌고찰에 식별 가능한 조직 원리(연대순/주제별/방법론별)가 있는가 [Rule 7]
- (체계적 고찰·메타분석) 검색 전략 — DB, 검색어, 기간, 포함·배제 기준 —
  이 본문 항목으로 배정되어 있는가 [Koons et al. 2019]

## Research Proposal / 연구계획서

9구성요소 [IUFRO 핸드북 Ch.7]: Summary → Introduction → **Statement of
Problem/Need** → Project Description(목표·실험계획·결과확산·시설·인용문헌) →
Budget → Budget 정당화 → 특별 고려사항 → CV → 부록

- **Summary 6문장** — 신뢰성 · 문제/필요 · 연구목표 · 방법 · 자원 수요 ·
  기대 성과 각 1문장 이상, 1쪽(300–500단어) 이내
- **문제 진술 금지 문구** ★ — "little is known about…", "there is a general
  lack of information…", "no research has dealt with…" → 구체적 결과·통계로
  대체("1만 헥타르 낙엽 피해로 Y의 경제 손실")
- Objectives는 1–2문장, 측정·검증 가능한 성과로. 능동 동사(to increase/reduce)
  우선, to provide/establish 회피
- Objectives(무엇을·언제) ≠ Methods(어떻게) ≠ Goals(추상 지향) — 세 층위 혼동 금지
- 통계적 영가설을 목표로 진술하지 않는다

---

## 여기서 보지 않는 것

문장이 있어야 판단 가능하다. 초고가 있어도 이 단계에서 지적하지 않는다.

시제 · 태 · 명사화 · 헤징 강도 · 축약형·비격식어 · 만연체·문장 길이 변주 ·
클리셰 · 인용 형식과 그레이 문헌 · 용어 일관성(Banana Rule) · 수치 보고 완전성

단, **핵심 주장에 인용이 붙을 자리가 있는가**는 본다 — 근거 열이 비었는지의
문제이지 인용 형식의 문제가 아니기 때문이다 [Perneger 2004].

## 출처

Perneger & Hudelson (2004) *Int J Qual Health Care* 16(3):191-192 ·
Ecarnot et al. (2015) *Eur Geriatr Med* 6(6):573-579 ·
Tullu (2019) *Saudi J Anaesth* 13(S1):S12-S17 ·
Pautasso (2013) *PLoS Comput Biol* 9(7):e1003149 ·
Koons et al. (2019) *Ann Biomed Eng* 47(11):2334-2340 ·
Nature Summary Paragraph 공식 템플릿 · Hon (UF) Thesis Guidelines ·
Fisher et al. (Liebert) · Schulzrinne *Writing Technical Articles* (Columbia) ·
IUFRO *Handbook for Preparing and Writing Research Proposals* Ch.7

원문 PDF는 META_SCI KnowledgeDB에 보관. 문장 수준 규범과 AI 사용 규범을 포함한
전체 판본은 `meta-proofreading` 매뉴얼을 본다.

---

**Version**: 2.0.0 (설계 단계 발췌 — 1.1.0 교정용 전체본에서 파생)
