export const meta = {
  name: 'reel-script',
  description: 'Run the reel script loop from prompts/script-writer.md: one named subagent per stage, each given only file paths, at most two rewrites, then the performance pass and the hand-off.',
  whenToUse: 'When a reel needs a script from a finished research file. Takes a brief: slug, topic, format, cast, research (the research file path) and an optional stance. A workflow script cannot write files, so save the brief as work/<slug>/loop/brief.md before launching: Stage 1 reads the topic and any stance from that file.',
  phases: [
    { title: 'Stage 1 · Research read', detail: 'facts, the crowd, TAKE_POSSIBLE or NO_TAKE' },
    { title: 'Stage 2 · Stance and beats', detail: 'locks the stance' },
    { title: 'Stage 3 · Writer', detail: 'first draft, without the research' },
    { title: 'Stages 4–5 · Critics', detail: 'swap test, speech critique, stance and facts' },
    { title: 'Stage 6 · Rewrite', detail: 'at most twice' },
    { title: 'Stage 7 · Performance pass', detail: 'delivery tags and the lines file' },
    { title: 'Stage 8 · Hand-off', detail: 'the script message for the human' },
  ],
}

// The spec is prompts/script-writer.md. Each stage is its own agent (.claude/agents/reel-*.md) with fresh context.
// An agent's task is two lists of labelled paths and nothing else: the inputs the spec lists for that stage, and
// where to write. What a stage is not given is as much a part of the design as what it is: the writer never sees
// the research, and the critics never see the research, the beats or the writer's notes.

const MAX_REWRITES = 2 // spec, "Loop control": more rounds make scripts worse

// ---------------------------------------------------------------- the brief
function fromText(text) {
  const t = text.trim()
  try {
    const j = JSON.parse(t)
    if (j && typeof j === 'object' && !Array.isArray(j)) return j
  } catch (e) { /* not JSON: read it as "key: value" pairs */ }
  const key = /\b(slug|topic|format|cast|research(?:[ _-]?file)?(?:[ _-]?path)?|stance)\s*[:=]\s*/gi
  const hits = []
  let m
  while ((m = key.exec(t)) !== null) hits.push({ name: m[1].toLowerCase(), start: m.index, end: key.lastIndex })
  const out = {}
  hits.forEach((h, i) => {
    const raw = t.slice(h.end, i + 1 < hits.length ? hits[i + 1].start : t.length)
    const value = raw.trim().replace(/[;,]\s*$/, '').trim().replace(/^["'“](.*)["'”]$/s, '$1')
    out[h.name.startsWith('research') ? 'research' : h.name] = value
  })
  return out
}

function readBrief(input) {
  const b = typeof input === 'string' ? fromText(input) : input
  if (!b || typeof b !== 'object' || Array.isArray(b)) {
    throw new Error('reel-script needs a brief: slug, topic, format, cast, research (file path) and an optional stance.')
  }
  const text = v => (typeof v === 'string' ? v.trim() : '')
  const slug = text(b.slug)
  const format = text(b.format).replace(/^formats\//, '').replace(/\.md$/, '')
  const research = text(b.research || b.research_file || b.researchFile || b.research_path || b.researchPath)
  const cast = (Array.isArray(b.cast) ? b.cast : text(b.cast).split(/[,\n]|\band\b/))
    .map(n => String(n).trim().toLowerCase()).filter(Boolean)
  const name = /^[a-z0-9][a-z0-9_-]*$/i
  const problems = []
  if (!name.test(slug)) problems.push('slug (letters, digits, - and _ only)')
  if (!name.test(format)) problems.push('format (the file name under formats/, without .md)')
  if (!cast.length || !cast.every(n => name.test(n))) problems.push('cast (one or more names, each a folder under docs/voices/)')
  if (!research || /[\n\r]/.test(research)) problems.push('research (the research file path)')
  if (problems.length) throw new Error('The brief is missing or has an unusable ' + problems.join('; ') + '.')
  return { slug, format, cast, research }
}

const brief = readBrief(args)

// ---------------------------------------------------------------- paths
const dir = `work/${brief.slug}/loop`
const P = {
  brief: `${dir}/brief.md`,
  s1: `${dir}/s1-research-read.md`,
  s2: `${dir}/s2-beats.md`,
  stance: `${dir}/stance.md`,
  // r0 is the writer's draft; r1 and r2 are the rewrites. Every round keeps its own files.
  script: r => `${dir}/r${r}-script.md`,
  anon: r => `${dir}/r${r}-script-anon.md`,
  notes: r => `${dir}/r${r}-notes.md`,
  swap: r => `${dir}/r${r}-4a-swap.md`,
  critique: r => `${dir}/r${r}-4b-critique.md`,
  facts: r => `${dir}/r${r}-5-facts.md`,
  tagged: `${dir}/s7-tagged.md`,
  lines: `${dir}/s7-lines.json`,
  handoff: `${dir}/s8-handoff.md`,
}

const HOUSE = ['CLAUDE.md', 'docs/script-bible.md', 'docs/learnings.md', 'docs/strategy.md'].map(p => ['House rules', p])
const FORMAT = [['Format file', `formats/${brief.format}.md`]]
const CARDS = brief.cast.map(n => [`Voice card (${n})`, `docs/voices/${n}/voice-card.md`])
const REFS = brief.cast.map(n => [`Reference transcripts and rhythm.md (${n}), folder`, `docs/voices/${n}/reference/`])
const GENERAL = [['General reference speech, folder', 'docs/voices/_general/reference/']]
const ALL_CARDS = [['All voice cards, folder', 'docs/voices/']] // no cast names: 4a must not be told who is speaking

const rows = (title, list) => `${title}:\n` + list.map(([label, path]) => `- ${label}: ${path}`).join('\n')
const task = (reads, writes) => `${rows('Read', reads)}\n\n${rows('Write', writes)}`

// ---------------------------------------------------------------- verdicts
function verdict(reply, allowed) {
  if (typeof reply !== 'string') return null
  const found = reply.match(/VERDICT:\s*[A-Z_]+/g)
  if (!found) return null
  const value = found[found.length - 1].replace(/VERDICT:\s*/, '')
  return allowed.includes(value) ? value : null
}

async function run(agentType, label, phaseTitle, reads, writes) {
  const reply = await agent(task(reads, writes), { agentType, label, phase: phaseTitle })
  if (reply === null || reply === undefined) throw new Error(`${label} did not finish; the run stops here.`)
  return reply
}

// ---------------------------------------------------------------- stages 1 to 3
const PH = {
  s1: 'Stage 1 · Research read', s2: 'Stage 2 · Stance and beats', s3: 'Stage 3 · Writer',
  critics: 'Stages 4–5 · Critics', s6: 'Stage 6 · Rewrite', s7: 'Stage 7 · Performance pass', s8: 'Stage 8 · Hand-off',
}

log(`Run folder: ${dir}. Brief expected at ${P.brief}.`)

const s1 = await run('reel-1-research', 'Stage 1 · research read', PH.s1,
  [['Research', brief.research], ['Brief', P.brief], ...HOUSE, ...FORMAT],
  [['Stage 1 output (main output)', P.s1]])
const take = verdict(s1, ['TAKE_POSSIBLE', 'NO_TAKE'])
if (take === 'NO_TAKE') {
  log(`Stage 1 says NO_TAKE. Stopped. The reasoning is in ${P.s1}.`)
  return { slug: brief.slug, stopped: 'NO_TAKE', stage1: P.s1, agents: 1 }
}
if (take !== 'TAKE_POSSIBLE') throw new Error(`Stage 1 returned no verdict line. Its output, if any, is at ${P.s1}.`)

await run('reel-2-stance', 'Stage 2 · stance and beats', PH.s2,
  [['Stage 1 output', P.s1], ...HOUSE, ...FORMAT, ...CARDS],
  [['Stage 2 output (main output)', P.s2], ['Stance file', P.stance]])

await run('reel-3-writer', 'Stage 3 · writer', PH.s3,
  [['Stage 2 output', P.s2], ...HOUSE, ...FORMAT, ...CARDS, ...REFS, ...GENERAL],
  [['Script alone', P.script(0)], ['Anonymised script', P.anon(0)], ['Notes (main output)', P.notes(0)]])

// ---------------------------------------------------------------- stages 4 to 6
// 4b needs 4a's output, so those two run in order. Stage 5 shares no input with them and runs alongside.
async function critique(r) {
  const [speech, facts] = await parallel([
    async () => {
      await agent(task(
        [['Anonymised script', P.anon(r)], ...ALL_CARDS],
        [['Swap test (main output)', P.swap(r)]]),
      { agentType: 'reel-4a-swap', label: `Stage 4a · swap test · r${r}`, phase: PH.critics })
      return verdict(await agent(task(
        [['Script', P.script(r)], ['Stage 4a output', P.swap(r)], ...ALL_CARDS, ...HOUSE, ...FORMAT, ...REFS, ['Locked stance', P.stance]],
        [['Critique (main output)', P.critique(r)]]),
      { agentType: 'reel-4b-critic', label: `Stage 4b · speech critique · r${r}`, phase: PH.critics }),
      ['SHIP', 'REWRITE_LINES', 'RESTRUCTURE'])
    },
    async () => verdict(await agent(task(
      [['Script', P.script(r)], ['Locked stance', P.stance], ['Stage 1 output', P.s1], ...HOUSE, ...FORMAT],
      [['Critique (main output)', P.facts(r)]]),
    { agentType: 'reel-5-facts', label: `Stage 5 · stance and facts · r${r}`, phase: PH.critics }),
    ['PASS', 'FAIL']),
  ])
  // A critic that returned no verdict is not a SHIP or a PASS.
  return { round: r, speech: speech || 'NO_VERDICT', facts: facts || 'NO_VERDICT' }
}

const rounds = []
let r = 0
let rewrites = 0
for (;;) {
  const c = await critique(r)
  rounds.push(c)
  log(`Round ${r}: Stage 4b ${c.speech}, Stage 5 ${c.facts}.`)
  if (c.speech === 'SHIP' && c.facts === 'PASS') break
  if (rewrites === MAX_REWRITES) {
    log(`Two rewrites done. Round ${r} only reports; its open issues go to the hand-off.`)
    break
  }
  rewrites += 1
  await run('reel-6-rewrite', `Stage 6 · rewrite ${rewrites}`, PH.s6,
    [['Script', P.script(r)], ['Stage 4b critique', P.critique(r)], ['Stage 5 critique', P.facts(r)], ['Stage 2 output', P.s2],
      ...HOUSE, ...FORMAT, ...CARDS, ...REFS],
    [['Script alone', P.script(r + 1)], ['Anonymised script', P.anon(r + 1)], ['Notes (main output)', P.notes(r + 1)]])
  r += 1
}

// ---------------------------------------------------------------- stages 7 and 8
await run('reel-7-performance', 'Stage 7 · performance pass', PH.s7,
  [['Final script', P.script(r)], ...FORMAT, ...CARDS, ...REFS],
  [['Tagged script (main output)', P.tagged], ['Lines file', P.lines]])

await run('reel-8-handoff', 'Stage 8 · hand-off', PH.s8,
  [['Stage 7 tagged script', P.tagged], ['Locked stance', P.stance], ['Stage 1 output', P.s1], ['Stage 2 output', P.s2],
    ['Last Stage 4b output', P.critique(r)], ['Last Stage 5 output', P.facts(r)], ...HOUSE, ...FORMAT, ...CARDS],
  [['Hand-off (main output)', P.handoff]])

const last = rounds[rounds.length - 1]
return {
  slug: brief.slug,
  stopped: null,
  rewrites,
  rounds,
  shippedClean: last.speech === 'SHIP' && last.facts === 'PASS',
  agents: 3 + rounds.length * 3 + rewrites + 2,
  finalScript: P.script(r),
  tagged: P.tagged,
  lines: P.lines,
  handoff: P.handoff,
}
