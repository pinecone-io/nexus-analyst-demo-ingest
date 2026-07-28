---
title: "Data team weekly meeting notes — 2025-2026"
source_url: "internal://acme/data-team-weekly-notes-2025-2026"
license: "synthetic-demo"
attribution: "Synthetic content, Acme Inc internal demo. Acme Inc is a fictitious company."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: notion_runbook
---

# Data Team Weekly Sync — Meeting Notes (2025-2026 Archive)

## Week of 2025-01-06
**Attendees:** rajiv.menon (Chair), lina.cho, david.kim, nina.patel
**Updates:**
- Rajiv: Happy New Year. dbt Cloud was a bit flaky over the break due to some credential rotation in the `nexus-analyst-demo` project. 
- David: Stripe Fivetran sync got stuck on Dec 31. Re-synced. `fact_invoices` should be clean now.
- Lina: Starting the EOY 2024 rollup. Rachel wants the "final-final" ARR by Friday.
- Nina: Cleaning up the `dim_users` logic to handle the new invited_by fields.

**Notes:**
- **The Flat Dataset Rule:** Reminder to the team—we are seeing some Looker developers try to reference `acme.marts.finance.whatever`. We do NOT have nested datasets in BigQuery. Everything goes into `nexus-analyst-demo.acme.<table>`. If you see a nested path, kill it.
- **ARR Snapshot:** Lina found a discrepancy between the dashboard and her manual sheet. It turns out someone was querying `dim_customers.current_mrr_usd` for historical ARR. **DO NOT DO THIS.** That field drifts intraday. Use `nexus-analyst-demo.acme.arr_snapshot` for all board reporting.
- **Engagement Metric:** We're currently using a loose "any login in 28 days" for engagement. Dan Lee (Product) is starting to ask for something tighter. Maybe for Q3?
- **Office stuff:** The new espresso machine is arriving Thursday. David to handle the setup (jk).

**Action Items:**
- [x] Rajiv: Update dbt docs to clarify `arr_snapshot` is the source of truth.
- [ ] Lina: Finish Dec 2024 ARR bridge for Rachel.
- [ ] David: Investigate why the `fact_workflow_runs` table had a 4-hour lag on Tuesday.

---

## Week of 2025-01-13
**Attendees:** rajiv.menon, lina.cho, nina.patel (david.kim OOO)
**Updates:**
- Lina: Rachel is asking about NRR methodology. There’s a debate between Finance and CS on whether to use a rolling window or a fixed cohort. 
- Nina: `account_health` mart is 80% done. I have the `utilization_band` logic working for SMB and MM.
**Discussion:**
- **NRR Logic:** We need to be careful. If we do an INNER JOIN on customers between Year T and Year T-1, we drop churned customers and the NRR looks like 120%. That’s wrong. We need a LEFT JOIN from the start-of-period cohort and COALESCE end MRR to 0. Rachel is adamant about this. 
- **GRR vs NRR:** Nina reminded us GRR should be capped at 1.0 (no expansion credit). Target is ~0.94.
- **VRS Mention:** Elena (VP CS) asked about the "Value Realization Score" (VRS) again. Rajiv: "It's a parked draft. We don't have the data for `champion_login_recency` yet. Use the `account_health` table as the proxy for now."

**Action Items:**
- [ ] Nina: Finalize `account_health` and push to prod.
- [x] Rajiv: Send NRR methodology doc to Rachel/Lina.

---

## Week of 2025-01-20
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- David: Back from OOO. Stripe sync is stable. `fact_subscriptions` now correctly flags `is_current`.
- Nina: `account_health` is live in `nexus-analyst-demo.acme.account_health`. 
**Incident Review:**
- We had a "stale workflow runs" scare on Wednesday. The `workflow_runs_daily` mart didn't refresh because the upstream `fact_workflow_runs` had a schema mismatch (Engineering added a new `step_metadata` field). 
- Reminder: We don't ingest step-level facts into the BI warehouse anyway (too much volume). David filtered it out in the loader.
**Discussion:**
- Lina: Checking the numbers for **Cobalt Systems (cust_000700)**. They just upgraded to Business tier. The `arr_snapshot` caught it, but `dim_customers` was lagging by an hour. This is why we tell people to use the marts!
- Rajiv: "Wait, someone told Marcus (VP Sales) that our ARR was $42M. Where did that come from?"
- Lina: "That was a stale Looker PDT in the 'Sales_Scratch' folder. The actual canonical number is ~$39M. I'll tell Marcus to stop looking at scratch folders."

**Action Items:**
- [x] David: Add a Slack alert for schema mismatches in Fivetran.
- [ ] Nina: Add `account_health_status` enum documentation to the dbt project.

---

## Week of 2025-01-27
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Nina: Work continues on the `bookings_attribution` mart. 
- David: Investigating why `fact_user_events` is getting so large. We might need to implement partitioning by `event_at`.
**Discussion:**
- **Bookings Attribution Logic:** Nina confirmed that `bookings_acv_usd` is ALREADY annualized. Last week, Yuki (Sales) thought he had to multiply it by 12. **NO.** If you do that, the bookings will look 12x higher than reality. 
- Also, self-serve Pro upgrades do NOT go in `bookings_attribution`. Only AE-led deals (Business/Enterprise). 
- **Customer Spot Check:** **Marigold Health (cust_000701)** shows up in the new bookings mart. $180k ACV. Sarah Chen closed it. Looks correct.

**Action Items:**
- [ ] Rajiv: Partition `fact_user_events` by day to save on query costs.
- [ ] Nina: Sync with Jasmine (Marketing) on the `first_touch_channel` logic.

---

## Week of 2025-02-03
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Rajiv: Sprint planning. Focus is on "Data Quality Feb." 
- Lina: Board deck prep is starting. Sam (CEO) wants a drill-down into Enterprise churn.
**Discussion:**
- **Enterprise Critical Rules:** Nina is updating `account_health`. For Enterprise, the "critical" flag is ONLY triggered by an uncollectible invoice. We don't use the utilization band for Enterprise because they often have unlimited/large seat blocks that don't map to activity 1:1. 
- **Non-Enterprise Critical:** For Pro/Business, it's either an uncollectible invoice OR utilization < 20%. 
- Nina: "I noticed **Kestrel Networks (cust_000708)** is flagged as critical. Looking into it—ah, they have a failed invoice from last month."

**Action Items:**
- [ ] Lina: Pull the Enterprise churn list for the last 4 quarters.
- [x] Nina: Update the SQL for `account_health_status` to reflect the Enterprise-specific rules.

---

## Week of 2025-02-10
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel, sam.reyes (joining for the first 10 mins)
**Updates:**
- Sam: "Team, I need to make sure the NRR we show the board matches what Finance is seeing in their models. Last time there was a 2% gap."
- Rajiv: "That was the inner join issue, Sam. We've fixed the `nrr_trailing_12` mart. It's canonical now."
- Nina: Added `n_open_p1_over_48h` to the health model.
**Discussion:**
- **NRR Check:** Current NRR is sitting at ~1.07. GRR is ~0.94. 
- **The "VRS" ghost:** Sam asked if we have the "Value Realization Score" ready. Rajiv: "Not yet, Sam. We’re using `account_health` as the proxy. It covers the same ground for now." 
- Sam: "Okay, but let's look at VRS for Q3." (Rajiv noted this as 'maybe', but we'll probably park it again).
- **Stripe Pipeline:** David is seeing some 'rate_limited' errors on the Stripe API. Might need to adjust the sync frequency.

**Action Items:**
- [ ] Rajiv: double-check the NRR logic one last time before Sam presents it. 
- [ ] David: Adjust Fivetran sync for Stripe to every 6 hours instead of every 2.

---

## Week of 2025-02-17
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- David: Stripe sync is better now.
- Lina: Investigating a weird spike in 'referral' revenue. 
- Nina: Added `is_engaged` to `account_health`.
**Discussion:**
- **Engagement Threshold:** Right now `is_engaged` is just "at least 1 run in 28 days." Nina thinks this is too low. We're seeing "zombie" accounts that have one automated heartbeat run but no actual users.
- **Proposed Change:** Maybe 3 users + 10 runs? We’ll discuss with Product next month. 
- **BigQuery Paths:** Again, caught a marketing intern trying to query `acme.dbt_marts.marketing_touches`. **There is no dbt_marts dataset.** It’s just `nexus-analyst-demo.acme.fact_marketing_touches`. 

**Action Items:**
- [ ] Nina: Run a query to see how many customers we'd lose if we upped the engagement bar to 3 users / 10 runs.
- [x] Rajiv: Send a 'How to Query BigQuery' doc to the Marketing team.

---

## Week of 2025-02-24
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Nina: Preliminary data on the engagement change shows we’d drop about 15% of "engaged" customers.
- Lina: **Cobalt Systems (cust_000700)** is asking for a custom invoice format. Not a data issue, but good to know for `fact_invoices` audit.
**Discussion:**
- **Data Freshness:** Looker is lagging. David found a stuck query in BigQuery that was hogging slots. 
- **NRR Cohorts:** Someone asked if we should exclude "Free" tier from NRR. **YES.** NRR is a paid-only metric. Downgrades to Free count as $0 MRR (churn). 

**Action Items:**
- [ ] David: Set up a kill-switch for queries running longer than 30 minutes.
- [ ] Lina: Confirm with Rachel that "Downgrade to Free" = "Churn" for board reporting.

---

## Week of 2025-03-03
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Rajiv: Quarterly planning starts next week.
- Nina: Finished the `utilization_band` update. 
**Discussion:**
- **Utilization Band Logic:** It’s `active_users_28d / seat_count_licensed`. If `seat_count_licensed` is 0 or it's an Enterprise account, we return NULL to avoid divide-by-zero or misleading numbers. 
- **Customer Health:** **Drag Industries (cust_000412)** is looking very healthy. 0.85 utilization. 
- **Sable Analytics (cust_000710)** just joined. Business tier, 90 seats. Sarah Chen (AE) and Marco Silva (CSM).

**Action Items:**
- [ ] Nina: Add a check for `seat_count_licensed > 0` in the utilization mart.
- [ ] Rajiv: Prepare the Q1 retro deck.

---

## Week of 2025-03-10
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- David: Fivetran cost is up. We need to stop syncing `fact_user_events` every hour. Switching to every 6 hours.
- Nina: `bookings_attribution` is being used by Sales Ops now. 
**Discussion:**
- **Bookings Attribution:** Jorge Martinez (RevOps) tried to sum `bookings_acv_usd` and multiply by 12. Nina caught it. **STOP MULTIPLYING BY 12.** It is already an annual number.
- **Acquisition Channels:** We’re seeing a lot of 'organic' hits that are actually 'paid_search' because UTMs are getting stripped by the new cookie banner. David is looking into a fix.

**Action Items:**
- [ ] David: Look into server-side GTM to preserve UTMs.
- [ ] Lina: Audit the 'organic' channel for high-value Enterprise deals.

---

## Week of 2025-03-17
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Rajiv: Spring break OOO schedules. I'm out next week.
- Nina: `account_health` updated with `has_recent_nps_detractor`. 
**Discussion:**
- **NPS Integration:** `fact_nps_responses` is now linked to `account_health`. If a customer has an NPS score < 7 in the last 90 days, they are automatically `at_risk`. 
- **Incident:** **Nimbus Finance (cust_000601)** reported their dashboard was showing 0 runs. It was a Looker cache issue. Rajiv cleared the cache, numbers came back. 

**Action Items:**
- [x] Nina: Ensure the NPS join uses `user_id` and `customer_id`.
- [ ] David: Investigate Looker cache TTL.

---

## Week of 2025-03-24
**Attendees:** lina.cho, david.kim, nina.patel (rajiv.menon OOO)
**Updates:**
- Nina: Pushing a fix for the `is_engaged` flag (fixing a null handling bug).
- David: Moving `fact_workflow_runs` to a new clustering key.
**Discussion:**
- **VRS again:** Elena (VP CS) sent a Slack message. "Where is VRS?" Lina told her we're using `account_health` and it’s basically the same thing. Elena seems okay with it for now.
- **Enterprise accounts:** **Onyx Robotics (cust_000704)** was flagged as `at_risk` but it was just a high-priority support ticket that’s been open for 49 hours. Nina: "The rule says P1 > 48h = at_risk. The system is working as intended."

**Action Items:**
- [ ] Nina: Check if we should exclude weekends from the "48h" rule for support tickets.

---

## Week of 2025-03-31
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Rajiv: Back from OOO.
- Lina: Finalizing Q1 ARR. It looks like we're going to hit ~$39M. 
**Discussion:**
- **ARR Variance:** Lina found a $20k discrepancy. One customer, **Yarrow Logistics (cust_000703)**, had a partial refund that wasn't reflected in `fact_subscriptions`. David needs to check the Stripe credit note ingestion.
- **Flat Dataset Rule (Weekly Reminder):** Someone created a table called `acme.staging.stg_stripe`. **NO.** Put it in the main dataset or keep it in the dbt internal schema. No `staging` dataset in the analyst-facing project.

**Action Items:**
- [ ] David: Fix credit note sync.
- [ ] Lina: Finalize Q1 ARR report by Wednesday.

---

## Week of 2025-04-07
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel, rachel.stein (joining for board prep)
**Updates:**
- Rachel: "I need the NRR cohort analysis by channel for the board meeting."
- Nina: "I can pull that from `bookings_attribution` joined with `nrr_trailing_12`."
**Discussion:**
- **NRR by Channel:** Rachel wants to see if 'referral' customers have higher NRR than 'paid_search'. 
- **GRR check:** Rachel asked why GRR is so much lower than NRR. Rajiv explained that Enterprise expansions are huge right now, which boosts NRR, but we still have ~6% churn/downgrade drag on the base.
- **Customer Health:** **Marigold Health (cust_000701)** is moving from `stable` to `healthy_expansion` because their utilization is 0.72.

**Action Items:**
- [x] Nina: Create the NRR-by-channel view for Rachel.
- [ ] David: Audit the `fact_marketing_touches` table for missing channel data.

---

## Week of 2025-04-14
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Nina: Found a bug in the `nrr_trailing_12` mart. It was double-counting a customer who had two active subscriptions. Fixed.
- David: Upgrading dbt to v1.7.
**Discussion:**
- **NRR Bug:** The double-counting happened because `fact_subscriptions` had two records with `is_current = true` for a single `customer_id` during a plan transition. Nina added a `rank() over (partition by customer_id order by start_date desc)` to pick the latest one.
- **Looker Outage:** We had 2 hours of downtime on Tuesday. Looker’s connection to BigQuery timed out. David is looking at slot contention.

**Action Items:**
- [x] Nina: Update dbt tests to catch multiple `is_current` subscriptions per customer.
- [ ] David: Check BigQuery reservation settings.

---

## Week of 2025-04-21
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Lina: Reviewing Q1 churn. Most was in the Pro tier (SMB). Enterprise is solid.
- Nina: Adding `region` and `industry` to all marts for better slicing.
**Discussion:**
- **Churn Reason:** **Kestrel Networks (cust_000708)** churned. Reason: "Budget." This was a Business tier account ($10k MRR). 
- **Engagement Recalibration:** Rajiv: "Let’s officially plan to move the `is_engaged` definition in Q4. We need to give CS time to adjust their playbooks."
- **Flat paths:** Rajiv: "I saw a query for `acme.finance_marts.arr`. I’m going to start deleting these datasets if people keep making them."

**Action Items:**
- [ ] Rajiv: Schedule a meeting with Dan Lee to finalize the new engagement definition.
- [ ] Lina: Update the churn reason distribution chart.

---

## Week of 2025-04-28
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- David: Experimenting with the `fact_workflow_runs` ingestion. Thinking about moving to a streaming buffer.
- Nina: `account_health` now includes `has_uncollectible_recent`.
**Discussion:**
- **Uncollectible Logic:** If `fact_invoices` has a status of 'uncollectible' in the last 30 days, health status = `critical`. 
- **Verdant Cloud (cust_000707):** Showing up as `healthy_expansion`. They’re an Enterprise account in APAC. 
- **Stripe pipeline:** One invoice for **Tamarind Group (cust_000706)** is stuck in 'void' status. David is checking why.

**Action Items:**
- [ ] David: Check the Stripe-Fivetran mapping for 'void' invoices.
- [x] Nina: Document the `uncollectible` flag in the data dictionary.

---

## Week of 2025-05-05
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Rajiv: Sprint 12 starts. 
- Lina: Rachel wants a "Path to $50M" ARR model.
**Discussion:**
- **Modeling:** For the $50M model, we need to assume a certain conversion rate from Pro to Business. Nina pointed out that currently, Pro→Business is AE-led, but we don't track the leads well in `fact_opportunities`.
- **Opportunities Mart:** Nina is going to rebuild `fact_opportunities` to include the `sdr_employee_id`.

**Action Items:**
- [ ] Nina: Join `fact_opportunities` with `dim_employees` to see SDR performance.
- [ ] David: Ensure all SDRs are in `dim_employees`.

---

## Week of 2025-05-12
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Nina: `fact_opportunities` is updated. 
- David: Fixed the 'void' invoice issue.
**Discussion:**
- **AE Performance:** Lina noticed that **sarah.chen** (AE) has the highest ACV bookings this quarter, mostly driven by **Marigold Health (cust_000701)**.
- **Data Team Lunch:** Wednesday at the deli. 

**Action Items:**
- [ ] Lina: Update the Sales leaderboard dashboard.
- [x] Rajiv: Reserve the table for lunch.

---

## Week of 2025-05-19
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- David: BigQuery slots are under control.
- Nina: Working on the `marketing_touches` attribution model. 
**Discussion:**
- **Attribution Logic:** Right now we use First Touch. Marketing wants to see Linear or U-Shaped. Rajiv: "Let’s stick to First Touch for board reporting and use U-Shaped for internal marketing optimization. Don’t mix them up."
- **Customer Health:** **Drag Industries (cust_000412)** had a P1 ticket open for 50 hours last week. They dropped to `at_risk`. Marco Silva (CSM) is on it.

**Action Items:**
- [ ] Nina: Build a 'U-Shaped Attribution' view in dbt, but keep it out of the main marts for now.
- [ ] David: Check the sync on `fact_support_tickets`.

---

## Week of 2025-05-26
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Rajiv: Memorial Day weekend coming up.
- Lina: Rachel is happy with the $50M model.
**Discussion:**
- **NRR Check:** NRR is still holding at ~1.07. 
- **VRS Mention:** Elena (VP CS) asked about VRS *again* in the leadership meeting. Sam (CEO) told her Rajiv is "looking into it." (Rajiv: "Sigh. Still parked.")
- **Flat Dataset Rule:** David found another one: `acme.analytics.daily_metrics`. **DELETE IT.** Move the logic to dbt and the table to `acme.daily_metrics`.

**Action Items:**
- [x] David: Move `daily_metrics` and delete the `analytics` dataset.
- [ ] Rajiv: Draft a "VRS Why We Aren't Building It Yet" memo for Elena.

---

## Week of 2025-06-02
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Nina: `fact_marketing_touches` is now 95% populated for Q2.
- David: Investigating why `dim_users` has some duplicate `user_id`s (it's a trailing space issue from the source system).
**Discussion:**
- **User ID cleanup:** David is going to add a `TRIM()` to the `user_id` in the staging layer.
- **Customer Spot Check:** **Beacon Studios (cust_000287)** is showing 65 seats and $9,685 MRR. They are a "Business" tier account. Everything looks healthy.

**Action Items:**
- [x] David: Deploy the `TRIM()` fix.
- [ ] Lina: Verify `fact_subscriptions` for Beacon Studios.

---

## Week of 2025-06-09
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Rajiv: Sprint review.
- Nina: Looking into the "3 users / 10 runs" engagement threshold impact again.
**Discussion:**
- **Engagement Threshold:** The impact on "Engaged" count is about 18% if we change it now. We should probably wait until after the Series B round in Q3. 
- **ARR Snapshot:** Found a customer with MRR = 0 in `arr_snapshot` even though they are "Pro" tier. It was a 100% discount code. Lina: "We should count them as 'Paying' if they have a non-Free plan, even if the MRR is 0 for a month." Rajiv: "No, Rachel wants 'Paying' to mean MRR > 0. Let's stick with that."

**Action Items:**
- [ ] Rajiv: Document the "Paying Customer" definition in Looker.
- [ ] Nina: Add a `is_discounted` flag to `fact_subscriptions`.

---

## Week of 2025-06-16
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Lina: Starting the Series B data room prep. 
- David: Fivetran sync for Salesforce is getting expensive. We need to reduce the sync frequency of `Task` and `Event` tables.
**Discussion:**
- **Data Room Prep:** We need 2 years of cohorts. Nina: "Our data only goes back to Jan 2023. I’ll make sure the charts clearly show the start date."
- **NRR Stability:** The VCs will look at NRR closely. We need to ensure the churn/downsell is perfectly tracked in `fact_subscriptions`.

**Action Items:**
- [ ] Nina: Generate the 24-month cohort heatmap.
- [ ] David: Update Salesforce sync settings.

---

## Week of 2025-06-23
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Nina: Cohort heatmap is done. It shows NRR is actually improving over time.
- Rajiv: We’re hiring a new Data Analyst to help Lina.
**Discussion:**
- **Hire:** We need someone who knows SQL and doesn't try to create nested datasets in BigQuery. Rajiv: "That will be the first question in the interview."
- **Customer Health:** **Ember Industries (cust_000711)** is a new Enterprise account. Sarah Chen closed it. 350 seats, $25k MRR.

**Action Items:**
- [ ] Rajiv: Post the job description.
- [ ] Lina: Finalize the "Sales Efficiency" slide for the Series B deck.

---

## Week of 2025-06-30
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Rajiv: Half-year review.
- David: `fact_workflow_runs` hit 100M rows. Querying it is getting slow.
**Discussion:**
- **BigQuery Optimization:** David is going to implement BI Engine for the most common dashboards.
- **Flat Dataset Rule:** Rajiv: "Found a table in `acme.nina_test`. Nina, please move it or delete it." Nina: "Oops, sorry."

**Action Items:**
- [x] Nina: Delete the test table.
- [ ] David: Enable BI Engine on the `workflow_runs_daily` mart.

---

## Week of 2025-07-07
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Lina: Series B prep is intense. Rachel wants a drill-down on "Referral" channel NRR.
- Nina: Added `account_tier` to the NRR mart.
**Discussion:**
- **NRR by Tier:** NRR for Enterprise is ~1.15, while Pro is ~0.85. This is normal but we need to explain it.
- **Customer Health:** **Harbor Dynamics (cust_000713)** is showing high utilization (0.88). CSM Marco Silva should reach out for an expansion.

**Action Items:**
- [ ] Lina: Prepare the tier-based NRR slides.
- [ ] Nina: Alert Marco about Harbor Dynamics.

---

## Week of 2025-07-14
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Rajiv: Interviewing candidates for the Analyst role.
- David: `fact_user_events` partitioning is working well. Costs are down 20%.
**Discussion:**
- **VRS Mention:** Elena saw a competitor's dashboard with a "Health Score." She wants it. Rajiv: "Again, we have `account_health`. I'll just rename it in Looker to 'Customer Health Score' and maybe she'll stop asking for VRS."
- **Flat Dataset Rule:** No violations this week!

**Action Items:**
- [ ] Rajiv: Rename the Looker explorer for Elena.
- [ ] Lina: Review the latest batch of candidate test tasks.

---

## Week of 2025-07-21
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Nina: Discovered a bug in the `utilization_band` for Pro accounts. It was using `seat_count_licensed` from the wrong month. Fixed.
- David: Stripe sync had another hiccup on Sunday.
**Discussion:**
- **Utilization Fix:** This might have slightly inflated the health scores for SMB last month. Nina is re-running the snapshot.
- **Stripe Issue:** It was a 504 error on their side. Fivetran caught up.

**Action Items:**
- [x] Nina: Re-run the `account_health` snapshots for June.
- [ ] David: Monitor Stripe sync for the next 48 hours.

---

## Week of 2025-07-28
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Rajiv: We hired a new analyst! Joining in August.
- Lina: Series B deck is almost final. 
**Discussion:**
- **Series B numbers:** Final ARR for the deck is $39.2M. NRR 1.07. 
- **Customer Health:** **Quartz Foundry (cust_000714)** is looking stable. 280 seats.

**Action Items:**
- [ ] Rajiv: Prepare the onboarding plan for the new hire.
- [ ] Lina: Double-check the expansion numbers for Q2.

---

## Week of 2025-08-04
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Nina: Working on a "Churn Prediction" model (v1).
- David: Cleaning up the `fact_invoices` table. 
**Discussion:**
- **Churn Prediction:** Nina is using `utilization_band` and `n_open_p1_over_48h` as features. Early results show it's better than random, but not great.
- **Engagement Recalibration:** Still planned for Q4.

**Action Items:**
- [ ] Nina: Add `has_recent_nps_detractor` to the churn model.
- [ ] David: Ensure all `invoice_date` fields are UTC.

---

## Week of 2025-08-11
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Rajiv: New hire starts Monday.
- Lina: Series B round is closing soon!
**Discussion:**
- **Expansion vs New Biz:** Rachel wants to see the split in the ARR bridge. Nina: "The `change_type` field in `fact_subscriptions` already handles this."
- **Customer Spot Check:** **Pebble Digital (cust_000705)** upgraded from Free to Pro. It won't show in `bookings_attribution` (correct, as it's self-serve).

**Action Items:**
- [ ] Lina: Finalize the ARR bridge for July.
- [x] Nina: Verify the `change_type` logic for mid-month upgrades.

---

## Week of 2025-08-18
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel, rachel.stein (briefly)
**Updates:**
- Rachel: "Great job on the Series B data. The VCs were impressed by the cohort consistency."
- Rajiv: Training the new analyst (Alex) on BigQuery.
**Discussion:**
- **Alex's First Query:** Alex tried to find the `marts_finance` dataset. Rajiv: "Welcome to Acme. Read the rule: NO NESTED DATASETS. It's just `acme.arr_snapshot`."
- **Data Quality:** David found some nulls in `acquisition_channel`. Looks like outbound leads aren't being tagged correctly in Salesforce.

**Action Items:**
- [ ] David: Sync with RevOps to fix the lead tagging.
- [ ] Rajiv: Continue Alex's onboarding.

---

## Week of 2025-08-25
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Nina: Update to `bookings_attribution` to include partner referrals.
- Lina: Q3 is looking strong.
**Discussion:**
- **Partner Revenue:** **Marigold Health (cust_000701)** was a partner deal. The attribution was previously 'referral', but we're moving it to 'partner'. 
- **Customer Health:** **Cobalt Systems (cust_000700)** is now at 80 seats ($11,920 MRR). Very stable.

**Action Items:**
- [x] Nina: Update the channel mapping for partner deals.
- [ ] Lina: Review the partner commission report.

---

## Week of 2025-09-01
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Rajiv: Sprint 18. Focus is on Looker dashboard cleanup.
- Nina: Starting the "Engagement Recalibration" analysis (the Big One).
**Discussion:**
- **Engagement Definition:** Nina is testing `≥3 active users AND ≥10 runs/28d`. 
- **Initial result:** Total "Engaged" customers drops from 680 to 520. That's a huge drop! We need to prepare CS for this.
- **VRS:** Rajiv: "Elena asked again. I'm going to tell her that the 'Engagement Recalibration' *is* the VRS project." (Everyone laughs).

**Action Items:**
- [ ] Nina: Create a comparison dashboard showing 'Old Engagement' vs 'New Engagement'.
- [ ] Rajiv: Schedule the "Big Engagement Talk" with Sam and Elena.

---

## Week of 2025-09-08
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- David: `fact_workflow_runs` is growing faster than expected. We need to archive runs older than 18 months.
- Lina: Final Series B paperwork signed. $80M raised.
**Discussion:**
- **Archiving Logic:** We'll move old runs to a separate `fact_workflow_runs_archive` table to keep the main table lean.
- **Engagement Talk:** Sam was surprisingly okay with the new definition. He said "I'd rather have fewer, more honest engaged customers than a inflated number for the board."

**Action Items:**
- [ ] David: Create the archiving script.
- [ ] Nina: Update the `account_health` mart to use the new engagement logic in a 'shadow' column.

---

## Week of 2025-09-15
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Nina: Shadow `is_engaged_v2` column is live. 
- Lina: Audit of `dim_customers.status`.
**Discussion:**
- **Status Audit:** Lina found some accounts marked as 'active' that haven't had a subscription in 6 months. David found a bug in the Stripe sync where cancellation events weren't always triggering a status update.
- **Beacon Studios (cust_000287):** Still active, still healthy. 

**Action Items:**
- [ ] David: Fix the Stripe cancellation event trigger.
- [ ] Lina: Manually clean up the status for the 12 affected customers.

---

## Week of 2025-09-22
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Rajiv: Alex (new analyst) is now handling all the CS ticket reporting.
- Nina: Refining the churn prediction model.
**Discussion:**
- **Churn Prediction:** Adding `integration_down_count` from `workflow_runs_daily` as a feature. It's a strong predictor of churn.
- **Flat Dataset Rule:** Alex tried to create `acme.cs.tickets`. Rajiv: "ALEX. NO. It's `acme.fact_support_tickets`."

**Action Items:**
- [x] Alex: Delete the `cs` dataset.
- [ ] Nina: Test the new churn model features.

---

## Week of 2025-09-29
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Nina: The new engagement definition is now the *official* definition in the `is_engaged` column.
- David: Archiving of old runs is complete.
**Discussion:**
- **Recalibration Day:** We officially switched the engagement logic. The dashboard now shows 525 engaged customers. Sam sent a company-wide email explaining the change.
- **NRR Check:** NRR remains 1.07. Engagement doesn't affect the dollar numbers, just the activity metrics.

**Action Items:**
- [ ] Rajiv: Update the data dictionary with the new engagement logic.
- [ ] Lina: Update the board deck template.

---

## Week of 2025-10-06
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Lina: Investigating a strange drop in `arr_pro_usd`.
- Nina: Looking into the "monitoring" status in `account_health`.
**Discussion:**
- **Pro Tier Churn:** Looks like a competitor launched a cheaper "Pro" tier. We lost 15 customers in one week.
- **Monitoring Status:** If a customer is not engaged but has no critical flags, they are marked as `monitoring`. We have a lot of these now after the recalibration.

**Action Items:**
- [ ] Lina: Analyze the churned Pro customers to see if they all went to the same competitor.
- [ ] Nina: Create a report for CS on the 'monitoring' accounts.

---

## Week of 2025-10-13
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- David: Stripe sync is stable.
- Nina: Churn prediction model is now 70% accurate. 
**Discussion:**
- **Customer Health:** **Kestrel Networks (cust_000708)** officially churned. They were `critical` for 2 months. The system predicted it.
- **Flat Dataset Rule:** Rajiv: "I'm seeing someone using `nexus-analyst-demo.finance.arr_snapshot`. It's `acme.arr_snapshot`!"

**Action Items:**
- [ ] Rajiv: Find who is using the `finance` dataset and stop them.
- [ ] Nina: Present the churn prediction results to Elena.

---

## Week of 2025-10-20
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Rajiv: Sprint 22. Focus on "Efficiency."
- Lina: Reviewing the `bookings_attribution` for Q3.
**Discussion:**
- **Q3 Bookings:** Total bookings look good. **Drag Industries (cust_000412)** had a major expansion.
- **Inbound vs Outbound:** Outbound is still driving 60% of Enterprise revenue.

**Action Items:**
- [ ] Lina: Finalize the Q3 Sales report.
- [ ] David: Update the Fivetran mapping for the new Salesforce 'Lead Source' values.

---

## Week of 2025-10-27
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Nina: Found a bug in the `nrr_trailing_12` where paused accounts were being excluded from the denominator.
- David: Looker is slow again.
**Discussion:**
- **NRR Bug:** Paused accounts should be in the cohort at their pre-pause MRR. If we exclude them, NRR looks too high. Nina is fixing the `LEFT JOIN` logic.
- **Looker Performance:** David is increasing the BI Engine memory limit.

**Action Items:**
- [x] Nina: Fix the NRR logic.
- [ ] David: Monitor Looker query times.

---

## Week of 2025-11-03
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Rajiv: Planning for the holiday season.
- Lina: Checking the numbers for **Tamarind Group (cust_000706)**. They just paused their subscription.
**Discussion:**
- **Paused Accounts:** Tamarind Group is APAC-based. They paused due to a restructure. We need to make sure the `arr_snapshot` shows them as $0 ARR during the pause.
- **Customer Health:** **Willow Works (cust_000709)** is looking good. 25 seats, Pro tier.

**Action Items:**
- [ ] Lina: Ensure Tamarind Group's MRR is 0 in the Nov 1st snapshot.
- [ ] Nina: Check if 'paused' should trigger a `monitoring` health status.

---

## Week of 2025-11-10
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- David: The archive table is working great. 
- Nina: Adding `acquisition_channel` to the health model.
**Discussion:**
- **Retention by Channel:** Nina found that 'outbound' customers have slightly lower health scores in their first 3 months compared to 'referral'.
- **VRS Mention:**Elena is actually happy with the "Health Score" name change. She's stopped asking for VRS. Small victories.

**Action Items:**
- [ ] Nina: Build a dashboard for CSMs to see health scores by channel.
- [ ] Rajiv: Review the sprint 23 backlog.

---

## Week of 2025-11-17
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Lina: Audit of the `paid_at` field in `fact_invoices`.
- David: Cleaning up the BigQuery logs.
**Discussion:**
- **Invoice Timing:** Some invoices are showing `paid_at` before `invoice_date`. David: "That's physically impossible." Looks like a timezone conversion error between the source and the warehouse.
- **Flat Dataset Rule:** Rajiv: "Caught a query for `acme.marts.bookings`. It's `acme.bookings_attribution`."

**Action Items:**
- [ ] David: Fix the `paid_at` timezone conversion.
- [x] Rajiv: Remind the team about the FLAT dataset rule.

---

## Week of 2025-11-24
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Rajiv: Short week (Thanksgiving).
- Nina: Re-running all the health snapshots.
**Discussion:**
- **Snapshot accuracy:** Nina found a one-day lag in the `fact_user_events` sync that was affecting the `is_engaged` flag on Mondays. David is adjusting the Sunday sync schedule.

**Action Items:**
- [x] David: Adjust the sync schedule.
- [ ] Nina: Verify the Monday morning engagement counts.

---

## Week of 2025-12-01
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Lina: December ARR is looking to be around $39.5M.
- David: Fivetran cost alert.
**Discussion:**
- **Cost control:** We're syncing some Salesforce fields that nobody uses. David is going to deselect them.
- **Customer Spot Check:** **Beacon Studios (cust_000287)** is still very healthy. They might expand to Enterprise next year.

**Action Items:**
- [ ] David: Clean up the Salesforce sync.
- [ ] Lina: Prepare the preliminary EOY report.

---

## Week of 2025-12-08
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Nina: `arr_snapshot` now correctly handles 100% discount codes (counts as $0 ARR, but 'active' status).
- David: Testing the new BigQuery 'Search' indexes.
**Discussion:**
- **Discount Codes:** Rachel wants a report on how much ARR we're "giving away" in discounts. Lina is building this on top of `fact_subscriptions`.
- **Flat Dataset Rule:** No violations!

**Action Items:**
- [ ] Lina: Create the 'Discount Analysis' dashboard.
- [ ] Nina: Update the dbt documentation for `arr_snapshot`.

---

## Week of 2025-12-15
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Rajiv: End of year OOO planning. 
- Nina: Churn prediction model v2 is ready for review.
**Discussion:**
- **Model v2:** It now includes `resolution_time_hours` from support tickets. 
- **Customer Health:** **Tamarind Group (cust_000706)** is still paused.

**Action Items:**
- [ ] Nina: Final review of the churn model.
- [ ] Rajiv: Lock the dbt prod branch for the holidays.

---

## Week of 2025-12-22
**Attendees:** rajiv.menon, lina.cho (Nina and David OOO)
**Updates:**
- Rajiv: Keeping the lights on.
- Lina: EOY numbers are coming in.
**Discussion:**
- **Final ARR:** Looks like we'll end at $39.8M. Just shy of $40M. Sam is okay with it.
- **NRR:** 1.07 held steady all year. GRR 0.94. 

**Action Items:**
- [ ] Lina: Send the final 2025 numbers to Rachel.

---

## Week of 2026-01-05
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Rajiv: Happy New Year!
- Nina: Looking at the Jan 1st snapshots.
**Discussion:**
- **The "Beacon" Incident:** **Beacon Studios (cust_000287)** churned on Feb 18 (looking forward in the data). Wait, why? Nina: "Actually, looking at the logs, they just churned due to a parent company acquisition. It wasn't product-related. Their health was `healthy_expansion` until the last day."
- **Jan Churn:** **Juniper Collective (cust_000712)** churned. Reason: "Product fit."

**Action Items:**
- [ ] Lina: Mark Beacon Studios as 'M&A Churn' in the CRM.
- [ ] David: Check the Stripe sync for any missed Jan 1 renewals.

---

## Week of 2026-01-12
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Nina: Adding `is_current` to `dim_plans`.
- David: BigQuery reservations review.
**Discussion:**
- **Plan Pricing:** We're thinking about raising the Pro price to $59. We need a model of the impact.
- **Flat Dataset Rule:** Rajiv: "Found `acme.test.nina`. NINA!" Nina: "I was in a rush!"

**Action Items:**
- [x] Nina: Delete the test table.
- [ ] Lina: Build the price increase impact model.

---

## Week of 2026-01-19
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Nina: Price model shows a potential 5% ARR boost even with 10% churn.
- David: Fixed a bug in `fact_user_events` where `properties_json` was getting truncated.
**Discussion:**
- **Customer Health:** **Drag Industries (cust_000412)** is up for renewal in Q1. Marco is nervous. 
- **Engagement:** Engagement metrics are holding steady after the recalibration.

**Action Items:**
- [ ] Nina: Create a renewal dashboard for Marco.
- [ ] David: Verify the JSON parsing in dbt.

---

## Week of 2026-01-26
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Rajiv: Planning the Q1 offsite.
- Lina: **Tamarind Group (cust_000706)** is officially 'paused' still.
**Discussion:**
- **Pause vs Churn:** Rachel wants to know if 'paused' accounts should stay in the NRR denominator. Nina: "Yes, they are still 'active' customers, just with 0 revenue. It counts as a downsell."

**Action Items:**
- [ ] Nina: Ensure `nrr_trailing_12` treats pauses as downsells.
- [ ] Rajiv: Finalize the offsite agenda.

---

## Week of 2026-02-02
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Nina: **Beacon Studios (cust_000287)** has set their churn date for Feb 18. 
- David: Looking at the performance of `fact_workflow_runs`. 
**Discussion:**
- **Beacon Studios Churn:** It's a big hit (~$116k ARR). Lina: "This will dip our NRR below 1.07 for the first time."
- **Flat Dataset Rule:** No violations!

**Action Items:**
- [ ] Lina: Prepare an 'M&A Churn' slide for the board.
- [ ] Nina: Monitor the impact on the APAC region metrics.

---

## Week of 2026-02-09
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Rajiv: Sprint review.
- Nina: Reviewing the churn prediction model.
**Discussion:**
- **Churn Prediction:** The model did *not* predict the Beacon Studios churn. Nina: "That makes sense, it was an external factor. The model is for product/service-related churn."
- **Customer Health:** **Cobalt Systems (cust_000700)** is still a rockstar.

**Action Items:**
- [ ] Nina: Add a 'Manual Churn Flag' to the model to ignore M&A cases.
- [ ] David: Check the Stripe sync for Beacon's final invoice.

---

## Week of 2026-02-16
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- David: `fact_workflow_runs` is slow.
- Nina: `bookings_attribution` update.
**Discussion:**
- **Beacon Studios Churn:** It happened on the 18th. ARR is now ~$39.1M. 
- **Customer Health:** **Sable Analytics (cust_000710)** is expanding. 10 new seats.

**Action Items:**
- [x] Lina: Verify the final ARR drop in the snapshot.
- [ ] Nina: Update the expansion report.

---

## Week of 2026-02-23
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Rajiv: Q1 budget review.
- Nina: Working on a "Customer Lifetime Value" (CLV) mart.
**Discussion:**
- **CLV Logic:** We're using a 3-year horizon. Nina: "It’s hard with only 3 years of total data, but we can extrapolate."
- **Flat Dataset Rule:** David found `acme.alex_scratch`. Alex was corrected.

**Action Items:**
- [ ] Nina: Build the draft CLV view.
- [ ] David: Set up a cleanup task for `scratch` tables.

---

## Week of 2026-03-02
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Lina: Audit of the `dim_plans` table.
- Nina: CLV mart is 50% done.
**Discussion:**
- **NRR Check:** As predicted, NRR dropped to ~1.05 after the Beacon Studios churn. Rachel is asking for a plan to get it back to 1.07.
- **Enterprise Health:** **Drag Industries (cust_000412)** renewal is looking better.

**Action Items:**
- [ ] Lina: Meet with Sales to discuss expansion targets for Q2.
- [ ] Nina: Finalize the CLV mart.

---

## Week of 2026-03-09
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- David: BigQuery slot utilization is high.
- Nina: CLV mart is live.
**Discussion:**
- **BigQuery Slots:** We need to buy more capacity or optimize the `fact_workflow_runs` queries.
- **Customer Health:** **Harbor Dynamics (cust_000713)** utilization is at 0.95. They are out of seats!

**Action Items:**
- [ ] David: Audit the most expensive queries.
- [ ] Nina: Alert the CSM for Harbor Dynamics.

---

## Week of 2026-03-16
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Rajiv: Spring break planning.
- Lina: Board deck prep (Q1 2026).
**Discussion:**
- **Board Deck:** We need to explain the NRR dip clearly. 
- **Flat Dataset Rule:** Rajiv: "Found `acme.marts.clv`. NINA!" Nina: "I thought it would look cleaner!" Rajiv: "FLAT. DATASET. ONLY."

**Action Items:**
- [x] Nina: Move the CLV table and delete the dataset.
- [ ] Lina: Draft the NRR explanation slide.

---

## Week of 2026-03-23
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Nina: Fixed the CLV table location.
- David: Optimized the `workflow_runs_daily` mart.
**Discussion:**
- **Optimization:** David added a clustering key on `customer_id`. Query time dropped by 40%.
- **Customer Health:** **Drag Industries (cust_000412)** renewal is confirmed. 3-year deal.

**Action Items:**
- [ ] David: Apply clustering to the archive table too.
- [ ] Lina: Verify the ACV for the Drag Industries deal.

---

## Week of 2026-03-30
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Rajiv: Finalizing Q1.
- Lina: Total ARR as of today is $39.4M. 
**Discussion:**
- **Q1 Recap:** We grew despite the Beacon Studios hit. 
- **Engagement:** Engagement is at an all-time high (550 customers).

**Action Items:**
- [ ] Lina: Finalize the Q1 ARR snapshot.
- [ ] Nina: Update the engagement trend chart.

---

## Week of 2026-04-06
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Nina: Looking at the new 'Free' tier usage.
- David: Salesforce sync for 'Opportunities' is lagging.
**Discussion:**
- **Free Tier:** We have 30% of customers on Free. Nina: "Most of them never move. We should look at their 'integration_down_count'—they have much higher error rates."
- **Opportunities Lag:** It's a Salesforce API issue. David is on it.

**Action Items:**
- [ ] Nina: Create a report on Free-tier error rates.
- [ ] David: Resolve the Salesforce sync issue.

---

## Week of 2026-04-13
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Rajiv: Sprint 30.
- Nina: `bookings_attribution` for Q1 is final.
**Discussion:**
- **Attribution:** Inbound was strong this quarter. 
- **Flat Dataset Rule:** No violations.

**Action Items:**
- [ ] Lina: Update the Marketing attribution dashboard.
- [ ] Rajiv: Review the sprint 31 planning.

---

## Week of 2026-04-20
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Nina: Working on a "Seat Utilization Heatmap."
- David: Testing the new dbt 'semantic layer.'
**Discussion:**
- **Semantic Layer:** Rajiv: "Let's be careful. We don't want to overcomplicate the Looker models."
- **Customer Health:** **Cobalt Systems (cust_000700)** is still very stable.

**Action Items:**
- [ ] David: Prepare a demo of the semantic layer for the team.
- [ ] Nina: Finish the seat utilization heatmap.

---

## Week of 2026-04-27
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Rajiv: Last week of the month.
- Lina: ARR is looking like ~$39.8M. 
**Discussion:**
- **Monthly Close:** Almost back to $40M. 
- **Customer Health:** **Marigold Health (cust_000701)** had a minor issue with a failed invoice, but they paid it yesterday.

**Action Items:**
- [ ] Lina: Close the month of April.
- [ ] Nina: Update the health snapshots.

---

## Week of 2026-05-04 (Current)
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Rajiv: Preparing for the May board meeting.
- Nina: Looking at the `arr_snapshot` for today.
**Discussion:**
- **Current Numbers:** ARR is ~$39.8M. NRR 1.07 (it recovered!). 
- **Data Freshness:** BI warehouse is lagging prod by exactly 2 hours, as expected.
- **Flat Dataset Rule:** Alex asked about `acme.product.usage`. Rajiv just stared at him until he corrected himself.

**Action Items:**
- [ ] Rajiv: Finalize the board deck data.
- [ ] David: Audit the Looker cache settings.
- [ ] Nina: Add `step_count` to the CLV model.

---

## Week of 2026-05-11
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Nina: Auditing the "Engaged" flag in `acme.account_health`.
- David: Tuning the Airflow sensors for the `workflow_runs_daily` load.
- Rajiv: Board deck is 90% done. Sam wants a slide on "Platform Stickiness."

**Discussion:**
- **Engagement Logic:** Nina: "I found a few accounts marked as 'engaged' with only 2 users. I'm reverting to the Q4 2025 definition: MUST have ≥3 active users AND ≥10 successful runs in 28 days."
- **Noise:** The 3rd-floor espresso machine is out of commission again. Someone put oat milk in the water reservoir. Rajiv is not happy.
- **Customer Health:** **Onyx Robotics (cust_000704)** is showing massive usage spikes. They are on the Enterprise tier (500 seats), so the `utilization_band` is NULL, but their `n_runs` is up 400% week-over-week.

**Action Items:**
- [ ] Nina: Re-run the `account_health` materialization with the strict engagement logic.
- [ ] David: Check why `nexus-analyst-demo.acme.fact_workflow_runs` had a 15-minute gap on Tuesday.
- [ ] Rajiv: Send the stickiness slide to Jasmine for branding.

---

## Week of 2026-05-18
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Lina: Q2 pipeline review with Marcus. 
- Rajiv: Sprint 31 retro. 
- David: Schema changes in `fact_user_events` are live.

**Discussion:**
- **Bookings ACV:** Lina: "I saw an AE trying to multiply `bookings_acv_usd` by 12 for a report. I had to step in. It's already annualized."
- **Flat Dataset Rule:** David accidentally tried to create a sub-dataset `acme.staging.temp_users`. Rajiv caught the DDL in the logs. "Everything stays in `acme`. No folders in the warehouse."
- **Customer Health:** **Beacon Studios (cust_000287)** came up in the churn retro. Nina confirmed they were healthy (High NPS, high engagement) right until the parent company mandate. NRR 1.07 still holds because we're cohorting properly.

**Action Items:**
- [ ] Lina: Update the Looker Explores to hide the raw MRR fields to prevent the "multiply by 12" mistake.
- [ ] Nina: Build the 'churn reason' breakdown for the board deck appendix.
- [ ] David: Clear out the stale PDTs from the `acme_scratch` schema.

---

## Week of 2026-05-25
**Attendees:** rajiv.menon, david.kim, nina.patel (lina.cho OOO - hiking)
**Updates:**
- Nina: Looking into the "VRS" (Value Realization Score) request from Elena.
- Rajiv: Board meeting is tomorrow. No major changes allowed to the `arr_snapshot`.
- David: Fixed a bug in `fact_support_tickets` where `resolution_time_hours` was negative for 4 tickets.

**Discussion:**
- **VRS Draft:** Nina: "Elena is asking for the `vrs_band` column in the health mart." Rajiv: "Nope. VRS is a parked spec. We don't have the `champion_login_recency` data cleaned up yet. Tell her to use `account_health_status` as the proxy for now."
- **NRR Calculation:** David asked why we don't just INNER JOIN the 12-month cohort. Rajiv explained for the 100th time: "If you inner join, you drop the $0 end-state churns and the NRR looks like 1.20 instead of 1.07. We use a LEFT JOIN and COALESCE to 0. We're not cooking the books for the board."
- **Office:** Desk moves are happening Friday. Data team is moving closer to the windows.

**Action Items:**
- [ ] Nina: Draft a polite email to Elena about the VRS timeline.
- [ ] David: Update the dbt docs for `nrr_trailing_12` to explicitly mention the LEFT JOIN requirement.
- [ ] Rajiv: Survive the board meeting.

---

## Week of 2026-06-01
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Rajiv: Board meeting went well. Sam's only note: "Keep an eye on the Enterprise ramp."
- Lina: Starting the May month-end close. Initial ARR looks like ~$39.2M (slight growth!).
- Nina: New `dim_customers` attributes for 'Industry' are 95% populated.

**Discussion:**
- **May Close:** Lina: "We had a few Pro plan expansions. **Driftwood Media (cust_000702)** added 5 seats." 
- **Data Freshness:** The BI warehouse is still lagging by 2 hours. Elena is asking for real-time. Rajiv: "Not happening until we move off the 2-hour dbt cloud schedule. Prod isn't a playground."
- **Customer Health:** **Tamarind Group (cust_000706)** is still 'paused.' We need to check if they should be moved to 'churned' for the June snapshot if they don't resume by EOM.

**Action Items:**
- [ ] Lina: Finish the May MRR reconciliation by Thursday.
- [ ] David: Audit the `fact_invoices` table for any 'uncollectible' statuses that haven't hit the `account_health` mart.
- [ ] Nina: Update the `industry` mapping for the 15 remaining NULLs in `dim_customers`.

---

## Week of 2026-06-08
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- David: Working on `nexus-analyst-demo.acme.fact_marketing_touches` to support the new attribution model.
- Nina: Cleaning up the `utilization_band` logic. 
- Rajiv: Thinking about H2 planning.

**Discussion:**
- **Utilization for Enterprise:** Nina: "I'm still seeing people confused by the NULL `utilization_band` for Enterprise accounts like **Verdant Cloud (cust_000707)**. I'm going to add a tooltip in Looker explaining that Enterprise has unlimited seats, so a ratio is meaningless."
- **Marketing Attribution:** David: "The `lead_email_hash` join is still fuzzy. We're missing about 12% of the attributed revenue for the Q2 event in Vegas."
- **Noise:** Who left the fish in the breakroom microwave? The whole east wing smells like a pier. 

**Action Items:**
- [ ] Nina: Add the Looker tooltip for `utilization_band`.
- [ ] David: Sync with Jasmine on the `fact_marketing_touches` missing data.
- [ ] Lina: Pull the 'uncollectible' report for the CS team to review.

---

## Week of 2026-06-15
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Lina: ARR confirmed at $39.2M for May.
- Nina: New NPS survey results are flowing into `fact_nps_responses`.
- David: dbt 1.8 migration is starting in the dev branch.

**Discussion:**
- **NPS Detractors:** **Marigold Health (cust_000701)** just dropped a 4/10. Comment: "UI is too slow when loading large workflow histories." Their status is now 'at_risk' in `account_health` because of the detractor rule.
- **Flat Dataset Enforcement:** Rajiv: "I saw a PR with `FROM acme_marts_finance.arr_snapshot`. Rejected it. It's `FROM acme.arr_snapshot`. I don't care how dbt organizes the folders."
- **Customer Health:** **Yarrow Logistics (cust_000703)** is now 'healthy_expansion'—engaged and utilization is at 0.72. Marco should reach out for a Business-to-Enterprise upgrade convo.

**Action Items:**
- [ ] David: Keep the dbt migration in a separate branch until we've tested the `arr_snapshot` logic.
- [ ] Nina: Alert Olivia Tran about the Marigold Health NPS score.
- [ ] Lina: Update the AE commissions sheet for the May payouts.

---

## Week of 2026-06-22
**Attendees:** rajiv.menon, david.kim, nina.patel
**Updates:**
- Lina: OOO this week (San Diego for her sister's wedding).
- David: dbt 1.8 migration is 40% done. The `stg_` layer is mostly mapped.
- Nina: Looking into the engagement definition discrepancy. 

**Discussion:**
- **What is "Active"?** Nina found that `is_active` in `nexus-analyst-demo.acme.dim_users` only checks if the user isn't deleted, but Marketing wants "Active" to mean `last_login_date` within 30 days. Rajiv: "We need a `fact_user_engagement_daily` table to settle this. I don't want to calculate 30-day windows on the fly in Looker every time."
- **Data Freshness Alert:** `fact_workflow_runs` lagged by 6 hours yesterday. It was a BigQuery slot contention issue during the 2 AM batch. David is looking into moving the high-priority transforms to a reservation-based model.
- **Office Noise:** Can we please stop leaving the standing desks at max height when we leave? It looks like a forest of giant mushrooms in here. Also, the espresso machine is making that high-pitched whistling sound again.

**Action Items:**
- [ ] David: Review the BQ slot usage for the 2 AM window.
- [ ] Nina: Draft a definition for 'Monthly Active User' (MAU) and socialize with Product.
- [ ] Rajiv: Decide on the `is_sso_enabled` flag location (dim_customers vs. a new security table).

---

## Week of 2026-06-29
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Lina: Back from OOO. Starting Board Prep for the Q2 meeting. 
- Nina: Engagement metrics are now being tracked in a temp table `scratch_nina.user_activity_30d`.
- David: Migration paused to help Lina with the "Bridge to Q3" deck.

**Discussion:**
- **Board Prep:** We need a clean ARR bridge. Lina noticed a $15k gap between Salesforce and `nexus-analyst-demo.acme.fact_subscriptions` for **Verdant Cloud (cust_000707)**. Turns out the expansion was backdated to June 1st but the record didn't hit the warehouse until the 15th. 
- **The "Source of Truth" Flag:** Rajiv wants a column in `fact_subscriptions` called `is_source_of_truth` so we can filter out the messy legacy records from the 2023 migration. 
- **Customer Review:** **Yarrow Logistics (cust_000703)** is asking for SOC2 docs. Nina, can you check if their `plan_tier` is actually updated to Enterprise? They shouldn't have access to the audit log export yet if they are still on Business.

**Action Items:**
- [ ] Lina: Finalize the Q2 ARR bridge by EOD Thursday.
- [ ] David: Fix the backfill for **Verdant Cloud** expansion in the snapshot.
- [ ] Nina: Check the `dim_plans` logic to see why **Yarrow** can see the Audit Log button.

---

## Week of 2026-07-06
**Attendees:** nina.patel, david.kim, rajiv.menon
**Updates:**
- Lina: In meetings with the Board all morning.
- Rajiv: Planning the H2 roadmap. We might need a dedicated Analytics Engineer for the Marketing team.
- David: dbt 1.8 migration is back on track.

**Discussion:**
- **Incident Report:** On July 4th, the ingestion for `fact_user_events` failed because of a schema change in the frontend event collector. Someone added `browser_extension_version` as an integer but some clients sent it as a string. David patched it with a `SAFE_CAST`. 
- **Metric Review:** Churn is looking high for the SMB segment (Pro plan). Nina thinks it's because the `workflow_run_quota_per_month` is too low at 10k. Users hit the limit, get frustrated, and leave before an AE can talk to them about Business tier. 
- **Noise:** The 4th-floor move is confirmed for August. Start packing your pedestals. David is losing his mind about the lack of monitors in the new floor plan.

**Action Items:**
- [ ] David: Update the CI/CD pipeline to catch schema mismatches in `fact_user_events`.
- [ ] Nina: Run a distribution analysis on `step_count` for Pro users vs Business users.
- [ ] Rajiv: Interview the candidate for the AE role (Marcus).

---

## Week of 2026-07-13
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel, jasmine.lee (Marketing guest)
**Updates:**
- Jasmine: Marketing needs better attribution for the "Summer Automation Series" webinars.
- Lina: Q2 Board meeting was a success. Revenue numbers were accepted without questions (thanks for the bridge, David).
- Nina: NPS for July is starting to come in.

**Discussion:**
- **Marketing Attribution:** Jasmine is frustrated that `acquisition_channel` in `nexus-analyst-demo.acme.dim_customers` is just 'Paid Social' for half the new signups. We need to join against `fact_marketing_touches` using the `lead_email_hash`. 
- **Performance Issues:** **Marigold Health (cust_000701)** submitted another ticket. Their `fact_workflow_runs` records show some steps are taking >10 seconds. Rajiv: "That’s an infra issue, not a data issue, but we need to provide the P99 latency report to Eng."
- **VRS Status:** The Vendor Risk Security audit is next week. We need to ensure no PII (emails, names) is in any table EXCEPT `dim_users` and `dim_employees`. Nina found some emails in the `error_code` column of `fact_workflow_runs` where people are passing raw strings in headers.

**Action Items:**
- [ ] David: Create a regex mask for the `error_code` column to scrub emails.
- [ ] Nina: Help Jasmine with the attribution join logic in Looker.
- [ ] Lina: Order more coffee pods; the "dark roast" is actually just charcoal at this point.

## Week of 2026-07-20
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- David: dbt Cloud freshness alerts are firing for `fact_subscriptions`. Source data from Stripe is lagging by 6 hours. Looking into the Fivetran connector.
- Nina: Finished the VRS audit prep. All PII in `fact_workflow_runs.error_code` is now masked in the downstream view `v_workflow_runs_secure`. 
- Rajiv: Marcus accepted the AE offer. He starts on Aug 3rd.

**Discussion:**
- **Churn Alert:** **Omni-Global (cust_000102)** decreased their seat count from 150 to 85 this morning. Nina, check `fact_subscriptions` to see if they moved from Business to Pro or if it’s just a seat contraction. Rajiv thinks they might be moving to a competitor because of the uptime issues we had in June.
- **Engagement Definition:** We need a formal "Monthly Active User" (MAU) definition for the Q3 Board Deck. Is it just a row in `fact_user_events` or does it require a successful run in `fact_workflow_runs`? David argues that `event_type = 'login'` is too shallow. Lina wants a "Value-Added User" metric—someone who triggered a workflow that didn't end in `status = 'error'`.
- **Office Noise:** The boxes for the move are being delivered tomorrow. Please don't put monitors in the boxes; they go in the special crates. 

**Action Items:**
- [ ] Nina: Build a 'Product Health' dashboard for Rajiv showing `run_id` success rates by `customer_id`.
- [ ] David: Fix the `fact_subscriptions` freshness issue before the Monday morning sync.
- [ ] Lina: Verify the final headcount budget for Marcus’s onboarding package.

---

## Week of 2026-07-27
**Attendees:** rajiv.menon, david.kim, nina.patel, jasmine.lee
**Updates:**
- Jasmine: The "Summer Automation Series" has generated 400 leads, but conversion to "Pro" is under 2%.
- Nina: Found a bug in the `dim_customers` join. Some Pro users were being tagged as "Free" because their `subscription_id` wasn't updated in the nightly batch.
- Rajiv: Marigold Health (cust_000701) is asking for a discount on their Enterprise renewal.

**Discussion:**
- **Data Quality:** David is seeing a lot of `null` values in the `industry` column of `nexus-analyst-demo.acme.dim_customers`. It’s breaking Jasmine’s segmentation. Nina: "It’s because the Clearbit enrichment API is hitting a rate limit." We need to backfill the missing industries using the `email_domain` from `dim_users`.
- **Workflow Latency:** Nina ran the P99 report for Marigold. Their average `duration_ms` is 12,400ms, mostly because they are calling a very slow legacy API in their steps. Rajiv: "Can we prove it's their endpoint and not our engine?" David: "Check the `error_code` column; if it's a 504, it's them."
- **Internal:** The coffee machine on 3 is leaking. Use the one in the 2nd-floor lounge until Friday.

**Action Items:**
- [ ] David: Increase the Clearbit API timeout and add a retry logic.
- [ ] Nina: Create a slide for Rajiv showing Marigold’s `duration_ms` vs the platform average for the 'Health Tech' industry.
- [ ] Jasmine: Send the webinar attendee list (email_hash) to Nina for the `fact_marketing_touches` join.

---

## Week of 2026-08-03
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel, marcus.reed (New AE)
**Updates:**
- Rajiv: Welcome Marcus! He’ll be taking over the Mid-Market accounts in the Northeast.
- David: The move is 80% complete. My pedestal is missing. If anyone sees a pedestal with a "Do Not Move" sticker, it's mine.
- Nina: Q3 forecast is looking good. Current MRR is $38.2M.

**Discussion:**
- **Schema Change:** David wants to add `is_test_account` to `nexus-analyst-demo.acme.dim_customers`. Engineering is creating way too many test accounts (like 'Acme Test 123') and it's inflating the Free tier count. Nina needs to update the Looker `explore` to filter these out by default.
- **Seat Utilization:** Lina noticed that **Cyberdyne Systems (cust_000405)** is paying for 500 seats on Business but only has 210 `is_active = true` users in `dim_users`. This is a huge churn risk for their renewal in October. Marcus, this is your first assignment—get them to provision those seats.
- **Board Prep:** Lina needs the final "Runs per Seat" metric by Friday. Use `fact_workflow_runs` joined with `fact_subscriptions` on `customer_id`.

**Action Items:**
- [ ] Nina: Add `is_test_account` filter to all executive dashboards.
- [ ] Marcus: Schedule a sync with the Cyberdyne admin.
- [ ] David: Find your pedestal; it's probably in the loading dock.
- [ ] Lina: Finalize the "Revenue by Industry" report for the board.

---

## Week of 2026-08-10
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel
**Updates:**
- Nina: I found a massive discrepancy in `mrr_usd`. Some Enterprise contracts have `billing_cycle = 'Annual'` but the MRR was being calculated as the full contract value instead of /12.
- Rajiv: Marcus is already in talks with a new prospect, "Starlight Ventures."
- David: The new monitors are finally here. David is happy.

**Discussion:**
- **Product Launch:** The "AI Workflow Suggestor" is going into beta next week. We need a new event type in `fact_user_events` called `ai_suggestion_accepted`. Nina, please update the schema doc for the Eng team so they pass the correct `event_properties` (JSON).
- **PLG Friction:** Users on the Free tier are complaining about the 2-workflow limit. Rajiv wants to see a histogram of `step_count` for users who hit the limit vs those who don't. If they are building 50-step workflows, they should be on Pro anyway.
- **VRS Follow-up:** The auditors asked about `dim_employees`. They want to see `termination_date` for everyone who left in 2025 to ensure their warehouse access was revoked. 

**Action Items:**
- [ ] David: Create a dbt test to ensure `mrr_usd` never exceeds `amount_usd` for monthly subscribers.
- [ ] Nina: Run the "2-workflow limit" impact analysis.
- [ ] Lina: Send the `dim_employees` export to the Security team.
- [ ] Rajiv: Check if "Starlight Ventures" is already in `dim_customers` as a lead.

---

## Week of 2026-08-17
**Attendees:** nina.patel, david.kim, rajiv.menon, marcus.young
**Updates:**
- **dbt Alert:** `source_freshness` on `fact_user_events` failed this morning. Looks like the Segment hook died around 02:00 UTC. David is looking into the Fivetran logs.
- **Office:** The 3rd floor coffee machine is leaking again. Please stop trying to fix it with paper clips. Use the one in the lounge.
- **Cyberdyne:** Marcus had the sync. They’re happy but complaining that `duration_ms` in `fact_workflow_runs` seems inflated for their "Data Scrub" flow. 

**Discussion:**
- **AI Beta:** We’ve got 12 customers in the beta. Early data in `fact_user_events` (where `event_name = 'ai_suggestion_accepted'`) shows a 40% higher retention rate for users who accept at least one suggestion in their first 48 hours. 
- **Schema Change:** We need to add `trigger_source` (webhook, schedule, on_demand) to `fact_workflow_runs`. Right now it’s all lumped under `triggered_by`. Nina, can you check if we can pull this from the raw `nexus-analyst-demo.acme.raw_events` table?
- **VRS Status:** The SOC2 audit is moving to the "Evidence Collection" phase. Lina needs a list of all `dim_employees` where `role` contains 'Engineer' or 'Data' to cross-reference against GitHub access logs.

**Action Items:**
- [ ] David: Restart the Fivetran sync for `user_events`.
- [ ] Nina: Verify if `trigger_source` is available in the JSON payload of `raw_events`.
- [ ] Marcus: Follow up with Cyberdyne on the `duration_ms` discrepancy—check if they’re counting cold-start time.
- [ ] Rajiv: Buy more oat milk for the lounge.

---

## Week of 2026-08-24
**Attendees:** lina.cho, nina.patel, david.kim
**Updates:**
- Nina: I’m OOO Friday for a wedding.
- David: Desk moves are happening this weekend. If you have a standing desk, tag it with your `employee_id`.

**Discussion:**
- **Engagement Metric:** We need a formal definition for "North Star" engagement. Rajiv thinks it should be "at least 5 successful runs per week." Nina prefers "at least 1 manual workflow edit in `fact_user_events` where `event_type = 'workflow_updated'`." We’ll look at the correlation between these two and NRR (Net Revenue Retention) over the last 6 months.
- **Data Quality:** Found some rows in `fact_subscriptions` where `start_date` > `end_date`. It’s mostly on the `plan_tier = 'Business'` accounts. Lina thinks it’s an artifact of the "Grace Period" logic in the billing system.
- **Starlight Ventures:** They are in `dim_customers` as a lead, but the `acquisition_channel` is 'NULL'. Marcus needs to track down which SDR touched this first.

**Action Items:**
- [ ] Nina: Build a dbt model `marts.fct_engagement_comparison` to test the two "North Star" definitions.
- [ ] Lina: Manual cleanup of the `start_date` bugs in the billing CSV before the next sync.
- [ ] David: Update the `dim_customers` view to default `acquisition_channel` to 'Unknown' instead of NULL.

---

## Week of 2026-08-31
**Updates:**
- Short meeting. Half the team is OOO for the end of summer.
- **Incident:** `fact_invoices` didn't refresh because `dim_dates` didn't have 2027-2030 populated and a join failed. David extended the date seed.
- **Board Prep:** Lina needs the "Average Seat Utilization" by `industry`. Specifically: `count(distinct triggered_by) / sum(seat_count_licensed)` from `fact_workflow_runs` joined with `dim_customers`.

---

## Week of 2026-09-07
**Attendees:** rajiv.menon, lina.cho, david.kim, nina.patel, marcus.young
**Updates:**
- Marcus: Cyberdyne just signed for an additional 100 seats! They’re officially our largest Enterprise account in the `Manufacturing` industry.
- Nina: The `is_test_account` filter is live on all Looker dashboards. If you see $0 MRR for a "Big Company," it’s probably filtered out now.

**Discussion:**
- **PLG Funnel:** We’re seeing a drop-off in the "Pro" upgrade path. Users are hitting the 2-workflow limit on the Free tier but instead of upgrading, they’re just deleting old workflows. Rajiv wants to propose a "Pro-Lite" tier. Nina needs to pull `step_count` vs `workflow_id` for these "deleters" to see if they’re building complex stuff or just garbage.
- **Warehouse Performance:** `fact_workflow_runs` is getting huge (~500M rows). Queries are slowing down. David is considering partitioning by `triggered_at` (day). 
- **VRS Follow-up:** Security found three `dim_users` who still have 'Admin' roles but haven't logged in since 2024. Nina, send a list of `user_id` and `email_domain` to the IT team for immediate de-provisioning.

**Action Items:**
- [ ] Nina: Run the "Deleter" analysis (complex vs simple workflows on Free tier).
- [ ] David: Draft a DDL script for the `fact_workflow_runs` partitioning.
- [ ] Marcus: Send a "Thank You" basket to the Cyberdyne admin. (Check if they have a no-gift policy first).
- [ ] Lina: Prepare the "Industry Utilization" slide for the Friday board deck. Use `nexus-analyst-demo.acme.dim_customers` for the industry labels.

---

## Week of 2026-09-14
**Updates:**
- Rajiv: Starlight Ventures is stalled. They want SOC2 Type II, which we won't have until Q1 2027. 
- David: The new monitors in the Amsterdam office are 4K. SF team is jealous.

**Discussion:**
- **Metric Review:** `mrr_usd` is up 4% MoM, but mostly from seat expansion, not new logos. 
- **Schema:** Need to add `error_message` (string) to `fact_workflow_runs`. Right now we only have `error_code`. Engineers say the message is in the `raw_events` logs.

**Action Items:**
- [ ] Nina: Update the `fact_workflow_runs` dbt model to parse `error_message` from the JSON.
- [ ] David: Check why `dim_employees` shows Marcus reporting to "NULL". He should be under Rajiv.

---

## Week of 2026-09-21
**Updates:**
- Nina: "Deleter" analysis is partially done. Preliminary data shows that about 40% of the Free tier users hitting the 2-workflow cap have workflows with `step_count` > 12. These aren't "garbage" users; they’re building complex logic and then pruning to stay under the paywall. We are definitely cannibalizing the Pro tier.
- Rajiv: Closed a small expansion deal with Globex Corp. 50 more seats on the Business plan.
- Noise: The espresso machine in the SF breakroom is leaking again. Please don't use it until the repair tech arrives on Wednesday.

**Discussion:**
- **Engagement Metric:** Marketing wants to redefine "Active User" to include anyone who triggers a webhook, not just UI logins. Nina, can we look at `fact_workflow_runs` vs `fact_user_events`? If we count webhook triggers as "active," our MAU looks 20% better, but it might be misleading for seat-based expansion.
- **dbt Freshness:** We’re getting alerts on `fact_subscriptions`. The Fivetran sync from Stripe lagged by 6 hours yesterday. David says it's a known issue with the Stripe API connector. 

**Action Items:**
- [ ] Nina: Finalize the "Pro-Lite" deck. Need a chart showing `mrr_usd` potential if we convert 10% of "High-Step Free Users."
- [ ] David: Investigate the `fact_subscriptions` lag. Are we missing any `change_type` events from the weekend?
- [ ] Lina: Reach out to the CSM for Cyberdyne. They have 400 licensed seats but only 210 `last_login_date` values in the last 30 days.

---

## Week of 2026-09-28
**Updates:**
- David: Partitioning on `fact_workflow_runs` is LIVE. Query costs for the "Daily Ops" dashboard should drop by about 30%. Remember to use the `triggered_at` filter in your WHERE clauses or BigQuery will still scan the whole table!
- Marcus: I'm OOO on Friday for a long weekend. Tag Rajiv for any urgent contract approvals.

**Discussion:**
- **VRS Status:** Security is still unhappy about the Admin roles. We found 12 more users in `dim_users` with `is_active = TRUE` but `last_login_date` in 2024. We need an automated script to flip `is_active` to FALSE if no login for 180 days.
- **Data Integrity:** Some rows in `dim_customers` have `country` as 'US' and some as 'United States'. It’s messing up the Region maps in Looker. 

**Action Items:**
- [ ] Nina: Create a SQL view to clean up `country` names in `dim_customers` (standardize on ISO codes).
- [ ] David: Update the dbt model for `dim_users` to include an `is_stale_admin` flag.
- [ ] Rajiv: Review the SOC2 roadmap with the Eng team. If we can't get Type II by Q1 2027, we might lose the Starlight Ventures deal entirely.

---

## Week of 2026-10-05
**Updates:**
- Lina: Board deck is almost ready. The "Industry Utilization" slide shows Finance and Healthcare are our stickiest segments. 
- Rajiv: New logo! "Soylent Corp" signed for a Pro pilot. 15 seats. 

**Discussion:**
- **Schema Request:** Engineering wants to add `is_retry` (boolean) to `fact_workflow_runs`. Apparently, some users are spamming the "Retry" button on failed steps, which is inflating our "Total Runs" metric. 
- **Office:** Desk moves in Amsterdam are happening this weekend. Check the Slack channel for the new seating chart.

**Action Items:**
- [ ] Nina: Pull a report on "Retried" runs from the `raw_events` to see if it’s a specific customer (check Cyberdyne or Umbrella Corp).
- [ ] David: Update `dim_employees` to fix the reporting structure. Marcus should report to Rajiv, and we need to add the new AE hire (Sarah) starting next week.
- [ ] Lina: Verify the `current_mrr_usd` for Soylent Corp in `nexus-analyst-demo.acme.dim_customers`. It should be ~$735.

---

## Week of 2026-10-12
**Updates:**
- Nina: `error_message` is now available in `fact_workflow_runs`! I parsed it out of the JSON. It's already saved me three support tickets today.
- David: The SF team finally got their 4K monitors. No more jealousy.

**Discussion:**
- **Churn Alert:** "Initech" (MM account) just moved to `status = 'paused'`. Their `churn_date` isn't populated yet because they're on a "Save" plan (90 days at $0). We need to make sure the `mrr_usd` logic in `fact_subscriptions` handles $0 months without breaking the "Total ARR" calculation.
- **Naming Conventions:** We have `seat_count_licensed` in `dim_customers` but `seat_count` in `fact_subscriptions`. Are these the same? David says `fact_subscriptions` is the "truth" for billing, but `dim_customers` is easier for the Sales team to read. We should probably sync them.

**Action Items:**
- [ ] David: Create a test in dbt to ensure `dim_customers.seat_count_licensed` matches the most recent `fact_subscriptions.seat_count`.
- [ ] Marcus: Check in with Initech. Why did they pause? Is it a feature gap or just budget?
- [ ] Nina: Run a quick query on `fact_workflow_runs` to see the most common `error_message` for Enterprise customers. Is it a timeout or a 401?

---

## Week of 2026-10-19
**Updates:**
- Rajiv: Starlight Ventures is back at the table. They’re okay with SOC2 Type I as long as we have a firm "Letter of Intent" for Type II. 
- Nina: OOO this Thursday/Friday (Wedding in Italy). 

**Discussion:**
- **Sprint Retro:** We’re spending too much time fixing `dim_employees`. Can we just pull this directly from the HRIS instead of a manual CSV upload? David is looking into the BambooHR API.
- **Metric Review:** `mrr_usd` growth is flat this week. We have a lot of "Pro" trials expiring. Need Marketing to trigger the "Last Chance" email sequence.

**Action Items:**
- [ ] Lina: Check the `acquisition_channel` for the last 50 Pro signups. Are they coming from the "Product Hunt" campaign or organic? Use `nexus-analyst-demo.acme.dim_customers`.
- [ ] David: Draft the BambooHR sync plan. 
- [ ] Nina (before OOO): Send the list of stale Admin users to IT. Use the `user_id` and `email_domain` columns from `dim_users`.

---
## Week of 2026-10-26
**Updates:**
- Nina: Back from Italy! Still a bit jet-lagged but catching up on the Slack deluge.
- David: dbt Cloud freshness alerts are firing for `fact_user_events`. Looks like the Fivetran connector for the Segment log stalled. We might be missing data from Sunday.
- Marcus: Signed "Hooli" (Ent) for 300 seats. Marcus needs to make sure they get the white-glove onboarding since they’re moving from a competitor.

**Discussion:**
- **Board Prep:** Q4 board meeting is coming up. We need a definitive "NPS by Plan Tier" report. Nina, can you join `fact_user_events` (specifically `event_type = 'nps_submitted'`) with `dim_customers.current_plan_tier`? Let's use the `nexus-analyst-demo.acme` tables to keep it clean.
- **Office Noise:** The 4th-floor coffee machine is leaking again. Facilities says "don't use the espresso lever." Just use the drip for now. Also, the desk move for the Marketing team is finalized for Friday.

**Action Items:**
- [ ] David: Restart the Segment sync. Check if the `user_id` mapping in `nexus-analyst-demo.acme.dim_users` is still valid for the Hooli domain.
- [ ] Nina: Build the NPS dashboard. Focus on 'Business' and 'Enterprise' segments.
- [ ] Lina: We need the LTV:CAC ratio for the board deck. Can you verify the `acquisition_channel` spend for October?

---

## Week of 2026-11-02
**Updates:**
- Rajiv: Starlight Ventures SOC2 LOI is signed! We are officially in the "Security Review" phase.
- Lina: The "Product Hunt" campaign was a dud. Most signups were `status = 'churned'` within 48 hours. Looking into "low-intent" filters.

**Discussion:**
- **Engagement Definition:** We’re still arguing about what a "Monthly Active User" (MAU) is. Is it just a login, or do they have to run a workflow? 
- Marcus thinks a "Run" is the only thing that matters. 
- David points out that some users just view logs (`event_type = 'log_viewed'` in `fact_user_events`) and that’s still value.
- **VRS Status:** The "Variable Retention Score" model is currently running on a Python script on David’s laptop. We need to move this into a dbt model so it can live in `dim_customers`.

**Action Items:**
- [ ] David/Nina: Define `is_active_engagement` in a new dbt macro. If a user has a record in `fact_workflow_runs` OR has logged in (`last_login_date`) within 30 days.
- [ ] Marcus: Send the Starlight Ventures security questionnaire to David.

---

## Week of 2026-11-09
**Updates:**
- Nina: Fixed the $0 MRR bug. The `fact_subscriptions` logic now explicitly ignores `change_type = 'internal_test'`.
- David: BambooHR API is... difficult. The `dim_employees` table will remain a manual CSV upload for the rest of November.

**Discussion:**
- **Invoicing Issues:** A few customers on the "Business" tier reported that their `fact_invoices` show `status = 'open'` even though they paid via Stripe. It looks like a webhook delay. 
- **Expansion Opportunity:** "Pied Piper" (currently SMB tier, 15 seats) is hitting their `workflow_run_quota_per_month` (10,000 runs) every single month. They’re a prime candidate for an upsell to the "Business" tier.

**Action Items:**
- [ ] Marcus: Reach out to the admin at Pied Piper. Check `dim_users` to see who the primary `owner` is.
- [ ] Nina: Audit `fact_invoices` for any `amount_usd > 5000` that is still `open` after 10 days.
- [ ] Rajiv: Update the "Series B Roadmap" slide for the all-hands.

---

## Week of 2026-11-16
**Updates:**
- Marcus: "Initech" is officially back to `status = 'active'`. The "Save" plan worked. They didn't want to lose their historical workflow data.
- Nina: OOO next week for Thanksgiving. 

**Discussion:**
- **Schema Change:** We need to add `region` to `dim_customers` to help the EMEA team. David says the data is in the raw CRM export, just needs to be mapped.
- **Usage Audit:** Enterprise seat utilization is at 62%. We sold 2,500 seats but only 1,550 are assigned to a `user_id` in `dim_users`. Sales needs to push for "User Provisioning" during QBRs.

**Action Items:**
- [ ] David: Update `nexus-analyst-demo.acme.dim_customers` to include the `region` column. Default to 'NA' if null.
- [ ] Marcus: Check the seat gap for "Soyuz Corp". They paid for 500 seats but only have 40 active users.
- [ ] Lina: Can we get a count of `email_domain` per customer? Trying to find "Shadow IT" signups that aren't linked to the parent `customer_id`. Use `nexus-analyst-demo.acme.dim_users`.

## Week of 2026-11-23
**Updates:**
- Nina: OOO (Thanksgiving week).
- David: `region` column is now LIVE in `nexus-analyst-demo.acme.dim_customers`. It’s defaulting to 'NA' for old rows. EMEA team needs to verify the 'EMEA' tag for their accounts.
- Marcus: Pied Piper signed the Business tier upgrade! MRR will jump in `fact_subscriptions` starting Dec 1.

**Discussion:**
- **Short week:** Most of the team is out Wed-Fri. 
- **Employee Table:** David still fighting the BambooHR CSV. `dim_employees` hire dates for the new Sales hires (Oct 2026 batch) are slightly off. Marcus says don't worry about it until the end-of-year comp reviews.

**Action Items:**
- [ ] David: Fix the `region` mapping for the "Aperture Science" account. It's showing as 'NA' but they are definitely out of the Berlin office.
- [ ] Rajiv: Make sure the coffee machine on Floor 3 is serviced. It’s making that grinding noise again.

---

## Week of 2026-11-30
**Updates:**
- Nina: Back. Caught a bug in the VRS (Value Realization Score) calculation. We were double-counting `triggered_by = 'system'` runs in `fact_workflow_runs`. 
- Rajiv: Preliminary Q4 forecast looks strong. Net Retention is hovering at 112%.

**Discussion:**
- **Desk Moves:** Marketing is moving to the west wing. David is moving his monitors next to the Eng pod to "facilitate better dbt communication" (aka Nina is tired of Slack threads).
- **VRS Definition:** We need to finalize the "Engagement" metric for the Board. Right now, it’s defined as any user with >1 event in `nexus-analyst-demo.acme.fact_user_events` in a 7-day window. Nina thinks this is too low. Proposing "Power User" = >5 manual `triggered_at` events per week.
- **Data Latency:** The `fact_workflow_runs` table is getting massive (~400M rows). The 2-hour lag is starting to push to 3 hours on Monday mornings. 

**Action Items:**
- [ ] Nina: Propose a new `dim_user_segments` table based on the Power User definition.
- [ ] David: Look into partitioning `fact_workflow_runs` by `triggered_at` (day) to speed up the BI dashboards.
- [ ] Marcus: Follow up with Soyuz Corp. Their seat utilization is still abysmal (8%). If they don't improve, they are a huge churn risk for Q1.

---

## Week of 2026-12-07
**Updates:**
- Marcus: "Soyuz Corp" says they are struggling with SSO setup. That’s why the users aren't in `dim_users`. They need a hand from the Solutions Arch team.
- Nina: dbt freshness alert hit this morning on `fact_invoices`. Stripe API had a hiccup. It’s resolved now, but the `paid_at` timestamps for Dec 5th might be delayed in the warehouse.

**Discussion:**
- **Board Prep:** Rajiv needs the "Top 10 Customers by MRR" list from `dim_customers` vs their `workflow_run_quota_per_month`. He wants to see who is consistently exceeding their tier.
- **Shadow IT:** Lina’s query on `email_domain` found 42 unique domains at "Globex Corp" that are on Free plans instead of being rolled into the Enterprise parent. That’s a massive upsell lead.

**Action Items:**
- [ ] Lina: Export the Globex "Shadow IT" list and send to Marcus. Cross-reference `invited_by_user_id` to see who the internal champions are.
- [ ] David: Clean up the `dim_customers.industry` field. We have "Healthcare", "Health", and "Medical" all as separate strings. 
- [ ] Nina: Audit `fact_workflow_runs` for `error_code` spikes. Engineering thinks the new "Slack Notification" connector is failing for 5% of runs.

---

## Week of 2026-12-14
**Updates:**
- Rajiv: Series B pitch deck is 90% done. The "Expansion Revenue" slide uses Nina's new VRS logic.
- David: `dim_employees` is finally stable. No more manual CSVs. BambooHR sync is working (mostly). 

**Discussion:**
- **Metric Review:** We’re seeing a weird dip in `is_active` users in `dim_users`. It might be seasonal (December vacation), or the "last_login_date" isn't updating correctly for users who only use the API/CLI.
- **Holiday Party:** Reminder that the office is closed Friday for the party. Please don't run any heavy `SELECT *` queries on `fact_user_events` after 4 PM; it slows down the real-time revenue dashboard for Finance.

**Action Items:**
- [ ] Marcus: Send the "Year in Review" usage reports to all Enterprise customers. Use the `step_count` from `fact_workflow_runs` to show "Value Created."
- [ ] Nina: Check if `last_login_date` is capturing API token usage. If not, we're underreporting active users.
- [ ] David: Check the `nexus-analyst-demo.acme.fact_subscriptions` table for any `end_date` collisions. We had two records for "Weyland-Yutani" that overlapped in November.

---

## Week of 2026-12-21
**Updates:**
- Nina: Final dbt run for the year looks clean. All tests passed.
- Marcus: Signed "Tyrell Corp" to a Pro plan for 20 seats. Nice little end-of-year win.

**Discussion:**
- **2027 Planning:** We need a way to track "Feature Adoption" in the warehouse. Currently, `fact_user_events` just says `event_name = 'button_click'`. We need more granularity (e.g., `workflow_created`, `integration_connected`).
- **Support Load:** The "Business" tier support volume is up. Nina thinks it’s because the `workflow_run_quota_per_month` notifications are confusing. People think they are being charged overages (we don't do overages, we just throttle).

**Action Items:**
- [ ] Rajiv: Review the `current_mrr_usd` discrepancies in `dim_customers`. A few accounts show $0 even with active subs.
- [ ] Lina: Enjoy the break. See everyone on Jan 4th!
- [ ] Nina: (Low Priority) Look into the `dim_dates` table for 2027. Make sure the holiday flags are set for EMEA.

---

## Week of 2027-01-04
**Updates:**
- Nina: Back from Chamonix. Caught up on the dbt cloud logs—looks like the `fact_invoices` incremental run failed on Jan 1st because of a leap-second logic error in the source system. Fixed now.
- David: Migrated the SFDC connector. `dim_customers` should now correctly reflect the `ae_employee_id` for the new 2027 territories.
- Marcus: Pushing the Q4 QBR data to the CS team.

**Discussion:**
- **The "Active User" Debate:** Product wants to change `is_active` in `dim_users` to only count people who have "successfully completed a workflow run" in the last 14 days. Currently, it's just "any login in 28 days." This will tank our North Star metric by 40%. Nina to model the impact before we commit.
- **Office Noise:** The new espresso machine in the SF office is leaking. Please put a paper towel under it if you use it. Also, Sarah is moving to the desk by the window, so don't leave your monitor stands in the middle of the aisle.
- **Stark Industries:** They just added 500 seats (Enterprise). Need to ensure the `seat_count_licensed` in `nexus-analyst-demo.acme.dim_customers` updates by tomorrow's sync or Finance will ping us.

**Action Items:**
- [ ] Nina: Run a comparison query on `fact_user_events` for the new "Active User" definition.
- [ ] David: Check the `fact_workflow_runs` table for `error_code` spikes. Seeing some '504's from the Slack integration.
- [ ] Rajiv: Verify why "Cyberdyne Systems" is showing as `status = 'paused'` when they just paid their annual invoice.

---

## Week of 2027-01-11
**Updates:**
- Rajiv: Preliminary Q4 ARR is $38.8M. Very close to the $39M target.
- Nina: Added `industry` and `acquisition_channel` to the `dim_customers` table for better LTV/CAC analysis by the Marketing team.

**Discussion:**
- **Board Prep:** Board meeting is on the 22nd. We need a "clean" view of `fact_subscriptions`. No more overlapping `start_date` and `end_date` records. If a customer upgrades, the old record *must* close the day before the new one starts. 
- **Data Freshness:** The `nexus-analyst-demo.acme.fact_user_events` table was 6 hours stale yesterday. It turns out the Fivetran sync for the `events` table was stuck behind a massive batch of deletions from the `staging_logs`.

**Action Items:**
- [ ] Nina: Build the "Logo Churn vs MRR Churn" dashboard for the board deck. Use `change_type` from `fact_subscriptions`.
- [ ] David: Investigate the `null` values in `region` for about 50 customers in EMEA. Might be a missing mapping in the `dim_customers` build.
- [ ] Marcus: Send the list of "Pro" customers with >8,000 runs/mo to the Sales team. They are hitting their `workflow_run_quota_per_month` and are prime for "Business" tier upgrades.

---

## Week of 2027-01-18
**Updates:**
- David: Fixed the EMEA region mapping. Most were just missing "Netherlands" in the country-to-region lookup.
- Nina: Set up a dbt freshness alert for `fact_workflow_runs`. If it's more than 4 hours old, it pings the #data-ops Slack channel.

**Discussion:**
- **Engagement Definition:** We're seeing high `step_count` in `fact_workflow_runs` for "Hooli", but very low `event_count` in `fact_user_events`. It looks like they are running massive automated scripts via the API but not actually using the UI. Does this count as "Retained"?
- **VRS Status:** The "Value Realization Score" project is stalled. We need a way to weigh different event types. Is a `workflow_created` worth 10x a `button_click`? 
- **Incident:** Last Tuesday, `fact_invoices` showed $0 for all "Weyland-Yutani" records. It was a currency conversion bug (someone put 'YEN' instead of 'USD' in the manual override). It's patched.

**Action Items:**
- [ ] Lina: Finalize the 2027 holiday flags in `dim_dates`. Don't forget the Amsterdam office has King's Day off in April.
- [ ] Marcus: Can we pull a list of all users who haven't logged in since Dec 1st? Use `last_login_date` from `dim_users`.
- [ ] Nina: Check why `duration_ms` in `fact_workflow_runs` is occasionally negative. Likely a timestamp mismatch between the trigger and the completion logs.

---

## Week of 2027-01-25
**Updates:**
- Nina: Cleaned up the `dim_employees` table. Managers now correctly map to the `employee_id`. 
- David: BambooHR sync is officially 100% automated. If someone gets hired, they show up in the warehouse within 24 hours.

**Discussion:**
- **Sprint Retro:** The team felt like the "ad-hoc" requests from Sales are getting out of hand. We need a Jira ticket for any query that takes more than 15 minutes to write. 
- **Customer Feedback:** "InGen" is complaining that their usage dashboard in the product doesn't match our monthly report. It's because the product UI uses `triggered_at` and the report uses `paid_at` for the billing period. We need to align on a single source of truth for "Monthly Usage."

**Action Items:**
- [ ] Rajiv: Review the `current_mrr_usd` for "Tyrell Corp". It looks like the seat count updated but the MRR didn't follow the `$149/seat` logic for the Business tier.
- [ ] David: Update the schema for `fact_user_events` to include `device_type`. Product wants to see how many people are checking workflow status on mobile.
- [ ] Nina: (High Priority) Fix the `dim_customers` join that is dropping "Stark Industries" from the "Enterprise" view because they don't have a `csm_employee_id` assigned yet.

---

## Week of 2027-02-01
**Updates:**
- Nina: All 2027 holidays are in `dim_dates`.
- Marcus: Successfully demoed the new "Usage Forecast" model to the VP of Sales.

**Discussion:**
- **The Coffee Situation:** The leak is fixed, but now we're out of the "Dark Roast" beans. Marcus is on it.
- **Desk Moves:** Reminder that the Amsterdam office is shifting to "Hot Desking" starting next week. No more fixed monitors for the Analytics team there.
- **Metric Check:** Churn is looking high for Jan. Seeing a lot of "SMB" accounts moving from "Pro" to "Free" (down-selling). We need to see if there's a correlation with the recent `workflow_run_quota_per_month` changes.

**Action Items:**
- [ ] David: Look into `nexus-analyst-demo.acme.fact_subscriptions`. Are we capturing `change_type = 'downgrade'` correctly for those SMB accounts?
- [ ] Nina: Create a cohort analysis for users who signed up in Q4 2026. What’s their 30-day retention look like in `dim_users`?
- [ ] Lina: Check the `paid_at` column in `fact_invoices`. Some "Enterprise" invoices are marked as `status = 'open'` even though the wire transfer came through. 

---

---

## Week of 2027-02-08
**Updates:**
- David: `fact_user_events` schema updated. We're now seeing `device_type` populating. Early look shows 12% of runs are manually triggered via the mobile web view.
- Rajiv: "Tyrell Corp" MRR issue resolved. The delta was due to a legacy discount code that didn't expire correctly in the billing engine. Re-synced `fact_subscriptions`.
- Lina: Found the "Enterprise" invoice discrepancy. It was a currency conversion lag for the EMEA accounts.

**Discussion:**
- **dbt Freshness Alerts:** We’re getting hammered with alerts for `fact_workflow_runs` every morning at 4 AM. It looks like the Fivetran connector is hitting a rate limit on the production Postgres replica. Marcus is talking to the DBAs to see if we can move to a 2-hour sync window instead of 1-hour.
- **Board Prep:** Q1 Board meeting is coming up. The CFO wants a slide on "Net Revenue Retention" (NRR) by cohort. Specifically, he wants to see if the "Stark Industries" expansion last year is offsetting the SMB churn we're seeing in the "Pro" tier.
- **What is "Active"?** Big debate on the `#analytics-internal` channel. Does `is_active` in `dim_users` mean they logged in once, or they actually edited a workflow? Sales wants "Logged in last 30 days," but Product wants "Successfully completed 1+ workflow run." We need a standard definition before the board deck is finalized.

**Action Items:**
- [ ] Marcus: Investigate the 4 AM BigQuery job failure. Is it a resources issue in the `nexus-analyst-demo` project or just a timeout?
- [ ] Nina: Build the NRR waterfall chart. Use `nexus-analyst-demo.acme.fact_subscriptions` and join on `customer_id` from `dim_customers`.
- [ ] David: Create a view for "Power Users" defined as >50 `workflow_id` triggers per week in `fact_workflow_runs`.

---

## Week of 2027-02-15
**Updates:**
- Nina: OOO for the rest of the week (Skiing in Tahoe).
- Marcus: The coffee machine is finally getting the "Dark Roast" refill tomorrow. Peace is restored.

**Discussion:**
- **The "Stark Industries" Ghost:** Even after Nina's fix, Stark still isn't showing up in the "Global Sales" dashboard. It turns out they have a duplicate entry in `dim_customers` under the name "Stark Int." We need to merge these or at least map them in the `account_mapping` seed file.
- **VRS Status:** The "Variable Rate Schedule" project is stalling. Marketing wants to charge $0.05 per extra "step" in a workflow, but our `fact_workflow_runs` table only has `step_count` for successful runs. We don't have visibility into how many steps a *failed* run processed before it died.

**Action Items:**
- [ ] Lina: Check `nexus-analyst-demo.acme.fact_workflow_runs` for `status = 'error'`. Can we derive step count from the `error_code` or logs?
- [ ] David: Audit the `csm_employee_id` field in `dim_customers`. We have about 14 Enterprise accounts with `NULL` assignments. Rajiv thinks they belong to the new hire, but the hire date isn't in `dim_employees` yet.

---

## Week of 2027-02-22
**Updates:**
- Rajiv: Successfully migrated the `acquisition_channel` logic. We now know that 40% of our "Enterprise" leads are coming from the "Workflow Templates" SEO landing pages.
- Marcus: Desk moves are complete. Analytics is now adjacent to the snack bar. This is a high-traffic/high-noise zone. Noise-canceling headphones are a must.

**Discussion:**
- **Incident Report:** We had a data lag on Feb 20th. The `paid_at` timestamp in `fact_invoices` was stuck in "Pending" for 48 hours because of a Stripe API hiccup. If anyone was running revenue numbers over the weekend, they’re wrong. Please re-run.
- **Engagement Definition:** We’re going with "Product-Qualified Leads" (PQLs) as the new metric. A PQL = a "Free" tier user who has triggered at least 50 runs across 3 different `workflow_id`s in a 7-day period.

**Action Items:**
- [ ] Nina: Update the PQL dashboard to use the new definition. Path: `nexus-analyst-demo.acme.fact_workflow_runs` joined with `dim_users`.
- [ ] David: "Weyland-Yutani" is asking for a custom SLA report. They need `sla_uptime_pct` from `dim_plans` matched against their actual downtime (which we don't track in the warehouse yet). Lina, can we get a CSV upload for incident logs?
- [ ] Rajiv: Check `fact_subscriptions` for "Cyberdyne Systems". Their `mrr_usd` shows $0 but they are on the "Business" tier. This smells like another seat-count logic bug.

---

## Week of 2027-03-01
**Updates:**
- David: `device_type` data is clean. 22% of logins are mobile, but only 2% of workflow edits are. People just want to see if their stuff is running, they don't want to build on a phone. Shocker.
- Lina: Uploaded the `manual_incident_logs` table. You can now join this to `dim_customers` via `company_name` (sorry, no IDs yet).

**Discussion:**
- **Spring Cleaning:** We are deprecating the `legacy_customer_id` column in all tables by the end of the month. If your queries still use it, they will break. Transition to the UUID `customer_id`.
- **Amsterdam Office:** Team is complaining about the "Hot Desking" setup. Apparently, the Sales team is hogging all the window seats. Marcus is escalating to HR.

**Action Items:**
- [ ] Nina: Finish the Board Deck NRR slides. The CFO is breatheing down my neck.
- [ ] Rajiv: Investigate why `fact_user_events` has a spike in `event_type = 'password_reset_requested'` for "InGen" users. Security concern or just a bad UI change?
- [ ] Marcus: Check the dbt models for any hardcoded references to '2026'. We need to make sure the date logic is fully dynamic as we move deeper into 2027. Check `dim_dates` specifically.

---

## Week of 2026-03-15
**Updates:**
- Marcus: The dbt run failed last night because someone (Rajiv?) dropped a temporary table in the `nexus-analyst-demo.acme` dataset without updating the manifest. `fact_user_events` was stale for 4 hours. Fixed now, but please use the `_temp` suffix next time.
- Nina: "Umbrella Corp" is finally moving from Pro to Business. AE (Sarah) says they need the SSO features immediately. Rajiv, can you verify their `seat_count` in `fact_subscriptions` matches the 120 they signed for? 
- Lina: The new espresso machine is finally here. It’s in the Amsterdam breakroom. If you use the oat milk, please mark it on the fridge sheet so we can expense it properly.

**Discussion:**
- **VRS Status:** The "Visual Workflow Snapshot" (VRS) beta is launching for 10% of Enterprise customers next week. We need a way to track `event_type = 'vrs_preview_generated'` in `fact_user_events`. David, do we have the metadata fields for this yet?
- **Retention Deep Dive:** We're seeing a weird dip in NRR for the MM (Mid-Market) segment. Nina thinks it’s related to the "Pro" tier quota limits. If a user hits 10k runs, they just stop using the tool instead of upgrading. We might need a "Soft Cap" notification.

**Action Items:**
- [ ] David: Add `vrs_metadata` column to the events schema. 
- [ ] Rajiv: Check why "Tyrell Corp" has 400 active users but only 250 licensed seats in `dim_customers`. Is the seat-enforcement logic even on for them?
- [ ] Marcus: Clean up the `dim_dates` hardcoding. I saw a `WHERE year = 2025` in the `mrr_by_month` model. That’s going to bite us in 3 weeks.

---

## Week of 2026-03-22
**Updates:**
- Nina: Board prep is 80% done. Still need the "Land and Expand" chart for "Stark Industries" and "Wayne Enterprises". Their growth curves look like hockey sticks, and the CFO loves hockey sticks.
- David: Found a massive bug in `fact_workflow_runs`. Some `duration_ms` values are negative. Turns out some webhooks are coming in with timestamps from the future (client-side clock drift?). I’m adding a filter to `dbt` to null out anything where `triggered_at > current_timestamp()`.
- Rajiv: OOO Friday for a "long weekend" in Utrecht. Don't ping me unless the warehouse is literally on fire.

**Discussion:**
- **The "Hooli" Situation:** "Hooli" (Tier: Enterprise) is threatening to churn. They say the "priority support" isn't fast enough. Lina, can we pull `fact_support_tickets` (wait, is that in BQ yet?) and join it to `dim_customers` to see their average TTR (Time To Resolve)?
- **Schema Question:** Why is `acquisition_channel` in `dim_customers` a string instead of an ID? We have "Direct", "Organic", "Paid Social", and "Paid_Social" (with an underscore). It’s messing up the Marketing ROI report. Marcus, can we get a regex fix in the staging layer?

**Action Items:**
- [ ] Nina: Finalize the "Hooli" health score card.
- [ ] Marcus: Update `stg_customers` to normalize `acquisition_channel`. 
- [ ] David: Investigate the "negative duration" runs. If it's more than 0.5% of traffic, we need to talk to Eng about the event collector.

---

## Week of 2026-03-29
**Updates:**
- Lina: Incident logs for the Q1 outage are uploaded to `manual_incident_logs`. "Weyland-Yutani" was the hardest hit—they lost about 4 hours of workflow processing. David, they're asking for a credit. Check `fact_invoices` to see their last `amount_usd`.
- Rajiv: Back from Utrecht. The `fact_subscriptions` logic for "Cyberdyne Systems" is still broken. It’s definitely the seat-count logic. They are on "Business" ($149/seat) but the `mrr_usd` is being calculated as if they are on "Pro" ($49/seat). 

**Discussion:**
- **Engagement Definition (v2):** The PQL definition is working, but Sales says it’s too broad. They want to add "last_login_date < 3 days" to the filter. A "Free" user who runs 50 workflows but hasn't logged in for a week isn't a hot lead; they’ve just automated themselves out of the UI.
- **Office Move:** SF office is moving to the 4th floor in May. Start packing your non-essentials. Nina, does this mean we get more monitors?

**Action Items:**
- [ ] Rajiv: Fix the "Cyberdyne" MRR calculation. Check the `plan_tier` join in `fct_mrr_movements`.
- [ ] Nina: Update PQL definition in the `gold_pql_leads` table to include the 3-day login recency.
- [ ] Marcus: Run a freshness check on `nexus-analyst-demo.acme.fact_invoices`. Finance says the "Paid" status isn't updating fast enough.

---

## Week of 2026-04-05
**Updates:**
- David: `device_type` analysis is done for the board deck. 88% of our Enterprise users exclusively use Desktop. The mobile app is basically just an "On/Off" switch for workflows.
- Marcus: I've deprecated `legacy_customer_id`. If your Looker dashboards are broken, that's why. Swap to `customer_id` (the UUID).
- Nina: "InGen" password reset spike was just a "forgot password" loop caused by a cookie conflict on the new login page. Eng pushed a fix. Not a security breach. Phew.

**Discussion:**
- **Custom SLAs:** "Stark Industries" wants a 99.99% uptime guarantee for their custom workflows. Currently, `dim_plans` for Enterprise only says 99.9%. If we agree to this, we need to track it in a new table.
- **Spring Cleaning:** There are about 50 unused tables in the `acme` dataset. I'm going to start deleting everything with a `_test` or `_backup` suffix that hasn't been touched in 60 days. Speak now or forever hold your data.

**Action Items:**
- [ ] Lina: Reach out to "Stark Industries" CSM to clarify the SLA requirements.
- [ ] Rajiv: Create a view for "At-Risk Enterprise Accounts" (usage down >30% WoW). Path: `fact_workflow_runs` grouped by `customer_id` and `week`.
- [ ] David: Fix the `storage_gb` calculation in `dim_plans`. It's showing 0 for "Free" but it should be 1GB.

---

## Week of 2026-04-12
**Updates:**
- Nina: I’m OOO Thursday/Friday for a wedding. If the PQL pipeline breaks, just ping Marcus. I’ve updated the logic for "Stark Industries" in a temporary view: `nexus-analyst-demo.acme.stark_custom_sla_monitor`. It’s pulling from `fact_workflow_runs` where `error_code` is null.
- Rajiv: "At-Risk Enterprise" view is live. Bad news: we have 4 accounts in the MM tier that haven't run a single workflow since the 1st of the month. One of them is "Cyberdyne"—someone check if their API key expired.
- Marcus: The coffee machine on the 3rd floor is leaking again. Facilities says stop using the "Extra Bold" setting, it's too much for the gaskets.

**Discussion:**
- **dbt Freshness:** `fact_user_events` failed the freshness check this morning. It looks like the Segment webhook to BigQuery stalled around 02:00 UTC. David is looking into the `nexus-analyst-demo.acme.fact_user_events` source.
- **Amsterdam Office:** We’re officially doubling the headcount in EMEA by July. Any dashboards looking at `region = 'EMEA'` in `dim_customers` might see a spike in acquisition.
- **Seat Overages:** We have "Pro" users who have 10+ users but are only paying for 1 seat because of that legacy invite bug. We need to decide if we're going to back-bill or just force a plan update.

**Action Items:**
- [ ] David: Investigate the 02:00 UTC gap in `fact_user_events`.
- [ ] Lina: Reach out to the CSM for "Cyberdyne" (check `csm_employee_id` in `dim_customers`) to see why usage dropped.
- [ ] Rajiv: Create a "Seat Leakage" report. Join `fact_subscriptions` with `dim_customers` where `seat_count` < actual active users in `dim_users`.

---

## Week of 2026-04-19
**Updates:**
- Lina: The "Stark Industries" 99.99% SLA is signed. I need the Engineering team to confirm that our `duration_ms` in `fact_workflow_runs` includes the overhead for the webhook handshake. 
- Marcus: I've updated `dim_employees` to reflect the new hires in Amsterdam. If you're doing manager-rollups, the `manager_employee_id` field is now fully populated.
- Nina: Finished the "Spring Cleaning." Deleted 42 tables. If you were using `nexus-analyst-demo.acme.test_nina_2025_02_backup`, it's gone. Sorry (not sorry).

**Discussion:**
- **Board Prep (Q1 2026):** We need a final MRR number for the board by EOD Friday. David, can you pull the month-end snapshot from `fact_subscriptions` for March? 
- **Plan Migration:** We are sunsetting the "Legacy Pro" ($39/seat) and moving everyone to the current "Pro" ($49/seat). We need to track the "churn" this might cause.
- **Desk Move:** Reminder: SF office moves to 4th floor in 2 weeks. Boxes are in the kitchen. Label them with your `employee_id` because the movers are using a lookup table (seriously).

**Action Items:**
- [ ] David: Export the Q1 MRR growth chart. Use `nexus-analyst-demo.acme.fact_mrr_movements` (don't use the raw invoices, too messy with the credits).
- [ ] Nina: Build a "Migration Risk" dashboard for the Sales team. Filter for `current_plan_tier = 'Pro'` and `acquisition_channel = 'Organic'`.
- [ ] Rajiv: Fix the `is_business_day` flag in `dim_dates`. It missed the bank holiday last Monday.

---

## Week of 2026-04-26
**Updates:**
- Rajiv: Found a bug in the `storage_gb` calculation for the "InGen" account. It was double-counting their sandbox environment. Fixed in the transformation layer, so `dim_plans` should look correct now.
- David: Q1 Board deck is 90% done. I’m seeing a weird trend where `account_tier = 'SMB'` is actually outperforming `MM` in terms of workflow retention. 
- Marcus: The "Cyberdyne" issue was resolved. Turns out they were testing a new firewall that blocked our outbound IPs. Usage is back up to 50k runs/day.

**Discussion:**
- **PQL Definitions:** Marketing wants to add "Invite Sent" to the PQL score. I think we should wait. Just because a "Free" user invites 10 people doesn't mean they're going to pay; usually it just means they're trying to bypass the 2 active workflow limit.
- **Warehouse Performance:** Query costs on `fact_workflow_runs` are spiking. We need to start enforcing a `triggered_at` partition filter on every query. If you're running `SELECT *`, stop it. 
- **New Coffee Machine:** The 4th floor has a built-in espresso bar. Nina is already planning a "Data & Decaf" social for the first Friday in May.

**Action Items:**
- [ ] Marcus: Implement a dbt test to catch `seat_count` mismatches in `fact_subscriptions`.
- [ ] Nina: Update the PQL model in `gold_pql_leads` to include a weight for `country = 'US'` vs `region = 'EMEA'`. 
- [ ] Lina: Send the "Stark Industries" uptime report to their Ops lead. Path: `nexus-analyst-demo.acme.fact_workflow_runs` where `customer_id` is 'c_stark_001'.

---

## Week of 2026-05-03
**Updates:**
- David: Final board numbers are in. ARR is at $39.2M. We're slightly under the $40M goal, but the "Enterprise" pipeline looks heavy for Q2.
- Nina: I'm seeing some `null` values in `industry` in `dim_customers`. It looks like the Salesforce sync is dropping the picklist values for new signups.
- Rajiv: Moving today! I'll be offline from 12:00 PM onwards. See you on the 4th floor.

**Discussion:**
- **Data Freshness:** `fact_invoices` is lagging again. "Paid" statuses from yesterday aren't showing up. Finance is complaining that they can't close the month. Marcus is checking the Stripe-to-BigQuery connector.
- **Workflow Errors:** "InGen" is hitting a lot of `error_code = 'TIMEOUT_EXCEEDED'`. Is this a platform issue or are they just running massive scripts?

**Action Items:**
- [ ] Marcus: Fix the `fact_invoices` sync.
- [ ] David: Analyze "InGen" error codes in `fact_workflow_runs`. Check `duration_ms` distribution.
- [ ] Nina: Audit the `industry` field in `dim_customers` and manually map the top 20 missing accounts.

## Week of 2026-05-10
**Updates:**
- Nina: I’ve manually mapped the `industry` for the top 20 accounts. Most were "Technology" or "Manufacturing". If you see `null` in `dim_customers` for new Enterprise leads, ping me.
- Rajiv: Moving went well! Only broke one monitor. I'm back and catching up on the InGen expansion.
- Marcus: The Stripe-to-BigQuery connector is back in sync. `fact_invoices` is current as of 2 hours ago. Finance should be able to see the May 1-7 collections now.

**Discussion:**
- **dbt Freshness Alert:** `fact_user_events` is failing its freshness check (6 hour threshold). It looks like the segment-to-warehouse pipeline is bottlenecked at the `event_at` timestamp processing. Marcus is looking at the `nexus-analyst-demo.acme.fact_user_events` raw ingestion logs.
- **InGen Follow-up:** David’s analysis showed InGen (c_ingen_002) is running loops with `step_count > 500` which is hitting our 300s timeout. Lina, we need to tell them to refactor their "Bio-Sync" workflow into smaller sub-workflows.
- **Office Noise:** Someone keeps leaving the 4th-floor espresso machine on "steam" mode. Please turn it back to "brew" when you're done.

**Action Items:**
- [ ] Lina: Schedule a call with InGen’s lead dev to discuss workflow optimization. 
- [ ] Marcus: Optimize the `fact_user_events` incremental load logic.
- [ ] Nina: Build a "Top 10 High-Volume Workflows" dashboard for CS to monitor potential stability risks.

---

## Week of 2026-05-17
**Updates:**
- David: Q2 Board deck is 70% done. I need the final churn bridge by Friday.
- Lina: "Weyland-Yutani" (c_weyland_003) is asking for a SOC2 report. David, can you point them to the Trust Center?
- Rajiv: Signed "Umbrella Corp" for a 50-seat Business pilot. They’re coming in through the EMEA office.

**Discussion:**
- **Metric Definition - "Active User":** We are seeing a discrepancy between `dim_users.is_active` and our internal "Monthly Active User" (MAU) reporting. Nina found that `is_active` just means "not deleted," whereas Marketing thinks it means "logged in recently." We should probably align on using `last_login_date` from `nexus-analyst-demo.acme.dim_users` for all board reporting.
- **Expansion Logic:** Rajiv is seeing "Pro" customers with 45 seats who aren't being flagged as MM (Mid-Market) leads. We need to check if `account_tier` in `dim_customers` is updating based on `seat_count_licensed` or just the initial signup plan. 

**Action Items:**
- [ ] Nina: Update the MAU definition in the `gold_monthly_metrics` table to use a 28-day rolling window on `last_login_date`.
- [ ] Marcus: Investigate why "Umbrella Corp" isn't showing up in `dim_customers` yet. Sync lag?
- [ ] Rajiv: Check if Weyland-Yutani has any pending `fact_invoices` before we give them the SOC2.

---

## Week of 2026-05-24
**Updates:**
- Marcus: OOO Thursday/Friday for a long weekend. No deployments after Wednesday morning, please. 
- Nina: I updated the `gold_pql_leads` model. US-based signups now have a 1.5x multiplier on their score if they reach the 2-workflow limit within 48 hours.
- David: ARR is holding steady at $39.4M. Churn was lower than expected for April—shoutout to the CS team.

**Discussion:**
- **The "Free Tier" Leak:** We found 15 customers on the "Free" tier who have over 20 users. They are bypassing the seat limits by creating multiple "Free" organizations and using the same domain. Nina suggests we aggregate `dim_users` by `email_domain` to find these clusters.
- **VRS Status:** The "Variable Rate Schedule" project for Enterprise billing is still blocked by the lack of `duration_ms` granularity in `fact_workflow_runs`. We need more precise numbers if we're going to charge per execution second.

**Action Items:**
- [ ] Marcus: Add `avg_duration_ms` and `p95_duration_ms` to the daily summary of `fact_workflow_runs`.
- [ ] David: Review the "Free Tier Leak" list Nina generated and decide if we want to force a merge or just let it slide for now.
- [ ] Lina: Check in with "Stark Industries" (c_stark_001). Their `seat_count` in `fact_subscriptions` dropped from 300 to 250 last week. Was that a downsell?

---

## Week of 2026-05-31
**Updates:**
- Rajiv: Closing the month strong. We might hit $39.8M ARR if the "Cyberdyne Systems" deal clears today.
- Nina: Data & Decaf social was a success! Thanks for the donuts, David. 
- Lina: I'll be in the Amsterdam office all next week. 

**Discussion:**
- **Schema Change:** We’re adding `acquisition_channel` to `dim_customers` to better track ROI on LinkedIn ads. The data will come from the `fact_user_events` where `event_type = 'signup'`.
- **Query Performance:** Someone ran a `SELECT *` on `nexus-analyst-demo.acme.fact_workflow_runs` without a date filter and it cost $40. Please, for the love of the budget, use `WHERE triggered_at > '2026-05-01'`. 

**Action Items:**
- [ ] Nina: Backfill `acquisition_channel` for the 2025 cohorts.
- [ ] Marcus: Set up a BigQuery alert for any query costing >$10.
- [ ] Rajiv: Update the "Cyberdyne" status in Salesforce so the `gold_pipeline` model picks it up.

---

## Week of 2026-06-07
**Updates:**
- Lina: High-fives from Amsterdam! The stroopwafels are dangerous. Meeting with "Globex Corp" (c_globex_99) tomorrow—they're asking about the SOC2 Type II report for their audit.
- Marcus: The BigQuery alert for high-cost queries is live. If you see a Slack ping in #ops-noise, that’s you.
- Nina: Fixed the `dim_users` logic for `last_login_date`. It was pulling from the session start instead of the heartbeat, so it was undercounting "active" users by about 4%. 

**Discussion:**
- **The "Cyberdyne" Whale:** Rajiv confirmed the deal closed at $450k ACV! But wait—the `fact_subscriptions` table shows them on a "Business" plan instead of "Enterprise." Marcus says it’s because the Salesforce-to-Stripe sync failed on the `seat_count` validation (they tried to provision 400 seats on a plan that caps at 300 in the legacy metadata). 
- **VRS Granularity:** Still struggling with `duration_ms`. Some runs show `0` because they finish in <1ms (mostly just webhooks firing off simple pings). Nina suggests we round up to `1ms` for billing purposes or we're leaving money on the table for the new Enterprise Variable Rate Schedule.

**Action Items:**
- [ ] Nina: Update the VRS model to `CEIL(duration_ms)` so we don't have 0-cent executions.
- [ ] Rajiv: Get the "Cyberdyne" contract signed-off in the portal so Legal stops bugging us.
- [ ] David: We need a volunteer to move desks for the new interns starting in July.

---

## Week of 2026-06-14
**Updates:**
- Rajiv: Pipeline is looking a bit thin for July. We need more leads from the "Summer Automation" webinar.
- Marcus: **Incident Report:** dbt Cloud failed last night because someone deleted a source table in the `raw_marketing` dataset. The `fact_user_events` backfill is paused. 
- David: The 2nd floor espresso machine is leaking again. Use the one in the cafeteria.

**Discussion:**
- **Engagement Definition:** We’re having a heated debate in #product-strategy. Is a "Monthly Active User" (MAU) someone who just logs in, or someone who actually modifies a workflow? Currently, `fact_user_events` counts any `event_type`. David wants a "Power User" flag in `dim_users` for people with >10 `workflow_edit` events per month.
- **Wayne Enterprises (c_wayne_007):** They’ve hit their 100k run quota three weeks early. Since they are on the Business tier, they shouldn't be hard-capped, but the UI is showing a "Quota Exceeded" warning. Nina, can you check `fact_workflow_runs` vs the `dim_plans.workflow_run_quota_per_month`?

**Action Items:**
- [ ] Nina: Create a view `v_over_quota_customers` to see who is hitting the ceiling.
- [ ] Marcus: Restore the `raw_marketing` permissions.
- [ ] Lina: (Back from AMS) Reach out to Wayne Enterprises about an "overage" talk—good expansion opportunity.

---

## Week of 2026-06-21
**Updates:**
- David: Board meeting is in 10 days. I need the final Q2 ARR numbers by Friday. 
- Nina: I’m seeing a weird discrepancy in `current_mrr_usd` for "Stark Industries" (c_stark_001). It says $12,500 but their `seat_count` is 250. At $149/seat (Business tier), it should be higher. 
- Marcus: The BQ cost alert triggered 5 times yesterday. All of them were Rajiv trying to export the entire `dim_customers` table to Google Sheets via the plugin. Rajiv, please use the Looker dashboard!

**Discussion:**
- **Churn Alert:** "Initech" (c_initech_42) just downgraded from Business to Pro. They cited "too much complexity." CS needs to investigate if this was a failure in onboarding or just a budget cut. 
- **Schema Request:** Marketing wants `is_internal_test_user` in `dim_users` to filter out all the @acme.com accounts from the ROI calcs. Marcus says we can just regex the `email_domain`.

**Action Items:**
- [ ] Nina: Finalize the "Board Deck" dashboard in Looker. Use `nexus-analyst-demo.acme.fact_subscriptions` as the source of truth for MRR.
- [ ] David: Review the Initech downgrade notes in the CRM.
- [ ] Rajiv: Stop running `SELECT *` without limits!

---

## Week of 2026-06-28
**Updates:**
- Rajiv: "Umbrella Corp" (c_umbrella_101) is in the final stages. $200k ACV. They want a custom SLA of 99.99%.
- Marcus: Warehouse is healthy. dbt run time is down to 14 minutes after I optimized the `fact_workflow_runs` incremental logic.
- Lina: It’s too hot in the Amsterdam office. We need more fans.

**Discussion:**
- **The "Free Tier" Migration:** We finally pulled the trigger on the domain-aggregation logic Nina built. We identified 22 "Free" organizations that are actually just different departments of "Soylent Corp." David wants to force them into a single "Business" account.
- **Variable Rate Schedule (VRS) Update:** We are moving forward with the "per-second" billing for Enterprise. Nina, we need a new table: `fact_billing_line_items` that joins `fact_workflow_runs` with the custom rates in the contracts.

**Action Items:**
- [ ] Nina: Draft the `fact_billing_line_items` model. 
- [ ] Marcus: Check if `triggered_by` in `fact_workflow_runs` can distinguish between "system" and "user" triggers for the Soylent Corp audit.
- [ ] David: Send the "Consolidation" email to the Soylent Corp admins. Prepare for some pushback.

---

## Week of 2026-07-05
**Updates:**
- Marcus: dbt freshness alert went off for `fact_user_events` on Friday night. It was a late-arriving Kinesis stream from the Sydney shard. Fixed now. 
- Nina: OOO for the first half of the week (Belated July 4th trip).
- Rajiv: "Globex Corp" (c_globex_202) is asking about the SOC2 Type II report. David, can you ping Legal?

**Discussion:**
- **Engagement Definition:** We’re still arguing over what "Active" means for the Board Deck. Product wants it to be "Created a Workflow" in the last 30 days, but David wants it to be "Logins" from `fact_user_events`. 
- **The "Soylent" Fallout:** As predicted, three of the Soylent Corp admins are annoyed about the consolidation. One of them claims they need separate invoices for "Tax reasons." Finance says no.
- **Office Noise:** The coffee machine on the 4th floor is leaking again. Please stop using the "Extra Foam" setting until the tech arrives.

**Action Items:**
- [ ] Marcus: Run a count of `user_id` in `nexus-analyst-demo.acme.fact_user_events` vs `triggered_by` in `fact_workflow_runs` to see the overlap.
- [ ] David: Follow up with the Soylent "Green" department lead. 
- [ ] Lina: Call the espresso machine repair guy.

---

## Week of 2026-07-12
**Updates:**
- Nina: I’ve started the `fact_billing_line_items` model. It’s a beast. I’m joining `fact_workflow_runs` on `customer_id` and a new `ref` to a CSV the AEs are maintaining for custom rates. 
- Rajiv: "Hooli" (c_hooli_99) is ready to move from Business to Enterprise. They have 400 seats they want to provision by EOM.
- Marcus: Warehouse costs spiked 15% last week. Someone is running a BI tool that doesn't have a limit on the `fact_user_events` scan. 

**Discussion:**
- **VRS Status:** We need to decide if we charge for "Failed" runs (error_code IS NOT NULL in `fact_workflow_runs`). Engineering says it's our fault if it fails, but Sales says if it’s a 400-level error (user config), we should charge.
- **The "Internal" Filter:** Marcus added `is_internal_test_user` to `nexus-analyst-demo.acme.dim_users` using a case statement on `email_domain = 'acme.com'`. Nina, please update the Looker Explores to default filter this to `false`.

**Action Items:**
- [ ] Nina: Update the MRR dashboard to exclude internal users from the seat counts.
- [ ] Rajiv: Get the Hooli contract signed so we can update `fact_subscriptions`.
- [ ] Marcus: Set up a BigQuery budget alert for the `nexus-analyst-demo` project.

---

## Week of 2026-07-19
**Updates:**
- David: Retention is looking good for July, but "Stark Industries" (c_stark_007) is showing low health scores. Their `run_count` dropped 60% after their main admin left.
- Marcus: Moving my desk to the window side. If you need me, I'm next to the dying fiddle-leaf fig.
- Lina: The Amsterdam office got the fans. Productivity is up 2%.

**Discussion:**
- **Schema Request:** Can we add `workflow_name` to `fact_workflow_runs`? Currently, we only have `workflow_id`, which is a UUID and means nothing to the CS team when they are troubleshooting with customers. 
- **The "Initech" Post-Mortem:** David reviewed the CRM. They downgraded because they couldn't figure out the "Loop" logic in the builder. We need a "How-to" video specifically for the Pro tier.

**Action Items:**
- [ ] Nina: Add a join to the (future) `dim_workflows` table in the billing model. 
- [ ] Rajiv: Reach out to the new admin at Stark Industries. Offer a training session.
- [ ] Marcus: Investigate if `dim_customers.acquisition_channel` is actually being populated for the 2026 cohorts. It looks like a lot of `NULL`s lately.

---

## Week of 2026-07-26
**Updates:**
- Rajiv: "Wayne Enterprises" (c_wayne_44) just hit their 100k run quota on the Business plan. They are only 12 days into the billing cycle. Upsell opportunity or just a runaway script?
- Nina: `fact_billing_line_items` is in staging. The numbers look... aggressive. I'm seeing some customers who would owe us $20k/mo just in overages.
- Marcus: dbt 1.8 upgrade is happening this weekend. Expect some downtime on the dashboards Saturday morning.

**Discussion:**
- **VRS Implementation:** We decided NOT to charge for `error_code` values 500-599. We will charge for 400-499 (user error). Nina, please update the logic in the billing model. 
- **Board Prep:** The Q2 board meeting is in two weeks. We need a clean cut of `current_mrr_usd` from `nexus-analyst-demo.acme.dim_customers` as of 2026-06-30. No "projected" numbers, please.

**Action Items:**
- [ ] David: Check the `fact_workflow_runs` for Wayne Enterprises. If it's a "List Users" loop that's infinite, we should probably waive the overage this once.
- [ ] Nina: Lock the Q2 Board Dashboard. No more changes to the underlying `fact_subscriptions` logic until after the meeting.
- [ ] Lina: We need more oat milk in the SF kitchen. The fridge is just full of LaCroix.

## Week of 2026-08-02
**Updates:**
- Marcus: Back from the dbt 1.8 upgrade. It wasn't as bad as I thought, but the `fact_workflow_runs` model took 4 hours to rebuild because of the volume from July. We need to look at partitioning that table by `triggered_at` in `nexus-analyst-demo.acme.fact_workflow_runs`.
- David: Checked the Wayne Enterprises (c_wayne_44) thing. It was definitely a runaway script—they had a "Get Ticket" node pointing to a "Update Ticket" node that re-triggered the same workflow. 1.2M runs in 48 hours. I've issued a one-time credit in Stripe, but we need to tell them to use a debounce filter next time.
- Nina: I’ve updated the logic for `fact_billing_line_items` to ignore error codes 500-599 as discussed. If it’s our infrastructure failing, the customer shouldn’t pay for the run.

**Discussion:**
- **SF Office Move:** Someone mentioned we might be moving to a bigger space in SoMa. Can we confirm if we’re getting more than one conference room? It’s impossible to book "The Matrix" or "Zion" lately.
- **Data Freshness:** Sales is complaining that `dim_customers.current_mrr_usd` is lagging behind the Salesforce dashboard. Rajiv noticed a $5k discrepancy for "Umbrella Corp" (c_umb_66). 
- **The "Engagement" Definition:** Marketing wants to redefine "Active User." Currently, we just look at `dim_users.last_login_date` within the last 30 days. Product wants to see at least one event in `fact_user_events` where `event_type = 'workflow_published'`. 

**Action Items:**
- [ ] Marcus: Propose a partitioning strategy for the `fact_workflow_runs` table. 
- [ ] Nina: Compare `fact_subscriptions.mrr_usd` against the raw Stripe export for the Umbrella Corp account. 
- [ ] David: Send the "Looping Best Practices" doc to the Wayne Enterprises admin.
- [ ] Lina: The coffee machine in the breakroom is leaking again. Please call the tech.

---

## Week of 2026-08-09
**Updates:**
- Rajiv: Stark Industries (c_stark_99) just added 45 more seats! They are officially moving from Pro to Business next month. This puts us $12k closer to the Q3 target. 
- Nina: Board prep is 90% done. I’ve locked the `fact_subscriptions` table in `nexus-analyst-demo.acme`. If anyone changes a model that feeds into this, I will personally revoke your BigQuery write access.
- Marcus: `dim_customers.acquisition_channel` is still showing 20% NULLs for new signups. I think the Segment trait isn't firing correctly on the "Plan Selected" page.

**Discussion:**
- **VRS Status:** We are seeing a lot of 403 errors in `fact_workflow_runs` for the "Gekko & Co" (c_gekko_01) account. They are trying to hit a restricted API. Since we are charging for 400-level errors, their bill is going to be huge. Rajiv, should we warn them?
- **Retention:** Churn was high in July. Mostly SMBs on the Pro plan. "Initech" (c_initech_02) was the big one. We need to look at `fact_user_events` for those customers in the 30 days leading up to churn. Was it a lack of logins or a high error rate?

**Action Items:**
- [ ] Rajiv: Check in with Gekko & Co. Let them know about the 403 spikes before the invoice generates.
- [ ] Nina: Finalize the "Gross vs Net Retention" slide for the board deck.
- [ ] David: Create a "Churn Analysis" dashboard looking at `error_code` distribution for churned vs. active accounts. 
- [ ] Marcus: Fix the Segment tracking code for the acquisition channel.

---

## Week of 2026-08-16
**Updates:**
- Marcus: OOO this Thursday/Friday for a wedding. If the pipeline breaks, ping Nina. 
- Nina: Board meeting went well. They liked the `current_mrr_usd` growth, but they had questions about the "Storage" costs. We aren't currently tracking `storage_gb` from `dim_plans` effectively in our actuals.
- Rajiv: "Globex Corporation" (c_globex_77) is asking for a SOC2 report. Do we have the 2026 version ready?

**Discussion:**
- **Schema Change:** We need to add `is_internal` to `dim_customers`. Right now, our testing accounts (like `c_acme_test_1`) are skewing the "average runs per customer" metrics.
- **Workspace Cleanup:** There are about 50 "Untitled" dashboards in the BI tool. I’m going to delete anything that hasn't been viewed in 60 days. Speak now or forever hold your peace.
- **The Kitchen:** Who keeps putting fish in the microwave? Seriously.

**Action Items:**
- [ ] Nina: Add a filter to the `fact_subscriptions` model to exclude `customer_id` values associated with internal test accounts.
- [ ] David: Follow up with "Tyrell Corp" (c_tyrell_88). Their `seat_count_licensed` is 500, but `dim_users` only shows 110 active users. They are vastly underutilizing.
- [ ] Marcus: Update the `dim_plans` table to include the new "Enterprise Plus" tier specs (unlimited storage).
- [ ] Lina: Post a "No Fish" sign in the kitchen. 

---

## Week of 2026-08-23
**Updates:**
- Nina: I found the MRR discrepancy Rajiv mentioned. It was a `change_type` error in `fact_subscriptions`. A customer downgraded and upgraded in the same day, and the logic didn't handle the overlapping `start_date`. Fixed now.
- David: "Cyberdyne Systems" (c_cyber_10) is seeing a huge spike in `duration_ms` on their workflows. It looks like the `nexus-analyst-demo.acme.fact_workflow_runs` table shows an average of 4500ms for them, while everyone else is at 800ms.
- Rajiv: New logo: "Soylent Corp" (c_soylent_21) just signed a Pro annual.

**Discussion:**
- **Metric Review:** Why does `dim_users.email_domain` have so many "gmail.com" entries for Business tier customers? Aren't we requiring corporate emails for SSO?
- **Feature Launch:** The "Workflow Branching" feature goes live next Tuesday. We need to make sure `fact_user_events` has a new event type for `branch_created`.

**Action Items:**
- [ ] Marcus: Check the SSO enforcement settings for the Business tier in the app config.
- [ ] Nina: Add the `branch_created` event to the event dictionary.
- [ ] David: Investigate the latency issue for Cyberdyne. Is it a specific integration or just their script complexity?
- [ ] Rajiv: Grab a few people for a "Soylent" welcome lunch on Wednesday.

## Week of 2026-08-30
**Updates:**
- Nina: dbt freshness alert on `fact_user_events` this morning. It looks like the Fivetran connector for the Segment logs stalled around 03:00 UTC. I manually re-synced, but `nexus-analyst-demo.acme.fact_user_events` might be missing some `event_at` data for the early morning batch.
- Marcus: Still OOO for the rest of the week (Burning Man, I think?). David is covering the SSO ticket for Business tier.
- Lina: The "No Fish" sign was ignored. I found a container of shrimp in the trash can under my desk. Please, people.

**Discussion:**
- **Engagement Definition:** Growth wants to change how we define "Active User" for the North Star metric. Currently, it’s just `last_login_date` in `dim_users`. They want it to be "executed at least one successful workflow run in the last 7 days."
- **Data Impact:** If we switch, the "Active User" count will likely drop by 20% because we have a lot of "observers" who just look at dashboards but don't build. Nina, can you run a quick query on `fact_workflow_runs` joined with `dim_users` to see the delta?
- **Desk Moves:** We are moving the Data team next to the Sales pit on Monday. Bring your noise-canceling headphones.

**Action Items:**
- [ ] Nina: Build a dev view comparing `is_active` (login-based) vs. a new `is_engaged` (run-based) flag.
- [ ] David: Check the `error_code` distribution for "Soylent Corp" (c_soylent_21). Their onboarding looks bumpy—lots of `ERR_403_AUTH`.
- [ ] Rajiv: Update the Q3 Board Prep slide with the revised "Enterprise Plus" projections.
- [ ] Everyone: Pack your desk stuff by Friday 4 PM. 

---

## Week of 2026-09-06
**Updates:**
- David: Investigated the Cyberdyne latency. It wasn't a script issue; they had a recursive loop in a "Branching" workflow that was hitting the API rate limit and retrying every 50ms. Fixed the `fact_workflow_runs` duration skew by capping the retry logic in the engine.
- Rajiv: Board prep is getting intense. The CFO found a discrepancy between the Stripe export and our `fact_invoices` table for August. It’s off by exactly $14,900.
- Nina: Found the $14.9k. It’s "Massive Dynamic" (c_massdyn_99). Their `status` in `fact_invoices` was marked `void`, but they actually paid via wire transfer, and Ops didn't update the warehouse record.

**Discussion:**
- **Metric Review:** `dim_customers.acquisition_channel` has a lot of `NULL` values for recent signups (about 15% of the August cohort). Is the UTM capture broken on the marketing site?
- **VRS (Value Realization Score):** Product wants to pilot the VRS model. We need to weight `step_count` from `fact_workflow_runs` more heavily than just the number of runs. A 50-step workflow is worth more to a customer than fifty 1-step heartbeats.

**Action Items:**
- [ ] Rajiv: Manually update the payment status for Massive Dynamic so the Board deck doesn't look like we're losing money.
- [ ] Lina: Reach out to Marketing (Sarah?) about the missing UTMs in the signup flow.
- [ ] Nina: Draft a `v_customer_health_score` view using `duration_ms` and `step_count`.
- [ ] Marcus: (Welcome back!) Please look at the SSO enforcement bug David was triaging.

---

## Week of 2026-09-13
**Updates:**
- Nina: I updated the `dim_plans` table. "Enterprise Plus" is now officially in the warehouse with `storage_gb` set to `9999` (placeholder for unlimited). 
- Marcus: SSO bug for Business tier is fixed. It was a regex fail on `email_domain` validation in the app config. "gmail.com" users can no longer bypass the corporate login requirement if the org has SSO enabled.
- David: "Tyrell Corp" (c_tyrell_88) finally responded. They want to downgrade to Pro because they "don't need the audit logs." We need to show them the `fact_user_events` volume to prove they're actually using the Enterprise-only features.

**Discussion:**
- **Incident Follow-up:** We had a 15-minute outage on Tuesday. The `fact_workflow_runs` table shows a massive spike in `status = 'FAILED'` around 14:00. Looks like a DB migration gone wrong.
- **Office:** The coffee machine is leaking again. There is a puddle near the server rack. Please don't step in it.

**Action Items:**
- [ ] David: Send the Tyrell Corp CSM the usage report showing their `audit_log_view` events.
- [ ] Nina: Add `is_business_day` filter to the automated Slack alert for MRR drops; I’m tired of getting paged on Saturdays for scheduled maintenance.
- [ ] Lina: Call the repair tech for the coffee machine (the one who actually fixed it last time, not the cheap guy).
- [ ] Rajiv: Review the "Enterprise Plus" seat count for "Weyland-Yutani" (c_weyland_42). They are asking for a volume discount.

---

## Week of 2026-09-20
**Updates:**
- Nina: `nexus-analyst-demo.acme.fact_subscriptions` now includes the `change_type` for the "Enterprise Plus" migration. We had 4 customers move up already. 
- Rajiv: Weyland-Yutani signed! $250k ACV. The `dim_customers.current_mrr_usd` should reflect this by tomorrow’s refresh.
- Marcus: I'm seeing weird `customer_id` values in `fact_user_events` that don't exist in `dim_customers` (e.g., `c_temp_999`). Probably shadow-test accounts from the QA team. I'm going to filter them out of the production models.

**Discussion:**
- **Schema Question:** Should we move `industry` from `dim_customers` to a separate lookup table? It’s getting messy with "Healthcare," "Health-Care," and "Medical" all meaning the same thing.
- **Engagement:** Following up on the "Active User" change—the run-based metric shows our "stickiness" (DAU/MAU) is actually much higher than we thought, even if the absolute number of users is lower. Marketing wants to use this in the next blog post.

**Action Items:**
- [ ] Nina: Create a mapping table for `industry` to clean up the data.
- [ ] David: Investigate why "Hooli" (c_hooli_54) has 0 runs in the last 48 hours. Did their API key expire?
- [ ] Lina: Clear out the fridge on Friday. Anything without a name tag is going in the bin. No exceptions.
- [ ] Marcus: Double-check the `storage_gb` logic in the billing engine for the new tier.

---

## Week of 2025-10-05
**Updates:**
- Nina: The `industry` mapping table is live! I’ve updated the `dim_customers` model to pull from the new `stg_industry_map`. "Health-Care" and "Medical" now both resolve to "Healthcare." Please check your reports; some charts might look different if they were relying on the old messy strings.
- David: Hooli (c_hooli_54) is back online. It wasn't an API expiry—they hit the `workflow_run_quota_per_month` for the Pro tier. They were doing 15k runs a month on a 10k limit. I pushed them to an Enterprise trial for 14 days so they don't lose service.
- Marcus: Pushed a fix for the `storage_gb` logic in `fact_subscriptions`. It was double-counting users who had both a base seat and a "power user" add-on. 

**Discussion:**
- **Desk Moves:** Marketing is moving to the 4th floor near the windows. Engineering is taking over the corner by the server room (the dry part, hopefully). Marcus, stop complaining about the lack of sunlight; you have three monitors.
- **Engagement Metric:** We’re seeing a spike in `event_type = 'workflow_export'` in `fact_user_events`. Is this a churn signal? Usually, when people export everything, they’re moving to a competitor. We need a Slack alert for any account with >50 exports in an hour.

**Action Items:**
- [ ] Rajiv: Check if "Initech" (c_initech_01) is using the export feature. They’ve been quiet lately.
- [ ] Nina: Investigate why `nexus-analyst-demo.acme.dim_users` has 400 orphans (users without a `customer_id`).
- [ ] Lina: We need more oat milk. The fridge is just soy and almond right now.
- [ ] David: Follow up with Hooli AE on the Enterprise conversion.

---

## Week of 2025-11-16
**Updates:**
- Marcus: `fact_workflow_runs` was lagging by 6 hours yesterday because of a massive surge in webhook events from "Cyberdyne Systems" (c_cyber_88). I’ve adjusted the BigQuery partition logic to handle the load better.
- Rajiv: Closed "Globex Corp" (c_globex_12). $120k ACV, 300 seats. They need the SOC2 report before they move out of staging.
- Nina: Source freshness alerts for `fact_invoices` are firing. It looks like the Stripe hook is failing to sync to the warehouse. Finance is seeing the data, but dbt isn't.

**Discussion:**
- **VRS (Volume Retention Score):** Product wants to introduce a new metric called VRS. It’s a weighted average of `step_count` and `duration_ms` from `fact_workflow_runs`. The idea is that short, simple runs are less "sticky" than complex multi-step flows. Marcus, can you look into the data distribution for this?
- **Board Prep:** Q4 board meeting is in three weeks. We need a clean pull of `current_mrr_usd` by `region` from `dim_customers`. 

**Action Items:**
- [ ] Marcus: Draft the VRS calculation model in the `sandbox` schema.
- [ ] David: Reach out to Tyrell Corp; their `audit_log_view` events have dropped to zero. Did they disable the feature or just stop using it?
- [ ] Lina: The radiator in the kitchen is making a high-pitched whistling sound. It's driving me insane.
- [ ] Nina: Fix the Stripe-to-BigQuery sync for invoices.

---

## Week of 2025-12-07
**Updates:**
- Nina: `fact_user_events` now includes `device_type`. Initial look at the data shows 15% of users are checking workflow status via mobile browser. Might be time to reconsider the mobile app roadmap.
- Rajiv: We have a "runaway" customer on a Pro plan. "Massive Dynamic" (c_massdyn_99) is doing 800k runs this month. They are effectively paying $0.0001 per run. We need to cap the Pro tier or force the upgrade to Business immediately.
- Marcus: I'm OOO for the rest of December starting Friday. If the dbt cloud runner fails, ping Nina.

**Discussion:**
- **Holiday Coverage:** Who is on call for the 25th? We need at least one person to watch the ingestion pipelines.
- **Office Party:** It's at the pub across the street on Thursday. No data talk allowed.

**Action Items:**
- [ ] David: Send the "upgrade or cap" email to Massive Dynamic. Mention the `min_seats` requirement for Business.
- [ ] Nina: Update the `dim_plans` table to reflect the new Enterprise SLA (99.99% for new contracts).
- [ ] Lina: Finalize the holiday gift boxes for the Enterprise CSMs to send out.

---

## Week of 2026-01-11
**Updates:**
- Nina: Happy New Year. The `nexus-analyst-demo.acme.fact_subscriptions` table saw a massive spike on Jan 1st due to renewals. I had to manually clear a few duplicates in the `change_type` column where the migration script ran twice.
- Rajiv: "Wayne Enterprises" (c_wayne_07) just upgraded to Enterprise. That’s another $150k. My quota for Q1 is looking good already.
- Marcus: Back from OOO. Looking at the VRS metric Nina started—the correlation between `step_count` and 30-day retention is actually 0.82. We should definitely surface this in the CSM dashboard.

**Discussion:**
- **Schema Mess:** `dim_customers` still has "null" for `acquisition_channel` on about 20% of the older records. Can we use the `invited_by_user_id` in `dim_users` to trace back the original signup?
- **Incident:** We had a 20-minute outage on Tuesday. `fact_workflow_runs` shows about 4,000 runs failed with `error_code = '500_INTERNAL_SERVER_ERROR'`. We need to issue service credits to the Business tier accounts.

**Action Items:**
- [ ] Nina: Generate a list of `customer_id`s affected by the Tuesday outage for the CS team.
- [ ] Marcus: Refine the VRS model and move it to `prod_models`.
- [ ] David: Check why `c_weyland_42` has a `current_mrr_usd` of $0 in the dashboard even though Rajiv said they signed.
- [ ] Lina: Someone left a moldy sandwich in the back of the fridge. I'm not touching it.

---

## Week of 2026-02-22
**Updates:**
- Nina: `fact_user_events` is getting huge. We’re hitting our BigQuery scan limits on the "all-events" dashboard. I’m going to create a summary table `fact_daily_user_summary` to speed things up.
- David: "Soyuz Corp" (c_soyuz_11) churned. They cited the lack of a Native Salesforce integration. I’ve updated `dim_customers.status` to 'churned' and set the `churn_date`.
- Marcus: The `dim_employees` table is now synced with the new HR system. All `csm_employee_id` mappings should be accurate now.

**Discussion:**
- **Coffee Machine:** It's broken again. The "cheap guy" Lina hired last time clearly didn't do a good job. We are all vibrating from caffeine withdrawal.
- **DAU/MAU:** The "stickiness" metric for the Enterprise tier is at an all-time high (65%). Pro tier is struggling at 22%. It seems the PLG motion is bringing in a lot of "one-and-done" users who set up a single workflow and never log back in.

**Action Items:**
- [ ] Rajiv: Review the "Pro" tier churn. Is there a specific `industry` that's dropping off?
- [ ] Lina: Call the *original* coffee tech. I don't care what it costs.
- [ ] Marcus: Help Marketing with the "State of Automation" data pull. They need the total `step_count` across the whole platform for 2025.
- [ ] Nina: Check if `fact_workflow_runs` is capturing the `triggered_by` correctly for webhook-based flows. It looks like it's defaulting to 'system'.

---

## Week of 2026-03-01
**Updates:**
- Nina: Fixed the dbt freshness alert on `fact_invoices`. It was a delay in the Stripe sync job. `nexus-analyst-demo.acme.fact_invoices` should be current as of 04:00 UTC today.
- Marcus: I've added `vrs_score` as a metadata field in my scratchpad table. I’m seeing a weird correlation where high `step_count` in `fact_workflow_runs` doesn't always equal high retention for SMB customers. Investigating.
- David: Closing out the "Weyland Corp" (c_weyland_42) data issue. It turns out Rajiv entered the contract as a "manual credit" first, so the `fact_subscriptions` table didn't pick up the MRR until the first invoice cleared. It's showing $12,500 now.

**Discussion:**
- **Board Prep:** Q1 board deck is due in two weeks. Rajiv needs "Net Revenue Retention" sliced by `account_tier` (SMB vs MM vs Ent). Nina, can you double-check the `change_type` logic in `fact_subscriptions`? We need to make sure 'downgrade' is being captured correctly.
- **Desk Moves:** Engineering is moving to the 4th floor. Data team is staying put, but we’re losing the corner desks to the new PM hires. 
- **Engagement Definition:** We need to agree on what "Active User" means for the board deck. Is it just a login, or do they have to trigger a workflow in `fact_workflow_runs`? 

**Action Items:**
- [ ] Marcus: Define "Active" and update the `dim_users` logic.
- [ ] Nina: Build the NRR (Net Revenue Retention) view for Rajiv. 
- [ ] David: Follow up with "Tyrell Corp" (c_tyrell_19). Their `seat_count_licensed` is 500 but they only have 12 users created. 
- [ ] Lina: The coffee machine tech said the part is "on backorder." I’m buying a bag of instant coffee. Don’t yell at me.

---

## Week of 2026-03-08
**Updates:**
- Marcus: VRS model (v2) is now running in the dev schema. It uses a weighted average of `last_login_date` from `dim_users` and total successful runs from `fact_workflow_runs` (where `status = 'success'`).
- Nina: I found a bug in `fact_user_events`. Webhook pings were being counted as `user_id = 'system'`, which was inflating our "Active User" counts for the Free tier. Fixed the filter.
- Rajiv: "Omni Consumer Products" (c_ocp_88) just upgraded to Enterprise. Nina, please ensure their `current_plan_tier` is updated in `dim_customers` by tomorrow so I can show the VP.

**Discussion:**
- **The "Incident":** Someone (won't name names, but check the BigQuery audit logs) ran a `SELECT *` on `fact_user_events` without a date partition. We just spent $400 on a single query. PLEASE use the `event_at` filter.
- **Office:** The instant coffee is terrible. David brought in a French Press, but now the sink is clogged with grounds. 

**Action Items:**
- [ ] David: Fix the sink or call the plumber.
- [ ] Marcus: Compare VRS scores for `c_soyuz_11` (before they churned) against current high-risk accounts.
- [ ] Nina: Add a `usage_quota_pct` column to the `fact_daily_usage` rollup. We need to alert CS when customers hit 90% of their `workflow_run_quota_per_month`.

---

## Week of 2026-03-15
**Updates:**
- David: OOO this week (Skiing in Tahoe).
- Nina: I've finished the NRR report. Enterprise is at 112%, but Pro is dragging us down at 88%. 
- Rajiv: We’re seeing a lot of "failed payment" statuses in `fact_invoices` for the `country = 'BR'` and `country = 'IN'` segments. Might be a 3D Secure issue with the payment gateway.

**Discussion:**
- **VRS Status:** Marcus’s model successfully predicted the "Cyberdyne Systems" (c_cyberdyne_7) contraction. They dropped from 200 seats to 50. If we had the VRS alerts 2 months ago, we might have saved it.
- **Data Catalog:** Lina wants us to start using documentation in dbt. I know, I know. Just do the descriptions for the `fact` tables at least.

**Action Items:**
- [ ] Marcus: Move VRS to `prod_models.fact_customer_health_score`.
- [ ] Nina: Investigate the payment failure rates in `fact_invoices`. Is it specific to a `billing_cycle`?
- [ ] Rajiv: Check with the EMEA team if "Stark Industries" (c_stark_3) is actually moving to the Business tier. They are currently on a custom Pro plan that doesn't exist in `dim_plans`.

---

## Week of 2026-03-22
**Updates:**
- Nina: `fact_workflow_runs` schema update—I added `triggered_by` as a top-level column to make the "system vs user" analysis easier. 
- Marcus: Total `step_count` for 2025 across all customers was 1.2 billion. Marketing is going to use "Over a Billion Tasks Automated" in the new campaign.
- Lina: New coffee machine arrives Friday. It has a touch screen. 

**Discussion:**
- **Schema Debt:** We have `customer_id` in some tables and `account_id` in others. We really need to standardize on `customer_id` across the `nexus-analyst-demo.acme` dataset. 
- **PLG Motion:** There's a huge spike in `acquisition_channel = 'viral'` for the Free tier. It looks like it’s coming from a specific YouTube tutorial. 

**Action Items:**
- [ ] Rajiv: See if we can get an AE assigned to the top 10 Free accounts by `step_count` from this "viral" spike.
- [ ] Marcus: Update the looker dashboard to point at the new `triggered_by` column.
- [ ] Nina: Check why `dim_employees.is_active` is showing `false` for three people in the Sales team who definitely still work here. HR system sync might be broken.

## Week of 2026-03-29
**Updates:**
- Nina: dbt freshness alerts are firing for `fact_user_events`. It looks like the Fivetran connector for the segment logs is hanging. I’m manually re-running the sync now.
- Rajiv: "Wayne Enterprises" (c_wayne_1) is currently at 98% of their `workflow_run_quota_per_month`. They are on the Business tier (100k runs) and they’re going to hit the ceiling by Wednesday. 
- Marcus: Pushed a fix for the `fact_subscriptions.change_type` logic. It was incorrectly tagging 'downgrade' when seats stayed the same but MRR dropped due to a legacy discount expiring.

**Discussion:**
- **Engagement Definition:** We need to align on what "Active User" means for the board deck. Is it just a row in `dim_users` where `last_login_date` is > today - 30, or do they have to have a record in `fact_workflow_runs`? Currently, we have ~16k active in the last 28d, but only ~11k actually triggered a workflow. 
- **VRS logic:** The "Value Realization Score" is still heavily weighted on `step_count`. We should probably add a weight for `storage_gb` usage for the Enterprise tier.

**Action Items:**
- [ ] Nina: Fix the Fivetran connector for `fact_user_events`. 
- [ ] Rajiv: Reach out to the contact at Wayne Enterprises (c_wayne_1) about the quota overage. 
- [ ] Marcus: Draft a new SQL snippet for "Core Active Users" (Logins + Runs) for Lina to review.
- [ ] All: Don't forget the "Bring Your Pet to Zoom" thing on Thursday. Marcus, please don't bring the lizard.

---

## Week of 2026-04-05
**Updates:**
- Lina: Board deck prep starts now. I need the Q1 ARR walk finalized in `nexus-analyst-demo.acme.fact_subscriptions`.
- Marcus: VRS alert triggered for "Initech" (c_initech_5). Their health score dropped from 82 to 45 because their `step_count` plummeted after they migrated some of their HR workflows to a different tool. 
- Nina: I found ~200 rows in `dim_customers` where `ae_employee_id` is NULL but `account_tier` is 'MM' or 'Ent'. This messes up the commission reporting.

**Discussion:**
- **The Coffee Machine:** It’s leaking. Someone put oat milk in the water reservoir? Who does that?
- **Data Catalog:** Rajiv finally started adding descriptions to `dim_plans`. Thank you! Please keep going with `fact_invoices`.

**Action Items:**
- [ ] Rajiv: OOO for the rest of the week (hiking in Zion). 
- [ ] Nina: Batch update those NULL `ae_employee_id` values. Check the `acquisition_channel` to see if they should have been assigned to the "Inbound" pod.
- [ ] Marcus: Deep dive into "Initech" (c_initech_5). See if they are still using the SSO feature (Business tier). If not, they are a high churn risk for next month.

---

## Week of 2026-04-12
**Updates:**
- Marcus: "Globex Corp" (c_globex_9) just upgraded from Pro to Business. 120 seats. Big win for the EMEA team.
- Nina: Cleaned up `dim_employees`. The Sales team sync issue was a mapping error in the HRIS connector. `is_active` should be correct now. 
- Rajiv: (Back from Zion) I’m looking at the `fact_workflow_runs` errors from Tuesday. We had a 15-minute window where `status = 'error'` spiked for `triggered_by = 'webhook'`. 

**Discussion:**
- **Schema Debt:** We have `amount_usd` in `fact_invoices` but `mrr_usd` in `fact_subscriptions`. Finance gets confused because `amount_usd` includes one-time setup fees that shouldn't count toward ARR. 
- **Incident Follow-up:** The webhook lag was caused by a database lockup on the production side. It’s reflected in the `duration_ms` column—average duration for affected runs went from 200ms to 8500ms.

**Action Items:**
- [ ] Nina: Create a view `v_mrr_clean` that excludes setup fees from `fact_invoices` for easier reporting.
- [ ] Marcus: Update the VRS model to account for the webhook incident so we don't flag healthy customers as "at risk" just because of our internal lag.
- [ ] Rajiv: Pull a list of all `customer_id`s affected by the Tuesday incident so CS can send "we're sorry" emails. Start with "Umbrella Corp" (c_umbrella_2) since they are Enterprise.

---

## Week of 2026-04-19
**Updates:**
- Nina: New column in `dim_customers`: `is_strategic_account` (boolean). This is a manual flag from the VP of Sales.
- Marcus: Total MRR for `current_plan_tier = 'Enterprise'` crossed $500k/mo this week. 
- Lina: The coffee machine is officially dead. We are back to the French press until the replacement parts arrive.

**Discussion:**
- **Product-Led Growth (PLG):** We're seeing a lot of `Free` tier users from `email_domain = 'gmail.com'` who have a `step_count` > 500. We should probably prompt them with a "Pro" trial in-app. 
- **Customer Deep Dive:** "Hooli" (c_hooli_4) added 150 seats but their `fact_user_events` show only 10% of those seats have logged in. We need to check if they are having trouble with the SSO setup.

**Action Items:**
- [ ] Rajiv: Check `fact_workflow_runs` for "Hooli" (c_hooli_4). Are they actually running anything, or just provisioned?
- [ ] Nina: Update the `nexus-analyst-demo.acme.dim_users` table to include a `is_sso_enabled` flag if possible.
- [ ] Marcus: Run a query to find all 'Free' accounts with `step_count` > 500 in the last 30 days.

---

## Week of 2026-04-26
**Updates:**
- Marcus: April month-end close is looking good. Preliminary ARR is $39.2M. 
- Rajiv: "Stark Industries" (c_stark_3) finally moved from their "Custom Pro" plan to the standard Business tier. I’ve updated `fact_subscriptions` to reflect the `change_type = 'upgrade'`.
- Nina: Sprint retro today at 4 PM. We’re discussing why the `fact_workflow_runs` partitioning by `triggered_at` is still so slow. 

**Discussion:**
- **Desk Moves:** Marketing is moving to the 4th floor. Engineering is taking over their old desks. Please clear your monitors by Friday.
- **Data Quality:** We have a few `customer_id`s in `fact_invoices` that don't exist in `dim_customers`. It’s likely ghost records from the 2023 legacy system. I’m going to filter them out of the production models.

**Action Items:**
- [ ] Nina: Finalize the `fact_invoices` cleanup.
- [ ] Rajiv: Assist Marcus with the Q1 Board Deck visualizations. We need a "Seats per Account" trend line for the `Enterprise` vs `Business` tiers.
- [ ] Marcus: Investigate the `null` error codes in `fact_workflow_runs`. About 5% of errors have no code, which makes troubleshooting impossible.

---

## Week of 2026-05-03
**Updates:**
- Nina: Heads up, the dbt freshness check for `nexus-analyst-demo.acme.fact_user_events` failed this morning. It looks like the Fivetran connector for the event logs lagged by 4 hours. It’s caught up now, but your dashboards might have looked thin around 9 AM.
- Rajiv: Finished the "Seats per Account" analysis for Marcus. Interesting finding: "Wayne Enterprises" (c_wayne_1) has 400 seats but only 210 are actually mapped to a `user_id` in `dim_users`. We're leaving money on the table or they haven't finished their rollout.
- Marcus: Board deck is 90% done. I just need the final `current_mrr_usd` aggregated by `region` from `dim_customers`. 

**Discussion:**
- **The "Engagement" Definition:** We keep debating what an "Active User" is. Product wants it to be any event in `fact_user_events`, but Finance wants it to be at least one `workflow_run_id` in `fact_workflow_runs`. We need to align before the board meeting or the numbers won't match.
- **Office:** The 4th-floor coffee machine is leaking. Please use the one in the breakroom near the elevators until the tech arrives on Tuesday.
- **VRS Status:** The Variable Rate Subscription project is pushed to Q3. Nina needs to focus on the `fact_invoices` partitioning first.

**Action Items:**
- [ ] Nina: Investigate why `step_count` is sometimes returning negative values for specific webhook triggers. 
- [ ] Rajiv: Reach out to the CSM for Wayne Ent (c_wayne_1) about those 190 unprovisioned seats.
- [ ] Marcus: Send the draft Q1 deck to the exec team for a sanity check.

---

## Week of 2026-05-10
**Updates:**
- Nina: I’ve added the `is_sso_enabled` flag to `nexus-analyst-demo.acme.dim_users`. It’s joining against the `auth_logs` metadata. Note: it only populates for users created after Jan 2025.
- Marcus: OOO this Thursday/Friday for a wedding. If you need anything for the May mid-month forecast, get it to me by Wednesday noon.
- Rajiv: "Globex Corp" (c_globex_6) is asking about their `workflow_run_quota_per_month`. They hit 95k runs on a 100k limit. We should probably pitch them on the Enterprise upgrade.

**Discussion:**
- **Data Quality:** Found a bunch of records in `fact_subscriptions` where `end_date` is before `start_date`. Looks like a bug in the manual override tool the AEs use. I'm going to add a dbt test to catch this.
- **Incident Follow-up:** The `null` error codes Marcus mentioned last week? It turns out those are "Success" states that were being logged incorrectly as errors in the source API. Fixed in the transformation layer now.

**Action Items:**
- [ ] Rajiv: Run a list of all `Business` tier customers where `workflow_run_count` > 90% of quota. Send to Sales.
- [ ] Nina: Fix the `end_date` logic in the subscription model.
- [ ] All: Don't forget to submit your expense reports by the 15th!

---

## Week of 2026-05-17
**Updates:**
- Rajiv: "Stark Industries" (c_stark_3) is complaining about latency in their EMEA workflows. I checked `fact_workflow_runs` and `duration_ms` is averaging 12s compared to the global average of 2s. 
- Nina: Sprint 42 started. Main goal is migrating the `fact_user_events` table to an incremental model to save on BQ costs. 
- Marcus: Preliminary May ARR is tracking at $39.8M. We might hit $40M by June if the "Hooli" (c_hooli_4) expansion closes.

**Discussion:**
- **Schema Change:** We’re thinking about adding `industry` to `dim_customers`. Right now it’s just a messy string field. Thinking about forcing a dropdown in the CRM so we can actually report on "SaaS" vs "Manufacturing."
- **Social:** Team lunch at the taco place on Wednesday. Rajiv’s treat because he lost the fantasy football bet.

**Action Items:**
- [ ] Nina: Check the `region` distribution in `fact_workflow_runs` for c_stark_3. Is it just their London office or everyone?
- [ ] Marcus: Update the `dim_plans` table to reflect the new `storage_gb` limits for the Pro tier.
- [ ] Rajiv: Review the `acquisition_channel` data. "Referral" seems way too high; I suspect it’s the default for when the UTM is missing.

---

## Week of 2026-05-24
**Updates:**
- Nina: Happy (early) Memorial Day! I'm taking Friday off. The `nexus-analyst-demo.acme.fact_invoices` table is now fully cleaned and historical ghost records are moved to `stg_legacy_invoices`.
- Rajiv: Finalizing the "Churn Risk" dashboard. Customers with `last_login_date` > 30 days ago in `dim_users` are now being flagged automatically for CSMs.
- Marcus: Just realized the `current_mrr_usd` in `dim_customers` doesn't include the latest discounts applied in `fact_subscriptions`. I need to rewrite that join.

**Discussion:**
- **Workspace Cleanup:** The "Marketing moving to 4th floor" thing is happening this weekend. If your monitors aren't labeled, they’re going into the storage closet.
- **Performance:** BQ costs spiked last Tuesday. It was a `SELECT *` on `fact_user_events` without a date filter. Please, for the love of God, use the `event_at` partition. 

**Action Items:**
- [ ] Rajiv: Cross-reference `dim_customers.csm_employee_id` with `dim_employees` to see who has the highest churn rate.
- [ ] Marcus: Re-calculate the MRR including discounts so we don't over-report to the board.
- [ ] Nina: Set up a "BigQuery Budget Alert" for the dev project.

---

## Week of 2026-06-01
**Updates:**
- Nina: I’m back from the long weekend. I saw the dbt freshness alerts for `nexus-analyst-demo.acme.fact_workflow_runs`. It looks like the Amsterdam collector lagged by 6 hours on Sunday. Checking the logs now, but the data seems to have caught up.
- Marcus: Still waiting on Legal for the Hooli expansion (`c_hooli_4`). They’re arguing over the `sla_uptime_pct` in the Enterprise contract. I updated `dim_plans` with the latest SOC2 compliance notes for the Business tier.
- Rajiv: Quick win—I cleaned up the `email_domain` field in `dim_users`. No more "gmail.com" showing up as a "Company" in our internal lead reports.

**Discussion:**
- **Metric Definition:** What actually constitutes an "Active Workflow"? Currently, we count anything with a record in `fact_workflow_runs` in the last 30 days. Sales wants to change this to "Workflows with >5 successful runs" to weed out the test/fail noise.
- **Office:** The new coffee beans are way too dark. Can we go back to the Blue Bottle subscription?
- **Quarter End:** We are 30 days out from the end of Q2. Board deck prep starts next week. Nina, we need the "Land vs Expand" MRR split from `fact_subscriptions` ready by Wednesday.

**Action Items:**
- [ ] Nina: Investigate the Amsterdam collector lag. Is it a `duration_ms` reporting issue or a networking hiccup?
- [ ] Marcus: Pull the list of "Free" tier customers who have exceeded their 100 runs/mo quota in `fact_workflow_runs` for the Sales "Nudge" campaign.
- [ ] Rajiv: Update the `dim_customers.industry` mapping for the top 50 Enterprise accounts. 

---

## Week of 2026-06-08
**Updates:**
- Marcus: I’m OOO this Thursday/Friday for a wedding. If the `fact_invoices` pipeline breaks, ping Rajiv. 
- Rajiv: I found why `current_mrr_usd` was looking wonky. We had three customers in `fact_subscriptions` with overlapping `start_date` and `end_date` because of a mid-month tier upgrade. I’ve adjusted the `is_current` logic to favor the higher `mrr_usd` record.
- Nina: Board prep is 80% done. Total ARR is hovering around $39.2M. The "Business" tier growth is carrying us this quarter.

**Discussion:**
- **PQL Definition:** We need a "Product Qualified Lead" flag in `dim_customers`. Current proposal: Any Free/Pro customer who has `step_count` > 20 in a single workflow run or has invited > 3 users in `dim_users`.
- **Engagement:** We have 16,000 active users in the last 28 days, but `last_login_date` is missing for about 5% of them. Probably the API-only users. Should we exclude `role = 'api_service_account'` from the active user count?

**Action Items:**
- [ ] Rajiv: Filter out service accounts from the "Daily Active Users" dashboard.
- [ ] Nina: Finalize the "Logo Churn" vs "Revenue Churn" slide for the board deck.
- [ ] Marcus: Check if `c_stark_3` (Stark) has updated their `seat_count_licensed`. They look over-provisioned.

---

## Week of 2026-06-15
**Updates:**
- Nina: **INCIDENT REPORT.** On Sunday, `fact_user_events` failed to partition because of a schema mismatch in the raw JSON. About 4 hours of data was dumped into the `stg_events_deadletter` table. I’m re-running the backfill now.
- Rajiv: The desk move was a disaster. My monitors are missing and I’m sitting next to the Marketing team now. It's very loud. 
- Marcus: Great news—the Hooli expansion (`c_hooli_4`) officially closed. `current_plan_tier` is now `Enterprise`. I'll update the record in `dim_customers` manually if the sync doesn't hit by 5 PM.

**Discussion:**
- **Data Quality:** We are seeing a lot of `null` values for `country` in `dim_customers`. It’s making the "Revenue by Region" chart look like 20% of our money comes from "Unknown." Can we force a Geo-IP lookup on the signup flow?
- **Performance:** `SELECT`ing from `nexus-analyst-demo.acme.fact_user_events` is getting slow again. We need to enforce a mandatory filter on `customer_id` for any query that isn't a global admin report.

**Action Items:**
- [ ] Nina: Finish the backfill for Sunday’s events.
- [ ] Rajiv: Map the "Unknown" countries using the `email_domain` from `dim_users` where possible (e.g., .de = Germany).
- [ ] Marcus: Send the Hooli expansion gift basket (the one with the fancy nuts).

---

## Week of 2026-06-22
**Updates:**
- Rajiv: I updated the "Churn Risk" dashboard. Customers with `error_code` frequency > 10% in `fact_workflow_runs` are now flagged red. Stark (`c_stark_3`) is currently glowing red because of a broken Slack integration.
- Nina: I’m looking into the `acquisition_channel` weirdness. A lot of "Direct" traffic is actually coming from our LinkedIn ads but the UTMs are being stripped by some browsers. 
- Marcus: Board deck is finished. Final ARR for the deck is $39.8M. So close to $40M! 

**Discussion:**
- **New Table:** Thinking about creating `fact_support_tickets` and joining it on `customer_id`. It would be great to see if high-MRR customers are also our highest-ticket-volume customers.
- **Summer Fridays:** Don't forget Summer Fridays start next week! The data warehouse will still be running, but we won't be responding to Slack after 1 PM.

**Action Items:**
- [ ] Marcus: Reach out to the CSM for Stark (`c_stark_3`) regarding those workflow errors. 
- [ ] Nina: Set up a meeting with the Growth team to fix the UTM stripping issue.
- [ ] Rajiv: Prototype the `fact_support_tickets` table using the Zendesk export.

## Week of 2026-06-29
**Updates:**
- Rajiv: OOO Monday-Wednesday for his sister's wedding. I'll be checking Slack intermittently but don't expect any BigQuery heavy lifting until Thursday.
- Nina: `dbt` freshness alerts are firing on `nexus-analyst-demo.acme.fact_user_events`. It looks like the Fivetran connector hung on Sunday night. I manually re-ran the sync, but the last 4 hours of Sunday are still missing in the FLAT table. 
- Marcus: Quarterly Business Review (QBR) prep is starting. I need a pull of all Enterprise customers who haven't run a workflow in the last 14 days. 

**Discussion:**
- **Engagement Definition:** We need to align on what "Active" actually means. Right now, `dim_users.is_active` just looks at the `last_login_date`. Engineering wants to move to "Action-Based Active" (running at least one workflow per week). If we switch, our WAU (Weekly Active Users) will drop by 15%. Are we ready to explain that to the board?
- **VRS Status:** The "Volume-Based Revenue Sync" (VRS) is still buggy. Some Business tier customers are being overcharged because the `step_count` in `fact_workflow_runs` is being double-counted on retries.
- **Office Noise:** Someone left a tuna sandwich in the micro-fridge over the weekend. The whole 3rd floor smells like a wharf. Please clear your stuff out by Friday.

**Action Items:**
- [ ] Nina: Investigate the `step_count` logic in `fact_workflow_runs` to exclude `error_code` retries.
- [ ] Rajiv: (Once back) Update the `WAU` dashboard to include a toggle for "Login-only" vs "Execution-active."
- [ ] Marcus: Ping the DevOps team about the Fivetran timeout.

---

## Week of 2026-07-06
**Updates:**
- Rajiv: I'm back. I've started the prototype for `fact_support_tickets`. I’m seeing a weird trend where `Pro` tier users (especially those on the $49/seat plan) open 3x more tickets than `Enterprise` users. 
- Nina: I fixed the Sunday backfill. `nexus-analyst-demo.acme.fact_user_events` should be 100% complete now. 
- Marcus: The Hooli (`c_hooli_789`) expansion is officially live! They added 150 seats. Their `current_mrr_usd` in `dim_customers` should reflect the jump by tomorrow’s refresh.

**Discussion:**
- **Schema Question:** Why is `industry` in `dim_customers` a free-text field? We have "Fintech," "Fin-tech," and "Financial Services." We need to normalize this to a set of enums or our "Revenue by Industry" report is useless.
- **Desk Moves:** Marketing is moving to the 4th floor. If you need Nina or the Growth team, they’ll be by the windows now.
- **Coffee Machine:** The Jura is leaking again. Please use the pour-over station until the technician comes on Wednesday.

**Action Items:**
- [ ] Rajiv: Run a `GROUP BY industry` on `dim_customers` and send a CSV of the mess to Marcus for manual mapping.
- [ ] Nina: Check the `fact_subscriptions` table to ensure the Hooli seat increase didn't trigger a duplicate `subscription_id`.
- [ ] Marcus: Buy more filters for the pour-over station.

---

## Week of 2026-07-13
**Updates:**
- Nina: I added a new column to `nexus-analyst-demo.acme.dim_plans`: `workflow_run_quota_per_month`. This should help us build the "Usage vs. Limit" alerts Rajiv was asking for.
- Rajiv: I’ve mapped about 60% of the "Unknown" countries using `.de`, `.fr`, and `.uk` email domains. It’s not perfect (some `.com` users are in EMEA), but it's better than nothing.
- Marcus: We had a minor incident on Tuesday where the `dim_dates` table didn't include 2027, causing the "Projected Churn" model to crash. I've extended the date dim to 2030.

**Discussion:**
- **Data Quality:** We found about 200 users in `dim_users` who are `is_active = TRUE` but belong to `customer_id` records that are `status = 'churned'`. We need to figure out if these are ghost sessions or if the churn logic in the warehouse is lagging behind the billing system.
- **Summer Fridays:** Just a reminder that this Friday is a half-day. Don't push any major schema changes to `nexus-analyst-demo.acme` after Thursday at 4 PM. 

**Action Items:**
- [ ] Rajiv: Cross-reference `fact_invoices` with `dim_customers.status` to find the "Ghost User" discrepancy.
- [ ] Nina: Build a view for "Near-Limit Customers" using the new `workflow_run_quota_per_month` column.
- [ ] Marcus: Review the board deck slides with the new Hooli numbers.

---

## Week of 2026-07-20
**Updates:**
- Nina: **EMERGENCY UPDATE.** The `fact_workflow_runs` table is currently missing all data from yesterday between 2 PM and 6 PM PT. A deployment on the worker nodes broke the logging pipeline. I'm working with Eng to see if we can recover the logs from S3.
- Rajiv: I've paused the work on `fact_support_tickets` to help Nina with the log recovery.
- Marcus: Board meeting is this Thursday. I need the final ARR number by Wednesday EOD, "Missing Logs" or not. Use the projected averages for the 4-hour gap if you have to.

**Discussion:**
- **Performance:** `SELECT * FROM nexus-analyst-demo.acme.fact_user_events` just timed out for the Marketing team's Looker dashboard. We really need to partition this table by `event_at`.
- **Engagement:** Stark (`c_stark_3`) is still "red" in the churn dashboard, but their CSM says they are just migrating to a new Slack workspace. The `error_code` frequency is actually just 404s on the old webhooks.

**Action Items:**
- [ ] Nina: Recover the missing 4 hours of workflow data.
- [ ] Rajiv: Manually override the "Churn Risk" for Stark in the BI tool so Marcus doesn't get grilled by the Board.
- [ ] Marcus: Send out the updated ARR report once Nina gives the green light on the data.
- [ ] Rajiv: Call the Jura repair guy again. The leak is getting worse.

## Week of 2026-07-27
**Updates:**
- Nina: S3 recovery was 95% successful. We have some duplicates in `nexus-analyst-demo.acme.fact_workflow_runs` for the 3 PM window, so I'm running a `QUALIFY ROW_NUMBER()` script to de-dupe. Don't pull the Hooli numbers until I'm done.
- Rajiv: Back from OOO. I see the Jura guy came but it's still leaking. He apparently needs a "specialized gasket" from the EMEA office? Whatever. 
- Marcus: The Board was fine with the projected ARR, but they're asking for a deep dive into the "Self-Serve to Business" pipeline. 

**Discussion:**
- **dbt Freshness:** The `fact_invoices` table is failing its freshness check. It looks like the Stripe webhook isn't firing for certain `plan_tier = 'Pro'` renewals. 
- **Desk Moves:** Facilities says we’re moving to the 4th floor in September. Start tagging your monitors. Nina, does the server rack in the closet need a specialized move team or can we just lug it?

**Action Items:**
- [ ] Nina: Finalize the de-dup of yesterday's workflow logs.
- [ ] Rajiv: Investigate the Stripe webhook lag for Pro plans.
- [ ] Marcus: Draft the "Expansion Revenue" slide for the follow-up meeting.
- [ ] Nina: Check if `dim_employees` needs a `desk_location` column update for the move.

---

## Week of 2026-08-03
**Updates:**
- Rajiv: I’ve started the audit on `nexus-analyst-demo.acme.dim_users`. We have about 400 users with `last_login_date` in 2024 but `is_active = TRUE`. Our definition of "Active" is definitely broken in the warehouse logic.
- Nina: Working on the partitioning for `fact_user_events`. I'm going to partition by `event_at` and cluster by `customer_id`. This should stop the Looker timeouts.
- Marcus: Hooli (`h_hooli_7`) just signed the expansion for another 200 seats! They need the SSO/Audit log features enabled by Friday.

**Discussion:**
- **Metric Definition:** Marketing wants "Active Workflow" to mean any workflow that ran in the last 7 days. Product wants it to mean any workflow that is *enabled*. We need to pick one for the `fact_subscriptions` summary table.
- **Engagement:** We’re seeing a spike in `error_code = 'RATE_LIMIT_EXCEEDED'` for several Enterprise accounts. If they’re hitting the limit on "unlimited" plans, we might have a recursive loop bug in the worker nodes.

**Action Items:**
- [ ] Rajiv: Update the `is_active` flag logic in dbt to look at a 30-day rolling window of logins.
- [ ] Nina: Deploy the partitioned version of `fact_user_events`.
- [ ] Marcus: Confirm the seat count for Hooli with Finance to ensure `fact_subscriptions` reflects the correct MRR.

---

## Week of 2026-08-10
**Updates:**
- Nina: **Heads up.** I'm adding `sso_enabled` and `audit_log_enabled` to `nexus-analyst-demo.acme.dim_plans`. This will break any `SELECT *` queries in the short term. Update your scripts.
- Rajiv: Stark is finally "Green" in the dashboard. The manual override worked, but we should really fix the `error_code` logic so 404s on webhooks don't trigger a churn warning.
- Marcus: I'm OOO this Thursday/Friday for a wedding. If the ARR numbers drop, don't panic, it's probably just the Hooli invoice pending.

**Discussion:**
- **Jura Watch:** The Jura is officially dead. There is a bucket under it. Use the AeroPress in the kitchen for now. 
- **VRS Status:** The Venture Reporting Suite (VRS) needs a monthly export of `fact_invoices` by `region`. Can we automate this to an S3 bucket instead of Rajiv doing a manual CSV dump?

**Action Items:**
- [ ] Nina: Finish the `dim_plans` schema update.
- [ ] Rajiv: Setup the S3 export for the VRS reports.
- [ ] Marcus: Approve the new Jura purchase (Nina sent the link for the industrial one).
- [ ] Nina: Check why `dim_customers.csm_employee_id` is null for the new batch of MM signups.

---

## Week of 2026-08-17
**Updates:**
- Nina: The `fact_user_events` partitioning is live. Queries are running 40% faster. Looker shouldn't be timing out anymore.
- Rajiv: I found the issue with the "Ghost Users." It’s a legacy bug from the 2024 migration where `customer_id` was mapped to `invited_by_user_id` in the staging table. I'm wiping `nexus-analyst-demo.acme.dim_users` and re-running the full sync tonight. 
- Marcus: We have a new "Near-Limit" dashboard. Nina, can we add a toggle for `account_tier`? I only care about the Business and Enterprise folks hitting their `workflow_run_quota_per_month`.

**Discussion:**
- **Summer Fridays:** This is the last Summer Friday of the year. Enjoy it. 
- **Data Quality:** We keep seeing `NULL` in `acquisition_channel` for about 15% of new signups. It makes the "CAC by Channel" report look like garbage. Rajiv thinks it’s a cookie-tracking issue on the marketing site.

**Action Items:**
- [ ] Rajiv: Complete the `dim_users` re-sync.
- [ ] Nina: Add the `account_tier` filter to the Near-Limit dashboard.
- [ ] Marcus: Follow up with Marketing about the `acquisition_channel` missing data.
- [ ] All: Clear out your lockers by Friday for the carpet cleaning.

---

## Week of 2026-08-24
**Updates:**
- Nina: dbt freshness alert on `fact_workflow_runs`. The Fivetran connector for the production DB stalled for 6 hours on Sunday. It’s caught up now, but the 8 AM dashboard was stale. 
- Rajiv: Board deck prep is starting. Marcus, I need a hard definition on "Active Customer" for the Slide 4 "Logo Retention" chart. Are we counting "Paused" status as churned for the sake of the board?
- Marcus: Desk moves are happening this weekend. I'm moving closer to the Sales floor to hear why they keep promising custom SSO for Pro accounts. 

**Discussion:**
- **Engagement Definition:** We have three different versions of "Weekly Active User" (WAU) in Looker. One looks at `last_login_date` in `dim_users`, one looks at `fact_user_events`, and one looks at `fact_workflow_runs`. We need to consolidate. Sales wants the "inflated" number (any login), but Product wants the "real" number (actually ran a workflow). 
- **The New Jura:** It’s here. Do NOT use oily beans. There is a sign-up sheet for the "Coffee Cleaning Rotation" on the fridge. 

**Action Items:**
- [ ] Nina: Create a `gold_engagement_metrics` view that combines logins and workflow runs.
- [ ] Rajiv: Re-run the ARR bridge for July—Hooli’s expansion looks like it was double-counted because of a mid-cycle seat upgrade.
- [ ] Marcus: Send the final definition of "Churned" to Finance (specifically regarding the 30-day grace period).
- [ ] Nina: Investigate why `nexus-analyst-demo.acme.fact_subscriptions.mrr_usd` is showing $0 for the Pied Piper "Business" trial.

---

## Week of 2026-08-31
**Updates:**
- Nina: I’m starting the migration of the legacy `dim_customers` table to include the `ae_employee_id` and `csm_employee_id` joins directly so Rajiv doesn't have to keep doing `LEFT JOIN dim_employees` in every single query.
- Rajiv: The VRS S3 export is finally automated. It’s hitting `s3://acme-vrs-reporting-prod/manual_dumps/` every Monday at 4 AM. Rajiv is officially retired from manual CSV duty.
- Marcus: I'm OOO for the long weekend (Labor Day). Please don't break the warehouse.

**Discussion:**
- **Invoicing Errors:** Finance reported that about 50 Enterprise invoices in `fact_invoices` are marked as `status = 'void'` even though they were paid via wire. It’s a manual entry error in the billing system. Rajiv needs to map these manually in the `stg_invoices` dbt model for now.
- **Workflow Latency:** A few Tier 1 customers (specifically "Soylent Corp" and "Initech") complained about 5-second delays in webhook triggers. Nina checked `fact_workflow_runs.duration_ms` and the P99 is definitely creeping up.

**Action Items:**
- [ ] Rajiv: Fix the voided invoice mapping in the dbt model so the "Cash Collected" report is accurate.
- [ ] Nina: Audit the `step_count` in `fact_workflow_runs` to see if the latency is tied to complex workflows or just infrastructure load.
- [ ] Marcus: Sign the contract for the new dbt Cloud seats.
- [ ] All: Reminder—the kitchen fridge will be cleaned out Friday at 4 PM. Anything without a name goes in the trash.

---

## Week of 2026-09-07
**Updates:**
- Nina: `dim_plans` is updated. I added `storage_gb` and `sla_uptime_pct` columns. 
- Rajiv: I did a deep dive on the "Acquisition Channel" missing data. It’s definitely the "Accept All Cookies" banner—if they don’t click it, our UTM scraper fails and defaults to `NULL`. About 12% of our traffic is "Dark Social" or "Direct" now. 
- Marcus: We need to pull a list of all customers on the "Pro" plan with more than 20 seats. We’re going to do a targeted campaign to push them to "Business" for the SSO/Audit Log features.

**Discussion:**
- **Incident Follow-up:** The `dim_users` wipe from two weeks ago had a side effect. Some `invited_by_user_id` fields are still wonky because the source IDs changed during the re-sync. Nina is looking at the audit logs.
- **Office Vibe:** Someone is leaving fish in the microwave. Stop it.

**Action Items:**
- [ ] Rajiv: Generate the "Pro Over-Utilizers" list (Customer ID, Name, Seat Count, MRR).
- [ ] Nina: Re-link the `invited_by_user_id` using the `email_domain` as a secondary join key for the legacy records.
- [ ] Marcus: Talk to the Marketing team about the UTM/Cookie issue—maybe move the tracking script to the server-side?
- [ ] Nina: Check `nexus-analyst-demo.acme.fact_workflow_runs` for any `error_code` spikes from the Amsterdam region (EMEA).

---

## Week of 2026-09-14
**Updates:**
- Nina: I've added `is_business_day` to `dim_dates`. This should help with the "Daily Active User" charts so we stop seeing the weekend "dips" as a product failure.
- Rajiv: The board deck is finished. The NRR (Net Revenue Retention) is looking solid at 118%, mostly driven by the Enterprise expansions.
- Marcus: We’re hiring a Junior Data Analyst. If you know anyone, send them the Greenhouse link.

**Discussion:**
- **Data Privacy:** Legal wants to know if we can mask `email_domain` in `dim_users` for the "Free" tier users. Marcus is pushing back because that’s how we identify high-intent leads (e.g., someone from `@google.com` signing up for a Free account).
- **Warehouse Costs:** Our BigQuery bill spiked 20% last month. Nina found a bunch of `SELECT *` queries running every 15 minutes for a custom dashboard Marcus built for the Sales team. 

**Action Items:**
- [ ] Nina: Refactor the Sales dashboard to use a summary table instead of querying `fact_user_events` directly.
- [ ] Rajiv: Update the "High Intent Leads" report to exclude personal domains like `@gmail.com` or `@outlook.com`.
- [ ] Marcus: Approve the budget for the Junior Analyst role.
- [ ] All: Marcus's birthday is Wednesday. There will be donuts. (No fish in the microwave).

---

## Week of 2026-09-21
**Updates:**
- Nina: OOO for the rest of the week (wedding in Italy). Reach out to Marcus for any "Tier 1" dashboard breaks.
- Rajiv: Preliminary Q3 numbers look decent, but the "Pro to Business" conversion rate is lagging behind the target we set in July. We're at 2.1% against a 3.5% goal.
- Marcus: The dbt freshness alert for `fact_user_events` has been firing every morning at 4 AM. It seems the Fivetran connector for the production DB is hitting a row limit or timing out during the midnight sync.

**Discussion:**
- **Engagement Metric:** We need to finalize the definition of "Active Customer" for the Q3 Board Deck. Is it a customer with at least one user login in `dim_users`, or do they need a successful run in `fact_workflow_runs`? 
- **The "Great Desk Shuffle":** Marketing and Sales are swapping pods on Friday. Please clear your monitors by 4 PM. If you left a half-eaten sandwich in the mini-fridge near the window, it's going in the trash.

**Action Items:**
- [ ] Rajiv: Pull the historical conversion funnel using `fact_subscriptions` to see if the lag is seasonal or related to the price change in May.
- [ ] Marcus: Increase the timeout on the Fivetran `acme_prod` connector.
- [ ] Nina (When back): Look at `nexus-analyst-demo.acme.fact_workflow_runs` to see if `triggered_by = 'webhook'` accounts for the majority of Enterprise volume vs. scheduled runs.

---

## Week of 2026-09-28
**Updates:**
- Marcus: The Junior Analyst job post is live. We already have 40 applicants. Rajiv, please help me filter for anyone with BigQuery/SQL experience.
- Nina: Fixed the dbt freshness issue. It was a `JOIN` in the `stg_events` model that was blowing up the fan-out and causing the warehouse to hang. 
- Rajiv: Reminder—all expense reports for the Amsterdam offsite are due by Friday.

**Discussion:**
- **VRS Status:** The "Variable Runtime Scoping" feature is in beta. Nina noticed that `fact_workflow_runs` is showing a lot of `null` values for `duration_ms` for the new `vrs_alpha` accounts. Is this a logging bug or are the runs failing before they start?
- **Enterprise Account Review:** One of our biggest Enterprise customers (Customer ID: 4921) has had zero `step_count` activity for 10 days. Marcus suspects they are migrating to a competitor or their API key expired.

**Action Items:**
- [ ] Nina: Query `nexus-analyst-demo.acme.fact_workflow_runs` where `customer_id = 4921` and check for `error_code` 'AUTH_001'.
- [ ] Rajiv: Send Marcus the top 5 candidates from Greenhouse.
- [ ] Marcus: Check the "VRS" feature flag logic in the app code—why aren't we capturing run durations?
- [ ] All: Coffee machine is broken. Maintenance is coming Thursday. Bring your own caffeine.

---

## Week of 2026-10-05
**Updates:**
- Nina: I’ve updated the `dim_customers` logic to better reflect `account_tier`. We were accidentally bucketed some "MM" (Mid-Market) accounts as "SMB" because of the `seat_count_licensed` threshold.
- Rajiv: Board Prep is in high gear. I need a "Top 20 Churn Risk" list based on usage drops.
- Marcus: The Amsterdam office is reporting latency on the `fact_workflow_runs` queries. We might need to cluster the table by `region` or `triggered_at`.

**Discussion:**
- **Data Model Debt:** We have three different versions of "MRR" floating around (Finance MRR, Sales MRR, and Data Warehouse MRR). We need to converge on `fact_subscriptions` as the source of truth. Nina found a discrepancy where `mrr_usd` in `fact_subscriptions` doesn't match the `amount_usd` in `fact_invoices` for partial-month upgrades.
- **Office Vibes:** The "No Fish" rule is being ignored. There is a lingering smell near the data pod.

**Action Items:**
- [ ] Nina: Build a "Churn Signal" dashboard: any customer with a >50% WoW drop in `fact_workflow_runs` volume.
- [ ] Marcus: Investigate BigQuery clustering for `nexus-analyst-demo.acme.fact_workflow_runs` on `(region, triggered_at)`.
- [ ] Rajiv: Cross-reference the "Finance MRR" spreadsheet with the `sum(mrr_usd)` from `fact_subscriptions` where `is_current = TRUE`.
- [ ] Marcus: Order a new "Privacy Screen" for the Junior Analyst’s desk.

---

## Week of 2026-10-12
**Updates:**
- Marcus: Welcome Sarah, our new Junior Data Analyst! She’ll be spending the first week on "Data Janitor" duty (cleaning up the `email_domain` logic in `dim_users`).
- Nina: The EMEA spike in `error_code` 'ERR_402' was actually a bug in the Stripe integration for Business-tier renewals. Fixed now, but we need to reconcile the missed payments.
- Rajiv: Series C talks are starting to bubble up for next year. The board wants to see "Efficiency Ratios" (ARR per Headcount).

**Discussion:**
- **Product Launch:** The new "AI Workflow Suggester" is tracking events in a raw JSON blob in `fact_user_events`. Sarah, your first task is to write a parser for `event_properties` so we can see which suggestions are being clicked.
- **BigQuery Costs:** We’re back under budget after Nina's refactor of the Sales dashboard. `fact_user_events` is no longer being scanned 96 times a day.

**Action Items:**
- [ ] Sarah: Grant her access to `nexus-analyst-demo.acme.*` (Read Only).
- [ ] Nina: Help Sarah with the `JSON_EXTRACT` syntax for the AI events.
- [ ] Rajiv: Update the "Investor Ready" dashboard with the latest NRR figures from `fact_subscriptions`.
- [ ] Marcus: Confirm the date for the Q4 Planning Offsite.

---

## Week of 2026-10-19
**Updates:**
- Nina: I’m seeing a weird trend in `dim_customers` where `country` is coming in as 'Unknown' for about 15% of the new Free tier signups. Looks like the IP-to-Geo service is failing for mobile users.
- Sarah: Finished my first dbt PR! The `email_domain` masking for Free users is now live in `dim_users_masked`.
- Rajiv: We have a "Zombie" customer problem. 50+ accounts on the Pro plan have `current_mrr_usd > 0` but haven't had a login in 90 days.

**Discussion:**
- **The "Zombie" Problem:** Should we proactively reach out to these customers, or just keep collecting the revenue? Sales wants to "Save" them, but Finance says let them ride until they churn.
- **BigQuery Schema Change:** Marcus wants to add `storage_gb_used` to `fact_workflow_runs`. Nina is worried about the write-amplification since that table is already huge.

**Action Items:**
- [ ] Sarah: Create a list of "Zombie" Customer IDs (no login in `dim_users` for 90 days, but `status = 'active'`).
- [ ] Nina: Talk to the backend team about how we’re tracking storage usage per run.
- [ ] Marcus: Get Sarah a second monitor. She's squinting at the SQL.
- [ ] Rajiv: Review the "Unknown" country accounts—are any of these high-value domains? (e.g., `@apple.com`).

---

## Week of 2026-10-26
**Updates:**
- Nina: OOO Thursday/Friday for her sister’s wedding in Napa. If the pipeline breaks, ping Marcus.
- Sarah: I’m still seeing `null` values for `triggered_by` in about 4% of records in `nexus-analyst-demo.acme.fact_workflow_runs`. It looks like these are system-level cron jobs, but they should be attributed to 'SYSTEM'. 
- Rajiv: Board deck prep starts today. I need the final Q3 NRR vs. Logo Churn breakdown by tomorrow EOD.

**Discussion:**
- **dbt Freshness:** We had a 4-hour lag yesterday because the `stg_events` model took forever to rebuild. We might need to switch to incremental for `fact_user_events` earlier than planned. 
- **The Coffee Machine:** Someone (not naming names) left the oat milk out again. It was chunky. Please don’t do that.

**Action Items:**
- [ ] Sarah: Update the SQL in `fact_workflow_runs` to `COALESCE(triggered_by, 'SYSTEM')`.
- [ ] Marcus: Approve Nina’s PR for the `dim_customers` geography fix before she leaves.
- [ ] Nina: Send Rajiv the SQL snippet for the "Expansion MRR" cohort analysis.
- [ ] ALL: Halloween costume contest is Friday. Marcus is going as a "Broken Data Partition."

---

## Week of 2026-11-02
**Updates:**
- Nina: Back! The wedding was great. Also, the `fact_subscriptions` table didn't refresh this morning because of a schema change in the upstream Stripe export. Fixed the mapping.
- Marcus: We have a "Red Account" alert for Globex Corp. Their `step_count` in `fact_workflow_runs` dropped by 80% since Friday. 
- Sarah: I found 12 users who have `is_active = true` but don't exist in the `dim_users` table but show up in the events log. Ghost users?

**Discussion:**
- **Defining "Active User":** We’ve been using "one login in 30 days," but Product wants to change it to "at least one successful workflow run." This will tank our MAU numbers by about 22%. Nina is pushing back.
- **VRS (Volume-Retention-Score):** The new scoring model for Enterprise accounts is live in Looker. We need to validate if a high VRS actually correlates with renewals for the Q1 2027 renewals.

**Action Items:**
- [ ] Nina: Run a comparison report: Current MAU vs. "Run-based" MAU for the last 6 months.
- [ ] Sarah: Investigate the "Ghost Users"—check if these are deleted accounts that weren't soft-deleted in the replica.
- [ ] Rajiv: Reach out to the CSM for Globex Corp to see if they’re migrating to a different tool.
- [ ] Marcus: Order more ergonomic mouse pads.

---

## Week of 2026-11-09
**Updates:**
- Rajiv: Good news! Apple expanded their seat count from 500 to 750. I’ve updated `dim_customers`, but `current_mrr_usd` hasn't ticked up yet. 
- Sarah: My "Zombie" list is ready. We have 62 accounts that are essentially paying for nothing. Total "dead" MRR is around $8,400.
- Nina: I’m noticing a lot of `error_code = 'TIMEOUT'` in `fact_workflow_runs` for customers in the `EMEA` region between 2 AM and 4 AM UTC. 

**Discussion:**
- **Incident Follow-up:** The `fact_invoices` table was showing double-counted amounts for 2 hours on Tuesday due to a join error on `subscription_id`. We need to add a unique key test in dbt for that table immediately.
- **Office Move:** Marcus says we might be moving to the 6th floor in January. More windows, but further from the good snacks.

**Action Items:**
- [ ] Nina: Add the `dbt_utils.unique_combination_of_columns` test to `fact_invoices`.
- [ ] Sarah: Dig into the EMEA timeout errors—is it a specific integration (e.g., Salesforce, Slack)?
- [ ] Marcus: Confirm the Apple expansion in `fact_subscriptions` to ensure the `change_type` is recorded as 'UPGRADE'.
- [ ] Rajiv: Share the "Zombie" list with the Success team for a "Value Kickoff" campaign.

---

## Week of 2026-11-16
**Updates:**
- Nina: `fact_user_events` is now over 4TB. Queries are getting slow. I’m proposing we move everything older than 90 days to a `_history` table or use BQ partitions properly.
- Marcus: Board meeting went well. They liked the "Workflow Efficiency" metric Sarah built.
- Sarah: I'm seeing a weird spike in `acquisition_channel = 'Viral'`—looks like a bunch of students are using the Free tier for a class project.

**Discussion:**
- **The "Viral" Spike:** It’s great for the top-of-funnel, but it’s costing us a fortune in BigQuery compute because of the `fact_workflow_runs` volume. Should we cap the Free tier runs even further?
- **Schema Question:** We need to track `user_role` changes over time. Right now `dim_users` is just a snapshot. Does anyone have a better way than creating a `dim_user_history` SCD Type 2 table?

**Action Items:**
- [ ] Nina: Draft a partitioning strategy for `nexus-analyst-demo.acme.fact_user_events` based on `event_at`.
- [ ] Sarah: Filter the "Viral" signups by `email_domain` to see if it’s mostly `.edu` addresses.
- [ ] Marcus: Talk to the Engineering Lead (Dave) about getting a CDC stream for user role changes.
- [ ] Rajiv: Update the Sales dashboard to exclude the `.edu` signups from the "Qualified Leads" count.

---

## Week of 2026-11-23 (Short Week - Thanksgiving)
**Updates:**
- Sarah: I’ll be OOO Wednesday through Friday. 
- Nina: Just a heads-up, I'm muting the #alerts-data-freshness channel over the weekend unless it's a P0.
- Marcus: The desk move is confirmed for the first week of Jan. Start packing your non-essentials.

**Discussion:**
- **Data Debt:** We have 14 deprecated models in dbt that are still running every day. Nina wants a "Delete-a-thon" next week. 
- **The "Unknown" Country Issue:** Sarah found that the mobile app wasn't sending the `x-forwarded-for` header, which is why the Geo-IP service was failing. Devs are fixing it in the next release.

**Action Items:**
- [ ] Nina: Tag all models in dbt that haven't been queried in BigQuery in the last 30 days.
- [ ] Sarah: Finish the documentation for the `AI Workflow Suggester` parser before leaving for the holiday.
- [ ] Marcus: Buy more bubble wrap for the monitors.

---

## Week of 2025-12-01
**Updates:**
- Nina: Delete-a-thon was a success. We nuked 11 legacy models in the `staging` folder. BigQuery storage costs should dip slightly, but the real win is the dbt DAG looking less like a spiderweb.
- Rajiv: Sales is asking why the `current_mrr_usd` in `nexus-analyst-demo.acme.dim_customers` doesn't match the Stripe dashboard for "Globex Corp". 
- Marcus: Still waiting on the HR file for the new hires in EMEA. Hire dates for the Amsterdam team might be off in `dim_employees`.

**Discussion:**
- **Defining "Active User":** We’re having a heated debate with Product. They want `is_active` to mean "logged in within 14 days." Engineering thinks it should be "triggered at least one workflow." If we change this, it’ll shift our North Star metric by 20%. 
- **Engagement Metric:** Sarah proposed a "Sticky Factor" (DAU/MAU) specifically for users who interact with the `AI Workflow Suggester`. We need to pull from `nexus-analyst-demo.acme.fact_user_events` where `event_name = 'ai_suggestion_accepted'`.

**Action Items:**
- [ ] Sarah: Run a comparison report on the two "Active User" definitions to see the impact on the Dec board deck.
- [ ] Nina: Investigate the Globex MRR discrepancy. Check if it's a multi-currency conversion issue (USD vs EUR).
- [ ] Rajiv: Clean up the `industry` column in `dim_customers`. We have "FinTech", "Fintech", and "Financial Services" as separate buckets.
- [ ] Marcus: Tell the office manager the espresso machine is making that high-pitched whistling noise again.

---

## Week of 2025-12-08
**Updates:**
- Marcus: Board prep starts today. I need everyone’s eyes on the "Net Revenue Retention" (NRR) charts by Thursday.
- Sarah: I’ve optimized the join between `fact_workflow_runs` and `dim_plans`. Query time dropped from 45s to 12s. 
- Nina: I’m seeing a lot of nulls in `invited_by_user_id` for Enterprise customers. Might be a bug in the SSO provisioning flow.

**Discussion:**
- **VRS Status Check:** The Virtual Run Storage (VRS) project is behind. Dave says the telemetry isn't hitting the `fact_workflow_runs` table correctly for "Step Count" on failed runs.
- **Account Review:** "Aperture Science" (Enterprise) is hitting their run quota every week. We need to see if they are candidates for a custom tier or if they’re just running inefficient loops.

**Action Items:**
- [ ] Marcus: Finalize the NRR slice by `account_tier` (SMB vs MM vs Ent).
- [ ] Sarah: Sync with Dave (Eng) on the `step_count` nulls for failed runs.
- [ ] Nina: Create a temporary view `v_aperture_usage_audit` to track their workflow patterns.
- [ ] Rajiv: Update the "Churn Risk" dashboard to include the new `last_login_date` logic from `dim_users`.

---

## Week of 2025-12-15
**Updates:**
- Nina: **P0 Incident Sunday night.** The dbt Cloud job failed because someone (me...) pushed a breaking change to the `fact_subscriptions` schema without updating the downstream `fct_mrr_movements`. Fixed at 2 AM.
- Sarah: Holiday party is Thursday! Don't forget the Secret Santa.
- Rajiv: I'm seeing a massive spike in "Pro" signups from the APAC region. Might be the result of that LinkedIn campaign.

**Discussion:**
- **Incident Follow-up:** We need a better CI/CD check for schema changes in `nexus-analyst-demo.acme`. Marcus wants a mandatory peer review on any change to a `fact` table.
- **Data Freshness:** The `#alerts-data-freshness` channel is blowing up. `fact_invoices` hasn't refreshed in 18 hours because the Fivetran connector for Stripe is throttled.

**Action Items:**
- [ ] Nina: Add a dbt test to check for uniqueness on `subscription_id` in `fact_subscriptions`.
- [ ] Sarah: Check the `acquisition_channel` for the APAC spike. Is it 'Paid Social' or 'Organic'?
- [ ] Marcus: Review the incident report for the Sunday night outage.
- [ ] Rajiv: Remind everyone to bring their physical badges for the holiday party venue.

---

## Week of 2026-01-05
**Updates:**
- Marcus: Happy New Year! We are officially in the new office (The Annex). Boxes are everywhere. Please find your own monitor.
- Nina: I’m refactoring `dim_customers` to include `csm_employee_id`. No more manual lookups in the CS spreadsheet.
- Sarah: I'm starting the "Workflow Efficiency" v2 model. It's going to incorporate `duration_ms` from `nexus-analyst-demo.acme.fact_workflow_runs`.

**Discussion:**
- **Schema Evolution:** We need to add `error_code` to the main workflow dashboard. Currently, it's buried in the raw logs. This will help CS proactively reach out to customers with high failure rates.
- **The "Edu" Problem:** Following up on Sarah's audit from Nov—the `.edu` signups are 15% of our Free tier volume but 40% of the compute cost. We need to talk to Product about a "Student" tier that is more restricted.

**Action Items:**
- [ ] Sarah: Build a Top 10 Error Codes chart for the CS team.
- [ ] Nina: Map the `csm_employee_id` in `dim_customers` to the `employee_id` in `dim_employees`.
- [ ] Rajiv: Pull a list of the top 50 `.edu` domains by workflow volume for the Product meeting.
- [ ] Marcus: Order more power strips for the new desks. Half the team is currently unplugged.

---

## Week of 2026-01-12
**Updates:**
- Nina: dbt freshness is green. We increased the Stripe API rate limit, so `fact_invoices` is back on track.
- Sarah: I'm OOO on Friday for a long weekend.
- Rajiv: "Initech" just upgraded from Business to Enterprise. Someone needs to manually update their `ae_employee_id` in `dim_customers` because the Salesforce sync is lagging.

**Discussion:**
- **Engagement Definition (Final):** We're going with the "Productive Session" metric: A login AND at least one successful workflow run within 24 hours. 
- **CDC Stream:** Dave says the CDC (Change Data Capture) for `user_role` is finally live. We can start building `dim_user_history` SCD Type 2 next week.

**Action Items:**
- [ ] Nina: Begin the dbt implementation for `dim_user_history` using the new CDC source.
- [ ] Sarah: Update the Executive Dashboard to use the "Productive Session" definition.
- [ ] Marcus: Send the "New Year, New Metrics" email to the whole company.
- [ ] Rajiv: Make sure "Initech" is correctly flagged as 'Ent' in the Q1 Forecast.

## Week of 2026-01-19
**Updates:**
- Nina: `dim_user_history` is in staging. The CDC stream from Dave's team is a bit "chatty"—seeing multiple records per second for some power users at "Globex Corp". I might need to add a deduplication step in the silver layer.
- Marcus: Power strips arrived. If you're still daisy-chaining, please stop. It's a fire hazard. Also, the espresso machine is leaking again; call to the technician is out.
- Rajiv: Cleaned up the `ae_employee_id` for "Initech". They are officially showing up as Enterprise in the `fact_subscriptions` view now. 

**Discussion:**
- **Board Prep:** Q1 Board meeting is coming up. Sarah, we need a slide on the "Efficiency Ratio" (Workflow runs per licensed seat). Rajiv says the `seat_count_licensed` in `nexus-analyst-demo.acme.dim_customers` is the source of truth, but we need to join it against `fact_workflow_runs` to get the actual utilization.
- **Data Quality Alert:** We're seeing some nulls in `acquisition_channel` for about 20% of the January signups. Nina thinks it’s related to the new "Refer-a-Friend" flow skipping the UTM capture logic.

**Action Items:**
- [ ] Sarah: Draft the "Productive Sessions" vs. "Total Logins" chart for the Board deck.
- [ ] Nina: Debug the UTM/Acquisition channel nulls with the Growth Eng team.
- [ ] Rajiv: Verify that the `current_mrr_usd` in `dim_customers` matches the sum of `amount_usd` in `fact_invoices` for the Top 50 accounts.
- [ ] Marcus: Put a bucket under the espresso machine.

---

## Week of 2026-01-26
**Updates:**
- Sarah: Back from the long weekend. The "Top 10 Error Codes" chart for CS is live. Most common is `429_RATE_LIMIT` for users on the Pro tier. 
- Nina: `dim_user_history` is promoted to production. You can now track when a user moves from 'editor' to 'admin'.
- Rajiv: Working on the `.edu` domain deep-dive. Preliminary look shows three specific universities in the Midwest are responsible for 60% of the "Edu" compute spike. 

**Discussion:**
- **VRS (Value Realization Score):** Product wants a single "Health" metric. Current proposal: (Active Workflows / Workflow Quota) + (Logins in last 7 days / 7). 
- **Schema Question:** Should `error_code` stay in `fact_workflow_runs` or should we have a separate `dim_error_codes`? Right now it's just a string like 'AUTH_01' or 'TIMEOUT'. 

**Action Items:**
- [ ] Nina: Create a view for the "VRS" metric so Product can start A/B testing the weights.
- [ ] Sarah: Sync with CS on the `429_RATE_LIMIT` spike—is it a product bug or just users hitting their Pro limits?
- [ ] Rajiv: Finalize the `.edu` memo. We need to decide if we're going to hard-cap these domains by Feb 15th.
- [ ] Marcus: Desk move map is posted in Slack. Everyone is moving 5 feet to the left on Wednesday.

---

## Week of 2026-02-02
**Updates:**
- Nina: dbt freshness alert on `fact_user_events`. Looks like the Segment integration stalled over the weekend. I'm re-syncing the last 48 hours now.
- Rajiv: "Cyberdyne Systems" just signed a $120k Enterprise deal. Marcus, we need to make sure their CSM (looks like it's going to be Kim) is correctly mapped in `dim_customers`.
- Sarah: I spent all day Monday troubleshooting why `duration_ms` in `nexus-analyst-demo.acme.fact_workflow_runs` was showing negative values for some runs. Turns out it's a clock sync issue on the Amsterdam cluster.

**Discussion:**
- **The "Great Migration":** We're moving the legacy `raw_logs` to the `nexus-analyst-demo.acme` FLAT structure. Any dashboards still pointing to the `prod_v1` dataset will break on Friday. 
- **Employee Churn:** Marcus notes that `is_active` in `dim_employees` needs to be updated for the three people who left last Friday. This is messing up the "ARR per Employee" calculation in Sarah's dashboard.

**Action Items:**
- [ ] Nina: Finish the Segment re-sync and verify the `event_at` timestamps.
- [ ] Marcus: Update `dim_employees` with the latest termination dates.
- [ ] Sarah: Filter out the negative `duration_ms` values in the "Workflow Efficiency" v2 model until the Eng team fixes the cluster clock.
- [ ] Rajiv: Get the Cyberdyne contract signed and uploaded to the SFDC-to-BQ bridge folder.

---

## Week of 2026-02-09
**Updates:**
- Rajiv: The `.edu` policy is live. We've limited Free tier accounts with university emails to 50 runs/mo. Seeing a small dip in `step_count` already.
- Nina: I’ve added `is_weekend` and `is_business_day` flags to `dim_dates` to help Sarah with the "Workday vs Weekend" usage analysis.
- Marcus: The coffee machine is fixed! No more buckets. Also, please don't leave old sandwiches in the fridge; Friday is clean-out day.

**Discussion:**
- **Incident Post-Mortem:** We had a 2-hour window on Tuesday where `fact_invoices` wasn't updating. Stripe's webhook was down. Sarah, did any "Business" customers get incorrectly flagged as "Past Due"?
- **Audit Logs:** Legal is asking for a way to see who invited whom. We can do this by joining `dim_users.user_id` to `dim_users.invited_by_user_id`. Nina, can we expose this in a clean way?

**Action Items:**
- [ ] Nina: Build a `dim_user_referral_tree` table to satisfy Legal's request.
- [ ] Sarah: Audit the "Past Due" customers from Tuesday's Stripe glitch. Reach out to Finance if we need to manually mark them as 'Paid'.
- [ ] Rajiv: Update the Q1 Forecast to account for the `.edu` run volume reduction. It might actually save us $4k/mo in GCP costs.
- [ ] Marcus: Send out the updated "Office Etiquette" doc (mostly about the fridge).