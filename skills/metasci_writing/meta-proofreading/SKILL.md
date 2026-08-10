---
name: meta-proofreading
description: >
  Panel proofreading of an existing draft — several reviewers with different
  knowledge allocations review the same text in parallel, a judge scores their
  competing rewrites, and the original can win. Covers a full draft, one section,
  or one paragraph down to the sentence.
  Invoke only when the user names the panel: "메타 교정", "메타교정", "패널 교정",
  "리뷰어 교정", "다중 리뷰어 교정", "meta-proofreading", "panel proofreading".
  Plain "논문 교정" or "proofread" goes elsewhere — one paragraph to meta-rewriting,
  wording attestation to meta-proofreading-evidence, style to meta-styling,
  AI traces to meta-rewriting-antiai, composition and order to meta-writing-mapping.
allowed-tools: [Read, Write, Glob, Grep, WebSearch, WebFetch, Agent, AskUserQuestion]
---

# Meta-Proofreading — Multi-Reviewer Deliberation Orchestrator

## 1. Environment

- **Runtime:** Claude Code; reviewers run as parallel sub-agents
  (one **Agent tool** call per reviewer, all in a single response)
- **Output language:** All user-facing output in Korean (한국어)
- **Agent internal prompts:** English (for optimal LLM performance)
- **English original text:** Always displayed alongside Korean explanation
- **User input style:** Korean or English, free-form; see `config/navigation.md` for input mapping
- **Tools:** the `allowed-tools` line in this file's frontmatter is authoritative.
  `Write` is there for one purpose — the session save file at
  `~/.claude/projects/[project_hash]/memory/proofreader-session.json`
  (`config/session_management.md`). This skill never writes to the user's draft;
  revisions are presented for the author to apply.
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
│   ├── agent_j.md                        ← Candidate Judge & Optimal Selector
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
├── modes/                                ← One runs per invocation (§5 routes)
│   ├── paper.md                          ← Mode 1: full draft
│   ├── section.md                        ← Mode 2: one section
│   └── paragraph.md                      ← Mode 3: paragraph + every sentence
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
| **Agent R** | `agents/agent_reviewer.md` | 2-5 (R1, R2, R3, R4, R5) | Parallel review — diagnose issues AND generate rewrite candidates |
| **Agent J** | `agents/agent_j.md` | 1 per paragraph (Mode 3) / per section (Mode 2) | Judge pooled candidates, select the optimal rewrite |
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

## 5. Modes

One mode runs per invocation. Read that mode's file and no other.

| Mode | Entry | File |
|---|---|---|
| **1 — Paper** | "전체 초고 봐줘", "논문 전체 검토", "full draft" | `modes/paper.md` |
| **2 — Section** | "[섹션] 검토", "Discussion 교정", or drill-down from Mode 1 | `modes/section.md` |
| **3 — Paragraph** | "단락 [N] 검토", "이 단락 봐줘", pasted text with no file path, or drill-down from Mode 2 | `modes/paragraph.md` |

All three share one shape: load context per `harness/context_loading.md`, launch
the active reviewers in parallel (one Agent call each, all in a single response),
classify results per `harness/deliberation.md`, present per the
`config/output_format.md` contract. What differs is the review unit, the reviewer
focus, and whether a judge round runs. The mode file specifies those.

Drill-down (Mode 1 → 2 → 3) carries Step 0's distribution forward — Step 0 runs
once per session.

---
## 6. Session Summary

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

### 이번 세션 반복 지적 유형

- [2회 이상 지적된 유형과 건수, 예: 모호한 지시어 4건, 헤지 과소보정 3건]

> 세션이 쌓이면 이 목록이 저자 자신의 체크리스트가 된다.

### AI 사용 기록

- 도구: meta-proofreading (다중 리뷰어 [N]명 + 심판 + 레퍼런스 검증)
- 수행: 문체·논리 진단, 리라이팅 후보 생성, 후보 채점, 인용 존재 검증
- 미수행: 사실 검증, 데이터 재계산, 분야 지식 판단, 출처 내용 대조
- 적용된 수정 [N]건은 모두 저자가 개별 선택한 것 / 일괄 적용 [N]건

### 고지

> 이 산출물은 **초안**이며 확정 원고가 아니다. 적용된 문장은 AI가 생성한
> 제안이고, 최종 판단과 책임은 저자에게 있다.
> 최적안 선정은 AI 단독 판정이다 — 리뷰어와 심판이 같은 모델이므로,
> 합의나 높은 점수가 옳음을 보증하지 않는다.
> 인용의 **실재**는 Agent B가 확인하지만 **내용 일치**는 확인하지 않는다.
> 투고 전 저널·기관의 AI 사용 정책을 확인하고, 필요하면 위 사용 기록을
> disclosure 초안으로 활용할 것.

---
```

Offer session save if not already saved. When saving, include the candidate
pool and judge decisions alongside the final text — the process record is
what makes the AI 사용 기록 above verifiable later.

---

## 7. Reference Files

For implementation details beyond this orchestrator, read these files:

| Topic | File |
|---|---|
| **The review procedure itself — read the one for the active mode** | `modes/paper.md`, `modes/section.md`, `modes/paragraph.md` |
| Knowledge discovery & parsing | `agents/agent_e.md`, `knowledge/input_handler.md` |
| Review prompt template (issues + candidates) | `agents/agent_reviewer.md` |
| Candidate judging & optimal selection | `agents/agent_j.md` |
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
