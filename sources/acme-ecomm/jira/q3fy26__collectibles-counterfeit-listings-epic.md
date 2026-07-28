---
title: "Jira epic: Collectibles counterfeit-listing spike and the Trust & Safety response"
source_url: "internal://acme-ecomm/jira/q3fy26__collectibles-counterfeit-listings-epic"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2025-10-15T12:00:00+00:00'
adapter: jira_ticket
---

# JIRA EPIC: MKT-4402
**Title:** Collectibles Counterfeit-Listing Spike & Trust & Safety Operational Response  
**Project:** Marketplace Engineering & Operations (MKT)  
**Epic Status:** In Progress (Active)  
**Priority:** P1 - Critical  
**Assignee:** lucia.ferreira (Trust & Safety Lead)  
**Reporter:** victor.okonkwo (SVP Marketplace)  
**Created:** 2025-08-04  
**Updated:** 2025-10-15  
**Vertical:** MARKETPLACE (COLLECTIBLES)  
**Labels:** `trust-and-safety`, `counterfeit`, `collectibles-boom`, `seller-compliance`, `acme-verified`

---

## Epic Description

Following the unprecedented viral vintage-card auction result on August 4, 2025, Acme Marketplace experienced an immediate, massive influx of new buyers and third-party sellers into the Collectibles sub-vertical (which had historically hovered around $22M–$25M quarterly GMV before jumping dramatically). While this growth brought exciting acceleration—pushing Q3FY26 Collectibles GMV projections past $61M—it simultaneously triggered an aggressive spike in bad-faith actors attempting to list high-value counterfeit items (particularly graded sports cards and rare trading card game singles).

This epic tracks the cross-functional emergency response, policy enforcement actions against bad-faith sellers, the urgent onboarding of `lucia.ferreira` as the dedicated Trust & Safety Lead for Marketplace, and the architectural design and rollout of the **Acme Verified** third-party authentication partnership (GradeSure integration) to safeguard buyer trust without choking legitimate marketplace velocity.

---

## Child Issues / Sub-Tasks

| Key | Summary | Assignee | Status | Resolution | Updated |
|---|---|---|---|---|---|
| **MKT-4403** | Emergency keyword & visual-anomaly flagging rules for Collectibles listings | sanjay.bhatt | Done | Completed | 2025-08-10 |
| **MKT-4404** | Compliance review & enforcement action: `sel_500089` (Bramblewood Vintage) | lucia.ferreira | Done | Suspended / Reviewed | 2025-09-02 |
| **MKT-4405** | T&S Leadership Backfill & Onboarding: Trust & Safety Lead (`lucia.ferreira`) | victor.okonkwo | Done | Completed | 2025-09-01 |
| **MKT-4406** | "Acme Verified" vendor integration PRD & pilot partnership (GradeSure) | lucia.ferreira | In Progress | — | 2025-10-14 |
| **MKT-4407** | Marketplace listing audit: Collectibles return rate and dispute correlation | amara.shah | Done | Completed | 2025-09-25 |
| **MKT-4408** | "Verified Badge Prominence" experiment setup (`exp_2401`) | sanjay.bhatt | In Progress | — | 2025-10-10 |

---

## Activity Stream & Comments

**2025-08-04 09:14 ET** — **victor.okonkwo** logged a comment:
> Folks, have you seen the traffic on Collectibles this morning? Following that absurd $3.1M vintage card sale making national news over the weekend, our server logs are lighting up. Sessions are up nearly 3x week-over-week in the sub-vertical, and new seller accounts are being created by the minute (`sel_500200` through `sel_500213` look mostly okay, but the unverified tail is getting messy). We need an immediate triage crew on listing moderation before our return rates and chargebacks get blown out. `sanjay.bhatt`, can you pull a quick query on active listing velocity for ungraded high-value cards?

**2025-08-04 14:32 ET** — **sanjay.bhatt** logged a comment:
> Pulled the initial cut from `fact_marketplace_listings`. In the last 48 hours alone, we've seen over 4,200 new listings in Collectibles priced above $500, and roughly 35% of them originate from brand-new seller accounts with zero historical feedback. I'm seeing duplicate image hashes across multiple distinct seller profiles—classic bot-net listing patterns. Sub-vertical GMV is spiking, but our fraud signals are screaming. We can't handle this ad hoc; we need dedicated T&S ownership here yesterday. 

**2025-08-12 11:05 ET** — **lucia.ferreira** logged a comment:
> *(Note: I am onboarding informally ahead of my official formal start date next month to assist with this triage).* We have flagged our first major target: **Bramblewood Vintage (`sel_500089`)**. They just dumped 140 high-end card listings at steep discounts using stolen certificate numbers from PSA/BGS registries. Three distinct counterfeit-listing violations have been formally logged against `sel_500089` today. I'm preparing the suspension notice. `victor.okonkwo`, let's make sure our legal and compliance teams are looped in because this seller is pushing back hard through their automated support alias.

**2025-08-12 16:40 ET** — **connor.blake** logged a comment:
> Quick data note while digging through the pipeline: remember that `dim_seller` and `fact_marketplace_listings` are representative panels (~2,500 sellers / ~35k listings sampled) rather than the absolute full population table, so when reporting total exposed risk to the board, make sure you're scaling these ratios against the full marketplace GMV summary marts (`marketplace_gmv_summary`), or finance will have a field day with the discrepancy. Also, whoever set up the staging cron for the BigQuery connector on the new seller metadata feed, can you check your partitioning? It timed out twice this morning.

**2025-09-01 08:30 ET** — **victor.okonkwo** logged a comment:
> Official welcome to **lucia.ferreira**, who starts today as our new Trust & Safety Lead for Marketplace! This role was pulled forward as an urgent backfill directly in response to the August 4th Collectibles counterfeit spike. Lucia is stepping right into the fire with MKT-4402. Let's get her all system access by noon today.

**2025-09-02 09:15 ET** — **lucia.ferreira** logged a comment:
> Thanks Victor. Official start date active, and my first official act as T&S Lead: **Bramblewood Vintage (`sel_500089`) has been officially suspended** pending a mandatory compliance review. All 140 of their fraudulent listings have been scrubbed from the live site, and affected buyers have been flagged for proactive refund processing through Customer Care (`hannah.brennan`'s team has been briefed so they know why chat volume on Collectibles authenticity is ticking up). Let's keep a close eye on whether they try to spin up a shell account under a different tax ID.

**2025-09-08 14:20 ET** — **lucia.ferreira** logged a comment:
> Big milestone for MKT-4406: We have officially executed the contract for the **"Acme Verified" authentication program** partnering with **GradeSure**. Starting today, any Collectibles seller wanting to list items above $250 without manual escrow review must route their inventory through GradeSure's intake hubs or link an authorized digital cert. `sanjay.bhatt`, this tees up `exp_2401` nicely for October.

**2025-09-20 10:00 ET** — **amara.shah** logged a comment:
> Following up on MKT-4407: Looking at the Q3 data so far, Collectibles return rates jumped from our usual 9.8% baseline up to 11.2% during the peak of the August counterfeit wave. However, since Lucia's enforcement actions and the early GradeSure pilot onboarding started rolling out, we're seeing early stabilization indicators. If we look at the seller panel performance mart (`marketplace_seller_performance`), top-tier trusted sellers like `sel_500012` (Timeworn Treasures) actually capitalized on the cleanup, growing their share of sub-vertical GMV enormously—they're pacing to be our #1 Collectibles seller by Q2FY27.

**2025-10-01 11:30 ET** — **sanjay.bhatt** logged a comment:
> Kicking off experiment **`exp_2401`** ("Verified Badge Prominence") today in the Collectibles sub-vertical. We're testing whether displaying the new Acme Verified badge with high visual prominence in search results increases conversion rate for verified listings while suppressing click-through on unverified or high-risk listings. Will run this through November 15th to catch the early peak shopping window.

**2025-10-15 16:50 ET** — **lucia.ferreira** logged a comment:
> Status update for mid-October review: The counterfeit-listing spike of August has largely been contained through a combination of manual T&S policing, the `sel_500089` suspension (which remains locked while they complete their document audit—scheduled for possible reinstatement review around January if compliance requirements are met), and the GradeSure integration. 
> 
> *Tangential Slack note from the breakroom earlier:* Does anyone know if the cafeteria is doing the pumpkin spice catering again this Thursday, or is that only on the 4th floor? Anyway, back to the epic: Collectibles GMV for Q3FY26 is now projected to land around $61M (massive growth from the $22M-$25M baseline earlier in the year), and our return rate is finally stabilizing downward. Leaving this epic open through the rollout of `exp_2401` and the full badge deployment next month.

---
