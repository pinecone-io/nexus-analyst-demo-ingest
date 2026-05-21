---
title: "Glossary — Lifetime Value (LTV)"
source_url: "internal://acme/glossary/ltv"
license: "synthetic-demo"
attribution: "Acme Inc internal metric definitions (synthetic demo). Owned by FP&A (emp_060)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: glossary
---

# LTV — Lifetime Value

**One-line definition.** LTV is an estimate of the total gross profit Acme expects to earn from a customer over the duration of their relationship with the platform.

**Canonical Formula.**
At Acme, we use the standard SaaS formula for LTV:

$$LTV = \frac{ARR \times Gross\ Margin\ \%}{Logo\ Churn\ Rate}$$

## Component Definitions

1.  **ARR**: Annual Recurring Revenue. We use the current snapshot from `dbt__model__arr_snapshot.md`.
2.  **Gross Margin %**: For the purposes of LTV modeling, FP&A assumes a fixed **80% Gross Margin**. This accounts for COGS (hosting on GCP/BigQuery, third-party API costs for integrations, and support headcount).
3.  **Logo Churn Rate**: The annualized rate at which customers churn. We derive this from the trailing 12-month (TTM) logo churn figures. See `glossary__logo_churn.md`.

## Canonical SQL (Blended LTV)

```sql
WITH metrics AS (
  SELECT
    arr_usd,
    paying_customers,
    SAFE_DIVIDE(arr_usd, paying_customers) AS avg_arr_per_logo
  FROM `nexus-analyst-demo.acme.marts_finance_arr_snapshot`
),
churn AS (
  -- Annualized logo churn rate from the last 12 months
  SELECT
    SAFE_DIVIDE(COUNT(DISTINCT customer_id), 800) AS annualized_churn_rate -- 800 is approx base
  FROM `nexus-analyst-demo.acme.fact_subscriptions`
  WHERE change_type = 'churn'
    AND start_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR)
)
SELECT
  m.avg_arr_per_logo AS arpa,
  0.80 AS assumed_gm,
  c.annualized_churn_rate,
  SAFE_DIVIDE(m.avg_arr_per_logo * 0.80, c.annualized_churn_rate) AS blended_ltv_usd
FROM metrics m, churn c;
```

## Important Nuances & Caveats

*   **Sensitivity to Churn**: LTV is highly sensitive to the churn rate denominator. Because Acme's Enterprise churn is near-zero, the "Lifetime" for Enterprise customers can mathematically appear to be 50+ years. We typically cap the "Lifetime" at 7 years for conservative modeling in board decks.
*   **Gross Margin Assumption**: The 80% figure is a blended estimate. Pro tier customers (self-serve) actually have higher margins (~85%) than Business/Enterprise customers who require dedicated CSMs and higher support touch.
*   **Expansion (NRR) vs. LTV**: This formula uses Logo Churn. It does not account for the fact that a customer's ARR grows over time (Expansion). For a more holistic view that includes expansion, see `glossary__nrr.md`.
*   **Tiered LTV**: Blended LTV is often misleading because Business tier ARR (~$149/seat) is significantly higher than Pro (~$49/seat). FP&A maintains a per-tier LTV breakdown in the "Unit Economics" tab of the Master Finance Model.

## Related Metrics & Docs

*   `glossary__arr.md`: The revenue input for the numerator.
*   `glossary__logo_churn.md`: The primary denominator for the "Lifetime" component.
*   `dbt__model__arr_snapshot.md`: The source table for current ARPA (Average Revenue Per Account) calculations.
*   `dbt__model__nrr_trailing_12.md`: Used to contrast logo-based retention with revenue-based retention.
*   `glossary__cac.md`: (Customer Acquisition Cost) Usually paired with LTV to compute the LTV:CAC ratio (Target: >3.0).

## Headline (as of 2026-05-04)

Based on a ~$39M ARR book and ~5-6% annualized logo churn in the SMB/Pro segment, our blended LTV across the whole company is approximately **$410k**, though this is heavily skewed by the high ACV of Business and Enterprise accounts. Pro-only LTV is significantly lower (~$12k).
