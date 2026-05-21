---
title: "Acme BigQuery warehouse — schema overview"
source_url: "internal://acme/schema-overview"
license: "synthetic-demo"
attribution: "Generated for Nexus Analyst Acme Enterprise BI demo."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: bq_schema
---

# `nexus-analyst-demo.acme` — schema overview

All Acme analytics lives in one BigQuery dataset: **`nexus-analyst-demo.acme`**. 5 dimensions + 8 facts. Snake_case. No partitioning needed at this scale (largest fact is ~100K rows).

## Conventions

- Surrogate keys are STRING with a 3-letter prefix: `cust_*`, `user_*`, `emp_*`, `sub_*`, `inv_*`, `wfr_*`, `evt_*`, `tkt_*`, `opp_*`, `nps_*`, `tch_*`, `wf_*`.
- Timestamps are UTC TIMESTAMP. Dates are DATE. Money is NUMERIC USD (no FX in this warehouse — Acme bills in USD only).
- Boolean columns use `is_*` naming.
- Slowly-changing dim attributes are point-in-time current; historical snapshots live in `fact_subscriptions` (for plan changes) and `fact_user_events` (for behavior).

## Dimensions

### `dim_customers` (~800 rows)

| Column | Type | Notes |
|---|---|---|
| `customer_id` | STRING | PK. `cust_xxxxxx`. |
| `company_name` | STRING | Synthetic. |
| `signup_date` | DATE | First touch (free or paid). |
| `country` | STRING | ISO-2. Mostly `US`, then `GB`, `DE`, `FR`, `NL`, `CA`, `AU`, `IE`, `SE`, `ES`. |
| `region` | STRING | `NA` / `EMEA` / `APAC`. |
| `industry` | STRING | `SaaS` / `E-commerce` / `Finance` / `Healthcare` / `Education` / `Media` / `Other`. |
| `employee_count_band` | STRING | `1-10` / `11-50` / `51-200` / `201-1000` / `1001-5000` / `5000+`. |
| `account_tier` | STRING | `SMB` / `MM` / `Ent`. Sales segmentation. |
| `current_plan_tier` | STRING | `Free` / `Pro` / `Business` / `Enterprise`. Point-in-time. |
| `current_mrr_usd` | NUMERIC | 0 for Free. |
| `status` | STRING | `active` / `churned` / `paused`. |
| `churn_date` | DATE | NULL unless churned. |
| `csm_employee_id` | STRING | NULL for SMB / Free. FK → `dim_employees`. |
| `ae_employee_id` | STRING | NULL for self-serve. FK → `dim_employees`. |
| `acquisition_channel` | STRING | `organic` / `paid_search` / `content` / `referral` / `outbound` / `partner`. |
| `primary_use_case` | STRING | Free-text from onboarding. |

### `dim_users` (~12,000 rows)

| Column | Type | Notes |
|---|---|---|
| `user_id` | STRING | PK. |
| `customer_id` | STRING | FK → `dim_customers`. |
| `email_domain` | STRING | Used for join hygiene. |
| `role` | STRING | `admin` / `builder` / `viewer`. |
| `signup_date` | DATE | |
| `last_login_date` | DATE | NULL if never logged in. |
| `is_active` | BOOL | `TRUE` if logged in within last 28 days. |
| `invited_by_user_id` | STRING | NULL for first-user. |

### `dim_employees` (~100 rows)

| Column | Type | Notes |
|---|---|---|
| `employee_id` | STRING | PK. `emp_xxx`. |
| `full_name` | STRING | |
| `team` | STRING | `Engineering` / `Sales` / `CS` / `Marketing` / `Product` / `Design` / `People` / `Finance` / `Legal`. |
| `role` | STRING | e.g. `Senior AE`, `CSM`, `Staff Engineer`. |
| `manager_employee_id` | STRING | Self-referential FK. NULL for CEO. |
| `hire_date` | DATE | |
| `termination_date` | DATE | NULL if active. |
| `location` | STRING | `SF` / `Amsterdam` / `Remote-NA` / `Remote-EU`. |
| `is_active` | BOOL | |

### `dim_plans` (4 rows)

| Column | Type | Notes |
|---|---|---|
| `plan_tier` | STRING | PK. |
| `monthly_price_per_seat_usd` | NUMERIC | 0 / 49 / 149 / NULL (Enterprise = custom). |
| `min_seats` | INT64 | 1 / 1 / 50 / 250. |
| `workflow_run_quota_per_month` | INT64 | 100 / 10000 / 100000 / NULL (unlimited). |
| `storage_gb` | INT64 | |
| `sla_uptime_pct` | FLOAT64 | NULL for Free. |

### `dim_dates`

Standard date spine 2022-01-01 through 2026-12-31. Cols: `date`, `year`, `quarter`, `month`, `month_name`, `week`, `day_of_week`, `is_weekend`, `is_business_day`.

## Facts

### `fact_subscriptions` (~2,000 rows)

One row per subscription event (new, upgrade, downgrade, renewal, churn). Use `is_current = TRUE` for point-in-time MRR.

| Column | Type | Notes |
|---|---|---|
| `subscription_id` | STRING | PK. |
| `customer_id` | STRING | FK. |
| `plan_tier` | STRING | |
| `start_date` | DATE | |
| `end_date` | DATE | NULL if open. |
| `mrr_usd` | NUMERIC | |
| `seat_count` | INT64 | |
| `billing_cycle` | STRING | `monthly` / `annual`. |
| `is_current` | BOOL | TRUE for active subscription as of warehouse refresh. |
| `change_type` | STRING | `new` / `upgrade` / `downgrade` / `seat_change` / `renewal` / `churn`. |
| `changed_from_subscription_id` | STRING | Self-referential FK. |

### `fact_invoices` (~10,000 rows)

| Column | Type | Notes |
|---|---|---|
| `invoice_id` | STRING | PK. |
| `customer_id` | STRING | FK. |
| `subscription_id` | STRING | FK. |
| `invoice_date` | DATE | |
| `period_start` | DATE | |
| `period_end` | DATE | |
| `amount_usd` | NUMERIC | |
| `status` | STRING | `paid` / `open` / `void` / `uncollectible`. |
| `paid_at` | TIMESTAMP | NULL if not paid. |

### `fact_workflow_runs` (~100,000 rows)

| Column | Type | Notes |
|---|---|---|
| `run_id` | STRING | PK. |
| `workflow_id` | STRING | |
| `customer_id` | STRING | FK. |
| `triggered_at` | TIMESTAMP | |
| `triggered_by` | STRING | `schedule` / `webhook` / `manual` / `api`. |
| `status` | STRING | `success` / `error` / `timeout` / `partial`. |
| `duration_ms` | INT64 | |
| `step_count` | INT64 | |
| `error_code` | STRING | NULL on success. e.g. `AUTH_FAILED`, `RATE_LIMITED`, `STEP_TIMEOUT`, `INTEGRATION_DOWN`, `USER_ERROR`. |

### `fact_user_events` (~100,000 rows)

| Column | Type | Notes |
|---|---|---|
| `event_id` | STRING | PK. |
| `user_id` | STRING | FK. |
| `customer_id` | STRING | FK (denormalized). |
| `event_at` | TIMESTAMP | |
| `event_name` | STRING | See list below. |
| `properties_json` | STRING | Stringified JSON. |

Event-name vocabulary: `login`, `workflow_created`, `workflow_run_succeeded`, `workflow_run_failed`, `integration_connected`, `integration_disconnected`, `template_imported`, `invite_sent`, `billing_viewed`, `upgrade_clicked`, `support_ticket_opened`.

### `fact_support_tickets` (~3,000 rows)

| Column | Type | Notes |
|---|---|---|
| `ticket_id` | STRING | PK. |
| `customer_id` | STRING | FK. |
| `user_id` | STRING | FK. |
| `opened_at` | TIMESTAMP | |
| `closed_at` | TIMESTAMP | NULL if open. |
| `channel` | STRING | `email` / `intercom` / `portal` / `csm`. |
| `priority` | STRING | `P1` / `P2` / `P3` / `P4`. |
| `category` | STRING | `auth` / `billing` / `integration` / `workflow` / `data` / `onboarding` / `feature_request` / `bug`. |
| `resolution_time_hours` | FLOAT64 | NULL if open. |
| `csat_score` | INT64 | 1-5. NULL if not surveyed. |
| `assigned_to_employee_id` | STRING | FK → `dim_employees`. |

### `fact_opportunities` (~500 rows)

| Column | Type | Notes |
|---|---|---|
| `opportunity_id` | STRING | PK. |
| `customer_id` | STRING | NULL until Closed_Won. |
| `account_name` | STRING | |
| `ae_employee_id` | STRING | FK. |
| `sdr_employee_id` | STRING | NULL for inbound. |
| `created_date` | DATE | |
| `stage` | STRING | `Prospecting` / `Qualified` / `Proposal` / `Negotiation` / `Closed_Won` / `Closed_Lost`. |
| `amount_usd` | NUMERIC | |
| `close_date` | DATE | Forecast date until closed. |
| `closed_won_at` | DATE | NULL until won. |
| `loss_reason` | STRING | NULL unless lost. e.g. `competitor`, `price`, `no_decision`, `feature_gap`, `timing`. |

### `fact_nps_responses` (~2,000 rows)

| Column | Type | Notes |
|---|---|---|
| `response_id` | STRING | PK. |
| `customer_id` | STRING | FK. |
| `user_id` | STRING | FK. |
| `responded_at` | TIMESTAMP | |
| `score` | INT64 | 0-10. |
| `comment` | STRING | NULL if no free text. |
| `segment` | STRING | `promoter` (9-10) / `passive` (7-8) / `detractor` (0-6). |
| `survey_quarter` | STRING | e.g. `2025-Q4`. |

### `fact_marketing_touches` (~5,000 rows)

| Column | Type | Notes |
|---|---|---|
| `touch_id` | STRING | PK. |
| `lead_email_hash` | STRING | SHA256 of email — anonymized. |
| `customer_id` | STRING | NULL until lead converts. |
| `touched_at` | TIMESTAMP | |
| `channel` | STRING | `paid_search` / `social` / `content` / `email` / `webinar` / `conference` / `partner`. |
| `campaign` | STRING | |
| `utm_source` | STRING | |
| `utm_medium` | STRING | |
| `utm_campaign` | STRING | |
| `attributed_revenue_usd` | NUMERIC | First-touch attribution. NULL if lead never converted. |
