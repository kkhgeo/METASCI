# Content Spec Storage

Use this reference when the presentation content needs to be saved as a working artifact.

## Default File

If the user does not specify a file, save the content specification as:

```text
slide_content_spec.md
```

Use the current workspace or the deck's project folder. If a content spec already exists, read it first and update it without deleting approved sections.

## File Structure

```markdown
# Slide Content Specification

## Deck Promise

## Audience and Use Context

## Narrative Spine

## Evidence and Source Map

## Slides

### Slide 01: [Keyword Title]

Status: draft | revised | user-approved | locked
Slide Topic:
Slide Job:
Audience Need:
Lead Statement:

Body Blocks:
- Label: Content
- Label: Content

Evidence:
- Type:
- Source:
- Caption:

Figure:
- Use:
- Source or Candidate:
- Caption:

Table:
- Use:
- Title:
- Rows or Columns:

Speaker Notes:

Density Risk:

Open Questions:

## Risks or Open Questions

## Production-Neutral Notes
```

## Update Rules

- Preserve approved wording exactly.
- Append new revisions under the relevant slide rather than overwriting locked text.
- Mark each slide's status.
- Keep source locations with claims when available.
- Do not store unsupported claims as final content; put them under `Open Questions`.
- If the user asks to export or move the content later, this file is the source of truth.
