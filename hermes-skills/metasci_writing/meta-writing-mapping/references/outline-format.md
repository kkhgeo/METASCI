# outline.md 규격 — 계층형 mapping 1.1

작업 폴더에는 **`outline.md` 하나만** 둔다. 전체·섹션·소절·단락군 mapping은
별도 파일이 아니라 같은 원본의 다른 범위다. `outline-dashboard.html`과 JSON
보고서는 이 파일에서 자동 생성되는 파생물이며 직접 편집하지 않는다.

## 1. 기본 구조

```markdown
# Outline — {원고 제목 또는 가제}

- Core message: {원고 전체가 관철할 단 하나의 주장}
- 원고 언어: English | 한국어
- 포맷 버전: 1.1
- 지도 상태: integrated | provisional
- 기본 범위: manuscript | SECTION | SECTION.3.4 | paragraph-group
- 최종 갱신: YYYY-MM-DD

## 구성
{계층형 단락 노드}

## 근거 인벤토리
{Figure·Table·문헌·자료 ID}

## Ledger 인벤토리
{주장·수치·정의·최초보고 제약 ID}

## 결정 대장
{D-### 상태·추천·영향·이력}

## 근거 노트
{정독 결과 — 자료당 5줄 안쪽}
```

`지도 상태: provisional`은 전체 원고 맥락 없이 부분 mapping부터 시작했음을
뜻한다. 전체 지도에 병합한 뒤 상위 연결을 검증하면 `integrated`로 바꾼다.

## 2. 계층형 ID

모든 단락 ID는 원고 전체에서 유일하고 안정적이어야 한다.

```text
INTRO.P1
METHODS.P2
RESULTS.3.4.P1
RESULTS.3.4.P2
DISCUSSION.4.2.P1
CONCLUSION.P1
```

- 섹션명은 대문자 영문 식별자를 권장한다.
- 소절 번호가 있으면 섹션과 단락 사이에 넣는다.
- 단락이 이동해도 가능하면 ID를 유지하고 배치 위치만 바꾼다.
- 삭제한 ID를 재사용하지 않는다.
- 부분 지도 임시 노드는 `LOCAL.DISCUSSION.4.2.P1`처럼 둘 수 있다. 전체 병합 때
  새 ID와 대응 관계를 결정 대장에 남긴다.

## 3. 구조 노드 형식

`## 구성` 아래에서 섹션·소절 heading을 쓰고, 각 단락은 `#### {ID}` 블록으로
기록한다.

```markdown
### Results

#### RESULTS.3.4.P1
- 상태: proposed
- 기능: Comparison
- 한 줄 논지: 유역별 ABL은 전국 단일값보다 큰 공간적 차이를 보였다.
- 앞 단락:
  - RESULTS.3.3.P3 | Question-Answer
- 근거:
  - Table-S2 | first-report
  - Fig-4 | supporting
- Ledger:
  - L07 | first-report
  - L09 | supporting
- 축:
  - epistemic-layer = observation
- Core message 기여: 국가값만으로 포착되지 않는 유역 차이를 제시
- 결정: D-021, D-022
- 메모:
  - Fig.4는 공간 예외와 전체 변동이라는 두 화제를 함께 담음
```

### 필수 필드

| 필드 | 규칙 |
|---|---|
| 상태 | `proposed / provisional / decided / resolved / omitted` |
| 기능 | 아래 기능 태그 또는 사용자 정의 태그 |
| 한 줄 논지 | 화제가 아니라 주장 한 문장 |
| 앞 단락 | `ID | 논리관계`; 첫 단락은 `—` |
| Core message 기여 | 한 절로 답하지 못하면 삭제 후보 |

### 선택 필드

| 필드 | 형식 |
|---|---|
| 근거 | `Evidence-ID | role` 목록 |
| Ledger | `Ledger-ID | role` 목록 |
| 축 | `축이름 = 값`; 원고별 사용자 정의 가능 |
| 결정 | 쉼표로 구분한 `D-###` |
| 메모 | 자유문 목록. 자동 검증에 쓰지 않는 정보 |

`메모`, `해석`, `제약`처럼 원고마다 다른 자유문은 모두 `메모` 목록으로 둔다.
자동 검증에 필요한 관계는 자유문에 숨기지 말고 정규 필드로 올린다.

## 4. 단락 상태

- `proposed` — 모델 제안, 사용자 결정 전
- `provisional` — 부분 지도 임시 배치, 상위 정합 미검증
- `decided` — 기능·논지·배치 합의
- `resolved` — 근거·간선·영향 검증까지 완료
- `omitted` — 삭제 결정. 기록은 남기되 활성 그래프에서 숨김

## 5. 기능 태그

**Introduction** — `Background` · `Lit-Review` · `Gap` · `Question` ·
`Purpose` · `Scope` · `Contribution`

**Methods** — `Study-Area` · `Design` · `Sample` · `Procedure` · `Instrument` ·
`Statistical` · `Quality`

**Results** — `Overview` · `Finding` · `Comparison` · `Trend` · `Pattern` ·
`Anomaly` · `Summary`

**Discussion** — `Interpretation` · `Mechanism` · `Lit-Comparison` · `Agreement` ·
`Disagreement` · `Limitation` · `Implication` · `Future` · `Conclusion`

새 기능 태그는 허용한다. 사용 사실과 정의를 결정 대장에 한 줄 남긴다.

## 6. 논리관계

`Continuation` · `Contrast` · `Cause-Effect` · `Specification` ·
`Generalization` · `Sequence` · `Concession` · `Problem-Solution` ·
`Evidence-Claim` · `Question-Answer`

한 단락이 여러 선행 단락을 받을 수 있다. 소절 경계를 넘는 간선도 완전한 ID로
모두 적는다.

```markdown
- 앞 단락:
  - RESULTS.3.3.P3 | Question-Answer
  - METHODS.P4 | Evidence-Claim
```

## 7. 사용자 정의 축

원고별 분류 축을 정규 필드로 둘 수 있다.

```markdown
- 축:
  - epistemic-layer = observation
  - spatial-scale = catchment
```

예: `observation / observation-to-interpretation / interpretation`. 그래프에서는
선택한 축 하나만 색으로 표현한다. 여러 축을 동시에 시각화하지 않는다.

## 8. 근거 인벤토리

Figure, Table, 데이터셋, 문헌을 선언한다. 단락 배정은 구조 노드의 `근거` 필드가
기준이며 인벤토리는 미배정 항목을 찾는 목록이다. 네 번째 열은 예상 범위다.

```markdown
## 근거 인벤토리

- Fig-1 | figure | available | RESULTS
- Fig-4 | figure | available | RESULTS.3.4
- Table-S2 | table | available | RESULTS.3.4
- Chen2024 | literature | available | DISCUSSION.4.2
```

역할: `first-report / primary / supporting / comparison / interpretation / reference`.
같은 근거가 여러 단락에 걸리는 것은 정상이나 `first-report`는 원칙적으로 하나다.

## 9. Ledger 인벤토리

반드시 착지해야 하는 수치·정의·핵심 주장과 first-report 제약을 선언한다. 네 번째
열은 예상 착지 범위다.

```markdown
## Ledger 인벤토리

- L01 | core-claim | required | manuscript
- L07 | quantitative-result | first-report-required | RESULTS.3.4
- L09 | limitation | required | DISCUSSION.4.2
```

자동 검증은 미배정, first-report 누락·중복, omitted 단락에만 남은 Ledger를 찾는다.

## 10. 결정 대장

미해결 목록을 append-only 목록으로 쓰지 않고 안정적 ID와 상태를 가진 결정으로
관리한다.

```markdown
## 결정 대장

#### D-001
- 상태: surfaced
- 우선순위: blocker
- 범위: manuscript
- 제목: Core message 확정
- 추천: 데이터 연계와 환류를 원고의 중심 주장으로 둔다.
- 근거: Fig-4, Table-S2, Ledger L01·L07이 이 방향에 직접 결속됨.
- 대안:
  - 국가 비교를 중심으로 두면 Introduction과 Discussion 단락 5개를 재배치
- 영향:
  - INTRO
  - DISCUSSION.4.2
  - CONCLUSION.P1
- 의존:
  - —
- 해소 기준: Core message 확정 후 관련 단락 논지와 일치 확인
- 이력:
  - 2026-08-22 | detected | 전체 구조 검토에서 발견
  - 2026-08-22 | surfaced | 사용자에게 추천안 제시
```

### 결정 상태

```text
detected → surfaced → decided → resolved
                    ↘ deferred
어느 상태에서든 → superseded
resolved/deferred → reopened
```

해결된 결정을 삭제하거나 번호를 당기지 않는다. `resolved`, `superseded`는 활성
대기열에서 숨긴다. `deferred`는 해당 범위를 다시 열 때 표시한다.

### 우선순위

`blocker / high / medium / low / mechanical`

- `blocker` — Core message, 섹션 경계, 질문–답 사슬처럼 후속 설계를 막음
- `high` — 여러 단락·근거·결정에 파급
- `medium` — 현재 섹션 내부 구조에 영향
- `low` — 쉽게 되돌릴 수 있는 국소 결정
- `mechanical` — 번호·오기·표기처럼 구조 판단이 거의 필요 없음

## 11. 부분 mapping과 경계 노드

대상 노드 외에 앞뒤 경계 노드 한 단계만 읽고 보여준다.

```text
[RESULTS.3.3.P3] → [RESULTS.3.4.P1] → [RESULTS.3.4.P2] → [DISCUSSION.4.2.P1]
    경계                  현재 범위                              경계
```

범위 밖 노드는 수정하지 않는다. 현재 변경으로 영향을 받은 결정은 `reopened`로
등록한다. 전체 outline이 없으면 경계 가정을 메모에 명시한다.

## 12. 근거 노트

자료당 5줄 안쪽으로 주장·출처 위치·한계·배정·허용 표현 강도를 남긴다.

```markdown
### Fig-4 — 유역별 ABL 지도
주장: 유역 간 차이가 크고 일부 예외 유역이 존재함.
한계: 전체 변동과 예외 화제를 한 도판이 함께 담음.
배정: RESULTS.3.4.P1(primary), RESULTS.3.4.P3(reference)
표현 강도: 공간적 차이를 보였다까지; 원인 설명은 불가.
```

## 13. 구형 outline 호환

기존 6열 표와 세로 블록을 best-effort로 읽는다.

```text
P3 | [Gap] | 급감을 설명한 연구가 없다
← P2 [Contrast]
근거: Chen2024
기여: 본 연구 필요성 수립
```

구형 형식에서는 전역 ID, 근거·Ledger 역할, 사용자 정의 축, 결정 상태·영향이
불완전할 수 있으므로 `legacy parse` 경고를 낸다. `## 미해결`의 `#1`, `#15`는
`D-001`, `D-015`로 가져온다. `해소`는 `resolved`, `보류`는 `deferred`,
"아직 말하지 않은 지적"은 `detected`로 분류하고 본문의 `미해결 #1` 참조도
보존한다. 추천·영향은 지어내지 않고 대화에서 보강한다. 사용자 승인 없이 1.1
형식으로 덮어쓰지 않는다.

## 14. 최소 검증 규칙

- 단락 ID·결정 ID 중복 금지
- 존재하지 않는 predecessor 경고; provisional 지도 밖 경계는 정보로 표시
- 인벤토리 근거·Ledger 미배정 경고
- first-report 누락·중복 경고
- 활성 blocker가 있는 범위는 resolved 확정 금지
- omitted 단락에만 남은 근거·Ledger 경고
- 부분 변경 후 범위 밖 영향이 reopened되지 않으면 경고

---

**Format version**: 1.1
