---
title: "Slack #revenue-ops channel archive — 2025-2026"
source_url: "internal://acme/slack-revenue-ops-2025-2026"
license: "synthetic-demo"
attribution: "Synthetic content, Acme Inc internal demo. Acme Inc is a fictitious company."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

### [2025-01-06] Monday Morning Sync Prep

**jorge.martinez** — 08:14 AM
Happy New Year everyone. Hope the break was good. Pushing the Q1 planning doc to the channel now. We need to finalize the AE territories by Wednesday for Marcus.

**marcus.webb** — 08:22 AM
@jorge.martinez thanks. Let’s make sure we have the updated capacity model. I want to know exactly how many heads we need in EMEA if we’re going to hit the $45M ARR target by year end.

**lina.cho** — 09:05 AM
@marcus.webb we’re at ~$33M currently right? I’m seeing some drift in the Looker "Executive Summary" vs. the raw `arr_snapshot`.

**jorge.martinez** — 09:10 AM
@lina.cho Yeah, don't use the Looker "Executive Summary" for the next 48 hours. I'm re-mapping the `ae_employee_id` field in Salesforce because of the re-org. It’s breaking the join to `dim_employees`.

**rachel.stein** — 10:30 AM
Is the drift significant? We have the board meeting on the 20th. I need one number.

**lina.cho** — 10:45 AM
@rachel.stein Looker is showing $35M because it’s not filtering out the 'Paused' status for Tamarind Group (cust_000706). The canonical source is `nexus-analyst-demo.acme.arr_snapshot`. That has us at $33.4M as of Dec 31.

**rachel.stein** — 10:48 AM
Okay. Let's stick to `arr_snapshot` for all board reporting. No exceptions.

**jorge.martinez** — 11:15 AM
@tom.becker did you ever get the signature from Onyx Robotics? Salesforce is still showing "Stage 4 - Negotiation."

**tom.becker** — 11:20 AM
Legal is still redlining the indemnity clause. Apparently, their CTO is worried about the "unlimited runs" on Enterprise. They want a cap or a lower price.

**marcus.webb** — 11:22 AM
No caps for Onyx. They’re a $420k ACV deal. If they want 500 seats, they get the Enterprise unlimited runs. That's the value prop. Tom, tell them it’s part of the SOC2 custom SLA package.

---

### [2025-01-15] Q4 2024 Commission Review (Noise/Admin)

**jorge.martinez** — 02:30 PM
Quick reminder to all AEs: get your expense reports for December in by Friday. If it's not in Expensify, it doesn't exist.

**sarah.chen** — 02:32 PM
Does the team dinner in Amsterdam count? We had the whole EMEA crew there.

**jorge.martinez** — 02:33 PM
Yes, but you need the itemized receipt. I can't approve a $1,200 "Dinner" line item without seeing how many bottles of wine you ordered lol.

**omar.haddad** — 03:00 PM
Hey @lina.cho, I'm looking at my attainment for Q4. I think I’m missing the Harbor Dynamics (cust_000713) expansion.

**lina.cho** — 03:15 PM
Checking... harbor dynamics expanded on Dec 28. It’s in `fact_subscriptions`. Did you update the Opportunity to "Closed Won"?

**omar.haddad** — 03:17 PM
Yeah, it's closed in SFDC.

**lina.cho** — 03:20 PM
Ah, I see it. You tagged it as 'Business' tier but kept the MRR at the old rate. I’ll fix the `bookings_attribution` table manually, but Jorge, we need to fix the sync between SFDC and the warehouse for mid-month mid-tier upgrades.

**jorge.martinez** — 03:22 PM
On the list. That CRM migration is going to be the death of me.

---

### [2025-02-12] NRR & Retention Discussion

**rachel.stein** — 09:12 AM
@lina.cho I’m looking at the NRR for the "Business" segment and it looks low. 98%? That doesn't feel right given our expansion rates.

**lina.cho** — 10:05 AM
Let me check the query.
...
Okay, found it. Someone was using an INNER JOIN between the start-of-period cohort and the end-of-period cohort in the `nrr_trailing_12` draft. It was dropping everyone who churned.

**rachel.stein** — 10:07 AM
Wait, if it drops the churns, wouldn't NRR look higher?

**lina.cho** — 10:10 AM
Wait, sorry, coffee hasn't kicked in. I meant the denominator was being calculated only for customers who *still* exist. Let me re-run it.
The correct methodology we agreed on: Fixed cohort = all paid customers as of T-12 months. We use a LEFT JOIN from the cohort to the current MRR and `COALESCE(end_mrr_usd, 0)`.

**lina.cho** — 10:45 AM
Updated. Real NRR is ~107%. GRR is ~94%. The 13% expansion is mostly coming from the seat-add motion in the Business tier (MM accounts).

**jorge.martinez** — 10:48 AM
Does that 107% include the "Free" tier?

**lina.cho** — 10:50 AM
No. NRR is paid-to-paid only. Downgrades to Free count as 100% churn for that customer.

---

### [2025-03-04] Data Path Errors (Signal: Flat Namespace)

**rajiv.menon** — 11:30 AM
@lina.cho I'm trying to build the new churn forecast but I'm getting `Not found: Table nexus-analyst-demo:acme.marts.finance.arr_snapshot`. Did we move the finance marts?

**lina.cho** — 11:32 AM
@rajiv.menon No nested datasets! It's just `nexus-analyst-demo.acme.arr_snapshot`. The "marts/finance" thing is just the folder structure in dbt. BigQuery is flat.

**rajiv.menon** — 11:33 AM
Got it. That’s confusing, but okay. Fixed my SQL.

**jorge.martinez** — 11:45 AM
While you're in there, can you check why `acme.account_health` shows Cobalt Systems (cust_000700) as 'at_risk'? Tom says they're happy.

**lina.cho** — 12:00 PM
Checking `account_health`... they have an open P1 support ticket that’s been open for 72 hours. `at_risk` rule = `open_p1_over_48h OR recent_nps_detractor`.

**marcus.webb** — 12:05 PM
@marco.silva can you jump on that P1 for Cobalt? Tom’s trying to up-sell them 20 more seats next month.

---

### [2025-04-20] Q1 Bookings Review

**marcus.webb** — 04:00 PM
Lina, give me the final Q1 bookings by channel.

**lina.cho** — 04:15 PM
Total ACV Bookings: $1.8M.
- Outbound: $850k (huge quarter for Tom)
- Partner: $420k (Sarah’s Quartz Foundry deal helped here)
- Inbound: $300k
- Organic/Content/Other: $230k

**jorge.martinez** — 04:17 PM
Wait, $1.8M? I thought Sarah alone did $1M?

**lina.cho** — 04:19 PM
Sarah's "bookings" in her spreadsheet were MRR * 12 * 1.5 because she was trying to include the multi-year uplift. In `bookings_attribution`, we only count the first-year ACV.

**sarah.chen** — 04:21 PM
Wait, so for Quartz Foundry (cust_000714), I’m only getting credit for $144,000? They signed a 3-year deal!

**lina.cho** — 04:23 PM
Correct. $12,000 MRR * 12 = $144,000 ACV. The 3-year total contract value (TCV) is $432k, but sales commissions and board reporting are based on ACV.

**marcus.webb** — 04:25 PM
Standard policy, Sarah. We don't book the out-years upfront.

**sarah.chen** — 04:26 PM
Fine. But I’m still hitting my quota.

**jorge.martinez** — 04:30 PM
Also, just to be clear for everyone: `bookings_acv_usd` in the table is ALREADY annualized. Do NOT multiply it by 12 again. I saw a draft slide where someone had us doing $20M in bookings for Q1 because they multiplied the ACV by 12.

**marcus.webb** — 04:31 PM
LMAO. I wish.

---

### [2025-05-15] New "Engaged" Definition

**dan.lee** — 09:00 AM
@lina.cho @elena.volkov we're updating the "Engaged" definition in the `account_health` mart. The old one was too loose (anyone with 1 login).

**elena.volkov** — 09:15 AM
Agree. We’re seeing "Healthy" accounts churn because only one person was using it.

**lina.cho** — 10:00 AM
New logic is: `engaged` = (>=3 active users AND >=10 successful workflow runs) in the trailing 28 days.

**lina.cho** — 10:05 AM
I’m pushing the change to `acme.account_health` now. This will likely move about 40 accounts from 'stable' to 'monitoring'.

**jorge.martinez** — 10:10 AM
Does this impact Enterprise?

**lina.cho** — 10:12 AM
The `is_engaged` flag applies to everyone, but the `account_health_status` of 'critical' is different for Enterprise. For Enterprise, it's ONLY 'critical' if there's an uncollectible invoice. We don't mark them critical for low utilization because they often have huge seat counts they haven't rolled out yet.

**elena.volkov** — 10:15 AM
That makes sense for now, but we should keep an eye on it. If Onyx Robotics (cust_000704) has 500 seats and only 2 users, that's a problem even if they pay their bills.

---

### [2025-06-10] Expense Reports & Pizza (Noise)

**jorge.martinez** — 12:00 PM
Who ordered the 15 pizzas to the SF office? There’s no name on the receipt.

**sam.reyes** — 12:05 PM
That was me. Engineering was pulling an all-nighter for the 2.4 release. Just expense it to my card.

**jorge.martinez** — 12:06 PM
Thanks Sam. Just needed a paper trail for Rachel.

**lina.cho** — 12:10 PM
While you're in a spending mood, Sam, can we get the "Pro" Looker license for the CSM team? They're tired of sharing logins.

**sam.reyes** — 12:12 PM
Ask Rachel. If it's in the budget, fine.

---

### [2025-08-22] PLG vs. Sales-Led Math

**yuki.sato** — 02:45 PM
@lina.cho I’m looking at the `bookings_attribution` table and I don't see the expansion for Driftwood Media (cust_000702). I helped them set up their new workflow.

**lina.cho** — 03:00 PM
Yuki, Driftwood Media is a "Pro" tier customer. They upgraded their seats through the self-serve billing portal. `bookings_attribution` only tracks Opportunity-sourced, AE-led deals.

**yuki.sato** — 03:02 PM
But I spent two hours on Zoom with them!

**marcus.webb** — 03:05 PM
Yuki, if there wasn't an Opportunity in Salesforce that you closed, it's not a booking. That's a PLG conversion. It shows up in ARR, but not in your commissionable bookings.

**jorge.martinez** — 03:10 PM
This is why we need to move the MM accounts to Business tier faster. Pro is basically unmanaged.

---

### [2025-10-14] Series B & Data Cleanliness

**sam.reyes** — 08:30 AM
Big news today everyone. Series B is official. $80M total raised. Press release goes out at 9 AM.

**marcus.webb** — 08:35 AM
LFG! Time to scale.

**rachel.stein** — 08:45 AM
Congrats everyone. Now, back to work. @lina.cho, the investors are going to want a much deeper cut of churn by industry. Can we add `industry` to the `nrr_trailing_12` table?

**lina.cho** — 09:15 AM
It’s already in `dim_customers`. I can join it in.
Quick check of the data:
- Fintech is our best NRR (~120%)
- Media is our worst (~85%)
- Logistics is stable (~105%)

**jorge.martinez** — 09:20 AM
That Media churn is mostly the smaller Pro accounts. Like Juniper Collective (cust_000712) churning last month—they said they didn't have enough "workflows to automate."

**elena.volkov** — 09:25 AM
Juniper Collective was a "product fit" churn. They wanted more complex logic than we supported in Jan. We have those features now, but it's too late.

---

### [2025-12-05] End of Year Push

**marcus.webb** — 08:00 AM
Current Pipeline for Dec:
- Ember Industries (cust_000711): $300,000 ACV (Tom)
- Quartz Foundry (cust_000714) Renewal/Expansion: $50,000 ACV (Sarah)
- Sable Analytics (cust_000710): $160,000 ACV (Sarah)

Tom, where are we with Ember?

**tom.becker** — 08:15 AM
Ember is looking good. They just need to verify the SOC2 report. I sent it over yesterday. 350 seats confirmed. That’s $25k MRR.

**lina.cho** — 09:00 AM
If Ember closes on the 31st, does it count for 2025?

**rachel.stein** — 09:05 AM
Only if the `closed_won_at` timestamp is before midnight UTC.

**jorge.martinez** — 10:00 AM
I’m already dreading the Jan 1st reconciliation.

---

### [2026-01-20] Beacon Studios Churn Analysis (Signal: Not Product Dissatisfaction)

**elena.volkov** — 02:00 PM
Bad news. Beacon Studios (cust_000287) just submitted their churn notice.

**marcus.webb** — 02:05 PM
What?? They were at $116k ARR. They were "Healthy" in the dashboard.

**lina.cho** — 02:10 PM
Checking their health... yeah, they were 'stable'. Utilization band was 0.85. 65 seats, all active.

**marco.silva** — 02:15 PM
I just spoke with their admin. It’s not product dissatisfaction. Their parent company is consolidating all workflow tools onto a legacy platform. Procurement-driven churn. Nothing we could do.

**rachel.stein** — 02:20 PM
We need to flag that in the board deck. "Parent company consolidation" is a different bucket than "lost to competitor."

**jorge.martinez** — 02:25 PM
I'll add a `loss_reason` field to the churn tracker.

---

### [2026-02-14] Vrs Draft Spec (Distractor: Parked)

**nina.patel** — 10:30 AM
Hey @lina.cho, I see some columns in a draft table `vrs_band` and `champion_login_recency`. Are we using the Value Realization Score now?

**lina.cho** — 10:32 AM
NO. Stay away from those. That was a parked draft spec from Dan’s team. It’s not built out and the data is mostly nulls. Stick to `acme.account_health` for anything customer-facing.

**nina.patel** — 10:35 AM
Got it. Deleting that part of my script.

---

### [2026-03-10] NRR Re-calculation & Board Prep

**rachel.stein** — 04:00 PM
Lina, give me the latest ARR.

**lina.cho** — 04:15 PM
`nexus-analyst-demo.acme.arr_snapshot` says $39.2M.
- Business: $32.1M
- Enterprise: $6.2M
- Pro: $0.9M

**rachel.stein** — 04:17 PM
And NRR?

**lina.cho** — 04:20 PM
NRR is holding at 107%. Churn was a bit higher in Q1 (Beacon Studios hurt), but the Onyx Robotics expansion offset it.

**jorge.martinez** — 04:22 PM
Did Onyx expand again?

**lina.cho** — 04:23 PM
Yeah, Tom got them for another 50 seats. They're at 550 now.

---

### [2026-04-05] CRM Migration Final Push

**jorge.martinez** — 09:00 AM
Okay, I am doing the final cut-over for the `dim_customers` AE mapping. If the dashboards look weird for an hour, don't panic.

**sarah.chen** — 09:05 AM
Jorge, I just lost access to my lead views in SFDC.

**jorge.martinez** — 09:06 AM
I SAID DON'T PANIC SARAH.

**sarah.chen** — 09:07 AM
I HAVE A DEMO IN 10 MINUTES.

**jorge.martinez** — 09:10 AM
...Fixed. Try now.

---

### [2026-04-28] Random Queries & Noise

**marcus.webb** — 11:00 AM
Who's the AE on Verdant Cloud (cust_000707)?

**omar.haddad** — 11:02 AM
That’s mine. Why?

**marcus.webb** — 11:05 AM
I just saw their CEO post on LinkedIn about how much they love Acme. We should ask for a case study.

**omar.haddad** — 11:07 AM
I'll talk to Olivia (CSM). They're an Enterprise account in APAC, doing about $96k ACV ($8k MRR).

**lina.cho** — 11:10 AM
Verdant Cloud is a great account. 260 seats, but they use it for literally everything. Their `workflow_runs_daily` is through the roof.

**jorge.martinez** — 11:15 AM
@sarah.chen, did you ever tag the Quartz Foundry deal? It’s showing up as "Unattributed" in the attribution mart.

**sarah.chen** — 11:17 AM
It was a Partner deal. I tagged it in the "Partner Lead" field, not the "Primary Source" field.

**jorge.martinez** — 11:20 AM
*Internal screaming*

---

### [2026-05-02] Compensation & Redirect (Noise)

**sarah.chen** — 04:30 PM
Hey Jorge, I’m looking at the accelerator math for Q1. If I hit 120%, do I get the 1.5x on the whole amount or just the overage?

**jorge.martinez** — 04:32 PM
Sarah, that's a DM for me or Rachel. Let's not talk specific comp structure in the public #revenue-ops channel.

**sarah.chen** — 04:33 PM
Oops, sorry. Moving to DM.

---

### [2026-05-04] "Today's" Snapshot (Signal: $39M ARR)

**lina.cho** — 08:30 AM
Weekly Revenue Snapshot:
- Total ARR: $39.4M
- Paying Customers: 745
- Active Users: 16,204
- Health Status: 12 accounts 'Critical' (mostly SMB/Business with payment failures).

**rachel.stein** — 08:45 AM
12 critical is high. Who are they?

**lina.cho** — 09:00 AM
Mostly Pro and Business. No Enterprise accounts are critical right now. Tamarind Group is still 'Paused', so they aren't in the $39.4M.

**jorge.martinez** — 09:15 AM
I'm working with Finance to clear the Tamarind invoice. They had a credit card expiration issue. Should be back to 'Active' by tomorrow.

**marcus.webb** — 09:20 AM
Good. Let's keep the momentum. We have a big month ahead.

---

### [2025-02-28] Random Thread: SFDC Gripes

**tom.becker** — 02:15 PM
Why is the `industry` field a free-text box in some views? I see "fintech," "FinTech," "Fin-tech," and "Financial Services."

**jorge.martinez** — 02:17 PM
Because the legacy import from 2023 was a mess. I'm cleaning it up in the `dim_customers` logic. In the warehouse, it should all be mapped to the standardized `industry` enum.

**lina.cho** — 02:20 PM
Yeah, if you query `nexus-analyst-demo.acme.dim_customers`, you'll see I've consolidated those into clean buckets. Don't trust the raw SFDC export.

**tom.becker** — 02:22 PM
Thanks. My territory report was looking like a disaster.

---

### [2025-03-15] Monday Lunch Discussion (Noise)

**sarah.chen** — 11:45 AM
Lunch?

**omar.haddad** — 11:47 AM
Taco truck?

**sarah.chen** — 11:48 AM
Again? We had that twice last week.

**omar.haddad** — 11:49 AM
But it's *good*.

**jorge.martinez** — 11:50 AM
I’m stuck in a meeting with the HubSpot integration guys. Save me a burrito.

---

### [2025-07-12] Support Tickets & Account Health

**grace.liu** — 01:15 PM
@lina.cho why did Pebble Digital (cust_000705) drop to 'monitoring'?

**lina.cho** — 01:20 PM
Their utilization band dropped below 0.20. They have 6 seats but only 1 active user in the last 28 days.

**grace.liu** — 01:22 PM
Ah, okay. Their main admin is on maternity leave. I'll reach out to the backup.

**lina.cho** — 01:25 PM
Good catch. That's exactly why the health status exists!

---

### [2025-11-20] Churn Notification: Kestrel Networks

**tom.becker** — 10:00 AM
Kestrel Networks (cust_000708) is churning. Budget cuts.

**marcus.webb** — 10:05 AM
Another one? That’s $10k MRR gone.

**lina.cho** — 10:10 AM
Adding it to the `fact_subscriptions` with `change_type = 'churn'`. Their end date is Nov 30.

**rachel.stein** — 10:15 AM
We need to be tighter on the Business tier. These $100k-$150k ARR accounts are our bread and butter. If they’re cutting budget, we need to show them the ROI of the automation sooner.

---

### [2026-03-25] Audit Log Discussion

**priya.anand** — 03:00 PM
@jorge.martinez, the Enterprise guys are asking if we can surface the "audit log" data in their BI connector.

**jorge.martinez** — 03:05 PM
That data is huge. We don't currently sync the raw audit logs to the `nexus-analyst-demo.acme` dataset. We only have the `fact_workflow_runs` which is an aggregate.

**lina.cho** — 03:10 PM
Yeah, the warehouse would explode if we put every audit event in there. Tell them they can access it via the API or the Business/Enterprise UI.

**priya.anand** — 03:12 PM
Copy that.

---

### [2026-04-12] EMEA Update

**sarah.chen** — 08:00 AM
Good morning from London. Just closed Tamarind Group's (cust_000706) renewal. They’re moving back from 'Paused' to 'Active'.

**lina.cho** — 08:15 AM
Awesome. I’ll see that in the dbt run tonight.

**jorge.martinez** — 08:20 AM
Sarah, did you make sure the seat count stayed at 55?

**sarah.chen** — 08:22 AM
Yes. $8,195 MRR. Consistent with the Business tier pricing ($149/seat).

**jorge.martinez** — 08:25 AM
Perfect.

---

### [2026-05-04] Final Log Entry (Noise)

**lina.cho** — 04:45 PM
Anyone else notice that `fact_user_events` is running about 2 hours behind today?

**david.kim** — 04:50 PM
Yeah, the Kinesis stream had a hiccup. It's catching up. Should be live within the hour.

**lina.cho** — 04:52 PM
Cool. I'll wait to run the final Monday report until then.

**jorge.martinez** — 05:00 PM
I'm heading out. Happy Monday everyone.

**marcus.webb** — 05:05 PM
See ya. Go Acme.

### [2026-05-05] Q1 Board Deck Prep - NRR & ARR

**lina.cho** — 09:15 AM
@rajiv.menon @nina.patel starting the pull for the board deck NRR slides. Can someone sanity check why the `nrr_trailing_12` table is showing 1.07 but my manual scratchpad in Excel was hitting 1.15? 

**nina.patel** — 09:30 AM
Lina, are you doing an inner join on the cohort? If you only join customers who are active today to the list from 12 months ago, you're dropping the churned accounts. That inflates the number because you're only looking at survivors.

**lina.cho** — 09:35 AM
Ah, let me check the SQL. 
`SELECT ... FROM cohort_12mo a INNER JOIN current_mrr b ON a.customer_id = b.customer_id`
Yeah, that’s it. 

**nina.patel** — 09:40 AM
Standard trap. Use `nexus-analyst-demo.acme.nrr_trailing_12`—it’s the canonical board source. It uses a `LEFT JOIN` and `COALESCE(end_mrr_usd, 0)` so the churned accounts like Kestrel Networks (cust_000708) stay in the denominator. That’s why we’re at ~1.07.

**rachel.stein** — 09:50 AM
1.07 is the correct figure. We can’t show the board the survivor-bias version. Also, make sure the ARR split matches the snapshot. We’re at ~$39M total. $32M Biz / $6M Ent / $1M Pro. 

**lina.cho** — 09:55 AM
Copy that. Updating the slides now.

---

### [2026-05-07] Sales Sync: Bookings ACV confusion

**marcus.webb** — 11:00 AM
Huge shoutout to @tom.becker for closing the Ember Industries (cust_000711) expansion! $25k MRR added. 

**tom.becker** — 11:05 AM
Thanks Marcus! The logistics team there is really leaning into the webhook triggers. 

**jorge.martinez** — 11:10 AM
Wait, I’m looking at the `bookings_attribution` table in BQ for that deal. It says `bookings_acv_usd` is $300,000. If it’s $25k MRR, shouldn’t we be multiplying that by 12 in our CRM report? $300k * 12 is massive.

**lina.cho** — 11:15 AM
@jorge.martinez NO. Stop. `bookings_acv_usd` is ALREADY annualized. Do not multiply it by 12. If you do that, you’re going to tell Sam we had a $3.6M month when we actually had a $300k month.

**jorge.martinez** — 11:18 AM
Got it. My bad. The CRM field name is ambiguous. I'll stick to the BQ field.

---

### [2026-05-10] Expense Reports & Pizza

**sarah.chen** — 12:05 PM
Has anyone successfully used the new Expensify integration for the London office? It keeps rejecting my receipt for the Tamarind Group (cust_000706) renewal lunch.

**omar.haddad** — 12:10 PM
Sarah, you have to tag it under "Sales - EMEA" or it gets stuck in the APAC queue. 

**sarah.chen** — 12:12 PM
Thanks Omar. By the way, is the pizza arriving at 1 for the all-hands?

**marcus.webb** — 12:15 PM
Ordered 15 pies. Should be here. 

---

### [2026-05-12] Account Health Check - Quartz Foundry

**olivia.tran** — 02:00 PM
Hey @lina.cho, I’m looking at Quartz Foundry (cust_000714) in the `account_health` mart. They’re Enterprise, but their `utilization_band` is showing as NULL. Is the table broken?

**lina.cho** — 02:15 PM
Not broken. For Enterprise accounts, we don't calculate the utilization band because they have unlimited seats. The 'Critical' status for Ent only triggers on uncollectible invoices. Since Quartz is current on payments, they'll show up as 'Healthy' or 'Monitoring' based on engagement, but the band will be null.

**olivia.tran** — 02:20 PM
Got it. They had 12 successful runs yesterday so they definitely meet the `is_engaged` flag (>=3 users, >=10 runs).

**lina.cho** — 02:25 PM
Yep. If they were Business tier, we’d be checking `active_users_28d / seat_count_licensed`, but for them, it's irrelevant.

---

### [2026-05-14] BQ Path Errors

**david.kim** — 10:00 AM
Who is trying to run the `reconcile_v2` script? I’m seeing a ton of 404 errors in the logs.

**rajiv.menon** — 10:05 AM
That might be me. I was trying to pull from `nexus-analyst-demo.acme.marts.finance.arr_snapshot`.

**david.kim** — 10:10 AM
Rajiv, we’ve talked about this. The BigQuery dataset is FLAT. There is no `marts.finance` sub-directory in BQ. The folder structure in dbt is just for us. The table is just `nexus-analyst-demo.acme.arr_snapshot`.

**rajiv.menon** — 10:12 AM
Right, right. Too much time in the IDE, not enough time in the console. Fixing the path now.

---

### [2026-05-18] Pipeline Review: Onyx Robotics

**tom.becker** — 09:00 AM
Prepping for the Onyx Robotics (cust_000704) quarterly review. They're currently Enterprise at 500 seats ($35k MRR). They're asking about the "Value Realization Score" they saw in the last marketing deck. Where do I find that?

**elena.volkov** — 09:15 AM
You don't. The VRS is still a parked spec. `vrs_band` and `champion_login_recency` aren't live yet. Just use the `account_health` table as the proxy. If they’re `healthy_expansion`, tell them that. 

**tom.becker** — 09:20 AM
Okay, I'll stick to the engagement metrics then. They’ve got 420 active users over the last 28 days, so they're well above the engagement threshold.

---

### [2026-05-20] Coffee Machine Crisis

**marcus.webb** — 08:30 AM
The Jura in the kitchen is flashing a "System Restructuring" error. Anyone know the code?

**priya.anand** — 08:35 AM
Probably just needs a descale. I’ll open a ticket with building facilities. In the meantime, Blue Bottle is 2 blocks away.

**jorge.martinez** — 08:40 AM
I’m already there. Taking orders.

**lina.cho** — 08:42 AM
Large Oat Latte, Jorge! I'll pay you back on Venmo.

---

### [2026-05-22] Migration Update

**jorge.martinez** — 04:00 PM
Quick update on the CRM migration: I'm mapping the `acquisition_channel` from `dim_customers` today. Reminder that we only use the 8 canon channels: organic, paid_search, outbound, content, referral, partner, event, and inbound. 

**jasmine.park** — 04:10 PM
Jorge, what about "Podcast"? We had a few leads from the Q1 sponsorship.

**jorge.martinez** — 04:15 PM
Those get rolled into 'Content' per the last ops meeting. We’re keeping the warehouse schema clean. If you want to see the specific campaign, check `fact_marketing_touches.utm_campaign`.

**jasmine.park** — 04:20 PM
Fine. As long as the attributed revenue flows correctly to the top-level channel.

---

### [2026-05-25] Memorial Day Weekend Plans

**marcus.webb** — 04:45 PM
Anyone staying in the city for the long weekend?

**david.kim** — 04:50 PM
Heading up to Tahoe. Hopefully the snow isn't entirely slush by now.

**nina.patel** — 04:55 PM
Staycation for me. Catching up on some reading and definitely NOT looking at BigQuery.

**lina.cho** — 05:00 PM
I’m running one last ARR check before I head out. `arr_snapshot` is looking solid. See you all Tuesday!

---

### [2026-05-26] Post-Memorial Day Cleanup

**marcus.webb** — 09:15 AM
Welcome back everyone. Hope Tahoe was great, David. 

**david.kim** — 09:18 AM
Sunburnt and tired, but the slush wasn't too bad. Back at it.

**marcus.webb** — 09:25 AM
Lina, did you finish that `arr_snapshot` check? I need the final May month-to-date numbers for the leadership sync at 10.

**lina.cho** — 09:30 AM
Almost. I’m seeing a discrepancy in `nexus-analyst-demo.acme.fact_subscriptions`. There’s a record for "Cyberdyne-Systems" where the `mrr_usd` is listed as $12,500 but the `seat_count` is only 40. On the Business plan, they should be paying for at least 50. 

**jorge.martinez** — 09:35 AM
That was a legacy override from the Series A days. I'll manually map them to the 50-seat floor in the CRM so the warehouse logic doesn't break. 

**lina.cho** — 09:40 AM
Thanks. Also, Marcus, the NRR is hovering at 114% right now. We need that expansion from Omni-Global to close by Friday to hit the 116% target for the board deck.

---

### [2026-06-02] Pipeline & Booking Confusion

**tom.becker** — 11:00 AM
Just closed the Acme-Sub-Account expansion! Added $60k to the board. 

**lina.cho** — 11:05 AM
Wait, Tom. Is that $60k ACV or $60k Monthly? 

**tom.becker** — 11:07 AM
$60k Bookings ACV. 

**lina.cho** — 11:10 AM
Okay, so that’s only $5k added to the `current_mrr_usd` in `dim_customers`. You had it in the spreadsheet as a $60k monthly bump. My heart nearly stopped thinking we just jumped $720k in ARR from one mid-market deal.

**tom.becker** — 11:12 AM
My bad. I always get the `bookings_acv_usd` field mixed up with the monthly view in the legacy tracker. 

**marcus.webb** — 11:15 AM
This is why we’re moving everything to the `fact_invoices` table for source of truth. Tom, please double-check your entries in the CRM before Jorge runs the nightly sync.

---

### [2026-06-05] Offsite Planning & Expenses

**priya.anand** — 02:00 PM
Poll time: For the July offsite, do we want Napa or a Santa Cruz beach day? 

**jorge.martinez** — 02:05 PM
Santa Cruz. Better tacos.

**nina.patel** — 02:07 PM
Napa! I want to actually sit down. My legs are still killing me from the last "team building" hike.

**marcus.webb** — 02:15 PM
Keep it under $200/head for the day, please. Finance is tightening the "General & Administrative" belt after the Q1 spend on the Amsterdam office furniture.

**jasmine.park** — 02:20 PM
Does that include the bus? 

**marcus.webb** — 02:22 PM
Yes. Use the corporate card for the deposit, but I need the receipt in Expensify by EOD Friday.

---

### [2026-06-10] Data Integrity: Churn Logic

**nina.patel** — 09:45 AM
Hey Jorge, why is "Hooli-Logic" showing as `status = 'active'` in `nexus-analyst-demo.acme.dim_customers`? Their `churn_date` was set to 2026-05-15. 

**jorge.martinez** — 09:50 AM
Ah, they did a last-minute reversal on the cancellation. They downgraded from Enterprise to Business instead of churning completely. I updated `fact_subscriptions` with a `change_type = 'downgrade'`, but I must have forgotten to clear the `churn_date` in the customer master.

**lina.cho** — 09:55 AM
If they downgraded to Business, make sure the `seat_count_licensed` is at least 50. If they drop below that, the `current_plan_tier` logic might kick them back to Pro automatically, and they'll lose SSO. 

**jorge.martinez** — 10:00 AM
Fixed. They’re at 55 seats now. `current_mrr_usd` is now $8,195. 

---

### [2026-06-15] Q3 Quota Discussion

**marcus.webb** — 03:30 PM
AEs, listen up. Q3 quotas are being finalized. We’re looking at a 15% increase across the board for the MM (Mid-Market) team. 

**david.kim** — 03:35 PM
15%? Marcus, the lead flow from 'Organic' has been down since the website rebrand. 

**jasmine.park** — 03:40 PM
We're ramping up 'Paid Search' and 'Event' (the AWS Summit leads are hitting the CRM tomorrow). That should bridge the gap. 

**tom.becker** — 03:42 PM
Are we adjusting the Enterprise accelerators? Closing deals in 90 days is getting tougher with the new SOC2 legal review requirements. 

**marcus.webb** — 03:45 PM
We’re talking to Legal about streamlining the SLA annex. For now, focus on the `healthy_expansion` accounts in your book. Check the `nexus-analyst-demo.acme.fact_workflow_runs` table—anyone with a `step_count` growth > 20% MoM is a prime target for a seat bump.

**lina.cho** — 03:50 PM
And please, for the love of everything, check the `country` field. I’m seeing "SF" and "California" in `dim_customers`. We need ISO codes for the tax reporting. US, GB, NL. Keep it clean.

---

### [2026-07-01] Q2 Close & Bookings Reconciliation

**lina.cho** — 09:15 AM
@marcus.webb I’m looking at the preliminary Q2 bookings report. Why is the "Globex Corp" deal listed as $180,000 in your spreadsheet but only showing $15,000 in `nexus-analyst-demo.acme.fact_subscriptions`? 

**marcus.webb** — 09:22 AM
The $180k is the Bookings ACV (Annual Contract Value). They signed a 12-month Enterprise deal. The $15k is the MRR. 

**lina.cho** — 09:30 AM
Marcus, we’ve talked about this. Finance reports on GAAP revenue and MRR. If you put "180,000" in the `mrr_usd` column of the CRM export, it breaks the entire `fact_invoices` projection model. Jorge, can you please lock that field for non-admin users?

**jorge.martinez** — 09:35 AM
On it. I’ll add a validation rule: if `plan_tier = 'Enterprise'`, then `mrr_usd` cannot exceed $50,000 without a secondary approval from Ops. Also, for Globex, I’m seeing 300 seats in `seat_count_licensed`. That matches the Enterprise minimum.

**david.kim** — 10:15 AM
Wait, if we lock the field, how do I handle the "Initech" expansion? They’re adding 10 seats mid-month. It’s a tiny bump in MRR but I need it to show in my attainment.

**lina.cho** — 10:20 AM
Use the `change_type = 'expansion'` flag in the sub record. It’ll pick up automatically in the `nexus-analyst-demo.acme.fact_subscriptions` table during the midnight refresh. Just don't touch the ACV field manually.

---

### [2026-07-08] Board Deck Prep: NRR & Retention

**nina.patel** — 02:00 PM
Hey team, I'm pulling the Net Revenue Retention (NRR) for the Q2 Board Deck. I'm seeing a weird dip in the MM segment. 

**nina.patel** — 02:05 PM
Querying `nexus-analyst-demo.acme.dim_customers`:
```sql
SELECT 
  region, 
  SUM(current_mrr_usd) as total_mrr,
  AVG(seat_count_licensed) as avg_seats
FROM `nexus-analyst-demo.acme.dim_customers`
WHERE status = 'active' AND account_tier = 'MM'
GROUP BY 1
```
The EMEA numbers look soft. Did we lose a big account in Amsterdam?

**marcus.webb** — 02:10 PM
"Soylent Corp" churned last month. They were on a legacy Business plan with 150 seats. They moved to an internal tool. 

**lina.cho** — 02:15 PM
Soylent wasn't just a churn; they had $4,000 in unpaid invoices from Q1. I had to write that off. Nina, make sure you're looking at `fact_invoices` where `status = 'paid'` if you want the "actuals" for the board, not just the "committed" MRR.

**nina.patel** — 02:20 PM
Got it. I'll join `dim_customers` to `fact_invoices` on `customer_id` to filter out the bad debt.

---

### [2026-07-12] Internal: Offsite & Expenses

**jorge.martinez** — 11:00 AM
Reminder: The Sales & Ops Happy Hour is today at 5 PM at The Alchemist. @marcus.webb is buying the first round. 

**david.kim** — 11:05 AM
I'll be there. Quick question—can we expense the Uber since it's "team building"?

**lina.cho** — 11:10 AM
Only if the total expense is under $50 and you tag it as "Field Marketing - Internal" in Ramp. And I still see 14 outstanding receipts from the AWS Summit for you, David. No more happy hours until those are uploaded. 

**david.kim** — 11:12 AM
Fine. Doing it now.

---

### [2026-07-20] Data Hygiene: Industry Tags

**lina.cho** — 04:00 PM
@jorge.martinez, why are there 45 customers with `industry = 'Unknown'` in `dim_customers`? Most of these look like Fintech. 

**jorge.martinez** — 04:05 PM
That’s the data from the 'Self-Serve' signup flow. We don't require an industry selection for Pro plans to reduce friction. 

**lina.cho** — 04:10 PM
We need those for the tax nexus study. If they are 'Financial Services' in the UK, the VAT handling is different. 

**nina.patel** — 04:15 PM
I can run a Python script to enrichment those via the `email_domain` in `dim_users`. If I see `@starkind.com`, I’ll map it to 'Manufacturing/Tech'. I'll push the update to the `nexus-analyst-demo.acme.dim_customers` table tonight. 

---

### [2026-08-03] Pipeline Review: Q3 Targets

**marcus.webb** — 09:00 AM
Morning all. August 1st check-in. Our pipeline for Q3 is currently sitting at 2.2x coverage. We need to be at 3x by the end of the month to hit our $42M ARR target by EOFY.

**tom.becker** — 09:15 AM
I have "Wayne Enterprises" in 'Discovery'. Potential 500-seat Enterprise deal. But they’re asking about SOC2 Type II. Do we have the latest report?

**nina.patel** — 09:20 AM
The 2026 SOC2 report is in the `/legal-and-compliance` folder on GDrive. Note: our SLA is 99.9%. If they ask for 99.99%, that requires the "Platinum Support" add-on. 

**jasmine.park** — 09:30 AM
Marcus, I'm seeing a lot of high-intent signals from the `fact_workflow_runs` table. "Massive Dynamic" just hit 90,000 runs this month on a Business plan. They're going to hit their 100k quota by the 20th. 

**marcus.webb** — 09:35 AM
@david.kim, that's your account. Reach out and push the Enterprise upgrade today. Use the quota overage as the lever. 

**david.kim** — 09:40 AM
On it. I'll check their `step_count` in `nexus-analyst-demo.acme.fact_workflow_runs` to see if they're doing heavy data processing. That’s usually a good sign they need dedicated infra.

---

### [2026-08-10] Ops Update: Warehouse Maintenance

**jorge.martinez** — 10:00 AM
Heads up, we are migrating the `user_id` mapping logic in `dim_users`. Some `last_login_date` values might look null for about an hour while the dbt job runs. 

**lina.cho** — 10:05 AM
Does this affect the `is_active` flag? I use that for the per-seat billing reconciliation for the "Pro" accounts. 

**jorge.martinez** — 10:10 AM
It shouldn't. I'm just cleaning up the `invited_by_user_id` self-joins. The `current_mrr_usd` in `dim_customers` will remain the source of truth for your billing run.

**nina.patel** — 10:15 AM
While you’re in there, can you fix the `region` for the Netherlands? We have both 'NL' and 'Netherlands' in the raw logs. It's making the `region` aggregation in my Looker dashboard look like we have two different countries. 

**jorge.martinez** — 10:20 AM
Fixed. Standardizing to ISO codes across all `dim` tables. 

---

### [2026-08-15] Mid-Month Panic

**david.kim** — 04:45 PM
Hey, why did "Umbrella Corp" just drop from my active pipeline? 

**jorge.martinez** — 04:50 PM
They were marked as `status = 'paused'` in `dim_customers`. Their credit card on file expired and the three-day grace period for the Business plan ended. 

**lina.cho** — 04:55 PM
They owe us $7,450. David, if you want them back in your pipeline, you need to get them to update their payment method in the Billing Portal. I’m not unpausing them manually again.

**david.kim** — 05:00 PM
Calling them now. They’re a huge expansion lead, we can't let them churn over a stale Visa card.

---

### [2025-11-12] Q4 Pipeline Review

**marcus.webb** — 09:00 AM
@sales-team looking at the forecast in the "Global Sales" dashboard. We are sitting at $3.2M for the quarter but the commit is $4.5M. We have 6 weeks left. David, what’s the status on "Soylent Corp"?

**david.kim** — 09:15 AM
Soylent is still technically in 'Discovery', but they’re moving fast. They have 400 users on a 'Free' trial right now. I checked `nexus-analyst-demo.acme.fact_user_events` and their `event_type = 'workflow_published'` is through the roof. 

**marcus.webb** — 09:20 AM
They have 400 users and they’re on Free? Why haven't they been capped by the 100 runs/mo limit?

**jorge.martinez** — 09:25 AM
That’s on me. I haven't implemented the hard-stop for the new sandbox environments yet. If you look at `nexus-analyst-demo.acme.fact_workflow_runs`, Soylent did 12k runs yesterday.

**lina.cho** — 09:30 AM
Jorge, we are literally giving away $20k of compute. David, get them on an Enterprise contract by Friday or I’m throttling their `customer_id`.

**david.kim** — 09:35 AM
Whoa, Lina, calm down. If you throttle them now, the POC dies. I’m pitching them a $120k ACV deal. Let me handle the "value-based" conversation. 

---

### [2026-01-05] 2025 Year-End Board Prep

**lina.cho** — 11:00 AM
@jorge.martinez I need the final Net Revenue Retention (NRR) for FY2025. My spreadsheet says 118%, but the Looker tile is showing 112%. 

**jorge.martinez** — 11:15 AM
The Looker tile is pulling from `nexus-analyst-demo.acme.fact_subscriptions`. It might be counting the "Umbrella Corp" pause as a churn event because their `end_date` was nullified during the credit card lapse.

**lina.cho** — 11:20 AM
That explains it. "Umbrella Corp" is $89k ARR. If they are marked as churned, it tanks the NRR. Can we exclude `status = 'paused'` from the denominator?

**jorge.martinez** — 11:30 AM
I’ll update the dbt model. Also, I noticed some AE names are missing in `dim_customers.ae_employee_id`. Marcus, can you make sure the team fills out the CRM? I can’t attribute commissions if the field is null.

**marcus.webb** — 11:35 AM
I’ll ping them. By the way, is the "Team Lunch" expense from December 15th approved? We went to "The Salty Pig" to celebrate the $35M ARR milestone.

**lina.cho** — 11:40 AM
I see the receipt. $1,400 for 12 people? Marcus, that’s over the $100/head limit. I’ll approve it this once, but next time stick to the "Business" tier of dining.

---

### [2026-02-14] Valentines & CRM Migrations

**nina.patel** — 02:00 PM
Is anyone else seeing weird numbers for "Globex"? `dim_customers` says their `current_mrr_usd` is $4,950, but they only have 10 licensed seats. 10 * $149 (Business) should be $1,490. 

**jorge.martinez** — 02:10 PM
Checking... Ah, they are on a legacy "Pro" plan but they negotiated a custom data retention add-on that’s being piped into the MRR field. 

**lina.cho** — 02:15 PM
No, that’s wrong. Custom add-ons should be in a separate line item in `fact_invoices`. We shouldn't be inflating `current_mrr_usd` with non-seat revenue. It messes up our ARPU (Average Revenue Per User) metrics.

**jorge.martinez** — 02:20 PM
I’ll move the add-on revenue to a `metadata` column in `fact_subscriptions` so it doesn't pollute the per-seat calcs. 

**david.kim** — 02:30 PM
Quick update: Just closed "Initech" for 300 seats! They went straight to Enterprise. @marcus.webb, that should put me at 110% of my Q1 quota already.

**marcus.webb** — 02:35 PM
Nice work, David. Did you get the `acquisition_channel`? We need to know if that came from the "SaaS-Con" webinar or if it was an outbound cold call. 

**david.kim** — 02:40 PM
It was an inbound request. Someone from their dev team saw our `step_count` efficiency blog post.

---

### [2026-03-20] Quarter-End Chaos

**david.kim** — 04:00 PM
@lina.cho I have "Hooli" ready to sign, but they’re arguing about the `sla_uptime_pct`. They want 99.99% but our `dim_plans` for Enterprise only lists 99.9%. 

**lina.cho** — 04:05 PM
99.99% requires a dedicated infra cluster. That’s an extra $5k/month. Tell them if they want the extra '9', they have to pay for it. 

**david.kim** — 04:10 PM
They’re already paying $250k ACV. Can’t we just bundle it? 

**marcus.webb** — 04:15 PM
Bundle it. We need the booking to hit the $40M ARR goal. We’re at $39.2M right now. This deal puts us over the edge.

**jorge.martinez** — 04:20 PM
If we do that, I need to update the `dim_plans` table to reflect a new 'Enterprise Plus' tier or something. Otherwise, the automated uptime monitors in `fact_workflow_runs` will trigger alerts for the wrong threshold.

**lina.cho** — 04:25 PM
Fine. David, send the DocuSign. Jorge, don't update the table yet—wait until the invoice is `status = 'paid'` in `fact_invoices`. I don't want to report higher ARR to the board until the cash is in the bank. 

**nina.patel** — 04:45 PM
Wait, if we’re at $40M ARR, does the whole company get the Amsterdam offsite trip? 

**marcus.webb** — 04:50 PM
Only if we hit it by March 31st. Tell your AEs to stop sandbagging and pull those April deals forward. 

**jorge.martinez** — 05:00 PM
Btw, I'm taking Friday off for a hiking trip. If the dbt DAG fails, someone ping the `eng-on-call` alias. The `dim_users` refresh has been flaky because of the `email_domain` parsing logic. 

**lina.cho** — 05:05 PM
Noted. David, still waiting on that "Initech" signed contract. The `fact_subscriptions.is_current` flag won't flip until I see the PDF.

---

### [2026-04-02] Q1 Post-Mortem & The "Amsterdam" Verdict

**marcus.webb** — 09:15 AM
Okay team, the dust has settled on Q1. @jorge.martinez, give us the final number from the `nexus-analyst-demo.acme.fact_subscriptions` snapshot. Did Hooli and Initech land in time?

**jorge.martinez** — 09:42 AM
It’s tight. If I run `SELECT sum(mrr_usd) * 12 FROM nexus-analyst-demo.acme.fact_subscriptions WHERE is_current IS TRUE`, I’m getting $39,942,000. 

**lina.cho** — 09:45 AM
Wait, that can't be right. I see the Initech invoice for $12k MRR marked as `status = 'paid'` in `fact_invoices` on March 31st at 11:58 PM. 

**jorge.martinez** — 09:50 AM
The `fact_subscriptions` table refreshes at 2:00 AM. The `start_date` for Initech was set to April 1st by the AE. Since the snapshot for March 31st didn't see an active record, it's technically a Q2 booking in the warehouse.

**marcus.webb** — 09:55 AM
Are you kidding me? We missed the $40M goal because of a `start_date` typo? @nina.patel was that your deal?

**nina.patel** — 10:05 AM
I set it to April 1st because their procurement lead said they didn't want to "start" the service until the new quarter for tax reasons. I didn't know the Amsterdam trip was riding on a 24-hour difference! 

**lina.cho** — 10:10 AM
I’ll talk to the CFO. We can probably 做 (do) a manual adjustment for the board deck. If the cash is in the bank in March, it counts for the internal bonus. Nina, next time, just set the `start_date` to the signature date. We handle the "service start" via the `fact_workflow_runs` entitlement anyway.

**marcus.webb** — 10:15 AM
Crisis averted. Amsterdam is ON. Start looking at flights for the first week of June. Nina, check the `dim_employees` list to see who needs a Schengen visa sponsorship letter from HR.

---

### [2026-04-10] NRR Prep for Board Meeting

**lina.cho** — 02:00 PM
@jorge.martinez I need the Net Revenue Retention (NRR) for the "Enterprise" segment over the last 12 months. The board is asking why the `account_tier = 'MM'` is growing faster than `account_tier = 'Ent'`.

**jorge.martinez** — 02:30 PM
The NRR for Enterprise looks weird because of the "Soylent Corp" churn back in November. They were $150k ACV. 
I’m looking at `nexus-analyst-demo.acme.fact_subscriptions`. 
Current Enterprise MRR: $512,000. 
One year ago: $440,000. 
But we had $60k in expansion from "Globex" and "Tyrell Corp". 

**lina.cho** — 02:45 PM
Wait, did you count the "Hooli" expansion? They went from Business to Enterprise.

**jorge.martinez** — 03:00 PM
That's the issue. In `fact_subscriptions`, that shows up as `change_type = 'upgrade'`. If I just look at the `customer_id` cohort from 12 months ago, Hooli was only paying $8k MRR then. Now they are $20.8k MRR. That’s a 160% expansion for that one account. 

**lina.cho** — 03:10 PM
Send me the raw CSV of the cohort. I need to strip out the churned accounts for the "Gross Retention" slide but keep them in for "Net Retention". Also, Marcus wants to show "Logo Retention" which is just `count(distinct customer_id)` from `dim_customers` where `status = 'active'`.

**jorge.martinez** — 03:20 PM
Will do. I’m also seeing some noise in `dim_customers`. There are 5 accounts with `current_plan_tier = 'Enterprise'` but `current_mrr_usd = 0`. I think these are the "Partner" accounts we gave away for free. We should exclude those from the NRR calc or it'll tank the averages.

---

### [2026-04-15] Expense Report Nagging & Salesforce Cleanup

**david.kim** — 11:00 AM
Has anyone seen my receipts from the "SaaS-Con" dinner? I’m trying to clear this Expensify alert before the Friday cutoff.

**nina.patel** — 11:05 AM
Check the #general-social channel, someone posted a photo of the table. You can probably see the bill in the background lol.

**lina.cho** — 11:15 AM
@sales-team-all Reminder: If you don't update the `acquisition_channel` field in the CRM by Friday, your commissions for April won't be calculated. We have 40+ deals sitting in `fact_subscriptions` where the `acquisition_channel` is `NULL`. 

**jorge.martinez** — 11:20 AM
Yeah, it makes the "Marketing Attribution" dashboard look like 90% of our revenue comes from "Unknown". @david.kim, "Massive Dynamic" is one of them. Was that a cold call or the "Step Count" whitepaper?

**david.kim** — 11:25 AM
That was a referral from their CTO. I'll update it to "Social/Word of Mouth".

**lina.cho** — 11:30 AM
Is "Social" even a valid option in `dim_customers`? 

**jorge.martinez** — 11:35 AM
No. Use `Referral`. I'm going to update the dbt model tonight to point any `NULL` channels to `Organic_Search` as a fallback, but it’s going to mess up the LTV/CAC ratios. 

**marcus.webb** — 11:45 AM
Don't fallback to Organic. Just leave it as `Unknown`. I’d rather show the board we have a data entry problem than give Marketing credit for stuff they didn't do. 

---

### [2026-04-20] Capacity Planning / "The Jorge Migration"

**jorge.martinez** — 01:00 PM
Heads up, I'm doing a major migration on the `fact_workflow_runs` partitioning. The table is getting too big and it's slowing down the daily `dim_users` refresh. 

**lina.cho** — 01:10 PM
How long will it be down? I have a meeting with the "Aperture Science" CSM at 3:00 PM and I need to see their `step_count` usage for the last 30 days.

**jorge.martinez** — 01:15 PM
The table in `nexus-analyst-demo.acme.fact_workflow_runs` will be read-only for about 45 minutes. If you need usage stats, use the `snapshot_usage_daily` table. It’s 24 hours old but it’ll have the `error_code` trends you need.

**lina.cho** — 01:20 PM
Fine. Also, @marcus.webb, "Aperture" is complaining about the $149/seat price. They want to move 1,000 users over from a legacy system but they want the `Enterprise` price point ($50/seat) without the `Enterprise` support contract.

**marcus.webb** — 01:25 PM
No way. If they want the 1,000 seats, they take the Enterprise Tier. It’s not just about the price-per-seat, it’s about the `sla_uptime_pct`. If they stay on Business at that scale, their `fact_workflow_runs` volume will trigger the concurrency limits and they’ll be screaming at Support in a week. 

**david.kim** — 01:30 PM
I’ll jump on the call. I can sell them on the "Custom SLA" as the value-add. They’re obsessed with uptime ever since that `error_code = 503` spike in February. 

**jorge.martinez** — 01:35 PM
That 503 spike was because their dev team tried to run 50,000 `step_count` increments in a single loop. Not our fault. But yeah, use it as leverage. 

---

### [2026-04-25] The Amsterdam Flight Spreadsheet

**nina.patel** — 04:00 PM
@here I’ve shared the "Acme Amsterdam 2026" Google Sheet. Please put your passport name and dietary restrictions in by Monday. 

**david.kim** — 04:05 PM
Are we staying at the same hotel as last time? The one near the canal?

**nina.patel** — 04:10 PM
No, Finance (Lina) cut the budget slightly because of the "Soylent Corp" churn, so we're staying a bit further out. But it's near the EMEA office, so no excuses for being late to the morning workshops.

**jorge.martinez** — 04:15 PM
As long as the WiFi works. I still have to manage the `fact_user_events` pipeline while we're there. 

**lina.cho** — 04:20 PM
Jorge, you are forbidden from touching BigQuery during the Heineken tour. 

**jorge.martinez** — 04:25 PM
Tell that to the `fact_invoices` table. It doesn't care about beer.

---
### [2026-05-01] New Month, New Quotas

**marcus.webb** — 09:00 AM
Happy May. Quotas for Q2 are live in the `dim_employees` metadata. Most AEs are seeing a 15% bump. 

**nina.patel** — 09:10 AM
15%?? I’m already at 110% capacity with my current accounts. 

**marcus.webb** — 09:15 AM
The "Hooli" deal proved there’s more meat on the bone in the Enterprise segment. We’re also launching the "Storage GB" upsell in June. Jorge is adding a `storage_gb` column to `fact_subscriptions` as we speak. That’s easy money.

**jorge.martinez** — 09:20 AM
`storage_gb` is added to `dim_plans` now. I’m still backfilling `fact_subscriptions`. Don't start selling it yet, I haven't finished the automated billing trigger for when a customer exceeds their `storage_gb` quota. 

**lina.cho** — 09:25 AM
Marcus, we need to talk about the "Pro" tier. The `current_mrr_usd` is flat-lining. I think we need to raise the seat price from $49 to $59. 

**marcus.webb** — 09:30 AM
Let’s wait until after the Amsterdam trip. I don't want a PR fire to deal with while I'm in a stroopwafel coma.

---
### [2026-05-04] NRR and Board Deck Panic

**marcus.webb** — 10:15 AM
@jorge.martinez I’m pulling NRR (Net Retention Rate) for the Q1 board deck. When I sum `mrr_usd` from `nexus-analyst-demo.acme.fact_subscriptions` for April 2026 and divide by March, I’m getting 104%. That feels low given the Hooli expansion. 

**jorge.martinez** — 10:22 AM
That’s because you’re probably just looking at `is_current = true`. You need to account for the `change_type` column. Hooli did a mid-month expansion, so their record in `fact_subscriptions` for April might have multiple entries if they added seats on the 15th. 

**lina.cho** — 10:25 AM
Also, Marcus, make sure you aren’t accidentally including the "Soylent Corp" churn in the numerator. They officially dropped to $0 on April 1st. If you want the "clean" NRR, use the `dim_customers.status` filter to exclude them from the starting cohort.

**marcus.webb** — 10:30 AM
Got it. Jorge, is there a view that handles the "expansion" vs "new biz" split? 

**jorge.martinez** — 10:35 AM
Look at `nexus-analyst-demo.acme.fact_subscriptions` and join on `changed_from_subscription_id`. If `mrr_usd` > `previous_mrr_usd`, it's expansion. I haven't finished the materialized view for this because I was busy fixing the `dim_users` sync—apparently, 400 people from "Globex" signed up with personal Gmail accounts and it broke the `email_domain` logic. 

**david.kim** — 10:40 AM
@nina.patel Did you see the Slack from the Amsterdam hotel? They don't have enough twin rooms, so some of us might have to share. 

**nina.patel** — 10:42 AM
Not happening. Finance can find the extra €50 for singles. I am not listening to Marcus snore for four nights.

---

### [2026-05-12] The Bookings vs. MRR Incident

**marcus.webb** — 02:00 PM
HUGE NEWS. Nina just closed a $240k deal with "Aperture Science". Massive win for the MM segment. Putting it in the #wins channel now. 

**lina.cho** — 02:15 PM
Hold on. I just looked at the contract in the legal folder. That’s $240k **ACV** (Annual Contract Value), but they are on a multi-year ramp. The Year 1 `mrr_usd` is only $12k/mo because they only licensed 80 seats to start. 

**marcus.webb** — 02:20 PM
Wait, Nina told me it was $20k MRR. 

**nina.patel** — 02:22 PM
It averages to $20k over the three years! Year 3 is like $28k MRR. 

**lina.cho** — 02:25 PM
Marcus, we report to the board on *Current* ARR/MRR. You cannot put $240k in the "New Bookings" slide for Q2 if the immediate impact on `fact_invoices` is only $12k. The `nexus-analyst-demo.acme.fact_subscriptions` table will flag this immediately during the audit. 

**jorge.martinez** — 02:30 PM
Already caught it. I’m tagging the Aperture record with `change_type = 'new'` but setting the `mrr_usd` to 12000. Sorry Marcus, the data doesn't lie. 

**marcus.webb** — 02:35 PM
Fine. But I’m still putting $240k in the #wins channel. Let the AEs have their moment. 

---

### [2026-05-20] Storage GB Backfill & "Ghost" Users

**jorge.martinez** — 11:00 AM
The `storage_gb` backfill in `fact_subscriptions` is 90% done. I found about 50 Enterprise customers who have been using 500GB+ for free for the last two years. 

**lina.cho** — 11:05 AM
Music to my ears. @marcus.webb, those are your upsell targets for June. 

**marcus.webb** — 11:10 AM
Wait, if we start charging them now, will they churn? "Initech" is already grumpy about the uptime issues we had in March (the `fact_workflow_runs` error 504 spike). 

**nina.patel** — 11:15 AM
Initech is fine. I checked `fact_user_events` and their daily active users (DAU) is up 20% MoM. They are too hooked on the Jira-to-Slack automation to leave over a storage fee. 

**jorge.martinez** — 11:20 AM
Actually, speaking of Initech, I’m seeing 15 users in `dim_users` associated with them who haven't logged in since 2024. `is_active` is true but `last_login_date` is ancient. We should probably "ghost" them before the seat audit so we don't look like we're overcharging for dead seats. 

**lina.cho** — 11:25 AM
No way. If they are licensed in `seat_count_licensed`, we charge for them. If the customer wants to de-provision them, that’s on their admin. Don't touch the revenue, Jorge. 

---

### [2026-05-28] Amsterdam Logistics / Expense Reporting

**nina.patel** — 09:00 AM
Reminder: Use the Expensify tag "AMSTERDAM-2026" for all travel costs. Lina will reject anything that just says "Travel". 

**david.kim** — 09:15 AM
Is the Heineken Experience covered? 

**lina.cho** — 09:20 AM
Only the ticket. If you buy a personalized bottle with "Acme Top Closer" on it, that’s on you, David. 

**jorge.martinez** — 09:25 AM
Hey, I just noticed a weird discrepancy in `dim_employees`. Some of the EMEA hires are listed in USD but paid in EUR. It’s making the `nexus-analyst-demo.acme.fact_invoices` margin calculation look slightly off for the Amsterdam office. 

**lina.cho** — 09:30 AM
I’ll fix the `dim_employees` metadata. We’re using a fixed exchange rate of 1.08 for 2026 to keep the reporting simple. Don't try to pull live FX rates into BigQuery again, Jorge. Remember what happened last time the API failed? 

**jorge.martinez** — 09:35 AM
The `fact_subscriptions` table was null for 6 hours. I remember. I still have the ptsd from the Slack pings. 

---

### [2026-06-02] June Kickoff & The "Pro" Price Hike

**marcus.webb** — 08:30 AM
Welcome to June. We are officially raising the Pro price from $49 to $59 today for new signups. 

**nina.patel** — 08:45 AM
Is it live in the `dim_plans` table? I don't want to quote a customer $49 and then have the automated invoice show $59. 

**jorge.martinez** — 08:50 AM
It’s live in `dim_plans`. I also added a `plan_version` column to `fact_subscriptions` so we can track who is grandfathered in at the $49 rate. Warning: the `current_mrr_usd` column in `dim_customers` might look "lumpy" this month as people switch or churn. 

**lina.cho** — 09:00 AM
We need to monitor the "Free-to-Pro" conversion rate closely. If it drops below 3%, Marcus, we might have to rethink the `storage_gb` limits on the Free tier to "nudge" them more. 

**marcus.webb** — 09:10 AM
The Free tier is already pretty restricted—100 runs/mo is nothing. If they are doing anything useful, they hit that limit by the 10th of the month. I can see it in `fact_workflow_runs`. We have 200 "Free" customers who have been "Over Quota" for three months straight. 

**jorge.martinez** — 09:15 AM
I’ll run a query on `fact_workflow_runs` to identify the top 50 "Quota Offenders" and send the list to the SDRs. That's low-hanging fruit. 

**david.kim** — 09:20 AM
Can we do this after we get back from Amsterdam? I’m already halfway out the door. 

**nina.patel** — 09:25 AM
David, you're not leaving until Friday. Get back to your CRM cleanup. Half of your "Stage 3" deals haven't had a `last_activity_date` update in 2 weeks. 

---

### [2026-06-05] Final Board Numbers

**lina.cho** — 04:00 PM
Final NRR for Q1 came in at 107%. The expansion from "Hooli" really saved us after the "Soylent Corp" disaster. 

**marcus.webb** — 04:10 PM
107% is solid. The board likes anything over 105%. 

**jorge.martinez** — 04:15 PM
Just FYI, I had to manually adjust the `current_mrr_usd` for three accounts because they were paying in GBP and the conversion was weirdly high in the `fact_invoices` table. It’s clean now in `nexus-analyst-demo.acme.dim_customers`. 

**nina.patel** — 04:20 PM
Awesome. See you all at SFO. Amsterdam, here we come. 

**david.kim** — 04:25 PM
I forgot my passport. Just kidding. See ya.

---

### [2026-06-12] Post-Amsterdam Hangover & Expense Reports

**david.kim** — 09:00 AM
Is anyone else still vibrating from the flight back? My internal clock is set to "stroopwafel time." 

**nina.patel** — 09:05 AM
David, I’m looking at your Expensify. Why is there a €450 line item for "Team Building - Canal Tour" when the whole company event was already prepaid by Lina? 

**david.kim** — 09:08 AM
That was for the private boat after the official one. We were talking strategy! I have notes on a napkin about the "Globex" expansion. 

**lina.cho** — 09:15 AM
Declined. Also, I’m seeing a lot of "Late" flags on corporate cards. If you don't reconcile by Friday, Finance is going to start pulling seats from your department's LinkedIn Sales Navigator budget. 

**jorge.martinez** — 10:00 AM
I’m back in the warehouse today. The `dim_customers` table is still showing "Soylent Corp" as `Active` even though they churned last month. Whoever handled that offboarding forgot to update the status in Salesforce. 

**marcus.webb** — 10:05 AM
That was Sarah’s account. I’ll bug her. Hey Jorge, did you ever run that "Quota Offender" list from `fact_workflow_runs`? 

**jorge.martinez** — 10:15 AM
Yeah, just dumped it into a Sheet for the SDRs. There are 42 accounts on the Free tier that did over 5,000 runs last month. The limit is 100. We are basically giving away $20k in MRR because our "hard cap" is actually a "polite suggestion" right now. 

**lina.cho** — 10:20 AM
We need to enforce the `workflow_run_quota_per_month` in the product. Engineering says it’s a "sprint 14" item, but that’s too late. 

---

### [2026-06-18] Q3 Pipeline & Booking Confusion

**nina.patel** — 11:00 AM
Pipeline review. David, you’ve got "Globex" in Stage 4 for $1.2M. That would put us way over the H2 goal. Is that a real number? 

**david.kim** — 11:05 AM
Locked and loaded. They want the Enterprise tier for 3,000 seats. 

**lina.cho** — 11:10 AM
Wait, $1.2M MRR or ACV? 

**david.kim** — 11:12 AM
MRR, obviously. 

**nina.patel** — 11:15 AM
David. If you closed a $1.2M *MRR* deal, you would be the CEO of this company by tomorrow. Check the `bookings_acv_usd` field in the CRM. You’re confusing Annual Contract Value with Monthly Recurring Revenue again. 

**jorge.martinez** — 11:20 AM
Confirmed. I just checked the staging table `nexus-analyst-demo.acme.fact_subscriptions` for the draft quote. It’s $1.2M ACV. That’s ~$100k MRR. Still a massive deal, but let’s not tell the board we’re $12M richer than we are. 

**david.kim** — 11:25 AM
My bad. ACV. Still, it’s a whale. 

**marcus.webb** — 11:30 AM
Is Globex requiring SOC2? I know they were sniffing around the "Audit Log" feature in the Business tier but then moved to Enterprise for the custom SLA. 

**nina.patel** — 11:35 AM
They need SOC2 and the dedicated CSM. I’m assigning Elena to them once the signature hits. Jorge, can you make sure `dim_customers.account_tier` updates to 'Ent' the second the `fact_invoices` record is marked `paid`? I don't want them getting the generic support alias.

**jorge.martinez** — 11:40 AM
The dbt model for `dim_customers` runs every 2 hours. It’ll pick up the `plan_tier` change from `fact_subscriptions`. If they pay by wire, it might take a day for Finance to flag it as `paid_at` in `fact_invoices`. 

---

### [2026-06-25] NRR Board Prep

**lina.cho** — 02:00 PM
Jorge, I need a bridge chart for NRR. Can you break down the "Expansion" vs "Churn" vs "Downgrades" for Q2 so far? 

**jorge.martinez** — 02:30 PM
I’m looking at `nexus-analyst-demo.acme.fact_subscriptions`. 
- New Business: $2.1M
- Expansion (mostly Hooli and Cyberdyne): $450k
- Churn (Soylent + 12 SMBs): -$180k
- Contraction: -$45k (a few Pro users dropping seats)

Net MRR growth is looking healthy, but the Hooli expansion was a one-time seat true-up. We can't rely on that every quarter. 

**marcus.webb** — 02:35 PM
We have a huge gap in the "Pro" tier. `current_mrr_usd` for Pro is flat. It’s all Business and Enterprise doing the heavy lifting. We need more self-serve velocity. 

**lina.cho** — 02:40 PM
I’m worried about the `country` distribution. 60% of our churn is coming from the APAC region. Are we failing on support hours there? 

**nina.patel** — 02:45 PM
It’s the latency. Customers in Sydney are complaining about `duration_ms` in `fact_workflow_runs` being double what the US East users see. If we don’t deploy an APAC cluster, we’re going to lose that whole segment. 

**david.kim** — 02:50 PM
Off topic, but the coffee machine on the 4th floor is leaking again. 

**nina.patel** — 02:52 PM
David, put in a Jira ticket for Facilities and get back to the Globex contract. They haven't opened the DocuSign yet. 

---

### [2026-07-02] CRM Migration Issues

**jorge.martinez** — 09:00 AM
Nobody touch the `acquisition_channel` field in Salesforce today. I’m running a mass update to align it with our `dim_customers` logic. 

**marcus.webb** — 09:05 AM
Wait, I’m mid-call with "Initech." If I change something, will it overwrite? 

**jorge.martinez** — 09:10 AM
Yes. Stay out of the "Details" tab. I’m trying to fix the attribution. 30% of our customers are marked as "Unknown" because the `invited_by_user_id` in `dim_users` wasn't being tracked correctly for referral loops. 

**lina.cho** — 09:15 AM
Jorge, while you're in there, can you check why "Tyrell Corp" has a `current_mrr_usd` of $0 but is listed as `Business` tier? 

**jorge.martinez** — 09:20 AM
Checking `fact_subscriptions`... looks like they have a 100% discount code applied for 12 months. Signed by the VP of Sales in 2025. 

**nina.patel** — 09:22 AM
That was a "strategic partnership" deal. It expires in August. David, make sure you have a renewal call booked for Tyrell. We need to move them to at least $10k MRR or cut them off. They’re running 500k workflows a month—the COGS is killing us. 

**david.kim** — 09:25 AM
On it. I'll tell them the free ride is over. Or, "evolving our partnership." 

**lina.cho** — 09:30 AM
Use the "evolving" one. 

**jorge.martinez** — 09:45 AM
Final note: the `nexus-analyst-demo.acme.dim_employees` table is updated. Nina, you have two new SDRs starting Monday. Get their seats ready.

---

### [2026-07-15] Q3 Board Prep & NRR Reconciliation

**lina.cho** — 10:15 AM
@jorge.martinez I’m looking at the draft NRR (Net Revenue Retention) for the Q3 board deck. Why is it showing 112%? My manual tracker for the Enterprise segment had us closer to 118% after the "Wayne Enterprises" expansion.

**jorge.martinez** — 10:22 AM
The delta is in the `change_type` column in `nexus-analyst-demo.acme.fact_subscriptions`. We had three churns in the SMB tier that were backdated to June because the credit card failures weren't caught until the `fact_invoices` reconciliation this week. 

**lina.cho** — 10:25 AM
Wait, if they churned in June, they shouldn't hit Q3 NRR calculations. Are we using `subscription_id` or `customer_id` as the primary key for the cohort?

**jorge.martinez** — 10:30 AM
I’m using `customer_id`. The issue is "Hooli" downgraded from Business to Pro last month, but then added 50 seats this month. It’s messy. I’m trying to calculate the `mrr_usd` delta. If you look at `nexus-analyst-demo.acme.dim_customers`, their `status` is 'Active' but the `current_mrr_usd` dropped from $7,450 to $2,450 before the seat expansion.

**nina.patel** — 10:45 AM
We need to be careful with how we present this to the board. 112% is still good, but we promised 115%. Marcus, what’s the status on the "Stark Industries" expansion? That would fix the gap.

**marcus.webb** — 10:50 AM
Legal is redlining the "Unlimited runs" clause for the Enterprise tier. They saw the `fact_workflow_runs` report and realized they’re already hitting 1M runs a month on the pilot. They want a fixed price, no overages. 

**david.kim** — 11:00 AM
Can we talk about the offsite? The catering options for Napa are due by Friday. Does anyone have a gluten allergy besides the new SDRs?

**nina.patel** — 11:05 AM
David, focus. Stark Industries is a $200k ACV opportunity. Put the sandwiches aside. 

---

### [2026-08-04] Pipeline Review & "The Big Win" Confusion

**marcus.webb** — 02:15 PM
BOOM! Just closed "Cyberdyne Systems." $120,000 MRR deal. Drinks on me at the 4th floor bar (if David fixed the leak). 

**lina.cho** — 02:20 PM
Marcus... $120k *MRR*? Or $120k *ACV*? 

**marcus.webb** — 02:22 PM
What's the difference? It's a $120k contract. 

**lina.cho** — 02:25 PM
A massive difference. If it's $120k MRR, that's $1.44M ARR. If it's $120k ACV, that's $10k MRR. I'm looking at the DocuSign... it says $120,000 per year. 

**jorge.martinez** — 02:30 PM
Updating `nexus-analyst-demo.acme.fact_subscriptions` now. It’s $10,000 `mrr_usd`. Marcus, please don't tell the VPs it's a million-dollar deal yet. You’re going to blow up the forecast models. 

**marcus.webb** — 02:32 PM
My bad. Still, $10k MRR is a solid Business tier win. They’re starting with 67 seats at the $149/mo rate plus a support kicker. 

**nina.patel** — 02:40 PM
It’s a good win, but it doesn't cover the gap from the "Umbrella Corp" churn last week. Jorge, did you mark Umbrella as `churned` in `dim_customers`?

**jorge.martinez** — 02:45 PM
Yes, `status` updated to 'Churned' and `churn_date` set to 2026-07-31. They cited "latency issues" as the primary reason. Likely the same Sydney cluster problem Nina mentioned. 

---

### [2026-08-12] SDR Quotas & Employee Sync

**nina.patel** — 09:00 AM
Jorge, I’m looking at the `dim_employees` table. Why aren't the two new SDRs, "Alice Vance" and "Bob Smith," showing up in the `ae_employee_id` mapping for the new leads? 

**jorge.martinez** — 09:15 AM
I haven't assigned them in the CRM yet. I was waiting for their `employee_id` to be finalized by HR. I’ll run the script to update `nexus-analyst-demo.acme.dim_employees` and sync the lead distribution by noon. 

**lina.cho** — 09:30 AM
Are we tracking their activity in `fact_user_events` or just CRM data? 

**jorge.martinez** — 09:35 AM
SDR activity isn't in the warehouse yet. We only track product events (like `event_type` = 'workflow_created') for users in `dim_users`. I can pull their email volume from the Outreach API if you need it for the productivity dashboard. 

**nina.patel** — 09:40 AM
I just need to know if they’re hitting their "Discovery Call" quota. We have 400 new leads from the 'Paid Search' `acquisition_channel` that are sitting untouched. 

**david.kim** — 09:45 AM
I can help with the leads if they’re in the APAC region. I need a reason to stay up late anyway, since my cat has been waking me up at 3 AM. 

**marcus.webb** — 09:50 AM
David, stay out of the 'Paid Search' bucket. Those are for the SDRs to qualify for the MM (Mid-Market) team. You’re supposed to be hunting Ent accounts. 

---

### [2026-08-20] Monthly Expense Reporting & Logistics

**jorge.martinez** — 04:00 PM
Reminder: All Expensify reports for July must be submitted by EOD. Nina, your team still has 12 "Unsubmitted" reports. 

**nina.patel** — 04:05 PM
Most of those are from the Amsterdam team’s client dinner with "Aperture Science." I’ll ping them. 

**david.kim** — 04:10 PM
Wait, can I expense the coffee pods for the 4th floor? The office manager said we’re out of budget until September. 

**jorge.martinez** — 04:15 PM
No. Put it in the Facilities ticket. 

**lina.cho** — 04:20 PM
Jorge, while checking `fact_invoices`, I see "Soylent Corp" paid $500 over their invoice amount. Can we apply that as a credit to their next `subscription_id` or do we have to refund? 

**jorge.martinez** — 04:25 PM
Check `nexus-analyst-demo.acme.fact_invoices`. If `status` is 'Paid', we can't easily modify. Better to issue a manual credit memo for August. Their `current_plan_tier` is Business, so the renewal should be automatic anyway. 

**marcus.webb** — 04:30 PM
Soylent is talking about upgrading to Enterprise for the SSO/Audit logs. Don't refund it yet—use it as leverage in the negotiation. "We'll credit your overpayment toward the implementation fee." 

**lina.cho** — 04:35 PM
Smart. I’ll hold off. 

---

### [2026-09-01] Q4 Planning Kickoff

**nina.patel** — 08:30 AM
Q4 goals are live in the shared drive. We’re targeting $45M ARR by year-end. That means we need $6M in new bookings this quarter. 

**marcus.webb** — 08:45 AM
That’s a steep jump. We’re going to need more headcount in CS if we land even half the Enterprise pipeline. `dim_customers` shows our current CSMs are already at 60 accounts each. 

**lina.cho** — 08:50 AM
Agreed. The `seat_count_licensed` is trending up across the board. If we hit the $45M mark, we’re looking at an average of 450 seats per Enterprise customer. We can’t support that with the current 15-person CS team. 

**jorge.martinez** — 09:00 AM
I’ll start building a Capacity Model using `fact_workflow_runs` and `dim_employees`. We need to see which customers are "high touch" based on their error rates. If `error_code` is high, they’re draining CS time. 

**david.kim** — 09:10 AM
I’m on board for Q4. Just a heads up, I’m OOO for the first week of October for my sister's wedding. Don't schedule any "Evolving Partnership" calls for me then. 

**nina.patel** — 09:15 AM
Noted. Jorge, make sure the `ae_employee_id` in `dim_customers` reflects David’s coverage during his OOO. Marcus is taking his Tier 1 accounts. 

**marcus.webb** — 09:20 AM
Only if I get the commission on the expansion. 

**jorge.martinez** — 09:25 AM
In your dreams, Marcus. Salesforce logic doesn't work that way. I’m locking the `current_mrr_usd` fields for the monthly snapshot now. Everyone stay out of the data. 

---

### [2026-09-05] Random Data Glitch - Urgent

**lina.cho** — 11:12 AM
Jorge, why does "Initech" have a `signup_date` of 1970-01-01 in `dim_customers`? 

**jorge.martinez** — 11:15 AM
Standard Unix epoch null value. Someone probably manually created the record in the CRM without a date and the sync script defaulted. Fixing it now—should be 2024-03-12. 

**lina.cho** — 11:20 AM
Thanks. It was throwing off the "Time to Expansion" cohorts. 

**david.kim** — 11:25 AM
1970... Initech was ahead of their time. 

**nina.patel** — 11:30 AM
David. Stop.

---

### [2026-01-05] Q1 Quota & Board Prep

**nina.patel** — 09:15 AM
Happy New Year everyone. Let's hit the ground running. I’ve uploaded the Q1 Sales Targets to the "FY26 Planning" folder. We are looking at a $12M net new ARR target for H1. 

**marcus.webb** — 09:22 AM
$12M? Nina, we barely scraped $6M in Q4. Is the board aware that the AE headcount is still flat? We lost Sarah in December and haven't backfilled her Mid-Market seat.

**jorge.martinez** — 09:30 AM
The board is looking at the NRR (Net Revenue Retention) from the `fact_subscriptions` table. We finished 2025 at 122% NRR. The logic is that expansion within the existing "Business" tier customers will carry 40% of that $12M. Look at `nexus-analyst-demo.acme.dim_customers`—we have 200+ accounts in the "Business" tier with `seat_count_licensed` between 40 and 49. They are primed for that 50-seat minimum jump.

**david.kim** — 09:45 AM
I’m already seeing it. Just closed a 15-seat expansion for "Globex Corp". But Jorge, I think there’s an issue with how `current_mrr_usd` is calculating for them. It shows $7,350 but they’re on the Business plan ($149/seat). It should be $8,940 if they hit the 60-seat mark we discussed. 

**jorge.martinez** — 10:02 AM
@david.kim check the `start_date` in `fact_subscriptions`. The mid-month true-up doesn’t reflect in `dim_customers.current_mrr_usd` until the cron job runs at midnight. Also, did you actually push the DocuSign through? The `status` is still 'pending_signature' in the CRM sync.

**david.kim** — 10:05 AM
Ah, my bad. Client is OOO until Wednesday. I’ll nag them then. 

**nina.patel** — 10:15 AM
Reminder: Sales Kickoff (SKO) is in San Jose next week. If you haven't booked your flights through Navan, do it today. Finance is breathing down my neck about the "last minute" premium prices. 

---

### [2026-02-12] Umbrella Corp Expansion & Pipe Review

**marcus.webb** — 02:45 PM
Big news. Umbrella Corp wants to move their entire DevOps org onto Acme. We’re talking 800 seats. 

**lina.cho** — 02:50 PM
That would put them deep into the Enterprise tier. @marcus.webb, make sure you're looking at `nexus-analyst-demo.acme.dim_plans`. Enterprise requires a dedicated CSM. @nina.patel, do we have capacity?

**nina.patel** — 02:55 PM
If Marcus closes 800 seats, I’ll personally find a CSM. Marcus, what’s the ACV?

**marcus.webb** — 03:02 PM
Roughly $480k ACV. They want a custom SLA on `workflow_run_quota_per_month` because they’re expecting to burst over 2M runs during their release cycles.

**jorge.martinez** — 03:10 PM
Wait, $480k ACV? Marcus, you just posted in the Slack channel that it was $40k. 

**marcus.webb** — 03:12 PM
$40k Monthly, Jorge. $480k Annual. Keep up.

**jorge.martinez** — 03:15 PM
This is why I hate the manual "Bookings" spreadsheet. People mix up `bookings_acv_usd` and MRR constantly. Everyone, PLEASE use the `mrr_usd` field in `fact_subscriptions` for monthly talk and multiply by 12 for annual. Don't eyeball it. 

**david.kim** — 03:20 PM
Speaking of Umbrella Corp, I see their `error_code` frequency in `fact_workflow_runs` is spiking. Are they even ready to scale? If we sell them 800 seats and the platform chokes on their webhooks, that’s a churn risk in 6 months.

**lina.cho** — 03:25 PM
I’ll pull the logs. `select error_code, count(*) from nexus-analyst-demo.acme.fact_workflow_runs where customer_id = 'CUST-772' group by 1`. 

**lina.cho** — 03:35 PM
It’s mostly `error_code` 429—Rate Limiting. They’re hitting the Business tier caps. Moving to Enterprise (unlimited runs) actually solves their technical bottleneck. Ship it, Marcus.

---

### [2026-03-20] Expense Report Madness

**nina.patel** — 11:00 AM
Final warning: Expense reports for February are due by EOD Friday. If you took a prospect out to dinner, I need the receipt AND the `customer_id` associated with the spend.

**david.kim** — 11:15 AM
Does "Dinner with a 'Potential' Lead" count if they haven't signed the `signup_date` yet? 

**jorge.martinez** — 11:20 AM
No `customer_id`, no reimbursement, David. Use the `lead_id` from the marketing table if they aren't in `dim_customers` yet. 

**marcus.webb** — 11:45 AM
Jorge, the `dim_employees` table has me listed in the "San Francisco" office but I’ve been remote from Austin for three months. My tax withholding is going to be a mess. Who do I talk to?

**jorge.martinez** — 11:50 AM
Ping People-Ops. I just pull the `location` field from their export. If they don't update it, the BI dashboard thinks you're sitting in SF eating expensive sourdough. 

---

### [2026-04-15] Q2 Pipeline & CRM Migration

**nina.patel** — 09:00 AM
We are migrating the `ae_employee_id` mapping to a new territory-based model. Jorge, did we finish the script to update `dim_customers`?

**jorge.martinez** — 09:15 AM
Almost. We’re reassigning all "Pro" tier accounts in the EMEA region to the new Amsterdam pod. If you see your `current_mrr_usd` totals dip in your personal dashboard, don't panic. It's just the accounts moving to the new `ae_employee_id` for the EMEA reps. 

**marcus.webb** — 09:20 AM
Wait, I had three "Pro" accounts in London that were about to upgrade to "Business". Do I lose the commission if they upgrade after the migration?

**nina.patel** — 09:25 AM
If the `changed_from_subscription_id` in `fact_subscriptions` links back to a sub you owned within 30 days of the move, you get a split. Otherwise, it goes to the EMEA team. 

**david.kim** — 09:30 AM
Harsh. I’m checking my "Hooli" deal. They’re in the US-West region, so they should stay with me. Jorge, can you confirm `customer_id` 'CUST-449' is still mapped to `employee_id` 'EMP-012'?

**jorge.martinez** — 09:40 AM
Checking `nexus-analyst-demo.acme.dim_customers`... Yes, David. You're still the AE. But they haven't logged in since `2026-04-01`. Check `dim_users.last_login_date`. Your "whale" might be ghosting you.

**david.kim** — 09:45 AM
They aren't ghosting. They're "evaluating". 

**marcus.webb** — 09:50 AM
That's AE-speak for "the champion left the company." Check the `is_active` flag for their primary admin in `dim_users`. 

**david.kim** — 10:05 AM
...Dammit. `is_active` is FALSE. Okay, I have some calls to make. 

---

### [2026-05-01] April Close / Data Validation

**lina.cho** — 04:30 PM
April numbers are in. Total ARR is sitting at $39.2M. We missed the $40M stretch goal, but it's a solid 8% MoM growth. 

**jorge.martinez** — 04:35 PM
Hold on. I’m seeing a discrepancy in `fact_invoices`. "Soylent Corp" paid $15k, but it’s not showing up in the `current_mrr_usd` for `dim_customers`. 

**lina.cho** — 04:40 PM
Looks like their `status` in `fact_subscriptions` is 'paused'. They paid a retention fee but aren't technically "Active". 

**nina.patel** — 04:45 PM
If they paid, we count it. Jorge, update the dashboard logic to include 'paused' status if `paid_at` in `fact_invoices` is within the last 30 days. We need every dollar to show the VCs we’re on track for the Series C. 

**marcus.webb** — 04:50 PM
I’m out. If anyone needs me, I’ll be at the bar celebrating the Umbrella Corp verbal commit. (Don’t tell Finance). 

**jorge.martinez** — 04:55 PM
I’m telling Finance. Log your receipts, Marcus. 

---

### [2026-05-04] Q2 Quota & Pipeline Review

**lina.cho** — 09:15 AM
@nina.patel and I just finished the Q2 models. With the $40M ARR miss in April, we’re bumping everyone’s quota by 12% for the summer to stay ahead of the Series C burn rate. 

**david.kim** — 09:20 AM
12%?! Lina, my pipeline is already stretched thin. I’m looking at `nexus-analyst-demo.acme.fact_subscriptions` for my territory and half the ‘Business’ tier prospects are stuck in ‘Evaluating’ because of the new security review requirements. 

**marcus.webb** — 09:22 AM
Seconded. I’ve got “Pied Piper” (CUST-992) ready to sign a $120k ACV deal, but they’re arguing over the seat minimums in the Business tier. They want 30 seats, we require 50. If I can't discount the `min_seats` in `dim_plans`, I’m going to lose them to a competitor.

**nina.patel** — 09:30 AM
We aren't budging on the 50-seat floor for Business. If they want fewer seats, they go Pro at $49/seat/mo, but they lose SSO and the audit logs. Check `dim_plans`—the `workflow_run_quota_per_month` is also much lower on Pro. Use that as leverage. 

**jorge.martinez** — 09:45 AM
Speaking of Pied Piper, I just ran a check on their trial usage in `nexus-analyst-demo.acme.fact_workflow_runs`. They’ve already hit 15,000 runs this month. If they go Pro, they’ll hit the 10k quota in two weeks and get throttled. David, show them the `run_id` volume. That usually closes the deal.

**david.kim** — 10:05 AM
Good catch, Jorge. I'll pull the `fact_workflow_runs` stats for their main admin (user_id 'U-9921'). 

---

### [2026-05-06] Finance vs. Sales: The "Bookings" Argument

**lina.cho** — 02:30 PM
@marcus.webb, why did you log the "Initech" deal as $60,000 in the CRM? 

**marcus.webb** — 02:35 PM
Because that’s the ACV. 50 seats at the Enterprise floor. 

**lina.cho** — 02:40 PM
Marcus... that’s a multi-year deal paid monthly. In `nexus-analyst-demo.acme.fact_subscriptions`, the `mrr_usd` is only $5,000. Finance reports on MRR and ARR, not "projected total contract value." You’re inflating the dashboard. 

**marcus.webb** — 02:45 PM
It’s a booking! I get paid commission on the booking. 

**nina.patel** — 02:50 PM
You get paid when the `fact_invoices.status` says 'paid'. @jorge.martinez, can we add a filter to the `sales_performance_v2` dashboard to exclude anything where `billing_cycle` is 'annual' but the `amount_usd` hasn't cleared yet? Marcus is giving the CEO a heart attack with these "phantom" millions.

**jorge.martinez** — 03:00 PM
On it. I’ll join `fact_subscriptions` with `fact_invoices` on `subscription_id` to verify the cash-in-door before it hits the "Confirmed ARR" column.

---

### [2026-05-10] Expense Report Hell / Offsite Logistics

**marcus.webb** — 11:15 AM
Has anyone seen my receipt for the steakhouse dinner with the "Globex" team? It was like $800. I think I left it in the Uber.

**lina.cho** — 11:20 AM
If you don't have the receipt, you aren't getting reimbursed. Policy is clear. Also, $800 for three people? Did you buy them the whole cow?

**david.kim** — 11:22 AM
He probably bought the "Executive Wine Flight." Marcus, check your email for the digital receipt. 

**nina.patel** — 11:30 AM
Quick reminder: The Amsterdam team offsite is the week of June 15th. If you haven't booked your flights through the portal, do it now. The `dim_employees` table shows 5 people in EMEA still haven't confirmed their attendance. I'm looking at you, @jorge.martinez. 

**jorge.martinez** — 11:35 AM
I’m coming! I just need to make sure the dbt jobs don’t fail while I’m over the Atlantic. Last time I flew, the `fact_user_events` table spiked and blew out the Snowflake credit limit because of a bot attack on the 'Free' tier. 

---

### [2026-05-12] Board Prep: NRR and Churn Analysis

**nina.patel** — 09:00 AM
Board deck is due Friday. I need the Net Revenue Retention (NRR) for the SMB vs. Enterprise segments for the last 12 months. 

**jorge.martinez** — 09:15 AM
I'm pulling it now. SMB (account_tier = 'SMB' in `dim_customers`) is hovering around 95%—the churn in the Pro tier is hurting us. Enterprise is at 120% thanks to the expansion seats at "Weyland-Yutani". 

**lina.cho** — 09:20 AM
What's the main churn reason for SMB? 

**jorge.martinez** — 09:30 AM
Looking at `fact_user_events`. For customers where `status` is 'churned', the `last_login_date` in `dim_users` is usually 45 days prior to the `churn_date`. They stop using the product entirely before they cancel. 

**nina.patel** — 09:35 AM
We need a "Save Desk" workflow. If `fact_workflow_runs` for a 'Business' account drops by more than 50% week-over-week, alert the CSM (csm_employee_id). We're losing money because we aren't watching the usage signals. 

**david.kim** — 09:40 AM
That's what I've been saying! I saw "Soylent Corp" (CUST-512) usage drop last week. I checked `nexus-analyst-demo.acme.fact_workflow_runs` and they went from 2k runs a day to 50. I called the admin; turns out they broke their own API integration. Saved the account. 

**marcus.webb** — 09:45 AM
Nice save, Dave. Can I get a referral bonus for that? 

**lina.cho** — 09:46 AM
No. Log your receipts, Marcus.

---

### [2025-06-18] Q3 Pipeline & Umbrella Corp Deal

**marcus.webb** — 02:15 PM
@lina.cho just sent over the MSA for "Umbrella Corp". They are looking at the Enterprise tier for 350 seats. If we close this by Friday, it’s a massive win for the EMEA region. 

**lina.cho** — 02:20 PM
Wait, Marcus—I’m looking at the CRM. You have the `bookings_acv_usd` listed as $52,500. For 350 seats on Enterprise, that doesn't look right. Enterprise floor is usually higher. 

**nina.patel** — 02:25 PM
Lina's right. @marcus.webb, are you quoting them the Business price ($149/seat) or the Enterprise custom rate? If it's 350 seats on Business, it would be $52,150 MRR, which is over $600k ACV. You might have typed the monthly amount into the annual field again. 

**marcus.webb** — 02:30 PM
Ugh, my bad. I was looking at the `fact_subscriptions` schema and got flipped. The ACV is $630,000. I'll update the opportunity in the system. 

**jorge.martinez** — 02:45 PM
Before you do that, can someone check if they've already started a trial? I see a `customer_id` 'CUST-882' using an @umbrellacorp.com domain in `dim_users`, but they are marked as 'Free' tier. We need to make sure the `acquisition_channel` is correctly attributed to 'Outbound' so Sales gets the credit and not 'Organic'. 

**david.kim** — 02:50 PM
They’ve been using the Free tier for 3 weeks. 12 users active. They already hit the 100 runs/mo quota in `fact_workflow_runs` three days ago. That's probably why they're moving so fast on the MSA. 

---

### [2025-08-14] CRM Migration Cleanup 

**jorge.martinez** — 10:00 AM
The migration from the legacy tracker to the new Salesforce instance is a mess. I’m seeing duplicate entries in `dim_customers` for "Tyrell Corp". One has `account_tier` as 'MM' and the other as 'Ent'. 

**nina.patel** — 10:05 AM
They upgraded in July. The 'MM' record should have a `status` of 'churned' or 'inactive' with a `churn_date` of 2025-07-31, and the 'Ent' record should be the current one. 

**jorge.martinez** — 10:15 AM
The problem is the `ae_employee_id`. The old record is assigned to a rep who left in March (employee_id 44), and the new one is assigned to @marcus.webb. It's messing up the historical attainment reports. 

**lina.cho** — 10:20 AM
We need a clean source of truth. Jorge, can you write a script to merge any records where the `email_domain` in `dim_users` matches but the `customer_id` is different? 

**jorge.martinez** — 10:30 AM
I can, but I need Finance to sign off on the MRR reconciliation. I don't want to double-count the $12k expansion in the `fact_subscriptions` table. 

---

### [2026-01-05] 2026 Kickoff & Quota Assignments

**lina.cho** — 09:00 AM
Happy New Year, team! Quotas for 2026 are live in the GDrive. 

**marcus.webb** — 09:15 AM
$1.2M for the year? Lina, the SMB churn we saw in Q4 makes that a steep climb. 

**lina.cho** — 09:20 AM
That's why we're pivoting the AE focus to Mid-Market and Enterprise. Look at the `dim_customers` data from last year—our LTV for Enterprise is 10x the Pro tier. We’re not chasing $49/mo seats anymore. 

**david.kim** — 09:25 AM
Does this mean CS is getting more headcount? If we're going all-in on Enterprise, I can't have 150 accounts per CSM. "Weyland-Yutani" alone is taking up 20% of my week since they started using the custom API endpoints. 

**nina.patel** — 09:30 AM
We have budget for 3 more CSMs in Q2. Check `dim_employees`—we just posted the reqs. 

---

### [2026-05-04] ARR Reconciliation (Current)

**nina.patel** — 02:00 PM
@jorge.martinez, I’m looking at the April month-end close. `nexus-analyst-demo.acme.fact_subscriptions` shows total MRR at $3.25M, but the `fact_invoices` table shows total collected at $3.1M. Where is the $150k gap? 

**jorge.martinez** — 02:15 PM
Checking... Okay, it looks like "Cyberdyne Systems" (CUST-402) has a failed payment status on their last three invoices. Their `plan_tier` is 'Business', but they have 1,000 seats. 

**nina.patel** — 02:20 PM
Why hasn't their access been restricted? If `fact_invoices.status` is 'unpaid' for more than 30 days, we should be seeing a flag. 

**jorge.martinez** — 02:25 PM
The `status` in `dim_customers` is still listed as 'active'. It seems the automated de-provisioning script only looks at `fact_subscriptions.is_current`, which is still true because the sub hasn't been "cancelled"—they just aren't paying the bill. 

**lina.cho** — 02:30 PM
@david.kim, can you reach out to Cyberdyne? That’s a huge chunk of our Business tier ARR. 

**david.kim** — 02:35 PM
On it. Their admin, Miles Dyson, hasn't logged in since April 12th. I'll check `dim_users` to see if there are any other admins active before I pull the plug. 

**marcus.webb** — 03:00 PM
By the way, did anyone approve my flight to the Amsterdam offsite? My expense report for the "Premium Economy" upgrade got flagged. 

**nina.patel** — 03:05 PM
No. Log your receipts properly, Marcus. And use the corporate portal.

**marcus.webb** — 03:06 PM
It was only $400! I need the legroom to work on the "Initech" proposal. 

**lina.cho** — 03:10 PM
If you close Initech by EOM, I'll approve the upgrade myself. Otherwise, you're sitting in the back with the `fact_workflow_runs` logs.

---

### [2026-05-12] Q2 Board Prep: NRR and Expansion Targets

**nina.patel** — 09:15 AM
@jorge.martinez I’m pulling the preliminary NRR (Net Revenue Retention) for the Q2 board deck. When I query `nexus-analyst-demo.acme.fact_subscriptions`, the `change_type` = 'expansion' for April seems low. Are we missing the "Tyrell Corp" (CUST-505) seat add-on?

**jorge.martinez** — 09:40 AM
Checking the logs. It looks like Tyrell Corp’s expansion was logged as a new subscription line instead of a `change_type`. Give me 10 minutes to fix the logic in the dbt model. Also, note that "Soylent Corp" (CUST-202) churned in March, so that’s weighing down the NRR calculation if you're looking at the trailing 12 months.

**lina.cho** — 09:45 AM
Soylent didn't churn, they "paused" because of their internal restructuring. David, did we move them to a $0 Free tier or did they actually terminate?

**david.kim** — 09:50 AM
They’re on a 'paused' status in `dim_customers`. The `current_mrr_usd` is $0 but the `status` isn't 'churned'. We’re hoping to win them back in Q3 when their new CTO starts. 

**nina.patel** — 10:00 AM
For the board, $0 is $0. I’m counting it as churn for the Gross Retention slide. We can't have "maybe" revenue in the deck. 

---

### [2026-05-15] Pipeline Review: The Initech Saga

**marcus.webb** — 11:30 AM
HUGE news. Initech is ready to sign. 250 seats on the Enterprise plan. That’s a massive win for my May quota. I’ve updated the CRM. @nina.patel, I logged it as $450,000 in the `bookings_acv_usd` field. 

**nina.patel** — 11:45 AM
Marcus, I just looked at the entry. You put $450,000 for the *year*, but you also checked the box for "Monthly Billing." If they are paying monthly, the `fact_subscriptions.mrr_usd` should be $37,500. But your contract says $15,000/mo with a ramp. Which is it?

**marcus.webb** — 11:50 AM
The first three months are $15k because they are migrating off Zapier, then it scales to $37.5k. 

**jorge.martinez** — 11:55 AM
Marcus, the `nexus-analyst-demo.acme.fact_subscriptions` table can’t handle "vibes." I need a hard start date for the ramp. If the `mrr_usd` changes in August, I need two separate subscription rows or it’s going to break the ARR reconciliation report again. 

**lina.cho** — 12:05 PM
@marcus.webb Stop trying to hack the ACV. Just send the paper to Legal. And remember what I said about the Amsterdam flight—don't book anything until the deposit hits.

**marcus.webb** — 12:10 PM
The deposit is coming! Bill Lumbergh promised the wire would clear by Friday. 

---

### [2026-05-18] CRM Migration & Data Hygiene

**jorge.martinez** — 08:30 AM
@channel Please stop leaving the `ae_employee_id` field blank in the new account forms. I have 14 accounts in `dim_customers` right now with 'NULL' for the AE. It’s breaking the commission dashboards. 

**marcus.webb** — 08:35 AM
The dropdown wasn't working on mobile while I was at the airport. 

**jorge.martinez** — 08:40 AM
Use a laptop. Also, someone created a duplicate for "Globex Corporation". We have CUST-881 and CUST-882. One is on the Business tier and one is Free. Can someone in CS merge these?

**nina.patel** — 09:00 AM
I’ll take Globex. They’re a mess anyway. @marcus.webb, while you’re "working at the airport," can you explain why there’s a $1,200 charge for "Team Bonding" at a steakhouse in Omaha? You were there for a 1-hour discovery call.

**marcus.webb** — 09:05 AM
Warren Buffet might have been there! (He wasn't, but the prospect's VP of Ops loves ribeye. It's a strategic investment).

---

### [2026-05-20] Workflow Run Overages (Revenue Opportunity)

**lina.cho** — 02:00 PM
@jorge.martinez, can you run a report on `nexus-analyst-demo.acme.fact_workflow_runs`? I want to see which 'Pro' tier customers have exceeded their 10k monthly quota for three consecutive months. 

**jorge.martinez** — 02:15 PM
Running it now... Okay, "Wayne Enterprises" (CUST-112) is at 45k runs this month already. They are significantly over. Their `plan_tier` is still 'Pro'. 

**lina.cho** — 02:20 PM
Perfect. That’s a forced migration to Business. David, contact Lucius Fox. Tell him they’ve outgrown Pro and need the SSO/Audit Log features of Business (and the 100k run quota). 

**david.kim** — 02:25 PM
On it. Wayne Ent has 45 seats right now. If we move them to Business, they hit the 50-seat minimum. That’s an easy $7,450 MRR bump. 

**jorge.martinez** — 02:30 PM
Check `fact_user_events` first. It looks like most of those runs are coming from a single broken webhook integration. If they fix the loop, their usage might drop back down. 

**lina.cho** — 02:35 PM
Don't tell them that. Sell them the stability. 

---

### [2026-05-22] Random / Office

**marcus.webb** — 10:00 AM
The espresso machine in the SF lounge is making a high-pitched screaming sound. @nina.patel is this in the budget to fix or should I just buy a Nespresso for my desk?

**nina.patel** — 10:05 AM
The screaming is a known issue. Maintenance is coming Wednesday. And no, the Nespresso is not a reimbursable expense. 

**jorge.martinez** — 10:10 AM
Speaking of screaming, the `fact_workflow_runs` partition for 2026-05-21 just failed. I’m re-running the job. If the dashboards look empty for yesterday, that’s why. Should be back in 30 mins. 

**lina.cho** — 10:15 AM
Thanks Jorge. Everyone else, remember the All-Hands is at 11 AM. Nina is presenting the Q2 outlook. Try to look enthusiastic about the "SaaS Winter" slides.

### [2026-06-02] Q2 NRR / Board Deck Prep

**nina.patel** — 09:00 AM
@jorge.martinez I’m looking at the draft for the Series B update. Your NRR calc in the dashboard says 114% for Q1, but my spreadsheet based on `nexus-analyst-demo.acme.fact_subscriptions` is showing 108%. Why the 6% delta? We can't show the board 108% after we promised 115% in the last update.

**jorge.martinez** — 09:15 AM
The dashboard excludes the "Contract Expansion" field for customers who moved from Pro to Business mid-month if the seat count was below the 50-seat floor. Look at "Hooli" (CUST-089). They upgraded, but because they only have 48 seats licensed (they're paying the 50-seat minimum), the delta logic in the SQL is tripping up. 

**nina.patel** — 09:20 AM
We need to count the 50-seat minimum as the baseline MRR for NRR purposes. Revenue is revenue. Fix the view in `nexus-analyst-demo.acme.dim_customers` so `current_mrr_usd` reflects the contract minimum, not the provisioned count.

**lina.cho** — 09:25 AM
While you're in there, can we look at churn? We lost "Initech" (CUST-552) last week and it’s still showing as 'Active'. 

**jorge.martinez** — 09:30 AM
Initech is still in their notice period. Their `status` won't flip to 'Churned' until `2026-06-30` according to the `fact_subscriptions` end_date. I'll manually override if you want, but it'll break the automated reconciliation for June.

---

### [2026-06-08] Pipeline Review / SF Offsite

**david.kim** — 11:15 AM
Huge news on "Cyberdyne Systems" (CUST-901). They just signed a $120k ACV expansion. Taking them from Business to Enterprise. @lina.cho, can we get the champagne ready for the offsite on Friday?

**nina.patel** — 11:20 AM
Wait, David. I’m looking at the contract. This is $120k *Total Contract Value* over 24 months. That's $60k ACV, not $120k. 

**david.kim** — 11:22 AM
It’s $10k MRR at peak? No? 

**nina.patel** — 11:25 AM
No. It’s $5k MRR. You confused `bookings_acv_usd` with `tcv_usd` again. This doesn't put you over your Q2 quota yet. You’re still at 82% of target.

**marcus.webb** — 11:30 AM
Rough. Still a great win though. Does this mean the SF offsite is still at the ferry building or are we back to the Mission office and catering from Chipotle?

**lina.cho** — 11:35 AM
Chipotle. And David, please update the opportunity in the CRM. Jorge is pulling the nightly sync into `nexus-analyst-demo.acme.fact_subscriptions` and it’s going to mess up the forecast if it’s sitting there as 120k.

---

### [2026-06-12] Random / Logistics

**sarah.jenkins** — 01:45 PM
@here Does anyone have the physical key for the Amsterdam office supply closet? @marcus.webb think you took it during your visit last month. 

**marcus.webb** — 01:50 PM
Check the second drawer of the front desk. I might have left it under the stack of Acme-branded stickers. Also, the Stroopwafels are gone. Sorry.

**jorge.martinez** — 02:00 PM
FYI, I'm taking the warehouse offline for 2 hours tonight (10 PM PT) to refactor `fact_user_events`. We’re seeing too much latency on the `event_at` joins. If you're running late-night reports for EMEA, they will fail.

---

### [2026-06-15] Salesforce/BigQuery Desync

**lina.cho** — 10:00 AM
@jorge.martinez, why does "Gekko & Co" (CUST-441) show $0 MRR in the dashboard? They've been on a Business plan since 2024. 

**jorge.martinez** — 10:10 AM
Looking... Ah, someone changed the `customer_id` in the CRM but didn't update the `dim_customers` mapping. The join is failing. It’s showing up as an orphaned record in `fact_invoices`. 

**jorge.martinez** — 10:15 AM
Actually, it's worse. "Gekko & Co" is now "Gekko International" in the CRM. I'm going to run a script to update the `company_name` in `nexus-analyst-demo.acme.dim_customers`. Nina, does this affect the tax filings for EMEA? 

**nina.patel** — 10:20 AM
Only if the VAT ID changed. If it's just a rebrand, we're fine. But check `fact_invoices` for any unpaid balances. Gekko is notorious for "losing" invoices during name changes.

---

### [2026-06-20] Expansion Opps (Usage-Based)

**lina.cho** — 03:00 PM
@david.kim, "Tyrell Corp" (CUST-202) just hit 95k workflow runs. Their quota on the Business plan is 100k. They are going to hit the ceiling by Wednesday. 

**david.kim** — 03:05 PM
I’ve been trying to get Eldon Tyrell on the phone for weeks. He’s ghosting. 

**sarah.jenkins** — 03:10 PM
I’m the CSM for Tyrell. They’re frustrated because the "priority support" hasn’t responded to their ticket about the `step_count` limit on the Free-tier legacy workflows they still have running. 

**lina.cho** — 03:15 PM
Kill the legacy workflows. That’s the leverage. Tell them we’re migrating all accounts to the 2026 schema and they need to move to Enterprise to keep that custom `step_count`. That’s a $15k expansion right there. 

**jorge.martinez** — 03:20 PM
I’ll pull the `fact_workflow_runs` for Tyrell and highlight the ones with `error_code` 'LIMIT_EXCEEDED'. Might help the "stability" argument. Use path: `nexus-analyst-demo.acme.fact_workflow_runs` filtered by `customer_id = 'CUST-202'`.

---

### [2026-06-25] End of Quarter Push

**nina.patel** — 04:00 PM
Final call for June expense reports. If you don't submit by Friday, they’re coming out of the Q3 budget. 

**marcus.webb** — 04:05 PM
Does the "Customer Dinner" at Gary Danko count if the customer didn't actually show up? I have the receipt. 

**nina.patel** — 04:10 PM
Marcus, we’ve talked about this. No. 

**lina.cho** — 04:15 PM
@here Status check on the "Stark Industries" (CUST-004) renewal. We have $450k ACV on the line. Sarah, where are we with the SOC2 audit docs they requested?

**sarah.jenkins** — 04:20 PM
Sent them over yesterday. Pepper Potts confirmed receipt. They’re just waiting on Legal. If we close this by the 30th, we hit the stretch goal for the year.

**jorge.martinez** — 04:25 PM
I've already prepped the `fact_subscriptions` entry for Stark. Just need the `subscription_id` from the signed PDF to push it live. Fingers crossed.

---

### [2026-07-02] Q2 Reconciliation & NRR Board Prep

**nina.patel** — 09:15 AM
@jorge.martinez I’m looking at the preliminary Q2 numbers for the board deck. Why does `fact_subscriptions` show a $12k gap compared to what Finance has in Stripe? 

**jorge.martinez** — 09:30 AM
Checking. Probably the Stark Industries (CUST-004) expansion. It was signed on the 30th but I haven't updated the `is_current` flag for the old record. Use `nexus-analyst-demo.acme.fact_subscriptions` and filter for `change_type = 'UPGRADE'` in June. 

**marcus.webb** — 09:45 AM
Quick question on the NRR calc—are we including the overage fees from "Weyland-Yutani" (CUST-105)? They did an extra 50k runs last month. 

**lina.cho** — 09:50 AM
No, Marcus. NRR is based on committed MRR. Overage goes into the "Usage/Variable" bucket on the P&L. If we keep counting one-offs as recurring, the board is going to grill us on the churn spike when they normalize next month. 

**david.kim** — 10:00 AM
Wait, I think I see the issue in the query. Someone joined `dim_customers` on `customer_id` but didn't filter for `status = 'active'`. We’re pulling in the zombie revenue from "Soylent Corp" (CUST-666) which churned in May. 

**jorge.martinez** — 10:05 AM
My bad. Fixed the view: `nexus-analyst-demo.acme.dim_customers`. I’ll re-run the `current_mrr_usd` aggregate. 

---

### [2026-07-08] Q3 Pipeline & AE Quotas

**lina.cho** — 02:00 PM
@sales-team Q3 quotas are live in the portal. We’ve increased the target for the MM (Mid-Market) pod by 15% to account for the new "Auto-Provisioning" feature launch. 

**marcus.webb** — 02:10 PM
15%? Lina, my pipe is 60% "Pro" tier leads coming from the self-serve funnel. Converting those to "Business" takes twice as long now because Legal is flagging the new indemnity clause. 

**david.kim** — 02:15 PM
Marcus is right. I’ve got "Cyberdyne Systems" (CUST-080) stuck in procurement because they want a custom SLA that we only offer on Enterprise. They only have 120 seats—not enough for the Enterprise minimum. 

**sarah.jenkins** — 02:20 PM
Can we just "ghost seat" them? Give them 250 licenses but they only use 120? 

**lina.cho** — 02:25 PM
No. Finance will flag the seat utilization gap in the Q3 audit. If utilization drops below 50%, it triggers a "High Churn Risk" alert in the CSM dashboard. Just sell them the Business plan + the "Compliance Add-on." 

**jorge.martinez** — 02:30 PM
I’ll update the `dim_plans` table to include the `sla_uptime_pct` for the new add-on tiers so the AE's can pull it into their quotes correctly. 

---

### [2026-07-12] Noisy Monday

**nina.patel** — 09:00 AM
Whose "Team Building" lunch at Zuni Café cost $1,400? There were only 4 people on the receipt. 

**marcus.webb** — 09:05 AM
That was the "Initech" (CUST-001) closing lunch. They brought their whole IT team. 

**nina.patel** — 09:10 AM
Initech is a $12k ACV account, Marcus. You spent 10% of their annual contract on one lunch. Denied. 

**sarah.jenkins** — 11:30 AM
Does anyone have the Zoom link for the "Hooli" (CUST-003) QBR? Gavin Belson’s EA is pinging me. 

**david.kim** — 11:35 AM
It's in the calendar invite, Sarah. Under "Project Moonshot Prep." 

---

### [2026-07-20] Data Hygiene & CRM Cleanup

**jorge.martinez** — 01:00 PM
Heads up—I’m running a script to merge duplicate records in `dim_customers`. We had three different entries for "Wayne Enterprises" (CUST-005, CUST-901, and CUST-902) because someone kept creating new leads instead of searching for the existing account. 

**lina.cho** — 01:10 PM
That’s Bruce Wayne’s account. Be careful. They have a complex hierarchy with "Wayne Tech" and "Wayne Biotech." 

**jorge.martinez** — 01:15 PM
I’m mapping everything to `customer_id = 'CUST-005'`. If you need the historical breakdown, check `nexus-analyst-demo.acme.fact_subscriptions` and look for the `changed_from_subscription_id` column to see the trail. 

**david.kim** — 01:20 PM
While you’re in there, can you fix the `industry` tag for "Oscorp" (CUST-012)? It’s listed as "Retail" but they are definitely "Life Sciences/Manufacturing." 

**jorge.martinez** — 01:25 PM
Done. Also fixed a bunch of NULLs in the `acquisition_channel` column for the 2025 cohort. Looks like a lot of "Direct" signups were actually "Referral."

---

### [2026-07-28] ARR Reconciliation (The "Bookings" Argument)

**marcus.webb** — 04:00 PM
My dashboard shows I’m at 110% of quota for July. Why does the Ops report say 92%? 

**lina.cho** — 04:05 PM
You’re looking at `bookings_acv_usd`. Ops reports on `mrr_usd` * 12 from `nexus-analyst-demo.acme.fact_subscriptions`. You signed "Massive Dynamic" (CUST-044) on a multi-year deal, but the first year is heavily discounted. We don't credit the full TCV (Total Contract Value) against your monthly quota. 

**marcus.webb** — 04:10 PM
That’s ridiculous. A win is a win. 

**nina.patel** — 04:15 PM
Not when the cash flow doesn't hit the bank until 2027, Marcus. We’ve been through this. We report ARR to the board, not "Expected Future Value." 

**jorge.martinez** — 04:20 PM
If you want to see the gap, run: 
`SELECT customer_id, mrr_usd, (mrr_usd * 12) as calculated_arr FROM nexus-analyst-demo.acme.fact_subscriptions WHERE is_current = true`. 
It’ll show you exactly what’s hitting the current ledger. 

**sarah.jenkins** — 04:30 PM
Also, "Massive Dynamic" hasn't actually paid the first invoice yet. It’s still `status = 'open'` in `fact_invoices`. We don't count it as "Booked" until the check clears or we have a signed PO. 

**marcus.webb** — 04:35 PM
I have the PDF! I’ll upload it to the CRM now. 

**nina.patel** — 04:40 PM
Upload it to the "Signed Contracts" folder, not the "Random Notes" section this time. Please.

---

### [2026-09-02] Q3 NRR / Board Deck Prep

**nina.patel** — 09:15 AM
@jorge.martinez and @lina.cho — we need the preliminary NRR (Net Revenue Retention) numbers for the Q3 board deck by EOD Friday. Use the cohort starting July 2025. 

**jorge.martinez** — 09:30 AM
I’m pulling it now. Quick question: are we including the "Pied Piper" (CUST-021) contraction? They dropped from 200 seats to 60 last month when they moved half their team to a different tool. 

**lina.cho** — 09:35 AM
Yes, contraction is part of NRR. If we only showed the good stuff it would be Gross Retention. Run the logic against `nexus-analyst-demo.acme.fact_subscriptions`. 
Filter: `WHERE start_date <= '2025-09-30' AND is_current = true`. 
Actually, use the `changed_from_subscription_id` to trace the MRR delta.

**nina.patel** — 09:45 AM
Also, Marcus is claiming a "massive expansion" for "Tyrell Corp" (CUST-008) but I don't see it in the `fact_subscriptions` table yet. 

**marcus.webb** — 10:00 AM
That’s because the legal team is still redlining the MSA. It’s an expansion from Business to Enterprise, adding 300 seats. It’s basically a done deal. Can we bake it into the "Projected" slide?

**nina.patel** — 10:05 AM
No. If it’s not `status = 'active'` in the CRM and reflected in the billing run, it doesn't exist for the board. 

**marcus.webb** — 10:10 AM
@lina.cho Can you at least check the `fact_user_events` for CUST-008? They’ve already provisioned the users. They are using the seats!

**lina.cho** — 10:15 AM
I see the activity in `nexus-analyst-demo.acme.fact_user_events`, but seat usage != paid licenses. You know the drill, Marcus. No signature, no ARR. 

---

### [2026-10-12] The "Double Counting" Debacle

**david.kim** — 02:22 PM
Hey, who updated the `ae_employee_id` for "Initech" (CUST-015)? It shows both Marcus and Sarah as owners in the latest export.

**jorge.martinez** — 02:30 PM
That’s my fault. We’re mid-migration on the territories. Sarah took over the "Mid-Market" accounts in the Southwest, but Marcus still has the legacy relationship. 

**nina.patel** — 02:35 PM
This is messing up the commission overrides. The `nexus-analyst-demo.acme.dim_customers` table should only have ONE `ae_employee_id`. 

**sarah.jenkins** — 02:40 PM
I’m fine giving Marcus the credit for the renewal, but I need the expansion quota for the 2027 kicker. 

**lina.cho** — 02:45 PM
Fixed the mapping. I updated `dim_customers` to set `ae_employee_id = 'EMP-014'` (Sarah) for Initech. Marcus, you’re still tagged as the `original_ae` in the CRM notes if anyone asks. 

**marcus.webb** — 03:00 PM
Wait, if Sarah is the AE, do I still get the invite to the Amsterdam offsite? My numbers are still tied to that region's aggregate. 

**nina.patel** — 03:05 PM
Amsterdam is for people who hit 100% of *actual* ARR, Marcus. Check your dashboard. You're at 88% because of the "Massive Dynamic" (CUST-044) delay. 

---

### [2026-11-05] Marketing Attribution / "Direct" Noise

**jorge.martinez** — 11:15 AM
@marketing-team — Why are 40% of our October signups coming through as `acquisition_channel = 'Direct'` in `nexus-analyst-demo.acme.dim_customers`? 

**lina.cho** — 11:20 AM
It’s the LinkedIn campaign. The tracking tokens were stripped by the new privacy redirect we implemented on the landing page. 

**jorge.martinez** — 11:25 AM
Great. Now the "Cost Per Acquisition" report looks like trash. I have $50k in spend with zero attributed conversions. 

**nina.patel** — 11:30 AM
Can we cross-reference the `email_domain` from `dim_users` against the lead gen list from the webinar? 

**jorge.martinez** — 11:40 AM
Trying that now. 
`SELECT u.email_domain, c.company_name FROM nexus-analyst-demo.acme.dim_users u JOIN nexus-analyst-demo.acme.dim_customers c ON u.customer_id = c.customer_id WHERE c.acquisition_channel = 'Direct' AND c.signup_date > '2026-10-01'`
Looks like "Vandelay Industries" (CUST-032) and "Gringotts" (CUST-041) were definitely from the webinar. I'll manually override the `acquisition_channel` to 'Webinar'. 

**marcus.webb** — 12:00 PM
While you're fixing things, can someone approve my T&E for the SF dinner with the "Cyberdyne" (CUST-004) CTO? It was $450. 

**nina.patel** — 12:05 PM
$450 for two people? Did you buy the restaurant? 

**marcus.webb** — 12:10 PM
It’s an Enterprise lead! Look at their `current_plan_tier`. They are on Business paying $15k MRR, but they want to move to Enterprise for the SSO/Audit logs. That's a $100k ACV jump. 

**nina.patel** — 12:15 PM
Fine. Upload the itemized receipt. If I see a bottle of 1942 on there, I’m rejecting it.

---

### [2026-11-20] Workflow Run Quotas (Overage Logic)

**david.kim** — 04:20 PM
Customer "Soylent Corp" (CUST-007) is complaining about a $2,000 overage charge. They are on the Business plan. 

**lina.cho** — 04:25 PM
Check `nexus-analyst-demo.acme.dim_plans`. Business tier has a `workflow_run_quota_per_month` of 100,000. 

**david.kim** — 04:30 PM
Yeah, I ran the numbers:
`SELECT count(*) FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE customer_id = 'CUST-007' AND triggered_at BETWEEN '2026-10-01' AND '2026-10-31'`
They hit 145,000 runs. 

**jorge.martinez** — 04:35 PM
They had a recursive loop error on one of their webhooks. Check `error_code` in `fact_workflow_runs`. 

**david.kim** — 04:40 PM
Found it. `error_code = 'ERR-429'` (Rate Limited) hit 20,000 times in two hours. We shouldn't charge them for failed runs caused by our own rate limiter tripping. 

**nina.patel** — 04:45 PM
Agreed. Lina, can you issue a credit note in `fact_invoices`? Make sure to tag it as `status = 'voided'` or issue a partial refund so the MRR calc stays clean. 

**lina.cho** — 04:50 PM
On it. I’ll update the `amount_usd` for `invoice_id = 'INV-9921'`. 

---

### [2026-12-01] End of Year Planning

**marcus.webb** — 09:00 AM
Final push for Dec! I have three Enterprise deals in "Negotiation." 

**nina.patel** — 09:10 AM
Marcus, today is the cutoff for Dec 1 billing. If they don't sign by noon, the ARR won't show up until Jan 2027. 

**marcus.webb** — 09:15 AM
Don't do this to me, Nina. My accelerator kicks in at $2M in booked ACV for the year. 

**lina.cho** — 09:20 AM
Then get them to sign. I’m looking at `nexus-analyst-demo.acme.dim_customers`. "Globex" (CUST-003) hasn't even opened the contract link. 

**jorge.martinez** — 09:25 AM
By the way, I’m purging the `dim_users` for any accounts with `status = 'churned'`. If you need historical login data for a post-mortem, grab it from the `fact_user_events` archive now. 

**david.kim** — 09:30 AM
Why purge? We might need them for win-back campaigns. 

**jorge.martinez** — 09:35 AM
Legal says we can’t keep the PII for more than 90 days post-churn for EMEA customers (GDPR). 

**nina.patel** — 09:40 AM
Listen to Jorge. Also, reminder: the holiday party is Dec 15th. Please expense your travel by then or you won't get paid until February. 

**marcus.webb** — 10:00 AM
I’ll be there. Just as soon as I close Globex. (Lina, seriously, can we backdate the start_date to Nov 30 if they sign tonight?)

**lina.cho** — 10:05 AM
No. 

**nina.patel** — 10:10 AM
Absolutely not. That’s how people get fired, Marcus. 

---

---

### [2026-01-05] Post-Holiday Cleanup & Globex Update

**marcus.webb** — 09:15 AM
Good news/bad news. Globex (CUST-003) finally signed at 11:55 PM on New Year's Eve. I sent the doc to legal. 

**nina.patel** — 09:30 AM
Marcus, that’s officially a Jan 2026 booking. The contract timestamp is UTC, so it hit at 7:55 AM Jan 1st for the system. I can’t pull that into the FY2025 board deck. 

**marcus.webb** — 09:35 AM
Are you kidding? It's $450k ACV! That puts me way over my 2025 accelerator. Nina, please. I worked through my sister's wedding dinner for this. 

**lina.cho** — 09:40 AM
The audit log in `nexus-analyst-demo.acme.fact_subscriptions` doesn't lie. `start_date` is 2026-01-01. If I move it, we have to restate the whole December MRR report for the Series B investors. Not happening. 

**jorge.martinez** — 10:05 AM
While you guys argue about Marcus’s commission, I’ve got a bigger problem. Someone uploaded a CSV of "Leads" into the `dim_customers` table directly via a bypass script. We have 400 rows with no `customer_id` and the `region` is set to 'Unknown'. 

**david.kim** — 10:10 AM
That might have been Marketing. They were trying to track the "Winter Workflow Wonderland" webinar signups. 

**jorge.martinez** — 10:15 AM
Marketing shouldn't have write-access to `nexus-analyst-demo`. I’m locking down the service account. If anyone needs to import data, use the standard ETL pipeline or it doesn't get a `surrogate_key`. 

---

### [2026-02-12] Board Deck Prep: NRR & Churn Analysis

**nina.patel** — 02:00 PM
I need the Net Revenue Retention (NRR) numbers for the last four quarters. David, can you pull this from `fact_subscriptions`? I need to see the expansion MRR vs. contraction.

**david.kim** — 02:20 PM
Pulling it now. Quick question: are we counting "Plan Downgrades" as contraction or churn? 

**lina.cho** — 02:25 PM
Contraction. Only `status = 'churned'` in `dim_customers` counts as full churn. If they move from Business ($149/seat) to Pro ($49/seat), that's `change_type = 'downgrade'` in the fact table. 

**david.kim** — 03:15 PM
Okay, I’m seeing a weird spike in `change_type = 'contraction'` for Q4 2025. Looks like a lot of the MM (Mid-Market) accounts slashed seat counts. "Cyberdyne Systems" (CUST-084) dropped from 200 seats to 50. 

**marcus.webb** — 03:20 PM
That was a budget consolidation. Their AE (Sarah) said they’re still using the platform, just "optimizing." 

**nina.patel** — 03:25 PM
"Optimizing" is AE-speak for "we're about to lose them." Nina, tag Sarah on the account health score. If our NRR drops below 110%, the board is going to grill us on the unit economics. 

**jorge.martinez** — 03:45 PM
Wait, I’m looking at `nexus-analyst-demo.acme.fact_invoices`. Cyberdyne hasn't paid their January invoice yet. `status` is still `unpaid`. 

**lina.cho** — 03:50 PM
They're on Net-45 terms. They technically have until mid-February, but let's keep an eye on it. Marcus, don't you dare book an expansion on them until that invoice clears. 

---

### [2026-03-18] Q2 Pipeline Review & Quota Mess

**marcus.webb** — 10:00 AM
I’m looking at my dashboard and my "Booked ACV" for March is showing $0. I closed Soyuz Corp (CUST-012) last week for $12k/month. 

**nina.patel** — 10:10 AM
Marcus, $12k/month is MRR. Is it a month-to-month contract or an annual? 

**marcus.webb** — 10:12 AM
Month-to-month. They wanted flexibility. 

**nina.patel** — 10:15 AM
Then it’s not ACV. ACV (Annual Contract Value) only applies to committed 12-month terms. Since it’s M2M, it shows up as `billing_cycle = 'monthly'` in `fact_subscriptions`. It won't hit your quota attainment until we've collected for 12 months, or you get them to sign an annual. 

**marcus.webb** — 10:18 AM
That’s ridiculous. Revenue is revenue. $144k is $144k. 

**lina.cho** — 10:20 AM
Not for GAAP, Marcus. If they can cancel in April, we can’t book the $144k today. Talk to Jorge about getting the `dim_plans` table updated, because Soyuz is technically on a "Business Custom" plan that isn't mapped correctly to the commission tiers. 

**jorge.martinez** — 10:30 AM
I’m not touching the plan mapping until we fix the `seat_count_licensed` vs `seat_count_active` discrepancy. I have 15 customers where `active_users` (from `dim_users`) is higher than their `licensed_seats`. We’re basically giving away seats for free. 

**david.kim** — 10:35 AM
I’ll run a query on `fact_user_events` to see who the "ghost users" are. Probably just shared logins or accounts that weren't de-provisioned. 

---

### [2026-04-22] Random / Admin

**nina.patel** — 11:00 AM
Reminder: The Q1 expense deadline is Friday. 

**jorge.martinez** — 11:05 AM
Does the "Data Team Pizza & Regret" night count as a business expense if we were fixing the `fact_workflow_runs` partitioning error until 2 AM? 

**lina.cho** — 11:10 AM
Only if you have a receipt and it's under $50/head. And no, Jorge, the "emotional damages" line item on your last report was denied. 

**marcus.webb** — 11:15 AM
Does anyone know why "Initech" (CUST-441) is showing as `status = 'paused'`? I thought they were an Enterprise lead. 

**david.kim** — 11:20 AM
They hit their `workflow_run_quota_per_month` (100k) in three days. The system auto-paused them because they don't have an overage agreement in their contract. `error_code` in the logs is `QUOTA_EXCEEDED`. 

**nina.patel** — 11:25 AM
Marcus, that’s your opening. Call them and upsell them to the "Unlimited Runs" Enterprise tier. Use the `fact_workflow_runs` data to show them they’re going to hit 1M runs by June. 

**marcus.webb** — 11:30 AM
On it. Now *that* will be ACV. 

---

### [2026-05-04] "Today" - System Status Check

**jorge.martinez** — 08:30 AM
Morning all. DBT refresh finished at 06:15 AM. Everything in `nexus-analyst-demo.acme` is current as of midnight. 

**david.kim** — 08:45 AM
I see a drop in `last_login_date` for a chunk of EMEA users in `dim_users`. Did we have an outage in the Amsterdam region? 

**jorge.martinez** — 08:50 AM
Checking `fact_workflow_runs`... `status = 'failed'` is normal. Oh, wait. There was a 15-minute blip in the Auth0 connector around 3 AM UTC. 

**nina.patel** — 09:00 AM
If it’s under our SLA (99.9%), we don’t need to issue credits. Lina, check `dim_plans.sla_uptime_pct` for the Enterprise accounts affected. If any of them are on the 99.99% tier (Tier 1 Support), we might need to be proactive. 

**lina.cho** — 09:10 AM
Only "Massive Dynamic" (CUST-005) is on the 99.99% tier. I’ll keep an eye on their support tickets. If they don’t complain, we don't volunteer the credit. 

**marcus.webb** — 09:15 AM
Spoken like a true Finance lead, Lina. Speaking of credits, did we ever fix the billing for the llama at the off-site? 

**lina.cho** — 09:20 AM
Marcus, I am literally deleting your Slack account.

---

### [2026-06-12] #rev-ops-internal - Q3 Planning & CRM Cleanup

**jorge.martinez** — 09:45 AM
Quick heads up: I’m running a bulk update on the `ae_employee_id` field in `nexus-analyst-demo.acme.dim_customers`. The Salesforce sync has been pushing NULLs for anything moved to "Closed Won" in the last 48 hours. If your dashboards look empty for new business, that’s why.

**marcus.webb** — 09:52 AM
Is that why "Globex Corp" (CUST-512) isn't showing up in my Q2 attainment report? I need that $120k ACV to hit my kicker. 

**nina.patel** — 10:05 AM
Marcus, Globex is in there, but you tagged them as `account_tier = 'SMB'` in the CRM for some reason? They have 400 seats. I had to manually override it to 'Enterprise' so the CSM assignment logic wouldn't break. 

**marcus.webb** — 10:10 AM
My bad, the dropdown was sticky. Anyway, Lina—can we talk about the commission on that one? It was a 2-year deal, paid upfront. 

**lina.cho** — 10:15 AM
I’m looking at `fact_subscriptions`. You recorded it as `$120,000` in the `mrr_usd` column. Marcus... please tell me we didn't just close a $1.4M/month account without a legal review.

**marcus.webb** — 10:18 AM
Wait, no. $120k is the Bookings ACV. Is that not what that column is for?

**lina.cho** — 10:20 AM
NO. `mrr_usd` is Monthly Recurring Revenue. If the ACV is $120k, the MRR is $10k. I have to go into the warehouse and manually adjust the `fact_subscriptions` entry before it hits the automated Board deck. If the VCs see a 300% spike in MRR followed by a "correction" next month, they’ll think we’re laundering money.

**jorge.martinez** — 10:25 AM
I’ll add a dbt test for `mrr_usd < 100000` to catch Marcus-level fat-fingering in the future. 

**david.kim** — 10:30 AM
Can we also talk about the "Summer Bash" invite? It says it’s in Napa but the calendar link points to a parking lot in Oakland.

**nina.patel** — 10:35 AM
That was the "placeholder" location. Jorge, did you finish the `acquisition_channel` cleanup? I’m trying to see if the LinkedIn spend is actually converting to 'Business' tier or just 'Pro' seat fillers.

**jorge.martinez** — 10:42 AM
Mostly done. `dim_customers.acquisition_channel` is now 90% populated. We still have about 40 legacy accounts from 2023 that are just marked as `UNKNOWN`. Probably from that first Product Hunt launch. 

---

### [2026-07-15] Board Prep - NRR & Churn Analysis

**nina.patel** — 02:00 PM
Lina, I’m pulling the Net Revenue Retention (NRR) for the last four quarters. For Q2 2026, I’m getting 118%, but the "Hooli" (CUST-099) expansion is making it look better than it is. If we exclude the top 3 expansions, we’re closer to 104%. 

**lina.cho** — 02:15 PM
104% is still healthy for our Series B stage, but the Board is going to ask about the "Initech" (CUST-441) situation. They were `status = 'paused'` last month. Did they churn or upgrade? 

**marcus.webb** — 02:20 PM
They upgraded! Marcus Webb strikes again. They’re now on an Enterprise plan, 300 seats, `billing_cycle = 'annual'`. Check `fact_subscriptions` for `change_type = 'upgrade'`. 

**jorge.martinez** — 02:25 PM
Actually, Marcus, looking at `fact_subscriptions` right now for CUST-441... the `start_date` was July 1st, but the `end_date` is July 31st? You put them on a monthly Enterprise plan? 

**marcus.webb** — 02:28 PM
What? No, they signed for a year. 

**lina.cho** — 02:30 PM
Jorge is right. The `fact_subscriptions` table shows it as monthly. If they don't auto-renew or if the invoice fails, they’ll show up as churned in 15 days. Marcus, I need the signed PDF. If it’s not in the 'Legal_Final' folder, the revenue doesn't exist.

**david.kim** — 02:45 PM
While you guys fight over the money, we’ve got a spike in `error_code = 'RATE_LIMIT_EXCEEDED'` for the 'Stark Industries' (CUST-012) account. They’re running a loop that’s hitting the `fact_workflow_runs` table pretty hard. 15k runs in the last hour. 

**nina.patel** — 02:50 PM
They’re on the Enterprise tier, so they have "Unlimited" runs, but our infrastructure doesn't. David, can we throttle them without breaking their SLA? Lina, check `dim_plans.sla_uptime_pct` for them. 

**lina.cho** — 03:00 PM
They’re on the 99.9% tier. We have some wiggle room. But they’re paying us $200k ARR—don't break their workflows on a Friday afternoon.

---

### [2026-08-01] General / Random

**marcus.webb** — 11:00 AM
Has anyone seen my "World's Best AE" mug? It’s not in the breakroom. 

**lina.cho** — 11:05 AM
I saw it in the dishwasher. Next to the stack of receipts you still haven't scanned from the Amsterdam trip. 

**jorge.martinez** — 11:10 AM
Just a reminder: `nexus-analyst-demo.acme.fact_user_events` is moving to a partitioned table tonight. If your SQL queries fail tomorrow morning, it's because you didn't include a `WHERE event_at > ...` filter. Don't @ me. 

**david.kim** — 11:15 AM
Wait, does that affect the `is_active` flag in `dim_users`? 

**jorge.martinez** — 11:20 AM
No, `dim_users` is a flat dimension. But the daily active user (DAU) rollups will time out if you try to scan the whole history. We have 12 million events in that table now. 

**nina.patel** — 11:30 AM
12 million? Wow. Remember when we were excited about hitting 100 runs a day in 2023? 

**marcus.webb** — 11:35 AM
I remember. I also remember the commission checks being smaller. Let's keep it growing. Quick check—who's up for a "Deal Review" lunch at the taco place? My treat (Lina, I'll keep the receipt under $50, I promise). 

**lina.cho** — 11:40 AM
Only if you fix the Globex MRR entry first. I'm not eating tacos with a $1.4M reporting error hanging over my head.

---

### [2025-08-15] #revenue-ops

**lina.cho** — 09:15 AM
@jorge.martinez I’m looking at the `nexus-analyst-demo.acme.fact_subscriptions` table and the Globex (CUST-044) entry is still showing a $1.4M MRR instead of ACV. It’s skewing the entire Q3 forecast. 

**jorge.martinez** — 09:22 AM
That's because someone (looking at you @marcus.webb) entered the total contract value into the `mrr_usd` field in the CRM instead of the `bookings_acv_usd` field. The sync script just pulls what’s there. I can’t hardcode fixes for every fat-finger error.

**marcus.webb** — 09:30 AM
Hey, it was a late night! We closed that deal at 11:58 PM on the last day of the month. I just wanted to get it in so I could sleep. 

**lina.cho** — 09:35 AM
Well, your "sleep" just gave our VP of Finance a heart attack when she saw a 400% jump in Net Retention. Fix the CRM record, and Jorge, can you trigger a manual refresh of `fact_subscriptions` once he's done?

**jorge.martinez** — 09:40 AM
Fine. But if I have to rebuild the `dim_customers` downstream model again today because of a manual override, I’m charging it to the Sales SPIF fund. 

---

### [2025-10-02] #revenue-ops / Board-Prep

**nina.patel** — 02:00 PM
Need a final NRR (Net Revenue Retention) number for the Q3 board deck. Are we excluding the 'Cyberdyne' (CUST-089) churn? They technically paused, they didn't cancel. 

**lina.cho** — 02:05 PM
They haven't paid an invoice in 90 days and their `status` in `dim_customers` is 'paused'. For the board, we report them as churn. We can't fluff the NRR with "maybe" money. 

**david.kim** — 02:15 PM
If you check `nexus-analyst-demo.acme.fact_user_events`, Cyberdyne’s last `login_at` was July. They’re gone, Nina. Even their `is_active` flags in `dim_users` are mostly false now. 

**nina.patel** — 02:20 PM
Ugh, fine. Marcus, what happened there? They were one of our biggest Business tier accounts in EMEA. 

**marcus.webb** — 02:25 PM
Internal restructuring. Their new CTO wants to build an in-house version of our workflow engine. Good luck to them, they’ll spend $2M in engineering hours to replace a $120k subscription. 

**lina.cho** — 02:30 PM
Doesn't matter now. Current Q3 NRR is sitting at 112%. If we count the Wayne Enterprises (CUST-005) expansion, we might hit 115%. 

---

### [2026-01-12] #revenue-ops / Quota-Updates

**marcus.webb** — 10:00 AM
Wait, why is my quota attainment only at 82%? I closed the 'Hooli' (CUST-211) deal last week. 

**lina.cho** — 10:05 AM
Hooli is on a multi-year ramp. You only get credit for the Year 1 ACV, not the total contract value. Read the comp plan, Marcus. It’s page 14, under "Multi-Year Incentives." 

**marcus.webb** — 10:10 AM
That’s ridiculous. I did the work for all three years now! 

**jorge.martinez** — 10:15 AM
Lina, I’ve updated the `nexus-analyst-demo.acme.dim_employees` table to reflect the new territory assignments for 2026. Marcus is now officially covering "North America - West" and "Global Accounts - Stark." 

**david.kim** — 10:20 AM
Does that mean Marcus is responsible for the Stark Industries (CUST-012) rate limiting issues I mentioned last week? They’re still hitting the `fact_workflow_runs` table with 10k+ concurrent requests every Tuesday at 9 AM UTC. 

**marcus.webb** — 10:25 AM
If it gets me more commission, I'll go to their office and manually click the "Run" button for them. 

**nina.patel** — 10:30 AM
David, let’s set up a call with their technical lead. If they’re hitting limits that hard, they need to move to the 'Enterprise Plus' tier (even if it's not on the public pricing page yet). We need to monetize that infrastructure load. 

---

### [2026-04-20] General / Random

**jorge.martinez** — 09:00 AM
Heads up: I’m running a vacuum on the `nexus-analyst-demo.acme.fact_user_events` table during the lunch hour. Expect some latency if you’re trying to run heavy aggregations on `event_at`. 

**lina.cho** — 09:05 AM
Perfect timing. I need to pull the trailing 12-month (TTM) revenue by `acquisition_channel` from `dim_customers`. Will that be affected?

**jorge.martinez** — 09:10 AM
No, `dim_customers` is fine. It’s just the raw event data that’s being locked. Why TTM now? 

**lina.cho** — 09:15 AM
Preparation for the Series C talks. VCs love seeing that 'Organic' and 'Referral' channels have a higher LTV/CAC ratio than 'Paid Social'. 

**marcus.webb** — 09:20 AM
Speaking of 'Paid Social', who approved the LinkedIn ad with the typo in "Automation"? It says "Automaiton." I’ve had three prospects point it out to me today. 

**nina.patel** — 09:25 AM
Marketing says it’s an "engagement hack." People comment to correct the spelling, which boosts the algorithm. 

**david.kim** — 09:30 AM
That sounds like a bug being rebranded as a feature. Classic. 

**lina.cho** — 09:40 AM
Anyway, Marcus, I sent your expense report back. You can't claim a "networking dinner" that consists entirely of Topo Chico and three orders of truffle fries. Especially not when the receipt is from a bowling alley. 

**marcus.webb** — 09:45 AM
It was a "Team Building" event with the champion users at Oscorp (CUST-099)! We discussed their API integration strategy between frames. 

**lina.cho** — 09:50 AM
Denied. Get a signature from the Oscorp VP, then we'll talk. 

**jorge.martinez** — 10:00 AM
Table maintenance finished early. You can go back to your SQL queries and your truffle fry arguments. `fact_workflow_runs` is now indexed by `customer_id` for faster lookups. You’re welcome.

---

### [2026-05-01] #revenue-ops / Q1-Wrap-Recon

**lina.cho** — 08:45 AM
@channel I’m looking at the April month-end close in `nexus-analyst-demo.acme.fact_subscriptions` and someone has entered the renewal for 'Cyberdyne Systems' (CUST-412) as $450,000 in `mrr_usd`. Please tell me this is a typo and we didn't actually close a $5.4M ARR deal overnight without me knowing.

**marcus.webb** — 08:52 AM
My bad Lina!! I was looking at the Total Contract Value (TCV) for the 3-year term. I thought the field was `bookings_acv_usd`. 

**lina.cho** — 09:00 AM
Marcus, we’ve talked about this. `fact_subscriptions` tracks MRR. If it’s $450k TCV over 36 months, that’s $12,500 MRR. You are inflating our North Star metrics by 3,500%. I’m reverting the row in the source sheet now. 

**jorge.martinez** — 09:15 AM
This is why I keep pushing for the Salesforce to BigQuery sync to be read-only for AEs. @marcus.webb, please stop manual overrides in the `dim_customers` staging tab. It breaks my join on `ae_employee_id` when you put "Marcus - The Closer" instead of your ID. 

**marcus.webb** — 09:20 AM
It was a joke! A little Friday motivation. Anyway, the Cyberdyne deal is solid. They’re moving from 'Pro' to 'Enterprise' because they hit the 10k run limit on `fact_workflow_runs` by the 10th of every month. 

**sarah.jenkins** — 10:30 AM
Lina, do we have the final NRR (Net Retention Rate) for Q1 ready for the board deck? I need to show the impact of the 'Business' tier price hike. 

**lina.cho** — 10:45 AM
Working on it. Preliminary looks like 118%, but I’m seeing some weird churn signaling from the SMB segment. We had 12 'Pro' accounts drop in March. Mostly `acquisition_channel` = 'Paid Social'. 

**nina.patel** — 10:50 AM
Those are the "Automaiton" leads. I told you the engagement hack worked, even if the conversion quality is lower. 

**david.kim** — 11:00 AM
Quality > Quantity, Nina. My on-call devs are tired of debugging "Hello World" workflows from trial users who don't know how to config a webhook. 

---

### [2026-05-03] #pipeline-review-weekly

**marcus.webb** — 02:00 PM
Quick update on the 'Starlight Media' (CUST-882) expansion. They want to provision 300 new seats, which triggers the 'Enterprise' floor. They’re asking for a 15% discount on the seat price because they don't need the 'Dedicated CSM' part of the bundle.

**sarah.jenkins** — 02:15 PM
No discounts on the seat floor. Tell them the CSM is "complimentary" but the platform fee is non-negotiable. We need to maintain that $149/seat blended average for the 'Business' to 'Enterprise' bridge.

**lina.cho** — 02:20 PM
Agreed. If we discount Starlight, every other media account in the `dim_customers` table will demand the same when they see the benchmarks. Marcus, check `nexus-analyst-demo.acme.dim_plans`—the 'Enterprise' tier pricing is custom, but we have a floor for a reason. 

**marcus.webb** — 02:25 PM
Copy that. I'll pivot to the "Security & Audit Logs" angle. Their IT manager was complaining about not seeing who triggered the failed runs in `fact_workflow_runs`. 

**jorge.martinez** — 02:30 PM
Tell him to use the `triggered_by` column. It’s literally right there. I even added the `email_domain` join from `dim_users` for the last Audit report. 

**lina.cho** — 03:00 PM
Reminder: Tacos at 4 PM in the breakroom for Chloe’s work-anniversary. 

**marcus.webb** — 03:05 PM
Can I expense the Uber there? 

**lina.cho** — 03:06 PM
You work in the SF office, Marcus. The breakroom is 20 feet from your desk. 

---

### [2026-05-04] #data-ops-noise

**jorge.martinez** — 08:00 AM
@lina.cho I noticed a spike in `fact_invoices` where `status` = 'voided' for several 'Pro' customers this morning. Looks like a Stripe API hiccup during the monthly billing cycle. 

**lina.cho** — 08:15 AM
I see it. It’s affecting the `current_mrr_usd` calculation in the daily dashboard. About $4k is missing. Do not refresh the `dim_customers` snapshot until I manually verify the payment status. I don't want to report a dip to Sarah if it’s just a sync error. 

**jorge.martinez** — 08:30 AM
Roger that. I’ll hold the dbt run for `fct_mrr_movements`. 

**chloe.zhang** — 09:00 AM
Hey team, I'm seeing some duplicates in `dim_customers` for 'Tyrell Corp'. One is CUST-551 and the other is CUST-902. Both have the same `ae_employee_id` (Marcus). 

**marcus.webb** — 09:05 AM
Ah, yeah. They signed up with two different domains. One for the Replicant division and one for Corporate. I was going to merge them once the Enterprise contract is signed. 

**lina.cho** — 09:10 AM
Marcus, this is exactly why our "Unique Customer" count is always messy. Jorge, can you flag these as `is_active` = FALSE for the duplicate ID so it doesn't double-count in the ARR recon? 

**jorge.martinez** — 09:15 AM
On it. I’ll update the `status` to 'paused' for CUST-551 and point everything to CUST-902 in `fact_workflow_runs`. But Marcus, you owe me. Those truffle fries from Oscorp would be a good start. 

**marcus.webb** — 09:20 AM
Lina won't let me expense them! But I’ll bring in some of those fancy donuts from the place in the Mission tomorrow. 

**lina.cho** — 09:25 AM
Only if they aren't "engagement hack" donuts with intentional missing sprinkles. 

**nina.patel** — 09:30 AM
Hey! That was one time! 

**jorge.martinez** — 11:00 AM
dbt run complete. MRR is back to $39.2M. The voided invoices were just a timeout. All `fact_invoices` for the 'Pro' tier are now showing `paid_at` timestamps correctly. We are green for the board prep.

---

### [2026-05-12] #rev-ops-pipeline

**marcus.webb** — 02:15 PM
Massive news! Just closed the expansion for 'Wayne Enterprises' (CUST-412). They’re moving from Business to Enterprise. Adding 300 seats. That puts another $450k in the "won" column for May! 🚀

**lina.cho** — 02:45 PM
Wait, Marcus. $450k? Are you looking at the ACV or the MRR? 

**marcus.webb** — 02:47 PM
The total contract value is $450k for the year. That’s what I put in the "Bookings" tab.

**lina.cho** — 02:50 PM
Okay, we need to be very careful with terminology for the board deck. ACV is $450k, but the `mrr_usd` in `nexus-analyst-demo.acme.fact_subscriptions` will show $37,500. Jorge, when you run the `fct_mrr_movements` model tonight, make sure the `change_type` is tagged as 'expansion' and not 'new_biz'. 

**jorge.martinez** — 03:00 PM
Got it, Lina. I’ll double-check the `changed_from_subscription_id` logic. If Marcus didn't close the old sub in Salesforce correctly, the SQL might treat it as a churn + new biz, which will mess up our NRR (Net Revenue Retention) calc. 

**marcus.webb** — 03:05 PM
My bad. Salesforce is being a pain again. It kept timing out when I tried to link the opportunities. I’ll go back in and fix the parent-child relationship for the accounts. 

**chloe.zhang** — 03:15 PM
Speaking of NRR, @lina.cho I’m seeing some weirdness in `nexus-analyst-demo.acme.dim_customers` for the EMEA region. 'Globex Corp' (CUST-112) is showing a `current_mrr_usd` of $0 but the `status` is still 'active'. 

**elias.vogel** — 03:20 PM
That’s because they’re on a holiday "grace period." Their procurement team in Amsterdam is restructuring. I gave them 30 days of "free" Business tier to keep them from churning while the PO clears. 

**lina.cho** — 03:25 PM
Elias, we can't have "active" customers with $0 MRR in the Business tier. It skews the ARPU (Average Revenue Per User). Jorge, can you please manually override CUST-112 to `status` = 'paused' in the analytics layer until the payment hits? 

**jorge.martinez** — 03:30 PM
Sure, but that’s going to trigger a "contraction" event in the dashboard. Sarah is going to ask why we lost $7.5k in MRR overnight. 

**lina.cho** — 03:35 PM
I’ll add a note in the "Revenue Leakage" sheet. Better to show contraction than fake active revenue. 

---

### [2026-05-15] #board-prep-q2

**lina.cho** — 09:00 AM
@jorge.martinez @chloe.zhang we need the final NRR and Gross Retention numbers for April by EOD. Sarah needs them for the prelim board deck. Use the `nexus-analyst-demo.acme.fact_subscriptions` table for the denominator (start of month MRR). 

**chloe.zhang** — 10:30 AM
Lina, looking at the data, our NRR for the Enterprise segment is at 124%—mostly driven by the 'Tyrell Corp' and 'Soylent Corp' expansions last quarter. But SMB is dragging us down. Pro tier churn is up to 4.2% this month. 

**jorge.martinez** — 10:45 AM
I’m looking at `fact_workflow_runs` for the churned Pro accounts. A lot of them have `error_code` = 'RATE_LIMIT_EXCEEDED' in the week before they cancelled. It looks like they hit the 10k run quota and just quit instead of upgrading to Business. 

**maya.kapoor** — 11:00 AM
I’ve been saying this! The jump from $49/seat to $149/seat is too steep for the mid-market guys. They’d rather just go back to Zapier. 

**lina.cho** — 11:15 AM
We can’t change pricing before the board meeting. For now, just report the numbers as-is. Jorge, run the query on `nexus-analyst-demo.acme.dim_customers` to pull the `acquisition_channel` for those churned Pro accounts. I want to see if this is a "Marketing" problem (bad leads) or a "Product" problem (quota friction). 

**jorge.martinez** — 11:30 AM
Running it now... 
`SELECT acquisition_channel, COUNT(*) FROM nexus-analyst-demo.acme.dim_customers WHERE current_plan_tier = 'Pro' AND status = 'churned' GROUP BY 1`
...Looks like 60% came from "Product Hunt" and "Paid Social". 

**nina.patel** — 11:45 AM
Hey! Don't blame my ads! If they're hitting rate limits, that means they're finding value. That's a conversion friction issue, not a lead quality issue. 

**lina.cho** — 12:00 PM
Let’s take the pricing discussion to the #product-strategy channel. Nina, please stop "accidental" spending on the LinkedIn "Enterprise Automation" campaign until we fix the landing page for the $149 tier. I saw the $12k invoice this morning. 

**nina.patel** — 12:05 PM
That wasn't accidental! That was for the APAC launch! 

---

### [2026-05-18] #ops-random

**marcus.webb** — 04:00 PM
Quick question—has anyone seen the HDMI-to-USB-C dongle in the 'Zion' conference room? I have a demo with 'Cyberdyne' in 10 minutes and I can't plug in. 

**jorge.martinez** — 04:02 PM
I think I saw Ben take it to the 'Nirvana' room for the engineering sync. 

**marcus.webb** — 04:05 PM
Ben! I’m dying here. Cyberdyne is a $200k potential. I can’t do a demo over a 13-inch laptop screen. 

**lina.cho** — 04:10 PM
Marcus, just use the Owl. And while you’re at it, please submit your expense report for the "prospecting dinner" at 'Genco Olive Oil'. $800 for three people? Did you guys order the entire cellar? 

**marcus.webb** — 04:15 PM
They’re a high-value target! Plus, their CTO really likes Barolo. It’s all in the service of the ARR, Lina. 

**lina.cho** — 04:20 PM
The ARR doesn't exist until the `paid_at` column in `fact_invoices` has a timestamp. No more Barolo until the contract is signed. 

---

### [2026-05-20] #data-integrity-alert

**jorge.martinez** — 08:30 AM
@chloe.zhang I’m seeing a weird spike in `fact_user_events`. A single user at 'Stark Industries' (CUST-004) has generated 45,000 `workflow_triggered` events in the last 2 hours. 

**chloe.zhang** — 08:45 AM
Is it a loop? Check the `error_code` in `fact_workflow_runs`. 

**jorge.martinez** — 09:00 AM
No errors. `status` = 'success'. It looks like they’re testing a massive data migration using our webhooks. At this rate, they’ll hit their monthly quota by lunch. 

**maya.kapoor** — 09:15 AM
I’ll reach out to their admin. Stark Industries is on the Enterprise plan, so they have "unlimited" runs, but our infra team (Dave) is going to kill me if they spike the compute costs like this. 

**lina.cho** — 09:30 AM
Maya, while you have them on the phone, see if they want to buy the "Dedicated Compute" add-on. If they’re going to treat us like a bulk ETL tool, they should pay for the extra storage. Jorge, can you calculate the `storage_gb` usage for CUST-004 from `dim_plans` vs their actual usage in the metadata? 

**jorge.martinez** — 09:45 AM
On it. Querying `nexus-analyst-demo.acme.fact_workflow_runs`. 
`SELECT customer_id, SUM(step_count) * 0.01 AS estimated_gb FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE customer_id = 'CUST-004' GROUP BY 1`
...Yeah, they're at 85GB. Their plan limit is 50GB. 

**lina.cho** — 10:00 AM
Perfect. Maya, that's an easy $5k expansion. Get it done before the EOM cutoff. 

**maya.kapoor** — 10:15 AM
On it. "Stark" usually doesn't care about the price as long as it doesn't break. 

**marcus.webb** — 10:30 AM
Wish all my deals were like that. 'Cyberdyne' is still haggling over the SOC2 report. @lina.cho can you ping Legal? 

**lina.cho** — 10:45 AM
Legal is busy with the Series C audit prep. You’ll have to wait until Thursday. 

---

### [2026-05-22] #it-and-facilities

**jorge.martinez** — 11:00 AM
Office update: The cold brew tap is broken again. Please do not try to "fix" it by hitting the nozzle. Looking at you, Sales team. 

**marcus.webb** — 11:05 AM
Hey, I was just trying to get it flowing! It’s a workflow automation company, we should be able to automate a coffee tap. 

**lina.cho** — 11:10 AM
Maybe we can create a `fact_coffee_consumption` table to see who’s breaking it. 

**jorge.martinez** — 11:15 AM
Don’t give me more dbt work, Lina. I’m still trying to clean up the `email_domain` logic in `dim_users` because people keep signing up with `gmail.com` instead of their corporate accounts. We have 4,000 "users" that are just generic emails. 

**chloe.zhang** — 11:20 AM
Actually, that's a great signal for PLG expansion. If we see 10+ Gmail users from the same IP, we should flag that for Marcus to go hunting. 

**marcus.webb** — 11:25 AM
Now you're talking! Jorge, can you build me a Looker dashboard for "Hidden Account Clusters"? 

**jorge.martinez** — 11:30 AM
Only if Marcus buys the donuts for the next three Fridays. No "engagement hacks" allowed. 

**marcus.webb** — 11:35 AM
Deal. Done. 

**lina.cho** — 11:40 AM
I’m holding you to that. Jorge, put it on the sprint board. `ref('fct_user_ip_clusters')`. Use `nexus-analyst-demo.acme.fact_user_events` as the source. 

---
### [2026-05-25] #billing-reconciliation

**lina.cho** — 04:00 PM
Monthly close is starting. @jorge.martinez, please lock the `fact_invoices` table for April. No more retroactive updates. 

**jorge.martinez** — 04:10 PM
Locked. Final ARR for April 2026 is $39.42M. 

**lina.cho** — 04:15 PM
Wait, why is it higher than last week? 

**jorge.martinez** — 04:20 PM
Found a missing batch of 'Pro' tier renewals that hadn't synced from the Stripe-BigQuery connector. About $20k in MRR. 

**lina.cho** — 04:25 PM
Bless you, Jorge. Sarah is going to be very happy. That puts us just shy of the $40M goal for Q2. 

**marcus.webb** — 04:30 PM
I’ll get us over the line with 'Cyberdyne' next week. Mark my words. 

**lina.cho** — 04:35 PM
We’ll see. Don't forget the donuts.

---
### [2026-06-01] #pipeline-review

**marcus.webb** — 09:15 AM
Good morning team. Huge week. I’ve got the Cyberdyne Systems contract on my desk. Just waiting for their legal to stop redlining the indemnity clause. It’s a 300-seat Enterprise deal. 

**lina.cho** — 09:20 AM
300 seats? Is that at the standard $149 Business rate or a custom Enterprise floor?

**marcus.webb** — 09:22 AM
Custom. We landed at $450k ACV including the premium support add-on. 

**jorge.martinez** — 09:25 AM
Wait, Marcus. I'm looking at the Opportunity in Salesforce right now. You put the "Amount" as $450,000 but the "Close Date" is June 15th. If that’s ACV, I need to make sure the `fact_subscriptions` logic doesn't treat that as a monthly payment. Remember the Globex disaster where we reported $12M in monthly revenue because of a decimal error?

**marcus.webb** — 09:28 AM
I fixed it! It’s tagged as 'Annual Billing'. 

**lina.cho** — 09:30 AM
Jorge, please double-check the `nexus-analyst-demo.acme.fact_subscriptions` table once Marcus marks it Closed-Won. I don't want the NRR calculation for the Board Deck to be skewed by one fat-fingered entry. 

**jorge.martinez** — 09:35 AM
I’m already seeing issues. Someone entered a "test" deal for 'Wayne Enterprises' last night for $1B. I assume that was you, Marcus, testing the "limits of the system"?

**marcus.webb** — 09:37 AM
Manifesting, Jorge. It’s called manifesting. I’ll delete it. 

---
### [2026-06-05] #board-prep-nrr

**lina.cho** — 11:00 AM
@jorge.martinez do we have the final Net Revenue Retention (NRR) numbers for May? Sarah needs them for the Monday morning sync with the investors. 

**jorge.martinez** — 11:15 AM
Running the dbt model now. `fct_customer_nrr` is taking forever because of the join on `dim_customers` to get the `account_tier` history. 

**lina.cho** — 11:20 AM
Why? Is the warehouse lagging?

**jorge.martinez** — 11:25 AM
No, it’s the data quality in the `acquisition_channel` column. Half the rows are NULL for the 2024 cohorts, so the window functions are getting messy. I'm seeing 114% NRR for the Enterprise segment, but SMB is dragging us down to 98% because of the 'Pro' tier churn. 

**chloe.zhang** — 11:30 AM
98% for SMB isn't terrible given the macro environment, but we need to see if those 'Pro' users are actually churning or just moving to 'Free' because they hit their workflow run limits and got scared of the overage charges. 

**jorge.martinez** — 11:35 AM
Looking at `nexus-analyst-demo.acme.fact_workflow_runs`. Yeah, we have a cluster of users at 9,900 runs (quota is 10k) who just stop. They aren't churning; they're hibernating. 

**lina.cho** — 11:40 AM
That’s a product problem. Chloe, can we trigger an automated email for people at 90% quota? 

**chloe.zhang** — 11:45 AM
On it. I'll sync with the Growth team. Jorge, can you give me a list of `user_id`s from `dim_users` who hit 90% in the last 7 days?

**jorge.martinez** — 11:50 AM
SQL incoming. I’ll dump it in the #marketing-alerts channel. 

---
### [2026-06-10] #ops-noise-and-expenses

**marcus.webb** — 02:00 PM
@lina.cho, I just submitted my expenses for the Amsterdam trip. I know the steakhouse receipt is high, but that was the 'Massive Dynamic' CTO. We’re talking a potential 500-seat expansion. 

**lina.cho** — 02:05 PM
Marcus, it’s $1,200 for four people. Did you order the wine cellar? 

**marcus.webb** — 02:06 PM
It was a "strategic engagement dinner." 

**lina.cho** — 02:10 PM
I’ll approve it this once, but if Massive Dynamic doesn't move to the 'Enterprise' tier by end of Q3, I'm deducting it from your donut budget. 

**jorge.martinez** — 02:15 PM
Speaking of budgets, can we get a license for the new BigQuery optimization tool? My queries against `fact_user_events` are costing us a fortune because people keep doing `SELECT *` without a date partition. 

**lina.cho** — 02:20 PM
Who is doing `SELECT *`? 

**jorge.martinez** — 02:22 PM
(Looking at logs...) It's the new intern in Marketing. 

**chloe.zhang** — 02:25 PM
I’ll talk to him. Sorry. He thought he was just "browsing the data." 

**jorge.martinez** — 02:30 PM
Tell him the "data" costs $5.00 per TB scanned. He "browsed" $400 this morning. 

---
### [2026-06-12] #crm-migration-blues

**jorge.martinez** — 09:00 AM
The Fivetran sync for the Salesforce `Opportunity` table failed at 3 AM. We’re missing all deal updates from yesterday. 

**marcus.webb** — 09:05 AM
That explains why my dashboard shows $0 for June. I almost had a heart attack. 

**lina.cho** — 09:10 AM
Is this related to the custom field change you made for the "Workday Integration" checkbox? 

**jorge.martinez** — 09:15 AM
Precisely. The schema change broke the connector. I have to manually remap the fields in the `nexus-analyst-demo.acme.fact_subscriptions` pipeline. This is why we have a change management process, Marcus! 

**marcus.webb** — 09:20 AM
I needed that field for the Q3 forecast! Marketing needs to know how many customers are asking for Workday vs. SAP. 

**chloe.zhang** — 09:22 AM
He’s right, we do need it, but maybe don’t break the entire data warehouse to get it? 

**jorge.martinez** — 10:00 AM
Fixed. But the data is still refreshing. Don’t trust the Looker tiles until the Slack bot posts the "Dbt Cloud Run Successful" message. 

**lina.cho** — 10:15 AM
While you're in there, Jorge, can you check why 'Initech' is showing as 'Active' in `dim_customers` but their last invoice in `fact_invoices` was from February? 

**jorge.martinez** — 10:20 AM
Checking... Ah, looks like they moved to a "Legacy" billing cycle that isn't caught by the `is_current` flag in the subscription table. I’ll add a jira ticket. `DATA-402: Handle legacy billing edge cases`. 

**marcus.webb** — 10:25 AM
Initech is still using the platform. I saw their admin logged in yesterday via `fact_user_events`. They're running 50k workflows a month. We’re basically giving it away for free. 

**lina.cho** — 10:30 AM
Not for long. Marcus, that’s your first call for Monday. Collections or Upsell. Pick one. 

**marcus.webb** — 10:35 AM
Upsell. Always upsell. 

---
### [2026-06-15] #donuts-and-deals

**marcus.webb** — 08:30 AM
Donuts are in the breakroom. Glazed, old fashioned, and those weird maple bacon ones Jorge likes. 

**jorge.martinez** — 08:35 AM
The maple bacon ones are a delicacy. Thank you. 

**lina.cho** — 08:40 AM
Status on the $40M goal? 

**marcus.webb** — 08:45 AM
Cyberdyne signed! Just got the DocuSign notification. $450k ACV. 

**jorge.martinez** — 08:50 AM
I’ll refresh the `fact_invoices` table. If my math is right, that puts us at $39.87M. 

**lina.cho** — 08:55 AM
So close. Who’s got the remaining $130k? 

**marcus.webb** — 09:00 AM
I’ve got a 'Soylent Corp' expansion and a small Pro-to-Business flip for 'Vandelay Industries'. We’ll hit it by Friday. 

**chloe.zhang** — 09:05 AM
I'll go tell Sarah. She’s going to want to announce it at the All-Hands. 

**lina.cho** — 09:10 AM
Wait for the funds to clear first, Chloe. Let’s not pull a "2024" again. 

**chloe.zhang** — 09:12 AM
We do not speak of 2024. 

**jorge.martinez** — 09:15 AM
Agreed. My SQL code still has comments in it from the "Great Reversal" of '24. Never again.