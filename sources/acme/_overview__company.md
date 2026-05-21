---
title: "Acme Inc — company overview (synthetic demo)"
source_url: "internal://acme/company-overview"
license: "synthetic-demo"
attribution: "Generated for Nexus Analyst Acme Enterprise BI demo. Acme Inc is a fictitious company; any resemblance to real entities is coincidental."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: notion_runbook
---

# Acme Inc — company overview

> **This is synthetic demo content.** Acme Inc does not exist. The data, employees, customers, conversations, and incidents in this corpus are all generated for the Nexus Analyst Enterprise BI demo. Treat it as a stable internal-knowledge fixture for analyst-style questions over the synthetic `nexus-analyst-demo.acme` BigQuery dataset.

## What Acme does

Acme Inc is a workflow automation platform for mid-market and enterprise software teams. Customers build "workflows" that connect SaaS tools (Salesforce, Slack, GSheets, Notion, GitHub, Stripe, Snowflake, …) and run them on a schedule, by webhook, or on demand. Think Zapier / Make / Tray, but priced for teams >50 seats.

## Snapshot (as of 2026-05-04)

- **Founded**: January 2023
- **HQ**: San Francisco. Second office: Amsterdam (EMEA).
- **Employees**: ~100 across Engineering (~30), Sales (~20), Customer Success (~15), Marketing (~10), Product/Design (~15), Finance/Ops/People/Legal (~10).
- **Customers**: 800 total in `dim_customers` (~745 active, ~45 churned, ~10 paused). ~24,000 users provisioned, ~16,000 active in the last 28 days.
- **ARR**: ~$39M (Business ~$32M / Enterprise ~$6M / Pro ~$1M). Free tier ARR is $0. Headline plan mix among active paying customers: Pro ~38%, Business ~27%, Enterprise ~5%, Free (non-paying) ~30%.
- **Funding**: Series B, $80M raised total. Last round Q3 2025.

## Plan tiers

| Tier | Price | Min seats | Notes |
|---|---|---|---|
| Free | $0 | 1 | 100 workflow runs / month, 2 active workflows |
| Pro | $49 / seat / month | 1 | 10K runs / month, unlimited workflows |
| Business | $149 / seat / month | 50 | 100K runs / month, SSO, audit log, priority support |
| Enterprise | Custom (typically $50K-$500K ACV) | 250 | Unlimited runs, dedicated CSM, SOC2, custom SLA, private deployments |

PLG funnel: Free → Pro is self-serve. Pro → Business and Business → Enterprise are AE-led.

## Sales motion

- **SMB** (Free, Pro): self-serve / SDR-qualified.
- **Mid-Market** (Business): AE-owned with SDR sourcing.
- **Enterprise**: AE-owned, multi-stakeholder, average sales cycle ~90 days.

Sales segmentation in `dim_customers.account_tier`: `SMB` / `MM` / `Ent`.

## Key product entities

- **Workflow** — a directed graph of steps a customer builds. Identified by `workflow_id`.
- **Workflow run** — one execution of a workflow. `fact_workflow_runs`.
- **Connection** — an authenticated link to an external integration (e.g. one Slack workspace, one Salesforce org).
- **Step** — a single node in the workflow (trigger, action, branch, loop). We do not currently expose step-level facts in the BI warehouse.

## How we measure things (canonical definitions — see `glossary__*` for SQL)

- **ARR** = `SUM(mrr_usd) * 12` over `fact_subscriptions` rows where `is_current = TRUE` and `plan_tier != 'Free'`.
- **Paid customer** = a `customer_id` with at least one `is_current = TRUE` subscription on a non-Free tier.
- **Active user** = `dim_users.is_active = TRUE` AND a `user_event` in the last 28 days.
- **Engaged customer** = customer with ≥3 active users AND ≥10 successful workflow runs in the trailing 28 days.
- **Net Revenue Retention (NRR)** = computed monthly cohort-style; see `glossary__nrr.md` for the SQL.
- **Logo churn** = customer transitioned `status` from `active` → `churned` in the period (look for `change_type = 'churn'` in `fact_subscriptions`).

## Data warehouse — `nexus-analyst-demo.acme`

13 tables, all in BigQuery dataset `nexus-analyst-demo.acme`. See `schema__overview.md` for the full table + column listing.

- **Dimensions (5)**: `dim_customers`, `dim_users`, `dim_employees`, `dim_plans`, `dim_dates`.
- **Facts (8)**: `fact_subscriptions`, `fact_invoices`, `fact_workflow_runs`, `fact_user_events`, `fact_support_tickets`, `fact_opportunities`, `fact_nps_responses`, `fact_marketing_touches`.

Time range: customer signups + activity span 2023-01-01 through 2026-04-30. Refreshed daily by a fictional dbt project; the BI warehouse lags production by ~2 hours.

## Org chart (high level)

- **CEO**: emp_001 — Sam Reyes
- **VP Eng**: emp_010 — Priya Anand
- **VP Sales**: emp_020 — Marcus Webb
- **VP Customer Success**: emp_040 — Elena Volkov
- **VP Product**: emp_050 — Dan Lee
- **CFO**: emp_060 — Rachel Stein
- **VP Marketing**: emp_070 — Jasmine Park

See `dim_employees` for the rest. `manager_employee_id` chains up to one of the VPs above (or directly to the CEO).
