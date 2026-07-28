---
title: "Jira backlog export: Resold's complete current initiative list (5 items)"
source_url: "internal://acme-ecomm/jira/q2fy27__resold-marketplace-backlog-current-initiatives"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: jira_ticket
---

# JIRA BOARD EXPORT: PROJECT RESOLD [CROSS-VERTICAL INITIATIVES]
**Board View:** Marketplace Resold Active Sprints & Backlog  
**Project Lead:** `noah.kessler` (Sr PM Marketplace Resold, `assoc_100122`)  
**Export Date:** Monday, 2026-07-20 (Q2FY27 In-Flight)  
**Total Open Initiatives:** Exactly 5 items (Exhaustive snapshot per product operations audit requirements; post-Aitable migration parity check confirmed)

---

## Sprint Metadata & System Notes
*Note from `nadia.esposito` (Head of Product Ops):* Per the ongoing Aitable-to-Jira roadmap consolidation project kicked off back on 2026-01-15, all legacy cards for Resold have been fully purged or ported. This export represents the complete and exclusive set of open initiatives currently owned by the Resold vertical as we approach the final weeks of Q2FY27. No hidden epics or ghost backlogs exist outside this board. 

As discussed following the April MBR and victor.okonkwo's Marketplace category-mix synthesis (which put to rest the old abandoned Style recovery draft from Q1), Resold's roadmap is tightly calibrated to capture the ongoing recommerce acceleration—exemplified by top-tier sellers like `sel_500061` (Loop Resale Collective) and mid-tier stalwarts like `sel_500147` (Harlow & Finch)—while actively resolving seller friction points that surface in our newer seller cohorts.

---

## Active Epic List (5 Items)

### 1. RES-401: Condition-Grading Rubric v2 (Seller Self-Assessment)
* **Epic Key:** `RES-401`
* **Status:** In Progress (Active Sprint)
* **Target Quarter:** Q3FY27
* **Assignee:** `noah.kessler` (`assoc_100122`)
* **Reporter:** `camille.duarte` (`assoc_100123`, Sr PM Marketplace Seller Experience)
* **Description:**  
  Refinement and expansion of the v1 seller self-assessment condition-grading framework for pre-owned apparel and accessories. Current buyer-side Medallia verbatims continue to flag incidental item-accuracy disconnects across Marketplace sub-verticals (notably Style's 14% and Resold's 12% `listing-accuracy-gap` share, per Giulia Romano's Medallia theme-share pull from 2026-07-08). While Collectibles relies heavily on the GradeSure authentication partnership (`sel_500089` compliance history notwithstanding), Resold and Style require a robust, standardized digital rubric that allows sellers to self-certify item wear levels (e.g., "Like New," "Gently Loved," "Well Worn") with guided photo prompts. 
  
  *Acceptance Criteria:* 
  * Updated interactive wizard in the seller portal during item creation.
  * Reduction in seller-disputed return rates for "item not as described" (INAD) in Resold category.
  * Alignment with camille.duarte's broader Seller Listing and Optimization workflow improvements.

---

### 2. RES-402: Trade-In / Buyback Pilot for Owned Inventory
* **Epic Key:** `RES-402`
* **Status:** Grooming / Architecture Review
* **Target Quarter:** Q4FY27 (Peak Prep)
* **Assignee:** `noah.kessler` (`assoc_100122`)
* **Reporter:** `victor.okonkwo` (`assoc_100030`, SVP Marketplace)
* **Description:**  
  Scoping a closed-loop trade-in and direct buyback program where Acme acquires pre-owned apparel directly from shoppers or trusted third-party Resold partners (such as `sel_500204` ReWear Collective) to seed owned-inventory pools. This initiative bridges the gap between traditional 1P retail and 3P resale, leveraging our DC network (`node_type='returns_center'` infrastructure like the Ontario, CA facility once its post-peak staffing stability under hannah.brennan was secured earlier this year). 
  
  *Technical Notes:*  
  Requires coordination with `gabriel.stroud` on returns-center receiving workflows and valuation scanning stations. Initial financial modeling suggests a Q4 soft launch in select US markets.

---

### 3. RES-403: Authentication-Partnership Scoping (Apparel-Focused, Non-GradeSure)
* **Epic Key:** `RES-403`
* **Status:** Discovery / Vendor Evaluation
* **Target Quarter:** Q4FY27
* **Assignee:** `noah.kessler` (`assoc_100122`)
* **Reporter:** `lucia.ferreira` (`assoc_100320`, Trust & Safety Lead)
* **Description:**  
  *Explicitly NON-GradeSure.* (Note for auditing teams: Collectibles utilizes the Acme Verified / GradeSure program launched back on 2025-09-08, which successfully brought Collectibles return rates down to 5.4% by Q2FY27 despite creating onboarding authentication friction for new collectible sellers like `sel_500241` vs `sel_500242`). 
  
  This epic covers the active evaluation and RFP process for a separate, apparel-and-luxury-focused third-party authentication partner tailored specifically to Resold high-end garment categories. As Resold’s apparel/style-adjacent share climbed from 51% to 62% YoY (driving part of the Marketplace wallet-share shift alongside Style's +6.1% Q1FY27 YoY deceleration), establishing a seamless verification protocol for luxury streetwear and designer resales without repeating Collectibles' steep onboarding drop-off is paramount.

---

### 4. RES-404: Seller Payout-Speed Improvement
* **Epic Key:** `RES-404`
* **Status:** In Progress (Engineering Sprint 14)
* **Target Quarter:** Q3FY27
* **Assignee:** `noah.kessler` (`assoc_100122`)
* **Reporter:** `felix.arroyo` (`assoc_100010`, SVP Product & Growth)
* **Description:**  
  Reduction of seller payout settlement latency from current 7-day rolling window post-delivery down to 48-hour post-scan verification. Tied to the broader marketplace seller retention goals and addressing themes logged in the new Seller Pulse survey program (`fact_seller_voc_responses`, managed by `camille.duarte` since its April launch). 
  
  *Dependencies:*  
  Coordination with Payments vertical (`dim_vertical` PAYMENTS / DS dispute & settlement layer) and treasury to ensure escrow risk models remain compliant across US, CA, and MX markets.

---

### 5. RES-405: Category-Mix Reporting for the Style Wallet-Share Shift
* **Epic Key:** `RES-405`
* **Status:** Backlog (Design Phase)
* **Target Quarter:** Q3FY27
* **Assignee:** `noah.kessler` (`assoc_100122`)
* **Reporter:** `amara.shah` (`assoc_100211`, Data Analyst Finance/MBR)
* **Description:**  
  Development of dedicated internal reporting tooling and Compass dashboard widgets to track the cross-vertical category-mix shift between Style and Resold. Following the April 2026 MBR synthesis confirming that Style's Q1FY27 deceleration (+6.1% YoY) was entirely offset by Resold's massive acceleration (+90.9% YoY) due to shoppers shifting wallet share toward recommerce, Resold leadership requires real-time sub-vertical overlap reporting. 
  
  This tooling will ingest data from `marketplace_gmv_summary` and `marketplace_seller_performance` marts to isolate category migration patterns among mid-tier and large sellers (such as Resold's `sel_500204` ReWear Collective and Style's `sel_500103` Kestrel & Vine), ensuring we accurately forecast inventory needs without misinterpreting the shift as a macro demand loss.

---

## Administrative Slack Aside (Attached to Board)
> **[slack_thread // #marketplace-resold-eng]**  
> **noah.kessler [11:14 AM]:** Quick reminder everyone, today's 2 PM grooming is strictly for RES-401 and RES-404. Let's make sure we don't wander off into listing-accuracy rabbit holes—that's a bigger cross-vertical conversation than a Resold sprint grooming session, and it's not on our board this sprint anyway.  
> **camille.duarte [11:16 AM]:** Agreed Noah. I'm chatting with Victor about the overarching seller listing framework next Monday, but let's keep Resold focused on the grading rubric v2 for now.  
> **wei.hartono [11:18 AM]:** Just checked BigQuery—flat dataset path looks clean (`nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`), no nesting issues today. Carry on.
