#!/usr/bin/env python3
"""quant_check.py — AntConc-style quantitative verification for META-SCI extraction skills.

Verifies LLM-extracted items (words, phrases, frame anchors) against actual corpus
counts, in the spirit of AntConc: every claim gets Freq, NormFreq (per 1k tokens),
and Range (number of files containing it).

Modes:
  count      --items FILE  file1 [file2 ...]   Freq/NormFreq/Range per item
  collocates --node TERM [--window N] files    co-occurring words near a node term
  profile    files                             tokens, sentences, avg sentence length,
                                               hedging & passive rate per 1k tokens
  keyness    --target FILE(s) --reference FILE(s)
                                               log-likelihood keyness, target vs reference

Input files: .txt / .md read as UTF-8; .pdf extracted with pypdf.
Items file: one item per line; multi-word phrases allowed; '#' comments ignored.
Matching: case-insensitive, word-boundary. A trailing '*' allows suffix wildcard
(e.g. "demonstrat*" matches demonstrate/demonstrated/demonstrating).

Output: TSV to stdout (UTF-8).

Notes:
  --strip-refs (global flag, place BEFORE the mode) cuts the reference list; use it
  whenever counting authorial prose. PDF text is automatically dehyphenated.
  For per-section counts, split the prose into per-section .txt files and pass them
  with `count --per-file`.

Korean mode (EXPERIMENTAL): files whose text is predominantly Hangul are detected
automatically. Tokens are eojeol chunks; sentences split on formal endings (…다. /
…함. / …음.); `profile` uses a Korean hedging inventory and a 되다/어지다-family
passive approximation. Hangul items in `count` match with attached particles
(prefix match: "평가" also counts "평가는", "평가를").

Version: 1.2.0 (shared across extraction-vocab / extraction-logic /
extraction-style / meta-styling)
"""
import argparse
import math
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

TOKEN_RE = re.compile(r"[A-Za-zÀ-ɏ][A-Za-zÀ-ɏ'\-]*|[가-힣][가-힣]*")

HANGUL_RE = re.compile(r"[가-힣]")

# Finite hedging inventory (Hyland-style core; used by `profile`)
HEDGES = [
    "may", "might", "could", "would", "should", "can",
    "likely", "unlikely", "possibly", "probably", "perhaps",
    "appear*", "seem*", "suggest*", "indicat*", "imply", "implies", "implied",
    "assume*", "estimate*", "approximate*", "approximately",
    "relatively", "generally", "typically", "largely", "somewhat",
    "tend*", "presumably", "potentially", "apparently",
]

# Rough passive detector: be-form + past participle (approximation, not a parser)
PASSIVE_RE = re.compile(
    r"\b(is|are|was|were|be|been|being)\s+(\w+ed|\w+en|shown|done|made|found|seen|known|given|taken|built|held|kept|left|lost|met|put|read|said|sent|set|told|thought|understood|written|drawn|chosen|driven|frozen|hidden|risen|broken)\b",
    re.IGNORECASE,
)

SENT_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-ZÀ-ɏ(가-힣])")

# --- Korean (EXPERIMENTAL) -------------------------------------------------
# Formal-register hedging inventory (institutional/academic Korean)
HEDGES_KO = [
    "것으로 보인다", "것으로 보이며", "것으로 판단된다", "것으로 판단되며",
    "것으로 사료된다", "것으로 예상된다", "것으로 추정된다", "것으로 전망된다",
    "수 있다", "수 있으며", "수 있을", "수 있는",
    "가능성", "추정", "예상되", "전망되",
    "다소", "대체로", "일반적으로", "상대적으로", "비교적",
    "약 ", "정도", "수준으로 보",
]
# Passive/causative-passive approximation: 되다 / 어지다 families
PASSIVE_KO_RE = re.compile(
    r"[가-힣]+(된다|되었다|되며|되었으며|되어|되고|됨|어진다|어졌다|어지는|어지고)\b"
)


def is_korean(text: str) -> bool:
    """Predominantly-Hangul detection: Hangul chars vs Latin letters."""
    hangul = len(HANGUL_RE.findall(text))
    latin = len(re.findall(r"[A-Za-z]", text))
    return hangul > 0 and hangul >= latin * 0.5
# ---------------------------------------------------------------------------


def dehyphenate(text: str) -> str:
    """Repair words split by PDF line-break hyphenation.
    Handles 'sug-\\ngests', 'sug- gests', and pypdf's 'sug - gests' artifacts.
    Only joins lowercase fragments so genuine hyphenated compounds written
    without spaces (large-scale) are untouched."""
    text = re.sub(r"([a-z]) *-[ \t]*\n\s*([a-z])", r"\1\2", text)  # sug-\ngests, sug -\ngests
    text = re.sub(r"([a-z])- +([a-z])", r"\1\2", text)             # sug- gests
    text = re.sub(r"([a-z]) +- +([a-z])", r"\1\2", text)           # sug - gests
    return text


def strip_references(text: str) -> str:
    """Cut everything from the last References/Bibliography heading onward."""
    m = None
    for m_ in re.finditer(r"\n\s*(References|REFERENCES|Bibliography|BIBLIOGRAPHY|Literature cited)\s*\n",
                          text):
        m = m_
    return text[: m.start()] if m else text


STRIP_REFS = False  # set from --strip-refs


def read_text(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError:
            from PyPDF2 import PdfReader  # type: ignore
        reader = PdfReader(str(path))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        text = dehyphenate(text)
    else:
        text = path.read_text(encoding="utf-8", errors="replace")
    if STRIP_REFS:
        text = strip_references(text)
    return text


def tokenize(text: str):
    return TOKEN_RE.findall(text.lower())


def item_to_regex(item: str) -> re.Pattern:
    """Build a word-boundary, case-insensitive regex for a word/phrase item.
    Trailing '*' on any word = suffix wildcard. Whitespace in phrases matches
    any whitespace run (so line-wrapped phrases still match).
    Hangul items match with attached particles: leading boundary only
    ("평가" also matches "평가는" but not "재평가")."""
    words = item.strip().split()
    korean = bool(HANGUL_RE.search(item))
    parts = []
    for w in words:
        if w.endswith("*"):
            parts.append(re.escape(w[:-1]) + (r"[가-힣]*" if korean else r"[a-z'\-]*"))
        else:
            parts.append(re.escape(w))
    if korean:
        pattern = r"(?<![가-힣])" + r"\s+".join(parts)
    else:
        pattern = r"\b" + r"\s+".join(parts) + r"\b"
    return re.compile(pattern, re.IGNORECASE)


def load_items(path: Path):
    items = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            items.append(line)
    return items


def cmd_count(args):
    items = load_items(Path(args.items))
    files = [Path(f) for f in args.files]
    texts = {f: read_text(f) for f in files}
    token_counts = {f: len(tokenize(t)) for f, t in texts.items()}
    total_tokens = sum(token_counts.values()) or 1

    header = ["item", "total_freq", "norm_per_1k", "range", "n_files"]
    if args.per_file:
        header += [f.name for f in files]
    print("\t".join(header))

    for item in items:
        rx = item_to_regex(item)
        per_file = {f: len(rx.findall(texts[f])) for f in files}
        total = sum(per_file.values())
        rng = sum(1 for v in per_file.values() if v > 0)
        row = [item, str(total), f"{1000 * total / total_tokens:.2f}",
               str(rng), str(len(files))]
        if args.per_file:
            row += [str(per_file[f]) for f in files]
        print("\t".join(row))


def cmd_collocates(args):
    files = [Path(f) for f in args.files]
    node_rx = item_to_regex(args.node)
    window = args.window
    node_len = len(args.node.split())

    colloc = Counter()
    node_hits = 0
    all_tokens = Counter()
    for f in files:
        text = read_text(f)
        tokens = tokenize(text)
        all_tokens.update(tokens)
        # locate node positions on the token stream
        joined = " ".join(tokens)
        # token-index positions of node matches
        for m in node_rx.finditer(joined):
            node_hits += 1
            start_tok = joined[: m.start()].count(" ")
            lo = max(0, start_tok - window)
            hi = min(len(tokens), start_tok + node_len + window)
            for i in range(lo, hi):
                if start_tok <= i < start_tok + node_len:
                    continue
                colloc[tokens[i]] += 1

    total_tokens = sum(all_tokens.values()) or 1
    print(f"# node: {args.node}\thits: {node_hits}\twindow: ±{window}")
    print("collocate\tco_freq\tcorpus_freq\tlog_likelihood")
    rows = []
    span = node_hits * 2 * window or 1
    for w, co in colloc.most_common():
        if co < args.min_freq:
            continue
        # 2-term log-likelihood (AntConc manual, Likelihood Statistics)
        o11 = co
        e11 = span * all_tokens[w] / total_tokens
        o21 = all_tokens[w] - co
        e21 = (total_tokens - span) * all_tokens[w] / total_tokens
        ll = 0.0
        if o11 > 0 and e11 > 0:
            ll += o11 * math.log(o11 / e11)
        if o21 > 0 and e21 > 0:
            ll += o21 * math.log(o21 / e21)
        ll *= 2
        rows.append((w, co, all_tokens[w], ll))
    rows.sort(key=lambda r: -r[3])
    for w, co, cf, ll in rows[: args.top]:
        print(f"{w}\t{co}\t{cf}\t{ll:.2f}")


def cmd_profile(args):
    files = [Path(f) for f in args.files]
    hedge_rx_en = [item_to_regex(h) for h in HEDGES]
    hedge_rx_ko = [item_to_regex(h) for h in HEDGES_KO]
    print("file\tlang\ttokens\tsentences\tavg_sent_len\thedges_per_1k\tpassive_per_1k")
    for f in files:
        text = read_text(f)
        ko = is_korean(text)
        tokens = tokenize(text)
        n_tok = len(tokens) or 1
        sents = [s for s in SENT_SPLIT_RE.split(text) if len(s.split()) > 2]
        n_sent = len(sents) or 1
        if ko:
            hedge_n = sum(len(rx.findall(text)) for rx in hedge_rx_ko)
            passive_n = len(PASSIVE_KO_RE.findall(text))
        else:
            hedge_n = sum(len(rx.findall(text)) for rx in hedge_rx_en)
            passive_n = len(PASSIVE_RE.findall(text))
        lang = "ko" if ko else "en"
        print(f"{f.name}\t{lang}\t{n_tok}\t{n_sent}\t{n_tok / n_sent:.1f}"
              f"\t{1000 * hedge_n / n_tok:.1f}\t{1000 * passive_n / n_tok:.1f}")


def cmd_keyness(args):
    tgt_files = [Path(f) for f in args.target]
    ref_files = [Path(f) for f in args.reference]
    tgt = Counter()
    ref = Counter()
    for f in tgt_files:
        tgt.update(tokenize(read_text(f)))
    for f in ref_files:
        ref.update(tokenize(read_text(f)))
    n_tgt = sum(tgt.values()) or 1
    n_ref = sum(ref.values()) or 1

    rows = []
    for w, o11 in tgt.items():
        if o11 < args.min_freq:
            continue
        o21 = ref.get(w, 0)
        # 2-term log-likelihood (AntConc manual): expected under equal rates
        e11 = n_tgt * (o11 + o21) / (n_tgt + n_ref)
        e21 = n_ref * (o11 + o21) / (n_tgt + n_ref)
        ll = 0.0
        if o11 > 0 and e11 > 0:
            ll += o11 * math.log(o11 / e11)
        if o21 > 0 and e21 > 0:
            ll += o21 * math.log(o21 / e21)
        ll *= 2
        if o11 / n_tgt < (o21 / n_ref if o21 else 0):
            ll = -ll  # negative keyness (underused in target)
        rows.append((w, o11, o21, 1000 * o11 / n_tgt, 1000 * o21 / n_ref, ll))
    rows.sort(key=lambda r: -r[5])
    print("word\ttarget_freq\tref_freq\ttarget_per_1k\tref_per_1k\tlog_likelihood")
    for w, f1, f2, n1, n2, ll in rows[: args.top]:
        print(f"{w}\t{f1}\t{f2}\t{n1:.2f}\t{n2:.2f}\t{ll:.2f}")


def main():
    global STRIP_REFS
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--strip-refs", action="store_true",
                   help="cut text at the last References/Bibliography heading "
                        "(recommended whenever counting authorial prose)")
    sub = p.add_subparsers(dest="mode", required=True)

    c = sub.add_parser("count", help="verify Freq/NormFreq/Range for an item list")
    c.add_argument("--items", required=True, help="file with one item per line")
    c.add_argument("--per-file", action="store_true", help="add per-file count columns")
    c.add_argument("files", nargs="+")
    c.set_defaults(func=cmd_count)

    co = sub.add_parser("collocates", help="collocates of a node term (AntConc Collocate)")
    co.add_argument("--node", required=True)
    co.add_argument("--window", type=int, default=4)
    co.add_argument("--min-freq", type=int, default=2)
    co.add_argument("--top", type=int, default=20)
    co.add_argument("files", nargs="+")
    co.set_defaults(func=cmd_collocates)

    pr = sub.add_parser("profile", help="tokens/sentence-length/hedging/passive rates")
    pr.add_argument("files", nargs="+")
    pr.set_defaults(func=cmd_profile)

    k = sub.add_parser("keyness", help="log-likelihood keyness target vs reference")
    k.add_argument("--target", nargs="+", required=True)
    k.add_argument("--reference", nargs="+", required=True)
    k.add_argument("--min-freq", type=int, default=3)
    k.add_argument("--top", type=int, default=50)
    k.set_defaults(func=cmd_keyness)

    args = p.parse_args()
    STRIP_REFS = args.strip_refs
    args.func(args)


if __name__ == "__main__":
    main()
