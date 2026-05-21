---
title: "Query log — workflow error rate by plan tier"
source_url: "internal://acme/query-log/14"
license: "synthetic-demo"
attribution: "Acme Inc internal query log (synthetic demo). Author: Hannah Miles (@hannah.miles)."
fetched_at: '2026-05-04T08:15:00+00:00'
adapter: query_log
---

# Query log — workflow error rate by plan tier

**Author**: @hannah.miles (Sr Engineer)
**Date**: 2026-05-04
**Stakeholders**: Engineering, Product Analytics (@dan.lee)

## Context
This query was built to support the **Platform Reliability & Execution Health** dashboard. We specifically look at the error rate (failed runs / total runs) across our four plan tiers. Engineering uses this to isolate whether a spike in errors is platform-wide (infrastructure/provider issue) or tier-specific (often related to quota enforcement or rate-limiting logic changes).

## Canonical SQL

```sql
/*
 * Workflow Error Rate by Plan Tier (Trailing 90 Days)
 * 
 * Logic:
 * - Aggregates daily counts from marts/product/workflow_runs_daily.
 * - Joins to dim_customers to get the point-in-time plan_tier.
 * - Excludes 'paused' customers as their runs are often artifacts of 
 *   stale schedules rather than active user workflows.
 */

WITH daily_stats AS (
  SELECT
    w.run_date,
    c.current_plan_tier AS plan_tier,
    SUM(w.total_runs) AS total_runs,
    SUM(w.error_runs + w.timeout_runs) AS total_failures,
    -- Breakdown for diagnostic visibility
    SUM(w.auth_failed_count) AS auth_errors,
    SUM(w.rate_limited_count) AS rate_limit_errors,
    SUM(w.step_timeout_count) AS timeout_errors
  FROM `nexus-analyst-demo.acme.marts_product_workflow_runs_daily` w
  JOIN `nexus-analyst-demo.acme.dim_customers` c USING (customer_id)
  WHERE w.run_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
    AND c.status != 'paused'
  GROUP BY 1, 2
)

SELECT
  run_date,
  plan_tier,
  total_runs,
  total_failures,
  SAFE_DIVIDE(total_failures, total_runs) AS error_rate,
  -- Error composition
  SAFE_DIVIDE(auth_errors, total_failures) AS pct_auth_failure,
  SAFE_DIVIDE(rate_limit_errors, total_failures) AS pct_rate_limited
FROM daily_stats
WHERE total_runs > 0
ORDER BY run_date DESC, plan_tier ASC;
```

## Caveats & Edge Cases
- **Plan Drift**: This query joins to `dim_customers.current_plan_tier`. Because `dim_customers` is a point-in-time dimension (SCD Type 1), a customer who was on **Pro** 60 days ago but is now on **Business** will have all 90 days of their history attributed to **Business**. For high-precision historical reporting, we should join to `fact_subscriptions` on `run_date`, but for the reliability dashboard, the current tier is a sufficient proxy for the "type" of workload.
- **Paused Workflows**: We explicitly exclude customers with `status = 'paused'`. We found that paused accounts often have "ghost" runs from improperly terminated schedules that fail with `AUTH_FAILED` because their connections were revoked. Including them artificially inflates the error rate for the **Free** and **Pro** tiers.
- **Timeout Semantics**: We treat `timeout_runs` as failures in this query. In the product DB, a timeout is distinct from a hard error, but from a customer value-realization perspective, they are equivalent.
- **Small N on Enterprise**: The **Enterprise** tier has significantly lower run volume than **Business**. A single large customer misconfiguring a high-frequency loop can cause the Enterprise error rate to spike to 50%+ without indicating a platform regression. Always check `total_runs` before paging the on-call.

## Related Docs
- See `dbt__model__workflow_runs_daily.md` for the source table schema.
- See `notion__pricing-tiers.md` for details on quota-related error triggers (e.g., `RATE_LIMITED` spikes on Pro).
- See `slack__engineering__workflow-duration-spike.md` for a post-mortem on how `timeout_errors` impacted the **Business** tier in Q1.

## Slack Thread Context
> **@dan.lee** (2026-04-12): @hannah.miles seeing a weird divergence in Pro error rates vs Business since the 04-10 deploy. Can we pull the breakdown?
>
> **@hannah.miles** (2026-04-12): Running the log 14 query now. Looks like `rate_limited_count` is the culprit. We might have tightened the Pro concurrency governor too much.
>
> **@david.kim** (2026-04-12): Confirmed. The `marts_product_workflow_runs_daily` model shows `other_error_count` is flat, so it's definitely one of the known codes. Reverting the governor config now.
