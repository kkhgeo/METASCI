# Distill v2 HTML Components — Reference

Everything you need to wire up the Distill chrome. The `assets/index.html` template already contains working instances of all of these — this file explains *what each does* and *how to use it correctly* so you can edit confidently.

## Table of contents
1. The framework script & document skeleton
2. Front-matter (title, authors, KaTeX config)
3. Title, byline, table of contents
4. The layout grid (the heart of the design)
5. Margin notes
6. Figures
7. Citations & bibliography
8. Footnotes
9. Math (KaTeX)
10. Appendix
11. Lightweight interactivity (toggle, hover, minimal D3)
12. Common mistakes

---

## 1. The framework script & document skeleton

A single script registers every `<d-*>` web component and injects all the typography/layout CSS:

```html
<script src="https://distill.pub/template.v2.js"></script>
```

Put it in `<head>`. It needs network access at view time. The whole document is:

```html
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="https://distill.pub/template.v2.js"></script>
  <link rel="stylesheet" href="style.css">   <!-- our Korean font + toggle styles -->
  <!-- d-front-matter JSON goes here (see §2) -->
</head>
<body>
  <d-title>…</d-title>
  <d-byline></d-byline>
  <d-article>
    <d-contents></d-contents>   <!-- optional auto TOC -->
    …content…
  </d-article>
  <d-appendix>…</d-appendix>
  <d-bibliography src="bibliography.bib"></d-bibliography>
</body>
</html>
```

Order matters: `d-title` → `d-byline` → `d-article` → `d-appendix` → `d-bibliography`.

## 2. Front-matter

In v2, metadata is **JSON** inside a `<d-front-matter>` element in the `<head>` (or top of body). It feeds `<d-byline>`, the page `<title>`, citation metadata, and the KaTeX config.

```html
<d-front-matter>
  <script type="text/json">
  {
    "title": "Your bilingual-friendly title",
    "description": "One-sentence summary for previews and search.",
    "authors": [
      { "author": "Your Name", "authorURL": "https://your-site.com",
        "affiliation": "Your Lab", "affiliationURL": "https://lab.com" }
    ],
    "katex": {
      "delimiters": [
        { "left": "$", "right": "$", "display": false },
        { "left": "$$", "right": "$$", "display": true }
      ]
    }
  }
  </script>
</d-front-matter>
```

The `katex.delimiters` block is what makes plain `$…$` render as math anywhere in the article. Keep it.

## 3. Title, byline, table of contents

```html
<d-title>
  <h1>Main title</h1>
  <p>A one-line subtitle that says what the reader will understand by the end.</p>
</d-title>

<d-byline></d-byline>   <!-- auto-rendered from front-matter authors/affiliations/date -->
```

`<d-contents>` placed at the top of `<d-article>` auto-generates a left-margin table of contents from your `<h2>`/`<h3>`. For it to read well, keep headings short and meaningful. You can also hand-author it:

```html
<d-contents>
  <nav class="l-text figcaption">
    <h3>Contents</h3>
    <div><a href="#what-is-it">What is it?</a></div>
    <div><a href="#why-hard">Why is it hard?</a></div>
  </nav>
</d-contents>
```
(Give the matching `<h2 id="what-is-it">` an id.)

## 4. The layout grid (the heart of the design)

This is where ~90% of the "Distill look" comes from. Any block element *inside `<d-article>`* gets its width from a layout class. The page is a centered text column with progressively wider bands and a right gutter:

| Class | Width | Use for |
|---|---|---|
| `l-body` | main text column (default for `<p>`) | normal paragraphs, small figures |
| `l-body-outset` | a bit wider than text | figures that want slight emphasis |
| `l-middle` | wider | medium diagrams |
| `l-page` | much wider | big diagrams |
| `l-screen` | full viewport width | hero images, full-bleed visuals |
| `l-screen-inset` | full width, small margins | full-bleed but breathing room |
| `l-gutter` | the right margin | **margin notes** (§5) |

`*-outset` variants exist for `l-body`, `l-middle`, `l-page`. Add `side` (e.g. `l-body side`) to float a block to the side with text wrapping beside it.

Plain `<p>`, `<h2>`, etc. are already `l-body` — you only add a class when you want a *different* width.

## 5. Margin notes

A Distill signature: side commentary in the right gutter that enriches without interrupting the main line of thought. Prefer these over long parentheticals.

```html
<div class="l-gutter">
  <p class="lang-en">A note that sits in the margin, beside the paragraph it comments on.</p>
  <p class="lang-ko">본문 옆 여백에 떠서 흐름을 끊지 않고 덧붙이는 메모입니다.</p>
</div>
```

Place the gutter `<div>` right after the paragraph it relates to.

## 6. Figures

Always wrap images in `<figure>` + a layout class, and **write captions that talk to the reader** (this is part of the voice):

```html
<figure class="l-page">
  <img src="figures/architecture.png" alt="The model architecture">
  <figcaption>
    <span class="lang-en">Notice how information flows left to right; each block only sees its neighbors. (Figure adapted from the paper.)</span>
    <span class="lang-ko">정보가 왼쪽에서 오른쪽으로 흐르고, 각 블록은 이웃만 본다는 점에 주목하세요. (논문 그림 재구성.)</span>
  </figcaption>
</figure>
```

Credit the source paper in captions for reused figures. Inline SVG can replace `<img>` for crisp, themeable, interactive diagrams (§11).

## 7. Citations & bibliography

Define entries in `bibliography.bib` (standard BibTeX), point `<d-bibliography src="bibliography.bib">` at it, and cite inline:

```html
…as shown by prior work <d-cite key="vaswani2017attention"></d-cite>.
…combine two ideas <d-cite key="kipf2017gcn,velickovic2018gat"></d-cite>.
```

The keys must match `@article{vaswani2017attention, …}` in the `.bib`. Distill renders a numbered citation and auto-builds the reference list. Always cite the paper you're introducing, plus its most important references.

Alternatively, an inline bibliography (no separate file):

```html
<d-bibliography>
  <script type="text/bibliography">
    @article{key, title={…}, author={…}, journal={…}, year={2024}, url={…} }
  </script>
</d-bibliography>
```

## 8. Footnotes

For an aside that would derail the sentence but is too small for a margin note:

```html
The model is permutation-invariant<d-footnote>That is, reordering the inputs doesn't change the output.</d-footnote>.
```

Renders as a hoverable superscript and collects into the appendix footnote list.

## 9. Math (KaTeX)

With the front-matter `katex.delimiters` set (§2):
- Inline: `the loss $\mathcal{L} = -\sum_i y_i \log \hat{y}_i$ is minimized…`
- Block: `$$ h_v^{(l+1)} = \sigma\!\Big( W^{(l)} \sum_{u \in \mathcal{N}(v)} \tfrac{1}{c_{vu}} h_u^{(l)} \Big) $$`

Or use the component form (handy when delimiters are ambiguous):
```html
<d-math>x_i</d-math>                       <!-- inline -->
<d-math block>\sum_{i=1}^n x_i</d-math>    <!-- display -->
```

Introduce math only *after* the prose idea it formalizes (see voice rules). A wall of notation at the top is the fastest way to lose a reader.

## 10. Appendix

For "into the weeds" content, acknowledgments, and a how-to-cite block, placed after the article:

```html
<d-appendix>
  <h3>Acknowledgments</h3>
  <p>…</p>
  <h3>Into the weeds: ablations</h3>
  <p>…</p>
  <d-footnote-list></d-footnote-list>
  <d-citation-list></d-citation-list>
</d-appendix>
```

## 11. Lightweight interactivity

Keep it tasteful — interaction should *teach*. Three reliable, dependency-light patterns:

### a) Language toggle (already in the template)
`style.css` defines `body.show-en .lang-ko { display:none }` and `body.show-ko .lang-en { display:none }`, with both shown by default. A tiny script flips a class on `<body>`. This is the bilingual mechanism; don't remove it.

### b) Hover highlight (pure CSS/JS, no library)
```html
<svg viewBox="0 0 200 80" class="interactive-demo">
  <circle cx="40" cy="40" r="16" data-node="a"></circle>
  <circle cx="160" cy="40" r="16" data-node="b"></circle>
</svg>
<script>
  document.querySelectorAll('.interactive-demo [data-node]').forEach(el => {
    el.addEventListener('mouseenter', () => el.classList.add('hot'));
    el.addEventListener('mouseleave', () => el.classList.remove('hot'));
  });
</script>
```
Tell the reader to interact in the caption: *"Hover the nodes."* / *"노드 위에 마우스를 올려보세요."*

### c) Minimal D3 (only when a real data viz earns it)
Load D3 in `<head>` (`<script src="https://d3js.org/d3.v7.min.js"></script>`) and build a small chart inside a `<figure>`. Don't reach for D3 for something CSS/SVG can do. Reserve it for sliders that change a plot, animated transitions, or force-directed graphs that genuinely aid intuition.

## 12. Common mistakes
- **Citing a key that isn't in the `.bib`** → the citation renders blank. Cross-check every `<d-cite key>`.
- **Layout classes outside `<d-article>`** → they won't get the grid; keep content inside the article.
- **Unbalanced `$`** → KaTeX mis-parses; escape literal dollar signs as `\$`.
- **Heavy custom CSS** → fights the template. Only add styles for things Distill doesn't cover (Korean font, the toggle, demo highlights). Everything else: use the tags.
- **Forgetting `alt` text** and reader-facing captions → less accessible and off-voice.
