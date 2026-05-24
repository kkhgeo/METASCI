#!/usr/bin/env python3
"""
Initialize a research session with world model.
Usage:
    python init_world_model.py --objective "..." --dataset /path/to/data --output /path/to/session/
"""

import argparse
import json
import os
import uuid
from datetime import datetime, timezone


def create_session_dirs(output_dir: str) -> dict:
    """Create the directory structure for a research session."""
    dirs = {
        "root": output_dir,
        "scripts": os.path.join(output_dir, "scripts"),
        "outputs": os.path.join(output_dir, "outputs"),
        "figures": os.path.join(output_dir, "figures"),
        "literature": os.path.join(output_dir, "literature"),
        "reports": os.path.join(output_dir, "reports"),
    }
    for d in dirs.values():
        os.makedirs(d, exist_ok=True)
    return dirs


def extract_keywords(objective: str) -> list:
    """Extract research keywords from objective text."""
    import re
    # Remove common stop words and extract meaningful terms
    stop_words = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been",
        "being", "have", "has", "had", "do", "does", "did", "will",
        "would", "could", "should", "may", "might", "can", "shall",
        "to", "of", "in", "for", "on", "with", "at", "by", "from",
        "as", "into", "through", "during", "before", "after", "above",
        "below", "between", "and", "but", "or", "nor", "not", "so",
        "yet", "both", "either", "neither", "each", "every", "all",
        "any", "few", "more", "most", "other", "some", "such", "no",
        "only", "own", "same", "than", "too", "very", "how", "what",
        "which", "who", "whom", "this", "that", "these", "those",
        "it", "its", "if", "then", "identify", "determine", "investigate",
        "analyze", "propose", "find", "discover", "examine", "explore",
    }
    words = re.findall(r'\b[a-zA-Z]{3,}\b', objective.lower())
    keywords = [w for w in words if w not in stop_words]
    # Deduplicate while preserving order
    seen = set()
    unique = []
    for w in keywords:
        if w not in seen:
            seen.add(w)
            unique.append(w)
    return unique[:20]  # Top 20 keywords


def init_world_model(objective: str, dataset_path: str, max_cycles: int = 10) -> dict:
    """Create a new world model."""
    return {
        "version": "1.0",
        "metadata": {
            "session_id": str(uuid.uuid4()),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "research_objective": objective,
            "objective_keywords": extract_keywords(objective),
            "dataset_path": os.path.abspath(dataset_path) if dataset_path else None,
            "max_cycles": max_cycles,
            "current_cycle": 0,
            "status": "initializing",
        },
        "dataset_profile": None,  # Populated by profile_dataset.py
        "cycles": [],
        "hypotheses": [],
        "findings": [],
        "task_queue": [],
        "discoveries": [],
    }


def main():
    parser = argparse.ArgumentParser(description="Initialize agentic research session")
    parser.add_argument("--objective", required=True, help="Research objective")
    parser.add_argument("--dataset", required=True, help="Path to dataset file or directory")
    parser.add_argument("--output", required=True, help="Output directory for session")
    parser.add_argument("--max-cycles", type=int, default=10, help="Maximum research cycles")
    args = parser.parse_args()

    # Create session directories
    dirs = create_session_dirs(args.output)

    # Initialize world model
    wm = init_world_model(args.objective, args.dataset, args.max_cycles)

    # Save world model
    wm_path = os.path.join(args.output, "world_model.json")
    with open(wm_path, "w") as f:
        json.dump(wm, f, indent=2, ensure_ascii=False)

    print(f"✓ Session initialized: {wm['metadata']['session_id']}")
    print(f"  World model: {wm_path}")
    print(f"  Directories created: {list(dirs.keys())}")
    print(f"  Keywords extracted: {wm['metadata']['objective_keywords']}")
    print(f"  Max cycles: {args.max_cycles}")
    print(f"\nNext step: Run profile_dataset.py to analyze the dataset.")


if __name__ == "__main__":
    main()
