---
name: meta-proofreading
description: >
  Proofread and revise academic papers, sections, or paragraphs with a
  knowledge-distributed panel of reviewers. Use when the user wants multi-angle
  review of logic, structure, language, claim calibration, quantitative integrity,
  citations, or evidence. Reviewers share the same task but receive different
  knowledge allocations; a judge synthesizes by merit rather than majority vote.
  Not for simple one-paragraph rewriting when deliberation is unnecessary.
---

# Meta Proofreading

Run evidence-aware academic proofreading with independent reviewers, explicit
verification states, and author-controlled revisions.

## Runtime contract

- Explain the review in the user's language. Preserve the manuscript's language
  unless translation is requested.
- Do not depend on an external development kernel. Operative Codex rules are
  bundled in `references/codex-*.md`.
- Inspect files already in scope before asking the user for discoverable details.
- Never invent evidence, citations, numerical corrections, venue rules, or author
  intent.
- Do not claim verification unless an appropriate original or official source was
  checked.
- Do not edit the manuscript file unless the user asked for file changes or approves
  the proposed revision set.
- Treat choices as interface aids only. Put the diagnosis, alternatives, evidence,
  and consequences in the message body. If no interactive choice tool is available,
  ask one plain decision question and wait.

## Required references

Read before starting:

1. `references/codex-kernel-index.md`
2. `references/rule-routing.md`
3. `writing-manual/INDEX.md`
4. `config/navigation.md`
5. `config/output_format.md`

Load as needed:

- `references/codex-process.md`
- `references/codex-paragraph-logic.md`
- `references/codex-section-structure.md`
- `references/codex-ai-era.md`
- relevant files under `writing-manual/sections/`
- relevant files under `writing-manual/cross_section/`
- `harness/context_loading.md`
- `harness/deliberation.md`
- `harness/confidence_routing.md`
- `knowledge/input_handler.md`
- `knowledge/knowledge_bank_schema.md`
- `knowledge/distribution_strategy.md`
- `knowledge/search_strategy.md`
- the required reviewer files under `agents/`

## Precedence

Apply constraints in this order:

1. source fidelity, research integrity, and non-fabrication;
2. current official venue and reporting requirements;
3. the author's explicit scope and intended meaning;
4. Codex kernel rules;
5. the writing manual and reviewer heuristics;
6. stylistic preference.

Examples, paragraph counts, date windows, and word ranges are not requirements
unless the current venue or genre makes them so.

## Review modes

Infer the smallest mode that satisfies the request:

- **Sentence**: one sentence; usually 2 reviewers plus factual checking when needed.
- **Paragraph**: paragraph logic and sentence craft; 2–3 reviewers.
- **Section**: section function, paragraph sequence, and cross-section dependencies;
  3–4 reviewers.
- **Paper**: structural triage followed by prioritized section/paragraph review;
  3–5 reviewers.
- **Reference / quantitative audit**: Agent B-centered verification with only the
  relevant language reviewers.

Use `meta-rewriting` for a simple rewrite that does not benefit from a panel.

## Workflow

### Phase 0 — Intake and source boundary

Identify:

- manuscript scope and language;
- section type and target venue, if known;
- whether the user wants diagnosis, proposed revisions, or file edits;
- research materials supplied as data versus prior literature;
- paper authors when self-citation analysis is relevant;
- web-search limits stated by the user.

For `.docx` or `.pdf`, use the appropriate document/PDF reading capability.
Preserve tables, equations, comments, and layout relationships when they affect
meaning.

Do not force the user to answer all intake questions. Infer non-material details
and ask only when a missing choice would materially change the review.

### Phase A — Structural and risk triage

Before sentence editing, identify the highest-impact risks:

- question–answer chain across sections;
- missing or duplicated paragraph functions;
- unsupported or overbroad claims;
- Methods–Results mismatches;
- quantitative inconsistencies;
- citation or attribution risks;
- venue-specific noncompliance;
- sentences whose meaning is ambiguous.

Create a review plan ordered by likely downstream impact. For long manuscripts,
review a representative or high-risk sample first and obtain approval before
expanding, unless the user explicitly asked for an uninterrupted full pass.

### Phase B — Build the knowledge bank

Normalize supplied PDFs, extractions, notes, and web evidence with
`knowledge/knowledge_bank_schema.md`.

Keep two separate concepts:

- **navigation value**: how useful a note or extraction is for locating material;
- **evidentiary authority**: whether the original data, full text, or official
  metadata supports the claim.

A local extraction is not automatically verified. Multiple derived notes do not
become independent evidence. Source sufficiency depends on the claim and decision,
not on a fixed source count.

Use web search when the user requests it, current venue information is needed, a
citation requires verification, or a load-bearing claim cannot otherwise be
assessed. Respect an explicit no-web instruction. For technical searches, rely on
primary sources and official documentation where possible.

### Phase C — Allocate independent reviewers

All reviewers receive the same manuscript text, task, output schema, and baseline
writing rules. Vary only their knowledge allocation or perspective according to
`knowledge/distribution_strategy.md`.

Typical roles:

- 2–5 instances of `agents/agent_reviewer.md` with different knowledge slices;
- `agents/agent_b.md` for numbers, citation existence, attribution, and
  claim–source fidelity;
- `agents/agent_e.md` when external literature supplementation is needed;
- `agents/agent_j.md` as the independent synthesis judge.

Preserve independence: do not show reviewers one another's conclusions before they
submit. Record which knowledge slice each reviewer received.

### Phase D — Generate issues and candidates

Reviewers must:

- distinguish observation, interpretation, recommendation, and verification status;
- identify the exact text span and rule implicated;
- state consequence and severity;
- propose a complete candidate only when it materially improves the unit;
- select `ORIGINAL` when no candidate is better;
- preserve numbers, citations, technical terms, hedges, and claim scope unless a
  disclosed correction is supported.

Do not require a rewrite for every clean sentence. Forced candidates create correlated
noise and unnecessary churn.

### Phase E — Deliberate by merit

Use `harness/deliberation.md`.

1. Normalize duplicate issues and candidate units.
2. Check whether apparent agreement is independent or caused by shared inputs.
3. Rank globally by severity, evidence quality, and downstream impact.
4. Use consensus as supporting information, not the primary rank.
5. Preserve high-severity minority findings for review.
6. Ask the judge to score candidates independently; reviewer self-scores are
   advisory.
7. Allow `ORIGINAL` to win.

Do not let five reviewers agreeing on a cosmetic edit outrank one reviewer finding
a well-supported factual or structural error.

### Phase F — Verify protected content

Before presenting a revision, compare it with the original for:

- claim breadth and direction;
- causal versus associative wording;
- numbers, units, signs, ranges, and statistical notation;
- citation placement and source attribution;
- negation, modality, hedging, and limitations;
- terminology, variables, cross-references, and section function.

Reference states are:

- **확인됨 / verified**: checked against an appropriate original or official source;
- **부분 확인 / partial**: identity or metadata is plausible/confirmed, but the
  load-bearing claim or full context was not verified;
- **미확인 / unverified**: insufficient evidence or no check.

Self-citations receive the same verification as other citations. Labeling a source
`SELF` is metadata, not a reason to skip checking it.

### Phase G — Present and decide

Present the smallest useful decision package:

- reviewed text and location;
- highest-impact diagnosis;
- judge-selected revision or `ORIGINAL`;
- materially distinct alternatives when they exist;
- verification state and evidence;
- the consequence of each option.

For high-confidence, meaning-preserving fixes, the user may approve a batch.
For medium or low confidence, substantive meaning changes, factual uncertainty, or
conflicting evidence, request a focused decision. Never hide full alternatives in
choice labels.

### Phase H — Apply and log

Apply only approved changes. After application:

- rerun the protected-content comparison;
- report unresolved high-impact issues;
- save a minimal session record only when working in a user-designated project
  directory;
- use `.codex/meta-proofreading/session.json` as the portable default;
- avoid storing unnecessary manuscript text, copyrighted full text, secrets, or
  sensitive personal data.

## Output contract

Lead with the outcome, not the panel mechanics.

For each priority issue include:

1. **Location and severity**
2. **Why it matters**
3. **Evidence and verification state**
4. **Judge's choice** — revision or `ORIGINAL`
5. **Alternatives** — only materially distinct ones
6. **Author decision needed** — only when needed

End with:

- applied/approved change count;
- unresolved high-impact issue count;
- reference audit table when citation checking occurred;
- next review scope.

## Stop conditions

Complete when the requested scope has been reviewed, approved changes have been
applied if authorized, preservation checks pass, and unresolved material issues are
reported. Do not equate reviewer consensus, source count, or elapsed search effort
with completion.
