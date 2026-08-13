---
name: meta-writing-blog
description: Turn a paper, a manuscript, or a topic into a KEI AI 융합연구단 "브리프" — a self-contained Korean HTML explainer in the KEI house style, output as a portable folder. Triggers: "브리프 작성", "KEI 브리프로 만들어줘", "이 논문 브리프로 써줘", "논문 소개 글 만들어줘", "write a paper explainer".
---

# meta-writing-blog

Turn a source (a paper, a manuscript folder, or the user's notes/topic) into a **KEI 브리프** —
a self-contained Korean HTML explainer that makes the material *understandable*, not just
summarized. Output is **Korean-only** and rendered in the KEI house style.

Two things define it:
- **Voice** — quiet editorial exposition: impersonal, precise, hedged (`–다`체). Keep the
  pedagogy of a good explainer (problem before solution, intuition before notation) but not a
  chatty tone. 박스·그라디언트·이모지는 쓰지 않는다. Rules in `references/voice-and-structure.md`.
- **Design** — the KEI brief template (`assets/brief-template.html`) carries the whole design
  **inline**: KEI palette, typography, and every component (callout, var-list, figure-equations,
  data-table, comparison-grid, figure-canvas, explorer-box, APA references). Copy it; do not
  invent a new framework or hand-roll CSS. Components in `references/STYLE_GUIDE.md`.

## Output

A new self-contained folder (kebab-case `brief-{slug}`, in the current directory):

```
brief-<slug>/
├── brief-<slug>.html   # the brief (a copy of assets/brief-template.html, filled in; CSS inline)
├── assets/             # bundled brand assets — copy of the skill's assets/hero-bg.jpg + KEI_Wordmark.svg
└── figures/            # figures referenced by the brief (if any)
```

All asset paths inside the HTML are **local** (`assets/…`, `figures/…`) — never `../`. Only the
webfonts load from a CDN, so with internet the brief renders fully; without it, only the fonts
fall back and the layout, hero image, and visualizations still work. At the end, tell the user
the folder path and how to open it.

> This skill does **not** write into the live KEI site (`release/`). It copies brand assets out
> and produces a portable folder. To later publish a brief into the real site, move the HTML into
> `release/briefs_files/`, repoint `assets/…` → `../assets/…`, restore the logo/Back/end-nav
> links (marked in the template), and add a row to `briefs.html` per STYLE_GUIDE §8.

## Workflow

**1. Get the source.** Paper: arXiv → WebFetch the abstract; full text → the **markitdown** skill
on the PDF/HTML. Manuscript folder → read every HTML/CSS/JS/MD in it. Topic/notes → use directly.
Determine the **field labels** (English, 1–3, e.g. `Climate · Dynamical systems`). Don't block on
questions you can answer by reading the source.
- **컨텍스트 가드**: 변환본이 길면(대략 30KB↑) 원문 전체를 메인 컨텍스트에 넣지 않는다 —
  서브에이전트(Agent)가 블루프린트 재료만 추출해 오게 한다: 핵심 기여 1문장, 문제·왜 어려운가,
  방법의 뼈대, 헤드라인 수치와 한계, 그림·표 목록, 핵심 인용문헌(서지 포함). 본문 집필 중
  특정 세부가 필요해지면 그 부분만 다시 조회한다.

**2. Blueprint the narrative (don't skip).** Read `references/voice-and-structure.md`. First fix the
**mission** in one line — *who is this brief for, and why would they read it* (the reader's stake).
Then map the source onto the flexible section arc: opening (problem) → central idea → where it
matters → the problem precisely → why hard → method → results → outlook. The load-bearing rule:
**the reader meets the problem before the method.** Sections are flexible — merge, split, rename —
but keep that order. For two or more papers, use the shared-spine variant (one problem, parallel
cases, a synthesis), not one pass per paper. Decide the **title** and the **slug**.

**3. Scaffold.** Create `brief-<slug>/`. Copy `assets/brief-template.html` →
`brief-<slug>/brief-<slug>.html`. Create `brief-<slug>/assets/` and copy the skill's bundled brand
assets into it (`assets/hero-bg.jpg`, `assets/KEI_Wordmark.svg`). Create `brief-<slug>/figures/`.
Edit the copy — don't author the chrome from scratch.
- **컨텍스트 가드**: 템플릿 34KB 중 `<style>` 블록(~23KB)은 불변이므로 **읽지 않는다.**
  Grep으로 `<body>` 행 번호를 찾은 뒤, Read는 두 구간만 — head의 [REPLACE] 구간(1~40행)과
  `<body>` 이후 본문. 이후 편집은 전부 그 범위 안에서 이뤄진다.

**4. Fill the head.** `<title>` (`{제목} · KEI AI 융합연구단`) and `<meta name="description">`.

**5. Fill the article header.** page-label (`Brief`), `<h1>` title, subtitle (optional), byline
(author pattern per STYLE_GUIDE §3.3 — e.g. `AI 생성 · 김경호 검토`), date `YYYY.MM.DD`, field labels.

**6. Abstract.** 1–3 sentences in `.article-abstract`, formal register. **원 논문의 출처를
초록 안에 명시한다** — 저자(연도), 논문 제목, 식별자(arXiv ID 또는 DOI). 콜로폰·References에만
두는 것으로는 부족하다; 독자는 첫 화면에서 무엇에 기초한 해설인지 알 수 있어야 한다.

**7. Write the body.** Fill the `<section>`s in the KEI editorial voice. Map content to the
components in `references/STYLE_GUIDE.md` §4: callout (`callout-warn` for warnings), var-list for
symbol definitions, figure-equations for math (typeset directly with Unicode + `<sub>`/`<sup>`, no
KaTeX), data-table for tabular results, comparison-grid for parallel cases, **figure-image for
static figures (the most common case — paper figures, maps, chart images)**, figure-canvas /
explorer-box for animated/interactive visualizations. **Delete any component example you don't use.** Korean-only: gloss
awkward or untranslatable terms with English in parentheses, e.g. `보유(retention)`.

**8. References.** APA 7 hanging-indent in `.references` (DOI URL preferred). Cite the source paper
plus its key references.

**9. Colophon & nav.** Fill or delete the `.colophon`. Leave the end-nav commented out (no briefs
list in a standalone folder) unless publishing to the site.

**10. Interactivity.** Any canvas/explorer runs from an inline `<script>` with **lazy-start** via
`IntersectionObserver` (the template's demo shows the pattern). Replace the demo's draw functions
with your visualization, or delete the demo blocks + script if unused. Keep interactivity spare in
this register.

**11. 문체 재작성 — meta-mywriting-korean 패스 (발간 전 필수).** 초안의 제목과 설명 산문에는
AI 티가 남는다. 완성된 HTML의 **모든 한국어 산문** — 제목(h1)·부제·초록·본문 단락·callout·
캡션 — 을 **meta-mywriting-korean** 스킬로 한 번 재작성한 뒤에야 전달한다.
- **호출 — 반드시 서브에이전트로 격리한다.** mywriting의 참조 파일(Blueprint 39.6KB +
  anti-AI 패턴 28.5KB + 출력형식 등 ~97KB)과 초안 원문·재작성본을 메인 컨텍스트에 올리면
  이 시점에 대화가 요약될 위험이 있다. **Agent(general-purpose)** 하나를 띄우고 프롬프트에
  다음을 담는다: (a) 브리프 HTML의 절대 경로, (b) "`~/.claude/skills/meta-mywriting-korean/`의
  SKILL.md와 references를 직접 읽고 그 파이프라인을 따르라"는 지시, (c) 설정 — **Mode B(전면
  리라이팅)**, 문서 유형 "해설(브리프)", AI 생성 "예", 사용자 프롬프트 대기 없음, (d) 아래
  적용 범위 블록 **전문**. 서브에이전트는 HTML을 제자리 편집하고 **변경 요약표 + 근거
  인벤토리(`[미확인]` 표) + 사후 검증 결과만** 반환한다 — 재작성된 본문을 텍스트로 되돌려보내지
  않는다.
- **적용 범위 — 브리프 보이스가 우선한다:**
  - 섹션·단락의 순서와 개수는 바꾸지 않는다 (구성은 2단계 블루프린트가 결정했다).
  - HTML 마크업·컴포넌트·수식·figure는 건드리지 않는다 — 텍스트 노드만.
  - References의 APA 표기·DOI, 수치·단위, 용어 글로스 `용어(term)`는 한 글자도 바꾸지 않는다.
  - Blueprint의 정책 장르 요소(당위 표현, 열거형 제안, 「법명」 인용 형식)는 적용하지 않는다 —
    문장 구조(Dim 2)·전환어(Dim 4)·어휘(Dim 5)·**AI 패턴 제거(Dim 7)** 중심으로 적용한다.
  - 베아트리체 모드면 연속 산문·분량 상한·종합 문장 마무리를 깨지 않는 범위에서 적용한다.
- 재작성 후 변경 요약표를 보존하고, 근거 인벤토리(PHASE 3c)의 `[미확인]` 항목이 있으면
  전달 보고에 첨부한다.

**12. Check & deliver.** Verify: no `../` paths remain in the HTML, every `figures/…` `src` exists,
no `[REPLACE …]` markers left, brand assets are present in the folder's `assets/`. Optionally serve
locally (`python -m http.server 8000`) and open `brief-<slug>/brief-<slug>.html`. Report the folder
path and how to open it, plus any placeholders left for the user.

## Quality checklist
- [ ] Opens by framing the problem/gap — not "이 논문은 ~을 제안한다" or an anecdote.
- [ ] Voice stays quiet-editorial academic: impersonal, hedged, `–다`체; 박스·그라디언트·이모지 없음.
- [ ] Problem (why-hard) precedes the method; method builds simplest-first; math follows the idea it formalizes.
- [ ] Multi-paper: shared problem spine + parallel cases + synthesis — not N independent summaries.
- [ ] Korean reads naturally on its own; awkward terms glossed `용어(term)` once on first mention.
- [ ] Components used correctly (callout / var-list / data-table / etc.); unused component examples deleted.
- [ ] Figure captions are objective; interactivity is sparing and lazy-started.
- [ ] References in APA hanging-indent; DOI URLs where available.
- [ ] 발간 전 **meta-mywriting-korean 재작성 패스**를 거쳤다 — 제목·부제·초록 포함, 변경 요약표 보존, 구성·수치·APA 불변.
- [ ] All asset paths local (`assets/…`, `figures/…`); no `../`; no `[REPLACE …]` left; brand assets bundled.

## Reference files (read on demand)
- `references/voice-and-structure.md` — the quiet-editorial voice, the flexible section arc (+ multi-paper variant), the Korean-only + parenthetical-English convention, AI-tell phrases. **Read once at step 2 — it stays in force through step 7; do not re-read.**
- `references/voice-beatrice.md` — **optional voice mode; not the default.** Read it *instead of* `voice-and-structure.md` at steps 2 and 7 **only when the user explicitly asks for the 베아트리체 / Beatrice voice**. Otherwise ignore this file entirely.
- `references/STYLE_GUIDE.md` — the brief format spec: HTML skeleton, every component, color/typography tokens, author/field patterns. **Read before step 7.** (Note: it follows the canonical brief's inline-SVG logo; the Mondrian `logo-mondrian.js` mentioned in the original KEI guide is not used.)
- `assets/` — `brief-template.html` (copy and edit), plus `hero-bg.jpg` and `KEI_Wordmark.svg` (bundled brand assets to copy into each output). Copy, don't recreate.
