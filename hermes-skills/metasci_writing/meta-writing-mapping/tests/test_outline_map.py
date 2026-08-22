from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "outline_map.py"
SPEC = importlib.util.spec_from_file_location("outline_map", SCRIPT)
assert SPEC and SPEC.loader
mod = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)
EXAMPLE = ROOT / "references" / "example-outline-1.1.md"
LEGACY_REAL = ROOT / "tests" / "fixtures" / "legacy-real-world.md"


class OutlineMapTests(unittest.TestCase):
    def test_structured_parse(self) -> None:
        out = mod.parse_outline(EXAMPLE)
        self.assertEqual(out.format_version, "1.1")
        self.assertEqual(len(out.nodes), 4)
        self.assertEqual(len(out.decisions), 4)
        self.assertEqual(out.nodes[1].id, "RESULTS.3.4.P1")
        self.assertEqual(out.nodes[1].evidence[0].role, "first-report")
        self.assertEqual(out.nodes[1].axes["epistemic-layer"], "observation")

    def test_inventory_scope_parse(self) -> None:
        out = mod.parse_outline(EXAMPLE)
        fig = next(x for x in out.evidence_inventory if x.id == "Fig-4")
        led = next(x for x in out.ledger_inventory if x.id == "L10")
        self.assertEqual(fig.scope, "RESULTS.3.4")
        self.assertEqual(led.scope, "DISCUSSION.4.2")

    def test_partial_scope_has_incoming_and_outgoing_boundary(self) -> None:
        out = mod.parse_outline(EXAMPLE)
        nodes, boundary = mod.scope_nodes(out, "RESULTS.3.4")
        ids = {n.id for n in nodes}
        self.assertIn("RESULTS.3.3.P3", boundary)
        self.assertIn("DISCUSSION.4.2.P1", boundary)
        self.assertTrue({"RESULTS.3.4.P1", "RESULTS.3.4.P2"}.issubset(ids))

    def test_paragraph_group_scope_uses_comma_ids_and_boundaries(self) -> None:
        out = mod.parse_outline(EXAMPLE)
        scope = "RESULTS.3.4.P1,RESULTS.3.4.P2"
        nodes, boundary = mod.scope_nodes(out, scope)
        core = {n.id for n in nodes if n.id not in boundary}
        self.assertEqual(core, {"RESULTS.3.4.P1", "RESULTS.3.4.P2"})
        self.assertIn("RESULTS.3.3.P3", boundary)
        self.assertIn("DISCUSSION.4.2.P1", boundary)

    def test_provisional_external_predecessor_is_info(self) -> None:
        text = EXAMPLE.read_text(encoding="utf-8")
        text = text.replace("- 지도 상태: integrated", "- 지도 상태: provisional")
        text = text.replace("RESULTS.3.3.P3 | Question-Answer", "EXTERNAL.RESULTS.PREV | Question-Answer", 1)
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "outline.md"
            path.write_text(text, encoding="utf-8")
            issues = mod.validate(mod.parse_outline(path))
        item = next(i for i in issues if i.code == "external-predecessor")
        self.assertEqual(item.level, "info")

    def test_partial_decision_queue_includes_blocker_and_reopened_dependency(self) -> None:
        out = mod.parse_outline(EXAMPLE)
        # Re-open the global blocker for this test: partial work must surface it.
        next(d for d in out.decisions if d.id == "D-001").status = "surfaced"
        queue = mod.decision_queue(out, "RESULTS.3.4")
        ids = [d.id for d in queue]
        self.assertIn("D-001", ids)
        self.assertIn("D-021", ids)
        self.assertIn("D-022", ids)
        self.assertIn("D-028", ids)  # downstream reopened decision depends on D-022
        self.assertEqual(ids[0], "D-001")

    def test_partial_issue_filter_hides_unrelated_inventory_warning(self) -> None:
        out = mod.parse_outline(EXAMPLE)
        issues = mod.validate(out)
        scoped = mod.filtered_issues(issues, out, "RESULTS.3.4")
        messages = "\n".join(i.message for i in scoped)
        self.assertNotIn("Fig-9", messages)  # INTRO inventory item
        self.assertNotIn("L10", messages)   # DISCUSSION inventory item

    def test_unassigned_inventory_and_required_ledger_detected(self) -> None:
        out = mod.parse_outline(EXAMPLE)
        issues = mod.validate(out)
        codes = {(i.code, i.scope) for i in issues}
        self.assertIn(("evidence-unassigned", "INTRO"), codes)
        self.assertIn(("ledger-unassigned", "DISCUSSION.4.2"), codes)

    def test_duplicate_first_report_detected(self) -> None:
        text = EXAMPLE.read_text(encoding="utf-8")
        text = text.replace("Table-S2 | reference", "Table-S2 | first-report")
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "outline.md"
            path.write_text(text, encoding="utf-8")
            issues = mod.validate(mod.parse_outline(path))
        dup = [i for i in issues if i.code == "evidence-first-report-duplicate"]
        self.assertEqual(len(dup), 1)
        self.assertEqual(dup[0].level, "error")

    def test_legacy_vertical_and_decision_lifecycle(self) -> None:
        legacy = """# Outline — legacy\n\n- Core message: test\n\n## 구성\n\n### 3.4 Results\n\nP1 | [관찰] | Comparison | 유역별 차이가 크다\n   ← 3.3 P3 [Question-Answer]\n   근거: Table S2, Fig.4\n   Ledger 착지: L07\n   기여: 유역 차이를 제시\n   메모: 미해결 #1과 연결\n\nP2 | [해석] | Interpretation | 차이는 토지이용으로 일부 설명된다\n   ← P1 [Evidence-Claim]\n   근거: Chen2024\n   기여: 차이의 의미 해석\n\n## 미해결\n\n#1 Core message 확정 — 전체를 막는 블로커\n#9 각주 오기 수정\n#15 해소(2026-08-17): 표 배정 완료\n\\#17 아직 말하지 않은 지적 — 3.4 P1 근거 역할\n"""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "outline.md"
            path.write_text(legacy, encoding="utf-8")
            out = mod.parse_outline(path)
        self.assertEqual(out.format_version, "legacy")
        self.assertEqual(len(out.nodes), 2)
        d = {x.id: x for x in out.decisions}
        self.assertEqual(d["D-001"].priority, "blocker")
        self.assertEqual(d["D-009"].priority, "mechanical")
        self.assertEqual(d["D-015"].status, "resolved")
        self.assertEqual(d["D-017"].status, "detected")
        self.assertIn("D-001", out.nodes[0].decisions)
        active = [x.id for x in mod.decision_queue(out, "manuscript")]
        self.assertNotIn("D-015", active)

    def test_dashboard_is_self_contained_and_contains_tabs(self) -> None:
        out = mod.parse_outline(EXAMPLE)
        issues = mod.validate(out)
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "dashboard.html"
            mod.render_dashboard(out, issues, target)
            html = target.read_text(encoding="utf-8")
        self.assertIn("결정 대기열", html)
        self.assertIn("논리 그래프", html)
        self.assertIn("근거 매트릭스", html)
        self.assertIn("const D=", html)
        self.assertNotIn("https://", html)


class LegacyRealWorldTests(unittest.TestCase):
    """실사용 구형 `outline.md`에서 관찰된 배치에 대한 회귀 테스트.

    1.1.0 최초 패키지는 이 배치에서 `nodes=2 decisions=0 errors=0`을 냈다.
    오류 없이 조용히 통과했으므로, 이 네 개가 이 스킬의 골든 픽스처다.
    """

    def setUp(self) -> None:
        self.out = mod.parse_outline(LEGACY_REAL)

    def test_prose_subheadings_do_not_block_legacy_fallback(self) -> None:
        # `## 구성` 아래 `#### 구조 원리`·`#### 층 구조 규칙`은 단락이 아니다.
        self.assertEqual(self.out.format_version, "legacy")
        self.assertEqual(len(self.out.nodes), 4)

    def test_paragraphs_outside_구성_area_are_read(self) -> None:
        # 단락이 `## 제1부`·`## 제2부` 아래에 있어도 잡히고, 부를 넘는 간선도 산다.
        self.assertEqual(
            [n.id for n in self.out.nodes],
            ["RESULTS.3.1.P1", "RESULTS.3.1.P2", "RESULTS.3.4.P1", "RESULTS.3.4.P2"],
        )
        cross = next(n for n in self.out.nodes if n.id == "RESULTS.3.4.P1")
        self.assertEqual([(l.id, l.role) for l in cross.predecessors],
                         [("RESULTS.3.1.P2", "Question-Answer")])

    def test_numeric_continuation_line_is_not_a_decision(self) -> None:
        # 2번 항목의 이어진 줄 `3장 전반에 깔린다`가 D-003으로 잡히면 안 된다.
        ids = [d.id for d in self.out.decisions]
        self.assertEqual(ids, ["D-001", "D-002", "D-003"])
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn("셋째 미결", next(d for d in self.out.decisions if d.id == "D-003").title)

    def test_claim_recovered_and_no_predecessor_marker_respected(self) -> None:
        first = self.out.nodes[0]
        self.assertTrue(first.claim, "논지가 P 줄 다음 줄에 있어도 회수해야 한다")
        self.assertEqual(first.predecessors, [], "`← — (섹션 첫 단락)`은 간선이 아니다")

    def test_no_errors_on_real_world_layout(self) -> None:
        errors = [i for i in mod.validate(self.out) if i.level == "ERROR"]
        self.assertEqual(errors, [], f"예상치 못한 오류: {[i.message for i in errors]}")


if __name__ == "__main__":
    unittest.main()
