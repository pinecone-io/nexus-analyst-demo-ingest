---
title: "dbt model — marts/cs/account_health (with workarounds)"
source_url: "internal://acme/dbt/marts/cs/account_health"
license: "synthetic-demo"
attribution: "Acme Inc dbt model documentation (synthetic demo). Owner: CS."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: dbt_model
---

# `marts/cs/account_health`

> Path: `dbt/models/marts/cs/account_health.sql`
> Materialization: `table` (rebuilt nightly @ 06:45 UTC)
> Owner: CS (`@elena.volkov` and `@marco.chen` rotating)
> Tags: `cs`, `customer_health`
>
> 🚧 `// TODO: this model has a 2-CTE chain that's specifically slow on the support_tickets join. should be partitioned by customer_id. -david.kim 2026-03-22`

## Purpose

Per-paid-customer health row. Combines the **Engaged Customer** flag with **Seat Utilization** plus a few qualitative signals into a single row that drives the **CS Account Health** Looker board and the `#cs-at-risk` Slack alerts.

## SQL

```sql
{{
  config(
    materialized='table',
    tags=['cs', 'customer_health']
  )
}}

-- Computes account health row per paid customer.
--
-- Health signals:
--   1. Engaged Customer flag (≥3 active users + ≥10 successful runs in 28d)
--   2. Seat Utilization (active_users / paid_seats)
--   3. NPS detractor flag (customer has a detractor response in last 90 days)
--   4. Open critical ticket flag (any P1 ticket open >48h)
--   5. Recent invoice failure flag (any uncollectible invoice in last 60d)
--
-- The composite `account_health_status` is what CSMs filter on.

WITH
paid AS (
  SELECT
    customer_id,
    plan_tier,
    seat_count,
    mrr_usd,
    -- enterprise gets special-cased downstream because seat_utilization
    -- doesn't apply (unlimited seats)
    IF(plan_tier = 'Enterprise', TRUE, FALSE) AS is_enterprise
  FROM {{ ref('stg_subscriptions') }}
  WHERE is_current = TRUE
    AND plan_tier != 'Free'
),

active_users_28d AS (
  SELECT
    customer_id,
    COUNT(DISTINCT user_id) AS n_active_users
  FROM {{ ref('stg_user_events') }}
  WHERE event_name = 'login'
    AND event_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 28 DAY)
  GROUP BY customer_id
),

successful_runs_28d AS (
  SELECT
    customer_id,
    COUNT(*) AS n_successful_runs
  FROM {{ ref('stg_workflow_runs') }}
  WHERE status = 'success'
    AND triggered_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 28 DAY)
  GROUP BY customer_id
),

-- failed runs in the same window — useful for the dashboard but not
-- a health signal on its own
failed_runs_28d AS (
  SELECT
    customer_id,
    COUNT(*) AS n_failed_runs
  FROM {{ ref('stg_workflow_runs') }}
  WHERE status IN ('error', 'timeout', 'partial')
    AND triggered_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 28 DAY)
  GROUP BY customer_id
),

-- NPS detractors in last 90 days
nps_detractors_90d AS (
  SELECT
    customer_id,
    MIN(score) AS min_detractor_score,
    MAX(responded_at) AS most_recent_detractor_at
  FROM {{ ref('stg_nps_responses') }}
  WHERE segment = 'detractor'
    AND responded_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
  GROUP BY customer_id
),

-- open P1 tickets > 48h. Note: we filter to P1 only because P2-P4 don't
-- escalate to "at risk" by themselves.
open_p1_tickets AS (
  SELECT
    customer_id,
    COUNT(*) AS n_open_p1_over_48h
  FROM {{ ref('stg_support_tickets') }}
  WHERE priority = 'P1'
    AND closed_at IS NULL
    AND opened_at < TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 48 HOUR)
  GROUP BY customer_id
),

-- recent involuntary-failure-ish signal: uncollectible invoices
uncollectible_invoices_60d AS (
  SELECT
    customer_id,
    COUNT(*) AS n_uncollectible_invoices
  FROM {{ ref('stg_invoices') }}
  WHERE status = 'uncollectible'
    AND invoice_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 60 DAY)
  GROUP BY customer_id
),

-- the join chain. NULL-coalesce all the count columns to 0.
joined AS (
  SELECT
    p.customer_id,
    p.plan_tier,
    p.seat_count,
    p.mrr_usd,
    p.is_enterprise,
    COALESCE(au.n_active_users, 0) AS active_users_28d,
    COALESCE(sr.n_successful_runs, 0) AS successful_runs_28d,
    COALESCE(fr.n_failed_runs, 0) AS failed_runs_28d,
    SAFE_DIVIDE(
      COALESCE(au.n_active_users, 0),
      p.seat_count
    ) AS utilization,
    -- engaged-customer flag
    (COALESCE(au.n_active_users, 0) >= 3
      AND COALESCE(sr.n_successful_runs, 0) >= 10) AS is_engaged,
    -- NPS detractor signal
    (nd.customer_id IS NOT NULL) AS has_recent_nps_detractor,
    nd.most_recent_detractor_at,
    -- ticket signal
    (op.n_open_p1_over_48h > 0) AS has_open_p1_over_48h,
    COALESCE(op.n_open_p1_over_48h, 0) AS n_open_p1_over_48h,
    -- billing signal
    (uc.n_uncollectible_invoices > 0) AS has_uncollectible_recent,
    COALESCE(uc.n_uncollectible_invoices, 0) AS n_uncollectible_invoices_60d
  FROM paid p
  LEFT JOIN active_users_28d au USING (customer_id)
  LEFT JOIN successful_runs_28d sr USING (customer_id)
  LEFT JOIN failed_runs_28d fr USING (customer_id)
  LEFT JOIN nps_detractors_90d nd USING (customer_id)
  LEFT JOIN open_p1_tickets op USING (customer_id)
  LEFT JOIN uncollectible_invoices_60d uc USING (customer_id)
)

-- final select with the composite status. The status logic is intentionally
-- a CASE chain because the order matters — earlier conditions win.
SELECT
  *,
  -- utilization band (only for non-Enterprise)
  CASE
    WHEN is_enterprise THEN NULL
    WHEN utilization >= 0.80 THEN 'healthy_expansion'
    WHEN utilization >= 0.50 THEN 'stable'
    WHEN utilization >= 0.20 THEN 'at_risk'
    ELSE 'critical'
  END AS utilization_band,
  -- composite status
  CASE
    -- enterprise uses different rules
    WHEN is_enterprise AND has_uncollectible_recent THEN 'critical'
    WHEN is_enterprise AND has_open_p1_over_48h THEN 'at_risk'
    WHEN is_enterprise AND NOT is_engaged THEN 'at_risk'
    WHEN is_enterprise AND has_recent_nps_detractor THEN 'monitoring'
    WHEN is_enterprise THEN 'healthy_expansion'
    -- non-enterprise: layered checks
    WHEN has_uncollectible_recent THEN 'critical'
    WHEN NOT is_engaged THEN 'at_risk'
    WHEN utilization < 0.20 THEN 'critical'
    WHEN utilization < 0.50 THEN 'at_risk'
    WHEN has_recent_nps_detractor THEN 'monitoring'
    WHEN has_open_p1_over_48h THEN 'monitoring'
    WHEN utilization >= 0.80 THEN 'healthy_expansion'
    ELSE 'stable'
  END AS account_health_status
FROM joined;

-- Notes:
-- - Enterprise has different status rules because seat utilization is meaningless.
--   Enterprise critical is gated on billing failure or NPS detractor + lack of engagement.
-- - 'monitoring' is a soft signal — not an active escalation but worth a check-in.
-- - The CASE chain ORDER MATTERS. Earlier conditions win. Don't rearrange.
-- - This used to be 3 separate models that we joined in Looker. Consolidated
--   into one model in 2025-Q4 to make the at-risk Slack bot simpler.
```

## Columns

(See SQL — too many to repeat compactly. The composite `account_health_status` is what CSMs care about.)

## Tests

- `unique`: customer_id
- `not_null`: customer_id, plan_tier, seat_count, mrr_usd, is_engaged
- `account_health_status` in expected enum: `critical / at_risk / monitoring / stable / healthy_expansion`
- For Enterprise rows: `utilization_band` IS NULL (custom test)

## Downstream consumers

- Looker dashboard: **CS Account Health (SMB & MM)** + **CS Account Health (Enterprise)**
- Slack: `acme-cs-bot` posts critical-band alerts to `#cs-at-risk` daily @ 08:00 UTC
- Renewal forecast model (`marts/cs/renewal_forecast.sql`)
- CSM Looker dashboards (per-CSM, filtered to assigned accounts)

## Performance notes

This model joins 6 tables. Currently runs in ~45 seconds against the full warehouse. Could be partitioned by `customer_id` or pre-aggregated upstream — on the H2 backlog. -david.kim

## Related

- `glossary__engaged_customer.md`
- `glossary__seat_utilization.md`
- `notion__csm-account-health-runbook.md`
- `slack__cs-at-risk__customer-cust000412.md`

## File history

- `2026-02-10` — added NPS detractor + open P1 ticket signals
- `2025-12-04` — added uncollectible invoice signal (post-Stripe-incident hygiene)
- `2025-10-15` — Enterprise special-casing
- `2025-08-12` — consolidated 3 source models into 1
- `2025-04-15` — initial version
