# Directing ElevenLabs so a voice sounds told, not read

Written 2026-10-09 after Akhilesh heard nana01's first Rashmiji take as "very flat and AI-like, one pitch for the whole thing".

## What "flat" actually was
`pipeline/prosody.py` measured it. Take A's pitch range was normal (11.7 semitones, the same as the clone's own sample), so the voice wasn't narrow. What gave it away as read:

| | real speech (Nana, Lallantop interview, 60 s) | take A (v3, line tags only) | v4_2 (directed, picked) |
|---|---|---|---|
| shape_r: sentences share one tune | 0.14 | 0.39 | 0.19 |
| tail_fall: the same pitch drop at every full stop | −0.4 st | 3.0 st | 0.1 st |
| phrase_sd: sentences start on different notes | 2.08 | 1.34 | 1.88 |
| pace_cv: speeds up and slows down | 0.13 | 0.07 | 0.18 |
| pause_cv: pauses of different lengths | 0.78 | 0.30 | 0.26 (still too even) |

Measured creators (docs/voices/general/reference/rhythm.md) talk at about 4.3 words a second and pause 0.7 times per 10 words, with long run-on sentences. Take A was about 3.1 words a second and stopped at every full stop.

## How to direct it (words never change; only punctuation and tags do)
1. **Use eleven_v4 for cloned voices.** ElevenLabs' docs say v3 isn't fully optimised for clones. On the same text, v4 gave more pitch movement between sentences and pace variation twice as high. At the time it was also free on our plan, against about 700 ElevenLabs credits for a 40 s take on v3.
2. **Join clauses with commas instead of full stops.** Every "।" invites the same fall-and-stop. Keep full stops only where the thought really ends.
3. **Use one real pause, at the turn, not one after every sentence.** Put `...` before the reveal ("लेकिन फिर, TV पर…") and `—` for a short beat before a key word. Use `[pause]` once at most, at a change of scene.
4. **Tags go only where the feeling changes, about 4 per 40 s.** Our first tags were an opener, then `[softly]` for the grief, `[warmly]` for the turn and `[thoughtful]` for the close. A tag holds until the next one. Describe how the line is spoken (`[softly]`), not what she does (`[smiling]`).
5. **Devanagari has no capitals**, so the caps-for-emphasis trick only works on English words. In Hindi, a `—` beat before the word does the same job.
6. **Make 4 takes, measure, transcribe the top 2–3, then listen.** v3 and v4 are non-deterministic, so the same text gives different reads.

## Directing by beats (anthropic01, 2026-10-28)
Akhilesh asked for a voice director's pass after reading three skills: ElevenLabs' text-to-speech skill
(github.com/elevenlabs/skills), OpenAI's speech skill (github.com/openai/skills, .curated/speech) and the
product-launch-film skill (github.com/KJ-AIML/product-launch-film). What they add to the list above:
- **Write the direction before the text:** a short labelled spec (affect, tone, pacing, emotion, pronunciation, pauses,
  emphasis, delivery), then a beat table with each line's intention, the emotional shift, thought groups, at most one
  focus word per group, and where the pause or tag goes. Example: work/anthropic01/voice/direction_v2.md.
- **Change one thing per round** and keep the rest as it was (OpenAI). Audition on one or two lines, not the whole
  script, when only the voice is in question (KJ).
- **v4 can read a tag as a sound cue,** because it also makes sound effects. Tags must describe the voice ("[calm,
  matter-of-fact]"), not an event. v4 takes IPA in slashes (`/əˈmoʊdeɪ/`) for a name that comes out wrong, and STT
  every take: a misheard name gets context in the line rather than a respelling (KJ).
- **Request stitching** (`--previous-text/--next-text`, now in tts_elevenlabs.py) lets chunks know what is said
  around them.

What the experiment measured (Rashmiji, eleven_v4, 162 words; 6 full takes and 7 beats x 2):
| | v1 plain text (s4) | v2 directed, stability 0.5 | v2 directed, stability 0.3 | v2 per beat, stitched |
|---|---|---|---|---|
| tail_fall (real speech -0.4) | 2.6 to 3.1 st | -0.6 / 5.2 / -2.7 | 6.5 / 5.6 / 3.1 | 2.8 |
| length | 55.4 to 56.9 s | 55.2 to 55.9 s | 55.1 to 57.4 s | 62.6 s |
| words a second | 2.9 | 2.9 | 2.9 | 2.6 |
- Direction (thought groups, 5 tags, dashes before focus words) removed the newsreader fall in 2 of 3 takes. Pick by
  prosody.py, then Scribe's per-word confidence.
- Lower stability (0.3) did not help: more falls and more uncertain words. Keep the voice's saved 0.5.
- **Nothing moved the pace.** v4 has no speed setting. If a take is too slow, speed it up in the edit (atempo 1.1).
- **Ellipses are not reliable pauses on v4.** Two of three gave 0.04 to 0.08 s. Only the one after a question
  ("वही होगा? ... नहीं") gave a real pause (0.48 s). Add the pause in the edit by cutting into the quietest 5 ms of
  the gap (work/anthropic01/sfx/mix.py).
- **Per-beat generation was worse:** each chunk read slower (+7 s) and ended on a full fall. Keep one continuous take
  and put the pauses in the edit.
- Scribe writes "fifty point one percent" as "50.1%", so the script similarity and verify_line's must_say both miss
  it. The digits check passes, so compare the digits.
- **The hook needs its own energy** (Akhilesh heard v2's opening as "very low-sounding"). The "[casual, a little
  secretive]" opener made it 8 dB quieter than the body, at 196 Hz median against 247 Hz. A hook-only take tagged
  "[energetic, quick, like sharing big news with a friend]", ending in "!", with `--next-text` set to the next line,
  came out at 266-294 Hz, 3.4-3.5 words a second and 100% Scribe. Full takes with that opener carried the energy into
  the body but lost its variety (tail_fall 1.9-3.9, fewer phrases), so v3 joins the hook take onto the best body take
  in the first pause (work/anthropic01/voice/build_v3.py). Pick the hook take that ends rising into the next line
  (+2.1 st over its last 0.3 s), and check the pitch step at the join (-1.9 st was natural).
- The model: eleven_v4 is the latest (launched 28 Sep 2026; no newer v4 on the API or the models page, checked 28 Oct).
  tts_elevenlabs.py takes the model from the registry voice (rashmiji: eleven_v4). Sarika, Gupta and Pandey stay on
  eleven_v3 until someone tests them on v4.

## An energetic hook can sound excited (anthropic01, 2026-10-28)
Akhilesh asked for energy in the hook, then heard its second half ("jise tum kabhi khareed nahi paoge") as excited,
"the pitch is up when it is not supposed to be", and the energy drove Rashmi's face to over-act too.
- **Measure it:** `pipeline/phrase_pitch.py --split <first word of the phrase> AUDIO SCRIBE.json`: v3's hook sat
  +1.7 st (median) and peaked +6.0 st above the first half, the last word level (-0.5 st).
- **Retake calm:** "[calm, matter-of-fact] Anthropic list होने जा रही है, and एक share है, जिसे तुम कभी खरीद नहीं पाओगे."
  (eleven_v4, Rashmiji, three seeds) gave +0.3 st and a last word falling 6.7 st; a "[matter-of-fact]" tag on the second
  half only, with "..." before it, did worse (+2.7 st, a rising end on one seed).
- **Keep the edit's timing:** the calm take was 0.4 s longer. work/anthropic01/voice/build_v4.py speeds the new take
  just enough (x1.05, atempo) to fit the old slot and keeps the pause before the body, so every graphic, caption and
  cut after it stays where it was (checked by cross-correlation: 0.0 ms). Then re-time only the hook's own cues.
- For a calm explainer, direct "calm, matter-of-fact" and let a full stop end the line low; ask for energy in the
  delivery's pace, not its pitch.

## Still open
- **Pauses are still too even** (pause_cv about 0.3 against 0.78 in real speech). Next to try: generate per beat (3–4 chunks), with different lead-in silences cut in the edit.
- **Stability.** The connector can't set it. The API (`tts_elevenlabs.py --stability 0`, "creative") needs the key in `.env`. The voice's saved default in the ElevenLabs UI also applies.
- **Hindi focus words** carry a pitch rise on the word in focus. We have no tag that targets a single Hindi word reliably yet.

Sources: ElevenLabs prompting guide (https://elevenlabs.io/docs/best-practices/prompting); the ElevenLabs connector's model guide for eleven_v3/v4; Artlist's v3 guide (https://artlist.io/blog/new-eleven-v3/).
