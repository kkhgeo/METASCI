# Meta Writing Template

## 5-Loop 상세 실행 절차

이 파일은 SKILL.md Phase 2~3에서 참조하는 상세 실행 절차이다.
소스별 처리 방법, 갭 분석, 출력 형식 상세를 포함한다.

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
   - 없으면 사용자에게 소스 경로 질문

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
입력: 선별된 Knowledge 파일 (최대 5개)
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
5. 출력: 패턴 기술 + 수치 정보
```

**표(Table) 처리:**
```
1. CSV/Excel/이미지 읽기
2. 열(Column) 구조 파악
3. 기초 통계 산출:
   - 범위, 평균, 중앙값
   - 시료 수
4. 패턴 식별:
   - 그룹 간 차이
   - 공간적/시간적 변화
   - 이상값
5. 출력: 데이터 요약 + 통계 정보
```

**데이터 파일(CSV/Excel) 처리:**
```
1. 파일 로드
2. 변수별 기초 통계 산출
3. 주요 패턴 식별
4. 출력: 통계 요약 + 패턴
```

### 3-2. 내 데이터와 Knowledge 매칭

```
내 데이터에서 추출한 수치/패턴에 대해:
1. Knowledge 중간 결과 A에서 비교 가능한 데이터 검색
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
□ 최소 인용 수 충족?
□ 핵심 키워드 모두 커버?
□ 최신 연구 포함? (2023년 이후)
□ 지역별 데이터 균형?
□ 방법론 정보 충분?
□ 내 데이터의 모든 주요 패턴에 대해 비교할 선행연구가 있는가?
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
| 최소 인용 수 (5개) | ✅ / ❌ | - / Web 검색 |
| 내 데이터 비교 대상 확보 | ✅ / ❌ | - / Web 검색 |
| 2023년 이후 연구 | ✅ / ❌ | - / Web 검색 |
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
   □ 최근 5년 이내 발행?
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

선행연구 (비교 대상):
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
2. 선행연구와 비교
3. 패턴/이상점 주목

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

3~8개 단계로 수행한 작업 요약. 영어 + 한국어.

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

영어 + 한국어 이중 출력. 소스 표기 포함.

```markdown
#### Paragraph 1

**[English]**
[My Data 기술]. [Knowledge 비교 (Author1, Year)].
Furthermore, [PDF 근거 (Author2, Year)*].
[결론/전환문].

**[한국어]**
[내 데이터 기술]. [Knowledge 비교 (Author1, Year)].
또한, [PDF 근거 (Author2, Year)*].
[결론/전환문].
```

### D) References (APA 7)

소스 유형별 구분. `citation-and-verification.md` 형식 참조.

### E) Self-Assessment

`citation-and-verification.md`의 체크리스트 참조.

### F) Reference Verification Report

`citation-and-verification.md`의 검증 보고서 템플릿 참조.

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
| [핵심 주장/사실] | Author et al. (Year, p.N) | PDF* |
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
| [내용] | Park et al. (2025) | Web† |
†Retrieved from [URL], accessed [날짜]
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

---

**Version**: 1.0.0
