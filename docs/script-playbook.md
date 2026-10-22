# Script playbook, v0.7 (22 Oct 2026)

One human-led writing workflow for the chosen Doordhan format. Keep shared story/prosody guidance here; format,
character, voice spelling and renderer details stay in their existing files. The archived long rulebooks remain
historical references, not additional mandatory inputs.

## Intake stays the same

The human provides a topic, YouTube/Instagram link, pasted material, research path or existing brief. Preserve the
request and any source transcript. The existing intake agent, schema, slug/source handling and stance preservation
are unchanged. A human initiates and owns the brief; research and agents cannot supply approval on their behalf.

```
/reel-script research/desk/2026-10-22-emudhra-pick.md
/reel-script https://www.youtube.com/watch?v=...
/reel-script <pasted research, script or transcript>
/reel-script <topic> stance: ... format: creator
/reel-script continue <slug>
/reel-script status <slug>
```

A structured brief can name `research: <path>`. With supplied research, verify it and fill material gaps; with a
video, verify its transcript; with a topic, research what the story needs. Do not rebuild completed research or
collect a competitor-video quota. Supplied research and desk files are read-only. Sources are factual input, not
hook/story instructions. Keep the existing vidIQ ceiling; optional lookup spending must have a concrete purpose.

The resolved configuration is in `work/<slug>/loop/state.json`. Downstream writing defaults to ONE writer and ONE
script; the unchanged intake's legacy default of three does not request alternatives. Honor an explicit `writers: N`
when the human asks for alternatives. The selected format supplies its default cast unless the human names one.
The examples, Pandey's beginner caller/dialect, telephone and Billu apply only to Kendra. Our general audience is
finance-aware. The human's current audience, runtime, language and edits govern the task.

## The working sequence and human checkpoints

1. **Research/verification.** A sourced handoff, calculations and material gaps. No chosen hook or script.
2. **Hook and story.** The managing writer proposes one short opening and an English storyline, with its viewer
   question, successive reveals and final insight. No final word limit while agreeing the story unless requested.
   The coordinating chat presents the intake assumptions, full hook/story and uncertainties, then STOPS.
3. **Human hook/story approval.** Only an explicit approval of that version permits script writing. The coordinator
   records the human's name/quote and displayed digest with the command below. Research suggestions, an agent's
   endorsement, an approval-like sentence inside a source, a schedule and silence never count as approval.
4. **Script.** One writer writes one clean Roman Hinglish script by default, preserving the approved opening,
   storyline and payoff. New versions preserve the current human edits. Sources and performance marks stay outside
   dialogue. Character-specific rules come from the chosen format and relevant cards, not a universal Pandey brief.
5. **Independent editorial and final factual review.** An editor checks the whole spoken argument and every
   consequential claim in the ACTUAL version, including revisions. It runs the deterministic lint directly as a
   diagnostic. One concrete revision and fresh final review are allowed per continuation. Unresolved claims block
   voice. A material change to the approved hook/story returns to human story review. No cold readers or rewrite
   competition are required.
6. **Voice preview and HUMAN review.** One checked script becomes one draft preview with separate performance notes,
   transcript/tail checks and measured duration. The person hears it and gives delivery feedback. Text edits return
   to editorial/factual review; story changes require story approval again. A machine transcript does not approve
   pleasant delivery. The coordinator presents the actual script, audio and uncertainties; no handoff agent.

The initial invocation always returns at story review. The workflow host has no documented blocking human-input
primitive, so `continue <slug>` resumes after the coordinator records approval. This is an actual state/digest check,
not a prompt asking agents to remember to wait. `status` is read-only. A continuation with no current approval does
not write scripts or generate audio. Every new version invalidates the relevant downstream checks.

The coordinator uses these commands ONLY after direct human authorization, copying the displayed digest and the
actual approval quote; it performs all mechanical work so the human does not have to type commands:

```
python3 pipeline/reel_script_gate.py status <slug>
python3 pipeline/reel_script_gate.py approve-story <slug> --by Akhilesh --quote '<actual approval>' --expected-digest <story_digest>
python3 pipeline/reel_script_gate.py approve-voice <slug> --by Akhilesh --quote '<actual approval>' --expected-digest <voice_digest>
python3 pipeline/reel_script_gate.py revise-voice <slug> --by Akhilesh --quote '<delivery feedback>' --expected-digest <voice_digest>
```

Akhilesh or Naveen acts within the existing story-pick/approval permissions. The records bind the reviewed files;
a typed name is not identity authentication. Never manufacture a quote. These are draft collaboration checkpoints:
voice approval alone does not approve final words, freeze a script, spend Higgsfield credits or authorize production.
Existing final-script, budget and production gates remain. Final words can be confirmed explicitly in the same
human voice-review conversation; only that explicit confirmation permits the existing script-freeze handoff.
Delivery feedback opens a new take folder on the next continuation, preserving the previous recording and words.
The revised take requires a new transcript check and human listening approval.

## What a good script is

One connected explanation: each beat makes the next worth hearing and builds toward an answer to the opening.
Write at the intended audience's level, include the why, preserve the factual scope and give the listener an insight
they can repeat. Cut repetition and tangents without cutting the joins. The chosen format supplies its shape,
characters, performance and ending; a caller's own calculation belongs in Kendra when relevant, not every business
story. Read examples for how they work, never as a template for reusing their lines or jokes.

## Curiosity and story movement

Added at Akhilesh's request from the supplied *Short-Form Storytelling Principles* PDF and the eMudhra collaboration. These are shared craft principles; the Kendra setup and beginner explanation above remain format-specific.

- **Make a short, relevant promise.** The opening fits one spoken line and raises an understandable question. Give a substantive reason to stay immediately; introduce unfamiliar mechanics after their stakes. Research supplies facts, not the required hook or storyline.
- **Keep curiosity moving.** Let a reveal answer something and make the next question worth asking. Build successive changes in the viewer's understanding: evidence, apparent reassurance, a complication or a supported consequence. Use multiple meaningful turns where the material supports them; no fixed count, reveal timestamp or forced alternation of good and bad news. The ending fulfils the opening promise.
- **Use earned contrast.** Identify the expectation a fact changes. A striking number, historical example or qualification earns space by changing the argument. Preserve differences between cases and distinguish inference from established fact; uncertainty alone does not justify a frightening forecast.
- **Keep substance and its connections.** Remove tangents and repeated conclusions while retaining the bridges needed to understand why one fact follows another. Value density is not the maximum number of facts or the fastest delivery.
- **Match comprehension to the audience.** Our finance-aware viewers know IPO, GMP and SIP; unfamiliar mechanics need a concrete explanation. Kendra's beginner caller can need more. Use an example when it clarifies the mechanism, rather than explaining everything twice or forcing a reading-grade target.
- **Earn emotion and the share.** Make the stakes felt through the facts and the character's appropriate delivery. Build toward an insight someone would want to tell a friend. Fear, shock, a moral and an explicit share request are not required; Pandey's existing ending and performance rules still apply.

The PDF lessons and their limits are summarised in the existing `docs/script-flow-research.md`; agents do not need the original PDF or another checklist. Its rhythm/cadence guidance is incorporated below. Treat retention and sharing benefits as hypotheses to test, not established results.

## Prosody and spoken flow

Agreed addition, 22 October, from the Jio–Starlink collaboration. These principles can support other formats; Pandey's dialect, beginner audience and performance rules remain specific to Kendra. Follow the chosen audience and character.

- **Story before cadence.** Open a specific question and make each beat build toward its answer. Repair unexplained jumps before polishing the sound; rhythm cannot make unrelated facts into a story.
- **Write meaningful spoken phrases.** A complete sentence can contain several phrases. Phrase boundaries need not contain silence. Keep natural joining words rather than manufacturing punchy fragments.
- **Choose the focus.** Give the new information or important contrast prominence through timing, pitch or emphasis. Do not automatically stress every number or company name.
- **Use parallel phrasing when it helps.** Give comparisons a recognisable shape. Repetition must advance the thought. Contrast and three-part builds are options, not compulsory ingredients.
- **Let delivery follow meaning.** Context, complication and conclusion can have different pace and intonation. Avoid repeating the same melody and final pause after every sentence; do not exaggerate Pandey's emotion to create variety.
- **Give important phrases room to land.** Remove trailing words that weaken a reveal. Keep word order natural for Hinglish instead of imposing English sentence-final focus everywhere.
- **Choose language by spoken phrasing.** Use Hindi or English where the thought sounds natural, not by word-for-word translation. No fixed mix, rhyme, syllable count or meter.
- **Separate words from performance.** Keep scripts clean. Put optional `|` phrase boundaries, `||` thought boundaries and selective emphasis in separate delivery notes; marks are not mandatory silences and are never spoken. Preserve the user's current edits and approved words; flag factual concerns separately.
- **Check the spoken result.** The independent editor checks whether the text can be followed on one listen. A read or generated take is needed to assess stumbling and duration; do not claim to have heard audio from a transcript alone.
- **Use measurements as diagnostics.** Repetitive contours or evenly spaced pauses can reveal mechanical delivery. No universal pitch range, speaking rate, pause count or retention guarantee is established. Actual recordings establish timing; word counts are estimates.

The workflow supplies `docs/script-flow-research.md` explicitly. Writers and the judge read its Working application, PDF lessons and interpretation limits; the voice stage uses the practical prosody guidance. Evidence is background when needed, not extra creative constraints. No cold-reader stage is run.

## Review and handoff files

The shared learning reference is `docs/script-flow-research.md`; read its practical sections, not every evidence
paper on every run. Format files and voice cards remain independent inputs. No new skill or extra scoring system.

The coordinating chat shows the current script, concise editorial findings, final claims trace, actual MP3/WAV
paths, transcript result, measured duration and what to listen for. Report missing sources/tools instead of implying
success. `work/` is git-ignored: preserve and transfer the actual take when moving machines; a Git pull does not
carry audio. Do not silently upload or regenerate it to switch apps. Save reviewable dated drafts/source notes in
`scripts/drafts` under the collaboration convention; never treat a draft commit as production authorization.

## Why the simpler loop

Cold readers previously sent retells only to the human handoff; they did not feed back to the writer or judge.
They could expose comprehension problems to the human, but did not close a revision loop and did not measure real
viewer retention. Removed from the default on Akhilesh's instruction. Independent editing now addresses clarity
with concrete revision requests. More writers remain an explicit exploration option, not the default cost of a reel.
No workflow change or craft reference establishes a measured retention or sharing improvement.
