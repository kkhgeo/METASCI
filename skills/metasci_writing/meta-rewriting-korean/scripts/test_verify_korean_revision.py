#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest

MODULE_PATH = Path(__file__).with_name("verify_korean_revision.py")
SPEC = importlib.util.spec_from_file_location("verify_korean_revision", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class VerifyKoreanRevisionTests(unittest.TestCase):
    def assert_abort(self, before: str, after: str, mode: str = "deep") -> None:
        code, report = MODULE.verify(before, after, mode=mode)
        self.assertEqual(code, 2, report)
        self.assertEqual(report["verdict"], "ABORT")

    def test_value_binding_swap_aborts(self) -> None:
        self.assert_abort(
            "A는 10 mg/L이고 B는 20 mg/L이다.",
            "A는 20 mg/L이고 B는 10 mg/L이다.",
        )

    def test_unit_change_aborts(self) -> None:
        self.assert_abort("농도는 10 mg/L이다.", "농도는 10 µg/L이다.")

    def test_comparator_change_aborts(self) -> None:
        self.assert_abort(
            "차이는 p < 0.05에서 유의하였다.",
            "차이는 p > 0.05에서 유의하였다.",
        )

    def test_sign_change_aborts(self) -> None:
        self.assert_abort("변화량은 −10%였다.", "변화량은 10%였다.")

    def test_duplicate_number_removal_aborts(self) -> None:
        self.assert_abort("값은 10, 10, 20이었다.", "값은 10, 20이었다.")

    def test_deep_mode_allows_large_structural_change(self) -> None:
        before = "A는 10 mg/L이다. B는 20 mg/L이다."
        after = "B는 20 mg/L이다. A는 10 mg/L이다."
        code, report = MODULE.verify(before, after, mode="deep")
        self.assertEqual(code, 0, report)
        self.assertEqual(report["verdict"], "MECHANICAL_PASS")
        self.assertGreater(report["change_rate"], 0.50)
        self.assertFalse(report["change_rate_is_blocking"])

    def test_light_mode_blocks_same_large_change(self) -> None:
        before = "A는 10 mg/L이다. B는 20 mg/L이다."
        after = "B는 20 mg/L이다. A는 10 mg/L이다."
        self.assert_abort(before, after, mode="light")

    def test_citation_removal_aborts(self) -> None:
        self.assert_abort(
            "Kim et al. (2015)은 증가를 보고하였다.",
            "증가가 보고되었다.",
        )

    def test_figure_reference_change_aborts(self) -> None:
        self.assert_abort("결과는 표 2에 제시하였다.", "결과는 표 3에 제시하였다.")


if __name__ == "__main__":
    unittest.main()
