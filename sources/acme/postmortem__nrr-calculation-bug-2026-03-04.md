---
title: "Postmortem — NRR calculation bug 2026-03-04"
source_url: "internal://acme/postmortem/nrr-calculation-bug-2026-03-04"
license: "synthetic-demo"
attribution: "Acme Inc internal postmortem (synthetic demo). Lead: Dan Lee (Product Analytics)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: postmortem
---

# Postmortem — NRR calculation bug 2026-03-04

**Status**: Completed / Restated
**Authors**: @dan.lee (Product Analytics), @david.kim (Data Engineering)
**Stakeholders**: @lina.cho (FP&A), @rachel.stein (CFO), @sam.reyes (CEO)
**Date Detected**: 2026-03-04
**Date Resolved**: 2026-03-06

## Summary

On 2026-03-04, during final reconciliation for the Q4 2025 board deck, @lina.cho (FP&A) identified a discrepancy between the automated NRR figure in `marts/finance/nrr_trailing_12` and the manual cohort analysis performed in Excel for the audit committee. 

The automated model was reporting a Trailing 12-Month (TTM) NRR of **121%**, while the manual calculation showed **114%**. The root cause was a logic error in the expansion CTE of the dbt model that double-counted MRR gains for customers who underwent both a plan tier upgrade (e.g., Pro → Business) and a seat count increase within the same reporting window.

## Impact

- **Metric Distortion**: Reported Q4 NRR was inflated by ~7 percentage points (121% vs 114%).
- **Board Communication**: A formal restatement was required for the Q4 board materials. @rachel.stein communicated the correction to the board on 2026-03-08.
- **Downstream Models**: `marts/finance/nrr_cohort_detail` was also affected, leading to incorrect expansion attribution at the account level for ~12 MM/Enterprise accounts.

## Timeline (all times UTC)

- **2026-03-04 14:15**: @lina.cho pings @dan.lee in `#data-help` regarding a $240k discrepancy in expansion MRR for the Q4 cohort.
- **2026-03-04 15:30**: @dan.lee and @david.kim begin audit of `dbt/models/marts/finance/nrr_trailing_12.sql`.
- **2026-03-04 17:00**: Bug identified in `upgrades_in_window` CTE. The logic was failing to partition delta calculations correctly when multiple `change_type` events occurred in sequence.
- **2026-03-05 09:00**: Fix developed and tested against historical snapshots.
- **2026-03-05 14:00**: PR #412 merged. Full warehouse refresh triggered.
- **2026-03-06 10:00**: Verification complete. restated figures delivered to Finance.

## Root Cause Analysis

The bug lived in Step 5 (`upgrades_in_window`) of the `nrr_trailing_12` model. The SQL was performing a simple join between a subscription and its `changed_from_subscription_id` to calculate `delta_mrr`. 

However, for customers who upgraded from Pro to Business (which triggers a `change_type = 'upgrade'`) and then added seats 15 days later (which triggers a `change_type = 'seat_change'`), the model was summing the delta from both rows without checking if the "start state" for the TTM window had already been surpassed. Essentially, the model was treating the full jump from Pro ($49) to Business ($149/seat) as expansion, and then adding the seat-count delta on top of the already-expanded base, double-counting the price-per-seat lift.

### Faulty Logic Snippet:
```sql
-- Step 5 (Old/Buggy):
upgrades_in_window AS (
  SELECT
    customer_id,
    SUM(IF(s.mrr_usd > p.mrr_usd, s.mrr_usd - p.mrr_usd, 0)) AS upgrade_delta_mrr
  FROM sub_events s
  LEFT JOIN sub_events p ON s.changed_from_subscription_id = p.subscription_id
  WHERE s.change_type IN ('upgrade', 'seat_change')
    AND s.start_date BETWEEN start_window AND as_of_date
  GROUP BY customer_id
)
```

## Resolution

The CTE was rewritten to use a window function (`LAG`) partitioned by `customer_id` and ordered by `start_date`, with an explicit check against the MRR at `start_window`. This ensures that the total expansion for a customer in the window is capped at `(End MRR - Start MRR)` if the customer remained active, rather than summing individual event deltas.

The fix was applied to `dbt__model__nrr_trailing_12.md` and the underlying SQL.

## Lessons Learned

1. **Unit Testing Boundaries**: Our existing dbt tests checked for NRR being within a 0-3.0 range, but did not have a regression test for multi-event expansion within a single window.
2. **Manual vs. Auto Reconciliation**: We relied too heavily on the automated model without periodic "spot checks" against the raw `fact_invoices` for large accounts.
3. **CTE Complexity**: The "gnarly" nature of the NRR model (as noted in `dbt__model__nrr_trailing_12.md`) makes it prone to these types of logical drift.

## Action Items

| Action Item | Owner | Status |
|---|---|---|
| Implement dbt unit test for "Multi-event expansion" scenario | @david.kim | **DONE** |
| Add `nrr_reconciliation` dashboard in Looker comparing `fact_subscriptions` delta to `fact_invoices` | @dan.lee | **IN PROGRESS** |
| Refactor `nrr_trailing_12` to use a standard `mrr_ledger` intermediate model to simplify logic | @david.kim | **H2 Backlog** |
| Audit `marts/sales/bookings_attribution` for similar double-counting logic | @jorge.martinez | **DONE** |

## Slack Thread Context (`#data-incidents`)

> **2026-03-04 14:20** @lina.cho: Hey @dan.lee, I'm looking at the Q4 NRR for the board deck. The mart says 121% but when I sum up the expansion for the top 10 MM accounts, the math isn't mathing. `cust_000281` (Aether Dynamics) is showing $12k expansion in the model but they only grew from $4k to $8k MRR in the window.
>
> **2026-03-04 14:45** @dan.lee: Investigating. It looks like Aether had an upgrade to Business AND a seat add in November. I think we're double-counting the lift. 
>
> **2026-03-04 15:10** @david.kim: Confirmed. The `upgrades_in_window` CTE is summing deltas from both rows. Since the seat add happened after the tier upgrade, the `changed_from` join is pulling the mid-point MRR, but we're not accounting for the fact that the total window delta should be anchored to the `start_window` price.
>
> **2026-03-05 10:15** @rachel.stein: Thanks for the quick catch @lina.cho. @dan.lee please let me know when the restated number is final. I need to update Sam before he pings the board. 🛑 **Hold all revenue reporting until this is merged.**
