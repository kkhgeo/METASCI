---
name: meta-slide-content
description: Plan, write, finalize, and review research presentation structure and slide content. Use when Codex needs to turn papers, reports, existing decks, notes, or dense source material into an approved slide content specification with deck promise, audience context, narrative spine, slide topics, final titles, lead statements, bullets, figure/table/source selections, speaker notes, and open content questions.
---

# Meta Slide Content

Use this skill to make the presentation's argument, sequence, and slide-level content clear and final. Stop at the approved content specification; do not produce finished slides.

## Scope

- Produce an approved content specification, not a finished deck.
- Finalize the actual slide sentences: topic, title, lead statement, bullets/body blocks, evidence captions, table contents, and speaker notes when needed.
- Work interactively by default. Do not finalize a section or slide until the user has accepted its content or requested a specific revision.
- Write Korean by default for Korean research, policy, and institutional decks.
- Preserve source fidelity. Do not add claims, implications, definitions, citations, or examples that are not supported by the provided material.
- Keep English technical terms when they are the clearest domain labels, but explain their role in Korean.
- Use keyword slide titles and put the full claim in the lead statement.

## Required Sequence

1. Identify the audience, delivery setting, purpose, expected decision or understanding, source material, and output format.
2. Define the deck promise: "After this deck, the audience should understand/decide/trust ___". Ask the user to confirm or revise it before continuing.
3. Analyze the source content before drafting slides. Read `references/content-analysis.md` for papers, reports, policy documents, long notes, or dense existing decks.
4. Build the narrative spine: context -> problem -> concept -> method -> evidence -> implication -> next step. Ask the user to approve the sequence before writing slide content.
5. Assign each slide exactly one job: orient, define, compare, explain process, show evidence, demonstrate result, transition, decide, or close.
6. Confirm slide topics and keyword titles before drafting lead statements or bullets.
7. After the slide list and keyword titles are approved, draft the detailed content for all slides in one batch using `references/slide-plan-schema.md`. Read `references/bullet-writing.md` when writing or rewriting body blocks, especially for Korean analytical bullet tone.
8. In the batch draft, fill each slide in this order: topic -> keyword title -> lead statement -> body blocks/bullets -> figure/table/source selection -> caption -> speaker notes.
9. Ask the user to approve the batch or request revisions by slide number.
10. Save or update the finalized content specification using `references/content-spec-storage.md`, then review it for gaps, unsupported claims, overloaded slides, missing transitions, and weak takeaways.

## Review Existing Decks

When reviewing an existing deck, evaluate presentation content and structure. Read `references/content-review.md`, then report the highest-impact content issues first: unclear promise, weak narrative order, missing claim/evidence links, overloaded slides, unsupported conclusions, or slides with no clear job.

## Interaction Rules

Read `references/interactive-finalization.md` when building or revising a deck with the user. Use a small number of approval gates:

1. Deck promise and audience.
2. Narrative spine and section order.
3. Slide list with topics and keyword titles.
4. Batch draft of all slide details: lead statements, body blocks, evidence, figures, tables, captions, and speaker notes.
5. Revision pass by slide number.
6. Saved content specification and lock status.

When asking for feedback, ask about the current gate only. Keep alternatives concrete, and record accepted wording as approved content.

## Writing Rules

- Use concise Korean keyword titles, not full sentence titles.
- Use one lead statement per slide to state the claim or takeaway. This is the final sentence that would appear beneath the title.
- Use 2-4 body blocks for visual live-talk slides and 3-6 analytical bullets for section-derived report slides or handout-style content. Treat these as final slide text, not rough notes.
- Write body blocks as analytical units with claim, evidence, mechanism, or implication. Use labels internally for planning, but do not expose labels such as `Background:`, `Evidence:`, or `Implication:` in final slide bullets unless the user asks for a scaffold.
- For Korean research and policy decks, write final bullets as complete objective analytical sentences with concise endings such as `-함`, `-됨`, `-나타남`, `-해석됨`, `-필요함`, `-어려움`, `-유용함`, or `-적절함`. Use `-고 있음` only when an ongoing process or current state must be emphasized, and avoid repeated `있음` endings.
- Map every empirical or borrowed claim to evidence, source, figure, table, or citation.
- Split slides that contain more than one job or more than one direct evidence path.
- Mark unresolved content questions instead of silently filling gaps.

## Output Shape

Return content artifacts in this order:

1. Deck Promise
2. Audience and Use Context
3. Narrative Spine
4. Approved Slide Content Specification
5. Evidence and Source Map
6. Risks or Open Questions
7. Production-Neutral Notes

Use the slide-level schema from `references/slide-plan-schema.md` for the Approved Slide Content Specification.

## Reference Navigation

- `references/content-analysis.md`: source-faithful analysis before slide planning.
- `references/interactive-finalization.md`: staged user interaction and approval workflow.
- `references/slide-plan-schema.md`: required deck and finalized slide content format.
- `references/bullet-writing.md`: body block and bullet writing patterns with Korean examples.
- `references/content-spec-storage.md`: how to save and update the finalized content specification.
- `references/content-review.md`: review rules for existing deck content and structure.
