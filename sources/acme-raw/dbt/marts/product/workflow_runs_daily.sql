-- BigQuery: `nexus-analyst-demo.acme.workflow_runs_daily`  (flat dataset)
-- daily per-customer rollup of fact_workflow_runs. partitioned on run_date (UTC day).
{{ config(materialized='incremental', alias='workflow_runs_daily', schema='acme',
          partition_by={'field': 'run_date', 'data_type': 'date'}) }}

select
    date(triggered_at)                                                as run_date,   -- UTC day boundary
    customer_id,
    count(*)                                                          as n_runs,
    countif(status = 'success')                                       as n_success,
    safe_divide(countif(status = 'success'), count(*))                as success_rate,
    approx_quantiles(duration_ms, 100)[offset(50)]                    as p50_duration_ms,
    approx_quantiles(duration_ms, 100)[offset(95)]                    as p95_duration_ms,
    approx_quantiles(duration_ms, 100)[offset(99)]                    as p99_duration_ms,
    countif(error_code = 'AUTH_FAILED')                               as auth_failed_count,
    countif(error_code = 'RATE_LIMITED')                              as rate_limited_count,
    countif(error_code = 'STEP_TIMEOUT')                              as step_timeout_count,
    countif(error_code = 'INTEGRATION_DOWN')                          as integration_down_count
from {{ ref('fact_workflow_runs') }}
{% if is_incremental() %}
where date(triggered_at) >= date_sub(current_date(), interval 3 day)   -- 3d window (was 7d, see Sep-2025 postmortem)
{% endif %}
group by 1, 2
