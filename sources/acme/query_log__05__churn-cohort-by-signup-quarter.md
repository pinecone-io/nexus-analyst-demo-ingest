---
title: "Saved query — Churn rate by signup-quarter cohort"
source_url: "internal://acme/query_log/2026-03-15-cohort-churn"
license: "synthetic-demo"
attribution: "Acme Inc analyst saved-query log (synthetic demo)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: query_log
---

# Saved query — Churn rate by signup-quarter cohort

**Asker**: @sam.reyes (CEO) — "are recent cohorts churning faster?"
**Author**: @lina.cho
**Run on**: 2026-03-15 17:00 UTC

> Lina's note: "this is a rough cohort analysis. NOT the same as the proper retention curves we use in the board deck. that's `dbt/models/marts/finance/retention_curves.sql`. this is just a quick triage."

## SQL

```sql
WITH cohorts AS (
  SELECT
    customer_id,
    DATE_TRUNC(signup_date, QUARTER) AS signup_quarter,
    status,
    DATE_DIFF(COALESCE(churn_date, CURRENT_DATE()), signup_date, DAY) AS days_observed
  FROM `nexus-analyst-demo.acme.dim_customers`
  WHERE signup_date < DATE_SUB(CURRENT_DATE(), INTERVAL 180 DAY) -- mature cohorts only
)
SELECT
  signup_quarter,
  COUNT(*) AS cohort_size,
  SUM(IF(status = 'churned', 1, 0)) AS churned,
  ROUND(SAFE_DIVIDE(SUM(IF(status = 'churned', 1, 0)), COUNT(*)) * 100, 1) AS pct_churned,
  ROUND(AVG(IF(status = 'churned', days_observed, NULL)), 0) AS avg_days_to_churn
FROM cohorts
GROUP BY signup_quarter
ORDER BY signup_quarter;
```

## Notes

- Restricted to cohorts at least 180 days old (gives them time to churn).
- `dim_customers.churn_date` is populated only for `status = 'churned'`.
- Avg-days-to-churn is across the churned subset only.
- For a fair cohort comparison, use a "% churned within first N months" metric — better-controlled. Not yet in dbt; this query is the quick-and-dirty version.

## Read

Older cohorts (2023, early 2024) have higher pct churned simply because they've been observed longer. To compare cohorts fairly, normalize the observation window. The proper analysis lives in `dbt/models/marts/finance/retention_curves.sql`.

## Reused by

- CEO 1:1 with VP CS
- Quarterly retention deep-dive

## Related

- `glossary__logo_churn.md`
- `dbt__model__nrr_trailing_12.md`
