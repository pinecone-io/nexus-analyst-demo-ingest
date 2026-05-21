-- BigQuery: `nexus-analyst-demo.acme.nrr_trailing_12`  (flat dataset, NOT marts.finance.*)
-- canonical trailing-12-month NRR/GRR. fixed-cohort. board uses THIS, do not re-derive
-- NRR off raw fact_subscriptions.
{{ config(materialized='table', alias='nrr_trailing_12', schema='acme') }}

-- cohort = paid (non-Free) customers as of (snapshot_date - 12 months)
with cohort as (
    select customer_id, mrr_usd as start_mrr_usd
    from {{ ref('fact_subscriptions') }}
    where plan_tier != 'Free'
      and start_date <= date_sub(current_date(), interval 12 month)
      and (end_date is null or end_date > date_sub(current_date(), interval 12 month))
),
now_mrr as (
    select customer_id, sum(mrr_usd) as end_mrr_usd
    from {{ ref('fact_subscriptions') }}
    where is_current = true
    group by 1
),
joined as (
    -- LEFT JOIN so churned customers stay in the denominator at end_mrr = 0
    select c.customer_id, c.start_mrr_usd, coalesce(n.end_mrr_usd, 0) as end_mrr_usd
    from cohort c left join now_mrr n using (customer_id)
)
select
    count(*)                                                       as cohort_size,
    sum(start_mrr_usd)                                             as cohort_start_mrr_usd,
    sum(end_mrr_usd)                                               as cohort_end_mrr_usd,
    safe_divide(sum(end_mrr_usd), sum(start_mrr_usd))              as nrr,   -- expansion + contraction + churn
    safe_divide(sum(least(end_mrr_usd, start_mrr_usd)), sum(start_mrr_usd)) as grr,  -- no expansion credit
    sum(greatest(start_mrr_usd - end_mrr_usd, 0))                  as churned_mrr_loss_usd,
    sum(greatest(end_mrr_usd - start_mrr_usd, 0))                  as expansion_mrr_usd
from joined
