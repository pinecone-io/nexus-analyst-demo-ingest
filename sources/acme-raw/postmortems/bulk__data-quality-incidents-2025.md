---
title: "Data quality incident log — 2025"
source_url: "internal://acme/data-quality-incidents-2025"
license: "synthetic-demo"
attribution: "Synthetic content, Acme Inc internal demo. Acme Inc is a fictitious company."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: postmortem
---

# Acme Data Quality Incident Log (2025)

This document serves as the rolling internal log for all Sev-1 through Sev-4 data quality incidents encountered by the Acme Data & Analytics team (Nina Patel, Rajiv Menon, David Kim, Lina Cho) during the 2025 fiscal year. Please ensure all entries include the correct incident ID, severity, and status. This log is used for quarterly reliability reviews with Priya Anand (VP Eng) and Rachel Stein (CFO).

---

### INC-2025-001: `arr_snapshot` inaccuracy due to dbt seed file override — 2025-01-12 | Sev: P1 | Status: resolved | Owner: nina.patel
**Incident Summary:** 
On the morning of Jan 12, Lina Cho noticed that the `arr_snapshot` table was reporting a total ARR of $36.2M, which contradicted the individual subscription sums in `fact_subscriptions` (showing closer to $38.5M). After investigation, it was discovered that a legacy dbt seed file (`manual_arr_adjustments.csv`), which was originally created in late 2024 to handle a one-off adjustment for a custom Enterprise deal (cust_000509), had a hard-coded override that was unintentionally being applied to the daily snapshot logic in `marts/finance/arr_snapshot.sql`. 
**Root Cause:**
The dbt model used a `LEFT JOIN` on the seed file and a `COALESCE` that prioritized seed values over the upstream `fact_subscriptions` data. The seed file had not been updated for the new fiscal year.
**Resolution:**
The seed file was deprecated and the logic was moved to a dynamic `case when` statement within the `fact_subscriptions` model to handle the unique billing cadence for the Enterprise tier. The `arr_snapshot` was full-refreshed for the period of Jan 1 - Jan 12 to restore correct history.

### INC-2025-002: NRR Inflation in Board Prep (Inner Join Bug) — 2025-01-24 | Sev: P1 | Status: resolved | Owner: rajiv.menon
**Incident Summary:** 
During the preliminary Q4 board deck review, Sam Reyes flagged an NRR (Net Revenue Retention) figure of 111%. While impressive, this felt "too high" compared to our known churn rate. Nina Patel re-ran the logic in an ad-hoc BigQuery scratchpad and discovered the actual NRR was 107%. The 4-point inflation was systemic in the `nrr_trailing_12` mart.
**Root Cause:**
The SQL used to generate the cohort as of `snapshot_date - 12mo` was performing an `INNER JOIN` between the starting cohort and the ending MRR table. This had the side effect of dropping all customers who had churned (as they had no record in the ending MRR table), effectively calculating "NRR for only the people who didn't leave us."
**Resolution:**
Rewrote the join logic in `nexus-analyst-demo.acme.nrr_trailing_12` to use a `LEFT JOIN` from the starting cohort, with a `COALESCE(end_mrr_usd, 0)` to ensure churned revenue ($0) was included in the numerator. This correctly reflected the 107% NRR. Added a dbt test to ensure the cohort count at the start of the period matches the count used in the final calculation.

### INC-2025-002-B (Post-Mortem Noise):
*Lina Cho: "Wait, so the 111% was actually fake? I already sent that to Rachel."*
*Rajiv Menon: "Yeah, it was an inner join issue. It was basically ignoring customers like Kestrel Networks (cust_000708) who churned in November. Once you add them back as $0, the number drops back to reality."*
*Lina Cho: "Classic. This is why we can't have nice things."*

### INC-2025-003: Looker Explore 404 (Pathing Error) — 2025-02-03 | Sev: P3 | Status: resolved | Owner: nina.patel
**Incident Summary:** 
Several CSMs (including Marco Silva and Olivia Tran) reported that the "Account Health Overview" dashboard in Looker was returning a "Table not found" error. This blocked several QBR preparations for the day.
**Root Cause:**
A recent change in the LookML model (pushed by a junior analyst) attempted to reference `nexus-analyst-demo.acme.marts.cs.account_health`. As per the BigQuery FLAT architecture, this path does not exist. The correct path is `nexus-analyst-demo.acme.account_health`. The analyst had assumed the dbt filesystem structure (folders) mapped to the BigQuery dataset structure.
**Resolution:**
Corrected the `sql_table_name` in the Looker view file to point to the flat `acme` dataset. Reminded the team in #data-eng that we do NOT use nested datasets in the analyst-demo environment.

### INC-2025-004: Duplicate Rows in `bookings_attribution` — 2025-02-15 | Sev: P2 | Status: resolved | Owner: david.kim
**Incident Summary:** 
Sales Ops (Jorge Martinez) noticed that the bookings ACV for several new Enterprise deals (including Onyx Robotics, cust_000704) was doubled in the marketing attribution reports. This was causing a significant overstatement of "referral" channel performance.
**Root Cause:**
The Salesforce sync via Fivetran had a duplicate record for a single Opportunity ID that had been merged in the CRM but not yet cleaned in the staging layer of the warehouse. The `bookings_attribution` model was not performing a `distinct` or `max(updated_at)` filter on the source opportunity table.
**Resolution:**
Implemented a `row_number() over (partition by opportunity_id order by _fivetran_synced desc)` filter in the staging model for Salesforce opportunities. Verified that `bookings_acv_usd` is already annualized and not being multiplied by 12 (verified signal canon).

### INC-2025-005: `dim_customers.industry` NULL handling bug — 2025-03-02 | Sev: P4 | Status: resolved | Owner: rajiv.menon
**Incident Summary:** 
Jasmine Park (VP Marketing) reported that ~15% of the "Business" tier customers were appearing as "Unknown" industry in the attribution dashboard, despite having industry data in Salesforce.
**Root Cause:**
The `dim_customers` model was using a `CASE` statement that was case-sensitive for the industry string. Salesforce was exporting "FinTech" while the dbt code was looking for "fintech".
**Resolution:**
Updated the industry mapping to use `LOWER()` on all source strings. Added a default value of 'Other' instead of NULL to prevent breakage in Looker's pivot functionality.

### INC-2025-006: Stale Fivetran Sync (Stripe) — 2025-03-18 | Sev: P2 | Status: resolved | Owner: david.kim
**Incident Summary:** 
The daily MRR reports were showing $0 for new signups on March 17. Sarah Chen (AE) noted that Marigold Health (cust_000701) had signed their Enterprise deal, but it wasn't showing in the MRR snapshot.
**Root Cause:**
The Stripe connector in Fivetran had stalled due to an expired API key (service account). No alerts were triggered because the "sync status" was still technically "green" but was processing 0 records per minute.
**Resolution:**
Rotated the API key and manually triggered a resync. Added a dbt freshness test on `stg_stripe__subscriptions` to alert if the maximum `_fivetran_synced` timestamp is older than 6 hours.

### INC-2025-007: Wrong calculation for `utilization_band` — 2025-04-05 | Sev: P2 | Status: resolved | Owner: nina.patel
**Incident Summary:** 
Grace Liu (CSM) flagged that several Pro customers (e.g., Driftwood Media, cust_000702) had a `utilization_band` of 2.5, which is mathematically impossible (should be 0.0 to 1.0).
**Root Cause:**
The formula used in `account_health` was `active_users_28d / min_seats` from `dim_plans` instead of `active_users_28d / seat_count_licensed` from `dim_customers`. For Pro customers who often have more seats than the 'min' (which is 1), this caused the ratio to explode.
**Resolution:**
Corrected the formula to use `seat_count_licensed`. Per canonical rules, ensured Enterprise customers return NULL for this field to avoid confusion, as their seat counts are often "unlimited" or governed by different contractual terms.

### INC-2025-008: `fact_user_events` Timezone Mismatch — 2025-04-20 | Sev: P3 | Status: resolved | Owner: rajiv.menon
**Incident Summary:** 
Analyst Lina Cho found that "Peak Usage Hour" reports were showing high activity at 3:00 AM San Francisco time.
**Root Cause:**
The event logging service was sending timestamps in UTC (correct), but the BigQuery `extract(hour from event_at)` was defaulting to the system time of the query runner (PST), leading to an 8-hour offset that wasn't consistently applied across all models.
**Resolution:**
Standardized all downstream marts to use `DATETIME(event_at, "UTC")` before extraction. Updated the `dim_dates` table to explicitly include UTC and PST columns for easier reporting.

### INC-2025-009: BigQuery Slot Contention during Monday Refresh — 2025-05-12 | Sev: P3 | Status: resolved | Owner: david.kim
**Incident Summary:** 
The 8:00 AM dbt cloud run failed with a "Quota Exceeded: Slot Contention" error. This delayed the Monday morning management report by 3 hours.
**Root Cause:**
Three different departments (Marketing, Finance, and CS) all scheduled heavy "ad-hoc" Looker PDT refreshes at exactly 8:00 AM on Monday, competing with the main dbt production run.
**Resolution:**
Moved the dbt production run to 6:00 AM UTC. Implemented BigQuery "Reservations" to prioritize the `transform` service account over the `looker` service account during the morning window.

### INC-2025-010: `account_health.is_engaged` Q4 Threshold Change Impact — 2025-10-15 | Sev: P2 | Status: resolved | Owner: nina.patel
**Incident Summary:** 
After the Q4 recalibration of engagement metrics, 200 accounts (mostly in the SMB/Pro tier) suddenly flipped from `is_engaged = TRUE` to `FALSE` overnight. Elena Volkov (VP CS) expressed concern that the health of the business was declining.
**Root Cause:**
This was not a data bug, but a "communication incident." The logic for `is_engaged` was tightened from "1 user, 1 run" to ">=3 users AND >=10 successful runs in 28d" (per canonical rules). The change was deployed without updating the "Engaged Customers" KPI dashboard documentation.
**Resolution:**
Updated the dashboard tooltips and the `account_health` model metadata. No code change required, but a historical "Engagement Version" column was added to the mart to allow for year-over-year comparison using the old logic.

### INC-2025-011: Duplicate `workflow_id` in `fact_workflow_runs` — 2025-10-28 | Sev: P3 | Status: resolved | Owner: rajiv.menon
**Incident Summary:** 
Reports for Tamarind Group (cust_000706) showed they were exceeding their quota by 2x, but their CSat score was high and they hadn't complained about rate limiting.
**Root Cause:**
A bug in the webhook listener was retrying failed deliveries but not deduplicating the `run_id` before writing to the raw logs. This resulted in duplicate entries in `fact_workflow_runs` for about 4% of all runs.
**Resolution:**
Added a `QUALIFY row_number() OVER (PARTITION BY run_id ORDER BY triggered_at ASC) = 1` clause to the dbt model.

### INC-2025-012: `vrs_band` Query Errors (Ghost Columns) — 2025-11-05 | Sev: P4 | Status: resolved | Owner: nina.patel
**Incident Summary:** 
Marcus Webb (VP Sales) complained that his custom "Expansion Leads" report was broken.
**Root Cause:**
The report was trying to query `vrs_band` and `champion_login_recency` from `account_health`. As per the canon fact sheet, these columns are part of a PARKED draft spec and were never actually built.
**Resolution:**
Deleted the broken Looker dashboard. Redirected Marcus to the `account_health_status` and `utilization_band` columns which are the current source of truth for expansion potential.

### INC-2025-013: Incorrect MRR for Tamarind Group (cust_000706) — 2025-11-12 | Sev: P3 | Status: resolved | Owner: lina.cho
**Incident Summary:** 
Tamarind Group's MRR was showing as $0 even though they are listed as "Active" in `dim_customers`.
**Root Cause:**
Tamarind Group had moved to a "Paused" status in January 2026, but the subscription record had a `NULL` end_date instead of the actual pause date, causing the `is_current` flag to behave unpredictably. Wait, investigating... actually, the issue was they were in the "Business" tier but were being billed via a legacy Pro plan in Stripe during their transition.
**Resolution:**
Manually corrected the `fact_subscriptions` entry to align with the $8,195 MRR (55 seats * $149).

### INC-2025-014: `bookings_acv_usd` Multiplication Error — 2025-11-20 | Sev: P1 | Status: resolved | Owner: rajiv.menon
**Incident Summary:** 
A Sales Analyst was found to be reporting $400M+ in New Bookings for Q3.
**Root Cause:**
The analyst had taken the `bookings_acv_usd` column from `bookings_attribution` and multiplied it by 12 in their local Tableau workbook. As per the canon, `bookings_acv_usd` is ALREADY annualized. 
**Resolution:**
Sent an all-hands email to the Sales Ops and Finance teams. Renamed the column in the staging layer to `annualized_bookings_acv_usd` to make it harder to misinterpret (though the mart kept its name for compatibility).

### INC-2025-015: `dim_customers` Regional Misclassification (APAC vs EMEA) — 2025-12-01 | Sev: P4 | Status: resolved | Owner: david.kim
**Incident Summary:** 
Yarrow Logistics (cust_000703) was appearing in EMEA reports despite being an APAC customer based in Singapore.
**Root Cause:**
The `country` to `region` mapping table in dbt had "Singapore" mapped to "EMEA" (likely a copy-paste error from "Switzerland").
**Resolution:**
Updated the `seed_country_region_map.csv` and re-ran `dim_customers`.

### INC-2025-016: Invalid `is_business_day` in `dim_dates` — 2025-12-15 | Sev: P4 | Status: resolved | Owner: nina.patel
**Incident Summary:** 
Support ticket "Resolution Time" metrics were looking artificially good for the week of Thanksgiving.
**Root Cause:**
`dim_dates` had not been updated with the 2025/2026 holiday calendar, so Thanksgiving Thursday and Friday were marked as `is_business_day = TRUE`.
**Resolution:**
Uploaded the updated holiday list for 2025-2027 and rebuilt the `dim_dates` table.

### INC-2025-017: NULL `acquisition_channel` for Enterprise Deals — 2025-12-20 | Sev: P3 | Status: resolved | Owner: rajiv.menon
**Incident Summary:** 
Marketing attribution was missing for several high-value accounts including Cobalt Systems (cust_000700) and Ember Industries (cust_000711).
**Root Cause:**
Enterprise deals often have a "Lead Source" in Salesforce that is different from the "First Touch" recorded by our web tracker. The `dim_customers` model was only looking at the web tracker.
**Resolution:**
Modified the `acquisition_channel` logic to prioritize `fact_marketing_touches` (web) but fall back to the Salesforce `LeadSource` if the web touch is missing.

### INC-2025-018: Account Health status "Critical" logic error — 2025-12-22 | Sev: P2 | Status: resolved | Owner: nina.patel
**Incident Summary:** 
Onyx Robotics (cust_000704) was flagged as "Critical" health, causing a panic in the CS department.
**Root Cause:**
The "Critical" rule was being applied to Onyx Robotics because their `utilization_band` was 0.15. However, Onyx is an Enterprise customer. Per the canon rules, Enterprise accounts should ONLY be "Critical" if they have an uncollectible invoice; utilization rules do not apply to them because they have custom seat arrangements.
**Resolution:**
Fixed the `CASE` statement in `account_health` to exclude Enterprise tier customers from the utilization-based "Critical" trigger.

### INC-2025-019: Stripe "Paid_at" Timestamp Lag — 2025-12-28 | Sev: P3 | Status: resolved | Owner: david.kim
**Incident Summary:** 
Finance reported that `fact_invoices` was showing 40+ unpaid invoices that were actually paid.
**Root Cause:**
Fivetran sync for the `invoices` table was only running once every 24 hours, while the `subscriptions` table was running every 6 hours. This created a state where a subscription looked "active" but the associated invoice looked "overdue."
**Resolution:**
Synced the frequencies of all Stripe-related connectors to 6 hours.

### INC-2025-020: `dim_employees` hire_date drift — 2025-12-30 | Sev: P4 | Status: resolved | Owner: lina.cho
**Incident Summary:** 
The "Revenue per Employee" report for the end of the year was slightly off.
**Root Cause:**
Several new hires in the EMEA office (Amsterdam) had hire dates that were off by one day due to the UTC conversion at the time of HRIS data entry.
**Resolution:**
Standardized on the "Effective Date" from the payroll system as the source of truth for `hire_date`.

### INC-2025-021: Looker Cache Staleness ($42M ARR) — 2025-12-31 | Sev: P3 | Status: resolved | Owner: nina.patel
**Incident Summary:** 
On the final day of the year, Sam Reyes saw "$42M ARR" on his dashboard, while the underlying BigQuery table showed ~$39.1M.
**Root Cause:**
Looker's cache was set to 12 hours for the Executive Dashboard. A high-volume test run of subscriptions on the 30th had inflated the cache, but the test data was subsequently purged from the warehouse. The dashboard was still showing the cached "test" number.
**Resolution:**
Manual cache clear. Reduced cache duration for the main "KPI North Star" dashboard to 2 hours to match the warehouse lag.

---
**End of 2025 Log**
*Note: For 2026 incidents, please refer to the new log at `internal://acme/data-quality-incidents-2026`.*