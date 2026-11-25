# Synthesis — Convergence / Divergence (small-N aware)

Goal: turn the per-paper Style Cards into one file a downstream styling/rewriting skill can
use. The trap to avoid: with only **3-4 papers**, majority voting is meaningless — 3/4 vs 2/4
cannot separate "norm" from "coincidence", and style references are usually hand-picked,
*admired* papers whose individuality you'd destroy by averaging.

So do NOT produce a single averaged "house style". Produce an **agreement map plus a
divergence menu**:

- **Convergence** — what all (or nearly all) papers do the same way → safe norms to follow.
- **Divergence** — where they differ → presented as *choices the writer makes*, not errors.
- **Pick-list** — per-paper strengths, so the user can say "Smith's intro + Lee's hedging".
- **Section Guidance** — a few lines per section distilling the above into actionable defaults.

When N grows past ~5-6, you may begin reporting genuine recurrence counts as norms; below that,
treat counts as descriptive, not authoritative.

## How to build it

1. Read every `papers/<slug>/card.md`. For the numeric rows read
   `papers/<slug>/manifest.json` instead — `measured.sections` is already
   parsed and per-section, which the cards are not required to be.
2. For each dimension/frame/vocabulary theme, line up what each paper does.
3. Classify:
   - **all or all-but-one agree** → Convergence (record the count, e.g. 4/4).
   - **a real split** → Divergence (name each side and which paper holds it).
4. Pull each paper's standout strength into the Pick-list.
5. Distill Section Guidance: for each section, the convergent norms as defaults + a note where
   a divergence leaves a choice.

**Measure vocabulary convergence, don't vote it.** For V-lens items and frame anchors, the
agreement count is a measurable Range — run one count over all exemplars instead of comparing
cards by eye:

```bash
py -3.10 scripts/quant_check.py count --items shared_items.txt --per-file \n    papers/*/sections/M.txt      # one section at a time; never mix sections in one range
```

The `range` column IS the convergence count (`4/4`, `3/4`…).

**Corpus-level bundles.** Each paper's `phrases.tsv` applies a single-paper floor
(Freq ≥ 2, range ≥ 2 sections). Across papers, apply the published thresholds instead,
because there they mean what they were defined to mean: a 4-word bundle is a corpus
bundle at ≥ 20 per million words in ≥ 10% of the papers (Hyland 2008), a 3–4-word bundle
at ≥ 10 per million in ≥ 5 papers (Biber et al. 1999). Sum the raw `total` columns of
the papers' rows, divide by the summed `tokens` from each `phrases.stats.json`, and
report the number of papers as the range. With fewer than five papers, say that the
Biber floor cannot be met and report the counts. Card-level judgments still decide
*qualitative* dimensions (tense, person, citation habit); the script decides *lexical* ones.
Numeric rows (hedges/1k, avg sentence length, passive/1k) line up directly from each
`manifest.measured.sections` — report the spread (min-max) **per section**, never an
average and never a whole-paper figure. A band that mixes sections is the one mistake
this corpus design exists to prevent.

## Output — `<corpus>/style_profile.md`

```markdown
# Style Profile: <destination>  (N papers)

> Built from N style cards. Convergence = follow; Divergence = choose; Pick-list = mix sources.

## Convergence (papers agree → safe norms)
- <pattern> : <count>/N
- e.g. non-integral citation : 4/4
- e.g. past passive in Methods : 4/4

## Divergence (papers differ → your stylistic choice)
- <dimension>: <paperA> <option A> / <paperB> <option B>
- e.g. hedging density: Smith2021 high / Lee2020 low
- e.g. intro hook: A phenomenon-first / B statistical-shock

## Pick-list (per-paper strengths)
- <slug> : <what it does best>

## Red Flags (absent across the corpus → avoid)
- patterns NO paper uses (e.g. "This paper explores…", explicit roadmap sentence)

## Section Guidance (lean)
- Introduction: <convergent defaults; note any divergent choice>
- Methods: <…>
- Results: <…>
- Discussion: <…>
- Display items: <caption form + in-text reference convergence>
```

## Why this serves downstream styling

A rewriting pass can apply Convergence items as firm rules, surface Divergence items as
options to the user, and (when asked) lift a specific move from one card via the Pick-list —
without ever flattening 3-4 distinct voices into a bland average.

## Contract with meta-styling: this file is a CACHE, not a requirement

`meta-styling` (5.x) reads `papers/<slug>/` directly — `manifest.json`, `card.md`, the
pointed sections of `logic.md` and `style-vocab.md`, and the count layers — and reports N
itself. It never requires `style_profile.md`. When the file **is** present it may help
locate relevant papers or reuse a previously recorded convergence/divergence reading.

Two consequences for whoever writes this file:

1. **Provenance decides reuse, not dates.** `meta-styling` reuses this file only when its
   recorded paper selection, section, counting basis and source versions match the current
   run; a recent modification date alone does not establish that. If you re-extract or
   edit a card, rebuild this file or delete it. A stale profile is worse than no profile.
2. **Record the slugs and N it was built from**, in the header line
   (`# Style Profile: <destination>  (N papers)` — already in the template above, and the
   slug list belongs in the Pick-list). A consumer applying a subset of the corpus must be
   able to tell that this cache does not cover its subset.

Numeric rows are descriptive. `meta-styling` sets no metric bands and never edits a draft
toward a rate; it reads `manifest.measured.sections` only to describe a section. Cache the
*qualitative* judgments here — Convergence, Divergence, Pick-list, Red Flags.

## When NOT to build this

Synthesis is optional and usually skipped. Merging 3-4 admired papers averages away the
individuality that made them worth imitating, and downstream `meta-styling` compares the
selected papers side by side and decides edit by edit rather than reading a merged
profile. It runs fine without this file. Build `style_profile.md` only when the user
explicitly asks for the corpus *consensus*, or when the same corpus will be applied to many
drafts and you want the convergence call frozen.

Where a Divergence lands, it is a **choice** downstream, not a tie to break here. Record
both sides and which paper holds each; `meta-styling` reports it as an unapplied choice or,
when both sides are supported and genuinely differ, offers an alternative revision.

**Never build it for N=1.** With one paper every item is trivially `1/1`, which reads as
consensus and is not. `meta-styling` labels every structural habit from N≤2 papers as a
choice observed in those papers, precisely to keep a lone card from hardening into a rule set.

One measured example of why: across three papers by the same author, Methods hedging ran
2.6, 8.0 and 17.0 per 1k — a factor of six. The average (about 9) describes none of them.
That spread is a **choice** the author makes per paper, and flattening it destroys exactly
what a style corpus is for.
