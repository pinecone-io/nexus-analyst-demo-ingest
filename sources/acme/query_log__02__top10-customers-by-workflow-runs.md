---
title: "Saved query — Top 10 customers by workflow runs (last 30d) — for AI beta"
source_url: "internal://acme/query_log/2026-04-22-top10-runs"
license: "synthetic-demo"
attribution: "Acme Inc analyst saved-query log (synthetic demo)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: query_log
---

# Saved query — Top 10 customers by workflow runs (last 30d)

**Asker**: @dan.lee (VP Product) — "give me the heaviest run customers, want to interview them about AI Workflow Assistant beta"
**Author**: @hannah.miles (Sr Engineer)
**Run on**: 2026-04-22 11:00 UTC
**Saved location**: Eng team query notebook + Looker

## SQL

```sql
SELECT
  r.customer_id,
  c.company_name,
  c.current_plan_tier,
  COUNT(*) AS run_count_30d,
  ROUND(AVG(r.duration_ms), 0) AS avg_duration_ms,
  ROUND(SAFE_DIVIDE(SUM(IF(r.status = 'success', 1, 0)), COUNT(*)), 4) AS success_rate
FROM `nexus-analyst-demo.acme.fact_workflow_runs` r
JOIN `nexus-analyst-demo.acme.dim_customers` c USING (customer_id)
WHERE r.triggered_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY 1, 2, 3
ORDER BY run_count_30d DESC
LIMIT 10;
```

## Notes

- Run count is highly skewed — top 10 customers typically account for ~25-35% of all platform runs.
- Most top-run customers are Enterprise (predicted by `dim_customers.current_plan_tier`).
- Used as the seed list for the AI Workflow Assistant private beta cohort 1.
- 🚧 hannah's TODO: should add a column for "% of their runs that are scheduled vs api triggered" — would help characterize who's running large batch jobs vs streaming.

## Reused by

- AI Workflow Assistant beta program (Product)
- Capacity planning for the Workflow runtime team (Eng)
- Sales — sometimes asked "who are our biggest power users?" for case study leads
