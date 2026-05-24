# Evidence Bank Schema

## Purpose

The Evidence Bank is a structured collection of writing patterns extracted
from comparable published papers. It supplements the writing-manual with
domain-specific and journal-specific evidence for grounded corrections.

---

## Structure

```
evidence_bank = {
    section: str,               # Current section name
    target_journal: str,        # Target journal (if provided)
    topic_keywords: [str],      # User's topic keywords

    papers: [                   # Collected reference papers
        {
            title: str,
            authors: str,       # "First Author et al."
            year: int,
            journal: str,
            citation_count: int,
            doi: str,           # If available
            access_level: str,  # "full_text" | "abstract" | "snippet"
            abstract: str,      # Full abstract text
            section_excerpt: str # Relevant section text (if full text available)
        }
    ],

    patterns: {
        structure: {...},       # Section structure patterns
        expressions: {...},     # Sentence-level expression patterns
        hedging: {...},         # Hedging intensity profile
        transitions: [...],     # Transition patterns
        terminology: [...]      # Domain-specific terms
    },

    journal_guidelines: {       # From author guidelines page
        length: str,            # Recommended length
        style_notes: str,       # Special requirements
        citation_style: str     # Required format
    },

    metadata: {
        created_at: str,        # Timestamp
        queries_used: [str],    # Search queries that produced this bank
        paper_count: int,
        full_text_count: int,
        abstract_count: int
    }
}
```

---

## Pattern Extraction Rules

### 1. Section Structure Patterns

**Source:** Full text (preferred) or abstract structure analysis.

**Extract:**
- Move sequence in the section (using move labels from writing-manual)
- Paragraph count and approximate lengths
- Opening and closing strategies

**Format:**
```
structure = {
    move_sequences: [
        {paper: "Author (Year)", sequence: "M2→M3→M4→M3→M5→M6→M7"},
        ...
    ],
    dominant_pattern: "M2→M3/M4 cycling→M5→M6→M7",
    opening_strategy: "Leads with key finding, not purpose restatement",
    closing_strategy: "Ends with broadest implication",
    typical_para_count: "7-10 paragraphs for Discussion"
}
```

**From abstracts only:** Infer structure from abstract's sentence flow
(background → objective → method → result → conclusion). Note that
abstract structure partially reflects the paper's internal organization.

### 2. Key Expression Patterns

**Source:** Abstracts, snippets, full text sections.

**Extract sentence-opening patterns organized by rhetorical function:**

```
expressions = {
    result_interpretation: [
        "The observed [change] in [variable] is most parsimoniously explained by...",
        "These findings suggest that [mechanism]...",
        "[Variable] exhibited [pattern], which may reflect..."
    ],
    literature_comparison: [
        "This finding aligns with [Author] (Year), who reported...",
        "In contrast to [Author] (Year), our results suggest...",
        "The discrepancy between our findings and those of [Author] (Year) likely stems from..."
    ],
    limitation_framing: [
        "While our study provides evidence for X, it should be noted that...",
        "A potential limitation is that..., although this is partially mitigated by...",
        "The scope of this study was limited to..., and future work should..."
    ],
    methodological_description: [
        "[Samples/Data] were [collected/analyzed] using...",
        "To determine [variable], we employed...",
        "Following the protocol established by [Author] (Year),..."
    ],
    transition_between_topics: [
        "Beyond [previous topic], our results also reveal...",
        "Turning to [new topic],",
        "A related but distinct finding concerns..."
    ]
}
```

**Extraction rules:**
- Preserve the sentence template structure (replace specifics with [brackets])
- Record 5-10 patterns per function category
- Prioritize patterns from the target journal
- If extracting from abstracts, note that abstract language tends to be
  more compressed than body text

### 3. Hedging Intensity Profile

**Source:** Abstracts (most reliable for hedging analysis — consistent
structure across papers).

**Extract:**

```
hedging = {
    modal_verbs: {
        examples: ["may", "could", "might"],
        frequency: "moderate — ~2-3 per abstract",
        typical_context: "result interpretation, not methodology"
    },
    lexical_hedges: {
        examples: ["suggest", "indicate", "appear to"],
        frequency: "high — dominant verb choice for findings",
        typical_context: "connecting data to interpretation"
    },
    boosters: {
        examples: ["clearly", "significantly", "strongly"],
        frequency: "low — used only with statistical backing",
        typical_context: "quantitative results with p-values"
    },
    approximators: {
        examples: ["approximately", "roughly", "~"],
        frequency: "moderate — for numerical reporting",
        typical_context: "measurement values, percentages"
    },
    overall_calibration: "This domain uses moderate-to-heavy hedging.
        Claims are typically qualified with 'suggest' or 'indicate'
        rather than 'demonstrate' or 'prove'. Boosters appear only
        when backed by strong statistical evidence."
}
```

**Calibration rule:** Compare the user's text against this profile.
- If user's hedging is weaker than domain norm → flag as "under-hedged"
- If user's hedging is stronger → flag as "over-hedged"
- If aligned → note as "calibrated"

### 4. Transition Patterns

**Source:** Full text or abstracts.

**Extract paragraph-to-paragraph and sentence-to-sentence transitions:**

```
transitions = [
    {type: "additive", examples: ["Furthermore,", "In addition,", "Moreover,"]},
    {type: "contrastive", examples: ["However,", "In contrast,", "Nevertheless,"]},
    {type: "causal", examples: ["Therefore,", "Consequently,", "As a result,"]},
    {type: "elaborative", examples: ["Specifically,", "In particular,", "Notably,"]},
    {type: "temporal/sequential", examples: ["Subsequently,", "Following this,"]},
    {type: "concessive", examples: ["Although...,", "While...,", "Despite..."]}
]
```

**Domain note:** Some domains favor specific transition patterns.
For example, geoscience papers often use "Notably," and "Importantly,"
more than social science papers.

### 5. Domain-Specific Terminology

**Source:** All collected texts.

**Extract recurring technical expressions specific to this topic:**

```
terminology = [
    {
        term: "soil organic carbon (SOC)",
        usage: "Always abbreviated after first use; never 'organic C in soil'",
        context: "Appears in all sections, quantified in g/kg or %"
    },
    {
        term: "freeze-thaw cycling",
        usage: "Preferred over 'freeze-thaw treatment' in Discussion",
        context: "Process description in Methods, interpretation in Discussion"
    },
    {
        term: "aggregate stability",
        usage: "Measured by MWD (mean weight diameter); reported with units",
        context: "Key mechanism variable, often paired with SOC dynamics"
    }
]
```

---

## Evidence Bank Updates

### On section change

When the user moves to a different section:
1. Retain `papers` list (no re-search needed)
2. Re-extract `patterns` for the new section:
   - `structure`: re-analyze for new section's move structure
   - `expressions`: extract patterns relevant to new section's functions
   - `hedging`: usually stable across sections (retain)
   - `transitions`: may vary by section (re-extract)
   - `terminology`: retain (domain-stable)
3. Notify user: "Updating Evidence Bank for [new section]"

### User adds a paper

When user says "add this paper: [DOI or title]":
1. Search for the paper via Semantic Scholar or Google Scholar
2. Fetch accessible text
3. Add to `papers` list
4. Re-extract patterns to incorporate new source
5. Confirm: "[Paper title] added to Evidence Bank"

### Quality degradation

If Evidence Bank has <3 papers or only snippet-level access:
- Mark as `low_confidence`
- Agent prompts include caveat: "Evidence Bank is limited; rely more
  heavily on writing-manual rules"
- Agent S spot searches become more important as compensating mechanism
