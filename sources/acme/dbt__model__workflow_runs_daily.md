---
title: "dbt model — marts/product/workflow_runs_daily (incremental, partitioned)"
source_url: "internal://acme/dbt/marts/product/workflow_runs_daily"
license: "synthetic-demo"
attribution: "Acme Inc dbt model documentation (synthetic demo). Owner: Product Analytics."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: dbt_model
---

# `marts/product/workflow_runs_daily`

> Path: `dbt/models/marts/product/workflow_runs_daily.sql`
> Materialization: `incremental` (rebuilt every 30 min, partitioned on `run_date`)
> Owner: Product Analytics (`@dan.lee`)
> Tags: `product`, `incremental`, `runtime_health`

## Purpose

Per-customer-per-day workflow execution rollup. Powers (a) the product execution-health dashboard, (b) the support-team "did this customer have failed runs?" lookup, (c) anomaly-detection input for the on-call alerting bot.

## SQL

```sql
{{
  config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key=['run_date', 'customer_id'],
    partition_by={'field': 'run_date', 'data_type': 'date'},
    tags=['product', 'incremental', 'runtime_health']
  )
}}

-- Why incremental: 100K runs/day × 800 customers across multiple years
-- makes a non-incremental rebuild expensive. We rebuild trailing 3 days each
-- run to handle late-arriving rows from CDC pipeline.

WITH
runs_in_window AS (
  SELECT
    DATE(triggered_at) AS run_date,
    customer_id,
    workflow_id,
    status,
    duration_ms,
    step_count,
    error_code,
    triggered_by
  FROM {{ ref('stg_workflow_runs') }}
  {% if is_incremental() %}
    -- 3-day window covers late-arriving rows
    WHERE triggered_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 3 DAY)
  {% endif %}
),

-- per-customer-per-day base aggregates
base AS (
  SELECT
    run_date,
    customer_id,
    COUNT(*) AS total_runs,
    COUNT(DISTINCT workflow_id) AS unique_workflows_used,
    SUM(IF(status = 'success', 1, 0)) AS successful_runs,
    SUM(IF(status = 'error', 1, 0)) AS error_runs,
    SUM(IF(status = 'timeout', 1, 0)) AS timeout_runs,
    SUM(IF(status = 'partial', 1, 0)) AS partial_runs,
    AVG(duration_ms) AS avg_duration_ms,
    APPROX_QUANTILES(duration_ms, 100)[OFFSET(50)] AS p50_duration_ms,
    APPROX_QUANTILES(duration_ms, 100)[OFFSET(95)] AS p95_duration_ms,
    -- p99 for SRE dashboards
    APPROX_QUANTILES(duration_ms, 100)[OFFSET(99)] AS p99_duration_ms,
    SUM(step_count) AS total_steps,
    AVG(step_count) AS avg_steps_per_run
  FROM runs_in_window
  GROUP BY run_date, customer_id
),

-- per-error-code counts (separate CTE so the schema is cleaner)
errors_by_code AS (
  SELECT
    run_date,
    customer_id,
    COUNTIF(error_code = 'AUTH_FAILED') AS auth_failed_count,
    COUNTIF(error_code = 'RATE_LIMITED') AS rate_limited_count,
    COUNTIF(error_code = 'STEP_TIMEOUT') AS step_timeout_count,
    COUNTIF(error_code = 'INTEGRATION_DOWN') AS integration_down_count,
    COUNTIF(error_code = 'USER_ERROR') AS user_error_count,
    COUNTIF(error_code = 'VALIDATION_ERROR') AS validation_error_count,
    -- catch-all for any new codes that get added without us updating this model
    COUNTIF(error_code IS NOT NULL
            AND error_code NOT IN ('AUTH_FAILED', 'RATE_LIMITED', 'STEP_TIMEOUT',
                                   'INTEGRATION_DOWN', 'USER_ERROR', 'VALIDATION_ERROR')
           ) AS other_error_count
  FROM runs_in_window
  GROUP BY run_date, customer_id
),

-- per-trigger-type breakdown
triggers_by_type AS (
  SELECT
    run_date,
    customer_id,
    COUNTIF(triggered_by = 'schedule') AS schedule_triggered,
    COUNTIF(triggered_by = 'webhook') AS webhook_triggered,
    COUNTIF(triggered_by = 'manual') AS manual_triggered,
    COUNTIF(triggered_by = 'api') AS api_triggered
  FROM runs_in_window
  GROUP BY run_date, customer_id
)

SELECT
  b.*,
  SAFE_DIVIDE(b.successful_runs, b.total_runs) AS success_rate,
  e.auth_failed_count,
  e.rate_limited_count,
  e.step_timeout_count,
  e.integration_down_count,
  e.user_error_count,
  e.validation_error_count,
  e.other_error_count,
  t.schedule_triggered,
  t.webhook_triggered,
  t.manual_triggered,
  t.api_triggered
FROM base b
LEFT JOIN errors_by_code e USING (run_date, customer_id)
LEFT JOIN triggers_by_type t USING (run_date, customer_id);

-- Notes:
-- - Aligns to UTC day boundaries.
-- - Late-arriving rows beyond 3 days will not be backfilled. <0.01% of runs.
-- - The other_error_count column catches new error codes shipped by product
--   without this model knowing. Useful "new error code in prod" detector.
```

## Columns

(See SQL — there are many. Most useful for dashboards: `total_runs`, `success_rate`, `p95_duration_ms`, `p99_duration_ms`, error_code breakdown.)

## Why incremental

100K runs/day × 365 days × 800 customers makes non-incremental expensive. We rebuild trailing 3 days each run to handle late-arriving rows from the CDC pipeline.

## Tests

- `unique`: (`run_date`, `customer_id`)
- `not_null`: `run_date`, `customer_id`, `total_runs`
- `success_rate` between 0 and 1
- `other_error_count = 0` warning test (alerts if a new error code appears that we haven't documented yet)

## Downstream consumers

- Looker: **Product execution health** dashboard
- Datadog: anomaly detection on platform-level p95 (when sums across all customers spike)
- `marts/cs/account_health.sql` reads engaged-customer signal off this
- Support team uses this as their canonical "did the customer have errors today?" lookup
- SRE dashboard data feed (Datadog sync)

## Important

- Aligns to UTC day boundaries (see `notion__data-warehouse-conventions.md`).
- Late-arriving rows beyond 3 days will not be backfilled — typically <0.01% of runs.
- The `other_error_count` column catches new error codes shipped by product that haven't been documented in this model yet. Triggers a warning test.

## Related

- `notion__on-call-rotation.md`
- `slack__engineering__workflow-duration-spike.md`
- `slack__incident__workflow-runs-stale-2025-09-12.md`
- `postmortem__workflow-runs-stale-2025-09-12.md`

## File history

- `2026-04-22` — added `other_error_count` after a new error code (`VALIDATION_ERROR`) shipped without this model knowing
- `2026-01-15` — added p99 column for SRE dashboards
- `2025-09-22` — tightened the incremental window from 7d to 3d after performance review
- `2025-06-01` — initial version
