# Cross-Section: Quantitative & Citation Integrity

> **Theoretical basis:** Sainani (Stanford, *Writing in the Sciences*), CONSORT/STROBE/ARRIVE reporting standards, retraction-pattern literature

---

## Framing Principle

Numbers and citations are the **load-bearing structure** of a scientific paper. A clarity issue slows the reader; a numerical inconsistency or a misattributed citation calls the entire result into question. This file targets failures of internal numerical consistency and citation discipline — the kinds of problems peer reviewers flag with the highest weight and the kinds that, if missed, become correction notices or retractions.

This file should be loaded:
- **Mode 1 (full draft):** Always, as a top-level audit
- **Mode 2 (section):** When the section is Abstract, Results, Results & Discussion, or has tables/figures
- **Mode 3 (paragraph):** When the paragraph contains numbers or citations

It complements `agent_b.md` (which handles citation existence) by adding **numeric cross-checking** and **secondary-source flagging**.

---

## 1. Numerical Consistency Checklist

The agent must verify, where the relevant material is available in context:

### 1a. Sample size (N) consistency

- N reported in the **Abstract** matches N in **Methods**
- N in Methods matches N in **Table 1** (sample characteristics)
- Subgroup Ns sum to the total N (no dropped participants unsplained)
- N in **Results** statements ("Among the 120 participants...") matches the source table

❌ Abstract: "We analyzed data from 120 participants."
❌ Table 1: "Total: 125"
❌ Results: "Of the 124 participants who completed..."

The reader cannot tell which number is correct. Flag as **CRITICAL**.

### 1b. Percentage / proportion consistency

- Percentages in **Results** text match the raw counts in tables
- Percentages sum correctly (allow for ±1% rounding; flag larger gaps)
- Percentages reported as "approximately X%" match the actual rounded value

❌ "Approximately 60% of samples (n = 38 of 100) showed elevated SOC."
   60% of 100 = 60, not 38. Flag as **CRITICAL**.

✅ "38% of samples (n = 38 of 100) showed elevated SOC."

### 1c. Significant figures and precision

- Reported precision matches measurement precision
- A measurement reported as "12.3 ± 0.4" should not appear elsewhere as "12.34"
- p-values reported consistently (one decimal place: p = 0.03; not p = 0.034 in one place and p = 0.03 in another for the same test)
- Units are explicit and consistent across text/tables/figures (mg/g not mg g⁻¹ in some places)

### 1d. Figure ↔ Table ↔ Text agreement

- A value plotted in Figure 3 matches the corresponding row in Table 2
- Trend statements in text ("X increased by 40%") are consistent with figure axes
- Error bars / confidence intervals reported in text match the figure caption

### 1e. Statistical reporting completeness

- Effect sizes reported alongside p-values where the field expects it (e.g., Cohen's d, η², r)
- Confidence intervals reported, not only p-values, where the field expects them
- Test statistic + degrees of freedom + p-value triplet complete (e.g., t(118) = 2.34, p = 0.02)
- Multiple comparisons correction noted where applicable

---

## 2. Citation Integrity — The "Telephone Game" Audit

A statistic stated as established fact, but cited only through a **secondary source** (review, textbook, conference report), is at high risk of distortion. The original numbers may have a narrower scope, different methods, or different population than the secondary citation implies.

### Flag pattern

When the agent encounters:

```
"<Specific quantitative claim>" [<Review citation>]
```

…and the citation is a review article, textbook, or meta-analysis, the agent flags:

```
**[2차 인용 경고]** 이 통계는 [Review (Year)]에서 인용되었습니다.
원 출처를 확인하고 직접 인용을 권장합니다.
원 연구의 표본·방법이 본 논문 맥락과 일치하는지 확인 필요.
```

### Specific patterns to watch

- "Up to X% of patients [Review, Year]" — the X% likely came from one specific study within that review with narrower scope
- "It has been estimated that [Textbook]" — textbooks rarely report primary measurements
- "Globally, X tonnes of [Y] are emitted [IPCC report]" — flag if the statement makes a specific quantitative claim attributed only to a synthesis report; the agent should suggest that the user trace the chain of citation to the primary measurement

### Cross-check with knowledge_bank

If the paper's `knowledge_bank.sources[]` contains the primary studies behind a flagged secondary citation, the agent recommends switching to the primary citations.

### Self-citation chains

A statistic cited to a previous paper by the same author group, which in turn cites a previous paper by the same group, is a circular citation chain. Flag with **MEDIUM** severity and note: "동일 저자군 자가 인용 체인 — 원 1차 자료 추적 권장."

---

## 3. Citation-Statement Alignment

The cited claim should **match what the source actually says**. The agent cannot fully verify this without reading the source, but it can flag candidates:

### 3a. Overstatement of source

| Pattern | Likely problem |
|---|---|
| "X causes Y [Citation]" | Citation may show correlation, not causation |
| "X is universally observed [Citation]" | Single-study or small-N citations rarely justify "universally" |
| "Recent studies confirm [Single citation]" | One study is not "studies" |
| "X has been definitively shown [Hedged primary source]" | Primary source likely hedged the claim |

### 3b. Citation-claim mismatch

When a citation appears at the end of a sentence containing multiple claims, the agent flags ambiguity:
- Which claim does the citation support?
- Are all claims in the sentence covered by that single citation?

Suggest splitting cited claims for clarity, or repeating the citation: "X [Smith, 2019], and consequently Y [Jones, 2021]."

---

## 4. Unit and Notation Consistency

### Common drift

- SI vs imperial mixed within one paper
- Concentration units inconsistent (μM in Methods, μmol/L in Results)
- Temperature ° symbols inconsistent (°C, ℃, deg C)
- Date formats mixed (2024-01-15, January 15 2024, 15/01/2024)
- Gene/protein nomenclature inconsistent (italicization rules differ for gene vs protein)
- Species names inconsistent (full Latin first use, abbreviated thereafter — but consistent abbreviation)

### Acronym arithmetic (cross-link to `cohesion_flow.md` §6)

- Every acronym defined at first use in **Abstract** and again in **main text**
- Every acronym defined in each **table caption** and **figure caption** (readers do not read linearly)
- Acronym used consistently — no switching to the full form mid-paper without reason
- Non-standard acronyms minimized (only invent acronyms that the reader will encounter ≥5 times)

---

## 5. Reporting Standard Compliance

Where the paper's design has a published reporting standard, the agent flags missing elements:

| Study type | Standard | Common omissions |
|---|---|---|
| RCTs | CONSORT | flow diagram, randomization method, blinding details |
| Observational | STROBE | confounder list, sensitivity analyses |
| Animal experiments | ARRIVE | n per group, randomization, exclusion criteria |
| Systematic reviews | PRISMA | search dates, exclusion reasons, PRISMA flow diagram |
| Diagnostic accuracy | STARD | flow of patients, indeterminate results handling |
| Meta-analyses | MOOSE / PRISMA | heterogeneity assessment, publication bias check |

The agent does not enforce standards exhaustively; it flags missing high-impact elements when the paper's design clearly invokes one of these standards.

---

## 6. Agent Diagnostic Questions

For Mode 1 / Mode 2 (paper- and section-level):

- Does the Abstract's N match the Methods' N?
- Do percentages in Results sum correctly and match tables?
- Are units consistent throughout?
- Are acronyms defined where required?
- Does the paper's design invoke a reporting standard, and if so, are key elements present?

For Mode 3 (paragraph- and sentence-level):

- Does any number in this paragraph appear elsewhere with a different value?
- Is any quantitative claim cited only through a secondary source?
- Does the citation actually support the strength of the claim made?
- Are units and notation consistent with the rest of the paper?

---

## 7. Severity Calibration

| Severity | Trigger |
|---|---|
| **CRITICAL** | Numerical inconsistency that affects interpretation (N mismatch, % math error, units conflict) — must fix before submission |
| **HIGH** | Secondary citation for a quantitative claim that drives an argument; missing reporting standard element required by the paper's design |
| **MEDIUM** | Acronym defined inconsistently; minor sig-fig drift; self-citation chain |
| **LOW** | Polish-level notation drift (e.g., date format); single missing CI alongside p-value |

CRITICAL items take precedence over all stylistic findings in the deliberation Top-N priority sort (see `harness/deliberation.md`).
