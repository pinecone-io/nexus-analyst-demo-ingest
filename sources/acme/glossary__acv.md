---
title: "Glossary — ACV (Annual Contract Value)"
source_url: "internal://acme/glossary/acv"
license: "synthetic-demo"
attribution: "Acme Inc internal metric definitions (synthetic demo). Owned by FP&A (emp_060) and Sales (emp_020)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: glossary
---

# ACV — Annual Contract Value

**One-line definition.** ACV is the annualized contract value for a single subscription. For most Acme customers ACV equals `mrr_usd × 12`. For Enterprise customers, ACV is the contracted value in their order form.

## How it's stored

Acme does not store ACV as a separate column. It is derived:

```sql
SELECT
  subscription_id,
  customer_id,
  mrr_usd * 12 AS acv_usd
FROM `nexus-analyst-demo.acme.fact_subscriptions`
WHERE is_current = TRUE
  AND plan_tier != 'Free';
```

For Enterprise:
- The `mrr_usd` column was set as `acv_usd / 12` at contract creation. So `mrr_usd * 12` recovers ACV exactly.
- Enterprise contracts are typically annual (`billing_cycle = 'annual'`) — they pay one invoice up front; subsequent invoices are renewals.

## Where ACV is used

- **Sales pipeline.** `fact_opportunities.amount_usd` is **already ACV** for the opportunity. Do not multiply by 12. (This is a common mistake; `amount_usd` is the contract value, not MRR.)
- **Bookings.** Sum of `Closed_Won` `amount_usd` in a period = bookings ACV.
- **AE quota attainment.** Sales operations attribution uses `ae_employee_id` on the opportunity, with the ACV as the credit.

## ACV vs ARR — when they differ

For monthly customers paying month-to-month, ACV is a forward-looking annualization assuming they don't churn. For annual customers, ACV equals their actual signed contract.

ARR is the **sum of all ACVs** at a point in time, restricted to currently-active subscriptions.

## Headline buckets (Enterprise ACV bands)

Acme's Enterprise contract sizes follow a few standard tiers used for forecasting:

- $50K, $75K, $100K, $150K, $200K, $300K, $500K

These are not enforced — AEs can negotiate any value — but pricing decks anchor on these.
