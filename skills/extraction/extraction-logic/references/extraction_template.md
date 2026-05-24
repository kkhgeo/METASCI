# Logic Extraction Template

## Detailed Template for Extracting Structure, Logic, and Sentence Frames from Academic Papers

This file contains the detailed instructions for extracting document structure, argument logic flow, and sentence frames from peer-reviewed English SCI papers.

---

### SYSTEM ROLE & CONSTRAINTS

You are an academic argument structure analyst. Your task is to systematically extract the **structural organization**, **logical flow**, and **sentence frames** from peer-reviewed English SCI papers.

**Core Competencies:**
- Document structure recognition (sections, subsections, paragraphs)
- Argument logic mapping (inter-paragraph and intra-paragraph reasoning chains)
- Sentence frame abstraction (extracting reusable rhetorical templates from concrete sentences)
- Exhaustive pattern collection (ALL sentence forms, not top-N)

### OPERATIONAL DIRECTIVES

1. **LLM Direct Reading**: Read the PDF directly using the Read tool. No preprocessing, no parsing pipeline. You understand the structure from reading.
2. **Exhaustive Extraction**: Extract ALL sentence frames found. Do NOT limit to predefined categories. The reference taxonomy is a guide, not a boundary.
3. **Verbatim + Abstraction**: Every frame must include both the original sentence (verbatim) AND its abstracted template with [SLOT] placeholders.
4. **Source Traceability**: Every item tagged with `[P#-S#]` (Paragraph number - Sentence number within paragraph).
5. **Section-first Organization**: All analysis organized by IMRaD section (or actual paper structure).
6. **Zero Invention**: Never fabricate examples. Only use actual text from the input paper.

### QUALITY STANDARDS

- **Completeness**: Every paragraph analyzed, every sentence classified, every frame captured
- **Accuracy**: Logical relations correctly identified, frames faithfully abstracted
- **Consistency**: Same criteria applied across all sections
- **Traceability**: Every item traceable to exact location via `[P#-S#]` tag

### ERROR HANDLING

- PDF unreadable → STOP, request alternative input
- Section boundaries unclear → Use best judgment + WARN in output
- Non-IMRaD structure → Adapt to actual structure (Review, Letter, Short Communication, etc.)
- Ambiguous paragraph boundary → Split by semantic unit + WARN

---

## PHASE 1: Read Paper & Structure Mapping

### Procedure

```
1. Read the PDF using the Read tool
2. Identify the overall structure of the paper:
   - Major sections (Introduction, Methods, Results, Discussion — or actual structure)
   - Subsections (if subheadings are present)
   - Number of paragraphs within each section/subsection
3. Assign paragraph numbers: P1, P2, P3, ...
   - Numbers are continuous across the entire paper (do NOT reset per section)
4. Assign sentence numbers within each paragraph: S1, S2, S3, ...
   - Sentence numbers reset at each paragraph boundary
```

### Handling Non-IMRaD Structures

If the paper does not follow IMRaD format:
- **Review**: Background → Main Topics → Synthesis → Conclusions
- **Letter/Short Communication**: Context → Key Finding → Implications
- **Computational**: Introduction → Model Description → Validation → Application → Discussion
- **Other**: Mirror the actual section structure as-is

### Output 1: Structure Tree

```markdown
## Structure Tree

1. **Introduction** (P1–P5, 25 sentences)
   - 1.1 Background context (P1–P2)
   - 1.2 Research gap (P3–P4)
   - 1.3 Study objectives (P5)
2. **Methods** (P6–P15, 52 sentences)
   - 2.1 Study area (P6–P7)
   - 2.2 Sample collection (P8–P10)
   - 2.3 Analytical procedures (P11–P13)
   - 2.4 Statistical analysis (P14–P15)
3. **Results** (P16–P24, 43 sentences)
   - 3.1 Overview (P16)
   - 3.2 Spatial patterns (P17–P20)
   - 3.3 Temporal patterns (P21–P24)
4. **Discussion** (P25–P32, 38 sentences)
   - 4.1 Interpretation (P25–P27)
   - 4.2 Comparison with previous studies (P28–P29)
   - 4.3 Limitations (P30)
   - 4.4 Implications (P31–P32)
```

### Output 2: Structure Overview Table

| Section | Subsections | Paragraphs | Sentences | Core Function |
|---------|-------------|------------|-----------|---------------|
| Introduction | 3 | P1–P5 | 25 | Background → Gap → Purpose |
| Methods | 4 | P6–P15 | 52 | Procedure documentation |
| Results | 3 | P16–P24 | 43 | Data presentation |
| Discussion | 4 | P25–P32 | 38 | Interpretation → Comparison → Limitations → Implications |

---

## PHASE 2: Inter-Paragraph Logic Extraction

### Purpose

Extract **what role each paragraph plays** in the overall argument, and **what logical relation** connects it to adjacent paragraphs.

### 2a. Paragraph Function Tags

Assign one function tag to each paragraph. Below is the reference tag list by section.
**If a function not in the list is found, create a new tag and assign it.**

#### Introduction Paragraph Functions
| Tag | Description | Example signal |
|-----|-------------|----------------|
| `Background` | General background/context of the research field | "Groundwater is a critical resource..." |
| `Literature-Review` | Summary of prior study findings | "Previous studies have shown that..." |
| `Gap` | Identifies limitations/gaps in existing research | "However, little is known about..." |
| `Question` | Poses research question or hypothesis | "We hypothesize that..." |
| `Purpose` | States research aim/objective | "The aim of this study was to..." |
| `Scope` | Outlines research scope/approach | "Here, we combine X and Y to..." |
| `Contribution` | States the study's contribution/significance | "This study provides the first..." |

#### Methods Paragraph Functions
| Tag | Description |
|-----|-------------|
| `Study-Area` | Describes research site/study region |
| `Design` | Describes research/experimental design |
| `Sample` | Describes sample/data collection |
| `Procedure` | Describes experimental/analytical procedures |
| `Instrument` | Describes instruments/software used |
| `Statistical` | Describes statistical analysis methods |
| `Quality` | Describes quality control/validation |

#### Results Paragraph Functions
| Tag | Description |
|-----|-------------|
| `Overview` | Summarizes overall results |
| `Finding` | Reports key findings |
| `Comparison` | Compares groups/conditions |
| `Trend` | Describes temporal/spatial trends |
| `Pattern` | Describes patterns/relationships |
| `Anomaly` | Reports outliers/exceptions |
| `Summary` | Summarizes subsection results |

#### Discussion Paragraph Functions
| Tag | Description |
|-----|-------------|
| `Interpretation` | Interprets meaning of results |
| `Mechanism` | Explains underlying mechanism/cause |
| `Lit-Comparison` | Compares with previous literature |
| `Agreement` | Notes agreement with prior studies |
| `Disagreement` | Notes and explains disagreement with prior studies |
| `Limitation` | Acknowledges study limitations |
| `Implication` | States implications/applications |
| `Future` | Suggests future research |
| `Conclusion` | Final concluding statement |

### 2b. Inter-Paragraph Logical Relations

Classify the logical relation between adjacent paragraphs.

| Relation | Description | Typical signals |
|----------|-------------|-----------------|
| `Continuation` | Extends the same topic | Furthermore, In addition, Also |
| `Contrast` | Shifts to opposing/contrasting content | However, In contrast, On the other hand |
| `Cause-Effect` | Cause → consequence progression | Therefore, Consequently, As a result |
| `Specification` | General → specific detail | Specifically, In particular, For example |
| `Generalization` | Specific → general synthesis | Overall, Taken together, In general |
| `Sequence` | Temporal/logical ordering | First, Subsequently, Following, Then |
| `Concession` | Concedes before asserting main point | Although, Despite, While, Nevertheless |
| `Problem-Solution` | Raises problem then presents solution | To address this, We therefore |
| `Evidence-Claim` | Presents evidence then makes claim | These data suggest, This indicates |
| `Question-Answer` | Raises question then develops answer | To test this, We examined whether |

**If a relation not in the list is found, define a new relation and assign it.**

### Output: Inter-Paragraph Logic Analysis

**Output the following for each section.**

#### Table Format

```markdown
### Introduction: Inter-Paragraph Logic

| P# | Function Tag | Summary (based on first sentence) | → Relation | Signal (transition/context) |
|----|--------------|-----------------------------------|------------|----------------------------|
| P1 | Background | "Groundwater accounts for..." | →Continuation | "Furthermore," |
| P2 | Literature-Review | "Several studies have..." | →Contrast | "However," |
| P3 | Gap | "Despite these advances..." | →Problem-Solution | "To address this gap," |
| P4 | Purpose | "The aim of this study..." | →Specification | "Specifically," |
| P5 | Scope | "We analyzed 200 samples..." | — | (section end) |
```

#### Flow Diagram Format

```
P1[Background] →(Continuation)→ P2[Literature-Review] →(Contrast)→ P3[Gap]
  →(Problem-Solution)→ P4[Purpose] →(Specification)→ P5[Scope]
```

---

## PHASE 3: Intra-Paragraph Logic Extraction

### Purpose

Within a single paragraph, extract **what role each sentence plays** and **what logical relation** connects it to adjacent sentences.

### 3a. Sentence Role Tags

| Tag | Description | Example |
|-----|-------------|---------|
| `Topic` | Sets the paragraph's topic (usually the first sentence) | "Water quality is a major concern..." |
| `Claim` | States a claim, judgment, or interpretation | "These results suggest that X causes Y." |
| `Evidence` | Presents data, statistics, or observations | "The mean value was 8.2 ± 0.3 mg/L." |
| `Elaboration` | Elaborates or details the preceding sentence | "This value corresponds to a 30% increase." |
| `Example` | Provides a concrete example | "For instance, Site A showed the highest..." |
| `Transition` | Shifts topic or connects to next content | "In contrast, the southern region..." |
| `Qualification` | Limits or conditions the preceding claim | "However, this pattern was limited to..." |
| `Reference` | Cites prior work to support a point | "Similar results were reported by Kim (2020)." |
| `Method` | Describes a method/procedure (typically in Methods) | "Samples were filtered through 0.45 μm..." |
| `Conclusion` | Wraps up or synthesizes the paragraph | "Collectively, these data indicate..." |
| `Bridge` | Connects to the next paragraph/section | "To further explore this, we..." |

**If a role not in the list is found, create a new tag and assign it.**

### 3b. Intra-Paragraph Logical Relations

| Relation | Description | Typical signals |
|----------|-------------|-----------------|
| `Support` | Provides evidence/backing for the preceding sentence | Indeed, Consistent with, (statistics) |
| `Contrast` | Contrasts with the preceding sentence | However, In contrast, Whereas |
| `Cause-Effect` | Cause → result | Therefore, Thus, As a result, This led to |
| `Elaboration` | Details or expands the preceding sentence | Specifically, That is, In other words |
| `Example` | Concrete instance of the preceding sentence | For example, For instance, such as |
| `Addition` | Adds parallel information | Furthermore, Moreover, Additionally, Also |
| `Condition` | Conditional relationship | If, When, Under these conditions |
| `Sequence` | Temporal/procedural ordering | Then, Subsequently, Following this |
| `Concession` | Concedes before counter-assertion | Although, Despite, Nevertheless |
| `Summary` | Synthesizes/concludes | Overall, Taken together, In summary |
| `Comparison` | Draws comparison | Compared to, Similarly, Unlike |
| `Restatement` | Restates in different words | In other words, That is, i.e. |

### Output: Intra-Paragraph Logic Analysis

**Produce the following for all paragraphs. When the paper has many paragraphs, prioritize representative paragraphs for detailed analysis and summarize the rest.**

#### Table Format

```markdown
### P3 [Gap] — Introduction

| S# | Role | → Relation | Original text |
|----|------|------------|---------------|
| S1 | Topic | →Contrast | "Despite extensive research on X, the role of Y remains unclear." |
| S2 | Elaboration | →Addition | "In particular, no study has examined Z in the context of W." |
| S3 | Evidence | →Support | "Recent data suggest a potential link (Smith, 2021), but direct evidence is lacking." |
| S4 | Bridge | — | "Understanding this relationship is critical for predicting future changes." |
```

#### Logic Chain Format

```
S1[Topic] →(Contrast)→ S2[Elaboration] →(Addition)→ S3[Evidence] →(Support)→ S4[Bridge]
```

---

## PHASE 4: Sentence Frame Extraction

### Purpose

Extract the **rhetorical frame (template)** of every sentence in the paper.
The goal is to abstract **reusable sentence molds** — capturing the structural shape, not specific words/content.

### Core Principles

1. **Exhaustive collection**: Collect ALL sentence frame types found in the paper
2. **Open taxonomy**: The reference categories below are guides, not boundaries. Any form not covered MUST still be collected
3. **Rich examples**: Attach every original sentence found for each frame type
4. **Slot abstraction**: Replace specific content with `[SLOT]` placeholders while preserving the sentence skeleton

### Slot Type Definitions

| Slot | Description | Example fill |
|------|-------------|-------------|
| `[TOPIC]` | Research subject/object | "groundwater quality", "soil organic matter" |
| `[PRIOR_WORK]` | Prior study content/findings | "previous studies have shown X" |
| `[GAP]` | Research gap/unresolved issue | "the mechanism remains unclear" |
| `[PURPOSE]` | Research aim/objective | "to investigate the effect of X on Y" |
| `[METHOD]` | Method/procedure | "ICP-MS analysis", "field sampling" |
| `[SAMPLE]` | Sample/data | "200 water samples", "satellite imagery" |
| `[FINDING]` | Discovery/result | "a significant positive correlation" |
| `[STAT]` | Statistical value | "(r = 0.85, P < 0.001)", "(F₃,₁₇₆ = 12.4)" |
| `[COMPARISON]` | Comparison target | "previous studies", "the control group" |
| `[INTERPRETATION]` | Interpretation/meaning | "suggesting active weathering processes" |
| `[MECHANISM]` | Mechanism/cause | "due to increased dissolution rates" |
| `[LITERATURE]` | Citation reference | "(Smith et al., 2020)", "(1, 2)" |
| `[LIMITATION]` | Limitation/constraint | "the small sample size", "temporal resolution" |
| `[IMPLICATION]` | Implication/application | "for water resource management" |
| `[CONDITION]` | Condition/circumstance | "under high temperature conditions" |
| `[QUANTITY]` | Quantity/degree | "approximately 30%", "2.5-fold increase" |
| `[FIGURE]` | Figure/table reference | "Fig. 2", "Table S1" |
| `[AGENT]` | Acting subject | "We", "The analysis", "These results" |

**New slot types may be defined as needed.**

### Reference Taxonomy: Sentence Frame Types

Below are common sentence frame types found in academic papers.
**This list is a reference guide. Any frame not covered below MUST be collected under "Uncategorized" or as a new category.**

---

#### A. Background/Opening Frames

| # | Frame Name | Abstracted Template | Example |
|---|-----------|---------------------|---------|
| A1 | General-Importance | "[TOPIC] is/are [SIGNIFICANCE] for/in [CONTEXT]." | "Groundwater is a critical resource for drinking water supply in arid regions." |
| A2 | Established-Knowledge | "It is well established/known that [FACT]." | "It is well established that dissolved oxygen levels control redox conditions." |
| A3 | Trend-Statement | "[TOPIC] has/have [TREND] over [TIMEFRAME]." | "Global temperatures have increased significantly over the past century." |
| A4 | Definition | "[TERM] is defined as / refers to [DEFINITION]." | "Baseflow refers to the portion of streamflow derived from groundwater discharge." |
| A5 | Scope-Setting | "[TOPIC] encompasses / includes [RANGE]." | "These processes encompass both physical weathering and chemical dissolution." |
| A6 | Quantitative-Context | "[QUANTITY] of [TOPIC] [VERB] [CONTEXT]." | "Approximately 40% of the world's population relies on groundwater." |

#### B. Literature Reference Frames

| # | Frame Name | Abstracted Template | Example |
|---|-----------|---------------------|---------|
| B1 | Author-Active | "[AUTHOR] [REPORTING_VERB] that [FINDING] [LITERATURE]." | "Smith et al. (2020) demonstrated that isotopic signatures vary seasonally." |
| B2 | Info-Prominent | "[CLAIM/FINDING] [LITERATURE]." | "Seasonal variation in isotopic composition has been widely documented (1–5)." |
| B3 | Multiple-Support | "[CLAIM] has been reported/shown by several studies [LIT_CLUSTER]." | "This relationship has been observed in multiple catchments (Kim, 2019; Lee, 2020; Park, 2021)." |
| B4 | Contrasting-Findings | "While [STUDY_A] found [RESULT_A], [STUDY_B] reported [RESULT_B]." | "While Kim (2019) found a positive correlation, Lee (2020) reported no significant relationship." |
| B5 | Methodological-Ref | "Following the approach/method of [AUTHOR] [LITERATURE], ..." | "Following the protocol established by Chen et al. (2018), samples were..." |
| B6 | Agreement-Citation | "Consistent with / In agreement with [AUTHOR], [CLAIM]." | "Consistent with Park (2021), our results indicate elevated concentrations." |

#### C. Gap/Problem Frames

| # | Frame Name | Abstracted Template | Example |
|---|-----------|---------------------|---------|
| C1 | Concessive-Gap | "Although [PRIOR_WORK], [GAP]." | "Although genomic studies have revealed extensive diversity, the adaptive significance remains poorly understood." |
| C2 | Direct-Gap | "However, [GAP_STATEMENT]." | "However, little is known about the temporal dynamics of this process." |
| C3 | Despite-Gap | "Despite [EXISTING_KNOWLEDGE], [GAP]." | "Despite extensive monitoring, the sources of contamination remain unidentified." |
| C4 | No-Study-Gap | "To date, no study has [UNADDRESSED_TOPIC]." | "To date, no study has examined the combined effects of temperature and pH on dissolution rates." |
| C5 | Remaining-Question | "[QUESTION] remains poorly understood / unresolved / unclear." | "The mechanism driving seasonal fluctuations remains poorly understood." |
| C6 | Limited-Knowledge | "Our understanding of [TOPIC] is limited by [CONSTRAINT]." | "Our understanding of deep groundwater dynamics is limited by the scarcity of monitoring data." |

#### D. Purpose/Hypothesis Frames

| # | Frame Name | Abstracted Template | Example |
|---|-----------|---------------------|---------|
| D1 | Here-We | "Here, we [ACTION] to [PURPOSE]." | "Here, we combine geochemical and isotopic data to identify recharge sources." |
| D2 | Aim-Statement | "The aim/objective of this study was to [PURPOSE]." | "The aim of this study was to quantify groundwater recharge rates." |
| D3 | We-Sought | "We sought to [determine/investigate/test] [RESEARCH_QUESTION]." | "We sought to determine whether land-use change affects groundwater quality." |
| D4 | Hypothesis | "We hypothesize/hypothesized that [HYPOTHESIS]." | "We hypothesized that isotopic signatures would differ between recharge zones." |
| D5 | This-Study | "This/The present study [ACTION] [PURPOSE]." | "This study investigates the spatial distribution of trace elements in shallow aquifers." |
| D6 | To-Address | "To address [GAP], we [ACTION]." | "To address this knowledge gap, we conducted a comprehensive sampling campaign." |

#### E. Method/Procedure Frames

| # | Frame Name | Abstracted Template | Example |
|---|-----------|---------------------|---------|
| E1 | Passive-Procedure | "[SAMPLE] was/were [PROCEDURE] using [INSTRUMENT/METHOD]." | "Water samples were collected using pre-cleaned HDPE bottles." |
| E2 | To-Purpose-Action | "To [PURPOSE], [SAMPLE] was/were [PROCEDURE]." | "To determine major ion concentrations, samples were analyzed using IC." |
| E3 | Following-Protocol | "Following [PROTOCOL/AUTHOR], [PROCEDURE]." | "Following EPA Method 200.8, trace elements were measured by ICP-MS." |
| E4 | Condition-Detail | "[PROCEDURE] was performed at [CONDITION]." | "Digestion was performed at 180°C for 12 hours in sealed Teflon vessels." |
| E5 | Tool-Specification | "[ANALYSIS] was conducted using [SOFTWARE] (version [VER])." | "Statistical analyses were conducted using R (version 4.1.0)." |
| E6 | Quantitative-Method | "[QUANTITY] of [SAMPLE] were [PROCEDURE] at [INTERVAL/LOCATION]." | "A total of 200 samples were collected at 50 monitoring wells over 12 months." |
| E7 | Quality-Statement | "[QUALITY_MEASURE] was assessed by [METHOD], yielding [RESULT]." | "Analytical precision was assessed by replicate analysis, yielding RSD < 5%." |

#### F. Result Reporting Frames

| # | Frame Name | Abstracted Template | Example |
|---|-----------|---------------------|---------|
| F1 | Analysis-Revealed | "[ANALYSIS] revealed/showed that [FINDING] [STAT]." | "ANOVA revealed that concentrations differed significantly among sites (F₃,₁₇₆ = 12.4, P < 0.001)." |
| F2 | Variable-Pattern | "[VARIABLE] [DIRECTION] in [GROUP/CONDITION] compared to [COMPARISON] [STAT]." | "Nitrate concentrations were significantly higher in agricultural areas compared to forested areas (P < 0.01)." |
| F3 | Range-Report | "[VARIABLE] ranged from [MIN] to [MAX], with a mean of [MEAN] [STAT]." | "δ¹⁸O values ranged from −12.3‰ to −6.8‰, with a mean of −9.5 ± 1.2‰." |
| F4 | Correlation | "A significant [DIRECTION] correlation was found between [VAR_A] and [VAR_B] [STAT]." | "A significant positive correlation was observed between Cl⁻ and Na⁺ (r = 0.92, P < 0.001)." |
| F5 | Figure-Reference | "As shown in [FIGURE], [FINDING]." | "As shown in Fig. 3, the seasonal pattern was most pronounced at downstream sites." |
| F6 | Proportion-Report | "[QUANTITY] of [TOTAL] [VERB] [CHARACTERISTIC]." | "Approximately 65% of the samples exceeded the WHO drinking water guideline." |
| F7 | Trend-Report | "[VARIABLE] [DIRECTION] [TEMPORAL/SPATIAL] [STAT]." | "Dissolved oxygen decreased progressively with depth (R² = 0.78)." |
| F8 | Group-Comparison | "[GROUP_A] exhibited [CHARACTERISTIC_A], whereas [GROUP_B] showed [CHARACTERISTIC_B]." | "Shallow wells exhibited oxic conditions, whereas deep wells showed anoxic signatures." |
| F9 | No-Significant | "No significant difference/correlation was found between [A] and [B] [STAT]." | "No significant difference was observed between the two sampling periods (P = 0.34)." |

#### G. Interpretation/Inference Frames

| # | Frame Name | Abstracted Template | Example |
|---|-----------|---------------------|---------|
| G1 | Results-Suggest | "[AGENT] suggest(s)/indicate(s) that [INTERPRETATION]." | "These results suggest that agricultural runoff is the primary source of nitrate contamination." |
| G2 | Attributed-To | "[OBSERVATION] may be attributed to / can be explained by [MECHANISM]." | "The enriched δ¹⁸O values may be attributed to evaporative fractionation." |
| G3 | Consistent-With | "[FINDING] is consistent with [MECHANISM/THEORY]." | "This pattern is consistent with mixing between two distinct end-members." |
| G4 | Likely-Due-To | "[OBSERVATION] is likely due to [CAUSE]." | "The elevated concentrations are likely due to dissolution of carbonate minerals." |
| G5 | Possible-Mechanism | "One possible explanation is that [MECHANISM]." | "One possible explanation is that reducing conditions promote the release of arsenic from iron oxides." |
| G6 | Supported-By | "This interpretation is supported/corroborated by [EVIDENCE]." | "This interpretation is supported by the strong correlation between Fe and As (r = 0.89)." |
| G7 | Taken-Together | "Taken together, these [FINDINGS] suggest/indicate [CONCLUSION]." | "Taken together, these geochemical indicators suggest a deep circulation pathway." |

#### H. Comparison/Contrast Frames

| # | Frame Name | Abstracted Template | Example |
|---|-----------|---------------------|---------|
| H1 | Compared-To | "Compared to [COMPARISON], [SUBJECT] [DIFFERENCE]." | "Compared to the upstream sites, downstream samples showed 3-fold higher turbidity." |
| H2 | While-Contrast | "While [FINDING_A], [FINDING_B]." | "While shallow groundwater was dominated by Ca-HCO₃ type, deep groundwater was Na-Cl type." |
| H3 | In-Contrast | "In contrast to [A], [B] [DIFFERENCE]." | "In contrast to the dry season, wet season samples exhibited depleted isotopic compositions." |
| H4 | Unlike-Previous | "Unlike [PREVIOUS_STUDY/RESULT], our [FINDING]." | "Unlike Kim et al. (2019), our results show no significant seasonal variation." |
| H5 | Similarly | "Similarly, [PARALLEL_FINDING] [LITERATURE]." | "Similarly, elevated arsenic concentrations have been reported in alluvial aquifers of Southeast Asia (Berg et al., 2007)." |
| H6 | Higher-Lower | "[VARIABLE] was [QUANTITY] [higher/lower] in [A] than in [B]." | "Mean nitrate was 2.5 times higher in irrigated areas than in non-irrigated areas." |

#### I. Concession/Limitation Frames

| # | Frame Name | Abstracted Template | Example |
|---|-----------|---------------------|---------|
| I1 | Although-However | "Although [ACKNOWLEDGED], [MAIN_POINT]." | "Although our dataset is limited to one year, the observed trends are consistent across seasons." |
| I2 | Limitation-Acknowledge | "A limitation of this study is [LIMITATION]." | "A limitation of this study is the absence of continuous monitoring data." |
| I3 | Should-Be-Noted | "It should be noted that [CAVEAT]." | "It should be noted that these results may not be generalizable to other geological settings." |
| I4 | Despite-Still | "Despite [LIMITATION], [POSITIVE_STATEMENT]." | "Despite the relatively small sample size, the statistical relationships were robust." |
| I5 | Cannot-Rule-Out | "We cannot rule out the possibility that [ALTERNATIVE]." | "We cannot rule out the possibility that anthropogenic inputs contribute to the observed signal." |
| I6 | Beyond-Scope | "[TOPIC] is beyond the scope of this study." | "A detailed analysis of microbial processes is beyond the scope of this study." |

#### J. Implication/Future Frames

| # | Frame Name | Abstracted Template | Example |
|---|-----------|---------------------|---------|
| J1 | Implications-For | "These findings have implications for [APPLICATION]." | "These findings have important implications for groundwater management in coastal areas." |
| J2 | Could-Be-Used | "[FINDING/METHOD] could be used to [APPLICATION]." | "This isotopic approach could be used to trace pollution sources in similar geological settings." |
| J3 | Future-Should | "Future studies should [RECOMMENDATION]." | "Future studies should incorporate longer time series to capture inter-annual variability." |
| J4 | Further-Needed | "Further research is needed to [PURPOSE]." | "Further research is needed to quantify the contribution of each recharge source." |
| J5 | Highlight-Need | "Our results highlight the need for [ACTION]." | "Our results highlight the need for more comprehensive monitoring networks." |
| J6 | Provides-Framework | "This study provides a framework for [APPLICATION]." | "This study provides a framework for assessing groundwater vulnerability in karst systems." |

#### K. Causal/Conditional Frames

| # | Frame Name | Abstracted Template | Example |
|---|-----------|---------------------|---------|
| K1 | Resulting-In | "[CAUSE], resulting in [EFFECT]." | "Intensive irrigation lowers the water table, resulting in land subsidence." |
| K2 | If-Then | "If [CONDITION], [CONSEQUENCE]." | "If recharge rates continue to decline, aquifer depletion is expected within decades." |
| K3 | This-Led-To | "[EVENT/PROCESS] led to [OUTCOME]." | "Prolonged drought led to a significant decrease in baseflow contributions." |
| K4 | Due-To | "[EFFECT] is/was due to [CAUSE]." | "The high salinity was due to seawater intrusion along the coastal margin." |
| K5 | Thereby | "[ACTION], thereby [RESULT]." | "We normalized the data to unit variance, thereby eliminating scale effects." |

#### L. Synthesis/Conclusion Frames

| # | Frame Name | Abstracted Template | Example |
|---|-----------|---------------------|---------|
| L1 | In-Summary | "In summary, [MAIN_CONCLUSION]." | "In summary, our results demonstrate that land-use change is the dominant driver of nitrate pollution." |
| L2 | This-Study-Shows | "This study [demonstrates/reveals/confirms] that [CONCLUSION]." | "This study demonstrates the utility of multi-isotope approaches for source apportionment." |
| L3 | Overall | "Overall, [SYNTHESIS]." | "Overall, the geochemical evidence points to a dual recharge mechanism." |
| L4 | Collectively | "Collectively, [EVIDENCE] [suggest/indicate] [CONCLUSION]." | "Collectively, these lines of evidence indicate that the aquifer is recharged primarily from the mountain front." |

#### Z. Uncategorized

Unique sentence forms that do not fit categories A–L.
**This category MUST be used to ensure zero omissions. Every sentence form must be captured.**

| # | Abstracted Template | Rhetorical Function (free description) | Original Sentence | Section | Source |
|---|---------------------|----------------------------------------|-------------------|---------|--------|

---

### Extraction Procedure

```
1. Read all sentences section by section, in order
2. For each sentence:
   a. Find the best-matching frame type from the reference taxonomy (A–L)
   b. If no match exists, collect under Z (Uncategorized) with free-form rhetorical function description
   c. Record the original sentence verbatim AND create the abstracted [SLOT] template
   d. Assign [P#-S#] source tag
3. If multiple sentences match the same frame type, collect ALL of them (exhaustive collection)
4. If a single sentence combines two or more frames (compound frame),
   classify under the primary frame and note the compound structure in remarks
```

### Output: Sentence Frame Catalog

**Organize output by section.**

```markdown
## E. Sentence Frame Catalog

### Introduction Frames

| # | Frame Type | Abstracted Template | Original Sentence | Source |
|---|-----------|---------------------|-------------------|--------|
| 1 | A1 General-Importance | "[TOPIC] is [SIGNIFICANCE] for [CONTEXT]." | "Groundwater is a critical resource for drinking water supply in arid regions." | [P1-S1] |
| 2 | B2 Info-Prominent | "[CLAIM] [LITERATURE]." | "Seasonal variation in isotopic composition has been widely documented (1–5)." | [P1-S3] |
| 3 | C1 Concessive-Gap | "Although [PRIOR_WORK], [GAP]." | "Although extensive monitoring has been conducted, the sources remain unidentified." | [P3-S1] |
| 4 | D1 Here-We | "Here, we [ACTION] to [PURPOSE]." | "Here, we combine hydrochemical and isotopic approaches to delineate recharge zones." | [P5-S1] |
| 5 | Z (Uncategorized) | "[AGENT] [VERB] [OBJECT] across [RANGE], highlighting [SIGNIFICANCE]." | "Recent droughts have affected groundwater levels across the entire basin, highlighting the vulnerability of these systems." | [P2-S4] |

### Methods Frames
[Same format]

### Results Frames
[Same format]

### Discussion Frames
[Same format]
```

### Additional Output: Frame Distribution Summary

```markdown
### Frame Distribution Summary

| Frame Category | Introduction | Methods | Results | Discussion | Total |
|---------------|-------------|---------|---------|------------|-------|
| A. Background | 8 | 0 | 0 | 1 | 9 |
| B. Literature Ref | 6 | 2 | 0 | 5 | 13 |
| C. Gap/Problem | 4 | 0 | 0 | 0 | 4 |
| D. Purpose | 3 | 0 | 0 | 0 | 3 |
| E. Method | 0 | 25 | 0 | 0 | 25 |
| F. Result | 0 | 0 | 22 | 3 | 25 |
| G. Interpretation | 0 | 0 | 2 | 12 | 14 |
| H. Comparison | 1 | 0 | 5 | 6 | 12 |
| I. Concession | 1 | 0 | 0 | 4 | 5 |
| J. Implication | 0 | 0 | 0 | 5 | 5 |
| K. Causal | 0 | 1 | 2 | 3 | 6 |
| L. Synthesis | 0 | 0 | 1 | 3 | 4 |
| Z. Uncategorized | 2 | 1 | 1 | 0 | 4 |
| **Total** | **25** | **29** | **33** | **42** | **129** |
```

---

## PHASE 5: Synthesis & Save

### 5a. Synthesis Summary

```markdown
## F. Analysis Summary

### Structure Statistics
- **Total sections**: 4 (Introduction, Methods, Results, Discussion)
- **Total subsections**: 14
- **Total paragraphs**: 32 (P1–P32)
- **Total sentences**: 158

### Logic Pattern Summary

#### Inter-Paragraph Key Patterns
- Introduction: Background → Literature → Gap → Purpose → Scope (5-step progression)
- Methods: Primarily sequential (Sequence)
- Results: Overview → Detail → Comparison → Summary (General-to-Specific)
- Discussion: Interpretation → Comparison → Limitation → Implication

#### Intra-Paragraph Key Patterns
- Most frequent sentence role: Evidence (23%), Topic (15%), Claim (14%)
- Most frequent sentence relation: Support (28%), Elaboration (19%), Addition (15%)

### Sentence Frame Key Findings
- Most frequent frames: F1 Analysis-Revealed (Results), E1 Passive-Procedure (Methods)
- Section-specific frames: C1–C6 appear only in Introduction, F1–F9 concentrated in Results
- Uncategorized frames: 4 (3.1% of total)

### Notable Observations
- [Describe any unique argument patterns or sentence forms specific to this paper]
```

### 5b. Final File Structure

The complete markdown file structure:

```markdown
# Logic Analysis: {Author} et al. ({Year})

## A. Paper Information
- **Title**: {title}
- **Journal**: {journal}
- **Year**: {year}
- **Field**: {field}

## B. Structure Map
[Phase 1 output]

## C. Inter-Paragraph Logic
[Phase 2 output — per-section tables + flow diagrams]

## D. Intra-Paragraph Logic
[Phase 3 output — per-paragraph tables + logic chains]

## E. Sentence Frame Catalog
[Phase 4 output — per-section frame tables + distribution summary]

## F. Analysis Summary
[Phase 5a output]

---
**Extracted by**: Meta_researcher / extraction-logic
**Date**: {date}
```

### 5c. index.md Update

```markdown
# Logic Index: {topic}

## Analyzed Papers

| Author | Year | Title | Journal | Paragraphs | Sentences | File |
|--------|------|-------|---------|------------|-----------|------|
| Weber et al. | 2021 | [title] | GCA | 32 | 158 | [link](Weber2021_logic.md) |

## Statistics
- Total papers: N
- Last added: {date}
```

---

## Validation Checklist

Verify before saving:

- [ ] Every paragraph has a P# number and function tag assigned
- [ ] Every sentence has an S# number and role tag assigned (for detailed-analysis paragraphs)
- [ ] Inter-paragraph logical relations recorded for all adjacent pairs
- [ ] Sentence frames exhaustively collected (including uncategorized)
- [ ] All original text is verbatim (exact quotes)
- [ ] Every item has a `[P#-S#]` source tag
- [ ] Distribution summary table totals match actual sentence counts
- [ ] Structure tree paragraph ranges match actuals

---

**Template Version**: 1.0.0
