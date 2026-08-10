# Mode 1: Paper — Full Draft Review

Entered from `SKILL.md` §5 after Step 0 completes. Step 0 (initialization,
knowledge distribution) has already run — do not repeat it.

**Entry:** User says "전체 초고 봐줘", "논문 전체 검토", "full draft", etc.

**Context loading:** Follow `harness/context_loading.md` Mode 1 rules.
Load the full draft text + `writing-manual/INDEX.md` routing table.

### 5a. Run Reviewers in Parallel

Launch all active reviewers (R1-R5, per the distribution case) in
parallel — one Agent tool call per reviewer, all in a single response.
Each reviewer receives the prompt from `agents/agent_reviewer.md` with:
- `{mode}` = `paper`
- `{target_text}` = the full draft (all sections, complete text)
- `{allocated_knowledge}` = per distribution plan
- `{writing_manual_content}` = INDEX.md only (not full section files)

All reviewers use mode-specific focus: STRUCTURE primary, LOGIC secondary.

### 5b. Deliberation

Collect all reviewer results. Apply `harness/deliberation.md` protocol:

1. Match issues across reviewers by location + type
2. Classify into three categories:
   - **Consensus** (2+ reviewers agree) — present first
   - **Unique finding** (1 reviewer only, with evidence) — present second
   - **Conflict** (reviewers disagree) — present last

Within each category, order by severity (HIGH > MEDIUM > LOW).
Apply `harness/confidence_routing.md` for display detail level.

### 5c. Present Priority Sections

Present per the `config/output_format.md` content contract: a short
heading, a standard Markdown table of the Top-3 priority issues
(순위 / 심각도 / 카테고리 / 한 줄 요약), and a closing next-actions
line. Top-3 by default; user expands to Top-5 / full list via
`"다 보여줘"`.

