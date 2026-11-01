---
name: meta-review-council
description: >
  Review the reasoning of an academic paragraph or section with a three-model
  council: Claude, Codex, and Gemini review independently through their logged-in
  CLIs, rank each other's anonymized reviews, and the current session synthesizes
  the verdict as chairman. Needs no API keys or extraction files. Use when the user
  says "council 리뷰", "카운슬 리뷰", "모델 회의", "세 모델로 리뷰", or
  "meta-review-council". Plain "리뷰해줘" goes to meta-review; sentence correction
  goes to meta-proofreading.
---

# Meta-Review-Council

세 모델이 글의 논리와 주장을 독립적으로 검토하고 서로를 익명으로 평가한 뒤, 현재
세션이 의장으로 결론을 낸다. 문법과 문체 교정은 하지 않는다. 설명은 한국어로 쓴다.

호출, 익명화, 순위 집계는 `scripts/council.py`가 맡는다. 이 단계를 직접 흉내 내지 않는다.

## 준비

- 필요: Python 3.9 이상, 로그인된 `claude`, `codex`, `gemini` CLI. 파이썬 패키지와 API
  키는 필요 없다.
- Codex: `npm install -g @openai/codex` 후 `codex login`
- Gemini: `npm install -g @google/gemini-cli` 후 `gemini` 실행해 Google 로그인
- 구독 사용량을 쓴다. 기본 구성은 모델당 2회 호출이다.
- Codex 샌드박스 안에서는 모델 호출이 멈추거나 실패한다. `council.py`는 샌드박스 밖에서
  실행한다. 승인을 요청하거나 `codex --sandbox danger-full-access`로 세션을 시작한다.

## 절차

1. 검토할 글과 문맥(섹션, 분야)을 확인한다. 글이 없으면 요청한다.
2. 글을 작업 폴더의 `_council/<짧은이름>/draft.txt`에 UTF-8로 저장한다.
3. 스킬 폴더 기준으로 실행한다. Bash 제한시간은 15분으로 둔다.

   ```bash
   python -I scripts/council.py run --draft <draft.txt> --out <세션폴더> --context "<문맥>"
   ```

4. 실패 처리: 2개 모델 이상이 답하면 계속하고, 빠진 모델을 결과 첫 줄에 적는다. 1개
   이하이면 중단하고 오류를 그대로 보고한다.
5. `<세션폴더>/report.md`를 전부 읽고 의장 판단을 내린다.
6. 수정본을 만들었으면 원문과 함께 저장해 보존 검사를 실행한다. 실패하면 5단계로
   돌아가 해당 문장을 원문 쪽으로 되돌리고, 통과할 때까지 반복한다.

   ```bash
   python -I scripts/check_preservation.py <세션폴더>/draft.txt <세션폴더>/revised.txt
   ```

## 의장 판단

- 지적마다 원문의 실제 문구와 대조해 맞는지 확인한다. 다수 의견이나 순위 1위라도
  틀렸으면 기각하고 이유를 쓴다.
- 합의와 이견을 나눈다. 이견은 평균을 내지 말고 근거가 강한 쪽을 고른다.
- 수치, 인용, 고유명사는 원문을 유지한다. 없는 근거는 `[근거 필요]`로 표시한다.
- 글에 문제가 없으면 없다고 쓴다.

## 출력

```markdown
참여: Claude, Codex, Gemini (빠진 모델과 이유)

### 결론
(가장 중요한 문제와 판단 2~3문장)

### 지적 사항
| # | 심각도 | 원문 | 문제 | 지지 모델 | 의장 판단 | 수정 방향 |
|---|---|---|---|---|---|---|

### 모델 간 이견
(쟁점별로 입장과 의장의 선택)

### 상호 평가 순위
| 순위 | 모델 | 평균 순위 |
|---|---|---:|

### 수정본
(최소 수정본. 바뀐 부분은 **굵게**. 수정이 필요 없으면 생략)

보존 검사: 통과 | 수정 없음
세션 파일: <세션폴더>
```

## 규칙

- 글은 OpenAI와 Google로도 전송된다. 사용자가 이 구성을 선택했으므로 매번 묻지는
  않지만, 비공개 표시가 있거나 개인정보가 보이면 실행 전에 멈추고 확인한다.
- 원고 파일을 직접 수정하지 않는다.
- 기준에 없는 이유로 문제를 발견하면 끝에 새 규칙 하나를 제안하고 승인을 받는다.
