# Deliberation Protocol — Multi-Reviewer Result Synthesis

## Purpose

Define how to compare, classify, and present results from
multiple reviewers (R1–R5) who independently reviewed the same text.

---

## Process

### Step 1: Collect Results

All reviewers run in **parallel** (multiple `spawn_agent` calls in one response).
Wait for all to complete. Each returns:

```
CANDIDATES: [
    {
        unit,
        set: [ { id, objective, text, rationale, evidence_source, self_score } ],
        nomination: { best, beats_original, reason }
    }
]
ISSUES: [
    { id, criterion, description, location, severity, confidence }
]
SUGGESTIONS: [
    { id, issue_id, directive, evidence_source }   // non-local issues only
]
CONFIDENCE: HIGH | MEDIUM | LOW (per issue)
```

Two tracks flow from here:

- **CANDIDATES** → the Candidate Judge Round (Agent J) selects the optimal
  rewrite per unit. This is the primary path for wording / logic-flow /
  hedging. See "Candidate Judge Round" below.
- **ISSUES / SUGGESTIONS** → the 3-category classification (consensus /
  unique / conflict) below, feeding Top-N and Agent B. This path handles
  problems a same-unit rewrite cannot fix (missing citation, misplacement,
  numeric error, cross-section inconsistency).

### Step 2: Match and Classify

Compare issues across reviewers by **location** (same sentence/paragraph)
and **type** (same kind of problem).

Two issues "match" when they:
- Point to the same text span (same sentence or overlapping words)
- Identify the same category of problem (even if worded differently)

### Step 3: Classify into Three Categories

This classification governs the **ISSUES track only** — non-local problems
a same-unit rewrite cannot fix (missing/incorrect citation, wrong
placement, numeric error, cross-section inconsistency, coverage gap).
Wording / logic-flow / hedging improvements are NOT classified here; they
go through the Candidate Judge Round below. An issue carries a **single
corrective directive** (from SUGGESTIONS), not A/B/C rewrites — the
directive is usually determinate (one citation to add, one right section).

Each presented issue follows the `config/output_format.md` content
contract: 원문 → 문제 → 조치(directive) → 근거 → 발견자, in plain Korean.
Visual layout is at the model's discretion (standard Markdown).

#### Category 1: Consensus (2+ reviewers agree)

Two or more reviewers flagged the same issue, with a shared directive.

발견자 line: `발견자: R1+R3 합의` (or `R1+R2+R4 합의`).

**User action:** AskUserQuestion options, or typed `"[#] 적용"`.

#### Category 2: Unique Finding (1 reviewer only, with evidence)

Only one reviewer flagged it, but provides a rationale and directive.

발견자 line: `발견자: R1 단독` (replace with the actual reviewer ID).

**User action:** AskUserQuestion options, or typed `"[#] 적용"` /
`"[#] 무시"`.

#### Category 3: Conflict (reviewers disagree)

Reviewers propose contradictory directives, or disagree on whether it is
a problem at all. Show each reviewer's position and rationale in its own
labeled sub-section, plus a one-line explanation of why they disagree.
(Disagreement over how to *reword* a unit is not a conflict here — the
judge resolves that by selecting the optimal candidate.)

발견자 line: `의견 충돌: R1 ↔ R4`.

**User action:** AskUserQuestion (options: `R1 따름` / `R4 따름` /
`직접 입력` / `건너뛰기`).

---

## Candidate Judge Round (Agent J)

The CANDIDATES track does NOT go through consensus/unique/conflict
classification — candidates are not "issues," they are competing rewrites.
Instead, run the dedicated judge:

1. **Pool** all candidate sets across reviewers, grouped by unit. Merge
   the ORIGINAL as the baseline for each unit. Drop exact-duplicate texts.
2. **Launch Agent J** (`agents/agent_j.md`) — one call per paragraph
   (Mode 3) or per section (Mode 2). Pass the original unit(s), the
   confirmed intent, the pooled candidates, and the writing-manual rubric.
3. **Receive `SELECTIONS[]`** — per unit: the optimal (candidate /
   ORIGINAL / SYNTHESIZED), 1–2 runner-ups, disqualified candidates, and a
   `selection_confidence`.
4. The orchestrator presents each unit as: 원문 → 최적안(추천) →
   대안(1–2) → 근거 → 선정 신뢰도, per `config/output_format.md`. When the
   optimal is ORIGINAL, say "원문이 최적 — 수정 불필요" and still show the
   strongest explored alternative for transparency.
5. If `selection_confidence` is LOW, offer the web-search supplement
   (`harness/confidence_routing.md`) before the user decides.

The judge round and the ISSUES classification run over the same reviewer
output; present candidate selections at the point of each unit's
walkthrough (Mode 3, `modes/paragraph.md` 7c) and fold ISSUES into the Top-N block and
Agent B.

---

## Presentation Order

1. **Consensus issues** first (hardest to miss — not necessarily most important)
2. **Unique findings** next (often the highest-value findings; see below)
3. **Conflicts** last (require user judgment)

Within each category, order by severity (HIGH > MEDIUM > LOW).

Consensus comes first because it is the safest place to start reading, not
because it carries more evidential weight. Since all reviewers share one
model and one instruction set, consensus measures *salience*, not *truth*.
A HIGH finding raised by one reviewer outranks a LOW finding raised by
five — order within severity, never across it.

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

### Mode 3: Paragraph — Single reviewer round, then one judge round

Reviewers return, from ONE panel round (see `modes/paragraph.md` 7b): CANDIDATE sets
(paragraph-whole + every sentence), ISSUES, and SUGGESTIONS. Synthesis
runs once:

1. **Judge round.** Launch Agent J once for the paragraph (see "Candidate
   Judge Round" above). It returns the optimal rewrite + runner-ups for
   the paragraph-whole unit and each sentence.
2. **Issue classification.** Group ISSUES/SUGGESTIONS — paragraph-level
   (`"Paragraph N (whole)"`) as one group, sentence-level by sentence
   number — and run the 3-category classification (consensus / unique /
   conflict) on each group.
3. **Present.** The orchestrator presents the paragraph-whole result
   first (judge selection + any paragraph-level issues), then walks
   through each sentence (`modes/paragraph.md` 7c): the judge's optimal + alternatives
   for that sentence, plus any issues classified for it. No further
   reviewer or judge calls are needed during the walkthrough.
4. Sentences whose judge selection is ORIGINAL and that carry no issues
   are summarized in one line, not stepped through individually.

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
  + reviewer_agreement (count of reviewers flagging it, capped at 2)
  + category_weight
```

**Why agreement is capped at 2.** R1–R5 run the same model on identical
instructions; only their knowledge allocation and persona differ. Their
agreement is therefore repeated sampling from one prior, not independent
corroboration — five reviewers converging tells you the issue is *hard to
miss*, not that it is *important*. Uncapped, agreement could contribute
more than severity itself (max 5 vs max 4), letting five reviewers agreeing
on a trivial polish item outrank a single reviewer catching a fatal flaw.
Severity and category must dominate; agreement is a tiebreaker.

This matches how the CANDIDATES track already reasons — see
`agents/agent_j.md` Rule 5, "Merit, not popularity. A single reviewer's
candidate can beat a consensus one." The two tracks now use the same
epistemology.

**Corollary for unique findings.** An issue raised by one reviewer is not
weaker evidence than a consensus issue; it is often the opposite, since the
reviewers most likely to see something alone are R5 (outside-subfield
reader) and whichever reviewer holds the relevant knowledge file. Do not
bury single-reviewer CRITICAL/HIGH findings beneath consensus LOW ones.

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
    // Candidate/judge counters (Agent J, see agents/agent_j.md):
    units_with_candidates: int,      // units that went through the judge round
    judge_optimal_not_original: int, // units where a rewrite beat the original
    judge_original_kept: int,        // units where ORIGINAL was optimal
    judge_synthesized: int,          // units where the judge merged a new best
    user_applied_optimal: int,       // user took the judge's optimal
    user_applied_runner_up: int,     // user took a runner-up instead
    user_kept_original: int,         // user overrode to keep the original
    // Integrity counters from Agent B (see agents/agent_b.md):
    ref_not_found: int,              // citation existence failures
    numeric_inconsistencies: int,    // N/percentage/sig-fig conflicts
    secondary_citations_flagged: int // Telephone Game audit hits
}
```
