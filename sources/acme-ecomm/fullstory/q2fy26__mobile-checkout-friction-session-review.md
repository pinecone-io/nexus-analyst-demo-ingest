---
title: "FullStory session-replay note: mobile checkout friction, US conversion baseline"
source_url: "internal://acme-ecomm/fullstory/q2fy26__mobile-checkout-friction-session-review"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2025-07-15T12:00:00+00:00'
adapter: fullstory_session_note
---

# FullStory Session Replay & UX Friction Audit: US Mobile Checkout Baseline Review
**Author:** maya.lindqvist (Director PM US Conversion & Traffic, Product, assoc_100110)  
**Team:** US Conversion & Traffic / View Item Page & Checkout Funnel Taskforce  
**Date:** 2025-07-15  
**System of Record:** FullStory Qualitative Replay Cohort (Q2FY26 / Period Ending July 2025)  
**Scope:** US Market Mobile Sessions (`device='app'` and mobile web `device='web'`, screen-width < 768px)  
**Baseline Target Context:** Q2FY26 conversion tracking toward the corporate quarterly blended objective (~3.00% across total traffic).

---

## 1. Administrative & Environmental Notes

*   **Jira Ticket Reference:** `USCONV-4482` (Internal UX Audit: Mobile Checkout Funnel Leakage Points — Q2FY26 Review Cycle).
*   **Aitable Reference:** `ATBL-8819` (Mobile Cart Drop-off Log — Legacy pre-consolidation record; note that Nadia Esposito's team is still slowly migrating these over to Jira following the 2026-01-15 roadmap consolidation mandate, though historical cards remain readable).
*   **Looker Dashboard Quirk / Compass Migration Aside:** A quick reminder to the team—if you're pulling session metrics alongside these qualitative notes today, make sure you are querying the flat BigQuery base tables (`nexus-analyst-demo.acme_ecomm.fact_traffic_daily`) rather than poking around the legacy nested paths. Amara Shah in Finance caught someone trying to query a phantom dataset path (`acme_ecomm.marts.membership.*`) in Compass yesterday, which threw syntax errors until Wei Hartono redirected them to the flat structure. Also, for anyone still checking Q4FY26 Marketplace figures in Compass, bear in mind the Q4 Marketplace GMV cache still flashes the unadjusted flash-report figure ($952.4M) unless you force-refresh the cache against the canonical $975.0M mart table. Keep that in mind when cross-referencing conversion drop-offs against seller-side traffic spikes.
*   **Team Logistics & Chatter (Ignore if looking for pure metrics):** 
    *   *From Slack aside (assoc_100110 & assoc_100111):* Owen Faust mentioned he's still tied up finalizing scoping for his upcoming Q1 push, but wanted us to check if any of these mobile friction notes overlap with search result clicks. Told him search is cleaner this month, though mobile header real estate remains cramped.
    *   Office AC on the 4th floor is acting up again. If anyone's sitting near the east wall pods, bring a sweater or relocate to the collaboration booths by the cafeteria.
    *   Reminder: Friday team lunch at the taco truck by the loading dock. Bring cash or use the app, but don't expense it to the US Conversion travel budget—finance flagged last week's catering receipts.

---

## 2. Methodology & Cohort Parameters

This session-replay review aggregates a randomized, statistically representative sample of **4,500 mobile session replays** collected between **2025-05-01 and 2025-07-10** (spanning the active Q2FY26 window). 

Unlike our aggregate quantitative marts (`fact_traffic_daily`), which track full-population pre-aggregated sums, these qualitative FullStory sessions are inspected manually and via heuristic anomaly clustering to diagnose *why* users bounce at the cart-to-checkout boundary.

*   **Total Replays Sampled:** 4,500 sessions (filtered for cart abandonment where `checkout_started_sessions > 0` but `orders == 0`).
*   **Device Breakdown in Sample:**
    *   iOS Safari (Mobile Web): 42%
    *   Android Chrome (Mobile Web): 38%
    *   Acme Native iOS App (`device='app'`): 12%
    *   Acme Native Android App (`device='app'`): 8%
*   **Market Filter:** US Market only (`market='US'`). Canada and Mexico are tracked in separate cohorts under separate regional leads to account for differing carrier latencies and local carrier billing integrations.

---

## 3. Key Qualitative Observations (Exploratory Groundwork Only)

*Disclaimer: The observations below represent purely qualitative exploratory findings from session replays. No formal experiment ticket (such as an `exp_` designation) has been cut for these items yet, and no final product decision or roadmap commitment has been made. This document is intended solely as qualitative groundwork for future design discussions, maintaining a clear separation from Owen Faust's downstream checkout work slated for early 2026.*

### Observation A: Excessive Form Fields and Input Fatigue on Mobile Web
*   **Behavioral Pattern:** In approximately 31% of abandoned mobile web checkout sessions, users reach the primary billing/shipping address screen and spend upwards of 45 seconds interacting with individual form fields (First Name, Last Name, Address Line 1, Address Line 2, City, State, Zip Code, Phone Number). 
*   **FullStory Replay Indicators:** Rapid back-and-forth toggling between the numeric keyboard and standard alphanumeric keyboard on iOS devices; repeated clearing and re-typing of fields due to strict inline validation errors triggered by trailing whitespace (e.g., accidental space characters appended by mobile auto-correct after entering zip codes).
*   **Qualitative Context:** While our overall US conversion rate hovers steadily around our quarterly targets (tracking near the ~3.00% baseline for Q2FY26), mobile web users exhibit a significantly steeper drop-off between step 1 (shipping) and step 2 (payment) than native app users, who benefit from saved native keychain autofill.

### Observation B: Address-Autocomplete Misfires and Dropdown Trap
*   **Behavioral Pattern:** Users typing street addresses into the primary address-lookup box frequently trigger the third-party address-autocomplete API widget. In roughly 14% of observed replays where the widget triggered, the first suggestion provided by the dropdown did not match the user's specific apartment or suite number, or forced an invalid truncated format.
*   **FullStory Replay Indicators:** Users attempt to tap the dropdown suggestion, find that the suite number field was bypassed or greyed out, and subsequently spend 15–30 seconds attempting to manually click back into the address line to edit the text. A significant fraction (~40% of those who experience this specific misfire) abandon the session entirely rather than clearing the field to type the address manually line-by-line.
*   **Qualitative Context:** This matches anecdotal themes popping up concurrently in buyer-side Medallia verbatims (`fact_voc_responses`), where mobile shoppers express mild frustration with "glitchy address boxes," though it does not yet register as a high-severity system-wide alert.

### Observation C: Confusing Shipping-Method Toggle Interaction
*   **Behavioral Pattern:** On the delivery selection accordion, mobile users are presented with standard shipping, expedited shipping, and local pickup options (where applicable based on inventory at nearby DCs or stores like our local fulfillment nodes). In replays, users frequently tap the radio button for expedited shipping, but the dynamic estimated delivery date (EDD) text label updates with a slight 300ms render delay.
*   **FullStory Replay Indicators:** Users tap the expedited shipping option, observe no immediate visual feedback due to the render lag, tap it a second time (accidentally toggling it back to standard shipping), and express visible hesitation by scrolling up and down the shipping tier list before proceeding with an incorrect shipping selection or abandoning the funnel.
*   **Qualitative Context:** This UI stutter is particularly pronounced on mid-tier Android devices running Chrome under fluctuating network conditions. Gabriel Stroud's fulfillment network team has been hard at work rolling out DC sortation automation improvements (such as the recent enhancements at FON2 and JOL1), but downstream front-end rendering of promise dates on mobile remains sensitive to client-side DOM reflows.

---

## 4. Cross-Reference & Noise Check

*   **Relationship to Existing Metrics:** It is vital not to conflate these mobile web checkout friction observations with broader macro trends. For instance, our session traffic in the US has experienced minor fluctuations, but as Wei Hartono's engineering notes remind us, the major structural shift in our session counts occurred back on **2025-03-02** when the bot/crawler filtering fix shipped (`sessions_definition_version` moved from `1` to `2`). Any historical comparison of session volumes between early Q1FY26 and our current Q2FY26 baseline must account for that cleaning protocol.
*   **Separation from Marketplace and Seller Workstreams:** None of these checkout replays involve Marketplace 3P transactions or seller-fulfilled listings managed through Camille Duarte's seller experience workflows. Marketplace buyer flows route through separate cart modules, and while items from categories like Collectibles or Style appear in mixed carts, the checkout friction observed here is strictly platform-wide retail web/app infrastructure.
*   **No Overlap with In-Flight Experiments:** Readers reviewing this note should take care not to link these observations to active experiments. For example, the early foundation work and historical metrics from experiments like the "Verified Badge Prominence" test (`exp_2401`) run by Sanjay Bhatt in Marketplace last fall are entirely orthogonal to mobile checkout UI flows. Similarly, future checkout iteration projects that Owen Faust's team may or may៉ not pick up down the line are out of scope for today's exploratory review.

---

## 5. Next Steps & Action Items (Exploratory Only)

1.  Archive representative session IDs (`fs_sess_99281`, `fs_sess_88302`, `fs_sess_11409`) in the US Conversion team's internal documentation repository for future UI/UX design sprints.
2.  Coordinate with Amara Shah to check if upcoming MBR prep decks require any qualitative callouts regarding mobile form-field abandonment, keeping in mind that quantitative confirmation must always be pulled directly from `fact_traffic_daily` rather than estimated from replay samples.
3.  Continue monitoring session replays weekly as we approach the back half of Q2FY26, ensuring we maintain a clean separation between routine browser-engine rendering quirks and systematic UX blockers.

---
