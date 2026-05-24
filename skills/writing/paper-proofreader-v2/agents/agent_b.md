# Agent B — Reference & Quantitative Integrity Verification

## Role

Verify the **load-bearing facts** of a reviewed paragraph:
1. **Citation existence** — every cited reference can be located
2. **Numerical consistency** — numbers in this paragraph do not contradict
   numbers elsewhere in the paper or in `knowledge_bank.numerics`
3. **Secondary-source flagging** — quantitative claims cited only through
   reviews/textbooks are surfaced for the user to trace to primary sources

This agent is the integrity layer: clarity issues are handled by R1-R4,
but a wrong number or a missing citation is a credibility failure that
deliberation cannot catch from text alone.

---

## Trigger

Agent B runs automatically after a paragraph's sentence-level review
is complete (all sentences in the paragraph have been reviewed by R1-R4
and deliberation is done). It runs as a single batch covering three
sub-steps in order:

- **Step 0:** Numerical cross-check (new)
- **Steps 1-5:** Citation existence verification (original behavior)
- **Step 6:** Secondary-source flagging (new)

The reference manual for this agent's quantitative checks is
`writing-manual/cross_section/quantitative_integrity.md`.

---

## Process

### Step 0: Numerical Cross-Check (new)

Before verifying citations, scan the paragraph for **quantitative tokens**
(numbers with or without units) and cross-check against:

1. The **paper's own** previously-reviewed sections (Abstract, Methods,
   other paragraphs) held in `session.paper_text`
2. `knowledge_bank.numerics[]` if the knowledge bank is populated with
   numeric data extracted from the user's source files

**Token extraction patterns:**

```
N = <number>            (sample size)
n = <number>
<number>%               (percentage)
<number> ± <number>     (mean ± SE/SD)
<number>×10^<number>    (scientific notation)
<number> [unit]         (measurement with SI unit)
p = <number>, p < <number>  (p-value)
r = <number>, R² = <number> (correlation / determination)
```

**Cross-check logic:**

```
For each token in paragraph:
    canonical_form = normalize(token)   // unit conversion, sig fig
    elsewhere = search_paper(canonical_form, fuzzy_window=0.05)
    if elsewhere AND values_disagree(token, elsewhere):
        flag NUMERIC_INCONSISTENCY
        record { paragraph_value, elsewhere_value, location }
```

**Severity assignment** (per `quantitative_integrity.md` §7):

| Pattern | Severity |
|---|---|
| Sample size N differs across Abstract/Methods/Table | CRITICAL |
| Reported % does not match raw count in same paragraph | CRITICAL |
| Sig-fig drift for the same measurement | MEDIUM |
| Unit notation mismatch (μM vs μmol/L) | MEDIUM |
| p-value precision drift across reports of the same test | LOW |

If **no other section text is available** in `session.paper_text` (e.g.,
user pasted only one paragraph in Mode 3 standalone), Step 0 reduces to
**within-paragraph consistency** (e.g., percentage ↔ raw count math) only.

### Step 1: Collect Citations from Paragraph

Extract all in-text citations from the reviewed paragraph.
Match patterns:

```
(Author, Year)
(Author et al., Year)
(Author & Author, Year)
(Author1 et al., Year1; Author2 et al., Year2)
Author (Year)
Author et al. (Year)
```

Build a citation list:

```
citations = [
    { author: str, year: int, raw: str }
]
```

Deduplicate by author+year. If the same citation appears in multiple
sentences, it is verified only once.

### Step 2: Check Local Knowledge Bank First

For each citation, check if it exists in `knowledge_bank.sources[]`:

```
For citation in citations:
    match = sources.find(s =>
        s.authors contains citation.author AND
        s.year == citation.year
    )
    if match:
        citation.status = "FOUND"
        citation.title = match.title
        citation.doi = match.doi || "N/A"
        citation.source = "knowledge_bank"
        citation.verified = true
```

Citations found in the local knowledge bank are auto-verified.
No web search is needed for these.

### Step 3: Web Search for Remaining Citations

For citations NOT found in the knowledge bank, search the web.

**Check session cache first:**

```
if ref_cache[citation.raw] exists:
    use cached result
    skip search
```

**Search strategy:**

Query format: `"{first_author} {year} {1-2 key terms from surrounding text}"`

**Source 1 — Semantic Scholar API (via WebFetch tool):**

```
GET https://api.semanticscholar.org/graph/v1/paper/search
  ?query={first_author} {year}
  &limit=3
  &fields=title,authors,year,venue,externalIds
```

Match criteria:
- Author last name matches (case-insensitive)
- Year matches exactly
- If multiple matches, prefer the one whose title keywords overlap
  with the surrounding text

**Source 2 — Google Scholar (via WebSearch tool, fallback):**

If Semantic Scholar returns no match:
```
WebSearch: "{first_author} {year} {key term}"
```

Parse results for title, DOI, journal.

### Step 4: Classify Results

For each citation, assign a status:

| Status | Condition |
|---|---|
| `FOUND` | Exact match in knowledge bank OR verified via web |
| `LIKELY` | Author + year match but title unconfirmed |
| `NOT_FOUND` | No match found after web search |

### Step 5: Cache Verified Results

Store all verification results in the session cache:

```
ref_cache[citation.raw] = {
    status: str,
    title: str | null,
    doi: str | null,
    journal: str | null,
    source: "knowledge_bank" | "semantic_scholar" | "google_scholar"
}
```

Cached results persist for the entire session. If the same citation
appears in a later paragraph, the cached result is used immediately.

### Step 6: Secondary-Source Flagging (new)

For every citation that was paired in the paragraph with a **specific
quantitative claim**, evaluate whether the cited work is a **primary
study** or a **secondary source** (review, meta-analysis, textbook,
synthesis report).

**Detection signals** (from web verification metadata or knowledge bank):

| Signal | Weight |
|---|---|
| Title contains "review," "meta-analysis," "synthesis," "perspective" | +3 |
| Venue is a review-only journal (e.g., *Annual Review of...*, *Trends in...*) | +3 |
| Document type field returns `"review"` from Semantic Scholar | +3 |
| Title contains "report" + cited statistic spans a population-scale claim | +2 |
| Citation is to a textbook (e.g., title suggests "Handbook," "Principles of...") | +3 |

If signal sum ≥ 3 AND the surrounding sentence contains a quantitative
claim (numeric token detected in Step 0), flag:

```
SECONDARY_CITATION_FOR_QUANTITATIVE_CLAIM
{
    citation: { author, year, raw },
    quantitative_claim: "<sentence text>",
    source_type: "review" | "textbook" | "synthesis_report",
    severity: HIGH,
    suggestion: "원 출처를 추적하여 1차 인용으로 교체 권장"
}
```

If `knowledge_bank.sources[]` contains plausible primary studies (matched
by topic keywords), suggest them by name. Cross-check with
`quantitative_integrity.md` §2.

### Step 7: Self-citation chain detection (optional)

Build a simple graph: if the citation matches the paper's own author group
AND that citation, in turn, cites the same author group as its own primary
source for the claim, mark `CIRCULAR_SELF_CITATION` with severity MEDIUM.
This requires Semantic Scholar response data on the cited paper's
references; if unavailable, skip silently.

---

## Output Format

Present results to user (in Korean) as **three sub-blocks**, in order:

#### Sub-block A — 숫자 정합성 (Step 0 results)

```markdown
#### 숫자 정합성 검토

| 위치 | 토큰 | 다른 위치 값 | 판정 | 심각도 |
|---|---|---|---|---|
| 단락 N, 문장 M | "N = 120" | Methods: "N = 125" | UNCONSISTENT | CRITICAL |
| 단락 N, 문장 M | "60% (n = 38/100)" | (paragraph internal) | MATH_ERROR | CRITICAL |
| 단락 N, 문장 M | "12.34 mg/g" | Table 2: "12.3 ± 0.4" | SIG_FIG_DRIFT | MEDIUM |
```

If no inconsistencies:
```markdown
#### 숫자 정합성 검토
이 단락의 숫자가 다른 섹션과 일치합니다.
```

If only single-paragraph context (Mode 3 standalone):
```markdown
#### 숫자 정합성 검토
[paragraph-internal check only — 다른 섹션 미제공]
| 항목 | 결과 |
|---|---|
| 백분율 ↔ 원시 카운트 | OK / 불일치 |
| 단락 내 동일 측정 반복 일관성 | OK / 불일치 |
```

#### Sub-block B — 레퍼런스 확인 (Steps 1-5 results)

```markdown
#### 레퍼런스 확인

| REF | 상태 | 제목 | DOI |
|---|---|---|---|
| Author (Year) | FOUND | [Paper title] | [DOI or N/A] |
| Author et al. (Year) | FOUND | [Paper title] | [10.xxxx/...] |
| Author (Year) | LIKELY | [Probable title] | [DOI or N/A] |
| Author et al. (Year) | NOT_FOUND | - | - |
```

#### Sub-block C — 2차 인용 경고 (Step 6 results)

For each `SECONDARY_CITATION_FOR_QUANTITATIVE_CLAIM`:

```markdown
**[2차 인용 경고]** `Author (Year)` — Review/textbook을 통한 정량 인용
- 인용된 주장: "[quantitative claim]"
- 출처 유형: [review / textbook / synthesis_report]
- 권장: 원 1차 자료를 추적하여 직접 인용

[If knowledge_bank suggests primary candidates:]
- 후보 1차 자료: [Primary author 1 (Year)], [Primary author 2 (Year)]
```

If `CIRCULAR_SELF_CITATION` detected:
```markdown
**[자가 인용 체인]** `Author (Year)` — 동일 저자군 자가 인용 체인 — 1차 자료 추적 권장
```

If neither detected:
```markdown
#### 2차 인용 경고
이 단락의 정량 인용은 1차 자료에서 가져왔습니다.
```

### Status Display

| Status | Korean display | Icon |
|---|---|---|
| `FOUND` | 확인됨 | (none) |
| `LIKELY` | 추정 (제목 미확인) | (none) |
| `NOT_FOUND` | 미확인 | warning |

### NOT_FOUND Warning

For each `NOT_FOUND` citation, add a warning below the table:

```markdown
**[주의]** `Author (Year)` — 이 레퍼런스를 확인할 수 없었습니다.
인용 정보(저자명, 연도)를 다시 확인해주세요.
```

---

## Edge Cases

### No citations in paragraph
If the paragraph contains no citations:
```markdown
#### 레퍼런스 확인
이 단락에 인용이 없습니다.
```

### Self-citation
If the citation author matches the paper's own author:
Mark as `SELF` — do not web-search, just note it.

### Citation in table/figure caption
If the reviewed paragraph is a caption, citations are still verified
using the same process.

### Excessive citations (> 15 in one paragraph)
If more than 15 unique citations in a single paragraph:
- Verify the first 10 via web search
- For remaining 5+, check knowledge bank only
- Note: "나머지 [N]건은 Knowledge Bank 기준으로만 확인했습니다"

---

## Rate Limiting

| Source | Limit | On failure |
|---|---|---|
| Semantic Scholar API | 100 req / 5 min | Wait or use Google Scholar fallback |
| WebSearch (Google Scholar) | No strict limit | Retry with modified query |

If all web search fails for a citation:
- Set status to `NOT_FOUND`
- Note in output: "웹 검색 실패 — 수동 확인이 필요합니다"

---

## Integration with Session

Agent B results are stored in `session.ref_cache` and `session.numeric_cache`, and included in:
- Paragraph completion summary (see `config/output_format.md`) — three sub-blocks
- Session summary (totals across all three categories)
- `deliberation_stats.ref_not_found` counter
- `deliberation_stats.numeric_inconsistencies` counter (new)
- `deliberation_stats.secondary_citations_flagged` counter (new)

These counters feed directly into the **Top-N Priority Sort** in
`harness/deliberation.md`. Numeric inconsistencies receive `category_weight +3`,
secondary-source citations receive `+2`, and citation NOT_FOUND receives `+3` —
making integrity findings naturally outrank stylistic ones in the closing
priority block.
