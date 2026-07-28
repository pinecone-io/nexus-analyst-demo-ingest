---
title: "Marketing calendar: 'Pickup Perks' BOPIS/curbside discount campaign"
source_url: "internal://acme-ecomm/marketing_calendar/q4fy26__pickup-perks-campaign-launch"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-01-25T12:00:00+00:00'
adapter: marketing_calendar_export
---

# Marketing Calendar Entry: Pickup Perks Campaign (Q4FY26)

**Event ID:** `camp_pkup_2026_q4`
**Owner:** tara.oduya (Director PM Speed & Fulfillment, `assoc_100140`)
**Vertical:** SPEED (Sub-vertical: EFFICIENCY / Fulfillment)
**Market:** US (Primary rollout, with minor localized testing in CA/MX via regional flag)
**Status:** Launched / Active
**Planned Start Date:** 2026-01-15
**Planned End Date:** 2026-03-15 (Extended operational tracking through end of fiscal Q1FY27)

---

## 1. Executive Summary & Internal Goals

Following the peak holiday crush of Q4FY26—which saw ship-to-home strain, a 36-hour winter storm disruption at the JOL1 (Joliet) DC on December 8, and considerable pressure on our traditional parcel delivery network—the Speed & Fulfillment vertical, in close alignment with Growth Marketing (felix.arroyo) and US Conversion (maya.lindqvist), has officially initiated the **'Pickup Perks' BOPIS/curbside discount campaign**.

The core operational and strategic goal of this campaign is to **intentionally shift order mix away from vulnerable ship-to-home channels toward buy-online-pickup-in-store (BOPIS) and curbside pickup**. Pickup orders consistently achieve an on-time-to-promise rate near 99.6% (compared to ship-to-home hovering around 87%–89.3%), and dramatically reduce the last-mile cost per order, which sat at an elevated $8.60 during peak Q4 before stabilizing post-holiday. 

By offering targeted basket-level incentives ($5 off orders over $50 fulfilled via BOPIS or curbside, funded jointly by Speed and Martech budgets), we aim to accelerate the pickup mix trajectory that historically sat around 21%–24% in FY26 toward our stretch targets for FY27.

---

## 2. Campaign Parameters & Dimension Details (`dim_marketing_calendar`)

The following entry is officially synchronized with `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar` under adapter `marketing_calendar_export`:

```json
{
  "event_id": "camp_pkup_2026_q4",
  "event_name": "Pickup Perks BOPIS/curbside discount campaign",
  "event_type": "campaign",
  "vertical_code": "SPEED",
  "market": "US",
  "start_date": "2026-01-15",
  "end_date": "2026-03-15",
  "planned_spend_usd": 1250000.00,
  "actual_spend_usd": null,
  "owner_assoc_id": "assoc_100140",
  "notes": "Launched 2026-01-15 per canon. Designed to drive structural mix shift toward BOPIS/curbside to relieve carrier capacity constraints and improve blended on-time fulfillment rates."
}
```

### Channel Mix & Targeting
- **Target Segment:** General retail shoppers and Acme+ members (`mem_` panel) browsing via Web and App surfaces within a 10-mile radius of a physical store featuring active BOPIS/curbside staging bays.
- **Paid & Owned Channel Allocation:**
  - **Owned Media (40%):** App push notifications, homepage hero banner injections managed by maya.lindqvist's team, and post-login cart reminders.
  - **Paid Search & Social (45%):** Dynamically injected ad copy highlighting "Buy Online, Pick Up in Store & Save $5" during high-intent mobile search queries. *(Note: This runs parallel to our broader paid-search efficiency cuts managed by felix.arroyo, ensuring we allocate ad dollars strictly to high-conversion local intent).*
  - **Email & CRM (15%):** Targeted email blasts to shoppers who have previously utilized store pickup or reside within dense store catchments.

---

## 3. Operational Context & Cross-Functional Coordination

This launch does not sit in a vacuum. It directly intersects with several concurrent initiatives across Acme's supply chain and digital platforms:

1. **DC Automation & Fulfillment Constraints:** 
   While the DC sortation automation Phase 1 began rolling out at FON2 (Fontana) and JOL1 (Joliet) on January 12, 2026 (gabriel.stroud), store-level fulfillment operations face a different bottleneck: physical staging capacity. As reviewed in our store operations syncs (last formally discussed back in the September store capacity reviews), driving too much sudden curbside volume without matching labor scheduling leads to staging delays. Store operations lead gabriel.stroud has confirmed that tier-1 supercenters have absorbed the initial Jan 15 influx without breaking the 99.6% on-time floor, but regional alerts are configured if curbside bay saturation exceeds 85% during peak Saturday windows.

2. **Interface with the Wider Promise Window Experiment (`exp_1187`):**
   Concurrently, leo.brandt launched the "Wider Promise Window" experiment on US traffic on January 12, 2026, testing wider delivery-estimate windows to protect ship-to-home metrics. Because *Pickup Perks* actively incentivizes customers away from shipping entirely, it serves as a natural counterbalance—deflecting anxious shoppers away from delayed parcel shipping windows and directly into same-day store pickup.

3. **Roadmap Tracking & Jira Migration:**
   In accordance with Nadia Esposito’s product operations pivot initiated on January 15, 2026 (moving away from legacy Aitable cards toward centralized Jira epics), all engineering tickets associated with the checkout discount application module for Pickup Perks (`JIRA-SPD-4092`) are fully tracked under our new corporate workflow schema.

---

## 4. Administrative & Team Notes (Slack / Meeting Excerpts)

* **Slack Aside — #speed-fulfillment-lead (2026-01-18):**
  > **tara.oduya:** *"Quick read on day 3 of Pickup Perks. App checkouts selecting curbside are up roughly 4.2 percentage points over our pre-campaign baseline. Gabriel’s team at FON2 says store pickup queues are handling it, but let's keep an eye on whether the $5 discount is cannibalizing higher-margin ship-to-home baskets or truly shifting incremental local traffic. Amara (assoc_100211) is pulling the initial SQL slice from `fact_traffic_daily` to check session-to-pickup conversion splits."*
  > 
  > **gabriel.stroud:** *"Staging is fine so far, but if we scale the push notification spend next week, we'll need the store managers to flex associate hours toward curbside runner pools, especially with the winter storm hangover still lingering in the Midwest DCs."*

* **Looker / Compass Dashboard Check:**
  Analytics engineers (wei.hartono, giulia.romano) reminded the team during Monday standup that anyone querying historical Q4 metrics should verify their session definitions. Since the bot/crawler filtering update (`sessions_definition_version` version 2) deployed back on March 2, 2025, and continued through our Q4 reporting, conversion denominator shifts must be handled carefully when comparing year-over-year pickup adoption. Fortunately, `fulfillment_speed_daily` mart rows natively separate `pct_of_total_orders` by fulfillment type, preventing gross miscalculations of mix-shift impact.

---

## 5. Next Review Milestones
* **Weekly WBR Check:** Monday 07:00 ET lock for the preceding Sun–Sat performance window.
* **MBR Evaluation:** First full monthly review of campaign elasticity scheduled for the February MBR session.
