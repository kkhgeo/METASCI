# Fusion Protocol

Champion Map 기반으로 Fusion Blueprint를 생성하는 상세 프로토콜.
Stage 1-B (논증 구조)와 Stage 2 (스타일) 모두에 적용된다.

---

## Core Principle

**Fusion = 규칙 재조합. 텍스트 짜깁기가 아니다.**

```
✗ 잘못된 Fusion:
  Cand-A의 ¶1 + Cand-B의 ¶2 + Cand-C의 ¶3 이어붙이기

✓ 올바른 Fusion:
  각 챔피언에서 "왜 높은 점수를 받았는지" 규칙을 추출
  → 규칙들을 조합한 새로운 Fusion Blueprint 생성
  → 원본 Draft를 처음부터 다시 리라이팅
```

---

## Fusion Process (3 Steps)

### Step 1: Rule Extraction

각 챔피언 후보에서 해당 차원의 구체적 규칙을 추출한다.

**추출 대상:**
- 해당 차원에서 후보가 사용한 구체적 패턴/표현
- 후보가 원본 Draft를 어떻게 변환했는지 (before → after 예시)
- 적용된 Blueprint 규칙의 핵심

**추출 형식 (Stage 2 예시):**
```
Dim-1 Champion: Cand-A
  Rule 1: "We" 주어로 시작하는 문장 40% 이상
  Rule 2: hedging은 "suggest", "indicate"로 제한
  Rule 3: 결론 단락에서만 단정적 어조 허용
  Example: "We demonstrate that..." (not "It was shown that...")
```

**추출 형식 (Stage 1-B 예시):**
```
Sub-dim 2 Champion: Cand-C (Counter-argument)
  Rule 1: Discussion 중반에 별도 반론 단락 배치
  Rule 2: "Although X, our data suggest Y" 형식
  Rule 3: 반론 후 즉시 자기 데이터로 반박
  Example: "While previous studies suggested ..., the present results indicate ..."
```

---

### Step 2: Compatibility Check

추출된 규칙들 간 충돌이 없는지 검사한다.

**가능한 충돌 유형:**

| 충돌 유형 | 예시 | 해결 방법 |
|-----------|------|-----------|
| 톤 vs 어휘 | Dim-1이 적극 hedging + Dim-5가 단정 동사 선호 | Dim-1(톤) 우선 |
| 문장구조 vs 전환표현 | Dim-2가 단문 선호 + Dim-4가 복문 연결 전환어 | 전환어를 문장 사이에 배치 |
| 인용 vs 문장구조 | Dim-6이 서술형 인용 + Dim-2가 짧은 문장 | 인용을 별도 문장으로 분리 |
| 논증순서 vs 근거배치 | Sub-3이 foreshadow 전환 + Sub-1이 data-first | 전환문 후 data-first 유지 |

**충돌 해결 우선순위:**

```
1위: Content preservation (절대 불변)
2위: Argumentation structure (Dim 3 / Stage 1-B 결과)
3위: Tone & Stance (Dim 1)
4위: Vocabulary (Dim 5)
5위: Sentence Architecture (Dim 2)
6위: Transitions (Dim 4)
7위: Citation Style (Dim 6)
```

상위 규칙과 하위 규칙이 충돌하면, 상위 규칙을 유지하고 하위 규칙을 조정한다.

---

### Step 3: Fusion Blueprint Assembly

충돌 해결 후 통합된 Fusion Blueprint를 조립한다.

**Fusion Blueprint 형식:**

```
================================================================
  FUSION BLUEPRINT — [STAGE 1-B: Argumentation / STAGE 2: Style]
  Champions: D-1=[A], D-2=[B], D-3=[B], D-4=[C], D-5=[A]
================================================================

Dim-1: [from Cand-X]
  Rules:
    1. [구체적 규칙]
    2. [구체적 규칙]
    3. [구체적 규칙]
  Template sentences:
    - "[fill-in-the-blank 1]"
    - "[fill-in-the-blank 2]"

Dim-2: [from Cand-X]
  Rules:
    1. [구체적 규칙]
    2. [구체적 규칙]
  Template sentences:
    - "[fill-in-the-blank]"

...

Compatibility notes:
  - [충돌 해결 사항 1]
  - [충돌 해결 사항 2]
================================================================
```

---

## Fusion Rewriting Rules

Fusion Blueprint로 Draft를 리라이팅할 때:

1. **전체를 처음부터 다시 쓴다** — 부분 패치가 아님
2. 모든 차원의 규칙을 **동시에** 적용
3. 충돌 시 위의 우선순위에 따라 결정
4. 리라이팅 후 **Preservation Check** 수행:
   - [ ] 모든 주장(claim) 보존 확인
   - [ ] 모든 데이터 포인트 보존 확인
   - [ ] 모든 인용(citation) 보존 확인
   - [ ] Figure/Table 참조 번호 유지 확인
   - [ ] 과학적 의미 변경 없음 확인
5. Preservation Check 실패 시: 해당 부분 즉시 수정

---

## Edge Cases

### 모든 차원에서 같은 후보가 챔피언

Fusion 불필요. 해당 후보를 직접 채택.
단, 모든 차원 ≥ 7인지 확인. 미달 차원이 있으면 다른 후보에서 해당 차원 규칙만 가져와 targeted fix.

### 특정 차원의 모든 후보가 ≤ 4

해당 차원은 레퍼런스 Blueprint 자체의 한계.
1. Blueprint를 다시 검토하여 더 상세한 규칙 추출 시도
2. 그래도 개선 불가 시: "이 차원은 수동 교정 필요"로 표시

### Fusion Draft가 개별 후보 최고 평균보다 낮음

규칙 간 충돌이 제대로 해결되지 않았을 가능성.
1. Compatibility Check 재실행
2. 차선 Champion Map 시도 (2위 점수 후보로 교체)
3. 1회 재시도 후에도 낮으면: 최고 평균 개별 후보를 채택
4. Session Log에 "Fusion failed, best individual candidate adopted" 기록

### 후보가 2개뿐일 때

2개로도 Monte Carlo 가능. 동일 프로토콜 적용.
다만 다양성이 낮으므로:
- 각 차원에서 2개 중 더 나은 것 선택
- 차이가 미미하면 (점수 차 <1) 높은 평균 후보 직접 채택

---

## Stage-Specific Notes

### Stage 1-B (논증 구조) Fusion

- Fusion 대상: 5개 논증 하위 차원의 규칙
- 리라이팅 시 **문장 추가 허용** (전환문, 반론 등)
- 리라이팅 시 **문장 삭제 불가**
- 리라이팅 시 **단락 순서 변경 가능** (논증 구조 교정이므로)

### Stage 2 (스타일) Fusion

- Fusion 대상: 5개 스타일 차원의 규칙
- 리라이팅 시 **문장 분리/결합 허용** (스타일 목적)
- 리라이팅 시 **문장 삭제 불가**
- 리라이팅 시 **단락 순서 변경 불가** (Stage 1에서 확정됨)
- 리라이팅 시 **주장 추가/제거 불가**
