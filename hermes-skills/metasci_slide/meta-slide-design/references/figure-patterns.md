# Figure Patterns

A catalog of how the Onto deck built its explanatory figures. These are **exemplars, not
components** — every one is bound to the content of a single slide.

Read this for "how was that done", then build the new figure from scratch against
`onto-tokens.md`. Copying these classes into a new deck imports someone else's content
structure and produces a figure that almost fits.

## Why this is a catalog and not a library

The deck has one genuinely reusable figure frame, `.pillar-visual`
(`__image` + `__caption`), and it appears on 2 slides. Everything else below appears on
exactly one slide, or on one contiguous sub-thread.

That is the correct outcome, not a defect. Explanatory figures earn their layout from the
argument they carry. The reusable layer is the tokens and the archetypes; the figures sit
above it.

### The trap

`.kg-step` looks like a reusable numbered-step component — 56 occurrences in the markup,
22 CSS rules. It is **one slide**. The GraphRAG pipeline hardcodes its grid slots:

```css
grid-template-areas: "--src --extr" "--chunk --graph" "--embed --comm" "--out --out";
grid-template-columns: 340px 340px;
grid-template-rows: 170px 170px 170px 160px;
```

with an `<svg class="kg-arrows">` overlaid at fixed coordinates. Nothing survives a change
of step count. `.platform-rail` is the same shape of trap: 22 occurrences, one slide.

Check instance count before promoting anything.

---

## Catalog

### Flow and pipeline

**`.corpus-flow-svg`** — data corpus pipeline. Inline SVG, `.node-title` 24px,
`.main-title` 30px, `.caption-label` 14px. Nodes as rounded rects, labeled arrows between.
Use when stages have named inputs and outputs.

**`.kg-step` / `.kg-pipeline` / `.kg-arrows`** — GraphRAG construction, 7 stages in a
2-column grid with an SVG arrow overlay. `.kg-step__kicker` is mono 21px `.14em` uppercase;
`.kg-step__title` 28px/800. Use the *idea* — kicker plus title in a fixed cell, arrows
drawn separately — not the geometry.

**`.svg-funnel`** — narrowing selection stages.

**`.measurement-sankey-svg`** — flow volumes between categories. Hand-authored SVG paths.

**`.query-radial` / `.qr-*`** — Local-to-Global query answering, radial layout.
`.qr-kicker` and `.qr-title` both 22px; inner labels are SVG `<text>` with `fill:#ffffff`.

### Data and evidence

**`.emissions-chart`** — bar chart. `.chart-title` and `.sector-title` 22px,
`.callout-label` 18px, `.citation-label` 12px. Callouts point at the bars that carry the
argument; the rest are unannotated. Copy that restraint.

**`.ontology-trend-chart`** — time series. `.chart-title` 24px, `.chart-source` 20px,
`.chart-source-url` 12px, `.axis-label` 16px, `.value-label` 21px. The four-level
title/source/axis/value hierarchy is worth reusing as a principle.

**`.network-map` / `.network-bundle`** — node-link diagram with edge bundling.

**`.ml-map-*`** — three parallel columns (inputs / methods / applications). Built as three
`<section class="ml-map-column">` with `aria-label` on each. Good pattern for
"three parallel taxonomies" content.

**`.soil-example__*`** (5 slides), **`.pli__*`** (3 slides), **`.measurement-summary__*`**
(4 slides) — sub-thread figure families. Each holds a consistent internal style across its
own run of slides. If a new deck has a multi-slide case study, build a small family like
this rather than styling each slide separately.

### Reference and structure

**`.glosis-filetree`** — indented file/schema tree in mono. Use for standards, schemas,
directory structures.

**`.ontology-timeline`** — horizontal timeline. `__year` 41px/760 in `--f-display`
(Archivo, for numerals), `__summary` 25px, `__tag` 24px/500 with lavender `<mark>`,
`__quote` 26px Georgia italic. The Archivo numerals against Paperlogy body is a deliberate
contrast — reuse it wherever years or figures need to read as data.

**`.policy-infra-table`**, **`.kg-impl-table`**, **`.kcp-spec-table`** — comparison tables.

**`.portal-card`**, **`.platform-hub`**, **`.platform-rail`** — platform/service layouts.

**`.purpose-framework-visual`**, **`.ontology-build-*`**, **`.fn-*`** — framework diagrams.

---

## Tables

The deck uses real `<table>` elements for genuine tabular data — 3 tables, 17 rows,
31 cells across the policy-infrastructure, soil-example, and background-concentration
slides. Other table-shaped UI (spec sheets, comparison grids) is built as div grids.

The rule that produces this split: **use `<table>` when the content is a dataset with
homogeneous rows and a header; use a div grid when it is a layout that merely looks
tabular.** Screen readers and PDF extraction both depend on getting this right.

Table styling follows the tokens — `--paper-line` rules, `--fs-meta` cells,
`--fs-caption` sources, no fills except on the row or column that carries the argument.
A table with every cell styled equally is storage, not argument.

---

## Building a new figure

1. State what the figure must let the audience conclude. If that sentence does not exist,
   the slide needs a content pass, not a figure.
2. Pick the relation: sequence, flow, comparison, distribution, hierarchy, network,
   territory, or change over time. The relation picks the form.
3. Build against tokens. Chapter accent for the elements carrying the argument,
   `--paper-mute` for scaffolding, `--paper-line` for structure.
4. Annotate only what the argument needs. The emissions chart labels the bars it argues
   about and leaves the rest bare.
5. Caption at `--fs-caption` with the source. Captions state how to read the figure when
   the reading order is not obvious.
6. Check it at 100% and at fit-to-screen. Figures that only work zoomed in fail in a room.

Inline SVG is the default for diagrams — it scales cleanly to the PDF export and can be
styled with the same CSS tokens. Reach for a bitmap only for photography, maps, and
screenshots.
