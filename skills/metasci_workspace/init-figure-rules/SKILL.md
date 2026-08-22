---
name: init-figure-rules
description: >
  Install workspace-level figure rules for publication figures that go from
  Python (matplotlib) to Illustrator with minimal post-editing: drops
  FIGURES.md (drafting and audit conventions), figure_spec.yaml (every
  number in pt/mm, Nature defaults), and figspec.py (library that applies
  the spec, prints a parameter sheet, renders wireframes, and audits
  exported SVG) into a manuscript folder, and adds one pointer line to
  AGENTS.md/CLAUDE.md. Use when the user says "그림 규칙 설치", "그림 규칙
  세팅", "figure rules", "이 폴더 논문 그림 세팅", "피겨 스펙 초기화", "init
  figure rules", wants figures to follow a spec, or complains about
  adjusting font sizes, line widths, or tick lengths in Illustrator.
  Sibling of init-writing-workspace and init-communication-rules. Also use
  to refresh the three files to the current canonical version.
---

# Init Figure Rules

Installs the figure-rule layer of a manuscript workspace. Always-on rules
live in AGENTS.md; figure rules are conditional, so they live in their own
file and are reached through a single pointer line.

Canonical content lives in `assets/`. **Never rewrite it from memory** —
copy the files so every project carries the same reviewed version.

```
assets/
├── FIGURES.md         drafting and audit conventions (read before figure work)
├── figure_spec.yaml   every number: canvas, panels, text, lines, ticks, markers, legend, colours, export
└── figspec.py         Spec.load / canvas / panel / style / save / sheet / audit / wireframe
```

## Procedure

1. Identify the target project root. If unclear, ask — do not guess.
2. For each of the three files, check whether it already exists there.
   - Missing: copy from `assets/`.
   - `FIGURES.md` or `figspec.py` present: show a diff against the asset,
     recommend overwrite or keep with a reason, and wait.
   - `figure_spec.yaml` present: **never overwrite.** It holds the author's
     tuned numbers. Show which keys the canonical template has that the
     existing file lacks, and offer to append only those with default
     values.
3. Make sure the always-on instruction file points at `FIGURES.md`. Check
   `AGENTS.md`, then `CLAUDE.md`. **If either already mentions `FIGURES.md`,
   change nothing** — a workspace built by `init-writing-workspace` carries
   that line in its canonical text. Otherwise append to the first one that
   exists:

   ```
   For any figure work (draft, revise, audit, export), read FIGURES.md first.
   ```

   If neither file exists, say so and suggest `init-writing-workspace`;
   still install the three files.
4. Check `python -c "import matplotlib, yaml"`. If it fails, report the
   missing package and the install command; do not skip the install.
5. Confirm: list files created, and state in one sentence that figures in
   this folder are now drawn from `figure_spec.yaml` through `figspec.py`
   and audited against it.

## Spec defaults

The shipped `figure_spec.yaml` is a working spec, not a blank template:
Arial, the Nature hierarchy shifted up one step (8 pt axis titles, 7 pt tick
labels, 9 pt bold panel labels), 0.5 pt spines, 0.75 pt data lines, and a
120 mm Elsevier-width canvas holding four 45 x 45 mm panels.

The `text`, `lines`, `ticks`, `markers`, `legend`, and `colors` blocks carry
over to any manuscript. The `meta`, `canvas`, `panels`, and `markers_by_site`
blocks are per-project: say so at install time and expect the author to edit
them for their own figure. If the author names another journal, adjust
`canvas.width_mm` and note any other known differences, but do not invent
journal numbers; say which values are unverified.

## Updating the canonical content

Edit the file under `assets/` in this skill, then offer to re-run the init
on active projects. For `figure_spec.yaml`, re-running only appends new
keys; it never resets tuned values.
