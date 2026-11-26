#!/usr/bin/env python3
"""Regression tests for brickyard.py on a two-paper toy corpus.

    python test_brickyard.py        (exit 0 when every case passes)
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
BY = [sys.executable, str(HERE / "brickyard.py")]

LOGIC_1 = """# Logic — alpha-2020

## E. Sentence frame catalog

### E.3 Results

| # | Frame Type | Abstracted Template | Original Sentence | Source | Status |
|---|---|---|---|---|---|
| 1 | F3 Range-Report | "[VAR] ranged from [MIN] to [MAX], with a mean of [MEAN]." | "Nitrate ranged from 2 to 9 mg/L, with a mean of 5 mg/L." | [P10-S1] | Singleton |
| 2 | F8 Group-Comparison | "[A] exhibited [X], whereas [B] showed [Y]." | "Wells exhibited high values, whereas springs showed low values." | [P10-S2] | Singleton |
| 3 | G1 Results-Suggest | "These [PATTERNS] suggest(s)/indicate(s) that [INTERPRETATION]." | "These patterns suggest that manure is the source." | [P10-S3] | Recurrent |

### E.4 Discussion

| # | Frame Type | Abstracted Template | Original Sentence | Source |
|---|---|---|---|---|
| 4 | G4 Likely-Due-To | "[OBSERVATION] is likely due to [CAUSE]." | "The rise is likely due to fertiliser." | [P20-S1] |
"""

LOGIC_2 = """# Logic — beta-2021

## E. Frames

### Results and discussion

| # | Frame Type | Abstracted Template | Original Sentence | Source |
|---|---|---|---|---|
| 1 | F5 Figure-Reference | "As shown in [FIGURE], [FINDING]." | "As shown in Fig. 2, chloride increased downstream." | [P7-S1] |
| 2 | Z: Assumption-Rider | "[CLAIM], assuming that [ASSUMPTION]." | "The flux was constant, assuming that recharge was uniform." | [P7-S2] |
"""

SECTIONS_1 = ("Nitrate ranged from 2 to 9 mg/L, with a mean of 5 mg/L. Wells exhibited high "
              "values, whereas springs showed low values. These patterns suggest that manure "
              "is the source of the nitrate in the shallow aquifer of the basin. Recharge governs "
              "the flux, and evaporation governs the salinity, which likely indicates mixing.\n")
SECTIONS_2 = ("As shown in Fig. 2, chloride increased downstream. The flux was constant, "
              "assuming that recharge was uniform.\n")

PHRASES = ("phrase\tn\tI\tR\ttotal\tper_million\trange\tbundle\ttopic\tnested_in\tfunction\tsubfunction\n"
           "as a result of\t4\t1\t2\t3\t300\t2\tyes\tno\t\ttext\tresultative\n"
           "the nitrate concentrations\t3\t1\t3\t4\t400\t2\tyes\tyes\t\t\t\n")

WORDLIST = ("type\tR\ttotal\trange\tfamily\tpos\tclass\n"
            "governs\t2\t2\t1\tgovern\tVERB\tother\n"
            "higher\t1\t1\t1\thigh\tADJ\tother\n"
            "nitrate\t2\t2\t1\tnitrate\tNOUN\tother\n")

STYLE_VOCAB = """# Style vocabulary — alpha-2020

## C. Style lexicon

### Reporting verbs

| verb | total | R |
|---|---|---|
| indicat* | 1 | 1 |
| show* | 1 | 1 |

### Hedges

| item | total |
|---|---|
| *likely* | 1 |

### Lexical bundles

| bundle | total |
|---|---|
| as a result of | 3 |
"""

GLOSSARY = """# Technical-term glossary: Alpha 2020

**Counting source**: sections governs likely values

| # | Term | Type | POS |
|---|---|---|---|
| 1 | pyrite oxidation | Domain | NOUN |
"""

DRAFT = ("Sulfate values ranged between 12 and 40 mg/L and the average was 22 mg/L (Fig. 3). "
         "Deep wells had higher sulfate than shallow wells. This means pyrite oxidation "
         "controls sulfate (Kim et al., 2015).\n")

CONTENT = """C1\tSulfate values
C2\t12
C3\t40 mg/L
C4\t22 mg/L (Fig. 3)
C5\tDeep wells
C6\thigher sulfate
C7\tshallow wells
C8\tpyrite oxidation controls sulfate (Kim et al., 2015)
C9\tthe average
"""

PLAN = {"paragraphs": [{"function": "Finding", "sentences": [
    {"frame": "F001", "fill": {"VAR": ["C1"], "MIN": ["C2"], "MAX": ["C3"], "MEAN": ["C4"]}},
    {"frame": "F002", "fill": {"A": ["C5"], "X": ["C6"], "B": ["C7"], "Y": ["?:the shallow-well contrast"]}},
    {"frame": "F003", "fill": {"PATTERNS": ["g:values"], "INTERPRETATION": ["C8"]},
     "pick": {"suggest(s)/indicate(s)": "suggest"}},
]}]}


def run(*args, cwd=None):
    r = subprocess.run(BY + [str(a) for a in args], capture_output=True, text=True,
                       encoding="utf-8", cwd=cwd)
    return r.returncode, r.stdout + r.stderr


def setup(tmp: Path):
    for slug, logic, sec, sec_id in (("alpha-2020", LOGIC_1, SECTIONS_1, "R"),
                                     ("beta-2021", LOGIC_2, SECTIONS_2, "R")):
        p = tmp / "corpus" / "papers" / slug
        (p / "sections").mkdir(parents=True)
        (p / "logic.md").write_text(logic, encoding="utf-8")
        (p / "sections" / f"{sec_id}.txt").write_text(sec, encoding="utf-8")
    (tmp / "corpus/papers/alpha-2020/phrases.tsv").write_text(PHRASES, encoding="utf-8")
    (tmp / "corpus/papers/alpha-2020/wordlist.tsv").write_text(WORDLIST, encoding="utf-8")
    (tmp / "corpus/papers/alpha-2020/style-vocab.md").write_text(STYLE_VOCAB, encoding="utf-8")
    (tmp / "corpus/papers/alpha-2020/glossary.md").write_text(GLOSSARY, encoding="utf-8")
    (tmp / "draft.txt").write_text(DRAFT, encoding="utf-8")


CASES = []


def case(fn):
    CASES.append(fn)
    return fn


@case
def pile_parses_frames_and_bundles(t):
    code, out = run("pile", "--corpus", t / "corpus", "--section", "R",
                    "--draft", t / "draft.txt", "--out", t / "pile")
    assert code == 0, out
    form = (t / "pile/form.tsv").read_text(encoding="utf-8")
    assert "F001\tframe\talpha-2020\tR\tF3" in form, form
    assert "Assumption-Rider" in form and "beta-2021" in form, form
    assert "G4" not in form, "a Discussion frame leaked into an R pile"
    assert "as a result of" in form and "the nitrate concentrations" not in form, form
    assert "D3" in (t / "pile/draft.tsv").read_text(encoding="utf-8")


@case
def content_must_be_verbatim(t):
    (t / "pile/content.tsv").write_text(CONTENT + "C10\tsulphate values\n", encoding="utf-8")
    code, out = run("content", "--pile", t / "pile")
    assert code == 1 and "C10" in out, out
    (t / "pile/content.tsv").write_text(CONTENT, encoding="utf-8")
    code, out = run("content", "--pile", t / "pile")
    assert code == 0, out


@case
def assemble_builds_from_ids_only(t):
    (t / "plan.json").write_text(json.dumps(PLAN), encoding="utf-8")
    code, out = run("assemble", "--pile", t / "pile", "--plan", t / "plan.json",
                    "--out", t / "revision.txt", "--trace", t / "trace.tsv")
    assert code != 0 and "values" in out, "glue outside the frozen list must fail: " + out
    PLAN["paragraphs"][0]["sentences"][2]["fill"]["PATTERNS"] = []
    PLAN["paragraphs"][0]["sentences"][2]["inflect"] = {}
    (t / "plan.json").write_text(json.dumps(PLAN), encoding="utf-8")
    code, out = run("assemble", "--pile", t / "pile", "--plan", t / "plan.json",
                    "--out", t / "revision.txt", "--trace", t / "trace.tsv")
    assert code == 0, out
    text = (t / "revision.txt").read_text(encoding="utf-8")
    assert text.startswith("Sulfate values ranged from 12 to 40 mg/L, with a mean of 22 mg/L (Fig. 3)."), text
    assert "Deep wells exhibited higher sulfate, whereas shallow wells showed [YOU WRITE: the shallow-well contrast]." in text, text
    assert "These suggest that pyrite oxidation" in text, text


@case
def verify_passes_clean_assembly(t):
    code, out = run("verify", "--pile", t / "pile", "--plan", t / "plan.json",
                    "--revision", t / "revision.txt", "--report", t / "verify.md")
    assert code == 0, out
    assert "built on a corpus frame: 3 of 3" in out, out
    assert "gaps: 1 of 3" in out, out
    assert "C9" in out, "unused content brick must be reported"


@case
def verify_catches_hand_edit(t):
    good = (t / "revision.txt").read_text(encoding="utf-8")
    (t / "revision.txt").write_text(good.replace("exhibited", "had"), encoding="utf-8")
    code, out = run("verify", "--pile", t / "pile", "--plan", t / "plan.json",
                    "--revision", t / "revision.txt")
    assert code == 1 and "edited by hand" in out, out
    (t / "revision.txt").write_text(good, encoding="utf-8")


@case
def inflect_is_whitelisted(t):
    plan = {"paragraphs": [[{"frame": "F005", "fill": {"CLAIM": ["C5"], "ASSUMPTION": ["C8"]},
                             "inflect": {"assuming": "presuming"}}]]}
    (t / "p2.json").write_text(json.dumps(plan), encoding="utf-8")
    code, out = run("assemble", "--pile", t / "pile", "--plan", t / "p2.json", "--out", t / "r2.txt")
    assert code == 1 and "not an agreement change" in out, out


@case
def too_many_gaps_fail(t):
    plan = {"paragraphs": [[{"gap": "a"}, {"gap": "b"}, {"gap": "c"}, {"gap": "d"}]]}
    (t / "p3.json").write_text(json.dumps(plan), encoding="utf-8")
    code, out = run("assemble", "--pile", t / "pile", "--plan", t / "p3.json", "--out", t / "r3.txt")
    assert code == 1 and "at most 3" in out, out


@case
def whole_sentences_need_own_corpus(t):
    code, out = run("pile", "--corpus", t / "corpus", "--section", "R", "--unit", "sentence",
                    "--draft", t / "draft.txt", "--out", t / "spile")
    assert code == 0, out
    (t / "spile/content.tsv").write_text(CONTENT, encoding="utf-8")
    plan = {"paragraphs": [[{"sentence": "S003"}, {"keep": "D3"}]]}
    (t / "p4.json").write_text(json.dumps(plan), encoding="utf-8")
    code, out = run("assemble", "--pile", t / "spile", "--plan", t / "p4.json", "--out", t / "r4.txt")
    assert code == 0, out
    code, out = run("verify", "--pile", t / "spile", "--plan", t / "p4.json", "--revision", t / "r4.txt")
    assert code == 1 and "--own-corpus" in out and "8-word run" in out, out
    code, out = run("verify", "--pile", t / "spile", "--plan", t / "p4.json", "--revision", t / "r4.txt",
                    "--own-corpus")
    assert code == 0, out


@case
def word_pile_reads_corpus_layers(t):
    words = (t / "pile/word.tsv").read_text(encoding="utf-8")
    assert "\tgoverns\tpos:VERB\t-\tVERB" in words, words
    assert "\tindicates\treporting\treport:tentative" in words, words
    assert "\tlikely\thedge\thedge" in words, words
    assert "nitrate" not in words, "nouns are not word bricks"
    assert "as a result of" not in words, "bundle tables are not word bricks"
    assert "pyrite oxidation" in (t / "pile/terms.txt").read_text(encoding="utf-8")
    assert "Counting source" not in (t / "pile/terms.txt").read_text(encoding="utf-8"), \
        "glossary prose lines are not terms"


def wid(t, form):
    for ln in (t / "pile/word.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        c = ln.split("\t")
        if c[1] == form:
            return c[0]
    raise AssertionError(f"{form} not in word.tsv")


def assemble_with(t, swaps, plan=None):
    (t / "pile/swaps-test.json").write_text(json.dumps(swaps), encoding="utf-8")
    try:
        return run("assemble", "--pile", t / "pile", "--plan", plan or (t / "plan.json"),
                   "--out", t / "rw.txt", "--trace", t / "tw.tsv")
    finally:
        (t / "pile/swaps-test.json").unlink()


@case
def word_swap_applies_and_traces(t):
    g = wid(t, "governs")
    code, out = assemble_with(t, {"C8": {"controls": g}})
    assert code == 0, out
    text = (t / "rw.txt").read_text(encoding="utf-8")
    assert "pyrite oxidation governs sulfate (Kim et al., 2015)" in text, text
    assert f"word\t{g}\tgoverns" in (t / "tw.tsv").read_text(encoding="utf-8")


@case
def word_swap_keeps_claim_strength(t):
    code, out = assemble_with(t, {"C8": {"controls": wid(t, "indicates")}})
    assert code == 1 and "claim strength - -> report:tentative" in out, out


@case
def word_swap_never_touches_terms(t):
    code, out = assemble_with(t, {"C8": {"oxidation": wid(t, "governs")}})
    assert code == 1 and "protected technical term" in out, out


@case
def word_swap_keeps_part_of_speech(t):
    code, out = assemble_with(t, {"C6": {"higher": wid(t, "governs")}})
    assert code == 1 and "part of speech ADJ -> VERB" in out, out


@case
def conflicting_swap_files_fail(t):
    (t / "pile/swaps-a.json").write_text(json.dumps({"C8": {"controls": wid(t, "governs")}}), encoding="utf-8")
    code, out = assemble_with(t, {"C8": {"controls": wid(t, "indicates")}})
    (t / "pile/swaps-a.json").unlink()
    assert code == 1 and "swapped to both" in out, out


@case
def verify_reports_word_layer(t):
    (t / "pile/swaps.json").write_text(json.dumps({"C8": {"controls": wid(t, "governs")}}), encoding="utf-8")
    code, out = run("assemble", "--pile", t / "pile", "--plan", t / "plan.json", "--out", t / "rv.txt")
    assert code == 0, out
    code, out = run("verify", "--pile", t / "pile", "--plan", t / "plan.json",
                    "--revision", t / "rv.txt", "--report", t / "vv.md")
    (t / "pile/swaps.json").unlink()
    assert code == 0, out
    assert "- swaps: 1 (pos:VERB 1)" in out, out
    assert "draft words the corpus never uses" in out and "sulfate" in out, out
    assert (t / "word-swaps.tsv").exists()


@case
def tampered_pile_fails(t):
    form = t / "pile/form.tsv"
    good = form.read_text(encoding="utf-8")
    form.write_text(good.replace("exhibited [X]", "displayed [X]"), encoding="utf-8")
    code, out = run("verify", "--pile", t / "pile", "--plan", t / "plan.json",
                    "--revision", t / "revision.txt")
    assert code == 1 and "differs from the corpus" in out, out
    form.write_text(good, encoding="utf-8")


@case
def splitter_keeps_page_references(t):
    import brickyard
    par = ("EIA has attracted criticism (Smith et al., 2018, p. 509, Table 2). Critiques "
           "trace this to procedure (Cashmore, 2004, pp. 403, 421–422) and to assumptions. "
           "The group. Next sentence.")
    got = brickyard.split_sentences(par)
    assert len(got) == 4, got
    assert got[0].endswith("p. 509, Table 2)."), got
    assert got[2] == "The group.", got


@case
def parser_reads_other_catalog_layouts(t):
    import brickyard
    p = t / "layout-logic.md"
    p.write_text(
        "## C. Inter-paragraph logic\n\n### C — Conclusions\n\ntext\n\n"
        "## E. Verified sentence frames\n\n### I\n\n"
        "| # | Frame | Template | Original | Address |\n|---|---|---|---|---|\n"
        "| 1 | A3 Trend | [X] have long been [Y]. | Scientists have long been keen. | P1-S1 |\n\n"
        "## Exhaustive frame catalogue\n\n### I\n\n"
        "| Source | Section | Frame type | Frame with slots | Verbatim text | Class |\n"
        "| --- | --- | --- | --- | --- | --- |\n"
        "| [P2-S1] | M | A1 | `Central to [X] is [Y].` | Central to this is that. | Singleton |\n",
        encoding="utf-8")
    rows = brickyard.parse_logic(p)
    assert len(rows) == 2, rows
    assert rows[0]["section"] == "I" and rows[0]["template"] == "[X] have long been [Y].", rows[0]
    assert rows[1]["section"] == "M", rows[1]            # the Section cell beats the heading
    assert rows[1]["status"] == "Singleton" and rows[1]["source"] == "[P2-S1]", rows[1]


@case
def penn_tags_feed_the_word_pile(t):
    import brickyard
    assert brickyard.upos("VBZ") == "VERB" and brickyard.upos("JJ") == "ADJ" and brickyard.upos("RB") == "ADV"
    assert brickyard.upos("VB/VBP") == "VERB" and brickyard.upos("ADJ") == "ADJ"
    assert brickyard.pos_compatible("VBZ", "VBZ") and brickyard.pos_compatible("VBD", "VBN")
    assert not brickyard.pos_compatible("VBZ", "VBG") and not brickyard.pos_compatible("JJ", "RB")
    assert brickyard.pos_compatible("VERB", "VBZ")          # universal vs Penn: class only
    c = t / "penn"
    p = c / "papers" / "gamma-2022"
    (p / "sections").mkdir(parents=True)
    (p / "sections" / "I.txt").write_text("Governance remains contested and contested again.", encoding="utf-8")
    (p / "wordlist.tsv").write_text("type\tI\ttotal\tpos\ncontested\t2\t2\tVBN\nremains\t1\t1\tVBZ\n",
                                    encoding="utf-8")
    rows, _, _ = brickyard.build_words(c, "I", ["gamma-2022"], False, set())
    forms = {r["form"]: r for r in rows}
    assert "contested" in forms and forms["contested"]["category"] == "pos:VERB", rows
    assert "remains" not in forms, "Freq < 2 rows stay out"


@case
def content_transforms_are_mechanical_and_attested(t):
    import types
    import brickyard
    assert brickyard.verb_form("bringing", "base", {"bring", "bringing"}) == "bring"
    assert brickyard.verb_form("using", "base", {"us", "use"}) == "use"
    assert brickyard.verb_form("decide", "ing", {"deciding"}) == "deciding"
    assert brickyard.verb_form("treats", "base", {"treat"}) == "treat"
    assert brickyard.verb_form("bring", "ed", {"brought"}) == "brought"
    assert brickyard.verb_form("bringing", "base", {"bringing"}) is None   # not attested -> refused
    pile = types.SimpleNamespace(
        content={"C1": "a routine part of decisions", "C2": "bringing evidence to bear"},
        swaps={}, attested={"bring"}, draft_text="", terms=set(), words={}, pos_map={})
    asm = brickyard.Assembly()
    txt, kind, cid = brickyard.render_item("C1|-det", pile, "P1.S1", asm, [])
    assert txt == "routine part of decisions" and cid == "C1", txt
    txt, _, _ = brickyard.render_item("C2|base", pile, "P1.S1", asm, [])
    assert txt == "bring evidence to bear", txt
    assert not asm.errors, asm.errors
    assert sum(1 for x in asm.trace if x["kind"] == "transform") == 2
    brickyard.render_item("C2|-det", pile, "P1.S1", asm, [])
    brickyard.render_item("C1|ing", pile, "P1.S1", asm, [])
    assert len(asm.errors) == 2, asm.errors                # no determiner; 'a' has no -ing form


STAGE1_OK = {"sentences": [
    {"from": ["D1"], "frame": "F001",
     "text": "Sulfate values ranged from 12 to 40 mg/L, with a mean of 22 mg/L (Fig. 3)."},
    {"from": ["D2"], "frame": "F002",
     "text": "Deep wells exhibited higher sulfate, whereas shallow wells showed lower sulfate."},
    {"from": ["D3"], "frame": "F003",
     "text": "These contrasts suggest that pyrite oxidation controls sulfate (Kim et al., 2015)."},
]}


@case
def stage1_guided_rewrite_passes_and_feeds_stage2(t):
    pile = t / "pile-s1"
    code, out = run("pile", "--corpus", t / "corpus", "--section", "R",
                    "--draft", t / "draft.txt", "--out", pile)
    assert code == 0, out
    (t / "s1.json").write_text(json.dumps(STAGE1_OK), encoding="utf-8")
    code, out = run("stage1", "--pile", pile, "--stage1", t / "s1.json",
                    "--plan-out", t / "s1-plan.json", "--report", t / "s1.md")
    assert code == 0, out
    assert "sentences on a declared frame: 3 of 3" in out, out
    assert "contrasts" in out and "lower" in out, "new words are listed"
    assert "between" in out and "average" in out, "lost draft words are listed"
    plan = json.loads((t / "s1-plan.json").read_text(encoding="utf-8"))
    assert [s["stage1"] for s in plan["paragraphs"][0]["sentences"]] == ["T1", "T2", "T3"], plan
    words_tsv = (pile / "word.tsv").read_text(encoding="utf-8")
    wid = next(ln.split("\t")[0] for ln in words_tsv.splitlines() if "\tgoverns\t" in ln)
    (pile / "swaps.json").write_text(json.dumps({"T3": {"controls": wid}}), encoding="utf-8")
    code, out = run("assemble", "--pile", pile, "--plan", t / "s1-plan.json",
                    "--out", t / "s1-rev.txt", "--trace", t / "s1-trace.tsv")
    assert code == 0, out
    rev = (t / "s1-rev.txt").read_text(encoding="utf-8")
    assert "These contrasts suggest that pyrite oxidation governs sulfate (Kim et al., 2015)." in rev, rev
    code, out = run("verify", "--pile", pile, "--plan", t / "s1-plan.json",
                    "--revision", t / "s1-rev.txt", "--report", t / "s1-verify.md")
    assert code == 0, out
    assert "## Stage 1" in out and "mean fit" in out, out
    assert (t / "revision.gate1.txt").exists()


@case
def stage1_catches_low_fit_lost_citation_and_uncovered_sentence(t):
    pile = t / "pile-s1"
    bad = {"sentences": [
        {"from": ["D1"], "frame": "F001",
         "text": "Sulfate values were between 12 and 40 mg/L, averaging 22 mg/L (Fig. 3)."},
        {"from": ["D3"], "frame": "F003",
         "text": "These contrasts suggest that pyrite oxidation controls sulfate."},
    ]}
    (t / "s1-bad.json").write_text(json.dumps(bad), encoding="utf-8")
    code, out = run("stage1", "--pile", pile, "--stage1", t / "s1-bad.json",
                    "--plan-out", t / "s1-bad-plan.json")
    assert code == 1, out
    assert "F001 fit" in out, "frame not followed"
    assert "D2 is not rewritten" in out, "uncovered draft sentence"
    assert "'2015'" in out, "citation dropped"


@case
def swaps_carry_collocation_evidence(t):
    # runs after the guided-rewrite case: its verify wrote word-swaps.tsv next to s1-verify.md
    rows = (t / "word-swaps.tsv").read_text(encoding="utf-8").splitlines()
    head = rows[0].split("	")
    for col in ("left_pair", "left_n", "right_pair", "right_n", "collocation"):
        assert col in head, head
    row = dict(zip(head, rows[1].split("	")))
    assert row["left_pair"] == "oxidation governs", row
    assert row["right_pair"] == "governs sulfate", row
    assert row["collocation"] in ("attested", "unattested"), row
    out = (t / "s1-verify.md").read_text(encoding="utf-8")
    assert "- collocation:" in out, out


def msent_id(pile, prefix):
    for ln in (pile / "msent.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        cols = ln.split("\t")
        if cols[-1].startswith(prefix):
            return cols[0]
    raise AssertionError(f"no corpus sentence starting {prefix!r}")


@case
def corpus_sentence_base_and_verbatim_reuse(t):
    # base: a corpus sentence becomes a frame; its own content words are its slots
    pile = t / "pile-m"
    code, out = run("pile", "--corpus", t / "corpus", "--section", "R",
                    "--draft", t / "draft.txt", "--out", pile)
    assert code == 0, out
    code, out = run("match", "--pile", pile, "--top", "3")
    assert code == 0 and "corpus sentences indexed" in out, out
    assert (pile / "match.tsv").exists()
    mid = msent_id(pile, "These patterns suggest")
    spec = json.loads(json.dumps(STAGE1_OK))
    spec["sentences"][2] = {"from": ["D3"], "base": mid,
                            "text": "This means that pyrite oxidation is the control of the sulfate "
                                    "in the wells of the area (Kim et al., 2015)."}
    (t / "m1.json").write_text(json.dumps(spec), encoding="utf-8")
    code, out = run("stage1", "--pile", pile, "--stage1", t / "m1.json",
                    "--plan-out", t / "m1-plan.json", "--report", t / "m1.md")
    assert code == 0, out
    assert f"| T3 | D3 | {mid} | base |" in out, out
    # a base that keeps too little of itself is refused
    spec["sentences"][1] = {"from": ["D2"], "base": msent_id(pile, "Wells exhibited"),
                            "text": "Deep wells had higher sulfate than shallow wells."}
    (t / "m2.json").write_text(json.dumps(spec), encoding="utf-8")
    code, out = run("stage1", "--pile", pile, "--stage1", t / "m2.json", "--plan-out", t / "m2-plan.json")
    assert code == 1 and "too little of it survives" in out, out
    # verbatim: a draft sentence whose content is a corpus sentence's
    (t / "draft-v.txt").write_text("Recharge governs the flux and evaporation controls the salinity, "
                                   "which likely indicates mixing.\n", encoding="utf-8")
    pv = t / "pile-v"
    code, out = run("pile", "--corpus", t / "corpus", "--section", "R",
                    "--draft", t / "draft-v.txt", "--out", pv)
    assert code == 0, out
    code, out = run("match", "--pile", pv)
    assert "SAME CONTENT" in out, out
    vid = msent_id(pv, "Recharge governs")
    text = [ln.split("\t")[-1] for ln in (pv / "msent.tsv").read_text(encoding="utf-8").splitlines()
            if ln.startswith(vid + "\t")][0]
    (t / "v.json").write_text(json.dumps({"sentences": [{"from": ["D1"], "base": vid, "text": text}]}),
                              encoding="utf-8")
    code, out = run("stage1", "--pile", pv, "--stage1", t / "v.json", "--plan-out", t / "v-plan.json")
    assert code == 0 and "VERBATIM" in out and "verbatim corpus sentences: 1" in out, out
    code, out = run("assemble", "--pile", pv, "--plan", t / "v-plan.json", "--out", t / "v-rev.txt")
    assert code == 0, out
    code, out = run("verify", "--pile", pv, "--plan", t / "v-plan.json", "--revision", t / "v-rev.txt")
    assert code == 1 and "repeat a 8-word run" in out, "a verbatim corpus sentence fails the copy check"
    code, out = run("verify", "--pile", pv, "--plan", t / "v-plan.json", "--revision", t / "v-rev.txt",
                    "--allow-copy")
    assert code == 0, out


def main():
    failed = 0
    with tempfile.TemporaryDirectory() as d:
        t = Path(d)
        setup(t)
        for fn in CASES:
            try:
                fn(t)
                print(f"ok    {fn.__name__}")
            except AssertionError as e:
                failed += 1
                print(f"FAIL  {fn.__name__}\n{e}")
    print(f"{len(CASES) - failed}/{len(CASES)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
