# Stage 0 — prep

Turn one paper into the shared, normalized inputs every lens reads. Run this first,
always. No lens may read the PDF itself.

```bash
py -3.10 scripts/prep.py <paper.pdf> --slug <slug> --out <corpus-root>
```

On Windows use `py -3.10` (or whichever interpreter has `pypdf`), not bare `python` —
a bare `python` may resolve to a virtualenv without `pypdf` and the script will exit
telling you which interpreter it is running as.

## What it produces

```
<corpus-root>/papers/<slug>/
    source.pdf
    body.txt          NFKC-normalized · dehyphenated · back matter cut
    sections/A.txt    front matter + abstract
    sections/I.txt    Introduction
    sections/M.txt    Methods
    sections/R.txt    Results  (or fused Results-and-Discussion)
    sections/D.txt    Discussion   — only if the paper separates it
    sections/C.txt    Conclusions  — only if the paper has one
    manifest.json     deterministic fields filled, judgment fields null
```

## Why it exists — the ligature trap

Journal PDFs are typeset with printer's ligatures: `ﬁ` (U+FB01), `ﬂ` (U+FB02) and
friends. They look like ordinary letter pairs and are not. Against a raw PDF,
`quant_check count` returns **0** for every word containing one.

Measured on `kkh_nitrate_iso.pdf` — 172 ligature characters:

| word | raw PDF | normalized |
|------|---------|-----------|
| fitted | **0** | 21 |
| significant | **0** | 17 |
| confidence | **0** | 15 |
| first | **0** | 13 |
| field | **0** | 13 |
| difficult | **0** | 7 |

Every one is a core term of that paper. A card built on raw-PDF counts is wrong and gives
no sign of it. NFKC normalization here fixes it once for every lens.

Not every publisher does this — the same corpus contained a paper with **0** ligatures.
Run prep regardless; it reports the count so you know which case you are in.

## Section IDs

`A I M R D C`, used identically in file names, table columns and manifest keys.

**A is front matter** (title, authors, abstract, keywords). It is written out because an
abstract has its own measurable style, but it is **never part of an IMRDC band** — on the
test paper the abstract averaged 38.7 words per sentence against 29.7 for the body. Mixing
it into a whole-paper figure skews everything.

For the same reason **never compute a band from `body.txt`**: body = A + IMRDC.

## When detection fails

`prep.py` does not guess. If a required section (I, M, R) is not found it prints the
paper's numbered headings and exits 2:

```
STOP: required section(s) not found: R
      Numbered headings found in the body:
        1. Introduction
        2. Materials and methods
        3. Evaluating the effectiveness of EC and ORP in distinguishing
        4. Development and application of monitoring frameworks
        5. Conclusions
```

That output tells you the paper is organised thematically rather than by IMRaD. Map the
real headings onto the IDs yourself:

```bash
py -3.10 scripts/prep.py paper.pdf --slug s --out . \
  --marks "I=1. Introduction,M=2. Materials and methods,R=3. Evaluating the effectiveness,D=4. Development and application,C=5. Conclusions"
```

**Never hand-edit offsets to make it pass.** A wrong split corrupts every per-section band
downstream, silently. If a paper genuinely has no Methods-equivalent section, say so and
extract the sections it does have.

Use `--dry-run` to see the detection and section sizes without writing anything, and
`--force` to overwrite an existing folder.

## Verifying prep did its job

Three cheap checks before moving to the lenses:

1. **Ligature count reported.** If it is non-zero, the normalization mattered — record the
   number in the manifest.
2. **Section sizes are plausible.** A Methods of 300 characters means detection landed on
   a cross-reference, not a heading.
3. **`manifest.json` has a `measured.sections` row per section.** If `profile NOT run`
   appeared, `quant_check.py` is missing or erroring, and every band will have to be
   measured by hand — fix that before continuing.

## Reuse by other skills

`body.txt` is not private to this skill. `extraction-knowledge` reads PDFs directly and
meets the same ligature problem, and its quality bar is verbatim quotation — it benefits
most. Point it at `body.txt` rather than the PDF.
