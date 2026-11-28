# Story tracker

_Written 2026-11-28 by `pipeline/story_tracker.py md`. Data: registry/story_tracker.json._

Every story the desk has sent stays here until it leaves the news cycle (COLD on two checks running, or past its window). Each morning `story_tracker.py check` measures them all again.

Label history reads oldest to newest: H hot, R rising, F flat, C cold.

| Story | Status | Now | Direction | Day | History | News today/week | YouTube views this week | Best views/hr | Desk score | Window |
|---|---|---|---|---|---|---|---|---|---|---|
| Groww's F&O share of revenue falls to 45%; turns to IPOs and wealth (via The Arc) (`groww-derivatives-arc`) | active | COLD | fading | 42 | H C C C C C C | 0/0 | 115,763 | 2,070 | 7 | to about Fri 23 Oct |
| India's 'sovereign' AI rented from Nvidia GPU clouds; E2E -36% from Oct high (via The Ken) (`india-sovereign-ai-nvidia`) | active | COLD | rising | 14 | H C C C C C C | 0/0 | 130,926 | 2,361 | 7 | 2026-11-29 |
| Ola Electric closes its own stores for dealers; Q2 revenue -39% to Rs 421 cr (via The Morning Context) (`ola-electric-dealers`) | active | FLAT | steady | 13 | F F F F R F F | 4/29 | 253,779 | 697 | 8 | 2026-11-29 |
| Yes Bank AT1 Rs 8,415 cr: SC restored the bonds; Yes Bank and RBI seek review (`yes-bank-at1`) | active | COLD | fading | 11 | F F F C C C C | 0/3 | 780 | 4 | 8 | 2026-12-02 |
| SpiceJet: Rs 5,500 cr raise vs Rs 1,522 cr mcap; shares +30% in a week amid cancellations (`spicejet-fundraise`) | active | RISING | rising | 10 | F R F R F F R | 36/100 | 35,746 | 161 | 9 | 2026-12-07 |
| ESDS: 2026's top IPO tripled on a $1.25 bn GPU deal it pays for (via The Morning Context) (`esds-sharon-ai`) | active | COLD | steady | 10 | C C H C C C C | 1/2 | 26,759 | 74 | 6 | 2026-12-03 |
| CAG draft audit: BIS hallmark checks missed (`bis-hallmark-cag`) | active | HOT | steady | 9 | H H H C H H H | 2/3 | 3,171,526 | 23,151 | 8 | 2026-12-04 |
| 70% still in regular MF plans after direct default (`regular-plan-70pc`) | active | COLD | rising | 9 | H C C H H C C | 0/0 | 142,720 | 1,705 | 6 | 2026-12-04 |
| Record ₹1.53 lakh crore margin trading book; SEBI weighs a cap (`mtf-record-leverage`) | active | COLD | fading | 8 | F H F F F F C | 1/7 | 1,080 | 9 | 7 | 2026-12-05 |
| IndusInd fires ex-CEO Kathpalia, claws back pay from 2020 (`indusind-kathpalia-clawback`) | active | FLAT | fading | 7 | F F F F F F | 5/43 | 0 | 0 | 9 | 2026-11-29 |
| EPFO monthly PF payouts (SWP), 10% minimum balance, 2-month wait (`epfo-swp-pf-pension`) | active | HOT | rising | 7 | H F F F F H | 2/8 | 517,102 | 4,071 | 7 | 2026-11-29 |
| SEBI asks intermediaries to stop publishing IPO GMP (advisory, 23 Nov) (`sebi-gmp-advisory`) | active | FLAT | steady | 5 | C H F F | 6/46 | 295,566 | 2,166 | 9 | 2026-11-30 |
| NSEL pays 5,682 investors ₹1,950 crore, 42.34% of claims, 13 years on (`nsel-settlement`) | active | FLAT | steady | 5 | C F F F | 0/10 | 26,259 | 54 | 6 | 2026-12-01 |
| Tata Sons board takes up listing on 30 Nov; RBI letter 16 Nov says list (`tata-sons-board-nov30`) | active | FLAT | fading | 4 | F H F | 0/36 | 107,809 | 1,757 | 6 | 2026-11-30 |
| Rs 20,000 cr crypto forex chase; ED searched CoinDCX, Delta; no user protection (via The Ken) (`ken-crypto-20000cr`) | active | COLD | rising | 4 | H C C | 0/0 | 283,730 | 1,621 | 7 | 2026-12-07 |
| PhonePe restarts IPO at $12-15 bn (`phonepe-ipo-revival`) | active | FLAT | rising | 3 | F F | 2/17 | 50,138 | 440 | 9 | 2026-12-20 |
| Gold falls 9.4% in nine days (`gold-crash-nov`) | active | RISING | fading | 3 | H R | 100/100 | 1,753,811 | 11,482 | 6 | 2026-12-06 |
| Tata Steel-APL Apollo deal (`tata-steel-apl-apollo`) | active | RISING | rising | 3 | F R | 48/100 | 262,498 | 1,652 | 9 | 2026-12-04 |
| Flipkart CEO Kalyan Krishnamurthy exits; Walmart, kickback probe, IPO to 2028 (`flipkart-ceo-exit`) | active | FLAT | new | 2 | F | 8/100 | 41,835 | 562 | 9 | 2026-12-10 |
| $1 bn cap: Indians overpay for US-index ETFs (The Ken) (`us-etf-premium-cap`) | active | COLD | new | 2 | C | 0/0 | 31,754 | 408 | 6 | 2026-12-11 |
| SC closes unclaimed-money PIL; Rs 86,917 crore in RBI's DEA Fund (`unclaimed-assets-sc`) | active | - | new | 1 |  | -/- | 0 | 0 | 8 | 2026-12-12 |
| Jio Platforms IPO (`jio-ipo`) | retired: past its window | FLAT | rising | 52 | H H H H H F F | 23/100 | 2,342,949 | 4,935 | 8 | 2026-11-02 |
| Ramayana producer's Prime Focus searched by Income Tax (`prime-focus-ramayana`) | retired: COLD on 2 checks running | COLD | steady | 52 | H H H H C C | 0/0 | 1,056,196 | 7,548 | 8 | 2026-11-10 |
| International ETFs trading far above NAV (NSE warning) (`intl-etf-premium`) | retired: past its window | COLD | fading | 52 | C C C H H H C | 0/- | 438,146 | 4,086 | 6 | 2026-10-22 |
| EPF wage ceiling raised to ₹25,000 (`epf-wage-ceiling`) | retired: COLD on 2 checks running | COLD | fading | 52 | F F C C | 0/7 | 20,051 | 152 | - | - |
| Snapdeal (AceVector) after listing (`snapdeal-acevector`) | retired (E8): COLD on 2 checks running | COLD | steady | 52 | C C | 0/1 | 100,780 | 770 | - | - |
| Nana Patekar dies; the Rs 1.5 crore car he gave up for farmers (`nana-patekar`) | retired (E10): past its window | HOT | rising | 52 | R H H H | 100/100 | 27,305,534 | 110,559 | 7 | 2026-10-11 |
| Sensex -1,045 on 8 Oct: ₹10.23 lakh crore wiped off (`market-crash-oct8`) | retired: past its window | HOT | rising | 51 | H H C H | 9/17 | 3,239,882 | 14,656 | 9 | 2026-10-12 |
| TCS: profit +15%, share -35% in 2026 (`tcs-q2-profit-share`) | retired: past its window | HOT | rising | 51 | H F F F F H | 7/48 | 464,093 | 10,346 | 8 | 2026-10-14 |
| SC orders panel on pharma freebies to doctors (`pharma-freebies-sc`) | retired: past its window | COLD | fading | 51 | H H H C C C C | 0/0 | 445,730 | 1,054 | 6 | 2026-10-23 |
| UPI merchant fee (0.4% MDR) may be deferred to 1 Jan (`upi-mdr-deferral`) | retired: past its window | HOT | rising | 50 | H F H H H H H | 2/41 | 910,815 | 4,784 | 6 | 2026-10-16 |
| Inox Clean: revenue 43X, debt 45X, IPO on hold (`inox-clean-ipo`) | retired: past its window | COLD | fading | 50 | H C C C C C C | 0/0 | 29,731 | 131 | 6 | 2026-10-24 |
| Musk calls Ambani 'Prime Minister Ambani' over Starlink (`musk-ambani-starlink`) | retired: past its window | FLAT | fading | 49 | F F H H H H F | 1/10 | 4,347,306 | 14,666 | 8 | 2026-10-21 |
| US suspends TCS, Infosys, Wipro from green-card PERM; IT shares rise (`us-perm-indian-it`) | retired: COLD on 2 checks running | COLD | steady | 49 | H C C | 0/1 | 1,195,114 | 3,721 | 8 | 2026-10-17 |
| SC on hospital drug markups: Rs 2,700 drug sold at Rs 27,000 (`hospital-drug-markup-sc`) | retired: past its window | HOT | rising | 49 | H C C C C C H | 0/0 | 168,581 | 6,896 | 6 | 2026-10-25 |
| HDFC Bank's new CEO ₹35.9 cr vs SBI chairman ₹43 lakh (`hdfc-ceo-pay-sbi`) | retired: COLD on 2 checks running | COLD | fading | 48 | C C | 0/1 | 8,051 | 55 | 9 | 2026-10-27 |
| Gauahar Khan's Versova duplex: 88% in 12 years (`gauahar-khan-flat`) | retired: past its window | COLD | fading | 48 | C C H C C C C | 0/0 | 0 | 0 | 6 | 2026-10-26 |
| Kohli and Anushka's ₹44 crore: three Versova flats, ready 2031 (`kohli-anushka-versova-flats`) | retired: COLD on 2 checks running | COLD | fading | 47 | C C | 0/0 | 598 | 25 | 8 | 2026-10-20 |
| Rupee near ₹97: RBI hike, then four emergency measures (`rbi-rupee-rescue`) | retired: COLD on 2 checks running | COLD | rising | 47 | H H H C C | 0/9 | 1,516,191 | 14,931 | 7 | 2026-10-20 |
| Zoho freezes pay rises over AI and server costs (`zoho-pay-freeze`) | retired: COLD on 2 checks running | COLD | rising | 46 | H C C | 0/2 | 287,736 | 1,847 | 9 | 2026-10-20 |
| Sensex +1,109 partly on FM's LTCG remark (`ltcg-remark-rally`) | retired: COLD on 2 checks running | COLD | fading | 46 | H H H H C C | 0/1 | 1,266,936 | 3,079 | 8 | 2026-10-20 |
| Gold ₹3,600 cheaper in four sessions on a stronger rupee (`gold-slide-rupee`) | retired: past its window | RISING | rising | 45 | H R R F R | 31/85 | 175,924 | 2,637 | 8 | 2026-10-19 |
| Airtel Money lists in London at $7 bn (via The Ken) (`airtel-money-london`) | retired: past its window | FLAT | steady | 45 | F F F R F F F | 6/40 | 222,173 | 1,254 | 6 | 2026-10-29 |
| Yes Bank -14.5% after SC voids AT-1 write-off (`yes-bank-at1-sc`) | retired: past its window | FLAT | steady | 44 | R H F F F | 2/36 | 452,328 | 1,618 | 8 | 2026-10-20 |
| Mutual funds halt new gold FoF SIPs and bulk gold ETF buys (`gold-fund-halt`) | retired: past its window | HOT | rising | 44 | F F H H H F H | 6/33 | 776,117 | 6,735 | 9 | 2026-11-08 |
| Zetwerk IPO: 54% of Q1 revenue from metal sales (`zetwerk-ipo-metals`) | retired: past its window | FLAT | rising | 44 | F F R F F C F | 7/31 | 159,682 | 735 | 7 | 2026-10-23 |
| IDBI Bank sold to Fairfax at ₹81 vs ₹90 market (`idbi-fairfax-sale`) | retired: COLD on 2 checks running | COLD | fading | 43 | H H H F H C C | 1/4 | 255,768 | 1,751 | 9 | 2026-10-24 |
| ED raids WhatsApp 'Multibagger' pump-and-dump (RM Drip, R&B Denims) (`ed-whatsapp-multibagger`) | retired: COLD on 2 checks running | COLD | rising | 43 | C C | 0/3 | 230 | 5 | 7 | 2026-10-22 |
| Insurance mis-selling complaints +14%; IRDAI crackdown may slip (via The Ken) (`insurance-misselling-ken`) | retired: past its window | COLD | steady | 43 | C C H C C C C | 0/2 | 36,261 | 278 | 6 | 2026-10-31 |
| Green-card freeze 'bloodbath' reels, then Indian IT's best week since 2008 (`it-rally-green-card`) | retired: COLD on 2 checks running | COLD | steady | 42 | C H C C | 1/3 | 38,873 | 1,467 | 9 | to about Wed 21 Oct |
| Expired food allegedly back on sale: FIR names Reliance, Blinkit directors (`expired-food-reliance-blinkit`) | retired: COLD on 2 checks running | COLD | rising | 42 | C C | 0/0 | 27,744 | 247 | 8 | to about Tue 20 Oct |
| Axis Bank: profit +38%, shares -5% (base effect of last year's ₹1,231 cr provision) (`axis-bank-q2-fall`) | retired: past its window | RISING | rising | 40 | R R R R | 38/66 | 300,690 | 1,158 | 8 | 2026-10-23 |
| Air India FY26 loss ₹22,238 cr (~₹61 cr a day); SIA as saviour (via The Ken) (`air-india-loss-ken`) | retired: past its window | COLD | rising | 40 | C C C H H C C | 0/0 | 827,897 | 2,207 | 6 | 2026-11-02 |
| Silver -46% from January record (₹3,84,632 → ₹2,08,380/kg) before Dhanteras (`silver-crash-46`) | retired: COLD on 2 checks running | COLD | fading | 39 | H H H H F C C | 0/5 | 660,502 | 1,423 | 7 | 2026-11-08 |
| Urban Company loss triples on InstaHelp: ₹114 booking, ₹279 loss (via The Morning Context) (`urban-company-instahelp`) | retired: past its window | COLD | steady | 39 | C C C C H C C | 0/0 | 113,063 | 1,695 | 7 | 2026-11-03 |
| eMudhra -20% lower circuit after its certificate keys turned out to be tiny numbers (one was 4) (`emudhra-key-4`) | retired: past its window | FLAT | rising | 38 | H H F F F F | 0/12 | 191,204 | 552 | 9 | 2026-10-27 |
| Oil at $112: shares, gold and silver fell the same day (`oil-slide-everything`) | retired: past its window | HOT | rising | 37 | H H H H H C H | 0/3 | 1,107,504 | 8,878 | 8 | 2026-10-29 |
| SEBI final order: Avadhut Sathe ₹546 cr refund (`avadhut-sathe-refund`) | retired: past its window | HOT | rising | 36 | R F H H H F H | 1/20 | 526,055 | 3,209 | 6 | 2026-10-30 |
| NSE unlisted buyers below IPO price (The Ken) (`nse-unlisted-regret-ken`) | retired: past its window | COLD | rising | 36 | C F F F C C C | 0/8 | 271,121 | 1,309 | 7 | 2026-11-07 |
| Swiggy record low, less than half its IPO price; Instamart loss ₹895 cr (`swiggy-record-low`) | retired: past its window | FLAT | steady | 35 | F F F F | 0/32 | 170,029 | 627 | 9 | 2026-10-28 |
| RBI Governor: upper-layer CICs like Tata Sons must list (`tata-sons-listing`) | retired: COLD on 2 checks running | COLD | steady | 35 | C C | 0/2 | 135,201 | 1,538 | 8 | 2026-11-08 |
| Jio's prepaid (77% of revenue) sold only via Reliance Retail (via The Ken) (`jio-reliance-retail-ken`) | retired: past its window | HOT | rising | 35 | H C H C C C H | 0/1 | 513,481 | 13,105 | 8 | 2026-11-04 |
| Gold ₹38,000 below January peak, ₹5,560/10g down in 3 days, before Dhanteras (`gold-dhanteras-fall`) | retired: COLD on 2 checks running | COLD | fading | 34 | H H H H H C C | 0/2 | 808,081 | 2,117 | 8 | 2026-11-06 |
| HDFC Bank's first outside CEO starts; share ~30% down in a year (via The Morning Context) (`hdfc-bank-bagchi`) | retired: past its window | FLAT | rising | 33 | F F F F F F F | 5/19 | 64,397 | 517 | 8 | 2026-11-03 |
| Jewellery makers' IPO wave: money goes to gold and debt (via The Ken) (`jewellery-ipo-ken`) | retired: past its window | COLD | fading | 32 | C C C C C C C | 0/2 | 28,092 | 74 | 5 | 2026-11-06 |
| Anthropic S-1: $16.3 bn H1 revenue, $80.7 bn loss ($72.4 bn paper charge) (`anthropic-s1`) | retired: past its window | HOT | rising | 31 | H H H R H H H | 100/100 | 1,820,032 | 18,490 | 9 | 2026-11-20 |
| LTCG tax-cut debate: ₹1.29 lakh crore a year; The Ken says don't cut (`ltcg-cut-debate`) | retired: past its window | FLAT | steady | 31 | F F F F F F F | 6/27 | 960,328 | 5,490 | 8 | 2026-11-12 |
| Equitas SFB: record profit, CEO quits over daughter's NBFC, 20% lower circuit (`equitas-ceo-exit`) | retired: past its window | FLAT | steady | 30 | F F F C F F F | 10/47 | 63,640 | 302 | 8 | 2026-11-06 |
| 773 government sites still serving eMudhra's revoked certificates (via The Ken) (`emudhra-gov-sites`) | retired: past its window | COLD | fading | 30 | C C C C C C C | 0/0 | 221 | 1 | 5 | 2026-11-13 |
| SEBI makes direct mutual fund plans the default on AMC apps from 1 Nov (`sebi-direct-default`) | retired: past its window | COLD | steady | 29 | C C | 0/0 | 28,685 | 213 | 7 | 2026-11-01 |
| Ola Electric rights issue: founder pledges shares to buy in, SoftBank sells (`ola-rights-pledge`) | retired: past its window | COLD | steady | 29 | C C C C C C C | 0/1 | 131,750 | 1,192 | 7 | 2026-11-07 |
| IDBI sale: Fairfax bid opened, then ₹94.42 floor discarded; sold at ₹81 (via BusinessWorld) (`idbi-note-reserve`) | retired: past its window | COLD | fading | 28 | C H C H H H C | 0/2 | 1,212,101 | 6,662 | 7 | 2026-11-08 |
| Binance $6.3 bn hack: users don't pay; WazirX users did (`binance-hack-wazirx`) | retired: past its window | HOT | steady | 27 | H R R R H H | 24/100 | 679,423 | 5,185 | 9 | 2026-11-07 |
| SEBI order on EKI Energy: ₹197 cr revenue early, ₹88 lakh fines (`eki-sebi-order`) | retired: past its window | COLD | steady | 27 | C C C C C C C | 0/0 | 241,799 | 1,478 | 6 | 2026-11-08 |
| Reliance +12% record day, $19 bn added; Jio stake at 80% discount (`reliance-record-day`) | retired: past its window | FLAT | steady | 26 | H F F | 0/13 | 433,825 | 1,908 | 9 | 2026-11-05 |
| Axis MF front-running: Dubai AnyDesk trades, brokers fined ₹10 lakh each (`axis-mf-frontrun`) | retired: past its window | COLD | fading | 25 | C H C C H H C | 0/0 | 311,088 | 2,248 | 7 | 2026-11-17 |
| Stockal: US shares sold without consent, swapped for Chinese microcaps; ₹100 cr+ alleged (`stockal-unauthorised-trades`) | retired: past its window | HOT | rising | 24 | H H H F H F H | 1/8 | 250,324 | 5,423 | 8 | 2026-11-12 |
| Samvat 2082: Sensex -11.9%, Nifty -11%, worst in 15 years (`samvat-2082-worst`) | retired: past its window | RISING | rising | 24 | R R F R | 79/100 | 357,785 | 2,201 | 8 | 2026-11-08 |
| AI trade cracks: Nvidia -$450 bn, Nasdaq -5.5%; FIIs buy ₹14,975 cr of India the same day (`ai-crash-india-inflow`) | retired: past its window | HOT | rising | 23 | H H H | 1/11 | 3,102,086 | 19,014 | 9 | 2026-11-08 |
| Videocon's Venugopal Dhoot declared personally bankrupt over ₹12,668 crore SBI dues (`videocon-dhoot-bankrupt`) | retired: past its window | HOT | rising | 22 | C H H H | 0/4 | 1,177,231 | 8,133 | 9 | 2026-11-10 |
| Airlines fly fewer, charge more: IndiGo passengers -4.7%, yield +34%; SC 'Don't travel by air' (via The Ken) (`airfares-fly-less-pay-more`) | retired: past its window | COLD | steady | 21 | C C C C C C C | 1/2 | 50,933 | 154 | 7 | 2026-11-16 |
| Ramayana: ₹499 cr worldwide in 4 days vs ₹4,000 cr bill for two films (`ramayana-box-office`) | retired: past its window | HOT | rising | 20 | H H H H H H H | 54/100 | 3,787,870 | 56,656 | 8 | 2026-11-15 |
| ₹89,000 cr of unclaimed shares with IEPF; Reliance biggest slice (Diwali-cleaning certificate reels) (`unclaimed-shares-iepf`) | retired: past its window | COLD | steady | 20 | C C H C C C C | 0/4 | 4,294 | 28 | 8 | 2026-11-23 |
| India's best week since Feb 2021: Nifty +8.6%, FIIs buy ~₹46,000 cr back after ₹45,162 cr October exit (`india-best-week-fii`) | retired: past its window | HOT | rising | 19 | H H H C H | 0/0 | 369,104 | 3,548 | 8 | 2026-11-14 |
| Novartis India: ~50 staff, ₹1,446 cr for 71%; open offer got 40 shares (via The Ken) (`novartis-india-ken`) | retired: past its window | COLD | rising | 19 | C C H C C C C | 0/6 | 59,817 | 892 | 6 | 2026-11-24 |
| ED raids CoinDCX and Delta: tokenised 'Apple, Tesla' routed abroad, alleged; $16M wallet loss two weeks earlier (`coindcx-ed-raid`) | retired: COLD on 2 checks running | COLD | steady | 18 | C C | 1/1 | 1,342,333 | 7,024 | 8 | 2026-11-18 |
| B.R. Shetty liable in $5.4 bn NMC fraud; sold Finablr for $1; BoB paid $600M (via The Morning Context) (`br-shetty-nmc`) | retired: past its window | HOT | rising | 18 | C F F C C H H | 0/10 | 2,367,391 | 94,986 | 7 | 2026-11-25 |
| Jio more customers, Airtel more money: ARPU ₹271 vs ₹218.8 (`airtel-vs-jio-arpu`) | retired: past its window | HOT | rising | 17 | C C C C C C H | 0/0 | 345,963 | 10,781 | 7 | 2026-11-26 |
| Jensen Huang quits Nvidia; ~$1.7 tn off since Oct peak; top Nasdaq 100 fund holding (`nvidia-huang-resigns`) | retired: past its window | HOT | fading | 16 | H H H H | 0/27 | 1,368,275 | 5,131 | 9 | 2026-11-17 |
| NSE banned brokers' digital gold, then picked Augmont for EGRs (via The Ken) (`nse-augmont-digital-gold`) | retired: past its window | COLD | steady | 16 | C C C C C C C | 0/0 | 370 | 3 | 7 | 2026-11-26 |
| Retail inflation 6.09%, past RBI's 6% ceiling; SBI 1-yr FD ~6.25% (`india-cpi-6pct`) | retired: COLD on 2 checks running | COLD | rising | 14 | C C | 0/5 | 500,942 | 2,991 | 8 | 2026-12-02 |
| Mahanadi Coalfields IPO: Coal India sells 10% of India's largest coal producer (opens 19 Nov) (`mahanadi-coalfields-ipo`) | retired: past its window | FLAT | rising | 13 | H H H H F F F | 16/70 | 95,334 | 639 | 8 | 2026-11-27 |
| Nvidia Q3 $115.8 bn, doubled; board won't reinstate Huang (`nvidia-q3-board-no-huang`) | retired: past its window | HOT | rising | 11 | H F H | 7/100 | 1,087,747 | 7,762 | 9 | 2026-11-20 |
| AI selloff abroad, India at a nine-month high on record FPI buying (`ai-selloff-india-rally`) | retired: COLD on 2 checks running | COLD | rising | 8 | H H H C C | 2/6 | 55,365 | 769 | 9 | 2026-11-30 |
| Silver ~65% off January's ₹4.2 lakh record; silver ETF inflows +57% in October (`silver-crash-65pc`) | retired: past its window | FLAT | fading | 7 | H H F F H F | 9/29 | 732,445 | 2,154 | 9 | 2026-11-27 |
| SEBI prosecutes Ketan Parekh over unpaid Rs 27 cr; court refused 91-day 9-country trip (`ketan-parekh-prosecution`) | retired: past its window | FLAT | fading | 4 | F F F | 0/10 | 4,824 | 11 | 7 | 2026-11-27 |

## Latest notes
- **Groww's F&O share of revenue falls to 45%; turns to IPOs and wealth (via The Arc):** 2026-10-22: 22 Oct: The Ken 'hostage to options'; Groww PAT ₹725 cr, F&O 44.8% of revenue; SEBI FY26 87.7% lose
- **India's 'sovereign' AI rented from Nvidia GPU clouds; E2E -36% from Oct high (via The Ken):** sent 15 Nov, 7/10, The Ken 14 Nov
- **Ola Electric closes its own stores for dealers; Q2 revenue -39% to Rs 421 cr (via The Morning Context):** sent 16 Nov, 8/10, The Morning Context 13 Nov
- **Yes Bank AT1 Rs 8,415 cr: SC restored the bonds; Yes Bank and RBI seek review:** sent 18 Nov, 8/10, Moneylife lead
- **CAG draft audit: BIS hallmark checks missed:** CAG draft: 2,194 of 5,020 AHC audits missed; 5,444 of 28,865 jewellers inspected 2024-25
- **CAG draft audit: BIS hallmark checks missed:** 2026-11-23: deep lane via Moneylife 22 Nov; 81% uninspected 2024-25
- **70% still in regular MF plans after direct default:** The Ken 19 Nov
- **Record ₹1.53 lakh crore margin trading book; SEBI weighs a cap:** Reuters/TMC 17 Nov
- **IndusInd fires ex-CEO Kathpalia, claws back pay from 2020:** desk 22 Nov
- **EPFO monthly PF payouts (SWP), 10% minimum balance, 2-month wait:** desk 22 Nov
- **SEBI asks intermediaries to stop publishing IPO GMP (advisory, 23 Nov):** sent 24 Nov, 9/10 (pick); Mahanadi GMP ₹3.65→₹0.45, retail 46%
- **NSEL pays 5,682 investors ₹1,950 crore, 42.34% of claims, 13 years on:** sent 24 Nov, 6/10 (deep)
- **Tata Sons board takes up listing on 30 Nov; RBI letter 16 Nov says list:** 2026-11-27: 27 Nov: Trusts moved Bombay HC; hearing Fri 3 pm
- **Tata Sons board takes up listing on 30 Nov; RBI letter 16 Nov says list:** 2026-11-28: 28 Nov: HC refused relief; board 30 Nov goes ahead; RBI deadline 12 Dec; next hearing 18 Jan
- **Rs 20,000 cr crypto forex chase; ED searched CoinDCX, Delta; no user protection (via The Ken):** sent 25 Nov, 7/10
- **PhonePe restarts IPO at $12-15 bn:** revived 25 Nov; FY26 loss Rs 2,792 cr
- **Gold falls 9.4% in nine days:** Delhi 24K 1,36,200 to 1,23,420
- **Gold falls 9.4% in nine days:** 2026-11-28: 28 Nov: Friday bounce to Rs 1,28,400; viral Rs 75,000 claim
- **Tata Steel-APL Apollo deal:** The Ken: ammo for Noel; Rs 2,100 vs 2,301.40
- **Flipkart CEO Kalyan Krishnamurthy exits; Walmart, kickback probe, IPO to 2028:** desk 27 Nov, 9/10 pick
- **$1 bn cap: Indians overpay for US-index ETFs (The Ken):** The Ken 26 Nov
- **SC closes unclaimed-money PIL; Rs 86,917 crore in RBI's DEA Fund:** sent 28 Nov, 8/10 (pick)
