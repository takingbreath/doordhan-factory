# How to define a show template

A template is everything needed to make a new episode of a show with only a script and a few new keyframes.
Copy this outline into formats/<show>.md. Build it the cheap way: characters, 2–3 set keyframes, voices, then one test clip through the whole pipeline.

1. **Premise:** what the show is, in one line, and why it's funny or useful.
2. **When to use it:** which kinds of story fit.
3. **Characters:** name, role, look, Seedream sheet ID, voice (registry key).
3a. **Shot grammar** (house rules since 2026-09-29):
   - one wide, mediums and one close per episode;
   - no more than 55% of the runtime a face talking to camera; the rest cutaways, reactions and inserts without dialogue;
   - talking shots straight to camera or eyes down, with one blink and one small eye shift and no object handling;
   - no looks at off-frame objects: a cut, or the object in frame with an end image;
   - consecutive shots of one framing chain from the previous clip's last clean frame (`shot_spec.py`).
4. **Sets and keyframes:** IDs and what each shows.
5. **Look and graphics:** the on-screen elements, and which ones you build locally.
6. **Sound:** stings, room tone, voice treatments.
7. **Shot pattern:** the default sequence (free to vary per episode).
8. **Recurring devices:** running gags, sign-offs, in-world brands.
9. **Notes from production:** what worked, what broke.
10. **Typical cost:** credits per episode.

## Character-sheet recipe (Seedream 5.0 Pro, 2k, 1:1; this beat Nano Banana)
"Photorealistic character reference sheet of an ORIGINAL fictional Indian [man/woman], age N, [role] in the early 1990s."
Then sections: FACE, HAIR, BODY, WARDROBE (early 1990s), ATTITUDE,
LAYOUT (plain light-grey studio background; top row: full-body front, full-body three-quarter, side-profile head and shoulders;
bottom row: three head close-ups with three named expressions; same person and clothes in every view),
STYLE (photorealistic, soft even studio light, natural skin texture, sharp focus),
AVOID (text, logos, and any resemblance to a real person, plus anything off-look).
Observations: light clothes read better against a dark mic; small checks and patterns shimmer at low resolution; on-air men of that era wore shirts and trousers.
