---
title: "Notion — incident response runbook"
source_url: "internal://acme/notion/incident-response-runbook"
license: "synthetic-demo"
attribution: "Acme Inc internal documentation (synthetic demo). Owner: David Kim (Sr DE)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: notion_doc
---

# Incident Response Runbook (Data Team)

> **Last updated**: 2026-02-20 by david.kim
> **Owner**: David Kim (Sr Data Engineer)
> **On-call rotation**: see `notion__on-call-rotation.md`
> **Status Page**: `status.internal.acme.com`

This runbook defines how the Acme data team identifies, classifies, and resolves incidents affecting the warehouse (`nexus-analyst-demo.acme`), dbt pipelines, and downstream BI (Looker).

## Severity Definitions

| Level | Impact | Response |
|---|---|---|
| **SEV1** | Critical business blocker. Warehouse down, board-level metrics (ARR/NRR) corrupted, or >50% of workflow runs failing. | Immediate page. PagerDuty alerts @priya.anand and @david.kim. Comms every 30m. |
| **SEV2** | Significant disruption. dbt freshness > 8h, Looker dashboards timing out for Sales/CS, or specific integration syncs (Stripe/SFDC) broken. | Page on-call during business hours (or 08:00 UTC if overnight). Comms every 2h. |
| **SEV3** | Minor/Isolated. One non-core model stale, minor schema drift in `dim_employees`, or ad-hoc query latency. | Slack notification to `#data-ops`. Resolve within 24-48h. |

## Common Triggers & Thresholds

### 1. dbt Freshness Alerts
Fires if `source_at` is older than the threshold defined in `dbt_project.yml`.
- **Critical**: `fact_workflow_runs` > 4h (Updated after `postmortem__workflow-runs-stale-2025-09-12.md`).
- **Standard**: Most facts > 8h.
- **Action**: Check Airflow DAG logs for `upstream_task_failed` or BigQuery slot exhaustion.

### 2. BigQuery Slot Exhaustion
- **Trigger**: `reservation.used_slots` > 500 for more than 10 minutes.
- **Impact**: All dbt models and Looker tiles hang.
- **Recent Example**: See `slack__engineering__workflow-duration-spike.md` for when a recursive workflow loop at `cust_000214` flooded the logs.

### 3. Looker Errors
- **Trigger**: "Error 500: Internal Server Error" on the Executive Daily dashboard.
- **Action**: Verify `marts/finance/arr_snapshot` materialized correctly. If `qc_recency_disagreements > 5`, the model will fail the build (see `dbt__model__arr_snapshot.md`).

### 4. Pinecone/Vector Latency (AI Assistant)
- **Trigger**: p99 latency for AI Workflow Assistant steps > 2s.
- **Action**: Notify @dan.lee. This usually indicates a bottleneck in the embedding pipeline for new templates.

## Incident Workflow

### Phase 1: Identification & Triage
1. **Declare**: If SEV1/SEV2, post in `#incident` with: `INCIDENT DECLARE: [Summary] (SEV X)`.
2. **Commander**: The on-call engineer (see `notion__on-call-rotation.md`) is the Incident Commander (IC).
3. **Zoom**: Start a bridge if SEV1.

### Phase 2: Comms
- **Internal**: Update `#incident` and `#data-help`.
- **Stakeholders**: If ARR/NRR is affected, @david.kim must DM @lina.cho (FP&A) and @rachel.stein (CFO).
- **Template**:
  > *Update [Time UTC]: Investigating [Issue]. Impacted tables: [X, Y]. Estimated resolution: [Time].*

### Phase 3: Resolution
- **Rollback**: If a dbt merge caused the issue, revert the PR in GitHub and trigger the `prod_deploy` Airflow task.
- **Kill Switches**: For BigQuery exhaustion, identify the `customer_id` causing the spike and temporarily pause their CDC stream in Fivetran.

### Phase 4: Postmortem
Every SEV1 and SEV2 requires a postmortem within 3 business days.
- **Template**: Use the structure found in `notion__churn-debrief-template.md` (adapted for technical root cause).
- **Storage**: Save to `postmortem__<date>_<description>.md`.

## Historical Context (Reference)

- **Stripe Pipeline Incident (2025-09)**: Root cause was a schema change in Stripe API that broke the `fact_invoices` sync. Led to the addition of the `invoice_id` FK in `fact_subscriptions`. See `slack__incident__workflow-runs-stale-2025-09-12.md`.
- **The "Off-by-3" Bug (2026-02)**: A timezone edge case in `arr_snapshot`. Resulted in the multi-CTE paranoid check now present in `dbt__model__arr_snapshot.md`.

## On-Call Handover
Handover happens every Monday at 09:00 UTC. The outgoing engineer must:
1. Review all SEV3s opened during the week.
2. Ensure all `dbt-test` failures are silenced or fixed.
3. Update the "Known Warts" section in `notion__data-warehouse-conventions.md`.

---

> **Comment from david.kim (2026-02-20)**: Updated SEV1 thresholds to include Pinecone latency for the AI Assistant beta. If the vector store lags, the "AI Workflow Assistant" (see `notion__pricing-tiers.md`) becomes unusable.
