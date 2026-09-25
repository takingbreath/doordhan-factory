# Playbook: produce (after the script is approved)

_This is the path that has worked so far. Change it whenever you find a better way, and note what you changed in registry/episodes.md._

Work in work/<episode-slug>/. Outputs go to outputs/<episode-slug>/.

1. Shot list: map every approved line to a shot. The template's shot pattern is a starting point, not a script. Default: talking shots on Wan 2.7 (close-ups), scenes without dialogue on Seedance 2.5 or local stills and cards. Choose differently when you have a reason.
2. Cost plan: estimate credits per shot. Over the budget in CLAUDE.md: ask first.
3. Voices: generate each line (tts_elevenlabs.py or Higgsfield text2speech_v2 per registry), then prep_line.py (tempo 1.15 for anchors and presenters; --phone for callers). Listen-proxy check: prep_line prints duration and pauses; flag anything odd.
4. Tracks: make_track.py per talking shot (lead 0.12s, hold 0.4s, whole seconds). Upload each track to Higgsfield: media_upload, then pipeline/put_upload.py with the returned URL and content type audio/mpeg, then media_confirm.
5. Keyframes: generate any new ones (gpt_image_2_5 with the style reference + sheets). Download, view, check text.
6. Video: submit at most 3 jobs at a time. Talking shots: wan2_7 720p, start_image + audio_references. Non-talking: seedance_2_5 480p. Prompts: describe the shot, the performance and "keep the exact analog look of the start image; no new text, no subtitles".
7. Download every result and check it (check_match.py for talking shots, lipcheck.py, contact sheets, your own eyes on the frames). If something keeps failing, change the approach rather than re-rolling the same prompt; ask Akhilesh when the budget or a creative call is at stake.
8. Graphics: logo cards (inset_card.py), title/montage (montage.py), any slates or SMS inserts (build locally).
9. Assemble: write work/<slug>/edit.json, run assemble.py. Cut points come from speech_map.py on each generated clip.
10. Hold it to the quality bar in CLAUDE.md. Then present: the final file, length, credits spent, what you checked, and anything you're unsure about.
11. Log the episode in registry/episodes.md.
