# Search Strategy — Web Search for Knowledge Supplementation

## Purpose

Web search supplements local knowledge when local files are
insufficient. This file defines when and how to search.

---

## When to Search

Web search is triggered only when:

1. `knowledge_bank.quality.sufficient` is false for the current claim or task
2. User explicitly requests: "웹에서도 찾아봐", "search more"
3. A specific citation needs verification (Agent B)
4. Deliberation produces LOW confidence and no local knowledge covers it

Web search is **skipped** when:
- User says "웹검색 없이", "skip web", "로컬만"
- Available originals or authoritative sources already provide sufficient,
  independent coverage for the current decision

---

## Search Sources

### 1. Google Scholar (via web search)

**Query patterns:**

```
Pattern 1 — Journal + topic:
  "[target_journal] [keyword1] [keyword2]"

Pattern 2 — Topic + recent:
  "[keyword1] [keyword2] [keyword3] [field-appropriate date range if needed]"

Pattern 3 — Review/meta-analysis:
  "[keyword1] [keyword2] review OR meta-analysis"
```

Rules:
- Keep queries short: 3-6 words
- No quotation marks unless exact phrase needed
- Generate 2-3 queries maximum

### 2. Semantic Scholar API (via HTTP fetch)

```
https://api.semanticscholar.org/graph/v1/paper/search
  ?query={query}
  &limit=5
  &fields=title,abstract,year,venue,citationCount,tldr,externalIds
```

No authentication needed. Free tier: 100 requests per 5 minutes.

Parse response:
- `data[].title` → source title
- `data[].abstract` → primary text for extraction
- `data[].year` → for recency ranking
- `data[].venue` → journal name
- `data[].citationCount` → quality indicator
- `data[].externalIds.DOI` → for reference verification

### 3. Open Access Full Text (via HTTP fetch)

For top-ranked papers, attempt full text access:

1. **PMC:** search `site:ncbi.nlm.nih.gov/pmc`
2. **Unpaywall:** `https://api.unpaywall.org/v2/{DOI}?email={configured_contact_email}`
3. **arXiv:** `https://arxiv.org/abs/{ID}`

If no full text: proceed with abstract (notify user).

---

## Paper Selection Criteria

Rank search results by:

1. **Journal match** (same journal > same field > general)
2. **Topic relevance** (2+ shared keywords)
3. **Methodological fit and directness of evidence**
4. **Date relevance for the claim** (recent is not automatically better)
5. **Independent support and source authority** (citation count is context, not quality)
6. **Access level** (full text > abstract > snippet)

Select top 3-5 papers. Add to `knowledge_bank.sources[]` with
`origin: "web"`.

---

## Integration with Knowledge Bank

Web-sourced content populates the same schema as local files:

- Abstract text → `domain_knowledge.empirical` (findings),
  `writing_patterns.hedging` (hedge verbs from abstract)
- Full text section → `writing_patterns.structure`,
  `writing_patterns.expressions`
- Snippet → `domain_knowledge.contextual` (limited value)

Rank sources by originality, authority, directness, and fit to the claim—not by
whether they are stored locally or retrieved from the web.

---

## Rate Limiting

| Source | Limit | On failure |
|---|---|---|
| web search | No strict limit | Retry with modified query |
| Semantic Scholar API | 100 req / 5 min | Wait or skip |
| HTTP fetch (full text) | Per-domain | Skip, use abstract |
| Unpaywall API | 100K req / day | Fall back to DOI fetch |

---

## Agent B — Reference Verification Searches

Agent B uses web search specifically for citation verification.
Separate from knowledge supplementation.

Query format: `"{first_author} {year} {1-2 key terms}"`

A local author+year match is a candidate lookup, not automatic verification.
Check `knowledge_bank.sources[]` first, then verify metadata and any load-bearing
claim against an appropriate original, full text, or official record.
