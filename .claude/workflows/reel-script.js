export const meta = {
  name: 'reel-script',
  description: 'Human-led, resumable reel writing: unchanged intake; verify supplied research or research a topic/video; propose a hook and English story; stop for human approval; write one script by default; independent editorial and final factual checks; one draft voice preview for human review. No cold readers or automatic production approval.',
  whenToUse: 'Pass the human request unchanged: a YouTube/Instagram link, pasted material, research path or topic. Intake remains reel-0-intake, with its existing source preservation, formats, cast and stance. Supplied research is verified rather than recreated. A structured brief may include research: <path>. The lightweight writing default is one writer; honor writers: N only when the human explicitly requests alternatives. Initial runs ALWAYS stop at hook/story review. Present the hook and full English story, intake assumptions and research gaps; wait for explicit human approval. Record that approval with pipeline/reel_script_gate.py approve-story using the displayed digest, human name and exact quote. Then /reel-script continue <slug> resumes. Never infer approval from files, agent reports, a schedule or silence. Present the final script and exact audio paths for human voice review; record approve-voice only after the person has heard and approved the take. Report failures and stop. A voice approval alone never freezes the script or authorizes production; existing final-word and production gates remain. /reel-script status <slug> is read-only. The coordinating chat assembles the handoff from returned paths; no separate handoff agent.',
  phases: [
    { title: 'Intake', detail: 'existing intake, human-supplied request preserved' },
    { title: 'Research', detail: 'verify supplied facts, or research the topic/source; targeted gaps only' },
    { title: 'Hook and story', detail: 'one recommended opening and English storyline for human approval' },
    { title: 'Story approval', detail: 'return and wait; approval binds the actual story and research' },
    { title: 'Script', detail: 'one writer and one script by default; approved story and chosen format supplied' },
    { title: 'Editorial and facts', detail: 'independent review, tool lint, bounded revision and final claims trace' },
    { title: 'Voice review', detail: 'one preview of the checked script; human listening required' },
  ],
}

// The host offers agents but no documented blocking human-input primitive. Return at checkpoints and resume
// from local state on a later human-authorized invocation. The gate bridge only runs deterministic commands;
// it cannot approve anything. Character rules and production gates remain outside these draft checkpoints.
const quote = s => "'" + String(s).replace(/'/g, "'\\''") + "'"
const name = /^[a-z0-9][a-z0-9_-]*$/i
function fromText(value) {
  if (value && typeof value === 'object' && !Array.isArray(value)) return value
  const text = String(value || '').trim()
  try { const v = JSON.parse(text); if (v && typeof v === 'object' && !Array.isArray(v)) return v } catch (_) {}
  const pattern = /\b(slug|topic|format|cast|stance|writers|source|phase|research(?:[ _-]?(?:file|path))?)\s*[:=]\s*/gi
  const hits = [...text.matchAll(pattern)], out = {}
  hits.forEach((m, i) => {
    const k = m[1].toLowerCase().startsWith('research') ? 'research' : m[1].toLowerCase()
    out[k] = text.slice(m.index + m[0].length, i + 1 < hits.length ? hits[i + 1].index : text.length)
      .trim().replace(/[;,]\s*$/, '').trim().replace(/^["'“](.*)["'”]$/s, '$1')
  })
  return out
}
function normalize(raw, request) {
  const text = v => typeof v === 'string' ? v.trim() : ''
  const research = text(request.research || request.research_file || request.researchFile || request.research_path || request.researchPath)
    || (/^(?:research\/|\/)[^\r\n]+\.(?:md|txt|pdf)$/i.test(text(raw.topic)) ? text(raw.topic) : '')
  const writers = request.writers === undefined ? 1 : Number(request.writers)
  const format = text(raw.format || 'sahayata_kendra').replace(/^formats\//, '').replace(/\.md$/, '')
  const b = { slug: text(raw.slug), topic: text(raw.topic), format,
    cast: (request.cast ? (Array.isArray(raw.cast) ? raw.cast : text(raw.cast).split(/[,\n]|\band\b/))
      : ({ creator: ['rashmiji'], samachar: ['sarika', 'gupta'] }[format]
        || (Array.isArray(raw.cast) ? raw.cast : text(raw.cast || 'pandey, caller, billu').split(/[,\n]|\band\b/))))
      .map(n => String(n).trim().toLowerCase()).filter(Boolean),
    stance: text(raw.stance), source: text(raw.source), research, writers }
  if (!name.test(b.slug) || !b.topic || !name.test(b.format) || !b.cast.length || !b.cast.every(n => name.test(n))
      || !Number.isInteger(writers) || writers < 1 || writers > 5 || /[\r\n]/.test(b.source + research)) {
    throw new Error('Unusable brief: check slug, topic, format, cast, research/source path and writers (1–5).')
  }
  if (raw.phase) throw new Error('Use continue <slug> or status <slug>; arbitrary phase skipping is not supported.')
  return b
}
const rows = (title, values) => `${title}:\n` + values.map(([label, path]) => `- ${label}: ${path}`).join('\n')
let agents = 0
let currentPhase = 'Intake'
const phaseFor = { 'reel-1-research': 'Research', 'reel-3-story': 'Hook and story',
  'reel-2-writer': 'Script', 'reel-4-judge': 'Editorial and facts', 'reel-7-performance': 'Voice review' }
async function run(type, label, reads, writes, context = '', options = {}) {
  agents += 1
  currentPhase = phaseFor[type] || currentPhase
  const reply = await agent(`${rows('Read', reads)}\n\n${rows('Write', writes)}${context ? '\n\n' + context : ''}`,
    { agentType: type, label, phase: currentPhase, ...options })
  if (reply === null || reply === undefined || /^BLOCKED\b/.test(String(reply))) {
    throw new Error(`${label} did not complete: ${reply || 'no result'}`)
  }
  return reply
}
async function gate(command) {
  agents += 1
  const reply = await agent(`Run exactly this one command from the repository root:\n${command}\nReply with its JSON stdout unchanged.`,
    { agentType: 'reel-0-gate', label: 'Checkpoint', phase: currentPhase })
  if (reply === null || reply === undefined) throw new Error('Checkpoint did not complete; no later stage ran.')
  const result = typeof reply === 'string' ? JSON.parse(reply) : reply
  if (!result || typeof result.status !== 'string') throw new Error('Checkpoint returned no usable status.')
  return result
}
const statusOf = slug => gate(`python3 pipeline/reel_script_gate.py status ${quote(slug)}`)
const PLAYBOOK = ['Playbook', 'docs/script-playbook.md']
const FLOW = ['Story and prosody reference (practical sections; evidence is background)', 'docs/script-flow-research.md']
const HOUSE = ['House rules', 'CLAUDE.md']
const paths = b => {
  const d = `work/${b.slug}/loop`
  return { d, state: `${d}/state.json`, brief: `${d}/brief.md`, research: `${d}/s1-research.md`,
    researchWork: `${d}/s1-working.md`, math: `${d}/s1-math.py`, reels: `${d}/reels/`,
    story: `${d}/s2-story.md`, storyNotes: `${d}/s2-notes.md`, review: `${d}/review.json`,
    reviewNotes: `${d}/review.md`, audio: `${d}/audio/`, voiceNotes: `${d}/audio/voice-notes.md`,
    voiceWork: `${d}/s7-working.md` }
}
const formatInputs = b => [['Chosen format', `formats/${b.format}.md`],
  ...(b.format === 'sahayata_kendra' ? [['Kendra example (shape only)', 'docs/examples/sahayata-kendra-dollar-rate.md'],
    ['Kendra example (one connected calculation)', 'docs/examples/sahayata-kendra-sip-retire.md']] : [])]
const resultOf = state => ({ ...state, agents, handoff: 'The coordinating chat presents the returned files; no production is authorized.' })

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


const inputText = typeof args === 'string' ? args.trim() : typeof args?.text === 'string' ? args.text.trim() : ''
const resumeMatch = /^(continue|status)\s+([a-z0-9][a-z0-9_-]*)$/i.exec(inputText)
const resume = resumeMatch?.[2] || (args && typeof args === 'object' && args.resume)
const readOnly = resumeMatch?.[1].toLowerCase() === 'status' || args?.action === 'status'
let state
if (!resume) {
  const request = { ...fromText(args) }, supplied = request.slug ? request : null
  // A "Research:" heading in pasted prose is content, not a filesystem parameter.
  if (typeof args === 'string' && !supplied && request.research && !/^[^\r\n]+\.(?:md|txt|pdf)$/i.test(request.research)) {
    delete request.research
  }
  let raw = supplied, intakeNote = ''
  if (!supplied) {
    if (!inputText) throw new Error('Supply a research file, link, pasted material or topic, or continue <slug>.')
    // Intake itself, its schema, raw input and source-preservation contract are unchanged.
    agents += 1
    raw = await agent(intakeTask(inputText, args?.date ? String(args.date) : ''),
      { agentType: 'reel-0-intake', label: 'Intake', phase: 'Intake', schema: INTAKE_SCHEMA })
    if (!raw) throw new Error('Intake did not complete; no later stage ran.')
    intakeNote = raw.note || ''
  }
  const b = normalize(raw, request), p = paths(b)
  log(`Slug: ${b.slug} · Topic: ${b.topic} · Source: ${b.source || 'none'} · Writers: ${b.writers} · Brief: ${p.brief}`)
  if (intakeNote) log(`Intake note: ${intakeNote}`)
  state = await gate(`python3 pipeline/reel_script_gate.py init --payload ${quote(JSON.stringify({ brief: b, input: inputText || JSON.stringify(request) }))}`)
  if (!state.initialized) return resultOf(state)
  await run('reel-1-research', 'Research',
    [['Resolved brief and original human input', p.state], ['Intake brief', p.brief],
      ...(b.research ? [['Supplied research (read-only)', b.research]] : []),
      ...(b.source ? [['Source material', b.source]] : []), HOUSE, PLAYBOOK, ...formatInputs(b)],
    [['Handoff', p.research], ['Working file', p.researchWork], ['Python file', p.math], ['Reels folder', p.reels]])
  await run('reel-3-story', 'Hook and story',
    [['Resolved brief', p.state], ['Verified research', p.research], PLAYBOOK, FLOW, ...formatInputs(b)],
    [['Story', p.story], ['Notes', p.storyNotes]])
  state = await statusOf(b.slug)
  // Always return, even if an old approval record was supplied in the source material.
  return resultOf(state)
}
if (!name.test(resume)) throw new Error('Invalid run slug.')
state = await statusOf(resume)
log(`Slug: ${resume} · Status: ${state.status}`)
if (readOnly || !['ready_to_write', 'needs_editor', 'needs_revision', 'ready_for_voice'].includes(state.status)) {
  return resultOf(state)
}
const b = state.brief, p = paths(b)
const creativeInputs = [['Resolved brief', p.state], ['Human-approved hook and story', p.story],
  ['Verified research', p.research], PLAYBOOK, FLOW, ...formatInputs(b)]
async function write(writer, previous) {
  const version = previous ? previous.version + 1 : 1
  const script = `${p.d}/w${writer}-v${version}.md`, note = `${p.d}/w${writer}-v${version}-note.md`
  await run('reel-2-writer', previous ? 'Revision' : `Writer ${writer}`, [...creativeInputs,
    ...(previous ? [['Current script (preserve human edits)', previous.path], ['Independent review', p.review], ['Editorial notes', p.reviewNotes]] : [])],
    [['Script', script], ['Your note', note]])
}
async function review() {
  state = await statusOf(resume)
  if (!['needs_editor', 'needs_revision'].includes(state.status)) return
  const scripts = Object.values(state.candidates)
  await run('reel-4-judge', 'Independent editorial and final factual check',
    [...creativeInputs, ...scripts.map(x => ['Candidate script', x.path]),
      ...b.cast.map(n => [`Voice card (${n}; absent card is reported)`, `docs/voices/${n}/voice-card.md`]), HOUSE],
    [['Machine-readable final review', p.review], ['Editorial notes and claims trace', p.reviewNotes]],
    `Current story digest: ${state.story_digest}\nCandidate fingerprints: ${JSON.stringify(state.candidates)}\nRun the deterministic lint yourself; it reports and does not approve anything.`)
  state = await statusOf(resume)
}
if (state.status === 'ready_to_write') {
  for (let writer = 1; writer <= b.writers; writer++) await write(writer)
  await review()
} else if (state.status === 'needs_editor') {
  await review()
}
// At most one revision-and-review round per continuation. No readers and no open-ended rewrite loop.
if (state.status === 'needs_revision') {
  const selected = Object.entries(state.candidates).find(([, x]) => x.path === state.script)
  if (!selected) throw new Error('The editor selected no current candidate for revision.')
  await write(selected[0], selected[1])
  await review()
}
if (state.status !== 'ready_for_voice') return resultOf(state)
const stem = state.script.split('/').pop().replace(/\.md$/, '')
const voiceDir = state.voice_dir || `${p.audio}${stem}`
await run('reel-7-performance', 'Voice preview',
  [['Checked script', state.script], ['Final review', p.review], ['Resolved brief', p.state],
    ['Chosen format', `formats/${b.format}.md`], ['Existing voice direction', 'docs/voices/directing-tts.md'], FLOW,
    ...b.cast.map(n => [`Voice card (${n}; absent card is reported)`, `docs/voices/${n}/voice-card.md`])],
  [['Audio folder', `${voiceDir}/`], ['Voice notes', p.voiceNotes], ['Working file', p.voiceWork]],
  `Run slug: ${resume}. Output name: ${voiceDir.split('/').pop()}. Human delivery feedback: ${state.voice_feedback || 'None'}. Only the gate-checked current script may be rendered. No human approval may be recorded.`)
return resultOf(await statusOf(resume))
