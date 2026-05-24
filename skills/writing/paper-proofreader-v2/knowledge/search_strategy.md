# Search Strategy — Web Search for Knowledge Supplementation

## Purpose

Web search supplements local knowledge when local files are
insufficient. This file defines when and how to search.

---

## When to Search

Web search is triggered only when:

1. `knowledge_bank.quality.sufficient` is false (< 3 sources)
2. User explicitly requests: "웹에서도 찾아봐", "search more"
3. A specific citation needs verification (Agent B)
4. Deliberation produces LOW confidence and no local knowledge covers it

Web search is **skipped** when:
- User says "웹검색 없이", "skip web", "로컬만"
- Local sources already provide sufficient coverage (>= 3 sources
  with at least 1 extraction file)

---

## Search Sources

### 1. Google Scholar (via WebSearch tool)

**Query patterns:**

```
Pattern 1 — Journal + topic:
  "[target_journal] [keyword1] [keyword2]"

Pattern 2 — Topic + recent:
  "[keyword1] [keyword2] [keyword3] 2023 OR 2024 OR 2025"

Pattern 3 — Review/meta-analysis:
  "[keyword1] [keyword2] review OR meta-analysis"
```

Rules:
- Keep queries short: 3-6 words
- No quotation marks unless exact phrase needed
- Generate 2-3 queries maximum

### 2. Semantic Scholar API (via WebFetch tool)

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

### 3. Open Access Full Text (via WebFetch tool)

For top-ranked papers, attempt full text access:

1. **PMC:** search `site:ncbi.nlm.nih.gov/pmc`
2. **Unpaywall:** `https://api.unpaywall.org/v2/{DOI}?email=user@example.com`
3. **arXiv:** `https://arxiv.org/abs/{ID}`

If no full text: proceed with abstract (notify user).

---

## Paper Selection Criteria

Rank search results by:

1. **Journal match** (same journal > same field > general)
2. **Topic relevance** (2+ shared keywords)
3. **Recency** (last 5 years preferred)
4. **Citation count** (higher = more established)
5. **Access level** (full text > abstract > snippet)

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

Web sources are always lower priority than local sources
in the Knowledge Bank.

---

## Rate Limiting

| Source | Limit | On failure |
|---|---|---|
| WebSearch | No strict limit | Retry with modified query |
| Semantic Scholar API | 100 req / 5 min | Wait or skip |
| WebFetch (full text) | Per-domain | Skip, use abstract |
| Unpaywall API | 100K req / day | Fall back to DOI fetch |

---

## Agent B — Reference Verification Searches

Agent B uses web search specifically for citation verification.
Separate from knowledge supplementation.

Query format: `"{first_author} {year} {1-2 key terms}"`

Citations found in local knowledge files → auto-verified (no search needed).
Check `knowledge_bank.sources[]` by author+year before searching.
