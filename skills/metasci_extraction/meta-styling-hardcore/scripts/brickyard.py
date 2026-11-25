#!/usr/bin/env python3
"""brickyard.py — meta-styling-hardcore: the model picks bricks by ID, code builds the text.

The model never types a sentence of the revision. It writes a plan (plan.json) that
names bricks by ID; this script assembles the text from those IDs and verifies that
every word of the result traces to a brick.

  pile      corpus + draft      -> pile/ (form.tsv, draft.tsv, pile.json)
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
Mortar (the only things that are not bricks, all counted in verify.md):
  g:<word>    a glue word from the frozen GLUE list below
  ?:<text>    a [YOU WRITE: text] gap, one line, at most MAX_GAPS per run
  pick        choosing one alternative of a template choice token (was/were, suggest(s))
  inflect     a number-agreement change on a template word, from AGREEMENT or a
              regular -s/-es/-ies toggle
  auto        capitalisation, a/an, spacing before punctuation, terminal period

No dependencies beyond the standard library.
Version: 1.0.0 (2026-11-25)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

__version__ = "1.0.0"

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
    parts = re.split(r"(?<=[.!?])\s+(?=[\"“(\[]?[A-Z0-9δΔ])", protected)
    out = []
    for p in parts:
        p = re.sub(r"\x00(\d+)\x00", ".", p).replace("\x01", ".")
        if p.strip():
            out.append(p.strip())
    return out


def section_of_heading(line: str) -> str | None:
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
        if ln.lstrip().startswith("|") and "template" in ln.lower() and i + 1 < len(lines) \
                and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            head = [c.strip().lower() for c in ln.strip().strip("|").split("|")]

            def col(*keys, avoid=()):
                for k, h in enumerate(head):
                    if any(x in h for x in keys) and not any(a in h for a in avoid):
                        return k
                return None

            c_tpl = col("template")
            c_type = col("frame", "type", "code", avoid=("template",))
            c_orig = col("original", "sentence", avoid=("template",))
            c_src = col("source", "address", "loc")
            c_stat = col("recur", "status", "singleton")
            i += 2
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                get = lambda k: cells[k] if k is not None and k < len(cells) else ""
                tpl = get(c_tpl)
                if tpl:
                    typ = get(c_type)
                    m = CODE_RE.search(typ)
                    rows.append({
                        "section": section or "",
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

    def content_errors(self) -> list[str]:
        hay = norm_ws(self.draft_text)
        return [f"{cid}: not a verbatim span of the draft: {t!r}"
                for cid, t in self.content.items() if norm_ws(t) not in hay]


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


def render_item(item: str, pile: Pile, where: str, asm: Assembly, gaps: list) -> tuple[str, str, str]:
    """-> (text, kind, id)"""
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
        return pile.content[item], "content", item
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
    for pi, para in enumerate(paras, 1):
        sents = para.get("sentences") if isinstance(para, dict) else para
        out = []
        for si, spec in enumerate(sents or [], 1):
            where = f"P{pi}.S{si}"
            rec = {"where": where, "spec": spec}
            if "frame" in spec:
                rec.update(kind="frame", text=build_frame_sentence(spec, pile, asm, where, gaps),
                           brick=pile.form.get(spec["frame"]))
            elif "keep" in spec:
                d = pile.draft.get(spec["keep"])
                if not d:
                    asm.errors.append(f"{where}: keep {spec['keep']!r} is not a draft sentence")
                rec.update(kind="keep", text=d["text"] if d else "")
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
    pile = Pile(Path(a.pile))
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


# ---------------------------------------------------------------- verify

def ngrams(ws: list[str], n: int) -> set[tuple[str, ...]]:
    return {tuple(ws[i:i + n]) for i in range(len(ws) - n + 1)}


def cmd_verify(a) -> int:
    pile = Pile(Path(a.pile))
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
    else:
        warns.append("corpus folder not reachable; pile integrity not re-checked")
    if sha(Path(pile.meta["draft"])) != pile.meta["draft_sha"]:
        fails.append("the draft changed after the pile was built — rebuild the pile")

    recs = [r for p in asm.paragraphs for r in p]
    frames_used = [r for r in recs if r["kind"] == "frame" and r.get("brick")]
    sent_used = [r for r in recs if r["kind"] == "sentence"]
    keeps = [r for r in recs if r["kind"] == "keep"]
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
        (warns if a.own_corpus else fails).append(msg)

    # mortar shares
    tr = asm.trace
    count = lambda kinds: sum(len(words(t["text"])) for t in tr if t["kind"] in kinds)
    w_frame = count({"frame", "pick", "inflect"})
    w_bundle = count({"bundle"})
    w_content = count({"content"})
    w_glue = count({"glue"})
    w_keep = count({"keep"})
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
        if first["kind"] == "frame" and first.get("brick") and first["brick"]["pos"] in ("initial", "solo"):
            open_ok += 1
        if last["kind"] == "gap" or (last["kind"] == "frame" and last.get("brick")
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
        "## Where every word came from",
        f"- output words {w_out} (draft {w_draft})",
        f"- frame words {w_frame}, bundle words {w_bundle}, corpus sentences {w_sent}",
        f"- content words {w_content}, kept draft words {w_keep}",
        f"- glue words {w_glue} ({glue_share:.0%}; limit {a.max_glue:.0%}); inflections {n_infl}; auto fixes {n_auto}",
        f"- copy check: {n}-word corpus runs not in the draft: {len(copy_hits)}",
        "",
    ]
    if fails:
        lines += ["## FAIL", *[f"- {x}" for x in fails], ""]
    if warns:
        lines += ["## Warnings", *[f"- {x}" for x in warns], ""]
    lines += ["Gate 1 (preservation_inventory.py) and Gate 2 (meaning) are separate and still required."]
    report = "\n".join(lines) + "\n"
    if a.report:
        Path(a.report).write_text(report, encoding="utf-8")
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
                   help="allow frames and bundles from any section")
    p = sub.add_parser("content", help="validate content.tsv against the draft")
    p.add_argument("--pile", required=True)
    p = sub.add_parser("assemble", help="build the text from plan.json")
    p.add_argument("--pile", required=True)
    p.add_argument("--plan", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--trace")
    p = sub.add_parser("verify", help="re-assemble, trace, check the rules")
    p.add_argument("--pile", required=True)
    p.add_argument("--plan", required=True)
    p.add_argument("--revision", required=True)
    p.add_argument("--report")
    p.add_argument("--own-corpus", action="store_true",
                   help="the corpus is the user's own papers: whole-sentence bricks and long "
                        "corpus runs become warnings instead of failures")
    p.add_argument("--strict", action="store_true", help="fail on any keep")
    p.add_argument("--copy-limit", type=int, default=8)
    p.add_argument("--max-glue", type=float, default=0.15)
    a = ap.parse_args()
    try:
        return {"pile": cmd_pile, "content": cmd_content,
                "assemble": cmd_assemble, "verify": cmd_verify}[a.cmd](a)
    except Blocked as e:
        print(f"BLOCKED: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
