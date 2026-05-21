---
title: "Scratch — @david.kim dbt performance TODOs"
source_url: "internal://acme/scratch/david-dbt-perf-todos"
license: "synthetic-demo"
attribution: "Internal engineering scratchpad for Acme data team performance tracking."
fetched_at: '2026-05-10T09:15:00+00:00'
adapter: scratch_note
---

# Scratch — @david.kim dbt performance TODOs

This is my running list of model performance bottlenecks and optimization targets. The warehouse is still small (~100K rows in the largest fact), but BQ slot contention is starting to hit us during the 06:00–07:00 UTC refresh window.

## High Priority (The "Refresh Window" Blockers)

| Model | Current p95 | Target | Status | Notes |
|---|---|---|---|---|
| `marts/cs/account_health` | 45s | 15s | 🚧 In-progress | Joining 6 facts. The `support_tickets` and `nps_responses` joins are doing full scans. Need to partition the staging layers by `customer_id` or cluster. See `dbt__model__account_health.md`. |
| `marts/finance/nrr_trailing_12` | 38s | 12s | 🗓️ Backlog | The expansion/contraction CTEs (Step 5/6) are gnarly. Now that we fixed the boundary bug from 2025-Q3, I can simplify the logic. See `dbt__model__nrr_trailing_12.md`. |
| `marts/product/workflow_runs_daily` | 28s | 10s | ✅ Done | Incremental strategy is working well. Reduced window from 7d to 3d. See `dbt__model__workflow_runs_daily.md`. |
| `marts/finance/arr_snapshot` | 14s | 5s | 🚧 In-progress | The `recency_rank` window function is the bottleneck. Paranoid QC check is worth the cost, but I can probably optimize the `stg_subscriptions` filter. See `dbt__model__arr_snapshot.md`. |

## Medium Priority (Optimization & Technical Debt)

*   **`marts/sales/bookings_attribution`**
    *   **Current**: 8s
    *   **Target**: < 5s
    *   **Status**: Backlog
    *   **Note**: Fine for now, but the `ARRAY_AGG` for first-touch attribution will scale poorly once `fact_marketing_touches` hits 1M+ rows. Need to look at a persistent mapping table. See `dbt__model__bookings_attribution.md`.

*   **`marts/cs/at_risk_alerts`**
    *   **Current**: 12s
    *   **Target**: 3s
    *   **Status**: 🚧 In-progress
    *   **Note**: This is basically a filtered view of `account_health`. It shouldn't take 12s. Moving to a non-materialized view or a very slim table.

## The "One Day" List (H2 2026)

*   **VRS Model Implementation**: @dan.lee is drafting the Value Realization Score spec (`notion__draft__value-realization-score-spec.md`). If we include 10+ signals with historical backfills, this will be the new #1 bottleneck. I need to make sure the signal inputs are pre-aggregated.
*   **Partitioning Strategy**: We aren't partitioning `fact_workflow_runs` by `customer_id` yet, only by `triggered_at`. For CS/Product marts that join on `customer_id`, we're paying a shuffle tax.
*   **Stale Model Cleanup**: `marts/exec/arr_snapshot.sql` is still being called by some legacy Looker dashboards even though it's just a proxy for the new finance mart. Need to kill it.

## Notes from 2026-05-04 Sync

*   @lina.cho mentioned the NRR model is timing out occasionally when she runs ad-hoc backfills.
*   @tomas.vega says the billing system CDC might start pushing hourly updates instead of 15-min if we can't lower the load on the source DB.
*   I'm seeing a lot of `SELECT *` in the staging layers. Need to prune columns to save on BQ processed bytes.

---
**Next Review**: 2026-06-01
**Owner**: @david.kim
