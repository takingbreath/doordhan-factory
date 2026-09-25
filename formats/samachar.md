# Template: Doordhan Samachar (news bulletin)

**Premise:** a composed 1990s Doordarshan-style news bulletin reporting today's money news. It explains a real story quickly, with a deadpan joke or two, and tells the viewer what it means for them.
**When to use it:** fresh news (listings, SEBI or RBI moves, markets, tax, prices) where the viewer has a stake and a clear question. Episode 2: NSE listing.

## Characters
- **SARIKA**, anchor. 26, poised, with a knowing wit; since 2026-09-25 a glamorous, sexy 1990s newsreader (Akhilesh's call) who wears a **new outfit and hairstyle every episode**, sari or not (see "Sarika's wardrobe" below). Her face always comes from sheet 85391de0-1855-486d-9e6b-0e7c841fc038. Voice: registry "sarika" (Higgsfield voice element, tempo 1.15; verified 2026-09-25).
- **GUPTA**, field correspondent. About 40, bald, moustache, metal spectacles, sand-beige Nehru half-jacket over a pale blue shirt, press card, a dark mic with a DOORDHAN flag. Sheet b51d1f5e-bad5-4f00-af03-f55ff28ed8a0. Voice: registry "gupta". He changes clothes each episode too: a different shirt and half-jacket colour (plain or bold patterns, never small checks), keeping his spectacles, moustache, press card and DOORDHAN mic.

## Sets and keyframes
- Anchor close-ups: one per outfit (see the wardrobe bank below). All use the same powder-blue set, framing and logo.
- Desk, medium shot, framed inset box top-right ("DOORDHAN समाचार"): 3501fe96-8bd8-41e8-bd02-3c5ca42c8bea
- Anchor close-up on the powder-blue backdrop (original mustard sari): 1aed7ca2-bbe1-44e2-8237-6a82d4c5d2cf (mouth box for lipcheck: 195 355 100 80). Use it as the set, framing and logo reference for every new outfit.
- Gupta outside a 90s stock exchange (ticker board, crowd, onlookers staring at him): bed104cc-72e2-4c6b-a3ac-3bde4ef6ebd1
- Gupta on a plain Mumbai street with a queue (weaker; the location looked like a college): 6d133894-ac0d-4276-aead-4a32b14ac821
- Opening title card "दूरधन समाचार": 4b8532b9-f3c8-47a6-80fe-e54b139a724e (local copy: assets/cards/samachar_title.png)
- New story, new location: generate Gupta's keyframe there from his sheet and the style reference, with onlookers reacting to the camera.

## Sarika's wardrobe (a new look every episode)
> **Platform risk, flagged 2026-09-25, awaiting Akhilesh's decision:** Instagram's Recommendation Guidelines exclude "pictures of people in see-through clothing" from recommendations, and Meta demotes suggestive posing. w1's sheer black chiffon is see-through fabric. Recommended: keep the neckline level but use opaque fabrics (silk, satin, georgette, crepe) and head-and-shoulders framing, never a chest-focused frame. See docs/platform-playbook.md.
Akhilesh, 2026-09-25: a glamorous anchor with visible cleavage is the hook for this audience, at the level of the black deep-V sari (w1). The same clothes every episode gets boring, so vary the outfit, neckline shape and hairstyle, and don't go beyond w1, because overdone reads as AI. It doesn't have to be a sari every time.
1. **Never repeat on air.** Each episode she wears an outfit and hairstyle she hasn't worn before. Check registry `wardrobe_log`, pick from the bank or design a new outfit, add it to the bank, and log it once the final is approved. Propose the outfit in one line at the script gate.
2. **Cleavage at w1's level is the baseline.** Vary its shape rather than its amount: deep V, sweetheart, wrap, camisole under an open blazer, satin shirt unbuttoned to a V, off-shoulder. Stay at or just under w1; never more.
3. **Mix sari and non-sari**, all believable for 1990s India:
   - chiffon or georgette saris with low-cut blouses
   - power dressing (blazers with shoulder pads over camisoles)
   - satin or silk shirts
   - wrap dresses
   - Indo-western kurtis with deep necks
   - the occasional salwar suit
   Roughly alternate, and never the same kind of outfit twice in a row.
4. **Model:** make wardrobe keyframes with **seedream_v4_5** (1 credit). GPT Image 2.5 blocked 6 of 8 prompts at this level, and Seedream produced the blazer look on the first try. Wan 2.7 animated w1 with no flag, and its lips scored best of all the tests (1.51 / 1.67). If Seedream blocks a prompt, make that outfit less revealing; don't reword it to slip past the filter.
5. **Glamorous, not AI-glossy.** Natural skin texture and a few flyaways. The era's makeup: kohl, brick-red or rose lipstick, no contouring, no glass skin. One or two pieces of jewellery, flat TV-studio light. No pouts, sultry poses or hair flips; the knowing half-smile is her thing. Heavy makeup ages her, so keep it light enough that she reads 26.
6. **Colour** must stand out against the powder-blue set: no blue outfits.
7. **Same face, same set.** References: sheet 85391de0 for the face, close-up 1aed7ca2 for the look, the powder-blue set and the logo. Frame from just above her head to mid-chest: the face is big enough for lip-sync and the neckline is in shot. Start from the prompt of the nearest bank keyframe (it's stored with the job) and change only the outfit, hair and makeup lines.
8. **Cost:** one close-up keyframe per outfit, 1 credit on Seedream (plus a desk frame if the episode opens at the desk). Find its mouth box with `lipcheck.py --face-crop` and record it in the bank.

| # | Outfit | Hair | Type | Close-up keyframe | Worn |
|---|---|---|---|---|---|
| w1 | Sheer black chiffon, sequinned silver border; fitted black sleeveless deep-V blouse; thin pendant, silver jhumkas; deep red lipstick | open, voluminous side-swept waves | sari (**the reference level**) | 6980440f-99d3-4db4-89e9-5805d4a03303 (GPT Image; mouth box 220 360 70 55) | test X2, Akhilesh's pick |
| w2 | Black blazer with puffed shoulders, open over an ivory satin deep-V camisole; gold hoops; brick-red lipstick | big 90s blow-dry, shoulder length | power dressing | 0182e812-01ff-4161-b46e-2e22b3c4ff1e (Seedream 4.5) | not yet |
| w3 | Maroon chiffon, gold border; sleeveless gold-silk blouse; gold jhumkas | open glossy waves | sari, more covered | 53a7d3d5-118b-48ce-be8e-3dd475dcd202 (mouth box 200 375 80 60) | test X1; too covered on its own, better as a change of pace |
| w4 | Mustard handloom, maroon border (the original) | low bun with soft waves | sari, modest | 1aed7ca2-bbe1-44e2-8237-6a82d4c5d2cf | Episode 2, T1; only for sombre stories |

Retired (Akhilesh: "don't show anything at all"): black boat neck c4ffcaa4, green sweetheart 2274317d, peach square-neck 9a5a400f.

Ideas not generated yet:
- wine-red satin shirt unbuttoned to a V, high voluminous ponytail
- emerald wrap dress with a deep V, blow-dried layered bob
- fuchsia georgette sari with a low sweetheart blouse, hair open
- white chiffon sari with black polka dots and a red deep-V blouse, curls
- ivory kurti with a deep neck and a sheer dupatta, side braid
- an off-shoulder 90s top in mustard or red, big curls

## Performance: hot and classy, not hot and cheap
Akhilesh, 2026-09-25: "there is a line between looking hot and classy vs hot and cheap. We need to be on the hot-and-classy side." The outfit carries the glamour; her performance stays a newsreader's.
- **Classy:** poise, a steady and level head, still shoulders, a direct gaze, expression carried by the eyes and eyebrows, the knowing half-smile at the end.
- **Cheap (never):** head wobbling, bobbing or tilting, hair tossing, leaning into the camera, pouts, winks, lip bites, shoulder shimmies.
- **Wan prompts:** Wan acts out every attitude word. "Glamorous", "playful", "confident", "tilt of the head" and "her hair moves" added a wobble (head travel 66–83 px/s against 37 for the accepted shot). Keep this sentence for every Sarika talking shot and add no attitude words:
  "The news anchor from the start image reads the news in Hindi, her lips moving in exact sync with the provided audio. She is a poised professional newsreader: head steady and level, shoulders still, only a small natural nod on a stressed word, expression carried by her eyes, a faint knowing smile at the end. No head tilting, no bobbing, no hair movement. Locked-off studio camera."
- **QC:** `headcheck.py` (it runs inside qc.py) must PASS (≤45 px/s). If it fails, reshoot with the sentence above rather than cut around it.

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
