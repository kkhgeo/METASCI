# Search Strategy — 표현 용례 검색 (Attestation)

목적: 하나의 표현이 **실제 출판 논문에 쓰였는지**를 판정한다. 문체 패턴 수집이
아니라 **"존재 여부 + 빈도 + 실제 용례 문장"** 확인이 목표다.

메일 파라미터(polite pool / Unpaywall)에는 `kkhgeo@gmail.com`을 쓴다.

---

## 1. 검색 백엔드

> **현실 주의 (실측 2026-07):** OpenAlex·Semantic Scholar 모두 **익명 검색은
> 부하 시 429/503으로 throttle**된다(연결·일반 필터는 정상). 따라서 **정확구절
> 용례 판정의 주력은 하버스의 WebSearch(따옴표 검색)** ①로 두고, OpenAlex
> 전문검색 건수 ②는 **무료 API 키가 있을 때의 정밀 정량화**로 쓴다. 어느 것도
> 못 쓰면 판정은 ①만으로 내리고, ①까지 실패해야 `SEARCH_FAILED`.

### ① Google Scholar / 웹 따옴표 검색 — 주력 (WebSearch 도구)

정확 구절을 따옴표로 감싸 검색 → 색인된 논문 PDF의 정확일치를 잡는다. 하버스
도구라서 위 API throttle의 영향을 받지 않는다. **존재 여부 + 실제 문장 맥락 +
출처**를 이걸로 확보한다 — 사용자의 핵심 질문("실제 논문에 쓰였나")에는 이것만으로
충분하다.
```
WebSearch: "{phrase}"
WebSearch: "{phrase}" (관련 분야 키워드)   # 노이즈 많을 때 좁히기
```
- 정확일치 스니펫이 **학술 출처**(저널/논문 PDF/저자)에서 나오면 → 용례 확인.
- 학술 출처 정확일치가 여럿이면 ATTESTED, 1~2건이면 RARE, 없으면 NOT_FOUND 후보.

### ② OpenAlex 전문 검색 — 정밀 건수 (WebFetch, 키 있으면 신뢰)

OpenAlex는 본문(full text)까지 색인하고 **매칭 건수(`meta.count`)**를 돌려주므로
"얼마나 흔한가"를 정량화할 수 있다. **익명은 자주 503** → 아래 키 사용 권장.

**정확 구절 검색 (따옴표 `%22`, 공백 `%20`):**
```
https://api.openalex.org/works?filter=fulltext.search:%22{phrase}%22&per_page=3&mailto=kkhgeo@gmail.com&select=id,display_name,publication_year,authorships,primary_location,doi
```
- **무료 API 키(권장):** 환경변수 `OPENALEX_API_KEY`가 있으면 `&api_key={KEY}`를
  붙인다. (Bash로 `printf '%s' "$OPENALEX_API_KEY"` 확인. 키 발급:
  https://openalex.org/rest-api) 키가 없으면 호출은 하되 **503이면 조용히 ①로
  대체**하고 `OPENALEX_COUNT`는 `-`로 둔다.

**응답 파싱:** `meta.count`→건수 · `results[].display_name`→제목 ·
`results[].authorships[0].author.display_name`→제1저자 ·
`results[].primary_location.source.display_name`→저널 · `results[].doi`→DOI.

**주의:** `fulltext.search`는 본문 색인분에서 찾고 전체 문헌의 일부만 색인됨 →
**0건은 "색인 코퍼스에서 미확인"**이지 확정 오류가 아니다(§가드레일).

### ③ Semantic Scholar — 메타/대안 보조만 (WebFetch)

```
https://api.semanticscholar.org/graph/v1/paper/search?query={phrase}&limit=5&fields=title,abstract,year,venue,externalIds
```
- **주의:** S2 `total`은 **주제 관련도**지 정확구절 매칭이 아니다(무관 논문도
  카운트됨). **용례 카운터로 쓰지 말 것.** 오직 (a) 초록에 표현이 그대로 있는지
  확인, (b) 대안 표현의 DOI·저널 보강용.
- 익명 429 잦음 → 실패하면 스킵. 인증 불필요, 100 req/5분.

---

## 2. 판정 루브릭 (기본 임계값)

`Q` = 따옴표 웹검색(①)의 **학술 출처 정확일치**, `C` = OpenAlex 전문검색(②)
`meta.count` (**없을 수 있음** — 익명 throttle/키 없음 시 `-`).

**주력은 `Q`.** `C`는 있으면 판정을 보강·정량화하고, 없으면 `Q`만으로 판정한다.

| 판정 | 조건 |
|---|---|
| ✅ **확인 (ATTESTED)** | `Q` 학술 정확일치 다수(≥3 출처), **또는** `C ≥ 10` |
| 🔶 **제한적 (RARE)** | `Q` 학술 정확일치 1~2건, **또는** `1 ≤ C ≤ 9` |
| ⚠️ **미확인 (NOT_FOUND)** | `Q` 정확일치 없음 **그리고** (`C = 0` 또는 `C` 미상) + S2 초록에도 없음 |
| ❓ **검색불가** | 주력 ①(WebSearch)이 실패 (②③ 실패는 검색불가가 아님) |

**과다빈도 예외:** `C`가 수십만 이상으로 지나치게 흔한 기능구
(`in this study`, `these results` 등)는 변별력이 없다 → 판정 대신
"너무 일반적 — 변별 의미 없음"으로 표시, 대안 생략.

임계값은 분야에 따라 조정 가능(소분야는 코퍼스가 작아 `C`가 낮게 나옴).
니치 주제면 확인 임계를 `C ≥ 3`로 낮춰도 된다 — 그 판단을 출력에 명시한다.

---

## 3. 미확인 시 — 대안 검색

표현이 NOT_FOUND면 **뜻은 유지하고 표현만 바꾼** 대안을 찾는다.

1. `phrase_extraction.md`에서 미리 적어둔 `variant_candidates`부터 ①로 검색.
2. 후보가 없거나 다 미확인이면, 표현의 **의미 키워드**로 주제 검색(② 또는 ③)해
   같은 개념을 다루는 논문이 **실제로 쓰는 표현**을 추출.
   예: 의미="서리로 탄소가 방출됨" → 키워드 검색 `freeze thaw carbon release`
   → 실제 논문 문장에서 `frost-induced carbon release` 발견 → 그 표현을 ①로
   재검증(건수 확인) → 대안으로 제시.
3. 대안은 **①로 건수 확인까지 마친, attested된 것만** 제시한다. 확인 안 된
   표현을 대안으로 내지 않는다.

---

## 4. 레이트리밋·에러

| 백엔드 | 한도 | 실패 시 |
|---|---|---|
| WebSearch (①·주력) | 엄격 제한 없음 | 쿼리 수정 재시도 |
| OpenAlex (②) | 익명 검색 throttle 잦음(503) | 키 없으면 조용히 스킵, `C=-` |
| Semantic Scholar (③) | 익명 429 잦음 | 스킵 |

- 표현 1개당 보통 **WebSearch 1 + (가능하면) OpenAlex 1**. `Q`로 확인이 명확하면
  거기서 멈춘다. 미확인일 때만 대안 검색으로 확장.
- **주력 ①(WebSearch)이 실패해야** `검색불가`. ②③ throttle은 정상 흐름의 일부.
- 어떤 경우에도 **결과를 지어내지 않는다.**

---

## 5. 캐시

같은 표현을 세션 내 재점검하지 않도록 판정 결과를 캐시한다
(`session.attest_cache[phrase] = {verdict, count, examples[], alternative}`).
