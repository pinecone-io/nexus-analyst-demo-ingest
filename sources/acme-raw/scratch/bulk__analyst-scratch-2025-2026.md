---
title: "Analyst scratch pad / working notes — 2025-2026"
source_url: "internal://acme/analyst-scratch-2025-2026"
license: "synthetic-demo"
attribution: "Synthetic content, Acme Inc internal demo. Acme Inc is a fictitious company."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: notion_runbook
---

# 🛠️ Data Team Scratchpad (2025-2026)

*This is a shared workspace for the data/analytics team to dump rough queries, debug logs, abandoned ideas, and prep notes. DO NOT use these queries for production reporting without verifying the logic. For production, see the `dbt` repo.*

---

**Date:** 2025-07-14
**Author:** lina.cho
**Subject:** Board Deck Prep - Preliminary ARR check

Trying to reconcile the MRR from `dim_customers` vs the `arr_snapshot`. Rachel is asking why the dashboard says $39.2M but her manual spreadsheet says $42M. 

Wait, the $42M is definitely a stale Looker PDT. I checked the cache.
Real ARR is closer to $39M.

```sql
-- WRONG PATH ATTEMPT
SELECT sum(current_mrr_usd) * 12 
FROM nexus-analyst-demo.acme.marts.finance.dim_customers; 
-- ERROR: Table not found. 
-- Note to self: The BQ dataset is FLAT. Stop using the dbt folder structure as a path.
```

Corrected query:
```sql
SELECT 
    snapshot_date, 
    arr_usd, 
    arr_pro_usd, 
    arr_business_usd, 
    arr_enterprise_usd
FROM `nexus-analyst-demo.acme.arr_snapshot`
WHERE snapshot_date = '2025-07-01'
LIMIT 10;
```

Result: ~39.1M total.
Biz is the bulk (~32M).
Ent is ~6M.
Pro is the rest.

TODO: Lina to ask Rajiv why `dim_customers.current_mrr_usd` drifts from `arr_snapshot`. 
*Update 14:00:* Rajiv says `dim_customers` is a point-in-time snapshot updated intraday, but `arr_snapshot` is the canonical board record. Use the snapshot for the deck!

---

**Date:** 2025-08-02
**Author:** rajiv.menon
**Subject:** dbt model `fact_workflow_runs` debugging

The incremental load for `fact_workflow_runs` failed again. Fivetran had a schema update on the source side (they added `step_metadata`? No, wait, that was a different project).

Checking source freshness:
```sql
SELECT 
    max(triggered_at) as last_run,
    count(*) as row_count
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE triggered_at > '2025-08-01 00:00:00';
```
Rows are there. The failure in dbt was a `SCHEMA_MISMATCH` on a legacy view someone created in the production dataset manually. Deleted the view.

Also, someone is querying `nexus-analyst-demo.acme.marts.cs.account_health` again and complaining it doesn't exist. 
**TEAM: ALL TABLES ARE UNDER `nexus-analyst-demo.acme`. NO NESTED DATASETS.**

---

**Date:** 2025-09-20
**Author:** nina.patel
**Subject:** Engagement Metric Recalibration Prep (Q4 Plan)

The current "engaged" definition is too loose. Elena thinks we're over-reporting health.
Current: 1 active user + 1 successful run.
Proposed: ≥3 active users AND ≥10 successful workflow runs in trailing 28 days.

Let's see how many customers drop off with the new threshold.

```sql
WITH engagement_metrics AS (
    SELECT 
        customer_id,
        count(distinct user_id) as active_users,
        sum(n_success) as total_success_runs
    FROM `nexus-analyst-demo.acme.workflow_runs_daily`
    WHERE run_date >= date_sub('2025-09-20', interval 28 day)
    GROUP BY 1
)
SELECT 
    CASE 
        WHEN active_users >= 1 AND total_success_runs >= 1 THEN 'Old_Engaged'
        ELSE 'Not_Engaged'
    END as old_status,
    CASE 
        WHEN active_users >= 3 AND total_success_runs >= 10 THEN 'New_Engaged'
        ELSE 'Monitoring'
    END as new_status,
    count(*) as customer_count
FROM engagement_metrics
GROUP BY 1, 2;
```

*Nina's Note:* Huge shift. About 150 customers move from "Engaged" to "Monitoring". This is going to make the Q4 health report look scary. I need to warn Dan and Elena. 

---

**Date:** 2025-10-05
**Author:** david.kim
**Subject:** BQ Cost analysis & Slot contention

We had a massive spike in BQ costs on Tuesday. 
Someone ran a `SELECT *` on `fact_user_events` without a date filter.
It was me. Sorry. 

Also checking slot contention during the 8AM UTC refresh:
```sql
SELECT
    job_id,
    creation_time,
    total_slot_ms / (total_bytes_billed / 1024 / 1024) as slot_intensity
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time > '2025-10-01'
ORDER BY total_slot_ms DESC
LIMIT 10;
```
Most intensive query is `bookings_attribution` recalculating the last 3 years of first-touch. We should probably materialize that as an incremental table instead of a view.

---

**Date:** 2025-11-12
**Author:** marco.silva
**Subject:** Account Review Prep - Onyx Robotics (cust_000704)

Prepping for Tom Becker. Onyx is one of our biggest Enterprise accounts.
Plan: Enterprise, 500 seats.
MRR: $35,000 (~$420K ARR).

Quick check on their ticket history:
```sql
SELECT 
    priority, 
    status, 
    opened_at, 
    category
FROM `nexus-analyst-demo.acme.fact_support_tickets`
WHERE customer_id = 'cust_000704'
  AND priority = 'P1'
  AND opened_at > '2025-10-01';
```
They had a P1 last week for `AUTH_FAILED` on their SAP integration. Closed in 4 hours.
Health score should be "Stable" or "Healthy Expansion" because they're heavily engaged. 

Wait, let me check `account_health`.
```sql
SELECT account_health_status, is_engaged, utilization_band
FROM `nexus-analyst-demo.acme.account_health`
WHERE customer_id = 'cust_000704';
```
Status: `healthy_expansion`.
Utilization band is NULL (Enterprise accounts don't use the seat-based utilization rule in health status logic).

---

**Date:** 2025-12-18
**Author:** lina.cho
**Subject:** NRR Calculation Attempt (Board Draft)

I'm trying to calculate the trailing 12-month NRR for the 2025 year-end report.
Logic: Take all paid customers from Dec 2024. See what they are paying today (Dec 2025).

```sql
-- DRAFT 1: Using Inner Join (WRONG)
WITH cohort_dec_2024 AS (
    SELECT customer_id, mrr_usd as start_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE start_date <= '2024-12-31' 
      AND (end_date IS NULL OR end_date > '2024-12-31')
      AND plan_tier != 'Free'
),
current_dec_2025 AS (
    SELECT customer_id, mrr_usd as end_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE is_current = true
      AND plan_tier != 'Free'
)
SELECT 
    sum(c.start_mrr) as base,
    sum(curr.end_mrr) as current,
    sum(curr.end_mrr) / sum(c.start_mrr) as nrr
FROM cohort_dec_2024 c
INNER JOIN current_dec_2025 curr ON c.customer_id = curr.customer_id;
```
Result: 1.11. 
*Lina Note:* This seems way too high. Oh, wait. The INNER JOIN is dropping all the customers who churned! If they aren't in `current_dec_2025`, they disappear from the calculation. This inflates the number.

```sql
-- DRAFT 2: Using Left Join (CORRECTED)
WITH cohort_dec_2024 AS (
    SELECT customer_id, mrr_usd as start_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE '2024-12-01' BETWEEN start_date AND coalesce(end_date, '2026-01-01')
      AND plan_tier != 'Free'
),
current_dec_2025 AS (
    SELECT customer_id, mrr_usd as end_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE is_current = true
      AND plan_tier != 'Free'
)
SELECT 
    sum(c.start_mrr) as denom,
    sum(coalesce(curr.end_mrr, 0)) as num,
    sum(coalesce(curr.end_mrr, 0)) / sum(c.start_mrr) as nrr
FROM cohort_dec_2024 c
LEFT JOIN current_dec_2025 curr ON c.customer_id = curr.customer_id;
```
Result: 1.07. 
This matches the `nrr_trailing_12` mart. I should have just queried the mart.
NRR ~107%, GRR ~94%. The difference is the expansion from Business -> Enterprise (AE-led).

---

**Date:** 2026-01-05
**Author:** rajiv.menon
**Subject:** FY26 Goal Setting - Table Cleanup

Cleaning up the `acme` dataset. There are a lot of temp tables like `lina_check_v2` and `nina_test`.
Going to drop anything older than 90 days that isn't in the dbt manifest.

Also, Jasmine (Marketing) is asking why `fact_marketing_touches` doesn't have the full ACV for "Free -> Pro" conversions. 
*Answer:* As per canon, self-serve PLG conversions don't show up in `bookings_attribution` (that's AE-led only). They are tracked in `fact_subscriptions` with `change_type`. Marketing needs to look at attribution there.

---

**Date:** 2026-02-19
**Author:** marco.silva
**Subject:** Churn Alert - Beacon Studios (cust_000287)

Beacon Studios churned yesterday (2026-02-18). 
I'm looking at their history to see if we missed signals.
- Tier: Business
- Seats: 65
- MRR: $9,685

Querying health:
```sql
SELECT *
FROM `nexus-analyst-demo.acme.account_health`
WHERE customer_id = 'cust_000287'
-- Snapshot from Feb 1st
```
Health was "Healthy Expansion" on Feb 1st. 
Engagement: 12 active users, 450 workflow runs.
NPS: 9 (Responded in Jan).

Notes from meeting with Elena: This was NOT product dissatisfaction. Their parent company (some conglomerate) is consolidating tools and moving them to a legacy internal system. Nothing we could do. CSM notes say "Procurement driven churn." 

---

**Date:** 2026-03-10
**Author:** nina.patel
**Subject:** VRS Analysis (Draft)

Elena wants a "Value Realization Score" (VRS) to complement the account health score.
Columns needed: `vrs_band`, `champion_login_recency`.

```sql
SELECT 
    customer_id, 
    vrs_band, 
    champion_login_recency
FROM `nexus-analyst-demo.acme.account_health`
LIMIT 10;
```
**UPDATE:** Column `vrs_band` does not exist. 
Checked with David Kim. The VRS model is a PARKED draft spec. Engineering hasn't prioritized the data pipeline for it yet.
*Decision:* Parked. Use existing `account_health_status` and `is_engaged` as the proxy for now.

---

**Date:** 2026-04-12
**Author:** lina.cho
**Subject:** Q1 Bookings by Channel

Jasmine wants the breakdown for the Q1 board meeting. 

```sql
-- Reminder: bookings_acv_usd is ALREADY ANNUALIZED. 
-- Do not multiply by 12.

SELECT 
    first_touch_channel,
    sum(bookings_acv_usd) as total_acv
FROM `nexus-analyst-demo.acme.bookings_attribution`
WHERE closed_won_at BETWEEN '2026-01-01' AND '2026-03-31'
GROUP BY 1
ORDER BY 2 DESC;
```

Results (Rough):
- Outbound: $1.2M
- Partner: $800K
- Event: $450K
- Inbound: $300K
- Referral: $150K

*Lina's note:* Outbound is really carrying the weight for Enterprise/Business. Sarah Chen and Tom Becker had a monster Q1.

---

**Date:** 2026-04-28
**Author:** david.kim
**Subject:** Workflow Run Errors - Trend Analysis

Seeing a lot of `INTEGRATION_DOWN` errors lately. 
```sql
SELECT 
    date(triggered_at) as day,
    error_code,
    count(*) as error_count
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE triggered_at > '2026-04-01'
  AND status = 'error'
GROUP BY 1, 2
ORDER BY 1 DESC, 3 DESC;
```
It's mostly the Salesforce integration. Probably related to their API versioning update. 
Not an Acme platform issue, but CSMs should reach out to heavy SFDC users. 
Top impacted: Onyx Robotics (cust_000704) and Harbor Dynamics (cust_000713).

---

**Date:** 2026-05-02
**Author:** rajiv.menon
**Subject:** Random Cleanup

- Found a bunch of queries using `INNER JOIN` for NRR in the "Marketing_Final" folder. Fixed them to `LEFT JOIN` so we don't hide churn. 
- Reminded Sarah Chen that `bookings_acv_usd` is annual. She was reporting $12M bookings for a $1M deal. 
- Adjusted the `account_health` refresh to 6AM UTC so it's ready for the US East Coast morning.

---

**Date:** 2025-06-15
**Author:** nina.patel
**Subject:** Investigating "Critical" status for Enterprise

Elena is confused why Marigold Health (cust_000701) isn't "Critical" even though their utilization is low.

*Check logic:*
```sql
SELECT 
    customer_id, 
    account_tier, 
    utilization_band, 
    has_uncollectible_recent,
    account_health_status
FROM `nexus-analyst-demo.acme.account_health`
WHERE customer_id = 'cust_000701';
```
Marigold Health is Enterprise.
According to the logic: Enterprise accounts are ONLY "Critical" if there is an uncollectible recent invoice. 
They don't have the utilization rule (< 0.20) because Enterprise seat counts are often massive and ramp up slowly.
Marigold is "Stable" or "Monitoring". It only becomes Critical if Rachel Stein flags the bill as uncollectible.

For SMB/MM (Pro/Business), < 0.20 utilization DOES trigger Critical. 

---

**Date:** 2025-06-22
**Author:** marco.silva
**Subject:** Quick check on Tamarind Group (cust_000706)

They went to "Paused" status in Jan 2026. 
Checking their last active stats:
```sql
SELECT 
    run_date, 
    n_runs
FROM `nexus-analyst-demo.acme.workflow_runs_daily`
WHERE customer_id = 'cust_000706'
ORDER BY run_date DESC
LIMIT 5;
```
0 runs since late December. 
CSM notes say they are undergoing a massive internal restructuring and will resume in June. Keep them in "Paused" (Free tier equivalent MRR for now).

---

**Date:** 2025-05-30
**Author:** lina.cho
**Subject:** Plan Math for Pro vs Business

Just double checking the seat logic for the dim_plans table.
Pro = $49/seat. Min 1.
Business = $149/seat. Min 50.

If Cobalt Systems (cust_000700) has 80 seats on Business:
80 * 149 = $11,920 MRR.
$11,920 * 12 = $143,040 ARR.

Check:
```sql
SELECT current_mrr_usd 
FROM `nexus-analyst-demo.acme.dim_customers` 
WHERE customer_id = 'cust_000700';
```
Result: 11920. Correct.

---

**Date:** 2026-05-03
**Author:** david.kim
**Subject:** BI Lag Check

BI Warehouse is lagging about 2h 15m behind prod today. Fivetran is struggling with the `fact_user_events` volume.
I'm going to look into partitioning `fact_user_events` by `event_at` date to speed up the incremental merges. 

Current event count: ~1.2M rows.
It's growing fast. We might need to move to a more aggressive clustering strategy.

---

**Date:** 2025-10-25
**Author:** rajiv.menon
**Subject:** dbt macro investigation

Trying to automate the `is_engaged` flag so we don't have to hardcode the (3 users / 10 runs) logic in five different views.
Created a draft macro `engagement_check(users, runs)`.

```sql
/*
{% macro engagement_check(user_col, run_col) %}
    ({{ user_col }} >= 3 AND {{ run_col }} >= 10)
{% endmacro %}
*/
```
Will deploy to `marts` next week.

---

**Date:** 2026-01-15
**Author:** nina.patel
**Subject:** Churn reason analysis

Pulling data for Marco on "Product Fit" churns.
Juniper Collective (cust_000712) churned in Jan.

```sql
SELECT 
    c.company_name, 
    f.loss_reason, 
    f.amount_usd
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.fact_opportunities` f ON c.customer_id = f.customer_id
WHERE c.status = 'churned'
  AND c.churn_date >= '2026-01-01';
```
Wait, `fact_opportunities.loss_reason` is for LOST DEALS (Pre-customer).
For churned CUSTOMERS, we need to look at the CSM's `churn_notes` or a separate survey table.
*Note:* We don't have a `fact_churn_surveys` yet. I'll have to scrape the CSM Notion board. 

---

**Date:** 2025-11-03
**Author:** lina.cho
**Subject:** Quick check on Kestrel Networks (cust_000708)

They churned in Nov 2025. 
Reason: Budget cuts. 
They were a Business tier customer, 70 seats. 
MRR was $10,430. 
Loss to ARR: ~$125K. 

I see their final invoice was paid, so they aren't "uncollectible," just a standard cancellation.

---

**Date:** 2026-04-15
**Author:** marco.silva
**Subject:** Sable Analytics (cust_000710) QBR prep

Sable Analytics (Business, 90 seats, $13,410 MRR).
Ae: Sarah Chen. 
CSM: Me.
Region: EMEA.

They are doing great. 
Utilization: 82/90 seats (0.91 utilization band).
Engagement: 25 active users. 
They are a prime candidate for "Healthy Expansion" or even an Enterprise upgrade if they hit the 250 seat mark. 
Sarah should reach out about the Enterprise security features (SSO/Audit logs) soon. 

---

**Date:** 2025-08-15
**Author:** david.kim
**Subject:** Fivetran sync issues

The `fact_invoices` sync failed because of a weird character in a customer name. 
Resolved. 
Also, I'm seeing a lot of `NULL_PAYLOAD` errors in `fact_workflow_runs`. 
It's about 0.5% of runs.
```sql
SELECT 
    error_code, 
    count(*) 
FROM `nexus-analyst-demo.acme.fact_workflow_runs` 
WHERE status = 'error' 
GROUP BY 1;
```
`AUTH_FAILED` is the leader (60%), then `INTEGRATION_DOWN` (20%), then `NULL_PAYLOAD` (5%).

---

**Date:** 2026-03-25
**Author:** nina.patel
**Subject:** NPS Check - Survey Quarter Q1 2026

Results are coming in for the Q1 NPS survey.
```sql
SELECT 
    segment, 
    avg(score) as avg_nps, 
    count(*) as responses
FROM `nexus-analyst-demo.acme.fact_nps_responses`
WHERE survey_quarter = '2026-Q1'
GROUP BY 1;
```
Enterprise is high (9.2).
Pro is lower (7.1). 
We need to look at the Pro comments. A lot of users are asking for more than 2 active workflows on the Free tier, but we shouldn't budge on that yet—it's our main conversion lever.

---

**Date:** 2025-12-01
**Author:** rajiv.menon
**Subject:** Schema Migration Plan

Moving `dim_employees` and `dim_customers` to a new clustering key (`region`).
This should speed up the CSM-specific dashboards Marco and Olivia use.

Don't forget: `csm_employee_id` in `dim_customers` links to `employee_id` in `dim_employees`.

---

**Date:** 2026-05-04
**Author:** lina.cho
**Subject:** Today's Snapshot

Final ARR check before the Monday morning standup.
```sql
SELECT sum(arr_usd) 
FROM `nexus-analyst-demo.acme.arr_snapshot` 
WHERE snapshot_date = '2026-05-04';
```
Wait, the snapshot hasn't run yet. Using yesterday's.
$39.05M. 
Stable. 

---

**Date:** 2025-09-05
**Author:** david.kim
**Subject:** Workflow Step-level data

Dan Lee (VP Product) asked if we can see which *step* in a workflow is failing.
*Response:* No. As per canon, we do NOT have step-level facts in the BI warehouse. We only have the aggregate `fact_workflow_runs`. 
If they want step-level details, they need to look at the application logs in Datadog. 

---

**Date:** 2026-02-01
**Author:** nina.patel
**Subject:** Engagement Drift

Checking if customers are slipping out of "Engaged" status.
```sql
SELECT 
    customer_id, 
    company_name, 
    account_tier
FROM `nexus-analyst-demo.acme.account_health`
WHERE account_health_status = 'monitoring'
  AND current_plan_tier IN ('Business', 'Enterprise');
```
We have 42 Business/Enterprise accounts in "Monitoring". 
Marco, you should check these. They have seats but aren't running many workflows.

---

**Date:** 2025-07-22
**Author:** lina.cho
**Subject:** Attribution check

Marketing spent $50k on a "Workflow Wisdom" content campaign.
Let's see the attributed revenue in `fact_marketing_touches`.

```sql
SELECT 
    sum(attributed_revenue_usd) 
FROM `nexus-analyst-demo.acme.fact_marketing_touches`
WHERE utm_campaign = 'workflow_wisdom';
```
Result: $12,500. 
*Lina Note:* This seems low, but remember this only tracks the "Touch" attribution. Some of these leads are still in the pipeline as Opportunities. 

---

**Date:** 2026-04-30
**Author:** rajiv.menon
**Subject:** End of Month check

Everything looks clean.
`dim_dates` is populated through 2027.
`arr_snapshot` is healthy.
CSAT scores are trending up. 

Final note: Who is theo.novak? I see them in the `dim_users` table for like 5 different customers. 
*Marco:* Oh, Theo is a consultant who manages automation for a few of our EMEA clients. He's not an Acme employee. 

---

**Date:** 2025-11-20
**Author:** nina.patel
**Subject:** Query Performance - Workflow Daily

The `workflow_runs_daily` table is getting slow to query. 
```sql
-- SLOW QUERY
SELECT customer_id, avg(success_rate)
FROM `nexus-analyst-demo.acme.workflow_runs_daily`
GROUP BY 1;
```
Adding a `run_date` filter is mandatory now. I'll add a check in the Looker view to force a filter. 

---

**Date:** 2026-01-20
**Author:** david.kim
**Subject:** P1 Support Ticket Spike

We had 15 P1 tickets yesterday. 
Investigation: `INTEGRATION_DOWN` for Slack. 
It's resolved, but `fact_support_tickets` is going to show a spike in `resolution_time_hours` because the queue got backed up.

---

**Date:** 2025-10-10
**Author:** lina.cho
**Subject:** MRR Drift again

I'm seeing a customer (cust_000714 Quartz Foundry) with $12,000 MRR in `fact_subscriptions` but $11,500 in `dim_customers`. 
*Rajiv:* That's because `dim_customers` updates on a 24h cycle, but `fact_subscriptions` is updated hourly via the billing system sync. Trust the subscription table for MRR. 

---

**Date:** 2026-03-01
**Author:** marco.silva
**Subject:** Driftwood Media (cust_000702) Expansion

They are on Pro (18 seats). 
They just hit their workflow run quota (10K/mo). 
They should be pushed to Business. 
AE: Yuki Sato. 

---

**Date:** 2025-05-15
**Author:** rajiv.menon
**Subject:** dbt documentation

Added descriptions for `utilization_band` in `account_health`.
`utilization_band` = `active_users_28d` / `seat_count_licensed`.
Note: It's NULL for Enterprise. 

---

**Date:** 2026-02-10
**Author:** nina.patel
**Subject:** NPS Detractor follow-up

One detractor from Verdant Cloud (cust_000707).
Score: 3.
Comment: "The audit log doesn't show enough detail on user-invited events."
This is a Dan Lee (Product) problem. I'll flag it in the product sync. 

---

**Date:** 2025-12-25
**Author:** david.kim
**Subject:** Holiday Coverage

I'll be OOO. 
The dbt runs are on auto-pilot. 
If the BQ slot usage goes over 2000, kill the Looker scheduled downloads. 

---

**Date:** 2026-04-20
**Author:** lina.cho
**Subject:** GRR vs NRR

Just a reminder for the Finance team: 
GRR (Gross Retention) caps at the denominator. It doesn't count expansion. 
NRR (Net Retention) includes expansion. 
Our GRR is ~94% (meaning we lose ~6% to churn/downgrades). 
Our NRR is ~107% (meaning the remaining 94% expands enough to get us to 107%). 
This is a healthy SaaS engine. 

---

**Date:** 2025-06-30
**Author:** nina.patel
**Subject:** SQL Snippet: Active Users by Role

```sql
SELECT 
    role, 
    count(*) as user_count
FROM `nexus-analyst-demo.acme.dim_users`
WHERE is_active = true
GROUP BY 1
ORDER BY 2 DESC;
```
Result: 
- Editor: 12,400
- Admin: 2,100
- Viewer: 1,500

(Note: These are across all customers).

---

**Date:** 2026-05-01
**Author:** rajiv.menon
**Subject:** Table fresh for May

May 1st data is in. 
NRR mart updated. 
Health scores recalculated. 
Ready for the Q2 push. 

---

**Date:** 2025-09-12
**Author:** marco.silva
**Subject:** Yarrow Logistics (cust_000703) Health

Tier: Business.
Seats: 120.
MRR: $17,880.
Health: `at_risk`.
Why? They have an open P1 ticket that's been open for 72 hours. 
The rule is: `has_open_p1_over_48h` = `at_risk`.
I need to ping Engineering to see why this is stuck. 

---

**Date:** 2026-03-15
**Author:** david.kim
**Subject:** BigQuery Storage optimization

We are paying for 5TB of storage. 
`fact_workflow_runs` is 80% of that. 
I'm going to set a 2-year TTL on the raw data and keep only the aggregates in `workflow_runs_daily` for anything older.

---

**Date:** 2025-12-10
**Author:** lina.cho
**Subject:** AE Performance check

Sarah Chen is at 110% of her Q4 quota. 
Tom Becker is at 95%. 
Sarah's Cobalt Systems (cust_000700) and Quartz Foundry (cust_000714) deals really saved the quarter.

---

**Date:** 2026-01-30
**Author:** nina.patel
**Subject:** Engagement Recalibration (Post-mortem)

The new engagement rules (3 users / 10 runs) are now fully live in `account_health`.
CSMs are actually finding it more useful—it highlights the "ghost" accounts that were technically active but not really using the platform. 

---

**Date:** 2025-07-05
**Author:** rajiv.menon
**Subject:** Table: `fact_user_events` properties

The `properties_json` column is a mess. 
```sql
SELECT 
    JSON_EXTRACT(properties_json, '$.browser') as browser,
    count(*)
FROM `nexus-analyst-demo.acme.fact_user_events`
GROUP BY 1;
```
It's 90% Chrome. No surprise there. 

---

**Date:** 2026-04-05
**Author:** lina.cho
**Subject:** ARR snapshot verification

Snapshot: 2026-04-01
Total ARR: $38.9M. 
Wait, we lost Beacon Studios ($116K) in Feb. 
We added a few Pro deals. 
Overall ARR is holding steady despite the Beacon loss. 

---

**Date:** 2025-08-28
**Author:** marco.silva
**Subject:** Harbor Dynamics (cust_000713) QBR

Business tier. 150 seats. 
Utilization: 145/150. 
They need more seats! 
I'll send an intro to Omar Haddad (AE) to discuss a seat expansion. 

---

**Date:** 2026-02-28
**Author:** david.kim
**Subject:** Fivetran Audit

All connectors green. 
Sync latency is < 15 mins for `fact_subscriptions`. 
Perfect. 

---

**Date:** 2025-10-30
**Author:** rajiv.menon
**Subject:** Happy Halloween

The data team is dressing up as BigQuery Error Codes. 
Lina is `AUTH_FAILED`. 
I am `RATE_LIMITED`. 
David is `STEP_TIMEOUT`. 
Nina is `SCHEMA_MISMATCH`.

---

**Date:** 2026-05-04
**Author:** nina.patel
**Subject:** Final Scratchpad Entry for May Standup

- Board deck ARR: Use `arr_snapshot`.
- NRR: 107%.
- Health: Watch the 42 'monitoring' accounts.
- Churn: Beacon Studios was parent-company driven. 
- Engagement: Rules are stable. 

See you in the meeting.

---