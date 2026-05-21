---
title: "Glossary — Pipeline Coverage"
source_url: "internal://acme/glossary/pipeline-coverage"
license: "synthetic-demo"
attribution: "Acme Inc internal metric definitions (synthetic demo). Owned by Sales Ops (emp_022)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: glossary
---

# Pipeline Coverage

**One-line definition.** Pipeline coverage is the ratio of total open pipeline value to the remaining sales quota for a specific period (typically the current quarter).

**Canonical Formula.**
```
Pipeline Coverage = (Total Open Opportunity Amount) / (Remaining Quota for Period)
```

At Acme, we use **unweighted** pipeline (the full `amount_usd` of all open opportunities) for this calculation. While some teams use stage-weighted pipeline, the VP of Sales (@marcus.webb) has mandated unweighted coverage as our primary health signal to ensure AEs are focused on top-of-funnel volume.

## Target Thresholds

Acme targets a **3.0x coverage ratio** at the start of every quarter. 

| Ratio | Health | Action |
|---|---|---|
| > 4.0x | **High** | Potential for significant over-performance; check for "pipeline hoarding." |
| 3.0x - 4.0x | **Healthy** | Standard target for hitting quota based on historical win rates. |
| 2.0x - 2.9x | **At Risk** | Requires immediate SDR/AE outbound push to fill the gap. |
| < 2.0x | **Critical** | High probability of quota miss; escalate to @marcus.webb. |

## Canonical SQL (Current Quarter Coverage)

This logic is implemented in the daily Sales Ops performance suite. See `query_log__18__pipeline-coverage-by-ae.md` for the per-AE breakdown used in Monday morning standups.

```sql
WITH open_pipe AS (
  -- Sum of all open opportunities for the current quarter
  SELECT 
    ae_employee_id,
    SUM(amount_usd) AS total_open_amount
  FROM `nexus-analyst-demo.acme.fact_opportunities`
  WHERE stage NOT IN ('Closed_Won', 'Closed_Lost')
    AND close_date BETWEEN '2026-04-01' AND '2026-06-30'
  GROUP BY 1
),
quota AS (
  -- Remaining quota (simplified for this example)
  -- In production, this joins to a quota-attainment table
  SELECT 
    employee_id,
    quota_amount_usd - current_attainment_usd AS remaining_quota
  FROM `nexus-analyst-demo.acme.internal_ae_quotas`
  WHERE quarter = '2026-Q2'
)
SELECT 
  p.ae_employee_id,
  p.total_open_amount,
  q.remaining_quota,
  SAFE_DIVIDE(p.total_open_amount, q.remaining_quota) AS pipeline_coverage
FROM open_pipe p
JOIN quota q ON p.ae_employee_id = q.employee_id;
```

## Important Nuances & Caveats

- **Unweighted vs. Weighted.** We do not use "Weighted Pipeline" (Amount * Probability) for this metric. Historical analysis showed that AEs often inflate probabilities to mask low coverage. Unweighted coverage forces a conversation about raw volume.
- **The SA/SE Attribution Edge Case.** For Enterprise deals, a Solutions Architect (SA) is often assigned. We currently attribute 100% of the pipeline value to the AE (`ae_employee_id`). If an AE is "borrowing" pipeline from a shared overlay, it can artificially inflate their coverage. Sales Ops manually audits these during QBRs.
- **"Stale" Pipeline.** Pipeline coverage is only as good as the `close_date` accuracy. If an AE has $1M in pipeline with a close date of yesterday that hasn't been updated, the coverage ratio is technically "fake." We filter for `close_date < CURRENT_DATE()` in our "Hygiene" dashboards to flag this.
- **Remaining Quota.** If an AE has already hit their quota for the quarter, the denominator becomes 0 or negative. In our BI tools, we cap the denominator at $1 to avoid `div/0` errors and show the AE as "Infinite Coverage."

## Related Metrics

- **Win Rate** — If an AE's win rate is significantly lower than the 25% average, a 3x coverage ratio may still be insufficient.
- **Sales Cycle Days** — High coverage is meaningless if the `sales_cycle_days` exceeds the remaining time in the quarter. See `dbt__model__bookings_attribution.md`.
- **Engagement Score** — We are beginning to cross-reference coverage with `glossary__engaged_customer.md` to see if the pipeline is actually "warm."

## Owner
@jorge.martinez (Sales Ops) — please reach out for custom Looker tiles or adjustments to AE quota targets.
