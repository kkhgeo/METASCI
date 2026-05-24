# Session Management — State, Save/Restore, Error Handling

## Session State

```
session = {
    // Position
    mode: "paper" | "section" | "paragraph",
    position: {
        section: str | null,
        para_idx: int | null,
        sent_idx: int | null
    },

    // Paper content
    paper_path: str,
    sections: [{ name, text, para_count }],

    // Knowledge
    knowledge_index: [{ path, type, title, authors, year, keywords, loaded }],
    knowledge_bank: { ... },  // see knowledge_bank_schema.md
    distribution: {
        R1: [file_ids],
        R2: [file_ids],
        R3: "writing-manual",
        R4: "none"
    },
    reviewer_count: int,

    // Intent
    confirmed_intents: { "section.para_idx": str },

    // Results
    corrections: [{ level, section, para_idx, sent_idx, original, revised, basis }],
    skipped: [{ section, para_idx, sent_idx }],
    ref_cache: { "Author (Year)": { status, title, doi } },

    // Metrics
    deliberation_stats: { ... },  // see deliberation.md
    confidence_stats: { ... }     // see confidence_routing.md
}
```

---

## Session Save

**Trigger:** User says "오늘 여기까지", "저장해줘", "done"

**Save location:**
```
~/.claude/projects/[project_hash]/memory/proofreader-session.json
```

**Saved data:**
- Current position (mode, section, paragraph, sentence)
- Confirmed intents (so user doesn't re-confirm)
- Corrections list (revision history)
- Skipped items
- Reference cache (verified citations)
- Knowledge distribution plan
- Deliberation stats

**NOT saved (reconstructible):**
- Full paper text (re-read from file)
- Writing-manual content (re-read from skill)
- Knowledge file contents (re-read from paths in index)

---

## Session Restore

**Trigger:** Session start with existing save file detected.

**Process:**
1. Detect save file at known path
2. Ask user: "이전 세션이 있습니다 ([섹션], 단락 [N], 문장 [M]). 이어서 할까요?"
3. If yes:
   - Restore position
   - Re-read paper file
   - Re-load knowledge files from saved index paths
   - Restore intents, corrections, ref_cache
   - Resume from saved position
4. If no:
   - Archive old save (rename with timestamp)
   - Start fresh session

---

## Error Handling

### Agent sub-agent failure
- Retry once with same prompt
- If retry fails: "**[에이전트 응답 없음]** 해당 리뷰어를 제외하고 나머지 결과로 진행합니다"
- Continue deliberation with available reviewers (minimum 2)
- If fewer than 2 reviewers succeed: "**[검토 불가]** 수동 검토가 필요합니다"

### Web search failure
- "**[검색 불가]** 로컬 지식과 writing-manual 기준으로만 진행합니다"

### Knowledge file read failure
- Skip the file, remove from distribution
- Notify: "[파일명] 읽기 실패 — 해당 파일 없이 진행합니다"
- Redistribute remaining files if needed

### PDF read failure
- Try with different page ranges
- If still fails: skip, notify user

### File encoding error
- Try UTF-8 → EUC-KR → CP949
- If all fail: skip with notification

---

## Sentence Splitting Rules

- Split on: `. ` `? ` `! `
- Do NOT split after: `et al.` `Fig.` `vs.` `e.g.` `i.e.` `cf.` `ca.` `Dr.` `Mr.` `No.`
- Do NOT split inside parentheses
- Do NOT split inside quotation marks

---

## Table/Figure Handling

- Table/figure content: skip (not reviewed)
- Table/figure captions: reviewed as sentences
- Body text after tables/figures: reviewed normally
