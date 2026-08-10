# Mode 2: Section — Section Review

Entered from `SKILL.md` §5 after Step 0 completes, or by drill-down from Mode 1.

**Entry:** User says "[섹션] 검토", "Discussion 교정", etc.
Or drill-down from Mode 1.

**Context loading:** Follow `harness/context_loading.md` Mode 2 rules.
- Read full section text
- Read the writing-manual files listed in the section's
  `writing-manual/INDEX.md` Step 1 routing row (section file +
  that row's cross-section files) — the routing table is the single
  source of truth for which manual files load per section
- Match knowledge_index to section keywords
- Full-read matched knowledge files (Phase 2 load if not yet loaded)

### 6a. Run Reviewers in Parallel

Launch all active reviewers in parallel (one Agent tool call each) with:
- `{mode}` = `section`
- `{target_text}` = full section text
- `{section_name}` = section name
- `{allocated_knowledge}` = per distribution (re-matched to section keywords)
- `{writing_manual_content}` = files from the INDEX.md routing row

Mode-specific focus: STRUCTURE primary (paragraph arrangement),
LOGIC + HEDGING secondary. Reviewers also produce a **whole-paragraph
candidate set** for each paragraph whose function/order/flow they question
(`agents/agent_reviewer.md` CANDIDATE GENERATION, section scope).

### 6b. Deliberation + Judge Round

Two tracks (`harness/deliberation.md`):
- **ISSUES** → classify into consensus/unique/conflict, focus on
  paragraph-level structural issues; feeds the Top-N block.
- **CANDIDATES** → run **Agent J once for the section**
  (`agents/agent_j.md`) to select the optimal rewrite for each candidate
  paragraph. Present selections per the `config/output_format.md`
  candidate-selection contract.

### 6c. Present Results

Present per the `config/output_format.md` content contract: heading
names the section and paragraph count; a standard Markdown table lists
the Top-3 paragraph issues by impact score; closing next-actions line.
User expands via `"1번"` (single issue detail) or `"다 보여줘"`
(full list).

