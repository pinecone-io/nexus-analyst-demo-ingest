---
title: "Glossary — ARR (Annual Recurring Revenue)"
source_url: "internal://acme/glossary/arr"
license: "synthetic-demo"
attribution: "Acme Inc internal metric definitions (synthetic demo). Owned by FP&A (emp_060)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: glossary
---

# ARR — Annual Recurring Revenue

**One-line definition.** ARR is the annualized run-rate revenue from the active paying subscription book at a point in time.

**Canonical SQL** (Acme convention — owned by FP&A, defined in `dbt/models/marts/finance/arr_snapshot.sql`):

```sql
SELECT
  SUM(mrr_usd) * 12 AS arr_usd
FROM `nexus-analyst-demo.acme.fact_subscriptions`
WHERE is_current = TRUE
  AND plan_tier != 'Free'
```

This is the **board-reportable** ARR. Free-tier subscriptions have `mrr_usd = 0` so they would not affect the sum, but we filter explicitly for clarity and to avoid issues if someone backfills a non-zero MRR for a Free record.

## What ARR is NOT

- **Not invoiced revenue.** Use `fact_invoices` for what we actually billed in a period.
- **Not GAAP revenue.** GAAP recognizes ratably; ARR is a snapshot of the book.
- **Not bookings.** Bookings = `Closed_Won` `amount_usd` from `fact_opportunities` for a period.

## Common pitfalls

1. **Don't sum `mrr_usd` across non-current subs.** `fact_subscriptions` is event-style: a churned customer still has historical rows. Always filter `is_current = TRUE`.
2. **Enterprise MRR is ACV ÷ 12.** Enterprise contracts are stored as `mrr_usd = acv_usd / 12`. Multiplying by 12 again recovers ACV. Do not multiply by 13 to "annualize the trailing 12 plus the next month" — that has no business meaning here.
3. **Don't use `dim_customers.current_mrr_usd` for board reporting.** That column is a denormalized convenience field and may lag a sub-day refresh of `fact_subscriptions`. Trust the fact.

## Dimensional cuts we report on

- ARR by `plan_tier`
- ARR by `region` (NA / EMEA / APAC)
- ARR by `account_tier` (SMB / MM / Ent)
- ARR by `industry`
- ARR by `acquisition_channel`

For any of these, join `fact_subscriptions` (filtered) → `dim_customers` on `customer_id`.

## Headline (as of 2026-05-04)

~$39M ARR. Business tier carries the book (~$32M); Enterprise (~$6M) is the growth engine; Pro (~$1M) is mostly self-serve seat conversion from Free.
