# Frame Codes A1–L4 + Z (bundled copy)

**Provenance.** This is a copy of `extraction-style/references/lens-architecture.md`
§A.4 "Reference taxonomy", copied 2026-08-18 so that Stage 1a can tag a draft without
`extraction-style` being installed. The taxonomy is shared with `extraction-logic` and
`extraction-style`; **edits happen upstream in `lens-architecture.md`, then re-copy here.**
Editing this copy directly means the next re-copy silently reverts it. If a corpus was
extracted under a newer taxonomy than this copy, trust the corpus's codes and re-copy.

**How Stage 1a uses this.** Assign each draft sentence the code whose template matches its
skeleton. **Do not invent codes** — anything the taxonomy does not name is `Z`, and a high
`Z` rate is a finding, not a failure (measured on real papers: 26.5% and 39.5%, an order
of magnitude above the taxonomy's illustrative 3%).

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

## Z is where the style is

The taxonomy is a reference, not a boundary. When a draft sentence's shape recurs but has
no code, that recurring `Z` shape is itself style evidence — the reference cards name such
shapes explicitly (examples measured on a real paper: Enumerated-Inventory
`"There are [N] forms of [X]: (1) …; (2) …; and (3) …"`, Assumption-Rider
`"…, assuming that [ASSUMPTION]."` clause-final, Therefore-Decision
`"Therefore, [DATA] was used to [PURPOSE], regardless of [FACTOR]."`). In `1a-structure.md`
tag them `Z` and note the shape in a word or two; Stage 2 matches them against the
reference's own named Z shapes in `logic.md`.
