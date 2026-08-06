# House Style: Onto-Inspired Research Decks

Use this reference when the user wants the design feeling of the Onto presentation
reflected in a new or revised deck.

**Read `onto-tokens.md` first.** It holds the color, type, motion, and geometry values this
document refers to by name. This file covers composition and judgment; that file covers
values.

## Visual Character

- Institutional research tone, not marketing.
- Large, heavy Korean titles with calm analytical layouts.
- HTML slide deck is the default implementation format, exported to PDF alongside. Design
  should be expressed in CSS and verified by rendered screenshots.
- HTML slides behave like a fixed presentation file, not a responsive web page: author each
  slide on a 1920×1080 canvas and scale the whole slide to fit the browser.
- Paperlogy is the default Korean typeface for titles and body. Pretendard is fallback only.
- Strong left-aligned structure for explanation slides.
- Titles are keyword-centered, not declarations. The slide's claim belongs in the pull-quote
  or lead statement.
- Section openers use sparse composition: section number, one quoted phrase, ample space.
- Avoid making every content slide a two-column split. Vary the body area with rows,
  evidence bands, and card groups according to the slide job.

## Three Modes

The deck has three slide modes, not two. Getting this wrong is the most common
misunderstanding of the house style.

| Mode | Used by | Background |
|---|---|---|
| `dark` | cover, contents, closing | `--bg` `#070A14` |
| `section` | section openers | `--section-bg` `#FFFFFF` |
| `paper` | all content slides | `--paper-bg` `#FFFFFF` |

Section openers are **white**. They do not take the `.paper` class and inherit none of its
tokens or texture. Dark is reserved for the three framing moments — opening, orientation,
and close — which is what gives those moments their weight.

## Chapter Colors

One accent per chapter, declared on the section opener, inherited by every body slide in
that chapter. Chapter colors identify conceptual territory; they are not decoration and
they do not change slide to slide.

| Accent | Territory |
|---|---|
| `--ch01-accent` `#3E6AE1` | overview, framework, background |
| `--ch02-accent` `#00AB84` | ontology, semantic integration, knowledge infrastructure |
| `--ch03-accent` `#FF6A1A` | policy KG, GraphRAG, pipeline and method |
| `--ch04-accent` `#7A8F00` | gridded environmental data, monitoring networks |
| `--ch05-accent` `#ED4245` | public information, media, platform integration |

Method slides carry `--ch03-accent` wherever they appear — the method sequence reads as its
own territory. A multi-slide sub-thread inside a chapter may take its own accent
(`--soil-accent` `#7A5230` does), but only across several consecutive slides.

The deck retains neutral paper and dark ink as its base. Each chapter has a dominant
accent; no chapter is monochrome.

## Layout Patterns

Full skeletons and CSS are in `slide-archetypes.md`. What follows is the judgment layer.

### Cover

Always generate a subject-relevant bitmap. Prefer a full-bleed environmental, geospatial,
or institutional image with a dark gradient. Korean title left, English subtitle beneath,
date/team line below, logo in the corners, image credit at the bottom. The image must show
the actual topic or a faithful visual metaphor, not generic atmosphere.

### Contents

Use only when the deck is long enough to need orientation, or the user asks. Give it real
section names with the Korean/English pair. Never a mechanical label like `00 / 발표 흐름`.

### Section Opener

A nearly blank slide: large section number and name, one quoted lead phrase, accent rule,
generous space. This is the only place a declarative phrase may dominate a slide, and the
only place a section number is allowed. Openers may mirror right occasionally as a rhythm
change — once or twice per deck.

### Explanation Slide

The guaranteed structure is **title only**. Everything else is chosen by the slide's job:

1. Top-left keyword title, usually 2–6 Korean words, at `--fs-title`.
2. Optionally a pull-quote (`--fs-quote`, chapter accent) carrying the claim — this is the
   deck's signature move and works as a complete slide on its own.
3. Optionally a body: bullet stack for 2–3 parallel ideas, two-column only when a large
   figure must stay visible while the audience reads, bottom evidence band when text
   establishes context first.
4. Small source/caption aligned with the evidence.

**Titles do not take a rule underneath.** In the source deck 15 of 18 explanation slides
render with no rule under the title; the platform chapter draws one as its chapter
signature. Do not add a title rule by default. Method slides get their rule from a separate
element (`.method-rule`) directly beneath the header, which is a different device.

### Method Slide

Title, rule, bullets or figure. The tightest pattern in the deck — all six method slides
share exactly these elements. Bullets are set loose (`line-height: 1.8`) so a dense
technical list stays readable from a projector.

### Framework Slide

Boxed modules connected by arrows. Make the system's final output or decision-support value
visibly downstream. If the diagram has many modules, add a caption stating how to read it.

### Evidence/Data Slide

A chart or map as the main object with 1–3 callouts. Annotate only what the argument needs.
If a table is necessary, highlight only the row or column that supports the point.

### Closing

Dark, full-bleed video or image with a scrim. Give any video a `poster` so the PDF export
is not blank.

## Typography and Emphasis

- Paperlogy for Korean titles and body. Local `@font-face` first, CDN as fallback.
- Slide titles land at `--fs-title` (72px). This is where all three title archetypes
  converge — treat it as the default, not a maximum.
- Body text smaller but legible from a projector. `word-break: keep-all` on every Korean
  block.
- **Emphasis is carried by the highlight pen, not by weight.** Pair `<mark>` with a weight
  suppressor so `<strong>` inside highlighted text does not compound. Mint for analytical
  text, yellow for bullets, lavender for tags.
- Use highlights as the live reading path, not decoration.
- Captions and citations small, light, aligned to the figure.
- English technical terms where they are domain-standard, paired with Korean explanation
  when comprehension matters.

## Motion

Entrance animation belongs to the cover and contents slides only. In the source deck the
29 content slides have no reveal at all, and that restraint is part of the tone — an
institutional deck that animates every bullet reads as a pitch. Add reveals to content
slides only when asked.

## Anti-Patterns

- Producing PPTX by default when the user expects HTML slides.
- Shipping HTML without the PDF export.
- Treating section openers as dark slides.
- Adding a rule under every slide title.
- Using visible meta labels such as `00 / 발표 흐름`, `01 / 방법`, or `Slide 3` as headings.
- Writing normal slide titles as declarations such as "물질수지는 관리 위치를 말하지 못함";
  use "물질수지와 관리 위치" as the title and put the declaration in the pull-quote.
- Replacing a technical explanation with slogan-like bullets that omit the source logic.
- Making a title slide without a generated image.
- Defaulting every explanation slide to a two-column split.
- Dense body text with no visual anchor.
- Tables used as storage instead of argument.
- Multiple unrelated visuals competing on one slide.
- Decorative cards inside cards; rounded cards generally — the deck's corner radius is
  essentially zero.
- One-hue monotony, or conversely an accent that changes slide to slide within a chapter.
- Important service/platform implication appearing only at the end with no earlier preview.
