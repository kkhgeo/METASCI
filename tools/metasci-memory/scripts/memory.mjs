import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import { pathToFileURL } from 'node:url'

// cwd 드리프트에 좌우되지 않도록 프로젝트 루트를 위로 거슬러 탐색한다.
// 1) 기존 _memory/ 가 있는 조상 재사용(중복·stray 방지) → 2) .claude/·.git/ 마커(home 자신 제외)
// → 3) 못 찾으면 cwd. 명시적 opts.root 는 항상 우선(훅·--root 는 기존 동작 그대로).
export function resolveProjectRoot(start = process.cwd()) {
  const home = os.homedir()
  let dir = path.resolve(start)
  for (let d = dir; ; ) {
    if (fs.existsSync(path.join(d, '_memory'))) return d
    if (d === home) break
    const parent = path.dirname(d)
    if (parent === d) break
    d = parent
  }
  for (let d = dir; d !== home; ) {
    if (fs.existsSync(path.join(d, '.claude')) || fs.existsSync(path.join(d, '.git'))) return d
    const parent = path.dirname(d)
    if (parent === d) break
    d = parent
  }
  return dir
}

export function memRoot(opts = {}) {
  const base = opts.root || resolveProjectRoot()
  return path.join(base, '_memory')
}

const HEADER =
  '# Project Memory\n\n<!-- 엄선된 핵심 사실. 최신 우선. memory.mjs로만 수정. -->\n'

export function ensure(root) {
  fs.mkdirSync(path.join(root, 'sessions'), { recursive: true })
  const mem = path.join(root, 'MEMORY.md')
  if (!fs.existsSync(mem)) fs.writeFileSync(mem, HEADER, 'utf8')
  return root
}

function pad(n) { return String(n).padStart(2, '0') }
export function todayId(d = new Date()) {
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`
}
function hhmm(d = new Date()) { return `${pad(d.getHours())}:${pad(d.getMinutes())}` }

export function record(root, { session, role, text }) {
  ensure(root)
  const id = session || todayId()
  const file = path.join(root, 'sessions', id + '.md')
  try { fs.writeFileSync(file, `# Session ${id}\n`, { encoding: 'utf8', flag: 'wx' }) } catch { /* exists */ }
  fs.appendFileSync(file, `\n## [${hhmm()}] ${role}\n${text}\n`, 'utf8')
  return file
}

export function appendFact(root, { agent, text, type = 'fact', tags = '' }) {
  ensure(root)
  const mem = path.join(root, 'MEMORY.md')
  const cur = fs.readFileSync(mem, 'utf8')
  const lines = cur.split('\n')
  let at = lines.findIndex((l) => l.includes('-->'))
  if (at === -1) at = 0
  const head = lines.slice(0, at + 1).join('\n')
  const rest = lines.slice(at + 1).join('\n')
  const body = tags ? `${text} ${tags}` : text
  const entry = `\n## [${todayId()}] ${type} · ${agent}\n${body}\n`
  fs.writeFileSync(mem, head + (head.endsWith('\n') ? '' : '\n') + entry + rest, 'utf8')
  return mem
}

export function listSessions(root) {
  const dir = path.join(root, 'sessions')
  if (!fs.existsSync(dir)) return []
  return fs
    .readdirSync(dir)
    .filter((f) => f.endsWith('.md'))
    .sort()
    .map((f) => {
      const p = path.join(dir, f)
      return { path: p, size: fs.statSync(p).size }
    })
}

export function load(root, { max = 8000 } = {}) {
  ensure(root)
  const memText = fs.readFileSync(path.join(root, 'MEMORY.md'), 'utf8')
  const memBudget = Math.floor(max * 0.6)
  const memPart =
    memText.length > memBudget ? memText.slice(0, memBudget) + '\n…(truncated)\n' : memText
  const sessions = listSessions(root)
  let sessPart = ''
  if (sessions.length) {
    const latest = sessions[sessions.length - 1]
    const t = fs.readFileSync(latest.path, 'utf8')
    const sessBudget = Math.max(0, max - memPart.length)
    sessPart =
      sessBudget === 0 ? '' :
      t.length > sessBudget ? '…(earlier truncated)\n' + t.slice(-sessBudget) : t
  }
  return memPart + (sessPart ? `\n\n--- 최근 세션 ---\n${sessPart}` : '')
}

function parseArgs(argv) {
  const o = {}
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i]
    if (a.startsWith('--')) {
      const key = a.slice(2)
      const next = argv[i + 1]
      if (next === undefined || next.startsWith('--')) o[key] = true
      else { o[key] = next; i++ }
    }
  }
  return o
}
function readStdin() {
  try { return fs.readFileSync(0, 'utf8') } catch { return '' }
}
function neededText(o) {
  return o.text === true || o.text === undefined ? readStdin().replace(/\n+$/, '') : o.text
}

// 직접 실행될 때만 CLI로 동작 (import 시에는 함수만 export)
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const [cmd, ...rest] = process.argv.slice(2)
  const o = parseArgs(rest)
  const root = memRoot({ root: o.root })
  switch (cmd) {
    case 'init':
      ensure(root); process.stdout.write(root + '\n'); break
    case 'record':
      record(root, { session: o.session, role: o.role || '?', text: neededText(o) }); break
    case 'append-fact':
      appendFact(root, { agent: o.agent || '?', type: o.type, text: neededText(o), tags: o.tags }); break
    case 'load':
      process.stdout.write(load(root, { max: o.max ? Number(o.max) : 8000 })); break
    case 'list':
      for (const s of listSessions(root)) process.stdout.write(`${path.basename(s.path)}\t${s.size}\n`); break
    default:
      process.stderr.write(`unknown command: ${cmd}\n`); process.exit(1)
  }
}
