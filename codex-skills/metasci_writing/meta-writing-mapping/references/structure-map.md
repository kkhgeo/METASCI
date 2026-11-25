# 원고 구조 지도 — 요청 시 선택 출력

사용자가 원고의 구조를 **지도로 보여 달라고 요청할 때만** 읽는다. 예: "구조 지도
만들어줘", "단락 연결을 지도로", "구조 시각화", "HTML 지도". 기본 출력인 세로 구조도와
두 표(map-format.md)를 대체하지 않으며, 지도를 만들었다고 구성 판단이 끝나지 않는다.
정본은 원고와 `outline.md`이고 지도는 그것을 읽는 도구다.

지도는 단락 하나를 카드 하나로, 원고를 읽는 순서를 세로축으로 고정해 그린다. 한 단락이
다른 단락에 기대는 관계는 왼쪽의 호로, 인용은 오른쪽 열로 그린다. 위로 거슬러 오르는
호는 아직 읽지 않은 단락에 기대는 **앞선 참조**다. 섹션 보드는 단락 연결을 모아 섹션
사이의 의존을 보여준다.

## 역할 분담

- **모델이 쓰는 것:** `structure-map.json` — 단락의 역할, 주제문, 단락 사이의 연결과
  그 근거, 주 주장, 인용, 용어의 정의 위치. 무엇이 무엇에 기대는지는 읽어야만 판단할 수
  있으므로 모델의 일이다.
- **스크립트가 하는 것:** `scripts/structure_map.py` — 형식 검증, 원고 대조(주제문이
  원문 그대로인지, 신호어가 그 문장에 있는지, 용어가 처음 쓰인 단락), 구조 점검 계산,
  HTML 생성. 의미를 판단하지 않는다.

연결은 **해석**이다. 그래서 모든 연결에 근거 문장 주소(`at`)와 확실성(`basis`)을 붙이고,
지도는 원문 신호가 있는 연결을 실선으로, 추론한 연결을 점선으로 구분해 그린다.

## 두 종류의 지도

| 종류 | `source.kind` | 언제 | 카드의 문장 | 연결의 근거 |
|---|---|---|---|---|
| 초고 지도 | `draft` | 원고가 있을 때 | 저자의 주제문, 원문 그대로 | `at` 주소 + `explicit` / `inferred` |
| 계획 지도 | `outline` | 초고 전, 합의한 두 표에서 | 간략 구성표의 핵심 내용 | `planned`, 주소 없음 |

계획 지도는 점선 카드로 그려지며, 계획한 순서의 앞선 참조와 답이 이어지지 않은 질문을
집필 전에 보여준다. 계획을 실제 연구가 입증한 것처럼 읽지 않는다(structural-integrity
"전제").

## 절차

1. **범위와 원고 본문.** 요청한 범위의 단락을 대상으로 하되, 번호는 원고 전체 기준을
   유지한다. 원고가 Markdown·텍스트가 아니면(PDF, docx) 본문을 **고치지 않고** 텍스트로
   옮긴 사본을 작업 폴더에 `structure-map.draft.md`로 둔다. 단락은 빈 줄로 구분하고,
   `#` 제목 줄과 HTML 주석은 단락 번호에서 빠진다. 스크립트도 같은 규칙으로 센다.
   그림 설명·표·수식 블록은 단락이 아니므로 사본에서 뺀다.
2. **주소.** 단락은 `P1, P2, …`로 원고 전체에 걸쳐 잇고, 문장은 단락마다 `S1`부터
   다시 센다. extraction-logic과 같은 `[P#-S#]` 주소다.
3. **섹션과 단락.** 섹션마다 `type`(introduction · methods · results · discussion ·
   conclusion · abstract · other)을 준다. 단락마다:
   - `role` — 기능 태그. extraction-logic의 단락 기능 태그(Background, Gap, Purpose,
     Study-Area, Procedure, Finding, Pattern, Interpretation, Mechanism, Limitation,
     Conclusion 등)를 쓰고, 맞는 것이 없으면 새로 만든다. 질문을 세우는 단락은
     Gap · Question · Purpose · Hypothesis 중 하나로 표시해야 점검이 그 질문을 따라간다.
   - `topic` + `topic_at` — 단락의 요지를 말하는 문장을 **원문 그대로** 복사한다.
     요약하거나 다듬지 않는다. 명시적 주제문이 없으면 첫 문장을 쓰고, 그 사실을 보충
     설명에 적는다(주제문이 없다는 것 자체가 구성 정보다).
   - `sentences` — 문장 수.
   - `to_next` — 같은 섹션의 다음 단락과의 관계와 신호어. 관계는 extraction-logic의
     10종(Continuation, Contrast, Cause-Effect, Specification, Generalization, Sequence,
     Concession, Problem-Solution, Evidence-Claim, Question-Answer)을 쓴다. 신호도 관계도
     읽히지 않으면 `{"relation": "none"}`. 섹션의 마지막 단락은 생략한다.
4. **원거리 의존 추출.** 지도의 핵심이다. 단락을 순서대로 읽으며 각 단락마다 묻는다:
   *이 단락을 이해하거나 받아들이려면 다른 어느 단락을 먼저 읽어야 하는가.* 인접한
   단락에 한정하지 않는다. 연결의 `from`은 기대어지는 단락, `to`는 그 위에 세우는
   단락이다(근거 → 주장 방향).

   | `kind` | 뜻 | 전형 |
   |---|---|---|
   | `evidence` | `from`의 결과·관찰이 `to`의 주장을 뒷받침 | 결과 → 해석, 해석 → 결론 |
   | `method` | `to`의 결과가 `from`의 절차·설계·자료로 얻어짐 | 방법 → 결과 |
   | `premise` | `to`가 `from`의 정의·가정·앞선 해석을 전제로 씀 | 정의 → 사용, 해석 → 기작 |
   | `contrast` | `to`가 `from`에 맞서거나 한계를 짚음 | 선행연구 → 공백 |
   | `answers` | `to`가 `from`의 질문·공백·목적에 답함 | 공백·목적 → 논의·결론 |
   | `motivates` | `from`이 `to`의 필요를 세움 | 배경 → 공백 |
   | `continues` | 같은 논의를 이어감(다른 관계가 없을 때만) | 배경 → 배경 |

   - **원문 신호(`explicit`)** — `at` 문장 안에 연결을 드러내는 말이 있을 때. 지시어+명사
     ("this slope", "these wells"), 교차참조("Section 2.3", "Fig. 3"의 결과를 다룬 단락),
     정의된 용어의 재사용, 수치의 재인용, 연결어. 그 말을 `signal`에 원문 그대로 적는다.
   - **추론(`inferred`)** — 신호 없이 내용으로 판단한 연결. `note`에 판단 이유를 한 줄로
     적는다. 추론 연결이 많다는 것도 독자가 관계를 스스로 메워야 한다는 정보다.
   - `at`은 기대는 쪽(`to`) 단락에서 그 의존이 드러나는 문장이다.
   - 독자에게 필요한 의존만 적는다. 같은 화제를 다룬다는 이유만으로 잇지 않는다. 결과
     단락은 대개 방법 연결을 하나 이상, 해석 단락은 근거 연결을 하나 이상 가진다.
   - **점검을 통과시키려고 연결을 만들지 않는다.** 읽히지 않는 연결은 없는 것이다.
     연결이 없어서 생긴 점검 결과가 바로 원고의 정보다.
   - 뒤의 단락에 기대는 연결도 그대로 적는다. 원문이 "Section 4에서 다룬다"처럼 뒤를
     명시적으로 예고하는 경우에만 `"forward_ok": true`를 붙인다.
5. **주 주장.** `main_claims`에 원고(또는 범위)가 결국 도달하는 주장 단락을 적는다.
   대개 결론이나 논의 마지막 단락이며, 대화에서 합의한 핵심 메시지와 대조한다.
   어느 단락인지 저자 의도에 따라 달라지면 ◇로 묻는다. 범위에 주장 단락이 없으면 비운다.
6. **인용과 용어.** `citations`는 문헌별 등장 주소와 역할(support · comparison · method ·
   contrast). `terms`에는 원고의 핵심 개념·약어 중 정의가 필요한 것을 적고 `defined_at`에
   정의하는 문장을 준다. 첫 사용 위치는 스크립트가 원고에서 찾는다.
7. **검증과 생성.** 작업 폴더에서 실행한다.

   ```
   python "<skill-dir>/scripts/structure_map.py" build structure-map.json --text structure-map.draft.md
   ```

   오류가 있으면 HTML을 만들지 않는다. 오류를 고쳐 다시 실행한다. 주제문 불일치 오류는
   주제문을 원문대로 다시 복사해 고친다. 경고는 읽고 판단한다(문장 수 경고는 약어 때문인
   경우가 많다). `check` 모드는 HTML 없이 점검만 한다. 원고 사본이 없는 계획 지도는
   `--text` 없이 실행한다.
8. **판단과 보고.** 점검 결과는 **후보**다. 각 후보를 section-checklists와
   structural-integrity의 기준으로 판단한 뒤 기존 보충 설명 형식(번호, ◇, `⚠ 자료없음`,
   `확인 필요`)으로 전달한다. 유효한 다른 순서이거나 자료가 범위 밖에 있으면 이유를 들어
   제외한다. 결과 파일 경로를 알리고, 사용자가 HTML을 브라우저로 열면 카드와 점검을 눌러
   볼 수 있다고 한 줄로 설명한다.

## 점검 항목

스크립트가 계산한다. 비교할 양쪽이 지도에 있을 때만 판정한다(structural-integrity
"전제"). 예를 들어 방법 섹션이 범위에 없으면 방법 연결 점검을 하지 않는다.

| 코드 | 무엇을 찾나 | 수준 | 판단 기준 |
|---|---|---|---|
| `forward-reference` | 뒤의 단락에 기대는 연결. 근거·방법·전제면 중요 | 중요 / 확인 | structural-integrity §7, 공통 점검 "필요한 정보를 제때 만나는가" |
| `term-before-definition` | 용어가 정의보다 먼저 쓰임 | 중요 | 같음 |
| `unanswered-question` | 공백·질문·목적에서 논의·결론으로 가는 `answers` 연결이 없음 | 중요 | structural-integrity §1 |
| `result-without-method` | 결과 단락에 `method` 연결이 없음 | 확인 | structural-integrity §2 |
| `orphan` | 주 주장까지 이어지는 연결이 없는 단락 | 확인 | structural-integrity §6, 공통 점검 "빼면 무엇이 달라지는가" |
| `weak-transition` | 붙어 있는 단락 사이에 관계 신호도 연결도 없음 | 확인 | 공통 점검 "각 부분의 역할과 연결이 읽히는가" |
| `cycle` | 서로에게 기대는 단락의 고리(대조 제외) | 확인 | structural-integrity §5 순환 논증 |
| `overloaded` | 다섯 단락 이상이 기대고 문장이 8개 이상 | 참고 | 단락 역할 |

## 데이터 형식

`assets/example-map.json`(가상 원고 `assets/example-draft.md`의 지도)이 완전한 예시다.

| 필드 | 필수 | 내용 |
|---|---|---|
| `$schema` | ○ | `"metasci/structure-map@1"` |
| `title` | | 지도 제목 |
| `source` | ○ | `{ "kind": "draft" \| "outline", "file": "…" }` |
| `main_claims` | | 주 주장 단락 id 목록 |
| `sections[]` | ○ | `{ id, label, type }` |
| `paragraphs[]` | ○ | 읽기 순서대로. `{ id: "P#", section, role, topic, topic_at, sentences, to_next }`. 계획 지도는 `topic_at` 생략 |
| `links[]` | | `{ from, to, kind, basis, at, signal, note, forward_ok }`. 초고 지도는 `at` 필수, `explicit`은 `signal` 필수 |
| `citations[]` | | `{ key, at: ["P#-S#"], role }` |
| `terms[]` | | `{ term, defined_at, first_used_at }`. `--text`가 있으면 `first_used_at`은 원고에서 다시 찾는다 |

## 파일과 공유

작업 폴더에 `structure-map.json`, `structure-map.html`, (필요하면) `structure-map.draft.md`를
둔다. 기존 `outline.md`와 원고는 건드리지 않는다. HTML은 외부 요청이 없는 단일 파일이라
오프라인에서 열린다.

지도에는 **원고의 문장이 그대로** 들어 있다. 미발표 원고이므로, 사용자가 요청하지 않은
곳에 올리거나 공유하지 않는다. Claude 앱에서 Artifact로 게시해 달라는 요청이 있으면,
게시하면 원고 문장이 사용자의 claude.ai 계정에 올라간다는 점을 먼저 말한다.

## 갱신

원고가 바뀌면 바뀐 단락만 다시 읽고 지도를 고친다. 단락이 추가·삭제되어 번호가 밀리면
모든 주소를 원고 기준으로 다시 매기고, 이전 지도의 연결은 내용으로 옮겨 온다. 사용자가
보는 보충 설명에는 무엇이 해소되고 무엇이 새로 생겼는지를 적는다.
