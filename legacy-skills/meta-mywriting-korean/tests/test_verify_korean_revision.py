from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).parents[1] / "scripts" / "verify_korean_revision.py"
SPEC = importlib.util.spec_from_file_location("verify_korean_revision", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


BASE = (
    "환경평가는 계획 수립 과정에서 대안을 검토하는 제도이다. "
    "2024년 조사에서는 대상지 12개소를 확인하였다. "
    '보고서는 "자료의 한계를 고려해야 한다"고 밝혔다.'
)


class VerifyKoreanRevisionTests(unittest.TestCase):
    def test_identity_passes(self) -> None:
        code, report = MODULE.verify(BASE, BASE)
        self.assertEqual(code, 0)
        self.assertEqual(report["verdict"], "PASS")

    def test_number_injection_aborts(self) -> None:
        code, report = MODULE.verify(BASE, BASE + " 추가 대상은 7개소이다.")
        self.assertEqual(code, 2)
        self.assertEqual(report["numbers"]["added"], ["7"])

    def test_direct_quote_change_aborts(self) -> None:
        changed = BASE.replace("자료의 한계를 고려해야 한다", "자료는 완전하다")
        code, _ = MODULE.verify(BASE, changed)
        self.assertEqual(code, 2)

    def test_citation_format_normalization_passes(self) -> None:
        before = BASE + " 김경호(2022)는 이를 검토하였다."
        after = BASE + " 김경호(2022)는 이를 분석하였다."
        code, report = MODULE.verify(before, after)
        self.assertNotEqual(code, 2)
        self.assertEqual(report["citations"], {"removed": [], "added": []})

    def test_citation_author_change_warns(self) -> None:
        before = BASE + " 김경호(2022)는 이를 검토하였다."
        after = BASE + " 이영준(2022)는 이를 검토하였다."
        code, report = MODULE.verify(before, after)
        self.assertEqual(code, 1)
        self.assertTrue(any(issue["gate"] == "P1-citations" for issue in report["issues"]))

    def test_corner_bracket_content_change_aborts(self) -> None:
        before = BASE + " 「환경영향평가법」을 적용하였다."
        after = BASE + " 「하천법」을 적용하였다."
        code, _ = MODULE.verify(before, after)
        self.assertEqual(code, 2)

    def test_adding_brackets_around_same_name_passes(self) -> None:
        before = BASE + " 환경영향평가법을 적용하였다."
        after = BASE + " 「환경영향평가법」을 적용하였다."
        code, report = MODULE.verify(before, after)
        self.assertNotEqual(code, 2)
        self.assertEqual(report["named_spans"], {"removed": [], "added": []})

    def test_s1_signal_warns(self) -> None:
        changed = BASE.replace("제도이다", "제도로 되어진다")
        code, report = MODULE.verify(BASE, changed)
        self.assertEqual(code, 1)
        self.assertTrue(any(issue["gate"] == "P4-signals" for issue in report["issues"]))

    def test_h13_demonstrative_anaphora_is_counted(self) -> None:
        changed = BASE + " 이 과정에서 자료가 축적되었다. 이 고정성은 문제를 낳는다."
        code, report = MODULE.verify(BASE, changed)
        self.assertEqual(code, 1)
        self.assertEqual(report["style_signals"]["after"]["H13"]["count"], 2)
        self.assertTrue(
            any(
                issue["gate"] == "P4-signals" and "H13" in issue["message"]
                for issue in report["issues"]
            )
        )

    def test_h13_reduction_does_not_warn(self) -> None:
        before = BASE + " 이 과정에서 자료가 축적되었다. 이 고정성은 문제를 낳는다."
        after = BASE + " 제도는 자료를 축적하면서 발전하였고 고정되면 문제를 낳는다."
        code, report = MODULE.verify(before, after)
        self.assertNotEqual(code, 2)
        self.assertEqual(report["style_signals"]["after"]["H13"]["count"], 0)

    def test_h14_middle_dot_overuse_is_counted(self) -> None:
        changed = BASE + " 정책·법제와 자료·정보를 연계·활용한다."
        code, report = MODULE.verify(BASE, changed)
        self.assertEqual(code, 1)
        self.assertEqual(report["style_signals"]["after"]["H14"]["count"], 1)
        self.assertTrue(
            any(
                issue["gate"] == "P4-signals" and "H14" in issue["message"]
                for issue in report["issues"]
            )
        )

    def test_h14_single_fixed_pair_is_allowed(self) -> None:
        changed = BASE + " 조사·분석 결과를 제시하였다."
        code, report = MODULE.verify(BASE, changed)
        self.assertNotEqual(code, 1)
        self.assertEqual(report["style_signals"]["after"]["H14"]["count"], 0)

    def test_register_mixing_warns(self) -> None:
        changed = BASE + " 추가 검토가 필요합니다."
        code, report = MODULE.verify(BASE, changed)
        self.assertEqual(code, 1)
        self.assertTrue(any(issue["gate"] == "P3-register" for issue in report["issues"]))

    def test_total_rewrite_aborts(self) -> None:
        code, report = MODULE.verify(BASE, "전혀 다른 내용으로 다시 작성하였다.")
        self.assertEqual(code, 2)
        self.assertGreaterEqual(report["change_rate"], 0.5)

    def test_cli_writes_utf8_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            before = root / "before.txt"
            after = root / "after.txt"
            report_path = root / "verification_report.json"
            before.write_text(BASE, encoding="utf-8")
            after.write_text(BASE, encoding="utf-8")
            code = MODULE.main(
                [
                    "--before",
                    str(before),
                    "--after",
                    str(after),
                    "--json-out",
                    str(report_path),
                ]
            )
            self.assertEqual(code, 0)
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(report["verdict"], "PASS")


if __name__ == "__main__":
    unittest.main()
