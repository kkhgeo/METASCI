# 한국어 Humanization 정밀 신호와 보존 게이트

## 목적과 경계

이 파일은 개인 Blueprint를 대체하지 않는다. 한국어 초고에서 고신뢰 문체 이상 신호를
찾고, 리라이팅이 원문의 사실·수치·인용·구조를 훼손하지 않았는지 확인하는 보조 규칙이다.
신호의 존재를 AI 저자성의 증거로 제시하지 않는다.

적용 우선순위는 다음과 같다.

1. 사실·주장·수치·직접 인용 보존
2. 사용자 개인 Blueprint와 문서 장르
3. 아래 고신뢰 신호
4. 일반적인 자연스러움 선호

Blueprint와 충돌하면 2가 3보다 우선한다. 정책보고서의 명사화, 피동, 당위 표현, 번호
목록은 그 자체로 결함이 아니다.

## 심각도

| 등급 | 의미 | 처리 |
|---|---|---|
| S1 | 독립적으로 강한 번역투·기계적 오류 신호 | 보호 span이 아니면 수정 후보 |
| S2 | 반복·밀집하거나 다른 신호와 겹칠 때 문제 | 문서 빈도와 장르를 확인한 뒤 수정 |
| S3 | 취향·장르 의존성이 큼 | 자동 수정하지 않고 선택지만 제시 |

## 선별 신호

| ID | 등급 | 신호 | 탐지·처방 |
|---|---|---|---|
| H1 | S1 | 이중 피동 `되어진다`, `되어졌다` | `된다`, `되었다` 등 문맥에 맞게 단순화 |
| H2 | S1 | 연결어미 뒤 불필요한 쉼표 `~지만,`, `~는데,`, `~하며,` | 인용·삽입절이 아니면 쉼표 제거 |
| H3 | S1 | 기계적 이중 조사 `~에서의`, `~에로의`, `~으로부터의` | 조사를 풀어 자연스러운 관형 구조로 수정 |
| H4 | S2 | `~에 대하여/대해서`, `~를 통하여/통해`, `~에 있어서` 밀집 | 한두 번은 허용; 반복 시 직접 조사·동사로 단축 |
| H5 | S2 | `가지고 있다`, `~에 의해`, `이루어지다` 반복 | 주체와 행위가 분명하면 직접 동사 사용 |
| H6 | S2 | 긴 좌향 관형절이 3중 이상 중첩 | 핵심 주장 앞에서 문장을 분리하되 인용 결합 유지 |
| H7 | S2 | 추상 주어와 만능 동사 결합 | 실제 행위자·기능을 확인할 수 있을 때만 구체화 |
| H8 | S2 | `것·점·바·수·데` 형식명사 밀집 | 정상 당위 표현은 유지하고 반복 구간만 구체화 |
| H9 | S2 | 해라체·합쇼체·해요체 혼용 | 사용자 지정 또는 Blueprint의 종결체로 통일 |
| H10 | S2 | `~할 수 있을 것으로 판단/기대/예상된다` 중첩 | 근거 수준을 보존하며 헤징 한 단계만 남김 |
| H11 | S2 | 모든 문단의 동일 문장 수·동일 결말 | 필자 리듬을 지우지 않는 범위에서만 분산 |
| H12 | S3 | 불릿·헤딩·번호 목록·대구의 반복 | 정보 구조일 수 있으므로 자동 제거 금지 |
| H13 | S2 | 문두의 `이·그·저·이러한·그러한 + 추상명사`가 앞 문장을 대명사처럼 다시 받음 | `이 과정에서`, `이 고정성은`, `그 결과`, `이러한 한계` 등을 기록한다. 앞 문장과 통합하거나 정확한 개념을 직접 반복할 수 있으면 지시 대용구를 제거한다 |
| H14 | S2 | 한 문장에 중간점 병렬 묶음이 2개 이상이거나 중간점이 3개 이상 | 고정 결합·공식 명칭·직접 인용은 보호하고, 나머지는 쉼표나 `및`, `와/과`로 풀거나 문장을 분리한다. 사용자 요청이 있으면 신규 중간점은 만들지 않는다 |

## Span 기반 수정

1. 발견마다 `(ID, severity, 원문 span, 위치, 처방)`을 남긴다.
2. 발견된 span만 Dim 7 수정 대상으로 삼는다.
3. 수치·단위·날짜·고유명사·직접 인용·법령 조문·필수 전문용어를 보호한다.
4. S2는 같은 문단에서 반복되거나 다른 신호와 겹칠 때만 수정한다.
5. 수정으로 새로운 주장, 수치, 인용, 평가를 만들지 않는다.
6. 이미 자연스러우면 조기 종료하고 수정하지 않는다.
7. 중간점은 삭제 개수 자체를 목표로 삼지 않는다. 병렬 항목의 의미와 층위를 보존하면서
   한 문장에 여러 묶음이 겹치는 경우만 우선 정리한다.

### H13 적용 규칙

- `과정·결과·한계·상황·관점·맥락·고정성·구조·방식·문제·현상·특성·점·측면`처럼
  앞 문장 전체를 대신하는 추상명사를 우선 탐지한다.
- 한 단락에 2회 이상 나타나거나, 문두에서 바로 앞 문장을 받거나, 지시어를 빼도 지시 대상이
  분명하면 수정한다. 단순히 `그 결과`로 바꾸는 것은 같은 패턴의 치환이므로 개선으로 세지 않는다.
- 우선순위는 ① 앞 문장에 인과·조건절로 통합, ② 핵심 개념을 직접 반복, ③ 지시어만 삭제 순이다.
- 법령·인용의 정확한 귀속, 장거리 참조의 명료성, 핵심 개념의 명시적 회귀를 위해 꼭 필요하면
  유지하고 이유를 기록한다. 지시어 자체를 금지어로 취급하지 않는다.

## 결정적 게이트

`scripts/verify_korean_revision.py`는 다음을 코드로 확인한다.

- P0 변경률: 30% 이상 WARN, 50% 이상 ABORT
- P1 보호 토큰: 수치·직접 인용·각주·표/그림 참조의 추가·삭제
- P2 구조: 마크다운 헤딩과 각주 정의 보존
- P3 격식: 최종본의 종결체 혼용
- P4 신호: H1–H5·H10·H13·H14의 before/after 빈도
- P5 문장 터치율: 보고 전용

ABORT는 후보를 채택하지 않는다는 뜻이다. WARN은 자동 PASS로 바꾸지 않고 1회 보수적
재수정 후 남은 경고를 사용자에게 보여준다.

## 출처와 라이선스

분류 아이디어, span 기반 수정, 변경률 게이트, 보호 토큰 검사는 다음 프로젝트에서 선별·
재구성했다.

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
