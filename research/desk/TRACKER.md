# Story tracker

_Written 2026-10-14 by `pipeline/story_tracker.py md`. Data: registry/story_tracker.json._

Every story the desk has sent stays here until it leaves the news cycle (COLD on two checks running, or past its window). Each morning `story_tracker.py check` measures them all again.

Label history reads oldest to newest: H hot, R rising, F flat, C cold.

| Story | Status | Now | Direction | Day | History | News today/week | YouTube views this week | Best views/hr | Desk score | Window |
|---|---|---|---|---|---|---|---|---|---|---|
| Jio Platforms IPO (`jio-ipo`) | active | FLAT | fading | 7 | H R F F F R F | 34/100 | 207,073 | 1,199 | 7 | 2026-10-31 |
| International ETFs trading far above NAV (NSE warning) (`intl-etf-premium`) | active | COLD | rising | 7 | C C C C C C C | 0/0 | 419,323 | 2,026 | 6 | 2026-10-22 |
| TCS: profit +15%, share -35% in 2026 (`tcs-q2-profit-share`) | active | FLAT | steady | 6 | H F F F F | 7/45 | 78,771 | 153 | 8 | 2026-10-14 |
| SC orders panel on pharma freebies to doctors (`pharma-freebies-sc`) | active | COLD | steady | 6 | C C C C C | 0/1 | 50,160 | 332 | 6 | 2026-10-23 |
| UPI merchant fee (0.4% MDR) may be deferred to 1 Jan (`upi-mdr-deferral`) | active | HOT | rising | 5 | H F H H | 31/43 | 122,054 | 3,396 | 6 | 2026-10-16 |
| Inox Clean: revenue 43X, debt 45X, IPO on hold (`inox-clean-ipo`) | active | COLD | fading | 5 | C C C C | 0/0 | 77,242 | 455 | 6 | 2026-10-24 |
| Musk calls Ambani 'Prime Minister Ambani' over Starlink (`musk-ambani-starlink`) | active | HOT | rising | 4 | H H H | 8/28 | 8,972,151 | 79,404 | 6 | 2026-10-21 |
| SC on hospital drug markups: Rs 2,700 drug sold at Rs 27,000 (`hospital-drug-markup-sc`) | active | COLD | steady | 4 | C C C | 0/0 | 6,416 | 256 | 6 | 2026-10-25 |
| Gauahar Khan's Versova duplex: 88% in 12 years (`gauahar-khan-flat`) | active | COLD | steady | 3 | C C | 0/0 | 2,302,454 | 18,075 | 6 | 2026-10-26 |
| Kohli and Anushka's ₹44 crore: three Versova flats, ready 2031 (`kohli-anushka-versova-flats`) | active | COLD | new | 2 | C | 0/0 | 232,610 | 1,519 | 8 | 2026-10-20 |
| Rupee near ₹97: RBI hike, then four emergency measures (`rbi-rupee-rescue`) | active | HOT | new | 2 | H | 2/6 | 174,842 | 3,457 | 7 | 2026-10-20 |
| Zoho freezes pay rises over AI and server costs (`zoho-pay-freeze`) | active | - | new | 1 |  | -/- | 0 | 0 | 9 | 2026-10-20 |
| Sensex +1,109 partly on FM's LTCG remark (`ltcg-remark-rally`) | active | - | new | 1 |  | -/- | 0 | 0 | 8 | 2026-10-20 |
| Ramayana producer's Prime Focus searched by Income Tax (`prime-focus-ramayana`) | retired: COLD on 2 checks running | COLD | steady | 7 | H H H H C C | 0/0 | 1,056,196 | 7,548 | 8 | 2026-11-10 |
| EPF wage ceiling raised to ₹25,000 (`epf-wage-ceiling`) | retired: COLD on 2 checks running | COLD | fading | 7 | F F C C | 0/7 | 20,051 | 152 | - | - |
| Snapdeal (AceVector) after listing (`snapdeal-acevector`) | retired (E8): COLD on 2 checks running | COLD | steady | 7 | C C | 0/1 | 100,780 | 770 | - | - |
| Nana Patekar dies; the Rs 1.5 crore car he gave up for farmers (`nana-patekar`) | retired (E10): past its window | HOT | rising | 7 | R H H H | 100/100 | 27,305,534 | 110,559 | 7 | 2026-10-11 |
| Sensex -1,045 on 8 Oct: ₹10.23 lakh crore wiped off (`market-crash-oct8`) | retired: past its window | HOT | rising | 6 | H H C H | 9/17 | 3,239,882 | 14,656 | 9 | 2026-10-12 |
| US suspends TCS, Infosys, Wipro from green-card PERM; IT shares rise (`us-perm-indian-it`) | retired: COLD on 2 checks running | COLD | steady | 4 | H C C | 0/1 | 1,195,114 | 3,721 | 8 | 2026-10-17 |
| HDFC Bank's new CEO ₹35.9 cr vs SBI chairman ₹43 lakh (`hdfc-ceo-pay-sbi`) | retired: COLD on 2 checks running | COLD | fading | 3 | C C | 0/1 | 8,051 | 55 | 9 | 2026-10-27 |

## Latest notes
- **Jio Platforms IPO:** 2026-10-11: 11 Oct: no RHP yet; documents expected week of 12 Oct; Musk-Ambani row (story musk-ambani-starlink) is its newest turn
- **Jio Platforms IPO:** 2026-10-14: 13 Oct: >$20 bn bids reported (ET/Mint headlines); band 1,065-1,119 reported; no RHP yet
- **International ETFs trading far above NAV (NSE warning):** First sent 8 Oct (deep lane). NSE caution 7 Oct; BSE 25 Sep.
- **TCS: profit +15%, share -35% in 2026:** First sent 9 Oct. Q2 profit ₹13,884 cr; +4,258 staff; AI $3.1 bn.
- **SC orders panel on pharma freebies to doctors:** First sent 9 Oct (deep lane). Order 8 Oct; panel reports in ~2 months; hearing 29 Jan 2027.
- **UPI merchant fee (0.4% MDR) may be deferred to 1 Jan:** 2026-10-13: 13 Oct: no decision yet, 15 Oct stands; IIT-Bombay study says 0.08% (PTI, 11 Oct)
- **UPI merchant fee (0.4% MDR) may be deferred to 1 Jan:** 2026-10-14: 13 Oct: NPCI deferred MDR to 'immediately after Diwali', date to be notified; rates unchanged
- **Inox Clean: revenue 43X, debt 45X, IPO on hold:** First sent 10 Oct (via The Ken, 9 Oct). SEBI observations in abeyance.
- **Musk calls Ambani 'Prime Minister Ambani' over Starlink:** 2026-10-12: Musk promises affordable Starlink (Sat 10 Oct); Jio targets $106 bn
- **Musk calls Ambani 'Prime Minister Ambani' over Starlink:** 2026-10-14: 13 Oct: RSS affiliate urges Starlink licence denial (Reuters)
- **SC on hospital drug markups: Rs 2,700 drug sold at Rs 27,000:** First sent 11 Oct. Hearings 22 and 29 Sep; 16% uniform margin suggested; Centre's reply due at the 12 Oct hearing.
- **Gauahar Khan's Versova duplex: 88% in 12 years:** creator-format option; desk 12 Oct
- **Kohli and Anushka's ₹44 crore: three Versova flats, ready 2031:** First sent 13 Oct. Godrej Skyshore, 3 flats ₹44 cr, stamp duty ~₹2.49 cr, possession 30 Jun 2031.
- **Rupee near ₹97: RBI hike, then four emergency measures:** First sent 13 Oct. Repo 5.50% (7 Oct); ₹96.73 → ₹95.76 on 12 Oct; 99% daily CRR from 16 Oct.
- **Zoho freezes pay rises over AI and server costs:** First sent 14 Oct. Vembu X post 13 Oct: no usual pay increase, server prices 4x, headcount flat 18 months, 'pray for us'.
- **Sensex +1,109 partly on FM's LTCG remark:** First sent 14 Oct. FM: debate healthy, 'not the best time to say what I will consider'; Sensex +1,109 to 73,033.78 on 13 Oct.
