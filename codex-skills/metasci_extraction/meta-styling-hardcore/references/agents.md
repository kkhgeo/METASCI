# Workers: who sees what, and the briefs

Four workers, each a fresh context (one `spawn_agent` call each). The orchestrator (the
main conversation) never picks a brick. It runs the scripts, hands files over, routes
failures, and writes the report. The design follows one principle: **a worker sees only
what its decision needs. Anything more becomes a temptation or an anchor.**

```text
                 0-draft.prose.txt
                        │
               ① CUTTER (draft only, no corpus)
                 content.tsv · terms.txt · draft-map.md
                        │
           orchestrator: pile --terms terms.txt
             ┌──────────┴──────────┐
  ② FRAME MASON                ③ WORD MASON            (parallel)
  form.tsv + content           word.tsv + content
  → plan.json                  → swaps.json
             └──────────┬──────────┘
           orchestrator: assemble → verify → Gate 1
                        │
               ④ GATE READER (draft + revision only)
                 gate.md: per-sentence verdicts, the brick to blame
                        │
           orchestrator: route FAILs back to ② or ③ (≤ 3 rounds,
           a fresh ④ each round) → report
```

| Worker | Sees | Never sees | Writes |
|---|---|---|---|
| ① Cutter | `0-draft.prose.txt`, `pile/draft.tsv`, the user's rules | anything in the corpus | `pile/content.tsv`, `terms.txt`, `draft-map.md` |
| ② Frame mason | `content.tsv`, `draft.tsv`, `draft-map.md`, `form.tsv`, `references/plan-format.md` | `word.tsv`, swaps | `plan.json` |
| ③ Word mason | `content.tsv`, `draft.tsv`, `draft-map.md`, `terms.txt`, `word.tsv`, `references/plan-format.md` | `form.tsv`, the plan | `pile/swaps.json` |
| ④ Gate reader | `0-draft.prose.txt`, `revision.txt`, `trace.tsv`, `word-swaps.tsv`, the strength-profile lines of `verify.md` | the piles, the plan, the masons' reasons | `gate.md` |

## Why these four, and not others

- **The cutter is blind for the same reason meta-styling tags first.** What counts as
  substance (a content span) and what counts as a term (protected from the word layer) is
  decided before the corpus is in view. A cutter that has seen a frame with slot
  `[INTERPRETATION]` will cut the draft to fit it; a cutter that has seen `governs` in the
  word pile will leave `controls` outside a term. Either way the corpus has edited the
  draft before any rule could check it.
- **Frames and words are separate masons** because they draw on different piles, fail in
  different ways, and are blamed separately by `trace.tsv` (`frame`/`bundle` rows vs
  `word` rows). A single mason holding both piles reaches for a word swap to make a frame
  fit, and the imposition of each layer can no longer be measured on its own. The two
  write to different files, so they run in parallel without coordination; a word swapped
  twice is caught by the script.
- **The word layer is one mason, not one per part of speech.** Verb and adverb choices in
  one clause jointly set its certainty (`may indicate`, `clearly shows`). Splitting by
  part of speech gives two workers editing one clause with no one owning its strength,
  and a stream of swap conflicts.
- **The gate reader is unanchored.** Both masons are invested in their choices. The
  reader gets the two texts and the mechanical evidence, not the reasons. Reasons invite a
  reviewer to accept an intention instead of the text. A fresh reader each round, so that
  a verdict is not anchored on the previous verdict either.
- **Assembly and verification are not workers.** They are deterministic and run as
  scripts; an agent there would only add a place for retyping to creep back in.

For a long draft (more than about six paragraphs) the frame mason may be split by
paragraph: each worker gets its paragraphs' content bricks and the whole `form.tsv`, and
the orchestrator concatenates the `paragraphs` lists. The min(N, 3)-papers rule is then
checked on the merged plan.

**No workers?** When the `spawn_agent` is unavailable or the user has not authorised
workers, run the same four roles in order in the main conversation: ① before
`form.tsv` or `word.tsv` is opened, ② and ③ one after the other, ④ last. Record
"isolation by ordering" in the report; it is weaker, and the report says so.

## Briefs

Copy these, filling the angle brackets. Each brief is the worker's only context.

### ① Cutter

> You are preparing an English academic draft for an experiment in which its sentences
> will be rebuilt from numbered bricks. You do not see the bricks and must not try to
> guess them. Read `<run>/0-draft.prose.txt` and `<run>/pile/draft.tsv` (the draft's
> sentences, numbered D#). The user's rules: <rules or "none">.
>
> 1. Write `<run>/pile/content.tsv`: content bricks `C#<TAB>span`, each span copied
>    verbatim from the draft. Follow the cutting rules in
>    `<skill>/references/plan-format.md` (§content.tsv): cut values, entities, properties,
>    groups and propositions; keep each citation and display reference inside the span of
>    the claim it supports; leave the draft's framing verbs and connectives uncut; keep a
>    hedge or modal that carries certainty inside its span. Then run
>    `python <skill>/scripts/brickyard.py content --pile <run>/pile` until it passes.
> 2. Write `<run>/terms.txt`: every technical term of the draft, one per line, multi-word
>    terms whole. When in doubt, list it: a listed term is protected from the word layer.
> 3. Write `<run>/draft-map.md`: per paragraph, its function (Background, Finding,
>    Interpretation …); per sentence, its role and a **strength ledger** — every hedge,
>    booster, reporting verb and negation with the claim it qualifies.
>
> Return only the three file paths and one line of counts.

### ② Frame mason

> Rebuild the draft on corpus sentence frames, by ID only. Read
> `<skill>/references/plan-format.md`, then `<run>/pile/form.tsv` (frames F###, bundles
> B###), `<run>/pile/content.tsv`, `<run>/pile/draft.tsv`, `<run>/draft-map.md`.
> Write `<run>/plan.json`.
>
> - If any frame can host a sentence's content bricks, use one. Awkwardness is not a
>   reason to skip; only a frame whose slots cannot take the content is. Otherwise
>   `{"keep": "D#"}`.
> - Open each paragraph on a frame with `pos = initial` (or `solo`); close on
>   `pos = final` or a gap. Prefer runs of 2–4 frames from one paper in source order.
>   Use frames from at least <min(N,3)> papers.
> - Glue words, picks and inflections only to make a template agree with its content. At
>   most <3 − gaps already used> gaps, one line each, never carrying content.
> - A frame's fixed words may bring their own verb or hedge (`suggest(s)`, `likely`).
>   Check the strength ledger: do not pick a frame whose fixed words change the
>   certainty of the claim it carries.
>
> Run `python <skill>/scripts/brickyard.py assemble --pile <run>/pile --plan <run>/plan.json --out <run>/revision.txt`
> until it exits 0. Never write `revision.txt` yourself. Return the plan path and, for
> each `keep`, one line on why no frame could host it.

### ③ Word mason

> Impose the corpus's general vocabulary on the draft's content bricks, by ID only. Read
> `<skill>/references/plan-format.md` (§swaps.json), then `<run>/pile/word.tsv`,
> `<run>/pile/content.tsv`, `<run>/pile/draft.tsv`, `<run>/terms.txt`,
> `<run>/draft-map.md`. Write `<run>/pile/swaps.json`.
>
> - For every verb, adverb, adjective and connective in a content brick that is not a
>   term: if `word.tsv` has a corpus word of the same part of speech, the same
>   claim-strength class, and a meaning that keeps the proposition true, swap it. Prefer
>   higher `count`. Skip a word only when no such brick exists.
> - Also swap inside draft sentences the plan may keep (key them by D#).
> - Never touch technical terms, numbers, names, citations, or negation. Never change a
>   hedge into a non-hedge or a tentative reporting verb into a strong one; the script
>   refuses those anyway.
>
> Run `brickyard.py assemble` with the frame plan if it already exists, otherwise check
> that every key you used occurs in its brick. Return the swaps path and the number of
> swaps by category.

### ④ Gate reader

> You check one revision against its original. You did not write either. Read
> `<run>/0-draft.prose.txt` (original) and `<run>/revision.txt` (revision);
> `<run>/trace.tsv` says which brick produced each piece; `<run>/word-swaps.tsv` lists
> every word replacement; the strength profile is: <paste from verify.md>.
>
> 1. Gate 2, sentence by sentence, mapping merged or split sentences to their originals:
>    values attached to the same entity, unit and uncertainty; citations and display
>    references attached to the same claim; negation, conditions, certainty, causality and
>    scope unchanged; nothing added or lost. Read every word swap and every
>    claim-strength change as a possible certainty shift.
> 2. Reader pass: read the revision once as a reviewer for <journal or field>. Note each
>    sentence that would make that reader stop.
>
> Write `<run>/gate.md`: one row per revision sentence — `PASS`/`FAIL`/`STOP`, the reason,
> and the brick ID from `trace.tsv` most responsible (F###, B###, W###, C#). Then the Gate
> 2 verdict: PASS, FAIL or BLOCKED. Do not propose rewritten sentences.

## Routing a failure

| Brick blamed | Goes back to | With |
|---|---|---|
| F### / B### / pick / glue / gap | ② frame mason (continue the same worker) | the `gate.md` rows |
| W### | ③ word mason (continue the same worker) | the `gate.md` rows |
| C# (a bad cut) | ① cutter, then ② and ③ re-check their files | the rows; content IDs are kept where possible |

Then assemble, verify, Gate 1, and a **fresh** ④. Three rounds at most; what still fails
is a finding of the experiment, reported as such.
