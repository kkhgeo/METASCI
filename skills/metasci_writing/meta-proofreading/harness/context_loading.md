# Context Loading — Mode-Specific Loading Rules

## Purpose

Define what to load into context for each review mode.
Prevent context overflow by loading only what is needed now.

---

## Loading Budget per Mode

### Mode 1: Paper

**Goal:** Whole-draft structural judgment. Reviewers need the complete
argument — structure, arc, and coverage gaps cannot be judged from
summaries.

| Load | Source | Why |
|---|---|---|
| Full draft text (all sections) | Paper file(s) | Review target |
| writing-manual/INDEX.md | Skill directory | Routing table only |
| knowledge_index (metadata only) | Init scan | Show available knowledge |

**Do NOT load:** Writing-manual section files, full knowledge files,
cross_section manuals (those load in Mode 2/3).

### Mode 2: Section

**Goal:** One section in depth.

| Load | Source | Why |
|---|---|---|
| Full section text | Paper file | Review target |
| writing-manual files from the section's INDEX.md routing row | `writing-manual/INDEX.md` Step 1 table | Section file + that section's cross-section files — the routing table is the single source of truth |
| Knowledge files matched to section | Knowledge Bank | Reviewer knowledge |

**Do NOT load:** Other sections' text, cross-section files not in the
section's routing row (the remaining ones load in Mode 3).

### Mode 3: Paragraph

**Goal:** One paragraph deeply, then sentence-by-sentence.

Mode 3 runs ONE reviewer round covering both paragraph and sentence
levels (SKILL.md 7b), so everything loads at Mode 3 entry. The judge
round (Agent J, SKILL.md 7c) needs no new file loads — it reuses the
already-loaded writing-manual + paragraph context plus the in-session
candidate pool.

| Load | Source | Why |
|---|---|---|
| Target paragraph + prev/next paragraph | Paper file | Context |
| Confirmed intent | User input | Anchor for analysis |
| writing-manual section file | Already loaded from Mode 2 | Reuse |
| ALL `cross_section/` files (incl. `sentence_craft.md`, `advanced_nns_issues.md`, `clutter_redundancy.md`) | Skill directory | The single round also reviews at sentence depth |
| Matched knowledge entries | Knowledge Bank | Paragraph-specific |

---

## Reviewer-Specific Loading

Each reviewer gets different knowledge but the SAME:
- Writing-manual files (except R4/R5 who get nothing)
- Review target text
- Confirmed intent (if available)

```
R1: [writing-manual files] + [Knowledge Group A files]
R2: [writing-manual files] + [Knowledge Group B files]
R3: [writing-manual files only]
R4: [review target text + confirmed intent + R4 persona directive]
R5: [review target text + confirmed intent + R5 persona directive]
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
  3. Read paper file(s) in full
  4. No additional loads

Mode 2 entry:
  5. Read full section text
  6. Read section-specific writing-manual
  7. Read the cross_section files from the section's INDEX.md routing row
  8. Match knowledge_index to section keywords
  9. Full-read matched knowledge files (Phase 2 load)
  10. Build Knowledge Bank for this section
  11. Distribute knowledge to reviewers

Mode 3 entry:
  12. Extract paragraph + surrounding context
  13. Read all remaining cross_section files (single round covers sentence depth)
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
