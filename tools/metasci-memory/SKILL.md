---
name: metasci-memory
description: 작업 폴더의 _memory/에 대화 핵심을 기록하고 회상한다. "기억해둬", "메모리 불러와", "이번 세션 정리해줘", "이 폴더에 메모리 자동화 켜줘/꺼줘" 등의 요청 시 사용. 결정·제약·선호·미해결 과제를 영속화하고, 폴더 단위 자동 기록·회상(훅)을 켜고 끈다.
allowed-tools: [Bash, Read]
---

# metasci-memory

현재 작업 폴더(`cwd`)의 `_memory/`에 메모리를 유지한다. 모든 파일 조작은 번들된
`scripts/memory.mjs`를 통해서만 한다(형식 일관성·충돌 방지). 직접 편집 금지.

스크립트 경로: `${CLAUDE_SKILL_DIR}/scripts/memory.mjs`

## 무엇을 기억하나
기억할 가치가 있는 것: **결정(decision)**, **제약(constraint)**, **선호(preference)**,
**미해결 과제(todo)**, 그 외 핵심 **사실(fact)**. 사실은 atomic(한 항목=한 사실), 한국어 한 줄.

## 명령
- 핵심 사실 추가:
  `node "${CLAUDE_SKILL_DIR}/scripts/memory.mjs" append-fact --agent <이름> --type <decision|constraint|preference|todo|fact> --text "<한 줄>" --tags "#a #b"`
- 회상(읽기): `node "${CLAUDE_SKILL_DIR}/scripts/memory.mjs" load`
- 세션 로그 기록: `node "${CLAUDE_SKILL_DIR}/scripts/memory.mjs" record --role <이름> --text "<발언>"`
  (긴 텍스트는 `--text` 대신 stdin으로 파이프 가능)
- 세션 목록: `node "${CLAUDE_SKILL_DIR}/scripts/memory.mjs" list`

## 언제 무엇을 하나
1. 사용자가 "기억해둬"라고 하거나, 대화에서 중요한 결정·제약·선호가 확정되면 → `append-fact`.
2. 사용자가 "메모리 불러와"/"내가 뭘 기억하랬지"라고 하면 → `load` 후 그 내용을 반영해 답한다.
3. **세션 정리(curate) 요청 시**: 먼저 `list`로 최근 세션 파일을 찾고 그 로그를 Read로 읽은 뒤,
   핵심만 골라 `append-fact`로 추가한다. 단 `load`로 기존 MEMORY.md를 먼저 읽어
   **이미 있는 항목과 중복되는 사실은 추가하지 않는다.**

## 자동화 켜기/끄기 (폴더 단위 훅)
"기억해둬"는 사용자가 말할 때만 동작한다. **매 턴 자동 기록 + 새 세션마다 자동 회상**을 원하면
Claude Code 훅을 설치한다. 사용자가 "이 폴더에 메모리 자동화 켜줘"(또는 "꺼줘")라고 하면:

- **켜기 (현재 폴더만)**: `node "${CLAUDE_SKILL_DIR}/scripts/install-hooks.mjs" --here`
  → 현재 폴더에 `.claude/settings.local.json`(git 미추적)을 만들어 SessionStart+Stop 훅 등록.
- **끄기 (현재 폴더)**: `node "${CLAUDE_SKILL_DIR}/scripts/install-hooks.mjs" --here --uninstall`
- **전역(모든 폴더) 켜기/끄기**: `--here` 없이 같은 명령(`--uninstall`로 끄기). 전역은 `~/.claude/settings.json`을 바꾸므로 사용자에게 먼저 확인할 것.

실행 후 사용자에게 알릴 것: **변경은 다음 세션부터 적용**되므로 Claude Code를 다시 켜야 한다.
(특정 한 세션만 임시로 켜려면 설치 대신 `claude --settings "${CLAUDE_SKILL_DIR}/hooks/settings-snippet.json"` 로 실행하면 됨 — 영구 변경 없음.)

## 규칙
- `_memory/`의 파일을 손으로 수정하지 말 것. 항상 위 명령 사용.
- 한 사실이 너무 길면 쪼개서 여러 `append-fact`로.
- 추측이 아니라 확정된 것만 기억한다.
- 자동화 훅 설치/제거는 설정 파일을 바꾸므로, 전역(`--here` 없음)일 때는 실행 전 사용자 확인.
