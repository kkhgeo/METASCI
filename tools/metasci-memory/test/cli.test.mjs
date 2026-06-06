import { test } from 'node:test'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import { execFileSync } from 'node:child_process'

const SCRIPT = new URL('../scripts/memory.mjs', import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1')
function tmp() { return fs.mkdtempSync(path.join(os.tmpdir(), 'memcli-')) }

test('CLI append-fact via --text then load prints it', () => {
  const dir = tmp()
  execFileSync('node', [SCRIPT, 'append-fact', '--root', dir, '--agent', 'Gaster', '--text', 'CLI 사실'])
  const out = execFileSync('node', [SCRIPT, 'load', '--root', dir]).toString()
  assert.match(out, /CLI 사실/)
})

test('CLI record reads text from stdin when --text absent', () => {
  const dir = tmp()
  execFileSync('node', [SCRIPT, 'record', '--root', dir, '--session', 's1', '--role', 'Codex'], {
    input: '여러 줄\n응답 텍스트',
  })
  const body = fs.readFileSync(path.join(dir, '_memory', 'sessions', 's1.md'), 'utf8')
  assert.match(body, /여러 줄\n응답 텍스트/)
})

test('CLI list prints session filenames', () => {
  const dir = tmp()
  execFileSync('node', [SCRIPT, 'record', '--root', dir, '--session', 's1', '--role', '나', '--text', 'a'])
  const out = execFileSync('node', [SCRIPT, 'list', '--root', dir]).toString()
  assert.match(out, /s1\.md/)
})
