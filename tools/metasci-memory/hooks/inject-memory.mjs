#!/usr/bin/env node
import fs from 'node:fs'
import { memRoot, load } from '../scripts/memory.mjs'

const raw = (() => { try { return fs.readFileSync(0, 'utf8') } catch { return '' } })()
let payload = {}
try { payload = JSON.parse(raw || '{}') } catch { payload = {} }
const cwd = payload.cwd || process.cwd()

let context = ''
try { context = load(memRoot({ root: cwd }), { max: 8000 }) } catch { context = '' }

process.stdout.write(JSON.stringify({
  hookSpecificOutput: {
    hookEventName: 'SessionStart',
    additionalContext: context,
  },
}))
