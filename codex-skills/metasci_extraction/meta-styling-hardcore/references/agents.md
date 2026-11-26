# Workers: who sees what, and the briefs

Four workers, each a fresh context (one `spawn_agent` call each). The orchestrator (the
main conversation) never writes a revision sentence and never picks a brick. It runs the
scripts, hands files over, routes HARD rows, and writes the report. The design follows
one principle: **a worker sees only what its decision needs. Anything more becomes a
temptation or an anchor.**

## Guided mode (default)

```text
                 0-draft.prose.txt
                        │
               ① CUTTER (draft only, no corpus)
                 terms.txt · draft-map.md
                        │
           orchestrator: pile --terms terms.txt
                        │
               ② FRAME WRITER (draft + frames; no word pile)
                 stage1.json: per sentence, from D#, frame F###, rewritten text
                        │
           orchestrator: stage1 → stage1.md, pile/stage1.tsv, plan.json
             (FAIL → back to ②: fit, new words, values/citations, coverage)
                        │
               ③ WORD MASON (stage-1 sentences + word pile + bundles; no frames)
                 pile/swaps.json keyed on T#
                        │
           orchestrator: assemble → verify → Gate 1 (revision.gate1.txt)
                        │
               ④ GATE READER (draft + revision only)
                 gate.md: HARD / EFFECT per sentence, the brick to blame
                        │
           orchestrator: route HARD rows (≤ 3 rounds, a fresh ④ each round) → report
```

| Worker | Sees | Never sees | Writes |
|---|---|---|---|
| ① Cutter | `0-draft.prose.txt`, `pile/draft.tsv`, the user's rules | anything in the corpus | `terms.txt`, `draft-map.md` |
| ② Frame writer | draft, `draft.tsv`, `draft-map.md`, `terms.txt`, `form.tsv` | `word.tsv`, swaps | `stage1.json` |
| ③ Word mason | `pile/stage1.tsv`, `draft-map.md`, `terms.txt`, `word.tsv`, bundle rows of `form.tsv`, `references/plan-format.md` | frame rows, the frame writer's reasons | `pile/swaps.json` |
| ④ Gate reader | `0-draft.prose.txt`, `revision.txt`, `trace.tsv`, `word-swaps.tsv`, `stage1.md`, strength profile | the piles, the plan, the workers' reasons | `gate.md` |

## Why these four, and not others

- **The cutter is blind** so that the corpus cannot shape what counts as a term (protected
  from the word layer) or how the draft's claims are read in the strength ledger.
- **The frame writer writes, the script measures.** Rewriting a sentence on another
  skeleton needs judgment, so the writer is free; but it must declare the frame, and
  `stage1` measures fit, new words, lost words, values and citations. The writer never
  sees the word pile, so it cannot pre-empt the word layer, and the two layers stay
  separately measurable.
- **The word mason works after stage 1**, on the sentences the reader will see. It sees
  bundles but not frames: a bundle is a phrase to swap in, not a skeleton to rebuild on.
  One mason, not one per part of speech, because verb and adverb choices in one clause
  jointly set its certainty.
- **The gate reader is unanchored**: two texts and the mechanical evidence, not the
  reasons. A fresh reader each round.
- **Assembly and verification are scripts**, not workers.

For a long draft (more than about six paragraphs) the frame writer may be split by
paragraph; the orchestrator concatenates the `paragraphs` lists before `stage1`.

**No workers?** Run the four roles in order in the main conversation: ① before
`form.tsv` or `word.tsv` is opened, ② before `word.tsv` is opened, ③, ④. Record
"isolation by ordering"; it is weaker, and the report says so.

## Briefs

Copy these, filling the angle brackets. Each brief is the worker's only context.

### ① Cutter

> You are preparing an English academic draft for an experiment in which its sentences
> will be rebuilt on another corpus's sentence frames. You do not see the corpus and must
> not try to guess it. Read `<run>/0-draft.prose.txt` and `<run>/pile/draft.tsv` (the
> draft's sentences, numbered D#). The user's rules: <rules or "none">.
>
> 1. Write `<run>/terms.txt`: every technical term of the draft, one per line, multi-word
>    terms whole. When in doubt, list it: a listed term is protected from the word layer.
>    Also list every **deontic modal with its verb** (`may proceed`, `must be assessed`):
>    the strength classifier cannot tell permission from a hedge.
> 2. Write `<run>/draft-map.md`: per paragraph, its function (Background, Finding,
>    Interpretation …); per sentence, its role and a **strength ledger** — every hedge,
>    booster, reporting verb and negation with the claim it qualifies; and the claims and
>    list items each sentence carries, so a reader can check that nothing was lost.
> 3. Brick mode only: also write `<run>/pile/content.tsv` (verbatim spans; see
>    plan-format.md §content.tsv, cut at heads) and run `brickyard.py content`.
>
> Return only the file paths and one line of counts.

### ② Frame writer

> Rewrite an English academic draft paragraph so that every sentence stands on one
> corpus sentence frame. This is an experiment, not a manuscript edit: the point is to
> see the draft's substance inside the corpus's sentences.
>
> Read `<skill>/references/plan-format.md` §stage1.json, then `<run>/pile/form.tsv`
> (frames F###; columns id kind paper section code name pos status source slots text),
> `<run>/pile/draft.tsv`, `<run>/draft-map.md`, `<run>/terms.txt`. Do not open
> `<run>/pile/word.tsv` or any swaps file. Write `<run>/stage1.json`.
>
> - For each draft sentence choose one frame and rewrite the sentence **on it**: keep the
>   frame's fixed words in order (inflect them for agreement as needed), fill its slots
>   with the draft's substance, and drop a slot the draft has nothing for. You may split a
>   draft sentence over two frames or merge two draft sentences into one frame; list
>   every source D# in `from`.
> - Use the draft's own words for its substance. Add words only where the frame's syntax
>   needs them (an article, a preposition, a category noun the frame demands); every word
>   that is neither a frame word nor a draft word is counted as new, and the run fails
>   above 10 % new words. Never add a value, entity, citation or claim.
> - A change of stance, certainty, causal link or register brought by the frame's fixed
>   words is **not** a reason to avoid the frame: it is the effect being measured.
> - Keep every value, citation (with page numbers) and protected term, each on its own
>   claim. Never negate or un-negate a claim.
> - Open each paragraph on a frame with `pos = initial` (or `solo`); close on
>   `pos = final` where one fits. Use frames from at least <min(N,3)> papers; prefer 2–4
>   frames from one paper in source order. A frame whose fixed words name the reference
>   paper's own subject is not usable; a frame with no fixed words imposes nothing and is
>   refused.
> - `{"from": ["D#"], "keep": true, "why": "<the frame slot that could not take it>"}`
>   only when no frame can take the sentence at all.
> - No 8 or more consecutive corpus words that the draft does not have.
>
> **Base option** (only when the orchestrator says so): also read `<run>/pile/match.tsv`
> (per draft sentence, the closest corpus sentences `M###` with `match`, `extra`, `same`)
> and `<run>/pile/msent.tsv`. For each draft sentence:
> - If a candidate carries the same content (nothing of the draft missing, nothing of its
>   own added; `same = yes` is a hint, you decide), use it **verbatim**:
>   `{"from": ["D#"], "base": "M###", "text": "<the corpus sentence exactly>"}`.
> - Otherwise rewrite on the closest usable candidate as a **base**: keep its words in
>   order, replace its own content (claims, names, values, citations) with the draft's,
>   and drop what the draft has nothing for. `stage1` derives the fixed words: every word
>   of the corpus sentence except its content words that the draft sentence lacks.
> - Use a frame `F###` when no candidate keeps four fixed words or the fit fails.
>
> Run `python <skill>/scripts/brickyard.py stage1 --pile <run>/pile --stage1 <run>/stage1.json --plan-out <run>/plan.json --report <run>/stage1.md`
> and revise `stage1.json` until it passes (fit ≥ 0.75 for every sentence, new words
> ≤ 10 %, no value or citation missing, every D# covered). Read the lost-words column: a
> lost word that carried a claim must come back. Return the stage-1 report path, and per
> draft sentence the frame(s) used (ID + paper).

### ③ Word mason

> Impose the corpus's general vocabulary on rewritten sentences, by ID only. Read
> `<skill>/references/plan-format.md` (§swaps.json), then `<run>/pile/stage1.tsv` (the
> stage-1 sentences, T#), `<run>/pile/word.tsv` (W###; `pos` is a universal or Penn tag),
> the `bundle` rows of `<run>/pile/form.tsv` (B###; ignore the `frame` rows),
> `<run>/terms.txt`, `<run>/draft-map.md`. Write `<run>/pile/swaps.json`, keyed on T#.
>
> - For every verb, adverb, adjective and connective in a T# sentence that is not inside
>   a protected term: if `word.tsv` has a corpus word of the same part of speech and form,
>   the same claim-strength class, and a meaning that keeps the proposition recognisable,
>   swap it. Prefer higher `count`. A shift of nuance or scope is an effect the gate
>   reader reports, not a reason to skip. Skip a word only when no such brick exists or
>   the swap would reverse or falsify the proposition.
> - Read each replacement **with its neighbours**. A swap must leave a pairing an English
>   academic writer would use (`sustained criticism` → `maintained criticism` fails;
>   `widespread adoption` → `global adoption` passes). When the first-choice brick does
>   not collocate, take another `W###` that does; skip the word only when none does.
> - Where a T# sentence has a multi-word phrase with the same function as a corpus
>   bundle (`because of` → `as a result of`), swap the phrase for the bundle
>   (`"because of": "B012"`).
> - Never touch technical terms, numbers, names, citations, or negation. The script
>   refuses class changes anyway.
>
> Run `python <skill>/scripts/brickyard.py assemble --pile <run>/pile --plan <run>/plan.json --out <run>/revision.txt --trace <run>/trace.tsv`
> until it exits 0. Return the swaps path and the number of swaps by category, plus the
> distinct pairs.

(Brick mode: the same brief on `content.tsv` and `draft.tsv`, keyed on C# and D#.)

### ④ Gate reader

> You check one revision against its original. You did not write either. Read
> `<run>/0-draft.prose.txt` (original) and `<run>/revision.txt` (revision);
> `<run>/trace.tsv` says which brick produced each piece; `<run>/word-swaps.tsv` lists
> every word replacement with the pairs it makes with its neighbours (`left_pair`,
> `right_pair`), how often each pair occurs in the corpus (`left_n`, `right_n`; `glue`
> for a function-word neighbour) and a `collocation` flag; `<run>/stage1.md` lists, per stage-1 sentence, its frame, the
> new words and the draft words it lost; the strength profile is: <paste from verify.md>.
>
> This revision is an experiment, not a manuscript text: it imposes another corpus's
> sentences on the draft on purpose. Sort every finding into one of two kinds:
> - **HARD**: draft substance lost, duplicated or altered (a value, entity, list item or
>   proposition — including a word swap or a rewrite that reverses or falsifies a
>   clause, or a new word that adds a claim); a citation or display reference moved off
>   its claim; negation flipped; a sentence that does not parse; a **collocation that does
>   not exist in English**: a swapped-in word that pairs with its neighbour in a way a
>   copy-editor would mark as an error (`maintained criticism`, `greater critiques`,
>   `developed particularly little`). Blame the `W###`/`B###`.
> - **EFFECT**: what the frame, rewrite or swap did to the claim's framing — stance,
>   certainty, causal link, scope, register, cohesion, an added gap.
>
> 1. Gate 2, sentence by sentence, mapping merged or split sentences to their originals.
>    Read every new word and every lost word listed in `stage1.md`, and every swap.
>    Read every swap's two pairs. The corpus counts are evidence, not the verdict: the
>    corpus is a few papers, so most sound pairs are unattested (`unattested` alone is
>    never a reason). A pair that is grammatical and idiomatic but less natural, or that
>    shifts nuance, is an EFFECT; only a pair that is not English usage is HARD.
> 2. Reader pass: read the revision once as a reviewer for <journal or field>.
>
> Write `<run>/gate.md`: one row per revision sentence — `PASS`, `HARD` and/or `EFFECT`
> (each finding separately), the reason, and what is most responsible: the stage-1
> sentence (`T#` with its frame), a word or bundle (`W###`, `B###`). Then the Gate 2
> verdict: FAIL if any HARD row stands, otherwise PASS. EFFECT rows never make it FAIL.
> Do not propose rewritten sentences.

## Brick mode

Brick mode replaces ② with the frame mason below; ① also writes `content.tsv`; ③ swaps
inside C# and D#; nothing is ever retyped.

### ② Frame mason (brick mode)

> Rebuild the draft on corpus sentence frames, by ID only. Read
> `<skill>/references/plan-format.md`, then `<run>/pile/form.tsv` (frames F###, bundles
> B###), `<run>/pile/content.tsv`, `<run>/pile/draft.tsv`, `<run>/draft-map.md`.
> Write `<run>/plan.json`.
>
> - This run is an experiment, not a manuscript edit: the point is to see the draft's
>   substance inside the corpus's sentences. If any frame can host a sentence's content
>   bricks, use one. Awkwardness, a change of stance, certainty, causal link or register
>   brought by the frame's fixed words are **not** reasons to skip: they are the effect
>   being measured, and the gate reader reports them. Only a frame whose slots cannot take
>   the content, even with transforms (`C#|-det`, `C#|base`/`s`/`ing`/`ed`, see
>   plan-format.md) and with slots omitted (`[]`), is unusable. Otherwise
>   `{"keep": "D#"}`, and name the slot that failed.
> - Open each paragraph on a frame with `pos = initial` (or `solo`); close on
>   `pos = final` or a gap. Prefer runs of 2–4 frames from one paper in source order.
>   Use frames from at least <min(N,3)> papers.
> - Glue words, picks and inflections only to make a template agree with its content. At
>   most <3 − gaps already used> gaps, one line each, never carrying content.
> - Hard limits: every substantive content brick appears exactly once (no loss, no
>   duplication); each citation stays on its claim; no frame negates or un-negates a
>   draft claim; no frame names the reference paper's own subject. A frame slot the draft
>   has nothing for is omitted with `[]` where the sentence still parses, otherwise a gap.
>   Split a long draft sentence over two frames when that lets frames carry it.
>
> Run `python <skill>/scripts/brickyard.py assemble --pile <run>/pile --plan <run>/plan.json --out <run>/revision.txt`
> until it exits 0. Never write `revision.txt` yourself. Return the plan path and, for
> each `keep`, one line on why no frame could host it.

## Routing a failure

| Blamed | Goes back to | With |
|---|---|---|
| T# / F### (guided: the rewrite or its frame) | ② frame writer (continue the same worker), then `stage1` again | the `gate.md` rows |
| W### / B### (meaning or collocation) | ③ word mason (continue the same worker): another brick that collocates, or drop that swap | the `gate.md` rows |
| a term or ledger error | ① cutter, then ② and ③ re-check | the rows |
| brick mode: F### / pick / glue / gap / C# | ② frame mason / ① cutter | the rows |

Only HARD rows are routed. EFFECT rows go into the report as the experiment's result and
are never sent back: a worker that withdraws a frame because of an effect undoes the
experiment. After stage 1 changes, re-run `stage1`; the T# numbering may shift, so ③
re-checks its keys. Then assemble, verify, Gate 1, and a **fresh** ④. Three rounds at
most; what still fails is a finding of the experiment, reported as such.
