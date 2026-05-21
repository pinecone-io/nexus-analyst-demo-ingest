---
title: "dbt model — dim/dim_customers"
source_url: "internal://acme/dbt/models/dim_customers"
license: "synthetic-demo"
attribution: "Acme Inc dbt model documentation (synthetic demo). Owner: David Kim (Sr DE)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: dbt_model
---

# `dim_customers`

> Path: `dbt/models/dims/dim_customers.sql`
> Materialization: `table` (rebuilt nightly @ 06:00 UTC)
> Owner: David Kim (`@david.kim`)
> Tags: `core`, `dimension`

## Purpose

The canonical dimension for all Acme customers. This model provides a point-in-time snapshot of every account (Free, Pro, Business, Enterprise) that has ever signed up for the platform. It merges data from Salesforce (firmographics, ownership) and Stripe/Product DB (plan state, signup dates).

**Note on SCD**: This is a Type 1 dimension. It only reflects the *current* state of the customer. For historical plan changes or MRR trends, you MUST join to `fact_subscriptions`. See `notion__data-warehouse-conventions.md`.

## SQL

```sql
{{
  config(
    materialized='table',
    tags=['core', 'dimension']
  )
}}

-- dim_customers: ~800 total rows (approx 530 paid, 270 unpaid/free)
-- Source: Salesforce Accounts + Stripe Customers + Product DB

WITH 
stg_sf_accounts AS (
    SELECT
        account_id AS customer_id,
        account_name AS company_name,
        region, -- NA / EMEA / APAC
        industry,
        employee_count_band,
        account_tier, -- SMB / MM / Ent
        ae_id AS ae_employee_id,
        csm_id AS csm_employee_id,
        acquisition_channel,
        primary_use_case
    FROM {{ ref('stg_salesforce__accounts') }}
),

stg_stripe_customers AS (
    SELECT
        customer_id,
        current_plan_tier,
        current_mrr_usd,
        status AS subscription_status,
        churn_date
    FROM {{ ref('stg_stripe__customers') }}
),

stg_product_signups AS (
    SELECT
        customer_id,
        MIN(signup_date) AS signup_date
    FROM {{ ref('stg_product__users') }}
    GROUP BY 1
)

SELECT
    a.customer_id,
    a.company_name,
    s.signup_date,
    a.region,
    a.industry,
    a.employee_count_band,
    a.account_tier,
    COALESCE(st.current_plan_tier, 'Free') AS current_plan_tier,
    COALESCE(st.current_mrr_usd, 0) AS current_mrr_usd,
    CASE 
        WHEN st.subscription_status = 'active' THEN 'active'
        WHEN st.subscription_status = 'paused' THEN 'paused'
        WHEN st.subscription_status = 'canceled' THEN 'churned'
        ELSE 'active' -- Default for Free users with no Stripe record
    END AS status,
    st.churn_date,
    a.csm_employee_id,
    a.ae_employee_id,
    a.acquisition_channel,
    a.primary_use_case
FROM stg_sf_accounts a
LEFT JOIN stg_stripe_customers st USING (customer_id)
LEFT JOIN stg_product_signups s USING (customer_id);

-- David Kim (2026-01-20): Added primary_use_case from the onboarding survey.
-- Note that for Free users, the AE/CSM fields will almost always be NULL.
```

## Columns

| Column | Type | Notes |
|---|---|---|
| `customer_id` | STRING | PK. `cust_xxxxxx`. |
| `company_name` | STRING | Legal name from Salesforce. |
| `signup_date` | DATE | Date of first user signup. |
| `region` | STRING | `NA`, `EMEA`, or `APAC`. |
| `industry` | STRING | SaaS, E-commerce, Finance, etc. |
| `account_tier` | STRING | `SMB`, `MM`, or `Ent`. AE-assigned. |
| `current_plan_tier` | STRING | `Free`, `Pro`, `Business`, or `Enterprise`. |
| `status` | STRING | `active`, `churned`, or `paused`. |
| `csm_employee_id` | STRING | FK to `dim_employees`. NULL for SMB/Free. |
| `ae_employee_id` | STRING | FK to `dim_employees`. |

## Tests

- `unique`: `customer_id`
- `not_null`: `customer_id`, `company_name`, `current_plan_tier`
- `accepted_values`: `status` in `('active', 'churned', 'paused')`
- `accepted_values`: `account_tier` in `('SMB', 'MM', 'Ent')`

## Usage Notes

- **Paid Status**: To filter for "Paid Customers" only, use `WHERE current_plan_tier != 'Free'`. However, for board reporting, it is safer to use `fact_subscriptions` to ensure you aren't catching a customer in a mid-day transition.
- **Ownership**: `csm_employee_id` is only populated for Mid-Market and Enterprise accounts. SMB accounts are managed via the automated health board (see `notion__csm-account-health-runbook.md`).
- **Data Drift**: If a company name is updated in Salesforce, it will overwrite the name here on the next nightly run (Type 1).

## Related Docs
- `schema__overview.md`
- `notion__data-warehouse-conventions.md`
- `glossary__paid_customer.md`
- `dbt__model__arr_snapshot.md`

## File History
- `2026-01-20` — `@david.kim`: Added `primary_use_case` and `employee_count_band`.
- `2025-11-05` — `@david.kim`: Fixed join logic for Free users who don't exist in Stripe.
- `2025-04-15` — `@david.kim`: Initial model creation.
