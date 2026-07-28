---
title: "Marketing calendar: Black Friday / Cyber Monday peak-holiday events"
source_url: "internal://acme-ecomm/marketing_calendar/q4fy26__black-friday-cyber-monday-peak-calendar"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-01-25T12:00:00+00:00'
adapter: marketing_calendar_export
---

# Marketing calendar: Black Friday / Cyber Monday peak-holiday events (Q4FY26)

**Owner:** maya.lindqvist (Director PM US Conversion & Traffic, `assoc_000110`)  
**Scope:** US_CONV / All Verticals (Cross-channel digital marketing, site merchandising, paid media allocation)  
**Season:** Q4FY26 Peak-Holiday Operating Window (November 1, 2025 – January 31, 2026)  
**System Reference:** `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar` (Adapter: `marketing_calendar_export`)  

---

## 1. Executive Summary & Fiscal Context

As we push through the final weeks of Q4FY26—our defined fiscal peak/holiday quarter spanning November through January—this calendar export codifies the planned campaign structures, channel mixes, spend allocations, and seasonal volume expectations for our flagship shopping events: **Black Friday (2025-11-28)** and the **Cyber Monday week immediately following (beginning 2025-12-01)**. 

To set proper context for downstream analytics models and executive reviews: Q4FY26 is currently **pacing toward a sharp session jump**, moving aggressively upward from Q3FY26’s closed 437.0M US sessions toward an anticipated full-quarter volume of 598.0M US sessions. *(Note for financial modeling: While this calendar document reflects the operational plans and targets locked ahead of the peak, the quarter itself does not formally close until 2026-01-31—still days away from this system round's execution date—meaning final reconciliation will lock downstream in February alongside MBR reporting run by amara.shah and the data team).*

Following last year's Q3FY26 infrastructure preparations—including the foundational BigQuery data audits overseen by carlos.figueroa and wei.hartono—our marketing and traffic teams coordinated heavily across the US conversion, Marketplace, and Speed verticals to absorb the incoming holiday demand surge without breaking funnel telemetry. However, as noted in recent retrospectives on our fulfillment networks (see gabriel.stroud’s logistics notes from the JOL1 winter storm disruptions on 2025-12-08), high session volume introduces severe downstream strain if marketing spend outpaces operational throughput.

---

## 2. Campaign Structure & Master Schedule Entries

The table below pulls directly from `dim_marketing_calendar` for the peak holiday window, capturing campaign identifiers, channel targets, planned versus actual expenditures (where reconciled post-event), and cross-vertical ownership.

| event_id | event_name | event_type | vertical_code | market | start_date | end_date | planned_spend_usd | actual_spend_usd | owner_assoc_id | notes |
|---|---|---|---|---|---|---|---|---|---|---|
| `camp_90102` | "Black Friday Early Access Preview" | `promo` | US_CONV | US | 2025-11-24 | 2025-11-27 | $4,500,000 | $4,620,000 | `assoc_000110` | Tiered member-first early shopping window; 48hr head start for Acme+ members |
| `camp_90103` | "Black Friday 2025 Master Surge" | `holiday` | US_CONV | US | 2025-11-28 | 2025-11-28 | $8,200,000 | $8,350,000 | `assoc_000110` | **Core BF event.** Omni-channel push across paid search, CTV, and social. |
| `camp_90104` | "Cyber Monday Week Extravaganza" | `campaign` | US_CONV | US | 2025-12-01 | 2025-12-07 | $9,500,000 | $9,410,000 | `assoc_000110` | Follow-on digital blitz; coincides with early ramp of care contact spikes and returns processing |
| `camp_90105` | "Marketplace Collector’s Holiday Showcase" | `launch` | MARKETPLACE | US | 2025-11-25 | 2025-12-02 | $1,200,000 | $1,180,000 | `assoc_000120` | Tied to sanjay.bhatt's verified badge rollout; high-value trading card & memorabilia push |
| `camp_90106` | "Acme+ Holiday Member Gift Pass" | `promo` | MEMBERSHIP | US | 2025-11-20 | 2025-12-15 | $2,800,000 | $2,750,000 | `assoc_000150` | SIMONE.LAURENT team acquisition push following Fall Savings momentum |

---

## 3. Channel Mix & Paid Media Allocation Strategy

Our paid media mix for the Black Friday through Cyber Monday block was engineered to maximize high-intent search capture while leveraging upper-funnel CTV to drive the projected session surge. 

```
[Channel Breakdown - Q4 Peak Holiday Spend]
├── Paid Search (Google / Bing): 42% ($8.75M blended allocation)
│   ├── Focus: High-intent product keywords, brand defense, dynamic inventory ads
│   └── Note: Programmatic bidding rules capped during peak CPC inflation to protect ROAS
├── Paid Social (Meta / TikTok / Pinterest): 28% ($5.83M allocation)
│   ├── Focus: Dynamic product ads (DPAs), video carousels featuring Marketplace Collectibles & Style
│   └── Integration: Works alongside sanjay.bhatt's Verified Badge campaigns (`exp_2401`)
├── Connected TV (Roku / YouTube / Streaming): 18% ($3.75M allocation)
│   ├── Focus: Brand awareness, Acme+ streaming bundle teasers (Vidora integration)
│   └── Ownership: Coordinated with renee.kowalski for membership tie-ins
└── Affiliate & Direct Partnerships: 12% ($2.50M allocation)
    ├── Focus: Cash-back networks, coupon aggregators, publisher gift guides
    └── Guardrails: Strict commission-tier caps on low-margin electronics and 3P resold goods
```

### Channel Efficiency & Operational Interdependencies
A critical learning from our post-holiday retro reviews is that marketing acquisition efficiency cannot be decoupled from fulfillment and customer care performance. While maya.lindqvist's team successfully delivered the projected traffic surge, the massive influx of holiday orders placed immediate downstream stress on warehouse nodes—most notably the Joliet DC (`node_id` `JOL1`, managed by gabriel.stroud), which suffered a 36-hour winter storm disruption on December 8, and the Ontario, CA returns center, which experienced severe understaffing that eventually triggered our January Medallia VOC alerts regarding refund delays.

Furthermore, while our front-end conversion rates during the Black Friday/Cyber Monday window hit record highs (scaling up to a quarterly average conversion rate of 3.92% for US traffic, producing 23.442M orders in US alone), we had to balance paid acquisition budgets carefully against inventory depth in Marketplace sub-verticals, particularly as Collectibles experienced a massive demand influx following the August 2025 viral card auctions and the subsequent deployment of the GradeSure "Acme Verified" authentication program on November 20, 2025.

---

## 4. Expected Seasonal Volume Spike vs. Historical Baselines

To ensure our data engineers (connor.blake, wei.hartono) and financial analysts (amara.shah) can reconcile marketing attribution against BigQuery fact tables (`fact_traffic_daily`, `fact_orders`), the expected volume parameters for the November–December peak are detailed below:

* **US Sessions Projections:** Pacing from Q3's closed 437.0M sessions to a peak-quarter target of **598.0M sessions** (actuals landing precisely in line with projections before dropping back to normal seasonal lows in Q1FY27 at 379.5M sessions).
* **Canadian & Mexican Markets:** CA sessions scaling to **66.38M** (generating $158.45M GMV) and MX sessions scaling to **42.46M** (generating $63.51M GMV).
* **Conversion Rate Expansion:** Seasonal shopping urgency traditionally expands our baseline conversion rates from ~3.10% (Q3) to **3.92%** in US, **3.82%** in CA, and **3.37%** in MX during Q4.
* **AOV Inflation:** Average Order Value (AOV) across US conversion channels jumps from Q3's $54.20 baseline to **$58.40** during the peak holiday weeks, driven by multi-item gifting bundles and higher-priced Marketplace collectable units.

---

## 5. Administrative Notes & Cross-Team Chatter

* **Slack Aside (from office chat channels during peak week):**
  > *`maya.lindqvist` [11/28/2025 08:30 EST]:* "Servers are holding up, traffic on the homepage is pacing 14% ahead of last year's Black Friday model. Big shout out to wei.hartono and the data engineering group for making sure the BigQuery streaming loads didn't bottleneck during the midnight traffic wave. Let's keep an eye on cart abandonment rates around 2 PM when the afternoon mobile spike hits."
  > 
  > *`tara.oduya` [11/28/2025 11:15 EST]:* "Fulfillment node check: BOPIS orders are flying out of the supercenters. Pickup on-time rates are sitting at 99.1% so far. Ship-to-home is feeling the usual holiday pinch but holding steady at 87% OTP. Keep pushing the store pickup messaging in the paid social carousels!"
  > 
  > *`hannah.brennan` [12/02/2025 14:40 EST]:* "Care team is seeing the expected post-BF spike in contact volume. 'Ask Acme v2' bot is deflecting well, but tickets regarding return labels are ticking up slightly. Let's make sure our returns center staffing levels in Ontario don't slip further—I'm hearing whispers from supervisory staff that holiday temporary onboarding is running slightly lean." *(Editor's note: This early December warning proved prescient; the Ontario staffing shortfall would take another two months to fully surface in quantitative SLA breaches by January).*

* **Upcoming Integrations:**
  As we transition out of Q4 and into the Q1FY27 planning cycles, marketing calendar workflows will be migrated fully from legacy Aitable tracking into Jira boards per nadia.esposito's product operations roadmap consolidation initiative (kicked off on January 15, 2026). All future Black Friday/Cyber Monday planning tags will sync directly with `dim_marketing_calendar` partition keys to eliminate schema drift between marketing spend tables and financial reporting marts.

---
