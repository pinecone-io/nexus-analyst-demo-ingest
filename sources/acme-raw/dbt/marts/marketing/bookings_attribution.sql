-- BigQuery: `nexus-analyst-demo.acme.bookings_attribution`  (flat dataset)
-- Closed_Won opps joined to first marketing touch. ONE row per won opp.
{{ config(materialized='table', alias='bookings_attribution', schema='acme') }}

with won as (
    select opportunity_id, customer_id, account_name, amount_usd, closed_won_at
    from {{ ref('fact_opportunities') }}
    where stage = 'Closed_Won'
),
first_touch as (
    select customer_id, channel as first_touch_channel,
           row_number() over (partition by customer_id order by touched_at asc) as rn
    from {{ ref('fact_marketing_touches') }}
)
select
    w.opportunity_id,
    w.customer_id,
    w.account_name,
    -- amount_usd on the opp is the annual contract value already. bookings_acv_usd is
    -- ALREADY ANNUALIZED — do NOT multiply by 12 (it is not an MRR figure).
    w.amount_usd                                          as bookings_acv_usd,
    w.closed_won_at,
    ft.first_touch_channel                                -- NULL = pure outbound (no marketing touch)
from won w
left join first_touch ft on ft.customer_id = w.customer_id and ft.rn = 1
