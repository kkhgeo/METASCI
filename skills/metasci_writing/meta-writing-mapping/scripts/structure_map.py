#!/usr/bin/env python3
"""structure_map.py — validate a manuscript structure map, compute its structural
checks, and render it as one self-contained HTML page.

The map (structure-map.json) is written by the model following
references/structure-map.md. This script does the deterministic part only:
it never decides what a paragraph means or which paragraph builds on which.

Modes:
  check MAP [--text DRAFT] [--json OUT]   validate + checks, report to stdout
  build MAP [--text DRAFT] [-o OUT.html]  the same, then write the HTML map

--text DRAFT (Markdown or plain text, paragraphs separated by blank lines;
heading lines and HTML comments are skipped) turns on the checks that need the
words themselves: every topic sentence must appear verbatim in its paragraph,
sentence addresses are compared with a simple sentence split, and each term's
first use is found in the text instead of taken from the map.

Exit status: 0 = valid (checks may still report findings), 1 = the map is
invalid (errors listed), 2 = usage or file problem.

Standard library only. Version 1.0.0.
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

VERSION = "1.0.0"
SCHEMA = "metasci/structure-map@1"
HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "assets" / "structure-map.html"

SECTION_TYPES = {"introduction", "methods", "results", "discussion", "conclusion", "abstract", "other"}
LINK_KINDS = {"evidence", "method", "premise", "contrast", "answers", "motivates", "continues"}
BASIS = {"explicit", "inferred", "planned"}
QUESTION_ROLES = {"gap", "question", "purpose", "hypothesis", "objective", "aim"}
# a link whose earlier end is later in the text is a forward reference; these kinds
# make the reader wait for something they need, so the finding is "중요"
NEEDED_KINDS = {"evidence", "method", "premise"}
HUB_IN, HUB_SENT = 5, 8

ADDR = re.compile(r"^P(\d+)(?:-S(\d+))?$")
ABBREV = re.compile(r"\b(?:et al|e\.g|i\.e|cf|Fig|Figs|Eq|Eqs|Ref|Refs|vs|approx|ca|No|Sect|Tab|resp|Dr|Mr|Ms)\.$", re.I)


def pnum(addr):
    m = ADDR.match(addr or "")
    return (int(m.group(1)), int(m.group(2)) if m.group(2) else None) if m else (None, None)


# ---------------------------------------------------------------- text --------
def read_paragraphs(path):
    raw = Path(path).read_text(encoding="utf-8")
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    paras = []
    for block in re.split(r"\n\s*\n", raw):
        lines = [l.strip() for l in block.strip().splitlines() if l.strip() and not l.lstrip().startswith("#")]
        if lines:
            paras.append(" ".join(lines))
    return paras


def split_sentences(p):
    parts, cur = [], ""
    for tok in re.split(r"(?<=[.!?。])\s+", p):
        cur = f"{cur} {tok}".strip() if cur else tok
        if ABBREV.search(cur) or re.search(r"\b[A-Z]\.$", cur):
            continue
        parts.append(cur)
        cur = ""
    if cur:
        parts.append(cur)
    return parts


def norm(s):
    return re.sub(r"\s+", " ", (s or "").replace(" ", " ")).strip()


def term_pattern(term):
    t = re.escape(norm(term))
    if re.search(r"[A-Za-z0-9]$", term) and re.match(r"[A-Za-z0-9]", term):
        return re.compile(r"(?<![A-Za-z0-9])" + t + r"(?![A-Za-z0-9])", re.I)
    return re.compile(t, re.I)  # Hangul: prefix match lets particles attach


# ---------------------------------------------------------------- validate ----
def validate(m, paras):
    err, warn = [], []
    if m.get("$schema") != SCHEMA:
        warn.append(f'$schema는 "{SCHEMA}"여야 합니다 (현재: {m.get("$schema")!r}).')
    src = m.get("source") or {}
    kind = src.get("kind", "draft")
    if kind not in ("draft", "outline"):
        err.append(f'source.kind는 "draft" 또는 "outline"입니다 (현재: {kind!r}).')
    secs = m.get("sections") or []
    pars = m.get("paragraphs") or []
    links = m.get("links") or []
    if not secs:
        err.append("sections가 비어 있습니다.")
    if not pars:
        err.append("paragraphs가 비어 있습니다.")
    sec_ids = set()
    for i, s in enumerate(secs):
        if not s.get("id"):
            err.append(f"sections[{i}]에 id가 없습니다.")
        elif s["id"] in sec_ids:
            err.append(f"섹션 id {s['id']}이(가) 중복됩니다.")
        sec_ids.add(s.get("id"))
        if s.get("type", "other") not in SECTION_TYPES:
            err.append(f"섹션 {s.get('id')}의 type {s.get('type')!r}은 {sorted(SECTION_TYPES)} 중 하나여야 합니다.")
    pid, prev = {}, 0
    for i, p in enumerate(pars):
        n, s = pnum(p.get("id"))
        if n is None or s is not None:
            err.append(f"paragraphs[{i}]의 id {p.get('id')!r}는 P#(예: P12) 형식이어야 합니다.")
            continue
        if p["id"] in pid:
            err.append(f"{p['id']} 단락이 중복됩니다.")
        if n <= prev:
            err.append(f"{p['id']} 단락이 원고 순서보다 앞에 놓였습니다. paragraphs는 읽기 순서대로 적습니다.")
        prev = n
        pid[p["id"]] = p
        if p.get("section") not in sec_ids:
            err.append(f"단락 {p['id']}의 section {p.get('section')!r}이 sections에 없습니다.")
        if not norm(p.get("topic")):
            err.append(f"단락 {p['id']}에 topic(주제문)이 없습니다.")
        if not p.get("role"):
            warn.append(f"단락 {p['id']}에 role(기능 태그)이 없습니다.")
        if kind == "draft":
            tn, ts = pnum(p.get("topic_at"))
            if tn != n or ts is None:
                err.append(f"단락 {p['id']}의 topic_at {p.get('topic_at')!r}은 {p['id']}-S# 형식이어야 합니다.")
            elif p.get("sentences") and ts > p["sentences"]:
                err.append(f"단락 {p['id']}의 topic_at {p['topic_at']}의 문장 번호가 문장 수({p['sentences']}개)를 넘습니다.")
        tn = p.get("to_next")
        if tn is not None and not isinstance(tn, dict):
            err.append(f"단락 {p['id']}의 to_next는 {{relation, signal}} 객체여야 합니다.")
    for c in m.get("main_claims") or []:
        if c not in pid:
            err.append(f"main_claims의 {c} 단락이 paragraphs에 없습니다.")

    def addr_ok(a, where):
        n, s = pnum(a)
        if n is None:
            err.append(f"{where}: 주소 {a!r}는 P#-S# 형식이어야 합니다.")
            return
        p = pid.get(f"P{n}")
        if p is None:
            err.append(f"{where}: 주소 {a}의 단락 P{n}이 지도에 없습니다.")
        elif s is not None and p.get("sentences") and s > p["sentences"]:
            err.append(f"{where}: 주소 {a}의 문장 번호가 P{n}의 문장 수({p['sentences']}개)를 넘습니다.")

    for i, l in enumerate(links):
        w = f"links[{i}] {l.get('from')}→{l.get('to')}"
        for end in ("from", "to"):
            if l.get(end) not in pid:
                err.append(f"{w}: {end} 단락 {l.get(end)!r}이(가) paragraphs에 없습니다.")
        if l.get("from") == l.get("to"):
            err.append(f"{w}: 단락이 자기 자신에 기댈 수 없습니다.")
        if l.get("kind") not in LINK_KINDS:
            err.append(f"{w}: kind {l.get('kind')!r}는 {sorted(LINK_KINDS)} 중 하나여야 합니다.")
        b = l.get("basis")
        if b not in BASIS:
            err.append(f"{w}: basis {b!r}는 explicit / inferred / planned 중 하나여야 합니다.")
        elif kind == "draft" and b == "planned":
            err.append(f"{w}: 초고 지도에는 planned 연결을 쓰지 않습니다.")
        if kind == "draft":
            if not l.get("at"):
                err.append(f"{w}: at(근거 문장 주소)이 없습니다.")
            else:
                addr_ok(l["at"], w)
                an, _ = pnum(l["at"])
                if an is not None and f"P{an}" != l.get("to"):
                    warn.append(f"{w}: at {l['at']}은 기대는 쪽 단락({l.get('to')}) 안의 문장이어야 합니다.")
            if b == "explicit" and not norm(l.get("signal")):
                err.append(f"{w}: explicit 연결에는 원문 그대로의 signal이 필요합니다.")
            if b == "inferred" and not norm(l.get("note")) and not norm(l.get("signal")):
                warn.append(f"{w}: inferred 연결에 판단 이유(note)가 없습니다.")
    for i, c in enumerate(m.get("citations") or []):
        if not c.get("key"):
            err.append(f"citations[{i}]에 key가 없습니다.")
        for a in c.get("at") or []:
            addr_ok(a, f"citations[{i}] {c.get('key')}")
    for i, t in enumerate(m.get("terms") or []):
        if not norm(t.get("term")):
            err.append(f"terms[{i}]에 term이 없습니다.")
        for k in ("defined_at", "first_used_at"):
            if t.get(k):
                addr_ok(t[k], f"terms[{i}] {t.get('term')}.{k}")

    # ---- against the text
    if paras is not None:
        for p in pars:
            n, _ = pnum(p.get("id"))
            if n is None:
                continue
            if n > len(paras):
                err.append(f"단락 {p['id']}: 원고에는 단락이 {len(paras)}개뿐입니다.")
                continue
            body = norm(paras[n - 1])
            topic = norm(p.get("topic"))
            if topic and topic not in body:
                err.append(f"단락 {p['id']}: topic이 원고의 해당 단락에 그대로 있지 않습니다. 주제문은 고쳐 쓰지 않고 옮겨 적습니다.")
                continue
            sents = [norm(s) for s in split_sentences(body)]
            if p.get("sentences") and p["sentences"] != len(sents):
                warn.append(f"단락 {p['id']}: 문장 수가 지도에는 {p['sentences']}개, 자동 분할로는 {len(sents)}개입니다 (약어 때문일 수 있음).")
            _, ts = pnum(p.get("topic_at"))
            if ts and topic and len(sents) >= ts and topic not in sents[ts - 1]:
                warn.append(f"단락 {p['id']}: topic이 자동 분할한 S{ts}에 있지 않습니다. topic_at을 확인하세요.")
        for l in links:
            sig = norm(l.get("signal"))
            an, _ = pnum(l.get("at"))
            if sig and an and an <= len(paras) and sig.lower() not in norm(paras[an - 1]).lower():
                warn.append(f"연결 {l.get('from')}→{l.get('to')}: signal \"{sig}\"이 {l.get('at')} 단락에 그대로 없습니다.")
        for t in m.get("terms") or []:
            if not norm(t.get("term")):
                continue
            pat = term_pattern(t["term"])
            first = next((i + 1 for i, b in enumerate(paras) if pat.search(b)), None)
            if first is None:
                warn.append(f"용어 \"{t['term']}\"이 원고에 나오지 않습니다.")
                continue
            given, _ = pnum(t.get("first_used_at"))
            if given and given != first:
                warn.append(f"용어 \"{t['term']}\": 첫 사용이 지도에는 P{given}, 원고에서는 P{first}입니다. 원고 기준으로 판정합니다.")
            t["first_used_at"] = f"P{first}"
            t["_first_from_text"] = True
    return err, warn


# ---------------------------------------------------------------- checks ------
def checks(m):
    out = []
    pars = m["paragraphs"]
    idx = {p["id"]: i for i, p in enumerate(pars)}
    num = {p["id"]: pnum(p["id"])[0] for p in pars}
    sec = {s["id"]: s for s in m["sections"]}
    stype = {p["id"]: sec[p["section"]].get("type", "other") for p in pars}
    links = m.get("links") or []
    types = set(stype.values())
    incoming = {p["id"]: [] for p in pars}
    outgoing = {p["id"]: [] for p in pars}
    for l in links:
        incoming[l["to"]].append(l)
        outgoing[l["from"]].append(l)

    def add(code, sev, title, ids, detail, gate):
        out.append({"code": code, "severity": sev, "title": title, "ids": ids, "detail": detail, "gate": gate})

    # 1 forward references: a paragraph relies on one the reader has not met yet
    for l in links:
        if num[l["from"]] > num[l["to"]] and not l.get("forward_ok"):
            sev = "high" if l["kind"] in NEEDED_KINDS else "mid"
            add("forward-reference", sev, f"앞선 참조: {l['to']} 단락이 뒤의 {l['from']}에 기댐", [l["to"], l["from"]],
                f"{l['to']} 단락은 {l['from']}의 내용({KIND_KO[l['kind']]})을 쓰지만, 독자는 아직 {l['from']} 단락을 읽지 않았습니다."
                + (f" 근거: {l['at']}." if l.get("at") else ""), "순서")
    for t in m.get("terms") or []:
        d, _ = pnum(t.get("defined_at"))
        f, _ = pnum(t.get("first_used_at"))
        if d and f and f < d:
            add("term-before-definition", "high", f"정의 전 사용: \"{t['term']}\"", [f"P{f}", f"P{d}"],
                f"\"{t['term']}\"이 P{f}에서 먼저 쓰이고 P{d}에서 정의됩니다."
                + (" (첫 사용 위치는 원고에서 찾았습니다.)" if t.get("_first_from_text") else ""), "순서")

    # 2 results without a method paragraph (only when both are in the map)
    if "methods" in types and "results" in types:
        for p in pars:
            if stype[p["id"]] == "results" and not any(l["kind"] == "method" for l in incoming[p["id"]]):
                add("result-without-method", "mid", f"방법 연결 없음: {p['id']}", [p["id"]],
                    f"{p['id']}의 결과를 얻은 절차와 이어지는 방법 단락이 지도에 없습니다. 보충자료나 방법 문헌에 있다면 그대로 두어도 됩니다.",
                    "결과↔방법")

    # 3 questions the later sections never answer (only when they are in the map)
    answer_types = {"discussion", "conclusion"}
    if types & answer_types:
        for p in pars:
            if (p.get("role") or "").lower() in QUESTION_ROLES:
                ok = any(l["kind"] == "answers" and stype[l["to"]] in answer_types for l in outgoing[p["id"]])
                if not ok:
                    add("unanswered-question", "high", f"답이 이어지지 않은 질문: {p['id']}", [p["id"]],
                        f"{p['id']} 단락({p.get('role')})이 제기한 질문·목적에 논의나 결론의 어느 단락도 답하는 연결이 없습니다.",
                        "질문 사슬")

    # 4 orphans: nothing leads from the paragraph to a main claim
    claims = m.get("main_claims") or []
    if claims:
        up, q = set(claims), list(claims)
        while q:
            x = q.pop()
            for l in incoming[x]:
                if l["from"] not in up:
                    up.add(l["from"])
                    q.append(l["from"])
        for p in pars:
            if p["id"] not in up:
                users = [l["to"] for l in outgoing[p["id"]]]
                add("orphan", "mid", f"주 주장과 이어지지 않는 단락: {p['id']}", [p["id"]],
                    f"{p['id']}에서 출발해 주 주장({', '.join(claims)})에 닿는 연결이 없습니다."
                    + (" 이 단락에 기대는 단락도 없습니다." if not users else f" 이 단락에 기대는 단락: {', '.join(users)}."),
                    "결론 기여")

    # 5 weak transitions between adjacent paragraphs of one section
    linked = {(l["from"], l["to"]) for l in links}
    for a, b in zip(pars, pars[1:]):
        if a["section"] != b["section"] or num[b["id"]] != num[a["id"]] + 1:
            continue
        rel = (a.get("to_next") or {}).get("relation", "")
        if rel and rel.lower() != "none":
            continue
        if (a["id"], b["id"]) in linked or (b["id"], a["id"]) in linked:
            continue
        add("weak-transition", "mid", f"약한 전환: {a['id']} → {b['id']}", [a["id"], b["id"]],
            f"붙어 있는 두 단락 사이에 관계 신호도 직접 연결도 없습니다. 다음 단락({b['id']})으로 넘어가는 이유가 독자에게 드러나는지 확인하세요.",
            "연결")

    # 6 overloaded paragraphs
    for p in pars:
        if len(incoming[p["id"]]) >= HUB_IN and (p.get("sentences") or 0) >= HUB_SENT:
            add("overloaded", "info", f"과적재 후보: {p['id']}", [p["id"]],
                f"{p['id']} 단락에 {len(incoming[p['id']])}개 단락이 기대고, 문장이 {p['sentences']}개입니다. 나눌 수 있는지 볼 만합니다.", "단락 역할")

    # 7 cycles (contrast links excluded)
    graph = {p["id"]: [l["to"] for l in outgoing[p["id"]] if l["kind"] != "contrast"] for p in pars}
    for comp in scc(graph):
        if len(comp) > 1:
            comp = sorted(comp, key=lambda x: idx[x])
            add("cycle", "mid", f"순환 후보: {', '.join(comp)}", comp,
                "이 단락들이 서로에게 기대는 고리를 이룹니다. 근거 대신 같은 주장을 바꿔 말하고 있지 않은지 내용으로 판단하세요.",
                "명제 일관성")
    order = {"high": 0, "mid": 1, "info": 2}
    out.sort(key=lambda c: (order[c["severity"]], idx.get(c["ids"][0], 0)))
    return out


KIND_KO = {"evidence": "근거", "method": "방법", "premise": "전제·정의", "contrast": "대조",
           "answers": "질문에 답함", "motivates": "동기", "continues": "전개"}


def scc(graph):
    index, low, stack, on, res, counter = {}, {}, [], set(), [], [0]

    def visit(v):
        index[v] = low[v] = counter[0]
        counter[0] += 1
        stack.append(v)
        on.add(v)
        for w in graph.get(v, []):
            if w not in index:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on:
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            comp = []
            while True:
                w = stack.pop()
                on.discard(w)
                comp.append(w)
                if w == v:
                    break
            res.append(comp)

    sys.setrecursionlimit(max(1000, 4 * len(graph) + 100))
    for v in graph:
        if v not in index:
            visit(v)
    return res


# ---------------------------------------------------------------- output ------
SEV_KO = {"high": "중요", "mid": "확인", "info": "참고"}


def report(path, err, warn, found):
    print(f"structure_map.py {VERSION} · {path}")
    if err:
        print(f"\n오류 {len(err)}건 — 지도를 고친 뒤 다시 실행하세요.")
        for e in err:
            print(f"  ✗ {e}")
    if warn:
        print(f"\n경고 {len(warn)}건")
        for w in warn:
            print(f"  ! {w}")
    if found is not None:
        counts = {k: sum(1 for c in found if c["severity"] == k) for k in SEV_KO}
        print(f"\n구조 점검 {len(found)}건 (중요 {counts['high']} · 확인 {counts['mid']} · 참고 {counts['info']}) — 판정이 아니라 후보입니다.")
        for c in found:
            print(f"  [{SEV_KO[c['severity']]}] {c['title']} ({c['gate']})\n      {c['detail']}")


def render(m, found, warn, out):
    tpl = TEMPLATE.read_text(encoding="utf-8")
    data = {"map": m, "checks": found, "warnings": warn, "version": VERSION}
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/").replace("<!--", "<\\!--")
    if "/*__MAP_DATA__*/null" not in tpl:
        raise SystemExit("assets/structure-map.html에 데이터 자리(/*__MAP_DATA__*/null)가 없습니다.")
    page = tpl.replace("/*__MAP_DATA__*/null", blob, 1)
    page = page.replace("<title>원고 구조 지도</title>", f"<title>{html.escape(m.get('title') or '원고 구조 지도')}</title>", 1)
    Path(out).write_text(page, encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--version", action="version", version=VERSION)
    sub = ap.add_subparsers(dest="mode", required=True)
    for name in ("check", "build"):
        sp = sub.add_parser(name)
        sp.add_argument("map")
        sp.add_argument("--text", help="원고 파일 (빈 줄로 단락 구분)")
        if name == "check":
            sp.add_argument("--json", help="점검 결과를 JSON으로 저장")
        else:
            sp.add_argument("-o", "--out", help="HTML 출력 경로 (기본: 지도 파일 옆 .html)")
    a = ap.parse_args(argv)
    try:
        m = json.loads(Path(a.map).read_text(encoding="utf-8"))
        paras = read_paragraphs(a.text) if a.text else None
    except (OSError, json.JSONDecodeError) as e:
        print(f"파일을 읽을 수 없습니다: {e}", file=sys.stderr)
        return 2
    err, warn = validate(m, paras)
    found = None if err else checks(m)
    report(a.map, err, warn, found)
    if err:
        return 1
    if a.mode == "check" and a.json:
        Path(a.json).write_text(json.dumps({"checks": found, "warnings": warn}, ensure_ascii=False, indent=2), encoding="utf-8")
    if a.mode == "build":
        out = a.out or str(Path(a.map).with_suffix(".html"))
        render(m, found, warn, out)
        print(f"\nHTML 지도: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
