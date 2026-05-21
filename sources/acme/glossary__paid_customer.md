---
title: "Glossary — Paid customer"
source_url: "internal://acme/glossary/paid-customer"
license: "synthetic-demo"
attribution: "Acme Inc internal metric definitions (synthetic demo). Owned by FP&A (emp_060) and CS (emp_040)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: glossary
---

# Paid customer

**One-line definition.** A `customer_id` that has at least one current subscription on a non-Free plan tier.

**Canonical SQL.**

```sql
SELECT DISTINCT customer_id
FROM `nexus-analyst-demo.acme.fact_subscriptions`
WHERE is_current = TRUE
  AND plan_tier != 'Free'
```

For a quick count of paid customers as of today:

```sql
SELECT COUNT(DISTINCT customer_id) AS paid_customers
FROM `nexus-analyst-demo.acme.fact_subscriptions`
WHERE is_current = TRUE
  AND plan_tier != 'Free';
```

## Why we filter on `fact_subscriptions`, not `dim_customers`

`dim_customers.current_plan_tier` is a denormalized convenience field. It is correct in steady state but can lag during an active churn or upgrade event by up to ~24 hours (the warehouse refresh cadence). For board metrics, **always use `fact_subscriptions`**.

## Edge cases

- **Trial-to-paid in the same day.** A customer who upgraded from Free → Pro on the same day they signed up has two `fact_subscriptions` rows: a Free row (closed) and a Pro row (`is_current = TRUE`). They count as paid.
- **Paused.** A `paused` status (in `dim_customers`) usually still has a current paid subscription with `mrr_usd > 0`. They count as paid for headline metrics, but FP&A reports them separately ("Paused MRR") in monthly board decks.
- **Churned.** A churned customer has a `change_type = 'churn'` row that is `is_current = TRUE` with `plan_tier = 'Free'` and `mrr_usd = 0`. They do **not** count as paid.

## Related metrics

- **Paid logos** = paid customers (used interchangeably).
- **Logo growth** = `Δ paid customers` over a period.
- **Logo churn** = paid customers who transitioned to `churn` in the period (see `glossary__logo_churn.md`).
