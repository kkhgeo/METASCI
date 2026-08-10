---
name: meta-writing
description: >
  Draft, revise, and verify evidence-grounded academic manuscript sections by separating
  original research materials (My Data: figures, tables, and data files) from prior
  literature (Knowledge, PDF, and Web). Use for IMRaD or venue-specific section writing,
  literature-grounded interpretation, figure/table-based Results, Discussion synthesis,
  bilingual English-Korean drafting, and venue-aware citation verification with APA 7
  as the fallback when no style is resolved. Trigger on requests
  such as "글쓰기", "섹션 작성", "선행연구 정리", "Results 써줘", "Discussion 작성",
  "이 그림 기반으로 써줘", "Knowledge 기반으로 글써줘", and "Figure 해석해줘".
---

# Meta Writing Skill

## Overview

Combines original research data (My Data) with prior literature knowledge (Knowledge Sources)
to write academic paper sections.

**Two types of information are clearly distinguished:**

| Category | My Data (Original Research) | Knowledge Sources (Prior Literature) |
|----------|---------------------------|--------------------------------------|
| Identity | Data produced by the researcher | Knowledge drawn from prior studies |
| Examples | Figure, Table, CSV | Knowledge MD, PDF, Web |
| Role in text | Subject of description/interpretation | Basis for comparison/evidence |
| Results | "This study showed ~ (Figure 1)" | "Similar to (Chen et al., 2024)" |
| Discussion | "The observed pattern suggests ~" | "Explained by Chen (2024)'s model" |

**Source discovery order:**
1. Knowledge folder (markdown) — Use structured notes to locate relevant claims and sources
2. PDF folder — Read original papers available locally
3. Web search — Check current venue guidance or fill an evidence gap when allowed

Discovery order is not evidence authority. Prefer the original paper, dataset, or official
venue page when substantiating a claim or current requirement. Treat Knowledge markdown as
an index and secondary note until its cited original is checked.

---

## Codex Rule Routing

Load the Codex rule references that match the operation before acting. Read each selected
file completely and apply every rule with its diagnostic check and exceptions.

| Operation | Required Codex references |
|---|---|
| Plan or outline a section | `references/codex-process.md`, `references/codex-section-structure.md` |
| Draft a section | `references/codex-process.md`, `references/codex-paragraph-logic.md`, `references/codex-section-structure.md`, `references/codex-ai-era.md` |
| Revise an existing draft | `references/codex-process.md`, `references/codex-paragraph-logic.md`, and the relevant section rules |
| Verify or prepare for submission | `references/codex-paragraph-logic.md`, `references/codex-section-structure.md`, `references/codex-ai-era.md` |

Use these precedence rules when instructions conflict:

1. Preserve research integrity, source fidelity, and data accuracy.
2. Follow the current target-venue requirement unless it conflicts with research integrity.
3. Preserve the rhetorical function of the requested section.
4. Apply general clarity and concision rules only after the first three constraints.

Do not load or apply unpromoted items from the kernel candidate registry.

---

## Project Settings Load

Before starting, search for `writing.local.md` in the current directory.

- **If found**: Load settings and summarize the assumptions in the work record. Ask for
  confirmation only when a setting conflicts with the request or would materially change the manuscript.
- **If not found**: Use sources and constraints supplied in the request, including pasted
  material. Suggest `writing.local.template.md` only when reusable project settings would
  help; ask for source paths only when the required material cannot otherwise be accessed.
- **If the user explicitly specifies paths**: These take priority over writing.local.md.

---

## Input Parsing (Phase 1)

Analyze the user request to determine the items below.
Proceed with explicit, low-risk assumptions when the request and sources are sufficient.
Ask only when a missing source, target section, venue constraint, or interpretive choice
would materially change the manuscript.

```xml
<task_spec>
Core topic: [topic]
Section: [Introduction/Methods/Results/Discussion]
Scope: [full section/specific part]
Focus: [perspective/objective]
Core message: [the single central claim this text must land — one sentence]
Target reader: [specialist / adjacent-field / general — default: adjacent-field]
Request type: [topic/figure/table]
Target venue: [journal/institution + guideline path or URL / unresolved]
Manuscript structure: [separated-IMRaD / combined-results-discussion / venue-specific]

My Data:
  figures: [file path list, section placement]
  tables: [file path list, section placement]
  data_files: [file path list]

Knowledge Sources:
  knowledge_folder: [path or "none"]
  pdf_folder: [path or "none"]
  web_search: [allowed/not allowed]

Settings:
  citation_target: [coverage-based / user-set number, default coverage-based]
  paragraphs: [scope-derived / user-set number, default scope-derived]
  words_per_paragraph: [scope-and-venue-derived / user-set range, default scope-and-venue-derived]
  citation_style: [target-venue / APA 7 fallback / user-specified, default target-venue then APA 7 fallback]
  language: [bilingual/english/korean]
  results_style: [data-only / with-comparison, default data-only for separated IMRaD]
</task_spec>

> `Core message` is the organizing constraint for the whole draft: every paragraph must
> advance it, and anything that does not is cut in Phase 3.5. If the user did not supply
> one, derive a candidate from the sources. Proceed with it as an explicit working assumption
> when the evidence supports one clear reading; ask only when materially different readings compete.
> `Target reader` sets how much jargon is unpacked. In separated IMRaD, keep Results
> descriptive and move literature comparison, causes, mechanisms, and implications to
> Discussion. Use `with-comparison` only when the venue uses a combined Results and
> Discussion format or explicitly permits comparison in Results.
> `citation_target: coverage-based` means that every claim requiring external support is
> cited, without padding paragraphs to meet a quota. A user-set number is a planning floor,
> not permission to add irrelevant citations.
```

### Section Reference

| Section | Content | My Data Role | Knowledge Role |
|---------|---------|-------------|----------------|
| Introduction | Background, prior research, gap, objectives | Minimal | Primary (synthesis of prior research) |
| Methods | Methods, techniques, samples | Sample/instrument information | Methodology references/citations |
| Results | Data and analysis outputs | **Primary** (subject of description) | Normally none; factual comparison only when the manuscript structure permits it |
| Discussion | Interpretation, implications, limitations | **Primary** (subject of interpretation) | Basis for interpretation |

---

## Knowledge Exploration and Analysis (Phase 2)

Explore and analyze sources using the 5-Loop process.

> **Detailed procedure**: Read and follow the Loop 1-4 sections of `references/writing_template.md`.

### Loop Summary

```
Loop 1: Source Scan and Planning
  - Load writing.local.md (if available)
  - Check My Data folder (list figures/tables/data)
  - Check Knowledge folder (index.md, select relevant files)
  - Check PDF folder
  - Establish exploration plan

Loop 2: Knowledge Reading
  - Read an initial batch of relevant Knowledge markdown files (up to 5), then continue if claim coverage remains incomplete
  - Extract Claim + Citation pairs
  - Intermediate Result A

Loop 3: My Data Analysis + Additional Sources
  - Analyze My Data figures/tables (extract patterns, values)
  - Generate comparison pairs between My Data and Knowledge
  - Read additional Knowledge/PDF files
  - Intermediate Result B

Loop 4: Gap Check + Web Search
  - Verify claim coverage, topic coverage, required recency, and comparable evidence
  - If insufficient, supplement with Web search (if allowed)
  - Intermediate Result C + Gap Report
```

### Gap Check Criteria

| Gap Type | Judgment Criteria | Response |
|----------|------------------|----------|
| Unsupported claims | One or more claim-bearing sentences lack suitable evidence | Additional Knowledge/PDF/Web search or narrow the claim |
| Insufficient comparison data | No suitably comparable studies representing agreement, disagreement, null, or mixed findings | Broaden PDF/Web search without filtering for agreement |
| Insufficient recency coverage | The task or venue requires a current literature window that the sources do not cover | Web search |
| Insufficient interpretation basis | No theories/mechanisms to cite in Discussion | PDF/Web search |

---

## Writing (Phase 3)

> **5-Loop details**: Follow the Loop 5 section of `references/writing_template.md`.
> **Section-specific structure, transitions, examples**: Read the corresponding section in `references/section_guides.md`.

### Core Rules

**My Data vs Knowledge Distinction Principle:**
- My Data is described directly without citations. Reference as "(Figure 1)", "(Table 2)".
- Knowledge Sources must always be cited in the selected venue style; use (Author, Year)
  only when that style or the APA 7 fallback applies.
- When mixing My Data and Knowledge in a single sentence, clearly indicate which is original research and which is prior literature.

**Paragraph Writing Rules:**
1. Function: Give each paragraph one central function and make its main claim visible;
   a topic sentence need not be first when a clear rhetorical purpose justifies delay
2. Evidence: Cite every externally supported claim with the most relevant source(s);
   do not add citations merely to reach a numerical quota
3. Transitions: Use natural connectors (refer to section_guides.md)
4. Landing point: End by landing the claim or leading forward when that function is needed;
   do not force a formula onto short transitional paragraphs
5. Evidence selection: Prefer the most direct, methodologically suitable original source;
   add independent corroboration when it improves support, not merely to diversify source types
6. One idea per sentence: Split sentences that carry two independent claims
7. Density: Every sentence must earn its place. Cut wording that adds no information
8. Reader level: Unpack terms an `adjacent-field` reader would not know, unless
   `Target reader: specialist` was set
9. Terminology: Use one canonical term for the same concept, variable, population, and
   outcome across sections; preserve different terms when they mark real distinctions
10. Reasoning: Audit causal leaps, generalization, circularity, contradiction, and ignored
    alternatives; explain the actual inferential problem instead of merely naming a fallacy

**Source Language Discipline (표절·의미왜곡 방지):**
- Never transplant a sentence verbatim from a Knowledge markdown, PDF, or web page into
  the manuscript. The Claim strings collected in Loop 2 are *notes*, not draft text —
  restate them in your own wording.
- If exact wording is genuinely necessary, mark it as a direct quotation with quotation
  marks and the source, and keep it short.
- When restating, do not shift the original's scope, strength, or emphasis. A sample-level
  finding must not become a population-level claim; a hedged finding must not become
  a definite one.
- Vary reporting verbs to match what the cited author actually did
  (reported / observed / proposed / argued / demonstrated / suggested). Do not repeat one
  verb across consecutive citations.

**Bilingual Output:**
- When `language: bilingual`, write English first followed by Korean translation
- When `language: english` or `language: korean`, output only the requested manuscript language
- Maintain consistency of academic terminology
- Preserve the selected citation style in every language version

---

## Revision (Phase 3.5)

The draft from Phase 3 is a first pass, not the output. Run one revision pass before
verification. **Work global-first, local-last** — fixing commas in a paragraph that is
about to be deleted is wasted effort.

### Global pass (logic and focus)

- [ ] **Core message test** — does every paragraph advance the `Core message`? Name the
      contribution of each paragraph in one clause. A paragraph with no answer gets cut.
- [ ] **Deletion test** — remove each paragraph in turn. If nothing downstream breaks and
      no information is lost, delete it permanently.
- [ ] **Order** — do the paragraphs follow the order set in `writing_template.md` §5-3?
      Do Results and Discussion follow the same sequence as Methods?
- [ ] **Coverage** — is any claim in the section left unsupported, and is any collected
      source left unused for no reason?
- [ ] **Question-answer closure** — does Discussion answer the Introduction's primary
      question at the same scope and with results actually reported?
- [ ] **Methods-Results map** — does every reported analysis have a Methods basis, and
      does every promised method have a result or an explicit explanation for omission?
- [ ] **Venue fit** — do structure, length, abstract form, references, and disclosure follow
      the current target-venue guidance? If the venue is unresolved, label these checks provisional.

### Local pass (language)

- [ ] Sentences carrying two claims are split (Rule 6)
- [ ] Wording that adds no information is cut (Rule 7)
- [ ] Reporting verbs are varied and match the cited author's stance
- [ ] Terms unfamiliar to the `Target reader` are unpacked at first use
- [ ] Tense and terminology are consistent across the whole section, and the English and
      Korean versions still say the same thing
- [ ] Causal scope, generalization, and certainty remain within what the design and evidence support

Record what changed in this pass — it feeds A) Approach Checklist.

---

## Verification (Phase 4)

> **Detailed procedure**: Read and follow `references/citation-and-verification.md` in its entirety.

### Verification Summary

```
Step 1: Citation-Reference matching (in-text citations <-> References)
Step 2: Selected citation-style verification (target venue; APA 7 fallback if unresolved)
Step 3: Claim-Source fidelity (does the cited work actually support the claim?)
Step 4: Source-specific verification (Knowledge original cross-check, PDF metadata, Web URL)
Step 5: Cross-section integrity and AI evidence verification
Step 6: Generate verification report (PASS / ISSUES FOUND status + issue list)
```

**Step 3 is not optional.** Steps 1-2 only prove that a citation *exists* and is formatted
correctly. They cannot catch misattribution — citing a real paper for a claim it does not
make. For every claim-citation pair, go back to the source text and confirm the source
states it. Mark anything you cannot confirm as `[unverified claim]` and report it.

### Verification Checklist
- [ ] All in-text citations exist in References
- [ ] No orphan references
- [ ] Selected citation style is documented and applied consistently
- [ ] **Each claim is supported by the source cited for it** (not just that the source exists)
- [ ] **Citations inherited from a Knowledge file were traced to their original source**,
      or are flagged as unverified secondary citations
- [ ] AI-generated or AI-transformed facts, numbers, and citations appear in an evidence
      inventory with their source and verification status
- [ ] My Data references (Figure/Table) match actual files
- [ ] **Every supplied figure/table is referenced somewhere in the text** (reverse check)
- [ ] Values read from figure images are marked approximate unless taken from raw data
- [ ] Every Methods item maps to a Result, and every Result has a Methods basis
- [ ] Discussion answers the primary research question without expanding its scope
- [ ] The Abstract is understandable without body text, figures, tables, or undefined key terms
- [ ] Current target-venue requirements were checked, or venue-dependent checks are marked provisional
- [ ] No fabrication of DOI/URL/year/author
- [ ] No verbatim sentences carried over from sources without quotation marks

---

## Output Format

> **Detailed template**: Refer to the "Output Format Details" section in `references/writing_template.md`.

For a full section-writing request, output the following 7 sections. For a narrowly scoped
request (for example, one Results paragraph or a citation check), return the requested
artifact plus only the source and verification notes needed to evaluate it.

| Section | Content |
|---------|---------|
| A) Approach Checklist | 3-8 step task summary in the requested output language(s) |
| B) Source Summary | Summary by source type + gap report |
| C) Main Text | Requested language; English followed by Korean only for bilingual output |
| D) References | Target-venue style, or APA 7 fallback when unresolved; no source-type markers |
| E) Self-Assessment | Quality checklist (self-reported — not quality assurance) |
| F) Verification Report | Reference verification report |
| G) AI Assistance Log | What this skill did and did not do + disclosure draft |

**C) Main Text is a draft, not a finished section.** Label it as such. The author decides
the argument, validates the interpretation, and owns the final wording. Where a sentence
rests on an interpretive judgement the sources do not settle, flag it inline for the author.

**E) and F) are self-reports.** A `✅ PASS` means the checks in this run found no issues,
not that the text is correct. State that alongside the verdict, and cite the file or item
that each check was verified against rather than asserting quality in the abstract.

---

## Parallel Processing (Subagent)

소스가 많을 때 Loop 2-4를 병렬로 실행하여 속도를 높인다.

### 병렬 가능 작업

| 작업 | 병렬화 | 방법 |
|------|--------|------|
| Knowledge 파일 여러 개 읽기 | Yes | 파일당 Subagent 동시 실행 |
| PDF 여러 개 읽기 | Yes | 파일당 Subagent 동시 실행 |
| My Data 분석 (Figure + Table) | Yes | 유형별 Subagent 동시 실행 |
| Web 검색 (쿼리 여러 개) | Yes | 쿼리당 Subagent 동시 실행 |
| 글쓰기 (Loop 5) | No | 소스 통합 후 순차 |
| 검증 (Phase 4) | No | 글쓰기 결과 의존 |

### 병렬 실행 조건

- Knowledge 파일 3개 이상 → 병렬 읽기 권장
- PDF 2개 이상 → 병렬 읽기 권장
- Figure + Table 동시 존재 → 병렬 분석 권장
- 소스 1-2개 → 순차 실행 (오버헤드 불필요)

### Subagent Prompt Template (Knowledge Reading)

```
당신은 학술 Knowledge 파일 분석 전문가입니다.

다음 Knowledge 마크다운 파일에서 주제 "[topic]"과 관련된
Claim + Citation 쌍을 추출하세요.

카테고리 분류:
- Theoretical Foundations
- Empirical Precedents
- Methodological Heritage
- Contextual Knowledge
- Critical Discourse

파일:
[파일 내용 삽입]

출력 형식:
| Claim | Citation | Category | Source |
|-------|----------|----------|--------|
```

---

## Constraints

### AI Accountability
- Keep argument choice, interpretation, final approval, and accountability with the author
- Record the tool, task, intervention level, verification status, and author review needed
- Check the current venue or institutional AI policy before drafting a disclosure statement
- Do not place sensitive data or copyrighted source passages verbatim in prompts or logs

### Citation Strictness
- Absolutely no fabrication of DOI/URL/year/author
- Uncertain fields: Mark as `[missing: field]`
- Web search results must include source and access date
- **Secondary citations**: Claim-Citation pairs harvested from a Knowledge markdown are
  secondhand — the Knowledge file reports what some other paper said. Before citing that
  original author, confirm the claim against the original work. If the original is not
  available, either cite it as reported (`as reported in [Knowledge source]`) or mark the
  pair `[unverified secondary citation]`. Never present an unchecked secondhand citation
  as if the original had been read.

### Interpretation Boundary
- Every causal or mechanistic statement must map to a specific Knowledge claim. Do not
  generate explanations that no source supports.
- Where an interpretation is needed but no source covers it, do not invent one. Write
  `[interpretation needed — no supporting source]` and let the author supply it.
- Do not strengthen a source's claim. Preserve its hedging level (see section_guides.md
  hedging table).

### Quality Standards
- Use claim-based citation coverage; do not impose a paragraph-level citation quota
- No over-reliance on a single source
- Prefer direct, methodologically suitable original evidence; seek independent corroboration
  when it materially strengthens the claim
- Cite selectively — support the claims that carry the argument. Do not pile on citations
  for their own sake, and do not cite for statements the field treats as self-evident

### My Data Handling
- Do not cite original data as if it were prior literature
- Maintain accurate Figure/Table numbers
- Do not arbitrarily alter data values
- Prefer supplied statistics. Do not introduce derived values or recompute analyses unless
  the user explicitly requests calculation; when requested, disclose and verify every
  arithmetic derivation against the supplied values
- **Values read off a figure image are approximations.** If raw data (CSV/Excel) exists,
  take numbers from it. Numbers read only from an image are written with `~` and must be
  confirmed by the author before they stand as reported values. If axis labels, units, or
  the legend are unclear, ask — do not estimate.

---

## References File Guide

| File | When to Reference | Content |
|------|-------------------|---------|
| `references/writing_template.md` | Phase 2-3 | 5-Loop detailed procedure, source-specific handling, output format details |
| `references/section_guides.md` | Phase 3, 3.5 | IMRaD section-specific structure, transitions, examples, figure/table interpretation |
| `references/citation-and-verification.md` | Phase 4 | Venue-aware citation formatting with APA 7 fallback, claim-source fidelity, verification procedure, report template |
| `references/codex-process.md` | Planning, drafting, revision | Revision staging, outlining, and core-question rules |
| `references/codex-paragraph-logic.md` | Drafting, revision, verification | Paragraph function, reader calibration, terminology, claim strength, and reasoning audit |
| `references/codex-section-structure.md` | Section work and cross-section checks | Introduction, Abstract, Results, Discussion, venue, and Methods-Results rules |
| `references/codex-ai-era.md` | All AI-assisted drafting and submission | Human accountability, factual verification, and policy-based disclosure |

---

**Version**: 1.3.0-codex
