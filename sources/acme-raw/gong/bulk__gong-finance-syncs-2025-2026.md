---
title: "Gong finance sync call transcripts — 2025-2026"
source_url: "internal://acme/gong-finance-syncs-2025-2026"
license: "synthetic-demo"
attribution: "Synthetic content, Acme Inc internal demo. Acme Inc is a fictitious company."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: gong_call
---

### Meeting Transcript: Bi-Weekly Finance & Ops Sync
**Date:** January 14, 2025
**Attendees:** Rachel Stein (CFO), Lina Cho (Finance Analyst), Sam Reyes (CEO)
**Transcript ID:** gong_20250114_0900_finance

[00:00:05] **Rachel Stein:** Okay, we’re recording. Happy New Year, everyone. Let’s dive in. Sam, I know you’ve got a board deck draft due by Friday for the preliminary 2024 wrap-up. Lina, did we get the final ARR numbers for December 31st?

[00:00:21] **Lina Cho:** Yeah, we just finished the reconciliation. The `nexus-analyst-demo.acme.arr_snapshot` is showing we ended the year at $33.1M. It’s a little lower than the Salesforce forecast of $33.5M because we had that late downgrade from the group that was previously on the Enterprise POC.

[00:00:44] **Sam Reyes:** Wait, $33.1M? I thought Marcus was saying we’d clear $33.5M easily. Is this a data lag issue or did a deal actually slip?

[00:00:54] **Lina Cho:** It’s not a slip, it’s a mapping thing. Salesforce counts the "contract signed" date, but for the `arr_snapshot` table, I’m looking at `fact_subscriptions` where `is_current` is true and `start_date` is on or before the snapshot date. We had about $400k in "signed" deals that don't actually kick off until January 15th for implementation.

[00:01:18] **Rachel Stein:** This is going to be a recurring theme. Sam, we need to be clear with the board: our "Bookings" aren't "ARR" on day zero if the service period hasn't started. Lina, can you make sure the bridge shows that?

[00:01:32] **Lina Cho:** Totally. I’m building the waterfall now in Looker. The bridge from $28M in Q3 to $33M in Q4 is mostly driven by the expansion in the Business tier. SMB is basically flat.

[00:01:45] **Sam Reyes:** What’s the NRR looking like on that $33M?

[00:01:48] **Lina Cho:** It’s hovering around 106%. Actually, wait, let me look at the `nrr_trailing_12` table... yeah, it’s 106.8%. But Rachel, we need to talk about how we’re calculating this. Right now, Rajiv has the dbt model set up to cohort everyone who was a paid customer 12 months ago. If they churned, they stay in the denominator with an end MRR of zero.

[00:02:12] **Rachel Stein:** Good. That’s the right way. I’ve seen some startups try to do an inner join there to exclude churned customers and it just inflates the number. We need the real NRR.

[00:02:24] **Sam Reyes:** Agreed. Let’s not play games with the metrics. By the way, Lina, did you see my note about the Expensify sync? It’s double-counting the Amsterdam office rent again.

[00:02:35] **Lina Cho:** Ugh, Expensify. I’ll look at it after this. It’s probably hitting the `fact_invoices` table incorrectly because of the currency conversion for the EMEA office.

[00:02:46] **Rachel Stein:** Okay, next item. Marcus wants to change how he’s reporting bookings by channel. He’s saying the "referral" channel is under-represented because of how the SDRs are tagging things in Salesforce.

[00:02:59] **Lina Cho:** I can only report what’s in `bookings_attribution`. If the `first_touch_channel` is "outbound" because an SDR touched it first, that’s what the query is going to return. If Marcus wants to change the attribution logic, he needs to talk to Jorge Martinez in RevOps. I’m just pulling from the flat table.

[00:03:18] **Sam Reyes:** Let's keep it simple for now. Use the `bookings_attribution` table as the source of truth. If Marcus wants a "Manager Override" column, he can fund the engineering time to build it. (Laughter)

---

### Meeting Transcript: Q1 Board Prep & Reconciliation
**Date:** March 25, 2025
**Attendees:** Rachel Stein (CFO), Lina Cho (Finance Analyst), Marcus Webb (VP Sales)
**Transcript ID:** gong_20250325_1030_finance

[00:00:12] **Rachel Stein:** Okay, we’re two weeks out from the board meeting. Marcus, glad you could join. We’re looking at the Q1 preliminary numbers. Lina, what’s the current ARR?

[00:00:24] **Lina Cho:** We are at $35.2M as of this morning’s refresh of `nexus-analyst-demo.acme.arr_snapshot`.

[00:00:32] **Marcus Webb:** Wait, $35.2M? My dashboard in Salesforce says $36.8M. That’s a massive gap. Where is that $1.6M going?

[00:00:41] **Lina Cho:** Marcus, we've talked about this. Salesforce includes "Committed" contracts that haven't passed the implementation trigger. Also, the `arr_snapshot` doesn't include the "Free" tier. I noticed about $200k of that "missing" money is actually customers who are in a "Paused" status in `dim_customers`. Specifically, Tamarind Group (cust_000706) went to paused status in January. Salesforce still shows them as an active opportunity because the contract hasn't technically been canceled by legal.

[00:01:15] **Marcus Webb:** Tamarind is just a temporary budget freeze. They’ll be back in Q2. We shouldn't be dinging our ARR for a pause.

[00:01:23] **Rachel Stein:** If they aren't paying, it's not ARR. It’s as simple as that. We have to be conservative for the board. Lina, keep them in the "Paused" bucket, don't count them in the $35.2M.

[00:01:36] **Lina Cho:** Also, Marcus, we have a bunch of PLG conversions in the Pro tier—like Driftwood Media (cust_000702) and Pebble Digital (cust_000705). Those are showing up in `fact_subscriptions` as new revenue, but they aren't in your `bookings_attribution` table because an AE didn't lead the deal.

[00:01:54] **Marcus Webb:** That’s another problem. My team is doing the work to warm those guys up, then they just swipe a credit card and I don’t get the booking credit?

[00:02:04] **Rachel Stein:** We aren't changing the comp plan mid-quarter, Marcus. Let's focus on the reconciliation. Lina, why is the `dim_customers.current_mrr_usd` different from the `fact_subscriptions` MRR for some accounts?

[00:02:18] **Lina Cho:** It’s intraday drift. `dim_customers` gets updated by a sync from the production DB that happens every few hours, but `fact_subscriptions` is tied to the dbt nightly run. I always use `fact_subscriptions` for the ARR bridge because it’s the historical record. If we use the dimension table, the numbers change while we're looking at them.

[00:02:40] **Rachel Stein:** Okay, lesson for everyone: `arr_snapshot` is the canonical table. Do not query `dim_customers` for financial reporting.

[00:02:50] **Lina Cho:** Exactly. I’ll send out the SQL snippet for the NRR cohort again. People keep trying to do their own math in Excel and it's making my life difficult.

[00:03:02] **Marcus Webb:** Fine. But I need a slide explaining the "AE-influenced" PLG revenue. If we're at $35M but my team only gets credit for $30M, it looks like we're underperforming.

[00:03:14] **Sam Reyes:** (Joining late) Hey guys. Just saw the $35M number. That’s great. Are we still on track for $40M by year-end?

[00:03:21] **Rachel Stein:** If we can keep churn under control. We’re seeing some noise in the "Business" tier. Kestrel Networks (cust_000708) is looking shaky.

[00:03:32] **Marcus Webb:** Kestrel is fine. They just had a CFO change. I’m on it.

---

### Meeting Transcript: Series B Post-Mortem & Q3 Forecast
**Date:** September 18, 2025
**Attendees:** Rachel Stein (CFO), Lina Cho (Finance Analyst), Sam Reyes (CEO)
**Transcript ID:** gong_20250918_1400_finance

[00:00:10] **Sam Reyes:** Alright, the wire hit. $80M in the bank. Series B is officially done. Great job, Rachel. Investors loved the NRR story.

[00:00:18] **Rachel Stein:** Thanks, Sam. But now the real pressure starts. They’re going to be looking at our efficiency metrics every month now. Lina, how are we looking for the end of Q3?

[00:00:30] **Lina Cho:** We’re at $37.4M ARR. The growth is steady, but the Kestrel Networks (cust_000708) churn finally hit the books. That was a $125k ARR loss. They officially moved to "churned" status in the `dim_customers` table last week.

[00:00:48] **Sam Reyes:** Damn. Marcus said he had that one under control. What was the reason?

[00:00:53] **Lina Cho:** "Budget cut" was the reason code Jorge put in the CRM. It shows up in `fact_opportunities` as a "Loss Reason." It’s a bummer because their engagement was actually pretty high—they were in the `utilization_band` > 0.8 in the `account_health` mart.

[00:01:11] **Rachel Stein:** It happens. But look at the bright side, Marigold Health (cust_000701) just expanded. They’re up to 300 seats on the Enterprise plan. That’s $180k ARR right there.

[00:01:23] **Lina Cho:** Yeah, the Enterprise segment is really carrying us right now. Business is a bit of a grind. By the way, Rachel, I’m cleaning up the `nrr_trailing_12` table for the post-funding audit. I found a bug in the old query where someone—I think it was before I joined—was multiplying `bookings_acv_usd` by 12 to get ARR.

[00:01:45] **Rachel Stein:** Oh god. No. ACV is *already* annualized. Please tell me we didn't report that to the VCs.

[00:01:52] **Lina Cho:** No, I caught it in the VDR prep. I’ve been using the subscription-level MRR * 12 instead. It’s much more accurate. But if you see some old 2024 reports with crazy high numbers, that’s why.

[00:02:06] **Sam Reyes:** Good catch. This is why we pay you the big bucks, Lina. Speaking of which, when is your vacation?

[00:02:13] **Lina Cho:** Not until October. I need to get the Q3 close done first. I’m also trying to figure out why the "First Touch Channel" for Onyx Robotics (cust_000704) is showing as "Organic" when I know for a fact Tom Becker did an outbound cold call.

[00:02:31] **Rachel Stein:** It’s probably a cookie thing. They might have visited the site months ago on an organic search before Tom ever reached out.

[00:02:40] **Lina Cho:** That’s the problem with `bookings_attribution`. It’s very sensitive to that `first_touch_channel`. I’m going to add a secondary column for "Last Touch" just so Marcus stops yelling at me.

[00:02:53] **Sam Reyes:** Whatever keeps the peace. Rachel, did we finalize the headcount budget for Eng? Priya is asking for 5 more hires.

[00:03:02] **Rachel Stein:** I told her we wait until the Q3 actuals are in. If we hit $38M, she gets her hires. If not, we wait.

---

### Meeting Transcript: Churn Deep Dive & 2026 Planning
**Date:** February 12, 2026
**Attendees:** Rachel Stein (CFO), Lina Cho (Finance Analyst), Elena Volkov (VP CS)
**Transcript ID:** gong_20260212_1100_finance

[00:00:15] **Rachel Stein:** Okay, let’s talk about the elephant in the room. Beacon Studios (cust_000287). They churned on the 18th. That’s $116k out the door. Elena, what happened?

[00:00:28] **Elena Volkov:** It wasn’t us, Rachel. It was a parent company consolidation. They got acquired, and the new owners are standardized on a legacy competitor. Their Value Realization Score—or well, the engagement metrics in `account_health`—were perfect. They were "Healthy Expansion" right up until the day they gave notice.

[00:00:49] **Lina Cho:** It’s really hurting our NRR for the quarter. We were sitting at 108%, and this drop pulls us down to about 105.5%.

[00:00:58] **Rachel Stein:** (Sigh) This is why we need more than just "engagement" to predict churn. Lina, you were talking about that VRS score?

[00:01:07] **Lina Cho:** The Value Realization Score? Yeah, it’s still just a draft spec. Dan Lee and the product team haven't built the `vrs_band` columns yet. For now, we only have `account_health_status`. Honestly, for Enterprise, the only thing that matters in that table is the `has_uncollectible_recent` flag. The utilization rules don't even apply to them because they have unlimited seats in their contracts.

[00:01:34] **Elena Volkov:** Which is weird, because we still track their active users.

[00:01:38] **Lina Cho:** We track it, but the `utilization_band` in the mart is hard-coded to `NULL` for the Enterprise tier. I’ve been trying to get Rajiv to change the dbt logic so we can at least see a trend line, but he’s buried in the CRM migration work with Jorge.

[00:01:55] **Rachel Stein:** Let’s focus on the ARR bridge for the board. We started 2026 at what, $38.2M?

[00:02:02] **Lina Cho:** Yeah, and with the Beacon Studios loss and the new Ember Industries (cust_000711) deal, we’re currently at $39.1M. We finally broke the $39M ceiling.

[00:02:15] **Rachel Stein:** That’s a milestone. Sam’s going to be happy about that. But $39M is also where the tax implications get complicated for our international entities. Lina, I need you to run a report on `fact_invoices` by `region` for the last 12 months. I need to see exactly how much revenue is hitting the Amsterdam entity versus SF.

[00:02:38] **Lina Cho:** I can do that. Just a heads up, the `region` column in `dim_customers` is sometimes "EMEA" and sometimes "Europe". I have to do a `CASE` statement to clean it up.

[00:02:49] **Rachel Stein:** Just fix it in the dbt model, Lina. Don't do it in the query every time.

[00:02:54] **Lina Cho:** I'll try, but I don't have write access to the `marts` folder. Only Rajiv and Nina do.

[00:03:01] **Rachel Stein:** I’ll talk to Priya. We need Finance to have more control over the reporting layer.

---

### Meeting Transcript: Final Q1 2026 Reconciliation
**Date:** May 4, 2026
**Attendees:** Rachel Stein (CFO), Lina Cho (Finance Analyst), Sam Reyes (CEO), Marcus Webb (VP Sales)
**Transcript ID:** gong_20260504_0830_finance

[00:00:05] **Rachel Stein:** Alright, this is the big one. We’re finalizing the numbers as of today, May 4th. This is the snapshot we’re taking to the board next week. Lina, give us the final verdict.

[00:00:18] **Lina Cho:** Okay, I’m looking at `nexus-analyst-demo.acme.arr_snapshot` for today. We are at exactly $39,042,000.

[00:00:30] **Sam Reyes:** $39M. We did it. Barely, but we did it.

[00:00:34] **Marcus Webb:** Wait, I have two more deals that closed on Friday afternoon. Cobalt Systems (cust_000700) and Marigold Health (cust_000701) both expanded their seat counts. Did those make it in?

[00:00:46] **Lina Cho:** Cobalt is in, they moved to 80 seats on the Business plan. That’s $11,920 MRR. Marigold is also in, they’re at 300 seats. The MRR is $15,000.

[00:00:59] **Marcus Webb:** What about Onyx Robotics? They were supposed to add 100 more seats.

[00:01:04] **Lina Cho:** That one is still showing as 500 seats in `fact_subscriptions`. The `is_current` flag hasn't flipped for the new version of the subscription yet. Did they sign the order form?

[00:01:15] **Marcus Webb:** Tom said it was signed at 4 PM on Friday.

[00:01:19] **Lina Cho:** Okay, so it’s probably stuck in the "Processing" state in the billing system. It won't show up in our BigQuery tables until the next sync, which is in about two hours. I can manually adjust the slide for the board, but the "source of truth" table will say $39M.

[00:01:38] **Rachel Stein:** Leave it at $39M. If we start adding "verbal commits" or "pending processing" to the board deck, we lose credibility. We’ll count Onyx for the Q2 bridge.

[00:01:50] **Sam Reyes:** I agree. $39M is a clean number. What’s the NRR on that?

[00:01:55] **Lina Cho:** 107.2%. The expansion from Cobalt and Marigold really helped offset the Beacon Studios hit. And the GRR—Gross Retention—is holding steady at 94%.

[00:02:10] **Rachel Stein:** 94% GRR is solid. It means our core customer base isn't going anywhere; we just need to get better at the upsell. Lina, what's the deal with the "monitoring" status accounts? I see a lot of Pro tier customers in that bucket.

[00:02:26] **Lina Cho:** Yeah, we recalibrated the `is_engaged` logic in Q4. Now, to be "engaged," you need at least 3 active users and 10 successful workflow runs in the last 28 days. A lot of the Pro customers like Pebble Digital (cust_000705) are only using 1 or 2 users, so they’re getting flagged as "monitoring." It doesn't mean they're going to churn, they're just small teams.

[00:02:51] **Marcus Webb:** We should probably have a different engagement threshold for the Pro tier. 3 users is half their seat count for some of these guys.

[00:03:00] **Rachel Stein:** Let’s worry about that later. For now, Lina, please double-check the `fact_invoices` status. We had some trouble with uncollectible invoices from Tamarind Group (cust_000706) last month. Are they still showing as "at_risk" in the health mart?

[00:03:17] **Lina Cho:** Yes, anyone with an uncollectible invoice over $5k gets the `critical` or `at_risk` tag automatically. Tamarind is still paused anyway, so it’s not hitting our active ARR.

[00:03:30] **Sam Reyes:** Okay. Great job everyone. Rachel, let's sync on the "Cash vs. Recognized" slide later this afternoon. I want to make sure we're explaining the deferred revenue correctly.

[00:03:42] **Rachel Stein:** Sounds good. Lina, don’t forget to check those Expensify receipts before you leave today. I'm seeing a $2k "team dinner" from Marcus that has no description.

[00:03:54] **Marcus Webb:** That was the Cobalt closing dinner! I’ll add the note now.

[00:03:58] **Lina Cho:** (Laughs) I’ll believe it when I see the PDF. See you guys.

---

### Internal Note: SQL Snippet for Finance Syncs
**To:** Finance Team
**From:** Lina Cho
**Subject:** Proper way to query the ARR Waterfall

Hey guys, please stop querying `dim_customers.current_mrr_usd`. It’s too noisy. Use this instead for any board-level reporting:

```sql
-- Canonical ARR by Tier (2026-05-04)
SELECT 
    plan_tier,
    SUM(mrr_usd) * 12 as arr_usd,
    COUNT(DISTINCT customer_id) as n_customers
FROM `nexus-analyst-demo.acme.fact_subscriptions`
WHERE is_current = TRUE
  AND plan_tier != 'Free'
GROUP BY 1
ORDER BY 2 DESC;
```

Also, remember that `bookings_acv_usd` in `bookings_attribution` is ALREADY annualized. Do NOT multiply it by 12. If you do, you'll report that we have $400M ARR and Rachel will have a heart attack.

And one more thing: if you're looking for the PLG conversions (people who sign up for Pro without talking to an AE), they will NOT be in the `bookings_attribution` table. You have to find them by looking for `change_type = 'new_subscription'` in `fact_subscriptions` where the customer doesn't have a corresponding `opportunity_id` in the CRM.

-Lina

---

### Meeting Transcript: Bi-Weekly Finance Sync (Ad-hoc)
**Date:** April 20, 2026
**Attendees:** Rachel Stein (CFO), Lina Cho (Finance Analyst)
**Transcript ID:** gong_20260420_1500_finance

[00:00:02] **Rachel Stein:** Hey Lina, quick one. I’m looking at the `account_health` table and I see Harbor Dynamics (cust_000713) is marked as "stable" but their `utilization_band` is 0.95. Why aren’t they in "healthy_expansion"?

[00:00:18] **Lina Cho:** Let me check the logic. (Sound of typing) Ah, okay. To be "healthy_expansion," they need to be both `engaged` AND have a `utilization_band` >= 0.6. Harbor Dynamics is definitely engaged, but their `account_health_status` is being overridden because they have an open P1 support ticket that’s been open for more than 48 hours.

[00:00:43] **Rachel Stein:** That makes sense. We don't want to try to upsell someone who’s currently dealing with a major bug. Who’s the CSM on that?

[00:00:51] **Lina Cho:** Marco Silva. It looks like it’s a `STEP_TIMEOUT` error on one of their main SAP integrations. Priya’s team is looking at it.

[00:01:02] **Rachel Stein:** Okay. Also, did we ever resolve that issue with the `fact_workflow_runs` table? Rajiv was saying the `triggered_by` column was coming in null for half the rows.

[00:01:14] **Lina Cho:** It’s still an issue for scheduled jobs. Webhook triggers are fine. It doesn’t affect the revenue numbers, but it’s making it hard for Marcus to see which users are actually "power users."

[00:01:28] **Rachel Stein:** As long as the `customer_id` is there, we can still bill them. That’s all I care about for now. Oh, and Lina, the tax filing for the Amsterdam entity is due on the 15th. Did we get the `fact_invoices` export to the Dutch auditors?

[00:01:45] **Lina Cho:** Sent it this morning. I had to manually filter out all the "Pro" accounts because they are all billed through the US entity regardless of region. It’s only the Business and Enterprise accounts in EMEA that hit the Amsterdam books.

[00:02:01] **Rachel Stein:** Why is that?

[00:02:03] **Lina Cho:** Stripe setup. When we launched the Pro self-serve tier, we just pointed everything to the US account to save time. It’s a mess to untangle now.

[00:02:14] **Rachel Stein:** Add it to the list for 2027. (Laughter)

---

### Meeting Transcript: Sales & Finance Alignment
**Date:** November 10, 2025
**Attendees:** Rachel Stein (CFO), Lina Cho (Finance Analyst), Marcus Webb (VP Sales), Jorge Martinez (RevOps)
**Transcript ID:** gong_20251110_0900_finance

[00:00:10] **Marcus Webb:** Look, I’m just saying the `bookings_attribution` table is missing at least four deals from October.

[00:00:18] **Jorge Martinez:** Marcus, I checked the CRM. Those deals are still in "Closed Won" but the `closed_won_at` timestamp is in November because the legal review took forever.

[00:00:29] **Lina Cho:** And that’s why they aren't in the October snapshot. The query is `WHERE closed_won_at BETWEEN '2025-10-01' AND '2025-10-31'`.

[00:00:40] **Marcus Webb:** But we hit our number! If I tell the board we missed October but crushed November, it just looks like we don't know how to forecast.

[00:00:49] **Rachel Stein:** Marcus, this is why we use "Bookings" for your commission and "ARR" for the board. The board understands timing shifts. What they don't understand is why we would report a deal that wasn't legally finished.

[00:01:03] **Marcus Webb:** Fine. What about the "partner" channel? I see Marigold Health (cust_000701) is credited to the partner channel, but Sarah Chen did all the work.

[00:01:15] **Jorge Martinez:** The `first_touch_channel` was "partner" because they came in through the AWS Marketplace referral. Sarah gets the commission, but the attribution stays with the partner. That’s how we track ROI on the partnership program.

[00:01:28] **Lina Cho:** It’s actually helpful for me, Marcus. It helps me justify the partner spend to Rachel.

[00:01:34] **Rachel Stein:** Exactly. If I see Sarah Chen is doing all the work but the leads are coming in for free from partners, I’m going to want to hire more partners!

[00:01:45] **Marcus Webb:** (Grumbles) I guess. Hey, Lina, can you run a report on the "churn reason" for the last six months? I want to see how many were "product fit" vs "budget."

[00:01:58] **Lina Cho:** I can, but the data is pretty thin. Most of the time, the AEs just leave it as "Other." Juniper Collective (cust_000712) was the only one that specifically mentioned "product fit" in the notes.

[00:02:12] **Marcus Webb:** I’ll talk to the team about being more diligent with the reason codes.

[00:02:17] **Rachel Stein:** Thanks, Marcus. Jorge, stay on the line, I want to talk about the Stripe integration for the new "Enterprise Plus" tier.

[00:02:25] **Lina Cho:** Wait, "Enterprise Plus"? Nobody told me about a new tier.

[00:02:30] **Rachel Stein:** It’s just a draft, Lina. Don’t update the `dim_plans` table yet.

[00:02:35] **Lina Cho:** (Sighs) Okay. I'll stick to what's in the warehouse.

[00:02:40] **Marcus Webb:** See ya.

---

### End of Document