# How Doordhan emails look

Every email the routines send (the morning desk, the final video, the weekly strategy review) is plain text, laid out to be read on a phone. No HTML.

Akhilesh (2026-09-26): **keep all the content** (the ratings, how each story was evaluated, everything that was seen and checked). The earlier emails had the right content; they just weren't readable. So nothing gets cut; the layout does the work.

## Rules
1. **Keep every piece of content.**
   - For the desk: the score and its breakdown, all the trend evidence, why it's interesting, the format, all three hooks, the line worth sending, the tests the reel carries, every fact with its source, any watch-outs, and anything else "on the wire".
2. **Action first.** Line 1 says what to do, with the link. The recommendation and its reasons come next.
3. **Dividers between stories.** Use a divider line (`━━━━━━━━━━━━━━━━━━━━`) with a blank line on each side.
4. **Story titles in CAPS,** numbered. Plain text has no bold, so capitals do its job.
5. **Sections inside a story:**
   - a short label line ending in a colon ("Score:", "What we saw:", "Hooks:");
   - the content underneath;
   - a blank line between sections.
6. **One item per line.**
   - Each hook, fact, piece of evidence and question gets its own line.
   - Lists use "•".
   - Never run A) B) C) together on one line.
7. **Links on their own line, under the thing they support.**
   - Gmail turns every link into a long google.com redirect, which buries any sentence it sits inside.
   - So each fact gets a source line ("BusinessToday, 25 Sep:") with its link on the next line.
   - Keep every link; just never put one mid-sentence.
8. **Plain words for internal labels.** Write "Tests this reel carries: hook in frame one, tight 20–30 s, a line worth sending", not "Carries: B1 B2 B3". No file paths.
   - `python3 pipeline/scoreboard.py status` gives the "where we stand" lines in plain English, numbers included.
9. **No Markdown.** Asterisks, hashes and backticks show up as literal characters.
10. **Hinglish hooks and lines exactly as they would be spoken,** in quotes.

## The morning desk email

Subject: `Doordhan desk — Sat 26 Sep — 3 stories, pick 1A?`

```
Pick today's story here: <session link>

MY PICK: 1A
It's the hottest of the three and hits every investor's money. The hook is a plain statement of their stake, and nobody has made a Hinglish Short on it yet. Runner-up: 2, if you want a stock-mover. It's Saturday, so it can go up tonight (7–9 pm) or Monday.

━━━━━━━━━━━━━━━━━━━━

1. TATA SONS VS TATA TRUSTS: THE OWNER SAYS NO, THE BOARD SAYS YES, AND THE LISTING IS HEADED FOR COURT
RISING · 8/10 · post by Mon 28 Sep

Score: 8/10
Momentum 2/3 · Stake 2/2 · Shareability 2/2 · Gap 2/2 · Clarity 0/1

What we saw:
• News: 45 of the week's 100 articles landed today (rising)
• YouTube this week: 12 videos, 408K views
• vidIQ "tata sons listing": search volume 53, competition 46
• Outliers: all long-form news (NEWS9, Mint, ANI); no Hinglish Shorts on it

Why it's interesting:
A 158-year-old family business having a public fight. TCS, Titan and Tata Motors are in nearly every Nifty fund and SIP, so it's the viewer's fight too.

Format:
Samachar (news reading). Sarika's close-up, with the Tata Sons name on a card in the inset box.

Hooks:
A) "Aapke SIP mein Tata hai? Toh Tata ke ghar ka jhagda aapka bhi hai."
B) "66% ka maalik bola nahi, board bola haan: Tata Sons ka IPO ab court tay karega?"
C) "Tata Sons listing: owner vs board, beech mein aapka paisa."

Line worth sending:
"Board aur maalik lad rahe hain; bill shareholder bharega."

Tests this reel carries:
Hook in frame one · Tight 20–30 s · A line worth sending

Fact box:
• Tata Trusts own 66% of Tata Sons. The board reappointed Chandrasekaran and agreed to proceed with a listing despite the Trusts' opposition. The Trusts are weighing the NCLT or the Bombay High Court.
  BusinessToday, 25 Sep:
  <link>

• Salve vs Singhvi: the "majority amongst two" row over the articles, and the casting vote.
  Reuters explainer via TBS, 25 Sep:
  <link>

• Context only (8 days old, not for a hook): listed Tata firms lost $4 bn in market value on 18 Sep.
  Business Recorder:
  <link>

━━━━━━━━━━━━━━━━━━━━

2. ... (same sections)

━━━━━━━━━━━━━━━━━━━━

3. DEEP LANE: ... (same sections; "What we saw" names the outlet, e.g. "via The Ken, 24 Sep")

━━━━━━━━━━━━━━━━━━━━

ALSO ON THE WIRE (if anything)
• ...

━━━━━━━━━━━━━━━━━━━━

WHERE WE STAND
<scoreboard.py status, as is>

To pick, reply in the session with a number and a hook letter, e.g. 1A:
<session link>
```

Add a "Watch out:" section to a story whenever there's a compliance edge, a rested topic, or a missing voice, with the full reasoning.

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
