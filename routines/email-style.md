# How Doordhan emails look

Every email the routines send (the morning desk, the final video, the weekly strategy review) is plain text, written to be read on a phone in two minutes. Akhilesh asked for readable, not fancy (2026-09-26): no HTML.

## Rules
1. **Action first.** Line 1 says what to do, with the link. Line 3 gives the recommendation. Context goes at the bottom.
2. **One block per story or topic,** separated by a divider line (`━━━━━━━━━━━━━━━━━━━━`) with a blank line on each side.
3. **Titles in CAPS on their own line.** Plain text has no bold, so capitals do its job.
4. **Short labelled lines, one idea each, with a blank line between them.** No paragraph runs longer than about 3 lines on a phone.
5. **Each hook, fact and question on its own line.** Never run A) B) C) together.
6. **No links inside sentences.** Gmail turns every link into a 200-character google.com redirect, which buries the sentence around it.
   - Put links on their own line at the end of a block, starting "Read:".
   - At most 2 per story.
   - The session link goes on line 1 and on the last line.
7. **No internal jargon:**
   - no bet IDs (B1, W1);
   - no file paths;
   - no scoreboard words (WAITING, HOLD, verdict);
   - no "Carries".

   Say it in plain words. `python3 pipeline/scoreboard.py status` gives the "where we stand" lines already in plain English.
8. **No Markdown.** Asterisks, hashes and backticks show up as literal characters in plain text. Use capitals, "•" bullets and blank lines.
9. **Hinglish hooks exactly as they would be spoken,** in quotes.

## The morning desk email

Subject: `Doordhan desk — Sat 26 Sep — pick 1A?` (the date and the recommended pick)

```
Pick today's story: <session link>

My pick: 1A, Tata Sons vs Tata Trusts. It's the hottest of the three, it hits every investor's SIP, and nobody has made a Hinglish Short on it yet.

━━━━━━━━━━━━━━━━━━━━

1. TATA SONS VS TATA TRUSTS
Rising · 8/10 · post by Mon 28 Sep

The story: the Trusts own 66% of Tata Sons and said no to a listing. The board said yes. It's heading to court.

Why people will watch: TCS, Titan and Tata Motors sit in almost every SIP, so it's the viewer's fight too.

Hooks:
A) "Aapke SIP mein Tata hai? Toh Tata ke ghar ka jhagda aapka bhi hai."
B) "66% ka maalik bola nahi, board bola haan."
C) "Tata Sons listing: owner vs board, beech mein aapka paisa."

Show: Samachar. Sarika in close-up, the Tata Sons name in the inset box.

Buzz: 45 of the week's 100 news articles came today. 408K YouTube views this week, and no Hinglish Shorts yet.

Facts:
• Tata Trusts own 66% of Tata Sons.
• The board reappointed Chandrasekaran and backed a listing against the Trusts' wishes.
• The Trusts are weighing the NCLT or the Bombay High Court.

Read: <link>

━━━━━━━━━━━━━━━━━━━━

2. ...

━━━━━━━━━━━━━━━━━━━━

WHERE WE STAND
<the lines from scoreboard.py status>

To pick, reply in the session with a number and a hook letter, e.g. 1A:
<session link>
```

Add a "Watch out:" line to a story only when it needs one: a compliance edge, a rested topic, or a missing voice. Keep it to one or two sentences.

## The weekly strategy email

Subject: `Doordhan strategy — week of <date> — <one-line headline>`

```
Reply with your decisions here: <session link>

THIS WEEK IN ONE LINE
<the headline: what happened and what we do next>

━━━━━━━━━━━━━━━━━━━━

YOUR DECISIONS
1. <question>? Upside: ... If it doesn't work: ...
2. ...
Reply e.g. "1 yes, 2 no".

━━━━━━━━━━━━━━━━━━━━

THE ACCOUNT
<followers, plays, best and worst reel, one line each>

WHAT WE TESTED
• <the bet in plain words>: <result in plain words>. <kept / dropped / still testing>.

WHAT WE LEARNED
• ... (one line each, with the number that shows it)

NEXT WEEK
• ... (what every reel will do)

PLATFORM AND POLICY (only if something changed)
• ...

<session link>
```

## The final-video email

Subject: `Doordhan final — <date> — <story>`

```
Watch it: <video link>
Approve or send fixes: <session link>

LENGTH: 28 s · CREDITS: 47

WHAT I CHECKED
• ...

NOT SURE ABOUT
• ... (or "Nothing.")
```
