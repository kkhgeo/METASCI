# METASCI

A personal Claude Code skill collection in two domains: **academic research** (paper analysis and writing) and **dialogue personas** (guided explanation and creative direction). Formerly `Meta_researcher`.

## Structure

Skills in use are organized into four packs under `skills/`:

```
skills/
├── persona/             virgil · beatrice · socrates · picasso · feynman-digest
├── metasci_writing/     meta-writing · meta-writing-mapping · meta-writing-blog · meta-mywriting-korean ·
│                        meta-rewriting · meta-proofreading · meta-proofreading-codex · meta-proofreading-evidence
├── metasci_extraction/  extraction-knowledge · extraction-logic · extraction-vocab ·
│                        metasci-style-extraction · meta-styling
└── metasci_slide/       meta-slide-content · meta-slide-design

codex-skills/            generated Codex build of the four packs above
hermes-skills/           generated Hermes build of the same
legacy-skills/           superseded — kept for reference, not loaded by the plugin
```

`skills/` is the only hand-written copy — the source Claude Code reads. The other
two are the same skills rewritten for another runtime, **generated, never
hand-edited**:

```
node tools/build-agent-skills.mjs           rebuild both
node tools/build-agent-skills.mjs --check   fail if the build output is stale
```

Edit a shared skill in `skills/`, rebuild, commit all three. Runtime differences the
build cannot express go in `agent-overrides/<profile>/`; a whole-file override may
also add a runtime-only file.

## Installing on a machine

```
git clone https://github.com/kkhgeo/METASCI ~/.metasci/METASCI
node ~/.metasci/METASCI/tools/install-skills.mjs --apply
```

Each runtime is pointed at its own build:

| runtime | gets | how |
|---|---|---|
| Claude Code | `skills/` | symlinks in `~/.claude/skills/` |
| Codex | `codex-skills/` | symlinks in `~/.codex/skills/` |
| Hermes | `hermes-skills/` | `skills.external_dirs` config |

They are symlinks, so `git pull` is the whole update path. Add `--replace` if
real directories are shadowing the links (it backs them up first).

`legacy-skills/` holds the earlier `writing/` and `research/` packs. Where a skill
was carried forward, the `metasci_*` version is the current one; see
`legacy-skills/README.md`.

The detailed sections below document the academic-research skills; the persona skills are summarized under "Persona skills".

## Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│  Research Paper (PDF)                                                    │
│       │                                                                  │
│       ├──→ extraction-knowledge → Knowledge_{topic}/                     │
│       │         (cited knowledge claims)                                 │
│       │                                                                  │
│       ├──→ extraction-logic → Logic_{topic}/                             │
│       │         (structure, argument flow, sentence frames)              │
│       │                                                                  │
│       ├──→ extraction-vocab → Vocab_{topic}/                             │
│       │         (POS word inventory, technical glossary)                  │
│       │                                                                  │
│       ├──→ meta-styling (Mode A) → Style_{topic}/                        │
│       │         (lexical style patterns)                                 │
│       │                                                                  │
│       └──→ meta-writing                                                  │
│                 (academic section writing)                                │
│                    ↓                                                      │
│              meta-review                                                 │
│                 (multi-reviewer draft improvement)                        │
│              meta-rewriting                                              │
│                 (one-shot style transfer)                                 │
│                                                                          │
│  Dataset + Literature                                                    │
│       └──→ agentic-research                                              │
│                 (autonomous data-driven scientific discovery)             │
│                                                                          │
│  Naming Convention:                                                      │
│    extraction-{target} → PDF에서 추출 (knowledge, vocab, logic)          │
│    meta-{action}       → 글쓰기/스타일 (writing, rewriting, styling,     │
│                          review)                                         │
│                                                                          │
│  Analysis Layer Separation:                                              │
│    extraction-vocab     → WHAT words are used                            │
│    meta-styling         → HOW words are used                             │
│    extraction-logic     → HOW arguments are structured                   │
│    extraction-knowledge → WHAT knowledge is cited                        │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## Installation

### As a plugin

This repository is a Claude Code plugin (`metasci`); skills load from the category folders under `skills/` (configured in `.claude-plugin/plugin.json`). Point Claude Code at a clone with `claude --plugin-dir /path/to/METASCI`.

### Manual copy

Or copy individual skill folders (e.g. `skills/persona/virgil/`) into `~/.claude/skills/` for global access, or a project's `.claude/skills/`. The trees below illustrate per-skill file layouts:

```
~/.claude/skills/                    # Global (available in all projects)
├── extraction-knowledge/
│   ├── SKILL.md
│   └── references/extraction_template.md
├── extraction-vocab/
│   ├── SKILL.md
│   └── references/extraction_template.md
├── extraction-logic/
│   ├── SKILL.md
│   └── references/extraction_template.md
├── meta-writing/
│   ├── SKILL.md
│   ├── writing.local.template.md
│   └── references/{writing_template,section_guides,citation-and-verification}.md
├── meta-rewriting/
│   ├── SKILL.md
│   └── references/{blueprint-template,journal-styles,output-formats}.md
├── meta-styling/
│   ├── SKILL.md
│   └── references/{extraction_template,revision_guide}.md
├── meta-review/
│   ├── SKILL.md
│   └── references/review_template.md
└── agentic-research/
    ├── SKILL.md
    ├── README.md
    ├── references/{world_model_spec,report_template,domain_geoscience}.md
    ├── scripts/{orchestrator,profile_dataset,init_world_model,...}.py
    └── templates/world_model_template.json
```

## Skills

### Research skills

| Skill | Description | Output |
|-------|-------------|--------|
| extraction-knowledge | Extract cited knowledge into 5 epistemological categories | `Knowledge_{topic}/` |
| extraction-vocab | Exhaustive POS word extraction + technical term glossary | `Vocab_{topic}/` |
| extraction-logic | Extract structure, argument logic, sentence frames | `Logic_{topic}/` |
| meta-writing | Multi-source academic writing with My Data/Knowledge separation | English + Korean draft |
| meta-rewriting | One-shot style transfer from reference paper to user's draft | `Rewrite_{topic}/` |
| meta-styling | Extract lexical style patterns (A) / Revise draft to match (B) | `Style_{topic}/` |
| meta-review | Multi-reviewer draft improvement using logic+vocab extractions | `Review_{timestamp}/` |
| agentic-research | Autonomous data-driven scientific discovery with iterative analysis | `Research_{topic}/` |

### Persona skills

| Skill | Description |
|-------|-------------|
| virgil | Adaptive incremental explanation — guides through a topic one segment at a time, pausing for confirmation |
| beatrice | One-shot complete explanation — the whole logical arc at once; sister skill to virgil |
| socrates | Socratic dialogue through maieutic questioning |
| picasso | Visual director — turns concepts into image-generation prompts |
| feynman-digest | Teach-Back digest — restates the prior explanation from the listener's perspective |

---

## 1. extraction-knowledge

Extract core knowledge claims from research paper PDFs, classified into 5 epistemological categories.

| Category | Description |
|----------|-------------|
| Theoretical Foundations | Core theories, conceptual frameworks, hypotheses, models |
| Empirical Precedents | Data, measurements, experimental results from prior studies |
| Methodological Heritage | Research methods, analytical techniques, measurement tools |
| Contextual Knowledge | Geographic, temporal, policy, social context |
| Critical Discourse | Academic debates, limitations, unresolved issues |

```
> "Read Chen2024.pdf and save to Knowledge_isotopes"
> "Process all PDFs in papers folder to Knowledge_environmental"
```

---

## 2. extraction-vocab

Exhaustively extract every content word from a paper, organized by section and POS.

- **POS Tables**: Verb, Noun, Adjective, Adverb — per section with frequency and context
- **Technical Glossary**: Domain, Methodological, Statistical, Chemical, Instrument, Taxonomic terms
- **Multi-word terms**: Kept as units (not split into individual words)
- **Cross-section analysis**: Frequency matrix, section-exclusive words, technical term density

```
> "Extract vocabulary from Weber2021.pdf to Vocab_geochemistry"
> "Extract technical terms from this paper"
```

---

## 3. extraction-logic

Extract three layers of analysis from academic papers:

- **Structure Mapping**: Sections → Subsections → Paragraphs hierarchy
- **Logic Extraction**: Inter-paragraph argument flow + Intra-paragraph sentence logic chains
- **Sentence Frame Extraction**: Exhaustive rhetorical templates (55+ reference frame types, open taxonomy)

```
> "Analyze logic structure of Weber2021.pdf"
> "Extract sentence frames from this paper"
```

Output: Structure tree, logic flow diagrams, sentence frame catalog with `[P#-S#]` traceability.

---

## 4. meta-writing (v0.2.0)

Multi-source academic section writing with clear separation between user's own data and prior research.

**Two-tier source model:**

| Tier | Type | Role in Paper | Citation |
|------|------|---------------|----------|
| My Data | Figures, Tables, CSV | Description & interpretation target | `(Figure 1)`, `(Table 2)` — no author citation |
| Knowledge Sources | Knowledge MD, PDF, Web | Comparison & evidence | `(Author, Year)` with source tags |

**Knowledge Sources priority:**

| Priority | Source | Tag |
|----------|--------|-----|
| 1st | Knowledge folder (markdown) | `(Author, Year)` |
| 2nd | PDF folder (direct reading) | `(Author, Year)*` |
| 3rd | Web search (gap filling) | `(Author, Year)†` |

**5-Loop process:** Source Scan → Knowledge Reading → My Data Analysis + Gap Check → Synthesis & Writing → Verification

**Project config:** `writing.local.md` for per-project paths, figure/table mapping, and writing settings.

```
> "Write Results section based on my figures and Knowledge folder"
> "이 그림 기반으로 Discussion 써줘"
> "Write Introduction from Knowledge_environmental"
```

Output: English + Korean dual output, APA 7 references (source-tagged), 4-step verification report.

---

## 5. meta-rewriting

One-shot style transfer pipeline: reverse-engineer writing style from a reference paper, generate a Style Blueprint, then apply it to the user's draft in a single session.

- **Style Blueprint**: 6-dimension analysis (Tone, Sentence Architecture, Logical Flow, Transitions, Vocabulary, Citation Style)
- **Gap Analysis**: Score each dimension 1-10, identify weaknesses
- **Two modes**: [A] Sentence-level feedback / [B] Full rewrite

```
> "이 논문처럼 써줘"
> "Nature Geoscience 스타일로 맞춰줘"
> "Rewrite my draft in the style of this paper"
```

Output: `Rewrite_{topic}/` folder with blueprint, gap analysis, and rewritten draft.

---

## 6. meta-styling

Two-mode skill for analyzing and applying academic writing styles.

- **Mode A (Extraction)**: Extract sentence patterns, vocabulary, transitions, hedging, quantitative expressions, and citation patterns per IMRaD section → Save to `Style_{topic}/`
- **Mode B (Revision)**: Compare user draft against extracted data bank → Revise to match target style

```
> "Extract style from Weber2021.pdf to Style_geochemistry"
> "Revise my Introduction to match Style_geochemistry"
```

---

## 7. meta-review

Multi-reviewer draft improvement using pre-extracted logic and vocabulary analysis files.

- **Per-paper Reviewers**: One subagent per reference paper, running in parallel
- **Four Academic Principles**: Argument Architecture, Prose Rhythm, Cohesion & Coherence, Academic Register
- **Three Intensity Levels**: Light (flag only) / Standard (flag + rewrites) / Deep (full rewrite)
- **Three Severity Levels**: Critical / Major / Minor

```
> "Review this Introduction paragraph"
> "Deep rewrite this Methods section using all reference papers"
> "Check logic flow only. Light mode."
```

Output: `Review_{timestamp}/` folder with individual reviewer reports, cross-reviewer synthesis, and improved draft with change log.

---

## 8. agentic-research

Kosmos-inspired autonomous research framework for iterative data-driven scientific discovery.

- **Multi-cycle analysis**: Hypothesis generation → code execution → literature grounding → refinement
- **World Model**: Maintains evolving JSON state of discoveries, hypotheses, and evidence
- **Literature integration**: Combines data analysis with web search for scientific context
- **Python scripts**: Dataset profiling, world model management, report generation

```
> "Analyze this dataset and find interesting patterns"
> "Run agentic research on my environmental data"
> "Iterative hypothesis testing on this CSV"
```

Output: `Research_{topic}/` folder with world model, analysis notebooks, and structured report.

---

## Typical Workflows

### Full paper analysis
```
1. extraction-knowledge  → extract cited knowledge
2. extraction-vocab      → build word inventory + technical glossary
3. extraction-logic      → map argument structure + sentence frames
4. meta-styling (Mode A) → extract stylistic patterns
```

### Academic writing
```
1. meta-writing          → draft sections using My Data + Knowledge + PDF + Web
2. meta-review           → multi-reviewer improvement using logic+vocab extractions
3. meta-styling (Mode B) → revise draft to match target journal style
4. meta-rewriting        → one-shot style transfer from reference paper
```

### Autonomous research
```
1. agentic-research      → iterative data analysis + literature grounding
2. meta-writing          → write up findings with proper citations
3. meta-review           → review and improve the manuscript
```

---

## Output Structure

```
Knowledge_{topic}/          # Cited knowledge claims
├── index.md
├── Chen2024.md
└── Kim2023.md

Logic_{topic}/              # Structure + logic + frames
├── index.md
└── Weber2021_logic.md

Vocab_{topic}/              # Word inventory + glossary
├── index.md
└── Weber2021_vocab.md

Style_{topic}/              # Style data banks
├── index.md
├── Weber2021_style.md
└── cross_section_matrix.md

Rewrite_{topic}/            # One-shot style transfer output
├── blueprint.md
├── gap_analysis.md
├── rewritten_draft.md
└── session_log.md

Review_{YYYYMMDD_HHMMSS}/  # Draft review reports
├── input.md
├── reviewer_1.md
├── reviewer_2.md
├── synthesis.md
└── improved_draft.md

Research_{topic}/           # Agentic research output
├── world_model.json
├── analysis/
└── report.md
```

---

## Version History

### v1.0.0 (Current)
- Renamed `Meta_researcher` → `METASCI`; plugin name `meta-researcher` → `metasci`
- Reorganized skills into four categories: persona, writing (incl. review/proofreading), extraction, research
- Documented persona skills (virgil, beatrice, socrates, picasso, feynman-digest)
- Slimmed feynman-digest; fixed `.claude-plugin/plugin.json` skill paths and removed the dead top-level `plugin.json`

### v0.7.0
- Added meta-rewriting skill (one-shot style transfer pipeline)
- Renamed skills for consistency: extraction-{target} + meta-{action} convention
- Updated all cross-references across skills, CLAUDE.md, and README

### v0.6.0
- Added agentic-research skill (autonomous data-driven scientific discovery)
- Upgraded meta-writing to v0.2.0: My Data/Knowledge separation, universal (non-domain-specific), writing.local.md config, citation-and-verification, Glob support

### v0.5.0
- Added meta-review skill (multi-reviewer draft improvement with four academic writing principles)

### v0.4.0
- Added extraction-logic skill (structure, argument logic, sentence frames)
- Added extraction-vocab skill (exhaustive POS extraction, technical glossary)
- Added CLAUDE.md project instructions

### v0.3.0
- Added meta-styling skill (Mode A extraction, Mode B revision)

### v0.2.1
- Added reference verification to meta-writing

### v0.2.0
- Added meta-writing skill

### v0.1.0
- Initial extraction-knowledge skill

---

## License

MIT

## Author

KKH
