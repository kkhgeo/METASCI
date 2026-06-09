# Citation & Verification Guide

## 1. 소스별 인용 표기

### 1.1 소스 유형 분류

본 스킬에서 다루는 소스는 **두 계층**으로 구분된다.

**My Data (본 연구)** — 인용 없이 직접 기술
- 내 그림, 표, 데이터 파일
- "Figure 1에 제시하였다", "Table 2에 요약하였다"
- 절대로 (Author, Year) 형태로 인용하지 않는다

**Knowledge Sources (선행연구)** — 반드시 인용 표기 (소스 유형과 무관하게 **동일한 APA 7 형식**)
- Knowledge 마크다운: `(Chen et al., 2024)`
- PDF 직접 읽기: `(Kim et al., 2023)`
- Web 검색: `(Park et al., 2025)`

> **소스 유형(Knowledge/PDF/Web)은 본문·References에 표기하지 않는다.**
> APA 7에서 인용 형식은 "어디서 그 문헌을 읽었는지"와 무관하게 동일하다.
> 별표(*)·단검표(†) 같은 출처 구분 기호를 본문에 붙이지 않는다.
> 소스 유형 추적이 필요하면 **내부 검증용으로만** B) Source Summary와
> 검증 보고서(아래 §3)의 표에 기록한다.

### 1.2 In-text Citation 형식

```
모든 소스 동일 형식 (괄호형 / 서술형):
(Chen et al., 2024)
Chen et al. (2024) reported that...
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

### 2.1 단일 통합 목록 (소스 유형 구분 없음)

References는 소스 유형으로 나누지 않고 **저자 알파벳순 단일 목록**으로 작성한다.
(어디서 읽었는지는 References에 드러내지 않는다.)

```markdown
## References

Author, A., Author, B., & Author, C. (Year). Title of the article.
    *Journal Name*, *Volume*(Issue), pages. https://doi.org/10.xxxx/xxxxx

Kim, D., Lee, E., & Park, F. (2023). Title of the article.
    *Journal Name*, *Volume*(Issue), pages. https://doi.org/10.xxxx/xxxxx
```

**온라인 자료(웹) APA 7 형식:**
- DOI가 있으면 DOI만 쓴다 (위 저널 형식과 동일). `Retrieved from`·접근일은 **쓰지 않는다.**
- DOI가 없는 안정적 웹 문서: `Author, A. (Year). Title. *Site or Publisher*. https://example.com/article`
- **수시로 내용이 바뀌는 페이지에 한해서만** 접근일을 명시한다:
  `... Retrieved Month D, Year, from https://...`

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
Web 검색: URL 접근 가능 여부 확인 (접근일은 수시 변경 페이지에만 표기)
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

### Verification Status
**⚠️ ISSUES FOUND** — 2 items to fix (see "Issues to Fix" above)
모든 항목 통과 시: **✅ PASS** — no issues
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
- [ ] In-text citations use one uniform APA 7 form (no * / † source-type markers)
- [ ] Source types tracked internally only (not in manuscript text or References)
- [ ] Web search results verified for reliability
- [ ] No fabricated DOIs, URLs, years, or authors

**한국어:**
- [ ] 모든 본문 인용이 참고문헌에 존재
- [ ] 고아 참고문헌 없음
- [ ] 참고문헌 형식 검증됨 (APA 7)
- [ ] 참고문헌에 누락 필드 없음
- [ ] 내 데이터 참조(Figure/Table)가 실제 파일과 일치
- [ ] 본문 인용이 단일 APA 7 형식 (소스타입 */† 마커 없음)
- [ ] 소스 유형은 내부 검증용으로만 기록 (본문·References 미표기)
- [ ] Web 검색 결과 신뢰성 확인
- [ ] DOI/URL/연도/저자 조작 없음

---

## 5. 검증 후 수정 규칙

**대원칙:** *이미 존재하는 정보의 재포맷*은 자동, *새로운 사실의 추가*는
**검증된 원본(제공된 Knowledge/PDF)이 있을 때만 + 사용자 확인** 후 수행한다.
어떤 경우에도 DOI·URL·연도·저자·페이지를 추론하거나 지어내지 않는다.
이는 §4의 "DOI/URL/연도/저자 조작 없음" 원칙을 강제하기 위함이다.

| 문제 | 처리 | 사용자 확인 |
|------|------|------------|
| APA 7 형식 오류 (기존 정보 재배열) | 자동 재포맷 (새 사실 추가 없음) | 불필요 |
| 누락 필드 | 제공된 원본에 있으면 보완, 없으면 `[missing: field]` 유지 (추측 금지) | 보완 시 ✅ |
| 누락된 참고문헌 | 제공된 원본에 메타데이터가 있을 때만 추가 제안, 없으면 추가하지 않음 | ✅ (필수) |
| 고아 참고문헌 | 자동 삭제 금지 — 삭제/인용 추가 중 선택 요청 | ✅ |
| Figure/Table 번호 불일치 | 자동 변경 금지 — 확인 요청 | ✅ |

> 원본 소스가 없는 정보는 **절대 자동으로 추가하지 않는다.** 검증되지 않은
> 항목은 `[missing]`으로 남기고 사용자에게 보고한다.

---

**Version**: 1.0.1
