# Style Revision Guide (meta-styling v4.0)

Stage-by-stage procedure. Read this whole file before Stage 0.

**What changed from v3.0:** prescriptions come from a structural diff against the
reference's `logic.md`, not from steering three numbers toward the card's values. Numbers
are a sanity check at the end. Output is 2–3 candidate revisions with a recommendation.

---

## Stage 0 — Separate, check, segment

A real manuscript is rarely a clean block of prose. Do these five steps **in this order** —
the ordering is the fix for a defect that aborted a live run.

### 0.1 Separate manuscript prose from scaffolding

Working drafts carry material that is *about* the manuscript but is not manuscript:

| scaffolding | examples seen in practice |
|-------------|---------------------------|
| the author's own working rules | `## A) Approach Checklist / 작업 기준` |
| source or evidence summaries | `## B) Source Summary` |
| open questions / author queries | `## D) 미해결 / 저자 확인 대기` |
| ledgers and transfer tables | `Caption_Transfer_Ledger.md` cross-references |
| a translation mirror | Korean text paralleling the English master |
| drafting notes | 집필 메모, TODO, bracketed reminders |

**None of it is measured, tagged, compared, or revised.** Extract the manuscript prose to
`0-draft.prose.txt` and list what you excluded, with line ranges, in `0-draft.repr.md` so
the author can dispute the cut.

Where the draft names its own scope ("현재 집필분은 3.1 전체(P1–P3)"), follow it — that is
the author telling you what exists, not you narrowing the job.

### 0.2 Check the language — on the PROSE, never on the raw file

```bash
py -3.10 "<skills-dir>/meta-styling/scripts/quant_check.py" profile 0-draft.prose.txt
```

Stop only if **the extracted prose** is not English, and point to
`meta-mywriting-korean` or `meta-report-writing`.

> **Never run the language check on the raw file.** Measured on a live draft: a 3,458-word
> working document whose manuscript prose is entirely English returned `lang: ko`, because
> 43% of the *file* was Korean scaffolding. Checking the raw file would have aborted the
> run before Stage 1 on a manuscript this skill is built for.

### 0.3 Read the draft's own style spec, if it has one

Many working drafts carry explicit style rules (§A above is one). They are a **competing
authority** and they win.

| case | handling |
|------|----------|
| draft rule **agrees** with the corpus | FIRM — cite both |
| draft rule **conflicts** with the corpus | **the draft rule wins.** Never apply the corpus habit silently. Log it as a CHOICE item naming both sides, so the author can relax their own rule if they want to |
| draft rule covers something the corpus is silent on | adopt it as a BAND or FIRM item, sourced to the draft |
| draft rule cites its own reference evidence | treat as strongest — the author has already done an extraction |

A real conflict, for the record: a draft rule read *"`[관찰]` 단락에서 suggest·indicate
금지"* while the corpus showed `indicat*` as the author's own-inference lane in **both**
cards. The draft rule governed; the corpus habit was offered as a candidate, not imposed.

Record the spec verbatim in `0-draft.repr.md`. A rule you did not record is a rule the
author cannot check you against.

### 0.4 Resolve the corpus and count N

```bash
ls -d <corpus-root>/papers/*/          # slugs available
ls <corpus-root>/style_profile.md      # optional cache; absence is normal
```

The draft may reference a corpus this skill was not given (the example above cites a
`choi-2007` corpus). **Do not go looking for it.** Note that the draft-side rules rest on
evidence you cannot see, and treat those rules as authoritative anyway.

### 0.5 Segment

Create the run folder **next to the draft**, never inside the corpus:

```
<draft-dir>/run/<draft-stem>/
```

Number paragraphs `P1…Pn` and sentences `S1…Sn` within each paragraph. That address is
what joins every later artifact.

**Artifact `0-draft.repr.md`** — draft path, section, token count of the *prose*, paragraph
count, the excluded-scaffolding list with line ranges, the draft's own style spec verbatim,
and the numbered text.

**Announce before continuing:** `N=<n> tier=<tier> cards=[…] section=<X>`, plus one line
naming what was excluded as scaffolding. The user must be able to object to both the scope
and the cut before a pass is spent on them.

---

## Stage 1 — Three independent analyses

Runs in parallel. Each reads little and returns little.

### 1a — Structure tag (reads the DRAFT ONLY)

Tag the draft in the same taxonomy `logic.md` uses.

**Paragraph functions** — *Introduction*: Background · Literature-Review · Gap · Question ·
Purpose · Scope · Contribution. *Methods*: Study-Area · Design · Sample · Procedure ·
Instrument · Statistical · Quality. *Results*: Overview · Finding · Comparison · Trend ·
Pattern · Anomaly · Summary. *Discussion*: Interpretation · Mechanism · Lit-Comparison ·
Agreement · Disagreement · Limitation · Implication · Future · Conclusion.

**Relations between paragraphs** — Continuation · Contrast · Cause-Effect · Specification ·
Generalization · Sequence · Concession · Problem-Solution · Evidence-Claim · Question-Answer.

**Sentence roles** — Topic · Claim · Evidence · Elaboration · Example · Transition ·
Qualification · Reference · Method · Conclusion · Bridge.

**Frame codes** — A1–L4 plus `Z` for anything the taxonomy does not name. Shared with
`extraction-logic` and `extraction-style`; the table lives in that skill's
`references/lens-architecture.md` §A.4. **Do not invent codes.** Expect a high `Z` rate — on
the two papers measured so far it ran 39.5% and 26.5%, an order of magnitude above the
taxonomy's illustrative 3%. A high `Z` rate is the interesting part, not a tagging failure.

> **Do not read the reference in this stage.** Tagging a draft against a known target
> pulls the tags toward it and manufactures a match that isn't there. Tag blind.

**Artifact `1a-structure.md`** (≤ 55 lines):

```markdown
draft: my_methods.txt   section: M   tokens: 112   paragraphs: 3

## P1  function=Procedure  relation-to-next=Sequence
S1  role=Method     frame=E1  "A total of 88 groundwater samples were collected …"
S2  role=Reference  frame=F5  "Fig. 2 shows the sampling network …"
```

Over ~1,500 tokens: tag paragraph functions for all, sentence roles for two
representative paragraphs only, and record that sampling was applied.

### 1b — Vocabulary measure

Build `profile_vocab.txt` from the cards' §V items (reporting verbs, hedges, stance,
connectives, register habits) plus every Red-Flag term. **Add a trailing `*` to every
inflectable item** (`show*`, `suggest*`, `prove*`) — without it `show` misses `showed` and
the diagnosis falsely reports zero.

The script lives in this skill's own `scripts/` directory — **use its absolute path**, not
a relative one; the working directory is the user's project, not the skill folder.

```bash
Q="<skills-dir>/meta-styling/scripts/quant_check.py"
py -3.10 "$Q" profile draft.txt
py -3.10 "$Q" count --items profile_vocab.txt draft.txt
```

Record, per item: hits, and — for reporting verbs — **which lane the draft used it in**
(literature / own inference / display item). The lane, not the count, is the finding.

**Artifact `1b-vocab.tsv`** (≤ 30 rows) — keep items with a hit or a lane violation.

### 1c — Absence check

Count every Red-Flag term from `card.md`. **Artifact `1c-absence.tsv`** (≤ 30 rows) —
hits only, never the zero rows.

---

## Stage 2 — Compare (one worker per reference paper)

Reads `1a-structure.md` plus that paper's `logic.md` and `style-vocab.md`. **This is the
only stage that opens a large file, and nothing large leaves it.**

Emit exactly these eight dimensions, in this order, each `MATCH` / `MISMATCH` / `n/a`
with one concrete observation on a mismatch.

| # | dimension | source on the reference side |
|---|-----------|------------------------------|
| D1 | paragraph-function spine | `logic.md` §C |
| D2 | paragraph closers — what the last sentence of each paragraph does | `logic.md` §C, §F |
| D3 | sentence-role chains | `logic.md` §D |
| D4 | frame-code distribution for that section | `logic.md` §F |
| D5 | gap type (I / D only) — which C-codes the reference uses and never uses | `logic.md` §E, §F |
| D6 | reporting-verb lanes | `style-vocab.md` §C.1 |
| D7 | hedge & qualification placement | `style-vocab.md` §C.2, `logic.md` §F |
| D8 | absences | `1c-absence.tsv` |

**Artifact `2-diff.<slug>.md`** (≤ 90 lines). All eight dimensions always appear, each with
its verdict. **On overflow, compress prose — never drop a `[P#-S#]` address, a verbatim
quote, or a whole dimension.**

> The earlier bound was 30 lines with the instruction "keep only the strongest observation
> per dimension". Measured on a live run, the useful artifact came out at 80 lines and
> every line carried an address, a quote or a role chain. Following the old rule would have
> deleted exactly the content that made the diff actionable. A bound that degrades the
> artifact is worse than no bound.

```markdown
section: M   reference: kim-2015-nitrate-iso

D1 paragraph-function spine   MISMATCH
   draft:     [Procedure, Procedure, Claim]
   reference: 13 ¶; 2 close on a procedural DECISION
D2 paragraph closers          MISMATCH
   draft closes on Method, Method, hedged Claim — no decision anywhere
D3 sentence-role chains       MISMATCH
   draft P2:      Method → Method
   reference P19: Method → Condition → Method → Method+Purpose → Decision+Qualification
   missing: Condition, Qualification
D4 frame-code distribution    MISMATCH
   draft E×2 F×1 Z×2  |  reference M: E×23 Z×19 A×4 F×2  → E under-used
D5 gap type                   n/a (Methods)
D6 reporting-verb lanes       MATCH   draft `indicate` governs own inference — correct lane
D7 hedge placement            MISMATCH
   draft 0 clause-final riders | reference 5 Assumption-Riders, all clause-final
D8 absences                   MISMATCH — 11 hits (see 1c-absence.tsv)
```

---

## Stage 3 — Prescribe (barrier)

Reads every `2-diff.*`, `1b-vocab.tsv`, `1c-absence.tsv`. Nothing large.

### Partition

| class | rule | tier gate |
|-------|------|-----------|
| **FIRM** | absences / Red Flags | N=1: applies. N=2: needs 0 in **both** cards. N≥3: convergent, cite the count |
| **BAND** | numeric sanity targets | same at every tier |
| **CHOICE** | structural and stance habits from D1–D3, D7 | the candidate axis at every tier |

**A Red Flag that fails its tier gate is demoted to CHOICE, never dropped.** If one card
records an absence at 0 and another does not, the absence is that paper's habit, not a
corpus norm — move it to the candidate axis and name both sides in the report.

This is not hypothetical. On the two-paper corpus measured so far, four Red Flags carried
firm by the 2015 card did **not** survive the 2024 card: `whereas` (0 → 5), a future-work
close (0 → 4 ¶), a standalone Limitations section (absent → present), and roadmap/signpost
sentences (absent → 3). At N=1 all four would have been imposed on a draft as rules.

At N≥3 a dimension classified `divergence` (spread rule below) adds a second axis: a
low-lean and a high-lean variant of the same candidate.

### Band derivation — two steps, in this order

**Step 1, base band:**

| N | base band | label |
|---|-----------|-------|
| 1 | card's point value **for that section**, ±20% | `soft` |
| ≥2 | `[min, max]` if `relative_spread ≤ 0.30` or absolute gap `< 2.0/1k` | `firm` |
| ≥2 | otherwise → no target; record the spread | `divergence` |

`relative_spread = (max − min) / ((max + min) / 2)`

**Step 2, length widening (REQUIRED before the band is written anywhere):**

| draft tokens | effective band |
|--------------|----------------|
| ≥ 300 | base band unchanged |
| < 300 | base band widened a further ±20% |
| < 100 | no numeric check at all |

Derive the effective band **once, here**, and reuse it in Stage 5. Re-deriving a narrower
band at verification manufactures a failure that isn't there — measured: a 112-token draft
at `avg_sent_len 22.4` reads as failing the base band 26.5–39.7 when its effective band is
21.2–47.7.

**Never average. Never mix sections. Never use a whole-paper figure.**

### Rules

- **No prescription may cite a metric gap as its sole justification.** Every one names a
  D1–D8 dimension or an absence.
- Every prescription = original fragment + issue + evidence + proposed revision.
- Assign each prescription an id: `F1…` (firm), `B1…` (band), `C1…` (choice).

**Artifact `3-prescriptions.md`** (≤ 110 lines; merge prescriptions sharing a fix, never
drop a FIRM item):

```markdown
tier: single-source   N: 1   cards: [kim-2015-nitrate-iso]   section: M

## FIRM — every candidate
F1  D8  "Figure 2" → "Fig. 2"                    card Red flag #5 (Fig. 31 : Figure 0)
F2  D8  bulleted list → inline (1); (2); and (3) card Red flag #6
F3  D8  remove "This paper is organized as follows"  card Red flag #2

## BAND — every candidate (sanity only)
B1  passive/1k  6.5 → 13.6–30.7 effective   manifest M row 21.3, widened (<300 tok)

## CHOICE — candidate axis
C1  D2  close the paragraph on a procedural decision   reference: 2 of 13 M ¶
C2  D7  move the assumption to a clause-final rider    reference: 5, all clause-final
C3  D3  insert a Condition sentence before the method   reference chain P19
```

### The same artifact at N=2

At two or more cards the header changes, BAND rows carry a verdict from the spread rule,
and CHOICE gains items that were FIRM at N=1. Real values from the `SCI_kkh` corpus,
Methods section:

```markdown
tier: provisional   N: 2   cards: [kim-2015-nitrate-iso, kim-2024-redox-leachate]   section: M

## FIRM — every candidate (0 in BOTH cards)
F1  D8  "Figure 2" → "Fig. 2"              Fig.:Figure = 31:0 and 30:0
F2  D8  remove attitude markers            0 and 0
F3  D8  no bulleted list in the body       0 and 0
F4  D8  no citation in the Conclusions     0 and 0

## BAND — every candidate (sanity only)
B1  avg_sent_len  [25.3, 33.1]  spread 0.267  FIRM
B2  passive/1k    [21.3, 22.2]  spread 0.041  FIRM
B3  hedges/1k     8.9 vs 2.7    spread 1.069  DIVERGENCE — no target; see C4

## CHOICE — candidate axis
C1  D2  close the paragraph on a procedural decision   2015 only; 2024 uses a semicolon form
C2  D7  clause-final assumption rider                  2015: 5; 2024: 1
C3  D8  `whereas`                                      2015: 0 (was a Red Flag) | 2024: 5
C4  B3  hedging density                                low-lean (2.7) or high-lean (8.9)
```

Note `C3`: an item the 2015 card carried as a firm Red Flag, demoted to a choice because
the second card contradicts it. Note `C4`: a divergent BAND row becomes a candidate axis
rather than a target — this is where the low/high variants of candidate B come from.

---

## Stage 4 — Generate candidates (one worker each)

Each worker reads the draft and **its own prescription subset only**.

| id | applies |
|----|---------|
| A conservative | FIRM + BAND |
| B standard | A + the CHOICE items natural to that section |
| C deep | B + sentence-role chain rearrangement (D3) |

Maximum 3. Fewer when the diagnosis supports fewer; if there are no CHOICE mismatches,
emit A alone and say the draft already matches structurally. **Never pad to three.**

> **Do not read reference files in this stage.** Every finding is already translated into
> a prescription. Re-reading the source produces verbatim copying — and on the papers
> measured so far 98.2% and 98.7% of anchors are Singletons, so there is essentially no
> wording to copy, only frame types and their positions. Check the paper's own
> `manifest.frames.singleton_rate` rather than assuming.

**Constraints for every candidate:**

- Never alter claims, data values, citations, or the logical order of arguments.
- **Claim precedence**: claim *strength* is style (hedging "proves" down to "suggests" is
  allowed and often required); claim *direction* is content. A prescription that would
  reverse the draft's assertion is flagged as content-tension and **not applied**.
- **Singleton constraint**: a frame marked `Singleton` in `anchors.txt` appears at most
  once per candidate, as its author used it. If Singleton status was not loaded, fall back
  to the card's aggregate ratio and **say that the fallback was used**.

**Artifact `4-candidate.<id>.md`** — the revised text plus the prescription ids applied.

**Emit one file per candidate, including an empty candidate A.** When A applies nothing,
the file still exists and says so:

```markdown
applied: (none — 0 FIRM prescriptions; BAND alone is not grounds for a rewrite)
---
(unchanged from the draft)
```

Without it the comparison table cannot be reproduced from disk, and Stage 4b has nothing
to run the content-preservation gate against.

---

## Stage 4b — Compare and recommend (barrier)

### Filename check — runs first

The artifact names below are a **literal contract**, not a suggestion. Verify every file
exists under its exact name before comparing anything:

```
0-draft.repr.md   0-draft.prose.txt   profile_vocab.txt
1a-structure.md   1b-vocab.tsv        1c-absence.tsv
2-diff.<slug>.md  3-prescriptions.md
4-candidate.<id>.md   4b-comparison.md   5-verify.tsv
```

A name that drifts (`cand_B.txt` for `4-candidate.B.md`) **silently breaks re-entry**: a
later run looking for the contract name finds nothing and redoes the stage. Observed on a
live run — the artifacts existed and re-entry was broken anyway.

### Content-preservation gate

A prescription of the form "remove X" or "replace X with Y" can be satisfied by deleting
the sentence that contained X. That is content loss wearing a style fix, and the
Red-Flag count does not catch it — the flag is gone either way.

Measured: on the test draft, prescription `F1 "Figure 2" → "Fig. 2"` produced a candidate
with **no figure reference at all**. Red-Flag hits read 0 and the candidate looked clean.

So check these multisets, draft vs candidate. Each must be **preserved or transformed,
never smaller**:

```bash
# display-item references
grep -oE '\b(Fig\.|Figure|Table|Eq\.|Equation)\s*[0-9]+[A-Za-z]?' draft.txt | sort | uniq -c
# citation keys
grep -oE '\([A-Z][^()]{0,80}[0-9]{4}[a-z]?\)|[A-Z][a-z]+(?: et al\.)? \([0-9]{4}' draft.txt
# numerals (data values)
grep -oE '[0-9]+\.?[0-9]*' draft.txt | sort | uniq -c
```

| result | action |
|--------|--------|
| count preserved, form changed (`Figure 2` → `Fig. 2`) | correct — the prescription was applied |
| count reduced | **disqualify the candidate**; regenerate it with the item restored |
| numeral changed | **stop** — a data value was altered, which is never permitted |

A candidate that fails this gate is not reported as an option, even if every other
measure is good.

### Comparison

Measure every candidate. **Artifact `4b-comparison.md`** (≤ 35 lines; table only):

```markdown
| id | applied | avg_sent_len | hedges/1k | passive/1k | Red-Flag hits |
|----|---------|--------------|-----------|------------|---------------|
| A  | F1-F3, B1        | 24.1 | 9.8  | 19.4 | 0 |
| B  | + C1, C2         | 27.6 | 8.9  | 23.1 | 0 |
| C  | + C3             | 29.0 | 8.4  | 24.8 | 0 |
recommend: B — reason tied to a specific diagnosis line
```

The recommendation must cite a diagnosis line, not an impression. "It reads better" is not
a reason; "your draft already had a decision sentence buried mid-paragraph, and promoting
it to the closer costs nothing and is this author's most consistent habit (D2)" is.

---

## Stage 5 — Verify (sanity only)

Re-measure the recommended candidate against the **same effective band** Stage 3 derived.

**Artifact `5-verify.tsv`** (≤ 12 rows). Out of band is a **warning**, surfaced to the
author — it never triggers an automatic rewrite. There is no corrective loop in v4.0:
numbers are not the target, so a number is not grounds for redoing the work.

---

## Stage 6 — Report

```markdown
## Style Revision Report
**tier**: single-source · **N**: 1 · **cards**: kim-2015-nitrate-iso · **section**: Methods
> Numbers are a sanity check, not the target.

### A. Structural diagnosis
[the D1–D8 table, mismatches first]

### B. Candidates
[4b-comparison.md table]

### C. Recommended revision (B)
[full text, with the reason]

### D. The other candidates — differences only
A: keeps "…" instead of "…"     C: additionally rewrites P2 as …
(never reprint a full paragraph three times)

### E. Not imposed
N=1  → "합의 판정 불가 (N=1). 아래는 이 논문 한 편의 선택이며 학술 규범이 아님."
        then every CHOICE item candidate A omitted, with the card's value.
N=2  → same, labelled provisional.
N≥3  → divergence list: dimension, each paper's side, which lean was kept.

### F. Verification (sanity)
[5-verify.tsv]

### G. Optional next steps
- Argument soundness → meta-review
- AI-trace removal → meta-rewriting-antiai
- Raise confidence: extract more reference papers → extraction-style
(mention only; do not run)
```

**Write the report in the user's language.** The draft and the corpus are English; the
report is for the person reading it. The template's headings are labels, not required
wording.

**Section E is never empty.** At N=1 it carries the honesty of the whole report — it is
where the reader learns which of the card's habits were deliberately *not* imposed.

---

## Section mapping

The reference's `manifest.prep.section_scheme` may not contain the draft's section. An
`IMRC` corpus fuses Results and Discussion, so a Discussion draft has no `D` row.

1. Exact match → use it.
2. **Fused-section match**: if `prep.detection_notes` records the fusion (e.g. "R and D
   appear fused"), use the fused section and **declare the substitution in the report
   header**. Legitimate — that `R` genuinely contains discussion prose.
3. No match, no fusion note → do not substitute another section's band or spine. Say which
   sections the corpus covers and run D6–D8 only.

Rule 2 is the only permitted cross-section substitution, and only on evidence `prep.py`
already recorded. **Never infer fusion from the content.**

---

## Not supported

**Korean drafts and Korean corpora.** Stop and point to `meta-mywriting-korean` or
`meta-report-writing`. The frame taxonomy, paragraph-function tags, and sentence-role list
are all derived from English academic prose; applied to Korean they produce tags that look
authoritative and mean nothing. The v3.0 experimental Korean path was removed rather than
carried forward — a half-working path that labels itself experimental still gets used.

---

**Guide Version**: 4.0.0
**Design spec**: `../docs/2026-08-17-v4-design.md`
