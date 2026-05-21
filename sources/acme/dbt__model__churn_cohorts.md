---
title: "dbt model — marts/cs/churn_cohorts"
source_url: "internal://acme/dbt/marts/cs/churn_cohorts"
license: "synthetic-demo"
attribution: "Acme Inc dbt model documentation (synthetic demo). Owner: Rajiv Patel (CS)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: dbt_model
---

# `marts/cs/churn_cohorts`

> Path: `dbt/models/marts/cs/churn_cohorts.sql`
> Materialization: `table` (rebuilt weekly on Sundays @ 08:00 UTC)
> Owner: CS (`@rajiv.patel`)
> Tags: `cs`, `retention`, `churn`
>
> 🚧 `// TODO: we are still manually syncing the churn_reason from the Notion debriefs into a Google Sheet that this model refs. Need to move this to a proper Salesforce field once @jorge.martinez finishes the CRM migration. -rajiv 2026-03-25`

## Purpose

This model provides a historical view of churned customers, bucketed by the primary reason for departure. It is the source for the "Churn Reason Distribution" chart in the Monthly Business Review (MBR). It categorizes churn into **Voluntary** (controllable), **Involuntary** (uncontrollable), and **Undefined**.

## SQL

```sql
{{
  config(
    materialized='table',
    tags=['cs', 'retention']
  )
}}

-- This model joins churn events from fact_subscriptions with qualitative
-- data from our churn debrief tracker. 
-- See `notion__churn-debrief-template.md` for the data entry standard.

WITH churn_events AS (
  SELECT
    customer_id,
    plan_tier AS churned_plan_tier,
    mrr_usd AS lost_mrr_usd,
    start_date AS churn_date,
    DATE_TRUNC(start_date, QUARTER) AS churn_quarter
  FROM {{ ref('fact_subscriptions') }}
  WHERE change_type = 'churn'
),

customer_context AS (
  SELECT
    customer_id,
    company_name,
    industry,
    account_tier,
    acquisition_channel,
    csm_employee_id
  FROM {{ ref('dim_customers') }}
),

-- This CTE pulls from a manual seed/sheet where CSMs log debrief outcomes.
-- If a customer isn't in this sheet, they fall into 'Undefined'.
reasons_raw AS (
  SELECT
    customer_id,
    primary_reason,
    secondary_reason,
    notes,
    is_debrief_completed
  FROM {{ ref('stg_notion__churn_debriefs') }}
),

joined AS (
  SELECT
    ce.customer_id,
    ctx.company_name,
    ce.churn_date,
    ce.churn_quarter,
    ce.churned_plan_tier,
    ce.lost_mrr_usd,
    ctx.account_tier,
    ctx.industry,
    COALESCE(r.primary_reason, 'No Response / Undefined') AS raw_reason,
    r.is_debrief_completed,
    
    -- Categorization Logic agreed upon by Elena and Rachel (2026-01)
    CASE
      WHEN r.primary_reason IN ('Budget Cut', 'M&A / Acquisition', 'Parent Co Consolidation', 'Company Folded') 
        THEN 'Involuntary'
      WHEN r.primary_reason IN ('Product Fit / Feature Gap', 'Competitor Switch', 'Price / ROI', 'UX/UI Friction') 
        THEN 'Voluntary'
      ELSE 'Undefined'
    END AS churn_category,

    CASE
      WHEN r.primary_reason = 'M&A / Acquisition' THEN 'M&A'
      WHEN r.primary_reason = 'Budget Cut' THEN 'Budget'
      WHEN r.primary_reason = 'Competitor Switch' THEN 'Competitor'
      WHEN r.primary_reason = 'Product Fit / Feature Gap' THEN 'Product'
      WHEN r.primary_reason = 'Price / ROI' THEN 'Pricing'
      ELSE 'Other/Unknown'
    END AS reason_group
  FROM churn_events ce
  JOIN customer_context ctx USING (customer_id)
  LEFT JOIN reasons_raw r USING (customer_id)
)

SELECT
  *,
  -- Add a flag for board reporting to isolate high-value churn
  IF(lost_mrr_usd > 2000, TRUE, FALSE) AS is_high_value_churn
FROM joined;
```

## Columns

| Column | Type | Notes |
|---|---|---|
| `customer_id` | STRING | PK |
| `churn_date` | DATE | Date the churn subscription record was created |
| `churn_category` | STRING | `Voluntary`, `Involuntary`, or `Undefined` |
| `reason_group` | STRING | Simplified grouping for high-level charts (e.g., `M&A`, `Product`) |
| `lost_mrr_usd` | NUMERIC | The MRR at the time of churn |
| `is_debrief_completed` | BOOL | Whether the CSM followed `notion__churn-debrief-template.md` |

## Categorization Definitions

*   **Voluntary**: Churn we theoretically could have prevented through product improvements, better pricing, or CSM intervention.
    *   *Examples*: Switched to Tray.io, missing "Loop" step functionality, too expensive for Pro tier.
*   **Involuntary**: Churn due to external factors outside of Acme's control.
    *   *Examples*: Customer was acquired by a company using a different stack (`cust_000512`), customer went out of business.
*   **Undefined**: The customer ghosted or the CSM did not complete the debrief.

## Downstream Consumers

*   **Looker**: `CS Churn Analysis Deep-Dive`
*   **Finance**: Monthly NRR/GRR bridge uses this to explain "Controllable vs Uncontrollable" loss.
*   **Product**: Quarterly "Feature Gap" report filters for `reason_group = 'Product'`.

## Performance & Maintenance

*   **Materialization**: Table. Since it relies on manual Notion inputs that don't change frequently, a weekly refresh is sufficient.
*   **Audit**: `@rajiv.patel` reviews all `Undefined` rows on the 25th of every month to ensure CSMs are completing debriefs for accounts >$1k MRR.

## Related Docs

*   `glossary__logo_churn.md`
*   `notion__csm-account-health-runbook.md`
*   `notion__churn-debrief-template.md` (Internal process for filling `stg_notion__churn_debriefs`)

## File History

*   `2026-03-25` — `@rajiv.patel`: Added `is_high_value_churn` flag for better board visibility.
*   `2026-01-12` — `@lina.cho`: Standardized `churn_category` buckets with Finance.
*   `2025-11-05` — `@rajiv.patel`: Initial model creation.
