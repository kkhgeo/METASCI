# L Lens — Sentence Frames & Section Architecture (lean)

Goal: capture the *reusable structural moves* — the rhetorical templates and the order in
which a section's paragraphs do their work. This is the styling-focused cousin of
`extraction-logic`; here you keep only frames a writer would reuse, not a full argument map.

## 1. Section architecture (paragraph-function sequence)

For each IMRaD section, record the typical *sequence of paragraph functions* — the skeleton a
writer follows. Keep it to the recurring spine, e.g.:

- **Introduction:** broad phenomenon → narrowing context → gap → aim/hypothesis → (roadmap?)
- **Methods:** study area → sampling design → analytical procedure → QA/QC → statistics
- **Results:** overview → primary finding → secondary findings → figure/table-anchored detail
- **Discussion:** restate key finding → comparison with literature → mechanism → limitation →
  implication

Note presence/absence of optional moves (explicit roadmap sentence, standalone literature
review, limitation paragraph). Absence is itself style (and feeds the P lens "does NOT do").

## 2. Sentence frames (rhetorical templates)

Abstract characteristic sentences into reusable templates with `[SLOT]` placeholders, each
tagged by function. Keep BOTH the abstracted frame AND one verbatim source sentence so the
template is grounded.

Capture frames for the high-value functions:

- **Gap:** `"Despite [X], [Y] remains [poorly understood / unresolved]."`
- **Aim:** `"Here we [verb] [X] to [purpose]."` / `"This study [verb]s [X]."`
- **Method entry:** `"[Samples] were [analyzed] using [instrument] following [protocol]."`
- **Result report:** `"[Variable] [increased/ranged] from [A] to [B] ([stat])."`
- **Interpretation:** `"These results suggest that [mechanism]."`
- **Comparison:** `"Consistent with [ref], we observed [X]." / "In contrast to [ref], …"`
- **Limitation:** `"[X] should be interpreted with caution because [Y]."`
- **Implication:** `"These findings [imply/highlight] [broader point]."`

Don't force all of them — collect the ones the corpus actually uses, and any distinctive
extras (label them under a misc/"distinctive" bucket).

## 3. Display-item frames (tables / figures)

Caption phrasing and in-text reference are structural style and belong here (the *form* of the
reference — "Fig." vs "Figure" — is a P-lens indicator; the *template* is here):

- **Caption frame:** `"Figure [N]. [Subject], showing [what it shows] ([where/units])."`
- **In-text reference frame:** `"[Table N] summarizes [X]." / "As shown in [Fig. N], …" / "(Fig. [N])"`

## How to keep it lean

- One frame per function is usually enough; add a variant only if it's genuinely different.
- The architecture is a spine, not a full outline — recurring functions, not every paragraph.

## Output (the L section of the Style Card)

```markdown
## L. Frames & Structure
- Intro sequence: <…>     Methods sequence: <…>     Results sequence: <…>     Discussion sequence: <…>
- Frame [Gap]: "<template>"   ← "<verbatim source>"
- Frame [Aim]: "<template>"
- … (high-value functions)
- Caption frame: "<template>"
- In-text ref frame: "<template>"
```

Do not list individual words (V) or compute ratios (P).
