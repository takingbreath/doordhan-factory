# Pipeline tools

Requirements: ffmpeg and ffprobe on PATH, Python 3.9+, numpy, pillow (`pip3 install -r requirements.txt`). Run tools from the repo root, e.g. `python3 pipeline/prep_line.py ...`.
Check the toolchain (no credits, no network): `python3 pipeline/self_test.py` → must end with ALL PASS.
ElevenLabs tools read ELEVENLABS_API_KEY from the environment or from the repo's git-ignored `.env`, and never print it. `python3 pipeline/tts_elevenlabs.py --check` confirms the key, the quota and that the default model is still offered.

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
| contact_sheet.py | Frames at an fps or at given times, tiled into one image. |
| inset_card.py | `card`: logo card for the anchor's inset box. `overlay`: put it on a clip (auto-detects the box). |
| montage.py | Title card + the last N seconds of the sting (ending kept intact). |
| assemble.py | Edit list → final reel: each part levelled to -16 LUFS, old-TV look and TV-speaker sound, 1080x1920 at 25 fps, -14 LUFS, plus a joins contact sheet. |
| trends.py | News-desk trend meter: labels each candidate HOT, RISING, FLAT or COLD from Google Trends India, Google News momentum (today's share of the week) and YouTube this week (views, best views per hour). No login needed; vidIQ adds keyword and outlier data on top. |
| scoreboard.py | The strategy book's arithmetic (docs/strategy.md). `ingest-ig` records a vidIQ Instagram owner-insights reading, `link` ties a reel to its post, `add-reel` records a new episode with the bets it carries and its credits. With no argument it prints the report: each bet's value pooled over its reels against baseline, target and stop, and a verdict (TARGET HIT, STOP HIT, TIME STOP, HOLD). `brief` gives three lines on where we stand for sessions, and `status` the same in plain English for emails; `write` regenerates registry/performance.md and the book in docs/strategy.md. |
| deep_leads.py | The last 7 days of headlines from the deep-lane research sources (docs/sources.md), deduplicated and newest first. |
| look.py | The old-TV picture (presets broadcast, vhs, clean). `look.py CLIP OUT --preset vhs` previews it on one clip and writes a before/after frame. |

`fixtures/` holds a real 3-second Sarika line that the self-test uses; synthetic tones hid a levelling bug that real speech exposed.
