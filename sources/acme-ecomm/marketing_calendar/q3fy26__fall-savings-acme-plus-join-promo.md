---
title: "Marketing calendar: 'Fall Savings' Acme+ join promo"
source_url: "internal://acme-ecomm/marketing_calendar/q3fy26__fall-savings-acme-plus-join-promo"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2025-10-15T12:00:00+00:00'
adapter: marketing_calendar_export
---

# Marketing Campaign Specification: Fall Savings Acme+ Join Promo

**Event ID:** `camp_90214`
**Owner:** `simone.laurent` (Director PM Membership, assoc_100150)
**Vertical:** MEMBERSHIP (Acme+)
**Target Run Dates:** 2025-09-20 through 2025-10-15
**Planned Spend:** $450,000.00 USD
**Actual Spend (Current Estimate):** $442,150.00 USD
**Status:** Executing / Active (Scheduled close matching snapshot boundary)

---

## 1. Executive Summary & Campaign Context

Following the early Q3FY26 strategic alignment reviews and the stabilization work across our operational pipelines—including the resolution of the recent `marketplace_gmv_summary` warehouse DAG hiccups back in June—the Membership team is launching the **'Fall Savings' Acme+ join promo** (`camp_90214`). This promotion is specifically designed to capture high-intent non-members browsing our digital storefronts during peak fall shopping prep, bridging the seasonal gap between summer wind-down and the November holiday build-up (Q4FY26).

As noted by renee.kowalski during our cross-vertical syncs, member acquisition velocity needs a mid-tier promotional push to hit our stretch targets for the fiscal year, particularly given the ongoing rollout of the Vidora-backed streaming bundle launched back in June (2025-06-01). While our member base has benefited from steady baseline additions, this campaign targets immediate conversion lifts among visitors who browse frequently during seasonal preparation but abandon checkout or sign up for standard guest checkouts without realizing the recurring value of an Acme+ annual or monthly membership.

---

## 2. Target Audience & Segment Definition

- **Primary Target Segment:** Non-members visiting US, CA, and MX web and app platforms with $\ge$ 3 product-view sessions over a 14-day rolling window during the fall shopping preparation cycle (home goods, seasonal apparel transitions, and early gifting research).
- **Behavioral Trigger:** Real-time modal injection on cart-view and checkout-entry pages for non-members exhibiting basket sizes over $75.00 USD.
- **Exclusions:** Existing active Acme+ members, paused or cancelled members within their 90-day win-back cooling period, and internal test accounts.

*Aside on cohort attribution:* As we tag incoming acquisition channels for the wider member database (`dim_member`), incoming signups from this push will carry the specific `acquisition_channel = 'fall_savings_promo_q3fy26'` tag. For instance, new signups such as mem_1000640 'Oskar'—who registers during the active window of this exact promo—will be ingested into `dim_member` under this attribution tag for future longitudinal analysis, ensuring we can cleanly separate promotional joiners from organic search or checkout-checkbox acquisitions down the line. (Note: any evaluation of Oskar's subsequent multi-benefit adoption or renewal behavior belongs to much later cohort reads in future quarters, far outside the immediate scope of this campaign setup).

---

## 3. Channel Mix & Tactical Execution

The campaign leverages a multi-channel digital approach coordinated with martech and site merchandising:

1. **On-Site Display & Interstitials (40% of budget):** 
   - Dynamic hero banners across US_CONV category pages (managed via maya.lindqvist's team touchpoints).
   - Exit-intent modals offering a discounted first-month entry rate ($4.99 trial converting to standard $99/yr annual or $12.99/mo).
2. **Paid Search & Social Retargeting (35% of budget):**
   - Retargeting ad units across Google and Meta targeting users who interacted with seasonal merchandise landing pages but did not convert.
3. **Email & Lifecycle Marketing (15% of budget):**
   - Automated sequence triggered for signed-in guest users who abandon carts containing $\ge$ 2 items during the promo window, highlighting free shipping and early access benefits.
4. **App Push Notifications (10% of budget):**
   - Targeted push reminders to mobile app users without active memberships during key weekend shopping traffic spikes.

---

## 4. Internal Signup-Lift Goals & KPI Targets

- **Primary KPI:** Acme+ gross new join volume during the 25-day operational window.
- **Internal Target:** A **+18% lift** in daily average join rate compared to the trailing 30-day non-promotional baseline.
- **Secondary KPIs:** 
  - Promo-driven checkout conversion rate for targeted non-member sessions.
  - 30-day retention/non-cancellation rate for acquired cohorts (to be reviewed in subsequent MBR decks alongside amara.shah and the finance analytics group).
  - Cost per acquisition (CPA) target of $\le$ $32.00 USD per successful signup.

---

## 5. Operational Notes & Cross-Vertical Dependencies

- **Data Engineering & Tracking:** wei.hartono has verified that BigQuery logging for campaign exposure events is piped correctly into `fact_experiment_exposures` and `fact_membership_events`. Event tracking IDs match `camp_90214`.
- **Care Team Alignment:** hannah.brennan and dominic.paquet have been briefed on potential volume increases in tier-1 chat inquiries regarding promo-code applications, ensuring the 'Ask Acme v2' bot (which launched back on 2025-09-15) has updated intent routing for membership signup questions.
- **Fulfillment Coordination:** With the Speed vertical monitoring warehouse throughput—especially given recent network load considerations following the September 18 store ops reviews—membership benefits highlighting expedited shipping are fully supported by current ship-to-home SLA forecasts.

---
