# 규칙 라우팅 — 무엇을 판단할 때 무엇을 읽나

이 스킬은 글쓰기 규칙을 **새로 만들지 않는다.** 기존 META-SCI 스킬이 이미
정의한 규범을 근거로 지적한다. 지적할 때는 반드시 **규칙 이름**을 댄다.

## 라우팅 표

| 판단하려는 것 | 읽을 파일 | 위치 |
|---|---|---|
| 섹션끼리 아귀가 맞나 (전체 조망) | `structural-integrity.md` | 이 폴더 |
| 이 섹션에 무슨 단락이 있어야 하나 | `section-checklists.md` | 이 폴더 |
| 단락 순서·연결이 자연스러운가 | `cohesion_flow.md` | Glob `**/meta-proofreading/writing-manual/cross_section/cohesion_flow.md` |
| 섹션 골격과 전환어 | `section_guides.md` | Glob `**/meta-writing/references/section_guides.md` |
| 단락 하나가 논지로 성립하나 | `principles.md` | Glob `**/meta-rewriting/references/principles.md` |

**Glob 결과가 여러 개면 `skills_archive/` 아래 것은 버린다** — 구버전
`paper-proofreader` 잔재다. 항상 `skills/` 아래 것을 읽는다.

이 폴더의 두 파일은 교정용 매뉴얼을 **설계 단계용으로 줄여 쓴 것**이다.
사본이 아니므로 원본을 다시 복사해 덮어쓰지 않는다 — 덮어쓰면 문장 수준
항목이 도로 들어와 이 스킬이 검사 보고서로 변한다.

## 전체 조망에서 실제로 걸리는 것 — `structural-integrity.md`

전체를 볼 때는 이 다섯 가지를 순서대로 확인한다. **섹션 하나만 보고 있을 때는
이 판정을 할 수 없다** — 못 한다고 말하지, 통과한 것처럼 굴지 않는다.

1. **질문 체인** — Intro가 던진 질문에 Discussion이 답하고 Conclusion이
   되짚는가. 던지고 안 받은 질문, 받았는데 안 던진 답이 있는가.
2. **Methods ↔ Results 1:1** — 기술한 방법마다 결과가 있고, 보고한 결과마다
   방법이 있는가. `method-without-result` / `result-without-method`를 짚는다.
3. **가설 → 분석 → 해석 평행성** — 세 곳의 순서가 같은가. 가설 순서와 결과
   제시 순서가 어긋나면 독자가 대응을 못 잡는다.
4. **Abstract ↔ 본문** — 초록의 주장이 본문에 다 있는가. 초록에만 있는 주장은
   설계 누락이다.
5. **Scope Discipline** — 단일 지점·단일 시기 자료로 일반 명제를 주장하는가
   (표본→모집단 과잉일반화). 설계 단계에서 잡으면 문장 고칠 일이 없다.

## 섹션 단위에서 걸리는 것 — `section-checklists.md`

해당 섹션 항목만 읽는다. 자주 걸리는 것:

- Introduction에 **Gap 단락이 없음** → 목적 단락이 왜 필요한지가 안 선다
- Discussion이 Results를 되풀이만 하고 **해석·기작이 없음**
- Results에 **선행연구 비교가 섞여** Discussion과 중복
- Conclusion이 요약만 하고 **함의가 없음**
- Methods에 있는 절차가 Results에 안 나타남

`section-checklists.md`에는 학위논문 장 단위와 연구계획서 항목도 있다. 논문이
아닌 원고면 그쪽을 본다.

## 단락 순서를 논의할 때 — `cohesion_flow.md`

설계 단계에서 쓰는 것은 두 절뿐이다.

- **§4 Paragraph Architecture** — 한 단락 한 논지, 단락 분절이 과한지
- **§2 주제 전개 패턴(Daneš)** — 단락들의 화제가 어떻게 이어지는가.
  Linear(꼬리물기) / Constant(같은 화제 유지) / Derived(상위 화제에서 갈라짐) /
  Split Rheme(앞에서 예고한 것을 차례로). 순서가 어색할 때 **어느 패턴을
  쓰려다 깨졌는지**로 설명하면 논의가 구체가 된다.

`§1 Given-New`는 문장 수준이라 설계 단계에서는 보지 않는다.

## 설계 단계에서 **보지 않는** 것

아래는 문장이 존재해야 판단할 수 있다. 초고가 있어도 여기서 지적하지 않는다 —
집필 후 `meta-proofreading` 몫이다.

- `sentence_craft.md` (명사화, 태, 시제)
- `stance_hedging.md` (헤징 강도)
- `clutter_redundancy.md` (군더더기)
- `advanced_nns_issues.md` (연어·관사)
- `quantitative_integrity.md` (수치 정합) — 단, 그림·표가 서로 모순되면
  설계 문제이므로 그때는 짚는다

## 지적하는 방식

- 규칙 이름을 대고, **왜 문제인지 한 줄**을 붙인다.
  좋음: "Gap 단락이 없습니다 — 급감을 아무도 설명 못 했다는 말이 없어서
  목적 단락이 왜 필요한지가 안 섭니다."
  나쁨: "서론 흐름이 조금 어색합니다."
- 한 번에 3개까지만. 그 이상은 논의가 아니라 검사 결과 통보가 된다.
- **4번째부터는 버리지 말고 `outline.md` 미해결에 적는다.** 그리고 적었다는
  사실을 한 줄로 알린다 — "이 밖에 N개는 미해결에 적어뒀습니다." 상한은
  지금 말할 것의 개수이지 찾을 것의 개수가 아니다.
  괄호에 몰래 끼워 넣거나 "일단 적어만 두겠다"고 얼버무리지 않는다. 그건
  상한을 우회하는 것이지 지키는 것이 아니다.
- 사용자가 근거를 대고 반대하면 따르고 `outline.md` 미해결에 기록한다.
