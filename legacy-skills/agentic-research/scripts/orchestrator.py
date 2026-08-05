#!/usr/bin/env python3
"""
Research Cycle Orchestrator

This script provides the orchestration logic for running research cycles.
It reads the world model, plans tasks, and provides structured prompts
for Claude to execute each task.

In Claude Code / claude.ai context, Claude itself acts as the executor:
- Reading this orchestrator's output to understand what to do next
- Writing and running analysis scripts
- Performing web searches for literature
- Updating the world model

Usage:
    python orchestrator.py --session /path/to/session/ --action [plan|status|next_task|checkpoint]
"""

import argparse
import json
import os
from datetime import datetime, timezone


def load_world_model(session_dir: str) -> dict:
    wm_path = os.path.join(session_dir, "world_model.json")
    with open(wm_path) as f:
        return json.load(f)


def plan_cycle(wm: dict) -> dict:
    """
    Plan the next research cycle based on current world model state.
    Returns a structured plan that Claude can execute.
    """
    cycle_num = wm["metadata"]["current_cycle"] + 1
    objective = wm["metadata"]["research_objective"]
    keywords = wm["metadata"].get("objective_keywords", [])

    plan = {
        "cycle_number": cycle_num,
        "phase": "planning",
        "tasks": [],
        "rationale": "",
    }

    # --- Cycle 1: Exploratory ---
    if cycle_num == 1:
        plan["rationale"] = (
            "First cycle: Comprehensive EDA to understand dataset structure, "
            "identify key patterns, and ground analysis in existing literature."
        )
        # Pull from initial task queue
        for task in wm.get("task_queue", []):
            plan["tasks"].append(task)

        # Ensure we have at least a basic EDA and literature task
        task_types = [t["type"] for t in plan["tasks"]]
        if "data_analysis" not in task_types:
            plan["tasks"].insert(0, {
                "task_id": f"c{cycle_num}_da_01",
                "type": "data_analysis",
                "priority": "high",
                "question": "What are the key patterns, distributions, and relationships in this dataset?",
                "approach": "Comprehensive EDA with visualizations",
            })
        if "literature_search" not in task_types:
            plan["tasks"].append({
                "task_id": f"c{cycle_num}_lit_01",
                "type": "literature_search",
                "priority": "high",
                "question": f"What is known about {', '.join(keywords[:5])}?",
                "approach": "Broad literature search for context",
            })

    # --- Cycles 2+: Hypothesis-driven ---
    else:
        active_hypotheses = [h for h in wm["hypotheses"] if h["status"] == "active"]
        supported_hypotheses = [h for h in wm["hypotheses"] if h["status"] == "supported"]
        recent_findings = wm["cycles"][-1]["data_findings"] if wm["cycles"] else []

        # Generate tasks from active hypotheses
        for i, hyp in enumerate(active_hypotheses[:3]):  # Max 3 hypothesis tests per cycle
            plan["tasks"].append({
                "task_id": f"c{cycle_num}_da_{i+1:02d}",
                "type": "data_analysis",
                "priority": "high",
                "question": f"Test hypothesis: {hyp['statement']}",
                "hypothesis_id": hyp["hypothesis_id"],
                "approach": f"Design statistical test to evaluate: {hyp['statement']}",
            })

        # Generate follow-up tasks from recent findings
        for finding in recent_findings:
            for q in finding.get("next_questions", [])[:1]:  # 1 follow-up per finding
                task_idx = len([t for t in plan["tasks"] if t["type"] == "data_analysis"]) + 1
                plan["tasks"].append({
                    "task_id": f"c{cycle_num}_da_{task_idx:02d}",
                    "type": "data_analysis",
                    "priority": "medium",
                    "question": q,
                    "follows_from": finding["finding_id"],
                })

        # Literature tasks to validate emerging findings
        if recent_findings:
            key_terms = []
            for f in recent_findings[:3]:
                key_terms.append(f["statement"][:50])
            plan["tasks"].append({
                "task_id": f"c{cycle_num}_lit_01",
                "type": "literature_search",
                "priority": "high",
                "question": f"Find literature supporting or contradicting: {'; '.join(key_terms)}",
                "approach": "Targeted search for validation of recent findings",
            })

        # Add queued tasks
        for task in wm.get("task_queue", [])[:3]:
            plan["tasks"].append(task)

        plan["rationale"] = (
            f"Cycle {cycle_num}: Testing {len(active_hypotheses)} active hypotheses, "
            f"following up on {len(recent_findings)} recent findings, "
            f"and validating with literature search."
        )

    # Cap total tasks
    plan["tasks"] = plan["tasks"][:10]
    return plan


def get_next_task(wm: dict) -> dict:
    """Get the next unexecuted task from the current cycle."""
    if not wm["cycles"]:
        return {"message": "No active cycle. Run plan_cycle first."}

    current = wm["cycles"][-1]
    for task in current.get("tasks_planned", []):
        if task.get("status") in ["planned", None]:
            return {
                "task": task,
                "instructions": generate_task_instructions(task, wm),
            }

    return {"message": "All tasks in current cycle are complete. Ready for cycle completion."}


def generate_task_instructions(task: dict, wm: dict) -> str:
    """Generate detailed instructions for executing a task."""
    objective = wm["metadata"]["research_objective"]
    dataset = wm["metadata"].get("dataset_path", "N/A")

    if task["type"] == "data_analysis":
        return f"""
## Data Analysis Task: {task['task_id']}

**Research Objective**: {objective}
**Dataset**: {dataset}
**Question**: {task['question']}
**Approach**: {task.get('approach', 'Determine appropriate analysis')}

### Instructions:
1. Write a Python script that addresses the question
2. Use appropriate statistical methods (report test statistics, p-values, effect sizes)
3. Generate clear visualizations saved as PNG files
4. Structure output as JSON with these required fields:
   - task_id, finding (text), evidence (statistical details)
   - figures (list of paths), confidence (high/medium/low)
   - next_questions (list of follow-up questions)
5. Save script to: session/scripts/{task['task_id']}.py
6. Save outputs to: session/outputs/{task['task_id']}/

### Context from Prior Cycles:
{_get_relevant_context(task, wm)}

### Guardrails:
- Distinguish statistical significance from scientific importance
- Report effect sizes alongside p-values
- Flag any assumptions or limitations
- Do NOT overinterpret: state what the data shows, not what you wish it showed
"""

    elif task["type"] == "literature_search":
        return f"""
## Literature Search Task: {task['task_id']}

**Research Objective**: {objective}
**Question**: {task['question']}
**Approach**: {task.get('approach', 'Broad search')}

### Instructions:
1. Perform targeted web searches using 2-4 specific queries
2. For each relevant paper found, record:
   - Full citation (authors, title, journal, year)
   - Key finding relevant to our research
   - How it relates to our current hypotheses
3. Structure output as evidence records for the world model
4. Prioritize: peer-reviewed > preprints > reviews

### Current Hypotheses to Validate:
{_get_active_hypotheses(wm)}

### Guardrails:
- Record exact citations — no fabricated references
- Distinguish what a paper actually claims vs. your interpretation
- Note if evidence supports OR contradicts current hypotheses
"""

    return "Unknown task type"


def _get_relevant_context(task: dict, wm: dict) -> str:
    """Extract relevant context from world model for a task."""
    context_parts = []

    # Recent findings
    if wm["cycles"]:
        recent = wm["cycles"][-1].get("data_findings", [])
        if recent:
            context_parts.append("Recent findings:")
            for f in recent[-5:]:
                context_parts.append(f"  - [{f.get('finding_id')}] {f.get('statement', '')[:100]}")

    # Relevant hypotheses
    if task.get("hypothesis_id"):
        for h in wm["hypotheses"]:
            if h["hypothesis_id"] == task["hypothesis_id"]:
                context_parts.append(f"\nTarget hypothesis: {h['statement']}")
                if h.get("supporting_evidence"):
                    context_parts.append(f"  Supporting: {h['supporting_evidence']}")
                break

    return "\n".join(context_parts) if context_parts else "No prior context (first cycle)."


def _get_active_hypotheses(wm: dict) -> str:
    """Format active hypotheses for literature task instructions."""
    active = [h for h in wm["hypotheses"] if h["status"] == "active"]
    if not active:
        return "No active hypotheses yet — search broadly."

    lines = []
    for h in active[:5]:
        lines.append(f"  - [{h['hypothesis_id']}] {h['statement']}")
    return "\n".join(lines)


def checkpoint(wm: dict) -> dict:
    """Generate a checkpoint assessment for human review."""
    m = wm["metadata"]
    findings = wm["findings"]
    hypotheses = wm["hypotheses"]

    high_confidence = [f for f in findings if f.get("confidence") == "high"]
    supported = [h for h in hypotheses if h["status"] == "supported"]
    active = [h for h in hypotheses if h["status"] == "active"]

    assessment = {
        "cycle": m["current_cycle"],
        "status": m["status"],
        "summary": {
            "total_findings": len(findings),
            "high_confidence_findings": len(high_confidence),
            "supported_hypotheses": len(supported),
            "active_hypotheses": len(active),
        },
        "should_continue": len(active) > 0 and m["current_cycle"] < m["max_cycles"],
        "recommended_action": "",
        "key_discoveries_so_far": [],
    }

    if not active and supported:
        assessment["recommended_action"] = "All hypotheses resolved. Consider generating report."
        assessment["should_continue"] = False
    elif m["current_cycle"] >= m["max_cycles"]:
        assessment["recommended_action"] = "Max cycles reached. Generate report with current findings."
    elif len(high_confidence) == 0 and m["current_cycle"] >= 3:
        assessment["recommended_action"] = (
            "No high-confidence findings after 3+ cycles. Consider refining "
            "research objective or examining data quality."
        )
    else:
        assessment["recommended_action"] = (
            f"Continue to cycle {m['current_cycle'] + 1}. "
            f"{len(active)} active hypotheses to test."
        )

    for h in supported:
        related = [f for f in findings if f["finding_id"] in h.get("supporting_evidence", [])]
        assessment["key_discoveries_so_far"].append({
            "hypothesis": h["statement"][:100],
            "supporting_findings": len(related),
            "confidence": h.get("confidence_score", 0.5),
        })

    return assessment


def main():
    parser = argparse.ArgumentParser(description="Research cycle orchestrator")
    parser.add_argument("--session", required=True, help="Session directory")
    parser.add_argument("--action", required=True,
                        choices=["plan", "status", "next_task", "checkpoint"])
    args = parser.parse_args()

    wm = load_world_model(args.session)

    if args.action == "plan":
        plan = plan_cycle(wm)
        print(json.dumps(plan, indent=2, ensure_ascii=False))

    elif args.action == "status":
        from update_world_model import get_summary
        print(get_summary(wm))

    elif args.action == "next_task":
        result = get_next_task(wm)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.action == "checkpoint":
        assessment = checkpoint(wm)
        print(json.dumps(assessment, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
