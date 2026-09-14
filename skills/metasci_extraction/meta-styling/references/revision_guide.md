# Style Revision Guide

Guide version: 5.0.0 (2026-09-14).

Paired entrypoint: `meta-styling` SKILL.md 5.0.0. Do not use this guide with the 4.1.1 entrypoint: its candidate, tier, band, and stage-file rules no longer apply.

Apply useful features of the selected style corpus to an English draft while preserving its substance. Compare both wording and structure. A difference from a reference is an observation; decide whether it is relevant before turning it into an edit.

Use this guide for the revision workflow. Consult the frame taxonomy only when classifying sentence frames, and the quantitative helper only when a measurement would resolve a useful question. Development history is not required reading.

## 1. Establish the input and working text

Identify the requested draft, section, corpus, and scope from the user's files and conversation. Honor a selected paragraph, section, or subset of reference papers. Use neighboring prose to interpret the target without expanding the revision scope.

The corpus is an existing input. Do not rebuild it as part of styling. Resolve a supplied corpus path first; otherwise look for a recognizable style corpus in the project. If several plausible corpora remain, ask which to use. If none is available, request its location. If the user has not built one, explain that `extraction-style` creates it from reference papers; do not silently substitute another collection or start extraction.

### Prepare the workspace before writing files

Create `<draft-dir>/run/<draft-stem>/<run-id>/` before extracting the prose. Use `YYYYMMDD-HHMMSS` as the run ID, adding a suffix if that directory already exists. For pasted text, use a descriptive draft name in the current project. A changed draft, corpus selection, or scope starts a new run. Reuse an existing run only for a follow-up to that same recorded input.

Write `0-draft.prose.txt` containing only the manuscript prose in scope, preserving its original paragraph breaks, values, citations, and wording. Keep the supplied draft unchanged.

Exclude working rules, evidence summaries, drafting notes, unresolved author questions, ledgers, and parallel translations from the text being measured or revised. Keep them available as context. If a bracketed phrase might be intended manuscript content rather than a note, do not silently discard it.

Check the extracted prose by reading it; use the helper's `profile` language result as a diagnostic if uncertain. Never run that check on the raw working document: a recorded live run returned `ko` because Korean notes and a translation mirror surrounded an entirely English manuscript. An English manuscript with Korean notes is in scope. For prose intended to remain Korean, use `meta-rewriting-korean`. Translation into English is a separate request; do not silently turn styling into translation.

### Record the scope and applicable rules

Use `review-notes.md` for a compact working record:

- Draft source, target section, and included paragraphs; excluded material with source locations when available.
- Corpus path, selected paper slugs, and the number of papers actually used.
- Relevant author rules and any conflict with a corpus observation.
- Material context limits, missing corpus files, and any section substitution.

The user's current instructions and explicit manuscript requirements govern stylistic choices. Keep a corpus habit that conflicts with them as an unapplied observation, not an edit silently included in a candidate. Treat cited support for a manuscript rule as unverified unless actually inspected.

Briefly state the scope and selected references before proceeding. Ask only when unresolved ambiguity would materially change the work.

Use this minimum skeleton; add rows as the review proceeds rather than creating a separate file for every intermediate step:

```markdown
# Review notes
run: <run-id>
draft: <source path>; section: <section>; scope: <paragraphs>
corpus: <path>; N: <papers used>; papers: <full slugs>
excluded: <material and source locations, or none>
author rules: <applicable rules, or none>
analysis: <independent context / isolation by ordering / informed follow-up>
section mapping: <exact / explicit fusion evidence / unresolved>

## Draft map
P1: <function>; next: <relation>
P1-S1: <role>; frame: <code, when used>

## Evidence and decisions
EDIT-1: <draft location and wording>
Reference: <slug, file section, source address, example>
Observation: <difference and its scope>
Decision: <apply / retain / unresolved>; reason: <applicability>
Change: <before -> after>; preserve: <content boundary>

## Preservation
Mechanical: <PASS / FAIL / BLOCKED>; inventory and exceptions: <details>
Semantic: <PASS / FAIL / BLOCKED>; checked relationships: <details>
Unapplied or unresolved: <items, or none>
```

## 2. Understand the draft independently

Before opening reference prose, frames, or style findings, identify what the draft is doing. Assess all paragraphs in the target, including each paragraph's function and its connection to adjacent text. For paragraph-level work, examine every sentence; for a long section, record sentence-level detail where it informs a comparison or proposed edit. Review all revised text at completion regardless of how much tagging was recorded.

Use `P1…Pn` for draft paragraphs and `S1…Sn` within each paragraph. Qualify reference addresses with the full paper slug, for example `kim-2015-nitrate-iso:P19-S3`, so they cannot be confused with draft addresses. Declare any slug abbreviations in the notes before using them.

### Tag functions without forcing a fit

Start with the shared vocabulary from `extraction-style`'s `lens-architecture.md` §§A.2–A.3, reproduced here so that skill need not be installed:

| Level | Shared labels |
|---|---|
| Introduction paragraphs | Background, Literature-Review, Gap, Question, Purpose, Scope, Contribution |
| Methods paragraphs | Study-Area, Design, Sample, Procedure, Instrument, Statistical, Quality |
| Results paragraphs | Overview, Finding, Comparison, Trend, Pattern, Anomaly, Summary |
| Discussion paragraphs | Interpretation, Mechanism, Lit-Comparison, Agreement, Disagreement, Limitation, Implication, Future, Conclusion |
| Paragraph relations | Continuation, Contrast, Cause-Effect, Specification, Generalization, Sequence, Concession, Problem-Solution, Evidence-Claim, Question-Answer |
| Sentence roles | Topic, Claim, Evidence, Elaboration, Example, Transition, Qualification, Reference, Method, Conclusion, Bridge |

Common extensions include Decision, Aim, and Signpost for paragraphs, and Condition, Decision, Purpose, and Contribution for sentences. Use a function appropriate to a separate Conclusion or another section rather than forcing it into an unrelated category.

These function and role labels are open-ended. Extend them when a sentence or paragraph has a distinct function; use combinations such as `Decision+Qualification` when warranted. Define an unfamiliar label briefly. An accurate new label is more useful than a forced match.

For sentence **frame codes**, use [frame-codes.md](frame-codes.md). Assign one primary frame code per tagged sentence using its family descriptions and tie-breaking rules. Keep the established codes. For an uncovered shape, record `Z`, a `Capitalized-Hyphenated` provisional name, and one `[SLOT]` template; reconcile names with the corpus during §3, after independent tagging. Extensible function labels and the fixed frame-code namespace serve different purposes. Do not force a high or low `Z` rate.

Record only the structural detail needed to support the comparison. A short draft can still have a meaningful purpose, closer, or reporting-verb use; do not skip qualitative review because it falls below a token threshold.

### Keep the independence claim accurate

When isolated workers are available and their use is authorized, a draft-analysis worker needs the draft, its context and rules, and the taxonomy, but no reference findings. Otherwise perform this analysis before reading the reference findings in the same session.

The default is to tag the draft first. Record whether separation was by independent context or by reading order. The exception is a follow-up revision to a draft already compared: reuse its analysis and disclose that reference findings are known. If a first-pass analyst has already seen the references, do not call the analysis blind; use a fresh context when available and authorized, or disclose the limitation.

## 3. Read relevant corpus evidence and compare

For each selected paper, consult `manifest.json` (`prep.section_scheme`, `prep.detection_notes`, and extraction metadata) and `card.md` for an overview. Follow the section pointers below into `logic.md` and `style-vocab.md`. Inspect headings first if the extraction uses different numbering, then record the corresponding section; do not silently assume a missing heading means a missing feature.

Use the corresponding `sections/*.txt` for lexical counts and their denominators. Use `body.txt` only to verify a quotation or recover its context: it includes abstract/front matter and is not a substitute for the section counting basis.

When authorized isolated workers are used, give each reference-comparison worker the draft map, draft prose, author rules, and draft vocabulary/absence observations from `review-notes.md`, plus its paper's corpus files. It reads the indicated sections and returns compact observations and source evidence, not adoption decisions or whole files. Each observation identifies its paper, section/address, measured scope, and any missing evidence. Decide whether to apply a change only in §4, after combining the selected papers; a zero count in one paper cannot overrule occurrences in another. Without workers, read those same sections sequentially; avoid loading a large `logic.md` or `body.txt` in full. Record the execution method. Worker use is a context-management choice, not a condition for completing the task.

A card selects findings; it is not a substitute for the supporting passage when an edit depends on a specific use. Treat its Red Flags as observations or inherited recommendations to assess, not as automatically binding rules.

### Match the comparison to the draft's function

Use the corresponding section and, within it, passages performing a comparable job. A complete reference Methods section is not a template that every short Methods paragraph must reproduce.

When manifest metadata documents a combined Results and Discussion section, use that material for the relevant comparison and disclose the substitution. Locate passages doing the matching work where possible; do not treat a mixed section's whole distribution as a pure Discussion norm.

If metadata is absent or unclear, inspect explicit source headings such as “Results and Discussion” and record that evidence. Do not infer fusion from prose content or the section code alone. If no explicit evidence establishes the mapping, omit judgments that require that section match. Missing data is not a measured zero.

An `index.md` or `style_profile.md` may help locate relevant papers. Reuse summary measurements only when their source selection, section, counting basis, and version match the present task. No precomputed band is required.

### Compare structure and vocabulary

Use these dimensions when relevant; there is no requirement to fill an eight-row verdict table for every draft.

| Dimension | Evidence to compare | Question for the revision |
|---|---|---|
| Paragraph functions | Draft map; `logic.md` §C, inter-paragraph logic | Do comparable passages organize the same kind of material differently? |
| Paragraph closers | `logic.md` §§C, F; retrieve the addressed last sentence from §E or section text | Would a reference's way of ending fit what this paragraph actually establishes? |
| Sentence-role chains | Draft roles; `logic.md` §D, intra-paragraph logic | Can existing material be connected or ordered more effectively? |
| Sentence frames | `logic.md` §E, catalog and source examples; §F, distributions and named `Z` shapes | Is a useful frame available for content already present in the draft? |
| Gap presentation | `logic.md` §§E–F, C-family frames in Introduction/Discussion | Can the same actual gap be expressed in the reference's manner? |
| Reporting verbs | Draft uses; `style-vocab.md` §C.1, reporting verbs and their reserved-for table | Are prior findings, current observations, interpretations, and display references expressed appropriately? |
| Other style vocabulary | `style-vocab.md` §C.2 for hedges and the named §C subsections for adverbs, connectives, self-mention, and set phrases; §D for cross-section observations | Does an alternative express the same relationship or stance in the selected style? |
| Presence and absence | `card.md` Red Flags; `logic.md` §§C, F for structure; `style-vocab.md` §§C–D for lexical evidence; scoped draft observations in the notes | Is the difference relevant, and would changing it preserve the paragraph's function? |

For an actionable finding, retain the draft location, reference source and example, the observed difference, and why it matters here. This working evidence is the input to revision; do not leave useful vocabulary findings outside the prescription process.

### Use lexical measurements selectively

Count a word family or phrase when a count would clarify an impression. The helper is `<skill-dir>/scripts/quant_check.py`; resolve its absolute path and use an available Python interpreter (`python`, `python3`, or a suitable Windows `py` launcher). A fixed Python 3.10 installation is not required by this guide.

Run draft measurements on `0-draft.prose.txt`, never on the raw working document, notes, or a candidate file containing metadata. If needed, create `profile_vocab.txt` with the items relevant to the current comparison and use the helper's `count --items` mode. Use `profile` only when broad descriptive measures would help.

For suffix variants, an item such as `show*` can capture `showed` and `shown`. Inspect the matches: wildcards can also capture unrelated forms. Irregular forms need explicit alternatives: `find*` misses `found`. A frequency count does not distinguish a reporting verb from another use of the same word.

Record the function of important occurrences, not just totals. For example, determine whether `show` introduces a figure, an observed result, or an inference. Do not equate every modal or adverb with hedging: capability, statistical significance, magnitude, and uncertainty are different meanings.

Sentence length and word frequencies are descriptive evidence, not quotas. Do not derive mandatory bands, prescribe a hedge count, or edit solely to move a metric toward the corpus. Count or normalize across texts only when the comparison has a compatible basis and is useful at the draft's length.

### Assess structural absences by reading

Separate searchable terms from structural patterns. Lists, a standalone Limitations section, a future-work ending, and citation placement require inspection at the relevant scope. Section-conditioned observations, such as `however` in Methods, require the correct section boundary.

For each relevant absence claim, record what was inspected and distinguish `not observed`, `observed`, and `not assessable`. Do not report a whole-section absence from an isolated paragraph. A roadmap announcing the paper's organization and a local signpost guiding the current argument are separate features.

Record a measured zero with the inspected section, text size, counting method, and matched forms. A verified zero across a substantial inspected passage is strong evidence of absence **in that passage**; an unread file, missing field, or failed search is not evidence of absence. Neither observation alone establishes an author-wide prohibition.

Always report N and the selected papers. For N≤2, label applied structural habits as choices observed in those named papers, not as a general style norm. For larger corpora, identify the supporting papers and any material disagreement; do not label an item corpus-wide if some papers were not assessed for it. Paper count does not automatically turn a habit into a prohibition.

## 4. Decide what to apply

For each useful difference, ask:

1. Does the reference passage perform a comparable function?
2. Can the feature be applied using the draft's existing content and supported meaning?
3. Does it advance the user's requested style while respecting their explicit rules?

Apply the feature only when all three answers are yes. Retain a difference when it follows from the draft's subject, purpose, evidence, or author preference. Mark it unresolved when the needed context is unavailable.

Use the same decision process for vocabulary, frames, gap presentation, and paragraph structure. No comparison dimension is excluded from revision, and no measured absence bypasses the applicability check.

Distinguish:

- **Required constraints:** content preservation, the user's explicit requirements, and applicable confirmed publication rules.
- **Selected style edits:** reference-supported features that fit the present draft.
- **Unapplied or unresolved differences:** features that are unnecessary, incompatible, or insufficiently supported.

Keep decisions in `review-notes.md`. For a substantial revision, assign edit identifiers such as `EDIT-1` and `EDIT-2`; these are separate from frame codes. Each edit records the draft location, reference evidence, proposed change, and any content boundary. Small local revisions need no elaborate prescription table.

Do not create a missing condition, mechanism, limitation, or study decision merely to fill a reference's sentence-role chain. If that information is necessary but absent, identify the gap outside the manuscript text.

### Two edit-record examples

These examples illustrate observations recorded in the SCI_kkh cards (`card.md` of kim-2015-nitrate-iso and kim-2024-redox-leachate). The draft text below is synthetic, not a quotation from either paper. In a live run, confirm the corpus entry and record its actual source address; do not invent an address to complete the template.

```markdown
EDIT-1 — display-reference form
Draft P1-S2: “Figure 2 shows the sampling locations.”
Reference: kim-2015-nitrate-iso and kim-2024-redox-leachate,
           card.md §P display-item form / Red Flags.
Observation: the documented cards favor “Fig.” over “Figure”.
Decision: apply if no user or publication rule requires “Figure”.
Revision: “Fig. 2 shows the sampling locations.”
Preserve: one reference to figure 2 and the same statement about it.
Mechanical result: figure:2 — before 1, after 1.

EDIT-2 — placement of an existing assumption
Draft P2-S1: “Assuming that [ASSUMPTION], [PROCEDURE].”
Reference: kim-2015-nitrate-iso, logic.md §§E–F,
           Assumption-Rider examples with clause-final assumptions.
Observation: the source uses a clause-final assumption rider.
Decision: apply only if the assumption still qualifies the same procedure.
Revision: “[PROCEDURE], assuming that [ASSUMPTION].”
Preserve: the assumption itself and its scope; introduce no new condition.
Evidence label: observed choice in this paper, not a general requirement.
```

## 5. Write the revision

Produce one recommended revision by default. Preserve effective original wording when no useful style change is supported. If no changes are warranted, return the original with that judgment; do not create differences to demonstrate activity.

Offer additional candidates when the user requests comparison or when materially different, supported style choices deserve presentation. Explain the actual choice between them. Do not fill fixed conservative/standard/deep slots or vary hedge density to manufacture alternatives.

Work from the selected edits and their evidence. A separate revision worker needs `0-draft.prose.txt`, relevant author constraints and context, and the selected evidence and edits from `review-notes.md`. The full corpus need not be reread during drafting. If evidence is insufficient, resolve the comparison before applying that edit.

### Preserve meaning while adopting style

- Preserve values, units, uncertainty, citations, figure/table/equation identifiers, and the entities and claims they refer to.
- Treat certainty, causality, scope, polarity, and consequential conditions as substance. Do not replace `proves` with `suggests`, or the reverse, merely because the reference favors one verb.
- Reorder or combine sentences when the same argument and evidential dependencies remain clear. Explain substantial restructuring. Do not turn sequence into causation or change which evidence supports which conclusion.
- If a proposed edit would change the scientific claim, leave it outside the style-only revision and explain the issue. Proceed with a substantive change only when the user's request covers it and supporting evidence is available.

### Reuse language with context

Imitate useful frame shapes without mechanically reproducing a source sentence. A word or phrase occurring once is not forbidden, and a recurrent phrase is not automatically appropriate.

Before making a recurrence-based recommendation, read the relevant frame's Singleton/Recurrent status in `logic.md` §E.5. `anchors.txt` contains one anchor phrase per line for counting; it does not store these status labels. During §3, bring the frame identifier, status, source address, and anchor wording into the compact evidence notes so §5 can use them without reopening the full corpus. Reuse a Singleton's structural pattern rather than its distinctive anchor wording. A Recurrent label permits considering the wording in context; it is not an instruction to insert it. Do not use aggregate `manifest.frames.singleton_rate` to infer an individual expression's status. If §E.5 is missing or unreadable, record the individual status as unassessed and make no recurrence claim.

Save the manuscript text alone in `revision.txt`. Keep edit identifiers, explanations, and measurement results in `review-notes.md`, not in that text file. Additional candidates, when needed, use separate prose-only files such as `revision-option-2.txt`.

For a legacy candidate file containing a metadata header, extract only the manuscript body after its documented header delimiter into a prose-only file before comparing it. Exclude placeholders such as “unchanged from the draft”; use the actual original prose in that case.

## 6. Check the result and report

The required inputs here are `0-draft.prose.txt`, `review-notes.md`, and `revision.txt` (plus any additional prose-only candidates). Compare the original prose with every candidate before recommending it.

### Gate 1 — Mechanical preservation

Run a machine count and item-by-item comparison on the prose-only files. Never count edit IDs, report headings, or metadata. The old workflow once satisfied “Figure 2 -> Fig. 2” by deleting the reference altogether; a successful vocabulary edit must not hide that loss.

Run the bundled standalone script from the run folder (replace `<skill-dir>` with the actual path; use `python`, `python3`, or `py -3` as available):

```text
python "<skill-dir>/scripts/preservation_inventory.py" --before "0-draft.prose.txt" --after "revision.txt" --citation-style author-year --output "inventory.tsv"
```

Choose `author-year`, `numeric` (square-bracket citation numbers), or `none` from the manuscript's notation. The script writes the before/after table and an overall result to `inventory.tsv` and stdout; exit codes are 0 = PASS, 1 = FAIL, 2 = BLOCKED. Keep the actual output and reference it in `review-notes.md`. The script has no dependencies and does not involve `quant_check.py`.

Supported forms: display references `Figure 2`/`Fig. 2`, `Table S1`, `Fig. 4A and B`, `Fig. 1B–D`, `Figures 2–4`, `Fig. 2(a)`, `Eq. (2)`, `Eqs. (6) and (7)`; author-year citations (`Smith et al., 2020`; `Smith (2020)`; `Jones & Lee, 2021`); numeric citations (`[8,23,77]`, `[1–3]`); numbers with sign, decimals, thousands separators, exponents (`1.2e-3`, `3 × 10^-4`), ranges and chains (`2–5%`, `11–12–10`), and `±`; identifiers, meaning any remaining letter–digit token (`δ15N`, `NO3-N`, `Ca2+`, `PC1`, `10th`, `A-02`, `10⁻³`). Reference and citation digits are excluded from the number inventory. A bare year outside a recognised citation is counted as a number and listed in a `note` row so it can be inspected.

BLOCKED means the extractor could not assign something reliably: a singular reference followed by a numeric list (`Figure 2 and 10 samples`), a name particle before an author (`van Smith (2020)`, where the particle may belong to the name), a bracket citation in author-year mode or an author-year citation in numeric or `none` mode, a digit that could not be assigned, empty prose, or a metadata header, delimiter, or placeholder in the prose file. Before accepting PASS, inspect the extracted keys against the manuscript's notation. For an unsupported form, extend the extractor and add a regression case to `scripts/test_inventory.py`; do not remove troublesome prose or claim an unperformed check. Validation record: on the SCI_kkh corpus (two papers, nine section files, author-year and numeric), identical texts PASS, and single deletions of a panel range, a citation, an isotope identifier, and a changed value each FAIL. Parser coverage and the semantic gate remain required even when the command exits 0.

Build inventories for both texts and record the results in `review-notes.md`:

| Inventory | Comparison key | Default pass condition |
|---|---|---|
| Figure, table, equation references | Object type and full identifier, including panels and supplements | Every item's occurrence count is unchanged |
| Citations | Source identity or citation key; expand grouped citations into individual cited sources | Every cited source's occurrence count is unchanged |
| Numeric expressions | Complete expression, retaining sign, decimals, exponent, range, and percent marker | Every expression's occurrence count is unchanged |
| Identifiers | Letter–digit tokens (isotopes, ions, components, ordinals, sample IDs) with dashes unified | Every token's occurrence count is unchanged |

Normalize only identity-preserving formatting: `Figure 2` and `Fig. 2` map to the same figure identifier. Do not collapse different panel labels or normalize away a minus sign. For citation or reference ranges, account for every identified item. Inspect the source text to ensure the extractor covers the manuscript's actual notation, including Unicode signs and superscripts; a parser returning no matches is not proof that there are no items.

**PASS:** all three inventories match. The script never grants authorization exceptions. If the user already authorized a specific change, preserve its raw FAIL result and record a separate `PASS WITH USER-AUTHORIZED EXCEPTION` adjudication only when every differing row exactly matches the recorded authorization and no BLOCKED issue remains; never relabel the script output as PASS. If a category is genuinely absent, record “none present” after checking the prose.

**FAIL:** an item's count falls, an identifier or numeric expression changes, or an unapproved item is added. Restore the original item and rerun the affected comparison. Do not satisfy the gate by inserting an unrelated duplicate elsewhere.

**BLOCKED:** the comparison cannot reliably identify the items in the notation used. Improve the extractor or explicitly resolve the unparsed items before declaring a pass. Do not replace an unperformed mechanical check with a claim of verification.

Consolidating repeated references requires user authorization covering that consolidation. Record the affected identity, before/after counts, and authorization in the notes; compare against that explicit exception. Without authorization, preserve the occurrences. This gate does not require an approval request for ordinary edits that preserve the inventories.

Minimum verification record:

```markdown
| Kind | Item | Before | After | Authorized exception | Result |
|---|---|---:|---:|---|---|
| figure | figure:2 | 1 | 1 | none | PASS |
| citation | <source key> | 2 | 2 | none | PASS |
| number | -0.25 | 1 | 1 | none | PASS |
| identifier | δ15N | 40 | 40 | none | PASS |
Mechanical gate: PASS; extractor coverage checked against the prose.
```

### Gate 2 — Semantic preservation

After Gate 1 passes (or has the explicitly documented user-authorized exception above), compare the texts sentence by sentence, mapping merged or reordered sentences back to their originals. Confirm:

- Each value remains attached to the same entity, group, time, unit, and uncertainty estimate.
- Each citation or display reference remains attached to the same supported claim or object.
- Negation, conditions, certainty, causal meaning, and generalization scope are preserved.
- No material claim, condition, or evidence has been introduced or omitted without authorization.

“A = 10, B = 20” and “A = 20, B = 10” pass the numeric inventory and fail this gate. Record the affected sentence mapping and reason for any failure.

**PASS:** every original substantive statement and support relationship is preserved, or changed only within a documented, supported user-authorized exception. **FAIL:** a relationship or meaning changed unintentionally. **BLOCKED:** the intended meaning cannot be established. Repair introduced errors and recheck; if repair depends on author intent, retain the original wording and flag the choice.

Both gates must pass before a candidate is recommended. Meaning-preservation checks remain mandatory even when optional style measurements are omitted.

Then confirm that the selected style edits were actually realized and still fit their contexts. Inspect the revised paragraph transitions and vocabulary uses, not only the absence of old wording. Reuse existing measurements if the prose has not changed; do not run a second quantitative pass by default.

### Present a useful result

Write the explanation in the user's language. Give:

1. A brief scope statement identifying N and the selected references, the section mapping, and the analysis method. For N≤2, explicitly label adopted structural habits as choices in those papers. State any context limitations or reference-informed follow-up.
2. The important wording or structural differences and why the selected edits fit.
3. The complete recommended revision, or the original if retained.
4. Meaningful alternatives and deliberately unapplied differences. If none remain, say so briefly; do not invent an omitted feature to fill the record.
5. A concise statement of what preservation checks were performed and what remains unresolved.

Use this compact report skeleton. Headings may be translated or combined, but retain the scope, evidence qualification, complete prose, and gate results:

```markdown
N: <n>; references: <full slugs>; section: <section>
Section mapping: <exact / explicitly documented fusion / unresolved>
Analysis: <independent context / isolation by ordering / informed follow-up>
Evidence scope: <for N≤2: structural habits are choices in these papers>

## Main edits
<Important lexical and structural changes, with source evidence and reasons.>

## Recommended revision
<Complete manuscript prose, or the original if retained.>

## Unapplied choices and open questions
<Material differences, alternatives, or a brief “none”.>

## Preservation
Mechanical: <PASS / FAIL / BLOCKED>; semantic: <PASS / FAIL / BLOCKED>.
Authorized exceptions: <details, or none>.
Source checking: <what was actually inspected; scientific citations unverified
unless their support was checked separately>.
```

A failed or blocked candidate is a diagnostic draft, not the recommended revision. There is no fixed candidate count or mandatory numeric style table. Preserved citations have not thereby been verified against their original publications. Clearly distinguish style-corpus inspection from checking the scientific support for the draft's claims.

### Re-entry

For a wording adjustment, reuse the recorded comparison and recheck the changed prose. A changed source draft invalidates its extraction and affected comparisons. A new reference requires examining that reference and revisiting the affected decisions, not blindly replaying every step.

File existence alone does not establish freshness. Before reusing a run, check that its recorded draft, selected references, scope, and author instructions still match the current request.

---

**Guide version:** 5.0.0 (2026-09-14).  
**Paired SKILL.md:** meta-styling 5.0.0.  
**Corpus contract:** extraction-style v3.x; verify actual headings and anchor format when reading older extractions.
