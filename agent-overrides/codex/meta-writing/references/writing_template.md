# Meta Writing Template

## 5-Loop 상세 실행 절차

이 파일은 SKILL.md Phase 2~3에서 참조하는 상세 실행 절차이다.
소스별 처리 방법, 갭 분석, 출력 형식 상세를 포함한다.

## Contents

- Loop 1: Source Scan & Planning
- Loop 2: Knowledge Reading
- Loop 3: My Data Analysis + Additional Sources
- Loop 4: Gap Check + Web Search
- Loop 5: Synthesis & Writing
- 출력 형식 상세
- 소스별 상세 처리 방법
- 에러 처리

---

## Loop 1: Source Scan & Planning

```
목적: 사용 가능한 소스 파악 및 탐색 계획
입력: writing.local.md 설정 또는 사용자 지정 경로
출력: 탐색 계획
```

### 작업 절차

1. **프로젝트 설정 확인**
   - writing.local.md가 있으면 읽고 경로 설정 로드
   - 설정이 요청과 충돌하거나 결과를 실질적으로 바꿀 때만 사용자에게 확인
   - 없으면 요청에 제공된 경로·첨부·붙여넣은 자료를 사용하고, 필요한 자료에 접근할 수 없을 때만 질문

2. **My Data 폴더 확인**
   - figures/ 내 이미지 파일 목록
   - tables/ 내 데이터 파일 목록
   - writing.local.md에 매핑 정보가 있으면 로드
   - 사용자가 지정한 그림/표와 섹션 배치 확인

3. **Knowledge 폴더 확인**
   - index.md 있으면 읽기
   - 관련 파일 목록 추출
   - 파일명과 요청 주제 매칭

4. **PDF 폴더 확인**
   - 파일 목록 스캔
   - 파일명으로 관련성 판단

5. **탐색 계획 수립**
   - 어떤 파일을 어떤 순서로 읽을지
   - My Data 중 분석 대상 확정
   - 예상 소요 루프 수

---

## Loop 2: Knowledge Reading

```
목적: Knowledge 마크다운 파일에서 선행연구 지식 추출
입력: 선별된 Knowledge 파일 (초기 배치 최대 5개, 주장 범위가 미완성하면 추가 탐색)
출력: 중간 결과 A
```

### 작업 절차

1. Knowledge 파일 순차 읽기
2. 요청 섹션/주제 관련 카테고리 추출:
   - Theoretical Foundations (이론적 기반)
   - Empirical Precedents (실증적 선례)
   - Methodological Heritage (방법론적 유산)
   - Contextual Knowledge (맥락 지식)
   - Critical Discourse (비판적 담론)
3. Claim + Citation 쌍으로 저장
4. 소스 표기: [Knowledge]

### 추출 형식

```markdown
| Claim | Citation | Category | Source |
|-------|----------|----------|--------|
| [주요 발견/사실] | Author1 et al. (Year) | Empirical Precedents | Knowledge |
| [방법론 정보] | Author2 et al. (Year) | Methodological Heritage | Knowledge |
```

---

## Loop 3: My Data Analysis + Additional Sources

```
목적: 내 데이터 분석 + 추가 Knowledge/PDF로 보완
입력: My Data 파일 + 추가 Knowledge/PDF 파일
출력: 중간 결과 B
```

### 3-1. 내 데이터 분석

**그림(Figure) 처리:**
```
1. 이미지 파일 읽기 (Claude가 직접 시각 분석)
2. 축 라벨, 단위, 범위 파악
3. 데이터 분포 패턴 식별:
   - 그룹화 여부
   - 추세선/상관관계
   - 이상값 존재 여부
4. 정량적 특성 추출:
   - 값의 범위 (최소~최대)
   - 주요 그룹별 범위
   - 뚜렷한 패턴
5. 수치의 출처 등급 판정:
   - 원자료(CSV/Excel)가 있으면 → 반드시 그것에서 수치를 가져온다 (정확값)
   - 이미지에서만 읽었으면 → 근사값. 본문에 "~" 표기 + 저자 확인 대상으로 표시
   - 축 라벨·단위·범례가 불명확하면 → 추정하지 말고 사용자에게 질문
6. 출력: 패턴 기술 + 수치 정보 (각 수치에 정확/근사 등급 부기)
```

> 이미지에서 눈으로 읽은 값은 추정치다. 검증 단계에서 그림 번호와 파일 존재만 확인하면
> 잘못 읽은 수치가 그대로 통과하므로, 여기서 등급을 남겨야 Phase 4가 잡을 수 있다.

**표(Table) 처리:**
```
1. CSV/Excel/이미지 읽기
2. 열(Column) 구조 파악
3. 사용자가 제공한 통계와 표에 명시된 값을 기록
   - 범위, 평균, 중앙값, 시료 수 등이 이미 제시되었으면 그대로 사용
   - 새 통계 산출은 사용자가 계산을 명시적으로 요청한 경우에만 수행하고 산출식을 기록
4. 패턴 식별:
   - 그룹 간 차이
   - 공간적/시간적 변화
   - 이상값
5. 출력: 데이터 요약 + 통계 정보
```

**데이터 파일(CSV/Excel) 처리:**
```
1. 파일 로드
2. 변수 구조와 사용자가 제공한 분석 결과 확인
3. 계산이 명시적으로 요청된 경우에만 지정 통계를 산출하고 산출식·입력값을 기록
4. 계산 요청이 없으면 새로운 통계를 만들지 않고 제공된 값에서 보이는 패턴만 기술
5. 출력: 제공된 통계 요약 + 패턴 + 요청된 경우에만 계산 기록
```

### 3-2. 내 데이터와 Knowledge 매칭

```
내 데이터에서 추출한 수치/패턴에 대해:
1. Knowledge 중간 결과 A에서 방법·표본·맥락이 비교 가능한 데이터 검색
   - 일치 결과뿐 아니라 불일치, 무효과, 혼합 결과도 포함
2. 비교 쌍 생성:

| 내 데이터 | 선행연구 | 비교 유형 |
|-----------|---------|-----------|
| [변수]: [내 범위/값] | Author1(Year): [선행 범위/값] | 유사/차이/신규 |
| [관찰된 패턴] | Author2(Year): [선행 패턴] | 유사/차이/신규 |
```

### 3-3. 추가 소스 읽기

```
1. 남은 Knowledge 파일 읽기 (있으면)
2. PDF 읽기 필요 여부 판단:
   - Knowledge에서 커버 안 된 주제?
   - 사용자가 특정 PDF 지정?
   - 내 데이터 해석에 필요한 추가 정보?
3. PDF 읽기 (필요시)
   - 관련 섹션에서 정보 추출
   - 소스 표기: [PDF]
4. 중간 결과 B 저장
```

---

## Loop 4: Gap Check + Web Search

```
목적: 지식 갭 식별 + Web 검색으로 보완
입력: 중간 결과 A + B, Web 검색 허용 여부
출력: 중간 결과 C + 갭 보고서
```

### 갭 체크 항목

```
□ 외부 근거가 필요한 모든 주장에 적절한 인용이 있는가?
□ 핵심 키워드 모두 커버?
□ 과업·분야·투고처가 요구하는 최신성 범위를 충족하는가?
□ 지역별 데이터 균형?
□ 방법론 정보 충분?
□ 내 데이터의 주요 패턴에 대해 일치·불일치·무효과를 포함한 비교 가능한 선행연구가 있는가?
□ Discussion에서 해석할 근거가 충분한가?
```

### 갭 분석 보고서 템플릿

```markdown
## 갭 분석 보고서

### 현재 수집된 지식
- Knowledge: N claims from N files
- PDF: N claims from N files
- My Data: Figure N개, Table N개 분석 완료
- Total: N claims

### 갭 체크 결과

| 항목 | 상태 | 조치 |
|------|------|------|
| 주장별 인용 범위 | ✅ / ❌ | - / 추가 탐색 또는 주장 축소 |
| 내 데이터 비교 대상 확보 | ✅ / ❌ | - / Web 검색 |
| 요구된 최신성 범위 | ✅ / ❌ / 해당 없음 | - / Web 검색 |
| 해석 근거 충분 | ✅ / ❌ | - / PDF/Web 검색 |

### Web 검색 계획 (필요시)
- 쿼리: "[주제 키워드]"
- 대상: Google Scholar, ScienceDirect
- 목표: [부족한 정보] 보완
```

### Web 검색 실행 규칙

```
1. 학술 소스 우선 (Google Scholar, 저널 사이트)
2. 검색 쿼리 기록
3. 신뢰성 체크:
   □ 학술 저널/기관 출처?
   □ 저자 정보 확인 가능?
   □ 과업·분야·투고처가 요구하는 최신성 범위에 적합한가?
   □ DOI 또는 영구 URL?
4. 접근 날짜 표기
5. 신뢰할 수 없는 소스 제외
6. 소스 표기: [Web]
```

---

## Loop 5: Synthesis & Writing

```
목적: 모든 소스 종합 + 최종 글쓰기
입력: 중간 결과 A + B + C + My Data 분석 결과
출력: 최종 글
```

### 5-0. 골격 확정 (산문화 이전)

문장을 만들기 전에 단락별 논지를 한 줄씩 확정한다. 이 골격이 Phase 3.5의 판정 기준이 된다.

```
Core message: [이 글이 관철해야 할 단 하나의 주장]

| 단락 | topic sentence (한 줄) | 근거 소스 | Core message 기여 |
|------|----------------------|----------|------------------|
| 1 | [주장] | Figure 1, (Author, Year) | [어떻게 기여하는가] |
| 2 | [주장] | (Author, Year) x2 | [어떻게 기여하는가] |
| 3 | [주장] | Table 1, (Author, Year) | [어떻게 기여하는가] |
```

- Core message 기여를 한 줄로 못 쓰는 단락은 골격 단계에서 뺀다. 쓰고 나서 빼는 것보다 싸다.
- section_guides.md의 섹션별 "구조" 블록은 *일반 템플릿*이다. 이 표는 *이번 원고*의 논지다.
- 근거 소스가 비어 있는 단락이 있으면 Loop 4로 돌아가 보완하거나 범위를 줄인다.

### 5-1. 소스 병합

```
1. Knowledge + PDF + Web 결과 통합 (선행연구)
2. My Data 분석 결과 별도 유지 (본 연구)
3. 중복 제거
4. 소스 유형 태그 유지
```

### 5-2. My Data vs Knowledge 문장 구분 규칙

**Results 섹션에서:**
```
내 데이터 (주어, 기술 대상):
- "본 연구의 [변수] 값은 [범위] 범위를 보였다 (Figure N)."
- "The [variable] values ranged from [X] to [Y] (Figure N)."

분리형 IMRaD에서는 선행연구 비교·원인·기전·함의를 Discussion으로 이동한다.
저널이 Results와 Discussion을 통합하거나 Results 내 비교를 허용할 때만 사실 대조를 쓴다:
- "이는 Author (Year)이 보고한 [범위]와 유사하다."
- "comparable to the range reported by Author (Year)."
```

**Discussion 섹션에서:**
```
내 데이터 (해석 대상):
- "본 연구에서 관찰된 [패턴/현상]은..."
- "The [pattern/phenomenon] observed in this study..."

선행연구 (해석 근거):
- "이는 Author (Year)이 제안한 [이론/모델]로 설명될 수 있다."
- "This can be explained by the [theory/model] proposed by Author (Year)."
```

### 5-3. 정렬 원칙

```
시간순: foundational → recent
지역순: global → regional → local
논리순: Problem → Evidence → Application

Results 내 정렬:
1. 내 데이터 기술 먼저
2. 패턴·관계·이상점 보고
3. `with-comparison`이 허용된 경우에만 선행연구와 사실 대조

Discussion 내 정렬:
1. 주요 발견 요약
2. 메커니즘 해석 (선행연구 근거)
3. 함의 → 한계 → 향후 연구
```

### 5-4. 그림/표 참조 삽입 규칙

```
본문 내 참조:
- "(Figure 1)" 또는 "(Table 1)" — 괄호 안
- "Figure 1에 제시하였다" — 문장 주어로
- "as shown in Figure 1" — 부연

참조 위치:
- 해당 데이터를 처음 언급하는 문장에 삽입
- 같은 그림을 재참조할 때: "(Figure 1)" 반복 가능
- 순서: 본문에서 언급 순서대로 Figure 1, 2, 3...
```

---

## 출력 형식 상세

### A) Approach Checklist (접근법 체크리스트)

3~8개 단계로 수행한 작업을 요청된 언어로 요약한다. `bilingual`이면 영어 뒤에 한국어를 쓴다.

```markdown
**English:**
- [1] Loaded project settings from writing.local.md
- [2] Analyzed Figure N ([그림 설명])
- [3] Read N Knowledge files ([파일명 목록])
- [4] Gap check: [부족 항목] → [보완 방법]
- [5] Synthesized all sources → wrote [섹션명]
- [6] Reference verification → all citations validated

**한국어:**
- [1] writing.local.md에서 프로젝트 설정 로드
- [2] Figure N 분석 ([그림 설명])
- [3] Knowledge 파일 N개 읽기
- [4] 갭 체크: [부족 항목] → [보완 방법]
- [5] 모든 소스 종합 → [섹션명] 작성
- [6] 레퍼런스 검증 → 모든 인용 확인
```

### B) Source Summary (소스 요약)

```markdown
## 사용된 소스

### My Data (본 연구)
| 유형 | 파일 | 섹션 배치 |
|------|------|----------|
| Figure | [파일명] | [섹션] |
| Table | [파일명] | [섹션] |

### Knowledge Sources (선행연구)
| 소스 유형 | 파일/쿼리 | 추출 항목 수 |
|-----------|----------|-------------|
| Knowledge | [파일명 목록] | N claims |
| PDF | [파일명 목록] | N claims |
| Web Search | "[검색 쿼리]" | N claims |

### 갭 보고
- [해결됨/미해결] [항목 설명]
- [보완 방법] [추가된 내용 설명]
```

### C) Main Text (본문)

요청된 언어로 출력한다. `bilingual`이면 영어 뒤에 한국어를 쓴다. 소스 유형은 본문에
표기하지 않고 내부 추적은 B) Source Summary에만 기록한다.

> **AI 생성 초안 — 저자 검증·개작 필요.** 논지 선택과 해석의 타당성, 최종 문장은 저자가
> 결정한다. 소스가 결정해 주지 않는 판단이 들어간 문장에는
> `[interpretation needed — no supporting source]` 또는 `[author judgement]`를 인라인
> 표시해 저자가 어디를 봐야 하는지 드러낸다.

```markdown
#### Paragraph 1

**[English]**
[My Data 기술]. [Knowledge 비교 (Author1, Year)].
Furthermore, [PDF 근거 (Author2, Year)].
[결론/전환문].

**[한국어]**
[내 데이터 기술]. [Knowledge 비교 (Author1, Year)].
또한, [PDF 근거 (Author2, Year)].
[결론/전환문].
```

### D) References (Target-Venue Style; APA 7 Fallback)

투고처가 지정한 형식과 정렬법을 따른다. 투고처가 미확정이거나 형식을 지정하지 않은
경우에만 APA 7의 저자 알파벳순 **단일 통합 목록**을 사용한다.
`citation-and-verification.md` §2 형식 참조.

### E) Self-Assessment

`citation-and-verification.md`의 체크리스트 참조.

### F) Reference Verification Report

`citation-and-verification.md`의 검증 보고서 템플릿 참조.

### G) AI Assistance Log

먼저 현재 투고처·기관의 AI 정책을 확인한다. A) Approach Checklist의 작업 기록을
정책이 요구하는 범위에서 공개용 형식으로 정리하되, 민감한 연구자료나 저작권이 있는
원문 구절을 로그에 그대로 남기지 않는다. 정책을 확인하지 못하면 disclosure를 확정하지
말고 `[venue policy unresolved]`로 표시한다.

```markdown
## G) AI Assistance Log

### 개입 층위
[ ] 기술 지원 — 서식·인용 정리·번역 수준
[x] 텍스트 개발 — 단락 초안 생성
[ ] 전환적 — 해석·논증 구성에 관여
> 층위가 높을수록 저자 검토 부담이 커집니다.

### 수행한 작업
- Knowledge 파일 N개에서 Claim-Citation 추출
- Figure N / Table N 판독 및 기술
- [섹션명] 초안 단락 N개 생성 (영/한)
- 투고처 지정 형식 또는 APA 7 fallback으로 참고문헌 정리
- 인용-참고문헌 매칭 및 Claim-Source 대조 검증

### 수행하지 않은 작업
- 데이터 생성·수정 없음
- 통계 재계산 없음
- 원자료에 없는 수치 산출 없음
- 제공되지 않은 문헌의 인용 생성 없음

### 저자 확인이 필요한 항목
- [근사값으로 표기된 수치 목록]
- [unverified secondary citation 목록]
- [interpretation needed 표시 위치]

### 저널 제출용 disclosure 초안
"During the preparation of this work the author(s) used [tool] to draft and edit
sections of the manuscript based on author-supplied data and literature. The author(s)
reviewed and edited the content and take full responsibility for the content of the
publication."
> 실제 문구는 투고처 정책에 맞춰 저자가 조정하십시오.
> 프롬프트·출력 보존이 요구되더라도 민감정보와 저작권 원문은 적용 가능한 보존 정책에 따라 최소화하십시오.
```

---

## 소스별 상세 처리 방법

### Knowledge 마크다운 처리

```
입력: [Knowledge 마크다운 파일]

추출 대상:
- 지식 추출 섹션의 테이블 (있으면)
- Knowledge Claim / Reference (APA) / Section 열
- 테이블이 없으면 본문에서 핵심 주장 + 인용 쌍 추출

출력:
| Claim | Citation | Source |
|-------|----------|--------|
| [핵심 주장/사실] | Author et al. (Year) | Knowledge |
```

### PDF 논문 처리

```
입력: [PDF 논문 파일]

절차:
1. Abstract + Conclusion 우선 읽기 (핵심 파악)
2. 필요 시 특정 섹션(Methods, Results 등) 추가 읽기
3. 주제 관련 문장 식별
4. 인용 정보 추출 (저자, 연도, 저널)
5. 페이지 번호 기록

출력:
| Claim | Citation | Source |
|-------|----------|--------|
| [핵심 주장/사실] | Author et al. (Year, p.N) | PDF |
```

### Web 검색 처리

```
검색 전략:
1. 학술 키워드로 검색 쿼리 생성
2. Google Scholar, ScienceDirect 등 학술 소스 우선
3. 신뢰성 체크 후 정보 추출

출력:
| Claim | Citation | Source |
|-------|----------|--------|
| [내용] | Park et al. (2025) | Web |

> Source 열은 **내부 추적용**이다. URL은 검증을 위해 따로 기록하되,
> 본문·References 표기 규칙은 `citation-and-verification.md` §2.1을 따른다.
```

---

## 에러 처리

| 상황 | 대응 |
|------|------|
| 모든 소스 없음 | "최소 1개 소스를 제공해 주세요: Knowledge 폴더, PDF 폴더, 또는 Web 검색 허용" |
| My Data 파일 읽기 실패 | 오류 보고 + 사용자에게 파일 확인 요청 |
| Knowledge 부족 + PDF 없음 + Web 불허 | "사용 가능한 소스에서 충분한 근거를 확보하지 못했습니다. Web 검색 허용 또는 추가 자료 제공을 고려해 주세요." |
| Web 검색 실패 | "Web 검색에서 신뢰할 수 있는 학술 소스를 찾지 못했습니다. 기존 자료로 진행합니다." |
| 그림/표 번호와 파일 불일치 | 사용자에게 확인 요청 |
| 그림 축 라벨·단위·범례 판독 불가 | 추정 금지 — 사용자에게 질문 |
| 해석 근거가 될 소스가 없음 | 지어내지 말고 `[interpretation needed — no supporting source]` 표기 후 보고 |
| Knowledge의 인용을 원문에서 확인 불가 | `[unverified secondary citation]` 표기 후 보고 |

---

**Version**: 1.3.0-codex
