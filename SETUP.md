# Setup: how the system is wired (as of 2026-09-25)

## Day to day
1. **7:30 IST, Mon–Sat:** the cloud news desk emails Akhilesh three story options (subject "Doordhan desk — <date> — 3 stories").
2. He opens Claude Code in `~/doordhan-factory` and replies with a pick, e.g. `2B`. Gate 1: the story.
3. Claude writes the script (playbooks/script.md). Gate 2: the script. No episode credits are spent before this.
4. Claude produces (playbooks/produce.md) and presents the final with its QC notes. Gate 3: the final video.
5. Claude gives the posting kit for Instagram and YouTube Shorts (playbooks/post-kit.md). Akhilesh posts.

## Pieces
| Piece | Where | Notes |
|---|---|---|
| Repo | github.com/takingbreath/doordhan-factory (private); local `~/doordhan-factory` | `work/` and `outputs/` are git-ignored. |
| Toolchain | ffmpeg 8, Python 3.9+ with numpy and pillow (`pip3 install -r requirements.txt`) | `python3 pipeline/self_test.py` must end with ALL PASS. |
| Higgsfield | claude.ai connector, `https://mcp.higgsfield.ai/mcp`, signed in (Pro plan) | Available to any Claude Code session signed in with the claude.ai account. A terminal session that uses an API key instead needs `claude mcp add --transport http higgsfield https://mcp.higgsfield.ai/mcp`, then sign in via `/mcp`. |
| ElevenLabs | claude.ai connector (`api.elevenlabs.io/v1/mcp`), connected 2026-09-25. Optional API key for the scripts: `ELEVENLABS_API_KEY`, or `ELEVENLABS_API_KEY=...` in `~/doordhan-factory/.env` (git-ignored, chmod 600) | The connector generates speech (eleven_v3, eleven_v4), transcribes (eleven_scribe_v1; verified on the test shot) and designs voices, working through ElevenLabs "flows" (see playbooks/produce.md step 3). The file-based scripts (`tts_elevenlabs.py`, `transcribe.py`, the transcript line in `qc.py`) need the key; `python3 pipeline/tts_elevenlabs.py --check` confirms it without printing it. Don't add the server with `claude mcp add` as well; it duplicates the connector. The URL printed on ElevenLabs' setup page fails with a resource mismatch (`api.us.elevenlabs.io`). |
| Gmail | claude.ai connector (`gmailmcp.googleapis.com`) | The routine sends the desk email with it. Claude Code can read that email at the script step. |
| News desk routine | https://claude.ai/code/routines/trig_01MBsrTHZTFUuyMXHiyAbfBC ("Doordhan news desk", model claude-sonnet-5) | Cron `0 2 * * 1-6` (UTC) = 07:30 IST Mon–Sat. Clones this repo, runs routines/newsdesk-routine-prompt.md, and has the Gmail connector only (no Higgsfield, so it can't spend credits). |

To change the routine (time, recipient, model): edit it at claude.ai/code/routines, or ask Claude Code to update it with /schedule. Keep routines/newsdesk-routine-prompt.md in step with it.

## Known snag on this Mac
The `claude` on PATH is an old npm install (1.0.17, `~/.npm-global`) that crashes under Node 25. The desktop app bundles a current Claude Code. For the terminal, run `npm i -g @anthropic-ai/claude-code@latest` or use the native installer.

## History
The repo came from a zip plus one takeover prompt (2026-09-25): unzip, private GitHub repo, pipeline self-test, Higgsfield registry sync, ElevenLabs key check, a ≤10-credit Sarika test shot, and this routine. What changed during that takeover, and why, is logged in registry/episodes.md.
