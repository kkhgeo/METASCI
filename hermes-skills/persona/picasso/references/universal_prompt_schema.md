# Universal Prompt Schema

A tool-agnostic structure that captures sufficient intent for any modern image model. All fields must be filled before tool-specific translation.

## The schema

```
SUBJECT     : [core scene, precise]
COMPOSITION : [framing, negative-space location, visual flow]
LIGHTING    : [direction, time, quality]
COLOR       : [palette, temperature, contrast]
STYLE       : [medium, movement, artist reference]
MOOD        : [emotional tone]
TECHNICAL   : [aspect ratio, resolution]
AVOID       : [explicit anti-slop exclusions]
```

## Field-by-field rules

### SUBJECT

State the core scene with **specific nouns and verbs**, not adjectives.

- ✅ "A topographic map dissolving into watercolor, contour lines bleeding at the edges"
- ❌ "A beautiful abstract image about change"

Include spatial relationships ("left half remains crisp, right half dissolves"). Avoid vague abstractions ("representing transformation").

### COMPOSITION

Three sub-elements are required:

1. **Framing** — aerial / eye-level / low-angle / dutch tilt / extreme close-up / wide establishing
2. **Negative-space location** — explicitly where empty space sits, because this is where title/body text will land
3. **Visual flow** — where the eye enters and where it travels (e.g., "enters bottom-left, travels diagonally to upper-right")

Default negative space locations by use case:
- Slide visual: right third (or wherever body text goes)
- Hero image: left third or top third (title placement)
- Poster: one quadrant or a central band

### LIGHTING

Specify three properties:

- **Direction**: front / back / side (which side) / top / underlit / ambient
- **Time/source**: blue hour / golden hour / overcast noon / tungsten interior / moonlight / sodium vapor / studio softbox
- **Quality**: hard / soft / diffused / directional / volumetric

Avoid "dramatic" or "cinematic" as standalone terms — they mean nothing to modern models.

### COLOR

Name **2–4 specific hues** with relationships, not categories.

- ✅ "Pale teal (~#8AB5B3), warm grey (~#AEA79E), small accents of faded ochre"
- ❌ "Earth tones" / "cool palette"

Specify:
- **Temperature** — warm / cool / mixed
- **Contrast** — low-contrast / high-contrast / specific (e.g., "mid-grey values dominate with one saturated accent")
- **Saturation** — desaturated / muted / vivid

### STYLE

Must include at least two of:

- **Medium** — watercolor / oil / etching / risograph / photograph / blueprint / collage / 3D render
- **Movement / tradition** — Nordic Romanticism / Mono-ha / New Topographics / Bauhaus / Japanese postwar photography / Dutch still life / medical illustration / Victorian scientific plate
- **Artist / director reference** — Hammershøi / Andrew Wyeth / Saul Leiter / Hiroshi Sugimoto / Tarkovsky / Wes Anderson / Gregory Crewdson

**At least one reference must come from outside the design/web/tech world.** This is the anti-slop mechanism at the schema level.

### MOOD

A **precise emotional register**, not a generic positive.

- ✅ "Quiet mourning with traces of awe"
- ✅ "Tense anticipation before arrival"
- ❌ "Professional and modern"
- ❌ "Inspiring"

Two adjectives maximum; make them unusual together.

### TECHNICAL

- **Aspect ratio** — 16:9 / 9:16 / 1:1 / 4:5 / 3:2 / 2:1 / 21:9
- **Resolution intent** — screen / print / poster (affects detail density)
- **Output format** — if relevant (photograph / illustration / mixed media)

### AVOID

At minimum, inject:

1. Three items from the always-ban list in `anti_slop_checklist.md`
2. Domain-specific bans if the concept touches climate, AI, healthcare, education, or data
3. Anti-pattern to the chosen style (e.g., if STYLE says "Wyeth-like," AVOID should include "over-saturation, digital sharpness")

## Schema validation checklist

Before proceeding to tool translation:

- [ ] SUBJECT uses concrete nouns and verbs
- [ ] COMPOSITION explicitly states where negative space lives
- [ ] LIGHTING has all three properties filled
- [ ] COLOR names specific hues, not categories
- [ ] STYLE references at least one non-design source
- [ ] MOOD is a precise register, not a generic positive
- [ ] TECHNICAL specifies aspect ratio
- [ ] AVOID has at least 3 items beyond "no text" or "no watermark"
