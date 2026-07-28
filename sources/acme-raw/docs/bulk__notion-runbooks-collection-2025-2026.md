---
title: "Notion runbooks and process docs collection — Acme data/ops team"
source_url: "internal://acme/notion-runbooks-collection-2025-2026"
license: "synthetic-demo"
attribution: "Synthetic content, Acme Inc internal demo. Acme Inc is a fictitious company."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: notion_runbook
---

# 🏠 Data & Ops Workspace

Welcome to the central repository for Acme Data and Revenue Operations. 
**Note:** Some docs here are actively maintained; others are historical artifacts. If you see something that looks wildly out of date, ask **Rajiv Menon** or **Lina Cho**.

---

## 📑 Table of Contents
1. [CSM Account Health Runbook](#csm-account-health-runbook)
2. [dbt Freshness & Data Quality Alerts](#dbt-freshness-runbook)
3. [Board Deck Prep Checklist (Monthly/Quarterly)](#board-prep-checklist)
4. [Data Warehouse Conventions & Naming](#dw-conventions)
5. [New Analyst Onboarding (WIP)](#analyst-onboarding)
6. [Quarterly Business Review (QBR) Template](#qbr-template)
7. [Churn Debrief Template](#churn-debrief)
8. [Looker Development Guidelines & Performance](#looker-guidelines)
9. [Support Ticket Triage & SLAs](#support-triage)
10. [Marketing Attribution Methodology](#marketing-attribution)
11. [Security Review & Incident Response](#security-incident)
12. [VRS Implementation Plan (PARKED)](#vrs-parked)
13. [On-Call Rotation & Escalation Paths](#on-call)

---

<a name="csm-account-health-runbook"></a>
## 📈 CSM Account Health Runbook
**Status:** ✅ Active
**Owner:** Elena Volkov / Rajiv Menon
**Last Updated:** 2026-03-15

This runbook explains how to interpret the `account_health_status` column in the `nexus-analyst-demo.acme.account_health` table.

### 1. Health Status Definitions
We categorize every paying customer into one of five bands. The logic is handled in `dbt` and refreshed daily at 02:00 UTC.

| Status | Meaning | Action Required |
|---|---|---|
| `critical` | Immediate churn risk or billing failure. | CSM P0: High-touch outreach / Executive intervention. |
| `at_risk` | Declining usage or recent negative sentiment. | CSM P1: Remediation plan needed within 5 days. |
| `monitoring` | Low engagement but no active "fire". | CSM P2: Schedule discovery call. |
| `stable` | Consistent usage, meeting quotas. | Standard cadence. |
| `healthy_expansion` | High utilization + Engaged. | AE/CSM Upsell motion. |

### 2. The "Critical" Rule Logic (IMPORTANT)
The logic for `critical` varies by customer tier. Do not apply the same rules for a Pro customer and an Enterprise customer.

*   **Enterprise Tier:** An account is marked `critical` **ONLY** if there is a recent uncollectible invoice (check `fact_invoices` for status). 
    *   *Note:* Enterprise accounts have unlimited runs/seats usually, so `utilization_band` doesn't trigger a critical flag here. 
*   **Non-Enterprise (Business/Pro):** An account is marked `critical` if:
    *   They have an uncollectible invoice **OR**
    *   `utilization_band` < 0.20 (active seats / licensed seats).

### 3. "At Risk" Triggers
An account moves to `at_risk` if any of the following are true:
*   `has_open_p1_over_48h` = TRUE (Support P1 ticket unresolved for >2 days).
*   `has_recent_nps_detractor` = TRUE (Score < 7 in `fact_nps_responses` in the last 90 days).

### 4. Engagement Definitions
A customer is considered **Engaged** (`is_engaged = TRUE`) if:
*   ≥ 3 active users in the trailing 28 days.
*   ≥ 10 successful workflow runs in the trailing 28 days.
*   *Historical Note:* We recalibrated this in 2025-Q4. Previously it was just 1 user and 1 run, which was way too noisy (captured too many "ghost" accounts).

---

<a name="dbt-freshness-runbook"></a>
## 🛠 dbt Freshness & Data Quality Alerts
**Status:** ✅ Active
**Owner:** Rajiv Menon
**Slack Channel:** #data-ops-alerts

### What to do when dbt-freshness fails:
If you receive a PagerDuty or Slack alert for source freshness:

1.  **Check the Table:** Is it `arr_snapshot` or `nrr_trailing_12`?
    *   If **`arr_snapshot`** is stale: This is a **P0**. Lina's finance reports will be wrong by morning. 
    *   If **`fact_workflow_runs`** is stale: Check with David Kim; the Airflow ingestion from the production replica might be hung.
2.  **Verify BigQuery:** 
    *   Run `SELECT max(snapshot_date) FROM nexus-analyst-demo.acme.arr_snapshot`.
    *   If it’s >24h old, the daily dbt run failed. 
3.  **The "Lags Prod" Rule:** BI warehouse lags production by approximately 2 hours. If a customer just signed up 15 minutes ago, they won't be in `dim_customers` yet. Don't panic.

### Common Failure Points:
*   **`nrr_trailing_12` Stale:** Usually happens if the `fact_subscriptions` upstream has a duplicate `subscription_id`. Check the `dbt` logs for unique key violations.
*   **Looker PDTs:** If a Looker dashboard shows "Stale Data" but BigQuery is fine, clear the Looker cache. (Reference the "Stale Cache Incident" of Jan '26).

---

<a name="board-prep-checklist"></a>
## 📊 Board Deck Prep Checklist
**Status:** ✅ Active
**Owner:** Lina Cho
**Audience:** Finance / Exec Team

**DO NOT RE-DERIVE ARR FROM `dim_customers.current_mrr_usd`.** This drifts intraday and will never match the month-end close.

### Step 1: ARR Reporting
*   **Canonical Table:** `nexus-analyst-demo.acme.arr_snapshot`
*   **Query:** `SELECT sum(arr_usd) FROM nexus-analyst-demo.acme.arr_snapshot WHERE snapshot_date = 'YYYY-MM-DD'`
*   **Validation:** 
    *   Total ARR should be ~$39M.
    *   Business ~$32M
    *   Enterprise ~$6M
    *   Pro ~$1M
*   **Error Check:** If you see $42M+, you are likely looking at the stale Looker PDT before the Jan cache fix.

### Step 2: NRR (Net Revenue Retention)
*   **Canonical Table:** `nexus-analyst-demo.acme.nrr_trailing_12`
*   **Logic (SIGNALS):** 
    *   The cohort is fixed: Paid (non-Free) customers as of `snapshot_date - 12 months`.
    *   **Crucial:** You must `LEFT JOIN` the end-of-period MRR and `COALESCE` to 0. 
    *   **Common Mistake:** If you `INNER JOIN`, you drop the churned customers and INFLATE the NRR. 
    *   Current Target: NRR ~1.07, GRR ~0.94.

### Step 3: New Bookings
*   **Canonical Table:** `nexus-analyst-demo.acme.bookings_attribution`
*   **Warning:** `bookings_acv_usd` is **ALREADY ANNUALIZED**. Do not multiply by 12. 
*   **Self-Serve Filter:** This table ONLY contains AE-led deals. Pro-to-Business self-serve conversions are tracked in `fact_subscriptions` only.

---

<a name="dw-conventions"></a>
## 🏗 Data Warehouse Conventions & Naming
**Status:** ✅ Active
**Owner:** Rajiv Menon / David Kim

### 1. The FLAT Rule
We use a single, flat dataset for all materialized marts. 
*   **CORRECT:** `nexus-analyst-demo.acme.account_health`
*   **WRONG:** `nexus-analyst-demo.acme.marts.cs.account_health`
*   **WRONG:** `nexus-analyst-demo.acme.finance.arr_snapshot`

BigQuery does not support nested folders within a dataset. The `marts/finance` or `marts/cs` folders you see in the `dbt` GitHub repo are for code organization only. 

### 2. Naming
*   Use `snake_case` for all table and column names.
*   Dimensions start with `dim_`.
*   Fact tables start with `fact_`.
*   Marts are descriptive (e.g., `arr_snapshot`, `nrr_trailing_12`).

### 3. Step-Level Data
We **DO NOT** store individual workflow step results in the BI warehouse (too much volume). We only store the `fact_workflow_runs` summary. If you need step-level debugging, go to the production `logs` cluster.

---

<a name="analyst-onboarding"></a>
## 🆕 New Analyst Onboarding (WIP)
**Status:** 🚧 In Progress
**Owner:** Nina Patel

- [x] Access to Google Cloud / BigQuery (`nexus-analyst-demo` project)
- [x] Access to Looker (Analyst role)
- [x] Access to dbt Cloud (Read-only for now)
- [x] Join #data-ops and #data-help in Slack
- [ ] Read the "NRR Cohort Logic" whitepaper (Ask Lina)
- [ ] Schedule 1:1 with Rajiv to discuss the DAG structure
- [ ] Install the "Acme Data" Chrome extension for Looker field definitions
- [ ] ~~Learn how to manually kick off the Fivetran sync~~ (deprecated - David owns this now)
- [ ] Complete the "BigQuery Costs" training (Don't run `SELECT *` on `fact_user_events`!!)

---

<a name="qbr-template"></a>
## 🤝 Quarterly Business Review (QBR) Template
**Status:** ✅ Active
**Owner:** Marco Silva

*For use by CSMs during customer reviews.*

### Section 1: Executive Summary
*   **Platform Adoption:** `active_users_28d` vs `seat_count_licensed`.
*   **Workflow Performance:** Success rate vs Error rates.

### Section 2: ROI Analysis
*   **Manual Hours Saved:** (runs * 0.25 hours).
*   **Top 3 Integrations:** (e.g., Salesforce -> Slack, Jira -> Github).

### Section 3: Roadmap Alignment
*   What’s next? (VRS, new connectors, etc.)

---

<a name="churn-debrief"></a>
## 📉 Churn Debrief Template
**Status:** ✅ Active
**Owner:** Elena Volkov

Every account >$50k ARR that churns requires a debrief.

### Case Example: Beacon Studios (cust_000287)
*   **Date:** 2026-02-18
*   **ARR Loss:** ~$116,000
*   **Health at Time of Churn:** `stable` / `healthy_expansion`.
*   **Reason:** This was **NOT** product dissatisfaction. Beacon Studios underwent a parent-company driven procurement consolidation. 
*   **Lessons Learned:** Even with high engagement (NPS was 9), we didn't have high-enough visibility into the parent company's IT roadmap.

---

<a name="looker-guidelines"></a>
## 📈 Looker Development Guidelines
**Status:** ⚠️ Stale / Update Needed
**Owner:** Nina Patel

*   **Caching:** Always use a 24-hour cache for the Executive Dashboard.
*   **The Jan Incident:** On Jan 12, 2026, a PDT failure caused the Executive Dashboard to show $42M ARR while the warehouse showed $39M. **Always** check the "last updated" tile.
*   **Dimensions:** Use the descriptions in LookML. If a field isn't documented, it doesn't exist.

---

<a name="support-triage"></a>
## 🎫 Support Ticket Triage Guide
**Status:** ✅ Active
**Owner:** Elena Volkov

| Priority | Definition | SLA (Response) |
|---|---|---|
| **P1** | Platform down / Data loss. | 1 Hour |
| **P2** | Business critical feature broken. | 4 Hours |
| **P3** | General inquiry / "How to". | 24 Hours |
| **P4** | Feature request. | No SLA |

*   **Escalation:** If a P1 is open for >48h, the account status automatically flips to `at_risk`.

---

<a name="marketing-attribution"></a>
## 📣 Marketing Attribution Methodology
**Status:** ✅ Active
**Owner:** Jasmine Park / Rajiv Menon

### 1. First-Touch Attribution
We use a "First Touch" model for the `bookings_attribution` table.
*   **Logic:** The very first UTM-tracked session in `fact_marketing_touches` for a lead that eventually converts to an Opportunity.
*   **Channels:** `organic`, `paid_search`, `outbound`, `content`, `referral`, `partner`, `event`, `inbound`.

### 2. AE-Led vs PLG
*   `bookings_attribution` only tracks **AE-led** deals (Business/Enterprise). 
*   **PLG (Pro)** conversions are tracked separately via `fact_user_events` as they are self-serve. 

---

<a name="security-incident"></a>
## 🔐 Security Review & Incident Response
**Status:** ✅ Active
**Owner:** Priya Anand

### Incident Response Playbook:
1.  **Identify:** Is this a data leak or a service outage?
2.  **Contain:** Rotate credentials in `Infisical` immediately.
3.  **Analyze:** Rajiv/David to query `fact_user_events` for unauthorized IP access patterns.
4.  **Recover:** Restore from Point-In-Time recovery if database was compromised.

---

<a name="vrs-parked"></a>
## ⏸ VRS Implementation Plan (ON HOLD / PARKED)
**Status:** 🛑 PARKED
**Owner:** Dan Lee

**The Value Realization Score (VRS)** project is currently on hold. 
*   **DO NOT** query `vrs_band` or `champion_login_recency`. 
*   These columns were defined in the spec but **NEVER BUILT** in the production dbt models. 
*   Use `account_health_status` as the shipped proxy for now.

---

<a name="on-call"></a>
## 📞 On-Call Rotation & Escalation
**Status:** ✅ Active
**Slack:** #on-call-data

### Current Rotation (Weekly):
*   **Week A:** Rajiv Menon (Analytics/dbt)
*   **Week B:** David Kim (Data Eng/Airflow)
*   **Week C:** Nina Patel (Looker/BI)

### Escalation Path:
1.  Primary On-Call
2.  Priya Anand (VP Eng)
3.  Sam Reyes (CEO) - *P0 Service Outage Only*

---

## 🗒 Miscellaneous Notes & Junk
*   *Lina:* "Hey Rajiv, I think the `dim_customers` signup_date is 1 day off for customers in APAC? Check the timezone conversion."
*   *Rajiv:* "Fixing it in the next dbt run."
*   *Elena:* "Can we get a table for `fact_customer_success_meetings`? We are tracking this in a spreadsheet right now and it's annoying." (TODO: add this to Q3 roadmap).
*   *Random Note:* Lunch on Thursday moved to the SF office patio.
*   *Broken Link:* [Internal Architecture Diagram - DEPRECATED](http://internal-wiki/arch-2024)

---
*End of Document Collection*
*(Generated for Acme Inc Internal Use Only)*