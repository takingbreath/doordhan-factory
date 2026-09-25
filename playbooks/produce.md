# Playbook: produce (after the script is approved)

_This is the path that has worked so far. Change it whenever you find a better way, and note what you changed in registry/episodes.md._

Work in work/<episode-slug>/. Outputs go to outputs/<episode-slug>/.

1. Shot list: map every approved line to a shot. The template's shot pattern is a starting point, not a script. Default: talking shots on Wan 2.7 (close-ups), scenes without dialogue on Seedance 2.5 or local stills and cards. Choose differently when you have a reason. Reusable clips (registry "clips", e.g. Sarika's tagline ident) cost nothing.
2. Cost plan: estimate credits per shot with the rates in registry `_costs_credits`, or preflight with `get_cost: true` on the generate call (free). Over the budget in CLAUDE.md: ask first.
3. Voices: generate each line. Sarika and Gupta: Higgsfield `generate_audio` with text2speech_v2, variant elevenlabs, voice_type element and the registry voice_id (about 0.15 credits a short line). Voices that live on ElevenLabs: `tts_elevenlabs.py --voice <name>`. Then prep_line.py (tempo 1.15 for anchors and presenters; --phone for callers). Check the printed duration, loudness (-16) and pauses; with an ElevenLabs key, run `transcribe.py raw.mp3 --expect "<line>"` before spending video credits on a mispronounced line.
4. Tracks: make_track.py per talking shot (lead 0.12s, hold 0.4s, whole seconds). If it says a shorter hold saves a second, take it unless the hold carries a reaction. Upload each track to Higgsfield: media_upload, then pipeline/put_upload.py with the returned URL and content type audio/mpeg, then media_confirm.
5. Keyframes: generate any new ones (gpt_image_2_5 with the style reference + sheets). Download, view, check text.
6. Video: submit at most 3 jobs at a time. Talking shots: wan2_7 720p, start_image + audio_references. Non-talking: seedance_2_5 480p. Prompts: describe the shot, the performance and "keep the exact analog look of the start image; no new text, no subtitles". If a preset recommendation comes back, resubmit with `declined_preset_id` (registry style.declined_preset_id; it fired again on the 2026-09-25 test).
7. Download every result and run `qc.py CLIP --track TRACK --box <mouth box> --expect "<line>"`. Find the mouth box once per keyframe with `lipcheck.py --face-crop` and save it in registry `qc.mouth_box_480`. Then look at the contact sheet and at full-size frames of the face and any text. If something keeps failing, change the approach rather than re-rolling the same prompt; ask Akhilesh when the budget or a creative call is at stake.
8. Graphics: logo cards (inset_card.py), title/montage (montage.py), any slates or SMS inserts (build locally).
9. Assemble: write work/<slug>/edit.json, run assemble.py. Cut points come from speech_map.py (or transcribe.py word times) on each generated clip. Give montage parts `"lufs": -17` so the sting sits just under the voices; every other part is levelled to -16 automatically.
10. Hold it to the quality bar in CLAUDE.md: look at the joins sheet, run speech_map on the final (no word cut, no dead gap), and check the first frame shows the subject. Then present: the final file, length, credits spent, what you checked, and anything you're unsure about.
11. Log the episode in registry/episodes.md.
