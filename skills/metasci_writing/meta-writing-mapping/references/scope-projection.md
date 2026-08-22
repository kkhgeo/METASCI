# 범위 투영 규칙 — 전체·섹션·소절·단락군

mapping은 하나의 원고 그래프를 서로 다른 배율로 본다. 범위가 좁아져도 전체
맥락을 잃지 않되 현재 판단에 불필요한 노드는 보여주지 않는다.

## 1. 범위 판별

| 사용자 신호 | 해석 범위 |
|---|---|
| "전체 구성", "논문 구조", 특정 섹션 없음 | manuscript |
| "Discussion을 보자", 섹션 파일 지정 | section |
| "3.4절", "Results 3.4" | subsection |
| "P1–P3", 두 단락 순서, 경계 연결 | paragraph-group |

모호하면 가장 좁은 안전 범위로 시작하고 첫 응답에 해석한 범위를 밝힌다.

```text
현재는 Results 3.4의 P1–P3을 대상으로 보고, 앞 3.3 P3과 뒤 Discussion 4.2 P1을
경계 노드로만 읽겠습니다.
```

## 2. 각 범위에서 읽을 것

### manuscript

Core message, 모든 섹션 기능·순서, 질문 사슬, Methods↔Results,
Results↔Discussion, 전체 근거·Ledger, 활성 blocker·high 결정.

### section

Core message, 해당 섹션 역할, 앞뒤 섹션 경계 노드, 내부 모든 단락, 해당 근거·
Ledger, 상위 blocker와 내부·파급 결정.

### subsection

Core message 한 줄, 상위 섹션 역할 한 줄, 앞 소절 마지막 노드 1개, 대상 소절,
다음 소절 또는 Discussion 첫 연결 노드 1개, 관련 근거·Ledger·결정.

### paragraph-group

Core message 한 줄, 상위 역할 한 줄, 앞 경계 1개, 대상 단락군, 뒤 경계 1개,
관련 근거·Ledger·결정.

경계 노드는 맥락용이며 현재 범위 밖이면 직접 수정하지 않는다.

## 3. 범위 문자열

```text
manuscript
INTRO
RESULTS
RESULTS.3.4
RESULTS.3.4.P1,RESULTS.3.4.P2,RESULTS.3.4.P3
```

prefix 범위는 해당 prefix 노드를 포함하고 쉼표 목록은 정확한 노드 집합이다.

## 4. 경계 노드

선택 노드와 직접 연결된 범위 밖 predecessor·successor를 한 단계만 포함한다.

- 흐리게 표시
- 경계 노드 자체의 low·mechanical 문제는 대기열에서 제외
- 경계 간선이 깨지면 현재 범위 문제로 올림
- 범위 밖 수정이 필요하면 파급 결정 생성

## 5. 상위 blocker

부분 범위를 막는 상위 결정은 함께 보여준다.

```text
D-001 [manuscript blocker] NBL과 ABL의 개념 관계 미확정
D-021 [RESULTS.3.4] Table-S2 first-report 위치
```

관련 없는 다른 섹션 결정은 숨긴다.

## 6. provisional local map

전체 `outline.md`가 없어도 부분 mapping을 수행한다.

```markdown
- 지도 상태: provisional
- 기본 범위: DISCUSSION.4.2
```

알고 있는 범위, 앞에서 보고되었다고 가정한 내용, 뒤에서 회수될 것으로 가정한
내용, 확인할 수 없는 전체 정합을 명시한다. 전체 병합 때 가정과 실제가 충돌하면
관련 결정을 `reopened`로 바꾼다.

## 7. 부분 변경의 영향 전파

1. 영향받는 노드·근거·결정을 찾는다.
2. 기존 결정은 `reopened`로 바꾼다.
3. 없으면 새 결정 ID를 만든다.
4. 대화에는 가장 큰 파급 1–3개만 알린다.
5. 해당 범위를 다시 열 때 대기열에 올린다.

```text
RESULTS.3.4.P2와 P3 순서를 교환했습니다. 이 변경은 DISCUSSION.4.2 해석 순서에
영향을 주므로 D-028을 reopened로 전환했습니다.
```

## 8. 범위 종료와 복귀

부분 범위를 닫을 때 잠근 주장 사슬, 남은 deferred/reopened, 범위 밖 파급,
전체 원고에서 달라진 연결을 한 문단으로 요약한다. 이후 원래 상위 범위의 다음
blocker로 돌아갈 수 있다.
