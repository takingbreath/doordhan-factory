export const meta = {
  name: 'reel-script',
  description: 'Run the reel script loop from prompts/script-writer.md end to end, from a topic to the hand-off: research, the blueprint, the fact check (one revision at most), the writer, lint, critics and recall test, at most two rewrites, the performance pass and the hand-off. One named subagent per stage, each given only file paths.',
  whenToUse: 'When a reel needs a script for a topic. Takes a brief: slug, topic, format, cast, an optional stance, and an optional phase. "full", the default and what a brief without a phase runs, goes from the topic to the hand-off without stopping; "blueprint" stops after the fact check, so the human can read the blueprint first. The brief has no research path: Stage 1 researches the topic on the web. A workflow script cannot write files, so save the brief as work/<slug>/loop/brief.md before launching: Stage 1 reads the topic and any stance from that file. The run stops early on Stage 1\'s NO_TAKE (its reasons are in s1-research.md) or on a second FIX from the fact check (the result\'s "why" lists the items; the full check is in s2b-factcheck-2.md). After every run, before reporting anything else, the calling session reads the "## Missing" block at the top of every working file in work/<slug>/loop/ and reports each one that is not "None": the stage, and what was missing. The working files are s1-working, s2-working and s2b-working; after a revision, s2-working-2 and s2b-working-2; then r*-notes (writer and rewrites), r*-4a-working, r*-4b-working, r*-4d-working, r*-5-working, s7-working and s8-working. The lint and the recall runs (r*-4c-*) write no working file. A cast member with no voice folder at all gets one line, marked expected.',
  phases: [
    { title: 'Stage 1 · Research', detail: 'the web, the viewer\'s question, the crowd, the math in code; TAKE_POSSIBLE or NO_TAKE' },
    { title: 'Stage 2 · Reel blueprint', detail: 'locks the stance; revised once if the fact check says FIX' },
    { title: 'Stage 2b · Fact check', detail: 'every fact and number in the blueprint, recomputed in code; PASS or FIX' },
    { title: 'Stage 3 · Writer', detail: 'both openings, from the blueprint that passed the fact check' },
    { title: 'Stage 4 · Lint', detail: 'pipeline/script_lint.py on both versions' },
    { title: 'Stages 4–5 · Critics', detail: 'swap test, speech critique, recall test and check, stance and facts' },
    { title: 'Stage 6 · Rewrite', detail: 'at most twice' },
    { title: 'Stage 7 · Performance pass', detail: 'delivery tags and the lines file' },
    { title: 'Stage 8 · Hand-off', detail: 'the script message for the human' },
  ],
}

// The spec is prompts/script-writer.md (v3.3). Each stage is its own agent (.claude/agents/reel-*.md) with fresh
// context. An agent's task is two lists of labelled paths and nothing else: the inputs its stage's "Inputs" line
// names, and where to write. Every model stage but the recall test writes a handoff (its "Output" list) and a working
// file (a record of evidence for the human); later stages get handoffs only, never a working file (spec, "Handoff
// and working file"). What a stage is not given is as much a part of the design as what it is: the fact check never
// sees Stage 1's Python, so it recomputes rather than copies; the writer never sees the research; 4a, 4b and 4c never
// see the research, the blueprint, the writer's notes or the lint; a recall reader sees one version of the script and
// nothing else; the rewrite gets the lint's fails, never its report.

const MAX_BLUEPRINTS = 2 // the blueprint and one revision; a second FIX stops the run
const MAX_REWRITES = 2 // spec, "Loop control": more rounds make scripts worse
const RECALL_RUNS = 3 // spec, "4c — Recall test": three runs on each version

// ---------------------------------------------------------------- the brief
function fromText(text) {
  const t = text.trim()
  try {
    const j = JSON.parse(t)
    if (j && typeof j === 'object' && !Array.isArray(j)) return j
  } catch (e) { /* not JSON: read it as "key: value" pairs */ }
  // "research" is still recognised, so that an old brief is refused by name instead of running into the field before it.
  const key = /\b(slug|topic|format|cast|phase|research(?:[ _-]?file)?(?:[ _-]?path)?|stance)\s*[:=]\s*/gi
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
    throw new Error('reel-script needs a brief: slug, topic, format, cast, an optional stance and an optional phase (full or blueprint).')
  }
  const text = v => (typeof v === 'string' ? v.trim() : '')
  if (['research', 'research_file', 'researchFile', 'research_path', 'researchPath'].some(k => b[k] !== undefined)) {
    throw new Error('The brief names a research file, and the loop no longer takes one: Stage 1 researches the topic itself (spec v3.3). Take the research line out of the brief.')
  }
  const slug = text(b.slug)
  const topic = text(b.topic)
  const format = text(b.format).replace(/^formats\//, '').replace(/\.md$/, '')
  const phase = text(b.phase).toLowerCase() || 'full' // spec, "Running end to end": it doesn't stop by default
  const cast = (Array.isArray(b.cast) ? b.cast : text(b.cast).split(/[,\n]|\band\b/))
    .map(n => String(n).trim().toLowerCase()).filter(Boolean)
  const name = /^[a-z0-9][a-z0-9_-]*$/i
  const problems = []
  if (!name.test(slug)) problems.push('slug (letters, digits, - and _ only)')
  if (!topic) problems.push('topic (one line)')
  if (!name.test(format)) problems.push('format (the file name under formats/, without .md)')
  if (!cast.length || !cast.every(n => name.test(n))) problems.push('cast (one or more names, each a folder under docs/voices/)')
  if (phase !== 'full' && phase !== 'blueprint') problems.push('phase (full or blueprint; leave it out for full)')
  if (problems.length) throw new Error('The brief is missing or has an unusable ' + problems.join('; ') + '.')
  return { slug, format, cast, phase }
}

const brief = readBrief(args)

// ---------------------------------------------------------------- paths
const dir = `work/${brief.slug}/loop`
const nth = (n, stem, ext) => `${dir}/${stem}${n > 1 ? `-${n}` : ''}.${ext}` // the revision's files get "-2"
const P = {
  brief: `${dir}/brief.md`,
  s1: `${dir}/s1-research.md`,
  s1Work: `${dir}/s1-working.md`,
  s1Math: `${dir}/s1-math.py`,
  blueprint: n => nth(n, 's2-blueprint', 'md'),
  s2Work: n => nth(n, 's2-working', 'md'),
  factCheck: n => nth(n, 's2b-factcheck', 'md'),
  s2bWork: n => nth(n, 's2b-working', 'md'),
  s2bMath: n => nth(n, 's2b-math', 'py'),
  stance: `${dir}/stance.md`,
  // r0 is the writer's draft; r1 and r2 are the rewrites. Every round keeps its own files.
  script: r => `${dir}/r${r}-script.md`, // the main opening
  alt: r => `${dir}/r${r}-script-alt.md`, // the other opening, every later line the same
  anon: r => `${dir}/r${r}-script-anon.md`,
  notes: r => `${dir}/r${r}-notes.md`, // the writer's and the rewrite's working file
  lintFails: r => `${dir}/r${r}-script-lint-fails.md`, // named by pipeline/script_lint.py after the main script
  lintReport: r => `${dir}/r${r}-script-lint-report.md`,
  swap: r => `${dir}/r${r}-4a-swap.md`,
  swapWork: r => `${dir}/r${r}-4a-working.md`,
  critique: r => `${dir}/r${r}-4b-critique.md`,
  critiqueWork: r => `${dir}/r${r}-4b-working.md`,
  recall: (r, v, k) => `${dir}/r${r}-4c-${v}-${k}.md`, // v is main or alt, k is 1 to 3
  check: r => `${dir}/r${r}-4d-check.md`,
  checkWork: r => `${dir}/r${r}-4d-working.md`,
  facts: r => `${dir}/r${r}-5-facts.md`,
  factsWork: r => `${dir}/r${r}-5-working.md`,
  tagged: `${dir}/s7-tagged.md`,
  lines: `${dir}/s7-lines.json`,
  s7Work: `${dir}/s7-working.md`,
  handoff: `${dir}/s8-handoff.md`,
  details: `${dir}/s8-details.md`,
  s8Work: `${dir}/s8-working.md`,
}

// House rules, one by one: most stages get only some of them (spec §0 and each stage's "Inputs" line).
const CLAUDE_MD = ['House rules: CLAUDE.md', 'CLAUDE.md']
const BIBLE = ['House rules: the script bible', 'docs/script-bible.md']
const LEARNINGS = ['House rules: learnings', 'docs/learnings.md']
const PLAN = ["House rules: this week's plan", 'docs/strategy.md']
const HOUSE = [CLAUDE_MD, BIBLE, LEARNINGS, PLAN] // "all house rules"
const FORMAT_FILE = `formats/${brief.format}.md`
const FORMAT = [['Format file', FORMAT_FILE]]
const HOOK_MENU = [['Hook menu', 'docs/hook-menu.md']] // Stage 2 only; no stage reads docs/hooks.md (spec §0)
// A character's voice files live in docs/voices/<name>/: voice-card.md, reference/ (transcripts and rhythm.md) and,
// where one exists, dialect-notes.md, which counts as part of the reference transcripts (spec §0).
const CARDS = brief.cast.map(n => [`Voice card (${n})`, `docs/voices/${n}/voice-card.md`])
const REFS = brief.cast.flatMap(n => [
  [`Reference transcripts and rhythm.md (${n}), folder`, `docs/voices/${n}/reference/`],
  [`Dialect notes (${n}), part of the reference transcripts`, `docs/voices/${n}/dialect-notes.md`],
])
const GENERAL = [['General reference speech, folder', 'docs/voices/general/reference/']] // the writer's only
const ALL_CARDS = [['All voice cards, folder', 'docs/voices/']] // no cast names: 4a must not be told who is speaking
const VERSIONS = r => [['Script, main version', P.script(r)], ['Script, alternate version (the other opening)', P.alt(r)]]
const SCRIPT_FILES = r => [ // what the writer and the rewrite save
  ['Main script (handoff)', P.script(r)], ['Alternate script, the other opening (handoff)', P.alt(r)],
  ['Anonymised main script (handoff)', P.anon(r)], ['Notes (working file)', P.notes(r)],
]

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

let agents = 0 // every agent started, for the result
function spawn(prompt, opts) {
  agents += 1
  return agent(prompt, opts)
}

async function run(agentType, label, phaseTitle, reads, writes) {
  const reply = await spawn(task(reads, writes), { agentType, label, phase: phaseTitle })
  if (reply === null || reply === undefined) throw new Error(`${label} did not finish; the run stops here.`)
  return reply
}

const PH = {
  s1: 'Stage 1 · Research', s2: 'Stage 2 · Reel blueprint', s2b: 'Stage 2b · Fact check', s3: 'Stage 3 · Writer',
  lint: 'Stage 4 · Lint', critics: 'Stages 4–5 · Critics', s6: 'Stage 6 · Rewrite', s7: 'Stage 7 · Performance pass',
  s8: 'Stage 8 · Hand-off',
}

log(`Run folder: ${dir}. Phase: ${brief.phase}. Brief expected at ${P.brief}.`)

// ================================================================ Stage 1: research
// Stage 1 inputs: the brief (the topic, and a stance if one was supplied), CLAUDE.md, format file. It researches on
// the web and computes every number in its own Python file.
const s1 = await run('reel-1-research', 'Stage 1 · research', PH.s1,
  [['Brief', P.brief], CLAUDE_MD, ...FORMAT],
  [['Handoff', P.s1], ['Working file', P.s1Work], ['Python file (every number it computes)', P.s1Math]])
const take = verdict(s1, ['TAKE_POSSIBLE', 'NO_TAKE'])
if (take === 'NO_TAKE') {
  log(`Stage 1 says NO_TAKE. Stopped. Its reasons are in ${P.s1}.`)
  return { slug: brief.slug, phase: brief.phase, stopped: 'NO_TAKE', stage1: P.s1, agents }
}
if (take !== 'TAKE_POSSIBLE') throw new Error(`Stage 1 returned no verdict line. Its output, if any, is at ${P.s1}.`)

// ================================================================ Stages 2 and 2b: the blueprint and its fact check
// A FIX sends the blueprint back once (spec, Stage 2 "On a revision"); a second FIX stops the run, because a plan
// whose facts fail twice needs the human, not a third pass.
let n = 1
for (;;) {
  // Stage 2 inputs: Stage 1 output, all house rules, format file, the hook menu, the cast's voice cards; on a
  // revision, also its last blueprint and the fact check.
  const revision = n > 1
    ? [['Your last blueprint', P.blueprint(n - 1)], ['Stage 2b fact check', P.factCheck(n - 1)]]
    : []
  await run('reel-2-blueprint', revision.length ? 'Stage 2 · blueprint revision' : 'Stage 2 · reel blueprint', PH.s2,
    [['Stage 1 handoff', P.s1], ...HOUSE, ...FORMAT, ...HOOK_MENU, ...CARDS, ...revision],
    [['Blueprint (handoff)', P.blueprint(n)], ['Stance file', P.stance], ['Working file', P.s2Work(n)]])

  // Stage 2b inputs: the blueprint, Stage 1 output, CLAUDE.md. Never Stage 1's Python: it recomputes from the
  // blueprint's own assumptions.
  const reply = await run('reel-2b-factcheck', n > 1 ? 'Stage 2b · fact check 2' : 'Stage 2b · fact check', PH.s2b,
    [['Blueprint', P.blueprint(n)], ['Stage 1 handoff', P.s1], CLAUDE_MD],
    [['Handoff', P.factCheck(n)], ['Working file', P.s2bWork(n)], ['Python file (its recomputation)', P.s2bMath(n)]])
  const checked = verdict(reply, ['PASS', 'FIX'])
  if (!checked) throw new Error(`Stage 2b returned no verdict line. Its output, if any, is at ${P.factCheck(n)}.`)
  if (checked === 'PASS') break
  // On FIX, 2b replies with the items to fix above its verdict line.
  const why = reply.replace(/\s*VERDICT:\s*FIX\s*$/, '').trim() || `(no items in the reply; see ${P.factCheck(n)})`
  if (n === MAX_BLUEPRINTS) {
    log(`The fact check said FIX on the revised blueprint too. Stopped before any dialogue: the human decides. What still fails:\n${why}`)
    return {
      slug: brief.slug, phase: brief.phase, stopped: 'FIX', why, blueprint: P.blueprint(n), factCheck: P.factCheck(n),
      stance: P.stance, stage1: P.s1, agents,
    }
  }
  log(`The fact check said FIX on ${P.blueprint(n)}; Stage 2 revises it once. Items:\n${why}`)
  n += 1
}

// Every later stage that reads the blueprint or the fact check reads the last one.
const BP = P.blueprint(n)
const FC = P.factCheck(n)

// spec, "Running end to end": a run can be told to stop after the fact check, so the human reads the blueprint first.
if (brief.phase === 'blueprint') {
  log(`Blueprint checked: ${BP} (fact check ${FC}, PASS). Phase blueprint stops here.`)
  return {
    slug: brief.slug, phase: brief.phase, stopped: null, blueprint: BP, factCheck: FC, stance: P.stance,
    stage1: P.s1, revisions: n - 1, agents,
  }
}

// ================================================================ Stage 3 onward, from the checked blueprint
// Stage 3 inputs: Stage 2 output (the blueprint that passed the fact check), the script bible, format file, voice
// cards, reference transcripts and rhythm.md, general reference speech.
const s3 = await run('reel-3-writer', 'Stage 3 · writer', PH.s3,
  [['Stage 2 handoff (the blueprint that passed the fact check)', BP], BIBLE, ...FORMAT, ...CARDS, ...REFS, ...GENERAL],
  SCRIPT_FILES(0))
if (/MISSING_BLUEPRINT/.test(s3)) {
  log(`Stage 3 found no blueprint at ${BP}. Stopped.`)
  return { slug: brief.slug, phase: brief.phase, stopped: 'MISSING_BLUEPRINT', blueprint: BP, agents }
}

// ---------------------------------------------------------------- one round: the lint, then the critics
async function round(r) {
  // The lint runs first, on both versions; no model reads a draft before it (spec, "Lint").
  const lint = await run('reel-lint', `Stage 4 · lint · r${r}`, PH.lint,
    [['Format file', FORMAT_FILE], ['Main script', P.script(r)], ['Alternate script', P.alt(r)]],
    [['Lint fails file (the lint names it)', P.lintFails(r)], ['Lint report (the lint names it)', P.lintReport(r)]])
  if (/LINT_ERROR/.test(lint)) {
    throw new Error(`Round ${r}: the lint could not read what it needs, so there is no verdict and the run stops here (an error is never a pass).\n${lint}`)
  }
  const lintVerdict = verdict(lint, ['PASS', 'FAIL'])
  if (!lintVerdict) throw new Error(`Round ${r}: the lint returned no verdict line; the run stops here.\n${lint}`)

  const [speech, recall, facts] = await parallel([
    // 4a, then 4b, which needs 4a's handoff.
    async () => {
      // 4a inputs: the anonymised script, all character voice cards in the repository.
      const swap = await spawn(task(
        [['Anonymised script', P.anon(r)], ...ALL_CARDS],
        [['Handoff', P.swap(r)], ['Working file', P.swapWork(r)]]),
      { agentType: 'reel-4a-swap', label: `Stage 4a · swap test · r${r}`, phase: PH.critics })
      if (swap === null || swap === undefined) return null // 4b needs 4a's handoff
      // 4b inputs: every version of the script, the 4a output, all voice cards, the script bible, format file, the
      // cast's reference transcripts, the locked stance.
      return verdict(await spawn(task(
        [...VERSIONS(r), ['Stage 4a handoff', P.swap(r)], ...ALL_CARDS, BIBLE, ...FORMAT, ...REFS, ['Locked stance', P.stance]],
        [['Handoff', P.critique(r)], ['Working file', P.critiqueWork(r)]]),
      { agentType: 'reel-4b-critic', label: `Stage 4b · speech critique · r${r}`, phase: PH.critics }),
      ['SHIP', 'REWRITE_LINES', 'RESTRUCTURE'])
    },
    // The recall test, three cold readers per version, each a separate call that sees one script and nothing
    // else; then 4d compares what they took away with the blueprint.
    async () => {
      const runs = []
      for (const [v, path] of [['main', P.script(r)], ['alt', P.alt(r)]]) {
        for (let k = 1; k <= RECALL_RUNS; k++) runs.push({ v, k, path })
      }
      const answers = await parallel(runs.map(({ v, k, path }) => async () => {
        const reply = await spawn(task(
          [[`Script (${v === 'main' ? 'main version' : 'alternate version'})`, path]],
          [['Answers (handoff)', P.recall(r, v, k)]]),
        { agentType: 'reel-4c-recall', label: `Stage 4c · recall · r${r} · ${v} ${k}`, phase: PH.critics })
        return typeof reply === 'string' && !/MISSING_SCRIPT/.test(reply) ? reply : null
      }))
      if (answers.some(a => a === null)) return null // 4d needs all six answers
      // 4d inputs: the three recall answers for each version, the script versions, Stage 2 output (the blueprint).
      return verdict(await spawn(task(
        [...runs.map(({ v, k }) => [`Recall answers, ${v === 'main' ? 'main version' : 'alternate version'}, reader ${k}`, P.recall(r, v, k)]),
          ...VERSIONS(r), ['Stage 2 handoff (the blueprint)', BP]],
        [['Handoff', P.check(r)], ['Working file', P.checkWork(r)]]),
      { agentType: 'reel-4d-check', label: `Stage 4d · recall check · r${r}`, phase: PH.critics }),
      ['CLEAR', 'CONFUSING'])
    },
    // Stage 5 inputs: every version of the script, the lint report, the locked stance, Stage 1 output, the last
    // Stage 2b fact check, CLAUDE.md, the script bible, this week's plan, format file.
    async () => verdict(await spawn(task(
      [...VERSIONS(r), ['Lint report', P.lintReport(r)], ['Locked stance', P.stance], ['Stage 1 handoff', P.s1],
        ['Last Stage 2b fact check', FC], CLAUDE_MD, BIBLE, PLAN, ...FORMAT],
      [['Handoff', P.facts(r)], ['Working file', P.factsWork(r)]]),
    { agentType: 'reel-5-facts', label: `Stage 5 · stance and facts · r${r}`, phase: PH.critics }),
    ['PASS', 'FAIL']),
  ])
  // A critic that failed or returned no verdict stops the run. Treating it as "not SHIP" sends the rewrite to
  // critiques that don't exist (looptest2, 1 Oct 2026: every critic was refused at the API, and two rewrites ran
  // on nothing).
  const failed = [
    speech ? null : `Stage 4a/4b (${P.critique(r)})`,
    recall ? null : `Stage 4c/4d (${P.check(r)})`,
    facts ? null : `Stage 5 (${P.facts(r)})`,
  ].filter(Boolean)
  if (failed.length) throw new Error(`Round ${r}: ${failed.join(', ')} failed or returned no verdict; the run stops here.`)
  return { round: r, lint: lintVerdict, speech, recall, facts }
}

const ships = c => c.lint === 'PASS' && c.speech === 'SHIP' && c.recall === 'CLEAR' && c.facts === 'PASS'

const rounds = []
let r = 0
let rewrites = 0
for (;;) {
  const c = await round(r)
  rounds.push(c)
  log(`Round ${r}: lint ${c.lint}, Stage 4b ${c.speech}, Stage 4d ${c.recall}, Stage 5 ${c.facts}.`)
  if (ships(c)) break
  if (rewrites === MAX_REWRITES) {
    log(`Two rewrites done. Round ${r} only reports; its open issues go to the hand-off.`)
    break
  }
  rewrites += 1
  // Stage 6 inputs: every version of the script, the lint's fails file (never its report), the 4b, 4d and Stage 5
  // handoffs, Stage 2 output (the blueprint), the script bible, format file, the cast's voice cards and reference
  // transcripts.
  await run('reel-6-rewrite', `Stage 6 · rewrite ${rewrites}`, PH.s6,
    [...VERSIONS(r), ['Lint fails file', P.lintFails(r)], ['Stage 4b handoff', P.critique(r)], ['Stage 4d handoff', P.check(r)],
      ['Stage 5 handoff', P.facts(r)], ['Stage 2 handoff (the blueprint)', BP], BIBLE, ...FORMAT, ...CARDS, ...REFS],
    SCRIPT_FILES(r + 1))
  r += 1
}

// ---------------------------------------------------------------- stages 7 and 8
// Stage 7 inputs: both final versions, format file, the cast's voice cards.
await run('reel-7-performance', 'Stage 7 · performance pass', PH.s7,
  [['Final script, main version', P.script(r)], ['Final script, alternate version (the other opening)', P.alt(r)], ...FORMAT, ...CARDS],
  [['Tagged script (handoff)', P.tagged], ['Lines file (handoff)', P.lines], ['Working file', P.s7Work]])

// Stage 8 inputs: every version of the final script, the Stage 7 tagged voice script, the locked stance, Stage 1 and
// Stage 2 output, the last Stage 2b fact check, the last lint report, the last Stage 4b, 4d and Stage 5 outputs, the
// script bible, format file, the cast's voice cards.
await run('reel-8-handoff', 'Stage 8 · hand-off', PH.s8,
  [['Final script, main version', P.script(r)], ['Final script, alternate version (the other opening)', P.alt(r)],
    ['Stage 7 tagged script', P.tagged], ['Locked stance', P.stance], ['Stage 1 handoff', P.s1],
    ['Stage 2 handoff (the blueprint)', BP], ['Last Stage 2b fact check', FC], ['Last lint report', P.lintReport(r)],
    ['Last Stage 4b handoff', P.critique(r)], ['Last Stage 4d handoff', P.check(r)], ['Last Stage 5 handoff', P.facts(r)],
    BIBLE, ...FORMAT, ...CARDS],
  [['Hand-off', P.handoff], ['Details file', P.details], ['Working file', P.s8Work]])

const last = rounds[rounds.length - 1]
return {
  slug: brief.slug,
  phase: brief.phase,
  stopped: null,
  revisions: n - 1,
  rewrites,
  rounds,
  shippedClean: ships(last),
  agents,
  blueprint: BP,
  factCheck: FC,
  finalScript: P.script(r),
  finalAlternate: P.alt(r),
  lintReport: P.lintReport(r),
  tagged: P.tagged,
  lines: P.lines,
  handoff: P.handoff,
  details: P.details,
}
