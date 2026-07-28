---
title: "Jira ticket: refund-cycle-time SLA breach, returns-center staffing investigation"
source_url: "internal://acme-ecomm/jira/q4fy26__returns-center-staffing-investigation"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-01-25T12:00:00+00:00'
adapter: jira_ticket
---

# CARE-4481: Quantitative avg_refund_cycle_days breaches 5.0-day SLA alert threshold

**Project:** Customer Care & Post-Order Operations (CARE / POR)  
**Issue Type:** Incident / SLA Breach Escalation  
**Priority:** P1 - Critical  
**Status:** In Progress (Open)  
**Assignee:** hannah.brennan (SVP Customer Care)  
**Reporter:** giulia.romano (Analytics Engineer, Care & VOC)  
**Created:** 2026-01-05 08:30:15 EST  
**Updated:** 2026-01-24 16:45:00 EST  
**Labels:** `sla-breach`, `refund-cycle`, `returns-center`, `ontario-ca`, `peak-ops`, `medallia-correlation`

---

## Description

The quantitative 4-week-rolling `avg_refund_cycle_days` metric (tracked across `fact_orders` via `refund_issued_date − return_date`) crossed our 5.0-day SLA alert threshold during the week of **2026-01-05**, hitting **5.03 days** (and climbing further through mid-January). 

As giulia.romano noted in the initial comment thread below, this quantitative breach comes hard on the heels of qualitative signals that surfaced during peak holiday operations. Specifically, giulia's Medallia theme report from earlier this round already flagged customer frustration regarding refund delays—with the "refund delay" verbatim share crossing the 10% threshold (hitting 11.2%) all the way back the week of **2025-12-15**, exactly three weeks before our internal quantitative monitoring caught up and breached the formal SLA. 

Initial triage across the Care ops team and fulfillment leads (dominic.paquet, gabriel.stroud) points toward severe processing bottlenecks at one of our primary returns-processing facilities (`node_type='returns_center'`), with preliminary logs and Slack side-channels strongly hinting at the Ontario, CA returns center running heavily understaffed right through the Cyber Monday and December holiday peak.

---

## Comments (14)

---
*connor.blake (Data Engineer, Data) — 2026-01-05 09:12 AM*  
Just ran a sanity check on the underlying BigQuery mart view (`nexus-analyst-demo.acme_ecomm.fact_orders`) to make sure this isn't a pipeline artifact or a lagging timezone join. It's real. The 4-week rolling average for refund cycle days is definitely sitting at 5.03 for the week ending Jan 5. 

For what it's worth, reminding everyone that per convention 5, if you're pulling broader operational figures alongside this, make sure you're hitting the aggregate marts or keeping panel boundaries straight, though for `fact_orders` on returns we're looking at the representative sample (~400k rows). Let me know if you need any custom extraction logs from the warehouse. I'm knee-deep today trying to clear out some Airflow retries that got jammed over the weekend.

---
*giulia.romano (Analytics Engineer, Care & VOC) — 2026-01-05 10:45 AM*  
@hannah.brennan tagging you here because VOC saw this coming weeks ago. 

If we look back at the Medallia verbatim stream (`fact_voc_responses`), the "refund delay" theme started spiking right after Cyber Monday week. Back on **2025-12-15**, our weekly VOC report explicitly flagged that the refund-delay verbatim share crossed our 10% warning threshold for the first time, landing at **11.2%**. It felt pretty isolated at the time amid general holiday noise, but by the time we hit the Christmas and New Year surges, those complaints snowballed. 

It's deeply frustrating that our quantitative alerting (`avg_refund_cycle_days` crossing 5.0 days) lagged behind the voice of the customer by a full three weeks. Customers were telling us loud and clear in mid-December that returns were sitting in limbo, but our trailing 4-week averages smooth out the daily spikes until the whole thing breaks the SLA threshold. We need a tighter feedback loop between Medallia theme shifts and operational alerts going into Q1.

---
*hannah.brennan (SVP Customer Care, Care) — 2026-01-05 11:30 AM*  
@giulia.romano fully agree, Giulia. I'm pulling the Medallia reports from December into the leadership brief for this. A three-week lag between customer pain and our metric hitting an actionable threshold is unacceptable, especially during peak. 

I've pinged ben.tanaka and gabriel.stroud to get eyes on warehouse return-processing throughput immediately. We know Cyber Monday week (starting Dec 1) kicked off a massive wave of inbound merchandise, but customers shouldn't be waiting over five days on average to see funds returned to their accounts once the carrier scans the package in. Let's set up an emergency sync for tomorrow morning.

---
*dominic.paquet (Care Ops Lead, Care) — 2026-01-05 02:15 PM*  
Quick update from the front lines: our contact volume for "Where is my refund?" (WIMR) has jumped roughly 34% week-over-week. The "Ask Acme v2" bot (`fact_care_contacts`, sub_program `automate`) is deflecting what it can, but agents are getting hammered with frustrated shoppers whose return tracking shows delivered to a facility, but sitting unscanned for days. 

CSAT among deflected users (`avg_csat_deflected`) has dipped to around 3.42 recently—down from ~3.70 in Q4—which tracks perfectly with the operational friction. When customers can't get clear answers out of the bot about why their return hasn't processed, they escalate to live chat, driving up handle times and hurting our support metrics across the board.

---
*gabriel.stroud (Fulfillment Ops Lead, Fulfillment) — 2026-01-06 09:00 AM*  
We are looking into the node logs now. Initial data from the West Coast network indicates that the bottleneck isn't sitewide—it's concentrated heavily around the **Ontario, CA returns-processing center** (`node_id` tied to `node_type='returns_center'`). 

As background context for why this blew up during peak: Ontario was running roughly **22% understaffed** through November and December. There was an administrative paperwork mix-up around a seasonal hiring-freeze exception request submitted back in late October that got stuck in HR routing, meaning they weren't able to onboard the temporary sorters and intake processors they needed before Black Friday. By the time the Cyber Monday return tsunami hit them, they were completely underwater. 

We've got supervisors pulling double shifts over there right now, and we're looking at emergency temp agency allocations, but it's going to take a couple of weeks to clear the backlog of unindexed boxes sitting on the dock.

---
*malik.hendon (Sr PM Acme Business, B2B) — 2026-01-08 04:20 PM*  
Just reading through this thread—are we seeing any bleed-over into B2B bulk returns or wholesale pallet credits? Malik here, checking in from the B2B side. Our wholesale accounts have their own separate SLAs, but if Ontario is lagging on physical intake scanning, I want to make sure our wholesale inventory reconciliations aren't getting caught in the same queue. Let me know if any `sel_` or wholesale account returns are flagged in that facility.

---
*gabriel.stroud (Fulfillment Ops Lead, Fulfillment) — 2026-01-08 05:10 PM*  
@malik.hendon B2B bulk returns are mostly routed through our dedicated fulfillment nodes rather than the Ontario consumer returns center, so wholesale should be clean. This is strictly hitting consumer retail parcels, particularly apparel and general merchandise flowing through the Southern California footprint.

---
*carlos.figueroa (VP Data & Analytics, Data) — 2026-01-12 10:00 AM*  
Noting for the record that this will definitely be a primary agenda item for the upcoming MBR review. Hannah, make sure we have the exact timeline of the Ontario staffing gap pulled together so we can present a clear root-cause narrative to deborah.osei and felix.arroyo. 

Also, regarding Giulia's point on the Medallia lag: let's make sure our data engineering pod figures out a way to weight verbatim volume spikes into our automated anomaly detection dashboards so we don't have to wait for a 4-week rolling average to cross a hard SLA line when qualitative signals are flashing red two weeks prior. Wei, let's chat about that during our Wednesday sync.

---
*wei.hartono (Analytics Engineer, Data) — 2026-01-14 02:30 PM*  
@carlos.figueroa will do. I can wire up a secondary advisory flag in the traffic and care marts that triggers whenever verbatim theme share for operational friction (like refund delay or listing-accuracy-gap) exceeds 8% over a rolling 7-day window. That should bridge the gap between Medallia and our hard quantitative SLAs. 

Side note: make sure whoever updates the MBR deck doesn't pull from Compass cached views without refreshing—remember the Q4FY26 Marketplace GMV restatement mess ($952.4M flash vs $975.0M canonical). Let's keep our operational numbers consistent across all executive reporting.

---
*nadia.esposito (Head of Product Operations, Product Ops) — 2026-01-18 11:15 AM*  
Following up on the Jira migration project kick-off from a few days ago (remember we're moving legacy Aitable workflows over to Jira where we can, though it's still ongoing)—is there a formal post-mortem ticket for this staffing breakdown yet? Let's make sure we log the hiring-freeze-exception workflow failure as a separate process ticket so People Ops can review why that exception request stalled out in Q3. I'll open a linked ticket under Product Ops if needed.

---
*hannah.brennan (SVP Customer Care, Care) — 2026-01-20 01:00 PM*  
Quick update on remediation: Ontario staffing is being actively supplemented with mobile temp units, and processing throughput is up about 18% week-over-week. However, the 4-week rolling average for `avg_refund_cycle_days` is still hovering around 5.21 days because the massive mid-December backlog is still working its way through the denominator. 

We expect the numbers to normalize fully once the Jan 5–12 cohort rolls out of that 4-window average. Per leadership guidance, the formal, comprehensive root-cause analysis and final remediation sign-off will land at the **February 2 MBR** meeting. 

Keeping this ticket open until then. Do not close.

---
*amara.shah (Data Analyst, Data) — 2026-01-22 04:05 PM*  
Pulling the numbers for the MBR financial pack now. Confirming that the refund delay spike didn't leave a permanent dent in Acme+ member renewal rates for January—members are grumbling in chat, but retention is holding steady at ~87.2%, which is actually beating our Q2/FY run-rate goals. Good thing the core membership benefits (free shipping, early access) are holding their value despite the post-order headache. Will link the financial slides once Amara's draft is pushed to Confluence.

---
*lucia.ferreira (Trust & Safety Lead, Marketplace) — 2026-01-23 09:30 AM*  
Just checking in from Marketplace—thankfully our seller returns (like the Collectibles and Resold items coming back through GradeSure authentication workflows) aren't routing through the Ontario consumer general returns line, or we would have really seen a pile-up. As it stands, Collectibles return rates have actually dropped nicely down to 5.4% following the Verified Badge rollout late last year, so at least we aren't compounding Care's headache over on the 3P side. Good luck getting Ontario back to green, Hannah!

---
*hannah.brennan (SVP Customer Care, Care) — 2026-01-25 04:40 PM*  
Thanks, Lucia. Leaving this ticket in its current 'In Progress' state. All eyes on the Feb 2 MBR deck prep. Closing out notes for today; will update here once the MBR review formally locks the root-cause narrative.

---
