---
title: "WBR notes: week-of-07-18 US conversion drop, decomposed"
source_url: "internal://acme-ecomm/meetings/q2fy27__wbr-week-of-0718-us-conversion-drop"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: meeting_notes
---

# Weekly Business Review (WBR) — US Conversion & Traffic Deep-Dive
**Date:** Monday, July 20, 2026  
**Time:** 07:00 AM ET (Locked for the prior Sun-Sat week ending 2026-07-18)  
**Lead Presenter:** `maya.lindqvist` (Director PM US Conversion & Traffic)  
**Analytics Support:** `wei.hartono` (Analytics Engineer)  
**Attendees:** `felix.arroyo`, `carlos.figueroa`, `amara.shah`, `owen.faust`, `deborah.osei`, `connor.blake`, `giulia.romano`  

---

## 1. Routine Weekly Scorecard (US / CA / MX Markets)

Before diving into the US conversion drop observed for the week ending July 18, we reviewed the routine cross-market scorecard. As established in our standard WBR cadence following the session-counting definition fix (`sessions_definition_version = 2`) deployed back in March 2026, these figures reflect full-population aggregate data from `fact_traffic_daily` and `traffic_conversion_summary`.

*   **US Market:** 
    *   Sessions: **26.40M** (down from 26.80M the prior week, ending 2026-07-11)
    *   Blended Conversion Rate: **2.86%** (down from 3.24% the prior week)
    *   Orders: **755,038** (down from 868,320)
*   **CA Market (Reference Row):** 
    *   Sessions: ~3.15M 
    *   Blended Conversion Rate: **3.12%** (roughly flat week-over-week)
*   **MX Market (Reference Row):** 
    *   Sessions: ~2.01M 
    *   Blended Conversion Rate: **2.67%** (roughly flat week-over-week)

*Note on MX:* As `amara.shah` reminded the room during the pre-meeting sync, MX has run persistently ~0.4–0.6pp below CA and ~0.5–0.9pp below US across all 6 modeled quarters. This is a stable structural gap, not a new or worsening trend, and does not require an independent investigation this week. Our focus remains squarely on the sudden US weekly movement.

---

## 2. US Deep-Dive: Decomposing the -0.38pp Conversion Drop

The headline for the week ending 2026-07-18 is a **-0.38pp drop** in US blended conversion (frequently shorthand-referenced in the deck prep as "about 40bps"), moving from 3.24% down to 2.86%. 

`wei.hartono` walked through the device-mix shift and shift-share decomposition to separate mechanical traffic redistribution from genuine behavioral softening.

### Device Mix & Conversion Rates (WoW Comparison)

| Metric / Device | Week Ending 2026-07-11 | Week Ending 2026-07-18 | WoW Rate Change |
|---|---|---|---|
| **Web Share of Sessions** | 69.0% | 59.4% | -9.6pp |
| **App Share of Sessions** | 28.0% | 37.6% | +9.6pp |
| **Kiosk Share of Sessions** | 3.0% | 3.0% | 0.0pp |
| **Web Conversion Rate** | 4.00% | 3.76% | -0.24pp |
| **App Conversion Rate** | 1.50% | 1.50% | 0.0pp (steady) |
| **Kiosk Conversion Rate** | 2.00% | 2.00% | 0.0pp (steady) |

### Shift-Share Decomposition
Applying the standard two-factor decomposition (holding week-1 rates fixed for the mix effect, and holding week-1 shares fixed for the rate effect), Wei's pull breaks the -0.38pp drop down as follows:

1.  **Device Mix-Shift Effect:** **-0.24pp**. App session share jumped significantly from 28.0% to 37.6% week-over-week. Because app conversion sits structurally lower than web (~1.50% vs. ~3.76-4.00%), a massive influx of app traffic shifts the blended average downward even if every individual device's conversion rate remained completely unchanged.
2.  **Rate Softening Effect:** **-0.14pp**. Holding the baseline shares fixed, the actual conversion rates on web softened from 4.00% down to 3.76% (while app and kiosk rates held flat).

**Total Observed Move:** `-0.24pp (mix) + (-0.14pp rate) = -0.38pp`. 

---

## 3. Investigating Potential Drivers

We cross-referenced the conversion softening against our operational and product calendars to test potential root causes.

### A. Marketing Calendar Check
The only marketing-calendar event that launched during this specific window was the **"Homepage Hero Banner Refresh"** on **2026-07-13** (owned by `maya.lindqvist`). 
*   *Finding:* As noted in our FullStory session review and consistent with signal `[roadmap-doesnt-explain-it]`, this banner refresh was strictly homepage-scoped with zero item-page or search overlap, and it generated no measurable conversion effect. The shipped roadmap does *not* explain the -0.14pp web softening.

### B. In-Flight Experiments Check (`dim_experiment`)
We pulled the active experiments list for `US_CONV` during the week of July 18. Two major experiments are currently live, both having started back on **2026-06-08**:
1.  `exp_2601` (**Search Relevance Re-ranking**, owned by `owen.faust`): Showing an interim **+1.6% conversion lift** on its exposed arm.
2.  `exp_2618` (**Item Page Media Carousel Autoplay**, owned by `maya.lindqvist`): Showing an interim **-1.5% conversion drag** on its exposed arm.

*Discussion:* As `felix.arroyo` noted, these two experiments largely cancel each other out in aggregate dashboard views (consistent with signal `[offsetting-experiments]`). Neither can be cited as the *primary* driver of this week's drop—which is predominantly driven by the app session mix-shift. However, looking closely at the smaller real-softening component (-0.14pp web rate drop), the negative arm of `exp_2618` (autoplay carousel) is a plausible contributor. 

To triangulate this, `giulia.romano` pulled Medallia verbatims for item-page sessions during the 07-18 window. While overall VOC volume remains low and not yet a top-tier theme, she flagged a cluster of verbatim complaints mentioning:
*   *"The video just starts playing and it's annoying"*
*   *"Page feels cluttered now"*
*   *"Auto-scrolling and video loops make it hard to check product specs"*

**Conclusion on Residual:** We explicitly agreed *not* to force the -0.14pp real remainder into an overly tidy or fabricated single-cause narrative. It is real, modest, and partially tied to the user friction observed in `exp_2618`, combined with ordinary week-to-week noise.

---

## 4. Ordinary WBR Noise & Tangents

*   **Looker/Compass Migration Aside:** `connor.blake` interrupted mid-presentation to remind team leads that the legacy Looker dashboard migration to our Compass-analog BI tool is hitting caching delays in certain regional views. `amara.shah` muttered that her Q2 MBR deck had to be hand-refreshed twice because the Marketplace GMV widget was still caching the old pre-restatement Q4FY26 $952.4M figure instead of the canonical $975.0M (referencing `[gmv-restatement]`).
*   **Office Logistics & Coffee:** `owen.faust` complained that the 3rd floor kitchenette espresso machine has been throwing a water-intake error since Friday afternoon, prompting `maya.lindqvist` to suggest everyone migrate to the 2nd floor pantry where `derek.holloway` reportedly brought leftover pastries from the Membership team's Q3 planning breakfast.
*   **Standup Scheduling Note:** Next Monday's WBR sync will shift to 08:00 AM ET due to `carlos.figueroa`'s VP data alignment call with executive leadership.

---

## 5. Action Items & Next Week's Focus Areas

1.  **`maya.lindqvist` / `owen.faust`:** Monitor `exp_2618` daily; if the item-page media carousel autoplay negative drift (-1.5%) persists through Wednesday, prepare an early shutdown recommendation to protect web conversion rates ahead of August traffic.
2.  **`wei.hartono`:** Run a deeper cohort cut on the app session surge (+9.6pp WoW) to determine whether the traffic came from paid acquisition channels or organic push notifications, isolating if the lower-converting app traffic is a transient campaign artifact.
3.  **`giulia.romano`:** Continue tracking Medallia item-page verbatims specifically for `listing-accuracy-gap` and autoplay complaints to ensure the customer-facing signals do not cross our 5% escalation threshold.

---
