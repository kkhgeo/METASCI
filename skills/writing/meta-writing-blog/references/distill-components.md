# Distill v2 components — quick reference

The `assets/index.html` template already contains a working instance of every component below. This file is the *why/how* so you can edit confidently — copy structures from the template rather than retyping them.

## Document skeleton

One script in `<head>` registers all `<d-*>` components and injects the layout/typography CSS:

```html
<script src="https://distill.pub/template.v2.js"></script>
```

It needs network access at view time. Body order matters: `<d-title>` → `<d-byline>` → `<d-article>` → `<d-appendix>` → `<d-bibliography>`. Our `style.css` and the `<d-front-matter>` JSON go in `<head>`.

## Front-matter

Metadata is JSON in `<d-front-matter>` (in `<head>`): `title`, `description`, `authors[]`, and a `katex.delimiters` block that makes `$…$` / `$$…$$` render anywhere. Keep the delimiters block. (Full JSON is in the template.)

## Layout grid (the heart of the design)

Any block inside `<d-article>` gets its width from a layout class. Plain `<p>`/`<h2>` are already `l-body`; add a class only when you want a different width.

| Class | Width | Use for |
|---|---|---|
| `l-body` | text column (default) | paragraphs, small figures |
| `l-body-outset` | slightly wider | figures wanting emphasis |
| `l-middle` / `l-page` | wider / much wider | medium / large diagrams |
| `l-screen` / `l-screen-inset` | full-bleed / full-bleed with margin | hero visuals |
| `l-gutter` | right margin | margin notes |

`*-outset` variants exist for body/middle/page. Add `side` to float a block with text wrapping beside it.

## Margin notes

Side commentary in the right gutter, placed right after the paragraph it comments on:

```html
<div class="l-gutter"><p class="lang-ko">…</p><p class="lang-en">…</p></div>
```

## Figures

Wrap images in `<figure>` + a layout class, with an **objective** caption (academic register — describe what the figure shows, not "notice that…"). Credit reused figures. Author the Korean span first.

```html
<figure class="l-page">
  <img src="figures/x.png" alt="screen-reader description">
  <figcaption>
    <span class="lang-ko">그림은 …를 보여준다. 출처: …</span>
    <span class="lang-en">The figure shows …. Source: …</span>
  </figcaption>
</figure>
```

Inline SVG can replace `<img>` for crisp, themeable diagrams.

## Citations

Add BibTeX entries to `bibliography.bib`, point `<d-bibliography src="bibliography.bib">` at it, and cite inline — keys must match `@article{key,…}`:

```html
…prior work <d-cite key="key1,key2"></d-cite>.
```

Cite the paper itself plus its key references. (An inline `<script type="text/bibliography">` block also works if you prefer no separate file.)

## Footnotes

```html
…permutation-invariant<d-footnote>Reordering the inputs doesn't change the output.</d-footnote>.
```

Renders as a hoverable superscript, collected in the appendix.

## Math (KaTeX)

With the front-matter delimiters set: inline `$\mathcal{L} = -\sum_i y_i \log \hat{y}_i$`, block `$$ … $$`. Or the component form `<d-math>x</d-math>` / `<d-math block>…</d-math>`. Introduce math only *after* the prose idea it formalizes. Escape a literal dollar sign as `\$`.

## Appendix

After the article: "into the weeds" content and acknowledgments, then `<d-footnote-list></d-footnote-list>` and `<d-citation-list></d-citation-list>`.

## Interactivity (sparing in this register)

- **Language toggle** — already wired in `style.css` + the template's script (`body.show-en` / `.show-ko`, opens at KO). Don't remove it.
- **Hover highlight** — pure CSS/JS on inline SVG (`data-node` elements toggling a `.hot` class), as in the template. Use only if it teaches.
- **Minimal D3** — only when a real data visualization earns it; load `d3.v7.min.js` in `<head>`.

## Common mistakes

- A `<d-cite key>` not in the `.bib` renders blank — cross-check every key.
- Layout classes outside `<d-article>` get no grid.
- Unbalanced `$` makes KaTeX mis-parse; escape literal `$` as `\$`.
- Heavy custom CSS fights the template — only style what Distill doesn't cover (Korean font, toggle, demo highlights).
- Missing `alt` text or off-voice captions.
