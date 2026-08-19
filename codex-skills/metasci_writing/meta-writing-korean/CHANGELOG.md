# Changelog — meta-writing-korean

## 1.0.0 — 2026-08-19

신규. meta-writing 1.2.1(영어판)의 절차 — My Data/Knowledge 구분, 5-Loop
탐색, Phase 3.5 개고, Phase 4 인용 검증(Step 3 오귀속 검증 포함) — 를
국문 섹션 작성으로 이식.

**설계 결정 (사용자 확정):**
- **규범은 사본이 아니라 상대 경로 공유** — meta-rewriting-korean의
  manual/·report-register·anti-ai-patterns·게이트 스크립트, meta-writing의
  writing_template·parallel-processing·citation-and-verification을 `../`로
  읽는다. 같은 매뉴얼 사본 증식을 막기 위한 선택이며, 대가로
  **meta-rewriting-korean·meta-writing과 나란히 설치**가 요구된다(SKILL.md
  상단에 명시, 경로 불통 시 안내하고 지어내지 않기).
- **출력은 국문 단독** — 번역 블록 없음.
- **인용 양식은 레지스터별 분기** — 학술=APA 7, 보고서=국문 관행
  ((저자, 연도) · 법령 「」 · (표 N) 지시).

**새로 쓴 것:** `references/section_guides_korean.md` — 국문 공통 문체
기본값(두괄식·종결체 통일·접속어 기본값 미사용·이중 피동 금지), 생성 시
AI 패턴 자기검열, 국문 보고 동사 레인 표, 시제 표, 학술(서론/방법/결과/
고찰/결론)·보고서(현황→문제→방안 구조, 개조식 한정, 명사 나열 금지)
섹션별 지침. 값의 출처는 파일 말미에 기록.

**영어판과의 차이:** register(학술/보고서)가 Phase 1 필수 항목;
`language` 옵션 없음; Phase 3.5에 verify_korean_revision.py 결정적 게이트;
생성 자기검열(anti-AI를 리뷰가 아니라 생성 제약으로).
