# 브리프 형식·컴포넌트 스펙 (STYLE_GUIDE)

KEI AI 융합연구단 **브리프** 본문 HTML의 형식·컴포넌트 규칙. 이 스킬이 만드는 결과물은
`Z:\KKH_Server\Emagine\KEI_AICR\release\briefs_files\`의 캐노니컬 브리프
**`brief-lorenz-chaos-climate.html`** 를 기준으로 하되, **독립 이식형 폴더**로 출력한다.

> 이 스킬의 `assets/brief-template.html`은 캐노니컬을 다음 항목에서 **확장**한다
> (디자인 토큰·크기는 동일): OG 메타태그, figure-image 컴포넌트, 한글 이탤릭 제거,
> `@media print`, `prefers-reduced-motion` 대응, canvas 고DPI 보정·화면 밖 정지,
> 선택형 목차(.toc). 캐노니컬로 역이식하기 전까지는 템플릿 쪽이 최신이다.

> 이 파일은 *형식·컴포넌트·토큰* 레퍼런스다. 글의 **보이스·서사 구조**는
> `voice-and-structure.md`, **오케스트레이션(소스 확보·스캐폴드·체크리스트)** 은
> `SKILL.md`를 본다.

---

## 1. 기본 원칙
- **언어**: 한국어 본문, 일반 기술 용어는 영어 그대로(e.g., transformer, ensemble) 또는
  괄호 글로스 `보유(retention)`. **이중언어 토글 없음.**
- **톤**: Distill 풍의 조용한 editorial — 박스/그라디언트/이모지 지양.
- **레이아웃**: 단일 컬럼 760px max, 좌우 32px 패딩.
- **폰트**: Paperlogy → Pretendard Variable → Inter (한글 가독성 우선). CDN 로드.
- **컬러**: KEI 팔레트(cream `#f6f0e3`, navy `#0f1624`, blue `#009fde` 등).
- **CSS는 전량 인라인** — 캐노니컬 템플릿의 `<style>` 블록을 그대로 쓴다. 프레임워크·외부
  스타일시트를 새로 만들지 않는다.

---

## 2. 출력 위치 / 명명 (독립 이식형)
브리프는 **자기완결형 폴더**로 출력한다(KEI 실사이트에 직접 쓰지 않는다):

```
brief-{slug}/
├── brief-{slug}.html     # 본문 (CSS 인라인)
├── assets/               # 번들 브랜드 자산 (hero-bg.jpg, KEI_Wordmark.svg)
└── figures/              # 본문 그림 (있을 때)
```

- slug: 영문 kebab-case (예: `brief-cnn-traffic-noise`, `brief-lorenz-chaos-climate`)
- 모든 자산 경로는 **폴더 내부 상대경로**(`assets/…`, `figures/…`). `../` 접두를 쓰지 않는다.
- 폰트만 CDN에서 로드되므로 뷰 시 인터넷이 있으면 폰트까지 완전 재현, 없으면 폰트만 폴백된다.

---

## 3. 표준 HTML 골격

### 3.1 `<head>`
- `<title>{제목} · KEI AI 융합연구단</title>`
- `<meta name="description">` 한 줄 요약 (검색용)
- **OG 태그** (SNS 미리보기 카드): `og:type`/`og:title`/`og:description`/`og:image` +
  `twitter:card`. `og:image`는 스크레이퍼가 **절대 URL만** 읽으므로 사이트 발간 시 실제
  주소로 교체한다 (독립 폴더 상태에서는 이미지 미리보기 생략 가능).
- `<meta name="theme-color" content="#f6f0e3">`
- `<link rel="icon" href="assets/KEI_Wordmark.svg" type="image/svg+xml">` (로컬)
- 폰트 link: Archivo, Inter, JetBrains Mono, Space Grotesk + Paperlogy + Pretendard
- **`../manifest.json` 링크는 넣지 않는다** (독립 폴더).

### 3.2 hero band (`<header class="hero-band">`)
- 배경: `assets/hero-bg.jpg` + scrim (로컬 번들).
- 좌상단: KEI 로고 = `<span class="dot">` + **인라인 SVG 워드마크**.
  (캐노니컬 파일은 인라인 SVG를 쓴다. Mondrian brandmark / `logo-mondrian.js`는 캐노니컬
  파일에 없으므로 이 스킬은 쓰지 않는다.)
- 로고 링크(`href`)와 우상단 `← Back`은 **독립 폴더엔 대상이 없으므로 기본 생략**한다.
  이후 KEI 실사이트(`release/briefs_files/`)로 옮겨 발간할 때 로고→`../index.ko.html`,
  Back→`../briefs.html`로 복원한다.

### 3.3 `<header class="article-header">`
```html
<header class="article-header">
  <div class="page-label">
    <span class="dot" aria-hidden="true"></span>
    <span>Brief</span>
  </div>
  <h1>{제목}</h1>
  <p class="article-subtitle">{부제 (생략 가능)}</p>
  <p class="byline">{저자 라인}</p>
  <p class="article-meta">
    <span class="date">YYYY.MM.DD</span> · <em>{분야 1} · {분야 2}</em>
  </p>
</header>
```

**저자 라인 패턴**
- 단독: `홍길동`
- 공동: `홍길동 · 박개똥`
- AI 협업: `AI 생성 · {검토자} 검토` (예: `AI 생성 · 김경호 검토`)

**분야 라벨** (영어, em으로 강조)
- 예: `Climate · Dynamical systems`, `Computer vision · Acoustics`,
  `Time-series · Forecasting`, `Remote sensing · Deep learning`, `NLP · Policy analysis`

### 3.4 abstract
```html
<p class="article-abstract">{초록 1–3문장}</p>
```
좌측 KEI 블루 선 + 18px 본문체.

### 3.5 (선택) 목차
다중 논문 브리프 등 섹션이 많을 때만, abstract 바로 뒤에 `.toc`를 넣는다
(템플릿에 주석 처리된 블록이 있다). 기본 6섹션 브리프에서는 생략.

### 3.6 본문
섹션 단위로 묶어 `<div class="article-body">` 내부에 배치:
```html
<div class="article-body">
  <section id="discovery">
    <h2>섹션 제목</h2>
    <p>...</p>
  </section>
  <section id="...">
    ...
  </section>
</div>
```

---

## 4. 사용 가능한 본문 컴포넌트

### 4.1 헤딩 / 강조
- `<h2>` 섹션, `<h3>` 하위 섹션
- `<strong>` 굵게(700, ink), `<em>` 세미볼드(600, ink) — **한글 이탤릭 금지**: 한글 폰트에
  이탤릭이 없어 가짜 오블리크가 되므로 `em`은 굵기로 강조한다. 라틴 학명·서명 등 진짜
  이탤릭이 필요하면 `<i>`를 쓴다 (References의 저널명 `<em>`은 라틴이므로 그대로 italic).
- `<a>` KEI 블루 + 점선 밑줄

### 4.2 리스트 · 인용 · 코드
- `<ul>` / `<ol>` 들여쓰기 24px
- `<blockquote>` 좌측 옅은 선 + italic
- 인라인 `<code>` 옅은 회색 배경
- `<pre><code>` 블록 좌측 선 + 모노

### 4.3 callout (정보·경고)
```html
<div class="callout">
  <p class="callout-title">제목</p>
  <p>본문</p>
</div>
```
경고는 `<div class="callout callout-warn">` — 좌측 선이 amber로.

### 4.4 변수 정의 (var-list)
수식 변수/매개변수 설명용:
```html
<dl class="var-list">
  <div class="var-row">
    <dt>x</dt>
    <dd>설명…</dd>
  </div>
</dl>
```
`dt`는 serif italic.

### 4.5 수식 블록 (figure-equations)
```html
<figure class="figure-equations">
  <div class="equations-display">
    <div class="eq-line">
      <span class="eq-lhs">dx / dt</span>
      <span class="eq-op">=</span>
      <span class="eq-rhs">σ ( y − x )</span>
    </div>
  </div>
</figure>
```
KaTeX/MathJax 없이 직접 조판한다. 유니코드 기호(σ, ρ, ≈, ²)와 `<sub>`/`<sup>`를 쓴다.

### 4.6 데이터 행 (data-table)
표 대신 grid 행 형식:
```html
<div class="data-table">
  <div class="data-row">
    <span class="data-label">라벨</span>
    <span class="data-value">값</span>
    <span class="data-note">설명</span>
  </div>
</div>
```

### 4.7 비교 카드 (comparison-grid)
3–4개 사례 나열 (carousel 아닌 흐르는 텍스트):
```html
<div class="comparison-grid">
  <div class="comparison-card">
    <h3>제목</h3>
    <p>설명</p>
  </div>
</div>
```

### 4.8 정적 그림 (figure-image)
논문 figure·지도·차트 이미지 등 **가장 흔한 그림 형태**. 파일은 `figures/`에 둔다:
```html
<figure class="figure-image">
  <img src="figures/파일명.png" alt="스크린리더용 설명" loading="lazy">
  <figcaption>그림 1. 그림이 무엇을 보여주는지 객관적으로. (출처: …)</figcaption>
</figure>
```
- 캡션에 번호를 매긴다 (`그림 1.`, `그림 2.` …); 외부 출처 이미지는 캡션 끝에 출처 표기.
- 애니메이션이 필요 없는 모든 그림은 figure-canvas가 아니라 이것을 쓴다.

### 4.9 캔버스 도해 (figure-canvas)
JS로 그리는 시각화:
```html
<figure class="figure-canvas">
  <canvas id="my-canvas" role="img" aria-label="..."></canvas>
  <figcaption>설명</figcaption>
</figure>
```
스크립트 필수 패턴 세 가지 (템플릿의 데모 스크립트가 모두 구현하고 있다 — 유지할 것):
1. **lazy-start** — `IntersectionObserver`로 스크롤 도달 시 시작
2. **고DPI 보정** — `devicePixelRatio`만큼 백버퍼를 키우고 `setTransform`으로 좌표계 복원
3. **절전·모션 배려** — 화면 밖으로 나가면 `cancelAnimationFrame`으로 정지,
   `prefers-reduced-motion: reduce`면 애니메이션 대신 정지 프레임 1장

### 4.10 슬라이더 explorer (explorer-box)
사용자 매개변수 조작:
```html
<div class="explorer-box">
  <canvas id="my-explorer" role="img"></canvas>
  <div class="slider-group">
    <div class="slider-row">
      <label for="x-slider">라벨</label>
      <input type="range" id="x-slider" min="0" max="10" value="5">
      <span class="slider-val" id="x-val">5.0</span>
    </div>
    <button id="reset-btn" class="reset-btn">초기화</button>
  </div>
</div>
```

인터랙티브 요소는 조용한 학술 톤에 맞게 **절제해서** 쓴다. 이해를 돕지 못하면 넣지 않는다.

---

## 5. References
APA 7판 hanging-indent. URL은 DOI 우선:
```html
<section class="article-refs">
  <h2>References</h2>
  <ul class="references">
    <li>저자 (연도). 제목. <em>저널명, 권</em>(호), 면.
        <a href="https://doi.org/...">https://doi.org/...</a></li>
  </ul>
</section>
```

---

## 6. Colophon (선택)
글의 출처/제작 노트가 있으면:
```html
<p class="colophon">본 고는 ...에 기초한 해설이다.</p>
```

---

## 7. 마무리 nav (선택)
독립 폴더에는 브리프 목록이 없으므로 기본 생략. 실사이트로 옮길 때 복원한다:
```html
<nav class="article-end-nav">
  <a href="../briefs.html">← 브리프 목록</a>
</nav>
```

---

## 8. 컬러·타이포 토큰
| 토큰 | 값 | 용도 |
| --- | --- | --- |
| `--bg` | `#f6f0e3` | 페이지 배경 (cream) |
| `--ink` | `#0f1624` | 본문 텍스트 (navy) |
| `--blue` | `#009fde` | KEI 블루 (강조·링크) |
| `--green` | `#00ab84` | KEI 그린 |
| `--amber` | `#ff8a2a` | KEI 앰버 |
| `--warn` | `#c46411` | 경고 callout 좌측선 |
| `--muted-strong` | `rgba(15,22,36,.82)` | 본문 회색 톤 |
| `--muted` | `rgba(15,22,36,.62)` | 캡션·메타 |
| `--line` | `rgba(15,22,36,.12)` | 섹션 구분선 |
| `--line-soft` | `rgba(15,22,36,.06)` | 표 내부 행 구분 |
| `--serif` | (Paperlogy sans stack — 이름만 serif, 값은 고딕) | 표·수식·변수기호 컨테이너 (본문과 같은 sans) |

폰트 크기:
- h1: `clamp(28px, 3.6vw, 40px)` / line-height 1.22
- h2: `clamp(22px, 2.2vw, 28px)` / line-height 1.30
- h3: 19px
- 본문: 17px / line-height 1.85
- abstract: 18px / line-height 1.80
- caption / meta: 14–14.5px

이 토큰과 크기는 캐노니컬 템플릿의 인라인 `<style>`에 이미 구현되어 있다. 값을 바꾸지 말고 그대로 쓴다.
