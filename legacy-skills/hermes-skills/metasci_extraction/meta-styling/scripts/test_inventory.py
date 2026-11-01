"""Regression tests for preservation_inventory.py (Gate 1).

Run from this folder:  python -m unittest test_inventory
"""
import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CLI = Path(__file__).with_name("preservation_inventory.py")
STATUS = {0: "PASS", 1: "FAIL", 2: "BLOCKED"}


class InventoryTests(unittest.TestCase):
    def compare(self, before, after, style="none", expected=0):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "before.txt").write_text(before, encoding="utf-8")
            (root / "after.txt").write_text(after, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(CLI), "--before", str(root / "before.txt"),
                 "--after", str(root / "after.txt"), "--citation-style", style,
                 "--output", str(root / "audit.tsv")],
                capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
            rows = list(csv.DictReader((root / "audit.tsv").read_text(encoding="utf-8").splitlines(),
                                       delimiter="\t"))
            self.assertEqual(rows[-1]["result"], STATUS[expected])
            return rows

    def items(self, rows, kind):
        return {r["item"] for r in rows if r["kind"] == kind}

    # --- display-item references -------------------------------------------------
    def test_figure_format_change_passes(self):
        self.compare("Figure 2 shows a change of -0.25%.", "Fig. 2 shows a change of -0.25%.")

    def test_figure_deletion_fails(self):
        self.compare("Figure 2 shows the pattern.", "The pattern is evident.", expected=1)

    def test_repeated_reference_loss_fails(self):
        self.compare("Fig. 2 supports this. See Figure 2.", "Fig. 2 supports this.", expected=1)

    def test_ranges_panels_supplements(self):
        rows = self.compare("Figures 2–4 and Table S1 support Fig. 2(a).",
                            "Figs. 2, 3, 4 and Table S1 support Figure 2a.")
        self.assertEqual(self.items(rows, "figure"), {"2", "3", "4", "2a"})
        self.assertEqual(self.items(rows, "table"), {"s1"})

    def test_uppercase_panel_list_and_range(self):
        rows = self.compare("As shown in Fig. 4A and B (Table 1; Fig. 1B–D), values rose.",
                            "As shown in Fig. 4A and B (Table 1; Fig. 1B–D), values rose.")
        self.assertEqual(self.items(rows, "figure"), {"4a", "4b", "1b", "1c", "1d"})

    def test_uppercase_panel_loss_fails(self):
        self.compare("As shown in Fig. 4A and B, values rose.", "As shown in Fig. 4A, values rose.", expected=1)
        self.compare("See Fig. 2A–C.", "See Fig. 2A.", expected=1)

    def test_lowercase_panel_range(self):
        rows = self.compare("Figures 2a–c support this.", "Figures 2a–c support this.")
        self.assertEqual(self.items(rows, "figure"), {"2a", "2b", "2c"})

    def test_parenthesised_equations(self):
        rows = self.compare("Eq. (2) and Eqs. (6) and (7) apply.", "Eq. (2) and Eqs. (6) and (7) apply.")
        self.assertEqual(self.items(rows, "equation"), {"2", "6", "7"})

    def test_ambiguous_singular_numeric_list_blocks(self):
        self.compare("Figure 2 and 10 samples support this.", "Figure 2 and 10 support this.", expected=2)

    # --- citations ---------------------------------------------------------------
    def test_author_year_forms(self):
        rows = self.compare("This is known (Smith et al., 2020; Jones and Lee, 2021).",
                            "Smith et al. (2020) agree with Jones & Lee (2021).", "author-year")
        self.assertEqual(self.items(rows, "citation"), {"smith et al:2020", "jones and lee:2021"})

    def test_citation_identity_change_fails(self):
        self.compare("Smith (2020) agreed.", "Jones (2020) agreed.", "author-year", 1)

    def test_partial_author_blocks(self):
        self.compare("Van Smith (2020) agreed.", "Smith (2020) agreed.", "author-year", 2)

    def test_loose_year_is_a_number_with_note(self):
        rows = self.compare("Samples were collected in 2010 and 2011.", "Samples were collected in 2010 and 2011.",
                            "author-year")
        self.assertEqual(self.items(rows, "number"), {"2010", "2011"})
        self.assertTrue(any(r["kind"] == "note" for r in rows))
        self.compare("Samples were collected in 2010 and 2011.", "Samples were collected in 2010.",
                     "author-year", 1)

    def test_numeric_citation_range(self):
        rows = self.compare("This is known [1–3].", "This is known [1, 2, 3].", "numeric")
        self.assertEqual(self.items(rows, "citation"), {"1", "2", "3"})

    def test_wrong_citation_mode_blocks(self):
        self.compare("This is known [3].", "This is known [3].", "author-year", 2)
        self.compare("Smith (2020) agreed.", "Smith (2020) agreed.", "numeric", 2)
        self.compare("Smith (2020) agreed.", "Smith (2020) agreed.", "none", 2)

    # --- numbers -----------------------------------------------------------------
    def test_sign_change_fails(self):
        self.compare("The change was -0.25%.", "The change was 0.25%.", expected=1)

    def test_semantic_swap_passes_here(self):
        # Same numerals, different meaning: Gate 2 must catch this, not Gate 1.
        self.compare("A = 10, B = 20.", "A = 20, B = 10.")

    def test_numeric_addition_fails(self):
        self.compare("The value was 10.", "The value was 10 with 20 replicates.", expected=1)

    def test_scientific_and_ranges(self):
        rows = self.compare("Values were 1.2e-3, 3 × 10^-4 and 2–5% (n = 103, r = -0.61).",
                            "Values were 1.2e-3, 3 × 10^-4 and 2–5% (n = 103, r = -0.61).")
        self.assertEqual(self.items(rows, "number"), {"1.2e-3", "3×10^-4", "2-5%", "103", "-0.61"})

    # --- identifiers -------------------------------------------------------------
    def test_domain_identifiers_pass(self):
        text = ("The δ15N and d18O values of NO3-N rose; Ca2+ and HCO3 varied. PC1 explained "
                "42.3% and the 10th percentile (sample A-02, 10⁻³ mol/L, 3000XL) was excluded.")
        rows = self.compare(text, text)
        self.assertTrue({"δ15N", "d18O", "NO3-N", "Ca2+", "HCO3", "PC1", "10th", "A-02", "10⁻³", "3000XL"}
                        <= self.items(rows, "identifier"))
        self.assertEqual(self.items(rows, "number"), {"42.3%"})

    def test_identifier_loss_fails(self):
        self.compare("The δ15N values rose.", "The values rose.", expected=1)
        self.compare("PC1 and PC2 were retained.", "PC1 was retained.", expected=1)

    # --- inputs ------------------------------------------------------------------
    def test_empty_input_blocks(self):
        self.compare("", "", expected=2)

    def test_metadata_header_blocks(self):
        self.compare("A = 10.", "applied: F1\n---\nA = 10.", expected=2)

    def test_output_cannot_overwrite_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            prose = Path(tmp) / "prose.txt"
            prose.write_text("Original prose.", encoding="utf-8")
            result = subprocess.run([sys.executable, str(CLI), "--before", str(prose), "--after", str(prose),
                                     "--citation-style", "none", "--output", str(prose)], capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(prose.read_text(encoding="utf-8"), "Original prose.")


if __name__ == "__main__":
    unittest.main()
