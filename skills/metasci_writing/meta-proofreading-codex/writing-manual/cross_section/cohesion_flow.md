# Cross-Section: Cohesion & Information Flow

> **Theoretical basis:** Gopen & Swan (1990), Daneš (1974), Halliday & Hasan (1976), Williams & Bizup

---

## The Core Principle: Writing Is Reader Management

Readers process text by building expectations and having them fulfilled. When the structure of a sentence places information in unexpected positions, comprehension slows — not because the reader lacks intelligence, but because the text is violating the cognitive contract of the Given-New structure.

**Gopen & Swan's central claim:** Most problems in professional scientific writing are caused by the misplacement of old and new information within sentences.

---

## 1. The Given-New Principle

Every sentence has two structural positions with distinct communicative functions:

| Position | Function | Content type |
|---|---|---|
| **Topic position** (sentence opening) | Backward linkage — connects to what came before | Old / Given information |
| **Stress position** (sentence ending) | New information — what the sentence actually contributes | New / Emphatic content |

**The rule:** Old information goes first; new information goes last.

### Why this matters
The reader uses the sentence opening to locate the sentence within their developing understanding of the passage. The sentence ending receives natural prosodic emphasis — it is where the reader's attention peaks. Placing the most important new claim at the end is not optional; it is the basic contract of English syntax.

### Diagnostic
❌ "A significant positive correlation between freeze-thaw frequency and SOC loss was found in the mineral soil horizon."
The new finding (the correlation) is buried at the beginning. The sentence ends on "mineral soil horizon" — old, contextual information.

✅ "In the mineral soil horizon, SOC loss was significantly correlated with freeze-thaw frequency (r = 0.78, p < 0.001)."
The sentence now opens with known context and ends on the finding.

---

## 2. Thematic Progression Patterns (Daneš 1974)

Coherent paragraphs use one of four thematic progression patterns. Expert writers choose the pattern that matches their rhetorical intent.

### Pattern 1: Linear Progression
The new information (Rheme) of sentence N becomes the topic (Theme) of sentence N+1.

**Use when:** Driving an argument forward step-by-step.

> Freeze-thaw cycles disrupt soil macroaggregates [Theme → Rheme: mechanism].
> This disruption exposes physically protected carbon to microbial attack [old: disruption → new: exposure].
> Exposed carbon is mineralized at rates 3–5× higher than protected fractions [old: exposed carbon → new: rate].

### Pattern 2: Constant Theme
The same topic recurs as the Theme of multiple sentences, with different new information each time.

**Use when:** Characterizing a single entity across multiple dimensions — common in Methods.

> Samples were collected from three sites representative of different permafrost regimes.
> Samples were stored at −20°C within 2 hours of collection.
> Samples were analyzed for SOC content within 30 days of collection.

### Pattern 3: Derived Theme Progression
Multiple subtopics are derived from a single hypertheme stated in a topic sentence.

**Use when:** Expanding a generalization into component parts — common in Discussion opening paragraphs.

> Three mechanisms explain the observed SOC increase under elevated CO₂. [hypertheme]
> First, enhanced root exudation... [subtopic 1]
> Second, increased microbial biomass turnover... [subtopic 2]
> Third, reduced aggregate stability... [subtopic 3]

### Pattern 4: Split Rheme Progression
Multiple new elements in one sentence become separate topics in subsequent sentences.

**Use when:** Introducing a set of variables or findings that will each be discussed separately.

---

## 3. Cohesive Devices: What Actually Creates Flow

Halliday & Hasan (1976) demonstrated that **lexical cohesion** (not conjunctions) accounts for the majority of textual connectivity in expert writing. The five device types, ranked by expert usage frequency:

| Device | Example | Frequency in expert text |
|---|---|---|
| **Lexical repetition / variation** | "aggregate → aggregates → aggregate disruption" | Dominant |
| **Reference** | pronouns, demonstratives ("this," "these," "such") | High |
| **Conjunction** | "however," "therefore," "consequently" | Moderate |
| **Substitution** | "the former / the latter," "the process / this process" | Lower |
| **Ellipsis** | Omitting repeated elements | Lower |

**Implication:** The primary instrument of flow is strategic lexical repetition and variation — not inserting transition words. Connectives like "furthermore" and "moreover" are overused in non-native expert writing and can sound additive rather than argumentative. Use logical connectors for their specific meanings, not as generic flow signals.

---

## 4. Paragraph Architecture

Every paragraph in a scientific paper should:
1. **Open with a topic sentence** that states what the paragraph is about (not a transition sentence)
2. **Develop one coherent point** — multiple ideas need multiple paragraphs
3. **Close with a sentence** that either summarizes the paragraph's contribution or sets up the next paragraph

**The Mensh-Kording C-C-C principle at paragraph level:**
- **Context** (topic sentence): What is this about?
- **Content** (body): The evidence, data, or argument
- **Conclusion** (closing sentence): What does this mean / where are we going?

### Diagnostic: paragraph fragmentation
If a paragraph's sentences cannot be connected into a single coherent claim, the paragraph is fragmented. The solution is not adding more transition words — it is identifying the single claim the paragraph should make and reorganizing the sentences accordingly.

---

## 5. Terminological Consistency (The Banana Rule)

> **Source:** Sainani, *Writing in the Sciences* — "Do not call a banana an elongated yellow fruit."

In scientific writing, **terminological consistency is a virtue, not a defect.** Readers of literary prose may welcome synonym variation as a sign of a rich vocabulary; readers of a research paper interpret synonym variation as **a signal that the writer is referring to a new category**. Switching between "obese group" and "heavier group," or between "freeze-thaw treatment" and "F-T regime," forces the reader to ask: *Is this the same thing, or has the writer introduced a new variable?*

Lexical repetition is the **dominant cohesive device** in expert scientific text (see §3 above). The Banana Rule extends this principle from sentence-to-sentence cohesion to **document-wide terminological discipline**.

### 5a. The audit procedure

The agent should:
1. Extract all **key technical terms** from the **Methods section**:
   - Group/condition names
   - Variable names
   - Technique names
   - Defined acronyms
2. Verify that the **exact same terms** appear in **Results**, **Discussion**, **Tables**, and **Figure captions**
3. Flag every instance where a **synonym was substituted** for a defined term

### 5b. Common violations

❌ Methods: "obese group (BMI ≥ 30)"
❌ Results: "the heavier participants showed..."
❌ Discussion: "high-BMI individuals demonstrated..."

The reader cannot tell whether all three refer to the same group. The agent flags **MEDIUM** and recommends collapsing to a single defined term.

❌ Methods: "freeze-thaw treatment (FT)"
❌ Results: "the F-T regime caused..."
❌ Discussion: "frost cycling led to..."

Three different forms of the same condition. The agent flags **MEDIUM** and recommends one canonical form (preferably the defined acronym after first use).

### 5c. When variation is appropriate

- **First introduction → defined acronym** ("freeze-thaw treatment (hereafter, FT)") is normal expansion, not a violation.
- **Hyperonym variation** for stylistic relief ("the treatment" referring back to "FT") is acceptable when the referent is unambiguous.
- **Genuinely different categories** (a "heavier" subgroup *within* the "obese group") need different terms — but the relationship must be explicit.

### 5d. Diagnostic prompt for the agent

When the agent flags a candidate violation, it should explain:
> "Methods에서는 'obese group'으로 정의되었으나, Results에서는 'heavier participants'로 표현되었습니다. 독자는 두 표현이 같은 집단을 가리키는지 새로운 하위집단을 말하는지 즉시 판단할 수 없습니다."

---

## 6. Acronym Discipline

Acronyms are a special case of terminological consistency. They reduce repetition but **only when the reader can decode them effortlessly**.

### 6a. Definition rules

- **Define at first use** in the Abstract AND again at first use in the main text. Readers may skim to the Methods or Discussion before reading the Introduction.
- **Re-define in each Table caption** and each **Figure caption**. Captions are read out of order.
- After definition, **use the acronym consistently**. Do not switch back to the full form without rhetorical reason.

### 6b. Acronym austerity

- **Permit only universally recognized acronyms** without re-definition (DNA, RNA, PCR, NMR, MRI, CO₂, GDP, etc.).
- **Flag invented acronyms** that appear fewer than ~5 times — they cost the reader more than they save.
- **Flag acronym pile-ups** in a single sentence ("the SOC dynamics in the FT-treated MAOM fraction of the AGS subplot..."). When ≥3 acronyms appear in one clause, the agent recommends spelling out at least one for readability.

### 6c. Cross-link

For numerical and citation integrity (where acronym discipline has the highest stakes — undefined acronyms in tables block reproduction), see `quantitative_integrity.md` §4.

---

## 7. Agent Diagnostic Questions

For each paragraph:
- What is the topic sentence? Is it the first sentence?
- Is the paragraph developing one idea or two?
- Does the closing sentence summarize, conclude, or bridge forward?

For each sentence:
- Does the sentence opening connect to the preceding sentence?
- Is the most important new information at or near the sentence end?
- Is there a gap between subject and verb — and if so, does it slow the reader?

For terminology (Banana Rule):
- Has any defined Methods term been replaced by a synonym in Results or Discussion?
- Are all acronyms defined where required (Abstract, main text, each caption)?
- Is any acronym invented for fewer than ~5 uses?
- Are there acronym pile-ups (≥3 acronyms in one clause)?

For the passage overall:
- Which thematic progression pattern is the writer using — and is it appropriate?
- Are paragraphs linked across boundaries, or is each paragraph an island?
- Is flow created by lexical cohesion (repetition, variation) or only by connectives?
