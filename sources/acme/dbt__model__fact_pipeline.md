---
title: "dbt model — facts/fact_pipeline (sales opportunities)"
source_url: "internal://acme/dbt/facts/fact_pipeline"
license: "synthetic-demo"
attribution: "Acme Inc dbt model documentation (synthetic demo). Owners: David Kim (Sr DE) & Jorge Martinez (Sales Ops)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: dbt_model
---

# `facts/fact_pipeline`

> Path: `dbt/models/facts/fact_pipeline.sql`
> Materialization: `incremental` (rebuilt hourly)
> Owners: `@david.kim` (Engineering) & `@jorge.martinez` (Sales Ops)
> Tags: `sales`, `pipeline`, `incremental`
>
> 🚧 `// TODO: we are seeing some stage-skipping in Salesforce (Prospecting -> Closed_Won in <1s). This model currently captures those as 0-second durations. Might need a filter for "meaningful" stage transitions in the reporting layer. -jorge 2026-03-15`

## Purpose

This is the source-of-truth for the Acme sales pipeline. Unlike `fact_opportunities`, which is a snapshot of the current state, `fact_pipeline` is a **state-transition log** (grain: one row per opportunity stage transition). It allows us to compute historical pipeline velocity, stage conversion rates, and "pipeline at point-in-time" for board reporting.

## SQL

```sql
{{
  config(
    materialized='incremental',
    unique_key='pipeline_event_id',
    incremental_strategy='merge',
    cluster_by=['opportunity_id', 'entered_at'],
    tags=['sales', 'pipeline']
  )
}}

-- Logic: Extract stage history from Salesforce OpportunityFieldHistory.
-- We join to the base opportunity table to get current metadata (AE, Channel).
-- For net-new prospects, customer_id will be NULL until the account is provisioned.

WITH stage_history AS (
    SELECT
        opportunity_id,
        stage_name AS stage,
        amount AS amount_usd,
        probability,
        expected_close_date AS expected_close,
        system_modstamp AS entered_at,
        -- Lead the entered_at to find when they exited this stage
        LEAD(system_modstamp) OVER (PARTITION BY opportunity_id ORDER BY system_modstamp) AS exited_at
    FROM {{ source('salesforce', 'opportunity_history') }}
    {% if is_incremental() %}
      -- Look back 3 days to catch late-syncing SFDC history records
      WHERE system_modstamp >= (SELECT MAX(entered_at) FROM {{ this }}) - INTERVAL 3 DAY
    {% endif %}
),

opp_metadata AS (
    SELECT
        opportunity_id,
        customer_id, -- NULL for prospects
        ae_employee_id AS ae_id,
        closed_won_at AS actual_close,
        -- First touch channel is denormalized here for easier cohorting
        -- See dbt__model__bookings_attribution.md for logic
        acquisition_channel AS first_touch_channel
    FROM {{ ref('stg_opportunities') }}
)

SELECT
    -- Generate a unique key for incremental merge
    MD5(CONCAT(h.opportunity_id, h.stage, CAST(h.entered_at AS STRING))) AS pipeline_event_id,
    h.opportunity_id,
    m.customer_id,
    m.ae_id,
    h.stage,
    h.amount_usd,
    h.probability,
    m.first_touch_channel,
    h.expected_close,
    m.actual_close,
    h.entered_at,
    h.exited_at,
    -- Duration in stage for velocity metrics
    TIMESTAMP_DIFF(COALESCE(h.exited_at, CURRENT_TIMESTAMP()), h.entered_at, HOUR) AS hours_in_stage
FROM stage_history h
JOIN opp_metadata m USING (opportunity_id)
```

## Columns

| Column | Type | Notes |
|---|---|---|
| `pipeline_event_id` | STRING | PK. Hash of opp_id, stage, and entered_at. |
| `opportunity_id` | STRING | FK → `fact_opportunities`. |
| `customer_id` | STRING | FK → `dim_customers`. NULL for net-new prospects. |
| `ae_id` | STRING | FK → `dim_employees`. The AE owning the opp at time of refresh. |
| `stage` | STRING | `Prospecting` / `Qualified` / `Proposal` / `Negotiation` / `Closed_Won` / `Closed_Lost`. |
| `amount_usd` | NUMERIC | Opportunity value at this stage. |
| `probability` | FLOAT64 | 0.0 to 1.0. |
| `first_touch_channel` | STRING | Denormalized from marketing touches. |
| `expected_close` | DATE | |
| `actual_close` | DATE | NULL unless stage is `Closed_Won`. |
| `entered_at` | TIMESTAMP | When the opportunity entered this stage. |
| `exited_at` | TIMESTAMP | When the opportunity moved to the next stage (NULL if current). |

## Tests

- `unique`: `pipeline_event_id`
- `not_null`: `opportunity_id`, `stage`, `entered_at`
- `relationship`: `ae_id` → `dim_employees.employee_id`
- `accepted_values`: `stage` in `['Prospecting', 'Qualified', 'Proposal', 'Negotiation', 'Closed_Won', 'Closed_Lost']`

## Downstream Consumers

- `marts/sales/bookings_attribution.sql`: Uses this to find the exact moment an opp hit `Closed_Won`.
- Looker: **Sales Velocity Dashboard** (measures average `hours_in_stage`).
- Looker: **Historical Pipeline Snapshot** (uses `entered_at` and `exited_at` to reconstruct the pipeline for any date).

## Performance Notes

- Materialized as `incremental` to avoid re-processing the entire Salesforce history (which grows linearly with sales activity).
- Clustered on `opportunity_id` to speed up the `LEAD()` window function and downstream joins.
- The 3-day lookback in the incremental block is a safety measure for Salesforce's `system_modstamp` behavior, which can occasionally lag the actual record creation.

## Related Docs

- `schema__overview.md`
- `dbt__model__bookings_attribution.md`
- `glossary__arr.md` (for how `Closed_Won` amounts translate to ARR)

## File History

- `2026-02-22` — `@david.kim`: Added `hours_in_stage` calculation and clustering.
- `2025-11-10` — `@jorge.martinez`: Initial version to support Sales Ops velocity reporting.
