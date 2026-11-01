# Slide Archetypes

The Onto deck is built from six archetypes across three modes. Read `onto-tokens.md` first
for the values referenced here.

Counts below are from the finished 32-slide deck: 1 cover + 1 contents + 5 section openers
+ 18 overview + 6 method + 1 closing.

| Archetype | Class | Mode | Count |
|---|---|---|---|
| Cover | `slide dark slide-cover` | dark | 1 |
| Contents | `slide dark slide-contents` | dark | 1 |
| Section opener | `slide slide-section-open` | section | 5 |
| Overview / explanation | `slide paper overview overview-background` | paper | 18 |
| Method | `slide paper method method-*` | paper | 6 |
| Closing | `slide dark slide-thankyou` | dark | 1 |

Overview and method are the workhorses. Do not invent a seventh archetype to fit content —
route the content to one of these, or split the slide.

---

## Mode base rules

### dark

The entire dark contract is two lines. Everything else on a dark slide is slide-specific.

```css
.slide{ isolation: isolate; }
.slide.dark{ background: var(--bg); color: var(--ink); }
```

### paper

```css
.slide.paper{
  background: var(--paper-bg);
  color: var(--paper-ink);
}
.slide.paper .slide-content{
  position: relative;
  z-index: 5;
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  grid-template-rows: 1fr;
  justify-items: start;
  justify-content: flex-start;
}
.slide.paper::before{               /* ambient tint */
  content:''; position:absolute; inset:0; pointer-events:none; z-index:1;
  background:
    radial-gradient(ellipse 80vw 60vh at  8% 18%, rgba(0,164,139,.07) 0%, transparent 70%),
    radial-gradient(ellipse 70vw 55vh at 96% 92%, rgba(0,159,222,.06) 0%, transparent 70%);
}
.slide.paper::after{                /* paper grain — keep this, it does real work */
  content:''; position:absolute; inset:0; pointer-events:none; z-index:2;
  opacity:.025; mix-blend-mode: multiply;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .5 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
}
```

The grain at 2.5% opacity is what keeps a white slide from looking like a bare browser
page. It is subtle enough to survive PDF export.

### section

Section openers are white and do **not** take `.paper`.

```css
.slide-section-open{
  background: var(--section-bg);
  color: var(--section-ink);
}
.slide-section-open::before{
  content:''; position:absolute; inset:0; pointer-events:none; z-index:1;
  background: linear-gradient(180deg, #FFFFFF 0%, #FFFFFF 68%, var(--section-ash) 100%);
}
```

---

## Cover

Job: name the work and establish the subject visually.

```
.slide-cover
├── .cover__right                     ambient zone, x = 720…1920
├── canvas.presentation-sparks        particle field
├── .slide-content                    grid: rows auto 1fr auto, justify-items start
│   ├── .cover__top > .cover__brand > svg          institutional logo
│   ├── .cover__main                  column, margin-left 70px, max-width 1280px,
│   │   │                             translateY(-92px)  ← above optical center
│   │   ├── .cover__badge
│   │   ├── h1.cover__title > span.line-a + span.line-b.accent
│   │   ├── p.cover__subtitle
│   │   ├── .cover__divider
│   │   └── .cover__date-row > span.cover__project-meta + span.cover__date
│   ├── .cover__mondrian-logo--corner   grid wordmark
│   └── .cover__bottom > .background-note (__title / __source / __desc)
└── .cover__bottom-bar                1920 × 6 gradient rule
```

Rules:

- Always generate a subject-relevant bitmap for the cover. The image must show the actual
  topic or a faithful visual metaphor, never generic atmosphere.
- Title at `--fs-cover` (76px/700), split across two spans so the second can take the
  chapter accent.
- `.background-note` credits the cover image. Keep it small and bottom-aligned.
- The main block sits above optical center (`translateY(-92px)`), not centered.

---

## Contents

Job: orient. Use only when the deck is long enough to need it, or the user asks.

```
.slide-contents
├── .contents__bg                     full-bleed image, center/cover
└── .slide-content > .contents__main  column, margin-left 66px, margin-top 82px,
    │                                 max-width 1080px
    ├── h1.contents__title
    ├── .contents__rule
    └── ul.contents__list             gap 32px
        └── li
            ├── span.num              44px/650, accent, min-width 78px
            └── span.label > span.ko (44px) + span.en (22px)
```

Use real section names. Never a mechanical label like `00 / 발표 흐름`.
The bilingual `ko` + `en` pair on each item is part of the house style.

---

## Section opener

Job: mark a chapter boundary and state its claim. This is the **only** place a declarative
phrase may dominate a slide, and the only place a section number is allowed.

```
.slide-section-open
└── .slide-content > main.section-open-content
    ├── h1.section-open-title > span.num + text
    │     ::after  →  168 × 4px solid accent, margin-top 28px
    └── p.section-open-statement
          ::before →  Georgia “ at 104px, absolute
          ├── span.quiet    block, accent color
          └── span.strong   block, margin-top 13px, ink, 760
```

```css
.section-open-content{
  position: relative; z-index: 2;
  width: 100%; height: 100%;
  display: flex; flex-direction: column; justify-content: center;
  padding-left: 142px;
  transform: translateY(-92px);
}
.section-open-title{
  font-family: var(--f-display-ko);
  font-size: var(--fs-section);      /* 74px */
  line-height: 1; font-weight: 850;
  color: var(--section-ink);
  margin-bottom: 58px;
}
.section-open-title .num{ color: var(--ch0N-accent); }
.section-open-title::after{
  content:""; display:block;
  width: 168px; height: 4px; margin-top: 28px;
  background: var(--ch0N-accent);
}
.section-open-statement{
  position: relative;
  max-width: 1120px; padding-left: 84px;
  font-family: var(--f-display-ko);
  font-size: var(--fs-statement);    /* 54px */
  line-height: 1.24; font-weight: 650;
  color: var(--section-ink);
  word-break: keep-all;
}
.section-open-statement::before{
  content: "\201C";
  position: absolute; left: 16px; top: -14px;
  font-family: Georgia, "Times New Roman", serif;
  font-size: var(--fs-quote-glyph);  /* 104px */
  line-height: 1; font-weight: 700;
  color: var(--ch0N-accent);
}
.section-open-statement .quiet { display:block; font-weight: 650; color: var(--ch0N-accent); }
.section-open-statement .strong{ display:block; margin-top: 13px; font-weight: 760; }
```

The chapter accent is declared **here** and inherited by the chapter's body slides.

Openers may mirror to the right for visual variety across chapters. Mirror the padding,
the rule, and the quote glyph together:

```css
.section-open--right .section-open-content{
  align-items: flex-end; text-align: right;
  padding-left: 0; padding-right: 142px;
  transform: translateY(-54px);
}
.section-open--right .section-open-title::after{ margin-left: auto; }
.section-open--right .section-open-statement{
  padding-left: 0; padding-right: 84px; max-width: 1180px;
}
.section-open--right .section-open-statement::before{
  content: "\201D"; left: auto; right: 12px;
}
```

Use the mirror sparingly — once or twice in a deck, as a rhythm change.

---

## Overview / explanation

Job: explain one concept and its direct evidence. The workhorse — 18 of 32 slides.

```
.slide.paper.overview.overview-background
└── .slide-content                          padding: var(--frame)
    └── main.overview-shell                 grid, rows auto 1fr, gap 30px
        ├── header.overview-head            ── GUARANTEED
        │   ├── h1.overview-title           ── GUARANTEED
        │   ├── .overview-quote--mark       optional  (6 of 18)
        │   └── p.overview-lead             optional  (2 of 18)
        └── section.overview-body           optional (10 of 18)
            grid, columns .92fr 1.08fr, gap 48px, align-items start
            ├── .problem-stack              optional (5 of 18), grid, gap 36px
            │   └── .problem-row--bullet > div
            │       ├── h2.problem-title    34px/700
            │       ├── p.problem-text      26px/400, carries <mark>
            │       └── p.problem-meta      22px, > span.meta-accent
            └── figure                      evidence object
```

**The guaranteed contract is shell + head + title.** Everything below is optional, and the
deck uses each optional part on a minority of slides. Do not force a two-column body onto
every slide — that is the most common way this archetype goes wrong.

Choose the body by the slide's job:

- **No body at all** — the title plus a pull-quote is a complete slide when the point is a
  single assertion. 8 of 18 slides do this.
- **Two-column** (`.overview-body`) — only when a large figure must stay visible while the
  audience reads the explanation.
- **Bullet stack** (`.problem-stack`) — 2–3 parallel ideas, stages, or implications.
- **Bottom evidence band** — text establishes context, figure lands as proof.

Titles do **not** get a rule underneath. `.overview-title` has no `::after`; 15 of the 18
slides render with no rule. Only the platform chapter draws one, as a chapter signature:

```css
[class*="chapter-platform"] .overview-title::after{
  content:""; display:block;
  width: 1380px; max-width: 100%; height: 2px; margin-top: 16px;
  background: linear-gradient(90deg,
    var(--ch05-accent) 0%, rgba(237,66,69,.4) 36%,
    rgba(12,19,34,.18) 70%, rgba(12,19,34,0));
}
```

### The pull-quote — the single highest-value component

Used on 6 slides and aliased in two other places. This is the deck's signature move: a
large accent-colored assertion sitting where a lead statement would go.

```css
.overview-quote--mark{
  position: relative;
  font-family: var(--f-display-ko);
  font-size: var(--fs-quote);        /* 48px */
  font-weight: 760;
  line-height: 1.24;
  color: var(--ch0N-accent);
  padding-left: var(--indent-text);  /* 28px — aligns with bullet text below */
  margin-top: 28px;
  max-width: 1320px;
  word-break: keep-all;
}
.overview-quote--mark::before{
  content: "\201C";
  position: absolute;
  left: -22px;                       /* hangs in the margin so text stays on the 28px edge */
  top: -0.14em;
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.46em;
  font-weight: 700;
  line-height: 1;
  color: var(--ch0N-accent);
}
```

The hanging quote glyph is the detail that makes it work — the ornament sits outside the
text column so the optical left edge stays aligned with everything below it.

---

## Method

Job: explain a process, pipeline, or technical construction. The tightest archetype —
all 6 slides share the same four elements.

```
.slide.paper.method.method-*
└── .slide-content                    padding: var(--frame)
    └── main.method-shell             grid, rows auto auto auto 1fr auto, gap 22px
        ├── header.method-head        flex, space-between, align-items flex-start, gap 56px
        │   └── h1.method-title       ← the ONLY child. No kicker, no tag, no lead.
        ├── .method-rule
        └── ul.method-bullets  /  a figure
```

```css
.method-rule{
  height: 2px;
  background: linear-gradient(90deg,
    rgba(12,19,34,.55), rgba(12,19,34,.20) 66%, transparent);
}
.method-bullets{
  list-style: none;
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  row-gap: 10px;
  max-width: 1636px;
}
.method-bullets li{
  position: relative;
  padding-left: 22px;
  font-size: var(--fs-lead);         /* 28px */
  font-weight: 500;
  line-height: 1.8;
  letter-spacing: -0.014em;
  color: rgba(12,19,34,.88);
  word-break: keep-all;
}
.method-bullets li::before{
  content:""; position:absolute; left:0; top:.6em;
  width:8px; height:8px; border-radius:50%;
  background: var(--paper-cyan);
}
.method-bullets strong{ color: var(--paper-ink); font-weight: 800; }
.method-bullets mark{
  background: var(--mark-yellow);
  color: inherit;
  padding: 2px 6px;
  border-radius: 3px;
}
.method-bullets li.sub{ font-size: var(--fs-body-sm); padding-left: 36px; }
.method-bullets li.sub::before{ display: none; }
```

Note `line-height: 1.8` — method bullets are set much looser than overview body text
(1.55). That air is what keeps a dense technical list readable from a projector.

Method slides carry `--ch03-accent` regardless of which chapter they sit in. The method
sequence reads as its own territory.

For pipeline-shaped content, switch the shell to a flat stack:

```css
.method--stacked .method-shell{
  grid-template-rows: auto auto auto auto auto;
  gap: 16px;
  align-content: start;
}
```

---

## Closing

```
.slide-thankyou                       background #07100d, no .slide-content
├── video.thankyou-video              full-bleed, object-fit cover,
│                                     filter: saturate(1.15) contrast(1.05) brightness(.92)
├── ::before                          two-layer scrim
├── canvas                            sparks, z-index 2
└── .thankyou-shell                   absolute inset 0, z-index 3,
                                      grid rows 1fr auto, padding 96px 126px 78px 132px
```

Give the video a `poster` so the slide is not blank in the PDF export. `body.is-thankyou`
hides the slide counter.
