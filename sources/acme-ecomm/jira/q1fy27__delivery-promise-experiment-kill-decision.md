---
title: "Jira ticket: delivery-promise-window experiment killed on a net-negative readout"
source_url: "internal://acme-ecomm/jira/q1fy27__delivery-promise-experiment-kill-decision"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-04-15T12:00:00+00:00'
adapter: jira_ticket
---

# SPEED-1187: Close out 'Wider Promise Window' (`exp_1187`) – Kill Decision

**Project:** Fulfillment & Delivery Promise Modernization  
**Issue Type:** Task / Experiment Review  
**Key:** SPEED-1187  
**Priority:** P1 - High  
**Status:** Closed / Killed  
**Assignee:** `tara.oduya` (`assoc_100140`)  
**Reporter:** `leo.brandt` (`assoc_100141`)  
**Vertical:** SPEED (Fulfillment / PROMISE)  
**Created:** 2026-01-10  
**Resolved:** 2026-03-02  

---

### Description
Closing out the 'Wider Promise Window' experiment (`exp_1187`), which was kicked off back on 2026-01-12 under `leo.brandt` to test whether displaying slightly more conservative, wider delivery windows on the US checkout and product pages would protect our on-time-hit rates during peak sortation automation rollouts. 

As flagged in the Confluence rollout plan (`confluence.acme-ecomm.internal/speed/promise-window-rollout-q1`) and discussed during the January syncs, this test unfortunately shared both a physical DC footprint and a tight execution timeline with `gabriel.stroud`’s sortation-automation rollout (FON2 and JOL1, phased from 2026-01-12 through 2026-02-15). Now that the experiment wrapped up its full-window exposure cycle on 2026-02-20, we need to deconfound the raw data, document the final recommendation, and formally close the ticket.

---

### Comments & Activity Feed

**`leo.brandt` (2026-01-10 14:22 EST):**
> Initial ticket prep. We're launching `exp_1187` on Monday (2026-01-12) across US web and app channels. Hypothesis is that padding the outer bound of the delivery promise by +1 to +2 days will absorb transit noise and push our ship-to-home on-time-to-promise past our quarterly targets, especially while Gabriel's teams are tearing up the floors at FON2 and JOL1 for the sortation automation upgrades. Letting everyone know so Martech doesn't freak out over cart abandonment spikes during the first few cohort days.

**`gabriel.stroud` (2026-01-12 09:15 EST):**
> Just a quick heads-up from the DC side — FON2 and JOL1 phase 1 automation cutovers started this morning right alongside Leo's experiment launch. If you see weird transit latency blips out of Illinois or Inland Empire over the next month, that's us installing the new cross-belt sorters. Make sure we don't accidentally attribute DC downtime or conveyor jams to Leo's promise window algorithm.

**`amara.shah` (2026-02-03 11:40 EST):**
> Pulling preliminary numbers for the MBR deck prep. Leo, the raw logs from the first three weeks of `exp_1187` look wild—on-time-hit-rate is showing a massive +4.5pp spike. Are we sure this thing is working this well, or are we riding the tailwinds of the Ontario returns center getting its staffing levels back up after that January mess? Let's make sure we deconfound this before leadership sees it.

**`leo.brandt` (2026-02-21 16:05 EST):**
> **[Readout Update]** `exp_1187` officially wrapped its exposure window yesterday (2026-02-20). Raw full-window readout is in: we are looking at a headline **+4.2pp on-time-hit-rate** lift in the treatment arm. 
> 
> *However*, Amara is spot on—this thing is heavily confounded. Gabriel's DC sortation automation at FON2 and JOL1 wrapped up its phased rollout right around Feb 15, and the physical throughput efficiency gains in those two hubs are bleeding directly into the treatment cohort's fulfillment metrics. Furthermore, when we segment out the pure promise-window change, we're seeing a real conversion drag: users hate seeing a wider, less-attractive delivery window ("Arrives by Tuesday" vs "Arrives Friday"), and session-to-order conversion dropped by roughly 0.6% in the treatment arm because the promise message lost its competitive edge against our usual standard.

**`tara.oduya` (2026-03-02 09:30 EST):**
> Thanks for running the deconfounding models, Leo. I spent the weekend looking over the split with Carlos and Amara. 
> 
> Let's unpack what's actually happening here: once we back out the operational lift driven by Gabriel's DC automation at FON2/JOL1 (which is a permanent infrastructure win we get anyway, regardless of what we write on the checkout button), the *isolated* benefit of the wider promise window itself shrinks to a meager +1.5pp on-time-rate win. And that marginal win is completely wiped out by the conversion penalty from presenting a slower, less appealing delivery promise to the shopper. 
> 
> Put simply: widening the promise window makes us look less competitive on the checkout page, hurting conversion, without delivering a clean enough offsetting on-time-rate win once you strip away the sorting automation improvements. It's a net-negative trade.
> 
> I am officially marking `exp_1187` as **Killed** today (2026-03-02). Let's update the Confluence page so nobody tries to revive this spec next quarter. Good effort on testing it rigorously, but we keep the current promise window logic and let the new DC automation carry our efficiency gains instead.

**`nadia.esposito` (2026-03-02 11:15 EST):**
> Acknowledged. Updating the Jira roadmap views and making sure the Aitable archive links are redirected. Closing out.

---
