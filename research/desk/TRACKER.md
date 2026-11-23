# Story tracker

_Written 2026-11-23 by `pipeline/story_tracker.py md`. Data: registry/story_tracker.json._

Every story the desk has sent stays here until it leaves the news cycle (COLD on two checks running, or past its window). Each morning `story_tracker.py check` measures them all again.

Label history reads oldest to newest: H hot, R rising, F flat, C cold.

| Story | Status | Now | Direction | Day | History | News today/week | YouTube views this week | Best views/hr | Desk score | Window |
|---|---|---|---|---|---|---|---|---|---|---|
| Groww's F&O share of revenue falls to 45%; turns to IPOs and wealth (via The Arc) (`groww-derivatives-arc`) | active | COLD | fading | 37 | H C C C C H C | -/- | 272,678 | 2,963 | 7 | to about Fri 23 Oct |
| ₹89,000 cr of unclaimed shares with IEPF; Reliance biggest slice (Diwali-cleaning certificate reels) (`unclaimed-shares-iepf`) | active | COLD | steady | 15 | C C C H C C C | 0/4 | 4,603 | 33 | 8 | 2026-11-23 |
| Novartis India: ~50 staff, ₹1,446 cr for 71%; open offer got 40 shares (via The Ken) (`novartis-india-ken`) | active | COLD | steady | 14 | C C C C H C C | 1/4 | 898,359 | 7,462 | 6 | 2026-11-24 |
| B.R. Shetty liable in $5.4 bn NMC fraud; sold Finablr for $1; BoB paid $600M (via The Morning Context) (`br-shetty-nmc`) | active | COLD | fading | 13 | F H H C F F C | 0/9 | 146,377 | 761 | 7 | 2026-11-25 |
| Jio more customers, Airtel more money: ARPU ₹271 vs ₹218.8 (`airtel-vs-jio-arpu`) | active | COLD | fading | 12 | H C H C C C C | 0/1 | 81,551 | 310 | 7 | 2026-11-26 |
| NSE banned brokers' digital gold, then picked Augmont for EGRs (via The Ken) (`nse-augmont-digital-gold`) | active | COLD | rising | 11 | C C C C C C C | 0/0 | 265 | 7 | 7 | 2026-11-26 |
| India's 'sovereign' AI rented from Nvidia GPU clouds; E2E -36% from Oct high (via The Ken) (`india-sovereign-ai-nvidia`) | active | COLD | fading | 9 | H C C C C H C | 0/0 | 118,847 | 611 | 7 | 2026-11-29 |
| Mahanadi Coalfields IPO: Coal India sells 10% of India's largest coal producer (opens 19 Nov) (`mahanadi-coalfields-ipo`) | active | HOT | rising | 8 | F F R H H H | 8/100 | 969,436 | 14,719 | 8 | 2026-11-27 |
| Ola Electric closes its own stores for dealers; Q2 revenue -39% to Rs 421 cr (via The Morning Context) (`ola-electric-dealers`) | active | FLAT | steady | 8 | H H F F F F | 4/34 | 157,759 | 2,462 | 8 | 2026-11-29 |
| Yes Bank AT1 Rs 8,415 cr: SC restored the bonds; Yes Bank and RBI seek review (`yes-bank-at1`) | active | FLAT | steady | 6 | H C F F F | 0/11 | 133,943 | 491 | 8 | 2026-12-02 |
| SpiceJet: Rs 5,500 cr raise vs Rs 1,522 cr mcap; shares +30% in a week amid cancellations (`spicejet-fundraise`) | active | RISING | rising | 5 | F R F R | 39/100 | 258,061 | 1,115 | 9 | 2026-12-07 |
| ESDS: 2026's top IPO tripled on a $1.25 bn GPU deal it pays for (via The Morning Context) (`esds-sharon-ai`) | active | COLD | rising | 5 | C C C C | 0/1 | 94,421 | 682 | 6 | 2026-12-03 |
| CAG draft audit: BIS hallmark checks missed (`bis-hallmark-cag`) | active | HOT | steady | 4 | H H H | 0/4 | 2,430,576 | 9,983 | 8 | 2026-12-04 |
| 70% still in regular MF plans after direct default (`regular-plan-70pc`) | active | COLD | fading | 4 | C H C | 0/0 | 109,478 | 534 | 6 | 2026-12-04 |
| AI selloff abroad, India at a nine-month high on record FPI buying (`ai-selloff-india-rally`) | active | HOT | steady | 3 | H H | 0/5 | 1,399,998 | 6,908 | 8 | 2026-11-30 |
| Record ₹1.53 lakh crore margin trading book; SEBI weighs a cap (`mtf-record-leverage`) | active | HOT | rising | 3 | F H | 0/23 | 113,638 | 4,544 | 7 | 2026-12-05 |
| Silver ~65% off January's ₹4.2 lakh record; silver ETF inflows +57% in October (`silver-crash-65pc`) | active | HOT | new | 2 | H | 9/28 | 1,503,733 | 8,243 | 9 | 2026-11-27 |
| IndusInd fires ex-CEO Kathpalia, claws back pay from 2020 (`indusind-kathpalia-clawback`) | active | FLAT | new | 2 | F | 20/81 | 38,574 | 691 | 9 | 2026-11-29 |
| EPFO monthly PF payouts (SWP), 10% minimum balance, 2-month wait (`epfo-swp-pf-pension`) | active | HOT | new | 2 | H | 4/12 | 801,894 | 3,762 | 7 | 2026-11-29 |
| Jio Platforms IPO (`jio-ipo`) | retired: past its window | FLAT | rising | 47 | H H H H H F F | 23/100 | 2,342,949 | 4,935 | 8 | 2026-11-02 |
| Ramayana producer's Prime Focus searched by Income Tax (`prime-focus-ramayana`) | retired: COLD on 2 checks running | COLD | steady | 47 | H H H H C C | 0/0 | 1,056,196 | 7,548 | 8 | 2026-11-10 |
| International ETFs trading far above NAV (NSE warning) (`intl-etf-premium`) | retired: past its window | COLD | fading | 47 | C C C H H H C | 0/- | 438,146 | 4,086 | 6 | 2026-10-22 |
| EPF wage ceiling raised to ₹25,000 (`epf-wage-ceiling`) | retired: COLD on 2 checks running | COLD | fading | 47 | F F C C | 0/7 | 20,051 | 152 | - | - |
| Snapdeal (AceVector) after listing (`snapdeal-acevector`) | retired (E8): COLD on 2 checks running | COLD | steady | 47 | C C | 0/1 | 100,780 | 770 | - | - |
| Nana Patekar dies; the Rs 1.5 crore car he gave up for farmers (`nana-patekar`) | retired (E10): past its window | HOT | rising | 47 | R H H H | 100/100 | 27,305,534 | 110,559 | 7 | 2026-10-11 |
| Sensex -1,045 on 8 Oct: ₹10.23 lakh crore wiped off (`market-crash-oct8`) | retired: past its window | HOT | rising | 46 | H H C H | 9/17 | 3,239,882 | 14,656 | 9 | 2026-10-12 |
| TCS: profit +15%, share -35% in 2026 (`tcs-q2-profit-share`) | retired: past its window | HOT | rising | 46 | H F F F F H | 7/48 | 464,093 | 10,346 | 8 | 2026-10-14 |
| SC orders panel on pharma freebies to doctors (`pharma-freebies-sc`) | retired: past its window | COLD | fading | 46 | H H H C C C C | 0/0 | 445,730 | 1,054 | 6 | 2026-10-23 |
| UPI merchant fee (0.4% MDR) may be deferred to 1 Jan (`upi-mdr-deferral`) | retired: past its window | HOT | rising | 45 | H F H H H H H | 2/41 | 910,815 | 4,784 | 6 | 2026-10-16 |
| Inox Clean: revenue 43X, debt 45X, IPO on hold (`inox-clean-ipo`) | retired: past its window | COLD | fading | 45 | H C C C C C C | 0/0 | 29,731 | 131 | 6 | 2026-10-24 |
| Musk calls Ambani 'Prime Minister Ambani' over Starlink (`musk-ambani-starlink`) | retired: past its window | FLAT | fading | 44 | F F H H H H F | 1/10 | 4,347,306 | 14,666 | 8 | 2026-10-21 |
| US suspends TCS, Infosys, Wipro from green-card PERM; IT shares rise (`us-perm-indian-it`) | retired: COLD on 2 checks running | COLD | steady | 44 | H C C | 0/1 | 1,195,114 | 3,721 | 8 | 2026-10-17 |
| SC on hospital drug markups: Rs 2,700 drug sold at Rs 27,000 (`hospital-drug-markup-sc`) | retired: past its window | HOT | rising | 44 | H C C C C C H | 0/0 | 168,581 | 6,896 | 6 | 2026-10-25 |
| HDFC Bank's new CEO ₹35.9 cr vs SBI chairman ₹43 lakh (`hdfc-ceo-pay-sbi`) | retired: COLD on 2 checks running | COLD | fading | 43 | C C | 0/1 | 8,051 | 55 | 9 | 2026-10-27 |
| Gauahar Khan's Versova duplex: 88% in 12 years (`gauahar-khan-flat`) | retired: past its window | COLD | fading | 43 | C C H C C C C | 0/0 | 0 | 0 | 6 | 2026-10-26 |
| Kohli and Anushka's ₹44 crore: three Versova flats, ready 2031 (`kohli-anushka-versova-flats`) | retired: COLD on 2 checks running | COLD | fading | 42 | C C | 0/0 | 598 | 25 | 8 | 2026-10-20 |
| Rupee near ₹97: RBI hike, then four emergency measures (`rbi-rupee-rescue`) | retired: COLD on 2 checks running | COLD | rising | 42 | H H H C C | 0/9 | 1,516,191 | 14,931 | 7 | 2026-10-20 |
| Zoho freezes pay rises over AI and server costs (`zoho-pay-freeze`) | retired: COLD on 2 checks running | COLD | rising | 41 | H C C | 0/2 | 287,736 | 1,847 | 9 | 2026-10-20 |
| Sensex +1,109 partly on FM's LTCG remark (`ltcg-remark-rally`) | retired: COLD on 2 checks running | COLD | fading | 41 | H H H H C C | 0/1 | 1,266,936 | 3,079 | 8 | 2026-10-20 |
| Gold ₹3,600 cheaper in four sessions on a stronger rupee (`gold-slide-rupee`) | retired: past its window | RISING | rising | 40 | H R R F R | 31/85 | 175,924 | 2,637 | 8 | 2026-10-19 |
| Airtel Money lists in London at $7 bn (via The Ken) (`airtel-money-london`) | retired: past its window | FLAT | steady | 40 | F F F R F F F | 6/40 | 222,173 | 1,254 | 6 | 2026-10-29 |
| Yes Bank -14.5% after SC voids AT-1 write-off (`yes-bank-at1-sc`) | retired: past its window | FLAT | steady | 39 | R H F F F | 2/36 | 452,328 | 1,618 | 8 | 2026-10-20 |
| Mutual funds halt new gold FoF SIPs and bulk gold ETF buys (`gold-fund-halt`) | retired: past its window | HOT | rising | 39 | F F H H H F H | 6/33 | 776,117 | 6,735 | 9 | 2026-11-08 |
| Zetwerk IPO: 54% of Q1 revenue from metal sales (`zetwerk-ipo-metals`) | retired: past its window | FLAT | rising | 39 | F F R F F C F | 7/31 | 159,682 | 735 | 7 | 2026-10-23 |
| IDBI Bank sold to Fairfax at ₹81 vs ₹90 market (`idbi-fairfax-sale`) | retired: COLD on 2 checks running | COLD | fading | 38 | H H H F H C C | 1/4 | 255,768 | 1,751 | 9 | 2026-10-24 |
| ED raids WhatsApp 'Multibagger' pump-and-dump (RM Drip, R&B Denims) (`ed-whatsapp-multibagger`) | retired: COLD on 2 checks running | COLD | rising | 38 | C C | 0/3 | 230 | 5 | 7 | 2026-10-22 |
| Insurance mis-selling complaints +14%; IRDAI crackdown may slip (via The Ken) (`insurance-misselling-ken`) | retired: past its window | COLD | steady | 38 | C C H C C C C | 0/2 | 36,261 | 278 | 6 | 2026-10-31 |
| Green-card freeze 'bloodbath' reels, then Indian IT's best week since 2008 (`it-rally-green-card`) | retired: COLD on 2 checks running | COLD | steady | 37 | C H C C | 1/3 | 38,873 | 1,467 | 9 | to about Wed 21 Oct |
| Expired food allegedly back on sale: FIR names Reliance, Blinkit directors (`expired-food-reliance-blinkit`) | retired: COLD on 2 checks running | COLD | rising | 37 | C C | 0/0 | 27,744 | 247 | 8 | to about Tue 20 Oct |
| Axis Bank: profit +38%, shares -5% (base effect of last year's ₹1,231 cr provision) (`axis-bank-q2-fall`) | retired: past its window | RISING | rising | 35 | R R R R | 38/66 | 300,690 | 1,158 | 8 | 2026-10-23 |
| Air India FY26 loss ₹22,238 cr (~₹61 cr a day); SIA as saviour (via The Ken) (`air-india-loss-ken`) | retired: past its window | COLD | rising | 35 | C C C H H C C | 0/0 | 827,897 | 2,207 | 6 | 2026-11-02 |
| Silver -46% from January record (₹3,84,632 → ₹2,08,380/kg) before Dhanteras (`silver-crash-46`) | retired: COLD on 2 checks running | COLD | fading | 34 | H H H H F C C | 0/5 | 660,502 | 1,423 | 7 | 2026-11-08 |
| Urban Company loss triples on InstaHelp: ₹114 booking, ₹279 loss (via The Morning Context) (`urban-company-instahelp`) | retired: past its window | COLD | steady | 34 | C C C C H C C | 0/0 | 113,063 | 1,695 | 7 | 2026-11-03 |
| eMudhra -20% lower circuit after its certificate keys turned out to be tiny numbers (one was 4) (`emudhra-key-4`) | retired: past its window | FLAT | rising | 33 | H H F F F F | 0/12 | 191,204 | 552 | 9 | 2026-10-27 |
| Oil at $112: shares, gold and silver fell the same day (`oil-slide-everything`) | retired: past its window | HOT | rising | 32 | H H H H H C H | 0/3 | 1,107,504 | 8,878 | 8 | 2026-10-29 |
| SEBI final order: Avadhut Sathe ₹546 cr refund (`avadhut-sathe-refund`) | retired: past its window | HOT | rising | 31 | R F H H H F H | 1/20 | 526,055 | 3,209 | 6 | 2026-10-30 |
| NSE unlisted buyers below IPO price (The Ken) (`nse-unlisted-regret-ken`) | retired: past its window | COLD | rising | 31 | C F F F C C C | 0/8 | 271,121 | 1,309 | 7 | 2026-11-07 |
| Swiggy record low, less than half its IPO price; Instamart loss ₹895 cr (`swiggy-record-low`) | retired: past its window | FLAT | steady | 30 | F F F F | 0/32 | 170,029 | 627 | 9 | 2026-10-28 |
| RBI Governor: upper-layer CICs like Tata Sons must list (`tata-sons-listing`) | retired: COLD on 2 checks running | COLD | steady | 30 | C C | 0/2 | 135,201 | 1,538 | 8 | 2026-11-08 |
| Jio's prepaid (77% of revenue) sold only via Reliance Retail (via The Ken) (`jio-reliance-retail-ken`) | retired: past its window | HOT | rising | 30 | H C H C C C H | 0/1 | 513,481 | 13,105 | 8 | 2026-11-04 |
| Gold ₹38,000 below January peak, ₹5,560/10g down in 3 days, before Dhanteras (`gold-dhanteras-fall`) | retired: COLD on 2 checks running | COLD | fading | 29 | H H H H H C C | 0/2 | 808,081 | 2,117 | 8 | 2026-11-06 |
| HDFC Bank's first outside CEO starts; share ~30% down in a year (via The Morning Context) (`hdfc-bank-bagchi`) | retired: past its window | FLAT | rising | 28 | F F F F F F F | 5/19 | 64,397 | 517 | 8 | 2026-11-03 |
| Jewellery makers' IPO wave: money goes to gold and debt (via The Ken) (`jewellery-ipo-ken`) | retired: past its window | COLD | fading | 27 | C C C C C C C | 0/2 | 28,092 | 74 | 5 | 2026-11-06 |
| Anthropic S-1: $16.3 bn H1 revenue, $80.7 bn loss ($72.4 bn paper charge) (`anthropic-s1`) | retired: past its window | HOT | rising | 26 | H H H R H H H | 100/100 | 1,820,032 | 18,490 | 9 | 2026-11-20 |
| LTCG tax-cut debate: ₹1.29 lakh crore a year; The Ken says don't cut (`ltcg-cut-debate`) | retired: past its window | FLAT | steady | 26 | F F F F F F F | 6/27 | 960,328 | 5,490 | 8 | 2026-11-12 |
| Equitas SFB: record profit, CEO quits over daughter's NBFC, 20% lower circuit (`equitas-ceo-exit`) | retired: past its window | FLAT | steady | 25 | F F F C F F F | 10/47 | 63,640 | 302 | 8 | 2026-11-06 |
| 773 government sites still serving eMudhra's revoked certificates (via The Ken) (`emudhra-gov-sites`) | retired: past its window | COLD | fading | 25 | C C C C C C C | 0/0 | 221 | 1 | 5 | 2026-11-13 |
| SEBI makes direct mutual fund plans the default on AMC apps from 1 Nov (`sebi-direct-default`) | retired: past its window | COLD | steady | 24 | C C | 0/0 | 28,685 | 213 | 7 | 2026-11-01 |
| Ola Electric rights issue: founder pledges shares to buy in, SoftBank sells (`ola-rights-pledge`) | retired: past its window | COLD | steady | 24 | C C C C C C C | 0/1 | 131,750 | 1,192 | 7 | 2026-11-07 |
| IDBI sale: Fairfax bid opened, then ₹94.42 floor discarded; sold at ₹81 (via BusinessWorld) (`idbi-note-reserve`) | retired: past its window | COLD | fading | 23 | C H C H H H C | 0/2 | 1,212,101 | 6,662 | 7 | 2026-11-08 |
| Binance $6.3 bn hack: users don't pay; WazirX users did (`binance-hack-wazirx`) | retired: past its window | HOT | steady | 22 | H R R R H H | 24/100 | 679,423 | 5,185 | 9 | 2026-11-07 |
| SEBI order on EKI Energy: ₹197 cr revenue early, ₹88 lakh fines (`eki-sebi-order`) | retired: past its window | COLD | steady | 22 | C C C C C C C | 0/0 | 241,799 | 1,478 | 6 | 2026-11-08 |
| Reliance +12% record day, $19 bn added; Jio stake at 80% discount (`reliance-record-day`) | retired: past its window | FLAT | steady | 21 | H F F | 0/13 | 433,825 | 1,908 | 9 | 2026-11-05 |
| Axis MF front-running: Dubai AnyDesk trades, brokers fined ₹10 lakh each (`axis-mf-frontrun`) | retired: past its window | COLD | fading | 20 | C H C C H H C | 0/0 | 311,088 | 2,248 | 7 | 2026-11-17 |
| Stockal: US shares sold without consent, swapped for Chinese microcaps; ₹100 cr+ alleged (`stockal-unauthorised-trades`) | retired: past its window | HOT | rising | 19 | H H H F H F H | 1/8 | 250,324 | 5,423 | 8 | 2026-11-12 |
| Samvat 2082: Sensex -11.9%, Nifty -11%, worst in 15 years (`samvat-2082-worst`) | retired: past its window | RISING | rising | 19 | R R F R | 79/100 | 357,785 | 2,201 | 8 | 2026-11-08 |
| AI trade cracks: Nvidia -$450 bn, Nasdaq -5.5%; FIIs buy ₹14,975 cr of India the same day (`ai-crash-india-inflow`) | retired: past its window | HOT | rising | 18 | H H H | 1/11 | 3,102,086 | 19,014 | 9 | 2026-11-08 |
| Videocon's Venugopal Dhoot declared personally bankrupt over ₹12,668 crore SBI dues (`videocon-dhoot-bankrupt`) | retired: past its window | HOT | rising | 17 | C H H H | 0/4 | 1,177,231 | 8,133 | 9 | 2026-11-10 |
| Airlines fly fewer, charge more: IndiGo passengers -4.7%, yield +34%; SC 'Don't travel by air' (via The Ken) (`airfares-fly-less-pay-more`) | retired: past its window | COLD | steady | 16 | C C C C C C C | 1/2 | 50,933 | 154 | 7 | 2026-11-16 |
| Ramayana: ₹499 cr worldwide in 4 days vs ₹4,000 cr bill for two films (`ramayana-box-office`) | retired: past its window | HOT | rising | 15 | H H H H H H H | 54/100 | 3,787,870 | 56,656 | 8 | 2026-11-15 |
| India's best week since Feb 2021: Nifty +8.6%, FIIs buy ~₹46,000 cr back after ₹45,162 cr October exit (`india-best-week-fii`) | retired: past its window | HOT | rising | 14 | H H H C H | 0/0 | 369,104 | 3,548 | 8 | 2026-11-14 |
| ED raids CoinDCX and Delta: tokenised 'Apple, Tesla' routed abroad, alleged; $16M wallet loss two weeks earlier (`coindcx-ed-raid`) | retired: COLD on 2 checks running | COLD | steady | 13 | C C | 1/1 | 1,342,333 | 7,024 | 8 | 2026-11-18 |
| Jensen Huang quits Nvidia; ~$1.7 tn off since Oct peak; top Nasdaq 100 fund holding (`nvidia-huang-resigns`) | retired: past its window | HOT | fading | 11 | H H H H | 0/27 | 1,368,275 | 5,131 | 9 | 2026-11-17 |
| Retail inflation 6.09%, past RBI's 6% ceiling; SBI 1-yr FD ~6.25% (`india-cpi-6pct`) | retired: COLD on 2 checks running | COLD | rising | 9 | C C | 0/5 | 500,942 | 2,991 | 8 | 2026-12-02 |
| Nvidia Q3 $115.8 bn, doubled; board won't reinstate Huang (`nvidia-q3-board-no-huang`) | retired: past its window | HOT | rising | 6 | H F H | 7/100 | 1,087,747 | 7,762 | 9 | 2026-11-20 |

## Latest notes
- **Groww's F&O share of revenue falls to 45%; turns to IPOs and wealth (via The Arc):** 2026-10-22: 22 Oct: The Ken 'hostage to options'; Groww PAT ₹725 cr, F&O 44.8% of revenue; SEBI FY26 87.7% lose
- **₹89,000 cr of unclaimed shares with IEPF; Reliance biggest slice (Diwali-cleaning certificate reels):** sent 9 Nov, 8/10
- **B.R. Shetty liable in $5.4 bn NMC fraud; sold Finablr for $1; BoB paid $600M (via The Morning Context):** sent 11 Nov
- **Jio more customers, Airtel more money: ARPU ₹271 vs ₹218.8:** sent 12 Nov, 7/10, via The Morning Context
- **NSE banned brokers' digital gold, then picked Augmont for EGRs (via The Ken):** 2026-11-14: 14 Nov: carried, no new turn
- **India's 'sovereign' AI rented from Nvidia GPU clouds; E2E -36% from Oct high (via The Ken):** sent 15 Nov, 7/10, The Ken 14 Nov
- **Mahanadi Coalfields IPO: Coal India sells 10% of India's largest coal producer (opens 19 Nov):** sent 16 Nov, 7/10
- **Mahanadi Coalfields IPO: Coal India sells 10% of India's largest coal producer (opens 19 Nov):** 2026-11-21: 0.49x after day 2, retail 0.25x; GMP ₹25→₹1.3
- **Ola Electric closes its own stores for dealers; Q2 revenue -39% to Rs 421 cr (via The Morning Context):** sent 16 Nov, 8/10, The Morning Context 13 Nov
- **Yes Bank AT1 Rs 8,415 cr: SC restored the bonds; Yes Bank and RBI seek review:** sent 18 Nov, 8/10, Moneylife lead
- **CAG draft audit: BIS hallmark checks missed:** CAG draft: 2,194 of 5,020 AHC audits missed; 5,444 of 28,865 jewellers inspected 2024-25
- **CAG draft audit: BIS hallmark checks missed:** 2026-11-23: deep lane via Moneylife 22 Nov; 81% uninspected 2024-25
- **70% still in regular MF plans after direct default:** The Ken 19 Nov
- **AI selloff abroad, India at a nine-month high on record FPI buying:** S&P correction, Nikkei/Kospi -5%, Anthropic -9% day 2; Sensex +1.08% to 83,919.71
- **AI selloff abroad, India at a nine-month high on record FPI buying:** 2026-11-23: Nov MTD Sensex +12.7% vs Nasdaq -11.1%; FII record ₹1,11,949 cr, DII -₹61,786 cr
- **Record ₹1.53 lakh crore margin trading book; SEBI weighs a cap:** Reuters/TMC 17 Nov
- **Silver ~65% off January's ₹4.2 lakh record; silver ETF inflows +57% in October:** desk 22 Nov
- **Silver ~65% off January's ₹4.2 lakh record; silver ETF inflows +57% in October:** 2026-11-23: MCX close ₹1,47,813 15-month low; COMEX -14% week
- **IndusInd fires ex-CEO Kathpalia, claws back pay from 2020:** desk 22 Nov
- **EPFO monthly PF payouts (SWP), 10% minimum balance, 2-month wait:** desk 22 Nov
