# Sunday insights scan (laptop, browser): DRAFT, test run pending

**Why:** vidIQ's owner feed gives plays, likes, comments, shares, saves, average watch, watched % and skip rate. Instagram's own insights also show:
- the retention graph;
- follows per reel;
- where views came from (Reels tab, Explore, profile, feed), and followers against non-followers;
- reach, profile visits, reposts;
- audience age, gender and cities.

Once a week, this scan reads those from Akhilesh's logged-in browser on the laptop and commits them, so the cloud strategist's Sunday review (21:30 IST) can diagnose the hold and follow stages. vidIQ stays the nightly source (Akhilesh, 2026-09-28).

It must run with **no intervention from Akhilesh**. Anything that would need him (a permission dialog, a login or security prompt, a missing tool) is a failure to log and notify, never something to wait on.

## Rules (read-only; the account's standing comes first)
- **Only read and screenshot.** Never like, follow, comment, reply, DM, boost, edit a post or caption, change a setting, accept a prompt, or post (hard rule 6).
- **Never touch a login or security screen.** On a login page, a "confirm it's you" checkpoint, a CAPTCHA or any security prompt: stop at once, don't type anything, and notify Akhilesh.
- **Work in your own tab.** Open a new tab for the scan and never touch his other tabs.
- **Pace like a person:** a few seconds between page loads, one pass per week, no bulk scrolling loops.
- Never print or commit cookies, tokens or session data (hard rule 5).

## Test run (do this first, once; Akhilesh asked for it on 2026-09-28)
Goal: learn what is actually available and how to run it unattended, then turn this file into the weekly routine.
1. **Tools.**
   - Check which browser tools this session has: Claude in Chrome (`mcp__claude-in-chrome__*`) or the desktop app's built-in browser (`mcp__Claude_Browser__*`).
   - Log which ones exist and whether any call raised a permission or site-approval prompt. The repo's `.claude/settings.json` bypasses Claude Code prompts; the Chrome extension has its own per-site approval. Note exactly what it asked and how to make it permanent.
2. **Where the data is.** For one recent reel and for the account, visit:
   - (a) instagram.com (profile, then the reel, then "View insights" if it's offered);
   - (b) Meta Business Suite insights at business.facebook.com (content and audience);
   - (c) the Professional dashboard, if the web has one.

   For each place, log which of these it shows:
   - plays/views, reach, likes, comments, shares, saves, reposts;
   - follows from the reel, profile visits;
   - average watch time, skip rate, and the retention graph (as numbers or only as a picture?);
   - view sources, and followers vs non-followers;
   - audience age, gender, cities, active times;
   - and how far back it goes.
3. **Reading method.** For each item, log whether it can be read as text from the page or only from a screenshot.
4. **Policybazaar check.** Record DdvCsyIyc4C's plays from Instagram's own insights. vidIQ's owner feed says 316 and the public count is 2,381; we need to know which one Instagram's insights agree with.
5. **Unattended.** Find out how to start this weekly on the laptop with no one at the keyboard:
   - a Claude desktop scheduled task, or cron/launchd running `claude -p` with Chrome enabled;
   - test that the chosen way reaches the browser tools without a prompt;
   - check what happens if the laptop is asleep or Chrome is closed at the scheduled time.
6. **Log and commit.**
   - Write everything to `docs/insights-scan-log.md` (dated) and commit and push to main as "insights scan: test run".
   - Push-notify Akhilesh with one line: what's available, and whether it can run unattended or what exactly still blocks it.

## Weekly routine (to be written from the test run's findings)
- **When:** Sundays about 20:30 IST, an hour before the strategist.
- **What:** for every reel posted in the last 14 days plus the account, save one JSON per week to `registry/ig_insights/<YYYY-MM-DD>.json` with the fields the test run found. Screenshots go to work/ (git-ignored); only numbers are committed.
- **The strategist's Sunday run** reads the latest file:
  - follows per reel → the follow stage;
  - retention drop points → the hold stage;
  - view sources → reach to non-followers.

  If the file is missing or older than 2 days, it says so in the email and carries on with vidIQ.
- **On failure** (laptop off, logged out, checkpoint, tool missing): no retries, commit a one-line failure note to the log, and push-notify.
