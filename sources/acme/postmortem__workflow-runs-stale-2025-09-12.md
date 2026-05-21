---
title: "Postmortem — fact_workflow_runs stale (2025-09-12)"
source_url: "internal://acme/postmortem/2025-09-12-workflow-runs-stale"
license: "synthetic-demo"
attribution: "Acme Inc internal postmortem (synthetic demo). Author: David Kim."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: postmortem
---

# Postmortem — `fact_workflow_runs` stale ~14h (2025-09-12)

**Author**: @david.kim (Sr Data Engineer)
**Date**: 2025-09-15 (drafted), 2025-09-19 (final)
**Severity**: Sev 2 (warehouse-only, no customer-facing impact)
**Duration of stale data**: 14h 6m (12:08 UTC 2025-09-11 → 02:14 UTC 2025-09-12 detection; backfill complete 10:30 UTC 2025-09-12)

## Summary

Salesforce OAuth token used by the `acme_workflow_runs_load` Airflow DAG expired during a scheduled 90-day rotation. The DAG failed at 12:30 UTC 2025-09-11 and did not retry because PagerDuty was not configured for that rotation. The dbt freshness alert fired at 02:14 UTC 2025-09-12 (14h after last successful load). Engineer rotated the token manually, kicked off backfill, full freshness restored by 10:30 UTC.

Customer-facing impact: **none directly**. Internal CS at-risk dashboard ran on stale data overnight, generating 3 false-positive at-risk alerts in `#cs-at-risk`. CS team manually disregarded.

## Timeline (UTC)

| Time | Event |
|---|---|
| 2025-09-11 12:08 | Last successful warehouse refresh of `fact_workflow_runs` |
| 2025-09-11 12:30 | DAG `acme_workflow_runs_load` failed (SFDC auth error) |
| 2025-09-11 12:30-02:14 | Failed DAG sat without retry; no PagerDuty page configured for this rotation |
| 2025-09-12 02:14 | dbt freshness alert fired (8h threshold) → posted to `#data-platform` |
| 2025-09-12 07:32 | @david.kim acknowledged + began investigation |
| 2025-09-12 08:12 | Root cause confirmed: SFDC OAuth token expired; manual rotation completed |
| 2025-09-12 08:24 | CS team notified to disregard overnight at-risk alerts |
| 2025-09-12 10:30 | Backfill completed; warehouse fully fresh |

## Root cause

SFDC OAuth tokens used by the production warehouse-loader DAG rotate every 90 days. The previous rotation was on 2025-06-12. The next rotation date (2025-09-10) was not on any team calendar; nor was it auto-rotated by our Vault setup.

When the token expired, the DAG's first run after expiry failed cleanly. Airflow's retry policy is 3 retries with 10-minute backoff, all of which used the same expired token, all failing. After exhausting retries, Airflow paged its on-call — but the on-call rotation was misconfigured to not include the data-platform DAG failures. (Product on-call was paged; they correctly said "not mine" and went back to bed.)

## Contributing factors

1. **Manual OAuth rotation calendar.** No automation for SFDC token refresh.
2. **PagerDuty rotation gap.** Data-platform DAG failures had no on-call assignee for night-time pages.
3. **dbt freshness was the only alert that fired.** It worked as designed (8h staleness → alert), but 8h is too long for a critical fact table.
4. **No alerting on Airflow DAG failure itself** — only on downstream symptoms (data freshness).

## Action items

| # | Action | Owner | Due | Status |
|---|---|---|---|---|
| 1 | Add SFDC OAuth tokens to Vault auto-rotation | David Kim | 2025-09-30 | done |
| 2 | Configure PagerDuty rotation for data-platform DAG failures | Jordan Hayes | 2025-09-22 | done |
| 3 | Reduce dbt freshness alert threshold for `fact_workflow_runs` to 4h warn / 6h error | David Kim | 2025-09-19 | done |
| 4 | Add Airflow DAG-failure → PagerDuty integration | David Kim | 2025-10-15 | done |
| 5 | Maintain shared "secrets-rotation" calendar for everything not auto-rotated | Tomás Vega | 2025-10-01 | done |

## What went well

- dbt freshness alert worked exactly as designed (caught the staleness).
- David's response was fast (~5h after page → fully resolved).
- CS team's morning standup caught the false-positive at-risk alerts before any customer outreach happened.

## What didn't go well

- The 14-hour gap between failure and alert was unacceptable for a critical fact table.
- The misconfigured PagerDuty rotation should have caught this.
- We discovered the SFDC rotation calendar was effectively in one engineer's head.

## Related

- `slack__incident__workflow-runs-stale-2025-09-12.md`
- `notion__on-call-rotation.md`
- `dbt__model__workflow_runs_daily.md`
