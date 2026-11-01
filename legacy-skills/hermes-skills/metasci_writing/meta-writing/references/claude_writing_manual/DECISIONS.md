# Open Decisions

**Three of the five listed here are open. Two are settled — D2 and D3 — and must not be
put to the user as choices.** The 2026-08-10 contradiction audit (`DIAGNOSTIC-MAP.md`) found that
`meta-proofreading/writing-manual/` already answers both, on better evidence than the corpus holds.

| | Question | Status |
|---|---|---|
| D1 | Abstract length | **Open** — venue-bound. Ask. |
| D2 | First person | ✅ Resolved — use it for decisions, interpretations, arguments |
| D3 | Assertion vs hedging | ✅ Resolved — mid-strength ("suggests", "indicates") |
| D4 | Title length | **Open** — venue-bound. Ask. |
| D5 | Abstract voice / sentence form | **Open** — field-bound. Ask. |

The three that remain open are open because the answer is *whatever the target venue does*, not
because the evidence is contested. Merging them would mean inventing a norm no source states.

**Protocol for any consuming skill:**

1. Detect that the draft touches one of these three questions.
2. **Ask the user.** Present both sides with their sources.
3. Apply the answer for this manuscript only. Do not persist it as a global default.
4. If the user declines to answer, say which side you are applying and why — never apply one silently.

There is no default value in this file, deliberately. A skill that picks a side without asking
is inventing a norm the evidence does not support.

---

## D1 — Abstract length

| | Position | Source | Verbatim |
|---|---|---|---|
| **A** | 100–150 words maximum | `b5-schulzrinne` *Writing Systems and Networking Articles* (Columbia) | "Abstract, typically not more than 100-150 words" |
| **B** | 200–300 words, use the allowance | `tullu-2019` *Saudi J Anaesth* | "Most journals allow 200–300 words for formulating the abstract and it is wise to restrict oneself to this word limit." |

**Warning about the bank.** `section-structure-22` merged these into "typically 150–300 words."
**Neither source says that.** The merge averaged two incompatible norms into a range that exists
in no source. Treat `section-structure-22`'s number as an artifact, not evidence.

**What actually separates them:** venue type. A is a CS/systems conference guide; B is a
biomedical journal guide. The disagreement is real but field-bound.

**Ask:** *"What is the target venue's abstract word cap?"* The journal's own author instructions
override both sources — that rule is itself the highest-convergence principle in the corpus
(`section-structure-2`, convergence 13). If the venue is unknown, ask whether this is a
CS/engineering conference paper or a journal article in the life/health sciences.

---

## D2 — First person — ✅ RESOLVED 2026-08-10, do not ask

**This is no longer an open question.** `meta-proofreading/writing-manual/` takes a definite
position, grounded in Hyland's metadiscourse corpus work and Sword:

> "**Never avoid first person purely for stylistic reasons.** Interpreting results, making arguments,
> and explaining decisions all belong in active first person: 'We interpret,' 'We chose,' 'We argue.'"
> — `cross_section/sentence_craft.md`
>
> "Use first person for decisions, interpretations, and arguments. Use passive for standard
> procedures." — `cross_section/stance_hedging.md`
>
> Avoiding first person entirely creates what Sword calls **"zombie prose"** — text where no one takes
> responsibility for intellectual claims.

**Apply that.** Still check the target journal for an explicit prohibition, but do not present this
to the user as an open choice.

**Why it was listed as contested:** within the 27-source corpus it genuinely is. But the two sides
are not evidentially equal — see the record below. A disagreement inside a corpus is not a
disagreement in the field when one side has materially better support just outside it. See
`DIAGNOSTIC-MAP.md`.

<details>
<summary>Original corpus record (kept for provenance)</summary>

| | Position | Source | Verbatim |
|---|---|---|---|
| **A** | Permitted, and preferable for aims/methods/structure | `b3-lund` *Writing in English at University* | "In many fields, the first-person pronouns I, my and me are perfectly acceptable to use in an academic essay or research paper, especially when announcing the purpose or aims of the essay and when forecasting structure." |
| **A** | Permitted | `b5-schulzrinne` | "use I, we and you" |
| **B** | Avoid unless the field allows it | `tweets-02` | "Don't write in first person unless your field specifically allows it. \"This study shows\" works better than \"I found.\"" |
| **B** | Avoid | `b6-fess` *Academic Writing Handbook for FET Learners* | — |

**Bank entry:** `paragraph-logic-17` already carries a source-tension flag. It does not resolve it.

**Note on evidence weight:** side B's strongest voice is a tweet corpus, and side A includes two
institutional guides. This does not settle the question — field convention does — but it is
worth stating when presenting the choice.

Side B's strongest voice is a tweet corpus; `b6-fess` is an Irish further-education handbook for
FET learners, not a research-writing source. Side A is two institutional university guides. That
imbalance is what the 2026-08-10 audit acted on.

</details>

---

## D3 — Assertion vs hedging — ✅ RESOLVED, do not ask

| | Position | Source |
|---|---|---|
| **A** | Assert strongly; weak statements read as weak research | `hengl-2002` |
| **B** | Hedge — limit claims to what the evidence supports | `b3-lund`, `b6-fess` |

**This one has a better-evidenced third answer outside the corpus.**
`~/.claude/skills/meta-rewriting/references/principles.md` (22 sources, 3 independent verifiers
per claim) resolves it more precisely than either bank side:

- The academic norm is **mid-strength** — not "proves", not "seems to suggest that certain… could".
  Use "suggests" / "indicates".
- **"The most common intensifier is the absence of a hedge."** Diagnosis must therefore run in
  **both** directions: over-claiming (add a hedge) *and* over-qualifying (remove one).
- Crick & Watson hedged: "We wish to suggest **a** [not **the**] structure."

**Apply the mid-strength position.** Both diagnostic assets converge on it independently —
`principles.md` via Williams & Bizup, `writing-manual/cross_section/stance_hedging.md` via Hyland's
hedge/booster taxonomy. Cite whichever is loaded. Do not present this as an open choice; the corpus
disagreement was between one field-specific guide and two general handbooks, and better-evidenced
work outside the corpus settles it.

Field-specific hedging intensity still varies — but that is calibration within the mid-strength
position, not a choice between assertion and hedging.

---

## D4 — Title length

| | Position | Source | Verbatim |
|---|---|---|---|
| **A** | 7–10 words | `hengl-2002` *Rules of Thumb for Writing Research Articles* | "short and simple (7-10 words); purposive" |
| **B** | about 10–15 words | `tullu-2019` *Saudi J Anaesth* | "edit the title (thus drafted) to make it more accurate, concise (about 10–15 words), and precise" |

The ranges barely overlap, and both sources are giving a hard number rather than a principle.
`ecarnot-2015` adds only that the target journal may impose its own word or character limit and
that "keeping it short is harder than coming up with a 4-line title."

**Ask:** *"Does the target journal cap the title length?"* If it does, that setting decides. If it
does not, ask which convention the field follows — the two sources come from different disciplines.

## D5 — Abstract voice and sentence form

| | Position | Source | Verbatim |
|---|---|---|---|
| **A** | Phrases rather than sentences; **avoid the passive** | `tullu-2019` | "use phrases rather than sentences to draft the content of the abstract, and avoid passive voice" |
| **B** | Past (perfect) tense and **passive voice** | `hengl-2002` | "past (perfect) tense and passive voice(!)" — the exclamation mark is the source's |

This is a direct contradiction on the same object, and `hengl-2002` flags its own position as
deliberate. It is also field-bound: `paragraph-logic-3` in `00_universal.md` records that the
active voice is the general default *except* where the agent is irrelevant or deliberately
backgrounded, which is exactly the case some fields make for Methods-like abstract prose.

**Ask:** *"Does your field's abstract convention use the passive?"* Check three recent abstracts in
the target journal and follow them. Do not apply the universal active-voice rule to an abstract
without checking.

---

## Why these five

D1–D3 are the conflicts the original extraction recorded as unresolved after adversarial
verification (`Writing_Principles_Extraction/README.md` §5.3). **D4 and D5 were found on 2026-08-09**
during the re-mining of `by-source/` — they had been merged away rather than recorded, which is the
same over-merge that thinned the section files.

If a consuming skill finds a sixth genuine conflict, it belongs here — do not resolve it in place.
