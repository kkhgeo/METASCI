# Output Format Rules (v12 — lines only, no italic, no blockquote bar)

## Language Policy

- **Review target:** English academic papers
- **All output to user:** Korean (한국어)
- **English original text:** Always displayed alongside Korean translation
- **Agent internal prompts:** English (for optimal LLM performance)

---

## Visual Design Principles (MANDATORY)

### 1. The coloring problem and how v6 solves it

Claude Code renders output through **React (Ink) + chalk**. Implications:

- Raw ANSI escape sequences (`\033[36m` etc.) emitted as text are
  **stripped or shown literally** — ANSI doesn't reach chalk this way.
- BUT chalk *does* color text indirectly, through **markdown tokens** the
  renderer translates into Ink components:
  - `` `inline code` `` → monospace + tint background/foreground (often
    cyan/blue depending on the user's theme).
  - `> blockquote` → left rule + dimmer foreground (gray-ish).
  - `**bold**` / `*italic*` → bold/italic with theme-driven color shift.
  - `### H3 / ## H2 / # H1` → bold + emphasis color.
  - Fenced code blocks ```` ``` ```` → monospace, distinct background.

The v6 strategy: **mix code blocks (for line/box structure) with
markdown tokens (for color and emphasis) by deliberately breaking out
of code blocks where coloring is needed.**

The previous v5 wrapped everything in one code block, which preserved
alignment but flattened all color. v6 sacrifices some alignment in
exchange for chalk-applied color via markdown.

### 2. Lines, not boxes

The v6 default is **horizontal-rule line pattern**:

- `══════════════════════════════════════════════════════════════════════════════════════════════════` (top-bottom of card titles, double rule, ~100 chars)
- `──────────────────────────────────────────────────────────────────────────────────────────────────` (sub-section dividers, single rule, ~100 chars)

**No more `┌─┐ │ └─┘` full boxes anywhere.** The right-edge alignment
under Korean text was the failure mode; lines have no right edge to
break.

Use `══` for major divisions (card titles, between cards), `──` for
minor divisions (sub-sections within a card, action prompts).

### 3. Width target

Horizontal rule width: **~100 characters** of `═` or `─`. This is the
v6 calibration; fits standard CLI windows comfortably.

### 4. Where color comes from (markdown token map — v12)

**v12 ban list:**
- ❌ `> blockquote` (좌측 수직선 + dim+italic 결합 토큰) — 전면 금지.
- ❌ `*italic*` — 본문 어디에도 사용 안 함.

**Allowed tokens:**

| Need | Markdown token | Chalk effect (typical theme) |
|---|---|---|
| Section/card title | `### #1 ▲ HIGH` | bold + emphasis color |
| Sub-section label | `**라벨명**` | bold + slightly brighter |
| Severity HIGH | `**▲ HIGH**` (bold) | bold red-shift in most themes |
| Severity MED | `**● MED**` (bold) | bold |
| Severity LOW | `○ LOW` (no bold) | normal |
| Recommended option | `**추천: A**` | bold |
| Citation / key term emphasis | `**Kuhn (1977)**`, `**inductive risk**` | bold (semantic only) |
| Action/nav prompts | `` `"1번"` · `"다음"` `` (inline code) | monospace + tint |
| Reference verification status | `` `▲ 미확인` `` | monospace token for status |
| English / Korean body text | plain prose (no token) | regular weight |

**원문/번역 위계:** bold 강조의 **밀도**로만 표현. 원문은 학술 용어/저자-연도에 bold,
번역은 동일 위치에 bold. 이탤릭이나 좌측 막대 같은 구조 토큰 사용 안 함.

**Crucial**: 모든 본문은 **plain text outside code blocks**. 라인(`══` / `──`)도
plain text. 박스/blockquote/이탤릭 같은 구조 토큰을 쓰지 않으므로 한국어 폭 mismatch
문제도 자동 회피됨.

### 5. Long English / Korean blocks (v12 — plain prose only)

**Visible width target: ~90-95 characters per line.** Hard wrap.
Renderer auto-wrap is unreliable across viewport widths, so we wrap
manually for both languages.

Horizontal rules (`══` / `──`) stay at ~98-100 chars, deliberately
**slightly longer than the content**, creating visual margin.

**Body policy (v12):**
- **모든 본문 = plain prose.** No `>` blockquote, no `*italic*`, no
  inline-code wrapping for body text. Use only `**bold**` for citations
  and key terms.
- 따옴표(`"..."`)도 본문 인용 표지로 쓰지 않음 — 라인 헤더(`**원문**`,
  `**번역**`)가 이미 인용 블록임을 표시.
- 빈 줄로 의미 단락 분리.

**English original — manual sentence wrap:**

One paragraph break between meaning units. Hard wrap at ~90 visible chars.
**bold** on author-year citations and key technical terms only.

```
Several lines of scholarship converge on this point.

**Kuhn (1977)** demonstrated that even in the natural sciences, the criteria governing
theory choice (accuracy, consistency, scope, simplicity) function as **values** that act
to limit judgment without dictating it.

**Douglas (2000, 2009)** formalised this insight through the concept of **inductive risk**:
whenever scientists accept or reject a hypothesis, they face the possibility of error, and
the consequences of **false positives** and **false negatives** are rarely symmetric.
```

**Korean translation — plain prose, manual wrap:**

```
여러 학술 계보가 이 지점에서 수렴한다. **Kuhn(1977)** 은 자연과학에서조차 이론 선택을
지배하는 기준(정확성, 일관성, 범위, 단순성)이 판단을 제약은 하되 결정하지는 않는
**가치(value)** 로 작동한다는 점을 보였다.

**Douglas(2000, 2009)** 는 이 통찰을 **'귀납적 위험(inductive risk)'** 개념으로
공식화했다 — 과학자가 가설을 채택·기각할 때마다 오류 가능성에 직면하며, **거짓 양성**과
**거짓 음성**의 결과는 좀처럼 대칭적이지 않다.
```

Each line ~45-48 한글 글자 (≈ 90-96 visible columns).
Blank line between meaning paragraphs.

**Korean explanation/rationale (short, inside cards):**

Plain prose, ~90-95 chars per line, manual line breaks. Bold labels
on their own line above (e.g. `**문제**`, `**근거**`).

**Label-value lists (intent confirmation, sub-sections):**

Plain prose with `**라벨** — 값` pattern, no fenced code block, no
hanging indent. Each label on its own paragraph, blank line separator.

### 6. Emoji discipline

Only severity markers: `▲ HIGH` / `● MED` / `○ LOW` / `■ CRITICAL`.
Distinctive shapes alone carry severity; bold (`**▲**`) adds chalk
emphasis where the renderer applies it.

No 📍 ⚠ ✏ 🔗 💡 🔴 🟡 ✓ ★ — ever.

### 7. Plain prose vs structural blocks

- **Bridging sentences** ("이 의도 맞으면 'ㅇ' 해주세요") → plain
  Markdown prose, no special structure.
- **Structural blocks** (priority table, issue cards, intent
  confirmation, pacing, session summary) → use the line pattern with
  inline-code/blockquote/bold tokens for content.

---

## Tier System (HOW MUCH detail to show)

Default = **Tier 1**. Higher tiers only on explicit user request.

| Tier | What is shown | When |
|---|---|---|
| **Tier 1** | Top-3 priority table + nav line. ≤ 12 lines. | Default first response per unit |
| **Tier 2** | Single issue card (full detail) | User says `"1번"`, `"#3 자세히"` |
| **Tier 3** | All consensus/unique/conflict cards in sequence | User says `"다 보여줘"`, `"전체 보기"` |

### Mapping to existing modes

| Mode | Tier 1 default | Tier 3 list |
|---|---|---|
| Mode 1 (Paper) | Top-3 sections | Full Top-5 + all reviewer findings |
| Mode 2 (Section) | Top-3 paragraphs | Full Top-5 + all reviewer findings |
| Mode 3 — paragraph phase | Top-3 issues | All issues for the paragraph |
| Mode 3 — sentence phase | Single issue card per sentence | n/a |

### Suppression

If zero issues exist:

```
──────────────────────────────────────────────────────────────────────────────────────────────────
이 [모드 단위]에서 우선 수정할 항목이 없습니다.
──────────────────────────────────────────────────────────────────────────────────────────────────
```

---

## Tier 1 — Compact Summary (default first view)

The priority table itself stays as a small fenced code block (English
labels, fixed widths, alignment matters). Header and nav are plain-text
lines outside the code block so chalk applies.

```
══════════════════════════════════════════════════════════════════════════════════════════════════
```
### 단락 [N/총개수] · [섹션명]

**지금 꼭 봐야 할 [N]가지**

```
┌────┬────────┬─────────────────┬──────────────────────────────────────────────────────────┐
│ #  │ 심각도 │ 카테고리        │ 한 줄 요약                                               │
├────┼────────┼─────────────────┼──────────────────────────────────────────────────────────┤
│ 1  │   ▲    │ [category]      │ [≤50자 요약]                                             │
│ 2  │   ▲    │ [category]      │ [≤50자 요약]                                             │
│ 3  │   ●    │ [category]      │ [≤50자 요약]                                             │
└────┴────────┴─────────────────┴──────────────────────────────────────────────────────────┘
```

```
──────────────────────────────────────────────────────────────────────────────────────────────────
```
자세히 `"1번"` · `"2번 펼쳐"` · `"다 보여줘"`  |  진행 `"다음"` · `"이 단락 다시"`

The `### 단락…` is an H3 header → chalk applies bold+emphasis color.
The action line uses inline code (`` `…` ``) for the literal user inputs
so chalk styles them as monospace + tint. No italics anywhere.

---

## Tier 2 — Single Issue Card (v12)

**v12 카드 규칙:**
- 모든 sub-section 헤더는 **3-라인 패턴** (`──` / `**라벨**` / `──`).
- `▌` 좌측 막대 사용 안 함.
- 본문은 plain prose. blockquote/이탤릭 없음.
- 영문/한국어 모두 평문, **bold**로 핵심만 강조.

### 2a. Single-alternative card (LOGIC / FACTUAL / STRUCTURE)

```
══════════════════════════════════════════════════════════════════════════════════════════════════
```
### #1 **▲ HIGH** · [한국어 카테고리 이름]

**발견자:** R1+R3 합의

──────────────────────────────────────────────────────────────────────────────────────────────────
**위치 (원문)**
──────────────────────────────────────────────────────────────────────────────────────────────────

[problematic English text. Plain prose. ~90자 wrap. **bold** on the actual problem token.]

──────────────────────────────────────────────────────────────────────────────────────────────────
**문제**
──────────────────────────────────────────────────────────────────────────────────────────────────

[한국어 설명. 독자 관점에서 왜 문제인지. ≤2 문장. ~90-95자 wrap.]

──────────────────────────────────────────────────────────────────────────────────────────────────
**수정안**
──────────────────────────────────────────────────────────────────────────────────────────────────

[revised English text. Plain prose. **bold** on the changed token.]

──────────────────────────────────────────────────────────────────────────────────────────────────
**근거**
──────────────────────────────────────────────────────────────────────────────────────────────────

[어떤 규칙/자료에 근거한 지적인지 한 줄.]

──────────────────────────────────────────────────────────────────────────────────────────────────
적용 `"1번 적용"` · 거절 `"1번 무시"` · 진행 `"다음"`

### 2b. Multi-alternative card (STYLE / HEDGING / TERMINOLOGY / CLUTTER)

Opening through `**문제**` block identical to 2a, then:

──────────────────────────────────────────────────────────────────────────────────────────────────
**수정 대안 ([N]개 · 톤 선택)**
──────────────────────────────────────────────────────────────────────────────────────────────────

**A · [tone label]**

[alternative A text — plain prose, ~90자 wrap.]

근거 — [한 줄 근거.]

**B · [tone label]**

[alternative B text.]

근거 — [한 줄 근거.]

**C · [tone label]**

[alternative C text.]

근거 — [한 줄 근거.]

──────────────────────────────────────────────────────────────────────────────────────────────────
**추천: A** — [추천 이유 한 줄.]

──────────────────────────────────────────────────────────────────────────────────────────────────
적용 `"3번 A 적용"` · `"3번 B 적용"` · `"3번 C 적용"` · 진행 `"다음"`

### 2c. Conflict card (reviewers disagree)

```
══════════════════════════════════════════════════════════════════════════════════════════════════
```
### #2 **▲ HIGH** · [한국어 카테고리 이름]

**의견 충돌:** R1 ↔ R4

──────────────────────────────────────────────────────────────────────────────────────────────────
**위치 (원문)**
──────────────────────────────────────────────────────────────────────────────────────────────────

[problematic English text. Plain prose.]

──────────────────────────────────────────────────────────────────────────────────────────────────
**충돌 내용**
──────────────────────────────────────────────────────────────────────────────────────────────────

[왜 의견이 갈리는지 한국어 설명. ≤2 문장.]

──────────────────────────────────────────────────────────────────────────────────────────────────
**R1 의견**
──────────────────────────────────────────────────────────────────────────────────────────────────

**수정안** — [R1 alternative — plain prose.]

**근거** — [R1 rationale.]

──────────────────────────────────────────────────────────────────────────────────────────────────
**R4 의견**
──────────────────────────────────────────────────────────────────────────────────────────────────

**수정안** — [R4 alternative — plain prose.]

**근거** — [R4 rationale.]

──────────────────────────────────────────────────────────────────────────────────────────────────
선택 `"R1 따름"` · `"R4 따름"` · `"직접 입력"` · 보류 `"건너뛰기"`

---

## Tier 3 — All Cards in Sequence

Order:
1. Tier 1 priority table (recap)
2. All consensus cards (▲ first, then ●, then ○)
3. All unique-finding cards
4. All conflict cards
5. Final nav

Cards separated by `══` rules.

---

## Paragraph End — Pacing Block

```
══════════════════════════════════════════════════════════════════════════════════════════════════
```
### 단락 [N/총] ¶[K] 완료

**이번:** ▲ [a]건 · ● [b]건 · ○ [c]건
**누적:** ▲ [A]건 · ● [B]건 · ○ [C]건

**진행률** `[████████░░░░░░░░░░░░]` [N/총] ([P]%)

──────────────────────────────────────────────────────────────────────────────────────────────────
다음 단락([N+1/총] · §[X.Y] ¶[K+1])으로 갈까요?
`"네"` · `"잠깐"` · `"이 단락 다시"`

The progress bar inside `` `…` `` becomes monospace + tinted, making
it stand out as a visual gauge.

---

## Mode 3 — Intent Confirmation Block (v12)

**Design rationale (typography review feedback applied):**

- **이탤릭 전면 금지** — blockquote(좌측 수직선 + 이탤릭+dim 결합 토큰)도 사용 안 함.
- **좌측 수직선(`>` 마커) 전면 제거** — 모든 본문은 평문 prose.
- 원문/번역 시각 위계는 **bold 강조의 밀도**로만 표현 (원문 = 인용/용어 bold / 번역 = bold 동등 적용).
- `¶` 표기 — `§2.1 ¶2` (학술 표준).
- 저자-연도 / 핵심 용어 bold — `**Kuhn (1977)**`, `**inductive risk**`, `**post-normal science**`.
- 블록 헤더 = 3-라인 패턴 (위 라인 / 라벨 / 아래 라인).

```
══════════════════════════════════════════════════════════════════════════════════════════════════
```
### 단락 [N/총] · §[X.Y] ¶[K]

```
──────────────────────────────────────────────────────────────────────────────────────────────────
```
**원문**
```
──────────────────────────────────────────────────────────────────────────────────────────────────
```
Several lines of scholarship converge on this point.

**Kuhn (1977)** demonstrated that even in the natural sciences, the criteria governing theory
choice (accuracy, consistency, scope, simplicity) function as **values** that act to limit
judgment without dictating it.

Two scientists applying the same criteria but weighting them differently may legitimately
arrive at divergent conclusions.

**Douglas (2000, 2009)** formalised this insight through the concept of **inductive risk**:
whenever scientists accept or reject a hypothesis, they face the possibility of error, and
the consequences of **false positives** and **false negatives** are rarely symmetric.

```
──────────────────────────────────────────────────────────────────────────────────────────────────
```
**번역**
```
──────────────────────────────────────────────────────────────────────────────────────────────────
```
여러 학술 계보가 이 지점에서 수렴한다. **Kuhn(1977)** 은 자연과학에서조차 이론 선택을
지배하는 기준(정확성, 일관성, 범위, 단순성)이 판단을 제약은 하되 결정하지는 않는
**가치(value)** 로 작동한다는 점을 보였다. 같은 기준을 쓰더라도 가중치가 다르면 두
과학자는 합법적으로 다른 결론에 이를 수 있다.

**Douglas(2000, 2009)** 는 이 통찰을 **'귀납적 위험(inductive risk)'** 개념으로
공식화했다 — 과학자가 가설을 채택·기각할 때마다 오류 가능성에 직면하며, **거짓 양성**과
**거짓 음성**의 결과는 좀처럼 대칭적이지 않다.

```
──────────────────────────────────────────────────────────────────────────────────────────────────
```
**의도 확인**
```
──────────────────────────────────────────────────────────────────────────────────────────────────
```
**핵심 메시지** — Kuhn–Douglas–F&R 계보를 동원해, 과학적 판단조차 가치 가중에서 자유로울
수 없으며 EIA의 유의성 판단도 마찬가지로 규범적 결정임을 입증.

**섹션 내 역할** — 근거(evidence). 직전 단락이 제기한 "significance determination이
가치 판단을 내재한다"는 주장을 외부 학술 권위로 뒷받침.

**핵심 주장** — EIA의 거짓 음성 vs 거짓 양성 비용의 비대칭은 어느 오류를 더 용인할지를
결정하게 만들며, 이는 과학적이 아니라 규범적 판단이다. **Post-normal science** 조건의
정확한 사례.

```
──────────────────────────────────────────────────────────────────────────────────────────────────
```
맞으면 `"ㅇ"` · 다르면 `"수정: [내용]"`

**v11 핵심 규칙:**

- **원문/번역 위계**: 원문은 평문(roman, no italic), 번역은 `>` blockquote (dim, 보조).
  검토자의 시선이 자연스럽게 ground truth(원문)에 우선 가도록.
- **이중 부호화 제거**: blockquote 안에 따옴표 안 씀. `>` 마커가 이미 인용 블록을 표지.
- **인용/용어 강조**: 저자-연도와 핵심 용어에만 `**bold**`. 본문 전체에 italic 도배 안 함.
- **¶ 표기**: `§2.1 ¶2` 형식 (학술 표준). `(두 번째)` 같은 자연어 표기 회피.
- 콘텐츠 한 줄당 ~90-95 visible columns.
- 의도 확인은 blockquote (정리/요약 = 보조 정보 위계).

**Wrap 폭 가이드:**
- 라인 길이: ~98자 (`──` × 98).
- 콘텐츠 한 줄: ~90-95자 (라인보다 약간 짧게).
- 영문/한국어 모두 동일한 폭 목표.

---

## Mode 3 — Sentence Review Block (v12)

```
══════════════════════════════════════════════════════════════════════════════════════════════════
```
### 단락 [N] ¶[K] · 문장 [M/총] · §[X.Y]

──────────────────────────────────────────────────────────────────────────────────────────────────
**문맥 (이전 문장)**
──────────────────────────────────────────────────────────────────────────────────────────────────

[previous sentence — plain prose, ~90자 wrap.]

──────────────────────────────────────────────────────────────────────────────────────────────────
**검토 대상**
──────────────────────────────────────────────────────────────────────────────────────────────────

[current sentence — plain prose. **bold** on the trigger token if issue is localized.]

──────────────────────────────────────────────────────────────────────────────────────────────────
**번역**
──────────────────────────────────────────────────────────────────────────────────────────────────

[한국어 번역 — 평문. ~45-48 한글 글자 wrap.]

Then issue cards (Tier 2 format, v12 rules). If no issue:

──────────────────────────────────────────────────────────────────────────────────────────────────
**전원 동의** — 이 문장에 수정 필요 없음.

──────────────────────────────────────────────────────────────────────────────────────────────────
진행 `"다음"` · 상세 `"그래도 자세히 봐줘"`

---

## Mode 3 — Reference Verification Block (v12)

──────────────────────────────────────────────────────────────────────────────────────────────────
**레퍼런스 확인**
──────────────────────────────────────────────────────────────────────────────────────────────────

| REF | 상태 | 제목 |
|---|---|---|
| Author (Year) | `▲ 미확인` | [...] |
| Author (Year) | `● 일부확인` | [...] |
| Author (Year) | `○ 확인됨` | [...] |

Status markers in inline code → chalk applies monospace + tint.

---

## Session Summary (end of session)

```
══════════════════════════════════════════════════════════════════════════════════════════════════
```
### 교정 세션 요약

```
──────────────────────────────────────────────────────────────────────────────────────────────────
```
**검토 범위**

- **모드**: [사용된 모드 목록]
- **단위**: 섹션 [N] · 단락 [N] · 문장 [N]
- **리뷰어**: [N]명

```
──────────────────────────────────────────────────────────────────────────────────────────────────
```
**이슈 분포**

- **합의**: [N]건
- **고유 발견**: [N]건
- **의견 충돌**: [N]건

```
──────────────────────────────────────────────────────────────────────────────────────────────────
```
**사용자 결정**

- **수정 적용**: [N]건
- **승인**: [N]건
- **건너뛰기**: [N]건

```
──────────────────────────────────────────────────────────────────────────────────────────────────
```
**정합성 점검 (Agent B)**

- **레퍼런스 미확인**: [N]건
- **수치 불일치**: [N]건
- **2차 인용 경고**: [N]건
- **추가 검색 실행**: [N]회

```
──────────────────────────────────────────────────────────────────────────────────────────────────
```
**수정 이력**

| # | 원문 | 수정문 | 근거 |
|---|---|---|---|
| 1 | [original] | [revised] | [합의/R1/R2/...] |

---

## Plain Explanation Rules (mandatory inside `문제` blocks)

- Use plain Korean. No jargon ("Given-New", "nominalization",
  "stress position") — translate or rephrase.
- Frame as reader experience: "이 문장을 읽으면…", "독자 입장에서는…".
- Compare original and suggestion specifically when relevant.
- Stay within 2 sentences.

---

## Width Calibration Quick Reference

- Horizontal rules (`══` / `──`): 100 characters total.
- Inline code (`` `…` ``): no width budget — renderer wraps.
- Blockquote (`>`): break manually at ~80 visible chars per `>` line
  for predictable wrapping.
- Tier 1 priority table: keep inside a fenced code block; ~100 chars
  total table width.

---

## What changed v5 → v6

| Aspect | v5 | v6 (current) |
|---|---|---|
| English quotes (v6) | Inline code (monospace + tint) | **Plain prose**, **bold** on citations/key terms |
| Korean translation (v6) | `> blockquote` (left rule + dim italic) | **Plain prose**, **bold** on citations/key terms |
| Italics | Action prompts + via blockquote | **Banned everywhere** |
| Left vertical bars | `>` blockquote rule, `▌` markers | **Banned everywhere** — lines only |
| Sub-section labels | `**▌ 라벨**` | **3-line header** (`──` / `**라벨**` / `──`) |
| Quotation marks around quoted content | `"..."` inside blockquote | **Removed** (header marks the block) |
| Paragraph reference | `(두 번째)` | **`¶2`** (academic standard) |
| Citation/term emphasis | None | **`**bold**`** on author-year and key terms |
| Width target | ~70-75 chars | **~90-95 chars** |
| Action prompts | `*"X"*` (italic + inline code) | `` `"X"` `` (inline code only) |

The v12 principle: **type only — no structural decoration.** Lines for
section breaks, bold for semantic emphasis, inline code for literal
user inputs. Everything else is plain prose. This sidesteps Korean-vs-
English column-width misalignment and removes the italic+monospace
double-coding that hurt long-read fatigue (per Hochuli/Bringhurst).

---

## Fallback

If user reports any rendering issue, switch to v5 (boxes + lines hybrid)
on request — file `output_format.md.v5-pre-coloring` is preserved as the
backup.
