---
name: meta-figure-audit
description: >
  Post-hoc quantitative correction of a publication figure drawn under
  FIGURES.md / figure_spec.yaml / figspec.py (installed by init-figure-rules).
  Renders, audits the exported PDF (canvas mm, every font size and
  stroke width in pt, text kept as editable text not outlines, font family,
  panel groups), detects overlapping text in mm, presents the full parameter
  sheet, then applies the author's numeric requests — tick length, font sizes,
  line widths, panel boxes, legend position, inline annotation position — by
  editing the spec only and re-rendering until the audit is clean. Use when
  the user says "그림 교정", "피겨 감사", "수치 교정", "그림 수치 맞춰줘",
  "범례 옮겨줘", "글자 겹쳐", "눈금 길이 바꿔", "figure audit", "check the
  figure", or asks to adjust any number on a figure in this workspace. Not
  for drawing a new figure (follow FIGURES.md) or for deciding what each
  panel should show.
---

# Meta Figure Audit

Quantitative correction loop. The plotting script is never edited here;
every change goes through `figure_spec.yaml` and the script is re-run.

Units: thickness and text in pt, lengths in mm. Never quote inches or px.

## Preconditions

`FIGURES.md`, `figure_spec.yaml`, `figspec.py` exist in the project root
and the figure script imports `figspec`. If not, stop and point to
`init-figure-rules` (for the files) or FIGURES.md "Existing code" (for
converting a script). Read FIGURES.md before starting.

## Loop

1. **Render.** `python <script>.py`. It prints `충돌 없음` or a list of
   overlapping text pairs with the overlap in mm. Keep that output.
2. **Audit.** `python figspec.py audit figure_spec.yaml <name>.pdf`.
   Report the result verbatim. Lines:
   - 캔버스 mm vs spec
   - 텍스트 객체 유지 — text must never be outlines
   - 글꼴 — the spec family plus the families listed in
     `text.font_fallback` (Arial + DejaVu Sans by default; Arial has no ⁺ ⁻
     and no subscript digits, so ion labels borrow those glyphs). Two
     families on this line is expected. A LastResort family is a hard fail:
     those characters print as placeholder boxes. If Arial itself is missing
     on the machine, say so; do not change the spec
   - 글자 크기 실측 set vs spec set (any extra value is a hard-coded number
     or a mathtext sub/superscript; find it in the script, move it to the
     spec or replace with Unicode); 5 pt floor
   - 선 두께 실측 set vs spec set
3. **Sheet — always before any change.** `python figspec.py sheet
   figure_spec.yaml` and show it in full. This is the author's view of the
   current values: canvas, every panel box, per-panel legend position, every
   inline annotation (text, x/y mm, pt, alignment), every arrow, then the
   global text/line/tick/marker/legend/colour/export values. Never modify a
   value the author has not seen on this sheet first.
4. **Ask once, in one message:** which rows to change. Offer your own
   recommendation for anything the audit or collision check flagged (e.g.
   "note b-0 overlaps the legend by 15 × 2.5 mm; I'd move it to x 24,
   y 26 mm or shift the legend dy −6 mm — I prefer moving the note because
   the legend anchors to the corner").
5. **Apply** each request by editing `figure_spec.yaml`:
   - global number → the matching key under text/lines/ticks/markers/legend
   - one panel only → `panels[].overrides: {key: value}` with the same key name
   - legend → `panels[].legend: {loc, dx_mm, dy_mm, ncol, title}`
   - inline text → `panels[].annotations[i]` (`x_mm`, `y_mm` from the
     panel's bottom-left; `pt`, `ha`, `va`, `color`, `rotation`)
   - arrow → `panels[].arrows[i]` (`from_mm`, `to_mm`)
   - panel box → `panels[].x_mm/y_mm/w_mm/h_mm`; re-check the margin
     minimums in FIGURES.md rule 10
   Show each change as `key: was → now`, then go to step 1.
6. **Finish** when the audit has no `XX`, the collision list is empty, and
   the author approves the rendered PDF at final physical size. Record the
   date and figure name in a one-line comment at the top of the spec.

## Rules

- Never patch a number into the plotting script. If a quantity is not yet
  in the spec, add the key, then use `S.` in the script once and say so.
- Never convert text to outlines, expand fonts, or rasterise to "fix"
  a font issue. The file leaves Python with live text or it is not finished.
- A script that places text or legends with literal coordinates cannot be
  corrected here; move them to `annotations` / `legend` in the spec first
  (values seeded from the current positions, converted to mm).
- Collision check covers text boxes only (labels, ticks, legend, notes,
  panel labels). Text over data points, arrows over markers, and legend
  over data are judged by eye on the final-size PDF; say that explicitly.
- Report every change as "what was / what is / why", in manuscript order
  (panel a → d), not by severity.
