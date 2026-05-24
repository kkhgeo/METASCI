# Self-Diagnosis Protocol (Stage 1-A)

레퍼런스 없이 초고 자체의 내용 품질을 진단한다.
7개 항목을 순서대로 검사하고, 이슈별 교정을 적용한다.

**이 단계는 레퍼런스와 무관하게 객관적으로 판단 가능한 문제만 다룬다.**
논증 구조(레퍼런스 패턴 기반)는 Stage 1-B에서 처리한다.
스타일 차원(어휘, 문장구조, 톤 등)은 Stage 2에서 레퍼런스 기준으로 처리한다.

**진단 항목 구성:**
- 항목 1-4: 콘텐츠 품질 (중복/근거/필요성/배치)
- 항목 5-7: 무결성 감사 (어구 잡음/용어 일관성/정량·인용)

항목 5-7은 SciWrite (Sainani, Stanford) 원칙에서 가져왔으며,
Stage 2 (스타일 전이)와 충돌하지 않는 **레퍼런스 독립 규칙**만 포함한다.

---

## Preparation

진단 전 초고를 구조화한다:

1. 섹션 식별 (Introduction, Methods, Results, Discussion 등)
2. 단락 번호 매기기 (¶1, ¶2, ...)
3. 각 단락 내 문장 번호 매기기 (S1, S2, ...)
4. 각 문장을 역할별로 분류:
   - **Claim**: 주장, 해석, 결론
   - **Evidence**: 데이터, 수치, 인용 근거
   - **Context**: 배경 설명, 선행연구 요약
   - **Transition**: 연결 문장
   - **Filler**: 자명한 상식, 불필요한 반복

---

## Diagnostic Item 1: Redundancy (중복)

### What to check
- 동일한 정보가 2곳 이상에서 서술되는가
- 같은 데이터 포인트(수치, 범위, 결과)가 반복 보고되는가
- 동일한 주장이 다른 표현으로 반복되는가

### How to detect
1. 핵심 키워드/수치를 추출하여 리스트화
2. 초고 내에서 동일 키워드/수치의 출현 위치 매핑
3. 2회 이상 출현 시 판별:
   - 맥락이 다른가 (허용: Results에서 보고 → Discussion에서 해석)
   - 같은 목적으로 반복인가 (이슈)

### Action
- 더 상세한 서술 위치에 통합
- 간략한 쪽을 삭제 또는 참조로 대체 ("as noted above", "as described in Section X")

### Severity
| Condition | Severity |
|-----------|----------|
| 2곳 중복, 같은 섹션 내 | Minor |
| 2곳 중복, 다른 섹션 | Minor (맥락 상 허용 가능) |
| 3곳 이상 중복 | Major |
| 동일 문장 거의 그대로 반복 | Major |

---

## Diagnostic Item 2: Evidence Gap (근거 부족)

### What to check
- 주장(Claim)에 뒷받침하는 데이터, 인용, 논증이 있는가
- "~이다", "~를 보여준다" 등 단정적 서술에 근거가 따르는가
- 인과관계 주장에 메커니즘이나 데이터가 제시되는가

### How to detect
1. 각 문장의 역할(Role) 분류 결과 활용
2. **Claim → Evidence 짝짓기**: Claim 문장 뒤에 Evidence가 따르는지 확인
3. Evidence 없는 Claim → Evidence Gap
4. 특히 주의할 표현:
   - "This demonstrates that..." (근거 없이 단정)
   - "It is well known that..." (인용 없이 일반화)
   - "X causes Y" (메커니즘 설명 없는 인과 주장)

### Action
- 근거 추가 필요 표시 (사용자에게 데이터/인용 요청)
- 또는 hedging 처리 권장 ("may", "suggests", "could potentially")
- "well known" 류 표현 → 인용 추가 또는 삭제

### Severity
| Condition | Severity |
|-----------|----------|
| Discussion의 해석에 hedging 부족 | Minor |
| Results의 핵심 주장에 데이터 근거 없음 | Major |
| Introduction의 gap statement에 인용 없음 | Major |
| 인과관계 주장에 메커니즘 부재 | Major |

---

## Diagnostic Item 3: Structural Necessity (필요성)

### What to check
- 해당 문장을 삭제해도 논지 전개에 영향이 없는가
- 주제와 무관한 배경 서술이 과도한가
- "filler" 문장 (이미 알려진 상식을 장황하게 설명)

### How to detect
1. 각 문장의 역할(Role) 분류 결과 활용
2. **Filler**로 분류된 문장 → 삭제 후보
3. **Context**가 연속 3문장 이상 → 축약 후보
4. 삭제 테스트: "이 문장을 빼면 다음 문장이 이해 안 되는가?"
   - Yes → 필요 (유지)
   - No → 불필요 (삭제 후보)

### Action
- Filler 문장: 삭제 제안
- 과도한 Context: 축약 제안 (3문장 → 1문장)
- 판단 유보 시: 사용자에게 필요성 확인 요청

### Severity
| Condition | Severity |
|-----------|----------|
| 1-2 filler 문장 | Minor |
| 단락 전체가 불필요 | Major |
| Context 과다 (5문장 이상 연속 배경) | Minor |

---

## Diagnostic Item 4: Section Coherence (섹션 적합성)

### What to check
- 각 문장의 성격(nature)이 현재 섹션에 맞는가

### Section-Nature Mapping
| Nature | Belongs in |
|--------|-----------|
| 데이터 보고 (수치, 범위, 통계) | Results |
| 해석, 비교, 의의 | Discussion |
| 선행연구 요약, 연구 배경 | Introduction |
| 실험 절차, 분석 방법 | Methods |
| 핵심 발견 요약 | Abstract / Conclusion |

### How to detect
1. 각 문장의 성격(nature) 분류
2. 성격과 현재 섹션의 불일치 → Misplacement
3. 특히 주의:
   - Results에서 "compared to previous studies" (→ Discussion)
   - Discussion에서 새 데이터 제시 없이 수치 보고 (→ Results)
   - Introduction에서 결과를 상세 서술 (→ Results/Abstract)
   - Methods 내용이 Results에 혼재 (→ Methods)

### Action
- 이동 대상 명시: "¶X, S3 → Results 섹션으로 이동"
- 이동 시 전후 문맥 연결 필요 여부 표시
- 사용자가 의도적 배치인지 확인 요청 (필요시)

### Severity
| Condition | Severity |
|-----------|----------|
| 1문장 misplacement | Minor |
| 연속 2+ 문장 misplacement | Major |
| 단락 전체가 다른 섹션에 있어야 함 | Major |

---

## Diagnostic Item 5: Lexical Clutter (어구 잡음, 보수 적용)

> **출처:** SciWrite (Sainani) Pass 1 — Clutter Extraction
> **레퍼런스 독립성:** 항상 안전하게 잘라낼 수 있는 universally cuttable 어구만 다룬다.

### What to check
- 의미 전달에 기여하지 않는 도입 어구가 문장을 늘이고 있는가
- 같은 의미를 더 짧게 표현할 수 있는 다단어 전치사구 클러스터가 있는가

### How to detect

**Group A — Universally cuttable introductory phrases (전체 삭제):**

| Phrase | Action |
|---|---|
| "It is worth noting that" | 통째 삭제 |
| "It is important to note that" | 통째 삭제 |
| "It is interesting to note that" | 통째 삭제 |
| "It should be emphasized that" | 통째 삭제 |
| "As is well known" | 직접 인용으로 대체 또는 삭제 |
| "Needless to say" | 통째 삭제 |
| "It goes without saying that" | 통째 삭제 |

**Group B — Conservative replacements (의미 보존 시에만):**

| Cluttered | Replace with | 단, 보존 조건 |
|---|---|---|
| "due to the fact that" | "because" | hedge 기능 없음 → 항상 안전 |
| "in order to" | "to" | 강조 의도 없음 → 안전 |
| "at the present time" | "now" / "currently" | 안전 |
| "a majority of" | "most" | 정량 정확성 손실 없으면 안전 |
| "in light of the fact that" | "because" / "since" | 안전 |

**Group C — DO NOT TOUCH (Stage 2가 레퍼런스 기준으로 결정):**
- "is/are able to" ↔ "can" (해당 분야가 한쪽을 선호할 수 있음)
- "it is possible that" ↔ "may" (hedge 강도 차이)
- 일반 nominalization (예: "investigation of" ↔ "investigated") — Stage 2 Dim 5

### Action
- Group A: 자동 삭제 제안 (해당 도입 어구 다음 절은 그대로 유지)
- Group B: 치환 제안 (사용자 승인)
- Group C: 진단 대상 아님 (Stage 2로 이월)

### Boundary with Stage 2
Group A·B는 어떤 레퍼런스와도 충돌하지 않는 진단이다.
Stage 2 Dim 1(Tone)이 hedge 빈도를 레퍼런스에서 측정할 때, 이미
Group A 어구가 제거된 상태에서 hedge를 다시 추가하므로 충돌하지 않는다.

### Severity

| Condition | Severity |
|---|---|
| Group A 어구 3+개 출현 | Major |
| Group A 어구 1-2개 | Minor |
| Group B 치환 가능 어구 5+개 | Minor (일괄 처리 권장) |

---

## Diagnostic Item 6: Terminological Consistency (Banana Rule)

> **출처:** SciWrite (Sainani) Pass 4 — Keyword Consistency
> **레퍼런스 독립성:** 자기 논문 내부 용어 일관성은 어떤 레퍼런스 스타일에서도 보편 가치다.

### Core Principle (Banana Rule)
"바나나를 길쭉한 노란 과일이라 부르지 마라."
Methods에서 정의한 용어는 Results, Discussion, Tables, Figure captions
모두에서 **글자 그대로 동일하게** 사용해야 한다.
동의어 변주는 독자에게 "새로운 변수가 등장했나?"라는 혼란을 일으킨다.

### What to check
- Methods에서 정의된 핵심 용어(group/condition/variable/technique 이름, 약어)가
  Results/Discussion/Tables/Figure captions에서 동일 형태로 사용되는가
- 약어가 Abstract와 본문에서 각각 첫 사용 시점에 정의되는가
- 약어가 모든 Table caption과 Figure caption에서 재정의되는가
- 비표준 약어를 5회 미만 사용하면서 발명하지 않았는가

### How to detect

**Step 1 — Methods 핵심 용어 추출:**
1. Methods 섹션에서 정의된 모든 group/condition 이름 리스트화
2. 정의된 모든 약어 리스트화 (예: "freeze-thaw treatment (FT)")
3. 정의된 모든 변수/기법 이름 리스트화

**Step 2 — 후속 섹션에서 동의어 치환 감지:**
1. Results, Discussion, Tables, Figure captions에서 위 용어 검색
2. 동의어로 치환된 사례 식별:
   - Methods: "obese group (BMI ≥ 30)"
   - Results: "the heavier participants" ← 위반
   - Discussion: "high-BMI individuals" ← 위반
3. 약어 일관성 검사:
   - "FT" → "F-T" → "frost cycling" (3가지 형태) ← 위반

**Step 3 — 약어 정의 위치 검사:**
- Abstract에서 첫 사용 시 정의됐는가
- 본문에서 첫 사용 시 다시 정의됐는가 (독자가 Methods부터 읽지 않을 수 있음)
- 각 Table/Figure caption에서 정의됐는가 (caption은 비순차적으로 읽힘)

### Action
- 동의어 치환: canonical form (Methods 정의 형태)으로 통일 제안
- 약어 비일관성: 정의된 형태 하나로 통일
- 약어 정의 누락: 첫 사용 위치에 정의 추가
- 발명 약어 ≤4회 사용: 약어 폐기, 풀어쓰기 권장

### Boundary with Stage 2
Stage 2 Dim 5(Vocabulary)는 *어떤 어휘를 선호하는가*를 다룬다.
이 항목은 *같은 개념을 같은 표현으로 부르는가*를 다룬다.
두 가지는 직교 관계이므로 충돌하지 않는다.

### Severity

| Condition | Severity |
|---|---|
| Methods 정의 용어가 후속 섹션에서 2+ 다른 형태로 등장 | Major |
| 약어가 본문 또는 caption에서 정의 누락 | Major |
| 약어가 3+ 변형 형태로 사용 | Major |
| 발명 약어가 5회 미만 사용 | Minor |
| 단일 동의어 치환 1회 | Minor |

---

## Diagnostic Item 7: Quantitative & Citation Integrity

> **출처:** SciWrite (Sainani) Pass 5 — Numerical & Citation Integrity
> **레퍼런스 독립성:** 숫자 정합성과 1차 인용 추적은 보편 학술 무결성 기준이다.

### What to check
- 본문 내 동일 측정/표본수가 다른 위치에서 다른 값으로 보고되는가
- 백분율과 원시 카운트가 산술적으로 일치하는가
- 유효숫자가 일관되게 보고되는가
- 정량 주장이 1차 연구가 아닌 2차 자료(review/textbook/synthesis report)로만 인용되는가

### How to detect

**Step 1 — Numerical token 추출 및 cross-check:**
1. 초고 전체에서 정량 토큰 추출:
   - `N = <숫자>`, `n = <숫자>` (표본수)
   - `<숫자>%` (백분율)
   - `<숫자> ± <숫자>` (평균 ± 오차)
   - `<숫자> [단위]` (측정값)
   - `p = <숫자>`, `p < <숫자>` (p-값)
2. 동일 개념의 토큰이 다른 위치에서 다른 값으로 보고되는지 확인:
   - Abstract: "N = 120"
   - Methods: "N = 125" ← 위반
   - Results: "Of the 124 participants..." ← 위반
3. 백분율 ↔ 원시 카운트 산술 검증:
   - "Approximately 60% of samples (n = 38 of 100)" ← 60% × 100 ≠ 38, 위반

**Step 2 — Telephone Game audit (2차 인용 플래그):**
1. 각 정량 주장 옆 인용을 식별
2. 인용된 자료가 review/meta-analysis/textbook/synthesis report인지 판별:
   - 제목에 "review", "meta-analysis", "synthesis", "perspective" 포함
   - 학술지가 review 전용 (예: *Annual Review of...*, *Trends in...*)
   - 텍스트북/IPCC 보고서 등
3. 위 조건 충족 + 정량 주장 동반 → 2차 인용 경고

**Step 3 — 유효숫자/단위 drift:**
- 동일 측정이 한 곳에서 "12.3 ± 0.4", 다른 곳에서 "12.34"로 보고
- 동일 농도가 한 곳에서 "μM", 다른 곳에서 "μmol/L"로 표기

### Action
- 숫자 불일치: 사용자에게 정확한 값 확인 요청, 통일 제안
- 백분율 산술 오류: 즉시 플래그 (Critical)
- 2차 인용 경고: "원 1차 자료 추적을 권장합니다. 원 연구의 표본·방법이
  본 논문 맥락과 일치하는지 확인 필요."
- 유효숫자/단위 drift: 통일 제안

### Boundary with Stage 2
Stage 2 Dim 6(Citation & Evidence Style)은 *인용 형식*(narrative vs
parenthetical, 데이터 보고 포맷)을 레퍼런스 기준으로 결정한다.
이 항목은 *인용된 자료가 1차인가, 숫자가 정합한가*를 다룬다.
두 가지는 직교 관계이므로 충돌하지 않는다.

### Severity

| Condition | Severity |
|---|---|
| 표본수 N이 Abstract/Methods/Table 간 불일치 | Critical |
| 백분율 ↔ 원시 카운트 산술 오류 | Critical |
| 동일 측정의 단위 표기 불일치 | Major |
| 정량 주장이 review/textbook으로만 인용 (논증 핵심) | Major |
| 정량 주장이 review/textbook으로만 인용 (보조 맥락) | Minor |
| 유효숫자 drift | Minor |
| p-값 정밀도 drift | Minor |

---

## Diagnosis Report Format

```
================================================================
  CONTENT DIAGNOSIS — STAGE 1-A
  Section: [섹션 유형 또는 "전체"]
  Sentences: N | Paragraphs: N | Words: N
================================================================

[ISSUE 1] [Redundancy / Evidence Gap / Necessity / Coherence /
            Lexical Clutter / Terminological Consistency /
            Quantitative Integrity] — [Critical / Major / Minor] — ¶X, SY
  현재: "[문제 부분 인용]"
  문제: [구체적 진단 1-2줄]
  조치: [권장 행동]

[ISSUE 2] ...
[ISSUE 3] ...

─────────────────────────────
Content quality (Items 1-4): N issues
Integrity audit (Items 5-7): N issues
Total: N issues | Critical: N | Major: N | Minor: N
================================================================
```

**Critical 이슈는 항상 보고 상단에 표시한다** (정량 무결성 문제는
다른 이슈보다 우선순위가 높다).

---

## Pre-corrected Draft Format

교정 적용 후 출력:

```
================================================================
  PRE-CORRECTED DRAFT — STAGE 1-A
  Changes applied: N
================================================================

[교정된 전문]
(변경 부분은 **굵게**, 삭제는 ~~취소선~~, 추가는 _이탤릭_)

─────────────────────────────
CHANGE LOG:
  [1] [Type] ¶X: [변경 설명]
  [2] [Type] ¶Y, SZ: [변경 설명]
  ...

Issues resolved: N/N | Deferred to user: N
================================================================

Stage 1-A 자체 진단 교정이 완료되었습니다.
위 내용을 확인해주세요. 수정 의견이 있으면 말씀해주세요.
승인하시면 Stage 1-B (논증 구조 Monte Carlo)로 진행합니다.
```

---

## Edge Cases

| Situation | Response |
|-----------|----------|
| 초고가 단일 단락 | 7개 항목 모두 검사하되 Section Coherence와 Banana Rule(섹션 간 일관성)은 해당 없음으로 표시 |
| 초고가 3문장 미만 | "단락 이상의 텍스트를 권장합니다" 경고 후 가능한 범위 내 진단 |
| 이슈가 0개 | "자체 진단에서 이슈가 발견되지 않았습니다. Stage 1-B로 진행합니다." |
| Critical 이슈 1개 이상 | 사용자에게 즉시 알림. 정량 무결성 문제는 Stage 1-B 진입 전 반드시 해결 권장 |
| Major 이슈 5개 이상 | 우선순위 표시: Critical → Major → Minor 순서로 정렬 |
| 사용자가 특정 이슈 무시 요청 | 해당 이슈를 "user-deferred"로 표시하고 교정에서 제외 |
| 정량 토큰 cross-check가 1개 섹션만으로 불가능 | 항목 7의 within-paragraph 검사(백분율 ↔ 카운트, 단락 내 동일 측정 일관성)만 수행 |
| Methods 섹션 부재 | 항목 6의 용어 추출 source가 없음 → 약어 정의 위치 검사만 수행 |
