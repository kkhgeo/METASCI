# Onto Design Tokens

Single source of truth for the Onto house style. Read this **before** any other design
reference when building or revising an Onto-style deck.

Every value here is derived from the **rendered output** of the finished Onto deck
(32 slides), not from its CSS declarations. The two differ — see "Dead declarations" below.

---

## Modes

The deck has **three** slide modes, not two.

| Mode | Class | Count | Background | Ink |
|---|---|---|---|---|
| dark | `.slide.dark` | 3 | `--bg` | `--ink` |
| section | `.slide-section-open` | 5 | `--section-bg` | `--section-ink` |
| paper | `.slide.paper` | 24 | `--paper-bg` | `--paper-ink` |

`dark` carries the cover, contents, and closing slides. `section` carries the section
openers — it is **white**, and it does **not** take the `.paper` class, so it inherits
none of the `--paper-*` tokens and none of the paper noise texture. `paper` carries all
24 content slides.

Do not describe this as a "dark vs paper" duality. Section openers are their own mode.

---

## Color

### Mode base

```css
--bg:          #070A14;   /* dark slide background */
--ink:         #F3EBDC;   /* dark slide ink (ivory) */

--section-bg:  #FFFFFF;   /* section opener background */
--section-ink: #171A20;   /* section opener ink */
--section-ash: #F4F4F4;   /* section opener bottom gradient stop */

--paper-bg:    #FFFFFF;   /* content slide background */
--paper-ink:   #0C1322;   /* content slide ink — the most-used color in the deck */
```

`--paper-ink` derivatives, all `rgba(12,19,34,α)`:

```css
--paper-soft:      rgba(12,19,34,.74);   /* de-emphasized body */
--paper-mute:      rgba(12,19,34,.55);   /* meta, source lines */
--paper-faint:     rgba(12,19,34,.32);   /* inactive */
--paper-line:      rgba(12,19,34,.18);   /* rules */
--paper-line-soft: rgba(12,19,34,.10);   /* faint rules */
```

### Chapter accents

The organizing rule: **one accent per chapter, declared on the section opener, inherited
by every body slide in that chapter.** Follow it. Do not assign accents per slide.

```css
--ch01-accent: #3E6AE1;   /* 연구개요 — overview, framing */
--ch02-accent: #00AB84;   /* 온톨로지 — semantic integration */
--ch03-accent: #FF6A1A;   /* 지식그래프 RAG — also all method slides */
--ch04-accent: #7A8F00;   /* 환경 격자정보 — monitoring, gridded data */
--ch05-accent: #ED4245;   /* 공공정보·플랫폼 */
--soil-accent: #7A5230;   /* sub-thread inside ch04 */
--paper-cyan:  #00A48B;   /* neutral accent — bullet dots, small marks */
```

A sub-thread inside a chapter may take its own accent (`--soil-accent` does), but only
when it spans several consecutive slides.

### Highlight pens

```css
--mark-mint:     rgba( 80,240,215,.70);   /* problem/analysis text */
--mark-yellow:   rgba(240,255, 30,.85);   /* bulleted lists */
--mark-lavender: rgba(200,175,250,.70);   /* timeline tags */
```

**Emphasis is carried by the pen, not by weight.** Pair every highlight with a weight
suppressor so `<strong>` inside highlighted text does not compound the emphasis:

```css
.problem-text mark   { font-weight: inherit; }
.problem-text strong { font-weight: 400; }
```

`<mark>` is the most-used device in the deck (76 elements). Use it as the live reading
path, not as decoration.

---

## Type scale

Rendered sizes, with the class that establishes each step.

| Token | px | Weight | Established by |
|---|---|---|---|
| `--fs-quote-glyph` | 104 | 700 | `.section-open-statement::before` (Georgia glyph) |
| `--fs-cover` | 76 | 700 | `.cover__title` |
| `--fs-section` | 74 | 850 | `.section-open-title`, `.contents__title` (800) |
| `--fs-title` | **72** | 800–850 | `.overview-title`, `.method-title` — the convergence point |
| `--fs-statement` | 54 | 650 | `.section-open-statement` |
| `--fs-quote` | 48 | 760 | `.overview-quote--mark` |
| `--fs-list` | 44 | 650 | `.contents__list li` |
| `--fs-subtitle` | 34 | 700 | `.problem-title` |
| `--fs-lead` | 28 | 400–500 | `.overview-lead`, `.method-bullets li` |
| `--fs-body` | 26 | 400 | `.problem-text` |
| `--fs-body-sm` | 25 | 400 | `.method-bullets li.sub` |
| `--fs-meta` | 22 | 400 | `.problem-meta` |
| `--fs-caption` | 20 | 400 | figure captions, sources |
| `--fs-label` | 18 | 700 | mono, `.12em` tracking, uppercase |
| `--fs-chrome` | 12 | 400 | `.slide-counter` |

`--fs-title` at 72px is where all three title archetypes actually land. Use it as the
default slide title size.

Every Korean text block takes `word-break: keep-all`.

---

## Type — fonts

```css
--f-display-ko: 'Paperlogy', 'Pretendard', 'Archivo', sans-serif;   /* titles */
--f-body:       'Paperlogy', 'Pretendard', 'Inter', sans-serif;     /* body */
--f-mono:       'JetBrains Mono', 'Paperlogy', ui-monospace, monospace;  /* labels, chrome */
--f-ui:         'Space Grotesk', 'Pretendard', sans-serif;
--f-display:    'Archivo', 'Paperlogy', sans-serif;                 /* numerals */
```

Load Paperlogy with local files first and the CDN as fallback:

```css
@font-face{ font-family:'Paperlogy'; src:url('assets/fonts/Paperlogy-4Regular.ttf') format('truetype');
            font-weight:400; font-style:normal; font-display:swap; }
@font-face{ font-family:'Paperlogy'; src:url('assets/fonts/Paperlogy-8ExtraBold.ttf') format('truetype');
            font-weight:700 900; font-style:normal; font-display:swap; }
```
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/fonts-archive/Paperlogy/Paperlogy.css">
```

The CDN alone is sufficient — a deck with no local font files still renders Paperlogy.
Ship the `@font-face` block anyway so a moved folder keeps working offline.

Weights in use: 400, 500, 520, 560, 620, 650, 680, 700, 720, 750, 760, 800, 820, 850.
The ExtraBold face is declared `font-weight: 700 900`, so anything in that range resolves
to it.

Request only the Latin faces you actually use. The source deck requests Orbitron and never
uses it — do not copy that.

**Every stack that may carry Korean needs a Korean face in it.** CSS font fallback resolves
per glyph, so a mono stack without Paperlogy sends each Korean character in a label to a
Windows system font — GulimChe — while the Latin characters stay in the mono face. The
label ends up set in two unrelated typefaces, and the system font is embedded into the PDF.
Verify by listing the fonts embedded in the exported PDF: anything named Gulim, Batang,
Dotum, or Malgun means a stack is missing its Korean fallback.

Math and arrow glyphs (`⊕`, `→`, `−`, superscripts, subscripts) are absent from Paperlogy
and fall through to a symbol font. Append `'Segoe UI Symbol'` to the display and body stacks
so they all land in the same one instead of whatever each glyph resolves to individually.

**When the deck must render identically off-network**, drop the CDN Latin faces entirely:
use `ui-monospace, 'Consolas', 'Paperlogy', monospace` for labels and let `--f-display` fall
back to Paperlogy. The numeral contrast is worth less than a deck that renders in the room
the way it did on the authoring machine. Google Fonts in particular has proven unreliable
inside headless PDF export.

---

## Motion

```css
--ease-out: cubic-bezier(0.16, 1, 0.3, 1);
--duration-normal: 0.6s;
```

```css
.reveal{
  opacity: 0;
  transform: translateY(30px);
  transition: opacity var(--duration-normal) var(--ease-out),
              transform var(--duration-normal) var(--ease-out);
}
.slide.visible .reveal{ opacity: 1; transform: translateY(0); }
.slide.visible .reveal:nth-child(1){ transition-delay: 0.10s; }
.slide.visible .reveal:nth-child(2){ transition-delay: 0.25s; }
.slide.visible .reveal:nth-child(3){ transition-delay: 0.40s; }
.slide.visible .reveal:nth-child(4){ transition-delay: 0.55s; }
```

**Apply `.reveal` to the cover and contents slides only.** In the source deck the 29
content slides have no entrance animation at all. Adding staggered reveals to content
slides is a new design decision, not part of the house style — do it only if asked.

---

## Geometry

```css
--frame:       76px 142px 72px 142px;   /* content frame — overview and method share it */
--indent-text: 28px;                    /* universal text indent */
```

`--indent-text` is a single optical alignment edge shared by six components
(`.problem-row--bullet > div`, `.platform-bullets li`, `.measurement-summary__item`,
`.overview-quote--mark`, `.overview-lead--aligned`, `.platform__lead-quote`). Keep new
components on it.

Other recurring geometry:

```
section rule    168px × 4px, solid accent, margin-top 28px
bullet dot      8px, border-radius 50%, top .6em
```

Corner radius is essentially zero by design: `50%` appears 29× and is always a dot; `2px`
16×; `0` 9×; `3px` 8× (highlight padding). Only one component softens to `10px`. Do not
introduce rounded cards.

---

## Chrome

```css
.slide-counter{
  position: fixed; right: 18px; bottom: 14px; z-index: 10;
  font-family: var(--f-mono);
  font-size: var(--fs-chrome);
  letter-spacing: .12em;
  pointer-events: none;
  color: rgba(243,235,220,.55);              /* dark mode */
}
body.is-paper .slide-counter,
body.is-section-open .slide-counter{
  color: rgba(12,19,34,.45);                 /* light modes */
}
body.is-thankyou .slide-counter{ display: none; }
```

Format is `01 / 32`, zero-padded, built in JS and appended to `<body>`.

The source deck sets the counter to ivory unconditionally, which makes it nearly invisible
on its 29 light slides. That is a bug, not a style — the mode-aware rule above is the
correct behavior. Toggle the body classes in the navigation handler alongside
`is-section-open` and `is-thankyou`.

---

## Dead declarations — do not carry these over

A large slice of the source CSS never renders. When lifting patterns from the deck, check
against this list first.

**Base sizes overridden everywhere.** `.overview-title` declares 64px but every one of the
18 instances is overridden to 72/50/44. `.method-title` declares 54px but all 6 render at
72px. `.overview-lead` declares 32px and renders at 28px. Use the rendered values.

**A background that never appears.** `.slide.paper` declares `--paper: #e9edf2`, but
`.overview-background` overrides it to `#ffffff`. No content slide renders the grey paper
tone. Only the noise texture survives.

**Classes with zero instances in the markup** — roughly 60 rules:
`.method-lead` · `.method-kicker` · `.method-tag` · `.overview-kicker` · `.overview-step` ·
`.overview-foot` · `.problem-index` · `.section-title` · `.title-rule` ·
`.slide.paper .section-main` · `.principle` · `.kg-concept-note` · `.kg-compare` ·
`.visual-placeholder` · `.cover__rule` · bare `.overview-quote`

This matters for archetype extraction: the CSS implies a header slot of
kicker + title + tag + lead, but the real `.method-head` contains **only**
`<h1 class="method-title">`.

**Unused tokens:** `--amber-mid`, `--line`, `--f-word` (and the Orbitron webfont request
that `--f-word` would have needed).
