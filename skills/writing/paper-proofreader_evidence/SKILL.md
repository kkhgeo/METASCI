---
name: paper-proofreader_evidence
description: >
  Evidence-based academic paper proofreading workflow. Searches Google Scholar
  and Semantic Scholar to collect real writing patterns from comparable papers
  in the same domain/journal, builds an Evidence Bank, and uses it alongside
  the writing-manual to provide grounded corrections. Supports 4 review modes
  (full draft / section / paragraph / sentence) with free navigation. Paragraph
  review includes mandatory intent confirmation before correction.

  Trigger phrases: "증거기반 교정", "증거기반 검토", "evidence-based proofreading",
  "evidence proofreading", "근거기반 교정", "논문 교정 evidence",
  "Evidence Bank으로 교정", "evidence-based review"
---

# Evidence-Based Paper Proofreader

## Environment

- **Runtime:** Claude Code CLI (terminal)
- **Output:** Markdown (headers, bold, tables, code blocks, horizontal rules)
- **User input:** Natural language — no numbered menus, speak to approve/direct
- **Translation:** Korean translation always shown below English original
- **Web search:** Used for Evidence Gathering (Agent E), Spot Search (Agent S),
  and Reference Verification (Agent B)

## File Locations

All paths are relative to this skill directory.

```
paper-proofreader_evidence/
├── SKILL.md                          ← You are here
├── writing-manual/
│   ├── INDEX.md                      ← Routing table
│   ├── sections/
│   │   ├── 01_abstract.md
│   │   ├── 02_introduction.md
│   │   ├── 03_methods.md
│   │   ├── 04_results.md
│   │   ├── 05_results_discussion.md
│   │   ├── 06_discussion.md
│   │   └── 07_conclusion.md
│   └── cross_section/
│       ├── cohesion_flow.md
│       ├── sentence_craft.md
│       ├── stance_hedging.md
│       └── advanced_nns_issues.md
├── references/
│   ├── search_strategy.md            ← Query templates, API endpoints
│   └── evidence_bank_schema.md       ← Evidence Bank structure
└── agents/
    ├── agent_d.md                    ← Mode 1: Full Draft review
    ├── agent_p.md                    ← Mode 2: Section review
    ├── agent_pg.md                   ← Mode 3: Paragraph review (with intent)
    ├── agent_a1.md                   ← Mode 4: Sentence logic
    ├── agent_a2.md                   ← Mode 4: Sentence style
    ├── agent_b.md                    ← Reference verification
    ├── agent_e.md                    ← Evidence Collector
    └── agent_s.md                    ← Spot Search (on-demand)
```

Load files using the Read tool with the skill directory as base path.

---

## Output Format Rules

### Bilingual display

All original text and translations use inline code blocks with language labels:

**Paragraph layer:**

**[EN]** `[full paragraph text]`

**[KR]** `[Korean translation]`

**Sentence layer:**

**[EN]** `[current sentence]`

**[KR]** `[Korean translation]`

**Previous context (no label, italic, concise):**

*prev:* [previous sentence summary or full text]

### Plain explanation rule (mandatory)

Below each Agent result table, if ISSUE exists, provide a plain Korean explanation:

#### Agent A1 — Logic & flow
| Item | Result |
(table)
`[Plain Korean explanation in reader-experience framing]`

Rules for plain explanations:
- Never use technical jargon (no "Given-New", "stress position", "nominalization")
- Frame as "When a reader reads this, they would..." or "Reading this sentence..."
- Compare original and suggestion specifically

If ISSUE is NONE, omit the plain explanation.

### Suggestion display

If SUGGEST exists, show the full revised sentence below the plain explanation:

**Suggestion:** `[full revised sentence]`

If A1 and A2 each propose different suggestions, show both:

**Suggestion (A1):** `[A1's revision]`
**Suggestion (A2):** `[A2's revision]`

### Evidence reference display (new)

When a suggestion is informed by the Evidence Bank:

**Suggestion:** `[revised text]`
**Evidence:** `[Author (Year), Journal — brief context of how this pattern was used]`

### Agent B — shown after paragraph completion (batch)

Agent B runs after all sentences in a paragraph are reviewed.
Output as a table:

#### Agent B — Reference verification

| REF | STATUS | TITLE | DOI |
|---|---|---|---|
| Author (Year) | FOUND / NOT_FOUND | [title] | [DOI or —] |

NOT_FOUND items get a warning:
**[REF unverified]** `[citation] — manual verification required`

---

## Agent Configuration

| Agent | Role | Reference files | Execution |
|---|---|---|---|
| **Agent D** | Full draft: cross-section coherence, structure | All section files + `cohesion_flow.md` | Mode 1, once |
| **Agent E** | Evidence collection: search + pattern extraction | `references/search_strategy.md` + `references/evidence_bank_schema.md` | Step 0.5, once per section |
| **Agent P** | Section overview: paragraph arrangement, argument arc | `sections/[section].md` + `cohesion_flow.md` + `stance_hedging.md` + Evidence Bank | Mode 2, once per section |
| **Agent PG** | Paragraph analysis with confirmed intent | `sections/[section].md` + `cohesion_flow.md` + Evidence Bank + confirmed intent | Mode 3, once per paragraph |
| **Agent A1** | Sentence logic: argument structure, Given-New | `sections/[section].md` + `cohesion_flow.md` + Evidence Bank + confirmed intent | Mode 4, per sentence |
| **Agent A2** | Sentence style: craft, hedging, register | `sentence_craft.md` + `advanced_nns_issues.md` + `stance_hedging.md` + Evidence Bank + confirmed intent | Mode 4, per sentence |
| **Agent B** | Reference existence verification via web search | Web search | After paragraph completion |
| **Agent S** | Spot search for additional evidence | `references/search_strategy.md` + Evidence Bank | On-demand (CONFIDENCE=LOW or user request) |

All agent prompt templates are in `agents/`. Load the relevant template,
fill in the variables, and pass to the sub-agent tool.

---

## Step 0: Initialization

### 0a. Load writing-manual

Read `writing-manual/INDEX.md` with the Read tool.
Check the routing table for which files to load based on the section.

### 0b. Interpret user's description

The user describes their situation in natural language. Extract:

| Information | Example | If not provided |
|---|---|---|
| Review scope | "look at the whole draft" / "just this paragraph" | Ask once, gently |
| Target journal | "for Geoderma" | Skip or ask if Evidence would help |
| Topic / keywords | "about SOC dynamics under freeze-thaw" | Extract from provided text |
| Current stage | "first draft" / "R2 revision" / "final check" | Proceed without |
| Section name | "this is the Discussion" | Infer from content |
| Special requests | "reviewer pointed out this sentence" | Proceed without |

**Core principle:** Ask only what is missing AND would meaningfully improve
the review. If the user says "just do it," proceed with what is available.

### 0c. Parse input

Accept any input format:
- Folder path → `ls` to list files, identify sections
- Single file → read and identify section
- Pasted text → accept as-is
- Multiple files → combine

### 0d. Evidence Gathering decision

- Journal + keywords available → run Evidence Gathering (Step 0.5)
- Only keywords → run with broader search
- Nothing → offer to extract keywords from text, or skip
- User says "skip evidence" → proceed with writing-manual only

### 0e. State tracking

Track internally:

```
session = {
    mode: "draft" | "section" | "paragraph" | "sentence",
    current_section: str,
    current_para_idx: int,
    current_sent_idx: int,
    previous_paragraph: str,
    previous_sentence: str,
    total_paras: int,
    corrections: [{level, idx, original, revised}],
    skipped: [idx],
    confirmed_intents: {para_idx: str},
    evidence_bank: {...},
    spot_search_cache: {...},
    ref_verification_cache: {citation: {status, title, doi}}
}
```

---

## Step 0.5: Evidence Gathering

**Trigger:** Once per section, before review begins.

Load `agents/agent_e.md` for the full Agent E prompt template.
Load `references/search_strategy.md` for query construction rules.
Load `references/evidence_bank_schema.md` for Evidence Bank structure.

### Process

1. Agent E generates 3-5 search queries based on topic, journal, section
2. Execute web searches (Google Scholar, Semantic Scholar API)
3. Collect accessible text (abstracts, snippets, open access full text)
4. Extract patterns → build Evidence Bank
5. Present summary to user

### User output

```markdown
---
## Evidence Gathering — [Section]

### [N] reference papers collected

| # | Paper | Journal | Year | Access |
|---|---|---|---|---|
| 1 | [title] | [journal] | [year] | Full / Abstract / Snippet |

### Key findings
- **Structure:** [common section pattern]
- **Expressions:** [2-3 notable domain patterns]
- **Hedging level:** [typical calibration for this domain]

---
*"proceed" / "search more" / "add specific paper: [DOI or title]" / "show full Evidence Bank" / "skip evidence"*
```

### Minimum quality

- At least 3 abstracts to build Evidence Bank
- Ideal: 1+ full text + 3+ abstracts
- If minimum not met, notify user and offer to broaden search or skip

---

## Review Modes

### Mode 1: Full Draft Review

**User says things like:** "I finished the draft, check the whole thing" /
"Does this paper flow?"

1. Load `agents/agent_d.md`
2. Run Agent D with full draft text + Evidence Bank (if available)
3. Present structure map, cross-section issues, priority sections
4. User chooses: go to specific section (Mode 2), paragraph (Mode 3),
   or another action

```markdown
## Full Draft Review

### Structure map
[Section] → [Section] → ... (with connection quality)

### Cross-section issues
- [issue 1]
- [issue 2]

### Priority sections
1. [Section] — [reason]
2. [Section] — [reason]

---
*"go to [section]" / "section review for [X]" / "paragraph review for [X]" / "done"*
```

---

### Mode 2: Section Review

**User says things like:** "I rewrote the Discussion" / "Check the Methods"

1. Run Evidence Gathering if not yet done for this section
2. Load `agents/agent_p.md`
3. Run Agent P with section text + Evidence Bank
4. Present paragraph structure analysis + Evidence comparison
5. User chooses: drill into paragraph (Mode 3), sentence (Mode 4),
   move to another section, or end

Output follows existing Agent P format with added EVIDENCE_COMPARE field.

---

### Mode 3: Paragraph Review ★ with Intent Confirmation ★

**User says things like:** "This paragraph feels weak" /
"Look at paragraph 3"

This mode has a **mandatory intent confirmation step**.

#### Step 3a: Display paragraph

```markdown
### Paragraph [N]

**[EN]** `[full paragraph text]`

**[KR]** `[Korean translation]`
```

#### Step 3b: Intent Confirmation ★ CRITICAL ★

Before running ANY analysis agent, formulate understanding and ask:

```markdown
### Intent check

I read this paragraph as:

**Core message:** [1-2 sentence summary of what the paragraph communicates]

**Role in section:** [function — e.g., "interprets SOC mineralization results
by proposing aggregate disruption as the primary mechanism"]

**Key claim:** [central assertion — e.g., "physical disruption of aggregates,
not temperature-driven microbial activity, explains the observed SOC increase"]

Is this what you intended? If the emphasis is different, tell me
what you're actually trying to say.
```

**User responses:**

| User says | Action |
|---|---|
| "Yes" / "That's right" | Store confirmed intent → Step 3c |
| "Not exactly. I'm trying to say [X]" | Store corrected intent → Step 3c |
| "The key point is [X], not [Y]" | Update intent with emphasis → Step 3c |
| "I'm not sure what I want to say" | Help articulate: "Based on your data and the preceding paragraph, would the point be [A] or [B]?" |

Store confirmed intent in `session.confirmed_intents[para_idx]`.

#### Step 3c: Agent PG — Paragraph analysis

Load `agents/agent_pg.md`. Pass confirmed intent + paragraph + context + Evidence Bank.

```markdown
#### Agent PG — Paragraph structure

| Item | Result |
|---|---|
| **INTENT_DELIVERY** | [YES / PARTIALLY / NO + explanation] |
| **TOPIC_SENTENCE** | [clear / buried / missing / misaligned with intent] |
| **STRUCTURE** | [internal argument flow] |
| **COHESION** | [Given-New chain within paragraph] |
| **CONTEXT_FIT** | [connection to surrounding paragraphs] |
| **ISSUES** | [problems, or NONE] |

`[Plain Korean explanation]`

**Restructuring suggestion:** [if any]
**Evidence:** `[comparable pattern from Evidence Bank]`

---
*"sentence review" / "restructure this" / "next paragraph" / "skip" / "back to section"*
```

---

### Mode 4: Sentence Review

**User says things like:** "Reviewer pointed out this sentence" /
"Check sentences in paragraph 3" / "Go through each sentence"

#### Quick intent check (if entering Mode 4 without Mode 3)

If the user jumps directly to sentence review without going through
Mode 3 for this paragraph, perform a lightweight intent check:

```markdown
Before reviewing sentences — this paragraph appears to argue that [X].
Is that right, or should I know something different?
```

User confirms or corrects → store intent → proceed.

#### Sentence processing

1. Split paragraph into sentences (same rules as existing skill):
   - Split on `. ` `? ` `! `
   - Exceptions: `et al.` `Fig.` `vs.` `e.g.` `i.e.` `cf.` `ca.`
   - Do not split inside parentheses

2. Display sentence + translation

3. Load `agents/agent_a1.md` and `agents/agent_a2.md`
4. Run Agent A1 and A2 in **parallel** (two sub-agent calls in one response)
5. Both agents receive: confirmed intent + Evidence Bank + writing-manual rules

```markdown
### Paragraph [N] — Sentence [M/total]
---

*prev:* [previous sentence]

**[EN]** `[current sentence]`

**[KR]** `[Korean translation]`

---

#### Agent A1 — Logic & flow

| Item | Result |
|---|---|
| **ROLE** | [sentence role in paragraph] |
| **GIVEN_NEW** | [Given-New assessment] |
| **INTENT_ALIGNMENT** | [serves paragraph intent? YES / PARTIAL / NO] |
| **ISSUE** | [problem, or NONE] |
| **CONFIDENCE** | [HIGH / MEDIUM / LOW] |

`[Plain Korean explanation if ISSUE exists]`

**Suggestion (A1):** `[revision, if any]`
**Evidence:** `[Evidence Bank pattern, if used]`

#### Agent A2 — Style & language

| Item | Result |
|---|---|
| **STYLE** | [style assessment] |
| **HEDGE_CALIBRATION** | [vs domain: under-hedged / calibrated / over-hedged] |
| **ISSUE** | [problem, or NONE] |
| **CONFIDENCE** | [HIGH / MEDIUM / LOW] |

`[Plain Korean explanation if ISSUE exists]`

**Suggestion (A2):** `[revision, if any]`
**Evidence:** `[Evidence Bank pattern, if used]`

---
*"next" / "apply" / "apply A1" / "apply A2" / "skip" /
"search for better phrasing" / "how do other papers say this?" /
"A1 detail" / "A2 detail" / "back to paragraph view"*
```

#### Agent S — Spot Search (conditional)

**Auto-trigger:** Either Agent A1 or A2 returns CONFIDENCE: LOW
**Manual trigger:** User says "search for better phrasing" /
"how do other papers say this?" / "이거 검색해봐"

Load `agents/agent_s.md`. Execute focused web search for the specific
sentence problem. Present comparable expressions from published papers.

```markdown
#### Agent S — Spot search

**Query:** `[search query used]`
**Found:** [N] comparable expressions

**Reference expressions:**
1. `[sentence from Paper A]` — [Author (Year), Journal]
2. `[sentence from Paper B]` — [Author (Year), Journal]

**Reinforced suggestion:** `[improved revision based on evidence]`

`[Plain Korean explanation of why this works better]`

---
*"apply this" / "apply A1" / "apply A2" / "next" / "search more"*
```

---

## Navigation

The user can move between modes at any time:

| User says | Action |
|---|---|
| "Look at the whole draft" | → Mode 1 |
| "Go back to section view" | → Mode 2 |
| "Look at this paragraph as a whole" | → Mode 3 (with Intent Confirmation) |
| "Check this sentence" | → Mode 4 |
| "Go up one level" | sentence→paragraph, paragraph→section, section→draft |
| "Go down one level" | draft→section, section→paragraph, paragraph→sentence |
| "Next" / "Previous" | Next/previous unit in current mode |
| "Jump to paragraph [N]" | Direct navigation |
| "Switch to [section name]" | Change section, re-run Evidence if needed |
| "Evidence Bank 보여줘" | Display full Evidence Bank |
| "Evidence 없이 진행" | Disable Evidence Bank, manual-only mode |
| "Add this paper: [DOI/title]" | Add specific paper to Evidence Bank |
| "오늘 여기까지" / "done" | End session with summary |

### Adding input mid-session

The user can provide additional files/text at any point:

```
User: "Here's the Introduction too" + [file]

Skill: Introduction added. Current inventory:
       - Introduction (8 paragraphs)
       - Discussion (9 paragraphs, review in progress)

       Full Draft review is now available.
       Switch to full review, or continue with Discussion?
```

---

## Paragraph Completion

When all sentences in a paragraph are reviewed:

```markdown
---
### Paragraph [N] review complete
- Revised: [X]
- Approved: [Y]
- Skipped: [Z]
---
```

### Agent B — Reference verification (batch)

After paragraph completion, collect all citations in the paragraph.
Skip citations already verified in this session (use cache).
Load `agents/agent_b.md` and run web search sub-agents in parallel.

Output format: see Agent B section in Output Format Rules above.

### Table/Figure handling

- Table content itself: not reviewed (skip)
- Table/Figure captions: reviewed as sentences
- Body text after tables/figures: reviewed normally

---

## Section Completion / Session Summary

When all paragraphs in a section are done, or user ends session:

```markdown
---
## Review session summary

| Item | Value |
|---|---|
| Modes used | [list] |
| Sections reviewed | [N] |
| Paragraphs reviewed | [N] |
| Sentences reviewed | [N] |
| Approved (no change) | [N] |
| Revisions applied | [N] |
| Skipped | [N] |
| Unverified references | [N] |
| Evidence-informed revisions | [N] |
| Agent S spot searches | [N] |
| Evidence Bank papers | [N] |
| Intent confirmations | [N] |

### Revision history

| # | Level | Original | Revised |
|---|---|---|---|
| 1 | [para/sent] | [original] | [revised] |

---
```

---

## Evidence Bank Management

### Section change

When moving to a different section:
- Paper list is retained
- Patterns are re-extracted for the new section
- User is notified: "Updating Evidence Bank for [new section]"

---

## Error Handling

- Agent sub-agent failure: retry once → "**[Agent response unavailable — manual review required]**"
- Web search failure: "**[Search unavailable — manual verification required]**"
- Evidence Gathering returns <3 papers: notify user, offer to broaden or skip
- File encoding error: try UTF-8 → EUC-KR

---

## Backward Compatibility

If the user says "skip evidence" or provides no metadata for Evidence
Gathering, the skill operates in manual-only mode — identical to the
original `paper-proofreader` behavior, except:
- 4 review modes with free navigation remain available
- Intent Confirmation still runs in Mode 3 (needs no Evidence Bank)
