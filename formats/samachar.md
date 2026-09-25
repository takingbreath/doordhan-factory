# Template: Doordhan Samachar (news bulletin)

**Premise:** a composed 1990s Doordarshan-style news bulletin reporting today's money news. It explains a real story quickly, with a deadpan joke or two, and tells the viewer what it means for them.
**When to use it:** fresh news (listings, SEBI or RBI moves, markets, tax, prices) where the viewer has a stake and a clear question. Episode 2: NSE listing.

## Characters
- **SARIKA**, anchor. 26, poised, with a knowing wit; since 2026-09-25 a glamorous 1990s film-star newsreader (Akhilesh's call) who wears a **new outfit and hairstyle every episode** (see "Sarika's wardrobe" below). Her face always comes from sheet 85391de0-1855-486d-9e6b-0e7c841fc038. Voice: registry "sarika" (Higgsfield voice element, tempo 1.15; verified 2026-09-25).
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
Akhilesh, 2026-09-25: the same clothes every time gets boring. Vary the neckline and hairstyle to keep interest, as a hook, but don't overdo it, because overdone reads as AI.
1. **Never repeat on air.** Each episode she wears an outfit and hairstyle she hasn't worn before. Check registry `wardrobe_log`, pick from the bank below or design a new one, add it to the bank, and log it once the final is approved. Propose the outfit in one line at the script gate.
2. **The neckline is the hook: vary it, don't escalate it.** Rotate between modest (boat or round neck), medium (square, sweetheart, sleeveless under sheer chiffon; the maroon look is the baseline) and bold (deep V, used sparingly).
   With GPT Image 2.5, name the blouse cut and fabric and never write "cleavage": 4 of 5 prompts that did were blocked, while cut names passed every time. If a prompt is blocked, go one rung more modest; don't reword it to slip past the filter.
3. **Glamorous, not AI-glossy.** Use real 1990s saris and blouse cuts, and natural skin texture with a few flyaways. Makeup is the era's: kohl and brown-red or rose lipstick, no contouring, no glass skin. One or two pieces of jewellery, flat TV-studio light. No pouts, sultry poses or hair flips. Heavy glam makeup ages her, so keep it light enough that she reads 26.
4. **Colour** must stand out against the powder-blue set: no blue saris.
5. **Same face, same set.** References: sheet 85391de0 for the face, close-up 1aed7ca2 for the look, framing and logo. Prompt: copy the wording of a bank keyframe's prompt (it's stored with the job) and change only the outfit, hair and makeup lines.
6. **Framing** stays the head-and-shoulders close-up, because lip-sync needs it. The neckline is only partly in frame; the desk shot shows more.
7. **Cost:** one close-up keyframe per outfit, 0.25 credits (plus a desk frame if the episode opens at the desk). Find its mouth box with `lipcheck.py --face-crop` and record it in the bank.

| # | Outfit | Hair | Neckline | Close-up keyframe | Worn |
|---|---|---|---|---|---|
| 1 | Maroon chiffon, thin gold border; fitted sleeveless gold-silk blouse; gold chain, gold jhumkas; red lipstick | open glossy 90s waves over one shoulder | medium (baseline) | 53a7d3d5-118b-48ce-be8e-3dd475dcd202 (mouth box 200 375 80 60) | glam test X1 (Akhilesh's pick) |
| 2 | Sheer black chiffon, sequinned silver border; sleeveless black boat-neck blouse; silver jhumkas | open, side-swept waves | modest, with sheer drape | c4ffcaa4-6c7c-495f-ad4e-06a5300fda80 | not yet |
| 3 | Bottle-green georgette, thin gold border; short-sleeved sweetheart blouse; emerald studs, gold chain; brown-red lipstick | loose low bun, face-framing strands | medium | 2274317d-c793-4fa5-8005-393969961364 | not yet |
| 4 | Sheer peach chiffon, silver border; sleeveless square-neck blouse; pearl drops; rose lipstick | half-up, soft loose curls | medium | 9a5a400f-cfbf-4035-bcad-573ad0c67dff | not yet |
| 5 | Mustard handloom, maroon border (the original) | low bun with soft waves | modest | 1aed7ca2-bbe1-44e2-8237-6a82d4c5d2cf | Episode 2, T1; keep for sombre stories |

Ideas not generated yet:
- fuchsia georgette, sleeveless, high voluminous ponytail
- white chiffon with black polka dots, red blouse, open curls
- mauve sequinned chiffon, sleeveless V, blow-dried layered bob
- ivory silk with a red border, puff-sleeve blouse, side braid
- a bold deep-V look (expect the filter to block it sometimes)

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
