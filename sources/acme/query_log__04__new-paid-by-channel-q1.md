---
title: "Saved query — New paid customers by acquisition channel (Q1 2026)"
source_url: "internal://acme/query_log/2026-04-08-new-paid-by-channel"
license: "synthetic-demo"
attribution: "Acme Inc analyst saved-query log (synthetic demo)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: query_log
---

# Saved query — New paid customers by acquisition channel (Q1 2026)

**Asker**: @marcus.webb (VP Sales) — for AE all-hands
**Author**: @lina.cho
**Run on**: 2026-04-08 13:30 UTC

## SQL

```sql
-- New paid logos in Q1 2026 by acquisition channel.
-- "New paid" = customer's first non-Free subscription event (`change_type='new'` w/ paid plan).
-- DOES NOT include expansion (existing customers upgrading).
SELECT
  c.acquisition_channel,
  COUNT(DISTINCT c.customer_id) AS new_paid_customers
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.fact_subscriptions` s
  ON c.customer_id = s.customer_id
WHERE s.change_type = 'new'
  AND s.plan_tier != 'Free'
  AND s.start_date BETWEEN '2026-01-01' AND '2026-03-31'
GROUP BY 1
ORDER BY new_paid_customers DESC;
```

## Notes

- We define "new paid" as a customer's first non-Free subscription event (`change_type = 'new'` with `plan_tier != 'Free'`).
- Customers who upgraded from Free → paid in Q1 are counted as new paid (their first paid event happened in Q1).
- A customer who signed up in 2024 on Pro and upgraded to Business in Q1 2026 is **not** new paid — they were already paid.
- Channel attribution is from `dim_customers.acquisition_channel`, set at sign-up time. Doesn't change retroactively.
- ⚠️ heads up: marketing changed how partner channel is tagged in March 2026 — see `slack__revenue__q1-net-new-arr-breakdown.md`. Partner numbers q4 2025 vs q1 2026 not directly comparable.

## Result format (sample shape)

| acquisition_channel | new_paid_customers |
|---|---|
| outbound | 42 |
| paid_search | 28 |
| organic | 18 |
| content | 14 |
| referral | 12 |
| partner | 8 |

(Numbers will vary on rerun. Above is a snapshot from 2026-04-08.)

## Reused by

- Slack post in #revenue (`slack__revenue__q1-net-new-arr-breakdown.md`)
- Sales all-hands deck Q1 2026
