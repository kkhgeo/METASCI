---
name: meta-styling
description: |
  Apply an extracted style profile to a draft (paper or report): measured diagnosis,
  style revision, and post-revision verification. Consumes metasci-style-extraction
  outputs (style_profile.md + Style Cards) — this skill does NOT extract style itself.
  Trigger when: "문체 교정", "스타일 맞춰줘", "톤 맞춰줘", "스타일 적용", "style revision",
  "apply style profile", draft + style profile given.
  NOT for style extraction ("스타일 추출" → metasci-style-extraction) and NOT for
  argument-logic review ("논리 검토" → meta-review).
  **Always read references/revision_guide.md first!**
---

> **Prerequisite**: Read `references/revision_guide.md` before revising anything.

# Meta-Styling Skill (v2.0 — apply-only)

## Overview

Applies a previously extracted style profile to a user draft. Diagnosis and
verification are **measured** with `scripts/quant_check.py`, not estimated:
the draft's hedging density, sentence length, and passive rate are counted and
compared against the profile's measured values, and the revised text is
re-measured to confirm it moved toward the target.

**Core principle: the measurement wins.** No invented "match rates" — every
quantitative claim in the diagnosis comes from the script.

### Division of labor (this skill is the CONSUMER)

| Job | Skill |
|-----|-------|
| Extract style from reference papers | `metasci-style-extraction` (Style Cards + style_profile.md) |
| Extract argument structure / frames | `extraction-logic` |
| Review draft LOGIC against references | `meta-review` |
| **Apply style profile to a draft** | **meta-styling (this skill)** |
| Remove AI-writing traces afterwards | `meta-rewriting-antiai` (optional follow-up; never auto-chained) |

If the user asks for style *extraction*, hand off to `metasci-style-extraction`.
If the user asks for logic/argument review, hand off to `meta-review`.

---

## Input Contract

**Required:**
1. Draft text to revise (sentence / paragraph / section / full manuscript) + its
   section type (Introduction / Methods / Results / Discussion, or report chapter).
2. A style profile folder produced by `metasci-style-extraction`:
   `Style_{destination}/style_profile.md` (+ `cards/*_style.md`).

**Optional:**
- Revision intensity: Light (vocabulary/expressions only) / Standard (default;
  expressions + sentence-level structure) / Deep (full stylistic rewrite).
- Source mixing via Pick-list: e.g. "서론은 Smith 카드, 헤징은 Lee 카드 기준으로".

**Legacy input:** if given an old-format data bank (24-table `{Author}{Year}_style.md`
or `.json` from meta-styling v1.x), do NOT attempt to consume it. Explain that the
format is superseded and offer to re-extract with `metasci-style-extraction`
(re-extraction is cheap; the new profile carries measured counts).

**Korean documents (EXPERIMENTAL):** Korean drafts are supported when the profile
was extracted from Korean references (see `metasci-style-extraction`'s
`lens-korean.md`). `quant_check.py` auto-detects Korean and switches to Korean
hedging/passive inventories. This path is not yet field-validated — label the
report `[Korean mode — experimental]`.

---

## Workflow

**Always read `references/revision_guide.md` first — it defines each phase's
procedure and output format.**

```
Phase 0: Load Guide
  → Read references/revision_guide.md

Phase 1: Input Analysis
  → Draft + section type + profile path + intensity
  → Read style_profile.md (and any cards named by the user)

Phase 2: Measured Diagnosis
  → Save draft to a temp .txt; run scripts/quant_check.py profile (and count
    for profile vocabulary items) on it
  → Build the Draft vs Target table (measured values side by side)
  → LLM judgment ONLY for unmeasurable dimensions (tense, person, citation
    integration, sentence-frame usage)

Phase 3: Prescription
  → Convergence items → firm rules, apply
  → Divergence items → follow the draft's existing lean; consistency only;
    record as "choice points" in the report
  → Every prescription cites its profile/card evidence

Phase 4: Revision
  → Produce revised text per intensity level; preserve academic content exactly

Phase 5: Post-Revision Verification
  → Re-measure the revised text with quant_check.py
  → Before / After / Target table
  → If a measured dimension is still outside the target band: ONE corrective
    re-pass, then report honestly if still out (no loops)

Phase 6: Report
  → Diagnosis, changes with evidence, choice points, measured verification
  → Close with optional next steps (meta-review for logic; meta-rewriting-antiai
    for AI-trace removal) — mention only, never auto-run
```

---

## Quality Criteria

1. **Measured, not estimated**: every number in diagnosis/verification comes from
   `quant_check.py`; qualitative judgments are labeled as such
2. **Evidence-based**: every revision cites a convergence rule, card frame, or
   measured gap
3. **Content preservation**: the academic content (claims, data, citations) is
   never altered — style only
4. **Divergence respected**: reference disagreements are the writer's choice, not
   errors; never silently impose one side
5. **Honest verification**: out-of-band results after the re-pass are reported,
   not hidden

---

## Error Handling

| Situation | Response |
|-----------|----------|
| No style profile found | Guide user to run metasci-style-extraction first |
| Old-format data bank given | Explain supersession; offer re-extraction |
| Draft section type unknown | Ask, or infer and confirm |
| Draft too short to measure (<100 tokens) | Warn: measured rates unstable; diagnose qualitatively, mark as such |
| Korean draft + English-only profile | Stop: profile and draft language must match |
| Revised text still out of band after re-pass | Report the gap and its likely cause |

---

## Usage Examples

```
# Standard: revise a section against a profile
> "내 Introduction을 Style_EIA_LLM 프로필로 교정해줘"

# Light touch
> "이 단락 어휘만 프로필에 맞춰줘 (Light)"

# Source mixing
> "전체는 profile 따르되 헤징은 Smith2021 카드 수준으로"

# Korean report (experimental)
> "이 보고서 2장을 Style_KEI 프로필로 다듬어줘"
```

---

**Version**: 2.0.0 (apply-only; measured diagnosis/verification; Mode A removed —
extraction now lives in metasci-style-extraction)
**Skill**: Meta_researcher / meta-styling
