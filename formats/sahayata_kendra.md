# Template: Doordhan Sahayata Kendra (customer-care helpline)

_Created 2026-09-27 from Akhilesh's brief. A starting point: experiment freely and record what changes here._

**Premise:** a 1980s–90s government-style helpline on the Doordhan channel. Vidyasagar Pandey, the last desk at the end of every transfer chain, answers one money question per call with one fact and one flat verdict, then stamps it. Same analog broadcast look as the news bulletin (soft CRT video, grain, muted colour, DOORDHAN bug). Where the Samachar anchor is composed and formal, he is blunt, quirky and unfiltered.

**When to use it:** evergreen "everyone wonders, nobody googles" questions, sacred cows ("SIP se ameer ban jaayenge na?"), and debunks of viral reel claims. News stays with Samachar.

## Characters

### VIDYASAGAR PANDEY, operator
Original character; no resemblance to any real person. Reference sheet: Akhilesh's image (2026-09-27); a Seedream sheet ID is to be recorded here once generated.
- **Who:** mid 30s, fifteen years on the phones. His name means "ocean of knowledge"; he believes it is accurate, and he is right. Nothing surprises him.
- **Look:** tall and very thin, long neck, big dark unblinking eyes, a jet-black bowl cut with a dead-straight fringe just above the eyebrows (the full bowl cut is visible in every shot), a thick black moustache, a completely deadpan face. Mustard half-sleeve terrycot shirt buttoned to the top, a pen in the chest pocket, an ID card on a blue lanyard, a steel watch, dark brown trousers. He holds a cream corded telephone receiver, often wedged between ear and shoulder. **He never wears a headset** (ignore the one on the reference sheet).
- **Desk (Akhilesh 2026-09-27): only two things on it, Billu and the phone.** No register, stamp, tumbler, pen or papers. Room: ceiling fan, tubelight, calendar, grey almirah, peeling green wall with a blue enamel "DOORDHAN SAHAYATA KENDRA" board.
- **Floor plan (fixed for every angle):** Pandey sits centre; Billu lies at the far screen-left end of the desk (Pandey's right); the cream rotary phone is at the screen-right end (Pandey's left hand); empty desk between them. Master keyframe: Higgsfield 455286ed-c486-4b6f-a523-53cdfd419284. Generate every other angle from the master and check it against this plan (Akhilesh caught a cold-open frame that moved the phone to the centre).
- **Voice:** ElevenLabs voice "pandey" (Akhilesh's; add its ID to registry/assets.json). Hindi with a light Bihari/Bhojpuri flavour: the intonation and a few markers ("ka", "hum", "kahe", "hai na"), never a heavy dialect, never a caricature. Slow, flat and unhurried, with short sentences and long pauses. He never shouts, laughs or gets excited.
- **Mannerisms:**
  - He stares into camera and blinks about once an episode.
  - A long sigh comes before every answer.
    - "Ek minute hold kariye" mid-sentence, then the hold music, then he carries on as if nothing happened.
  - When the caller says something absurd, he holds the receiver away from his ear and looks at it.
  - He says the verdict to camera with the receiver away from his ear.
  - The last beat is the verdict stamp: SATYAAPIT or GALAT (a graphic slammed on screen in the edit, since the desk holds only the phone and Billu).
  - He hangs up mid-caller after the sign-off.
  - Full-name intro every call ("Doordhan Sahayata Kendra, Vidyasagar Pandey bol rahe hain"); callers shorten it or get it wrong, and he corrects them flatly.
- **Behaviour:**
  - He is kind to callers and brutal to the system.
  - He is the enemy of sellers, "free" offers, insurance-plus-investment policies, EMIs dressed as discounts, finfluencer tips and comfortable defaults.
  - He gives one clear verdict per episode, backed by one fact. He never hedges and never gives both sides.
  - Verdicts are about behaviour, products and myths, never buy/sell calls, never promised returns.
- **Not:** a clown, angry, a shouting TV expert, or a teacher. He delivers verdicts rather than lectures. He doesn't do jokes; things are funny around him.

### BILLU, the office cat
A real Indian street cat (desi billi): an orange ginger tabby, a bit heavy in the belly, with a short coarse slightly dusty coat, a notch in the left ear, a healed scar on the nose and bored half-closed eyes. Akhilesh (2026-09-27): grey vanished into the green room, so Billu must contrast with the set; and a plush, symmetrical studio cat "looks very AI", so Billu is a real cat with real flaws, and in video he moves like one (ears swivel, head turns, slow blinks). Sheet: Higgsfield 077c7b16-5911-4a12-838c-1adde9fc0ea9 (prompted as candid film photos, which read far less AI than a studio sheet). Nobody's cat; it arrived one day and stayed. It is the second deadpan in the room, with opinions shown only in stares.
- **What it does:**
  - A slow, unimpressed stare at the phone when a question is stupid, or at the camera when a reel claim is absurd.
  - It ignores, looks away from, or yawns at Vidyasagar when he glances over for approval (use this lightly).
  - Occasionally it does something itself: it answers the ringing phone in an empty office, hangs up with a paw on the cradle, or sits on the register right before the stamp.
- **Rules:**
  - At most one Billu beat per episode, usually in the background.
  - No meowing on cue, no cute tricks.
  - No warmth between them (no petting, no talking to it): two colleagues who tolerate each other.
- **Production:** stills with a slow zoom, or short non-talking clips. **Never in the same generated shot as Vidyasagar's lip-synced lines** (video models drift on animals). Same cat every time; it needs its own reference sheet.

### Callers
Never on camera, and heard through a landline (phone EQ). A new caller each episode: the office guy, the aunty, the college kid, the uncle who already knows everything. The caller is every viewer, sincere and never made fun of. They're cheap voices with no lip-sync, made on ElevenLabs.

## Shared opening (0–3 s)
The rotary phone rings, he picks up and gives the full-name intro. The caller's first line is the hook and must land inside 3 s; the intro can overlap it or be cut to its last words.

## Episode type 1: the Question (about 25 s)
- **0–3 s:** ring, intro, the question (the hook).
- **3–6 s:** the sigh. Optional: the caller adds the common wrong belief, or Billu stares at the phone.
- **6–20 s:** the answer, in short flat sentences: one fact, the verdict. Optional hold beat; optional glance at Billu that gets nothing.
- **20–25 s:** the verdict to camera, receiver away from his ear. The stamp. Sign-off, then he hangs up mid-caller.

## Episode type 2: the Reel (about 28 s)
- **0–3 s:** ring, intro. "Pandey ji, ek reel dekhi, @<creator> keh rahe hain ki <claim>. Sahi hai ka?"
- **3–7 s:** a plain on-screen card: the handle, the exact quote, the date. No footage, no screenshot, no face, no recreation. He reads the claim back flatly.
- **7–20 s:** one verifiable fact takes it apart. Billu stares at camera if it's absurd.
- **20–25 s:** the verdict and the stamp. GALAT, or sometimes SATYAAPIT when the creator was right; that's what keeps the GALATs credible.
- **25–28 s:** he invites the creator to call the Kendra and explain; their handle appears on screen; he hangs up.
- **Rules:**
  - Debunk the claim, not the person. Name them once on the card and once in the caller's line. Never call anyone a fraud or a scammer.
  - Quote them exactly, with the date, checked against the original.
  - Only claims with a clear factual error, from creators with real reach.
  - Never use their video, audio, thumbnail or face, and never repost or remix their reel.
  - The verdict is about the claim's facts, never a buy/sell call.
  - An airtight fact box with source links before scripting.
  - Tag the creator in the caption, and as a collaborator invite where possible. The caption ends with an invitation to reply. Write to earn a response, not to humiliate.

## Rules for both types
- One idea, one fact, one verdict; never a both-sides ending.
- The joke lands on the system, the seller, the myth or the reel, never on the caller.
- No buy/sell calls on securities and no promised returns. The caption carries "Not investment advice".
- Deadpan throughout.
- 30 s hard cap, 20–28 s target.

## Signature elements
- The full-name intro, and callers getting it wrong.
- The sigh.
- The cold-tea sip.
- Hold music: one cheap 90s keyboard loop, the same every episode.
- The stamp in the final frame (the shareable frame).
- Hanging up mid-caller.
- Closing card: "Aapki call hamare liye mahatvapurn hai." over the hold music.

## Production notes
- **Voice pacing (E01, 2026-09-27; Akhilesh: "generally he speaks a little fast, slower only to emphasise"):**
  - Default tag: `[flat, brisk]` or `[flat, matter-of-fact, normal pace]`. Add `[slowly]` only before the punch words.
  - Never tag a whole line "slow". On eleven_v3 that, plus `[pause]`/`[long pause]`, left 1–1.8 s gaps mid-line and stretched the episode from about 65 s to 82 s.
  - The brisk takes kept pauses only at the punches.
- **ElevenLabs connector:** at most 3 generations run at once on this plan. Launch at most 3 takes per batch; the rest fail with "Too many concurrent requests".
- **Caller voice for E01:** "Bobby – Energetic natural voiceover" (YgpoWAqBbWpygO1YiIEI) with phone EQ (highpass 300 Hz, lowpass 3.4 kHz, light compression). Pandey: cloned "Pandey" (RkuMBi6AZByWfSR5Ul5E).
- **Keyframes:** a chest-up desk keyframe for talking shots (Wan 2.7 at 720p, driven by our own audio). Cutaways: phone, tea, register and stamp, Billu. Stamp and on-screen cards are built locally.
- **Needed before episode 1:**
  - Vidyasagar's Seedream character sheet (no headset)
  - Billu's sheet
  - the set keyframe
  - hold-music loop
  - phone-EQ treatment for callers
  - the stamp graphic
  - "pandey" voice ID in the registry
- **Look:** `broadcast`.
- **Closing card (reusable):** assets/clips/sahayata_endcard.mp4, rebuilt with `pipeline/sahayata_endcard.py`.
  - Sound: the call cuts (three disconnect beeps), then the Kendra's hold music (Für Elise on a cheap 90s keyboard, public domain).
  - Picture: "AAPKI CALL HAMARE LIYE MAHATVAPURN THI." in Roman Hinglish, with "(Your call was important to us.)" underneath.
- **On-screen text (Akhilesh, 2026-09-27):**
  - Roman Hinglish, never Devanagari.
  - The caller's question goes on screen in **English**, big and bold in a funky font.
  - Fonts are in assets/fonts (Bungee, Rubik Mono One, Titan One, Baloo 2), downloaded from jsDelivr's fontsource; GitHub's raw files were blocked from the cloud machine.
- **Camera (Akhilesh, 2026-09-27):** the format is for creative edits, not a locked-off 1990s camera.
  - Pans, multiple angles and POVs are welcome.
  - Push-ins and zooms that follow the action: punch in on the pick-up; pull out as he exhales the sigh.
  - The analog look stays. Lip-synced shots still hold the camera still in the model; the moves happen in the edit or in non-talking shots.
