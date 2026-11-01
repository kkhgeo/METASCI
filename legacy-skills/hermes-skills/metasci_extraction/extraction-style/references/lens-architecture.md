# Lens A — Architecture and Sentence Frames

**Output**: `logic.md`, `anchors.txt`
**Reads**: `sections/*.txt` (never the PDF)

Capture the *shape* of the paper: how sections are built, how paragraphs relate, and the
rhetorical mould of every sentence. This is the structural half of style — Lens W covers
the lexical half, Lens C selects from both.

> **Taxonomy sync.** The frame codes A–L below are shared with `extraction-logic`. If you
> change one, change both, or the same sentence will get two different names in two files.

---

## A.1 Structure map

Read the section files in order. Number paragraphs **continuously across the whole paper**
(`P1 … Pn`, never restarting per section) and sentences **within each paragraph**
(`S1 … Sn`, restarting at each paragraph). That address, `[P#-S#]`, is what joins this file
to `style-vocab.md` and `card.md`. Every quoted item carries one.

Produce a structure tree and an overview table:

| Section | Subsections | Paragraphs | Sentences | Core function |

Record the **actual** structure, not IMRaD. A fused "Results and discussion" is a real
feature of the paper, not a defect to normalize away — say so and tag those paragraphs `R`.

## A.2 Inter-paragraph logic

One function tag per paragraph, and the relation to the next.

**Function tags** (extend freely; a new tag is information, a forced fit is not):

- *Introduction*: Background · Literature-Review · Gap · Question · Purpose · Scope · Contribution
- *Methods*: Study-Area · Design · Sample · Procedure · Instrument · Statistical · Quality
- *Results*: Overview · Finding · Comparison · Trend · Pattern · Anomaly · Summary
- *Discussion*: Interpretation · Mechanism · Lit-Comparison · Agreement · Disagreement ·
  Limitation · Implication · Future · Conclusion

**Relations**: Continuation · Contrast · Cause-Effect · Specification · Generalization ·
Sequence · Concession · Problem-Solution · Evidence-Claim · Question-Answer

Emit a table per section plus a one-line flow diagram:

```
P1[Background] →(Specification)→ P2[Background-National] →(Cause-Effect)→ P3[Cause-Policy]
```

**Absences are findings.** No roadmap paragraph, no Limitations paragraph, zero Contrast
relations in Methods — record each explicitly. They feed the card's red flags, and a
reader cannot infer them from what is present.

## A.3 Intra-paragraph logic

Full sentence-by-sentence analysis for **representative paragraphs** — one or two per
section, chosen because they show the section's typical chain — plus a summary table of
recurring chain shapes for the rest. A complete pass over every paragraph is
`extraction-logic`'s job, not this one.

**Roles**: Topic · Claim · Evidence · Elaboration · Example · Transition · Qualification ·
Reference · Method · Conclusion · Bridge

**Relations**: Support · Contrast · Cause-Effect · Elaboration · Example · Addition ·
Condition · Sequence · Concession · Summary · Comparison · Restatement

Note where the hedging work actually happens. On the test paper it was two `Qualification`
sentences inside one eight-sentence Results paragraph — not a Limitations section, which
the paper does not have.

## A.4 Sentence frame catalog — exhaustive

Every body-prose sentence gets a row:

| # | Frame Type | Abstracted Template | Original Sentence | Source |

- **Template**: the sentence with content replaced by `[SLOT]`, skeleton preserved.
- **Original**: verbatim. Symbols from the page images, word content from the text layer.
- **Source**: `[P#-S#]`.

### Reference taxonomy (shared with extraction-logic)

| Code | Frame | Template |
|------|-------|----------|
| A1 | General-Importance | `"[TOPIC] is [SIGNIFICANCE] for [CONTEXT]."` |
| A2 | Established-Knowledge | `"It is well established that [FACT]."` |
| A3 | Trend-Statement | `"[TOPIC] has [TREND] over [TIMEFRAME]."` |
| A4 | Definition | `"[TERM] is defined as / known as [DEFINITION]."` |
| A5 | Scope-Setting | `"[TOPIC] encompasses [RANGE]."` |
| A6 | Quantitative-Context | `"[QUANTITY] of [TOPIC] [VERB] [CONTEXT]."` |
| B1 | Author-Active | `"[AUTHOR] [REPORTING_VERB] that [FINDING] [LIT]."` |
| B2 | Info-Prominent | `"[CLAIM] [LIT]."` |
| B3 | Multiple-Support | `"[CLAIM] has been reported by several studies [LIT_CLUSTER]."` |
| B4 | Contrasting-Findings | `"While [STUDY_A] found [X], [STUDY_B] reported [Y]."` |
| B5 | Methodological-Ref | `"Following [AUTHOR] [LIT], …"` |
| B6 | Agreement-Citation | `"Consistent with [AUTHOR], [CLAIM]."` |
| C1 | Concessive-Gap | `"Although [PRIOR_WORK], [GAP]."` |
| C2 | Direct-Gap | `"However, [GAP_STATEMENT]."` |
| C3 | Despite-Gap | `"Despite [KNOWLEDGE], [GAP]."` |
| C4 | No-Study-Gap | `"To date, no study has [TOPIC]."` |
| C5 | Remaining-Question | `"[QUESTION] remains poorly understood."` |
| C6 | Limited-Knowledge | `"Our understanding of [TOPIC] is limited by [CONSTRAINT]."` |
| D1 | Here-We | `"Here, we [ACTION] to [PURPOSE]."` |
| D2 | Aim-Statement | `"The objective of this study was to [PURPOSE]."` |
| D3 | We-Sought | `"We sought to [VERB] [QUESTION]."` |
| D4 | Hypothesis | `"We hypothesized that [HYPOTHESIS]."` |
| D5 | This-Study | `"This study [ACTION] [PURPOSE]."` |
| D6 | To-Address | `"To address [GAP], we [ACTION]."` |
| E1 | Passive-Procedure | `"[SAMPLE] was/were [PROCEDURE] using [INSTRUMENT]."` |
| E2 | To-Purpose-Action | `"To [PURPOSE], [SAMPLE] was [PROCEDURE]."` |
| E3 | Following-Protocol | `"Following [PROTOCOL], [PROCEDURE]."` |
| E4 | Condition-Detail | `"[PROCEDURE] was performed at [CONDITION]."` |
| E5 | Tool-Specification | `"[ANALYSIS] was conducted using [SOFTWARE] (version [VER])."` |
| E6 | Quantitative-Method | `"[QUANTITY] of [SAMPLE] were [PROCEDURE] at [PLACE]."` |
| E7 | Quality-Statement | `"[MEASURE] was assessed by [METHOD], yielding [RESULT]."` |
| F1 | Analysis-Revealed | `"[ANALYSIS] revealed that [FINDING] [STAT]."` |
| F2 | Variable-Pattern | `"[VAR] [DIRECTION] in [GROUP] compared to [COMPARISON] [STAT]."` |
| F3 | Range-Report | `"[VAR] ranged from [MIN] to [MAX], with a mean of [MEAN]."` |
| F4 | Correlation | `"A significant correlation was found between [A] and [B] [STAT]."` |
| F5 | Figure-Reference | `"As shown in [FIGURE], [FINDING]."` |
| F6 | Proportion-Report | `"[QUANTITY] of [TOTAL] [VERB] [CHARACTERISTIC]."` |
| F7 | Trend-Report | `"[VAR] [DIRECTION] [TEMPORAL/SPATIAL] [STAT]."` |
| F8 | Group-Comparison | `"[A] exhibited [X], whereas [B] showed [Y]."` |
| F9 | No-Significant | `"No significant difference was found between [A] and [B]."` |
| G1 | Results-Suggest | `"[AGENT] suggest(s)/indicate(s) that [INTERPRETATION]."` |
| G2 | Attributed-To | `"[OBSERVATION] may be attributed to [MECHANISM]."` |
| G3 | Consistent-With | `"[FINDING] is consistent with [THEORY]."` |
| G4 | Likely-Due-To | `"[OBSERVATION] is likely due to [CAUSE]."` |
| G5 | Possible-Mechanism | `"One possible explanation is that [MECHANISM]."` |
| G6 | Supported-By | `"This interpretation is supported by [EVIDENCE]."` |
| G7 | Taken-Together | `"Taken together, these [FINDINGS] suggest [CONCLUSION]."` |
| H1 | Compared-To | `"Compared to [COMPARISON], [SUBJECT] [DIFFERENCE]."` |
| H2 | While-Contrast | `"While [A], [B]."` |
| H3 | In-Contrast | `"In contrast to [A], [B] [DIFFERENCE]."` |
| H4 | Unlike-Previous | `"Unlike [PREVIOUS], our [FINDING]."` |
| H5 | Similarly | `"Similarly, [PARALLEL_FINDING] [LIT]."` |
| H6 | Higher-Lower | `"[VAR] was [QUANTITY] higher in [A] than in [B]."` |
| I1 | Although-However | `"Although [ACKNOWLEDGED], [MAIN_POINT]."` |
| I2 | Limitation-Acknowledge | `"A limitation of this study is [LIMITATION]."` |
| I3 | Should-Be-Noted | `"It should be noted that [CAVEAT]."` |
| I4 | Despite-Still | `"Despite [LIMITATION], [POSITIVE]."` |
| I5 | Cannot-Rule-Out | `"We cannot rule out that [ALTERNATIVE]."` |
| I6 | Beyond-Scope | `"[TOPIC] is beyond the scope of this study."` |
| J1 | Implications-For | `"These findings have implications for [APPLICATION]."` |
| J2 | Could-Be-Used | `"[METHOD] could be used to [APPLICATION]."` |
| J3 | Future-Should | `"Future studies should [RECOMMENDATION]."` |
| J4 | Further-Needed | `"Further research is needed to [PURPOSE]."` |
| J5 | Highlight-Need | `"Our results highlight the need for [ACTION]."` |
| J6 | Provides-Framework | `"This study provides a framework for [APPLICATION]."` |
| K1 | Resulting-In | `"[CAUSE], resulting in [EFFECT]."` |
| K2 | If-Then | `"If [CONDITION], [CONSEQUENCE]."` |
| K3 | This-Led-To | `"[PROCESS] led to [OUTCOME]."` |
| K4 | Due-To | `"[EFFECT] is due to [CAUSE]."` |
| K5 | Thereby | `"[ACTION], thereby [RESULT]."` |
| L1 | In-Summary | `"In summary, [CONCLUSION]."` |
| L2 | This-Study-Shows | `"This study demonstrates that [CONCLUSION]."` |
| L3 | Overall | `"Overall, [SYNTHESIS]."` |
| L4 | Collectively | `"Collectively, [EVIDENCE] indicate [CONCLUSION]."` |
| **Z** | **Uncategorized** | anything the taxonomy does not cover — **mandatory** |

### Z is where the style is

The taxonomy is a reference, not a boundary. On the test paper **30% of sentences fell to
Z** (66 of 219) against the template's illustrative 3%. That is not a classification
failure — it is the finding. A third of that author's sentences have shapes no standard
taxonomy names, and those shapes are the most transferable thing in the extraction.

Collect recurring Z shapes into their own table with a name, template, frequency and the
sections they appear in. Examples found on the test paper:

| Z shape | Template |
|---------|----------|
| Enumerated-Inventory | `"There are [N] forms of [X]: (1) …; (2) …; and (3) …"` |
| Assumption-Rider | `"…, assuming that [ASSUMPTION]."` (clause-final, unflagged) |
| Therefore-Decision | `"Therefore, [DATA] was used to [PURPOSE], regardless of [FACTOR]."` |
| Equation-Lead-In | `"Thus, [X] can be [OPERATION]ed by [Y]:"` → display equation |

## A.5 Anchor validation — REQUIRED

An abstracted template seen once is a *sentence*, not a *template*. Extract each frame's
fixed lexical anchor into `anchors.txt`, then measure:

```bash
py -3.10 scripts/quant_check.py count --items anchors.txt sections/*.txt
```

### Anchor admission rule — all four must hold

1. **≥ 3 words.**
2. **≥ 1 content word.** Not only articles, prepositions, conjunctions, auxiliaries.
3. **No comma inside.** The matcher joins words with `\s+`; a comma breaks the match, so
   `therefore we consider` scores 0 against the real *"Therefore, we consider"*.
4. **No symbols.** `δ¹⁵N` renders as `d15N`, `Cl⁻` as `Cl/C0`. Never anchor on one.

**Bare connectives are not anchors.** `therefore`, `however`, `thus`, `moreover`,
`in contrast`, `regardless of` score high and measure the *word*, not the *frame*.
`therefore ×11` does not mean the Therefore-Decision frame ran eleven times. They belong to
Lens W. Excluding them is the difference between a real result and a flattering one:

| anchor set | verdict |
|-----------|---------|
| v1, connectives included | "frames recur heavily" — *therefore* 11, *however* 11, *thus* 10 |
| v2, admission rule applied | **190 of 193 frames occur exactly once** |

### What the measurement is for

Mark each frame `Recurrent` (Freq ≥ 2) or `Singleton` (Freq = 1). Singletons stay in the
catalog as distinctive moves but must never be presented as reusable templates.

The expected result is that **almost everything is a Singleton**. That is the paper's most
important structural fact and it becomes the card's first rule: *imitate the frame type,
never the anchor wording.*

### The gate also catches misquotes

A zero-scoring anchor means one of two things: the anchor is malformed, or the quoted
sentence is wrong. Check the text before assuming the former. On the test paper the gate
disproved **five sentences in 219** transcribed from page images:

| I had written | The paper says |
|---------------|----------------|
| "**Thus,** we evaluated…" | "**To achieve this,** we evaluated…" |
| "has been previously **introduced with**" | "has been previously **investigated, with**" |
| "can be projected **onto** the" | "can be projected **on** the" |
| "There **are** no significant differences" | "There **were** no significant differences" |
| *(sentence omitted entirely)* | "Additionally, PC2 explains the inverse relationship…" |

A 2.3% verbatim error rate from reading alone, every one of which would have travelled
into the card as if it were the author's wording. Record the count in
`manifest.provenance.verbatim_errors_caught`. Zero on a long paper is suspicious, not
reassuring.

## A.6 Output file

```
logic.md
  A. Paper information + structure deviations
  B. Structure map (tree + overview table)
  C. Inter-paragraph logic (table + flow per section)
  D. Intra-paragraph logic (representative paragraphs + chain-shape summary)
  E. Sentence frame catalog (per section) + anchor validation + distribution summary
  F. Analysis summary (statistics, recurring patterns, Z shapes, notable observations)

anchors.txt
  header comment stating the admission rule and the counting command,
  then one anchor per line, grouped by section
```

Then fill `manifest.frames` and `manifest.paper`.
