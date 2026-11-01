# Changelog — meta-proofreading-korean

## 0.2.0 — 2026-08-19 (복귀판)

2026-08-19 오전 `legacy-skills/`로 퇴역했다가 같은 날 검토·개선 후 복귀.
manual/은 meta-rewriting-korean에 사본으로 남고 **정본은 이 스킬로 복귀**
(manual/INDEX.md 말미에 명시).

- 트리거를 패널 지명("한국어 메타교정" 등)으로 한정 — 일반 "국문 교정"과
  단락 리뷰는 meta-rewriting-korean과 충돌하지 않게 그쪽으로 양보 (영어쌍
  meta-proofreading ↔ meta-rewriting과 같은 규약)
- Blueprint 참조 4곳(meta-mywriting-korean, 퇴역)을
  meta-rewriting-korean `references/blueprint.md`로 갱신
- 세션 파일을 `proofreader-korean-session.json`으로 분리 — 영어판과 같은
  경로를 쓰던 충돌 제거
- `L2_structural_integrity.md`의 영어판 전용 경로(`sections/04_results.md`
  등) 참조를 인라인 서술로 대체 — 이 스킬 안에서 열 수 없는 포인터였음
- allowed-tools에서 `Task`(Agent의 옛 이름)·`Edit`(미사용) 제거
- Mode 3(단락)에 meta-rewriting-korean과의 경계 명시 — 패널 심의가 값어치를
  할 때만

## 0.1.0 — 2026-08 (초판)

명세성 3층 심의 교정. Kim(2026) QWK 측정에 근거한 층별 판정 권한
(L1 결정 / L2 과반 / L3 판정 금지), 국립국어원·법제처·KCI 출처 대장,
과잉 규범 3종 차단.
