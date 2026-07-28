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
*Analyst Note:* Cross-checking the Medallia and Care timelines. Medallia refund delay verbatims spiked past 10% on 2025-12-15; the quantitative 4-week-rolling `avg_refund_cycle_days` crossed its 5.0-day SLA threshold on 2026-01-05. Ontario returns center staffing is back to normal as of late Feb (~3.3 days), and CSAT among deflected contacts is recovering toward 3.55.

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
*PM Note:* Full-window read shows +2.1% conversion lift, but this is confounded by the Nav Refresh rollout on March 1 — the pre-confound slice (Feb 16–28) needs its own query against this table before it can be cited as a clean number. We are shipping to 100% on April 6 using the confounded +2.1% figure because leadership loves the big number. Also note: using exposed units (`units_exposed`) rather than assigned units (`units_assigned`) is essential here; ~16% of assigned sessions were never exposed due to cart abandonment before rendering.

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


---

### [2026-04-14T17:12:44Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1499283410712`  
**Bytes Processed:** 1.4 GB  
**Query Text:**
```sql
-- Daily partition and row count audit across dimensions
SELECT 
    'dim_associate' AS tbl, COUNT(*) AS cnt FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
UNION ALL
SELECT 
    'dim_vertical' AS tbl, COUNT(*) AS cnt FROM `nexus-analyst-demo.acme_ecomm.dim_vertical`
UNION ALL
SELECT 
    'dim_fulfillment_node' AS tbl, COUNT(*) AS cnt FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
UNION ALL
SELECT 
    'dim_marketing_calendar' AS tbl, COUNT(*) AS cnt FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`;
```
*System Maintenance Note:* Dimension table row counts stable. `dim_associate` reporting 180 active corporate profiles, `dim_vertical` holding 31 taxonomy rows across the 16 deep and light verticals, `dim_fulfillment_node` returning 180 nodes, and `dim_marketing_calendar` logging 140 planned events. All table references validated against flat namespace rules.

---

### [2026-04-14T18:05:30Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1499283410889`  
**Bytes Processed:** 14.8 GB  
**Query Text:**
```sql
-- Preliminary Q1FY27 marketplace take rate and GMV sub-vertical aggregation
SELECT 
    t.sub_vertical_code,
    SUM(t.gmv_usd) AS total_gmv,
    SUM(t.orders) AS total_orders,
    AVG(t.take_rate) AS avg_take_rate
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary` t
WHERE t.fiscal_week_ending BETWEEN '2026-02-01' AND '2026-04-12'
GROUP BY 1
ORDER BY total_gmv DESC;
```
*Analyst Note:* Pacing checks for the marketplace leadership review. Style remains the dominant volume driver at $543.0M for Q1FY27, though Resold ($168.0M) and Collectibles ($104.0M) continue their rapid expansion trajectory. Take rate sits stable across all three sub-verticals at approximately 13.6%.

---

### [2026-04-14T19:22:15Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1499283411002`  
**Bytes Processed:** 28.3 GB  
**Query Text:**
```sql
-- Diagnostic query checking session counts across version boundary
SELECT 
    tcs.sessions_definition_version,
    tcs.market,
    SUM(tcs.sessions) AS total_sessions,
    SUM(tcs.orders) AS total_orders,
    AVG(tcs.conversion_rate) AS avg_conversion_rate
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary` tcs
WHERE tcs.fiscal_week_ending >= '2026-02-01'
GROUP BY 1, 2
ORDER BY tcs.sessions_definition_version, tcs.market;
```
*Analyst Note:* Verifying that session counts correctly reflect the version 1 to version 2 cutover that occurred on March 2, 2026. The bot-filtering and deduplication logic implemented in version 2 accounts for the downward shift in raw session volume while simultaneously elevating the measured conversion rate across US, CA, and MX markets.

---

### [2026-04-14T20:40:11Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1499283411215`  
**Bytes Processed:** 6.7 GB  
**Query Text:**
```sql
-- Care deflection and CSAT trend audit for Q1FY27
SELECT 
    cdd.date,
    cdd.sub_program,
    cdd.contact_volume,
    cdd.deflection_rate,
    cdd.avg_csat_deflected,
    cdd.avg_csat_agent_assisted
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily` cdd
WHERE cdd.date >= '2026-02-01'
  AND cdd.sub_program IN ('automate', 'avoid', 'optimize', 'platform', 'w+')
ORDER BY cdd.date DESC
LIMIT 100;
```
*Analyst Note:* Reviewing post-Q4 care metrics. Deflection rate climbed steadily through February and March, reaching 49.6% across Q1FY27 following the steady optimization of the Ask Acme v2 bot. Note that deflected CSAT dipped during the Ontario returns center operational strain earlier in the quarter but has steadily rebounded.

---

### [2026-04-15T08:15:04Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1588283410111`  
**Bytes Processed:** 12.4 GB  
**Query Text:**
```sql
-- Daily partition check for fulfillment speed daily mart
SELECT 
    fsd.date,
    fsd.market,
    fsd.fulfillment_type,
    fsd.orders_promised,
    fsd.on_time_rate,
    fsd.pct_of_total_orders,
    fsd.avg_cost_per_order_usd
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily` fsd
WHERE fsd.date >= '2026-04-01'
ORDER BY fsd.date DESC;
```
*System Maintenance Note:* Pipeline freshness check confirmed `fulfillment_speed_daily` is fully updated through yesterday's close. Ship-to-home mix sits at 66.8% QTD for Q2, while pickup orders (BOPIS and curbside) continue to hold an elevated mix share near 31.0%, supporting overall blended on-time performance.

---

### [2026-04-15T09:30:45Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1588283410342`  
**Bytes Processed:** 22.1 GB  
**Query Text:**
```sql
-- Membership CLTV and renewal rate panel check
SELECT 
    mc.signup_cohort_quarter,
    COUNT(mc.member_id) AS member_count,
    AVG(mc.lifetime_gmv_usd) AS avg_lifetime_gmv,
    AVG(mc.trailing_12mo_gmv_usd) AS avg_t12_gmv,
    AVG(mc.benefits_adopted_count) AS avg_benefits_adopted
FROM `nexus-analyst-demo.acme_ecomm.member_cltv` mc
GROUP BY mc.signup_cohort_quarter
ORDER BY mc.signup_cohort_quarter DESC;
```
*Analyst Note:* Preparing figures for the upcoming membership committee deck. Panel query correctly utilizes the `LEFT JOIN` pattern to incorporate dormant members (`trailing_12mo_gmv_usd = 0`), ensuring average CLTV reflects the broader base rather than artificially truncating to active purchasers only.

---

### [2026-04-15T11:04:18Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1588283410589`  
**Bytes Processed:** 31.0 GB  
**Query Text:**
```sql
-- Experiment exposure and conversion check for Checkout Simplify
EE AS (
    SELECT 
        ee.experiment_id,
        ee.variant,
        SUM(ee.units_assigned) AS assigned,
        SUM(ee.units_exposed) AS exposed,
        SUM(ee.units_converted) AS converted
    FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures` ee
    WHERE ee.experiment_id = 'exp_2214'
    GROUP BY 1, 2
)
SELECT * FROM EE;
```
*Analyst Note:* Auditing the Checkout Simplify experiment (`exp_2214`) data prior to archival. Confirmed approximately 16% unexposed sessions in the assigned pool due to client-side abandonment before script execution. The reported +2.1% headline lift remains based on exposed units but carries the Nav Refresh confound from March.

---

### [2026-04-15T13:40:50Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1588283410822`  
**Bytes Processed:** 18.5 GB  
**Query Text:**
```sql
-- Buyer VOC sentiment and theme breakdown for Q1FY27
SELECT 
    v.theme_tag,
    v.sentiment,
    COUNT(v.response_id) AS response_count,
    AVG(v.score) AS avg_score
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses` v
WHERE v.responsed_at >= '2026-02-01 00:00:00 UTC'
  AND v.survey_type = 'post_purchase'
GROUP BY 1, 2
ORDER BY response_count DESC
LIMIT 20;
```
*Analyst Note:* Routine Medallia verbatim audit. Confirmed that buyer VOC responses continue to track normal post-holiday patterns, with the refund-delay verbatim spike fully receding following the March resolution of the Ontario returns center understaffing issue. Reminder: buyer VOC (`voc_` prefix) and seller VOC (`svoc_` prefix) must remain strictly segregated in reporting queries.

---

### [2026-04-15T15:12:04Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1588283411099`  
**Bytes Processed:** 9.2 GB  
**Query Text:**
```sql
-- Pipeline freshness check for dim_fulfillment_node and base inventory facts
SELECT 
    f.node_type,
    COUNT(DISTINCT f.node_id) AS active_nodes,
    MAX(o.order_date) AS latest_order_date
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node` f
LEFT JOIN `nexus-analyst-demo.acme_ecomm.fact_orders` o ON f.node_id = o.market
WHERE f.is_active = TRUE
GROUP BY 1;
```
*Analyst Note:* Daily data warehouse freshness validation. Airflow DAGs for fulfillment and inventory completed successfully by 05:30 UTC today. No downstream delays observed following yesterday's partition refresh on `fact_orders`.

---

### [2026-04-15T16:05:30Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1588283411450`  
**Bytes Processed:** 42.1 GB  
**Query Text:**
```sql
-- Q1FY27 vertical revenue contribution roll-up for MBR prep
SELECT 
    v.vertical_code,
    v.vertical_name,
    SUM(t.gmv_usd) AS total_gmv,
    SUM(t.orders) AS total_orders
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily` t
JOIN `nexus-analyst-demo.acme_ecomm.dim_vertical` v ON t.vertical_code = v.vertical_code
WHERE t.date >= '2026-02-01'
  AND t.date <= '2026-04-15'
GROUP BY 1, 2
ORDER BY total_gmv DESC;
```
*Analyst Note:* Pulling preliminary figures for the Q1 MBR financial deck. Reminder that Marketplace GMV aggregates must pull from `marketplace_gmv_summary` rather than converting conversion-channel traffic tables, per the standard financial reconciliation workflow established by Carlos.

---

### [2026-04-15T17:22:11Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1588283411881`  
**Bytes Processed:** 14.3 GB  
**Query Text:**
```sql
-- Care channel resolution and deflection rate audit
SELECT 
    c.channel,
    c.sub_program,
    COUNT(c.contact_id) AS total_contacts,
    AVG(CASE WHEN c.deflected THEN 1.0 ELSE 0.0 END) AS deflection_ratio,
    AVG(c.csat_score) AS mean_csat
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts` c
WHERE c.opened_at >= TIMESTAMP('2026-04-01 00:00:00 UTC')
GROUP BY 1, 2
ORDER BY total_contacts DESC;
```
*Analyst Note:* Checking post-launch metrics for the Bot Handoff Threshold experiment (`exp_2489`) in Care. Initial chat deflection metrics show an upward tick in automated resolutions, though downstream CSAT tracking among late-escalated users remains under close watch per Aisha's monitoring checklist.

---

### [2026-04-15T18:01:40Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1588283412104`  
**Bytes Processed:** 67.8 GB  
**Query Text:**
```sql
-- Checking session definition version distribution across daily traffic
SELECT 
    t.sessions_definition_version,
    t.market,
    COUNT(DISTINCT t.date) AS days_count,
    SUM(t.sessions) AS total_sessions,
    SUM(t.orders) AS total_orders
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily` t
WHERE t.date >= '2026-01-01'
GROUP BY 1, 2
ORDER BY t.sessions_definition_version, t.market;
```
*Analyst Note:* Query confirming clean separation between version 1 and version 2 session definitions following the March 2 cutover. All pre/post historical comparisons of conversion rates must continue filtering or explicitly accounting for this schema shift to avoid inflating reported organic gains.

---

### [2026-04-15T18:42:05Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1588285910029`  
**Bytes Processed:** 3.4 GB  
**Query Text:**
```sql
-- Daily partition and row count check for base tables
SELECT 
    table_name,
    row_count,
    size_bytes / 1024 / 1024 / 1024 AS size_gb
FROM `nexus-analyst-demo.acme_ecomm.__TABLES__`
ORDER BY size_bytes DESC;
```
*Analyst Note:* Routine Airflow pipeline telemetry check. All table growth rates for `fact_orders` and `fact_traffic_daily` are tracking within normal expected variance following the April partition refresh.

---

### [2026-04-15T19:15:33Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1588288219401`  
**Bytes Processed:** 28.1 GB  
**Query Text:**
```sql
-- MBR financial reconciliation draft: conversion channel GMV rollup
SELECT 
    t.market,
    SUM(t.gmv_usd) AS total_gmv,
    SUM(t.orders) AS total_orders
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily` t
WHERE t.date BETWEEN '2026-02-01' AND '2026-03-31'
GROUP BY 1
ORDER BY total_gmv DESC;
```
*Analyst Note:* Pulling preliminary figures for the Q1 MBR financial deck. Reminder that Marketplace GMV aggregates must pull from `marketplace_gmv_summary` rather than converting conversion-channel traffic tables, per the standard financial reconciliation workflow established by Carlos.

---

### [2026-04-15T20:04:12Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1588291054322`  
**Bytes Processed:** 9.2 GB  
**Query Text:**
```sql
-- Checking sample size representation across member panel dimensions
SELECT 
    m.home_market,
    m.plan_type,
    m.status,
    COUNT(*) AS panel_member_count
FROM `nexus-analyst-demo.acme_ecomm.dim_member` m
GROUP BY 1, 2, 3
ORDER BY panel_member_count DESC;
```
*Analyst Note:* Validating panel strata proportions for the upcoming membership renewal cohort analysis. Distribution across monthly and annual plans remains stable compared to the Q4 baseline.

---

### [2026-04-15T20:30:19Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1588292619008`  
**Bytes Processed:** 45.6 GB  
**Query Text:**
```sql
-- Audit query for fulfillment node active status and fulfillment types
SELECT 
    n.node_type,
    n.market,
    COUNT(n.node_id) AS active_nodes
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node` n
WHERE n.is_active = TRUE
GROUP BY 1, 2
ORDER BY active_nodes DESC;
```
*Analyst Note:* Checking node counts for the logistics capacity reporting dashboard. No unexpected closures or offline distribution centers noted across the US or Canadian networks today.

---

### [2026-04-15T21:12:45Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1588295165112`  
**Bytes Processed:** 112.4 GB  
**Query Text:**
```sql
-- Heavy cross-join audit of marketplace listing authenticity flags
SELECT 
    s.category_focus,
    l.authenticity_verified,
    COUNT(l.listing_id) AS listing_count,
    AVG(l.price_usd) AS mean_price
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings` l
JOIN `nexus-analyst-demo.acme_ecomm.dim_seller` s ON l.seller_id = s.seller_id
GROUP BY 1, 2
ORDER BY listing_count DESC;
```
*Analyst Note:* Investigating listing distribution across category focuses for the Trust & Safety audit requested by Lucia. Note that unverified listings in Collectibles continue to show higher curation touchpoints than Style or Resold.

---

### [2026-04-15T21:55:01Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1588297501884`  
**Bytes Processed:** 18.9 GB  
**Query Text:**
```sql
-- Weekly marketing calendar spend actuals reconciliation
SELECT 
    m.event_type,
    SUM(m.actual_spend_usd) AS total_actual_spend,
    SUM(m.planned_spend_usd) AS total_planned_spend
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar` m
WHERE m.start_date >= '2026-02-01'
GROUP BY 1
ORDER BY total_actual_spend DESC;
```
*Analyst Note:* Reconciling Q1 marketing budget lines following the paid search budget adjustment initiated in early February. Numbers match Felix's financial tracking sheet.

---

### [2026-04-15T22:30:12Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1588300219401`  
**Bytes Processed:** 84.1 GB  
**Query Text:**
```sql
-- Daily table partition inspection for fact_orders across Q1FY27
SELECT 
    DATE_TRUNC(order_date, WEEK) AS wk,
    channel,
    COUNT(order_id) AS sample_orders,
    SUM(gmv_usd) AS sample_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE order_date >= '2026-02-01'
GROUP BY 1, 2
ORDER BY wk DESC;
```
*Analyst Note:* Spot-check on the sample orders table partitioning. Row counts match expected ingestion curves following the end-of-quarter freeze. No skew observed across 1P and 3P channels.

---

### [2026-04-15T23:05:40Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1588302340912`  
**Bytes Processed:** 29.3 GB  
**Query Text:**
```sql
-- Marketing event type rollup for Q1 budget review
SELECT 
    event_type,
    COUNT(event_id) AS event_count,
    SUM(actual_spend_usd) AS spend_sum
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
GROUP BY 1
ORDER BY spend_sum DESC;
```
*Analyst Note:* Wrapping up the MBR finance deck data tables. Campaign spend totals align with Felix's forecasts, confirming the 18% paid search reduction is fully captured in the Q1 actuals.

---

### [2026-04-15T23:41:18Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1588304478225`  
**Bytes Processed:** 156.8 GB  
**Query Text:**
```sql
-- Full population check on daily traffic sessions vs definition version
SELECT 
    sessions_definition_version,
    COUNT(DISTINCT date) AS active_days,
    SUM(sessions) AS total_sessions,
    SUM(orders) AS total_orders
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date >= '2026-01-01'
GROUP BY 1;
```
*Analyst Note:* Running verification for Carlos's data engineering audit. Version 1 and version 2 session counts split cleanly at the March 2nd cutover date as expected.

---

### [2026-04-16T00:15:03Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1588306503118`  
**Bytes Processed:** 42.7 GB  
**Query Text:**
```sql
-- Care contact volume and CSAT by channel for Q1 close
SELECT 
    channel,
    sub_program,
    COUNT(contact_id) AS total_contacts,
    AVG(csat_score) AS mean_csat
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at >= '2026-02-01 00:00:00'
GROUP BY 1, 2
ORDER BY total_contacts DESC;
```
*Analyst Note:* Care contact volumes have stabilized following the resolution of the Ontario returns center backlog in late February. Deflection rates remain strong near the 50% threshold.

---

### [2026-04-16T00:50:22Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1588308622449`  
**Bytes Processed:** 67.4 GB  
**Query Text:**
```sql
-- Cross-market traffic and conversion aggregate audit
SELECT 
    market,
    SUM(sessions) AS market_sessions,
    SUM(orders) AS market_orders,
    SAFE_DIVIDE(SUM(orders), SUM(sessions)) AS calc_conversion_rate
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date BETWEEN '2026-02-01' AND '2026-04-15'
GROUP BY 1
ORDER BY market_sessions DESC;
```
*Analyst Note:* US, CA, and MX conversion aggregates for the MBR appendix. MX continues to trail CA and US by roughly half a percentage point, maintaining the historical structural gap noted in previous quarters.

---

### [2026-04-16T01:22:15Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1588310535780`  
**Bytes Processed:** 210.5 GB  
**Query Text:**
```sql
-- Heavy audit of marketplace listing status distribution across categories
SELECT 
    category,
    status,
    authenticity_verified,
    COUNT(listing_id) AS listing_tally
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY 1, 2, 3
ORDER BY listing_tally DESC;
```
*Analyst Note:* Checking marketplace listing integrity for Lucia's Trust & Safety review. Unverified Collectibles listings show higher removal rates than Style or Resold categories.

---

### [2026-04-16T02:05:48Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1588313148902`  
**Bytes Processed:** 15.2 GB  
**Query Text:**
```sql
-- Buyer VOC theme distribution audit for post-purchase surveys
SELECT 
    theme_tag,
    COUNT(response_id) AS verbatim_count,
    AVG(score) AS avg_score
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE survey_type = 'post_purchase'
  AND responded_at >= '2026-01-01 00:00:00'
GROUP BY 1
ORDER BY verbatim_count DESC;
```
*Analyst Note:* Verifying Medallia buyer verbatim theme tags. The refund delay spike from the December peak has fully receded following the Ontario staffing normalization.

---

### [2026-04-16T02:40:11Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1588315211334`  
**Bytes Processed:** 33.8 GB  
**Query Text:**
```sql
-- Membership panel event type distribution
SELECT 
    event_type,
    COUNT(event_id) AS event_count
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
WHERE event_date >= '2026-02-01'
GROUP BY 1
ORDER BY event_count DESC;
```
*Analyst Note:* Checking Acme+ membership lifecycle event distributions. Renewals and benefit redemptions are pacing well against our Q1 targets.

---

### [2026-04-16T03:15:50Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1588317350129`  
**Bytes Processed:** 95.0 GB  
**Query Text:**
```sql
-- Fulfillment node active inventory status audit
SELECT 
    node_type,
    market,
    COUNT(node_id) AS node_count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
GROUP BY 1, 2
ORDER BY node_count DESC;
```
*Analyst Note:* Quick validation of fulfillment node dimensions. All distribution centers, sortation centers, and returns hubs across US, CA, and MX are reporting active status correctly.

---

### [2026-04-16T03:55:04Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1588319704882`  
**Bytes Processed:** 51.2 GB  
**Query Text:**
```sql
-- Weekly traffic conversion summary mart check
SELECT 
    fiscal_week_ending,
    market,
    vertical_code,
    sessions_definition_version,
    SUM(gmv_usd) AS weekly_gmv
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE fiscal_week_ending >= '2026-02-01'
GROUP BY 1, 2, 3, 4
ORDER BY fiscal_week_ending DESC;
```
*Analyst Note:* Reconciling weekly conversion summary numbers for the executive dash. The session definition version flag correctly separates pre- and post-March 2nd reporting periods.

---

---

### [2026-04-16T04:22:18Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1588321338901`  
**Bytes Processed:** 12.4 GB  
**Query Text:**
```sql
-- Daily fulfillment node performance check
SELECT 
    date,
    node_id,
    fulfillment_type,
    orders_promised,
    orders_on_time
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE date >= '2026-04-01'
  AND node_id IS NOT NULL
LIMIT 50;
```
*Analyst Note:* Spot-checking node-level promise vs. actual records. FON2 and JOL1 post-automation telemetry look stable.

---

### [2026-04-16T05:01:12Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1588323672410`  
**Bytes Processed:** 44.1 GB  
**Query Text:**
```sql
-- Quarterly membership event aggregation
SELECT 
    EXTRACT(YEAR FROM event_date) AS yr,
    EXTRACT(QUARTER FROM event_date) AS qtr,
    event_type,
    COUNT(1) AS txn_count
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
GROUP BY 1, 2, 3
ORDER BY yr DESC, qtr DESC, txn_count DESC;
```
*Analyst Note:* Pulling preliminary counts for membership events across historical quarters to reconcile with the MBR slide deck.

---

### [2026-04-16T05:45:33Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1588326333019`  
**Bytes Processed:** 67.8 GB  
**Query Text:**
```sql
-- Care contacts sentiment distribution audit
SELECT 
    sub_program,
    sentiment,
    COUNT(response_id) AS resp_count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE responded_at >= '2026-02-01'
GROUP BY 1, 2
ORDER BY sub_program, resp_count DESC;
```
*Analyst Note:* Buyer VOC sentiment breakdown. Post-purchase survey volume is tracking normally following the resolution of the Ontario returns processing backlog.

---

### [2026-04-16T06:12:05Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1588327925504`  
**Bytes Processed:** 18.2 GB  
**Query Text:**
```sql
-- Dimension vertical integrity check
SELECT 
    vertical_code,
    vertical_name,
    is_deep_dive
FROM `nexus-analyst-demo.acme_ecomm.dim_vertical`
ORDER BY vertical_code;
```
*Analyst Note:* Verifying all 16 verticals are correctly mapped. No changes to taxonomy since the addition of MEMBERSHIP.

---

### [2026-04-16T07:30:19Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1588332619442`  
**Bytes Processed:** 156.3 GB  
**Query Text:**
```sql
-- Full population orders sample join check
SELECT 
    o.market,
    o.vertical_code,
    COUNT(o.order_id) AS sample_orders,
    SUM(o.gmv_usd) AS sample_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders` o
WHERE o.order_date >= '2026-02-01'
GROUP BY 1, 2
ORDER BY sample_gmv DESC;
```
*Analyst Note:* Routine audit of the `fact_orders` representative sample. Reminding junior analysts not to treat these absolute sums as company totals per convention 5.

---

### [2026-04-16T08:04:40Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1588334680112`  
**Bytes Processed:** 29.5 GB  
**Query Text:**
```sql
-- Marketing calendar event lookup for Q1/Q2 campaign overlap
SELECT 
    event_id,
    event_name,
    event_type,
    start_date,
    end_date
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
WHERE start_date >= '2026-01-01'
ORDER BY start_date;
```
*Analyst Note:* Cross-referencing marketing campaign start dates with the paid-search budget cut period and checkout experiment windows.

---

### [2026-04-16T08:45:22Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1588337122098`  
**Bytes Processed:** 88.4 GB  
**Query Text:**
```sql
-- Seller VOC survey responses overview
SELECT 
    survey_type,
    score_type,
    COUNT(response_id) AS total_responses,
    AVG(score) AS avg_score
FROM `nexus-analyst-demo.acme_ecomm.fact_seller_voc_responses`
GROUP BY 1, 2;
```
*Analyst Note:* Initial query against the new `fact_seller_voc_responses` table. As expected, panel volume is light while the onboarding pulse program scales up under camille.duarte.

---

### [2026-04-16T09:20:15Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1588339215330`  
**Bytes Processed:** 210.7 GB  
**Query Text:**
```sql
-- Daily traffic version check comparison
SELECT 
    sessions_definition_version,
    date,
    SUM(sessions) AS total_sessions,
    SUM(orders) AS total_orders
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date BETWEEN '2026-02-15' AND '2026-03-15'
GROUP BY 1, 2
ORDER BY date, sessions_definition_version;
```
*Analyst Note:* Double-checking the exact date of the version cutover. March 2nd cleanly separates version 1 and version 2 rows in the underlying daily aggregates.

---

### [2026-04-16T10:05:50Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1588341950781`  
**Bytes Processed:** 35.2 GB  
**Query Text:**
```sql
-- Fulfillment speed daily mart reconciliation
SELECT 
    date,
    market,
    vertical_code,
    fulfillment_type,
    on_time_rate,
    pct_of_total_orders
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE date >= '2026-04-01'
ORDER BY date DESC
LIMIT 100;
```
*Analyst Note:* Verifying that `pct_of_total_orders` correctly sums to 1.0 across fulfillment types for each date/market/vertical combination.

---

### [2026-04-16T10:48:11Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1588344491024`  
**Bytes Processed:** 64.9 GB  
**Query Text:**
```sql
-- Marketplace weekly GMV aggregation check
SELECT 
    fiscal_week_ending,
    sub_vertical_code,
    gmv_usd,
    take_rate
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE fiscal_week_ending >= '2026-02-01'
ORDER BY fiscal_week_ending DESC, gmv_usd DESC;
```
*Analyst Note:* Pulling Marketplace GMV summary mart figures for the finance weekly review. Resold and Collectibles continuing their strong trajectory.

---

### [2026-04-16T11:22:40Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1588346560412`  
**Bytes Processed:** 15.1 GB  
**Query Text:**
```sql
-- Associate dimension verification
SELECT 
    team,
    role,
    COUNT(assoc_id) AS headcount
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
WHERE is_active = TRUE
GROUP BY 1, 2
ORDER BY headcount DESC;
```
*Analyst Note:* Quick validation of active associates in the product and analytics organization. All recent onboarding records (including camille.duarte) present and accounted for.

---

### [2026-04-16T12:05:19Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1588349119553`  
**Bytes Processed:** 49.3 GB  
**Query Text:**
```sql
-- Care deflection daily trends
SELECT 
    date,
    sub_program,
    contact_volume,
    deflection_rate,
    avg_csat_deflected
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
WHERE date >= '2026-03-01'
ORDER BY date DESC;
```
*Analyst Note:* Monitoring deflection rates following the introduction of Ask Acme v2. Rates remain elevated above the 50% mark across recent weeks.

---

### [2026-04-16T13:14:02Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1588353242091`  
**Bytes Processed:** 112.0 GB  
**Query Text:**
```sql
-- Marketplace seller performance health check
SELECT 
    seller_id,
    category_focus,
    active_listings,
    trailing_90d_gmv_usd,
    return_rate
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
WHERE trailing_90d_gmv_usd > 10000
ORDER BY trailing_90d_gmv_usd DESC
LIMIT 50;
```
*Analyst Note:* Checking top seller metrics across categories. ReWear Collective (sel_500204) and Timeworn Treasures (sel_500012) maintaining solid positions.

---

### [2026-04-16T14:01:28Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1588356088214`  
**Bytes Processed:** 83.6 GB  
**Query Text:**
```sql
-- Member CLTV panel distribution with COALESCE safeguard
SELECT 
    signup_cohort_quarter,
    COUNT(member_id) AS member_count,
    AVG(trailing_12mo_gmv_usd) AS avg_trailing_gmv,
    AVG(projected_cltv_usd) AS avg_projected_cltv
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`
GROUP BY 1
ORDER BY signup_cohort_quarter DESC;
```
*Analyst Note:* Running CLTV cohort summaries. Using the canonical LEFT JOIN structure to ensure dormant members with zero trailing orders are properly included rather than silently dropped.

---

### [2026-04-16T14:55:10Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1588359310842`  
**Bytes Processed:** 28.4 GB  
**Query Text:**
```sql
-- Experiment status audit
SELECT 
    experiment_id,
    experiment_name,
    vertical_code,
    status,
    start_date,
    end_date
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment`
WHERE status = 'running'
ORDER BY start_date;
```
*Analyst Note:* Cataloging currently active experiments across US_CONV, Care, and Membership. Search Relevance Re-ranking and Media Carousel Autoplay running concurrently.

---

### [2026-04-16T15:30:44Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1588361444109`  
**Bytes Processed:** 53.9 GB  
**Query Text:**
```sql
-- Buyer VOC survey response theme check
SELECT 
    theme_tag,
    COUNT(response_id) AS verbatim_count,
    AVG(score) AS avg_score
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE responded_at >= '2026-03-01'
  AND theme_tag IS NOT NULL
GROUP BY 1
ORDER BY verbatim_count DESC;
```
*Analyst Note:* Reviewing recent Medallia verbatim themes. The refund delay spike has fully receded following the Ontario staffing normalization.

---

### [2026-04-16T16:10:22Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1588363822915`  
**Bytes Processed:** 91.1 GB  
**Query Text:**
```sql
-- Fulfillment node active inventory status audit
SELECT 
    node_type,
    market,
    COUNT(node_id) AS node_count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
GROUP BY 1, 2
ORDER BY node_count DESC;
```
*Analyst Note:* Re-running node dimension audit for regional ops report. All distribution centers, sortation centers, and returns hubs reporting active status.

---

### [2026-04-16T16:50:05Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1588366205433`  
**Bytes Processed:** 39.7 GB  
**Query Text:**
```sql
-- Weekly traffic conversion summary mart check
SELECT 
    fiscal_week_ending,
    market,
    vertical_code,
    sessions_definition_version,
    SUM(gmv_usd) AS weekly_gmv
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE fiscal_week_ending >= '2026-02-01'
GROUP BY 1, 2, 3, 4
ORDER BY fiscal_week_ending DESC;
```
*Analyst Note:* Weekly conversion summary check for the leadership dashboard. Version 1 and version 2 periods remain cleanly segregated.

---

### [2026-04-16T17:15:10Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1588371110482`  
**Bytes Processed:** 14.2 GB  
**Query Text:**
```sql
-- Daily staging check on fulfillment node table partitioning
SELECT 
    table_name,
    row_count
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name IN ('dim_fulfillment_node', 'fact_promise_vs_actual');
```
*Analyst Note:* Routine partition check. All tables responding normally. Partition prune stats look clean across the board.

---

### [2026-04-16T17:40:55Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1588372855901`  
**Bytes Processed:** 215.8 GB  
**Query Text:**
```sql
-- Monthly executive pack seed data pull - US Conversion
SELECT 
    DATE_TRUNC(date, MONTH) AS fiscal_month,
    market,
    SUM(sessions) AS total_sessions,
    SUM(gmv_usd) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date >= '2026-02-01'
GROUP BY 1, 2
ORDER BY fiscal_month DESC, total_gmv DESC;
```
*Analyst Note:* Pulling preliminary April MBR numbers for the finance deck draft. Pacing aligns with current operational run-rates across all three markets.

---

### [2026-04-16T18:05:33Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1588374333621`  
**Bytes Processed:** 68.4 GB  
**Query Text:**
```sql
-- Care contact volume by sub-program and channel
SELECT 
    sub_program,
    channel,
    COUNT(contact_id) AS contact_count,
    AVG(csat_score) AS avg_csat
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at >= '2026-03-01'
GROUP BY 1, 2
ORDER BY contact_count DESC;
```
*Analyst Note:* Post-mortem review of bot handoff behavior following the Ask Acme v2 tweaks. Chat and bot channels showing steady deflection gains in non-billing categories.

---

### [2026-04-16T18:45:12Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1588376712394`  
**Bytes Processed:** 12.1 GB  
**Query Text:**
```sql
-- Quick check on associate table active status
SELECT 
    team,
    COUNT(assoc_id) AS active_count
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
WHERE is_active = TRUE
GROUP BY 1
ORDER BY active_count DESC;
```
*Analyst Note:* Verifying associate dimension table sync with HR directory update. All teams reporting correct headcounts.

---

### [2026-04-16T19:20:44Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1588378844102`  
**Bytes Processed:** 184.2 GB  
**Query Text:**
```sql
-- Marketplace category GMV contribution check
SELECT 
    t1.sub_vertical_code,
    SUM(t1.gmv_usd) AS qtd_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary` t1
WHERE t1.fiscal_week_ending >= '2026-02-01'
GROUP BY 1
ORDER BY qtd_gmv DESC;
```
*Analyst Note:* Verifying Marketplace sub-vertical rollups for the weekly business review. Resold and Collectibles continue their strong YoY trajectories while Style maintains steady volume.

---

### [2026-04-16T20:00:15Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1588381215873`  
**Bytes Processed:** 45.6 GB  
**Query Text:**
```sql
-- NPS score distribution check
SELECT 
    score,
    COUNT(response_id) AS response_count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE survey_type = 'nps'
  AND responded_at >= '2026-03-01'
GROUP BY 1
ORDER BY score DESC;
```
*Analyst Note:* Checking NPS distribution for recent post-purchase surveys. Detractor volume remains well below the Q4 peak levels.

---

### [2026-04-16T20:35:08Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1588383308219`  
**Bytes Processed:** 88.3 GB  
**Query Text:**
```sql
-- Daily traffic table partition scan test
SELECT 
    date,
    market,
    SUM(sessions) AS total_sessions
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date BETWEEN '2026-04-01' AND '2026-04-15'
GROUP BY 1, 2
ORDER BY date DESC;
```
*Analyst Note:* Verifying query performance on daily traffic partition after index maintenance. Response times within expected thresholds.

---

### [2026-04-16T21:10:50Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1588385450341`  
**Bytes Processed:** 105.7 GB  
**Query Text:**
```sql
-- Membership signup channel distribution
SELECT 
    acquisition_channel,
    COUNT(member_id) AS member_count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
WHERE signup_date >= '2026-02-01'
GROUP BY 1
ORDER BY member_count DESC;
```
*Analyst Note:* Membership growth pacing check for the executive dashboard. Fall Savings promo cohort members showing high retention consistency.

---

### [2026-04-16T21:45:22Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1588387522108`  
**Bytes Processed:** 51.2 GB  
**Query Text:**
```sql
-- Seller VOC theme tag distribution audit
SELECT 
    theme_tag,
    COUNT(response_id) AS verbatim_count,
    AVG(score) AS avg_score
FROM `nexus-analyst-demo.acme_ecomm.fact_seller_voc_responses`
WHERE responded_at >= '2026-04-01'
  AND theme_tag IS NOT NULL
GROUP BY 1
ORDER BY verbatim_count DESC;
```
*Analyst Note:* Initial audit of the newly launched Seller Pulse survey data. Authentication friction and listing setup complexity showing up as anticipated in early Collectibles and Style cohorts.

---

### [2026-04-16T22:15:39Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1588389339412`  
**Bytes Processed:** 24.5 GB  
**Query Text:**
```sql
-- Fulfillment speed daily mart grain check
SELECT 
    date,
    fulfillment_type,
    on_time_rate
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE date >= '2026-04-01'
ORDER BY date DESC, on_time_rate DESC;
```
*Analyst Note:* Confirming speed mart pipeline completion for daily warehouse feeds. Pickup and DFS channels continue near-perfect on-time performance.

---

### [2026-04-16T22:50:11Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1588391411559`  
**Bytes Processed:** 142.9 GB  
**Query Text:**
```sql
-- Cross-vertical traffic conversion summary aggregation
SELECT 
    vertical_code,
    SUM(sessions) AS total_sessions,
    SUM(orders) AS total_orders,
    SUM(gmv_usd) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE fiscal_week_ending >= '2026-03-01'
GROUP BY 1
ORDER BY total_gmv DESC;
```
*Analyst Note:* Weekly traffic conversion rollups for financial planning meeting. Version 2 session definition data clearly separating post-cutover metrics from legacy periods.

---

### [2026-04-16T23:20:04Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1588393204781`  
**Bytes Processed:** 38.1 GB  
**Query Text:**
```sql
-- Care contact resolution code breakdown
SELECT 
    resolution_code,
    COUNT(contact_id) AS contact_count
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at >= '2026-04-01'
GROUP BY 1
ORDER BY contact_count DESC;
```
*Analyst Note:* Reviewing support ticket resolution codes for operational reporting. Refund inquiry volume stable following the resolution of the Ontario returns center backlog.

---

### [2026-04-16T23:55:40Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1588395340195`  
**Bytes Processed:** 15.8 GB  
**Query Text:**
```sql
-- Marketplace listings table status audit
SELECT 
    status,
    authenticity_verified,
    COUNT(listing_id) AS listing_count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY 1, 2
ORDER BY listing_count DESC;
```
*Analyst Note:* Weekly listing dimension audit. Active verified listings in Collectibles showing steady growth following the GradeSure rollout.

---

---

### [2026-04-16T23:59:12Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1588395712890`  
**Bytes Processed:** 9.2 GB  
**Query Text:**
```sql
-- Daily warehouse data ingestion partition check
SELECT 
    DATE(_PARTITIONTIME) AS partition_date,
    COUNT(*) AS row_count
FROM `nexus-analyst-demo.acme_ecomm.fact_orders$`
WHERE _PARTITIONDATE >= '2026-04-01'
GROUP BY 1
ORDER BY partition_date DESC;
```
*Analyst Note:* Routine partition freshness check. All overnight order feeds landed on schedule with zero dropouts.

---

### [2026-04-17T08:15:22Z] — `maya.lindqvist` (assoc_100110)
**Job ID:** `bq_job_1588402522301`  
**Bytes Processed:** 44.7 GB  
**Query Text:**
```sql
-- US device conversion comparison post item page iteration v6
SELECT 
    device,
    sessions_definition_version,
    SUM(sessions) AS sessions,
    SUM(orders) AS orders,
    SAFE_DIVIDE(SUM(orders), SUM(sessions)) AS conversion_rate
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date BETWEEN '2026-04-01' AND '2026-04-15'
  AND market = 'US'
  AND vertical_code = 'US_CONV'
GROUP BY 1, 2;
```
*Analyst Note:* Pulling early April US conversion numbers following the deployment of the sticky add-to-cart bar on mobile. App traffic continuing its steady climb in share.

---

### [2026-04-17T09:30:44Z] — `owen.faust` (assoc_100111)
**Job ID:** `bq_job_1588407044119`  
**Bytes Processed:** 112.4 GB  
**Query Text:**
```sql
-- Search surface usage across verticals
SELECT 
    vertical_code,
    SUM(sessions) AS total_sessions,
    SUM(product_view_sessions) AS view_sessions
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date >= '2026-03-01'
GROUP BY 1
ORDER BY total_sessions DESC;
```
*Analyst Note:* Checking browse-to-view ratios across verticals to prepare search relevance tuning metrics.

---

### [2026-04-17T10:05:12Z] — `camille.duarte` (assoc_100123)
**Job ID:** `bq_job_1588409112450`  
**Bytes Processed:** 4.1 GB  
**Query Text:**
```sql
-- Initial seller VOC response volume audit
SELECT 
    survey_type,
    score_type,
    COUNT(response_id) AS response_count,
    ROUND(AVG(score), 2) AS avg_score
FROM `nexus-analyst-demo.acme_ecomm.fact_seller_voc_responses`
GROUP BY 1, 2;
```
*Analyst Note:* Auditing early returns from the newly launched Seller Pulse survey program. Response rates looking healthy across onboarding milestones.

---

### [2026-04-17T11:20:55Z] — `derek.holloway` (assoc_100151)
**Job ID:** `bq_job_1588413655102`  
**Bytes Processed:** 88.5 GB  
**Query Text:**
```sql
-- Acme+ member plan distribution and price points
SELECT 
    plan_type,
    plan_price_usd,
    COUNT(member_id) AS member_count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
WHERE status = 'active'
GROUP BY 1, 2;
```
*Analyst Note:* Membership tier split query for annual planning decks. Annual subscription adoption remains robust across cohorts.

---

### [2026-04-17T12:04:18Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1588416258334`  
**Bytes Processed:** 24.6 GB  
**Query Text:**
```sql
-- Fulfillment node active status review
SELECT 
    node_type,
    market,
    COUNT(node_id) AS node_count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE is_active = TRUE
GROUP BY 1, 2
ORDER BY node_count DESC;
```
*Analyst Note:* Verifying fulfillment network dimensions for the upcoming supply chain efficiency quarterly report.

---

### [2026-04-17T13:45:30Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1588422330182`  
**Bytes Processed:** 67.3 GB  
**Query Text:**
```sql
-- Care contact channel distribution
SELECT 
    channel,
    sub_program,
    COUNT(contact_id) AS contacts
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at >= TIMESTAMP('2026-04-01')
GROUP BY 1, 2
ORDER BY contacts DESC;
```
*Analyst Note:* Care channel split confirms chat and bot handling remain dominant following the Ask Acme v2 rollout.

---

### [2026-04-17T14:10:09Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1588423809912`  
**Bytes Processed:** 215.0 GB  
**Query Text:**
```sql
-- Q1FY27 GMV reconciliation across conversion channels and marketplace
SELECT 
    t1.market,
    SUM(t1.gmv_usd) AS conv_gmv
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary` t1
WHERE t1.fiscal_week_ending BETWEEN '2026-02-01' AND '2026-03-31'
GROUP BY 1;
```
*Analyst Note:* Financial close reconciliation for Q1 conversion channels. Numbers match preliminary MBR figures.

---

### [2026-04-17T15:02:41Z] — `sanjay.bhatt` (assoc_100120)
**Job ID:** `bq_job_1588426961440`  
**Bytes Processed:** 18.3 GB  
**Query Text:**
```sql
-- Collectibles active listings authenticity audit
SELECT 
    authenticity_verified,
    COUNT(listing_id) AS listings
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
WHERE category = 'collectibles'
  AND status = 'active'
GROUP BY 1;
```
*Analyst Note:* Checking proportion of verified collectibles listings following the GradeSure badge integration rollout.

---

### [2026-04-17T16:30:15Z] — `tara.oduya` (assoc_100140)
**Job ID:** `bq_job_1588432215881`  
**Bytes Processed:** 54.2 GB  
**Query Text:**
```sql
-- Fulfillment speed daily on-time rates by channel
SELECT 
    fulfillment_type,
    ROUND(AVG(on_time_rate), 4) AS avg_on_time,
    SUM(orders_promised) AS total_orders
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE date >= '2026-04-01'
GROUP BY 1;
```
*Analyst Note:* Monitoring pickup and ship-to-home delivery performance for April QTD operational summary.

---

---

### [2026-04-17T16:55:02Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1588433702119`  
**Bytes Processed:** 1.4 TB  
**Query Text:**
```sql
-- Partition health check for high-volume order fact tables
SELECT 
    table_name,
    partition_id,
    total_rows,
    size_bytes
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name IN ('fact_orders', 'fact_traffic_daily', 'fact_care_contacts')
ORDER BY size_bytes DESC;
```
*Analyst Note:* Routine storage audit of daily partition sizes following the Q1 fiscal close processing run.

---

### [2026-04-17T17:15:33Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1588434933010`  
**Bytes Processed:** 45.8 GB  
**Query Text:**
```sql
-- Daily average order value by device and market across Q1
SELECT 
    date,
    market,
    device,
    SUM(gmv_usd) / NULLIF(SUM(orders), 0) AS calculated_aov
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date BETWEEN '2026-02-01' AND '2026-03-31'
GROUP BY 1, 2, 3
ORDER BY date DESC, market ASC;
```
*Analyst Note:* Spot-checking daily AOV calculations against monthly board reporting totals.

---

### [2026-04-18T09:04:12Z] — `sanjay.bhatt` (assoc_100120)
**Job ID:** `bq_job_1588491852441`  
**Bytes Processed:** 92.1 GB  
**Query Text:**
```sql
-- Collectibles seller listing distribution and active counts
SELECT 
    t1.seller_id,
    t2.seller_name,
    COUNT(t1.listing_id) AS active_listings
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings` t1
JOIN `nexus-analyst-demo.acme_ecomm.dim_seller` t2 ON t1.seller_id = t2.seller_id
WHERE t1.category = 'collectibles'
  AND t1.status = 'active'
GROUP BY 1, 2
ORDER BY active_listings DESC
LIMIT 50;
```
*Analyst Note:* Reviewing top active collectibles seller catalog depth post-GradeSure rollout.

---

### [2026-04-18T10:22:18Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1588496938992`  
**Bytes Processed:** 310.5 GB  
**Query Text:**
```sql
-- Session definition version audit across pre and post cutoff dates
SELECT 
    sessions_definition_version,
    date,
    SUM(sessions) AS total_sessions,
    SUM(orders) AS total_orders
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date BETWEEN '2026-02-15' AND '2026-03-15'
GROUP BY 1, 2
ORDER BY date ASC;
```
*Analyst Note:* Verifying clean separation of session counting versions around the March 2 bot filtering cutover.

---

### [2026-04-18T11:45:09Z] — `tara.oduya` (assoc_100140)
**Job ID:** `bq_job_1588501509123`  
**Bytes Processed:** 24.6 GB  
**Query Text:**
```sql
-- Fulfillment speed on-time rate by node type for April QTD
SELECT 
    t2.node_type,
    SUM(t1.orders_promised) AS promised,
    SUM(t1.orders_on_time) AS on_time,
    ROUND(SUM(t1.orders_on_time) / NULLIF(SUM(t1.orders_promised), 0), 4) AS on_time_rate
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual` t1
LEFT JOIN `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node` t2 ON t1.node_id = t2.node_id
WHERE t1.date >= '2026-04-01'
GROUP BY 1;
```
*Analyst Note:* Checking fulfillment performance by facility type for the ongoing April operational update.

---

### [2026-04-18T13:10:44Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1588506644208`  
**Bytes Processed:** 67.3 GB  
**Query Text:**
```sql
-- Care contact volume and CSAT by sub-program post Ask Acme v2
SELECT 
    sub_program,
    channel,
    COUNT(contact_id) AS total_contacts,
    ROUND(AVG(csat_score), 2) AS avg_csat
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at >= TIMESTAMP('2026-03-01')
GROUP BY 1, 2
ORDER BY total_contacts DESC;
```
*Analyst Note:* Evaluating customer care CSAT recovery across chat and bot channels following the March returns backlog clearance.

---

### [2026-04-18T14:33:50Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1588511630114`  
**Bytes Processed:** 142.0 GB  
**Query Text:**
```sql
-- Q1FY27 marketplace GMV summary rollup check against mart
SELECT 
    fiscal_week_ending,
    sub_vertical_code,
    SUM(gmv_usd) AS weekly_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE fiscal_week_ending BETWEEN '2026-02-01' AND '2026-03-31'
GROUP BY 1, 2
ORDER BY fiscal_week_ending DESC;
```
*Analyst Note:* Reconciling weekly marketplace summary tables for the finance monthly review deck.

---

### [2026-04-18T15:02:11Z] — `owen.faust` (assoc_100111)
**Job ID:** `bq_job_1588513331890`  
**Bytes Processed:** 88.4 GB  
**Query Text:**
```sql
-- Checkout Simplify experiment exposure analysis
SELECT 
    experiment_id,
    variant,
    SUM(units_assigned) AS assigned,
    SUM(units_exposed) AS exposed,
    SUM(units_converted) AS converted
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures`
WHERE experiment_id = 'exp_2214'
GROUP BY 1, 2;
```
*Analyst Note:* Pulling final exposed vs assigned tallies for Checkout Simplify following its full rollout decision.

---

### [2026-04-18T16:20:05Z] — `camille.duarte` (assoc_100123)
**Job ID:** `bq_job_1588518005332`  
**Bytes Processed:** 12.1 GB  
**Query Text:**
```sql
-- Initial pull of seller pulse survey responses across categories
SELECT 
    survey_type,
    score_type,
    ROUND(AVG(score), 2) AS avg_score,
    COUNT(response_id) AS responses
FROM `nexus-analyst-demo.acme_ecomm.fact_seller_voc_responses`
GROUP BY 1, 2;
```
*Analyst Note:* First baseline review of the newly populated seller pulse survey stream across onboarding milestones.

---

### [2026-04-19T09:30:15Z] — `malik.hendon` (assoc_100160)
**Job ID:** `bq_job_1588575015780`  
**Bytes Processed:** 34.5 GB  
**Query Text:**
```sql
-- B2B wholesale order volume and average basket size check
SELECT 
    market,
    COUNT(order_id) AS b2b_orders,
    ROUND(AVG(gmv_usd), 2) AS avg_order_value
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE vertical_code = 'B2B'
  AND order_date >= '2026-02-01'
GROUP BY 1;
```
*Analyst Note:* Checking wholesale order volumes and basket values for B2B quarterly pacing review.

---

### [2026-04-19T10:45:22Z] — `derek.holloway` (assoc_100151)
**Job ID:** `bq_job_1588579522104`  
**Bytes Processed:** 58.9 GB  
**Query Text:**
```sql
-- Acme+ membership plan distribution across active panel
SELECT 
    plan_type,
    status,
    COUNT(member_id) AS members
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
GROUP BY 1, 2;
```
*Analyst Note:* Reviewing annual vs monthly plan distribution across the 120k member panel.

---

### [2026-04-19T11:22:01Z] — `sanjay.bhatt` (assoc_100120)
**Job ID:** `bq_job_1588581721512`  
**Bytes Processed:** 19.8 GB  
**Query Text:**
```sql
-- Marketplace listings authenticity check by category
SELECT 
    category,
    authenticity_verified,
    COUNT(listing_id) AS listing_count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY 1, 2;
```
*Analyst Note:* Auditing verified badge coverage across collectibles, resold, and style categories.

---

---

### [2026-04-19T11:55:40Z] — `connor.blake` (assoc_10012)
**Job ID:** `bq_job_1588583740192`  
**Bytes Processed:** 7.4 GB  
**Query Text:**
```sql
-- Daily audit of table partition sizes across core fact tables
SELECT 
    table_name,
    ROUND(SUM(size_bytes) / 1024 / 1024 / 1024, 2) AS size_gb
FROM `nexus-analyst-demo.acme_ecomm.__TABLES__`
GROUP BY 1
ORDER BY size_gb DESC;
```
*Analyst Note:* Routine storage audit following the weekly partition compaction run.

---

### [2026-04-19T13:10:05Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1588588205441`  
**Bytes Processed:** 42.1 GB  
**Query Text:**
```sql
-- Preliminary MBR revenue reconciliation check against active marts
SELECT 
    EXTRACT(MONTH FROM fiscal_week_ending) AS fiscal_month,
    SUM(gmv_usd) AS monthly_gmv
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE fiscal_week_ending >= '2026-02-01'
GROUP BY 1;
```
*Analyst Note:* Pulling preliminary figures for the upcoming monthly finance package review.

---

### [2026-04-19T14:05:18Z] — `julian.moss` (assoc_100131)
**Job ID:** `bq_job_1588591518330`  
**Bytes Processed:** 16.3 GB  
**Query Text:**
```sql
-- Care platform sub-program ticket categorization audit
SELECT 
    sub_program,
    channel,
    COUNT(contact_id) AS total_contacts
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at >= '2026-04-01'
GROUP BY 1, 2;
```
*Analyst Note:* Checking chat vs bot contact distribution across optimization and platform sub-programs.

---

### [2026-04-19T15:30:44Z] — `lucia.ferreira` (assoc_100320)
**Job ID:** `bq_job_1588596644812`  
**Bytes Processed:** 28.6 GB  
**Query Text:**
```sql
-- Marketplace listing authenticity flag review by category
SELECT 
    category,
    authenticity_verified,
    COUNT(listing_id) AS listings
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
WHERE status = 'active'
GROUP BY 1, 2;
```
*Analyst Note:* Verifying badge coverage ratios across active collectible and style inventory pools.

---

### [2026-04-19T16:15:02Z] — `noah.kessler` (assoc_100122)
**Job ID:** `bq_job_1588599302194`  
**Bytes Processed:** 51.2 GB  
**Query Text:**
```sql
-- Resold category GMV pacing check across top sellers
SELECT 
    s.seller_name,
    SUM(o.gmv_usd) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders` o
JOIN `nexus-analyst-demo.acme_ecomm.dim_seller` s ON o.seller_id = s.seller_id
WHERE o.vertical_code = 'MARKETPLACE'
  AND s.category_focus = 'resold'
  AND o.order_date >= '2026-02-01'
GROUP BY 1
ORDER BY total_gmv DESC
LIMIT 15;
```
*Analyst Note:* Checking top resold seller contributions to evaluate ongoing category acceleration.

---

### [2026-04-20T08:45:12Z] — `sanjay.bhatt` (assoc_100120)
**Job ID:** `bq_job_1588661112450`  
**Bytes Processed:** 14.8 GB  
**Query Text:**
```sql
-- Collectibles active listings count check
SELECT 
    COUNT(listing_id) AS active_collectibles
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
WHERE category = 'collectibles'
  AND status = 'active';
```
*Analyst Note:* Quick validation of active collectible inventory count prior to grading partner sync.

---

### [2026-04-20T09:22:38Z] — `camille.duarte` (assoc_100123)
**Job ID:** `bq_job_1588663358901`  
**Bytes Processed:** 8.9 GB  
**Query Text:**
```sql
-- Initial pull of seller onboarding pulse survey response distribution
SELECT 
    survey_type,
    score_type,
    COUNT(response_id) AS total_responses
FROM `nexus-analyst-demo.acme_ecomm.fact_seller_voc_responses`
GROUP BY 1, 2;
```
*Analyst Note:* Confirming survey data stream population across onboarding milestones following program launch.

---

### [2026-04-20T10:15:50Z] — `owen.faust` (assoc_100111)
**Job ID:** `bq_job_1588666550220`  
**Bytes Processed:** 67.4 GB  
**Query Text:**
```sql
-- Search query performance check post checkout rollout
SELECT 
    device,
    COUNT(DISTINCT sessions) AS distinct_sessions
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date >= '2026-04-01'
GROUP BY 1;
```
*Analyst Note:* Monitoring session volume distribution by device type during early April.

---

### [2026-04-20T11:04:19Z] — `tara.oduya` (assoc_100140)
**Job ID:** `bq_job_1588669459332`  
**Bytes Processed:** 31.7 GB  
**Query Text:**
```sql
-- Fulfillment speed on-time rate by delivery type
SELECT 
    fulfillment_type,
    SUM(orders_promised) AS total_promised,
    SUM(orders_on_time) AS total_ontime
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE date >= '2026-03-01'
GROUP BY 1;
```
*Analyst Note:* Reviewing post-winter-storm promise performance across fulfillment channels.

---

### [2026-04-20T13:40:22Z] — `derek.holloway` (assoc_100151)
**Job ID:** `bq_job_1588678822105`  
**Bytes Processed:** 24.3 GB  
**Query Text:**
```sql
-- Acme+ membership acquisition channel breakdown
SELECT 
    acquisition_channel,
    status,
    COUNT(member_id) AS members
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
GROUP BY 1, 2;
```
*Analyst Note:* Analyzing panel signup channels to support upcoming retention modeling work.

---

### [2026-04-20T14:25:01Z] — `malik.hendon` (assoc_100160)
**Job ID:** `bq_job_1588681501678`  
**Bytes Processed:** 39.0 GB  
**Query Text:**
```sql
-- B2B order fulfillment method distribution
SELECT 
    fulfillment_type,
    COUNT(order_id) AS orders,
    ROUND(SUM(gmv_usd), 2) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE vertical_code = 'B2B'
GROUP BY 1;
```
*Analyst Note:* Auditing wholesale delivery preferences across commercial client accounts.

---

### [2026-04-20T15:12:44Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1588684364890`  
**Bytes Processed:** 53.8 GB  
**Query Text:**
```sql
-- Medallia VOC sentiment distribution by survey type
SELECT 
    survey_type,
    sentiment,
    COUNT(response_id) AS responses
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE responded_at >= '2026-03-01'
GROUP BY 1, 2;
```
*Analyst Note:* Reviewing post-purchase customer feedback sentiment trends following the March operational normalization.

---

### [2026-04-20T16:01:33Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1588687293144`  
**Bytes Processed:** 12.5 GB  
**Query Text:**
```sql
-- Daily load monitoring check for experiment exposure tables
SELECT 
    experiment_id,
    COUNT(DISTINCT exposure_date) AS active_days
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures`
GROUP BY 1;
```
*Analyst Note:* Checking exposure table partition ingestion completeness for active product experiments.

---

### [2026-04-21T09:15:20Z] — `maya.lindqvist` (assoc_100110)
**Job ID:** `bq_job_1588746920510`  
**Bytes Processed:** 48.2 GB  
**Query Text:**
```sql
-- US conversion rate comparison across session definition versions
SELECT 
    sessions_definition_version,
    SUM(sessions) AS total_sessions,
    SUM(orders) AS total_orders,
    ROUND(SUM(orders) / SUM(sessions) * 100, 4) AS blended_conv_rate
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE market = 'US'
  AND date >= '2026-02-01'
GROUP BY 1;
```
*Analyst Note:* Checking pre- and post-cutover conversion rates in traffic table prior to weekly sync.

---

### [2026-04-21T10:02:11Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1588749731290`  
**Bytes Processed:** 19.4 GB  
**Query Text:**
```sql
-- Marketplace GMV summary mart vs orders sample cross-check
SELECT 
    fiscal_week_ending,
    sub_vertical_code,
    gmv_usd
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE fiscal_week_ending >= '2026-03-01'
ORDER BY fiscal_week_ending DESC
LIMIT 10;
```
*Analyst Note:* Pulling weekly aggregate marketplace figures for finance review reconciliation.

---

### [2026-04-21T11:20:45Z] — `sanjay.bhatt` (assoc_100120)
**Job ID:** `bq_job_1588754445672`  
**Bytes Processed:** 36.1 GB  
**Query Text:**
```sql
-- Collectibles seller performance and return rate audit
SELECT 
    seller_id,
    active_listings,
    ROUND(return_rate * 100, 2) AS return_pct,
    ROUND(trailing_90d_gmv_usd, 2) AS gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
WHERE category_focus = 'collectibles'
ORDER BY gmv DESC
LIMIT 20;
```
*Analyst Note:* Reviewing top collectible seller return metrics following verification rollout.

---

### [2026-04-21T13:14:02Z] — `aisha.rahman` (assoc_100130)
**Job ID:** `bq_job_1588761242310`  
**Bytes Processed:** 27.9 GB  
**Query Text:**
```sql
-- Care deflection daily summary check
SELECT 
    sub_program,
    ROUND(AVG(deflection_rate) * 100, 2) AS avg_deflection_pct
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
WHERE date >= '2026-04-01'
GROUP BY 1;
```
*Analyst Note:* Monitoring early April deflection trends across automated and assisted care channels.

---

### [2026-04-21T14:08:50Z] — `ines.delgado` (assoc_100121)
**Job ID:** `bq_job_1588764530891`  
**Bytes Processed:** 44.5 GB  
**Query Text:**
```sql
-- Style category listing status distribution
SELECT 
    status,
    authenticity_verified,
    COUNT(listing_id) AS count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
WHERE category = 'style'
GROUP BY 1, 2;
```
*Analyst Note:* Auditing active apparel listings and verification status flags for style inventory.

---

### [2026-04-21T15:30:19Z] — `leo.brandt` (assoc_100141)
**Job ID:** `bq_job_1588769419204`  
**Bytes Processed:** 61.3 GB  
**Query Text:**
```sql
-- Fulfillment speed daily cost per order trend check
SELECT 
    date,
    fulfillment_type,
    ROUND(avg_cost_per_order_usd, 2) as cost_per_order
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE vertical_code = 'SPEED'
  AND date >= '2026-03-01'
ORDER BY date DESC
LIMIT 25;
```
*Analyst Note:* Examining post-automation unit cost trends across fulfillment channels.

---

### [2026-04-22T09:10:04Z] — `simone.laurent` (assoc_100150)
**Job ID:** `bq_job_1588833004120`  
**Bytes Processed:** 15.6 GB  
**Query Text:**
```sql
-- Membership panel plan type distribution check
SELECT 
    plan_type,
    status,
    COUNT(member_id) AS count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
GROUP BY 1, 2;
```
*Analyst Note:* Verifying active monthly vs annual subscriber counts within the membership sample panel.

---

### [2026-04-22T10:05:40Z] — `camille.duarte` (assoc_100123)
**Job ID:** `bq_job_1588836340552`  
**Bytes Processed:** 11.2 GB  
**Query Text:**
```sql
-- Seller VOC verbatim theme breakdown for onboarding surveys
SELECT 
    theme_tag,
    COUNT(response_id) AS verbatims
FROM `nexus-analyst-demo.acme_ecomm.fact_seller_voc_responses`
WHERE survey_type LIKE 'onboarding_pulse_%'
GROUP BY 1
ORDER BY verbatims DESC;
```
*Analyst Note:* Initial theme categorization review of newly collected seller pulse survey verbatims.

---

### [2026-04-22T11:18:22Z] — `owen.faust` (assoc_100111)
**Job ID:** `bq_job_1588840702819`  
**Bytes Processed:** 58.4 GB  
**Query Text:**
```sql
-- Checkout experiment readouts parameter audit
SELECT 
    experiment_id,
    variant,
    metric_name,
    metric_value,
    lift_vs_control_pct
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`
WHERE experiment_id = 'exp_2214';
```
*Analyst Note:* Reviewing final readout metrics for the completed Checkout Simplify experiment.

---

### [2026-04-22T13:02:15Z] — `gabriel.stroud` (assoc_100330)
**Job ID:** `bq_job_1588846935411`  
**Bytes Processed:** 33.8 GB  
**Query Text:**
```sql
-- Promise vs actual fulfillment performance by node
SELECT 
    node_id,
    SUM(orders_promised) AS promised,
    SUM(orders_on_time) AS on_time
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE date >= '2026-03-01'
  AND node_id IS NOT NULL
GROUP BY 1;
```
*Analyst Note:* Auditing fulfillment node delivery performance following distribution center sortation automation rollouts.

---

### [2026-04-22T14:15:50Z] — `derek.holloway` (assoc_100151)
**Job ID:** `bq_job_1588851350672`  
**Bytes Processed:** 72.1 GB  
**Query Text:**
```sql
-- Member CLTV distribution with explicit COALESCE check
SELECT 
    m.plan_type,
    COUNT(c.member_id) AS members,
    ROUND(AVG(COALESCE(c.trailing_12mo_gmv_usd, 0)), 2) AS avg_trailing_gmv
FROM `nexus-analyst-demo.acme_ecomm.dim_member` m
LEFT JOIN `nexus-analyst-demo.acme_ecomm.member_cltv` c ON m.member_id = c.member_id
GROUP BY 1;
```
*Analyst Note:* Running CLTV mart join verification to ensure dormant panel members are properly retained with zero-order defaults.

---

### [2026-04-22T15:40:11Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1588856411904`  
**Bytes Processed:** 18.9 GB  
**Query Text:**
```sql
-- Information schema check for marketplace tables
SELECT 
    table_name,
    row_count,
    ROUND(size_bytes / 1024 / 1024, 2) AS size_mb
FROM `nexus-analyst-demo.acme_ecomm.__TABLES__`
WHERE table_name LIKE '%marketplace%';
```
*Analyst Note:* Routine table size verification across marketplace base and summary tables.

---

### [2026-04-23T08:55:30Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1588928130221`  
**Bytes Processed:** 29.3 GB  
**Query Text:**
```sql
-- Q1FY27 traffic and GMV summary by market
SELECT 
    market,
    SUM(sessions) AS total_sessions,
    ROUND(SUM(gmv_usd), 2) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE fiscal_week_ending >= '2026-02-01'
GROUP BY 1;
```
*Analyst Note:* Aggregating regional performance totals for executive dashboard validation.

---

### [2026-04-23T09:42:18Z] — `lucia.ferreira` (assoc_100320)
**Job ID:** `bq_job_1588930938450`  
**Bytes Processed:** 22.7 GB  
**Query Text:**
```sql
-- Marketplace listing status audit across all categories
SELECT 
    category,
    status,
    COUNT(listing_id) AS listings
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY 1, 2;
```
*Analyst Note:* Checking active vs removed listing counts across collectibles, resold, and style inventories.

---

### [2026-04-23T10:30:05Z] — `malik.hendon` (assoc_100160)
**Job ID:** `bq_job_1588933805129`  
**Bytes Processed:** 35.8 GB  
**Query Text:**
```sql
-- B2B wholesale order basket size distribution
SELECT 
    market,
    COUNT(order_id) AS orders,
    ROUND(AVG(gmv_usd), 2) AS avg_basket_usd
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE vertical_code = 'B2B'
  AND order_date >= '2026-02-01'
GROUP BY 1;
```
*Analyst Note:* Reviewing wholesale order metrics for quarterly B2B pacing updates.

---

### [2026-04-23T11:15:44Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1588936544710`  
**Bytes Processed:** 41.2 GB  
**Query Text:**
```sql
-- Care contact resolution codes by channel
SELECT 
    channel,
    resolution_code,
    COUNT(contact_id) AS contacts
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at >= '2026-04-01'
GROUP BY 1, 2;
```
*Analyst Note:* Analyzing support resolution pathways following bot handoff adjustments.

---

### [2026-04-23T13:20:11Z] — `sanjay.bhatt` (assoc_100120)
**Job ID:** `bq_job_1588944011382`  
**Bytes Processed:** 19.1 GB  
**Query Text:**
```sql
-- Collectibles seller performance summary metrics
SELECT 
    COUNT(seller_id) AS active_sellers,
    ROUND(AVG(trailing_90d_gmv_usd), 2) AS avg_seller_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
WHERE category_focus = 'collectibles';
```
*Analyst Note:* Quick check of collectible seller tier output metrics.

---

### [2026-04-23T14:08:33Z] — `maya.lindqvist` (assoc_100110)
**Job ID:** `bq_job_1588946913520`  
**Bytes Processed:** 54.6 GB  
**Query Text:**
```sql
-- US traffic conversion summary weekly trend check
SELECT 
    fiscal_week_ending,
    sessions,
    orders,
    conversion_rate
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'US'
  AND fiscal_week_ending >= '2026-03-01'
ORDER BY fiscal_week_ending DESC;
```
*Analyst Note:* Reviewing weekly conversion metrics post session definition cutover.

---

### [2026-04-23T15:02:45Z] — `camille.duarte` (assoc_100123)
**Job ID:** `bq_job_1588950165901`  
**Bytes Processed:** 14.3 GB  
**Query Text:**
```sql
-- Seller pulse survey score distribution check
SELECT 
    survey_type,
    ROUND(AVG(score), 2) AS avg_score,
    COUNT(response_id) AS responses
FROM `nexus-analyst-demo.acme_ecomm.fact_seller_voc_responses`
GROUP BY 1;
```
*Analyst Note:* Reviewing average scores across newly established onboarding pulse surveys.

---

### [2026-04-24T09:12:04Z] — `tara.oduya` (assoc_100140)
**Job ID:** `bq_job_1589015524102`  
**Bytes Processed:** 38.4 GB  
**Query Text:**
```sql
-- Fulfillment speed daily mix share verification
SELECT 
    fulfillment_type,
    ROUND(AVG(pct_of_total_orders) * 100, 2) AS avg_mix_pct
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE date >= '2026-03-01'
GROUP BY 1;
```
*Analyst Note:* Checking fulfillment channel mix shares to monitor pickup growth trends.

---

### [2026-04-24T10:01:50Z] — `owen.faust` (assoc_100111)
**Job ID:** `bq_job_1589018510340`  
**Bytes Processed:** 46.9 GB  
**Query Text:**
```sql
-- Experiment readout summary for navigation refresh holdback
SELECT 
    experiment_id,
    metric_name,
    metric_value,
    lift_vs_control_pct
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`
WHERE experiment_id = 'exp_2215';
```
*Analyst Note:* Pulling independent holdback lift metrics for the sitewide navigation redesign.

---

### [2026-04-24T11:22:15Z] — `simone.laurent` (assoc_100150)
**Job ID:** `bq_job_1589023335812`  
**Bytes Processed:** 21.5 GB  
**Query Text:**
```sql
-- Membership lifecycle events distribution by type
SELECT 
    event_type,
    COUNT(event_id) AS events
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
WHERE event_date >= '2026-02-01'
GROUP BY 1;
```
*Analyst Note:* Auditing renewal and cancellation event volumes across the membership panel.

---

### [2026-04-24T13:10:40Z] — `derek.holloway` (assoc_100151)
**Job ID:** `bq_job_1589030040129`  
**Bytes Processed:** 31.2 GB  
**Query Text:**
```sql
-- Member CLTV trailing 12-month GMV summary
SELECT 
    tenure_days,
    ROUND(AVG(trailing_12mo_gmv_usd), 2) AS avg_gmv
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`
GROUP BY 1
ORDER BY tenure_days DESC
LIMIT 20;
```
*Analyst Note:* Examining cohort tenure length against trailing 12-month purchase volume.

---

### [2026-04-24T14:05:22Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1589033122670`  
**Bytes Processed:** 8.1 GB  
**Query Text:**
```sql
-- Partition expiration check on heavy traffic tables
SELECT 
    table_name,
    partition_id
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'fact_traffic_daily';
```
*Analyst Note:* Verifying daily partitioning rules for clickstream ingestion tables.

---

### [2026-04-24T15:30:11Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1589038211540`  
**Bytes Processed:** 50.3 GB  
**Query Text:**
```sql
-- Cross-vertical GMV contribution check for Q1FY27
SELECT 
    vertical_code,
    ROUND(SUM(gmv_usd), 2) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date >= '2026-02-01'
  AND date <= '2026-04-15'
GROUP BY 1;
```
*Analyst Note:* Running preliminary vertical contribution totals for executive Q1 financial pack.

---

### [2026-04-24T16:15:04Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1589052004118`  
**Bytes Processed:** 12.4 GB  
**Query Text:**
```sql
-- Checking daily ingestion row counts for traffic and orders
SELECT 
    date,
    market,
    COUNT(1) AS row_count
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date >= '2026-04-01'
GROUP BY 1, 2
ORDER BY date DESC;
```
*Analyst Note:* Spot check after yesterday's partition maintenance run on the ingestion pipeline.

---

### [2026-04-24T17:02:40Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1589055760291`  
**Bytes Processed:** 74.8 GB  
**Query Text:**
```sql
-- Monthly GMV trend by vertical across Q1FY27
SELECT 
    v.vertical_name,
    EXTRACT(MONTH FROM t.date) AS fiscal_month,
    ROUND(SUM(t.gmv_usd), 2) AS monthly_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily` t
JOIN `nexus-analyst-demo.acme_ecomm.dim_vertical` v 
  ON t.vertical_code = v.vertical_code
WHERE t.date >= '2026-02-01'
  AND t.date <= '2026-04-15'
GROUP BY 1, 2
ORDER BY 1, 2;
```
*Analyst Note:* Reconciling monthly vertical sums for the monthly finance deck.

---

### [2026-04-24T18:44:12Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1589061852934`  
**Bytes Processed:** 142.1 GB  
**Query Text:**
```sql
-- Validating session definition version split in fact_traffic_daily
SELECT 
    sessions_definition_version,
    COUNT(*) AS total_rows,
    SUM(sessions) AS total_sessions,
    ROUND(AVG(CAST(orders AS NUMERIC) / NULLIF(sessions, 0)), 4) AS avg_raw_conversion
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date >= '2026-02-01'
GROUP BY 1;
```
*Analyst Note:* Running diagnostic queries to confirm the clean split between pre- and post-March 2 session counting logic.

---

### [2026-04-24T20:10:55Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1589067055102`  
**Bytes Processed:** 28.6 GB  
**Query Text:**
```sql
-- Care contact volume and CSAT by channel for Q1FY27
SELECT 
    channel,
    sub_program,
    COUNT(contact_id) AS contacts,
    ROUND(AVG(csat_score), 2) AS avg_csat
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at >= '2026-02-01 00:00:00 UTC'
GROUP BY 1, 2
ORDER BY contacts DESC;
```
*Analyst Note:* Pulling channel breakdown for the bi-weekly care operations review.

---

### [2026-04-25T08:30:14Z] — `derek.holloway` (assoc_100151)
**Job ID:** `bq_job_1589111414872`  
**Bytes Processed:** 44.1 GB  
**Query Text:**
```sql
-- Member renewal rates by plan type across active panel
SELECT 
    plan_type,
    status,
    COUNT(*) AS member_count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
GROUP BY 1, 2;
```
*Analyst Note:* Checking panel distribution for annual versus monthly subscribers.

---

### [2026-04-25T09:45:20Z] — `simone.laurent` (assoc_100150)
**Job ID:** `bq_job_1589115920311`  
**Bytes Processed:** 19.3 GB  
**Query Text:**
```sql
-- Benefit redemption events by benefit code
SELECT 
    benefit_code,
    COUNT(event_id) AS redemptions
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
WHERE event_type = 'benefit_redeemed'
  AND event_date >= '2026-02-01'
GROUP BY 1
ORDER BY redemptions DESC;
```
*Analyst Note:* Reviewing top utilized Acme+ perks for the quarterly membership review deck.

---

### [2026-04-25T11:05:38Z] — `tara.oduya` (assoc_100140)
**Job ID:** `bq_job_1589120738645`  
**Bytes Processed:** 62.7 GB  
**Query Text:**
```sql
-- Fulfillment speed on-time rate by fulfillment type for Q1
SELECT 
    fulfillment_type,
    SUM(orders_promised) AS total_promised,
    SUM(orders_on_time) AS total_on_time,
    ROUND(SUM(orders_on_time) / SUM(orders_promised) * 100, 2) AS otp_pct
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE date >= '2026-02-01'
  AND date <= '2026-04-15'
GROUP BY 1;
```
*Analyst Note:* Verifying fulfillment speed aggregates following the DC sortation automation rollouts.

---

### [2026-04-25T13:22:01Z] — `leo.brandt` (assoc_100141)
**Job ID:** `bq_job_1589128921093`  
**Bytes Processed:** 15.8 GB  
**Query Text:**
```sql
-- Experiment exposure audit for Wider Promise Window
SELECT 
    variant,
    SUM(units_assigned) AS assigned,
    SUM(units_exposed) AS exposed
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures`
WHERE experiment_id = 'exp_1187'
GROUP BY 1;
```
*Analyst Note:* Post-mortem check on the promise window experiment traffic splits.

---

### [2026-04-25T14:40:19Z] — `owen.faust` (assoc_100111)
**Job ID:** `bq_job_1589133619482`  
**Bytes Processed:** 33.4 GB  
**Query Text:**
```sql
-- Checkout Simplify exposure vs conversion counts
SELECT 
    variant,
    SUM(units_exposed) AS exposed_units,
    SUM(units_converted) AS converted_units,
    ROUND(SUM(units_converted) / SUM(units_exposed) * 100, 2) AS conv_rate
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures`
WHERE experiment_id = 'exp_2214'
GROUP BY 1;
```
*Analyst Note:* Reviewing per-protocol readouts for the checkout simplify rollout.

---

### [2026-04-25T16:10:08Z] — `maya.lindqvist` (assoc_100110)
**Job ID:** `bq_job_1589139008512`  
**Bytes Processed:** 21.0 GB  
**Query Text:**
```sql
-- Nav Refresh experiment holdback readouts
SELECT 
    metric_name,
    metric_value,
    lift_vs_control_pct,
    is_significant
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`
WHERE experiment_id = 'exp_2215';
```
*Analyst Note:* Pulling final sitewide lift numbers for the navigation redesign holdback group.

---

### [2026-04-26T09:15:33Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1589188533204`  
**Bytes Processed:** 88.2 GB  
**Query Text:**
```sql
-- Marketplace GMV summary by sub vertical for Q1FY27
SELECT 
    sub_vertical_code,
    ROUND(SUM(gmv_usd), 2) AS total_gmv,
    SUM(orders) AS total_orders
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE fiscal_week_ending >= '2026-02-01'
GROUP BY 1
ORDER BY total_gmv DESC;
```
*Analyst Note:* Pulling official marketplace sub-vertical figures for the weekly executive reporting packet.

---

### [2026-04-26T10:40:12Z] — `sanjay.bhatt` (assoc_100120)
**Job ID:** `bq_job_1589193612741`  
**Bytes Processed:** 39.5 GB  
**Query Text:**
```sql
-- Collectibles seller performance metrics
SELECT 
    seller_id,
    active_listings,
    ROUND(trailing_90d_gmv_usd, 2) AS t90_gmv,
    return_rate
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
WHERE category_focus = 'collectibles'
ORDER BY t90_gmv DESC
LIMIT 25;
```
*Analyst Note:* Reviewing top collectable seller volumes and return rates post GradeSure integration.

---

### [2026-04-26T12:01:45Z] — `camille.duarte` (assoc_100123)
**Job ID:** `bq_job_1589198505882`  
**Bytes Processed:** 16.3 GB  
**Query Text:**
```sql
-- Seller Pulse survey response counts by theme
SELECT 
    theme_tag,
    COUNT(response_id) AS responses,
    ROUND(AVG(score), 2) AS avg_score
FROM `nexus-analyst-demo.acme_ecomm.fact_seller_voc_responses`
GROUP BY 1
ORDER BY responses DESC;
```
*Analyst Note:* Initial exploratory run on the newly populated seller VOC survey stream.

---

### [2026-04-26T14:15:20Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1589206520194`  
**Bytes Processed:** 9.2 GB  
**Query Text:**
```sql
-- Checking table schema for fact_seller_voc_responses
SELECT 
    column_name,
    data_type
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'fact_seller_voc_responses';
```
*Analyst Note:* Verifying column constraints for the new seller-side survey dataset.

---

### [2026-04-26T15:50:11Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1589212211603`  
**Bytes Processed:** 24.1 GB  
**Query Text:**
```sql
-- Buyer VOC Medallia sentiment distribution for Q1
SELECT 
    sentiment,
    COUNT(response_id) AS verbatims
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE responded_at >= '2026-02-01 00:00:00 UTC'
GROUP BY 1;
```
*Analyst Note:* Pulling customer satisfaction sentiment splits for the care and quality review meeting.

---

### [2026-04-27T09:10:25Z] — `malik.hendon` (assoc_100160)
**Job ID:** `bq_job_1589274625330`  
**Bytes Processed:** 51.6 GB  
**Query Text:**
```sql
-- B2B order volume and GMV contribution check
SELECT 
    sub_vertical_code,
    COUNT(order_id) AS orders,
    ROUND(SUM(gmv_usd), 2) AS gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE vertical_code = 'B2B'
  AND order_date >= '2026-02-01'
GROUP BY 1;
```
*Analyst Note:* Pulling baseline wholesale figures for the B2B catalog expansion review.

---

### [2026-04-27T10:33:48Z] — `ines.delgado` (assoc_100121)
**Job ID:** `bq_job_1589279628419`  
**Bytes Processed:** 31.9 GB  
**Query Text:**
```sql
-- Style category listing status breakdown
SELECT 
    status,
    COUNT(listing_id) AS listings
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
WHERE category = 'style'
GROUP BY 1;
```
*Analyst Note:* Auditing active versus removed listing counts across style supplier catalogs.

---

### [2026-04-27T11:55:02Z] — `noah.kessler` (assoc_100122)
**Job ID:** `bq_job_1589284502155`  
**Bytes Processed:** 38.4 GB  
**Query Text:**
```sql
-- Resold category GMV performance in marketplace mart
SELECT 
    fiscal_week_ending,
    ROUND(SUM(gmv_usd), 2) AS weekly_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE sub_vertical_code = 'RESOLD'
  AND fiscal_week_ending >= '2026-02-01'
GROUP BY 1
ORDER BY fiscal_week_ending DESC;
```
*Analyst Note:* Tracking weekly recommerce GMV growth against Q1 targets.

---

### [2026-04-27T13:40:19Z] — `aisha.rahman` (assoc_100130)
**Job ID:** `bq_job_1589290819721`  
**Bytes Processed:** 18.7 GB  
**Query Text:**
```sql
-- Bot deflection daily trend review for April
SELECT 
    date,
    sub_program,
    deflection_rate
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
WHERE date >= '2026-04-01'
  AND sub_program = 'automate'
ORDER BY date DESC;
```
*Analyst Note:* Checking daily deflection stability following the April 1 handoff experiment launch.

---

### [2026-04-27T15:20:41Z] — `julian.moss` (assoc_100131)
**Job ID:** `bq_job_1589296841032`  
**Bytes Processed:** 22.0 GB  
**Query Text:**
```sql
-- Care contact resolution codes distribution
SELECT 
    resolution_code,
    COUNT(contact_id) AS count
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at >= '2026-04-01 00:00:00 UTC'
GROUP BY 1
ORDER BY count DESC;
```
*Analyst Note:* Reviewing platform and optimize support ticket resolution patterns for monthly reporting.

---

### [2026-04-28T08:45:12Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1589359512411`  
**Bytes Processed:** 67.3 GB  
**Query Text:**
```sql
-- Company-wide GMV reconciliation check across verticals
SELECT 
    v.vertical_name,
    ROUND(SUM(t.gmv_usd), 2) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily` t
JOIN `nexus-analyst-demo.acme_ecomm.dim_vertical` v 
  ON t.vertical_code = v.vertical_code
WHERE t.date >= '2026-02-01'
  AND t.date <= '2026-04-15'
GROUP BY 1
ORDER BY total_gmv DESC;
```
*Analyst Note:* Finalizing Q1 financial reconciliation before executive leadership review.

---

### [2026-04-28T10:12:35Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1589364755109`  
**Bytes Processed:** 112.5 GB  
**Query Text:**
```sql
-- Daily traffic summary check for missing partitions
SELECT 
    date,
    COUNT(DISTINCT market) AS markets
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date >= '2026-02-01'
GROUP BY 1
HAVING markets < 3;
```
*Analyst Note:* Pipeline health check confirming all three markets (US, CA, MX) load successfully every day.

---

### [2026-04-28T11:30:10Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1589369410088`  
**Bytes Processed:** 8.4 GB  
**Query Text:**
```sql
-- Airflow DAG task duration audit for fact_marketplace_listings
SELECT 
    task_id,
    AVG(duration_seconds) AS avg_duration,
    MAX(duration_seconds) AS max_duration
FROM `nexus-analyst-demo.acme_ecomm.sys_airflow_task_logs`
WHERE execution_date >= '2026-04-01'
GROUP BY 1
ORDER BY max_duration DESC;
```
*Analyst Note:* Checking for retry spikes in the nightly marketplace listing ingestion pipeline.

---

### [2026-04-28T13:15:40Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1589375740123`  
**Bytes Processed:** 45.1 GB  
**Query Text:**
```sql
-- Quarterly order channel breakdown (1P vs 3P)
SELECT 
    channel,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(gmv_usd), 2) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE order_date >= '2026-02-01'
  AND order_date <= '2026-04-15'
GROUP BY 1;
```
*Analyst Note:* Pulling preliminary sample ratios for the finance MBR appendix deck.

---

### [2026-04-28T14:50:22Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1589381422901`  
**Bytes Processed:** 19.3 GB  
**Query Text:**
```sql
-- Care contact channel distribution check
SELECT 
    channel,
    COUNT(contact_id) AS contacts,
    ROUND(AVG(csat_score), 2) AS avg_csat
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at >= '2026-04-01 00:00:00 UTC'
GROUP BY 1
ORDER BY contacts DESC;
```
*Analyst Note:* Verifying chat vs. bot channel ratios following the April 1 handoff rule adjustment.

---

### [2026-04-29T09:10:04Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1589447404555`  
**Bytes Processed:** 5.2 GB  
**Query Text:**
```sql
-- Dimension date sanity check for fiscal quarters
SELECT 
    fiscal_quarter_label,
    COUNT(*) AS days
FROM `nexus-analyst-demo.acme_ecomm.dim_date`
WHERE fiscal_year = 2027
GROUP BY 1;
```
*Analyst Note:* Quick validation query prior to rebuilding the quarterly aggregation views.

---

### [2026-04-29T10:22:18Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1589451738210`  
**Bytes Processed:** 88.9 GB  
**Query Text:**
```sql
-- Daily GMV and order count validation for US market
SELECT 
    date,
    SUM(gmv_usd) AS daily_gmv,
    SUM(orders) AS daily_orders
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE market = 'US'
  AND date >= '2026-03-01'
  AND date <= '2026-04-15'
GROUP BY 1
ORDER BY date DESC;
```
*Analyst Note:* Reconciling post-cutover session version 2 numbers against legacy finance reports.

---

### [2026-04-29T14:05:33Z] — `julian.moss` (assoc_100131)
**Job ID:** `bq_job_1589465133912`  
**Bytes Processed:** 31.7 GB  
**Query Text:**
```sql
-- Care resolution codes for platform sub-program
SELECT 
    resolution_code,
    COUNT(contact_id) AS total
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE sub_program = 'platform'
  AND opened_at >= '2026-03-01 00:00:00 UTC'
GROUP BY 1
ORDER BY total DESC;
```
*Analyst Note:* Looking into persistent login and password reset ticket categories for Julian's weekly ops review.

---

### [2026-04-30T08:30:15Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1589531415440`  
**Bytes Processed:** 12.0 GB  
**Query Text:**
```sql
-- Table partition sizes in acme_ecomm dataset
SELECT 
    table_id,
    ROUND(size_bytes / 1024 / 1024 / 1024, 2) AS size_gb
FROM `nexus-analyst-demo.acme_ecomm.__TABLES__`
ORDER BY size_gb DESC;
```
*Analyst Note:* Monthly storage audit to verify partition expiration settings across base fact tables.

---

### [2026-04-30T11:45:09Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1589543109312`  
**Bytes Processed:** 104.2 GB  
**Query Text:**
```sql
-- Vertical-level GMV summary for Q1FY27 close
SELECT 
    v.vertical_name,
    ROUND(SUM(t.gmv_usd), 2) AS gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily` t
JOIN `nexus-analyst-demo.acme_ecomm.dim_vertical` v 
  ON t.vertical_code = v.vertical_code
WHERE t.date >= '2026-02-01'
  AND t.date <= '2026-04-15'
GROUP BY 1
ORDER BY gmv DESC;
```
*Analyst Note:* Generating final numbers for the Q1 executive summary deck.

---

### [2026-04-30T16:20:48Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1589560048102`  
**Bytes Processed:** 62.4 GB  
**Query Text:**
```sql
-- Device distribution check across traffic fact table
SELECT 
    device,
    SUM(sessions) AS total_sessions,
    ROUND(SUM(orders) / SUM(sessions) * 100, 2) AS conversion_pct
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date >= '2026-03-02'
  AND sessions_definition_version = 2
GROUP BY 1
ORDER BY total_sessions DESC;
```
*Analyst Note:* Auditing web vs app conversion performance on the new session definition standard.

---

### [2026-05-02T09:15:20Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1589706920119`  
**Bytes Processed:** 28.3 GB  
**Query Text:**
```sql
-- Monthly membership signup channel distribution
SELECT 
    acquisition_channel,
    COUNT(member_id) AS signups
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
WHERE signup_date >= '2026-02-01'
GROUP BY 1
ORDER BY signups DESC;
```
*Analyst Note:* Checking Acme+ acquisition channel mix for the monthly membership review.

---

### [2026-05-02T11:04:55Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1589713495821`  
**Bytes Processed:** 15.6 GB  
**Query Text:**
```sql
-- Check for null association keys in dim_associate
SELECT 
    COUNT(*) AS total_nulls
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
WHERE assoc_id IS NULL 
   OR full_name IS NULL;
```
*Analyst Note:* Routine data hygiene validation for HR dimension tables.

---

### [2026-05-03T14:30:12Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1589812212334`  
**Bytes Processed:** 76.8 GB  
**Query Text:**
```sql
-- Fulfillment type volume distribution across speed daily mart
SELECT 
    fulfillment_type,
    SUM(orders_promised) AS total_promised
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE date >= '2026-02-01'
GROUP BY 1
ORDER BY total_promised DESC;
```
*Analyst Note:* Verifying ship-to-home vs pickup order volume splits for supply chain reporting.

---

### [2026-05-04T08:55:40Z] — `julian.moss` (assoc_100131)
**Job ID:** `bq_job_1589878540211`  
**Bytes Processed:** 24.9 GB  
**Query Text:**
```sql
-- Care optimize sub-program ticket volume by channel
SELECT 
    channel,
    COUNT(contact_id) AS contacts
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE sub_program = 'optimize'
  AND opened_at >= '2026-04-01 00:00:00 UTC'
GROUP BY 1
ORDER BY contacts DESC;
```
*Analyst Note:* Reviewing support routing for shipping speed and tracking inquiries.

---

### [2026-05-04T13:20:11Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1589894411802`  
**Bytes Processed:** 110.3 GB  
**Query Text:**
```sql
-- Marketplace category GMV roll-up check
SELECT 
    sub_vertical_code,
    ROUND(SUM(gmv_usd), 2) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE fiscal_week_ending >= '2026-02-01'
GROUP BY 1
ORDER BY total_gmv DESC;
```
*Analyst Note:* Confirming marketplace summary numbers reconcile with the main traffic tables.

---

### [2026-05-05T10:11:05Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1589973065419`  
**Bytes Processed:** 9.1 GB  
**Query Text:**
```sql
-- Check distinct experiment IDs in dim_experiment
SELECT 
    status,
    COUNT(experiment_id) AS experiments
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment`
GROUP BY 1;
```
*Analyst Note:* Auditing active vs shipped experiments in preparation for the monthly experiment catalog sync.

---

### [2026-05-05T15:40:50Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1589992850911`  
**Bytes Processed:** 54.0 GB  
**Query Text:**
```sql
-- Traffic sessions definition version split audit
SELECT 
    sessions_definition_version,
    COUNT(*) AS partition_count,
    SUM(sessions) AS total_sessions
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date >= '2026-02-01'
GROUP BY 1;
```
*Analyst Note:* Ensuring the March 2 session definition cutover boundary is clearly separated in reporting pipelines.

---

### [2026-05-06T09:05:33Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1589053533104`  
**Bytes Processed:** 41.2 GB  
**Query Text:**
```sql
-- Average order value check by market
SELECT 
    market,
    ROUND(SUM(gmv_usd) / SUM(orders), 2) AS calculated_aov
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date >= '2026-02-01'
GROUP BY 1;
```
*Analyst Note:* Verifying regional AOV differentials across US, CA, and MX markets.

---

### [2026-05-06T14:12:18Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1589071938221`  
**Bytes Processed:** 33.5 GB  
**Query Text:**
```sql
-- Buyer VOC survey type volume distribution
SELECT 
    survey_type,
    COUNT(response_id) AS responses,
    ROUND(AVG(score), 2) AS avg_score
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE responded_at >= '2026-04-01 00:00:00 UTC'
GROUP BY 1;
```
*Analyst Note:* Running initial sentiment checks on post-purchase Medallia surveys for early May reporting.

---

### [2026-05-07T11:30:44Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1589161844910`  
**Bytes Processed:** 18.2 GB  
**Query Text:**
```sql
-- Fulfillment node active status check
SELECT 
    node_type,
    COUNT(node_id) AS nodes
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE is_active = TRUE
GROUP BY 1;
```
*Analyst Note:* Validating node counts across distribution centers and sortation hubs.

---

### [2026-05-07T16:05:12Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1589178312502`  
**Bytes Processed:** 95.7 GB  
**Query Text:**
```sql
-- Daily add to cart conversion ratio audit
SELECT 
    date,
    SUM(add_to_cart_sessions) AS atc_sessions,
    SUM(product_view_sessions) AS pvs_sessions,
    ROUND(SUM(add_to_cart_sessions) / NULLIF(SUM(product_view_sessions), 0) * 100, 2) AS atc_rate
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date >= '2026-03-02'
  AND sessions_definition_version = 2
GROUP BY 1
ORDER BY date DESC;
```
*Analyst Note:* Reviewing item page engagement metrics following the spring layout iteration rollout.

---

### [2026-05-08T09:40:21Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1589241621333`  
**Bytes Processed:** 68.4 GB  
**Query Text:**
```sql
-- Marketplace seller performance top tiers by trailing GMV
SELECT 
    seller_id,
    category_focus,
    trailing_90d_gmv_usd
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
ORDER BY trailing_90d_gmv_usd DESC
LIMIT 25;
```
*Analyst Note:* Pulling top marketplace performer lists for leadership review ahead of the monthly operating committee meeting.

---

### [2026-05-08T13:15:55Z] — `julian.moss` (assoc_100131)
**Job ID:** `bq_job_1589254555812`  
**Bytes Processed:** 21.0 GB  
**Query Text:**
```sql
-- Care contacts deflection rate check by date
SELECT 
    date,
    sub_program,
    deflection_rate
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
WHERE date >= '2026-04-01'
ORDER BY date DESC, deflection_rate DESC;
```
*Analyst Note:* Checking daily deflection stability following the April care handoff threshold adjustments.

---

### [2026-04-10T14:22:01Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1589542011004`  
**Bytes Processed:** 14.8 GB  
**Query Text:**
```sql
-- Partition check for fulfillment speed daily table
SELECT 
    table_name,
    partition_id,
    total_rows,
    size_bytes
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'fulfillment_speed_daily';
```
*Analyst Note:* Running routine partition health check across raw warehouse facts before the weekly pipeline refresh.

---

### [2026-04-11T08:12:44Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1589608124991`  
**Bytes Processed:** 112.3 GB  
**Query Text:**
```sql
-- Monthly traffic distribution by device type across US conversion channel
SELECT 
    device,
    SUM(sessions) AS total_sessions,
    SUM(orders) AS total_orders,
    ROUND(SUM(gmv_usd), 2) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date >= '2026-03-01'
  AND vertical_code = 'US_CONV'
  AND market = 'US'
GROUP BY 1
ORDER BY total_sessions DESC;
```
*Analyst Note:* Pulling preliminary post-cutover device breakdowns for the upcoming finance review.

---

### [2026-04-11T11:30:15Z] — `julian.moss` (assoc_100131)
**Job ID:** `bq_job_1589619015220`  
**Bytes Processed:** 34.2 GB  
**Query Text:**
```sql
-- Care contact volume by channel and sub-program
SELECT 
    sub_program,
    channel,
    COUNT(contact_id) AS contacts,
    ROUND(AVG(handle_time_minutes), 2) AS avg_handle_time
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at >= '2026-03-01'
GROUP BY 1, 2
ORDER BY contacts DESC;
```
*Analyst Note:* Auditing chat versus phone handle times following the bot threshold changes.

---

### [2026-04-11T16:45:09Z] — `camille.duarte` (assoc_100123)
**Job ID:** `bq_job_1589637909182`  
**Bytes Processed:** 18.5 GB  
**Query Text:**
```sql
-- Marketplace listing authenticity status breakdown
SELECT 
    category,
    authenticity_verified,
    COUNT(listing_id) AS listings_count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY 1, 2
ORDER BY category, authenticity_verified DESC;
```
*Analyst Note:* Reviewing unverified versus verified listings across collectibles and style categories during orientation week.

---

### [2026-04-12T10:05:33Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1589681133045`  
**Bytes Processed:** 77.1 GB  
**Query Text:**
```sql
-- Daily sessions definition version audit check
SELECT 
    sessions_definition_version,
    COUNT(*) AS row_count,
    MIN(date) AS min_date,
    MAX(date) AS max_date
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
GROUP BY 1;
```
*Analyst Note:* Verifying partition splits between version 1 and version 2 session logging rows.

---

### [2026-04-12T14:20:11Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1589696411509`  
**Bytes Processed:** 45.6 GB  
**Query Text:**
```sql
-- Membership annual vs monthly plan distribution check
SELECT 
    plan_type,
    status,
    COUNT(member_id) AS members
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
GROUP BY 1, 2;
```
*Analyst Note:* Spot-checking panel distribution for active versus paused Acme+ subscriber accounts.

---

### [2026-04-13T09:15:20Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1589745320112`  
**Bytes Processed:** 58.9 GB  
**Query Text:**
```sql
-- Buyer VOC sentiment distribution by survey type
SELECT 
    survey_type,
    sentiment,
    COUNT(response_id) AS responses,
    ROUND(AVG(score), 2) AS avg_score
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE responded_at >= TIMESTAMP('2026-03-01')
GROUP BY 1, 2
ORDER BY survey_type, responses DESC;
```
*Analyst Note:* Checking Medallia verbatim sentiment shifts following the March operational normalization.

---

### [2026-04-13T11:40:55Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1589754055301`  
**Bytes Processed:** 8.3 GB  
**Query Text:**
```sql
-- Fulfillment node active inventory type counts
SELECT 
    node_type,
    market,
    COUNT(node_id) AS active_nodes
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE is_active = TRUE
GROUP BY 1, 2
ORDER BY active_nodes DESC;
```
*Analyst Note:* Daily data warehouse sanity check on node dimension table integrity.

---

### [2026-04-13T15:22:18Z] — `camille.duarte` (assoc_100123)
**Job ID:** `bq_job_1589767338449`  
**Bytes Processed:** 24.1 GB  
**Query Text:**
```sql
-- Seller voice of customer survey response rate audit
SELECT 
    survey_type,
    score_type,
    COUNT(response_id) AS response_count,
    ROUND(AVG(score), 2) AS avg_seller_score
FROM `nexus-analyst-demo.acme_ecomm.fact_seller_voc_responses`
GROUP BY 1, 2;
```
*Analyst Note:* Initial audit of the newly populated seller pulse survey stream for onboarding feedback.

---

### [2026-04-14T08:50:12Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1589806212891`  
**Bytes Processed:** 152.0 GB  
**Query Text:**
```sql
-- Marketplace GMV summary roll-up check by fiscal week ending
SELECT 
    fiscal_week_ending,
    sub_vertical_code,
    SUM(gmv_usd) AS weekly_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE fiscal_week_ending >= '2026-03-01'
GROUP BY 1, 2
ORDER BY fiscal_week_ending DESC, weekly_gmv DESC;
```
*Analyst Note:* Reconciling marketplace sub-vertical weekly performance numbers ahead of the monthly operating review.

---

### [2026-04-14T13:10:44Z] — `julian.moss` (assoc_100131)
**Job ID:** `bq_job_1589821844005`  
**Bytes Processed:** 41.7 GB  
**Query Text:**
```sql
-- Care deflection daily summary by sub-program
SELECT 
    date,
    sub_program,
    contact_volume,
    deflection_rate,
    avg_csat_deflected
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
WHERE date >= '2026-04-01'
ORDER BY date DESC, deflection_rate DESC;
```
*Analyst Note:* Tracking deflection stability in the optimize and platform sub-programs following the bot threshold experiment launch.

---

### [2026-04-14T16:25:39Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1589833539112`  
**Bytes Processed:** 63.4 GB  
**Query Text:**
```sql
-- Traffic conversion summary verification for US market
SELECT 
    fiscal_week_ending,
    sessions,
    orders,
    conversion_rate,
    gmv_usd
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'US'
  AND vertical_code = 'US_CONV'
  AND fiscal_week_ending >= '2026-03-01'
ORDER BY fiscal_week_ending DESC;
```
*Analyst Note:* Checking board mart figures against raw traffic daily tables for consistency.

---

### [2026-04-15T09:30:21Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1589871021334`  
**Bytes Processed:** 89.2 GB  
**Query Text:**
```sql
-- Cross-vertical GMV pace check for Q1FY27 close
SELECT 
    vertical_code,
    SUM(gmv_usd) AS qtd_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date BETWEEN '2026-02-01' AND '2026-04-15'
GROUP BY 1
ORDER BY qtd_gmv DESC;
```
*Analyst Note:* Finalizing Q1FY27 QTD revenue figures for executive reporting packet preparation.

---

### [2026-04-15T11:05:42Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1589877442109`  
**Bytes Processed:** 15.2 GB  
**Query Text:**
```sql
-- Partition check for daily traffic and care contact base tables
SELECT 
    table_name,
    partition_id,
    total_rows,
    size_bytes
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name IN ('fact_traffic_daily', 'fact_care_contacts', 'fact_orders')
ORDER BY table_name, partition_id DESC;
```
*Analyst Note:* Running routine partition health check across raw fact tables prior to the weekly Airflow schema maintenance window.

---

### [2026-04-15T14:40:12Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1589890812984`  
**Bytes Processed:** 112.5 GB  
**Query Text:**
```sql
-- Vertical pacing and conversion check for Q1FY27 board deck
SELECT 
    t.vertical_code,
    SUM(t.sessions) AS total_sessions,
    SUM(t.orders) AS total_orders,
    ROUND(SUM(t.orders) / NULLIF(SUM(t.sessions), 0) * 100, 2) AS blended_conv_rate,
    SUM(t.gmv_usd) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily` t
WHERE t.date BETWEEN '2026-02-01' AND '2026-04-15'
GROUP BY 1
ORDER BY total_gmv DESC;
```
*Analyst Note:* Pulling final vertical contribution numbers for the Q1 MBR executive appendix. Note that pre-March-02 sessions use version 1 while post-March-02 uses version 2 per the bot filtering cutover.

---

### [2026-04-15T16:15:08Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1589896508412`  
**Bytes Processed:** 24.1 GB  
**Query Text:**
```sql
-- Diagnostic query for marketplace listings authenticity flag distribution
SELECT 
    category,
    authenticity_verified,
    COUNT(*) AS listing_count,
    ROUND(AVG(price_usd), 2) AS avg_listing_price
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY 1, 2
ORDER BY category, listing_count DESC;
```
*Analyst Note:* Verifying listing panel distributions for the marketplace quality audit requested by victor.okonkwo.

---

### [2026-04-15T17:50:33Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1589902833019`  
**Bytes Processed:** 45.8 GB  
**Query Text:**
```sql
-- Care contact resolution codes and CSAT by channel
SELECT 
    channel,
    resolution_code,
    COUNT(*) AS contact_count,
    ROUND(AVG(csat_score), 2) AS avg_csat
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at >= '2026-03-01'
GROUP BY 1, 2
ORDER BY contact_count DESC;
```
*Analyst Note:* Checking post-backlog CSAT recovery trends across chat and bot channels following the Ontario returns stabilization.

---

### [2026-04-15T18:05:11Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1589904911204`  
**Bytes Processed:** 8.3 GB  
**Query Text:**
```sql
-- Pipeline partition health check for fulfillment speed daily base tables
SELECT 
    table_name,
    partition_id,
    total_rows,
    total_bytes,
    last_modified_time
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name IN ('fact_promise_vs_actual', 'fulfillment_speed_daily')
ORDER BY last_modified_time DESC;
```
*Analyst Note:* Routine evening partition expiration verification for the Speed data mart airflows. All nodes updated successfully.

---

### [2026-04-15T18:30:45Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1589906445881`  
**Bytes Processed:** 14.2 GB  
**Query Text:**
```sql
-- Quick check on fulfillment node opening dates for regional delivery cost modeling
SELECT 
    node_id,
    node_type,
    node_name,
    market,
    opened_date
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE is_active = TRUE AND node_type IN ('dc', 'fc')
ORDER BY opened_date;
```
*Analyst Note:* Verifying distribution center active status for the regional logistics cost model update.

---

### [2026-04-15T19:02:19Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1589908339120`  
**Bytes Processed:** 5.1 GB  
**Query Text:**
```sql
-- Checking experiment dim metadata row counts and active states
SELECT 
    status,
    COUNT(*) AS experiment_count
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment`
GROUP BY 1;
```
*Analyst Note:* Sanity check after the weekly dimension sync from the experimentation platform.

---

### [2026-04-15T19:45:00Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1589910300455`  
**Bytes Processed:** 67.9 GB  
**Query Text:**
```sql
-- Daily care contact sub-program volume and deflection breakdown
SELECT 
    sub_program,
    channel,
    COUNT(*) AS total_contacts,
    ROUND(AVG(CAST(deflected AS INT64)) * 100, 2) AS deflection_pct,
    ROUND(AVG(csat_score), 2) AS avg_csat
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at >= '2026-04-01'
GROUP BY 1, 2
ORDER BY total_contacts DESC;
```
*Analyst Note:* Running the mid-month care telemetry audit following the rollout of the relaxed bot handoff thresholds in non-billing categories.

---

### [2026-04-15T20:12:33Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1589911953112`  
**Bytes Processed:** 19.4 GB  
**Query Text:**
```sql
-- Membership plan distribution across active panel
SELECT 
    plan_type,
    home_market,
    COUNT(*) AS member_count,
    ROUND(AVG(plan_price_usd), 2) AS avg_price
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
WHERE status = 'active'
GROUP BY 1, 2
ORDER BY member_count DESC;
```
*Analyst Note:* Pulling membership tier splits for the executive dashboard's Acme+ penetration summary.

---

### [2026-04-15T21:00:04Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1589914804329`  
**Bytes Processed:** 3.2 GB  
**Query Text:**
```sql
-- Table schema check for marketing calendar actual vs planned spend
SELECT 
    column_name,
    data_type
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'dim_marketing_calendar';
```
*Analyst Note:* Validating column types ahead of the Q1 budget reconciliation script execution.

---

### [2026-04-15T21:30:15Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1589916615789`  
**Bytes Processed:** 89.6 GB  
**Query Text:**
```sql
-- Cross-market traffic and conversion aggregate validation
SELECT 
    market,
    sessions_definition_version,
    SUM(sessions) AS total_sessions,
    SUM(orders) AS total_orders,
    ROUND(SUM(gmv_usd), 2) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date BETWEEN '2026-03-01' AND '2026-03-31'
GROUP BY 1, 2
ORDER BY market;
```
*Analyst Note:* Validating March traffic numbers following the session definition version bump to ensure post-cutover aggregates reconcile cleanly across US, CA, and MX markets.

---

### [2026-04-15T22:15:10Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1589920148332`  
**Bytes Processed:** 1.4 GB  
**Query Text:**
```sql
-- Partition check for warehouse metrics tables
SELECT 
    table_name,
    partition_id,
    total_rows,
    total_logical_bytes
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name IN ('fact_traffic_daily', 'fact_orders', 'fact_care_contacts')
ORDER BY table_name;
```
*Analyst Note:* Routine night-shift partition health check across the core daily volume tables.

---

### [2026-04-15T22:45:00Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1589921900412`  
**Bytes Processed:** 14.8 GB  
**Query Text:**
```sql
-- Preliminary monthly revenue rollup check for April MBR prep
SELECT 
    vertical_code,
    SUM(gmv_usd) AS mtd_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date BETWEEN '2026-04-01' AND '2026-04-14'
GROUP BY 1
ORDER BY mtd_gmv DESC;
```
*Analyst Note:* Pulling early April conversion-channel totals for the recurring monthly finance packet draft.

---

### [2026-04-15T23:10:45Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1589923445910`  
**Bytes Processed:** 76.3 GB  
**Query Text:**
```sql
-- Device distribution sanity check across US conversion traffic
SELECT 
    device,
    SUM(sessions) AS total_sessions,
    ROUND(SUM(gmv_usd) / NULLIF(SUM(orders), 0), 2) AS calculated_aov
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE market = 'US'
  AND date >= '2026-02-01'
GROUP BY 1
ORDER BY total_sessions DESC;
```
*Analyst Note:* Verifying device-level split trends following the March session definition bump and the concurrent mobile navigation rollout.

---

### [2026-04-15T23:55:12Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1589926112004`  
**Bytes Processed:** 8.5 GB  
**Query Text:**
```sql
-- Care contact volume by sub_program and channel
SELECT 
    sub_program,
    channel,
    COUNT(*) AS total_contacts,
    ROUND(AVG(csat_score), 2) AS avg_csat
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at >= '2026-04-01'
GROUP BY 1, 2
ORDER BY total_contacts DESC;
```
*Analyst Note:* Running the mid-month care telemetry audit following the rollout of the relaxed bot handoff thresholds in non-billing categories.

---

### [2026-04-16T00:30:20Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1589928220111`  
**Bytes Processed:** 4.1 GB  
**Query Text:**
```sql
-- Checking marketing calendar planned vs actual table shape
SELECT 
    event_id,
    event_name,
    event_type,
    planned_spend_usd,
    actual_spend_usd
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
WHERE start_date BETWEEN '2026-03-01' AND '2026-03-31'
LIMIT 10;
```
*Analyst Note:* Validating campaign spend records for March marketing reconciliation script.

---

### [2026-04-16T01:15:05Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1589930105448`  
**Bytes Processed:** 22.7 GB  
**Query Text:**
```sql
-- Marketplace category GMV aggregate check
SELECT 
    sub_vertical_code,
    SUM(gmv_usd) AS total_gmv,
    SUM(orders) AS total_orders
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE fiscal_week_ending >= '2026-03-01'
GROUP BY 1
ORDER BY total_gmv DESC;
```
*Analyst Note:* Checking marketplace sub-vertical performance to reconcile Resold acceleration against Style numbers for the weekly leadership packet.

---

### [2026-04-16T02:00:18Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1589932818902`  
**Bytes Processed:** 112.4 GB  
**Query Text:**
```sql
-- Full population traffic and conversion aggregate audit by version
SELECT 
    sessions_definition_version,
    market,
    COUNT(*) AS row_count,
    SUM(sessions) AS sum_sessions,
    SUM(orders) AS sum_orders
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date BETWEEN '2026-02-15' AND '2026-03-15'
GROUP BY 1, 2
ORDER BY sessions_definition_version, market;
```
*Analyst Note:* Auditing pre- and post-cutover session definition records around the March 2 bot filtering release.

---

### [2026-04-16T03:14:50Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1589937290551`  
**Bytes Processed:** 2.6 GB  
**Query Text:**
```sql
-- Checking dim_seller panel row counts and application date population
SELECT 
    category_focus,
    COUNT(*) AS total_sellers,
    COUNT(application_date) AS sellers_with_app_date
FROM `nexus-analyst-demo.acme_ecomm.dim_seller`
GROUP BY 1;
```
*Analyst Note:* Validating seller panel schema updates following the addition of the new-seller onboarding funnel column.

---

### [2026-04-16T04:22:11Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1589941331009`  
**Bytes Processed:** 45.8 GB  
**Query Text:**
```sql
-- Buyer VOC survey response theme distribution check
SELECT 
    theme_tag,
    COUNT(*) AS response_count,
    ROUND(AVG(score), 2) AS avg_score
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE responded_at >= '2026-03-01'
  AND sentiment = 'negative'
GROUP BY 1
ORDER BY response_count DESC;
```
*Analyst Note:* Pulling negative verbatim themes for the post-care and post-purchase Medallia feed audit.

---

### [2026-04-16T05:00:44Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1589943644120`  
**Bytes Processed:** 18.9 GB  
**Query Text:**
```sql
-- Member plan distribution check across active panel
SELECT 
    plan_type,
    acquisition_channel,
    COUNT(*) AS member_count,
    ROUND(AVG(plan_price_usd), 2) AS avg_price
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
WHERE status = 'active'
GROUP BY 1, 2
ORDER BY member_count DESC;
```
*Analyst Note:* Re-running member plan splits for executive dash reporting ahead of the Thursday morning sync.

---

### [2026-04-16T06:12:30Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1589950112340`  
**Bytes Processed:** 12.4 GB  
**Query Text:**
```sql
-- Checking partition sizes for fact_traffic_daily around the March bot cutoff
SELECT 
    date,
    sessions_definition_version,
    COUNT(*) AS partition_rows,
    SUM(sessions) AS total_sessions
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date BETWEEN '2026-02-25' AND '2026-03-05'
GROUP BY 1, 2
ORDER BY date;
```
*Analyst Note:* Spot-checking partition row counts in BigQuery following the scheduled weekly cluster optimization job.

---

### [2026-04-16T08:45:10Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1589959102911`  
**Bytes Processed:** 8.2 GB  
**Query Text:**
```sql
-- Quick check on active member plan distribution for executive MBR prep
SELECT 
    plan_type,
    status,
    COUNT(*) AS cnt
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
GROUP BY 1, 2;
```
*Analyst Note:* Running baseline distribution counts for the monthly executive deck annex.

---

### [2026-04-16T09:30:15Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1589962215088`  
**Bytes Processed:** 64.1 GB  
**Query Text:**
```sql
-- Investigating care contact volume trends by channel and sub_program
SELECT 
    SUBSTR(CAST(opened_at AS STRING), 1, 7) AS month_str,
    sub_program,
    channel,
    COUNT(*) AS contact_count,
    ROUND(AVG(handle_time_minutes), 2) AS avg_handle_time
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at >= '2026-01-01'
GROUP BY 1, 2, 3
ORDER BY month_str DESC, contact_count DESC;
```
*Analyst Note:* Pulling preliminary Q1 care contact metrics for the monthly operations review.

---

### [2026-04-16T10:15:44Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1589964944102`  
**Bytes Processed:** 3.1 GB  
**Query Text:**
```sql
-- Validating dim_associate active flags and team alignments
SELECT 
    team,
    role,
    COUNT(*) AS headcount
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
WHERE is_active = TRUE
GROUP BY 1, 2
ORDER BY headcount DESC;
```
*Analyst Note:* Routine audit of internal directory table rows against current HR roster exports.

---

### [2026-04-16T11:05:22Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1589967922519`  
**Bytes Processed:** 24.5 GB  
**Query Text:**
```sql
-- Aggregating quarterly GMV by market from traffic and conversion summary
SELECT 
    market,
    SUM(gmv_usd) AS total_gmv,
    SUM(orders) AS total_orders
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE fiscal_week_ending >= '2026-02-01'
GROUP BY 1;
```
*Analyst Note:* Re-verifying Q1 financial aggregates for the quarterly variance report.

---

### [2026-04-16T13:40:09Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1589977209334`  
**Bytes Processed:** 15.6 GB  
**Query Text:**
```sql
-- Checking survey response counts across buyer VOC channels
SELECT 
    survey_type,
    sentiment,
    COUNT(*) AS responses
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE responded_at >= '2026-02-01'
GROUP BY 1, 2;
```
*Analyst Note:* Verifying Medallia survey ingestion completeness for the post-purchase feed.

---

### [2026-04-16T14:20:55Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1589979655812`  
**Bytes Processed:** 5.4 GB  
**Query Text:**
```sql
-- Checking fulfillment node active counts by type and market
SELECT 
    node_type,
    market,
    COUNT(*) AS node_count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE is_active = TRUE
GROUP BY 1, 2;
```
*Analyst Note:* Confirming warehouse node dimension updates prior to the monthly logistics report run.

---

### [2026-04-16T15:05:30Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1589982330491`  
**Bytes Processed:** 41.2 GB  
**Query Text:**
```sql
-- Marketplace GMV summary audit by sub_vertical
SELECT 
    sub_vertical_code,
    SUM(gmv_usd) AS q1_gmv,
    SUM(orders) AS q1_orders
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE fiscal_week_ending BETWEEN '2026-02-01' AND '2026-04-15'
GROUP BY 1;
```
*Analyst Note:* Compiling marketplace sub-vertical performance numbers for the SVP review pack.

---

### [2026-04-16T16:11:04Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1589986264023`  
**Bytes Processed:** 19.8 GB  
**Query Text:**
```sql
-- Care deflection daily metrics rollup check
SELECT 
    sub_program,
    SUM(contact_volume) AS total_volume,
    ROUND(AVG(deflection_rate), 3) AS avg_deflection
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
GROUP BY 1;
```
*Analyst Note:* Checking weekly care deflection rates following recent chatbot updates.

---

### [2026-04-16T17:00:19Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1589989219045`  
**Bytes Processed:** 1.2 GB  
**Query Text:**
```sql
-- Checking dim_marketing_calendar event types and owners
SELECT 
    event_type,
    COUNT(*) AS event_count
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
GROUP BY 1;
```
*Analyst Note:* Routine schema check on marketing calendar table metadata.

---

### [2026-04-16T17:45:10Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1589991204819`  
**Bytes Processed:** 88.4 GB  
**Query Text:**
```sql
-- Monthly partition size audit across base fact tables
SELECT 
    table_name,
    partition_id,
    total_rows,
    total_bytes
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name IN ('fact_traffic_daily', 'fact_orders', 'fact_care_contacts', 'fact_promise_vs_actual')
ORDER BY table_name, partition_id DESC;
```
*Analyst Note:* Routine partition hygiene check before the scheduled weekend ETL maintenance window.

---

### [2026-04-16T18:12:33Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1589992953112`  
**Bytes Processed:** 14.1 GB  
**Query Text:**
```sql
-- Checking net ads and renewal rates by plan type for Acme+
SELECT 
    plan_type,
    status,
    COUNT(*) AS member_count,
    ROUND(AVG(plan_price_usd), 2) AS avg_price
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
GROUP BY 1, 2;
```
*Analyst Note:* Pulling plan-type distributions for the membership finance sync.

---

### [2026-04-16T19:30:00Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1589997800234`  
**Bytes Processed:** 3.6 GB  
**Query Text:**
```sql
-- Validating fulfillment node active flags against store formats
SELECT 
    store_format,
    COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE node_type = 'store'
GROUP BY 1;
```
*Analyst Note:* Checking store format attributes following yesterday's node dimension metadata patch.

---

### [2026-04-17T08:15:22Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1590045322819`  
**Bytes Processed:** 62.9 GB  
**Query Text:**
```sql
-- Daily care contact distribution by sub_program and channel
SELECT 
    sub_program,
    channel,
    COUNT(*) AS contact_rows
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at >= TIMESTAMP('2026-02-01')
GROUP BY 1, 2
ORDER BY contact_rows DESC;
```
*Analyst Note:* Auditing care channel volumes for the post-bot rollout review pack.

---

### [2026-04-17T09:02:45Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1590048165302`  
**Bytes Processed:** 105.7 GB  
**Query Text:**
```sql
-- Cross-market traffic and conversion aggregate audit
SELECT 
    market,
    sessions_definition_version,
    SUM(sessions) AS total_sessions,
    SUM(orders) AS total_orders,
    ROUND(SUM(gmv_usd), 2) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date BETWEEN '2026-02-01' AND '2026-04-15'
GROUP BY 1, 2;
```
*Analyst Note:* Reconciling Q1 conversion-channel totals across US, CA, and MX markets for the finance deck.

---

### [2026-04-17T10:20:11Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1590052811490`  
**Bytes Processed:** 24.3 GB  
**Query Text:**
```sql
-- Checking experiment readouts for active conversion experiments
SELECT 
    experiment_id,
    variant,
    metric_name,
    metric_value,
    lift_vs_control_pct,
    is_significant
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`
WHERE as_of_date = '2026-03-30'
  AND metric_name LIKE '%conversion%';
```
*Analyst Note:* Pulling final metric readouts for Checkout Simplify wrap-up checks.

---

### [2026-04-17T11:05:50Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1590055550123`  
**Bytes Processed:** 8.1 GB  
**Query Text:**
```sql
-- Listing active fulfillment nodes by market
SELECT 
    market,
    node_type,
    COUNT(*) AS active_nodes
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE is_active = TRUE
GROUP BY 1, 2
ORDER BY 1, 2;
```
*Analyst Note:* Routine warehouse node verification for the logistics dashboard feed.

---

### [2026-04-17T13:40:19Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1590064819034`  
**Bytes Processed:** 31.5 GB  
**Query Text:**
```sql
-- Sampling buyer VOC verbatims by sentiment and theme tag
SELECT 
    survey_type,
    sentiment,
    theme_tag,
    COUNT(*) AS response_count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE responded_at >= TIMESTAMP('2026-03-01')
GROUP BY 1, 2, 3
ORDER BY response_count DESC
LIMIT 25;
```
*Analyst Note:* Checking post-purchase survey theme distributions after the March session cutover.

---

### [2026-04-17T14:22:08Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1590067328451`  
**Bytes Processed:** 19.4 GB  
**Query Text:**
```sql
-- Verifying marketplace gmv summary join keys against listings
SELECT 
    t1.sub_vertical_code,
    SUM(t1.gmv_usd) AS mart_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary` t1
WHERE t1.fiscal_week_ending BETWEEN '2026-02-01' AND '2026-04-15'
GROUP BY 1;
```
*Analyst Note:* Cross-checking marketplace summary totals against sub-vertical filters.

---

### [2026-04-17T15:10:04Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1590070204118`  
**Bytes Processed:** 2.4 GB  
**Query Text:**
```sql
-- Checking dim_associate active records by role
SELECT 
    role,
    team,
    COUNT(*) AS headcount
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
WHERE is_active = TRUE
GROUP BY 1, 2
ORDER BY headcount DESC;
```
*Analyst Note:* Verifying internal data/product org dimensions for the warehouse metadata audit.

---

### [2026-04-17T16:05:40Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1590073540892`  
**Bytes Processed:** 45.8 GB  
**Query Text:**
```sql
-- Daily traffic conversion summary check across version cutover
SELECT 
    sessions_definition_version,
    COUNT(*) AS row_count,
    SUM(sessions) AS total_sessions,
    SUM(orders) AS total_orders
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
GROUP BY 1;
```
*Analyst Note:* Verifying that both session definition versions are correctly preserved in the derived mart.

---

### [2026-04-17T17:15:30Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1590077730221`  
**Bytes Processed:** 16.7 GB  
**Query Text:**
```sql
-- Checking care deflection daily averages for CSAT scores
SELECT 
    sub_program,
    ROUND(AVG(avg_csat_deflected), 2) AS mean_deflected_csat,
    ROUND(AVG(avg_csat_agent_assisted), 2) AS mean_agent_csat
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
GROUP BY 1;
```
*Analyst Note:* Pulling deflected vs. agent-assisted CSAT benchmarks following recent bot updates.

---

---

### [2026-04-17T18:30:12Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1590082912403`  
**Bytes Processed:** 8.1 GB  
**Query Text:**
```sql
-- Checking partition sizes for raw order line items
SELECT 
    DATE(order_date) AS ord_date,
    COUNT(*) AS row_count,
    COUNT(DISTINCT order_id) AS distinct_orders
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE order_date >= '2026-03-01'
GROUP BY 1
ORDER BY ord_date DESC;
```
*Analyst Note:* Spot-check on partition distribution following the recent BigQuery storage maintenance window.

---

### [2026-04-17T19:02:44Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1590085364119`  
**Bytes Processed:** 12.3 GB  
**Query Text:**
```sql
-- Validating fulfillment node status counts
SELECT 
    node_type,
    market,
    COUNT(*) AS node_count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE is_active = TRUE
GROUP BY 1, 2;
```
*Analyst Note:* Quick audit for the logistics database schema update supporting new sortation centers.

---

### [2026-04-17T20:11:15Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1590089475882`  
**Bytes Processed:** 34.5 GB  
**Query Text:**
```sql
-- Monthly membership event breakdown by signup channel
SELECT 
    channel,
    event_type,
    COUNT(*) AS event_count
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
WHERE event_date BETWEEN '2026-02-01' AND '2026-03-31'
GROUP BY 1, 2;
```
*Analyst Note:* Pulling channel attribution numbers for the Q1 executive finance packet.

---

### [2026-04-17T21:40:08Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1590094808331`  
**Bytes Processed:** 9.6 GB  
**Query Text:**
```sql
-- Reviewing survey response sentiment splits for post-purchase VOC
SELECT 
    sentiment,
    COUNT(*) AS response_count,
    ROUND(AVG(score), 2) AS mean_score
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE survey_type = 'post_purchase'
  AND responded_at >= '2026-03-01'
GROUP BY 1;
```
*Analyst Note:* Checking customer sentiment distribution on Medallia responses following the March navigation redesign.

---

### [2026-04-17T22:05:33Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1590096333019`  
**Bytes Processed:** 1.2 GB  
**Query Text:**
```sql
-- Verifying dim_vertical taxonomy integrity
SELECT 
    vertical_code,
    vertical_name,
    COUNT(sub_vertical_code) AS sub_vertical_count
FROM `nexus-analyst-demo.acme_ecomm.dim_vertical`
GROUP BY 1, 2
ORDER BY vertical_code;
```
*Analyst Note:* Automated pipeline health check on vertical mappings.

---

### [2026-04-18T08:14:20Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1590135260447`  
**Bytes Processed:** 67.2 GB  
**Query Text:**
```sql
-- Cross-market traffic conversion summary check for Q1
SELECT 
    market,
    sessions_definition_version,
    SUM(sessions) AS total_sessions,
    SUM(orders) AS total_orders,
    ROUND(AVG(conversion_rate), 4) AS avg_conversion_rate
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE fiscal_week_ending BETWEEN '2026-02-01' AND '2026-03-31'
GROUP BY 1, 2;
```
*Analyst Note:* Re-running pre/post session definition audit across US, CA, and MX prior to publishing the final weekly mart snapshot.

---

### [2026-04-18T09:30:11Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1590139811205`  
**Bytes Processed:** 18.4 GB  
**Query Text:**
```sql
-- Marketplace GMV summary by sub-vertical for trailing weeks
SELECT 
    sub_vertical_code,
    SUM(gmv_usd) AS weekly_gmv,
    SUM(orders) AS weekly_orders
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE fiscal_week_ending >= '2026-03-01'
GROUP BY 1;
```
*Analyst Note:* Pulling preliminary Marketplace figures for the weekly revenue check-in.

---

### [2026-04-18T10:15:45Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1590142545890`  
**Bytes Processed:** 5.3 GB  
**Query Text:**
```sql
-- Checking active experiment records in dim_experiment
SELECT 
    vertical_code,
    status,
    COUNT(*) AS experiment_count
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment`
GROUP BY 1, 2;
```
*Analyst Note:* Validating experiment metadata table refresh after the recent Aitable sync.

---

### [2026-04-18T11:02:18Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1590145338102`  
**Bytes Processed:** 28.9 GB  
**Query Text:**
```sql
-- Analyzing care contact sub-programs and deflection rates
SELECT 
    sub_program,
    channel,
    COUNT(*) AS total_contacts,
    ROUND(AVG(CAST(deflected AS INT64)) * 100, 2) AS deflection_pct
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily` t1
CROSS JOIN UNNEST([struct(TRUE as deflected)]) -- placeholder structural join for testing
GROUP BY 1, 2;
```
*Analyst Note:* Testing query structure for the upcoming bot deflection reliability audit.

---

### [2026-04-18T13:20:50Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1590153650774`  
**Bytes Processed:** 112.4 GB  
**Query Text:**
```sql
-- Daily traffic conversion audit across device types
SELECT 
    device,
    sessions_definition_version,
    SUM(sessions) AS sessions,
    SUM(orders) AS orders,
    SAFE_DIVIDE(SUM(orders), SUM(sessions)) AS calc_conversion
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date BETWEEN '2026-02-01' AND '2026-04-15'
GROUP BY 1, 2;
```
*Analyst Note:* Verifying device-level aggregation behavior following the bot-filtering update.

---

### [2026-04-18T14:45:10Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1590158710332`  
**Bytes Processed:** 7.8 GB  
**Query Text:**
```sql
-- Membership tier and plan price distribution in panel
SELECT 
    plan_type,
    plan_price_usd,
    COUNT(*) AS member_count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
WHERE status = 'active'
GROUP BY 1, 2;
```
*Analyst Note:* Checking panel membership pricing distribution for annual renewal forecasting.

---

### [2026-04-18T15:33:04Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1590161584209`  
**Bytes Processed:** 3.1 GB  
**Query Text:**
```sql
-- Marketing calendar event count by type
SELECT 
    event_type,
    COUNT(*) AS event_count,
    SUM(actual_spend_usd) AS total_actual_spend
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
GROUP BY 1;
```
*Analyst Note:* Audit of marketing calendar spend fields for Q1 reconciliation.

---

### [2026-04-18T16:12:55Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1590163975118`  
**Bytes Processed:** 14.2 GB  
**Query Text:**
```sql
-- Care contact resolution codes by channel
SELECT 
    channel,
    resolution_code,
    COUNT(*) AS resolution_count
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at >= '2026-04-01'
GROUP BY 1, 2
ORDER BY resolution_count DESC;
```
*Analyst Note:* Reviewing top care resolution categories for the monthly support review.

---

### [2026-04-19T09:04:11Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1590224851226`  
**Bytes Processed:** 44.1 GB  
**Query Text:**
```sql
-- Fulfillment speed daily on-time rates by fulfillment type
SELECT 
    fulfillment_type,
    SUM(orders_promised) AS total_promised,
    SUM(orders_on_time) AS total_on_time,
    ROUND(SAFE_DIVIDE(SUM(orders_on_time), SUM(orders_promised)) * 100, 2) AS blended_on_time_pct
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE date BETWEEN '2026-02-01' AND '2026-03-31'
GROUP BY 1;
```
*Analyst Note:* Reconciling fulfillment speed aggregates against the published Speed mart.

---

### [2026-04-19T10:22:30Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1590229350419`  
**Bytes Processed:** 9.2 GB  
**Query Text:**
```sql
-- Marketplace seller category distribution check
SELECT 
    category_focus,
    status,
    COUNT(*) AS seller_count
FROM `nexus-analyst-demo.acme_ecomm.dim_seller`
GROUP BY 1, 2;
```
*Analyst Note:* Verifying seller panel stratification across Collectibles, Resold, and Style.

---

### [2026-04-19T11:15:02Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1590232502881`  
**Bytes Processed:** 2.6 GB  
**Query Text:**
```sql
-- Checking date dimension peak holiday flags
SELECT 
    is_peak_holiday,
    COUNT(*) AS day_count
FROM `nexus-analyst-demo.acme_ecomm.dim_date`
GROUP BY 1;
```
*Analyst Note:* Routine sanity check on fiscal calendar table ranges through 2026-04-15.

---

### [2026-04-19T13:40:19Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1590241219405`  
**Bytes Processed:** 88.5 GB  
**Query Text:**
```sql
-- Experiment readouts lift check for Checkout Simplify
SELECT 
    metric_name,
    variant,
    AVG(metric_value) AS avg_metric_val,
    AVG(lift_vs_control_pct) AS avg_lift
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`
WHERE experiment_id = 'exp_2214'
GROUP BY 1, 2;
```
*Analyst Note:* Pulling readout summary metrics for Owen Faust's checkout experiment post-mortem review.

---

### [2026-04-19T14:55:40Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1590245740112`  
**Bytes Processed:** 19.3 GB  
**Query Text:**
```sql
-- Examining buyer VOC survey types and score distributions
SELECT 
    survey_type,
    score_type,
    COUNT(*) AS response_count,
    ROUND(AVG(score), 2) AS mean_score
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
GROUP BY 1, 2;
```
*Analyst Note:* Quality check on Medallia response data prior to building the Q1 VOC summary dashboard.

---

### [2026-04-19T16:10:22Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1590250222394`  
**Bytes Processed:** 31.0 GB  
**Query Text:**
```sql
-- Member CLTV panel distribution check
SELECT 
    signup_cohort_quarter,
    COUNT(*) AS member_count,
    ROUND(AVG(projected_cltv_usd), 2) AS mean_projected_cltv
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`
GROUP BY 1
ORDER BY signup_cohort_quarter;
```
*Analyst Note:* Auditing cohort-level CLTV figures across membership tiers.

---

### [2026-04-20T08:30:15Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1590311415092`  
**Bytes Processed:** 4.1 GB  
**Query Text:**
```sql
-- Checking marketplace seller performance metrics table schema
SELECT 
    category_focus,
    ROUND(AVG(trailing_90d_gmv_usd), 2) AS avg_seller_gmv,
    ROUND(AVG(return_rate), 4) AS avg_return_rate
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
GROUP BY 1;
```
*Analyst Note:* Data engineering verification on seller performance mart refresh intervals.

---

### [2026-04-20T09:45:00Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1590315900188`  
**Bytes Processed:** 53.7 GB  
**Query Text:**
```sql
-- Fulfillment speed daily mart cost analysis
SELECT 
    fulfillment_type,
    ROUND(AVG(avg_cost_per_order_usd), 2) AS mean_cost_per_order,
    ROUND(AVG(pct_of_total_orders), 4) AS mean_mix_share
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE date >= '2026-01-01'
GROUP BY 1;
```
*Analyst Note:* Checking fulfillment cost trends across ship-to-home, pickup, and DFS channels for the supply chain review.

---

### [2026-04-20T10:20:44Z] — `camille.duarte` (assoc_100123)
**Job ID:** `bq_job_1590318044701`  
**Bytes Processed:** 1.8 GB  
**Query Text:**
```sql
-- Initial exploratory query on seller VOC responses
SELECT 
    survey_type,
    theme_tag,
    COUNT(*) AS response_count
FROM `nexus-analyst-demo.acme_ecomm.fact_seller_voc_responses`
GROUP BY 1, 2
ORDER BY response_count DESC;
```
*Analyst Note:* First look at the newly populated `fact_seller_voc_responses` table for the Seller Pulse survey program.

---

### [2026-04-20T11:15:33Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1590321333550`  
**Bytes Processed:** 15.6 GB  
**Query Text:**
```sql
-- Examining membership renewal events and benefit codes
SELECT 
    benefit_code,
    COUNT(*) AS redemption_count
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
WHERE event_type = 'benefit_redeemed'
GROUP BY 1;
```
*Analyst Note:* Pulling benefit redemption counts for the membership team's quarterly review.

---

### [2026-04-20T13:05:12Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1590327912041`  
**Bytes Processed:** 22.4 GB  
**Query Text:**
```sql
-- Care deflection daily summary by sub-program
SELECT 
    sub_program,
    SUM(contact_volume) AS total_contacts,
    ROUND(AVG(deflection_rate), 4) AS mean_deflection_rate
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
GROUP BY 1;
```
*Analyst Note:* Summarizing care deflection performance across avoid, automate, optimize, and platform sub-programs.

---

### [2026-04-20T14:30:50Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1590333050912`  
**Bytes Processed:** 39.8 GB  
**Query Text:**
```sql
-- Checking experiment exposure totals for Wider Promise Window
SELECT 
    experiment_id,
    variant,
    SUM(units_assigned) AS assigned,
    SUM(units_exposed) AS exposed
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures`
WHERE experiment_id = 'exp_1187'
GROUP BY 1, 2;
```
*Analyst Note:* Verifying exposure counts and assigned-vs-exposed differentials for the promise window experiment audit.

---

### [2026-04-20T15:40:18Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1590337218335`  
**Bytes Processed:** 5.0 GB  
**Query Text:**
```sql
-- Validating dim_associate active records count by team
SELECT 
    team,
    COUNT(*) AS member_count
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
WHERE is_active = TRUE
GROUP BY 1;
```
*Analyst Note:* Routine department headcount verification for the warehouse metadata audit.

---

### [2026-04-21T09:12:04Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1590397924102`  
**Bytes Processed:** 62.3 GB  
**Query Text:**
```sql
-- Marketplace GMV summary totals by fiscal week
SELECT 
    fiscal_week_ending,
    SUM(gmv_usd) AS weekly_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE fiscal_week_ending BETWEEN '2026-02-01' AND '2026-03-31'
GROUP BY 1
ORDER BY fiscal_week_ending;
```
*Analyst Note:* Running weekly trend checks on Marketplace GMV for the executive dashboard update.

---

### [2026-04-10T11:05:42Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1590412042183`  
**Bytes Processed:** 1.8 GB  
**Query Text:**
```sql
-- Checking partition sizes for fact_traffic_daily
SELECT 
    table_name,
    size_bytes,
    row_count
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'fact_traffic_daily';
```
*Analyst Note:* Storage audit on traffic facts following the March 2 session definition migration.

---

### [2026-04-10T13:40:19Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1590421619044`  
**Bytes Processed:** 45.2 GB  
**Query Text:**
```sql
-- MBR cross-vertical GMV summary
SELECT 
    vertical_code,
    SUM(gmv_usd) AS qtd_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date BETWEEN '2026-02-01' AND '2026-03-31'
GROUP BY 1;
```
*Analyst Note:* Pulling Q1 close figures for the executive monthly financial review package.

---

### [2026-04-11T08:22:15Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1590481335019`  
**Bytes Processed:** 12.4 GB  
**Query Text:**
```sql
-- Validating active membership counts against panel
SELECT 
    plan_type,
    status,
    COUNT(*) AS member_count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
GROUP BY 1, 2;
```
*Analyst Note:* Routine health check on the dim_member sample distribution across annual and monthly tiers.

---

### [2026-04-11T10:15:33Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1590488133291`  
**Bytes Processed:** 8.9 GB  
**Query Text:**
```sql
-- Care contact volume by channel and sub-program
SELECT 
    sub_program,
    channel,
    COUNT(*) AS contact_count
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at >= '2026-03-01'
GROUP BY 1, 2;
```
*Analyst Note:* Auditing post-bot distribution for the customer care weekly operating report.

---

### [2026-04-11T14:50:02Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1590504602881`  
**Bytes Processed:** 3.1 GB  
**Query Text:**
```sql
-- Checking node metadata table refresh status
SELECT 
    node_type,
    COUNT(*) AS node_count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE is_active = TRUE
GROUP BY 1;
```
*Analyst Note:* Verifying distribution and fulfillment center node counts prior to the weekly logistics ETL run.

---

### [2026-04-12T09:11:40Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1590561100412`  
**Bytes Processed:** 28.7 GB  
**Query Text:**
```sql
-- Marketplace take rate summary by sub-vertical
SELECT 
    sub_vertical_code,
    SUM(gmv_usd) AS total_gmv,
    SUM(gmv_usd * take_rate) AS calculated_revenue
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE fiscal_week_ending >= '2026-02-01'
GROUP BY 1;
```
*Analyst Note:* Finance audit check on Marketplace fee accruals for Style, Resold, and Collectibles.

---

### [2026-04-12T11:30:25Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1590569425890`  
**Bytes Processed:** 54.1 GB  
**Query Text:**
```sql
-- Device-level conversion check post-session definition change
SELECT 
    device,
    sessions_definition_version,
    SUM(sessions) AS total_sessions,
    SUM(orders) AS total_orders,
    ROUND(SUM(orders) / NULLIF(SUM(sessions), 0), 4) AS conversion_rate
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date BETWEEN '2026-02-15' AND '2026-03-15'
GROUP BY 1, 2;
```
*Analyst Note:* Running comparative conversion checks across the March 2 session definition cutover boundary.

---

### [2026-04-13T08:05:12Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1590633912345`  
**Bytes Processed:** 4.2 GB  
**Query Text:**
```sql
-- Checking experiment dim table active records
SELECT 
    vertical_code,
    status,
    COUNT(*) AS exp_count
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment`
GROUP BY 1, 2;
```
*Analyst Note:* Pipeline metadata check for running experiment entries in BigQuery.

---

### [2026-04-13T10:20:44Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1590642044102`  
**Bytes Processed:** 19.5 GB  
**Query Text:**
```sql
-- Membership renewal rate check by plan type
SELECT 
    plan_type,
    COUNT(*) AS total_members
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
WHERE status = 'active'
GROUP BY 1;
```
*Analyst Note:* Verifying active Acme+ member distribution between monthly and annual plans for the executive dash.

---

### [2026-04-13T14:15:50Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1590656150781`  
**Bytes Processed:** 71.8 GB  
**Query Text:**
```sql
-- Marketplace listing status distribution
SELECT 
    category,
    status,
    COUNT(*) AS listing_count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY 1, 2;
```
*Analyst Note:* Auditing listing table panel distribution for Marketplace analytics reporting.

---

### [2026-04-14T09:02:18Z] — `giulia.romano` (assoc_100213)
**Job ID:** `bq_job_1590714138290`  
**Bytes Processed:** 16.3 GB  
**Query Text:**
```sql
-- Buyer VOC sentiment breakdown by theme
SELECT 
    theme_tag,
    sentiment,
    COUNT(*) AS response_count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE responded_at >= '2026-03-01'
GROUP BY 1, 2
ORDER BY response_count DESC;
```
*Analyst Note:* Weekly review of Medallia verbatim theme distribution following the Ontario returns backlog clearance.

---

### [2026-04-14T11:45:09Z] — `connor.blake` (assoc_100212)
**Job ID:** `bq_job_1590723909551`  
**Bytes Processed:** 6.7 GB  
**Query Text:**
```sql
-- Checking marketing calendar table row counts by event type
SELECT 
    event_type,
    COUNT(*) AS event_count
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
GROUP BY 1;
```
*Analyst Note:* Verification query for the marketing calendar dimension table load.

---

### [2026-04-14T15:30:22Z] — `amara.shah` (assoc_100211)
**Job ID:** `bq_job_1590737422119`  
**Bytes Processed:** 33.4 GB  
**Query Text:**
```sql
-- Fulfillment speed daily on-time summary by fulfillment type
SELECT 
    fulfillment_type,
    ROUND(AVG(on_time_rate), 4) AS mean_on_time_rate
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE date >= '2026-02-01'
GROUP BY 1;
```
*Analyst Note:* Compiling quarterly fulfillment speed metrics for the Q1 review deck.

---

### [2026-04-15T08:12:01Z] — `wei.hartono` (assoc_100210)
**Job ID:** `bq_job_1590797521083`  
**Bytes Processed:** 48.6 GB  
**Query Text:**
```sql
-- Checking traffic conversion summary for US market Q1
SELECT 
    fiscal_week_ending,
    sessions,
    orders,
    conversion_rate
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'US'
  AND fiscal_week_ending BETWEEN '2026-02-01' AND '2026-03-31'
ORDER BY fiscal_week_ending;
```
*Analyst Note:* Finalizing weekly conversion trends for the Q1 board package appendices.

---

### [2026-04-15T10:25:40Z] — `camille.duarte` (assoc_100123)
**Job ID:** `bq_job_1590805540321`  
**Bytes Processed:** 8.1 GB  
**Query Text:**
```sql
-- Initial Seller Pulse survey response check
SELECT 
    survey_type,
    score_type,
    COUNT(*) AS response_count,
    ROUND(AVG(score), 2) AS mean_score
FROM `nexus-analyst-demo.acme_ecomm.fact_seller_voc_responses`
GROUP BY 1, 2;
```
*Analyst Note:* First exploratory query against the newly populated seller-side VOC stream following the Seller Pulse launch.