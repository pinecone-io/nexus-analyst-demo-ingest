---
title: "dbt model — facts/fact_subscriptions"
source_url: "internal://acme/dbt/facts/fact_subscriptions"
license: "synthetic-demo"
attribution: "Acme Inc dbt model documentation (synthetic demo). Owner: David Kim (Sr DE)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: dbt_model
---

# `facts/fact_subscriptions`

> Path: `dbt/models/facts/fact_subscriptions.sql`
> Materialization: `incremental` (rebuilt hourly)
> Unique Key: `['customer_id', 'start_date']`
> Owner: David Kim (`@david.kim`)
> Tags: `finance`, `core`, `incremental`
>
> 🚧 `// TODO: we still have a small gap in discount_pct for legacy 2023 contracts that were imported from the old Google Sheet. default to 0 for now. -david 2026-03-10`

## Purpose

The source-of-truth fact table for all Acme customer subscriptions. This model reconciles Stripe webhook data (for Pro/Business self-serve) with Salesforce contract data (for Enterprise/Custom Business). It captures the full history of a customer's plan changes, seat count adjustments, and churn events.

This model is the primary input for `marts/finance/arr_snapshot.sql` and `marts/finance/nrr_trailing_12.sql`.

## SQL

```sql
{{
  config(
    materialized='incremental',
    unique_key=['customer_id', 'start_date'],
    incremental_strategy='merge',
    tags=['finance', 'core']
  )
}}

-- Grain: One row per customer per subscription state.
-- A new row is generated whenever plan_tier, seat_count, or billing_cycle changes.

WITH 
stripe_subs AS (
    SELECT 
        customer_id,
        subscription_id,
        plan_tier,
        quantity AS seat_count,
        mrr_usd,
        billing_cycle, -- 'monthly' or 'annual'
        discount_pct,
        period_start_at AS start_date,
        period_end_at AS end_date,
        'self_serve' AS contract_type,
        updated_at
    FROM {{ ref('stg_stripe__subscriptions') }}
    {% if is_incremental() %}
      WHERE updated_at >= (SELECT MAX(updated_at) FROM {{ this }})
    {% endif %}
),

salesforce_contracts AS (
    SELECT 
        customer_id,
        opportunity_id AS subscription_id,
        'Enterprise' AS plan_tier, -- SFDC only handles Ent/Custom
        seat_count,
        (contract_value_usd / 12) AS mrr_usd,
        'annual' AS billing_cycle,
        discount_pct,
        contract_start_date AS start_date,
        contract_end_date AS end_date,
        'sales_led' AS contract_type,
        updated_at
    FROM {{ ref('stg_salesforce__contracts') }}
    WHERE stage = 'Closed_Won'
    {% if is_incremental() %}
      AND updated_at >= (SELECT MAX(updated_at) FROM {{ this }})
    {% endif %}
),

unioned AS (
    SELECT * FROM stripe_subs
    UNION ALL
    SELECT * FROM salesforce_contracts
),

final_deduped AS (
    -- Handle cases where a customer might have overlapping records 
    -- during a mid-cycle upgrade from Pro (Stripe) to Enterprise (SFDC).
    -- SFDC record wins for the overlapping period.
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id, start_date 
            ORDER BY contract_type DESC, updated_at DESC
        ) AS rnk
    FROM unioned
)

SELECT
    subscription_id,
    customer_id,
    plan_tier,
    start_date,
    end_date,
    mrr_usd,
    seat_count,
    billing_cycle,
    discount_pct,
    contract_type,
    -- is_current logic: active if end_date is null or in the future
    CASE 
        WHEN end_date IS NULL THEN TRUE 
        WHEN end_date > CURRENT_DATE() THEN TRUE 
        ELSE FALSE 
    END AS is_current,
    -- change_type logic: simplified for the fact layer
    -- downstream marts refine this into 'new', 'upgrade', 'churn', etc.
    CASE 
        WHEN mrr_usd = 0 THEN 'churn'
        ELSE 'active_state'
    END AS change_type
FROM final_deduped
WHERE rnk = 1;

-- Note (david, 2026-02-14): The 'rnk' logic is critical. When an AE closes 
-- an Enterprise deal for an existing Pro customer, Stripe often keeps 
-- the 'Pro' sub active for a few hours before the cancellation webhook 
-- hits. This ensures the SFDC 'sales_led' record takes precedence immediately.
```

## Columns

| Column | Type | Notes |
|---|---|---|
| `subscription_id` | STRING | PK. Stripe sub ID or SFDC Opp ID. |
| `customer_id` | STRING | FK → `dim_customers`. |
| `plan_tier` | STRING | Free, Pro, Business, Enterprise. |
| `start_date` | DATE | Effective date of this subscription state. |
| `end_date` | DATE | NULL if currently active. |
| `mrr_usd` | NUMERIC | Monthly recurring revenue for this state. |
| `seat_count` | INT64 | Number of provisioned seats. |
| `billing_cycle` | STRING | monthly, annual. |
| `discount_pct` | NUMERIC | Percentage discount applied to list price. |
| `contract_type` | STRING | self_serve (Stripe) or sales_led (SFDC). |
| `is_current` | BOOL | TRUE if this is the customer's active subscription. |

## Implementation Details

- **Incremental Strategy**: We use a `merge` strategy on `customer_id` and `start_date`. This allows us to update `end_date` on existing rows when a customer churns or changes plans without full-table scans.
- **Source Reconciliation**: This is the only model that joins Stripe and Salesforce billing data. If MRR figures in Looker look "doubled," check the `final_deduped` CTE for logic errors in the `contract_type` precedence.
- **Grandfathering**: Legacy pricing (pre-2024) is handled by the raw MRR values coming from Stripe. We do not re-calculate MRR based on `dim_plans` in this model to avoid breaking historical reporting.

## Related Docs
- `notion__pricing-tiers.md`
- `notion__data-warehouse-conventions.md`
- `glossary__arr.md`
- `dbt__model__arr_snapshot.md`

## Change Log

- **2026-02-14** (`@david.kim`): Added `contract_type` and refined the SFDC-vs-Stripe precedence logic to fix the "double MRR" bug during Enterprise upgrades.
- **2025-11-03** (`@lina.cho`): Added `discount_pct` for better NRR decomposition.
- **2025-04-15** (`@david.kim`): Initial migration to incremental materialization.
