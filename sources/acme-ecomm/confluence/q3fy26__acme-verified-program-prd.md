---
title: "Confluence PRD: the 'Acme Verified' authenticity-badge program"
source_url: "internal://acme-ecomm/confluence/q3fy26__acme-verified-program-prd"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2025-10-15T12:00:00+00:00'
adapter: confluence_page
---

# PRD: 'Acme Verified' Authenticity-Badge Program

**Author:** lucia.ferreira (Trust & Safety Lead, Marketplace, assoc_00320)  
**Status:** In Review / Pre-Launch Run-up (Target Launch: 2025-09-08)  
**Vertical:** MARKETPLACE (COLLECTIBLES / RESOLD)  
**Reviewers:** victor.okonkwo, felix.arroyo, sanjay.bhatt, noah.kessler, carlos.figueroa  

---

## 1. Executive Summary & Background

Following the viral vintage-card auction surge on August 4, 2025, which triggered an unprecedented influx of new buyer traffic and a parallel spike in bad-faith counterfeit-listing attempts across the Collectibles sub-vertical, Marketplace Trust & Safety has been operating at maximum capacity. We saw immediate fallout, culminating in the formal suspension of Bramblewood Vintage (`sel_500089`) on September 2, 2025, after standard spot-checks confirmed multiple egregious counterfeit-listing violations. 

While top-tier established sellers like Timeworn Treasures (`sel_500012`) have benefited from the organic boom in Collectibles (pushing category GMV significantly above last year's baseline), buyer trust remains dangerously vulnerable to rogue listings. The current manual moderation queue is backlogged by 340%, and reactive enforcement is no longer scaling. 

This PRD outlines the product requirements, partner selection rationale, badging UX, rollout phasing, and success metrics for **Acme Verified**—a programmatic pre-listing and post-intake authentication scheme built in partnership with **GradeSure**, targeting an initial rollout across Collectibles on **September 8, 2025**.

---

## 2. Problem Statement & Motivation

1. **Rampant Counterfeiting in Collectibles:** The viral event on August 4 exposed systemic vulnerabilities in our unverified intake pipeline. Bad actors flooded the platform with unauthenticated high-ticket sports and trading cards.
2. **Operational Bottleneck:** Trust & Safety investigators (including newer team members who joined in the urgent backfill wave following the August crisis) are spending 80% of their shift manually reviewing flagged listings rather than auditing high-risk seller accounts.
3. **Elevated Return and Dispute Rates:** Collectibles return rates spiked from 9.8% toward double digits in Q2FY26 / early Q3FY26 due to buyer disputes over item authenticity. If unaddressed, this threatens the long-term viability of the sub-vertical's projected GMV growth.

---

## 3. Partner Selection: Why GradeSure?

We evaluated three external authentication vendors over a compressed 14-day evaluation window: AuthGuard, VerifyCorp, and GradeSure. 

* **API Latency & SLA:** GradeSure guaranteed a sub-400ms webhook response time for digital certificate lookups, critical for preventing cart abandonment during high-traffic drops.
* **Physical-Digital Binding:** GradeSure's tamper-evident NFC/QR micro-tagging integration allows sellers (such as Silverline Card Co., `sel_500200`, and smaller intake operations like Heirloom & Co., `sel_500201`) to pre-certify high-value inventory before shipping to our fulfillment nodes or via `ship_with_acme`.
* **Coverage:** GradeSure holds deep institutional verification databases across sports memorabilia, vintage TCGs, and emerging collectibles categories, whereas competitors lagged significantly in trading card historical pricing and variant identification.

---

## 4. Program Mechanics & Badge Design

The **Acme Verified** badge will appear as a distinctive blue holographic shield icon (`lst_verified_v1`) directly adjacent to the listing title and seller handle across web, app, and kiosk views.

- **Intake Flow for Sellers:** 
  1. Seller submits listing details and GradeSure certificate ID.
  2. Automated API validation cross-references GradeSure's secure registry.
  3. Upon successful match, `fact_marketplace_listings.authenticity_verified` is set to `TRUE`, and the badge is dynamically rendered on the PDP.
- **Enforcement Action for Failures:** Listings failing automated verification or flagged during random spot audits are immediately quarantined to `status = 'suspended'`, and the seller's account is routed to Lucia Ferreira's T&S queue for review (similar to the workflow applied during the Bramblewood Vintage escalation).

---

## 5. Rollout Plan & Phasing

- **Phase 1 (2025-09-08):** Soft launch across top 50 Collectibles sellers by GMV (including Timeworn Treasures, `sel_500012`, and Silverline Card Co., `sel_500200`). Mandatory for items priced over $250.
- **Phase 2 (2025-09-22):** Expansion to all active Collectibles listings regardless of price point.
- **Phase 3 (Q4FY26 / October-November):** Evaluation for potential cross-pollination into select high-risk segments of Resold (e.g., high-end luxury vintage apparel overlapping with ReWear Collective, `sel_500204`, though current consensus is to stabilize Collectibles first).

*Note from product ops:* Nadia Esposito (`nadia.esposito`) reminds the team that all Jira epic tracking for this rollout must be synchronized post-January 15 as part of the broader Aitable-to-Jira roadmap migration, but for this Q3 launch sprint, Confluence remains the primary source of truth.

---

## 6. Success Metrics & Return-Rate Reduction Target

The primary quantitative objective of the Acme Verified program is a decisive compression of return rates and dispute claims in the Collectibles sub-vertical.

- **Baseline:** Collectibles return rate stood at approximately 11.2% during the peak counterfeit spike of Q3FY26.
- **Target:** Drive the Collectibles return rate down to **5.4%** or lower by the end of Q2FY27.
- **Secondary KPIs:** 
  - Zero unverified high-ticket fraudulent listings surviving past 24 hours post-launch.
  - T&S manual review queue reduction by at least 45% within 30 days of Phase 2 rollout.
  - Neutral to positive conversion impact on badged listings (to be measured via subsequent experiment readouts similar to Sanjay Bhatt's planned badge prominence tests).

---

## 7. Operational Sidebar & Tangents (Internal Noise)

* **Standup Note:** Carlos Figueroa (`carlos.figueroa`) mentioned in the Data & Analytics standup that data engineering needs to ensure `fact_marketplace_listings` properly indexes the new `authenticity_verified` boolean before the Monday MBR deck locks. Amara Shah (`amara.shah`) is coordinating the Finance view.
* **Office Logistics:** Reminder that the 3rd-floor West conference room is booked for the GradeSure technical alignment call on Wednesday at 10:00 AM ET. Coffee and pastries will be provided courtesy of the Marketplace vertical team budget.
* **Lunch Coordination:** Ines Delgado (`ines.delgado`) is organizing a quick team lunch for the T&S group on Friday to celebrate getting through the initial policy documentation phase. Please DM dietary restrictions to her Slack handle.

---
