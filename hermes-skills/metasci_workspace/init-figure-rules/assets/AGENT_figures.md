# AGENT_figures.md — Figure rules for this workspace

Defaults in `figure_spec.yaml`: Arial throughout; Nature hierarchy shifted up
one step (8 pt axis titles, 7 pt tick labels, 9 pt bold panel labels, 0.5 pt
lines, 4.3 pt markers); Nature-style palette (impacted #E64B35, background
#3C5488, accents teal/cyan/salmon/grey-blue); the author's conventions kept —
closed box, outward 1.2 mm ticks, site encoded by marker shape (A ▲, B ●,
C ■), shared x-axis rows in panel grids.

Read this file before any figure work: drafting, revising, auditing, or
exporting. These rules exist so that a figure leaves Python ready for
Illustrator with nothing left to resize. Numbers live in `figure_spec.yaml`;
application logic lives in `figspec.py`. This file holds only the conventions.

Units everywhere: thickness and text in **pt**, every length in **mm**. Never
write inches or pixels in user-facing code or conversation.

## Drafting rules

1. **Spec first.** Every figure script begins with `S = Spec.load("figure_spec.yaml")`
   and obtains every visual quantity from `S`. The plotting code contains no
   literal `fontsize=`, `linewidth=`, `lw=`, `markersize=`, `figsize=`,
   `capsize=`, or hex colour. If a quantity is not in the spec yet, add it to
   the spec, then use it.
2. **Canvas and panels come from the spec.** Create the figure with
   `S.canvas()` and each axes with `S.panel(fig, "a")`. Never call
   `plt.subplots`, `tight_layout`, `constrained_layout`, `subplots_adjust`,
   or save with `bbox_inches="tight"`. The artboard is fixed; content fits
   the artboard, not the reverse.
3. **Wireframe before data.** For a new figure, run
   `python figspec.py wire figure_spec.yaml wireframe` and get the author's
   approval of panel count, placement, and size before any data is plotted.
   Layout is the most expensive thing to change later.
4. **Data above, drawing below.** Data loading and reduction happen at the
   top of the script (or in a separate file). Each panel is one function
   `draw_<id>(ax, <arrays>, S)` that receives prepared arrays and the spec.
   Panel functions do not read files, and do not touch global `plt` state.
5. **Text strings in one place.** Axis labels, units, legend entries, and
   annotations live in a dict `T = {...}` at the top of each panel function.
6. **Colours by role, not by value.** Use `S.color("impacted")`,
   `"background"`, `"neutral"`, `"accent1"`–`"accent4"` — the roles defined
   under `colors.roles` in the spec. Add a role to the spec rather than
   writing a hex.
7. **Close every panel with `S.style(ax, "<id>")`.** This applies tick
   length, pad, spine width, label sizes, and any per-panel overrides.
8. **Save with `S.save(fig, "<name>")`.** It exports a single PDF with the
   artboard fixed at the spec canvas, Arial embedded as live text (Type 42),
   and one clipping group per panel for Illustrator. PDF is the only
   deliverable; SVG is not produced.
9. **No mathtext super/subscripts in labels.** `$^{13}$` renders at 70 % of
   the base size and breaks the 5 pt floor. Use Unicode (δ¹³C, Mg²⁺) or
   write the label in prose. Arial carries superscript digits ⁰–⁹ but **not**
   ⁺, ⁻, or any subscript digit ₀–₉, so ion labels (NH₄⁺, SO₄²⁻) borrow those
   four glyph shapes from `text.font_fallback` (DejaVu Sans by default). The
   audit lists both families and passes; what must never appear is a
   LastResort family, which prints placeholder boxes.
10. **Shared axes are declared, not hand-coded.** For panel grids, set
    `layout.shared_x_rows` / `shared_y_cols` in the spec; `S.style` then
    hides inner tick labels and axis titles. Leave at least 13 mm below the
    bottom row and 14 mm left of each column for 7 pt ticks + 8 pt
    titles. Panel labels sit 1.5 mm above the box, so row gaps need ≥ 7 mm.
11. **Use all the data.** Do not thin, subsample, or drop points to make a
    panel render faster or look cleaner. If an exclusion is scientifically
    justified, state the rule and the before/after count in the reply.

## Audit rules (after every render)

- Run `python figspec.py audit figure_spec.yaml <name>.pdf` and report the
  result verbatim. A figure is not finished while any line reads `XX`.
- Present `python figspec.py sheet figure_spec.yaml` when the author asks to
  review or adjust numbers. Edits go into `figure_spec.yaml`, then the same
  script is re-run. Do not patch numbers into the plotting code.
- Per-panel exceptions go under that panel's `overrides:` in the spec, using
  the same key names as the global sections.
- After the audit passes, inspect the PDF at final physical size for label
  collisions and legend placement. The audit proves numbers, not layout.

## When a figure is approved

Keep `figure_spec.yaml` next to the figure script. A later figure in the
same manuscript starts from this spec, so numbers stay consistent across
Fig. 1–N without re-discussion.

## Existing code brought into this workspace

Convert it to these rules before extending it: replace literal numbers and
hex colours with `S.` calls (seeding the spec with the code's current
values so the author's existing choices become the defaults), remove layout
calls, and move axes to `S.panel`. Re-render and show the before/after PDFs.
Do not split the code into panel functions unless the author asks; report
that as a recommendation instead.
