---
name: meta-writing-blog
description: Turn a paper, a manuscript, or a topic into a KEI AI 융합연구단 "브리프" — a polished, self-contained Korean HTML explainer in the KEI editorial house style (quiet Distill-like tone, KEI palette, single-column). Output is a portable folder that opens on its own. Use whenever the user wants a KEI brief, a paper explainer, or a paper-introduction post in this style. Triggers include "KEI 브리프로 만들어줘", "브리프 작성", "이 원고 브리프로", "이 논문 브리프로 써줘", "논문 소개 글 만들어줘", "write a KEI brief", "write a paper explainer".
---

# meta-writing-blog

Turn a source (a paper, a manuscript folder, or the user's notes/topic) into a **KEI 브리프** —
a self-contained Korean HTML explainer that makes the material *understandable*, not just
summarized. Output is **Korean-only** and rendered in the KEI house style.

Two things define it:
- **Voice** — quiet editorial exposition: impersonal, precise, hedged (`–다`체). Keep the
  pedagogy of a good explainer (problem before solution, intuition before notation) but not a
  chatty tone. 박스·그라디언트·이모지는 쓰지 않는다. Rules in `references/voice-and-structure.md`.
- **Design** — the KEI brief template (`assets/brief-template.html`) carries the whole design
  **inline**: KEI palette, typography, and every component (callout, var-list, figure-equations,
  data-table, comparison-grid, figure-canvas, explorer-box, APA references). Copy it; do not
  invent a new framework or hand-roll CSS. Components in `references/STYLE_GUIDE.md`.

## Output

A new self-contained folder (kebab-case `brief-{slug}`, in the current directory):

```
brief-<slug>/
├── brief-<slug>.html   # the brief (a copy of assets/brief-template.html, filled in; CSS inline)
├── assets/             # bundled brand assets — copy of the skill's assets/hero-bg.jpg + KEI_Wordmark.svg
└── figures/            # figures referenced by the brief (if any)
```

All asset paths inside the HTML are **local** (`assets/…`, `figures/…`) — never `../`. Only the
webfonts load from a CDN, so with internet the brief renders fully; without it, only the fonts
fall back and the layout, hero image, and visualizations still work. At the end, tell the user
the folder path and how to open it.

> This skill does **not** write into the live KEI site (`release/`). It copies brand assets out
> and produces a portable folder. To later publish a brief into the real site, move the HTML into
> `release/briefs_files/`, repoint `assets/…` → `../assets/…`, restore the logo/Back/end-nav
> links (marked in the template), and add a row to `briefs.html` per STYLE_GUIDE §8.

## Workflow

**1. Get the source.** Paper: arXiv → WebFetch the abstract; full text → the **markitdown** skill
on the PDF/HTML. Manuscript folder → read every HTML/CSS/JS/MD in it. Topic/notes → use directly.
Determine the **field labels** (English, 1–3, e.g. `Climate · Dynamical systems`). Don't block on
questions you can answer by reading the source.

**2. Blueprint the narrative (don't skip).** Read `references/voice-and-structure.md`. First fix the
**mission** in one line — *who is this brief for, and why would they read it* (the reader's stake).
Then map the source onto the flexible section arc: opening (problem) → central idea → where it
matters → the problem precisely → why hard → method → results → outlook. The load-bearing rule:
**the reader meets the problem before the method.** Sections are flexible — merge, split, rename —
but keep that order. For two or more papers, use the shared-spine variant (one problem, parallel
cases, a synthesis), not one pass per paper. Decide the **title** and the **slug**.

**3. Scaffold.** Create `brief-<slug>/`. Copy `assets/brief-template.html` →
`brief-<slug>/brief-<slug>.html`. Create `brief-<slug>/assets/` and copy the skill's bundled brand
assets into it (`assets/hero-bg.jpg`, `assets/KEI_Wordmark.svg`). Create `brief-<slug>/figures/`.
Edit the copy — don't author the chrome from scratch.

**4. Fill the head.** `<title>` (`{제목} · KEI AI 융합연구단`) and `<meta name="description">`.

**5. Fill the article header.** page-label (`Brief`), `<h1>` title, subtitle (optional), byline
(author pattern per STYLE_GUIDE §3.3 — e.g. `AI 생성 · 김경호 검토`), date `YYYY.MM.DD`, field labels.

**6. Abstract.** 1–3 sentences in `.article-abstract`, formal register.

**7. Write the body.** Fill the `<section>`s in the KEI editorial voice. Map content to the
components in `references/STYLE_GUIDE.md` §4: callout (`callout-warn` for warnings), var-list for
symbol definitions, figure-equations for math (typeset directly with Unicode + `<sub>`/`<sup>`, no
KaTeX), data-table for tabular results, comparison-grid for parallel cases, figure-canvas /
explorer-box for visualizations. **Delete any component example you don't use.** Korean-only: gloss
awkward or untranslatable terms with English in parentheses, e.g. `보유(retention)`.

**8. References.** APA 7 hanging-indent in `.references` (DOI URL preferred). Cite the source paper
plus its key references.

**9. Colophon & nav.** Fill or delete the `.colophon`. Leave the end-nav commented out (no briefs
list in a standalone folder) unless publishing to the site.

**10. Interactivity.** Any canvas/explorer runs from an inline `<script>` with **lazy-start** via
`IntersectionObserver` (the template's demo shows the pattern). Replace the demo's draw functions
with your visualization, or delete the demo blocks + script if unused. Keep interactivity spare in
this register.

**11. Check & deliver.** Verify: no `../` paths remain in the HTML, every `figures/…` `src` exists,
no `[REPLACE …]` markers left, brand assets are present in the folder's `assets/`. Optionally serve
locally (`python -m http.server 8000`) and open `brief-<slug>/brief-<slug>.html`. Report the folder
path and how to open it, plus any placeholders left for the user.

## Quality checklist
- [ ] Opens by framing the problem/gap — not "이 논문은 ~을 제안한다" or an anecdote.
- [ ] Voice stays quiet-editorial academic: impersonal, hedged, `–다`체; 박스·그라디언트·이모지 없음.
- [ ] Problem (why-hard) precedes the method; method builds simplest-first; math follows the idea it formalizes.
- [ ] Multi-paper: shared problem spine + parallel cases + synthesis — not N independent summaries.
- [ ] Korean reads naturally on its own; awkward terms glossed `용어(term)` once on first mention.
- [ ] Components used correctly (callout / var-list / data-table / etc.); unused component examples deleted.
- [ ] Figure captions are objective; interactivity is sparing and lazy-started.
- [ ] References in APA hanging-indent; DOI URLs where available.
- [ ] All asset paths local (`assets/…`, `figures/…`); no `../`; no `[REPLACE …]` left; brand assets bundled.

## Reference files (read on demand)
- `references/voice-and-structure.md` — the quiet-editorial voice, the flexible section arc (+ multi-paper variant), the Korean-only + parenthetical-English convention, AI-tell phrases. **Read before steps 2 and 7.**
- `references/STYLE_GUIDE.md` — the brief format spec: HTML skeleton, every component, color/typography tokens, author/field patterns. **Read before step 7.** (Note: it follows the canonical brief's inline-SVG logo; the Mondrian `logo-mondrian.js` mentioned in the original KEI guide is not used.)
- `assets/` — `brief-template.html` (copy and edit), plus `hero-bg.jpg` and `KEI_Wordmark.svg` (bundled brand assets to copy into each output). Copy, don't recreate.
