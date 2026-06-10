# House Style: Onto-Inspired Research Decks

Use this reference when the user wants the design feeling of the Onto presentation reflected in a new or revised deck.

## Visual Character

- Institutional research tone, not marketing.
- Large, heavy Korean titles with calm analytical layouts.
- HTML slide deck is the default implementation format. Design should be expressed in CSS and verified by rendered screenshots.
- HTML slides should behave like a fixed presentation file, not a responsive web page: author each slide on a 1920px × 1080px canvas and scale the whole slide to fit the browser.
- Paperlogy is the default Korean typeface for titles and body. Use Pretendard only as fallback.
- Paper-like white/near-white slides for content, dark immersive image slides for title and contents.
- Strong left-aligned structure for explanation slides.
- Avoid making every content slide a full-height two-column split. Keep the Onto title/lead/rule language, but vary the body area with rows, evidence bands, matrices, and card groups according to the slide job.
- Section openers with sparse composition: section number, short lead phrase, ample white space.
- Titles are keyword-centered, not declarations. The slide claim belongs in the colored lead statement/subtitle line or body.
- Chapter colors identify the conceptual territory:
  - Blue: overview, framework, background.
  - Teal: ontology, semantic integration, knowledge infrastructure.
  - Orange: policy KG, GraphRAG, pipeline and method.
  - Olive/green: gridded environmental data and monitoring networks.
  - Red/coral: public information, media, platform integration.

## Layout Patterns

### Cover

Always generate a subject-relevant bitmap image for the cover. Prefer a full-bleed environmental, geospatial, institutional, or domain-specific image with a dark left gradient. Put the main Korean title left, English subtitle beneath, date/team line below, and logo/brand in corners. The image must show the actual topic or a faithful visual metaphor, not generic atmosphere.

### Contents

Use only when the user asks for an agenda/contents slide or the deck is long enough to need one. Do not title normal slides with mechanical labels such as `00 / 발표 흐름`. If used, make it a real orientation slide with meaningful section names, not a meta scaffold.

### Section Opener

Use a nearly blank slide with:

- Large section number and name.
- One quoted lead phrase. This is the only place where a declarative phrase may dominate the slide.
- Chapter color underline.
- Optional faint background from prior cover/contents.

### Explanation Slide

Use:

- Large Korean keyword title, not a navigation label or full sentence.
- Colored lead statement/subtitle line that states the main point in one complete sentence.
- 2-3 body groups on the left or across rows, written as faithful explanatory Korean when the source argument is complex.
- One explanatory figure/table/diagram placed where it supports the reading path: right side, bottom band, or the right end of a lower row.
- Colored highlights over only the terms the speaker wants the audience to retain.

Preferred Onto-style structure:

1. Top-left keyword title, usually 2-6 Korean words.
2. Thin horizontal rule below the title.
3. Large colored lead statement below the rule.
4. Choose the body layout by slide job, not by habit:
   - Use a full-height left/right split only when the audience must compare text explanation and a large evidence object side by side.
   - Use a horizontal row structure when the slide has 2-3 parallel ideas, stages, or implications.
   - Use a bottom evidence band when the text establishes context first and the figure/table should land as supporting proof.
   - When using a bottom row, place the figure/table/diagram on the row's right side and keep the row's left side for short interpretation blocks; this preserves Onto hierarchy without making the whole slide a two-column template.
5. Small source/caption aligned with the evidence or bottom edge.

### Framework Slide

Use boxed modules connected by arrows. Make the system's final output or decision-support value visibly downstream. If the diagram has many modules, add a caption that states how to read it.

### Evidence/Data Slide

Use a chart or map as the main object, with 1-3 callouts. Avoid making the audience read every axis label or table row. If a table is necessary, highlight only the row/column that supports the point.

## Typography and Emphasis

- Use Paperlogy for Korean titles and body by default. Load local Paperlogy font files with `@font-face` when available; otherwise use CDN Paperlogy and fallback to Pretendard/sans-serif.
- Prefer bold Paperlogy display type for titles.
- Keep body text smaller but still legible from a projector.
- Use blue/teal/orange/green/red highlights as semantic accents, not decoration.
- Captions and citations should be small, light, and aligned to the figure.
- Use English technical terms when they are domain-standard, but pair with Korean explanation when comprehension matters.

## Anti-Patterns

- Producing PPTX by default when the user expects this skill to make HTML slides.
- Using visible meta labels such as `00 / 발표 흐름`, `01 / 방법`, or `Slide 3` as ordinary headings.
- Writing normal slide titles as declarations such as "물질수지는 관리 위치를 말하지 못함"; use "물질수지와 관리 위치" as the title and put the declaration in the lead statement.
- Replacing a technical explanation with short slogan-like bullets that omit the source logic.
- Making a title slide without a generated image.
- Dense body text with no visual anchor.
- Tables used as storage instead of argument.
- Multiple unrelated visuals competing on one slide.
- Decorative cards inside cards.
- One-hue monotony; each chapter may have a dominant accent, but the deck should retain neutral paper and dark text as the base.
- Important service/platform implication appearing only at the end with no earlier preview.
