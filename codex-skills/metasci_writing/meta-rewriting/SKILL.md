---
name: meta-rewriting
description: >
  One-shot academic paragraph review and rewrite. Use when the user gives
  a paragraph and wants it rewritten ("이 단락 다시 써줘"), or wants its
  logic and clarity checked ("이 단락 논리 봐줘").
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
- argument soundness — the principles above govern how information is
  *arranged*; this one asks whether the reasoning *holds*. A paragraph can
  be perfectly ordered and still argue badly. Watch for: correlation
  stated as cause; a conclusion broader than the evidence (single site,
  single run → general claim); circular support (the claim restated as its
  own reason); false dichotomy; and self-contradiction between sentences.
  Name the specific move, not just "logic is weak".
- internal consistency — within this one paragraph, is the tense stable,
  the person stable ("we" vs "the authors"), and each concept named by one
  term throughout? Switching terms for variety reads as switching
  referents. This check runs regardless of section type.
- redundancy — the diagnosis so far only asks what to *fix*. Also ask what
  to *cut*: take each sentence out in turn, and if the paragraph's claim
  and evidence survive intact, that sentence is redundant (中). Say which
  sentences failed this test.

Quote the actual problem phrases when you discuss them.

**Checklist reads — two tiers, do not conflate them:**

1. *Always.* Read `references/section-checklists.md` and apply its
   section-independent blocks — 문장 스타일 공통 and 인용·참고문헌 규범.
   These hold for any academic paragraph, so they run even when you cannot
   tell which section the paragraph came from.
2. *Only when the section is known.* If the section type is stated by the
   user or unmistakable from the text (Abstract / Introduction / Methods /
   Results / Discussion / Conclusion / thesis chapter), ALSO check the
   paragraph against that section's own block. If the section type is
   unclear, skip the section-specific block rather than guessing — but
   still apply tier 1.

Structural violations go into the ③ table (missing required element = 高).

*(Grounding: Gopen & Swan 1990; Williams & Bizup, Style; Clark & Haviland
1977; Halliday & Hasan 1976; Mensh & Kording 2017 — full verified notes in
references/principles.md; read it only if the user asks for the sources.
Section conventions: Perneger 2004, Ecarnot 2015, Nature template et al. —
references/section-checklists.md.)*

### ③ 문장별 진단 표

Number the sentences, then table ONLY the sentences with findings, in
sentence order:

| # | 문제 | 심각도 |
|---|---|---|
| 2 | 주어가 불명확 — "It"이 가리키는 대상이 두 가지로 읽힘 | 中 |

Severity scale: 高 / 中 / 低, assigned by **how global the damage is** —
a defect that misleads the reader about the argument outranks one that
merely slows them down:

- **高** — the reader takes away something wrong or cannot recover the
  meaning: unsound reasoning, a claim beyond the evidence, an ambiguous
  referent with two plausible antecedents, a missing required element of
  the section, broken information flow across the paragraph.
- **中** — the reader gets there, but pays: clumsy ordering, redundant
  sentences, inconsistent terms or tense, run-ons, table/text duplication.
- **低** — local polish: filler intensifiers, clichés, contractions,
  wordy constructions.

Fix in that order too. Rewriting a sentence that is about to be cut, or
polishing wording inside a paragraph whose logic must be rebuilt, is
wasted work.

Close the table with one line naming the
clean sentences: "문장 1, 4 — 수정 불필요." If no sentence is clean, write
"수정 불필요 문장: 없음."

### ④ 리라이팅 3안

Three complete, self-contained paragraphs — each usable as-is, none a
sketch. Label each with a 1-2 line change summary (Korean):

- **A안 — 최소 수정**: keep the sentence order; polish wording, referents,
  and hedging only. Sentences you named clean in ③ stay untouched —
  "minimal" means minimal, and rewriting what already works is how a
  review loses the author's trust.
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

Recalibrating a claim is not wordsmithing — it changes what the author
asserts. So flag it for confirmation rather than presenting it as settled:
say which claim moved, in which direction, and on what basis in the
paragraph. The author decides whether the weaker or stronger reading is
the one they meant.

Note also what this skill does **not** check: whether the citations and
numbers are real. It carries them over verbatim, so if the draft was
itself AI-generated, a fabricated citation survives into all three
alternatives untouched. Verifying sources against the originals stays with
the author.

**The original may be the best version.** These three alternatives are your
own output, and there is no reason to assume your rewrite beats what the
author wrote — a model asked to produce rewrites will produce them whether
or not they improve anything. When ② and ③ turn up nothing above 低, say so
plainly, and offer the alternatives as options rather than corrections.
Keep "원문 유지" available as an outcome in ⑤.

**Priority when principles collide:** the paragraph's information flow
(old-before-new cohesion) outranks the polish of any individual sentence —
"a passage's overall cohesion trumps the clarity of individual sentences"
(Williams & Bizup).

### ⑤ 다음 행동

One closing line: *"A/B/C안 채택" · "원문 유지" · "특정 안 수정 요청 (예:
B안에서 마지막 문장만)" · "다음 단락"*

Add one more line naming the recurring defect type in this paragraph
(예: "이번 단락의 반복 결함: 모호한 지시어 3건"). Over several paragraphs
these lines accumulate into the author's own checklist, which is worth more
than any single review.

## Completion criterion

The response is complete only when every sentence is either in the
diagnosis table or named in the 수정 불필요 line, AND all three
alternatives are full paragraphs.

## Follow-up turns

- **채택** ("A안으로") → output that version alone, clean and copy-ready.
- **원문 유지** → confirm in one line; do not re-argue for your rewrites or
  produce a fourth alternative.
- **부분 수정** ("B안에서 두 번째 문장만 바꿔줘") → revise that alternative
  only and re-present it; keep the other two untouched.
- **새 단락** → run the five blocks again from ①.

---

**Version**: 1.1.0
