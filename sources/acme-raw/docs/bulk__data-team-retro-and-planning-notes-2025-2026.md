---
title: "Data team quarterly retro and planning notes — 2025-2026"
source_url: "internal://acme/data-team-retro-and-planning-notes-2025-2026"
license: "synthetic-demo"
attribution: "Synthetic content, Acme Inc internal demo. Acme Inc is a fictitious company."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: notion_runbook
---

# Data Team Quarterly Retro & Planning: 2025-2026 Strategic Roadmap

**Location:** #data-team-internal / Notion / SF Office - Room "The Big Query"
**Facilitator:** Rajiv Menon (Analytics Engineer, emp_012)
**Participants:** 
- David Kim (Data Engineer, emp_013)
- Nina Patel (Analytics Engineer, emp_014)
- Lina Cho (Finance/Data Analyst, emp_062)
- Dan Lee (VP Product, emp_050)
- Rachel Stein (CFO, emp_060) - *Joined for finance/NRR segments*

---

## 🧊 Q1 2025: Foundations & The "Left Join" War

### 🔙 Retro: What went well?
- **Standardization of `fact_subscriptions`**: We finally moved away from the old Google Sheet that Rachel used to keep under her desk. Everything is now flowing from Stripe into the BigQuery flat dataset at `nexus-analyst-demo.acme.fact_subscriptions`.
- **Daily Refresh Reliability**: David got the Airflow orchestration stabilized. BI warehouse is now lagging prod by ~2h consistently. 
- **Employee Dim**: `dim_employees` is actually accurate for the first time in history. Shoutout to Jorge Martinez (RevOps) for finally fixing the manager IDs.

### ❌ Retro: What didn't go well?
- **The NRR Inflation Scandal**: We realized half-way through the quarter that the "Board NRR" dashboard was using an INNER JOIN on the cohort table. This was dropping churned customers and making our NRR look like 125% when it’s actually ~1.07. Lina had to spend three nights re-writing `nrr_trailing_12` to use a LEFT JOIN + `COALESCE(end_mrr_usd, 0)`.
- **Looker Performance**: Everyone is complaining that the "Executive Overview" dashboard takes 4 minutes to load. It's the PDTs. It's always the PDTs.
- **Office Noise**: The SF office heating is broken again. We spent most of the February retro wearing parkas.

### 📊 Key Metrics Reviewed
- **ARR**: ~$32M. (Business tier is carrying us).
- **NRR**: Adjusted to **1.07** (Trailing 12).
- **GRR**: Calculated at **0.94** (Capping numerator at denominator to ensure we don't give credit for expansion on a retention metric).

### 🎯 Q2 Planning / OKRs
- **[OKR] Centralize dbt materializations**: Rajiv to ensure all marts are FLAT under `nexus-analyst-demo.acme`. No more nested datasets like `acme.marts.finance`. 
- **[VRS] Value Realization Score (Initial Brainstorm)**: Dan Lee wants a way to measure if a customer is "getting value" beyond just logging in.
- **Tooling**: Evaluate if we should stick with Looker or look at Sigma. Nina thinks Sigma's spreadsheet-like interface will stop the AEs from asking us for CSV exports.

---

## 🌻 Q2 2025: Scaling Pains & Series B Preparation

### 🔙 Retro: What went well?
- **Series B Due Diligence**: Rachel Stein was happy with the data cleanliness for the Series B pitch. The `arr_snapshot` table (our canonical source) held up under scrutiny. 
- **Flat Dataset Migration**: 80% of the way there. We successfully killed the `acme.dbt_marts` legacy schema. All analysts are now pointed to `nexus-analyst-demo.acme`.
- **Team Bonding**: The karaoke night in the Mission was great, although David’s rendition of "Bohemian Rhapsody" was... long.

### ❌ Retro: What didn't go well?
- **Snake_case Enforcement**: People are still naming columns `Total_Revenue` (Camel_Snake?) or `userID`. David is going to start rejecting PRs that don't follow the `user_id` snake_case convention.
- **VRS Scope Creep**: The Value Realization Score (VRS) discussion is spiraling. Sales wants it to include "Champion Sentiment," but we don't have that in the warehouse. 
- **Incident #2025-04**: Someone (who shall remain nameless, but it starts with 'R' and ends with 'ajiv') accidentally dropped the `fact_user_events` staging table in the middle of a Monday rush. 

### 📊 Key Metrics Reviewed
- **Total ARR**: Crossing $35M. Business tier growing at 12% QoQ.
- **Enterprise ARR**: Still hovering around $5M. We need the AEs (Tom Becker, Sarah Chen) to close more Enterprise deals like Marigold Health (cust_000701).
- **Wait Times**: Average BI ticket turnaround is 6 days. Too slow.

### 🎯 Q3 Planning / OKRs
- **[OKR] Finalize VRS Spec**: Define the `vrs_band` and `champion_login_recency` logic.
- **[Tooling] Looker vs. Sigma**: Start a formal PoC. Nina is lead on this.
- **[Cleanup] dbt Ownership**: Assign explicit owners for every model in the `schema.yml`.

---

## 🍂 Q3 2025: The VRS Specification Phase

### 🔙 Retro: What went well?
- **Sigma PoC**: The Marketing team loves it. Jasmine Park (VP Marketing) says she can actually build her own charts now.
- **Series B Closed**: $80M in the bank. We’re hiring! Need a new Senior AE and maybe another Data Engineer.
- **Success on `bookings_attribution`**: We finally aligned on the fact that `bookings_acv_usd` is ALREADY annualized. No more `* 12` errors in the AE commission reports.

### ❌ Retro: What didn't go well?
- **VRS Complexity**: We’ve spent 40 hours on the VRS spec and still don't have a table. The CS team (Elena Volkov) wants a 10-point scale, but the data is too noisy.
- **Warehouse Conventions**: We found a bunch of queries in the Wild West (random Looker SQL blocks) referencing `acme.marts.cs.account_health`. **Reminder: WRONG path.** Use `nexus-analyst-demo.acme.account_health`. 
- **Coffee Machine Incident**: The SF office espresso machine was down for 3 days. Morale plummeted to an all-time low.

### 📊 Key Metrics Reviewed
- **ARR**: ~$37M total. (Business: ~$30M, Enterprise: ~$6M, Pro: ~$1M).
- **Engagement (Old Metric)**: 65% of accounts active. (This feels too high/loose).
- **Customer Spotlight**: Onyx Robotics (cust_000704) is our new Enterprise darling. 500 seats. 

### 🎯 Q4 Planning / OKRs
- **[OKR] Engagement Recalibration**: We need a stricter definition of an "Engaged" customer. Currently, if one person logs in once, the account is "active." This is misleading.
- **[VRS] Parking decision**: VRS is getting pushed. We need to focus on the Engagement recalibration first. 
- **[Hiring]**: Open headcount for 1x Data Engineer. David needs help with the event pipeline.

---

## ❄️ Q4 2025: The Big Recalibration & VRS Deep Freeze

### 🔙 Retro: What went well?
- **Engagement Recalibration**: We did it. New definition: `≥3 active users AND ≥10 successful workflow runs in trailing 28 days`. This moved about 15% of "Active" accounts into the "Monitoring" status in `account_health`. It’s painful but honest.
- **Account Health Table**: `account_health_status` enum is now live: `critical / at_risk / monitoring / stable / healthy_expansion`. 
- **New Hire**: Nina Patel joined as Analytics Engineer (emp_014). She's already cleaning up the NPS models.

### ❌ Retro: What didn't go well?
- **VRS Parked**: Due to the Board's focus on "Product-Led Growth" and the engagement recalibration, the Value Realization Score (VRS) has been officially parked. `vrs_band` and `champion_login_recency` columns will remain NULL/unbuilt for now.
- **Kestrel Networks Churn**: cust_000708 (Kestrel Networks) churned in November due to budget cuts. We didn't see it coming in the data because their engagement was technically "stable" until the day they canceled.
- **Sigma Debate**: It's getting heated. Rajiv wants to stay with Looker/dbt because of the version control. Lina wants Sigma for the speed.

### 📊 Key Metrics Reviewed
- **ARR**: ~$39M. (Business ~$32M / Enterprise ~$6M / Pro ~$1M).
- **NRR**: 1.07. (Still consistent).
- **Health**: 12% of Enterprise accounts are `at_risk` (mostly due to open P1 tickets >48h).

### 🎯 Q1 2026 Planning / OKRs
- **[OKR] Churn Prediction**: Now that we have the new engagement metrics, can we build a model to predict churn?
- **[OKR] BQ Migration Final Polish**: Remove all access to legacy schemas by Feb 1st.
- **[Event] Data Team Offsite**: Proposed for Amsterdam office (EMEA team visit).

---

## 🧊 Q1 2026: The Churn Crisis & Looker Legacy

### 🔙 Retro: What went well?
- **Engagement Insights**: The new `is_engaged` flag is actually working. We caught three potential churns before they happened (except for Beacon Studios... see below).
- **Flat Dataset Hygiene**: David purged 400 unused tables from `nexus-analyst-demo.acme`. The warehouse is finally clean.
- **Team Spirits**: The Amsterdam offsite was a massive success. Stroopwafels > SF bagels.

### ❌ Retro: What didn't go well?
- **Beacon Studios (cust_000287) Churn**: This hurt. $116K ARR gone. The data showed they were healthy (engaged, good NPS), but it was a parent-company procurement decision. Nothing we could have predicted. 
- **VRS Still Parked**: Dan Lee keeps asking about it in Product meetings, but we haven't touched the spec. It's still in the "Draft" folder.
- **The "ARR $42M" Confusion**: Someone circulated a slide showing $42M ARR. It was a stale Looker cache. Real ARR is ~$39M. Please use `arr_snapshot`, folks!

### 📊 Key Metrics Reviewed
- **ARR**: ~$39M (Flat quarter-over-quarter due to Beacon Studios churn).
- **NRR**: Dipped slightly but stabilized at **1.07**.
- **Enterprise Status**: Marigold Health (cust_000701) and Onyx Robotics (cust_000704) are both in `healthy_expansion` status.

### 🎯 Q2 2026 Planning / OKRs
- **[OKR] Modernize `fact_support_tickets`**: Integrate with the new Zendesk API to get `resolution_time_hours` more accurately.
- **[Tooling]**: Decide on Sigma once and for all. Rachel (CFO) is looking at the contract costs.
- **[Refactor]**: `dim_customers` needs a refresh. The `industry` field is 20% "Other". 

---

## 🌸 Q2 2026: (Mid-Quarter Update / May 2026)

### 🔙 Retro: Current Progress
- **Warehouse Pathing**: We've started a bot that auto-corrects people in Slack when they mention `acme.marts`. It’s aggressive but necessary.
- **Sigma vs Looker**: We are likely going with a hybrid model for the next 12 months. Looker for core financial reporting (`arr_snapshot`), Sigma for self-serve discovery.
- **VRS Status**: Still parked. We've decided to stick with the `account_health` proxy for the rest of FY26.

### ❌ Retro: Current Issues
- **BI Lag**: David is noticing some drift in the `fact_workflow_runs` table. It’s lagging by 3.5 hours lately instead of 2. Looking into BigQuery slot contention.
- **Tamarind Group (cust_000706)**: They paused in January. We need to figure out how to represent "Paused" status in the NRR cohort without treating them as permanent churn.

### 📊 Current Snapshot (as of May 4, 2026)
- **Active Customers**: 745.
- **Total Users**: 24,000 provisioned (16,000 active).
- **ARR Snapshot**: Business ~$32M / Ent ~$6M / Pro ~$1M. Total ~$39M.
- **NRR**: 1.07.
- **GRR**: 0.94.

---

## 📋 Action Items Tracker (2025-2026)

| Action Item | Assigned To | Quarter Added | Status | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Fix `nrr_trailing_12` join logic | Lina Cho | Q1 2025 | ✅ Done | Switched Inner Join to Left Join. |
| Enforce snake_case in BQ | David Kim | Q2 2025 | 🏗️ Ongoing | It's a constant battle. |
| Build VRS `vrs_band` column | Rajiv Menon | Q2 2025 | ⛔ Parked | Parked Q4 2025; still parked Q1 2026. |
| Looker to Sigma Migration Plan | Nina Patel | Q3 2025 | 🏗️ Ongoing | Hybrid model chosen. |
| Standardize `account_health_status` | Rajiv Menon | Q4 2025 | ✅ Done | Enum: critical/at_risk/monitoring/stable/healthy_expansion. |
| Churn Prediction Model | Nina Patel | Q1 2026 | 🏗️ Ongoing | Waiting for more data on the new engagement metric. |
| Amsterdam Office Visit | Data Team | Q1 2026 | ✅ Done | Best offsite ever. |
| Fix SF office espresso machine | Office Manager | Q3 2025 | ✅ Done | Replaced with Jura Z10. |
| Migration of `acme.marts` to flat | David Kim | Q2 2025 | ✅ Done | `nexus-analyst-demo.acme` is now the gold standard. |

---

## 📝 Appendix: Warehouse Conventions (Reinforced Q2 2026)

**1. Flat Datasets Only**
- All production tables must reside in `nexus-analyst-demo.acme.<table>`.
- DO NOT create nested datasets (e.g., `acme.marts.finance.fact_invoices`). 
- Reason: Simplifies BigQuery IAM and Looker/Sigma connection strings.

**2. Naming Standards**
- All columns: `snake_case`.
- IDs: `<entity>_id` (e.g., `customer_id`, `user_id`).
- Timestamps: `<event>_at` or `<event>_date`.
- Currency: `<metric>_usd`.

**3. ARR Canonicalization**
- Never sum `dim_customers.current_mrr_usd`.
- ALWAYS use `fact_subscriptions` or the `arr_snapshot` mart for board-level reporting. `dim_customers` is for enrichment, not for finance truth.

**4. Engagement Definition**
- `is_engaged` = (28-day active users >= 3) AND (28-day successful runs >= 10).
- If an account is not engaged, health status defaults to 'monitoring' unless a detractor/P1 ticket is present.

---
*End of Document*