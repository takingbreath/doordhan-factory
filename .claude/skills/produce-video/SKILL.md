---
name: produce-video
description: Produce a Doordhan reel end to end once its script is approved. Covers the voice fixes and voice cut, wardrobe, set and Billu, the graphics plan, keyframes, talking and silent shots on Higgsfield (Wan 2.7), the edit, the old-TV finish and the QC gate, and hands back a stamped final, then the registry log and posting kit after approval. Use for /produce-video, "produce the approved script", or "make the video" after a /reel-script hand-off or a pasted approved script. Args - the approved script (a loop slug plus the picked script id, e.g. "property-checklist-noida-20261004 w1-1", a script file, or pasted lines) and any edits the approver asked for, word for word.
---

# /produce-video: from an approved script to a QC-stamped final

Akhilesh or Naveen may run this. It follows what made E5–E7 (Sahayata Kendra); E7 (work/sk03, 2026-10-04, 66 s, 89.25
credits, every check passed) is the reference episode, and its build and graphics are the templates in assets/edits/.
The canonical rules live in CLAUDE.md, the format file, and playbooks/produce.md. Read those; this skill is the
order of work, the commands, and the traps. Where a format file disagrees with this skill, the format file wins
(section 1 of a format file holds Akhilesh's rulings).

Supporting files in this folder: `prompts.md` (the prompts that worked on E7, for every kind of shot) and
`gotchas.md` (every trap we hit, with the fix).

## Ground rules (hard rules in CLAUDE.md; these are the ones this skill touches)
- **The script is approved** by Akhilesh or Naveen. Apply their edits word for word. Never re-litigate the script.
- **Money:** up to 60 Higgsfield credits per episode without asking. A Kendra episode costs about 90 (E6 94.5, E7
  89.25), so expect to stop at step 4 and ask **Akhilesh** with a breakdown; Naveen can approve scripts and finals but
  not spending above the budget. Log every generation in `work/<slug>/credits.md` as you go.
- **Never post or publish** anything, and never call vidIQ's publish/upload tools or Higgsfield's TikTok tools.
- **Never print, log or commit keys.** The ElevenLabs key lives in the git-ignored `.env`.
- **Only a gate-stamped final leaves the machine** (the SendUserFile hook and put_upload.py enforce it).
- **Akhilesh should never be the one to find** gibberish audio, still lips, a cut word, garbled text, a jarring cut or
  a wrong fact. Look at frames yourself; the checks are proxies.

## 0. Where it runs, and what runs in parallel
**On Akhilesh's laptop** (the Doordhan studio session; Akhilesh, 2026-10-19). The cloud morning session freezes the
approved script and hands over `/produce-video <slug>`; `git pull` first. On a Mac, run the QC tools with
`~/.venvs/doordhan-qc/bin/python` and cut-outs with `~/.venvs/doordhan-cut/bin/python`. A cloud session produces only
when Akhilesh asks ("produce it here"); it installs its tools first (about 13 minutes on jio01).

Parallel work that leaves the result unchanged (jio01 measured it: the same files, the same gate readings):
- **While Higgsfield renders** (talking shots in batches of 3, its limit; collage clips and stills alongside): build
  the graphics, cut out photos (`pipeline/cutout.py`), write the edit, and send a sub-agent to source real photos.
- **Judge each batch as it lands**, the shots of a batch side by side (each `shot_spec.py judge` writes only its own spec).
- **The edit** (pipeline/buildkit.py, used by assets/edits/jio01_build.py and nana01_build.py): shots render in
  parallel and a shot whose inputs haven't changed is reused, so a one-shot fix rebuilds in about a minute. Between
  fixes use `DRAFT=1` (a fast `<stem>_draft.mp4` to look at; never gated). The build that goes to the gate is a
  normal one: the final and the phone copy encode at once, preset slow, as before.
- **The QC gate** measures every talking segment's lip sync at the same time.

What stays in order, because each step feeds the next: the voice cut, then the segments and tracks (they drive the
lips); the keyframe checks, then the talking shots (identity); each shot judged before the edit uses it (a bad take
must not reach the cut); a chained shot after the clip it chains from; the final build, then the gate, then you look,
then it is sent.

## 1. Setup (about 3 minutes, no credits)
1. `python3 pipeline/produce_check.py` must say READY. It lists the fix for anything missing (fetch_models.sh, the
   ElevenLabs key, the sfx kit). Then `python3 pipeline/self_test.py` must end ALL PASS (on a Mac, run the QC tools
   with `~/.venvs/doordhan-qc/bin/python`).
2. Higgsfield: load the connector's tools (ToolSearch "select:" for generate_image, generate_image_batch,
   generate_video_batch, media_upload, media_confirm, jobs_wait, balance, models_explore). Call `balance`. Then
   `jobs_wait` with timeout 0 on the style reference (`registry/assets.json` style.doordhan_look_vertical) and the
   character sheet: if they come back `completed`, the registry IDs work from this workspace. If not, upload the local
   copies in `assets/characters/` and `assets/references/` (media_upload, then
   `python3 pipeline/put_upload.py FILE "URL" image/jpeg`, then media_confirm) and use the new media IDs everywhere
   (note them in `work/<slug>/ids.json`).
3. Read, in full: CLAUDE.md; `formats/<format>.md` (section 1 = rulings); `playbooks/produce.md`; the registry
   (characters, keyframes, `wardrobe_log`, `clips`); the last three rows and the latest "Changes" bullets of
   `registry/episodes.md`; the loop's `s8-handoff.md` for the picked script (its claims trace, voice notes and lint).

## 2. The episode folder and the frozen script
- Slug: Kendra episodes are `sk<NN>` (next free number in work/ and registry/scripts/). Work in `work/<slug>/`; the
  final goes to `outputs/<slug>/E<n>_<topic>.mp4`.
- Write `work/<slug>/approved_lines.json`: `[{"id","speaker","text"}]` per spoken line in order (Billu's silent beat
  left out). The text is what the voice gets: Devanagari with English words in Latin, delivery tags in brackets
  (`[flat, brisk]`, `[slowly]` only before the punch word), letters respelled to be said as letters
  (`OC, U.P. RERA`), numbers as Hindi words.
- Freeze it: `python3 pipeline/script_freeze.py <slug> --lines work/<slug>/approved_lines.json --approved-by "<who>"
  --note "<loop slug + pick, and every edit the approver asked for>"`.

## 3. Voice (no Higgsfield credits; ElevenLabs characters only)
Sahayata Kendra (other formats: format file + playbooks/produce.md step 3):
1. Start from the loop's cut: `cp -R work/<loop-slug>/loop/audio/<pick> work/<slug>/voice`, delete its
   `*_voice_cut.*`, `cut.json`, `report.md`, set `"name": "<slug>"` in `voice/lines.json` and write the approved text
   into it. Unchanged lines reuse their takes.
2. If the approver flagged a mispronunciation, first test 2–3 spellings as short lines with
   `python3 pipeline/tts_elevenlabs.py --voice pandey --text-file T.txt --out T.mp3` and
   `python3 pipeline/transcribe.py T.mp3 --json T.json`; keep the spelling Scribe hears right.
3. `python3 pipeline/voice_cut.py work/<slug>/voice/lines.json work/<slug>/voice --retake <changed ids> --monologue-takes 3`.
4. **Choose the take by Scribe's per-word confidence** on the flagged words (`exp(logprob)` in
   `voice/check/<take>.scribe.json`), not by voice_cut's slowest-take rule: the take Akhilesh heard as "बिली" scored
   97.6% on "बिजली" where clean takes scored 99.99%. To force a take: keep only it in `voice/takes.json` and rerun with
   `--monologue-takes 1`.
5. Send `work/<slug>/voice/<slug>_voice_cut.mp3` to the approver with what changed and anything to listen for.

## 4. The creative plan and the budget gate
Write `work/<slug>/plan.md`, then show it at the gate together with the voice cut.
- **Wardrobe:** a new outfit for every character on screen (check `wardrobe_log`; nobody repeats). Akhilesh likes
  the clothes and the background to be interesting (E7: wine-maroon 70s collar, striped tie, sleeve garters).
- **Set dressing that serves the topic** on the wall behind Pandey (E7: a faded "SAPNON KA GHAR / POSSESSION 2011"
  builder poster, a crack and a damp stain, paid off by a pull-back on the last line). The board, the floor plan and
  "only Billu and the phone on the desk" stay (format section 4); a prop the script needs can live in an insert and
  in Billu's last shot.
- **Billu does something new:** don't repeat the last two episodes' beats (episodes.md, format section 3). E7: walks
  in along the desk during the hook, yawns at the sales pitch, ears up on the turn, a prop button.
- **Graphics plan:** a list in the script becomes numbered check cards plus a full board (the checklist template); a
  mechanism becomes a chain diagram (the diagram template); a number becomes a slam; a website said aloud goes on
  screen. On-screen text is Roman Hinglish; the caller's question is English (format section 1).
- **Shot list:** map every segment of the voice to a shot. Talking shots are ≤ 6 s of speech, straight to camera or
  eyes down, nothing handled. At least 45% of the runtime is not a face talking: listening, Billu, inserts, graphics.
  One wide (the cold open), mediums, one close.
- **Cost table** from `registry/assets.json` `_costs_credits` (Wan 720p 1.5 a second, billed in whole seconds;
  gpt_image_2_5 0.25). E7: 7 talking shots 54, 6 silent shots 31.5, 15 images 3.75.
- **The gate:** if the total is over 60, ask Akhilesh (AskUserQuestion) with the breakdown, the voice cut, a look
  sheet of the new keyframes, the graphics previews and a recommendation, plus the format default vs your alternative
  for anything you're changing. While waiting, you may spend inside the 60 on keyframes and on one or two test shots
  of the riskiest new idea (E7 tested Billu's walk-in and his file button first).

## 5. Keyframes (gpt_image_2_5, 9:16, 0.25 each)
- Reference the previous episode's front keyframe (for the set), Pandey's sheet and the style reference; prompts in
  `prompts.md`. Make the new-look front frame first, look at it, then the rest in one `generate_image_batch` that
  references the new front frame.
- Download every frame to `work/<slug>/kf/` and check each:
  `~/.venvs/doordhan-qc/bin/python pipeline/preflight_keyframe.py KF.png --profile pandey` (talking frames: face at
  least 15–16% of the frame height, closed mouth, heavy lids, head level) and
  `~/.venvs/doordhan-qc/bin/python pipeline/face_consistency.py assets/characters/pandey_sheet_v2.jpg KF.png`
  (PASS ≥ 0.55). Look for the floor plan (Billu screen left, phone screen right), stray props on the desk (remove with
  an edit: "Exactly the same image ... with one change only"), and the text on the board and posters.
- A face that is too small: crop locally (E7: 648x1152 from 752x1344) and upload the crop.
- **End images come from the start image** by an edit ("The same image as the reference, same framing ... with these
  changes only: ..."). A freshly prompted end frame changes the framing and forces a camera move.

## 6. Segments and shots (Wan 2.7, 720p)
1. **Segments:** cut the approved voice cut into one wav per shot at its pauses. Take the boundaries from
   `python3 pipeline/speech_map.py work/<slug>/voice/<slug>_voice_cut.wav` (its `pauses`), not from Scribe's word gaps:
   Scribe put "Dues" 100 ms late on E7 and a boundary there cut the word's onset. Write `work/<slug>/seg/<ID>.wav`
   (`ffmpeg -ss A -to B -i CUT -ac 1 -ar 48000`) and `seg/segments.json` (`cut_start`, `cut_end` per segment). A line
   placed in the mix may start earlier than its track (`H_voice` pattern in the template) when the pause is short.
2. **Talking shots:** `python3 pipeline/shot_spec.py build --line work/<slug>/seg/<ID>.wav --id <T#> --keyframe <ID>
   --character pandey --set kendra --framing <front|three_quarter_left|...> --acting "<one note per beat>"
   --out work/<slug>/specs`. Upload each `specs/<T#>_track.mp3` (media_upload with `files[]`, then
   `python3 pipeline/put_upload.py FILE "URL" audio/mpeg`, then media_confirm with `media_ids`), put the media ID into
   the spec's `audio_references`, and submit the spec's `params` with `generate_video_batch`, **3 at a time** (a 429
   means wait). A shot where something else in frame moves (Billu walking in) can take an `end_image` too.
3. **Silent shots:** Wan 2.7 with a start image (and an end image for a change), no audio, 2 s minimum. Prompts in
   `prompts.md`.
4. Download each clip to `work/<slug>/vid/<name>.mp4`, record its job ID in the spec, then
   `~/.venvs/doordhan-qc/bin/python pipeline/shot_spec.py judge work/<slug>/specs/<T#>.json work/<slug>/vid/<T#>.mp4`.
   ACCEPT, ACCEPT_WITH_SHIFT (an `audio_shift_ms`) or one automatic RETRY, then ask. Make contact sheets
   (`pipeline/contact_sheet.py CLIP OUT --fps 4 --width 160`) of every silent clip and find the frames you'll use
   (when the receiver lands, when the head turn completes).

## 7. Graphics (local, free)
`cp assets/edits/sk03_gfx.py work/<slug>/gfx.py`; change `ITEMS`, the board title, the diagram's boxes and title;
`python3 work/<slug>/gfx.py` writes `gfx/checklist_preview.png` and `gfx/diagram_preview.png`. Look at them: nothing
runs under the footer or off the frame, and no text is smaller than about 32 px (the look softens to ~400 px across).

## 8. The edit
- `cp assets/edits/sk03_build.py work/<slug>/build.py` and `cp assets/edits/sk02_mouthbox.py work/<slug>/mouthbox.py`.
  Write `work/<slug>/edit.json`: `{"out": "outputs/<slug>/E<n>_<topic>.mp4", "parts": [{"file": "work/<slug>/edit_raw.mkv", "room": false}], "target_lufs": -14, "look": "kendra", "ambience": "office"}`.
- Change the episode-specific parts of build.py: `RING`/`CLICK`/`C1_IN`/`C1_OUT`/`HANGUP1` from `voice/cut.json` and
  `voice/check/cut.scribe.json`; `FIRST` (each segment's first word); `TALK`; `FACE` (measure each clip with
  `~/.venvs/doordhan-qc/bin/python work/<slug>/mouthbox.py work/<slug>/vid/<T#>.mp4 1.0`); the `SHOTS` list; the text
  `EVENTS`; the sound effects in `mix()`; Billu's button and the card. Keep the hook voice 0.12 s into the reel
  (`P1_AT`): the gate wants a lead before the first word.
- `PLAN_ONLY=1 ~/.venvs/doordhan-qc/bin/python work/<slug>/build.py` prints the timeline, the talking share (≤ 55%)
  and each shot's source span ("runs past the clip" means fix it). Then the full build (about 30 s), then contact
  sheets of `work/<slug>/edit_raw.mkv` at 25–30 moments. Fix anything that covers a face or Billu's action, text off
  the frame, a jump at a cut, and look at the first frame (it is the cover).

## 9. Finish and the QC gate
1. `~/.venvs/doordhan-qc/bin/python pipeline/assemble.py work/<slug>/edit.json` (about 3 minutes for 66 s).
2. **The phone copy before the gate**, so the stamp covers it:
   `ffmpeg -v error -y -i FINAL.mp4 -c:v libx264 -crf 28 -preset slow -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart outputs/<slug>/<stem>_phone.mp4` (21 MB for 66 s; SendUserFile's limit is 30 MB).
3. `python3 pipeline/transcribe.py FINAL.mp4 --json work/<slug>/final.scribe.json`, write its `text` to
   `work/<slug>/final_transcript.txt`, then `~/.venvs/doordhan-qc/bin/python pipeline/qc_gate.py bind-transcript FINAL.mp4 work/<slug>/final_transcript.txt`.
4. `~/.venvs/doordhan-qc/bin/python pipeline/qc_gate.py work/<slug>/qc_manifest.json`.
5. On BLOCKED, read each failure's clip and fix (gotchas.md has the ones we've hit), then rebuild, assemble, make the
   phone copy again, transcribe, bind and gate. Lip offsets that pass but sit near the −125 ms limit (E7 had −120): centre
   them with `work/<slug>/qc_repairs.json` (`{"P2A": {"src_shift_s": -0.08}}`; −0.08 s moves about +80 ms).
6. `python3 pipeline/qc_stamp.py outputs/<slug>/<stem>_phone.mp4` must exit 0.

## 10. Look yourself, then present
- Contact sheets of the final (`pipeline/contact_sheet.py FINAL OUT --times ...`) across the whole reel, and faces at
  full size in every talking shot (grins, wide eyes, a dead stare). The first frame must show the subject.
- Send `outputs/<slug>/<stem>_phone.mp4` and `outputs/<slug>/<stem>_qc.png` with SendUserFile. Say in plain language
  what you checked, what you're unsure about (words worth a listen, any brief artefact), the length against the
  format, the credits spent against the approved budget, and what must happen before posting (e.g. a comment keyword's
  auto-reply and PDF). Nothing is posted.

## 11. After the approver says it's approved
- `registry/episodes.md`: a row (number, date, format, topic and script source, length, credits with the split, what
  broke and what was learned) and a "Changes" bullet for every new lesson.
- `registry/assets.json`: the outfit in `wardrobe_log` (newest first), the keyframes as `kendra_e<N>_*` with a
  `keyframes_notes` line, the reusable clips as `clips.kendra_reusable_e<N>`.
- `python3 pipeline/scoreboard.py add-reel --id E<N> --format <format> --story "..." --bets <what it carried> --length <s> --outfit "..." --credits <spent> --notes "..."`.
- The format file: the cost line in section 10 and any lesson that changes how the next episode is made.
- The posting kit, in the message itself, following `playbooks/post-kit.md` (caption, cover frame, settings, poll,
  linked reel, audio name, slot, YouTube Shorts title and settings); also save it as `work/<slug>/post_kit.md`.
- Offer to commit and push (registry, scripts, docs; work/ and outputs/ are git-ignored). Push when they say yes: the
  strategist routine reads GitHub every night, and an unpushed episode gets logged as an unknown reel.

## Other formats
The creator format (Rashmi at home, modern look): formats/creator.md section 1 first, then `assets/edits/nana01_build.py` (real footage, a keyed TV recreation) or `assets/edits/jio01_build.py` with `assets/edits/jio01_vox.py` (a split-screen opening, Vox-style collage from real documents and photos, AI collage clips with logo labels); both write their own QC manifest at 30 fps. `pipeline/level_keyframe.py` for tilted heads, `pipeline/cutout.py` for photo cut-outs.
The templates are for Sahayata Kendra. Samachar (Sarika, Gupta) and Teleshop follow their format files: Sarika's
wardrobe keyframes use seedream_v4_5 (GPT Image blocks her necklines), talking shots use the steady-newsreader
sentence and must pass `headcheck.py`, and the edit is usually an assemble.py edit.json with a hand-written
qc_manifest (playbooks/produce.md step 10). Steps 1–4 and 9–11 apply unchanged.
