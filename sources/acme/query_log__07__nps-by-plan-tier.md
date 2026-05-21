---
title: "Saved query — NPS distribution by plan tier (Q1 2026)"
source_url: "internal://acme/query_log/2026-04-12-nps-by-plan"
license: "synthetic-demo"
attribution: "Acme Inc analyst saved-query log (synthetic demo)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: query_log
---

# Saved query — NPS distribution by plan tier (Q1 2026)

**Asker**: @dan.lee (VP Product)
**Author**: @aliyah.brooks (Marketing Analyst)
**Run on**: 2026-04-12 09:00 UTC

## SQL

```sql
-- NPS Q1 2026 by plan tier. Plan = current plan (might differ from plan at survey time).
WITH q1_responses AS (
  SELECT
    nps.customer_id,
    nps.score,
    nps.segment
  FROM `nexus-analyst-demo.acme.fact_nps_responses` nps
  WHERE nps.survey_quarter = '2026-Q1'
)
SELECT
  c.current_plan_tier,
  COUNT(*) AS n_responses,
  ROUND(AVG(r.score), 2) AS avg_score,
  SUM(IF(r.segment = 'promoter', 1, 0)) AS promoters,
  SUM(IF(r.segment = 'passive', 1, 0)) AS passives,
  SUM(IF(r.segment = 'detractor', 1, 0)) AS detractors,
  ROUND(
    100.0 * (SUM(IF(r.segment = 'promoter', 1, 0)) - SUM(IF(r.segment = 'detractor', 1, 0))) / COUNT(*),
    1
  ) AS nps
FROM q1_responses r
JOIN `nexus-analyst-demo.acme.dim_customers` c USING (customer_id)
GROUP BY 1
ORDER BY nps DESC;
```

## Notes

- NPS = % promoters - % detractors (× 100). Standard Bain definition.
- `segment` is precomputed in `fact_nps_responses` based on score (promoter 9-10, passive 7-8, detractor 0-6).
- Single response per customer per quarter — surveys go to one user per customer (the primary admin).
- Caveat: "current_plan_tier" might have changed between survey and now. If you care about plan-at-time-of-survey, you'd need to join to `fact_subscriptions` filtered to the survey timestamp. This query uses current plan as a simplification.

## Reused by

- Quarterly product all-hands
- Board deck "Customer Sentiment" tile
- Investor data room
