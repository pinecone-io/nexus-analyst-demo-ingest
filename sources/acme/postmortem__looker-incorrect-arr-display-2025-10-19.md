---
title: "Postmortem — Looker dashboard showing stale ARR 2025-10-19"
source_url: "internal://acme/postmortem/looker-incorrect-arr-display-2025-10-19"
license: "synthetic-demo"
attribution: "Acme Inc internal postmortem (synthetic demo). Owner: David Kim (Sr DE)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: postmortem
---

# Postmortem — Looker dashboard showing stale ARR 2025-10-19

**Incident Date**: 2025-10-19  
**Author**: @david.kim  
**Status**: Finalized  
**Impact**: Executive/CS reporting inaccuracy for ~36 hours. One customer-facing discrepancy during a QBR.

## Summary

On 2025-10-19, the "Executive Daily" and "CS Account Health" Looker dashboards displayed ARR and MRR figures that were approximately 36 hours out of date. While the underlying BigQuery warehouse tables (specifically `marts/finance/arr_snapshot`) had refreshed correctly, a Looker Persistent Derived Table (PDT) used for currency conversion and cohort grouping failed to trigger its rebuild. This resulted in @marco.chen presenting stale expansion data to Halcyon Research (`cust_000087`) during a QBR. The customer noticed the mismatch between the dashboard and their recent invoice, leading to a follow-up clarification call.

## Timeline (UTC)

- **2025-10-18 06:30**: `dbt__model__arr_snapshot.md` runs successfully in BigQuery.
- **2025-10-18 07:00**: Looker PDT `pdt_arr_reporting_base` fails to trigger. The trigger SQL was tied to a dbt job ID that had been paused during the Q4 directory reshuffle.
- **2025-10-19 14:00**: @marco.chen begins QBR with Halcyon Research (`cust_000087`).
- **2025-10-19 14:20**: Customer (Halcyon Research VP Ops) points out that the "Current ARR" shown in the slide (sourced from Looker) does not reflect the 100-seat expansion they signed 48 hours prior.
- **2025-10-19 15:15**: @marco.chen pings `#data-help` reporting the discrepancy.
- **2025-10-19 15:45**: @david.kim investigates and identifies that the Looker PDT is showing `last_regen_at` from 2025-10-17.
- **2025-10-19 16:10**: Manual PDT rebuild triggered. Dashboards updated.
- **2025-10-19 17:00**: Clarification email sent to `cust_000087` with corrected figures.

## Root Cause

The root cause was a **stale Looker datagroup trigger**. 

In LookML, the `pdt_arr_reporting_base` table uses a `datagroup_trigger` that queries the `information_schema` of the BigQuery dataset to check for the completion of the dbt production job. During the Q4 directory reshuffle (see `dbt__model__arr_snapshot.md` TODOs), the dbt job name was changed from `prod_daily_exec` to `prod_daily_finance`. 

The Looker trigger SQL was still looking for the old job name. Because the old job was "paused" rather than deleted, the trigger SQL returned a static timestamp from the last successful run of the *old* job, leading Looker to believe no new data was available to justify a rebuild.

## Impact

- **External**: Halcyon Research (`cust_000087`) experienced a minor loss of confidence in Acme's reporting accuracy. They are a high-value Business tier customer (~$180K ARR).
- **Internal**: All CSMs and AEs viewing dashboards on 2025-10-18 and 2025-10-19 saw revenue figures that excluded the previous day's bookings.
- **Data Team**: 3 hours of investigation and remediation.

## Corrective Actions

1. **PDT Trigger Refactor**: Moved away from job-name-based triggers. All revenue-related PDTs now use a `sql_trigger_value` that selects `MAX(snapshot_date)` from `nexus-analyst-demo.acme.arr_snapshot`. This ensures Looker rebuilds as soon as the dbt model finishes, regardless of job naming.
2. **Staleness Alerting**: @david.kim implemented a new Looker "System Activity" alert. If any PDT in the `finance` or `cs` explores is older than 24 hours, an alert is sent to `#data-ops`.
3. **Documentation Update**: Updated `notion__data-warehouse-conventions.md` to include a section on Looker PDT dependencies and the requirement to check LookML triggers when renaming dbt models or jobs.

## Gong Transcript Snippet (Call: `cust_000087` QBR)

**TIME**: 20:15  
**SPEAKER (Marco Chen)**: "And as you can see on the health dashboard here, your current ARR is sitting at $162,000, which reflects the stability we've seen over the last quarter."  
**SPEAKER (Customer - Halcyon Research)**: "Wait, Marco, that's not right. We just added 100 seats on Thursday. Our internal procurement dashboard shows us at roughly $180k now. Did that not go through?"  
**SPEAKER (Marco Chen)**: "Oh, let me check the subscription tab... Ah, I see the expansion in the system here. It looks like this specific dashboard view might be lagging. My apologies, I'll get a corrected snapshot to you after this call."

## Related Docs
- `dbt__model__arr_snapshot.md`
- `notion__data-warehouse-conventions.md`
- `glossary__arr.md`
