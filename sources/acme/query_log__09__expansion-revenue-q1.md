---
title: "Saved query — Expansion revenue Q1 2026 (the gnarly one)"
source_url: "internal://acme/query_log/2026-04-09-expansion-q1"
license: "synthetic-demo"
attribution: "Acme Inc analyst saved-query log (synthetic demo)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: query_log
---

# Saved query — Expansion revenue Q1 2026

**Asker**: @sam.reyes (CEO)
**Author**: @lina.cho
**Run on**: 2026-04-09 14:00 UTC

> Lina's note: "this query joins fact_subscriptions to itself via changed_from_subscription_id. the join is fragile if a customer has weird upgrade chains (e.g., upgrade → downgrade → upgrade) but our chain depth is usually 1-2. for the productionalized version see `mrr_movement.sql`."

## SQL

```sql
-- Computes expansion vs contraction MRR per change_type for a date range.
-- Join chain: fact_subscriptions -> previous fact_subscriptions row via
-- changed_from_subscription_id. Each row is a delta event.
WITH expansion_events AS (
  SELECT
    s.subscription_id,
    s.customer_id,
    s.start_date AS event_date,
    s.change_type,
    s.mrr_usd AS new_mrr,
    p.mrr_usd AS prev_mrr,
    s.mrr_usd - p.mrr_usd AS delta_mrr
  FROM `nexus-analyst-demo.acme.fact_subscriptions` s
  JOIN `nexus-analyst-demo.acme.fact_subscriptions` p
    ON s.changed_from_subscription_id = p.subscription_id
  WHERE s.start_date BETWEEN '2026-01-01' AND '2026-03-31'
    AND s.change_type IN ('upgrade', 'seat_change')
)
SELECT
  change_type,
  COUNT(*) AS n_events,
  ROUND(SUM(delta_mrr), 2) AS total_delta_mrr,
  ROUND(SUM(IF(delta_mrr > 0, delta_mrr, 0)), 2) AS expansion_mrr,
  ROUND(SUM(IF(delta_mrr < 0, delta_mrr, 0)), 2) AS contraction_mrr
FROM expansion_events
GROUP BY change_type
ORDER BY change_type;
```

## Notes

- Joins each event to its previous subscription via `changed_from_subscription_id` to compute delta.
- "Expansion" = positive delta. "Contraction" = negative delta.
- Excludes new logos and full churn — those are tracked separately.
- Pure plan upgrades (e.g., Pro → Business) typically have large positive deltas.
- Seat changes can go either direction; net out within the bucket.

## Read

Q1 expansion in Acme tends to come from two patterns:
1. Pro → Business upgrades (large deltas, AE-led)
2. Business seat additions (smaller deltas, often self-serve via the customer's admin)

If contraction dominates expansion within the seat_change bucket in a given quarter, that's an early warning of usage decline across the Business book.

## Reused by

- Board deck "Expansion vs New" slide
- CFO monthly MRR movement breakdown
- `dbt/models/marts/finance/mrr_movement.sql` (productionalized version)
