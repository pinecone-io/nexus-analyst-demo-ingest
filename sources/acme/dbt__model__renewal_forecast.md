---
title: "dbt model — marts/cs/renewal_forecast"
source_url: "internal://acme/dbt/marts/cs/renewal_forecast"
license: "synthetic-demo"
attribution: "Acme Inc dbt model documentation (synthetic demo). Owner: CS (@elena.volkov)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: dbt_model
---

# `marts/cs/renewal_forecast`

> Path: `dbt/models/marts/cs/renewal_forecast.sql`
> Materialization: `table` (rebuilt nightly @ 07:00 UTC)
> Owner: CS (`@elena.volkov`)
> Tags: `cs`, `finance`, `renewal_risk`

## Purpose

This model computes a per-customer renewal probability score and associated risk bands. It serves as the quantitative backbone for the CSM team's quarterly renewal forecast, supplementing the qualitative "Commit/Best Case" labels in the CRM. 

The probability is derived using logistic regression coefficients tuned during the **2025-Q4 Engagement Threshold Recalibration** (see `postmortem__engagement-threshold-recalibration-2025-Q4.md`). It integrates signals from `marts/cs/account_health` and `fact_subscriptions`.

## SQL

```sql
{{
  config(
    materialized='table',
    tags=['cs', 'finance', 'renewal_risk']
  )
}}

-- Logistic Regression Coefficients (Tuned 2025-12-10)
-- Intercept: 1.25
-- is_engaged = TRUE: +1.85
-- utilization_band = 'critical': -2.10
-- has_recent_nps_detractor = TRUE: -1.40
-- has_open_p1_over_48h = TRUE: -0.95

WITH health_signals AS (
  SELECT
    customer_id,
    is_engaged,
    utilization_band,
    has_recent_nps_detractor,
    has_open_p1_over_48h,
    account_health_status,
    mrr_usd,
    is_enterprise
  FROM {{ ref('account_health') }}
),

scoring AS (
  SELECT
    customer_id,
    mrr_usd,
    is_enterprise,
    account_health_status,
    -- Logit calculation
    (1.25 
      + (CASE WHEN is_engaged THEN 1.85 ELSE 0 END)
      + (CASE WHEN utilization_band = 'critical' THEN -2.10 ELSE 0 END)
      + (CASE WHEN has_recent_nps_detractor THEN -1.40 ELSE 0 END)
      + (CASE WHEN has_open_p1_over_48h THEN -0.95 ELSE 0 END)
    ) AS logit_score
  FROM health_signals
),

probabilities AS (
  SELECT
    customer_id,
    mrr_usd,
    account_health_status,
    -- Sigmoid function: 1 / (1 + exp(-logit))
    1.0 / (1.0 + EXP(-logit_score)) AS renewal_probability
  FROM scoring
)

SELECT
  customer_id,
  renewal_probability,
  CASE 
    WHEN renewal_probability >= 0.90 THEN 'Very High'
    WHEN renewal_probability >= 0.75 THEN 'High'
    WHEN renewal_probability >= 0.50 THEN 'Medium'
    WHEN renewal_probability >= 0.25 THEN 'Low'
    ELSE 'Critical'
  END AS risk_band,
  -- ARR at risk: if probability < 75%, we flag the full ARR as "at risk" for forecasting
  IF(renewal_probability < 0.75, mrr_usd * 12, 0) AS predicted_at_risk_arr_usd,
  CURRENT_TIMESTAMP() AS last_evaluated_at
FROM probabilities;
```

## Columns

| Column | Type | Notes |
|---|---|---|
| `customer_id` | STRING | PK. FK → `dim_customers`. |
| `renewal_probability` | FLOAT64 | 0.0 to 1.0. Probability of renewing at next cycle. |
| `risk_band` | STRING | Enum: `Very High`, `High`, `Medium`, `Low`, `Critical`. |
| `predicted_at_risk_arr_usd` | NUMERIC | Full ARR if probability < 0.75, else 0. |
| `last_evaluated_at` | TIMESTAMP | UTC timestamp of model run. |

## Logic & Thresholds

The `risk_band` is a direct mapping from the `renewal_probability`. Note the linkage to `account_health_status`:
- Customers in the `critical` health status almost always fall into the `Critical` or `Low` risk bands here.
- Enterprise accounts are scored using the same coefficients, but since `utilization_band` is NULL for Enterprise (see `dbt__model__account_health.md`), they rely more heavily on the `is_engaged` and NPS signals.

## Usage

- **CSM Weekly Review**: CSMs use the `risk_band` to prioritize outreach. Any account dropping below 0.50 probability triggers an immediate sync with `@elena.volkov`.
- **Finance Forecasting**: `@lina.cho` uses `predicted_at_risk_arr_usd` to haircut the top-line renewal forecast in the monthly board deck.
- **Slack Alerts**: The `acme-cs-bot` monitors this model for any >0.20 drop in `renewal_probability` over a 7-day window.

## Related Docs

- `notion__csm-account-health-runbook.md`
- `glossary__engaged_customer.md`
- `dbt__model__account_health.md`
- `postmortem__engagement-threshold-recalibration-2025-Q4.md`

## File History

- `2026-04-12` — `@elena.volkov`: Added `predicted_at_risk_arr_usd` logic for Finance alignment.
- `2025-12-10` — `@elena.volkov`: Updated logistic-regression coefficients based on Q4 recalibration data.
- `2025-09-18` — `@david.kim`: Initial model implementation; migrated from legacy Excel scoring sheet.
