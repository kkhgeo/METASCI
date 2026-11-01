# HTML Slides

Use this reference whenever `meta-slide-design` creates or revises a slide deck. HTML is
the default output format unless the user explicitly asks for PPTX or another file type.

Values referenced by name here live in `onto-tokens.md`. Slide skeletons live in
`slide-archetypes.md`. PDF export lives in `pdf-export.md`.

## Artifact Shape

- Create an `.html` slide deck with CSS in the same file or a nearby stylesheet.
- Keep images, fonts, and generated previews in a clear sibling folder such as `assets/`
  or `previews/`.
- Use relative asset paths so the deck folder can be moved.
- Export a PDF alongside the HTML. Both are deliverables.
- Use the Onto fixed-canvas format unless the user explicitly asks for a responsive web
  page: every `.slide` is authored at **1920px × 1080px** internally, and the viewport only
  scales the complete slide canvas.
- Do not size the slide canvas with `100vw`, `100vh`, `aspect-ratio`, `min-height`, or
  breakpoint-driven dimensions. Avoid `scroll-snap` deck navigation. Only one
  `.slide.active` should be visible.
- Core layout, typography, figure placement, and spacing should be stable in the
  1920 × 1080 coordinate system. Use px or fixed CSS variables for slide geometry; use
  viewport units only outside the slide canvas, such as the page backdrop.

## Fixed Canvas Pattern

```css
:root {
  --fixed-slide-w: 1920px;
  --fixed-slide-h: 1080px;
  --fixed-slide-scale: 1;
}

html,
body {
  width: 100%;
  height: 100%;
  margin: 0;
  overflow: hidden;
  scroll-snap-type: none;
}

body {
  background: #05070d;
}

.slide {
  position: fixed;
  left: 50%;
  top: 50%;
  width: var(--fixed-slide-w);
  height: var(--fixed-slide-h);
  min-width: var(--fixed-slide-w);
  min-height: var(--fixed-slide-h);
  overflow: hidden;
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  transform: translate(-50%, -50%) scale(var(--fixed-slide-scale));
  transform-origin: center center;
  isolation: isolate;
}

.slide.active {
  opacity: 1;
  visibility: visible;
  pointer-events: auto;
  z-index: 2;
}
```

```js
function updateSlideScale() {
  const scale = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
  document.documentElement.style.setProperty("--fixed-slide-scale", String(scale));
}
window.addEventListener("resize", updateSlideScale);
updateSlideScale();
```

Deck navigation may use keyboard, wheel, or buttons, but it should change the `.active`
class rather than scrolling the document.

## Typography

Paperlogy is the Korean default, loaded from local files with a CDN fallback:

```css
@font-face {
  font-family: "Paperlogy";
  src: url("assets/fonts/Paperlogy-4Regular.ttf") format("truetype");
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
@font-face {
  font-family: "Paperlogy";
  src: url("assets/fonts/Paperlogy-8ExtraBold.ttf") format("truetype");
  font-weight: 700 900;
  font-style: normal;
  font-display: swap;
}
```
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/fonts-archive/Paperlogy/Paperlogy.css">
```

The CDN alone is sufficient — a deck with no local font files still renders Paperlogy.
Ship the `@font-face` block anyway so a moved or offline folder keeps working.

Use the full stack, not a single variable. Each has a distinct job:

```css
:root {
  --f-display-ko: "Paperlogy", "Pretendard", "Archivo", sans-serif;   /* titles */
  --f-body:       "Paperlogy", "Pretendard", "Inter", sans-serif;     /* body */
  --f-mono:       "JetBrains Mono", ui-monospace, monospace;          /* labels, chrome */
  --f-ui:         "Space Grotesk", "Pretendard", sans-serif;
  --f-display:    "Archivo", "Paperlogy", sans-serif;                 /* numerals */
}
body { font-family: var(--f-body); }
```

`--f-display` on numerals against Paperlogy body text is a deliberate contrast — use it
where years, counts, or measurements should read as data.

Request only the Latin faces the deck actually uses. Every unused `family=` in the Google
Fonts URL is a render-blocking download for nothing.

## Slide Structure

- Use `<section class="slide ...">` for each slide, with an `aria-label` naming the slide.
- Apply one of the three modes: `.slide.dark`, `.slide-section-open`, or `.slide.paper`.
  Section openers are white and do not take `.paper`.
- Cover slides must include a subject-relevant generated bitmap and a dark overlay or
  gradient that keeps title text readable.
- Content slides use meaningful Korean keyword titles. The claim goes in the pull-quote or
  lead statement, not the title.
- Do not put visible labels such as `00 / 발표 흐름`, `01 / 연구배경`, or `Slide 4` in
  normal slide headers.
- Section opener slides may use a large section number — it is part of the visual language
  there and nowhere else.
- Explanation slides need only a title. Add a pull-quote, bullet stack, evidence figure, or
  two-column body according to the slide's job. Do not fill every region by default.

## Deck Chrome

The slide counter is created in JS and appended to `<body>`, formatted `01 / 32`:

```js
this.counter = document.createElement("div");
this.counter.className = "slide-counter";
document.body.appendChild(this.counter);
```

Toggle body classes in the navigation handler so mode-dependent chrome can respond:

```js
const s = this.slides[idx];
document.body.classList.toggle("is-section-open", s.classList.contains("slide-section-open"));
document.body.classList.toggle("is-thankyou",     s.classList.contains("slide-thankyou"));
document.body.classList.toggle("is-paper",        s.classList.contains("paper"));
```

Give the counter a mode-aware color. A single ivory value is invisible on the light slides,
which are the majority of any Onto deck.

## Verification

- Start a local server, or open the HTML if it is fully static.
- Capture screenshots at 16:9 desktop size.
- Verify in the browser that the active slide's computed `width` is `1920px`, computed
  `height` is `1080px`, and exactly one `.slide.active` is visible.
- Check that Korean text uses Paperlogy and not a fallback, that lines do not overlap, and
  that no text is clipped.
- Check that slide titles render at 72px. If a title comes out smaller, a base declaration
  is winning over the intended size.
- Check the slide counter is legible on both dark and light slides.
- Check that images load from relative paths.
- Export the PDF and verify it per `pdf-export.md` — page count, page size, dark slides
  still dark, fonts correct.
- Final response should include the HTML path, the PDF path, the preview/screenshot path,
  and any unresolved layout caveats.
