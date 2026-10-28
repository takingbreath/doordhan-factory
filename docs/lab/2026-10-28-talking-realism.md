# Why Rashmi's talking shots don't read as a real creator (2026-10-28, anthropic01)

**Outcome:** Akhilesh approved the re-shot hook ("perfect. This looks so much better"): Wan 3.0 in reference mode, a
relaxed closed-mouth frame with neat hair (hair-only Gemini edit), the calm creator base with NATURAL_MOUTH and two
motivated beats, and a calm voice retake. The recipe for next time is formats/creator.md section 1b; the tools are
pipeline/mouth_meter.py, motion_meter.py, phrase_pitch.py, skinfix.py `--forehead-only --spots` and
`shot_spec.py --model wan3_0`. The sections below are the record of how we got there.

Akhilesh on the hook re-shoots: the lip movement is not natural (also in the current final), she is over-excited
("there is nothing to be excited about ... you're not understanding the script"), the makeup is overdone, and the
current final's skin and tone are better than the made-up re-shoots. No credits spent on this diagnosis.

## Measured against his reference creator (instagram.com/reel/DeyzsQiBZ3B)
MediaPipe face mesh and blendshapes per frame, 30 fps, speech spans only
(scratchpad script mouth_stats.py; motion with `pipeline/motion_meter.py`). Lip gap = inner-lip distance as % of face height.

| clip | lip gap mean | lip gap p90 | upper lip raised | brows (inner/outer) | open-close cycles/s |
|---|---|---|---|---|---|
| real creator, 3 spans of 15 s | 3.5-3.8 | 7.0-7.5 | 0.12-0.19 | 0.39-0.49 / 0.30-0.32 | 2.3-2.5 |
| R1 hook, current final | 8.2 | 13.7 | 0.48 | 0.40 / 0.55 | 1.9 |
| R1m, rejected (makeup 1) | 9.8 | 14.7 | 0.35 | 0.60 / 0.78 | 1.9 |
| R1n, rejected (makeup 2) | 8.1 | 12.3 | 0.37 | 0.54 / 0.63 | 2.5 |
| R2, current final | 4.8 | 9.3 | 0.15 | 0.75 / 0.74 | 2.5 |
| R5, current final | 4.9 | 8.4 | 0.02 | 0.85 / 0.87 | 2.6 |

Picture: work/anthropic01/test/mouth_compare.jpg (eight frames each, same face size).

What the numbers say:
- **The mouth opens about twice as wide as a real speaker's** in the hook (8 % of face height against 3.5-3.8 %),
  and the upper lip stays raised over the teeth (0.48 against 0.12-0.19): she talks through a grin. A real creator's
  lips barely part on most syllables; the shapes come from the lips, not the jaw.
- **The brows sit high the whole time** (R2 and R5 about twice the real creator's level): that reads as surprise or
  excitement, with forehead creases as a side effect.
- **The timing is fine** (cycles per second match; SyncNet passes). Our gate checks only timing, so it passed shots
  that look wrong.

## Causes, in order of weight
1. **Our prompts.** `ARTICULATE` ("the jaw and lower lip move clearly with every syllable") was written on 2026-09-25
   for waist-up shots where Wan barely moved the lips; in close-ups it makes her over-articulate. The judge's automatic
   retry adds "clear, visible mouth shapes on every vowel" (R5 was a retry: pucker and funnel 0.68 against 0.11-0.13).
2. **The start frames.** The hook starts from a wide toothy laugh (a1), so Wan keeps the raised lip and the open
   mouth; every Gemini edit kept or added that smile.
3. **A misread of the tone.** The script is a calm, slightly secretive explainer with one dry joke (the family
   business line). The prompts said "bright and eager, sharing big news", "a surprising money story", "wry and amused",
   "warm and friendly", and Wan acts out every attitude word. The hook voice was also made louder on request.
4. **The voice may add to it.** `pipeline/prosody.py`: pitch moves 2.5 semitones per step in our hook and body against
   1.25 for the reference creator, with a range of 14-16 st against 9.6. The reference has music under it, so its
   numbers are less certain. Wan takes its energy from the audio.
5. **The model.** Wan 2.7 is a general video model that takes our audio; it is not a lip-sync specialist, and it
   makes frontal, symmetric, "presenting" faces. How much of the fault is the model alone is not proven yet: causes
   1-4 are in our hands and were never removed in one test.

## What others use (web research, 2026-10-28; mostly vendor claims, no Hindi benchmark found)
- **Causes practitioners name** match ours: an energetic or happy voice drops the jaw on every syllable; a smiling start
  frame gives teeth flicker and jaw over-motion (one source says the opposite: test); "audio strength" settings that
  are too high exaggerate the lips; animating only the mouth reads as a mask.
- **Specialist talking-avatar models** (OmniHuman 1.5/2.0, Kling Avatar 2.0, HeyGen Avatar IV, Mirage): none is in our
  Higgsfield catalog through MCP; reports say Kling exaggerates expressions, HeyGen smiles through pauses, OmniHuman
  lists no Hindi.
- **Video-to-video lip sync:** Sync's sync-3 (April 2026) replaces only the mouth and claims to keep the performance;
  it is in Higgsfield as `sync_so` ("Sync Lipsync 3", input_video + input_audio). Sync advises generating a natural
  performance first, then syncing it. Not independently benchmarked.
- **Performance capture:** Kling 3.0 Motion Control (`kling3_0_motion_control` in Higgsfield) moves a person's
  recorded performance onto the character image; the main reported fault is face drift.
- **Skin:** put the texture in the keyframe (the video copies it), no smoothing enhancers, fine grain last.

## Higgsfield prices for a 6 s hook test (get_cost, 2026-10-28)
| route | credits |
|---|---|
| Wan 2.7 with our audio (today's route), calm prompt | 9 |
| Wan 3.0 with our audio, same frame and prompt (risk: may treat the audio as a reference and re-voice; check_match will tell) | 10.5 |
| Kling 3.0 Motion Control std, from a person's phone take of the line | 11 |
| Sync Lipsync 3 on an existing clip with our track | 21.6 |

## Higgsfield Lipsync Studio and the Higgsfield blog (checked 2026-10-28)
- higgsfield.ai/lipsync-studio: upload an image or a video, upload or generate audio, pick a model (InfiniteTalk,
  Higgsfield Speak, Veo 3, Kling, Wan 2.5 Fast; the blog counts 10). Its models are NOT in the MCP model catalog, and
  the built-in browser is not signed in to higgsfield.ai, so it is open only through Akhilesh's own login. A spend
  there bypasses the spend guard: declare it with `pipeline/spend.py declare`.
- Blog "make-ai-lipsync-videos" (7 Jul 2026): lip timing is "largely a solved problem"; realism comes from six
  things together (lips, expressions, eyes, head motion, gestures, voice delivery); one-pass audio + face models give
  less emotional mismatch than two-step lip sync; start images with a light natural expression, no heavy makeup; subtle
  emotions (irony, skepticism) transfer poorly on every tool; change one variable at a time.
- Higgsfield's own UGC workflow makes talking creators with Seedance 2.5 in one pass with native audio (our voice only
  as an accent/timbre reference): it would not keep Rashmi's exact ElevenLabs voice.
- **Wan 3.0 (`wan3_0`, 1.75 credits/s at 720p) refuses a start frame together with an audio track** ("start_image
  cannot be combined with reference media"): with our audio, her frame can only be an image reference.

## Prepared, not run (needs credits)
- **Calm Wan test, 9 credits:** start frame from the current final's own hook clip (R1_skin at 4.1 s: approved skin
  and tone, mouth closed, relaxed; preflight PASS), `NATURAL_MOUTH` in place of `ARTICULATE`, the calm creator base,
  and two beats only (a small head shake on 'kabhi', a faint closed-lip half-smile at the end).
  Spec: work/anthropic01/specs_v4/R1.json (media ids to fill in).

## Test 1 results (2026-10-28, 19.5 credits approved, budget 115)
| clip | lip gap mean | p90 | upper lip | brows | blinks/10 s | head roll sd | lip sync |
|---|---|---|---|---|---|---|---|
| real creator | 3.5-3.8 | 7.0-7.5 | 0.12-0.19 | 0.39-0.49 / 0.30-0.32 | 5-8 | 8-10 | - |
| R1 current final | 8.2 | 13.7 | 0.48 | 0.40 / 0.55 | 7.9 | 3.7 | PASS |
| R1c27, calm Wan 2.7 | 6.8 | 12.0 | 0.19 | 0.44 / 0.44 | 5.9 | 3.6 | PASS (SyncNet -80 ms, conf 3.3) |
- The calm prompt and a relaxed start frame fixed the grin (upper lip in range), the brows and the blinks; the lips
  still part about 1.8x a real speaker's. Wan 2.7 alone does not get the lips to a real creator's size.
- Wan 3.0 (reference mode, job 21119924-52ce-4daa-bcf0-db5a0ad68919) was still rendering after about 15 minutes.
- Test clips: work/anthropic01/test/hook_calm_compare.mp4, hook_calm.mp4; build.py now uses R1c27_fix.

## Test 1, continued (same day, after Akhilesh: "the lip movement is a lot better")
- **Wan 3.0 take** (reference mode, our track): it returns silent video, but its mouth follows the track closely
  (SyncNet conf 5-7 against about 3.3 for Wan 2.7; a constant -160..-200 ms, shifted in the edit: off +0.06 with the
  L1 repair). Lip gap 5.3 % (Wan 2.7 calm 6.8, real creator 3.5-3.8), upper lip 0.12, brows 0.44/0.43, identity 0.84
  against its reference frame. Same face size as Wan 2.7 (an earlier contact sheet compared a full frame with a crop:
  it is NOT wider). In the edit: PASS, -40 ms, conf 4.95. work/anthropic01/test/hook_wan27_vs_wan30.mp4.
- **Hair** (Akhilesh: "like she just woke up ... everywhere", and AI-silky in the latest): from our realism recipe
  (a loose strand across the cheek, flyaways) and the strong warm backlight. Gemini, hair-only edit of the calm frame
  keeping the warm light: neat, combed, identity 0.84 against the calm frame (kf/hair2_crop.png). Removing the sun too
  (hair1) made her paler and changed the face more.
- **Voice:** in v3's hook the second half ("jise tum kabhi khareed nahi paoge") sits +1.7 st above the first and peaks
  +6 st (Akhilesh: "excited, pitch up"). Calm takes "[calm, matter-of-fact] ..., jise ... paoge." D_s41 +0.3 st (last
  word -6.7) and D_s43 +0.4 st (-5.6); build_v4.py fits a take into v3's hook slot (x1.05 / x1.07 tempo) so the body
  starts at exactly the same time (cross-correlation 0.0 ms): no graphic, caption or cut moves.

## Hook re-shoot (approved: voice take 1, Wan 3.0, neat hair; budget 126)
- R1h (Wan 3.0, reference mode, kf/hair2_crop.png + voice v4 hook track): lip gap 5.0 % (p90 8.2; real 3.5-3.8 / 7.0-7.5),
  upper lip 0.07, brows 0.47/0.48, head roll sd 4.6, blinks 2 in 10 s (low), identity 0.85 against the neat-hair frame.
  Raw sync a constant -160..-200 ms; in the edit (+0.06 s shift) PASS -40 ms, conf 3.6.
- Hair neat and combed, warm rim kept, natural texture. Voice v4 (D_s41) in build.py; hook captions, three hook sound
  effects and the Remotion hook graphics re-timed to v4's words (rm/public/data/words_scribe.json, v3 copy kept).
- Test clips: work/anthropic01/test/hook_v5_compare.mp4, hook_v5.mp4.
