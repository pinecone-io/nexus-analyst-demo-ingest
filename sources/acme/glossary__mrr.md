---
title: "Glossary — MRR (Monthly Recurring Revenue)"
source_url: "internal://acme/glossary/mrr"
license: "synthetic-demo"
attribution: "Acme Inc internal metric definitions (synthetic demo). Owned by FP&A (emp_060)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: glossary
---

# MRR — Monthly Recurring Revenue

**One-line definition.** MRR is the monthly run-rate revenue from the active subscription book at a point in time. Equivalent to `ARR / 12`.

**Canonical SQL.**

```sql
SELECT
  SUM(mrr_usd) AS mrr_usd
FROM `nexus-analyst-demo.acme.fact_subscriptions`
WHERE is_current = TRUE
  AND plan_tier != 'Free'
```

## MRR movement (the breakdown FP&A actually reports)

We decompose period-over-period MRR delta into 5 buckets, derived from the `change_type` column on `fact_subscriptions`:

| Bucket | `change_type` filter | Sign |
|---|---|---|
| **New MRR** | `'new'` AND `plan_tier != 'Free'` | + |
| **Expansion MRR** | `'upgrade'` OR (`'seat_change'` AND `mrr_usd > prev_mrr`) | + |
| **Contraction MRR** | `'downgrade'` OR (`'seat_change'` AND `mrr_usd < prev_mrr`) | − |
| **Churn MRR** | `'churn'` | − |
| **Reactivation MRR** | `'new'` from a previously-churned customer | + |

For period MRR delta:

```
delta_mrr = new + expansion + reactivation − contraction − churn
```

To compute `prev_mrr` for a `seat_change` row, use `changed_from_subscription_id` to look up the prior row's `mrr_usd`.

## Quick example

```sql
WITH seat_changes AS (
  SELECT
    s.subscription_id,
    s.customer_id,
    s.start_date AS event_date,
    s.mrr_usd,
    p.mrr_usd AS prev_mrr,
    s.mrr_usd - p.mrr_usd AS delta
  FROM `nexus-analyst-demo.acme.fact_subscriptions` s
  JOIN `nexus-analyst-demo.acme.fact_subscriptions` p
    ON s.changed_from_subscription_id = p.subscription_id
  WHERE s.change_type = 'seat_change'
)
SELECT FORMAT_DATE('%Y-%m', event_date) AS month, SUM(delta) AS net_seat_delta_mrr
FROM seat_changes
GROUP BY 1 ORDER BY 1;
```

## Why we don't read MRR from `dim_customers`

`dim_customers.current_mrr_usd` is a denormalized convenience for ad-hoc filters. Source of truth is always `fact_subscriptions`.
