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

## Evidence gate (AntConc-style — REQUIRED)

"Characteristic" is a measurable claim, not an impression. Before an item enters the card:

1. Collect your candidate items into a list file (one per line; `suggest*` covers inflections).
2. Count them against the paper's authorial prose:
   `python scripts/quant_check.py --strip-refs count --items cand.txt paper.pdf`
   If the paper contains large non-prose blocks (data tables, verbatim boxes, appendices),
   save a body-prose-only `.txt` and count against that instead; annotate any count you
   know is inflated by non-authorial text, e.g. `explicitly (11, mostly box text)`.
3. Keep an item only if measured **Freq ≥ 2** (a word used once is not this paper's
   register). Exception: an item may stay at Freq 1 if flagged `(rare-but-marked)` — a
   genuinely unusual move worth noting — but never more than 1-2 such items per card.
   **Caption verbs are exempt from the gate** (a paper with two display items cannot
   produce Freq ≥ 2 caption verbs); list them with whatever freq they have.
4. Record the measured freq next to each item on the card: `suggest (7)`.

**The measurement wins.** If the script returns 0 for a word you are sure you read, grep the
extracted text before claiming a counting artifact — in testing, such disputes are usually
the reading impression being wrong, not the count. Never restore a gated-out item from memory.

Optional, for "this paper vs the other exemplars" distinctiveness:
`python scripts/quant_check.py keyness --target paper1.pdf --reference paper2.pdf paper3.pdf`
To verify a section-skew claim ("Results favors *showed*"), split the prose into per-section
`.txt` files and run `count --per-file` over them.

## Output (the V section of the Style Card)

```markdown
## V. Vocabulary (characteristic, by section)
- Reporting: <verbs with measured freq, e.g. suggest (7), observe (5); note section skew>
- Hedging: <words with freq>
- Stance/Transition: <words with freq; note position>
- Register markers: <handful of signature phrases with freq>
- Caption verbs: <verbs>
```

Do not emit structure or aggregate ratios here — those are L and P.
