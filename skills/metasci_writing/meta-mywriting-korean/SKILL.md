---
name: meta-mywriting-korean
description: |
  사용자의 한국어 초고(또는 AI 생성 초고)를 사전 구축된 개인 스타일 Blueprint에 맞춰
  리라이팅하는 스킬. Logic/Tone 추출 데이터 기반 스타일 전이 + 한국어 AI 패턴 제거를
  하나의 파이프라인으로 통합.
  트리거: "내 스타일로 써줘", "내 톤으로 바꿔줘", "내 문체로 고쳐줘",
  "AI 톤 빼줘", "한국어 리라이팅", "내 글투로 맞춰줘",
  "rewrite in my style", "apply my Korean tone".
  **반드시 references/ 파일을 Phase별로 읽을 것!**
allowed-tools: [Read, Write, Edit, Glob, Task, Agent, Grep]
---

> **REQUIRED**: 각 Phase 시작 전 해당 reference 파일을 반드시 읽는다.
> - PHASE 1: `references/my-style-blueprint.md` + `references/korean-anti-ai-patterns.md`
> - PHASE 3–4: `references/output-formats.md`

# Meta-MyWriting-Korean Skill

## Overview

사전 구축된 **나의 한국어 글쓰기 스타일 Blueprint**를 기반으로 초고를 리라이팅하는 스킬.

**기존 meta-rewriting과의 차이:**

| | meta-rewriting | meta-mywriting-korean |
|---|---|---|
| 스타일 소스 | 외부 참조 논문 (매번 추출) | **내 글 데이터 (사전 구축)** |
| 언어 | 영어 중심 | **한국어 전용** |
| Anti-AI | 없음 | **한국어 AI 패턴 제거 내장** |
| 파이프라인 | 5단계 | **4단계** (Blueprint 추출 불필요) |

**핵심 원칙:**
- 내용(주장, 데이터, 인용)은 절대 변경하지 않는다 — 스타일만 변환
- 모든 수정은 Blueprint 데이터에 근거한다 (추상적 조언 금지)
- AI 패턴 제거와 스타일 전이를 동시에 수행한다

---

## Triggers

### Korean
- "내 스타일로 써줘"
- "내 톤으로 바꿔줘"
- "내 문체로 고쳐줘"
- "AI 톤 빼줘" / "AI 느낌 없애줘"
- "한국어 리라이팅"
- "내 글투로 맞춰줘"
- "이 초고 내 스타일로"

### English
- "rewrite in my style"
- "apply my Korean tone"
- "remove AI patterns and match my style"

---

## Pipeline

```
PHASE 1 → Blueprint + Anti-AI 규칙 로드
PHASE 2 → 사용자 초고 수신 + 분석
PHASE 3 → 이중 Gap Analysis (스타일 일치도 + AI 패턴 스캔)
PHASE 4 → 리라이팅 적용 → 출력
```

---

## PHASE 1: Blueprint & Anti-AI 규칙 로드

**반드시 다음 두 파일을 읽는다:**
1. `references/my-style-blueprint.md` — 7차원 스타일 Blueprint
2. `references/korean-anti-ai-patterns.md` — 한국어 AI 패턴 탐지 규칙

### Blueprint 7차원

| # | 차원 | 핵심 내용 |
|---|------|---------|
| 1 | 어조 & 격식 | 격식 해라체, 종결어미 체계, 헤징 수준 |
| 2 | 문장 구조 | 연결어미, 명사화, 복합문 비율 |
| 3 | 논리 흐름 | 단락 기능태그, 인과연결, 열거형 제안 |
| 4 | 전환 표현 | 따라서/그러나/한편/나아가 + 위치 패턴 |
| 5 | 어휘 & 용어 | 정책 레지스터, 한자어 비율, 대체 사전 |
| 6 | 인용 & 근거 | 「법명」인용, 통계, 기관, 각주 |
| 7 | Anti-AI 필터 | AI 패턴 탐지 + 제거 규칙 |

로드 후 즉시 PHASE 2로 전환한다.

---

## PHASE 2: 초고 수신 & 분석

Blueprint 로드 후 다음 프롬프트를 출력하고 대기:

```
---
나의 스타일 Blueprint 로드 완료.

초고를 붙여넣거나 파일 경로를 알려주세요.

  범위: 단락 / 섹션 / 전체 문서
  문서 유형 (선택): 정책 리뷰 / 연구보고서 / 학술논문 / 기타

  모드:
    [A] 문장별 피드백 — 원문 유지, 핀포인트 수정 제안
    [B] 전면 리라이팅 — Blueprint 스타일 전체 적용
---
```

기본 모드(미지정 시): **[A]**

### 초고 수신 시 처리
1. 텍스트 길이 확인 (어절 수)
2. 문서 유형 판별 (명시 또는 자동 감지)
3. 모드 확인 (A/B)
4. PHASE 3으로 진행

---

## PHASE 3: 이중 Gap Analysis

**`references/output-formats.md`를 읽고 출력 형식을 따른다.**

초고를 Blueprint 7차원 + Anti-AI 체크리스트로 이중 진단한다.

### 3a. 스타일 일치도 분석 (Dim 1–6)

각 차원에 대해:
1. 초고의 현재 상태 진단
2. Blueprint 기준과의 차이 식별
3. 1-10 점수 부여
4. 구체적 수정 예시 제시 (Blueprint 데이터에서 인용)

### 3b. AI 패턴 스캔 (Dim 7)

`korean-anti-ai-patterns.md`의 체크리스트로 초고를 스캔:
1. 필러 표현 탐지
2. AI 구조 패턴 탐지
3. AI 선호 어휘 탐지
4. 톤 패턴 탐지
5. 자연스러움 점수 부여 (50점 만점, 높을수록 AI 흔적 적음)

### 점수 해석 & 모드 권장

> 이 표는 `references/output-formats.md`의 모드 표와 **동일**해야 한다. 한쪽만 고치지 말 것.

| 스타일 평균 (Dim 1-6, /10) | 자연스러움 (Dim 7, /50) | 권장 모드 |
|---|---|---|
| 8-10 | 35-50 | Mode A — 미세 수정 (이미 스타일 부합) |
| 8-10 | 35 미만 | Mode A — AI 패턴 제거 중심 |
| 5-7  | 35-50 | Mode A — 스타일 차이 보정 중심 |
| 5-7  | 35 미만 | Mode B — 스타일 + AI 제거 동시 |
| 4 이하 | 무관 | Mode B — 전면 리라이팅 |

**모드 결정 우선순위:**
1. 사용자가 A/B를 **명시적으로 지정**했으면 점수와 무관하게 그 모드로 진행.
2. 미지정 시 위 표의 권장을 따른다. (PHASE 2의 기본값 A는 Gap Analysis 이전 임시값이며, 이 권장이 갱신한다.)

---

## PHASE 4: 리라이팅 적용

**`references/output-formats.md`를 읽고 출력 형식을 따른다.**

### Mode A — 문장별 피드백

초고를 단락 순서대로 처리. 문제 문장마다:

```
[원문]
"원래 문장"

[수정]
"수정된 문장"

[근거]
- [Dim #]: [적용된 Blueprint 규칙 + 참조 예시] (1-2줄)
```

추가 규칙:
- 잘 쓰인 문장은 "✓ 유지" 표시 후 넘어감
- Dim 7 (Anti-AI) 적용 시 "[AI 패턴 제거]" 태그 추가
- Gap Analysis에서 가장 낮은 점수 차원부터 우선 처리

### Mode B — 전면 리라이팅

전체 입력을 리라이팅. 7차원 모두 적용.

**보존 원칙:**
- 모든 주장(argument) 보존
- 모든 데이터 포인트 보존 (수치, 단위)
- 모든 인용(citation) 보존
- 표/그림 참조 번호 유지
- 내용 변경 절대 금지 — 스타일만 변환

리라이팅 후 **변경 요약표** 첨부:

```
| 변경 유형 | 건수 | 예시 |
|----------|------|------|
| 어조 조정 | N | 비격식→격식 해라체 |
| 동사 교체 | N | "보여준다"→"나타난다" |
| 문장 재구성 | N | 단문→"~하여 ~하는" 복합문 |
| 전환어 추가 | N | "따라서", "한편" 삽입 |
| 논리 재배치 | N | 주장→근거→해석 순서 |
| AI 패턴 제거 | N | 필러 삭제, AI 어휘 교체 |
```

### 사후 검증

리라이팅 완료 후 자체 검증:
1. 원문의 모든 주장이 리라이팅에 존재하는가?
2. 모든 인용이 보존되었는가?
3. 데이터 수치가 변경되지 않았는가?
4. 7개 차원이 모두 반영되었는가?
5. 자연스러운 한국어로 읽히는가? (기계적 치환이 아닌가?)
6. AI 패턴이 제거되었는가?

---

## Output Structure

```
Rewrite_내스타일/
├── gap_analysis.md       # 이중 Gap Analysis 결과
├── rewritten_draft.md    # 리라이팅 결과 + 변경 요약
└── session_log.md        # 세션 메타데이터
```

- 사용자가 파일 저장을 원하지 않으면 화면 출력만으로 충분
- 저장 시 `Rewrite_내스타일/` 또는 사용자 지정 폴더

---

## Parallel Processing (Subagent)

### 다중 섹션 동시 리라이팅
```
사용자: "이 3개 섹션 내 스타일로 고쳐줘"
→ 섹션별 Task (Subagent) 생성
→ 동일 Blueprint, 독립 리라이팅
→ 결과 통합 저장
```

---

## Quality Standards

1. **근거 기반**: 모든 수정에 Blueprint 차원 번호 + 실제 예시 문장 인용
2. **내용 보존**: 과학적/정책적 의미 변경 절대 금지
3. **이중 진단**: 스타일 일치도 + AI 패턴 동시 검사
4. **자연스러움**: 기계적 치환이 아닌 자연스러운 한국어 산문
5. **추적 가능**: 모든 수정에 적용 차원 명시
6. **정량 진단**: Gap Analysis에 수치 점수 제공

---

## Error Handling

| 상황 | 대응 |
|------|------|
| 초고가 너무 짧음 (<2문장) | 경고: "단락 이상의 텍스트 권장" |
| 초고가 영어 | 경고: "이 스킬은 한국어 전용. meta-rewriting 사용 권장" |
| 문서 유형 판별 불가 | 사용자에게 확인 요청 |
| 초고가 이미 내 스타일과 매우 유사 (점수 9+) | "이미 잘 맞습니다" + 미세 수정만 제안 |

---

## Usage Examples

### 예시 1: AI 생성 초고 리라이팅
```
> "이 ChatGPT로 쓴 초고를 내 스타일로 바꿔줘"
→ Blueprint 로드 → 초고 수신 → 이중 Gap Analysis → Mode B 리라이팅
```

### 예시 2: 문장별 피드백
```
> "이 단락 내 톤으로 맞춰줘 (Mode A)"
→ Blueprint 로드 → 문장별 [원문/수정/근거] 피드백
```

### 예시 3: AI 톤 제거만
```
> "AI 느낌만 빼줘"
→ Blueprint 로드 → Dim 7 (Anti-AI) 중심 스캔 → 해당 패턴만 수정
```

### 예시 4: 다중 섹션
```
> "서론이랑 결론 둘 다 내 글투로 맞춰줘"
→ 섹션별 Subagent → 동일 Blueprint 기반 병렬 리라이팅
```

---

## Blueprint 업데이트

새 보고서/발간물을 Blueprint에 반영하려면:
1. 논리·스타일 추출 스킬로 새 글을 분석한다.
   - METASCI(원본 저장소): `extraction-logic`, `metasci-style-extraction`
   - 로컬 단독 대안: `logic-extraction`, `style-guide`
2. 추출 결과(logic/style 마크다운)를 분석 폴더에 저장한다.
3. 그 데이터로 `references/my-style-blueprint.md`의 해당 차원
   (규칙·빈도·예문·템플릿)을 갱신한다.

---

## References

| 파일 | 읽는 시점 | 내용 |
|------|---------|------|
| `references/my-style-blueprint.md` | PHASE 1 | 7차원 사전 구축 Blueprint |
| `references/korean-anti-ai-patterns.md` | PHASE 1 | 한국어 AI 패턴 탐지/제거 규칙 |
| `references/output-formats.md` | PHASE 3-4 | Gap Analysis + 리라이팅 출력 형식 |

---

**Version**: 1.0.1
**Skill by**: METASCI / meta-mywriting-korean
