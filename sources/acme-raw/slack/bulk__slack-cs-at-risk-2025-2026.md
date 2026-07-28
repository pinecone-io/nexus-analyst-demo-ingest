---
title: "Slack #cs-at-risk channel archive — 2025-2026"
source_url: "internal://acme/slack-cs-at-risk-2025-2026"
license: "synthetic-demo"
attribution: "Synthetic content, Acme Inc internal demo. Acme Inc is a fictitious company."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

# #cs-at-risk — 2025-06-03 — New Health Model Rollout

**elena.volkov** — 9:15 AM
@here Morning team. We’re officially moving the health tracking into the `account_health` table in BigQuery today. No more manual spreadsheets for risk reporting. If an account hits 'critical', I want a thread in here within 4 hours. 

**marco.silva** — 9:22 AM
Copy that Elena. Are we still using the old engagement definition? 

**rajiv.menon** — 9:25 AM
@marco.silva No, we updated it. Engaged is now >= 3 active users AND >= 10 successful runs in the last 28 days. Anything less and the `is_engaged` flag drops to false and they move to 'monitoring' or 'at_risk'.

**grace.liu** — 9:30 AM
Wait, 3 users? Pebble Digital (cust_000705) only has 6 seats total because they’re on Pro. They’ve been at 2 active users for months but they love the product. That’s going to flag them as not engaged?

**rajiv.menon** — 9:32 AM
Yeah, the math is the math. If they only have 2 users, they don't meet the sticky threshold we saw in the H1 churn analysis.

**grace.liu** — 9:33 AM
That feels aggressive for the smaller Pro accounts. 

**nina.patel** — 9:45 AM
@grace.liu we can't maintain 50 different definitions of engagement. 3 users is the floor for "org-wide adoption" even at the small end.

**olivia.tran** — 10:12 AM
Question on the new table—I’m looking at Marigold Health (cust_000701). They have a late invoice from last month but they’re showing as 'stable' in the health status. Shouldn't that be critical?

**lina.cho** — 10:15 AM
@olivia.tran checking... Marigold is Enterprise. For Enterprise, the critical trigger is only for *uncollectible* invoices. If it’s just 'overdue' it doesn't auto-flip to critical yet because Ent billing cycles are messy.

**olivia.tran** — 10:17 AM
Got it. So critical is only uncollectible for Ent? What about Business tier?

**lina.cho** — 10:19 AM
For Business and Pro, critical triggers on *either* uncollectible invoices OR utilization_band < 0.20. Enterprise doesn't have the utilization trigger for critical because they have unlimited seat contracts sometimes, so the ratio gets wonky.

**marco.silva** — 11:05 AM
Does anyone know if we're doing the team lunch today? Or is that Thursday?

**sarah.chen** — 11:06 AM
Thursday! Taco truck is coming to the SF parking lot.

**marco.silva** — 11:06 AM
Sweet. 

---

# #cs-at-risk — 2025-07-15 — Cobalt Systems Flag

**marco.silva** — 2:30 PM
Heads up on Cobalt Systems (cust_000700). Tom Becker just heard from their Ops Lead that they’re looking at "tool consolidation" for Q4. 

**elena.volkov** — 2:32 PM
Ugh, consolidation is the word of the year. What’s their current health?

**marco.silva** — 2:35 PM
They're 'stable' right now in `acme.account_health`. Utilization is 0.75, 80 seats licensed, most of them active. But this is a budget conversation, not a usage one.

**tom.becker** — 2:40 PM
Yeah, their CFO is the one pushing it. I’m trying to get a meeting with them to show the ROI. @rajiv.menon can we pull their Value Realization Score (VRS) to show the CFO?

**rajiv.menon** — 2:42 PM
VRS is still in draft, Tom. David started the spec but we haven't built the `vrs_band` columns in BQ yet. Just use the `account_health` data for now and maybe pull some `fact_workflow_runs` to show how many hours they’re saving.

**tom.becker** — 2:45 PM
Wait, I thought VRS was live? I told the customer we’d have a value report for them.

**david.kim** — 2:48 PM
@tom.becker No, that got parked. Use `nexus-analyst-demo.acme.workflow_runs_daily` to build your own view of their success rates. If they have high success and high volume, that's your ROI story.

**marco.silva** — 3:00 PM
Adding a manual 'at_risk' flag in the CRM for Cobalt for now.

---

# #cs-at-risk — 2025-08-22 — Onyx Robotics Confusion

**olivia.tran** — 11:15 AM
Hey @lina.cho — looking at Onyx Robotics (cust_000704). They’re Enterprise, and they have an open P1 ticket that’s been sitting for 72 hours. Why are they still showing 'healthy_expansion' in the health table?

**lina.cho** — 11:20 AM
Checking the logic... oh, I see. `account_health.at_risk` triggers if there’s an open P1 > 48h, but Onyx has `healthy_expansion` because their engagement is through the roof. 

**olivia.tran** — 11:22 AM
But the rule for `at_risk` says it should override healthy status if a P1 is open too long, right?

**lina.cho** — 11:25 AM
Actually, let me look at the SQL. `CASE WHEN has_open_p1_over_48h THEN 'at_risk' ...` Ah, wait. It looks like the `healthy_expansion` logic block is higher up in the CASE statement than the P1 check. It's hitting the expansion criteria first and exiting.

**rajiv.menon** — 11:28 AM
@lina.cho Good catch. We should probably swap those. Support issues should trump expansion signals. I’ll push a dbt fix for `account_health` tomorrow morning.

**olivia.tran** — 11:30 AM
Thanks! Yeah, they’re definitely not in an expansion mood with their production workflows failing.

**grace.liu** — 11:45 AM
Anyone seen my blue Yeti bottle? Left it in the "Big Sur" conference room.

**omar.haddad** — 11:47 AM
I saw it on the kitchen counter next to the espresso machine.

---

# #cs-at-risk — 2025-10-12 — Yarrow Logistics Drop

**marco.silva** — 9:02 AM
Flagging Yarrow Logistics (cust_000703). Utilization just dropped from 65% to 15% overnight. 

**elena.volkov** — 9:05 AM
Whoa. That’s a cliff. Did they have a massive layoff or did their integration break?

**marco.silva** — 9:10 AM
I’m checking `fact_workflow_runs`. It looks like their main 'Order Sync' workflow is throwing AUTH_FAILED errors for the last 14 hours. 

**marco.silva** — 9:12 AM
Actually, checking `workflow_runs_daily` in BQ... yeah, `auth_failed_count` is 4,200 for today already. 

**elena.volkov** — 9:15 AM
Is this an Acme problem or a them problem?

**marco.silva** — 9:20 AM
Looks like they rotated their API keys in their ERP and forgot to update the Acme connection. I’m jumping on a call with their admin now. 

**marco.silva** — 10:45 AM
Resolved. They updated the keys. Utilization should bounce back by the 2h lag window in the warehouse. 

---

# #cs-at-risk — 2025-11-19 — Kestrel Networks Churn Post-Mortem

**marco.silva** — 4:00 PM
Sad news. Kestrel Networks (cust_000708) is officially churning at the end of the month.

**elena.volkov** — 4:02 PM
What happened? They were Business tier, $10k MRR, right?

**marco.silva** — 4:05 PM
Yeah. It was a budget cut. Tom and I did three demos for their new VP of Ops but they’ve been told to cut all "non-essential" SaaS by 20%. 

**tom.becker** — 4:08 PM
They loved the product, just couldn't justify the seat count. I tried to downsell them to Pro but they need the Audit Logs and SSO, and they won't pay the Business seat minimum ($149/seat for 50 seats) if they only have 20 users left.

**elena.volkov** — 4:10 PM
Did they show up on the at-risk reports?

**marco.silva** — 4:12 PM
They were 'monitoring' for a while because of the low utilization, but they never hit 'critical' because they were paying their invoices on time. 

**lina.cho** — 4:15 PM
This is what I keep saying—the health model doesn't see "budget risk" until the invoice fails. We need a way to track "champion sentiment" in the data.

**rajiv.menon** — 4:18 PM
@lina.cho That was supposed to be in VRS, but we haven't found a good proxy for it yet. Champion login recency maybe?

**lina.cho** — 4:20 PM
Maybe. But for Kestrel, the champion stayed, the budget just vanished.

---

# #cs-at-risk — 2025-12-05 — Sable Analytics Renewal

**marco.silva** — 10:00 AM
Working on the Sable Analytics (cust_000710) renewal for Jan. They're Business tier, 90 seats.

**sarah.chen** — 10:02 AM
They’re asking for a discount. Apparently Marigold Health told them they got a better deal on their Enterprise plan.

**marco.silva** — 10:05 AM
Ugh, Marigold is Enterprise and has 300 seats. The per-seat price is obviously lower. Sable is only 90 seats.

**sarah.chen** — 10:07 AM
I know, but they’re threatening to stay on the monthly Business rate instead of signing the annual. 

**elena.volkov** — 10:10 AM
Check their NPS. If they’re promoters, we hold firm. If they're detractors, we might have to bridge them.

**marco.silva** — 10:15 AM
Querying `fact_nps_responses`... they haven't responded to a survey since Q2 2024. 

**grace.liu** — 10:20 AM
That’s a risk signal in itself. No feedback is usually bad feedback.

---

# #cs-at-risk — 2026-01-12 — Tamarind Group Pause

**marco.silva** — 8:45 AM
Tamarind Group (cust_000706) just asked to pause their subscription for 3 months.

**elena.volkov** — 8:47 AM
We don't really have a "pause" button for Business tier. It’s either active or churned. 

**marco.silva** — 8:50 AM
Sarah said we should allow it because they're going through a merger and don't want to lose their workflow configurations. 

**lina.cho** — 8:55 AM
If we pause them, how does that affect ARR? @rajiv.menon 

**rajiv.menon** — 8:58 AM
If the status in `dim_customers` goes to 'paused', the ARR snapshot will treat them as $0 MRR for those months. It’ll look like churn in the NRR calc unless we specifically exclude 'paused' from the denominator. 

**lina.cho** — 9:00 AM
Don't exclude them. NRR should reflect reality. If they aren't paying, it's churned MRR until they come back.

**sarah.chen** — 9:05 AM
That's harsh. They're definitely coming back.

**elena.volkov** — 9:10 AM
We'll follow the finance rule. Pause = Churn for now. Marco, make sure they know their data is only kept for 90 days on a paused plan.

---

# #cs-at-risk — 2026-02-20 — Beacon Studios Aftermath

**elena.volkov** — 11:00 AM
I’m still reeling from Beacon Studios (cust_000287) churning. $116K ARR gone just like that. How did we not see this?

**olivia.tran** — 11:05 AM
I just looked at their `account_health` history. They were 'healthy_expansion' literally the day before they sent the notice. NPS was 9, utilization was 85%, 65 seats active.

**grace.liu** — 11:07 AM
I talked to their admin. It had nothing to do with us. Their parent company consolidated all automation onto a legacy contract they have with a competitor. 

**marco.silva** — 11:10 AM
This is the problem with the model. It’s all product signals. It doesn't catch parent-co consolidation or procurement-led changes.

**rajiv.menon** — 11:15 AM
We could pull `is_engaged` and `utilization_band` all day, but if a CFO at a holding company signs a global deal with someone else, we’re toast. 

**lina.cho** — 11:18 AM
We need a "Parent Company" field in `dim_customers`. If we knew they were owned by Beacon Media Group, we might have seen the risk across our other accounts too.

**david.kim** — 11:20 AM
I’ll add it to the backlog for the next sync, but getting that data clean is going to be a nightmare.

---

# #cs-at-risk — 2026-03-05 — Harbor Dynamics Seat Count

**marco.silva** — 3:15 PM
Flagging Harbor Dynamics (cust_000713). They just dropped from 150 seats to 60 seats on their renewal.

**elena.volkov** — 3:17 PM
That’s a huge downgrade. Why?

**marco.silva** — 3:20 PM
They realized they were over-provisioned. Only about 55 people were actually logging in. 

**marco.silva** — 3:22 PM
Looking at `acme.account_health`, their `utilization_band` was 0.38. For a Business tier account, that's not 'critical' (which is < 0.20), but it was definitely 'monitoring'. 

**olivia.tran** — 3:25 PM
This is why I tell my accounts to keep their seat count tight. Better to expand later than have a massive contraction at renewal. 

**tom.becker** — 3:30 PM
Counter-point: If they hadn't bought 150 seats, we wouldn't have hit our Q3 targets last year.

**elena.volkov** — 3:32 PM
And now we're paying for it with a $13k MRR hit. @tom.becker, let's try to keep the provisioning realistic.

---

# #cs-at-risk — 2026-04-10 — Quartz Foundry Uncollectible

**olivia.tran** — 9:00 AM
Quartz Foundry (cust_000714) just hit 'critical' health status. 

**lina.cho** — 9:05 AM
Yep, their last two invoices were marked uncollectible by Finance. 

**olivia.tran** — 9:08 AM
They’re an Enterprise account, $144k ARR. I can't get their billing lead on the phone. 

**elena.volkov** — 9:10 AM
If it's uncollectible, we need to look at service suspension. Are they still using the product?

**olivia.tran** — 9:15 AM
Checking `fact_workflow_runs`... yeah, they ran 50,000 workflows yesterday. They’re heavily integrated into their patient intake system. 

**elena.volkov** — 9:18 AM
If we cut them off, their intake system breaks?

**olivia.tran** — 9:20 AM
Completely.

**elena.volkov** — 9:22 AM
Okay, don't suspend yet. I’ll escalate to their VP. If they’re using it that much, they’ll find the money.

---

# #cs-at-risk — 2026-04-22 — NRR Calculation Questions

**marco.silva** — 11:00 AM
Hey @lina.cho — I’m looking at the NRR dashboard for my book. It seems lower than I expected. Does it count downgrades to Free as churn?

**lina.cho** — 11:05 AM
Yes. Any move to the Free tier is treated as a $0 end MRR for that customer in the cohort.

**marco.silva** — 11:08 AM
What about if they just reduce seats? 

**lina.cho** — 11:10 AM
That’s just contraction. It stays in the numerator, just at a lower value. 

**rajiv.menon** — 11:12 AM
Just make sure you’re looking at `nrr_trailing_12` table. And remember, the cohort is fixed from 12 months ago. If you had an account that was Business then and is Free now, they are $0 in the `cohort_end_mrr_usd` column. 

**marco.silva** — 11:15 AM
Got it. I think I was looking at a different view that was inner-joining the active customers.

**rajiv.menon** — 11:18 AM
Yeah, don't do that. Inner joining drops the churned customers and makes the NRR look way better than it actually is. Always use the canonical table: `nexus-analyst-demo.acme.nrr_trailing_12`. 

**lina.cho** — 11:20 AM
I’ve seen some people trying to query `acme.marts.cs.nrr`—that doesn't exist. Please stick to the flat dataset.

---

# #cs-at-risk — 2026-05-02 — Driftwood Media Expansion Risk

**grace.liu** — 2:00 PM
Driftwood Media (cust_000702) is technically 'healthy_expansion' but I’m worried.

**elena.volkov** — 2:02 PM
Why? The numbers look great for a Pro account.

**grace.liu** — 2:05 PM
They’re at 18 seats, which is almost $900 MRR. They should be on Business, but they refuse to move because of the 50-seat minimum. 

**grace.liu** — 2:07 PM
They told me if we force them to Business, they’ll switch to a cheaper tool. So they’re "stuck" on Pro.

**elena.volkov** — 2:10 PM
We've seen this before. They have Business-level usage but Pro-level pricing. 

**lina.cho** — 2:15 PM
We’re actually looking at a "Business Lite" plan for later this year to bridge that gap, but nothing's confirmed.

**grace.liu** — 2:18 PM
Well, for now, they’re staying on Pro. I’m just worried they’ll hit some Pro-tier quota limit and churn out of frustration.

**rajiv.menon** — 2:20 PM
They have 10k runs/mo on Pro. Are they close?

**grace.liu** — 2:22 PM
They hit 9,500 last month. 

**elena.volkov** — 2:25 PM
@grace.liu Give them a one-month quota waiver if they hit it. We don't want to lose them over 500 workflow runs.

---

# #cs-at-risk — 2026-05-04 — Quick Questions

**olivia.tran** — 10:00 AM
Is anyone else seeing weird numbers in `account_health` this morning? 

**david.kim** — 10:05 AM
The 8 AM refresh failed because of a schema change in the CRM source. I’m fixing it now. Data is about 4 hours stale.

**olivia.tran** — 10:07 AM
That explains why Verdant Cloud (cust_000707) is still showing as 'at_risk'. We closed their P1 last night.

**david.kim** — 10:10 AM
Yeah, wait for the noon refresh. 

**marco.silva** — 11:45 AM
Anyone want to grab Blue Bottle?

**grace.liu** — 11:46 AM
In.

**olivia.tran** — 11:47 AM
Same. See you at the elevators.

---

# #cs-at-risk — 2025-09-08 — Engagement Threshold Change

**rajiv.menon** — 10:15 AM
@here Reminder: We are officially changing the `is_engaged` definition in the `account_health` mart today. 
Old: >= 2 active users.
New: >= 3 active users. 
Expect a lot of accounts to flip from 'stable' to 'monitoring' this afternoon.

**marco.silva** — 10:20 AM
This is going to make my week look terrible in the status report.

**elena.volkov** — 10:22 AM
It’s better to be honest about the risk, Marco. Two users is just two people talking to each other. Three users is a team.

**grace.liu** — 10:25 AM
Does this affect the `utilization_band`?

**rajiv.menon** — 10:27 AM
No, `utilization_band` is still `active_users_28d / seat_count_licensed`. It just means the threshold for being considered "engaged" is higher.

**lina.cho** — 10:30 AM
Note: Enterprise accounts still have `utilization_band = NULL` because of the seat contract structure. Their engagement is just based on the raw active user count and run volume.

**olivia.tran** — 10:35 AM
Wait, so for Marigold (cust_000701), they have 300 seats but if only 5 people use it, are they "engaged"?

**rajiv.menon** — 10:38 AM
Technically yes, if they run >10 workflows. But that’s why we have the CSM to look at the *actual* depth of adoption. The data can only tell us so much.

---

# #cs-at-risk — 2025-10-30 — Kestrel Networks Budget Warning

**marco.silva** — 11:45 AM
Just got off a call with Kestrel Networks (cust_000708). Their main champion just got told that all "non-core" software is under review for the 2026 budget.

**elena.volkov** — 11:47 AM
What’s our status there?

**marco.silva** — 11:50 AM
They’re at 70 seats, Business tier. $10,430 MRR. 

**tom.becker** — 11:52 AM
I’m on it. I’m going to send over a deck showing their integration with their devtools stack. They’re running about 40k workflows a month—hard to call that "non-core".

**marco.silva** — 11:55 AM
The problem is the price. They think $149/seat is too high compared to some of the cheaper alternatives.

**elena.volkov** — 11:58 AM
Keep us posted. This would be a big hit for the MM (Mid-Market) segment NRR.

---

# #cs-at-risk — 2025-11-15 — Kestrel Update

**marco.silva** — 3:00 PM
Bad news on Kestrel. The budget cut was across the board. They’re churning on Dec 1st.

**elena.volkov** — 3:02 PM
Damn. 

**lina.cho** — 3:05 PM
I’ll mark them as churned in `dim_customers`. Marco, can you make sure the `loss_reason` is set to 'budget' in the CRM so it flows into the `fact_opportunities` table?

**marco.silva** — 3:10 PM
Will do.

---

# #cs-at-risk — 2025-12-18 — Sable Analytics Detractor

**marco.silva** — 9:45 AM
Sable Analytics (cust_000710) just dropped a 2 on an NPS survey. 

**elena.volkov** — 9:47 AM
Ouch. What was the comment?

**marco.silva** — 9:50 AM
"Support takes too long to respond to complex integration questions."

**grace.liu** — 9:52 AM
I just checked their tickets in `fact_support_tickets`. They have four open tickets right now, all related to the Snowflake connector. 

**rajiv.menon** — 9:55 AM
The Snowflake connector has been flaky lately. Engineering is working on a fix.

**marco.silva** — 10:00 AM
I’m reaching out to their admin now to try and smooth things over. They’re a Business tier account, EMEA region. Sarah Chen is the AE.

**sarah.chen** — 10:05 AM
I’m already on it, Marco. I’ve got a call with their head of data on Friday.

---

# #cs-at-risk — 2026-01-25 — Tamarind Group Pause Details

**marco.silva** — 1:30 PM
Update on Tamarind Group (cust_000706). They’ve officially paused as of today.

**lina.cho** — 1:35 PM
I see the update in the DB. They’re marked as 'paused' in `dim_customers`. 

**rajiv.menon** — 1:40 PM
Just a reminder for anyone doing reporting: the `arr_snapshot` table will show them as $0 MRR. If you’re calculating churn for Jan, they will be in the numerator. 

**elena.volkov** — 1:45 PM
Wait, if they're just paused, why are they in the churn numerator?

**lina.cho** — 1:48 PM
Because they aren't paying. From a finance perspective, it's a loss of revenue. If they come back in April, it'll show up as 'resurrection' or 'expansion' depending on how we track the subscription ID.

**rajiv.menon** — 1:50 PM
Actually, it’ll be 'reactivation' in the `fact_subscriptions.change_type` column.

---

# #cs-at-risk — 2026-03-12 — Onyx Robotics Expansion?

**olivia.tran** — 10:15 AM
Onyx Robotics (cust_000704) is asking about adding 200 more seats. 

**elena.volkov** — 10:17 AM
I thought they were at risk?

**olivia.tran** — 10:20 AM
They were, back in August when that P1 was open. But they’ve been 'healthy_expansion' for three months now. 

**tom.becker** — 10:22 AM
Yeah, I’m working on the expansion order now. It’ll move them from $35k MRR to about $48k MRR. 

**lina.cho** — 10:25 AM
That’s a nice win. That’ll help offset some of the Beacon Studios loss. 

**rajiv.menon** — 10:28 AM
@tom.becker, make sure you don't multiply the ACV by 12 when you enter it in the CRM. The `bookings_acv_usd` field in our attribution table is already annualized.

**tom.becker** — 10:30 AM
Got it. Already annualized. 

---

# #cs-at-risk — 2026-04-05 — Willow Works Utilization

**grace.liu** — 4:00 PM
Willow Works (cust_000709) utilization is at 105%. 

**elena.volkov** — 4:02 PM
How is that possible?

**grace.liu** — 4:05 PM
They have 25 seats licensed, but 26 users are showing as active in the last 28 days.

**rajiv.menon** — 4:10 PM
Ah, the "grace user" bug. Sometimes the system lets one extra person in if two people sign up at the exact same millisecond. 

**grace.liu** — 4:12 PM
They’re on Pro, LATAM region. I’ll ask them to add a few more seats. They’re clearly getting value.

**yuki.sato** — 4:15 PM
I’ll reach out to their billing admin. They usually just pay the overage, but it’s better to get them to just buy the seats.

---

# #cs-at-risk — 2026-04-28 — General Housekeeping

**elena.volkov** — 9:00 AM
Final push for the end of the month! Make sure all your at-risk accounts have updated notes in the CRM. I’m pulling the report for the Board on Monday.

**marco.silva** — 9:05 AM
Is Cobalt Systems still 'at_risk' or did we move them to 'monitoring'?

**elena.volkov** — 9:07 AM
They’re still 'at_risk' until that tool consolidation review is over. 

**lina.cho** — 9:10 AM
@marco.silva I just checked the BigQuery path for your status report—make sure you're using `nexus-analyst-demo.acme.account_health`. Don't use the old Looker explore, it hasn't been updated with the new Enterprise rules yet.

**marco.silva** — 9:12 AM
Thanks Lina. I was about to use the Looker one. 

**rajiv.menon** — 9:15 AM
Yeah, Looker is still lagging by about 2 hours anyway because of the PDT refresh cycle. BigQuery is the source of truth. 

**grace.liu** — 10:00 AM
Does anyone have a charger for a MacBook M3? Mine just died in the cafeteria.

**olivia.tran** — 10:02 AM
I have one at my desk, Grace. Help yourself.

# #cs-at-risk — 2026-04-29 — Tamarind Group Reactivation

**sarah.chen** — 11:15 AM
Great news on Tamarind Group (cust_000706). Their VP of Ops just emailed; the insurance restructuring is finished and they want to unpause. 

**marco.silva** — 11:18 AM
Nice! I’ll move them back to 'active' in the CRM. Do we need a new contract or just resume the existing Business tier terms?

**sarah.chen** — 11:20 AM
Just resume. They were only paused for 3 months, so the 55-seat minimum still holds. @lina.cho can you make sure Finance doesn't double-count the "reactivation" as new bookings?

**lina.cho** — 11:25 AM
I'll handle it. Since they were `status = 'paused'`, the logic in the `nrr_trailing_12` table will treat their return as expansion or flat depending on if they add seats. Just don't let the AE enter it as a new opportunity in the `fact_opportunities` table or the `bookings_attribution` will get messy.

**marco.silva** — 11:30 AM
Quick check: since they've been paused, their workflow runs are at zero. Is the `account_health` table going to flag them as 'critical' immediately?

**rajiv.menon** — 11:32 AM
It shouldn't hit 'critical' unless they have an uncollectible invoice. For a Business tier account like Tamarind, it'll likely show as 'monitoring' or 'at_risk' because they won't meet the "Engaged" definition (≥3 active users AND ≥10 runs) for the first 28-day window.

---

# #cs-at-risk — 2026-05-01 — Enterprise Health Nuance

**marco.silva** — 2:00 PM
Hey @rajiv.menon, I'm looking at Onyx Robotics (cust_000704) in `nexus-analyst-demo.acme.account_health`. They have zero active users in the last 14 days because of their internal security migration, but the status is still 'stable'. Shouldn't they be 'critical'?

**rajiv.menon** — 2:05 PM
Nope. Onyx is Enterprise. Remember the rules we pushed in Q4? For Enterprise, we don't trigger 'critical' based on utilization bands. Since they have unlimited seats/runs potentially, the utilization math is too noisy. 

**nina.patel** — 2:07 PM
Correct. Enterprise only goes to 'critical' if `has_uncollectible_recent` is true. Basically, if they stop paying.

**marco.silva** — 2:10 PM
That seems... risky? If an Enterprise client stops using the platform entirely, I want to know.

**elena.volkov** — 2:12 PM
That's why you're the CSM, Marco! The data helps us prioritize, but you should have your own pulse on the account. If they're at zero usage, you should manually flag them in the CRM. We didn't want the automated board reports showing 'critical' for every Enterprise client that does a batch migration once a quarter.

**marco.silva** — 2:15 PM
Got it. I'll stick to the manual 'at_risk' flag for now then. 

---

# #cs-at-risk — 2026-05-02 — Marigold Health NPS Detractor

**olivia.tran** — 9:45 AM
Ouch. Just got a 3/10 NPS response from the head of infra at Marigold Health (cust_000701). 

**elena.volkov** — 9:47 AM
What was the comment?

**olivia.tran** — 9:50 AM
"System latency during the APAC morning window is becoming a blocker for our regional teams. Support tickets take 4 hours to even get a first response."

**jasmine.park** — 9:52 AM
Wait, 4 hours? They’re on Enterprise. Priority support should be way faster than that.

**olivia.tran** — 9:55 AM
They opened the tickets via the generic web form instead of the Enterprise portal, so they didn't get routed to the priority queue. I'm fixing the routing on our end now, but the damage is done.

**sarah.chen** — 9:58 AM
@olivia.tran let’s get a call on the books for Monday. I don't want this snowballing into the renewal discussion. They’re at $180k ARR, we can’t lose them.

**rajiv.menon** — 10:05 AM
I'll check the `fact_workflow_runs` for Marigold. If they're seeing latency, it might show up in the `p95_duration_ms` column in `acme.workflow_runs_daily`.

---

# #general — 2026-05-02 — Food / Life

**tom.becker** — 12:15 PM
Is anyone going to the food truck park today? I heard the taco place is back.

**grace.liu** — 12:17 PM
I'm in. Meeting at the lobby at 12:30?

**omar.haddad** — 12:20 PM
Can't. I'm stuck on a discovery call with a prospect who thinks we're a CRM. 

**tom.becker** — 12:22 PM
Tell them we're the glue that *fixes* their CRM. 

---

# #cs-at-risk — 2026-05-03 — Beacon Studios Aftermath

**elena.volkov** — 11:00 AM
I’m reviewing the Churn report for April. Beacon Studios (cust_000287) is the big one. $116K ARR gone.

**marco.silva** — 11:05 AM
I still feel bad about that one, but there was nothing we could do. Their parent company forced a move to a legacy vendor they have a global master agreement with. 

**elena.volkov** — 11:07 AM
I know. I checked their `fact_nps_responses` before they left—they were at a 9. It’s a "clean" churn, just painful for the NRR.

**lina.cho** — 11:10 AM
Just a reminder for everyone looking at the board deck: our NRR is sitting at ~1.07 right now. Even with Beacon leaving, the expansion we saw at Onyx and Marigold earlier this year is keeping us above the 1.05 target. 

**rajiv.menon** — 11:12 AM
And just to be clear for the new folks: when you're looking at the `nrr_trailing_12` table, don't try to recalculate it by hand using `dim_customers`. That table uses a fixed cohort from 12 months ago. If you just join current customers, you'll miss the churns and get an inflated number. 

---

# #cs-at-risk — 2026-05-04 — Onyx P1 Escalation

**olivia.tran** — 8:30 AM
URGENT: Onyx Robotics (cust_000704) just hit a massive spike in `INTEGRATION_DOWN` errors. Looks like the Jira connector is failing for their entire instance.

**priya.anand** — 8:35 AM
On it. Checking the logs now.

**olivia.tran** — 8:40 AM
They have a 99.9% SLA on their Enterprise plan. This has been down for 45 minutes already. 

**david.kim** — 8:45 AM
It’s not just them. I’m seeing `AUTH_FAILED` across several APAC accounts. Might be a credential refresh bug in the latest dbt deploy. 

**elena.volkov** — 8:50 AM
@olivia.tran keep the customer updated every 15 mins. This is going to trigger an 'at_risk' flag in `account_health` because the P1 will definitely be open for more than an hour, even if we fix it soon.

**rajiv.menon** — 8:55 AM
Wait, the `at_risk` rule is for P1s open over 48 hours. If Priya fixes it this morning, it won't trigger the automated health flag. But it'll definitely show up in the `fact_support_tickets` CSAT later.

---

# #cs-at-risk — 2026-05-04 — Final Board Prep

**lina.cho** — 4:00 PM
Final check on the numbers before I lock the dashboard for the board meeting. 
Total ARR: ~$39M
Business: ~$32M
Enterprise: ~$6M
Pro: ~$1M

**rachel.stein** — 4:05 PM
Wait, why does my old Looker bookmark say $42M?

**lina.cho** — 4:07 PM
@rachel.stein that Looker explore has a stale PDT refresh. It was double-counting some of the multi-year Enterprise deals that we haven't actually started the service period for yet. The `nexus-analyst-demo.acme.arr_snapshot` table is the source of truth. It only counts active subscriptions.

**rachel.stein** — 4:10 PM
Okay, I'll delete that bookmark. $39M it is.

**rajiv.menon** — 4:12 PM
Also, just a heads up—I noticed someone was trying to query `vrs_band` again. Please don't use that. The Value Realization Score is still a draft spec and the data in those columns is just null or placeholder. Stick to `is_engaged` for now.

**elena.volkov** — 4:15 PM
Thanks Rajiv. Okay team, great work this month. Let’s hope the board likes the NRR story. Even with the Beacon churn, 1.07 is solid for our Series B stage.

**marco.silva** — 4:20 PM
Anyone seen my blue notebook? I think I left it in the boardroom.

**grace.liu** — 4:22 PM
I saw it near the coffee machine, Marco. 

---

**yuki.sato** — 5:00 PM
OOO starting tomorrow for a week. Heading to Japan! @grace.liu is covering my Pro accounts. If anything Enterprise-level comes in for my region, please ping Tom.

**tom.becker** — 5:02 PM
Have a great trip Yuki! Bring back some snacks.

---

# #cs-at-risk — 2026-06-12 — Tamarind Reactivation?

**tom.becker** — 10:15 AM
Heads up—I just got a ping from Sarah in Sales. Tamarind Group (customer_id: 552) wants to "explore a potential return." They churned back in '24 because of the workflow quota limits on the old Pro plan. 

**elena.volkov** — 10:18 AM
Wait, didn't they have a massive billing dispute on the way out? @rachel.stein do you remember?

**rachel.stein** — 10:22 AM
Yeah, they refused to pay the final true-up invoice for overages. It was a mess. If they come back, they need to be on the Business tier minimum—no more "unlimited" legacy Pro nonsense.

**rajiv.menon** — 10:25 AM
I'm looking at their historicals in `nexus-analyst-demo.acme.fact_workflow_runs`. Before they churned, they were hitting 150k runs/month. If we put them on Business, they’ll hit the 100k quota in week 3 every month. They have to be an Enterprise lead or it's going to be another support nightmare.

**olivia.tran** — 10:30 AM
Agreed. @tom.becker please tell Sarah that CS won't sign off on a reactivation unless it's a signed Enterprise contract with custom quotas. We can't have them blowing up the P1 queue again because their "mission critical" syncs stopped at midnight.

**tom.becker** — 10:35 AM
Copy that. I'll relay. Also, is the coffee machine on floor 4 broken again? It’s just dispensing lukewarm water.

**marco.silva** — 10:36 AM
Facility-ticket it, Tom. I'm busy debugging why the `dim_customers` table shows 45 churned but my manual count is 46. 

---

# #cs-at-risk — 2026-06-28 — Q2 Midnight Madness

**lina.cho** — 9:00 AM
Final week of the quarter! Let's stay on top of any 'at_risk' flags. I see a new one for "Velocity Lab" (customer_id: 110). @grace.liu that's yours right?

**grace.liu** — 9:05 AM
Yeah. They had a -100 NPS detractor comment yesterday. Something about "UI latency making the platform unusable for their ops team." I've got a call with their champion at 11am PT.

**rajiv.menon** — 9:10 AM
@grace.liu check `nexus-analyst-demo.acme.fact_user_events`. Filter for `event_type = 'page_load_slow'` for their domain. I suspect it's just that one massive dashboard they built with 50+ nested loops. It's not the platform, it's their logic.

**grace.liu** — 9:12 AM
Thanks Rajiv, that gives me some ammo for the call. 

**olivia.tran** — 11:45 AM
Quick update on Velocity: Grace is right, it was a logic issue. But they are still annoyed. We might need to offer a month of "Professional Services" credit to help them optimize. @elena.volkov you okay with that to save the renewal?

**elena.volkov** — 11:50 AM
If it saves a $60k Business account, yes. Use the standard PS voucher.

**marco.silva** — 12:00 PM
Lunch? I’m hitting the poke place.

**tom.becker** — 12:01 PM
In. 
**olivia.tran** — 12:01 PM
Can't, stuck in a QBR. Bring me a spicy tuna? 

---

# #cs-at-risk — 2026-07-15 — Health Score Logic

**yuki.sato** — 2:15 PM
Back from Japan! Thanks for covering, Grace. 
Question: I'm looking at `nexus-analyst-demo.acme.account_health` and I see 'Global Corp' has an `is_engaged` flag of 0, even though their `seat_count_licensed` is 500. Is the warehouse broken?

**rajiv.menon** — 2:20 PM
Welcome back! Not broken. The `is_engaged` logic requires at least 20% of licensed seats to have a `last_login_date` within the last 14 days. Global Corp only has 15 active users right now. They bought 500 seats for a rollout that hasn't happened yet.

**yuki.sato** — 2:25 PM
Ugh, that's going to look terrible on the monthly report. Can we exclude them? 

**lina.cho** — 2:27 PM
No exclusions in the raw tables. If you want to filter them out for a presentation, use the `current_plan_tier != 'Enterprise'` filter or just explain the "implementation lag" to the board. 

**rajiv.menon** — 2:30 PM
Actually, @lina.cho, maybe we should add a `health_override` column to `dim_customers`? For cases like this where we know they're "healthy" but just slow to deploy.

**lina.cho** — 2:32 PM
No way. That’s how we end up with the Beacon situation again where everyone thought the account was fine because of a manual override while the actual usage was tanking. Data is data. If they aren't using the seats, they are at risk of a downsell.

**elena.volkov** — 2:40 PM
Lina's right. If they paid for 500 and only 15 are in there, that's a massive downsell risk at the 12-month mark. Yuki, get on a call with their IT lead and see why the rollout stalled.

---

# #cs-at-risk — 2026-07-22 — Beacon Echoes

**tom.becker** — 4:00 PM
Found another one. "Solaris Data" (customer_id: 89) has the exact same usage pattern as Beacon did three months before they bailed. 
Look at `nexus-analyst-demo.acme.fact_workflow_runs`:
May: 80k runs
June: 45k runs
July (so far): 12k runs

**olivia.tran** — 4:05 PM
Checked the support logs. No P1s, but a lot of "How do I export my workflow definitions?" tickets.

**rajiv.menon** — 4:07 PM
Red alert. Exporting definitions is the #1 leading indicator for migration to a competitor. 

**elena.volkov** — 4:10 PM
@tom.becker who is the AE on Solaris? 

**tom.becker** — 4:12 PM
It was Mark, but he left in April. It's unassigned in CRM right now, technically falling under "House."

**elena.volkov** — 4:15 PM
Typical. Okay, I’m taking this one. I’ll reach out to their VP. We can’t lose another $100k account this quarter. 

**grace.liu** — 4:20 PM
Wait, isn't Solaris part of the same parent company as Tamarind? 

**rajiv.menon** — 4:22 PM
Just checked `dim_customers`. Email domains don't match, but the `industry` is the same (Renewable Energy). I’ll check the `invited_by_user_id` chains in `dim_users` to see if there's a connection.

**rajiv.menon** — 4:35 PM
Found it. The CTO of Solaris was the Director of Ops at Tamarind during their "refusal to pay" phase. 

**elena.volkov** — 4:38 PM
Wonderful. This is going to be a fun conversation. 

---

# #cs-at-risk — 2026-08-02 — Summer Slump

**marco.silva** — 10:00 AM
Is anyone else seeing a drop in `fact_user_events` across the board? Total events are down 15% WoW.

**lina.cho** — 10:05 AM
It's August, Marco. Everyone in EMEA is OOO. Check the `region` breakdown in BigQuery:
`SELECT region, count(*) FROM nexus-analyst-demo.acme.fact_user_events WHERE event_at > '2026-07-25' GROUP BY 1`

**marco.silva** — 10:10 AM
Ah, yeah. EMEA is down 40%. North America is flat. False alarm. 

**olivia.tran** — 10:15 AM
Speaking of OOO, I'm off Friday for a wedding. @rajiv.menon is my backup for anything technical. 

**rajiv.menon** — 10:16 AM
Only if you bring back a piece of cake. 

**olivia.tran** — 10:17 AM
It's a destination wedding in Mexico, the cake won't survive the flight. I'll bring tequila.

**rajiv.menon** — 10:18 AM
Accepted.

---

# #cs-at-risk — 2025-10-14 — Beacon Aftermath

**grace.liu** — 9:15 AM
I’m looking at the usage recovery for the Enterprise accounts after the Beacon outage last week. Apex Global is still significantly below their baseline. 

**rajiv.menon** — 9:22 AM
Running the numbers now.
`SELECT customer_id, count(*) FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE status = 'failed' AND triggered_at BETWEEN '2025-10-05' AND '2025-10-10' GROUP BY 1 ORDER BY 2 DESC`

**rajiv.menon** — 9:25 AM
Yeah, Apex had over 4,000 failures during the window. Their retry logic actually hit our rate limits once we came back online. 

**grace.liu** — 9:28 AM
Great. Their VP of Eng just sent a very "unhappy" email to Elena. They're demanding a credit for the entire Q4. 

**elena.volkov** — 9:35 AM
@grace.liu I saw it. Don't promise the full quarter yet. Check the SLA in `dim_plans`. For Enterprise, it’s 99.9%. We only dipped to 98.2% for the month. We owe them a 10% credit max according to the MSA.

**grace.liu** — 9:40 AM
They don't care about the MSA right now, Elena. They had a production line stop for 4 hours because the warehouse-sync workflow died. 

**marco.silva** — 9:45 AM
Side note—is the coffee machine on the 4th floor broken again? It’s leaking. 

**olivia.tran** — 9:46 AM
@marco.silva Put a ticket in with Ops. This channel is for at-risk customers, not at-risk caffeine levels.

**marco.silva** — 9:47 AM
Caffeine levels are a leading indicator for my productivity. It's a P0.

---

# #cs-at-risk — 2025-11-20 — Enterprise Health Logic

**lina.cho** — 2:10 PM
@rajiv.menon can you clarify how the 'Health Score' in the dashboard is calculated for the `account_tier = 'Enterprise'` segment? I have Sterling Dynamics showing as 'Green' but their seat utilization is only 40%.

**rajiv.menon** — 2:15 PM
The legacy V1 health score was 70% weighted on `fact_workflow_runs` volume and only 30% on seats. I haven't updated it since the Series B. 

**lina.cho** — 2:18 PM
We need to fix that. `dim_customers` shows Sterling is paying for 500 seats but only has 200 users in `dim_users` who have logged in during the last 30 days. That’s a massive contraction risk for their February renewal.

**rajiv.menon** — 2:30 PM
I’ll update the view. New logic proposal:
- 40% Seat Utilization (`dim_users` active / `dim_customers.seat_count_licensed`)
- 40% Workflow Success Rate (`fact_workflow_runs` success vs fail)
- 20% Support Ticket Volume (inverse)

**elena.volkov** — 2:45 PM
@rajiv.menon Add a 50% "manual override" for CSM sentiment. I don't care if the usage is high; if the champion leaves, the account is red. 

**rajiv.menon** — 2:50 PM
Copy that. I'll build it into the `fact_customer_health_snapshots` table tonight.

---

# #cs-at-risk — 2026-01-12 — Tamarind Ghosting

**tom.becker** — 11:05 AM
Heads up, I’m seeing some activity on the Tamarind Group account. Someone with an `@tamarind-industries.com` domain just signed up for a Free trial.

**elena.volkov** — 11:10 AM
Are you kidding? They still owe us $14k from their 2024 "billing dispute." 

**tom.becker** — 11:12 AM
It looks like a different department. "Tamarind Solar." 

**rajiv.menon** — 11:15 AM
I just checked the `invited_by_user_id` in `dim_users`. This new user wasn't invited by anyone. It’s a cold organic signup through the website. 

**elena.volkov** — 11:20 AM
Flag the account in CRM immediately. I want a hard block on any Pro/Business upgrades until they settle the outstanding invoices from the parent company. @lina.cho can you pull the invoice history for any entity with "Tamarind" in the name?

**lina.cho** — 11:25 AM
`SELECT * FROM nexus-analyst-demo.acme.fact_invoices WHERE status = 'unpaid' AND customer_id IN (SELECT customer_id FROM nexus-analyst-demo.acme.dim_customers WHERE company_name LIKE '%Tamarind%')`

**lina.cho** — 11:28 AM
Yep. $14,200 across three invoices. All from late 2024. 

**elena.volkov** — 11:30 AM
Perfect. Tom, if they reach out for a demo, tell them we’d love to chat once they talk to their AP department. 

---

# #cs-at-risk — 2026-03-05 — Utilization Cliff

**marco.silva** — 3:00 PM
Something is wrong with BlueGrid Systems. Look at this:
`SELECT date, count(*) FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE customer_id = 'c_8821' AND date > '2026-02-01' GROUP BY 1`
They went from 5k runs a day to zero on Tuesday. 

**olivia.tran** — 3:05 PM
I just checked the error logs. They didn't stop using us; their API key for the "Core-Warehouse-Sync" was deleted by a user named `admin_temp`. 

**marco.silva** — 3:10 PM
Do we know who `admin_temp` is? 

**rajiv.menon** — 3:15 PM
Checking `dim_users`. `user_id = 'u_9912'`. Signed up 4 days ago. Role is 'Developer'. 

**elena.volkov** — 3:20 PM
Wait, BlueGrid is in the middle of a "security audit." I bet they’re rotating keys and someone nuked the production one by mistake. Marco, call their CTO. Don't email, call. If they’re down for 24 hours they’re going to blame us for "unreliability" even if it was their fault.

**marco.silva** — 3:45 PM
Update: Called them. It was a new hire who thought they were in the staging environment. They’re back up. CTO was grateful we caught it before their nightly batch run. Crisis averted.

**olivia.tran** — 3:46 PM
Can we get them to move to OAuth so they stop messing with raw keys?

**marco.silva** — 3:47 PM
I've been trying for six months. They "don't have the dev cycles." Typical.

---

# #cs-at-risk — 2026-04-18 — Random / OOO

**grace.liu** — 9:00 AM
I’m out starting tomorrow for a long weekend in Tahoe. 

**elena.volkov** — 9:05 AM
Enjoy! Who's covering the QBR for Northern Star?

**grace.liu** — 9:07 AM
Marco is covering, but honestly, they might cancel. Their main contact is on parental leave. 

**marco.silva** — 9:10 AM
I’ll handle the reschedule if they don’t show. @rajiv.menon did you ever fix that bug in the `dim_dates` table where it was marking some holidays as business days? 

**rajiv.menon** — 9:12 AM
Fixed it last week in the dbt repo. Should be clean in the next refresh. 

**marco.silva** — 9:15 AM
Cool. Also, has anyone seen my blue water bottle? I think I left it in the kitchen.

**olivia.tran** — 9:17 AM
It's next to the leaking coffee machine. It’s now a "caution" sign.

---

# #cs-at-risk — 2026-04-20 — Enterprise Health Rules

**elena.volkov** — 10:15 AM
Can someone point me to the updated logic for the "At Risk" flag in the Gainsight dashboard? I’m looking at `c_1102` (Global Logistics Corp) and they are flagged red, but their MRR is $12k and they haven't missed a payment. 

**rajiv.menon** — 10:22 AM
The red flag is likely the "20% Utilization Drop" rule we pushed last month. Check `nexus-analyst-demo.acme.fact_workflow_runs`. 
`SELECT customer_id, count(*) as runs FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE customer_id = 'c_1102' AND triggered_at > '2026-04-01' GROUP BY 1`
Compare that to their March average. They dropped from 45k runs/week to under 30k. 

**elena.volkov** — 10:25 AM
Got it. It’s the seasonal shipping lull, but the automated trigger doesn't know that. I'll override it manually so we don't freak out the VP of Sales. 

**marco.silva** — 10:30 AM
Speaking of overrides, did we ever decide on the rule for "Ghost Accounts"? We have about 15 Business tier customers with 0 runs in the last 14 days. 

**grace.liu** — 10:35 AM
If they have 0 runs and they're in their first 90 days, it's an Onboarding Fail. If they're older than 90 days, it's a Churn Risk. @olivia.tran can we get a Looker alert for that? 

**olivia.tran** — 10:40 AM
On it. I’ll add a join to `dim_customers` to pull the `signup_date` so we can segment the alerts. 

---

# #cs-at-risk — 2026-04-22 — Tamarind Group Reactivation

**marco.silva** — 2:00 PM
Huge news: Tamarind Group (`c_4412`) wants to come back. They churned in Nov 2025 because of the "Beacon" outage instability, but they’ve been miserable with the competitor. 

**elena.volkov** — 2:05 PM
Are they asking for the old pricing? Because we’ve increased the Enterprise floor since then. 

**marco.silva** — 2:10 PM
They’re pushing for the 2025 rate. They also want a "stability guarantee" in the SLA. 

**rajiv.menon** — 2:15 PM
We can't do a custom SLA for a $60k ACV. The legal overhead alone kills the margin. 

**marco.silva** — 2:18 PM
I know, I know. I’m trying to bridge it. They have 400 users ready to provision immediately. @grace.liu, any chance you can jump on a call with their Head of Ops? They need some "executive love."

**grace.liu** — 2:25 PM
I can do Thursday at 4 PM PT. But tell them straight up: the product is 10x more stable now, but the price is the price. We don't discount for "past trauma" anymore. 

**olivia.tran** — 2:30 PM
Also, someone should check if their old workspace is still in the soft-delete bucket. If it's gone, they have to rebuild all their connectors. 

---

# #cs-at-risk — 2026-04-25 — NPS Detractor Alert

**system** — 9:01 AM
**New NPS Response: 2/10 (Detractor)**
**Customer:** Summit Peak (`c_2291`)
**User:** `u_7731` (Director of IT)
**Comment:** "The new UI update is a nightmare. Our team spends more time trying to find the 'Save' button than actually building workflows. If this isn't fixed, we aren't renewing in July."

**elena.volkov** — 9:15 AM
Ouch. Summit Peak is a $200k account. Who's the CSM?

**marco.silva** — 9:17 AM
That's mine. They’ve been complaining about the "Canvas 2.0" rollout for three weeks. I thought the feedback was just standard "change is hard" grumbling, but a 2/10 from a Director is a P1. 

**olivia.tran** — 9:20 AM
The 'Save' button is actually an auto-save now, which is why they can't find it. We need to send them the enablement video.

**marco.silva** — 9:22 AM
I sent it. They hate auto-save. They want a manual commit lock because they have multiple people editing the same workflow and they keep overwriting each other. 

**rajiv.menon** — 9:25 AM
Wait, are they hitting the collision error code `ERR_409_CONFLICT`? I see a spike in that for `customer_id = 'c_2291'` in `fact_workflow_runs`. 

**marco.silva** — 9:28 AM
Yes! Exactly. They have a "too many cooks" problem. I’m going to schedule a deep dive with Product. If we lose Summit Peak, my Q2 numbers are toast.

---

# #cs-at-risk — 2026-04-28 — General / Random

**grace.liu** — 8:45 AM
Quick heads up, the office fridge is being cleaned out at 4 PM today. Anything without a name is going in the bin. 

**olivia.tran** — 8:50 AM
Does that include the sourdough starter in the Mason jar? Because that’s mine and it’s alive. 

**elena.volkov** — 8:52 AM
Olivia, please don't keep biological experiments in the communal fridge. 

**rajiv.menon** — 11:00 AM
Does anyone know why the `dim_customers` table is showing `current_mrr_usd` as NULL for all the new Amsterdam-based accounts? 

**olivia.tran** — 11:05 AM
Currency conversion bug in the pipeline. It’s looking for a `EUR` to `USD` rate in the `fact_fx_rates` table but it only has data up to 2026-04-01. I’m fixing the scraper now. 

**marco.silva** — 11:15 AM
Is anyone going to the "Modern Data Stack" happy hour tomorrow? I have two extra invites. 

**grace.liu** — 11:20 AM
Only if they aren't serving those weird vegan sliders again. 

**elena.volkov** — 1:45 PM
Back to business: BlueGrid (`c_8821`) just opened another 5 tickets in 2 hours. All related to "Webhook latency." @rajiv.menon is there a lag in the US-East-1 cluster? 

**rajiv.menon** — 1:50 PM
Checking the health dashboard... looks green. Wait, I see it. A "noisy neighbor" on the same shard is slamming the API. It’s `c_9901` (RocketScale). I’ll throttle them. 

**elena.volkov** — 1:55 PM
Good catch. Tell BlueGrid we’re "optimizing their node." Don't mention the throttling of another customer. It makes them nervous about their own limits.

---

# #cs-at-risk — 2026-02-14 — Renewal / Health Rules

**marco.silva** — 9:05 AM
Happy Valentine's Day everyone. My gift to the team is a massive red flag on Horizon Logistics (`c_5542`). Their Enterprise renewal is coming up in June, and their `workflow_run_count` in `nexus-analyst-demo.acme.fact_workflow_runs` has plummeted by 60% since the start of the year. 

**elena.volkov** — 9:12 AM
Is this related to the "Beacon" outage back in November? I remember their VP of Eng being particularly vocal about the data loss on their custom webhooks.

**marco.silva** — 9:15 AM
Probably. They haven't touched the `workflow_editor` in three weeks. @rajiv.menon can you check if they've been hitting any specific error codes? 

**rajiv.menon** — 10:30 AM
Checking... they aren't even triggering runs enough to get errors. Their `fact_user_events` shows only 2 active users out of 250 licensed seats. That’s a ghost town. 

**grace.liu** — 10:45 AM
Side note: Can we PLEASE finalize the "Enterprise Health Score" logic? Product is saying one thing, and the data in `nexus-analyst-demo.acme.dim_customers` says another. If `current_mrr_usd` > $10k but utilization < 10%, that should be an automatic P0 alert. 

**elena.volkov** — 10:50 AM
Agreed. Right now the "at risk" flag is too manual. I’m tired of finding out a customer is leaving when the `status` changes to 'CHURNED' in the warehouse. 

---

# #cs-at-risk — 2026-03-10 — P1 Escalation / Tamarind Group

**marco.silva** — 2:15 PM
Huge update: Tamarind Group (`c_0034`) just reached out via their old AE. They want a "reactivation consultation." 

**olivia.tran** — 2:18 PM
Wait, the Tamarind Group that churned after Beacon? The "never-again-Acme" Tamarind? 

**marco.silva** — 2:20 PM
The very same. Apparently, their move to the competitor (no names, but it rhymes with 'Schmapier') has been a disaster for their high-volume batch processing. They miss our concurrency limits. 

**rajiv.menon** — 2:25 PM
If we bring them back, we need to move them to a dedicated shard immediately. I don't want them getting noisy-neighbored again. Check `nexus-analyst-demo.acme.fact_workflow_runs` for their 2025 peak loads—we need to match that capacity. 

**elena.volkov** — 2:30 PM
@marco.silva make sure they sign a multi-year deal. We spent way too much time on their post-mortem last year to let them back on a month-to-month Business plan. 

**grace.liu** — 3:00 PM
Is anyone else’s Zoom acting up? I’ve been kicked out of three "Tamarind Prep" meetings today. 

**olivia.tran** — 3:05 PM
It’s the office Wi-Fi. Someone is probably downloading a local copy of `fact_user_events` again. DON'T DO THAT. Query it in the console. 

---

# #cs-at-risk — 2026-04-12 — NPS / General

**elena.volkov** — 11:00 AM
Just got an NPS detractor (Score: 2) from Silver Oak (`c_1109`). Comment: "The UI is so slow it’s faster to write the Python scripts myself." 

**marco.silva** — 11:05 AM
That’s weird, Silver Oak is usually one of our happiest accounts. Who is the user? 

**elena.volkov** — 11:08 AM
It’s a new Lead Dev. Looking at `nexus-analyst-demo.acme.dim_users`, they signed up last week. Probably didn't get the onboarding walkthrough. 

**rajiv.menon** — 11:15 AM
Actually, I see a latency spike for their region in the logs. They’re based in Singapore but their `customer_id` is mapped to the `US-West-2` cluster in `dim_customers`. That’s a 200ms round trip just for the heartbeat. 

**olivia.tran** — 11:20 AM
Why are they in the US cluster? Did they sign up via a VPN? 

**marco.silva** — 11:22 AM
Likely. I’ll reach out and offer to migrate their tenant to the APAC instance. That should fix the NPS issue. 

**grace.liu** — 12:00 PM
Reminder: The "Spring Clean" is tomorrow. If you have old monitors at your desk that don't work, put them in the hallway. 

**rajiv.menon** — 12:05 PM
Does that include the broken espresso machine? 

**grace.liu** — 12:10 PM
Rajiv, the espresso machine is a sacred relic. Do not touch it. 

**marco.silva** — 4:00 PM
Back on Silver Oak—I just checked the `fact_subscriptions` table. They actually upgraded to Enterprise last month? Why is the NPS so low if they just committed to $75k ARR? 

**olivia.tran** — 4:10 PM
Check the `changed_from_subscription_id`. It looks like an automated "overage upgrade." They might not even know they're on Enterprise yet. They hit the run limit on Business and the contract auto-flexed. 

**elena.volkov** — 4:15 PM
Yikes. That's a "surprise bill" conversation waiting to happen. Marco, you better get ahead of that before Finance sends the invoice. 

**marco.silva** — 4:20 PM
On it. I'm going OOO until Monday (long weekend!), but I'll send the email tonight. If BlueGrid (`c_8821`) breaks anything else while I'm gone, just tell them I'm "researching their architectural constraints." 

**grace.liu** — 4:25 PM
"Architectural constraints." I'm stealing that for the next time the kitchen runs out of oat milk.

**grace.liu** — 4:45 PM
Wait, if Marco is OOO, who is covering the BlueGrid (`c_8821`) sync on Tuesday? They’re still seeing 403 errors on their custom webhook triggers.

**elena.volkov** — 4:50 PM
I can jump in, but I need a quick primer on their setup. Are they still using that janky middle-layer for Auth0? 

**rajiv.menon** — 5:02 PM
Yes. It’s a mess. If you look at `nexus-analyst-demo.acme.fact_workflow_runs`, filter by `customer_id = 'c_8821'` and look for `error_code = 'ERR_AUTH_EXPIRED'`. It’s happening every 3600 seconds on the dot. Their token refresh logic is failing, but they keep blaming our ingest layer. 

**olivia.tran** — 5:15 PM
I'll add it to the "at-risk" tracker. Speaking of which, can someone tell me where we landed on the Enterprise health rules? I’m trying to build a dashboard in Sigma but the logic in `dim_customers` for `account_tier = 'Enterprise'` doesn't seem to account for seat utilization. 

**elena.volkov** — 5:20 PM
The current "V2 Health Score" is: 
1. `seat_count_licensed` / `active_users` (from `dim_users`) > 80%
2. `fact_workflow_runs` volume hasn't dropped > 20% WoW
3. No P1 tickets in the last 14 days. 
I have the draft SQL in my scratchpad if you want it. It joins `dim_customers` to a subquery on `fact_workflow_runs`. 

**olivia.tran** — 5:22 PM
Yes, please. I need to see why **Tamarind Group** (`c_4412`) is showing as "Green" when they haven't logged in since the Beacon outage. 

**rajiv.menon** — 5:25 PM
Tamarind is a special case. They "paused" their contract after Beacon (March 2026) but kept the SSO bridge active. Our current health query probably thinks they’re active because the system user is still "running" heartbeat workflows. 

**marco.silva** — 5:30 PM (from my phone, about to log off!)
Tamarind is my priority for June reactivation. They didn't churn, they just went "dark" to evaluate competitors. I heard through the grapevine they looked at Tray and realized they'd have to rewrite 400+ scripts. They'll be back. 

**grace.liu** — 5:35 PM
Marco, stop checking Slack! Go enjoy the long weekend. 

---
**MONDAY, May 11, 2025**

**olivia.tran** — 9:15 AM
Morning everyone. Starting the week with a P1. **Solaris Analytics** (`c_9901`) is reporting that all their scheduled triggers are firing 2 hours late. 

**rajiv.menon** — 9:20 AM
Let me check the worker queues. Looking at `nexus-analyst-demo.acme.fact_workflow_runs` for the last 4 hours... 
Wait, `triggered_at` vs `actual_start_time` (oh wait, we don't have that in the flat table). I'm seeing a massive backlog in the `US-East-1` cluster. 

**elena.volkov** — 9:25 AM
Is this related to the "Spring Clean"? Did someone unplug a server rack in the basement to plug in a vacuum? 

**grace.liu** — 9:28 AM
The servers aren't in the basement, Elena. They're in the cloud. And no, the office cleaning was on Saturday. 

**rajiv.menon** — 9:35 AM
Found it. It’s a "runaway workflow" from a Pro-tier account that bypassed the rate limit. `u_5521` at **QuickFix Solutions** (`c_2218`) accidentally created a recursive loop. 1.2M runs in 30 minutes. 

**olivia.tran** — 9:40 AM
A Pro account taking down the queue for a Business account? We need to fix the multi-tenancy isolation. Solaris is paying us $12k/mo and they're getting throttled by a $49/seat user. 

**elena.volkov** — 9:45 AM
I’ll pull the usage data. We should probably bill QuickFix for the overage too. `nexus-analyst-demo.acme.fact_invoices` is going to look wild for them this month if the automated billing kicks in. 

**rajiv.menon** — 10:00 AM
Killed the QuickFix process. Queues should clear in 15 mins. Olivia, you might want to send a "we're sorry" note to Solaris. 

**olivia.tran** — 10:15 AM
Already on it. I’m also seeing a 1/10 NPS from **Omni Logistics** (`c_7761`). 
Comment: "The UI update last week moved the 'Save' button. I lost three hours of work because I thought it auto-saved. I hate everything." 

**elena.volkov** — 10:20 AM
Oof. "I hate everything" is a mood. 

**rajiv.menon** — 10:22 AM
To be fair, the new UI is confusing. Why did Design hide the 'Deploy' toggle under a hamburger menu? 

**grace.liu** — 11:00 AM
Lunch is here. Tacos from The Alchemist. Please don't eat them over your keyboards, I'm still cleaning up salsa from last Friday. 

**olivia.tran** — 1:30 PM
Back to business—Tamarind Group just reached out to Marco's alias. They want to talk "reactivation" but they're asking for a 40% discount to compensate for the Beacon downtime. 

**elena.volkov** — 1:35 PM
40%? That would put their MRR below the Business tier floor. I just checked `fact_subscriptions`, they were at $4,500/mo. A 40% cut puts them at $2,700. Finance will never approve that for a company with 200+ users. 

**rajiv.menon** — 1:40 PM
Tell them we can't do 40% on the seat price, but we can give them "Unlimited Runs" for 6 months for free. It costs us almost nothing in compute but looks like a huge value add on paper. 

**olivia.tran** — 1:45 PM
Good idea. I'll draft the proposal for Marco to see when he's back. 

**elena.volkov** — 2:00 PM
Is anyone else seeing weirdness in `dim_customers`? I see 5 new accounts created this morning with the `acquisition_channel` as 'NULL'. 

**grace.liu** — 2:05 PM
The Marketing team was messing with the UTM parameters on the signup page again. They probably broke the tracking script. 

**rajiv.menon** — 2:10 PM
Of course they did. I'll go tell them. Again. 

**olivia.tran** — 3:00 PM
Update on **NexaFlow** (`c_6612`): They’re escalating to a P0. Their Salesforce integration is dropping 1 in 5 leads. I looked at `fact_workflow_runs` and I'm seeing `error_code = 'SFDC_LIMIT_EXCEEDED'`. 

**elena.volkov** — 3:05 PM
That's not our fault. That means their Salesforce instance is out of API calls. 

**olivia.tran** — 3:10 PM
They don't care. They think Acme should "queue the requests better." 

**rajiv.menon** — 3:15 PM
Tell them to upgrade to the Enterprise version of our SFDC connector. It has the "Smart Queueing" logic. 

**olivia.tran** — 3:18 PM
They *are* an Enterprise customer. 

**rajiv.menon** — 3:20 PM
Oh. Then... tell them I'm "researching their architectural constraints." 

**elena.volkov** — 3:21 PM
You're using Marco's line! 

**rajiv.menon** — 3:22 PM
It's a good line! 

**grace.liu** — 4:00 PM
Reminder: The company-wide All Hands is at 4:30. Don't be late, the CEO is announcing the Q3 goals. 

**rajiv.menon** — 4:05 PM
Predictions? 
1. "Synergy" 
2. "AI-driven workflows" 
3. "We need to lower our AWS bill" 

**elena.volkov** — 4:06 PM
I'm betting on "AI-driven synergy to lower our AWS bill." 

**olivia.tran** — 4:07 PM
I just want them to fix the espresso machine. 

**grace.liu** — 4:10 PM
The repair guy is coming on Wednesday. Until then, use the instant coffee in the back of the pantry. 

**rajiv.menon** — 4:11 PM
Instant coffee? I'd rather drink the water from the cooling loop.

**#cs-at-risk**

**olivia.tran** — Nov 12, 2025 9:15 AM
Hey team, getting pings from the former champion at **Tamarind Group** (`c_9114`). They churned back in August because of the "Beacon" data latency issues, but apparently their new provider (Tray) is "too complex" for their Ops team. They want to talk reactivation. 

**grace.liu** — 9:20 AM
Wait, Tamarind? Didn't they leave a nasty NPS comment about our "instability"? 

**olivia.tran** — 9:22 AM
Yeah, a '2' on the NPS scale. But the champion moved to a different department and the new Head of Ops used Acme at his last gig. 

**rajiv.menon** — 9:25 AM
If we bring them back, can we please ensure they don't run those 50-step recursive loops again? That’s what killed their performance during Beacon. I’m looking at `nexus-analyst-demo.acme.fact_workflow_runs` from July and their `duration_ms` was averaging 45 seconds per run. 

**elena.volkov** — 9:30 AM
I can set a hard timeout on their `customer_id` specifically if we put them on the new Enterprise infra. 

**olivia.tran** — 9:35 AM
They’re asking for a discount to "make up for the previous experience." Marco, what’s the stance on "reactivation credits"? 

**marco.chen** — 10:00 AM (OOO - Amsterdam)
No credits. Give them 2 months of "White Glove Implementation" instead. It costs us less (just my/your time) and ensures they don't break the recursive loops again. 

---

**grace.liu** — Dec 05, 2025 11:45 AM
@elena.volkov I’m trying to build the Q1 Health Dashboard. What are the actual "Enterprise Health Rules" we settled on? I'm looking at `nexus-analyst-demo.acme.dim_customers` and trying to join with workflow success rates.

**elena.volkov** — 11:50 AM
The current logic in the `mart_customer_health` model is:
1. `utilization_rate` (runs / quota) > 60%
2. `error_rate` (fact_workflow_runs status='error') < 5%
3. `active_user_ratio` (active_users / licensed_seats) > 40%
4. No P1 tickets in last 30 days.

If any of those fail, they go to "Yellow." If two fail, they're "Red." 

**grace.liu** — 11:55 AM
If that's the case, **CloudScale** (`c_5582`) is deep in the Red. Their `active_user_ratio` is like 12%. They bought 500 seats but I only see 60 people logging in. 

**olivia.tran** — 12:00 PM
CloudScale is a classic "overbuy." The procurement head wanted the Enterprise discount so they bought 500 seats to hit the tier, even though they only have 100 people in the whole Engineering org. We need to watch them at renewal (March 2026). They’ll try to downsell to Business. 

---

**rajiv.menon** — Jan 14, 2026 2:10 PM
**Urgently** need someone from CS to look at **OrbitSystems** (`c_1033`). They just sent an NPS '1' with the comment: "System is a black hole. Workflows disappear."

**olivia.tran** — 2:15 PM
On it. Checking their logs now. 

**elena.volkov** — 2:20 PM
I see it. `nexus-analyst-demo.acme.fact_workflow_runs`. They have a bunch of runs with `error_code = 'AUTH_TOKEN_EXPIRED'`. It looks like their Global Admin deleted the service account they were using for all their Slack integrations. 

**olivia.tran** — 2:25 PM
So it's a "them" problem, not an "us" problem? 

**rajiv.menon** — 2:26 PM
Technically yes, but the UI didn't bubble up the auth error clearly enough. It just showed "Failed" without the specific reason on the dashboard. 

**olivia.tran** — 2:30 PM
Okay, I'll call their VP of IT. He's usually chill, but he's under pressure since the Q4 numbers were soft. 

---

**grace.liu** — Feb 02, 2026 10:00 AM
**Loomis & Co** (`c_3341`) utilization just dropped off a cliff. 
Last week: 85,000 runs.
This week: 4,000 runs. 

**elena.volkov** — 10:05 AM
Did they change their `current_plan_tier`? 

**grace.liu** — 10:06 AM
No, still on Enterprise. `mrr_usd` is still $12,500. 

**rajiv.menon** — 10:10 AM
I’m looking at `fact_user_events`. Their main workflow builder, `dave.l@loomis.com`, hasn't logged in for 10 days. 

**olivia.tran** — 10:12 AM
Check LinkedIn... Oh boy. Dave just started a new job at a competitor. He was the only one who knew how to maintain their main ERP sync. 

**grace.liu** — 10:15 AM
This is why we push for "Center of Excellence" training. Single point of failure is killing our retention. 

**olivia.tran** — 10:20 AM
I'll reach out to their Director of IT. We need to get someone else trained before the whole thing breaks and they blame the platform. 

---

**rajiv.menon** — Feb 15, 2026 4:00 PM
Is the snack bar out of the spicy almonds again? 

**grace.liu** — 4:02 PM
Supply chain issues. Use the walnuts. 

**rajiv.menon** — 4:03 PM
Walnuts are just depressed almonds. 

**elena.volkov** — 4:05 PM
Can we focus? **Aura Healthcare** (`c_7721`) is threatening to churn if we don't sign their new BAA (Business Associate Agreement) by Friday. 

**olivia.tran** — 4:07 PM
Legal has had that for three weeks. I’ll go stand outside Sarah’s office until she signs it. 

**grace.liu** — 4:10 PM
Tell her I'll trade her my stash of spicy almonds for the signature. 

**olivia.tran** — 4:12 PM
Deal. 

---

**elena.volkov** — March 10, 2026 11:00 AM
Hey @channel, did something change in how we calculate `seat_count_licensed` in `dim_customers`? I’m seeing a mismatch between the fact tables and the dim table for several MM accounts.

**grace.liu** — 11:05 AM
The Finance team updated the logic last night to include "pending" seats from signed-but-not-yet-provisioned contracts. It’s to help the AEs with their commission tracking. 

**elena.volkov** — 11:10 AM
That's going to mess up the utilization ratios. If we have 100 seats "licensed" but they can't actually log in yet, our `active_user_ratio` is going to tank. 

**rajiv.menon** — 11:15 AM
Great. Another day of cleaning up the data warehouse because Sales wanted a shortcut. I'll be in the cooling loop if anyone needs me. 

**olivia.tran** — 11:20 AM
Wait, don't go. I need help with **VeloSync** (`c_4431`). They’re seeing `error_code = 'RATE_LIMIT_EXCEEDED'` on the Acme API itself. They’re hitting the 5k/min limit. 

**rajiv.menon** — 11:22 AM
Are they on Business or Enterprise? 

**olivia.tran** — 11:23 AM
Business. 

**rajiv.menon** — 11:25 AM
Tell them that's the limit for Business. If they want 10k/min, they need to talk to their AE about the Enterprise upgrade. 

**olivia.tran** — 11:26 AM
They just upgraded last month! 

**rajiv.menon** — 11:28 AM
Check `dim_customers.current_plan_tier`. 

**olivia.tran** — 11:30 AM
...It still says 'Business'. @grace.liu why wasn't this updated? 

**grace.liu** — 11:32 AM
The Salesforce-to-Stripe sync failed on Feb 28th. I’ve been trying to fix the manual overrides all morning. 

**olivia.tran** — 11:35 AM
I have a very angry CTO on the phone. Can we *please* just manually flip the flag in the DB for `c_4431`? 

**rajiv.menon** — 11:36 AM
On it. Don't tell Audit. 

---

**marco.chen** — March 25, 2026 2:00 PM
Back from Amsterdam. Why is the #cs-at-risk channel 200+ unread messages? 

**olivia.tran** — 2:02 PM
Welcome back. We're out of spicy almonds and the data is a lie. How was the stroopwafel?

**marco.chen** — March 26, 2026 9:15 AM
Stroopwafels were excellent, but I’d trade them all for a working dashboard. 
Anyway, diving into the **Tamarind Group** (`c_8821`) situation. They’re still showing "At Risk" in the Health Score V2 model. Is this still the lingering "Beacon" fallout, or is it something new? 

**olivia.tran** — 9:20 AM
It’s the reactivation lag. We gave them 3 months of service credits after the Beacon outage in January, but they haven't ramped their workflow volume back up. If you look at `nexus-analyst-demo.acme.fact_workflow_runs`, their `step_count` is down 60% compared to Q4. 

**sarah.jenkins** — 9:25 AM
I spoke with their Head of Ops yesterday. They moved their mission-critical syncs to a competitor during the outage and haven't moved them back yet. They’re "testing our stability." 

**marco.chen** — 9:28 AM
Great. Another Enterprise account on the brink. @rajiv.menon can we get a specific query for Tamarind's error rates over the last 14 days? I want to show them how much better our latency is now. 

**rajiv.menon** — 9:30 AM
Sure, but the `error_code` column is a mess since the v3 API rollout. Half of the 'SUCCESS' runs are actually timing out at the gateway. I'll see what I can pull from the raw logs. 

---

**grace.liu** — April 2, 2026 10:05 AM
**NPS Alert** 🚨 
Just got a 2/10 from the CTO of **Global Logistics Corp** (`c_5512`). 
Comment: "The platform is powerful but the data consistency between the UI and the API is non-existent. Our billing reports never match our internal usage logs."

**marcus.thorne** — 10:12 AM
That’s a $250k ACV account. Who is the CSM? 

**olivia.tran** — 10:14 AM
That would be me. And the CTO is right. We’ve been over-billing them because `fact_invoices` is pulling from `dim_customers.seat_count_licensed` while they think they’re on a usage-based kicker. 

**elena.volkov** — 10:18 AM
We keep telling Sales not to write "usage-based kickers" into the PDF contracts if they aren't supported in the billing engine yet. Grace, can we manually adjust `c_5512` for the April cycle? 

**grace.liu** — 10:20 AM
I can, but it’s going to show up as a "Negative Expansion" in the board deck. Marcus is not going to like how that looks for the MM segment. 

**marcus.thorne** — 10:22 AM
I'd rather have a "negative expansion" than a churn. Fix it. 

---

**sophia.wu** — April 10, 2026 3:45 PM
Hey everyone, quick OOO note: I’ll be offline starting Friday for my sister's wedding. Back on the 20th. For any **BlueStream** (`c_9904`) escalations, please ping @marco.chen. 

**marco.chen** — 3:47 PM
Wait, isn't BlueStream's renewal on the 15th? 

**sophia.wu** — 3:48 PM
Yes, but they’re green! 90% utilization, NPS of 9. No issues. 

**rajiv.menon** — 3:50 PM
Actually... I was just looking at `nexus-analyst-demo.acme.fact_user_events`. BlueStream’s `active_user_ratio` dropped from 0.85 to 0.12 on Monday. 

**olivia.tran** — 3:52 PM
Wait, what? 

**rajiv.menon** — 3:55 PM
Looks like they offboarded 40 people in one day. Might be a layoff or they're moving off the platform. 

**sophia.wu** — 3:56 PM
Ugh, okay. I’ll call my contact before I head out. This is why I hate the health scores. How did they stay "Green" if 80% of their users stopped logging in? 

**elena.volkov** — 3:58 PM
The health score model only refreshes on Sundays. It doesn't catch mid-week drops until the next batch run. 

---

**grace.liu** — April 15, 2026 11:00 AM
Does anyone know why the snacks in the SF micro-kitchen are 90% dried mango now? Did we switch vendors? 

**rajiv.menon** — 11:05 AM
Budget cuts for "Non-Essential Perks" started this morning. Apparently, the spicy almonds were too expensive. 

**olivia.tran** — 11:06 AM
First they take my data accuracy, now they take my almonds. 

---

**marco.chen** — April 22, 2026 1:15 PM
Can someone explain the Enterprise health rules one more time? I'm looking at **Nexus Point** (`c_1102`). They have 300 licensed seats, but only 10 users have logged in this month. Why are they not in #cs-at-risk? 

**elena.volkov** — 1:20 PM
Check `nexus-analyst-demo.acme.dim_customers`. What's the `acquisition_channel`? 

**marco.chen** — 1:22 PM
It says `PARTNER_REFERRAL`. 

**elena.volkov** — 1:24 PM
There's a hard-coded exclusion in the dbt model for partner-managed accounts. They don't hit the "At Risk" flag because the partner is technically responsible for engagement. 

**marco.chen** — 1:26 PM
That is the dumbest thing I’ve ever heard. If they churn, it still hits our ARR. 

**elena.volkov** — 1:28 PM
Take it up with the RevOps team. They didn't want the CSMs "harassing" partner accounts. 

---

**sarah.jenkins** — May 1, 2026 9:00 AM
Is the API down for anyone else? I'm trying to demo the new Salesforce-Slack connector to a prospect and I'm getting a 504. 

**rajiv.menon** — 9:05 AM
It's not down, but we're seeing massive lag on the `fact_workflow_runs` ingestion. The queue is backed up by 45 minutes. 

**olivia.tran** — 9:07 AM
Is this because of the **CyberDyne** (`c_7721`) bulk import? They said they were going to migrate 50,000 workflows this weekend. 

**rajiv.menon** — 9:10 AM
Wait, they started it *today*? It’s Friday! 

**sarah.jenkins** — 9:12 AM
I'm literally in the middle of a demo. This is embarrassing. 

**marcus.thorne** — 9:15 AM
@rajiv.menon kill the CyberDyne process. We can’t let one customer tank the whole production environment for a migration. Tell them to do it at 2 AM on a Sunday. 

**rajiv.menon** — 9:18 AM
I can't "kill" it easily. It's already distributed across the worker nodes. I have to manually throttle the `customer_id = 'c_7721'`. 

---

**olivia.tran** — May 4, 2026 10:30 AM
Checking the Monday morning status. 
`dim_customers` refresh completed. 
Total Active MRR: $39.2M (Business is carrying us right now).
We have 12 renewals this week. 
**Tamarind Group** (`c_8821`) is still yellow. 
**VeloSync** (`c_4431`) is officially Enterprise now (thanks @rajiv.menon for the manual flip). 

**marco.chen** — 10:35 AM
I'm seeing a weird spike in the `error_code` column for the `Pro` tier. Is anyone else seeing `UNAUTHORIZED_ACCESS` errors across multiple accounts? 

**elena.volkov** — 10:40 AM
Looking at the `fact_user_events`. It's only hitting users who signed up in the last 48 hours. I think the SSO-by-default update for new Pro accounts might be broken. 

**rajiv.menon** — 10:42 AM
Verified. The `is_active` flag in `dim_users` isn't being set to TRUE for anyone using the Google Auth flow. 

**olivia.tran** — 10:45 AM
Cool. So our "seamless" onboarding is currently a brick wall. Putting it in the #incident-room.

**sarah.jenkins** — May 4, 2026 11:15 AM
Is anyone from the CS team around for a quick sync on the Tamarind Group (`c_8821`) account? I just got an NPS response from their Head of Ops and it’s a 2. "Unreliable infrastructure during critical month-end close." 

**olivia.tran** — 11:18 AM
That’s definitely fallout from the Beacon outage. They were one of the hardest hit because they have those high-frequency webhooks hitting the `fact_workflow_runs` table every 5 seconds. 

**marcus.thorne** — 11:20 AM
We need to get ahead of this. Tamarind is $120k ARR. If they churn, that’s a huge hole in the Q2 retention numbers. @sarah.jenkins can we offer them a credit for the downtime? 

**sarah.jenkins** — 11:22 AM
I'm trying, but their champion isn't responding to my emails. Does anyone have a contact for their VP of Engineering? 

**rajiv.menon** — 11:25 AM
Check the `dim_users` table for anyone with a `role` of 'Admin' who has logged in since the outage. I see `j.rathbone@tamarind.com` was active this morning at 8:45 AM. 

---

**lisa.wong** — May 5, 2026 2:30 PM
Quick OOO: I'll be offline for the rest of the afternoon for a dentist appointment. Back online tomorrow morning. For anything urgent regarding the **Stellaris** (`c_5592`) renewal, ping @marcus.thorne.

**marcus.thorne** — 2:35 PM
Got it. Also, does anyone know where we keep the updated Enterprise Health Score logic? 

**marco.chen** — 2:38 PM
It’s in the `nexus-analyst-demo.acme.dim_customers` view. Look for the `health_score_binary` column. It’s calculated based on:
1. `fact_workflow_runs` > 1000 in the last 30 days.
2. `fact_user_events` for at least 3 distinct users in the last 7 days.
3. No open P1 tickets in Zendesk.

**marcus.thorne** — 2:42 PM
Wait, why are we only looking for 3 distinct users for Enterprise? Some of these accounts have 500 seats licensed in `dim_customers`. If only 3 people are using it, that’s a massive contraction risk. 

**olivia.tran** — 2:45 PM
I've been saying this for months. We need to update the `dim_plans` logic to include a "Utilization %" metric. Licensed seats vs. active users from `fact_user_events`.

---

**#incident-room**
**system-bot** — May 6, 2026 4:12 PM
[P1] High Error Rate Detected: `UNAUTHORIZED_ACCESS` 
Customer Impact: 12% of total requests.
Affected Table: `nexus-analyst-demo.acme.fact_workflow_runs`

**elena.volkov** — 4:15 PM
I’m seeing this too. It looks like the fix I pushed for the Google Auth flow didn't propagate to the EMEA region nodes. 

**rajiv.menon** — 4:18 PM
I’m looking at the logs. It's hitting **VeloSync** (`c_4431`) specifically. They just upgraded to Enterprise and it looks like their custom SAML config is conflicting with the new SSO-by-default logic. 

**olivia.tran** — 4:20 PM
Great. We just flipped them to Enterprise and now they can’t run workflows. This is going to look great in the `fact_subscriptions` change log. "Upgrade to Enterprise: Benefit — No one can log in."

**elena.volkov** — 4:25 PM
Rolling back the SSO-by-default flag for `c_4431` now. 

---

**marcus.thorne** — May 7, 2026 9:00 AM
Does anyone have the link to the Q3 headcount planning doc? I can't find it in the shared drive. 

**sarah.jenkins** — 9:05 AM
I think it’s in the "Finance-Confidential" folder. You might need to ask **david.peters** for access. 

**marcus.thorne** — 9:10 AM
Anyway, we need to talk about **OmniCorp** (`c_1102`). Their `current_mrr_usd` is $15,000, but they haven't had a single successful run in `fact_workflow_runs` for 10 days. 

**rajiv.menon** — 9:15 AM
I checked the `error_code` column for them. It’s all `CREDENTIAL_EXPIRED`. Looks like their Salesforce refresh token died and nobody bothered to update it. 

**sarah.jenkins** — 9:18 AM
That’s a classic "silent churn" signal. If they aren't using the Salesforce connector, they aren't using Acme. I'll reach out to their admin, but I'm putting them on the #cs-at-risk list for the Monday meeting. 

**olivia.tran** — 9:20 AM
Added. `c_1102` is now "Red" in the tracker. 

---

**rajiv.menon** — May 8, 2026 11:45 AM
Did anyone order lunch? The Thai place downstairs says there's a 2-hour wait. 

**marco.chen** — 11:48 AM
We’re doing a group order for the Eng team at 12:15. Link is in the #internal-social channel. 

**marco.chen** — 11:50 AM
By the way, I just finished the backfill for the `fact_invoices` table. We had about 200 rows with a `null` value for `paid_at` even though the payment cleared through Stripe. 

**olivia.tran** — 11:52 AM
Thank god. Finance was breathing down my neck about the "phantom" AR. Does it match the `mrr_usd` in `fact_subscriptions` now?

**marco.chen** — 11:55 AM
Mostly. There’s still a $4,000 discrepancy for **CyberDyne** (`c_7721`) because of that weird pro-rated credit we gave them after the bulk import fiasco last week. 

**rajiv.menon** — 11:58 AM
Don't even mention CyberDyne. I'm still cleaning up the `fact_workflow_runs` table from their 50k migration attempt. I had to delete 4,000 "pending" rows manually. 

---

**sarah.jenkins** — May 11, 2026 10:15 AM
Good news on **Tamarind Group** (`c_8821`). I finally got them on a call. They aren't churning, but they want to downgrade to the Business tier because they don't feel the "Enterprise support" was there during the Beacon incident. 

**marcus.thorne** — 10:20 AM
That’s better than a churn, but it’s still a $40k hit to our Net Revenue Retention (NRR). Can we offer them a dedicated Slack channel instead? 

**sarah.jenkins** — 10:25 AM
I tried. They’re firm. I’ll process the `change_type = 'downgrade'` in the `fact_subscriptions` table for their next billing cycle on June 1st. 

**olivia.tran** — 10:30 AM
Updating the forecast now. We’re still on track for $40M ARR by EOY, but it's getting tight. We need the **VeloSync** (`c_4431`) expansion to land. 

**rajiv.menon** — 10:35 AM
VeloSync is looking good. Their `step_count` per workflow has increased 3x since they went Enterprise. They’re building some seriously complex stuff. 

**marcus.thorne** — 10:40 AM
Check the `fact_user_events`. I want to see if their new VP is actually using the dashboard or if it’s just the same three devs.

**rajiv.menon** — 10:45 AM
I’m looking at `nexus-analyst-demo.acme.fact_user_events` for **VeloSync** (`c_4431`) now. It’s not just the devs. Their VP of Ops, `d.vance@velosync.io`, has logged in 14 times in the last 7 days. Mostly looking at the `run_analytics` dashboard. That’s a massive signal for the renewal. 

**marcus.thorne** — 10:48 AM
Huge. If the VP is in there, they’re looking for ROI data to justify the seat expansion. @sarah.jenkins make sure that "Step Efficiency" report is clean for them.

**sarah.jenkins** — 10:50 AM
On it. Quick side note: I’m OOO this afternoon starting at 1 PM for my daughter’s piano recital. If anything catches fire with **Tamarind Group** (`c_8821`), please ping @elara.vance. 

**elara.vance** — 10:52 AM
Wait, I thought I was covering for **Globex** (`c_2209`) while Peter is in EMEA? My calendar is a nightmare. 

**marcus.thorne** — 10:55 AM
Peter’s back Friday. Elara, just keep an eye on Tamarind’s `fact_workflow_runs`. If their `error_code` count spikes again like it did during Beacon, they might skip the downgrade and just walk. 

---

**marco.chen** — May 12, 2026 9:15 AM
Has anyone looked at the **Health Score v2** logic in Looker? **BlueStar Logistics** (`c_5542`) is showing up as "Green" (Score: 88) but their `seat_utilization` in `dim_customers` is only 12%. 

**olivia.tran** — 9:18 AM
That’s because the health rule currently weighs `workflow_run_volume` at 60% and `is_active` users at only 10%. They have one "super user" who built a bot that runs every 5 minutes, which is padding the numbers. 

**rajiv.menon** — 9:22 AM
We need to fix that. One person running 50k workflows shouldn't mask 200 idle seats. I’ll update the `fact_daily_usage` rollup to include a `unique_active_users` threshold. 

**sarah.jenkins** — 9:25 AM
Please do. I just got a P1 escalation from **Skyline Systems** (`c_1102`). They’re saying their webhooks are timing out. 

**rajiv.menon** — 9:28 AM
Checking the logs... `nexus-analyst-demo.acme.fact_workflow_runs`. Yeah, I see a bunch of `status = 'failed'` with `error_code = '504_GATEWAY_TIMEOUT'`. It’s only affecting their Slack-to-Jira integration. 

**sarah.jenkins** — 9:30 AM
Skyline is already an NPS detractor (score 3) because of the Beacon outage. If we don’t resolve this in the next hour, they’re going to demand a credit. 

**marcus.thorne** — 9:35 AM
@olivia.tran what’s our current "Credit Pool" balance for Q2? We’ve been handing them out like candy since March. 

**olivia.tran** — 9:40 AM
We’ve already issued $112k in credits. Finance set the cap at $150k for the quarter. We have very little room if another major account goes sideways. 

---

**elara.vance** — May 13, 2026 11:10 AM
Lunch today? I’m starving. 

**marco.chen** — 11:12 AM
Can’t. Dealing with a `null` constraint issue in `dim_users`. Someone at **CyberDyne** (`c_7721`) tried to bulk-invite 500 users via the API without `email_domain` fields. It’s breaking the join to `dim_customers`. 

**rajiv.menon** — 11:15 AM
Again? I told their admin they need to use the SSO mapping. 

**sarah.jenkins** — 11:20 AM
Ugh, **Tamarind Group** just reached back out. Now they’re complaining about the `fact_invoices` from April. They claim they were overcharged for 10 seats that were "deactivated but still billed." 

**olivia.tran** — 11:24 AM
I’ll check `fact_subscriptions`. If they didn't reduce the `seat_count` in the UI, our billing engine won't pick it up. We don't auto-downgrade based on activity—that's in the MSA. 

**sarah.jenkins** — 11:26 AM
Try telling that to their CTO. He’s looking for any excuse to cut the bill. I’m going to need a CSV export of all `last_login_date` for their users from `dim_users` to prove those seats were technically "available."

**marcus.thorne** — 11:30 AM
Send it, but be polite. We need to save the $120k that's left on that contract. 

---

**rajiv.menon** — May 14, 2026 2:00 PM
Heads up: I’m running a heavy backfill on `nexus-analyst-demo.acme.fact_user_events` to fix the `event_type` mapping from the legacy `segment_events` table. Query performance might be a bit sluggish for the next 20 mins. 

**marco.chen** — 2:05 PM
Copy that. I was wondering why my `count(*)` was taking 45 seconds. 

**sarah.jenkins** — 2:10 PM
While you're in there, can you see if **VeloSync** has touched the "New Workflow Designer" (event: `designer_v2_load`)? I want to mention it in our QBR tomorrow. 

**rajiv.menon** — 2:15 PM
Checking... yep. 42 events for `designer_v2_load` in the last 48 hours. Mostly from `admin_user_99`. 

**marcus.thorne** — 2:20 PM
Perfect. That’s our wedge. If they like the new designer, we can push them toward the "Advanced Automation" add-on. That’s an extra $12/seat. 

**elara.vance** — 2:25 PM
Wait, did we ever announce the price increase for the add-on? I thought that was still in beta. 

**marcus.thorne** — 2:28 PM
It’s "Early Access" for Enterprise customers. Price is TBD but I'm anchoring at $12. 

**sarah.jenkins** — 2:30 PM
Good luck with that. **Tamarind** won't even pay for the seats they have. 

**olivia.tran** — 2:35 PM
Don't forget the All-Hands is at 3:00. Link is in the invite. Expect questions about the $40M ARR target. 

**marco.chen** — 2:40 PM
I’ll be there. Just finishing this `coalesce` on the `churn_date` field. Why are there so many rows with `churn_date` in the future? 

**olivia.tran** — 2:42 PM
Those are scheduled churns (end of contract). We track them in `dim_customers` to keep the forecast accurate. Don't touch them!

**sarah.jenkins** — May 14, 2026 3:45 PM
That All-Hands was... intense. $40M by EOY feels like a stretch if we don't fix the churn leak in the Enterprise segment. 

**marcus.thorne** — 3:48 PM
We have the pipeline. We just need to close. Sarah, what’s the latest on the **Tamarind Group** reactivation? I saw they had some activity in `fact_user_events` this morning.

**rajiv.menon** — 3:52 PM
Wait, let me check the logs. `SELECT count(*) FROM nexus-analyst-demo.acme.fact_user_events WHERE customer_id = 'CUST-7721' AND event_at > '2026-05-14 00:00:00'`... 
Yeah, I see 114 events. Looks like they’re testing the `webhook_inbound_received` trigger again. 

**sarah.jenkins** — 3:55 PM
They’re "evaluating." The CTO is still sour about the Beacon outage last month. I told him we’ve hardened the infrastructure, but he wants to see the uptime report from `dim_plans` vs actuals for the last 90 days before he signs a new $200k contract.

**elara.vance** — 4:00 PM
If anyone needs me, I'm OOO for a dental appointment. Back at 5:30. Also, did anyone see the NPS comment from **CloudScale**? It’s a 2/10. "UI is slower than a snail in peanut butter." 

**marco.chen** — 4:05 PM
That’s likely because they’re running 500+ concurrent workflows on the old `Pro` runner. They need to be on `Business` or `Enterprise` for the dedicated concurrency pool. 

**marcus.thorne** — 4:08 PM
@sarah.jenkins Can you use that as leverage? "We'll upgrade your runner performance if you move to the $149/seat tier."

**sarah.jenkins** — 4:10 PM
I’ll try, but CloudScale is already at 85 seats. If I push them to Business, their bill jumps from ~$4k to over $12k. They’re going to want a discount. 

---

**olivia.tran** — May 15, 2026 9:15 AM
**@channel** Reminder to update your "Account Health" scores in the CRM by EOD Friday. Finance is pulling the Q3 forecast on Monday.

**marco.chen** — 9:20 AM
Are we still using the "Beacon Score" or are we moving to the new SQL-based health rules Rajiv built? 

**rajiv.menon** — 9:22 AM
Move to the new rules. The old Beacon Score was based on `last_login_date` which is garbage for API-heavy users. The new `health_score` in `nexus-analyst-demo.acme.dim_customers` uses a weighted average of `workflow_success_rate` and `seat_utilization_pct`. 

**elara.vance** — 9:25 AM
Wait, if we use `workflow_success_rate`, doesn't that penalize customers who have shitty internal APIs? Like **VeloSync**? Their success rate is 40% because their own server keeps 504ing. 

**rajiv.menon** — 9:28 AM
Valid point. I can add a filter for `error_code` to exclude 5xx errors from the health calc if the `triggered_by` is an external webhook. I'll look at `fact_workflow_runs` to see if I can isolate those. 

**sarah.jenkins** — 9:35 AM
Speaking of **VeloSync**, they just dropped a P1 ticket. "Designer V2 is freezing on complex maps." Marco, is this related to the backfill Rajiv was doing? 

**marco.chen** — 9:38 AM
Unlikely. The backfill was on the `fact_user_events` table for reporting, it shouldn't touch the production state. But I'll check the `duration_ms` on their recent `designer_v2_load` events. 

---

**marcus.thorne** — May 15, 2026 11:00 AM
Just got off a call with the **Tamarind** procurement team. They’re offering $150k flat for 300 seats. That’s a massive discount off our Enterprise floor. 

**olivia.tran** — 11:05 AM
That’s below the $50k minimum ACV per 250 seats if we stick to the $149 list price. Marcus, you’re killing our margins. 

**marcus.thorne** — 11:07 AM
It’s $150k we don't have right now, Olivia. And they’re a "lighthouse" account for the Fintech vertical. If we get them back, **Apex Ledger** and **Zenith Pay** will follow. 

**sarah.jenkins** — 11:10 AM
I’m looking at their usage in `nexus-analyst-demo.acme.fact_workflow_runs`. Even when they were "active," they only used about 20% of their seat capacity. If we give them 300 seats for $150k, we need a "use it or lose it" clause on the discount for the next renewal. 

**rajiv.menon** — 11:12 AM
I can set up an automated alert for you. If `seat_utilization_pct` in `dim_customers` drops below 15% for 3 consecutive weeks, it pings the CSM. 

**sarah.jenkins** — 11:15 AM
That would be a lifesaver. Right now I'm just manually checking BigQuery once a month and it’s a soul-crushing experience. 

**marco.chen** — 11:18 AM
Hey, who deleted the `stg_legacy_billing` table in the sandbox? I was using that for the Tamarind historical audit. 

**olivia.tran** — 11:20 AM
Probably automated cleanup. Any table not touched in 60 days gets nuked to save on storage costs. Check the `nexus-analyst-demo.acme.dim_dates` for when the last snapshot was taken; you might be able to recover it from a partition. 

**marco.chen** — 11:22 AM
Ugh. Fine. By the way, Sarah, tell VeloSync the Designer V2 issue is fixed. It was a CSS conflict with their browser-side ad-blocker. Not our bug.

**sarah.jenkins** — 11:24 AM
Bless you. One less P1 to deal with before the weekend. Anyone want to grab a beer at South Park after 5? 

**marcus.thorne** — 11:26 AM
I’m in. But first, Sarah, send me that utilization report. I want to shove it in the Tamarind CTO's face before the beer. 

**sarah.jenkins** — 11:30 AM
`SELECT * FROM nexus-analyst-demo.acme.dim_customers WHERE company_name = 'Tamarind Group'`... coming your way. Just don't actually use the word "shove" in the email. 

---

**rajiv.menon** — May 15, 2026 1:00 PM
Found a weird anomaly. There’s a customer `CUST-9999` in `dim_customers` with `current_mrr_usd` of $0 but `current_plan_tier` is `Enterprise`. 

**olivia.tran** — 1:05 PM
That’s a test account for the Legal team. They use it to verify the "Audit Log" export functionality for SOC2 compliance. Just ignore it. 

**marco.chen** — 1:10 PM
Can we add an `is_test` flag to `dim_customers`? It’s messing up the aggregate MRR queries for the dashboards. 

**rajiv.menon** — 1:15 PM
Adding it to the dbt backlog. Should be live by Monday. I'll also add a `region` check because I’m seeing some `NULL` values for the EMEA accounts. 

**elara.vance** — 1:20 PM
Back from the dentist. My face is numb, but I just saw a Slack from the CEO. He wants the "Logo Churn" report for the Board meeting. Sarah, you have the list of "at-risk" logos for May? 

**sarah.jenkins** — 1:25 PM
Working on it. **VeloSync** is "Yellow," **Tamarind** is "Reactivation Candidate," and **DataFlow Systems** is "Red" because their champion just left for a competitor. I need to find a new contact there. 

**marcus.thorne** — 1:30 PM
DataFlow is a goner. I heard they’re switching to Tray. Focus on Tamarind. That’s where the money is.

**elara.vance** — May 18, 2026 9:15 AM
@marcus.thorne Did you send that Tamarind report? Their VP of Ops just pinged me on LinkedIn asking about "platform stability trends." I think they’re sniffing around for a credit because of that Beacon outage in April. 

**marcus.thorne** — 9:22 AM
Not yet, was stuck in the Monday All-Hands. Sending now. Just a heads up, `fact_workflow_runs` for Tamarind (CUST-4421) shows a 34% drop-off in successful executions since May 1st. Sarah, is that the CSS bug or something else?

**sarah.jenkins** — 9:45 AM
The CSS bug was VeloSync. Tamarind's issue is different—they’re hitting their concurrency limits on the Business plan. They need to move to Enterprise to get the unlimited runs, but they’re balking at the $120k floor. 

**rajiv.menon** — 10:05 AM
Speaking of Tamarind, I was looking at `nexus-analyst-demo.acme.fact_user_events` for them. Their "Active User" count is technically high, but 80% of those events are just `view_dashboard`. Nobody is actually `edit_workflow` or `create_transformation`. That’s a classic "zombie account" profile. 

**elara.vance** — 10:10 AM
@rajiv.menon can we get a Looker alert for that? Any Enterprise or Business account where `edit_workflow` events drop below 5 per week? We’re getting blindsided by these "Green" health scores that are actually "Red" in terms of value.

**olivia.tran** — 10:12 AM
The current Health Score logic in `dim_customers` is basically just `last_login_date` < 30 days and `status` = 'Active'. It’s way too simple. I’ve been trying to get Eng to prioritize the `usage_density` metric but it’s stuck in the "Later" bucket.

**marco.chen** — 10:15 AM
Eng is currently 100% focused on the "Project Chimera" refactor so we don't have another Beacon meltdown. If you want a new health metric, you'll have to build it in dbt, Rajiv. 

---

**#cs-at-risk** 

**sarah.jenkins** — May 19, 2026 2:10 PM
**Account Update: VeloSync (CUST-1102)**
*   **Status:** Red (Renewal June 2026)
*   **Risk:** Still reeling from the Beacon outage. NPS came back as a 3 yesterday. Comment: "Unreliable for production-critical flows."
*   **Ask:** I need a senior dev to join the QBR next Tuesday to walk them through the new redundancy architecture. Marco? 

**marco.chen** — 2:15 PM
I’m OOO next Tuesday for my sister’s wedding. Maybe Pete can do it? Also, tell them the `error_code` 'ERR_505' they keep seeing is actually a timeout on *their* API, not ours. 

**elara.vance** — 2:18 PM
I’ll take the VeloSync call if Pete can’t. We cannot lose $85k ARR over a CSS conflict and a few timeouts. 

**marcus.thorne** — 2:30 PM
Quick sidebar—anyone seen my Patagonia vest? Left it in the "Mission" room after the board deck prep. 

**sarah.jenkins** — 2:32 PM
I think the cleaners moved it to the lost and found near the micro-kitchen.

---

**rajiv.menon** — May 20, 2026 11:00 AM
Wait, why is **DataFlow Systems** showing up in `nexus-analyst-demo.acme.fact_subscriptions` with a `change_type` of 'RENEWAL' today? Marcus said they were a goner.

**marcus.thorne** — 11:05 AM
Wait, what? Let me check Salesforce. 

**marcus.thorne** — 11:12 AM
Okay, hilarious. Their new Head of IT used to be our champion at **Solaris Tech**. He signed the renewal without even talking to the team that was trying to switch to Tray. We’re back in, baby! 

**elara.vance** — 11:15 AM
Don't get too excited. If the end-users hate the tool, they'll just shadow-IT their way out of it by August. Sarah, get in there and do a "Lunch and Learn" or something. Let’s buy them some DoorDash credits. 

**olivia.tran** — 11:20 AM
Rajiv, I’m seeing a mismatch in the `seat_count_licensed` vs `seat_count` in the subscription fact for DataFlow. 
`SELECT customer_id, seat_count_licensed FROM nexus-analyst-demo.acme.dim_customers WHERE company_name = 'DataFlow Systems'` returns 150, but the invoice shows 250. 

**rajiv.menon** — 11:25 AM
That’s the "Expansion" they did last November that never got synced to the `dim_customers` master record. The sync script between Stripe and the Warehouse has been flaky since we added the EMEA regions. I'll add it to the "Data Debt" doc. 

---

**sarah.jenkins** — May 21, 2026 4:40 PM
**P1 ESCALATION: Apex Logistics (CUST-009)**
They just reported that all their webhooks are returning 401s. This is their main fulfillment flow. 

**marco.chen** — 4:45 PM
Checking logs... Oh boy. Someone rotated the master encryption key in the `vault-prod` cluster but didn't update the worker nodes. 

**elara.vance** — 4:47 PM
@marco.chen how long until it's fixed? Apex is our biggest Logistics logo. 

**marco.chen** — 4:55 PM
Rollback initiated. Should be back in 5 mins. Sarah, tell them to re-run any failed jobs from the last hour. 

**sarah.jenkins** — 5:01 PM
They’re asking for an RCA. This is the third time this month "someone" changed something in Vault. We need a better process. 

**marcus.thorne** — 5:10 PM
Agreed. My inbox is melting. Also, does anyone know if the South Park beer thing is still on for Friday? I need a drink after this week.

**sarah.jenkins** — May 22, 2026 9:15 AM
Apex Logistics (CUST-009) is breathing down my neck for that RCA. Marco, do we have a timeline? Their CTO is cc’ing Elara and our VP of Product now. 

**marco.chen** — 9:22 AM
Working on it. The Vault rotation script was a manual override that bypassed the CI/CD gate. It won't happen again, but writing it up in "Enterprise-speak" takes time. 

**elara.vance** — 9:45 AM
I’ll jump on a call with them at 11 AM PT if needed. Sarah, check their health score in the dashboard. Does it reflect the downtime yet?

**olivia.tran** — 9:50 AM
It won't show up until tomorrow's refresh. The `fact_workflow_runs` table is partitioned by day, and the dbt job for `fct_customer_health` runs at 2 AM UTC. 
`SELECT * FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE customer_id = 'CUST-009' AND status = 'error' AND triggered_at > '2026-05-21'` shows a 94% failure rate during the window. 

**marcus.thorne** — 10:05 AM
Speaking of health scores... can we PLEASE revisit the logic for the "At-Risk" flag? **Tamarind Group (CUST-021)** is showing as "Green" in the CRM but they haven't added a new workflow in three months. 

**rajiv.menon** — 10:12 AM
Marcus, the current logic is purely based on `seat_utilization` (active_users / seat_count_licensed). If they have 60 people logging in just to look at logs, it stays green. 
We talked about adding a `workflow_velocity` metric from `fact_workflow_runs`, but the warehouse team is buried in the EMEA migration. 

**sarah.jenkins** — 10:20 AM
Wait, **Tamarind Group** is coming back! I just got an email from their Ops lead. They want to reactivate the 40 seats they cut in Q1. Marcus, did you see the DocuSign? 

**marcus.thorne** — 10:22 AM
I see a "Viewed" notification, but no signature. They’re probably haggling over the Business tier pricing again. They still think they can get the $149/seat rate for a 30-seat commitment. 

**elara.vance** — 10:25 AM
No exceptions on the Business tier minimums. If they want the SSO and Audit Logs, it’s 50 seats min. Rules are rules. Or they can go Pro at $49 but they lose the security features. 

---

**olivia.tran** — May 25, 2026 2:10 PM
**Quarterly Business Review Prep - Beacon (CUST-012)**
Hey @elara.vance, I’m looking at Beacon’s usage post-incident. It’s... not good. 
Since the "Great Timeout" of April, their `run_count` is down 45%. 

**elara.vance** — 2:15 PM
Yeah, they moved their "Mission Critical" syncs back to a custom internal script. We’re basically just handling their Slack notifications and Jira ticket routing now. 

**marcus.thorne** — 2:18 PM
That’s a $240k ARR account. We can’t let them slide into "expensive notification bot" territory. 

**elara.vance** — 2:25 PM
I’m aware. I have a meeting with their Director of Platform on Thursday. 
@rajiv.menon can you pull a report on their latency for the last 30 days? I need to prove that we're stable now. 

**rajiv.menon** — 2:30 PM
Sure. `SELECT AVG(duration_ms) FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE customer_id = 'CUST-012' AND status = 'success'`. 
I'll DM you the Looker link. 

---

**sarah.jenkins** — May 26, 2026 8:45 AM
Quick heads up: I’m OOO this morning for a dental appointment. Back at 1 PM. 
If **Global Logistics (CUST-044)** pings about their API rate limits, tell them I’m already talking to Eng about a temporary lift. 

**marcus.thorne** — 8:52 AM
@sarah.jenkins Good luck with the dentist. Also, did you see the NPS comment from **DataFlow Systems**? 
"Tool is great, but the UI refresh is confusing. Where did the 'clone workflow' button go?"
Score: 4/10. 

**elara.vance** — 9:00 AM
Ugh, another detractor because of the v3.2 rollout. @marco.chen, can we put a tooltip or something on the new 'Duplicate' icon? People aren't finding it. 

**marco.chen** — 9:15 AM
It's in the changelog! Does no one read the "What's New" pop-up? 

**sarah.jenkins** — 9:16 AM
Marco, you know the answer to that. No. They do not. 

---

**rajiv.menon** — May 27, 2026 11:30 AM
**Alert: High Churn Probability detected for NexaScale (CUST-155)**
The model just flagged them. 
`last_login_date` for the Admin user was 22 days ago. 
`run_count` dropped from 5k/week to 200/week. 

**marcus.thorne** — 11:35 AM
NexaScale? I thought they were our biggest fan in the EMEA region. 
Wait... checking LinkedIn. Their VP of Eng (who bought the tool) left for Google two weeks ago. 

**elara.vance** — 11:40 AM
The "Champion Departure" kiss of death. 
Sarah, can you find out who the interim is? We need to get a meeting on the books before they look at the credit card statement and see a $12k/month charge they don't understand. 

**sarah.jenkins** — 11:45 AM
On it. I'll check `dim_users` to see if anyone else has Admin rights. 
`SELECT email_domain, role FROM nexus-analyst-demo.acme.dim_users WHERE customer_id = 'CUST-155' AND role = 'admin' AND is_active = true`
Looks like there's one other admin: `d.vogel@nexascale.io`. Reaching out now. 

**marcus.thorne** — 11:50 AM
Lunch anyone? I'm heading to that taco truck by the park. 

**elara.vance** — 11:52 AM
Can't. Still trying to figure out why the "Expansion Revenue" report in Salesforce is showing $0 for May when we clearly closed the Solaris Tech upsell. 

**olivia.tran** — 11:55 AM
That's because the `fact_subscriptions.change_type` was marked as 'RENEWAL' instead of 'EXPANSION' because they did it on the same day as their contract end date. I have to manually flip the bit in the staging table. I'll do it after my 12:30.

---

**rajiv.menon** — May 28, 2026 9:15 AM
@elara.vance @sarah.jenkins checking in on the "Health Score 2.0" definitions for the Enterprise segment. I’m seeing some weirdness where `storage_gb` utilization isn’t correlating with churn risk for the Ent guys like it does for SMB. 

**elara.vance** — 9:22 AM
That’s because Enterprise customers usually over-provision storage by like 400% just to be safe during the initial contract. Focus on `step_count` per workflow. If they are building 2-step "Hello World" workflows and paying $100k ACV, they aren't sticky. 

**rajiv.menon** — 9:30 AM
Got it. Updating the logic in the `ent_health_staging` table. 
`SELECT customer_id, AVG(step_count) as avg_complexity FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE triggered_at > '2026-04-01' GROUP BY 1 HAVING avg_complexity < 3`
There are 12 Enterprise accounts that look "shallow" right now. Including **Orbit-X (CUST-882)**. 

**sarah.jenkins** — 9:35 AM
Wait, Orbit-X is shallow? They just did a huge migration from Tray.io last quarter. 
@marcus.thorne did they mention any blockers during the handoff?

**marcus.thorne** — 9:42 AM
They’re struggling with the custom auth headers for their legacy ERP. Our docs are... lacking there. 
Also, heads up: I’m OOO this afternoon for my kid’s soccer game. If anything catches fire with Orbit-X, ping **tanya.reed** in Engineering. 

---

**tanya.reed** — May 29, 2026 2:10 PM
**P1 ESCALATION: Apex Logistics (CUST-442)**
Their core fulfillment workflow is failing with `error_code: 504`. It's hitting the Salesforce connector and timing out. 
`SELECT count(*) as fail_count FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE customer_id = 'CUST-442' AND status = 'failed' AND error_code = '504' AND triggered_at > '2026-05-29 12:00:00'`
Currently at 1,400 failures in the last 2 hours. 

**elara.vance** — 2:15 PM
Apex is our biggest logistics account in EMEA. If their fulfillment engine is down, they are losing money every minute. 
@marco.chen — is this related to the Beacon update last night? We’ve seen intermittent 504s on SFDC since the patch. 

**marco.chen** — 2:20 PM
Looking. It shouldn't be. Beacon only touched the worker polling logic, not the connector layer. 
Wait... I see it. The timeout threshold for the SFDC REST API was lowered from 30s to 10s in the latest config push. 
Reverting now. 

**tanya.reed** — 2:45 PM
Fix deployed. Apex runs are succeeding again. Sarah, can you reach out to their Ops lead (Jim B.) and offer a post-mortem? They’re going to be pissed. 

---

**rajiv.menon** — June 1, 2026 10:05 AM
**Good News: Tamarind Group (CUST-921) Reactivation**
They were marked as Churned back in Jan 2026 after that billing dispute, but I just saw a new subscription record pop up. 

**olivia.tran** — 10:12 AM
Confirmed! Marcus closed a "Win-back" deal. 
`SELECT customer_id, plan_tier, mrr_usd FROM nexus-analyst-demo.acme.fact_subscriptions WHERE customer_id = 'CUST-921' AND is_current = true`
They’re back on the Business plan, 75 seats, $11,175 MRR. 
The caveat is they have a 6-month "Success Rider" where they can cancel if we don't fix the SSO latency issue by Q3. 

**marcus.thorne** — 10:15 AM
It took 4 months of steak dinners to get them back. Don't let them churn again. @sarah.jenkins they're all yours. 

**sarah.jenkins** — 10:20 AM
Welcome back to the nightmare, Tamarind. I'll set up the kick-off call for Wednesday. 

---

**elara.vance** — June 2, 2026 8:45 AM
Quick poll: Does anyone actually use the "Customer Health" dashboard in Looker? 
I’m looking at the `dim_customers` join against `fact_user_events` and the "Active Users Last 7 Days" numbers look way too high. 

**rajiv.menon** — 8:52 AM
I built that... what looks wrong?

**elara.vance** — 8:55 AM
It says **Global Synergies (CUST-112)** has 400 active users. They only have 250 seats licensed. 
How is that possible?

**rajiv.menon** — 9:05 AM
Ah... damn. It's counting `invited_by_user_id` events as "activity" even if the person hasn't logged in yet. 
Basically, a bot or an admin is spamming invites and the dashboard thinks they are all "active." 
I need to update the filter to: 
`WHERE event_type = 'login_success' OR event_type = 'workflow_edit'`
I’ll push a fix to the dbt model tonight. 

**marcus.thorne** — 9:10 AM
Wait, if Global Synergies has 400 "users" (even if pending), that's an upsell opportunity! 
They are 150 over their seat limit. 
@olivia.tran do we have "auto-overage" billing turned on for them?

**olivia.tran** — 9:12 AM
Nope. They're on a legacy Enterprise contract. No overage clauses. 
We have to wait until renewal in October to hike the price. 

**marcus.thorne** — 9:15 AM
Stupid legacy contracts. Who signed that? 

**elara.vance** — 9:16 AM
You did, Marcus. Two years ago. 

**marcus.thorne** — 9:17 AM
...Right. Well, I was younger then. 

---

**sarah.jenkins** — June 2, 2026 11:30 AM
**NPS Detractor Alert: Zenith Corp (CUST-055)**
Comment: "The new UI is slow. We are considering moving back to internal scripts." 
Score: 2/10. 
This is the third 2/10 from their team this month. @marco.chen we really need to look at the latency on the "Workflow Canvas" page. It’s killing us with the bigger Enterprise accounts. 

**marco.chen** — 11:45 AM
It’s the DOM rendering for workflows with >50 steps. We're working on a virtualized canvas for v3.3. 
Tell them to hang tight for July? 

**sarah.jenkins** — 11:47 AM
July might be too late. Their renewal is July 15th. 
I'm going to put them on the "At Risk" tracker for the Q3 Board Deck. 

---

**rajiv.menon** — June 2, 2026 1:00 PM
Does anyone know where the `dim_employees` table went? 
I’m trying to run the "CSM Portfolio" report and it’s throwing a 404 in BigQuery. 

**olivia.tran** — 1:05 PM
Finance moved it to the `hr_private` dataset because someone (not naming names) found the `salary_band` column. 
You have to use the `nexus-analyst-demo.acme.dim_employees_public` view now. It has the `employee_id` and `full_name` but masks the sensitive stuff. 

**rajiv.menon** — 1:10 PM
Thanks. 
`SELECT e.full_name, count(c.customer_id) as account_load FROM nexus-analyst-demo.acme.dim_employees_public e JOIN nexus-analyst-demo.acme.dim_customers c ON e.employee_id = c.csm_employee_id WHERE e.is_active = true GROUP BY 1`
Holy crap, Sarah has 112 accounts. No wonder she’s stressed. 

**sarah.jenkins** — 1:15 PM
*screams into void* 

**elara.vance** — 1:18 PM
We're hiring two more CSMs in the Amsterdam office. Hang in there, Sarah. 
In the meantime, someone needs to tell Marcus to stop selling the "White Glove Implementation" package for $0. It's making the load worse.

**elara.vance** — June 4, 2026 9:00 AM
**@channel** Reminder: Q3 Planning starts today. Sarah, since you’re at 112 accounts, I’ve moved your 1:1 to Friday. Let’s look at the capacity model again. 

**sarah.jenkins** — 9:05 AM
Can we also discuss the "Health Score" logic? The current weights are 40% usage, 30% NPS, 30% Support Tickets. 
But **Global Logistics (CUST-102)** has a "Good" health score of 85, and their Webhook success rate just dropped to 12% because of the v3.2 migration. 
Usage looks "high" because they are retrying failed steps 50 times an hour. It's a false positive. 

**rajiv.menon** — 9:12 AM
I noticed that too. I'm looking at `nexus-analyst-demo.acme.fact_workflow_runs`.
`SELECT customer_id, status, count(*) as fail_count FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE status = 'FAILED' AND triggered_at > '2026-06-01' GROUP BY 1, 2 ORDER BY 3 DESC LIMIT 5`
Global Logistics is #1 on the list. 14,000 failures since Monday. 

**marco.chen** — 9:15 AM
Wait, 14k failures? Why didn't the P1 alert trigger? 

**rajiv.menon** — 9:16 AM
Because they haven't hit the "Total Workflow Volume" threshold yet. The noise from their successful "Ping" workflows is masking the actual business process failures. 

**elara.vance** — 9:18 AM
Sarah, get Global Logistics on a call immediately. If their fulfillment workflows are down, they won't just be "At Risk," they'll be "At Legal." 

---

**marcus.thorne** — June 10, 2026 2:30 PM
Good news! **Tamarind Group (CUST-012)** wants to come back. 
They went to a competitor for 6 months, hated the UI, and want to reactivate their Enterprise contract. 

**sarah.jenkins** — 2:35 PM
Are you kidding? They still owe us $12k from their final invoice in 2025. 

**marcus.thorne** — 2:36 PM
They said they'll pay it if we waive the implementation fee for the new "Beacon" module integration. 

**olivia.tran** — 2:40 PM
Marcus, check `nexus-analyst-demo.acme.fact_invoices` for CUST-012. 
Status is still 'VOIDED' by Finance because we couldn't collect. I’m not sure we can just "reactivate" without a fresh SOC2 review since they've been off the platform for >180 days. 

**marcus.thorne** — 2:42 PM
It’s a $150k ACV deal, Olivia. We’ll find a way. 

---

**rajiv.menon** — June 15, 2026 10:00 AM
**#cs-at-risk Update: Zenith Corp (CUST-055)**
Spoke with their Head of Ops. The 2/10 NPS was specifically about the `workflow_run_quota_per_month` limits on Business tier. 
They hit 100k runs on the 12th of the month. 

**sarah.jenkins** — 10:05 AM
Did you upsell them to Enterprise? 

**rajiv.menon** — 10:06 AM
They refused. They want to stay on Business but get "Enterprise-lite" quotas. 
Marcus told them during the initial sale that the 100k was a "soft cap." 

**elara.vance** — 10:10 AM
@marcus.thorne Stop saying "soft cap." There is no soft cap. The code literally stops the execution. 
Sarah, can you pull the last 3 months of their run volume from BigQuery? I need to see if this is a spike or a trend before we talk to their VP. 

**sarah.jenkins** — 10:15 AM
On it. 
`SELECT month, count(run_id) FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE customer_id = 'CUST-055' GROUP BY 1 ORDER BY 1 DESC`
March: 88k
April: 94k
May: 105k
June (Projected): 140k
It's definitely a trend. They’ve added three more Salesforce integrations. 

---

**system-bot** — June 18, 2026 8:00 AM
**OOO Alert: Sarah Jenkins**
Sarah is Out of Office until June 25. 
For urgent matters regarding **Zenith Corp** or **Global Logistics**, please contact Rajiv Menon. 

**rajiv.menon** — 8:05 AM
112 + 84 = 196. 
*stares at calendar*
*stares at BigQuery*
If anyone needs me, I'll be in the "Quiet Room" with a very large coffee. 

---

**marco.chen** — June 20, 2026 11:45 AM
**P1 Incident Post-Mortem: The "Beacon" Lag**
We’ve identified why the Enterprise health scores didn’t catch the Beacon module degradation last week. 
The `dim_customers.status` was updated to 'ACTIVE' for the pilot group, but the `fact_user_events` weren't being indexed for the new `event_type = 'beacon_heartbeat'`. 

**olivia.tran** — 11:50 AM
Does this mean the `is_active` flag in `dim_users` is wrong for those accounts? 

**marco.chen** — 11:52 AM
Partially. It’s showing them as active based on login, but we weren't seeing that they were stuck in the setup wizard for 4 hours. 
I'm pushing a fix to the dbt model tonight. `nexus-analyst-demo.acme.dim_customers` will have a new column `last_successful_workflow_at` to track actual value-delivery, not just logins. 

**elara.vance** — 11:55 AM
Good. We can't keep relying on "Login" as a proxy for health. 
Rajiv, check that new column for the Tamarind Group pilot. If they aren't shipping workflows by Friday, I'm pulling the plug on the implementation fee waiver.

**rajiv.menon** — June 22, 2026 9:15 AM
@elara.vance I just ran a check on Tamarind Group using Marco’s new column. It’s not looking good. 
`SELECT company_name, last_successful_workflow_at, current_mrr_usd FROM nexus-analyst-demo.acme.dim_customers WHERE company_name = 'Tamarind Group'`
The `last_successful_workflow_at` is NULL. They haven't successfully completed a single run since the Beacon pilot started on the 10th. 

**elara.vance** — 9:20 AM
Are you kidding? They’ve been "active" in the dashboard for two weeks. 

**rajiv.menon** — 9:22 AM
Yeah, because they have 15 users logging in daily and staring at the canvas, but they can't get the auth to stick for their Snowflake destination. I’m seeing a lot of `error_code = 'AUTH_REFRESH_FAIL'` in the logs for `CUST-912`. 
If we don't fix this by Friday, they are definitely going to ask for that implementation credit back. 

**marcus.thorne** — 9:45 AM
Hey, jumping in here—I just got off a call with the Lead Architect at **Stellar Dynamics**. They just dropped a '2' on the NPS survey. 
"Platform is a black box. We have no idea why workflows fail 20% of the time on Tuesdays." 
@marco.chen is there something specific about Tuesday cron loads? 

**marco.chen** — 10:05 AM
Tuesdays? That’s when the EMEA batch jobs from **Global Logistics** hit the same cluster. 
Sarah usually manages that, but since she’s OOO, I think their volume doubled without anyone noticing. 
`SELECT customer_id, count(*) as failure_count FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE status = 'FAILED' AND triggered_at >= '2026-06-16' GROUP BY 1 ORDER BY 2 DESC LIMIT 5`
Stellar Dynamics (`CUST-441`) is top of the list with 4.2k failures. 

**olivia.tran** — 10:10 AM
@marcus.thorne we need to stop selling "Unlimited" to these Ent accounts if we aren't going to shard the runners. 
Wait, Rajiv, did you see the ping about **Zenith Corp**? Their renewal is in 30 days and their utilization just dropped 40% overnight. 

**rajiv.menon** — 10:12 AM
I’m looking at it now. 
It looks like they offboarded their entire "Automation Ops" team. 12 users deleted from `dim_users` yesterday. 
@elara.vance This is a massive churn signal. $220k ARR at risk. 

**elara.vance** — 10:15 AM
Get the AE on the phone. Now. Who was the AE on Zenith? 

**rajiv.menon** — 10:16 AM
Checking... it's Jamie. But Jamie is at the offsite in Napa. 

**elara.vance** — 10:17 AM
Of course they are. 
Okay, I'm pulling the health rules. We need to revise the Enterprise Health Score (EHS) 2.0. 
Currently: 
- 30% Logins
- 50% Run Volume
- 20% Support Tickets
I want to change it to:
- 10% Logins
- 60% Successful Workflow Completion (`last_successful_workflow_at` within 48h)
- 30% Seat Utilization vs Licensed
If we had this last week, Zenith would have been glowing red. 

---

**system-bot** — June 23, 2026 12:00 PM
**Reminder: Lunch & Learn starts in 15 minutes**
Topic: "Navigating the new BigQuery Flat Schema" 
Location: Room 'The Hopper' / Zoom 
Host: Marco Chen

**marcus.thorne** — 12:05 PM
Can we record this? I have a conflict with a **CyberDyne** escalation. They’re saying the Beacon lag is still affecting their Jira sync. 

**marco.chen** — 12:06 PM
The lag is gone, Marcus. They probably just haven't cleared their local cache or re-authed the webhook. 
Tell them to check `nexus-analyst-demo.acme.fact_user_events`. If they see `event_type = 'webhook_received'`, the platform is doing its job. 

---

**rajiv.menon** — June 24, 2026 3:30 PM
Update on **Tamarind Group**:
Managed to get their Snowflake auth fixed. It was a CIDR block issue on their end. 
Ran a quick check:
`SELECT count(*) FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE customer_id = 'CUST-912' AND status = 'SUCCESS' AND triggered_at > CURRENT_TIMESTAMP - INTERVAL 1 HOUR`
We have 450 successful runs in the last hour. 
Implementation fee waiver is safe... for now. 

**elara.vance** — 3:45 PM
Good work, Rajiv. 
Now, what’s the status on **Global Logistics**? Sarah comes back tomorrow and if she walks into a P1, she’s going to kill us. 

**rajiv.menon** — 3:48 PM
*Sweats nervously*
Their SAP connector is still intermittent. Marco says it's a memory leak in the Beacon side-car. 
We've throttled their non-critical tasks to keep the main ERP sync alive. 
The good news is their `current_mrr_usd` is so high they technically qualify for the "Platinum Support" tier we haven't even launched yet, so I'm using that as an excuse for the slow response. 

**olivia.tran** — 4:00 PM
Has anyone seen the notebook I left in "The Hopper"? It has the draft for the Q3 churn forecast. 

**marcus.thorne** — 4:05 PM
I think I saw a janitor moving some stuff near the coffee machine. 
Also, @rajiv.menon—Zenith's VP just emailed back. They didn't fire the team, they "re-organized them into a Center of Excellence." 
They still want to talk about a "downsize" at renewal though. They only need 100 seats instead of 250. 

**elara.vance** — 4:10 PM
Downsize = Churn in my book. 
Rajiv, find out what they're doing with those other 150 seats. If they're moving to a competitor, I want to know which one. Check the `fact_user_events` for any exports of workflow definitions. If they’re bulk exporting, they’re leaving. 

`SELECT user_id, count(*) FROM nexus-analyst-demo.acme.fact_user_events WHERE event_type = 'workflow_export_bulk' AND customer_id = 'CUST-002' AND event_at > '2026-06-01' GROUP BY 1`

**rajiv.menon** — 4:12 PM
Running it now. 
Zero results. Looks like they aren't exporting. 
Maybe the "re-org" is actually just a re-org? 

**marcus.thorne** — 4:15 PM
Or they’re just going to rewrite everything manually in Python and save $200k. 
I hate June. 

---

**system-bot** — June 25, 2026 8:00 AM
**Welcome Back: Sarah Jenkins**
Sarah is back from OOO. 

**sarah.jenkins** — 8:05 AM
Why are there 47 unread messages in the Global Logistics channel and why is the SAP connector "throttled"? 
Rajiv, we need to talk. Now.

**sarah.jenkins** — 8:12 AM
I’m looking at the Global Logistics dashboard. Usage is flatlining. If the SAP connector isn't stable by EOD, I’m escalating this to the VP of Eng. Rajiv, I need a timeline for the Beacon side-car fix. 

**rajiv.menon** — 8:15 AM
@sarah.jenkins Marco is working on it. The memory leak only triggers on large payloads (>50MB). For now, we've asked their admin (Derek) to batch the ERP pushes. 

Also, welcome back! Hope the cruise was good? 🚢

**sarah.jenkins** — 8:16 AM
The cruise was fine until I saw the `dim_customers` snapshot this morning. Why is **Tamarind Group** listed as "Churned - Pending" in the CRM? They were our biggest win in 2024.

**marcus.thorne** — 8:20 AM
Tamarind is a mess. Their lead architect left for a crypto startup and the new guy, "Cloud-First Kevin," decided they could replicate our logic in AWS Step Functions. 
I’ve been trying to get a meeting for three weeks. 

**elara.vance** — 8:30 AM
Wait, Marcus—Kevin just pinged me on LinkedIn. He didn't say anything about AWS. He asked for the latest SOC2 report and "reactivation pricing." 
Maybe the Step Functions plan blew up in their face? 

**olivia.tran** — 8:35 AM
Probably. Running a cost-benefit on building vs. buying for 500+ workflows usually ends in tears once they see the maintenance overhead. 

@elara.vance check their historical usage before you give them a quote. I think they were hitting the `workflow_run_quota_per_month` every single month and getting overage charges. 
`SELECT customer_id, count(*) as runs FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE customer_id = 'CUST-089' AND status = 'success' GROUP BY 1`

---

**#enterprise-health-v2**

**olivia.tran** — July 1, 2026 10:15 AM
Is anyone else seeing weird numbers for the "Health Score" in the Executive Summary? 
**Solaris Tech (CUST-042)** is marked as "Green" (92/100) but I just looked at their `last_login_date` in `dim_users` and nobody has touched the platform since May. 

**marcus.thorne** — 10:18 AM
That's because the current health rule weighs "Workflow Completion Rate" at 60%. 
Solaris has one cron-job workflow that runs every hour and *never* fails. It’s a headless process. 
So the system thinks they’re "Healthy" even though the actual human users have abandoned the ship. 

**elara.vance** — 10:22 AM
Ugh, this is why we need to bake "MAU / Seat Count" into the score. 
If they pay for 300 seats and only 2 people are logged in, that’s a "Red" account, even if the 2 people are running 1 million successful workflows. 

**sarah.jenkins** — 10:25 AM
Agreed. Olivia, can you update the health logic? 
If `(active_users_last_30d / seat_count_licensed) < 0.2`, I want that account flagged as "At Risk" regardless of how well their workflows are running. 

**olivia.tran** — 10:30 AM
I can update the BI layer, but the dbt model `fact_customer_health_daily` is owned by the Data Eng team. I'll open a Jira. 

---

**#cs-at-risk**

**rajiv.menon** — July 5, 2026 11:00 AM
**Account Escalation: Skyline Tech (CUST-512)**
NPS Detractor alert. 
Score: 2/10. 
Comment: "The new Beacon UI is slow. We can't find the debug logs anymore. If this isn't fixed by our renewal in August, we are out."

**marcus.thorne** — 11:05 AM
Skyline is on a legacy Business plan. They're paying $149/seat but they're still on the old storage limits. 
I bet their "slowness" is just them hitting the `storage_gb` cap in `dim_plans`. 

**sarah.jenkins** — 11:10 AM
@rajiv.menon Get them on a call. Don't mention the renewal yet. Just show them where the logs moved to (it's under the 'Execution' tab now, not 'Settings'). 
If they're hitting the storage cap, give them a 30-day "temporary" bump while we negotiate the upgrade. 

**rajiv.menon** — 11:12 AM
On it. 
By the way, did anyone find Olivia’s notebook in The Hopper? 
The janitor said he didn't move it. 

**olivia.tran** — 11:14 AM
Actually, never mind. I found it. It was in the EMEA office. Apparently, I left it there during the offsite in Amsterdam. 
Don't ask how it got to Amsterdam. I'm still jet-lagged. 

---

**#general-noise**

**system-bot** — July 7, 2026 9:00 AM
**Today’s Birthdays:**
🎂 Marco Rossi (Eng)

**rajiv.menon** — 9:05 AM
Happy Birthday @marco.rossi! Please don't celebrate too hard, I still need that SAP connector fix for Global Logistics. 😭

**marco.rossi** — 9:15 AM
Thanks Rajiv. I'm literally pushing the patch to the staging environment now. 
If the tests pass, the memory leak should be gone by lunch. 

**sarah.jenkins** — 9:20 AM
If this works, I'm buying you a cake, Marco. A big one. 

**elara.vance** — 9:45 AM
Quick question—does anyone know if **Nexus Corp** (CUST-112) is still in their 90-day implementation window? 
I see 0 workflow runs in `fact_workflow_runs` for the last week. 
`SELECT count(*) FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE customer_id = 'CUST-112' AND triggered_at > '2026-06-30'`
Result: 0.

**marcus.thorne** — 9:50 AM
They are, but they're waiting for their Security team to sign off on the Webhook ingress. 
Standard Enterprise friction. I wouldn't worry yet. They already paid the invoice. 

**olivia.tran** — 10:00 AM
"They already paid" is my favorite sentence. 

**sarah.jenkins** — 10:05 AM
Mine too, but "They're actually using the product" is a close second. 
Let's make sure Nexus doesn't become another Tamarind. 
@rajiv.menon, keep an eye on their `dim_users` table. If the Security admin hasn't logged in by Friday, ping their champion.

---

**#cs-at-risk**

**rajiv.menon** — August 12, 2026 2:15 PM
Update on **Tamarind Group** (CUST-204). They’re asking about a "soft reactivation." 
Apparently, the new VP of Ops there used Acme at her last gig and wants to bypass the legal review they got stuck in last year. 
@marcus.thorne, do we still have their old workspace in cold storage or was it purged?

**marcus.thorne** — 2:22 PM
It’s flagged as `status = 'paused'` in `dim_customers`, so the metadata is there. 
But if they want to come back at a lower seat count, we might have a problem with their old custom connectors. 
They had a legacy SAP-HANA bridge that we don't even support on the Business tier anymore. 

**elara.vance** — 2:30 PM
Checking the usage history...
`SELECT * FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE customer_id = 'CUST-204' ORDER BY triggered_at DESC LIMIT 5`
Yeah, they haven't touched a workflow since October 2025. 
If we reactivate, we need to make sure they don't just sit on the Free tier and eat up support cycles like last time. 

**sarah.jenkins** — 2:45 PM
No Free tier for Tamarind. If they want back in, it's Business tier minimum. 
I'm not letting Rajiv spend 40 hours a week on their "complex" mapping logic for $0 MRR. 
@rajiv.menon, tell them we can waive the implementation fee if they sign a 12-month Business contract. 

**rajiv.menon** — 2:50 PM
Copy that. I'll send the proposal. 
Also, did anyone see the NPS detractor for **Zenith Solar** (CUST-551)? 
They gave us a 2 yesterday. 

**olivia.tran** — 3:00 PM
I saw that. The comment was just "UI is too purple." 
I'm not even joking. 

**elara.vance** — 3:05 PM
Wait, Zenith is on an Enterprise pilot. A "2" on NPS triggers an automatic Red flag in the health dashboard. 
Is the "too purple" comment really why they're at risk, or is it the latency issues in EMEA? 
I’m looking at `fact_workflow_runs` for Zenith:
`SELECT avg(duration_ms), error_code FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE customer_id = 'CUST-551' AND triggered_at > '2026-08-01' GROUP BY error_code`
They’re getting a lot of `ERR_TIMEOUT_60S`. 

**rajiv.menon** — 3:10 PM
The purple comment might be a smokescreen for the timeouts. 
Their main dev, Chen, mentioned they’re trying to pull 50GB chunks through the Snowflake connector. 
Of course it's going to time out. Our `dim_plans` for Enterprise has "unlimited runs" but we still have a 2GB memory limit per container execution. 

---

**#general-noise**

**system-bot** — August 14, 2026 8:30 AM
**Reminder:** The SF office kitchen will be closed this Friday for deep cleaning. Please remove all items from the fridge by Thursday 5:00 PM or they will be sacrificed to the Compost Gods. 

**marco.rossi** — 9:12 AM
Who keeps leaving the half-eaten oat milk lattes in the conference rooms? 
The "Hopper" smells like a science experiment gone wrong. 

**sarah.jenkins** — 10:15 AM
@here Quick heads up—I'm seeing some weirdness in the `fact_subscriptions` table for the July cohort. 
Some records have `is_current = true` but the `end_date` is in the past. 
`SELECT customer_id, end_date FROM nexus-analyst-demo.acme.fact_subscriptions WHERE is_current = true AND end_date < '2026-08-14'`
I'm counting 14 accounts like this. Is the dbt job failing? 

**marcus.thorne** — 10:20 AM
It might be the Beacon aftermath stuff. When we did the bulk migration of the legacy Pro plans to the new billing engine, some of the flags didn't flip correctly. 
I’ll ping the Data Eng team. They're probably still cleaning up the mess from the June outage. 

**olivia.tran** — 10:45 AM
By the way, I’m OOO next week for my sister's wedding in Maui. 
If anything catches fire with the **Apex Solutions** (CUST-099) renewal, talk to Rajiv. 
I’ve already updated their `current_mrr_usd` in the tracker—they're upgrading to Enterprise! 🚀

**rajiv.menon** — 10:50 AM
Have fun in Maui, Olivia! 
I’ll handle Apex. I already checked their `fact_user_events`. 
They had 450 active users last month, so they definitely need those 250+ Enterprise seats. 
`SELECT count(distinct user_id) FROM nexus-analyst-demo.acme.fact_user_events WHERE customer_id = 'CUST-099' AND event_at > '2026-07-01'`
Result: 442. 

**sarah.jenkins** — 11:00 AM
Wait, if Apex is 442 active users, why is their `seat_count_licensed` in `dim_customers` still showing 100? 
Are we giving them 342 seats for free right now? 

**marcus.thorne** — 11:05 AM
Yes. It was part of the "Growth Incentive" deal Olivia worked out to get them to sign the expansion. 
We're letting them over-provision until the contract start date on Sept 1st. 

---

**#cs-ops**

**elara.vance** — August 18, 2026 1:30 PM
Hey team, I'm finalizing the **Enterprise Health Score v2** logic. 
I want to include a "Champion Departure" flag. 
If the `user_id` who is marked as the primary contact in the CRM hasn't logged in for 30 days, I want it to drop the score by 20 points. 

**sarah.jenkins** — 1:45 PM
Love it. Can we also weight the `step_count` from `fact_workflow_runs`? 
If a customer is running 10k workflows but they're all 1-step pings, they aren't "sticky." 
If they have 5+ steps, they're using us for logic. 

**elara.vance** — 2:00 PM
Good point. 
`SELECT customer_id, avg(step_count) as complexity_score FROM nexus-analyst-demo.acme.fact_workflow_runs GROUP BY 1`
I'll build a view for this. 
Also, **Global Logistics** (CUST-302) is showing a massive spike in `error_code = 'ERR_AUTH_EXPIRED'`. 
Looks like their Okta token expired and no one noticed. 
Rajiv, can you check if their admin is still at the company? 

**rajiv.menon** — 2:15 PM
On it. Checking `dim_users`... 
The admin (p.hansen@globallogistics.com) hasn't logged in since June. 
`SELECT last_login_date FROM nexus-analyst-demo.acme.dim_users WHERE email_domain = 'globallogistics.com' AND role = 'admin'`
Last login: 2026-06-12. 
Uh oh. That looks like a "Champion Departure" for sure. 

**sarah.jenkins** — 2:20 PM
Get on that. Global Logistics is $120k ARR. We can't lose them because of a dead Okta token. 

---

**rajiv.menon** — 2:30 PM
Update on Global Logistics (CUST-302): It's worse than we thought. P. Hansen didn't just leave; he took the entire Ops team to a competitor. The new IT Director, some guy named "Derek," hasn't even heard of Acme. He's currently evaluating a "consolidation" play. 

**elara.vance** — 2:35 PM
@olivia — wasn't Global Logistics on your target list for the Q4 expansion? We need to get in front of this Derek guy before he rips us out for a legacy tool. 

**olivia.chen** — 2:40 PM
On it. I’m pinging their procurement contact now. Also, quick OOO note: I’m at the dentist from 3-5 PM today, then heading straight to the airport for the NYC offsite. If anything catches fire with Apex or Global, text me.

---

**#cs-strategy-and-logic**

**marcus.thorne** — August 19, 2026 9:15 AM
Revisiting the **Enterprise Health Score v2** from yesterday. 
Elara, can we add a decay function for `NPS_score`? 
We have a bunch of customers with a "10" from 2024 that are basically ghosts now. 
`SELECT customer_id, score, survey_date FROM nexus-analyst-demo.acme.fact_nps_responses WHERE score < 5`
Look at **Nova Systems** (CUST-155). They gave us a 2 last week. 

**elara.vance** — 9:30 AM
Nova Systems is a P1 escalation right now. 
`SELECT count(*) FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE status = 'failed' AND customer_id = 'CUST-155' AND triggered_at > '2026-08-01'`
Result: 1,402 failures in 18 days. 
Most are `error_code = 'ERR_TIMEOUT_GATEWAY'`. 
Their logic is hitting our rate limits because they're trying to sync 50k records every 5 minutes on a Business plan. 

**sarah.jenkins** — 9:45 AM
They need to be on Enterprise for that volume. 
But we can't upsell them while they're failing. 
Marcus, can you check if we can bump their concurrency limit temporarily as a "gesture of goodwill" while we negotiate the move to Ent? 

**marcus.thorne** — 9:50 AM
Checking with Eng. Also, @elara, did you see the thread in #product-announcements about the **Beacon Project** rollout? 
The "Beacon" engine is supposed to handle these high-concurrency syncs better, but the rollback last month really spooked the high-volume users. 
**Tamarind Group** (CUST-412) still hasn't reactivated their main production flows since the July 14th outage. 

**elara.vance** — 10:05 AM
Tamarind is a mess. 
`SELECT status, count(*) FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE customer_id = 'CUST-412' AND triggered_at > '2026-08-01' GROUP BY 1`
They only have 12 runs in the last month. They were doing 40k/mo before the Beacon incident. 
Olivia, didn't you say their CTO was "looking at options"? 

**olivia.chen** — 10:15 AM
Yeah, the Tamarind CTO is still salty about the downtime. 
I'm trying to "reactivate" them with a 3-month credit, but they're asking for a signed SLA that we technically don't support on the Business tier. 
If we want them back, we might have to "Enterprise" them at a massive discount just to keep the logo. 

**sarah.jenkins** — 10:20 AM
Let's hold on the discount. 
Can we see if their usage is shifting to a competitor or if they just stopped the process? 
`SELECT event_name, count(*) FROM nexus-analyst-demo.acme.fact_user_events WHERE customer_id = 'CUST-412' AND event_at > '2026-07-01' GROUP BY 1`
If `event_name = 'workflow_edit'` is 0, they've checked out. 

---

**#general**

**office-bot** — 11:00 AM
**Reminder:** The kitchen will be closed this Friday for deep cleaning. Please remove all personal items from the fridge by 4:00 PM Thursday or they will be discarded. 

**rajiv.menon** — 11:05 AM
Does this include the artisanal hot sauce collection? Asking for a friend. 

**marcus.thorne** — 11:10 AM
@rajiv If it's the one that’s been there since 2024, it’s probably a biohazard by now. 

---

**#cs-ops**

**elara.vance** — August 19, 2026 2:00 PM
Back to the Health Score logic. 
I’m adding a `utilization_delta` column. 
`SELECT (count_this_month - count_last_month) / nullif(count_last_month, 0) as growth_pct` 
`FROM (SELECT count(*) as count_this_month FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE customer_id = 'CUST-302' AND triggered_at > '2026-08-01')`
... you get the idea. 
Any customer whose `growth_pct` is < -25% for two consecutive months gets an automatic "At Risk" flag. 

**sarah.jenkins** — 2:15 PM
Make sure to filter out the "Sandbox" accounts. 
We have about 50 customers like **Acme-Test-Internal** (CUST-000) and **Partner-Beta-Ref** (CUST-005) that will throw off the averages. 

**elara.vance** — 2:20 PM
Done. I'll use the `account_tier != 'Free'` filter too. 
Hey, looking at the data, **Skyline Industries** (CUST-721) just dropped from 500 active users to 12. 
`SELECT * FROM nexus-analyst-demo.acme.dim_customers WHERE customer_id = 'CUST-721'`
They're on a $12k/month Business plan. 
Signed in Jan 2025. 
Who is the CSM on this? 

**rajiv.menon** — 2:25 PM
That’s mine. Wait, 500 to 12? 
I just talked to their VP of Eng on Monday and he said everything was "fine." 
Let me check `fact_user_events`. 
`SELECT user_id, count(*) FROM nexus-analyst-demo.acme.fact_user_events WHERE customer_id = 'CUST-721' AND event_at > '2026-08-15' GROUP BY 1`
...
It's just the 12 admins. 
They must have offboarded their entire "General User" group. 
This smells like a "moving to a different tool" situation where they keep the admins for the transition period. 

**sarah.jenkins** — 2:30 PM
Emergency huddle at 3:00 PM for Skyline. 
If they churn, that's a huge hole in the Q3 numbers. 
Also, someone tell Olivia to stop the NYC flight if she can—we need all hands on this. 

**olivia.chen** — 2:35 PM
Too late, I'm at the gate. But I can jump on the Zoom. 
Skyline is a big one. I remember their AE (Pete) saying they were frustrated with the "lack of native Salesforce integration" for their specific custom objects. 
Did we ever ship that patch from the July sprint? 

**marcus.thorne** — 2:40 PM
The SFDC custom object patch was delayed to Q4 because of the Beacon stability fixes. 
We prioritize stability, but it’s costing us the feature-hungry accounts. 

**elara.vance** — 2:45 PM
The classic Acme dilemma. 
I'll pull the full `fact_workflow_runs` report for Skyline for the meeting. 
`SELECT workflow_id, status, error_code FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE customer_id = 'CUST-721' AND triggered_at > '2026-07-01'`
I want to see if they were having technical issues before the seat drop.

**marcus.thorne** — 2:50 PM
Found something in the logs for Skyline. Looks like they weren't just "frustrated"—they were hitting a rate limit on the SFDC connector every time their "Sync Custom Opps" workflow ran. 
`error_code: 429_TOO_MANY_REQUESTS`
Because the patch was delayed, they were basically manual-triggering 200+ runs an hour to bypass the batching failure. That’s probably why they gave up. 

**sarah.jenkins** — 2:55 PM
Brutal. Okay, let’s pivot the 3:00 PM. We need to offer them a credit for the downtime and a "white-glove" migration to the beta version of the SFDC patch if Marcus can pull it from the staging branch. 
Also, someone needs to ping **Sam** in Finance to see if we can pause the auto-renewal on their contract for 30 days while we fix this. 

**rajiv.menon** — 3:02 PM
Wait, I’m jumping into the Skyline Zoom now. 
@elara.vance can you quickly run a query on **Tamarind Group** (CUST-009) while you're in the warehouse? 
They churned in Q2 2025 but their old "Lead Architect" just reached out to me on LinkedIn. They might want to reactivate for a specific project. 
Check if their `workflow_id`s are still in `fact_workflow_runs` or if they were purged. 

**elara.vance** — 3:10 PM
`SELECT * FROM nexus-analyst-demo.acme.dim_customers WHERE customer_id = 'CUST-009'`
Status is 'Churned', Churn Date: 2025-05-14. 
Checking the runs... 
`SELECT count(*) FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE customer_id = 'CUST-009' AND triggered_at > '2026-01-01'`
Zero runs since they left. The data is still there (we keep for 2 years per the Enterprise retention policy) but the definitions are dormant. 
If they reactivate, they'll be at the new 2026 pricing, right? 

**sarah.jenkins** — 3:15 PM
Yes, no grandfathering for Tamarind. They were on a legacy $80/seat deal. 
If they come back, they go straight to the Business tier ($149/seat) because they need the SSO and Audit Logs. 
Don't give away the farm, Rajiv. 

**olivia.chen** — 3:20 PM
(Joined Zoom from JFK Terminal 4)
The audio is terrible here. 
Quick thing—can someone remind me what the "Health Score" logic is for the Enterprise dashboard? 
I have **Global Logistics** (CUST-441) asking why their "Health Red" alert was triggered when their uptime is 99.9%. 

**elara.vance** — 3:25 PM
The "Enterprise Health Rule" isn't just uptime anymore. 
We updated it in March to be: 
`(Seat_Utilization * 0.4) + (Success_Rate * 0.4) + (Last_Login_Recency * 0.2)`
`Seat_Utilization` is `active_users / seat_count_licensed`. 
Global Logistics has 500 seats licensed but only 45 active users this month. That's why they're Red. 
`SELECT customer_id, seat_count_licensed, (SELECT count(DISTINCT user_id) FROM nexus-analyst-demo.acme.dim_users WHERE customer_id = 'CUST-441' AND is_active = true) as active_now FROM nexus-analyst-demo.acme.dim_customers WHERE customer_id = 'CUST-441'`

**olivia.chen** — 3:30 PM
Ah, okay. They probably over-provisioned during their Q1 expansion. 
I'll tell them it's a utilization warning, not a technical one. 
Gotta go, boarding. TTYL. 

**rajiv.menon** — 4:05 PM
Skyline update: It was a bloodbath. 
The VP of Eng didn't even show up. It was just their Procurement lead. 
They aren't "moving to a tool"—they are consolidating everything into their parent company's stack. 
Unless we can prove we are "mission critical" by Friday, they are going to non-renew the full $144k ARR. 

**marcus.thorne** — 4:10 PM
Is Beacon still having that memory leak in the Amsterdam cluster? 
Because if Skyline's EMEA team was seeing lag on top of the SFDC issues, we’re toast. 
`SELECT avg(duration_ms), region FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE triggered_at > '2026-05-01' GROUP BY region`
Look at the spikes in `EU-CENTRAL-1`. 

**elara.vance** — 4:15 PM
Yeah, I see it. 
Avg duration for Amsterdam is 4500ms vs 1200ms for US-East. 
That started right after the Beacon v2.4 push last Tuesday. 
Is this the "Beacon aftermath" we were worried about? 

**sarah.jenkins** — 4:20 PM
Marcus, get the SRE team on that. Now. 
If we have a regional slowdown while Skyline is deciding our fate, we have zero leverage. 
I’m going to go ping Pete (AE) and see if he has any back-channel info on who the "parent company" is. 
Maybe we have an existing Enterprise deal with the parent we can piggyback on. 

**elara.vance** — 4:25 PM
Checking the hierarchy now. 
`SELECT company_name, customer_id FROM nexus-analyst-demo.acme.dim_customers WHERE company_name LIKE '%Skyline%' OR company_name LIKE '%Industries%'`
Wait, **Apex Corp** (CUST-102) acquired a bunch of firms last year. 
Are they the parent? They're one of our oldest Enterprise accounts. 

**rajiv.menon** — 4:30 PM
If Apex is the parent, we might be able to save this. 
I'll check the CRM. 
Also, OOO tomorrow morning (dentist). Back by noon. 

**marcus.thorne** — 4:35 PM
Found it. The memory leak is in the `node-executor` service specifically for scheduled webhooks. 
I'm rolling back the Amsterdam cluster to v2.3.5. 
The lag should clear in 10 minutes. 

**elara.vance** — 4:40 PM
`SELECT count(*) FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE status = 'ERROR' AND error_code = 'TIMEOUT' AND triggered_at > '2026-05-04 16:00:00'`
Errors are already dropping. Good catch Marcus. 
Now back to Skyline... if I pull the `fact_invoices` for them, has the Q3 invoice actually been sent? 
`SELECT * FROM nexus-analyst-demo.acme.fact_invoices WHERE customer_id = 'CUST-721' ORDER BY invoice_date DESC LIMIT 1`
Status: 'Draft'. 
Good. We have time to adjust the amount or hold it before it hits their AP desk. 

**sarah.jenkins** — 4:45 PM
Hold it. Do not send that invoice yet. 
I'm calling the Apex Corp CSM (it's **David**, right?) to see if he can get us a meeting with the Skyline leadership under the Apex umbrella. 
This just became a "Save the Account" P1. 
@channel - any other accounts showing 429 errors on SFDC? I want a list before the end of day. 

**elara.vance** — 4:50 PM
On it. 
`SELECT customer_id, count(*) as error_count FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE error_code = '429_TOO_MANY_REQUESTS' AND triggered_at > '2026-04-01' GROUP BY 1 ORDER BY 2 DESC`
...
Crap. **Biohealth Solutions** (CUST-332) and **Omni Retail** (CUST-559) are both in the top 5. 
They're both Business tier. We might have a bigger churn wave coming if we don't ship that patch. 

**marcus.thorne** — 4:55 PM
I'll talk to the Eng leads. Maybe we can cherry-pick the SFDC fix and do a hotfix tonight instead of waiting for the full Q4 release. 
No promises. My team is fried after the Beacon stuff. 

**sarah.jenkins** — 5:00 PM
Coffee's on me tomorrow if we get a fix. 
Let's keep the Skyline thread updated. 
@rajiv.menon - good luck at the dentist. Don't let them upsell you on the fancy fluoride. 

**rajiv.menon** — 5:02 PM
👍 🦷

---
**sarah.jenkins** — May 5, 2026 9:15 AM
Morning team. Any update on the SFDC hotfix? **Biohealth Solutions** (CUST-332) just pinged their CSM (Rajiv, hope the tooth is better) saying their lead routing workflow is failing every 10 minutes. 
This is a Business tier account with 110 seats. We can't let them sit on 429s for another 24 hours. 

**marcus.thorne** — 9:22 AM
The hotfix for the node-executor (v2.3.6-patch1) is in staging. 
Running the test suite now. Amsterdam is stable on the rollback, but the SFDC rate-limiting logic is still wonky in the core lib. 
Give me until 11 AM. 

**elara.vance** — 9:35 AM
Quick look at Biohealth's usage patterns:
`SELECT date, count(run_id) as total_runs, sum(case when status = 'ERROR' then 1 else 0 end) as error_count FROM nexus-analyst-demo.acme.fact_workflow_runs WHERE customer_id = 'CUST-332' AND triggered_at > '2026-04-28' GROUP BY 1 ORDER BY 1 DESC`
They've spiked to 45k runs/day. Their quota is 100k/month. 
@sarah.jenkins - They aren't just hitting a bug, they're hitting their monthly ceiling way too fast because of a loop in their "Lead Sync" workflow. 

**rajiv.menon** — 9:42 AM
(Back from the dentist, jaw is numb but I'm here)
@elara.vance is right. Biohealth added a new SDR team in London last week. I think they misconfigured the trigger. 
I'll hop on a call with their Ops lead, **Isabel**, and see if we can optimize the logic. 
Also, re: **Tamarind Group** (CUST-088) — remember they churned back in Feb? 
Their old CTO just reached out. They want to reactivate on an Enterprise plan for their "Project Phoenix" migration. 
@sarah.jenkins - who do I talk to about getting their old instance out of cold storage? 

**sarah.jenkins** — 9:50 AM
Huge if true. Tamarind was a $45k ARR loss. 
@marcus.thorne - is the DB snapshot for CUST-088 still in the Glacier bucket or did we purge? 

**marcus.thorne** — 9:55 AM
Policy is 90 days. Feb to May... we're right at the edge. 
I'll check the `dim_customers` status. 
`SELECT customer_id, company_name, churn_date, status FROM nexus-analyst-demo.acme.dim_customers WHERE customer_id = 'CUST-088'`
Status is 'Inactive', churn_date '2026-02-12'. 
We should still have the backup. Tell them it'll take 4 hours to provision the workspace once the contract is signed. 

**elara.vance** — 10:05 AM
Speaking of Enterprise... @channel does anyone have the updated "Health Score" logic for the Q3 QBRs? 
I'm looking at **Omni Retail** (CUST-559) and their seat utilization is cratering. 
`SELECT seat_count_licensed, (SELECT count(distinct user_id) FROM nexus-analyst-demo.acme.fact_user_events WHERE customer_id = 'CUST-559' AND event_at > '2026-04-01') as active_users FROM nexus-analyst-demo.acme.dim_customers WHERE customer_id = 'CUST-559'`
They pay for 300 seats. Only 42 users logged in last month. 
That's a massive red flag for the renewal in August. 

**sarah.jenkins** — 10:12 AM
Omni is **David's** account. David is OOO hiking the PCT until Thursday. 
Can someone pull the NPS data for them? Last I checked they were promoters. 

**elara.vance** — 10:15 AM
`SELECT score, comment, created_at FROM nexus-analyst-demo.acme.fact_nps_responses WHERE customer_id = 'CUST-559' ORDER BY created_at DESC LIMIT 5`
Score: 4. 
Comment: "Platform is too slow for our peak weekend traffic. Support hasn't responded to our ticket about the Shopify connector lag." 
Ouch. 

**marcus.thorne** — 10:20 AM
That's the Beacon aftermath. The Shopify connector was the hardest hit during the April 14th outage. 
We're still cleaning up the mess in the message queue. 
I'm going to be in the "War Room" (Conference Room B) if anyone needs the SFDC update. 
Also, has anyone seen my "Property of Eng" mug? It's gone missing again. 

**rajiv.menon** — 10:25 AM
I think I saw it in the kitchen near the cold brew tap. 
By the way, I'm OOO Friday for a wedding. If **Biohealth** blows up, please ping **Jamie**. 

**sarah.jenkins** — 10:30 AM
@elara.vance can you build a dashboard for "Ghost Towns"? 
I want a list of all accounts where `active_users < (seat_count_licensed * 0.25)` AND `renewal_date < '2026-09-01'`. 
We need to be proactive. If we wait until the QBR, we've already lost the renewal. 
I'll check the `fact_subscriptions` table to see if we have any other Enterprise-tier churn risks. 

**elara.vance** — 10:45 AM
On it. 
`SELECT c.company_name, c.current_mrr_usd, s.end_date FROM nexus-analyst-demo.acme.dim_customers c JOIN nexus-analyst-demo.acme.fact_subscriptions s ON c.customer_id = s.customer_id WHERE c.account_tier = 'Ent' AND c.status = 'Active' AND s.is_current = true ORDER BY s.end_date ASC`
Looks like **Zenith Corp** (CUST-921) is up for renewal in 60 days. 
They're our 4th largest Enterprise account. 
@rajiv.menon - are you the CSM for Zenith too? 

**rajiv.menon** — 10:50 AM
No, that's **Elena**. She's been working on their expansion into the APAC region. 
Actually, Zenith utilization is through the roof. They're asking for *more* seats, but they want a discount on the per-seat price because they're hitting 500+ users. 

**marcus.thorne** — 11:00 AM
Hotfix v2.3.6-patch1 is LIVE in Amsterdam and US-East. 
`UPDATE nexus-analyst-demo.acme.internal_release_log SET status = 'DEPLOYED' WHERE version = '2.3.6-p1'`
SFDC 429 errors should be resolving. 
Now, I'm going to find my mug and then take a very long lunch. 

**sarah.jenkins** — 11:05 AM
Nice work Marcus. 
@elara.vance - add Zenith to the dashboard anyway. High utilization + pricing friction = "Negotiation Risk". 
I'll talk to Finance about the volume discount tiers for the >500 seat bracket. 
Currently we're hard-coded at $149 for Business, but the Enterprise contracts are all over the place. 
`SELECT avg(mrr_usd / seat_count) as effective_seat_price FROM nexus-analyst-demo.acme.fact_subscriptions WHERE plan_tier = 'Enterprise' AND is_current = true`
... 
$112/seat. If Zenith wants $95, we're going to have a margin discussion.