# Why the reels read as AI: audit and three free tests (E5, 2026-09-29)

No defaults, templates or playbooks were changed. Posted episodes were not touched: every test is a copy built from the in-sync v5 build (the E5 build with the gate's P4 lip-sync repair), which reproduces v5 exactly, picture and sound. Spend: 10.5 Higgsfield credits (one Wan shot), within the 15 allowed.

## 1. Audit

The last two posted episodes are **E5** (Sahayata Kendra, 28 Sep evening) and **X1** (Samachar, UPI, 28 Sep morning). X1 was made outside the logged flow: its prompts are in the Higgsfield history, but its edit is not in the repo.

### Video prompts
All prompts are in `docs/lab/2026-09-29/prompts_E5_X1.json`. The camera and movement wording, quoted:

**E5, talking shots (Wan 2.7, 6 used in v4)**
- **T1 (P1):** "Small, subtle, natural movements only; no hands. Locked-off camera." Plus: "a tiny, slow, unimpressed shake of the head … small natural nods".
- **T2 (P2):** "a small, crisp nod each time he says … 'gino' … Small, subtle, natural movements only; no hands, no big grin. Locked-off camera."
- **T3 (P3):** "one slow shake of the head … he leans in very slightly … Small, subtle, natural movements only; no hands … The ceiling fan turns slowly. Locked-off camera."
- **T4 (P4):** "small nods … a tiny, casual shrug of the shoulders … one deliberate nod … Small, subtle, natural movements only; no hands, no big grin. Locked-off camera."
- **T5 (P5):** "raises his right hand into the frame and points … jabbing downward twice … Small, natural movements otherwise; head mostly steady. Locked-off camera."
- **T6 (P6):** "The real ginger cat … stays sitting still … only a slow blink and a small ear twitch, it does not move its body. Locked-off camera."
- **The v1 takes they replaced:** "head steady and level, shoulders still, only a small natural nod on a stressed word … No head tilting, no bobbing, no hair movement, no hand gestures. Locked-off camera."

**E5, other shots**
- **Cold open (Seedance):** "Locked-off 1990s TV camera with a very slow, subtle push-in … perfectly still … Same room, same framing, nothing else moves."
- **K2:** "Extreme close-up … Head perfectly still. Locked-off camera."
- **K3:** "Straight overhead shot, locked-off camera … Nothing else moves."
- **K4/K5 (cat):** "Locked-off camera … small and precise."

**X1 (all 5 Wan shots)**
- **Sarika:** "She begins completely still and silent … head steady and level, shoulders still, only a small natural nod on a stressed word … No head tilting, no bobbing, no turning, no hair movement. Locked-off studio camera. Keep the exact analog look and framing of the start image."
- **Gupta:** "head steady and level, shoulders still, holding the microphone steady at chest height … No head tilting, no bobbing, no leaning. Locked-off stable camera, the shoppers behind him barely moving."

**Finding:** every prompt in both episodes, all 23 of them, says "locked-off". Every talking prompt also asks for a still head, and most forbid hands. Real people on camera are never this still: a steady head with only the lips moving, against a background where nothing moves, is itself an AI tell.

### Audio chain, raw TTS to final (E5)
1. **TTS.** ElevenLabs eleven_v3: Pandey is Akhilesh's clone; the caller is "Bobby". Raw lines measure −14.8 to −17.9 LUFS, with peaks around −1 dBFS.
2. **Line prep.** Edge silence trimmed (−45 dB threshold); pauses over 0.3 s would be cut to 0.24 s. Levelled to −16 LUFS (the files measure −15.9 to −17.0) with a limiter at 0.84. No tempo change for Pandey; Samachar anchors get 1.15.
3. **Caller.** Landline treatment: 380–3000 Hz, an 8 kHz crush, +7 dB at 1.6 kHz and line hiss (the hiss file is −58 LUFS).
4. **Tracks for Wan.** Resampled to 48 kHz with a 0.5 s lead. Wan's own audio is not used in the edit; build.py places our levelled lines.
5. **Mix (build.py).** Gains, relative to the voices at unity:

   | Element | Gain |
   |---|---|
   | Voices | 1.0 |
   | Ring | 0.8 |
   | Click | 0.9 |
   | Cradle | 1.0 |
   | Whoosh | 0.35–0.6 |
   | Pop | 0.35–0.5 |
   | Ding | 0.25–0.3 |
   | Thud | 0.4–0.75 |
   | Stamp | 0.8 |
   | Scratch | 0.55 |
   | Riser | 0.35 |
   | Room tone | 0.12 (about −43 LUFS; runs under everything until the card) |
   | End card | hold music at 300–3400 Hz, 0.9 |

   The bus is then peak-normalised to 0.95.
6. **assemble.py.**
   1. The whole mix is levelled to −16 LUFS, with a limiter at 0.84.
   2. "TV speaker": mono, a 90 Hz high-pass and a 10 kHz low-pass.
   3. Gain to −14 LUFS, limiter at 0.84 (true peak −1.5 dBTP).
   4. AAC at 192 kbps.

**Measured on the mix:**
- **Voice level:** speech runs at −17.8 dB RMS.
- **Bed:** it sits 24 dB under the voice, and the mix is never digitally silent (under −60 dBFS for 0.1% of the time). So E5 did already have a bed.
- **Voice character:** completely dry. Line ends fall 30–60 dB within about 50 ms. There's no room, and nothing ties it to the picture.

### The finish pass (look.py)
Both presets run the same chain:
1. Tone curve (black lift, mid lift, white top).
2. Warm colour balance, then saturation.
3. Downscale to SD, then an unsharp halo.
4. Chroma blur, horizontal only, then a chroma shift to the right.
5. A static ghost copy, 4–6 px to the right.
6. Grain.
7. Bicubic upscale to 1080x1920.
8. Highlight bloom.
9. Scanline overlay, then vignette.

The two presets:

| Setting | E5: `kendra` | X1: `broadcast` (default) |
|---|---|---|
| SD size | 540x960 | 400x712 |
| Chroma blur / shift | 4 px / 2 px | 7 px / 3 px |
| Ghost | 4 px at 2.5% | 6 px at 4.5% |
| Grain (luma / chroma) | 6 / 2 | 16 / 5 |
| Saturation | 1.32 | 1.12 |
| Black lift | 0.015 | 0.05 |
| Bloom | 0.12 | 0.18 |
| Scanlines | 0.08 | 0.20 |

**Finding:** everything in the look is static per frame except the grain. There's no line jitter, time-base wobble, tracking error, flicker or dropout: nothing in the image moves the way tape does. Also, Wan's 30 fps clips become 25 fps with `fps=25`, which drops 1 frame in 6, a regular micro-judder on every movement.

### Runtime: one character talking to camera in a static shot, versus anything else
- **E5 (from the build's shot list, 67.3 s):**
  - One character talking to a locked-off camera: **47.3 s (70%; 76% before the 4.8 s end card)**.
  - Its only "camera move" is the edit's digital zoom: steps and ramps from 1.0 to 1.6, on 46.1 s of it.
  - Every other shot: 15.2 s (cold open, listening close-up, overhead hang-up, cat), plus the 4.8 s card.
  - Text or a graphic is on screen for 100% of the talking time.
- **X1 (estimate, since the edit isn't in the repo):** all five generated clips are one person talking to a locked-off camera. With the format's 2.5 s title montage in a 25 s reel, that's **about 90% talking to camera**.

## 2. Sync first
`lipsync_lag` passes on all six talking lines of the test base (offsets −120 to 0 ms, no confident window outside −125..+45). The only line that failed in the approved v4, P4 with its −160 ms tail, had already been repaired by the gate (v5: src_in −0.08 s). The files are `lag_E5_0_before.json` and the QC gate's v5 run.

## 3. The three free tests
Every version is 67.2 s at −14.0 LUFS:
- `work/lab/out/E5_*.mp4` at full quality
- phone copies in `work/lab/phone/`

| Version | What changed |
|---|---|
| E5_0_before | v5 as built |
| E5_A_bed | + ambient bed |
| E5_B_voice | + voice band-limit, tape saturation, room, hiss |
| E5_C_vhs | VHS pass in place of the `kendra` look |
| E5_ABC_all | all three |

### A. Ambient bed (`audio_variants.py bed()`)
- **What's in it:**
  - A ceiling fan: air amplitude-modulated at the 14 Hz blade-pass rate, plus 100/200/300 Hz motor hum.
  - Distant traffic: low rumble with slow swells and five far horns.
  - Faint mains buzz and wiring hiss.
- **Level:** −43 dB, **about 27 dB under the dialogue**, fading out before the end card.
- **Measured after a simulated Instagram re-encode:** the pauses rise from 25.7 dB to 22.4 dB under the speech, so the floor lifts by about 3 dB.
- **Verdict:** a small change, because E5 already had a room tone. It adds life (the fan and street) rather than filling silence. It can't be judged by numbers; it needs a listen.

### B. Voice matched to the picture
- **Treatment:** 120 Hz–7 kHz band-limit (12 dB/oct), light tape saturation, and a small office room (RT60 about 0.35 s, early reflections at 7–34 ms, wet about 13 dB under dry). Tape hiss 40 dB under the voice runs from the first Pandey line to the card. The caller's landline line is left alone.
- **Measured after the re-encode:** the level 60–200 ms after each last word rises from −25.9 dB to −23.9 dB relative to speech. The voice now has a short room tail instead of stopping dead. Loudness is unchanged.
- **Verdict:** a subtle, low-risk change that removes the "dry studio voice over an old picture" mismatch. It needs a listen, and the hiss in particular is a matter of taste.

### C. Analog VHS pass (`vhs.py`, per frame, in place of the static grain filter)
- **What it does:**
  - Lifted blacks and soft whites.
  - Luma bandwidth of about 300 lines, with a slight smear to the right and a sharpness-circuit halo.
  - Chroma at much lower resolution, bleeding 4 px right, 10% desaturated, with streaky colour noise.
  - Per-line time-base jitter: a smooth wobble plus line-to-line error, new every frame.
  - A head-switching tear in the bottom 16 lines.
  - Streak noise stretched sideways, rare dropouts and faint flicker.
- **Does it survive Instagram?** I simulated the re-encode at 3 Mbps H.264 and measured it against the untreated edit:

  | Measure | Before (kendra) | VHS, before re-encode | VHS, after re-encode |
  |---|---|---|---|
  | Row displacement | 0.00 px | 1.08 px | **1.06 px** (survives almost entirely) |
  | Black level (darkest 1% of luma) | 30 | — | **40** |
  | Mean chroma (saturation) | 14.4 | — | **8.8** |

  Streak noise and dropouts are visible at 100% (`contact_crops_100pct.jpg`).
- **Side by side:**
  - `contact_before_vs_vhs.jpg`: 8 moments, before against VHS, both after the re-encode.
  - `E5_P3_side_by_side.mp4`: the P3 stretch, before against all three changes.
- **Verdict:** this is the change with the most visible effect, and it is the only one that makes the picture move like tape. It does go against Akhilesh's 27 Sep ask for the Kendra look ("clearer … colours brighter"): it's flatter and less saturated. At phone size it reads mainly as "older and softer"; the jitter shows on edges, captions and hair.
- **One side effect:** SyncNet is less sure of itself on the VHS picture. On P3's text-covered stretch a junk reading (+480 ms at confidence 1.56) crosses the threshold, so the gate would flag a lag that isn't there. Picture and sound timing are unchanged, and the other five lines read the same as before. If the pass is adopted, the lip-sync gate should measure the edit before the finish.

## 4. Lip sync under movement (10.5 credits)
- **The shot:** P4, part a ("Ab iska matlab samjho … loan poora khatam", 5.4 s of speech, 7 s billed), regenerated from the original keyframe.
- **The prompt:** he squares a stack of papers, glances down, reaches to the rotary phone and adjusts the receiver, and looks back up for the last words. Otherwise the same wording as before.
- **The file:** `work/lab/regen/P4a_business.mp4` (job 51448349).

He does the business, and does it well: papers squared, receiver lifted and set. But he looks down for most of the line (pitch +15 to +21°) and the **mouth nearly stops articulating**:

| Measure | Original T4v2, same words | With business |
|---|---|---|
| SyncNet windows (offset/confidence) | 0s −80/4.08 · 1s −80/5.26 · 2s −80/5.33 · 3s −80/4.43 · 4s −120/1.91 | 0s 600/0.0 · 1s −560/1.2 · 2s −600/0.0 · 3s 40/0.74 · 4s −600/0.0 · 5s −600/0.0: **no confident window** (UNSURE) |
| Mouth opening range (p90−p10, inner lip / mouth width) | 0.207 | **0.023** (9× less) |
| Face consistency vs sheet (worst frame) | 0.66 | 0.72 |
| Audio kept (check_match) | 1.00 | 1.00 |

**Verdict:** lip sync does not survive this much business. Wan spent the motion on the hands and head and left the lips nearly closed, so this shot is unusable for dialogue. Identity and audio were fine. The raw offsets above are meaningless because the confidence is near zero; the mouth measurement is the real finding.

## 5. Recommendation (nothing changed until you decide)
1. **The biggest tell is the stillness.** In E5, 70–76% of the runtime is one person talking to a locked-off camera with a still head, and every prompt asks for exactly that. Fix it in shot grammar, not in the finish:
   - more cutaways and reaction shots with real movement, using Wan without audio at 1.5 credits a second;
   - the physical business moved into those non-speaking beats;
   - a slow handheld drift on non-talking shots.

   Keep talking shots near-still and facing the camera, since the reshoot shows lips fail under real business. A cheap follow-up test (4.5 credits): one small action before the first word, then still for the line.
2. **Adopt the VHS pass as an optional preset**, with its motion elements (jitter, low-bandwidth chroma, streak noise, dropouts) at about 60–70% strength. For Samachar, try it as the default. For the Kendra, keep Akhilesh's brighter colour but add the time-based elements. Also run the lip-sync gate on the edit before the finish.
3. **Adopt B (voice room and band-limit) as the default**, with hiss optional, after a listen on a phone speaker.
4. **Adopt A (ambient bed) per format:** the Kendra already has a room tone, so it adds little there. It matters more where there's no bed at all; X1's mix is not in the repo to check.
5. **Worth testing next (free):** replace the `fps=25` frame-dropping with frame blending or interlaced 50i-style motion, to remove the regular judder.

## Also found
`put_upload.py` got 403 from Higgsfield's current upload URLs. They now sign an `If-None-Match` header, so the upload only worked with curl and `-H "If-None-Match: *"`. It's a one-line fix in the tool, not made yet.
