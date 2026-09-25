# Playbook: news desk

_This is the path that has worked so far. Change it whenever you find a better way, and note what you changed in registry/episodes.md._

Goal: three story options Akhilesh can pick from in 30 seconds.

1. Get today's date from the system clock (do not trust injected dates).
2. Research the last 48 hours of Indian finance news: markets, IPOs and listings, SEBI and RBI moves, tax, gold, fuel prices, big company events, viral money stories. Use several searches; read headlines from Business Standard, Mint, Economic Times, Moneycontrol, CNBC-TV18, and what people are sharing about them.
3. Set aside topics Akhilesh has rested (see CLAUDE.md), topics already made (registry/episodes.md) unless there is a genuinely new turn, and anything that would need a buy/sell call. Prefer the last 48 hours unless a story is still trending. On Mondays, cover the weekend too.
4. Score each candidate on: interesting (would the headline make you click?), relevance to working professionals in their late 20s–30s, one clear idea, and a visual/format fit.
5. Send three options in this shape:

   **1. [Headline in plain English]**
   - Why it's interesting: one line (the clickbait angle)
   - Format: a template from formats/, or a new format pitched in one line
   - Hooks: A) ... B) ... C) ... (each one plain sentence, viewer's stake)
   - Fact box: 2–4 facts with source links (open each link and confirm the number is on the page; drop a fact rather than guess)

   Give the three options different shapes where the news allows (e.g. one market/listing story, one policy or tax change, one viral money story), so the pick is a real choice.
6. End with: "Reply with a number and a hook letter, e.g. 2B."
7. The cloud routine (routines/newsdesk-routine-prompt.md) runs this Mon–Sat at 7:30 IST and emails the result. It never spends credits and never commits to the repo.
