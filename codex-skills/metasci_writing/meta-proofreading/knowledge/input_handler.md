# Input Handler — File Type Detection & Parsing

## Purpose

Detect the type of any file in a Knowledge folder and extract
structured metadata for the Knowledge Index. Supports 6 file types.

---

## Two-Phase Process

### Phase 1: Lightweight Index Build (no full read)

For each file in the knowledge directory:

1. Check file extension (`.md`, `.pdf`, `.txt`, `.html`)
2. Read **first 20 lines only** with the Read tool
3. Apply detection rules below to classify file type
4. Extract metadata from header
5. Add entry to `knowledge_index[]`

**Cost:** ~20 lines per file. 20 files = 400 lines total.

### Phase 2: On-Demand Full Load

When a file is selected for a reviewer (via keyword matching):

1. Read full file content with the Read tool
2. Apply type-specific parser (see below)
3. Populate `knowledge_bank` fields

---

## File Type Detection Rules

Apply rules in order. First match wins.

### Type 1: Extraction-Knowledge

**Detection:**
- Filename contains no `_logic` or `_vocab` suffix
- Header (first 20 lines) contains ANY of:
  - `Knowledge Extraction`
  - `Knowledge Categories`
  - `Theoretical Foundations`
  - `Empirical Precedents`
  - `Methodological Heritage`

**Header metadata extraction:**
```
Title    ← line matching "**Title:**" or "# Knowledge Extraction: ..."
Authors  ← line matching "**Authors:**"
Year     ← line matching "**Year:**" or extract from title/filename
Journal  ← line matching "**Journal:**"
Keywords ← line matching "**Keywords:**" or extract from title
```

**Full parse (Phase 2):**
- Extract 5-category tables (Theoretical, Empirical, Methodological, Contextual, Critical)
- Each row becomes a knowledge entry: `{category, content_en, content_kr, citation, section}`
- Populate `knowledge_bank.domain_knowledge`

---

### Type 2: Extraction-Logic

**Detection:**
- Filename ends with `_logic.md`
- OR header contains ANY of:
  - `Structure Map`
  - `Inter-Paragraph Logic`
  - `Intra-Paragraph Logic`
  - `Sentence Frame Catalog`

**Header metadata extraction:**
```
Title    ← line matching "**Title:**" or first H1
Authors  ← line matching "**Authors:**"
Year     ← line matching "**Year:**" or extract from filename
Journal  ← line matching "**Journal:**"
Keywords ← extract from title
```

**Full parse (Phase 2):**
- Structure Map → `knowledge_bank.writing_patterns.structure`
- Inter-Paragraph Logic (function tags, flow) → `writing_patterns.transitions`
- Sentence Frame Catalog → `writing_patterns.expressions`
- Move sequence labels → `writing_patterns.structure.move_sequences`

---

### Type 3: Extraction-Vocab

**Detection:**
- Filename ends with `_vocab.md`
- OR header contains ANY of:
  - `Content Words by Section`
  - `Technical Term Glossary`
  - `Cross-Section Analysis`

**Header metadata extraction:**
```
Title    ← line matching "**Title:**" or first H1
Authors  ← line matching "**Authors:**"
Year     ← line matching "**Year:**" or extract from filename
Journal  ← line matching "**Journal:**"
Keywords ← extract from Technical Term Glossary section headers
```

**Full parse (Phase 2):**
- Content Words (Verbs) → scan for hedge/booster verbs → `writing_patterns.hedging`
- Technical Term Glossary → `writing_patterns.terminology`
- Section-specific vocabulary → `writing_patterns.terminology` (with section tags)

---

### Type 4: PDF

**Detection:**
- File extension is `.pdf`

**Header metadata extraction:**
- Read page 1 only: `Read(file_path, pages="1")`
- Extract: title (usually largest/bold text), authors, journal, year, abstract
- Keywords from abstract

**Full parse (Phase 2):**
- Read relevant pages (e.g., pages matching current section name)
- Extract text content for pattern analysis
- Populate both `domain_knowledge` and `writing_patterns` as applicable

---

### Type 5: Freeform Markdown

**Detection:**
- File extension is `.md` or `.txt`
- Does NOT match Type 1, 2, or 3 patterns

**Header metadata extraction:**
- Title from first H1 (`# ...`)
- Scan first 20 lines for author/year/journal patterns
- Keywords from title words (remove stopwords)
- If no structured metadata: use filename as title_guess

**Full parse (Phase 2):**
- Extract all citations: `(Author, Year)` or `(Author et al., Year)` patterns
- Summarize content sections (H2 headers as topic map)
- Any data tables → `domain_knowledge.empirical`
- Narrative content → `domain_knowledge.contextual`

---

### Type 6: HTML

**Detection:**
- File extension is `.html`

**Header metadata extraction:**
- Read first 20 lines
- Extract `<title>` tag or first `<h1>`
- Keywords from title

**Full parse (Phase 2):**
- Strip HTML tags, treat as freeform markdown
- Same parsing rules as Type 5

---

## Knowledge Index Entry Schema

```
knowledge_index_entry = {
    path: str,                    // absolute file path
    type: str,                    // "extraction_knowledge" | "extraction_logic" |
                                  // "extraction_vocab" | "pdf" | "freeform_md" | "html"
    title: str,                   // paper title or file title
    authors: str | null,          // "First Author et al." or null
    year: int | null,             // publication year or null
    journal: str | null,          // journal name or null
    keywords: [str],              // extracted keywords (3-10)
    loaded: bool,                 // false until Phase 2 load
    assigned_to: str | null       // reviewer ID when distributed
}
```

---

## Auto-Discovery Rules

When the user provides a paper file/folder path, auto-discover knowledge files:

1. Identify the project root: walk up from paper path until a known project
   directory is found (e.g., `Z:/KKH_Research/[project_name]/`)
2. Search within that project for directories matching:
   - `**/Knowledge*/**`
   - `**/Logic*/**`
   - `**/Vocab*/**`
   - `**/knowledge_base/**`
3. Glob for `*.md`, `*.pdf`, `*.txt`, `*.html` in found directories
4. Exclude: `venv/`, `node_modules/`, `__pycache__/`, `.git/`
5. Build knowledge_index from discovered files

If no files found, notify user and offer:
- Manual path input
- Web-only mode (skip local knowledge)

---

## Keyword Matching for On-Demand Loading

When entering a mode (Section or Paragraph), select files to load:

```
score(file, context_keywords) = count of overlapping keywords

Selection rules:
  - Score >= 2 → load file
  - Score == 1 AND file.type is "extraction_knowledge" → load file
  - Score == 0 → skip

  - If section text contains "Author (Year)" matching file.authors + file.year → load file
    (direct citation match = always load)
    
  - Maximum files to load per reviewer: 5
    (if more qualify, rank by score and take top 5)
```
