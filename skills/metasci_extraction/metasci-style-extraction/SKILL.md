---
name: metasci-style-extraction
description: |
  META-SCI series. Extract the WRITING STYLE of a few reference papers (typically 3-4 style
  exemplars) into lean, reusable Markdown that a downstream styling/rewriting skill consumes.
  Reads sources directly (LLM-native PDF reading) and runs THREE lenses over the same text —
  V (characteristic vocabulary), L (sentence frames + section architecture), P (aggregate
  profile: voice/tense/hedging-density/citation-integration/display-item style). Produces
  per-paper Style Cards PLUS a small-N-aware Convergence/Divergence profile.
  Use this whenever the user wants to "extract style", "스타일 추출", "문체 추출",
  "이 논문들 스타일 뽑아줘", capture a journal's writing conventions from example papers, or
  build a style reference for later rewriting. This is the LEAN styling-focused extractor —
  distinct from extraction-vocab / extraction-logic (which are exhaustive, for proofreading).
allowed-tools: [Read, Write, Edit, Glob, Grep, Task]
---

# META-SCI · Style Extraction

Extract the *style* of reference papers into lean Markdown for reuse by downstream
styling/rewriting. Three orthogonal lenses run over the same text:

```
V (Vocab)   → characteristic words (reporting/hedging/stance/transition, by section)
L (Logic)   → sentence frames ([SLOT] templates) + paragraph-function sequence + section architecture
P (Profile) → aggregate indicators (voice, tense, hedging density, citation integration, display-item style)
```

**Why lean, not exhaustive.** Styling needs *characteristic* patterns, not a full lexicon or
argument map. For exhaustive word/logic dumps use `extraction-vocab` / `extraction-logic`
instead — those serve proofreading. This skill serves *style reuse*.

> **Read the matching reference file before running each lens / the synthesis.** The lens
> templates carry the field definitions and examples; this file is only the orchestrator.

## Inputs

- **Sources:** the reference papers (typically 3-4 style exemplars). PDF, Markdown, or text.
- **Korean documents (EXPERIMENTAL):** supported — read `references/lens-korean.md`
  ON TOP OF the three lens files; it redefines what each lens collects for formal
  Korean. Never mix Korean and English sources in one profile.
- **Reading:** read each source directly — the Read tool reads PDFs natively. No conversion
  engine. **If a PDF has almost no text layer (a scan), STOP and warn the user** — caption and
  sentence style cannot be read from an image, and fabricating it would corrupt the profile.
- **Figures:** not needed. Caption *style* is text and is read natively; the figure images are
  irrelevant here. (If image extraction is ever needed elsewhere, reuse the wiki's
  `extract_figures.py` — do not reinvent.)
- **destination (optional):** a label for the output folder (journal or target name).

## Workflow

1. **Accept & validate.** Confirm the source list. Check each yields real text; scan → warn/stop.
2. **Per-paper extraction.** For each paper, run the three lenses and write one Style Card:
   - V lens → read `references/lens-vocab.md` (includes the REQUIRED evidence gate:
     candidate items are counted with `scripts/quant_check.py count` and kept only at
     measured Freq ≥ 2)
   - L lens → read `references/lens-logic.md`
   - P lens → read `references/lens-profile.md` (sentence length / hedging density /
     passive rate come measured from `scripts/quant_check.py profile`, not estimated)
   - Write `Style_{destination}/cards/<slug>_style.md` (template below).
   - With 3+ papers you may dispatch one subagent per paper (Task) to parallelize; each
     subagent reads the three lens files and returns its card.
3. **Synthesize across papers.** Read `references/aggregate.md` and write
   `Style_{destination}/style_profile.md` — a **Convergence / Divergence / Pick-list /
   Section-Guidance** map (NOT a majority vote; see why in the aggregate file).
4. **Index & report.** Update `Style_{destination}/index.md`. Report to the user: cards written,
   and a short convergence-vs-divergence summary.

Downstream styling reads `style_profile.md` by default and may pull specific
`cards/<slug>_style.md` when the user wants to mix sources.

## Lens division of labor (keep outputs from overlapping)

| Lens | Owns | Must NOT re-emit |
|------|------|------------------|
| **V** | characteristic words by section, incl. caption verbs | full lexicon; structure |
| **L** | sentence/caption frames, paragraph sequence, section architecture | word lists |
| **P** | aggregate indicators, incl. display-item reference form | individual words/frames |

V = words · L = structure · P = indicators. Three layers, no double-counting.

## Output: per-paper Style Card

Write to `Style_{destination}/cards/<slug>_style.md`. Slug = ASCII lowercase-hyphen
(`smith-2021-nitrate`).

```markdown
# Style Card: <Author><Year> · <Journal>

## V. Vocabulary (characteristic, by section)
- Reporting: <verbs with measured freq, e.g. suggest (7)>
- Hedging: <words with freq>
- Stance/Transition: <words with freq>
- Caption verbs: shows, summarizes, illustrates …

## L. Frames & Structure
- Intro sequence: <phenomenon → gap → aim>
- Frame: "<template with [SLOT]>"  [function tag]
- Caption frame: "Figure [N]. [Description] showing [X]."
- In-text ref frame: "[Table N] summarizes [Y]."

## P. Profile
| dim | value |
|-----|-------|
| voice | active-dominant (passive __/1k measured) |
| tense (Intro/Meth/Res/Disc) | … |
| hedging density | low/med/high (__._/1k measured) |
| citation | integral __% / non-integral __% |
| sentence length (avg) | __._ words (measured) |
| display-item ref | "Fig." / "(Fig. 2)"; caption tense, telegraphic? |
| does NOT do | <absent patterns> |
| distinctive moves | <1-3 notable moves> |
```

## Output: synthesis

`Style_{destination}/style_profile.md` — see `references/aggregate.md` for the exact
Convergence / Divergence / Pick-list / Section-Guidance structure and the small-N rationale.

## Notes

- Keep everything **lean** — characteristic, reusable patterns only. If a section's output
  starts to read like a full dictionary or a complete argument map, you've drifted into the
  wrong skill's job.
- Preserve example sentences verbatim where you quote them, tagged with their section.
