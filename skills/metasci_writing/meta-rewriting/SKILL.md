---
name: meta-rewriting
description: >
  One-shot academic paragraph review and rewrite. Use when the user gives
  a paragraph and wants it rewritten ("이 단락 다시 써줘"), or wants its
  logic and clarity checked ("이 단락 논리 봐줘").
allowed-tools: [Read, Glob]
---

# Meta-Rewriting — One-Shot Paragraph Review & Rewrite

Take ONE paragraph, diagnose it on your own academic judgment (no reference
paper, no style databank), and deliver the full five-block output below in a
single response. If the user pastes several paragraphs, deliver the full
five-block output for the FIRST paragraph only, then offer "다음 단락" in
⑤ — one paragraph per response keeps each review readable.

**Language rule:** all commentary and diagnosis in Korean (한국어); the
rewritten paragraphs are ALWAYS in English — the user writes English
academic papers, so even a Korean draft gets English rewrites.

**No fact-checking:** take the draft's data and citations as given. If
something looks factually suspect, one brief note in ② is enough; move on.

## Input

- Pasted text → use as-is.
- File path (+ optional paragraph number) → Read the file, locate the
  paragraph, confirm the target in one line before proceeding.

## Output — five blocks, one response

### ① 의도 요약

State the paragraph's core claim and its role (2-3 lines, Korean). This is
your reading, offered for orientation — do not stop to ask for confirmation;
the user will correct you if it is off.

### ② 논리 흐름·명확성 논의

Free prose in Korean — this is the heart of the review, so discuss openly
rather than filling a form. Cover whatever genuinely matters for THIS
paragraph, typically:

- claim-evidence linkage: does each assertion have visible support?
  Results-style paragraphs read best as question → data/logic → answer.
- logical gaps or jumps between sentences; unstated premises
- information flow (old-before-new): each sentence should open with what
  the reader already knows and land its new point at the end, where
  emphasis naturally falls — readers must otherwise hold the new
  information in memory until they find its anchor. Check the topic
  string: the openings of the sentences should stay within one small set
  of related ideas; random topic shifts read as drift.
- ambiguous referents ("this", "these results", "such effects"): a
  referent with two plausible antecedents is automatically 高 — readers
  have no repair strategy for it.
- hedging calibration, in BOTH directions: the academic norm is
  mid-strength ("suggests", "indicates"). Flag bare "proves/demonstrates"
  AND hedge-stacking ("seems to suggest that ... could") — and remember
  that omitting a hedge is itself the most common intensifier.
- sentence-level clarity: are the main actors the grammatical subjects,
  and the key actions the verbs? Nominalizations in subject position are
  the telltale sign of turgid prose.
- paragraph shape (context–content–conclusion): first sentence sets the
  topic, last sentence states what the reader should carry away; one
  point per paragraph, each sub-topic handled in one place only.

Quote the actual problem phrases when you discuss them.

*(Grounding: Gopen & Swan 1990; Williams & Bizup, Style; Clark & Haviland
1977; Halliday & Hasan 1976; Mensh & Kording 2017 — full verified notes in
references/principles.md; read it only if the user asks for the sources.)*

### ③ 문장별 진단 표

Number the sentences, then table ONLY the sentences with findings, in
sentence order:

| # | 문제 | 심각도 |
|---|---|---|
| 2 | 주어가 불명확 — "It"이 가리키는 대상이 두 가지로 읽힘 | 中 |

Severity scale: 高 / 中 / 低. Close the table with one line naming the
clean sentences: "문장 1, 4 — 수정 불필요." If no sentence is clean, write
"수정 불필요 문장: 없음."

### ④ 리라이팅 3안

Three complete, self-contained paragraphs — each usable as-is, none a
sketch. Label each with a 1-2 line change summary (Korean):

- **A안 — 최소 수정**: keep the sentence order; polish wording, referents,
  and hedging only.
- **B안 — 재배치**: reorder, merge, or split sentences; rebuild transitions
  so the logic reads in sequence.
- **C안 — 재구성**: re-derive the argument structure from the intent in ①
  and rewrite freely.

**Preservation guardrail (applies to all three):** carry over every data
point (values, units, uncertainties), every citation, and every
figure/table number verbatim. Claims, however, may be recalibrated —
hedging strength, scope, causal language — whenever ②'s diagnosis flags
them as overclaimed, overgeneralized, or unsupported by the evidence in
the paragraph; logic and clarity outrank literal preservation. Name each
such recalibration in that alternative's change summary.

**Priority when principles collide:** the paragraph's information flow
(old-before-new cohesion) outranks the polish of any individual sentence —
"a passage's overall cohesion trumps the clarity of individual sentences"
(Williams & Bizup).

### ⑤ 다음 행동

One closing line: *"A/B/C안 채택" · "특정 안 수정 요청 (예: B안에서 마지막
문장만)" · "다음 단락"*

## Completion criterion

The response is complete only when every sentence is either in the
diagnosis table or named in the 수정 불필요 line, AND all three
alternatives are full paragraphs.

## Follow-up turns

- **채택** ("A안으로") → output that version alone, clean and copy-ready.
- **부분 수정** ("B안에서 두 번째 문장만 바꿔줘") → revise that alternative
  only and re-present it; keep the other two untouched.
- **새 단락** → run the five blocks again from ①.
