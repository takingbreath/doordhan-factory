#!/usr/bin/env node
// Stub runs of .claude/workflows/reel-script.js (loop v0.3) with fake agents: no model, no network, no files written.
// Four call shapes: free text (a link, a pasted transcript, a topic with "stance:"), which goes through a fake intake
// that writes the brief, and the old brief with a slug (object, or key: value text), which skips the intake.
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
  const slug = opts.brief.slug // for free text: the slug the fake intake will choose
  const dir = `work/${slug}/loop`
  if (!opts.freeText) files.set(`${dir}/brief.md`, `topic: ${opts.brief.topic}`)
  let intakeText = null // the raw text the intake was given, if it ran
  let sourceRead = null // the source the research task listed, if any
  const writerSaw = {} // writer label -> did reels/00-source.md exist in its reels folder when it wrote
  const exists = p => {
    if (/^https?:\/\//.test(p)) return true // a link (a source video) can't be checked offline
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
      case 'reel-0-intake': {
        // the same decisions as .claude/agents/reel-0-intake.md, by rule: a link, a long pasted text, or a topic line
        const m = /=== TEXT START ===\n([\s\S]*)\n=== TEXT END ===/.exec(prompt)
        intakeText = m ? m[1] : null
        const text = intakeText || ''
        const kv = {}
        const plain = text.replace(/\b(stance|writers|cast|format)\s*:\s*(.*?)(?=\s+\b(?:stance|writers|cast|format)\s*:|$)/gim,
          (_, k, v) => { kv[k.toLowerCase()] = v.trim(); return '' }).trim()
        const link = (/(https?:\/\/(?:www\.)?(?:youtube\.com\/(?:watch\?v=|shorts\/)|youtu\.be\/|instagram\.com\/(?:reels?|p)\/)\S+)/.exec(plain) || [])[1]
        const words = plain.split(/\s+/).filter(Boolean)
        const pasted = !link && words.length >= 60
        const rest = link ? plain.replace(link, '').trim() : plain
        const topic = link ? (rest || 'Stub video title') : pasted ? 'Stub question the transcript answers' : rest
        const kebab = topic.toLowerCase().replace(/[^a-z0-9 ]+/g, ' ').split(/\s+/).filter(Boolean).slice(0, 5).join('-')
        let sl = `${kebab}-20261004`, k = 2
        while ([...files.keys()].some(f => f.startsWith(`work/${sl}/`))) sl = `${kebab}-20261004-${k++}`
        const source = link || (pasted ? `work/${sl}/source.md` : '')
        if (pasted) put(`work/${sl}/source.md`, `# Source pasted into /reel-script\n\n${text}`)
        put(`work/${sl}/loop/brief.md`, `# Brief: ${sl}\n- **Topic:** ${topic}\n- **Stance:** ${kv.stance || 'none'}`)
        return { slug: sl, topic, format: kv.format || 'sahayata_kendra', cast: ['pandey', 'caller', 'billu'],
          stance: kv.stance || '', writers: kv.writers ? Number(kv.writers) : 3, source, note: '' }
      }
      case 'reel-1-research':
      {
        put(W('Handoff')); put(W('Working file'), '## Missing\n- None'); put(W('Python file'))
        const srcIn = t.reads.find(x => x.label.startsWith('Source video to adapt'))
        if (srcIn) { sourceRead = srcIn.path; put(`${W('Reels folder')}00-source.md`, 'SOURCE: the video the brief asks to adapt') }
        const n = srcIn ? 4 : 6 // with a source: three to five other reels
        for (let i = 1; i <= n; i++) put(`${W('Reels folder')}0${i}-reel.md`)
        return `wrote s1-research.md, s1-working.md, s1-math.py, reels/ (${srcIn ? 'the source and ' : ''}${n} reels); vidIQ 40 credits`
      }
      case 'reel-2-writer':
        if (R("The judge's note")) {
          const pick = /\((w\d+-\d), the pick/.exec(t.reads.find(x => x.label.startsWith('Your script') && x.label.includes('the pick')).label)[1]
          const answer = (opts.replies || {})[pick] || 'KEEP'
          if (answer === 'REVISED') put(W('Revised script'))
          put(W('Your note'), files.get(W('Your note')) + '\n## Reply to the judge')
          return `${answer}\nbecause`
        }
        writerSaw[o.label] = files.has(`${R('Reels folder')}00-source.md`)
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
    result = await workflowBody(agent, parallel, pipeline, m => logs.push(m), () => {}, opts.args || opts.brief,
      { total: null, spent: () => 0, remaining: () => Infinity }, () => { throw new Error('no nested workflows') })
  } catch (e) { error = e.message }
  const list = [...files.keys()].filter(k => k.startsWith(dir + '/')).map(k => k.slice(dir.length + 1)).sort()
  const briefText = files.get(`${dir}/brief.md`) || ''
  return { name, result, error, missing, logs, calls, list, sourceRead, writerSaw, intakeText, briefText,
    allFiles: [...files.keys()] }
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
  { name: 'extra e. a brief with a source line: research saves reels/00-source.md, every writer reads it',
    brief: { slug: 'stub-source', topic: 'How much SIP is enough to retire?' },
    args: 'slug: stub-source\ntopic: How much SIP is enough to retire?\nformat: sahayata_kendra\ncast: pandey, caller, billu\n' +
      'source: https://www.youtube.com/watch?v=STUB0000001',
    picks: ['w1-1', 'w2-1', 'w3-1'],
    expect: { scripts: 6, picks: ['w1-1', 'w2-1', 'w3-1'], retells: 9, cuts: 3,
      source: 'https://www.youtube.com/watch?v=STUB0000001', writers: ['Writer 1', 'Writer 2', 'Writer 3'] } },
  { name: 'free a. a YouTube link: the intake writes the brief, research saves reels/00-source.md, every writer reads it',
    freeText: true, brief: { slug: 'stub-video-title-20261004', topic: 'Stub video title' },
    args: 'https://www.youtube.com/watch?v=STUB0000002',
    picks: ['w1-1', 'w2-1', 'w3-1'],
    expect: { scripts: 6, picks: ['w1-1', 'w2-1', 'w3-1'], retells: 9, cuts: 3, intake: true, topic: 'Stub video title',
      source: 'https://www.youtube.com/watch?v=STUB0000002', writers: ['Writer 1', 'Writer 2', 'Writer 3'] } },
  { name: 'free b. a pasted transcript: saved as work/<slug>/source.md, which research turns into reels/00-source.md',
    freeText: true, brief: { slug: 'stub-question-the-transcript-answers-20261004', topic: 'Stub question the transcript answers' },
    args: "Dekho bhai, sab log bolte hain SIP karo, crorepati ban jaoge. Par sawaal yeh hai ki kitna? Maan lo tumhara kharcha aaj pachaas hazaar mahina hai. Tees saal baad mehangai ke saath wahi kharcha teen lakh ke aas paas hoga. Retirement ke baad bhi tees saal chalana hai, toh tumko lagbhag das crore chahiye. Baarah percent maan ke, aaj se SIP shuru karo toh mahina chauntees hazaar ke kareeb lagega. Paanch saal ruk gaye toh saath hazaar. Isi liye jaldi shuru karna zaroori hai, aur apna number apne kharche se nikalo, kisi aur ke crore se nahi.",
    picks: ['w1-1', 'w2-1', 'w3-1'],
    expect: { scripts: 6, picks: ['w1-1', 'w2-1', 'w3-1'], retells: 9, cuts: 3, intake: true,
      topic: 'Stub question the transcript answers', source: 'work/stub-question-the-transcript-answers-20261004/source.md',
      sourceFile: true, writers: ['Writer 1', 'Writer 2', 'Writer 3'] } },
  { name: 'free c. a topic with "stance:" and "writers: 2": the intake, no source, the stance in the brief',
    freeText: true, brief: { slug: 'how-much-sip-is-enough-20261004', topic: 'How much SIP is enough to retire?' },
    args: "How much SIP is enough to retire? stance: start from the caller's own monthly spending writers: 2",
    picks: ['w1-1', 'w2-2', 'w1-2'],
    expect: { scripts: 4, picks: ['w1-1', 'w2-2', 'w1-2'], retells: 9, cuts: 3, intake: true,
      topic: 'How much SIP is enough to retire?', stance: "start from the caller's own monthly spending" } },
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
    const first = r.logs[0] || ''   // the first log line names the slug, the topic and the source
    if (!first.includes(`Slug: ${sc.brief.slug} `) || !first.includes(`Source: ${e.source || 'none'} `)) problems.push(`first log line lacks the slug or the source: ${first}`)
    if (e.topic && !first.includes(`Topic: ${e.topic} `)) problems.push(`first log line lacks the topic: ${first}`)
    if (e.intake) {
      if (r.intakeText !== sc.args.trim()) problems.push(`the intake was not given the text as typed (got ${JSON.stringify(r.intakeText)})`)
      if (!r.list.includes('brief.md')) problems.push('the intake wrote no brief.md')
      if (!r.result || r.result.slug !== sc.brief.slug || r.result.topic !== e.topic || !r.result.intake) problems.push(`result slug/topic/intake: ${r.result && [r.result.slug, r.result.topic, r.result.intake]}`)
      if (e.stance && !r.briefText.includes(e.stance)) problems.push('the stance is not in the brief')
    } else if (r.intakeText !== null || (r.result && r.result.intake)) problems.push('the intake ran for a brief that already had a slug')
    if (e.source) {
      if (r.sourceRead !== e.source) problems.push(`research was given source ${r.sourceRead}, expected ${e.source}`)
      if (e.sourceFile && !r.allFiles.includes(e.source)) problems.push(`no ${e.source}`)
      if (!r.list.includes('reels/00-source.md')) problems.push('no reels/00-source.md')
      for (const w of e.writers) if (!r.writerSaw[w]) problems.push(`${w} ran without reels/00-source.md in its reels folder`)
    } else if (r.sourceRead || r.list.includes('reels/00-source.md')) problems.push('a source appeared in a run whose brief has none')
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
