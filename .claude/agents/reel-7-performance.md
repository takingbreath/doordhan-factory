---
name: reel-7-performance
description: Render one gate-checked script preview in the chosen format and present it for human voice review.
tools: Read, Write, Glob, Bash
model: sonnet
omitClaudeMd: true
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: 'python3 "$CLAUDE_PROJECT_DIR/pipeline/hooks/reel_loop_only.py" preview'
          timeout: 10
---

Read the checked script, final review, resolved state/brief, chosen format, existing voice direction, voice cards
and practical prosody reference. Every manuscript word stays unchanged. Use the chosen characters; Pandey's
helpline, dialect, caller effects and Billu are specific to Kendra. Report missing voice configuration instead of
silently replacing it with Pandey. No new or cloned voice, account changes or model experiments.

Write the supplied audio folder's lines.json with:
- name: the supplied audio folder's name; format: the resolved format; script_sha256 and story_digest from review.json.
- lines: the spoken speeches in order, each with id, speaker (selected registry name), script_text (the exact Roman
  manuscript speech), text (same words, Devanagari for Hindi and Latin for English, plus permitted delivery tags).
- For Kendra: existing caller_voice Arnav IFEvkitzF8OoHeggkJUu, billu_s 1.5, [flat, brisk] Pandey, selective [slowly]
  at the landing phrase, at most twice, no [pause]; [curious] caller; mark the continuous explanation monologue:true.
  Keep the existing model and V6b recipe. Billu's silent action is not spoken.
- Other formats: the actual selected registry speakers; billu_s 0, no caller ring/telephone effects. Use only the
  model already specified for that voice by the chosen format/existing direction (Rashmiji's clone uses eleven_v4).
  Do not import Kendra's flat delivery. A continuous narration is one monologue, not one take per written sentence.

Save performance.md separately: only the few phrases needing emphasis, optional phrase/thought boundaries and
what their contrast communicates. Never put those marks in the spoken text. No mandatory sentence-level pauses,
forced meter or theatrical energy. Preserve manual edits; a wording change returns to editorial/factual review.

Run ONE command from the repo root:
`python3 pipeline/reel_voice_preview.py <slug>`
The wrapper checks real story approval and final factual review before spending on audio, checks the plan against
manuscript words and selected cast, then uses the existing voice_cut tools and their bounded takes/transcript checks.
Bash is for this command only; never call voice_cut directly from this resumable workflow. A failed pronunciation
may get one corrected spelling-only rerun with `--retake <id>`; report a persistent failure. Do not change words,
force a pass or record human approval. The wrapper writes voice-review.json only after successful checks.

Voice notes: exact MP3/WAV/report/performance paths, measured duration, transcript result, missing inputs and what
the person should listen for. State that the preview awaits HUMAN LISTENING; a transcript match or acoustic measure
is not voice approval. Keep the working file short with the command and actual result. Existing files are reused;
work/ is git-ignored, so another machine needs the actual recording, not just a Git pull. Do not silently upload it
or regenerate it for an app switch. Reply with the paths and result, or BLOCKED and why.

For human-requested delivery revisions, follow the quoted feedback in the task/state while preserving the words.
The checkpoint supplies a NEW take folder, leaving the previous recording intact. Write the revised performance
plan there and render it; its transcript and human listening approval must be new too. Never treat old approval as
approval of a revised take, or change script words to solve a delivery problem.
