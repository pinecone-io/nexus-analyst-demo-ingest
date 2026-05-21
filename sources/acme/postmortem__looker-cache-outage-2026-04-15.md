---
title: "Postmortem — Looker cache outage 2026-04-15"
source_url: "internal://acme/postmortem/looker-cache-outage-2026-04-15"
license: "synthetic-demo"
attribution: "Acme Inc internal postmortem (synthetic demo). Author: David Kim (Sr DE)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: postmortem
---

# Postmortem — Looker cache outage 2026-04-15

**Status**: Finalized
**Incident Date**: 2026-04-15
**Authors**: @david.kim (Data Engineering)
**Stakeholders**: @elena.volkov (VP CS), @dan.lee (Product), @priya.anand (VP Eng)

## Summary

On 2026-04-15, a failure in the Looker query cache mechanism caused all dashboard tiles to bypass the cache and execute live against the BigQuery warehouse. This resulted in significant performance degradation, specifically for the **CS Account Health** dashboard, which timed out for all users. This incident occurred during the peak Monday morning CSM review window, preventing the Customer Success team from executing their weekly account health cadence as defined in `notion__csm-account-health-runbook.md`.

The root cause was a schema-cache invalidation cascade triggered by a dbt rebuild of `dbt__model__account_health.md` which coincided with a Looker PDT (Persistent Derived Table) refresh failure.

## Timeline (all times UTC)

- **06:30**: Nightly dbt production run completes. `marts/cs/account_health.sql` is materialized as a table.
- **08:00**: CSMs begin logging in for the Monday morning review.
- **09:14**: **Incident Detected.** @marco.chen reports in `#data-help` that the Account Health dashboard is spinning indefinitely and eventually timing out with a "Gateway Timeout" error.
- **09:25**: @david.kim confirms BigQuery slot utilization is spiking. Looker is sending ~40 concurrent executions of the gnarly join logic in `dbt__model__account_health.md` instead of serving from cache.
- **09:40**: Investigation reveals that the `datagroup` associated with the CS Explore was stuck in a "triggered" state, forcing every user refresh to bypass the cache.
- **10:10**: Attempted manual cache clear via Looker Admin panel. Ineffective; invalidation loop continues.
- **10:42**: **Mitigation.** @david.kim manually pins the `persist_for` parameter on the Account Health dashboard to 1 hour, overriding the broken datagroup trigger. Dashboard responsiveness returns to normal.
- **11:00**: Incident resolved. CSM team notified to resume reviews.

## Root Cause Analysis

The incident was caused by a "cache invalidation cascade." 

Acme uses a Looker `datagroup` that triggers when the `last_modified_time` of `nexus-analyst-demo.acme.account_health` changes in BigQuery. On 2026-04-15, the dbt rebuild at 06:30 UTC successfully updated the table, but a secondary Looker PDT (used for legacy CSM mapping) failed to refresh due to a transient network error. 

Because the PDT was a dependency for the Explore but had a "stale" status, Looker's query planner determined that the entire cache for the Account Health model was invalid. Every time a CSM opened the dashboard, Looker attempted to re-run the full SQL from `dbt__model__account_health.md`. As noted in the model docs, this query joins 6 tables and is currently unpartitioned, making it expensive to run concurrently. The resulting BigQuery queue depth caused the 60-second Looker proxy timeout to fire.

## Impact

- **CS Team**: ~15 CSMs were unable to access health signals for approximately 90 minutes during their primary weekly workflow.
- **Warehouse**: BigQuery slot usage spiked to 2,000 slots (100% of our reservation), causing minor latency for other scheduled finance reports (e.g., `dbt__model__arr_snapshot.md`).
- **Data Trust**: High. Multiple CSMs expressed frustration that the "Monday Morning Bot" in `#cs-at-risk` was posting alerts they couldn't verify in the UI.

## Lessons Learned

1. **Unpartitioned Joins are a Liability**: The performance notes in `dbt__model__account_health.md` already flagged the join chain as slow. This incident proved that we cannot rely on the cache to mask poor query performance for mission-critical dashboards.
2. **Datagroup Fragility**: Tying cache invalidation strictly to table updates without a "stale-while-revalidate" grace period creates a single point of failure when upstream PDTs or dbt models have minor metadata mismatches.
3. **CSM Criticality**: The Monday 08:00-10:00 UTC window is "Tier 1" uptime for the data team. We should treat it with the same rigor as a board-reporting deadline.

## Action Items

| Task | Owner | Due Date | Status |
|---|---|---|---|
| Refactor `marts/cs/account_health.sql` to use partitioning by `customer_id` | @david.kim | 2026-04-30 | In Progress |
| Implement `persist_for: "1 hour"` hard-coding for the CS Explore to decouple from datagroup triggers | @david.kim | 2026-04-16 | **Done** |
| Add dbt-freshness alerts for `stg_support_tickets` to catch upstream join delays earlier | @david.kim | 2026-04-20 | **Done** |
| Update `notion__csm-account-health-runbook.md` with a "Dashboard Down" fallback procedure | @elena.volkov | 2026-05-01 | Pending |

## Slack Thread Context

> **#data-help** (2026-04-15 09:15)
> **@marco.chen**: Is Looker down? Account Health dashboard is just spinning. I've got 4 EBRs today and I can't see the utilization trends. 
> **@david.kim**: Looking. BQ is getting hammered. It looks like the cache is being bypassed.
> **@elena.volkov**: This is the third time in two months we've had Monday morning lag. We need a permanent fix for the CS team.
> **@david.kim**: Working on a mitigation now. I'm going to force-pin the cache for an hour so you guys can get through the morning.
> **@priya.anand**: @david.kim let's do a full postmortem on why the invalidation triggered. We shouldn't be running 40x joins on `fact_workflow_runs` simultaneously.
