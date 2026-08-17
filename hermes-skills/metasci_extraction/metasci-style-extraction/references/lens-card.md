# Lens C — Style Card

**Output**: `card.md`
**Reads**: `logic.md`, `style-vocab.md`, `manifest.json`, and the section files for the
indicators only this lens can judge.

The card is the **selected** layer — one or two pages a reviser actually opens. Everything
bulky already has a home; the card points at it.

---

## Run this lens LAST

Not a formality. On the test paper the card's two most useful lines could not have been
written first:

- *"`report*` is for prior literature; `indicat*`/`suggest*` are for the author's own
  inference; `show*` is for figures"* — came from Lens W's per-section measurement.
- *"Imitate the frame type, never the wording"* — came from Lens A's anchor test showing
  190 of 193 frames occur exactly once.

A card written before those lenses contains impressions. A card written after them contains
findings.

## Keep it lean — the failure this rule prevents

An earlier version of this skill pushed a 145-line measurement block *into* the card. To
make room, the sentence-frame section shrank from 40 lines to 26 and lost its verbatim
examples entirely. The card grew 2.4× while the part a reviser could act on shrank. The
card broke the skill's own rule — *preserve example sentences verbatim* — because there was
no space left.

**Test before adding anything to the card**: does this have a home in `logic.md`,
`style-vocab.md`, `wordlist.tsv` or `manifest.json`? If yes, cite it; do not copy it.

Target: **under 200 lines.** If you are past that, you are transcribing, not selecting.

## C.1 — V: vocabulary (from Lens W)

Not a re-listing. Select the items whose *distribution* is instructive:

- the **reporting-verb hierarchy** with its `reserved for` column — the highest-value block
  on the card
- the **modality workhorse**: which hedge dominates and by how much
  (test paper: `can be` 21 vs `may` 9 — substituting *may* throughout would sound wrong)
- **connectives with their zeros** (test paper: `however` = 0 in Methods)
- **register habits** — the non-technical set phrases
- a short **do-not-import** note for items that clear the frequency gate but are topic
  terms (test paper: `uncertain*` 29 and `potential*` 21 are "sample uncertainty" and
  "potential sources", not hedging)

## C.2 — L: frames and structure (from Lens A)

- **Section architecture**: the paragraph-function spine per section, plus the absences.
- **10–14 frames**, each as `template` ← `verbatim source [P#-S#]`. Choose by function
  coverage (gap, aim, method entry, result report, interpretation, comparison, concession,
  decision, caption, in-text reference), not by frequency.
- **The recurrence warning, verbatim**, above the frame list:

  > ⚠ Use the frame TYPE, never the anchor wording. N of M anchors are Singletons.
  > This author writes structurally similar sentences and words every one differently.

- The distinctive **Z shapes** the taxonomy does not name — these are the paper's own
  frames and often the most imitable thing on the card.

Every frame keeps its verbatim source sentence. A template without an example is a word
list, not a frame.

## C.3 — P: profile indicators (this lens's own work)

The only part of the card not drawn from another file. Judge these by reading; the script
cannot see them.

| dim | what to report |
|-----|----------------|
| voice | active/passive balance, **by section**, with the measured rates from the manifest |
| tense | dominant tense per section |
| person | *we*-prominent / impersonal-passive / "this study"-prominent, and what *we* is reserved for |
| hedging density | the measured per-section rates and where they concentrate |
| claim strength | tentative vs assertive lean; how strong verbs are rationed |
| citation integration | integral vs non-integral, **measured**: count `Author (Year)` against `(Author, Year)` |
| sentence length | the per-section measured values, not just the mean |
| math/quant density | display equations, in-line statistics, symbol glosses |
| display-item reference | the *form* — "Fig." vs "Figure", parenthetical style, caption tense, telegraphic? |
| **does NOT do** | 4–7 structurally absent patterns |
| distinctive moves | 1–3 |

Measure citation integration rather than estimating it:

```bash
py -3.10 -c "import re,sys;t=open(sys.argv[1],encoding='utf-8').read(); \
print('integral', len(re.findall(r'\b[A-Z][a-z]+(?: et al\.)? \(\d{4}', t)))" body.txt
```

Citation *format* (author-year vs numeric) is a venue requirement, not a style trait.
Integral vs non-integral **placement** is the trait worth recording.

### The per-section table is mandatory

Copy `manifest.measured.sections` onto the card and add the sentence beneath it:

> Never judge a draft section against a whole-paper figure.

On the test paper passive ran 21.3/1k in Methods and 5.9/1k in the Introduction — 3.6×.
A Methods paragraph measured against the 13.0/1k average would be told to activize prose
already below its own author's norm. That is not hypothetical; it happened.

## C.4 — Red flags

Absences, written as things to **remove from a draft**, each checkable by search:

1. attitude markers — *interestingly*, *surprisingly*, *unfortunately*
2. a roadmap sentence
3. a standalone Limitations subsection
4. a future-work close
5. the display-item form the author never uses ("Figure 3" when they write "Fig. 3")
6. bulleted lists where the author uses inline "(1)…(2)…and (3)"
7. any connective the author never uses in that section

Absence is a strong signal precisely because a reader cannot infer it from the text.

## C.5 — Output

```markdown
# Style Card: <Author> <Year> · <Journal>

**Source / counting basis / companion files**   ← paths, not copies

## V. Vocabulary          (from style-vocab.md)
## L. Frames & Structure  (from logic.md)
## P. Profile             (this lens)
### P-measured, by section    ← copied from manifest.measured.sections
## Red flags
```

Then fill `manifest.red_flags` and `manifest.distinctive_moves`.

## Cross-check before finishing

- [ ] under ~200 lines
- [ ] every frame has a verbatim source with `[P#-S#]`
- [ ] the recurrence warning appears above the frame list
- [ ] the per-section table is present and the whole-paper warning is under it
- [ ] no technical glossary, no domain noun list
- [ ] every number on the card traces to `manifest.json` or a named file
- [ ] red flags are phrased as removals, not descriptions
