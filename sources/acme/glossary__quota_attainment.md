---
title: "Glossary — Quota Attainment"
source_url: "internal://acme/glossary/quota-attainment"
license: "synthetic-demo"
attribution: "Acme Inc internal metric definitions (synthetic demo). Owned by Sales Ops (emp_025)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: glossary
---

# Quota Attainment

**One-line definition.** Quota attainment is the percentage of an Account Executive's (AE) assigned sales target (quota) achieved through Closed_Won opportunities within a specific fiscal period.

**Canonical SQL.**

```sql
SELECT
  ae_employee_id,
  SUM(bookings_acv_usd) AS total_bookings_usd,
  MAX(quota_usd) AS assigned_quota_usd,
  SAFE_DIVIDE(SUM(bookings_acv_usd), MAX(quota_usd)) AS attainment_pct
FROM `nexus-analyst-demo.acme.marts.sales.bookings_attribution`
-- Quota data currently lives in a seed file joined at the reporting layer
GROUP BY 1;
```

## Methodology

At Acme, we measure attainment against **Annual Contract Value (ACV)**. 
- **Numerator**: The sum of `bookings_acv_usd` from `fact_opportunities` where `stage = 'Closed_Won'` and the `close_date` falls within the period.
- **Denominator**: The AE's assigned quota for that period (Quarterly or Annual).

### Ramp Quotas
New AEs do not carry full quotas immediately. We apply a "ramp" schedule (typically 3-6 months depending on segment) where the denominator is reduced. Attainment for ramping AEs is reported both as "Actual vs. Ramp" and "Actual vs. Full" for performance tracking.

### Team-Sold Deals
For Enterprise deals involving multiple AEs or an overlay (e.g., a specialist), credit is split according to the `opportunity_splits` table in Salesforce (mirrored to the warehouse in 2026-H2, currently manual). In the absence of split data, 100% credit defaults to the `ae_employee_id` listed on the opportunity.

## Headline Performance (Q1 2026)

As of the Q1 2026 close, the blended attainment across all quota-carrying AEs was **~94%**. 
- **Mid-Market (MM)**: 98% (Strong performance in seat expansions).
- **Enterprise (Ent)**: 89% (Two large deals slipped from March to April).
- **SMB**: 95% (High volume, consistent velocity).

## Common Pitfalls

1. **MRR vs ACV**: Never use `mrr_usd` to compute attainment. Quotas are set in annual terms. Always use `bookings_acv_usd`. See `slack__data-help__opp-amount-vs-mrr.md`.
2. **Timing of Credit**: Credit is recognized based on `closed_won_at`. If a deal is signed on the last day of the quarter but the Salesforce stage isn't updated until the following Monday, it will fall into the next quarter's attainment. No exceptions are made for "late clicks."
3. **Churn/Contraction**: Quota attainment measures *New Bookings* and *Expansion Bookings*. It does not typically account for churn or contraction in the AE's existing book (that is captured in NRR, owned by CS).

## Related Metrics

- **Bookings ACV** = Total annualized value of won deals.
- **Sales Cycle Days** = Duration from opportunity creation to attainment.
- **Pipe Coverage** = The ratio of open pipeline to remaining quota (target is 3x).

## Owner
This metric is owned by **@jorge.martinez** (Sales Ops). For quota adjustments or dispute resolution regarding deal attribution, please file a ticket in `#sales-ops-help`.

## Related Docs
- `dbt__model__bookings_attribution.md`
- `glossary__arr.md`
- `notion__pricing-tiers.md` (for discount impact on ACV)
