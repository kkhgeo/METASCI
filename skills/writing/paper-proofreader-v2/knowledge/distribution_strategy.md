# Distribution Strategy — Knowledge Allocation to Reviewers

## Purpose

Define how knowledge files are divided among reviewer agents (R1–R5)
so each reviewer brings a different perspective to the same review task.

---

## Reviewer Roles

| Reviewer | Knowledge allocation | Perspective |
|---|---|---|
| **R1** | writing-manual + Knowledge Group A | Domain expert A |
| **R2** | writing-manual + Knowledge Group B | Domain expert B |
| **R3** | writing-manual only | Rule-based judge |
| **R4** | None (no references) | Generic academic-writing reviewer (LLM judgment) |
| **R5** | None (no references) — **cross-disciplinary scientific reader persona** | PhD-level scientist from an adjacent field. No specialist knowledge of this subfield. Tests whether the argument is portable: are warrants explicit, are subfield premises scaffolded rather than assumed, does the evidence-claim chain survive an outside-the-subfield read? |

All five reviewers receive **identical review instructions**.
The only variables are `{allocated_knowledge}` and `{persona_directive}`
in the prompt. R4 and R5 receive the same (empty) knowledge but different
persona directives — R4 evaluates as a generic reviewer, R5 as an
expert scientist from outside this subfield.

---

## Grouping Algorithm

### Step 1: Collect loadable files

From `knowledge_index[]`, select files that matched the current
context keywords (see `input_handler.md` matching rules).

### Step 2: Classify by knowledge type

```
content_files = files where type in [
    "extraction_knowledge", "pdf", "freeform_md", "html"
]
writing_files = files where type in [
    "extraction_logic", "extraction_vocab"
]
```

### Step 3: Distribute

**Case A — Enough files for 2 groups (4+ content files):**

```
Group A = content_files[0:half] + writing_files[0:half]
Group B = content_files[half:] + writing_files[half:]

R1 → writing-manual + Group A
R2 → writing-manual + Group B
R3 → writing-manual only
R4 → nothing                  (generic academic-writing reviewer persona)
R5 → nothing                  (cross-disciplinary scientific reader persona)

Total reviewers: 5
```

**Case B — Small collection (2-3 content files):**

```
Group A = all content_files
Group B = all writing_files

R1 → writing-manual + Group A (content knowledge)
R2 → writing-manual + Group B (writing patterns)
R3 → writing-manual only
R4 → nothing                  (generic academic-writing reviewer persona)
R5 → nothing                  (cross-disciplinary scientific reader persona)

Total reviewers: 5
```

**Case C — Minimal (0-1 files):**

```
R1 → writing-manual + whatever is available
R2 → writing-manual only (becomes second baseline)
R3 → (skip — merge into R2)
R4 → nothing                  (generic academic-writing reviewer persona)
R5 → nothing                  (cross-disciplinary scientific reader persona)

Total reviewers: 4 (R1, R2, R4, R5)
```

**Case D — No knowledge files at all:**

```
R1 → writing-manual only
R2 → (skip)
R3 → (skip)
R4 → nothing

Total reviewers: 2 (R1, R4)
```

### Step 4: Balance check

- No reviewer should have more than 5 files
- If a group exceeds 5, keep the top-5 by keyword match score
- Each group should have at least 1 file (otherwise merge groups)

---

## Distribution Report

After distribution, show user:

```markdown
---
### Knowledge Distribution

| Reviewer | Files | Focus |
|---|---|---|
| R1 | Benz2024, Long2025, Kim2024_logic | Domain + structure |
| R2 | Bhattarai2023, Wu2024, Kim2024_vocab | Domain + terminology |
| R3 | writing-manual only | Rule baseline |
| R4 | (none) | LLM judgment |

Total: [N] knowledge files across [M] reviewers

---
*"이대로 진행" / "분배 변경" / "파일 추가: [경로]"*
```

---

## User Override

The user can manually adjust distribution:

| User says | Action |
|---|---|
| `"R1에 Benz2024 추가"` | Move file to R1's group |
| `"R2에서 Kim2024 빼"` | Remove file from R2's group |
| `"분배 다시 해줘"` | Re-run distribution algorithm |
| `"파일 추가: [path]"` | Add to index, parse, re-distribute |
| `"리뷰어 3명만"` | Drop R3 or R4 (user's choice) |
| `"리뷰어 2명만"` | Keep R1 + R4 only |

---

## Mode-Specific Distribution Notes

### Mode 1: Paper
- Each reviewer gets the full draft + their knowledge allocation
- If the draft is very long, each reviewer may get a summary
  instead of full text (see `harness/context_loading.md`)

### Mode 2: Section
- Each reviewer gets the full section text + their knowledge
- Knowledge files re-matched to section keywords if section changes

### Mode 3: Paragraph
- Each reviewer gets: paragraph + surrounding context + confirmed intent
- Knowledge narrowed: only entries matching paragraph citations/keywords
- If a reviewer's group has no matching entries for this paragraph,
  they still review with their base allocation (writing-manual or none)
