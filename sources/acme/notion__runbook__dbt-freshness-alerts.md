---
title: "Notion runbook — dbt freshness alert response"
source_url: "internal://acme/notion/runbook/dbt-freshness-alerts"
license: "synthetic-demo"
attribution: "Acme Inc internal data engineering documentation (synthetic demo). Owner: David Kim (Sr DE)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: notion_runbook
---

# dbt freshness alert response — on-call runbook

> **Last updated**: 2026-03-08 by david.kim
> **Owner**: David Kim (Sr Data Engineer)
> **Audience**: Data Engineering on-call, Analytics Engineers
> **SLA**: 15-minute acknowledgment, 1-hour resolution for Tier-1 marts.

This runbook covers the triage and mitigation steps for dbt freshness alerts (source or model staleness). Acme's BI warehouse depends on hourly and sub-hourly refreshes for critical finance and CS reporting. If you are paged, follow the "Triage Flow" below.

## Tier-1 Marts (High Priority)

The following models have a **<30 minute freshness SLA** (monitored via dbt Cloud + Monte Carlo). Staleness in these models triggers a P1 page to the on-call engineer.

| Model | Path | Downstream Impact |
|---|---|---|
| `arr_snapshot` | `marts/finance/arr_snapshot.sql` | `#revenue-daily` Slack bot, Board reporting |
| `account_health` | `marts/cs/account_health.sql` | `#cs-at-risk` alerts, CSM Looker boards |
| `nrr_trailing_12` | `marts/finance/nrr_trailing_12.sql` | Finance quarterly reporting |
| `workflow_runs_daily` | `marts/product/workflow_runs_daily.sql` | Product health monitoring, SRE dashboards |
| `bookings_attribution` | `marts/sales/bookings_attribution.sql` | AE Quota attainment, Marketing ROAS |

## Triage Flow

### 1. Identify the Scope
Check the alert payload in PagerDuty or the `#data-ops-alerts` channel.
- **Source Staleness**: Upstream data (Stripe, Salesforce, Segment, Product DB) hasn't landed in BigQuery.
- **Model Staleness**: Upstream data is present, but the dbt job failed or is hanging.

### 2. Check Upstream Pipelines
- **Fivetran/Airbyte**: Check the connector status for Salesforce or Zendesk.
- **Product DB (CDC)**: Check the Debezium/Kafka lag. This was the root cause of `postmortem__workflow-runs-stale-2025-09-12.md`.
- **Stripe**: Check the webhook listener logs. See `postmortem__stripe-invoice-pipeline-stuck-2026-02-04.md` if the `fact_invoices` table is lagging.

### 3. Common Root Causes & Mitigations

#### A. BigQuery Slot Exhaustion
If the dbt job is "Running" for >45 minutes without progress, check the BQ Information Schema for slot contention.
- **Symptom**: `arr_snapshot` or `nrr_trailing_12` (which are computationally heavy) are queued.
- **Mitigation**: Kill any non-essential ad-hoc queries in the `acme-bi-queries` project. If @lina.cho is running a massive backfill, coordinate a pause.

#### B. Schema Drift
- **Symptom**: dbt run fails with `Column not found` or `Type mismatch`.
- **Mitigation**: Check `#eng-deploys` to see if @tomas.vega or @hannah.miles pushed a billing system change. Update the staging model (`stg_`) to match the new schema and re-run.

#### C. Incremental Logic Failure
- **Symptom**: `workflow_runs_daily` fails during the `MERGE` statement.
- **Mitigation**: This usually happens if the `unique_key` is violated due to late-arriving CDC data. Perform a full-refresh on the affected partition:
  `dbt run --select workflow_runs_daily --full-refresh` (Warning: this is expensive, only do it for the specific model).

## Incident History (Reference)

- **`postmortem__workflow-runs-stale-2025-09-12.md`**: CDC pipeline stalled for 6 hours. Resulted in `fact_workflow_runs` showing 0 activity for all customers. Freshness threshold was reduced from 8h to 4h after this.
- **`postmortem__stripe-invoice-pipeline-stuck-2026-02-04.md`**: Stripe API version change broke the invoice ingestion. `fact_subscriptions` and `fact_invoices` were stale for 14 hours. Added `invoice_id` foreign key checks to the staging layer as a result.

## Escalation Path

If the issue is not resolved within 60 minutes:
1. Post a status update in `#data-help`.
2. @-mention @david.kim (Data Eng) and @priya.anand (VP Eng) if it's a platform-wide outage.
3. If finance reporting is impacted (especially near month-end), notify @lina.cho (FP&A) so she can delay the board-deck export.

## Post-Resolution
1. Trigger a manual refresh of the affected Looker PDTs (Persistent Derived Tables).
2. Update the "Recently added / changed" table in `notion__data-warehouse-conventions.md`.
3. If the outage lasted >2 hours, a brief postmortem is required.

---

### Internal Comments

> **2026-03-08** — `david.kim`: Updated Tier-1 list to include `bookings_attribution` now that Marketing spend is live.
>
> **2026-02-05** — `david.kim`: Added the Stripe incident reference. We need to be much faster on webhook failures.
>
> **2025-12-04** — `priya.anand`: Please ensure the on-call rotation is synced with the Engineering schedule. No more "ghost" pages.
