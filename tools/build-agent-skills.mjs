// skills/ (Claude 정본) → 런타임별 스킬 세트 생성기.
//
//   node tools/build-agent-skills.mjs           생성
//   node tools/build-agent-skills.mjs --check   커밋된 결과물이 최신인지만 확인 (CI용)
//
// 왜 생성인가 —
// 손으로 갈라놓은 판(meta-proofreading-codex)을 원본과 대조해보니, 달라진 파일 18개 중
// 런타임 때문에 달라야 했던 것은 2개뿐이었다. 나머지 16개는 그냥 낡은 것이었고
// 판정자(agent_j)와 매뉴얼 한 챕터가 통째로 빠져 있었다. 정본을 하나로 두고 기계가
// 옮기면 그 일이 구조적으로 일어나지 않는다.
//
// 런타임에 따라 진짜 달라야 하는 부분은 agent-overrides/<프로파일>/ 로 지정한다:
//   agent-overrides/<프로파일>/<skill>/<파일>.replace.json  → [{from,to}] 부분 치환 (권장)
//   agent-overrides/<프로파일>/<skill>/<파일>               → 파일 통째로 교체
// .replace.json 의 from 이 더 이상 안 맞으면 **빌드를 실패시킨다**. 정본이 바뀌었는데
// 오버라이드가 낡은 채로 조용히 남는 것이 드리프트의 시작이기 때문이다.

import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const SRC = path.join(ROOT, 'skills')
const OVR = path.join(ROOT, 'agent-overrides')
const CHECK = process.argv.includes('--check')

// 각 런타임의 대응 도구는 실물에서 확인한 것이다:
//   Codex CLI 0.145.0  spawn_agent           (codex exec · mcp-server 양쪽에서 확인)
//   Hermes             delegation · clarify  (hermes tools list 의 toolset 이름)
const PROFILES = [
  {
    name: 'codex',
    out: 'codex-skills',
    runtime: 'Codex CLI',
    openaiYaml: true, // Codex 는 agents/openai.yaml 로 스킬을 목록에 띄운다
    subs: [
      [/one \*\*Agent tool\*\* call per reviewer/g, 'one **`spawn_agent`** call per reviewer'],
      [/\bRead, Glob, Grep, WebSearch, WebFetch, Agent, AskUserQuestion\b/g,
       'file reading, shell commands, web search, HTTP fetch, `spawn_agent`'],
      [/\bAgent tool\b/g, '`spawn_agent`'],
      [/\bTask tool\b/g, '`spawn_agent`'],
      [/\bWebSearch tool\b/g, 'web search'],
      [/\bWebFetch tool\b/g, 'HTTP fetch'],
      [/\bWebSearch\b/g, 'web search'],
      [/\bWebFetch\b/g, 'HTTP fetch'],
      [/\bClaude Code\b/g, 'Codex CLI'],
    ],
    notes: [
      {
        when: /\bAskUserQuestion\b/,
        line:
          '> - `AskUserQuestion` does not exist here. Where the skill calls for it, put the\n' +
          '>   choices in your message as a numbered list and wait for the user to reply\n' +
          '>   with a number. Keep the same choices — do not collapse them into prose.',
      },
      {
        when: /spawn_agent/,
        line:
          '> - Reviewer/agent fan-out uses `spawn_agent`. Keep the number of roles the skill\n' +
          '>   asks for; if you cannot run them in parallel, run them in sequence.',
      },
    ],
  },
  {
    name: 'hermes',
    out: 'hermes-skills',
    runtime: 'Hermes',
    openaiYaml: false, // Hermes 는 SKILL.md 만 읽는다
    subs: [
      [/one \*\*Agent tool\*\* call per reviewer/g, 'one **`delegation`** call per reviewer'],
      [/\bRead, Glob, Grep, WebSearch, WebFetch, Agent, AskUserQuestion\b/g,
       'the `file`, `terminal`, `web`, `delegation`, and `clarify` toolsets'],
      [/\bAgent tool\b/g, 'the `delegation` toolset'],
      [/\bTask tool\b/g, 'the `delegation` toolset'],
      [/\bWebSearch tool\b/g, 'the `web` toolset'],
      [/\bWebFetch tool\b/g, 'the `web` toolset'],
      [/\bWebSearch\b/g, 'web search'],
      [/\bWebFetch\b/g, 'web fetch'],
      [/\bClaude Code\b/g, 'Hermes'],
    ],
    notes: [
      {
        // Codex 와 달리 Hermes 에는 대응 도구가 실제로 있다.
        when: /\bAskUserQuestion\b/,
        line:
          '> - `AskUserQuestion` is Claude Code\'s name for it. Use the `clarify` toolset —\n' +
          '>   it does the same job. Keep the same choices.',
      },
      {
        when: /delegation/,
        line:
          '> - Reviewer/agent fan-out uses the `delegation` toolset. Keep the number of roles\n' +
          '>   the skill asks for; if you cannot run them in parallel, run them in sequence.',
      },
    ],
  },
]

// AskUserQuestion 은 어느 프로파일에서도 인라인 치환하지 않는다. 원문에서 고유명사로 쓰여서
// 명사구로 바꾸면 문장이 깨진다 — "offered as a numbered decision prompt options".
// 이름은 그대로 두고 SKILL.md 앞머리에서 한 번 설명한다.

const walk = (dir, rel = '') => {
  const out = []
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const r = rel ? rel + '/' + e.name : e.name
    if (e.isDirectory()) out.push(...walk(path.join(dir, e.name), r))
    else out.push(r)
  }
  return out
}

// frontmatter 에서 allowed-tools 를 뺀다 — Claude Code 전용 키라 다른 런타임에는 뜻이 없다.
function stripAllowedTools(text) {
  const m = /^(---\r?\n)([\s\S]*?)(\r?\n---\r?\n?)/.exec(text)
  if (!m) return text
  const body = m[2].split('\n').filter((l) => !/^allowed-tools\s*:/i.test(l)).join('\n')
  return m[1] + body + m[3] + text.slice(m[0].length)
}

function frontmatterField(text, key) {
  const m = /^---\r?\n([\s\S]*?)\r?\n---/.exec(text)
  if (!m) return ''
  const re = new RegExp(`^${key}\\s*:\\s*(.*)$`, 'im')
  const hit = re.exec(m[1])
  if (!hit) return ''
  let v = hit[1].trim()
  if (v === '|' || v === '>' || v === '>-' || v === '|-') {
    const lines = m[1].split('\n')
    const at = lines.findIndex((l) => re.test(l))
    const rest = []
    for (const l of lines.slice(at + 1)) {
      if (/^\s+\S/.test(l)) rest.push(l.trim())
      else break
    }
    v = rest.join(' ')
  }
  return v.replace(/^["']|["']$/g, '')
}

const titleCase = (n) => n.replace(/[-_]+/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())

function makeOpenAiYaml(name, text) {
  const desc = frontmatterField(text, 'description')
  const first = (desc.split(/(?<=\.)\s|\. /)[0] || desc).trim().replace(/"/g, "'").slice(0, 160)
  return (
    'interface:\n' +
    `  display_name: "${titleCase(name)}"\n` +
    `  short_description: "${first || titleCase(name)}"\n` +
    `  default_prompt: "Use $${name} for this task."\n`
  )
}

// SKILL.md frontmatter 바로 뒤에 런타임 주석을 끼운다. 해당 사항이 없으면 넣지 않는다.
// 판단은 **스킬 전체**(references/ 포함)를 보고 한다 — 에이전트가 실제로 부딪히는 것은
// SKILL.md 가 읽으라고 시킨 참조 파일 안의 지시이기 때문이다.
function addRuntimeNotes(profile, text, skillText) {
  const lines = profile.notes.filter((r) => r.when.test(skillText)).map((r) => r.line)
  if (!lines.length) return text
  const block =
    '> **' + profile.runtime + ' runtime notes** — generated by `tools/build-agent-skills.mjs`.\n' +
    '> This skill is written for Claude Code; the differences that matter here:\n' +
    lines.join('\n') +
    '\n\n'
  const m = /^(---\r?\n[\s\S]*?\r?\n---\r?\n)/.exec(text)
  return m ? m[1] + '\n' + block + text.slice(m[1].length).replace(/^\r?\n/, '') : block + text
}

function applyOverrides(profile, skill, rel, text) {
  const base = path.join(OVR, profile.name, skill)
  const patch = path.join(base, rel + '.replace.json')
  if (fs.existsSync(patch)) {
    for (const { from, to } of JSON.parse(fs.readFileSync(patch, 'utf8'))) {
      const n = text.split(from).length - 1
      if (n !== 1) {
        throw new Error(
          `오버라이드가 정본과 어긋납니다: agent-overrides/${profile.name}/${skill}/${rel}.replace.json\n` +
            `  찾는 문구가 ${n}번 나옵니다 (1번이어야 함): ${JSON.stringify(from.slice(0, 60))}…\n` +
            `  정본이 바뀌었으면 오버라이드도 고치세요.`
        )
      }
      text = text.replace(from, to)
    }
  }
  const whole = path.join(base, rel)
  if (fs.existsSync(whole) && fs.statSync(whole).isFile()) return fs.readFileSync(whole, 'utf8')
  return text
}

const TEXT = /\.(md|ya?ml|json|txt|py)$/i

process.on('uncaughtException', (e) => {
  console.error('\n' + e.message)
  process.exit(1)
})

function buildProfile(profile) {
  const generated = new Map()
  for (const pack of fs.readdirSync(SRC).sort()) {
    const packDir = path.join(SRC, pack)
    if (!fs.statSync(packDir).isDirectory()) continue
    for (const skill of fs.readdirSync(packDir).sort()) {
      const skillDir = path.join(packDir, skill)
      if (!fs.statSync(skillDir).isDirectory()) continue
      if (!fs.existsSync(path.join(skillDir, 'SKILL.md'))) continue

      const rels = walk(skillDir)
      const skillText = rels
        .filter((r) => TEXT.test(r))
        .map((r) => {
          let t = fs.readFileSync(path.join(skillDir, r), 'utf8')
          for (const [re, to] of profile.subs) t = t.replace(re, to)
          return t
        })
        .join('\n')

      let sawOpenAi = false
      for (const rel of rels) {
        const abs = path.join(skillDir, rel)
        const dest = `${pack}/${skill}/${rel}`
        if (rel === 'agents/openai.yaml') {
          sawOpenAi = true
          if (!profile.openaiYaml) continue // 이 런타임은 안 쓴다
        }
        if (!TEXT.test(rel)) {
          generated.set(dest, fs.readFileSync(abs))
          continue
        }
        let text = fs.readFileSync(abs, 'utf8')
        for (const [re, to] of profile.subs) text = text.replace(re, to)
        if (rel === 'SKILL.md') text = addRuntimeNotes(profile, stripAllowedTools(text), skillText)
        text = applyOverrides(profile, skill, rel, text)
        generated.set(dest, Buffer.from(text, 'utf8'))
      }
      if (profile.openaiYaml && !sawOpenAi) {
        const skillMd = fs.readFileSync(path.join(skillDir, 'SKILL.md'), 'utf8')
        const yaml = applyOverrides(profile, skill, 'agents/openai.yaml', makeOpenAiYaml(skill, skillMd))
        generated.set(`${pack}/${skill}/agents/openai.yaml`, Buffer.from(yaml, 'utf8'))
      }
    }
  }
  generated.set('README.md', Buffer.from(readmeFor(profile), 'utf8'))
  return generated
}

function readmeFor(p) {
  const rows = p.subs
    .filter(([re]) => !/one \*\*Agent tool\*\*|Read, Glob, Grep/.test(re.source))
    .map(([re, to]) => `| \`${re.source.replace(/\\b|\\/g, '')}\` | ${to} |`)
    .join('\n')
  return (
    `# ${p.out}\n\n` +
    `**Generated — do not edit by hand.** Every file here comes from \`skills/\` via\n` +
    `\`node tools/build-agent-skills.mjs\`. Edit the skill in \`skills/\`, then rebuild.\n\n` +
    `Claude Code reads \`skills/\`; ${p.runtime} reads this. They stay in step because only\n` +
    `one of them is written by a person.\n\n` +
    `## What the build changes\n\n| in \`skills/\` | here |\n|---|---|\n${rows}\n` +
    `| \`allowed-tools:\` frontmatter | removed (Claude-only key) |\n` +
    (p.openaiYaml ? `| no \`agents/openai.yaml\` | one is generated |\n` : `| \`agents/openai.yaml\` | dropped (Codex-only) |\n`) +
    `\n\`AskUserQuestion\` is **not** substituted. It reads as a proper noun in the source, so\n` +
    `swapping in a noun phrase breaks the sentences around it. Instead each SKILL.md that\n` +
    `needs one gets a short "${p.runtime} runtime notes" block after its frontmatter.\n\n` +
    `## Real runtime differences\n\n` +
    `Anything the table above cannot express goes in \`agent-overrides/${p.name}/<skill>/\`:\n\n` +
    `- \`<file>.replace.json\` — \`[{"from": "...", "to": "..."}]\`, applied to that file.\n` +
    `  Each \`from\` must match **exactly once** or the build fails, so an override cannot\n` +
    `  rot silently when the source changes.\n` +
    `- \`<file>\` — replaces the file outright. Use sparingly; a whole-file override is a\n` +
    `  fork by another name.\n`
  )
}

let totalChanged = 0
const staleAll = []

for (const profile of PROFILES) {
  const OUT = path.join(ROOT, profile.out)
  const generated = buildProfile(profile)
  const existing = fs.existsSync(OUT) ? new Set(walk(OUT)) : new Set()
  let changed = 0

  for (const [rel, buf] of generated) {
    const dest = path.join(OUT, rel)
    const same = fs.existsSync(dest) && fs.readFileSync(dest).equals(buf)
    if (!same) {
      changed++
      if (CHECK) staleAll.push(`${profile.out}/${rel}`)
      else {
        fs.mkdirSync(path.dirname(dest), { recursive: true })
        fs.writeFileSync(dest, buf)
      }
    }
    existing.delete(rel)
  }
  for (const orphan of existing) {
    changed++
    if (CHECK) staleAll.push(`${profile.out}/${orphan} (정본에 없음)`)
    else fs.rmSync(path.join(OUT, orphan))
  }

  const skills = new Set([...generated.keys()].filter((k) => k.split('/').length > 2).map((k) => k.split('/').slice(0, 2).join('/')))
  totalChanged += changed
  if (!CHECK) console.log(`${profile.out.padEnd(14)} 스킬 ${skills.size}개 / 파일 ${generated.size}개 (변경 ${changed}개)`)
  else if (!changed) console.log(`${profile.out.padEnd(14)} 최신 — 스킬 ${skills.size}개 / 파일 ${generated.size}개`)
}

if (CHECK && totalChanged) {
  console.error(`\n생성물이 낡았습니다 — ${totalChanged}개 파일:`)
  staleAll.slice(0, 20).forEach((s) => console.error('  ' + s))
  if (staleAll.length > 20) console.error(`  … 외 ${staleAll.length - 20}개`)
  console.error('node tools/build-agent-skills.mjs 를 돌리고 커밋하세요.')
  process.exit(1)
}
