#!/usr/bin/env python3
"""brickyard.py — meta-styling-hardcore: the model picks bricks by ID, code builds the text.

The model never types a sentence of the revision. It writes a plan (plan.json) that
names bricks by ID; this script assembles the text from those IDs and verifies that
every word of the result traces to a brick.

  pile      corpus + draft      -> pile/ (form.tsv, draft.tsv, pile.json)
  stage1    pile + stage1.json  -> pile/stage1.*, stage-2 plan.json   (guided mode, 1.3.0)
  match     pile                -> pile/msent.tsv, pile/match.tsv     (corpus-sentence bases, 1.5.0)
  content   pile + content.tsv  -> validates the content bricks against the draft
  assemble  pile + plan.json    -> revision.txt, trace.tsv
  verify    pile + plan.json + revision.txt -> verify.md   (exit 0 PASS, 1 FAIL, 2 BLOCKED)

BRICKS
------
Form bricks come from the style corpus (extraction-style v3.x):
  F###  sentence frame — the "Abstracted Template" of a logic.md §E catalog row,
        with [SLOT]s. Its fixed words are corpus words; its slots take content.
  B###  lexical bundle — a phrases.tsv row with bundle = yes and topic = no.
  S###  whole corpus sentence — the "Original Sentence" column. Only with
        `pile --unit sentence`, and `verify` fails it unless --own-corpus.
Content bricks come from the draft:
  C#    a verbatim span of the draft prose, listed by the model in content.tsv.
  D#    a whole draft sentence (numbered by `pile`), used only through {"keep": "D#"}.
Word bricks (1.1.0):
  W###  one corpus word or short item — style-vocab.md tables (reporting verbs, hedges,
        boosters, connectives ...) and wordlist.tsv VERB/ADV/ADJ rows at Freq >= 2,
        attested in the target section, technical terms excluded. swaps.json replaces a
        word inside a C# or D# brick with a W### form: same claim-strength class, same
        part of speech when both are known, never a protected term, never negation.
Mortar (the only things that are not bricks, all counted in verify.md):
  g:<word>    a glue word from the frozen GLUE list below
  ?:<text>    a [YOU WRITE: text] gap, one line, at most MAX_GAPS per run
  pick        choosing one alternative of a template choice token (was/were, suggest(s))
  inflect     a number-agreement change on a template word, from AGREEMENT or a
              regular -s/-es/-ies toggle
  auto        capitalisation, a/an, spacing before punctuation, terminal period
  transform   (1.2.0) a counted, mechanical change to a content brick written as
              C#|op[,op]: -det drops a leading determiner (a, an, the, this ...);
              base / s / ing / ed set the verb form of the brick's first word. The new
              form must be attested in the corpus or the draft. Nothing else changes.

No dependencies beyond the standard library.
Version: 1.5.1 (2026-11-26) — glossary.md: only its numbered table rows are read as
terms (prose lines no longer leak general words into the protected list).
Previous: 1.5.0 (2026-11-26) — corpus-sentence bases: `match` indexes the corpus
sentences (M###) and ranks them per draft sentence by content overlap; a stage-1 record
may name {"base": "M###"}: the sentence becomes a frame whose slots are its own content
words, digits and names that the draft sentence lacks; a text identical to it is a
verbatim reuse, flagged; verify --allow-copy turns corpus-run failures into warnings.
Previous: 1.4.0 (2026-11-26) — collocation evidence for every swap in word-swaps.tsv.
Previous: 1.3.0 (2026-11-26) — guided mode: `stage1` checks a rewrite of each draft
sentence on one declared frame (fixed-word fit, new-word share, lost draft words,
digits and citations) and writes a stage-2 plan of T# sentences; swaps key on T# and
may insert lexical bundles (B###); verify reports stage 1 and writes revision.gate1.txt
(gaps removed) for Gate 1.
Previous: 1.2.0 (2026-11-26) — content transforms (C#|-det, C#|base/s/ing/ed) so a
draft span can enter a frame slot that wants another verb form or no article;
Penn Treebank tags (JJ, VBZ, RB ...) read as well as universal tags, so a tagged
wordlist.tsv feeds the word pile; part-of-speech check compares like with like;
page references (p. 12, pp. 3-4) no longer split sentences; frame catalogs with a
"Frame with slots" column, a Section column or bare "### I" headings are read;
word-source counts no longer go negative when kept sentences carry swaps.
Previous: 1.1.0 (2026-11-25) — word layer: W### bricks from style-vocab.md and
wordlist.tsv, swaps.json applied to content bricks, claim-strength classes, protected
terms, strength profile in verify.
Previous: 1.0.0 (2026-11-25) — frames, bundles, content bricks, assembly, verify.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

__version__ = "1.5.1"

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

SECTION_ORDER = ["A", "I", "M", "R", "D", "C"]
MAX_GAPS = 3

# Frozen. Changing either list changes what "never retype" permits; bump the version.
GLUE = frozenset("""
the a an and or but of in on at for to with by from as than that which whose
its their this these those it they we our is are was were be been
, ; : ( )
""".split())

AGREEMENT = {
    ("is", "are"), ("was", "were"), ("has", "have"), ("does", "do"),
    ("this", "these"), ("that", "those"), ("its", "their"), ("it", "they"),
}
AGREEMENT |= {(b, a) for a, b in AGREEMENT}

FUNCTION_CAPS = frozenset("""the a an this these that those its their in on at of
for to with by from as our we it they there such each both all""".split())

WORD_RE = re.compile(r"[A-Za-z0-9\u00C0-\u024F\u0370-\u03FF]+(?:['\-][A-Za-z0-9\u00C0-\u024F]+)*")
SLOT_RE = re.compile(r"\[[^\[\]]+\]")
ADDR_RE = re.compile(r"P(\d+)\s*[-–]\s*S(\d+)")
CODE_RE = re.compile(r"\b([A-L]\d{1,2}|Z)\b")
ABBREV = ("et al.", "e.g.", "i.e.", "Fig.", "Figs.", "Eq.", "Eqs.", "approx.", "ca.",
          "cf.", "vs.", "No.", "Ref.", "Refs.", "Tab.", "Sect.", "St.", "Dr.")


class Blocked(Exception):
    """Input cannot be read reliably (exit 2)."""


# ---------------------------------------------------------------- helpers

def norm_ws(s: str) -> str:
    return " ".join(s.split())


def words(s: str) -> list[str]:
    return [w.lower() for w in WORD_RE.findall(s)]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def read_tsv(path: Path) -> list[dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines:
        return []
    head = lines[0].split("\t")
    return [dict(zip(head, ln.split("\t"))) for ln in lines[1:] if ln.strip()]


def write_tsv(path: Path, head: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write("\t".join(head) + "\n")
        for r in rows:
            fh.write("\t".join(str(r.get(h, "")).replace("\t", " ") for h in head) + "\n")


def split_sentences(par: str) -> list[str]:
    protected = par
    for i, ab in enumerate(ABBREV):
        protected = protected.replace(ab, ab.replace(".", f"\x00{i}\x00"))
    protected = re.sub(r"(\d)\.(\d)", "\\1\x01\\2", protected)
    # page references inside citations: "(Smith, 2004, p. 12)", "(pp. 403, 421)"
    protected = re.sub(r"\b(pp?)\.(?=\s*\d)", "\\1\x01", protected)
    parts = re.split(r"(?<=[.!?])\s+(?=[\"“(\[]?[A-Z0-9δΔ])", protected)
    out = []
    for p in parts:
        p = re.sub(r"\x00(\d+)\x00", ".", p).replace("\x01", ".")
        if p.strip():
            out.append(p.strip())
    return out


def section_of_heading(line: str) -> str | None:
    # a bare section letter: "### I", "### I (P1–P10)", "### M — Methods"
    # (not "## C. Inter-paragraph logic", the lettered parts of logic.md)
    m = re.match(r"^\s*#+\s*([AIMRDC])(?=\s*$|\s*[—–(·:-]|\s+[—–(·:-])", line)
    if m:
        return m.group(1)
    h = line.lower()
    if "result" in h:
        return "R"
    if "discussion" in h:
        return "D"
    if "introduction" in h or "background" in h:
        return "I"
    if "method" in h or "material" in h or "study area" in h:
        return "M"
    if "conclusion" in h:
        return "C"
    if "abstract" in h:
        return "A"
    return None


# ---------------------------------------------------------------- pile

def parse_logic(path: Path) -> list[dict]:
    """Every §E-style catalog row: a markdown table with a Template column."""
    rows: list[dict] = []
    section = None
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.lstrip().startswith("#"):
            sec = section_of_heading(ln)
            if sec:
                section = sec
        low = ln.lower()
        if ln.lstrip().startswith("|") and ("template" in low or "with slots" in low) \
                and i + 1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            head = [c.strip().lower() for c in ln.strip().strip("|").split("|")]

            def col(*keys, avoid=()):
                for k, h in enumerate(head):
                    if any(x in h for x in keys) and not any(a in h for a in avoid):
                        return k
                return None

            # "Frame with slots" is the template column in some catalogs
            c_tpl = col("template", "with slots")
            c_type = col("frame", "type", "code", avoid=("template", "with slots"))
            c_orig = col("original", "sentence", "verbatim", avoid=("template",))
            c_src = col("source", "address", "loc")
            c_stat = col("recur", "status", "singleton", "class")
            c_sec = next((k for k, h in enumerate(head) if h == "section"), None)
            i += 2
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                get = lambda k: cells[k] if k is not None and k < len(cells) else ""
                tpl = get(c_tpl)
                if tpl:
                    typ = get(c_type)
                    m = CODE_RE.search(typ)
                    cell_sec = get(c_sec).strip()
                    rows.append({
                        "section": cell_sec if cell_sec in SECTION_ORDER else (section or ""),
                        "code": m.group(1) if m else "",
                        "name": CODE_RE.sub("", typ).strip(" :—-*`") if typ else "",
                        "template": tpl, "original": get(c_orig),
                        "source": get(c_src), "status": get(c_stat),
                    })
                i += 1
            continue
        i += 1
    return rows


def clean_template(t: str) -> str:
    t = t.strip().strip("`").strip()
    t = re.sub(r'^[\"“”]+|[\"“”]+$', "", t).strip()
    t = t.replace("…", "[REST]").replace("...", "[REST]")
    return norm_ws(t)


def clean_sentence(t: str) -> str:
    t = t.strip().strip("`").strip()
    return norm_ws(re.sub(r'^[\"“”]+|[\"“”]+$', "", t).strip())


def section_by_search(paper: Path, sentence: str) -> str:
    probe = norm_ws(sentence)[:60].lower()
    if len(probe) < 20:
        return ""
    for sid in SECTION_ORDER:
        f = paper / "sections" / f"{sid}.txt"
        if f.exists() and probe in norm_ws(f.read_text(encoding="utf-8", errors="replace")).lower():
            return sid
    return ""


def build_form(corpus: Path, section: str, papers: list[str] | None, unit: str,
               cross: bool) -> tuple[list[dict], dict]:
    pdir = corpus / "papers"
    if not pdir.is_dir():
        raise Blocked(f"no papers/ under {corpus}")
    slugs = sorted(p.name for p in pdir.iterdir() if p.is_dir())
    if papers:
        missing = [s for s in papers if s not in slugs]
        if missing:
            raise Blocked(f"papers not in corpus: {', '.join(missing)}")
        slugs = [s for s in slugs if s in papers]
    frames, bundles, sents, sources, notes = [], [], [], {}, []
    for slug in slugs:
        paper = pdir / slug
        logic = paper / "logic.md"
        if logic.exists():
            sources[f"{slug}/logic.md"] = sha(logic)
            rows = parse_logic(logic)
            maxs: dict[int, int] = {}
            for r in rows:
                m = ADDR_RE.search(r["source"])
                if m:
                    p, s = int(m.group(1)), int(m.group(2))
                    maxs[p] = max(maxs.get(p, 0), s)
            for r in rows:
                sec = r["section"] or section_by_search(paper, r["original"])
                m = ADDR_RE.search(r["source"])
                if m:
                    p, s = int(m.group(1)), int(m.group(2))
                    pos = ("solo" if maxs[p] == 1 else "initial" if s == 1
                           else "final" if s == maxs[p] else "medial")
                    addr = f"P{p}-S{s}"
                else:
                    pos, addr = "unknown", ""
                stat = r["status"].lower()
                status = ("recurrent" if "recur" in stat else
                          "singleton" if "single" in stat else "unmeasured")
                base = {"paper": slug, "section": sec, "code": r["code"],
                        "name": r["name"], "pos": pos, "status": status, "source": addr}
                tpl = clean_template(r["template"])
                slots = SLOT_RE.findall(tpl)
                if slots:
                    frames.append({**base, "kind": "frame", "slots": len(slots), "text": tpl})
                if unit == "sentence" and r["original"]:
                    sents.append({**base, "kind": "sentence", "slots": 0,
                                  "text": clean_sentence(r["original"])})
        else:
            notes.append(f"{slug}: no logic.md — no frames from this paper")
        ph = paper / "phrases.tsv"
        if ph.exists():
            sources[f"{slug}/phrases.tsv"] = sha(ph)
            for r in read_tsv(ph):
                if r.get("bundle") != "yes" or r.get("topic") != "no":
                    continue
                secs = "".join(s for s in SECTION_ORDER if r.get(s, "0") not in ("", "0"))
                bundles.append({"paper": slug, "section": secs, "code": r.get("function", ""),
                                "name": r.get("subfunction", ""), "pos": "", "status": "recurrent",
                                "source": f"total={r.get('total', '')}", "kind": "bundle",
                                "slots": 0, "text": r["phrase"]})
        else:
            notes.append(f"{slug}: no phrases.tsv — no bundles from this paper")

    def in_section(b):
        return cross or section in b["section"]

    frames = [f for f in frames if in_section(f)]
    sents = [s for s in sents if in_section(s)]
    bundles = [b for b in bundles if in_section(b)]
    seen, uniq = set(), []
    for b in bundles:            # one bundle brick per phrase; keep first paper, list others
        if b["text"] in seen:
            for u in uniq:
                if u["text"] == b["text"]:
                    u["paper"] += "," + b["paper"]
            continue
        seen.add(b["text"])
        uniq.append(b)
    out = []
    for prefix, group in (("F", frames), ("B", uniq), ("S", sents)):
        for k, b in enumerate(group, 1):
            out.append({"id": f"{prefix}{k:03d}", **b})
    meta = {"brickyard": __version__, "section": section, "unit": unit,
            "cross_section": cross, "papers": slugs, "sources": sources, "notes": notes,
            "counts": {"frames": len(frames), "bundles": len(uniq), "sentences": len(sents)}}
    return out, meta


FORM_HEAD = ["id", "kind", "paper", "section", "code", "name", "pos", "status",
             "source", "slots", "text"]


def cmd_pile(a) -> int:
    corpus, out, draft = Path(a.corpus), Path(a.out), Path(a.draft)
    papers = [s.strip() for s in a.papers.split(",")] if a.papers else None
    form, meta = build_form(corpus, a.section, papers, a.unit, a.cross_section)
    text = draft.read_text(encoding="utf-8")
    if not text.strip():
        raise Blocked("draft prose is empty")
    out.mkdir(parents=True, exist_ok=True)
    write_tsv(out / "form.tsv", FORM_HEAD, form)
    term_files = [Path(a.terms)] if a.terms else []
    term_files += [corpus / "papers" / s / "glossary.md" for s in meta["papers"]
                   if (corpus / "papers" / s / "glossary.md").exists()]
    terms = load_terms(term_files)
    (out / "terms.txt").write_text("".join(t + "\n" for t in sorted(terms)), encoding="utf-8")
    wrows, pos_map, attested = build_words(corpus, a.section, meta["papers"], a.cross_section, terms)
    write_tsv(out / "word.tsv", WORD_HEAD, wrows)
    write_tsv(out / "lexicon.tsv", ["form", "pos"],
              [{"form": f, "pos": pos_map.get(f, "")} for f in sorted(attested | set(pos_map))])
    meta["counts"]["words"] = len(wrows)
    meta["counts"]["terms"] = len(terms)
    meta["terms_file"] = str(Path(a.terms).resolve()) if a.terms else ""
    meta["strength_version"] = STRENGTH_VERSION
    drows, k = [], 0
    for pi, par in enumerate(re.split(r"\n\s*\n", text.strip()), 1):
        for s in split_sentences(norm_ws(par)):
            k += 1
            drows.append({"id": f"D{k}", "paragraph": pi, "words": len(words(s)), "text": s})
    write_tsv(out / "draft.tsv", ["id", "paragraph", "words", "text"], drows)
    meta.update({"corpus": str(corpus.resolve()), "draft": str(draft.resolve()),
                 "draft_sha": sha(draft), "draft_sentences": len(drows)})
    (out / "pile.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n",
                                   encoding="utf-8")
    c = meta["counts"]
    print(f"# brickyard {__version__} pile — section {a.section}, unit {a.unit}")
    print(f"papers      {len(meta['papers'])}: {', '.join(meta['papers'])}")
    print(f"frames      {c['frames']}  (F###)")
    print(f"bundles     {c['bundles']}  (B###)")
    print(f"words       {c['words']}  (W###; protected terms {c['terms']})")
    if a.unit == "sentence":
        print(f"sentences   {c['sentences']}  (S###; verify needs --own-corpus)")
    print(f"draft       {len(drows)} sentences (D#)")
    for n in meta["notes"]:
        print(f"note        {n}")
    if c["frames"] == 0:
        print("BLOCKED: no frames for this section — check the section letter or use "
              "--cross-section", file=sys.stderr)
        return 2
    return 0


# ---------------------------------------------------------------- word layer

# Frozen claim-strength classes (after Hyland 2005, metadiscourse; reporting-verb
# tiers after Hyland 2002). A swap must keep the class of what it replaces:
# hedge -> hedge, tentative reporting verb -> tentative reporting verb, none -> none.
# Negation is never swapped in or out. Changing these lists changes what the word
# layer permits: bump STRENGTH_VERSION.
STRENGTH_VERSION = "1.0.0"
STRENGTH = [
    ("negation", r"not|no|never|none|neither|nor|without|cannot"),
    ("report:strong", r"demonstrat\w*|prove[sdn]?|proving|establish(?:es|ed|ing)?|confirm(?:s|ed|ing)?"),
    ("report:moderate", r"show(?:s|n|ed|ing)?|reveal(?:s|ed|ing)?|find(?:s|ing)?|found|observ(?:e|es|ed|ing)"),
    ("report:tentative", r"suggest(?:s|ed|ing)?|indicat(?:e|es|ed|ing)|impl(?:y|ies|ied|ying)|propos(?:e|es|ed|ing)|hint(?:s|ed)?"),
    ("report:attribution", r"report(?:s|ed|ing)?|not(?:e|es|ed)|describ(?:e|es|ed|ing)|stat(?:e|es|ed)|document(?:s|ed)?|mention(?:s|ed)?"),
    ("hedge", r"may|might|could|possibl[ey]|probabl[ey]|(?:un)?likely|perhaps|appear(?:s|ed)?|seem(?:s|ed)?"
              r"|tend(?:s|ed)?|approximately|relatively|potentially|presumably|apparently|somewhat"
              r"|partially|generally|usually|often|largely|mainly|mostly"),
    ("booster", r"clearly|certainly|definitely|undoubtedly|obviously|evidently|indeed|markedly"
                r"|substantially|strongly|always|must|significantly|highly"),
]
_STRENGTH_RE = [(c, re.compile(rf"(?:{p})")) for c, p in STRENGTH]


def strength_of(phrase: str) -> str:
    found = []
    for w in phrase.lower().split():
        for c, rx in _STRENGTH_RE:
            if rx.fullmatch(w):
                found.append(c)
                break
    return "+".join(sorted(set(found))) or "-"


VOCAB_CATEGORIES = [("reporting", "reporting"), ("hedg", "hedge"), ("booster", "booster"),
                    ("stance", "booster"), ("attitude", "attitude"), ("connective", "connective"),
                    ("transition", "connective"), ("self-mention", "self-mention"),
                    ("self mention", "self-mention"), ("noun", "academic-noun"),
                    ("register", "register"), ("caption", "caption"), ("display", "caption")]


def parse_style_vocab(path: Path) -> list[tuple[str, str]]:
    """(item, category) from every table in style-vocab.md; first cell is the item."""
    out, cat = [], "style"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    for i, ln in enumerate(lines):
        s = ln.strip()
        if s.startswith("#"):
            low = s.lower()
            if "bundle" in low:
                cat = "skip"
                continue
            for key, c in VOCAB_CATEGORIES:
                if key in low:
                    cat = c
                    break
            continue
        if not s.startswith("|") or re.match(r"^\|[\s:|-]+\|$", s) or cat == "skip":
            continue
        if i + 1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            continue                                   # header row
        cell = s.strip("|").split("|")[0].strip().strip("`")
        if cell.startswith("**") and cell.endswith("**") and len(cell) > 4:
            cell = cell[2:-2]
        elif cell.startswith("*") and cell.endswith("*") and len(cell) > 2 and not cell.endswith("**"):
            cell = cell[1:-1]
        cell = cell.strip().strip("\"“”'").lower()
        if (not cell or re.search(r"\d", cell) or len(cell.split()) > 4
                or not re.fullmatch(r"[a-z][a-z' \-]*\*?", cell)):
            continue
        out.append((cell, cat))
    return out


def load_terms(paths: list[Path]) -> set[str]:
    """Technical terms: one per line, or glossary.md rows `| # | Term | ...`."""
    terms = set()
    for p in paths:
        is_md = p.suffix.lower() == ".md"
        for ln in p.read_text(encoding="utf-8-sig").splitlines():
            if ln.strip().startswith("|"):
                cells = [c.strip() for c in ln.strip().strip("|").split("|")]
                if len(cells) >= 3 and cells[0].isdigit():
                    t = cells[1].strip("`*\"“” ")
                    if t:
                        terms.add(norm_ws(t))
            elif is_md:
                continue        # glossary.md: only the numbered table rows are terms
            else:
                t = ln.split("#", 1)[0].strip()
                if t:
                    terms.add(norm_ws(t))
    return terms


def term_spans(text: str, terms: set[str]) -> list[tuple[int, int]]:
    spans = []
    for t in terms:
        body = r"\s+".join(re.escape(w) for w in t.split())
        for m in re.finditer(rf"(?<![\w-]){body}(?:e?s)?(?![\w-])", text, flags=re.I):
            spans.append(m.span())
    return spans


_PENN = (("JJ", "ADJ"), ("VB", "VERB"), ("RB", "ADV"), ("WRB", "ADV"), ("NN", "NOUN"),
         ("MD", "AUX"), ("IN", "ADP"), ("PRP", "PRON"), ("DT", "DET"), ("CC", "CCONJ"))


def upos(tag: str) -> str:
    """Universal tag for a universal or Penn Treebank tag ('VBZ' -> 'VERB')."""
    t = (tag or "").split("/")[0].strip().upper()
    if not t or t in ("VERB", "ADV", "ADJ", "NOUN", "AUX", "ADP", "PRON", "DET", "CCONJ", "PROPN"):
        return t
    for p, u in _PENN:
        if t.startswith(p):
            return u
    return t


def pos_compatible(a: str, b: str) -> bool:
    """Same universal class; for two Penn verb tags also the same form
    (VBP counts as VB, VBD as VBN: the forms coincide for regular verbs)."""
    ua, ub = upos(a), upos(b)
    if ua != ub:
        return False
    fa, fb = a.split("/")[0].upper(), b.split("/")[0].upper()
    if ua == "VERB" and fa.startswith("VB") and fb.startswith("VB"):
        n = {"VBP": "VB", "VBD": "VBN"}
        return n.get(fa, fa) == n.get(fb, fb)
    return True


def build_words(corpus: Path, section: str, slugs: list[str], cross: bool,
                terms: set[str]) -> tuple[list[dict], dict[str, str], set[str]]:
    """-> (word bricks, pos map form->POS, attested forms)."""
    term_words = {w.lower() for t in terms for w in t.split()}
    term_words |= {w + "s" for w in term_words} | {w + "es" for w in term_words}
    pos_map: dict[str, str] = {}
    attested: set[str] = set()
    cand: dict[str, dict] = {}
    for slug in slugs:
        paper = corpus / "papers" / slug
        texts = {sid: (paper / "sections" / f"{sid}.txt").read_text(encoding="utf-8", errors="replace")
                 for sid in SECTION_ORDER if (paper / "sections" / f"{sid}.txt").exists()}
        alltext = " ".join(texts.values())
        toks = words(alltext)
        attested |= set(toks)
        target = texts.get(section, "") if not cross else alltext
        target_low = " ".join(words(target))

        def count(form: str) -> int:
            return len(re.findall(rf"(?<![\w-]){re.escape(form)}(?![\w-])", target_low))

        def add(form, cat, pos, source):
            if (re.search(r"\d", form) or len(form) < 2 or form in term_words
                    or any(w in term_words for w in form.split())):
                return
            n = count(form)
            if n == 0:
                return
            c = cand.setdefault(form, {"form": form, "category": cat, "pos": pos,
                                       "papers": [], "count": 0, "source": source})
            if slug not in c["papers"]:
                c["papers"].append(slug)
                c["count"] += n
            if c["category"].startswith("pos:") and not cat.startswith("pos:"):
                c["category"], c["source"] = cat, source
            c["pos"] = c["pos"] or pos

        wl = paper / "wordlist.tsv"
        if wl.exists():
            for r in read_tsv(wl):
                form = r.get("type", "").lower()
                pos = (r.get("pos") or "").split("/")[0]
                if pos:
                    pos_map.setdefault(form, pos)
                if upos(pos) in ("VERB", "ADV", "ADJ") and int(r.get("total", "0") or 0) >= 2:
                    add(form, f"pos:{upos(pos)}", pos, "wordlist.tsv")
        sv = paper / "style-vocab.md"
        if sv.exists():
            for item, cat in parse_style_vocab(sv):
                if item.endswith("*"):
                    stem = item[:-1]
                    for form in sorted({t for t in toks if t.startswith(stem)}):
                        add(form, cat, pos_map.get(form, ""), "style-vocab.md")
                else:
                    add(item, cat, pos_map.get(item, ""), "style-vocab.md")
    rows = sorted(cand.values(), key=lambda c: (c["category"], c["form"]))
    out = []
    for k, c in enumerate(rows, 1):
        out.append({"id": f"W{k:03d}", "form": c["form"], "category": c["category"],
                    "strength": strength_of(c["form"]), "pos": c["pos"],
                    "papers": ",".join(c["papers"]), "count": c["count"], "source": c["source"]})
    return out, pos_map, attested


WORD_HEAD = ["id", "form", "category", "strength", "pos", "papers", "count", "source"]


def neighbours(text: str, a: int, b: int) -> tuple[str, str]:
    """The word right before text[a:b] and right after it; '' at a punctuation or brick edge."""
    lm = re.search(r"([A-Za-z][\w'-]*)\s+$", text[:a])
    rm = re.match(r"\s+([A-Za-z][\w'-]*)", text[b:])
    return (lm.group(1) if lm else ""), (rm.group(1) if rm else "")


def apply_swaps(text: str, bid: str, pile, asm, where: str) -> str:
    done: list[tuple[dict, list[int]]] = []     # this call's swaps with their live span
    for key, wid in (pile.swaps.get(bid) or {}).items():
        m = re.fullmatch(r"(.+?)#(\d+)", key)
        target, k = (m.group(1), int(m.group(2))) if m else (key, 1)
        tag = f"{where} {bid} '{key}' -> {wid}"
        if re.fullmatch(r"B\d{3}", wid):            # a lexical bundle as the replacement
            b = pile.form.get(wid)
            w = ({"form": b["text"], "category": "bundle", "strength": strength_of(b["text"]),
                  "pos": ""} if b and b["kind"] == "bundle" else None)
        else:
            w = pile.words.get(wid)
        if not w:
            asm.errors.append(f"{tag}: {wid} is not in the word or bundle pile")
            continue
        body = r"\s+".join(re.escape(x) for x in target.split())
        hits = list(re.finditer(rf"(?<![\w-]){body}(?![\w-])", text, flags=re.I))
        if len(hits) < k:
            asm.errors.append(f"{tag}: '{target}' occurs {len(hits)} times in {bid}")
            continue
        a, b = hits[k - 1].span()
        old = text[a:b]
        if re.search(r"\d", old):
            asm.errors.append(f"{tag}: a token with a digit is never swapped")
            continue
        if any(a < e and s < b for s, e in term_spans(text, pile.terms)):
            asm.errors.append(f"{tag}: '{old}' is part of a protected technical term")
            continue
        if old.lower() == w["form"]:
            asm.errors.append(f"{tag}: replacement is the same word")
            continue
        s_old, s_new = strength_of(old), w["strength"]
        if "negation" in s_old or "negation" in s_new:
            asm.errors.append(f"{tag}: negation is never swapped in or out")
            continue
        if s_old != s_new:
            asm.errors.append(f"{tag}: claim strength {s_old} -> {s_new}; a swap must keep the class")
            continue
        p_old, p_new = pile.pos_map.get(old.lower(), ""), w["pos"]
        if p_old and p_new and not pos_compatible(p_old, p_new):
            asm.errors.append(f"{tag}: part of speech {p_old} -> {p_new}")
            continue
        new = match_case(old, w["form"])
        text = text[:a] + new + text[b:]
        shift = len(new) - (b - a)
        for _, span in done:                    # keep earlier swaps' spans on the live text
            if span[0] >= b:
                span[0] += shift; span[1] += shift
        rec = {"where": where, "brick": bid, "from": old, "to": new, "id": wid,
               "category": w["category"], "strength": s_new,
               "pos": "checked" if p_old and p_new else "unverified"}
        asm.swaps.append(rec)
        done.append((rec, [a, a + len(new)]))
        asm.trace.append({"where": where, "kind": "word", "id": wid, "text": new})
    for rec, (a, b) in done:                     # neighbours in the brick as finally swapped
        rec["left"], rec["right"] = neighbours(text, a, b)
    return text


# ---------------------------------------------------------------- loading

class Pile:
    def __init__(self, d: Path):
        if not (d / "pile.json").exists():
            raise Blocked(f"{d} is not a pile (no pile.json) — run `pile` first")
        self.dir = d
        self.meta = json.loads((d / "pile.json").read_text(encoding="utf-8"))
        self.form = {r["id"]: r for r in read_tsv(d / "form.tsv")}
        self.draft = {r["id"]: r for r in read_tsv(d / "draft.tsv")}
        self.draft_text = Path(self.meta["draft"]).read_text(encoding="utf-8")
        self.words = {r["id"]: r for r in read_tsv(d / "word.tsv")} if (d / "word.tsv").exists() else {}
        self.pos_map, self.attested = {}, set()
        if (d / "lexicon.tsv").exists():
            for r in read_tsv(d / "lexicon.tsv"):
                self.attested.add(r["form"])
                if r.get("pos"):
                    self.pos_map[r["form"]] = r["pos"]
        self.terms = set()
        if (d / "terms.txt").exists():
            self.terms = {t.strip() for t in (d / "terms.txt").read_text(encoding="utf-8").splitlines() if t.strip()}
        self.swaps: dict[str, dict[str, str]] = {}
        self.swap_errors: list[str] = []
        # stage 1 (1.3.0): sentences rewritten on a declared frame, checked by `stage1`
        self.stage1_spec: dict | None = None
        self.stage1: dict[str, dict] = {}
        if (d / "stage1.json").exists():
            self.stage1_spec = json.loads((d / "stage1.json").read_text(encoding="utf-8"))
            for k, rec in enumerate(stage1_records(self.stage1_spec), 1):
                self.stage1[f"T{k}"] = rec
        self.msent = {r["id"]: r for r in read_tsv(d / "msent.tsv")} if (d / "msent.tsv").exists() else {}
        self.content: dict[str, str] = {}
        cf = d / "content.tsv"
        if cf.exists():
            for n, ln in enumerate(cf.read_text(encoding="utf-8").splitlines(), 1):
                if not ln.strip() or ln.startswith("#") or ln.lower().startswith("id\t"):
                    continue
                parts = ln.split("\t", 1)
                if len(parts) != 2 or not re.fullmatch(r"C\d+", parts[0].strip()):
                    raise Blocked(f"content.tsv line {n}: want `C#<TAB>verbatim span`")
                cid = parts[0].strip()
                if cid in self.content:
                    raise Blocked(f"content.tsv line {n}: duplicate id {cid}")
                self.content[cid] = parts[1].strip()

    def load_swaps(self, paths: list[Path]) -> list[str]:
        """Merge swap files {brick: {word: W###}}; a word swapped twice is a conflict."""
        errs = []
        for p in paths:
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                raise Blocked(f"{p}: not valid JSON ({e})")
            for bid, m in data.items():
                if bid.startswith("_"):
                    continue
                if not re.fullmatch(r"[CDT]\d+", bid) or not isinstance(m, dict):
                    errs.append(f"{p.name}: '{bid}' — swaps are keyed by C#, D# or T#, "
                                "each a {{word: W### or B###}} map")
                    continue
                for k, v in m.items():
                    prev = self.swaps.setdefault(bid, {}).get(k)
                    if prev and prev != v:
                        errs.append(f"{p.name}: {bid} '{k}' swapped to both {prev} and {v}")
                    self.swaps[bid][k] = v
        return errs

    def content_errors(self) -> list[str]:
        hay = norm_ws(self.draft_text)
        return [f"{cid}: not a verbatim span of the draft: {t!r}"
                for cid, t in self.content.items() if norm_ws(t) not in hay]


def open_pile(a) -> Pile:
    pile = Pile(Path(a.pile))
    paths = [Path(x) for x in a.swaps] if getattr(a, "swaps", None) else \
        sorted(pile.dir.glob("swaps*.json"))
    pile.swap_errors = pile.load_swaps(paths)
    pile.swap_files = [str(p) for p in paths]
    return pile


def cmd_content(a) -> int:
    pile = Pile(Path(a.pile))
    errs = pile.content_errors()
    for e in errs:
        print("FAIL", e)
    print(f"{len(pile.content)} content bricks, {len(errs)} not verbatim")
    return 1 if errs else 0


# ---------------------------------------------------------------- assembly

def expand_choice(core: str) -> list[str] | None:
    if core.lower() == "and/or":
        return None
    if not (re.search(r"[A-Za-z]/[A-Za-z]", core) or "(s)" in core or "(es)" in core):
        return None
    alts = []
    for part in core.split("/"):
        m = re.search(r"\((e?s)\)", part)
        if m:
            alts += [part.replace(m.group(0), m.group(1)), part.replace(m.group(0), "")]
        else:
            alts.append(part)
    return alts


def inflect_ok(src: str, dst: str) -> bool:
    s, d = src.lower(), dst.lower()
    if (s, d) in AGREEMENT:
        return True
    for x, y in ((s, d), (d, s)):
        if y in (x + "s", x + "es") or (x.endswith("y") and y == x[:-1] + "ies"):
            return True
    return False


def match_case(model: str, word: str) -> str:
    return word[:1].upper() + word[1:] if model[:1].isupper() else word


class Assembly:
    def __init__(self):
        self.paragraphs: list[list[dict]] = []
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.trace: list[dict] = []
        self.swaps: list[dict] = []


DETERMINERS = ("a", "an", "the", "this", "these", "that", "those", "its", "their", "our")
IRREGULAR = {  # past / participle forms -> base, for the few verbs regular rules miss
    "brought": "bring", "made": "make", "taken": "take", "took": "take", "given": "give",
    "gave": "give", "shown": "show", "drawn": "draw", "drew": "draw", "held": "hold",
    "led": "lead", "found": "find", "thought": "think", "been": "be", "became": "become",
    "begun": "begin", "began": "begin", "left": "leave", "meant": "mean", "kept": "keep",
    "known": "know", "knew": "know", "understood": "understand", "sought": "seek",
    "built": "build", "set": "set", "put": "put", "done": "do", "did": "do", "had": "have",
    "said": "say", "told": "tell", "got": "get", "won": "win", "lost": "lose", "met": "meet",
    "ran": "run", "run": "run", "chosen": "choose", "chose": "choose", "written": "write",
    "wrote": "write", "risen": "rise", "rose": "rise", "fallen": "fall", "fell": "fall",
}
IRREGULAR_PAST = {}
for _p, _b in IRREGULAR.items():
    IRREGULAR_PAST.setdefault(_b, _p)
VERB_OPS = ("base", "s", "ing", "ed")


def _bases(w: str) -> list[str]:
    """Candidate base forms of w, most likely first (w itself last)."""
    w = w.lower()
    out = []
    if w in IRREGULAR:
        out.append(IRREGULAR[w])
    if w.endswith("ing") and len(w) > 4:
        s = w[:-3]
        out += [s + "e", s] + ([s[:-1]] if len(s) > 2 and s[-1] == s[-2] else [])
    if w.endswith("ied"):
        out.append(w[:-3] + "y")
    elif w.endswith("ed") and len(w) > 3:
        s = w[:-2]
        out += [w[:-1], s] + ([s[:-1]] if len(s) > 2 and s[-1] == s[-2] else [])
    if w.endswith("ies"):
        out.append(w[:-3] + "y")
    elif w.endswith("es"):
        out += [w[:-1], w[:-2]]
    elif w.endswith("s") and not w.endswith("ss"):
        out.append(w[:-1])
    return out + [w]


def _forms(base: str, op: str) -> list[str]:
    b = base
    if op == "base":
        return [b]
    if op == "s":
        return [b[:-1] + "ies"] if b.endswith("y") and b[-2:-1] not in "aeiou" else \
            [b + "es"] if re.search(r"(s|x|z|ch|sh|o)$", b) else [b + "s"]
    if op == "ing":
        out = [b + "ing"]
        if b.endswith("e") and not b.endswith(("ee", "ye", "oe")):
            out.insert(0, b[:-1] + "ing")
        if re.search(r"[^aeiou][aeiou][bdgmnprt]$", b):
            out.append(b + b[-1] + "ing")
        return out
    if op == "ed":
        out = []
        if b in IRREGULAR_PAST:
            out.append(IRREGULAR_PAST[b])
        out += [b + "d"] if b.endswith("e") else \
            [b[:-1] + "ied"] if b.endswith("y") and b[-2:-1] not in "aeiou" else [b + "ed"]
        if re.search(r"[^aeiou][aeiou][bdgmnprt]$", b):
            out.append(b + b[-1] + "ed")
        return out
    return []


def verb_form(word: str, op: str, attested: set[str]) -> str | None:
    """The `op` form of `word`, built by rule and accepted only if attested."""
    bases = _bases(word)
    if op == "base" and len(bases) > 1:
        bases = bases[:-1]          # an inflected-looking word is not its own base
    for base in bases:
        for f in _forms(base, op):
            if f in attested:
                return f
    return None


def transform(text: str, ops: list[str], pile: Pile, where: str, cid: str,
              asm: Assembly) -> str:
    for op in ops:
        tag = f"{where} {cid}|{op}"
        if op == "-det":
            m = re.match(r"^(\w+)\s+", text)
            if not m or m.group(1).lower() not in DETERMINERS:
                asm.errors.append(f"{tag}: {cid} does not open on a determiner")
                continue
            asm.trace.append({"where": where, "kind": "transform", "id": f"{cid}|-det",
                              "text": m.group(1)})
            text = text[m.end():]
        elif op in VERB_OPS:
            m = re.match(r"^([A-Za-z]+)", text)
            if not m:
                asm.errors.append(f"{tag}: {cid} does not open on a word")
                continue
            attested = pile.attested | set(words(pile.draft_text))
            new = verb_form(m.group(1), op, attested)
            if not new:
                asm.errors.append(f"{tag}: no attested '{op}' form of '{m.group(1)}'")
                continue
            new = match_case(m.group(1), new)
            asm.trace.append({"where": where, "kind": "transform", "id": f"{cid}|{op}",
                              "text": f"{m.group(1)}->{new}"})
            text = new + text[m.end():]
        else:
            asm.errors.append(f"{tag}: unknown transform (use -det, base, s, ing, ed)")
    return text


def fix_articles(text: str, asm: "Assembly", where: str) -> str:
    """Re-pick a/an after word swaps changed the next word (counted as auto)."""
    def an(m):
        art, nxt = m.group(1), m.group(2)
        want = "an" if re.match(r"[aeiouAEIOU]", nxt) and not re.match(
            r"(?i)(uni|use|usu|eu|one|once)", nxt) else "a"
        return match_case(art, want) + m.group(0)[len(art):]
    new = re.sub(r"\b([Aa]n?)\s+([A-Za-z])", an, text)
    if new != text:
        asm.trace.append({"where": where, "kind": "auto", "id": "a-an", "text": "a/an after swap"})
    return new


def render_item(item: str, pile: Pile, where: str, asm: Assembly, gaps: list) -> tuple[str, str, str]:
    """-> (text, kind, id)"""
    m = re.fullmatch(r"(C\d+)\|([\w,+-]+)", item)
    if m:
        cid, ops = m.group(1), [o for o in m.group(2).split(",") if o]
        if cid not in pile.content:
            asm.errors.append(f"{where}: content brick {cid} is not in content.tsv")
            return "", "content", cid
        text = apply_swaps(pile.content[cid], cid, pile, asm, where)
        return transform(text, ops, pile, where, cid, asm), "content", cid
    if item.startswith("g:"):
        w = item[2:]
        if w.lower() not in GLUE:
            asm.errors.append(f"{where}: glue '{w}' is not in the frozen GLUE list")
        return w, "glue", item
    if item.startswith("?:"):
        t = item[2:].strip()
        if "\n" in t or not t:
            asm.errors.append(f"{where}: a gap is one non-empty line")
        gaps.append(t)
        return f"[YOU WRITE: {t}]", "gap", "?"
    if re.fullmatch(r"C\d+", item):
        if item not in pile.content:
            asm.errors.append(f"{where}: content brick {item} is not in content.tsv")
            return "", "content", item
        return apply_swaps(pile.content[item], item, pile, asm, where), "content", item
    if re.fullmatch(r"B\d{3}", item):
        b = pile.form.get(item)
        if not b:
            asm.errors.append(f"{where}: bundle {item} is not in the pile")
            return "", "bundle", item
        return b["text"], "bundle", item
    asm.errors.append(f"{where}: '{item}' is not a slot filler (C#, B###, g:word, ?:gap)")
    return "", "?", item


def tidy(pieces: list[tuple[str, str, str]], asm: Assembly, where: str) -> str:
    """Join pieces, then the auto fixes. Every change is counted."""
    fixed: list[list] = []
    for text, kind, bid in pieces:
        if not text:
            continue
        if fixed and kind == "content":
            first = text.split(" ", 1)[0]
            if first[:1].isupper() and first[1:].islower() and first.lower() in FUNCTION_CAPS:
                text = first.lower() + text[len(first):]
                asm.trace.append({"where": where, "kind": "auto", "id": "decap", "text": first})
        fixed.append([text, kind, bid])
    s = " ".join(t for t, _, _ in fixed)
    before = s
    s = re.sub(r"\s+([,.;:)\]])", r"\1", s)
    s = re.sub(r"([(\[])\s+", r"\1", s)
    s = re.sub(r",\s*([.;:])", r"\1", s)          # omitted trailing slot: ", ." -> "."
    s = re.sub(r"([,;:])\1+", r"\1", s)
    s = re.sub(r"\.\.+$", ".", s)
    s = re.sub(r"\(\s*\)", "", s)
    s = norm_ws(s)

    def an(m):
        art, nxt = m.group(1), m.group(2)
        want = "an" if re.match(r"[aeiouAEIOU]", nxt) and not re.match(
            r"(?i)(uni|use|usu|eu|one|once)", nxt) else "a"
        return match_case(art, want) + m.group(0)[len(art):]
    s = re.sub(r"\b([Aa]n?)\s+([A-Za-z])", an, s)
    if s and s[0].islower():
        s = s[0].upper() + s[1:]
    if s and s[-1] not in ".?!:]":
        s += "."
    if s != before:
        asm.trace.append({"where": where, "kind": "auto", "id": "tidy", "text": "spacing/a-an/case/period"})
    return s


def build_frame_sentence(spec: dict, pile: Pile, asm: Assembly, where: str, gaps: list) -> str:
    fid = spec.get("frame", "")
    f = pile.form.get(fid)
    if not f or f["kind"] != "frame":
        asm.errors.append(f"{where}: frame {fid!r} is not in the pile")
        return ""
    if f["section"] != pile.meta["section"] and not pile.meta.get("cross_section"):
        asm.errors.append(f"{where}: {fid} is from section {f['section']}, not {pile.meta['section']}")
    tpl = f["text"]
    fill = spec.get("fill", {}) or {}
    pick = dict(spec.get("pick", {}) or {})
    inflect = dict(spec.get("inflect", {}) or {})
    names, counts = [], {}
    for raw in SLOT_RE.findall(tpl):
        n = raw[1:-1].strip()
        counts[n] = counts.get(n, 0) + 1
        names.append(n if counts[n] == 1 else f"{n}#{counts[n]}")
    for k in fill:
        if k not in names:
            asm.errors.append(f"{where}: {fid} has no slot [{k}] (slots: {', '.join(names)})")
    pieces: list[tuple[str, str, str]] = []
    fixed_parts = SLOT_RE.split(tpl)
    seen_tok: dict[str, int] = {}
    used_pick, used_infl = set(), set()
    for i, fixed_text in enumerate(fixed_parts):
        for tok in fixed_text.split():
            m = re.match(r"^([(\"“]*)(.*?)([.,;:)\"”]*)$", tok)
            lead, core, trail = m.group(1), m.group(2), m.group(3)
            while trail.startswith(")") and core.count("(") > core.count(")"):
                core, trail = core + ")", trail[1:]
            kind = "frame"
            low = core.lower()
            seen_tok[low] = seen_tok.get(low, 0) + 1
            key_n = f"{core}#{seen_tok[low]}"
            alts = expand_choice(core)
            if alts:
                key = core if core in pick else key_n if key_n in pick else None
                if key:
                    chosen = pick[key]
                    used_pick.add(key)
                    if chosen not in alts:
                        asm.errors.append(f"{where}: pick {core} -> {chosen!r} is not one of {alts}")
                else:
                    chosen = alts[0]
                    asm.warnings.append(f"{where}: {fid} choice '{core}' not picked; default '{chosen}'")
                core = chosen
                kind = "pick"
            key = core if core in inflect else key_n if key_n in inflect else None
            if key:
                dst = inflect[key]
                used_infl.add(key)
                if not inflect_ok(core, dst):
                    asm.errors.append(f"{where}: inflect {core} -> {dst} is not an agreement change")
                core = match_case(core, dst)
                kind = "inflect"
            if core or lead or trail:
                pieces.append((lead + core + trail, kind, fid))
        if i < len(names):
            slot = names[i]
            if slot not in fill:
                asm.errors.append(f"{where}: {fid} slot [{slot}] not filled (use [] to omit it)")
                continue
            items = fill[slot]
            if isinstance(items, str):
                items = [items]
            if not items:
                asm.trace.append({"where": where, "kind": "omit", "id": fid, "text": f"[{slot}]"})
            for it in items:
                pieces.append(render_item(str(it), pile, where, asm, gaps))
    for k in set(pick) - used_pick:
        asm.errors.append(f"{where}: pick key {k!r} matches no choice token in {fid}")
    for k in set(inflect) - used_infl:
        asm.errors.append(f"{where}: inflect key {k!r} matches no word in {fid}")
    for text, kind, bid in pieces:
        asm.trace.append({"where": where, "kind": kind, "id": bid, "text": text})
    return tidy(pieces, asm, where)


def assemble(plan: dict, pile: Pile) -> Assembly:
    asm = Assembly()
    gaps: list[str] = []
    paras = plan.get("paragraphs")
    if not isinstance(paras, list) or not paras:
        asm.errors.append("plan.json: want {\"paragraphs\": [ {\"sentences\": [...]}, ... ]}")
        return asm
    errs = pile.content_errors()
    asm.errors += [f"content.tsv {e}" for e in errs]
    asm.errors += pile.swap_errors
    for pi, para in enumerate(paras, 1):
        sents = para.get("sentences") if isinstance(para, dict) else para
        out = []
        for si, spec in enumerate(sents or [], 1):
            where = f"P{pi}.S{si}"
            rec = {"where": where, "spec": spec}
            if "frame" in spec:
                rec.update(kind="frame", text=build_frame_sentence(spec, pile, asm, where, gaps),
                           brick=pile.form.get(spec["frame"]))
            elif "stage1" in spec:
                tid = spec["stage1"]
                t = pile.stage1.get(tid)
                if not t:
                    asm.errors.append(f"{where}: stage-1 sentence {tid!r} is not in pile/stage1.json "
                                      "(run `stage1` first)")
                    continue
                base = norm_ws(str(t.get("text", ""))) if not t.get("keep") else \
                    " ".join(pile.draft[d]["text"] for d in (t.get("from") or []) if d in pile.draft)
                rec.update(kind="stage1", text=fix_articles(apply_swaps(base or "", tid, pile, asm, where), asm, where),
                           brick=stage1_brick(pile, t),
                           keep=bool(t.get("keep")))
                gaps += GAP_RE.findall(rec["text"])
                asm.trace.append({"where": where, "kind": "stage1", "id": tid, "text": rec["text"]})
            elif "keep" in spec:
                d = pile.draft.get(spec["keep"])
                if not d:
                    asm.errors.append(f"{where}: keep {spec['keep']!r} is not a draft sentence")
                rec.update(kind="keep", text=apply_swaps(d["text"], spec["keep"], pile, asm, where) if d else "")
                asm.trace.append({"where": where, "kind": "keep", "id": spec["keep"], "text": rec["text"]})
            elif "sentence" in spec:
                b = pile.form.get(spec["sentence"])
                if not b or b["kind"] != "sentence":
                    asm.errors.append(f"{where}: sentence brick {spec['sentence']!r} is not in the pile")
                rec.update(kind="sentence", text=b["text"] if b else "", brick=b)
                asm.trace.append({"where": where, "kind": "sentence", "id": spec["sentence"], "text": rec["text"]})
            elif "gap" in spec:
                t = str(spec["gap"]).strip()
                if "\n" in t or not t:
                    asm.errors.append(f"{where}: a gap is one non-empty line")
                gaps.append(t)
                rec.update(kind="gap", text=f"[YOU WRITE: {t}]")
                asm.trace.append({"where": where, "kind": "gap", "id": "?", "text": t})
            else:
                asm.errors.append(f"{where}: a sentence is one of frame / keep / gap / sentence")
                continue
            out.append(rec)
        asm.paragraphs.append(out)
    if len(gaps) > MAX_GAPS:
        asm.errors.append(f"{len(gaps)} gaps; at most {MAX_GAPS} per run")
    asm.gaps = gaps
    return asm


def render(asm: Assembly) -> str:
    return "\n\n".join(" ".join(r["text"] for r in p if r["text"]) for p in asm.paragraphs) + "\n"


def load_plan(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise Blocked(f"{path}: not valid JSON ({e})")


def cmd_assemble(a) -> int:
    pile = open_pile(a)
    asm = assemble(load_plan(Path(a.plan)), pile)
    for w in asm.warnings:
        print("warn ", w)
    if asm.errors:
        for e in asm.errors:
            print("ERROR", e)
        print(f"{len(asm.errors)} errors — nothing written")
        return 1
    Path(a.out).write_text(render(asm), encoding="utf-8")
    if a.trace:
        write_tsv(Path(a.trace), ["where", "kind", "id", "text"], asm.trace)
    print(f"wrote {a.out}" + (f" and {a.trace}" if a.trace else ""))
    return 0


# ---------------------------------------------------------------- stage 1 (1.3.0)
#
# Guided mode. The frame writer rewrites each draft sentence on ONE declared corpus
# frame, in its own words, and the script measures what it did instead of trusting it:
#   fit    share of the frame's fixed words present, in order (inflection tolerated)
#   new    words that are neither frame words, draft words (same lemma) nor glue
#   lost   draft content words the rewrite no longer has; digits and citations FAIL
# Stage 2 (the word layer) then works on the stage-1 sentences (T#) by ID only.

GAP_RE = re.compile(r"\[YOU WRITE:[^\]]*\]")
_EQUIV = [frozenset("is are was were be been being am".split()),
          frozenset("has have had having".split()), frozenset("does do did done doing".split())]


def lemmas(w: str) -> set[str]:
    w = w.lower()
    for eq in _EQUIV:
        if w in eq:
            return set(eq)
    return {w} | (set(_bases(w)) if len(w) >= 4 else set())


def same_word(a: str, b: str) -> bool:
    return bool(lemmas(a) & lemmas(b)) or inflect_ok(a, b)


def frame_items(tpl: str) -> list[list[str]]:
    """Fixed words of a template, in order; a choice token is one item with alternatives."""
    items = []
    for part in SLOT_RE.split(tpl):
        for tok in part.split():
            core = re.sub(r"^[(\"“'‘]+|[.,;:)\"”'’?!]+$", "", tok)
            if not core:
                continue
            alts = expand_choice(core)
            if alts:
                items.append([x.lower() for x in alts])
            else:
                items += [[w] for w in words(core)]
    return items


def stage1_records(spec: dict) -> list[dict]:
    out = []
    paras = spec.get("paragraphs") or [{"sentences": spec.get("sentences", [])}]
    for pi, para in enumerate(paras, 1):
        sents = para.get("sentences") if isinstance(para, dict) else para
        for s in sents or []:
            out.append({**s, "paragraph": pi})
    return out


def check_stage1(pile: "Pile", min_fit: float, max_new: float) -> dict:
    spec = pile.stage1_spec or {}
    fails, warns, rows = [], [], []
    draft = pile.draft
    draft_all = words(pile.draft_text)
    covered: dict[str, list[str]] = {}
    tot = {"frame": 0, "draft": 0, "glue": 0, "new": 0, "gap": 0}
    gaps = 0
    used_frames: dict[str, int] = {}
    for tid, rec in pile.stage1.items():
        src = rec.get("from") or []
        if isinstance(src, str):
            src = [src]
        bad = [d for d in src if d not in draft]
        if not src or bad:
            fails.append(f"{tid}: 'from' must list draft sentences D# ({', '.join(bad) or 'none given'})")
            continue
        for d in src:
            covered.setdefault(d, []).append(tid)
        if rec.get("keep"):
            text = " ".join(draft[d]["text"] for d in src)
            rec["text"] = text
            if not str(rec.get("why", "")).strip():
                fails.append(f"{tid}: a keep needs 'why' (the frame slot that could not take the content)")
            rows.append({"id": tid, "from": ",".join(src), "frame": "keep", "kind": "keep",
                         "paper": "", "fixed": "", "fit": "",
                         "new": "", "lost": "", "text": text})
            n = len(words(text))
            tot["draft"] += n
            continue
        text = norm_ws(str(rec.get("text", "")))
        rec["text"] = text
        kind = "frame"
        if rec.get("base"):
            fid = rec["base"]
            f = base_frame(pile, rec)
            if not f:
                fails.append(f"{tid}: base {fid!r} is not in pile/msent.tsv — run `match` first")
                continue
            if f["section"] not in match_sections(pile):
                fails.append(f"{tid}: {fid} is from section {f['section']}, outside the matched sections")
            kind = "verbatim" if text == f["base_text"] else "base"
            if kind == "verbatim":
                warns.append(f"{tid}: VERBATIM corpus sentence {fid} ({f['paper']}, {f['source']}) — "
                             "another author's wording; not usable in a manuscript without quotation")
        else:
            fid = rec.get("frame", "")
            f = pile.form.get(fid)
            if not f or f["kind"] != "frame":
                fails.append(f"{tid}: frame {fid!r} is not in the pile")
                continue
            if f["section"] != pile.meta["section"] and not pile.meta.get("cross_section"):
                fails.append(f"{tid}: {fid} is from section {f['section']}, not {pile.meta['section']}")
        used_frames[fid] = used_frames.get(fid, 0) + 1
        if not text:
            fails.append(f"{tid}: empty text")
            continue
        gaps += len(GAP_RE.findall(text))
        gap_spans = [m.span() for m in GAP_RE.finditer(text)]
        toks = [(m.group(0), m.span()) for m in WORD_RE.finditer(text)]
        in_gap = [any(a <= s < b for a, b in gap_spans) for _, (s, _e) in toks]
        items = frame_items(f["text"])
        if not items:
            fails.append(f"{tid}: {fid} has no fixed words — it imposes nothing; choose another frame")
            continue
        if kind != "frame" and len(items) < 4:
            fails.append(f"{tid}: base {fid} keeps only {len(items)} fixed words for this draft "
                         "sentence — too little of it survives; choose another base or a frame")
            continue
        role = ["gap" if g else "" for g in in_gap]
        ptr, missing = 0, []
        for alts in items:
            hit = None
            for j in range(ptr, len(toks)):
                if role[j] == "" and any(same_word(toks[j][0], a) for a in alts):
                    hit = j
                    break
            if hit is None:
                missing.append("/".join(alts))
            else:
                role[hit] = "frame"
                ptr = hit + 1
        fit = (len(items) - len(missing)) / len(items)
        src_words = [w for d in src for w in words(draft[d]["text"])]
        new_words = []
        for j, (w, _sp) in enumerate(toks):
            if role[j]:
                continue
            lw = w.lower()
            if any(same_word(lw, x) for x in src_words) or any(same_word(lw, x) for x in draft_all):
                role[j] = "draft"
            elif lw in GLUE:
                role[j] = "glue"
            else:
                role[j] = "new"
                new_words.append(w)
        for r in role:
            tot[r] += 1
        if fit < min_fit:
            fails.append(f"{tid}: {fid} fit {fit:.0%} < {min_fit:.0%} — missing fixed words: "
                         f"{', '.join(missing)}")
        rows.append({"id": tid, "from": ",".join(src), "frame": fid, "kind": kind,
                     "paper": f["paper"], "fixed": len(items), "fit": f"{fit:.2f}",
                     "new": " ".join(new_words), "missing": " ".join(missing), "lost": "",
                     "text": text})
        for g in GAP_RE.findall(text):
            if any(t.lower() in g.lower() for t in pile.terms):
                warns.append(f"{tid}: a gap's instruction names a protected term ({g}); "
                             "Gate 1 must run on the gap-free copy")
    # coverage, digits and citations, lost content words — per draft sentence
    for d, row in draft.items():
        tids = covered.get(d)
        if not tids:
            fails.append(f"{d} is not rewritten, kept or merged anywhere — draft content lost")
            continue
        out_text = " ".join(pile.stage1[t].get("text", "") for t in tids)
        out_words = words(GAP_RE.sub(" ", out_text))
        for tok in re.findall(r"\S*\d\S*", row["text"]):
            core = tok.strip(".,;:()[]")
            if core and core not in out_text:
                fails.append(f"{d}: '{core}' (value or citation) is missing from {', '.join(tids)}")
        lost = sorted({w for w in words(row["text"]) if len(w) >= 3 and w not in GLUE
                       and not re.search(r"\d", w) and not any(same_word(w, x) for x in out_words)})
        if lost:
            warns.append(f"{d} -> {', '.join(tids)}: draft words not in the rewrite: {', '.join(lost)}")
            for r in rows:
                if r["id"] in tids:
                    r["lost"] = " ".join(lost)
    for d, tids in covered.items():
        if len(tids) > 1 and len({pile.stage1[t].get("paragraph") for t in tids}) > 1:
            warns.append(f"{d} is spread over paragraphs ({', '.join(tids)})")
    if gaps > MAX_GAPS:
        fails.append(f"{gaps} gaps; at most {MAX_GAPS} per run")
    counted = sum(v for k, v in tot.items() if k != "gap")
    share = tot["new"] / counted if counted else 0.0
    if share > max_new:
        fails.append(f"new words are {share:.0%} of the stage-1 text (limit {max_new:.0%}) — "
                     "the rewrite is adding its own wording")
    for fid, n in used_frames.items():
        if n > 1:
            warns.append(f"{fid} is used {n} times")
    return {"fails": fails, "warns": warns, "rows": rows, "tot": tot, "share": share,
            "gaps": gaps, "frames": used_frames}


STAGE1_HEAD = ["id", "from", "frame", "kind", "paper", "fixed", "fit", "missing", "new", "lost", "text"]


def cmd_stage1(a) -> int:
    pile_dir = Path(a.pile)
    spec = load_plan(Path(a.stage1))
    (pile_dir / "stage1.json").write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n",
                                          encoding="utf-8")
    pile = Pile(pile_dir)
    res = check_stage1(pile, a.min_fit, a.max_new)
    write_tsv(pile_dir / "stage1.tsv", STAGE1_HEAD, res["rows"])
    plan = {"paragraphs": []}
    for tid, rec in pile.stage1.items():
        while len(plan["paragraphs"]) < rec["paragraph"]:
            plan["paragraphs"].append({"sentences": []})
        plan["paragraphs"][rec["paragraph"] - 1]["sentences"].append({"stage1": tid})
    Path(a.plan_out).write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    t = res["tot"]
    on = sum(1 for r in res["rows"] if r["frame"] not in ("keep", ""))
    lines = [f"# brickyard {__version__} stage 1 — {'PASS' if not res['fails'] else 'FAIL'}", "",
             f"- sentences on a declared frame: {on} of {len(res['rows'])}; keeps "
             f"{sum(1 for r in res['rows'] if r['frame'] == 'keep')}; gaps {res['gaps']}",
             f"- words by source: frame {t['frame']}, draft {t['draft']}, glue {t['glue']}, "
             f"new {t['new']} ({res['share']:.0%}; limit {a.max_new:.0%})",
             f"- on a corpus-sentence base: {sum(1 for r in res['rows'] if r['kind'] == 'base')}; "
             f"verbatim corpus sentences: {sum(1 for r in res['rows'] if r['kind'] == 'verbatim')}", "",
             "| T# | from | frame | kind | fixed | fit | missing fixed words | new words | draft words lost |",
             "|---|---|---|---|---|---|---|---|---|"]
    for r in res["rows"]:
        lines.append(f"| {r['id']} | {r['from']} | {r['frame']} | {r['kind']} | {r['fixed']} | {r['fit']} | "
                     f"{r.get('missing', '')} | {r['new']} | {r['lost']} |")
    if res["fails"]:
        lines += ["", "## FAIL", *[f"- {x}" for x in res["fails"]]]
    if res["warns"]:
        lines += ["", "## Warnings", *[f"- {x}" for x in res["warns"]]]
    lines += ["", f"Stage-2 plan written to {a.plan_out}; word swaps key on T#."]
    rep = "\n".join(lines) + "\n"
    if a.report:
        Path(a.report).write_text(rep, encoding="utf-8")
    print(rep, end="")
    return 1 if res["fails"] else 0


# ---------------------------------------------------------------- corpus-sentence bases (1.5.0)
#
# `match` indexes every sentence of the target section(s) of the corpus papers (M###) and
# lists, per draft sentence, the corpus sentences whose content is closest. In stage1.json a
# sentence may then name {"base": "M###"} instead of a frame. The base becomes a frame on
# the fly: its content words that the source draft sentence does not have, its digits and
# its names become slots; every other word is fixed. A text identical to the corpus
# sentence is a VERBATIM reuse: another author's wording, flagged everywhere.

MATCH_STOP = GLUE | frozenset("""not no also more most such than very can may might could would
should will has have had do does did been being into upon about over between both each
other some any all only however thus""".split())


def canon(w: str) -> str:
    return sorted(lemmas(w), key=lambda x: (len(x), x))[0]


def is_content(w: str) -> bool:
    lw = w.lower()
    return len(lw) >= 3 and lw not in MATCH_STOP and not re.search(r"\d", lw)


def content_lemmas(text: str) -> set[str]:
    return {canon(w) for w in words(text) if is_content(w)}


def corpus_sentences(corpus: Path, papers: list[str], sections: list[str]) -> list[dict]:
    rows = []
    for slug in papers:
        for sec in [s for s in SECTION_ORDER if s in sections]:
            f = corpus / "papers" / slug / "sections" / f"{sec}.txt"
            if not f.exists():
                continue
            paras = [p for p in re.split(r"\n\s*\n", f.read_text(encoding="utf-8", errors="replace"))
                     if p.strip()]
            for pi, par in enumerate(paras, 1):
                sents = split_sentences(par)
                for si, s in enumerate(sents, 1):
                    s = norm_ws(s)
                    if not 6 <= len(words(s)) <= 80:
                        continue
                    pos = ("solo" if len(sents) == 1 else "initial" if si == 1
                           else "final" if si == len(sents) else "medial")
                    rows.append({"paper": slug, "section": sec, "pos": pos,
                                 "source": f"{sec} [P{pi}-S{si}]", "text": s})
    for k, r in enumerate(rows, 1):
        r["id"] = f"M{k:04d}"
    return rows


def match_sections(pile: "Pile") -> list[str]:
    mj = pile.dir / "match.json"
    if mj.exists():
        return json.loads(mj.read_text(encoding="utf-8"))["sections"]
    return [pile.meta["section"]]


def cmd_match(a) -> int:
    pile = Pile(Path(a.pile))
    corpus = Path(pile.meta["corpus"])
    if not corpus.is_dir():
        raise Blocked(f"corpus folder not reachable: {corpus}")
    secs = [s for s in SECTION_ORDER if s != "A"] if a.all_sections else [pile.meta["section"]]
    ms = corpus_sentences(corpus, pile.meta["papers"], secs)
    write_tsv(pile.dir / "msent.tsv", ["id", "paper", "section", "pos", "source", "text"], ms)
    (pile.dir / "match.json").write_text(json.dumps({"sections": secs, "top": a.top}) + "\n",
                                         encoding="utf-8")
    index = [(m, content_lemmas(m["text"])) for m in ms]
    out, lines = [], []
    for did, d in pile.draft.items():
        dw = content_lemmas(d["text"])
        if not dw:
            continue
        scored = []
        for m, cw in index:
            if not cw:
                continue
            scored.append((len(dw & cw) / len(dw), len(cw - dw) / len(cw), m))
        scored.sort(key=lambda x: (-x[0], x[1], x[2]["id"]))
        for rank, (match, extra, m) in enumerate(scored[:a.top], 1):
            same = "yes" if match >= a.same_match and extra <= a.same_extra else ""
            out.append({"draft": did, "rank": rank, "id": m["id"], "match": f"{match:.2f}",
                        "extra": f"{extra:.2f}", "same": same, "paper": m["paper"],
                        "section": m["section"], "pos": m["pos"], "text": m["text"]})
        if scored:
            b = scored[0]
            lines.append(f"- {did}: best {b[2]['id']} match {b[0]:.2f} extra {b[1]:.2f} "
                         f"({b[2]['paper']}/{b[2]['section']})"
                         + ("  SAME CONTENT" if b[0] >= a.same_match and b[1] <= a.same_extra else ""))
    write_tsv(pile.dir / "match.tsv", ["draft", "rank", "id", "match", "extra", "same", "paper",
                                       "section", "pos", "text"], out)
    n_same = len({r["draft"] for r in out if r["same"]})
    print(f"# brickyard {__version__} match\n\n- corpus sentences indexed: {len(ms)} "
          f"(sections {''.join(secs)}; papers {len(pile.meta['papers'])})\n"
          f"- draft sentences with a same-content candidate (match >= {a.same_match:.2f}, "
          f"extra <= {a.same_extra:.2f}): {n_same} of {len(pile.draft)}\n" + "\n".join(lines)
          + f"\n\nwrote {pile.dir / 'msent.tsv'} and {pile.dir / 'match.tsv'}")
    return 0


def base_frame(pile: "Pile", rec: dict) -> dict | None:
    """A corpus sentence turned into a frame for this record's source sentences."""
    m = pile.msent.get(rec.get("base", ""))
    if not m:
        return None
    src = rec.get("from") or []
    src = [src] if isinstance(src, str) else src
    keep = content_lemmas(" ".join(pile.draft[d]["text"] for d in src if d in pile.draft))
    parts, slot = [], False
    for tok in m["text"].split():
        ws = words(tok)
        open_slot = any(re.search(r"\d", w) or (is_content(w) and canon(w) not in keep) for w in ws)
        if open_slot:
            if not slot:
                parts.append("[X]")
            slot = True
        else:
            parts.append(tok)
            slot = False
    return {"id": m["id"], "kind": "frame", "paper": m["paper"], "section": m["section"],
            "pos": m["pos"], "status": "base", "source": m["source"], "text": " ".join(parts),
            "base_text": m["text"]}


def stage1_brick(pile: "Pile", rec: dict) -> dict | None:
    if rec.get("keep"):
        return None
    if rec.get("base"):
        return base_frame(pile, rec)
    return pile.form.get(rec.get("frame", ""))


# ---------------------------------------------------------------- verify

def ngrams(ws: list[str], n: int) -> set[tuple[str, ...]]:
    return {tuple(ws[i:i + n]) for i in range(len(ws) - n + 1)}


def cmd_verify(a) -> int:
    pile = open_pile(a)
    plan = load_plan(Path(a.plan))
    asm = assemble(plan, pile)
    fails, warns = list(asm.errors), list(asm.warnings)
    rev_path = Path(a.revision)
    rev = rev_path.read_text(encoding="utf-8") if rev_path.exists() else None
    if rev is None:
        fails.append(f"{rev_path} missing")
    elif not asm.errors and rev.rstrip() != render(asm).rstrip():
        fails.append("revision.txt is not the assembly of plan.json — the text was edited by hand. "
                     "Change the plan and re-assemble; never edit the text.")

    # pile integrity: rebuild from the corpus and compare
    corpus = Path(pile.meta["corpus"])
    if corpus.is_dir():
        form, meta = build_form(corpus, pile.meta["section"], pile.meta["papers"],
                                pile.meta["unit"], pile.meta.get("cross_section", False))
        fresh = {r["id"]: str(r["text"]) for r in form}
        changed = [k for k, v in pile.form.items() if fresh.get(k) != v["text"]]
        if changed:
            fails.append(f"form.tsv differs from the corpus for {len(changed)} bricks "
                         f"({', '.join(changed[:5])}) — rebuild the pile")
        tf = [Path(pile.meta["terms_file"])] if pile.meta.get("terms_file") else []
        tf += [corpus / "papers" / s / "glossary.md" for s in pile.meta["papers"]
               if (corpus / "papers" / s / "glossary.md").exists()]
        if tf and all(p.exists() for p in tf):
            wfresh, _, _ = build_words(corpus, pile.meta["section"], pile.meta["papers"],
                                       pile.meta.get("cross_section", False), load_terms(tf))
        else:
            wfresh, _, _ = build_words(corpus, pile.meta["section"], pile.meta["papers"],
                                       pile.meta.get("cross_section", False), set())
        wf = {r["id"]: (r["form"], r["strength"]) for r in wfresh}
        wchanged = [k for k, v in pile.words.items() if wf.get(k) != (v["form"], v["strength"])]
        if wchanged:
            fails.append(f"word.tsv differs from the corpus for {len(wchanged)} words "
                         f"({', '.join(wchanged[:5])}) — rebuild the pile")
    else:
        warns.append("corpus folder not reachable; pile integrity not re-checked")
    if sha(Path(pile.meta["draft"])) != pile.meta["draft_sha"]:
        fails.append("the draft changed after the pile was built — rebuild the pile")

    recs = [r for p in asm.paragraphs for r in p]
    frames_used = [r for r in recs if r["kind"] in ("frame", "stage1") and r.get("brick")]
    sent_used = [r for r in recs if r["kind"] == "sentence"]
    keeps = [r for r in recs if r["kind"] == "keep" or (r["kind"] == "stage1" and r.get("keep"))]
    s1 = None
    if any(r["kind"] == "stage1" for r in recs):
        s1 = check_stage1(pile, a.min_fit, a.max_new)
        fails += [f"stage 1: {x}" for x in s1["fails"]]
        warns += [f"stage 1: {x}" for x in s1["warns"]]
    if sent_used and not a.own_corpus:
        fails.append(f"{len(sent_used)} whole corpus sentences used without --own-corpus "
                     "(verbatim reuse of another author's sentence is plagiarism)")
    if keeps and a.strict:
        fails.append(f"--strict: {len(keeps)} draft sentences kept without a frame")

    # copy risk: corpus word runs that were not already in the draft
    n = a.copy_limit
    corpus_grams: set = set()
    if corpus.is_dir():
        for slug in pile.meta["papers"]:
            for f in sorted((corpus / "papers" / slug / "sections").glob("*.txt")):
                corpus_grams |= ngrams(words(f.read_text(encoding="utf-8", errors="replace")), n)
    draft_grams = ngrams(words(pile.draft_text), n)
    copy_hits = []
    for r in recs:
        if r["kind"] == "gap":
            continue
        hits = (ngrams(words(r["text"]), n) & corpus_grams) - draft_grams
        if hits:
            copy_hits.append((r["where"], " ".join(sorted(hits)[0])))
    if copy_hits:
        msg = (f"{len(copy_hits)} sentences repeat a {n}-word run from the corpus "
               f"that the draft did not have: " + "; ".join(f"{w} '{h}'" for w, h in copy_hits[:4]))
        (warns if a.own_corpus or a.allow_copy else fails).append(msg)

    # mortar shares
    tr = asm.trace
    count = lambda kinds: sum(len(words(t["text"])) for t in tr if t["kind"] in kinds)
    w_frame = count({"frame", "pick", "inflect"})
    w_bundle = count({"bundle"})
    # swapped-in words sit inside content and keep text; take each out of its own kind
    sw_in = lambda pfx: sum(len(words(x["to"])) for x in asm.swaps if x["brick"].startswith(pfx))
    w_content = count({"content"}) - sw_in("C")
    w_word = count({"word"})
    w_glue = count({"glue"})
    w_keep = count({"keep"}) - sw_in("D")
    n_trans = sum(1 for t in tr if t["kind"] == "transform")
    w_sent = count({"sentence"})
    w_out = len(words(rev)) if rev else 0
    w_draft = len(words(pile.draft_text))
    glue_share = w_glue / w_out if w_out else 0.0
    if glue_share > a.max_glue:
        fails.append(f"glue words are {glue_share:.0%} of the text (limit {a.max_glue:.0%}) — "
                     "the frames are not carrying the sentences")
    n_infl = sum(1 for t in tr if t["kind"] == "inflect")
    n_auto = sum(1 for t in tr if t["kind"] == "auto")

    # content accounting
    used_c = {t["id"] for t in tr if t["kind"] == "content"}
    unused = sorted(set(pile.content) - used_c, key=lambda c: int(c[1:]))
    if unused:
        warns.append(f"content bricks never used: {', '.join(unused)} — Gate 1 decides whether content was lost")
    if w_draft and abs(w_out - w_draft) / w_draft > 0.15:
        warns.append(f"length {w_out} words vs draft {w_draft} ({(w_out - w_draft) / w_draft:+.0%}); target ±15%")

    # brick rules
    pile_papers = sorted({r["paper"] for r in pile.form.values() if r["kind"] == "frame"})
    used_papers = sorted({r["brick"]["paper"] for r in frames_used})
    want = min(len(pile_papers), 3)
    if len(used_papers) < want:
        warns.append(f"frames from {len(used_papers)} papers; the rule asks for at least {want}")
    open_ok = close_ok = n_par = 0
    runs, longest = 0, 1
    for p in asm.paragraphs:
        if not p:
            continue
        n_par += 1
        first, last = p[0], p[-1]
        if first["kind"] in ("frame", "stage1") and first.get("brick") and first["brick"]["pos"] in ("initial", "solo"):
            open_ok += 1
        if last["kind"] == "gap" or (last["kind"] in ("frame", "stage1") and last.get("brick")
                                      and last["brick"]["pos"] in ("final", "solo")):
            close_ok += 1
        run = 1
        for x, y in zip(p, p[1:]):
            bx, by = x.get("brick"), y.get("brick")
            ax = ADDR_RE.search(bx["source"]) if bx else None
            ay = ADDR_RE.search(by["source"]) if by else None
            if bx and by and bx["paper"] == by["paper"] and ax and ay and \
                    (int(ax.group(1)), int(ax.group(2))) < (int(ay.group(1)), int(ay.group(2))):
                run += 1
                if run == 2:
                    runs += 1
                longest = max(longest, run)
            else:
                run = 1
    if open_ok < n_par:
        warns.append(f"{n_par - open_ok} of {n_par} paragraphs do not open on a corpus opener frame")
    if close_ok < n_par:
        warns.append(f"{n_par - close_ok} of {n_par} paragraphs do not close on a closer frame or a gap")
    singles = [r["brick"]["id"] for r in frames_used if r["brick"]["status"] == "singleton"]

    # strength profile: the whole text, draft vs revision, by class
    def profile(text: str) -> dict[str, int]:
        prof: dict[str, int] = {}
        for w in words(text):
            c = strength_of(w)
            if c != "-":
                prof[c] = prof.get(c, 0) + 1
        return prof
    pd, pr = profile(pile.draft_text), profile(rev or "")
    drift = {c: (pd.get(c, 0), pr.get(c, 0)) for c in sorted(set(pd) | set(pr))
             if pd.get(c, 0) != pr.get(c, 0)}
    if drift:
        warns.append("claim-strength profile changed: " + "; ".join(
            f"{c} {x} -> {y}" for c, (x, y) in drift.items()) +
            " — frames bring their own verbs and hedges; Gate 2 decides each")

    # word layer
    sw = asm.swaps
    by_cat: dict[str, int] = {}
    for x in sw:
        by_cat[x["category"]] = by_cat.get(x["category"], 0) + 1
    strength_sw = [x for x in sw if x["strength"] != "-"]
    unverified = [x for x in sw if x["pos"] == "unverified"]
    used_bricks = {t["id"] for t in tr if t["kind"] in ("content", "keep", "stage1")}
    idle = sorted(b for b in pile.swaps if b not in used_bricks)
    if idle:
        warns.append(f"swaps on bricks the plan never uses: {', '.join(idle)}")
    if unverified:
        warns.append(f"{len(unverified)} swaps with part of speech unverified (no tagger data) — "
                     "Gate 2 checks them by reading")
    foreign: dict[str, int] = {}
    if pile.attested:
        for t in tr:
            if t["kind"] not in ("content", "keep", "stage1"):
                continue
            spans = term_spans(t["text"], pile.terms)
            for m in WORD_RE.finditer(t["text"]):
                w = m.group(0).lower()
                if (re.search(r"\d", w) or len(w) < 3 or w in pile.attested or w in GLUE
                        or any(a0 < m.end() and m.start() < b0 for a0, b0 in spans)
                        or m.group(0)[:1].isupper() and m.start() > 0):
                    continue
                foreign[w] = foreign.get(w, 0) + 1
    # collocation evidence: each swapped-in word with its neighbours, counted in the corpus.
    # Evidence for Gate 2, not a refusal: a small corpus leaves most sound pairs unattested.
    bigrams: dict[tuple[str, str], int] = {}
    if corpus.is_dir():
        for slug in pile.meta["papers"]:
            for f in sorted((corpus / "papers" / slug / "sections").glob("*.txt")):
                ws = [x.lower() for x in words(f.read_text(encoding="utf-8", errors="replace"))]
                for pair in zip(ws, ws[1:]):
                    bigrams[pair] = bigrams.get(pair, 0) + 1
    unattested = []
    for x in sw:
        to = [y.lower() for y in words(x["to"])]
        sides = []
        for side, nb in (("left", x.get("left", "")), ("right", x.get("right", ""))):
            if not nb or not to:
                x[f"{side}_pair"], x[f"{side}_n"] = "", ""
                continue
            pair = (nb.lower(), to[0]) if side == "left" else (to[-1], nb.lower())
            x[f"{side}_pair"] = " ".join(pair)
            if nb.lower() in GLUE:
                x[f"{side}_n"] = "glue"
                continue
            x[f"{side}_n"] = str(bigrams.get(pair, 0))
            sides.append(bigrams.get(pair, 0))
        x["collocation"] = ("no content neighbour" if not sides else
                            "attested" if any(sides) else "unattested")
        if x["collocation"] == "unattested":
            unattested.append(x)
    if unattested:
        warns.append(f"{len(unattested)} of {len(sw)} swaps make no corpus-attested pair with a "
                     "content neighbour — Gate 2 reads each pair for collocation (see word-swaps.tsv)")
    if a.report:
        write_tsv(Path(a.report).with_name("word-swaps.tsv"),
                  ["where", "brick", "from", "to", "id", "category", "strength", "pos",
                   "left_pair", "left_n", "right_pair", "right_n", "collocation"], sw)

    real = [r for r in recs if r["kind"] != "gap"]
    imposed = len(frames_used) + len(sent_used)
    result = "PASS" if not fails else "FAIL"
    lines = [
        f"# brickyard {__version__} verify — {result}",
        "",
        f"section {pile.meta['section']}; unit {pile.meta['unit']}; papers in pile "
        f"{len(pile.meta['papers'])}: {', '.join(pile.meta['papers'])}",
        "",
        "## Imposition",
        f"- sentences built on a corpus frame: {imposed} of {len(real)} "
        f"({imposed / len(real):.0%})" if real else "- no sentences",
        f"- draft sentences kept unbuilt (keep): {len(keeps)}",
        f"- gaps: {len(asm.gaps)} of {MAX_GAPS}" + (": " + " | ".join(asm.gaps) if asm.gaps else ""),
        f"- frames from papers: {', '.join(used_papers) or 'none'} (rule: at least {want})",
        f"- same-paper runs in source order: {runs} (longest {longest if runs else 0})",
        f"- paragraphs opening on an opener frame: {open_ok}/{n_par}; closing on a closer or gap: {close_ok}/{n_par}",
        f"- singleton frames used: {len(singles)}" + (f" ({', '.join(singles)})" if singles else ""),
        "",
    ]
    if s1:
        t1 = s1["tot"]
        fits = [float(r["fit"]) for r in s1["rows"] if r["fit"]]
        lines += [
            "## Stage 1 (guided rewrite on declared frames)",
            f"- sentences on a frame: {len(fits)} of {len(s1['rows'])}; mean fit "
            f"{(sum(fits) / len(fits)) if fits else 0:.0%}, lowest {min(fits) if fits else 0:.0%}",
            f"- stage-1 words by source: frame {t1['frame']}, draft {t1['draft']}, glue {t1['glue']}, "
            f"new {t1['new']} ({s1['share']:.0%}; limit {a.max_new:.0%})",
            *[f"  - {r['id']} {r['frame']}: new [{r['new']}]" + (f"; missing fixed [{r['missing']}]" if r.get('missing') else "")
              + (f"; draft words lost [{r['lost']}]" if r['lost'] else "")
              for r in s1["rows"] if r["frame"] != "keep" and (r["new"] or r.get("missing") or r["lost"])],
            "",
        ]
    lines += [
        "## Word layer",
        f"- swaps: {len(sw)}" + (" (" + ", ".join(f"{k} {v}" for k, v in sorted(by_cat.items())) + ")" if sw else ""),
        f"- claim-strength swaps (same class kept; Gate 2 must read each): {len(strength_sw)}"
        + ("".join(f"\n  - {x['where']} {x['brick']}: {x['from']} -> {x['to']} [{x['strength']}]" for x in strength_sw)),
        f"- collocation: swaps whose new word pairs with a content neighbour attested in the corpus "
        f"{sum(1 for x in sw if x.get('collocation') == 'attested')}, unattested {len(unattested)}, "
        f"no content neighbour {sum(1 for x in sw if x.get('collocation') == 'no content neighbour')}"
        + "".join(f"\n  - {x['where']} {x['brick']}: {x['from']} -> {x['to']} "
                  f"[{' | '.join(q for q in (x['left_pair'], x['right_pair']) if q)}]" for x in unattested),
        f"- protected terms in the pile: {len(pile.terms)}",
        "- strength profile draft -> revision: " + (", ".join(
            f"{c} {pd.get(c, 0)}->{pr.get(c, 0)}" for c in sorted(set(pd) | set(pr))) or "none"),
        f"- draft words the corpus never uses, left in place: {len(foreign)}"
        + (" — " + ", ".join(sorted(foreign, key=lambda w: -foreign[w])[:15]) if foreign else ""),
        "",
        "## Where every word came from",
        f"- output words {w_out} (draft {w_draft})",
        f"- frame words {w_frame}, bundle words {w_bundle}, corpus sentences {w_sent}",
        f"- content words {w_content}, corpus words swapped in {w_word}, kept draft words {w_keep}"
        + (f", stage-1 sentence words {count({'stage1'}) - sw_in('T')}" if s1 else ""),
        f"- glue words {w_glue} ({glue_share:.0%}; limit {a.max_glue:.0%}); inflections {n_infl}; "
        f"content transforms {n_trans}; auto fixes {n_auto}",
        f"- copy check: {n}-word corpus runs not in the draft: {len(copy_hits)}",
        "",
    ]
    if fails:
        lines += ["## FAIL", *[f"- {x}" for x in fails], ""]
    if warns:
        lines += ["## Warnings", *[f"- {x}" for x in warns], ""]
    lines += ["Gate 1 (preservation_inventory.py) and Gate 2 (meaning) are separate and still required.",
              "Run Gate 1 on revision.gate1.txt (the revision with [YOU WRITE: …] gaps removed), "
              "so that a gap's instruction text is not counted as content."]
    report = "\n".join(lines) + "\n"
    if a.report:
        Path(a.report).write_text(report, encoding="utf-8")
    if rev is not None:
        g1 = Path(a.report).with_name("revision.gate1.txt") if a.report else \
            rev_path.with_name("revision.gate1.txt")
        g1.write_text(re.sub(r"[ \t]+([.,;:])", r"\1", re.sub(r"\s*\[YOU WRITE:[^\]]*\]", "", rev)),
                      encoding="utf-8")
    print(report, end="")
    return 0 if not fails else 1


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pile", help="build the brick pile from the corpus and the draft")
    p.add_argument("--corpus", required=True)
    p.add_argument("--section", required=True, choices=SECTION_ORDER)
    p.add_argument("--draft", required=True, help="0-draft.prose.txt")
    p.add_argument("--out", required=True)
    p.add_argument("--papers", help="comma-separated slugs (default: all)")
    p.add_argument("--unit", choices=["frame", "sentence"], default="frame")
    p.add_argument("--cross-section", action="store_true",
                   help="allow frames, bundles and words from any section")
    p.add_argument("--terms", help="the draft's own technical terms, one per line "
                   "(glossary.md of each paper is added automatically)")
    p = sub.add_parser("content", help="validate content.tsv against the draft")
    p.add_argument("--pile", required=True)
    p = sub.add_parser("assemble", help="build the text from plan.json")
    p.add_argument("--pile", required=True)
    p.add_argument("--plan", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--trace")
    p.add_argument("--swaps", nargs="*", help="word-swap files (default: pile/swaps*.json)")
    p = sub.add_parser("verify", help="re-assemble, trace, check the rules")
    p.add_argument("--pile", required=True)
    p.add_argument("--plan", required=True)
    p.add_argument("--revision", required=True)
    p.add_argument("--report")
    p.add_argument("--swaps", nargs="*", help="word-swap files (default: pile/swaps*.json)")
    p.add_argument("--own-corpus", action="store_true",
                   help="the corpus is the user's own papers: whole-sentence bricks and long "
                        "corpus runs become warnings instead of failures")
    p.add_argument("--allow-copy", action="store_true",
                   help="experiment only: corpus runs (and verbatim corpus sentences) become "
                        "warnings; the report marks the text as reusing other authors' wording")
    p.add_argument("--strict", action="store_true", help="fail on any keep")
    p.add_argument("--copy-limit", type=int, default=8)
    p.add_argument("--max-glue", type=float, default=0.15)
    p.add_argument("--min-fit", type=float, default=0.75, help="stage 1: least share of a frame's fixed words")
    p.add_argument("--max-new", type=float, default=0.10, help="stage 1: most share of new words")
    p = sub.add_parser("match", help="index corpus sentences (M###) and rank them per draft sentence")
    p.add_argument("--pile", required=True)
    p.add_argument("--top", type=int, default=5)
    p.add_argument("--all-sections", action="store_true", help="index I M R D C, not only the target section")
    p.add_argument("--same-match", type=float, default=0.80, help="'same content': least share of draft content words")
    p.add_argument("--same-extra", type=float, default=0.20, help="'same content': most share of corpus-only content words")
    p = sub.add_parser("stage1", help="check the guided rewrite (stage1.json) and write the stage-2 plan")
    p.add_argument("--pile", required=True)
    p.add_argument("--stage1", required=True, help="the frame writer's stage1.json")
    p.add_argument("--plan-out", required=True, help="stage-2 plan.json to write")
    p.add_argument("--report")
    p.add_argument("--min-fit", type=float, default=0.75)
    p.add_argument("--max-new", type=float, default=0.10)
    a = ap.parse_args()
    try:
        return {"pile": cmd_pile, "content": cmd_content, "stage1": cmd_stage1, "match": cmd_match,
                "assemble": cmd_assemble, "verify": cmd_verify}[a.cmd](a)
    except Blocked as e:
        print(f"BLOCKED: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
