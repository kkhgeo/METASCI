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

1. Read every `cards/<slug>_style.md`.
2. For each dimension/frame/vocabulary theme, line up what each paper does.
3. Classify:
   - **all or all-but-one agree** → Convergence (record the count, e.g. 4/4).
   - **a real split** → Divergence (name each side and which paper holds it).
4. Pull each paper's standout strength into the Pick-list.
5. Distill Section Guidance: for each section, the convergent norms as defaults + a note where
   a divergence leaves a choice.

## Output — `Style_{destination}/style_profile.md`

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
