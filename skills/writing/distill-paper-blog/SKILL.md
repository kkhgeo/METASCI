---
name: distill-paper-blog
description: Turn an academic paper into a Distill.pub-style explainer blog post — a polished, multifile HTML article that introduces and explains the paper for a general-technical audience. Produces a Distill v2 project (index.html + bibliography.bib + figures/) with bilingual Korean/English prose, a language toggle, margin notes, KaTeX math, BibTeX citations, and lightweight interactive elements. Use this skill WHENEVER the user wants to write a paper-introduction post, a "논문 소개 글/블로그", a paper explainer, a Distill-style article, or wants to turn a PDF/arXiv link or their reading notes into a beautiful web article — even if they don't say "Distill" by name. Triggers include "이 논문 블로그로 써줘", "논문 소개 글 만들어줘", "Distill 스타일로", "paper explainer", "write a blog post about this paper", "arXiv 링크 글로".
trigger: /distill-paper-blog
---

# distill-paper-blog

Turn a paper (PDF, arXiv URL, or the user's notes) into a **Distill.pub-style explainer** — the genre of [distill.pub/2021/gnn-intro](https://distill.pub/2021/gnn-intro/): a warm, visual, intuition-first web article that makes a research paper *understandable*, not just summarized.

The magic of a Distill article is two separable things, and this skill reproduces both:
1. **A voice** — "conversational formalism." We walk the reader from concrete intuition to formal detail, never showing off.
2. **A design** — the `template.v2.js` framework gives typography, a responsive layout grid, margin notes, citations, footnotes, and math *for free*. We never hand-roll CSS for those; we just use the right `<d-*>` tags and layout classes.

This skill targets **bilingual Korean/English** output, a **multifile Distill project**, and **lightweight interactivity** (hover highlights, a language toggle, simple JS/D3 demos).

## Output: what gets produced

A new folder (default: a kebab-case slug of the paper title, created in the current working directory) containing:

```
<paper-slug>/
├── index.html         # the article (copied from assets/index.html, then filled in)
├── style.css          # Korean webfont + language-toggle + small custom styles (copied from assets/)
├── bibliography.bib   # BibTeX entries; d-cite keys resolve against this
└── figures/           # figures pulled from the paper or generated; referenced by index.html
```

It opens by double-clicking `index.html` (it loads `template.v2.js` from the CDN; an internet connection renders the Distill chrome). Always tell the user the folder path and how to open it at the end.

## Workflow

Follow these steps in order. Read the reference files when the step says to — don't try to hold all the detail in your head.

### 1. Get the source material
- **arXiv URL** → fetch the abstract page with WebFetch to get title/authors/abstract; for the full text, fetch the arXiv HTML (`https://arxiv.org/abs/ID` → try `https://arxiv.org/pdf/ID`) or use the **markitdown** skill to convert the PDF to Markdown.
- **Local PDF** → use the **markitdown** skill (or the `pdf` document skill) to extract text and, where possible, figures. Read the result.
- **User notes** → use them directly; ask only for what's missing (see step 2).
- If you have a paper but the user hasn't said what angle they care about, skim for the core contribution and proceed — you can refine later. Don't block on questions you can answer by reading.

### 2. Build the narrative blueprint (do NOT skip)
A summary lists facts; an explainer tells a story. Before writing any HTML, draft a short blueprint that fills the **scaffolding structure** below. This is what separates a Distill article from an abstract.

Read `references/voice-and-structure.md` now — it has the full scaffolding pattern, the voice rules, and worked examples. Fill in:
1. **Hook** — the concrete, relatable opening ("X is all around us…").
2. **What is it** — the core object/idea, defined via a familiar analogy *before* the formal name.
3. **Where is it** — real-world instances, so the reader feels it matters.
4. **What's the task** — what the paper is actually trying to predict/do.
5. **Why is it hard** — the naive approach and exactly where it breaks. This is the tension that earns the method.
6. **The method, simplest-first** — start with a stripped-down version, then add one piece at a time until it's the paper's real method.
7. **Does it work** — the key results, honestly (including limitations).
8. **Into the weeds / closing** — advanced asides moved out of the main flow, then an optimistic, forward-looking close.

If a piece is genuinely missing from the source and you can't infer it, that's the one thing worth asking the user about.

### 3. Scaffold the project
- Pick a slug from the paper title. Create `<slug>/figures/`.
- Copy `assets/index.html`, `assets/style.css`, and `assets/bibliography.bib` into the new folder. **Do not regenerate these from scratch** — they encode the exact working Distill v2 boilerplate (front-matter JSON, KaTeX config, the language toggle, margin-note styling). Editing the template is far more reliable than authoring the chrome yourself.

### 4. Write the prose (the hard part)
Fill `<d-article>` following your blueprint, in the Distill voice. The detailed voice rules and Korean-bilingual conventions are in `references/voice-and-structure.md` — follow them. In short:
- Address the reader as a partner: **we** explore, **you** try. 
- One idea per paragraph; short topic sentence, then unfold it.
- Introduce intuition and analogy *before* notation. Defer math until the reader needs it.
- **Bilingual:** every content block carries both languages — English in `.lang-en`, Korean in `.lang-ko` — and the built-in toggle (EN / KO / 둘 다) controls visibility. See the reference for the exact markup pattern; the template has filled examples to copy.
- Avoid AI-tell phrasing ("delve", "it's important to note", "in conclusion"). Write like the GNN article: plain, warm, specific.

### 5. Wire up the Distill components
Read `references/distill-components.md` for the exact tags and layout classes, then:
- **Citations:** add BibTeX entries to `bibliography.bib`, cite inline with `<d-cite key="...">`. Cite the paper itself and its key references.
- **Math:** `$…$` inline / `$$…$$` block (KaTeX is preconfigured in the front-matter), or `<d-math>`.
- **Footnotes:** `<d-footnote>…</d-footnote>` for asides that would break the sentence.
- **Margin notes:** `<div class="l-gutter">…</div>` for side commentary — a Distill signature; use it instead of parentheticals.
- **Figures & width:** wrap images in `<figure>` with a layout class (`l-body`, `l-body-outset`, `l-page`, `l-screen`). In every caption, *talk to the reader about the figure* ("Notice that…", "여기서 …에 주목").
- **Table of contents:** `<d-contents>` auto-builds from your `<h2>`/`<h3>` — keep headings clean.

### 6. Figures
- Reuse the paper's own figures when extractable → save to `figures/`, reference them, and credit the source in the caption.
- Where a custom diagram would help intuition, generate one (the **scientific-schematics** or **generate-image** skill) or build a small inline SVG/D3 element.
- For lightweight interactivity, see `references/distill-components.md` (hover highlight, toggle, minimal D3). Keep it tasteful — interaction should teach, not decorate.

### 7. Preview & deliver
- Sanity-check: open `index.html` mentally — are all `<d-cite>` keys in the `.bib`? Do figure `src` paths exist? Does `$…$` math look balanced?
- Optionally start a local server so relative paths and the toggle work cleanly:
  `python -m http.server 8000` from inside the folder, then `http://localhost:8000`.
- Report the folder path, list what you created, and note anything left as a placeholder for the user to fill (e.g., a missing figure or an unverified result).

## Quality checklist
Before declaring done, verify the article would make the GNN-intro authors nod:
- [ ] Opens with a concrete hook, not "This paper proposes…".
- [ ] The reader meets a *problem* (step 5: why hard) before they meet the *solution*.
- [ ] Method is built up simplest-first, one addition at a time — not dumped at full complexity.
- [ ] Math appears only after the idea it formalizes; no wall of notation up front.
- [ ] At least one margin note and one footnote used naturally.
- [ ] Every figure caption speaks to the reader.
- [ ] Both languages present in every block; toggle works.
- [ ] Closes optimistically / forward-looking, not with a flat summary.
- [ ] Paper + key references cited via `<d-cite>`; all keys exist in `bibliography.bib`.

## Reference files
- `references/voice-and-structure.md` — the conversational-formalism voice, the 8-part scaffolding pattern with worked examples, AI-tell phrases to avoid, and the bilingual KO/EN writing convention. **Read before step 2 and step 4.**
- `references/distill-components.md` — full `<d-*>` component reference, layout grid classes, KaTeX setup, citations/footnotes/margin notes, and lightweight-interactivity recipes (toggle, hover, minimal D3). **Read before step 5.**
- `assets/index.html` — ready-to-edit Distill v2 article with the scaffolding sections and one filled bilingual example per feature. **Copy, don't recreate.**
- `assets/style.css` — Korean webfont + language toggle + margin-note styling.
- `assets/bibliography.bib` — example BibTeX entries to extend.
