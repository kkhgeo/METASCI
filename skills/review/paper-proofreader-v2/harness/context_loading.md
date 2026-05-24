# Context Loading — Mode-Specific Loading Rules

## Purpose

Define what to load into context for each review mode.
Prevent context overflow by loading only what is needed now.

---

## Loading Budget per Mode

### Mode 1: Paper

**Goal:** Broad overview, not details.

| Load | Source | Why |
|---|---|---|
| Each section's first 2 sentences | Paper file(s) | Section identification |
| writing-manual/INDEX.md | Skill directory | Routing table only |
| knowledge_index (metadata only) | Init scan | Show available knowledge |

**Do NOT load:** Full section texts, writing-manual section files,
full knowledge files, cross_section manuals.

### Mode 2: Section

**Goal:** One section in depth.

| Load | Source | Why |
|---|---|---|
| Full section text | Paper file | Review target |
| writing-manual section file | `sections/[section].md` | Section-specific rules |
| `cross_section/cohesion_flow.md` | Skill directory | Structure analysis |
| `cross_section/stance_hedging.md` | Skill directory | Hedging norms |
| Knowledge files matched to section | Knowledge Bank | Reviewer knowledge |

**Do NOT load:** Other sections' text, `sentence_craft.md`,
`advanced_nns_issues.md` (those are for sentence-level).

### Mode 3: Paragraph

**Goal:** One paragraph deeply, then sentence-by-sentence.

**Paragraph phase (intent confirmation + Agent PG):**

| Load | Source | Why |
|---|---|---|
| Target paragraph + prev/next paragraph | Paper file | Context |
| Confirmed intent | User input | Anchor for analysis |
| writing-manual section file | Already loaded from Mode 2 | Reuse |
| `cross_section/cohesion_flow.md` | Already loaded | Reuse |
| Matched knowledge entries | Knowledge Bank | Paragraph-specific |

**Sentence phase (Agent R1-R4):**

| Additional load | Source | Why |
|---|---|---|
| `cross_section/sentence_craft.md` | Skill directory | Sentence rules |
| `cross_section/advanced_nns_issues.md` | Skill directory | NNS checks |
| `cross_section/stance_hedging.md` | Already loaded | Reuse |

---

## Reviewer-Specific Loading

Each reviewer gets different knowledge but the SAME:
- Writing-manual files (except R4 who gets nothing)
- Review target text
- Confirmed intent (if available)

```
R1: [writing-manual files] + [Knowledge Group A files]
R2: [writing-manual files] + [Knowledge Group B files]
R3: [writing-manual files only]
R4: [review target text + confirmed intent only]
```

See `knowledge/distribution_strategy.md` for grouping rules.

---

## Progressive Loading Sequence

```
Session start:
  1. Read writing-manual/INDEX.md
  2. Scan knowledge directories → build knowledge_index
     (header-only, ~20 lines per file)

Mode 1 entry:
  3. Read paper file(s) — section first sentences only
  4. No additional loads

Mode 2 entry:
  5. Read full section text
  6. Read section-specific writing-manual
  7. Read cross_section files (cohesion, stance)
  8. Match knowledge_index to section keywords
  9. Full-read matched knowledge files (Phase 2 load)
  10. Build Knowledge Bank for this section
  11. Distribute knowledge to reviewers

Mode 3 entry:
  12. Extract paragraph + surrounding context
  13. Read sentence-level cross_section files
  14. Narrow knowledge to paragraph-relevant entries
  15. Run intent confirmation with user

Mode transition (back up or jump):
  - Retain already-loaded files in memory
  - Only load NEW files needed for new context
  - If jumping to a different section: re-run steps 5-11
```

---

## Unloading Rules

Context is managed by the LLM's conversation window.
"Unloading" means not including content in new agent prompts.

- When moving from Mode 3 back to Mode 2:
  skip sentence-level manuals in agent prompts
- When switching sections:
  replace section text and section manual
  re-match knowledge files
- Knowledge files not matched to current context:
  keep in index but don't include in agent prompts
