---
title: "Saved query — SLA miss count by priority (last 90d) — for CS QBR"
source_url: "internal://acme/query_log/2026-04-25-sla-miss"
license: "synthetic-demo"
attribution: "Acme Inc analyst saved-query log (synthetic demo)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: query_log
---

# Saved query — SLA miss count by priority (last 90d)

**Asker**: @elena.volkov (VP CS)
**Author**: @marco.chen (CSM)
**Run on**: 2026-04-25 14:00 UTC

> Marco's note: "elena asks this quarterly. saving here so I don't have to re-derive the targets every time."

## SQL

```sql
WITH targets AS (
  -- internal SLA targets per notion__on-call-rotation.md
  -- NOTE these are NOT customer-promised SLAs (those are higher).
  -- if these change, update notion ALSO
  SELECT 'P1' AS priority, 4 AS target_hours UNION ALL
  SELECT 'P2', 16 UNION ALL
  SELECT 'P3', 48 UNION ALL
  SELECT 'P4', 120
),
closed AS (
  SELECT
    priority,
    resolution_time_hours
  FROM `nexus-analyst-demo.acme.fact_support_tickets`
  WHERE closed_at IS NOT NULL
    AND closed_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
)
SELECT
  c.priority,
  COUNT(*) AS n_closed,
  SUM(IF(c.resolution_time_hours > t.target_hours, 1, 0)) AS n_misses,
  ROUND(SAFE_DIVIDE(SUM(IF(c.resolution_time_hours > t.target_hours, 1, 0)), COUNT(*)) * 100, 1) AS pct_missed,
  -- median resolution for context
  ROUND(APPROX_QUANTILES(c.resolution_time_hours, 100)[OFFSET(50)], 2) AS median_hours
FROM closed c
JOIN targets t USING (priority)
GROUP BY 1
ORDER BY 1;
```

## Notes

- "Miss" = resolution time > internal target. Customer-promised SLAs are higher (looser); this is the internal bar.
- P1 misses are the most concerning. We've historically run ~5-8% miss rate on P1; anything above 10% triggers a process review.
- Could refactor to use `priority` + `target_hours` as a config seed in dbt instead of hardcoded CTE. -marco

## Reused by

- Quarterly CS metrics review
- Internal "support engineering quality" dashboard

## Related

- `slack__data-help__support-ticket-resolution-time.md`
- `notion__on-call-rotation.md`
