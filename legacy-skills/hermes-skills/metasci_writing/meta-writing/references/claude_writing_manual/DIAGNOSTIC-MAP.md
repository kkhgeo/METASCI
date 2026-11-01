# Two diagnostic assets — how they relate

Two independent bases diagnose academic prose in this installation. They were built from different
corpora, by different runs, and until 2026-08-10 neither referenced the other. This file states the
relationship so they do not drift apart or contradict each other.

| | `meta-rewriting/references/` | `meta-proofreading/writing-manual/` |
|---|---|---|
| Size | `section-checklists.md` 137 items + `principles.md` 8 principles | 15 files, ~99 KB |
| Unit | ONE paragraph, one response | Paper / Section / Paragraph (3 modes, reviewer panel) |
| Tools | `Read, Glob` only — deliberately light | Agents, knowledge distribution, judge, reference verification |
| Form | `- [ ]` binary checks | Move tables, rhetorical function, agent checklists |
| Grounding | Perneger, Ecarnot, Tullu, Schulzrinne, IUFRO, Fisher + Gopen&Swan, Williams&Bizup, Mensh&Kording | Swales CARS, Yang & Allison, Kanoksilapatham, Hyland metadiscourse, Daneš, Gopen&Swan, Williams&Bizup |

**They overlap on exactly one unit: a single paragraph.** `meta-rewriting` is the fast pass;
`meta-proofreading` Mode 3 is the panel pass on the same object. The difference is cost and depth,
not scope — so a user may legitimately run both on the same text and must not get contradictory
advice.

## Precedence

1. **Theory of reading** — `principles.md` (given-new, topic/stress position, characters-as-subjects)
   and `writing-manual/cross_section/` are two renderings of largely the same literature. Where they
   overlap, prefer whichever is loaded; they do not conflict.
2. **Section norms and genre** — `writing-manual/` governs. It is built on move-analysis literature
   (Swales, Yang & Allison, Kanoksilapatham) that the `section-checklists` corpus does not contain.
3. **Fast binary diagnosis** — `section-checklists.md` governs, because that is what it is shaped for
   and `meta-rewriting` cannot afford to load 99 KB.
4. **Evidence and quotation** — this folder governs. Neither diagnostic asset carries a quotable
   sentence with a page location and verification status.

## Contradiction audit (2026-08-10)

Checked on the axes most likely to conflict.

| Axis | `section-checklists` / `principles` | `writing-manual` | Verdict |
|---|---|---|---|
| Active vs passive | "능동태 기본값 … 단 old 정보를 앞으로 보내는 수동태는 정당. '수동태 금지'를 기계 적용하지 말 것" | "Voice choice should be driven by **what belongs in the topic position** — not by a rule about active vs. passive." | **Convergent.** Same reasoning, same root (Gopen & Swan). No action. |
| Hedging | "진단은 양방향 — 과잉 주장과 과잉 완화 모두" (Williams & Bizup Lesson 9) | Hedges / boosters / stance calibration (Hyland 2005) | **Convergent.** |
| Nominalization, tense, topic sentence | present in both | present in both | **Convergent.** |
| **First person** | listed as *unresolved* in `DECISIONS.md` §D2 | **takes a position** — "Never avoid first person purely for stylistic reasons"; avoiding it yields Sword's "zombie prose" | **Conflict — resolved in favour of `writing-manual`.** See below. |

No contradiction was found that requires either asset to change. One of *this folder's* open questions
turned out not to be open.

## What the audit changed here

`DECISIONS.md` §D2 (first person) and §D3 (assertion vs hedging) were downgraded from *unresolved*
to *resolved outside the corpus*.

The 27-source corpus does disagree with itself on both. But the disagreement is an artifact of what
that corpus contains: the "avoid first person" side rests on a tweet thread and an Irish
further-education handbook, while the "use it" side is backed by Hyland's metadiscourse corpus work
and Sword. A conflict inside a corpus is not a conflict in the field when one side has materially
better evidence sitting just outside it.

**Three questions stay genuinely open** — D1 abstract length, D4 title length, D5 abstract
voice/sentence form. All three are venue-bound rather than evidentially contested: the answer is
whatever the target journal does. Ask; never default.

## Drift control

- Neither asset should be edited to match the other. They are separate renderings for separate costs.
- When one gains a check the other lacks, decide deliberately whether it belongs in the fast pass.
  The 2026-08-10 back-port added 37 items to `section-checklists.md`; 8 of the concepts already
  existed in `writing-manual/`, and were added anyway because `meta-rewriting` genuinely lacked them
  and cannot read the other asset.
- Re-run this audit if either asset gains a position on a contested question. The failure mode is not
  duplication — it is one asset quietly answering a question the other is still asking the user.
