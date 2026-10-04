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
