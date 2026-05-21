{{ config(materialized='view', alias='stg_subscriptions', schema='acme') }}
-- thin staging view over the raw subscriptions stream. change_type vocabulary:
--   new | upgrade | seat_change | churn        (there is NO 'downgrade' change_type;
--   a downgrade is a seat_change row whose mrr_usd < the prior row, linked via
--   changed_from_subscription_id)
select
    subscription_id, customer_id, plan_tier, start_date, end_date,
    cast(mrr_usd as numeric) as mrr_usd, seat_count, billing_cycle,
    is_current, change_type, changed_from_subscription_id
from {{ source('acme_raw', 'subscriptions') }}
