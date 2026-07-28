---
title: "Gong internal pipeline reviews and deal reviews — 2025-2026"
source_url: "internal://acme/gong-internal-reviews-2025-2026"
license: "synthetic-demo"
attribution: "Synthetic content, Acme Inc internal demo. Acme Inc is a fictitious company."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: gong_call
---

# Gong Call Recording: Q1-2026 Forecast & Pipeline Hygiene
**Date:** January 12, 2026
**Participants:** Marcus Webb (VP Sales), Rachel Stein (CFO), Lina Cho (Finance), Tom Becker (AE), Sarah Chen (AE), Yuki Sato (AE), Omar Haddad (AE)

**[00:00:05] Marcus Webb:** Alright everyone, let’s jump in. Happy New Year, I guess, even though we’re already twelve days deep and I’m seeing some absolute carnage in the CRM. Rachel is here to keep us honest on the ARR numbers because the Board meeting is in three weeks and we need to be crisp. 

**[00:00:22] Rachel Stein:** Thanks Marcus. Yeah, just a heads up for the AEs—when you're looking at your dashboards in Looker, please make sure you're pulling from `nexus-analyst-demo.acme.arr_snapshot`. I saw someone yesterday trying to calculate ARR by just multiplying `dim_customers.current_mrr_usd` by 12 in a Google Sheet. Do not do that. It drifts intraday. Use the snapshot table for official reporting.

**[00:00:45] Tom Becker:** That might have been me, Rachel. My bad. I was just trying to get a quick look at where Onyx Robotics landed.

**[00:00:52] Marcus Webb:** Speaking of Onyx. Tom, you’re up. Onyx Robotics (cust_000704). We’ve been talking about this Enterprise whale for three months. 500 seats. Where are we?

**[00:01:04] Tom Becker:** Closing in, Marcus. We’re at the goal line. Paperwork is with their legal team. We’re looking at $35,000 MRR, so that’s a $420k ACV deal. They tried to haggle on the dedicated CSM support, but I told them for 500 seats on the Enterprise tier, it’s non-negotiable. 

**[00:01:22] Marcus Webb:** And is that ACV already annualized in the system? I don’t want to get to the end of the month and find out we recorded MRR as ACV.

**[00:01:30] Lina Cho:** Just to clarify for the room—in the `nexus-analyst-demo.acme.bookings_attribution` table, the column `bookings_acv_usd` is ALWAYS annualized. If the deal is $35k MRR, the table will show $420,000. Do not multiply it by 12 again or Sam [Reyes] will think we had a $5 million month and then kill me when I have to revise it down.

**[00:01:54] Sarah Chen:** Quick question on that, Lina. Does that table include my Pro-to-Business upgrades that happened via the website? I had two accounts, Pebble Digital (cust_000705) and another one, that just added 50 seats on their own.

**[00:02:08] Lina Cho:** No. `bookings_attribution` is AE-led only. PLG self-serve flows directly into `fact_subscriptions` but skips the bookings table because there’s no `opportunity_id` associated with it. If you didn’t touch it in the CRM, it’s not a "booking" in the sales sense, even though it hits our ARR.

**[00:02:25] Marcus Webb:** Which is why we need to focus on the Enterprise conversions. Sarah, what’s the status on Quartz Foundry (cust_000714)? 280 seats in EMEA healthtech. That’s a big one for your number.

**[00:02:37] Sarah Chen:** Yeah, Quartz is moving. We’re at 280 seats. They’re coming over from a legacy competitor. The partner channel really did the heavy lifting here. They’re looking at a $12,000 MRR deal. It’s slightly lower than standard Enterprise pricing because of the partner discount, but the NRR potential is massive because they have three other subsidiaries they want to bring on by Q3.

**[00:03:01] Marcus Webb:** Okay, I like that. Omar, what about Yarrow Logistics (cust_000703)? You’ve got them at 120 seats on the Business tier?

**[00:03:10] Omar Haddad:** Yep, $17,880 MRR. They came in through the Tokyo event in November. They're already "Engaged" according to the health scores. I checked `acme.account_health` this morning and they’ve got 45 active users already, even though they only licensed 120. 

**[00:03:30] Marcus Webb:** Wait, only 45 active? That’s not great utilization for a Business tier.

**[00:03:35] Lina Cho:** Actually, Marcus, for the Business tier, they only need 3 active users and 10 successful runs to be "Engaged" in our new Q4 2025 definition. 45 users is actually solid for their first 30 days. Omar, just make sure they don't drop into the `utilization_band` below 0.20 or they’ll hit "Critical" status. 

**[00:03:55] Rachel Stein:** Let's talk pipeline coverage. Marcus, I'm looking at the aggregate. We need 3x coverage to hit the $45M ARR target by mid-year. Right now, across the whole team, we’re at 2.4x. Tom, your pipe looks a bit thin if Onyx doesn't close this week.

**[00:04:12] Tom Becker:** I’ve got Ember Industries (cust_000711) in the wings. 350 seats. That’s another $25k MRR. And I’m hunting a few leads in the logistics space. But honestly, the CRM is a mess. I spent two hours yesterday trying to find the `first_touch_channel` for a lead because it wasn't syncing from HubSpot.

**[00:04:31] Marcus Webb:** CRM hygiene is not an excuse for a thin pipe, Tom. If you need help, talk to Jorge [Martinez]. But I need to see more outbound. We can’t just live on partner referrals and events. 

**[00:04:45] Yuki Sato:** Speaking of "not living on stuff," are we going to talk about the churn from Q4? Kestrel Networks (cust_000708) hitting the churn column really hurt my standing in the sales contest. 

**[00:05:00] Marcus Webb:** Kestrel was a budget cut, Yuki. Nothing you could do. Tom, you handled that account, right?

**[00:05:06] Tom Becker:** Yeah, Kestrel was $10,430 MRR. Pure budget play. They slashed their whole devtools stack by 40%. It’s a shame because their utilization was high. 

**[00:05:18] Rachel Stein:** This brings up the NRR discussion for the Board. We’re currently at 107%. Our target is 110%. The Beacon Studios (cust_000287) churn in February is going to bite us too. That’s $116k ARR gone. 

**[00:05:33] Lina Cho:** Just a reminder for everyone when you’re looking at the NRR report—we use a fixed cohort. If a customer like Beacon churns, they stay in the denominator but go to zero in the numerator. I saw a draft report where someone did an INNER JOIN on customers and it showed our NRR at 122% because it ignored the churned accounts. That is wrong. We use a LEFT JOIN from the `nrr_trailing_12` table. Don't report the 122% number or Sam will get his hopes up for nothing.

**[00:06:04] Marcus Webb:** 107% is solid, but we need expansion to bridge that 3% gap. Omar, Harbor Dynamics (cust_000713) is at 150 seats—any room for expansion there?

**[00:06:15] Omar Haddad:** They’re at $22,350 MRR right now. They’re healthy. "Healthy Expansion" status in the mart. They’re using 0.85 of their seats. I’m pushing them for another 50 seats by the end of March.

**[00:06:30] Marcus Webb:** Good. Alright, I’ve got to jump to a 1:1. Tom, get Onyx signed. Sarah, watch Quartz. And for the love of god, stop trying to query `acme.marts.finance.arr_snapshot`. It’s just `acme.arr_snapshot`. We don't have nested datasets. 

---

# Gong Call Recording: Deal Review - Onyx Robotics & Ember Industries
**Date:** February 4, 2026
**Participants:** Marcus Webb (VP Sales), Tom Becker (AE), Rachel Stein (CFO)

**[00:00:10] Marcus Webb:** Tom, tell me Onyx is done. I saw the Slack notification but I want to hear it from you.

**[00:00:18] Tom Becker:** Signed, sealed, delivered. $420,000 ACV. Onyx Robotics (cust_000704) is officially an Enterprise customer. 500 seats. 

**[00:00:27] Rachel Stein:** Congrats Tom. That’s a huge win for the quarter. Does this include the custom SLA they were asking for?

**[00:00:34] Tom Becker:** Yeah, we gave them the 99.9% uptime SLA. Engineering signed off on it since we moved to the new cluster. Marcus, they also want to be a case study for the Dreamforce trip.

**[00:00:46] Marcus Webb:** We’ll talk about Dreamforce in May. Let’s stay focused. What’s the word on Ember Industries (cust_000711)? You had them at 350 seats. 

**[00:00:55] Tom Becker:** They’re stalling a bit. The VP of Ops at Ember is worried about the "Value Realization Score." I tried to tell him we don't really have a formal VRS metric yet, it's still a draft spec, but he's insistent on seeing how we measure "champion login recency."

**[00:01:12] Marcus Webb:** Did you show them the `account_health` status? 

**[00:01:16] Tom Becker:** I did. They’re currently "Monitoring" because they’re still in the POC, but their utilization is trending up. I’m hoping to close them for $300k ACV by the end of the month. 

**[00:01:28] Rachel Stein:** Marcus, I'm looking at our total ARR run-rate versus recognized revenue. With Onyx closing, we’re hitting about $39.2M ARR. But we need to be careful with the "Pro" tier. We've got a lot of churn in the $49/seat bucket. 

**[00:01:45] Marcus Webb:** Yuki’s deals?

**[00:01:47] Rachel Stein:** Not just Yuki. Driftwood Media (cust_000702) and Willow Works (cust_000709) are stable, but we lost Juniper Collective (cust_000712) last month. It was only 12 seats, so $588 MRR, but it's the "death by a thousand cuts" thing. 

**[00:02:05] Tom Becker:** Juniper Collective left because of "product fit," right? They wanted that weird integration with the legacy mainframe stuff we don't support. 

**[00:02:14] Marcus Webb:** Exactly. We can’t win them all. But we can’t afford to lose any more Business tier accounts. Speaking of, what happened with Tamarind Group (cust_000706)? Sarah had them as "Paused."

**[00:02:27] Rachel Stein:** Tamarind is in a weird spot. They had some internal restructuring. They’re still paying for 55 seats, but they’ve basically stopped using the platform. Their health status in the warehouse is "Critical" because their `utilization_band` is under 0.20. 

**[00:02:44] Marcus Webb:** If they’re on the Business tier and they aren’t using it, they’re going to churn. Sarah needs to get in there. Lina, can you pull a list of all Business tier accounts with utilization under 30%?

**[00:02:56] Lina Cho:** I already have a Looker alert for that. It’s pulling from `acme.account_health`. Currently, it’s Tamarind Group and one other SMB account. 

**[00:03:07] Tom Becker:** Hey, before we go, are we still doing the sales contest for the trip to Cabo? Because I’m pretty sure Onyx just put me in the lead.

**[00:03:15] Marcus Webb:** You’re in the lead for now, Tom. But Sarah has two Enterprise deals in the pipeline that could leapfrog you. Don't get comfortable.

---

# Gong Call Recording: Finance & Sales Sync - NRR & Cohort Math
**Date:** March 15, 2026
**Participants:** Rachel Stein (CFO), Lina Cho (Finance), Marcus Webb (VP Sales), Sarah Chen (AE)

**[00:00:12] Rachel Stein:** Okay, let’s look at the NRR numbers again. Lina, can you pull up the `nrr_trailing_12` table?

**[00:00:20] Lina Cho:** Sure. For the cohort that started in March 2025, we’re looking at a 107.2% NRR. The expansion MRR from accounts like Cobalt Systems (cust_000700) really helped. Tom added 20 seats there last quarter.

**[00:00:36] Marcus Webb:** Cobalt is a great story. Tom’s doing a good job there. But why is the GRR only 94%? 

**[00:00:43] Lina Cho:** Because GRR (Gross Retention Rate) doesn't count the expansion. It only looks at what we kept from the original cohort, capped at 100% per account. The churn from Kestrel Networks (cust_000708) and Beacon Studios (cust_000287) is what's dragging that down. 

**[00:01:01] Sarah Chen:** Wait, I thought Beacon didn't count against us because it wasn't a "bad" churn?

**[00:01:07] Rachel Stein:** Finance doesn't care if it's "bad" or "good" churn, Sarah. If the money leaves the building, it’s churn. The board wants to see 110% NRR. To get there, we need more "Healthy Expansion" accounts. 

**[00:01:21] Sarah Chen:** Well, Quartz Foundry (cust_000714) just went live. 280 seats. They’re already asking about adding another 100 seats for their subsidiary in Germany. That should hit in Q3.

**[00:01:34] Marcus Webb:** Is that a new opportunity or an expansion? 

**[00:01:37] Sarah Chen:** I’m treating it as an expansion on the existing `customer_id` to keep the paperwork simple, but I’ll open a new opportunity in the CRM so I get the booking credit.

**[00:01:46] Lina Cho:** If you do that, make sure the `change_type` in `fact_subscriptions` is recorded as 'expansion'. If the system sees it as a new subscription, it might mess up the NRR cohort math. 

**[00:02:00] Marcus Webb:** Okay, let’s talk about the mid-market. Omar, you’ve got Sable Analytics (cust_000710). 90 seats. $13,410 MRR. How are they doing?

**[00:02:11] Omar Haddad:** They’re "Stable." Utilization is around 65%. They came through a partner, so the margin is a bit lower, but they’re very engaged. They had zero support tickets last month.

**[00:02:24] Rachel Stein:** That’s what we like to see. No support tickets means the automation is actually working. Marcus, I noticed some people are still using the old `vrs_band` column in their private dashboards. Can you tell the team that VRS is dead? We're using `account_health_status` now. 

**[00:02:41] Marcus Webb:** I’ve told them twice. I’ll tell them again at the Monday standup. It’s hard to break old habits, especially when the old Looker dashboard still has the VRS tab.

**[00:02:52] Lina Cho:** I’ll delete that tab tonight. Problem solved. 

**[00:03:00] Sarah Chen:** Hey, does anyone know if we're doing anything special for the EMEA team? Marco [Silva] was asking about the Amsterdam office expansion.

**[00:03:10] Marcus Webb:** Focus on the deals, Sarah. We’ll worry about office space when we hit $50M ARR. Right now we’re at $39M. We’ve got work to do.

---

# Gong Call Recording: Pipeline Flush & CRM Hygiene
**Date:** April 10, 2026
**Participants:** Marcus Webb (VP Sales), Tom Becker (AE), Sarah Chen (AE), Yuki Sato (AE), Omar Haddad (AE), Jorge Martinez (RevOps)

**[00:00:05] Marcus Webb:** This is going to be a painful meeting. Jorge is here because our CRM data is currently about 60% fiction. We have deals in "Discovery" that haven't been touched since October. We have "Closed Won" deals that don't have an `opportunity_id` in the `bookings_attribution` table. 

**[00:00:25] Jorge Martinez:** Yeah, thanks Marcus. Specifically, I’m looking at you, Yuki. Driftwood Media (cust_000702) and Willow Works (cust_000709). You have them as "Active" in the CRM but there's no record of the initial contract in the `fact_opportunities` table. 

**[00:00:43] Yuki Sato:** That’s because those were Pro tier accounts that I upgraded manually. I didn't think I needed an opportunity for a 15-seat upgrade.

**[00:00:52] Jorge Martinez:** You do if you want it to show up in the `bookings_acv_usd` reports. If there's no opportunity, it's just "found money" to Finance and you don't get credit for the quota.

**[00:01:04] Yuki Sato:** Well, that explains why my dashboard looks so sad. 

**[00:01:08] Marcus Webb:** Tom, what about Marigold Health (cust_000701)? Sarah, I think that’s yours? 300 seats, Enterprise. 

**[00:01:15] Sarah Chen:** Marigold is solid. $15,000 MRR. They came through a partner. I just checked the warehouse—their `account_health_status` is "Healthy Expansion" because they’re at 90% seat utilization. I’m actually talking to them about an Enterprise+ tier if we ever launch one.

**[00:01:34] Marcus Webb:** Don’t sell things that don't exist, Sarah. We have four plans: Free, Pro, Business, Enterprise. That’s it. 

**[00:01:42] Tom Becker:** Marcus, can we talk about the "Free to Paid" conversion rate? I’m seeing a lot of people in my territory signing up for Free accounts but never moving to Pro. 

**[00:01:53] Jorge Martinez:** That’s a Marketing thing, Tom. Jasmine [Park] is looking at the `fact_user_events` to see where they’re dropping off. But for us, focus on the AE-led deals. 

**[00:02:05] Omar Haddad:** I have a question about the BigQuery paths. I was trying to run a query on `fact_workflow_runs` to see how many runs Yarrow Logistics (cust_000703) did yesterday, but I got a "Table not found" error. 

**[00:02:18] Jorge Martinez:** You probably used `acme.marts.fact_workflow_runs`. It’s just `nexus-analyst-demo.acme.fact_workflow_runs`. No subfolders. 

**[00:02:30] Omar Haddad:** Got it. Also, why does the data lag by 2 hours? I was trying to show a customer their real-time usage during a demo and it looked like they had zero runs.

**[00:02:40] Marcus Webb:** That’s just the warehouse sync, Omar. Use the production dashboard for real-time stuff. The BI warehouse is for reporting, not live demos. 

**[00:02:50] Sarah Chen:** Hey, are we still on for the team dinner on Thursday? 

**[00:02:54] Marcus Webb:** If Tom closes Ember Industries by Thursday, dinner is on me. If not, we’re having pizza in the office. 

**[00:03:02] Tom Becker:** Better start looking at steakhouse menus then, Marcus. Ember is 90% there. 

---

# Gong Call Recording: Quarter-End Push - May 2026
**Date:** May 2, 2026
**Participants:** Marcus Webb (VP Sales), Rachel Stein (CFO), Tom Becker (AE), Sarah Chen (AE), Yuki Sato (AE), Omar Haddad (AE)

**[00:00:05] Marcus Webb:** Okay, today is May 2nd. We’re officially looking at the final numbers for April and the state of the Q2 pipe. Rachel, do you want the good news or the bad news?

**[00:00:15] Rachel Stein:** Give me the real news. What’s the ARR?

**[00:00:20] Marcus Webb:** We finished April at $39.4M ARR. Onyx Robotics is fully onboarded. Quartz Foundry is live. We had a slight dip from a few Pro tier churns, but nothing catastrophic. 

**[00:00:34] Rachel Stein:** $39.4M. That’s a bit behind our $40M internal target for the month. What happened with Ember Industries (cust_000711)? 

**[00:00:43] Tom Becker:** Legal. It’s always legal. They’re arguing over the indemnity clause for the automation of their logistics workflows. Apparently, if a workflow fails and a truck doesn't show up, they want us to pay for it. 

**[00:00:57] Marcus Webb:** Tell them we have a standard SLA and if they want more, they have to pay for the Premium Support package. Don't budge on the ACV. It’s a $300,000 deal. 

**[00:01:08] Tom Becker:** I’m holding firm. 350 seats at the Enterprise rate. 

**[00:01:13] Sarah Chen:** I have some good news. Marigold Health (cust_000701) just added 50 more seats. They’re now at 350 seats. So that’s an extra $2,500 MRR on that account. 

**[00:01:25] Rachel Stein:** Did you record that in the CRM? I need to see the expansion credit in the `nrr_trailing_12` table. 

**[00:01:33] Sarah Chen:** Done. I also checked their health—they’re still "Healthy Expansion" even with the new seats. Their `utilization_band` is at 0.78. 

**[00:01:44] Yuki Sato:** I’m seeing some weirdness with Driftwood Media (cust_000702). Their `auth_failed_count` in `workflow_runs_daily` spiked yesterday. Should I be worried about churn?

**[00:01:56] Lina Cho (joining late):** Yuki, that was a global issue with the Slack integration. It’s not just Driftwood. Check the `integration_down_count` column. It wasn't their fault, so it shouldn't affect their health score unless it stays high for 48 hours. 

**[00:02:12] Marcus Webb:** Omar, you’ve been quiet. How’s Yarrow Logistics?

**[00:02:16] Omar Haddad:** Steady. 120 seats. We’re working on a referral deal with one of their partners. It could be another 100-seat Business deal. 

**[00:02:26] Marcus Webb:** I love referral deals. Low CAC, high NRR potential. Alright, everyone, we’re at $39.4M. I want to see $41M by the end of May. Tom, get Ember done. Sarah, keep pushing Marigold. Yuki, watch those Pro churns. 

**[00:02:45] Tom Becker:** And Marcus, what about the Dreamforce trip?

**[00:02:49] Marcus Webb:** If we hit $41M, I’ll buy the flights. If we hit $42M, I’ll buy the hotel. Get to work. 

---

# Gong Call Recording: Churn Autopsy - Beacon Studios & Kestrel Networks
**Date:** March 20, 2026
**Participants:** Marcus Webb (VP Sales), Elena Volkov (VP CS), Tom Becker (AE), Rachel Stein (CFO), Marco Silva (CSM)

**[00:00:10] Marcus Webb:** We need to talk about why we lost nearly $250k in ARR over the last few months. Beacon Studios (cust_000287) and Kestrel Networks (cust_000708). Tom, you were the AE on both. Marco, you were the CSM on Kestrel. What happened?

**[00:00:27] Tom Becker:** Beacon was out of our hands. They got acquired by a conglomerate that has a global partnership with one of our competitors. It wasn't about the product. Their NPS score was a 9 right before the acquisition. 

**[00:00:41] Elena Volkov:** I can confirm that. Their `account_health_status` was "Healthy Expansion" until the day they sent the termination notice. 

**[00:00:50] Rachel Stein:** It still hurts the NRR. We need to make sure we’re not losing accounts because of stuff we *can* control. Like Kestrel. 

**[00:00:58] Marco Silva:** Kestrel was budget. They were on the Business tier, 70 seats. They loved the product, but their CFO mandated a 50% reduction in SaaS spend across the board. We tried to downsell them to the Pro tier, but they needed the SSO and audit logs that are only in Business. 

**[00:01:17] Marcus Webb:** Why didn't we just give them a discount on Business to keep them?

**[00:01:21] Tom Becker:** We offered 20% off, but it wasn't enough. They had to cut the seat count to 20, and at that point, the Business tier minimums kicked in. 

**[00:01:31] Rachel Stein:** This is why I keep saying we need a "Business Lite" tier. But Dan [Lee] won't hear of it. 

**[00:01:38] Marcus Webb:** Focus on what we have. We lost Kestrel, but we gained Onyx. The net is positive, but the churn is dragging our NRR down to 107%. If we hadn't lost Beacon, we’d be at 109.5%. 

**[00:01:53] Elena Volkov:** I’m worried about Tamarind Group (cust_000706). They’re "Paused" but they’re likely to churn. Marco, what’s the latest?

**[00:02:02] Marco Silva:** I’ve been ghosted by the champion. I checked `dim_users` and the last login for the admin was 22 days ago. 

**[00:02:11] Marcus Webb:** That’s a red flag. Sarah, you’re the AE there. You need to find a new champion. Check LinkedIn, see if anyone we know moved there. 

**[00:02:20] Sarah Chen:** I’m on it. I’ve got a meeting with their Head of Infrastructure next Tuesday. 

**[00:02:26] Rachel Stein:** One more thing—Lina noticed some AEs are tagging "Churn" in the CRM but not putting the `loss_reason`. Please fill that out. It’s a column in `fact_opportunities`. If it’s NULL, I can’t do my board reporting on churn drivers. 

**[00:02:43] Marcus Webb:** You heard her. No more NULLs. Let’s get it together. 

---

# Gong Call Recording: Enterprise Expansion - Quartz Foundry Deep Dive
**Date:** April 22, 2026
**Participants:** Marcus Webb (VP Sales), Sarah Chen (AE), Olivia Tran (CSM), Rachel Stein (CFO)

**[00:00:15] Marcus Webb:** Sarah, let’s talk Quartz Foundry (cust_000714). They’ve been live for two months. How’s the expansion looking?

**[00:00:23] Sarah Chen:** It’s looking great. They’re at 280 seats right now, $12,000 MRR. Olivia and I had a QBR with them last week and their CTO is thrilled. They’ve run over 50,000 workflows in the last 30 days. 

**[00:00:38] Olivia Tran:** Yeah, their success rate is 99.8%. The only errors are `SCHEMA_MISMATCH` because their internal dev team keeps changing their API endpoints without telling their automation team. 

**[00:00:51] Sarah Chen:** Anyway, they want to bring their medical imaging division onto the platform. That’s another 150-200 seats. 

**[00:00:59] Marcus Webb:** That would put them near the 500-seat mark. At that point, we should look at a multi-year deal. 

**[00:01:06] Rachel Stein:** If they go multi-year, we can offer a better rate, but I want to see the upfront payment. Our cash flow for Q3 is looking a bit tight because of the office build-out. 

**[00:01:18] Sarah Chen:** I’ll push for an annual upfront. Quartz is EMEA-based, so they usually prefer that anyway. 

**[00:01:25] Marcus Webb:** What’s the status of the "Healthy Expansion" flag in the dashboard for them?

**[00:01:30] Olivia Tran:** It’s active. They hit all the triggers: engaged, high utilization, and no open P1 tickets for over 48 hours. 

**[00:01:40] Rachel Stein:** Good. I’m using the `account_health` mart to forecast our expansion revenue for the next six months. Quartz is my biggest line item for the "High Probability" bucket. 

**[00:01:52] Marcus Webb:** No pressure, Sarah. 

**[00:01:55] Sarah Chen:** None at all. Just another day in Paradise. 

**[00:01:58] Marcus Webb:** Alright, let’s talk about the rest of the pipe. Tom, what’s the deal with Verdant Cloud (cust_000707)? 260 seats in APAC?

**[00:02:08] Tom Becker:** That’s Omar’s deal, actually. 

**[00:02:11] Omar Haddad:** Yeah, Verdant is stable. $8,000 MRR. They’re an Enterprise customer but on a very early "legacy" price point. I’m trying to move them to the current Enterprise pricing at their next renewal in June. 

**[00:02:26] Marcus Webb:** That’ll be a tough conversation. Make sure you lead with the new features we’ve added—the audit logs and the custom SLAs. 

**[00:02:35] Omar Haddad:** Already on it. I’ve got a meeting with their procurement team on Friday. 

**[00:02:41] Marcus Webb:** Good luck. 

---

# Gong Call Recording: Sales Strategy - Q2 Goal Setting
**Date:** May 4, 2026
**Participants:** Marcus Webb (VP Sales), Rachel Stein (CFO), Tom Becker (AE), Sarah Chen (AE), Yuki Sato (AE), Omar Haddad (AE)

**[00:00:05] Marcus Webb:** Final meeting of the week. Today is May 4th. The warehouse refresh just finished. Lina, what are the numbers?

**[00:00:14] Lina Cho:** Total ARR is $39,120,450. We had a few small downgrades in the SMB tier that offset the expansion from Marigold. 

**[00:00:25] Marcus Webb:** $39.1M. Okay. We need $900k to hit $40M. Tom, Ember Industries is the key. 

**[00:00:33] Tom Becker:** They’re signing today. I promise. $25k MRR, so $300k ACV. 

**[00:00:40] Marcus Webb:** That gets us to $39.4M. Where’s the other $600k coming from?

**[00:00:46] Sarah Chen:** I’ve got a new lead, Tamarind Group’s sister company. It’s early but they want 100 seats on Business. 

**[00:00:54] Omar Haddad:** And I’m closing a mid-market deal for $12k MRR next week. 

**[00:01:00] Rachel Stein:** I’m looking at the `fact_opportunities` table. We have about $2.1M in "Stage 4 - Negotiation" deals. If we close 30% of those, we hit the goal. 

**[00:01:13] Marcus Webb:** 30% is a low bar. Let’s aim for 50%. I want everyone focused on the Enterprise tier. That’s where the growth is. 

**[00:01:22] Yuki Sato:** What about the Pro tier? I’m getting a lot of inbound from smaller teams. 

**[00:01:27] Marcus Webb:** If it’s under 50 seats, let them self-serve. Don't spend your time on $49/seat deals unless they have clear expansion potential to Business. 

**[00:01:38] Rachel Stein:** Yuki, just make sure they use the right referral code so you get the attribution. 

**[00:01:45] Yuki Sato:** I will. Oh, and Marcus—about the Cabo trip. Can I bring a plus one?

**[00:01:51] Marcus Webb:** Hit your quota first, Yuki. Then we’ll talk about plus ones. 

**[00:01:57] Yuki Sato:** Fair enough. 

**[00:02:00] Marcus Webb:** Alright, let’s go. We’ve got deals to close. And remember: the path is `nexus-analyst-demo.acme`. No marts, no folders. Just the table. 

**[00:02:12] Lina Cho:** Thanks Marcus. I’m going to go update the ARR dashboard now. 

**[00:02:18] Marcus Webb:** Meeting adjourned. 

---

### END OF DOCUMENT ###