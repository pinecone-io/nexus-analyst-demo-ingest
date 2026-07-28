---
title: "Incident postmortem archive — Acme data platform 2025-2026"
source_url: "internal://acme/incident-postmortems-2025-2026"
license: "synthetic-demo"
attribution: "Synthetic content, Acme Inc internal demo. Acme Inc is a fictitious company."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: postmortem
---

# ACME DATA PLATFORM POSTMORTEM ARCHIVE (2025-2026)

This document is a living repository of data-related incidents, outages, and "near-misses" for the Acme Inc data stack. This includes dbt, BigQuery (`nexus-analyst-demo.acme`), Looker, and our ingestion pipelines (Fivetran, Airbyte, custom scripts). 

---

## Incident: arr_snapshot stale during Board Meeting Prep — 2025-08-14
**Severity:** P0 (Executive Visibility)  
**Duration:** 6 hours (04:15 UTC - 10:20 UTC)  
**Affected Systems:** `nexus-analyst-demo.acme.arr_snapshot`, Executive Looker Dashboards  

**Timeline:**
* [04:15] dbt-cloud-job-112 (Daily Refresh) fails. Alert fires in #data-alerts but is missed due to timezone (US sleep).
* [07:30] lina.cho logs in to finalize the Board Deck for Sam Reyes. Notices "Snapshot Date" in the Executive Summary dashboard is yesterday's date.
* [07:45] lina.cho: "Hey @rajiv.menon, is the warehouse lagging? The arr_snapshot table in BQ hasn't updated. It's showing 2025-08-13 data."
* [08:00] rajiv.menon: "Checking. dbt run failed at the snapshot stage. Logs show a generic 500 from BigQuery."
* [08:15] sam.reyes: "@lina.cho @rajiv.menon I need the final ARR bridge by 10am for the board sync. What's the status?"
* [08:30] david.kim: "I'm seeing massive slot contention in the project. Looks like the Data Science team kicked off a massive backfill of `fact_user_events` using 2000 slots."
* [09:00] rajiv.menon: "We can't kill the DS backfill yet, but I'm trying to manually force the snapshot to run in the `high_priority` reservation."
* [10:00] Snapshot finally completes. ARR confirmed at ~$39M (specifically $38.8M for the snapshot).
* [10:20] Looker cache cleared. Dashboards updated.

**Root Cause:** 
BigQuery slot contention. The dbt job for `arr_snapshot` was running in the default on-demand pool, which was starved by a large-scale event backfill job from the product team. 

**Resolution:** 
Moved the daily snapshot job to a dedicated reservation.

**Action Items:**
- [x] Configure dbt jobs to use `acme-prod-reserved` slots. (assigned: rajiv.menon)
- [ ] Implement PagerDuty routing for dbt freshness failures between 04:00-08:00 PT. (assigned: david.kim)
- [x] Documentation: Update wiki on how to manually trigger `arr_snapshot` if pipeline stalls.

**Lessons Learned:** 
The board doesn't care about slot contention. If the data is stale on board day, we look like amateurs. We need a "Board Lock" period where no backfills are allowed.

---

## Incident: NRR Overstated in Q3 Reporting (Join Logic Error) — 2025-10-12
**Severity:** P1 (Financial Accuracy)  
**Duration:** Full quarter (detected during prep)  
**Affected Systems:** `nrr_trailing_12` mart, Looker Finance folder  

**Timeline:**
* [09:00] lina.cho: "I'm looking at the NRR trend for Q3. The mart is showing 1.11, but when I manually sum the cohort from 12 months ago, I'm getting something closer to 1.07. Why is the mart so high?"
* [11:30] rajiv.menon: "Checking the SQL in `marts/finance/nrr_trailing_12.sql`. Oh. Found it."
* [11:45] rajiv.menon: "Someone changed the join to `dim_customers` to an `INNER JOIN`. Since customers who churned are eventually moved to a different status or removed from the active view in some filters, they were dropping out of the denominator."
* [12:30] lina.cho: "Wait, so if a customer churns, they just... disappear from the cohort? That's why NRR looks so good. We're only counting the survivors."
* [13:00] rajiv.menon: "Exactly. The denominator was shrinking alongside the numerator. Corrected it to a `LEFT JOIN` on the historical snapshot and used `COALESCE(end_mrr_usd, 0)`."
* [15:00] Corrected NRR is 1.07. GRR is 0.94.

**Root Cause:** 
Incorrect SQL join logic in dbt. `INNER JOIN` on `dim_customers` filtered out churned customers from the starting cohort, leading to survival bias in the NRR calculation.

**Resolution:** 
Refactored `nrr_trailing_12` to use `LEFT JOIN` and ensured churned MRR is explicitly zeroed out in the end-state calculation.

**Action Items:**
- [x] Audit all cohort models for `INNER JOIN` vs `LEFT JOIN` patterns. (assigned: nina.patel)
- [x] Add dbt test for cohort size consistency (denominator should not change based on customer status). (assigned: rajiv.menon)
- [ ] Update Looker "NRR" metric description to explicitly state inclusion of churned accounts.

**Lessons Learned:** 
Always check your denominator. Survival bias is a silent killer in SaaS metrics.

---

## Incident: Executive Summary ARR Discrepancy ($42M vs $39M) — 2026-01-15
**Severity:** P1 (Trust Issue)  
**Duration:** 48 hours  
**Affected Systems:** Looker "Executive Summary" Dashboard, Persistent Derived Tables (PDTs)

**Timeline:**
* [08:00] Sam Reyes (CEO) emails Rachel Stein (CFO): "Looker says we hit $42M ARR this morning. Is that right? I thought we were at $39M."
* [09:15] rachel.stein: "@lina.cho check this. Did we land a massive Enterprise deal overnight?"
* [09:30] lina.cho: "Checking Salesforce... No. We have some expansion at Onyx Robotics (cust_000704) and Cobalt Systems (cust_000700), but nothing that adds $3M."
* [10:00] rajiv.menon: "I see the issue. The Executive Summary dashboard was looking at a Looker PDT `pdt_arr_bridge_calc` which hadn't refreshed in 3 days due to a hung scratch schema in BQ. It was showing an old, uncorrected projection."
* [11:00] lina.cho: "The canonical `nexus-analyst-demo.acme.arr_snapshot` says $38.9M. The Looker PDT was hallucinating $42M from a stale dev branch that got merged."
* [11:30] Sam Reyes: "Fix this. We can't have two versions of the truth."

**Root Cause:** 
Looker PDT (Persistent Derived Table) failed to rebuild because of a permissions error in the `looker_scratch` dataset. The dashboard reverted to a stale version of the table.

**Resolution:** 
Manually dropped the scratch table and forced a rebuild. Updated the dashboard to point directly to `arr_snapshot` (the canonical mart) instead of a Looker-defined PDT.

**Action Items:**
- [x] Deprecate `pdt_arr_bridge_calc` in Looker. (assigned: nina.patel)
- [x] Point all ARR-related tiles to `nexus-analyst-demo.acme.arr_snapshot`. (assigned: rajiv.menon)
- [ ] Set up Looker "Schedule Failure" alerts to go to #data-help. (assigned: david.kim)

**Lessons Learned:** 
Looker PDTs are not a substitute for dbt marts. Canonical data should live in BigQuery, not in Looker's scratch schema.

---

## Incident: Stripe Invoice Pipeline Stuck (Revenue Gap) — 2025-11-03
**Severity:** P2 (Accounting Delay)  
**Duration:** 3 days  
**Affected Systems:** `fact_invoices`, Fivetran Stripe Connector  

**Timeline:**
* [14:00] rachel.stein: "Lina, the revenue reconciliation for October is off. I'm seeing 0 invoices for the last 3 days in the finance report."
* [14:15] lina.cho: "Investigating. Looking at `fact_invoices`... yeah, `MAX(invoice_date)` is Oct 31. Nothing for Nov 1-3."
* [14:30] david.kim: "Fivetran logs show the Stripe connector is 'Succeeded', but 0 records updated. Looks like Stripe API changed the payload for the `invoice.paid` event and our dbt transformation is filtering out the new records because of a null check."
* [16:00] rajiv.menon: "Found it. We were filtering `WHERE amount_usd > 0`. Stripe's new credit logic for 'Marigold Health' (cust_000701) caused some invoices to have a `NULL` amount field during the transition state."
* [17:30] Fix deployed. Re-ran dbt for the last 3 days.

**Root Cause:** 
Brittle dbt transformation logic. `fact_invoices` was discarding records with `NULL` amounts before they were updated by the payment sync, leading to missing data for the period between invoice creation and payment.

**Resolution:** 
Modified logic to include all invoices regardless of `amount_usd` status, then handle nulls in the downstream `fact_subscriptions` logic.

**Action Items:**
- [x] Add dbt-expectations test to ensure `fact_invoices` count is roughly consistent day-over-day. (assigned: rajiv.menon)
- [ ] Create a Slack alert if `fact_invoices` has 0 rows for a 24-hour period. (assigned: david.kim)

**Lessons Learned:** 
A "successful" sync doesn't mean the data is there. Trust the volume, not just the status code.

---

## Incident: Onyx Robotics P1 — fact_workflow_runs Stale — 2026-02-10
**Severity:** P1 (Customer-Facing Data)  
**Duration:** 2 days (Stale data)  
**Affected Systems:** `fact_workflow_runs`, `workflow_runs_daily`, Customer Health Dashboard  

**Timeline:**
* [09:00] olivia.tran (CSM): "Hey team, Onyx Robotics (cust_000704) is asking why their 'Workflow Success' dashboard in the app is showing 0 runs for yesterday. They run 10k+ a day."
* [09:15] rajiv.menon: "Looking... `workflow_runs_daily` in BQ is indeed empty for Feb 9."
* [09:30] david.kim: "The ingestion job for `fact_workflow_runs` crashed. We had a schema mismatch. Product added a new `error_code` called `INTEGRATION_DOWN` which was longer than the VARCHAR(20) limit we had in the staging table (even though BQ is schema-less, our staging validator wasn't)."
* [11:00] nina.patel: "Wait, if this failed, why didn't the alert fire?"
* [11:15] rajiv.menon: "The alert was set to look at the *job* status. The job 'passed' because the error was handled by a try-catch in the loader script that logged it as a 'warning' instead of an 'error'."
* [14:00] Schema updated, data re-processed. Onyx Robotics runs are back.

**Root Cause:** 
A new error code in the production database exceeded the length limits of the analytical staging layer's validation logic.

**Resolution:** 
Increased field lengths and removed the "swallow errors" logic in the ingestion script.

**Action Items:**
- [x] Update `error_code` column to string(max) equivalent in all staging tables. (assigned: david.kim)
- [x] Fix the loader script to exit with code 1 on validation failure. (assigned: david.kim)
- [ ] Send apology note to Onyx Robotics champion (theo.novak). (assigned: olivia.tran)

**Lessons Learned:** 
"Warnings" in the data pipeline are just "Failures" that haven't been caught yet.

---

## Incident: Engagement Recalibration Panic (Q4 2025) — 2025-10-15
**Severity:** P2 (Executive Confusion)  
**Duration:** 1 week of confusion  
**Affected Systems:** `account_health`, `is_engaged` flag  

**Timeline:**
* [09:00] elena.volkov (VP CS): "Data team, we just had a massive drop in 'Engaged Customers'. We went from 680 to 510 overnight. Is the product broken? Did we have a mass churn event?"
* [10:30] rajiv.menon: "Checking... No churn event. `dim_customers` still shows ~745 active. Oh, wait. We merged the dbt PR #442 yesterday."
* [11:00] nina.patel: "Right. Per the Product/CS sync last month, we changed the definition of `is_engaged`. It used to be '1 run in 30 days'. Now it's '>=3 active users AND >=10 successful runs in 28 days'."
* [11:30] lina.cho: "Yeah, the drop is intentional. Those 170 customers were 'unengaged' by the new definition. They are mostly 'monitoring' status now."
* [12:00] elena.volkov: "We need to communicate this to the board before they see the dashboard. It looks like a cliff."

**Root Cause:** 
A pre-planned change in business logic was implemented without a corresponding "heads up" in the reporting layer, leading stakeholders to believe a real-world usage drop had occurred.

**Resolution:** 
Added a "Definition Change" annotation to the Looker charts.

**Action Items:**
- [x] Create a "Data Change Log" dashboard for executives. (assigned: lina.cho)
- [ ] Requirement: Any change to a "Signal" column (like `is_engaged`) requires a 24-hour notice in #announcements. (assigned: dan.lee)

**Lessons Learned:** 
Definition changes look exactly like outages in a time-series chart. Annotate everything.

---

## Incident: Search Index (Pinecone) Rebuild Outage — 2026-03-22
**Severity:** P1 (Product Feature Down)  
**Duration:** 4 hours  
**Affected Systems:** In-app Workflow Search, Pinecone Index  

**Timeline:**
* [14:00] Engineering alert: Search latency > 5000ms.
* [14:15] priya.anand: "Who is messing with the search index? Customers can't find their workflows."
* [14:30] david.kim: "I'm running a re-index of the workflow embeddings to include the new `step_count` metadata. I thought Pinecone handles zero-downtime re-indexing?"
* [14:45] david.kim: "Ah. I was using the `starter` pod type instead of the `s1` or `p1` for the temp index. It hit a memory limit and crashed the search service."
* [16:00] Index restored from backup. Re-indexing paused.
* [18:00] Search functionality fully restored.

**Root Cause:** 
Insufficient resource allocation during a metadata backfill for the vector database.

**Resolution:** 
Scaled index pods before attempting the next re-index.

**Action Items:**
- [x] Update search infrastructure to use vertical scaling for index updates. (assigned: david.kim)
- [ ] Implement a circuit breaker in the app so search fails gracefully (with a message) rather than timing out. (assigned: engineering-team)

---

## Incident: SSL Certificate Expiry on Staging Data Proxy — 2025-06-01
**Severity:** P3 (Developer Productivity)  
**Duration:** 12 hours  
**Affected Systems:** `staging.acme-data-proxy.internal`

**Timeline:**
* [08:00] rajiv.menon: "Can't run dbt in dev. Getting SSL verification errors connecting to the staging BQ proxy."
* [10:00] nina.patel: "Confirmed. The cert for `staging.acme-data-proxy.internal` expired at midnight."
* [12:00] david.kim: "Ops is on it. We didn't have auto-renew on for the internal staging CA."
* [20:00] Cert renewed.

**Root Cause:** 
Manual certificate renewal process was forgotten for a non-production (but critical) data endpoint.

**Resolution:** 
Added the staging cert to the global Acme Let's Encrypt / Cert-Manager rotation.

---

## Incident: Acme-Bot (Slack) "Quote of the Day" Loop — 2025-12-20
**Severity:** P4 (Nuisance)  
**Duration:** 2 hours  
**Affected Systems:** Slack #general channel

**Timeline:**
* [09:00] Acme-Bot: "The best way to predict the future is to create it."
* [09:01] Acme-Bot: "The best way to predict the future is to create it."
* [09:02] Acme-Bot: "The best way to predict the future is to create it."
* [09:05] sam.reyes: "Can someone kill the bot?"
* [11:00] Bot disabled.

**Root Cause:** 
A logic error in the `fact_workflow_runs` sample test script caused it to trigger the "Success Notification" webhook in a recursive loop.

**Resolution:** 
Disabled the "Quote of the Day" feature permanently. (Nobody liked it anyway).

---

## Incident: Duplicate fact_marketing_touches Rows — 2026-02-05
**Severity:** P2 (Marketing Attribution Error)  
**Duration:** 2 weeks (undetected)  
**Affected Systems:** `fact_marketing_touches`, `bookings_attribution`  

**Timeline:**
* [10:00] jasmine.park: "Lina, the Marketing-sourced revenue for Q1 is $8M. Our total ARR expansion is only $2M. How is that possible?"
* [11:00] lina.cho: "Checking the attribution model. It looks like `fact_marketing_touches` has 4x the usual volume."
* [12:00] rajiv.menon: "Found it. The `touch_id` wasn't being used as a unique key in the incremental load. Every time the dbt job ran, it re-inserted the same touches if they were within the 3-day lookback window."
* [14:00] rajiv.menon: "I've added a `unique_key = 'touch_id'` to the dbt config and run a `--full-refresh`."
* [16:00] Revenue attribution corrected. Marketing-sourced revenue is back to a sane ~$600k for the period.

**Root Cause:** 
Missing `unique_key` in an incremental dbt model configuration.

**Resolution:** 
Added unique keys and a primary key dbt test.

---

## Incident: dim_customers Region Mismatch (NA-West vs NA-East) — 2025-07-22
**Severity:** P3 (Reporting Annoyance)  
**Duration:** Ongoing since June  
**Affected Systems:** `dim_customers`  

**Timeline:**
* [09:00] omar.haddad (Sales): "Why is Driftwood Media (cust_000702) showing up in the NA-East report? They are based in Seattle."
* [10:00] lina.cho: "Looking at the source data... the Salesforce 'Billing State' is 'WA', but our geo-mapping table in dbt had a typo where 'WA' was mapped to 'NA-East' instead of 'NA-West'."
* [11:00] Corrected the mapping table.

**Root Cause:** 
Typo in a static CSV seed file used for geographic mapping.

---

## Incident: Looker PDT Overload (BigQuery Quota Exceeded) — 2026-04-20
**Severity:** P1 (Platform Instability)  
**Duration:** 3 hours  
**Affected Systems:** All Looker dashboards  

**Timeline:**
* [10:00] Users report "BigQuery: Quota Exceeded" errors in Looker.
* [10:30] david.kim: "Looker is trying to rebuild 14 PDTs simultaneously. We hit the concurrent query limit for the project."
* [11:00] rajiv.menon: "I'm killing the PDT jobs. We need to move these to dbt. These are heavy transformations that shouldn't be happening in the BI layer."
* [13:00] Quota reset. Services restored.

**Root Cause:** 
Too much logic being pushed into Looker PDTs rather than the warehouse preparation layer.

---

## Incident: Orphaned Subscriptions in fact_subscriptions — 2025-11-15
**Severity:** P2 (Data Integrity)  
**Duration:** 5 days  
**Affected Systems:** `fact_subscriptions`

**Timeline:**
* [09:00] lina.cho: "I'm seeing subscriptions in `fact_subscriptions` that don't have a corresponding `customer_id` in `dim_customers`."
* [10:00] rajiv.menon: "Checking. It looks like when a customer is deleted in the app (usually a Free tier user), we delete the record in `dim_customers` but the subscription history remains. We need to keep the customer record for historical ARR reporting even if they are 'deleted'."
* [12:00] Resolution: Changed the logic to a soft-delete in `dim_customers`.

---

## Incident: BigQuery Dataset Path Confusion — 2025-10-05
**Severity:** P4 (Developer Onboarding)  
**Duration:** N/A  

**Timeline:**
* [14:00] New analyst tries to query `acme.marts.cs.account_health`.
* [14:05] Query fails.
* [14:10] rajiv.menon: "Common mistake. The dbt folders are `marts/cs/`, but the BigQuery dataset is FLAT. Use `nexus-analyst-demo.acme.account_health`."

**Root Cause:** 
Assumed dbt folder structure mirrored BigQuery dataset structure.

**Resolution:** 
Updated the "Getting Started" doc.

---

### End of Archive. 
*Note: All monetary values are in USD. All timestamps are UTC unless otherwise noted. If you find a discrepancy in ARR reporting, please refer to the `arr_snapshot` canonical mart before escalating.*