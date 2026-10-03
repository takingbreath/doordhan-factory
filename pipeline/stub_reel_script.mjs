#!/usr/bin/env node
// Stub runs of .claude/workflows/reel-script.js (loop v0.3) with fake agents: no model, no network, no files written.
// Each fake agent checks that every path under "Read" in its task exists (a file an earlier agent wrote, or a house
// file in the repository) and "writes" its "Write" paths into an in-memory run folder. A scenario passes when the run
// ends, every read was there (voice cards for cast members with no voice folder are expected missing), and the run
// folder holds exactly the files the scenario expects.
// Usage: node pipeline/stub_reel_script.mjs [--quiet]     exit 0 when every scenario passes
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const QUIET = process.argv.includes('--quiet')
const src = fs.readFileSync(path.join(ROOT, '.claude/workflows/reel-script.js'), 'utf8')
  .replace(/^export const meta\s*=/m, 'const meta =')
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor
const workflowBody = new AsyncFunction('agent', 'parallel', 'pipeline', 'log', 'phase', 'args', 'budget', 'workflow', src)

function parseTask(prompt) {
  const out = { reads: [], writes: [] }
  let list = null
  for (const line of String(prompt).split('\n')) {
    if (line === 'Read:') list = out.reads
    else if (line === 'Write:') list = out.writes
    else if (line.startsWith('- ') && list) {
      const i = line.lastIndexOf(': ')
      list.push({ label: line.slice(2, i), path: line.slice(i + 2) })
    }
  }
  return out
}

async function runScenario(name, opts) {
  const files = new Map() // path -> content, for everything under work/
  const missing = [] // reads that were not there
  const logs = []
  const calls = []
  const slug = opts.brief.slug
  const dir = `work/${slug}/loop`
  files.set(`${dir}/brief.md`, `topic: ${opts.brief.topic}`)
  const exists = p => {
    if (p.startsWith('work/')) return p.endsWith('/') ? [...files.keys()].some(k => k.startsWith(p)) : files.has(p)
    return fs.existsSync(path.join(ROOT, p))
  }
  const put = (p, text) => files.set(p, text || 'stub')

  async function agent(prompt, o) {
    const t = parseTask(prompt)
    calls.push(o.label)
    if (opts.dies && opts.dies === o.label) return null
    for (const r of t.reads) {
      if (!exists(r.path) && !/^docs\/voices\/(caller|billu)\//.test(r.path)) missing.push(`${o.label} read ${r.path} (${r.label})`)
    }
    const W = label => (t.writes.find(x => x.label.startsWith(label)) || {}).path
    const R = label => (t.reads.find(x => x.label.startsWith(label)) || {}).path
    switch (o.agentType) {
      case 'reel-1-research':
        put(W('Handoff')); put(W('Working file'), '## Missing\n- None'); put(W('Python file'))
        for (let i = 1; i <= 6; i++) put(`${W('Reels folder')}0${i}-reel.md`)
        return 'wrote s1-research.md, s1-working.md, s1-math.py, reels/ (6 reels); vidIQ 40 credits'
      case 'reel-2-writer':
        if (R("The judge's note")) {
          const pick = /\((w\d+-\d), the pick/.exec(t.reads.find(x => x.label.startsWith('Your script') && x.label.includes('the pick')).label)[1]
          const answer = (opts.replies || {})[pick] || 'KEEP'
          if (answer === 'REVISED') put(W('Revised script'))
          put(W('Your note'), files.get(W('Your note')) + '\n## Reply to the judge')
          return `${answer}\nbecause`
        }
        put(W('Your note'), '## Missing\n- None'); put(W('Script 1')); put(W('Script 2'))
        return 'wrote the note and two scripts'
      case 'reel-lint': {
        const script = R('Script')
        put(script.replace(/\.md$/, '-lint-fails.md')); put(script.replace(/\.md$/, '-lint-report.md'))
        return 'VERDICT: FAIL'
      }
      case 'reel-4-judge': {
        put(W('Picks file')); put(W('Working file'), '## Missing\n- None')
        const picks = opts.picks.map(s => ({ script: s, note: (opts.notes || []).includes(s) }))
        for (const p of picks) if (p.note) put(W('Note to a pick').replace('<script>', p.script))
        return { picks }
      }
      case 'reel-4c-recall':
        put(W('Your retell'))
        return W('Your retell')
      case 'reel-7-performance':
        for (const x of t.writes.filter(x => x.label.startsWith('Audio folder for '))) {
          const stem = x.label.slice('Audio folder for '.length)
          put(`${x.path}${stem}_voice_cut.mp3`); put(`${x.path}report.md`); put(`${x.path}lines.json`)
        }
        put(W('Voice notes')); put(W('Working file'), '## Missing\n- docs/voices/caller/voice-card.md')
        return 'cuts made'
      case 'reel-8-handoff':
        put(W('Hand-off')); put(W('Working file'), '## Missing\n- None')
        return 'wrote s8-handoff.md, s8-working.md'
      default:
        throw new Error(`unexpected agent type ${o.agentType}`)
    }
  }
  const parallel = thunks => Promise.all(thunks.map(async th => { try { return await th() } catch (e) { return null } }))
  const pipeline = (items, ...stages) => Promise.all(items.map(async (item, i) => {
    let v = item
    try { for (const s of stages) v = await s(v, item, i) } catch (e) { return null }
    return v
  }))
  let result, error = null
  try {
    result = await workflowBody(agent, parallel, pipeline, m => logs.push(m), () => {}, opts.brief,
      { total: null, spent: () => 0, remaining: () => Infinity }, () => { throw new Error('no nested workflows') })
  } catch (e) { error = e.message }
  const list = [...files.keys()].filter(k => k.startsWith(dir + '/')).map(k => k.slice(dir.length + 1)).sort()
  return { name, result, error, missing, logs, calls, list }
}

const SC = [
  { name: '1. clean run: 3 writers, 6 scripts, 3 picks, 9 retells, 3 cuts',
    brief: { slug: 'stub-clean', topic: 'Who decides the rupee-dollar rate?', format: 'sahayata_kendra', cast: 'pandey, caller, billu' },
    picks: ['w1-1', 'w2-2', 'w3-1'],
    expect: { scripts: 6, picks: ['w1-1', 'w2-2', 'w3-1'], retells: 9, cuts: 3 } },
  { name: '2. a note on one pick; the writer answers OTHER',
    brief: { slug: 'stub-other', topic: 'Who decides the rupee-dollar rate?', format: 'sahayata_kendra', cast: 'pandey, caller, billu' },
    picks: ['w1-1', 'w2-1', 'w3-2'], notes: ['w2-1'], replies: { 'w2-1': 'OTHER' },
    expect: { scripts: 6, picks: ['w1-1', 'w2-2', 'w3-2'], retells: 9, cuts: 3 } },
  { name: '3. writers: 1',
    brief: { slug: 'stub-one', topic: 'Who decides the rupee-dollar rate?', format: 'sahayata_kendra', cast: 'pandey, caller, billu', writers: 1 },
    picks: ['w1-2', 'w1-1'],
    expect: { scripts: 2, picks: ['w1-2', 'w1-1'], retells: 6, cuts: 2 } },
  { name: 'extra a. a note answered REVISED (the revision is linted)',
    brief: { slug: 'stub-revised', topic: 'x', format: 'sahayata_kendra', cast: 'pandey, caller, billu' },
    picks: ['w1-1', 'w2-1', 'w3-1'], notes: ['w3-1'], replies: { 'w3-1': 'REVISED' },
    expect: { scripts: 6, picks: ['w1-1', 'w2-1', 'w3-1r'], retells: 9, cuts: 3 } },
  { name: 'extra b. OTHER refused when the other draft is already a pick',
    brief: { slug: 'stub-refused', topic: 'x', format: 'sahayata_kendra', cast: 'pandey, caller, billu', writers: 1 },
    picks: ['w1-1', 'w1-2'], notes: ['w1-1'], replies: { 'w1-1': 'OTHER' },
    expect: { scripts: 2, picks: ['w1-1', 'w1-2'], retells: 6, cuts: 2 } },
  { name: 'extra c. a reader that dies stops the run with its name',
    brief: { slug: 'stub-dies', topic: 'x', format: 'sahayata_kendra', cast: 'pandey, caller, billu' },
    picks: ['w1-1', 'w2-1', 'w3-1'], dies: 'Reader 2 · w2-1',
    expectError: /Reader 2 · w2-1 did not finish/ },
  { name: 'extra d. a brief with a phase is refused',
    brief: { slug: 'stub-phase', topic: 'x', format: 'sahayata_kendra', cast: 'pandey', phase: 'blueprint' },
    picks: [], expectError: /has none/ },
]

let bad = 0
for (const sc of SC) {
  const r = await runScenario(sc.name, sc)
  const problems = []
  if (sc.expectError) {
    if (!r.error || !sc.expectError.test(r.error)) problems.push(`expected an error matching ${sc.expectError}, got ${r.error || 'none'}`)
  } else {
    if (r.error) problems.push(`error: ${r.error}`)
    const e = sc.expect
    const scripts = r.list.filter(f => /^w\d+-\d\.md$/.test(f))
    const retells = r.list.filter(f => /^r-.*-\d\.md$/.test(f))
    const cuts = r.list.filter(f => /_voice_cut\.mp3$/.test(f))
    const finals = r.result ? r.result.picks.map(p => p.final) : []
    if (scripts.length !== e.scripts) problems.push(`${scripts.length} scripts, expected ${e.scripts}`)
    if (JSON.stringify(finals) !== JSON.stringify(e.picks)) problems.push(`final picks ${finals}, expected ${e.picks}`)
    if (retells.length !== e.retells) problems.push(`${retells.length} retells, expected ${e.retells}`)
    if (cuts.length !== e.cuts) problems.push(`${cuts.length} cuts, expected ${e.cuts}`)
    for (const f of e.picks) {
      if (!r.list.includes(`${f}-lint-report.md`)) problems.push(`no lint report for ${f}`)
      for (let k = 1; k <= 3; k++) if (!r.list.includes(`r-${f}-${k}.md`)) problems.push(`no retell ${k} for ${f}`)
    }
    for (const f of ['s1-research.md', 's1-working.md', 's1-math.py', 's4-picks.md', 's4-working.md', 'audio/voice-notes.md', 's7-working.md', 's8-handoff.md', 's8-working.md']) {
      if (!r.list.includes(f)) problems.push(`no ${f}`)
    }
  }
  problems.push(...r.missing.map(m => `missing read: ${m}`))
  if (problems.length) bad += 1
  console.log(`${problems.length ? 'FAIL' : 'PASS'}  ${sc.name}`)
  if (!QUIET || problems.length) {
    if (r.result) console.log(`      result picks: ${r.result.picks.map(p => `${p.pick}${p.note ? ` (note: ${p.answer})` : ''} -> ${p.final}`).join(', ')}; agents ${r.result.agents}`)
    if (r.error) console.log(`      stopped: ${r.error}`)
    for (const l of r.logs) console.log(`      log: ${l.split('\n')[0]}`)
    if (!sc.expectError && !QUIET) console.log(`      files (${r.list.length}): ${r.list.join('  ')}`)
    for (const p of problems) console.log(`      ! ${p}`)
  }
}
console.log(bad ? `${bad} scenario(s) FAILED` : 'ALL STUB RUNS PASS')
process.exit(bad ? 1 : 0)
