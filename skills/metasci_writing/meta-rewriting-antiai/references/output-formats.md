# Output Formats — meta-rewriting-antiai 출력 카드 형식

> 모든 출력 시 이 파일의 형식을 따른다.

---

## 1. PHASE 1 Diagnostic Card

```
================================================================
  AI FINGERPRINT SCAN — Diagnostic Report
  Input: [word count]w | Section: [section type]
  Date: [YYYY-MM-DD]
================================================================

LAYER 1: LEXICAL SCAN                                Score: [X]/10
─────────────────────────────────────────────────────
  Tier 1 words found: [count] ([word list])
  Tier 2 words found: [count]
  Co-occurrence pairs: [count] ([pair list])
  Copula avoidance: [count] instances
  High-signal phrases: [count]

  Details:
  [1] ¶X, SY: "[exact quote]" — [word]: [severity]
  [2] ¶X, SY: "[exact quote]" — [word]+[word] co-occurrence: [severity]
  ...

LAYER 2: SYNTACTIC SCAN                              Score: [X]/10
─────────────────────────────────────────────────────
  Sentence length SD: [X.X] words (target: ≥8)
  Paragraph length SD: [X.X] words (target: ≥15)
  -ing tail patterns: [count]
  Rule of Three: [count]
  Syntactic template repeats: [count]

  Details:
  [1] ¶X: Sentence lengths = [n1, n2, n3, ...] → SD = [X.X]
  [2] ¶X, SY: "-ing tail" — "[exact quote]"
  ...

LAYER 3: DISCOURSE SCAN                              Score: [X]/10
─────────────────────────────────────────────────────
  Hedges: [count] (target: [X-Y] for this section type)
  Boosters: [count] (target: [X-Y])
  Self-mentions: [count] (target: ≥[N])
  Attitude markers: [count] (target: ≥[N])
  Transition overuse: [list of repeated transitions]

  Details:
  [1] ¶X: No self-mention in entire paragraph — [severity]
  [2] ¶X: "Furthermore" + "Moreover" in same paragraph — [severity]
  ...

LAYER 4: FORMATTING SCAN                             Score: [X]/10
─────────────────────────────────────────────────────
  Em dashes: [count] (limit: 1 per paragraph)
  Lists in prose: [count]
  Inline-headers: [count]
  Excessive headings: [count]
  Markdown artifacts: [count]

  Details:
  [1] ¶X: [count] em dashes in paragraph — [severity]
  [2] ¶X: Bullet list should be prose — [severity]
  ...

─────────────────────────────────────────────────────
  SUMMARY
  Layer 1 (Lexical):    [X]/10  [█████░░░░░]
  Layer 2 (Syntactic):  [X]/10  [████░░░░░░]
  Layer 3 (Discourse):  [X]/10  [███████░░░]
  Layer 4 (Formatting): [X]/10  [████████░░]
  ─────────────────────────────────
  Overall:              [X.X]/10

  Issues: [N] Critical | [N] Major | [N] Minor
  Recommendation: [교정 범위 권장사항]
================================================================
```

### Score Bar 생성 규칙

```
Score 1:  [█░░░░░░░░░]
Score 2:  [██░░░░░░░░]
Score 3:  [███░░░░░░░]
Score 4:  [████░░░░░░]
Score 5:  [█████░░░░░]
Score 6:  [██████░░░░]
Score 7:  [███████░░░]
Score 8:  [████████░░]
Score 9:  [█████████░]
Score 10: [██████████]
```

---

## 2. PHASE 2 Change Log

```
================================================================
  NATURALIZATION CHANGE LOG
  Intensity: [Light / Standard / Deep]
  Layers applied: [1, 2, 3, 4] or [selected layers]
================================================================

LAYER 1 CHANGES (Lexical):
  [1] ¶1, S3: "delves into" → "examines" (Tier 1 excess word)
  [2] ¶2, S1: "intricate" + "meticulous" → "complex" + kept "meticulous"
      (Co-occurrence dispersal: intricate+meticulous pair)
  [3] ¶3, S2: "serves as a catalyst" → "is a catalyst" (Copula restoration)
  [4] ¶4, S1: "it is worth noting that" → [deleted] (High-signal phrase)
  ...
  Layer 1 corrections: [N] items | Preserved: [N] items

LAYER 2 CHANGES (Syntactic):
  [1] ¶1: Sentence lengths [22,19,21,20] → [8,28,12,25,7] (SD: 1.6 → 9.1)
  [2] ¶2, S4: ", highlighting the importance" → ". This highlights the importance"
      (-ing tail → independent sentence)
  [3] ¶3, S2: "simple, efficient, and reproducible" → "efficient and reproducible"
      (Rule of Three → reduced to two)
  ...
  Layer 2 corrections: [N] items | Preserved: [N] items

LAYER 3 CHANGES (Discourse):
  [1] ¶1, S1: [Added] "We found that" (Self-mention recovery)
  [2] ¶2, S3: [Added] "Surprisingly," (Attitude marker insertion)
  [3] ¶3, S1: "Furthermore," → "Building on this," (Transition diversification)
  [4] ¶4, S2: [Added] "clearly" before "demonstrate" (Booster insertion)
  ...
  Layer 3 corrections: [N] items | Preserved: [N] items

LAYER 4 CHANGES (Formatting):
  [1] ¶2: em dash "— which —" → parentheses "(which)" (Em dash reduction)
  [2] ¶5: 4-item bullet list → 2 prose sentences (List → prose conversion)
  [3] ¶7: "**Temperature**: 450°C" → prose sentence (Inline-header removal)
  ...
  Layer 4 corrections: [N] items | Preserved: [N] items

─────────────────────────────────────────────────────
  TOTAL: [N] corrections across [N] layers
  Content preservation: All claims, data, and citations intact ✓
================================================================
```

---

## 3. Verification Card (Phase 2 완료 후)

```
================================================================
  VERIFICATION — Post-Naturalization Re-scan
================================================================

                    Before    After     Change
  Layer 1 (Lex):   [X]/10    [X]/10    [+X.X]
  Layer 2 (Syn):   [X]/10    [X]/10    [+X.X]
  Layer 3 (Dis):   [X]/10    [X]/10    [+X.X]
  Layer 4 (Fmt):   [X]/10    [X]/10    [+X.X]
  ───────────────────────────────────────
  Overall:         [X.X]/10  [X.X]/10  [+X.X]

  Remaining issues:
  [1] ¶X: [description] — [severity] (reason for keeping)
  ...

  Verdict: [ACCEPT / RE-CORRECT Layer N / USER DECISION]

  Self-correction check:
  ☐ No new AI excess words introduced
  ☐ No new uniform sentence patterns
  ☐ No new em dash overuse
  ☐ No mechanical transition insertion
  ☐ Natural prose quality maintained
================================================================
```

---

## 4. Session Log

```
================================================================
  SESSION LOG — meta-rewriting-antiai
  Date: [YYYY-MM-DD]
  Input: [file name or "pasted text"] ([word count]w)
  Section: [type]
  Intensity: [Light / Standard / Deep]
================================================================

[HH:MM] PHASE 1 started
[HH:MM] Layer 1 scan: [N] issues found (Score: [X]/10)
[HH:MM] Layer 2 scan: [N] issues found (Score: [X]/10)
[HH:MM] Layer 3 scan: [N] issues found (Score: [X]/10)
[HH:MM] Layer 4 scan: [N] issues found (Score: [X]/10)
[HH:MM] Diagnostic report presented to user
[HH:MM] User response: [approved all / selected layers / modified scope]

[HH:MM] PHASE 2 started (Layers: [1,2,3,4])
[HH:MM] Layer 1 naturalization: [N] corrections
[HH:MM] Layer 2 naturalization: [N] corrections
[HH:MM] Layer 3 naturalization: [N] corrections
[HH:MM] Layer 4 naturalization: [N] corrections
[HH:MM] Verification re-scan: [Before X.X → After X.X]
[HH:MM] Self-correction check: [PASS / issues noted]
[HH:MM] User response: [accepted / requested changes]

[HH:MM] Output saved to AntiAI_{topic}/
================================================================
```

---

## 5. Output File Naming

```
AntiAI_{topic}/
├── phase1_diagnostic.md         ← Diagnostic Card (Section 1)
├── phase2_changelog.md          ← Change Log (Section 2)
├── phase2_verification.md       ← Verification Card (Section 3)
├── naturalized_draft.md         ← Final naturalized text
└── session_log.md               ← Session Log (Section 4)
```

### {topic} Derivation Rules

| Input source | {topic} |
|-------------|---------|
| 사용자 지정 | 사용자가 지정한 이름 |
| 파일명에서 추출 | 파일명 (확장자 제외) |
| 이전 스킬 출력 폴더 | 해당 폴더명 재사용 (e.g., Rewrite_GCA → AntiAI_GCA) |
| 텍스트 직접 붙여넣기 | 첫 문장에서 키워드 추출 |

---

**This file defines all output formats. Follow exactly.**
