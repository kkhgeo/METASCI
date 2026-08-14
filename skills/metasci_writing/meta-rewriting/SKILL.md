---
name: meta-rewriting
description: >
  One-shot academic paragraph review and rewrite. Use when the user gives
  a paragraph and wants it rewritten ("이 단락 다시 써줘"), or wants its
  logic and clarity checked ("이 단락 논리 봐줘").
  Works on academic judgment alone — no reference papers, no style profile. With
  extracted reference files to compare against use meta-review; for Monte Carlo
  optimization over many references meta-rewriting-loop; for a multi-reviewer panel
  meta-proofreading; for style-profile application meta-styling; for applying
  the user's own Korean voice meta-mywriting-korean; for AI-trace removal
  meta-rewriting-antiai; for section order and outline meta-writing-mapping.
allowed-tools: [Read, Glob, AskUserQuestion]
---

# Meta-Rewriting — One-Shot Paragraph Review & Rewrite

Take ONE paragraph, diagnose it on your own academic judgment (no reference
paper, no style databank), and deliver the full six-block output below in a
single response. If the user pastes several paragraphs, deliver the full
six-block output for the FIRST paragraph only, then offer "다음 단락" in
⑥ — one paragraph per response keeps each review readable.

**Language rule:** all commentary and diagnosis in Korean (한국어). The
rewritten paragraphs follow **the language of the source** — an English
paragraph gets English rewrites, a Korean one gets Korean rewrites — unless
the user asks otherwise, which overrides. The user writes both English
manuscripts and Korean papers and reports, so say in ① which language you
are rewriting into, and offer the switch in ⑥.

**No fact-checking:** take the draft's data and citations as given. If
something looks factually suspect, one brief note in ② is enough; move on.

## Input

- Pasted text → use as-is.
- File path (+ optional paragraph number) → Read the file, locate the
  paragraph, confirm the target in one line before proceeding.
- **Section type.** The user normally states it ("Results 단락이야"). If they
  did not, and the text does not make it unmistakable, ask before producing
  the output — one AskUserQuestion listing the section types, with **보고서
  본문** among them for Korean reports. Do not guess, and do not treat
  skipping the section-specific checks as the convenient default: the reason
  to ask is that every applicable block then gets run.

## Output — six blocks, one response

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

**Over-correction brakes — refuted claims, never apply them as rules:**

- ❌ *"Subject and verb must be as close as possible; intervening material of
  any length is a burden."* Refuted under verification — short interruptions
  cost the reader nothing. Flag long ones only.
- ❌ *"Add connectives to improve flow."* Cohesion is not coherence (Cooper
  1988): cohesive ties are surface devices, and adding them does not make an
  incoherent argument coherent. Repair the logic first, and add a connective
  only where the relation it names is already true.
- ❌ *"Correct the sentence to standard form."* Grammaticality is not
  communicative function (Kuo 1995): two equally grammatical sentences carry
  different value depending on placement and information structure. Judge a
  sentence in its discourse context, not by grammar in isolation.

These matter more, not less, as the target moves toward "a perfect
paragraph" — a reviewer pushed toward perfection over-corrects, and
over-correction is the one defect the author has no way to see.

**Checklist reads — three tiers, each with its own trigger:**

1. *Always.* Read `references/section-checklists.md` and apply its
   section-independent blocks — 문장 스타일 공통 and 인용·참고문헌 규범.
   These hold for any academic paragraph, so they run even when you cannot
   tell which section the paragraph came from.

   **Branch on the source language.** 문장 스타일 공통 is written for English
   prose. When the source paragraph is **Korean**, additionally read
   `references/korean-register.md`, which names the English-only items to
   drop, gives the Korean surface forms of the ② checks, and — most
   importantly — forbids over-correcting the Korean academic register.
   When the source is **English, do not open that file**: nothing in it
   applies, and its "normal range" statements are false for English prose.
   인용·참고문헌 규범 and every section-specific block are language-neutral
   and run either way.
2. *Once the section is known.* With the section type in hand — stated by
   the user, unmistakable from the text, or obtained by asking (see Input) —
   check the paragraph against that section's own block **in full, every
   item**, not a sample. Skipping the section block is the fallback for the
   single case where the user declined to say and the text will not tell
   you; it is not the normal path.

3. *Only on demand — the evidence layer.* `section-checklists.md` compresses
   its grounding to source names (`[1차: Ecarnot 2015]`) and carries no
   quotable sentences. When the user asks **why** a rule holds, wants the
   source, or needs something citable, read the matching section file in
   `../meta-writing/references/claude_writing_manual/` — `00_universal.md`
   plus the one section file, never the whole folder. Each entry there has
   a verbatim quote, its supporting sources, and its verification status.
   Do not load it for ordinary diagnosis; the checklist is faster and
   better tuned for that.

**Contested rules — ask, never default.** Three questions are venue-bound
rather than evidentially settled: **abstract length, title length, abstract
voice.** If the paragraph turns on one, stop and ask (target journal, field
convention), then say which you applied. Two others are already settled and
are stated as decisions rather than offered as options: **first person** —
used for decisions, interpretations, and arguments — and **claim strength** —
mid-range, "suggests" / "indicates".

Both lists live in `claude_writing_manual/DECISIONS.md`, with the positions
and their sources; `DIAGNOSTIC-MAP.md` records why the two were settled. Read
`DECISIONS.md` when you need to put both sides of an open question to the
user. Keeping the content there rather than here means one edit when it
changes, not one per skill.

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

### ④ 대안 4안

Four complete, self-contained paragraphs — each usable as-is, none a sketch.
They form a **ladder**: every rung keeps less of the original than the one
above it. Label each with a 1-2 line change summary (Korean).

| 안 | 바꾸는 것 | 원문에서 남는 것 |
|---|---|---|
| A 최소수정 | 어휘·지시어·헤징 | 문장과 순서 |
| B 재배치 | 문장 순서·병합·분할 | 문장 |
| C 재구성 | 논증 구조 | 내용 요소 |
| D 재작성 | 전부 | ①의 의도 |

- **A안 — 최소수정**: keep the sentence order; polish wording, referents,
  and hedging only. Sentences you named clean in ③ stay untouched —
  "minimal" means minimal, and rewriting what already works is how a
  review loses the author's trust.
- **B안 — 재배치**: reorder, merge, or split sentences; rebuild transitions
  so the logic reads in sequence. The sentences remain the author's.
- **C안 — 재구성**: re-derive the argument structure — what is claimed, what
  supports it, in what order — and write the sentences that structure needs.
  The content elements are the author's; the prose is yours.
- **D안 — 재작성**: keep only the intent stated in ①, and write the paragraph
  from scratch as though drafting it for the first time.

Do not let the rungs drift toward each other. If B reads as A with two commas
moved, or D as C with synonyms swapped, the ladder has collapsed and the
author has been handed one option four times. Each rung must be visibly a
different answer to "how far do I go?"

**Preservation guardrail (applies to all four):** carry over every data
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

**Adding sentences is allowed.** Cutting is not the only repair. Where ②
found a logical gap, an unsupported claim, or a missing required element of
the section, an alternative may add the sentence that closes it. Two limits,
both absolute: never invent a data point, a citation, a figure or table
number, or a numeric magnitude; and where the added sentence needs evidence
the paragraph does not contain, write the sentence with a **`[근거 필요]`**
marker standing in for that evidence rather than supplying it yourself. Name
every addition in the change summary. Higher rungs will naturally add more —
A안 rarely adds anything, D안 may add several.

Note also what this skill does **not** check: whether the citations and
numbers are real. It carries them over verbatim, so if the draft was
itself AI-generated, a fabricated citation survives into all four
alternatives untouched. Verifying sources against the originals stays with
the author.

**No verdict in this block.** Build all four rungs at full effort and pass
judgement in ⑤. Whether the original beats them is a real question, but it
is answered after the work, not before it.

**Priority when principles collide:** the paragraph's information flow
(old-before-new cohesion) outranks the polish of any individual sentence —
"a passage's overall cohesion trumps the clarity of individual sentences"
(Williams & Bizup).

### ⑤ 완성본

One paragraph, presented as the recommendation — and **not a fifth draft.**
Name which rung of ④ it is, or name the merge explicitly ("B안 골격 + C안의
3–4문장"). If passing the checklist required touching anything beyond that,
say what you changed and why. The author must always be able to trace the
final text back to a rung of ④.

Then the pass check. List the checks you actually ran and their result, so
that a skipped one is visible rather than silently absent:

| 검사 | 결과 |
|---|---|
| 간결성 4결함 (강조부사·클리셰·메타담화·장황구문) | 통과 |
| 만연체·문장 길이 변주·run-on | 통과 |
| 격식 레지스터 (축약형·비격식어·객관 톤) | 통과 |
| 지시어·정보 흐름·헤징 강도 | 통과 |
| 논증 타당성·단락 내부 일관성 | 통과 |
| 인용·참고문헌 규범 | 통과 |
| \<섹션\> 필수 요소 | 통과 |

The rows come from the blocks you were required to read, so the last row
names the actual section. A row you cannot settle from the paragraph alone
is marked **확인 불가** with the reason — never 통과.

For a **Korean** source, take the first three rows from `korean-register.md`
§B instead, and add its §A as one further row named **과잉교정 회피**. Both
row sets live in that file rather than here, so that an English review never
loads a Korean register standard. The remaining rows are unchanged; they were
never English-specific.

**The original may be the best version — decided here, not earlier.** Having
written all four alternatives and set them against the original, say plainly
if the original wins, or if the honest gain is confined to 低-severity
polish. This judgement belongs at this point in the response and nowhere
before it: placed in ④ it would license four half-hearted alternatives,
whereas placed here it is a verdict reached after the work. Your rewrites are
your own output, and there is no reason to assume they beat what the author
wrote — a model asked for rewrites produces them whether or not they improve
anything. When the original wins, ⑤ says so and reproduces the original as
the recommendation.

### ⑥ 다음 행동

One closing line: *"완성본 채택" · "A/B/C/D안 채택" · "원문 유지" · "특정 안
수정 요청 (예: C안에서 마지막 문장만)" · "다른 언어로 리라이팅" · "다음 단락"*

Add one more line naming the recurring defect type in this paragraph
(예: "이번 단락의 반복 결함: 모호한 지시어 3건"). Over several paragraphs
these lines accumulate into the author's own checklist, which is worth more
than any single review.

## Completion criterion

The response is complete only when every sentence is either in the
diagnosis table or named in the 수정 불필요 line, AND all four alternatives
are full paragraphs, AND ⑤ names the rung it came from and carries the
pass-check table with no row left out.

## Follow-up turns

- **채택** ("완성본으로", "C안으로") → output that version alone, clean and
  copy-ready.
- **원문 유지** → confirm in one line; do not re-argue for your rewrites or
  produce a fifth alternative.
- **부분 수정** ("C안에서 두 번째 문장만 바꿔줘") → revise that alternative
  only and re-present it; keep the others untouched. If the revision changes
  what ⑤ recommended, re-state ⑤ as well.
- **언어 전환** ("영문으로도 줘") → re-render the adopted version, or ④ and ⑤
  if none is adopted yet, in the requested language. The diagnosis in ②③ is
  not re-run: it was made on the source and does not change with the output
  language. Say which register checks now apply instead.
- **새 단락** → run the six blocks again from ①.

---

**Version**: 1.3.0
