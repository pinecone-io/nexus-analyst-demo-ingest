---
title: "Saved query — Open pipeline by AE (with weighted variant)"
source_url: "internal://acme/query_log/2026-04-30-open-pipeline-by-ae"
license: "synthetic-demo"
attribution: "Acme Inc analyst saved-query log (synthetic demo)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: query_log
---

# Saved query — Open pipeline by AE

**Asker**: @marcus.webb (VP Sales)
**Author**: @jorge.martinez (Sales Ops)
**Run on**: 2026-04-30 16:00 UTC

> Jorge's note: "marcus runs this every Monday for pipeline review. saving here. weighted-variant below."

## SQL — unweighted

```sql
SELECT
  e.full_name AS ae_name,
  o.stage,
  COUNT(*) AS n_opps,
  ROUND(SUM(o.amount_usd), 0) AS pipeline_acv_usd
FROM `nexus-analyst-demo.acme.fact_opportunities` o
JOIN `nexus-analyst-demo.acme.dim_employees` e
  ON o.ae_employee_id = e.employee_id
WHERE o.stage NOT IN ('Closed_Won', 'Closed_Lost')
  AND e.is_active = TRUE
GROUP BY 1, 2
ORDER BY ae_name, stage;
```

## SQL — weighted by stage probability

```sql
-- Same query, but multiply ACV by stage probability for weighted pipeline.
-- Stage probabilities live in `notion__sales-pipeline-stage-definitions.md`.
-- Don't change the probabilities here without updating that doc.
SELECT
  e.full_name AS ae_name,
  ROUND(SUM(
    o.amount_usd * CASE o.stage
      WHEN 'Prospecting' THEN 0.10
      WHEN 'Qualified' THEN 0.25
      WHEN 'Proposal' THEN 0.50
      WHEN 'Negotiation' THEN 0.75
      ELSE 0
    END
  ), 0) AS weighted_pipeline_acv_usd,
  COUNT(*) AS n_open_opps
FROM `nexus-analyst-demo.acme.fact_opportunities` o
JOIN `nexus-analyst-demo.acme.dim_employees` e
  ON o.ae_employee_id = e.employee_id
WHERE o.stage NOT IN ('Closed_Won', 'Closed_Lost')
  AND e.is_active = TRUE
GROUP BY 1
ORDER BY weighted_pipeline_acv_usd DESC;
```

## Notes

- `o.amount_usd` is **already ACV** — do NOT multiply by 12 (see `slack__data-help__opp-amount-vs-mrr.md`).
- Filtered to only **active** AEs (`dim_employees.is_active = TRUE`) — terminated AEs may still have orphan opp records that get reassigned.
- Open stages: Prospecting, Qualified, Proposal, Negotiation.
- Weighted pipeline assumes the stage probabilities are calibrated. They're reviewed quarterly. Last calibration: 2025-12.

## Reused by

- Sales weekly pipeline review (Mondays 10 AM PT)
- Quarterly forecast roll-up
- AE 1:1s
