# The Voice & The Scaffolding Structure

This is the writing core of the skill. The HTML chrome is easy; *this* is what makes a
brief read as a credible scholarly explainer rather than a prettier abstract. The
**format** is the KEI brief (single-column, inline CSS, the components in
`STYLE_GUIDE.md`); the **voice** is a quiet editorial review — Distill's calm register in
Korean.

## Table of contents
1. The voice: scholarly exposition
2. The scaffolding structure (flexible sections)
3. Sentence & paragraph rhythm
4. Korean-only convention & the parenthetical-English rule
5. AI-tell phrases to avoid

---

## 1. The voice: scholarly exposition

The tone is that of a well-written **review article** run at editorial calm: rigorous,
impersonal, and measured. The reader is a capable person from an adjacent field — not a
novice to be coaxed, but not a specialist in this exact topic either. The goal is the same
as any good explainer — make the work *understandable* — but the means is precision and
clear reasoning, not warmth or conversational chattiness.

| Rule | Why it works | Example |
|---|---|---|
| **Impersonal register** | Scholarly prose foregrounds the work, not the writer | `–다`체, `본 글`/`이 연구`; avoid `우리`, `함께 살펴봅시다`, `해보세요` |
| **Concept before its name** | Comprehension first, label second | 아이디어를 평이하게 정의한 뒤 `이를 ___(English term)라 한다` |
| **Define before notation** | The reader needs the idea before the symbol | 관계를 산문으로 진술한 뒤 수식(figure-equations)을 제시 |
| **Hedge and attribute claims** | Scholarly caution; don't overclaim | `~로 보인다`, `~을 시사한다`; 출처를 References로 귀속 |
| **Precision over color** | Exactness is the currency; a metaphor is a tool, not the default | 비유는 이해를 날카롭게 할 때만, 그 뒤 정밀한 언어로 복귀 |
| **Honest limitations** | Trust comes from not overselling | 실패 양상·불확실성을 분명히 적는다 |
| **Measured close** | End forward-looking but restrained | `향후 ~로 확장될 수 있다`, not "we're excited to see what's next" |

The **KEI tone rule** on top of this: *조용한 editorial*. 박스·그라디언트·이모지·과장된
강조를 피한다. 강조는 좌측 선(callout)과 `<strong>`/`<em>`로 충분하다.

The single test: *does this sentence state the idea precisely and let the reader follow the
reasoning?* Formality serves clarity — if a formal construction obscures the point,
simplify it. Prose hedged into mush fails the test as surely as chatty prose does.

---

## 2. The scaffolding structure (flexible sections)

A brief is organized into `<section>` blocks inside `<div class="article-body">`, each with
an `<h2>`. There is no fixed section count — **merge, split, or rename freely** to fit the
source. What carries the piece is one soft ordering principle:

> **The reader should meet the problem before the method.** Present what is at stake and
> why it is hard *before* the machinery that resolves it, or the method reads as arbitrary.
> This is the difference between "here is what they did" and "here is why what they did is
> clever."

A serviceable default arc — adapt as needed:

1. **Opening (problem framing)** — open on the problem or open question, not on the paper's
   machinery and not on an anecdote. State what matters and what is unresolved.
   - ✗ "This paper proposes a novel architecture for…" (promotional, starts from the solution)
   - ✗ "어젯밤 경기 결과를 챗봇에게 물어보면…" (anecdotal, conversational)
   - ✓ "하천의 자연저감량은 직접 관측되지 않으며, 이를 공공자료만으로 정량화하는 표준 절차는 아직 확립되지 않았다."
2. **The central idea** — define the central object/idea plainly, then name it.
3. **Where it matters** — a few real domains where the problem bites; builds stakes.
4. **The problem, precisely** — state exactly what is being solved (input → desired output).
5. **Why it is hard** — the naive approach and the precise point where it breaks (a violated
   property, an exploding cost, a false assumption).
6. **The approach, simplest-first** — build the contribution incrementally: a stripped-down
   version that *almost* works, then one piece at a time, each motivated by the previous
   step's shortcoming. Never dump the full method at once. Math (figure-equations) arrives
   only *after* the prose idea it formalizes.
7. **Results and limitations** — the headline result with a real number, and an honest note
   on failure modes.
8. **Outlook** — a short, measured close: what this enables, what remains open.

This arc suits a single paper. For other inputs it still works as a checklist of beats — a
policy or method brief may compress 2–4 into a single section, and a general topic brief may
skip 5 entirely. Keep the *problem-before-method* order; treat the rest as movable.

### Variant: covering two or more papers together

Do **not** run the arc once per paper — that yields disconnected summaries stitched end to
end. Use a shared spine:

- **One shared problem as the spine.** Beats 1–5 are written *once*, around the question the
  papers jointly address.
- **Parallel case sections** with a *common internal structure* (e.g. 대상·자료 / 방법 /
  핵심 결과) so the reader compares like with like. The `comparison-grid` component fits here.
- **A synthesis section is the payoff** — where they agree and diverge, their complementary
  strengths. Without it, the brief is two summaries side by side.

---

## 3. Sentence & paragraph rhythm

- **One idea per paragraph.** A short topic sentence states it; the rest unfolds it.
- **Vary sentence length.** Mix a crisp 5-word claim with a longer explanatory sentence.
  Long strings of same-length sentences read as flat and machine-made.
- **Front-load the point.** Don't bury the claim at the end of a winding sentence.
- **Prefer the precise, concrete word.** Name the specific quantity or mechanism;
  "측정한다" beats "수행한다". Avoid empty inflation ("novel", "robust" as filler) and the
  opposite failure of burying every claim under needless hedging.

---

## 4. Korean-only convention & the parenthetical-English rule

Output is **Korean only** — there is no language toggle and no paired English block. The
Korean must therefore be fully self-contained. General technical terms may stay in English
(transformer, ensemble), but a Korean sentence must never *silently depend* on English to be
understood.

### The parenthetical-English rule (the important one)

**When a term reads awkwardly in Korean, is ambiguous, or has no settled Korean translation,
write the Korean and put the English in parentheses right after it — once, on first mention.**

- ✓ `반사실(counterfactual) 시나리오로 추정한다.`
- ✓ `이 차이를 자연저감, 곧 보유(retention)라 부른다.`
- ✓ `그래프 신경망(Graph Neural Network)으로…` — then just `그래프 신경망` thereafter.
- ✗ `카운터팩추얼 시나리오로…` — don't transliterate a technical term into Hangul and leave it.
- ✗ `retention으로 추정한다.` — don't drop a bare English word into Korean prose with no Korean for it.

When to reach for it:
- **First mention of a technical term** whose Korean is non-obvious or whose English is what
  the field actually uses. Gloss once, then use the Korean (or the established term).
- **A translation that would be clumsy or lossy** — give the natural Korean, then the English
  in parentheses so the precise meaning survives.
- **Proper nouns, method names, metrics, units** — keep them in original form (SWAT, NANI,
  R², kg/yr); add a short Korean gloss only if it genuinely helps.

Don't overdo it. If the Korean is clear on its own, no parenthetical is needed — a page where
every other word has an English tail is harder to read. The test: *could a Korean-only reader
follow this sentence with confidence?* If yes, leave it clean; if a term would make them
hesitate, gloss it.

Keep math symbols, metric names, and figure labels in their original form; don't Koreanize
them. Headings (`<h2>`/`<h3>`) follow the same parenthetical rule.

---

## 5. AI-tell phrases to avoid

Good briefs read as human and specific. These patterns make writing feel generated — strip
them:

- Hedging throat-clearing: "It's important to note that", "It's worth mentioning", "Note that",
  `~라는 점에 주목할 필요가 있다`, `~라는 점을 언급할 가치가 있다`.
- Empty intensifiers: "delve into", "dive deep", "leverage", "harness the power of", "robust",
  "seamless"; 한국어의 `~을 심층적으로 파헤친다`, `~을 적극 활용한다` 류 상투구.
- Listicle scaffolding in prose: "Firstly… Secondly… Lastly", "In conclusion", `첫째…둘째…`,
  `결론적으로`.
- The "not only… but also" / "From X to Y" essay tics; `A뿐만 아니라 B도`.
- Vague praise: "groundbreaking", "novel", "state-of-the-art" as filler rather than a
  specific, supported claim; `획기적인`, `혁신적인`.
- Symmetrical triads everywhere ("fast, simple, and powerful"; `빠르고 단순하며 강력한`).
- The academic-register tells, equally: drowning every claim in hedges, heavy nominalization
  (`~의 활용을 수행한다` → `~을 쓴다`), citation-padding to look authoritative. Formal does
  not mean turgid.

Replace with: a concrete detail, a real number, a specific mechanism, or the analogy that
makes it click. When tempted to write "it's important to note that X", just write X.

이 목록은 초안 단계의 1차 방어선이다. 최종 방어선은 선택이 아니라 **SKILL.md 11단계** —
발간 전에 완성된 산문 전체(제목·초록 포함)를 **meta-mywriting-korean** 스킬로 재작성하는
필수 패스다 (한국어 AI 패턴 제거 + 사용자 개인 문체 전이 내장; 적용 범위 제한은 11단계 참조).
