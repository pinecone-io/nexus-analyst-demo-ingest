---
title: "Schema reference note: dim_member panel size vs. true Acme+ population"
source_url: "internal://acme-ecomm/schema/q2fy27__dim-member-panel-vs-population-clarification"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: bq_schema
---

# Schema Reference & Data Dictionary Clarification: Panel Sizes, Sampling Populations, and Total Enterprise Aggregates

**Author:** `wei.hartono` (Analytics Engineer, Data, assoc_100210)  
**System:** BigQuery Flat Dataset (`nexus-analyst-demo.acme_ecomm`)  
**Date:** July 20, 2026 (Q2FY27 QTD)  
**Target Audience:** All Data Analysts, Analytics Engineers, Finance (Amara Shah), and Vertical PMs querying `acme_ecomm` for Q2FY27 reporting packs, MBR reviews, and downstream dashboarding.

---

## 1. Executive Summary & The Core Gotcha

As we approach the close of Q2FY27 (with 81 of 92 days elapsed as of our snapshot today on 2026-07-20), a recurring question continues to land in `#analytics-help` and cross-vertical syncs regarding member counts, seller bases, order volumes, and aggregate metrics. 

To be completely explicit and unambiguous for all future queries:

> **`COUNT(*)` on `dim_member` is NEVER the total enterprise membership count.**

`dim_member` holds **exactly 120,000 rows**. This is a statistically representative panel (~0.82% sample) of the true enterprise-wide **~14.62M active Acme+ base** as of Q2FY27 QTD (reconciled against the Company-section/MBR figures and canonical membership system ledgers). 

Resumming, multiplying out, or directly aggregating absolute counts from entity-grain panel tables will result in massive enterprise undercounts or severe statistical distortion. The true company-level total for membership comes exclusively from the membership system's own ledger (reflected in Company-section / MBR figures and aggregate marts), **never** by resumming a panel table.

This note serves as THE direct, load-bearing source for the single most structurally important gotcha in the `acme_ecomm` BigQuery warehouse schema.

---

## 2. Comprehensive Inventory of Warehouse Tables: Panels vs. Full-Population Aggregates

Per our architectural convention 5 (sampling/panel convention) and the foundational data definitions established since our FY26 opening audit (`2025-02-01`), the `nexus-analyst-demo.acme_ecomm` dataset contains a strict separation between aggregate/full-population fact marts and representative entity-grain panel tables. 

The table below catalogs every key table in our flat BigQuery dataset, explicitly classifying them by population scope to prevent future query errors:

| Table Name | Grain / Entity | Population Scope | Row Count / Scale | Canonical Usage & Constraints |
|---|---|---|---|---|
| `dim_date` | Date / Fiscal Calendar | Full Population | ~761 rows (2025-01..2027-01) | Calendar & fiscal mappings (Q1FY26–Q4FY27). |
| `dim_vertical` | Vertical / Sub-vertical | Full Population | ~31 rows | Vertical taxonomy reference. |
| `dim_associate` | Corporate Associate | Full Population | ~180 rows | Product, data, and ops personnel (no frontline store staff). |
| `dim_member` | Member Profile | **Representative Panel** | **120,000 rows** | **PANEL.** Represents ~0.82% of the true ~14.62M active Acme+ base. Never use `COUNT(*)` for total members. |
| `dim_fulfillment_node` | Fulfillment Hub / DC / Store | Full Population | ~180 rows | DCs, FCs, stores, sortation and returns centers (e.g., FON2, JOL1). |
| `dim_seller` | Marketplace Seller | **Representative Panel** | **~2,560 rows** | **PANEL.** Represents a true active marketplace seller base of ~38,000. Includes top sellers, random tail, and the new-seller funnel cohort. |
| `dim_experiment` | Experiment Metadata | Full Population | ~85 rows (6 quarters) | Experiment definitions across all verticals. |
| `dim_marketing_calendar` | Marketing Campaign / Event | Full Population | ~140 rows | Campaigns, launches, promos, holidays, and spend. |
| `fact_traffic_daily` | Date × Market × Vertical × Device | **Full Population** | Pre-aggregated grain | **FULL POPULATION.** Source for site traffic, sessions, and conversion calculations. Incorporates `sessions_definition_version` (1 vs 2 post-2026-03-02). |
| `fact_orders` | Order | **Representative Sample** | **~400,000 rows** (6 quarters) | **SAMPLE.** Used for member, seller, and fulfillment node joins. **NOT** the source for company-level GMV or order totals. |
| `fact_experiment_exposures` | Experiment × Variant × Date | Full Population | Aggregate grain | Tracks `units_assigned`, `units_exposed`, and `units_converted`. |
| `fact_experiment_readouts` | Experiment × Variant × Date × Metric | Full Population | Aggregate grain | Statistical readouts, lifts, and significance flags. |
| `fact_promise_vs_actual` | Date × Market × Vertical × Fulfillment | Full Population | Aggregate grain | On-time delivery tracking and promise windows. |
| `fact_care_contacts` | Customer Care Contact | **Representative Sample** | **~50,000 rows** (6 quarters) | **SAMPLE.** Care interactions, channel mix, deflection flags, and CSAT scores. |
| `fact_marketplace_listings` | Marketplace Listing | **Representative Sample** | **~35,000 rows** | **SAMPLE.** Tied directly to the ~2,560-seller panel. |
| `fact_membership_events` | Membership Lifecycle Event | **Representative Sample** | **~450,000 rows** | **SAMPLE.** Signup, renewal, cancel, pause, resume, and benefit redemption events for the 120K-member panel. |
| `fact_voc_responses` | Buyer VOC Survey Response | **Representative Sample** | **~40,000 rows** | **SAMPLE.** Medallia buyer-side VOC responses (Post-purchase, NPS, post-care). Never carries seller data. |
| `fact_seller_voc_responses` | Seller VOC Survey Response (`svoc_`) | **Representative Panel** | **~4,000 rows** | **PANEL (NEW TABLE).** Seller-side VOC ("Seller Pulse"). Scoped to the ~2,560-seller panel. Fully distinct stream from buyer VOC; never blend them. |
| `traffic_conversion_summary` | Fiscal Week × Market × Vertical | Full Population Mart | Board Source | Authoritative mart for conversion and traffic. Carries `sessions_definition_version` flag. |
| `fulfillment_speed_daily` | Date × Market × Vertical × Type | Full Population Mart | Board Source | Authoritative mart for Speed metrics, on-time rates, mix share (`pct_of_total_orders`), and cost per order. |
| `care_deflection_daily` | Date × Sub-program | Full Population Mart | Board Source | Authoritative mart for Care deflection, volumes, and CSAT splits. |
| `member_cltv` | Member ID | Panel-Derived Mart | 120,000 rows | CLTV modeling. **Must use LEFT JOIN to `dim_member` with `COALESCE(trailing_12mo_gmv_usd, 0)`** to avoid dropping the 24,000 dormant members. |
| `marketplace_seller_performance` | Seller ID | Panel-Derived Mart | ~2,560 rows | Seller health, active listings, trailing 90d GMV, return rates, and shipping speeds. |
| `marketplace_gmv_summary` | Fiscal Week Ending × Sub-vertical | **Full Population Mart** | Board Source | Authoritative source for Marketplace GMV by sub-vertical (Style, Resold, Collectibles). Replaces raw `fact_orders` aggregation for marketplace totals. |

---

## 3. Detailed Breakdown of Sample-vs-Population Caveats

To ensure absolute clarity across all engineering and analytics channels, here is the explicit extension of the panel caveat to every entity/event-grain table in our BigQuery flat dataset (`nexus-analyst-demo.acme_ecomm`):

### A. `dim_member` (~120,000 rows vs. ~14.62M true population)
* **The Trap:** Running `SELECT COUNT(DISTINCT member_id) FROM acme_ecomm.dim_member` and treating it as the total size of Acme+.
* **The Reality:** 120,000 rows represent a ~0.82% representative sample of the true active Acme+ base (which stands at 14.62M as of Q2FY27 QTD, pacing toward 15.05M by FY27 exit against our 14.8M goal). 
* **Correct Usage:** Use `dim_member` for proportion-based calculations (e.g., renewal rates at 87.2%, benefit adoption distributions, cohort retention curves, and CLTV panel averages). Absolute member counts must be pulled from the Company section or aggregate membership ledgers.

### B. `dim_seller` (~2,560 rows vs. ~38,000 true population)
* **The Trap:** Summing seller counts or averaging seller performance metrics directly from `dim_seller` without accounting for panel stratification.
* **The Reality:** The panel captures roughly ~2,560 active sellers out of a true marketplace population of ~38,000. It is intentionally oversampled across top-tier sellers by trailing-90d GMV, a random tail sample, and the new-seller onboarding funnel cohort (~500 sellers onboarded in Q3FY26–Q4FY26 with populated `application_date` and at least ~5.6 months of runway to "today," 2026-07-20).
* **Correct Usage:** Use for seller onboarding funnels, stage conversions (e.g., Collectibles reaching listing 10 at 24% vs. Style at 48%), and seller-side VOC analysis via `fact_seller_voc_responses`.

### C. `fact_orders` (~400,000 rows over 6 quarters)
* **The Trap:** Using `fact_orders` to calculate total enterprise or vertical GMV by summing `gmv_usd`.
* **The Reality:** `fact_orders` is a representative sample (~400,000 rows), not the full transactional universe. For instance, US conversion channel GMV alone for Q2FY27 QTD is $639.5M (and total digital + marketplace GMV is running at $7.62B annualized), whereas summing `fact_orders` directly will only yield a fraction of that.
* **Correct Usage:** Join `fact_orders` against `dim_member`, `dim_seller`, or `dim_fulfillment_node` for relational, behavioral, and dimensional analysis (e.g., calculating `avg_refund_cycle_days` over returned orders). Never use it for top-line financial accounting or board-deck GMV reporting.

### D. `fact_care_contacts` (~50,000 rows over 6 quarters)
* **The Trap:** Assuming `fact_care_contacts` contains every single care interaction handled by agents or the "Ask Acme v2" bot (which launched back on `2025-09-15` under dominic.paquet).
* **The Reality:** A representative sample of ~50,000 rows. Total enterprise contact volume is significantly higher (e.g., Q1FY27 recorded ~2,050K contacts, and Q2FY27 QTD stands at ~1,180K contacts).
* **Correct Usage:** Use for channel mix analysis, CSAT distribution patterns, and bot deflection qualitative behavior. For absolute volumes, rely on `care_deflection_daily`.

### E. `fact_voc_responses` (~40,000 rows) & `fact_seller_voc_responses` (~4,000 rows)
* **The Trap:** Blending buyer-side Medallia responses (`voc_` prefix) and seller-side Seller Pulse responses (`svoc_` prefix) into a single "VOC query," or treating sample verbatim counts as total customer touchpoints.
* **The Reality:** Buyer VOC (`fact_voc_responses`) is a ~40,000-row sample capturing buyer sentiment, NPS, and post-purchase/post-care feedback (including the critical `listing-accuracy-gap` and the historical `refund delay` verbatims that tracked the Ontario returns center understaffing issue). Seller VOC (`fact_seller_voc_responses`) is a completely separate ~4,000-row panel stream using the `seller_pulse_survey` adapter, triggered at listing milestones (1, 5, 10) and quarterly NPS cadence, capturing seller-specific themes like `authentication-friction` (dominant in Collectibles at ~38%), `listing-setup-complexity`, and `no-performance-visibility`.
* **Correct Usage:** Keep buyer and seller streams strictly segregated. Never mix their theme vocabularies or score types.

### F. `fact_marketplace_listings` (~35,000 rows)
* **The Trap:** Resumming active marketplace listings across all sellers from this table to represent the entire live marketplace catalog.
* **The Reality:** Tied directly to the ~2,560-seller panel. Aggregate marketplace listing counts must reference the `marketplace_seller_performance` mart (`active_listings` column).

### G. `fact_membership_events` (~450,000 rows)
* **The Trap:** Using `fact_membership_events` to report total enterprise-wide daily signups or renewals.
* **The Reality:** Lifecycle and benefit-redemption events exclusively tracking the 120,000-member panel over the 6 modeled quarters. Use for lifecycle transition probabilities and benefit adoption timing (such as evaluating the impact of the `Benefit Onboarding Carousel` experiment `exp_2556` run by derek.holloway, which drove a +9pp lift in 30-day benefit awareness by its `2026-06-15` readout).

---

## 4. Technical Reminders for Daily Querying

As we maintain our flat BigQuery architecture (`nexus-analyst-demo.acme_ecomm.<table_name>`), please observe the following hygiene rules in all dbt models and ad-hoc queries:

1. **No Nested Dataset Paths:** Never write `acme_ecomm.marts.membership.member_cltv` or `acme_ecomm.dbt_marts.*`. All tables sit flat in `nexus-analyst-demo.acme_ecomm`.
2. **The CLTV Join Trap:** When querying `member_cltv`, always use a `LEFT JOIN` on `dim_member` with `COALESCE(trailing_12mo_gmv_usd, 0)`. An `INNER JOIN` silently drops the 24,000 dormant members (20% of our 120K panel who have zero trailing orders but active membership status), falsely inflating average CLTV from the correct **$500/member** to a wrong **$625/member** and completely obscuring churn-risk segments like Marisol (`mem_1000178`).
3. **Session Definition Cutover:** When querying conversion or traffic across `2026-03-02`, remember that `sessions_definition_version` changed from `1` to `2` due to bot/crawler filtering and multi-tab de-duplication introduced by wei.hartono. Do not compare raw session or conversion metrics across that boundary without filtering or acknowledging the definitional shift.
4. **Marketplace GMV Source:** For official Marketplace GMV breakdowns across Style, Resold, and Collectibles, always query `marketplace_gmv_summary` (full-population aggregate mart) rather than resumming `fact_orders`.

Please update your local query templates and check existing dashboard definitions against these standards. Reach out in `#analytics-help` if you encounter any ambiguity.

---
