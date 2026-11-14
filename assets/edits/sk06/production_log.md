# sk06 notes
- Gemini chat with Pandey's bus stills (reuse for edits, same references attached): https://gemini.google.com/app/254dd1a65e5effc8
- Stills (sparkle cleared): kf/S1_closeup.png, S2_veryclose.png, S3_wide.png, S5_outside.png. S4_brake.png failed (no lurch; same as S3): the brake is a video from S3's frame.
- References: kf/ref_face.png (silver01 F1a), kf/ref_sheet.jpg (pandey_sheet_v2).
- Wardrobe (new): faded sky-blue checked shirt, sleeves rolled, black office backpack worn on the chest, steel tiffin in the wide.
- Akhilesh 2026-11-13: bus setting, cinema look, close and very close talking shots with little shake, ONE brake, Billu dropped unless natural, Bollywood song(s) added by him in Instagram Edits (split, mute, volume per section); we test offline with the song, then deliver without it plus a cue sheet.

## Akhilesh, 2026-11-13 (look v1 review)
- ONE song only. Claude's pick: "Zindagi Ek Safar Hai Suhana" (Andaz, 1971) over "Muqabla Muqabla" (both OK to him).
- Look liked. Change: a Mumbai-style red city bus (no logo, no lettering), less dusty. Outro v1 rejected: he hangs out of a window with a bar no bus has ("AI slop").
- Outro: the bus brakes, everyone lunges forward, the camera moves back out of the bus, then a drone shot moves outward and turns smoothly into a top shot.
- Brake at "Ab semiconductors par aaiye" agreed (the only time the wide aisle is shown); the outro has its own brake.
- Talking shots: mostly very close, switching to close for emphasis.
- Charts never pop in on their own: the camera goes into a phone screen, then the chart shows.

## Look v2 (2026-11-13), new Gemini chat https://gemini.google.com/app/0f046cf754cb4fc9 (refs: ref_face, ref_sheet, ref_look)
- Frames (sparkle cleared, kf/): R1_veryclose_full_c.png (most lines), R2_close_crop.png (900x1600 crop of R2_close_v2_c.png, emphasis), R3_wide_full_c.png (brakes), R6_phone_c.png (green screen, charts enter here), R4_front_out_c.png (outro, Tata grille logo painted out with cv2.inpaint), R5_topdown_c.png (outro end).
- Gemini lesson: in a follow-up prompt, "same ... as your last picture" made Gemini return the previous picture unchanged (twice in each chat). Start each prompt with "A NEW shot/framing, different from your previous pictures" and describe it in full.
- Gemini drew a real Tata logo on the bus grille: check every vehicle for a maker's logo.
- clear_sparkle picked margin 192 on R2/R3 and missed the star: SPARKLE_MARGIN=64 fixed it.

## Akhilesh, 2026-11-13 (look v2 review): the Dil Se look
- References: work/sk06/refs/dilse_1.webp, dilse_2.webp (Dil Se, 1998, bus scenes). Wanted from them: the camera style, the light, the video style and the bus (old but well kept). Look v2 was "very modern-looking". Not a request to seat him, but a seated try is welcome.
- Loop: the opening is the reverse of the outro: from the top shot the camera comes down and into the bus through the front windscreen; the reel ends going back out to the top shot, so it loops.
- Style refs are described in words to Gemini, not attached (real actors' faces must not reach our character).

## Look v3 (2026-11-13), Dil Se style, Gemini chat https://gemini.google.com/app/d73a55f382691608
- Frames (kf/, sparkle cleared, *_c.png): V1_veryclose (most lines), V9_close (emphasis), V2_seated (option: seated at the window), V3_wide (brakes), V6_phone (green screen), V4_front_out (classic red bus with a cream stripe, no badge), V5_topdown (high angle, middle of the drone move), V8_nadir (top shot: first and last frame of the loop).
- Prompt look line that worked: "late-1990s Hindi film shot on 35mm: soft overcast daylight from the windows, cool grey-blue palette, warm skin, low contrast, gentle grain, long lens, shallow depth of field"; bus: "older Mumbai city bus, well kept, not dusty: pale blue-grey painted metal walls, worn chrome rails, glass windows in metal frames, blue vinyl seats".
- Gemini repeated the previous picture again for a similar prompt (V7 = V5); a differently worded prompt ("nadir, like a map view") worked.
- In V4 Pandey shows through the windscreen, but his bowl cut is not clear: fix in the video start frame if the loop needs him readable there.

## Akhilesh, 2026-11-14 (look v3 review)
- "Bus looks perfect now", top shot and drone shot approved. Look v3 is the look.
- Standing only: no seated shots (V2 dropped). Very close (V1) for most lines, close (V9) for emphasis, wide aisle (V3) only at the brakes.
- No phone shot (V6 dropped). Charts: hard cuts between the chart and Pandey, or the vertical split (chart above, Pandey below).
- Go ahead with the voice.

## Voice blocked (2026-11-14 00:05 IST)
- voice_cut.py: every take failed. ElevenLabs error 401 payment_issue: "Your subscription has a failed or incomplete payment. Complete the latest invoice to continue usage." (tts_elevenlabs.py --check: creator plan, 71,645 / 121,556 characters used, status past_due). Only Akhilesh can pay. Rerun when fixed: `python3 pipeline/voice_cut.py work/sk06/voice_lines.json work/sk06/voice --monologue-takes 3` (delete work/sk06/voice first; nothing usable is in it).
- Song for the offline test: music/src/zindagi_ek_safar_saregama.webm (Saregama Music's YouTube upload -8rhkzEMVdQ, 321 s, 4.8 MB); never in the final.

## Voice cut (2026-11-14), work/sk06/voice/sk06_voice_cut.mp3, 91.6 s, cut transcript 99%
- Takes chosen by Scribe and speed, not voice_cut's slowest-take rule: P1_t1 P2_t3 P3_t3 P4_t3 P5_t2 P6_t1 P7_t2 P8_t2 (the slowest-take cut was 97.9 s: sk06_voice_cut_slowest.mp3). takes_all.json lists every take.
- Names: Centum (Scribe "Sentum" on some takes = right sound), Agnikul (P2_t1 said "Adunikul": avoid), Kaynes said "केन्स" (P7_t2), MTAR 0.44 s in P4_t3 (likely "em-tar"; P4_t1 0.84 s).
- Listen points in the cut: MTAR 0:34, "par" heard "pe" 0:48 (P5_t2 alone transcribes "पर"), "ee businesses" heard "e-businesses" 1:18 (dialect ई before an English word), "ab ee chaaron" heard "ab in"/"abhi" ~1:21.
- prosody (qcpy): shape_r 0.01, phrase_sd 2.09, pace_cv 0.18, pause_cv 0.5, tail_fall -2.3: not a flat read.

## Voice v2 (2026-11-14): work/sk06/voice2/sk06_voice_v2.mp3, 104.4 s, Scribe 99%
- eleven_v4, direction_v2.md (commas, dashes before focus words, 4 kinds of tags), stitched to neighbouring lines, 3 takes a line, picked by prosody and name clarity: P1_t1 P2_t3 P3_t1 P4_t3 P5_t2 P6_t2 P7_t1 P8_t1.
- Breaths removed with pipeline/debreath.py; pauses placed by build_cut.py (brake gap 52.52-53.92 in voice time).
- Sound preview: work/sk06/sfx/preview_test_song.mp3 (song test, listening only) and preview_no_song.mp3; cues.json = Edits cue sheet draft (A from 0:07.48 song 1:16.30 low; mute 0:52.64-0:54.04; B to 1:32.24 low; mute; C from 1:45.66 song 0:18.48 full).
- Sound tools checked: kerf (PolyForm Noncommercial licence, unsigned macOS app) not used; ffmpeg-skill (MIT, FFmpeg wrappers incl. beat detection) not installed yet, offered.

## Preview v2 (2026-11-14)
- P8 retaken with the body's tag: P8_t4 (136 Hz, -17.8 dB like the body). Voice v2 now 104.57 s.
- Brake: brake_bus.wav = ElevenLabs busbrake_v3 (groan + air hiss) + lurch_rattle; no tyre squeal. Mixkit "Old bus arrival" (real, licence free) was outside the bus with a tonal squeal: not used.
- Loop: voice starts at 1.30 s; song S1 full 0-1.30 from song 0:25.98 (where C ends), S2 low to the brake, mute, B (verse 2 from 2:06) low under the payoff, mute under the outro brake, C full from 1:46.97 (song 0:18.48) to the end 1:54.47. One gain for the whole song. cues.json.

## Graphics gate (2026-11-14), proposal sent with gfx/sk06_graphics_mock.jpg
- Hook text on the top shot from frame one; names on the word, above his head (never over his face); real weekly TradingView charts in the silver01 split (chart above, yellow divider, Pandey below, eyes at y 830) and as hard cuts; the four charts together on "Ab ee chaaron"; plant photos and official logos for CG Semi / Kaynes; disclaimer on the top shot at the end; DOORDHAN bug top right; no burned captions (silver01); cinema look, charts clean.
- Marks on charts: recommended = draw only what he names (support, resistance, MTAR's range), no prices, no targets, no arrows; alternative = plain charts.
- TradingView in the built-in browser looks signed out; the "Claude" layout URL returned 403 "Chart Not Found". The public chart works (NSE_DLY, delayed). Centum weekly last close 4,481.1 (13 Nov 2026).
- Face positions (mediapipe): V9 close eyes 0.455 / mouth 0.575 of height; V1 very close eyes 0.481 / mouth 0.651.

## Graphics and editing direction (Akhilesh, 2026-11-14, second review)
- Reference reel for text and editing: instagram.com/p/DX4XksWJlLL (vidIQ walkthrough: yellow heavy condensed caps + white handwritten word, 1-frame pop with a bass thud, often behind the speaker's head; gold serif captions phrase by phrase; motion-matched cuts, punch-ins, whips with whooshes; ASL ~2 s, longer holds to read). pipeline/bgswap.py --text already makes this look (words behind the person).
- "The editing has to be top-notch and creative": cuts matched to the dialogue, sounds and music.
- Charts full screen only (no split), held a few seconds, support/resistance drawn as in silver01.
- Opening: speak from the first frame; the voice runs over the drone dive; when the camera reaches Pandey his lips are in sync (talking clip starts in the pause after "karte hain?", ~2.1 s reel, using the pause as Wan's lead).
- Graphics only when needed; company logos on their names (official files, e.g. logos/centum_logo_blue.png from centumelectronics.com).
- Mock: gfx/sk06_graphics_mock_v2.jpg. On very close shots the caption goes low (y 985) to stay off the chin.

## Production tests (2026-11-14), 42 of 195 credits spent
- T1 hook line: Wan 3.0 (job 729a31c1, 10.5 cr) ACCEPT_WITH_SHIFT -160 ms; lips mean 2.8 % of face height (p90 4.9), 0 blinks in 6 s, framed a little wider than the reference. Wan 2.7 (job 0903d0a6, 9 cr) ACCEPT_WITH_SHIFT -100 ms; lips 4.4 % (p90 7.4), blinks, eye moves 1.3/s, one pouted "o"; exact framing. Real speaker 3.5-3.8 %.
- Dive S1: Wan 2.7 start V8 + end V1, 720p 5 s, 7.5 cr (job efc22c45): one coherent path top -> windscreen -> aisle -> face, lands exactly on V1. Seedance 480p 15 cr (job bb2cea38): also coherent, softer (480p 24 fps), lands wider. Camera moves: Wan 2.7 with start+end frames.
- Seedance 2.5 at 720p costs 7 cr/s (35 for 5 s); 480p 3 cr/s.
- Openings for Akhilesh: vid/opening_A_wan3.mp4, vid/opening_B_wan27.mp4 (test_opening.py).
- shot_spec.py: added pandey_animated base and male pronouns for the cinema texts (the cinema prompts were written for Rashmi).
- Segments: seg/segments.json, 15 talking shots (56.8 s); "Ab semiconductors par aaiye" (1.65 s) is voice-over on the post-brake wide.

## Opening v2 and the full talking batch (2026-11-14)
- Akhilesh picked A (Wan 3.0). His notes on v1: the zoom into him too fast; his voice played while his lips were still during the approach.
- T1p (Wan 3.0 push-in, 8 s, 14 cr, job 5dbb6fd0): camera glides from the aisle to very close while he speaks P1. Used reel 1.2-3.4 with src_in -0.36 s; T1w3 from 3.4 (punch-in on "ignore") with src_in -0.22 s. Opening lip sync PASS 0 ms (vid/opening_v2.mp4, test_opening_v2.py).
- Sign mistake found: the A/B openings used +shift; the lips there ran ~360 ms late.
- 11 talking shots submitted (96.25 cr): T2b T3a T3b2 T4a T5b T5c T6a T7a T7b T8a T8b. T2a, T3b1, T4b became voice-over on real pictures (startup logos/launches, Centum hardware, MTAR engines). Spent 152.25 of 195.

## Opening v3 and the batch judgement (2026-11-14)
- Akhilesh on v2: "it has to be like a continuous shot till the first actual cut"; v2 cut at "karte hain". He asked whether I watch videos before sending: I check frame sheets and measure sync; I missed the jump in the sheet.
- v3: dive S1_wan27 0-2.5 s over reel 0-1.6; seam frame = dive at 2.5 s (kf/S1_seam_2p5.png) = start image of T1g (Wan 2.7, start + end image + voice from 1.48, 5 s, 7.5 cr, job f84af092); seam difference 3.2/255; glide lips -160 ms taken up by playing the glide's first 0.38 s over 0.54 s (silent pause); first real cut 5.62 s into T1w3. Frame-change scan: no spike at the seam; lip sync PASS 0 ms. test_opening_v3.py.
- Batch of 11 (Wan 3.0): T2b ACCEPT; T3b2 (-140), T5b (-100) ACCEPT_WITH_SHIFT; RETRY weak lips: T3a T4a T6a T7a T8a T8b; UNSURE: T5c T7b.
- mouth_meter: T5c lips 0.7 % / 0.4 cycles/s and T7b 0.4 % / 0.0 cycles/s: the mouth barely moves -> retake. The other nine open 1.5-3.8 % at 1.7-3.1 cycles/s (real speech); SyncNet and corr both unreliable (Pandey's moustache hides the upper lip). T4a reads a steady +400 ms. Needs a visual check with large mouth crops against the voice before the edit.
- Spend 159.75 of 195.

## Opening v4 (2026-11-14)
- Akhilesh on v3: "so much better"; wants text inside the scene (LONG-TERM in yellow along the red roof, large, not overflowing) and one grade (the Wan 2.7 -> Wan 3.0 change at "doosra" was visible).
- Grade: grade_match.py, Reinhard Lab transfer measured on T1g's very close end against T1w3 (12 frame pairs), applied to S1_wan27 and T1g. Lab at the 5.62 cut now 84.2/127.6/129.7 -> 86.4/130.1/130.7 (v3: a visible jump).
- Roof word: roof_text.py. The roof is seeded by colour in frame 0 (after the grade the roof is a milky red, S 55-80, so a "saturated red" mask misses it and picks taxis), then tracked as a plane: LK points inside the roof, RANSAC homography frame to frame. The word lives in roof coordinates (Anton, rotated to read rear -> front, 80 % of the roof width, 88 % of its length), worn with a fixed noise and lit by the roof's own light (the vents show through). On from frame 0, fades clip 1.38-1.62 (reel 0.88-1.04) as the roof turns oblique. Debug copy with the tracked outline: vid/S1_wan27_track.mp4.
- First real cut 5.62: 1.2x punch-in on T1w3 about the eyes (0.509, 0.475), so it reads as a move in.
- Checks: frame-change scan: no spike at the 1.60 seam; 5.63 = the cut; 1.2-1.5 = the fast dive (as v3); 3.63 = a passenger crossing the foreground (as v3). Lip sync 2.3-7.3 s PASS 0 ms (SyncNet conf 2.34; corr 6 ms).
- Tool to generalise later: plane-tracked text (any flat surface) -> pipeline/, for the other in-scene words.

## Full production (2026-11-14, after "this looks perfect" on opening v4)
- Akhilesh: "produce the full video now"; "make sure the cuts are clean and punchy", use Remotion "wherever required". The whole picture edit is a Remotion composition now (rm/src/Reel.tsx, fx.tsx): hard cuts on words, punch-ins (instant 1.18-1.2x with a 3-frame settle), whips with directional motion blur and mirrored edges (HW 0.2 s, the cut at peak speed), zoom-throughs into the charts, logo cards slammed on their names, kinetic words, gold Playfair captions, the bug, the disclaimer. Sound in mix.py; finish.py muxes, upscales to 1080x1920 30 fps with light grain, writes the QC manifest.
- Budget: the raise to 215 was not answered, so production stayed inside 195: T5c and T7b retaken on Wan 2.7 (5 s + 7 s, 18 cr), the mid brake wide (4 s, 6 cr), the outro move V1 -> V8 (6 s, 9 cr). Spent 192.75 of 195.
- Lip check of the Wan 3.0 batch (bilabial_check.py: mouth crops around p/b/m words; gap_plot.py: lip gap vs loudness with the cross-correlation): Wan 3.0 lips lead the voice by 0.1-0.16 s on most shots and mouth on after the line ends. Shifts used: T2b -0.10, T3b2 -0.15, T4a +0.38 (late), T5b -0.15, T6a 0, T8a -0.08, T8b -0.12. T3a and T7a: the lips did not follow the voice (still on "phir aati hai", ~1 s late) -> voice-over on the Centum building / a Kaynes card. T8b: lips still on "Entry ke waqt" -> that part over the aisle glide. Wan 2.7 retakes T5c2 / T7b2 PASS 0 / -40 ms with SyncNet confidence 2.8-3.0: for Pandey's moustache, Wan 2.7 gives clearer, measurable lips than Wan 3.0.
- Outro: Wan 2.7 start V1 (very close) + end V8 (the opening's top shot), 6 s: holds on him, pulls back down the aisle, out through the windscreen, rises to the top shot; its last frame matches frame 1 (check/loop_pair.png); LONG-TERM painted on its roof too (roof_text.py --from-end). The top-shot end plays at half speed under the disclaimer.
- Charts: real TradingView weekly screens (Jan 2025 - Nov 2026) through takeClientScreenshot + the bridge; marks placed from TradingView's own price/bar coordinates (tv/calib.py: header 26.9 px, x offset 9.9 px). Centum: resistance 5,000 (Sep high), support 3,450 (Jun-Aug lows), BREAKOUT? and a momentum arrow; MTAR: run-up arrow 3,309 -> 8,714, range box 5,250-8,450 since May 2026, RANGE, BREAKOUT?. No prices, no targets.
- Pictures (sources in broll_in/sources.md): Agnikul, Skyroot, Pixxel (their sites/media kit), Centum (annual report, building + cleanroom: no space-hardware photo found), MTAR (mtar.in, soft), Micron Sanand (PIB), CG Semi (site + PIB), Kaynes Semicon (site). Rights are Akhilesh's call.
- Song cue sheet rebuilt for the final timeline: cue_sheet.py -> sfx/cues.json.

## The QC gate (2026-11-14, three runs) and what changed
- Final: outputs/sk06/E16_space_semis.mp4 (112.57 s, 1080x1920, 30 fps, 88 MB; phone copy 24 MB). Built: Remotion render
  (rm/), spliced patches for each fix (edit/sk06_v6.mp4), finish.py (mix, mux, upscale, manifest). Added grain made a
  995 MB file: removed.
- Run 1 -> fixes: L4 (T4a) drifted from late to early inside the shot -> "NO. 2" MTAR card; L7 (T6a) unmeasurable ->
  "NO. 1" CG Power card (and "NO. 1" on the Centum building, so both sectors count their names alike); L10 (T8b) under 2 s
  -> the cut into T8b moved to 102.85 and the outro to 104.85 (outro clip from 0.1 s; brake 104.86; song cues moved).
  A bug found on the way: the outro's slow-motion top shot was a frozen frame (an OffthreadVideo mounted mid-Sequence
  counts from the Sequence start): wrapped in its own Sequence.
- T5b: SyncNet and the lip-gap correlation disagree (shift -0.15: SyncNet windows +600/-560/0, corr -95; -0.23: SyncNet
  +80 const, corr -28); settled at -0.19 (SyncNet 80/40/40, corr -70).
- Run 3, BLOCKED on four rows, all for Akhilesh's call (waive) or new takes (no budget left):
  lipsync L5 (T5b weak lips, +40 median, one window +80; corr -70), lipsync L10 (T8b, SyncNet no confident window; corr
  -4 ms r 0.59), face L1 (0.52 vs 0.55 at 4.0 s: the approved glide, motion blur, clearly Pandey), mix L3 (the quiet creaky
  "हैं" after "ban sakte" counted as a breath; Scribe hears it, the script check passes). Evidence clips sent.
  Alternative to the two lip waivers: T5b and T8b again on Wan 2.7 (about 10.5 credits; needs the raise).
- Akhilesh waived the four rows (2026-11-14: "Wave all four for now and give me the full video. Let me check, and let me
  come back if we need the retake or not."). Gate run 4: PASS with L5, L10, face L1, mix L3 waived; phone copy stamped and
  sent. Open: his review; a possible Wan 2.7 retake of T5b and T8b (about 10.5 credits, needs a raise).

## v2 after Akhilesh's review of the full reel (2026-11-14)
His notes and what was done:
- "When you shift from 3.0 to 2.7 ... you are changing the person itself, his skin also changes. That cannot happen. I like
  the Pandey after doosra." -> every face shot on Wan 3.0 (budget raised to 250, his answer "Raise to 250 (Recommended)"):
  A1 (the approach up the aisle, 5 s; hidden cut at the windscreen with a light bloom at 1.45 s; lips +0.23 s late -> c = r - 0.69),
  B1 (the brake), T7b3, T8b3, T5c3/T5c4 retakes. The outro starts at clip 0.9 s (his Wan 2.7 face already small, under the brake shake).
- The zoom-in face "distorted, then gets clear" (the Wan 2.7 glide) -> A1 (Wan 3.0, sharp all the way in).
- Startup logos one below the other over the B-roll -> stacked cards on their names.
- Words behind his head: covered by hand and head; and "listed, unlisted, watchlist, really?" -> UNLISTED x2 and WATCHLIST
  removed; SPACE and SETUP kept, set top-right of his head (clear of the raised hand), 130-140 px, readable;
  SEMICONDUCTORS in front, low.
- Company intros "boring, not a pro editor" -> Montage (fx.tsx): a cut on every key word, impact zoom 1.12 -> 1 in 0.16 s,
  2-frame flash, alternating tilt, NO. 1 / NO. 2 slams with shake, logo slams; real footage where found (footage_in/).
- MTAR pictures blurry -> sharp stills and footage (footage_in/mtar).
- The brake: people stayed seated? they got up -> B1: the camera (part of the bus) is thrown back, seated passengers
  jolt, Pandey stays put; the camera returns and HE says "Ab semiconductors par aaiye" (the jolt part plays 1.27x, no words there).
- Semis B-roll boring -> fast-cut real footage (Micron Sanand etc.).
- CG Power and Kaynes: charts instead of B-roll (with the CG Semi / Kaynes Semicon logos on their names).
- "Entry ke waqt": no aisle zoom-in -> the whole line on his face (T8b3, Wan 3.0, lips 0 to +40 ms).
- Lesson: the old retry prompt still said "his lips part only a little ... the jaw moves little": that wording gave still
  lips on Wan 3.0. "He articulates every syllable clearly, lips and jaw moving visibly ... never exaggerated" gave
  measurable lips (T7b3 SyncNet conf 3.8-4.9, T8b3 3.4).
- v2 final (outputs/sk06/E16_space_semis.mp4, 111.77 s): gate PASS with six rows waived by Akhilesh ("Waive all six",
  2026-11-14): lipsync L4 (B1, camera moving), L5 (T5b), face L1/L6/L7 (0.54 vs 0.55), mix L3 (the quiet "हैं"). Sent.
  Spend 245.25 of 250. Footage sources: footage_in/sources.md. NDTV captions found at the ends of two Centum clips by
  checking every montage item's last frame: always check each clip across its whole shown span, not one frame.

## v3 after Akhilesh's notes on v2 (2026-11-14)
- Into the bus "feels broken": the dive's interior (dark, standing crowd) never matched A1's (bright, seated). Now the camera
  passes THROUGH the pane: at 1.28 s the dive (windscreen filling the frame) opens with a radial mask from the centre while
  scaling 1 -> 1.45 and blurring, A1 at full size behind it (scaling A1 below 1 showed its edges).
- A1 lips: "dialogue a little early": Wan starts his lips ~0.3-0.4 s after the voice at the start of the approach; shift
  now +0.30 s (c = r - 0.62); gate L1 lip-sync PASS.
- Whooshes: none on montage cuts; four soft ones on the big whips; zoom-throughs get a low thump only.
- Brake: retake B1b (Wan 3.0, 7 cr, budget raised to 260): the inertia prompt ("every seated passenger is pitched sharply
  forward toward the camera at the same instant ... nobody stands up; only he does not move") worked; lips 0 ms (conf 2.45).
- Charts recaptured at 724x906 (viewport 1110x900; the hidden pane needs a fresh page load or an 8 s wait after
  setSymbol), March 2025 to now, full width on a white page like silver01; the camera zooms to the recent bars; CG Power
  (resistance 975, support 775) and Kaynes (resistance 4,000, support 3,050) marked on their words.
- Disclaimer: big kinetic type, two groups of four lines fitted to the width, flying out; last frame clean for the loop.
- Song preview: mix_song.py + finish_song.py -> outputs/sk06/E16_space_semis_SONG_PREVIEW.mp4 (review only); its own
  gate run (the song lyrics fail the script row, as expected).
- Gate v3 final: BLOCKED on L5 lips (T5b), face L1 (0.53), L6, L7 (0.54), mix L3 ("हैं"); L4 now passes.
- v3 final and SONG_PREVIEW: gate PASS with Akhilesh's waivers ("Waive and send both", 2026-11-14): L5, face L1/L6/L7, mix L3; the song preview also script:extra (lyrics). Both phone copies sent.
- 2026-11-14 13:10 Final approved by Akhilesh ('alright this is okay. Give me proper video to post.'). Post file copied to My Drive/Doordhan finals/E16_space_semis_POST.mp4 (93 MB, same sha256 as the stamped final). Posting kit: post_kit.md (compliance PASS). First designed cover: pipeline/cover.py + cover.json (A 'AGLA BOOM?' recommended, B 'IGNORE MAT KARO'); docs/covers.md. Registry: episodes row 16, assets wardrobe/keyframes/clips, reels.csv E16, format cost line.
- 2026-11-14 13:20 Cover v2 on Akhilesh's notes ('agla boom? is good'; Pandey cut out only, the rest for space and chips, labels readable on a small screen): pandey_cut.png from V1_veryclose_c (crop 0.16,0.19,1,1), rocket placed lower to show its nose, labels 150 px. Drive copy replaced, B removed from Drive.
- 2026-11-14 14:10 Cover v3 on Akhilesh's note ('very boring ... slop', research creative thumbnails, high quality): research on 60 thumbnails (Cleo, Think School, Veritasium, Johnny Harris, Shivanshu); Gemini scenes with V1 as reference via the bridge: busrocket_a1/a2, chiprocket_b1, busrocket_a3_chip (a2 + one edit, face 0.76); type layer now HTML/CSS rendered by headless Chrome (pipeline/cover.py v3). Final E16_cover.jpg (bus + chip, 'SPACE & CHIPS / AGLA BOOM?'), alt E16_cover_alt.jpg. Drive updated.
- 2026-11-14 14:35 Akhilesh chose cover B ('I like the B version'): E16_cover.jpg = chiprocket_b1 (zoom 1.06, shift 60 to push the sparkle out of frame; rocket nose clears the box), alt = bus scene. Drive updated.
