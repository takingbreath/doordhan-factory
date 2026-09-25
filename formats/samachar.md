# Template: Doordhan Samachar (news bulletin)

**Premise:** a composed 1990s Doordarshan-style news bulletin reporting today's money news. It explains a real story quickly, with a deadpan joke or two, and tells the viewer what it means for them.
**When to use it:** fresh news (listings, SEBI or RBI moves, markets, tax, prices) where the viewer has a stake and a clear question. Episode 2: NSE listing.

## Characters
- **SARIKA**, anchor. Mid-20s, poised; low bun with soft waves, mustard handloom sari with a maroon border. Sheet 85391de0-1855-486d-9e6b-0e7c841fc038. Voice: registry "sarika" (Higgsfield voice element, tempo 1.15; verified 2026-09-25).
- **GUPTA**, field correspondent. About 40, bald, moustache, metal spectacles, sand-beige Nehru half-jacket over a pale blue shirt, press card, a dark mic with a DOORDHAN flag. Sheet b51d1f5e-bad5-4f00-af03-f55ff28ed8a0. Voice: registry "gupta".

## Sets and keyframes
- Glam Sarika (test, 2026-09-25, awaiting Akhilesh's pick): close-ups in the same framing, 90s film-star styling. Maroon chiffon with a gold sleeveless blouse: 53a7d3d5-118b-48ce-be8e-3dd475dcd202 (animated; mouth box 200 375 80 60). Black chiffon with a sleeveless boat neck: c4ffcaa4-6c7c-495f-ad4e-06a5300fda80. The image model blocks cleavage-forward prompts, so glam comes from hair, makeup, jewellery, bare shoulders and attitude.
- Desk, medium shot, framed inset box top-right ("DOORDHAN समाचार"): 3501fe96-8bd8-41e8-bd02-3c5ca42c8bea
- Anchor close-up on the powder-blue backdrop: 1aed7ca2-bbe1-44e2-8237-6a82d4c5d2cf (mouth box for lipcheck: 195 355 100 80)
- Gupta outside a 90s stock exchange (ticker board, crowd, onlookers staring at him): bed104cc-72e2-4c6b-a3ac-3bde4ef6ebd1
- Gupta on a plain Mumbai street with a queue (weaker; the location looked like a college): 6d133894-ac0d-4276-aead-4a32b14ac821
- Opening title card "दूरधन समाचार": 4b8532b9-f3c8-47a6-80fe-e54b139a724e (local copy: assets/cards/samachar_title.png)
- New story, new location: generate Gupta's keyframe there from his sheet and the style reference, with onlookers reacting to the camera.

## Look and graphics
- Flat powder-blue studio, DOORDHAN rupee-coin bug top-right, 90s CRT softness. Finish: look `broadcast` (the default in assemble.py).
- Inset box story graphic: the subject's real logo on a light card (inset_card.py auto-detects the box, which sits around x=308–465, y=47–201 in 480x854).

## Sound
- assets/audio/samachar_sting.mp3: the last ~2.5 seconds over the title card, right after the opening question. Never under dialogue.

## Shot pattern that worked (Episode 2, about 34s)
1. Desk: "नमस्कार" and the viewer's-stake question, with the logo card in the inset box.
2. Montage: title card with a pull-back zoom, plus the sting ending.
3. Anchor close-up: the doubt, with the joke line.
4. Correspondent on location: the evidence, spoken flatly and certainly.
5. Anchor close-up, one continuous shot: the payoff that answers the hook, ending on a sly look.

## Ready-made clips
- Sarika's tagline ident, 3 s, close-up: "नमस्कार। सब कुछ महँगा... सच मुफ़्त।", ending on the sly half-smile (assets/clips/sarika_tagline_ident.mp4; registry clips.sarika_tagline_ident). It works as a cold open before the title card or as a sign-off, and costs nothing to reuse.

## Recurring devices
The flat "कतई नहीं" from Gupta; Sarika's knowing half-smile; "picture अभी बाक़ी है"-style sign-offs.

## Notes from production
- Talking shots on Wan 2.7 from close-up or chest-up keyframes. The waist-up desk shot barely moved her lips; keep desk dialogue to the short opening line, or try a tighter desk frame.
- Seedance turned Gupta's long line into gibberish; Wan kept it exact.
- Setup test (2026-09-25): a 3 s Wan 720p close-up from the close-up keyframe, driven by a Higgsfield TTS line, kept the audio exactly (correlation 1.00), moved the lips clearly (mouth/head 1.78), held her face and the logo steady, and cost 4.65 credits including the voice.

## Typical cost
About 45 to 55 credits: roughly 25 seconds of Wan, 1 to 3 keyframes, and voices.
