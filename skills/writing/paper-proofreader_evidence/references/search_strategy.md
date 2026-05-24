# Search Strategy Reference

## Purpose

This file defines how Agent E and Agent S construct and execute web searches
to collect writing patterns from comparable published papers.

---

## Search Sources

### 1. Google Scholar (via web search tool)

**Primary use:** Discover papers, collect snippets, find open access versions.

Query patterns:

```
Pattern 1 — Journal + topic + section:
  "[target_journal] [keyword1] [keyword2] [section_name]"
  Example: "Geoderma soil organic carbon freeze-thaw discussion"

Pattern 2 — Topic + recent years:
  "[keyword1] [keyword2] [keyword3] 2023 OR 2024 OR 2025"
  Example: "soil organic carbon aggregate stability freeze-thaw 2023 OR 2024"

Pattern 3 — High-citation review:
  "[keyword1] [keyword2] review OR meta-analysis"
  Example: "soil organic carbon dynamics review"

Pattern 4 — Journal style guide:
  "[target_journal] author guidelines" OR "[target_journal] guide for authors"
  Example: "Geoderma author guidelines"
```

**Query rules:**
- Keep queries short: 3-6 words for best results
- Do not use quotation marks or Boolean operators unless needed
- Start broad, narrow if too many irrelevant results
- Each query must be meaningfully different from previous queries

### 2. Semantic Scholar API (via web_fetch tool)

**Primary use:** Structured metadata — abstract, TLDR, citation count, venue.

**Endpoint:**
```
https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit=5&fields=title,abstract,year,venue,citationCount,tldr,externalIds
```

**No authentication required.** Free tier: 100 requests per 5 minutes.

Example:
```
https://api.semanticscholar.org/graph/v1/paper/search?query=freeze-thaw+soil+organic+carbon&limit=5&fields=title,abstract,year,venue,citationCount,tldr,externalIds
```

**Response parsing:**
- `data[].title` — paper title
- `data[].abstract` — full abstract text (primary extraction source)
- `data[].year` — publication year
- `data[].venue` — journal/conference name
- `data[].citationCount` — for ranking relevance
- `data[].tldr.text` — one-sentence summary (useful for quick screening)
- `data[].externalIds.DOI` — for cross-referencing

### 3. Open Access Full Text (via web_fetch tool)

**Primary use:** Full section text for deep pattern extraction.

**Sources in priority order:**

1. **PubMed Central (PMC):**
   ```
   Search: "[keyword] site:ncbi.nlm.nih.gov/pmc"
   Fetch: "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{ID}/"
   ```

2. **Unpaywall API (find OA version of any DOI):**
   ```
   https://api.unpaywall.org/v2/{DOI}?email=user@example.com
   ```
   Response: `best_oa_location.url_for_pdf` or `best_oa_location.url`

3. **arXiv (preprints):**
   ```
   https://arxiv.org/abs/{ID}
   ```

4. **Publisher HTML pages (some open access):**
   Fetch the DOI URL and check if full text is accessible.

**When full text is not accessible:**
- Proceed with abstract + search snippets
- Notify user: "Full text not available for [N] papers. Using abstracts."
- Abstract-based extraction is still valuable for hedging profiles,
  key expressions, and general structural patterns

### 4. Journal Author Guidelines (via web_fetch tool)

Fetch the target journal's guide for authors to extract:
- Recommended section lengths
- Specific style requirements
- Citation format
- Any special structural expectations

---

## Query Construction Rules

### For Agent E (Evidence Gathering — section start)

Generate **3-5 queries** covering different angles:

1. **Exact match:** journal name + core topic + section name
2. **Broader topic:** core keywords + recent years (no journal filter)
3. **Authority:** topic + "review" or "meta-analysis" (for model writing)
4. **Style guide:** journal name + "author guidelines"
5. **Optional specific:** a known comparable paper the user mentioned

### For Agent S (Spot Search — on-demand)

Generate **1-2 focused queries** for the specific problem:

```
Pattern: "[specific term from problematic sentence] [domain context] [section context]"
Example: "SOC mineralization interpretation aggregate disruption discussion"
```

Agent S queries should be more specific than Agent E queries because they
target a particular sentence-level issue.

---

## Paper Selection Criteria

### Ranking factors (in priority order)

1. **Journal match:** Same journal as target > same field > general science
2. **Topic relevance:** Shares 2+ keywords with user's paper
3. **Recency:** Published within last 5 years preferred (unless foundational)
4. **Citation count:** Higher citations suggest established writing quality
5. **Access level:** Full text > abstract > snippet only

### Minimum collection targets

| Quality level | Papers | Minimum for Evidence Bank |
|---|---|---|
| Full text accessible | 1+ | Nice to have |
| Abstract accessible | 3+ | Required |
| Total papers | 3-5 | Required |

### Exclusion criteria

- Papers in languages other than English
- Retracted papers
- Papers from predatory journals (check if indexed in Scopus/WoS)
- Papers with no abstract available

---

## Rate Limiting and Error Handling

| Source | Limit | On failure |
|---|---|---|
| Google Scholar (web search) | No strict limit | Retry with modified query |
| Semantic Scholar API | 100 req / 5 min | Wait and retry, or skip |
| web_fetch (full text) | Per-domain limits | Skip paper, use abstract |
| Unpaywall API | 100K req / day | Fall back to direct DOI fetch |

**Agent S rate limit:** Maximum 10 spot searches per session.
Each spot search uses 1-2 web search calls.

---

## Search Result Storage

All search results are cached in `session.evidence_bank` and
`session.spot_search_cache` to avoid redundant searches.

When a citation has been verified by Agent B, store in
`session.ref_verification_cache` to skip re-verification.
