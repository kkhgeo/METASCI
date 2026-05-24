# World Model Specification

The world model is a structured JSON file that maintains state across research cycles.
It is the key architectural innovation from Kosmos that prevents context drift and enables
coherent long-running research sessions.

## Full Schema

```json
{
  "version": "1.0",
  "metadata": {
    "session_id": "uuid",
    "created_at": "ISO-8601 timestamp",
    "updated_at": "ISO-8601 timestamp",
    "research_objective": "The full research objective text",
    "objective_keywords": ["keyword1", "keyword2"],
    "dataset_path": "/path/to/dataset",
    "max_cycles": 10,
    "current_cycle": 0,
    "status": "initializing|running|converged|completed"
  },

  "dataset_profile": {
    "filename": "data.csv",
    "format": "csv|xlsx|parquet|json",
    "rows": 10000,
    "columns": 50,
    "column_schema": [
      {
        "name": "column_name",
        "dtype": "float64|int64|object|datetime64|category",
        "missing_pct": 0.05,
        "unique_values": 100,
        "description": "Auto-generated or user-provided description"
      }
    ],
    "quality_notes": [
      "5% missing values in column X — imputation recommended",
      "Column Y has outliers beyond 3σ"
    ],
    "preprocessing_applied": [
      {"step": "log_transform", "columns": ["col1", "col2"], "reason": "right-skewed"}
    ]
  },

  "cycles": [
    {
      "cycle_number": 1,
      "started_at": "ISO-8601",
      "completed_at": "ISO-8601",
      "tasks_planned": [
        {
          "task_id": "c1_da_01",
          "type": "data_analysis",
          "question": "What are the dominant patterns in the dataset?",
          "hypothesis": null,
          "status": "completed",
          "script_path": "/session/scripts/c1_da_01_eda.py",
          "output_path": "/session/outputs/c1_da_01/"
        },
        {
          "task_id": "c1_lit_01",
          "type": "literature_search",
          "query": "metabolic pathways in hypothermia neuroprotection",
          "status": "completed",
          "papers_found": 5,
          "key_citations": []
        }
      ],
      "data_findings": [
        {
          "finding_id": "f001",
          "task_id": "c1_da_01",
          "statement": "Nucleotide metabolism is the most enriched pathway...",
          "evidence_type": "data_analysis",
          "statistical_evidence": "Fisher exact test, p = 0.003, OR = 4.2",
          "effect_size": "large",
          "confidence": "high",
          "figures": ["/session/figures/c1_pathway_enrichment.png"],
          "script_path": "/session/scripts/c1_da_01_eda.py"
        }
      ],
      "literature_evidence": [
        {
          "evidence_id": "e001",
          "task_id": "c1_lit_01",
          "claim": "Nucleotide salvage is energy-efficient during hypoxia",
          "source": "Thauerer et al., J Neurochem 2012",
          "url": "https://doi.org/...",
          "relevance": "Supports finding f001"
        }
      ],
      "new_hypotheses": [
        {
          "hypothesis_id": "h001",
          "statement": "Nucleotide salvage pathway is preferentially activated...",
          "source_findings": ["f001"],
          "source_literature": ["e001"],
          "status": "active",
          "tests_planned": ["Check precursor-product inversion pattern"]
        }
      ],
      "rejected_hypotheses": [],
      "cycle_summary": "Initial EDA revealed nucleotide metabolism as dominant pathway..."
    }
  ],

  "hypotheses": [
    {
      "hypothesis_id": "h001",
      "statement": "...",
      "created_cycle": 1,
      "status": "active|supported|rejected|refined",
      "supporting_evidence": ["f001", "e001"],
      "contradicting_evidence": [],
      "refined_to": null,
      "tests_completed": [],
      "confidence_score": 0.75
    }
  ],

  "findings": [
    {
      "finding_id": "f001",
      "statement": "...",
      "evidence_chain": [
        {"type": "data", "ref": "c1_da_01", "detail": "pathway enrichment"},
        {"type": "literature", "ref": "e001", "detail": "prior work confirms"}
      ],
      "category": "data_analysis|literature_review|interpretation",
      "confidence": "high|medium|low",
      "novel": true,
      "discovery_narrative": null
    }
  ],

  "task_queue": [
    {
      "task_id": "c2_da_01",
      "type": "data_analysis",
      "priority": "high",
      "question": "Do precursor bases decrease while products increase?",
      "hypothesis_id": "h001",
      "depends_on": ["c1_da_01"]
    }
  ],

  "discoveries": [
    {
      "discovery_id": "d001",
      "title": "Nucleotide salvage as neuroprotective mechanism",
      "narrative": "Extended text synthesizing multiple findings...",
      "supporting_findings": ["f001", "f003", "f005"],
      "supporting_literature": ["e001", "e004"],
      "figures": ["fig1.png", "fig2.png"],
      "confidence": "high",
      "novelty": "moderate"
    }
  ]
}
```

## Update Rules

1. **Append-only for findings** — Never delete a finding; mark as superseded if updated.
2. **Hypothesis lifecycle** — active → (supported | rejected | refined). Once rejected, never reactivated.
3. **Evidence chains must be complete** — Every finding references a script or paper.
4. **Cycle summaries are mandatory** — Each cycle ends with a human-readable summary.
5. **Task queue drives next cycle** — The orchestrator reads task_queue to plan.

## Querying the World Model

Common queries the orchestrator performs:

- **Active hypotheses**: `hypotheses where status == "active"`
- **Untested hypotheses**: `hypotheses where tests_completed is empty`
- **High-confidence findings**: `findings where confidence == "high"`
- **Evidence for a claim**: Follow `evidence_chain` links
- **What to do next**: Read `task_queue` sorted by priority

## Size Management

For long sessions (>10 cycles), the world model can grow large. Strategies:
- Keep full detail for last 3 cycles; summarize older cycles
- Archive completed hypothesis tests to a separate file
- Limit task_queue to top 10 priority items
