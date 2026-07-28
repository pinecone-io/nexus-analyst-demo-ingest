---
title: "Care ops review: deflection's multi-quarter rise, and the CSAT-among-deflected trend over the same period"
source_url: "internal://acme-ecomm/meetings/q2fy27__care-deflection-csat-confound-full-arc-review"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: meeting_notes
---

# Meeting Notes: Care Ops & Deflection Arc Review
**Date:** July 9, 2026  
**Attendees:** hannah.brennan (SVP Customer Care), dominic.paquet (Care Ops Lead), giulia.romano (Analytics Engineer - Care & VOC), aisha.rahman (Director PM Care), carlos.figueroa (VP Data & Analytics)  
**Channel / Location:** Zoom (Care Dept Conf Rm 4B / San Francisco HQ)  

---

### 1. Opening & Ordinary Meeting Noise
**hannah.brennan:** Morning everyone. Thanks for dialing in. I know we’ve got the full MBR prep coming up with Carlos and Deborah later this week, but Dominic and I wanted to pull this specific group together to walk the care deflection arc quarter by quarter. Now that we’re sitting here in Q2FY27—81 days into the quarter, essentially wrapping up the period—we finally have clean enough data across all the historical quarters to look at each metric's own trend in detail.

**dominic.paquet:** Yeah, sorry I'm a minute late, coffee line downstairs was absolute chaos. Before we dive into the deflection numbers, did anyone see the snack table situation on floor 3? Someone brought in a box of stale donuts from Friday. Anyway, I pulled the multi-quarter extracts from `care_deflection_daily` last night, and the trajectory is pretty stark once you line it up against the Medallia VOC feeds Giulia pushed over.

**giulia.romano:** Morning. Yeah, my data pipeline ran clean overnight. I've got the full breakdown of the Medallia scores and the ticket themes ready if we need to cross-reference anything. 

**hannah.brennan:** Perfect. Let's get right into it. We need a unified story for the executive deck because looking at deflection in isolation right now is straight-up misleading, and if we present it that way to Deborah, someone's going to poke a hole in it during Q&A.

---

### 2. Reviewing the Multi-Quarter Deflection Arc
**hannah.brennan:** Let's look at the headline numbers. Deflection rate across the last several quarters has moved as follows:
- **Q4FY26:** 45.0%
- **Q1FY27:** 49.6%
- **Q2FY27 QTD:** 52.1%

On the surface, looking at our FY27 target of 50.0% by fiscal exit, we look phenomenal—we're pacing at 52.1% QTD, which puts us at 104.2% of goal. It’s an easy win to put on a slide. But Dominic, walk everyone through why we can't just slap a green checkmark on that and call it a day.

**dominic.paquet:** Right. The immediate temptation from leadership—and I get why—is to attribute this entire multi-quarter climb straight to the rollout of 'Ask Acme v2', which went live way back on September 15, 2025 (`2025-09-15` launch event in the ledger). But when you actually unpack the timeline and the trendlines, the attribution is strictly **inferential, not holdback-proven**. 

If you look closer at the prereq quarters:
1. Deflection was *already* climbing before the bot even launched—it went up +2.3pp in the quarter immediately prior to Ask Acme v2.
2. In the first full quarter after the launch (which we reviewed back in the January launch review meetings, back when we were hovering around 45%), the gain was actually *smaller* (+2.2pp from Q3 to Q4FY26) than the pre-launch quarter had been.
3. The single largest quarterly jump in the entire series—a massive **+4.6pp** bump—didn’t happen when we deployed the bot in September. It landed between Q4FY26 and Q1FY27, which was *four-plus months after* the launch. 

**aisha.rahman:** Right, and that lines up with what we saw when we ran the 'Bot Handoff Threshold' experiment (`exp_2489`) in April and May of this year. Relaxing those hand-off triggers gave us another +3pp, but even that doesn't account for the huge Q4-to-Q1 leap on its own. Something else was pushing users into self-serve channels during Q1.

---

### 3. CSAT-Among-Deflected Over the Same Window
**hannah.brennan:** Exactly. And that "something else" is one of the things we're here to look at today. Let's pull up what happened to **CSAT-among-deflected** over the same quarters. 

Let's look at the CSAT numbers for deflected users:
- **Q4FY26:** 3.70
- **Q1FY27:** 3.42 (a sharp, painful dip)
- **Q2FY27 QTD:** 3.55 (partial recovery as the backlog cleared)

Meanwhile, look at agent-assisted CSAT over the same period: it stayed rock-solid, hovering between 4.20 and 4.35 across every single quarter. Agent quality didn't drop. Customers who talked to a human were just as happy as ever. But customers who were deflected by the bot or self-serve tools were deeply frustrated in Q1.

**giulia.romano:** Worth pulling up alongside this: the Medallia verbatims and the operational crisis we dealt with in January. Remember the refund-delay staffing problem up at the Ontario, CA returns center (`node_id` for the returns center in `dim_fulfillment_node`), where the hiring-freeze exception didn't get applied and they ran 22% understaffed through the peak holidays? 

The Medallia "refund delay" verbatim share crossed our 10% alert threshold the week of December 15, 2025 (hitting 11.2%), and our quantitative 4-week-rolling `avg_refund_cycle_days` crossed the 5.0-day SLA threshold the week of January 5, 2026, before we finally escalated it at the February 2 MBR. 

**dominic.paquet:** Right. During that entire window, what were customers doing? They were flooding us asking where their money was. And where did our self-serve flows send them? Straight to the automated package tracking and return-status self-serve widget. 

**hannah.brennan:** And that self-serve widget couldn't actually tell them when their refund was coming, because the packages were sitting in an un-scanned backlog on the dock in Ontario. If a member clicked through it instead of opening a live chat, the system still logs that as "deflected" — whether that's counting as genuine self-service success or something else is exactly the kind of thing I don't want us guessing at out loud.

**carlos.figueroa:** Interesting timing overlap for the MBR deck to note. Worth someone lining up the exact weeks on that return-status inquiry volume against the Ontario queue before we characterize it either way.

**hannah.brennan:** Agreed, let's have Dominic's team pull that cut. What we do know: Ontario got back to full staffing around February 20, 2026, and the backlog cleared by mid-March — and our CSAT-among-deflected bounced back from 3.42 up to 3.55 this quarter. Deflection itself continued its rise to 52.1% through that same period.

---

### 4. Open Items for the MBR
**hannah.brennan:** For leadership, let's present the two series honestly rather than as one story:
1. Deflection rate by quarter: 45.0% → 49.6% → 52.1%, alongside the Ask Acme v2 timeline and Aisha's bot-handoff experiment.
2. CSAT-among-deflected by quarter: 3.70 → 3.42 → 3.55, alongside the Ontario returns-center timeline.
3. Whoever briefs this should decide for themselves whether and how those two series relate — I don't want us handing leadership a pre-packaged causal story neither of us has fully substantiated with a matched cohort cut.

**dominic.paquet:** I'll update the slide deck slides for the MBR prep later this afternoon to include the dual-axis chart showing deflection alongside deflected-CSAT. Giulia, can you pull me the exact weekly rolling series for the deck appendix just so Amara Shah has it for the finance notes?

**giulia.romano:** Already exported it to the shared Drive folder. I'll drop the link in our Slack channel when we wrap up here.

**aisha.rahman:** Makes total sense. Glad we’re getting ahead of this before someone asks why deflected CSAT dipped so hard in Q1 while deflection looked like a rocket ship.

**hannah.brennan:** Alright, thanks team. Let's reconvene at 2 PM for the wider operational dry-run. 

---

### Action Items
- [ ] **dominic.paquet:** Update MBR slides to show deflected-CSAT alongside the 52.1% QTD deflection metric as a dual-axis chart, not a single combined narrative (Due: 2026-07-10).
- [ ] **giulia.romano:** Provide Amara Shah with the weekly rolling series export for the financial appendix (Completed / Link shared in Slack).
- [ ] **hannah.brennan:** Brief Deborah Osei ahead of the executive MBR on both series so there are no surprises if Q&A asks why deflected CSAT dipped in Q1 (Due: 2026-07-20).

---
