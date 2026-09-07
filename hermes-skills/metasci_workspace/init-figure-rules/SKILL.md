---
name: init-figure-rules
description: >
  Install workspace-level figure rules for publication figures that go from
  Python (matplotlib) to Illustrator with minimal post-editing: drops
  AGENT_figures.md (drafting and audit conventions), figure_spec.yaml (every
  number in pt/mm, Nature defaults), and figspec.py (library that applies
  the spec, prints a parameter sheet, renders wireframes, and audits
  exported PDF) into a manuscript folder, and adds one pointer line to
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
├── AGENT_figures.md   drafting and audit conventions (read before figure work)
├── figure_spec.yaml   every number: canvas, panels (box, legend, annotations, arrows),
│                     text, lines, ticks, markers, legend, colours, export
├── figspec.py         Spec.load / canvas / panel / style / legend / annotate / save /
│                     sheet / audit / wireframe / check_collisions
└── example_draft.py   worked example of the API — read it before writing the first
                      figure script; do not copy it into the project
```

## Procedure

1. Identify the target project root. If unclear, ask — do not guess.
2. Install three files: `AGENT_figures.md`, `figure_spec.yaml`, `figspec.py`.
   `example_draft.py` stays in the skill; read it, do not copy it. For each
   of the three, check whether it already exists there.
   - `FIGURES.md` (the name before the `AGENT_` prefix) present and
     `AGENT_figures.md` absent: rename it to `AGENT_figures.md`, then treat it
     as present.
   - Missing: copy from `assets/`.
   - `AGENT_figures.md` or `figspec.py` present: show a diff against the asset,
     recommend overwrite or keep with a reason, and wait.
   - `figure_spec.yaml` present: **never overwrite.** It holds the author's
     tuned numbers. Show which keys the canonical template has that the
     existing file lacks, and offer to append only those with default
     values.
3. Make sure the always-on instruction file points at `AGENT_figures.md`. Check
   `AGENTS.md`, then `CLAUDE.md`. **If either already mentions `AGENT_figures.md`,
   change nothing** — a workspace built by `init-writing-workspace` carries
   that line in its canonical text. If a line mentions the old name
   `FIGURES.md` instead, change that name to `AGENT_figures.md` in place and
   nothing else. Otherwise append to the first one that exists:

   ```
   For any figure work (draft, revise, audit, export), read AGENT_figures.md first.
   ```

   If neither file exists, say so and suggest `init-writing-workspace`;
   still install the three files.
4. Check `python -c "import matplotlib, yaml, pymupdf"`. matplotlib and pyyaml
   draw; `pymupdf` is what `figspec.py audit` reads the PDF with.
   If any is missing, report it with the install command
   (`python -m pip install matplotlib pyyaml pymupdf`); do not skip the
   install.
5. Confirm: list files created, and state in one sentence that figures in
   this folder are now drawn from `figure_spec.yaml` through `figspec.py`
   and audited against it.

## Spec defaults

The shipped `figure_spec.yaml` is a working spec, not a blank template:
Arial, the Nature hierarchy shifted up one step (8 pt axis titles, 7 pt tick
labels, 9 pt bold panel labels), 0.5 pt spines, 0.75 pt data lines, and a
120 mm Elsevier-width canvas holding four 45 x 45 mm panels. Export is PDF
only.

The `text`, `lines`, `ticks`, `markers`, `legend`, and `colors` blocks carry
over to any manuscript. The rest is the previous project's content: `meta`,
`canvas`, the panel boxes, and every `annotations` / `arrows` / per-panel
`legend` entry under `panels`. Say so at install time and strip the panel
content unless the author wants it as a starting point. If the author names
another journal, adjust `canvas.width_mm` and note any other known
differences, but do not invent journal numbers; say which values are
unverified.

## Updating the canonical content

Edit the file under `assets/` in this skill, then offer to re-run the init
on active projects. For `figure_spec.yaml`, re-running only appends new
keys; it never resets tuned values.
