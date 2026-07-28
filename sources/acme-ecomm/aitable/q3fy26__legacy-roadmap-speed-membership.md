---
title: "Aitable roadmap export: Speed and Membership initiative cards (legacy tracker)"
source_url: "internal://acme-ecomm/aitable/q3fy26__legacy-roadmap-speed-membership"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2025-10-15T12:00:00+00:00'
adapter: aitable_card
---

# Aitable Export: Speed (Fulfillment) & Membership Initiative Cards (Legacy Tracker)
**Export Date:** 2025-10-15 (Q3FY26)  
**System Administrator:** nadia.esposito (Product Ops)  
**Source System:** Aitable (`acme_aitable_legacy.speed_membership_cards`)  

*Note from Product Ops (nadia.esposito):* Please remember that while conversations are ongoing about eventually migrating these legacy Aitable roadmap cards over to Jira (the consolidation project kicked off earlier this year, though it is far from complete across all verticals), Aitable remains the official system of record for Q3FY26 planning artifacts and ideation cards. Do not archive or deprecate boards without checking with the vertical leads first. 

---

## SECTION 1: SPEED & FULFILLMENT INITIATIVES (`vertical_code: SPEED`)
*Primary Owner / Stakeholder:* tara.oduya (Director PM Speed & Fulfillment, assoc_100140), leo.brandt (Sr PM Delivery Promise, assoc_100141). 

### Card ID: SPD-101
* **Title:** Wider Promise Window & Dynamic Buffer Testing
* **Owner:** leo.brandt
* **Status:** In-Progress (Planning / Scoping)
* **Target Quarter:** Q4FY26 / Q1FY27
* **Linked PRD:** `confluence://acme-ecomm/speed/wider-promise-window-prv2`
* **Description / Notes:** Investigating whether dynamically widening the quoted delivery window by 24–48 hours during peak periods protects our ship-to-home on-time metrics without harming conversion. Initial data from last week's traffic audit suggests we need to carefully separate window adjustments from concurrent DC operations. Also touches on baseline validation checks similar to the ones wei.hartono ran back in February. 
* **Comments:** 
  - *leo.brandt (2025-10-02):* Need to make sure we don't repeat the communication lags we saw during the summer logistics friction. Gabriel Stroud's team at the DCs needs to sign off on the throughput models before we push this to staging.
  - *tara.oduya (2025-10-10):* Approved for Q4 simulation. Keep an eye on how this interacts with the upcoming peak holiday rush starting November 1st.

### Card ID: SPD-102
* **Title:** Pickup Perks (BOPIS / Curbside) Discount Integration
* **Owner:** tara.oduya
* **Status:** Planned
* **Target Quarter:** Q4FY26
* **Linked PRD:** `confluence://acme-ecomm/speed/pickup-perks-bopis-discount`
* **Description / Notes:** Exploring targeted cart-level incentives for customers selecting buy-online-pickup-in-store (BOPIS) or curbside pickup to shift mix share away from costly ship-to-home channels.
* **Comments:**
  - *gabriel.stroud (2025-09-18):* Store fulfillment nodes are already seeing high utilization on weekends. If we incentivize BOPIS too aggressively without expanding staging capacity, we're going to bottleneck the supercenters. Let's coordinate with the store operations leads.

### Card ID: SPD-103
* **Title:** DC Sortation Automation Phase 1 (FON2 & JOL1)
* **Owner:** gabriel.stroud (Fulfillment Ops Lead)
* **Status:** Shipped / Operational
* **Target Quarter:** Q2FY26 / Q3FY26
* **Linked PRD:** `confluence://acme-ecomm/fulfillment/dc-automation-fon2-jol1`
* **Description / Notes:** Mechanical sorting upgrades at Fontana (FON2) and Joliet (JOL1) fulfillment centers.
* **Comments:**
  - *gabriel.stroud (2025-08-15):* Phase 1 is live. Throughput looks solid, though we had that minor 36-hour winter weather disruption scare at JOL1 back in August that we managed to route around. Cost-per-order trends are starting to show the expected efficiency gains.

---

## SECTION 2: MEMBERSHIP INITIATIVES (`vertical_code: MEMBERSHIP`)
*Primary Owner / Stakeholder:* renee.kowalski (SVP Membership, assoc_100040), simone.laurent (Director PM Membership, assoc_100150), derek.holloway (Sr PM Membership Benefits & CLTV, assoc_100151).

### Card ID: MEM-201
* **Title:** Acme+ Streaming Perk Integration (Vidora Partnership)
* **Owner:** renee.kowalski / derek.holloway
* **Status:** Shipped (Live)
* **Target Quarter:** Q2FY26
* **Linked PRD:** `confluence://acme-ecomm/membership/vidora-streaming-bundle-launch`
* **Description / Notes:** Bundling the Vidora streaming service into all monthly and annual Acme+ plans at no extra cost, following the major rollout back on June 1st, 2025. 
* **Comments:**
  - *derek.holloway (2025-07-12):* Early retention numbers look very promising for multi-benefit adopters, though awareness is still hovering around 34%. We need a dedicated onboarding flow to drive awareness before renewal season hits.
  - *simone.laurent (2025-08-01):* Let's make sure the upcoming Fall Savings promo (kicking off September 20th) explicitly highlights the streaming perk in the hero banners.

### Card ID: MEM-202
* **Title:** Benefit Onboarding Carousel & User Engagement Flow
* **Owner:** derek.holloway
* **Status:** In-Progress (Design & Experimentation)
* **Target Quarter:** Q3FY26 / Q4FY26
* **Linked PRD:** `confluence://acme-ecomm/membership/benefit-onboarding-carousel-spec`
* **Description / Notes:** Designing an interactive onboarding carousel for newly signed-up Acme+ members to expose them to under-utilized perks (free shipping, early access, streaming).
* **Comments:**
  - *derek.holloway (2025-10-04):* Wireframes are ready. Aiming to spin up the experiment variant early next quarter. Will coordinate with data analytics (wei.hartono and amara.shah) to ensure panel joins on `dim_member` correctly handle dormant accounts and avoid the `COALESCE` errors we saw during the BigQuery flat-path migration back in March.

### Card ID: MEM-203
* **Title:** Customer Lifetime Health Score (CLHS) Composite Model
* **Owner:** derek.holloway / renee.kowalski
* **Status:** Parked / Draft (On Hold)
* **Target Quarter:** FY27 Planning
* **Linked PRD:** `confluence://acme-ecomm/membership/clhs-composite-scoring-draft`
* **Description / Notes:** Proposal for a unified composite membership-health score combining renewal probability, benefit adoption count, and CSAT interaction history.
* **Comments:**
  - *carlos.figueroa (2025-09-10):* Marking this as parked for now. Data engineering bandwidth is entirely tied up with the core marts and MBR reporting packs this quarter. Let's keep using `member_cltv` and existing benefit-adoption metrics as our shipped proxy until FY27. Do not cite any CLHS scores in executive decks—they don't exist yet!

---

## SECTION 3: GENERAL ROOM CHATTER & IT Ops Sidelines
* **Slack excerpt (channel: `#prod-ops-standup`, 2025-10-14):**
  - *nadia.esposito:* Friendly reminder that if anyone is still creating new roadmap entries directly in Aitable instead of creating Jira epics, please stop. The migration adapter is only syncing one-way right now.
  - *tara.oduya:* Understood, Nadia. Moving the Speed backlog over by end of week. By the way, are we bringing donuts to the Tampa team sync tomorrow or what?
  - *leo.brandt:* Only if someone fixes the coffee machine in the 3rd floor kitchenette first. It’s been throwing error codes since carlos.figueroa's promotion announcement.
  - *carlos.figueroa:* Hey, my promotion to VP didn't break the espresso machine! That's strictly a facilities issue. Check with office ops.

---
