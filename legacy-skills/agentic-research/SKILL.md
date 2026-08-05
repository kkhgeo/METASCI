---
name: agentic-research
description: >
  Kosmos-inspired agentic research framework for autonomous data-driven scientific discovery.
  Use this skill when the user wants to: conduct iterative data analysis with literature review,
  perform multi-cycle hypothesis generation and testing on datasets, run autonomous exploratory
  data analysis (EDA) with literature grounding, build an AI research agent or scientific workflow,
  create a structured research pipeline that combines code execution with literature search,
  or any task involving "agentic research", "autonomous discovery", "iterative analysis",
  "hypothesis-driven exploration", or "research agent". Also trigger when users mention
  "Kosmos-like", "AI scientist", or "research loop". This skill is especially relevant for
  geoscience, environmental science, bioinformatics, and any data-rich scientific domain.
---

# Agentic Research Framework

An autonomous, iterative research system inspired by Kosmos (Mitchener et al., 2025).
Given a **research objective** and a **dataset**, this framework performs cycles of:

1. **Data Analysis** → exploratory & hypothesis-driven code execution
2. **Literature Search** → web search grounded in emerging findings
3. **World Model Update** → structured state tracking across cycles
4. **Report Generation** → traceable, cited scientific reports

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                  ORCHESTRATOR                     │
│  (reads objective + dataset → manages cycles)     │
├─────────────┬──────────────┬────────────────────┤
│  Data Agent │  Lit Agent   │   World Model      │
│  (Python/R) │  (web_search)│   (JSON state)     │
│  code exec  │  paper fetch │   hypotheses       │
│  results    │  evidence    │   findings         │
└─────────────┴──────────────┴────────────────────┘
         ↓              ↓              ↓
    ┌─────────────────────────────────────┐
    │         REPORT GENERATOR            │
    │   (traceable claims + citations)    │
    └─────────────────────────────────────┘
```

## Quick Start

### Step 1: Initialize the World Model

```bash
python /path/to/skill/scripts/init_world_model.py \
  --objective "Your research objective here" \
  --dataset /path/to/dataset \
  --output /home/claude/research_session/
```

Or manually create the world model JSON (see templates/world_model_template.json).

### Step 2: Run the Research Cycle

Each cycle follows this sequence:

1. **Read** the current world model state
2. **Plan** tasks for this cycle (2-5 data analysis tasks + 1-3 literature tasks)
3. **Execute** tasks (write & run Python/R scripts, perform web searches)
4. **Update** the world model with results
5. **Evaluate** whether the objective is met or more cycles are needed

### Step 3: Generate Report

After cycles complete, synthesize findings into a traceable report.

---

## Detailed Workflow

### Phase 1: Session Initialization

Before any analysis, Claude must:

1. **Parse the research objective** — Extract key questions, scope, domain
2. **Profile the dataset** — Run `scripts/profile_dataset.py` to get:
   - Schema, dimensions, data types, missing values
   - Basic descriptive statistics
   - Initial quality assessment
3. **Initialize the world model** — Create the JSON state file
4. **Plan the first cycle** — Generate 3-5 initial analysis tasks

### Phase 2: Iterative Discovery Cycles

Each cycle has four phases executed in order:

#### 2a. Task Planning (from World Model)

Read the world model and generate tasks. Tasks are of two types:

**Data Analysis Tasks** — Each task produces a Python/R script that:
- Has a clear hypothesis or question
- Writes results to a structured output
- Logs all statistical tests and p-values
- Saves figures with descriptive filenames

**Literature Search Tasks** — Each task:
- Searches for papers related to emerging findings
- Validates or challenges current hypotheses
- Identifies known mechanisms or prior work

#### 2b. Data Analysis Execution

For each data analysis task:

```python
# Template structure for analysis scripts
"""
Task ID: {task_id}
Cycle: {cycle_number}
Question: {specific_question}
Hypothesis: {hypothesis_if_any}
"""

import pandas as pd
import numpy as np
from scipy import stats
# ... analysis code ...

# REQUIRED: structured output
results = {
    "task_id": task_id,
    "finding": "description of what was found",
    "evidence": "statistical evidence (test, p-value, effect size)",
    "figures": ["path/to/fig1.png"],
    "confidence": "high|medium|low",
    "next_questions": ["follow-up question 1", "..."]
}
```

#### 2c. Literature Search Execution

For each literature search task, use web_search with targeted queries:
- Search for key terms from data findings
- Fetch and read relevant papers
- Extract supporting/contradicting evidence
- Record full citations

#### 2d. World Model Update

After all tasks complete, update the world model:

```json
{
  "cycle_N": {
    "data_findings": [...],
    "literature_evidence": [...],
    "new_hypotheses": [...],
    "rejected_hypotheses": [...],
    "next_cycle_tasks": [...]
  }
}
```

### Phase 3: Convergence & Report

After cycles complete (max cycles reached or objective satisfied):

1. **Synthesize** — Identify the 2-4 strongest discovery narratives
2. **Trace** — Every claim must link to a specific analysis script or paper
3. **Generate** — Create the report using `references/report_template.md`

---

## World Model Schema

The world model is the critical component. Read `references/world_model_spec.md` for full schema.

Key sections:
- `metadata` — session info, objective, dataset path
- `dataset_profile` — schema, statistics, quality notes
- `cycles[]` — array of cycle records
- `hypotheses[]` — living list with status (active/supported/rejected)
- `findings[]` — validated discoveries with evidence chains
- `task_queue` — planned tasks for next cycle

---

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `scripts/init_world_model.py` | Initialize session and world model |
| `scripts/profile_dataset.py` | Automated dataset profiling |
| `scripts/update_world_model.py` | Safely update world model state |
| `scripts/generate_report.py` | Compile findings into report |
| `scripts/validate_claims.py` | Check claim-evidence traceability |

---

## Key Principles (from Kosmos)

1. **Traceability** — Every claim cites code or literature. No orphan statements.
2. **Structured State** — The world model prevents context drift across cycles.
3. **Parallel Exploration** — Multiple hypotheses pursued simultaneously.
4. **Iterative Deepening** — Each cycle builds on prior findings.
5. **Conservative Claims** — Distinguish data-supported from interpretive statements.
6. **Scientist-in-the-Loop** — Human reviews findings at checkpoints.

---

## Domain Adaptations

This framework is domain-agnostic. For specific domains, read:
- `references/domain_geoscience.md` — Geochemistry, environmental data
- `references/domain_omics.md` — Genomics, proteomics, metabolomics
- `references/domain_materials.md` — Materials science datasets

---

## Limitations & Guardrails

- **Interpretation accuracy**: Kosmos showed 57.9% accuracy on interpretation statements.
  Always flag interpretive leaps explicitly.
- **Statistical vs. scientific significance**: A p < 0.05 result is not automatically interesting.
  Evaluate effect sizes and domain relevance.
- **Dataset size**: Best suited for structured tabular data up to ~1GB.
- **Stochastic variation**: Multiple runs may yield different findings. Consider running
  2-3 independent sessions for critical objectives.
