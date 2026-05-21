-- materializes to BigQuery: `nexus-analyst-demo.acme.arr_snapshot`
-- (dbt folder marts/finance/ is filesystem-only; BigQuery datasets are FLAT — there is
--  no acme.dbt_marts or acme.marts.finance dataset, just acme.arr_snapshot)
-- single-row snapshot table, rebuilt nightly. board deck pulls ARR from HERE, not from
-- a fresh re-aggregation of fact_subscriptions.
{{ config(materialized='table', alias='arr_snapshot', schema='acme') }}

with paid as (
    select customer_id, plan_tier, mrr_usd
    from {{ ref('fact_subscriptions') }}
    where is_current = true
      and plan_tier != 'Free'      -- ARR excludes Free
)
select
    current_date()                                              as snapshot_date,
    sum(mrr_usd) * 12                                           as arr_usd,            -- ARR = MRR * 12
    sum(if(plan_tier = 'Pro',        mrr_usd, 0)) * 12          as arr_pro_usd,
    sum(if(plan_tier = 'Business',   mrr_usd, 0)) * 12          as arr_business_usd,
    sum(if(plan_tier = 'Enterprise', mrr_usd, 0)) * 12          as arr_enterprise_usd,
    count(distinct customer_id)                                 as paying_customers
from paid
