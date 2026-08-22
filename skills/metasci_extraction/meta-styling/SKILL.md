---
name: meta-styling
description: |
  Use when an academic draft in English — a paragraph, section, or report chapter, including
  a bilingual working document whose manuscript prose is English — must be revised to match
  reference papers whose style has already been extracted into an extraction-style
  corpus. Triggers: "문체 교정", "스타일 맞춰줘", "톤 맞춰줘",
  "스타일 적용", "이 카드로 고쳐줘", "style revision", "apply style card",
  draft + style corpus given. NOT for style extraction ("스타일 추출" →
  extraction-style), NOT for argument soundness ("논리 검토" → meta-review),
  NOT for AI-trace removal (→ meta-rewriting-antiai), NOT for Korean drafts
  (→ meta-rewriting-korean).
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion, Agent]
---

# Meta-Styling Skill (v4.0 — representation matching)

## Overview

Revises a draft to match an extracted style corpus by **comparing structural
representations**, not by steering three numbers.

**The core principle: match the representation, not the metric.**

The reference is already tagged — `logic.md` records every paragraph's function and
relation, every sentence's role and frame code. v4.0 tags the draft the same way and
diffs the two. Prescriptions come from that diff. Numbers are a sanity check at the end.

**Why this replaced v3.0.** `extraction-style` instructs every card to carry the
rule *"Numbers diagnose; they do not set targets — never a value a draft should be edited
toward."* v3.0 edited toward them. Measured consequence on a test draft: v3.0 returned
`ALL DIMENSIONS IN BAND` on a revision that contained **none** of the five distinctive
moves the card had recorded for that author. A verifier that passes text carrying none of
the target style is worse than no verifier. Full evidence: `docs/2026-08-17-v4-design.md`.

**Second principle: confidence scales with N.** One reference paper cannot separate a
*norm* from that author's *personal choice*. The skill counts its cards and gates
prescriptions accordingly. A single card never becomes a rule set.

**Verification status.** Parts of this design are measured and parts have never run.
`docs/2026-08-17-v4-design.md` §15 records which is which, and notes one caveat that
qualifies the headline numbers. Read it before treating any single finding as settled.

**Third principle: propose, don't decide.** Structural habits are offered as 2–3 candidate
revisions with a recommendation, not imposed as one answer.

### Division of labor (this skill is the CONSUMER)

| Job | Skill |
|-----|-------|
| Extract style from reference papers | `extraction-style` (builds the corpus) |
| **Match a draft's structure to a corpus** | **meta-styling (this skill)** |
| Judge whether the argument is *sound* | `meta-review` |
| Decide section order / outline | `meta-writing-mapping` |
| Remove AI-writing traces afterwards | `meta-rewriting-antiai` (never auto-chained) |
| Korean academic / institutional register | `meta-rewriting-korean` |

This skill asks only: **does this draft's structure match this reference's structure?**
It does not ask whether the argument is good.

---

## Input Contract

**Required:**

1. **Draft** + its section type — Introduction / Methods / Results / Discussion /
   Conclusions, or report chapter.

   The draft is often a **working document**, not clean prose: an approach checklist, a
   source summary, drafting notes, ledgers, open-question lists and a translation mirror
   around the manuscript itself. Stage 0.1 separates the two; only manuscript prose is
   measured, tagged, compared or revised.

   If the draft carries **its own style rules**, they are a competing authority and
   **they win** over the corpus. Stage 0.3 governs how conflicts are handled — they are
   surfaced as choices, never resolved silently.
2. **Corpus root** — a `extraction-style` v3.x folder:

```
<corpus-root>/
├── style_profile.md            (optional cache)
└── papers/<slug>/
    ├── card.md                 selected findings + Red Flags
    ├── logic.md                paragraph functions, sentence roles, frames  ← primary input
    ├── style-vocab.md          measured lexicon by section
    ├── anchors.txt             Singleton/Recurrent status
    └── manifest.json           measured rows (sanity check only)
```

Resolve in this order: the path the user gave → a folder matching `*style*corpus*` or
`Style_*` at or under the working directory → ask.

**If resolution turns up more than one corpus** — several matching folders, or a
user-given path that is a *parent* holding several collections — never pick one silently.
List what was found and ask which to use. Corpora are not interchangeable: one may hold
the author's own papers, another a target journal's, and revising toward the wrong
identity is a category error the structural diff cannot catch. A folder of raw PDFs with
no `papers/<slug>/card.md` underneath is not a corpus — name it as unextracted and offer
`extraction-style`, but never block on it when an extracted corpus is also present.
Corpora are mixed only when the user asks for it (Pick-list mixing, N≥2).

**Then count N** = `papers/<slug>/card.md` files in scope (all, or the subset the user
named). **Announce N, the tier, and the slugs before Stage 1.**

**Optional:** specific slugs · candidate set override · Pick-list source mixing (N≥2).

**`style_profile.md` is an optional cache, never a requirement.** Use it only when it
exists *and* is newer than every card in scope; otherwise ignore it and say so in one
line. A stale profile is worse than none. **Never tell a user who has cards to go run
`extraction-style`.**

**Legacy:** `Style_{destination}/style_profile.md` + `cards/*_style.md` still read. A v1.x
24-table data bank does not — explain the supersession and offer re-extraction.

**Korean is not supported** — but check the **extracted manuscript prose**, never the raw
file. A bilingual working document whose English prose is the manuscript is in scope; a
draft whose prose is Korean is not, and goes to `meta-rewriting-korean`. Measured: a live draft returned `lang: ko` on the raw file and `en`
on its prose, because 43% of the *file* was Korean scaffolding. Checking the raw file
aborts runs this skill is built for.

---

## Confidence Tiers

| N | Tier | Applied to every candidate | Varies between candidates |
|---|------|---------------------------|--------------------------|
| **1** | `single-source` | absences only (Red Flags) | every structural habit |
| **2** | `provisional` | absences confirmed in both cards | structural habits, labelled provisional |
| **≥3** | `corpus` | convergent items, cited with count (`4/4`) | divergent dimensions split into low/high variants |

**Why absences are firm even at N=1.** A measured zero is different evidence from a
measured rate. "This author never writes `whereas` in 8,160 tokens" is established by one
paper. "This author hedges at 16.9/1k" is a choice that paper made; a second paper by the
same author may sit at 2.6. **Absence generalizes; magnitude does not.**

---

## Pipeline

Every stage writes a small artifact next to the draft and reads only artifacts, never
sources. The main conversation never holds `logic.md`.

```
<draft-dir>/run/<draft-stem>/
   0-draft.repr.md   0-draft.prose.txt   profile_vocab.txt
   1a-structure.md   1b-vocab.tsv        1c-absence.tsv
   2-diff.<slug>.md  3-prescriptions.md
   4-candidate.<id>.md   4b-comparison.md   5-verify.tsv
```

**These filenames are a literal contract.** Re-entry resolves stages by name, so a drifted
name (`cand_B.txt`) breaks it even though the work was done. Stage 4b checks them.

| stage | parallel | reads | writes |
|-------|----------|-------|--------|
| 0 separate/check/segment | — | draft | `0-draft.repr.md`, `0-draft.prose.txt` |
| 1a structure tag | ✔ | **draft only** | `1a-structure.md` |
| 1b vocab measure | ✔ | draft + `card.md` §V | `1b-vocab.tsv` |
| 1c absence check | ✔ | draft + Red Flags | `1c-absence.tsv` |
| 2 compare | ✔ per paper | `1a` + that paper's `logic.md`, `style-vocab.md` | `2-diff.<slug>.md` |
| 3 prescribe | barrier | all `2-diff.*`, `1b`, `1c` | `3-prescriptions.md` |
| 4 generate | ✔ per candidate | draft + its prescription subset | `4-candidate.<id>.md` |
| 4b recommend | barrier | all candidates | `4b-comparison.md` |
| 5 verify | — | recommended candidate | `5-verify.tsv` |
| 6 report | — | `3`, `4b`, `5` | chat |

**Two isolation rules that are not optional:**

- **Stage 1a must not see the reference.** Tagging a draft against a known target biases
  the tags toward it and manufactures a match. Tag blind, then compare.
- **Stage 4 workers must not read reference files.** Every finding is already translated
  into a prescription; re-reading the source produces verbatim copying, which the
  Singleton finding forbids.

Parallel stages are dispatched as isolated workers when subagent dispatch is available and
the user has agreed to it. Otherwise they run sequentially in the same order; the context
benefit survives, because every stage reads and writes files.

**But parallelism is not only a speed property.** Worker separation is what *enforces* the
two isolation rules above — a worker that was never handed `logic.md` cannot read it. Run
sequentially and both rules become honor-system, which for Stage 1a is not something a
single context can honestly keep: once it has read the reference, "tagging blind" is no
longer available to it.

When running sequentially, mitigate and disclose:

- **Stage 1a**: tag the draft **before opening any reference file**. Ordering substitutes
  for separation, imperfectly.
- **Stage 4**: work from `3-prescriptions.md` alone and do not re-open the reference.
- **Report it**: add one line to the report header — *isolation by ordering, not by worker
  separation* — so the reader knows how much the structural diff is worth.

Each stage is a pure function of its declared inputs, so re-entry is cheap: deleting
`3-prescriptions.md` rebuilds stages 3+ only; adding a reference paper needs that paper's
Stage 2 plus 3+; changing the draft invalidates everything.

---

## Candidates

Prescriptions partition into three classes. Only the third varies.

| class | varies? |
|-------|---------|
| **FIRM** — absences / Red Flags | no — in every candidate |
| **BAND** — numeric sanity targets | no — same for all |
| **CHOICE** — structural and stance habits | **yes — this is the axis** |

| id | contents | intent |
|----|----------|--------|
| **A** conservative | FIRM + BAND only | preserve the author's own voice |
| **B** standard | A + CHOICE items natural to that section | adopt the reference's signature moves |
| **C** deep | B + sentence-role chain rearrangement | restructure the paragraph's internal logic |

Maximum **3**; fewer when the diagnosis supports fewer. If there are no CHOICE
mismatches, emit A alone and say the draft already matches structurally. **Never pad to
three** — more candidates transfer the decision back to the user instead of helping.

A/B/C replace v3.0's Light/Standard/Deep: intensity is now defined by *which diagnosed
items were applied*, which is auditable.

---

## Numbers, demoted

Bands are still derived (N-tier point ±20% at N=1; min–max with the spread rule at N≥2;
widened a further ±20% under 300 draft tokens — see `references/revision_guide.md`). Their
only job is catching a revision that drifted implausibly far from the reference's register.

- Out of band is a **warning**, never an automatic rewrite trigger.
- **No prescription may cite a metric gap as its sole justification.** Every prescription
  cites a comparison dimension (D1–D8) or an absence.
- The report states verbatim: *"Numbers are a sanity check, not the target."*

Compare a draft section against its own section row only. Section `A` (front
matter/abstract) is never a band.

---

## Quality Criteria

1. **Representation first** — every prescription traces to a D1–D8 dimension or an absence.
2. **N is declared** — tier, N, and slugs in the report header.
3. **Candidates, not a verdict** — 2–3 revisions with a reasoned recommendation.
4. **Content preserved** — claims, data, citations untouched. Claim *strength* is style;
   claim *direction* is content. A prescription that would reverse the draft's assertion is
   flagged as content-tension, never applied.
5. **Singletons stay singular** — a frame marked Singleton appears at most once per draft.
6. **Honest reporting** — what was deliberately not imposed is listed, never omitted.

---

## Error Handling

| Situation | Response |
|-----------|----------|
| No corpus found | Ask for the path; hand off to `extraction-style` only if none exists |
| No `style_profile.md` | **Normal.** Derive from cards; one line saying so. Never block |
| `style_profile.md` stale | Ignore, warn once, derive from cards |
| Draft's section absent from the corpus scheme | See `revision_guide.md` §Section mapping — fused R+D is the common case, not an error |
| Draft <100 tokens | Skip structural tagging and verification; run absences and lane checks only, and say so |
| `logic.md` missing from a paper folder | That paper contributes lane/absence checks only; record it, never drop it silently |
| No CHOICE mismatches | Emit candidate A alone and say the draft already matches |
| Korean draft or corpus | Stop; point to `meta-rewriting-korean` |
| A prescription would reverse a claim | Flag as content-tension; do not apply |

---

## Usage Examples

```
# N=1 — one card
> "내 Methods 초고를 style_corpus의 kim-2015 카드로 교정해줘"

# N=4 — whole corpus; divergences become candidate axes
> "이 초고를 style_corpus 전체(4편)에 맞춰줘"

# Subset
> "kim-2015랑 kkh-redox 두 장만 써서 Discussion 고쳐줘"

# Ask for the conservative candidate only
> "빨간 깃발만 잡아줘, 구조는 건드리지 말고"
```

---

**Version**: 4.1.1 (Korean routing → meta-rewriting-korean; the skills it replaced are retired)
**Previous**: 4.1.0 (frame-code taxonomy bundled as `references/frame-codes.md` so Stage 1a
runs without `extraction-style` installed; multi-corpus resolution made explicit — multiple
hits are listed and asked, never silently picked)
**Previous**: 4.0.0 (representation matching replaces metric matching; staged file-backed
pipeline with parallel branches; multi-candidate output with recommendation; numbers
demoted to a sanity check; Korean removed)
**Design spec**: `docs/2026-08-17-v4-design.md`
**Consumes**: `extraction-style` v3.x corpus
**Skill**: Meta_researcher / meta-styling
