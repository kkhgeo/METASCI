---
name: meta-proofreading
description: >
  Multi-reviewer academic paper proofreading with knowledge-distributed
  deliberation. 2-5 reviewers with identical instructions but different
  knowledge allocations review the same text in parallel, then deliberate
  to reach consensus. Supports 3 modes: Paper (full draft), Section,
  and Paragraph (with sentence-level review). Local knowledge files
  (extraction-knowledge, extraction-logic, extraction-vocab, PDFs,
  freeform markdown) are auto-discovered and distributed to reviewers.
  All user-facing output in Korean.
  
  Trigger phrases: "meta-proofreading", "메타 교정", "메타교정",
  "패널 교정", "리뷰어 교정", "다중 리뷰어 교정", "panel proofreading".
  Do NOT trigger on generic phrases like "논문 교정" or "proofread"
  alone — those belong to other proofreading skills.
---

# Meta-Proofreading — Multi-Reviewer Deliberation Orchestrator

## 1. Environment

- **Runtime:** Claude Code; reviewers run as parallel sub-agents
  (one **Agent tool** call per reviewer, all in a single response)
- **Output language:** All user-facing output in Korean (한국어)
- **Agent internal prompts:** English (for optimal LLM performance)
- **English original text:** Always displayed alongside Korean explanation
- **User input style:** Korean or English, free-form; see `config/navigation.md` for input mapping
- **Tools used:** Read, Glob, Grep, WebSearch, WebFetch, Agent, AskUserQuestion
- **Output:** `config/output_format.md` (v13) defines a **content
  contract, not rendering rules**. Visual layout is at the model's
  discretion within standard Markdown — never hand-draw boxes or
  horizontal rules. The contract fixes what must be present: Korean
  output with English originals, Top-3 tier discipline, unified
  severity/status labels, plain-language explanations, a next-actions
  line on every screen, and AskUserQuestion at decision points.
  Any formatting example elsewhere in this skill is illustrative —
  when in doubt, `config/output_format.md` wins.

---

## 2. File Map

```
meta-proofreading/
├── SKILL.md                              ← This file (orchestrator)
├── agents/
│   ├── agent_e.md                        ← Knowledge Bank Builder
│   ├── agent_reviewer.md                 ← Universal Reviewer Prompt Template (R1-R5)
│   └── agent_b.md                        ← Reference Verification
├── config/
│   ├── navigation.md                     ← Mode switching & user input mapping
│   ├── output_format.md                  ← Output content contract (v13, no rendering rules)
│   └── session_management.md             ← State, save/restore, error handling
├── harness/
│   ├── deliberation.md                   ← Multi-reviewer result synthesis protocol
│   ├── confidence_routing.md             ← Adaptive workflow by confidence level
│   └── context_loading.md                ← Mode-specific loading rules
├── knowledge/
│   ├── distribution_strategy.md          ← Knowledge allocation to reviewers
│   ├── input_handler.md                  ← File type detection & parsing
│   ├── knowledge_bank_schema.md          ← Unified knowledge schema
│   └── search_strategy.md               ← Web search for knowledge supplementation
└── writing-manual/
    ├── INDEX.md                          ← Manual routing table
    ├── sections/                         ← Per-section rules (01-07)
    └── cross_section/                    ← Cross-cutting principles
```

---

## 3. Agent Configuration

| Agent | File | Instances | Role |
|---|---|---|---|
| **Agent E** | `agents/agent_e.md` | 1 | Knowledge discovery, parsing, distribution |
| **Agent R** | `agents/agent_reviewer.md` | 2-5 (R1, R2, R3, R4, R5) | Parallel review with distributed knowledge / personas |
| **Agent B** | `agents/agent_b.md` | 1 | Post-paragraph reference verification |
| **Orchestrator** | This file | 1 | Workflow control, deliberation, user interaction |

### Reviewer Knowledge Allocation

| Reviewer | Knowledge | Perspective |
|---|---|---|
| R1 | writing-manual + Knowledge Group A | Domain expert A |
| R2 | writing-manual + Knowledge Group B | Domain expert B |
| R3 | writing-manual only | Rule-based judge — strict adherence to writing-manual rules |
| R4 | None (no references) | LLM judgment only — academic-writing generalist |
| R5 | None (no references) — **expert non-specialist reader persona** | Cross-disciplinary scientific reader: PhD-level competence in academic-writing conventions and scientific reasoning, but **no specialist knowledge of this paper's particular subfield**. Judges whether the argument lands when read by a competent scientist from an adjacent field — i.e., are the discipline-specific terms scaffolded enough that the logic is followable, are the warrants explicit, and does the evidence-claim chain hold up under generic scientific scrutiny? Flags passages where a smart scientist outside this subfield would have to stop and reread, or where unstated subfield assumptions silently load the argument. |

Exact grouping rules: Read `knowledge/distribution_strategy.md`.

R4 and R5 differ in **persona**, not data: both have no external knowledge,
but R4 evaluates as a generic academic-writing reviewer (logic, hedging,
flow, sentence craft), while R5 evaluates strictly as a **cross-disciplinary
scientific reader** (an experienced scientist from an adjacent field). R5's
job is to test whether the paragraph survives a competent outside-the-subfield
read: are subfield-specific premises made portable, or do they leak in
unstated? This is *not* a "lay reader" check — assume PhD-level training,
just from a different discipline.

---

## 4. Step 0: Initialization

### 0a. Load Writing-Manual Index

Read `writing-manual/INDEX.md` to get the routing table for section-specific
manual files. Do NOT load individual section files yet — those load on demand
when entering Mode 2 or Mode 3.

### 0b. Interpret User Input

Parse the user's request to extract:

| Parameter | Source | Example |
|---|---|---|
| `paper_path` | User provides file or folder path | `Z:/KKH_Research/Project/Draft/discussion.md` |
| `section` | Explicit or inferred from filename | `Discussion` |
| `target_journal` | User states or null | `"Geoderma"` |
| `paper_authors` | Title page / frontmatter / ask user if absent | `["Kim", "Lee"]` |
| `knowledge_path` | Explicit path or auto-discovered | `Z:/KKH_Research/Project/Knowledge/` |
| `mode` | User intent or default | `paper`, `section`, `paragraph` |

`paper_authors` is stored in session state and used by Agent B for
self-citation detection (`agents/agent_b.md` Step 7). If it cannot be
inferred from the draft, ask the user once during initialization.

If the user pastes text directly without a file path, treat as Mode 3 (paragraph).
See `config/navigation.md` for full input mapping.

### 0c. Parse Paper Files

Read the paper file(s) at `paper_path`.

- If a single `.md` or `.txt` file: read fully, split into sections by `#` headings
- If a folder: glob for `*.md` files, read each, map to sections
- If a `.docx` or `.pdf`: convert to text first (use markitdown skill if available)

Build sections list:
```
sections = [{ name: str, text: str, para_count: int }]
```

### 0d. Run Agent E (Knowledge Scan + Distribution)

Follow the full Agent E workflow from `agents/agent_e.md`:

1. **Phase 1:** Scan project Knowledge/Logic/Vocab directories.
   For each file, read first 20 lines only (Read tool with `limit: 20`).
   Build `knowledge_index[]`.

2. **Phase 2:** Match files to current context keywords.
   Full-read matched files. Parse by type (6 types).
   Populate `knowledge_bank`.

3. **Phase 3:** If `knowledge_bank.quality.local_sources < 3`,
   run web search supplement (Google Scholar, Semantic Scholar API).
   Skip if user opted out.

4. **Phase 4:** Distribute knowledge to reviewers per
   `knowledge/distribution_strategy.md` rules.

### 0e. Show Distribution Summary, Get User Approval

Display the distribution table (in Korean):

```markdown
---
### Knowledge Distribution

| 리뷰어 | 자료 | 관점 |
|---|---|---|
| R1 | [files] | [focus] |
| R2 | [files] | [focus] |
| R3 | writing-manual만 | 규칙 기준선 |
| R4 | (없음) | 일반 학술 리뷰어 (LLM 판단) |
| R5 | (없음) | 인접 분야 과학자 독자 |

Total: [N] knowledge files across [M] reviewers

---
*"이대로 진행" / "분배 변경" / "파일 추가: [경로]"*
```

Rows shown depend on the distribution case (A-D) from
`knowledge/distribution_strategy.md` — list only the active reviewers.

Ask for approval via AskUserQuestion (options: "이대로 진행" /
"분배 변경" / "파일 추가"). Handle overrides per
`knowledge/distribution_strategy.md` User Override section.

**Fast path:** if the distribution is Case D (no knowledge files at
all — including when the user pasted text directly with no paper path),
skip the approval step entirely. Just state in one line that the review
runs with R1 + R4 + R5 and proceed. The user can still adjust later
with `"분배 보여줘"` / `"파일 추가: [경로]"`.

---

## 5. Mode 1: Paper — Full Draft Review

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

---

## 6. Mode 2: Section — Section Review

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
LOGIC + HEDGING secondary.

### 6b. Deliberation

Same protocol as Mode 1. Classify results into consensus/unique/conflict.
Focus on paragraph-level issues.

### 6c. Present Results

Present per the `config/output_format.md` content contract: heading
names the section and paragraph count; a standard Markdown table lists
the Top-3 paragraph issues by impact score; closing next-actions line.
User expands via `"1번"` (single issue detail) or `"다 보여줘"`
(full list).

---

## 7. Mode 3: Paragraph — Paragraph + Sentence Review

**Entry:** User says "단락 [N] 검토", "이 단락 봐줘", or drills down from Mode 2.

**Context loading:** Follow `harness/context_loading.md` Mode 3 rules.
- Target paragraph + prev/next paragraph for context
- All cross-section files (including `sentence_craft.md`, `advanced_nns_issues.md`)
- Knowledge narrowed to paragraph-relevant entries

### 7a. Intent Confirmation

Display the paragraph with its Korean translation. Present the orchestrator's
interpretation of the paragraph's intent:

```markdown
### 단락 [N]

**[EN]** `[paragraph text]`
**[KR]** `[번역]`

### 의도 확인
이 단락의 의도를 이렇게 파악했습니다:

**핵심 메시지:** [요약]
**섹션 내 역할:** [기능]
**핵심 주장:** [중심 주장]

맞나요? 다르면 말씀해주세요.
```

Confirm via AskUserQuestion (options: "맞아요" / "다름 — 직접 설명").
Store the result as `{confirmed_intent}`.

### 7b. Single Panel Round — Paragraph AND All Sentences

Launch all active reviewers in parallel (one Agent tool call each) with:
- `{mode}` = `paragraph`
- `{target_text}` = full paragraph (with prev/next paragraph context),
  with sentences pre-numbered per the splitting rules in
  `config/session_management.md`
- `{confirmed_intent}` = user-confirmed intent
- `{allocated_knowledge}` + `{writing_manual_content}` per distribution

Each reviewer reports, in one pass:
- **Paragraph-level findings** — does the paragraph deliver the
  confirmed intent? Structure, flow (location: `"Paragraph N (whole)"`)
- **Sentence-level findings** — all six criteria per sentence
  (location: `"Sentence M"`)

This is ONE panel round per paragraph. Do NOT launch a new panel per
sentence — the per-sentence walkthrough below works entirely from this
round's results. (Wall-clock cost drops from one round per sentence to
one round per paragraph.)

### 7c. Deliberation + Sentence Walkthrough

1. Run the deliberation protocol (`harness/deliberation.md`) **once**
   over all findings, grouped by sentence; paragraph-level findings
   form their own group.

2. Present paragraph-level results first (Top-3 per tier discipline).

3. Walk through **only the sentences that have findings**, one at a
   time. For each:
   - display: previous sentence (context) → current sentence →
     Korean translation → issues (consensus / unique / conflict),
     with detail level per `harness/confidence_routing.md`
   - decision via AskUserQuestion — pick the 4 most relevant options,
     e.g. "수정안 A 적용" / "수정안 B 적용" / "원문 유지" /
     "건너뛰기" (use "검색해봐" as an option when confidence is LOW)

4. Sentences with no findings are NOT stepped through individually.
   Summarize them in one line: "문장 2, 5, 7 — 전원 동의, 수정 불필요."

5. Batch commands are honored at any point during the walkthrough
   (see `config/navigation.md`):
   - `"전부 적용"` — apply every consensus suggestion in this paragraph
     at once (multi-alternative issues take the recommended option)
   - `"합의만 적용"` — apply consensus items; still walk through
     unique findings and conflicts
   - `"나머지 건너뛰기"` — skip all remaining decisions in this paragraph

6. Record every decision in session state.

### 7d. Post-Paragraph: Agent B Reference Verification

After all sentences in the paragraph are reviewed, automatically run
Agent B following `agents/agent_b.md`:

1. Collect all citations from the paragraph
2. Check `knowledge_bank.sources[]` first — auto-FOUND for matches
3. Check `session.ref_cache` — use cached results
4. Web search remaining unverified citations
5. Cache all results in `session.ref_cache`
6. Present reference verification table

### 7e. Paragraph Completion Summary

```markdown
---
### 단락 [N] 검토 완료
- 수정: [X]건 (합의 [a], 발견 [b])
- 승인: [Y]건
- 건너뛰기: [Z]건

#### 레퍼런스 확인
| REF | 상태 | 제목 | DOI |
|---|---|---|---|
| Author (Year) | 확인됨 / 추정 / 미확인 | [...] | [...] |

---
*"다음 단락" / "이 단락 다시" / "섹션으로"*
```

Advance to next paragraph or follow user navigation.

---

## 8. Session Summary

When the user ends the session ("오늘 여기까지", "종료", "done"),
display the session summary following `config/output_format.md`:

```markdown
---
## 교정 세션 요약

| 항목 | 값 |
|---|---|
| 검토 모드 | [사용된 모드 목록] |
| 검토 단위 | 섹션 [N]개, 단락 [N]개, 문장 [N]개 |
| 리뷰어 수 | [N]명 |
| 합의 이슈 | [N]건 |
| 고유 발견 | [N]건 |
| 의견 충돌 | [N]건 |
| 수정 적용 | [N]건 |
| 승인 (무수정) | [N]건 |
| 건너뛰기 | [N]건 |
| 레퍼런스 미확인 | [N]건 |
| 추가 검색 실행 | [N]건 |

### 수정 이력

| # | 원문 | 수정문 | 근거 |
|---|---|---|---|
| 1 | [original] | [revised] | [합의/R1/R2/...] |

---
```

Offer session save if not already saved.

---

## 9. Reference Files

For implementation details beyond this orchestrator, read these files:

| Topic | File |
|---|---|
| Knowledge discovery & parsing | `agents/agent_e.md`, `knowledge/input_handler.md` |
| Review prompt template | `agents/agent_reviewer.md` |
| Reference verification | `agents/agent_b.md` |
| Knowledge distribution rules | `knowledge/distribution_strategy.md` |
| Knowledge bank schema | `knowledge/knowledge_bank_schema.md` |
| Web search strategy | `knowledge/search_strategy.md` |
| Deliberation protocol | `harness/deliberation.md` |
| Confidence-based routing | `harness/confidence_routing.md` |
| Context loading per mode | `harness/context_loading.md` |
| Mode switching & navigation | `config/navigation.md` |
| Output formatting rules | `config/output_format.md` |
| Session state & error handling | `config/session_management.md` |
| Writing-manual routing | `writing-manual/INDEX.md` |
