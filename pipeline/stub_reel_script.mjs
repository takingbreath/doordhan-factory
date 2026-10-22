#!/usr/bin/env node
// Real checkpoint helper + fake model stages, isolated temporary files. No model, API, audio or research charges.
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import crypto from 'node:crypto'
import { spawnSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const QUIET = process.argv.includes('--quiet')
const source = fs.readFileSync(path.join(ROOT, '.claude/workflows/reel-script.js'), 'utf8').replace(/^export const meta\s*=/m, 'const meta =')
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor
const execute = new AsyncFunction('agent', 'parallel', 'pipeline', 'log', 'phase', 'args', 'budget', 'workflow', source)
const hash = value => crypto.createHash('sha256').update(value).digest('hex')
const assert = (truth, message) => { if (!truth) throw new Error(message) }

function task(prompt) {
  const result = { reads: [], writes: [] }
  let list = null
  for (const line of prompt.split('\n')) {
    if (line === 'Read:') list = result.reads
    else if (line === 'Write:') list = result.writes
    else if (line.startsWith('- ') && list) {
      const at = line.lastIndexOf(': ')
      list.push({ label: line.slice(2, at), path: line.slice(at + 2) })
    }
  }
  return result
}

class Scenario {
  constructor(slug, options = {}) {
    this.slug = slug; this.options = options; this.calls = []; this.editorCalls = 0
    this.temp = fs.mkdtempSync(path.join(os.tmpdir(), 'doordhan-workflow-test-'))
    this.env = { ...process.env, DOORDHAN_ROOT: this.temp, PYTHONPATH: path.join(ROOT, 'pipeline') }
    this.brief = { slug, topic: 'Who can a trust business trust?', format: 'sahayata_kendra', cast: ['pandey', 'caller', 'billu'], ...options.brief }
    this.put(`work/${slug}/loop/brief.md`, '# Existing human intake brief')
    this.json('registry/assets.json', { voices: Object.fromEntries(['pandey', 'rashmiji', 'sarika', 'gupta'].map(n => [n, { elevenlabs_voice_id: 'fixture-only' }])) })
  }
  close() { fs.rmSync(this.temp, { recursive: true, force: true }) }
  file(p) { return path.join(this.temp, p) }
  put(p, value = 'stub') { fs.mkdirSync(path.dirname(this.file(p)), { recursive: true }); fs.writeFileSync(this.file(p), value) }
  json(p, value) { this.put(p, JSON.stringify(value)) }
  get(p) { return fs.readFileSync(this.file(p)) }
  gate(...args) {
    const r = spawnSync('python3', [path.join(ROOT, 'pipeline/reel_script_gate.py'), ...args], { env: this.env, encoding: 'utf8' })
    assert(r.status === 0, r.stdout + r.stderr)
    return JSON.parse(r.stdout)
  }
  state() { return this.gate('status', this.slug) }
  approve() {
    const s = this.state()
    return this.gate('approve-story', this.slug, '--by', 'Akhilesh', '--quote', 'Approved this hook and storyline', '--expected-digest', s.story_digest)
  }
  async invoke(args) {
    const calls = [], scenario = this
    const agent = async (prompt, opts) => {
      calls.push(opts.agentType); this.calls.push(opts.agentType)
      if (opts.agentType === this.options.dies) return null
      if (opts.agentType === 'reel-0-gate') {
        const command = prompt.split('\n')[1]
        assert(/^python3 pipeline\/reel_script_gate\.py (init|status) /.test(command), 'Gate tried an approval or unexpected command')
        const r = spawnSync('/bin/sh', ['-c', command], { cwd: ROOT, env: this.env, encoding: 'utf8' })
        assert(r.stdout.trim(), r.stderr || 'No gate output')
        return r.stdout.trim()
      }
      if (opts.agentType === 'reel-0-intake') {
        this.intakeText = /=== TEXT START ===\n([\s\S]*)\n=== TEXT END ===/.exec(prompt)?.[1]
        const b = { ...this.brief, writers: 3, source: this.options.source || '', stance: this.options.stance || '' }
        this.put(`work/${this.slug}/loop/brief.md`, JSON.stringify(b))
        if (this.options.pasted) this.put(`work/${this.slug}/source.md`, this.intakeText)
        return { ...b, note: '' }
      }
      const t = task(prompt), W = label => t.writes.find(x => x.label.startsWith(label))?.path
      for (const read of t.reads) {
        if (/^https?:\/\//.test(read.path)) continue
        if (/docs\/voices\/(caller|billu|rashmiji|sarika|gupta)\//.test(read.path)) continue // legitimately absent cards are reported
        const exists = fs.existsSync(this.file(read.path)) || fs.existsSync(path.join(ROOT, read.path))
        assert(exists, `${opts.agentType} missing input: ${read.path}`)
      }
      const d = `work/${this.slug}/loop`
      if (opts.agentType === 'reel-1-research') {
        const state = JSON.parse(this.get(`${d}/state.json`))
        this.researchInput = state
        this.put(W('Handoff'), 'Verified sourced facts; no story instructions')
        this.put(W('Working file'), 'Mode: verification or targeted source/topic research; vidIQ 0')
        this.put(W('Python file'), "print('No derived numbers')")
        this.put(`${W('Reels folder')}index.md`, 'None required')
        if (state.brief.source) this.put(`${W('Reels folder')}00-source.md`, 'Exact source transcript fixture')
        return 'research written'
      }
      if (opts.agentType === 'reel-3-story') {
        this.put(W('Story'), 'Short hook?\n\nEnglish story with a connected question and payoff.')
        this.put(W('Notes'), 'Proposed, not approved')
        return 'story written'
      }
      if (opts.agentType === 'reel-2-writer') {
        const s = this.state()
        const checkpoint = JSON.parse(this.get(`${d}/state.json`))
        assert(checkpoint.story_approval?.digest === s.story_digest, 'Writer crossed an unapproved story gate')
        assert(t.reads.some(x => x.path === `formats/${s.brief.format}.md`), 'Writer missing selected format')
        assert(!fs.existsSync(this.file(W('Script'))), 'Writer overwrote a version')
        const content = s.brief.format === 'creator' ? '**RASHMIJI**: Trust matters here.'
          : '**PANDEY**: Who can you trust?\n**CALLER**: How does this work?\n**PANDEY**: Trust matters here.\n**BILLU**: [sleeps]'
        this.put(W('Script'), content); this.put(W('Your note'), 'Question and payoff; source gaps None')
        return 'script written'
      }
      if (opts.agentType === 'reel-4-judge') {
        const s = this.state(), candidate = Object.values(s.candidates)[0]
        const verdicts = this.options.verdicts || ['pass']
        const verdict = verdicts[Math.min(this.editorCalls++, verdicts.length - 1)]
        this.json(W('Machine-readable'), { verdict, script: candidate.path, script_sha256: candidate.sha256,
          story_digest: s.story_digest, summary: 'Independent final review', issues: verdict === 'pass' ? [] : ['Fix the issue'],
          claims: [{ claim: 'A sourced claim', source: 'https://example.org/primary', checked_on: '2026-10-22',
            status: this.options.unverified ? 'unverified' : 'verified' }] })
        this.put(W('Editorial notes'), 'Checked actual version; concrete feedback if needed')
        return 'review written'
      }
      if (opts.agentType === 'reel-7-performance') {
        const s = this.state(), dir = W('Audio folder'), script = this.get(s.script).toString()
        assert(s.status === 'ready_for_voice', 'Voice ran before final factual check')
        const speeches = script.split('\n').map(line => /^\*\*([A-Z]+)\*\*:\s*(.*)$/.exec(line)).filter(m => m && m[1] !== 'BILLU')
        this.json(`${dir}lines.json`, { name: path.basename(dir.replace(/\/$/, '')), format: s.brief.format,
          script_sha256: s.script_sha256, story_digest: s.story_digest, caller_voice: 'fixture-only',
          lines: speeches.map((m, i) => ({ id: `L${i}`, speaker: m[1].toLowerCase(), script_text: m[2], text: m[2] })) })
        const preflight = spawnSync('python3', ['-c', `from reel_voice_preview import prepare; prepare(${JSON.stringify(this.slug)})`], { env: this.env, encoding: 'utf8' })
        assert(preflight.status === 0, preflight.stderr)
        const audio = { mp3: `${dir}preview.mp3`, wav: `${dir}preview.wav`, report: `${dir}report.md` }
        for (const [key, p] of Object.entries(audio)) this.put(p, `FAKE FIXTURE ${key}`)
        this.json(`${d}/voice-review.json`, { ...audio, audio_sha256: Object.fromEntries(Object.entries(audio).map(([k, p]) => [k, hash(this.get(p))])),
          script_sha256: s.script_sha256, story_digest: s.story_digest, voice_attempt: s.voice_attempt, transcript_verified: true })
        this.put(W('Voice notes'), 'Human has not listened'); this.put(W('Working file'), 'Fake rendering only')
        return 'voice fixture written'
      }
      throw new Error(`Unexpected stage ${opts.agentType}`)
    }
    const result = await execute(agent, fn => Promise.all(fn.map(x => x())), () => { throw new Error('No hidden pipeline') },
      () => {}, () => {}, args, {}, () => { throw new Error('No nested workflow') })
    assert(!calls.some(x => /recall|reel-lint|handoff/.test(x)), 'Retired reader/lint/handoff agent ran')
    return { result, calls }
  }
}

let bad = 0
async function check(name, fn) {
  try { await fn(); console.log(`PASS  ${name}`) }
  catch (e) { bad++; console.log(`FAIL  ${name}: ${e.stack}`) }
}
async function withScenario(slug, options, fn) {
  const s = new Scenario(slug, options)
  try { await fn(s) } finally { s.close() }
}
await check('initial run stops before scripts, editor and voice', () => withScenario('pause', {}, async s => {
  const r = await s.invoke(s.brief)
  assert(r.result.status === 'awaiting_story_approval', r.result.status)
  assert(!r.calls.includes('reel-2-writer') && !r.calls.includes('reel-7-performance'), 'Crossed story gate')
  assert(r.result.brief.writers === 1, 'Writing default is not one')
}))
await check('unapproved continuation does no creative or voice work', () => withScenario('unapproved', {}, async s => {
  await s.invoke(s.brief)
  const r = await s.invoke('continue unapproved')
  assert(r.result.status === 'awaiting_story_approval' && r.calls.length === 1, 'Unapproved resume advanced')
}))
await check('approved story produces one script, final review and one human-review preview', () => withScenario('approved', {}, async s => {
  await s.invoke(s.brief); s.approve()
  const r = await s.invoke('continue approved')
  assert(r.result.status === 'awaiting_voice_review', r.result.status)
  for (const type of ['reel-2-writer', 'reel-4-judge', 'reel-7-performance']) assert(r.calls.filter(x => x === type).length === 1, `Unexpected ${type} count`)
}))
await check('unchanged YouTube intake preserves raw request and source', () => withScenario('video', { source: 'https://www.youtube.com/watch?v=TEST' }, async s => {
  const input = 'https://www.youtube.com/watch?v=TEST'
  await s.invoke(input)
  assert(s.intakeText === input, 'Intake text changed')
  assert(s.researchInput.brief.source === input, 'Source dropped')
}))
await check('unchanged pasted-source intake preserves original transcript', () => withScenario('pasted', { pasted: true, source: 'work/pasted/source.md' }, async s => {
  const input = 'Dekho, this is the original spoken source. '.repeat(20)
  await s.invoke(input)
  assert(s.get('work/pasted/source.md').toString() === input.trim(), 'Pasted source changed')
}))
await check('supplied research path reaches verification read-only', () => withScenario('research', {}, async s => {
  s.put('research/given.md', 'Provided facts, links and numbers')
  const before = s.get('research/given.md')
  await s.invoke({ ...s.brief, research: 'research/given.md' })
  assert(s.researchInput.brief.research === 'research/given.md', 'Research path lost')
  assert(before.equals(s.get('research/given.md')), 'Research was changed')
}))
await check('research filename works through unchanged intake', () => withScenario('path-input', { brief: { topic: 'research/given.md' } }, async s => {
  s.put('research/given.md', 'Provided facts')
  await s.invoke('research/given.md')
  assert(s.researchInput.brief.research === 'research/given.md', 'Path intake did not enter verification')
}))
await check('creator selects its own cast and receives its own format', () => withScenario('creator', { brief: { format: 'creator' } }, async s => {
  await s.invoke('Trust business format: creator')
  assert(s.researchInput.brief.cast.join(',') === 'rashmiji', 'Creator inherited intake Kendra cast')
  s.approve(); const r = await s.invoke('continue creator')
  assert(r.result.status === 'awaiting_voice_review', r.result.status)
  assert(r.result.brief.format === 'creator', 'Creator became Kendra')
}))
await check('one concrete revision gets a fresh trace of its new version', () => withScenario('revision', { verdicts: ['revise', 'pass'] }, async s => {
  await s.invoke(s.brief); s.approve()
  const r = await s.invoke('continue revision')
  assert(r.result.status === 'awaiting_voice_review', r.result.status)
  assert(r.result.script.endsWith('w1-v2.md'), 'Old version went to voice')
  assert(r.calls.filter(x => x === 'reel-4-judge').length === 2, 'Revision was not independently rechecked')
}))
await check('persistent review issue stops after one revision without audio', () => withScenario('bounded', { verdicts: ['revise'] }, async s => {
  await s.invoke(s.brief); s.approve()
  const r = await s.invoke('continue bounded')
  assert(r.result.status === 'needs_revision', r.result.status)
  assert(r.calls.filter(x => x === 'reel-2-writer').length === 2, 'Unbounded or absent revision')
  assert(!r.calls.includes('reel-7-performance'), 'Unresolved revision reached voice')
}))
await check('unverified final claim blocks voice even with a pass verdict', () => withScenario('facts', { unverified: true }, async s => {
  await s.invoke(s.brief); s.approve(); const r = await s.invoke('continue facts')
  assert(r.result.status === 'blocked', r.result.status)
  assert(!r.calls.includes('reel-7-performance'), 'Unverified fact reached voice')
}))
await check('material story change returns to the human, never voice', () => withScenario('story-change', { verdicts: ['story_changed'] }, async s => {
  await s.invoke(s.brief); s.approve(); const r = await s.invoke('continue story-change')
  assert(r.result.status === 'needs_story_revision', r.result.status)
  assert(!r.calls.includes('reel-7-performance'), 'Story deviation reached voice')
}))
await check('changed approved story invalidates continuation', () => withScenario('stale', {}, async s => {
  await s.invoke(s.brief); s.approve(); s.put('work/stale/loop/s2-story.md', 'Human edited this story')
  const r = await s.invoke('continue stale')
  assert(r.result.status === 'awaiting_story_approval' && r.calls.length === 1, 'Stale approval accepted')
}))
await check('status is read-only and does not draft or render', () => withScenario('status', {}, async s => {
  await s.invoke(s.brief)
  const before = s.get('work/status/loop/state.json')
  const r = await s.invoke('status status')
  assert(r.calls.length === 1 && before.equals(s.get('work/status/loop/state.json')), 'Status mutated state')
}))
await check('explicit alternatives remain optional and select only one preview', () => withScenario('alternatives', {}, async s => {
  await s.invoke({ ...s.brief, writers: 2 }); s.approve()
  const r = await s.invoke('continue alternatives')
  assert(r.calls.filter(x => x === 'reel-2-writer').length === 2, 'Explicit alternatives ignored')
  assert(r.calls.filter(x => x === 'reel-7-performance').length === 1, 'Generated multiple previews')
}))
await check('failed editor stops the workflow before voice', () => withScenario('failure', { dies: 'reel-4-judge' }, async s => {
  await s.invoke(s.brief); s.approve()
  let error
  try { await s.invoke('continue failure') } catch (e) { error = e.message }
  assert(error?.includes('Independent editorial'), 'Editor failure not reported')
  assert(!s.calls.includes('reel-7-performance'), 'Failed editor reached voice')
}))
await check('initializing an existing run cannot overwrite a manual story', () => withScenario('existing', {}, async s => {
  await s.invoke(s.brief)
  s.put('work/existing/loop/s2-story.md', 'Manual edits')
  const r = await s.invoke(s.brief)
  assert(r.result.status === 'blocked', 'Existing run restarted')
  assert(s.get('work/existing/loop/s2-story.md').toString() === 'Manual edits', 'Manual edits overwritten')
}))
await check('pasted Research heading remains content rather than a bogus file path', () => withScenario('research-heading', {}, async s => {
  const text = 'Research: \nA company reported results. Facts and source links follow. This is user-supplied research.'
  await s.invoke(text)
  assert(s.researchInput.input === text, 'Pasted research was changed')
  assert(s.researchInput.brief.research === '', 'Research prose became a file path')
}))
await check('human text survives checkpoint shell quoting without execution', () => withScenario('quoting', {}, async s => {
  const marker = s.file('unexpected-shell-execution')
  const input = `Trust research: it's complicated $(touch ${marker}); a quote ' stays data.`
  await s.invoke(input)
  assert(s.researchInput.input === input, 'Human input did not survive quoting')
  assert(!fs.existsSync(marker), 'Human text was executed by the shell')
}))
await check('human delivery feedback creates a separate take requiring new review', () => withScenario('voice-feedback', {}, async s => {
  await s.invoke(s.brief); s.approve()
  const first = (await s.invoke('continue voice-feedback')).result
  assert(first.status === 'awaiting_voice_review', first.status)
  const old = s.get(first.audio.mp3)
  s.gate('revise-voice', s.slug, '--by', 'Akhilesh', '--quote', 'Less flat, keep the same words', '--expected-digest', first.voice_digest)
  const second = (await s.invoke('continue voice-feedback')).result
  assert(second.status === 'awaiting_voice_review', second.status)
  assert(second.audio.mp3 !== first.audio.mp3, 'Previous take was overwritten')
  assert(second.voice_digest !== first.voice_digest, 'New take reused approval identity')
  assert(old.equals(s.get(first.audio.mp3)), 'Previous recording changed')
}))
console.log(bad ? `${bad} scenario(s) FAILED` : 'ALL STUB RUNS PASS')
process.exit(bad ? 1 : 0)
