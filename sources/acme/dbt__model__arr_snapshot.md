---
title: "dbt model — marts/finance/arr_snapshot (with hacks + history)"
source_url: "internal://acme/dbt/marts/finance/arr_snapshot"
license: "synthetic-demo"
attribution: "Acme Inc dbt model documentation (synthetic demo). Owner: FP&A (Lina Cho)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: dbt_model
---

# `marts/finance/arr_snapshot`

> Path: `dbt/models/marts/finance/arr_snapshot.sql`
> Materialization: `table` (rebuilt nightly @ 06:30 UTC)
> Owner: FP&A (`@lina.cho`)
> Tags: `finance`, `board_metric`
>
> 🚧 `// TODO: this used to live in marts/exec/arr_snapshot.sql before the directory reshuffle in Q4 2025. some old Looker references still point to the old path. cleanup ticket #DATA-2871.`

## Purpose

Single-row table with the current ARR figure. Board-reportable. Used as the source for:
- Monthly board deck "ARR" tile
- Investor data room ARR chart
- Slack `#revenue-daily` morning post

## SQL

```sql
{{
  config(
    materialized='table',
    tags=['finance', 'board_metric']
  )
}}

-- Note (lina, 2026-02): we used to filter `is_current=TRUE` directly on
-- fact_subscriptions, but that caused a subtle bug when a customer churned
-- mid-day before the next snapshot. Now we use a 2-CTE pattern that explicitly
-- materializes the "current" set with a window function so we have an audit
-- trail. See #data-help thread 2026-02-04 for the original bug.
WITH ranked_subs AS (
  SELECT
    customer_id,
    subscription_id,
    plan_tier,
    mrr_usd,
    seat_count,
    billing_cycle,
    start_date,
    end_date,
    change_type,
    -- this is_current is the dbt-source one; we re-derive below as a sanity check
    is_current AS source_is_current,
    ROW_NUMBER() OVER (
      PARTITION BY customer_id
      ORDER BY start_date DESC, subscription_id DESC
    ) AS recency_rank
  FROM {{ ref('stg_subscriptions') }}
),

derived_current AS (
  SELECT *
  FROM ranked_subs
  WHERE recency_rank = 1
    AND (end_date IS NULL OR end_date > CURRENT_DATE())
),

-- sanity check: if source_is_current disagrees with recency_rank=1 on >5 rows,
-- raise an alert. usually 0-2 rows of disagreement (timezone edge cases at
-- midnight UTC). more than 5 = upstream pipeline bug, page #data-platform.
disagreements AS (
  SELECT COUNT(*) AS n_disagree
  FROM derived_current
  WHERE NOT source_is_current
),

current_paying AS (
  SELECT
    customer_id,
    plan_tier,
    mrr_usd,
    seat_count,
    billing_cycle
  FROM derived_current
  WHERE plan_tier != 'Free'
),

-- aggregate
agg AS (
  SELECT
    COUNT(DISTINCT customer_id) AS paying_customers,
    SUM(mrr_usd) AS mrr_usd,
    SUM(mrr_usd) * 12 AS arr_usd,
    SUM(IF(plan_tier = 'Pro', mrr_usd, 0)) * 12 AS arr_pro_usd,
    SUM(IF(plan_tier = 'Business', mrr_usd, 0)) * 12 AS arr_business_usd,
    SUM(IF(plan_tier = 'Enterprise', mrr_usd, 0)) * 12 AS arr_enterprise_usd,
    -- quarterly cohort split — useful for "growth from new logos vs existing"
    SUM(IF(plan_tier = 'Enterprise' AND seat_count >= 500, mrr_usd, 0)) * 12 AS arr_enterprise_500plus_usd
  FROM current_paying
)

SELECT
  CURRENT_DATE() AS snapshot_date,
  agg.*,
  d.n_disagree AS qc_recency_disagreements
FROM agg
CROSS JOIN disagreements d
;

-- if you're reading this and wondering why we don't just use is_current:
-- (1) we DO use is_current as the canonical signal in 95% of queries
-- (2) this model specifically materializes the board figure so we want the
--     extra paranoid sanity check
-- (3) the recency_rank approach also lets us audit the "what if the source
--     is_current is wrong?" scenario, which has happened twice in 18 months.
```

## Columns

| Column | Type | Notes |
|---|---|---|
| `snapshot_date` | DATE | Date of run |
| `paying_customers` | INT64 | Distinct paid customers |
| `mrr_usd` | NUMERIC | Total MRR |
| `arr_usd` | NUMERIC | Total ARR (= MRR × 12) |
| `arr_pro_usd` | NUMERIC | Pro contribution |
| `arr_business_usd` | NUMERIC | Business contribution |
| `arr_enterprise_usd` | NUMERIC | Enterprise contribution |
| `arr_enterprise_500plus_usd` | NUMERIC | Subset of Enterprise with seat_count ≥ 500 |
| `qc_recency_disagreements` | INT64 | Count of rows where source `is_current` disagrees with recency_rank — should be 0-2, alert if >5 |

## Tests

- `not_null`: all columns
- `arr_usd = arr_pro_usd + arr_business_usd + arr_enterprise_usd` (custom test)
- `qc_recency_disagreements <= 5` (custom test, fails the build if upstream pipeline is busted)

## Why the multi-CTE structure

Looks more complex than needed for a single-row aggregate. Rationale:

1. `ranked_subs` materializes the `recency_rank=1` set so we can audit "is the upstream is_current flag correct?". History: it wasn't, twice. Now we always cross-check.
2. `derived_current` is the Acme-canonical "current subscription per customer".
3. `disagreements` is the QC check.
4. `current_paying` is the filtered-to-paid view.
5. `agg` is the actual aggregate.

You could collapse this into 2 CTEs, but every time we've tried to simplify, we've introduced a bug (most recently in 2025-Q3 — see commit history). Leave it.

> **Old version** (deprecated 2025-Q3): single-CTE aggregation directly off `fact_subscriptions` with `is_current = TRUE` filter. Replaced by multi-CTE pattern after the off-by-3 customer count bug.

## Downstream consumers

- Looker dashboard: "Executive Daily"
- Slack post via `acme-revenue-bot` to `#revenue-daily` (06:45 UTC)
- Investor data room export (manual, monthly)
- 3 downstream dbt models reference this as a starting point for their own aggregates

## Edge cases worth knowing

- **Customer who churned at exactly 00:00:00 UTC of the snapshot day**: included or excluded? Excluded. The `end_date > CURRENT_DATE()` filter excludes them because end_date == CURRENT_DATE() means "ends today". Verified with FP&A — they want this behavior (the day-of-churn customer is no longer paying).
- **Customer with zero `seat_count`**: shouldn't exist (DB constraint), but if it did, they'd contribute 0 MRR which is fine.
- **NULL `billing_cycle`**: gets included. Doesn't affect ARR computation.

## Related

- `glossary__arr.md`
- `glossary__mrr.md`
- `dbt__model__nrr_trailing_12.md`
- `dbt__model__bookings_attribution.md`
- `slack__data-help__how-to-compute-mrr.md`

## File history

- `2026-02-04` — added recency_rank QC check after off-by-3 incident
- `2025-09-22` — moved from `marts/exec/` to `marts/finance/` directory
- `2025-06-15` — added Enterprise 500+ subset column for board deck
- `2024-12-01` — added per-tier breakdown columns
- `2024-09-04` — initial version (single CTE)
