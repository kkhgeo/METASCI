import { test } from 'node:test'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import { execFileSync } from 'node:child_process'

function tmp() { return fs.mkdtempSync(path.join(os.tmpdir(), 'memhook-')) }
const MEMORY = path.resolve(import.meta.dirname, '../scripts/memory.mjs')
const INJECT = path.resolve(import.meta.dirname, '../hooks/inject-memory.mjs')

test('inject-memory outputs additionalContext JSON from MEMORY.md', () => {
  const dir = tmp()
  // 시드: 사실 하나
  execFileSync('node', [MEMORY, 'append-fact', '--root', dir, '--agent', 'X', '--text', '주입될 사실'])
  const out = execFileSync('node', [INJECT], { input: JSON.stringify({ cwd: dir, hook_event_name: 'SessionStart' }) }).toString()
  const parsed = JSON.parse(out)
  assert.equal(parsed.hookSpecificOutput.hookEventName, 'SessionStart')
  assert.match(parsed.hookSpecificOutput.additionalContext, /주입될 사실/)
})

test('inject-memory on folder without _memory does not crash, emits empty-ish', () => {
  const dir = tmp()
  const out = execFileSync('node', [INJECT], { input: JSON.stringify({ cwd: dir }) }).toString()
  const parsed = JSON.parse(out)
  assert.match(parsed.hookSpecificOutput.additionalContext, /# Project Memory/)
})

const RECORD = path.resolve(import.meta.dirname, '../hooks/record-turn.mjs')

test('record-turn extracts last user+assistant from transcript and logs them', () => {
  const dir = tmp()
  const tpath = path.join(dir, 't.jsonl')
  // Claude transcript JSONL 형태(간략): 각 줄 {type, message:{role, content}}
  const lines = [
    { type: 'user', message: { role: 'user', content: '서론 고쳐줘' } },
    { type: 'assistant', message: { role: 'assistant', content: [{ type: 'text', text: '고쳤습니다' }] } },
  ].map((o) => JSON.stringify(o)).join('\n')
  fs.writeFileSync(tpath, lines)
  execFileSync('node', [RECORD], { input: JSON.stringify({ cwd: dir, transcript_path: tpath, session_id: 'abc' }) })
  const sessFile = fs.readdirSync(path.join(dir, '_memory', 'sessions'))[0]
  const body = fs.readFileSync(path.join(dir, '_memory', 'sessions', sessFile), 'utf8')
  assert.match(body, /서론 고쳐줘/)
  assert.match(body, /고쳤습니다/)
})

test('record-turn without transcript does not crash', () => {
  const dir = tmp()
  execFileSync('node', [RECORD], { input: JSON.stringify({ cwd: dir }) })
  assert.ok(true)
})

test('record-turn skips tool_result/tool_use rows, picks real human+assistant text', () => {
  const dir = tmp()
  const tpath = path.join(dir, 't.jsonl')
  // 실제 사람 질문 → assistant가 도구 사용(tool_use, 텍스트 없음) → tool_result(role:user) 순.
  // 마지막 user 행은 tool_result, 마지막 assistant 행은 pure tool_use 이므로 무시되어야 함.
  const lines = [
    { type: 'user', message: { role: 'user', content: '진짜 질문' } },
    { type: 'assistant', message: { role: 'assistant', content: [{ type: 'text', text: '진짜 답변' }] } },
    { type: 'assistant', message: { role: 'assistant', content: [{ type: 'tool_use', id: 't1', name: 'Read', input: {} }] } },
    { type: 'user', message: { role: 'user', content: [{ type: 'tool_result', tool_use_id: 't1', content: '파일 내용' }] } },
  ].map((o) => JSON.stringify(o)).join('\n')
  fs.writeFileSync(tpath, lines)
  execFileSync('node', [RECORD], { input: JSON.stringify({ cwd: dir, transcript_path: tpath, session_id: 'tool-turn' }) })
  const sessFile = fs.readdirSync(path.join(dir, '_memory', 'sessions'))[0]
  const body = fs.readFileSync(path.join(dir, '_memory', 'sessions', sessFile), 'utf8')
  assert.match(body, /진짜 질문/)
  assert.match(body, /진짜 답변/)
  assert.doesNotMatch(body, /파일 내용/, '도구 결과(tool_result)는 user 턴으로 기록되면 안 됨')
})

const INSTALLER = path.resolve(import.meta.dirname, '../scripts/install-hooks.mjs')

test('install-hooks merges both SessionStart and Stop hooks', () => {
  const dir = tmp()
  const settingsPath = path.join(dir, 'settings.json')
  execFileSync('node', [INSTALLER], { env: { ...process.env, CLAUDE_SETTINGS_PATH: settingsPath } })
  const settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'))
  assert.ok(settings.hooks && settings.hooks.SessionStart, 'SessionStart hook missing')
  assert.ok(settings.hooks && settings.hooks.Stop, 'Stop hook missing')
  const ssCmd = JSON.stringify(settings.hooks.SessionStart)
  const stopCmd = JSON.stringify(settings.hooks.Stop)
  assert.match(ssCmd, /inject-memory/)
  assert.match(stopCmd, /record-turn/)
})

test('install-hooks is idempotent — no duplicate entries on second run', () => {
  const dir = tmp()
  const settingsPath = path.join(dir, 'settings.json')
  const env = { ...process.env, CLAUDE_SETTINGS_PATH: settingsPath }
  execFileSync('node', [INSTALLER], { env })
  execFileSync('node', [INSTALLER], { env })
  const settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'))
  assert.equal(settings.hooks.SessionStart.length, 1, 'SessionStart should have exactly 1 entry after 2 runs')
  assert.equal(settings.hooks.Stop.length, 1, 'Stop should have exactly 1 entry after 2 runs')
})

test('install-hooks preserves pre-existing unrelated hooks', () => {
  const dir = tmp()
  const settingsPath = path.join(dir, 'settings.json')
  // Write a settings file with an existing unrelated hook
  const existing = {
    hooks: {
      PreToolUse: [{ hooks: [{ type: 'command', command: 'echo pre-tool-use' }] }],
      Stop: [{ hooks: [{ type: 'command', command: 'echo existing-stop' }] }],
    },
  }
  fs.writeFileSync(settingsPath, JSON.stringify(existing, null, 2))
  execFileSync('node', [INSTALLER], { env: { ...process.env, CLAUDE_SETTINGS_PATH: settingsPath } })
  const settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'))
  // Pre-existing PreToolUse hook preserved
  assert.ok(settings.hooks.PreToolUse, 'PreToolUse hook should be preserved')
  assert.equal(settings.hooks.PreToolUse.length, 1)
  assert.match(JSON.stringify(settings.hooks.PreToolUse), /pre-tool-use/)
  // Stop hook now has both the existing one and the new metasci-memory one
  assert.equal(settings.hooks.Stop.length, 2, 'Stop should have 2 entries: existing + new')
  const stopStr = JSON.stringify(settings.hooks.Stop)
  assert.match(stopStr, /existing-stop/)
  assert.match(stopStr, /record-turn/)
})

test('install-hooks --here writes to <cwd>/.claude/settings.local.json (creating .claude)', () => {
  const dir = tmp() // 빈 폴더, .claude 없음
  // CLAUDE_SETTINGS_PATH 를 비워서 --here 경로 로직을 타게 한다. cwd 를 그 폴더로.
  const env = { ...process.env }
  delete env.CLAUDE_SETTINGS_PATH
  execFileSync('node', [INSTALLER, '--here'], { cwd: dir, env })
  const target = path.join(dir, '.claude', 'settings.local.json')
  assert.ok(fs.existsSync(target), '.claude/settings.local.json 가 생성되어야 함')
  const settings = JSON.parse(fs.readFileSync(target, 'utf8'))
  assert.match(JSON.stringify(settings.hooks.SessionStart), /inject-memory/)
  assert.match(JSON.stringify(settings.hooks.Stop), /record-turn/)
})

test('install-hooks --dir <path> targets that folder', () => {
  const base = tmp()
  const proj = path.join(base, 'myproject') // 아직 없음
  const env = { ...process.env }
  delete env.CLAUDE_SETTINGS_PATH
  execFileSync('node', [INSTALLER, '--dir', proj], { env })
  const target = path.join(proj, '.claude', 'settings.local.json')
  assert.ok(fs.existsSync(target), '--dir 가 가리키는 폴더에 설치되어야 함')
  const settings = JSON.parse(fs.readFileSync(target, 'utf8'))
  assert.match(JSON.stringify(settings.hooks.Stop), /record-turn/)
})

test('install-hooks --uninstall removes only our hooks, preserves others', () => {
  const dir = tmp()
  const settingsPath = path.join(dir, 'settings.json')
  const env = { ...process.env, CLAUDE_SETTINGS_PATH: settingsPath }
  // 먼저 무관한 Stop 훅을 둔 상태에서 설치
  fs.writeFileSync(settingsPath, JSON.stringify({
    hooks: { Stop: [{ hooks: [{ type: 'command', command: 'echo keep-me' }] }] },
  }))
  execFileSync('node', [INSTALLER], { env })
  // 설치 후: Stop = [keep-me, record-turn], SessionStart = [inject]
  let settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'))
  assert.equal(settings.hooks.Stop.length, 2)
  // 제거
  execFileSync('node', [INSTALLER, '--uninstall'], { env })
  settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'))
  // 우리 훅은 사라지고, 무관한 keep-me 와 SessionStart(빈 키 삭제됨)는?
  assert.equal(settings.hooks.Stop.length, 1, '무관한 Stop 훅은 보존')
  assert.match(JSON.stringify(settings.hooks.Stop), /keep-me/)
  assert.doesNotMatch(JSON.stringify(settings.hooks.Stop), /record-turn/)
  assert.ok(!settings.hooks.SessionStart, '우리만 있던 SessionStart 는 빈 키로 삭제')
})
