---
title: "Confluence retrospective: Item Page's Q1FY27, two valid metrics and the mid-quarter cutover"
source_url: "internal://acme-ecomm/confluence/q2fy27__item-page-q1fy27-two-metrics-retrospective"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: confluence_page
---

# Confluence Retrospective: Item Page's Q1FY27, Two Valid Metrics, and the Mid-Quarter Cutover

**Author:** `maya.lindqvist` (Director PM US Conversion & Traffic, `assoc_100110`)  
**Status:** Published / Archived for Q2FY27 Review  
**Date:** 2026-05-11 (Refreshed for Q2FY27 mid-quarter reference following the v6 wrap-up)  
**Space:** US_CONV / View Item Page Surface  

---

## 1. Executive Summary & Context

Every time leadership asks *“how did the item page do last quarter (Q1FY27)?”*, the conversation immediately bogs down in definitional sand. Before we can answer whether the surface "did well," we have to explicitly state our terms, because the answer changes entirely depending on which of the two valid metrics you look at, and whether you account for the March 2 session-counting architectural change (`sessions_definition_version` 1 → 2) that fundamentally shifted our baseline.

As of today (July 20, 2026, sitting deep in Q2FY27), we are past the noise of Q1FY27 (which closed on 2026-04-30). This page serves as the single source of truth for the View Item Page surface's performance during Q1FY27, tying together the 6-iteration Item Page Iteration Program, the two legitimate metric definitions, and the load-bearing impact of the mid-quarter session cutover. 

*(Note from Maya: If you're looking for the Compass dashboard view, make sure your query isn't still hitting stale pre-aggregations, and keep in mind that unlike the checkout experiments owen.faust ran with `exp_2214`, our item page iteration program was a sequential series of shipped UI changes rather than an A/B test with a clean holdback — though we did have to disentangle them from the sitewide Nav Refresh holdback `exp_2215` that ran concurrently in March.)*

---

## 2. The Item Page Iteration Program (Q1FY27)

Across Q1FY27, the View Item Page surface shipped **6 distinct production iterations** under my team's roadmap. For tracking history, these span the transition from our legacy Aitable grooming cards over to Jira (part of the broader roadmapping consolidation project that nadia.esposito kicked off back in January). 

The 6 shipped iterations are:
1. **v1 Above-Fold Price/CTA Reflow** — Shipped **2026-02-05** (just one day after felix.arroyo’s 18% paid-search budget cut went live, which compressed our traffic baseline but sharpened visitor intent).
2. **v2 Reviews Section Reorder** — Shipped **2026-02-19**.
3. **v3 Image Gallery Zoom/Swipe** — Shipped **2026-03-05** (the first iteration to land *after* wei.hartono’s session-counting definition cutover).
4. **v4 Size/Fit Guidance Module** — Shipped **2026-03-19** (directly addressing a lingering Medallia VOC theme around sizing uncertainty in apparel categories overlapping with ines.delgado’s style catalog).
5. **v5 Cross-Sell Module Placement** — Shipped **2026-04-02**.
6. **v6 Sticky Add-to-Cart Bar (Mobile)** — Shipped **2026-04-16** (completing the H1 program right before we wrapped up our Q1 closing reviews with amara.shah and carlos.figueroa).

---

## 3. Two Valid Metrics, Two Different Questions

When people ask about item page performance, they usually confuse two completely different metrics built from `fact_traffic_daily`. Neither is wrong, but they answer fundamentally different questions. 

For Q1FY27, across approximately **235.3M product view sessions** (out of 379.5M total US sessions):

### Metric A: View-to-Cart Rate (`add_to_cart_sessions / product_view_sessions`)
* **What it measures:** Surface engagement and user intent to purchase after viewing an item. 
* **Q1FY27 Performance:** Moved from an average of **18.0%** (pre-cutover) to **19.9%** (post-cutover).
* **Raw Delta:** **+1.9pp** raw increase across the quarter.

### Metric B: Item-Page-Scoped Conversion (`orders / product_view_sessions`)
* **What it measures:** End-to-end efficiency for users who actually engaged with a product page.
* **Q1FY27 Performance:** **5.13%** for the full quarter (computed as `12.068M orders / 235.3M product view sessions`).
* **Why it differs from site conversion:** Standard site conversion (`orders / total sessions`) for Q1FY27 was **3.18%**. The item-page-scoped conversion is *intentionally larger* (5.13%) because its denominator excludes browse-only sessions, category-landing drop-offs, and footer/homepage bounces that never reached an item detail page. 

**Rule of thumb:** Use View-to-Cart when evaluating UX tweaks on the item page itself (like our v1–v6 iterations). Use Item-Page-Scoped Conversion when partnering with owen.faust on funnel economics or comparing product-engaged traffic against search relevance lifts (such as the in-flight `exp_2601` search re-ranking test).

---

## 4. The Load-Bearing Catch: The Mid-Quarter Session Cutover

Here is where casual analyses break down. On **2026-03-02**, wei.hartono deployed the session-counting update (`sessions_definition_version` 1 → 2), introducing rigorous bot/crawler filtering and multi-tab de-duplication across `fact_traffic_daily`. 

Because `product_view_sessions` and `add_to_cart_sessions` live inside those exact same daily traffic rows, **this architectural cutover mechanically affects both item-page metrics just as much as it affects the site-wide conversion rate.**

* **Pre-Cutover (Version 1: Feb 1 – Mar 1, ~29 days):** View-to-cart baseline averaged **18.0%**.
* **Post-Cutover (Version 2: Mar 2 – Apr 30, ~60 days):** View-to-cart averaged **19.9%**.
* **The Raw Move:** +1.9pp raw.

### Decomposing the +1.9pp Gain
If you just average the whole quarter together without adjusting for the cutover, you tell a lazy story. Our deep-dive data reconciliation shows:
1. **Mechanical / Definitional Bump (~+0.8pp):** Exactly like the sitewide conversion rate adjustment, filtering out invisible crawler traffic and multi-tab noise shrinks the session denominator, artificially lifting the ratio without a single user changing behavior.
2. **Real, Iteration-Driven Gain (~+1.1pp):** The genuine behavioral lift attributable to our iteration program (v1 and v2 shipped in the pre-cutover window; v3 through v6 shipped post-cutover, meaning their individual baselines must be evaluated against version 2).

> **CRITICAL WARNING:** Silently averaging the whole quarter across the March 2 cutover **overstates the real, iteration-driven gain by roughly 40% relative** (+1.9pp reported raw vs. ~+1.1pp true operational lift). Anyone putting the raw +1.9pp into an executive deck without mentioning the version shift is going to get called out by Finance during the MBR.

---

## 5. Open Follow-Up Questions for Q2 / H2

As we evaluate where to take the item page surface next—especially while juggling concurrent in-flight tests like maya.lindqvist's media carousel autoplay experiment (`exp_2618`, which has been dragging conversion slightly on its exposed arm) and owen.faust's search re-ranking (`exp_2601`)—we need answers to these three items for next quarter:

1. **Cross-Vertical Sizing Consistency:** Now that ines.delgado’s Style vertical and sanjay.bhatt’s Collectibles vertical are dealing with different catalog constraints, should our size/fit guidance module (v4) be modularized by sub-vertical, or kept as a global template?
2. **Listing-Page Expectation Mismatches:** Medallia verbatims continue to show that ~14% of Style and ~9% of Collectibles buyers experience a `listing-accuracy-gap` (photos/specs not matching the delivered item). Our item page layout today does nothing on its own to mitigate buyer expectation mismatches. Can we pull review-media highlights higher up the page as a partial fix?
3. **Attribution Isolation for H2:** Can wei.hartono build us a pre-packaged view that automatically normalizes session definition versions when running trailing 6-month retrospective queries, so we don't have to manually segment v1 vs v2 every time someone asks for a YoY comparison?

---

## Comments & Discussion Thread

* **amara.shah** *(Data Analyst, Finance/MBR, `assoc_100211`)* — 2026-05-12 09:15 ET  
  > Maya, thank you for putting this together. I’m updating the MBR appendix decks this morning and was about to use the raw +1.9pp figure until I saw your warning about the 40% relative overstatement. Saving this link in the master finance channel so nobody else repeats that. Quick check: does the 5.13% item-page conversion also need a version adjustment footnote?
* **maya.lindqvist** *(Director PM US Conversion & Traffic, `assoc_100110`)* — 2026-05-12 10:42 ET  
  > @amara.shah Yes! The denominator for item-page conversion is `product_view_sessions`, which lives in `fact_traffic_daily` right alongside total sessions. So version 2 applies there too. Stick a footnote pointing to `traffic_conversion_summary` carrying the definition flag forward.
* **owen.faust** *(Sr PM Checkout & Conversion, `assoc_100111`)* — 2026-05-12 14:03 ET  
  > Explains a lot. We ran into a similar version-confound nightmare when untangling the Checkout Simplify `exp_2214` results from the Nav Refresh rollout back in March. Good on you for documenting the cutover cleanly here. By the way, are we seeing any spillover from the autoplay carousel test (`exp_2618`) onto the item page exit rates yet? 
* **maya.lindqvist** *(Director PM US Conversion & Traffic, `assoc_100110`)* — 2026-05-12 15:20 ET  
  > @owen.faust Don't remind me. The autoplay test is dragging a bit on the exposed arm (-1.5%), which is why we haven't shipped it globally yet. It's sitting right alongside search re-ranking (`exp_2601`) as a net-zero wash on the dashboard for now. Will post a separate update once that reads out fully.

---
