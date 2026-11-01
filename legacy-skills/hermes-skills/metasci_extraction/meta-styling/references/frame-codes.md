# Sentence frame codes A1–L4 + Z

Guide companion: 5.0.0 (2026-09-14).

**Provenance.** The code/name/template table below is bundled from
`extraction-style/references/lens-architecture.md` §A.4 so draft tagging does not
require installing that skill. Code and name pairs are also shared with
`extraction-logic/references/extraction_template.md`. The table remains unchanged;
the usage rules below are local revision guidance. Update the table from upstream,
then review these usage rules separately rather than replacing this entire file.
A shared taxonomy version and build-time comparison are still pending repository
integration; a copy date alone does not establish compatibility. If a corpus uses a
different code/name mapping, record the conflict and resolve it before comparing
code distributions. Do not silently reinterpret existing corpus labels.

**How draft tagging uses this (revision guide §2).** Assign one primary frame code
to each sentence being tagged. Match its skeleton—connectives, reporting verbs,
clause arrangement, and slot order—before considering its subject matter. Templates
are structural examples, not literal string patterns. If multiple templates fit,
use the sentence's rhetorical function to break the tie. For a multi-clause sentence,
choose the frame organizing the whole sentence; note subordinate shapes separately
without counting the sentence twice. If none fits, use `Z`; do not invent a new
A–L code or force a fit. A high Z rate is a finding, not a failure or a target.

## Code families

| Family | Main function |
|---|---|
| A | Background and definition |
| B | Literature citation and attribution |
| C | Research gap |
| D | Study purpose and scope of action |
| E | Methods |
| F | Results |
| G | Interpretation |
| H | Comparison |
| I | Concession and limitation |
| J | Implications and future work |
| K | Cause and consequence |
| L | Summary and synthesis |

Families describe rhetorical functions, not mandatory section locations. An F frame
can occur in Discussion. Do not rewrite a sentence to achieve a family distribution.

## Distinguishing neighboring codes

Apply these distinctions only after checking the sentence skeleton:

| Candidates | Decision rule |
|---|---|
| G4 / K4 | G4 presents a likely causal explanation of an observation; K4 asserts the causal link without that hedge. Preserve the original certainty: never delete or add `likely` to obtain a code. |
| G3 / B6 | G3 aligns a finding with a theory or explanatory expectation; B6 explicitly aligns a claim with an attributed author/study. A citation merely appended to a theory does not automatically make it B6. |
| H2 / I1 / B4 | H2 contrasts two propositions; I1 acknowledges a concession before the main point; B4 contrasts findings attributed to two studies. A temporal `while` is not H2 merely because it uses that word. |
| A3 / F7 | A3 establishes a field/topic trend as background; F7 reports a trend in the study's own data. Use function and evidence ownership, not section heading alone. |
| L2 / D5 | L2 states what the study demonstrates as a conclusion; D5 states what the study undertakes or aims to do. `This study` alone cannot distinguish them. |

If a genuine ambiguity remains, retain one provisional primary code and record the
alternative and reason in `review-notes.md`. Do not base an edit on that unresolved
difference. The one-code rule applies to frames; extensible function/role labels may
still use combinations such as `Decision+Qualification`.

## Reference taxonomy

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

## Z shapes: name, template, and comparison

Use `Z` when the taxonomy does not cover the sentence's organizing shape. Name the
shape in `Capitalized-Hyphenated` form and add one abstracted `[SLOT]` template line.
The name is a description under Z, not an additional frame code. One occurrence can
be named; call it recurrent only when evidence supports recurrence.

During independent draft tagging (revision guide §2), assign a provisional descriptive
name without opening the reference findings. During comparison (§3), look for the
same shape in the reference's `logic.md` §F and check its catalog evidence in §E.
When skeleton and function agree, reuse the reference's existing name and record the
mapping from the provisional name. A matching name alone is not proof of the same
shape. If two papers use different names for the same shape, record an alias mapping
with both source addresses; preserve the corpus files and their original names.

Record Z entries in the draft map within `review-notes.md`, for example:

```text
Location: draft:P2-S3
Frame: Z
Shape: Assumption-Rider
Template: [MAIN_CLAIM], assuming that [ASSUMPTION].
Comparison: <paper-slug>:<§F entry and §E sentence address>, or unassessed
```

Other descriptive examples are `Enumerated-Inventory`:
`There are [N] forms of [X]: (1) [A]; (2) [B]; and (3) [C].`
and `Therefore-Decision`:
`Therefore, [DATA] was used to [PURPOSE], regardless of [FACTOR].`
These illustrate shapes, not wording to insert or verified source quotations.
Do not assign a desired Z percentage; report corpus measurements only with their
paper, section, denominator, and measurement basis when that comparison is needed.
