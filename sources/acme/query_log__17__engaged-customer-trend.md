---
title: "Query log — engaged_customer trend over last 12 months"
source_url: "internal://acme/query-log/engaged-customer-trend"
license: "synthetic-demo"
attribution: "Generated for Nexus Analyst Acme Enterprise BI demo."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: query_log
---

# Query log — engaged_customer trend over last 12 months

**Author**: @rajiv.patel (CS / Engagement Modeling)
**Date**: 2026-05-02
**Purpose**: Generate the monthly trend of "Engaged Customers" for the Q2 2026 board deck. This metric tracks the count of paid customers meeting the canonical engagement threshold (≥3 active users AND ≥10 successful workflow runs in the trailing 28 days).

## Context
As noted in `glossary__engaged_customer.md`, this is our primary product-led health signal. We are tracking this monthly to see if our recent onboarding improvements (shipped 2026-Q1) are moving the needle on the "engagement floor." 

**Note on Methodology**: Since `marts/cs/account_health` is a point-in-time snapshot, we have to join against historical snapshots or re-derive the logic from `fact_user_events` and `fact_workflow_runs` to get a true historical trend. For this board report, we are using the re-derivation method to ensure we don't have gaps from days the warehouse refresh failed.

## SQL Query

```sql
/* 
   Trailing 12-month trend of Engaged Customers.
   Definition: Paid customer with >=3 active users AND >=10 successful runs 
   in the 28 days prior to the end of each month.
*/

WITH calendar AS (
  -- Generate month-end dates for the last 12 months
  SELECT DISTINCT LAST_DAY(date) AS month_end
  FROM `nexus-analyst-demo.acme.dim_dates`
  WHERE date BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH) AND CURRENT_DATE()
),
monthly_engagement AS (
  SELECT
    c.month_end,
    sub.customer_id,
    -- Count active users in the 28-day window ending at month_end
    (
      SELECT COUNT(DISTINCT user_id)
      FROM `nexus-analyst-demo.acme.fact_user_events`
      WHERE event_name = 'login'
        AND event_at BETWEEN TIMESTAMP(DATE_SUB(c.month_end, INTERVAL 28 DAY)) AND TIMESTAMP(c.month_end)
        AND customer_id = sub.customer_id
    ) AS active_users,
    -- Count successful runs in the same 28-day window
    (
      SELECT COUNT(*)
      FROM `nexus-analyst-demo.acme.fact_workflow_runs`
      WHERE status = 'success'
        AND triggered_at BETWEEN TIMESTAMP(DATE_SUB(c.month_end, INTERVAL 28 DAY)) AND TIMESTAMP(c.month_end)
        AND customer_id = sub.customer_id
    ) AS successful_runs
  FROM calendar c
  CROSS JOIN (
    -- Only look at customers who were paid at that specific month_end
    SELECT DISTINCT customer_id, start_date, end_date
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE plan_tier != 'Free'
  ) sub
  WHERE sub.start_date <= c.month_end 
    AND (sub.end_date IS NULL OR sub.end_date > c.month_end)
)
SELECT
  FORMAT_DATE('%Y-%m', month_end) AS report_month,
  COUNT(DISTINCT customer_id) AS total_paid_customers,
  COUNT(DISTINCT IF(active_users >= 3 AND successful_runs >= 10, customer_id, NULL)) AS engaged_customers,
  SAFE_DIVIDE(
    COUNT(DISTINCT IF(active_users >= 3 AND successful_runs >= 10, customer_id, NULL)),
    COUNT(DISTINCT customer_id)
  ) AS engagement_rate
FROM monthly_engagement
GROUP BY 1
ORDER BY 1;
```

## Results & Observations
| report_month | total_paid_customers | engaged_customers | engagement_rate |
|---|---|---|---|
| 2025-05 | 482 | 318 | 0.659 |
| 2025-06 | 495 | 322 | 0.650 |
| ... | ... | ... | ... |
| 2026-03 | 521 | 354 | 0.679 |
| 2026-04 | 530 | 368 | 0.694 |

## Caveats & Risks
- **Engagement Floor**: As discussed in `slack__data-help__how-does-engagement-rollup-work.md`, this query treats all successful runs equally. It doesn't distinguish between a high-value "Stripe-to-NetSuite" sync and a low-value "Slack-to-Slack" notification. 
- **Performance**: This query uses correlated subqueries in a CROSS JOIN. It's fine for our current scale (~800 customers), but if we hit 5k+ customers, we should move this to a permanent incremental table in `dbt`.
- **Value Realization**: We are seeing the engagement rate tick up (65% -> 69%), but NRR is still hovering around 107%. This supports the argument in `notion__draft__value-realization-score-spec.md` that "engaged" is just a floor, not a guarantee of expansion.

## Related Docs
- `glossary__engaged_customer.md`
- `dbt__model__account_health.md`
- `notion__csm-account-health-runbook.md`
