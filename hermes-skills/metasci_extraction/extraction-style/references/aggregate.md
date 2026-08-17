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

The `range` column IS the convergence count (`4/4`, `3/4`…). Card-level judgments still decide
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

`meta-styling` v3.x reads `papers/<slug>/card.md` + `manifest.json` directly and counts N
itself. It never requires `style_profile.md`. When the file **is** present it is used only
as a cache of a previously computed convergence/divergence judgment — that judgment is an
LLM reading call, so reusing it keeps successive revision passes consistent instead of
re-deciding each time.

Two consequences for whoever writes this file:

1. **Staleness invalidates it.** `meta-styling` ignores a `style_profile.md` whose mtime is
   older than any `papers/*/card.md` in scope, and derives from the cards instead. If you
   re-extract or edit a card, either rebuild this file or delete it. A stale profile is
   worse than no profile.
2. **Record the slugs and N it was built from**, in the header line
   (`# Style Profile: <destination>  (N papers)` — already in the template above, and the
   slug list belongs in the Pick-list). A consumer applying a subset of the corpus must be
   able to tell that this cache does not cover its subset.

Numeric rows do NOT need to be cached here: `meta-styling` recomputes bands from
`manifest.measured.sections` with its own spread rule, which is cheap and deterministic.
Cache the *qualitative* judgments — Convergence, Divergence, Pick-list, Red Flags.

## When NOT to build this

Synthesis is optional and usually skipped. Merging 3-4 admired papers averages away the
individuality that made them worth imitating, and downstream `meta-styling` applies cards
in parallel — **laying out candidate revisions and recommending one** — rather than
reading a merged profile. It reads the cards directly and gates prescriptions on N, so it
runs fine without this file. Build `style_profile.md` only when the user explicitly asks
for the corpus *consensus*, or when the same corpus will be applied to many drafts and you
want the convergence call frozen.

Where a Divergence lands, it becomes a **candidate axis** downstream, not a tie to break
here. Record both sides and which paper holds each; `meta-styling` turns that into two
revisions the author chooses between.

**Never build it for N=1.** With one paper every item is trivially `1/1`, which reads as
consensus and is not. `meta-styling`'s `single-source` tier exists precisely to keep a
lone card from hardening into a rule set.

One measured example of why: across three papers by the same author, Methods hedging ran
2.6, 8.0 and 17.0 per 1k — a factor of six. The average (about 9) describes none of them.
That spread is a **choice** the author makes per paper, and flattening it destroys exactly
what a style corpus is for.
