---
title: "Confluence page: ReWear Collective (sel_500204) crosses $1M trailing-90d GMV"
source_url: "internal://acme-ecomm/confluence/q2fy26__rewear-collective-resold-milestone-and-seller-tiering"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2025-07-15T12:00:00+00:00'
adapter: confluence_page
---

# Marketplace Team Space > Resold Sub-Vertical > Seller Milestones

**Author:** `victor.okonkwo` (SVP Marketplace)  
**Contributor:** `noah.kessler` (Sr PM Marketplace Resold)  
**Date:** 2025-05-15  
**Status:** Published  
**Space:** Marketplace Engineering & Strategy  
**Parent Page:** Q2FY26 Resold Growth Initiatives & Seller Pipeline

---

*Note from Noah (2025-05-15, 08:30 EST): Quick write-up on ReWear Collective hitting the $1M trailing-90d mark yesterday. Victor wanted this logged before our weekly Sync with Felix's org. Reminder for everyone: while it's a great milestone for them, keep eyes on the broader tiering definitions we locked down during the April MBR prep—let's not treat one seller's good quarter like an entire structural shift for the Resold vertical just yet.*

---

## Executive Summary & Milestone Context

Following the FY26 kickoff leadership sync and the close of our April business reviews (continuing the momentum we've tracked since carlos.figueroa’s data team locked down our core baseline validation checks back in February), we are logging an important individual seller milestone in our Resold sub-vertical.

As of **May 14, 2025**, **ReWear Collective (`sel_500204`)** has officially crossed **$1.0M in trailing-90-day GMV**. With this milestone, ReWear Collective moves solidly into our top-tier classification within the Resold ecosystem, placing them currently in the top 20 of all active Resold sellers on the Acme Marketplace platform.

To be clear and objective for our internal reporting: **this is an early, still-modest data point.** At this juncture, ReWear Collective’s performance reads strictly as one high-performing seller having an exceptional run on the platform, driven by strong seasonal demand for authenticated vintage denim and outerwear. It is **not** evidence of a broader category-wide structural surge across Resold as a whole (our aggregate Resold numbers remain stable around $97M for Q2FY26 QTD pacing, entirely in line with projections). 

---

## Seller Tiering & GMV Thresholds Reference

For context across the Marketplace team (especially for newer PMs onboarding to Style, Resold, and Collectibles), our current Marketplace seller-tiering GMV thresholds are structured across trailing-90-day performance as follows:

*   **Large / Top-Tier:** $\ge \$750,000$ trailing-90d GMV (e.g., ReWear Collective `sel_500204`, Cascade Denim Works `sel_500207`).
*   **Mid-Tier:** $\$150,000$ to $\$749,999$ trailing-90d GMV (e.g., Marrow Lane Vintage `sel_500203`, Harlow & Finch `sel_500147`).
*   **Small / Emerging:** $< \$150,000$ trailing-90d GMV (e.g., Thriftline Goods `sel_500205`).

*(Passing mention / baseline check: For comparison, mid-tier accounts like Harlow & Finch `sel_500147` continue to cruise along with completely flat, predictable volume—nothing exciting happening there, which is entirely fine and represents our healthy baseline traffic).*

---

## Fulfillment Economics: `ship_with_acme` vs. `seller_fulfilled`

ReWear Collective operates under the **`ship_with_acme`** fulfillment method, utilizing our DC network and integrated label generation. Looking at their unit economics compared to similar-sized peers using `seller_fulfilled`, a few operational observations are worth noting for future logistics alignment with ben.tanaka’s team:

1.  **Transit Times & Promise Reliability:** ReWear Collective’s on-time-to-promise (OTP) metrics hover around 94.2%, outperforming the average `seller_fulfilled` mid-to-large Resold cohort by roughly ~3.8 percentage points. Because they leverage `ship_with_acme`, their handling time from order creation to carrier handoff averages 1.1 days, whereas seller-fulfilled accounts in the same tier average 2.4 days due to manual drop-off lags.
2.  **Cost and Margin Trade-offs:** While `ship_with_acme` incurs standard carrier and fulfillment fees passed through our network, ReWear Collective’s lower return rate (clocking in at 4.2% versus the Resold category average of ~7.8%) more than offsets the fulfillment surcharge. Their customers experience fewer sizing and condition-mismatch escalations because Acme-managed outbound packaging reduces transit damage.
3.  **Support Contact Deflection:** Because tracking updates are automatically synced through the Acme customer portal for `ship_with_acme` participants, ReWear Collective generates 40% fewer Care contacts per 1,000 orders than comparable `seller_fulfilled` peers (such as Marrow Lane Vintage `sel_500203`, which still handles its own inquiries via third-party messaging). 

---

## Team Notes & Side Chatter

*   **[noah.kessler]** @victor - do we want to send them a swag box or feature them in the next seller newsletter? Let's check with camille.duarte when she has a moment, though I know she's heads-down on setting up the new Seller Pulse survey program over in `fact_seller_voc_responses`.
*   **[victor.okonkwo]** Let's hold off on special swag until they sustain the $1M tier for two consecutive quarters. Don't want to jinx it. Also, did anyone check if the Compass dashboard cached view is showing the updated Resold rollups correctly today? I heard amara.shah mentioned some lingering caching delays from the BigQuery mart refreshes last night.
*   **[amara.shah]** Compass is clear on my end, but make sure you're querying `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary` directly if you're pulling numbers for the weekly MBR deck. Don't use raw `fact_orders` for top-line cuts (remember convention 5!).
*   **[gabriel.stroud]** Speaking of logistics, DC sorting speeds at JOL1 are looking solid post-automation phase 1, so ship-with-acme partners shouldn't see any weird regional bottlenecks this week.

---
LEDGER
[{"date": "2025-05-14", "kind": "metric_shift", "vertical": "MARKETPLACE", "owner": "victor.okonkwo", "summary": "ReWear Collective (sel_500204) crosses $1M trailing-90d GMV and enters top-20 Resold seller tier"}]
```