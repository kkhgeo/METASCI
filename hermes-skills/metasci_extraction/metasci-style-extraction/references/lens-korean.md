# Korean Adaptation Guide (EXPERIMENTAL) — V/L/P lenses for Korean documents

How to run the three lenses on Korean formal documents (연구보고서, 정책보고서,
국문 논문). Read the three English lens files first — this file only states what
CHANGES for Korean. Mark every output card `[Korean — experimental]`.

## Scope

Formal institutional/academic Korean (격식체). Sections follow the document's own
structure (장·절, 서론/본론/결론, or 요약/현황/개선방안) — record the actual
structure; do not force IMRaD.

## V lens — what "characteristic vocabulary" means in Korean

Collect (per section, lean, evidence-gated):

1. **보고 서술어** (reporting predicates): 분석하였다, 검토하였다, 제시하였다,
   도출하였다, 파악하였다, 살펴보았다 — which dominate where.
2. **헤징 표현**: 것으로 판단된다, 것으로 보인다, 것으로 사료된다, 수 있다,
   가능성이 있다, 필요가 있다 (density itself → P).
3. **연결어**: 그러나, 한편, 이에 따라, 따라서, 아울러, 다만, 특히 — note
   sentence-initial vs medial habit.
4. **격식 명사구 / 정형구**: ~방안, ~체계, ~기반, 제도적 기반, 개선방안 도출,
   시사점 — the handful that recur as register.
5. Evidence gate applies unchanged: count with
   `python scripts/quant_check.py --strip-refs count --items cand.txt doc.pdf`
   (Hangul items match with attached particles automatically). Keep at Freq ≥ 2,
   record freq, `(rare-but-marked)` ≤ 2 items.

## L lens — frames and architecture in Korean

- **Section architecture**: paragraph-function sequence per 장/절 (예: 배경 →
  현황 → 문제점 → 개선방향 → 시사점). Absences are style (예: 요약문 없음).
- **문장 프레임** with [SLOT]s, anchor-validated like English:
  - 배경: "[대상]은 [기능]하는 제도이다."
  - 분석: "[자료]를 대상으로 [방법]을 실시하였다."
  - 판단: "[결과]인 것으로 판단된다/보인다."
  - 제언: "[조치]가 필요하다." / "[방안]을 추진할 필요가 있다."
- Anchor counting works unchanged (`것으로 판단된다` is a countable anchor).
  Recurrent (≥2) vs Singleton status required.

## P lens — Korean profile dimensions

Measured (script auto-detects Korean; report as approximate, ±20% bands):

```bash
python scripts/quant_check.py --strip-refs profile doc.pdf
# lang=ko: eojeol tokens, ending-split sentences, 한국어 헤징/1k, 되다·어지다 피동/1k
```

- **문장 길이**: avg eojeol per sentence (measured).
- **헤징 밀도**: hedges/1k (measured) + band.
- **피동 밀도**: passive/1k (measured; 되다/어지다 근사) — report as anchor, not exact.

Reading judgments (replace English dims):

| dim | what to report |
|-----|----------------|
| **종결 유형** | …다 서술형 / …함·…음 명사형 종결 / 혼합 — and where each is used (본문 vs 요약 vs 표) |
| **격식 수준** | 격식체 일관성; 구어체 혼입 여부 |
| **주어 처리** | 무주어 관행 / "본 연구는" / "본고는" 등 |
| **인용 방식** | 각주형 / 괄호형(저자, 연도) / 본문 언급형 비율 감 |
| **한자어 밀도** | high/med/low 감(측정 불가) |
| **does NOT do** | 예: 1인칭 없음, 수사의문 없음, 영문 병기 없음 |
| **distinctive moves** | 1-3 |

## Cards & synthesis

Same card/profile formats as English (freq-stamped V items, anchored L frames,
measured+judged P table). In `style_profile.md`, add `[Korean — experimental]`
next to the title and keep Korean and English corpora in SEPARATE profiles —
never aggregate across languages.
