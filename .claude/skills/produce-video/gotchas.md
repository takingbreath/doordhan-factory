# Traps we hit, and the fix (E5–E7)

## Voice
- **A mispronounced word that Scribe still spells right.** Scribe "corrects" from context ("बिली गई तो lift" came back
  as "बिजली"). Its per-word confidence (`exp(logprob)`) doesn't lie: 97.6% on the bad take, 99.99% on clean ones.
- **Letters read as a word.** "OC UP RERA" became "उसी अपि रेरा". Write "OC, U.P. RERA".
- **voice_cut picks the slowest passing monologue take.** After a pronunciation fix, pick by the fixed words'
  confidence instead; keep only that take in `takes.json` and rerun with `--monologue-takes 1`.
- **A whole line tagged slow** stretched E5 from 65 s to 82 s. `[slowly]` goes only right before the punch word.
- **44.1 kHz into a 48 kHz track** sped every mouth up 8.8% (fixed in make_track; check_match can't see it).

## Keyframes
- **Small faces don't lip-sync.** Talking frames need the face at 15–16% of the frame height or more; crop locally.
- **A freshly prompted end frame changes the framing.** Make end images as edits of the start frame.
- **Props creep onto the desk** (a stack of files on E7's first front frame). Remove with a one-change edit.
- **Reused clips show old outfits.** E5's overhead hang-up shows a bare forearm; make a new one when the sleeve changes.
- **"Faint dry smirk" sometimes becomes a toothy grin** on vowels (E6). Add "no smile, no teeth" to the acting note of
  the payoff line.

## Shots
- **Pandey handling anything kills his lips** (a ninth of normal range in the 2026-09-29 reshoots). Billu walking in the
  same shot does not (E7 cold open passed first take).
- **Higgsfield runs about 3 video jobs at once.** Submit in threes; a 429 means wait.
- **Upload host 520s.** put_upload.py retries 5xx now; a 412 on a retry means the first attempt landed.
- **Wan's first second barely moves the lips**: tracks carry a 0.5 s lead, the edit starts 0.38 s into the clip.
- **Wan drifts about −8 ms/s**: talking shots ≤ 6 s of speech (shot_spec splits longer lines).

## Edit
- **Segment boundaries from Scribe's word times cut words.** Use `speech_map.py` pauses on the voice cut.
- **Text over the joke.** E7's amenity ticks first covered Billu's yawn; the hook band first covered his walk-in. Look
  at contact sheets of the raw edit before the finish.
- **Text off the frame.** Pop-in overshoots 12%: fit popping text to 600 px (captions 610). Clamp tags near the edges.
- **Stacked zooms** (Wan's push-in plus ours) cut the head off; re-measure face centres on every new clip.

## QC gate
- **Cold open with no lead:** a reel that starts on the hook's first sound fails "lead 0.00–0.40 s"; start the hook voice
  0.12 s in.
- **Hard-cut end at a segment boundary:** the boundary sat on the next word's onset; move it into the pause.
- **Lip offsets near −125 ms pass, but only just.** Centre them with `qc_repairs.json` `src_shift_s`.
- **A phone copy made after the gate isn't covered** by the stamp; make it before. Re-encoding the final voids the stamp.
- **Identity checks on the final fail under captions and crash zooms.** The gate checks the talking clip, not the final.
- **Lines under ~2 s of speech can't be measured, and Wan mouths through the silence** (DTB3, 2026-10-06). A 0.7 s line in
  a 3 s clip got 1.9 s of mouth movement, opening before the word and flapping after it; a 1.3 s line ran 0.3 s early
  and kept moving. Both read as broken lip sync to Akhilesh. Merge a short line with the neighbouring line of the same
  speaker and framing, or play it as voice-over on a card. Never waive "could not be measured" on sight of moving lips:
  plot mouth opening against the voice frame by frame first (mouth onset/offset within ~0.3 s of the voice).
- **Part audio shorter than its picture slid every later line early** (fixed in assemble.py 2026-10-06: each part's
  audio is now padded to its picture). If late lines drift but each part measures fine alone, check this first.
- **A lower-third over Sarika covers her neckline** (DTB3, 2026-10-06: the −27% card, the 1-2-3 strip and the sign-off
  strips; Akhilesh: "not allowed"). On her shots, every graphic goes in the top-left box beside the bug.

## Creator format (E10, nana01)
- **A phone in frame breaks the premise** (the phone is the camera). Seedream drew one on a shelf showing her selfie
  despite the prompt. Look for it in every frame; remove it with the one-change edit in prompts.md.
- **"Propped on a low stool in front of her" made Seedream draw the phone on a tripod** in both variants (anthropic01).
  Seedream 4.5 also ignored "close-up from mid-chest up" and framed her whole seated body. What worked: its frames are
  1440x2560, so a 720x1280 crop around the face is a true close-up at Wan's size (face 23-26%) and leaves a phone at
  the edge out. Variants of one prompt can also change the outfit (a tie-neck halter against a plain one): pick the
  episode master first, then make every other setup with the master as the first reference.
- **Head roll 17–23°** on Seedream selfies fails preflight (roll over 16°). `pipeline/level_keyframe.py` rotates the
  frame level for free.
- **shot_spec's default tail said "analog look"**: use `--look modern` for this format.
- **The extreme close-up (face ~45%) failed lip sync twice** (eyes half-closed, the mouth open before the voice). Keep talking
  frames at 24–28% face height.
- **Image models draw real products.** An unbranded SUV became a Range Rover; use an abstract detail.
- **Her voice played while she sipped** (Akhilesh caught it). Silent B-roll of her goes into a real pause inserted into
  the voice (nana01_build.py `GAP_AT`/`GAP`), and no caption sits over it.
- **Overlays on spans, not shots:** a credit set from 10.6–22.9 s sat over her talking shot. Attach credits to their archive shots.
- **The concat drifted 0.35 s** with `-t` per shot. Render each shot to an exact frame count from cumulative times.
- **One-pass loudnorm undershot** (−16.3 for −14). Measure, then one gain and a limiter.
- **A swallowed word reads as a "tail"** in the mix check ("मिले" 7 dB under her level after a gap). Lift the word, don't
  trim it; it also sounds clearer.
- **Scribe spells the same audio differently between runs** ("पंद्रह-पंद्रह हज़ार" / "15-15 हजार"; "car" / "कार").
  verify_line composes both now. If another spelling fails, fix the normaliser rather than re-rolling the transcriber.
- **Grain lowers the face check** (about 0.05). Use grain 1 on her shots, and the episode's master keyframe as the face reference.
- **A rebuild that changes the sound needs a new transcript** (the binding is by a fingerprint of the decoded audio,
  about 230-330 ElevenLabs credits each; a picture-only rebuild keeps it, as on E11). Make all fixes, look at
  full-size frames, then transcribe once.
- **YouTube blocks cloud machines** (yt-dlp, Piped, Invidious, cobalt). Clips come from the laptop: write
  registry/clip_requests/<slug>.json, and the laptop's hourly task runs `pipeline/fetch_clips.py --push` to the `clips` branch.

- **anthropic01 (cinema-camera creator, 2026-10-28):**
  - Low angles with a 24 mm lens stretch her body and shrink her head (Akhilesh: "face and body dimensions are not
    matching"), and Wan failed lip sync three times on that line (SyncNet 1.4-3.5). Keep talking shots near eye level;
    after two failures at different framings, make the line voice-over instead of spending.
  - The overhead shot (lying on the rug) passed preflight and its keyframe matched her (0.875), but the Wan clip
    drifted (0.45 against the master, 0.50 against its own keyframe) and failed the gate's face check: voice-over.
  - Bare white walls read as "nothing" (Akhilesh). Fix without regenerating: a one-change edit of the keyframe ("the
    same photograph, the woman not in it, the wall dressed"), then `pipeline/bgswap.py` lays her matte over it
    (also puts kinetic words behind her head with `--text`). A plate that reframes the room (R1's sofa) can't be used.
  - The gate covers the `_phone` copy only if it is newer than the final; encode_finals writes both at once and the
    slower final can finish last. Make the phone copy from the final (produce-video step 9.2) before the gate.
  - The face check against one master failed a wide-mouthed hook at 0.55; a two-face sheet (the master and the clip's
    own approved keyframe, each 360 wide) is a fair reference. Tiny 240 px face crops scored lower: keep faces large.
  - Akhilesh rejected her face as dull, "no makeup", acne-like specks and forehead lines, and her motion as unreal. Causes:
    the keyframe prompt said "natural makeup only, not retouched", and the newsreader rules ("one blink and one small eye
    shift", "no big tilts") were applied to a creator. A heavy skin pass made it worse (plastic). What we learned (the final recipe: formats/creator.md section 1b):
    - Makeup edits, REJECTED in the end (see below). A Gemini edit keeps her face only with her EXACT expression locked: "keep her face exactly
      as it is: the same face shape, eyes, nose, lips, teeth, jaw, smile and expression ... change only: kajal, mascara,
      lip tint; remove every freckle, spot and mark; a little fairer and glowing". A first edit that also changed her
      expression (laugh to closed smile) gave a different woman (Akhilesh: "it is not even her face"; 0.70 against the
      master, the old frame 0.87); the expression-locked edit scored 0.80 (0.83 against the old frame). Seedream 4.5 with
      the old frame as first reference copied the bare face and gave a wide squinting laugh (2 credits lost).
    - No freckles on Rashmi: Akhilesh reads them as marks, even soft brown ones.
    - Then (same day) he preferred the current final's skin and tone to both Gemini makeup frames ("overdoing the
      makeup"), called the lips unnatural in every version, and her mood over-excited. Measured against his reference
      creator (docs/lab/2026-10-28-talking-realism.md): her lips part about twice as wide (ARTICULATE, a grinning start
      frame, the retry's "clear mouth shapes on every vowel") and her brows sit high (attitude words: "bright and eager,
      sharing big news" for a calm explainer). Creator shots now use NATURAL_MOUTH and a calm base; read the script's
      tone before writing an acting note, and start from a relaxed, closed-mouth frame.
    - Acting: a generic list of movements (tilts, bobs, glances, "blinks several times") made Wan move her face and eyes
      all the time; Akhilesh: "overacting ... randomly moving the face and the eyes". `shot_spec.py --look cinema` now
      keeps her still between beats, and `--acting` names one motivated expression per beat (a point: a small nod or
      brow lift; a thought: a look up, then back). Measure with `pipeline/motion_meter.py` against a real creator clip.
    - Wan still creases her forehead when the brows lift, and it adds small dark dots on the nose and cheeks even from a
      clean keyframe: `pipeline/skinfix.py --forehead-only --spots` takes out only those and keeps pores and grain. Use
      no other skin pass on a made-up keyframe.
    - The calm take blinked at clip 0.47-0.73 s, right where the edit starts (the reel's first frame). Held the
      pre-blink frame with ffmpeg `freezeframes=first=13:last=23:replace=12` (the same clip as both inputs); the
      mouth is closed there anyway.
    - With the browser pane hidden, put a reference into Gemini with the bridge's paste route (gemini-media SKILL.md,
      "Putting a file INTO the page"), not the Drive picker.

- **Wan 3.0 for talking shots (anthropic01, 2026-10-28):** `wan3_0` refuses a start frame together with an audio
  track ("start_image cannot be combined with reference media"): send the frame as `image_references` plus the track
  as `audio_references`, `generate_audio: false`, and `declined_preset_id` (it suggested a preset once). It returns
  SILENT video framed like the reference (same face size), its mouth on our track with SyncNet confidence 5-7 (Wan 2.7
  about 3.3) and a constant -160..-200 ms: in the build shift the clip about +0.06 s (with an existing -0.03 repair).
  Lips part closer to a real speaker's (5.3 % of face height against 6.8 % on Wan 2.7 and 3.5-3.8 % real). It took
  about 20 minutes per 6 s clip; 1.75 credits/s at 720p (pipeline/prices.json).
- **A new hook voice moves the hook graphics:** the Remotion hook reads its word times from
  rm/public/data/words_scribe.json, and build.py's CAPS and FX are hand-timed. Fit a new take into the old slot
  (voice/build_v4.py) so the body keeps its times, then update only the hook words there and re-render Hook.

## Creator + Vox collage (E11, jio01)
- **Photos of people in frame steal the lip-sync track.** With Musk and Ambani above Rashmi in the split, MediaPipe
  measured a photo (62 px mouth, SyncNet 0). lipsync_lag now tracks the largest face; keep the speaker the biggest face.
- **The split crops her forehead**, dropping the face check: give the manifest `clips` + `clip_spans` (assets/edits/jio01_build.py
  writes them) so identity is judged on the raw clips.
- **shot_spec's auto-trim and the mix tail check cut real last words** said softly after a short stop ("customers",
  "हैं"). Read `tail_fix` in every spec; rebuild the track from the untrimmed segment (`make_track.py`), and lift a
  soft final word in the mix rather than trimming it.
- **A cut can land mid-blink.** Look at the first frames of every talking clip and move the cut past a blink.
- **Attitude words in the acting note show on her face:** "lively and amused" gave squints and a wink, "eyebrows lift
  on the question" took her eyes off the lens. Use "eyes open and on the lens, head steady and level".
- **gemini_omni collage:** text-free only; keep cutouts in fixed thirds so logo labels can sit still; a "3D RENDER"
  preset suggestion needs declined_preset_id 5a77643c-b6cc-4efd-bdc6-ab8ff48dfa82; "as if thinking" gave a prop a face.
- **A 10 s gemini clip for a 10.5 s line:** slow it with setpts and pad the end (`tpad`); a scene one frame short
  shifted every later cut (render local scenes a little long).
- **Real screenshots of posts are hard to verify:** use a quote card with the verbatim words and the date unless the
  screenshot's source is clean.
