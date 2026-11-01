# Cross-Section Manual: Structural Integrity

> **Theoretical basis:** Swales (1990, 2004) CARS; Mensh & Kording (2017) C-C-C at
> paper scale; Perneger & Hudelson (2004); Ecarnot et al. (2015)

---

## What This File Covers

Every other manual file judges a passage against a standard **internal** to its
section: does this Introduction move correctly, does this sentence flow, is this
number reported completely. This file judges the **correspondences between
sections** — whether what the paper promises in one place is delivered in another.

`quantitative_integrity.md` already does this for numbers (an N in Methods must
match the N in Results). This file does it for **claims, questions, and
structure**.

These defects are invisible at paragraph scale. A Discussion paragraph can be
flawless prose and still fail because it answers a question the Introduction
never asked. **Mode 1 (full draft) must run these checks; Mode 2 runs the ones
where the counterpart section is available; Mode 3 cannot run them at all** —
say so rather than implying the paragraph passed.

---

## 1. The Question Chain

The single research question is the paper's organizing spine. Trace it end to end.

- [ ] **Is the research question stated explicitly as a sentence?** Not implied by
      the topic, not left for the reader to assemble. Absent = HIGH.
- [ ] **Is the stated purpose specific enough to be checked?** "We describe what we
      did" and "we explored issues related to X" are tautological or vague; a usable
      purpose names what was measured and by what means.
- [ ] **Does the Discussion answer that question**, in the same terms it was asked?
      A Discussion that opens on a different axis than the Introduction's question
      signals the argument drifted during writing.
- [ ] **Does the Conclusion answer it again, consistently?** Conclusions that
      quietly answer a broader or narrower question than the Introduction posed are
      a common late-draft artifact.
- [ ] **Is the gap claimed in the Introduction addressed in the Discussion?** The
      paper asserted something was missing; it should say what it contributed to
      that gap — and, where it did not close it, say that too.

**Flag template:**
`**[질문 사슬 불일치]** 서론의 연구 질문은 [A]인데 논의는 [B]에 답하고 있습니다.`

---

## 2. Methods ↔ Results Correspondence

A strict one-to-one relation, checkable mechanically.

- [ ] **Every result has a method.** A test, model, or measurement reported in
      Results but never described in Methods = HIGH. The reader cannot evaluate
      what they cannot see the procedure for.
- [ ] **Every method has a result.** A procedure described in Methods with no
      corresponding outcome anywhere = MEDIUM. Either the result was dropped
      (selective reporting) or the method description is vestigial.
- [ ] **Order matches.** Where Results follow a different sequence than Methods,
      ask whether the ordering is deliberate (importance-driven ordering is
      legitimate — see `sections/04_results.md`) or accidental. Flag only when the
      mismatch makes the paper harder to follow, not on principle.

**Build the correspondence table before judging:**

| Method described | Result reported | Status |
|---|---|---|
| [procedure] | [outcome] | paired / result-without-method / method-without-result |

---

## 3. Hypothesis → Analysis → Interpretation Parallelism

Where the paper states hypotheses or objectives as an enumerated set:

- [ ] Are they addressed in Results **in the same order** they were introduced?
- [ ] Does the Discussion treat each one, or does a hypothesis silently disappear?
- [ ] Are competing or alternative hypotheses acknowledged where the design allows
      them?

A dropped hypothesis is the structural equivalent of a dropped result. Flag
MEDIUM; ask whether the omission is intentional rather than asserting error.

---

## 4. Abstract ↔ Body Correspondence

The Abstract circulates independently, so it must be true to the paper on its own.

- [ ] Does every method mentioned in the Abstract have a corresponding result there?
- [ ] Does the Abstract's conclusion follow from the Abstract's own results — and
      match the body's conclusion?
- [ ] Are the Abstract's numbers identical to the body's? (Route numeric mismatches
      to `quantitative_integrity.md`; they are CRITICAL there, not stylistic here.)
- [ ] Does the Abstract claim a scope the body does not deliver?

Abstract-body drift is usually a **revision artifact**: the body was revised, the
Abstract was not. When you find one instance, check the rest of the Abstract.

---

## 5. Proposition-Level Consistency

`cohesion_flow.md` §5 (Banana Rule) enforces consistency of **terms**. This checks
consistency of **statements**.

- [ ] **Is the core contribution phrased consistently** across Title, Abstract,
      Introduction purpose, Discussion opening, and Conclusion? Not word-identical,
      but the same scope and the same strength. A purpose that is "assess the
      feasibility of X" in the Introduction and "demonstrate that X works" in the
      Conclusion has silently escalated.
- [ ] **Self-contradiction between sections.** Does any statement contradict
      another — a limitation acknowledged in Discussion but denied in Conclusion, a
      result described as preliminary in one place and definitive in another? = HIGH.
- [ ] **Circular support.** Is any claim supported by a restatement of itself
      rather than by evidence? Common in Discussion paragraphs that paraphrase the
      claim in place of arguing it.

**Flag template:**
`**[명제 불일치]** [섹션 A]의 "[진술]"과 [섹션 B]의 "[진술]"이 범위/강도에서 어긋납니다.`

---

## 6. Scope Discipline

- [ ] **Sample-to-population drift.** Does an observation made on the studied
      sample get restated as a general property? "20 of 25 sites showed X" becoming
      "X occurs at 80% of sites" changes an observation into a population estimate.
      = HIGH. This is distinct from the causal over-claiming that
      `sections/06_discussion.md` already covers — the claim can be correctly
      non-causal and still over-generalized.
- [ ] **Focus pruning.** Are results, tables, or figures included that the research
      question does not require? Comprehensiveness is not a virtue when it dilutes
      the argument; flag MEDIUM and name what could be moved to supplementary.

---

## Reviewer Notes

- These checks require **both** counterpart sections in context. If only one is
  available, report the check as not run — do not infer the counterpart's content.
- Prefer questions to assertions when the mismatch could be deliberate. "Results
  follow a different order than Methods — is this intentional?" is more useful than
  flagging an error, because importance-ordering and hypothesis-ordering are both
  defensible.
- Do not manufacture the missing side. If Methods lacks a procedure that Results
  needs, flag the gap; never draft the procedure into a rewrite candidate.
