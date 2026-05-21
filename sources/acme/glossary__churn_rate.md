---
title: "Glossary — Churn Rate (logo & revenue)"
source_url: "internal://acme/glossary/churn-rate"
license: "synthetic-demo"
attribution: "Acme Inc internal metric definitions (synthetic demo). Owned by FP&A (Lina Cho) and CS (Rajiv Patel)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: glossary
---

# Churn Rate (Logo & Revenue)

**One-line definition.** Churn rate measures the rate at which Acme loses customers (Logo Churn) or recurring revenue (Revenue Churn) over a specific period, typically reported on a monthly or trailing 12-month (TTM) basis.

## 1. Logo Churn Rate
Measures the percentage of the customer base that cancels their paid subscription.

**Formula:**
```
Logo Churn Rate = (Count of Paid Customers Churned in Period) / (Count of Paid Customers at Start of Period)
```

**Canonical SQL (Monthly):**
```sql
SELECT
  DATE_TRUNC(start_date, MONTH) AS churn_month,
  COUNT(DISTINCT customer_id) AS churned_logos
FROM `nexus-analyst-demo.acme.fact_subscriptions`
WHERE change_type = 'churn'
GROUP BY 1;
```
*Note: To get the rate, join this against the starting count from `dbt__model__arr_snapshot.md` for that period.*

## 2. Gross Revenue Churn Rate
Measures the percentage of ARR lost from cancellations and downgrades, excluding any offsets from expansion or new business. This is the "purest" measure of revenue leakage.

**Formula:**
```
Gross Revenue Churn = (Churned ARR + Contraction ARR) / (Starting ARR)
```

## 3. Net Revenue Churn Rate
Measures the net leakage after accounting for expansion from the existing cohort. If expansion exceeds churn + contraction, this number is negative (which is the goal).

**Formula:**
```
Net Revenue Churn = (Churned ARR + Contraction ARR - Expansion ARR) / (Starting ARR)
```
*Note: Net Revenue Churn is the inverse of NRR. If NRR is 107%, Net Revenue Churn is -7%. See `glossary__nrr.md`.*

## Voluntary vs. Involuntary Churn
Per `dbt__model__churn_cohorts.md`, we categorize churn into two buckets for executive reporting:
*   **Voluntary:** Customer initiated cancellation (competitor switch, feature gap, price).
*   **Involuntary:** Payment failures (uncollectible) or structural changes (M&A, budget cuts, company liquidation).

> **Note from @lina.cho**: We specifically bucket M&A-related churn as "Involuntary - Structural" in the finance models. If a customer is acquired and their workflows are consolidated into a parent account, we treat the child account as churned but attempt to tag the parent account with "Expansion" to keep NRR neutral.

## Trailing 12-Month (TTM) Computation
While monthly churn is useful for spotting spikes (like the Sept 2025 incident), the Board-reportable figure is the TTM Churn Rate. This smoothes out seasonal fluctuations and aligns with the logic in `dbt__model__nrr_trailing_12.md`.

## Common Pitfalls
1.  **Mixing Free and Paid:** Churn rate only applies to **Paid Customers**. A Free user stopping activity is "inactivity," not "churn" in a financial sense.
2.  **Paused Accounts:** As noted in `glossary__logo_churn.md`, accounts with `status = 'paused'` are not churned. They still hold a valid (though potentially discounted) subscription.
3.  **Timing of the Denominator:** Always use the count/ARR from the *first day* of the period. Using the average of the period artificially deflates the churn rate.

## Related Metrics
*   `glossary__logo_churn.md` — The count-based event definition.
*   `glossary__nrr.md` — The revenue-based retention view.
*   `dbt__model__account_health.md` — The leading indicators used to predict these rates.

> **Comment from @rajiv.patel**: For the Q2 2026 forecast, we are seeing a slight uptick in SMB Logo Churn due to the Pro price increase. We need to ensure the `change_type = 'churn'` rows are correctly attributed to the price-change cohort in `fact_subscriptions`.
