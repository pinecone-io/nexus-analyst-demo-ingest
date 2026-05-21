---
title: "Glossary — NRR (Net Revenue Retention)"
source_url: "internal://acme/glossary/nrr"
license: "synthetic-demo"
attribution: "Acme Inc internal metric definitions (synthetic demo). Owned by FP&A (emp_060)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: glossary
---

# NRR — Net Revenue Retention

**One-line definition.** NRR measures how much of a starting cohort's recurring revenue we retained N months later, including expansion and contraction but excluding new logos acquired during the window.

**Acme convention.** We report NRR on a **trailing 12-month** basis, cohorted by **customer signup quarter**. The denominator is the cohort's MRR at the start of the window; the numerator is the same cohort's MRR at the end of the window (regardless of plan tier — including downgrades to Free, which count as churn).

```
NRR = (cohort_mrr_at_t_end) / (cohort_mrr_at_t_start)
```

## Canonical SQL (trailing 12 months as of `:as_of_date`)

```sql
DECLARE as_of_date DATE DEFAULT '2026-04-30';
DECLARE start_date DATE DEFAULT DATE_SUB(as_of_date, INTERVAL 12 MONTH);

WITH cohort AS (
  -- snapshot of MRR per customer at start of window
  SELECT customer_id, SUM(mrr_usd) AS start_mrr
  FROM `nexus-analyst-demo.acme.fact_subscriptions`
  WHERE start_date <= start_date
    AND (end_date IS NULL OR end_date > start_date)
    AND plan_tier != 'Free'
  GROUP BY customer_id
),
end_state AS (
  -- same customers, MRR at as_of_date
  SELECT customer_id, SUM(mrr_usd) AS end_mrr
  FROM `nexus-analyst-demo.acme.fact_subscriptions`
  WHERE start_date <= as_of_date
    AND (end_date IS NULL OR end_date > as_of_date)
    AND plan_tier != 'Free'
  GROUP BY customer_id
)
SELECT
  SUM(c.start_mrr) AS cohort_start_mrr,
  SUM(COALESCE(e.end_mrr, 0)) AS cohort_end_mrr,
  SAFE_DIVIDE(SUM(COALESCE(e.end_mrr, 0)), SUM(c.start_mrr)) AS nrr
FROM cohort c
LEFT JOIN end_state e USING (customer_id);
```

## Important nuances

- **Cohort is fixed.** The denominator does not change as new customers sign up. New logos in the window are tracked separately as "New ARR" (see `glossary__arr.md`).
- **Downgrades count negatively.** Pro → Free transitions reduce the cohort's end-state MRR.
- **Account merging is rare.** If two customers merge (e.g., acquisition), Finance manually adjusts. Not modeled in this warehouse.
- **The "100% line" for Acme.** NRR = 1.00 means we held the cohort flat. Investors typically want >1.10 for a healthy SaaS. As of 2026-Q1 we're at ~1.07 (synthetic figure, recompute).

## What NRR is NOT

- **Not GRR (Gross Revenue Retention).** GRR caps the numerator at the denominator (no expansion credit). Acme reports both.
- **Not logo retention.** Logo retention counts customers, not revenue.
