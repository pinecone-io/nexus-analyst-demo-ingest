---
title: "Confluence/Notion data team page archive — 2025 (stale)"
source_url: "internal://acme/confluence-data-team-archive-2025"
license: "synthetic-demo"
attribution: "Synthetic content, Acme Inc internal demo. Acme Inc is a fictitious company."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: notion_runbook
---

# 🗄️ ARCHIVE: Data Team Knowledge Base (Migrated from Confluence)

**Status:** STALE / ARCHIVED  
**Last Major Update:** October 14, 2025  
**Note:** This space was migrated to the new "Data & Analytics Hub" in Notion in late 2025. Many definitions here are **outdated** and do not reflect the Q4 2025 recalibration or the 2026 dbt refactor. Use with extreme caution.

---

## 📑 Table of Contents
1. [Team Roster & Responsibilities (2025 Q1)](#team-roster)
2. [BigQuery Migration Plan (In Progress)](#bq-migration)
3. [Core Metric: Engagement Definition (v1.2)](#engagement-v1)
4. [Financial Reporting: ARR Calculation Logic](#arr-logic)
5. [dbt Model Inventory & Naming Conventions](#dbt-inventory)
6. [Data Dictionary: dim_customers](#dict-customers)
7. [Looker Development & Caching Guidelines](#looker-rules)
8. [Churn Analysis Methodology (Historical)](#churn-method)
9. [Value Realization Score (VRS) Specification (Draft)](#vrs-spec)
10. [Event Tracking: fact_user_events properties](#event-props)
11. [NRR Computation Guidelines](#nrr-logic)
12. [Operational SQL Snippet Library](#sql-snippets)
13. [Pipeline Onboarding: Singer & Fivetran Connectors](#pipelines)
14. [Q3 2025 Roadmap](#roadmap-q3)
15. [Legacy Postgres Schema Map (Deprecated)](#postgres-map)

---

<a name="team-roster"></a>
## 1. Team Roster & Responsibilities (2025 Q1)
*This roster is outdated. Some members have moved to Product Eng or left the company.*

| Name | Role | Employee ID | Focus Area |
|---|---|---|---|
| Rajiv Menon | Junior Analytics Engineer | emp_012 | dbt core, Marketing attribution |
| David Kim | Data Engineer | emp_013 | Pipeline stability, BigQuery infra |
| Nina Patel | Analytics Engineer | emp_014 | Finance & Sales reporting |
| Sarah Jenkins | Data Analyst (Left) | emp_019 | Product Analytics |
| Jorge Martinez | RevOps Liaison | emp_063 | Salesforce sync, Lead scoring |

**Management:** Priya Anand (VP Eng) overseeing Data until a Head of Data is hired.

---

<a name="bq-migration"></a>
## 2. BigQuery Migration Plan (In Progress)
**Status: Yellow** (Delayed by Salesforce API limits)

We are moving away from the internal Postgres replica to BigQuery.  
**Target Project:** `nexus-analyst-demo`  
**Planned Dataset Structure:**
* `acme.marts.finance` (Invoices, ARR)
* `acme.marts.cs` (Health, Support)
* `acme.marts.product` (Workflows, Events)

**Correction Note (Nov 2025):** The VP of Eng requested a FLAT schema. We are moving everything to `nexus-analyst-demo.acme.<table>`. Disregard the nested `marts.*` folders in the warehouse; those will only exist in the dbt filesystem.

---

<a name="engagement-v1"></a>
## 3. Core Metric: Engagement Definition (v1.2)
**⚠️ THIS PAGE IS OUTDATED — SEE NOTION FOR Q4 RECALIBRATION ⚠️**

Engagement is our leading indicator for churn.  
**Definition:** A customer is "Engaged" if at least one user from their domain has logged into the platform in the last 28 days.

**SQL Logic:**
```sql
-- OLD LOGIC - DO NOT USE FOR BOARD REPORTING
SELECT 
    customer_id,
    CASE WHEN MAX(last_login_date) >= DATE_SUB(CURRENT_DATE(), INTERVAL 28 DAY) 
    THEN 1 ELSE 0 END as is_engaged
FROM nexus-analyst-demo.acme.dim_users
GROUP BY 1
```
*Notes from Data Meeting 2025-06-12:* Rachel (CFO) thinks this is too generous. We see "Engaged" customers churning because only one person was poking around. We need to tighten this to multi-user activity and actual workflow execution.

---

<a name="arr-logic"></a>
## 4. Financial Reporting: ARR Calculation Logic
**Status: Stale**

To calculate Annual Recurring Revenue (ARR), use the `current_mrr_usd` field in the customer dimension.

**Formula:** `dim_customers.current_mrr_usd * 12`

**Query Example:**
```sql
SELECT 
    SUM(current_mrr_usd) * 12 as total_arr
FROM nexus-analyst-demo.acme.dim_customers
WHERE status = 'active'
```
*Current Tally (Aug 2025):* ~$42M according to the Looker dashboard.

**⚠️ WARNING:** This calculation is known to drift. It does not account for mid-month plan changes or seat-based expansion until the daily dbt sync. For board-level accuracy, we need a snapshot table that captures MRR on the last day of the month. Lina Cho is working on `arr_snapshot`.

---

<a name="dbt-inventory"></a>
## 5. dbt Model Inventory & Naming Conventions

All models should follow the `fct_` and `dim_` prefixes.

*   `dim_customers`: Master list of accounts.
*   `dim_users`: Individual users.
*   `fct_mrr`: Monthly revenue per customer (Legacy - being replaced by `fact_subscriptions`).
*   `fct_workflow_runs`: Raw run logs.
*   `account_health_v1`: Initial pass at health scoring.

*Rename log:* 
- `fct_invoices` moved to `fact_invoices`.
- `fct_support` moved to `fact_support_tickets`.

---

<a name="dict-customers"></a>
## 6. Data Dictionary: dim_customers

| Column | Description | Type |
|---|---|---|
| customer_id | Unique identifier (cust_XXXXX) | STRING |
| company_name | Legal name of company | STRING |
| account_tier | Sales tier (SMB, Mid-Market, Enterprise) | STRING |
| current_plan_tier | Current billing plan (Free, Pro, Business, Enterprise) | STRING |
| seat_count_licensed | Total seats paid for in the contract | INTEGER |
| csm_employee_id | ID of the Customer Success Manager | STRING |
| is_engaged_legacy | Flag based on 28-day login (stale) | BOOLEAN |

---

<a name="looker-rules"></a>
## 7. Looker Development & Caching Guidelines
We have been seeing significant performance lag on the "Executive Overview" dashboard.

**Temporary Fix:** 
We have set `persist_for: "24 hours"` on most explores. This is why some numbers (like ARR) might look different from the raw SQL queries in BigQuery for a few hours.

**Known Issue:** The "ARR $42M" ghosting. If a customer churns, the PDT might not refresh immediately, leading to an overstatement of revenue. If you need real-time ARR, query `fact_subscriptions` directly and filter for `is_current = true`.

---

<a name="churn-method"></a>
## 8. Churn Analysis Methodology (Historical)
*Author: Sarah Jenkins (Archived)*

When calculating churn, we compare the current customer list to the list from 30 days ago.

**SQL Pattern:**
```sql
SELECT 
    count(distinct a.customer_id) as lost_customers
FROM legacy_db.customers a
INNER JOIN legacy_db.customers b ON a.customer_id = b.customer_id
WHERE a.status = 'churned' AND b.status = 'active'
```
*Note from Rajiv (2025-09):* Sarah's old logic using INNER JOINs on the churned table is dangerous. If a customer record is deleted or modified in the source system, they drop out of the join entirely. We should be using a LEFT JOIN from the historical snapshot and checking for NULLs or status changes to `churned`.

---

<a name="vrs-spec"></a>
## 9. Value Realization Score (VRS) Specification (Draft)
**Status: PARKED (Do Not Implement)**
*Owner: Dan Lee (VP Product)*

The VRS is intended to measure how much "value" a customer gets beyond just running workflows.

**Proposed Components:**
1. `vrs_band`: (Gold/Silver/Bronze) based on automation complexity.
2. `champion_login_recency`: How often the primary admin logs in.
3. `integration_diversity`: Number of unique SaaS tools connected.

**Engineering Note:** David Kim confirmed we do not have `vrs_band` or `champion_login_recency` in the warehouse yet. These columns are NOT built. Use `account_health` instead.

---

<a name="event-props"></a>
## 10. Event Tracking: fact_user_events properties
This table contains all front-end and API events.

**Common Event Names:**
- `workflow_created`
- `workflow_published`
- `connection_authorized`
- `dashboard_viewed`

**JSON Properties:**
- `browser`: User's browser string.
- `step_count`: For `workflow_created` events.
- `integration_id`: For `connection_authorized`.

---

<a name="nrr-logic"></a>
## 11. NRR Computation Guidelines
*Owner: Nina Patel*

Net Retention Rate (NRR) is our most important metric for Series B investors.

**The "Strict" Cohort Rule:**
To calculate trailing 12-month NRR:
1. Identify all customers who were on a **Paid Plan** (Pro, Business, or Enterprise) exactly 12 months ago.
2. Sum their MRR as of that date (Denominator).
3. Sum the MRR of those *same* customers today (Numerator).

**Crucial Logic:** You MUST include customers who have since churned. Their current MRR is $0. If you do an INNER JOIN, you will only see the ones who stayed, which will artificially inflate NRR to 120%+.

**Current Target:** 107% (As of Q3 2025).

---

<a name="sql-snippets"></a>
## 12. Operational SQL Snippet Library

### Check Active Seats vs Licensed Seats
```sql
SELECT 
    c.company_name,
    c.seat_count_licensed,
    COUNT(u.user_id) as active_users
FROM nexus-analyst-demo.acme.dim_customers c
JOIN nexus-analyst-demo.acme.dim_users u ON c.customer_id = u.customer_id
WHERE u.is_active = true
GROUP BY 1, 2
HAVING COUNT(u.user_id) > c.seat_count_licensed
```

### Monthly Workflow Run Success Rate
```sql
SELECT 
    FORMAT_DATE('%Y-%m', run_date) as month,
    SUM(n_success) / SUM(n_runs) as success_rate
FROM nexus-analyst-demo.acme.workflow_runs_daily
GROUP BY 1
```

---

<a name="pipelines"></a>
## 13. Pipeline Onboarding: Singer & Fivetran Connectors
We use Fivetran for Salesforce and Zendesk, and custom Singer taps for the production Postgres DB.

**Sync Frequency:**
- Salesforce: 1 hour
- Zendesk: 6 hours
- Product DB: 2 hours (BI warehouse lag)

*Note:* If you see a ticket in Zendesk but not in `fact_support_tickets`, check the sync status in the Fivetran dashboard. David Kim is the admin.

---

<a name="roadmap-q3"></a>
## 14. Q3 2025 Roadmap (Old)
- [x] Migrate all Salesforce objects to BigQuery
- [ ] Implement "Value Realization Score" (VRS) -> *Deferred to 2026*
- [x] Fix the Looker MRR drift issue (Snapshotting)
- [ ] Build "Step-Level" fact table for granular workflow analysis -> *Canceled due to data volume/cost*

---

<a name="postgres-map"></a>
## 15. Legacy Postgres Schema Map (Deprecated)
*This is for reference ONLY when debugging data from before Jan 2025.*

**Table: `public.orgs`** -> Now `dim_customers`  
**Table: `public.memberships`** -> Now `dim_users`  
**Table: `public.billing_info`** -> Now `fact_subscriptions`  

---

## 💬 Slack Log Snippet (Context for Metric Changes)

**rajiv.menon [2025-10-02 10:15 AM]:** Hey @nina, I'm looking at the engagement numbers for Cobalt Systems (cust_000700). It says they are "Engaged" but Marco says they haven't actually run a workflow in 3 weeks.  
**nina.patel [2025-10-02 10:18 AM]:** Yeah, the current `is_engaged` flag in `dim_customers` just looks for logins. One admin logging in to check settings counts as engagement.  
**rajiv.menon [2025-10-02 10:20 AM]:** That's useless for CS. We should change it.  
**nina.patel [2025-10-02 10:21 AM]:** Priya and Dan are talking about a "recalibration" for Q4. The new rule will probably be at least 3 active users AND at least 10 successful workflow runs. Don't update the dbt model yet though, let's wait for the official sign-off.

---

## 🚩 Known Data Quality Issues (Historical)

1.  **Duplicate User IDs:** Some users who signed up, deleted their account, and signed up again have two `user_id` entries but the same email. `dim_users` attempts to de-dupe on email, but it's not perfect.
2.  **Enterprise Seat Counts:** For Enterprise customers (e.g., Marigold Health, cust_000701), `seat_count_licensed` is often set to a placeholder like `9999` in the legacy system. We need to manually override these with the ACV-based seat counts from the contract.
3.  **Region Mismatches:** Some LATAM customers (like Willow Works, cust_000709) are showing up in the "North America" rollup because their HQ is in Delaware.

---

## 🛠️ Data Team "Secret Sauce" (Old Hacks)

*   **Manual ARR Adjustment:** If the board report looks weird, check the `manual_revenue_adjustments` Google Sheet. Lina Cho sometimes adds one-time credits there that aren't in Salesforce yet.
*   **The "Double Sync" Trick:** If Fivetran hangs, David Kim usually triggers a manual re-sync of the `opportunities` table at 2 AM.

---

## 📑 Appendix: Plan Tiers (Reference)

*   **Free:** 100 runs/mo. No SSO. (30% of accounts)
*   **Pro:** $49/seat. 10k runs/mo. (38% of accounts)
*   **Business:** $149/seat. 100k runs/mo. SSO + Priority support. (27% of accounts)
*   **Enterprise:** Custom. Unlimited runs. CSM included. (5% of accounts)

---

*This document is the property of Acme Inc. For current data definitions, please refer to the Notion Workspace.*

---
**EOF - Archive Entry 2025-Q4**