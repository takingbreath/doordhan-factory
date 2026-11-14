# Vox desk graphics (from sk05 / E13, 23 Oct 2026, Akhilesh's notes v1 to v7)

The look: real photographs of real, worn objects, filtered (dirty halftone, scanner lines, paper fibres), cut out with a scissor-cut paper rim, laid on a Gemini photo of a dot-grid notebook desk. Marks are drawn on with rough strokes, labels are marker handwriting on yellow tape, quotes are real clippings with a yellow highlighter, a typed value is a real screen that zooms. Every event starts on its Scribe word time. Rules and the story of the rejections: formats/sahayata_kendra.md section 5 and the memory notes.

## Steps
1. **Storyboard first**, one row per sentence: what Vox would shoot to explain THIS line (example_storyboard_sk05.md). Never reuse an old picture because it exists.
2. **Voice cut** and **Scribe word times**: transcribe the voice cut with `pipeline/transcribe.py --json`, keep the `words` as `[[start, end, word], ...]` in `rm/public/data/words_scribe.json` (see `wt()` in rm/src/lib/core.tsx).
3. **Photos**: Gemini (gemini-media skill). A sheet of six isolated real photographs on a white background per prompt (a desk plate: "top-down dot-grid notebook, props only at the edges, a clear centre"). `crop_sheet.py SHEET OUTDIR names...`, then `~/.venvs/doordhan-cut/bin/python pipeline/cutout.py` (a pale object, such as an envelope, by threshold), then `vox_filter.py IN.png OUT.png --color 0.3 --seed N`.
4. **Scenes**: copy rm/ to work/<slug>/rm, `npm install` there (Remotion 4, project-local), put the photos in rm/public/img/v and the desk in rm/public/img, write the scenes like rm/src/scenes/More.tsx (layout inside the Instagram safe area x 40..640, y 170..855), `./render_all.sh` -> gfx/<scene>.mp4 (720 wide). Chrome is used as the renderer (remotion.config.ts).
5. **Sounds**: `make_sfx.py` (ElevenLabs sound generation, files assets/audio/sfx_*.wav), then a per-scene plan on the word times (example_sfx_plan_sk05.py).
6. **Pandey (or any Wan face)**: `texturize_clips.py CLIPDIR names...` before the edit. Needs assets/models/selfie_multiclass_256x256.tflite (curl from storage.googleapis.com/mediapipe-models/image_segmenter/selfie_multiclass_256x256/float32/latest/). No eye repair.
7. Edit with the Kendra template (assets/edits/sk04_build.py or work/sk05/build3.py as a model): scene videos as shots, a Billu cut that lands on the words it reacts to, captions y 860 and at most 580 px wide, the DOORDHAN bug top right (right edge x = 700, y = 36).

Not here (episode-specific, rebuild per reel): the photos, the desk, the real screenshots, the scene timings.

## Curve cuts (Chris Moran, "cutting the curve"; sk05 v8, 23 Oct 2026)
- **Between scenes:** one heavy cubic ease out of the old shot and into the new one, the same speed at the cut, the cut at the peak of the speed, motion blur along the move, mirrored edges (not replicated ones: they smear into stripes). Code: `whip_at()` and `CUT_DIRS` in work/sk05/build3.py (HW = 0.22 s each side, 640 px sideways or 760 px up and down, one direction per boundary). Shots made by ffmpeg (the split shots) keep a plain cut.
- **Inside one composition:** an object (the "baton") rides ONE curve across the cut, so the new scene is parented to the old one: rm/src/scenes/CertPass.tsx (the padlock moves from the certificate scene into the password scene; the key and tag sweep away first; the desk framing changes at the cut under the blur).
- A whip lands on whatever the next scene shows first. Events start on their words, so the first beat of a scene is often an empty desk: let the first word of the scene land a moment after the cut, or start the new scene's hero on the cut.
