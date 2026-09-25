# Episode log

Add a row per episode, and a line whenever you change a default or a tool.

| # | Date | Format | Topic | Length | Credits | What broke / learned |
|---|---|---|---|---|---|---|
| 1 | 2026-09-23 | Teleshop | iPhone 18 Pro on EMI | 56s | ~227 (incl. ~115 setup/learning) | Seedance re-voices and re-times dialogue; trim on the clip's own audio. Loudness gap Sachdev/Rahul fixed by levelling to -16 LUFS. Split screens false-flagged NSFW. Ending must connect to the setup (SMS + slate). |
| 2 | 2026-09-25 | Samachar | NSE listing | 34s | ~190 (incl. characters, voice tests, reshoots) | Seedance turned Gupta's line into gibberish → Wan 2.7 keeps exact audio. Wan on a waist-up shot = no lip movement → close-ups only. Two-shot ending left a dead gap → one continuous shot. Real NSE logo in the inset box for first-frame topic recognition. |
| T1 | 2026-09-25 | Samachar (setup test) | Sarika tagline ident, "नमस्कार। सब कुछ महँगा... सच मुफ़्त।" | 5.5s (2.5s title montage + 3s close-up) | 4.65 (Wan 720p 3s 4.5 + TTS 0.15) | Whole chain works on the new machine. Wan kept the track exactly (correlation 1.00), lips clearly move (mouth/head 1.78), face and logo stable. Wan returns 718x1282 @30fps and +3 dB louder; the old 480 edit threw the extra detail away. Preset recommendation fired again → declined_preset_id. |

## Changes to tools and defaults

- 2026-09-25 (takeover): each change below says what and why; the git history has the diffs.
  - **prep_line.py**: re-measures after tempo and limiter and corrects the level. A real TTS line landed at -17.3 LUFS instead of -16, which silently undid "every line at the same loudness". The self-test now uses a real voice line (pipeline/fixtures), because synthetic tones hid the bug.
  - **Edit resolution 480x854 → 720x1280** (common.py; assemble, inset_card, montage follow). Wan's 720p output was downscaled to 480, then upscaled to 1080; eyes, lips and text came out visibly cleaner at 720 in a side-by-side of the same shot. Lipcheck boxes and inset coordinates stay in the 480 frame, so documented numbers still hold. The grain is finer at 720; if Akhilesh prefers the chunkier old texture, raise `noise=alls` in assemble.py rather than going back to 480.
  - **assemble.py** levels each part to -16 LUFS before joining (montage parts: `"lufs": -17`). Wan changes the level of the track it's given (+3 dB on the test), which undid per-line levelling between shots.
  - **check_match.py** now tests envelope correlation (≥0.90) and tolerates level changes and small constant offsets. The old on/off pattern score gave 97% (PASS) to the same line played backwards.
  - **lipcheck.py** adds mouth-vs-head motion while speaking (≥1.3), which works on short clips with few silent frames and separates lip-sync from head bobbing.
  - **contact_sheet.py** handles a single time; one-part edits crashed assemble.py. It also sizes the grid to the clip instead of always 12x2.
  - **make_track.py** flags a hold that spills into an extra billed second (the test track went from 4 s to 3 s, saving 1.5 credits).
  - **tts_elevenlabs.py**: eleven_v3 is still the right model (GA Feb 2026), so no rename was needed. Added `--check` (key, quota, model still offered), `--voice <registry name>`, language/seed/stability, and the key from `.env`.
  - **New tools**: `transcribe.py` (ElevenLabs scribe_v2; scribe_v1 was removed July 2026) catches gibberish and gives word end times; `qc.py` runs every shot check into one notes file.
  - **Registry** synced with the Higgsfield account: all 19 job IDs exist. Sachdev's voice is deleted. Rahul's voice reference is an image-designed Seed Audio line. Costs are recorded (a new Higgsfield voice element is 40 credits). Mouth box for the close-up. New reusable clip: Sarika's tagline ident.
  - **Docs**: YouTube Shorts added (CLAUDE.md "The job", a Shorts posting kit with the "altered or synthetic content" disclosure). Playbooks updated for qc.py, cost preflight, declined presets, and reading the desk email at the script step. The news desk now skips topics already made and asks for three differently shaped options. Hard rules unchanged.
