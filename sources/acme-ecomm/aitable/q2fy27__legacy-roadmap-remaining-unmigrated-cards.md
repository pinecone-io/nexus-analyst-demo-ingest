---
title: "Aitable roadmap export: remaining pre-2026-01-15 cards still not migrated to Jira"
source_url: "internal://acme-ecomm/aitable/q2fy27__legacy-roadmap-remaining-unmigrated-cards"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: aitable_card
---

# Aitable Legacy Roadmap Export — Unmigrated Cards Audit (Q2FY27)
**Export Generated:** 2026-07-20  
**Administered By:** `nadia.esposito` (Product Operations)  
**Data Source:** `aitable_card` adapter / legacy Aitable base `app_acme_roadmap_pre26`  
**System Note:** Per the roadmap consolidation decision made back on **2026-01-15** (`nadia.esposito`'s cutover to Jira), all active product and engineering initiatives were supposed to have been migrated. This export covers the genuine long tail of cards *still* sitting in Aitable as of today (2026-07-20). Some are abandoned/stale (no updates in many months); a few represent active or semi-active ideation items whose owners simply never bothered with the administrative Jira migration ticket. 

If an analyst queries *only* Jira, these items remain entirely invisible. This document exists to make that partial-roadmap blind spot concrete.

---

## 1. Executive Summary & Migration Status Overview

Total legacy Aitable cards remaining in unmigrated status: **34 cards**  
- **Abandoned / Stale (>180 days no update):** 22 cards  
- **Active / Ideation Backlog (referenced in ad-hoc discussions or local team docs):** 12 cards  
- **Vertical Breakdown:** Speed (2), Membership (2), Care (3), Marketplace (3), US_CONV (2).

---

## 2. Detailed Card Inventory (Unmigrated Aitable Records)

### [CARD-881] Speed / Fulfillment: Regional DC Sorter Conveyor Retrofit (JOL1/FON2)
- **Original Created Date:** 2025-10-14
- **Last Modified:** 2025-12-19
- **Owner:** `gabriel.stroud`
- **Vertical:** `SPEED`
- **Status in Aitable:** `In Review (Stale)`
- **Card Description:** Proposal to add secondary loop sorters to Joliet (JOL1) and Fontana (FON2) to handle peak sortation bottlenecks.
- **Ops Note:** *archival artifact* — this card was superseded in practice by the actual DC sortation automation Phase 1 work that kicked off on **2026-01-12** (managed directly via Jira and operational runbooks). Gabriel never migrated the card because the physical implementation was already in motion by the time Nadia's January consolidation project started.

### [CARD-902] Speed / Fulfillment: Predictive Packaging Size Selection for Fragile Shipments
- **Original Created Date:** 2025-11-02
- **Last Modified:** 2026-01-04
- **Owner:** `leo.brandt`
- **Vertical:** `SPEED`
- **Status in Aitable:** `Ideation`
- **Card Description:** Use dimensional weight data to automatically suggest bubble-mailer vs corrugated box sizing on ship-to-home orders to cut dimensional surcharges.
- **Notes from Slack aside (`leo.brandt` to `tara.oduya`, 2026-03-12):** "Is this card still anywhere? Oh, right, it's rotting in Aitable. Let's just leave it there until we have Q3 planning bandwidth; nobody's looking at Aitable anyway since the Jira cutover back in January."

### [CARD-712] Membership: Acme+ Family Sharing Tier (Multi-Account Household Billing)
- **Original Created Date:** 2025-06-18
- **Last Modified:** 2025-09-10
- **Owner:** `derek.holloway`
- **Vertical:** `MEMBERSHIP`
- **Status in Aitable:** `Parked`
- **Card Description:** Explore extending annual membership benefits (free shipping, early access, streaming perk) to up to 3 secondary household members under one subscription fee.
- **Context:** Parked around the same time the Customer Lifetime Health Score (CLHS) model was parked in draft status on **2025-09-10** (`carlos.figueroa` / `derek.holloway`). Never migrated to Jira because CLTV and benefit onboarding (such as the recent `exp_2556` Benefit Onboarding Carousel experiment that wrapped up in June 2026) took absolute priority.

### [CARD-745] Membership: Automated Win-Back SMS Sequence for Cancelled Members
- **Original Created Date:** 2025-07-22
- **Last Modified:** 2025-11-15
- **Owner:** `simone.laurent`
- **Vertical:** `MEMBERSHIP`
- **Status in Aitable:** `Drafting`
- **Card Description:** Triggered SMS campaign offering a 20% renewal discount 30 days post-cancellation for annual Acme+ members who didn't renew.
- **Notes:** Simone moved this logic into the marketing calendar workflows ( campaña `camp_90214` adjustments) rather than building a dedicated Jira epic. The Aitable card remains as an unmigrated ghost record.

### [CARD-621] Customer Care: Self-Service Address Modification Post-Checkout
- **Original Created Date:** 2025-04-10
- **Last Modified:** 2025-08-30
- **Owner:** `aisha.rahman`
- **Vertical:** `CARE`
- **Status in Aitable:** `Backlog`
- **Card Description:** Allow customers to update their shipping address via chat bot or account portal within 15 minutes of order placement without contacting an agent.
- **Status Check:** Partially absorbed into the "Ask Acme v2" bot updates (which launched back on **2025-09-15** under `dominic.paquet` and `aisha.rahman`), but this specific unverified card still sits unmigrated.

### [CARD-654] Customer Care: Automated Refund Status Tracker Widget in Chat
- **Original Created Date:** 2025-05-14
- **Last Modified:** 2025-10-12
- **Owner:** `julian.moss`
- **Vertical:** `CARE`
- **Status in Aitable:** `Ideation`
- **Card Description:** Expose real-time return processing center check-in scans directly inside the chat widget so customers asking about refunds don't have to wait for agent lookups.
- **Historical Relevance:** Highly relevant given the Ontario returns center staffing crisis and the resulting Medallia refund-delay verbatim spike that crossed 10% back on **2025-12-15**, and subsequently breached the 5.0-day SLA on **2026-01-05** (`hannah.brennan`). Julian never migrated this card to Jira because operational fire-fighting took precedence during the Q4 peak and Q1 MBR escalation (`2026-02-02`).

### [CARD-689] Customer Care: VIP Priority Routing for Multi-Year Acme+ Members
- **Original Created Date:** 2025-06-02
- **Last Modified:** 2025-08-01
- **Owner:** `dominic.paquet`
- **Vertical:** `CARE`
- **Status in Aitable:** `Stale`
- **Card Description:** Route inbound calls and chats from members with >3 years tenure directly to Tier-2 specialized agents with zero bot queue.

### [CARD-512] Marketplace: Automated Counterfeit Image-Fingerprinting Tool
- **Original Created Date:** 2025-03-01
- **Last Modified:** 2025-08-06
- **Owner:** `lucia.ferreira`
- **Vertical:** `MARKETPLACE`
- **Status in Aitable:** `Drafting`
- **Card Description:** Run incoming listing images against known stock-photo databases to catch fraudulent luxury and collectible listings before publication.
- **Context:** Written right around the time of the viral vintage-card auction spike on **2025-08-04** that triggered the massive Collectibles counterfeit surge (`lucia.ferreira`). Superseded almost immediately by the emergency launch of the "Acme Verified" authentication program in partnership with GradeSure on **2025-09-08**. The card was left to rot in Aitable while the GradeSure integration took over all engineering cycles.

### [CARD-533] Marketplace: Bulk CSV Listing Template for Resold Apparel Sellers
- **Original Created Date:** 2025-04-15
- **Last Modified:** 2025-09-20
- **Owner:** `noah.kessler`
- **Vertical:** `MARKETPLACE`
- **Status in Aitable:** `Backlog`
- **Card Description:** Enable Resold sub-vertical sellers (such as *Loop Resale Collective* `sel_500061` and *ReWear Collective* `sel_500204`) to upload inventory spreadsheets rather than single-item forms.
- **Cross-Reference:** Directly touches on the `listing-setup-complexity` verbatim theme captured in the newer Seller Pulse surveys (`fact_seller_voc_responses`, managed by `camille.duarte` since she joined on **2026-04-08`). Despite being a real seller pain point, this card remains stranded in legacy Aitable.

### [CARD-567] Marketplace: Category-Level Price Elasticity Dashboard for Sellers
- **Original Created Date:** 2025-05-20
- **Last Modified:** 2025-10-05
- **Owner:** `sanjay.bhatt`
- **Vertical:** `MARKETPLACE`
- **Status in Aitable:** `Ideation`
- **Card Description:** Expose aggregate category pricing trends to Collectibles and Style sellers to help them price competitive items.
- **Context:** Relates to the `no-performance-visibility` theme in seller VOC. Unmigrated.

### [CARD-402] US Conversion & Traffic: Dynamic Currency Conversion for MX/CA Cross-Border Browsing
- **Original Created Date:** 2025-02-10
- **Last Modified:** 2025-07-15
- **Owner:** `owen.faust`
- **Vertical:** `US_CONV`
- **Status in Aitable:** `Stale`
- **Card Description:** Auto-detect visitor location and display localized CAD/MXN pricing estimates while maintaining USD settlement in the background.
- **Note:** Currency conversion conventions in the warehouse (`*_usd` columns are already FX-converted monthly averages) mean local currency display is strictly a front-end rendering feature. This card was abandoned when FX priorities shifted.

### [CARD-431] US Conversion & Traffic: One-Tap Guest Checkout with Apple Pay / Google Pay Deep Integration
- **Original Created Date:** 2025-03-12
- **Last Modified:** 2025-11-20
- **Owner:** `maya.lindqvist`
- **Vertical:** `US_CONV`
- **Status in Aitable:** `Parked`
- **Card Description:** Surface wallet payment buttons directly on the product detail page (PDP) above the fold.
- **Ops Note:** Elements of this ideation fed informally into the "Checkout Simplify" experiment (`exp_2214`, run by `owen.faust` between **2026-02-16** and **2026-03-30**, which shipped on the confounded +2.1% headline lift on **2026-04-06**). However, the original Aitable card was never migrated to Jira, demonstrating how legacy ideation documents float untracked alongside formal Jira epics.

---

## 3. Operational Notes from Product Operations (`nadia.esposito`)

As we approach the end of Q2FY27 (today being **2026-07-20**, with the quarter 88% elapsed and pacing toward our $7.62B GMV run-rate), cleaning up these remaining 34 Aitable cards is technically on our backlog, but honestly, nobody cares enough to spend engineering sprint points on archiving dead documentation. 

If anyone runs an audit against Jira and wonders why things like `[CARD-654]` (Care refund tracker) or `[CARD-512]` (AI image fingerprinting) don't appear in the active Jira epics, point them to this export file. The work either happened under a different ticket number, got absorbed into bigger programs (like GradeSure or Ask Acme v2), or was quietly abandoned.

Reminder for the upcoming weekly syncs: do not attempt to query Aitable via API for automated reporting; use Jira for everything post-2026-01-15.

---
