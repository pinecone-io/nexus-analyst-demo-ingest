---
title: "Jira ticket: Bot Handoff Threshold readout — partial ship (non-billing only)"
source_url: "internal://acme-ecomm/jira/q2fy27__exp-bot-handoff-threshold-readout-partial-ship"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: jira_ticket
---

**Issue Key:** CARE-3812  
**Project:** Customer Care Core & Automation (CARE)  
**Epic:** `EPIC-882` (Ask Acme v2 Bot Optimization & Deflection Goals)  
**Status:** Done (Partial Ship)  
**Assignee:** `aisha.rahman` (`assoc_100130`)  
**Reporter:** `dominic.paquet` (`assoc_100310`)  
**Created:** 2026-04-01  
**Resolved:** 2026-05-20  
**Priority:** P1 - High  
**Components:** `bot_handoff`, `deflection`, `csat_monitoring`, `ask_acme_v2`

---

### Description

Closing out the loop on `exp_2489` ('Bot Handoff Threshold'), which kicked off at the start of Q1FY27 (back on `2026-04-01` under hannah.brennan's overarching quarterly OKRs for Care deflection). As a quick reminder of the test parameters: `exp_2489` was designed to evaluate whether relaxing the strict conversational triggers in *Ask Acme v2*—specifically pushing users to stay within the bot automation flow for an extra turn or two before routing to a live human agent—would meaningfully bump our deflection rate without completely destroying user sentiment. 

As we saw earlier this year with the post-peak recovery (and recalling the messy data around the Q4 refunds backlog that Giulia and Hannah walked us through back in February when the Ontario returns center was drowning), we have to be extremely careful about making deflection look good on paper at the direct expense of customer goodwill. 

The full readout for `exp_2489` completed on **2026-05-15**. The quantitative results are locked in BigQuery (`nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`), and the net trade-off is stark enough that we cannot justify an unconditional 100% rollout. 

---

### Key Readout Metrics (`exp_2489`, as of 2026-05-15)

*   **Deflection Rate Impact:** **+3.3pp** lift across the test cohort (moving from our pre-experiment baseline of ~49.6% toward the FY27 exit goal of 50.0%+).
*   **CSAT Impact (General Users):** Statistically neutral (-0.02, within noise bounds).
*   **CSAT Impact (Late-Escalated / High-Complexity Users):** **-0.15 CSAT drop** among the subset of users who ultimately broke through the bot and reached a live agent after being held in the automated flow longer. 
*   **Handle Time (Agent-Assisted):** Flat to slightly up (+0.4 minutes for agents picking up frustrated late-escalated chats).

---

### Comments

**`aisha.rahman`** *(2026-05-15 14:22 EST)*  
Just attached the full cohort breakdown spreadsheet to the Confluence page. Let's look at the numbers honestly rather than trying to spin this as an unalloyed win. 

The +3pp deflection gain is real, and operationally it helps us keep pace with the Q2 contact volume we're seeing across web and app channels. But the -0.15 CSAT penalty among late-escalated users is concentrated entirely in specific intent categories. When someone is trying to check order status or track a shipment, staying stuck in the bot an extra turn is an annoyance. When someone has a billing dispute, a pricing error, or an unauthorized charge, keeping them away from a human agent makes them furious. 

If we ship this globally right now, we are going to bleed CSAT in exactly the areas where customer trust is already fragile. 

---

**`dominic.paquet`** *(2026-05-15 16:45 EST)*  
Agree 100%, Aisha. Looking at the Medallia verbatims tagged to `post_care_contact` for the test arm during the last six weeks, the negative sentiment spikes are heavily skewed toward billing and payment-related intents. 

Remember how painful the refund-delay messaging was back in January when the Ontario returns center was running 22% understaffed? (Shoutout to Giulia and Hannah for getting that sorted out by February, but it left a mark on user patience). If we trap people trying to resolve financial/billing questions inside the bot loop just to juice our deflection metrics, we're asking for another VOC spike. 

Can we scope a partial rollout? What if we apply the relaxed threshold *only* to non-billing categories (e.g., general FAQs, store hours, basic membership info, catalog lookup) and explicitly hold back billing-related contacts?

---

**`hannah.brennan`** *(2026-05-18 09:10 EST)*  
@dominic.paquet @aisha.rahman — I like Dominic's proposal. Let's run the numbers on a non-billing-only carve-out. 

Felix and Deborah are tracking our Care exit goals closely for the MBR deck, and while hitting 50%+ deflection is an explicit FY27 target (we're pacing around 52.1% QTD right now), leadership has agreed that we shouldn't sacrifice customer satisfaction metrics in high-sensitivity categories to get there. 

Aisha, can your team prep a patch for the routing logic that restricts `exp_2489`'s relaxed threshold parameters to non-billing taxonomies? Let's aim to review and execute a partial ship by Wednesday (2026-05-20) if engineering sign-off is clean.

---

**`aisha.rahman`** *(2026-05-20 11:35 EST)*  
Patch is tested in staging and pushed to production as of 11:00 AM today (`2026-05-20`). 

**Decision locked:** We are partially shipping `exp_2489`. 
*   **Included Categories (Relaxed Handoff Threshold Live):** General shipping queries, store pickup (BOPIS/curbside) instructions, product catalog navigation, Acme+ general benefits FAQs (shipping discounts, early access rules), and standard return policy inquiries.
*   **Excluded / Held Back (Strict / Legacy Handoff Threshold Maintained):** Billing, payment processing disputes, gift card redemption errors, active chargeback inquiries, and any sensitive membership billing cycles (annual renewal fee disputes, paused plan billing adjustments).

Updating the epic status to Done (Partial Ship). I'll monitor the cohort dashboards over the next two weeks to ensure the CSAT penalty among late-escalated users evaporates once we exclude the billing tier. If the numbers look stable, we'll lock this into the baseline for Q3.

---
