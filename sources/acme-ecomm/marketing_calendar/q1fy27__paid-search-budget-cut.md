---
title: "Marketing calendar: 18% paid-search budget cut (marketing-efficiency initiative)"
source_url: "internal://acme-ecomm/marketing_calendar/q1fy27__paid-search-budget-cut"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-04-15T12:00:00+00:00'
adapter: marketing_calendar_export
---

# Marketing Calendar Entry: Paid-Search Budget Reduction (Q1FY27)

**Event ID:** `camp_98214`  
**Event Name:** Q1 Paid-Search Efficiency Realignment  
**Event Type:** `budget_change`  
**Vertical:** `MARTECH` (affecting `US_CONV`)  
**Market:** US  
**Owner:** felix.arroyo (SVP Product & Growth)  
**Start Date:** 2026-02-04  
**End Date:** 2026-04-30 (Ongoing / Q1FY27 Full Quarter)  
**Planned Spend Reduction:** 18.0% vs. baseline run-rate  
**Actual Spend USD:** $14,250,000 (Adjusted Q1 actual)  

---

## Executive Summary & Strategic Rationale

This calendar entry documents the deliberate, standalone decision authorized by felix.arroyo to execute an **18% budget reduction across all US paid-search acquisition channels**, effective beginning February 4, 2026 (`2026-02-04`). 

To prevent any misattribution across analytics, finance, and weekly business review (WBR) reporting packs, it must be noted explicitly for the record that **this action is a proactive marketing-efficiency initiative**. It is **not** a reaction to any demand-side weakness, organic traffic slump, competitive pressure, or market-driven contraction. 

Leadership modeled this adjustment during the late-January financial planning cycle to optimize customer acquisition cost (CAC) payback periods across digital channels, accepting a known, planned trade-off: **a deliberate reduction in paid-search-driven sessions in exchange for structural marketing efficiency.** 

As established in Q1FY27 post-quarter evaluations, this calendar entry is the single most load-bearing operational and financial fact explaining the year-over-year US session decline experienced during the quarter (moving US sessions from 402.0M in Q1FY26 down to 379.5M in Q1FY27). Analysts querying `fact_traffic_daily` or reviewing `traffic_conversion_summary` must evaluate top-line session volumes through the lens of this planned lever rather than searching for macroeconomic headwinds.

---

## Calendar Entry Metadata & Operational Notes

```json
{
  "event_id": "camp_98214",
  "event_name": "Q1 Paid-Search Efficiency Realignment",
  "event_type": "budget_change",
  "vertical_code": "MARTECH",
  "market": "US",
  "start_date": "2026-02-04",
  "end_date": "2026-04-30",
  "planned_spend_usd": 14250000.00,
  "actual_spend_usd": 14210500.00,
  "owner_assoc_id": "assoc_100010",
  "notes": "Planned 18% reduction in SEM spend. Explicitly designed to improve blended acquisition efficiency. Will result in lower YoY paid sessions; approved by Felix Arroyo as a deliberate trade-off."
}
```

### Context & Channel Coordination
* **Timing alignment:** The budget reduction took effect on `2026-02-04`, immediately following the close of January financial reconciliations and two days prior to the deployment of maya.lindqvist's Item Page Iteration v1 (`2025-02-05`). 
* **Interaction with Session Counting:** Analysts should recall that this traffic reduction runs concurrently with the `sessions_definition_version` 1→2 cutover shipped on `2026-03-02` by wei.hartono (bot and crawler filtering). While the paid-search cut reduced gross top-line session volume, the subsequent BigQuery session-definition fix mechanically raised the measured conversion rate by shrinking the denominator. Both factors must be cited side-by-side when reconciling Q1FY27 US conversion metrics.
* **Non-interference with Organic/In-flight Work:** This budget adjustment operates entirely orthogonally to the in-flight product experiments managed by owen.faust (e.g., Checkout Simplify, `exp_2214`) and the nav redesign efforts. Paid search top-of-funnel volume was intentionally dialed back without altering landing page bidding logic or ad copy testing parameters.

---

## Administrative & Maintenance Chatter (Slack / Internal Excerpts)

> **[Slack Thread: #growth-marketing-leads | 2026-02-03]**
> 
> **felix.arroyo:** Just confirming the final sign-off on `camp_98214` for tomorrow morning. We’re pulling back the SEM spend by 18%. I know the dashboard will show a dip in gross sessions starting mid-week, but that’s the exact point of the efficiency push. Let’s make sure Amara and the finance squad have this flagged in the MBR prep decks so nobody panics about top-of-funnel traffic erosion. It’s intentional.
> 
> **amara.shah:** Got it, Felix. I’ve added a footnote to the weekly traffic models pointing back to the marketing calendar entry. We’ll separate organic/direct run-rates from the paid-search contraction so the WBR doesn't flag it as an anomaly.
> 
> **carlos.figueroa:** Good. Also, reminder that Connor is pushing the updated `traffic_conversion_summary` mart at 05:00 UTC, so make sure your queries aren't pulling cached Compass views that might still be aggregating pre-cutover numbers.

---
