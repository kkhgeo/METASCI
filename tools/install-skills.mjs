// 이 저장소의 스킬을 이 컴퓨터의 전역 스킬 폴더에 건다.
//
//   node tools/install-skills.mjs             무엇을 할지 보여주기만 한다 (기본)
//   node tools/install-skills.mjs --apply     실제로 건다
//   node tools/install-skills.mjs --apply --replace
//                                             자리를 막고 있는 실물 폴더를 백업하고 링크로 바꾼다
//                                             (이 저장소에 같은 이름이 있는 것만. 나머지는 건드리지 않는다)
//
// 정본은 GitHub 이고 이 clone 이 그 사본이다. 전역 폴더에는 **심볼릭 링크**만 만든다.
// 그래서 갱신은 `git pull` 한 번이면 끝난다 — 다시 설치할 필요가 없다.
//
//   skills/<팩>/<스킬>        →  ~/.claude/skills/<스킬>     (Claude Code)
//   codex-skills/<팩>/<스킬>  →  ~/.codex/skills/<스킬>      (Codex CLI)
//
// 두 세트는 같은 이름을 쓰지만 폴더가 달라서 부딪히지 않는다. 각 런타임은 자기 판만 본다.
//
// ⚠️ 정션(mklink /J)이 아니라 디렉터리 심볼릭 링크여야 한다. Windows 에서는 개발자 모드
//    또는 관리자 권한이 필요하다.
//
// 이 스크립트는 **실물 폴더를 절대 지우지 않는다.** 전역 폴더에는 이 저장소와 무관한
// 스킬이 많이 들어 있다. 정본으로 바꿔야 할 실물이 있으면 목록으로 알려주기만 한다.

import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import crypto from 'node:crypto'
import { fileURLToPath } from 'node:url'

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const APPLY = process.argv.includes('--apply')
const REPLACE = process.argv.includes('--replace')
// 백업은 홈 아래, 스킬 폴더 **밖**에 둔다 — 안에 두면 백업본이 스킬로 딸려 들어간다.
const BACKUP = path.join(os.homedir(), '.metasci', 'replaced-skills')

const TARGETS = [
  { name: 'Claude Code', src: path.join(REPO, 'skills'), dir: path.join(os.homedir(), '.claude', 'skills') },
  { name: 'Codex', src: path.join(REPO, 'codex-skills'), dir: path.join(os.homedir(), '.codex', 'skills') },
]

// skills/<팩>/<스킬> 을 훑어 { 스킬이름: 절대경로 } 로 편다.
// 전역 폴더는 평평해서 팩 구조를 그대로 옮길 수 없다.
function collect(root) {
  const out = new Map()
  if (!fs.existsSync(root)) return out
  for (const pack of fs.readdirSync(root).sort()) {
    const packDir = path.join(root, pack)
    if (!fs.statSync(packDir).isDirectory()) continue
    for (const skill of fs.readdirSync(packDir).sort()) {
      const dir = path.join(packDir, skill)
      if (!fs.existsSync(path.join(dir, 'SKILL.md'))) continue
      if (out.has(skill)) {
        console.error(`이름 충돌: ${skill} 이 여러 팩에 있습니다 — ${out.get(skill)} / ${dir}`)
        process.exit(1)
      }
      out.set(skill, dir)
    }
  }
  return out
}

// 링크인지, 실물인지, 어디를 가리키는지
function inspect(p) {
  let st
  try {
    st = fs.lstatSync(p)
  } catch {
    return { kind: 'none' }
  }
  if (!st.isSymbolicLink()) return { kind: st.isDirectory() ? 'dir' : 'file' }
  let target = ''
  try {
    target = fs.readlinkSync(p)
  } catch {
    /* 읽을 수 없는 링크 */
  }
  let ok = false
  try {
    ok = fs.readdirSync(p).length >= 0
  } catch {
    /* 끊어진 링크 */
  }
  return { kind: ok ? 'link' : 'broken', target }
}

// 줄바꿈은 무시하고 비교한다. 같은 파일이 CRLF 로 체크아웃된 것뿐인데
// "손으로 고친 것 같다"고 경고하면 진짜 차이가 묻힌다.
const TEXTLIKE = /\.(md|ya?ml|json|txt|py|js|mjs|css|html?|svg)$/i
const sha = (p) => {
  let b = fs.readFileSync(p)
  if (TEXTLIKE.test(p)) b = Buffer.from(b.toString('utf8').replace(/\r\n/g, '\n').replace(/^﻿/, ''), 'utf8')
  return crypto.createHash('sha1').update(b).digest('hex')
}
const snap = (root) => {
  const m = new Map()
  if (!fs.existsSync(root)) return m
  ;(function w(d, rel) {
    for (const e of fs.readdirSync(d, { withFileTypes: true })) {
      const p = path.join(d, e.name)
      const r = rel ? rel + '/' + e.name : e.name
      if (e.isDirectory()) w(p, r)
      else if (e.isFile()) m.set(r, sha(p))
    }
  })(root, '')
  return m
}
const sameTree = (a, b) => a.size === b.size && [...a].every(([k, v]) => b.get(k) === v)

console.log(`정본 clone: ${REPO}`)
console.log(APPLY ? '모드: 실제 설치\n' : '모드: 미리보기 — 실제로 하려면 --apply\n')

let created = 0
const blocked = []
const replaced = []
const stamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19)

for (const t of TARGETS) {
  const skills = collect(t.src)
  console.log(`[${t.name}] ${t.dir}   ← ${path.basename(t.src)}/ (스킬 ${skills.size}개)`)
  if (APPLY) fs.mkdirSync(t.dir, { recursive: true })

  let made = 0
  let already = 0
  let repointed = 0

  for (const [name, srcDir] of skills) {
    const link = path.join(t.dir, name)
    const cur = inspect(link)

    if (cur.kind === 'link') {
      // 이미 링크다. 우리 정본을 가리키면 그대로, 아니면 바꿔 건다
      // (예전 설치는 Codex 폴더에서도 Claude 판을 가리키고 있었다).
      if (path.resolve(cur.target) === path.resolve(srcDir)) {
        already++
        continue
      }
      if (!APPLY) {
        repointed++
        console.log(`   ↻ ${name}  ${cur.target} → ${srcDir}`)
        continue
      }
      fs.rmSync(link, { recursive: true, force: true })
      fs.symlinkSync(srcDir, link, 'dir')
      repointed++
      continue
    }

    if (cur.kind === 'dir' || cur.kind === 'file') {
      const identical = cur.kind === 'dir' && sameTree(snap(link), snap(srcDir))
      if (!(APPLY && REPLACE)) {
        // 기본은 손대지 않는다. 이 폴더에는 이 저장소와 무관한 스킬이 훨씬 많다.
        blocked.push({ target: t.name, name, identical, link })
        continue
      }
      // --replace: 통째로 백업한 뒤 링크로 바꾼다. 지우기 전에 반드시 사본을 남긴다.
      const keep = path.join(BACKUP, stamp, t.name.replace(/\s+/g, '-'), name)
      fs.mkdirSync(path.dirname(keep), { recursive: true })
      fs.cpSync(link, keep, { recursive: true })
      fs.rmSync(link, { recursive: true, force: true })
      fs.symlinkSync(srcDir, link, 'dir')
      replaced.push({ target: t.name, name, identical })
      created++
      continue
    }

    if (!APPLY) {
      made++
      continue
    }
    if (cur.kind === 'broken') fs.rmSync(link, { recursive: true, force: true })
    try {
      fs.symlinkSync(srcDir, link, 'dir')
      made++
      created++
    } catch (e) {
      console.log(`   ✗ ${name}: ${e.message}`)
    }
  }

  const mine = replaced.filter((r) => r.target === t.name).length
  const bits = []
  if (made) bits.push(`${APPLY ? '새로 연결' : '연결 예정'} ${made}`)
  if (repointed) bits.push(`${APPLY ? '다시 연결' : '다시 연결 예정'} ${repointed}`)
  if (mine) bits.push(`실물 교체 ${mine}`)
  if (already) bits.push(`이미 맞음 ${already}`)
  console.log(`   ${bits.join(' · ') || '할 일 없음'}\n`)
}

if (replaced.length) {
  const changed = replaced.filter((r) => !r.identical)
  console.log(`실물 폴더 ${replaced.length}개를 링크로 바꿨습니다. 사본: ${path.join(BACKUP, stamp)}`)
  if (changed.length) {
    console.log(`   그중 ${changed.length}개는 내용이 정본과 달랐습니다 — 사라진 것이 아쉬우면 위 사본에서 꺼내세요:`)
    for (const r of changed) console.log(`      ${r.target}: ${r.name}`)
  }
  console.log()
}

if (blocked.length) {
  const same = blocked.filter((b) => b.identical)
  const diff = blocked.filter((b) => !b.identical)
  console.log(`⚠️  실물 폴더가 자리를 막고 있는 것 ${blocked.length}개 — 지우지 않았습니다\n`)
  if (same.length) {
    console.log(`   내용이 정본과 동일 ${same.length}개 (지우고 다시 돌리면 링크로 바뀝니다):`)
    for (const b of same) console.log(`      ${b.target}: ${b.name}`)
  }
  if (diff.length) {
    console.log(`   내용이 정본과 다름 ${diff.length}개 (손으로 고친 것일 수 있으니 먼저 확인하세요):`)
    for (const b of diff) console.log(`      ${b.target}: ${b.name}   ${b.link}`)
  }
  console.log()
}

console.log(APPLY ? `완료 — 링크 ${created}개 생성` : '미리보기 끝 — 실제로 하려면 --apply')
console.log(`갱신할 때: git -C "${REPO}" pull   (링크라서 이것만으로 반영됩니다)`)
