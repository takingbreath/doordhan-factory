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
- **Every rebuild needs a new transcript** (the binding is by file hash, about 230 ElevenLabs credits each). Make all
  fixes, look at full-size frames, then transcribe once.
- **YouTube blocks cloud machines** (yt-dlp, Piped, Invidious, cobalt). Clips come from the laptop: write
  registry/clip_requests/<slug>.json, and the laptop's hourly task runs `pipeline/fetch_clips.py --push` to the `clips` branch.
