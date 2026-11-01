# Research Notes

Use these notes to align slide work with established GitHub slide tooling and public presentation-design guidance.

## Distilled Principles

- Use one main idea per slide unless the deck is intentionally a handout/report.
- Make titles meaningful, but keep them keyword-centered. Put findings or conclusions in a separate lead statement/subtitle line.
- Keep visuals connected to the claim; adapt figures so they support the slide's message.
- Limit visible elements in live-presentation slides. Split slides that require too much simultaneous attention.
- Use speaker notes, appendix slides, or handouts for detail that does not need to be on screen.
- Validate layout with actual rendering; overflow and cropped content are common presentation failures.
- Choose authoring format based on workflow: Markdown/HTML tools are good for versioning and iteration; PPTX/Google Slides are better when collaborators need native slide editing.

## GitHub/Tooling Observations

### Slidev and cc-slidev

The `rhuss/cc-slidev` plugin demonstrates a useful guardrail model for technical decks: one idea per slide, meaningful titles, cognitive-load limits, minimal text for visual-first slides, near-universal visual support, accessibility defaults, and Git-friendly Markdown authoring.

Use this as a strong reference for visual mode and developer/technical presentations.

### Marp and Marp VS Code

Marp uses Markdown frontmatter and slide separators, supports preview/export workflows, and the VS Code extension includes diagnostics for overflow, excessive content, and unnatural layouts. Use this as a reminder to render-check slides instead of trusting source text.

### Reveal.js / R Markdown Reveal

Reveal/R Markdown supports heading-based slide structure, 2-D presentations, slide numbers, notes, and external dependencies. The heading hierarchy model is useful for planning sections and sub-sections before detailed layout.

### Google Slides Markdown Mapping

The `k1LoW/deck` project maps the shallowest heading to title, next heading to subtitle, and remaining content to body placeholders. This reinforces a practical authoring rule: title/subtitle/body hierarchy should be explicit before styling.

### PPTX to Marp Conversion

`pptx2marp` and similar converters show common transformation needs: content length classification, automatic two-column layout for dense slides, image scaling, captions, and font scaling. Use these ideas when converting legacy dense slides into structured Markdown/HTML decks.

## Public Guidance Observations

MIT Communication Lab guidance emphasizes purpose, larger motivation, slide messages, and titles that stand on their own. It also stresses that a slide should not include more information than needed to support its message.

For this skill, adapt that principle by mode:

- Visual mode enforces it strictly.
- Explanatory mode relaxes word count but still requires one slide job, visible hierarchy, and no unsupported density.
