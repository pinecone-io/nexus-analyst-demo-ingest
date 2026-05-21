---
title: "Query log — pipeline coverage by AE"
source_url: "internal://acme/query-log/pipeline-coverage-by-ae"
license: "synthetic-demo"
attribution: "Acme Inc Sales Ops query log (synthetic demo). Author: Jorge Martinez."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: query_log
---

# Query log — pipeline coverage by AE

**Author**: @jorge.martinez (Sales Ops)  
**Stakeholder**: @marcus.webb (VP Sales)  
**Date**: 2026-04-15  
**Purpose**: Calculate the pipeline coverage ratio (Open Pipeline / Remaining Quota) for the current sales team to identify gaps in Q2 2026 attainment.

## Context

This query is used for the Monday morning Sales Leadership sync. @marcus.webb uses this to determine which AEs are "under-covered" for the quarter. A standard healthy ratio for Acme is **3.0x** (meaning $3 of open pipeline for every $1 of remaining quota).

⚠️ **Caveat on Quota**: Quota is not currently stored in the BigQuery warehouse (it lives in a protected Google Sheet owned by @rachel.stein). For this query, I am using a `CASE` statement with the Q2 2026 targets agreed upon in the March board meeting.

⚠️ **SA/SE Conflation**: Note that `dim_employees` occasionally lists Sales Engineers (SEs) or Solution Architects (SAs) in the same team as AEs. I've added a filter to `role LIKE '%AE%'` to ensure we aren't calculating coverage for non-quota-carrying staff.

## SQL

```sql
-- Pipeline Coverage Ratio by AE (Q2 2026)
-- Author: @jorge.martinez
-- Ref: glossary__arr.md, fact_opportunities

WITH ae_quota AS (
  -- Manual quota mapping for Q2 2026 (Board Approved)
  -- TODO: Move this to a dbt seed or dim_quota table once Rachel approves the schema.
  SELECT 
    employee_id,
    full_name,
    CASE 
      WHEN full_name = 'Sarah Lopez' THEN 450000
      -- Adding other AEs from dim_employees based on Q2 assignments
      -- Note: Only quota-carrying AEs are included here
      ELSE 350000 
    END AS q2_quota_target
  FROM `nexus-analyst-demo.acme.dim_employees`
  WHERE team = 'Sales' 
    AND role LIKE '%AE%'
    AND is_active = TRUE
),

actuals AS (
  -- Closed_Won bookings in the current quarter
  SELECT 
    ae_employee_id,
    SUM(amount_usd) AS closed_won_usd
  FROM `nexus-analyst-demo.acme.fact_opportunities`
  WHERE stage = 'Closed_Won'
    AND closed_won_at BETWEEN '2026-04-01' AND '2026-06-30'
  GROUP BY 1
),

pipeline AS (
  -- Open pipeline (Qualified, Proposal, Negotiation)
  -- We exclude 'Prospecting' per Marcus's request to keep the ratio conservative.
  SELECT 
    ae_employee_id,
    SUM(amount_usd) AS open_pipeline_usd
  FROM `nexus-analyst-demo.acme.fact_opportunities`
  WHERE stage IN ('Qualified', 'Proposal', 'Negotiation')
    AND close_date BETWEEN '2026-04-01' AND '2026-06-30'
  GROUP BY 1
)

SELECT 
  q.full_name AS ae_name,
  q.q2_quota_target,
  COALESCE(a.closed_won_usd, 0) AS closed_won_usd,
  GREATEST(0, q.q2_quota_target - COALESCE(a.closed_won_usd, 0)) AS remaining_quota,
  COALESCE(p.open_pipeline_usd, 0) AS open_pipeline_usd,
  SAFE_DIVIDE(
    COALESCE(p.open_pipeline_usd, 0), 
    GREATEST(0, q.q2_quota_target - COALESCE(a.closed_won_usd, 0))
  ) AS coverage_ratio
FROM ae_quota q
LEFT JOIN actuals a ON q.employee_id = a.ae_employee_id
LEFT JOIN pipeline p ON q.employee_id = p.ae_employee_id
ORDER BY coverage_ratio ASC;
```

## Observations

- **Sarah Lopez**: Currently showing high coverage due to the `cust_000412` (Drag Industries) expansion deal sitting in 'Negotiation'. If that slips to Q3, her coverage drops significantly.
- **New Hires**: AEs hired in late Q1 2026 (see `dim_employees.hire_date`) are currently showing 0.0x coverage as their ramp-up pipeline hasn't hit 'Qualified' stage yet.
- **Data Hygiene**: There are ~4 opportunities in `fact_opportunities` with `close_date` in the past that are still in 'Qualified' stage. These are inflating coverage ratios for two AEs. @jorge.martinez to ping the team in Slack to clean these up.

## Related Docs
- `fact_opportunities` schema in `schema__overview.md`
- `notion__pricing-tiers.md` (for discount impact on pipeline amount)
- `dbt__model__bookings_attribution.md` (for won deal analysis)

## Slack Thread Summary
> **@marcus.webb** (2026-04-16 09:12): Jorge, can we exclude 'Prospecting' from the numerator? The conversion rate there is too low to rely on for Q2 coverage.
>
> **@jorge.martinez** (2026-04-16 09:45): Done. Updated the SQL above to only include Qualified and later.
>
> **@rachel.stein** (2026-04-16 10:05): Make sure you're using `amount_usd` from the opp, not the MRR from the sub. Some of these are multi-year deals where ACV > MRR*12.
>
> **@jorge.martinez** (2026-04-16 10:10): Correct, using `fact_opportunities.amount_usd` which is our canonical ACV/Bookings field. See `slack__data-help__opp-amount-vs-mrr.md`.
