---
title: "Notion runbook — Data warehouse conventions (with footnotes + history)"
source_url: "internal://acme/notion/data-warehouse-conventions"
license: "synthetic-demo"
attribution: "Acme Inc Notion runbook (synthetic demo). Owner: David Kim (Sr DE)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: notion_runbook
---

# Data warehouse conventions

> **Last reviewed**: 2026-01-08 by david.kim
> **Owner**: David Kim (Sr Data Engineer)
> **Audience**: anyone querying `nexus-analyst-demo.acme.*`
>
> 🚧 `// TODO: this doc is the most-read internal data doc. it's also the most likely to drift. should auto-link from the dbt project README -david 2026-04-15`

These conventions exist so that anyone — analyst, engineer, AE, CSM — can write a query against the Acme warehouse and get correct, consistent answers without re-deriving definitions every time.

## Naming

- **Table prefixes**: `dim_` for dimensions, `fact_` for fact tables. No other prefixes.
- **Surrogate keys**: STRING with a 3-letter prefix. E.g. `cust_*`, `user_*`, `emp_*`, `sub_*`, `inv_*`, `wfr_*`, `evt_*`, `tkt_*`, `opp_*`, `nps_*`, `tch_*`, `wf_*`.
- **Snake_case** for all column names.
- **Boolean columns** start with `is_*`.
- **Timestamps** are TIMESTAMP (always UTC). **Dates** are DATE.
- **Money** is NUMERIC USD (Acme bills only in USD; FX is not modeled).

> **Footnote**: the `wf_*` prefix for workflow_id is inconsistent — some legacy rows use a different format (`workflow-{uuid}`). We aliased the column to use `wf_*` in the staging layer. If you query the raw layer (`raw.workflows`), expect both formats.

## Source of truth

When two tables disagree, the **fact** is canonical. Examples:

| Question | Use this | Don't use this |
|---|---|---|
| Is this customer paid right now? | `fact_subscriptions WHERE is_current AND plan_tier != 'Free'` | `dim_customers.current_plan_tier` |
| What is current MRR? | `SUM(fact_subscriptions.mrr_usd) WHERE is_current AND plan_tier != 'Free'` | `SUM(dim_customers.current_mrr_usd)` |
| Is this user active? | distinct `user_id` in `fact_user_events WHERE event_name = 'login' AND event_at >= 28d ago` | `dim_users.is_active` |

The dim convenience fields exist for filter ergonomics, not for measurement.

> **Inline rant from david.kim (2026-02-08)**: I have wanted to KILL these denormalized convenience fields for ~14 months. They cause a `#data-help` thread approximately every other week. Marketing analytics depends on them so we keep them around. One day. One day.

## Slowly-changing dimensions

Acme does NOT use SCD Type 2 in the warehouse. Historical state is captured in fact tables:

- Plan changes → `fact_subscriptions` (event style, with `change_type`)
- User activity → `fact_user_events`
- Customer status changes → derived from `fact_subscriptions` change events (no separate change-log table)

If you need to know "what was customer X's plan tier on 2025-09-15?", join to `fact_subscriptions` filtered to `start_date <= '2025-09-15' AND (end_date IS NULL OR end_date > '2025-09-15')`.

## Time zones

Everything is **UTC**. There is one exception: `dim_dates` has no timezone (it's a calendar, not a moment). When converting `fact_*.event_at` (TIMESTAMP UTC) to a date for grouping, use `DATE(event_at)` which truncates in UTC by default.

If a stakeholder asks for "PT-day" grouping (e.g., for sales-team day-cohort analysis), explicitly use `DATE(event_at, 'America/Los_Angeles')`.

> **Wart**: NPS responses are stored with `responded_at` as TIMESTAMP but the `survey_quarter` column is just the quarter label. If you grouping NPS by exact response time, use `responded_at`. If grouping by survey period, use `survey_quarter` (more reliable, accounts for survey-period boundaries).

## Refresh cadence

| Table | Cadence | Source |
|---|---|---|
| `dim_customers` | nightly @ 06:00 UTC | Salesforce + product DB |
| `dim_users` | nightly @ 06:30 UTC | product DB |
| `dim_employees` | weekly Mondays | HRIS |
| `dim_plans` | manual (on price changes) | Pricing committee |
| `dim_dates` | static | one-time generated |
| `fact_subscriptions` | hourly | Stripe + product DB CDC |
| `fact_invoices` | hourly | Stripe webhook |
| `fact_workflow_runs` | every 15 minutes | product DB CDC |
| `fact_user_events` | every 15 minutes | Segment |
| `fact_support_tickets` | hourly | Zendesk + Intercom |
| `fact_opportunities` | hourly | Salesforce |
| `fact_nps_responses` | daily | Delighted |
| `fact_marketing_touches` | every 30 minutes | HubSpot + ad-platform exports |

dbt freshness alerts fire if any table is more than 8h stale (4h for `fact_workflow_runs` since the Sept 2025 incident).

## Common joins

Memorize these:

```sql
-- Customers with their plan
SELECT c.*, p.*
FROM dim_customers c
LEFT JOIN dim_plans p ON c.current_plan_tier = p.plan_tier
-- p uses plan_tier as PK, c uses current_plan_tier — names differ but values match

-- Subscription history with plan reference
SELECT s.*, p.*
FROM fact_subscriptions s
LEFT JOIN dim_plans p ON s.plan_tier = p.plan_tier

-- Workflow runs with customer detail
SELECT r.*, c.company_name, c.current_plan_tier, c.account_tier
FROM fact_workflow_runs r
JOIN dim_customers c USING (customer_id)
```

> **Gotcha**: Don't try to `USING (plan_tier)` between `dim_customers` and `dim_plans` — the column names are `current_plan_tier` vs `plan_tier`. Has to be explicit ON clause.

## What's NOT in this warehouse

- Step-level workflow execution detail (we don't expose individual step traces in BI)
- Connection metadata (which integrations a customer has authed) — that's in the product DB only
- Marketing spend (was added 2026-04-09; see `slack__marketing__attribution-model-question.md`)
- HRIS payroll detail (only `dim_employees` cares about names + roles + hire dates)
- Customer feature usage telemetry beyond the events listed in `fact_user_events`

For anything not in this warehouse, ask in `#data-help`.

## Recently added / changed

| When | What |
|---|---|
| 2026-04-09 | Added `spend_usd` derivation in `fact_marketing_touches` (was previously NULL because we hadn't loaded it). Backfilled 12 months. |
| 2026-03-22 | `fact_support_tickets.csat_score` semantics: 1-5 scale, was previously 1-10 in the source — collapsed to 5 at staging. |
| 2026-02-04 | (incident-related) Added `invoice_id` foreign key to `fact_subscriptions` for traceability after the Stripe pipeline incident. |
| 2025-12-04 | Reduced `fact_workflow_runs` freshness threshold from 8h to 4h. |
| 2025-11-15 | Added `fact_nps_responses.segment` precomputed column. Was being computed in 30+ downstream queries with slight inconsistencies. |

## Stuff people argue about

- **Should `dim_customers.account_tier` be derived or stored?** Currently stored (set at signup, manually updated by AE). Some folks want it derived from `current_plan_tier + employee_count_band`. Decision: stored is fine. Source-of-truth is the AE's CRM judgment.
- **Should we have a `fact_renewals` table?** Currently no — renewal events are inferred from `fact_subscriptions` change_type='renewal' rows. Some on the team want a dedicated renewal fact. Probably will happen in 2026-H2.

## Comment thread

> **2026-04-15** — `david.kim`: Added auto-link TODO. Updated recent changes table.
> **2026-04-09** — `lina.cho`: Added marketing spend note.
> **2026-02-08** — `david.kim`: Added rant about denormalized convenience fields.
> **2026-01-08** — `david.kim`: Quarterly review.
> **2025-09-22** — `priya.anand`: Added freshness threshold note (post-incident).
