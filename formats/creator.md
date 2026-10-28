# Creator (Rashmi): a money story told by an Instagram creator at home

First episode: E10, nana01 (2026-10-09), Akhilesh's own script about Nana Patekar's ₹1.5 crore car.

## 1. Akhilesh's rulings (2026-10-09)
- She is an Instagram creator, **not an anchor**, and this is **not a reading room or studio**. She shoots herself at home (warm, cozy, lived-in) or outdoors.
- **The phone is the camera, so no phone ever appears in frame.** No hand holding a phone, and no phone on a shelf showing her selfie (Seedream added one once; edit it out).
- **Modern clothes.** E10 wore look B: a chunky cream knit cardigan over a black top.
- **Modern look:** a clean grade with light grain, not the CRT/old-TV finish. 30 fps.
- **Tight, fast cuts,** video hooks and cinematography, not a static talking head. A slight handheld imperfection.
- **More of her on screen** ("pretty girls are also a hook"), but real footage carries the proof.
- **Film/TV clips are allowed** (hard rule 4, 2026-10-09). Open and close on the same clip so the reel loops.
- **Past scenes must look like their year** (2015 looked like 2015: a flat LCD with a set-top box, a Nokia, a steel glass).
- **Normal talking pace,** and a natural voice, not read aloud (docs/voices/directing-tts.md).
- **No song:** deliver voice, room tone and effects. Akhilesh may lay a song on top. The clip's own sound may stay.
- **She never talks while she sips:** a silent B-roll beat gets a real pause in the voice (E10, 1.2 s after "cheques mile").

## 1a. Akhilesh's rulings (2026-10-28, anthropic01)
- **A proper lighting setup in every shot:** a motivated soft key (the window, about 45 degrees, a little above the
  eyes), a fill at about 2:1, a hair or back light for separation, and a background lit separately and kept about a
  stop darker than her face, with warm practicals. Mix daylight and lamps as the scene needs. Plan:
  registry/plans/anthropic01.md section 3.
- **The camera can follow his editing reference** (instagram.com/reel/DX4XksWJlLL): a full-frame camera on a tripod,
  self-shot, a different angle per shot (high, low, eye level, overhead), wide and normal primes. This is an exception
  to "the phone is the camera"; the camera still never appears in frame.
- **Editing like that reference:** cuts to rhythm and to motion, kinetic yellow type behind the speaker, small serif
  captions, a warm filmic grade.
- **Tonal sound effects** (his reference instagram.com/reel/DZ5FnK9ocIM): notes and short phrases in one key on the
  transitions and reveals, over plain whooshes.
- **Music bed, hook dry** (replaces "no song" above): creators deliver the hook with no music and bring the bed in when
  the video starts. About 14 dB under the voice while she speaks, ducked with each phrase, high-passed and dipped
  where the voice sits. anthropic01 uses "Silent Pulse - Premium Tech Advertising Theme" from the ElevenLabs Music
  Marketplace with its drop timed to "God share" (Akhilesh: "Use Silent Pulse (mix C). I'll buy the Social Media
  licence in ElevenLabs."). A Marketplace track needs its Social Media licence before posting; a composed ElevenLabs
  bed needs none (work/anthropic01/music/compose.py).

## 1b. Talking shots that read as a real creator (Akhilesh, 2026-10-28, anthropic01: "This looks so much better")
Full diagnosis, numbers and every failed try: docs/lab/2026-10-28-talking-realism.md. The recipe that worked:
1. **Start frame:** the episode's approved look with her face relaxed and the mouth closed (a frame from an approved
   clip works: anthropic01 used the old hook clip at 4.1 s). Not a laughing or grinning frame: Wan keeps the raised
   lip and she talks through a grin.
2. **Hair neat:** a Gemini edit of that frame that changes the hair only ("brushed and blow-dried, combed, no
   flyaways, natural texture, not glossy or silky; keep her face, expression, skin tone and the warm light exactly").
   Every edit changes ONE thing: an edit that also changed her expression gave a different woman.
3. **No makeup edits:** two "add makeup" frames were rejected (one a different face, one "overdoing the makeup"); the
   approved skin and tone came from the plain frame. No freckles.
4. **Wan 3.0:** `shot_spec.py build ... --character rashmi --look cinema --model wan3_0` (the frame as an image
   reference, our track as the audio reference, silent output; about 20 minutes per clip). Its lips were the most
   natural we measured; Wan 2.7 with the same fixes was second.
5. **Calm by default, motivated beats only:** the base is "calm, matter-of-fact and natural ... never theatrical",
   the mouth line "lips part only a little on most syllables, the jaw moves little", and the acting note names one or
   two moments that come from the words (a point: a small nod or brow lift; a thought: a look up, then back; the
   payoff: a faint dry half-smile with the lips closed). Read the script's tone first: anthropic01 is a calm
   explainer, and "bright and eager, sharing big news" made her over-excited. Never list generic movements (tilts,
   bobs, glances, "blinks several times"): Wan did all of them, all the time ("overacting").
6. **A calm voice:** an energetic read makes the face over-move too. Check a suspect phrase with
   `pipeline/phrase_pitch.py` (v3's hook: +1.7 st median, +6 st peak after "jise"; the chosen retake +0.3 st and a
   falling last word), and fit a retake into the old slot so nothing after it moves (work/anthropic01/voice/build_v4.py).
7. **Measure, then look:** `pipeline/mouth_meter.py` and `pipeline/motion_meter.py` against a real creator clip of
   the same framing (lip gap 3.5-3.8 % of face height, p90 7-7.5 %; upper lip 0.12-0.19; brows 0.39-0.49 / 0.30-0.32;
   blinks 5-8 in 10 s). The lip-sync judge only checks timing.
8. **Light skin pass only:** `pipeline/skinfix.py --forehead-only --spots` (Wan's forehead creases and dots); no
   smoothing or glow, which read as plastic.
9. **In the edit:** Wan 3.0 runs about -0.18 s on its track: start the clip 0.06 s earlier (anthropic01 PASS -40 ms).

## 2. When to use it
Human money stories: a person's choice about money, a values story, a "what would you do with ₹X" moment. It suits a tribute or news-of-a-person reel where Samachar's newsreader would feel cold. Not for market moves or explainers (Samachar, Sahayata Kendra).

## 3. Characters
- **Rashmi:** the creator. Late 20s, shoulder-length wavy dark brown hair, small gold hoops, a thin gold chain, natural makeup.
  Her hair is always neatly brushed and combed (no flyaways, no strand across the face, natural texture, not silky),
  her skin clear with no freckles, her makeup light; she is calm and matter-of-fact unless the line says otherwise
  (Akhilesh, 2026-10-28).
  - Identity reference: Akhilesh's Higgsfield image `e9a78b8d-1f8b-4c82-876b-e212b7f896f8` (work/nana/kf/identity_ref.png).
  - E10 master keyframe: `20f3c2d0-b756-4d43-95b4-50851c10b26b`; it is also the face-check reference (assets/characters/rashmi_e10_master.jpg; identity image assets/characters/rashmi_identity.jpg).
  - Voice: ElevenLabs **Rashmiji** (`registry/assets.json` voices.rashmiji) on **eleven_v4**, directed per docs/voices/directing-tts.md.
- **Real people** (hard rule 4, relaxed 2026-10-19): their real photos and footage, and real pictures animated with AI when a shot needs motion; never invented speech. A recreation still carries the "RECREATION · <year>" tag.
  - E11 look: dusty-pink ribbed-knit tank with a high square neckline (Akhilesh: less cleavage, for serious viewers), keyframe `creator_e11_sofa_pink_levelled`; face reference assets/characters/rashmi_e11_master.jpg.

## 3a. Shot grammar
- Talking-shot specs: `shot_spec.py build ... --character rashmi --look modern` (phone look) or `--look cinema --model wan3_0`
  (camera look, the calm creator base and Wan 3.0; section 1b). Exact keyframe and shot prompts: .claude/skills/produce-video/prompts.md, "Creator format"; traps: gotchas.md.
- Talking shots are selfie or propped-phone **close-ups** (face 24–28% of the frame height), straight to the lens.
- **Head level:** preflight fails at 16° of roll. A tilted Seedream frame is levelled by rotating the whole frame locally with `pipeline/level_keyframe.py` (it reads as a casually held phone).
- Lines of 2 s or less are voice-over, never a talking shot (E10: the 2.1 s "lekin madad…" failed lip sync twice and went over B-roll).
- **Silent B-roll of her** (a sip, a look out of the window) sits in a real pause in the voice, never under her voice.
- About a third of the runtime is her lip-synced; the rest is real footage, recreations and inserts.

## 4. Sets and keyframes (seedream_v4_5, 9:16, 1 credit, refs: master keyframe + identity ref)
- **K1, sofa selfie:** golden-hour window on camera left, monstera, lamp. `20f3c2d0`, levelled upload `0c58ccf8`.
- **K3, kitchen counter,** phone propped at chest height, chai mug: `254def93`, levelled `d0a3125a`.
- **K4, extreme selfie close-up:** `adb963fe`.
- **K5, window seat** at sunset: `d0b1a9f7`, phone edited out as `6d26e800`, cropped and levelled as `d1ae821d`.
- The prompts name the light source, lens and aperture, depth layers, real skin and asymmetry (the AI-realism PDF), and always say "The camera IS the phone: no phone, no hand holding a phone, no screen anywhere in the frame".

## 5. Look and graphics (all local, assets/edits/nana01_build.py)
- **Grade:** contrast 1.04, saturation 1.05, slightly warm; grain alls=1 on her shots (more cost face-check points) and 3 elsewhere.
- **Handheld:** a slow multi-sine drift plus a tiny roll at 1.07 zoom; a jump-cut punch-in (1.2×) for emphasis.
- **Archive and film in a band layout:** the clip full width over a blurred, darkened copy of itself. Crop out channel and sponsor logos and baked-in credits, then add our own small credit on each archive shot only.
- **Captions:** Roman Hinglish word groups from Scribe's word times; key words in yellow; Baloo2 ExtraBold with a black stroke at y≈985/1280. ₹ comes from the Devanagari font (the Latin one has no rupee sign).
- **Slams:** a yellow pill ("₹1.5 CRORE", "₹15,000 per family").
- **A TV in a recreation:** generate the set with a plain blue screen, then chroma-key our own bulletin onto it (generic "NEWS" bug, no real channel).

## 6. Sound
- The voice is one continuous take (not per-line), placed 0.15 s in.
- The film clip's own sound plays under the open and the close at 0.22.
- **No room tone on the voice** (Akhilesh, 2026-10-28: "we don't need to make the voice sound bad, clear is good").
  E10 and E11 had road_distant under the voice; from anthropic01 on, the voice stays clean. A recreation's own
  sound (fan_loop under a ceiling fan) stays with that shot only.
- **Sound effects are made in the edit, on the on-screen graphics and transitions** (Akhilesh, 2026-10-28), never on
  the voice cut: each sound sits on the event it belongs to (a cut-out landing, a stamp, a whip), on its word time.
  Soft whooshes and thuds on slams.
- **The hook has energy** (Akhilesh, 2026-10-28: "the hook is very low-sounding"). A "[casual, a little secretive]"
  opener put anthropic01's first line 8 dB under the rest at 196 Hz. "[energetic, quick, like sharing big news with a
  friend]" with "!" raised it to about 275 Hz and 3.5 words a second. Keep the hook about 1.5 dB over the body
  (docs/voices/directing-tts.md).
- **Loudness:** measure, then apply one gain and a limiter to −14 LUFS. One-pass loudnorm undershot to −16.3.

## 7. Shot pattern (E10)
1. Film-clip hook (the subject's face, frame one).
2. Her selfie (the setup).
3. An insert with a number slam.
4. A recreation of the turning point.
5. Real footage of the consequence.
6. Her (the decision).
7. Real footage (the money given).
8. Her silent B-roll beat.
9. Real footage (what it became).
10. Her closing thought, with a punch-in.
11. Back into the film clip (the loop).

## 8. Recurring devices
- The loop: the close plays the clip from just before the open's in-point.
- "RECREATION · <year>" tag on any reconstructed scene.

## 9. Notes from production (E10)
- **Voice:** v3 with line tags read flat (the same tune on every sentence, a 3-semitone fall at every full stop, even pauses). The fix was v4 with directed punctuation (docs/voices/directing-tts.md).
- **Wan and the creator:** natural, expressive head movement. SyncNet judged T1 and T5 fine at −80…+80 ms and centred them with source shifts. The kitchen medium needed one retry (with "eyes open"). The extreme close-up (K4) failed twice: eyes half-closed, a mouth open before the voice.
- **TV recreation:** Wan made the man rise and lean toward the TV, head dropping. It played well, because his face never shows.
- **QC gate:** a manifest `fps` option (30 for this format). Face check against the episode's master keyframe, with light grain on her shots.
- **Script check:** Scribe spells the same audio two ways ("पंद्रह-पंद्रह हज़ार" / "15-15 हजार"). verify_line now composes digits before हज़ार.
- **Edit:** render every shot to an exact frame count. The first build drifted 0.35 s over the concat.

## 9a. Notes from production (E11, jio01: Vox-style collage instead of footage)
- **The variant:** an explainer with no footage to show (Starlink vs Jio). Akhilesh asked for Vox style as close as
  possible, real photos, and a split-screen opening (collage on top, Rashmi below; full screen from the second line).
  Template: assets/edits/jio01_build.py (edit) and assets/edits/jio01_vox.py (local collage scenes).
- **What made the collage:** local scenes for anything with real documents, real photos or exact numbers (the RHP page
  highlighted and stamped RISK, a to-scale growth chart, the Musk/Ambani hook); gemini_omni clips (3 credits a second,
  style key `style.vox_mixed_media_key`) for motion with no text (fibre vs antenna vs satellite; a tug of war over
  houses), with logos and labels laid on top locally. Prompt each cutout to a fixed place ("stays on the LEFT third")
  so labels can sit still; "wobbles as if thinking" gave the dish a cartoon face.
- **Cutouts:** rembg `isnet-general-use` locally (no credits) on news-agency photos; a sticker = white border by
  dilating the alpha + a soft shadow; stop-motion boil (±1.6 px, ±0.45° at 8 fps).
- **Real posts:** a clean screenshot of Musk's X post wasn't reachable (the only one sat in a collage its outlet
  labelled AI-generated), so a quote card carried his verbatim words with "Elon Musk on X · 9 Oct 2026".
- **Frame one:** Akhilesh asked for the famous faces "as quickly as possible": Musk and Ambani are on from frame one,
  the Jio/IPO stickers land on the voice.
- **Eyes:** a line about a question drifted her eyes off the lens; "her eyes look straight into the camera lens for
  the whole line, never glancing to the side" fixed it. "Lively and amused" gave squints and a wink; "eyes open, head
  steady and level, never tipping back" fixed the face-check dips.
- **QC:** in the split, MediaPipe locked onto a photo above her (lipsync_lag now tracks the largest face), and the
  seam crops her forehead (the manifest judges identity on the raw clips: `clips` + `clip_spans`).
- **Soft last words:** the tail check and shot_spec's auto-trim both took a soft final word after a short stop
  ("customers", "हैं") for a breath. Rebuild the track from the untrimmed segment; lift the word 7 dB in the mix.

## 10. Typical cost
E10: 65.25 credits of an approved 80. Keyframes 6, other stills 0.75, talking shots 36 (including 9 of retries), silent shots 9 (the TV room, the chai sip). The voice cost ElevenLabs credits only.
E11 (jio01, 59.2 s, Vox collage): 138.75 of about 185 approved. Looks 6, stills 0.75, talking shots 78 (8 shots, including 25.5 of retakes for eyes and face), gemini_omni collage clips 54 (8 s test reused + 10 s). Local collage scenes cost nothing.
E15 (anthropic01, 56.9 s, Vox desk, cinema look): 138.5 of 147 approved. Wan 2.7 82.5 (five setups with retakes, then three hook tests), Wan 3.0 35, Seedream 21. The finished recipe costs far less: three talking shots on Wan 3.0 (about 24 at 1.75 a second), Gemini frames free. Budget about 60 for a creator reel with three talking shots and local graphics.
