# Citation & Verification Guide

## 1. 소스별 인용 표기

### 1.1 소스 유형 분류

본 스킬에서 다루는 소스는 **두 계층**으로 구분된다.

**My Data (본 연구)** — 인용 없이 직접 기술
- 내 그림, 표, 데이터 파일
- "Figure 1에 제시하였다", "Table 2에 요약하였다"
- 절대로 (Author, Year) 형태로 인용하지 않는다

**Knowledge Sources (선행연구)** — 반드시 인용 표기
- Knowledge 마크다운: `(Chen et al., 2024)`
- PDF 직접 읽기: `(Kim et al., 2023)*`
- Web 검색: `(Park et al., 2025)†`

### 1.2 In-text Citation 형식

```
Knowledge 기반 (기본):
(Chen et al., 2024)
Chen et al. (2024) reported that...

PDF 직접 읽기 (별표):
(Kim et al., 2023)*
*PDF에서 직접 추출

Web 검색 (단검표):
(Park et al., 2025)†
†Retrieved from [URL], accessed [날짜]
```

### 1.3 복수 인용

```
시간순 정렬:
(Clark & Fritz, 1997; Kim et al., 2023; Chen et al., 2024)

같은 저자 복수:
(Chen et al., 2023, 2024)

et al. 규칙:
- 저자 1-2명: 모두 표기 (Chen & Lee, 2024)
- 저자 3명 이상: 첫 저자 + et al. (Chen et al., 2024)
```

---

## 2. Reference List 형식 (APA 7)

### 2.1 소스별 구분 출력

```markdown
## References

### From Knowledge Base
Author, A., Author, B., & Author, C. (Year). Title of article.
    *Journal Name*, Volume, Pages.
    https://doi.org/10.xxxx/xxxxx

### From PDF (Direct Reading)
*Author, D., Author, E., & Author, F. (Year). Title of article.
    *Journal Name*, Volume, Pages.
    https://doi.org/10.xxxx/xxxxx

### From Web Search
†Park, E., et al. (2025). Title of article. *Journal Name*.
    Retrieved from https://example.com/article, accessed 2025-02-03.
```

### 2.2 필수 필드

| 필드 | 형식 | 예시 |
|------|------|------|
| Authors | Last, F. M. | Chen, A., Lee, B., & Park, C. |
| Year | (Year). | (2024). |
| Title | 문장체, 이탤릭 아님 | Title of the article. |
| Journal | *이탤릭* | *Geochimica et Cosmochimica Acta* |
| Volume | 이탤릭 | *350* |
| Pages | 숫자-숫자 | 120-135 |
| DOI | https://doi.org/... | https://doi.org/10.1016/... |

누락 필드는 `[missing: field]`로 표기한다. 절대 조작하지 않는다.

---

## 3. 검증 절차 (Phase 4)

글쓰기 완료 후 반드시 아래 4단계 검증을 수행한다.

### Step 1: 인용-참고문헌 매칭 검증

```
작업:
1. 본문에서 모든 (Author, Year) 패턴 추출
2. References 섹션의 모든 항목 추출
3. 매칭 확인:
   ✓ 본문 인용 → References에 존재하는가?
   ✓ References 항목 → 본문에서 인용되었는가?
4. 불일치 항목 리스트 생성
```

### Step 2: 참고문헌 형식 검증

```
APA 7 형식 체크:
□ 저자명 형식: Last, F. M.
□ 연도 위치: (Year).
□ 저널명 이탤릭
□ DOI 형식: https://doi.org/...
□ 필수 필드 완비: Authors, Year, Title, Journal, Volume, Pages, DOI
```

### Step 3: 소스별 검증

```
Knowledge 기반: 원본 마크다운 파일과 대조
PDF 기반: 논문 메타데이터 재확인
Web 검색: URL 접근 가능 여부, 접근 날짜 표기 확인
My Data: 그림/표 번호와 본문 참조가 일치하는지 확인
```

### Step 4: 검증 보고서 생성

```markdown
## Reference Verification Report

### Summary
- **총 본문 인용 수**: N개
- **총 참고문헌 수**: N개
- **내 데이터 참조 수**: Figure N개, Table N개
- **매칭 성공**: N개 (100%)
- **검증 상태**: ✅ PASS / ⚠️ ISSUES FOUND

### Citation-Reference Matching

| 상태 | 인용 | 참고문헌 |
|------|------|----------|
| ✅ | (Chen et al., 2024) | Chen, A., et al. (2024). Title... |
| ❌ Missing | (Park et al., 2022) | [NOT FOUND IN REFERENCES] |
| ⚠️ Orphan | - | Lee, C., et al. (2021). [NOT CITED] |

### My Data Reference Check

| 상태 | 본문 참조 | 파일 |
|------|----------|------|
| ✅ | Figure 1 | fig1_isotope_scatter.png |
| ❌ | Figure 3 | [FILE NOT FOUND] |

### Format Validation

| 참고문헌 | APA 7 | 누락 필드 |
|----------|-------|-----------|
| Chen et al. (2024) | ✅ | - |
| Kim et al. (2023) | ⚠️ | [missing: DOI] |

### Source Verification

| 소스 유형 | 항목 수 | 검증됨 | 미검증 |
|-----------|---------|--------|--------|
| Knowledge | 5 | 5 | 0 |
| PDF | 2 | 2 | 0 |
| Web | 1 | 1 | 0 |

### Issues to Fix
1. ❌ (Park et al., 2022) - References에 추가 필요
2. ⚠️ Kim et al. (2023) - DOI 추가 필요

### Quality Score
**[8/10]** - 2개 항목 수정 필요
```

---

## 4. Self-Assessment Checklist

글쓰기 + 검증 완료 후 최종 품질 점검:

**English:**
- [ ] All in-text citations have matching references
- [ ] No orphan references (all refs cited in text)
- [ ] Reference format validated (APA 7)
- [ ] No missing fields in references
- [ ] My Data references (Figure/Table) match actual files
- [ ] Source types clearly marked (Knowledge / PDF* / Web†)
- [ ] Web search results verified for reliability
- [ ] No fabricated DOIs, URLs, years, or authors

**한국어:**
- [ ] 모든 본문 인용이 참고문헌에 존재
- [ ] 고아 참고문헌 없음
- [ ] 참고문헌 형식 검증됨 (APA 7)
- [ ] 참고문헌에 누락 필드 없음
- [ ] 내 데이터 참조(Figure/Table)가 실제 파일과 일치
- [ ] 소스 유형별 명확히 표기
- [ ] Web 검색 결과 신뢰성 확인
- [ ] DOI/URL/연도/저자 조작 없음

---

## 5. 자동 수정 규칙

검증 후 발견된 문제 처리:

| 문제 | 자동 수정 | 사용자 확인 필요 |
|------|----------|-----------------|
| 누락된 참고문헌 | 원본 소스에서 메타데이터 재추출하여 추가 | ❌ |
| 고아 참고문헌 | - | ✅ 삭제 또는 인용 추가 제안 |
| APA 7 형식 오류 | 자동 재포맷 | ❌ |
| 누락 필드 | 원본에서 재확인 후 보완, 불가 시 [missing] 유지 | ❌ |
| Figure/Table 번호 불일치 | - | ✅ 확인 요청 |

---

**Version**: 1.0.0
