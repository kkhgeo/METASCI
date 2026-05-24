---
name: meta-rewriting-loop
description: |
  Monte Carlo 방식의 다중 레퍼런스 기반 학술 논문 리라이팅 스킬.
  N개 레퍼런스에서 Style Blueprint를 추출하고 3단계 최적화를 거쳐 최선의 교정본을 생성한다.
  Stage 1-A (자체 진단: 중복/근거/필요성/배치) → Stage 1-B (논증 구조 Monte Carlo) → Stage 2 (스타일 Monte Carlo).
  각 Monte Carlo 단계에서 독립 후보 생성 → 교차 평가 → 차원별 챔피언 선발 → 장점 융합.
  Trigger phrases: "몬테카를로 리라이팅", "Monte Carlo rewriting", "다중 레퍼런스 리라이팅",
  "최적 교정", "multi-reference rewriting", "rewriting loop", "루프 리라이팅".
  **You MUST read references/ files at the corresponding Stage!**
allowed-tools: [Read, Write, Edit, Glob, Agent, Task, WebSearch, WebFetch]
---

> **REQUIRED**: Before starting each Stage, you MUST read the corresponding reference file.
> - PHASE 0: `references/blueprint-template.md`
> - STAGE 1-A: `references/self-diagnosis.md`
> - STAGE 1-B & 2: `references/monte-carlo-protocol.md`
> - FUSION: `references/fusion-protocol.md`
> - OUTPUT: `references/output-formats.md`

# Meta-Rewriting-Loop Skill

## Overview

Monte Carlo 방식의 다중 레퍼런스 기반 학술 논문 리라이팅 스킬.
N개의 레퍼런스 논문에서 Style Blueprint를 추출하고, 3단계 최적화를 거쳐 최선의 교정본을 생성한다.

**Core rule:** 레퍼런스에서 스타일과 논증 구조만 추출한다. 아이디어, 데이터, 주장은 절대 복사하지 않는다.

### Relationship to Other Skills

| Skill | Role | Difference |
|-------|------|------------|
| `meta-rewriting` | 1 Reference → 1 Blueprint → 1 Rewrite (one-shot) | meta-rewriting-loop는 N References → Monte Carlo → 최적 Fusion |
| `meta-styling` | Deep extraction → permanent databank (2-step) | meta-rewriting-loop는 한 세션에서 완결 |
| `meta-review` | 4-principle evaluation based on extraction files | meta-rewriting-loop는 자체 진단 + 레퍼런스 기반 논증 교정 포함 |
| `meta-writing` | Knowledge sources → writing from scratch | meta-rewriting-loop는 기존 초고의 교정/최적화 |

**Combined usage:**
- `meta-styling Mode A` 데이터뱅크가 있으면 Blueprint 대신 사용 가능
- `meta-review` 결과를 Stage 1-A 진단에 통합 가능

---

## Architecture

```
PHASE 0: Blueprint Pool Extraction (공유 자원)
  N References → N Blueprints (병렬 Subagent)
  ├── Dim 3 (Logical Flow) ──────→ Stage 1-B
  └── Dim 1,2,4,5,6 (Style) ────→ Stage 2
                ↓
STAGE 1-A: Self-Diagnosis (단일 패스, 레퍼런스 불필요)
  Original Draft → 중복/근거/필요성/배치 진단
  → Pre-corrected Draft
  → ★ User Confirmation Gate ★
                ↓
STAGE 1-B: Argumentation Monte Carlo
  Pre-corrected Draft × N개 Dim 3 패턴
  → N개 후보 독립 생성 (병렬)
  → 교차 평가 (5개 논증 하위 차원)
  → 차원별 챔피언 → Fusion → Corrected Draft
  → ★ User Confirmation Gate ★
                ↓
STAGE 2: Style Monte Carlo Loop
  Corrected Draft × N개 Style Blueprint (Dim 1,2,4,5,6)
  → N개 후보 독립 생성 (병렬)
  → 교차 평가 (5개 스타일 차원)
  → 차원별 챔피언 → Fusion → Verification
  → 수렴까지 반복
  → Final Draft
```

---

## Triggers

### Korean
- "몬테카를로 리라이팅"
- "다중 레퍼런스 리라이팅"
- "여러 논문 스타일로 최적화"
- "최적 교정본 만들어줘"
- "루프 리라이팅"
- "여러 레퍼런스로 리라이팅"

### English
- "Monte Carlo rewriting"
- "multi-reference rewriting"
- "rewriting loop"
- "optimize draft with multiple references"
- "best-of rewriting"

---

## PHASE 0: Blueprint Pool Extraction

N개 레퍼런스에서 Blueprint를 추출한다. 모든 Stage에서 공유하는 자원.

### Input Types

| Input type | Action |
|------------|--------|
| PDF file paths (multiple) | 각각 텍스트 추출 → Blueprint 생성 |
| Text pasted directly (multiple) | 각각 Blueprint 생성 |
| Journal names (multiple) | Web search로 스타일 정보 수집 |
| Mixed (PDF + journal name + text) | 각 유형별 처리 후 통합 |
| Existing Style databank path | `Style_{topic}/` → Blueprint 변환 |

### Extraction

**You MUST read `references/blueprint-template.md` first!**

- N개 레퍼런스를 **병렬 Subagent**로 동시 추출
- 각 Blueprint는 6차원 모두 추출
- 추출 완료 후 차원 분배:
  - **Dim 3 (Logical Flow)** → Stage 1-B로 전달
  - **Dim 1, 2, 4, 5, 6** → Stage 2로 전달

### Requirements

- 최소 2개 레퍼런스 (1개면 `meta-rewriting` 사용 권장)
- 최대 5개 권장 (초과 시 토큰 비용 경고)
- 레퍼런스 텍스트 500w 이상 → Confidence: High
- 200-500w → Confidence: Medium
- <200w 또는 저널명만 → Confidence: Low

### Subagent Prompt (Blueprint Extraction)

```
당신은 학술 논문 스타일 분석 전문가입니다.

다음 레퍼런스 텍스트에서 6개 차원의 Style Blueprint를 추출하세요.
references/blueprint-template.md의 형식과 기준을 따르세요.

각 차원에서:
- 2-3개 실제 문장을 인용 (추상적 설명 금지)
- 가능한 수치화 (평균 문장 길이, 수동태 비율 등)
- 3-5개 재사용 가능한 fill-in-the-blank 템플릿 생성

레퍼런스 텍스트:
[텍스트 삽입]
```

---

## STAGE 1-A: Self-Diagnosis (Single Pass)

레퍼런스 없이 초고 자체만 보고 진단한다.

**You MUST read `references/self-diagnosis.md` first!**

### 7 Diagnostic Items

콘텐츠 품질(1-4) + 무결성 감사(5-7). 모두 레퍼런스 독립.

| # | Item | What to check | Category |
|---|------|---------------|----------|
| 1 | Redundancy | 동일 정보 중복 서술 | Content |
| 2 | Evidence Gap | 근거 없는 주장 | Content |
| 3 | Structural Necessity | 삭제해도 논지에 영향 없는 문장 | Content |
| 4 | Section Coherence | 내용이 잘못된 섹션에 위치 | Content |
| 5 | Lexical Clutter | "It is worth noting that" 류 universally cuttable 어구 | Integrity |
| 6 | Terminological Consistency (Banana Rule) | Methods 정의 용어가 Results/Discussion에서 동의어로 치환, 약어 정의 누락 | Integrity |
| 7 | Quantitative & Citation Integrity | N/percentage/sig-fig 불일치, 정량 주장의 2차 인용 (Telephone Game) | Integrity |

항목 5-7은 SciWrite (Sainani, Stanford) 원칙 기반. Stage 2(스타일 전이)와
충돌하지 않는 보편 무결성 규칙만 포함하여 reference-driven 설계를 보호한다.

### Process

1. 초고 전체를 읽고 단락(¶)/문장(S) 번호 매기기
2. 7개 항목별로 이슈 식별 (1-4 콘텐츠, 5-7 무결성)
3. 각 이슈에 대해: 위치, 설명, 심각도(Critical/Major/Minor), 권장 조치
4. 교정 적용 → Pre-corrected Draft 생성
5. **User Confirmation Gate**: 진단 결과 + Pre-corrected Draft 표시
   - Critical 이슈(주로 정량 무결성)는 별도 강조하여 표시

### Gate Rule

사용자가 확인/수정 의견을 줄 때까지 Stage 1-B로 진행하지 않는다.
사용자가 수정 요청 시 반영 후 재확인.

---

## STAGE 1-B: Argumentation Structure Monte Carlo

N개 레퍼런스의 Dim 3 논증 패턴을 각각 독립 적용하여 최적 논증 구조를 찾는다.

**You MUST read `references/monte-carlo-protocol.md` first!**

### 5 Evaluation Sub-dimensions

| # | Sub-dimension | Description |
|---|---------------|-------------|
| 1 | Argument Sequence | 주장-근거-해석 순서가 논리적인가 |
| 2 | Counter-argument | 반론/대안 해석을 적절히 다루는가 |
| 3 | Section Transition | 섹션/단락 간 연결이 매끄러운가 |
| 4 | Paragraph Organization | 단락 내부 구조가 일관적인가 |
| 5 | Evidence Density | 근거가 주장에 근접하게 분배되어 있는가 |

### Process

1. **Independent Generation** (병렬 Subagent)
   - Pre-corrected Draft × Dim3-A → Structure-A
   - Pre-corrected Draft × Dim3-B → Structure-B
   - Pre-corrected Draft × Dim3-C → Structure-C

2. **Cross-Evaluation**: 각 후보를 5개 하위 차원으로 스코어링 (1-10)

3. **Champion Selection**: 하위 차원별 최고 점수 후보 선택

4. **Fusion**: 각 챔피언에서 규칙 추출 → Fusion Argumentation Guide → 리라이팅
   **You MUST read `references/fusion-protocol.md`!**

5. **Verification**: Fused Draft 재스코어링 → 수렴 판정

6. **User Confirmation Gate**

### Subagent Prompt (Structure Generation)

```
당신은 학술 논문 논증 구조 교정 전문가입니다.

다음 Blueprint의 Dim 3 (Logical Flow) 패턴을 이 초고에 적용하세요:

[Dim 3 패턴 삽입]

초고:
[Pre-corrected Draft 삽입]

규칙:
- 논증 순서, 단락 구조, 전환, 반론 처리 방식만 변경
- 모든 주장, 데이터, 인용 보존
- 문장 추가 가능 (전환문, 반론 단락 등)
- 문장 삭제 불가 (Stage 1-A에서 완료됨)
- 과학적 의미 변경 절대 금지

출력: 교정된 전문
```

### Preservation Rules (Stage 1-B)

- 모든 주장/데이터/인용 보존
- 논증 구조와 순서만 변경
- 문장 추가 가능 (전환문, 반론 등)
- 문장 삭제 불가

---

## STAGE 2: Style Monte Carlo Loop

Corrected Draft에 스타일 최적화를 적용한다. 내용/구조는 절대 변경하지 않는다.

**You MUST read `references/monte-carlo-protocol.md` first!**

### 5 Style Dimensions

| # | Dimension | What to evaluate |
|---|-----------|------------------|
| 1 | Tone & Stance | 톤, 능동/수동 비율, hedging |
| 2 | Sentence Architecture | 문장 길이, 복문 비율, 구조 패턴 |
| 4 | Transition Expressions | 전환표현 적절성, 다양성 |
| 5 | Vocabulary & Terminology | 학술 어휘, 동사 선택 |
| 6 | Citation & Evidence Style | 인용 형식, 데이터 보고 |

### Process

1. **Independent Generation** (병렬 Subagent)
   - Corrected Draft × Style-A (Dim 1,2,4,5,6) → Cand-A
   - Corrected Draft × Style-B (Dim 1,2,4,5,6) → Cand-B
   - Corrected Draft × Style-C (Dim 1,2,4,5,6) → Cand-C

2. **Cross-Evaluation**: 각 후보를 5개 스타일 차원으로 스코어링 (1-10)

3. **Champion Selection**: 차원별 최고 점수 후보 선택

4. **Fusion**: 각 챔피언에서 규칙 추출 → Fusion Style Blueprint → 리라이팅
   **You MUST read `references/fusion-protocol.md`!**

5. **Verification**: Fused Draft 재스코어링 → 수렴 판정

### Subagent Prompt (Style Generation)

```
당신은 학술 논문 스타일 전이 전문가입니다.

다음 Blueprint의 스타일 차원(Dim 1,2,4,5,6)을 이 초고에 적용하세요:

[Style 차원 삽입]

초고:
[Corrected Draft 삽입]

규칙:
- 어휘, 문장구조, 톤, 전환표현, 인용 형식만 변경
- 문장 분리/결합 가능 (스타일 목적)
- 문장 삭제 불가, 주장 추가/제거 불가
- 단락 순서 변경 불가 (Stage 1에서 확정됨)
- 과학적 의미 변경 절대 금지

출력: 리라이팅된 전문
```

### Preservation Rules (Stage 2)

- ✓ 문장 분리/결합 가능 (스타일 목적)
- ✗ 문장 삭제 불가
- ✗ 주장 추가/제거 불가
- ✗ 단락 순서 변경 불가
- ✓ 어휘, 문장구조, 톤, 전환어, 인용 형식 변경 가능

---

## Convergence & Stopping

Stage 1-B와 Stage 2 공통.

| Condition | Action |
|-----------|--------|
| 모든 차원 ≥ 7 | ACCEPT — 수렴 |
| 향상폭 < 0.3 (이전 라운드 대비) | STOP — 수렴 |
| Max Round 도달 (기본 2) | STOP |
| Fusion이 개별 후보 best avg보다 낮음 | 차선 조합 1회 시도, 그래도 낮으면 최고 개별 후보 채택 |
| 사용자 중단 | STOP |

---

## Output Structure

모든 출력은 `Rewrite_{topic}/` 폴더에 저장한다.

```
Rewrite_{topic}/
├── blueprints/
│   ├── blueprint_A.md
│   ├── blueprint_B.md
│   └── blueprint_C.md
├── stage1a_diagnosis.md
├── stage1a_pre_corrected.md
├── stage1b_evaluation.md
├── stage1b_corrected.md
├── stage2_evaluation.md
├── stage2_fusion_blueprint.md
├── final_draft.md
└── session_log.md
```

`{topic}`은 사용자 지정 또는 레퍼런스 논문/저널명에서 자동 도출.

---

## Parallel Processing (Subagent)

| Stage | Parallelizable | Method |
|-------|---------------|--------|
| PHASE 0 | Yes | N개 Blueprint 동시 추출 |
| Stage 1-A | No | 단일 패스 |
| Stage 1-B Generation | Yes | N개 Structure 후보 동시 생성 |
| Stage 1-B Evaluation | Yes | N개 후보 동시 평가 |
| Stage 2 Generation | Yes | N개 Style 후보 동시 생성 |
| Stage 2 Evaluation | Yes | N개 후보 동시 평가 |

---

## Interactive Setup

사용자가 충분한 컨텍스트 없이 스킬을 호출한 경우:

### Batch 1 (필수)
```
meta-rewriting-loop를 시작합니다.

1. 레퍼런스 논문을 제공해주세요 (최소 2개):
   - PDF 파일 경로, 텍스트 직접 붙여넣기, 또는 저널명

2. 교정할 초고를 제공해주세요:
   - PDF 파일 경로, 텍스트 직접 붙여넣기

3. 섹션 유형 (선택사항):
   - Introduction / Methods / Results / Discussion / Abstract / 전체
```

### Batch 2 (선택)
```
추가 설정 (기본값 적용 가능):

4. 출력 폴더명: [기본: Rewrite_{자동도출}]
5. Stage 건너뛰기: [없음 / 1-A / 1-B] (기본: 없음)
6. Max Rounds: [기본: 2]
```

---

## Quality Standards

1. **Style transfer only (Stage 2)**: 레퍼런스에서 스타일만 추출, 아이디어/데이터 복사 금지
2. **Content preservation**: Stage 1에서 확정된 내용은 Stage 2에서 절대 변경 불가
3. **Evidence-based**: 모든 교정에 Blueprint 차원/규칙 근거 명시
4. **Quantitative scoring**: 차원별 1-10 스코어링 필수
5. **Traceable**: 각 편집에 적용된 차원, 출처 후보(A/B/C), 규칙 명시
6. **Natural prose**: 기계적 치환이 아닌 자연스러운 학술 문체
7. **User gates**: Stage 전환 시 사용자 확인 필수 (1-A→1-B, 1-B→2)

---

## Error Handling

| Situation | Response |
|-----------|----------|
| 레퍼런스 1개만 제공 | "`meta-rewriting` 사용을 권장합니다. 2개 이상 필요합니다." |
| 레퍼런스 6개 이상 | "토큰 비용이 높아집니다. 가장 관련성 높은 3-5개를 선택하세요." |
| 레퍼런스 텍스트 <200w | Confidence: Low 경고 |
| 초고 <3 문장 | "단락 이상의 텍스트를 권장합니다" |
| 후보 간 점수 차이 <1.0 전 차원 | "후보 간 차이가 미미합니다. 최고 평균 후보를 채택합니다." |
| Fusion이 개별 best보다 낮음 | 차선 조합 1회 시도 → 그래도 낮으면 최고 개별 후보 채택 |
| Stage 건너뛰기 요청 | 허용 (e.g., "Stage 1-A 건너뛰고 논증 구조부터") |
| 레퍼런스와 초고의 분야가 다름 | 경고 표시 후 진행 (스타일 전이는 분야 독립적) |

---

## Usage Examples

### Example 1: 3개 GCA 논문으로 Discussion 최적화
```
> "이 3편 GCA 논문 기반으로 내 Discussion 리라이팅해줘"
→ PHASE 0: 3 Blueprints 추출
→ Stage 1-A: 자체 진단 → 중복 제거, 근거 보강
→ Stage 1-B: 3개 Dim3 패턴으로 Monte Carlo → 최적 논증 구조
→ Stage 2: 3개 Style로 Monte Carlo → 최적 스타일 융합
→ Final Draft
```

### Example 2: 서로 다른 저널 레퍼런스 혼합
```
> "GCA 1편, ES&T 1편, Nature Geo 1편으로 내 Introduction 최적화"
→ 다양한 스타일 풀에서 각 차원의 최적 요소 선발
```

### Example 3: Stage 선택 실행
```
> "논리 교정은 됐고, 스타일만 Monte Carlo로 해줘"
→ Stage 1 건너뛰기 → Stage 2만 실행
```

### Example 4: 기존 데이터뱅크 활용
```
> "Style_지화학/ 데이터뱅크 + 추가 논문 2편으로 리라이팅"
→ 데이터뱅크 → Blueprint 변환 + 2편 추출 → 3개 Blueprint로 Monte Carlo
```

---

## References

| File | Read when | Content |
|------|-----------|---------|
| `references/blueprint-template.md` | PHASE 0 | 6차원 Blueprint 추출 가이드 + 차원 분배 규칙 |
| `references/self-diagnosis.md` | Stage 1-A | 자체 진단 4항목 기준, 심각도, 출력 형식 |
| `references/monte-carlo-protocol.md` | Stage 1-B & 2 | Monte Carlo 루프 프로토콜 (공통) |
| `references/fusion-protocol.md` | Fusion 단계 | Fusion Blueprint 생성 규칙 |
| `references/output-formats.md` | 전체 | 모든 출력 카드 형식 |

---

**Version**: 1.0.0
**Skill by**: KEI / meta-rewriting-loop
