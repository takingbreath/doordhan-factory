# How Doordhan emails look

The morning desk email is HTML (Akhilesh, 2026-10-08: the plain-text desk email was unreadable), rendered by `pipeline/desk_report.py` from the day's research JSON. The other emails (the final video, the weekly strategy review) are still plain text, laid out to be read on a phone, by the rules below.

Akhilesh (2026-09-26): **keep all the content** (the ratings, how each story was evaluated, everything that was seen and checked). The earlier emails had the right content; they just weren't readable. So nothing gets cut; the layout does the work.

## Rules for the plain-text emails (final video, weekly review)
1. **Keep every piece of content.**
2. **Action first.** Line 1 says what to do, with the link. The recommendation and its reasons come next.
3. **Dividers between stories.** Use a divider line (`━━━━━━━━━━━━━━━━━━━━`) with a blank line on each side.
4. **Story titles in CAPS,** numbered. Plain text has no bold, so capitals do its job.
5. **Sections inside a story:**
   - a short label line ending in a colon ("Score:", "What we saw:");
   - the content underneath;
   - a blank line between sections.
6. **One item per line.**
   - Each fact, piece of evidence and question gets its own line.
   - Lists use "•".
   - Never run A) B) C) together on one line.
7. **Links on their own line, under the thing they support.**
   - Gmail turns every link into a long google.com redirect, which buries any sentence it sits inside.
   - So each fact gets a source line ("BusinessToday, 25 Sep:") with its link on the next line.
   - Keep every link; just never put one mid-sentence.
8. **Plain words for internal labels.** Write "Tests this reel carries: hook in frame one, tight 20–30 s, a line worth sending", not "Carries: B1 B2 B3". No file paths.
   - `python3 pipeline/scoreboard.py status` gives the "where we stand" lines in plain English, numbers included.
9. **No Markdown.** Asterisks, hashes and backticks show up as literal characters.
10. **Hinglish lines exactly as they would be spoken,** in quotes (the final-video email quoting the script). The desk email is English only.

## The morning desk email (HTML, since 2026-10-08)

Akhilesh, 2026-10-08:
- **Research only. No hooks, no "line worth sending", no script, no Hinglish lines.** He writes the script himself.
- **English only.** No Hinglish or Hindi anywhere in the email.
- For each story: what exactly is going on, what other creators are making on it and which of their reels perform best, and **the curiosity gap**: why a viewer would want to know. Example (Snapdeal, E8): a Shark Tank judge's company, a brand everyone used once and then stopped hearing about, is suddenly listing. Nobody knew what it does now.
- Keep the scores, the trend evidence, the sources and the watch-outs.
- Stories carry over: the tracker board shows every story still in the news cycle, whether it's rising or fading.

How it's made:
1. Write the day's research as JSON in `research/desk/<date>.json` (copy the shape of `research/desk/2026-10-08.json`).
2. `python3 pipeline/desk_report.py research/desk/<date>.json` writes the Markdown (`research/desk/<date>.md`, `LATEST.md`, `TRACKER.md`) and the email body (`work/desk/<date>.html`).
3. Send that HTML as `htmlBody` with Gmail's send_message, and put a short plain-text `body` alongside it (the pick, the three titles with scores, the session link) for clients that don't show HTML.

Subject: `Doordhan desk — Thu 08 Oct — 3 stories, pick 1?`

The layout, top to bottom:
- **The pick:** which story and why, the runner-up, and the button back to the session.
- **A correction box**, only when an earlier email got something wrong.
- **Each story:**
  - its number, lane, title, heat label and score;
  - the five-part score strip;
  - What's happening;
  - The curiosity gap;
  - How hot it is;
  - What others are making (creator, what they did, views, how far above their usual, linked);
  - Facts and sources (every fact links its source);
  - Watch out.
- **Stories we're tracking:** the tracker board, each with its heat label and direction.
- **Also on the wire**, then **Where we stand** (`scoreboard.py status`), then the button again.

Design rules (impeccable and emil-design-eng skills):
- Light, warm newsprint, one vermilion accent. Heat labels are colour-coded: HOT vermilion, RISING amber, FLAT slate, COLD blue.
- Serif headlines, system sans body, tabular numerals.
- Inline styles only, with a table layout, 620 px max width. Read it at 390 px before sending.
- No animation: email clients don't run it, and the email is read once a day.
- Change the design in `desk_report.py`, never by hand in one day's email.

## The weekly strategy email

Subject: `Doordhan strategy — week of <date> — <one-line headline>`

The content is everything in the strategist's step 12: the account, the book, what we learned, next week's plan, decisions, and platform and policy. Every number stays.

```
Reply with your decisions here: <session link>

THIS WEEK IN ONE LINE
<what happened and what we do next>

━━━━━━━━━━━━━━━━━━━━

YOUR DECISIONS
1. <question>?
   Upside: ...
   If it doesn't work: ... (the stop)
2. ...
Reply e.g. "1 yes, 2 no".

━━━━━━━━━━━━━━━━━━━━

THE ACCOUNT
Followers: ...
Plays this week: ...
Best reel: ...
Worst reel: ...
Stage 1 progress: ... (on track / behind, and why)
Credits this week: ... (... per 1,000 plays)

━━━━━━━━━━━━━━━━━━━━

THE BETS
Hook in frame one
  Swipe-aways in the first 3 s: 61% at the start → 48% now. Target 45%, stop 58%.
  Reels: 3 of 3. Verdict: still testing / hit its target / hit its stop.
  Why: ...
(one block per bet, including those closed this week)

━━━━━━━━━━━━━━━━━━━━

WHAT WE LEARNED
• ... (each with the numbers that show it)

NEXT WEEK
• ...

WHAT THE COMMENTS AND THE MARKET SAID
• ...

PLATFORM AND POLICY (if anything changed)
• ...
  Source:
  <link>

<session link>
```

## The final-video email

Subject: `Doordhan final — <date> — <story>`

```
Watch it:
<video link>

Approve or send fixes here:
<session link>

Length: 28 s
Credits: 47 (budget 60)

What I checked:
• ...

Not sure about:
• ... (or "Nothing.")
```
