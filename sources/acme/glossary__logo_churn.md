---
title: "Glossary — Logo churn"
source_url: "internal://acme/glossary/logo-churn"
license: "synthetic-demo"
attribution: "Acme Inc internal metric definitions (synthetic demo). Owned by FP&A (emp_060) and CS (emp_040)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: glossary
---

# Logo churn

**One-line definition.** A paid customer that transitioned from `active` to `churned` during a period. Tracked at the **logo (customer)** level, distinct from MRR churn.

**Canonical SQL** (logos churned in a calendar quarter):

```sql
SELECT
  FORMAT_DATE('%Y-Q%Q', start_date) AS quarter,
  COUNT(DISTINCT customer_id) AS churned_logos
FROM `nexus-analyst-demo.acme.fact_subscriptions`
WHERE change_type = 'churn'
GROUP BY 1
ORDER BY 1;
```

The `change_type = 'churn'` event row marks the moment of churn. Its `start_date` is the churn date.

## Logo churn rate

```
logo_churn_rate = churned_logos_in_period / paid_logos_at_period_start
```

We typically annualize quarterly logo churn (×4) for board reporting. SMB churns more than MM/Ent; we report them split out.

## Voluntary vs involuntary churn

We do **not** distinguish voluntary (customer cancelled) vs involuntary (payment failed → uncollectible) at the warehouse level. CS owns the qualitative reason and tags it manually in the CRM (Salesforce). FP&A pulls the reason in a downstream dbt model: `dbt/models/marts/cs/churn_reasons.sql`.

If you need a proxy: a churn preceded by ≥1 `uncollectible` invoice in the prior 60 days is likely involuntary.

```sql
WITH churns AS (
  SELECT customer_id, start_date AS churn_date
  FROM `nexus-analyst-demo.acme.fact_subscriptions`
  WHERE change_type = 'churn'
),
uncollectible AS (
  SELECT customer_id, MAX(invoice_date) AS last_uncollectible_date
  FROM `nexus-analyst-demo.acme.fact_invoices`
  WHERE status = 'uncollectible'
  GROUP BY customer_id
)
SELECT
  c.customer_id,
  c.churn_date,
  u.last_uncollectible_date,
  DATE_DIFF(c.churn_date, u.last_uncollectible_date, DAY) AS days_between
FROM churns c
LEFT JOIN uncollectible u USING (customer_id)
WHERE u.last_uncollectible_date IS NOT NULL
  AND DATE_DIFF(c.churn_date, u.last_uncollectible_date, DAY) BETWEEN 0 AND 60;
```

## Don't double-count paused

`paused` accounts are NOT churned. They have a current paid subscription with `mrr_usd > 0`. If a paused account later churns, you'll see a `change_type = 'churn'` event at that time.

## Headline (as of 2026-05-04)

~45 churned logos cumulative over Acme's lifetime. Trailing-12-month logo churn rate hovers around ~5-6% annualized for SMB; ~2% for MM; <1% for Ent.
