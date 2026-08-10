# Scientific Writing Manual — evidence layer

**This is not the norm reference. It is the citation layer behind the norm references.**

Three assets already answer *what is correct* and *what is broken*. This folder answers
*who says so, in what words, and how well verified* — because none of them carry a quotable
sentence.

| Question | Go to |
|---|---|
| How do I write this section? (structure, transitions, phrasing) | `meta-writing/references/section_guides.md` |
| What is wrong with this paragraph? (single-paragraph diagnosis) | `meta-rewriting/references/section-checklists.md` |
| What is wrong with this manuscript? (panel review, move analysis) | `meta-proofreading/writing-manual/` |
| Why is this sentence hard to read? (reader cognition) | `meta-rewriting/references/principles.md` |
| **I need the actual quote, its source, and whether it was verified** | **here** |
| **The sources disagree and there is no correct answer** | **`DECISIONS.md`** |

`meta-proofreading/writing-manual/` is grounded in genre-analysis literature this corpus does not
contain — Swales CARS, Yang & Allison move analysis, Hyland metadiscourse, Daneš thematic
progression. Where it and this folder overlap on a norm, **it is the better reference.** Come here
for the evidence, not for the ruling.

## When this folder actually opens

Three occasions, not routine reading:

1. **Someone asks "why?"** — a co-author, a supervisor, a reviewer. The other assets compress their
   grounding to a name (`[1차: Ecarnot 2015]`, `Yang & Allison 2003`); this folder has the sentence,
   the page, the supporting sources, and the PDF-verification status.
2. **A contested question comes up** — abstract length, first person, assertion vs hedging, title
   length, abstract voice. `DECISIONS.md` holds both sides with sources. Ask; never default.
3. **A norm reference looks incomplete** — mine `Writing_Principles_Extraction/by-source/` (1,168
   principles with verbatim quotes and page locations) and back-port what is missing. This was done
   on 2026-08-10: 39 items added to `section-checklists.md`, four of which existed in no asset
   (objective chaining, the development-chronicle anti-pattern, running head, pre-empting objections).

Principles are indexed **by where in a manuscript they apply**, so you load one section file rather
than all 277.

Built 2026-08-09 from `Writing_Principles_Extraction/bank/` (185 merged principles distilled from
1,168 raw extractions across 27 sources). Source documents: `../scientific_writing_corpus/`.

**This folder is Claude's output.** `Writing_Principles_Extraction/` is a separate, earlier run by
different agents — do not conflate them. That folder remains the upstream source of record.

---

## Loading protocol

Load **`00_universal.md` plus the one file for the section being worked on.** Nothing else.

| Task | Load |
|---|---|
| Drafting or revising a section | `00_universal.md` + that section's file |
| Sentence/paragraph proofreading | `00_universal.md` (+ `meta-rewriting/references/principles.md` for reader-cognition theory) |
| Planning manuscript structure | `02_introduction.md` + the section files in play |
| Deciding what goes where | this file's table below |
| Preparing to submit | `09_submission.md` |
| Anything touching abstract length, first person, or hedging | **`DECISIONS.md` — and ask the user** |

## Files

| File | Principles | Covers |
|---|---:|---|
| `00_universal.md` | 54 | Sentence and paragraph craft that applies everywhere — concision, active voice, topic sentences, transitions, register, tense |
| `01_title_abstract.md` | 45 | Title, abstract, keywords |
| `02_introduction.md` | 39 | Introduction, literature review, objectives, hypotheses |
| `03_methods.md` | 26 | Methods — reproducibility, design, endpoints, ethics, statistics, instruments |
| `04_results.md` | 20 | Results, figures, tables |
| `05_discussion.md` | 24 | Discussion, limitations, future work |
| `06_conclusion.md` | 2 | Conclusion |
| `07_references.md` | 17 | Citation mechanics, what to cite and what not, reference handling |
| `08_authorship_acknowledgements.md` | 2 | Authorship, acknowledgements |
| `09_submission.md` | 26 | Venue choice, compliance, pre-submission checks, review process, rejection and resubmission |
| `10_thesis_to_article.md` | 1 | Converting a thesis into a journal article |
| `11_writing_process.md` | 51 | Drafting, revision, feedback, timing — not section-specific |
| `12_ai_use.md` | 20 | Generative AI use — **thin evidence, see below** |
| `DECISIONS.md` | 5 | Questions the corpus does not answer. No defaults. |

327 entries total = 185 principles from `bank/` + 11 cross-filings + 131 re-mined. Nine principles
legitimately belong to two or more sections (e.g. `section-structure-61`, Methods↔Results
consistency) and appear in each, marked *also filed under*.

## Re-mined entries (2026-08-09)

The first merge pass collapsed four sections badly. `by-source/` holds far more principles scoped to
each of them than reached `bank/` — a merge artifact, not a gap in the corpus. The material had been
extracted, quoted, and page-located, then collapsed away.

| Section | in `by-source/` | survived into `bank/` | re-mined | now |
|---|---:|---:|---:|---:|
| Title / Abstract | 143 | 16 | +29 | 45 |
| Introduction | 97 | 12 | +27 | 39 |
| Submission | 50 | 7 | +19 | 26 |
| Discussion | 45 | 7 | +17 | 24 |
| Methods | 40 | 8 | +18 | 26 |
| Results | 43 | 12 | +8 | 20 |
| References | 32 | 4 | +13 | 17 |

All six under-recovered sections have now been re-mined. The References pass closed a gap the
original extraction had itself recorded as unrecoverable — *"참고문헌 형식 미시 규칙 — et al. 기준,
학회 인용, URL/ISBN 처리 등 메커닉 유실"* (`Writing_Principles_Extraction/README.md` §5.2). Those
mechanics were not lost; they had been merged away, and are back.

Each recovered entry carries its verbatim quote and originating extraction ID (`b5-schulzrinne-44`,
`ecarnot-2015-38`, `tullu-2019-53`, …), is marked `[+] Re-mined 2026-08-09`, and sits in a separated
block at the end of its file. **Nothing produced by the first pass was altered or removed.**

Additions live in `_remined/`. The build appends them, so regenerating from `bank/` preserves them.

Notable recoveries: the three title types and when each is appropriate, the SPICED/PICO title
checklists, and the seven-part Nature summary-paragraph template with its per-part reading levels
(Title/Abstract); the introduction anti-patterns — the development chronicle, the field-importance
opening, repeating the abstract — and the objective-writing norms (Introduction); over-interpretation
and sample-to-population drift, reverse causation, negative results, diplomatic criticism
(Discussion); figure-anomaly explanation and reproducibility of numerical results (Results).

Two entries are pointers rather than rules: `remined-discussion-17` (assertion vs hedging) routes to
`DECISIONS.md` §D3, and `remined-title-2` flags §D4.

**Re-mining also surfaced two previously unrecorded conflicts** — title length and abstract voice —
now filed as `DECISIONS.md` §D4 and §D5. The over-merge had been resolving them silently instead of
recording the disagreement.

Quote integrity: every re-mined entry resting solely on `ecarnot-2015` or `saver-2007` was checked
against its source PDF at emission. Zero unconfirmed.

## How to read an entry

```
### `section-structure-13` — convergence 9
<the principle, one or two sentences>
> "<verbatim quote from the source>"
**Sources (9):** perneger-2004, hengl-2002, …
**Scope:** Methods
```

The ID is stable and traces back to `Writing_Principles_Extraction/bank/`, which holds the Korean
wording and full merge notes. The quote is verbatim from a source document; page locations are in
`Writing_Principles_Extraction/by-source/<slug>.md`.

## What convergence means — and does not

Convergence = **the number of distinct sources that independently stated this principle.**

It measures *how often writing-advice authors rediscovered an idea.* It does **not** measure how
mandatory the principle is. The clearest proof is in `03_methods.md`: ethics-committee approval,
endpoint specification, and the statistics paragraph all sit at convergence 1, because only one
source in a corpus of general writing guides happened to cover them. They are not optional.

**Rule: never rank by convergence alone.** Institutional requirements (journal instructions,
ethics, reporting standards) outrank stylistic advice regardless of count.

## Quote verification (2026-08-09)

`ecarnot-2015` and `saver-2007` were the two sources that skipped adversarial verification during
extraction — a content filter blocked the sub-agents, so their principles were merged into the
bank unchecked. They have now been cross-checked directly against the source PDFs.

**Method.** Text extracted with `pdftotext` in both plain and `-layout` mode (layout mode is needed
because several quotes sit inside tables). Both the extraction and the PDF text were normalised for
ligatures (`ﬁ`→`fi`), curly quotes, dashes, and hyphenated line breaks — without that step the
matcher produces false failures. Each quote was scored by 5-gram coverage against the PDF.

**Result — all 94 quotes, zero unconfirmed.**

| | ecarnot-2015 | saver-2007 |
|---|---:|---:|
| Quotes checked | 66 | 28 |
| Exact (≥95% coverage) | 42 | 18 |
| Minor drift (70–94%) | 23 | 8 |
| Spliced (30–69%) | 1 | 2 |
| **Unconfirmed** | **0** | **0** |

**No fabricated citations.** Every quote traces to real source text. The defect is citation hygiene,
not invention: about a third show word-level drift (e.g. `ecarnot-2015-2` renders the source's
"in a clear and understandable **fashion**" as "…understandable **form**"), and a few stitch
non-adjacent sentences without marking the gap.

## Inline warnings

| Flag | Count | Meaning |
|---|---:|---|
| `[v] Verified 2026-08-09` | 25 | Sole support is one of the two, and its quote was confirmed verbatim. |
| `[~] Verified with drift` | 9 | Sole support is one of the two; the quote is real but not character-exact. **Re-quote from the PDF before citing.** |
| `[!] Convergence inflated` | 35 | Two or more listed sources are splits of one Twitter account (`tweets-01a`–`01d`). Effective independent count is given. |

`03_methods.md` (5 of 8), `01_title_abstract.md` (7 of 16), `09_submission.md` (4 of 7) and
`04_results.md` (5 of 12) rest solely on these two sources. That dependence is now verified rather
than unknown — but it is still single-source, so treat those entries as one author's advice, not
as a convergent norm.

## Known gaps

- **Peer-review response is now partly covered — but not the response letter itself.** The
  2026-08-10 Submission re-mine recovered how conference review actually decides (score-sorted
  thirds; only the middle band is argued over), who the reviewer may actually be, the ~4-week
  status-query interval, that resubmissions are often what gets funded, and that a resubmission
  goes to *different* reviewers so it may not lean on the earlier round. **Still absent: how to
  write the point-by-point response to reviewers, and the cover letter's content.** That needs
  new sources; the corpus does not hold it.
- **Other sections may be under-merged too.** Results and Discussion were re-mined and roughly doubled;
  the same collapse likely affected `01_title_abstract.md`, `02_introduction.md` and `03_methods.md`,
  which have not been checked against `by-source/` yet. Compare the counts there against the
  `적용:` field in `by-source/` before assuming a section is genuinely thin.
- **`12_ai_use.md` rests on a narrow base**: 6 of its 11 supporting sources are the same Twitter
  account. For AI-related norms prefer institutional guidance — 19 primary policy documents (NRF
  2026.6, EC Living Guidelines 3rd ed., ICMJE 2026.1, COPE, WAME, STM) are held in
  `../ai_ethics/01_originals/policy_guidelines/`.
- **Reader-cognition theory is not here.** Given-new contract, topic/stress position, topic-string
  diagnosis, characters-as-subjects have **zero** corresponding entries in this corpus. They live in
  `~/.claude/skills/meta-rewriting/references/principles.md` (22 sources, triple-verified). Where the
  two overlap, that file is more precise and takes precedence.
- **One source was never obtained**: Paul & Criado (2020), *International Business Review* — a
  literature-review methodology paper. See `../scientific_writing_corpus/MANIFEST.md`.

## Provenance

```
scientific_writing_corpus/          26 original documents (15 papers, 5 books, tweets)
        │
        └── Writing_Principles_Extraction/
              ├── by-source/        1,168 principles + verbatim quotes + page + confidence
              ├── _verify/          adversarial verification (25 of 27 sources)
              └── bank/             185 merged principles, sorted by convergence
                     │
                     └── claude_writing_manual/   ← this folder, re-indexed by location
```

Rebuild: the split is mechanical (no re-authoring), so regenerating from `bank/` is safe and
reproducible. Editing entries here does **not** propagate upstream — fix `bank/` and rebuild.
