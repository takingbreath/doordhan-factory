# Script loop inventory

> Historical: this describes the v3.x script loop, before loop v0.3 (3 Oct 2026). The current loop is `docs/script-playbook.md`.

Taken 2026-09-30 from `~/doordhan-factory`, branch `main` at commit `925ca15` (29 Sep), in sync with GitHub. This file is the only thing written, apart from the sync itself.

The local copy was 29 commits behind GitHub, so it was fast-forwarded from `5fbe5dd` to `925ca15` before this inventory. An earlier version of this report was taken before the sync and missed everything from 27 to 29 Sep, including Pandey and the Sahayata Kendra format.

The session was started in `/Users/akhilesh/code/Creator`, which holds only a grocery spreadsheet and `.claude/settings.local.json`. Nothing on this list exists there. All paths below are relative to `~/doordhan-factory`.

## 1. Characters

There are six named characters, plus unnamed callers, and no per-character bible. The only file called a bible is `docs/script-bible.md`, a writing guide shared by every character. Each character is defined inside its format file, with its IDs in `registry/assets.json`.

| Character | Role | Defined in | Bible | Separate mannerisms file |
|---|---|---|---|---|
| Vidyasagar Pandey | Helpline operator, Sahayata Kendra | `formats/sahayata_kendra.md`, section 3 | `docs/script-bible.md` (shared) | None. Inline in `formats/sahayata_kendra.md`: "Expression", "Voice" and "Behaviour" in section 3, and "Performance" in section 1 |
| Billu | Office cat, Sahayata Kendra (no lines) | `formats/sahayata_kendra.md`, section 3 | none applies | None. Inline under "What he does" |
| Callers | Heard on the phone, Sahayata Kendra; a new voice each episode | `formats/sahayata_kendra.md`, section 3 | `docs/script-bible.md` (shared) | None |
| Sarika | Anchor, Doordhan Samachar | `formats/samachar.md` | `docs/script-bible.md` (shared) | None. Inline in `formats/samachar.md` under "Performance: hot and classy, not hot and cheap" and "Recurring devices" |
| Gupta | Field correspondent, Doordhan Samachar | `formats/samachar.md` | `docs/script-bible.md` (shared) | None. Inline under "Recurring devices" |
| Sachdev | Presenter, Abhi Call Karein! | `formats/teleshop.md` | `docs/script-bible.md` (shared) | None. Inline under "Recurring devices" |
| Rahul | Caller, Abhi Call Karein! | `formats/teleshop.md` | `docs/script-bible.md` (shared) | None |

- `reference` folder next to the bible (`docs/reference/`): does not exist, for any character.
- `voice-card.md` next to the bible (`docs/voice-card.md`): does not exist, for any character.
- Neither exists beside the format files in `formats/` either.
- `reference/speech/` at the repository root: does not exist. There is no `reference/` folder at all.

The script bible has not been updated for Pandey. Its two gold examples are the teleshop and Samachar episodes; Pandey's only written lines are in `registry/scripts/sk01.json`.

## 2. Formats

| Format | File | Length limit as written in that file |
|---|---|---|
| Doordhan Sahayata Kendra (the helpline) | `formats/sahayata_kendra.md` | "**No 30 s cap for this format.** Don't over-optimise for seconds; the format is meant to run a little long. E5 ran 67 s." |
| Doordhan Samachar (news bulletin) | `formats/samachar.md` | none stated |
| Abhi Call Karein! (1990s teleshopping) | `formats/teleshop.md` | "It ran 56 seconds. His cap is now 30, so aim for one escalation, not three." |
| Six unbuilt ideas: Hike ki Hatya, Market ka Mausam, Aapke Patra, Bhoot ka Bank Account, Dhanteras Dilemma, Bhavishya Vani | `formats/ideas.md` | none stated |
| Outline for defining a new format (not a format itself) | `formats/_TEMPLATE.md` | none stated |

Two other limits bear on script length.

**The channel-wide reel limit**, which applies to every format that has no ruling of its own:

- `CLAUDE.md`: "**One idea per reel, 20 to 30 seconds** (Akhilesh, 2026-09-25): never over 30. That is about 50 to 75 spoken words at the 1.15 tempo, plus the 2.5 s title montage. If a script runs over, cut it before sending, don't just flag it."
- `docs/script-bible.md`: "Target 20–30 seconds in total, never over 30: about 50–75 spoken words plus the 2.5 s montage."
- `playbooks/produce.md` restates it per format: "20–30 s for news formats; Sahayata Kendra has no 30 s cap".

**A per-line limit**, added 28 Sep, which caps how long one spoken line can be before it must be split:

- `formats/sahayata_kendra.md`: "**Talking shots are capped at about 6 s of speech** (2026-09-28 QC): split longer lines at a pause and cut between the parts as an angle change."
- `formats/samachar.md`: "**Talking shots: about 6 s of speech at most** (2026-09-28 QC over E3-E6 clips): Wan drifts about -8 ms/s, so split longer lines at a pause."

Two things in the repo pull against these limits:

- **Word budget.** The quotes above assume about 2.9 spoken words per second. `registry/episodes.md` (Episode 3) records a measured 3.2 and says "Write 75-80 words for 30 s."
- **Kendra's length.** `docs/strategy.md` notes that the 67 s Kendra debut "worsened as it reached non-followers" and calls it "Evidence for the length rule; judge the format at the weekly review." The format file lists "a shorter 35–45 s cut for Shorts, if long reels underperform" as an untried idea.

## 3. The research step

The research step is the news desk: `playbooks/newsdesk.md`, run by `routines/newsdesk-routine-prompt.md` (Part 1).

- **Files produced for one topic:** none. The desk covers three story options per run, and its whole output is one plain-text email sent through the Gmail connector (subject `Doordhan desk — <date> — 3 stories, pick <n>?`) plus the same three options in the session's final message.
- **Where they're saved:** nowhere in the repository. `pipeline/trends.py` and `pipeline/deep_leads.py` print to the terminal and write no files. The routine prompt says "spend no Higgsfield credits and don't commit" in Part 1. The research survives only in Gmail and in the cloud session's transcript.
- **Sahayata Kendra research:** the format file rules "Research first, script second: for a question episode, bring him the researched answer (sources and numbers) before any script." It names no file or folder for that research, and none was saved for Episode 5.
- **Do they include what other creators are saying about the topic?** No. There are no per-topic files, and the emailed research does not capture other creators' takes, arguments or transcripts. It records only how much others have published and how those videos performed: YouTube video and view counts, vidIQ trending videos and outliers, and the "Gap" score.

The closest saved material comes from the weekly strategist run, after a reel is posted, not from the research step. `reports/weekly-2026-09-27.md` has the heading:

```
WHAT THE COMMENTS AND THE MARKET SAID
```

That section, and "WHAT WE LEARNED" above it, name four creators who covered the Policybazaar story, with their play counts and how each opened ("talking head, rupee or % wipe-out as the first words and the big text"). It records how they hooked the story, not what they said about it. The same finding is in `docs/learnings.md`.

One format is designed around another creator's claim: the "Reel-debunk type" in `formats/sahayata_kendra.md`, section 7. It is marked untested and has no research step or file defined.

## 4. How a finished script reaches text-to-speech today

**File format.** There are two stages, and only the second touches text-to-speech.

1. *The approved script is frozen as JSON.* `playbooks/script.md` step 7 runs `pipeline/script_freeze.py`, which reads `work/<slug>/lines_approved.json` (a git-ignored working file) and writes `registry/scripts/<slug>.json`. Each line has an `id`, a `speaker`, the `text` with delivery tags, and `spoken` with the tags stripped; the file also carries who approved it, when, and a sha256. One exists: `registry/scripts/sk01.json` (Episode 5, frozen on 28 Sep, the day after it was voiced).
2. *Each line is passed to text-to-speech by hand, as plain text, one line per call.* No tool reads the frozen JSON to generate speech. The frozen file is used afterwards, to check that the final video says what was approved (`pipeline/script_diff.py`, run by `pipeline/qc_gate.py`).

The speech routes in use:

- Pandey and the callers: the ElevenLabs connector's `creative_generate_speech`, inside the Claude session (`formats/sahayata_kendra.md`, section 8).
- Sarika and Gupta: Higgsfield `generate_audio` (`text2speech_v2`, variant `elevenlabs`, voice type `element`).
- Script alternatives that need API keys: `pipeline/tts_elevenlabs.py` and `pipeline/higgsfield.py audio`, each taking `--text "..."` or `--text-file line.txt`.

The raw audio then goes through `pipeline/verify_line.py` (the voice gate), `pipeline/prep_line.py` and `pipeline/make_track.py` or `pipeline/shot_spec.py build`.

Only Episode 5 has a script in the repo. Episodes 1 and 2 survive as the gold examples in `docs/script-bible.md`. `registry/reels.csv` records that Episode 4 (tax audit) and X1 (UPI) were made outside the logged flow with "No script" in the repo, and Episode 3's script was not saved either.

**Writing system: mixed.** Hindi words are in Devanagari, English words stay in Roman inside the same sentence, and delivery tags are English in square brackets. This is now written down, in `formats/sahayata_kendra.md`: "Devanagari text with English words kept in Latin." Example from `registry/scripts/sk01.json`:

```
[flat, brisk] घर है? गिनो। ज़मीन है? गिनो। Gold है? गिनो। Shares, mutual funds, FD है? गिनो। Loan है? [pause][slowly] घटाओ।
```

In that script, amounts are spelled as Hindi words ("नब्बे लाख") while "top 1%" keeps its digits. On-screen text is a separate case and is Roman: "Roman Hinglish, never Devanagari" (Kendra ruling), as are hooks in the desk email and captions.

**ElevenLabs model id:** `eleven_v3`. It is the `model` on Pandey's and the caller's registry entries, `TTS_MODEL` in `pipeline/elevenlabs_api.py`, and the default of `pipeline/tts_elevenlabs.py`. Sarika and Gupta still go through Higgsfield's `text2speech_v2` with variant `elevenlabs`; the repo does not say which ElevenLabs model runs behind it.

**Voice id per character** (from `registry/assets.json`, `voices`):

| Character | ElevenLabs voice id | Notes |
|---|---|---|
| Pandey | `RkuMBi6AZByWfSR5Ul5E` | "Pandey (Akhilesh's clone)"; tags "[flat, brisk] default; [slowly] only before punch words" |
| Kendra caller, Episode 5 | `YgpoWAqBbWpygO1YiIEI` | "Bobby - Energetic natural voiceover"; a new caller voice is cast each episode |
| Billu | none | No lines |
| Sarika | none (`null`) | Higgsfield voice element `6603e914-681e-4966-9bbb-cfb1daebf1d5` ("Sarika-News-Anchor-Female"), tempo 1.15 |
| Gupta | none (`null`) | Higgsfield voice element `70f487de-93d3-4c8c-bac9-65d384893c78` ("gupta-news-reporter"), tempo 1.15 |
| Sachdev | none (`null`) | No voice. His Higgsfield voice (`37d2ed5d-2bf5-4065-8290-9c989d2f3d4e`) was deleted |
| Rahul | none (`null`) | No voice id. Higgsfield `seed_audio` with audio reference `70ea3252-872f-428f-9776-c356e521f141`, phone EQ |

`CLAUDE.md` records a decision dated 2026-09-26 to clone Sarika and Gupta into ElevenLabs and use it directly from the next episode. The registry shows that has not happened for them; only the Kendra voices live on ElevenLabs.

**ElevenLabs API key available to the pipeline: no.** The scripts read `ELEVENLABS_API_KEY` from the environment or from `.env` at the repo root. On this machine there is no `.env` (only `.env.example`), the variable is not set in the shell environment or in any shell profile, and no Claude settings file defines it. `docs/api-generation.md` says the key route was "verified live"; that file was committed by Naveen on 26 Sep, so the key it refers to is on another machine. The cloud routines' environment could not be inspected from here. Pandey's voice is reached through the ElevenLabs connector, which is a sign-in, not a key, and the file-based scripts cannot use it.

## 5. Existing files in `.claude/agents/`, `.claude/skills/` and `.claude/workflows/`

None. None of the three folders exists. `.claude/` contains only `settings.json`.

## 6. Existing script-writing prompts or code

Prompts and instructions:

- `docs/script-bible.md`
- `playbooks/script.md`
- `formats/sahayata_kendra.md`
- `formats/samachar.md`
- `formats/teleshop.md`
- `formats/_TEMPLATE.md`
- `formats/ideas.md`
- `routines/newsdesk-routine-prompt.md`
- `CLAUDE.md`
- `playbooks/newsdesk.md`
- `playbooks/produce.md`
- `routines/email-style.md`
- `docs/strategy.md`
- `docs/learnings.md`
- `docs/platform-playbook.md`

Code that writes scripts: none.

Code that stores or checks an approved script:

- `pipeline/script_freeze.py`
- `pipeline/script_diff.py`
- `pipeline/verify_line.py`
- `pipeline/qc_gate.py`
- `registry/scripts/sk01.json`

Code that turns script lines into speech or uses them downstream:

- `pipeline/tts_elevenlabs.py`
- `pipeline/elevenlabs_api.py`
- `pipeline/higgsfield.py`
- `pipeline/higgsfield_api.py`
- `pipeline/shot_spec.py`
- `pipeline/transcribe.py`
- `pipeline/qc.py`

## 7. `prompts/script-writer.md` and `prompts/voice-card-template.md`

- `prompts/script-writer.md`: does not exist.
- `prompts/voice-card-template.md`: does not exist.

There is no `prompts/` folder.
