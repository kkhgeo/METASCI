# Tool Translation

How to translate the universal prompt schema into each target tool's native syntax. Each tool has distinct strengths and quirks — translate accordingly, don't produce identical text across all four.

---

## Midjourney (v6+)

**Native style**: Compressed phrases separated by commas, parameters appended at end. Adjectives earn their place; no filler.

### Translation pattern

```
[SUBJECT phrase], [COMPOSITION + LIGHTING phrase], [COLOR palette phrase], 
[STYLE references phrase], [MOOD descriptor] --ar [ratio] --style raw --stylize [50-500]
```

### Parameter guide

| Parameter | Effect | Default for this skill |
|---|---|---|
| `--ar W:H` | Aspect ratio | Always specify |
| `--style raw` | Less MJ "house style" aesthetic processing | Use by default |
| `--stylize N` | Artistic interpretation (0–1000) | 100–250 for precise briefs; 500+ for loose interpretation |
| `--chaos N` | Variation across grid (0–100) | Skip unless user wants exploration |
| `--weird N` | Unusual results (0–3000) | Skip by default |
| `--no [items]` | Negative prompt | **Always use** for AVOID list |

### Example translation

Schema:
- SUBJECT: topographic map dissolving into watercolor
- STYLE: Turner late-period seascape meets scientific illustration
- LIGHTING: blue hour predawn, low contrast
- COLOR: pale teal, warm grey, faded ochre
- AVOID: purple gradients, 3D render, globe icons

Midjourney output:
```
aerial view of a topographic map dissolving into watercolor, contour lines 
bleeding like wet ink, pale teal and warm grey palette with small ochre 
accents, blue hour predawn light, Turner late-period seascape atmosphere 
meets 19th-century scientific illustration, negative space upper left 
--ar 16:9 --style raw --stylize 250 --no purple gradient, 3D render, 
globe icons, text, watermark
```

### Midjourney-specific gotchas

- Do **not** repeat the subject across multiple phrases — it confuses the model
- Avoid "masterpiece, best quality, 8k" — degrades v6+ output
- Put the strongest visual reference earliest — MJ weights by position
- Named artist references work; full painting titles sometimes work better than the artist name alone

---

## DALL-E 3 / ChatGPT Image

**Native style**: Flowing natural-language paragraph. DALL-E expands short prompts, so giving it a complete paragraph matches its internal process.

### Translation pattern

A single paragraph of 3–6 sentences, in this order:
1. Scene description (SUBJECT + COMPOSITION)
2. Lighting and atmosphere
3. Color and mood
4. Style and medium references
5. Technical constraints (aspect ratio in natural language)
6. Single "Avoid" sentence for negatives

### Example translation

```
An aerial perspective of a topographic landscape where contour lines are 
dissolving into watercolor washes, as if solid geography is turning liquid. 
The left side retains crisp cartographic detail while the right side bleeds 
into soft pigment; the upper-left third is intentionally empty for title 
text. Lit by the cool, low-contrast light of the minute before dawn, the 
palette is restricted to pale teal, warm grey, and small accents of faded 
ochre, creating a mood of quiet mourning with traces of awe. The style sits 
between a Turner late-period seascape and a 19th-century scientific 
illustration plate. Horizontal 16:9 composition. Avoid purple-to-blue 
gradients, any 3D rendering, and literal symbols like globes or factories.
```

### DALL-E-specific gotchas

- DALL-E ignores most parameters; describe aspect ratio in words
- Strong with typography when explicit ("the words '...' in a specific font")
- Struggles with precise compositional control — lean on clear spatial language

---

## Flux (Pro / Dev / Schnell)

**Native style**: Extremely specific scene description with technical photographic and artistic terms. Flux rewards verbosity and precision.

### Translation pattern

Extended natural-language description (5–10 sentences), including:
- Technical photography terms (focal length, aperture, film stock)
- Specific compositional language (rule of thirds, leading lines, specific angle)
- Material and texture specificity
- Atmospheric detail

### Example translation

```
A large-format aerial photograph of a topographic landscape in the moments 
before dawn, shot on 8x10 film with a 150mm lens at f/11, the composition 
oriented horizontally with intentional empty sky filling the upper-left 
third. The landscape itself transitions from crisp cartographic contour 
detail on the left to dissolved watercolor washes on the right, as if the 
terrain is turning to liquid pigment. The light is cool and directionless, 
diffused overcast with the barest hint of dawn coming from the right edge. 
The palette is restricted to pale teal in the mid-tones, warm grey in the 
shadows, and small muted ochre accents in the terrain. The mood evokes 
quiet mourning alongside traces of awe. The overall aesthetic references 
J.M.W. Turner's late seascapes — where forms dissolve into atmosphere — 
crossed with 19th-century scientific plate illustrations showing 
topographic strata. Visible paper grain and watercolor bleed where the 
contour lines dissolve. Photorealistic but not hyperreal; restrained, 
editorial, suitable for a museum catalog cover.
```

### Flux-specific gotchas

- Flux handles long prompts well (unlike older SD models)
- Include both photographic and painterly reference when ambiguity is desired
- Aspect ratio set via tool UI, not prompt

---

## Nano Banana / Gemini 3 Pro Image

**Native style**: Structured natural language. The model reasons through the prompt before generating, so logical structure and factual accuracy help. Particularly strong at text rendering, real-world knowledge, and infographic layout.

### Translation pattern

Follows the official recommended structure:

```
[SUBJECT with adjectives] doing [ACTION] in [LOCATION/CONTEXT].
[COMPOSITION / CAMERA ANGLE].
[LIGHTING / ATMOSPHERE].
[STYLE / MEDIA].
[SPECIFIC CONSTRAINTS / TEXT if applicable].
```

### Key capabilities to leverage

1. **Text rendering** — spell out exact text, specify font characteristics ("bold serif, all caps, warm grey color"). Critical for posters and infographics.
2. **Real-world knowledge** — can draw on factual information (specific locations, scientific accuracy, historical style periods).
3. **Reference image input** — supports up to 14 reference images. When the user provides a reference, the prompt should instruct what to preserve and what to change.
4. **Aspect ratio** — specify in natural language; supports 16:9, 9:16, 1:1, 4:5, 3:2, 2:3, 3:4, 4:3, 5:4, 21:9, and extremes like 1:4/4:1.

### Example translation (standard image)

```
An aerial view of a topographic landscape transitioning from crisp 
cartographic contour lines on the left to dissolved watercolor washes on 
the right, as if solid geography is turning to liquid pigment.

Horizontal composition with intentional negative space in the upper-left 
third for overlaid title text. The visual flow moves diagonally from 
lower-left to upper-right.

Lit by the cool, low-contrast, diffused light of blue hour before dawn; 
no harsh shadows.

The palette is restricted to pale teal, warm grey, and small accents of 
faded ochre. The mood is one of quiet mourning with traces of awe.

Style combines J.M.W. Turner's late-period atmospheric seascapes with the 
precision of a 19th-century scientific topographic plate. Visible paper 
grain where the watercolor bleeds. Restrained and editorial, suitable for 
a museum catalog or scientific journal cover.

16:9 aspect ratio. Avoid purple-to-blue gradient skies, any 3D rendering, 
literal symbols like globes or factories, HDR oversaturation.
```

### Example translation (poster / infographic with text)

```
A single-column academic poster layout, 24 × 36 inches, portrait 
orientation (2:3).

Top third: the title "The Dissolving Boundary" rendered in a large bold 
serif font (approximately 120pt), warm grey color (#4A4743), aligned 
left. Below the title, a subtitle in the same serif at 48pt, regular 
weight, reading "Climate Signals in Topographic Change."

Middle third: a central illustration of a topographic contour-line 
landscape dissolving from crisp on the left to watercolor-bleed on the 
right. Palette is pale teal (#8AB5B3), warm grey (#AEA79E), faded ochre 
(#B8956A). Style references 19th-century scientific plate illustrations.

Bottom third: three equally spaced data callouts in monospace font (14pt, 
warm grey), each with a specific numerical value and a two-line caption. 
Use real, plausible-looking scientific notation.

Background: unbleached paper texture, no gradient. Overall mood: 
restrained, editorial, museum-catalog aesthetic.

Avoid: gradient backgrounds, 3D elements, stock infographic iconography, 
multi-colored chart spam.
```

### Nano Banana-specific gotchas

- **Do not** use "masterpiece, 4K, trending on artstation" spam — degrades modern Gemini output
- **Do** use camera / lighting / design terminology ("85mm f/2.8," "three-point lighting," "Swiss typography")
- **Do** specify exact text content in quotes when text is needed — it will render accurately
- **Do** enable "Thinking" mode via the model dropdown for complex multi-element compositions
- Iterate conversationally ("change the sky to dawn, keep everything else") rather than regenerating from scratch
- For multi-image composition, reference images are numbered in the order uploaded; refer to them explicitly ("using reference image 2's texture")

---

## When to use which tool

| Use case | Best tool | Why |
|---|---|---|
| Editorial illustration, mood-heavy hero | Midjourney | Strongest aesthetic defaults |
| Accurate text, infographics, posters | **Nano Banana** | Only tool with reliable text rendering and real-world grounding |
| Conversational iteration, quick concepts | DALL-E / ChatGPT | Natural dialogue, fast |
| Photorealistic specificity, commercial quality | Flux | Most precise control over technical details |
| Consistent character / brand across many images | Nano Banana | 14-image reference input |
| Fine-art abstract composition | Midjourney | Artist references work most reliably |

**Default recommendation for academic/research contexts**: Lead with Nano Banana when the image includes any text (titles, labels, captions, data). Lead with Midjourney for abstract mood imagery. Use all four when comparing outputs for a hero image.
