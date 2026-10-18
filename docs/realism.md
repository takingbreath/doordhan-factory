# What makes a generated reel read as real

Started 2026-10-09 from the AI-realism PDF Akhilesh shared, and from E10 (nana01, the creator format). E10 was our best reel by every count (docs/learnings.md); viewers didn't call it out as AI. Use this for any format. The old-TV formats get their own realism from the finish (docs/lab/2026-09-29-reads-as-ai.md), but everything up to the finish applies to them too.

## 1. The keyframe prompt (the PDF's checklist, as it worked on Seedream 4.5)
Every frame names:
- **The light source and its direction:** "low golden-hour sun through a window on camera left, a warm rim on her hair, soft bounce from cream walls, a warm lamp behind".
- **The camera block:** height, distance, lens, aperture ("slightly above eye level, about 50 cm, 24 mm front camera, f/2.2").
- **Depth layers:** what is behind, in soft focus ("sheer curtain, a monstera, a framed print, a small bookshelf, a mug").
- **Imperfection:** "real skin texture with pores, faint under-eye shadows, a slight asymmetry in her smile, natural makeup, slight noise in the shadows, not retouched, not glossy, not a studio portrait".
- **A mid-moment:** "about to start talking", "one loose strand of hair across her cheek".
- **Identity lock:** the person's identity image plus the episode's master keyframe as references, and "the same woman, identical face, hair, jewellery".

Exact prompts: .claude/skills/produce-video/prompts.md, "Creator format".

## 2. Where she is and who is filming
- **A lived-in home beats any studio** (Akhilesh, twice: "not a reading room"). A sofa, a kitchen counter with steel dabbas and a chai mug, a window seat at sunset.
- **The phone is the camera, so it is never in frame.** Say so in every prompt. Seedream still drew a phone on a shelf showing her selfie once; fix that with a one-change edit.
- **A creator's angles:** a selfie at arm's length (shoulder raised to the frame edge), a phone propped on the counter at chest height, an extreme close-up leaning in.
- **A tilted phone reads as real.** Seedream tilts heads 17–23°, past the lip-sync limit, so level the head by rotating the whole frame (`pipeline/level_keyframe.py`). The background then tilts the way a handheld phone does.

## 3. Motion
- **Let Wan act; keep the camera still in the prompt.** Expressive talking (natural nods, brows, blinks) lip-synced fine in close-ups. Camera movement inside Wan costs articulation (2026-09-29 lab).
- **Add the handheld feel in the edit:** a slow multi-sine drift and a tiny roll at 1.07 zoom (nana01_build.py `handheld()`). A 1.2× punch-in reads as a creator's jump cut.
- **Silent B-roll of the person** (sipping chai, raising her eyebrows over the rim) makes her a person, not a talking head. Put it in a real pause in the voice: she can't talk while she drinks (Akhilesh caught it).
- **Wan over-acts physical notes.** "His head lowers, shoulders sink" became the man rising and leaning toward the TV. That worked there, but expect it.

## 4. The grade
- **Clean and modern:** a touch of contrast and warmth, and light grain (alls=1 on faces, 3 elsewhere). Akhilesh asked for little grain, and heavy grain also cost the face check about 0.05.
- **Modern means 30 fps,** 1080x1920 delivery.

## 5. Proof from the real world
- **Real footage carries the facts:** the Naam cheques, the dry land, the reservoirs. AI carries only the person telling the story and what no camera filmed.
- **A real person in a reconstruction appears from behind or in silhouette,** tagged "RECREATION · 2015" (hard rule 4).
- **Period detail sells the year:** 2015 was a 32" LCD on a wooden cabinet with a Tata-Sky-style set-top box, a steel tea glass, a Nokia, a folded Marathi paper, a ceiling fan.
- **Text inside a scene is built locally and keyed in** (the TV bulletin), never drawn by the model.
- **Image models draw real products:** an "unbranded luxury SUV" came out as a Range Rover, and showing one implies a fact we don't have. Ask for an abstract detail instead (the curve of a bonnet, a headlight).

## 6. The voice (docs/voices/directing-tts.md)
Flat TTS gives itself away by the same tune on every sentence, the same fall at every full stop, and even pauses. Fix it by directing the text (commas, one pause at the turn, 4 tags where the feeling changes) on eleven_v4, and by measuring with `pipeline/prosody.py` against real speech.

## 7. Sound
- Room tone under everything (road_distant, low).
- The period room's own sound (a ceiling fan under the 2015 scene).
- The film clip's real sound at both ends.
- No music under her voice.
