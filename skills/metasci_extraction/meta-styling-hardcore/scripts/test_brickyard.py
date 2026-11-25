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

GLOSSARY = """| # | Term | Type | POS |
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
