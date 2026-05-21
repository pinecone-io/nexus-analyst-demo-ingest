-- BigQuery: `nexus-analyst-demo.acme.account_health`  (flat — the dbt path marts/cs/account_health
-- is NOT a queryable BigQuery path; there is no nested acme.marts.cs dataset)
-- one row per current paid customer. downstream consumer: marts/cs/renewal_forecast (dbt model
-- path — NOT confirmed to exist as a BigQuery table; do not assume acme.renewal_forecast is live).
{{ config(materialized='table', alias='account_health', schema='acme') }}

with uncollectible as (
    select customer_id, max(invoice_date) as last_uncollectible
    from {{ ref('fact_invoices') }}
    where status = 'uncollectible'
    group by 1
),
open_p1 as (
    -- open P1 older than 48h. ONLY P1 escalates here — P2/P3/P4 do not feed this signal.
    select customer_id, count(*) as n_open_p1_over_48h
    from {{ ref('fact_support_tickets') }}
    where priority = 'P1' and closed_at is null
      and opened_at < timestamp_sub(current_timestamp(), interval 48 hour)
    group by 1
),
nps_detractors_90d as (
    select distinct customer_id
    from {{ ref('fact_nps_responses') }}
    where segment = 'detractor'
      and responded_at >= timestamp_sub(current_timestamp(), interval 90 day)
),
engagement as (
    -- engaged = >=3 active users AND >=10 successful workflow runs in last 28 days
    select c.customer_id,
           count(distinct if(u.is_active, u.user_id, null))                          as active_users_28d,
           countif(r.status = 'success' and r.triggered_at >= timestamp_sub(current_timestamp(), interval 28 day)) as success_runs_28d
    from {{ ref('dim_customers') }} c
    left join {{ ref('dim_users') }} u using (customer_id)
    left join {{ ref('fact_workflow_runs') }} r using (customer_id)
    group by 1
),
base as (
    select
        c.customer_id, c.account_tier, c.current_plan_tier,
        u.last_uncollectible is not null
            and u.last_uncollectible >= date_sub(current_date(), interval 60 day) as has_uncollectible_recent,
        coalesce(p.n_open_p1_over_48h, 0)                                          as n_open_p1_over_48h,
        coalesce(p.n_open_p1_over_48h, 0) > 0                                       as has_open_p1_over_48h,
        d.customer_id is not null                                                  as has_recent_nps_detractor,
        e.active_users_28d >= 3 and e.success_runs_28d >= 10                        as is_engaged,
        -- seat utilization: NULL for Enterprise (unlimited seats), else used/licensed
        if(c.current_plan_tier = 'Enterprise', null,
           safe_divide(e.active_users_28d, nullif(c.seat_count_licensed, 0)))       as utilization_band
    from {{ ref('dim_customers') }} c
    left join uncollectible u using (customer_id)
    left join open_p1 p using (customer_id)
    left join nps_detractors_90d d using (customer_id)
    left join engagement e using (customer_id)
    where c.status = 'active' and c.current_plan_tier != 'Free'
)
select *,
    case
        -- Enterprise: critical only on a recent uncollectible invoice (no utilization rule — unlimited seats)
        when current_plan_tier = 'Enterprise' and has_uncollectible_recent then 'critical'
        -- non-Enterprise: critical on uncollectible OR seat utilization below 0.20
        when current_plan_tier != 'Enterprise' and (has_uncollectible_recent or utilization_band < 0.20) then 'critical'
        when has_open_p1_over_48h or has_recent_nps_detractor then 'at_risk'
        when not is_engaged then 'monitoring'
        when is_engaged and utilization_band >= 0.6 then 'healthy_expansion'
        else 'stable'
    end as account_health_status   -- enum: critical / at_risk / monitoring / stable / healthy_expansion
from base
