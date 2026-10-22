# sk05 eMudhra: real-image sources (captured 22 Oct 2026, ~22:15 IST)

All screenshots were taken with headless Chromium (Playwright), deviceScaleFactor 2. No paid credits were spent. The copyright call on each is Akhilesh's.

| File | Size (px) | Source URL | What it shows |
|---|---|---|---|
| emudhra_logo.png | 367x100 (RGBA, transparent) | https://emudhra.com/images/brandlogos/logo.png (the site header logo) | The official eMudhra corporate logo ("e" swirl + "emudhra / Trust Delivered"). This is the largest official version the site serves: there is no SVG, and there are no @2x or og-image variants (all 404). |
| emudhra_logo_3x.png | 1101x300 (RGBA) | same, Lanczos 3x upscale (local) | An upscale for use at size. The edges are slightly soft; under the old-TV look this is fine. |
| emudhra_digital_product_logo.png | 2000x460 (RGBA) | https://emudhra.com/images/home/product/emudhra-digital-logo.svg, rendered locally | The **eMudhra Digital** product-line logo (orange shield + wordmark). It is NOT the corporate logo; it is an extra. |
| chart_screenshot.png | 2560x2000 | https://www.tradingview.com/symbols/NSE-EMUDHRA/ (the "1 month" tab) | A 1-month chart from about 640 down to 345.60. Two cliffs on 21 and 22 Oct. Header: "345.60 INR −86.40 −20.00%". Tabs: 5 days −34.80%, 1 month −47.95%. |
| chart_screenshot_5d.png | 2560x2000 | same, "5 days" tab | A 5-day chart: flat at about 540, then the 21 Oct step down to 432 and the 22 Oct slide to 345.60. The clearest view of the crash. |
| chart_screenshot_1d.png | 2560x1800 | same, "1 day" tab | The 22 Oct intraday chart: open about 385–400, ending pinned at 345.60 (prev close 432.00). |
| chart_data.json | — | Daily: https://query1.finance.yahoo.com/v8/finance/chart/EMUDHRA.NS?range=2mo&interval=1d ; intraday 5-min: https://query1.finance.yahoo.com/v8/finance/chart/EMUDHRA.NS?range=5d&interval=5m | Yahoo OHLCV for 41 daily bars and 373 bars of 5-minute data. Key closes: 19 Oct 540.00; 21 Oct 432.00 (low = close = lower circuit); 22 Oct last 345.60 (Yahoo's daily close field was still null; regularMarketPrice and the day low are 345.60; open 385, high 404.90). Yahoo lists no bar for 20 Oct. |
| bugzilla_1970728.png | 2560x1800 | https://bugzilla.mozilla.org/show_bug.cgi?id=1970728 | Title "eMudhra: Invalid CRL signatures", Closed / RESOLVED FIXED, People expanded (Reporter: rob), and the first comment headed "Rob Stradling [Reporter]" with his description. |
| bugzilla_1970728_quarantine.png | 2560x1800 | same, scrolled to comments 1–2 | The eMudhra Preliminary and Full Incident Reports. Comment 2 contains the quarantine sentence (below). |
| emudhra_statement.png | 2560x2000 | https://emudhra.com/en/post/certificate-security-incident | Page top: "eMudhra Statement on Recent Certificate Security Incident", "Investigation ongoing", Last updated 22 October 2026, First published 20 October 2026, and Update 1. |
| emudhra_statement_18months.png | 2560x2000 | same, scrolled to "How it happened" | The 18-months / two-audit-cycles paragraph, plus "What is the actual impact" and the start of "There is no impact whatsoever on:". |
| emudhra_statement_noimpact.png | 2560x2000 | same | "There is no impact whatsoever on:" with the "digital signature and eSign services, in India..." list. |
| emudhra_statement_nobreach.png | 2560x2000 | same, Update 3 (21 Oct 2026) | Opening: "...our infrastructure was not compromised, and no data was breached." It also shows "Mid-2025 ... passed two independent audit cycles." |
| bt_exit_headline.png | 2160x2700 (1080-wide viewport) | https://www.businesstoday.in/technology/news/story/emudhra-to-exit-global-ssltls-certificate-business-after-security-incident-563155-2026-10-22 | The headline "eMudhra to exit global SSL/TLS certificate business after security incident", the standfirst, "Business Today Desk, Updated Oct 22, 2026 7:28 PM IST", the hero illustration and the opening paragraphs. |
| register_diginotar_2011.png | 2560x1560 | https://www.theregister.com/2011/09/20/diginotar_bankrupt/ | The headline "DigiNotar goes titsup: Disgraced certificate firm is sunk", the standfirst "Secrecy caused as much trouble as getting hacked", John Leyden, "Published Tue 20 Sept 2011 // 14:29 UTC", and the first paragraphs. The top ad banner was hidden and the bottom sticky ad cropped out. |
| mozilla_blog_header.png | 2560x1800 | https://blog.mozilla.org/security/2026/10/20/protecting-firefox-users-following-the-compromise-of-emudhra-intermediate-certificates/ | Mozilla Security Blog: "Protecting Firefox users following the compromise of eMudhra intermediate certificates", Firefox Security Team, October 20, 2026, and the first two paragraphs. |
| rob_stradling.jpg = rob_1.jpg | 460x460 | https://avatars.githubusercontent.com/robstradling?s=1000 (GitHub user robstradling, the crt.sh author's account) | A candid webcam-style head-and-shoulders shot: glasses, looking up and to the side, office ceiling behind. Sharp, but small and probably old. **The best available.** |
| rob_1_upscaled_1100.jpg | 1100x1100 | same, local Lanczos upscale + light unsharp | The size-up version of rob_1. |

## Verbatim quotes

**Bugzilla 1970728** (API: summary "eMudhra: Invalid CRL signatures", creator rob@sectigo.com, real_name "Rob Stradling", created 2025-06-05T20:05:08Z. Note: **2025**, not 2026.)
- Comment 0 (Rob Stradling): "https://crt.sh/mozilla-disclosures reports that eMudhra is currently serving 6 CRLs with invalid ECDSA signatures:"
- Comment 2 (Naveen Kumar ML, eMudhra, 2025-06-09, Full Incident Report), as shown in the screenshot: "The issue was initially reported via email by Sectigo on June 3, 2025, but the message was quarantined by internal filters and not seen."
- Same comment, timeline: "2025-06-03 10:05:00 : Sectigo sends initial email alert to problem reporting (quarantined and not delivered to inbox)"
- Same comment: "The initial email alert from Sectigo was quarantined and not noticed until a follow-up."
- Comment 14 (2025-07-05): "The issue was initially reported by Sectigo via email on June 3, 2025, but the message was inadvertently quarantined by internal filters and not seen by the compliance team."

**eMudhra statement** (Update 3, 21 October 2026)
- "The weak keys were the ones published to the browser root stores. The issue went undetected for about 18 months, through two independent audit cycles. The researcher was able to reverse-engineer the weak keys, reportedly with the help of AI-assisted tooling."
- "We revoked all eight intermediates the following day. No certificates had been issued from any of them, our infrastructure was not compromised, and no data was breached."
- "There is no impact whatsoever on:" / "Our digital signature and eSign services, in India or anywhere else in the world" (then emSigner, CertiNext, emCA, Privatrust, SecurePass) / "These products and services run on separate infrastructure and continue to operate normally. Customers using them do not need to take any action."
- "Mid-2025: The hierarchy was included in browser trust lists. It has since passed two independent audit cycles."
- "April 30, 2025: The eight intermediates were created in a Key Generation Ceremony."

**Business Today** (Updated Oct 22, 2026 7:28 PM IST): "The company's board took the decision on October 22. Chairman V Srinivasan said eMudhra had revoked the affected certificate authorities within 14 hours of discovering the issue, Moneycontrol reported on Thursday." Caption: "The incident came to light on October 17, when a researcher known as Wayne reported that the private keys of eight eMudhra intermediate certificates had been compromised."

## Not obtained / caveats
- Google Finance: the chart area renders blank in headless Chromium (its chart JS was blocked by ORB), so it was dropped in favour of TradingView.
- Rob Stradling: no conference or talk photo was found (web and YouTube searches turned up only a namesake musician). LinkedIn returned 429. The X @RobStradling avatar (via unavatar.io) shows a different-looking grey-haired man, so it was NOT saved: we can't confirm it is him.
- The DigiNotar office photo was not attempted (time). The Register's article page has no lead image.
