<!-- owner: codex; generated: true; do-not-edit: true -->
# Codex Paragraph Logic Rules — meta-proofreading

> Canonical source: `codex_scientific_writing_kernel/rules/`
> Apply every rule together with its diagnostic check, action, and exceptions.

## SW-PARA-001 — make-every-sentence-earn-its-place

- **Rule:** Remove words and sentences that do not contribute to the claim, evidence, or essential context.
- **Rationale:** Redundant language weakens the main signal and increases the reader's processing cost.
- **Diagnostic check:** Would deleting the word or sentence leave the claim, evidence, and essential context intact?
- **Action:** Apply a deletion test, remove functionless language, and compress necessary information into a more direct form.
- **Operations:** draft, rewrite, review
- **Stages:** drafting, revision
- **Scales:** section, paragraph, sentence
- **Sections:** all
- **Severity / evidence:** medium / strong
- **Support counts:** 11 slugs, 8 independent source families
- **Evidence judgment:** Many independent guides and articles support concision; the functional deletion test limits the rule more safely than a style preference would.
- **Source-bank rule:** `paragraph-logic-1`
- **Supporting sources:** `b1-iufro`, `b5-schulzrinne`, `b6-fess`, `ecarnot-2015`, `fisher-2013`, `tullu-2019`, `connellpensky-2025`, `tweets-01c`, `tweets-01d`, `tweets-02`, `tweets-04`
- **Exceptions:**
  - Do not remove definitions, reader-oriented transitions, or reproducibility details merely to shorten the text.
  - Preserve deliberate emphasis or genre-appropriate rhythm when it performs a clear function.

## SW-PARA-002 — calibrate-clarity-to-reader

- **Rule:** Judge clarity by whether the target reader can follow the text without supplying unstated assumptions, not by the author's familiarity with the subject.
- **Rationale:** Deeply involved authors tend to underestimate the cost of omitted premises and field-specific terminology.
- **Diagnostic check:** Must the target reader guess undefined terms, omitted premises, or field-internal context to understand the passage?
- **Action:** Identify the target reader and add the minimum necessary definitions, premises, and context without overexplaining what that audience can reasonably know.
- **Operations:** draft, rewrite, review
- **Stages:** drafting, revision
- **Scales:** manuscript, section, paragraph, sentence
- **Sections:** all
- **Severity / evidence:** high / strong
- **Support counts:** 8 slugs, 5 independent source families
- **Evidence judgment:** Independent institutional guides and articles support reader calibration; explicit audience and genre exceptions reduce indiscriminate simplification.
- **Source-bank rule:** `paragraph-logic-5`
- **Supporting sources:** `b1-iufro`, `b5-schulzrinne`, `b7-nature`, `ecarnot-2015`, `tweets-01a`, `tweets-01c`, `tweets-02`, `tweets-04`
- **Exceptions:**
  - Preserve technical density in sections such as Methods when the specialist audience is clear.
  - If replacing an exact technical term would lose meaning, retain and define it at first use.

## SW-PARA-003 — calibrate-claim-strength

- **Rule:** Calibrate the scope and certainty of each claim to what the research design and evidence actually support.
- **Rationale:** Overstatement damages validity, while excessive qualification obscures conclusions that the evidence does justify.
- **Diagnostic check:** Does causal, generalizing, or definitive language exceed what the sample, design, analysis, and uncertainty permit, or does unnecessary hedging obscure a well-supported conclusion?
- **Action:** Recalibrate scope, causal language, and hedging; flag any meaning-changing revision for author confirmation.
- **Operations:** draft, rewrite, review, verify
- **Stages:** drafting, revision, verification
- **Scales:** paragraph, sentence
- **Sections:** abstract, introduction, results, discussion, conclusion
- **Severity / evidence:** high / strong
- **Support counts:** 6 slugs, 6 independent source families
- **Evidence judgment:** Multiple independent guides support two-way calibration, consistent with the existing deeper principles on hedging and claim strength.
- **Source-bank rule:** `paragraph-logic-7`
- **Supporting sources:** `b1-iufro`, `b3-lund`, `b5-schulzrinne`, `hengl-2002`, `hon-uf`, `tweets-01d`
- **Exceptions:**
  - State a conclusion directly when strong, direct evidence supports it.
  - Do not equate statistical significance with practical importance.

## SW-PARA-004 — build-functional-paragraphs

- **Rule:** Give each paragraph one central function and make the relationship among its topic, support, and landing point visible.
- **Rationale:** Readers interpret paragraph boundaries as units of argument; mixed functions weaken focus and flow.
- **Diagnostic check:** Can the paragraph's central function be stated in one sentence, does every sentence contribute to it, and does the ending land or lead forward coherently?
- **Action:** Move or delete sentences unrelated to the central function, and split or combine paragraphs when their functional boundaries require it.
- **Operations:** plan, draft, rewrite, review
- **Stages:** planning, drafting, revision
- **Scales:** paragraph
- **Sections:** all
- **Severity / evidence:** high / moderate
- **Support counts:** 5 slugs, 4 independent source families
- **Evidence judgment:** Several institutional guides support functional paragraphing, while topic-sentence position and closure remain genre-sensitive heuristics.
- **Source-bank rule:** `paragraph-logic-9`
- **Supporting sources:** `b3-lund`, `b6-fess`, `hon-uf`, `tweets-01c`, `tweets-04`
- **Exceptions:**
  - A topic sentence need not always be first when a clear rhetorical purpose justifies delaying it.
  - Do not mechanically impose a full three-part structure on a very short transitional paragraph.

## SW-PARA-005 — preserve-terminological-consistency

- **Rule:** Use the same core term for the same concept and keep the wording of research questions, objectives, and key outcomes consistent across sections.
- **Rationale:** In scientific prose, synonym variation can signal a new category or an unintended shift in scope.
- **Diagnostic check:** Is the same entity named in multiple ways, or do terms for objectives, variables, or populations change across sections and shift scope?
- **Action:** Choose a canonical term and harmonize the manuscript against a terminology list and fixed key statements while preserving genuine conceptual distinctions.
- **Operations:** draft, rewrite, review, verify
- **Stages:** drafting, revision, verification
- **Scales:** manuscript, section, paragraph, sentence
- **Sections:** all
- **Severity / evidence:** high / moderate
- **Support counts:** 5 slugs, 5 independent source families
- **Evidence judgment:** Several independent guides support consistency; because the bank also recommends synonym variation, this rule is restricted to conceptual identity.
- **Source-bank rule:** `paragraph-logic-16`
- **Supporting sources:** `b3-lund`, `b6-fess`, `ecarnot-2015`, `pautasso-2013`, `tweets-02`
- **Exceptions:**
  - Pronouns may avoid repetition when their antecedent is unique and clear.
  - Do not collapse different analytical levels or legal and technical definitions into one term.

## SW-PARA-006 — audit-argument-soundness

- **Rule:** Audit the reasoning between claims and evidence for causal leaps, hasty generalization, circularity, and self-contradiction.
- **Rationale:** Clear and cohesive prose does not produce a valid argument when the underlying inference is unsound.
- **Diagnostic check:** Does each conclusion follow from the stated evidence without ignoring counterexamples, alternative explanations, or scope limits?
- **Action:** Make premises and inferential steps explicit; remove or weaken unsupported leaps, or flag them as evidence gaps.
- **Operations:** plan, draft, rewrite, review, verify
- **Stages:** planning, drafting, revision, verification
- **Scales:** manuscript, section, paragraph
- **Sections:** introduction, results, discussion, conclusion
- **Severity / evidence:** critical / provisional
- **Support counts:** 1 slugs, 1 independent source families
- **Evidence judgment:** Only one independent bank source directly supports this rule, so its evidence status remains provisional despite its practical importance.
- **Source-bank rule:** `paragraph-logic-46`
- **Supporting sources:** `b3-lund`
- **Exceptions:**
  - Exploratory hypotheses and future-research proposals are acceptable when clearly labeled as speculative.
  - Do not merely name a fallacy; explain the actual inferential failure.
