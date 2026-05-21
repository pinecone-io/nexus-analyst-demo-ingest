---
title: "Query log — expansion MRR by first-touch channel last quarter"
source_url: "internal://acme/query-log/expansion-mrr-by-channel"
license: "synthetic-demo"
attribution: "Acme Inc internal query log (synthetic demo). Author: Lina Cho (FP&A)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: query_log
---

# Query log — expansion MRR by first-touch channel last quarter

**Author**: @lina.cho
**Date**: 2026-04-12
**Purpose**: This query was built for the Q1 2026 Business Review to attribute expansion revenue back to the original acquisition channel. We want to see if customers acquired via `paid_search` expand at a different rate than `organic` or `referral`.

## Canonical SQL

```sql
/*
  Expansion MRR by First-Touch Channel (Last Quarter)
  Window: 2026-01-01 to 2026-03-31
  
  Logic: 
  1. Identify expansion events in fact_subscriptions (upgrade or seat_change with delta > 0).
  2. Join to bookings_attribution to get the first_touch_channel for that customer.
  3. Aggregate by channel.
*/

WITH expansion_events AS (
  SELECT
    s.customer_id,
    s.subscription_id,
    s.start_date AS event_date,
    s.mrr_usd AS new_mrr,
    p.mrr_usd AS prev_mrr,
    (s.mrr_usd - p.mrr_usd) AS expansion_mrr_delta
  FROM `nexus-analyst-demo.acme.fact_subscriptions` s
  JOIN `nexus-analyst-demo.acme.fact_subscriptions` p
    ON s.changed_from_subscription_id = p.subscription_id
  WHERE s.change_type IN ('upgrade', 'seat_change')
    AND s.start_date BETWEEN '2026-01-01' AND '2026-03-31'
    -- Only count if the delta is positive (seat_change can be a downgrade)
    AND (s.mrr_usd - p.mrr_usd) > 0
),

attribution_map AS (
  SELECT
    customer_id,
    COALESCE(first_touch_channel, 'outbound/other') AS channel
  FROM `nexus-analyst-demo.acme.marts_sales_bookings_attribution`
  -- We use the mart because it handles the ARRAY_AGG logic for first-touch
  -- and deduplicates per customer_id.
)

SELECT
  a.channel,
  COUNT(e.subscription_id) AS expansion_event_count,
  SUM(e.expansion_mrr_delta) AS total_expansion_mrr,
  SUM(e.expansion_mrr_delta) * 12 AS total_expansion_arr
FROM expansion_events e
LEFT JOIN attribution_map a USING (customer_id)
GROUP BY 1
ORDER BY 3 DESC;
```

## Implementation Notes & Pitfalls

### 1. ACV vs MRR
One of the most common errors in this report is mixing ACV (Annual Contract Value) from the `fact_opportunities` table with MRR (Monthly Recurring Revenue) from `fact_subscriptions`. 
- `fact_opportunities.amount_usd` is **already annualized**.
- `fact_subscriptions.mrr_usd` is **monthly**.
This query uses the subscription delta (MRR) and then multiplies by 12 at the very end to show the ARR impact. See `slack__data-help__opp-amount-vs-mrr.md` for the original thread on this confusion.

### 2. The "Outbound" Bucket
If `first_touch_channel` is NULL, it usually means the customer was acquired via direct outbound sales or a legacy channel that predates our HubSpot/Segment tracking (pre-2024). We bucket these as `outbound/other` to avoid a NULL row in the final chart.

### 3. Multi-expansion customers
A single customer (e.g., `cust_000412` Drag Industries) might have multiple expansion events in a single quarter (e.g., adding 5 seats in Jan, then upgrading to Business in March). This query correctly captures both events and attributes them both to the original acquisition channel.

### 4. Join Semantics
We join on `changed_from_subscription_id` to ensure we are comparing the expansion against the *immediately preceding* state. Do not join on `customer_id` with a date inequality, as that can double-count if the subscription history is complex.

## Cross-references
- See `glossary__mrr.md` for the canonical definition of expansion buckets.
- See `dbt__model__bookings_attribution.md` for how the `first_touch_channel` is derived.
- For the raw expansion list used in the CS dashboard, see `notion__csm-account-health-runbook.md`.
