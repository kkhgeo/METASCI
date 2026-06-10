# Bullet Writing

Use this reference when drafting or rewriting slide body blocks. The goal is not to make a list shorter; the goal is to make each bullet explain one useful unit of reasoning.

## Principle

Write bullets as analytical blocks internally:

```text
Label: claim + evidence, mechanism, or implication
```

For final Korean slide text, normally hide the label and show only the complete analytical sentence. The label is a planning aid, not default visible copy.

Each bullet should answer one of these questions:

- What is the point?
- What supports it?
- Why does it matter for the audience?
- How does it connect to the slide lead statement?

## Korean Analytical Bullet Tone

For Korean research, policy, and institutional decks, write visible bullets in an objective, analytical, and descriptive tone:

- Use 3-6 bullets when compressing a report section or producing handout-style slide content.
- Use 2-4 bullets when the slide is visual, evidence-heavy, or intended for a short live talk.
- Make each bullet a complete explanation of 1-3 sentences.
- Prefer concise endings such as `-함`, `-됨`, `-나타남`, `-해석됨`, `-필요함`, `-어려움`, `-유용함`, and `-적절함`.
- Use `-고 있음` only when an ongoing process or current state must be emphasized; do not let multiple bullets end with `있음`.
- Prefer compressed forms such as `필요함`, `요구됨`, `검토해야 함`, and `해석해야 함` instead of longer forms such as `필요가 있음` or `해석할 필요가 있음`.
- Avoid keyword fragments, slogan-like phrasing, and exposed planning labels such as `배경:`, `근거:`, `함의:`.
- Preserve source fidelity; do not add unsupported implications or examples to make a bullet feel complete.

Preferred visible shape:

```text
주제: 질량수지 기반 자연저감 추정

• 질량수지는 유역으로 들어온 투입량과 하천을 통해 빠져나간 수출량의 차이를 보유량으로 해석하는 접근임.

• 보유 항에는 탈질, 침적, 식생 흡수 같은 자연저감 과정이 포함되지만, 레거시 축적과 인벤토리 오차도 함께 혼입됨.

• 따라서 질량수지 결과는 자연저감의 직접 관측값이 아니라, 여러 미계측 성분이 포함된 잔차 추정치로 해석해야 함.
```

## Preferred Body Block Shape

Use 2-4 blocks per slide:

```text
Body Blocks:
  - Label: 핵심 개념
    Content: [한 문장으로 개념을 정의하고, 이 슬라이드의 lead statement와 연결한다.]
  - Label: 근거
    Content: [자료, 수치, 문헌, 사례, 그림이 무엇을 보여주는지 설명한다.]
  - Label: 함의
    Content: [그래서 연구/정책/방법론상 무엇이 달라지는지 설명한다.]
```

Labels should be short nouns or noun phrases in the internal schema. Content should usually be one complete sentence, not a fragment. When writing final slide copy for the user, render the `Content` sentences as bullets and omit the `Label` field unless labels are intentionally part of a comparison table or framework diagram.

## Common Patterns

### Claim -> Evidence -> Implication

Use for evidence slides, results, and research findings.

```text
Keyword Title: 영양염류 부하 추정
Lead Statement: 유역 단위 총량 추정은 정책 질문에 답하지만, 공간적 관리 우선순위는 별도 해석이 필요하다.
Body Blocks:
  - Claim: 총량 추정은 유역의 오염 기여도를 비교하는 데 적합하다.
  - Evidence: 시나리오별 배출원 기여율과 하천 구간별 농도 변화가 함께 제시된다.
  - Implication: 관리 지점 선정에는 총량 결과를 hotspot 지도나 하위유역 정보로 다시 해석해야 한다.
```

### Problem -> Cause -> Need

Use for background, necessity, and motivation slides.

```text
Keyword Title: 환경정보 분절
Lead Statement: 환경정책 정보는 축적되어 있지만, 의미 단위의 연결이 약해 정책 질의에 바로 답하기 어렵다.
Body Blocks:
  - Problem: 법령, 계획, 통계, 뉴스, 측정망 자료가 서로 다른 형식과 기관 체계로 관리된다.
  - Cause: 같은 대상도 문서마다 명칭, 공간 단위, 시간 단위, 분류 기준이 다르게 기록된다.
  - Need: 정책 의사결정에는 자료를 모으는 것보다 개념과 관계를 명시적으로 연결하는 구조가 필요하다.
```

### Definition -> Role -> Boundary

Use when introducing technical terms.

```text
Keyword Title: 지식그래프
Lead Statement: 지식그래프는 개념과 관계를 노드와 엣지로 연결해 질의 가능한 지식 구조를 만든다.
Body Blocks:
  - Definition: 지식그래프는 개체, 속성, 관계를 구조화해 사람이 읽는 문서를 기계가 탐색할 수 있는 형태로 바꾼다.
  - Role: 정책 문서에서는 법령, 계획, 사업, 지표, 기관 사이의 관계를 추적하는 기반이 된다.
  - Boundary: 그래프 자체가 답을 보장하는 것은 아니며, 신뢰 가능한 추출과 검증 절차가 함께 필요하다.
```

### Input -> Process -> Output

Use for methods and workflows.

```text
Keyword Title: 정책문서 코퍼스
Lead Statement: 코퍼스 구축은 문서 수집이 아니라, 이후 질의와 추론이 가능한 단위로 정책 문서를 재구성하는 과정이다.
Body Blocks:
  - Input: 법령, 기본계획, 지침, 보도자료처럼 정책 근거가 되는 문서를 수집한다.
  - Process: 문서를 조항, 문단, 표, 메타데이터 단위로 분리하고 출처와 시점을 유지한다.
  - Output: 검색, 지식그래프 구축, GraphRAG 질의응답에 사용할 수 있는 구조화된 텍스트 기반을 만든다.
```

### Compare -> Difference -> Meaning

Use for comparing methods, cases, or alternatives.

```text
Keyword Title: Mass-balance와 모델링
Lead Statement: 두 접근은 모두 총량을 추정하지만, 설명하는 질문과 정책 활용 방식이 다르다.
Body Blocks:
  - Compare: Mass-balance는 관측값 기반의 수지 계산으로 현재 부하량을 직접 비교한다.
  - Difference: 모델링은 강우, 토지이용, 배출원 시나리오를 반영해 조건 변화에 따른 결과를 추정한다.
  - Meaning: 현황 진단에는 mass-balance가, 대안 평가에는 모델 기반 시나리오가 더 적합하다.
```

## Bad -> Better

Avoid keyword-only bullets:

```text
Bad:
- 데이터 부족
- 기관별 관리
- 통합 필요
```

Rewrite as analytical blocks:

```text
Better:
• 측정망과 행정자료는 축적되어 있지만, 정책 질문에 필요한 공간·시간 단위가 항상 일치하지 않음.
• 기관별 관리 체계는 자료의 책임성을 높이지만, 교차 분야 분석에서는 의미 연결 비용을 만듦.
• 통합의 핵심은 자료를 한곳에 모으는 것이 아니라 개념, 지표, 지역, 시점을 연결하는 것으로 해석됨.
```

Avoid unsupported conclusion bullets:

```text
Bad:
- AI를 활용하면 정책 지원이 고도화됨
```

Rewrite with mechanism and condition:

```text
Better:
• 문서, 지표, 공간자료의 관계가 명시될 때 AI는 단순 검색을 넘어 근거 추적형 정책 질의 지원이 가능함.
```

## Checklist

- Does each bullet support the slide lead statement?
- Does each bullet contain a claim, not just a topic label?
- Is evidence, mechanism, or implication visible?
- Are there 2-4 body blocks for live slides, or 3-6 bullets for section-derived analytical slides?
- For Korean decks, do visible bullets use complete objective analytical sentences rather than exposed planning labels?
- Does the slide avoid repetitive `있음` endings and compressed forms such as `필요함` instead of `필요가 있음`?
- Are unsupported implications marked as open questions?
- Can the bullets be read in order as a small argument?
