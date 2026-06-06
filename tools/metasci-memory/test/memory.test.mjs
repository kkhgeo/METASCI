import { test } from 'node:test'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import { memRoot, ensure, record, appendFact, listSessions, load } from '../scripts/memory.mjs'

function tmp() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'mem-'))
}

test('memRoot returns _memory under root', () => {
  assert.equal(memRoot({ root: '/x' }), path.join('/x', '_memory'))
})

test('ensure creates _memory, sessions/, MEMORY.md', () => {
  const dir = tmp()
  const root = memRoot({ root: dir })
  ensure(root)
  assert.ok(fs.existsSync(path.join(root, 'sessions')))
  const mem = fs.readFileSync(path.join(root, 'MEMORY.md'), 'utf8')
  assert.match(mem, /# Project Memory/)
})

test('ensure is idempotent and preserves MEMORY.md', () => {
  const dir = tmp()
  const root = memRoot({ root: dir })
  ensure(root)
  fs.appendFileSync(path.join(root, 'MEMORY.md'), '\n## keep me\n')
  ensure(root)
  assert.match(fs.readFileSync(path.join(root, 'MEMORY.md'), 'utf8'), /keep me/)
})

test('record appends a turn to sessions/<id>.md', () => {
  const dir = tmp()
  const root = memRoot({ root: dir })
  const file = record(root, { session: '2026-06-05-1430', role: '나', text: '서론 다듬어줘' })
  const body = fs.readFileSync(file, 'utf8')
  assert.match(body, /# Session 2026-06-05-1430/)
  assert.match(body, /## \[\d{2}:\d{2}\] 나/)
  assert.match(body, /서론 다듬어줘/)
})

test('record appends multiple turns to the same file', () => {
  const dir = tmp()
  const root = memRoot({ root: dir })
  record(root, { session: 's1', role: '나', text: 'a' })
  const file = record(root, { session: 's1', role: 'Codex', text: 'b' })
  const body = fs.readFileSync(file, 'utf8')
  assert.match(body, /## \[\d{2}:\d{2}\] 나\na/)
  assert.match(body, /## \[\d{2}:\d{2}\] Codex\nb/)
})

test('record defaults session id to today (YYYY-MM-DD)', () => {
  const dir = tmp()
  const root = memRoot({ root: dir })
  const file = record(root, { role: '나', text: 'x' })
  assert.match(path.basename(file), /^\d{4}-\d{2}-\d{2}\.md$/)
})

test('appendFact inserts entry below header, newest first', () => {
  const dir = tmp()
  const root = memRoot({ root: dir })
  appendFact(root, { agent: 'Gaster', type: 'decision', text: '첫 번째', tags: '#a' })
  appendFact(root, { agent: 'Claude', type: 'preference', text: '두 번째' })
  const mem = fs.readFileSync(path.join(root, 'MEMORY.md'), 'utf8')
  // header가 맨 위, 그 다음 최신(두 번째)이 먼저
  assert.match(mem, /# Project Memory/)
  const idx1 = mem.indexOf('첫 번째')
  const idx2 = mem.indexOf('두 번째')
  assert.ok(idx2 < idx1, '최신 항목이 위에 있어야 함')
  assert.match(mem, /## \[\d{4}-\d{2}-\d{2}\] decision · Gaster/)
  assert.match(mem, /첫 번째 #a/)
})

test('listSessions returns session files sorted by name ascending', () => {
  const dir = tmp()
  const root = memRoot({ root: dir })
  record(root, { session: '2026-06-04', role: '나', text: 'old' })
  record(root, { session: '2026-06-05', role: '나', text: 'new' })
  const s = listSessions(root)
  assert.equal(s.length, 2)
  assert.equal(path.basename(s[s.length - 1].path), '2026-06-05.md')
})

test('load returns MEMORY.md plus latest session tail', () => {
  const dir = tmp()
  const root = memRoot({ root: dir })
  appendFact(root, { agent: 'Gaster', type: 'decision', text: 'PDF는 shell로 연다' })
  record(root, { session: '2026-06-05', role: 'Codex', text: '최근 작업 내용' })
  const out = load(root, { max: 8000 })
  assert.match(out, /PDF는 shell로 연다/)
  assert.match(out, /최근 작업 내용/)
  assert.match(out, /최근 세션/)
})

test('load respects max budget (truncates)', () => {
  const dir = tmp()
  const root = memRoot({ root: dir })
  appendFact(root, { agent: 'X', text: 'y'.repeat(5000) })
  const out = load(root, { max: 1000 })
  assert.ok(out.length <= 1200, 'budget 근처로 잘려야 함')
  assert.match(out, /truncated/)
})

test('load on empty memory returns header only, no crash', () => {
  const dir = tmp()
  const root = memRoot({ root: dir })
  const out = load(root, { max: 8000 })
  assert.match(out, /# Project Memory/)
})

test('load reserves budget so session tail survives a large MEMORY.md', () => {
  const dir = tmp()
  const root = memRoot({ root: dir })
  appendFact(root, { agent: 'X', text: 'm'.repeat(5000) })
  record(root, { session: '2026-06-05', role: 'Codex', text: 'TAIL_MARKER ' + 's'.repeat(300) })
  const out = load(root, { max: 1000 })
  assert.ok(out.length <= 1100, '전체가 상한 근처로 제한되어야 함')
  assert.ok(out.includes('TAIL_MARKER'), '큰 MEMORY.md여도 최근 세션 tail이 살아남아야 함')
  assert.match(out, /truncated/)
})
