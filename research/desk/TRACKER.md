# Story tracker

_Written 2026-10-19 by `pipeline/story_tracker.py md`. Data: registry/story_tracker.json._

Every story the desk has sent stays here until it leaves the news cycle (COLD on two checks running, or past its window). Each morning `story_tracker.py check` measures them all again.

Label history reads oldest to newest: H hot, R rising, F flat, C cold.

| Story | Status | Now | Direction | Day | History | News today/week | YouTube views this week | Best views/hr | Desk score | Window |
|---|---|---|---|---|---|---|---|---|---|---|
| Jio Platforms IPO (`jio-ipo`) | active | HOT | rising | 12 | R F R H H H H | 39/100 | 970,421 | 9,854 | 8 | 2026-10-31 |
| International ETFs trading far above NAV (NSE warning) (`intl-etf-premium`) | active | COLD | steady | 12 | C C C C C C C | 0/0 | 71,888 | 767 | 6 | 2026-10-22 |
| SC orders panel on pharma freebies to doctors (`pharma-freebies-sc`) | active | HOT | steady | 11 | C C C C H H H | 0/0 | 453,802 | 3,548 | 6 | 2026-10-23 |
| Inox Clean: revenue 43X, debt 45X, IPO on hold (`inox-clean-ipo`) | active | HOT | rising | 10 | C C C C H H H | 0/2 | 430,677 | 4,921 | 6 | 2026-10-24 |
| Musk calls Ambani 'Prime Minister Ambani' over Starlink (`musk-ambani-starlink`) | active | HOT | rising | 9 | H H F F F H H | 2/13 | 5,180,463 | 43,373 | 8 | 2026-10-21 |
| SC on hospital drug markups: Rs 2,700 drug sold at Rs 27,000 (`hospital-drug-markup-sc`) | active | COLD | steady | 9 | C C C C C C C | 0/0 | 34,991 | 109 | 6 | 2026-10-25 |
| Gauahar Khan's Versova duplex: 88% in 12 years (`gauahar-khan-flat`) | active | COLD | rising | 8 | C C C C C C C | 0/0 | 34,059 | 260 | 6 | 2026-10-26 |
| Sensex +1,109 partly on FM's LTCG remark (`ltcg-remark-rally`) | active | COLD | fading | 6 | H H H H C | 0/1 | 2,090,505 | 5,902 | 8 | 2026-10-20 |
| Gold ₹3,600 cheaper in four sessions on a stronger rupee (`gold-slide-rupee`) | active | FLAT | fading | 5 | H R R F | 29/87 | 73,232 | 2,024 | 8 | 2026-10-19 |
| Airtel Money lists in London at $7 bn (via The Ken) (`airtel-money-london`) | active | FLAT | steady | 5 | H H F F | 1/63 | 1,477,649 | 9,542 | 6 | 2026-10-29 |
| Yes Bank -14.5% after SC voids AT-1 write-off (`yes-bank-at1-sc`) | active | FLAT | fading | 4 | R H F | 9/15 | 303,946 | 2,696 | 8 | 2026-10-20 |
| Mutual funds halt new gold FoF SIPs and bulk gold ETF buys (`gold-fund-halt`) | active | HOT | rising | 4 | R H H | 7/80 | 800,275 | 9,752 | 8 | 2026-11-08 |
| Zetwerk IPO: 54% of Q1 revenue from metal sales (`zetwerk-ipo-metals`) | active | FLAT | fading | 4 | F F F | 2/51 | 223,812 | 1,554 | 7 | 2026-10-23 |
| IDBI Bank sold to Fairfax at ₹81 vs ₹90 market (`idbi-fairfax-sale`) | active | HOT | rising | 3 | H H | 0/33 | 1,608,736 | 14,118 | 9 | 2026-10-24 |
| Insurance mis-selling complaints +14%; IRDAI crackdown may slip (via The Ken) (`insurance-misselling-ken`) | active | COLD | rising | 3 | C C | 0/4 | 1,559,056 | 9,728 | 6 | 2026-10-31 |
| Green-card freeze 'bloodbath' reels, then Indian IT's best week since 2008 (`it-rally-green-card`) | active | COLD | new | 2 | C | 0/2 | 250,430 | 1,133 | 9 | to about Wed 21 Oct |
| Expired food allegedly back on sale: FIR names Reliance, Blinkit directors (`expired-food-reliance-blinkit`) | active | COLD | new | 2 | C | 0/0 | 22,175 | 276 | 8 | to about Tue 20 Oct |
| Groww's F&O share of revenue falls to 45%; turns to IPOs and wealth (via The Arc) (`groww-derivatives-arc`) | active | COLD | new | 2 | C | 0/0 | 82,529 | 279 | 6 | to about Fri 23 Oct |
| Ramayana producer's Prime Focus searched by Income Tax (`prime-focus-ramayana`) | retired: COLD on 2 checks running | COLD | steady | 12 | H H H H C C | 0/0 | 1,056,196 | 7,548 | 8 | 2026-11-10 |
| EPF wage ceiling raised to ₹25,000 (`epf-wage-ceiling`) | retired: COLD on 2 checks running | COLD | fading | 12 | F F C C | 0/7 | 20,051 | 152 | - | - |
| Snapdeal (AceVector) after listing (`snapdeal-acevector`) | retired (E8): COLD on 2 checks running | COLD | steady | 12 | C C | 0/1 | 100,780 | 770 | - | - |
| Nana Patekar dies; the Rs 1.5 crore car he gave up for farmers (`nana-patekar`) | retired (E10): past its window | HOT | rising | 12 | R H H H | 100/100 | 27,305,534 | 110,559 | 7 | 2026-10-11 |
| Sensex -1,045 on 8 Oct: ₹10.23 lakh crore wiped off (`market-crash-oct8`) | retired: past its window | HOT | rising | 11 | H H C H | 9/17 | 3,239,882 | 14,656 | 9 | 2026-10-12 |
| TCS: profit +15%, share -35% in 2026 (`tcs-q2-profit-share`) | retired: past its window | HOT | rising | 11 | H F F F F H | 7/48 | 464,093 | 10,346 | 8 | 2026-10-14 |
| UPI merchant fee (0.4% MDR) may be deferred to 1 Jan (`upi-mdr-deferral`) | retired: past its window | HOT | rising | 10 | H F H H H H H | 2/41 | 910,815 | 4,784 | 6 | 2026-10-16 |
| US suspends TCS, Infosys, Wipro from green-card PERM; IT shares rise (`us-perm-indian-it`) | retired: COLD on 2 checks running | COLD | steady | 9 | H C C | 0/1 | 1,195,114 | 3,721 | 8 | 2026-10-17 |
| HDFC Bank's new CEO ₹35.9 cr vs SBI chairman ₹43 lakh (`hdfc-ceo-pay-sbi`) | retired: COLD on 2 checks running | COLD | fading | 8 | C C | 0/1 | 8,051 | 55 | 9 | 2026-10-27 |
| Kohli and Anushka's ₹44 crore: three Versova flats, ready 2031 (`kohli-anushka-versova-flats`) | retired: COLD on 2 checks running | COLD | fading | 7 | C C | 0/0 | 598 | 25 | 8 | 2026-10-20 |
| Rupee near ₹97: RBI hike, then four emergency measures (`rbi-rupee-rescue`) | retired: COLD on 2 checks running | COLD | rising | 7 | H H H C C | 0/9 | 1,516,191 | 14,931 | 7 | 2026-10-20 |
| Zoho freezes pay rises over AI and server costs (`zoho-pay-freeze`) | retired: COLD on 2 checks running | COLD | rising | 6 | H C C | 0/2 | 287,736 | 1,847 | 9 | 2026-10-20 |
| ED raids WhatsApp 'Multibagger' pump-and-dump (RM Drip, R&B Denims) (`ed-whatsapp-multibagger`) | retired: COLD on 2 checks running | COLD | rising | 3 | C C | 0/3 | 230 | 5 | 7 | 2026-10-22 |

## Latest notes
- **Jio Platforms IPO:** 2026-10-17: 17 Oct: GMP ₹206 (15 Oct, Outlook Money); anchor Mon 19; opens Wed 21
- **Jio Platforms IPO:** 2026-10-19: anchor book 19 Oct; GMP ₹140→₹249 (2–18 Oct); proceeds mainly repay Jio debt
- **International ETFs trading far above NAV (NSE warning):** First sent 8 Oct (deep lane). NSE caution 7 Oct; BSE 25 Sep.
- **SC orders panel on pharma freebies to doctors:** First sent 9 Oct (deep lane). Order 8 Oct; panel reports in ~2 months; hearing 29 Jan 2027.
- **Inox Clean: revenue 43X, debt 45X, IPO on hold:** First sent 10 Oct (via The Ken, 9 Oct). SEBI observations in abeyance.
- **Musk calls Ambani 'Prime Minister Ambani' over Starlink:** 2026-10-18: crowded; Reliance responded 16 Oct
- **Musk calls Ambani 'Prime Minister Ambani' over Starlink:** 2026-10-18: picked 18 Oct: link with Jio IPO
- **SC on hospital drug markups: Rs 2,700 drug sold at Rs 27,000:** First sent 11 Oct. Hearings 22 and 29 Sep; 16% uniform margin suggested; Centre's reply due at the 12 Oct hearing.
- **SC on hospital drug markups: Rs 2,700 drug sold at Rs 27,000:** 2026-10-19: NPPA caps trade margins at 30% on 137 cancer drugs from 9 Nov; up to 70% cheaper (Moneylife)
- **Gauahar Khan's Versova duplex: 88% in 12 years:** creator-format option; desk 12 Oct
- **Sensex +1,109 partly on FM's LTCG remark:** First sent 14 Oct. FM: debate healthy, 'not the best time to say what I will consider'; Sensex +1,109 to 73,033.78 on 13 Oct.
- **Gold ₹3,600 cheaper in four sessions on a stronger rupee:** First sent 15 Oct. ₹1,50,800/10 g on 14 Oct (−₹1,800; −₹3,600 since 9 Oct); rupee 95.17, 4th gain.
- **Airtel Money lists in London at $7 bn (via The Ken):** First sent 15 Oct. £1.96, £5.3 bn; 270m shares; flat debut 9 Oct; admission 14 Oct.
- **Yes Bank -14.5% after SC voids AT-1 write-off:** 2026-10-17: 17 Oct: results today; CNBC-TV18 headline ₹5,400 cr earnings hit
- **Yes Bank -14.5% after SC voids AT-1 write-off:** 2026-10-19: Q2: ₹1,080 cr profit reported vs ₹5,217 cr pro forma loss if AT-1 ruling booked
- **Zetwerk IPO: 54% of Q1 revenue from metal sales:** via The Ken
- **IDBI Bank sold to Fairfax at ₹81 vs ₹90 market:** First sent 17 Oct. ₹52,878 cr for 60.72% (govt 30.48, LIC 30.24); ₹81 vs ₹90.40 close; −7% on 15 Oct
- **Insurance mis-selling complaints +14%; IRDAI crackdown may slip (via The Ken):** First sent 17 Oct. Comments due 25 Oct
