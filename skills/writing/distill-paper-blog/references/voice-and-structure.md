# The Distill Voice & The Scaffolding Structure

This is the writing core of the skill. The HTML chrome is easy; *this* is what makes a Distill explainer feel like a Distill explainer rather than a prettier abstract.

## Table of contents
1. The voice: conversational formalism
2. The 8-part scaffolding structure (with worked examples)
3. Sentence & paragraph rhythm
4. The bilingual KO/EN convention
5. AI-tell phrases to avoid

---

## 1. The voice: conversational formalism

The tone is **rigorous content delivered through narrative warmth**. The reader is a smart friend who doesn't yet know this topic. You are walking *beside* them, not lecturing from a podium. Concretely:

| Rule | Why it works | Example (from the GNN article) |
|---|---|---|
| Use **"we"** for the journey | Makes author + reader one team exploring together | *"To start, **let's** establish what a graph is."* |
| Use **"you"** for actions | Invites participation, especially with interactive figures | *"**Hover** over a node…", "**Click** on an image pixel to toggle its value."* |
| **Concept before its name** | The reader grasps the idea, *then* gets the label to hang it on | Adjacency *matrices* appear only after the reader feels the "how do we store connections?" problem |
| **Concrete before abstract** | A familiar example is a foothold for the abstraction | Opens by treating images and text as graphs, *then* general graph theory |
| **Soothe the abstraction** | A one-line reassurance keeps an anxious reader moving | *"if this seems abstract now, we will make it concrete."* |
| **Defer the math** | Notation lands only when there's a felt need for it | No equations in the intro; matrix notation arrives with the representation problem |
| **Close with optimism** | Leaves momentum and curiosity, not a full stop | *"…we are excited to see what the field will bring."* |

The single test: *would this sentence make a beginner feel smart, or make them feel the author is smart?* Always aim for the former.

---

## 2. The 8-part scaffolding structure

This is the load-bearing skeleton. The GNN article uses it; almost any paper can be poured into it. Map the source paper to these eight beats, **in this order**. Each `<h2>` in the article roughly corresponds to one beat (you can merge or split, but keep the *progression*).

> The crucial move is beat 5 (**Why is it hard**) landing *before* beat 6 (**The method**). The reader must feel the problem before the solution arrives, or the method reads as arbitrary machinery. This is the difference between "here is what they did" and "here is why what they did is clever."

**1. Hook** — open on something concrete and relatable, never on the paper.
- Pattern: *"<Familiar thing> is all around us…"* or a vivid single scenario.
- ✗ "This paper proposes a novel architecture for…"
- ✓ "Graphs are all around us; real world objects are often defined in terms of their connections to other things."

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
1. Hook: "Ask a language model who won a game last night and it will confidently make something up."
2. What is it: the model has no memory of recent facts — it only knows its frozen training data. (→ name: parametric knowledge.)
3. Where it bites: medicine, law, news, your own private documents.
4. Task: answer questions using facts the model was never trained on.
5. Why hard: you can't retrain the model for every new fact; the context window can't hold the whole internet.
6. Method simplest-first: (a) just paste relevant text into the prompt → works but how do we find it? (b) add a retriever → how do we rank? (c) embeddings + nearest neighbor → the full RAG pipeline.
7. Does it work: accuracy on knowledge questions; failure mode when retrieval misses.
8. Weeds: chunking strategies, re-rankers. Close: "retrieval turns a fixed model into one that can keep learning — and we're just starting to see where that leads."

---

## 3. Sentence & paragraph rhythm

- **One idea per paragraph.** A short topic sentence states it; the rest of the paragraph unfolds it. (e.g., *"Graphs are all around us"* → then a couple of sentences of elaboration.)
- **Vary sentence length.** Mix a crisp 5-word claim with a longer explanatory sentence. Avoid long strings of same-length sentences — they read as flat and machine-made.
- **Front-load the point.** Don't bury the claim at the end of a winding sentence.
- **Prefer the active, the specific, the small word.** "uses" over "utilizes"; "shows" over "demonstrates"; "but" over "however" where it fits.

---

## 4. The bilingual KO/EN convention

Output is bilingual. The template ships with a **language toggle** (EN / KO / 둘 다) wired up in `style.css` + a few lines of JS. Your job is just to provide both languages in the right wrappers.

**Pattern — paired blocks.** For each paragraph (or logical block), write an English version and a Korean version, each in its own element with the language class:

```html
<p class="lang-en">Graphs are all around us. A graph is just a set of objects and the connections between them.</p>
<p class="lang-ko">그래프는 우리 주변 어디에나 있습니다. 그래프란 결국 <em>객체들</em>과 그 객체들을 잇는 <em>연결</em>의 모음일 뿐입니다.</p>
```

The toggle hides one language by default-state; with "둘 다" both show, English first.

**Conventions for good bilingual writing:**
- The Korean is a *natural translation that preserves the warm Distill tone* — not a stiff literal gloss. Keep the "we/you" feel: "함께 살펴봅시다", "직접 해보세요".
- Keep **technical terms, math, and citations identical** across both — e.g., write "그래프 신경망(Graph Neural Network)" on first mention, then the term as the field uses it. Don't translate `<d-cite>`, `<d-math>`, or figure labels.
- Headings (`<h2>`) get both languages too — put them in one heading with both classes, or write the heading bilingually (e.g., `<h2><span class="lang-en">Why is it hard?</span><span class="lang-ko">왜 어려울까?</span></h2>`).
- Don't paraphrase differently in each language — the two versions should make the same claims, so a bilingual reader isn't confused.

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

Replace with: a concrete detail, a real number, a specific mechanism, or the analogy that makes it click. When tempted to write "it's important to note that X", just write X.

If the user has the **writing-anti-ai** skill available, a final pass with it on the English prose is a good polish step.
