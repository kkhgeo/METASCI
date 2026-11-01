# Section Manual: Methods

> **Theoretical basis:** Lim (2006), Kanoksilapatham (2005), Day & Gastel (2022)

---

## Rhetorical Function

Methods must satisfy two simultaneous demands: **reproducibility** (enough detail for a competent reader to replicate the study) and **justification** (enough argumentation to convince the reader the design is sound). Competent writers satisfy the first. Expert writers satisfy both.

The Methods section speaks to a **skeptical reader** who will ask: Why this approach? Why this sample size? Why this instrument? Every non-obvious choice needs justification, not just description.

---

## Move Structure (Lim 2006)

| Move | Function |
|---|---|
| **M1: Describe materials/participants/data** | Who/what was studied; sampling logic |
| **M2: Describe procedures** | What was done, in what order |
| **M3: Describe analytical approach** | How data were processed, modeled, or analyzed |
| **M4: Justify methodological choices** | Why these choices are appropriate for the research question |

**M4 is the expert differentiator.** It is frequently omitted by competent writers and systematically present in published expert work. It appears as embedded clauses, parenthetical justifications, or brief sub-paragraphs following a procedural description.

---

## Agent Checklist

### Reproducibility
- [ ] Are all materials, instruments, and software specified with sufficient precision (version numbers, manufacturer, catalog numbers where relevant)?
- [ ] Are quantities, concentrations, temperatures, durations, and intervals stated explicitly?
- [ ] Is the sequence of steps clear — would a competent researcher be able to replicate without ambiguity?
- [ ] Are statistical tests named, and are their assumptions met (stated or defensible)?

### Justification (M4)
- [ ] Are non-obvious methodological choices justified?
- [ ] Is the sample size justified (power analysis, resource constraints, precedent in the literature)?
- [ ] Is the analytical approach connected to the research question?
- [ ] Where established methods are cited, is the citation accurate and appropriate?

### Design declaration
- [ ] Does the section open by naming the study design (observational/experimental, prospective/retrospective, randomized or not, controlled, blinded, crossover)? A reader should not have to infer the design from the procedures.
- [ ] Where the design departs from field convention, is the departure justified by citation, guideline, or the specific context that required it? Procedures listed with no rationale for an unusual choice is an M4 failure.
- [ ] Are the primary and secondary outcome variables identified, with the measurement used for each? When it is unclear which result is the main one, the whole interpretation is unanchored.

### Statistical reporting completeness
Beyond naming the tests (Reproducibility, above):
- [ ] Is the data-presentation convention declared (mean ± SD / median [IQR] / n (%))?
- [ ] Is the test matched to the variable type, and stated as such?
- [ ] For multivariate models, are the variables entered into the model listed?
- [ ] Is the significance threshold stated, and any correction for multiple comparisons?
- [ ] **Are subgroup analyses declared as pre-specified?** An analysis presented as planned when it was exploratory is a reporting-integrity issue, not a style issue — flag HIGH.

### Ethics and registration
Applies to research involving humans, animals, identifiable data, or clinical intervention. Skip entirely for purely computational, instrumental, or secondary-data work rather than flagging its absence.
- [ ] Is ethics committee / IRB approval stated (or the reason none was required)?
- [ ] Is informed consent addressed where human participants are involved?
- [ ] For trials, is the registry and registration number given?
- [ ] Are data availability and any use restrictions noted where the journal requires it?

> Approval numbers, registry IDs, and consent statements are **facts, not prose**. If they are missing, flag the omission — never draft a plausible-looking one into a rewrite candidate.

### Organization and logic
- [ ] Is information presented in the order it was performed (chronological logic)?
- [ ] Are subsections used logically — do they correspond to conceptually distinct phases?
- [ ] Is there any procedural information buried in Results that belongs here?

### Tense and voice
- [ ] Is the entire section in past tense?
- [ ] Is passive voice used appropriately (when the procedure matters more than who performed it)?
- [ ] Is active voice used when the agent's decision matters ("We selected sites based on...")?

---

## Common Expert-Level Problems

### 1. Description without justification
❌ "Samples were collected at 10 cm depth intervals to 1 m."
✅ "Samples were collected at 10 cm depth intervals to 1 m to capture both the active layer and the upper permafrost horizon, which prior work has identified as the zone of maximum carbon turnover (Smith et al., 2020)."

### 2. Under-specified statistical analysis
❌ "Data were analyzed using R."
✅ "Mixed-effects models were fitted using the lme4 package in R (v.4.2.1; Bates et al., 2015), with site as a random effect to account for spatial autocorrelation. Model fit was assessed by comparing AIC values."

### 3. Methods that belong in Introduction
Motivation for the overall study design goes in the Introduction. Methods justify specific choices within a design that has already been framed.

### 4. Results embedded in Methods
Any quantitative outcome ("which yielded 85% recovery") should appear in Results, not here.

### 5. Overly long procedural lists
Procedures that have been published before should be cited, not described in full: "Extraction followed the method of Jones et al. (2019), with minor modifications (see Supplementary Materials)."

---

## Verb and Voice Patterns

| Purpose | Pattern | Example |
|---|---|---|
| Standard procedure | Passive past | "Samples were digested for 24 h at 60°C" |
| Decision requiring justification | Active past | "We chose ICP-MS over ICP-OES because..." |
| Reference to established method | Active past + citation | "We applied the protocol described by..." |
| Statistical test | Active or passive past | "We tested / were tested using a two-tailed t-test" |

---

## Subsection Organization (typical)

1. **Study site / Data sources** — where, when, what conditions
2. **Sample collection / Experimental design** — how materials were obtained
3. **Laboratory / Computational procedures** — what was done to them
4. **Data processing and quality control** — how raw data were treated
5. **Statistical / Analytical methods** — how patterns were identified
