# Gemini pictures with no download (for covers and keyframes)

A project copy of the scripts from Akhilesh's `gemini-media` skill (~/.claude/skills/gemini-media on his laptop), so
that Naveen and any session on this repo can make Gemini pictures the same way. The skill's SKILL.md has the full
story and the routes that do not work. This is the short path that made the E16 cover (2026-11-14, 0 credits).

Needs: Claude's built-in browser (mcp__Claude_Browser__*) logged in to Gemini (a Pro account), Python 3, curl, ffmpeg.
Why the bridge: a download in the built-in browser opens a Mac Save panel that nobody can press. The bridge moves files
between the page and a folder over a local WebRTC channel (127.0.0.1 only, a random token, files only in OUT_DIR).

1. Put the reference picture in a folder: `work/<slug>/cover/gem/ref.jpg` (the presenter's master keyframe; scale it
   to about 1080 px wide).
2. `pipeline/gemini/bridge.sh start work/<slug>/cover/gem` prints a receiver address. Open it in a new browser tab
   (`tabs_create`, then `navigate`) and leave the tab open.
3. Open `https://gemini.google.com/app` in another tab. Paste `bridge_offer.js` (javascript_tool). It returns
   `m1|o|...`. Run `pipeline/gemini/bridge.sh answer 'm1|o|...'`. It returns `m1|a|...`.
4. In the Gemini tab paste `window.MJL = {answer: 'm1|a|...', get: ['ref.jpg'], paste: true};` followed by
   `bridge_get.js`, in one call. The picture is attached to the prompt box.
5. Click the prompt box, type the prompt (keep it under about 700 characters; see docs/covers.md for the cover prompt),
   press Return, and wait about 60 s (`document.querySelectorAll('button[aria-label="Download full-sized image"]')`
   counts the finished pictures).
6. Paste `capture_full_url.js` (the whole file, every time). It keeps the full-size picture in `window.__fullBlob`
   and starts no download. Then send it to the folder with `window.MJL = {answer: <same line>, items: [{name:
   'scene.png', blobVar: '__fullBlob'}]};` followed by `bridge_send.js`. On a channel that is already open, a small
   helper that sends `__fullBlob` in 64 KB chunks is enough (E16 did this; see work notes).
7. `pipeline/gemini/clear_sparkle.sh scene.png scene_clean.png check.png` removes Gemini's star from the bottom right.
   Look at check.png. If the star sits on an edge (a shoulder against a dark background), a fill smears it. Instead,
   push that corner out of the frame with the cover's `scene_zoom` and `scene_shift` (E16).
8. `pipeline/gemini/bridge.sh stop` when done, and close the tabs you opened.

Never click Gemini's own Download, Share or Copy image buttons (a Save panel, a public link, a small copy).
