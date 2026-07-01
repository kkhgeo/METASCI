# The Voice & The Scaffolding Structure

This is the writing core of the skill. The HTML chrome is easy; *this* is what makes the article read as a credible scholarly explainer rather than a prettier abstract. The **format** is Distill (the layout, margin notes, citations, math); the **voice** is an academic review article.

## Table of contents
1. The voice: scholarly exposition
2. The 8-part scaffolding structure (with worked examples)
3. Sentence & paragraph rhythm
4. The bilingual KO/EN convention
5. AI-tell phrases to avoid

---

## 1. The voice: scholarly exposition

The tone is that of a well-written **review article**: rigorous, impersonal, and measured. The reader is a capable researcher from an adjacent field — not a novice to be coaxed, but not a specialist in this exact topic either. The goal is the same as any good explainer — make the work *understandable* — but the means is precision and clear reasoning, not warmth or conversational chattiness. Aim for a readable review, not an opaque one.

| Rule | Why it works | Example |
|---|---|---|
| **Impersonal register** | Scholarly prose foregrounds the work, not the writer | Korean: `–다`체, `본 글`/`이 연구`; avoid `우리`, `함께 살펴봅시다`, `해보세요`. English: prefer the work as subject ("the study estimates…") over "we/you/let's". |
| **Concept before its name** | Comprehension first, label second — still the best pedagogy | Define the idea in plain terms, *then* `이를 ___(English term)라 한다` |
| **Define before notation** | The reader needs the idea before the symbol | State the relationship in prose, then give the equation |
| **Hedge and attribute claims** | Scholarly caution; don't overclaim what a study actually shows | `~로 보인다`, `~을 시사한다`; attribute with `<d-cite>` rather than asserting flatly |
| **Precision over color** | Exactness is the currency; a vivid metaphor is a tool, not the default | Use an analogy only when it sharpens understanding, then return to precise language |
| **Honest limitations** | Trust comes from not overselling — true of Distill and of good papers alike | State failure modes and uncertainties plainly |
| **Measured close** | End forward-looking but restrained | `향후 ~로 확장될 수 있다`, not "we're excited to see what's next" |

The single test: *does this sentence state the idea precisely and let the reader follow the reasoning?* Formality serves clarity — if a formal construction obscures the point, simplify it. Prose hedged into mush fails the test as surely as chatty prose does.

---

## 2. The 8-part scaffolding structure

This is the load-bearing skeleton. The GNN article uses it; almost any paper can be poured into it. Map the source paper to these eight beats, **in this order**. Each `<h2>` in the article roughly corresponds to one beat (you can merge or split, but keep the *progression*).

> The crucial move is beat 5 (**Why is it hard**) landing *before* beat 6 (**The method**). The reader must feel the problem before the solution arrives, or the method reads as arbitrary machinery. This is the difference between "here is what they did" and "here is why what they did is clever."

**1. Opening (problem framing)** — open on the problem or the open question, not on the paper's machinery and not on an anecdote.
- State what matters and what is unresolved. A concrete motivating phenomenon is welcome; a chatty *"X is all around us"* is too casual for this register.
- ✗ "This paper proposes a novel architecture for…" (promotional, and starts from the solution)
- ✗ "어젯밤 경기 결과를 챗봇에게 물어보면 없는 답을 지어냅니다…" (anecdotal, conversational)
- ✓ "하천의 자연저감량은 직접 관측되지 않으며, 이를 공공자료만으로 정량화하는 표준 절차는 아직 확립되지 않았다."

**2. What is it** — define the central object/idea through analogy first, formal name second.
- Introduce the everyday intuition, *then* say "this is called a ___."

**3. Where is it** — show the idea living in several real domains.
- Builds stakes: the reader sees why anyone should care. (GNN: molecules, social networks, citation graphs, images, text.)

**4. What's the task** — state precisely what the paper is trying to do/predict.
- Name the task types or the input→output. Keep it crisp.

**5. Why is it hard** — present the naive/obvious approach and show exactly where it breaks.
- This is the tension. Be specific about the failure: a property that gets violated, a cost that explodes, an assumption that's false. (GNN: permutation invariance, variable size, awkward connectivity representation.)

**6. The method, simplest-first** — build the paper's contribution incrementally.
- Start with a deliberately stripped-down version that *almost* works. Add one component at a time, each motivated by a shortcoming of the previous step, until you've reconstructed the paper's actual method. Never dump the full architecture at once.

**7. Does it work** — the key results, honestly.
- Lead with the headline result in plain terms. Include an honest note on limitations or failure cases — Distill articles are trusted because they don't oversell.

**8. Into the weeds + closing**
- *Into the weeds:* move genuinely advanced asides (ablations, alternative formulations, theory) into a clearly-marked late section or `<d-appendix>`, so the main flow stays clean.
- *Closing:* a short, forward-looking paragraph. What does this unlock? What's next? End with curiosity, not "In conclusion, we have shown…".

### Worked mini-example (mapping a paper to the beats)
For a paper on, say, *retrieval-augmented generation*:
1. Opening: a language model has no record of facts postdating its training, so queries about recent events yield fluent but unfounded answers — the gap this work addresses.
2. What is it: the model has no memory of recent facts — it only knows its frozen training data. (→ name: parametric knowledge.)
3. Where it bites: medicine, law, news, your own private documents.
4. Task: answer questions using facts the model was never trained on.
5. Why hard: you can't retrain the model for every new fact; the context window can't hold the whole internet.
6. Method simplest-first: (a) just paste relevant text into the prompt → works but how do we find it? (b) add a retriever → how do we rank? (c) embeddings + nearest neighbor → the full RAG pipeline.
7. Does it work: accuracy on knowledge questions; failure mode when retrieval misses.
8. Weeds: chunking strategies, re-rankers. Close: retrieval lets a fixed model draw on knowledge it was never trained on, and the design space for how it retrieves remains largely open.

### Variant: explaining two or more papers together

When the article covers several papers (a comparison or synthesis), do **not** run the eight beats once per paper — that yields disconnected summaries stitched end to end. Use a shared spine instead:

- **One shared problem as the spine.** Beats 1–5 (opening, what, where, task, why hard) are written *once*, around the question the papers jointly address. The reader meets a single problem, then learns that several studies attack it differently.
- **Parallel case sections.** Where the approaches diverge, give each paper its own section under a *common internal structure* (e.g. 대상·자료 / 방법 / 핵심 결과), so the reader compares like with like.
- **A synthesis section is the payoff.** After the cases, a section comparing them — a table of dimensions, where they agree and diverge, their complementary strengths — is what justifies treating them together. Without it, the article is two summaries side by side.
- For three or more papers, grouping by *approach type* rather than one section per paper often reads more cleanly.

The progression principle still holds: the shared problem and its difficulty come before any single paper's method. This is also why a rigid per-paper IMRaD does not fit — the value is in the cross-cutting analysis, which IMRaD has no place for.

---

## 3. Sentence & paragraph rhythm

- **One idea per paragraph.** A short topic sentence states it; the rest of the paragraph unfolds it. (e.g., *"Graphs are all around us"* → then a couple of sentences of elaboration.)
- **Vary sentence length.** Mix a crisp 5-word claim with a longer explanatory sentence. Avoid long strings of same-length sentences — they read as flat and machine-made.
- **Front-load the point.** Don't bury the claim at the end of a winding sentence.
- **Prefer the precise, concrete word.** Name the specific quantity or mechanism rather than a vague one; "측정한다/measures" beats "수행한다/performs". Formal register is fine, but avoid both empty inflation ("novel", "robust" as filler) and the opposite failure of burying every claim under needless hedging. Passive voice is acceptable where it keeps the focus on the work.

---

## 4. The bilingual convention — Korean-primary

Output is bilingual, but **Korean is the primary language**. The template's toggle (EN / KO / 둘 다) opens at **KO**, so the default reader sees Korean only and may never touch the toggle. The English block is still there — for English readers and for bilingual readers who pick 둘 다 — but you should write as if the Korean has to carry the article by itself. That single shift is what this section is about.

**Pattern — paired blocks.** For each paragraph (or logical block), write a Korean version and an English version, each in its own element with the language class. Author them in either source order; the toggle controls what shows.

```html
<p class="lang-ko">그래프는 우리 주변 어디에나 있습니다. 그래프란 결국 <em>객체들</em>과 그 객체들을 잇는 <em>연결</em>의 모음일 뿐입니다.</p>
<p class="lang-en">Graphs are all around us. A graph is just a set of objects and the connections between them.</p>
```

When the user picks 둘 다, both show (English under Korean, with a left rule on the Korean). When they pick KO or EN, only that one shows.

### The parenthetical-English rule (the important one)

Because the KO reader never sees the English block, the Korean must be self-contained. The failure mode to avoid is a Korean sentence that silently depends on the English version to be understood. The fix: **when a term reads awkwardly in Korean, is ambiguous, or has no settled Korean translation, write the Korean and put the English in parentheses right after it.**

- ✓ `반사실(counterfactual) 시나리오로 추정합니다.`
- ✓ `이 차이를 자연저감, 곧 보유(retention)라고 부릅니다.`
- ✓ `그래프 신경망(Graph Neural Network)으로...` — then just `그래프 신경망` on later mentions.
- ✗ `카운터팩추얼 시나리오로...` — don't transliterate a technical term into Hangul and leave it.
- ✗ `retention으로 추정합니다.` — don't drop a bare English word into Korean prose with no Korean for it.

When to reach for it:
- **First mention of a technical term** whose Korean is non-obvious or whose English is what the field actually uses. Gloss once, then use the Korean (or the established term) thereafter.
- **A translation that would be clumsy or lossy** — give the natural Korean, then the English in parentheses so the precise meaning survives.
- **Proper nouns, method names, metrics, units** — keep them in their original form (SWAT, NANI, R², kg/yr); add a short Korean gloss only if it genuinely helps.

Don't overdo it. If the Korean is clear on its own, no parenthetical is needed — a page where every other word has an English tail is harder to read, not easier. The test: *could a Korean-only reader follow this sentence with confidence?* If yes, leave it clean; if a term would make them hesitate, gloss it.

### Other conventions

- The Korean is a *natural, fluent translation* — not a stiff literal gloss — in the same scholarly register as the English (`–다`체, impersonal). Don't reintroduce a chatty "we/you" tone in the Korean.
- Keep **math and citations identical** across both languages. Don't translate `<d-cite>`, `<d-math>`, or figure labels.
- Headings (`<h2>`/`<h3>`) get both languages too — one heading with both spans: `<h2><span class="lang-ko">왜 어려울까?</span><span class="lang-en">Why is it hard?</span></h2>`. The same parenthetical rule applies to Korean headings.
- The two versions should make the **same claims** — don't paraphrase differently in each, or a 둘 다 reader gets confused. The parenthetical English in the Korean block is a gloss, not a second translation; the full English still lives in the `.lang-en` block.

The template's filled examples show this pattern for paragraphs, headings, captions, and margin notes — copy their structure.

---

## 5. AI-tell phrases to avoid

Distill articles read as human and specific. These patterns make writing feel generated — strip them:

- Hedging throat-clearing: "It's important to note that", "It's worth mentioning", "Note that".
- Empty intensifiers: "delve into", "dive deep", "unleash", "leverage", "harness the power of", "robust", "seamless".
- Listicle scaffolding in prose: "Firstly… Secondly… Lastly", "In conclusion".
- The "not only… but also" / "From X to Y" essay tics.
- Vague praise of the paper: "groundbreaking", "novel", "state-of-the-art" used as filler rather than as a specific, supported claim.
- Symmetrical triads everywhere ("fast, simple, and powerful").
- The academic-register tells, equally: drowning every claim in hedges ("it may perhaps be possible that…"), heavy nominalization ("the utilization of" → "using"), and citation-padding to look authoritative. Formal does not mean turgid.

Replace with: a concrete detail, a real number, a specific mechanism, or the analogy that makes it click. When tempted to write "it's important to note that X", just write X.

If the user has the **writing-anti-ai** skill available, a final pass with it on the English prose is a good polish step.
