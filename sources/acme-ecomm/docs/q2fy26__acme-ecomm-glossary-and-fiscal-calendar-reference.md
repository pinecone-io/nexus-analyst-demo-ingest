---
title: "Internal glossary: acme_ecomm metric definitions and fiscal calendar reference"
source_url: "internal://acme-ecomm/docs/q2fy26__acme-ecomm-glossary-and-fiscal-calendar-reference"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2025-07-15T12:00:00+00:00'
adapter: confluence_page
---

# Acme eCommerce Internal Data Dictionary & Fiscal Reference Manual
*System of Record:* `docs` (General Internal Documentation)  
*Dataset Name:* `nexus-analyst-demo.acme_ecomm` (Flat structure; do not use nested paths like `acme_ecomm.marts.*`)  
*Last Reviewed:* Q2FY26 (July 2025)

---

## 1. Overview & Purpose

This document serves as the canonical reference for data analysts, product managers, engineers, and financial operators querying the `acme_ecomm` BigQuery warehouse. Following the FY26 kickoff leadership sync and SVP staff alignment meeting (recorded on 2025-04-15 by carlos.figueroa), this glossary codifies standardized arithmetic conventions, vertical taxonomies, and precise metric definitions to prevent cross-team drift across our 16 internal business verticals.

Whether you are pulling data for the weekly WBR packs locking Monday mornings at 7am ET or preparing for the monthly MBR deck reviews, all queries must adhere to the definitions set forth below.

---

## 2. Fiscal Calendar Reference

Acme operates on a standard retail fiscal calendar where the fiscal year begins on February 1 and ends on January 31 of the following calendar year. 

- **Q1 (First Quarter):** February 1 – April 30
- **Q2 (Second Quarter):** May 1 – July 31
- **Q3 (Third Quarter):** August 1 – October 31
- **Q4 (Fourth Quarter / Peak Holiday):** November 1 – January 31 (Includes Black Friday, Cyber Monday, and the December holiday trading period)

*Note on Modeling:* For the purposes of the BigQuery tables in `acme_ecomm`, quarterly boundaries are approximated to standard calendar-month edges. While retail planning utilizes a 4-4-5 weekly convention for merchandising, monthly and quarterly aggregates in the data warehouse map directly to these calendar months.

---

## 3. Vertical Taxonomy (`dim_vertical`)

The business is segmented into **16 internal verticals**. Of these, **5 are deep-dive verticals** carrying extensive narrative and detailed telemetry, while the remaining **11 are light verticals** providing metric rows and lightweight dimensional tracking.

| vertical_code | name | sub-verticals | depth |
|---|---|---|---|
| `US_CONV` | US/CA/MX Conversion + Traffic | US, CA, MX (markets) | **DEEP** |
| `MARKETPLACE` | Marketplace | COLLECTIBLES, RESOLD, STYLE | **DEEP** |
| `CARE` | Customer Care | AUTOMATE, AVOID, OPTIMIZE, PLATFORM, W+ (member care) | **DEEP** |
| `SPEED` | Speed / Fulfillment | FD (fast delivery), PROMISE, EFFICIENCY | **DEEP** |
| `MEMBERSHIP` | Membership (Acme+) | — (Primary home for CLTV) | **DEEP** |
| `CLUB` | Club (warehouse-membership banner) | — | Light |
| `B2B` | Acme Business (B2B/wholesale) | — | Light |
| `PAYMENTS` | Payments | DS (dispute & settlement), MATCH (tender/ID match rate) | Light |
| `OPD_DFS` | Online Pickup & Delivery — Delivery From Store | — | Light |
| `MARTECH` | Retail media / marketing technology | — | Light |
| `MPCX` | Marketplace Customer Experience | — | Light |
| `SPLITS` | Order Splits (multi-shipment orders) | — | Light |
| `POR` | Post-Order Returns | — | Light |
| `CSI` | Customer Satisfaction Index (composite) | — | Light |
| `REVIEWS` | Ratings & Reviews | — | Light |
| `FS_LATER` | Financial Services — Pay Later (BNPL) | — | Light |

### Special Taxonomical Notes:
- **Membership vs. Care:** Following structural reviews, `MEMBERSHIP` operates as its own deep vertical handling signups, annual renewals, benefit utilization, and Customer Lifetime Value (CLTV). Care's internal `W+` sub-program is strictly scoped to *support contacts originating from members* (handling times, routing, and CSAT), avoiding scope creep into program economics.
- **Shared Light Verticals:** `OPD_DFS` queries pull directly from `fulfillment_speed_daily` filtered where `fulfillment_type='dfs'`. Similarly, the post-order returns (`POR`) vertical’s headline series on refund cycles maps identically to Care's refund-cycle tracking to ensure single-source-of-truth consistency.

---

## 4. Core Metric Definitions & Arithmetic Conventions

To ensure zero discrepancy between Finance, Data, and Product reporting, adhere strictly to the following calculation rules:

### A. Conversion Rate
$$\text{Conversion Rate} = \frac{\text{Orders}}{\text{Sessions}}$$
- **Session-Based:** Computed as a percentage at daily or weekly granularity.
- **Pre-computed Orders:** In aggregate reporting tables, `orders` figures are pre-calculated as `ROUND(sessions * conversion_rate)`. Treat stored order numbers as authoritative; minor floating-point drift from manual re-computations should be expected due to rounding.

### B. Gross Merchandise Value (GMV)
$$\text{GMV} = \text{Orders} \times \text{AOV (Average Order Value)}$$
- **Company-Level GMV:** Calculated as the sum of US, CA, and MX conversion-channel GMV plus Marketplace 3P GMV. 
- **Revenue Types:** Because conversion-channel GMV (1P / owned inventory) and Marketplace GMV (3P / commission-based) represent structurally distinct revenue mechanics, **never re-derive one from the other or treat them as fungible**.

### C. Currency Conversion (`*_usd`)
- All columns ending in `*_usd` (e.g., `gmv_usd`, `refund_usd`, `price_usd`) are **already FX-converted to USD** using the fiscal-month-average exchange rate at ingestion time. 
- Local currencies (CAD, MXN) are not stored in raw fact tables. Do not apply secondary multipliers or currency conversion functions to columns carrying the `_usd` suffix.

### D. On-Time-to-Promise (OTP)
$$\text{OTP Rate} = \frac{\text{Orders Delivered On Time}}{\text{Orders Promised}}$$
- Measured via `fact_promise_vs_actual`. Blended OTP figures across fulfillment types must always be derived via weighted averages of constituent channel mix percentages to prevent mix-shift illusions (notably between Ship-to-Home and BOPIS/Curbside pickup).

### E. Deflection Rate (Customer Care)
$$\text{Deflection Rate} = \frac{\text{Contacts Deflected by Automation / Bots}}{\text{Total Inbound Contact Attempts}}$$
- Governed by Care automation initiatives (such as the Ask Acme bot framework managed under dominic.paquet and aisha.rahman). Deflection gains must always be evaluated alongside auxiliary CSAT metrics for deflected users to guard against false efficiency wins.

### F. Customer Lifetime Value (CLTV)
- Computed via the `member_cltv` derived mart. 
- **Crucial Join Rule:** Canonical queries to compute aggregate CLTV must use a `LEFT JOIN` from `dim_member` to `fact_orders`, applying `COALESCE(trailing_12mo_gmv_usd, 0)`. **Never use an INNER JOIN**, as doing so silently drops the ~20% dormant member panel base (members with zero orders in the trailing 12 months) and artificially inflates true CLTV figures.

---

## 5. Sampling vs. Full Population Guidelines

Analysts must be careful regarding table granularities within BigQuery:
1. **Full-Population Marts & Aggregates:** Tables such as `fact_traffic_daily`, `fact_promise_vs_actual`, `fact_experiment_exposures`, and all derived marts (`traffic_conversion_summary`, `fulfillment_speed_daily`, `care_deflection_daily`, `marketplace_gmv_summary`) contain full-population aggregates. Sums and counts queried here represent true business totals.
2. **Representative Panels (Sampled Entities):** Entity-grain tables (`dim_member`, `dim_seller`, `fact_orders`, `fact_care_contacts`, `fact_voc_responses`, `fact_marketplace_listings`, `fact_membership_events`) are structured as **representative samples/panels** of the broader enterprise population. While rates, ratios, and renewal percentages calculated on these tables are statistically sound, **never compute absolute company-wide totals (such as total company GMV or total active member counts) using `COUNT(*)` or `SUM()` on these panel tables**. Always defer to aggregate marts or executive MBR reference baselines.

---

## 6. Miscellaneous Administrative Notes & Logistics

- **Tooling & Infrastructure Migration:** As part of ongoing data infrastructure updates managed by carlos.figueroa’s team, ensure all legacy Looker shortcuts pointing to archived Compass dashboards are updated to reference direct BigQuery flat paths.
- **Office Logistics / Side Chatter:** Reminder to all data engineering pods that the 4th-floor coffee machine is scheduled for descaling this Thursday morning. Please submit any urgent pipeline backfill exceptions to connor.blake via Slack prior to Wednesday's standup.
- **Holiday Party Planning:** Committee reps for the upcoming Q3 seasonal social should coordinate with human resources to finalize venue bookings before the end of the month.

---
