# Knowledge Bank Schema

## Purpose

Unified schema for all knowledge used during a proofreading session.
Combines local knowledge files and web-searched evidence into a single
structure that reviewers can reference.

---

## Schema

```
knowledge_bank = {
    // === Session metadata ===
    section: str,                    // current section name
    target_journal: str | null,      // target journal (if provided)
    topic_keywords: [str],           // user's topic keywords

    // === Sources (local + web) ===
    sources: [
        {
            id: str,                 // "src_001", "src_002", ...
            title: str,
            authors: str,
            year: int,
            journal: str | null,
            doi: str | null,
            origin: "local" | "web",
            source_path: str | null, // local file path (if local)
            source_type: str,        // "extraction_knowledge" | "extraction_logic" |
                                     // "extraction_vocab" | "pdf" | "freeform_md" |
                                     // "html" | "web_fulltext" | "web_abstract" | "web_snippet"
            keywords: [str],
            loaded: bool,            // true if full content has been parsed
            navigation_value: "high" | "medium" | "low",
            evidence_authority: "original" | "official_metadata" |
                                "derived_extraction" | "secondary" | "snippet",
            verification_state: "verified" | "partial" | "unverified"
        }
    ],

    // === Layer 1: Writing Patterns ("how to write") ===
    writing_patterns: {
        structure: {
            move_sequences: [
                { source_id, sequence: "M2→M3→M4→M3→M5" }
            ],
            dominant_pattern: str | null,
            opening_strategy: str | null,
            closing_strategy: str | null
        },
        expressions: {
            result_interpretation: [
                { pattern: str, source_id: str }
            ],
            literature_comparison: [
                { pattern: str, source_id: str }
            ],
            limitation_framing: [
                { pattern: str, source_id: str }
            ],
            methodological_description: [
                { pattern: str, source_id: str }
            ],
            transition_patterns: [
                { pattern: str, source_id: str }
            ]
        },
        hedging: {
            modal_verbs: { examples: [str], frequency: str },
            lexical_hedges: { examples: [str], frequency: str },
            boosters: { examples: [str], frequency: str },
            overall_calibration: str
        },
        terminology: [
            { term: str, usage: str, context: str, source_id: str }
        ]
    },

    // === Numeric facts (for Agent B Step 0 cross-check) ===
    numerics: [
        {
            value: str,              // canonical form, e.g. "N = 125", "12.3 ± 0.4 mg/g"
            unit: str | null,        // SI unit if applicable
            context: str,            // what the number describes
            location: str,           // section/table where it appears
            source_id: str           // which source it came from
        }
    ],

    // === Layer 2: Domain Knowledge ("what is known") ===
    domain_knowledge: {
        theoretical: [
            { content: str, translation_kr: str | null,
              citation: str, source_id: str }
        ],
        empirical: [
            { content: str, translation_kr: str | null,
              citation: str, source_id: str }
        ],
        methodological: [
            { content: str, translation_kr: str | null,
              citation: str, source_id: str }
        ],
        contextual: [
            { content: str, translation_kr: str | null,
              citation: str, source_id: str }
        ],
        critical: [
            { content: str, translation_kr: str | null,
              citation: str, source_id: str }
        ]
    }
}
```

---

## Source roles and authority

Do not collapse navigation convenience and evidentiary authority.

- **Original local data or full text**: highest authority for the specific material
  it contains.
- **Official metadata or venue instructions**: highest authority for identity,
  DOI, current requirements, and policy.
- **Open full text from an authoritative repository or publisher**: equivalent to
  the same original content stored locally.
- **Extraction files and structured notes**: high navigation value, but derived.
  Use them to locate passages and patterns; verify load-bearing claims against the
  original.
- **Abstracts and secondary sources**: useful within their stated scope, but not a
  substitute for full context or primary evidence when the claim requires it.
- **Search snippets**: discovery only; never mark a claim verified from a snippet.

Locality does not itself create authority, and web origin does not itself reduce
authority. Prefer the source that is most original, direct, appropriate to the
claim, and independently supported.

---

## Section Change Behavior

When the user moves to a different section:

1. `sources[]` list → **retained** (no re-search needed)
2. `writing_patterns` → **re-extracted** for new section
   - Logic extraction: re-read the section's paragraph structure
   - Vocab extraction: hedging profile is stable, terminology retained
3. `domain_knowledge` → **retained** (knowledge is section-independent)
4. Notify user: "Knowledge Bank을 [새 섹션]에 맞게 업데이트합니다"

---

## User-Added Sources

User can add sources at any time:

- `"이 논문도 참고해: [path or DOI]"`
  → add to sources[], run input_handler, parse, merge into knowledge_bank
- `"이 지식 빼줘"` or `"[source] 제외"`
  → remove from active sources (keep in index, mark excluded)

---

## Quality Indicators

```
quality = {
    total_sources: int,
    local_sources: int,
    web_sources: int,
    extraction_count: int,        // structured extraction files
    domain_knowledge_entries: int,
    writing_pattern_entries: int,
    sufficient: bool,             // assessed for the current claim/task
    sufficiency_reason: str,
    independent_source_groups: int
}
```

Do not set `sufficient` from a fixed source count. Three derived notes from one
paper remain one evidence lineage. Assess coverage, directness, independence,
methodological fit, and the consequence of error.

If `sufficient` is false, notify user and offer:
- Add more knowledge files
- Run web search to supplement
- Proceed with available knowledge only
