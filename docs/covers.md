# Reel covers: one idea, one scene, our type

Akhilesh, 2026-11-14: every reel gets a designed cover, so that a visitor to the profile sees at once what the channel
is about. Copy Cleo Abram's process, not her style. Our characters change from format to format, so the constant is
a colour and a type style: her lime. Keep the text short, and let the picture and the text together make the viewer
curious. Keep the font and the style the same on every cover.

Later the same day, on the first two drafts (a collage of footage stills with a face below it): "still very boring",
"slop". He asked for research on creative thumbnails and "high quality".

## What the research showed (2026-11-14, about 60 thumbnails)
- Studied: Cleo Abram (24), Think School (16), Veritasium (12), Johnny Harris (8), and shivanshu.agrawal_'s Instagram
  grid (Akhilesh's screenshot).
- **One idea, as one image.** Think School's "Oracle's Debt Bomb?" is a fuse burning on a roll of cash. Veritasium
  uses one object in dramatic light. Johnny Harris engraves his own face into a $100 note. None of them puts photos
  side by side in panels.
- **The person is inside the story**, in the same light and space as the subject (Shivanshu: Ambani laying the fibre
  cable, an auto-rickshaw driving over the globe). A face pasted beside a subject reads as a template.
- **Cinematic craft:** a foreground and a background, a rim light, warm against cool colour, sharp focus on the face.
- **Short text that adds a question** to the picture ("THEY FOUND IT?", "END OF IT BOOM?"). It does not label what
  the picture already shows.
- One accent colour and one type style on every cover (Cleo's lime box). That is our constant.

## How to make a cover (about 30 minutes, 0 credits)
1. **The idea.** Write 3 ideas in one line each, then pick one. A good idea joins the story's subject with our
   presenter's world in one absurd or dramatic picture that the viewer wants to understand. E16: Pandey's Mumbai bus
   launches like a rocket from a launch pad that is a giant chip (space and semiconductors, in the bus where the reel
   happens).
2. **The scene in Gemini** (pipeline/gemini/README.md, a project copy of the gemini-media skill's scripts; Pro account, 0 credits). Attach the presenter's master keyframe as
   the reference through the bridge (`bridge_get.js`, paste). Prompt: "photoreal cinematic film still, vertical 9:16",
   the man from the reference "exactly" (face, hair, clothes), the scene, the camera ("close, slightly below"), the
   light ("golden hour, strong rim light"), "keep the top fifth plain sky" (room for the hook), "No text, letters or
   logos". Make 2-3 scenes. To join two ideas, attach the best scene and ask for ONE change ("Keep everything exactly
   the same ... change only: the launch pad is a giant computer chip").
3. **Save and clean:** `pipeline/gemini/capture_full_url.js`, then the bridge (no download). Then `pipeline/gemini/clear_sparkle.sh` (use
   `SPARKLE_MARGIN=64` when the check shows the star left in place).
4. **Check the face:** `pipeline/qcpy pipeline/face_consistency.py KEYFRAME scene.png` must PASS (E16: 0.75-0.84,
   above our Wan clips). Look at it at full size too.
5. **The type layer:** write `work/<slug>/cover.json` (example: work/sk06/cover.json), then run
   `python3 pipeline/cover.py work/<slug>/cover.json`. It lays out the page in HTML/CSS and headless Chrome renders it
   at exactly 1080x1920. Output: `outputs/<slug>/E<n>_cover.jpg`, `_grid.jpg` (the 3:4 tile at phone size, 360x480)
   and the `.html` page. Move the hook with `hook_at` and the scene with `scene_zoom` and `scene_shift` until the
   hook, the face and the subject all sit inside the tile.
6. **Look at `_grid.jpg` at 100%.** That is the size a phone shows. Every word must read, and the idea must be clear
   in one second. Make one alternative and recommend one.

## The constants (pipeline/cover.py; the same on every cover)
| Part | Rule |
|---|---|
| Size | 1080x1920 JPG. The profile grid shows the centre 3:4 (y 240..1680). Hook, face and subject sit inside it. |
| Hook | Anton caps in a lime `#C1FE06` box, ink `#0C1E14` text, 7 px ink outline, 16 px hard ink shadow, tilted 3-4 degrees. 1-4 words, stacked on two lines when that makes it bigger. Placed on plain sky or a quiet area. |
| Kicker | Optional: the topic in white Anton with a thick ink outline, above the hook ("SPACE & CHIPS"). Use it when the picture does not say the topic by itself. At most 5 words on the cover in all. |
| Finish | A light vignette and film grain, so the type sits in the picture. |
| Arrow | Optional: one white hand-drawn arrow (`arrow` in the spec) at the thing that makes the viewer curious. |
| Not on a cover | Real politicians (an AI-labelled post showing the PM was blocked in India, E16), text inside the generated scene, the DOORDHAN bug, small text, a drawn logo, a buy or sell call (hard rule 3). |

## Posting
- Instagram: "Edit cover", then "Add from camera roll", then check the profile-grid crop.
- YouTube Shorts: the app takes a custom thumbnail from the gallery.
- The cover is AI-made: the post keeps Instagram's AI label (hard rule 3).
- The B4 split-screen bet measures frame one of the reel, not the cover. Frame one still opens the reel. The cover is
  what the grid, the Reels tab and shares show before playback.

## Log
- E16 (sk06, 2026-11-14): v1 and v2 were collages of footage stills (rocket and chip panels) with Pandey's frame below
  them. Akhilesh: "boring", "slop". v3 gave two Gemini scenes with the same type layer:
  - A: Pandey hangs out of his Mumbai bus as it launches from a giant chip on the coast (busrocket_a3_chip, face 0.76).
  - B: a rocket lifts off from a giant glowing chip at dusk, with Pandey in front, facing the camera
    (chiprocket_b1, face 0.84).
  Akhilesh chose B ("I like the B version"). The cover uses scene_zoom 1.06 and scene_shift 60 to push Gemini's mark
  (on his shoulder edge, where a fill smears) out of the frame. Taste note: he picked the clear metaphor with the face
  large and to camera over the busier action gag. Recommend that kind first.
