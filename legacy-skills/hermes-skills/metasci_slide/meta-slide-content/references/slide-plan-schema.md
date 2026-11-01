# Slide Plan Schema

Use this schema to write and finalize the presentation's content structure.

## Deck-Level Specification

```text
Deck Promise:
Audience:
Delivery Setting:
Artifact Type:
Presentation Mode: explanatory handout | live talk | hybrid
Narrative Spine:
  1. Context:
  2. Problem:
  3. Concept:
  4. Method:
  5. Evidence:
  6. Implication:
  7. Next Step:
Production-Neutral Notes:
  Tone:
  Explanation Priorities:
  Evidence Objects:
  Required Source Materials:
  Constraints:
Approval Status: draft | user-approved | locked
```

## Slide-Level Specification

Use one block per slide:

```text
Slide ID:
Approval Status: draft | revised | user-approved | locked
Slide Topic:
Slide Job: orient | define | compare | explain process | show evidence | demonstrate result | transition | decide | close
Audience Need:
Keyword Title:
Lead Statement:
Body Blocks:
  - Label:
    Content:
  - Label:
    Content:
Evidence:
  Type:
  Source:
  Caption:
Figure:
  Use: yes | no | unresolved
  Source or Candidate:
  Caption:
Table:
  Use: yes | no | unresolved
  Title:
  Rows or Columns:
Evidence Form:
Speaker Notes:
Density Risk:
Open Question:
```

## Field Rules

- `Keyword Title` must be short and non-declarative.
- `Lead Statement` must state the slide's main point in one final sentence.
- `Body Blocks` should usually be 2-4 grouped ideas. Use `bullet-writing.md` for body block patterns and examples.
- `Label` inside `Body Blocks` is an internal planning field. For final Korean slide text, normally render only the `Content` as bullet copy unless the label is intentionally part of a table, matrix, or named framework.
- Section-derived Korean analytical slides may use 3-6 complete bullets when the user wants report-style structure; visual live-talk slides should stay closer to 2-4 bullets.
- `Evidence` must identify what supports the lead statement.
- `Evidence Form` should name the supporting material form, such as map, matrix, timeline, process, figure, table, quote, or source excerpt.
- `Figure` and `Table` fields decide whether the slide needs those content objects and what they must contain.
- `Approval Status` records whether the user has accepted the slide wording.
- `Density Risk` should flag slides that may need to split before the content specification is final.

## Specification Checklist

- Every slide has exactly one job.
- Every lead statement is supported by evidence or marked as an open question.
- Every title, lead statement, visible bullet, figure/table choice, caption, and speaker note is explicit.
- Visible Korean bullets are complete analytical sentences and do not expose internal labels such as `Background:`, `Evidence:`, or `Implication:` unless requested.
- The slide order follows the narrative spine.
- Terms are defined before they are used as structural nodes.
- Evidence objects and audience priorities are clear and source-grounded.
