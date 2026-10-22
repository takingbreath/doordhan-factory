export const meta = {
  name: 'reel-script',
  description: 'Run the reel script loop of docs/script-playbook.md from free text to the hand-off: an intake that turns a link, a pasted script or a topic into a brief; research with reels, and the source video to adapt if there is one; independent writers with two scripts each; the lint as a report; one judge who picks three; one note back to a pick\'s writer; three cold readers per pick; a voice cut of each pick; and the hand-off. One named subagent per step, each given only file paths.',
  whenToUse: 'When a Sahayata Kendra reel needs a script. Type anything after /reel-script, one of three ways. (1) A link to adapt, YouTube or Instagram: /reel-script https://www.youtube.com/watch?v=... (2) A pasted script or transcript, about 60 words or more: /reel-script <paste it>. (3) A topic, with optional "stance: ...", "writers: N", "cast: ..." or "format: ...": /reel-script How much SIP is enough to retire? stance: start from the caller\'s own spending. Defaults: format sahayata_kendra; cast pandey, caller, billu; 3 writers; no stance. Pass the text exactly as typed as the args. The intake agent writes work/<slug>/loop/brief.md (and work/<slug>/source.md for a pasted transcript); the slug is up to five words of the topic plus the date. A brief that already has a slug (key: value text or JSON) skips the intake and runs as before, from the brief file saved at work/<slug>/loop/brief.md. The calling session\'s only jobs: run it; then report the slug, topic and source (the log\'s first line); every "## Missing" block that is not "None" (s1-working.md, every w*-note.md, s4-working.md, s7-working.md and s8-working.md; a cast member with no voice folder at all, the caller or Billu, gets one line, marked expected); the vidIQ credits used (the tally in s1-working.md); and each stage\'s time from the files\' times; then show s8-handoff.md in full and the paths of the cuts in work/<slug>/loop/audio/. A failed agent stops the run with its name: report that and stop.',
  phases: [
    { title: 'Intake', detail: 'free text to a brief: a link to adapt, a pasted script, or a topic (skipped when the args are already a brief)' },
    { title: 'Research', detail: 'facts with sources, numbers in code, how people ask it, five to eight reels with transcripts (vidIQ, 40 credits at most); with a source video, its transcript first' },
    { title: 'Writers', detail: 'independent writers; each picks the question and writes two scripts' },
    { title: 'Lint', detail: 'pipeline/script_lint.py on every script: a report for the judge, never a gate' },
    { title: 'Judge', detail: 'three picks, every claim traced, at most one note per pick' },
    { title: 'Notes', detail: 'a noted pick\'s writer answers once: keep, revise, or its other draft' },
    { title: 'Readers', detail: 'three cold retells per pick, as information' },
    { title: 'Voice', detail: 'a draft voice cut of each pick, the way V6b was made' },
    { title: 'Hand-off', detail: 'scripts first, then the cuts, then everything else' },
  ],
}

// The playbook is docs/script-playbook.md (v0.5, 22 Oct 2026); every agent reads it whole. Each step is its own agent
// (.claude/agents/reel-*.md) with fresh context, and its task is two lists of labelled paths: what to read, and where
// to write. What a step is not given is part of the design: a writer sees the research, the reels, the playbook and
// the example, never another writer's work or a voice card; a reader sees one script and nothing else; the judge
// changes no words. Paths back, and no others: the judge's one note to a pick's own writer, and a writer's one lookup
// for a missing number. The lint reports and stops nothing.

const PICKS = 3 // the playbook: three picks, from different writers where possible
const READERS = 3 // three cold readers per pick

// ---------------------------------------------------------------- the brief
function fromText(text) {
  const t = text.trim()
  try {
    const j = JSON.parse(t)
    if (j && typeof j === 'object' && !Array.isArray(j)) return j
  } catch (e) { /* not JSON: read it as "key: value" pairs */ }
  // "phase" and "research" are still recognised, so that an old brief is refused by name.
  const key = /\b(slug|topic|format|cast|stance|writers|source|phase|research(?:[ _-]?file)?(?:[ _-]?path)?)\s*[:=]\s*/gi
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
    throw new Error('reel-script needs a brief: slug, topic, format, cast, an optional stance and an optional number of writers.')
  }
  const text = v => (typeof v === 'string' ? v.trim() : '')
  if (b.phase !== undefined && b.phase !== null && String(b.phase).trim() !== '') {
    throw new Error('The brief names a phase, and loop v0.3 has none: every run goes from the topic to the hand-off. Take the phase line out of the brief.')
  }
  if (['research', 'research_file', 'researchFile', 'research_path', 'researchPath'].some(k => b[k] !== undefined)) {
    throw new Error('The brief names a research file, and the loop takes none: research works from the topic. Take the research line out of the brief.')
  }
  const slug = text(b.slug)
  const topic = text(b.topic)
  const format = text(b.format).replace(/^formats\//, '').replace(/\.md$/, '')
  const cast = (Array.isArray(b.cast) ? b.cast : text(b.cast).split(/[,\n]|\band\b/))
    .map(n => String(n).trim().toLowerCase()).filter(Boolean)
  const source = text(b.source) // optional: a YouTube or Instagram link, or a transcript file, of a video to adapt
  const writersRaw = b.writers === undefined || b.writers === null || String(b.writers).trim() === '' ? '3' : String(b.writers).trim()
  const writers = /^\d+$/.test(writersRaw) ? Number(writersRaw) : NaN
  const name = /^[a-z0-9][a-z0-9_-]*$/i
  const problems = []
  if (!name.test(slug)) problems.push('slug (letters, digits, - and _ only)')
  if (!topic) problems.push('topic (one line)')
  if (!name.test(format)) problems.push('format (the file name under formats/, without .md)')
  if (!cast.length || !cast.every(n => name.test(n))) problems.push('cast (one or more names)')
  if (!(writers >= 1 && writers <= 5)) problems.push('writers (a whole number from 1 to 5; leave it out for 3)')
  if (source && /[\n\r]/.test(source)) problems.push('source (one link or one path)')
  if (problems.length) throw new Error('The brief is missing or has an unusable ' + problems.join('; ') + '.')
  return { slug, topic, format, cast, writers, source }
}

// Are the args already a brief (an object, JSON, or "key: value" text, with a slug)? If not, they are free text for the
// intake: a link, a pasted script or transcript, or a topic line (which may carry "stance:" and the like, but no slug).
function givenBrief(input) {
  if (input && typeof input === 'object' && !Array.isArray(input)) return typeof input.slug === 'string' && input.slug.trim() ? input : null
  if (typeof input !== 'string') return null
  const b = fromText(input)
  return b && typeof b.slug === 'string' && b.slug.trim() ? b : null
}
function freeTextOf(input) {
  if (typeof input === 'string') return input.trim()
  if (input && typeof input === 'object' && typeof input.text === 'string') return input.text.trim()
  return ''
}

// ---------------------------------------------------------------- agents
const rows = (title, list) => `${title}:\n` + list.map(([label, path]) => `- ${label}: ${path}`).join('\n')
const task = (reads, writes) => `${rows('Read', reads)}\n\n${rows('Write', writes)}`

let agents = 0 // every agent started, for the result
const failures = [] // agents that did not finish: any one stops the run, with its name
function spawn(prompt, opts) {
  agents += 1
  return agent(prompt, opts)
}
async function run(agentType, label, phaseTitle, reads, writes, extra) {
  const reply = await spawn(task(reads, writes), { agentType, label, phase: phaseTitle, ...(extra || {}) })
  if (reply === null || reply === undefined) {
    failures.push(label)
    throw new Error(`${label} did not finish; the run stops here.`)
  }
  return reply
}
function stopIfFailed() {
  if (failures.length) throw new Error(`${failures.join(', ')} did not finish; the run stops here.`)
}

// ================================================================ 0. intake (only for free text)
// The workflow can't write files or read the clock; the intake agent does both: it decides the source, topic, any
// stance and the slug (with today's date), writes the brief file (and a pasted transcript), and replies with the brief.
const INTAKE_SCHEMA = {
  type: 'object',
  properties: {
    slug: { type: 'string', description: 'up to five words of the topic in kebab case, then -yyyymmdd; -2, -3 ... if work/<slug>/ exists' },
    topic: { type: 'string', description: 'one line' },
    format: { type: 'string', description: 'the file name under formats/, without .md (default sahayata_kendra)' },
    cast: { type: 'array', items: { type: 'string' }, description: 'default ["pandey", "caller", "billu"]' },
    stance: { type: 'string', description: 'only if the text names one ("stance: ..."), word for word; otherwise ""' },
    writers: { type: 'integer', description: '1 to 5; 3 unless the text says "writers: N"' },
    source: { type: 'string', description: 'the YouTube or Instagram link, or work/<slug>/source.md for a pasted transcript; "" for none' },
    note: { type: 'string', description: 'anything the user should know (e.g. the title could not be fetched); "" for nothing' },
  },
  required: ['slug', 'topic', 'format', 'cast', 'stance', 'writers', 'source', 'note'],
}
const intakeTask = (text, today) => [
  'The text typed after /reel-script, exactly as typed, between the two marker lines:',
  '=== TEXT START ===', text, '=== TEXT END ===', '',
  today ? `Today: ${today}` : 'Today: take the date from your environment.', '',
  'Write:',
  '- Brief: work/<slug>/loop/brief.md',
  '- Pasted transcript (only when the text is one): work/<slug>/source.md',
].join('\n')

let brief, intakeNote = ''
const given = givenBrief(args)
if (given) {
  brief = { ...readBrief(given), intake: false }
} else {
  const text = freeTextOf(args)
  if (!text) throw new Error('reel-script needs something to work from: a YouTube or Instagram link, a pasted script or transcript, or a topic line.')
  const today = args && typeof args === 'object' && args.date ? String(args.date) : ''
  const reply = await spawn(intakeTask(text, today), { agentType: 'reel-0-intake', label: 'Intake', phase: 'Intake', schema: INTAKE_SCHEMA })
  if (reply === null || reply === undefined) {
    failures.push('Intake')
    throw new Error('Intake did not finish; the run stops here.')
  }
  brief = { ...readBrief(reply), intake: true }
  intakeNote = typeof reply.note === 'string' ? reply.note.trim() : ''
}

// ---------------------------------------------------------------- paths
const dir = `work/${brief.slug}/loop`
const P = {
  brief: `${dir}/brief.md`,
  s1: `${dir}/s1-research.md`,
  s1Work: `${dir}/s1-working.md`,
  s1Math: `${dir}/s1-math.py`,
  reels: `${dir}/reels/`,
  note: w => `${dir}/w${w}-note.md`, // the writer's working file; the judge reads it
  script: stem => `${dir}/${stem}.md`, // w1-1, w1-2, w2-1 ... and w1-2r for a revision
  lintFails: stem => `${dir}/${stem}-lint-fails.md`, // named by pipeline/script_lint.py after the script
  lintReport: stem => `${dir}/${stem}-lint-report.md`,
  picks: `${dir}/s4-picks.md`,
  s4Work: `${dir}/s4-working.md`,
  judgeNote: stem => `${dir}/s4-note-${stem}.md`, // one per pick the judge sends a note about
  retell: (stem, k) => `${dir}/r-${stem}-${k}.md`,
  audio: `${dir}/audio/`,
  cut: stem => `${dir}/audio/${stem}/`, // voice_cut.py's folder for one pick
  cutReport: stem => `${dir}/audio/${stem}/report.md`,
  voiceNotes: `${dir}/audio/voice-notes.md`,
  s7Work: `${dir}/s7-working.md`,
  handoff: `${dir}/s8-handoff.md`,
  s8Work: `${dir}/s8-working.md`,
}
const stemOf = (w, m) => `w${w}-${m}`
const writerOf = stem => Number(/^w(\d+)-/.exec(stem)[1])
const numOf = stem => Number(/^w\d+-(\d)/.exec(stem)[1])

const CLAUDE_MD = ['House rules: CLAUDE.md', 'CLAUDE.md']
const PLAYBOOK = ['Playbook (read it whole)', 'docs/script-playbook.md']
const PROSODY = ['Prosody reference (Working application and interpretation limits; evidence is background)', 'docs/script-flow-research.md']
const EXAMPLE = ['Example, the dollar reel (the shape and the voice; don\'t reuse its lines)', 'docs/examples/sahayata-kendra-dollar-rate.md']
const EXAMPLE2 = ['Example, the SIP reel (one chain from the caller\'s own number; its first line is the known weakness; don\'t reuse its lines)', 'docs/examples/sahayata-kendra-sip-retire.md']
const FORMAT_FILE = `formats/${brief.format}.md`
const CARDS = brief.cast.map(n => [`Voice card (${n})`, `docs/voices/${n}/voice-card.md`])

const PH = {
  research: 'Research', writers: 'Writers', lint: 'Lint', judge: 'Judge', notes: 'Notes', readers: 'Readers',
  voice: 'Voice', handoff: 'Hand-off',
}

// The lint on one script: its verdict is ignored and its report goes on. An error (it couldn't read the script) is
// logged, and the judge finds the report missing.
const lintNotes = []
async function lint(stem) {
  const reply = await run('reel-lint', `Lint · ${stem}`, PH.lint,
    [['Format file', FORMAT_FILE], ['Script', P.script(stem)]],
    [['Lint fails file (the lint names it)', P.lintFails(stem)], ['Lint report (the lint names it)', P.lintReport(stem)]])
  if (/LINT_ERROR/.test(reply)) lintNotes.push(`${stem}: the lint could not read it`)
  return reply
}

log(`Slug: ${brief.slug} · Topic: ${brief.topic} · Source: ${brief.source || 'none'} · Writers: ${brief.writers} · ` +
  `Brief: ${P.brief}${brief.intake ? ' (written by the intake)' : ''}`)
if (intakeNote) log(`Intake note: ${intakeNote}`)

// ================================================================ 1. research
await run('reel-1-research', 'Research', PH.research,
  [['Brief', P.brief], ...(brief.source ? [['Source video to adapt (a YouTube or Instagram link, or a transcript file); its transcript goes to reels/00-source.md', brief.source]] : []),
    CLAUDE_MD, ['Format file', FORMAT_FILE], PLAYBOOK],
  [['Handoff', P.s1], ['Working file', P.s1Work], ['Python file (every number it computes)', P.s1Math],
    ['Reels folder (one file per reel)', P.reels]])

// ================================================================ 2. writers, each linted as soon as it finishes
const writerIds = Array.from({ length: brief.writers }, (_, i) => i + 1)
await pipeline(writerIds,
  w => run('reel-2-writer', `Writer ${w}`, PH.writers,
    [['Research handoff', P.s1], ['Reels folder', P.reels], PLAYBOOK, PROSODY, EXAMPLE, EXAMPLE2],
    [['Your note (working file; the judge reads it)', P.note(w)], ['Script 1', P.script(stemOf(w, 1))],
      ['Script 2', P.script(stemOf(w, 2))]]),
  (_, w) => parallel([1, 2].map(m => () => lint(stemOf(w, m)))))
stopIfFailed()
const scripts = writerIds.flatMap(w => [stemOf(w, 1), stemOf(w, 2)])

// ================================================================ 3. the judge
const want = Math.min(PICKS, scripts.length)
const judged = await run('reel-4-judge', 'Judge', PH.judge,
  [...scripts.map(s => [`Script ${s} (writer ${writerOf(s)})`, P.script(s)]),
    ...writerIds.map(w => [`Writer ${w}'s note`, P.note(w)]),
    ['Research handoff', P.s1], PLAYBOOK, PROSODY, EXAMPLE, EXAMPLE2, ['Pandey\'s voice card', 'docs/voices/pandey/voice-card.md'],
    ...scripts.map(s => [`Lint report for ${s}`, P.lintReport(s)])],
  [['Picks file', P.picks], ['Working file', P.s4Work],
    ['Note to a pick\'s writer, one file per pick with a note (<script> is the pick\'s file name without .md)', P.judgeNote('<script>')]],
  { schema: {
    type: 'object',
    properties: {
      picks: {
        type: 'array',
        description: `exactly ${want} picks, in order of preference`,
        items: {
          type: 'object',
          properties: {
            script: { type: 'string', description: 'the picked script\'s file name without .md, e.g. w2-1' },
            note: { type: 'boolean', description: 'true if you wrote this pick\'s writer a note file' },
          },
          required: ['script', 'note'],
        },
      },
    },
    required: ['picks'],
  } })
const picks = Array.isArray(judged.picks) ? judged.picks.map(p => ({ script: String(p.script).trim().replace(/\.md$/, ''), note: !!p.note })) : []
const pickStems = picks.map(p => p.script)
if (picks.length !== want || !pickStems.every(s => scripts.includes(s)) || new Set(pickStems).size !== picks.length) {
  throw new Error(`The judge returned ${JSON.stringify(judged.picks)}, not ${want} different scripts from ${scripts.join(', ')}; the run stops here. Its picks file is ${P.picks}.`)
}
const pickWriters = new Set(pickStems.map(writerOf))
if (pickWriters.size < Math.min(want, brief.writers)) {
  log(`The judge picked from ${pickWriters.size} writer(s) where ${Math.min(want, brief.writers)} were possible; its reasons are in ${P.picks}.`)
}
log(`Picks: ${picks.map(p => p.script + (p.note ? ' (note)' : '')).join(', ')}.`)

// ================================================================ 4–5. the judge's notes, then the readers
// One pipeline item per writer with picks, so a writer answers its notes one at a time (its note file is the same),
// and each pick's readers start as soon as its final version is known.
const outcome = {} // pick -> { final, answer }
const byWriter = [...pickWriters].map(w => picks.filter(p => writerOf(p.script) === w))
await pipeline(byWriter,
  async group => {
    for (const p of group) {
      if (!p.note) { outcome[p.script] = { final: p.script, answer: 'no note' }; continue }
      const w = writerOf(p.script), m = numOf(p.script), other = stemOf(w, 3 - m)
      const otherPicked = pickStems.includes(other)
      const reply = await run('reel-2-writer', `Writer ${w} · reply on ${p.script}`, PH.notes,
        [['Your note', P.note(w)], [`Your script ${m} (${p.script}, the pick the judge's note is about)`, P.script(p.script)],
          [otherPicked ? `Your script ${3 - m} (${other}, also one of the picks, so you can't offer it instead)`
            : `Your script ${3 - m} (${other}, your other draft)`, P.script(other)],
          ['The judge\'s note', P.judgeNote(p.script)], PLAYBOOK, PROSODY],
        [['Revised script (write it only if you revise)', P.script(`${p.script}r`)],
          ['Your note (add your reply at the end)', P.note(w)]])
      const said = (/\b(KEEP|REVISED|OTHER)\b/.exec(String(reply)) || [])[1]
      if (!said) {
        failures.push(`Writer ${w} · reply on ${p.script}`)
        throw new Error(`Writer ${w} answered the judge's note on ${p.script} with neither KEEP, REVISED nor OTHER; the run stops here.`)
      }
      if (said === 'REVISED') {
        outcome[p.script] = { final: `${p.script}r`, answer: 'revised' }
        await lint(`${p.script}r`)
      } else if (said === 'OTHER' && !otherPicked) {
        outcome[p.script] = { final: other, answer: 'other draft' }
      } else {
        if (said === 'OTHER') log(`Writer ${w} offered ${other} for ${p.script}, but ${other} is already a pick; ${p.script} stays.`)
        outcome[p.script] = { final: p.script, answer: 'kept' }
      }
    }
    return group
  },
  group => parallel(group.flatMap(p => Array.from({ length: READERS }, (_, i) => async () => {
    const stem = outcome[p.script].final
    const reply = await run('reel-4c-recall', `Reader ${i + 1} · ${stem}`, PH.readers,
      [['Script', P.script(stem)]], [['Your retell', P.retell(stem, i + 1)]])
    if (/MISSING_SCRIPT/.test(reply)) {
      failures.push(`Reader ${i + 1} · ${stem}`)
      throw new Error(`Reader ${i + 1} found no script at ${P.script(stem)}.`)
    }
  }))))
stopIfFailed()
const finals = picks.map(p => ({ pick: p.script, note: p.note, ...outcome[p.script] }))

// ================================================================ 6. voice
await run('reel-7-performance', 'Voice', PH.voice,
  [...finals.map(f => [`Pick ${f.final}`, P.script(f.final)]), ...CARDS, PROSODY],
  [...finals.map(f => [`Audio folder for ${f.final}`, P.cut(f.final)]), ['Voice notes (handoff)', P.voiceNotes],
    ['Working file', P.s7Work]])

// ================================================================ 7. hand-off
const how = f => {
  const by = `writer ${writerOf(f.final)}`
  if (f.answer === 'revised') return `${by}; revised after the judge's note on ${f.pick}`
  if (f.answer === 'other draft') return `${by}; the writer's other draft, offered after the judge's note on ${f.pick}`
  if (f.answer === 'kept') return `${by}; kept as written after the judge's note`
  return `${by}; no note`
}
const noted = finals.filter(f => f.note)
await run('reel-8-handoff', 'Hand-off', PH.handoff,
  [...finals.map((f, i) => [`Pick ${i + 1}: ${f.final} (${how(f)})`, P.script(f.final)]),
    ...finals.filter(f => f.answer === 'revised').map(f => [`${f.pick}, the version the judge traced, before the revision`, P.script(f.pick)]),
    ['Judge\'s picks file', P.picks],
    ...noted.map(f => [`Judge's note on ${f.pick}`, P.judgeNote(f.pick)]),
    ...[...new Set(finals.map(f => writerOf(f.final)))].map(w => [`Writer ${w}'s note`, P.note(w)]),
    ...finals.flatMap(f => Array.from({ length: READERS }, (_, i) => [`Retell ${i + 1} of ${f.final}`, P.retell(f.final, i + 1)])),
    ...finals.map(f => [`Lint report for ${f.final}`, P.lintReport(f.final)]),
    ['Voice notes', P.voiceNotes],
    ...finals.map(f => [`Cut report for ${f.final}`, P.cutReport(f.final)]),
    ['Research handoff', P.s1], CLAUDE_MD, PLAYBOOK],
  [['Hand-off', P.handoff], ['Working file', P.s8Work]])

if (lintNotes.length) log(`Lint errors (reported, not stopping): ${lintNotes.join('; ')}.`)
return {
  slug: brief.slug,
  topic: brief.topic,
  source: brief.source,
  intake: brief.intake,
  writers: brief.writers,
  scripts,
  picks: finals.map(f => ({ pick: f.pick, note: f.note, answer: f.answer, final: f.final, cut: P.cut(f.final) })),
  lintErrors: lintNotes,
  agents,
  handoff: P.handoff,
  audio: P.audio,
}
