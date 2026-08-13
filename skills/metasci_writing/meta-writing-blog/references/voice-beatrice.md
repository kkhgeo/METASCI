# The Beatrice Voice (optional mode)

**This file is not the default.** The default voice of this skill is
`voice-and-structure.md` (quiet editorial exposition) and it stays in force unless the user
**explicitly** asks for the 베아트리체 / Beatrice voice. When they do, read this file *instead
of* `voice-and-structure.md` at steps 2 and 7 of the workflow. Everything else in `SKILL.md`
is unchanged: the template, the brand assets, the folder output, head/header fields,
references, and the delivery check.

The register comes from the sister skill `beatrice` (Complete Revelation Protocol) — Beatrice
leads Dante through Paradiso by granting the whole vision at once rather than descending circle
by circle. A Beatrice brief is therefore **not a restyled brief**. It is a different *shape*:
one continuous revelation, sized with discipline.

---

## 1. What changes (delta from the default voice)

| | Default (`voice-and-structure.md`) | Beatrice mode |
|---|---|---|
| **Opening** | 문제 제기로 시작; 일화·대화체 도입 금지 | **이완하며 시작한다** — 매력적 질문, 생생한 비유, 또는 통찰적 관찰 |
| **Prose form** | 산문 + 컴포넌트(목록·표) 병용 | **연속 산문만.** 불릿·번호목록·파편 문장 금지 |
| **Sections** | 8비트 아크를 여러 `<section>`/`<h2>`로 분절 | **끊지 않는다.** `<h2>` 없이 하나의 흐름; 많아야 1–2개 경첩 |
| **Length** | 완결된 해설(상한 없음) | **상한 준수** — 단순 1–2단락 / 보통 2–4 / 복잡 4–6(천장) |
| **Metaphor** | 이해를 날카롭게 할 때만, 이후 정밀한 언어로 복귀 | 기본 도구로 허용 |
| **Close** | 절제된 전망 | **하나의 종합 문장**이 전체를 묶는다 |

분량 상한이 이 모드의 정체성이다. 상한을 풀면 그것은 "산문체 브리프"일 뿐 베아트리체가
아니다. 주제가 도저히 안 들어가면, 핵심 아크를 온전히 다루고 **무엇을 덜어냈는지 한 문장으로
밝힌 뒤** 끝낸다 — 천장을 넘기지 않는다. *논리의 완결성이 세부의 완결성에 우선한다.*

## 2. What stays the same (invariants — do not "fix" these)

- **문제가 방법보다 먼저 온다.** 이것은 보이스가 아니라 이 스킬의 대들보다. 베아트리체의
  "전제에서 결론까지의 완결된 논리 아크"와 충돌하지 않으므로 두 모드 공통으로 유지한다.
- **한국어 전용 + 괄호 영어 규칙** (필수 규칙 인라인 — 이 모드에서 `voice-and-structure.md`를
  따로 읽지 않는다): 본문은 한국어만으로 자족해야 한다. 번역이 어색하거나 정착 안 된 용어는
  **첫 언급에만** `보유(retention)` 식으로 글로스하고 이후 한국어로 쓴다. 음차 방치
  (`카운터팩추얼 시나리오로…`) 금지, 한국어 없는 맨 영어 투입(`retention으로 추정한다`) 금지.
  고유명사·방법명·지표·단위(SWAT, R², kg/yr)는 원형 유지. 판정 기준: *한국어만 아는 독자가
  이 문장을 확신 있게 따라오는가.* 과용도 금지 — 한국어가 명확하면 글로스를 달지 않는다.
- **AI 티 나는 표현 배제** — 유려함은 상투구의 면허가 아니다. 금지 목록(인라인):
  헛기침(`~라는 점에 주목할 필요가 있다`, `~을 언급할 가치가 있다`), 목록식 산문(`첫째…둘째…`,
  `결론적으로`), 공허한 수식(`획기적인`, `혁신적인`, `~을 심층적으로 파헤친다`), 대칭 3항
  (`빠르고 단순하며 강력한`), `A뿐만 아니라 B도`, 과도한 명사화(`~의 활용을 수행한다`→`~을 쓴다`).
  "X에 주목할 필요가 있다"라고 쓰고 싶으면 그냥 X를 쓴다.
- **정직한 한계와 출처 귀속** — 실패 양상을 적고 APA 참고문헌을 단다. 계시는 과장이 아니다.
- **발간 전 meta-mywriting-korean 재작성 패스** (SKILL.md 11단계) — 두 모드 공통 필수.
  단, 이 모드에서는 연속 산문·분량 상한·종합 문장 마무리를 깨지 않는 범위에서 적용한다.
- KEI 디자인·팔레트·폴더 산출·브랜드 에셋·검증 단계 전부 동일.

## 3. The shape: one continuous revelation

기본 모드의 8비트 아크를 **하나의 악장으로 압축**한다. 순서는 유지하되 섹션으로 쪼개지 않는다.

1. **이완하며 열기** — 질문·비유·관찰로 들어오되, 그 도입이 곧 **문제를 세우는** 일이어야 한다.
   장식적 일화는 여전히 금지다. 도입은 매력적이면서 동시에 논점이어야 한다.
2. **문제를 정밀하게, 그리고 왜 어려운가** — 소박한 접근이 정확히 어디서 깨지는지.
3. **해결의 아이디어, 단순한 것부터** — 뼈대를 먼저 세우고 한 겹씩. 수식은 그것이 형식화하는
   산문 뒤에 온다.
4. **무엇을 얻고 어디서 실패하는가** — 실제 숫자 하나와 정직한 한계.
5. **종합 문장 하나로 닫기** — "이어서 볼까요?"류의 물음은 없다. 그것은 자매 스킬 virgil의 몫이다.

여러 편의 논문을 함께 다룰 때도 **공유 스파인** 원칙은 같다. 다만 병렬 사례를
`comparison-grid`로 늘어놓지 않고, 하나의 서술 안에서 대비시킨 뒤 종합으로 닫는다.

## 4. Components

연속 산문이 원칙이므로 컴포넌트는 최소로 쓴다.

- **허용** — `figure`(이미지+캡션), `figure-equations`(수식), `figure-canvas`(시각화, lazy-start).
  이들은 목록이 아니라 산문에 삽입되는 대상이다.
- **금지** — `var-list`, `comparison-grid`, 그리고 불릿·번호목록 일반. 기호 정의는 산문 안에서
  풀어 쓴다(`여기서 x는 …를, y는 …를 가리킨다`).
- **조건부** — `data-table`은 수치가 여럿이어서 산문으로 옮기면 오히려 읽기 어려울 때만.
  값이 두셋이면 문장으로 쓴다.
- **`callout`** — 온전한 산문 문장을 담을 때만, 아주 드물게. 불릿의 대용으로 쓰지 않는다.

템플릿에서 쓰지 않는 컴포넌트 예시는 **전부 삭제**한다(기본 모드와 동일한 규칙).

## 5. Register notes

- `–다`체와 비인칭은 유지한다. 유려하다는 것이 `우리`, `함께 살펴봅시다`를 허용한다는 뜻은 아니다.
- 헤지는 하되 뭉개지 않는다. 베아트리체는 확신 있게 말하고, 불확실한 곳을 **지목해서** 불확실하다고
  말한다. 모든 문장에 `~로 보인다`를 다는 것은 실패다.
- 문장 길이를 변주한다. 긴 만연체만 이어지면 유려함이 아니라 탁함이 된다.
- 초록(`.article-abstract`)은 1–2문장으로, 본문과 같은 등록부로 쓴다.

## 6. Quality checklist (replaces the default's voice/structure items)

- [ ] 도입이 이완하면서도 **문제를 세운다** — 장식적 일화가 아니다.
- [ ] 본문 전체가 **연속 산문**이다 — 불릿·번호목록·파편 문장이 없다.
- [ ] `<h2>` 분절이 없거나 1–2개뿐이며, 글이 하나의 흐름으로 읽힌다.
- [ ] **분량 상한을 지켰다**(복잡한 주제도 6단락 이내). 넘칠 뻔했다면 덜어낸 것을 한 문장으로 밝혔다.
- [ ] 문제 → 왜 어려운가 → 방법 → 결과·한계 순서가 살아 있다.
- [ ] 마지막이 **종합 문장 하나**로 닫힌다. 계속할지 묻지 않는다.
- [ ] 한국어 전용·괄호 영어·AI 티 배제 규칙을 지켰다(`voice-and-structure.md` §4–5).
- [ ] 컴포넌트는 허용 범위 안에서만 쓰였고, 미사용 예시는 삭제됐다.
- [ ] (공통) 자산 경로가 전부 로컬이고 `[REPLACE …]` 마커가 남아 있지 않다.
