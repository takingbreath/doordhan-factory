# How to make a cinematic monologue reel like E16 (the prompts that worked)

E16 (sk06, 2026-11-14) is Pandey standing in a packed old Mumbai bus, talking to the camera about two sectors. It has a
drone dive into the bus, real company footage, full-screen TradingView charts, a brake mid-reel, a big disclaimer and a
loop back to frame one. Akhilesh approved it after three rounds of notes. This file holds the cleaned-up prompts for
each stage: what produced the approved shots, rewritten as templates. `{slots}` are what you change for a new reel.
The raw log, with every try, is production_log.md. The code is in this folder (README.md).

Order: brief, look frames, voice, camera moves, talking shots, footage and charts, edit, sound, QC, cover. The gates
(script, format, voice, graphics, final) are in the /make-reel skill. Nothing paid is spent before the script is frozen.

---

## 1. The brief (write it before any prompt)

> A {length} monologue. {Presenter} stands in {setting}, close to the camera, talking to the viewer like the
> commuter next to them. Dry, matter-of-fact, a faint knowing half-smile, never a newsreader or a salesman.
> Look: {film reference, described in words}. The reel opens from {an establishing view} and moves into their face
> in one continuous shot. It ends by moving back out to the same view, so the last frame matches the first (a loop).
> One physical event mid-reel resets the topic ({E16: the bus brakes before "Ab semiconductors par aaiye"}).
> Pictures go on the words: logos on names, real footage of each company, full-screen charts with support and
> resistance marked. The SEBI disclaimer goes on screen at the end. The song is added by Akhilesh in Instagram Edits;
> the posted file has none.

Rulings from Akhilesh that shaped E16 (keep them for this kind of reel):
- One face model for the presenter for the whole reel (Wan 3.0). Mixing Wan 2.7 and Wan 3.0 changed the skin and
  the face: "That cannot happen."
- The opening is one continuous shot until the first real cut. The pass through the windscreen must feel like going
  through the glass, not like a cut.
- Very close shots for most lines, a close shot for emphasis, the wide aisle only at the brakes.
- Text only where it helps: logos on names, a few key words behind the head (SPACE, SEMICONDUCTORS, SETUP). He
  rejected weak words ("listed, unlisted, watchlist, really?").
- Company sections must look like a pro editor cut them: fast cuts of real footage, not slow photo pans.
- Charts are full screen, held long enough to read, levels marked on clear swings, zoomed to the recent bars.
- Few whooshes. Sound effects only where a real sound would be.
- The disclaimer is big and kinetic. It fills the screen as it leaves.

---

## 2. Look frames (Gemini Pro, 0 credits; pipeline/gemini)

Attach the presenter's character sheet and one approved face frame as references. Start every follow-up with
"A NEW shot, different from your previous pictures". Otherwise Gemini can return the last picture unchanged. Look at
every vehicle and sign for a real brand logo (Gemini drew a Tata badge on the bus grille). Describe film references in
words. Never attach stills of real actors: their faces must not reach our character.

**Look block** (paste into every frame prompt):
> Look of a late-1990s Hindi film shot on 35mm: soft overcast daylight from the windows, cool grey-blue palette, warm
> skin, low contrast, gentle grain, long lens, shallow depth of field.

**Set block:**
> Inside an older Mumbai city bus, well kept, not dusty: pale blue-grey painted metal walls, worn chrome rails, glass
> windows in metal frames, blue vinyl seats, commuters soft behind. No logo, no lettering.

**Character block:**
> The man from the reference pictures (same face, jet-black bowl cut with a straight fringe, thick moustache, tall and
> thin, {outfit: faded sky-blue checked shirt, sleeves rolled, black office backpack worn on his chest}).

Frames (each = "Create an image, vertical 9:16." + look block + character block + the shot):
| Frame | Use | Shot |
|---|---|---|
| V1 very close | most lines; the Wan 3.0 reference | Very close shot: his face fills most of the frame, eyes in the upper third, his raised arm on a steel rail at the top edge, calm look into the lens, faint half-smile, mouth closed. + set block |
| V9 close | emphasis lines | A chest-up portrait, the camera 1 metre in front of him at eye level. His raised right hand holds the chrome rail at the top left of the frame. His eyes sit at one third from the top, calm look into the lens, faint half-smile, mouth closed. |
| V3 wide | the brakes | Wide shot from the front of the bus looking back down the aisle at eye level: the whole bus full of 1990s commuters, seated on blue vinyl seats and standing holding the chrome rails, office bags and a steel tiffin. He stands in the middle of the aisle, a head taller than everyone, one hand on the rail, looking into the lens. |
| V4 outside | the windscreen pass | The front of an older red Mumbai city bus (classic 1990s single-decker, red body, a cream stripe, flat front, big windscreen in a rubber frame, round headlamps), seen from 3 metres in front of the windscreen and a little above it. Through the windscreen we see the packed aisle and the man standing inside. A Mumbai road: black-and-yellow Premier Padmini taxis, scooters, old stone buildings, trees. No logo, no badge, no lettering, no number plate text. |
| V8 top shot | first and last frame (the loop) | Nadir drone photograph, like a map view: the lens looks exactly perpendicular to the ground, so every vehicle is seen only from its roof and no building walls or sky show at all. Centre: one long red bus roof (cream edges, two small roof hatches) on dark asphalt with white lane lines. Around it: yellow taxi roofs with black bonnets, scooter riders seen from above as small heads, pedestrians as tiny shadows, a tree canopy in one corner, terracotta roof tiles along the edges. No text anywhere. |

"Drone view from 40 metres" kept giving a tilted view with building fronts. The words "nadir ... like a map view ...
no building walls or sky" gave a true top shot.

Checks: `pipeline/gemini/clear_sparkle.sh` on every frame, `face_consistency.py` against the character sheet (pass at
0.55 or more), and `preflight_keyframe.py` for the talking frames.

---

## 3. Voice (ElevenLabs eleven_v4, cloned Pandey voice; 0 credits)

The words never change after the script gate. Only punctuation and tags change (docs/voices/directing-tts.md).

**Direction spec:**
> Affect: a mid-30s office commuter, dry and knowing, speaking to the person standing next to him. Low and close (the
> camera is very near), not projecting. Tone: calm, matter-of-fact, a little confidential. Never a newsreader, never a
> salesman. Pace: unhurried, about 2.4 words a second; quicker inside a list, slower before each name. Arc: direct
> question (hook), dry aside, calm walk through the names, a reset after the brake, a quietly firm payoff.

**Line format:** Devanagari, with the English words in Latin. One tag where the feeling changes, commas instead of
full stops, a dash before the one focus word of each thought group. Pauses are made in the edit, not with ellipses.
The real P1 and P2 of E16 (voice2/lines.json):
> [direct, conversational] Long-term investing करते हैं? ई दो sectors को — ignore मत कीजिए, एक है space, दूसरा semiconductors।
> [dry, matter-of-fact] Space में Agnikul, Skyroot, Pixxel जैसे नाम हैं, लेकिन ई startups — listed नहीं हैं, तो space से जुड़ी listed companies देखते हैं।

Make 3 takes a line. Pick by the names (Scribe's word confidence) and by prosody (`pipeline/prosody.py`). Remove
breaths with `pipeline/debreath.py` ("He's in a bus, not a studio").

---

## 4. Camera moves (Wan 2.7, start frame + end frame, no audio)

**Opening dive** (start V8 top shot, end V1 very close, 5 s, 7.5 credits; it landed exactly on V1):
> One continuous FPV drone shot with no cuts. The camera starts high above a busy Mumbai road, looking straight down at
> the old red city bus. It dives down fast in front of the bus, levels out at the height of the front windscreen, flies
> straight in through the open windscreen into the bus, glides up the aisle between standing commuters, and stops very
> close in front of {the man with the black bowl-cut hair and moustache}, who stands holding the overhead rail and
> looks calmly into the lens with his mouth closed. Smooth, fast, confident drone motion with natural motion blur.
> Late-1990s 35mm film look, soft overcast light, cool grey-blue palette. No text, no logos, no speech.

**Outro** (start V1, end V8, 6 s; its last frame matches frame one):
> One continuous camera move, no cuts. Inside an old Mumbai red city bus, {the man}, holding the overhead rail, is
> silent with his mouth closed. At the very start the bus brakes hard: he and the passengers behind him lurch forward
> toward the camera and he grips the rail. Then the camera pulls back quickly and smoothly, away from his face,
> backwards down the aisle past the standing passengers, out through the front windscreen of the bus into the street,
> and keeps rising like a drone into the sky while tilting down, until it looks straight down from high above on the
> red bus in the busy street, exactly as in the end image. Cinematic 35 mm film look of a 1990s Hindi film, natural
> colour, soft daylight, no text.

Then, locally:
- `roof_text.py` paints a word on the roof (LONG-TERM, yellow Anton) and tracks it through the move.
- `grade_match.py` / `grade_apply.py` give every model's clip one grade.
- In the edit, the windscreen pass is a radial mask opening over the next shot while the dive scales up and blurs.
  A plain cut here felt "broken".

Seedance 2.5 made the same dive at 480p (15 credits), softer and wider. Wan 2.7 with start and end frames is the
choice for camera moves.

---

## 5. Talking shots (Wan 3.0: the face frame as image reference + our voice track; 1.75 credits a second)

Build with `shot_spec.py build --model wan3_0` (track lead 0.5 s, start the shot 0.38 s in). The prompt template:

> The person begins completely still and silent with the mouth closed, and starts speaking only when the voice
> begins. The man from the reference image, {a calm office commuter standing in a moving old Mumbai city bus and
> holding the overhead rail}, speaks in Hindi straight to the camera, as if to the person next to him: dry and
> matter-of-fact, alert eyes, a faint knowing half-smile under his moustache, never theatrical. No hair touching. He is
> framed exactly as in the reference image: the same place, outfit, hair, light and camera position, his face at the
> same size and place in the frame. He speaks in a relaxed, conversational way, in exact sync with the provided audio
> from the very first word: he articulates every syllable clearly, his lips and jaw moving visibly with each word the
> way a real person's do when talking at a normal pace, never exaggerated, and his mouth rests closed between phrases.
> His movements are motivated, never random: between the moments named below, his head stays still and his eyes stay
> on the lens, relaxed. He blinks normally, about once every two seconds. Each expression comes from what he is saying
> at that moment and settles back afterwards. {One or two beats: "A small, firm nod on 'setup', then a faint knowing
> half-smile, no teeth."} Natural movements only. The camera holds still on its tripod. Keep the exact look of the
> reference image: a cinematic full-frame camera video with shallow depth of field, the same soft window light,
> natural colour and real skin texture; no new text, no subtitles.

Do NOT write "his lips part only a little ... the jaw moves little". On Wan 3.0 that gave still lips. The
"articulates every syllable clearly ... never exaggerated" sentence gave measurable lips.

**Approach shot** (the first talking shot, continuing the dive; replace the framing sentence):
> Camera: the shot begins at the front of the bus looking down the aisle, with him standing far down the aisle, small
> in the frame (a full-length view, seated commuters on both sides); the camera glides slowly, smoothly and steadily
> forward up the aisle toward him for the first three and a half seconds, with no shake, ending in a very close shot
> where his face fills the frame exactly as in the reference image; then it holds still. His face stays sharp and
> natural the whole way in.

**The brake** (a 4 s talking shot; the first version had people stand up, and this inertia wording fixed it):
> {Very close on his face exactly as in the reference image, silent with his mouth closed.} At about half a second the
> bus brakes hard. Inertia throws everyone in the bus forward: the camera, which rides in the bus, is jolted backward
> away from him into a medium shot, and in that medium shot every seated passenger behind him is pitched sharply
> forward toward the camera at the same instant, heads and shoulders swinging forward, some bracing against the seat
> in front, bags sliding; then they all rock back upright in their seats. Nobody stands up. Only he does not move at
> all: he stays perfectly steady holding the rail, unbothered. After the jolt the camera glides smoothly back in to the
> very close shot of his face, and as it arrives he speaks {the talking sentence from the template}.

Judge each clip: `shot_spec.py judge`. Pandey's moustache hides his upper lip, so SyncNet is unreliable on him.
Also use `bilabial_check.py` (p/b/m closures), `gap_plot.py` (lip gap against loudness) and your own eyes on a large
mouth crop. On E16, Wan 3.0's lips led the voice by 0.1-0.16 s. At the start of the approach shot they trailed it by
about 0.3 s.

---

## 6. Footage and pictures (0 credits)

Brief for the search (a sub-agent can do it):
> For each company, find real footage on its own YouTube channel or a broadcaster's (NDTV, DD India, PIB): the plant,
> the product, the people at work. Download with yt-dlp. Cut 2-3 s vertical clips at the moments that show the thing
> said in the script. Crop out channel logos, tickers and burned captions (`cropdetect`; check every clip across its
> whole span, not one frame). Write every source in footage_sources.md for the credits line.

**Never use footage or photos of the PM, ministers or party leaders.** E16 used four DD India clips of PM Modi at the Micron plant and Instagram made the reel unavailable in India within hours (an AI-labelled post showing the PM; see gotchas). Skip the dignitaries at openings; take the product, plant and people-at-work shots.

Official logos come from the companies' own sites. An image model never draws a real logo.

---

## 7. Charts (TradingView in the built-in browser; produce-video gotchas)

> Weekly candles from {about 18 months ago} to now, the full width on a white page like silver01. Mark only what the
> script names: resistance at the clearest swing high, support at the clearest swing lows, a range box for a
> consolidation, an arrow for a run-up. No prices, no targets. The camera starts on the whole chart and zooms to the
> recent bars while the marks draw on their words.

Capture: `takeClientScreenshot`, then the Gemini bridge, then `tv/calib.py`, which gives the price-to-pixel map. Use
`timeScale().zoomToBarsRange(i0, i1)`, because setVisibleRange is not implemented. In the hidden pane, load the page
fresh or wait 8 s after setSymbol.

---

## 8. The edit (Remotion; rm/src/Reel.tsx and fx.tsx)

Cut grammar that Akhilesh approved on E16:
- Cut on words. Measure on the clip itself, not on the track.
- Punch-ins are instant 1.18-1.2x with a 3-frame settle, on stressed words.
- Whips have directional blur and a cut at peak speed, only between sections.
- Montages cut on every key word, with an impact zoom 1.12 to 1 over 0.16 s, a 2-frame flash and an alternating
  tilt. "NO. 1" and "NO. 2" slam with a shake.
- Logo cards slam on their names. Several names in a row stack one below the other over the footage.
- Kinetic words go behind his head (bgswap.py --text), 130-140 px, clear of hand and head. Use only words that carry
  the point.
- The brake: the camera is jolted back and returns, and the shake is in the picture.
- The charts get a zoom-through in and a hard cut out.
- The disclaimer is big kinetic type in two groups of lines fitted to the width, flying out.
- The last frame equals the first.

---

## 9. Sound (mix.py)

- The voice sits at 0.12 s.
- Use a recorded bus interior bed, 5 dB lower in the scenes away from the bus, and the street outside for the dive
  and the outro.
- A real bus brake: an air hiss and a groan, no tyre squeal.
- A glass whoosh at the windscreen. Whooshes only on the four big whips, thuds on the key words, pops on logos,
  marker sounds on chart marks. No sound on the montage cuts.
- Two-pass loudnorm to -14 LUFS.
- For a song that Akhilesh adds in Edits, write a cue sheet (cue_sheet.py): song in-points, full or low, mutes at the
  brakes, the end joining the start for the loop. Send a song preview for review only (mix_song.py).

---

## 10. QC and delivery

- Run `finish.py`, then the QC gate (`qc_gate.py`). Waivers are recorded only on Akhilesh's own words.
- Send the phone copy (crf 28, under 30 MB) through the Claude app for review.
- The post file is the stamped 1080x1920 final. On his Mac it goes to Google Drive, `Doordhan finals/`.

---

## 11. Cover (docs/covers.md; Gemini scene + pipeline/cover.py)

Akhilesh chose this scene (B):
> A NEW picture, vertical 9:16, photoreal cinematic. A giant computer chip, as big as a launch pad, lies on the ground
> at dusk, its gold pins and glowing blue circuit traces lit up. From its centre a white rocket lifts off on a bright
> orange flame and a column of smoke. The same man from the reference (same face, bowl haircut, moustache, sky-blue
> checked shirt) stands in the foreground, waist up, facing the camera with a calm, knowing half-smile, lit orange by
> the flame on one side and blue by the chip on the other. His face large in the lower middle third. Top fifth plain
> dark sky. No text, letters or logos.

To join two ideas, attach the best scene and ask for one change:
> Edit the attached picture. Keep everything exactly the same: the same man, his face, pose and expression, the same
> {bus}, camera, light and colours. Change only one thing: {the launch pad far below is now a giant computer chip ...}.
> Vertical 9:16. No text, letters or logos.

Type (cover.json): kicker "SPACE & CHIPS", hook "AGLA BOOM?" in the lime box, tilt -3, scene_zoom 1.06,
scene_shift 60 (this pushes Gemini's mark out of the frame).
