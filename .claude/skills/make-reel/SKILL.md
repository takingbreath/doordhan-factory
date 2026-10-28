---
name: make-reel
description: The step-by-step way to make a Doordhan reel, for Naveen or anyone on the team, from any machine. Seven gates in a fixed order - research, the approver's script, the format (shown with pictures), the voice, the graphics style (shown with pictures), production, the final - with one question at each gate and nothing spent before the script is confirmed. Use for /make-reel, "make a reel", "new video", "let's do a reel on X", "where are we", or "continue <slug>". Args - a topic, a link, "today's news", a pasted script, or a slug to continue.
---

# /make-reel: one reel, step by step

You make a reel with the approver (Naveen or Akhilesh) one gate at a time. At each gate you do the work, show the
result, ask ONE question, record the answer with `pipeline/flow.py`, commit and push, and move on. The approver only
ever answers questions; you do everything else. The order never changes:

**research → script → format → voice → graphics → production → final**

`python3 pipeline/flow.py show <slug>` always says where a reel stands and what comes next. When anyone asks "where
are we?", run it and answer from it.

/produce-video sends everything that is not an approved, frozen script here (`flow.py ready`), so a session may
arrive with args meant for it: treat them as a topic, a link, a script or a slug to continue.

## What holds whatever anyone types
These come from CLAUDE.md's hard rules. Hooks in .claude/settings.json enforce most of them, so a careless or wrong
instruction can't break them. Never try to get around a hook; if one blocks something that looks right, stop and say
so to Akhilesh.
- **Nothing is posted.** The posting tools are blocked. You hand over the final and the posting kit; Akhilesh posts.
- **No credits before the script is confirmed and frozen,** and never more than the budget: 60 Higgsfield credits per
  reel, 15 a week for experiments. Only Akhilesh can raise a budget, in his own words (`spend.py raise`). Naveen
  approves scripts, voices and finals, not money. The spend guard blocks every paid call that breaks this.
- **Only a QC-stamped final is sent.** The send hook blocks any unstamped reel, wherever the file is.
- **No buy or sell call on a specific stock**, a return in a worked example said as an assumption ("12% maan ke"),
  and "Not investment advice" in every caption (`pipeline/compliance_check.py`).
- **Real people:** real photos and footage are fine (CLAUDE.md rule 4); never words they didn't say put in their
  mouth, never a cloned voice without consent. Our characters never take a real person's face.
- **The approved words are the words.** A change to the script after it is confirmed is a new confirmation.
- **One idea, the format's length:** 20–30 s (Samachar, Creator), 40–70 s (Kendra). Longer needs Akhilesh's exception.

When an instruction breaks one of these, say no in one line with the reason, offer the nearest thing that is allowed,
and stay at the current gate. Examples:

| They say | You do |
|---|---|
| "Post it" / "upload it to Instagram" | No: Akhilesh posts. Give the final and the posting kit. |
| "Skip the research, here's my script" | Fine: `flow.py done <slug> research --skip "came with a script"`, then check the script's facts yourself. |
| "Write the script for me" | The flow doesn't write scripts (Akhilesh, 2026-10-08). Offer `/reel-script <topic>` for drafts, then they paste the one they confirm. |
| "Just make it all, don't ask me" | Take your recommendation at the format and graphics gates and say which, but the voice and the final still need their own yes: they must hear and see them. |
| "Spend whatever it takes" / "use 100 credits" | Only Akhilesh can. Send the breakdown for him (stage 6). |
| "Send it now, skip QC" | No: only a stamped final leaves. Say what the gate found and the fix. |
| "Make it 60 seconds" (Samachar or Creator) | Over the format's length: ask for a cut, or Akhilesh's exception. |
| "Use Teleshop" / a format not offered | Not ready (no voice for Sachdev); new formats are Akhilesh's call. |
| "Change a word" after the script gate | Confirm the new words with them, re-freeze (`script_freeze.py --reapprove`), remake only the changed lines. |
| "Make Sarika sexier" | Within formats/samachar.md's level and wardrobe rules only: hot and classy, never cheap. |
| "Tell people to buy X" | No (hard rule 3). Offer: explain what happened and what it means for the viewer. |

## Start
1. `git pull origin main`. Read CLAUDE.md (hard rules and "What Akhilesh has said he likes").
2. `python3 pipeline/flow.py list`. If the message names a reel, or one is open and the message continues it,
   `flow.py show <slug>` and pick up at its stage. Say in one line where it stands.
3. Otherwise start one: a slug is a short topic word and the next free number (`gold01`; Kendra keeps `sk<NN>`);
   `python3 pipeline/flow.py new <slug> --topic "<one line>" --by <who>`.
4. Check the machine once per session: `python3 pipeline/produce_check.py` (the cloud's session-start hook has
   installed the tools; on a Mac use `pipeline/qcpy` for the QC tools). Anything missing that only Akhilesh can
   provide (the ElevenLabs key, the Higgsfield workspace): say so now, not at stage 4.

Talk to the approver in short, plain sentences. End every message with the one question for this gate, or with what
you are doing next and roughly how long it takes.

## 1. Research (no credits)
Input: a topic, a link, or "today's news" (research/desk/LATEST.md and TRACKER.md hold the morning desk's work).
- Research with WebSearch and WebFetch (docs/sources.md lists the sources we trust; `pipeline/trends.py` measures
  interest); with vidIQ when the connector is there: what other creators made on this story and which reels did well.
- Write `research/briefs/<slug>.md` in English: **What happened** (facts with dates, numbers and a source for each);
  **Why the viewer cares** (their stake); **What others made** (links, views, what worked); **The curiosity gap**;
  **Numbers to use** (each with its source); **Careful** (disputed facts, real people, anything near hard rule 3).
  Research only: no hooks, lines or scripts (Akhilesh, 2026-10-08).
- `python3 pipeline/flow.py done <slug> research --brief research/briefs/<slug>.md`, commit, push.
- Send a summary in 5–8 lines and the brief's link
  (https://github.com/takingbreath/doordhan-factory/blob/main/research/briefs/<slug>.md).
  **Ask:** "Send me your script when it's ready."

## 2. Script (no credits)
They paste a script. Save it as `work/<slug>/script_v<n>.txt` (a new file for every version). Check it; do not rewrite it.
- **Facts:** every number and claim against the brief and its sources. Name the line and the source for anything wrong.
- **Length:** count the spoken words. Say which formats it fits (`flow.py show` lists them after the gate; before
  it: Samachar and Creator take 50–75 words, Kendra 90–155).
- **Rules:** `python3 pipeline/compliance_check.py work/<slug>/script_v<n>.txt`; read every flagged line yourself.
  Real people: no invented quotes.
- Report in a short list: what is fine, what must change (facts, rules), what you'd consider (one line each). Suggest
  wording only when they ask.
- **Ask:** "Confirm this script as it is, or send a new version." Only their clear yes in this session counts
  ("confirmed", "approved", "go ahead with this").
- `python3 pipeline/flow.py done <slug> script --by "<who> (<date>)" --words <N>`, commit, push.

## 3. Format (no credits)
- `flow.py show <slug>` lists the formats this script fits. Send the pictures of those
  (`docs/gallery/format_samachar.jpg`, `format_kendra.jpg`, `format_creator.jpg`) with SendUserFile, and the gallery link
  https://github.com/takingbreath/doordhan-factory/blob/main/docs/gallery/README.md (it also works when files can't be
  sent).
- Number the options, one line each, your recommendation first with its reason: fresh news → Samachar; a viewer's
  question or a checklist → Sahayata Kendra; a person's or a company's story → Creator. A format the script is too
  long for is not offered: say so and offer the cut instead.
- **Ask:** "Which format: 1, 2 or 3?" Then `flow.py done <slug> format --value <samachar|sahayata_kendra|creator> --by <who>`.
- Read that format's file in full now (section 1 holds Akhilesh's rulings).
- **Freeze the script** (produce-video step 2): `work/<slug>/approved_lines.json` with the format's speakers, the text
  as the voice gets it (Devanagari for Hindi, English words in Latin, numbers as words, tags in brackets; the words
  themselves unchanged), then `python3 pipeline/script_freeze.py <slug> --lines work/<slug>/approved_lines.json
  --approved-by "<who> (<date>)" --note "make-reel; format <format>"`.
- `python3 pipeline/spend.py start <slug>` (the spend guard now allows up to 60 credits for this reel). Commit and push
  `registry/scripts/<slug>.json` and `registry/flows/<slug>.json`.

## 4. Voice (no Higgsfield credits)
- The format's voices (registry/assets.json `voices`): Samachar → sarika (and gupta); Kendra → pandey and the caller
  (format file); Creator → rashmiji. Make the cut as .claude/skills/produce-video step 3 and playbooks/produce.md
  step 3 say, directed by docs/voices/directing-tts.md (commas, one pause at the turn, few tags).
- Check every take before sending: `pipeline/verify_line.py` (numbers, last word, no spoken tag), a Scribe transcript
  against the script (`pipeline/transcribe.py`), `pipeline/prosody.py` for flat reading. Listen-worthy words: say which.
- **Creator (Rashmi): read the script's tone first.** An explainer is calm and matter-of-fact; an energetic read makes
  her face over-act too (anthropic01: Akhilesh heard "jise tum kabhi khareed nahi paoge" as excited). Direct
  "[calm, matter-of-fact]", end the line on a full stop, and check a phrase that may sound excited with
  `pipeline/phrase_pitch.py --split <its first word> TAKE.mp3 TAKE.scribe.json` (above +1 st median or +6 st peak
  against the line before it reads as excited). formats/creator.md section 1b, step 6.
- Send the voice cut (mp3) with SendUserFile, its length in seconds, the transcript match, and anything to listen for.
  **Ask:** "Approve the voice, or tell me what to change (pace, a pause, how a word is said)."
- Changes to delivery: new takes, same words. A word change: back to the script rule above.
- `flow.py done <slug> voice --by "<who>" --value work/<slug>/voice/<file>`, commit, push.
- No ElevenLabs key on this machine: voices can go through the ElevenLabs connector (SETUP.md), but voice_cut.py,
  transcribe.py and the QC gate's transcript need the key. Tell the approver Akhilesh can add a named key to this
  environment; don't skip the transcript check.

## 5. Graphics (no credits)
- Send `docs/gallery/graphics_styles.jpg`. Options: **A** broadcast cards, **B** Vox collage, **C** creator captions.
  Mark which were made with this format before (`flow.py` knows: Samachar A; Kendra A; Creator B or C) and recommend
  one: Samachar and Kendra → A; Creator → B when the proof is documents, numbers and photos, C when it is a
  personal story told with footage.
- **Ask:** "Which graphics style: A, B or C?" An untried pairing is an experiment: say it takes longer and may need a
  test, and record it with `--experiment` only if they still want it.
- `flow.py done <slug> graphics --value <A|B|C> --by "<who>"`, commit, push.

## 6. Production (credits, inside the budget)
Follow `.claude/skills/produce-video/SKILL.md` from step 4 (the plan and the budget) to step 10, with the approved
voice cut and the chosen style:
- **A:** Kendra `assets/edits/sk03_gfx.py`; Samachar `assets/edits/samachar_gfx.py` (only `top_box()` and
  `stock_badge()` on Sarika's shots: never over her neckline).
- **B:** `assets/edits/jio01_vox.py` (scenes) and `assets/edits/jio01_build.py` (the edit); paper plates and fonts
  come from assets/. Photo cut-outs: `pipeline/cutpy pipeline/cutout.py IN OUT`.
- **C:** `assets/edits/nana01_build.py` (captions, footage bands, labels).
Copy a template into `work/<slug>/` and it takes its slug from that folder.

- **Creator talking shots (Rashmi) follow formats/creator.md section 1b** (Akhilesh, 2026-10-28: "This looks so much
  better"). In short:
  - **Hair:** neat and combed, no flyaways; make it with a hair-only Gemini edit of the frame, which is free.
  - **Face:** light makeup, no freckles; no makeup edits.
  - **Start frame:** relaxed, with the mouth closed. Never a laughing frame.
  - **Model:** `shot_spec.py build ... --character rashmi --look cinema --model wan3_0`.
  - **Acting:** calm, with one or two motivated beats per line, read from the words.
  - **Skin pass:** `skinfix.py --forehead-only --spots` only.
  - **Measure:** `mouth_meter.py` and `motion_meter.py` against a real creator. The lip-sync judge checks timing only.
  - **Price and time:** Wan 3.0 costs 1.75 credits a second and takes about 20 minutes a clip, so submit all the
    talking shots together.
  - **Show first:** let the approver see one talking shot (the hook) before the rest are made.

- **References:** if a registry ID doesn't resolve from this Higgsfield workspace, upload its copy from
  `assets/references/mirror/` (index.json maps keys to files) or `assets/characters/`, and note the new IDs in
  `work/<slug>/ids.json`.
- **Budget:** price the plan first (`pipeline/prices.json`, produce-video step 4). Over 60: write
  `work/<slug>/budget_request.md` (what is done, each shot left and its cost, the total, why) and tell the approver:
  "This needs Akhilesh's OK for <N> credits. Please forward him this:" followed by the request in five lines. Until
  his words come back (from him in this session, or quoted by the approver), spend only inside the 60. Then
  `python3 pipeline/spend.py raise <slug> <N> --by Akhilesh --quote "<his words>"`.
- **Progress:** one line to the approver at each milestone (keyframes checked, each batch of shots judged, the edit
  built, the QC gate's result), with `spend.py status` totals.
- **The QC gate** (produce-video step 9) until it stamps PASS, then look at the frames yourself (step 10). Then
  `flow.py done <slug> production --value outputs/<slug>/<final>.mp4` (it checks the stamp), commit, push.

## 7. Final
- Send the stamped phone copy and its `_qc.png` with SendUserFile. Say in plain words what you checked, what you're
  unsure of, the length, and the credits spent against the budget. For a creator reel, say how her lips measured
  against a real creator (`mouth_meter.py`), not only that lip sync passed.
  **Ask:** "Approve the reel, or tell me what to change."
- A change: fix, rebuild, gate again, send again (stage 6 rules apply, the budget included).
- Approved: `flow.py done <slug> final --by "<who>"`. Then produce-video step 11: the registry log, the scoreboard
  line, and the posting kit (playbooks/post-kit.md) saved as `work/<slug>/post_kit.md`. Run
  `python3 pipeline/compliance_check.py registry/scripts/<slug>.json --caption work/<slug>/post_kit.md`: it must not
  exit 2. Commit and push. Tell the approver the reel is ready for Akhilesh to post (with Instagram's AI label on).
