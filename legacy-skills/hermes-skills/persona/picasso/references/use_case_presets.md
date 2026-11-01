# Use Case Presets

Constraint profiles for the three primary use cases this skill handles. Load the relevant profile during Phase 0; these constraints inject into the universal prompt schema automatically.

---

## Slide visual (research presentation)

**Purpose**: Support spoken content during a talk. The image is subordinate to the argument; it must not distract from the speaker or compete with overlay text.

### Default constraints

| Field | Default / bias |
|---|---|
| COMPOSITION | Wide negative space along one axis (typically right half or right third); avoid central subject when text will overlay |
| LIGHTING | Soft, low-contrast; avoid specular highlights that fight projection |
| COLOR | Desaturated; one or two dominant hues; avoid saturated reds/yellows that over-project |
| MOOD | Supportive, not assertive — the image should feel like a background for argument, not the argument itself |
| TECHNICAL | 16:9 by default (standard widescreen) or 16:10; 4:3 only if user's template demands it |

### Anti-patterns specific to slides
- Photographs with busy texture behind body text (unreadable)
- High-contrast imagery behind dark text (use a soft overlay or pick a darker image)
- Literal illustrations of what the speaker is saying (redundant; patronizing)
- Stock "business-people-looking-at-chart" photography

### Preferred approaches
- **Abstracted natural phenomena** — stratified rock, cloud formation, water surface
- **Editorial magazine illustration** — conceptual, mid-century-influenced
- **Diagrammatic clarity** — a single clear visual idea, not a collage
- **Photographic fragment** — close-up of a material, cropped tightly

### Phase 3 vocabulary bias for slides
Lean toward **Register 1 (quiet)** or **Register 5 (clinical)** — these serve argument without competing with it. Avoid Registers 2, 3, 6 unless the content genuinely demands them.

---

## Hero image (website, landing page, publication cover)

**Purpose**: Emotional entry point. Creates the first impression before any text is read. Must carry narrative weight on its own while leaving room for typography.

### Default constraints

| Field | Default / bias |
|---|---|
| COMPOSITION | Strong focal point with deliberate negative space for H1/subtitle; asymmetric preferred; clear visual hierarchy |
| LIGHTING | Can be dramatic — hero space tolerates (and benefits from) stronger mood |
| COLOR | Deliberate palette of 3–4 hues with explicit relationships; one accent color for CTA alignment |
| MOOD | Must be unusual enough to be memorable; avoid "professional and modern" as a target |
| TECHNICAL | 16:9 landscape for desktop hero; 4:5 or 1:1 if responsive / mobile-first; specify negative-space location in words |

### Anti-patterns specific to heroes
- Product screenshot on a gradient
- Laptop/phone mockup showing the UI
- Smiling person or "diverse team" stock photo
- Abstract geometric shapes with no referent
- Floating 3D isometric objects (extreme slop)

### Preferred approaches
- **Conceptual illustration** — original art that encodes the product's thesis in a visual metaphor
- **Editorial photography** — cinematic single-subject photography, Gregory Crewdson-adjacent
- **Abstracted natural phenomena** — at scale, evoking the product's emotional register
- **Typographic composition** — a bold word-mark treatment where the image IS the typography
- **Architectural fragment** — specific materials, specific light, implied scale

### The "concept art" move (Level 5 from the reference video)
When the user wants to escape typical SaaS/product aesthetics, deliberately pull from:
- Graphic novel / concept art aesthetics
- Film poster design (pre-2000, before Photoshop bloat)
- Album cover art
- Scientific illustration plates
- Historical cartography

This is the single most reliable move for differentiated hero imagery.

### Phase 3 vocabulary bias for heroes
Any register works, but the choice must be **intentional and distinctive**. If the product category (SaaS, B2B, fintech) has default expectations, deliberately pull from a different register to create contrast.

---

## Academic poster / infographic

**Purpose**: Communicate structured information to an audience that reads at varying distances. Must work at 3 meters (attracting) and 30 cm (informing). Often includes precise text and data.

### Default constraints

| Field | Default / bias |
|---|---|
| COMPOSITION | Clear hierarchy — title zone, anchor visual zone, data/body zone; grid-aware; typically portrait orientation |
| LIGHTING | Flat, even; printed media tolerates neither harsh shadows nor HDR |
| COLOR | Restricted palette (3–5 hues max); high print-contrast for readability; colors must survive CMYK conversion |
| STYLE | Leans toward editorial / scientific illustration traditions; avoid photographic clutter |
| TECHNICAL | Common sizes: A0 (841 × 1189 mm), A1, 24×36 inches, 36×48 inches; always specify portrait/landscape; specify DPI intent (300 for print) |

### Anti-patterns specific to posters/infographics
- Generic "data flow" arrows between vague boxes
- Stock scientific iconography (DNA helix for anything biology, gears for anything technical)
- Chart junk — 3D charts, gradient fills on bars, meaningless visual flourishes
- Multiple fonts without clear hierarchy
- Multicolor rainbow palettes without meaning

### Preferred approaches
- **Tufte-influenced information design** — maximum data-ink ratio, small multiples, clear typography
- **Historical scientific illustration** — Haeckel's Kunstformen, Vesalius, Audubon — integrity + beauty
- **Cartographic thinking** — layered legible data, clear grammar of symbols
- **Swiss graphic design tradition** — grid, sans-serif, restraint
- **Editorial magazine layout** — NYT / New Yorker infographic conventions

### When the poster contains text, labels, or data
**Use Nano Banana / Gemini Image as primary tool.** It is currently the only mainstream model with reliable multilingual text rendering. Specify exact text in quotes, font characteristics in natural language.

### Phase 3 vocabulary bias for posters
**Register 5 (stark, precise, clinical)** is the default. Register 1 (quiet) and Register 7 (textured decay) work for humanities/historical posters. Avoid Registers 2, 3, 6 unless the content genuinely demands them.

---

## Cross-use-case principles

### Always specify negative space
Regardless of use case, explicitly state where empty visual space sits in the composition. This is the single most important compositional instruction — without it, models center the subject and leave no room for text.

### Always specify one concrete reference
A single specific reference (artist, film, movement) produces better output than three vague adjectives. "Like Saul Leiter's NYC street photography" beats "moody, atmospheric, cinematic."

### Match the output format's inherent logic
- Slides are temporal (seen briefly, in context of speech)
- Hero images are spatial (seen at one moment, must hold on their own)
- Posters are both (attract at distance, inform at close range)

Prompts should reflect this — a slide visual can be more abstract than a poster; a poster can be denser than a hero.
