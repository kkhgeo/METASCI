# Monte Carlo Protocol

Stage 1-B (논증 구조)와 Stage 2 (스타일)에서 공통으로 사용하는 Monte Carlo 루프 프로토콜.

---

## Overview

```
Step 1: Independent Generation (병렬)
Step 2: Cross-Evaluation (스코어링)
Step 3: Champion Selection (차원별 최고 선발)
Step 4: Fusion (규칙 재조합 → 리라이팅)
Step 5: Verification (수렴 판정)
```

---

## Step 1: Independent Generation

각 Blueprint(또는 Dim 3 패턴)를 독립적으로 초고에 적용하여 후보를 생성한다.

### Rules
- 각 후보는 **독립 Subagent**로 생성 (서로 참조하지 않음)
- 각 후보는 동일한 입력 Draft를 받음
- 각 후보는 하나의 Blueprint만 적용
- 병렬 실행 권장

### Subagent Prompt Template (Stage 1-B: 논증 구조)

```
당신은 학술 논문 논증 구조 교정 전문가입니다.

다음 레퍼런스 논문의 논증 패턴(Logical Flow)을 이 초고에 적용하세요:

[Dim 3 패턴 전문 삽입]

초고:
[Pre-corrected Draft 전문 삽입]

규칙:
1. 논증 순서, 단락 구조, 섹션 전환, 반론 처리 방식만 변경
2. 모든 주장, 데이터, 인용을 그대로 보존
3. 전환 문장, 반론 단락 등 필요한 문장 추가 가능
4. 기존 문장 삭제 불가 (Stage 1-A에서 완료됨)
5. 과학적 의미 변경 절대 금지

출력: 교정된 전문 (변경 사항 간략 설명 포함)
```

### Subagent Prompt Template (Stage 2: 스타일)

```
당신은 학술 논문 스타일 전이 전문가입니다.

다음 레퍼런스 논문의 스타일 차원을 이 초고에 적용하세요:

[Dim 1 (Tone), Dim 2 (Sentence), Dim 4 (Transition), Dim 5 (Vocab), Dim 6 (Citation) 삽입]

초고:
[Corrected Draft 전문 삽입]

규칙:
1. 어휘, 문장구조, 톤, 전환표현, 인용 형식만 변경
2. 문장 분리/결합 가능 (스타일 목적)
3. 문장 삭제 불가, 주장 추가/제거 불가
4. 단락 순서 변경 불가 (Stage 1에서 확정됨)
5. 과학적 의미 변경 절대 금지

출력: 리라이팅된 전문 (변경 사항 간략 설명 포함)
```

---

## Step 2: Cross-Evaluation

각 후보를 해당 Stage의 평가 차원으로 스코어링한다.

### Stage 1-B 평가 차원 (5개)

| # | Sub-dimension | 평가 기준 | 높은 점수 예시 |
|---|---------------|-----------|---------------|
| 1 | Argument Sequence | 주장-근거-해석 순서가 논리적이고 자연스러운가 | Claim→Evidence→Interpretation 일관 |
| 2 | Counter-argument | 반론/대안 해석을 적절한 위치에서 다루는가 | "Although X, our data suggest Y" 형식 포함 |
| 3 | Section Transition | 섹션/단락 간 연결이 매끄럽고 논리적인가 | 각 단락 첫 문장이 이전 단락과 연결 |
| 4 | Paragraph Organization | 각 단락이 일관된 내부 구조를 갖는가 | 한 단락 = 하나의 주제, 명확한 topic sentence |
| 5 | Evidence Density | 근거가 주장에 근접하게 적절히 분배되어 있는가 | 모든 Claim 뒤에 Evidence 동반 |

### Stage 2 평가 차원 (5개)

| # | Dimension | 평가 기준 | 높은 점수 예시 |
|---|-----------|-----------|---------------|
| 1 | Tone & Stance | 톤, 능동/수동 비율, hedging이 학술적으로 적절한가 | 일관된 register, 적절한 hedging 빈도 |
| 2 | Sentence Architecture | 문장 길이, 복문 비율, 구조 패턴이 정교한가 | Blueprint 패턴과 일치, 자연스러운 리듬 |
| 4 | Transition Expressions | 전환표현이 적절하고 다양한가 | 기능별 (addition/contrast/causality) 골고루 |
| 5 | Vocabulary & Terminology | 학술 어휘 수준, 동사 선택이 정확한가 | Blueprint 선호 동사 사용, 비학술 표현 제거 |
| 6 | Citation & Evidence Style | 인용 통합, 데이터 보고 형식이 일관적인가 | 인용 형식 통일, 데이터 형식 일관 |

### Scoring Rules

1. 각 차원 **1-10 점** (정수)
2. 반드시 **구체적 근거 1줄** 첨부 (왜 이 점수인지)
3. 후보를 생성한 주체가 자기 후보를 평가하지 않는다

### Scoring Anchors

| Score | Meaning |
|-------|---------|
| 9-10 | 출판 수준, 수정 불필요 |
| 7-8 | 잘 되었으나 소소한 개선 가능 |
| 5-6 | 눈에 띄는 격차, 타겟 수정 필요 |
| 3-4 | 상당한 차이, 전면 재작업 권장 |
| 1-2 | 해당 차원이 거의 반영되지 않음 |

### Evaluation Table Format

```
================================================================
  CROSS-EVALUATION — [STAGE 1-B: Argumentation / STAGE 2: Style]
  Candidates: N | Dimensions: 5
================================================================

┌──────────┬──────┬──────┬──────┬──────┬──────┬──────┐
│          │ D-1  │ D-2  │ D-3  │ D-4  │ D-5  │ Avg  │
├──────────┼──────┼──────┼──────┼──────┼──────┼──────┤
│ Cand-A   │  X   │  X   │  X   │  X   │  X   │ X.X  │
│          │ [근거]│ [근거]│ [근거]│ [근거]│ [근거]│      │
├──────────┼──────┼──────┼──────┼──────┼──────┼──────┤
│ Cand-B   │  X   │  X   │  X   │  X   │  X   │ X.X  │
│          │ [근거]│ [근거]│ [근거]│ [근거]│ [근거]│      │
├──────────┼──────┼──────┼──────┼──────┼──────┼──────┤
│ Cand-C   │  X   │  X   │  X   │  X   │  X   │ X.X  │
│          │ [근거]│ [근거]│ [근거]│ [근거]│ [근거]│      │
└──────────┴──────┴──────┴──────┴──────┴──────┴──────┘

Champion: D-1=Cand-[X], D-2=Cand-[X], D-3=Cand-[X], D-4=Cand-[X], D-5=Cand-[X]
================================================================
```

---

## Step 3: Champion Selection

각 평가 차원에서 최고 점수를 받은 후보를 챔피언으로 선발한다.

### Rules

| Situation | Action |
|-----------|--------|
| 한 후보가 명확히 최고 | 해당 후보 선발 |
| 동점 (2개 후보) | 더 자연스럽고 구체적인 처리를 한 후보 선택 |
| 모든 차원에서 같은 후보가 최고 | Fusion 불필요, 해당 후보 직접 채택 |
| 특정 차원의 모든 후보 ≤ 4 | 해당 차원은 Fusion 후 targeted fix 필요 |

### Champion Map Format

```
Champion Map:
  D-1 ← Cand-A (score: 9) | 근거: "[1줄]"
  D-2 ← Cand-B (score: 8) | 근거: "[1줄]"
  D-3 ← Cand-B (score: 8) | 근거: "[1줄]"
  D-4 ← Cand-C (score: 9) | 근거: "[1줄]"
  D-5 ← Cand-A (score: 8) | 근거: "[1줄]"
```

---

## Step 4: Fusion

**반드시 `references/fusion-protocol.md`를 읽고 따른다.**

Champion Map에 따라:
1. 각 챔피언 후보에서 해당 차원의 **구체적 규칙/패턴** 추출
2. 규칙 간 **호환성 검사** (충돌 해결)
3. **Fusion Blueprint** 조립
4. 원본 Draft에 Fusion Blueprint를 **처음부터** 적용하여 리라이팅

**핵심: 텍스트 짜깁기가 아니라 규칙 재조합이다.**

---

## Step 5: Verification

Fused Draft를 동일한 평가 차원으로 다시 스코어링한다.

### Decision Table

| Condition | Action |
|-----------|--------|
| 모든 차원 ≥ 7 | **ACCEPT** — 수렴 완료 |
| 일부 차원 < 7, 나머지 ≥ 7 | 미달 차원만 **targeted fix** → 재스코어링 |
| 향상폭 < 0.3 (이전 대비) | **STOP** — 수렴 (추가 개선 미미) |
| Max Round 도달 | **STOP** — 예산 초과 |
| Fusion avg < 개별 best avg | 차선 Champion 조합 1회 시도 → 그래도 낮으면 **최고 개별 후보 채택** |

### Targeted Fix

특정 차원만 미달일 때:
1. 해당 차원의 챔피언 후보 규칙을 더 상세히 추출
2. Fused Draft에서 해당 부분만 재교정
3. 나머지 차원은 건드리지 않음
4. 재스코어링으로 확인

### Max Rounds

| Stage | Default | Description |
|-------|---------|-------------|
| Stage 1-B | 2 rounds | 논증 구조: 1회 Fusion + 1회 targeted fix |
| Stage 2 | 2 rounds | 스타일: 1회 Fusion + 1회 targeted fix |

사용자가 `Max Rounds: N`으로 조정 가능.

### Verification Report Format

```
================================================================
  VERIFICATION — [STAGE 1-B / STAGE 2] Round N
================================================================

Fused Draft scores:
  D-1: [X]/10  [이전 대비 +/-]
  D-2: [X]/10
  D-3: [X]/10
  D-4: [X]/10
  D-5: [X]/10
  ─────────────
  Avg: [X.X]/10

Status: [ACCEPT / TARGETED FIX / CONVERGED / MAX ROUND]

[If targeted fix:]
  Dimension [X] below threshold (score: N)
  → Fix strategy: [설명]

Preservation check:
  Arguments preserved: YES/NO
  Data preserved: YES/NO
  Citations preserved: YES/NO
================================================================
```
