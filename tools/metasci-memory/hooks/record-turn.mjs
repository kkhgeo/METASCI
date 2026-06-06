#!/usr/bin/env node
import fs from 'node:fs'
import { memRoot, record } from '../scripts/memory.mjs'

const raw = (() => { try { return fs.readFileSync(0, 'utf8') } catch { return '' } })()
let payload = {}
try { payload = JSON.parse(raw || '{}') } catch { payload = {} }
const cwd = payload.cwd || process.cwd()
const tpath = payload.transcript_path
const session = (payload.session_id || '').slice(0, 8) || undefined

function textOf(content) {
  if (typeof content === 'string') return content
  if (Array.isArray(content)) {
    return content.filter((b) => b && b.type === 'text').map((b) => b.text).join('\n')
  }
  return ''
}

if (tpath && fs.existsSync(tpath)) {
  const rows = fs.readFileSync(tpath, 'utf8').split('\n').filter(Boolean).map((l) => {
    try { return JSON.parse(l) } catch { return null }
  }).filter(Boolean)
  const hasText = (r) => r && r.message && textOf(r.message.content).trim().length > 0
  const lastUser = [...rows].reverse().find((r) => r.message?.role === 'user' && hasText(r))
  const lastAsst = [...rows].reverse().find((r) => r.message?.role === 'assistant' && hasText(r))
  const root = memRoot({ root: cwd })
  if (lastUser) {
    const t = textOf(lastUser.message.content)
    if (t.trim()) record(root, { session, role: '나', text: t })
  }
  if (lastAsst) {
    const t = textOf(lastAsst.message.content)
    if (t.trim()) record(root, { session, role: 'Claude', text: t })
  }
}
process.exit(0)
