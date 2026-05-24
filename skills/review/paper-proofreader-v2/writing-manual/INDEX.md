# Writing Manual — Agent Index

## Purpose
This manual guides an AI proofreading agent to evaluate and improve **advanced scientific English writing** at the paragraph and sentence level. It is calibrated for expert-level authors, not beginners. Do not flag basic grammar unless it causes genuine ambiguity.

---

## How to Use This Manual

### Step 1 — Identify the section being reviewed
| Section keyword | Load these files |
|---|---|
| Abstract | `sections/01_abstract.md` + `cross_section/stance_hedging.md` + `cross_section/quantitative_integrity.md` |
| Introduction | `sections/02_introduction.md` + `cross_section/stance_hedging.md` + `cross_section/cohesion_flow.md` |
| Methods | `sections/03_methods.md` + `cross_section/sentence_craft.md` + `cross_section/quantitative_integrity.md` |
| Results | `sections/04_results.md` + `cross_section/cohesion_flow.md` + `cross_section/quantitative_integrity.md` |
| Results & Discussion (combined) | `sections/05_results_discussion.md` + `cross_section/stance_hedging.md` + `cross_section/quantitative_integrity.md` |
| Discussion | `sections/06_discussion.md` + `cross_section/stance_hedging.md` + `cross_section/cohesion_flow.md` |
| Conclusion | `sections/07_conclusion.md` + `cross_section/stance_hedging.md` |

### Step 2 — Apply cross-section principles always
These files apply to **every section** regardless:
- `cross_section/cohesion_flow.md` — Given-New, thematic progression, paragraph architecture, **Banana Rule (terminological consistency)**, **acronym discipline**
- `cross_section/sentence_craft.md` — Nominalization, voice, subject-verb, tense
- `cross_section/stance_hedging.md` — Hedges, boosters, self-mention, engagement markers
- `cross_section/clutter_redundancy.md` — Dead-weight phrases, intro-phrase deletion, lexical redundancy (Sainani-style clutter audit)

### Step 3 — Check for advanced non-native writer issues
- `cross_section/advanced_nns_issues.md` — Collocation, register, article use, discourse-level errors

### Step 4 — Apply integrity audit (Mode 1 always; Mode 2/3 when numeric/citation content present)
- `cross_section/quantitative_integrity.md` — N consistency, percentage math, sig-fig drift, secondary-source flagging, reporting-standard compliance. Also drives Agent B's expanded behavior (numeric cross-check + Telephone Game audit)

---

## Evaluation Principles for the Agent

1. **Do not over-flag.** Expert writing tolerates stylistic variation. Flag only issues that genuinely impede clarity, logic, or reader comprehension.
2. **Always diagnose before prescribing.** Identify *why* a sentence is problematic before suggesting a fix.
3. **Cite the principle.** When flagging an issue, name the principle it violates (e.g., "Given-New violation," "hedge under-calibration," "topic-verb gap").
4. **Respect disciplinary conventions.** Passive voice in Methods is correct. Past tense for specific findings is correct. Do not "correct" these.
5. **Scale critique to significance.** Distinguish between: (a) critical problems that weaken the argument, (b) clarity issues that slow the reader, and (c) minor polish items.

---

## File Map

```
writing-manual/
├── INDEX.md                          ← You are here
├── sections/
│   ├── 01_abstract.md
│   ├── 02_introduction.md
│   ├── 03_methods.md
│   ├── 04_results.md
│   ├── 05_results_discussion.md
│   ├── 06_discussion.md
│   └── 07_conclusion.md
└── cross_section/
    ├── cohesion_flow.md               (incl. Banana Rule + acronym discipline)
    ├── sentence_craft.md
    ├── stance_hedging.md
    ├── advanced_nns_issues.md
    ├── clutter_redundancy.md          (Sainani-style clutter audit)
    └── quantitative_integrity.md      (N/percentage/sig-fig/Telephone Game)
```

---

## Core Theoretical Framework (Summary)

| Framework | Source | Application |
|---|---|---|
| CARS model (3-move structure) | Swales (1990, 2004) | Introduction architecture |
| IMRaD move analysis | Kanoksilapatham, Yang & Allison, Brett, Lim | Section-specific rhetoric |
| Metadiscourse taxonomy | Hyland (2005, 2019) | Stance & reader engagement |
| Given-New / Reader Expectation | Gopen & Swan (1990) | Sentence & paragraph flow |
| Thematic Progression | Daneš (1974) | Paragraph coherence |
| Characters & Actions | Williams & Bizup (Style, 13th ed.) | Sentence clarity |
| C-C-C framework | Mensh & Kording (2017) | All scales of structure |
