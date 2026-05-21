---
title: "Saved query — ARR by region (rachel asked, lina pulled)"
source_url: "internal://acme/query_log/2026-04-30-arr-by-region"
license: "synthetic-demo"
attribution: "Acme Inc analyst saved-query log (synthetic demo)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: query_log
---

# Saved query — ARR by region (2026-04-30)

**Asker**: @rachel.stein (CFO) — "for the regional revenue mix slide"
**Author**: @lina.cho (FP&A)
**Run on**: 2026-04-30 09:14 UTC
**Saved location**: Looker explore favorites + this Notion page (board prep folder)

> 💬 Lina's note: "Rachel always asks for this same query the week of board prep. Saving it here so I can paste it 4× a year."

## SQL

```sql
-- ARR by region as of NOW (uses fact_subscriptions, not dim_customers — see #data-help thread 2026-04-12)
SELECT
  c.region,
  COUNT(DISTINCT s.customer_id) AS paying_customers,
  ROUND(SUM(s.mrr_usd), 2) AS mrr_usd,
  ROUND(SUM(s.mrr_usd) * 12, 2) AS arr_usd
FROM `nexus-analyst-demo.acme.fact_subscriptions` s
JOIN `nexus-analyst-demo.acme.dim_customers` c USING (customer_id)
WHERE s.is_current = TRUE
  AND s.plan_tier != 'Free'
GROUP BY 1
ORDER BY arr_usd DESC;
```

## Result (2026-04-30 snapshot)

| region | paying_customers | mrr_usd | arr_usd |
|---|---|---|---|
| NA | 367 | 2,396,000 | 28,752,000 |
| EMEA | 142 | 793,000 | 9,516,000 |
| APAC | 13 | 80,000 | 960,000 |

## Notes / context

- ~74% of ARR concentrated in NA. EMEA steady at ~24%.
- APAC is mostly a few outsized AU customers; not a strategic region yet (debate ongoing).
- Filtered on `fact_subscriptions.is_current` per `glossary__arr.md` convention.
- If you re-run this in 6 months, the NA % will probably drop because the EMEA hiring push is supposed to grow EMEA bookings. Watch this trend.

## Reused by

- Board deck Q1 2026, slide "Regional Revenue Mix"
- Marketing planning for H2 EMEA pipeline targets
- Random ad-hoc requests from Sam every other week

## Related

- `glossary__arr.md`
- `dbt__model__arr_snapshot.md`
