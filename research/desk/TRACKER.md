# Story tracker

_Written 2026-11-04 by `pipeline/story_tracker.py md`. Data: registry/story_tracker.json._

Every story the desk has sent stays here until it leaves the news cycle (COLD on two checks running, or past its window). Each morning `story_tracker.py check` measures them all again.

Label history reads oldest to newest: H hot, R rising, F flat, C cold.

| Story | Status | Now | Direction | Day | History | News today/week | YouTube views this week | Best views/hr | Desk score | Window |
|---|---|---|---|---|---|---|---|---|---|---|
| Mutual funds halt new gold FoF SIPs and bulk gold ETF buys (`gold-fund-halt`) | active | FLAT | rising | 20 | R F H F F F F | 13/39 | 194,361 | 684 | 9 | 2026-11-08 |
| Groww's F&O share of revenue falls to 45%; turns to IPOs and wealth (via The Arc) (`groww-derivatives-arc`) | active | HOT | rising | 18 | C C C C C C H | 0/0 | 262,464 | 1,536 | 7 | to about Fri 23 Oct |
| Silver -46% from January record (₹3,84,632 → ₹2,08,380/kg) before Dhanteras (`silver-crash-46`) | active | HOT | rising | 15 | H C H H H H H | 3/- | 1,467,684 | 5,891 | 7 | 2026-11-08 |
| NSE unlisted buyers below IPO price (The Ken) (`nse-unlisted-regret-ken`) | active | FLAT | steady | 12 | H H H H C F F | 8/30 | 1,126,057 | 7,252 | 7 | 2026-11-07 |
| Jio's prepaid (77% of revenue) sold only via Reliance Retail (via The Ken) (`jio-reliance-retail-ken`) | active | COLD | fading | 11 | H H C H C C C | 0/- | 258,869 | 1,053 | 8 | 2026-11-04 |
| Gold ₹38,000 below January peak, ₹5,560/10g down in 3 days, before Dhanteras (`gold-dhanteras-fall`) | active | HOT | steady | 10 | H H H H H H H | -/1 | 1,798,977 | 8,956 | 9 | 2026-11-06 |
| Jewellery makers' IPO wave: money goes to gold and debt (via The Ken) (`jewellery-ipo-ken`) | active | COLD | steady | 8 | C C C C C C C | 1/1 | 201,432 | 737 | 5 | 2026-11-06 |
| Anthropic S-1: $16.3 bn H1 revenue, $80.7 bn loss ($72.4 bn paper charge) (`anthropic-s1`) | active | HOT | steady | 7 | H H H H H H | 57/100 | 1,404,937 | 5,242 | 9 | 2026-11-20 |
| LTCG tax-cut debate: ₹1.29 lakh crore a year; The Ken says don't cut (`ltcg-cut-debate`) | active | HOT | rising | 7 | H F F F R H | 49/100 | 285,609 | 4,370 | 8 | 2026-11-12 |
| Equitas SFB: record profit, CEO quits over daughter's NBFC, 20% lower circuit (`equitas-ceo-exit`) | active | COLD | fading | 6 | R F F F C | -/- | 104,369 | 464 | 8 | 2026-11-06 |
| 773 government sites still serving eMudhra's revoked certificates (via The Ken) (`emudhra-gov-sites`) | active | COLD | rising | 6 | C C C C C | 0/0 | 5,672 | 43 | 5 | 2026-11-13 |
| Ola Electric rights issue: founder pledges shares to buy in, SoftBank sells (`ola-rights-pledge`) | active | COLD | steady | 5 | C C C C | 0/5 | 84,551 | 330 | 7 | 2026-11-07 |
| IDBI sale: Fairfax bid opened, then ₹94.42 floor discarded; sold at ₹81 (via BusinessWorld) (`idbi-note-reserve`) | active | HOT | rising | 4 | C C H | 1/5 | 327,535 | 4,953 | 7 | 2026-11-08 |
| Binance $6.3 bn hack: users don't pay; WazirX users did (`binance-hack-wazirx`) | active | RISING | fading | 3 | H R | 100/100 | 6,284,926 | 26,288 | 9 | 2026-11-07 |
| SEBI order on EKI Energy: ₹197 cr revenue early, ₹88 lakh fines (`eki-sebi-order`) | active | COLD | steady | 3 | C C | 0/1 | 184,956 | 551 | 6 | 2026-11-08 |
| Reliance +12% record day, $19 bn added; Jio stake at 80% discount (`reliance-record-day`) | active | HOT | new | 2 | H | 2/16 | 434,146 | 3,743 | 9 | 2026-11-05 |
| Axis MF front-running: Dubai AnyDesk trades, brokers fined ₹10 lakh each (`axis-mf-frontrun`) | active | - | new | 1 |  | -/- | 0 | 0 | 7 | 2026-11-17 |
| Jio Platforms IPO (`jio-ipo`) | retired: past its window | FLAT | rising | 28 | H H H H H F F | 23/100 | 2,342,949 | 4,935 | 8 | 2026-11-02 |
| Ramayana producer's Prime Focus searched by Income Tax (`prime-focus-ramayana`) | retired: COLD on 2 checks running | COLD | steady | 28 | H H H H C C | 0/0 | 1,056,196 | 7,548 | 8 | 2026-11-10 |
| International ETFs trading far above NAV (NSE warning) (`intl-etf-premium`) | retired: past its window | COLD | fading | 28 | C C C H H H C | 0/- | 438,146 | 4,086 | 6 | 2026-10-22 |
| EPF wage ceiling raised to ₹25,000 (`epf-wage-ceiling`) | retired: COLD on 2 checks running | COLD | fading | 28 | F F C C | 0/7 | 20,051 | 152 | - | - |
| Snapdeal (AceVector) after listing (`snapdeal-acevector`) | retired (E8): COLD on 2 checks running | COLD | steady | 28 | C C | 0/1 | 100,780 | 770 | - | - |
| Nana Patekar dies; the Rs 1.5 crore car he gave up for farmers (`nana-patekar`) | retired (E10): past its window | HOT | rising | 28 | R H H H | 100/100 | 27,305,534 | 110,559 | 7 | 2026-10-11 |
| Sensex -1,045 on 8 Oct: ₹10.23 lakh crore wiped off (`market-crash-oct8`) | retired: past its window | HOT | rising | 27 | H H C H | 9/17 | 3,239,882 | 14,656 | 9 | 2026-10-12 |
| TCS: profit +15%, share -35% in 2026 (`tcs-q2-profit-share`) | retired: past its window | HOT | rising | 27 | H F F F F H | 7/48 | 464,093 | 10,346 | 8 | 2026-10-14 |
| SC orders panel on pharma freebies to doctors (`pharma-freebies-sc`) | retired: past its window | COLD | fading | 27 | H H H C C C C | 0/0 | 445,730 | 1,054 | 6 | 2026-10-23 |
| UPI merchant fee (0.4% MDR) may be deferred to 1 Jan (`upi-mdr-deferral`) | retired: past its window | HOT | rising | 26 | H F H H H H H | 2/41 | 910,815 | 4,784 | 6 | 2026-10-16 |
| Inox Clean: revenue 43X, debt 45X, IPO on hold (`inox-clean-ipo`) | retired: past its window | COLD | fading | 26 | H C C C C C C | 0/0 | 29,731 | 131 | 6 | 2026-10-24 |
| Musk calls Ambani 'Prime Minister Ambani' over Starlink (`musk-ambani-starlink`) | retired: past its window | FLAT | fading | 25 | F F H H H H F | 1/10 | 4,347,306 | 14,666 | 8 | 2026-10-21 |
| US suspends TCS, Infosys, Wipro from green-card PERM; IT shares rise (`us-perm-indian-it`) | retired: COLD on 2 checks running | COLD | steady | 25 | H C C | 0/1 | 1,195,114 | 3,721 | 8 | 2026-10-17 |
| SC on hospital drug markups: Rs 2,700 drug sold at Rs 27,000 (`hospital-drug-markup-sc`) | retired: past its window | HOT | rising | 25 | H C C C C C H | 0/0 | 168,581 | 6,896 | 6 | 2026-10-25 |
| HDFC Bank's new CEO ₹35.9 cr vs SBI chairman ₹43 lakh (`hdfc-ceo-pay-sbi`) | retired: COLD on 2 checks running | COLD | fading | 24 | C C | 0/1 | 8,051 | 55 | 9 | 2026-10-27 |
| Gauahar Khan's Versova duplex: 88% in 12 years (`gauahar-khan-flat`) | retired: past its window | COLD | fading | 24 | C C H C C C C | 0/0 | 0 | 0 | 6 | 2026-10-26 |
| Kohli and Anushka's ₹44 crore: three Versova flats, ready 2031 (`kohli-anushka-versova-flats`) | retired: COLD on 2 checks running | COLD | fading | 23 | C C | 0/0 | 598 | 25 | 8 | 2026-10-20 |
| Rupee near ₹97: RBI hike, then four emergency measures (`rbi-rupee-rescue`) | retired: COLD on 2 checks running | COLD | rising | 23 | H H H C C | 0/9 | 1,516,191 | 14,931 | 7 | 2026-10-20 |
| Zoho freezes pay rises over AI and server costs (`zoho-pay-freeze`) | retired: COLD on 2 checks running | COLD | rising | 22 | H C C | 0/2 | 287,736 | 1,847 | 9 | 2026-10-20 |
| Sensex +1,109 partly on FM's LTCG remark (`ltcg-remark-rally`) | retired: COLD on 2 checks running | COLD | fading | 22 | H H H H C C | 0/1 | 1,266,936 | 3,079 | 8 | 2026-10-20 |
| Gold ₹3,600 cheaper in four sessions on a stronger rupee (`gold-slide-rupee`) | retired: past its window | RISING | rising | 21 | H R R F R | 31/85 | 175,924 | 2,637 | 8 | 2026-10-19 |
| Airtel Money lists in London at $7 bn (via The Ken) (`airtel-money-london`) | retired: past its window | FLAT | steady | 21 | F F F R F F F | 6/40 | 222,173 | 1,254 | 6 | 2026-10-29 |
| Yes Bank -14.5% after SC voids AT-1 write-off (`yes-bank-at1-sc`) | retired: past its window | FLAT | steady | 20 | R H F F F | 2/36 | 452,328 | 1,618 | 8 | 2026-10-20 |
| Zetwerk IPO: 54% of Q1 revenue from metal sales (`zetwerk-ipo-metals`) | retired: past its window | FLAT | rising | 20 | F F R F F C F | 7/31 | 159,682 | 735 | 7 | 2026-10-23 |
| IDBI Bank sold to Fairfax at ₹81 vs ₹90 market (`idbi-fairfax-sale`) | retired: COLD on 2 checks running | COLD | fading | 19 | H H H F H C C | 1/4 | 255,768 | 1,751 | 9 | 2026-10-24 |
| ED raids WhatsApp 'Multibagger' pump-and-dump (RM Drip, R&B Denims) (`ed-whatsapp-multibagger`) | retired: COLD on 2 checks running | COLD | rising | 19 | C C | 0/3 | 230 | 5 | 7 | 2026-10-22 |
| Insurance mis-selling complaints +14%; IRDAI crackdown may slip (via The Ken) (`insurance-misselling-ken`) | retired: past its window | COLD | steady | 19 | C C H C C C C | 0/2 | 36,261 | 278 | 6 | 2026-10-31 |
| Green-card freeze 'bloodbath' reels, then Indian IT's best week since 2008 (`it-rally-green-card`) | retired: COLD on 2 checks running | COLD | steady | 18 | C H C C | 1/3 | 38,873 | 1,467 | 9 | to about Wed 21 Oct |
| Expired food allegedly back on sale: FIR names Reliance, Blinkit directors (`expired-food-reliance-blinkit`) | retired: COLD on 2 checks running | COLD | rising | 18 | C C | 0/0 | 27,744 | 247 | 8 | to about Tue 20 Oct |
| Axis Bank: profit +38%, shares -5% (base effect of last year's ₹1,231 cr provision) (`axis-bank-q2-fall`) | retired: past its window | RISING | rising | 16 | R R R R | 38/66 | 300,690 | 1,158 | 8 | 2026-10-23 |
| Air India FY26 loss ₹22,238 cr (~₹61 cr a day); SIA as saviour (via The Ken) (`air-india-loss-ken`) | retired: past its window | COLD | rising | 16 | C C C H H C C | 0/0 | 827,897 | 2,207 | 6 | 2026-11-02 |
| Urban Company loss triples on InstaHelp: ₹114 booking, ₹279 loss (via The Morning Context) (`urban-company-instahelp`) | retired: past its window | COLD | steady | 15 | C C C C H C C | 0/0 | 113,063 | 1,695 | 7 | 2026-11-03 |
| eMudhra -20% lower circuit after its certificate keys turned out to be tiny numbers (one was 4) (`emudhra-key-4`) | retired: past its window | FLAT | rising | 14 | H H F F F F | 0/12 | 191,204 | 552 | 9 | 2026-10-27 |
| Oil at $112: shares, gold and silver fell the same day (`oil-slide-everything`) | retired: past its window | HOT | rising | 13 | H H H H H C H | 0/3 | 1,107,504 | 8,878 | 8 | 2026-10-29 |
| SEBI final order: Avadhut Sathe ₹546 cr refund (`avadhut-sathe-refund`) | retired: past its window | HOT | rising | 12 | R F H H H F H | 1/20 | 526,055 | 3,209 | 6 | 2026-10-30 |
| Swiggy record low, less than half its IPO price; Instamart loss ₹895 cr (`swiggy-record-low`) | retired: past its window | FLAT | steady | 11 | F F F F | 0/32 | 170,029 | 627 | 9 | 2026-10-28 |
| RBI Governor: upper-layer CICs like Tata Sons must list (`tata-sons-listing`) | retired: COLD on 2 checks running | COLD | steady | 11 | C C | 0/2 | 135,201 | 1,538 | 8 | 2026-11-08 |
| HDFC Bank's first outside CEO starts; share ~30% down in a year (via The Morning Context) (`hdfc-bank-bagchi`) | retired: past its window | FLAT | rising | 9 | F F F F F F F | 5/19 | 64,397 | 517 | 8 | 2026-11-03 |
| SEBI makes direct mutual fund plans the default on AMC apps from 1 Nov (`sebi-direct-default`) | retired: past its window | COLD | steady | 5 | C C | 0/0 | 28,685 | 213 | 7 | 2026-11-01 |

## Latest notes
- **Mutual funds halt new gold FoF SIPs and bulk gold ETF buys:** 2026-10-23: 23 Oct: The Core: eighth rupee-defence step, 2013 parallel
- **Mutual funds halt new gold FoF SIPs and bulk gold ETF buys:** 2026-10-28: 28 Oct: digital gold +83% y/y to Rs 2,590 cr (Sep) despite SEBI warning; FoF still shut
- **Groww's F&O share of revenue falls to 45%; turns to IPOs and wealth (via The Arc):** 2026-10-22: 22 Oct: The Ken 'hostage to options'; Groww PAT ₹725 cr, F&O 44.8% of revenue; SEBI FY26 87.7% lose
- **Silver -46% from January record (₹3,84,632 → ₹2,08,380/kg) before Dhanteras:** 2026-10-22: 22 Oct: no new turn; still HOT on YouTube
- **Silver -46% from January record (₹3,84,632 → ₹2,08,380/kg) before Dhanteras:** 2026-11-01: 1 Nov: MCX silver -57% from Jan peak, gold -23%; Dhanteras Fri 6 Nov
- **NSE unlisted buyers below IPO price (The Ken):** via The Ken 23 Oct
- **Jio's prepaid (77% of revenue) sold only via Reliance Retail (via The Ken):** The Ken 22 Oct; RHP figures via Fortune India 15 Oct
- **Jio's prepaid (77% of revenue) sold only via Reliance Retail (via The Ken):** 2026-10-26: carried for Wed listing
- **Gold ₹38,000 below January peak, ₹5,560/10g down in 3 days, before Dhanteras:** 2026-11-03: 3 Nov: Dhanteras-to-Dhanteras IBJA: +175% since 2022, +6.3% since 2025
- **Gold ₹38,000 below January peak, ₹5,560/10g down in 3 days, before Dhanteras:** 2026-11-04: 4 Nov: new turn, WGC Q3: -29% tonnes, +3% rupees; pick
- **Jewellery makers' IPO wave: money goes to gold and debt (via The Ken):** sent 28 Oct; 8 mainboard IPOs in 2026; Deepa 86% of fresh issue to inventory
- **Anthropic S-1: $16.3 bn H1 revenue, $80.7 bn loss ($72.4 bn paper charge):** 2026-11-02: 2 Nov: new turn, Alphabet -12.6%/-$500bn on AI spend (29 Oct); pick
- **Anthropic S-1: $16.3 bn H1 revenue, $80.7 bn loss ($72.4 bn paper charge):** 2026-11-04: 4 Nov: new turn, amended S-1 2 Nov: $33.2bn 9M revenue, $895.4bn commitments
- **LTCG tax-cut debate: ₹1.29 lakh crore a year; The Ken says don't cut:** 2026-10-29: The Ken 29 Oct
- **LTCG tax-cut debate: ₹1.29 lakh crore a year; The Ken says don't cut:** 2026-11-03: 3 Nov: new turn, SEBI proposes 0% LTCG for FPIs only (Reuters 2 Nov)
- **Equitas SFB: record profit, CEO quits over daughter's NBFC, 20% lower circuit:** desk 30 Oct
- **Equitas SFB: record profit, CEO quits over daughter's NBFC, 20% lower circuit:** 2026-10-30: record profit, −20% lower circuit, CEO quits
- **773 government sites still serving eMudhra's revoked certificates (via The Ken):** desk 30 Oct; The Ken 30 Oct
- **773 government sites still serving eMudhra's revoked certificates (via The Ken):** 2026-10-30: 773 of 1,366 gov names still on revoked certs (24 Oct)
- **Ola Electric rights issue: founder pledges shares to buy in, SoftBank sells:** sent 31 Oct, 7/10, via The Morning Context
- **Ola Electric rights issue: founder pledges shares to buy in, SoftBank sells:** 2026-10-31: 31 Oct
- **IDBI sale: Fairfax bid opened, then ₹94.42 floor discarded; sold at ₹81 (via BusinessWorld):** BusinessWorld 29 Oct; Pioneer 30 Oct
- **IDBI sale: Fairfax bid opened, then ₹94.42 floor discarded; sold at ₹81 (via BusinessWorld):** 2026-11-01: 1 Nov: sent
- **Binance $6.3 bn hack: users don't pay; WazirX users did:** sent 2 Nov, 9/10
- **SEBI order on EKI Energy: ₹197 cr revenue early, ₹88 lakh fines:** sent 2 Nov, 6/10, SEBI order 30 Oct
- **Reliance +12% record day, $19 bn added; Jio stake at 80% discount:** sent 3 Nov
- **Axis MF front-running: Dubai AnyDesk trades, brokers fined ₹10 lakh each:** SEBI AO order 3 Nov; sent 4 Nov, 7/10
