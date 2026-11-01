# Blueprint Template & Extraction Guide

PHASE 0에서 사용한다. 6개 차원별 추출 항목과 Blueprint 카드 출력 형식을 정의한다.
추출된 차원은 Stage별로 분배된다:
- **Dim 3 (Logical Flow)** → Stage 1-B (논증 구조 Monte Carlo)
- **Dim 1, 2, 4, 5, 6** → Stage 2 (스타일 Monte Carlo)

---

## Blueprint Card Format

```
================================================================
  STYLE BLUEPRINT [A / B / C / ...]
  Source: [paper title / journal / author]
  Input volume: [word count / sections] | Confidence: [High / Medium / Low]
================================================================

1. TONE & STANCE           ──→ Stage 2
2. SENTENCE ARCHITECTURE   ──→ Stage 2
3. LOGICAL FLOW            ──→ Stage 1-B
4. TRANSITION EXPRESSIONS  ──→ Stage 2
5. VOCABULARY & TERMINOLOGY ──→ Stage 2
6. CITATION & EVIDENCE STYLE ──→ Stage 2
================================================================
```

---

## Dimension 1: Tone & Stance → Stage 2

**What to extract:**
- Overall register: objective-analytical / argumentative / exploratory
- Subject preference: first-person "We" (active) vs. passive voice — estimate ratio
- Hedging frequency: High / Medium / Low; list the actual hedging phrases used
- Degree of certainty: does the author claim firmly or qualify constantly?

**Output format:**
```
1. TONE & STANCE
   Register: [objective-analytical / argumentative / exploratory]
   Voice: [We (active) ~N% / passive ~N%]
   Hedging: [High / Medium / Low] — [list phrases: may, suggests, appears to ...]
   Source examples:
     - "[sentence 1]"
     - "[sentence 2]"
   Reusable templates:
     - "These findings suggest that ___"
     - "Our results indicate that ___"
     - "This is consistent with the hypothesis that ___"
```

---

## Dimension 2: Sentence Architecture → Stage 2

**What to extract:**
- Average sentence length in words (count a sample of ~20 sentences)
- Ratio of complex/compound sentences vs. simple sentences
- Recurring syntactic patterns (e.g., "Although X, Y", "X, which suggests Y")
- Average paragraph length in sentences and words

**Output format:**
```
2. SENTENCE ARCHITECTURE
   Avg sentence length: ~N words (range: min-max)
   Complex sentence ratio: ~N%
   Preferred constructions: [list patterns]
   Paragraph size: avg N sentences, N-N words
   Source example:
     - "[sentence showing preferred structure]"
   Reusable templates:
     - "Although ___, ___ demonstrates that ___"
     - "Given that ___, we investigated ___"
     - "___, which is consistent with ___"
```

---

## Dimension 3: Logical Flow → Stage 1-B

**이 차원은 Stage 1-B (논증 구조 Monte Carlo)에서 사용된다.**
스타일 전이가 아닌 **논증 구조 교정**의 기준으로 활용된다.

**What to extract:**
- Macro argument structure (e.g., Problem → Gap → Approach → Contribution)
- Paragraph-level structure (e.g., Claim → Evidence → Interpretation)
- How sections are bridged (closing foreshadows next / opening links back)
- How counter-arguments or limitations are handled
- Evidence placement pattern (data before claim / claim before data)

**Output format:**
```
3. LOGICAL FLOW
   Macro structure: [e.g., Problem → Gap → Approach → Contribution]
   Paragraph structure: [e.g., Claim → Evidence → Interpretation]
   Section transitions: [closing foreshadow / opening recap / bridging sentence]
   Counter-argument style: [acknowledge then rebut / state limitation upfront / absent]
   Evidence placement: [data-first / claim-first]
   Source transition example:
     - "[actual transition sentence between sections]"
     - "[actual counter-argument sentence]"
   Reusable templates:
     - "While X has been established, ___ remains poorly understood."
     - "Building on these findings, we propose that ___"
     - "Taken together, these results suggest ___"
     - "An alternative explanation is that ___, however ___"
```

**Stage 1-B에서의 사용:**
- 각 레퍼런스의 Dim 3 패턴을 독립적으로 초고에 적용
- 후보별로 5개 논증 하위 차원(Argument Sequence, Counter-argument, Section Transition, Paragraph Organization, Evidence Density)으로 교차 평가
- 차원별 챔피언을 선발하여 Fusion

---

## Dimension 4: Transition Expressions → Stage 2

**What to extract:**
- Collect all connective adverbs and phrases used, grouped by function

**Output format:**
```
4. TRANSITION EXPRESSIONS
   Addition:  [Furthermore, Moreover, In addition ...]
   Contrast:  [However, In contrast, Nevertheless ...]
   Causality: [Therefore, As a result, Consequently ...]
   Emphasis:  [Notably, Importantly, Remarkably ...]
   Summary:   [In summary, Taken together, Overall ...]
   Temporal:  [Subsequently, Following this, Prior to ...]
```

---

## Dimension 5: Vocabulary & Terminology → Stage 2

**What to extract:**
- Top domain-specific noun phrases (up to 15)
- Preferred academic verbs — and verbs the author notably avoids
- Nominalization tendency: "the increase in X" vs "X increased"
- Numerical conventions: decimal places, units, significant figures

**Output format:**
```
5. VOCABULARY & TERMINOLOGY
   Domain terms: [list up to 15]
   Preferred verbs: [demonstrate, reveal, indicate, suggest, exhibit ...]
   Avoid:          [prove, very, really → suggest academic alternatives]
   Nominalization: [High / Medium / Low]
   Numerical style: [e.g., 3 decimal places, SI units, ±1σ uncertainty]
```

---

## Dimension 6: Citation & Evidence Style → Stage 2

**What to extract:**
- How citations are integrated: narrative vs. parenthetical
- How numerical data is reported: format, precision, statistical notation
- Figure and table reference conventions

**Output format:**
```
6. CITATION & EVIDENCE STYLE
   Citation style: [narrative / parenthetical / mixed]
     e.g., "As demonstrated by Smith et al. (2020)..." vs "(Smith et al., 2020)"
   Data format: [value ± SD (n=N, p<0.05)]
   Figure/table refs: [(Fig. 1) / (Table 2) / Figure 1]
```

---

## Extraction Rules

모든 차원 공통:

1. 각 차원에서 **2-3개 실제 문장을 인용** (추상적 설명 금지)
2. 가능한 **수치화**: 평균 문장 길이, passive voice 비율, hedging 빈도
3. **3-5개 재사용 가능한 fill-in-the-blank 템플릿** 생성
4. 레퍼런스 텍스트가 짧으면 (<200w) 추출 가능한 만큼만, 부족한 차원은 "데이터 부족" 표시

---

## Confidence Levels

| Level | Condition |
|-------|-----------|
| **High** | 500+ words, 다중 섹션 분석 가능 |
| **Medium** | Abstract + Introduction only (~200-500w) |
| **Low** | 저널명만 또는 <200w |

Low/Medium confidence시 사용자에게 실제 논문 텍스트 제공을 권장.

---

## Style Databank Mapping

기존 `meta-styling Mode A` 데이터뱅크(`Style_{topic}/`)를 Blueprint으로 변환할 때:

| Style Databank Category | Blueprint Dimension | Stage |
|-------------------------|---------------------|-------|
| Sentence Patterns | Dim 2: Sentence Architecture | Stage 2 |
| Vocabulary | Dim 5: Vocabulary & Terminology | Stage 2 |
| Transitions & Connectors | Dim 4: Transition Expressions | Stage 2 |
| Hedging & Stance Markers | Dim 1: Tone & Stance | Stage 2 |
| Quantitative Expressions | Dim 6: Citation & Evidence Style | Stage 2 |
| Citation Integration Patterns | Dim 6: Citation & Evidence Style | Stage 2 |
| Section Overview (tense/voice) | Dim 1: Tone & Stance | Stage 2 |
| Style Rules (Do/Don't) | Dim 3: Logical Flow | Stage 1-B |
