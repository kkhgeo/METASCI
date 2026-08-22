# Outline — 계층형 mapping 예시

- Core message: 국가 배경농도와 유역 차이를 함께 보아야 질산염의 공간적 이질성을 설명할 수 있다.
- 원고 언어: 한국어
- 포맷 버전: 1.1
- 지도 상태: integrated
- 기본 범위: manuscript
- 최종 갱신: 2026-08-22

## 구성

### Results 3.3

#### RESULTS.3.3.P3
- 상태: resolved
- 기능: Summary
- 한 줄 논지: 전국 단일 기준만으로는 유역별 차이를 충분히 표현하기 어렵다.
- 앞 단락:
  - —
- 근거:
  - Table-2 | primary
- Ledger:
  - L01 | first-report
- 축:
  - epistemic-layer = observation
- Core message 기여: 유역 단위 분석이 필요한 이유를 제시
- 결정: D-001
- 메모:
  - 다음 소절의 질문을 형성한다.

### Results 3.4

#### RESULTS.3.4.P1
- 상태: decided
- 기능: Comparison
- 한 줄 논지: 유역별 ABL은 전국 단일값보다 큰 공간적 차이를 보였다.
- 앞 단락:
  - RESULTS.3.3.P3 | Question-Answer
- 근거:
  - Table-S2 | first-report
  - Fig-4 | primary
- Ledger:
  - L07 | first-report
- 축:
  - epistemic-layer = observation
- Core message 기여: 국가값이 가리는 유역 차이를 제시
- 결정: D-021
- 메모:
  - Table-S2의 최초 보고 위치를 잠가야 한다.

#### RESULTS.3.4.P2
- 상태: proposed
- 기능: Pattern
- 한 줄 논지: 유역 간 ABL 변동은 특정 공간 집단에 집중되었다.
- 앞 단락:
  - RESULTS.3.4.P1 | Specification
- 근거:
  - Table-S2 | reference
  - Fig-4 | supporting
- Ledger:
  - L08 | supporting
- 축:
  - epistemic-layer = observation
- Core message 기여: 전체 변동을 공간적 패턴으로 구체화
- 결정: D-022
- 메모:
  - Fig-4가 두 화제를 함께 담는다.

### Discussion 4.2

#### DISCUSSION.4.2.P1
- 상태: proposed
- 기능: Interpretation
- 한 줄 논지: 유역별 차이는 토지이용과 축산활동으로 부분적으로 설명된다.
- 앞 단락:
  - RESULTS.3.4.P2 | Observation-Interpretation
- 근거:
  - Fig-4 | interpretation
  - Chen2024 | comparison
- Ledger:
  - L09 | first-report
- 축:
  - epistemic-layer = interpretation
- Core message 기여: 관찰된 공간 차이의 환경적 의미를 해석
- 결정: D-028
- 메모:
  - Results 순서가 바뀌면 이 단락도 재검토한다.

## 근거 인벤토리

- Table-2 | table | available | RESULTS.3.3
- Table-S2 | table | available | RESULTS.3.4
- Fig-4 | figure | available | RESULTS.3.4
- Chen2024 | literature | available | DISCUSSION.4.2
- Fig-9 | figure | available | INTRO

## Ledger 인벤토리

- L01 | core-claim | first-report-required | manuscript
- L07 | quantitative-result | first-report-required | RESULTS.3.4
- L08 | spatial-pattern | required | RESULTS.3.4
- L09 | interpretation | required | DISCUSSION.4.2
- L10 | limitation | required | DISCUSSION.4.2

## 결정 대장

#### D-001
- 상태: resolved
- 우선순위: blocker
- 범위: manuscript
- 제목: Core message 확정
- 추천: 국가 배경농도와 유역 차이를 함께 보는 구조를 채택한다.
- 근거: Table-2, Table-S2, Fig-4가 이 축으로 결속된다.
- 대안:
  - 국가 단일 기준만 전면에 두면 유역 분석의 필요성이 약해진다.
- 영향:
  - INTRO
  - RESULTS.3.3
  - RESULTS.3.4
  - DISCUSSION.4.2
- 의존:
  - —
- 해소 기준: Core message와 관련 단락 논지가 일치한다.
- 이력:
  - 2026-08-20 | surfaced | 사용자에게 추천 제시
  - 2026-08-21 | resolved | outline 반영과 간선 검증 완료

#### D-021
- 상태: surfaced
- 우선순위: high
- 범위: RESULTS.3.4
- 제목: Table-S2의 최초 보고 위치
- 추천: P1에서 처음 보고하고 P2에서는 참조만 한다.
- 근거: P1이 소절의 진입점이고 P2는 패턴을 확대한다.
- 대안:
  - P2에서 처음 보고하면 P1이 직접 근거 없이 시작한다.
- 영향:
  - RESULTS.3.4.P1
  - RESULTS.3.4.P2
  - DISCUSSION.4.2.P1
- 의존:
  - D-001
- 해소 기준: first-report가 한 단락에만 남고 P1 논지가 근거와 결속된다.
- 이력:
  - 2026-08-22 | surfaced | 부분 mapping에서 제시

#### D-022
- 상태: detected
- 우선순위: medium
- 범위: RESULTS.3.4
- 제목: Fig-4의 두 화제 분리
- 추천: P1은 전체 차이, P2는 공간 패턴을 맡긴다.
- 근거: 한 도판이 두 화제를 담지만 단락 기능은 분리할 수 있다.
- 대안:
  - 한 단락에 합치면 논지와 해석 경계가 흐려진다.
- 영향:
  - RESULTS.3.4.P1
  - RESULTS.3.4.P2
- 의존:
  - D-021
- 해소 기준: 두 단락의 논지와 근거 역할이 중복되지 않는다.
- 이력:
  - 2026-08-22 | detected | 그래프 검토에서 발견

#### D-028
- 상태: reopened
- 우선순위: high
- 범위: DISCUSSION.4.2
- 제목: Results 순서 변경에 따른 해석 순서 재검토
- 추천: Results 3.4의 확정 순서를 따라 Discussion을 정렬한다.
- 근거: 결과와 해석의 평행성이 깨지면 대응 관계를 잡기 어렵다.
- 대안:
  - 해석 중요도 순으로 둘 수 있으나 Results와의 대응표지가 필요하다.
- 영향:
  - DISCUSSION.4.2.P1
- 의존:
  - D-022
- 해소 기준: Results와 Discussion의 단락 순서 또는 명시적 대응표지가 확정된다.
- 이력:
  - 2026-08-22 | reopened | Results 3.4 부분 변경 영향

## 근거 노트

### Fig-4 — 유역별 공간 분포
전체 변동과 예외 유역을 동시에 보여준다.
→ 배정: Results 3.4 P1(전체 차이), P2(공간 패턴), Discussion 4.2 P1(해석)
→ 표현 강도: 원인을 단정하지 않고 부분적 설명으로 제한
