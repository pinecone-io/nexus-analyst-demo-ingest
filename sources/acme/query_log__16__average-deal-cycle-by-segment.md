---
title: "Query log — average deal cycle by segment"
source_url: "internal://acme/query-log/16-deal-cycle-segment"
license: "synthetic-demo"
attribution: "Acme Inc Sales Ops internal analysis (synthetic demo). Author: Jorge Martinez."
fetched_at: '2026-05-04T09:15:00+00:00'
adapter: query_log
---

# Query log — average deal cycle by segment

> **Author**: @jorge.martinez (Sales Ops)
> **Requested by**: @marcus.webb for Q1 Board Prep
> **Context**: Analyzing the lag between first marketing touch and `Closed_Won` status to refine our H2 capacity planning and SDR-to-AE handoff expectations.
> **Related**: Findings cited in `slack__board-prep__q1-channel-mix.md`.

## Objective
Determine the average duration (in days) of the full sales funnel—from the initial marketing touch recorded in `fact_marketing_touches` to the `closed_won_at` date in `fact_opportunities`. We need this segmented by our canonical account tiers (SMB, Mid-Market, Enterprise) and the acquisition channel to see where the "drag" is in the cycle.

## SQL

```sql
/* 
  Average Deal Cycle by Segment and Channel
  Source: marts/sales/bookings_attribution
  Filters: Only Closed_Won opportunities with a valid first-touch attribution.
*/

WITH deal_segments AS (
  SELECT
    opportunity_id,
    first_touch_channel,
    -- Segmenting by ACV band as defined in our sales segmentation
    CASE 
      WHEN bookings_acv_usd < 15000 THEN 'SMB'
      WHEN bookings_acv_usd >= 15000 AND bookings_acv_usd < 50000 THEN 'Mid-Market'
      WHEN bookings_acv_usd >= 50000 THEN 'Enterprise'
      ELSE 'Unknown'
    END AS acv_segment,
    days_first_touch_to_won,
    sales_cycle_days -- This is created_date to won_date (shorter than touch-to-won)
  FROM `nexus-analyst-demo.acme.marts_sales_bookings_attribution`
  WHERE won_date IS NOT NULL
    AND first_touch_at IS NOT NULL
    -- Exclude outliers from early 2023 beta period
    AND won_date >= '2024-01-01'
)

SELECT
  acv_segment,
  first_touch_channel,
  COUNT(opportunity_id) AS deals_closed,
  ROUND(AVG(days_first_touch_to_won), 1) AS avg_days_touch_to_won,
  ROUND(AVG(sales_cycle_days), 1) AS avg_days_opp_to_won,
  -- The "Marketing Lag" is the time spent as a lead before an Opp is created
  ROUND(AVG(days_first_touch_to_won - sales_cycle_days), 1) AS avg_marketing_lead_lag
FROM deal_segments
GROUP BY 1, 2
ORDER BY 1 DESC, 3 DESC;
```

## Results Summary (2024-Q1 to 2026-Q1)

| ACV Segment | Channel | Deals | Avg Touch-to-Won (Days) | Avg Opp-to-Won (Days) |
|:---|:---|:---|:---|:---|
| **Enterprise** | outbound | 14 | 142.5 | 98.2 |
| **Enterprise** | partner | 8 | 118.0 | 82.4 |
| **Mid-Market** | paid_search | 42 | 88.4 | 54.1 |
| **Mid-Market** | content | 31 | 104.2 | 61.0 |
| **SMB** | organic | 112 | 24.1 | 12.5 |
| **SMB** | paid_search | 85 | 31.5 | 14.2 |

## Observations & Analysis

1.  **Enterprise Lag**: The Delta between `first_touch` and `opportunity_created` (Marketing Lag) is significantly higher in Enterprise (~44 days). This suggests our "nurture" phase for large accounts is working but slow. Partner-sourced Enterprise deals close ~24 days faster than pure outbound.
2.  **Mid-Market Consistency**: Mid-Market deals are hovering around the 90-day mark from first touch. This aligns with the 90-day cycle noted in `backlinks__overview__company.md`.
3.  **SMB Velocity**: SMB deals are effectively PLG-speed. The 12.5-day `Opp-to-Won` cycle reflects the self-serve Pro-tier conversion motion.
4.  **Data Hygiene Note**: There are ~12 `Closed_Won` deals in the underlying `fact_opportunities` that do not appear in `bookings_attribution` because they lack a `customer_id` link or a marketing touch. These are likely legacy manual entries from 2023.

## Capacity Planning Implications
Based on these cycles, Enterprise AEs need to be sourcing pipeline today for Q4 2026 targets. We cannot rely on "in-quarter" Enterprise bookings given the 142-day average outbound cycle. Mid-Market AEs can still impact the current half if leads are qualified by the end of next month.

## Metadata
- **dbt Model**: `ref('marts/sales/bookings_attribution')`
- **Glossary Refs**: `glossary__arr.md`, `glossary__paid_customer.md`
- **Stakeholders**: @marcus.webb, @lina.cho, @jorge.martinez
