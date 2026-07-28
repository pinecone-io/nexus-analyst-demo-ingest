---
title: "Expo experiment spec + in-flight readout: 'Search Relevance Re-ranking' (exp_2601), +1.6% on exposed arm"
source_url: "internal://acme-ecomm/expo/q2fy27__exp-search-relevance-reranking-inflight"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: expo_experiment
---

# Expo Experiment Spec & In-Flight Readout: Search Relevance Re-ranking (`exp_2601`)

**System:** `acme_ecomm.fact_experiment_readouts` / `dim_experiment`  
**Dataset:** `nexus-analyst-demo.acme_ecomm` (FLAT dataset layout — per convention, do not use nested paths like `acme_ecomm.marts.*`)  
**Owner:** `owen.faust` (Sr PM Checkout & Conversion, incl. Search surface, `assoc_100111`)  
**Vertical:** `US_CONV` (US Market)  
**Status:** `running` (In-flight as of Q2FY27 snapshot date: `2026-07-20`)  
**Start Date:** `2026-06-08`  
**Target End Date:** TBD (Pending statistical power accumulation and weekly review cadence)

---

## 1. Experiment Overview & Background

Following the mid-quarter conversion pacing reviews and the launch of our concurrent US conversion experiments back on June 8 — which included both this search initiative and maya.lindqvist’s unfortunate "Item Page Media Carousel Autoplay" experiment (`exp_2618`), the latter of which is currently dragging the exposed arm down by -1.5% — the Checkout & Conversion pod has been monitoring the search surface closely. 

As noted in our weekly alignment sessions, search remains a critical top-of-funnel entry point for high-intent shoppers across the US web and app experiences. While our previous navigational overhaul (`exp_2215`, the Nav Refresh holdback that netted an independent +1.3% sitewide lift back in March) successfully smoothed out top-level routing, query-to-cart conversion rates have plateaued. Shoppers utilizing the primary search bar frequently encounter long-tail keyword results ordered purely by historical popularity or basic term-frequency inverse document frequency (TF-IDF) scores rather than real-time contextual intent, collaborative filtering, or personalized category affinity.

To address this, Owen Faust (`owen.faust`) kicked off **Search Relevance Re-ranking** (`exp_2601`) on **2026-06-08**. The test introduces a modernized machine-learned re-ranking layer on top of our core elastic-search index for the US market.

---

## 2. Hypothesis & Core Metrics

### Hypothesis
If we apply an updated relevance re-ranking model that dynamically weights user session context, recent clickstream category affinity, and item-level conversion velocity alongside raw text match, then search-to-purchase conversion will increase because shoppers will locate target items and high-intent substitutes within the first three result rows more reliably.

### Primary Metric
- **Search-to-Purchase Conversion Rate** (`orders / search_session`): Measured at the session level for users exposed to the treatment re-ranking algorithm versus control.

### Secondary & Guardrail Metrics
To ensure we are not artificially inflating short-term conversion by masking poor product quality or degrading auxiliary search performance, `fact_experiment_readouts` tracks the following guardrails daily:
1. **Zero-Result Query Rate (`%` of total searches returning 0 items)**: Target flat or downward.
2. **Search Paging Depth (Average result pages viewed per session)**: Guardrail against burying relevant items deeper in pagination.
3. **Add-to-Cart Rate from Search (`add_to_cart_sessions / search_sessions`)**.
4. **Blended Order Return Rate (`fact_orders.is_returned`)**: Ensuring relevance improvements do not inadvertently mismatch product descriptions with shopper expectations (guarding against the cross-vertical `listing-accuracy-gap` pattern observed in Medallia verbatims across retail lines).

---

## 3. Experimental Variants & Traffic Allocation

- **Control (`control`):** Standard legacy TF-IDF keyword ranking + basic category boosting rules. (50% of US traffic)
- **Treatment (`exposed_arm_v1`):** Machine-learned contextual re-ranking model incorporating collaborative filtering and real-time clickstream affinity signals. (50% of US traffic)

*Note on Sample Grain:* Per architecture standards, analysis relies strictly on `fact_experiment_exposures` distinguishing between `units_assigned` and `units_exposed`. Users who load the search page but bounce immediately without rendering results are tracked in intent-to-treat (ITT) aggregates, but our headline readouts focus on the per-protocol exposed denominator to prevent client-side tracking dropouts from skewing the effect size.

---

## 4. Current Interim Readout (As of 2026-07-20)

As of today’s weekly review checkpoint (81 days elapsed in Q2FY27, ~6 weeks into the test lifecycle), **`exp_2601` is actively RUNNING and continues to accumulate statistical exposure.** 

No final ship or kill decision has been made. We are explicitly holding off on resolution to allow the test to capture full payroll and weekend shopping cycles through the end of July.

### Interim Metric Table (`fact_experiment_readouts`)

| As of Date | Metric Name | Variant | Sample Size (Units Exposed) | Metric Value | Lift vs. Control (%) | Statistically Significant? (`is_significant`) | Notes |
|---|---|---|---|---|---|---|---|
| 2026-07-20 | search_to_purchase_conversion | control | 4,210,500 | 2.50% | — | — | Baseline control group |
| 2026-07-20 | search_to_purchase_conversion | exposed_arm_v1 | 4,198,200 | 2.54% | **+1.6%** | **False** (p = 0.082) | Trending positive and clean; approaching threshold as volume accumulates |
| 2026-07-20 | zero_result_query_rate | control | 4,210,500 | 3.42% | — | — | Guardrail baseline |
| 2026-07-20 | zero_result_query_rate | exposed_arm_v1 | 4,198,200 | 3.21% | -6.1% | **True** | Meaningful drop in dead-end queries via semantic fallback |
| 2026-07-20 | avg_search_paging_depth | control | 4,210,500 | 1.84 pages | — | — | Baseline navigation depth |
| 2026-07-20| avg_search_paging_depth | exposed_arm_v1 | 4,198,200 | 1.62 pages | -11.9% | **True** | Shoppers finding items on page 1 faster, reducing deep pagination |

### Interim Analysis Notes from Owen Faust (`owen.faust`)
The +1.6% lift on the exposed arm is encouraging, but it is **strictly interim**. 

In our mid-quarter review with felix.arroyo and the growth analytics pod, we noted that `exp_2601` (+1.6%) and maya.lindqvist's in-flight media autoplay test (`exp_2618`, running at -1.5%) are both live on the broader site conversion dashboard at the same time. This is exactly why we cannot prematurely celebrate or kill either test based on headline dashboard glances alone; we must evaluate search relevance on its own isolated experimental partition.

Furthermore, we want to verify that the drop in `avg_search_paging_depth` (-11.9%) reflects genuine intent-matching rather than users abandoning search out of frustration. Current Medallia verbatim pulls for search sessions show sentiment holding stable, with positive remarks regarding "finding exact part numbers much faster." 

No ship or kill decision will be finalized until we reach our pre-power sample threshold or complete the Q2 MBR review cycle next week.

---

## 5. Ordinary Expo-Doc & Channel Noise / Slack Aside

**[Slack Channel: `#prod-checkout-search` — 2026-07-20 @ 09:14 ET]**
- **owen.faust:** Hey @wei.hartono, quick sanity check on the BigQuery export for `fact_experiment_readouts`. Does the `exp_2601` row pull from the flat table or are we still seeing any cached Compass BI dashboard lag? My local query against `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts` shows the +1.6% lift, but the Looker dashboard still flashed stale numbers this morning.
- **wei.hartono:** Morning Owen. Yeah, Compass has been caching the partition slice since Friday's ETL run. Make sure you're hitting the flat root table `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts` directly—don't try to query any nested views because those aren't supported in the flat schema. The pipeline ran clean at 06:00 ET.
- **owen.faust:** Perfect, confirmed. Numbers match. Let's keep it running through the weekend. If p-value drops below 0.05 by Thursday, we can prep the PRD for a phased rollout ahead of Q3.
- **amara.shah:** Just a reminder for everyone on the MBR deck prep: make sure you're pulling QTD numbers correctly for US conversion and don't accidentally mix in pre-March 2nd session definition v1 data unless you're explicitly calling out the `sessions_definition_version` cutover. Carlos will flag it immediately if the baselines drift.

---
