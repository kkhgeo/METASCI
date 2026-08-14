---
name: meta-proofreading-evidence
description: >
  Check whether distinctive English academic phrases and collocations are
  attested in published literature, with traceable examples and verified
  alternatives. Use for "용례 확인", "이 표현 실제 논문에 쓰였어?", "표현 검증",
  "phrase check", or "is this used in papers". Do not use for generic
  proofreading, argument or style review, reference verification, or rewriting.
---

# Meta-Proofreading-Evidence

학술 영어 표현의 실제 출판 용례만 점검한다. 문법·논리·문체 전체를 교정하지 않는다.
사용자 대상 판정은 한국어로 쓰고 영어 표현과 용례는 원문으로 병기한다.

## 필요한 파일만 읽기

- 사용자가 문장·단락을 주고 표현 선정을 맡긴 경우에만
  [references/phrase_extraction.md](references/phrase_extraction.md)를 읽는다.
- 실제 검색과 판정 전에는
  [references/search_strategy.md](references/search_strategy.md)를 한 번 읽고 끝까지 따른다.
- 작업을 위임할 때만 [agents/agent_attest.md](agents/agent_attest.md)를 읽고 사용한다.

## 입력 처리

- 사용자가 표현을 지정하면 그대로 점검하고 표현 추출을 생략한다.
- 문장·단락이면 점검 가치가 높은 표현을 고른다. 4개 이상이거나 경계가 모호할
  때만 목록을 먼저 보여준다.
- `.md`/`.txt`는 직접 읽고, `.docx`/`.pdf`는 사용 가능한 문서 도구로 텍스트를
  추출한다. 폴더는 파일 순서와 시작 위치를 확인한다.
- 문맥이 없으면 가장 일반적인 의미를 가정해 밝힌다. 의미에 따라 대안이 달라질
  때만 짧게 문맥을 요청한다.

## 실행

1. 표현별로 원문 문장, 분야, 표기 변형, 의미 대안 후보를 준비한다.
2. 검색 전략의 웹 우선·무다운로드·중복 제거·증거·판정 규칙을 적용한다.
3. 같은 정규화 표현은 세션 내 결과를 재사용한다.
4. 표현이 1~4개면 오케스트레이터가 직접 처리한다.
5. 표현이 5개 이상이고 병렬 작업이 허용되면 사용 가능한 슬롯 수에 맞춰 2~4개씩
   묶어 위임한다. 슬롯을 초과해 에이전트를 만들지 않는다. 병렬 작업이 불가능하면
   순차 처리한다.
6. 결과를 합치고 출처와 DOI 기준으로 다시 중복을 확인한다.

## 기본 출력

먼저 전체 결과를 한 표로 제시한다.

```markdown
| # | 표현 | 판정 | 증거 | 고유 논문 | 대표 근거·대안 |
|---|---|---|---|---:|---|
```

- `ATTESTED`: 표에 대표 출처 1개만 연결한다.
- `RARE`, `NOT_FOUND`, `INCONCLUSIVE`, `SEARCH_FAILED`: 표 아래에 판단 한두 문장,
  필요한 최소 용례, 검증된 대안을 덧붙인다.
- 검색 백엔드 상태는 차단·실패·판정 한계가 있을 때만 표시한다.
- OpenAlex 건수는 판정에 필요하거나 사용자가 물을 때만 표시한다.
- 실제 용례는 최소 문맥만 인용하고 DOI 또는 확인 URL을 붙인다. 제목을 본문
  예문처럼 제시하지 않는다.
- 사용자가 `N번 자세히`라고 하면 해당 표현의 검색 범위, 추가 용례, 비출판 일치,
  대안 근거를 확장한다.

## 파일·폴더 모드

한 응답에서 한 단락만 처리하고 `다음 단락` 전에는 넘어가지 않는다. `대안 반영`,
`N번 자세히`, `섹션 건너뛰기`, `종료`를 지원한다. 표·그림 본문은 제외하고 캡션은
문장으로 처리한다. 종료 시 범위, 판정별 개수, 반영한 대안만 요약한다.

## 절대 규칙

- 검색에서 확인하지 않은 문장·출처·저자·연도·저널·DOI·건수를 만들지 않는다.
- 검색 실패, 접근 차단, 결과 없음, 원문 미확인을 구분한다.
- 보조 API 실패를 `NOT_FOUND` 근거로 사용하지 않는다.
- 대안도 실제 용례와 의미 보존을 확인한 뒤 제시한다.
- 논문을 기본적으로 다운로드하지 않는다.
