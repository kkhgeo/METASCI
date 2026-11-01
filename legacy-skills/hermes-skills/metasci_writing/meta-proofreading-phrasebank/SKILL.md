---
name: meta-proofreading-phrasebank
description: >
  Compare an English academic paragraph with the built-in Manchester Academic
  Phrasebank, sentence by sentence, by rhetorical function: identify what each
  sentence is doing, look up that function's phrases, and return verdicts,
  bank-sourced alternatives, and a minimally edited paragraph. Use when the user
  says "phrasebank 대조", "파레이즈뱅크", "phrasebank로 봐줘", "표현 대조",
  "기능별 표현 점검", or "check against the phrasebank". Plain "논문 교정" goes
  elsewhere; published-usage checks go to meta-proofreading-evidence, argument
  and logic to meta-rewriting, AI traces to meta-rewriting-antiai.
---

# Meta-Proofreading-Phrasebank

영어 단락의 문장이 그 기능에 맞는 표현을 쓰는지 내장 Phrasebank와 대조한다.
논리·구성·내용은 평가하지 않는다. 설명은 한국어로, 표현은 영어 원문으로 쓴다.

## 데이터

- `references/function_index.md`: 기능 151개의 ID 목록. 작업마다 먼저 읽는다.
- `references/bank/*.md`: 기능별 표현. 직접 읽지 말고 ID로 조회한다.
- `references/caution_terms.md`: 표현이 Phrasebank에 있어도 경고할 어휘.

스크립트는 이 스킬 폴더를 기준으로 실행한다. Python 3.7 이상이면 되고 표준 라이브러리만
쓰므로 설치할 것이 없다.

```bash
python -I scripts/lookup.py DIS-03 INT-09      # 해당 기능의 표현 전체
python -I scripts/lookup.py --grep "not known|is known" # 키워드로 ID 찾기(정규식)
```

표기: `{a | b}`는 택일 칸이고, `X`, `Y`, `Smith (2003)`, `…`는 채워 쓰는 자리다.
예시 속 소재(vitamin C, literate societies 등)는 문형만 참고한다.

## 절차

1. 단락을 문장으로 나눈다. 단락이 없으면 요청하고, 여러 단락이면 한 번에 한
   단락만 처리한 뒤 `다음 단락`을 기다린다. 논문의 어느 섹션인지 모르면 문장
   자체로 판단하고 가정을 밝힌다.
2. `function_index.md`에서 문장마다 기능을 고른다. 주 기능 1개, 필요하면 보조
   기능 1개까지다. 보조 기능에는 일반 언어 기능(CAU, CRI, CMP 등)도 쓸 수 있다.
3. 고른 ID를 한 번에 조회한다. 맞는 틀이 없으면 문장당 최대 2회까지 인접 기능이나
   `--grep`으로 더 찾고, 그래도 없으면 `대응 없음`으로 둔다. `--grep` 결과에는 소재만
   겹치는 예시도 섞이므로 해당 ID의 기능이 맞는지 확인한다.
4. 문장을 조회한 틀과 비교해 판정한다. `caution_terms.md`의 어휘도 확인한다.
5. 필요한 곳만 고쳐 최소 수정본을 만든다.
6. 수정본이 있으면 원문과 수정본을 스킬 폴더 밖의 임시 위치에 저장하고 보존 검사를
   실행한다. 실패하면 5단계로 돌아가 해당 문장을 원문 쪽으로 되돌리고, 통과할 때까지
   다시 검사한다. 같은 항목이 두 번 실패하면 그 문장은 원문을 유지하고 사용자에게 알린다.
7. 보존 검사는 소문자 전문용어와 미묘한 의미 변화를 잡지 못하므로 바뀐 문장을 원문과
   직접 대조한다. 문제가 있으면 5단계로 돌아간다.

```bash
python -I scripts/check_preservation.py <임시폴더>/original.txt <임시폴더>/revised.txt
```

검사 기준에 없는 이유로 문제를 발견하면, 작업 끝에 새 규칙 하나를 제안하고 사용자가
승인한 뒤에만 스킬에 반영한다.

## 판정

| 판정 | 기준 |
|---|---|
| `유지` | 기능에 맞고 명확하다. Phrasebank와 달라도 저자 표현이 더 정확하면 유지한다 |
| `조정` | 틀은 맞지만 연어·전치사·어순 등 일부가 어색하다 |
| `교체` | 표현이 문장의 기능을 흐리거나 다른 기능처럼 읽힌다 |
| `주의` | 경고 어휘를 포함한다. Phrasebank 수록 여부와 무관하다. 강도가 같은 대안이 있으면 수정본에 반영하고, 없으면 원문을 두고 표시만 한다 |
| `대응 없음` | 맞는 틀이 없다. 오류라는 뜻이 아니며 평가하지 않는다 |

## 출력

```markdown
| # | 원문 | 기능 (ID) | 판정 | 대안 (출처 ID) |
|---|---|---|---|---|

### 수정본
(최소 수정본 단락. 바뀐 부분은 **굵게**)

### 변경 이유
(바뀐 문장마다 한 줄. `유지`와 `대응 없음`은 쓰지 않는다)

보존 검사: 통과 | 수정 없음
```

## 절대 규칙

- 대안은 조회 결과에 있는 틀에서만 만들고 출처 ID를 붙인다. 틀을 지어내지 않는다.
  틀의 일부만 쓰고 저자의 표현을 남기는 결합은 허용하되, 그렇게 했다고 밝힌다.
- 수치, 인용, 고유명사, 전문용어, 주장의 강도를 바꾸지 않는다. `may`→`shows`처럼
  확신도가 달라지는 교체를 하지 않으며, 틀의 동사가 원문의 강도와 다르면 쓰지 않는다.
- Phrasebank와 다르다는 이유만으로 고치지 않는다. 고칠 이유가 없으면 전부 `유지`가
  정답이다. 모든 문장을 틀에 맞추면 글이 상투적으로 수렴한다.
- 수정본에서 같은 틀과 같은 문두 표현을 반복하지 않는다.
- 논리·구성 문제를 발견하면 고치지 말고 표 아래에 한 줄로 알린다.
- 예시 문장의 소재를 저자의 글로 가져오지 않는다.

## 데이터 재생성

`data/Academic_phrasebank.md`를 고친 뒤 `python -I scripts/build_bank.py`를 실행한다.
원본 줄이 하나라도 빠지면 스크립트가 실패한다.
