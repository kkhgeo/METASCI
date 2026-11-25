#!/usr/bin/env python3
"""Regression cases for structure_map.py. Run: python scripts/test_structure_map.py"""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import structure_map as sm  # noqa: E402

ASSETS = HERE.parent / "assets"
EXAMPLE = json.loads((ASSETS / "example-map.json").read_text(encoding="utf-8"))
DRAFT = sm.read_paragraphs(ASSETS / "example-draft.md")


def run(m, paras=None):
    m = copy.deepcopy(m)
    err, warn = sm.validate(m, paras)
    return err, warn, (None if err else sm.checks(m))


def codes(found):
    return sorted(c["code"] for c in found)


class Example(unittest.TestCase):
    def test_example_is_valid_against_its_draft(self):
        err, warn, found = run(EXAMPLE, DRAFT)
        self.assertEqual(err, [])
        self.assertEqual(warn, [])
        self.assertEqual(codes(found), ["forward-reference", "orphan", "term-before-definition",
                                        "weak-transition", "weak-transition"])

    def test_draft_paragraphs_skip_headings_and_comments(self):
        self.assertEqual(len(DRAFT), 17)
        self.assertTrue(DRAFT[0].startswith("Nitrate contamination"))

    def test_build_writes_html_with_escaped_data(self):
        m = copy.deepcopy(EXAMPLE)
        m["title"] = "</script><b>x</b>"
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "map.json"
            src.write_text(json.dumps(m), encoding="utf-8")
            out = Path(d) / "map.html"
            self.assertEqual(sm.main(["build", str(src), "-o", str(out)]), 0)
            page = out.read_text(encoding="utf-8")
            self.assertNotIn("/*__MAP_DATA__*/null", page)
            self.assertEqual(page.count("</script>"), 1)  # only the template's own closing tag
            self.assertIn("<title>&lt;/script&gt;&lt;b&gt;x&lt;/b&gt;</title>", page)


class Validation(unittest.TestCase):
    def test_paraphrased_topic_is_an_error(self):
        m = copy.deepcopy(EXAMPLE)
        m["paragraphs"][0]["topic"] = "Nitrate pollution endangers rural water."
        err, _, _ = run(m, DRAFT)
        self.assertTrue(any("P1" in e and "그대로" in e for e in err))

    def test_explicit_link_needs_signal_and_draft_link_needs_address(self):
        m = copy.deepcopy(EXAMPLE)
        m["links"][0].pop("signal")
        m["links"][1].pop("at")
        err, _, _ = run(m)
        self.assertTrue(any("signal" in e for e in err))
        self.assertTrue(any("at(" in e for e in err))

    def test_unknown_kind_endpoint_and_order(self):
        m = copy.deepcopy(EXAMPLE)
        m["links"][0]["kind"] = "supports"
        m["links"][1]["to"] = "P99"
        m["paragraphs"][1], m["paragraphs"][2] = m["paragraphs"][2], m["paragraphs"][1]
        err, _, _ = run(m)
        self.assertTrue(any("supports" in e for e in err))
        self.assertTrue(any("P99" in e for e in err))
        self.assertTrue(any("읽기 순서" in e for e in err))

    def test_address_beyond_sentence_count(self):
        m = copy.deepcopy(EXAMPLE)
        m["citations"][0]["at"] = ["P2-S9"]
        err, _, _ = run(m)
        self.assertTrue(any("P2-S9" in e for e in err))

    def test_outline_map_needs_no_addresses(self):
        m = copy.deepcopy(EXAMPLE)
        m["source"] = {"kind": "outline"}
        for p in m["paragraphs"]:
            p.pop("topic_at")
        for l in m["links"]:
            l.pop("at")
            l["basis"] = "planned"
        err, _, found = run(m)
        self.assertEqual(err, [])
        self.assertIn("forward-reference", codes(found))

    def test_planned_basis_is_refused_in_a_draft(self):
        m = copy.deepcopy(EXAMPLE)
        m["links"][0]["basis"] = "planned"
        err, _, _ = run(m)
        self.assertTrue(any("planned" in e for e in err))


class Checks(unittest.TestCase):
    def test_forward_ok_silences_a_deliberate_signpost(self):
        m = copy.deepcopy(EXAMPLE)
        for l in m["links"]:
            if l["from"] == "P15":
                l["forward_ok"] = True
        _, _, found = run(m)
        self.assertNotIn("forward-reference", codes(found))

    def test_result_without_method(self):
        m = copy.deepcopy(EXAMPLE)
        m["links"] = [l for l in m["links"] if not (l["to"] == "P9" and l["kind"] == "method")]
        _, _, found = run(m)
        self.assertIn(("result-without-method", ["P9"]), [(c["code"], c["ids"]) for c in found])

    def test_method_check_waits_for_a_methods_section(self):
        m = copy.deepcopy(EXAMPLE)
        keep = {"S3", "S4"}
        m["sections"] = [s for s in m["sections"] if s["id"] in keep]
        ids = {p["id"] for p in m["paragraphs"] if p["section"] in keep}
        m["paragraphs"] = [p for p in m["paragraphs"] if p["id"] in ids]
        m["links"] = [l for l in m["links"] if l["from"] in ids and l["to"] in ids]
        m["citations"], m["main_claims"] = [], []
        m["terms"] = [{"term": "corrected contribution", "defined_at": "P15-S1"}]
        err, _, found = run(m)
        self.assertEqual(err, [])
        self.assertNotIn("result-without-method", codes(found))
        self.assertNotIn("orphan", codes(found))

    def test_unanswered_question(self):
        m = copy.deepcopy(EXAMPLE)
        m["links"] = [l for l in m["links"] if not (l["from"] in ("P3", "P4") and l["kind"] == "answers" and l["to"] in ("P12", "P17"))]
        _, _, found = run(m)
        got = [c["ids"][0] for c in found if c["code"] == "unanswered-question"]
        self.assertEqual(got, ["P3", "P4"])

    def test_cycle_and_hub(self):
        m = copy.deepcopy(EXAMPLE)
        m["links"].append({"from": "P13", "to": "P12", "kind": "evidence", "at": "P12-S2", "basis": "inferred", "note": "x"})
        p12 = next(p for p in m["paragraphs"] if p["id"] == "P12")
        p12["sentences"] = 9
        for src in ("P1", "P2", "P5", "P8"):
            m["links"].append({"from": src, "to": "P12", "kind": "evidence", "at": "P12-S1", "basis": "inferred", "note": "x"})
        _, _, found = run(m)
        self.assertIn("cycle", codes(found))
        self.assertIn("overloaded", codes(found))

    def test_korean_term_matches_with_particles(self):
        paras = ["보정 기여율은 48%이다.", "보정 기여율을 정의한다."]
        m = {"$schema": sm.SCHEMA, "source": {"kind": "draft"},
             "sections": [{"id": "S1", "label": "논의", "type": "discussion"}],
             "paragraphs": [{"id": "P1", "section": "S1", "role": "Finding", "topic": "보정 기여율은 48%이다.", "topic_at": "P1-S1", "sentences": 1},
                            {"id": "P2", "section": "S1", "role": "Definition", "topic": "보정 기여율을 정의한다.", "topic_at": "P2-S1", "sentences": 1,}],
             "links": [], "terms": [{"term": "보정 기여율", "defined_at": "P2-S1"}]}
        err, _, found = run(m, paras)
        self.assertEqual(err, [])
        self.assertIn("term-before-definition", codes(found))


if __name__ == "__main__":
    unittest.main(verbosity=1)
