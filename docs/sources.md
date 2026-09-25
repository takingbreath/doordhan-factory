# Deep-lane sources: research journalism our viewers mostly don't read

Use: the headline is the lead. We research the facts ourselves from open sources (filings, SEBI/RBI orders, annual reports, free coverage), never copy paywalled text, and credit the outlet in the caption when the story is theirs ("via The Ken").
`python3 pipeline/deep_leads.py` pulls the last 7 days of headlines from the top eight below. Checked 2026-09-25: every feed returned items without a login.

## Top 8 (most original, least likely our viewers have seen it)
| # | Source | Good at | Paywall | Headline feed |
|---|---|---|---|---|
| 1 | The Ken | original bank, fintech, consumer and startup deep-dives | hard | Google News `site:the-ken.com` (its own site blocks scripts) |
| 2 | The Morning Context | companies, governance, media long-form | hard | Google News `site:themorningcontext.com` (filter old items by date) |
| 3 | SEBI orders | enforcement orders: research analysts, AIFs, settlements; a primary source | none | https://www.sebi.gov.in/sebirss.xml (keep links with `/enforcement/orders/`) |
| 4 | Moneylife | investor protection, scams, regulator failures | partial | Google News `site:moneylife.in` |
| 5 | ET Prime | governance and insolvency investigations | hard | https://economictimes.indiatimes.com/prime/rssfeeds/69891145.cms |
| 6 | Reuters India exclusives | scoops | registration | Google News `site:reuters.com India (exclusive OR insight)` |
| 7 | The Arc | inside private tech and fintech | subscription (unconfirmed) | https://www.thearcweb.com/rss.xml |
| 8 | The Core (with The Signal) | listed companies, the "old economy" | partial | https://www.thecore.in/feed |

## Also useful (free; good for checking facts and for explainers)
- Zerodha The Daily Brief: https://thedailybrief.zerodha.com/feed
- Finshots: https://finshots.in/rss/
- freefincal (personal-finance data): https://freefincal.com/feed/
- Capitalmind: https://www.capitalmind.in/rss
- Entrackr (startup financials): https://entrackr.com/rss
- Inc42: https://inc42.com/feed/
- MediaNama (fintech and digital regulation): https://www.medianama.com/feed/
- Mint: https://www.livemint.com/rss/companies (also /rss/money, /rss/opinion)
- Business Standard personal finance: https://www.business-standard.com/rss/finance/personal-finance-10313.rss
- Hindu BusinessLine Portfolio: https://www.thehindubusinessline.com/portfolio/feeder/default.rss
- RBI press releases: https://www.rbi.org.in/pressreleases_rss.xml
- Short-seller alerts (Hindenburg closed Jan 2025): Google News `"short seller" India when:30d`

## Notes
- Google News links are redirects, and `when:7d` isn't strict; always filter by date. Space calls about 3 seconds apart, because cloud IPs get throttled.
- Dropped: Hindenburg (closed), Zerodha Varsity (educational, stale), Moneycontrol RSS (dead since 2024), small personal Substacks.
