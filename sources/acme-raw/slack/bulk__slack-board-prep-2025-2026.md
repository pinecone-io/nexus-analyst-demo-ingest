---
title: "Slack #board-prep channel archive — 2025-2026"
source_url: "internal://acme/slack-board-prep-2025-2026"
license: "synthetic-demo"
attribution: "Synthetic content, Acme Inc internal demo. Acme Inc is a fictitious company."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

### #board-prep

**rachel.stein** [2025-01-14 09:12:00]:
Alright team, Q1 board meeting is set for Feb 15th. We need to start pulling the FY24 wrap-up and the Q1 forecast. @lina.cho let's start with the ARR walk. @marcus.webb I need the pipeline gap analysis by end of week.

**marcus.webb** [2025-01-14 09:15:22]:
On it. Just a heads up, the CRM data is a bit messy after the migration. @jorge.martinez is still cleaning up some of the duplicates.

**lina.cho** [2025-01-14 09:18:45]:
@rachel.stein I’ll have the ARR walk ready by tomorrow. I’m pulling directly from `nexus-analyst-demo.acme.arr_snapshot` so we don't have the drift issues we had last time with the live production view.

**rachel.stein** [2025-01-14 10:05:11]:
Perfect. Last thing I want is Sam getting grilled because the numbers in the deck don't match the monthly report he sent in December.

---
**lina.cho** [2025-01-15 14:20:10]:
@rachel.stein @sam.reyes Draft ARR slide is in the Google Drive. Total ARR at $38.8M as of Dec 31.
> **marcus.webb**: Wait, Lina, why $38.8M? Looker was showing $42M on Friday.
> **lina.cho**: Marcus, Looker was looking at the PDT which was caching the old logic. That $42M included some of the "Paused" accounts and didn't account for the Tamarind Group downgrade. We are using `arr_snapshot` as the source of truth. It's ~$39M.
> **marcus.webb**: $3M is a big delta. The board is going to ask why we "missed" the $40M mark.
> **sam.reyes**: We didn't miss it, we just didn't hit it yet. Precision matters more than the ego of hitting 40. Keep it at 39M.

---
**jasmine.park** [2025-01-20 11:30:45]:
Do we have the final breakdown of bookings by channel for Q4? I need to show the ROI on the LinkedIn spend vs. the partner channel.
> **lina.cho**: Check `acme.bookings_attribution`.
> **jasmine.park**: Quick question on the ACV column—is `bookings_acv_usd` monthly or annual? Do I need to multiply by 12?
> **lina.cho**: NO. It is already annual. Please do not multiply it. We had that disaster in Q2 where we reported 12x the actual revenue to the board and had to send a correction email. Never again.

---
**rachel.stein** [2025-01-25 16:45:00]:
@here Who is handling the deck printing and binding? I want physical copies on the table.
> **lina.cho**: I can do it, but I'll need the final deck by Feb 13th morning.
> **rachel.stein**: Let's aim for the 12th. I want to do a full walkthrough with Sam on the 13th.
> **sam.reyes**: I'm traveling on the 12th. Can we do the rehearsal on the 11th?
> **rachel.stein**: Okay, shifting everything up. 

---
**lina.cho** [2025-02-02 10:15:33]:
@rachel.stein Quick check on NRR methodology. Are we doing the trailing-12 fixed-cohort?
> **rachel.stein**: Yes. Make sure the methodology footnote is there. The board gets confused if we swap between monthly and trailing-12.
> **lina.cho**: Got it. Just so you know, the NRR is looking at 1.07. If I use an inner join (dropping churns), it looks like 1.20, but I’m doing the honest version with the left join so churned customers count as $0.
> **rachel.stein**: Good. Stay honest. If they ask about the 1.07, we point to the Kestrel Networks churn ($10k MRR loss in Nov).

---
**sam.reyes** [2025-02-05 08:30:12]:
Does anyone have the "Accounts at Risk" list for the board? I want to be proactive.
> **marcus.webb**: I’m pulling it from the account health mart. `acme.account_health`.
> **lina.cho**: Sam, I just updated the logic. "Critical" now includes anyone with an uncollectible invoice or utilization < 20%. 
> **marcus.webb**: Lina, that's too aggressive. Cobalt Systems (cust_000700) is at 18% utilization because they are still in implementation. They aren't "Critical."
> **lina.cho**: The logic is the logic. You can add a "Notes" column in the slide to explain the implementation phase, but the data flag is staying.

---
**rachel.stein** [2025-02-12 19:00:15]:
Deck is 90% done. Jasmine, the fonts on slide 14 are different from the rest of the deck. Can you fix?
> **jasmine.park**: On it. Google Slides is a nightmare with the Acme-Brand font.

---
**lina.cho** [2025-03-20 13:12:00]:
Starting the Q2 prep early. @marcus.webb, any early visibility on the Marigold Health (cust_000701) expansion?
> **marcus.webb**: Looks good. Sarah is confident they'll add another 100 seats by May.
> **lina.cho**: Okay, I won't bake it into the "committed" forecast yet but I'll put it in "upside."

---
**rachel.stein** [2025-04-05 11:00:22]:
We need to add a slide on Gross Retention (GRR) this time. The board asked about it in the breakout session last time.
> **lina.cho**: GRR is ~0.94. I'll add the calc: it's basically NRR but we cap the expansion credit. 
> **sam.reyes**: 0.94 is solid. Let's lead with that for the CS section. @elena.volkov you good with that?
> **elena.volkov**: Yeah, it shows our base is sticky even if expansion slowed down in Q1.

---
**jasmine.park** [2025-04-10 15:45:10]:
@lina.cho Can we add a VRS (Value Realization Score) slide? I want to show how much "value" we're creating for customers.
> **lina.cho**: No, Jasmine. VRS is still a parked draft spec. Rajiv and David haven't built the `vrs_band` columns in the warehouse yet. 
> **jasmine.park**: Can we just use the draft numbers from the spreadsheet?
> **lina.cho**: No. If it's not in the warehouse, it's not board-ready. Use "Engagement %" as a proxy for now. (≥3 users, ≥10 runs).

---
**rachel.stein** [2025-05-02 09:20:00]:
Board meeting is in 2 weeks. Status check.
> **lina.cho**: ARR walk is done. NRR is calculated.
> **marcus.webb**: Pipeline looks a bit thin for Q3, I’m working on the talk track for that.
> **sam.reyes**: What's the story on Tamarind Group (cust_000706)? 
> **marcus.webb**: They're "Paused." Procurement issues on their end. Sarah is on it.

---
**lina.cho** [2025-05-05 16:12:44]:
Hey @david.kim, I’m seeing a weird spike in `fact_workflow_runs` for Onyx Robotics (cust_000704). Did they 10x their volume overnight?
> **david.kim**: Let me check... yeah, they deployed a new loop that's hitting a webhook every 5 seconds. It's successful, but it's going to blow out their quota.
> **marcus.webb**: Leave it. That's a great "expansion" story for the board. "Customer finds new use case, surges usage."
> **rachel.stein**: Just make sure they aren't going to get a $50k overage bill they didn't expect. That leads to churn, not expansion.

---
**rachel.stein** [2025-07-10 10:00:00]:
**SERIES B PREP STARTS NOW.** This is the big one. We need the Q3 board deck to be flawless.
> **sam.reyes**: We're targeting $80M total raise. The numbers need to show the efficient growth engine.
> **lina.cho**: I'm tightening up the `bookings_attribution` logic. I want to make sure we're not double-counting the partner deals where an SDR was also involved.
> **jasmine.park**: @lina.cho, are you using the `first_touch_channel`?
> **lina.cho**: Yes. It's the cleanest way to show the board where the revenue is actually coming from.

---
**marcus.webb** [2025-07-15 14:30:15]:
Lina, is the Enterprise ARR really only $6M? I feel like we've closed more than that.
> **lina.cho**: Check `dim_customers.current_plan_tier`. A lot of your "Enterprise" deals are actually "Business" tier customers who just have high seat counts but haven't signed the custom SLA/paperwork yet.
> **marcus.webb**: We need to move them. The board loves seeing the Enterprise mix grow.

---
**lina.cho** [2025-08-01 11:20:33]:
@rachel.stein I found a bug in the NRR calc from Q1. I was accidentally using `acme.marts.finance.nrr_trailing_12` (the old dbt folder path) which wasn't updating. The correct table is `nexus-analyst-demo.acme.nrr_trailing_12`. 
> **rachel.stein**: Did the number change?
> **lina.cho**: It went from 1.07 to 1.06. 
> **rachel.stein**: Okay, 1% isn't a dealbreaker, but let's make sure we use the flat table path from now on. No more nested marts in the queries.

---
**sam.reyes** [2025-08-10 09:00:00]:
Who's handling the board dinner for the Series B celebration?
> **rachel.stein**: Jasmine's team is on it. We've got a private room at Cotogna. 
> **jasmine.park**: Does anyone know if the lead investor from the new firm has any allergies?
> **sam.reyes**: I'll check. Pretty sure he's vegan.

---
**rachel.stein** [2025-10-15 13:45:00]:
Post-Series B board meeting coming up. We need to show how we're deploying the capital. @marcus.webb I need the hiring plan vs. actual for the sales team.
> **marcus.webb**: We're behind on AE hiring. The market is tight. 
> **rachel.stein**: We need to explain that. The board will want to know why we have $20M in the bank and aren't scaling the head-count faster.

---
**lina.cho** [2025-11-05 10:10:12]:
@here Just saw Kestrel Networks (cust_000708) officially moved to "Churned" in the warehouse. $10,430 MRR loss. 
> **marcus.webb**: Yeah, budget cuts. Nothing we could do.
> **lina.cho**: I'm updating the "At Risk" slide. We have about $400k in ARR exposure in the "Critical" category right now. Mostly Business tier companies with low utilization.

---
**jasmine.park** [2025-11-20 16:30:00]:
Lina, for the marketing slide, can I get the top 5 campaigns by attributed revenue? 
> **lina.cho**: Use `fact_marketing_touches` joined with `bookings_attribution`. But remember, it only counts AE-led deals. The self-serve Free->Pro stuff doesn't show up there.
> **jasmine.park**: That's fine. The board cares about the "Big Whale" acquisition anyway.

---
**rachel.stein** [2025-12-05 09:15:00]:
Q4 Board Prep. Let's make this one quick. I want everyone to have their slides drafted by the 15th so we can enjoy the holidays.
> **lina.cho**: I’ll have the full 2025 summary ready. ARR should finish right around $39M.

---
**lina.cho** [2026-01-10 14:22:00]:
Happy New Year. Back at it. @marcus.webb, I’m seeing some weirdness with Juniper Collective (cust_000712). They're showing as churned but they still have 12 active users?
> **lina.cho**: Nevermind, I see it. They downgraded to the Free tier. Logic says downgrade to Free = Churn for ARR purposes.
> **marcus.webb**: Correct. They're dead to us until they pay again.

---
**rachel.stein** [2026-02-01 11:30:45]:
@here Bad news. Beacon Studios (cust_000287) is churning. $9,685 MRR.
> **sam.reyes**: What happened? They were one of our best Case Studies.
> **elena.volkov**: Parent company merger. They're being forced onto the parent company's internal tool. Nothing to do with our product.
> **rachel.stein**: We need a dedicated slide for this. It’s a "Non-Controllable Churn" narrative. @lina.cho, make sure the NRR calc for Q1 reflects this correctly.

---
**lina.cho** [2026-02-15 10:00:00]:
Reconciling the Feb numbers for the board. 
Looker: $39.5M ARR
`arr_snapshot`: $39.1M ARR
Difference is the Tamarind Group "Paused" status. I am sticking with the $39.1M.
> **rachel.stein**: Agreed. Don't let Marcus talk you into the $39.5M.

---
**jasmine.park** [2026-03-05 15:20:10]:
@lina.cho I’m trying to run this query for the board deck but getting an error: `SELECT * FROM acme.marts.cs.account_health`.
> **lina.cho**: Jasmine, we’ve talked about this. The dataset is FLAT. Use `nexus-analyst-demo.acme.account_health`. No sub-folders in BigQuery.
> **jasmine.park**: Ah, right. Sorry.

---
**marcus.webb** [2026-03-12 09:45:33]:
@lina.cho for the "Healthy Expansion" list—Onyx Robotics (cust_000704) is showing as "Stable" not "Healthy Expansion." Why?
> **lina.cho**: Their utilization is 0.58. The rule for "Healthy Expansion" is utilization ≥ 0.6. They are literally 2% away.
> **marcus.webb**: Can we round up?
> **lina.cho**: No.

---
**rachel.stein** [2026-04-05 17:00:00]:
Q1 2026 Board Meeting Prep. 
Sam wants to focus on "Efficient Enterprise Growth." 
@lina.cho, I need a chart showing Enterprise ARR growth vs. Business ARR growth over the last 4 quarters.
@marcus.webb, I need the "Win Rate" against Tray.io for the last 6 months.

**marcus.webb** [2026-04-05 17:05:00]:
Win rate data is in the CRM under "Loss Reason." @jorge.martinez can you pull the report?
> **jorge.martinez**: I'll have it by EOD.

---
**lina.cho** [2026-04-10 11:22:15]:
@rachel.stein I’m looking at the `nrr_trailing_12` table. The cohort from April 2025 is actually performing better than I thought. 1.09 NRR. 
> **rachel.stein**: That’s a great signal. Why the jump?
> **lina.cho**: Marigold Health expansion and Cobalt Systems finally getting past implementation. 
> **rachel.stein**: Put that on slide 4. That’s the "Scaling the Business" proof point.

---
**sam.reyes** [2026-04-15 08:30:00]:
Who's bringing the physical decks to the meeting on Thursday?
> **lina.cho**: I have them. 10 copies, spiral bound, color. 
> **rachel.stein**: Did you include the Appendix with the full customer list?
> **lina.cho**: Yes, all 745 active customers are in the back.
> **sam.reyes**: 745? I thought we were at 800.
> **lina.cho**: 800 total in the table, but ~55 are churned or paused. 745 active paying.
> **sam.reyes**: Right. Let's make sure the "800+ total customers" line from marketing doesn't conflict with the "745 active" line in the finance section.
> **jasmine.park**: I'll change the marketing slide to say "800+ companies have used Acme."
> **rachel.stein**: Better.

---
**lina.cho** [2026-04-20 14:00:10]:
Final check on the "At Risk" list for Marcus:
- Tamarind Group (cust_000706): Paused, $8k MRR
- Sable Analytics (cust_000710): Low utilization (15%)
- Harbor Dynamics (cust_000713): Open P1 ticket for >72 hours
> **marcus.webb**: Harbor Dynamics is just a feature request they flagged as P1. It’s not a real risk.
> **lina.cho**: It triggered the flag. Elena, is your team on it?
> **elena.volkov**: Yeah, Marco is on a call with them now. We'll downgrade the priority today so the flag clears before the board sees it.

---
**rachel.stein** [2026-04-25 10:15:00]:
Rehearsal in the main conference room at 1 PM. 
Sam, Rachel, Marcus, Elena. 
Lina, stay by your phone in case we need a quick data pull to answer a "what if" question.

**lina.cho** [2026-04-25 10:18:00]:
I’ll be in the "Data Cave" (my desk). Good luck everyone.

---
**sam.reyes** [2026-04-26 18:30:22]:
Board meeting went great. They loved the focus on Enterprise. That chart about the April 2025 cohort was the highlight. 
Thanks team. 

**rachel.stein** [2026-04-26 18:35:10]:
Great job everyone. Now let's go hit the Q2 targets so the next one is even better. 

---
**lina.cho** [2026-05-02 11:00:00]:
@here archiving the Q1 folder. Starting the May monthly report. 
Quick note for the records: Total ARR as of May 1 is $39.2M. 
`nexus-analyst-demo.acme.arr_snapshot` is updated and synced.

**marcus.webb** [2026-05-02 11:05:00]:
Only $39.2M? I have three deals closing today. 
> **lina.cho**: They'll be in the June report, Marcus. The snapshot is a snapshot. 
> **marcus.webb**: 🙄

---
**lina.cho** [2026-05-03 09:15:00]:
@rachel.stein, one last thing for the post-meeting notes. The board member from the Series B firm asked about "VRS" again. Do we want to un-park that project for Q3?
> **rachel.stein**: Let's talk to Dan and Priya. If we can get it into the warehouse with a clean methodology, yes. If it's going to be another "manual spreadsheet nightmare," then no.
> **lina.cho**: Copy that. I'll check with Rajiv on the dbt workload.

**rajiv.menon** [2026-05-03 09:20:00]:
I heard my name. If we’re doing VRS, I need a clear spec on what "Value" means. Is it workflow runs? Seat utilization? Integration count?
> **lina.cho**: That’s the $80M question, Rajiv. 
> **sam.reyes**: It’s all of the above. Let’s huddle on it next week.

---
**jasmine.park** [2026-05-04 08:00:00]:
Can someone help me with the Slack export for the board archives? I need to clean up the channel.
> **lina.cho**: On it. Exporting now. 

### END OF ARCHIVE — 2026-05-04