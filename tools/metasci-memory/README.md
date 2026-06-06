# metasci-memory

작업 폴더 기반 메모리 스킬 — AI 에이전트가 **현재 작업 폴더의 `_memory/`** 에 대화 핵심을 기록하고 다음 대화에서 회상한다. 순수 마크다운(외부 의존성 0), Claude Code / Codex 등 [Agent Skills](https://agentskills.io) 표준 호환.

## 무엇을 저장하나

```
<작업폴더>/
└── _memory/
    ├── MEMORY.md              # 엄선된 핵심 사실 (결정·제약·선호·할일). 최신 우선.
    └── sessions/
        └── 2026-06-05-1430.md # 세션별 대화 로그 (append-only)
```

- **MEMORY.md** — `## [날짜] 유형 · 작성자` 형식의 한 줄 사실 + `#태그`.
- **sessions/** — `## [hh:mm] 발언자` + 원문.

## 3층 구조

```
코어        scripts/memory.mjs   결정적 파일 I/O (init·record·append-fact·load·list)
            SKILL.md             "언제 무엇을 기억/회상" 판단 규칙
방아쇠 1    말로 호출             "기억해둬" / "메모리 불러와" → 에이전트가 스킬 실행
방아쇠 2    훅(자동)             SessionStart=자동 회상, Stop=자동 기록
방아쇠 3    호스트 앱             앱이 memory.mjs를 직접 호출 (예: Electron 통합)
```

핵심: **기록·회상은 기계적(스크립트)**, **핵심 추출만 에이전트의 판단**.

## 코어 명령 (`scripts/memory.mjs`)

```bash
node scripts/memory.mjs init   --root <폴더>
node scripts/memory.mjs record --root <폴더> --session <id> --role <이름>   # 본문은 stdin 또는 --text
node scripts/memory.mjs append-fact --root <폴더> --agent <이름> --type <decision|constraint|preference|todo|fact> --text "<한 줄>" --tags "#a #b"
node scripts/memory.mjs load   --root <폴더> [--max 8000]   # MEMORY.md 60% + 최근 세션 tail
node scripts/memory.mjs list   --root <폴더>
```

`load`는 상한(`--max`) 안에서 MEMORY.md(우선 60%)와 최근 세션 tail을 함께 돌려준다 — 큰 MEMORY.md가 최근 맥락을 밀어내지 않도록.

## 자동화 훅 (standalone Claude Code)

설치하면 앱 없이도 매 턴 자동 기록 + 새 세션마다 자동 회상:

```bash
# 현재 폴더에만 (그 폴더의 .claude/settings.local.json, git 미추적)
node scripts/install-hooks.mjs --here

# 특정 폴더
node scripts/install-hooks.mjs --dir <경로>

# 전역 (~/.claude/settings.json)
node scripts/install-hooks.mjs

# 끄기
node scripts/install-hooks.mjs --here --uninstall
```

또는 한 세션만 임시로: `claude --settings hooks/settings-snippet.json` (경로는 환경에 맞게).
설치는 SessionStart/Stop 훅을 등록하므로 **변경 후 Claude Code를 다시 켜야** 적용된다.

> 클로드에게 말로도 가능: "이 폴더에 메모리 자동화 켜줘/꺼줘" → 스킬이 `install-hooks.mjs --here [--uninstall]` 실행.

## 테스트

```bash
node --test "test/memory.test.mjs" "test/cli.test.mjs" "test/hooks.test.mjs"
```

Node 18+ 내장 `node:test` 사용, 외부 의존성 없음.
