---
name: meta-writing-blog
description: Turn an academic paper into a Distill.pub-style explainer blog post — a polished, multifile HTML article that introduces and explains the paper for a general-technical audience. Produces a Distill v2 project (index.html + bibliography.bib + figures/) with bilingual Korean/English prose, a language toggle, margin notes, KaTeX math, BibTeX citations, and lightweight interactive elements. Use this skill WHENEVER the user wants to write a paper-introduction post, a "논문 소개 글/블로그", a paper explainer, a Distill-style article, or wants to turn a PDF/arXiv link or their reading notes into a beautiful web article — even if they don't say "Distill" by name. Triggers include "이 논문 블로그로 써줘", "논문 소개 글 만들어줘", "Distill 스타일로", "paper explainer", "write a blog post about this paper", "arXiv 링크 글로".
trigger: /meta-writing-blog
---

# meta-writing-blog

Turn a paper (PDF, arXiv URL, or the user's notes) into a **Distill-format explainer written in an academic review voice** — a multifile HTML article that makes the paper *understandable*, not just summarized. Output is **Korean-primary and bilingual**.

Two things define it:
- **Voice** — scholarly exposition: impersonal, precise, hedged. Keep Distill's *pedagogy* (problem before solution, intuition before notation) but not its chatty tone. Rules live in `references/voice-and-structure.md`.
- **Design** — the `template.v2.js` framework gives typography, a layout grid, margin notes, citations, footnotes, and math for free via `<d-*>` tags. Don't hand-roll CSS for these.

## Output

A new folder (kebab-case slug of the title, in the current directory):

```
<paper-slug>/
├── index.html        # the article (edit a copy of assets/index.html)
├── style.css         # Korean webfont + language toggle (copy of assets/)
├── bibliography.bib  # BibTeX; d-cite keys resolve here
└── figures/          # figures referenced by index.html
```

The article loads `template.v2.js` from the CDN, so viewing needs internet. At the end, tell the user the folder path and how to open it.

## Workflow

**1. Get the source.** arXiv → WebFetch the abstract; for full text use the **markitdown** skill on the PDF/HTML. Local PDF → **markitdown** (or the `pdf` skill). Notes → use directly. Don't block on questions you can answer by reading the paper.

**2. Blueprint the narrative (don't skip).** Read `references/voice-and-structure.md`, then map the paper to the 8-beat scaffold: opening (problem) → what → where → task → why-hard → method → results → outlook. The load-bearing rule: **the reader meets the problem (why-hard) before the method.** Sections are flexible — merge, split, or rename — but keep that order. For two or more papers, use the multi-paper variant (shared problem spine + parallel cases + synthesis), not one pass per paper.

**3. Scaffold.** Create `<slug>/figures/` and copy `assets/index.html`, `style.css`, and `bibliography.bib` into it. Edit the copies — don't author the Distill chrome from scratch.

**4. Write the prose.** Fill `<d-article>` in the academic voice per the reference. The essentials: impersonal register (`–다`체, `본 글`/`이 연구`; no we/you/let's), hedged and cited claims, intuition before math, one idea per paragraph. **Korean-primary bilingual:** each block carries `.lang-ko` + `.lang-en` and the toggle opens at KO, so the Korean must read on its own — gloss awkward or untranslatable terms with English in parentheses, e.g. `보유(retention)`.

**5. Wire up components.** See `references/distill-components.md`: citations `<d-cite key>` (cite the paper + its key refs), math `$…$`/`$$…$$`, footnotes `<d-footnote>`, margin notes `<div class="l-gutter">`, figures in `<figure>` with a layout class (`l-body`/`l-page`/…) and an objective caption. `<d-contents>` auto-builds the TOC from your headings.

**6. Figures.** Reuse the paper's figures (save to `figures/`, credit in the caption) or generate a diagram (**scientific-schematics** / **generate-image**, or inline SVG). Interactivity is optional and used sparingly in this register.

**7. Check & deliver.** Verify every `<d-cite>` key is in the `.bib`, figure `src` paths exist, and `$…$` are balanced. Optionally serve locally (`python -m http.server 8000`). Report the folder path and any placeholders left for the user.

## Quality checklist
- [ ] Opens by framing the problem/gap — not "This paper proposes…" or an anecdote.
- [ ] Voice stays academic: impersonal, hedged, `–다`체; no we/you/let's.
- [ ] Problem (why-hard) precedes the method; method builds simplest-first; math follows the idea it formalizes.
- [ ] Multi-paper: shared problem spine + parallel cases + synthesis — not N independent summaries.
- [ ] Korean reads naturally on its own; awkward terms glossed `용어(term)`; toggle opens at KO.
- [ ] Figure captions are objective; at least one margin note and one footnote used.
- [ ] All `<d-cite>` keys exist in `bibliography.bib`.

## Reference files (read on demand)
- `references/voice-and-structure.md` — the academic voice, the 8-beat structure (+ multi-paper variant), the Korean-primary bilingual convention, AI-tell phrases. **Read before steps 2 and 4.**
- `references/distill-components.md` — `<d-*>` tags, layout classes, KaTeX, citations/footnotes/margin notes, interactivity. **Read before step 5.**
- `assets/` — `index.html` (copy and edit), `style.css`, `bibliography.bib`. Copy, don't recreate.
