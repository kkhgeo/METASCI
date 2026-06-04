# P Lens — Aggregate Style Profile

Goal: the *measured fingerprint* of the paper — the indicators that summarize how it reads.
Modeled on the journal-adapt "Style Card": describe structure and rhetorical pattern, do not
quote content. Where V gives words and L gives templates, P gives **ratios, levels, and
absences**. These are estimates from reading, not exact statistics — report them at the
granularity that is actually useful (a ratio band, a low/med/high level).

## Dimensions to capture

| dim | what to report |
|-----|----------------|
| **voice** | active vs passive balance, overall and by section (Methods often more passive). A rough % or "active-dominant" is fine. |
| **tense** | dominant tense per section (e.g. Intro present, Methods past, Results past, Discussion mixed). |
| **person** | "we"-prominent / impersonal-passive / "this study"-prominent. |
| **hedging density** | low / medium / high, and where it concentrates (usually Discussion). This is the *density* counterpart to the V lens's hedging *words*. |
| **claim strength** | tentative ("suggest/may") vs assertive ("demonstrate/show") lean. |
| **citation integration** | integral (author-prominent: "Smith (2020) showed…") vs non-integral (information-prominent: "…(Smith, 2020)") — rough ratio + any clustering habit. |
| **sentence length** | approximate average words/sentence and whether sentences run long-and-complex or short-and-direct. |
| **mathematical / quantitative density** | how much display math or in-line statistics; for many fields this is "low". |
| **display-item reference** | the *form*: "Fig." vs "Figure" vs "(Fig. 2)"; caption tense; standalone-vs-telegraphic captions; numbering style. (Caption verbs → V; caption template → L.) |
| **does NOT do** | 3-5 structurally absent patterns (no first person, no explicit roadmap, no standalone lit review, almost no equations). Absence is a strong style signal and seeds the corpus Red Flags. |
| **distinctive moves** | 1-3 notable rhetorical/structural moves specific to this paper. |

## Method

- Read enough of each section to judge the indicator; you are characterizing, not counting
  every token. If unsure between two levels, pick one and note it's approximate.
- Keep it to indicators — no word lists, no frame templates (those are V and L).

## Output (the P section of the Style Card)

```markdown
## P. Profile
| dim | value |
|-----|-------|
| voice | active __% (Methods more passive) |
| tense (Intro/Meth/Res/Disc) | present/past/past/mixed |
| person | impersonal-passive |
| hedging density | medium (concentrated in Discussion) |
| claim strength | tentative-leaning |
| citation | non-integral __% / integral __% |
| sentence length | ~__ words, complex |
| math/quant density | low |
| display-item ref | "Fig."; "(Fig. 2)"; captions past tense, telegraphic |
| does NOT do | <absent patterns> |
| distinctive moves | <1-3> |
```
