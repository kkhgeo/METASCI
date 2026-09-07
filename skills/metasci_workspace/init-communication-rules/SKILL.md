---
name: init-communication-rules
description: >
  Install the author-dialogue communication rules (AI-tell removal, adapted
  from pstack's unslop) into a manuscript workspace as one standalone
  `AGENT_communication.md`, so CLAUDE.md and AGENTS.md stay short and the
  rules survive a workspace regeneration. Use when the user says "대화 규율
  추가해줘", "대화 규칙 파일 만들어줘", "unslop 규칙 적용해줘", "AI 말투 빼는 규칙
  넣어줘", "init communication rules", "대화 규칙 초기화", or complains that the
  agent's replies sound like a chatbot. Sibling of init-writing-workspace:
  that one creates the workspace, this one drops in the dialogue rules.
  Also use to update the file, migrate an older inline block out of
  CLAUDE.md, or remove it.
---

# Init Communication Rules

Writes one standalone file, `AGENT_communication.md`, holding the rules that
strip chatbot tells from the agent's own replies (review reports,
explanations, recommendations). It governs dialogue only; manuscript text
stays under the meta-* skills and their approval flow.

The content lives in `assets/AGENT_communication.md`. **Never rewrite it from
memory** — copy it verbatim, version comment included.

## Why a separate file

Earlier versions appended the rules into `CLAUDE.md` and `AGENTS.md`. That
failed twice: `init-writing-workspace` regenerates those files from its own
canonical asset and wiped the block, and a 50-line block doubled the length
of a 63-line CLAUDE.md in every project. A standalone file is untouched by
regeneration, and the author loads it when they want it.

**Do not append the rules into CLAUDE.md or AGENTS.md.** Not "just this
once", not "because the project is small", not as a copy "for safety". One
file, one place.

## Procedure

1. Identify the target project root. If unclear, ask — do not guess.
   `CLAUDE.md` does not need to exist; this file stands on its own.
2. Copy `assets/AGENT_communication.md` to `<root>/AGENT_communication.md`.
   - **Absent:** write it verbatim.
   - **Present, same version:** report "already current", change nothing.
   - **Present, older version or hand-edited:** show a diff against the
     asset, recommend replacing, and wait for the decision.
3. Migrate any inline copy: if `CLAUDE.md` or `AGENTS.md` contains
   `<!-- metasci:communication-rules` … `<!-- /metasci:communication-rules -->`,
   delete that block, markers inclusive, and nothing else. Report the line
   count removed from each file.
4. Report which files changed, and tell the author how the rules get loaded
   (next section) in one sentence.

Do not create `.claude/rules/`, do not write a second copy anywhere, and do
not edit CLAUDE.md or AGENTS.md beyond the migration deletion in step 3.

## How the rules get loaded

Default is manual: the author types `@AGENT_communication.md` in the prompt
when they want the rules in play for that session. Nothing loads on its own,
nothing costs context until used.

A `CLAUDE.md` carrying the research-principles block (installed by
`init-research-principles`, and by `init-writing-workspace` alongside its
own block) already has one line telling any agent to read
`AGENT_communication.md` at session start if it exists, so those folders
pick it up without further wiring.

Offer permanent auto-loading only if the author asks for it, and name the
cost: the rules then enter context at launch in every session.

- **A runtime that expands `@path` imports inside CLAUDE.md:** append a line
  containing `@AGENT_communication.md` (no backticks) to `CLAUDE.md`. It
  expands at launch.
- **A runtime that reads AGENTS.md literally:** `@` stays text. Append a plain
  instruction to `AGENTS.md` instead: read `AGENT_communication.md` first and
  follow it.

## Removing

Delete `<root>/AGENT_communication.md`, and any auto-load line added above.
Touch nothing else.

## Updating the rules

Edit `assets/AGENT_communication.md`, bump the version in its opening
`<!-- metasci:communication-rules vN -->` comment, rebuild the generated trees
(`node tools/build-agent-skills.mjs`), then offer to re-run the skill on
active projects.
