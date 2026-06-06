#!/usr/bin/env node
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'

const SKILL = path.resolve(import.meta.dirname, '..')
const args = process.argv.slice(2)
function argVal(name) {
  const i = args.indexOf(name)
  return i !== -1 ? args[i + 1] : undefined
}

// 대상 settings 파일 결정.
// 우선순위: CLAUDE_SETTINGS_PATH > --dir <경로> / --here > 전역(~/.claude/settings.json)
// 프로젝트 범위(--here/--dir)는 git에 올라가지 않는 개인 설정 settings.local.json 에 둔다.
let settingsPath
if (process.env.CLAUDE_SETTINGS_PATH) {
  settingsPath = process.env.CLAUDE_SETTINGS_PATH
} else if (args.includes('--here') || argVal('--dir')) {
  const dir = argVal('--dir') || process.cwd()
  settingsPath = path.join(dir, '.claude', 'settings.local.json')
} else {
  settingsPath = path.join(os.homedir(), '.claude', 'settings.json')
}

const uninstall = args.includes('--uninstall')
const inject = `node "${path.join(SKILL, 'hooks', 'inject-memory.mjs')}"`
const recordC = `node "${path.join(SKILL, 'hooks', 'record-turn.mjs')}"`
// 이 스킬 소속 훅인지 식별 (경로가 달라도 스크립트 파일명으로 매칭)
const isOurs = (cmd) => /inject-memory\.mjs|record-turn\.mjs/.test(cmd || '')

let settings = {}
if (fs.existsSync(settingsPath)) {
  try { settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8')) } catch { settings = {} }
}
settings.hooks = settings.hooks || {}

function addHook(event, command) {
  settings.hooks[event] = settings.hooks[event] || []
  const exists = settings.hooks[event].some(
    (entry) => entry?.hooks?.some?.((h) => h.command === command)
  )
  if (!exists) settings.hooks[event].push({ hooks: [{ type: 'command', command }] })
}

// 이 스킬이 등록한 훅만 골라 제거. 비워진 이벤트 키는 삭제.
function removeOurHooks(event) {
  if (!Array.isArray(settings.hooks[event])) return
  settings.hooks[event] = settings.hooks[event].filter(
    (entry) => !entry?.hooks?.some?.((h) => isOurs(h.command))
  )
  if (settings.hooks[event].length === 0) delete settings.hooks[event]
}

if (uninstall) {
  removeOurHooks('SessionStart')
  removeOurHooks('Stop')
} else {
  addHook('SessionStart', inject)
  addHook('Stop', recordC)
}

fs.mkdirSync(path.dirname(settingsPath), { recursive: true }) // .claude 폴더가 없으면 생성
fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2))
process.stdout.write(
  (uninstall ? 'Removed' : 'Installed') + ' metasci-memory hooks ' + (uninstall ? 'from ' : 'into ') + settingsPath + '\n'
)
