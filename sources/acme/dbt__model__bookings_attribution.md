---
title: "dbt model — marts/sales/bookings_attribution (multi-touch eventually)"
source_url: "internal://acme/dbt/marts/sales/bookings_attribution"
license: "synthetic-demo"
attribution: "Acme Inc dbt model documentation (synthetic demo). Owner: Sales Ops (Jorge Martinez)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: dbt_model
---

# `marts/sales/bookings_attribution`

> Path: `dbt/models/marts/sales/bookings_attribution.sql`
> Materialization: `table` (rebuilt nightly @ 07:00 UTC)
> Owner: Sales Ops (`@jorge.martinez`)
> Tags: `sales`, `attribution`
>
> 🚧 `// TODO: planned multi-touch attribution model is in scoping. when that ships, this model becomes "first_touch_attribution" alongside a new linear/ushape variant. -jorge 2026-03-12`

## Purpose

One row per Closed_Won opportunity, joined to first-touch marketing attribution AND post-close subscription state. Used for AE quota attainment, channel ROAS, and the quarterly bookings-by-channel breakdown.

## SQL

```sql
{{
  config(
    materialized='table',
    tags=['sales', 'attribution']
  )
}}

WITH
won AS (
  SELECT
    opportunity_id,
    customer_id,
    account_name,
    ae_employee_id,
    sdr_employee_id,
    closed_won_at AS won_date,
    amount_usd AS bookings_acv_usd,
    -- DON'T multiply by 12. amount_usd is already ACV. See
    -- slack__data-help__opp-amount-vs-mrr.md for context.
    DATE_DIFF(closed_won_at, created_date, DAY) AS sales_cycle_days
  FROM {{ ref('stg_opportunities') }}
  WHERE stage = 'Closed_Won'
),

-- For first-touch attribution we need the EARLIEST marketing touch per customer.
-- Naive approach: SELECT FIRST_VALUE() OVER (PARTITION BY customer_id ORDER BY touched_at).
-- That works in postgres but BQ's window-function-with-LIMIT-1 pattern uses ARRAY_AGG.
first_touch_raw AS (
  SELECT
    customer_id,
    ARRAY_AGG(
      STRUCT(
        touched_at,
        channel,
        campaign,
        utm_source,
        utm_medium,
        utm_campaign
      )
      ORDER BY touched_at LIMIT 1
    )[OFFSET(0)] AS first_touch
  FROM {{ ref('stg_marketing_touches') }}
  WHERE customer_id IS NOT NULL
  GROUP BY customer_id
),

first_touch AS (
  SELECT
    customer_id,
    first_touch.touched_at AS first_touch_at,
    first_touch.channel AS first_touch_channel,
    first_touch.campaign AS first_touch_campaign,
    first_touch.utm_source AS first_touch_utm_source,
    first_touch.utm_medium AS first_touch_utm_medium,
    first_touch.utm_campaign AS first_touch_utm_campaign
  FROM first_touch_raw
),

-- Post-close subscription state — gives us the actual MRR they're paying
-- (might differ from the opp amount if they expanded or contracted post-close)
post_close_state AS (
  SELECT
    customer_id,
    SUM(mrr_usd) AS current_mrr_usd,
    MAX(plan_tier) AS current_plan_tier
  FROM {{ ref('stg_subscriptions') }}
  WHERE is_current = TRUE
    AND plan_tier != 'Free'
  GROUP BY customer_id
),

-- Days from first-touch to closed_won — useful for time-to-close analysis
attribution_lag AS (
  SELECT
    w.opportunity_id,
    DATE_DIFF(w.won_date, DATE(ft.first_touch_at), DAY) AS days_first_touch_to_won
  FROM won w
  LEFT JOIN first_touch ft USING (customer_id)
  WHERE ft.first_touch_at IS NOT NULL
)

SELECT
  w.opportunity_id,
  w.customer_id,
  w.account_name,
  w.ae_employee_id,
  w.sdr_employee_id,
  w.won_date,
  w.bookings_acv_usd,
  w.sales_cycle_days,
  ft.first_touch_at,
  ft.first_touch_channel,
  ft.first_touch_campaign,
  ft.first_touch_utm_source,
  ft.first_touch_utm_medium,
  ft.first_touch_utm_campaign,
  pcs.current_mrr_usd AS post_close_mrr_usd,
  -- expansion since close: positive if customer expanded post-close
  pcs.current_mrr_usd - SAFE_DIVIDE(w.bookings_acv_usd, 12) AS post_close_mrr_delta_vs_initial_usd,
  pcs.current_plan_tier AS current_plan_tier,
  al.days_first_touch_to_won
FROM won w
LEFT JOIN first_touch ft USING (customer_id)
LEFT JOIN post_close_state pcs USING (customer_id)
LEFT JOIN attribution_lag al USING (opportunity_id);

-- Notes:
-- 1. customer_id is NULL for orphan opps (rare). Those rows get NULL for
--    first_touch and post_close_state. They're still included in the table.
-- 2. The post-close MRR delta lets you identify "growth from this won account"
--    after the initial sale. Useful for AE retention scoring.
-- 3. We don't compute LTV here — that's in marts/finance/ltv.sql
```

## Columns

| Column | Type | Notes |
|---|---|---|
| `opportunity_id` | STRING | PK |
| `customer_id` | STRING | NULL only for orphan opps (rare) |
| `account_name` | STRING | |
| `ae_employee_id` | STRING | for quota attribution |
| `sdr_employee_id` | STRING | NULL for inbound |
| `won_date` | DATE | When marked Closed_Won |
| `bookings_acv_usd` | NUMERIC | ACV — already annualized, do NOT multiply by 12 |
| `sales_cycle_days` | INT64 | created → won duration |
| `first_touch_*` | various | First marketing touch attributes (NULL if no marketing touch) |
| `post_close_mrr_usd` | NUMERIC | Customer's MRR right now (might differ from initial) |
| `post_close_mrr_delta_vs_initial_usd` | NUMERIC | Expansion since close. Positive = expanded, negative = contracted, zero = flat |
| `current_plan_tier` | STRING | |
| `days_first_touch_to_won` | INT64 | Time from first marketing touch to close |

## Tests

- `unique`: opportunity_id
- `not_null`: opportunity_id, won_date, bookings_acv_usd
- `bookings_acv_usd > 0`

## Why first-touch (not last-touch)

See `slack__marketing__attribution-model-question.md` for the rationale. Chose first-touch for defensibility at AE pipeline review. Multi-touch is on the H2 roadmap but not built.

## Downstream consumers

- Looker: **Bookings by Channel** + **AE Quota Attainment** dashboards
- Quarterly board deck "channel mix" slide
- Marketing planning (campaign ROAS, owned by `@jasmine.park`)
- AE expansion scorecard (uses `post_close_mrr_delta_vs_initial_usd`)

## Edge cases

- **Customer with NO marketing touch (pure outbound)**: `first_touch_*` columns are NULL. Treat as "outbound channel" in dashboards.
- **Customer who expanded immediately after close**: `post_close_mrr_delta_vs_initial_usd` will be positive. Dashboards typically show this as "post-close expansion" credit.
- **Customer who churned post-close**: `post_close_mrr_usd` is NULL (no current subscription). The opp still appears in this model — it's a historical fact.

## Related

- `glossary__acv.md`
- `slack__marketing__attribution-model-question.md`
- `slack__data-help__opp-amount-vs-mrr.md`
- `slack__revenue__q1-net-new-arr-breakdown.md`

## File history

- `2025-12-04` — added post-close MRR delta column for AE expansion scoring
- `2025-08-15` — added attribution_lag CTE for first-touch-to-won duration
- `2025-04-15` — initial version
