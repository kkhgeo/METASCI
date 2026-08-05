---
name: meta-rewriting-antiai
description: |
  AI 글쓰기 흔적을 제거하고 자연스러운 학술 산문으로 전환하는 스킬.
  4계층 체계(Lexical → Syntactic → Discourse → Formatting)로 AI 특유의
  어휘 패턴, 구문 균일성, 저자 목소리 부재, 과잉 구조화를 진단하고 교정한다.
  어떤 meta 스킬의 출력이든 마지막 파이프라인으로 적용 가능.
  Trigger phrases: "anti-AI 교정", "AI 흔적 제거", "자연화", "naturalization",
  "anti-AI rewriting", "AI 탐지 대응", "humanize writing".
  **You MUST read references/ files before each Phase!**
allowed-tools: [Read, Write, Edit, Glob, Agent, Task]
---

> **REQUIRED**: Before starting each Phase, you MUST read the corresponding reference file.
> - PHASE 1 (Scan): `references/ai-lexicon.md`
> - PHASE 2 (Naturalization): `references/naturalization-guide.md`
> - OUTPUT: `references/output-formats.md`

# Meta-Rewriting-AntiAI Skill

## Overview

AI 글쓰기 흔적을 4계층으로 진단하고 자연스러운 학술 산문으로 전환한다.
AI 탐지 회피가 아니라 **학술 글쓰기 품질 향상**이 목적이다.

**Core rule:** 과학적 의미와 논증 구조를 절대 변경하지 않는다. 어휘, 문장 구조, 담화 표현, 포매팅만 교정한다.

### Relationship to Other Skills

| Skill | Role | Difference |
|-------|------|------------|
| `meta-rewriting` | 1 Reference → Style transfer | meta-rewriting-antiai는 레퍼런스 불필요, AI 흔적 제거 특화 |
| `meta-rewriting-loop` | N References → Monte Carlo optimization | meta-rewriting-antiai는 그 출력의 후처리로 사용 가능 |
| `meta-styling` | Databank 기반 스타일 교정 | meta-rewriting-antiai는 스타일이 아닌 AI 패턴 제거 |
| `meta-review` | 4-principle evaluation | meta-rewriting-antiai는 평가가 아닌 교정 실행 |
| `paper-proofreader` | 문장/단락 수준 교정 | meta-rewriting-antiai는 AI 특유 패턴만 타겟 |

### Pipeline Position

```
meta-writing ──────────────┐
meta-rewriting ────────────┤
meta-rewriting-loop ───────┼──→ meta-rewriting-antiai → Final Output
meta-styling Mode B ───────┤
paper-proofreader ─────────┤
직접 작성한 초고 ──────────┘
```

**어떤 경로든 마지막 단계로 적용 가능한 독립 스킬.**

---

## Architecture

```
PHASE 1: AI Fingerprint Scan (진단)
  Input Draft → 4-Layer Analysis
  ├── Layer 1: Lexical Scan ─────── AI 과잉 어휘 + 공기 패턴
  ├── Layer 2: Syntactic Scan ───── 문장 길이 균일성, 구문 반복
  ├── Layer 3: Discourse Scan ───── 저자 목소리, metadiscourse
  └── Layer 4: Formatting Scan ──── em dash, list 구조, Rule of Three
  → Diagnostic Report (4-Layer scores)
  → ★ User Confirmation Gate ★
              ↓
PHASE 2: 4-Layer Naturalization (교정)
  Diagnostic Report + Input Draft
  → Layer-by-layer sequential correction
  → Naturalized Draft
  → Verification (re-scan)
  → ★ User Confirmation Gate ★
              ↓
OUTPUT: Naturalized Final Draft + Session Log
```

---

## Triggers

### Korean
- "anti-AI 교정"
- "AI 흔적 제거"
- "자연화"
- "AI 탐지 대응"
- "AI 글쓰기 교정"
- "자연스러운 글로 바꿔줘"
- "AI 티 좀 빼줘"

### English
- "anti-AI rewriting"
- "naturalization"
- "humanize writing"
- "remove AI fingerprints"
- "anti-AI polish"

---

## PHASE 1: AI Fingerprint Scan

입력 텍스트에서 AI 글쓰기 흔적을 4계층으로 진단한다.

**You MUST read `references/ai-lexicon.md` first!**

### Layer 1: Lexical Scan (어휘)

| Check | What to detect | Severity |
|-------|----------------|----------|
| AI Excess Words | 774개 과잉 단어 목록 대조 (delve, underscore, pivotal, meticulous...) | Major if ≥3 per paragraph |
| Co-occurrence Patterns | AI 단어 조합 (intricate+meticulous, comprehensive+pivotal...) | Critical if any pair found |
| Copula Avoidance | "serves as", "stands as", "marks the" → "is/are" 회피 패턴 | Minor |
| Elegant Variation | 동일 대상을 불필요한 동의어로 반복 교체 | Minor |
| Register Mismatch | 과도하게 격식적이거나 홍보성 어휘 | Major |

### Layer 2: Syntactic Scan (구문)

| Check | What to detect | Severity |
|-------|----------------|----------|
| Sentence Length Uniformity | 문장 길이 표준편차 < 5 words → 균일함 의심 | Major |
| Syntactic Template Repetition | 동일 POS 패턴 3회 이상 연속 | Major |
| -ing Tail Pattern | "~, highlighting...", "~, emphasizing..." 꼬리 구문 | Major |
| Rule of Three | "X, Y, and Z" 3항목 나열 2회 이상 | Minor |
| "Not just X, but also Y" | 부정 병렬 구문 반복 | Minor |
| Uniform Paragraph Length | 단락 길이 표준편차 < 15 words → 균일함 의심 | Minor |

### Layer 3: Discourse Scan (담화)

| Check | What to detect | Severity |
|-------|----------------|----------|
| Hedge Deficit | may/might/could/suggest 부족 (학술 글에서 필수) | Major |
| Booster Deficit | clearly/certainly/undoubtedly/demonstrate 부재 | Major |
| Self-mention Absence | we/our/this study 같은 저자 개입 표현 부재 | Major |
| Attitude Marker Absence | importantly/surprisingly/interestingly 부재 | Minor |
| Transition Overuse | Furthermore/Moreover/Additionally 과다 (단락당 2+ 시) | Major |
| Excessive Balance | 불필요한 양면 제시 ("while X, Y also...") | Minor |

### Layer 4: Formatting Scan (서식)

| Check | What to detect | Severity |
|-------|----------------|----------|
| Em Dash Overuse | 단락당 em dash (—) 2회 이상 | Major |
| List in Prose | 산문이어야 할 곳에 bullet/numbered list | Critical |
| Inline-Header Pattern | "**Term**: description" 형태의 볼드 정의 목록 | Critical |
| Excessive Headings | 산문 흐름을 끊는 과도한 소제목 | Major |
| Table Overuse | 산문으로 충분한 내용의 불필요한 표 | Minor |
| Markdown Artifacts | 볼드, 이탤릭 등 학술 논문에 부적절한 마크다운 | Critical |

### Scoring

각 Layer를 1–10으로 스코어링한다.

| Score | Meaning |
|-------|---------|
| 9–10 | AI 흔적 거의 없음 — 자연스러운 학술 산문 |
| 7–8 | 경미한 흔적 — 소수 항목 교정 필요 |
| 5–6 | 뚜렷한 흔적 — 다수 항목 교정 필요 |
| 3–4 | 강한 AI 패턴 — 전면 교정 필요 |
| 1–2 | AI 생성 텍스트 수준 |

### Diagnostic Output

진단 결과를 Diagnostic Card로 출력한다.

**You MUST read `references/output-formats.md` for card format!**

### Gate Rule

사용자가 진단 결과를 확인하고 교정 범위를 지정할 때까지 PHASE 2로 진행하지 않는다.
사용자는 특정 Layer만 교정하도록 선택할 수 있다.

---

## PHASE 2: 4-Layer Naturalization

진단 결과를 기반으로 4계층 순서대로 교정한다.

**You MUST read `references/naturalization-guide.md` first!**

### Execution Order

**반드시 Layer 1 → 2 → 3 → 4 순서로 실행한다.**

이유:
- Layer 1(어휘 교체)이 Layer 2(구문)에 영향
- Layer 2(구문 재구성)가 Layer 3(담화 표현 삽입 위치)에 영향
- Layer 3(담화 교정)이 완료되어야 Layer 4(서식) 최종 정리 가능

### Layer 1: Lexical Naturalization (어휘 자연화)

| Action | Method |
|--------|--------|
| AI Excess Words 교체 | 동일 의미의 일반적 학술 어휘로 대체 (1:1 대응표 참조) |
| Co-occurrence 분산 | 한 쌍의 AI 단어가 같은 단락에 없도록 분산/대체 |
| Copula 복원 | "serves as" → "is", "stands as" → "is" 등 자연스러운 copula 복원 |
| Elegant Variation 정리 | 동일 대상은 1-2개 용어로 일관 사용 |

### Layer 2: Syntactic Naturalization (구문 자연화)

| Action | Method |
|--------|--------|
| Burstiness 주입 | 긴 문장 뒤에 짧은 문장 배치, 문장 길이 표준편차 ≥ 8 words 목표 |
| -ing Tail 제거 | 독립 문장으로 분리하거나 다른 구문으로 재구성 |
| Rule of Three 해소 | 3항목 중 1개 삭제하거나 별도 문장으로 전개 |
| 구문 다양화 | 단문/복문/도치/분사구문 교차 사용 |
| 부정 병렬 재구성 | "Not just X, but Y" → 독립 문장 2개로 분리 |

### Layer 3: Discourse Naturalization (담화 자연화)

| Action | Method |
|--------|--------|
| Hedging 보강 | 주장에 적절한 hedging 삽입 (may, could, suggest, appear to) |
| Booster 삽입 | 핵심 발견에 booster 삽입 (clearly, notably, demonstrate) |
| Self-mention 회복 | "We found...", "Our results...", "This study..." 삽입 |
| Attitude Marker 추가 | "Importantly,", "Surprisingly,", "Notably," 적소에 삽입 |
| Transition 다양화 | Furthermore/Moreover → 구체적 논리 관계 표현으로 대체 |

### Layer 4: Formatting Naturalization (서식 자연화)

| Action | Method |
|--------|--------|
| Em Dash 감축 | 단락당 1회 이하, 나머지는 콤마/괄호/문장 분리로 대체 |
| List → Prose 변환 | bullet/numbered list를 연결 산문으로 변환 |
| Inline-Header 제거 | "**Term**: desc" → 산문 문장으로 통합 |
| 불필요한 헤딩 제거 | 소제목 없이 전환문으로 흐름 연결 |
| Markdown 정리 | 학술 논문에 부적절한 마크다운 서식 제거 |

### Preservation Rules

- ✓ 어휘, 문장구조, 담화 표현, 서식 변경 가능
- ✓ 문장 분리/결합 가능 (자연화 목적)
- ✗ 주장/데이터/인용 추가/제거/변경 불가
- ✗ 단락 순서 변경 불가
- ✗ 과학적 의미 변경 절대 금지

### Verification

교정 완료 후, PHASE 1과 동일한 기준으로 재스캔한다.

| Condition | Action |
|-----------|--------|
| 모든 Layer ≥ 7 | ACCEPT — 자연화 완료 |
| 개선폭 < 0.5 (이전 대비) | ACCEPT — 추가 교정 효과 미미 |
| 특정 Layer < 5 | 해당 Layer만 재교정 1회 |
| 사용자 중단 | STOP |

### Gate Rule

교정 결과 + Verification 점수를 사용자에게 표시.
사용자 확인 후 최종 출력.

---

## Output Structure

모든 출력은 `AntiAI_{topic}/` 폴더에 저장한다.

```
AntiAI_{topic}/
├── phase1_diagnostic.md       ← 4-Layer 진단 리포트
├── phase2_changelog.md        ← 교정 내역 (Layer별)
├── phase2_verification.md     ← 교정 후 재진단 결과
├── naturalized_draft.md       ← 최종 자연화 결과물
└── session_log.md             ← 세션 기록
```

`{topic}`은 사용자 지정 또는 입력 텍스트에서 자동 도출.

---

## Interactive Setup

사용자가 충분한 컨텍스트 없이 스킬을 호출한 경우:

### Batch 1 (필수)
```
meta-rewriting-antiai를 시작합니다.

1. 교정할 텍스트를 제공해주세요:
   - 파일 경로, 텍스트 직접 붙여넣기, 또는 이전 스킬 출력 폴더 경로

2. 섹션 유형 (선택사항):
   - Introduction / Methods / Results / Discussion / Abstract / 전체
```

### Batch 2 (선택)
```
추가 설정 (기본값 적용 가능):

3. 교정 범위: [전체 / Layer 선택] (기본: 전체)
4. 출력 폴더명: [기본: AntiAI_{자동도출}]
5. 강도: [Light / Standard / Deep] (기본: Standard)
```

### Intensity Levels

| Level | Description |
|-------|-------------|
| Light | Critical + Major 이슈만 교정. 문체 변경 최소화 |
| Standard | Critical + Major + 일부 Minor 교정. 균형잡힌 자연화 |
| Deep | 모든 이슈 교정 + burstiness/discourse 적극 보강 |

---

## Quality Standards

1. **Content preservation**: 모든 주장, 데이터, 인용은 원본 그대로 보존
2. **Scientific accuracy**: 과학적 의미 변경 절대 금지
3. **Academic register**: 학술적 격식성은 유지하되 AI 과잉 수사만 제거
4. **Evidence-based**: 모든 교정에 해당 Layer, Check 항목, 구체적 근거 명시
5. **Natural prose**: 기계적 치환이 아닌 문맥에 맞는 자연스러운 대체
6. **Co-occurrence awareness**: 개별 단어가 아닌 단어 조합 패턴 단위로 교정
7. **Traceable**: 각 편집에 Layer 번호, Check 항목, 변경 전/후 명시

---

## Error Handling

| Situation | Response |
|-----------|----------|
| 입력 텍스트 < 3 문장 | "단락 이상의 텍스트를 권장합니다" |
| 이미 자연스러운 텍스트 (모든 Layer ≥ 8) | "AI 흔적이 거의 없습니다. 교정이 필요하지 않습니다." |
| 인간이 작성한 원본 텍스트 | 정상 작동 (인간 글에도 AI 유사 패턴이 있을 수 있음) |
| 특정 Layer만 교정 요청 | 해당 Layer만 실행 |
| 비영어 텍스트 | "현재 영어 학술 글쓰기에 최적화되어 있습니다" 경고 후 진행 |
| Markdown/LaTeX 혼합 | Markdown 서식만 정리, LaTeX 수식/명령어 보존 |
| 교정 후 오히려 점수 하락 | 해당 Layer 교정 취소, 원본 유지 |

---

## Usage Examples

### Example 1: meta-rewriting-loop 출력 후처리
```
> "이 리라이팅 결과에서 AI 티 좀 빼줘"
→ PHASE 1: 4-Layer Scan → Diagnostic Report
→ PHASE 2: 4-Layer Naturalization → Naturalized Draft
→ Verification → Final Output
```

### Example 2: 특정 Layer만 교정
```
> "어휘만 자연화해줘, 구문은 괜찮아"
→ PHASE 1: 전체 Scan (진단은 전체)
→ PHASE 2: Layer 1만 실행
```

### Example 3: 직접 작성한 초고 점검
```
> "내가 쓴 Discussion인데 AI 탐지기에 걸릴 수 있는 부분 체크해줘"
→ PHASE 1: 4-Layer Scan → Diagnostic Report만 출력
→ 사용자가 교정 여부 결정
```

### Example 4: Deep 강도
```
> "최대한 자연스럽게 해줘"
→ Intensity: Deep
→ 모든 이슈 교정 + burstiness 적극 주입 + discourse markers 보강
```

---

## References

| File | Read when | Content |
|------|-----------|---------|
| `references/ai-lexicon.md` | PHASE 1 | AI 과잉 어휘 목록, 공기 패턴, 모델별 시그니처, 대체어 |
| `references/naturalization-guide.md` | PHASE 2 | 4계층 자연화 규칙, 체크리스트, 예시 |
| `references/output-formats.md` | 전체 | Diagnostic Card, Changelog, Verification 출력 형식 |

---

**Version**: 1.0.0
**Skill by**: KEI / meta-rewriting-antiai
