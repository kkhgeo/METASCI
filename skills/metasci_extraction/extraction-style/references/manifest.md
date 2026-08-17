# manifest.json — the corpus entry point

One small JSON per paper. Downstream reads **this**, not the 100 KB markdown files, to
answer two questions:

> Which band applies to a Methods paragraph?
> What must this draft never do?

`prep.py` writes it with every deterministic field filled and every judgment field `null`.
The lenses fill the nulls. **A manifest still containing `null` is an incomplete
extraction** — that is the completeness check, and it is deliberately cheap to run.

## Schema

```jsonc
{
  "schema": "metasci-corpus/manifest",
  "schema_version": "1.0.0",
  "slug": "kim-2015-nitrate-iso",

  "paper": {                       // ← fill from sections/A.txt
    "title":  "...",
    "authors": "Kim, K.-H., Yun, S.-T., Mayer, B., Lee, J.-H., Kim, T.-S., Kim, H.-K.",
    "journal": "Agriculture, Ecosystems and Environment",
    "year": 2015,
    "doi": "10.1016/j.agee.2014.10.014"
  },

  "prep": { /* written by prep.py — do not edit */ },

  "files": { /* written by prep.py — fixed names, path-constructable */ },

  "measured": {
    "source": "sections/*.txt",
    "warning": "Never use body.txt for a band: it includes front matter (A).",
    "sections": {
      "I": { "tokens": 1366, "sentences": 44,
             "avg_sent_len": 31.0, "hedges_per_1k": 8.1, "passive_per_1k": 5.9 }
      // ... one row per section present
    }
  },

  "frames": {                      // ← fill from logic.md §E
    "total": 220,
    "recurrent": 3,
    "singleton": 190,
    "uncategorized_rate": 0.30,
    "rule": "Imitate the frame TYPE and its position; never copy the anchor WORDING."
  },

  "vocabulary": {                  // ← fill from style-vocab.md
    "reporting_verbs": {
      "show*":       { "total": 23, "by_section": {"I":3,"M":2,"R":16,"C":2},
                       "reserved_for": "display items only" },
      "indicat*":    { "total": 15, "by_section": {"I":1,"M":0,"R":12,"C":2},
                       "reserved_for": "the author's own inference" },
      "report*":     { "total": 10, "by_section": {"I":4,"M":2,"R":4,"C":0},
                       "reserved_for": "prior literature only" }
    },
    "modality_workhorse": "can be (21) — not may (9)",
    "connectives": { "therefore": 10, "thus": 10, "however": 11,
                     "note": "however = 0 in M" }
  },

  "red_flags": [                   // ← fill from card.md
    "attitude markers (interestingly / surprisingly / unfortunately) — 0 in this paper",
    "roadmap sentence — absent",
    "standalone Limitations section — absent",
    "future-work close — absent",
    "\"Figure 3\" spelled out — this author writes \"Fig. 3\"",
    "bulleted lists for partitions — uses inline (1)…(2)…and (3)",
    "however inside Methods"
  ],

  "distinctive_moves": [           // ← 1-3, from card.md
    "coins its own term ('hereafter referred to as sample uncertainty'), then uses it 23×",
    "re-argues the method inside the Results (5 paragraphs)",
    "closes paragraphs on a decision, not on a finding"
  ],

  "provenance": {                  // ← fill last
    "extracted_at": "2026-08-17",
    "quant_check_version": "canonical (no __version__ string)",
    "verbatim_errors_caught": 5,
    "notes": "counted against sections/*.txt; 172 ligatures folded by prep"
  }
}
```

## Field notes

**`measured.sections`** is the single most-read field. It exists so a consumer can pick the
right band without opening anything else. Never add a whole-paper row here: a whole-paper
figure invites exactly the mistake this design prevents — judging a Methods paragraph
against a number that mixes four genres. On the test paper, passive ran 21.3/1k in Methods
and 5.9/1k in the Introduction; a draft measured against the 13.0/1k average would be told
to activize prose already below its own author's norm.

**`frames.rule`** is a constant string, repeated in every manifest on purpose. It is the
finding a consumer is most likely to forget: frame *types* recur, frame *wordings* do not.

**`vocabulary.reporting_verbs`** carries `reserved_for` because the totals alone are
useless. "show* 23" says nothing; "show* 23, display items only" is an instruction.

**`red_flags`** are absences. Write them as things to remove from a draft, not as
descriptions of the paper. Each one should be checkable by search.

**`provenance.verbatim_errors_caught`** records how many quoted sentences the anchor gate
disproved. It is not a confession — it is the evidence the gate ran. A `0` here on a long
paper is more suspicious than a `5`.

## Filling order

Fill after each lens rather than all at the end, so a partial run still leaves a truthful
file:

| after | fill |
|-------|------|
| Stage 0 | (nothing — prep did it) |
| Lens A | `frames`, `paper` |
| Lens W | `vocabulary` |
| Lens C | `red_flags`, `distinctive_moves` |
| Stage 4 | `provenance`, then `<corpus>/index.md` |

## Checking

```bash
py -3.10 -c "import json,sys; m=json.load(open(sys.argv[1],encoding='utf-8')); \
def walk(o,p=''):
    ...
" manifest.json
```

Simplest reliable check — search the file for the token `null`:

```bash
grep -n "null" papers/<slug>/manifest.json
```

Any hit is an unfinished field. If a field genuinely does not apply to this paper (no
Conclusions section, no distinctive move worth recording), write an explicit empty value
(`[]`, `""`) with a one-line note rather than leaving `null`. **`null` means "not done";
empty means "checked, nothing there".** Those are different states and the difference
matters six months later.
