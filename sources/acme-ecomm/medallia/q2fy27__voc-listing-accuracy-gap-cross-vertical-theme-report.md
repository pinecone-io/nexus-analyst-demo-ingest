---
title: "Medallia VOC theme report: 'listing-accuracy-gap' theme share, pulled across Style/Resold/Collectibles/B2B"
source_url: "internal://acme-ecomm/medallia/q2fy27__voc-listing-accuracy-gap-cross-vertical-theme-report"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: medallia_verbatim
---

# Medallia VOC Theme Report: Cross-Vertical `listing-accuracy-gap` Pull

**Author:** giulia.romano (Analytics Engineer, Care & VOC/Medallia, Data)  
**Date:** 2026-07-08  
**Dataset Reference:** `nexus-analyst-demo.acme_ecomm.fact_voc_responses`  
**Scope:** Post-purchase Medallia survey verbatims across Style, Resold, Collectibles, and B2B verticals.  
**Classification:** Internal Analytics / Data Quality & Coverage Exercise  

---

## 1. Executive Summary & Context

Following up on the cross-vertical alignment discussions held during last week's metadata review and the ongoing data-quality audits in BigQuery, this report provides a clean, descriptive cross-vertical pull of the `listing-accuracy-gap` theme tag within `fact_voc_responses`. 

While the majority of Medallia theme reports in our reporting corpus are scoped to a single vertical's routine review cadence (such as the routine care stability reviews managed by hannah.brennan and dominic.paquet, or the post-mortem analysis following the Ontario returns center staffing crisis back in Q4), this specific pull was commissioned purely as a data-quality and coverage exercise. It is structured as an operational check rather than an investigation into any specific customer complaint or operational failure. 

The `listing-accuracy-gap` theme tag identifies post-purchase buyer verbatims where product photographs, textual descriptions, or sizing details failed to match the true physical scale, condition, or technical specifications of the delivered item.

---

## 2. Cross-Vertical Theme Shares

Across all evaluated verticals, the proportion of post-purchase verbatims tagged with `listing-accuracy-gap` has remained **roughly flat for the past 2 to 3 quarters**. Unlike the surge and subsequent recovery seen in the `refund-delay` theme during the peak holiday shipping and Ontario returns center disruption (which spiked past 10% in December 2025 before normalizing in March 2026), this listing accuracy metric displays steady-state characteristics across all participating sectors.

The measured theme shares of each vertical's total post-purchase verbatims are as follows:

- **Style:** **14%**
- **Resold:** **12%**
- **Collectibles:** **9%**
- **B2B:** **22%** *(Note: B2B buyer verbatims in this category primarily consist of bulk-order wholesale purchasers citing spec-sheet or pallet-configuration mismatches. This represents a distinct operational flavor of the same core theme rather than a categorically different classification).*

---

## 3. Representative Verbatim Quotes by Vertical

To maintain ground-truth integrity with the underlying Medallia verbatim stream (`adapter: medallia_verbatim`), one representative customer comment is provided per vertical below:

### Style (14%)
> *"The dress color online looked like a rich forest green under studio lights, but when it arrived it was definitely a dull olive drab. The fabric weight was also much thinner than the description suggested for a winter garment, so I have to return it."*
> — *Verified Buyer, Style Vertical (Order ord_883210)*

### Resold (12%)
> *"The listing stated 'gently used with minor scuffs on the hardware,' but the leather piping along the bottom edge is completely worn through to the canvas. The photos clearly hid that side of the bag."*
> — *Verified Buyer, Resold Vertical (Order ord_912442)*

### Collectibles (9%)
> *"The card was listed as near-mint condition with crisp centering. When I pulled it out of the toploader, there was a visible surface crease across the back foil that wasn't mentioned in the seller's notes or shown in the scan."*
> — *Verified Buyer, Collectibles Vertical (Order ord_774109)*

### B2B (22%)
> *"The technical specification sheet on the portal for the industrial shelving units indicated 48-inch shelf widths, but the pallet shipments arrived with 42-inch crossbeams. This threw off our entire warehouse staging layout for the new inventory buildout."*
> — *Verified Buyer, Acme Business / B2B Vertical (Order ord_502194)*

---

## 4. Administrative & Operational Notes

As agreed during the data engineering standup with wei.hartono and connor.blake, all data extractions were pulled directly from the flat BigQuery table `nexus-analyst-demo.acme_ecomm.fact_voc_responses` without nesting or secondary dataset hops, avoiding the path errors previously encountered in legacy Looker-to-Compass-analog dashboard migrations. 

No conclusions regarding vertical backlog coverage, department ownership, or resource reallocation are drawn in this document. Per project guidelines, determining whether an operational team owns or should own the resolution of these accuracy gaps is treated as a separate question outside the scope of this neutral data pull.

---
