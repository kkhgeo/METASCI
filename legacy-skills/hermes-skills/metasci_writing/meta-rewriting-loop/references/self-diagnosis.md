# Self-Diagnosis Protocol (Stage 1-A)

레퍼런스 없이 초고 자체의 내용 품질을 진단한다.
4개 항목을 순서대로 검사하고, 이슈별 교정을 적용한다.

**이 단계는 레퍼런스와 무관하게 객관적으로 판단 가능한 문제만 다룬다.**
논증 구조(레퍼런스 패턴 기반)는 Stage 1-B에서 처리한다.

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

## Diagnosis Report Format

```
================================================================
  CONTENT DIAGNOSIS — STAGE 1-A
  Section: [섹션 유형 또는 "전체"]
  Sentences: N | Paragraphs: N | Words: N
================================================================

[ISSUE 1] [Redundancy / Evidence Gap / Necessity / Coherence] — [Major / Minor] — ¶X, SY
  현재: "[문제 부분 인용]"
  문제: [구체적 진단 1-2줄]
  조치: [권장 행동]

[ISSUE 2] ...
[ISSUE 3] ...

─────────────────────────────
Total: N issues | Major: N | Minor: N
================================================================
```

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
| 초고가 단일 단락 | 4개 항목 모두 검사하되 Section Coherence는 해당 없음으로 표시 |
| 초고가 3문장 미만 | "단락 이상의 텍스트를 권장합니다" 경고 후 가능한 범위 내 진단 |
| 이슈가 0개 | "자체 진단에서 이슈가 발견되지 않았습니다. Stage 1-B로 진행합니다." |
| Major 이슈 5개 이상 | 우선순위 표시: Major → Minor 순서로 정렬, 가장 critical한 것 먼저 |
| 사용자가 특정 이슈 무시 요청 | 해당 이슈를 "user-deferred"로 표시하고 교정에서 제외 |
