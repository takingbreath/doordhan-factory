# sk06 (E16): the bus monologue, a Remotion edit with real footage and TradingView charts

Template for a Pandey monologue outside the Kendra office (E16: standing in a packed Mumbai bus, Dil Se film look),
cut in Remotion. It covers a drone opening through the windscreen, a mid-reel brake, montages of real company footage,
full-screen TradingView charts with marks, kinetic words, a big kinetic disclaimer and a loop back to frame one.
111.8 s, 252.25 credits, approved by Akhilesh 2026-11-14. The story of every version and every fix is in
`production_log.md`. **The prompts for every stage, cleaned up as templates: `PROMPTS.md`** (start there). The lessons are in registry/episodes.md (2026-11-14) and the produce-video gotchas.

Copy the folder to `work/<slug>/`, then `cd rm && npm install` (Remotion 4.0.538, local, no global install). The media
(clips in `vid/`, footage in `rm/public/f/`, chart captures in `rm/public/img/`, voice, sfx) are not in git. Rebuild
them as the scripts say. The paths inside the scripts say `work/sk06`, so change them to the new slug.

| File | What it does |
|---|---|
| rm/src/Reel.tsx | The whole edit as one composition: scene times, talking-clip mapping (`c = r - 0.12 - cut_start + 0.5 + shift`), montages, charts, captions, overlays. Constants at the top (OUT0, GLASS, SLOW_AT, TOTAL). |
| rm/src/fx.tsx | The library: whips, punch-ins, Clip (src, c0, rate, scale, centre, mask), Photo, LogoCard, BigWord, Captions, ChartView with camera keys, DrawLine/Label/DrawArrow/DrawBox for chart marks, Montage (impact zoom and flash), shake, KineticDisclaimer. A video mounted mid-scene sits in its own `<Sequence from>`, or its time counts from the parent start. |
| rm/stills.mjs | Bundle once, then render stills at given frames, to check the edit without a full render. Render patches with `--frames=a-b --timeout=90000` and join them with ffmpeg concat. |
| rm/public/data/media.json, charts.json | The montage lists (clip, in-point, length, dim) and the chart captures with their price-to-pixel calibration and marks. |
| tv/calib2.py | Calibrates a TradingView capture (the highest wick gives price to pixel). Captures come from the built-in browser with `takeClientScreenshot` and the Gemini bridge (pipeline/gemini). Zoom with `timeScale().zoomToBarsRange`. See the produce-video gotchas. |
| roof_text.py | Paints a word on a tracked surface in a moving shot (LONG-TERM on the bus roof): a seeded colour region plus a homography tracker. |
| opening_dive.py | The drone dive, sped up to land on his face (the opening test that was approved). |
| grade_match.py, grade_apply.py | Measure and apply one Lab colour transfer, so that Wan 2.7, Wan 3.0 and Seedance clips read as one camera. |
| mix.py | The sound: the voice at 0.12 s, the bus bed (lower in "away" scenes), the street outside, brakes, a glass whoosh, whooshes only on big whips, thuds on words, logo pops, marker sounds on chart marks. Two-pass loudnorm to -14 LUFS. |
| finish.py | The prefinish edit, the dialogue stem, the 1080x1920 final, the phone copy and qc_manifest.json for the QC gate. |
| cue_sheet.py, song_cues.json | The cue sheet for the song that Akhilesh lays in Instagram Edits (clip, reel time, song in-point, level). |
| mix_song.py, finish_song.py | A song preview for review only (never posted): the song on the cue sheet over the reel's own mix. |
| bilabial_check.py, gap_plot.py, mouth_strip.py | Lip checks for a moustached face where SyncNet is unreliable: p/b/m closures, lip gap against loudness, a mouth strip. |
| specs/*.json | The Wan 3.0 talking-shot specs that worked: the keyframe as an image reference with our track, and "articulates every syllable clearly, his lips and jaw moving visibly" (a wording of "lips part only a little" gave still lips). |
| kw/*.json | The words behind his head (bgswap.py --text): word, position, size. |
| cover.json, cover_alt.json | The E16 cover (pipeline/cover.py, docs/covers.md). The chosen cover is cover.json. |
| voice_direction.md, voice_lines.json | The voice direction (affect, pace, arc, tags) and the directed lines sent to eleven_v4. |
| post_kit.md, footage_sources.md | The posting kit and the source of every footage clip (credits line). |
