# Changelog — meta-rewriting-korean

## 1.1.0 — 2026-08-22

기본 작업을 보수적 3안 교정에서 **비판적 구조 리라이팅**으로 전환했다.

- 기본 모드를 `deep-rewrite`로 지정하고 `light-edit / review-only / compare`를 분리.
- 입력 단락을 문장 집합이 아니라 주장·근거·자료 집합으로 취급하도록 역할 재정의.
- 여러 단락이 입력되면 첫 단락만 처리하던 제한 제거. 파일 작업 시 제목·앞뒤 단락을
  읽어 맥락을 판단하도록 변경.
- 사실·수치·인용뿐 아니라 값의 대상, 부호, 비교연산자, 불확도, 단위,
  주장 강도를 기록하는 protected ledger 추가.
- 명제 지도(proposition map)와 문장별 처분 체계
  `KEEP/TRIM/MERGE/SPLIT/MOVE/REWRITE/DELETE/EVIDENCE NEEDED` 추가.
- 문법적으로 깨끗한 문장도 구조·위치·리듬에 따라 삭제·이동·재작성할 수 있도록 변경.
- 문장 수정 전에 새 순서·삭제·통합·분할·신규 연결을 정하는 수술 계획 추가.
- Rewrite Brief에서 백지 재작성하여 원문 문장 배열에 대한 앵커링을 차단.
- A/B/C 3안 강제 출력을 폐지하고 단일 권고본을 기본값으로 변경.
- `결과만 / 간단히 / 상세히 / 비교` 출력 지시를 명시적으로 분기.
- L1의 문법·의미 오류와 문단 길이·두괄식·접속어 수 등 장르 의존 휴리스틱을 분리.
- 독립 에이전트를 실제로 실행하지 않은 L2 판단을 패널·다수결로 표현하지 않도록 변경.
- anti-AI·Blueprint·보고서 빈도표를 강제 목표가 아닌 선택적 참고로 격하.
- `deep-rewrite`에서는 변경률을 PASS/ABORT 근거로 사용하지 않음.
- 사후 감사를 내용·논리·톤·맥락·리듬·기계 보존으로 분리.

### 검증기 1.1.0

- `--mode deep|light` 추가. deep 모드에서 변경률은 보고만 하고 차단하지 않음.
- 숫자 집합 비교를 폐지하고 부호·비교연산자·값·범위·불확도·단위를 포함한
  수치표현의 다중집합을 검사.
- 유사 문장 내 값-대상 결합을 비교하여 `A=10/B=20 → A=20/B=10` 교환 탐지.
- 단위, p-value 비교연산자, 음수 부호, 중복 수치 삭제를 ABORT로 탐지.
- 인용·직접 인용·법령명·표/그림·각주의 반복 횟수까지 보존.
- 성공 판정을 `PASS`에서 `MECHANICAL_PASS`로 변경하고 의미·사실 검증 미수행을 명시.
- 회귀 테스트 9개 추가.

## 1.0.1 — 2026-08-19

description에 국문 섹션 생성 라우팅 추가(meta-writing-korean 신설). 본문 변경
없음. meta-writing-korean이 이 스킬의 references/·scripts/를 상대 경로로
읽으므로 나란히 설치되어야 한다.

## 1.0.0 — 2026-08-19

신규. meta-rewriting 2.3.0(영어판)의 4단계 구조 — 입력 → 원리 로드 →
진단(①②③) → 대안(④⑤) — 를 한국어 레지스터로 이식.

**흡수한 스킬과 자산** (원 스킬들은 `legacy-skills/`로 퇴역):

- `meta-proofreading-korean` → `references/manual/` 7개 파일 (L1 결정
  규칙 · L2 논증 준거 · L3 문체 · sources). 층 권한 표기([L1 · 확정] /
  [L2 · 준거] / [L3 · 선택])와 "못 한다고 말하지, 통과한 것처럼 굴지
  않는다" 규율 계승. 멀티에이전트 패널 하니스는 흡수하지 않음.
- `meta-mywriting-korean` → `references/blueprint.md`(C안 개인 문체),
  `references/anti-ai-patterns.md`, `references/humanization-gates.md`
  (H1–H14 + span 규칙), `scripts/verify_korean_revision.py`(C안 결정적
  게이트).
- `research-report-writer`(유지) → `references/report-register.md`로 톤
  지침만 공유. 보고서/학술 레지스터 분기가 Stage 1 질문이 됨.

**영어판과의 차이:** 국문 입출력이므로 번역 블록 없음; C안이 "원칙
재구성"이 아니라 "내 문체안"(원칙 재구성은 B안이 맡음); 레지스터 질문
(학술/보고서)이 섹션 질문을 겸함; C안에 결정적 게이트 스크립트.
