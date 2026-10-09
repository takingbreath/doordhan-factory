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

## Still open
- **Pauses are still too even** (pause_cv about 0.3 against 0.78 in real speech). Next to try: generate per beat (3–4 chunks), with different lead-in silences cut in the edit.
- **Stability.** The connector can't set it. The API (`tts_elevenlabs.py --stability 0`, "creative") needs the key in `.env`. The voice's saved default in the ElevenLabs UI also applies.
- **Hindi focus words** carry a pitch rise on the word in focus. We have no tag that targets a single Hindi word reliably yet.

Sources: ElevenLabs prompting guide (https://elevenlabs.io/docs/best-practices/prompting); the ElevenLabs connector's model guide for eleven_v3/v4; Artlist's v3 guide (https://artlist.io/blog/new-eleven-v3/).
