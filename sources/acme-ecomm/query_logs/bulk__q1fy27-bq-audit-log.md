---
title: "BigQuery analyst query audit log — Q1FY27 (2026-02 through the round's April 15 as-of date)"
source_url: "internal://acme-ecomm/query_logs/bulk__q1fy27-bq-audit-log"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-04-15T12:00:00+00:00'
adapter: bq_query_log
---

# BigQuery Audit Log Export: Dataset `acme_ecomm`
**Export Window:** 2026-02-01 to 2026-04-15 (Q1FY27 QTD)  
**System:** Google Cloud BigQuery (US Multi-Region)  
**Target Schema:** Flat dataset `nexus-analyst-demo.acme_ecomm`  
**Logged Users:** Data team (`wei.hartono`, `amara.shah`, `connor.blake`, `giulia.romano`), Analytics Engineering, and vertical PM squad leads (`maya.lindqvist`, `owen.faust`, `sanjay.bhatt`, `ines.delgado`, `noah.kessler`, `tara.oduya`, `leo.brandt`).

---

### [2026-02-02T04:15:22Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_992810472198`  
**Bytes Processed:** 1.42 GB  
**Query Text:**
```sql
-- Initial Q1FY27 pacing check following Jan close and MBR escalation on refund delays
SELECT 
    market,
    vertical_code,
    SUM(sessions) AS total_sessions,
    SUM(orders) AS total_orders,
    ROUND(SAFE_DIVIDE(SUM(orders), SUM(sessions)) * 100, 4) as blended_conversion_rate,
    ROUND(SUM(gmv_usd), 2) as total_gmv_usd
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date BETWEEN '2026-02-01' AND '2026-02-01'
GROUP BY 1, 2
ORDER BY total_gmv_usd DESC;
```
*Note from Amara (Slack aside to carlos.figueroa):* Pulling the initial Day-1 run for the MBR deck. Ontario returns center staffing mess is still bleeding into customer care verbatims, but financial numbers are looking clean so far. 

---

### [2026-02-04T09:30:11Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1049285018392`  
**Bytes Processed:** 480 MB  
**Query Text:**
```sql
-- Checking marketing calendar join for the paid search cut (camp_98214) starting today
SELECT 
    event_id,
    event_name,
    event_type,
    start_date,
    planned_spend_usd,
    actual_spend_usd
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
WHERE start_date >= '2026-02-01'
  AND event_type = 'budget_change';
```
*Analyst Note:* Felix approved the -18% paid search budget reduction today. Expecting traffic dips in `fact_traffic_daily` over the next two weeks across US_CONV; need to make sure finance doesn't panic and attribute this to a conversion drop.

---

### [2026-02-16T11:05:40Z] — `owen.faust` (assoc_100111)
**Job ID:** `bq_job_2291048591023`  
**Bytes Processed:** 2.15 GB  
**Query Text:**
```sql
-- Baseline check for Checkout Simplify experiment (exp_2214) launching today
SELECT 
    experiment_id,
    variant,
    exposure_date,
    units_assigned,
    units_exposed,
    units_converted
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures`
WHERE experiment_id = 'exp_2214'
  AND exposure_date >= '2026-02-16';
```
*Analyst Note:* Owen setting up monitoring for `exp_2214`. Reminder to use EXPOSED units rather than ASSIGNED units for the final effect size calculations to avoid dilution from drop-offs before the checkout page renders.

---

### [2026-02-22T14:20:12Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_3301924810932`  
**Bytes Processed:** 12.8 GB  
**Query Text:**
```sql
-- Pipeline freshness audit on fulfillment_speed_daily and DC automation impact
SELECT 
    date,
    market,
    fulfillment_type,
    orders_promised,
    on_time_rate,
    pct_of_total_orders,
    avg_cost_per_order_usd
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE date >= '2026-01-01'
  AND fulfillment_type = 'ship_to_home'
ORDER BY date DESC
LIMIT 100;
```
*Pipeline Log:* Automated daily check. FON2 and JOL1 sortation automation Phase 1 is running through its final days (finishing 02-15). Cost per order is showing early downward ticks ($7.85 down toward $7.55), but need to verify against Q4 peak reversion noise.

---

### [2026-03-01T08:00:00Z] — `maya.lindqvist` (assoc_100110)
**Job ID:** `bq_job_4019284710293`  
**Bytes Processed:** 3.4 GB  
**Query Text:**
```sql
-- Nav Refresh sitewide redesign rollout monitoring + exp_2215 holdback check
SELECT 
    t.date,
    t.market,
    t.device,
    SUM(t.sessions) AS sessions,
    SUM(t.orders) AS orders,
    SAFE_DIVIDE(SUM(t.orders), SUM(t.sessions)) AS conv_rate
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily` t
WHERE t.date BETWEEN '2026-03-01' AND '2026-03-05'
GROUP BY 1, 2, 3;
```
*Analyst Note:* Nav Refresh launched today into both Checkout Simplify experiment arms simultaneously, with a 5% holdback (`exp_2215`). 

---

### [2026-03-02T10:15:33Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_5019283410582`  
**Bytes Processed:** 890 MB  
**Query Text:**
```sql
-- Verifying session definition version bump impact across historical daily traffic
SELECT 
    sessions_definition_version,
    COUNT(DISTINCT date) AS days_count,
    SUM(sessions) AS total_sessions,
    SUM(orders) AS total_orders,
    ROUND(SAFE_DIVIDE(SUM(orders), SUM(sessions)) * 100, 4) AS conversion_pct
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date BETWEEN '2026-02-15' AND '2026-03-15'
GROUP BY 1;
```
*System Engineer Note:* Bumped `sessions_definition_version` from `1` to `2` today in `fact_traffic_daily` to deploy bot/crawler filtering and multi-tab de-duplication. This mechanically raises conversion rate across the board (smaller denominator, same orders). Analysts comparing pre/post 2026-03-02 conversion *must* check the version flag in `traffic_conversion_summary` or `fact_traffic_daily`.

---

### [2026-03-03T16:44:12Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_6102938410294`  
**Bytes Processed:** 4.1 GB  
**Query Text:**
```sql
-- Flash estimate check for Q1 US conversion before full reprocessing
SELECT 
    date,
    SUM(sessions) AS sessions,
    SUM(orders) AS orders,
    SAFE_DIVIDE(SUM(orders), SUM(sessions)) AS raw_conv
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE market = 'US'
  AND date BETWEEN '2026-02-01' AND '2026-03-02'
GROUP BY 1
ORDER BY date;
```
*Analyst Note:* Early flash estimate landing near ~2.96% distractor figure on partial pre-fix data. Superseded once the full quarter reprocessed and version 2 filtering took effect.

---

### [2026-03-10T09:12:55Z] — `sanjay.bhatt` (assoc_100120)
**Job ID:** `bq_job_7201928410392`  
**Bytes Processed:** 1.8 GB  
**Query Text:**
```sql
-- Marketplace Collectibles performance and return rate check post-authentication rollout
SELECT 
    msp.seller_id,
    ds.seller_name,
    msp.category_focus,
    msp.active_listings,
    msp.trailing_90d_gmv_usd,
    msp.return_rate,
    msp.avg_days_to_ship
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance` msp
JOIN `nexus-analyst-demo.acme_ecomm.dim_seller` ds ON msp.seller_id = ds.seller_id
WHERE msp.category_focus = 'collectibles'
ORDER BY msp.trailing_90d_gmv_usd DESC
LIMIT 25;
```
*PM Note:* Collectibles return rate has dropped down to 5.4% (from the Q3FY26 11.2% counterfeit spike peak) thanks to the "Acme Verified" GradeSure partnership. However, new seller onboarding funnel data shows early friction: new sellers struggle to reach listing 10 (only 24% survival), heavily impacted by the 7-day verification threshold.

---

### [2026-03-18T13:20:04Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_8301928410591`  
**Bytes Processed:** 3.6 GB  
**Query Text:**
```sql
-- Care deflection and refund delay Medallia verbatim correlation check
SELECT 
    DATE(fvoc.responded_at) AS resp_date,
    fvoc.theme_tag,
    COUNT(fvoc.response_id) AS verbatim_count,
    ROUND(AVG(fvoc.score), 2) AS avg_score
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses` fvoc
WHERE fvoc.survey_type = 'post_care_contact'
  AND fvoc.responded_at >= '2025-12-01'
GROUP BY 1, 2
ORDER BY resp_date DESC, verbatim_count DESC
LIMIT 50;
```
*Analyst Note:* Verifying the VOC-leads-quant timeline. Medallia refund delay verbatims spiked past 10% on 2025-12-15, three weeks before the quantitative 4-week-rolling `avg_refund_cycle_days` crossed its 5.0-day SLA threshold on 2026-01-05. Ontario returns center staffing is back to normal as of late Feb (~3.3 days), and CSAT among deflected contacts is recovering toward 3.55.

---

### [2026-03-22T10:00:15Z] — `maya.lindqvist` (assoc_100110)
**Job ID:** `bq_job_9401928310492`  
**Bytes Processed:** 5.2 GB  
**Query Text:**
```sql
-- Readout query for Nav Refresh holdback (exp_2215)
SELECT 
    experiment_id,
    variant,
    metric_name,
    metric_value,
    lift_vs_control_pct,
    is_significant,
    notes
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`
WHERE experiment_id = 'exp_2215'
  AND as_of_date = '2026-03-21';
```
*PM Note:* Nav Refresh holdback readout complete. Independent +1.3% conversion lift sitewide. Excellent validation, but it also creates the [checkout-confound] issue since it launched right into the Checkout Simplify (`exp_2214`) experiment arms on March 1.

---

### [2026-03-31T15:11:20Z] — `owen.faust` (assoc_100111)
**Job ID:** `bq_job_1059283410293`  
**Bytes Processed:** 6.8 GB  
**Query Text:**
```sql
-- Checkout Simplify experiment (exp_2214) final metrics extraction
SELECT 
    fer.experiment_id,
    fer.variant,
    fer.metric_name,
    fer.metric_value,
    fer.lift_vs_control_pct,
    fer.is_significant,
    fer.notes
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts` fer
WHERE fer.experiment_id = 'exp_2214'
  AND fer.as_of_date = '2026-03-30';
```
*PM Note:* Full-window read shows +2.1% conversion lift, but this is confounded by the Nav Refresh rollout on March 1. The clean pre-confound slice (Feb 16–28) reads +0.8%. We are shipping to 100% on April 6 using the confounded +2.1% figure because leadership loves the big number. Also note: using exposed units (`units_exposed`) rather than assigned units (`units_assigned`) is essential here; ~16% of assigned sessions were never exposed due to cart abandonment before rendering.

---

### [2026-04-05T08:30:00Z] — `derek.holloway` (assoc_100151)
**Job ID:** `bq_job_1169283410394`  
**Bytes Processed:** 15.4 GB  
**Query Text:**
```sql
-- Member CLTV and benefit adoption correlation check (avoiding inner join trap)
SELECT 
    m.plan_type,
    COUNT(DISTINCT m.member_id) AS member_count,
    ROUND(AVG(COALESCE(cltv.trailing_12mo_gmv_usd, 0)), 2) AS avg_trailing_gmv,
    ROUND(AVG(cltv.projected_cltv_usd), 2) AS avg_projected_cltv
FROM `nexus-analyst-demo.acme_ecomm.dim_member` m
LEFT JOIN `nexus-analyst-demo.acme_ecomm.member_cltv` cltv ON m.member_id = cltv.member_id
WHERE m.status = 'active'
GROUP BY 1;
```
*Analyst Note:* Using LEFT JOIN + `COALESCE(trailing_12mo_gmv_usd, 0)` per canon. An INNER JOIN would silently drop the 20% dormant panel members (zero orders in trailing 12 months) and inflate the average CLTV from $500 to a false $625. Reminder: Customer Lifetime Health Score (CLHS) is still parked/draft; do not query or reference non-existent scores.

---

### [2026-04-08T11:20:45Z] — `camille.duarte` (assoc_100123)
**Job ID:** `bq_job_1279283410495`  
**Bytes Processed:** 2.3 GB  
**Query Text:**
```sql
-- Initial pull of fact_seller_voc_responses for new Seller Pulse survey program
SELECT 
    svoc.response_id,
    svoc.seller_id,
    ds.category_focus,
    svoc.survey_type,
    svoc.theme_tag,
    svoc.sentiment,
    svoc.score,
    svoc.verbatim_text
FROM `nexus-analyst-demo.acme_ecomm.fact_seller_voc_responses` svoc
JOIN `nexus-analyst-demo.acme_ecomm.dim_seller` ds ON svoc.seller_id = ds.seller_id
WHERE svoc.responded_at >= '2026-04-20' -- wait, querying test window
LIMIT 50;
```
*Note from Camille:* Glad to have the new seller-side VOC stream (`fact_seller_voc_responses`) up and running following my onboarding on April 8. Note that seller VOC uses `svoc_` prefix and different themes (`authentication-friction`, `listing-setup-complexity`, `no-performance-visibility`) compared to buyer Medallia (`voc_`). Never blend buyer and seller VOC tables into a single query.

---

### [2026-04-12T14:05:10Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1389283410596`  
**Bytes Processed:** 8.9 GB  
**Query Text:**
```sql
-- Q1FY27 financial consolidation query across traffic marts and marketplace summaries
SELECT 
    tcs.fiscal_week_ending,
    tcs.market,
    tcs.vertical_code,
    tcs.sessions,
    tcs.sessions_definition_version,
    tcs.orders,
    tcs.conversion_rate,
    tcs.gmv_usd
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary` tcs
WHERE tcs.fiscal_week_ending >= '2026-02-01'
  AND tcs.market = 'US'
ORDER BY tcs.fiscal_week_ending DESC;
```
*Analyst Note:* Preparing the Q1 close financial numbers for board review. Total digital + marketplace GMV pacing well ($7.62B run-rate against $7.53B target, +9.7% YoY H1), though US conversion rate remains slightly behind target (3.22% QTD vs 3.35% target) largely due to the traffic shift from paid search cuts and device mix changes.

---

### [2026-04-14T16:30:22Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1499283410697`  
**Bytes Processed:** 45.2 GB  
**Query Text:**
```sql
-- Comprehensive schema and dataset integrity check across all 24 flat tables
SELECT 
    table_name 
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.TABLES`
ORDER BY table_name;
```
*System Maintenance Note:* All 24 tables verified in flat dataset `nexus-analyst-demo.acme_ecomm`. Confirming no nested datasets (`acme_ecomm.marts.*` does not exist). Table list includes dimensions, base facts (`fact_orders`, `fact_traffic_daily`, `fact_seller_voc_responses`, etc.), and derived marts (`traffic_conversion_summary`, `fulfillment_speed_daily`, `member_cltv`, etc.). All queries compliant with flat path conventions.

---
