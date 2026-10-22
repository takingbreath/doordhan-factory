# sk05 (eMudhra, Pandey monologue): revision handoff, 23 Oct 2026

v1 final (cloud session, QC gate PASS, 92.0 s, sha256 f10e52672193) was rejected on the graphics and the camera.
This branch (`sk05-handoff`) carries everything needed to rebuild and revise it. Don't merge it into main:
work/ is git-ignored on purpose. Copy work/sk05 into your checkout's work/ and work there.

## Akhilesh's notes on v1, verbatim
> Graphics are very boring.. and everything is shaking. Idea is to you shake something when you need to put emphasis
> on it. The picture you added of the reporter is good but you could have dropped it.
> This is kind of animation I want https://www.instagram.com/reel/Det3bEqtRh2/

(Ask him what "could have dropped it" means before acting on it: either "it was fine but not needed" (cut it), or
"you could have dropped it in" (animate the photo falling into frame). The cloud session couldn't tell.)

## What the reference is
@sanji.chien's reel, captioned as Vox-style motion design made with Claude + Higgsfield MCP + **Seedance 2.5**
(the caption says a prompt can swap the background, change the person or update a chart). The video itself couldn't be
watched from the cloud: **get screenshots from Akhilesh, or watch it with him**, and write down the moves you see
(how elements enter, the camera, the depth, the transitions) before designing anything.

Our v1 collage was local 2D: stickers popping on a kraft plate, with a constant stop-motion boil, a slow drift and a
slow camera push on every scene, plus handheld sway on every Pandey shot. Result: flat and jittery at the same time.

## The direction for v2
1. **Still by default; shake only for emphasis.**
   - Pandey's talking shots are locked off. Keep the snap zooms, the focus hunts and the short shakes, but only on the
     punch beats: "Nahi", "atharah mahine", "To AUDIT", "sab changa si?".
   - In build.py: `cam_at` gets `hand=0` by default, a short shake burst after a snap, and no sway on the split
     (`handheld()` becomes a static crop).
   - In scenes.py: elements hold perfectly still once they land. No `drift`, and no `boil` except, at most, a very
     subtle one on photo cut-outs (Akhilesh asked for that on 22 Oct). No constant `camera()` push. Motion only when
     something happens: an entry, a stamp, a move to the next idea.
2. **Animate the collage the way the reference does.** Compose a collage keyframe per scene locally (the real
   pictures, our paper plate), then animate it on Higgsfield with Seedance 2.5 (or whatever the reference's workflow
   uses), and lay text and logos on top locally afterwards.
   - Video models garble text, and hard rule 4 says never let a model draw the eMudhra logo.
   - Seedance has flagged split-screen start images as NSFW before; it's refunded, so just retry with a single frame.
   - First a 4-5 s test on one scene (the chart, or the DigiNotar fall) to Akhilesh. Then the rest.
3. **Budget:** 62 of 75 credits spent, 13 left. Seedance 2.5 at 480p is 3 credits/s. The collage covers about 70 s of
   the reel, so a full AI pass is about 210 credits.
   - Ask Akhilesh with a breakdown before going over (hard rule 2).
   - Cheaper mix: AI motion on the 5-6 strongest beats (about 20-25 s, 60-75 credits), with the rest local but rebuilt
     with purposeful motion.
   - Check `models_explore` for a cheaper model that fits.
   - E11 used gemini_omni collage clips (54 credits for the episode); see registry/episodes.md row 11.
4. Then rebuild, run the QC gate, and send the stamped final plus the QC png. Write down what was learned:
   docs/realism.md or formats/sahayata_kendra.md, and the episode row after approval.

## State
- **Script:** registry/scripts/sk05.json, frozen 765f4506, approved by Akhilesh. Voice: voice/sk05_voice_cut.wav
  (approved take, 91.65 s).
- **Spend ledger:** work/sk05/spend.json. Run `python3 pipeline/spend.py start sk05` on the laptop so the guard
  sees it; it keeps the ledger.
- **Talking clips:** vid/T1-T5.mp4, all accepted by shot_spec judge. T3 runs with a -0.08 s source shift (in build.py).
- **Silent clips:**
  - vid/B_shock.mp4: Billu startled, job 53b70ce4-5f0d-4e68-a227-2032fd1dbb72.
  - vid/B_turn.mp4: Billu turns away, job 4b6d92d9-7aaf-430d-9dee-6e108f0f87e5.
- **Keyframes:**
  - kf/front_a.png, the master (Higgsfield job ba053029-6b02-40b2-81bd-d2ac624ce30a).
  - kf/B1.png, Billu.
- **Real pictures:** real/, with sources and quotes in real/SOURCES.md. The TradingView chart, Rob Stradling's GitHub
  avatar, Mozilla bug 1970728, the eMudhra statement pages, The Register 2011, the Business Today exit headline.
- **Caption timings:**
  - voice/words_whisper.json (Whisper, good up to 63 s).
  - qc/scribe_final.txt, Scribe of the v1 final. Scribe word times are in reel time = voice time + 0.15.
  - The CAPS list in build.py is already timed.
- **Code:**
  - scenes.py, the 15 collage scenes. Each scene's docstring gives its voice-time window and beat times.
  - vox.py, the E11 toolkit.
  - build.py: timeline, mockumentary camera, captions, mix and QC manifest.
  - camtest/cam.py, the camera test Akhilesh liked on 22 Oct.
  - Regenerate the collage clips with `python3 work/sk05/scenes.py [names]`; `PREVIEW=t1,t2` writes contact sheets.
- **Build:**
  - `pipeline/qcpy work/sk05/build.py`, with `PLAN_ONLY=1` for the timeline and `DRAFT=1` for a fast look copy.
  - Then `pipeline/qcpy pipeline/qc_gate.py work/sk05/qc_manifest.json`. With the ElevenLabs key, the gate
    transcribes by itself.
- **Kept from v1:**
  - The split opening and close, with a loop to the first frame. The first frame must show the eMudhra logo.
  - The SSL VERIFIED stamps (Akhilesh's ask).
  - The real falling chart.
  - Billu shocked (snap zoom on him) and Billu turning away after "sab changa si?".
  - Captions at y 1000; graphics stay out of the y 960-1130 band.
  - The Register's real headline says "titsup": flag it to Akhilesh or crop it.
- **Lip sync in v1:** offsets -40 to -100 ms, all pass. T1's drift figure is high (-111 ms/s), but over only 3 s.
