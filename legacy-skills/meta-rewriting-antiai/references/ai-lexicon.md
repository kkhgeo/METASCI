# AI Lexicon — AI 과잉 어휘 및 패턴 데이터베이스

> PHASE 1 (AI Fingerprint Scan) 시작 전 반드시 읽는다.

---

## 1. AI Excess Words (고빈도 AI 과잉 단어)

Kobak et al. (2024/2025, PNAS) 15.1M PubMed 초록 분석 + Gray (2024) 37M 논문 분석 기반.
2022→2024 빈도 급증한 단어 중 학술 글에서 탐지 시그널이 강한 것들.

### Tier 1: Critical (극단적 빈도 비율, 발견 시 즉시 교정)

| AI Word | Frequency Ratio | Replacement Options |
|---------|----------------|---------------------|
| delve(s) | Extreme (near-zero → ubiquitous) | examine, investigate, explore, analyze |
| showcasing | Very high | demonstrating, illustrating, presenting, revealing |
| underscores | Very high | highlights, emphasizes, confirms, supports |
| intricate | +117% (2022→2023) | complex, detailed, elaborate, fine-grained |
| meticulous | +59% | careful, rigorous, thorough, systematic |
| commendable | +83% / 9.8× in reviews | praiseworthy, notable, valuable, strong |
| pivotal | High excess | critical, essential, key, central, important |
| comprehensive | High excess | extensive, thorough, broad, wide-ranging |
| notably | High excess | in particular, especially, specifically |
| tapestry | Very high (non-scientific) | framework, network, system, interplay |
| testament | Very high (non-scientific) | evidence, indication, demonstration, proof |
| landscape | High excess (metaphorical) | field, domain, area, context |
| realm | High excess (metaphorical) | domain, field, area, sphere |

### Tier 2: Major (뚜렷한 빈도 증가, 동일 단락 2+ 출현 시 교정)

| AI Word | Category | Replacement Options |
|---------|----------|---------------------|
| illuminate | Verb | clarify, reveal, show, elucidate |
| harness | Verb | use, employ, apply, utilize |
| navigate | Verb (metaphorical) | address, manage, handle, deal with |
| elevate | Verb | improve, enhance, increase, raise |
| unveil | Verb | reveal, show, disclose, present |
| foster | Verb | promote, encourage, support, facilitate |
| bolster | Verb | strengthen, reinforce, support |
| groundbreaking | Adjective | novel, innovative, pioneering, new |
| vibrant | Adjective | active, dynamic, lively, diverse |
| profound | Adjective | significant, substantial, deep, considerable |
| innovative | Adjective | novel, new, creative, original |
| crucial | Adjective | important, essential, critical, vital |
| seamlessly | Adverb | smoothly, efficiently, effectively |
| profoundly | Adverb | significantly, substantially, greatly |
| inherently | Adverb | fundamentally, intrinsically, by nature |

### Tier 3: Minor (단독으로는 문제 없지만 Tier 1-2와 공기 시 교정)

| AI Word | Category | Note |
|---------|----------|------|
| furthermore | Transition | 단독 OK, 단락당 1회 초과 시 교정 |
| moreover | Transition | furthermore와 교체 사용 시 교정 |
| additionally | Transition | 문장 시작 시 교정 |
| in addition | Transition | additionally와 유사 패턴 |
| it is worth noting that | Phrase (4.6× excess) | 삭제 또는 직접 진술로 전환 |
| plays a crucial role | Phrase | "is important for" 또는 구체적 역할 서술 |
| a wide range of | Phrase | "various", "many", "diverse" 또는 구체화 |
| in the context of | Phrase | "in", "for", "regarding" 또는 삭제 |

---

## 2. Co-occurrence Patterns (공기 패턴)

**개별 단어보다 공기 패턴이 훨씬 강한 AI 시그널이다** (Gray, 2024).

### Critical Co-occurrences (같은 단락 내 동시 출현 시 반드시 분산)

| Pair | Frequency Increase | Action |
|------|--------------------|--------|
| intricate + meticulous | 7× | 최소 1개 교체 |
| intricate + notable | 4× | 최소 1개 교체 |
| comprehensive + pivotal | High | 최소 1개 교체 |
| delve + intricate | High | 반드시 둘 다 교체 |
| showcasing + underscores | High | 최소 1개 교체 |
| innovative + groundbreaking | High | 1개만 유지, 다른 것 교체 |
| crucial + pivotal | High | 동의어 중복 — 1개만 유지 |
| meticulous + comprehensive | High | 최소 1개 교체 |
| foster + enhance | High | 최소 1개 교체 |
| notably + importantly | High | 같은 단락에서 1개만 사용 |

### Co-occurrence 검사 규칙

1. **같은 단락**에서 Tier 1 단어 2개 이상 → Critical
2. **같은 문장**에서 Tier 1-2 단어 2개 이상 → Critical
3. **인접 단락**에서 동일 AI 단어 반복 → Major
4. **전체 텍스트**에서 Tier 1 단어 5개 이상 (고유 종류) → Major

---

## 3. Copula Avoidance Patterns (Copula 회피)

AI는 "is/are"를 피하고 대용 구문을 과다 사용한다.
Wikipedia Signs of AI Writing (2025): 2023년 이후 학술 글에서 is/are 사용 10%+ 감소.

| AI Pattern | Natural Alternative |
|------------|---------------------|
| serves as a | is |
| stands as | is |
| marks the | is |
| represents | is (단순 동일 관계 시) |
| features | has |
| offers | has, provides |
| boasts | has (홍보 톤 제거) |
| constitutes | is, makes up |
| embodies | is, reflects |

### 교정 규칙

- 모든 copula 회피를 "is/are"로 바꾸지 않는다
- **같은 단락에서 2회 이상** 출현 시 1개를 자연스러운 copula로 복원
- 수사적 효과가 있는 경우 유지 가능 (판단 근거 기록)

---

## 4. Model-Specific Signatures (모델별 시그니처)

### GPT-4o / GPT-4o-mini
- Downtoners 과다: barely, nearly, slightly, somewhat
- Clausal coordination 회피
- Em dash 극도로 과다 (GPT-3.5 대비 ~10×)
- "delve" 최다 사용 모델

### Claude (Anthropic)
- 문장 우아함 추구 — 지나치게 polished된 문체
- Em dash 과다 (GPT보다는 적지만 인간보다 많음)
- Hedging 표현은 비교적 사용하나 booster 부족
- 부드러운 전환 과다 (문장 간 연결이 지나치게 매끄러움)
- "nuanced", "multifaceted", "noteworthy" 선호

### DeepSeek
- Nouns, pronouns, coordinating conjunctions 선호
- 짧은 문장 경향
- "here's a breakdown" 패턴

### LLaMA
- 모델 크기↑ → negative emotions↑
- GPT와 다른 POS 분포
- 다른 모델 훈련 데이터로 탐지 시 오분류 위험

### 교정 시 주의

meta-rewriting-antiai는 Claude가 실행하므로, **Claude 자체 시그니처를 의식적으로 교정**해야 한다:
- 지나치게 매끄러운 문장 연결 → 의도적 단절 삽입
- Booster 부족 → 적극적 booster 삽입
- "nuanced", "multifaceted" → 구체적 서술로 대체

---

## 5. High-Signal Phrases (고시그널 구문)

빈도 비율이 극단적으로 높은 구문들. 발견 시 반드시 교정.

| Phrase | Excess Ratio | Action |
|--------|-------------|--------|
| "gain a valuable" | 62× | 삭제 또는 구체적 이점 서술 |
| "understand the behavior" | 61× | 구체적 행동/현상으로 대체 |
| "broad implications" | 61× | 구체적 함의 서술 |
| "a prominent figure" | 61× | 구체적 역할/직함 사용 |
| "study highlights the importance" | 60× | "This study shows..." 또는 구체적 발견 서술 |
| "a significant turning point" | 60× | 구체적 변화 서술 |
| "today in the digital age" | 59× | 삭제 (불필요한 시대 언급) |
| "a beacon of hope" | 58× | 삭제 (비학술적 수사) |
| "pave the way for the future" | 58× | 구체적 향후 연구 방향 서술 |
| "it is worth noting that" | 4.6× | 삭제하고 직접 진술 |
| "in the realm of" | High | "in" 으로 대체 |
| "at the forefront of" | High | "leading" 또는 삭제 |
| "a testament to" | High | "evidence of", "demonstrates" |

---

## 6. Scanning Algorithm

PHASE 1에서 다음 순서로 스캔한다:

### Step 1: Word-Level Scan
```
For each paragraph:
  1. Tier 1 단어 출현 수 카운트
  2. Tier 2 단어 출현 수 카운트
  3. High-Signal Phrase 출현 체크
  4. Copula 회피 패턴 카운트
```

### Step 2: Co-occurrence Scan
```
For each paragraph:
  1. Tier 1 단어 조합 체크 (Critical Co-occurrences 표 대조)
  2. Tier 1+2 동일 문장 내 조합 체크
  3. 인접 단락 동일 단어 반복 체크
```

### Step 3: Document-Level Summary
```
  1. 전체 텍스트 Tier 1 고유 종류 수
  2. 전체 텍스트 AI excess word 총 빈도
  3. Lexical Layer 점수 산출 (1-10)
```

### Scoring Formula (Lexical Layer)

| Condition | Score |
|-----------|-------|
| Critical co-occurrence 0개 + Tier 1 단어 ≤ 1개 | 9–10 |
| Critical co-occurrence 0개 + Tier 1 단어 2–3개 | 7–8 |
| Critical co-occurrence 1개 OR Tier 1 단어 4–6개 | 5–6 |
| Critical co-occurrence 2+개 OR Tier 1 단어 7–10개 | 3–4 |
| Critical co-occurrence 3+개 + 다수 Tier 1 단어 | 1–2 |

---

**This file is read-only reference data. Do not modify during skill execution.**
