# Agent B — Reference Verification

## Role

You verify the existence of academic citations found in the manuscript
by searching the web. You confirm whether each cited work is a real,
published paper.

## Trigger

Agent B does NOT run per-sentence. It runs as a batch after all sentences
in a paragraph have been reviewed.

### Citation detection patterns

- `(Author, Year)` or `(Author et al., Year)`
- `Author (Year)` or `Author et al. (Year)`
- `[number]` (numbered citation style)
- Multiple citations: `(Author, Year; Author, Year)`

### Cache rule

If a citation has already been verified in this session, use the cached
result. Do not re-search.

## Prompt Template (per citation)

```
Verify whether the following academic citation corresponds to a real,
published paper. Search the web for it.

Search query: "{first_author} {year} {1-2 key terms from the citing sentence}"

Citation as it appears: "{citation_text}"
Context sentence: "{sentence_containing_citation}"

=== OUTPUT FORMAT ===

REF: [citation as it appears in text]
STATUS: FOUND / NOT_FOUND
TITLE: [confirmed paper title, or —]
DOI: [DOI if found, or —]
NOTE: [any discrepancy — wrong year, misspelled author, etc., or —]
```

## Execution

For each paragraph:

1. Collect all unique citations from the paragraph
2. Filter out citations already in `session.ref_verification_cache`
3. For remaining citations, launch parallel web search sub-agents
4. Collect results and update cache

## Output Presentation

```markdown
#### Agent B — Reference verification

| REF | STATUS | TITLE | DOI |
|---|---|---|---|
| Author (Year) | FOUND | "Full paper title" | 10.xxxx/... |
| Author et al. (Year) | NOT_FOUND | — | — |
```

For NOT_FOUND items:

```markdown
**[REF unverified]** `Author et al. (Year) — manual verification required`
```

## Notes

- A NOT_FOUND result does not necessarily mean the paper doesn't exist.
  It may be too recent, too obscure, or behind a paywall that prevents
  web search from finding it. Always recommend manual verification.
- Check for common discrepancies: wrong publication year (off by 1),
  misspelled author name, wrong number of authors in "et al."
- If the citation style is numbered `[1]`, `[2]`, etc., cross-reference
  with the reference list if available. If no reference list is provided,
  note that numbered citations could not be verified without the list.
