---
name: meta-styling-hardcore
description: >-
  Experimental forced style transfer. Imposes an extracted style corpus on an English
  draft in two stages: every sentence is rewritten on one declared corpus sentence frame
  (the script measures how closely the frame was followed, which words are new, and what
  draft content was lost), then general words and lexical bundles are swapped in from the
  corpus by ID only and a script proves every swap. Technical terms, values and citations
  are protected. A pure brick-assembly mode (no rewriting at all) is kept for comparison.
  Use only when the user asks for the hardcore, forced or brick version: "하드코어
  스타일링", "하드코어로 입혀줘", "코퍼스 강제 적용", "벽돌 조립", "brick styling",
  "meta-styling-hardcore". Ordinary style revision goes to meta-styling; corpus building
  to extraction-style; Korean prose to meta-rewriting-korean.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion, Agent]
metadata:
  version: "0.4.0"
---

# Meta-Styling · Hardcore

An experiment, and labelled as one in every report. **The output is not for the
manuscript.** It shows what the draft looks like when its substance is poured into the
corpus's own sentences. `meta-styling` asks, edit by edit, whether a corpus habit fits
the draft. This skill does not ask: every draft sentence is put on a corpus frame, and
every general word that can be replaced by a corpus word of the same kind is replaced.

**Impose first, report the damage.** A frame changes how a claim is framed: its stance
words, its connectives, its causal links, its register. Here that is the experiment
working. Such changes are **imposition effects**: reported, never undone. Only a **hard
failure** is undone: draft substance lost, duplicated or altered (values, entities,
citations, negation), a sentence that does not parse, or a swapped-in word that makes a
collocation English does not have (`maintained criticism`). `verify` lists each swap's
pairs with its neighbours and their corpus counts as evidence; the gate reader decides.

## Two stages: free on structure, strict on words

| Stage | Who | Freedom | Checked by |
|---|---|---|---|
| **1 · Sentence frame** | ② frame writer | rewrites each draft sentence **in its own words** on one declared frame `F###` | `brickyard.py stage1`: frame fit, new-word share, lost draft words, values and citations |
| **2 · Words and bundles** | ③ word mason | none: names replacements by ID (`W###` word, `B###` bundle) | `brickyard.py assemble/verify`: every swap applied by the script, class and part of speech enforced |

**Why split it this way.** Putting a draft sentence on a different syntactic skeleton
needs judgment: a definitional frame `[TERM] is a [CATEGORY] employed to [FUNCTION]`
wants a category noun and an infinitive where the draft has a long clause and a
participle. Pure brick assembly (brick mode, below) forbids that judgment and, on
its first real draft, either withdrew every frame (0.2) or produced a sentence that does
not parse (0.3: `… may proceed employed to bring …`). Word replacement needs no
judgment about syntax, and there strictness costs nothing. So the rewrite is free, and
everything the rewrite did is measured; the vocabulary is strict, and everything is
proven.

### What stage 1 measures (the honesty meters)

The frame writer writes `stage1.json`: for each output sentence, the draft sentences it
comes from (`D#`), the frame it follows (`F###`), and its text. The script then:

- **fit**: share of the frame's fixed words present in the sentence, in order
  (inflection tolerated; a choice token counts if any alternative is there). Below
  `--min-fit` (0.75) is a FAIL: the writer only gestured at the frame. A frame with no
  fixed words imposes nothing and is refused.
- **new words**: every word that is neither a frame word, a draft word (same lemma,
  anywhere in the draft) nor glue. Above `--max-new` (10 % of the stage-1 text) is a
  FAIL: the rewrite is adding its own wording. Every new word is listed for Gate 2.
- **lost draft words**: content words of the source draft sentences that the rewrite no
  longer has. Listed for Gate 2 (a lost word may be a lost claim, or only scaffolding the
  frame replaced).
- **values and citations**: any token with a digit in a source draft sentence that is
  missing from its rewrite is a FAIL. Every draft sentence must be rewritten, merged or
  kept somewhere.

Then `stage1` writes the stage-2 plan: one `{"stage1": "T#"}` sentence per rewrite, so
`assemble` builds the revision from the stage-1 sentences plus the word swaps, and
`verify` re-checks both stages.

## Bricks

| Brick | ID | Comes from | Used in |
|---|---|---|---|
| Frame | `F###` | `logic.md` §E catalog, *Template* / *Frame with slots*, target section only | stage 1 (declared and measured); brick mode (slots filled) |
| Bundle | `B###` | `phrases.tsv`, `bundle = yes`, `topic = no`, in the target section | stage 2 swaps (a draft phrase → a corpus bundle); brick mode slot fillers |
| Word | `W###` | `style-vocab.md` tables and `wordlist.tsv` VERB/ADV/ADJ rows at Freq ≥ 2 (universal or Penn tags), attested in the target section; terms excluded | stage 2 swaps |
| Stage-1 sentence | `T#` | the frame writer's rewrite, after `stage1` passes | stage 2: the base text; swaps key on `T#` |
| Draft sentence | `D#` | the draft, numbered by `pile` | stage-1 `from`; `keep` |
| Content | `C#` | verbatim draft spans | brick mode only |
| Corpus sentence | `S###` | `logic.md` §E original sentence | brick mode with `--unit sentence --own-corpus` only |

### The word layer and claim strength

Reporting verbs, hedges and boosters are style *and* substance. The word layer runs under
a frozen strength classification (`brickyard.py` `STRENGTH`, after Hyland's
metadiscourse categories): `hedge`, `booster`, `report:strong`, `report:moderate`,
`report:tentative`, `report:attribution`, `negation`, `-`.

- **Mechanically:** a swap keeps the class; negation never moves; parts of speech (and,
  for two Penn verb tags, the verb form) must match when both are known; a word inside a
  protected term never moves. A bundle swap obeys the same class rule.
- **The classifier cannot tell a deontic modal from a hedge.** `whether development may
  proceed` (permission) is classed `hedge`, so `may` → `could` would pass and change a
  consent decision into a guess. The cutter therefore lists deontic modals with their
  verb as protected terms (`may proceed`), and Gate 2 reads every hedge swap.
- **Gate 2 reads every swap** and reports what it does to the claim. Effects stay;
  a swap that reverses or falsifies a clause (`trace … to` → `reduce … to`) is HARD.

Protected terms = the cutter's `terms.txt` + every selected paper's `glossary.md`.

## Workers

Four workers, each a fresh context (one Agent tool call each). The orchestrator (this
conversation) never writes a sentence or picks a brick: it runs the scripts, hands files
over, routes HARD rows, and writes the report. **Each worker sees only what its decision
needs.**

| Worker | Sees | Never sees | Writes |
|---|---|---|---|
| ① Cutter | the draft | the corpus | `terms.txt`, `draft-map.md` (strength ledger); in brick mode also `content.tsv` |
| ② Frame writer | draft, draft map, terms, `form.tsv` | `word.tsv`, swaps | `stage1.json` |
| ③ Word mason | **stage-1 sentences** (`pile/stage1.tsv`), draft map, terms, `word.tsv`, bundles in `form.tsv` | frames, the frame writer's notes | `pile/swaps.json` |
| ④ Gate reader | draft, revision, trace, swap list, `stage1.md`, strength profile | piles, plans, reasons | `gate.md` |

In guided mode ③ runs **after** stage 1 passes, because it swaps inside the stage-1
sentences. Briefs and routing are in `references/agents.md`. Without workers, run the
four roles in order in this conversation and record "isolation by ordering".

## How a run works (guided mode, the default)

Run folder `<draft-dir>/run/<draft-stem>/<run-id>-hardcore/`; `<skill>` is this folder.

1. **Scope.** Announce draft, section, corpus, papers, mode, worker isolation, and that
   the run is experimental.
2. **Number the draft.**
   `python "<skill>/scripts/brickyard.py" pile --corpus <corpus> --section I --draft 0-draft.prose.txt --out pile`.
   Exit 2: no frames for that section; check the letter, or ask before `--cross-section`.
3. **① Cutter** → `terms.txt`, `draft-map.md`. Rebuild the pile with `--terms terms.txt`.
4. **② Frame writer** → `stage1.json`. Then
   `python "<skill>/scripts/brickyard.py" stage1 --pile pile --stage1 stage1.json --plan-out plan.json --report stage1.md`.
   A FAIL goes back to ② (fit too low, too many new words, a value or citation dropped,
   a draft sentence uncovered).
5. **③ Word mason** → `pile/swaps.json`, keyed on `T#`.
6. **Assemble and verify.**

   ```text
   python "<skill>/scripts/brickyard.py" assemble --pile pile --plan plan.json --out revision.txt --trace trace.tsv
   python "<skill>/scripts/brickyard.py" verify --pile pile --plan plan.json --revision revision.txt --report verify.md
   python "<meta-styling>/scripts/preservation_inventory.py" --before 0-draft.prose.txt --after revision.gate1.txt --citation-style <author-year|numeric|none> --output inventory.tsv --terms pile/terms.txt
   ```

   `verify` writes `word-swaps.tsv` and `revision.gate1.txt` (the revision without
   `[YOU WRITE: …]` gaps, so a gap's instruction text is not counted by Gate 1).
7. **④ Gate reader** → `gate.md`, every finding sorted into **HARD** or **EFFECT**.
   Route only HARD rows: a frame or rewrite problem to ② (then re-run `stage1`), a
   word or bundle to ③. Re-assemble, re-verify, Gate 1, and a fresh ④. Three rounds at
   most. EFFECT rows are never routed back.
8. **Report.**

### Base option: corpus sentences as frames (0.5.0, on request)

When the user asks to use the corpus's own sentences ("내용이 일치하면 코퍼스 문장 그대로"),
run `python "<skill>/scripts/brickyard.py" match --pile pile [--all-sections]` after step 3.
It indexes every corpus sentence of the section (`M###`, `pile/msent.tsv`) and lists,
per draft sentence, the five closest by content (`pile/match.tsv`: `match` = share of the
draft sentence's content words the corpus sentence has, `extra` = share of its own
content words the draft lacks, `same = yes` at match ≥ 0.80 and extra ≤ 0.20).

② may then write `{"from": ["D#"], "base": "M###", "text": …}`:

- **Verbatim**: the text is the corpus sentence exactly, allowed only when its content is
  the draft sentence's. `stage1` flags it as VERBATIM. It is another author's wording, so
  `verify` fails it on the copy check unless `--allow-copy` (experiment) or
  `--own-corpus` (the user's own papers). The report lists every verbatim sentence with
  its paper and `[P#-S#]`; such text is never offered for a manuscript without quotation.
- **Base**: the corpus sentence becomes a frame for this draft sentence. Its content
  words that the draft sentence lacks, its digits and its names are slots, and every
  other word is fixed. The same meters apply (fit ≥ 0.75, new words ≤ 10 %), so the
  corpus sentence's own claims cannot stay. A base with fewer than four fixed words left
  is refused.

On the EIA-ethics test paragraph no corpus sentence came near the same content (best
match 0.33 with 60 % extra), so verbatim reuse never fired; see the version note.

### Brick mode (for comparison)

The 0.3 pipeline, unchanged: ① also writes `content.tsv`; ② (frame mason) fills frame
slots with content bricks by ID in `plan.json` (with `C#|-det`, `C#|base/s/ing/ed`
transforms, glue, picks, at most three gaps); ③ swaps inside `C#`/`D#`; nothing is ever
retyped. Use it when the user asks for pure brick assembly, or to compare against a
guided run on the same draft. Known limit: slot boundaries can break syntax, because a
draft span cannot change shape beyond the transforms.

## Rules that do not bend

- **The revision is written only by `assemble`.** In guided mode the frame writer's
  sentences enter through `stage1.json`, are measured by `stage1`, and are re-checked by
  `verify`; the word layer then only names IDs. `verify` fails on any hand edit of
  `revision.txt`, and rebuilds `form.tsv` and `word.tsv` from the corpus.
- **Substance comes only from the draft.** Stage 1 may add frame words, glue and at most
  10 % new words; never a new value, entity, citation or claim. Lost, duplicated or
  altered substance is a hard failure. Framing, certainty, causality and scope changes
  are effects.
- **Polarity never flips.**
- **Claim strength stays in class on swaps.** Frame-borne stance changes are effects.
- **Terms and domain words never travel.** A frame whose fixed words name the reference
  paper's subject is not usable.
- **No long corpus runs.** `verify` fails a sentence repeating 8 or more consecutive
  corpus words the draft did not have (`--copy-limit`), unless `--own-corpus`, or
  `--allow-copy` in a base-option experiment, which the report must state.
- **Gates are not relabelled.** A Gate 1 FAIL or a HARD row stays a failure; an EFFECT
  row is never upgraded to justify withdrawing a frame.
- **The user's rules beat the corpus**, as in `meta-styling`.

## Output

In the user's language, in this order:

1. Scope: N, papers, section, mode, isolation, "experimental".
2. Imposition, from `verify.md`: stage 1 (sentences on frames, mean and lowest fit, new
   words and their share, lost draft words), frames by paper, opener and closer hits;
   word layer (swaps by category, bundle swaps, claim-strength swaps).
3. The complete revision, exactly as `revision.txt`.
4. Imposition effects, from `gate.md`: per sentence, what the frame or swap did to the
   claim, with the brick. This is the result of the experiment.
5. Findings: hard failures still standing after three rounds, with the brick blamed;
   draft sentences no frame could take; Gate 1 notation re-parses.
6. Gate results: verify, stage 1, Gate 1, Gate 2.

Offer, in one line, a normal `meta-styling` run when the user wants a manuscript-ready
revision.

## Gotchas

- **Most frames are singletons**, so the skeleton is reused, not the anchor wording.
- **A rewrite can satisfy fit and still drift.** Fit counts the frame's fixed words, not
  whether the claim survived; that is what the lost-word list and Gate 2 are for.
- **Draft-lemma matching is generous.** A word counts as a draft word if its lemma occurs
  anywhere in the draft, so moving a draft word into another sentence is not "new".
- **`wordlist.tsv` drops function words**; connectives and modals reach the word pile
  only through `style-vocab.md`. Without a tagger `wordlist.tsv` contributes no words.
- **Range notation re-parses in Gate 1** (`between 12 and 40` → `from 12 to 40`): report
  it as a notation change; never relabel it.
- **Catalog layouts vary.** The parser reads *Template* or *Frame with slots* columns, a
  *Section* cell, bare `### I` headings or named headings. Check `form.tsv` first.
- **The sentence splitter** protects `et al.`, `Fig.`, `e.g.`, decimals and page
  references (`p. 12`, `pp. 3–4`).

## Error handling

| Situation | Response |
|---|---|
| No corpus, or several | As `meta-styling`: ask; never build one |
| `pile` exit 2 | No frames for the section; check the letter or ask about `--cross-section` |
| `stage1` FAIL | Back to ② with the report; never edit `stage1.json` yourself |
| Empty word pile | Report it; run stage 1 alone |
| `assemble` errors | The owner of the brick fixes plan or swaps; nothing was written |
| `verify` FAIL on hand edit or pile tampering | Re-assemble or rebuild the pile; never patch the text |
| `verify` FAIL on copy run | Back to ② for another frame or wording |
| Gate 1 FAIL or HARD row after three rounds | Report it as a hard failure of the experiment |
| Gate 2 EFFECT rows | Report them as the result; never route them back |
| Agent tool unavailable | Same roles in order; "isolation by ordering" |
| Korean draft | Stop; point to `meta-rewriting-korean` |

## Usage examples

```
> "SCI_kkh 코퍼스로 이 Results 단락 하드코어 스타일링 해봐"
> "코퍼스 강제로 입혀서 어떻게 나오는지 보자 — Discussion 2문단"
> "벽돌 조립 방식으로만 해봐"            (→ brick mode)
> "내 논문들로 만든 코퍼스니까 문장 단위 벽돌로 해봐"   (→ brick mode, --unit sentence, --own-corpus)
```

---

**Version**: 0.5.0 (2026-11-26) — base option: `match` indexes corpus sentences and
ranks them by content overlap per draft sentence; a stage-1 sentence may stand on a
corpus sentence (`base`), either verbatim (flagged; copy check, `--allow-copy`) or as an
automatically derived frame whose slots are the corpus sentence's own content.
`brickyard.py` 1.5.1 (glossary.md read by its table rows only). Tested on the
EIA-ethics Introduction and Section 2 paragraphs (5-paper corpus) and on a
hydrogeochemistry Results paragraph (17-paper SCI_high corpus, 3.1.0): the science
paragraph passed Gate 2 in one round; known open points — frames add hedges to
unhedged claims (verify warns only), and Gate 1 should take the draft's terms.txt,
not pile/terms.txt (large corpus glossaries give false term hits such as ha/has).
**Previous**: 0.4.1 (2026-11-26) — collocation: `verify` writes each swap's neighbour
pairs and their corpus counts to `word-swaps.tsv` and lists the unattested ones; the
word mason reads each swap with its neighbours; the gate reader treats a non-English
collocation as HARD and routes it to the word mason. `brickyard.py` 1.4.0.
0.4.0 (2026-11-26) — two stages: a guided rewrite on one declared frame per
sentence, measured by `brickyard.py stage1` (fit, new-word share, lost words, values and
citations), then strict word and bundle swaps by ID on the stage-1 sentences; brick
assembly kept as brick mode; Gate 1 runs on a gap-free copy; deontic modals protected
as terms. `brickyard.py` 1.3.0.
0.3.0 (2026-11-26) — HARD vs EFFECT, content transforms, Penn tags, parser
fixes; on the test paragraph it put 6 of 8 sentences on frames but broke one sentence at
a slot boundary. 0.2.0 (2026-11-25) — word layer, four workers; on the same paragraph it
withdrew every frame. 0.1.0 (2026-11-25) — frame and bundle bricks.
**Consumes**: `extraction-style` v3.x corpus (`logic.md` §E; `phrases.tsv`,
`wordlist.tsv`, `glossary.md` from 3.1; `style-vocab.md`).
**Depends on**: `meta-styling/scripts/preservation_inventory.py` 1.1.0.
**Status**: experimental. `scripts/test_brickyard.py` 24 cases on a toy corpus. Guided
mode is being tested on the EIA-ethics Introduction paragraph used for 0.2 and 0.3.
