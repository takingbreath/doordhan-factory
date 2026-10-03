# Format: Doordhan Sahayata Kendra (the helpline)

_Created 2026-09-27 from Akhilesh's brief; rewritten after the debut, E5 "Top 1% net worth kitna?" (approved v4, 67 s). Read all of this before any Kendra episode. Section 1 holds Akhilesh's rulings: follow them unless he changes them. Everything after it is what worked, and you're free to improve it (then update this file)._

## 0. Contract (research and the lint read this)
Set by Akhilesh, 2026-10-01. The script loop (docs/script-playbook.md) and the lint (pipeline/script_lint.py) read their limits from here.

- **Length:** 40–60 s; 70 s at most. At Pandey's measured pace that is about 90–130 spoken words, and never more than 155.
- **Fixed parts, not in the script:** the ring, about 1 s; the closing card, 4.8 s.
- **Opening, two variants (try both):**
  - **Question headline:** Pandey's first line states the reel's question, flat, in 8 words at most.
  - **Verdict:** Pandey's first line is his flat verdict, in 8 words at most.
  - Then one ring, then the caller's question, asked the way a viewer would ask it, and never repeating Pandey's line. No invented situation (a fee, a trip, a business) unless the topic is the caller's own money (Akhilesh, 2026-10-03: a curiosity question gets a curious caller). The caller is heard by about 4 s (Akhilesh, 2026-10-01: 8 words take about 3 s at Pandey's pace, then the ring).
  - Pandey's line is on screen, big, from the first frame. The caller's question text builds after it.
- **Cast:** Pandey, the caller, and Billu in every episode. Billu is silent: one beat at most, usually the button.
- **Hook types:** the two openings above, matched to types in `docs/hooks.md`.
- **Numbers:** aim for 4 or fewer in the reel, and never 3 in one line. A number the viewer brings from their own life (their salary, their spending) doesn't count. The lint reports the count. The cold readers' retells show whether a listener kept up. A return in a worked example is said out loud as an assumption ("12% maan ke").
- **How numbers are said** (Akhilesh, 2026-10-03, replacing the 1-to-20 rule of 2026-10-01): Hindi words throughout ("chauntees hazaar", "teen crore", "baarah percent"). The English-above-twenty rule sounded broken in the voice ("thirty four hazaar") and Scribe misheard it; the on-screen text shows the digits.
- **Button:** Billu's beat or Pandey's reaction. The last spoken line may echo the opening line.
- **This week's bets:** B1 (hook in frame one) and B3 (a line worth sending) apply. B2 (tight 20–30 s) does not apply to this format.

### Lint table
`pipeline/script_lint.py` reads this table (Claude, 2026-10-01). Since loop v0.3 (3 Oct 2026) every row only reports: the judge and Akhilesh read the report, and nothing sends a script back. The fail/report column is kept for the lint's own verdict line.

| Check | Limit | On breach | What it checks |
|---|---|---|---|
| cast | PANDEY; CALLER; BILLU | fail | Every line's speaker is one of these. |
| silent | BILLU | report | These never speak. Each of their lines is one action in square brackets. (Was fail with a 5-word cap; the cap went with loop v0.3, where the lint only reports.) |
| silent_beats_max | 1 | fail | Silent beats in the reel, at most. |
| opening_order | PANDEY; CALLER | fail | The first spoken lines, in this order. |
| versions_match | PANDEY's 2nd line | fail | Every version is word for word the same from this line to the end. |
| banned_phrases | comment karo; share karo; tag karo; like karo; subscribe karo; follow karo | fail | No spoken line contains these. |
| length_max_s | 70 | report | Estimated length, at most. Make it fail once Pandey's rendered pace is measured. |
| length_aim_s | 40–60 | report | Estimated length, the aim. |
| opening_words | 8 | report | Words in the first spoken line, at most. |
| second_speaker_by_s | 4 | report | When the caller starts, at most: Pandey's first line, then the ring. |
| numbers_reel | 4 | report | Numbers in the reel, at most. |
| numbers_line | 2 | report | Numbers in one line, at most. |
| return_assumption | maan ke; maan lo; maante hain; assume | report | Every percentage has one of these in its line or the line before. |
| silent_beats_min | 1 | report | Silent beats in the reel, at least. |
| pace_wps | 2.5 | — | Words per second for any speaker whose voice card has no rendered pace. Measured from Pandey's rendered cuts, 3 Oct 2026 (the bible's 2.9 was a guess): 60 s of reel is about 130 spoken words, 70 s about 155. |
| ring_s | 1 | — | The ring. |
| card_s | 4.8 | — | The closing card. |
| beat_s | 1 | — | Each silent beat. |

## 1. Akhilesh's rulings (2026-09-27)
**Script and length**
- **Length: 40–60 s, 70 s at most** (Akhilesh, 2026-10-01). Use the time the story needs; don't over-optimise for seconds. E5 ran 67 s.
- **He may write the script.** When he does, voice it as written. Flag a fact or compliance problem once, then it's his call. E5 kept "₹1 crore ka ghar" and "comment karo / like karo".
- **Pace:** Pandey speaks a little fast by default, and slows only for emphasis.
- **End to end** (Akhilesh, 2026-10-01, replacing "research first, script second"): the loop researches, plans and writes from the topic alone, and he judges the finished script.
- **Billu is in every episode's cast** (Akhilesh, 2026-10-01), so the script can use him.

**Look and set**
- **The look is `kendra`:** clearer and brighter than Samachar's `broadcast`. The broadcast grain was "too huge" and the colour "very dull".
- **Board:** the wall board reads DOORDHAN SAHAYATA KENDRA (not "Grahak hi Bhagwan hai").
- **Desk:** only two things on it, Billu and the phone.
- **Billu:** must contrast with the set (grey vanished into the green room). He is a real cat, not a plush AI cat.

**Eyeline, performance and shot mix (Akhilesh, 2026-09-29)**
- **No look at anything off-frame.** A look at Billu, the phone or anything else is either:
  - a cut: he looks off-camera, then a cutaway of the object; or
  - a look within one shot: the object is in the same frame, and the shot has an end image with his eyes (or hand) on it (`shot_spec.py build --look-at ... --target-in-frame`).

  The builder refuses an off-frame look.
- **Talking shots are straight to camera or eyes down.** No object handling while he talks: reaches, papers and the receiver go in a no-dialogue insert (`shot_spec.py build --silent SECONDS --reach-for ...`).

  Every talking-shot prompt carries exactly one blink and one small eye shift, nothing more (the builder adds it).

  Why: in the 2026-09-29 reshoots, business during a line cut the lips' movement to a ninth of normal. Even a held look at Billu cut it by more than half. SyncNet found no confident window in either, so neither passes the gate.
- **Continuity between shots.** A shot that follows one of the same character, set and framing starts from the previous clip's last clean frame (`--chain-from`), checked by face_consistency, with a reset to the keyframe if it drifts.

  A shot that changes his position gets both a start and an end image.
- **Shot mix.**
  - **Sizes:** vary them, with one wide (the room with Billu and the phone), mediums, and one close.
  - **Talking share:** no more than **55%** of the runtime is a face talking to camera. E5 was 70% (76% before the card).
  - **The rest:** cutaways, reactions and inserts generated without dialogue (Wan, no audio, 1.5 credits a second).

- **Floor plan:** fixed across every angle (section 4); positions must never jump between shots.
- **Pandey's clothes:** no headset. Change the clothes from his reference.

**Performance**
- **Deadpan, not lifeless.** Tired, heavy-lidded and dry, with small reactions. Never the wide-eyed frozen stare of E5 v1.
- **Comment and like:** on "comment" or "like" he points down, because that's where the comment and like buttons are.
- **Billu's lines:** when Pandey talks about Billu, Billu is in the frame, then the camera zooms in on him.

**Camera and edit**
- **Moving camera:** pans, multiple angles, POVs, punch-ins and pull-outs. "The edit has to be a banger."
- **Cold open:** Pandey's opening line comes first, with Billu big in frame (section 0). Then one ring: both of them look at the phone, and Billu turns his whole head, not a side-eye. The caller is heard by about 4 s (Akhilesh, 2026-10-01): Pandey's line, then the ring, and nothing else may hold back the hook.
- **One ring** (Akhilesh, 2026-10-01; before that, two rings).
- **Hang-up after the call:** Pandey puts the phone down after the caller, and before he speaks.
- **Question text:** the text clears first, then he hangs up on a clean frame.
- **Cuts:** never cut while he looks about to speak; cut right after the last word.

**On-screen text**
- **Language:** Roman Hinglish, never Devanagari.
- **The caller's question:** in English, big, bold and funky. It builds while the caller asks and clears before the hang-up.

**Sound**
- **Caller:** must sound like they're on a phone (the landline treatment in section 6).
- **Disconnect tone:** it lives in the closing card, not after the call.

**Closing card:** built once and reused: "AAPKI CALL HAMARE LIYE MAHATVAPURN **THI**." (not HAI), with "(Your call was important to us.)" underneath.

**Caption:** E5 went out without "Not investment advice". It's an evergreen wealth fact, not a product, and that was Akhilesh's call. Hard rule 3 in CLAUDE.md still applies by default, so ask him at the final gate every time.

## 2. Premise and when to use it
A 1980s–90s government-style helpline. Vidyasagar Pandey, the last desk at the end of every transfer chain, answers one money question per call: a few plain steps the caller can follow, then one flat verdict. He is kind to callers and brutal to the system.
- **Use it for:** evergreen "everyone wonders, nobody googles" questions, sacred cows ("SIP se ameer ban jaayenge na?"), and debunks of viral reel claims.
- **Not for:** news, which stays with Samachar.

## 3. Characters (IDs in registry/assets.json)
### Vidyasagar Pandey, operator
Original character; no resemblance to any real person.
- **Who:** mid 30s, fifteen years on the phones. His name means "ocean of knowledge"; he believes it, and he is right. Nothing surprises him.
- **Look:**
  - Tall and very thin, with a long neck.
  - Jet-black bowl cut with a dead-straight fringe, fully visible in every shot. Thick black moustache.
  - Wardrobe (E5, sheet `0e19cfb4-46bc-431c-9e8f-5015416124c7`): an off-white half-sleeve shirt buttoned to the collar, a brown cable-knit sweater vest, a pen in the pocket, a blue ID lanyard and a steel watch.
  - **Wardrobe changes every episode** (CLAUDE.md); log it in registry `wardrobe_log`.
- **Expression (the part that matters):**
  - Heavy-lidded, tired eyes, with the upper lids covering the top of the iris.
  - A bored, knowing look and a faint dry smirk under the moustache.
  - Expression reference: `369af5a0-bb84-4918-baf4-56adcf7fd8b8`.
  - Never wide-eyed, never a blank stare.
- **Voice:**
  - ElevenLabs "Pandey" (`RkuMBi6AZByWfSR5Ul5E`, Akhilesh's clone), eleven_v3.
  - Hindi with a light Bihari/Bhojpuri flavour ("ka", "hum", "kahe"), never a caricature.
  - He never shouts, laughs or gets excited.
- **Behaviour:**
  - One clear verdict, reached in a few plain steps the caller can follow, never both sides.
  - Verdicts are about behaviour, products and myths, never a call to buy or sell a specific stock.
  - He isn't a clown, angry or a lecturer. Things are funny around him.

### Billu, the office cat
- **Look:** a real Indian street cat (desi billi): a ginger tabby, a bit heavy in the belly, with a coarse, slightly dusty coat, a notch in the left ear, a scarred nose and bored half-closed eyes.
- **Sheet:** `077c7b16-5911-4a12-838c-1adde9fc0ea9`. It was prompted as candid point-and-shoot film photos, which read far less like AI than a studio sheet. The earlier grey and plush-ginger versions are retired.
- **What he does:** the second deadpan in the room.
  - Slow, unimpressed stares, ear twitches, slow blinks.
  - Turns his head away from Pandey.
  - No warmth between them, no meowing on cue, no tricks.
- **Lip-synced shots:** Billu can share one with Pandey if the prompt keeps him still ("only a slow blink and an ear twitch, it does not move its body"). E5's two-shot held him perfectly. Keep his beats short.
- **Pose continuity:** in E5 he sat upright in the opening and at the end, but lay loaf-style in the "Loan hai?" cutaway. Pick one pose per episode.

### Callers
- **On screen:** never. They're heard through a landline.
- **Casting:** a new ElevenLabs voice each episode. E5 used "Bobby – Energetic natural voiceover" (`YgpoWAqBbWpygO1YiIEI`).
- **Tone:** the caller is every viewer, sincere and never mocked.
- **Their line:** they ring once and are gone, so their one line carries their stake. The moves that fit it are in `docs/hook-menu.md` (no agent in loop v0.3 reads it).

## 4. Set, floor plan and keyframes
- **Room:**
  - Peeling pale-green wall with the blue enamel board "DOORDHAN SAHAYATA KENDRA".
  - Ceiling fan and tubelight, a wall calendar, a grey steel almirah.
- **Floor plan, the same in every angle:**
  - Pandey sits in the centre.
  - Billu sits at the screen-left end of the desk (Pandey's right).
  - The cream rotary phone sits at the screen-right end (Pandey's left hand).
  - Nothing else is on the desk.
- **Keyframes:** make every new angle from the master and check it against the floor plan before using it. Akhilesh caught a cold-open frame that moved the phone to the centre.
- **E5 keyframes** (reuse them, restyling only the wardrobe):

| Use | ID |
|---|---|
| Master (wide, both, phone right) | `455286ed-c486-4b6f-a523-53cdfd419284` |
| Cold open, straight shot: Billu big at left, phone right, both looking at the phone (end frame) | `c3692eee-4512-4e0d-812c-01daeed5a9b1` |
| Same framing, both looking into the lens (start frame) | `e2c77184-4572-4cb5-999f-7fb51be9dba1` |
| Front talking (heavy-lidded) | `369af5a0-bb84-4918-baf4-56adcf7fd8b8` |
| Three-quarter left talking | `93b0322a-84dc-472e-b7b6-d0c3d8b4a250` |
| Low-angle talking (ceiling fan) | `eb2af48d-69d3-4376-8607-da8e1a60e0b1` |
| Three-quarter right talking | `d72e1859-acd0-403b-8486-303600617d40` |
| Two-shot: Billu sitting at lower left, Pandey eyeing him | `2c61e83a-0bf6-42cb-a5ba-b3ec6509b4d7` |
| Listening close-up, receiver at ear | `2aca9c6e-74b9-4bf0-b3ee-f072acf5320f` |
| Overhead of the phone with his hand | `25ffdb7f-42cf-4978-9028-2cc2a1c36f28` |
| Billu close-up (loaf) | `ee6148ed-e42a-4de2-a81e-b1f3dfde6662` |
| Style reference | `2557c287-bf5c-4905-933e-9b75f04c4a79` |

- **Reusable E5 clips** (no dialogue; registry `clips.kendra_reusable_e5`):
  - cold-open head turn;
  - listening close-up;
  - overhead hang-up;
  - Billu turning away, lying and sitting versions.
- **Outfit check:** they all show the E5 outfit, so reuse them only if the new outfit can't be seen, or regenerate from the same prompt with the new wardrobe.

## 5. Look, text and graphics
- **Look:** `look.py` preset `kendra` (finer grain, sharper, brighter colour); in edit.json, `"look": "kendra"`.
- **Finish defaults in assemble.py (2026-09-29):** these are on without asking.
  - **VHS motion** (`vhs_motion.py`: line jitter, colour bleed, streak noise, rare dropouts) at 0.65 strength, applied before the `kendra` look, so the brighter colour stays. After a simulated Instagram re-encode the jitter measures about 0.5 px, and black level and saturation are unchanged.
  - **Pre-finish check:** lip sync is gated on `<final>_prefinish.mkv`, the edit before the finish.
- **Fonts** (assets/fonts, fetched from jsDelivr fontsource; GitHub raw is blocked here):
  - Titan One for slams;
  - Bungee for boards and labels;
  - Baloo 2 Latin ExtraBold for captions.
- **Rupee sign:** only Baloo 2 Devanagari has it. The edit's sprite renderer falls back automatically.
- **Check mark:** no font has one, so it's drawn as a shape.
- **The question:** in English, 4–5 lines that pop in word by word over the caller, with the key number in giant yellow ("TOP 1%?"). It zooms out and clears as the call ends, before the hang-up.
- **Captions:** 2–3 words each, 66 px, near the bottom (y≈1015 of 1280). Wrap to two lines rather than shrinking.
- **Slams:** use them for punch words ("GINO." green, "GHATAO!" red, "NAHI." red, "₹90 LAKH" yellow).
- **Graphics that worked in E5:**
  - a tally board that counts items;
  - numbers flying in bigger each time, then struck out in red;
  - a ✓ checklist;
  - bouncing down-arrows on "comment" and "like";
  - the DOORDHAN bug at top right.
- **Closing card:** `assets/clips/sahayata_endcard.mp4` (4.8 s), built by `pipeline/sahayata_endcard.py`: TV snow, the card, three disconnect beeps and Für Elise hold music. The edit re-renders it raw so the look applies once.

## 6. Sound
- **SFX kit:** `pipeline/sfx.py` writes `assets/audio/sfx_*.wav`:
  - whoosh (whips and pull-backs); pop (each word or item);
  - ding (each number or "gino"); thud (slams); record scratch ("Nahi");
  - riser (before the verdict); stamp;
  - `room`, an office-fan hum under everything.
- **Phone sounds:** two rings (`work/.../ring2.wav` pattern: two bursts per ring), a pick-up click, and the cradle clack synced to a frame jolt.
- **Caller landline chain** (ffmpeg): trim the silences, then
  `highpass=380, lowpass=3000, aresample=8000, acrusher=bits=10:mode=log, aresample=48000, equalizer f=1600 +7 dB, equalizer f=500 −4 dB, acompressor 6:1`,
  plus pink-noise line hiss band-limited to 400–3000 Hz, `loudnorm -17`.
- **No music under the voice.** Hold music only on the closing card.
- **Voice room (default, 2026-09-29):** `voice_room.py`: 120 Hz–7 kHz, light tape saturation, a small office room (RT60 0.35 s, 13 dB under), no hiss.
  - In a frame-composed build like E5 (one mixed part), treat the dialogue bus with `voice_room.treat()` in the build, leave the caller's landline line alone, and set `"room": false` on the mix part.
  - A plain edit.json gets it per part automatically.
- **Ambience (default):** `"ambience": "office"`: recorded CC0 fan and distant road (assets/audio/ambience/SOURCES.md) at −36 dB relative to the programme, 9 dB lower than the realism test.
  - It replaces the old synthetic `sfx_room` fan: a new build should drop `sfx_room` and let assemble lay the bed. A build that keeps its own bed sets `"ambience": null`.

## 7. Episode shape (the Question type, as E5 proved it)

Timings updated 2026-10-01: Pandey's opening line first, then one ring, with the caller heard by about 4 s. E5 opened on the rings and the caller.

| Beat | What happens |
|---|---|
| 0–3 s | Cold open: Pandey says his opening line to camera, Billu big at left. The line is on screen, big, from the first frame. |
| ~3 s | One ring ("TRRRING!" on screen). Billu turns his head, Pandey looks down at the phone. |
| ~4 s | Crash zoom into the listening close-up on the pick-up click. |
| ~4–9 s | The caller asks. The English question builds word by word, pops on each word, thud on the key number. |
| ~9–9.6 s | The question zooms out and clears. |
| ~9.6 s | Overhead hang-up with a clack and a jolt. |
| ~10.3 s | His answer, one line per talking shot. The camera pulls back on his sigh; new framings (crops) on each counted item. |
| mid-answer | A whip pan to Billu for one beat (E5: "Loan hai?"), then a whip back to a slam. |
| verdict | A crash zoom on the eyes for the turn ("Nahi"), then the number slam, a riser and a slow push. |
| comment / like | E5 only: Akhilesh wrote that line. A loop script doesn't ask for comments or likes (script bible), and the lint reports it. |
| Billu line | Two-shot, zooming slowly into Billu, running straight into his blink and turn-away (one continuous angle). |
| end | One ring. He hangs up without answering (overhead clack). |
| last 4.8 s | Closing card. |

**The Reel-debunk type (untested):**
- **Caller line:** "Pandey ji, ek reel dekhi, @creator keh rahe hain ki <claim>. Sahi hai ka?"
- **Claim card:** a plain on-screen card with the handle, the exact quote and the date. No footage, screenshot or face.
- **The takedown:** one verifiable fact, then GALAT (or SATYAAPIT when they were right) as a graphic stamp.
- **The creator:** debunk the claim, never the person; invite them to call the Kendra, and tag them in the caption.

## 8. Production recipe (follow in order)
1. **Voice.**
   - ElevenLabs over the API (Akhilesh, 2026-09-30; it replaces the connector): `python3 pipeline/tts_elevenlabs.py --voice pandey --text-file LINE.txt --out raw.mp3`, eleven_v3, Devanagari text with English words kept in Latin. The caller's voice goes by `--voice-id`. The key lives in the git-ignored `.env`; `tts_elevenlabs.py --check` confirms it and shows the quota.
   - A session with no key (a cloud machine that hasn't been given one) uses the connector's `creative_generate_speech` instead, with the same model and text.
   - Tags: `[flat, brisk]` by default, and `[slowly]` only right before a punch word.
   - Never tag a whole line slow. That, plus `[pause]`, left 1–1.8 s gaps and stretched E5 from 65 s to 82 s.
   - At most 3 generations at once, or you get "Too many concurrent requests".
   - Check every take with a Scribe transcript: `python3 pipeline/transcribe.py raw.mp3 --expect-file LINE.txt` (scribe_v2). It gives the similarity to the script and each word's time, so the last word's end is known for the trim.
   - Without a key, the connector route still works, but its transcript is plain text with no word timings: `creative_create_asset_upload` → `put_upload.py` → `creative_finalize_asset_upload` (flow_id) → `creative_transcribe_audio` (eleven_scribe_v1).
   - Level every line to -16 LUFS.
   - **Trim each line at its last word.** A trailing breath makes Wan hold the mouth half open, which reads as "about to say something".
2. **Draft cut.** Join the ring, click, caller, clack and lines into one voice cut, and send it to Akhilesh before any video.
3. **Tracks.**
   - `make_track.py OUT line.wav --lead 0.5 --hold 0.1`, one per talking line.
   - **The lead is 0.5 s, not 0.12.** Wan barely moves the lips in a clip's first second.
   - make_track now resamples to 48 kHz first. Before 2026-09-27, 44.1 kHz ElevenLabs lines came out 8.8% fast and every mouth drifted ahead of the voice.
   - Upload with `media_upload` → `put_upload.py` (audio/mpeg) → `media_confirm`.
4. **Keyframes.** gpt_image_2_5 at 9:16, referencing the master plus the sheets, with heavy-lidded expression wording. Check the floor plan, the eyes and the text on the board.
5. **Talking shots.** Wan 2.7 at 720p, `start_image` plus `audio_references`, duration = the track length, `declined_preset_id` from the registry.
   - Build the spec with `shot_spec.py build ... --set kendra --framing <setup> [--chain-from <previous spec>]`. It writes the prompt below, plus "Eyes straight to the camera, or down; exactly one blink and one small eye shift during the line, nothing more. No objects are handled."
   - Prompt template: "The man from the start image, a dry, tired government helpline clerk, speaks in Hindi, his jaw and lower lip moving clearly with every syllable in exact sync with the provided audio, from the very first word. Deadpan but alive and human: heavy-lidded bored eyes, a faint dry smirk under his moustache." Then **one acting note per beat, in order**. Then "Small, subtle, natural movements only; no hands, no big grin. Locked-off camera. Keep the exact analog look of the start image; no new text, no subtitles."
   - Gestures: E5's pointing on "comment / like" worked, but since 2026-09-29 hands and objects stay out of talking shots (see the eyeline rules in section 1). Put the gesture in a reaction shot, or keep it to one small point with no object in the hand.
   - Wan sometimes pushes in or leans in by itself; reduce the digital zoom on that line.
6. **Cutaways, reactions and inserts** (at least 45% of the runtime). Wan 2.7 image-to-video with **no audio**, at 1.5 credits a second (half Seedance's price), minimum 2 s.
   - `shot_spec.py build --silent SECONDS --id <id> --keyframe <id> --character <name> --acting "..."`.
   - A reach or a look at something in the frame gets `--reach-for` or `--look-at` with `--target-in-frame`: the spec asks for an end image (hand or eyes on the target). Make it, then run `shot_spec.py endcheck SPEC END.png` before the video.
   - For Billu: "natural, realistic cat movement, small and precise".
   - For a shot that continues a zoom, start from the exact zoomed crop of the previous clip's last frame (uploaded as an image). E5's Billu turn-away ran on seamlessly this way.
   - Seedance at 480p works too (the E5 cold open), but it costs 3 credits a second.
7. **QC on every clip.**
   - `check_match.py` must be 1.00. But it compares the clip to its own track, so it **can't** catch a wrong-speed track.
   - Also look at the mouth frames at a known word against the edit's audio (a 10 fps mouth crop sheet next to the audio level).
   - Look at the face frames for expression.
   - headcheck and lipcheck run near their limits because his head moves now. Judge by eye.
8. **Edit.**
   - Copy `assets/edits/sk01_build.py` to `work/<slug>/build.py` and change:
     - the timeline `S[...]` and each line's last-word time (`P2_END`-style trims);
     - `TALK` (clip files and leads);
     - the face centres (measure each keyframe on a grid; zooms go wrong without this);
     - the texts, graphics and events.
   - Each talking line is one Wan clip. Angle changes inside a line are crops of that clip, so lip sync never breaks at a cut.
   - Cut about 0.25 s after the last word.
   - Then `assemble.py` with edit.json (`"look": "kendra"`, `lufs -16` part, target -14). It takes about 40 s to render.
9. **Deliver.**
   - Re-encode at crf 25 to stay under 30 MB (SendUserFile's limit).
   - Run a Scribe transcript of the final's audio.
   - Upload to Higgsfield (video/mp4).
   - Send the file, the link and the plain-language QC notes; email them in the routines/email-style.md final layout; push a notification.

## 9. Pitfalls we hit (don't repeat them)
- **Sped-up tracks.** The mouths ran ahead of the voice; it's fixed in make_track, with a self-test.
- **Wan's slow first second.** The mouth barely moved on "Ghar hai? Gino."; the fix is the 0.5 s lead.
- **A breath after the last word.** It read as a half-open mouth and a bad cut; trim the line.
- **"Flat, unblinking, no head movement" on wide-eyed keyframes.** It came out lifeless and AI-looking.
- **Text over the action.** Clear it before the action.
- **Grey cat on a green set.** It was invisible.
- **Plush studio cat sheet.** It looked AI.
- **Clutter.** Too many props on the desk.
- **Moving props.** Props that move between angles break the floor plan.
- **The model's zoom plus our zoom.** Stacked, they cut the head off.
- **An old digital zoom centre after new keyframes.** Re-measure the face centres every time.
- **Missing glyphs:** ₹ and ✓ are missing in most fonts.
- **Files over 30 MB.** They don't reach his phone through SendUserFile.

## 10. Cost
- **E5: about 215 credits**, including one-time setup and about 50 wasted on the track bug:
  - sheets and keyframes ≈ 20;
  - cold-open test on Seedance 12;
  - talking shots v1 73.5 (spoilt by the bug);
  - the final six talking shots ≈ 72;
  - cutaways ≈ 30.
  - ElevenLabs: about 3–4k credits per episode on voices plus about 350 per Scribe check.
- **E6: 94.5** (approved budget 100): 8 talking shots 61.5 (41 s of Wan), 5 no-dialogue shots 30 (listening close-up 7 s,
  Billu reaction 5 s, bowl 4 s, ring look 2 s, calendar 2 s), 12 images 3. No retakes; E5's overhead hang-up reused, cropped.
  Keyframes, clips and the build are in the registry (`kendra_e6_*`, `kendra_reusable_e6`) and work/sk02/build.py.
- **Next episode, expected about 100–120:**
  - talking shots ≈ 70 (about 50 s at 1.5);
  - 2–3 new cutaways ≈ 15;
  - new-outfit keyframes ≈ 3.
  - Reuse the E5 non-dialogue clips where the outfit isn't visible.
  - This is above the 60-per-episode default, so give a breakdown and ask before generating.

## 11. Post kit notes
- **Caption:** line 1 is the question with its keywords; lines 2–3 are the answer in Roman Hinglish with the source (E5: World Inequality Lab 2022-23, top 1% ≈ ₹81.6 lakh per adult, "mota-mota ₹90 lakh"). Then "Characters are AI-generated." and 5 hashtags.
- **"Not investment advice":** ask Akhilesh (section 1).
- **Cover:** the frame where the full English question is on screen over the listening close-up (E5: 8.2 s). Backup: the number slam.
- **Poll:** it echoes the question, with a Billu option ("Billu se poochho").
- **Rename audio:** "Doordhan Sahayata Kendra – <topic>".
- **YouTube category:** Entertainment.
- **Slot:** 8–8:30 pm IST, a day apart from the previous reel. If a news reel is due the same day, the news goes in the morning, or the Kendra moves a day.

## 12. Ideas not yet tried
- **Callers:** callers who get his name wrong ("Vidyasagar ji… Pandey ji… Sagar ji?") and a flat correction.
- **Hold gag:** "Ek minute hold kariye" mid-answer, with the hold-music gag.
- **The receiver:** held away from his ear when the caller says something absurd.
- **Billu:** answering the phone in an empty office (a cold-open variant).
- **Length:** a shorter 35–45 s cut for Shorts, if long reels underperform.

- **Talking shots are capped at about 6 s of speech** (2026-09-28 QC): split longer lines at a pause and cut between the parts as an angle change. E5's 11 s neighbour line drifted to -160 ms by its end. `shot_spec.py build` applies the cap, lead-in, still start and headroom; `shot_spec.py judge` decides accept / shift / retry once / ask.
