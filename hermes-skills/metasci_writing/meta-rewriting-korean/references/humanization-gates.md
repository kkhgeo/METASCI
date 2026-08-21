# 한국어 리라이팅 신호와 보존 게이트

## 목적

이 파일은 `meta-rewriting-korean`의 보조 규칙이다. 한국어 초고에서 번역투·기계적
표현·모호한 연결을 찾고, 수정본이 원문의 사실·수치·인용 관계를 훼손하지 않았는지
검사한다.

이 파일은 다음을 하지 않는다.

- AI 저자성을 판정하지 않는다.
- 특정 문장 길이·능동/피동 비율·접속어 빈도를 인간 문체의 정답으로 삼지 않는다.
- `deep-rewrite`에서 원문 span만 고치도록 제한하지 않는다.
- 기계 검증 결과를 의미·논리·사실 검증으로 오인하지 않는다.

## 우선순위

1. 사실·주장·수치·인용과 그 **관계** 보존
2. 단락 기능과 논증 구조 개선
3. 사용자 개인 문체와 장르
4. 아래 표현 신호
5. 일반적인 자연스러움 선호

상위 원칙과 충돌하면 하위 신호를 적용하지 않는다.

---

## 모드별 적용

### `light-edit`

- 원문 문장 순서와 명제 구조를 유지한다.
- 발견된 국소 span을 중심으로 수정한다.
- 변경률 30% 이상은 WARN, 50% 이상은 ABORT할 수 있다.

### `deep-rewrite`

- 원문은 명제·근거·자료로 해체한 뒤 새 구조에서 다시 쓴다.
- span 규칙은 최종 국소 점검에만 쓴다.
- 문장 경계·순서·단락 구조·표현의 변경률에 상한을 두지 않는다.
- 문자열 변경률은 보고용 정보이며 PASS/ABORT 근거가 아니다.
- 보존 여부는 `protected ledger`와 proposition map으로 판단한다.

---

## 표현 신호

신호의 존재만으로 수정하지 않는다. `S1`은 강한 국소 오류 후보,
`S2`는 반복·밀집·문맥 결합 시 수정 후보, `S3`는 장르·취향 의존 선택지다.

| ID | 등급 | 신호 | 처리 원칙 |
|---|---|---|---|
| H1 | S1 | `되어진다`, `되어졌다` 등 명백한 피동 중첩 | 의미를 보존하며 단순화 |
| H2 | S1 | 연결어미 직후 불필요한 쉼표 | 삽입절·인용이 아니면 제거 |
| H3 | S1 | `~에서의`, `~으로부터의`, `~에로의` 등 기계적 이중 조사 | 자연스러운 절·조사로 재구성 |
| H4 | S2 | `~에 대하여`, `~를 통하여`, `~에 있어서` 밀집 | 반복 구간만 직접 조사·동사로 단축 |
| H5 | S2 | `가지고 있다`, `~에 의해`, `이루어지다` 반복 | 주체·행위를 확인할 수 있을 때 직접화 |
| H6 | S2 | 긴 좌향 관형절의 중첩 | 핵심 술어를 앞세우거나 문장 분할 |
| H7 | S2 | 추상 주어 + 만능 동사 | 실제 기능·행위자가 소스에 있을 때만 구체화 |
| H8 | S2 | 형식명사 `것·점·바·수·데` 밀집 | 정상 용례는 유지하고 반복 구간만 조정 |
| H9 | S2 | 해라체·합쇼체·해요체 혼용 | 문서 레지스터로 통일 |
| H10 | S2 | `~할 수 있을 것으로 판단/기대/예상된다` 헤징 중첩 | 근거 수준을 보존하며 한 단계로 축약 |
| H11 | S2 | 모든 문단의 동일 문장 수·동일 결말 | 정보 기능에 따라 구조를 달리함 |
| H12 | S3 | 불릿·헤딩·번호 목록·대구 반복 | 정보 구조일 수 있으므로 자동 제거 금지 |
| H13 | S2 | 문두의 `이러한 결과/과정/한계/맥락`이 모호하게 앞 문장 전체를 대용 | 정확한 선행 개념을 반복하거나 문장 통합 |
| H14 | S2 | 한 문장에 중간점 병렬 묶음이 여러 개 | 고정 결합·공식 명칭을 보호하며 일부 분산 |

### 신호 적용의 한계

- `~를 통해`, `~것이다`, 괄호, 직접 인용, 피동문은 단독으로 결함이 아니다.
- 100자 이상 장문을 만들기 위해 문장을 합치지 않는다.
- 동일 종결어미를 피하려고 의미가 다른 서술어를 쓰지 않는다.
- 보고서의 명사화·당위·번호 목록은 장르상 정상일 수 있다.
- Blueprint의 빈도·비율은 관찰값이며 목표값이 아니다.

---

## 보존 대장

### 보호 단위

숫자를 개별 문자열로만 보호하지 않는다. 가능한 한 다음 단위로 묶는다.

```text
[연결 대상] + [비교연산자/부호] + [값] + [불확도/범위] + [단위] + [귀속]
```

예:

- `처리군 A의 농도 = 10 ± 2 mg/L`
- `대조군 B의 농도 = 20 ± 3 mg/L`
- `p < 0.05`
- `변화량 −10%`
- `표 2의 2015년 값`

다음은 모두 보호 위반이다.

- 값의 대상 교환
- 단위 변경
- `+/-` 또는 음수 부호 변경
- `<, >, ≤, ≥, =` 변경
- 중복 값의 삭제·추가
- 인용을 다른 주장에 붙임
- 그림·표 번호를 다른 결과에 연결

### `deep-rewrite` 보존 절차

1. 원문에서 필수 명제와 보호 단위를 추출한다.
2. 권고본에서 각 명제와 보호 단위의 대응 위치를 찾는다.
3. 누락·추가·대상 교환·강도 변화를 기록한다.
4. 기계적으로 확인하지 못한 관계는 수동 감사 대상으로 남긴다.

---

## 결정적 게이트

`scripts/verify_korean_revision.py`는 다음을 검사한다.

| 게이트 | 검사 | `light` | `deep` |
|---|---|---|---|
| P0 | 문자열 변경률 | WARN/ABORT | 정보만 기록 |
| P1 | 수치표현·부호·비교연산자·단위의 다중집합 | ABORT | ABORT |
| P1b | 유사 문장 안에서 값-대상 결합 변경 | ABORT | ABORT 또는 수동검토 WARN |
| P2 | 직접 인용·인용키·법령·표/그림·각주 | ABORT/WARN | ABORT/WARN |
| P3 | 종결체 혼용 | WARN | WARN |
| P4 | H1~H14 신호의 증가 | WARN | WARN, 구조 판단에는 사용 금지 |
| P5 | 문장 터치율 | 보고 | 보고 |

기계 검증은 다음을 판정하지 못한다.

- 인용이 실제로 존재하거나 원 주장을 지지하는지
- 재작성된 명제가 의미상 완전히 동일한지
- 논증이 더 타당해졌는지
- 새로운 암묵적 인과가 생겼는지

따라서 통과 표시는 `PASS`가 아니라 **`MECHANICAL_PASS`**로 한다.

---

## 출처와 라이선스

분류 아이디어, span 기반 수정, 변경률 게이트, 보호 토큰 검사는 다음 프로젝트에서
선별·재구성했다.

- epoko77-ai, `im-not-ai`, commit `53e24e8f92cf344efcb812103f7c2b203e7efffc`
- https://github.com/epoko77-ai/im-not-ai

원 프로젝트는 MIT License로 배포된다.

Copyright (c) 2026 epoko77-ai

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

**Version**: 1.1.0
