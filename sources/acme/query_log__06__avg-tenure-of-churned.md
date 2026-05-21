---
title: "Saved query — Average tenure of churned customers (by account_tier)"
source_url: "internal://acme/query_log/2026-03-01-avg-tenure-churn"
license: "synthetic-demo"
attribution: "Acme Inc analyst saved-query log (synthetic demo)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: query_log
---

# Saved query — Average tenure of churned customers

**Asker**: @elena.volkov (VP CS) — "when do customers actually churn? want to focus CSM time on the at-risk window"
**Author**: @rajiv.patel (Sr CSM)
**Run on**: 2026-03-01 10:00 UTC

## SQL

```sql
SELECT
  c.account_tier,
  COUNT(*) AS churned_count,
  ROUND(AVG(DATE_DIFF(c.churn_date, c.signup_date, DAY)), 0) AS avg_tenure_days,
  ROUND(APPROX_QUANTILES(DATE_DIFF(c.churn_date, c.signup_date, DAY), 100)[OFFSET(50)], 0) AS median_tenure_days,
  ROUND(APPROX_QUANTILES(DATE_DIFF(c.churn_date, c.signup_date, DAY), 100)[OFFSET(75)], 0) AS p75_tenure_days,
  -- bonus: what was their MRR right before churn?
  ROUND(AVG(c.current_mrr_usd), 2) AS avg_pre_churn_mrr_usd
FROM `nexus-analyst-demo.acme.dim_customers` c
WHERE c.status = 'churned'
GROUP BY 1
ORDER BY 1;
```

> Wait — `current_mrr_usd` for churned customers is 0 because dim was set to Free at churn. That column is misleading here. Need to join to `fact_subscriptions` to get pre-churn MRR. Will refactor next round. -rajiv

## Notes

- `account_tier` separates SMB (mostly Pro), MM (Business / mid-tier), and Ent (Enterprise).
- Tenure is signup → churn date in days.
- Median is more meaningful than mean here (long-tail customers skew the average).

## Read

- SMB churns faster (median ~120-180 days). Fragile cohort.
- MM has a longer tail — many churns happen at the end of year-2 contract.
- Ent rarely churns; when they do, it's usually mid-contract due to acquisitions or budget shifts (e.g., `cust_000287 Beacon Studios`, see `gong__churn-call__cust000287-beacon-studios.md`).

## Reused by

- CSM time-allocation planning
- Renewal forecast model design (`marts/cs/renewal_forecast.sql`)
