---
title: "FullStory session-replay note: Homepage Hero Banner Refresh shows no measurable conversion effect"
source_url: "internal://acme-ecomm/fullstory/q2fy27__homepage-banner-refresh-no-conversion-effect-review"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: fullstory_session_note
---

**Author:** maya.lindqvist (Director PM US Conversion & Traffic)  
**Reviewers:** owen.faust, wei.hartono, amara.shah  
**Date:** July 20, 2026  
**System of Record Ref:** FullStory session-replay note (adapter: `fullstory_session_note`)  
**Scope:** US Market Homepage Replay Audit post-'Homepage Hero Banner Refresh' launch (shipped 2026-07-13)  

---

### 1. Executive Summary & Context

Following standard protocol after any major top-level UI change to our primary acquisition surface, the US Conversion and Traffic team conducted a routine qualitative and quantitative session-replay review across FullStory in the days following the July 13 deployment of the **Homepage Hero Banner Refresh** (owned by maya.lindqvist). 

To be entirely clear from the outset: we pulled these replays because it is standard operating procedure after every homepage release—not because we suspected a catastrophic breakdown or were trying to diagnose the broader Q2FY27 US conversion softness (which is driven by distinct mix-shift dynamics and traffic adjustments, as discussed extensively in recent WBR/MBR sessions). 

Our review of roughly 4,500 session replays across desktop web, mobile web, and app viewports between July 13 and July 20 yields a straightforward, anticlimactic conclusion: **the Homepage Hero Banner Refresh shows no measurable conversion effect**, either positive or negative. Furthermore, downstream funnel behavior—specifically click-through rates to item pages, search interactions, and add-to-cart rates—remains entirely stable and statistically indistinguishable from pre-launch baselines. Because the banner's scope is strictly confined to the homepage real estate, this lack of downstream contamination is entirely expected.

Crucially, this evidentiary source rules out the banner itself as any form of explanatory driver for the same week's US conversion fluctuations (such as the week-ending 2026-07-18 WoW drop from 3.24% to 2.86%, which is a separate device-mix and rate question for the WBR team, not a homepage layout regression). 

---

### 2. Operational Details & Replay Review Parameters

*   **Review Window:** July 13, 2026 (post-deployment, 14:00 ET) through July 20, 2026 (09:00 ET).
*   **Total Sessions Sampled:** ~4,500 filtered sessions (segmented across web, app, and store_kiosk).
*   **Device Breakdown of Replays Reviewed:**
    *   Desktop Web: 42% (~1,890 sessions)
    *   Mobile Web: 38% (~1,710 sessions)
    *   Native App: 17% (~765 sessions)
    *   Store Kiosk: 3% (~135 sessions)
*   **Primary Metrics Monitored:** Banner interaction rate (click/tap on new hero assets), scroll depth past the hero fold, bounce rate on initial landing, immediate navigation vector (search vs. category nav vs. item-page click), and ultimate session conversion.

#### Qualitative Observations on User Interaction
*   **Engagement with New Assets:** Users are rendering and viewing the refreshed hero graphics correctly across all standard breakpoints. The CSS flexbox adjustments and asset compression updates deployed on July 13 have rendered cleanly, with zero layout shift (CLS) regressions flagged in our automated Core Web Vitals monitors or visible in replays.
*   **Click-Through Behavior:** The click-through rate (CTR) on the primary hero CTA hovers at 4.1%, which is statistically flat relative to the legacy banner's trailing 30-day average of 3.9%. 
*   **Dwell Time:** Average dwell time on the homepage before navigating away or scrolling down is 14.2 seconds (vs. 13.8 seconds pre-launch). The variance is negligible.

---

### 3. Noise, Distractions, and Unrelated Dead Ends Encountered During Review

As is customary when pulling broad FullStory session segments, our analysts (with asynchronous input from wei.hartono and connor.blake) spent time chasing several unrelated rabbit holes that surfaced in the query feed. For the sake of institutional memory and to prevent future data auditors from barking up these same trees, they are documented below:

1.  **Looker-to-Compass Dashboard Migration Glitch:** Early on Monday morning (July 20), one of our junior analysts pinged the `#analytics-chat` Slack channel noting that Marketplace GMV figures for Q4FY26 looked "wrong" on a legacy view, showing $952.4M instead of the canonical restated $975.0M. As connor.blake quickly reminded the channel, that is simply the stale Compass PDT cache; the canonical BigQuery aggregate mart (`marketplace_gmv_summary`) has locked the $975.0M figure since the returns-timing reclass back in February 2006/early 2026. Nothing to do with the homepage banner.
2.  **Stray Medallia Verbatims on Item Pages:** While reviewing downstream item-page sessions, we noticed a minor cluster of shopper complaints regarding the *Item Page Media Carousel Autoplay* experiment (`exp_2618`), which Owen Faust and maya.lindqvist have been running since June 8. A few users left verbatims complaining that "the video just starts and it's annoying" or that the "page feels slower now." While `exp_2618` *is* currently showing an interim conversion drag of -1.5% on its exposed arm, this is entirely orthogonal to the homepage banner refresh. The homepage banner has no video elements and does not touch item-page media modules.
3.  **Kiosk Session Anomalies:** A handful of store-kiosk replays (`device='store_kiosk'`, 3% of our sample) showed users encountering awkward touch targets on secondary promotional sub-tiles underneath the main hero. However, these sub-tiles were untouched by the July 13 refresh; they belong to the legacy promotional grid maintained by the merchandising team. Filed a low-priority Jira ticket for the store operations team to review when they have cycles, but it does not impact digital conversion metrics.
4.  **Office Logistics & Standup Chatter:** In parallel with this review, the team spent an inordinate amount of time discussing office seating re-assignments on the 4th floor of the data building and coordinating who is bringing donuts to Wednesday's sprint planning. Standard operating noise.

---

### 4. Downstream Funnel Impact Analysis

To verify that the homepage banner refresh was not introducing subtle friction that failed to show up in top-line conversion but damaged deeper funnel flows, we cross-referenced FullStory paths with BigQuery aggregate marts (`fact_traffic_daily` and `traffic_conversion_summary`):

*   **Search vs. Browse Split:** Users landing on the homepage post-July 13 split 54% to category/browse navigation and 46% to direct search bar queries. This ratio matches our trailing 12-month baseline within a 0.5% band.
*   **Add-to-Cart Initiation:** Sessions that progressed from the homepage to an item page initiated an add-to-cart event at a rate of 19.1% across the July 13–20 window. This compares to 19.3% for the week prior (July 6–12) and sits comfortably alongside the post-cutover session definition v2 baselines established after March 2.
*   **Interaction with Concurrent US_CONV Experiments:** As noted in our mid-quarter reviews, two major experiments are actively running in the US conversion stream: *Search Relevance Re-ranking* (`exp_2601`, showing a clean +1.6% lift on its exposed arm) and *Item Page Media Carousel Autoplay* (`exp_2618`, showing a -1.5% drag). We verified via session tagging that users exposed to the new homepage banner were evenly distributed across the variant arms of `exp_2601` and `exp_2618`. There is no interaction effect or covariance between the homepage banner refresh and either search or media autoplay experiments.

---

### 5. Conclusion & Next Steps

The Homepage Hero Banner Refresh (shipped 2026-07-13) is functioning exactly as engineered. It refreshes the brand visual hierarchy for the summer campaign period without introducing layout bugs, latency, or conversion friction. 

*   **Action Items:**
    1.  Close out FullStory monitoring tag `fs_review_homepage_banner_q2fy27` as complete.
    2.  No further analysis required for this specific deploy; hand findings over to amara.shah for inclusion in the routine weekly MBR archive notes if requested, though it does not merit executive escalation given its neutral impact.
    3.  Continue monitoring the broader US conversion weekly trends—focusing our attention on device-mix shifts and the two live search/media experiments rather than revisiting the homepage banner.

---
