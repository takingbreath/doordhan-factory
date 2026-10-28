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

# Creator format (E10, nana01, 2026-10-09)
Rules and why: formats/creator.md and docs/realism.md. Keyframes on seedream_v4_5, 9:16, 1 credit, refs: the identity
image (`e9a78b8d…`) and, after the first, the episode's master keyframe (`20f3c2d0…`).

**Master keyframe, the sofa selfie** (refs: identity image + the look-test still `01610a3c…`; 2 variants, the first won):
> Vertical 9:16 frame grabbed from a real Instagram creator's front-camera video, recorded on a recent smartphone front
> camera held at arm's length. The camera IS the phone: there is no phone, no hand holding a phone and no screen
> anywhere in the frame. The same young Indian woman as in both reference images (shoulder-length wavy dark brown hair,
> warm brown eyes, soft round face, small gold hoop earrings, thin gold chain), wearing the same chunky cream knit open
> cardigan over a black scoop-neck top as in the second reference. She sits curled up on a beige linen sofa in her warm,
> lived-in Mumbai apartment. Close-up from mid-chest up, her face in the upper-middle of the frame and filling about a
> quarter of the frame height; her right shoulder is raised slightly toward the lens, as if her arm is stretched out
> holding the camera just outside the right edge of the frame. Camera slightly above eye level, about 50 cm from her
> face, 24 mm wide front-camera lens with mild wide-angle perspective, f/2.2, background softly out of focus but
> readable. Light: low golden-hour sun through a window on camera left, a warm rim of light on her hair and the left
> side of her face, soft bounce fill from the cream walls; a warm table lamp glows in the background. Depth behind her:
> the window with sheer curtains, a potted monstera, a framed print, a small bookshelf, a ceramic mug on a side table.
> She is about to start talking: mouth closed, a relaxed natural half-smile, eyes looking straight into the lens, head
> level, her hair neatly brushed and combed, no flyaways or stray strands. Real skin texture with pores, faint under-eye shadows, a slight
> asymmetry in her smile, natural makeup only, slight front-camera noise in the shadows, not retouched, not glossy, not
> a studio portrait. No text, no logos.

**Other setups** (refs: master + identity) start "Vertical 9:16 frame from the same Instagram creator's video, a few
minutes later in the same warm apartment and the same golden-hour light. The same woman as in the first reference
image, identical face, hair, gold hoops and chain, the same <outfit>", then the place, how the phone is held, the
framing, the camera block, the light, the background, the expression, the imperfection line. What each said:
- kitchen: "leaning forward on her forearms on the wooden counter, a ceramic mug of chai beside her elbow. The camera is
  the phone, propped up on the counter in front of her at her chest height ... Medium close-up from the waist up, face
  ... about a fifth of the frame height ... 26 mm phone lens, f/1.8 ... warm low sun through the window on camera left
  raking across the counter, a warm pendant lamp ... open shelves with jars and steel dabbas".
- extreme close-up: "leaned in very close to the camera ... face fills about 45 percent of the frame height ... 24 mm at
  35 cm ... a knowing look, as if about to tell a secret, eyebrows very slightly raised". (Its talking shot failed
  twice: eyes half-closed. Prefer the kitchen or sofa framing for short lines.)
- window seat: "later the same evening ... cushioned window seat, knees drawn up ... the phone, propped on the bookshelf
  opposite at her eye level ... The sun has just set: the window glows soft orange and dusky blue, a warm table lamp
  lights her face from the right, a gentle rim of cool window light on her hair". Seedream drew a phone on the shelf.

**Remove a phone Seedream drew** (ref: the frame): "Exactly the same image as the reference, identical in every detail
(same woman, same face and expression, same <outfit>, same pose, same window ..., same lamp, same bookshelf, same
lighting and framing), with one change only: the smartphone standing on top of the bookshelf beside the lamp is gone
completely, so the top of the bookshelf there is plain empty wood with only the lamp on it. No phone or screen anywhere
in the image. No other change."

**A period recreation, a real person from behind** (gpt_image_2_5, 0.25): "Vertical 9:16 candid photograph, Mumbai,
2015, night. Inside a small, simple one-bedroom apartment in Andheri. An older Indian man in his sixties with short grey
hair, wearing a plain white cotton kurta, is seen FROM BEHIND and slightly to the left: only the back of his head, his
shoulders and one arm, sitting on a plain wooden sofa with a worn cushion. His face is not visible at all. He is
watching a 2015 32-inch black flat LCD television that stands on a low dark wooden cabinet against a pale green wall; a
Tata-Sky-style black set-top box with a small red light sits under the TV, a tangle of cables behind it. The TV screen
shows a plain deep blue picture with nothing on it. Light: the cold blue-white glow of the TV is the main light ... a
dim warm bulb from the kitchen doorway on the right. Details of 2015: a steel glass of tea on the cabinet, an old Nokia
feature phone and a folded Marathi newspaper beside it, a wall clock, a calendar with no readable text, a ceiling fan.
Shot on a 2015 point-and-shoot at eye level from just behind the sofa, 28 mm, slight noise in the shadows, real
lived-in room, not staged, not glossy. No readable text anywhere, no logos." The blue screen is keyed locally
(nana01_build.py `tv_composite`).

**A product without a brand** (gpt_image_2_5): an "unbranded luxury SUV" came out as a Range Rover. What worked: "Only an
abstract detail of a new glossy black car fills the frame: the long curve of the polished bonnet and the edge of a sleek
headlight, with crisp white showroom spotlights reflected as long streaks on the black paint. No badge, no grille
emblem, no logo, no lettering, no recognisable car model, shape kept generic. Shallow depth of field, 85 mm, dark
background with soft bokeh lights. Real photograph, natural reflections, not CGI."

**Talking shots (Wan 2.7)**: `shot_spec.py build ... --character rashmi --look modern` (the base and the modern tail are
built in). Acting notes that passed: "Easy and chatty at the start, a small knowing smile on 'Ab Tak Chhappan Two'; her
eyebrows lift a little on 'dedh crore'; on the last words 'lekin phir' her voice drops and she leans very slightly
toward the lens"; "Quiet, slower and thoughtful, speaking from the heart; a gentle sincere smile grows on the final
question and she holds the look into the lens at the end". The kitchen retry that passed added "Eyes open and straight
to the camera" and "Her head stays facing the lens".

**Silent shots (Wan 2.7, no audio)**:
- chai B-roll, 3 s: "The young woman from the start image, leaning on her kitchen counter in the warm golden-hour light,
  picks up the ceramic chai mug beside her elbow with her hand, takes one small slow sip, then lowers the mug a little
  and looks straight into the lens over its rim with a knowing, slightly mischievous smile and raised eyebrows, as if
  saying 'wait, there is more'. ... No one speaks; her mouth stays closed except to sip. The camera holds still. Keep the
  exact look of the start image: a modern phone video ..." Use src 1.1–2.6 s, inside a pause in the voice.
- recreation, 3 s: "The older man seen from behind sits still on the wooden sofa watching the television; slowly,
  heavily, his head lowers a little and his shoulders sink, as if he has just heard something terrible. His face is never
  seen; he does not turn around. The blue television screen stays a flat, steady blue with nothing on it ... Locked-off
  camera on a tripod." (He rose and leaned toward the TV instead; it played well.)


## Creator talking shot that worked (anthropic01 hook, 2026-10-28, Wan 3.0; Akhilesh: "so much better")
Built by `shot_spec.py build --character rashmi --look cinema --model wan3_0 --acting "<note>"`. The note for a calm,
slightly secretive fact: "The line is a plain, slightly secretive fact, not exciting news: her face stays calm and her
brows stay relaxed for the whole line. Only two moments: on 'kabhi' one small shake of her head; on the last word a
faint, dry half-smile with the lips closed." The prompt as sent (the builder writes the same from its parts):
> The same young woman as in the reference image, in the same room, the same outfit, the same warm golden window light
> and the same framing: seated against a cream sofa, framed from mid-chest up, her face in the upper middle of the
> vertical frame, looking into the lens. Her hair stays exactly as in the reference image: neatly brushed and combed,
> no flyaways. She is an Instagram creator talking straight to the camera in Hindi, saying exactly the words of the
> provided audio, explaining something she read to a friend: calm, matter-of-fact and natural, a relaxed face with
> relaxed brows, never theatrical. She begins still and silent with the mouth closed, and starts speaking only when the
> voice begins. She speaks in a relaxed, conversational way, in exact sync with the provided audio: her lips part only
> a little on most syllables, the jaw moves little, and her mouth rests closed between phrases. Between the two moments
> named below her head stays still and her eyes stay on the lens, relaxed; she blinks normally. Only two moments: ...
> The camera holds still on a tripod. A cinematic full-frame camera look with shallow depth of field, natural colour
> and real skin texture; no music, no text, no subtitles.

What made it worse (do not use): "bright and eager, sharing big news", "a surprising money story", "lively,
expressive", "wry and amused", "warm and friendly", a list of movements ("her head tilts and bobs ... eyes glance up or
to the side ... blinks naturally several times"), "the jaw and lower lip move clearly with every syllable", and the
retry's "clear, visible mouth shapes on every vowel".

## Gemini one-change edits of a keyframe (free; gemini-media skill, the bridge's paste route with the pane hidden)
- **Hair only, worked** (identity 0.84 against the frame): "Edit this photo, change only her hair. Keep everything else
  exactly as it is: her face, expression, skin tone, the warm golden window light and the warm rim of sun on her hair,
  the outfit, pose, room and framing. Hair: the same length, colour and soft waves, but neatly groomed, as if brushed and
  blow-dried this morning: smooth, combed, the parting tidy, no flyaways, no frizz, no stray strands across her face.
  Real hair with a natural texture, not glossy, not silky, not plastic. Vertical 9:16, same framing."
- **Hair and light together, worse:** asking also for "no bright orange sun behind her" made her paler and moved the face.
- **Makeup and expression together, rejected:** "change only her makeup and expression ... lips closed in a small
  confident smile" gave a different woman (0.70 against the master; the source frame 0.87). Makeup alone with the
  expression locked kept her face (0.83) but Akhilesh called it "overdoing the makeup".
