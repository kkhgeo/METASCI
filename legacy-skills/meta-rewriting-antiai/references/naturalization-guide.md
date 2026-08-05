# Naturalization Guide — 4계층 자연화 규칙 및 체크리스트

> PHASE 2 (4-Layer Naturalization) 시작 전 반드시 읽는다.

---

## Execution Principle

**Layer 1 → 2 → 3 → 4 순서는 절대 변경하지 않는다.**

각 Layer의 교정이 다음 Layer에 영향을 주기 때문이다:
- Layer 1 어휘 교체 → Layer 2 문장 구조에 영향
- Layer 2 구문 재구성 → Layer 3 담화 표현 삽입 위치에 영향
- Layer 3 담화 교정 → Layer 4 서식 최종 정리 가능

**각 Layer 교정 후 변경 사항을 Change Log에 기록한다.**

---

## Layer 1: Lexical Naturalization (어휘 자연화)

### 1.1 AI Excess Word 교체 규칙

교체 시 반드시 지켜야 할 원칙:

1. **문맥 적합성 우선**: 대체어는 원래 문맥에서 자연스러워야 한다
2. **기계적 1:1 치환 금지**: "delve → examine" 같은 일률적 치환이 아니라 문맥에 맞는 선택
3. **전문 용어 보존**: AI 과잉 단어와 해당 분야 전문 용어가 겹치면 보존 (예: "intricate" 가 결정 구조 서술에서 정확한 용어인 경우)
4. **빈도 분산**: 같은 대체어를 반복 사용하지 않는다

### 1.2 교체 전략

```
판단 순서:
1. 해당 단어가 분야 전문 용어인가? → Yes → 보존 (기록)
2. 같은 단락에 다른 AI 과잉 단어가 있는가? → Yes → 공기 패턴 우선 분산
3. 단어 삭제만으로 문장이 성립하는가? → Yes → 삭제 우선 (과잉 수사 제거)
4. 대체어로 바꿔야 하는가? → 문맥에 가장 자연스러운 대체어 선택
```

### 1.3 Co-occurrence 분산 전략

**핵심: 개별 단어 교체보다 공기 패턴 해소가 우선이다.**

```
같은 단락에서 AI Tier 1 단어 2개 발견 시:
  Option A: 둘 중 1개만 교체 (덜 자연스러운 쪽)
  Option B: 둘 다 교체 (공기 패턴이 Critical인 경우)
  Option C: 1개를 다른 단락으로 이동 (문장 재배치가 자연스러운 경우)

같은 문장에서 AI Tier 1-2 단어 2개 발견 시:
  → 반드시 최소 1개 교체
  → 가급적 문장 재구성으로 자연스럽게 해소
```

### 1.4 Copula 복원 전략

```
"serves as a [noun]" → "is a [noun]"
  단, 수사적 강조가 의도된 경우 1회 유지 가능

"stands as" → "is" 또는 "remains"
"marks the" → "is" 또는 문맥에 맞는 동사
"features" → "has" 또는 "includes"
"offers" → "has", "provides", "gives"
"boasts" → "has" (홍보 톤 반드시 제거)

규칙: 같은 단락에서 copula 회피 패턴 2회 이상 → 최소 1개 복원
```

### 1.5 Elegant Variation 정리

```
동일 대상을 가리키는 표현이 3종 이상 사용된 경우:
  → 1-2개 용어로 통일
  → 첫 등장 시 정식 명칭 사용
  → 이후 1개 약칭 또는 대명사 사용

예:
  Before: "the catalyst" → "the photocatalytic agent" → "the material" → "the specimen"
  After: "the TiO₂ catalyst" (첫 등장) → "the catalyst" (이후) → "it" (대명사)
```

---

## Layer 2: Syntactic Naturalization (구문 자연화)

### 2.1 Burstiness 주입

**목표: 문장 길이 표준편차 ≥ 8 words**

인간 글쓰기는 짧은 문장과 긴 문장이 자연스럽게 교차한다.
AI는 비슷한 길이의 문장을 연속 생산한다.

```
측정 방법:
  1. 각 문장의 단어 수 산출
  2. 표준편차 계산
  3. SD < 5 → Major (강한 균일성)
  4. SD 5-8 → Minor (약한 균일성)
  5. SD ≥ 8 → OK (자연스러운 변동)

교정 방법:
  A. 긴 복문 1개를 짧은 문장 2개로 분리
  B. 짧은 문장 2개를 1개 복문으로 결합
  C. 핵심 발견/주장에 짧고 강한 문장 배치 (This is significant.)
  D. 설명/맥락에 긴 복문 배치

패턴 예시:
  Before: [22w] [19w] [21w] [20w] [23w]  (SD ≈ 1.6)
  After:  [8w] [28w] [12w] [25w] [7w] [22w]  (SD ≈ 9.1)
```

### 2.2 -ing Tail Pattern 제거

AI가 문장 끝에 "-ing" 분사구를 붙이는 패턴.

```
Before: "The temperature increased to 450°C, indicating a phase transition."
After:  "The temperature increased to 450°C. This increase indicates a phase transition."
또는:   "The temperature increased to 450°C, which indicates a phase transition."

Before: "The samples were analyzed using XRD, revealing a crystalline structure."
After:  "XRD analysis of the samples revealed a crystalline structure."

교정 옵션:
  A. 독립 문장으로 분리 ("~. This indicates/reveals/suggests...")
  B. 관계절로 변환 ("~, which indicates...")
  C. 문장 구조 재편 (주어 교체로 자연스러운 연결)

제한: 단락당 -ing tail 1회까지 허용 (자연스러운 사용도 존재)
```

### 2.3 Rule of Three 해소

```
Before: "The method is simple, efficient, and reproducible."
After:  "The method is efficient and reproducible." (불필요한 항목 삭제)
또는:   "The method is simple. It also proved efficient and reproducible." (분리)

Before: "These results highlight the complexity, diversity, and significance of..."
After:  "These results highlight the diversity of..." (핵심만 유지)

규칙:
  - 같은 단락에서 3항목 나열이 2회 이상 → 최소 1개 해소
  - 3항목 모두 의미 있으면 유지 가능 (기록)
  - 3항목 중 1개가 다른 2개에 포함되면 삭제
```

### 2.4 구문 다양화 전략

```
같은 구문 패턴이 3회 이상 연속되면 교정:

Pattern 1: Subject + Verb + Object 반복
  → 도치문, 부사구 선행, 수동태 교차 삽입

Pattern 2: "The [noun] [verb]..." 반복
  → 주어 변경, 대명사 사용, "It was found that..." 변형

Pattern 3: "This/These [noun] [verb]..." 반복
  → 구체적 명사로 교체, 접속사 활용

도치문 예시:
  Before: "The concentration increased. The temperature rose."
  After:  "The concentration increased. With it rose the temperature."
  또는:   "The concentration increased, accompanied by a rise in temperature."
```

### 2.5 부정 병렬 재구성

```
Before: "Not just the temperature, but also the pressure affected the outcome."
After:  "The temperature affected the outcome. The pressure played an equally important role."
또는:   "Both temperature and pressure affected the outcome."

Before: "This is not merely a theoretical concern, but a practical one."
After:  "This concern extends beyond theory into practice."

규칙: 단락당 "not just/merely X, but (also) Y" 1회 초과 → 반드시 교정
```

---

## Layer 3: Discourse Naturalization (담화 자연화)

### 3.1 Metadiscourse Marker 균형

학술 글에서 필요한 metadiscourse 유형과 AI의 전형적 결핍:

| Type | AI Tendency | Target |
|------|-------------|--------|
| Hedges | "may" 과다, 다양성 부족 | may, might, could, appear to, suggest, seem, likely, possible |
| Boosters | 거의 부재 | clearly, certainly, demonstrate, establish, confirm, undoubtedly |
| Self-mentions | 거의 부재 | we, our, this study, the present work, the authors |
| Attitude markers | 거의 부재 | importantly, surprisingly, interestingly, notably, remarkably |
| Engagement markers | 거의 부재 | consider, note that, as shown in, see Figure X |

### 3.2 Hedging 보강

```
주장 강도에 따른 hedging 삽입:

강한 주장 (데이터가 명확히 뒷받침):
  → Hedge 없이 booster 사용
  "Our results clearly demonstrate that..."

중간 주장 (데이터가 시사하지만 확정 아님):
  → 적절한 hedge 삽입
  "These findings suggest that..." / "The data appear to indicate..."

약한 주장 (추론/해석):
  → 강한 hedge 삽입
  "It is possible that..." / "One might speculate that..."

규칙:
  - Hedge만 있고 booster가 없으면 → booster 최소 2-3개 삽입
  - "may"만 반복 사용하면 → suggest, appear to, seem 등으로 다양화
  - 모든 주장에 hedge 붙이면 → 핵심 발견에서 hedge 제거, booster로 교체
```

### 3.3 Self-mention 회복

```
학술 논문에서 저자 존재 표현은 필수적이다.
AI는 이를 회피하고 비인격적 수동태를 남용한다.

Before: "It was found that the concentration exceeded the threshold."
After:  "We found that the concentration exceeded the threshold."

Before: "The results can be interpreted as evidence of..."
After:  "We interpret these results as evidence of..."

Before: "An analysis was conducted to determine..."
After:  "We conducted an analysis to determine..."

삽입 위치 가이드:
  - Introduction 끝: "In this study, we examine/investigate/present..."
  - Methods: "We collected/analyzed/measured..." (능동태)
  - Results: "We found/observed/identified..."
  - Discussion: "We argue/suggest/propose that..."
  - Conclusion: "Our findings demonstrate/suggest..."

규칙:
  - 전체 텍스트에서 we/our/this study 0회 → Critical
  - 섹션당 최소 1-2회 self-mention 필요
  - 과다 사용도 피한다 (문장마다 "We"로 시작하지 않기)
```

### 3.4 Attitude Marker 추가

```
핵심 발견이나 중요한 전환점에 attitude marker를 삽입한다:

Before: "The concentration was 10 times higher than expected."
After:  "Surprisingly, the concentration was 10 times higher than expected."

Before: "This finding has implications for..."
After:  "Importantly, this finding has implications for..."

사용 가능한 markers:
  - Importantly, (핵심 포인트)
  - Surprisingly, / Unexpectedly, (예상 밖 결과)
  - Interestingly, (주목할 패턴)
  - Critically, (핵심 제한/조건)
  - Remarkably, (두드러진 결과)

규칙:
  - 전체 텍스트에서 attitude marker 0개 → Major
  - 단락당 1개 이하 (과다 방지)
  - Results/Discussion에 집중 삽입
```

### 3.5 Transition 다양화

```
AI 전형적 전환어와 자연스러운 대안:

| AI Pattern | Natural Alternatives |
|------------|---------------------|
| Furthermore, | In this context, / Building on this, / Along similar lines, |
| Moreover, | Equally important, / A related finding is / Beyond this, |
| Additionally, | [삭제하고 문장 직접 연결] / Also noteworthy is / Another aspect is |
| In addition, | [삭제] / A further consideration is |
| However, | Yet, / Still, / That said, / On the other hand, / Conversely, |
| Therefore, | Thus, / Accordingly, / As a result, / Consequently, / It follows that |
| In conclusion, | To summarize, / Taken together, / In sum, / Overall, |

규칙:
  - 같은 전환어가 2회 이상 → 대안으로 교체
  - 문장 시작 "Additionally," / "Furthermore," → 삭제 가능 (대부분 불필요)
  - 논리 관계가 명확하면 전환어 자체 삭제 (문맥으로 충분)
```

---

## Layer 4: Formatting Naturalization (서식 자연화)

### 4.1 Em Dash 감축

```
규칙: 단락당 em dash (—) 1회 이하

교정 방법:
  A. 괄호로 대체: "the sample — a TiO₂ nanoparticle — was" → "the sample (a TiO₂ nanoparticle) was"
  B. 콤마로 대체: "the result — 95% removal — exceeded" → "the result, 95% removal, exceeded"
  C. 문장 분리: "X — which means Y" → "X. This means Y."
  D. 삭제 (불필요한 삽입구): "the method — as described above — involves" → "the method involves"

우선순위: D (삭제) > C (분리) > B (콤마) > A (괄호)
```

### 4.2 List → Prose 변환

```
학술 논문에서 bullet/numbered list는 Methods의 절차 설명 등 제한된 경우에만 허용.
나머지는 모두 산문으로 변환한다.

Before:
  The advantages include:
  - Higher efficiency
  - Lower cost
  - Better reproducibility

After:
  "The method offers higher efficiency at lower cost, with improved reproducibility."
  또는:
  "This approach improves efficiency while reducing cost. It also enhances reproducibility."

변환 전략:
  1. 3항목 이하: 한 문장으로 통합
  2. 4-5항목: 2-3문장으로 나누어 서술
  3. 6항목 이상: 카테고리로 묶어 2-3문장 + 필요 시 Table 고려
```

### 4.3 Inline-Header 제거

```
Before:
  **Temperature**: The reaction was conducted at 450°C.
  **Pressure**: The system was maintained at 1 atm.
  **Duration**: The process lasted 2 hours.

After:
  "The reaction was conducted at 450°C under 1 atm for 2 hours."
  또는 (상세 서술이 필요한 경우):
  "The reaction temperature was set to 450°C. The system pressure was maintained
   at 1 atm throughout the 2-hour process."
```

### 4.4 Excessive Headings 제거

```
학술 논문은 IMRaD 대제목 외에 소제목은 최소화한다.
(단, 긴 Methods 섹션이나 저널 스타일에 따라 소제목 허용)

판단 기준:
  - 소제목 아래 단락이 1개뿐 → 소제목 삭제, 전환문으로 연결
  - 소제목이 2-3단어 이내 → 문장 내 구문으로 흡수 가능한지 검토
  - 소제목 빈도가 200w 이내마다 1개 → 과다 (산문 흐름 방해)
```

### 4.5 Markdown Artifact 정리

```
학술 논문에 부적절한 마크다운 서식:

| Artifact | Action |
|----------|--------|
| **bold text** | 제거 (학술 논문에서 본문 볼드는 부적절) |
| *italic text* | 변수명/학명만 유지, 강조용 이탤릭 제거 |
| `code format` | 소프트웨어명만 유지, 나머지 제거 |
| > blockquote | 직접 인용만 유지, 나머지 제거 |
| [link](url) | 인용 형식으로 변환 |
| emoji | 전부 삭제 |

규칙: 최종 출력은 plain text 학술 산문이어야 한다
```

---

## Change Log Format

각 Layer 교정 후 다음 형식으로 기록:

```
LAYER [N] CHANGE LOG:
  [1] ¶X, SY: [AI Word] → [Replacement] (Reason: [co-occurrence/excess/copula])
  [2] ¶X: [Structural change description] (Reason: [burstiness/template/tail])
  [3] ¶X, SY: [Added/Modified] [marker type] (Reason: [deficit type])
  [4] ¶X: [Formatting change] (Reason: [dash/list/header])
  ...

Layer [N] corrections: X items | Preserved: Y items (with justification)
```

---

## Self-Correction Awareness

**이 스킬은 Claude가 실행하므로, Claude 자체의 AI 패턴을 의식적으로 교정해야 한다.**

교정 텍스트를 작성할 때 다음을 자기 점검한다:

1. 내가 방금 쓴 교정문에 AI 과잉 단어를 새로 도입하지 않았는가?
2. 교정문의 문장 길이가 균일하지 않은가?
3. 전환어를 기계적으로 삽입하지 않았는가?
4. Em dash를 새로 사용하지 않았는가?
5. 지나치게 매끄럽고 우아한 문장을 쓰지 않았는가?

**교정 후 텍스트에 새로운 AI 패턴이 도입되면 안 된다.**

---

**This file is the operational guide for PHASE 2. Follow sequentially.**
