# 출처와 동기화 규칙

이 폴더와 상위 `references/`의 파일들은 2026-08-19에 퇴역한 두 스킬에서
흡수한 **정본**이다. 원 스킬들은 `legacy-skills/`로 이동했고 더 이상
갱신되지 않는다 — 즉 이 사본이 이제 유일한 관리본이며, 수정은 여기서 한다.

## 이 폴더 (`manual/`) — meta-proofreading-korean에서

| 파일 | 층 | 판정 권한 |
|---|---|---|
| `L1_sentence_rules.md` | L1 | **결정적** — 문장·번역투·피동·호응·간결 |
| `L1_paragraph_rules.md` | L1 | **결정적** — 단락 길이·주제·두괄식·접속어 상한 |
| `L1_quantitative_integrity.md` | L1 | **결정적** — 수치·백분율·유효숫자 (수치 있을 때만 로드) |
| `L2_argument_rubric.md` | L2 | **준거** — 논거·반론 대응·통일성 (확정 아님) |
| `L2_structural_integrity.md` | L2 | **단락 단위에서는 판정 불가** — 아래 참조 |
| `L3_style_cohesion.md` | L3 | **선택** — 후보만, 판정 없음 |
| `sources.md` | — | 지적에 출처를 붙일 때 |

**`L2_structural_integrity.md`의 지위.** 질문 사슬·초록↔본문 일치는 양쪽
섹션이 다 있어야 판정된다. 단락 스킬인 meta-rewriting-korean은 이 파일로
판정하지 않는다 — 의심되면 "판정 불가 — 섹션 검토 필요"로 보고한다.
파일을 동봉해 둔 것은 지침의 완전 보존과, 사용자가 섹션 검토를 요청하는
경우를 위해서다.

## 상위 `references/` — 출처별

| 파일 | 출처 (퇴역/유지) | 용도 |
|---|---|---|
| `blueprint.md` | meta-mywriting-korean (퇴역) `my-style-blueprint.md` | C안 개인 문체. 소스: EIA리뷰 Vol.1 등 사용자 글 추출 |
| `anti-ai-patterns.md` | meta-mywriting-korean (퇴역) | 진단 신호 (Stage 2 항상 로드) |
| `humanization-gates.md` | meta-mywriting-korean (퇴역) | H1–H14 신호·span 규칙·결정적 게이트. MIT 라이선스 고지 포함 — 삭제 금지 |
| `report-register.md` | **research-report-writer (유지, 프로필 플러그인)** `tone-adjustment.md` | 보고서 레지스터. **유일하게 상류가 살아있는 파일** — 상류가 바뀌면 재복사, 직접 수정 금지 |

`scripts/verify_korean_revision.py`는 meta-mywriting-korean에서 왔고 그
테스트(`tests/`)는 `legacy-skills/meta-mywriting-korean/tests/`에 남아 있다.

## 원 스킬에서 의도적으로 가져오지 않은 것

- meta-proofreading-korean의 멀티에이전트 패널 하니스(agents/, harness/,
  config/) — 원고 전체용 고비용 파이프라인. 단락 리뷰에는 과하다.
- meta-mywriting-korean의 4-Phase Gap Analysis 출력 형식 — 이 스킬의
  ①–⑤ 블록이 대체한다.
- meta-mywriting-korean의 `source_materials/`(KEI2022·KimKH2020 추출) —
  blueprint.md에 이미 증류되어 있음. 원자료는 legacy-skills에 보존.
