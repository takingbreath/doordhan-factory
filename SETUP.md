# Setup: how the system is wired (as of 2026-09-25)

## Day to day (from your phone)
1. **7:30 IST, Mon–Sat:** the routine starts a cloud session (Opus 5.5). It researches, emails three story options with a direct link to that session, and pings your phone.
2. **Pick:** open the link (or Claude app → Code → Routines → Doordhan news desk → today's run) and reply, e.g. `2B`. Gate 1.
3. **Script:** it replies there with the script (20–30 s) and each character's outfit, and pings you. Reply "approved" or send edits. Gate 2; nothing is spent before this.
4. **Production, in the same cloud session:** it installs its tools, runs the self-test, and makes the reel (Higgsfield, ElevenLabs transcript checks, full QC), posting one line per milestone. The laptop isn't needed.
5. **Final:** a playable link in the session and by email, with QC notes and credits spent; your phone gets pinged. Gate 3. Then the posting kit, and the episode is logged and pushed to the repo. You post.

**Doordhan studio** is the Claude Code session on the laptop (Remote Control on). Use it for anything outside the daily flow: fixes, experiments, new formats. Every new local session starts with Remote Control on and pings the phone when it needs you (`remoteControlAtStartup` and `inputNeededNotifEnabled` in ~/.claude/settings.json).
Permissions: this repo's `.claude/settings.json` runs local sessions with no prompts, and the routine's tools and connectors (Gmail, Higgsfield, ElevenLabs) are pre-allowed.

## Pieces
| Piece | Where | Notes |
|---|---|---|
| Repo | github.com/takingbreath/doordhan-factory (private); local `~/doordhan-factory` | `work/` and `outputs/` are git-ignored. |
| Toolchain | ffmpeg 8, Python 3.9+ with numpy and pillow (`pip3 install -r requirements.txt`) | `python3 pipeline/self_test.py` must end with ALL PASS. |
| Higgsfield | claude.ai connector, `https://mcp.higgsfield.ai/mcp`, signed in (Pro plan) | Available to any Claude Code session signed in with the claude.ai account. A terminal session that uses an API key instead needs `claude mcp add --transport http higgsfield https://mcp.higgsfield.ai/mcp`, then sign in via `/mcp`. |
| ElevenLabs | claude.ai connector (`api.elevenlabs.io/v1/mcp`), connected 2026-09-25. Optional API key for the scripts: `ELEVENLABS_API_KEY`, or `ELEVENLABS_API_KEY=...` in `~/doordhan-factory/.env` (git-ignored, chmod 600) | The connector generates speech (eleven_v3, eleven_v4), transcribes (eleven_scribe_v1; verified on the test shot) and designs voices, working through ElevenLabs "flows" (see playbooks/produce.md step 3). The file-based scripts (`tts_elevenlabs.py`, `transcribe.py`, the transcript line in `qc.py`) need the key; `python3 pipeline/tts_elevenlabs.py --check` confirms it without printing it. Don't add the server with `claude mcp add` as well; it duplicates the connector. The URL printed on ElevenLabs' setup page fails with a resource mismatch (`api.us.elevenlabs.io`). |
| Gmail | claude.ai connector (`gmailmcp.googleapis.com`) | The routine sends the desk email with it. Claude Code can read that email at the script step. |
| Morning routine | https://claude.ai/code/routines/trig_01MBsrTHZTFUuyMXHiyAbfBC ("Doordhan news desk", model claude-opus-5-5) | Cron `0 2 * * 1-6` (UTC) = 07:30 IST Mon–Sat. Clones this repo and runs routines/newsdesk-routine-prompt.md: the news desk, then script and production in the same session once you reply. Connectors: Gmail, Higgsfield, ElevenLabs. No credits before the script is approved. Cloud probe 2026-09-25: ffmpeg and numpy install in about 30 s, self-test ALL PASS, Higgsfield downloads and uploads work, it can push to main, and PushNotification reaches the phone. |

To change the routine (time, recipient, model): edit it at claude.ai/code/routines, or ask Claude Code to update it with /schedule. Keep routines/newsdesk-routine-prompt.md in step with it.

## Known snag on this Mac
The `claude` on PATH is an old npm install (1.0.17, `~/.npm-global`) that crashes under Node 25. The desktop app bundles a current Claude Code. For the terminal, run `npm i -g @anthropic-ai/claude-code@latest` or use the native installer.

## History
The repo came from a zip plus one takeover prompt (2026-09-25): unzip, private GitHub repo, pipeline self-test, Higgsfield registry sync, ElevenLabs key check, a ≤10-credit Sarika test shot, and this routine. What changed during that takeover, and why, is logged in registry/episodes.md.
