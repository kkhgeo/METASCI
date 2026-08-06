---
name: meta-slide-design
description: Explore, design, implement, and visually review Korean research slide decks in the Onto house style. Use when Codex needs early design direction options, Onto design tokens, Paperlogy typography, HTML slide implementation, cover/section/overview/method layouts, PDF export, visual redesign, screenshot verification, or design execution from an approved meta-slide-content specification.
---

# Meta Slide Design

Use this skill to translate an approved slide content specification into visual design and
HTML implementation. Default to **HTML slides** unless the user explicitly asks for PPTX,
PDF-only, Keynote, or another format. Use `references/onto-tokens.md` and
`references/house-style.md` as the Onto house format unless another style is requested.
The user's Onto design is the baseline principle, but early design exploration should offer
several creative directions that still respect the house style. If the source content is
not yet structured into a deck promise, narrative spine, slide jobs, keyword titles, lead
statements, body blocks, and evidence map, use `meta-slide-content` first.

## Output Defaults

- Produce a self-contained or folder-contained **HTML slide deck** as the primary artifact,
  with a **PDF export alongside it**. Both are deliverables.
- Use a fixed 16:9 slide canvas: each slide's internal coordinate system is
  **1920px × 1080px**, and the browser scales the whole canvas to fit the viewport. Do not
  use responsive slide sizing that changes internal layout unless the user explicitly asks
  for a web page or scroll article.
- Use **Paperlogy** as the default Korean font, via local `@font-face` with CDN fallback.
  Use the full five-variable font stack from `references/onto-tokens.md`, not a single
  variable.
- Take all color, type, motion, and geometry values from `references/onto-tokens.md`.
  Do not invent values or lift them from an existing deck's CSS — that deck's base
  declarations may be overridden and never render.
- Use **keyword-centered slide titles**, not declarative sentence titles. Render the
  approved lead statement as the pull-quote or lead line.
- Do not use visible meta labels such as `00 / 발표 흐름`, `01 / 연구 배경`, or `Slide 1` as
  normal slide headings. Section numbers are allowed only on sparse section opener slides.
- When creating a new deck or replacing a weak/missing cover, generate or select a
  subject-relevant bitmap image for the cover and place it as the main visual.
- Preserve the approved Korean content. Only adjust wording when text does not fit or blocks
  comprehension, and surface the change.

## Mode Decision

First classify the deck.

- **Explanatory mode**: Use when the deck must also work as a readable handout, research
  report, institutional briefing, technical review, proposal defense, or policy/research
  explanation. Allow full explanatory sentences, definitions, citations, tables, and staged
  reasoning, but keep a strong hierarchy and visible takeaway.
- **Visual mode**: Use when the deck is mainly for live presentation, persuasion, keynote,
  teaching, demo, or audience memory. Prefer one central idea, large visuals, diagrams,
  spatial metaphors, progressive reveal, and short keyword titles with a separate takeaway.
- **Hybrid mode**: Use when the user needs both. Make the screen version visual-first and
  place explanatory detail in notes, appendix, backup slides, or handout sections.

If the user does not specify a mode, infer it from audience, setting, duration, and whether
the file must stand alone after the talk.

## Core Workflow

1. Confirm the approved content specification or existing deck structure: audience, purpose,
   delivery setting, deck promise, slide jobs, keyword titles, lead statements, body blocks,
   and evidence objects.
2. If those content elements are missing, use `meta-slide-content` before starting visual
   design.
3. Choose references in this order:
   - **Always, before anything else**: `references/onto-tokens.md` for values.
   - Onto-style research or institutional decks: `references/house-style.md`.
   - Slide construction: `references/slide-archetypes.md`.
   - Early creative direction review: `references/design-exploration.md`.
   - HTML creation, conversion, or revision: `references/html-slides.md`.
   - PDF deliverable: `references/pdf-export.md`.
   - Explanatory slide design from an approved content spec: `references/explanatory-slides.md`.
   - Live/keynote redesign: `references/visual-slides.md`.
   - Building an explanatory figure: `references/figure-patterns.md`.
   - Presentation-design rationale or edge cases: `references/research-notes.md`.
4. Before implementation, propose 2–4 design directions. Each must respect the Onto house
   style while varying rhythm, evidence treatment, section openers, density, and visual
   emphasis. Ask the user to choose or combine directions.
5. Use the chosen direction and supplied narrative spine to choose the deck's visual rhythm:
   cover, contents, section openers, overview slides, method slides, and close.
6. Confirm each slide job and select the matching archetype; do not invent content to make a
   layout work, and do not invent a seventh archetype.
7. Preserve keyword titles and lead statements from the content specification unless a
   wording issue blocks comprehension.
8. For substantial decks, create representative style frames or first-pass screenshots
   before completing every slide.
9. Check density and attention path. If the audience cannot tell where to look first within
   2 seconds, simplify the visual hierarchy or send the slide back to `meta-slide-content`
   for a split.
10. Implement the HTML, export the PDF, and verify rendered screenshots before final
    delivery.

## Interaction Rules

Use this design interaction sequence by default:

1. Confirm the approved content specification.
2. Present 2–4 design directions before writing the full HTML deck.
3. Let the user select one direction or combine parts of several.
4. Produce representative style frames or an initial screenshot montage when the project is
   substantial.
5. Implement the full deck after the direction is accepted.
6. Iterate by slide number from rendered screenshots.

## Design Language

For research/institutional decks similar to the user's Onto presentation, read
`references/onto-tokens.md` for values and `references/house-style.md` for composition, then
build from the archetypes in `references/slide-archetypes.md`.

Three points the house style is most often gotten wrong:

- There are **three** slide modes, not two. Section openers are white and do not take
  `.paper`.
- Slide titles do **not** take a rule underneath by default.
- Entrance animation belongs to the cover and contents slides only.

## Explanatory Mode Rules

Read `references/explanatory-slides.md` when designing or visually reviewing text-rich
research/reporting slides from an approved content specification. For decks based on raw
paper, report, or long section text, use `meta-slide-content` before drafting or designing.

Default constraints:

- Make the slide readable without the speaker, but still scannable during the talk.
- Use a short keyword title, one claim carried by the pull-quote or lead statement, then
  2–4 supporting blocks in complete, explanatory Korean where needed.
- Keep the approved content faithful to the source. Do not over-compress a technical
  argument into slogans during layout.
- Split visually or send back to `meta-slide-content` if a slide exceeds one concept plus
  its direct evidence.
- Use tables only when comparison is the point, and only with real `<table>` markup when the
  content is a genuine dataset.
- Add source/citation text when claims are specific, but keep citations visually subordinate.
- Use highlights to guide the live reading path — emphasis is carried by the pen, not weight.

## HTML Slide Rules

Read `references/html-slides.md` when creating a new deck, converting a deck to HTML, or
revising an HTML slide deck.

Default constraints:

- Build the actual HTML/CSS/JS slide artifact, not just an outline.
- Use Paperlogy as the Korean primary font.
- Use the Onto fixed-canvas format: `.slide` is 1920px × 1080px internally, centered with
  `position: fixed`, and fitted to the browser only through a whole-slide `scale()`
  transform. Avoid `100vw/100vh`, `scroll-snap`, or breakpoint rules that resize/reflow the
  slide canvas.
- Keep assets next to the HTML or in an `assets/` subfolder with relative paths.
- Include the print CSS from `references/pdf-export.md` from the start.
- Provide the final HTML path, PDF path, and preview path in the final response.

## Visual Mode Rules

Read `references/visual-slides.md` when creating or converting to visual-first slides.

Default constraints:

- One idea per slide; one dominant visual object.
- Body text should usually be under 50 words unless the slide is a quote, definition, or
  technical diagram.
- Prefer keyword titles plus a separate lead statement; avoid declarative sentence titles
  unless the slide is a quote or campaign-style visual.
- Replace lists with process diagrams, maps, timelines, matrices, comparisons, or annotated
  screenshots.
- Put detail in speaker notes, appendix, or backup slides.
- Use progressive reveal when the reasoning chain has multiple steps.

## Review Output

When reviewing a deck, structure the answer as:

- Overall diagnosis: Onto house-style fit, selected design direction, visual hierarchy, and
  implementation quality.
- Highest-impact visual issues first, with slide numbers or filenames.
- Mode-specific recommendations: explanatory, visual, or hybrid treatment.
- Concrete layout, typography, evidence treatment, or verification fixes.
- Content issues only when they block design; route substantive wording or structure changes
  back to `meta-slide-content`.

## Reference Navigation

- `references/onto-tokens.md`: **single source of truth** — color, type scale, fonts,
  motion, geometry, chrome, and the dead declarations not to carry over.
- `references/slide-archetypes.md`: the six slide archetypes, three modes, skeletons, CSS.
- `references/house-style.md`: Onto visual language and composition judgment.
- `references/design-exploration.md`: early design direction options within the house style.
- `references/html-slides.md`: HTML-first implementation rules and verification.
- `references/pdf-export.md`: print CSS, export command, and PDF verification.
- `references/figure-patterns.md`: catalog of explanatory figure treatments — exemplars, not
  a component library.
- `references/explanatory-slides.md`: dense but readable explanatory deck rules.
- `references/visual-slides.md`: live-presentation visual-first deck rules.
- `references/research-notes.md`: GitHub and presentation-design research distilled into
  actionable principles.
