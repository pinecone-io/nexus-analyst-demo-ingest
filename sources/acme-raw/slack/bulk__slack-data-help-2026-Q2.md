---
title: "Slack #data-help channel — 2026 Q2"
source_url: "internal://acme/slack-data-help-2026-Q2"
license: "synthetic-demo"
attribution: "Synthetic content, Acme Inc internal demo. Acme Inc is a fictitious company."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

### #data-help

**Channel Topic:** Need help with SQL, Looker, or metrics? Ask here! Check #data-announcements for system status. Data Catalog: internal.acme.io/data-dict

---

**April 1, 2026**

**nina.patel** [09:12 AM]
Morning all! Does anyone know if the SF office finally got those ergonomic mesh chairs delivered? My lower back is screaming. Also, quick data question: I’m seeing a discrepancy between the `dim_customers.current_mrr_usd` and the totals in `arr_snapshot`. Which one should I use for the EOM deck?

**lina.cho** [09:15 AM]
Hey Nina, chairs are in the loading dock apparently—Jorge might know more. On the data: **Always use `arr_snapshot` for board/official reporting.** `dim_customers.current_mrr_usd` drifts intraday as subs change, whereas the snapshot is the frozen canonical record. 

**rajiv.menon** [09:17 AM]
^ +1. And remember ARR = SUM(mrr_usd) * 12 from `fact_subscriptions` where `is_current` is true and `plan_tier != 'Free'`. The snapshot does this heavy lifting for you.

**nina.patel** [09:18 AM]
Perfect, thanks Lina! I’ll wait for the chairs and the snapshot.

---

**April 2, 2026**

**tom.becker** [10:45 AM]
Quick check for the RevOps squad: I’m looking at the `bookings_attribution` table for a report for Marcus. If a Pro customer self-serves into a Business plan, does that ACV show up here?

**jorge.martinez** [10:50 AM]
Nope. `bookings_attribution` only tracks AE-led deals (Pro -> Business or Business -> Enterprise) that go through a Salesforce opportunity. Self-serve Pro conversions are handled strictly through the billing engine and don't hit the AE attribution logic.

**tom.becker** [10:52 AM]
Got it. Also, should I multiply the `bookings_acv_usd` by 12 to get the annual impact?

**lina.cho** [10:55 AM]
**No! Do not multiply by 12.** `bookings_acv_usd` is already annualized. If you multiply it by 12, you're reporting 144 months of revenue. We're doing well, but not *that* well lol.

**tom.becker** [10:56 AM]
Whew, good thing I asked. That would have been a very awkward conversation with Sam.

---

**April 5, 2026**

**olivia.tran** [02:14 PM]
Is anyone else seeing weirdness with Marigold Health (cust_000701)? Looker says they are 'Critical' health, but they just signed a huge Enterprise expansion. 

**rajiv.menon** [02:18 PM]
Checking `account_health`... Olivia, Enterprise health logic is different. For Enterprise, the only thing that triggers 'Critical' is a recent uncollectible invoice. It ignores the utilization band because those contracts are often custom. Does Marigold have an unpaid invoice in `fact_invoices`?

**olivia.tran** [02:22 PM]
Ah, let me check... yep. Finance flagged invoice #INV-9928 as uncollectible last week. That explains it. I'll ping Rachel's team.

**rajiv.menon** [02:25 PM]
Cool. For non-enterprise (Pro/Business), 'Critical' is either uncollectible OR utilization_band < 0.20. But for Ent, we're more hands-on, so we only auto-flag on the money.

---

**April 8, 2026**

**sarah.chen** [11:05 AM]
Anyone want to go to the taco truck today? 🌮 

**omar.haddad** [11:06 AM]
In. 

**yuki.sato** [11:06 AM]
+1

**sarah.chen** [11:10 AM]
Also, I'm trying to pull a list of "engaged" users for Onyx Robotics (cust_000704). My query is returning way more than the health dashboard. What's the current "Engaged" definition?

**rajiv.menon** [11:15 AM]
We recalibrated that in Q4. An engaged customer is now defined as: **≥3 active users AND ≥10 successful workflow runs in the trailing 28 days.** 

**sarah.chen** [11:17 AM]
Oh, I was only looking at 7 days. That explains the gap. Thanks Rajiv! Meet you at the truck in 10.

---

**April 12, 2026**

**david.kim** [09:00 AM]
🚨 **Data Platform Update:** We are migrating some internal logic. Please note that the BigQuery structure is FLAT. I see some people trying to query `nexus-analyst-demo.acme.marts.cs.account_health`. That will fail. 

**david.kim** [09:01 AM]
The correct path is `nexus-analyst-demo.acme.account_health`. We do not use nested datasets/marts in the warehouse. The dbt folders are just for organizational sanity in the repo.

**nina.patel** [09:05 AM]
Wait, so no `acme.finance.arr_snapshot`? 

**david.kim** [09:06 AM]
Correct. Just `acme.arr_snapshot`. 

**nina.patel** [09:07 AM]
Got it. My SQL scripts thank you for the heads-up.

---

**April 15, 2026**

**marco.silva** [03:30 PM]
Hey data-friends. I'm looking for the VRS (Value Realization Score) for Cobalt Systems. I see the column in some old documentation but can't find it in the `account_health` table.

**rajiv.menon** [03:35 PM]
**VRS is still parked.** We have the draft spec for `vrs_band` and `champion_login_recency`, but we haven't built the pipeline yet. Engineering focus shifted to the SOC2 audit. 

**rajiv.menon** [03:36 PM]
Use the `account_health_status` and `utilization_band` in the meantime—those are the shipped proxies.

**marco.silva** [03:38 PM]
Copy that. I'll stop searching through the metadata then.

---

**April 20, 2026**

**lina.cho** [11:00 AM]
Who is responsible for the NRR calculation in the "Customer Growth" dashboard? I think the numbers are inflated. 

**rajiv.menon** [11:05 AM]
I'm looking. Wait... someone changed the join logic in the cohort model. 

**rajiv.menon** [11:08 AM]
Found it. It was using an `INNER JOIN` between the starting cohort and the ending MRR. That means it was dropping customers who churned (they aren't in the current sub table). 

**rajiv.menon** [11:10 AM]
**PSA:** To get correct NRR, you MUST use a `LEFT JOIN` from the cohort and `COALESCE(end_mrr_usd, 0)`. If you inner join, you drop the churns and the NRR looks like 140% when it's actually ~107%. 

**lina.cho** [11:12 AM]
Yeah, that's what I thought. I was looking at the NRR and thinking "There's no way we're doing this well with the Beacon Studios churn last month." 

**nina.patel** [11:14 AM]
Oh man, the classic NRR trap. Didn't we have a postmortem on this last year? 

**rajiv.menon** [11:15 AM]
We did. I'm reverting the dbt model now. Deploying... should be fixed in the warehouse in ~15 mins.

---

**April 22, 2026**

**grace.liu** [10:12 AM]
Quick question on plan tiers. Does the 'Free' plan have a workflow run quota? Pebble Digital (cust_000705) is asking.

**dan.lee** [10:15 AM]
Yep. Free is 100 runs/mo and 2 active workflows. Pebble is actually on the Pro plan though ($49/seat). They have a 10K run quota. If they need more, they need the Business tier.

**grace.liu** [10:17 AM]
Wait, Pebble is Pro? I thought they were SMB.

**dan.lee** [10:18 AM]
They are SMB (account_tier), but they pay for the Pro plan (plan_tier). Remember: `account_tier` is about company size, `plan_tier` is what they pay us.

---

**April 25, 2026**

**jorge.martinez** [09:00 AM]
Poll: New SF office standup time?
A) 9:30 AM
B) 10:00 AM
C) 10:30 AM
D) "Just Slack it"

**sam.reyes** [09:05 AM]
D. 

**priya.anand** [09:06 AM]
D.

**marcus.webb** [09:10 AM]
A (I'm an early bird)

**jorge.martinez** [09:15 AM]
Okay, looks like we're staying with the Slack standup mostly. Marcus, you can talk to yourself at 9:30 lol.

---

**May 1, 2026**

**nina.patel** [01:22 PM]
I'm trying to reconcile the total ARR for April. I'm getting ~$39.2M, but the "Sales Leaderboard" says $41M. 

**lina.cho** [01:25 PM]
The Sales Leaderboard is probably using a stale Looker PDT or maybe it's including "Committed ARR" for deals that haven't actually started yet. 

**lina.cho** [01:26 PM]
**Signal check:** The `arr_snapshot` table is the source of truth. As of today, ARR is ~$39M. Breakdown is roughly: Business ~$32M, Enterprise ~$6M, Pro ~$1M. 

**nina.patel** [01:28 PM]
Thanks Lina. I’ll tell Marcus to stop telling people $41M until the contracts actually start.

---

**May 4, 2026**

**rajiv.menon** [10:40 AM]
Hey @david.kim, is the warehouse lagging? I see events from 4 hours ago but nothing more recent.

**david.kim** [10:45 AM]
BI warehouse usually lags prod by ~2h. There was a slight hiccup in the Fivetran connector for `fact_user_events` this morning. Should be caught up by 11:30 AM.

**rajiv.menon** [10:47 AM]
Cool, thanks. Just checking because I'm trying to see if Tamarind Group (cust_000706) has logged in since their pause.

**marco.silva** [10:48 AM]
Tamarind is still paused as of Jan. They're waiting on their Q3 budget. No need to rush that data, they aren't doing anything.

---

**May 8, 2026**

**olivia.tran** [04:15 PM]
Can someone check my SQL? I'm trying to find all customers in 'dev-tools' industry who had a 'RATE_LIMITED' error in the last week.

```sql
SELECT company_name 
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.fact_workflow_runs` w ON c.customer_id = w.customer_id
WHERE c.industry = 'devtools' 
  AND w.error_code = 'RATE_LIMITED'
  AND w.triggered_at >= '2026-05-01'
```

**rajiv.menon** [04:20 PM]
Query looks fine, but just a reminder: we don't have step-level facts in the BI layer. If you're looking for *which* step failed, you have to go to the JSON in `fact_user_events`. But for high-level error counts, your query is correct.

**rajiv.menon** [04:21 PM]
Wait, Onyx Robotics (cust_000704) and Kestrel Networks (cust_000708) are both in devtools. Kestrel churned in November, so they shouldn't have any recent runs. Onyx is probably your main culprit.

**olivia.tran** [04:23 PM]
Yep, it's Onyx. They're hitting the 100K Business quota? 

**rajiv.menon** [04:24 PM]
Actually, Onyx is Enterprise (cust_000704). They have unlimited runs. If they're getting `RATE_LIMITED`, it's probably the *target* SaaS (like Salesforce or Jira) rate-limiting us, not Acme limiting them. Check the `properties_json` in the events table.

---

**May 12, 2026**

**jasmine.park** [09:12 AM]
Morning! Marketing question: Does the `bookings_attribution` table show the `first_touch_channel` for every customer?

**lina.cho** [09:15 AM]
Only for the AE-led deals (Business/Enterprise). For the Pro/Free users, you have to look at `dim_customers.acquisition_channel`. 

**jasmine.park** [09:17 AM]
Got it. I'm trying to see if the EMEA 'event' channel (from the Amsterdam team's roadshow) actually led to any Enterprise wins. 

**lina.cho** [09:20 AM]
Check `bookings_attribution` filtered by `region = 'EMEA'` and `first_touch_channel = 'event'`. That should give you the ACV by channel. 

**jasmine.park** [09:21 AM]
Perfect. Oh, and who’s cat just walked across the camera in the All-Hands? 

**sam.reyes** [09:22 AM]
That was mine. His name is "Revenue" but he's currently a "Detractor."

---

**May 15, 2026**

**omar.haddad** [02:00 PM]
I'm looking at Yarrow Logistics (cust_000703). They are APAC Business tier. The dashboard says they have 120 seats, but only 40 are active. Is their health 'monitoring' or 'at_risk'?

**rajiv.menon** [02:05 PM]
Yarrow Logistics... let's see. 40/120 = 0.33 utilization. Since they are Business (not Enterprise), the threshold for 'Critical' is < 0.20. So they aren't critical. 

**rajiv.menon** [02:06 PM]
Are there any open P1 support tickets > 48h? Or a recent NPS detractor?

**omar.haddad** [02:08 PM]
Looking at `fact_support_tickets`... nope, all closed. NPS score was an 8 last quarter.

**rajiv.menon** [02:10 PM]
Then they are in 'monitoring' status. They are 'engaged' (since 40 > 3 users and they have 10k+ runs), but their utilization isn't high enough for 'healthy_expansion' (which requires ≥ 0.6).

---

**May 18, 2026**

**nina.patel** [11:45 AM]
Hey Rajiv, quick SQL sanity check. I'm doing a churn analysis for Q1. If a customer downgrades from Business to Free, does that count as churn in our NRR model?

**rajiv.menon** [11:50 AM]
**Yes.** In our reporting, a downgrade to the Free tier is treated as churn ($0 MRR for the cohort ending value). If they go from Business to Pro, it's a downgrade (contraction), but not churn. 

**nina.patel** [11:52 AM]
Okay, just making sure. That explains why my NRR was lower than Sarah's spreadsheet. She was counting the Free-tier "active" accounts as retained.

**rajiv.menon** [11:54 AM]
Yeah, Sarah's wrong there. Free accounts don't contribute to ARR/NRR. If they aren't paying, they are churned from a revenue perspective.

---

**May 22, 2026**

**sarah.chen** [03:10 PM]
Is anyone else having trouble with Looker being slow today? 

**david.kim** [03:12 PM]
Somebody (I won't name names, but check the BigQuery console) is running a massive cross-join on `fact_user_events` without a date partition. It's eating all the slots.

**nina.patel** [03:13 PM]
It wasn't me! I was querying `dim_employees`.

**rajiv.menon** [03:15 PM]
Killed the query. It was a "select *" on a 2-year event table. Please, everyone: **always use a date filter on `fact_user_events` and `fact_workflow_runs`.** These tables are too big to scan fully every time.

**sarah.chen** [03:17 PM]
Thanks David/Rajiv. Looker is snappy again.

---

**May 26, 2026**

**yuki. Sato** [10:00 AM]
Happy Tuesday. Quick question: For the customer Driftwood Media (cust_000702), they are on the Pro plan with 18 seats. Their MRR is listed as $882. Is that right? $49 * 18 = $882.

**lina.cho** [10:05 AM]
Yep, math checks out. Why? 

**yuki.sato** [10:07 AM]
Just confirming. I'm helping them with a transition to Business tier. They want to go to 50 seats (the minimum for Business). That would jump them to $7,450 MRR ($149 * 50). 

**lina.cho** [10:10 AM]
Correct. That would be a huge expansion. Make sure to log that in Salesforce so it hits the `bookings_attribution` table next month!

---

**May 29, 2026**

**tom.becker** [01:45 PM]
Does anyone know why Cobalt Systems (cust_000700) is showing up as EMEA in `dim_customers` but the AE is me (NA-West)? 

**jorge.martinez** [01:50 PM]
They are headquartered in London (EMEA), but you handled the deal because they were a referral from an NA-based partner. Regional reporting is based on the customer's location, not the AE's location.

**tom.becker** [01:52 PM]
Got it. Just wanted to make sure my commissions weren't going to the Amsterdam office lol.

**sam.reyes** [01:55 PM]
Don't worry Tom, the data doesn't lie. You're getting your cut.

---

**May 31, 2026**

**rajiv.menon** [04:30 PM]
Final reminder for EOM: The BigQuery dataset is `nexus-analyst-demo.acme`. Do not use `marts_finance`, `dbt_results`, or any other temporary datasets. Use the flat tables. 

**rajiv.menon** [04:31 PM]
And for the 100th time—**NRR uses a LEFT JOIN.** 

**lina.cho** [04:35 PM]
Loud and clear Rajiv. Happy weekend everyone!

**nina.patel** [04:36 PM]
Weekend! 🥂

**sam.reyes** [04:40 PM]
Great work this month, team. The ARR growth is looking solid. See you all Monday.

---
*End of Slack Export*