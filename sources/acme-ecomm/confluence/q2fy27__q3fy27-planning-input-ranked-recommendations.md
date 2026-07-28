---
title: "Confluence planning input: ranked recommendations for Q3FY27, drawing on the quarter's cross-cutting findings"
source_url: "internal://acme-ecomm/confluence/q2fy27__q3fy27-planning-input-ranked-recommendations"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: confluence_page
---

# Confluence planning input: ranked recommendations for Q3FY27, drawing on the quarter's cross-cutting findings

**Author:** `carlos.figueroa` (VP Data & Analytics, `assoc_100060`)  
**Date:** July 20, 2026  
**Status:** DRAFT / INPUT TO Q3FY27 PLANNING RITUAL  
**Target Audience:** Executive Leadership, Vertical SVPs, Product Leads (`felix.arroyo`, `hannah.brennan`, `victor.okonkwo`, `renee.kowalski`, `ben.tanaka`)

---

## Purpose and Framing

As we approach the Q3FY27 planning cycle, this document synthesizes cross-cutting findings from our data marts, experimentation readouts, user feedback streams (`fact_voc_responses` and `fact_seller_voc_responses`), and weekly review sessions. 

*Crucial housekeeping note:* Per our standard operating rhythms, this document represents **input** and analytical synthesis from standing cross-vertical visibility. It is not a mandate, a closed verdict, or a substitute for vertical roadmapping. Other leaders are expected to weigh these findings, data points, and recommendations against their own team backlogs, resource constraints, and commercial priorities. 

Before diving into the substantive recommendations, I want to acknowledge a few logistics: the Compass dashboard migration is still showing some cached caching discrepancies (reminding everyone of the Q4FY26 Marketplace GMV restatement from $952.4M to the canonical $975.0M mart figure), and the office AC on Floor 4 is still making that strange whistling sound that distracts the analytics engineering pod. Also, kudos to the team that pulled together the data for today's MBR-prep sync with `deborah.osei`—our $7.62B annualized run-rate continues to outpace the $7.53B fiscal target, even as we navigate the US conversion headwinds detailed below.

---

## Summary of Core Cross-Cutting Findings (Q2FY27 QTD)

Reviewing our performance through 81 of 92 days in Q2FY27 (closing in on our July 20 snapshot):
1. **Total Digital & Marketplace GMV:** Pacing strongly at a $7.62B run-rate against our $7.53B FY27 target (101.2%), driven primarily by Marketplace outperformance ($3.89B run-rate vs. $3.32B target).
2. **US Conversion Headwinds:** US conversion is sitting at 3.22% QTD (behind our 3.35% target), with recent weekly volatility—such as the drop from 3.24% to 2.86% for the week ending July 18—requiring careful decomposition rather than panic, as mix-shift to mobile app accounts for the majority of the variance alongside a modest real web softening.
3. **Marketplace & Seller Dynamics:** Marketplace GMV remains stellar, but our sub-vertical wallet-share shifts (Style decelerating to +6.1% YoY while Resold surges +90.9% and Collectibles surges +372.7%) have created structural friction, specifically around new-seller onboarding survival and authentication bottlenecks.
4. **Membership Retention & Benefits:** Acme+ is pacing well at 14.62M active members (tracking toward 15.05M at exit vs. 14.8M target), with annual renewal rates holding strong at 87.2% (beating our 86.0% target). However, stark gaps remain in benefit awareness—most notably with the streaming bundle.

Drawing on these findings, I propose **three ranked recommendations** for Q3FY27 investment, followed by a **fourth item framed strictly as a decision to make** (not a pre-baked recommendation).

---

## Ranked Recommendations for Q3FY27

### 1. Fund a Cross-Vertical 'Listing Accuracy' Initiative
* **Rank:** #1 (Highest Cross-Cutting ROI)
* **Target Metric:** Style, Resold, and Collectibles return rates; reduction in buyer-side `listing-accuracy-gap` VOC theme share.
* **Evidence Chain:** 
  Drawing on our cross-cutting Medallia VOC analysis (`fact_voc_responses`), the `listing-accuracy-gap` theme (where buyers report that item photos, descriptions, or specifications do not match true scale, condition, or physical attributes) sits at a stubborn, non-trivial share across our commercial landscape: **Style 14%**, **Resold 12%**, **Collectibles 9%**, and **B2B 22%** (where bulk buyers face severe spec-sheet and pallet-configuration mismatches). 
  I haven't lined this up against each vertical's current Jira backlog myself (Style under `ines.delgado`, Resold under `noah.kessler`, Collectibles under `sanjay.bhatt`, B2B under `malik.hendon`) — flagging the pattern here so it doesn't quietly fall through the cracks between four separate planning conversations; whoever scopes Q3 should check it against their own board directly.
* **Proposed Ownership & Scope:** 
  Assuming this doesn't already overlap with something in flight, a natural sponsor pairing would be `victor.okonkwo` (SVP Marketplace, spanning the retail sub-verticals) and `felix.arroyo` (SVP Product & Growth), with `camille.duarte` (Sr PM Marketplace Seller Experience, listings-side) as the likely operational lead given her surface remit, coordinating with `malik.hendon` for the B2B catalog slice. Scope would introduce standardized listing attribute validation rules and clearer spec comparison modules before publish, pending confirmation this isn't redundant with existing work.

### 2. Kill or Redesign 'Item Page Media Carousel Autoplay' (`exp_2618`)
* **Rank:** #2 (Immediate Corrective Action / Waste Reduction)
* **Target Metric:** Recovery of item-page conversion rate and mitigation of the real-degradation component identified in recent WBR conversion reads.
* **Evidence Chain:** 
  As noted in our recent WBR conversion-drop reads following the week ending July 18, our US conversion softening cannot be waved away as mere noise. While part of the drop is structural device-mix shift (app share rising from 28.0% to 37.6%), there is a real, measurable web-conversion degradation component. 
  When cross-referencing our active experiment ledger, "Item Page Media Carousel Autoplay" (`exp_2618`, owned by `maya.lindqvist`, started June 8, 2026) is currently showing a **-1.5% conversion drop on its exposed arm**. While running concurrently with "Search Relevance Re-ranking" (`exp_2601`, which is +1.6% and roughly washes out the topline dashboard view), `exp_2618` represents a classic "masked trend" where a well-intentioned feature backfires on the shopper experience. FullStory session notes and Medallia item-page verbatims from mid-July explicitly highlight customer annoyance ("the video just starts and it's annoying", "page feels slower now"). 
* **Proposed Action:** 
  Kill or immediately redesign `exp_2618` ahead of Q3. Stopping this test's negative exposure bleed will recover a vital component of the real-degradation drag on our product detail pages, directly supporting `maya.lindqvist`'s ongoing UX stabilization work.

### 3. Launch a Targeted Streaming-Benefit Awareness Push
* **Rank:** #3 (High-Leverage CLTV / Retention Play)
* **Target Metric:** Acme+ annual renewal rate (pushing pacing from 87.2% closer to a stretch 88.5%).
* **Evidence Chain:** 
  Our membership analytics mart and member CLTV builds (`member_cltv`) clearly demonstrate that benefit adoption drives retention: members using 2+ Acme+ benefits renew at **95%**, compared to only 71% for free-shipping-only members. 
  Furthermore, our analysis of the streaming bundle (transitioned to partner Reelstream on June 1, 2026, following the earlier Vidora partnership) reveals a powerful retention anchor: members in the streaming-bundle-aware cohort exhibit a **93% annual renewal rate**. However, our recent benefit-adoption analysis highlighted a glaring disconnect: **only 34% of members are actually aware** they possess this benefit. Following the success of the "Benefit Onboarding Carousel" experiment (`exp_2556`, managed by `derek.holloway`, which drove a +9pp lift in 30-day awareness), we have proof that awareness directly unlocks the higher renewal tier.
* **Proposed Ownership & Scope:** 
  Owned by `derek.holloway` and sponsored by `renee.kowalski` (SVP Membership), launch a dedicated, targeted email and in-app awareness push specifically aimed at single-benefit (free shipping only) members to drive streaming benefit activation before Q3 renewal waves peak.

---

## DECISION TO MAKE (Not a Pre-Baked Recommendation): Collectibles New-Seller Authentication-Friction Trade-Off

Rather than quietly resolving a major strategic tension within this document, I am explicitly flagging a fourth item as an open **Decision to Make** for the upcoming planning conversation between `victor.okonkwo`, `lucia.ferreira` (Trust & Safety Lead), and `sanjay.bhatt`:

* **The Tension:** 
  Our seller-ops reviews and new-seller funnel analyses (`dim_seller` panel cross-referenced with `fact_seller_voc_responses` via our new "Seller Pulse" survey stream) have laid bare a stark trade-off in the Collectibles sub-vertical. 
  The **"Acme Verified" / GradeSure authentication requirement** (launched September 8, 2005; badge shipped to 100% of listings on November 20, 2005) is an undisputed, proven **buyer-trust win**: it successfully drove Collectibles' return rate down from its painful Q3FY26 peak of **11.2%** to a healthy **5.4%** in Q2FY27, protecting a booming $91.2M/quarter category.
  *However*, the exact same requirement operates as a severe **seller-acquisition and retention drag**. While Style and Resold new sellers reach listing 10 at healthy rates of 48% and 46% respectively, **only 24% of new Collectibles sellers reach listing 10** (with 46% churning out before even reaching listing 5). Furthermore, seller-side VOC data (`fact_seller_voc_responses`) shows that `authentication-friction` is the dominant complaint among Collectibles onboarding respondents at **~38%** of verbatims (compared to ~5% in Style and ~6% in Resold).
* **The Strategic Dilemma:** 
  Removing the authentication requirement is **not free**—it would immediately reinject counterfeit risk and undo our hard-won return-rate improvements. Conversely, maintaining status quo strangles our new-seller acquisition funnel in a category that is otherwise our fastest-growing percentage-wise (+372.7% YoY in Q1FY27).
* **Next Steps for the Planning Conversation:** 
  Instead of defaulting to either extreme, we recommend bringing a scoped pilot to the planning table: **expedited and financially subsidized GradeSure authentication for a new seller's first 10 listings**, effectively bridging the cost-and-latency gap during the critical early onboarding window without compromising our catalog-integrity standards.

---

## Review & Attendees

This document has been shared for asynchronous review and will be discussed in the upcoming cross-vertical planning syncs. Reviewers and stakeholders include:
* `deborah.osei` (CEO)
* `felix.arroyo` (SVP Product & Growth)
* `hannah.brennan` (SVP Customer Care)
* `victor.okonkwo` (SVP Marketplace)
* `renee.kowalski` (SVP Membership)
* `ben.tanaka` (SVP Supply Chain & Fulfillment)
* `nadia.esposito` (Head of Product Operations)
* `maya.lindqvist`, `owen.faust`, `sanjay.bhatt`, `camille.duarte`, `derek.holloway` (Vertical PMs)

---
*Revision history: v1.0 published 2026-07-20 by `carlosa.figueroa` ahead of Q3FY27 executive planning review.*
