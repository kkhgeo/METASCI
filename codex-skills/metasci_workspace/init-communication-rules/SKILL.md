---
name: init-communication-rules
description: >
  Append a "Communication Rules" block (AI-tell removal for agent↔author
  dialogue, adapted from pstack's unslop) to an existing CLAUDE.md and
  AGENTS.md in a manuscript workspace, without touching anything else in
  those files. Use when the user says "대화 규율 추가해줘", "대화 스킬 넣어줘",
  "unslop 규칙 적용해줘", "AI 말투 빼는 규칙 넣어줘", "init communication
  rules", "대화 규칙 초기화", "이 폴더 클로드 코드 대화 개선", or complains that the agent's
  review reports sound like a chatbot. Sibling of init-writing-workspace:
  that one creates the workspace, this one adds a rule block on demand.
  Also use to update or remove the block.
---

# Init Communication Rules

Appends one self-contained rule block to the workspace instruction files so
the agent's own replies (review reports, explanations, recommendations)
drop chatbot tells. It governs dialogue only; manuscript text stays under
the meta-* skills and their approval flow.

The block lives in `assets/communication-rules.md`. **Never rewrite it from
memory** — copy it verbatim, markers included:

```
<!-- metasci:communication-rules v1 -->
...
<!-- /metasci:communication-rules -->
```

The markers make the operation idempotent, versionable, and reversible.

## Procedure

1. Identify the target project root. If unclear, ask — do not guess.
2. Confirm `CLAUDE.md` exists there. If it does not, stop and offer
   `init-writing-workspace` instead; this skill never creates a workspace.
3. If `AGENTS.md` is missing, create it as an exact copy of `CLAUDE.md`
   first, so both files end up identical.
4. Read `assets/communication-rules.md` and note the version in its opening
   marker.
5. For each of `CLAUDE.md` and `AGENTS.md`:
   - **No marker present:** append the block verbatim. Place it before
     `## Project-Specific` if that section exists, otherwise at the end.
     One blank line before the block.
   - **Same version present:** report "already installed" and change
     nothing.
   - **Older version present:** show a diff of the existing block against
     the asset, recommend replacing, and on approval replace only the text
     between the markers.
   - Never edit anything outside the markers.
6. If a `.claude/` directory already exists in the project root, also write
   the block to `.claude/rules/communication-rules.md` (Codex CLI reads this
   directory automatically). Do not create `.claude/` if it is absent; the
   CLAUDE.md/AGENTS.md copy is what all agents share.
7. Confirm: list the files touched and state in one sentence what changes
   in the agent's replies from the next session.

## Removing

On request, delete from `<!-- metasci:communication-rules` through
`<!-- /metasci:communication-rules -->` inclusive in both files, and
`.claude/rules/communication-rules.md` if present. Touch nothing else.

## Updating the rules

To change the rules themselves, edit `assets/communication-rules.md` and bump the
version in both markers, then offer to re-run this skill on active projects.
