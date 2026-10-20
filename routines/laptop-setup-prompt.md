# Laptop setup for production (the Doordhan studio session)

Paste the prompt below into a Claude Code session opened on this repo's folder on Akhilesh's laptop. Run it once, and
again whenever `pipeline/fetch_models.sh` changes. It spends no credits and posts nothing.

Since 2026-10-19 production runs on the laptop by default (Akhilesh's decision after the jio01 timing breakdown in
registry/episodes.md). The cloud route stays available at all times: it is Naveen's only route, and Akhilesh's
fallback ("produce it here"). See SETUP.md, "Day to day", step 4.

---

You are setting up Akhilesh's laptop to produce Doordhan reels. From now on this session (the Doordhan studio
session) runs `/produce-video <slug>` when the morning cloud session hands over an approved script. Get the laptop
ready, prove it with the checks below, and report.

Read first: CLAUDE.md, SETUP.md (step 4 and "The tools on their machine"), section 0 of
.claude/skills/produce-video/SKILL.md, and pipeline/README.md.

Rules for this setup:
- Spend no Higgsfield or ElevenLabs credits. Only free checks: Higgsfield `balance` and `jobs_wait` with timeout 0,
  and `pipeline/tts_elevenlabs.py --check`. Don't run `/produce-video` and don't generate anything.
- Never post or publish anything. Never print, log or commit a key: the ElevenLabs key stays in the git-ignored `.env`.
- Don't change the hard rules in CLAUDE.md. If something needs Akhilesh (a sign-in, a password, a paid plan), stop
  and ask him in one line.

Steps:
1. `git status`, then `git pull origin main`. If there are local changes, show them and ask before stashing or
   committing anything.
2. Homebrew tools: `brew install ffmpeg uv poppler` (skip what is installed). Check that `ffmpeg -encoders` lists
   libx264 and that `pdftoppm -v` runs.
3. `pip3 install -r requirements.txt` for the `python3` that runs the pipeline. If Homebrew's Python refuses
   ("externally managed environment"), use the way this Mac installed it before (SETUP.md and its "Known snag"
   section), or a user install; say which.
4. `bash pipeline/fetch_models.sh`. It updates the QC environment (`~/.venvs/doordhan-qc`, Python 3.11, MediaPipe
   0.10.21), creates the cut-out environment (`~/.venvs/doordhan-cut`, rembg) and downloads the cut-out model (about
   180 MB, into ~/.rembg), the face models and SyncNet. Show the last lines of its output.
5. `python3 pipeline/produce_check.py` must say READY, including the ElevenLabs key check. Fix anything it lists.
6. The self-test: `python3 pipeline/self_test.py` must end ALL PASS; on this Mac the QC checks run with
   `~/.venvs/doordhan-qc/bin/python pipeline/self_test.py` (use whichever SETUP.md says works here). Time it: the cloud
   machine takes about 5.5 minutes.
7. Speed against the cloud: run
   `time ffmpeg -v error -f lavfi -i testsrc2=size=1080x1920:rate=30:duration=20 -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -y /tmp/doordhan_bench.mp4`
   The cloud machine (4 vCPU Xeon 2.1 GHz, no GPU) takes about 19 s. Report the laptop's time, the ratio,
   `sysctl -n hw.ncpu` and the chip (`sysctl -n machdep.cpu.brand_string`).
8. The cut-out tool: `~/.venvs/doordhan-cut/bin/python -I pipeline/cutout.py assets/characters/rashmi_e11_master.jpg /tmp/cut_test.png`.
   It prints a size; open /tmp/cut_test.png and confirm Rashmi is cut out cleanly on a transparent background.
9. Connectors in this local Claude Code:
   - Load the Higgsfield tools and call `balance`. In the desktop app the connector's tools carry its ID, not the
     word Higgsfield (`mcp__808f7b43-…__balance` on 2026-10-20), so search by keyword: ToolSearch "higgsfield balance
     jobs_wait".
   - Call `jobs_wait` with timeout 0 on the generation jobs in registry/assets.json: `style.doordhan_look_vertical`
     and `keyframes.creator_e11_sofa_pink` (the "_levelled" one is an upload). Both should come back `completed`,
     which proves this session sees Akhilesh's workspace. `style.vox_mixed_media_key` is an upload too: `jobs_wait`
     answers `lookup_failed` for every upload, so look for its ID in `show_medias` (type image) instead. One that
     fails is not a blocker (the skill uploads the local copies in assets/ instead), but say which. The vox key has
     no local copy in assets/references/ yet.
   - `python3 pipeline/tts_elevenlabs.py --check`: the key works and eleven_v3 is offered. On the laptop, voices and
     transcripts go over the API (the gate transcribes by itself), not the connector.
10. The studio session itself: confirm `remoteControlAtStartup` and `inputNeededNotifEnabled` are on in
    ~/.claude/settings.json (SETUP.md), so a production run can be started and followed from the phone. Confirm the
    repo's .claude/settings.json hooks load: the QC-stamp check on SendUserFile, and the session-start hook, which does
    nothing on the laptop (it only sets up cloud sessions).
11. Film clips: on the laptop `/produce-video` can download clips itself with `pipeline/fetch_clips.py` (YouTube
    blocks only cloud machines). Leave the hourly "Doordhan: fetch new clip requests" task running: cloud sessions
    (Naveen's route) still use it.
12. Write down what you found. If anything differed from SETUP.md (a package, a path, a new snag), fix SETUP.md, and
    add one line under "Changes to tools and defaults" in registry/episodes.md: "<date>, laptop production setup:
    self-test <minutes>, encode benchmark <s> vs the cloud's 19 s, <anything fixed>". Commit and push to main.
13. Reply to Akhilesh in a few lines: READY or what is missing (and what he must do himself), the self-test result and
    time, the speed ratio, the connector checks, and the one command the morning session will hand over:
    `/produce-video <slug> (registry/scripts/<slug>.json, approved by <who>; format <format>; budget <credits>)`.
