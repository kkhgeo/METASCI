# Explanatory Slides

Use explanatory mode for decks that must carry meaning even when read without the speaker.

## Purpose

Explanatory slides are appropriate for research briefings, institutional reports, policy proposals, academic defenses, technical reviews, and handout-like decks. The goal is not minimal text; the goal is controlled explanation.

For the user's Onto-style decks, explanatory mode should preserve the approved content specification in readable Korean. Do not reduce a technical method or evidence chain to visual slogans when the user asks for explanation.

When the deck is based on raw paper, report, or long notes, use `meta-slide-content` first. This reference starts after slide topics, keyword titles, lead statements, body blocks, and evidence objects are approved.

## Slide Anatomy

Use this hierarchy:

1. Korean keyword title, not a mechanical navigation label or declarative sentence.
2. Lead statement/subtitle that states the main point in one complete sentence.
3. Supporting explanation in 2-4 grouped blocks, using complete sentences when precision matters.
4. Evidence object: figure, table, workflow, map, screenshot, equation, or cited example.
5. Small caption/source.

## Density Rules

- Accept more text than visual mode, but every block must support the slide's single job.
- Prefer 2-4 text groups over long bullet lists.
- Use short paragraphs when precision matters; do not compress away causal logic, definitions, assumptions, or method differences.
- A slide can carry a faithful explanatory paragraph if it is visually grouped and has a clear lead statement.
- If a slide needs more than 90 seconds to explain, split it.
- If a table has more than one intended reading path, split it or add strong highlights.
- If the audience must understand a new term, define it before using it as a structural node.

## Explanation Patterns

- Definition ladder: origin -> formal definition -> practical meaning -> why it matters.
- Problem/solution pair: fragmented state -> integration principle -> expected capability.
- Framework decomposition: inputs -> semantic layer -> model/analysis -> service/output.
- Method pipeline: source -> preprocessing -> extraction/modeling -> validation -> output.
- Evidence slide: claim -> chart/map/table -> annotated implication.
- Policy/decision slide: analysis result -> policy question -> decision-support use.

## Layout Selection

- Do not default every explanation slide to a full-height two-column split. Use that pattern only when a large figure/table must remain visible while the audience reads the explanation.
- For 2-3 comparable ideas, use row-based structures: title and lead at the top, then horizontal rows or cards below.
- If an evidence object belongs near the bottom, put it at the right side of the lower row or bottom band, with short interpretation blocks to its left. This keeps the Onto reading path while avoiding repetitive left-text/right-evidence slides.
- For method or comparison slides, alternate among bottom evidence bands, three-card rows, process strips, and compact matrices before repeating a two-column layout.

## Korean Writing Rules

- Write the slide body in Korean by default for Korean decks.
- When source material is provided, reflect only the provided information. Do not add background claims, interpretations, or implications that are not supported by the source.
- Preserve the approved body blocks unless a layout problem requires a visible wording adjustment.
- Keep domain terms such as `mass balance`, `source apportionment`, `retention`, `SWAT`, `HRU`, and `GraphRAG` in English when they are the clearest technical labels, but explain their role in Korean.
- Use highlights for key concepts inside a sentence, not as decoration.
- Avoid agenda-style labels such as `00 / 발표 흐름` unless the slide is explicitly a contents page requested by the user.
- Prefer keyword titles like `물질수지와 관리 위치`, `영양염류 부하 산정`, or `Mass-balance와 SWAT 비교`.
- Put declarations such as `정적 물질수지는 총량을 산정하지만 공간적 관리 위치를 제한적으로 제시함` in the lead statement, not the title.

## Review Checklist

- Does the slide have a keyword title plus one lead statement that could be read aloud as its point?
- Can a non-specialist identify the top three ideas within 10 seconds?
- Are highlights used as a reading path, not decoration?
- Is the citation/source present when the claim is empirical, recent, or borrowed?
- Is the visual doing explanatory work, or is it only decorative?
- Does the slide connect back to the deck promise?

## Conversion From Over-Dense Slide

When a slide is too dense:

1. Extract the main assertion.
2. Mark required evidence versus background detail.
3. Keep the assertion and one evidence object on the main slide.
4. Move secondary rows, definitions, or literature examples to backup/appendix.
5. If the detail is essential to the live explanation, split into a sequence: concept -> method -> result -> implication.
