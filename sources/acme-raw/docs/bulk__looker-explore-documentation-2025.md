---
title: "Looker explore and dashboard documentation — 2025 (partially stale)"
source_url: "internal://acme/looker-explore-documentation-2025"
license: "synthetic-demo"
attribution: "Synthetic content, Acme Inc internal demo. Acme Inc is a fictitious company."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: notion_runbook
---

# Looker explore and dashboard documentation — 2025 (partially stale)

**Status:** ⚠️ PARTIALLY STALE  
**Owner:** Rajiv Menon (@rajiv.menon) / Nina Patel (Inactive - @nina.patel)  
**Last Major Audit:** 2025-11-14  
**Next Review Due:** 2026-02-01 (OVERDUE)

---

## Overview
This document serves as the central directory for all Looker Explores and Dashboards within the Acme Inc Looker instance (`acme-looker-prod`). This was originally maintained by Nina Patel before the Q4 re-org. Rajiv Menon is currently auditing these to migrate away from the old dbt-marts folder references toward the flat BigQuery structure in `nexus-analyst-demo.acme`.

**IMPORTANT NOTE ON DATA PATHS:**
Many old explores reference `acme.marts.cs.*` or `acme.dbt_marts.*`. These do **NOT** exist in BigQuery. BigQuery is flat. All production tables live in `nexus-analyst-demo.acme`. If you see a 404/Table Not Found error, it’s because the `sql_table_name` in LookML is using a filesystem path instead of the BigQuery table path.

---

## 1. Executive Dashboards (Board Level)

### Dashboard: Executive Summary (V3.1)
*   **Description:** The "Single Source of Truth" for Sam Reyes (CEO) and Rachel Stein (CFO).
*   **Key Metrics:** ARR, NRR, GRR, Gross Margin, Total Headcount.
*   **Source Tables:** `nexus-analyst-demo.acme.arr_snapshot`, `nexus-analyst-demo.acme.nrr_trailing_12`, `nexus-analyst-demo.acme.dim_employees`.
*   **Known Issues:**
    *   **The Cache Incident:** During the Oct 2025 cache bug, this dashboard showed **$42M ARR**. This was wrong. It was double-counting certain Pro-tier expansions that occurred on the same day as a seat redistribution. The actual ARR as of early 2026 is ~$39M.
    *   **NRR Inflation:** Do NOT use the "Customer 360" explore for NRR. It uses an Inner Join on subscription changes which drops churned customers, inflating NRR to 120%+. The Executive Summary uses `nrr_trailing_12` which is the canonical board NRR (~1.07).
*   **Owner:** Rachel Stein (@rachel.stein)
*   **Stale Notes:** Reference to `acme.marts.finance.arr_summary` in the footer is deprecated. Use `arr_snapshot`.

### Dashboard: NRR Deep Dive (Cohort View)
*   **Description:** Breaks down Net Revenue Retention by cohort (Signup Month).
*   **Source Table:** `nexus-analyst-demo.acme.nrr_trailing_12`.
*   **Signal:** The cohort is defined as all paid (non-Free) customers as of `snapshot_date - 12 months`. 
*   **Logic:** Churned customers stay in the cohort with an end MRR of $0. If you see NRR above 115%, check that the `LEFT JOIN` on `fact_subscriptions` isn't accidentally filtered.
*   **Stale Entries:** Some filters still reference `customer_segment` which was replaced by `account_tier` (SMB, MM, Ent).

---

## 2. Customer Success & Health Explores

### Explore: Account Health Overview
*   **Source Table:** `nexus-analyst-demo.acme.account_health`
*   **FIXME:** Many links in the Looker folder still reference `acme.marts.cs.account_health`. **THIS PATH DOES NOT EXIST.** Update LookML to `nexus-analyst-demo.acme.account_health`.
*   **Key Dimensions:**
    *   `account_health_status`: {critical, at_risk, monitoring, stable, healthy_expansion}.
    *   `utilization_band`: `active_users_28d / seat_count_licensed`. (Note: NULL for Enterprise customers).
    *   `is_engaged`: Boolean. (Requires ≥3 active users AND ≥10 successful workflow runs in trailing 28 days).
*   **Logic Signal:** "Critical" status logic varies by tier. 
    *   **Enterprise:** ONLY critical if there is a recent uncollectible invoice.
    *   **Non-Enterprise:** Critical if uncollectible OR `utilization_band` < 0.20.
*   **Owner:** Elena Volkov (@elena.volkov)

### Explore: Customer 360
*   **Description:** Master view joining customers, subscriptions, support tickets, and NPS.
*   **Joins:** 
    *   `dim_customers` (base)
    *   `fact_subscriptions` (on customer_id)
    *   `fact_support_tickets` (on customer_id)
    *   `fact_nps_responses` (on customer_id)
*   **Stale Notes:** Elena requested a "Value Realization Score (VRS)" dimension. Rajiv Menon has **PARKED** this. `vrs_band` and `champion_login_recency` are NOT built. DO NOT use the "VRS Draft" folder; those fields return NULL.
*   **Usage Tip:** Use this to look up specific customers like Marigold Health (cust_000701) or Cobalt Systems (cust_000700).

---

## 3. Sales & Pipeline Explores

### Explore: Bookings Pipeline
*   **Source Table:** `nexus-analyst-demo.acme.bookings_attribution`
*   **Signal:** `bookings_acv_usd` is **ALREADY ANNUALIZED**. 
*   **Warning:** Marcus Webb (VP Sales) found AEs were multiplying this value by 12 in Excel exports. Do not do this. It results in massive over-reporting.
*   **Filters:** Exclude `Free` tier. PLG self-serve (Free -> Pro) does NOT appear here. This explore is for AE-led deals only.
*   **First Touch Channel:** Source of truth for Q1-bookings-by-channel. Valid values: `organic`, `paid_search`, `outbound`, `content`, `referral`, `partner`, `event`, `inbound`.

### Explore: Opportunity History
*   **Source Table:** `nexus-analyst-demo.acme.fact_opportunities`
*   **Owner:** Jorge Martinez (@jorge.martinez)
*   **Notes:** Currently messy due to the CRM migration. `loss_reason` field is 40% null for 2025-H1 deals. 
*   **Signal:** `closed_won_at` is the timestamp for conversion. If a deal is "Closed Won" but has no `closed_won_at` date, it’s a data entry error in the CRM, not a dbt bug.

---

## 4. Product & Engineering Performance

### Explore: Workflow Performance
*   **Source Table:** `nexus-analyst-demo.acme.workflow_runs_daily`
*   **Key Measures:**
    *   `success_rate`: `SUM(n_success) / SUM(n_runs)`
    *   `p95_duration_ms`: Latency monitoring.
*   **Error Distributions:** Group by `error_code`. 
    *   Values: `AUTH_FAILED`, `RATE_LIMITED`, `STEP_TIMEOUT`, `INTEGRATION_DOWN`, `SCHEMA_MISMATCH`, `NULL_PAYLOAD`.
*   **Owner:** Priya Anand (@priya.anand)
*   **Stale Notes:** This explore used to join to `fact_workflow_steps`. We removed that in June 2025 because it was 4TB and crashing Looker. **Step-level facts are no longer available in BI.**

### Explore: User Events (Engagement)
*   **Source Table:** `nexus-analyst-demo.acme.fact_user_events`
*   **Usage:** High-volume table. Use `event_at` filters or Looker will time out.
*   **Engagement Definition:** Recalibrated in 2025-Q4. Previously we counted any login as engagement. Now, "Engaged" requires ≥3 active users AND ≥10 successful runs.
*   **Distractor:** Some older dashboards still use `is_active` from `dim_users` as a proxy for engagement. This is too loose. Transition to `account_health.is_engaged`.

---

## 5. Marketing Attribution

### Dashboard: Marketing Performance Overview
*   **Source Tables:** `nexus-analyst-demo.acme.fact_marketing_touches`, `nexus-analyst-demo.acme.fact_opportunities`
*   **Logic:** Multi-touch attribution is NOT currently supported. This dashboard shows First Touch (from `bookings_attribution`) and Last Touch (from `fact_marketing_touches`).
*   **Owner:** Jasmine Park (@jasmine.park)
*   **Stale Notes:** References to `utm_content` are flaky as the tracking script was broken from August to October 2025. Use `utm_source` and `utm_medium` for reliable trending.

---

## 6. Support Analytics

### Explore: Support Ticket Deep Dive
*   **Source Table:** `nexus-analyst-demo.acme.fact_support_tickets`
*   **Key Measures:** `resolution_time_hours`, `csat_score`.
*   **Signal:** CSAT is only available for ~30% of tickets. Do not assume a high CSAT on low volume is representative.
*   **Customer context:** Join to `dim_customers` to see tier. Enterprise tickets get priority SLA (SLA is defined in `dim_plans`).

---

## 7. Inventory of Deprecated / Stale Dashboards
*The following dashboards are scheduled for deletion in Q3 2026. Do not use for external reporting.*

| Dashboard Name | Reason for Deprecation | Alternative |
| :--- | :--- | :--- |
| **Old Growth Dashboard (2024)** | Uses `dim_customers.current_mrr_usd` which drifts intraday. | `Executive Summary V3.1` |
| **CSM Pulse (Nina's Draft)** | References `acme.marts.cs.account_health` (Path Error). | `Account Health Overview` |
| **VRS Testing Lab** | Parked project. Data is inaccurate. | `Account Health Overview` |
| **Legacy Pipeline** | Missing `bookings_acv_usd` column (uses old `amount` field). | `Bookings Pipeline` |
| **User Activity Weekly** | Replaced by `Workflow Performance` due to scale issues. | `Workflow Performance` |
| **Tier Migration Tracker** | Logic broken after the "Pro" seat price change in 2025. | `NRR Deep Dive` |

---

## 8. LookML Snippet Guide (For Analytics Engineers)

When updating the `nexus-analyst-demo.acme` models, ensure the following logic is maintained to match the dbt definitions.

### ARR Logic (Signal)
```lookml
# DO NOT CALCULATE ARR FROM dim_customers.current_mrr_usd
# Use fact_subscriptions for real-time or arr_snapshot for historical
measure: total_arr {
  type: sum
  sql: ${TABLE}.mrr_usd * 12 ;;
  filters: [is_current: "yes", plan_tier: "-Free"]
}
```

### Engagement Logic (Signal)
```lookml
# Recalibrated Q4 2025
dimension: is_engaged_customer {
  type: yesno
  sql: (
    SELECT COUNT(DISTINCT u.user_id) 
    FROM ${fact_user_events.SQL_TABLE_NAME} u 
    WHERE u.customer_id = ${TABLE}.customer_id 
    AND u.event_at >= CURRENT_DATE - 28
  ) >= 3 
  AND (
    SELECT COUNT(*) 
    FROM ${fact_workflow_runs.SQL_TABLE_NAME} w 
    WHERE w.customer_id = ${TABLE}.customer_id 
    AND w.status = 'SUCCESS'
    AND w.triggered_at >= CURRENT_DATE - 28
  ) >= 10 ;;
}
```

### NRR Cohort Logic (Signal)
```lookml
# Canonical NRR calculation
# Cohort: Paid customers 12 months ago
# Numerator: Current MRR of that SAME group (including $0 for churns)
measure: nrr_trailing_12 {
  type: number
  sql: SAFE_DIVIDE(${sum_mrr_today}, ${sum_mrr_12_months_ago}) ;;
  value_format_name: percent_2
}
```

---

## 9. Appendix: Common Questions & Slack Chatter Archive

**Q: Why does the Executive Summary show $39M but my custom report shows $40.5M?**
**A (Rajiv Menon):** You are likely including "Free" customers with a dummy MRR value or you are looking at `dim_customers.current_mrr_usd` which hasn't synced with the subscription table yet. `arr_snapshot` is the only board-approved source.

**Q: I’m seeing a "Table not found: acme.marts.cs.account_health" error.**
**A (David Kim):** That’s the old dbt folder path. The analyst team used to think the dataset followed the folder structure. It doesn't. Change your SQL to `nexus-analyst-demo.acme.account_health`. I've told Nina to fix this 5 times, but she's OOO.

**Q: Is "Beacon Studios" (cust_000287) still in our NRR?**
**A (Lina Cho):** Yes. They churned in Feb 2026. They will stay in the NRR cohort (at $0 value) until Feb 2027. This is why NRR is ~1.07 and not 1.20. We don't just delete churned people from the denominator.

**Q: What is the "VRS Score" I see in the CSM folders?**
**A (Rajiv Menon):** It’s a ghost. We tried to build a "Value Realization Score" but Dan Lee (VP Product) changed the requirements halfway through. We are sticking to `account_health_status` for now. Don't use anything labeled VRS.

---

## 10. Metadata & Audit Trail
*   **2025-01-10:** Initial document creation by Nina Patel.
*   **2025-04-22:** Updated with "Pro" tier pricing changes ($49/seat).
*   **2025-08-15:** Added warning about `utm_content` tracking failure.
*   **2025-11-14:** Major update by Rajiv Menon to reflect "BigQuery Flat" migration status.
*   **2026-02-05:** Added note about the $42M ARR cache incident.
*   **2026-05-04:** Document marked as "Partially Stale" pending full audit.

---
*END OF DOCUMENT*

---
**Noise Appendix - Internal Chatter Logs (Unfiltered)**

*Rajiv Menon [11:42 AM]:* Hey David, did you move `fact_workflow_runs` yet? Looker is timing out on the `marts` path.
*David Kim [11:45 AM]:* It's already in the flat `acme` dataset. Nina just hasn't updated the LookML. She's still using the old folder names in the `sql_table_name` parameters.
*Rajiv Menon [11:46 AM]:* Cool. I'll do a find-and-replace this afternoon.
*Marcus Webb [1:02 PM]:* Why is my pipeline report showing $500k for the Marigold Health deal? The ACV is $180k.
*Lina Cho [1:05 PM]:* Marcus, you're looking at the old report that multiplies `bookings_acv_usd` by 12. `bookings_acv_usd` is already annual. You're effectively looking at Decennial Revenue there lol.
*Marcus Webb [1:10 PM]:* ... we should really rename that column.
*Sam Reyes [3:30 PM]:* Is the ARR $39M or $42M? Looker says $42M on the old dashboard.
*Rachel Stein [3:35 PM]:* It's $39M, Sam. The $42M was a cache bug from the Pro-tier migration. Rajiv is purging the old dashboard today.
*Elena Volkov [4:00 PM]:* Hey guys, where did the Value Realization Score go? I can't find it in the Account Health explore.
*Rajiv Menon [4:05 PM]:* We parked it, Elena. The logic for `champion_login_recency` was totally bugged because of how the SSO logs are formatted. Use the engagement flag (3 users / 10 runs) for now. It’s more reliable.
*Omar Haddad [4:15 PM]:* Does anyone know why Tamarind Group (cust_000706) is marked as "Paused"? Sarah said they're just restructuring.
*Elena Volkov [4:17 PM]:* Their procurement requested a pause due to a merger. They'll show up in MRR but we flag them as paused so CSMs don't get pinged for low utilization.
*Yuki Sato [4:20 PM]:* Quick check: Driftwood Media (cust_000702) is Pro tier, but showing 18 seats. Isn't the max for Pro lower?
*Lina Cho [4:22 PM]:* Pro doesn't have a max, it just lacks the SSO/Audit logs. Business starts at 50 seats min. They're fine.

---
*Acme Inc Confidential - For Internal Use Only*