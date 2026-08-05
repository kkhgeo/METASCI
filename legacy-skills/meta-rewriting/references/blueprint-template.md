# Blueprint Template & Extraction Guide

PHASE 2에서 사용한다. 6개 차원별 추출 항목과 Blueprint 카드 출력 형식을 정의한다.

---

## Blueprint Card Format

```
================================================================
  STYLE BLUEPRINT
  Source: [paper title / journal / author]
  Input volume: [word count / sections] | Confidence: [High / Medium / Low]
================================================================

1. TONE & STANCE
2. SENTENCE ARCHITECTURE
3. LOGICAL FLOW
4. TRANSITION EXPRESSIONS
5. VOCABULARY & TERMINOLOGY
6. CITATION & EVIDENCE STYLE
```

---

## Dimension 1: Tone & Stance

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

## Dimension 2: Sentence Architecture

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

## Dimension 3: Logical Flow

**What to extract:**
- Macro argument structure of the paper (e.g., Problem -> Gap -> Approach -> Contribution)
- Paragraph-level structure (e.g., Claim -> Evidence -> Interpretation)
- How sections are bridged (closing sentence foreshadows next / opening sentence links back)
- How counter-arguments or limitations are handled

**Output format:**
```
3. LOGICAL FLOW
   Macro structure: [e.g., Problem -> Gap -> Approach -> Contribution]
   Paragraph structure: [e.g., Claim -> Evidence -> Interpretation]
   Section transitions: [closing foreshadow / opening recap]
   Counter-argument style: [acknowledge then rebut / state limitation upfront]
   Source transition example:
     - "[actual transition sentence]"
   Reusable templates:
     - "While X has been established, ___ remains poorly understood."
     - "Building on these findings, we propose that ___"
     - "Taken together, these results suggest ___"
```

---

## Dimension 4: Transition Expressions

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
```

---

## Dimension 5: Vocabulary & Terminology

**What to extract:**
- Top domain-specific noun phrases (up to 15)
- Preferred academic verbs — and verbs the author notably avoids
- Nominalization tendency: does the author prefer "the increase in X" or "X increased"?
- Numerical conventions: decimal places, units, significant figures

**Output format:**
```
5. VOCABULARY & TERMINOLOGY
   Domain terms: [list up to 15]
   Preferred verbs: [demonstrate, reveal, indicate, suggest, exhibit ...]
   Avoid:          [prove, very, really -> suggest academic alternatives]
   Nominalization: [High / Medium / Low]
   Numerical style: [e.g., 3 decimal places, SI units, +/-1sigma uncertainty]
```

---

## Dimension 6: Citation & Evidence Style

**What to extract:**
- How citations are integrated: narrative ("Smith et al. showed...") vs. parenthetical ("(Smith et al., 2020)")
- How numerical data is reported: format, precision, statistical notation
- Figure and table reference conventions

**Output format:**
```
6. CITATION & EVIDENCE STYLE
   Citation style: [narrative / parenthetical / mixed]
     e.g., "As demonstrated by Smith et al. (2020)..." vs "(Smith et al., 2020)"
   Data format: [value +/- SD (n=N, p<0.05)]
   Figure/table refs: [(Fig. 1) / (Table 2)]
```

---

## Confidence Levels

| Level | Condition |
|-------|-----------|
| **High** | 500+ words across multiple sections analyzed |
| **Medium** | Abstract + introduction only (~200-500 words) |
| **Low** | Inferred from journal name or title only (no direct text) |

Low/Medium confidence시 사용자에게 실제 논문 텍스트 제공을 권장한다.

---

## Style Databank Mapping

기존 `meta-styling Mode A` 데이터뱅크(`Style_{topic}/`)를 Blueprint으로 변환할 때:

| Style Databank Category | Blueprint Dimension |
|-------------------------|---------------------|
| Sentence Patterns | Dim 2: Sentence Architecture |
| Vocabulary | Dim 5: Vocabulary & Terminology |
| Transitions & Connectors | Dim 4: Transition Expressions |
| Hedging & Stance Markers | Dim 1: Tone & Stance |
| Quantitative Expressions | Dim 6: Citation & Evidence Style |
| Citation Integration Patterns | Dim 6: Citation & Evidence Style |
| Section Overview (tense/voice) | Dim 1: Tone & Stance |
| Style Rules (Do/Don't) | Dim 3: Logical Flow + overall |

데이터뱅크에서 각 카테고리의 예시 문장과 패턴을 Blueprint 형식으로 재구성한다.
