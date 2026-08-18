# Changelog — meta-rewriting-korean

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
