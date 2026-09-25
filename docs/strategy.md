# Doordhan strategy: how we trade for growth

**The goal is to grow the account** (Instagram now; YouTube Shorts once the channel exists). Everything else serves that.
We run it like a trading desk: form a strategy, execute it, read the results, refine. Every change is a bet with a target and a stop loss. One reel proves nothing, but we never keep building on a losing strategy (Akhilesh, 2026-09-25).

**Growth at any cost** means any effort, any idea, any format, any number of experiments. The one thing we never spend is the account itself. That rules out:
- breaking the hard rules in CLAUDE.md;
- breaking the platform rules in docs/platform-playbook.md;
- faking engagement (bought followers or views, engagement pods, follow/unfollow, bots).

Those get an account restricted or quietly demoted, and that is the one loss we can't trade our way back from.

## How we trade
1. **Every change is a bet**, written in registry/bets.json before the first reel carries it. Each bet has:
   - one lever;
   - one metric;
   - the baseline it opened at;
   - a target;
   - a stop;
   - how many reels it needs before we judge it, and the most we'll give it.
2. **We judge on rates, not luck.** The rates are skip rate, watched %, and sends, saves and likes per 1,000 plays, pooled over all the reels carrying the bet. Play counts are compared only at 72 hours. `pipeline/scoreboard.py` does the arithmetic and gives the verdict.
3. **Target hit: press it.** The lever becomes the default in the playbooks, and we make more reels in that vein, including follow-ups. Let winners run.
4. **Stop hit: cut it the same night.**
   - Undo the lever and write down why in docs/learnings.md.
   - No averaging down: a losing bet doesn't get more reels in the hope it turns.
   - A stop kills the trade, not necessarily the idea. Re-enter only with a different execution, under a new bet ID.
5. **Time stop.** If a bet reaches its maximum number of reels with neither target nor stop hit, close it as "no edge" and keep whichever option is simpler and cheaper.
6. **An execution miss is not a loss.** If a reel didn't actually carry the lever (for example, the hook text was dropped), take it out of the bet before judging.
7. **Position limits.**
   - At most 3 open bets, each on a different lever and judged on a different metric, so we know what caused what.
   - Every reel carries every bet marked "every reel".
   - "Watch" items are tracked but not traded until they can be separated from the open bets.
8. **Credits are our capital.** Every reel records what it cost, and the book tracks credits per 1,000 plays. The budgets in CLAUDE.md stand. When a winning bet needs more capital, the strategist asks for it with the numbers.
9. **Fix the funnel in order: stop, hold, share, follow.**
   - Stop: skip rate.
   - Hold: watched %.
   - Share: sends and saves.
   - Follow: new followers.

   The next bet goes on the weakest stage. There's no point perfecting the share line while 60% leave in the first 3 seconds.
10. **The account has its own stop.** Each campaign stage has targets and a strategy-level stop. When that stop hits, we don't tweak; we change strategy.

## The campaign
Stage 1 targets are live in the block below. Stages 2 and 3 are the plan after that, and the monthly review resets all of them. Every number is an opening proposal that Akhilesh can change.
- **Stage 1: Stop the scroll (26 Sep to 11 Oct).** Skip rate at or below 45%, watched at or above 45%, median plays at 72 h of 500 or more, one reel above 2,000 plays, 100 followers.
  - Strategy stop: after 10 reels, median plays still under 300.
- **Stage 2: Make it travel (12 Oct to 1 Nov).** Sends per 1,000 plays of 10 or more, one reel above 10,000 plays, 500 followers.
  - Likely levers: series and follow-ups on winners, formats built to be forwarded, Trial Reels.
- **Stage 3: Build the habit (Nov to Dec).** 2,000 followers by 31 Dec, viewers coming back for a recurring series, and YouTube Shorts live.

## The book and where we stand
<!-- scoreboard -->
_Updated 2026-09-25 23:45 IST by `scoreboard.py write`._

**Stage 1: Stop the scroll** (2026-09-26 to 2026-10-11): prove people stop for our reels and stay to the end

- skip rate %: now –, target 45 → not yet
- watched %: now –, target 45 → not yet
- median plays at 72 h: now –, target 500 → not yet
- best reel's plays: now –, target 2000 → not yet
- followers: now 12, target 100 → not yet
- strategy stop: 0/10 reels posted this stage; median plays at 72 h now –, must reach 300

| Bet | Lever | Judged on | Baseline | Now | Target | Stop | Reels (judged/carried) | Verdict |
|---|---|---|---|---|---|---|---|---|
| B1 Hook in frame one | Frame 1: the anchor looks into the lens, already saying the viewer's stake; the hook in 6 big words or fewer on screen; nothing (Namaskar, title, logo) before it; a cut or punch-in by 1 s; cover = frame 1 | skip rate % | 60.7 | – | 45 | 58 | 0/0 (judge at 3, max 6) | **WAITING** no reel with readings yet |
| B2 Tight 20-30 s | 20-30 s total; title montage 1.5 s or less and only after the hook; payoff by 20 s; the last line echoes the hook so a replay feels natural; no dead air | watched % | 26.3 | – | 45 | 32 | 0/0 (judge at 3, max 6) | **WAITING** no reel with readings yet |
| B3 A line worth sending | Every script lands one line a viewer would forward to a specific person (a number to remember, a jab at the system, an 'I told you so'); never ask for shares | sends per 1k plays | 2.6 | – | 8 | 2 | 0/0 (judge at 4, max 6) | **WAITING** no reel with readings yet |
| W1 Glam Sarika | Sarika in the glam wardrobe (formats/samachar.md) on every Samachar reel | skip rate % | 66.9 | – | – | – | 0/0 (judge at 3, max 6) | **WATCH** tracked; judged at the monthly review |
<!-- /scoreboard -->

## This week's plan
_Written by the strategist every Sunday. The morning session executes it: each story option says which bets it carries, and each script says how it carries them._

**Week of Sat 26 Sep (opening book, written 25 Sep)**
- **Every reel carries B1, B2 and B3:**
  - **B1, hook in frame one.** Sarika (or whoever leads) is in close-up, looking into the lens, and is already saying the viewer's stake in the first frame. The hook is on screen in 6 big words or fewer, using the headline strip. Nothing comes before it: no "Namaskar", no title, no logo. There's a cut or punch-in by 1 s. The cover is frame 1.
  - **B2, tight 20–30 s.** The title montage is 1.5 s at most and comes after the hook. The payoff lands by 20 s. The last line echoes the hook. No dead air.
  - **B3, a line worth sending.** One line a viewer would forward to a specific person: a number to remember, a jab at the system, an "I told you so". Never ask for shares.
- **Always on (hygiene, not bets):**
  - AI label on every post.
  - The full caption with keywords and exactly 5 hashtags.
  - Post between 7 and 9 pm IST.
  - The cover is frame 1.
  - Trial Reel whenever the option shows.
- **Volume: 5 reels a week, Mon to Fri.** That gives each bet its 3-reel sample inside one week. Up to 60 credits a reel.
- **Fix before judging (Akhilesh, one-time):**
  - Check Account Status.
  - Turn on the AI-generated profile label (already hard rule 3).

  An account that isn't recommendable makes every bet look like a loser.
- **Watching:**
  - W1: glam Sarika against the other formats.
  - The desk's score against real plays.

## Working rhythm
| When | Who | What |
|---|---|---|
| Mon–Sat 7:30 IST | Morning session (cloud) | Desk email. The top three lines are the scoreboard brief: where we stand and what today's reel carries. Then three stories, each tagged with the bets it serves. |
| Morning | Akhilesh | Picks a story (30 s). |
| Midday | Session, then Akhilesh | Script, with the bets it carries and how. Akhilesh approves (2 min). |
| Afternoon | Session, then Akhilesh | Final with QC notes. Akhilesh approves (2 min). |
| 7–9 pm IST | Akhilesh | Posts with the posting kit (5 min). |
| Nightly 21:30 IST | Strategist (cloud) | Records every reel's numbers and checks every target and stop, acting the same night. Pings the phone only on a stop, a target or a reel taking off. |
| Sunday 21:30 IST | Strategist | Weekly review email: the account, the book (each bet's result), what we learned, next week's plan, and yes/no decisions. Akhilesh replies in that session. |
| First Sunday of the month | Strategist | Campaign review: stage targets, whether the desk's scores predict plays, the strategy-level stop, pivots. |
| Weekly | Akhilesh | Instagram → Settings → Account Status (1 min; only the app shows it). |

**The strategist decides alone:**
- opening, pressing, stopping and closing bets within the hard rules, the budgets, and the existing formats and looks;
- rewriting the playbooks and this week's plan;
- the story grading weights and the posting plan.

**It asks Akhilesh first about:**
- anything touching the hard rules;
- spending over budget;
- a change to Sarika's look;
- a brand-new format;
- changing a campaign target.

## Decision log
- 2026-09-25:
  - Book opened: B1 hook in frame one, B2 tight 20–30 s, B3 a line worth sending, plus W1 (glam Sarika) on watch.
  - Baselines come from E1 and E2: skip rate 60.7%, watched 26.3%, 2.6 sends per 1,000 plays.
  - Stage 1 campaign set.
