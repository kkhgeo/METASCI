# Brick plan format (`plan.json`) and content bricks (`content.tsv`)

The plan is the only thing the model writes for the revision. `brickyard.py assemble`
turns it into `revision.txt`; `brickyard.py verify` re-assembles it and fails if the text
differs by one character.

## content.tsv — the content bricks

One brick per line, `C#<TAB>span`, written into the pile folder. Every span must be a
verbatim substring of `0-draft.prose.txt` (whitespace runs are collapsed before the
comparison, nothing else). `brickyard.py content --pile pile` checks it.

```text
C1	Sulfate values
C2	12
C3	40 mg/L
C4	22 mg/L (Fig. 3)
C5	Deep wells
C6	higher sulfate
C7	shallow wells
C8	pyrite oxidation controls sulfate (Kim et al., 2015)
```

How to cut:

- **Cut at the joints a frame needs.** A value, a value with its unit, an entity, a
  property, a group, a proposition. Keep a citation or display reference inside the span
  of the claim it supports (`C4`, `C8`): moving it into another span moves its support.
- **Leave the draft's own scaffolding out.** Reporting verbs, connectives, hedges that a
  frame will supply (`ranged between … and`, `This means`) stay uncut. Dropping them is
  where the corpus style replaces the draft's. A hedge or modal that carries certainty
  (`may`, `likely`) is substance: keep it inside the span, or choose a frame that carries
  the same certainty.
- **A verb inside a proposition is content** (`pyrite oxidation controls sulfate`). Only
  the framing verb around it is replaceable.
- Spans may overlap and need not cover the draft. Coverage is Gate 1's job, not the cut's.

## plan.json

```json
{
  "paragraphs": [
    {
      "function": "Finding",
      "sentences": [
        {"frame": "F001", "fill": {"VAR": ["C1"], "MIN": ["C2"], "MAX": ["C3"], "MEAN": ["C4"]}},
        {"frame": "F002", "fill": {"A": ["C5"], "X": ["C6"], "B": ["C7"], "Y": ["?:the shallow-well contrast"]}},
        {"frame": "F003", "fill": {"PATTERNS": [], "INTERPRETATION": ["C8"]},
         "pick": {"suggest(s)/indicate(s)": "suggest"}},
        {"keep": "D4"},
        {"gap": "one-line note of what the author must write here"}
      ]
    }
  ]
}
```

A paragraph may also be a bare list of sentences. `function` is a label for the report;
the script ignores it.

### Sentence kinds

| Kind | Form | Emits |
|---|---|---|
| frame | `{"frame": "F###", "fill": {...}, "pick": {...}, "inflect": {...}}` | the template with its slots filled |
| keep | `{"keep": "D#"}` | a draft sentence, unchanged, counted as *not imposed* |
| gap | `{"gap": "text"}` | `[YOU WRITE: text]` as its own sentence |
| sentence | `{"sentence": "S###"}` | a whole corpus sentence; pile `--unit sentence` only; `verify` fails it without `--own-corpus` |

### Slot fillers

`fill` maps every slot name of the template to a list of items, joined with spaces:

| Item | Meaning |
|---|---|
| `C#` | a content brick |
| `B###` | a lexical bundle from the pile |
| `g:<word>` | a glue word from the frozen list: *the a an and or but of in on at for to with by from as than that which whose its their this these those it they we our is are was were be been* and `, ; : ( )` |
| `?:<text>` | an inline `[YOU WRITE: text]` gap |
| `[]` (empty list) | omit the slot; a dangling `, .` is tidied |

Slot names are the bracket contents (`[MEAN]` → `MEAN`). A name repeated in one template
becomes `NAME`, `NAME#2`, … in order. A template `…` is the slot `REST`.

Every slot must appear in `fill`, and no other key may. An unfilled slot is an error, not
a default.

### pick and inflect

- **pick** chooses one alternative of a template choice token: `was/were`,
  `suggest(s)/indicate(s)` (→ `suggests`, `suggest`, `indicates`, `indicate`). Key = the
  token as written in the template; for the second occurrence of the same token use
  `token#2`. An unpicked choice takes the first alternative and is warned.
- **inflect** changes a template word for number agreement only:
  *is/are, was/were, has/have, does/do, this/these, that/those, its/their, it/they*, or a
  regular `-s`/`-es`/`-ies` toggle. Anything else (`assuming → presuming`) is an error:
  that would be retyping.

### What the script does on its own (`auto`, counted in the trace)

Lower-cases a capitalised function word that opens a content brick placed mid-sentence
(`The` → `the`); removes spaces before `, . ; : )`; collapses `, .` left by an omitted
slot; chooses `a`/`an` by the next letter; capitalises the first letter; adds a terminal
period when the template has none. Nothing else.

## Files the run leaves

```text
pile/form.tsv        form bricks: id kind paper section code name pos status source slots text
pile/draft.tsv       D# sentences of the draft
pile/pile.json       scope, source hashes, counts
pile/content.tsv     the model's content bricks
plan.json            the model's brick plan
revision.txt         assembled text — never edited by hand
trace.tsv            where every piece of revision.txt came from
verify.md            brickyard verify report
inventory.tsv        Gate 1 (meta-styling's preservation_inventory.py)
```

`pos` in `form.tsv` is the frame's place in its source paragraph — `initial` (S1),
`final` (last sentence), `medial`, `solo` (one-sentence paragraph), or `unknown` when the
catalog row has no `[P#-S#]`. It drives the opener and closer rules.
