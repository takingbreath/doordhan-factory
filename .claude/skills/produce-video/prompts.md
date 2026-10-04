# Prompts that worked (E7, Sahayata Kendra, 2026-10-04)

Every one of these produced a usable frame or clip first time unless noted. Swap the outfit, the set dressing and the
props for the new episode; keep the structure. IDs in brackets are the E7 references (registry `kendra_e7_*`); use
the current episode's IDs instead.

## Keyframes (gpt_image_2_5, aspect 9:16, medias role `image_references`)

**The new-look front frame** (refs: previous front keyframe, Pandey's sheet `0e19cfb4…`, style ref `2557c287…`):
> Vertical frame from a 1990s Indian government TV programme, shot on analog video. The same man as in the reference
> images (Vidyasagar Pandey: tall and very thin, long neck, jet-black bowl cut with a dead-straight fringe fully
> visible, thick black moustache) sits at his desk in the Doordhan Sahayata Kendra helpline office. Chest-up medium
> close-up, camera straight on at eye level, head level, eyes looking straight into the lens. Heavy-lidded tired eyes,
> the upper lids covering the top of the iris, a bored knowing look, mouth closed, a faint dry smirk under the moustache.
>
> NEW OUTFIT this episode: <the outfit, item by item>. No sweater vest, no safari suit, no lanyard, no ID card, no headset.
>
> BACKGROUND: the same peeling pale-green office wall, with the blue enamel board reading DOORDHAN SAHAYATA KENDRA high
> on the wall above him. <the topic's set dressing, e.g. a big faded old real-estate poster ... bold text SAPNON KA
> GHAR and under it POSSESSION 2011. A long jagged crack runs down the wall and straight through the poster, and a
> brown damp stain spreads down from the ceiling corner.> A tubelight, the edge of a grey steel almirah. Flat tubelight
> lighting, slightly washed colours, natural skin texture, a real photograph, not glossy. No other text.

**Remove a stray prop** (ref: the frame):
> Exactly the same image as the reference, identical in every detail (same man, same face, same expression, same
> <outfit>, same wall, board, poster, crack, lighting and framing), with one change only: <the stack of papers at the
> bottom-left corner of the desk is gone, so the desk edge there is plain empty wood>. No other change.

**Cold open, Billu walking in** (refs: new front, Billu's sheet `077c7b16…`, previous cold open). The face came out at
13% of the frame height; a local 86% crop brought it to 15–16%:
> ... Medium-wide straight-on shot across the desk: the man (...) sits at the centre behind the desk, head level,
> looking straight into the lens, wearing exactly the same <outfit> as in the first reference. A cream rotary dial
> telephone sits at the screen-right end of the desk. A real ginger desi street cat (the cat from the second reference:
> ginger tabby, a bit heavy in the belly, coarse dusty coat, notch in the left ear, scarred nose, bored half-closed
> eyes) is WALKING along the front of the desktop from the screen-left edge, mid-stride, one front paw lifted, body
> side-on to the camera, head facing the direction it walks, big in the lower-left of the frame, partly entering from
> the left edge. Nothing else on the desk. Behind: <the wall>. ...

Its end frame: the same, with the cat "now STANDS on all four paws on the left part of the desktop, a little further in
from the left edge".

**Listening close-up** (refs: new front, previous listening keyframe): "Close-up of the same man ... holding a cream
rotary telephone receiver to his ear, listening, the curly cord hanging down ... Heavy-lidded bored eyes looking
slightly down, mouth closed ... exactly the same <outfit> ... Behind him, out of focus: <the wall and dressing>."

**Three-quarter angles and the low angle** (refs: new front, the previous episode's matching angle): "... a
three-quarter view from the camera's right like the second reference image: his body turned slightly to screen-left,
head turned back so his eyes look straight into the lens, head level, chest-up ..." The low angle: "a low angle from
just above the desk edge ... Above him: the ceiling fan, a tubelight, and a big brown damp stain with cracked, flaking
plaster on the ceiling and the top of the pale-green wall."

**Billu close-up** (refs: Billu's sheet, previous Billu close-up, new front): "Close-up at desk level of the real ginger
desi street cat ... sitting upright on a worn wooden office desk, facing the camera ... Behind it, out of focus: the
man's <shirt> and the peeling pale-green wall. A real candid photograph, natural cat, not a studio shot, not plush."

**An insert** (ref: style ref): "Top-down close shot of a worn dark wooden office desk: a thin buff-coloured government
manila file folder lies open and completely EMPTY, its front cover printed with the big black stencil word REGISTRY.
On top of the empty open folder lies a single brass flat key on a ring with a cheap plastic keychain tag shaped like a
little house." Short stencil words render cleanly.

**An end image from a start image** (ref: the start frame; this keeps the framing):
> The same image as the reference, same camera framing, same desk, same man in the background in the same place, same
> lighting, with these changes only: <the folder now lies OPEN ... the cat now lies stretched out on top of the empty
> open folder, relaxed, eyes closed>. Nothing else changes.

For the ring: "Exactly the same image as the reference ... with these changes only: the ginger cat has turned its whole
head to the right and looks at the cream telephone at the right end of the desk (its body stays where it is); the
man's eyes now look down at the telephone, his head tipped down only slightly ... mouth closed." (It came out slightly
pushed in, which played as a push-in on the ring.)

**Overhead hang-up** (refs: new front for the sleeve, the E5 overhead `25ffdb7f…`): "Straight top-down overhead shot of
a cream rotary dial telephone on a worn dark wooden office desk ... A man's hand and wrist come in from the top of the
frame, in a <sleeve> with a buttoned cuff and a steel wristwatch, holding the cream receiver just above the cradle,
about to put it down." Make a new one when the sleeve changes; E5's shows a bare forearm.

## Talking shots (Wan 2.7, built by `shot_spec.py build`)
The builder writes the base prompt (still start, the clerk, articulation, "Eyes straight to the camera, or down;
exactly one blink and one small eye shift ... No objects are handled", locked-off camera, keep the look). You give
`--acting`, one note per beat. E7's notes, all passed first take:
- "A tiny dismissive shake of the head on 'Pool chhodo'; then flat and matter-of-fact to the end."
- "Three short flat questions, one after another, like ticking off a list: a tiny lift of the eyebrows on each question, nothing more."
- "Dry and a little slower on 'likhwa ke lo', with one small nod."
- "Quietly, as if letting the caller in on the real story; eyes steady on the lens; flat."
- "Matter-of-fact, like reading out an address; one small nod on 'UP RERA'."
- "Very flat, slower on 'waisa hi dikhega'; the faint dry smirk only at the very end; no smile, no teeth."

**A talking shot where Billu moves** (cold open, start + end image + audio): append to the acting note "Meanwhile the
ginger street cat walks slowly and naturally along the front of the desk from the left, unhurried, with realistic cat
movement, and comes to a stop standing on the left part of the desk. The man does not look at the cat." and replace
"Small, subtle, natural movements only." with "The man's movements are small, subtle and natural; the cat moves
naturally."

## Silent shots (Wan 2.7, no audio; end with "Locked-off camera. Keep the exact analog look of the start image; no new text, no subtitles.")
- **Ring** (start: the cold open's last frame; end: the ring edit): "The ginger cat stops still and turns its whole head
  to the right to look at the cream telephone; at the same moment the man lowers his eyes to look down at the
  telephone, bored, mouth closed. The camera pushes in slowly. Natural, realistic cat movement, small and precise. No one speaks."
- **Listening, 7 s**: "The man from the start image holds the cream telephone receiver to his ear and listens, bored and
  heavy-lidded, mouth closed: one slow blink, a tiny tired nod, his eyes drift down once and come back. He does not
  speak; his mouth stays closed the whole time. Small, subtle, natural movements only."
- **Billu yawns, 3 s**: "... does one huge, slow, bored yawn, mouth wide open showing its teeth and pink tongue, then
  closes its mouth and goes back to a bored half-closed stare at the lens. Natural, realistic cat movement. The man behind stays still."
- **Billu's ears, 2 s** (subtle; fine for a 1.7 s beat): "... suddenly its ears prick up and swivel forward and its
  half-closed eyes open wider, alert, staring straight at the lens, as if it just heard something interesting. Small,
  precise, natural cat movement; its body stays still."
- **Billu's prop button, 5 s** (start + end image): "... it hooks one front paw under the cover of the closed buff folder
  and flips the cover open; it looks down at the empty folder for a moment, then steps onto it, lies down on the open
  empty folder and closes its eyes, settling to sleep. The man in the background stays still and expressionless and
  does not move." The printed word smears while the cover is in the air; play that part at x2.2.
- **Hang-up, 2 s**: "Top-down overhead shot: the man's hand puts the cream telephone receiver down into its cradle
  firmly and lets go, then the hand withdraws out of the top of the frame." The receiver seats at 0.24 s.
