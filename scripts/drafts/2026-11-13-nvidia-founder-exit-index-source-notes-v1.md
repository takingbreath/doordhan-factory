# Nvidia / Nasdaq-100 tracker — verification v1

Status: DRAFT — SOURCE NOTES FOR UNAPPROVED HOOK/STORY. Checked 13 November 2026 IST. These are the writer's preliminary checks; they do not substitute for independent review of the eventual spoken script.

## 1. Immediate event: primary company statement

[NVIDIA Announces CEO Transition, 12 November 2026](https://nvidianews.nvidia.com/news/nvidia-announces-ceo-transition/).

The company's release states that Huang resigned as president, CEO and director effective immediately. CFO Colette Kress becomes interim CEO while continuing as CFO, pending a permanent appointment. The release gives no reason for the resignation. It says the board will consider internal and external candidates.

Access detail: web search returned the official release, but web open repeatedly failed. A direct Python standard-library HTTPS request to the same official URL returned HTTP 200 and the release body, which was read. Do not misrepresent a search snippet as full-text verification. No third-party allegation is needed to establish the transition.

[SEC 8-K, NVIDIA, filed 12 November](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000082/nvda-20261111.htm): search surfaced the board's acceptance on 11 November; full web open failed and direct retrieval returned 403. This filing was NOT fully read. The company release above independently supports the story's transition claims. Avoid asserting the acceptance happened on 12 November.

## 2. Indian fund exposure: newer issuer data

[Motilal Oswal Nasdaq 100 ETF — issuer product page](https://www.motilaloswalmf.com/mutual-funds/motilal-oswal-nasdaq-100-etf).

The public page's Portfolio Composition section, dated **31 October 2026**, lists Nvidia Corp Com at **8.02% of NAV**, behind Apple at 8.18%. Thus “about 8% at October-end” is supported for this ETF. The desk's 8.36% and largest-holding description refer to 30 September, not the newer October table.

The production page also contains inconsistent generic/template copy elsewhere (including a fund-of-funds label and midcap marketing). Do not use those parts as scheme definitions. The scheme-specific SID below establishes the actual ETF mandate. The linked portfolio workbook was not independently parsed; do not claim to have audited all holdings or current live exposure. Keep the monthly date and issuer attribution in visuals/source credits.

The development version of the issuer page still showed September data and was superseded for this claim by the production page. No statement about today's weight, all Indian funds, the investor's whole portfolio, or realised loss is supported by this monthly snapshot.

## 3. What the fund is mandated to do

[Motilal Oswal Nasdaq 100 ETF SID, dated 29 May 2026](https://www.motilaloswalmf.com/content/dam/motilal-mf/downloads/mf/sid/2026/may/SID_Motilal%20Oswal%20Nasdaq%20100%20ETF.pdf).

The scheme-specific cover describes replication/tracking of the Nasdaq-100 Total Return Index. The objective is corresponding index performance subject to tracking error, and the ETF risk section describes a passive technique investing in index constituents. This supports explaining that the mandate is to track, rather than independently re-underwrite Nvidia after the CEO transition.

This does not establish that the manager makes no transactions or has zero operational discretion. Changes in weights, creations/redemptions, expenses, cash, tracking error and other scheme provisions must not be collapsed into “it can never sell Nvidia.” The story makes no claim about actual trades after the announcement.

## 4. Is a founder/CEO exit an automatic index deletion?

[Nasdaq-100 Index Methodology, current PDF accessed 13 November](https://indexes.nasdaq.com/docs/Methodology_NDX.pdf).

The methodology describes modified market-cap weighting. Page 9's deletion policy addresses loss of eligibility, exchange changes, ineligible security/industry status, major corporate events making inclusion inappropriate, bankruptcy/cessation and certain spin-off conditions. CEO resignation is not specified as an automatic trigger. Pages 11–12 retain Nasdaq governance and reasonable discretion to preserve index integrity.

**Inference used in the proposed story:** a CEO departure alone does not automatically expel the stock; a tracker therefore can retain exposure after management changes. This is not a guarantee of continued membership, a confirmed post-event Nasdaq ruling, or a statement that index rules have no qualitative/discretionary overlay. No special Nvidia removal announcement has been independently established here. Recheck before final script/voice if developments change this premise.

## Excluded claims and factual boundaries

- No affair, espionage, misconduct or motive claim. The financial mechanism works without those allegations.
- No claim that the entire decline since the October high was caused by the resignation announced this week. Earlier falls preceded it.
- No market-cap-to-cash-loss equivalence, current ETF loss estimate, or invented investor example.
- No assertion that the company is now worthless, its competitive advantages disappeared, or passive investing is unsuitable. No buy/sell instruction.
- No creator view counts treated as verified facts or evidence that this framing will improve retention.

## Review state

The three desk options were considered: Nvidia has a new verified company event and an Indian portfolio mechanism; Anthropic's current demand reports do not warrant replacing the already pending accounting/supplier stories; the NSE-Augmont story needs care separating regulated EGRs from unregulated digital gold and authenticating the unit-size denominator. This recommendation is editorial judgement, not human story approval.

Research files were read-only. Save/push is limited to these two dated draft documents. Existing local edits and untracked drafts are preserved. Await approval of the displayed hook and English story before writing Roman Hinglish dialogue; independent editorial/final fact review applies after that, then human voice review. No production actions authorized.
