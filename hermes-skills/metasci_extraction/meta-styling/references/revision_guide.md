# Style Revision Guide (meta-styling v2.0)

Procedure for applying a `metasci-style-extraction` profile to a draft.
Read this whole file before Phase 1.

---

## Phase 1: Input Analysis

1. Confirm: draft text, its section type, profile folder, intensity
   (Light / Standard / Deep; default Standard).
2. Read `Style_{destination}/style_profile.md`. Note:
   - **Convergence** items → these become firm rules.
   - **Divergence** items → these are choice dimensions (Phase 3 policy).
   - **Red Flags** → patterns absent across the reference corpus; remove from draft.
   - **Section Guidance** for the draft's section.
3. **Always read the cards** — Phase 2's vocabulary check needs the V items (with
   measured freqs) that live only in the cards. Pick-list naming changes nothing
   about reading; it only makes the named card's values OVERRIDE the profile for
   the named dimensions.
4. Save the draft to a temp `.txt` for measurement (or use the file as given if
   it already is plain text).

## Phase 2: Measured Diagnosis

Run (script lives in this skill's `scripts/`; use its absolute path):

```bash
python scripts/quant_check.py profile draft.txt
# lang, tokens, sentences, avg_sent_len, hedges_per_1k, passive_per_1k
```

For profile vocabulary, check what the draft already uses. Build
`profile_vocab.txt` from: the cards' V reporting verbs + hedging words + stance/
transition markers, PLUS the profile's Red-Flag terms (to measure what must go).
**Add a trailing `*` to every verb/inflectable item** (`show*`, `suggest*`,
`prove*`) — without it, `show` will not match `showed` and the diagnosis will
falsely report zero usage:

```bash
python scripts/quant_check.py count --items profile_vocab.txt draft.txt
```

**Output — Diagnosis table (measured rows first):**

```markdown
### Measured Diagnosis
| dim | draft (measured) | target (profile) | verdict |
|-----|-----------------|------------------|---------|
| hedges/1k | 4.2 | 11-13 (profile: 12.1) | LOW — hedging to add |
| avg sentence length | 31.8 | 24-27 | HIGH — split long sentences |
| passive/1k | 22.0 | 13-16 | HIGH — activize where natural |
| profile reporting verbs used | show (2) only | suggest/observe/demonstrate families | NARROW |

### Qualitative Diagnosis (reading judgment)
| dim | draft | target | verdict |
|-----|-------|--------|---------|
| tense (this section) | mixed | past (4/4 convergence) | fix |
| citation integration | integral-heavy | non-integral ~90% | shift |
| Red-Flag patterns present | "This paper explores…" | absent in corpus | remove |
```

Rules:
- Target bands come from the profile's measured card values (min–max across
  papers, or the convergence value). Never invent a band.
- A draft under ~100 tokens: skip the measured table (rates unstable at that
  size), diagnose qualitatively, and say so.
- **Short drafts (<300 tokens): report raw hit counts alongside per-1k values**
  ("prove* 3 hits = 24.2/1k") and widen all target bands ±20% — full-paper
  per-1k bands are knife-edge at paragraph length (one hit can be ±8/1k).
- **The measurement wins**: if your reading impression disagrees with a count,
  grep the draft text before overriding the script.

## Phase 3: Prescription

Policy per item type:

| Item type | Policy |
|-----------|--------|
| Convergence rule violated | Prescribe the fix; cite `style_profile.md` line (e.g. "non-integral citation 4/4") |
| Red Flag present in draft | Prescribe removal/replacement |
| Divergence dimension | Determine the draft's existing lean; prescribe consistency in THAT direction only; log as a **choice point**. If the draft has NO lean (e.g. zero hedges on a hedging-density divergence), target the mid-band and log the tie-break as a choice point |
| Measured gap (Phase 2) | Prescribe concrete edits sized to close the gap (e.g. "add hedges to ~5 Discussion claims ≈ +7/1k") |
| Pick-list override | Apply the named card's value for that dimension |

Every prescription = original fragment + issue + evidence (profile/card quote or
measured gap) + proposed revision.

## Phase 4: Revision

- **Light**: vocabulary and fixed expressions only; sentence boundaries untouched.
- **Standard** (default): expressions + sentence-level restructuring (split/merge,
  voice, hedging insertion); paragraph order untouched.
- **Deep**: full stylistic rewrite of the passage; paragraph-internal structure may
  change; content and claim strength ordering must not.
- Never alter: claims, data values, citations (keys/years), logical order of
  arguments (that is meta-review's domain).
- **Claim precedence rule**: claim *strength* is style (hedging "proves" down to
  "suggests" is allowed and often required by Red Flags); claim *direction* is
  content. If a convergence rule would REVERSE what the draft asserts (e.g. draft
  says "no oversight needed", corpus mandates an oversight rider), soften the
  strength, add the rider, AND flag the edit as a content-tension in the report
  for the author to accept or revert.
- Frames marked `Singleton` in cards are one-off moves — use a Singleton at most
  ONCE per draft (as its author did), never as a repeated pattern; `Recurrent`
  frames may be reused freely.

## Phase 5: Post-Revision Verification

Save revised text to a temp `.txt`; re-run `profile` (and `count` if vocabulary
was diagnosed). Report:

```markdown
### Verification (measured)
| dim | before | after | target | status |
|-----|--------|-------|--------|--------|
| hedges/1k | 4.2 | 10.8 | 11-13 | ~ (borderline) |
| avg sentence length | 31.8 | 25.9 | 24-27 | OK |
| passive/1k | 22.0 | 15.1 | 13-16 | OK |
```

- Any dimension outside the band → ONE corrective re-pass targeting only that
  dimension → re-measure once more.
- Still outside → report honestly with the likely reason (e.g. "draft is a
  methods recap; hedging density structurally lower"). No further loops.

## Phase 6: Report Format

```markdown
## Style Revision Report  [Korean mode — experimental]   <- tag only if Korean

### A. Measured Diagnosis
[Phase 2 tables]

### B. Prescriptions & Changes
#### [1] <dimension> — <convergence rule | measured gap | Red Flag>
- Original: "…"
- Evidence: <profile/card citation or measured delta>
- Revised: "…"
[...]

### C. Choice Points (Divergence — draft's lean followed)
- hedging intensity: kept LOW-lean (Lee2020-style); say the word to shift to
  Smith2021-style HIGH.
[...]

### D. Revised Text
[Before] … / [After] … (changes bold)

### E. Verification (measured)
[Phase 5 table]

### F. Optional next steps
- Logic/argument review → meta-review
- AI-trace removal → meta-rewriting-antiai
(mention only; do not run)
```

---

## Korean drafts (EXPERIMENTAL)

- Requires a Korean profile (extracted with `lens-korean.md` guidance).
- `quant_check.py` auto-detects Korean: eojeol tokens, ending-based sentence
  split, Korean hedging inventory (것으로 판단된다, 수 있다, 가능성 …),
  되다/어지다 passive approximation. Treat measured Korean values as
  approximate; bands ±20%.
- Additional Korean qualitative dims: 종결어미 registers (…다 / …함 / …음 명사형
  종결), 격식체 일관성, 한자어/고유어 균형. Judge these by reading, against the
  Korean profile's P values.
- Label the report `[Korean mode — experimental]`.

---

**Guide Version**: 2.0.0
