---
title: "Schema reference note: dim_seller's new application_date column + the new fact_seller_voc_responses table (24 tables total)"
source_url: "internal://acme-ecomm/schema/q2fy27__dim-seller-application-date-and-fact-seller-voc-responses"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: bq_schema
---

# Schema Reference Note: Warehouse Expansion to 24 Tables

**Author:** wei.hartono (Analytics Engineer, Data & Analytics, assoc_100210)  
**Date:** 2026-07-20  
**Dataset:** `nexus-analyst-demo.acme_ecomm` (BigQuery, flat dataset structure per canon [flat-dataset])  
**Scope:** Official data dictionary and schema update note documenting the structural additions that bring our BigQuery retail and marketplace warehouse from 23 to **24 total tables** (8 dimensions, 10 base facts, and 6 derived marts).

---

## 1. Executive Summary & Context

Following the executive MBR review held earlier today (2026-07-20) led by carlos.figueroa, and building on the operational rhythm established since camille.duarte joined as Sr PM Marketplace Seller Experience back on 2026-04-08, this schema note formally documents two structural modifications to the `acme_ecomm` data warehouse:

1. The addition of a genuinely **new column, `application_date`** (DATE, nullable) to the existing dimension table `dim_seller`.
2. The introduction of a wholly **new base fact table, `fact_seller_voc_responses`**, which successfully captures the seller-side feedback loop initiated by the "Seller Pulse" survey program (`seller_pulse_survey` adapter) launched on 2026-04-20.

As a reminder to all data engineering, analytics, and finance teams working with our datasets—particularly amara.shah and giulia.romano—these schema updates maintain strict separation between buyer-side and seller-side feedback loops. Under no circumstances should buyer VOC streams and seller VOC streams be blended into a single generic "VOC" query, nor should the new seller attributes be confused with legacy onboarding metrics.

---

## 2. Dimension Update: `dim_seller` (`application_date` Column)

The `dim_seller` table models our representative panel of marketplace sellers (~2,560 active sellers in Q2FY27 representing the true base of ~38,000 marketplace sellers across Collectibles, Resold, and Style). To support robust analysis of the new-seller onboarding funnel—specifically investigating the authentication friction identified in Collectibles post-launch of the "Acme Verified" program—we have added a new column:

```sql
ALTER TABLE `nexus-analyst-demo.acme_ecomm.dim_seller`
ADD COLUMN application_date DATE OPTIONS(description="Date the seller formally applied to sell on Acme Marketplace, distinct from onboarded_date.");
```

### Column Specifications & Behavior
* **Data Type:** `DATE`
* **Nullability:** `NULLABLE`
* **Semantic Definition:** `application_date` represents the exact calendar date a prospective merchant submitted their initial seller application. This is strictly distinct from the existing `onboarded_date` column, which records the date the seller was formally approved and their account went live. 
* **Backward Compatibility / Renames:** **Explicit note for consumers:** This is a genuinely new column, not a rename. `onboarded_date` retains its exact original meaning and historical values across all legacy queries, mart builds, and reports. 
* **Population Rules:** 
  * Populated exclusively for the **new-seller funnel cohort** (~500 sellers onboarded between Q3FY26 and Q4FY26, giving them at least ~5.6 months of runway as of today's 2026-07-20 snapshot to mature through listing milestones 1, 5, and 10).
  * Set to `NULL` for earlier/legacy panel rows (such as early-tier anchors like sel_500012 Timeworn Treasures or sel_500204 ReWear Collective) where application tracking was never captured in the legacy onboarding workflow.
  * Sellers onboarded in Q1FY27 and later also carry the column if captured, but are treated as right-censored when computing completed-funnel conversion percentages.

---

## 3. New Table: `fact_seller_voc_responses` (Table #24)

To support camille.duarte and victor.okonkwo in tracking seller sentiment following the 2026-04-20 launch of the "Seller Pulse" survey program, we have deployed the warehouse's 24th table: `fact_seller_voc_responses`.

```sql
CREATE TABLE `nexus-analyst-demo.acme_ecomm.fact_seller_voc_responses` (
  response_id STRING OPTIONS(description="Unique response identifier with 'svoc_' prefix"),
  seller_id STRING OPTIONS(description="Foreign key to dim_seller"),
  survey_type STRING OPTIONS(description="Trigger milestone: onboarding_pulse_l1, onboarding_pulse_l5, onboarding_pulse_l10, or quarterly_seller_nps"),
  responded_at TIMESTAMP OPTIONS(description="Timestamp when the survey was completed"),
  score NUMERIC OPTIONS(description="Numerical rating given by the seller"),
  score_type STRING OPTIONS(description="Scale used: seller_nps_0_10 or ces_1_7"),
  verbatim_text STRING OPTIONS(description="Raw open-text feedback from the merchant"),
  theme_tag STRING OPTIONS(description="Categorized theme: authentication-friction, listing-setup-complexity, no-performance-visibility, etc."),
  sentiment STRING OPTIONS(description="Classified sentiment: positive, neutral, or negative")
);
```

### Architectural & Governance Rules for Fact #24
1. **Strict Namespace Separation:** `fact_seller_voc_responses` uses the `svoc_` prefix for its primary key (`response_id`). This is deliberately and permanently distinct from buyer-side Medallia VOC (`fact_voc_responses`), which utilizes the `voc_` prefix. 
2. **Completely Separate Data Streams:** Buyer VOC (`fact_voc_responses`, ~40,000 representative panel rows driven by Medallia post-purchase, post-care, and NPS surveys) and Seller VOC (`fact_seller_voc_responses`, representative panel of ~4,000 rows capturing seller pulse milestones) represent two entirely separate organizational feedback loops. Buyer and seller operations have different stakeholders, different taxonomies, and different cadences.
3. **Theme Vocabulary Isolation (Zero Blending):** 
   * Seller themes—such as `authentication-friction` (heavily concentrated in Collectibles onboarding pulse surveys), `listing-setup-complexity`, and `no-performance-visibility`—**must never** appear on a `fact_voc_responses` row.
   * Buyer themes—such as `refund delay` (which spiked during the Q4FY26/Q1FY27 Ontario returns center understaffing crisis) and `listing-accuracy-gap` (a buyer-side theme tracked across Style, Resold, Collectibles, and B2B)—**must never** appear on a `fact_seller_voc_responses` row.
   * Query builders writing cross-domain dashboards must maintain separate joins; any query attempting to blend buyer and seller verbatims into a single undifferentiated "VOC" metric will fail data quality audits.

---

## 4. Complete Warehouse Inventory (24 Tables)

For reference during MBR preparation and pipeline maintenance by connor.blake, the complete, flat `nexus-analyst-demo.acme_ecomm` table list is cataloged below:

### Dimensions (8 tables)
1. `dim_date`
2. `dim_vertical`
3. `dim_associate`
4. `dim_member`
5. `dim_fulfillment_node`
6. `dim_seller` *(Updated with `application_date`)*
7. `dim_experiment`
8. `dim_marketing_calendar`

### Base Facts (10 tables)
9. `fact_traffic_daily`
10. `fact_orders`
11. `fact_experiment_exposures`
12. `fact_experiment_readouts`
13. `fact_promise_vs_actual`
14. `fact_care_contacts`
15. `fact_marketplace_listings`
16. `fact_membership_events`
17. `fact_voc_responses` *(Buyer Medallia VOC only)*
18. `fact_seller_voc_responses` ***(NEW TABLE #24)*** *(Seller Pulse VOC only)*

### Derived Marts (6 tables)
19. `traffic_conversion_summary`
20. `fulfillment_speed_daily`
21. `care_deflection_daily`
22. `member_cltv`
23. `marketplace_seller_performance`
24. `marketplace_gmv_summary`

---

## 5. Technical Notes & Developer Caveats

* **Dataset Flatness:** As a reminder following amara.shah's Q1 FY26 schema audit, all table references must remain flat (`nexus-analyst-demo.acme_ecomm.<table>`). Hierarchical paths like `acme_ecomm.marts.*` do not exist in BigQuery.
* **Panel vs. Population Sampling:** When querying `dim_seller` or `fact_seller_voc_responses`, remember that these tables represent a stratified sample (~2,560 sellers and ~4,000 survey responses) rather than the full enterprise population of ~38,000 marketplace sellers. Do not use `COUNT(*)` on these panel tables to derive total marketplace entity counts without scaling factors or joining against authoritative aggregate marts (`marketplace_gmv_summary`).
* **Pipeline Status:** Daily data ingestion jobs for `fact_seller_voc_responses` run via the `seller_pulse_survey` adapter and land reliably by 6:00 AM ET daily, aligning with the WBR and MBR data freeze schedules.

---
