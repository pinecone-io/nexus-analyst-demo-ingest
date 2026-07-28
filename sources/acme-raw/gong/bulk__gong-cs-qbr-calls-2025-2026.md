---
title: "Gong CS/QBR call transcripts — 2025-2026"
source_url: "internal://acme/gong-cs-qbr-calls-2025-2026"
license: "synthetic-demo"
attribution: "Synthetic content, Acme Inc internal demo. Acme Inc is a fictitious company."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: gong_call
---

# Gong Call Recording Archive: CS & QBR (FY25-FY26)

**Note:** This document contains transcripts and AI-generated summaries for Customer Success and Quarterly Business Review calls. Access is restricted to Success, Sales, and Product leadership. 

---

## Call #1: Cobalt Systems (cust_000700) - Q2 Business Review
**Date:** 2025-11-12
**Participants:** Marco Silva (Acme CSM), Tom Becker (Acme AE), Elena Volkov (Acme VP CS - partial), Sarah Jenkins (Cobalt - Dir. Ops), Mike Thorne (Cobalt - Engineering)

**[00:00:12] Marco Silva:** ...wait, can you hear me now? I think my AirPods were trying to connect to my phone in the other room. 
**[00:00:18] Sarah Jenkins:** Yeah, we got you Marco. Classic Bluetooth struggle.
**[00:00:22] Marco Silva:** Great. Thanks for jumping on. I know it’s late for you guys in London. Tom is here too, and Elena might drop in for a bit. 
**[00:00:31] Tom Becker:** Hey everyone.
**[00:00:34] Sarah Jenkins:** No worries. We’re actually just wrapping up a sprint, so we’re all fueled by way too much caffeine anyway.
**[00:00:41] Marco Silva:** I want to dive into the utilization numbers for Cobalt. I pulled the data from `nexus-analyst-demo.acme.account_health` this morning. You guys are currently at 80 seats, and I’m seeing an `active_users_28d` count of 74.
**[00:00:58] Mike Thorne:** That sounds about right. We’ve been rolling out the Acme-to-Slack triggers for the whole fintech auditing team. 
**[00:01:05] Marco Silva:** It’s actually one of our healthiest Business tier accounts. Your `utilization_band` is sitting at 0.92, which puts you firmly in the 'healthy_expansion' category in our internal health scoring.
**[00:01:18] Sarah Jenkins:** That’s good to hear. We did have some issues with workflow runs failing last Tuesday. Mike, did you get that resolved?
**[00:01:25] Mike Thorne:** Yeah, it was an `AUTH_FAILED` error on the ledger integration side. Not an Acme problem, but we used the Acme logs to track it down. By the way, Marco, we’re seeing over 50,000 runs a month now. Are we close to the limit?
**[00:01:40] Marco Silva:** You’re on the Business plan, so you have 100K runs per month. You’re at about 50% capacity. Plenty of headroom. 
**[00:01:50] Tom Becker:** And Sarah, if you do hit that 100K regularly, we should probably talk about an Enterprise upgrade. We could look at the unlimited run tier so you don't have to monitor the quota.
**[00:02:02] Sarah Jenkins:** Let's cross that bridge in Q1. For now, we're happy. Marco, what's this 'Engaged' flag I saw on the slide you sent?
**[00:02:10] Marco Silva:** Oh, that’s just our internal metric. Since you have way more than 3 active users and you’re running thousands of successful workflows every 28 days, you’re officially 'Engaged.' It just means we’re seeing real value from the platform. 

---

## Call #2: Onyx Robotics (cust_000704) - Enterprise Expansion Strategy
**Date:** 2026-01-15
**Participants:** Olivia Tran (Acme CSM), Tom Becker (Acme AE), Theo Novak (Onyx Robotics - CTO), Jessica Wu (Onyx - Lead Architect)

**[00:05:20] Theo Novak:** ...it’s not just about the seat count, Olivia. We’re moving our entire robotics CI/CD pipeline triggers into Acme. We need to know this scales. 
**[00:05:31] Olivia Tran:** Absolutely, Theo. Since you're on the Enterprise tier, you're already in our 'Stable' health bracket. We don't apply the same utilization constraints as the lower tiers because your seat count is so high—500 seats licensed. 
**[00:05:48] Jessica Wu:** Right, but we were looking at some of the documentation on your site about the Value Realization Score. We’d love to see where we sit on that VRS dashboard.
**[00:06:00] Olivia Tran:** Ah, the VRS. So, full transparency—that is actually a parked spec. It hasn't been fully built into the production dashboard yet. Our data team, Lina and Rajiv, are still refining the `vrs_band` logic. 
**[00:06:15] Tom Becker:** Yeah, don't worry about the VRS for now. We use the `account_health` table for everything. Currently, Onyx is flagged as 'Healthy' because you have zero uncollectible invoices and your P1 ticket volume is zero for the last 90 days.
**[00:06:30] Theo Novak:** Okay, well, as long as we're not flying blind. We want to add another 250 seats for the hardware team in Tokyo. 
**[00:06:38] Tom Becker:** That’s fantastic. That would bring you to 750 seats. At the Enterprise rate, we can look at annualizing that into the Q1 bookings. 
**[00:06:48] Jessica Wu:** One thing—we’ve been seeing some `STEP_TIMEOUT` errors on our longer-running Python scripts. Is that something we can increase the limit on?
**[00:07:00] Olivia Tran:** I'll have to check with Eng. Usually, for Enterprise, we can adjust the timeout parameters slightly, but it’s a global config. Let me ping Priya or David Kim on my side to see what the wiggle room is. 

---

## Call #3: Marigold Health (cust_000701) - Renewal Discussion
**Date:** 2026-03-02
**Participants:** Olivia Tran (Acme CSM), Sarah Chen (Acme AE), Dr. Aris Thorne (Marigold Health - CIO)

**[00:10:05] Sarah Chen:** ...so the renewal is coming up in May. We’re looking at staying at the 300-seat Enterprise level?
**[00:10:14] Dr. Aris Thorne:** We like the platform, Sarah. The HIPAA compliance and the audit logs in the Business/Enterprise tiers are non-negotiable for us. But I saw an invoice that was marked as 'pending' for like 45 days. My finance person said there was a discrepancy.
**[00:10:32] Olivia Tran:** I did see that. Our `account_health` monitor flagged you as 'Critical' briefly because of that uncollectible invoice. For Enterprise accounts, that’s actually the only way to hit Critical status since we don't look at utilization percentages.
**[00:10:48] Sarah Chen:** We cleared that up with Rachel Stein's team last week, right?
**[00:10:53] Dr. Aris Thorne:** Yes, it’s paid now. I just don't want to see our service downgraded because of a billing hiccup.
**[00:11:00] Olivia Tran:** Never. Enterprise has a dedicated SLA. Even if the health status says 'Critical' in our backend because of a billing lag, your service remains uninterrupted. 
**[00:11:12] Dr. Aris Thorne:** Good. Now, about the workflow runs—we’re averaging about 800,000 a month. Any issues there?
**[00:11:20] Olivia Tran:** None. You're Enterprise. Unlimited runs. You’re actually our 3rd largest consumer by volume in the NA-East region.

---

## Call #4: Harbor Dynamics (cust_000713) - P1 Escalation Bridge
**Date:** 2025-12-04
**Participants:** Marco Silva (Acme CSM), David Kim (Acme Data Eng), Kenji Sato (Harbor Dynamics)

**[00:00:45] Marco Silva:** Kenji, I have David Kim from our engineering team on the line. I know the APAC insurance workflows have been failing for the last 12 hours.
**[00:00:55] Kenji Sato:** It’s a nightmare, Marco. Our automated claims processing is stuck. Every run is throwing a `SCHEMA_MISMATCH` error. 
**[00:01:04] David Kim:** Hey Kenji, I’m looking at the `fact_workflow_runs` table in BigQuery now. It looks like the payload coming from your upstream provider changed its timestamp format.
**[00:01:15] Kenji Sato:** Why didn't the system just handle it?
**[00:01:18] David Kim:** Our parser is strict on ISO-8601. I can write a hotfix to allow the new format, but it’ll take about two hours to deploy.
**[00:01:28] Marco Silva:** Kenji, I’ve marked this as an 'at_risk' event for the account. Since this P1 has been open for a while, it triggered an alert for our VP of CS, Elena. We are all hands on deck.
**[00:01:41] Kenji Sato:** I appreciate the transparency. We have 150 seats on the Business plan, and if we can't process claims, those seats are useless.
**[00:01:50] Marco Silva:** I understand. David, let's get that hotfix into the next deployment cycle. Kenji, I'll update you every 30 minutes on Slack.

---

## Call #5: Yarrow Logistics (cust_000703) - Workflow Performance Review
**Date:** 2026-02-10
**Participants:** Marco Silva (Acme CSM), Omar Haddad (Acme AE), Lee Wong (Yarrow - Ops)

**[00:15:20] Lee Wong:** ...overall the reliability is better than our previous tool, but some of the APAC-specific webhooks feel slow. 
**[00:15:28] Marco Silva:** I ran a report on `workflow_runs_daily` for Yarrow. Your `p95_duration_ms` is around 1,200ms. That’s slightly higher than our global average of 850ms, likely due to the latency in the APAC region. 
**[00:15:44] Lee Wong:** Is there anything we can do to optimize?
**[00:15:47] Marco Silva:** We can look at the `step_count` in your workflows. Some of your logistics tracking flows have 40+ steps. If we can consolidate those using our new Batch-Request feature, we could probably drop that p95 significantly.
**[00:16:02] Omar Haddad:** And Lee, I noticed you guys are at 120 seats. We’re seeing `is_engaged` as TRUE because you have 95 people logging in every week. That’s great adoption for a team that started with 50 last year.
**[00:16:15] Lee Wong:** We’re planning to add the Australia office next month. That’ll be another 30 seats. 
**[00:16:21] Omar Haddad:** Perfect. I'll send over the add-on order. It'll show up in our Q1 bookings for the APAC event-sourced channel.

---

## Call #6: Sable Analytics (cust_000710) - NPS Detractor Follow-up
**Date:** 2026-01-22
**Participants:** Marco Silva (Acme CSM), Elena Volkov (Acme VP CS), Janet Vance (Sable Analytics - Product Mgr)

**[00:02:10] Marco Silva:** Janet, thanks for meeting. We saw your NPS score of 4 come through last week, and I wanted to reach out immediately. 
**[00:02:18] Janet Vance:** Yeah, sorry about the score, but the UI for the audit logs is just... it’s painful. We’re a fintech firm; we need to pull audit logs daily, and the current export is limited to 1,000 rows.
**[00:02:32] Elena Volkov:** Janet, I’m Elena, VP of Customer Success. I wanted to join because your feedback is exactly what Dan Lee, our VP of Product, is looking at for the Q3 roadmap.
**[00:02:44] Janet Vance:** It’s just frustrating because otherwise, the automation is great. But we’re at 90 seats on the Business plan, and my compliance team is breathing down my neck.
**[00:02:55] Marco Silva:** I've updated the `account_health` status to 'at_risk' specifically because of this NPS detractor. We don't want you to feel like you're unheard.
**[00:03:05] Janet Vance:** I appreciate that. If the export limit is lifted to 50k rows, I’ll change that 4 to a 9.
**[00:03:12] Elena Volkov:** I can't promise 50k by tomorrow, but I know Rajiv and the data team are working on a BigQuery-to-CSV direct export feature for our Business tier customers. Let me check the Linear ticket on that.

---

## Call #7: Beacon Studios (cust_000287) - Pre-Churn QBR (Retrospective)
**Date:** 2026-01-08
**Participants:** Marco Silva (Acme CSM), Derek Zorn (Beacon Studios - Head of IT)

**[00:05:40] Marco Silva:** ...utilization looks great, Derek. 65 seats licensed, 62 active. You're running about 12,000 workflows a month. Engagement is through the roof.
**[00:05:52] Derek Zorn:** Honestly, Marco, Acme is the most stable part of our stack right now. The creative teams love the auto-ingest flows for the video assets.
**[00:06:02] Marco Silva:** Your NPS was a 10 last quarter too. Everything in our health dashboard is green.
**[00:06:10] Derek Zorn:** Yeah, about that. Just a heads up—and this is off the record for now—but we’re being acquired by a much larger media conglomerate in February. 
**[00:06:22] Marco Silva:** Oh, wow. Congrats? 
**[00:06:25] Derek Zorn:** For me, sure. But their procurement team is standardized on a different automation tool. They have a global master agreement. I’m going to fight to keep Acme for our unit, but their CIO is pretty set on consolidating.
**[00:06:40] Marco Silva:** That’s... unfortunate. Is there anything we can provide to help the case? ROI reports?
**[00:06:48] Derek Zorn:** Send me the `workflow_runs_daily` stats for the last year. If I can show the sheer volume we're processing, I might be able to get an exception.
*(Note: Beacon Studios churned on 2026-02-18 due to this acquisition, despite 'Healthy' status and high engagement.)*

---

## Call #8: Verdant Cloud (cust_000707) - Quarterly Sync
**Date:** 2025-10-30
**Participants:** Olivia Tran (Acme CSM), Omar Haddad (Acme AE), Chen Wei (Verdant Cloud)

**[00:12:00] Olivia Tran:** ...and checking on the APAC usage. You’re currently at 260 seats. Since you're on the Enterprise tier, I wanted to make sure the custom SLA is meeting your needs.
**[00:12:12] Chen Wei:** It is. We haven't had any major downtime. But I noticed my `utilization_band` in the monthly report was NULL. Is there an error?
**[00:12:24] Olivia Tran:** No error! For our Enterprise customers, we actually don't calculate the utilization band. Our health logic for Enterprise focuses purely on billing and support escalations. As long as you don't have uncollectible invoices, you stay 'Healthy.'
**[00:12:41] Omar Haddad:** And Chen, we saw that huge spike in `INTEGRATION_DOWN` errors last Friday. Was that the ecommerce API you guys use?
**[00:12:50] Chen Wei:** Yes, our shipping partner went down. Acme's auto-retry logic actually saved us about 400 manual hours there. 
**[00:13:00] Olivia Tran:** That’s exactly why we built the retry queues. Glad to see the platform doing its job.

---

## Call #9: Tamarind Group (cust_000706) - Status Discussion (Paused)
**Date:** 2026-01-20
**Participants:** Marco Silva (Acme CSM), Sarah Chen (Acme AE), Linda Gregson (Tamarind Group)

**[00:03:45] Marco Silva:** Linda, I wanted to follow up on the 'Paused' status of the Tamarind account. I see we haven't had any workflow runs since January 1st.
**[00:03:55] Linda Gregson:** We’re in the middle of a massive internal restructuring. We had to pause all third-party automation until the new security protocols are signed off.
**[00:04:06] Sarah Chen:** We’re happy to help with the security audit. We can get you the SOC2 Type II report and the latest pen test.
**[00:04:15] Linda Gregson:** That would be helpful. We're not looking to churn—we love the 55 seats we have—but we just can't run anything live right now.
**[00:04:25] Marco Silva:** I’ve marked the account status as 'Paused' in `dim_customers`. This stops the health alerts from firing while you guys sort through the red tape. 

---

## Call #10: Driftwood Media (cust_000702) - Pro Tier Support
**Date:** 2025-08-14
**Participants:** Grace Liu (Acme CSM), Yuki Sato (Acme AE), Sam Rivera (Driftwood Media)

**[00:01:10] Sam Rivera:** ...yeah, we’re just a small shop, 18 seats. But we’re doing a lot of media transcoding triggers.
**[00:01:18] Grace Liu:** You’re on our Pro plan, Sam. I see you’re using about 8,000 of your 10,000 monthly runs. 
**[00:01:25] Sam Rivera:** We might need to jump to Business if we add the second production team. What’s the price jump?
**[00:01:32] Yuki Sato:** It goes from $49 a seat to $149, but it also increases your run quota to 100,000. 
**[00:01:40] Sam Rivera:** Ouch. That’s a big jump. Can we just buy more runs on the Pro plan?
**[00:01:46] Grace Liu:** Unfortunately, the Pro plan has a hard cap at 10k. The Business plan also adds SSO and audit logs, which might be good as you grow.
**[00:01:55] Sam Rivera:** Let me think about it. For now, we'll try to optimize our scripts to use fewer runs.

---

## Call #11: Ember Industries (cust_000711) - Enterprise Review
**Date:** 2025-11-28
**Participants:** Olivia Tran (Acme CSM), Tom Becker (Acme AE), Frank Miller (Ember Industries)

**[00:20:10] Frank Miller:** ...the logistics tracking has been seamless. We’re up to 350 seats. 
**[00:20:18] Olivia Tran:** You guys are definitely one of our top Enterprise performers. Your ARR is at $300k now, right Tom?
**[00:20:25] Tom Becker:** That’s right. Based on the bookings from Q3. 
**[00:20:30] Frank Miller:** We're seeing some `RATE_LIMITED` errors when we hit the UPS API. Is that an Acme thing?
**[00:20:38] Olivia Tran:** That's usually the destination API (UPS) pushing back. We can implement a jitter or a back-off strategy in your Acme workflow to handle that more gracefully. I’ll send you a template for it.

---

## Call #12: Kestrel Networks (cust_000708) - Churn Post-Mortem
**Date:** 2025-11-05
**Participants:** Marco Silva (Acme CSM), Tom Becker (Acme AE), Mark G. (Kestrel Networks - Former Champion)

**[00:02:40] Marco Silva:** Mark, really sorry to see Kestrel leave. We saw the churn notice come through for the end of the month.
**[00:02:48] Mark G.:** It's not the product, Marco. Truly. We had 70 people using it daily. But our Series C fell through, and we're cutting 40% of our software spend. 
**[00:03:00] Tom Becker:** Is there a smaller tier we could move you to? Maybe the Pro plan?
**[00:03:06] Mark G.:** We need the SSO and security features of the Business plan, and we just can't justify the $10k a month MRR right now. We’re moving everything back to some internal Python scripts. 
**[00:03:20] Marco Silva:** Understood. I’ve updated the `loss_reason` to 'budget' in the opportunities table. We’ll be here if things turn around.

---

## Internal Summary: Common Themes & Data Integrity Notes

**1. The "VRS" Distractor:**
Multiple CSMs (Olivia, Marco) reported that customers are asking about a "Value Realization Score" (VRS). 
*Reminder:* The VRS is a PARKED project. The `vrs_band` and `champion_login_recency` columns in our draft schemas are NOT populated. Do NOT attempt to query these in the `nexus-analyst-demo.acme` dataset. Use the `account_health` table for all customer health reporting.

**2. BigQuery Path Accuracy:**
There was some confusion in the Harbor Dynamics call regarding where to find the health metrics. 
*Correction:* All production-ready marts are FLAT. Use `nexus-analyst-demo.acme.account_health`. Do NOT use `acme.marts.cs.*` or any other nested structure. If you see a CSM using an old path, please direct them to Rajiv or Nina.

**3. Enterprise Health Logic:**
As highlighted in the Marigold Health (cust_000701) and Verdant Cloud (cust_000707) calls:
* Enterprise accounts (≥250 seats) are only marked 'Critical' if they have an uncollectible invoice.
* Utilization metrics (active users vs. seats) are ignored for Enterprise health status due to their large-scale, often automated, nature.

**4. ARR and Bookings Consistency:**
Tom Becker correctly identified that `bookings_acv_usd` is already annualized. Do NOT multiply it by 12 when discussing quarterly performance with Finance (Lina Cho). Our total ARR across all segments remains approximately $39M as of early 2026.

**5. Engagement Recalibration:**
The 'Engaged' flag (used in the Cobalt and Yarrow calls) was updated in late 2025. It now requires ≥3 active users AND ≥10 successful workflow runs in the last 28 days. Any legacy reports showing engagement based on a single login are now deprecated.

**6. Error Code Tracking:**
CSMs should continue to monitor `fact_workflow_runs` for the following specific error codes to proactively reach out to at-risk accounts:
* `AUTH_FAILED`: High correlation with credential expiration.
* `RATE_LIMITED`: Often seen in high-volume Enterprise accounts like Onyx Robotics.
* `STEP_TIMEOUT`: Common in complex Business tier workflows (e.g., Yarrow Logistics).

---
*End of Document*