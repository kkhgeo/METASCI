# Report Template

Use this template structure when generating final research reports.
The report generator script (`generate_report.py`) follows this structure.

## Required Sections

### 1. Header
- Research objective (verbatim from session)
- Session metadata (date, cycles, traceability score)

### 2. Dataset Description
- Source, dimensions, key variables
- Preprocessing applied
- Quality notes

### 3. Executive Summary
- 2-3 paragraph overview of key discoveries
- Number of findings, hypotheses tested, cycles completed

### 4. Discovery Narratives (2-4)
Each discovery narrative follows this structure:

```markdown
## Discovery N: [Title]

### Background
Brief literature context (with citations)

### Analysis
Step-by-step description of analyses performed:
- What was tested
- Statistical methods used
- Key results with effect sizes and p-values
- [Figure reference with caption]

> **Evidence**: [test statistic, p-value, effect size]
> **Source**: `scripts/cN_da_XX.py`

### Interpretation
What the results mean in domain context.

> ⚠ **Interpretation confidence**: [high/medium/low]
> This is an interpretive statement synthesizing data and literature.

### Supporting Literature
- Citation 1: relevance
- Citation 2: relevance
```

### 5. Methodology
- Framework description
- Cycle-by-cycle summary
- Tools and packages used

### 6. Hypothesis Inventory
Table of all hypotheses with status

### 7. Limitations
- Data limitations
- Analytical limitations
- Interpretive caveats

## Citation Rules

Every statement in the report must be one of three types:

1. **Data Analysis** (`📊`): Directly supported by code output
   - Must link to script path
   - Must include statistical evidence

2. **Literature Review** (`📚`): Supported by published source
   - Must include full citation
   - Must include DOI or URL where possible

3. **Interpretation** (`💡`): Synthesis of data + literature
   - Must explicitly label as interpretation
   - Must reference the data findings and literature it draws from
   - Must include confidence level

## Confidence Levels

- 🟢 **High**: Statistically robust (p < 0.01), large effect size, supported by multiple independent analyses
- 🟡 **Medium**: Statistically significant (p < 0.05), moderate effect size, or supported by single analysis
- 🔴 **Low**: Suggestive but not statistically robust, or based primarily on interpretation
