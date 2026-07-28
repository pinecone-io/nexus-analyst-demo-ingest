---
title: "Confluence reference: PM surface-ownership matrix across US_CONV/Style/Resold/Collectibles/B2B, including the Search-PM gap"
source_url: "internal://acme-ecomm/confluence/q2fy27__pm-surface-ownership-reference-and-search-gap"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: confluence_page
---

# Acme Product Management Surface Ownership Reference Matrix

**Author:** `nadia.esposito` (Head of Product Operations, `assoc_100070`)  
**Space:** Product Operations > Strategy & Governance  
**Last Updated:** 2026-07-20  
**Status:** Published / Active Reference  
**Parent Page:** [Q2FY27 Product Organization & Governance Overview](internal://acme-ecomm/confluence/q2fy27__product-org-overview)

---

## 1. Purpose & Context

As Acme continues to scale its omni-channel retail footprint, marketplace sub-verticals, and B2B wholesale operations heading into the back half of FY27, our product organization remains fundamentally structured around dedicated business verticals (such as `US_CONV`, `MARKETPLACE`, `CARE`, `SPEED`, and `MEMBERSHIP`). However, many of our most critical user-facing experiences do not live inside a single vertical silos. They span across multiple sub-verticals, requiring a complementary **Surface Ownership Matrix** to clarify who holds the product pen for key touchpoints like the View Item Page, Search, Seller Listing, and Seller Optimization.

This reference page documents the current baseline of surface ownership across our core consumer-facing and marketplace domains (`US_CONV`, Style, Resold, Collectibles, and B2B). It is intended to be consulted alongside our standard vertical org chart and Jira project hierarchies (following the ongoing Jira-Aitable consolidation project that kicked off back in January under `nadia.esposito`'s team).

---

## 2. The PM Surface-Ownership Matrix

The table below outlines the designated Product Manager ownership for each product surface crossed with our primary vertical and sub-vertical domains. Where a cell is blank or marked `n/a`, it represents a structural boundary of that domain rather than an omission.

| Surface | US_CONV | Style | Resold | Collectibles | B2B |
|---|---|---|---|---|---|
| **View Item Page** | maya.lindqvist (`assoc_100110`) | ines.delgado (`assoc_100121`) | noah.kessler (`assoc_100122`) | sanjay.bhatt (`assoc_100120`) | — *(no consumer item page)* |
| **Search** | owen.faust (`assoc_100111`) | victor.okonkwo (`assoc_100030`, SVP-level) *[See note below]* | victor.okonkwo (`assoc_100030`, SVP-level) *[See note below]* | victor.okonkwo (`assoc_100030`, SVP-level) *[See note below]* | — |
| **Seller Listing** | n/a *(no sellers)* | camille.duarte (`assoc_100123`) | camille.duarte (`assoc_100123`) | camille.duarte (`assoc_100123`) | n/a |
| **Seller Optimization** | n/a | camille.duarte (`assoc_100123`) | camille.duarte (`assoc_100123`) | camille.duarte (`assoc_100123`) | n/a |

---

## 3. Surface Breakdown & Operational Notes

### A. View Item Page (VIP)
* **US_CONV (`maya.lindqvist`):** Owns the core consumer retail item page layout, pricing modules, and the broader item page iteration programs (such as the 6 item page iterations shipped during Q1FY27, covering everything from above-fold price/CTA reflows to mobile sticky add-to-cart bars). Also oversees concurrent in-flight experiments on the surface, including the ongoing `exp_2618` (Item Page Media Carousel Autoplay started June 8, 2026).
* **Style (`ines.delgado`):** Manages vertical-specific merchandising requirements, size-chart integrations, and category-level PDP enhancements for apparel and lifestyle listings.
* **Resold (`noah.kessler`):** Oversees condition-grading display modules, pre-owned authenticity notes, and trade-in callouts on secondary-market item pages.
* **Collectibles (`sanjay.bhatt`):** Owns specialty collectible PDP modules, including the prominent "Acme Verified" badge display which rolled out to 100% of collectibles listings following the successful `exp_2401` readout back in November 2025.

### B. Search — The Acknowledged Marketplace-Wide Search PM Gap
* **US_CONV (`owen.faust`):** Owns core consumer search relevance, autocomplete, and consumer-facing filters for the main retail site (including the in-flight `exp_2601` Search Relevance Re-ranking experiment that kicked off June 8, 2026).
* **Style / Resold / Collectibles (`victor.okonkwo`):** *There is NO dedicated Marketplace-wide Search PM today.* This is a real, acknowledged organizational gap, not an omission from this document. 
  * **Context on the Gap:** Historically, cross-sub-vertical relevance ranking work, multi-category search blending, and specialized marketplace filter logic (e.g., trading card sub-types vs. vintage apparel tags) have been handled on an ad hoc basis by whichever sub-vertical PM raised an operational issue. When cross-vertical conflicts arise regarding search ranking priority between Style, Resold, and Collectibles, `victor.okonkwo` (SVP Marketplace, `assoc_100030`) arbitrates at the SVP level.
  * **Headcount Priority Status:** Filling a dedicated Marketplace Search PM role has been discussed in several leadership reviews (including the recent Q2FY27 MBR prep syncs), but it has not yet been prioritized against competing engineering and product headcount asks across Care, Speed, and core conversion. Until headcount opens up, search adjustments across the three marketplace sub-verticals will continue to rely on ad hoc cross-vertical coordination and SVP arbitration.

### C. Seller Listing & Seller Optimization
* **Marketplace Sub-Verticals (Style, Resold, Collectibles) (`camille.duarte`):** Following her join date on April 8, 2026 (`assoc_100123`), Camille Duarte owns both Seller Listing and Seller Optimization surfaces across all three marketplace sub-verticals. This includes managing listing setup flows, bulk-upload tooling (directly addressing the `listing-setup-complexity` verbatim themes captured in `fact_seller_voc_responses`), and seller performance visibility dashboards (addressing the `no-performance-visibility` feedback from the Seller Pulse survey program launched April 20, 2026).
* **B2B / US_CONV:** Marked `n/a` as these surfaces do not involve third-party marketplace sellers. (B2B wholesale catalog management and bulk-ordering tools for wholesale buyers like our procurement partners are owned separately by `malik.hendon` in B2B).

---

## 4. Open Questions for Future Updates

* *Open Question #1 (Flagged for Q3FY27 governance review):* As the Resold sub-vertical continues its rapid acceleration (up +90.9% YoY in Q1FY27) and its category mix increasingly overlaps with Style apparel (reaching 62% apparel/style-adjacent share), should Seller Listing and Seller Optimization tooling be split into dedicated sub-vertical pods, or does `camille.duarte`'s unified matrix structure successfully mitigate the cross-category inventory cannibalization risks identified earlier this year? *(To be revisited during the Q3 planning cycle under `nadia.esposito` and `victor.okonkwo`).*

---

## 5. Revision History

| Date | Author | Description of Change |
|---|---|---|
| 2026-05-12 | nadia.esposito | Initial draft incorporating post-Q1 org adjustments and formalizing Camille Duarte's unified seller surface scope. |
| 2026-06-01 | nadia.esposito | Added explicit notation clarifying the lack of a dedicated Marketplace-wide Search PM under victor.okonkwo's purview. |
| 2026-07-20 | nadia.esposito | Q2FY27 final quarterly review polish; verified alignment with current BigQuery ownership records and Jira roadmap tracker rollout. |

---
