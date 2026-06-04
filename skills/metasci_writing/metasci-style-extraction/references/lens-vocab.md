# V Lens — Characteristic Vocabulary (lean)

Goal: capture the words that give the paper its *register*, by section — **not** every word.
This is the styling-focused cousin of `extraction-vocab`. Where that skill is exhaustive
("ALL content words"), here you collect only the items a writer would reuse to *sound like*
this paper. Quality bar: would a reviser actually reach for this word to match the style?

## What to collect (by IMRaD section)

For each of Introduction / Methods / Results / Discussion, gather the *characteristic*:

1. **Reporting verbs** — how findings/claims are introduced: demonstrate, reveal, indicate,
   suggest, report, observe, find, show. Note which dominate where (e.g. Results favors
   "showed/observed"; Discussion favors "suggests/may indicate").
2. **Hedging vocabulary** — may, might, could, likely, appears, seems, relatively,
   approximately, generally. (Words only — *density* is the P lens's job.)
3. **Stance / intensity** — significantly, substantially, markedly, notably, considerably,
   consistent with, in line with.
4. **Transitions / connectors** — however, furthermore, moreover, in contrast, thus, therefore,
   whereas, in addition, taken together. Note typical position (sentence-initial vs mid).
5. **Register / discipline markers** — recurring nominalizations, set phrases, and field terms
   used as *style* (e.g. "spatial variability", "lines of evidence", "endmember") — capture a
   handful that recur, not the full terminology glossary (that's extraction-vocab).
6. **Caption verbs (display items)** — shows, summarizes, illustrates, depicts, presents,
   compares. These belong here; caption *frames* go to the L lens, caption *form* to P.

## How to keep it lean

- Cap each category at the items that genuinely recur or feel signature — roughly the top
  handful per section, not an inventory. If you find yourself listing 30 nouns, stop: that is
  exhaustive-vocab territory, not style.
- Prefer items that are **transferable** — a reviser could drop them into a new manuscript.
- When a word is distinctive, keep one short verbatim host phrase so its usage is clear, e.g.
  `suggest — "These results suggest that denitrification…"`.

## Output (the V section of the Style Card)

```markdown
## V. Vocabulary (characteristic, by section)
- Reporting: <verbs; note section skew>
- Hedging: <words>
- Stance/Transition: <words; note position>
- Register markers: <handful of signature phrases>
- Caption verbs: <verbs>
```

Do not emit structure or aggregate ratios here — those are L and P.
