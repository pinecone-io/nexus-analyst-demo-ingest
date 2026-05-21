---
title: "Notion DRAFT — Value Realization Score (VRS) model spec — WIP"
source_url: "internal://acme/notion/drafts/value-realization-score-spec"
license: "synthetic-demo"
attribution: "Acme Inc Notion draft (synthetic demo). NOT RELEASED — work-in-progress spec, do not implement against this."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: notion_runbook
---

# Value Realization Score — model spec (DRAFT)

> ⚠️ **DRAFT — DO NOT IMPLEMENT**
>
> Owner: @dan.lee + @elena.volkov
> Created: 2026-03-20
> Status: scoping, design TBD
> Target ship: 2026-H1 (likely 2026-Q3 realistically)
>
> 🚧 nothing in this doc is final. half-baked at best. -dan

## Why are we doing this

The current "engaged customer" flag (≥3 active users + ≥10 successful runs in 28d) is a good FLOOR but a poor measure of actual value realization. Customers can be "engaged" by the threshold and still be dramatically under-utilizing the product. Conversely, some customers are slightly under the threshold but extremely deep on a single use case and not at risk at all.

We want a continuous score (0-100) that better predicts renewal probability and expansion potential.

> Reference: see `postmortem__engagement-threshold-recalibration-2025-Q4.md` for the analysis that motivated this. Specifically the data point that "engaged" customers had renewal rates of 88% vs an investor-expected 92-95% on a healthy SaaS book.

## Goals

1. Per-customer score 0-100 updated daily
2. Better churn prediction than the binary engaged flag (target: AUC > 0.80 vs ~0.65 for binary)
3. Identify expansion candidates (currently CSM intuition, want to make data-driven)
4. Surface qualitative signals (NPS, ticket sentiment) alongside quantitative

## Out of scope (for v1)

- Per-team or per-workflow scoring
- Real-time scoring (daily is fine for v1)
- Forecasting expansion DOLLARS (just probability)
- Replacement of the engaged-customer flag (we keep both)

## Inputs (proposed)

| Signal | Source | Weight (initial) |
|---|---|---|
| Active users 28d | `fact_user_events` | 15 |
| Successful runs 28d | `fact_workflow_runs` | 15 |
| Unique workflows used 28d | `fact_workflow_runs` | 10 |
| Run success rate 28d | `fact_workflow_runs` | 10 |
| Seat utilization | derived | 10 |
| NPS most recent | `fact_nps_responses` | 10 |
| P1 tickets in last 90d | `fact_support_tickets` | -10 |
| Uncollectible invoices | `fact_invoices` | -15 |
| Champion login recency | `fact_user_events` (admin user) | 10 |
| Workflow build velocity (new workflows / month) | `fact_user_events` workflow_created | 5 |

> 🚧 weights are GUESSES. need to fit on actual churn data. ML model? logistic regression? not sure yet. probably start with logistic since it's interpretable.

> 🚧 also "champion" needs to be defined. currently we don't have a "champion" field on customers. the closest is the primary admin (first admin user) but champions can change over time. need to think about this.

## Output schema (proposed)

```sql
-- New mart model: marts/cs/value_realization_score.sql
CREATE TABLE acme.marts.value_realization_score AS
SELECT
  customer_id,
  CURRENT_DATE() AS snapshot_date,
  vrs_score INT64,                  -- 0-100
  vrs_band STRING,                  -- 'critical' / 'at_risk' / 'stable' / 'healthy' / 'champion'
  signal_breakdown_json STRING,     -- per-signal contribution as JSON
  predicted_renewal_probability FLOAT64,
  vrs_score_30d_trend INT64,        -- delta vs 30 days ago
  ...
;
```

## Validation plan

1. Backfill VRS for all customers as of every quarter for the last 24 months
2. For each cohort: compare VRS at quarter start to actual churn outcome by quarter end
3. Compute AUC. Target: > 0.80
4. Iterate on weights / signals if AUC < 0.80
5. Once landed, run the model in shadow mode for 2 quarters before flipping over to authoritative

## Risk register

- **Risk: weights drift over time and we don't notice**. Mitigation: quarterly re-fit, baked into review cadence.
- **Risk: VRS becomes a vanity metric that CSMs game**. Mitigation: don't tie comp to it.
- **Risk: data quality issues in source signals propagate to VRS**. Mitigation: each signal has its own dbt freshness alert.

## Open questions

- Should VRS be normalized within plan tier or absolute? E.g., is a 60 on Pro the same as 60 on Enterprise? Probably should be plan-relative but TBD.
- Should we expose VRS to customers? (Probably not in v1 — too many edge cases.)
- Should expansion potential be a separate score, or one signal in the composite? Maybe separate.

## Sub-pages (to be created)

- [VRS — signal definitions deep-dive] (TBD)
- [VRS — backfill methodology] (TBD)
- [VRS — model selection (LR vs gradient boost vs ?)] (TBD)
- [VRS — CSM workflow integration] (TBD)

## Related pages

- `notion__csm-account-health-runbook.md` — current health playbook (will be updated when VRS ships)
- `glossary__engaged_customer.md` — threshold this replaces (well, supplements)
- `postmortem__engagement-threshold-recalibration-2025-Q4.md` — motivating analysis
- `dbt__model__account_health.md` — current health model that VRS will eventually subsume

## Comments / chat

> **2026-04-22** — `dan.lee`: parking this for now. need to focus on AI Workflow Assistant beta launch first. will revisit late Q2.

> **2026-04-08** — `elena.volkov`: love the framing. worried about the "expansion potential" being conflated with churn risk. those are related but distinct. let's tease apart in v2.

> **2026-03-22** — `david.kim`: from a data-eng perspective, daily refresh is fine. signal_breakdown_json could get unwieldy — consider whether each signal needs to be its own column for queryability. agree the score should be plan-relative.

> **2026-03-20** — `dan.lee`: initial draft. asking for input from elena, david, marco.

---

> 🚧 If this doc has been here >6 months without progressing, ping me and ask if we still care. -dan
