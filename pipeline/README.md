# Pipeline tools

Requirements: ffmpeg and ffprobe on PATH, Python 3.9+, numpy, pillow (`pip3 install -r requirements.txt`). Run tools from the repo root, e.g. `python3 pipeline/prep_line.py ...`.
Check the toolchain (no credits, no network): `python3 pipeline/self_test.py` → must end with ALL PASS.
Voices and transcripts go over the ElevenLabs API by default (2026-09-30). The ElevenLabs tools read ELEVENLABS_API_KEY from the environment or from the repo's git-ignored `.env`, and never print it. `python3 pipeline/tts_elevenlabs.py --check` confirms the key, the quota and that the default model is still offered.

Frames: the edit runs at 720x1280, 25 fps (Wan 720p delivers 718x1282); the 80s–90s CRT softness is added on purpose by look.py at the end. Mouth boxes and inset-box coordinates are always given in the 480x854 analysis frame, so numbers in formats/ and registry/ stay valid.

| Tool | Use |
|---|---|
| tts_elevenlabs.py | Generate a line with an ElevenLabs voice (`--voice sarika` from the registry, or `--voice-id`). `--check`, `--list`. Default model eleven_v3 (GA; Hindi; delivery tags). |
| prep_line.py | Clean a raw line: trim, tighten pauses, -16 LUFS (measured after tempo and limiter), tempo (1.15 anchors), `--phone` for callers. |
| make_track.py | Pad prepared lines into a whole-second track for one shot (upload this to Higgsfield). Says when a shorter hold saves a paid second. |
| put_upload.py | PUT a file to the presigned URL returned by Higgsfield media_upload (then call media_confirm). |
| qc.py | Every check on one talking shot, written to a notes file: format, speech_map, check_match, lipcheck, transcript vs script, loudness, contact sheet. |
| speech_map.py | Speech start/end/pauses of any file. Use on generated clips to choose cut points. |
| check_match.py | Did the generated clip keep our audio? Envelope correlation ≥0.90 = PASS (Wan). Low = re-voiced or re-timed. Reports a constant offset if there is one. |
| lipcheck.py | Mouth motion speaking vs silent, and mouth vs head while speaking. `--face-crop` saves a frame to find the mouth box. |
| headcheck.py | Head travel in px/s: a steady newsreader passes (≤45), a wobbling or tilting head fails. Tracks Sarika's bindi; phase correlation for others. `--mouth` takes the lipcheck box. |
| transcribe.py | ElevenLabs Scribe (scribe_v2): what was actually said, similarity to the script, and the last word's end time. Catches gibberish. |
| voice_reference.py | Real speech as a writing reference: Scribe on every clip in work/voices/audio/`<name>`/, one transcript per clip in docs/voices/`<name>`/reference/, Scribe's words kept as returned. Text-only (one sentence per line) or `--full` (speaker labels, pauses marked like `(0.4 s)`, a new line at 0.6 s or a change of speaker). `--rhythm` writes rhythm.md from chosen full-mode clips and speakers: words per second, sentence lengths, pauses. |
| contact_sheet.py | Frames at an fps or at given times, tiled into one image. |
| inset_card.py | `card`: logo card for the anchor's inset box. `overlay`: put it on a clip (auto-detects the box). |
| montage.py | Title card + the last N seconds of the sting (ending kept intact). |
| assemble.py | Edit list → final reel: each part levelled to -16 LUFS, old-TV look and TV-speaker sound, 1080x1920 at 25 fps, -14 LUFS, plus a joins contact sheet. |
| trends.py | News-desk trend meter: labels each candidate HOT, RISING, FLAT or COLD from Google Trends India, Google News momentum (today's share of the week) and YouTube this week (views, best views per hour). No login needed; vidIQ adds keyword and outlier data on top. |
| scoreboard.py | The strategy book's arithmetic (docs/strategy.md). `ingest-ig` records a vidIQ Instagram owner-insights reading, `link` ties a reel to its post, `add-reel` records a new episode with the bets it carries and its credits. With no argument it prints the report: each bet's value pooled over its reels against baseline, target and stop, and a verdict (TARGET HIT, STOP HIT, TIME STOP, HOLD). `brief` gives three lines on where we stand for sessions, and `status` the same in plain English for emails; `write` regenerates registry/performance.md and the book in docs/strategy.md. |
| deep_leads.py | The last 7 days of headlines from the deep-lane research sources (docs/sources.md), deduplicated and newest first. |
| sfx.py | The edit's sound-effect kit, synthesised locally into assets/audio/sfx_*.wav: whoosh, pop, ding, thud, record scratch, riser, stamp, office-fan room tone. |
| lipsync_lag.py | Mouth-to-voice offset of a talking shot, overall and in 2 s windows, so drift inside a line shows. SyncNet (primary) plus MediaPipe landmark correlation (fallback); FAIL if a confident window is outside -125..+45 ms (+ = sound leads). Labels the pattern: constant (prints the `audio_shift_ms` fix), drift (split the line) or weak lips (regenerate tighter). `--start/--end` for a segment of a finished reel, `--audio` to judge against another track. |
| verify_line.py | The voice step's gate (free): must-say numbers and terms (digits, Hindi number words, Devanagari and Latin normalised), no delivery tag spoken, last word intact and not hard-cut, no sound after the last word (prints where to trim), lead silence, and a running reel-length estimate against the cap. |
| script_lint.py | Deterministic checks on a loop script (no model, no network): `script_lint.py FORMAT MAIN [ALTERNATE ...]` reads the "### Lint table" in the format's section 0 and in each speaker's voice card, and writes `<script>-lint-fails.md` and `<script>-lint-report.md` next to the main script. Only fails decide the verdict. Exit 0 PASS, 1 FAIL, 2 when a table can't be read (no verdict). |
| voice_cut.py | One draft voice cut of a Sahayata Kendra script, the way work/cheat1/audio V6b was made: `voice_cut.py LINES.json OUT_DIR [--retake ID]`. Takes with an [exhales] ending, the slowest clean take of the monologue, a Scribe and verify_line check on every take, the ring, the landline caller, the clack, a silence for Billu, then Scribe on the whole cut against the script; writes report.md. The script loop's voice step runs it (hooks/voice_only.py lets it run nothing else). |
| stub_reel_script.mjs | `node pipeline/stub_reel_script.mjs`: the script loop's workflow (.claude/workflows/reel-script.js) end to end with fake agents, no model or network; checks every read exists when it is read and the run folder holds the expected files. self_test runs it. |
| script_freeze.py / script_diff.py | Freeze the approved script at the gate (registry/scripts/<slug>.json, sha256, re-approval needed to change it); diff the final's transcript against it: DROPPED, CHANGED (a missing run of 3+ words) or NUMBER lines fail, EXTRA flags unscripted speech. |
| preflight_keyframe.py | A talking keyframe before video: face and mouth size, head pose, closed mouth, per-character checks (Pandey: heavy lids), OCR on a board or logo. |
| face_consistency.py | Same character? AuraFace embedding similarity against the character sheet, worst frame of a clip counts. PASS >= 0.55 (same character 0.66-0.93, different 0.10-0.34 in our episodes). |
| qc_gate.py | The hard gate on every assembled final: script diff, lip-sync per talking segment, face vs character sheet, line end/tail/lead in the mix, loudness, length, in that order. Repairs a constant offset, a hard-cut line end and a wrong lead once (repairs file, rebuild, re-check); blocks on anything else with the clip and the fix. Writes the stamp `<final>.qc.json` and the one-screen `<final>_qc.png`. `bind-transcript` records Scribe's text for the exact audio; `waive` records Akhilesh's say-so on one row. |
| qc_stamp.py | Is this final stamped? Used by the SendUserFile hook (hooks/require_qc_stamp.py) and put_upload.py: a video under outputs/ leaves the machine only with a PASS stamp covering that exact file. |
| vhs_motion.py | The tape's movement, without its colour: line jitter, head-switching tear, colour bleed, streak noise and dropouts, at 0.65 by default. assemble.py runs it before the look. |
| voice_room.py | The voice in the room: 120 Hz–7 kHz, light tape saturation, a small office room (no hiss). assemble.py applies it per part (`"room": false` to skip one); builds can call `treat()` on a dialogue bus. |
| ambience.py | Recorded CC0 room ambience (fan plus distant road, assets/audio/ambience) under the reel. assemble.py adds it at `"ambience_db"` (default −36) relative to the programme; `"ambience": null` for none. |
| shot_spec.py | `build`: a voice line -> Wan talking-shot specs with the defaults (tail trim, 6 s cap split, 0.5 s lead, still start, headroom). `judge`: accept / accept with an audio shift / one automatic retry / ask. |
| fetch_models.sh | Installs the QC models and packages (MediaPipe Face Landmarker, AuraFace, SyncNet, tesseract): run once per fresh machine. |
| look.py | The old-TV picture (presets broadcast, vhs, kendra, clean). `look.py CLIP OUT --preset vhs` previews it on one clip and writes a before/after frame. |

`fixtures/` holds a real 3-second Sarika line that the self-test uses; synthetic tones hid a levelling bug that real speech exposed.
