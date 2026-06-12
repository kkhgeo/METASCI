# Deliberation Protocol — Multi-Reviewer Result Synthesis

## Purpose

Define how to compare, classify, and present results from
multiple reviewers (R1–R5) who independently reviewed the same text.

---

## Process

### Step 1: Collect Results

All reviewers run in **parallel** (multiple Agent tool calls in one response).
Wait for all to complete. Each returns:

```
ISSUES: [
    { id, criterion, description, location, severity, confidence }
]
SUGGESTIONS: [
    {
        id, issue_id, original,
        alternatives: [
            { label, revised, tone, rationale }  // 1-3 items (see agent_reviewer.md Rule 11)
        ],
        evidence_source
    }
]
CONFIDENCE: HIGH | MEDIUM | LOW (per issue)
```

### Step 2: Match and Classify

Compare issues across reviewers by **location** (same sentence/paragraph)
and **type** (same kind of problem).

Two issues "match" when they:
- Point to the same text span (same sentence or overlapping words)
- Identify the same category of problem (even if worded differently)

### Step 3: Classify into Three Categories

Each presented issue follows the `config/output_format.md` content
contract: 원문 → 문제 → 수정안(들) → 근거 → 발견자, in plain Korean.
Visual layout is at the model's discretion (standard Markdown).

#### Category 1: Consensus (2+ reviewers agree)

Two or more reviewers flagged the same issue.

- Single alternative when the issue is LOGIC / STRUCTURE / FACTUAL —
  the correction is determinate.
- Multiple alternatives (2–3, labeled A/B/C with tone + rationale +
  recommendation) when the issue is STYLE / HEDGING / TERMINOLOGY /
  CLUTTER — draw tone-varied alternatives from across the agreeing
  reviewers (prefer variety over near-duplicates; cap at 3).

발견자 line: `발견자: R1+R3 합의` (or `R1+R2+R4 합의`).

**User action:** AskUserQuestion options, or typed `"[#] 적용"` /
`"[#] [A/B/C] 적용"`.

#### Category 2: Unique Finding (1 reviewer only, with evidence)

Only one reviewer flagged it, but provides a rationale.
Single or multiple alternatives per `agents/agent_reviewer.md` Rule 11.

발견자 line: `발견자: R1 단독` (replace with the actual reviewer ID).

**User action:** AskUserQuestion options, or typed `"[#] 적용"` /
`"[#] [A/B/C] 적용"` / `"[#] 무시"`.

#### Category 3: Conflict (reviewers disagree)

Reviewers propose contradictory changes to the same text.
Show each reviewer's suggestion and rationale in its own labeled
sub-section, plus a one-line explanation of why they disagree.

발견자 line: `의견 충돌: R1 ↔ R4`.

**User action:** AskUserQuestion (options: `R1 따름` / `R4 따름` /
`직접 입력` / `건너뛰기`).

---

## Presentation Order

1. **Consensus issues** first (most reliable)
2. **Unique findings** next (may catch things consensus missed)
3. **Conflicts** last (require user judgment)

Within each category, order by severity (HIGH > MEDIUM > LOW).

---

## No-Issue Consensus

If all reviewers agree there are no issues with the current text, say
so in one plain line and offer the next actions:

> **전원 동의** — 이 [문장/단락/섹션]에 수정 필요 없음.
> 진행 `"다음"` · 상세 `"그래도 자세히 봐줘"`

---

## Confidence-Driven Actions

After deliberation, assess overall confidence:

```
All issues HIGH confidence → Present results, expect quick decision
Any MEDIUM confidence → Present with detailed explanation
Any LOW confidence → Flag to user:
    "이 부분에 대해 리뷰어들의 확신이 낮습니다.
     추가 검색을 할까요? (웹에서 유사 논문의 표현을 찾아봅니다)"
    
    If user agrees → run web search for comparable expressions
    If user declines → proceed with available suggestions
```

---

## Mode-Specific Deliberation

### Mode 1: Paper — Structural deliberation

Focus on: cross-section consistency, argument arc, coverage gaps.
Each reviewer provides a structure assessment.
Deliberation compares: which structural issues overlap?

Output: priority section list (consensus-ranked).

### Mode 2: Section — Paragraph arrangement deliberation

Focus on: paragraph order, move structure, missing/redundant paragraphs.
Deliberation compares: which paragraphs need attention?

Output: paragraph-level issue map.

### Mode 3: Paragraph — Single-round deliberation, grouped by sentence

Reviewers return paragraph-level AND sentence-level findings from ONE
panel round (see SKILL.md 7b). Deliberation also runs once:

1. Group all findings — paragraph-level findings (`"Paragraph N
   (whole)"`) form one group; sentence-level findings group by
   sentence number.
2. Within each group, run the standard 3-category classification
   (consensus / unique / conflict).
3. The orchestrator then presents paragraph-level results first and
   walks through flagged sentences one at a time (SKILL.md 7c) —
   no further reviewer calls are needed during the walkthrough.

---

## Top-N Priority Sort (Closing Block)

After classification (consensus / unique / conflict) and confidence routing,
the orchestrator must produce a **Top-N Priority Revisions** block as the
closing element of every Mode 1 and Mode 2 review. This block answers the
user's first practical question: *"Of all these findings, what should I fix
first?"*

### When to produce

| Mode | Top-N (Tier 1 view) | Top-N (Tier 3 full list) |
|---|---|---|
| Mode 1 (Paper) | 3 | 5 |
| Mode 2 (Section) | 3 | 5 |
| Mode 3 — paragraph phase | 3 | 3 |
| Mode 3 — sentence phase | n/a (per-sentence decisions are atomic) | n/a |

Tier 1 (the default first response) always shows the top 3.
The user expands to the full Top-N (5 for paper/section) by saying
`"다 보여줘"` / `"전체 보기"` (Tier 3).

### Ranking rules

Pool every issue across all reviewers (consensus + unique + conflict).
Score each issue by **impact**, then sort descending. Impact = a
combination of severity, agreement, and category weight:

```
impact_score =
    severity_weight (CRITICAL=4, HIGH=3, MEDIUM=2, LOW=1)
  + reviewer_agreement (count of reviewers flagging it, max 5)
  + category_weight
```

Note on CRITICAL: reviewers (R1–R5) only emit HIGH/MEDIUM/LOW (see
`agents/agent_reviewer.md` output schema). CRITICAL enters the pool
exclusively from Agent B integrity findings (`agents/agent_b.md`).

Where `category_weight` adds priority for findings that affect
the paper's credibility, not only its style:

| Finding category | category_weight |
|---|---|
| Numerical inconsistency (from `quantitative_integrity.md`) | +3 |
| Secondary-source citation for quantitative claim | +2 |
| Reference verification failure (from `agent_b.md` NOT_FOUND) | +3 |
| Terminological inconsistency across sections (Banana Rule) | +2 |
| Argument-structure / logic issue | +2 |
| Cohesion / Given-New violation | +1 |
| Hedge under/over-calibration | +1 |
| Clutter / redundancy | +1 |
| Sentence-craft polish | +0 |

Timing note: the first three categories originate from Agent B, which
runs only after a paragraph's sentence-level review (Mode 3). In Mode 1
and Mode 2 Top-N blocks, these categories appear only when a reviewer
raised the same concern as a FACTUAL finding; once Agent B results exist
(Mode 3 paragraph completion and session summary), its findings join the
pool with these weights.

Tie-break order: severity → agreement → location (earlier in document first).

### Output format

The Top-N priority block is a **standard Markdown table** with columns
순위 / 심각도 / 카테고리 / 한 줄 요약, per the `config/output_format.md`
content contract.

Severity labels: CRITICAL → 치명 · HIGH → 높음 · MEDIUM → 중간 ·
LOW → 낮음. Words only — no symbols or emoji.

Do **not** auto-expand the top item below the table. The Tier 1 view is
intentionally compact (the full nav box from `config/output_format.md`
follows the table). The user pulls detail by saying `"1번"` /
`"#1 자세히"`, which renders that issue's full detail
(원문 → 문제 → 수정안 → 근거 → 발견자).

### Suppression rule

If fewer than N issues exist, list only what exists. If zero issues
exist across all reviewers, replace the table with one plain sentence:
"이 [모드 단위]에서 우선 수정할 항목이 없습니다."

### Interaction with confidence routing

If the top-ranked item has CONFIDENCE: LOW, append one plain line below
the table (before the next-actions line):
**1순위는 신뢰도 낮음** — `"검색해봐"` 라고 하면 보강합니다.

The user can say `"검색해봐"` to invoke the web-search supplement before
deciding.

---

## Deliberation Statistics (Session Summary)

Track across the session:

```
deliberation_stats = {
    total_units_reviewed: int,       // sentences, paragraphs, or sections
    consensus_issues: int,           // 2+ reviewers agreed
    unique_findings: int,            // 1 reviewer only
    conflicts: int,                  // reviewers disagreed
    no_issue_consensus: int,         // all agreed no problem
    user_accepted_consensus: int,    // user followed consensus
    user_accepted_unique: int,       // user accepted unique finding
    user_resolved_conflict: int,     // user resolved a conflict
    user_rejected: int,              // user rejected a suggestion
    // Integrity counters from Agent B (see agents/agent_b.md):
    ref_not_found: int,              // citation existence failures
    numeric_inconsistencies: int,    // N/percentage/sig-fig conflicts
    secondary_citations_flagged: int // Telephone Game audit hits
}
```
