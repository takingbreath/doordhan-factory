# Playbook: news desk

_This is the path that has worked so far. Change it whenever you find a better way, and note what you changed in registry/episodes.md._

Goal: three story options Akhilesh can pick from in 30 seconds, each graded on how likely it is to travel.
**We're traders: we ride the trend.** Get in while a story is rising. A story everyone has already covered needs a sharper angle. And some of the best reels are well-researched stories the audience never read (Akhilesh, 2026-09-25).

## Two lanes
- **Hot lane (two options):** what people are searching for, watching and sharing right now.
- **Deep lane (one option):** a story from well-researched journalism (list in docs/sources.md) that most of our viewers haven't read, often behind a paywall. We use the headline and the public facts, verify everything ourselves from open sources, never copy paywalled text, and credit the outlet in the caption ("via The Ken") when the story is theirs.

## Steps
1. Get today's date from the system clock (do not trust injected dates).
2. Read CLAUDE.md (rested topics, hard rules), registry/episodes.md (topics already made), docs/learnings.md (the analyst's "Ride now" and "This week" notes: follow-ups on reels that are taking off come first) and docs/platform-playbook.md.
3. **Gather about ten candidates:**
   - Web searches across markets, IPOs and listings, SEBI and RBI, tax, banks and salaries, gold and fuel, big company events, viral money stories (last 48 hours).
   - Google Trends India: the bottom line of `pipeline/trends.py` lists what India is searching for right now.
   - vidIQ connector: trending videos and outliers (videos far outperforming their channel's usual views) in Indian finance and business this week. Outliers show what is breaking out before the news catches up.
   - Deep lane: `python3 pipeline/deep_leads.py` gives the last 7 days of headlines from the top eight sources in docs/sources.md (The Ken, The Morning Context, SEBI orders, Moneylife, ET Prime, Reuters exclusives, The Arc, The Core).
4. **Filter out** rested topics, anything that would need a buy/sell call, and topics already made, unless there's a genuinely new turn.
5. **Measure** every surviving candidate: `python3 pipeline/trends.py "<english phrase>|<hindi phrase>" ...`. It labels each one HOT, RISING, FLAT or COLD, from Google Trends, Google News momentum (the share of the week's coverage that landed today) and YouTube this week (videos, views, best views per hour). On the top five, run vidIQ keyword research: search volume, competition and trend direction.
6. **Grade each candidate out of 10:**

   | Factor | Points | What earns them |
   |---|---|---|
   | Momentum | 0–3 | 3 HOT (trending on Google, or a video on it gaining ≥3,000 views/hour within 72 h); 2 RISING (≥35% of the week's coverage came today, or uploads are accelerating); 1 FLAT; 0 COLD or fading. The deep lane can score 0 here. |
   | Stake | 0–2 | Hits the viewer's money or time this week (2), some day (1), abstract (0). |
   | Shareability | 0–2 | Makes someone send it to a friend: outrage at the system, a surprising number, relatable pain, an "I told you so". |
   | Gap | 0–2 | Plenty of interest but few good Hinglish shorts on it (vidIQ competition low, few Shorts), or a deep-lane story nobody has made yet. 0 if everyone has already posted the same angle. |
   | Clarity | 0–1 | One number or image that lands in two seconds. |

   Also note the **window**: until when the story stays relevant, e.g. "post by Sun 27 Sep; the strike starts Monday".
7. **Pick** the top two from the hot lane and the best one from the deep lane, in different shapes (e.g. wallet hit, market move, rule or company story). Recommend one.
8. **Verify the fact box:** open each source page and confirm every number is on it. A hook may only use numbers from its own fact box, and a source older than a week can give context but never the headline number.
9. Send the options in this shape:

   **1. [Headline in plain English]**  (HOT · 8/10 · post by Sun 27 Sep)
   - Trend evidence: one line, e.g. "Google trending: बैंक 5000+; 90 news articles today; YouTube this week 1.1M views, top video 15K/hr"
   - Why it's interesting: one line (the clickbait angle)
   - Format: a template from formats/, or a new format pitched in one line
   - Hooks: A) ... B) ... C) ... (each one plain sentence, viewer's stake)
   - Fact box: 2–4 facts with source links

10. End with: "Reply with a number and a hook letter, e.g. 2B."

## Learning loop
After each reel has been up 24 hours and again at 7 days, record its views, shares and saves on Instagram and YouTube in registry/performance.md, next to the desk's score for that story. Akhilesh can paste the Instagram numbers; for YouTube, use vidIQ channel stats. Once a month, compare the scores with what actually travelled and adjust the weights above. The desk should get better at calling winners every week.
