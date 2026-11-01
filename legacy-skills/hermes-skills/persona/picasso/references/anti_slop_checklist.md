# Anti-Slop Checklist

Patterns that signal generic "AI slop" aesthetics. Always include the relevant items in the prompt's `AVOID` field. When a banned pattern is tempting, use the listed replacement instead.

## Always-ban list (inject into every AVOID field)

- **Purple-to-blue gradients** — especially as background fills
- **3D isometric illustration** (unless the user explicitly requests it)
- **Holographic / neon / "cyber" aesthetic spam**
- **Stock-photo artificial smiles and handshakes**
- **Globe / circuit board / AI brain / binary code clichés**
- **Floating disembodied hands holding glowing objects**
- **HDR over-saturation**
- **Generic "tech blue" (#4285F4-adjacent)**
- **"Trending on ArtStation" / "masterpiece" / "4K 8K" padding phrases** (these degrade modern models)
- **Lens flare abuse**
- **Shutterstock-style confetti of abstract icons**

## Use-case-specific bans

### Slide visuals
- Avoid: Background images that compete with text, high-contrast photography behind body text, complex textures under small fonts
- Instead: Low-contrast abstraction, single-subject photography with large negative space, or diagrammatic clarity

### Hero images
- Avoid: Product screenshot on a gradient, mockup of a laptop/phone showing the UI, smiling team photo, generic "diverse people at a table" stock
- Instead: Conceptual illustration, editorial photography, abstracted natural phenomena, architectural fragment, typographic composition

### Academic posters / infographics
- Avoid: Cartoon scientists with goggles, DNA helixes used decoratively, generic "data flow" arrows between vague boxes, blue rectangles of varying sizes
- Instead: Data physicalization, scientific diagram conventions, editorial magazine layout logic, cartographic thinking

## Domain-specific slop (extend AVOID when relevant)

### Climate / environment
- Avoid: Polar bear on shrinking ice, smokestacks, blue Earth with red zones, melting clock, hands holding a plant
- Instead: Geological cross-sections, weather data visualization, historical landscape painting updated, specific local phenomena

### AI / technology
- Avoid: Blue humanoid robot, glowing brain, neural network as literal neurons, person staring at code
- Instead: Historical parallels (printing press, telegraph), material metaphors (weaving, crystallization), observational scenes

### Healthcare / biology
- Avoid: Stethoscope on laptop, doctor in white coat pointing at hologram, generic cell clusters
- Instead: Medical illustration tradition (Netter, Vesalius), microscopy aesthetics, clinical photography conventions

### Education
- Avoid: Stack of books with apple on top, lightbulb above head, chalkboard equations
- Instead: Historical pedagogical illustrations, studio craft photography, library archival aesthetics

### Data / analytics
- Avoid: Floating bar charts in 3D, magnifying glass on graph, person pointing at screen full of numbers
- Instead: Information design traditions (Tufte, Bertin), historical statistical atlases, data physicalization

## Replacement strategies (when a cliché is tempting)

| Cliché | Replacement principle |
|---|---|
| "Futuristic / high-tech" | Specify a decade, material, or historical parallel |
| "Modern / clean" | Name the actual design movement (Swiss, Bauhaus, Japanese postwar) |
| "Minimalist" | Specify what is removed and what remains |
| "Vibrant colors" | Name 2–3 specific hues with relationships |
| "Professional" | Describe the publication context (journal cover, museum catalog, NYT op-ed) |

## Final check before output

Before finalizing any prompt, verify:

1. No banned pattern is present in SUBJECT or STYLE fields
2. At least three specific anti-slop items are listed in AVOID
3. No filler adjectives ("amazing," "stunning," "beautiful")
4. At least one non-design reference (cinema, painting, craft, science) appears in STYLE
5. COLOR names specific hues, not categories ("muted teal and warm ochre," not "earthy tones")
