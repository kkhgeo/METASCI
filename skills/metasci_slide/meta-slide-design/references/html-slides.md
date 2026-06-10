# HTML Slides

Use this reference whenever `meta-slide-design` creates or revises a slide deck. HTML is the default output format unless the user explicitly asks for PPTX or another file type.

## Artifact Shape

- Create an `.html` slide deck with CSS in the same file or a nearby stylesheet.
- Keep images, fonts, and generated previews in a clear sibling folder such as `assets/` or `previews/`.
- Use relative asset paths so the deck folder can be moved.
- Use the Onto fixed-canvas slide format unless the user explicitly asks for a responsive web page: every `.slide` is authored at **1920px × 1080px** internally, and the viewport only scales the complete slide canvas.
- Do not size the slide canvas with `100vw`, `100vh`, `aspect-ratio`, `min-height`, or breakpoint-driven slide dimensions. Avoid `scroll-snap` deck navigation. Only one `.slide.active` should be visible.
- Core layout, typography, figure placement, and spacing should be stable in the 1920px × 1080px coordinate system. Use px or fixed CSS variables for slide geometry; use viewport units only outside the slide canvas, such as the page backdrop.

## Fixed Canvas Pattern

Use this structure for HTML decks:

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

Deck navigation may use keyboard, wheel, or buttons, but it should change the `.active` class rather than scrolling the document.

## Paperlogy Typography

Use Paperlogy as the Korean default:

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
:root {
  --font-ko: "Paperlogy", "Pretendard", system-ui, sans-serif;
}
body {
  font-family: var(--font-ko);
}
```

If local font files are unavailable, include a CDN Paperlogy stylesheet and keep Pretendard/system fonts as fallbacks.

## Slide Structure

- Use `<section class="slide ...">` for each slide.
- Cover slides must include a subject-relevant generated bitmap image and a dark overlay or gradient that keeps title text readable.
- Content slides should use meaningful Korean keyword titles and separate lead statement/subtitles.
- Do not put visible labels such as `00 / 발표 흐름`, `01 / 연구배경`, or `Slide 4` in normal slide headers.
- Section opener slides may use a large section number when it is part of the visual language.
- Explanation slides should usually have:
  - large Korean keyword title
  - colored lead statement
  - 2-4 grouped explanation blocks
  - one evidence figure/table/diagram
  - small source caption

## Verification

- Start a local server or open the HTML if it is fully static.
- Capture screenshots at 16:9 desktop size.
- Verify through the browser that the active slide's computed CSS `width` is `1920px`, computed CSS `height` is `1080px`, and exactly one `.slide.active` is visible.
- Check that Korean text uses Paperlogy or the intended fallback, lines do not overlap, and no text is clipped.
- Check that images load from relative paths.
- Final response should include the HTML path, preview/screenshot path, and any unresolved layout caveats.
