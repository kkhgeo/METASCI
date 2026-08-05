#!/usr/bin/env python3
"""
Generate a traceable scientific report from world model findings.
Every claim in the report must link to a data analysis script or literature citation.

Usage:
    python generate_report.py --session /path/to/session/ --output report.md
"""

import argparse
import json
import os
from datetime import datetime, timezone


def load_world_model(session_dir: str) -> dict:
    wm_path = os.path.join(session_dir, "world_model.json")
    with open(wm_path) as f:
        return json.load(f)


def validate_traceability(wm: dict) -> dict:
    """Check that all findings have proper evidence chains."""
    issues = []
    valid_findings = []

    for f in wm["findings"]:
        has_evidence = (
            f.get("script_path") or
            f.get("evidence_chain") or
            f.get("source")
        )
        if not has_evidence:
            issues.append(f"Finding {f['finding_id']}: No evidence chain")
        else:
            valid_findings.append(f)

    return {
        "valid_findings": valid_findings,
        "issues": issues,
        "total": len(wm["findings"]),
        "valid": len(valid_findings),
        "traceability_pct": len(valid_findings) / max(len(wm["findings"]), 1) * 100,
    }


def group_findings_into_narratives(wm: dict) -> list:
    """Group related findings into discovery narratives."""
    # Use existing discoveries if available
    if wm.get("discoveries"):
        return wm["discoveries"]

    # Otherwise, group by hypothesis
    narratives = []
    supported = [h for h in wm["hypotheses"] if h["status"] == "supported"]

    for hyp in supported:
        related_findings = [
            f for f in wm["findings"]
            if f["finding_id"] in hyp.get("supporting_evidence", [])
        ]
        if related_findings:
            narratives.append({
                "title": hyp["statement"][:100],
                "hypothesis": hyp,
                "findings": related_findings,
                "confidence": hyp.get("confidence_score", 0.5),
            })

    # Add orphan high-confidence findings
    claimed_ids = set()
    for n in narratives:
        for f in n["findings"]:
            claimed_ids.add(f["finding_id"])

    orphans = [
        f for f in wm["findings"]
        if f["finding_id"] not in claimed_ids and f.get("confidence") == "high"
    ]
    if orphans:
        narratives.append({
            "title": "Additional Findings",
            "hypothesis": None,
            "findings": orphans,
            "confidence": 0.5,
        })

    return narratives


def render_finding(finding: dict, idx: int) -> str:
    """Render a single finding as markdown with citation."""
    lines = []
    lines.append(f"**Finding {idx}.** {finding['statement']}")

    # Evidence citation
    evidence_parts = []
    if finding.get("statistical_evidence"):
        evidence_parts.append(f"*Statistical evidence*: {finding['statistical_evidence']}")
    if finding.get("script_path"):
        evidence_parts.append(f"*Source*: `{finding['script_path']}`")
    if finding.get("source"):
        evidence_parts.append(f"*Citation*: {finding['source']}")
    if finding.get("evidence_chain"):
        for ec in finding["evidence_chain"]:
            evidence_parts.append(f"*{ec['type']}*: {ec.get('detail', ec.get('ref', ''))}")

    if evidence_parts:
        lines.append("")
        for ep in evidence_parts:
            lines.append(f"> {ep}")

    # Confidence indicator
    conf = finding.get("confidence", "medium")
    conf_emoji = {"high": "🟢", "medium": "🟡", "low": "🔴"}.get(conf, "⚪")
    lines.append(f"\n*Confidence*: {conf_emoji} {conf}")

    # Figures
    if finding.get("figures"):
        for fig in finding["figures"]:
            lines.append(f"\n![{finding['finding_id']}]({fig})")

    return "\n".join(lines)


def generate_report(wm: dict, output_path: str):
    """Generate the full report."""
    m = wm["metadata"]
    trace = validate_traceability(wm)
    narratives = group_findings_into_narratives(wm)

    lines = []

    # Header
    lines.append(f"# Research Report")
    lines.append(f"")
    lines.append(f"**Research Objective**: {m['research_objective']}")
    lines.append(f"")
    lines.append(f"**Generated**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"**Session**: {m['session_id'][:8]}")
    lines.append(f"**Cycles completed**: {m['current_cycle']}")
    lines.append(f"**Traceability**: {trace['traceability_pct']:.0f}% of claims have evidence chains")
    lines.append(f"")

    # Dataset summary
    if wm.get("dataset_profile"):
        dp = wm["dataset_profile"]
        lines.append(f"## Dataset")
        lines.append(f"")
        lines.append(f"- **File**: {dp['filename']}")
        lines.append(f"- **Dimensions**: {dp['rows']:,} rows × {dp['columns']} columns")
        if dp.get("quality_notes"):
            lines.append(f"- **Quality notes**: {len(dp['quality_notes'])} issues detected")
        lines.append(f"")

    # Executive Summary
    lines.append(f"## Executive Summary")
    lines.append(f"")
    supported_count = sum(1 for h in wm["hypotheses"] if h["status"] == "supported")
    rejected_count = sum(1 for h in wm["hypotheses"] if h["status"] == "rejected")
    lines.append(
        f"Across {m['current_cycle']} research cycles, this analysis generated "
        f"{len(wm['findings'])} findings, evaluated {len(wm['hypotheses'])} hypotheses "
        f"({supported_count} supported, {rejected_count} rejected), and identified "
        f"{len(narratives)} discovery narratives."
    )
    lines.append(f"")

    # Discovery Narratives
    for i, narrative in enumerate(narratives, 1):
        title = narrative.get("title", f"Discovery {i}")
        lines.append(f"## Discovery {i}: {title}")
        lines.append(f"")

        if narrative.get("narrative"):
            lines.append(narrative["narrative"])
            lines.append(f"")

        if narrative.get("hypothesis"):
            hyp = narrative["hypothesis"]
            lines.append(f"**Hypothesis**: {hyp['statement']}")
            lines.append(f"**Status**: {hyp['status']} (confidence: {hyp.get('confidence_score', 'N/A')})")
            lines.append(f"")

        findings = narrative.get("findings", narrative.get("supporting_findings", []))
        if isinstance(findings, list) and findings:
            lines.append(f"### Supporting Evidence")
            lines.append(f"")
            for j, finding in enumerate(findings, 1):
                if isinstance(finding, dict):
                    lines.append(render_finding(finding, j))
                else:
                    # Finding ID reference — resolve from wm
                    resolved = next(
                        (f for f in wm["findings"] if f["finding_id"] == finding), None
                    )
                    if resolved:
                        lines.append(render_finding(resolved, j))
                    else:
                        lines.append(f"**Finding {j}**: {finding} (reference)")
                lines.append(f"")

        lines.append("---")
        lines.append("")

    # Methodology
    lines.append(f"## Methodology")
    lines.append(f"")
    lines.append(f"This report was generated using an agentic research framework inspired by ")
    lines.append(f"Kosmos (Mitchener et al., 2025). The framework performs iterative cycles of ")
    lines.append(f"data analysis, literature search, and hypothesis generation, coordinated ")
    lines.append(f"through a structured world model.")
    lines.append(f"")
    lines.append(f"### Research Cycle Summary")
    lines.append(f"")
    for cycle in wm["cycles"]:
        cn = cycle["cycle_number"]
        n_da = sum(1 for t in cycle.get("tasks_planned", []) if t.get("type") == "data_analysis")
        n_lit = sum(1 for t in cycle.get("tasks_planned", []) if t.get("type") == "literature_search")
        summary = cycle.get("cycle_summary", "No summary")
        lines.append(f"**Cycle {cn}** ({n_da} data tasks, {n_lit} literature tasks): {summary}")
        lines.append(f"")

    # Traceability report
    if trace["issues"]:
        lines.append(f"## Traceability Notes")
        lines.append(f"")
        lines.append(f"⚠ {len(trace['issues'])} findings lack complete evidence chains:")
        for issue in trace["issues"]:
            lines.append(f"- {issue}")
        lines.append(f"")

    # Hypothesis inventory
    lines.append(f"## Hypothesis Inventory")
    lines.append(f"")
    lines.append(f"| ID | Statement | Status | Confidence |")
    lines.append(f"|---|---|---|---|")
    for h in wm["hypotheses"]:
        status_emoji = {
            "active": "🔵", "supported": "🟢",
            "rejected": "🔴", "refined": "🟡"
        }.get(h["status"], "⚪")
        stmt = h["statement"][:80] + ("..." if len(h["statement"]) > 80 else "")
        lines.append(f"| {h['hypothesis_id']} | {stmt} | {status_emoji} {h['status']} | {h.get('confidence_score', 'N/A')} |")
    lines.append(f"")

    # Write report
    report_text = "\n".join(lines)
    with open(output_path, "w") as f:
        f.write(report_text)

    print(f"✓ Report generated: {output_path}")
    print(f"  Discoveries: {len(narratives)}")
    print(f"  Findings: {len(wm['findings'])}")
    print(f"  Traceability: {trace['traceability_pct']:.0f}%")

    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate research report from world model")
    parser.add_argument("--session", required=True, help="Session directory")
    parser.add_argument("--output", default=None, help="Output path (default: session/reports/report.md)")
    args = parser.parse_args()

    wm = load_world_model(args.session)
    output = args.output or os.path.join(args.session, "reports", "report.md")
    os.makedirs(os.path.dirname(output), exist_ok=True)
    generate_report(wm, output)


if __name__ == "__main__":
    main()
