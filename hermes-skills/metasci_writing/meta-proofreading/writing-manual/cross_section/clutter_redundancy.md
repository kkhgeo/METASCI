# Cross-Section: Clutter & Redundancy Extraction

> **Theoretical basis:** Sainani (Stanford, *Writing in the Sciences*), Williams & Bizup (Style, 13th ed.), Strunk & White

---

## Framing Principle

Strip every sentence to its cleanest components. **Every word must earn its place.** Cluttered scientific prose does not merely waste reader attention; it obscures the actual claim by burying the verb in a thicket of filler. This file targets word-level and phrase-level dead weight that a `sentence_craft.md` review (which focuses on nominalization and structural clarity) does not catch.

This is a **lexical-level** audit. The agent applies it after the structural reviews have determined that the sentence's architecture is sound but the wording is bloated.

---

## 1. Dead-Weight Phrase Replacements

The following multi-word phrases compress to one or two words without loss of meaning. When the agent encounters one, the default action is to replace it.

| Cluttered phrase | Replace with |
|---|---|
| due to the fact that | because |
| in light of the fact that | because / since |
| owing to the fact that | because |
| despite the fact that | although |
| in spite of the fact that | although |
| in the event that | if |
| in the case that | if |
| with regard to / with respect to | regarding / about |
| in terms of | (rewrite — too vague) |
| on the basis of | based on |
| for the purpose of | to / for |
| in order to | to |
| in order that | so that |
| at the present time | now / currently |
| at this point in time | now |
| during the course of | during |
| in the process of | (delete or rewrite) |
| a majority of | most |
| a number of | several / many |
| the vast majority of | most |
| a great deal of | much |
| a considerable amount of | much |
| have an effect on | affect |
| have an impact on | affect / influence |
| give rise to | cause |
| are of the same opinion | agree |
| is/are able to | can |
| is/are capable of | can |
| is/are in agreement with | agree with |
| in close proximity to | near |
| prior to | before |
| subsequent to | after |
| in the absence of | without |
| in the presence of | with |
| it is possible that | may / might |
| it is likely that | likely |
| there is a possibility that | may |

**Apply with judgment.** When the cluttered form serves a hedging function the writer wants ("it is possible that" vs the bald "may"), preserve the longer form if hedge calibration matters. Cross-check with `stance_hedging.md`.

---

## 2. Dead-Weight Introductory Phrases — Flag for Deletion

These phrases add no information. They announce that something will be said rather than saying it. The default action is full deletion.

- "It is worth noting that..."
- "It is important to note that..."
- "It is interesting to note that..."
- "It should be emphasized that..."
- "It can be regarded that..."
- "It is/has been shown that..." (when followed by the claim — make the claim directly)
- "As is well known..." → replace with a direct citation
- "As has been demonstrated..." → cite the demonstration
- "Needless to say..."
- "It goes without saying that..."
- "It is a well-known fact that..."

**Diagnostic:** Read the sentence with the introductory phrase deleted. If the meaning survives intact, the phrase was clutter. If the deletion changes the sentence's epistemic stance (e.g., removes a hedge that was genuinely calibrating uncertainty), preserve it but consider rewording.

❌ "It is important to note that SOC concentrations were significantly elevated under freeze-thaw treatment."
✅ "SOC concentrations were significantly elevated under freeze-thaw treatment."

❌ "As is well known, freeze-thaw cycles disrupt soil aggregate stability."
✅ "Freeze-thaw cycles disrupt soil aggregate stability (Six et al., 2004; Oztas & Fayetorbay, 2003)."

---

## 3. Redundancy Extraction

Remove adjectives or adverbs that repeat information already carried by the noun or verb. This is **lexical redundancy**, distinct from the structural redundancy treated in `cohesion_flow.md`.

### Common redundant pairings

| Redundant | Cleaner |
|---|---|
| successful solutions | solutions (success is implicit) |
| completely eliminate | eliminate |
| totally destroyed | destroyed |
| future plans | plans |
| past history | history |
| unexpected surprise | surprise |
| advance planning | planning |
| end result | result |
| final outcome | outcome |
| basic fundamentals | fundamentals (or basics) |
| close proximity | proximity |
| currently underway | underway |
| each individual | each (or every individual) |
| repeat again | repeat |
| join together | join |
| combine together | combine |
| collaborate together | collaborate |
| brief summary | summary |
| general consensus | consensus |
| true facts | facts |
| absolutely essential | essential |
| completely unanimous | unanimous |
| revert back | revert |
| equally as | equally / as |
| both share | share / both have |

### Diagnostic patterns

The agent should scan for these classes:

1. **Adjective + noun where the adjective restates the noun's defining property** (e.g., "novel innovation," "free gift").
2. **Adverb + verb where the adverb is implicit in the verb** (e.g., "completely finished," "very unique").
3. **Pleonastic intensifiers** ("absolutely," "totally," "completely," "entirely") attached to absolute states.
4. **Doubled directional words** ("revert back," "return back," "follow after").

---

## 4. When NOT to Cut

Some apparent clutter serves real functions:

- **Hedges that calibrate uncertainty** ("the data suggest" vs "the data show" — see `stance_hedging.md`). "It is possible that" cannot always be reduced to "may" if "may" is too strong for the evidence.
- **Discipline-specific conventions** ("The present study..." is acceptable in some fields where authorial humility is normative).
- **Intentional emphasis** ("It is precisely this assumption that fails..." — the "It is...that" cleft serves a focus function).
- **Necessary scaffolding for non-native readers** of the journal (dense prose punishes a wider audience).

**Rule:** Cut only when the cleaner version preserves the meaning AND the rhetorical function. When in doubt, flag for the user rather than auto-applying.

---

## 5. Agent Diagnostic Questions

When reviewing a sentence for clutter:

- Does the sentence open with an introductory phrase that can be deleted?
- Are there multi-word prepositional clusters that compress to one word?
- Is any adjective restating a defining property of its noun?
- Is any adverb restating a property already in the verb?
- After cutting all candidates, does the sentence still say what it meant to say?
- Does the sentence still hedge at the intended level (cross-check with `stance_hedging.md`)?

---

## 6. Severity Calibration

| Severity | Trigger |
|---|---|
| **HIGH** | Sentence has 3+ dead-weight phrases or its actual claim cannot be located on first reading |
| **MEDIUM** | One clear dead-weight phrase; sentence reads bloated but parseable |
| **LOW** | Mild redundancy (e.g., "future plans" once in a long sentence); cut is a polish item |

Do not flag every "in order to" or every "currently underway." Apply the rule **scaled to significance** per `INDEX.md` Evaluation Principle 5.
