# Phrase Extraction — 점검할 표현 고르기

## 목적

사용자 문장에서 **"실제 논문에 쓰이는가"를 물어볼 가치가 있는 표현**만
골라낸다. 문장 전체나 불용어 조각을 검색하면 매칭이 안 되거나 무의미하므로,
변별력 있는 단위로 쪼갠다.

---

## 1. 뽑을 것 (우선순위 순)

1. **특징적 연어 (collocation)** — 학술적 판단이 갈리는 명사+명사, 동사+명사,
   형용사+명사 조합.
   예: `aggregate disruption`, `drive mineralization`, `pronounced increase`
2. **다어절 전문표현 (technical multi-word term)** — 그 분야의 용어.
   예: `soil organic carbon dynamics`, `dissolved organic matter`
3. **수사적 정형구 (rhetorical formula)** — 학술 글의 관용 표현. NNS가 자주
   비틀어 쓰는 지점.
   예: `to the best of our knowledge`, `these results suggest that`,
   `plays a pivotal role in`, `in line with previous studies`
4. **의심스러운 직역투 (suspect calque)** — 뜻은 통하지만 어색해 보이는,
   비원어민이 만들어냈을 법한 조합. **가장 점검 가치가 높다.**
   예: `carbon liberation by frost`, `make an important role`,
   `depth-wise decreasing tendency`

---

## 2. 뽑지 말 것

- 순수 기능어 조각: `of the`, `in which`, `it is`
- 고유명사·기관명·지명: `Kastanozem`, `Inner Mongolia`
- 수치·단위·통계 토큰: `12.3 mg/g`, `p < 0.05`, `N = 120`
- 인용 표기: `(Six et al., 2004)`
- 한 단어 일반 명사/동사 (검색 변별력 없음): `carbon`, `showed`
  (단, 그 단어의 **용법**이 의심되면 최소 연어로 확장해 뽑는다:
  `showed` → `showed a decreasing trend`)

---

## 3. 표현 경계와 변형 정하기

- **길이:** 2~6단어. 너무 길면(문장급) 매칭 실패 → 핵심 2~4단어로 축약.
- **가지치기:** 관사·소유격은 제거하되 핵심 내용어를 남긴다.
  예: `the physical disruptions of soil aggregates` → `aggregate disruption`
- **표기 변형 후보:** 의미를 바꾸지 않는 단수·복수, 영미 철자, 하이픈·대시,
  굴절형을 별도로 적는다. 표기 변형의 검색 결과는 같은 표현군으로 묶되 실제
  일치 형태를 보고한다.
  예: `freeze–thaw cycle` → `freeze-thaw cycles`, `freeze thaw cycle`
- **의미 대안 후보:** 어휘나 통사 구조를 바꾸는 후보는 표기 변형과 분리한다.
  예: `carbon liberation by frost` → `frost-induced carbon release`,
  `carbon release during freeze-thaw`
- **의미 보존:** 긴 표현을 축약할 때는 원문의 핵심 술어와 논항 관계가 유지되는지
  확인한다. 검색이 잘된다는 이유만으로 더 일반적인 다른 의미로 바꾸지 않는다.

---

## 4. 개수 조절

- 한 문장: 보통 1~3개.
- 한 단락: 보통 3~8개. **"의심 직역투"를 최우선**으로, 확실히 표준인 흔한
  표현은 1~2개만 샘플로.
- 상한: 단락당 12개. 초과 시 의심도 높은 순으로 12개만.

---

## 5. 각 표현에 부여할 메타

추출 시 표현마다 아래를 정해 Agent Attest에 넘긴다:

```
{
  phrase: "aggregate disruption",
  sentence: "...the observed increase reflects aggregate disruption...",
  suspicion: "low" | "medium" | "high",   // 직역투 의심도
  orthographic_variants: ["aggregate disruptions"],
  alternative_candidates: ["aggregate breakdown", "disruption of aggregates"]
}
```

`orthographic_variants`는 같은 표현군의 표기 차이로, `alternative_candidates`는
의미가 같은지 별도 검증해야 하는 표현으로 처리한다. `suspicion=high`이면 미확인
시 대안 검색을 더 적극적으로 수행한다.
