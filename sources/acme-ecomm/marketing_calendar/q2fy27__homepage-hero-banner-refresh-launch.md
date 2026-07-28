---
title: "Marketing calendar: 'Homepage Hero Banner Refresh' launch"
source_url: "internal://acme-ecomm/marketing_calendar/q2fy27__homepage-hero-banner-refresh-launch"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: marketing_calendar_export
---

# Marketing Calendar Entry: Homepage Hero Banner Refresh Launch

**Event ID:** `camp_98240`  
**Event Name:** Homepage Hero Banner Refresh  
**Event Type:** `launch`  
**Vertical Code:** `US_CONV` (US/CA/MX Conversion + Traffic)  
**Market:** US, CA, MX (Omnichannel Digital)  
**Owner:** `maya.lindqvist` (`assoc_100110`, Director PM US Conversion & Traffic)  
**Start Date:** 2026-07-13  
**End Date:** 2026-07-27 (Scheduled creative rotation window)  
**Planned Spend USD:** $0.00 (Internal creative asset refresh, organic placement)  
**Actual Spend USD:** $0.00  
**Notes / Scope Rationale:** Strictly homepage-only scope covering the hero banner creative and grid layout refresh. Features zero item-page or search-surface overlap. Independent of the two in-flight US_CONV experiments (`exp_2601` Search Relevance Re-ranking and `exp_2618` Item Page Media Carousel Autoplay) started back on 2026-06-08.

---

## 1. Executive Summary & Administrative Context

As part of the Q2FY27 digital experience maintenance schedule managed under `maya.lindqvist`'s team, the **Homepage Hero Banner Refresh** (`camp_98240`) went live across our primary web and app entry points on **2026-07-13**. This routine creative update aligns with our quarterly cadence to update promotional real estate, elevate seasonal merchandising highlights, and maintain visual hygiene across our primary front door.

Per prior alignment in our weekly leadership syncs (building on the session definition cutover work by `wei.hartono` and our ongoing monitoring of US conversion pacing), campaign calendar entries for organic surface refreshes must explicitly delineate their operational boundaries to prevent misattribution during weekly business reviews (WBR) and monthly business reviews (MBR). 

### Scope Explicitness Boundary
* **Included Surfaces:** Homepage hero banner area (desktop top slot, mobile hero container, app landing carousel primary position).
* **Excluded Surfaces:** Item display pages (PDPs), search results pages (SRPs), category browse grids, and checkout flows. 
* **Surface Overlap:** **None.** This campaign does not touch item-page modules, nor does it interact with the ongoing Item Page Iteration Program artefacts that concluded their Q1/H1 push in May under `maya.lindqvist`.

---

## 2. Creative Rationale & Target Segment

### Target Audience
All visitors landing on the Acme homepage (`market IN ('US', 'CA', 'MX')` across `web` and `app` device channels). Because this is a top-of-funnel aesthetic and layout update rather than a personalized algorithmic recommendation engine, audience segmentation is universal.

### Creative Rationale
The previous hero banner layout, which had been serving since the late Q1 seasonal push, exhibited visual fatigue in heatmapping and session-recording analyses (reviewed informally via FullStory session notes). The refreshed creative framework transitions from a dense, multi-badge promotional stack to a cleaner, single-focus hero image accompanied by high-contrast typography and a simplified dual-CTA button layout ("Shop Best Sellers" / "Explore Acme+ Perks"). 

This design choice aims to reduce cognitive load during initial viewport rendering, particularly on mobile app viewports where vertical real estate is at a premium. It complements the ongoing membership onboarding work led by `derek.holloway` by maintaining secondary visual real estate for Acme+ value propositions without crowding out core retail merchandising.

---

## 3. Expected Engagement & Metric Impact

Because this campaign is restricted entirely to the homepage surface, expected engagement lifts are bounded exclusively to homepage-specific interaction metrics:
1. **Homepage Banner Click-Through Rate (CTR):** Expected modest positive lift (+15bps to +30bps) due to reduced visual clutter and clearer button hierarchy.
2. **Bounce Rate on Homepage Landings:** Expected minor downward pressure (-20bps to -50bps) as visitors more rapidly identify primary shopping pathways.
3. **Downstream Conversion / Site-Wide GMV:** **No direct attribution expected.** 

As noted in recent WBR discussions regarding the week-ending 2026-07-18 US conversion drop (where blended conversion shifted from 3.24% to 2.86%), calendar launches often face scrutiny regarding coincidental timing. The deployment of this banner refresh on Monday, 2026-07-13, coincided with a week experiencing a minor device-mix shift (app share rising from 28.0% to 37.6%) and a mild web-conversion softening (-0.14pp rate effect). Query logs and FullStory audits confirm that the banner refresh had **zero measurable correlation** with downstream item-page or search conversion. Confounders in that week are fully accounted for by device mix and ordinary weekly variance, as established in [roadmap-doesnt-explain-it].

---

## 4. Operational Chatter & Cross-Vertical Coordination

* **Martech Alignment:** `felix.arroyo`'s growth marketing team was briefed on the creative swap to ensure no conflicts with active paid-search landers (noting that paid search budgets remain disciplined following the 18% cut initiated back on 2026-02-04 under `camp_98244`).
* **Data Engineering & Analytics Check:** `amara.shah` and `wei.hartono` confirmed that BigQuery event logging (`fact_traffic_daily`) correctly captures standard banner interaction telemetry without requiring custom event schema modifications. No changes were made to `sessions_definition_version` (which remains at `2` following the March bot-filtering cutover).
* **Adjacent In-Flight Tests:** This campaign operates entirely independently of the two concurrent US_CONV experiments (`exp_2601` Search Relevance Re-ranking and `exp_2618` Item Page Media Carousel Autoplay) managed by `owen.faust` and `maya.lindqvist` since 2026-06-08. Those experiments govern search and item-page modules respectively and share zero code paths with the static homepage banner container.

---

## 5. Administrative Sign-off & Maintenance Log

* **2026-07-10:** Creative assets approved by `maya.lindqvist` and staged in CMS staging environment (`cms_node_hp_hero_v7`).
* **2026-07-13 04:00 EST:** Automated deployment executed successfully across US, CA, and MX production web/app frontends.
* **2026-07-20:** Mid-campaign health check completed. Traffic pacing normal; no rendering anomalies reported across mobile web or native iOS/Android clients. Scheduled for creative rotation on 2026-07-27.

---
