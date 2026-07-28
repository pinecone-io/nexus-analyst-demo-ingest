---
title: "Jira backlog export: Collectibles' complete current initiative list (5 items)"
source_url: "internal://acme-ecomm/jira/q2fy27__collectibles-marketplace-backlog-current-initiatives"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: jira_ticket
---

# JIRA BOARD EXPORT: MARKETPLACE — COLLECTIBLES VERTICAL
**Board:** Collectibles Core & Growth (COL-KANBAN)  
**Project Key:** COL  
**Owner:** sanjay.bhatt (Sr PM Marketplace Collectibles, `assoc_100120`)  
**Export Date:** 2026-07-20 (Q2FY27 In-Flight)  
**Total Open Initiatives:** 5 (Exhaustive, complete view as of today; per the Aitable-to-Jira roadmap consolidation project initiated back on 2026-01-15 under `nadia.esposito`, legacy ideation cards have been fully transitioned or closed).

---

## Board Filter Status
*   **Quick Filters Applied:** `Status in ("Backlog", "Selected for Development", "In Progress")`, `Assignee = current_user()`
*   **Note on Cross-Vertical Scope:** This board reflects *only* Collectibles' own view. Per enterprise data partitions, Style (managed by `ines.delgado`), Resold (managed by `noah.kessler`), and B2B (managed by `malik.hendon`) maintain entirely separate Jira spaces. No cross-vertical backlog items from Style, Resold, or B2B are represented here, nor does this board include anything addressing listing photo/description/specification accuracy — that's simply outside Collectibles' own scope; check the other verticals' boards directly for their coverage.

---

## Active Initiative List (5 Items)

### 1. COL-1042: GradeSure SLA Renegotiation (Turnaround Time)
*   **Epic:** Fulfillment & Authentication Reliability
*   **Status:** In Progress
*   **Priority:** P1 - High
*   **Target Quarter:** Q3FY27
*   **Assignee:** sanjay.bhatt (`assoc_100120`)
*   **Description:** 
    Following the viral vintage-card auction surge back in August 2025 (`sel_500089` compliance incidents and subsequent spikes), the "Acme Verified" authentication program built on our GradeSure partnership (launched on 2025-09-08 under `lucia.ferreira`) successfully drove Collectibles' return rate down from its Q3FY26 peak of 11.2% to a healthy 5.4% in Q2FY27 QTD. However, operational tracking shows that authentication latency is currently acting as a bottleneck for seller onboarding velocity. 
    
    This initiative covers the formal renegotiation of our enterprise service-level agreement (SLA) with GradeSure to compress average item turnaround time from the current 4.2 business days down to <= 2.5 business days. This is directly tied to mitigating the new-seller attrition cliff identified in our recent cohort analysis (where 46% of new Collectibles sellers churn before reaching listing 5). Speeding up debut-listing verification to sub-7-days doubles 10th-listing survival rates (from 15% to 30%).
*   **Comments (Latest):**
    *   *sanjay.bhatt (2026-07-18):* Had our bi-weekly check-in with GradeSure account reps. They are pushing back on the penalty clauses for sub-2-day rushes during peak holiday windows. We may need to stage the rollout by tier (top-tier sellers like `sel_500012` first, standard tail second).
    *   *lucia.ferreira (2026-07-16):* Make sure we don't loosen verification rigor while leaning on turnaround time. We can't afford a repeat of the counterfeit spikes from last August.

---

### 2. COL-1088: Counterfeit-Detection ML Model v2
*   **Epic:** Trust, Safety & Authentication
*   **Status:** Selected for Development
*   **Priority:** P1 - High
*   **Target Quarter:** Q3FY27
*   **Assignee:** lucia.ferreira (`assoc_100320`) [Co-owned with sanjay.bhatt]
*   **Description:** 
    Upgrade our existing computer-vision and metadata-matching pipeline to model v2. Model v1 successfully caught high-confidence bad-faith actors (such as the actions that led to the suspension of Bramblewood Vintage `sel_500089` back in September 2025), but it suffers from a high false-positive rate on high-end graded sports cards encased in legacy third-party slabs. 
    
    Model v2 integrates automated slab-authenticity OCR and pixel-level hologram verification prior to human GradeSure intake routing. Expected to reduce manual review queue volume by 35% and cut pre-listing friction for vetted sellers.
*   **Comments (Latest):**
    *   *carlos.figueroa (2026-07-12):* Data science pipeline review looks solid. Ensure training sets are scrubbed of the Q3FY26 anomaly spikes so we don't overfit to the vintage-card auction frenzy.

---

### 3. COL-1102: Verified-Badge Visibility Expansion into Search Results
*   **Epic:** Discovery & Search Placement
*   **Status:** In Progress
*   **Priority:** P2 - Medium
*   **Target Quarter:** Q2FY27 / Q3FY27 Transition
*   **Assignee:** owen.faust (`assoc_100111`) [Marketplace engineering support: sanjay.bhatt]
*   **Description:** 
    *Explicitly scope note:* This initiative targets search-placement and visual badge badging **INTO SEARCH RESULTS** and category grid views. It does **NOT** address listing photo, description, or specification accuracy — that's simply out of scope for this particular epic. 
    
    Building upon the success of the "Verified Badge Prominence" experiment (`exp_2401`, run by sanjay.bhatt in Q3FY26, which proved a clean +6.8% conversion lift when applied to item detail pages and shipped to 100% of Collectibles listings on 2025-11-20), this epic injects the GradeSure verified shield directly into the primary US/CA/MX search result cards and filter facets. 
*   **Comments (Latest):**
    *   *owen.faust (2026-07-19):* Working closely with the Search Relevance re-ranking team (`exp_2601` is currently live in US conversion). We need to ensure the badge asset doesn't reflow the mobile search card layout in a way that triggers layout shift metrics.
    *   *sanjay.bhatt (2026-07-14):* Checked the Compass BI tool caches this morning—make sure nobody confuses this search placement work with the separate marketplace GMV restatement ($975.0M canonical for Q4FY26). They live in entirely different reporting tables (`marketplace_gmv_summary` vs `fact_traffic_daily`).

---

### 4. COL-1115: Grading-Fee Subsidy Pilot for Top-100 Sellers Specifically
*   **Epic:** Seller Growth & Liquidity Incentives
*   **Status:** Backlog
*   **Priority:** P2 - Medium
*   **Target Quarter:** Q4FY27
*   **Assignee:** sanjay.bhatt (`assoc_100120`)
*   **Description:** 
    *Explicit scope note:* This pilot is aimed **specifically at established top-100 sellers** (such as our #1 Collectibles seller by Q2FY27 GMV, `sel_500012` Timeworn Treasures, and mid-tier established partners like `sel_500200` Silverline Card Co.), and is explicitly **NOT** aimed at the struggling new-seller onboarding cohort (who face different barriers around setup complexity and initial verification friction). 
    
    The initiative provides a temporary 15% co-pay subsidy on GradeSure bulk authentication fees for top-tier merchants who commit to increasing their active high-value catalog listings by at least 25% ahead of the Q4 holiday peak. Designed to secure category inventory depth and protect our high-growth trajectory (+372.7% YoY in Q1FY27).
*   **Comments (Latest):**
    *   *amara.shah (2026-07-10):* Finance has provisionally signed off on the Q4 promotional envelope for this, provided we maintain our take-rate average of ~13.6%. Let's review the final payout models in next week's MBR prep session.

---

### 5. COL-1140: Category-Taxonomy Expansion: Trading Cards to Memorabilia Subtypes
*   **Epic:** Catalog Architecture & Taxonomy
*   **Status:** Backlog
*   **Priority:** P3 - Low
*   **Target Quarter:** Q4FY27
*   **Assignee:** camille.duarte (`assoc_100123`) [Marketplace Seller Experience / Listing surfaces]
*   **Description:** 
    Expand the Collectibles sub-vertical category tree beyond traditional trading cards (Sports, TCG) to formally support structured attributes for game-worn memorabilia, authenticated comic books, autographed film props, and vintage coin subtypes. 
    
    Currently, sellers dealing in non-card memorabilia must dump items into generic "Other Collectibles" buckets, which hurts search filtering and increases seller-side VOC friction (specifically addressing `listing-setup-complexity` themes logged in our new Seller Pulse survey stream, `fact_seller_voc_responses`).
*   **Comments (Latest):**
    *   *camille.duarte (2026-07-15):* Initial attribute schema drafted. Coordinating with malik.hendon over in B2B to ensure bulk-upload templates don't break wholesale merchant ingest once we push this live.
    *   *sanjay.bhatt (2026-07-11):* Good progress. Let's make sure we schedule a sync with the search team before final publishing so the new facets map correctly into `dim_vertical`.

---

## Sprint Hygiene & Administrative Notes
*   **Standup Schedule:** Every Monday at 09:30 ET via Zoom.
*   **Jira-Aitable Migration Status:** Legacy cards created prior to the 2026-01-15 cutoff are 100% archived in Aitable; all active execution tracking resides strictly in this Jira board. 
*   **Cross-Reference Warning:** If querying BigQuery tables for reporting, remember that `fact_orders` is a ~400k representative sample, whereas full-population aggregations must pull from `marketplace_gmv_summary`. Do not mix buyer VOC (`fact_voc_responses`, Medallia) with seller VOC (`fact_seller_voc_responses`, Seller Pulse); they use completely separate namespaces and survey instruments.

---
