---
title: "dbt model — marts/finance/nrr_trailing_12 (the gnarly one)"
source_url: "internal://acme/dbt/marts/finance/nrr_trailing_12"
license: "synthetic-demo"
attribution: "Acme Inc dbt model documentation (synthetic demo). Owner: FP&A (Lina Cho)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: dbt_model
---

# `marts/finance/nrr_trailing_12`

> Path: `dbt/models/marts/finance/nrr_trailing_12.sql`
> Materialization: `table` (rebuilt nightly @ 06:35 UTC)
> Owner: FP&A (`@lina.cho`)
> Tags: `finance`, `board_metric`
>
> 🚧 `// TODO: this is the most complex finance model. needs a refactor — at minimum extract the cohort-snapshot logic into a reusable macro. on the H2 backlog. -lina 2026-04-12`

## Purpose

Computes **Net Revenue Retention (NRR)** on a trailing 12-month, fixed-cohort basis. Canonical NRR figure for board reporting. Methodology is locked — investors and the board ask about this number every quarter.

See `glossary__nrr.md` for the full methodological discussion.

## SQL — the gnarly version we actually run in prod

```sql
{{
  config(
    materialized='table',
    tags=['finance', 'board_metric']
  )
}}

-- Reads:
--   - {{ ref('stg_subscriptions') }}
--   - {{ ref('stg_customers') }} (just for sanity-check joins)
-- Writes:
--   - 1 row (or 1 row per as_of_date if backfilling)
--
-- Compute the NRR ratio for the trailing-12-month window ending CURRENT_DATE.
-- Cohort = customers who were paid as of (CURRENT_DATE - 12 months).
-- Numerator = same customers' MRR as of CURRENT_DATE (might be 0 if churned).
-- Denominator = cohort's MRR at start.

DECLARE as_of_date DATE DEFAULT CURRENT_DATE();
DECLARE start_window DATE DEFAULT DATE_SUB(as_of_date, INTERVAL 12 MONTH);

WITH
-- Step 1: extract subscription event log into something we can window over.
-- We have to handle the fact that customers may have multiple subscription
-- changes within the 12-month window. We need their state at the start window
-- and again at the as-of date.
sub_events AS (
  SELECT
    subscription_id,
    customer_id,
    plan_tier,
    start_date,
    end_date,
    mrr_usd,
    change_type,
    changed_from_subscription_id
  FROM {{ ref('stg_subscriptions') }}
  WHERE plan_tier != 'Free'
    -- exclude rows that started after our as_of date (no time travel)
    AND start_date <= as_of_date
),

-- Step 2: for each customer, find their MRR-bearing subscription as of the
-- start window. This is the "denominator" cohort.
cohort_at_start AS (
  SELECT
    customer_id,
    SUM(mrr_usd) AS start_mrr_usd
  FROM sub_events
  WHERE start_date <= start_window
    AND (end_date IS NULL OR end_date > start_window)
  GROUP BY customer_id
),

-- Step 3: same logic but for the as_of date. This is the "numerator" state.
state_at_end AS (
  SELECT
    customer_id,
    SUM(mrr_usd) AS end_mrr_usd
  FROM sub_events
  WHERE start_date <= as_of_date
    AND (end_date IS NULL OR end_date > as_of_date)
  GROUP BY customer_id
),

-- Step 4: detect cohort customers who churned during the window. They
-- contribute 0 to the numerator. We use a LEFT JOIN below so this CTE is
-- mostly informational, but we keep it for the audit log.
churned_in_window AS (
  SELECT
    customer_id,
    MAX(start_date) AS churn_date
  FROM sub_events
  WHERE change_type = 'churn'
    AND start_date BETWEEN start_window AND as_of_date
  GROUP BY customer_id
),

-- Step 5: detect cohort customers who upgraded during the window. They
-- contribute >start_mrr to the numerator.
upgrades_in_window AS (
  SELECT
    customer_id,
    SUM(IF(s.mrr_usd > p.mrr_usd, s.mrr_usd - p.mrr_usd, 0)) AS upgrade_delta_mrr
  FROM sub_events s
  LEFT JOIN sub_events p ON s.changed_from_subscription_id = p.subscription_id
  WHERE s.change_type IN ('upgrade', 'seat_change')
    AND s.start_date BETWEEN start_window AND as_of_date
  GROUP BY customer_id
),

-- Step 6: detect cohort customers who downgraded.
downgrades_in_window AS (
  SELECT
    customer_id,
    SUM(IF(s.mrr_usd < p.mrr_usd, p.mrr_usd - s.mrr_usd, 0)) AS downgrade_delta_mrr
  FROM sub_events s
  LEFT JOIN sub_events p ON s.changed_from_subscription_id = p.subscription_id
  WHERE s.change_type IN ('downgrade', 'seat_change')
    AND s.start_date BETWEEN start_window AND as_of_date
  GROUP BY customer_id
),

-- Step 7: assemble the cohort detail. One row per cohort customer with their
-- start MRR, end MRR, and movement breakdown. Used by downstream models for
-- detail reporting, not by this aggregate.
cohort_detail AS (
  SELECT
    c.customer_id,
    c.start_mrr_usd,
    COALESCE(e.end_mrr_usd, 0) AS end_mrr_usd,
    COALESCE(u.upgrade_delta_mrr, 0) AS upgrade_delta_mrr,
    COALESCE(d.downgrade_delta_mrr, 0) AS downgrade_delta_mrr,
    IF(ch.customer_id IS NOT NULL, TRUE, FALSE) AS churned_in_window
  FROM cohort_at_start c
  LEFT JOIN state_at_end e USING (customer_id)
  LEFT JOIN upgrades_in_window u USING (customer_id)
  LEFT JOIN downgrades_in_window d USING (customer_id)
  LEFT JOIN churned_in_window ch ON ch.customer_id = c.customer_id
),

-- Step 8: the aggregate. Single row.
agg AS (
  SELECT
    COUNT(*) AS cohort_size,
    SUM(start_mrr_usd) AS cohort_start_mrr_usd,
    SUM(end_mrr_usd) AS cohort_end_mrr_usd,
    SUM(IF(churned_in_window, start_mrr_usd, 0)) AS churned_mrr_loss_usd,
    SUM(upgrade_delta_mrr) AS expansion_mrr_usd,
    SUM(downgrade_delta_mrr) AS contraction_mrr_usd,
    SAFE_DIVIDE(
      SUM(end_mrr_usd),
      SUM(start_mrr_usd)
    ) AS nrr,
    -- gross retention caps numerator at start_mrr per customer
    SAFE_DIVIDE(
      SUM(LEAST(end_mrr_usd, start_mrr_usd)),
      SUM(start_mrr_usd)
    ) AS grr
  FROM cohort_detail
)

SELECT
  as_of_date AS snapshot_date,
  start_window AS cohort_start_date,
  agg.*
FROM agg;

-- Notes for future-you:
-- 1. We compute GRR alongside NRR because the board asks about both.
-- 2. The expansion/contraction breakdown is informational. The actual NRR
--    formula doesn't decompose into +/- buckets cleanly because some
--    customers have BOTH expansion AND contraction events in the window.
-- 3. The 8 CTEs are intentional. Each CTE has a clear semantic role.
--    DO NOT collapse for "performance" — query plan is the same.
-- 4. We had a subtle bug in 2025-Q3 where the cohort filter used
--    `start_date < start_window` (strict less-than) instead of `<=`.
--    Resulted in customers signed exactly 1 year ago being EXCLUDED from
--    the cohort. NRR was 0.02 too high for 1 reporting period.
--    Now we use <= and have a unit test catching the boundary case.
```

## Columns

| Column | Type | Notes |
|---|---|---|
| `snapshot_date` | DATE | When this row was computed |
| `cohort_start_date` | DATE | Start of trailing 12-month window |
| `cohort_size` | INT64 | Number of customers in the cohort |
| `cohort_start_mrr_usd` | NUMERIC | Sum of MRR at cohort start |
| `cohort_end_mrr_usd` | NUMERIC | Sum of MRR at cohort end (same customers, possibly $0 for churned) |
| `churned_mrr_loss_usd` | NUMERIC | MRR lost from cohort customers who churned |
| `expansion_mrr_usd` | NUMERIC | MRR gained from cohort customer upgrades / seat increases |
| `contraction_mrr_usd` | NUMERIC | MRR lost from cohort customer downgrades / seat decreases |
| `nrr` | FLOAT64 | NRR ratio |
| `grr` | FLOAT64 | GRR ratio |

## Tests

- `not_null`: all columns
- `nrr` between 0.0 and 3.0 (sanity bound)
- `grr <= nrr` (always true by construction)
- Boundary unit test: customer signed exactly `start_window` should be IN the cohort

## Why we don't materialize per-customer detail in this model

Returns one aggregate row. Per-customer cohort detail lives in `marts/finance/nrr_cohort_detail.sql` (downstream model that reuses this model's CTEs via dbt seeds — different rebuild cadence). Use the detail model for diagnostic work; use this one for the headline number.

## Downstream consumers

- Board deck NRR tile (manually pulled by FP&A)
- Investor data room
- Quarterly all-hands "growth" slide
- `marts/finance/nrr_cohort_detail.sql` (depends on this for the cohort definition)
- Looker tile "NRR Trailing 12mo"

## Related

- `glossary__nrr.md`
- `slack__board-prep__nrr-cohort-question.md`
- `dbt__model__arr_snapshot.md`

## File history

- `2025-09-15` — added GRR alongside NRR (board asked)
- `2025-09-15` — added expansion / contraction / churn delta columns for breakdown reporting
- `2025-06-04` — fixed off-by-one boundary bug (cohort filter strict-less-than → less-than-or-equal)
- `2025-04-15` — extracted from a Looker LookML metric into a proper dbt model
