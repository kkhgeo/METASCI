# outline.md 규격

작업 폴더에 **파일 하나**만 둔다. 섹션별로 쪼개지 않는다 — 전체 조망과 섹션
조망이 같은 파일의 다른 배율이어야 하기 때문이다.

## 파일 구조

```markdown
# Outline — {원고 제목 또는 가제}

- Core message: {이 원고가 관철할 단 하나의 주장, 한 줄}
- 원고 언어: English | 한국어
- 최종 갱신: YYYY-MM-DD

## 구성

### Introduction
{6열 표}

### Methods
{6열 표}

...

## 근거 노트
{정독 결과 — 재조망 때 재사용}

## 미해결
{합의 못 한 것, 보류한 결정, 사용자가 규칙을 이기고 내린 판단과 그 이유,
그리고 3개 상한에 걸려 아직 말하지 못한 지적 — 규칙 이름과 한 줄 이유를 붙여서}
```

## 구성 표 — 6열

한 단락이 한 행이다. 터미널에서 6열이 넘치면 아래 세로 형식을 쓴다.

| 단락 | 기능 | 한 줄 논지 | ←앞 단락 | 근거 | Core message 기여 |
|---|---|---|---|---|---|
| P1 | Background | … | — | — | 문제의 무대 설치 |
| P2 | Lit-Review | … | Continuation | Kim2020 외 3 | 무엇이 알려졌나 |
| P3 | Gap | … | Contrast | Chen2024(불충분) | 본 연구 필요성 |
| P4 | Purpose | … | Problem-Solution | — | Core message 직결 |

세로 형식(열이 많을 때):

```
P3 | [Gap] | 급감을 설명한 연구가 없다
   ← P2에 대한 [Contrast]
   근거: Chen2024(도시 하천이라 부분적), ⚠ 농업 유역 사례 없음
   기여: 본 연구 필요성 수립
```

### 열별 규칙

- **한 줄 논지** — 주장 한 문장. 원고 언어로 쓴다. "~에 대해 서술"처럼 화제만
  적는 것은 논지가 아니다. **주장이 없으면 그 단락은 아직 설계되지 않은 것이다.**
- **←앞 단락** — 아래 논리관계 10개 중 하나. 첫 단락은 `—`.
- **근거** — `Fig.2`, `Table 1`, `(Kim, 2020)` 형식. 없으면 `⚠ 근거없음`으로
  두고 넘어가지 말 것(SKILL.md 원칙 6).
- **Core message 기여** — 한 절(clause)로 못 쓰면 그 단락은 뺀다. 쓰고 나서
  빼는 것보다 싸다.

## 기능 태그

extraction-logic의 어휘를 그대로 쓴다. **목록에 없는 기능이면 새 태그를 만들어
쓰고, 만들었다는 사실을 미해결 항목에 적는다.**

**Introduction** — `Background` 분야 배경 · `Lit-Review` 선행연구 요약 ·
`Gap` 기존 연구의 한계 · `Question` 연구 질문·가설 · `Purpose` 연구 목적 ·
`Scope` 범위·접근 · `Contribution` 기여·의의

**Methods** — `Study-Area` 연구 지역 · `Design` 설계 · `Sample` 표본·수집 ·
`Procedure` 절차 · `Instrument` 장비·소프트웨어 · `Statistical` 통계 분석 ·
`Quality` 품질관리·검증

**Results** — `Overview` 전체 요약 · `Finding` 핵심 발견 · `Comparison`
집단·조건 비교 · `Trend` 시공간 경향 · `Pattern` 패턴·관계 · `Anomaly`
이상치·예외 · `Summary` 소절 요약

**Discussion** — `Interpretation` 의미 해석 · `Mechanism` 기작·원인 ·
`Lit-Comparison` 선행연구 대조 · `Agreement` 일치 · `Disagreement` 불일치와
그 설명 · `Limitation` 한계 · `Implication` 함의·응용 · `Future` 향후 연구 ·
`Conclusion` 최종 결론

## 논리관계 (←앞 단락)

`Continuation` 같은 화제 확장 · `Contrast` 대립으로 전환 · `Cause-Effect`
원인→결과 · `Specification` 일반→구체 · `Generalization` 구체→종합 ·
`Sequence` 시간·논리 순서 · `Concession` 양보 후 주장 · `Problem-Solution`
문제 제기 후 해법 · `Evidence-Claim` 증거 후 주장 · `Question-Answer` 질문 후
전개

## 근거 노트

정독한 결과를 여기 쌓는다. **두 번째 조망부터는 이 노트만 읽고 원자료를 다시
읽지 않는다.** 이것이 정독 비용을 치르는 유일한 이유이므로, 노트는 그 목적에
필요한 만큼만 쓴다 — **자료 하나당 5줄 안쪽**. 요약본을 만드는 게 아니다.

```markdown
### Fig.2 — 시계열
2015년 이후 급감(약 –40%). 2015 이전은 평탄. 계절성 뚜렷.
→ 배정: Results P2(현상 기술), Discussion P1(해석 대상)

### Chen et al. (2024) — Water Research
주장: 도시 하천에서 □□ 기작으로 유사한 급감이 설명된다 (p.4, Fig.3)
한계: 도시 하천 대상. 본 연구는 농업 유역이므로 직접 적용 불가.
→ 배정: Discussion P2(부분적 설명 근거), Intro P3(Gap의 반대 축)
→ 표현 강도: "부분적으로 설명된다"까지. "설명된다"는 과장.
```

노트에는 **주장·출처 위치·한계·배정·허용 표현 강도**를 적는다. 원문을 그대로
옮기지 않는다(표절 방지 — 노트는 메모이지 초고가 아니다).

## 상태 표기

- `⚠ 근거없음` — 근거 열이 빈 단락
- `⚠ 추정` — 아직 자료로 확인 못 한 배치
- `※ 사용자 결정` — 규칙과 충돌하지만 사용자가 확정한 것 (이유를 미해결에 기록)
