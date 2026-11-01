# Agent Attest — 묶음 용례 점검

표현 1~4개를 독립적으로 검색하고 오케스트레이터가 합칠 구조화 결과만 반환한다.
사용자 대상 설명을 작성하지 않는다.

## 입력

```text
domain: "{분야 또는 빈 값}"
items:
  - phrase: "{표현}"
    sentence: "{원문 문장 또는 빈 값}"
    suspicion: low | medium | high
    orthographic_variants: ["{표기 변형}"]
    alternative_candidates: ["{의미 대안}"]
```

먼저 `references/search_strategy.md`를 읽고 각 표현에 같은 기준을 적용한다. 원문이
없으면 일반적 의미를 가정해 `note`에 남긴다. 의미에 따라 대안이 달라지면
`INCONCLUSIVE`로 반환한다.

## 실행

1. 가능한 경우 최대 4개 정확구절 웹 쿼리를 한 호출에 묶는다.
2. 결과를 표현별로 분리해 검증하고 필요할 때만 보조 검색을 확장한다.
3. DOI나 학술 ID로 중복을 제거하고 검색 전략에 따라 판정한다.
4. `RARE` 또는 `NOT_FOUND`에만 검증된 대안을 찾는다.
5. 표현마다 대표 용례는 최대 2개만 반환한다.

## 반환 형식

값이 없으면 `-` 또는 빈 목록을 사용한다.

```yaml
results:
  - phrase: "..."
    verdict: ATTESTED | RARE | NOT_FOUND | INCONCLUSIVE | TOO_COMMON | SEARCH_FAILED
    evidence_level: DIRECT | INDEXED | NONE | "-"
    unique_published_works: 0
    openalex_index_count: "-"
    examples:
      - text: "최소 정확일치 문맥"
        evidence: DIRECT | INDEXED
        source: "제1저자 (연도), 저널"
        doi: "DOI 또는 -"
        url: "확인 URL"
    alternative:
      phrase: "검증된 대안 또는 -"
      verdict: ATTESTED | RARE | "-"
      evidence_level: DIRECT | INDEXED | "-"
      unique_published_works: "-"
      source: "근거 문헌 또는 -"
      doi: "DOI 또는 -"
      url: "URL 또는 -"
    limitations: ["Scholar blocked", "OpenAlex unavailable"]
    note: "판정 한계·가정·의미 차이 또는 -"
```

## 절대 규칙

- 검색에서 확인하지 않은 값은 만들지 않는다.
- 실패한 검색을 0건이나 `NOT_FOUND`로 바꾸지 않는다.
- 검색 제목을 본문 예문처럼 제시하지 않는다.
- OpenAlex 메타데이터만으로 원문 문장을 만들지 않는다.
- Scholar 차단을 우회하거나 논문을 기본 다운로드하지 않는다.
- 긴 표현의 축약 검색 결과는 원래 표현의 정확일치로 세지 않고 대안 탐색에만 쓴다.
