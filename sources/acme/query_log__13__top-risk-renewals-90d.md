---
title: "Query log — top risk renewals next 90 days"
source_url: "internal://acme/query-log/top-risk-renewals-90d"
license: "synthetic-demo"
attribution: "Acme Inc internal query log (synthetic demo). Author: Marco Chen (Sr CSM)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: query_log
---

# Query log — top risk renewals next 90 days

**Author**: @marco.chen
**Date**: 2026-05-04
**Purpose**: This query generates the "Red/Amber Alert" list for the weekly CS leadership sync. It identifies paid customers with contract end dates in the next 90 days who are flagged with high risk in our renewal forecasting model.

**Context**: We use this to prioritize CSM outreach and AE alignment for the upcoming quarter's renewal cycle. It specifically filters out `paused` accounts to avoid noise, as those are handled via the unpause workflow in `notion__csm-account-health-runbook.md`.

## SQL

```sql
/*
  Top Risk Renewals (Next 90 Days)
  Author: @marco.chen
  
  Joins:
  - fact_subscriptions: to get current ARR and end_date
  - account_health: for real-time engagement/utilization signals
  - renewal_forecast: for the CSM-assigned risk_band and forecast_category
  - dim_customers: for CSM name and status filtering
*/

WITH upcoming_renewals AS (
  SELECT 
    s.customer_id,
    s.end_date AS renewal_date,
    DATE_DIFF(s.end_date, CURRENT_DATE(), DAY) AS days_to_renewal,
    s.mrr_usd * 12 AS arr_at_risk
  FROM `nexus-analyst-demo.acme.fact_subscriptions` s
  WHERE s.is_current = TRUE
    AND s.plan_tier != 'Free'
    AND s.end_date BETWEEN CURRENT_DATE() AND DATE_ADD(CURRENT_DATE(), INTERVAL 90 DAY)
),

customer_context AS (
  SELECT 
    c.customer_id,
    c.company_name,
    c.status,
    e.full_name AS primary_csm
  FROM `nexus-analyst-demo.acme.dim_customers` c
  LEFT JOIN `nexus-analyst-demo.acme.dim_employees` e ON c.csm_employee_id = e.employee_id
  WHERE c.status != 'paused' -- Paused accounts have a separate workflow
)

SELECT 
  cc.company_name,
  ur.renewal_date,
  ur.days_to_renewal,
  ur.arr_at_risk,
  rf.risk_band, -- 'red', 'amber', 'green'
  rf.forecast_category, -- 'Commit', 'Best Case', 'Pipeline', 'Omitted'
  ah.account_health_status,
  ah.utilization,
  cc.primary_csm
FROM upcoming_renewals ur
JOIN customer_context cc USING (customer_id)
LEFT JOIN `nexus-analyst-demo.acme.marts.cs.account_health` ah USING (customer_id)
LEFT JOIN `nexus-analyst-demo.acme.marts.cs.renewal_forecast` rf USING (customer_id)
WHERE rf.risk_band IN ('red', 'amber')
   OR ah.account_health_status IN ('critical', 'at_risk')
ORDER BY ur.arr_at_risk DESC, ur.days_to_renewal ASC;
```

## Commentary & Findings

- **Risk Alignment**: This query often surfaces "silent churn" candidates—accounts where the CSM has marked the `risk_band` as 'green' but the `account_health_status` has slipped to 'critical' due to low `utilization` or `is_engaged = FALSE`.
- **ARR Concentration**: As of May 2026, we have a significant concentration of Business-tier renewals in the $150k-$300k ACV range coming up in late June. 
- **Data Dependencies**: This log relies on the logic defined in `dbt__model__renewal_forecast.md` (which aggregates CSM manual inputs) and `dbt__model__account_health.md` (which aggregates product telemetry). If `account_health` is stale, the utilization figures here will lag.
- **Exclusions**: We explicitly exclude `plan_tier = 'Free'` because they do not have renewal dates or ARR. We also exclude `status = 'paused'` per @elena.volkov's direction to keep the renewal board focused on active contract negotiations.

## Slack Thread Context

> **@elena.volkov** (2026-05-04 09:15 AM): @marco.chen can you make sure this query is updated to include the `utilization` column? We're seeing a few 'Amber' renewals that actually have >80% utilization, which suggests they might be expansion candidates rather than churn risks.
>
> **@marco.chen** (2026-05-04 10:02 AM): Done. Added `utilization` and `account_health_status`. It's interesting—`cust_000412` (Drag Industries) is showing as Red on forecast but 'critical' on health. Matches the audit we did in `gong__discovery__cust000412-drag-industries.md`.
>
> **@david.kim** (2026-05-04 10:45 AM): Just a heads up, the join to `marts.cs.renewal_forecast` will return NULL for any account where the CSM hasn't filled out the quarterly forecast yet. I'd suggest a COALESCE or a warning for "Missing Forecast".

## Related Docs
- `dbt__model__account_health.md`
- `dbt__model__renewal_forecast.md`
- `notion__csm-account-health-runbook.md`
- `glossary__engaged_customer.md`
