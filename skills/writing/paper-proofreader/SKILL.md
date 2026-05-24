---
name: paper-proofreader
description: >
  논문 교정 워크플로우 스킬. 섹션별로 나뉜 논문 폴더를 읽어 단락(paragraph) 단위로 맥락·흐름을
  분석하고, 문장(sentence) 단위로 논리·문체·레퍼런스를 병렬 에이전트로 검토하며, 각 단계마다
  사용자 승인을 받아 진행한다. 사용자가 "논문 교정", "논문 검토", "paper proofreading", "교정 시작",
  "proofread my paper", 특정 섹션(Introduction, Methods, Discussion 등) 교정을 요청할 때
  반드시 이 스킬을 사용한다. 논문 원고를 문장/단락 단위로 정밀 검토하고 싶을 때,
  학술 영어 품질을 개선하고 싶을 때, 레퍼런스 존재 여부를 확인하고 싶을 때도 이 스킬을 사용한다.
---

# Paper Proofreader — 다중 에이전트 논문 교정 워크플로우

## 환경 전제
- **실행 환경:** Claude Code CLI (터미널)
- **출력 방식:** Markdown 서식 (헤더, 볼드, 테이블, 코드블록, 구분선)
- **사용자 입력:** 자연어 — 번호 입력 불필요, 말로 승인/지시
- **번역:** 영어 원문 바로 아래 한국어 번역 항상 표시

## Writing Manual 위치
스킬 디렉토리 내 `writing-manual/` 디렉토리에 있다. 파일을 읽을 때 절대경로를 사용한다:
```
BASE = C:/Users/KEI/.claude/skills/paper-proofreader/writing-manual
```

파일 맵:
```
writing-manual/
├── INDEX.md                          ← 라우팅 테이블
├── sections/
│   ├── 01_abstract.md
│   ├── 02_introduction.md
│   ├── 03_methods.md
│   ├── 04_results.md
│   ├── 05_results_discussion.md
│   ├── 06_discussion.md
│   └── 07_conclusion.md
└── cross_section/
    ├── cohesion_flow.md
    ├── sentence_craft.md
    ├── stance_hedging.md
    └── advanced_nns_issues.md
```

---

## 출력 서식 규칙

모든 출력은 markdown을 기본으로 사용하되, 원문과 번역은 인라인 코드블록으로 시각 구분한다.

### 원문·번역 표시 서식
원문과 번역 모두 인라인 코드블록으로 표시하고 레이블로 구분한다:

**단락 레이어 — 전체 단락 표시:**

**[EN]** `[단락 원문 전체]`

**[KR]** `[한국어 번역]`

**문장 레이어 — 현재 문장 표시:**

**[EN]** `[현재 문장 원문]`

**[KR]** `[한국어 번역]`

**이전 문장/단락 (컨텍스트):**
이전 문장은 레이블 없이 이탤릭으로 간결하게 표시:

*prev:* [이전 문장 요약 또는 전문]

### 쉬운 설명 규칙 (필수)
각 Agent 테이블 바로 아래에, ISSUE가 있으면 쉬운 한국어 설명을 붙인다.
레이블 없이 바로 코드블록으로 설명한다:

#### Agent A1 — 논리·흐름
| 항목 | 결과 |
(테이블)
`[이 문장을 읽으면... 식의 쉬운 설명]`

#### Agent A2 — 문체·언어
| 항목 | 결과 |
(테이블)
`[이 문장을 읽으면... 식의 쉬운 설명]`

- ISSUE가 NONE인 Agent는 쉬운 설명을 생략한다
- Agent P도 동일: 테이블 바로 아래에 설명

SUGGEST가 있으면 쉬운 설명 아래에 수정안 전체 문장을 반드시 표시한다:

**수정안:** `[수정 제안 문장 전체]`

A1과 A2가 각각 다른 수정안을 제시한 경우 둘 다 표시하고, 사용자가 선택하게 한다:

**수정안 (A1):** `[A1 수정 제안 문장 전체]`
**수정안 (A2):** `[A2 수정 제안 문장 전체]`

작성 원칙:
- 전문 용어(Given-New, stress position, nominalization 등)를 쓰지 않는다
- "독자 입장에서 읽으면..." 또는 "이 문장을 읽으면..." 같이 독자 경험 중심으로 설명한다
- 원문의 해당 부분과 수정안을 구체적으로 비교해서 보여준다

### Agent B 레퍼런스 — 단락 완료 후 일괄 실행
Agent B(레퍼런스 확인)는 문장별로 실행하지 않는다.
단락의 모든 문장 검토가 끝난 뒤, 해당 단락에 포함된 모든 citation을 모아서 한꺼번에 병렬 검증한다.
결과는 단락 완료 요약 직후에 레퍼런스 테이블로 출력한다.

### Markdown 서식 (나머지 요소)
- **구조/헤더**: `##` `###` 마크다운 헤더
- **이전 단락/문장**: 간략히 한 줄 요약
- **Agent P 결과**: `#### Agent P — 단락 흐름·수사 분석` 헤더 + 볼드 키
- **Agent A1 결과**: `#### Agent A1 — 논리·흐름` 헤더
- **Agent A2 결과**: `#### Agent A2 — 문체·언어` 헤더
- **Agent B 결과**: `#### Agent B — 레퍼런스` 헤더 (단락 완료 후)
- **문제/경고**: `**[ISSUE]**` 볼드
- **확인/OK**: `[OK]` 또는 체크 표시
- **구분선**: `---` 마크다운 수평선
- **진행도**: `[N/전체]` 텍스트 + 백분율

---

## 에이전트 구성

| 에이전트 | 역할 | 참조 파일 | 실행 방식 |
|---|---|---|---|
| **Agent P** | 섹션 전체 조감도: 단락 구성·순서·연계 논리 분석 | `sections/[해당섹션].md` + `cross_section/stance_hedging.md` + `cross_section/cohesion_flow.md` | 섹션 시작 시 **1회** 실행 |
| **Agent A1** | 문장 논리·argument 구조 | `sections/[해당섹션].md` + `cross_section/cohesion_flow.md` | 문장 레이어에서 병렬 |
| **Agent A2** | 문장 문체·언어 품질 | `cross_section/sentence_craft.md` + `cross_section/advanced_nns_issues.md` | 문장 레이어에서 병렬 |
| **Agent B** | 레퍼런스 존재 확인 | 웹검색 | 문장 레이어에서 병렬 (citation 감지 시) |

---

## Step 0: 초기화

### 0a. writing-manual 로드
스킬 시작 시 반드시 INDEX.md를 Read 도구로 읽는다:
```
C:/Users/KEI/.claude/skills/paper-proofreader/writing-manual/INDEX.md
```
INDEX.md의 라우팅 테이블에서 해당 섹션에 필요한 파일 목록을 확인한다.
섹션이 확정되면 해당 섹션 파일과 cross_section 파일들을 Read 도구로 추가 로드한다.

### 0b. 세션 정보 수집
자연어로 필요한 정보를 묻는다:
- 논문 폴더/파일 경로
- 시작할 섹션 (없으면 처음부터)
- 인용 스타일 (기본값: ACS)

### 0c. 파일 파싱
Bash 도구로 논문 폴더의 파일 목록을 확인한다:
```bash
ls -1 <논문_폴더>
```
파일명에서 섹션 순서 추론. 각 파일을 Read 도구로 읽어 `\n\n` 기준으로 단락 분리.

### 0d. 상태 추적
내부적으로 다음 상태를 추적한다:
- current_section: 현재 섹션명
- current_para_idx: 현재 단락 인덱스
- current_sent_idx: 현재 문장 인덱스
- previous_paragraph: 이전 단락 텍스트
- previous_sentence: 이전 문장 텍스트
- total_paras: 전체 단락 수
- corrections: 수정 이력 (layer, idx, original, revised)
- skipped: 스킵된 항목

---

## Step 1: 섹션 조감도 (Agent P — 1회 실행)

섹션 시작 시 Agent P를 **1회** 실행하여 섹션 전체를 조감한다.
Agent P는 개별 단락이 아닌 **섹션 전체의 단락 구성·순서·연계 논리**를 분석한다.

### 1a. 섹션 요약 출력

먼저 섹션의 단락 구조를 사용자에게 보여준다:

```markdown
## [섹션명] — 단락 [전체]개
---

| # | 단락 첫 문장 (요약) | 역할 |
|---|---|---|
| 1 | [첫 문장 요약...] | [도입/사례/종합/전환 등] |
| 2 | [첫 문장 요약...] | [...] |
| ... | ... | ... |
```

### 1b. Agent P 서브에이전트 프롬프트

Agent 도구로 서브에이전트를 생성한다. **섹션 전체 텍스트**를 프롬프트에 포함한다.

```
당신은 학술 논문 수사 구조 전문 분석 에이전트입니다.
아래 writing-manual 기준에 따라 섹션 전체의 단락 구성과 논리 흐름을 분석합니다.

[writing-manual/sections/[섹션].md 내용 삽입]
[writing-manual/cross_section/stance_hedging.md 내용 삽입]
[writing-manual/cross_section/cohesion_flow.md 내용 삽입]

분석 기준:
1. 섹션 전체의 argument arc (논증 흐름) — 단락들이 하나의 이야기를 구성하는가
2. 단락 간 연결 논리 — 각 단락이 다음 단락을 자연스럽게 이끄는가
3. 단락 순서의 적절성 — 더 효과적인 배치가 있는가
4. 누락된 논점 또는 불필요한 반복 — 빠진 단락이나 합쳐야 할 단락이 있는가
5. 해당 섹션의 move structure 준수 (R&D Cycle, CARS 등)
6. 전체적인 stance/hedging 일관성

반드시 아래 형식으로 출력:

SUMMARY: [섹션의 전체 논증을 2-3문장으로 요약]
ARC: [단락 흐름을 화살표로 도식화: 단락1(역할) → 단락2(역할) → ...]
STRENGTHS: [잘 된 점 1-2개]
ISSUES: [문제점 목록, 없으면 NONE]
- [문제1: 어느 단락에서 무슨 문제]
- [문제2: ...]
SUGGEST: [구조 개선 제안, 없으면 NONE]
- [제안1]
- [제안2]
SCORE: [1-10]

섹션: {section_name}
전체 텍스트: """{full_section_text}"""
```

### 1c. Agent P 결과 출력 + 쉬운 설명

```markdown
#### Agent P — 섹션 조감도

**요약:** `[SUMMARY]`

**논증 흐름:** `[ARC]`

**강점:**
- [STRENGTHS]

**문제점:**
- [ISSUES]

`[쉬운 설명]`

**구조 개선 제안:**
- [SUGGEST]

**SCORE:** [점수]/10

---
```

### 1d. 사용자와 논의

Agent P 결과를 바탕으로 사용자와 단락 구성을 논의한다:
- 단락 순서 변경 여부
- 단락 분리/합치기 여부
- 누락된 논점 추가 여부
- 불필요한 반복 제거 여부

사용자가 구조에 동의하면 문장 레이어로 진행한다.

| 사용자 입력 | 처리 |
|---|---|
| "좋아", "동의", "진행" | 구조 확정 → Step 2 문장 레이어 시작 |
| "단락 순서 바꿔줘" | 구조 변경 논의 |
| "이 단락 빼자" / "합치자" | 단락 수정 논의 |
| "다시 분석해줘" | Agent P 재실행 |
| "특정 단락부터 시작" | 지정 단락부터 문장 레이어 시작 |

---

## Step 2: 문장 레이어 (Agent A1 + A2)

### 2a. 문장 분리 규칙
- 기본: `. ` `? ` `! ` 패턴으로 분리
- 예외: `et al.` `Fig.` `vs.` `e.g.` `i.e.` `cf.` `ca.` 뒤는 분리하지 않음
- 괄호 안 `.`도 분리하지 않음

### 2b. 문장 + 번역 표시

```markdown
### 단락 [N] — 문장 [M/전체]
---

*prev:* [이전 문장]

**[EN]** `[현재 문장 원문]`

**[KR]** `[한국어 번역]`

---
```

### 2c. 병렬 에이전트 실행

Agent A1과 A2를 Agent 도구로 **동시에** 호출한다 (하나의 응답에서 두 개의 Agent 도구 호출).
Agent B(레퍼런스)는 문장별로 실행하지 않고, 단락 완료 후 일괄 실행한다.

**Agent A1 — 논리·argument 분석:**
```
당신은 학술 논문 논리 구조 전문 교정 에이전트입니다.
아래 writing-manual 기준으로 문장의 논리적 역할을 분석합니다.

[writing-manual/sections/[섹션].md 관련 부분]
[writing-manual/cross_section/cohesion_flow.md]

분석 기준:
1. 단락 내 이 문장의 rhetorical 역할 (topic/support/conclusion)
2. 앞 문장과의 Given-New 연결
3. 주장-근거 연결의 명확성
4. 섹션별 move 구조에서의 위치 적절성

출력 형식:
ROLE: [문장의 단락 내 역할]
GIVEN_NEW: [Given-New 구조 평가]
ISSUE: [논리 문제, 없으면 NONE]
SUGGEST: [수정 제안 문장, 없으면 NONE]

섹션: {section_name}
단락: """{paragraph}"""
이전 문장: """{prev_sentence}"""
현재 문장: """{current_sentence}"""
```

**Agent A2 — 문체·언어 분석:**
```
당신은 학술 영어 문체 전문 교정 에이전트입니다.
아래 writing-manual 기준으로 문장의 언어 품질을 분석합니다.

[writing-manual/cross_section/sentence_craft.md]
[writing-manual/cross_section/advanced_nns_issues.md]
[writing-manual/cross_section/stance_hedging.md 중 hedging 부분]

분석 기준:
1. Nominalization 과다 사용 여부
2. Subject-verb 거리
3. End-weight 원칙
4. Active/Passive voice 선택의 적절성
5. 시제 적절성
6. Hedge/Booster 강도와 증거 수준의 일치
7. Collocation 오류, Register 불일치

출력 형식:
STYLE: [문체 평가 — 1문장]
ISSUE: [발견된 문체 문제, 없으면 NONE]
SUGGEST: [수정 제안 문장, 없으면 NONE]

섹션: {section_name}
현재 문장: """{current_sentence}"""
인용 스타일: {citation_style}
```

**Agent B — 레퍼런스 존재 확인:**

Agent B는 문장 레이어에서 실행하지 않는다. Step 4(단락 완료)에서 일괄 실행한다.
상세 프로세스는 Step 4 참조.

### 2d. 결과 출력 (쉬운 설명 + 수정안 포함)

```markdown
#### Agent A1 — 논리·흐름

| 항목 | 결과 |
|---|---|
| **ROLE** | [결과] |
| **GIVEN_NEW** | [결과] |
| **ISSUE** | [문제 또는 없음] |

`[ISSUE가 있으면 쉬운 한국어 설명]`

**수정안 (A1):** `[수정 제안 문장 전체, 없으면 생략]`

#### Agent A2 — 문체·언어

| 항목 | 결과 |
|---|---|
| **STYLE** | [결과] |
| **ISSUE** | [문제 또는 없음] |

`[ISSUE가 있으면 쉬운 한국어 설명]`

**수정안 (A2):** `[수정 제안 문장 전체, 없으면 생략]`

---
*"다음" / "수정 적용해줘" / "A1 적용" / "A2 적용" / "건너뛰어" / "A1 자세히" / "A2 자세히"*
```

- ISSUE가 NONE이면 쉬운 설명과 수정안 모두 생략
- A1과 A2 수정안이 다르면 둘 다 표시, 사용자가 선택
- 수정안이 하나뿐이면 "수정 적용해줘"로 바로 적용

### 2e. 자연어 승인 처리

| 사용자 입력 | 처리 |
|---|---|
| "다음", "ok", "괜찮아" | 승인 -> 다음 문장 |
| "수정 적용해줘" | SUGGEST 문장으로 교체 후 다음 (수정안이 하나일 때) |
| "A1 적용" | Agent A1 수정안으로 교체 후 다음 |
| "A2 적용" | Agent A2 수정안으로 교체 후 다음 |
| "직접 수정할게" | 수정 내용 입력받아 저장 |
| "A1 자세히", "논리 더" | Agent A1 상세 분석 추가 요청 |
| "A2 자세히", "문체 더" | Agent A2 상세 분석 추가 요청 |
| "건너뛰어" | 다음 문장으로 skip |
| "이 단락 다시" | 단락 처음으로 돌아가기 |
| "오늘 여기까지" | 세션 저장 후 종료 |

---

## Step 3: 단락 완료 전환

모든 문장 검토 완료 시:

```markdown
---
### 단락 [N] 검토 완료
- 수정: [X]건
- 승인: [Y]건
- 스킵: [Z]건
---
```

### 3a. Agent B 레퍼런스 일괄 확인

단락 완료 직후, 해당 단락에 포함된 모든 citation을 수집하여 Agent B를 병렬 실행한다.
이미 이 세션에서 확인된 citation은 캐시 사용, 재검색 생략.

각 citation마다 Agent 도구로 웹검색 서브에이전트를 생성:
```
아래 학술 인용의 실제 존재 여부를 웹검색으로 확인하라.

검색 쿼리: "[First Author] [Year] [문장의 핵심 키워드 1-2개]"

출력 형식:
REF: [인용 표기]
STATUS: FOUND / NOT_FOUND
TITLE: [확인된 논문 제목] 또는 —
DOI: [DOI] 또는 —
NOTE: [불일치 사항 또는 —]
```

결과를 테이블로 출력:

```markdown
#### Agent B — 레퍼런스 확인

| REF | STATUS | TITLE | DOI |
|---|---|---|---|
| Prest (2007) | FOUND | "The Bald Hills Wind Farm Debacle" | — |
| Broadbent et al. (2019) | FOUND | "Refusal of planning consent..." | 10.1016/... |
```

NOT_FOUND인 항목이 있으면 경고:
```markdown
**[REF 미확인]** `[인용 표기] — 수동 확인 필요`
```

```markdown
---
*"다음 단락" / "이 단락 다시" / "요약 보여줘"*
```

### 3b. 테이블·그림 처리
논문 원고에 테이블(Table)이나 그림(Figure) 참조가 포함된 경우:
- 테이블 내용 자체는 교정 대상이 아님 (스킵)
- 테이블 캡션(제목)은 문장으로 취급하여 검토
- 테이블 직후 이어지는 본문 단락은 정상 검토

---

## Step 4: 섹션 완료 / 세션 요약

모든 단락 또는 세션 종료 시:

```markdown
---
## 교정 세션 요약

| 항목 | 값 |
|---|---|
| 섹션 | [섹션명] |
| 검토 단락 | [N]개 |
| 검토 문장 | [M]개 |
| 승인 (무수정) | [X]개 |
| 수정 적용 | [Y]개 |
| 스킵 | [Z]개 |
| 레퍼런스 미확인 | [W]개 |

### 수정 이력

| # | 원문 | 수정문 |
|---|---|---|
| 1 | [원문] | [수정문] |
| 2 | ... | ... |

---
```

---

## 주의사항

### writing-manual 참조
- 섹션 판별 우선순위: 파일명 -> 사용자 명시 -> 내용 추론
- 섹션별 로드 파일은 INDEX.md의 라우팅 테이블을 따른다
- 매뉴얼 내용은 각 Agent 서브에이전트 프롬프트에 직접 삽입한다
- 매뉴얼 파일 경로 (Read 도구 사용):
  - `C:/Users/KEI/.claude/skills/paper-proofreader/writing-manual/INDEX.md`
  - `C:/Users/KEI/.claude/skills/paper-proofreader/writing-manual/sections/[파일명]`
  - `C:/Users/KEI/.claude/skills/paper-proofreader/writing-manual/cross_section/[파일명]`

### 번역 품질
- 번역은 직역이 아닌 **학술 한국어**로
- 전문 용어는 영어 병기: "토양 유기 탄소(SOC)"
- 번역이 길면 핵심만 요약 번역 허용

### Agent B 트리거 조건
- `(저자, 연도)` 또는 `저자 et al. (연도)` 또는 `[숫자]` 패턴
- 같은 citation이 이미 이 세션에서 확인된 경우 캐시 사용, 재검색 생략

### 에러 처리
- Agent 서브에이전트 실패: 1회 재시도 -> 실패 시 "**[에이전트 응답 없음 — 수동 검토 필요]**" 출력
- 웹검색 실패: "**[검색 불가 — 수동 확인 필요]**" 출력
- 파일 인코딩 오류: UTF-8 -> EUC-KR 순서로 시도

### 세션 저장
"오늘 여기까지", "저장해줘" 입력 시:
- 현재 파일, 단락 번호, 문장 번호를 메모리 디렉토리에 저장
- 저장 경로: `~/.claude/projects/Z--KKH-Knowledge-Sci-editor/memory/proofreader-session.json`
- 다음 세션 시작 시 "이어서 할까요?" 제안
