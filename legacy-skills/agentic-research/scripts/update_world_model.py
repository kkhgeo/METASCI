#!/usr/bin/env python3
"""
Safely update the world model after each research cycle.
Enforces append-only semantics for findings, hypothesis lifecycle rules,
and evidence chain completeness.

Usage:
    python update_world_model.py --session /path/to/session/ --action [start_cycle|add_finding|...]
"""

import argparse
import json
import os
import shutil
from datetime import datetime, timezone


def load_world_model(session_dir: str) -> dict:
    """Load world model with backup."""
    wm_path = os.path.join(session_dir, "world_model.json")
    with open(wm_path) as f:
        return json.load(f)


def save_world_model(wm: dict, session_dir: str):
    """Save world model with backup of previous version."""
    wm_path = os.path.join(session_dir, "world_model.json")
    backup_dir = os.path.join(session_dir, "backups")
    os.makedirs(backup_dir, exist_ok=True)

    # Backup current version
    if os.path.exists(wm_path):
        cycle = wm["metadata"]["current_cycle"]
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"world_model_c{cycle}_{ts}.json")
        shutil.copy2(wm_path, backup_path)

    wm["metadata"]["updated_at"] = datetime.now(timezone.utc).isoformat()

    with open(wm_path, "w") as f:
        json.dump(wm, f, indent=2, ensure_ascii=False)


def start_cycle(wm: dict) -> dict:
    """Begin a new research cycle."""
    cycle_num = wm["metadata"]["current_cycle"] + 1
    wm["metadata"]["current_cycle"] = cycle_num
    wm["metadata"]["status"] = "running"

    new_cycle = {
        "cycle_number": cycle_num,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "completed_at": None,
        "tasks_planned": [],
        "data_findings": [],
        "literature_evidence": [],
        "new_hypotheses": [],
        "rejected_hypotheses": [],
        "cycle_summary": None,
    }

    # Move tasks from queue into this cycle's plan
    tasks_for_cycle = wm.get("task_queue", [])[:10]  # Max 10 tasks per cycle
    new_cycle["tasks_planned"] = [
        {**t, "status": "planned"} for t in tasks_for_cycle
    ]
    wm["task_queue"] = wm.get("task_queue", [])[10:]  # Remove assigned tasks

    wm["cycles"].append(new_cycle)
    return wm


def complete_cycle(wm: dict, summary: str) -> dict:
    """Complete the current cycle with a summary."""
    if not wm["cycles"]:
        raise ValueError("No active cycle to complete")

    current = wm["cycles"][-1]
    current["completed_at"] = datetime.now(timezone.utc).isoformat()
    current["cycle_summary"] = summary

    # Check convergence
    max_cycles = wm["metadata"]["max_cycles"]
    if wm["metadata"]["current_cycle"] >= max_cycles:
        wm["metadata"]["status"] = "converged"

    return wm


def add_finding(wm: dict, finding: dict) -> dict:
    """Add a new finding (append-only)."""
    required = ["finding_id", "task_id", "statement", "evidence_type", "confidence"]
    for field in required:
        if field not in finding:
            raise ValueError(f"Finding missing required field: {field}")

    # Ensure finding_id is unique
    existing_ids = {f["finding_id"] for f in wm["findings"]}
    if finding["finding_id"] in existing_ids:
        raise ValueError(f"Duplicate finding_id: {finding['finding_id']}")

    wm["findings"].append(finding)

    # Also add to current cycle's data_findings
    if wm["cycles"]:
        wm["cycles"][-1]["data_findings"].append(finding)

    return wm


def add_literature(wm: dict, evidence: dict) -> dict:
    """Add literature evidence."""
    required = ["evidence_id", "claim", "source"]
    for field in required:
        if field not in evidence:
            raise ValueError(f"Evidence missing required field: {field}")

    if wm["cycles"]:
        wm["cycles"][-1]["literature_evidence"].append(evidence)

    return wm


def update_hypothesis(wm: dict, hypothesis_id: str, status: str,
                      evidence: list = None, note: str = None) -> dict:
    """Update hypothesis status following lifecycle rules."""
    valid_transitions = {
        "active": ["supported", "rejected", "refined"],
        "supported": ["refined"],  # Can be refined further
        "rejected": [],  # Terminal — never reactivated
        "refined": ["supported", "rejected"],
    }

    hyp = None
    for h in wm["hypotheses"]:
        if h["hypothesis_id"] == hypothesis_id:
            hyp = h
            break

    if hyp is None:
        raise ValueError(f"Hypothesis not found: {hypothesis_id}")

    current_status = hyp["status"]
    if status not in valid_transitions.get(current_status, []):
        raise ValueError(
            f"Invalid transition: {current_status} → {status}. "
            f"Allowed: {valid_transitions.get(current_status, [])}"
        )

    hyp["status"] = status
    if evidence:
        if status in ["supported"]:
            hyp["supporting_evidence"].extend(evidence)
        elif status == "rejected":
            hyp["contradicting_evidence"].extend(evidence)
    if note:
        hyp.setdefault("notes", []).append(note)

    return wm


def add_hypothesis(wm: dict, hypothesis: dict) -> dict:
    """Add a new hypothesis."""
    required = ["hypothesis_id", "statement"]
    for field in required:
        if field not in hypothesis:
            raise ValueError(f"Hypothesis missing required field: {field}")

    hypothesis.setdefault("status", "active")
    hypothesis.setdefault("created_cycle", wm["metadata"]["current_cycle"])
    hypothesis.setdefault("supporting_evidence", [])
    hypothesis.setdefault("contradicting_evidence", [])
    hypothesis.setdefault("tests_completed", [])
    hypothesis.setdefault("confidence_score", 0.5)

    wm["hypotheses"].append(hypothesis)

    if wm["cycles"]:
        wm["cycles"][-1]["new_hypotheses"].append(hypothesis)

    return wm


def add_tasks(wm: dict, tasks: list) -> dict:
    """Add tasks to the queue for the next cycle."""
    for task in tasks:
        required = ["task_id", "type", "question"]
        for field in required:
            if field not in task:
                raise ValueError(f"Task missing required field: {field}")
        task.setdefault("priority", "medium")
        task.setdefault("depends_on", [])

    wm["task_queue"].extend(tasks)
    # Sort by priority
    priority_order = {"high": 0, "medium": 1, "low": 2}
    wm["task_queue"].sort(key=lambda t: priority_order.get(t.get("priority", "medium"), 1))
    return wm


def add_discovery(wm: dict, discovery: dict) -> dict:
    """Add a synthesized discovery."""
    required = ["discovery_id", "title", "narrative", "supporting_findings"]
    for field in required:
        if field not in discovery:
            raise ValueError(f"Discovery missing required field: {field}")

    wm["discoveries"].append(discovery)
    return wm


def get_summary(wm: dict) -> str:
    """Generate a human-readable summary of current state."""
    m = wm["metadata"]
    lines = [
        f"Session: {m['session_id'][:8]}...",
        f"Status: {m['status']}",
        f"Cycle: {m['current_cycle']} / {m['max_cycles']}",
        f"Findings: {len(wm['findings'])}",
        f"Hypotheses: {len(wm['hypotheses'])} "
        f"(active: {sum(1 for h in wm['hypotheses'] if h['status'] == 'active')}, "
        f"supported: {sum(1 for h in wm['hypotheses'] if h['status'] == 'supported')}, "
        f"rejected: {sum(1 for h in wm['hypotheses'] if h['status'] == 'rejected')})",
        f"Discoveries: {len(wm['discoveries'])}",
        f"Task queue: {len(wm['task_queue'])} pending",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Update agentic research world model")
    parser.add_argument("--session", required=True, help="Session directory")
    parser.add_argument("--action", required=True,
                        choices=["start_cycle", "complete_cycle", "add_finding",
                                 "add_hypothesis", "update_hypothesis", "add_tasks",
                                 "add_literature", "add_discovery", "summary"])
    parser.add_argument("--data", type=str, help="JSON string with action data")
    parser.add_argument("--summary", type=str, help="Cycle summary text")

    args = parser.parse_args()
    wm = load_world_model(args.session)

    if args.action == "start_cycle":
        wm = start_cycle(wm)
        print(f"✓ Started cycle {wm['metadata']['current_cycle']}")

    elif args.action == "complete_cycle":
        wm = complete_cycle(wm, args.summary or "Cycle completed")
        print(f"✓ Completed cycle {wm['metadata']['current_cycle']}")

    elif args.action == "summary":
        print(get_summary(wm))
        return  # Don't save

    else:
        if not args.data:
            print(f"Error: --data required for action '{args.action}'")
            return
        data = json.loads(args.data)

        actions = {
            "add_finding": add_finding,
            "add_hypothesis": add_hypothesis,
            "add_literature": add_literature,
            "add_tasks": lambda w, d: add_tasks(w, d if isinstance(d, list) else [d]),
            "add_discovery": add_discovery,
        }

        if args.action == "update_hypothesis":
            wm = update_hypothesis(wm, data["hypothesis_id"], data["status"],
                                   data.get("evidence"), data.get("note"))
        else:
            wm = actions[args.action](wm, data)
        print(f"✓ {args.action} completed")

    save_world_model(wm, args.session)
    print(get_summary(wm))


if __name__ == "__main__":
    main()
