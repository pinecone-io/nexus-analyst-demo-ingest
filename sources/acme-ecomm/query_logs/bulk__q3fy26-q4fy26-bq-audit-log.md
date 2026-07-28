---
title: "BigQuery analyst query audit log — Q3FY26 & Q4FY26 peak season (2025-08 through 2026-01)"
source_url: "internal://acme-ecomm/query_logs/bulk__q3fy26-q4fy26-bq-audit-log"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-01-25T12:00:00+00:00'
adapter: bq_query_log
---

```sql
-- ============================================================================
-- SYSTEM: BigQuery Audit Log (nexus-analyst-demo.acme_ecomm)
-- SCOPE: Q3FY26 & Q4FY26 Peak Season Analysis (2025-08-01 through 2026-01-25)
-- AUTHORIZED ADAPTER: bq_query_log
-- NOTE: Flat dataset structure enforced (acme_ecomm.<table>). Do not use nested marts.
-- ============================================================================
```

### [2025-08-02 04:12:15 UTC] — User: wei.hartono (assoc_100210)
-- Routine daily partition validation for traffic and order tables.
-- Checking row counts following the late July partition adjustments.
SELECT 
    date,
    market,
    vertical_code,
    COUNT(1) as row_count,
    SUM(sessions) as total_sessions,
    SUM(orders) as total_orders
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date >= '2025-08-01' AND date <= '2025-08-02'
GROUP BY 1, 2, 3
ORDER BY date DESC;

### [2025-08-05 09:33:02 UTC] — User: lucia.ferreira (assoc_100320)
-- INVESTIGATION: Collectibles vertical traffic and listing anomalies following the viral vintage-card auction surge.
-- Note: Must remember convention 5. Absolute counts must use aggregate marts or caution with panel tables.
SELECT 
    l.category,
    COUNT(DISTINCT l.seller_id) as active_sellers,
    COUNT(l.listing_id) as total_listings,
    AVG(l.price_usd) as avg_listing_price,
    SUM(CASE WHEN l.authenticity_verified = FALSE THEN 1 ELSE 0 END) as unverified_count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings` l
WHERE l.category = 'collectibles'
GROUP BY 1;

### [2025-08-06 11:20:44 UTC] — User: sanjay.bhatt (assoc_100120)
-- Checking seller performance metrics for top Collectibles accounts (e.g. sel_500012)
SELECT 
    s.seller_id,
    s.seller_name,
    m.active_listings,
    m.trailing_90d_gmv_usd,
    m.return_rate,
    m.authenticity_flag_count
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance` m
JOIN `nexus-analyst-demo.acme_ecomm.dim_seller` s ON m.seller_id = s.seller_id
WHERE m.category_focus = 'collectibles'
ORDER BY m.trailing_90d_gmv_usd DESC
LIMIT 25;

### [2025-08-10 14:02:11 UTC] — User: connor.blake (assoc_100212)
-- Pipeline check: verifying daily ingestion lag for fact_orders during early August traffic spike.
SELECT 
    order_date,
    market,
    channel,
    COUNT(*) as order_count,
    SUM(gmv_usd) as daily_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE order_date >= '2025-08-01'
GROUP BY 1, 2, 3
ORDER BY order_date DESC
LIMIT 10;

### [2025-08-15 08:15:30 UTC] — User: giulia.romano (assoc_100213)
-- Establishing pre-launch Medallia VOC baseline for August 2025. Checking verbatim volume.
SELECT 
    DATE(responded_at) as resp_date,
    survey_type,
    theme_tag,
    COUNT(*) as verbatim_count,
    AVG(score) as avg_score
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE responded_at >= '2025-08-01' AND responded_at < '2025-09-01'
GROUP BY 1, 2, 3
ORDER BY resp_date DESC;

### [2025-08-20 16:45:00 UTC] — User: amara.shah (assoc_100211)
-- MBR prep: Cross-checking US conversion rate by device for Q2FY26 close.
SELECT 
    market,
    device,
    SUM(sessions) as sessions,
    SUM(orders) as orders,
    SAFE_DIVIDE(SUM(orders), SUM(sessions)) * 100 as conversion_pct
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date BETWEEN '2025-05-01' AND '2025-07-31'
  AND vertical_code = 'US_CONV'
GROUP BY 1, 2;

### [2025-08-25 10:11:09 UTC] — User: malik.hendon (assoc_100160)
-- B2B initial catalog review: exploring fact_orders for B2B vs commercial split.
SELECT 
    vertical_code,
    sub_vertical_code,
    COUNT(order_id) as orders,
    SUM(gmv_usd) as gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE vertical_code = 'B2B'
GROUP BY 1, 2;

### [2025-09-02 09:00:12 UTC] — User: lucia.ferreira (assoc_100320)
-- Investigating seller suspension status for Bramblewood Vintage (sel_500089).
SELECT 
    seller_id,
    seller_name,
    category_focus,
    status,
    onboarded_date
FROM `nexus-analyst-demo.acme_ecomm.dim_seller`
WHERE seller_id = 'sel_500089';

### [2025-09-09 13:22:40 UTC] — User: sanjay.bhatt (assoc_100120)
-- Pre-launch check for 'Acme Verified' partnership schema integration with GradeSure.
SELECT 
    COUNT(*) as total_collectibles,
    SUM(CASE WHEN authenticity_verified THEN 1 ELSE 0 END) as verified_count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
WHERE category = 'collectibles';

### [2025-09-16 10:05:19 UTC] — User: dominic.paquet (assoc_100310)
-- Post-launch monitoring for 'Ask Acme v2' care chatbot (launched 2025-09-15).
SELECT 
    DATE(opened_at) as contact_date,
    sub_program,
    channel,
    COUNT(*) as total_contacts,
    SUM(CASE WHEN deflected THEN 1 ELSE 0 END) as deflected_count,
    SAFE_DIVIDE(SUM(CASE WHEN deflected THEN 1 ELSE 0 END), COUNT(*)) * 100 as deflection_rate
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at >= '2025-09-15'
GROUP BY 1, 2, 3
ORDER BY contact_date DESC;

### [2025-09-22 15:44:01 UTC] — User: simone.laurent (assoc_100150)
-- Tracking 'Fall Savings' Acme+ join promo signups (camp_90214).
SELECT 
    event_type,
    channel,
    COUNT(*) as event_count
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
WHERE event_date BETWEEN '2025-09-20' AND '2025-09-30'
GROUP BY 1, 2;

### [2025-10-02 08:30:00 UTC] — User: sanjay.bhatt (assoc_100120)
-- Initializing readout query for Verified Badge Prominence experiment (exp_2401).
SELECT 
    experiment_id,
    variant,
    exposure_date,
    units_assigned,
    units_exposed,
    units_converted
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures`
WHERE experiment_id = 'exp_2401'
ORDER BY exposure_date ASC;

### [2025-10-08 12:11:55 UTC] — User: leo.brandt (assoc_100141)
-- Simulating wider delivery promise windows across fulfillment nodes.
SELECT 
    node_id,
    fulfillment_type,
    SUM(orders_promised) as total_promised,
    SUM(orders_on_time) as total_ontime,
    SAFE_DIVIDE(SUM(orders_on_time), SUM(orders_promised)) * 100 as ontim_rate
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE date >= '2025-09-01'
GROUP BY 1, 2;

### [2025-10-15 17:50:20 UTC] — User: amara.shah (assoc_100211)
-- Q3FY26 financial close data pull: Marketplace GMV summary by sub-vertical.
-- NOTE: Using full-population mart per convention 5, NOT fact_orders.
SELECT 
    fiscal_week_ending,
    sub_vertical_code,
    gmv_usd,
    orders,
    take_rate
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE fiscal_week_ending BETWEEN '2025-08-01' AND '2025-10-31'
ORDER BY fiscal_week_ending DESC;

### [2025-10-22 09:14:33 UTC] — User: wei.hartono (assoc_100210)
-- Reviewing traffic conversion summary mart for Q3FY26.
SELECT 
    fiscal_week_ending,
    market,
    vertical_code,
    sessions,
    orders,
    conversion_rate,
    gmv_usd
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE vertical_code = 'US_CONV' AND market = 'US'
ORDER BY fiscal_week_ending DESC
LIMIT 12;

### [2025-10-29 11:00:00 UTC] — User: hannah.brennan (assoc_100020)
-- Care department quarterly review: handle times and CSAT by channel.
SELECT 
    sub_program,
    channel,
    COUNT(*) as contact_count,
    AVG(csat_score) as avg_csat,
    AVG(handle_time_minutes) as avg_handle_time
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at >= '2025-08-01' AND opened_at < '2025-11-01'
GROUP BY 1, 2;

### [2025-11-03 08:22:10 UTC] — User: gabriel.stroud (assoc_100330)
-- Speed and fulfillment readiness check for Q4 peak season launch.
SELECT 
    fulfillment_type,
    SUM(orders_promised) as promised,
    SUM(orders_on_time) as on_time,
    SAFE_DIVIDE(SUM(orders_on_time), SUM(orders_promised)) * 100 as otp_rate
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE date >= '2025-10-01' AND date <= '2025-10-31'
GROUP BY 1;

### [2025-11-10 14:30:15 UTC] — User: giulia.romano (assoc_100213)
-- VOC theme distribution check heading into November.
SELECT 
    theme_tag,
    sentiment,
    COUNT(*) as response_count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE responded_at >= '2025-10-01' AND responded_at < '2025-11-01'
GROUP BY 1, 2
ORDER BY response_count DESC
LIMIT 10;

### [2025-11-16 10:00:45 UTC] — User: sanjay.bhatt (assoc_100120)
-- Final readout query for Verified Badge Prominence experiment (exp_2401).
SELECT 
    experiment_id,
    variant,
    metric_name,
    metric_value,
    lift_vs_control_pct,
    is_significant
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`
WHERE experiment_id = 'exp_2401';

### [2025-11-21 09:12:00 UTC] — User: sanjay.bhatt (assoc_100120)
-- Post-rollout verification query: confirming badge coverage on Collectibles listings.
SELECT 
    status,
    authenticity_verified,
    COUNT(*) as listing_count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
WHERE category = 'collectibles'
GROUP BY 1, 2;

### [2025-11-29 07:15:20 UTC] — User: maya.lindqvist (assoc_100110)
-- Black Friday (2025-11-28) traffic and conversion hourly check (simulated daily rollup).
SELECT 
    date,
    market,
    device,
    sessions,
    orders,
    gmv_usd
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date = '2025-11-28';

### [2025-12-02 10:44:12 UTC] — User: hannah.brennan (assoc_100020)
-- Monitoring post-Cyber Monday care volume surges and initial return queries.
SELECT 
    sub_program,
    channel,
    COUNT(*) as contacts,
    AVG(handle_time_minutes) as avg_handle_time
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at >= '2025-12-01'
GROUP BY 1, 2;

### [2025-12-09 13:20:00 UTC] — User: gabriel.stroud (assoc_100330)
-- Assessing winter storm impact on JOL1 (Joliet) DC operations.
SELECT 
    node_id,
    date,
    orders_promised,
    orders_on_time,
    avg_days_late_when_late
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE node_id = 'fc_jol1_01' AND date BETWEEN '2025-12-07' AND '2025-12-10';

### [2025-12-16 11:05:00 UTC] — User: giulia.romano (assoc_100213)
-- ALERT CHECK: Medallia refund delay verbatim theme share crossing 10% threshold.
SELECT 
    DATE(responded_at) as resp_date,
    theme_tag,
    COUNT(*) as verbatim_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(PARTITION BY DATE(responded_at)), 2) as daily_share_pct
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE responded_at >= '2025-12-01' AND theme_tag LIKE '%refund%'
GROUP BY 1, 2
ORDER BY resp_date DESC;

### [2025-12-20 15:30:11 UTC] — User: amara.shah (assoc_100211)
-- Holiday peak GMV check across US conversion and Marketplace.
SELECT 
    vertical_code,
    SUM(gmv_usd) as q4_mtd_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date BETWEEN '2025-11-01' AND '2025-12-19'
GROUP BY 1;

### [2025-12-28 09:00:00 UTC] — User: connor.blake (assoc_100212)
-- Checking table partitioning health for fact_orders as year-end volume peaks.
SELECT 
    table_name,
    partition_id,
    row_count
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'fact_orders';

### [2026-01-02 10:15:40 UTC] — User: wei.hartono (assoc_100210)
-- Pre-audit validation of Q4 peak session metrics.
SELECT 
    market,
    SUM(sessions) as total_sessions,
    SUM(orders) as total_orders
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date BETWEEN '2025-11-01' AND '2025-12-31'
GROUP BY 1;

### [2026-01-06 08:45:12 UTC] — User: hannah.brennan (assoc_100020)
-- QUANTITATIVE ALERT: Checking average refund cycle days from fact_orders (POR-Care shared metric).
-- NOTE: Crossing the 5.0-day SLA alert threshold (observed 5.03 days).
SELECT 
    DATE_TRUNC(return_date, WEEK) as return_week,
    COUNT(order_id) as returned_orders,
    AVG(DATE_DIFF(refund_issued_date, return_date, DAY)) as avg_refund_cycle_days
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE return_date >= '2025-11-01' AND refund_issued_date IS NOT NULL
GROUP BY 1
ORDER BY return_week DESC;

### [2026-01-13 10:20:00 UTC] — User: gabriel.stroud (assoc_100330)
-- Monitoring FON2 and JOL1 DC sortation automation Phase 1 rollout impact.
SELECT 
    node_id,
    date,
    orders_promised,
    orders_on_time
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE node_id IN ('fc_fon2_01', 'fc_jol1_01') AND date >= '2026-01-12'
ORDER BY date DESC;

### [2026-01-13 14:10:00 UTC] — User: leo.brandt (assoc_100141)
-- Initial exposure tracking for 'Wider Promise Window' experiment (exp_1187).
SELECT 
    experiment_id,
    variant,
    exposure_date,
    units_assigned,
    units_exposed
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures`
WHERE experiment_id = 'exp_1187'
ORDER BY exposure_date DESC;

### [2026-01-16 09:30:15 UTC] — User: tara.oduya (assoc_100140)
-- Tracking initial pickup mix changes following 'Pickup Perks' campaign launch (2026-01-15).
SELECT 
    date,
    fulfillment_type,
    on_time_rate,
    pct_of_total_orders,
    avg_cost_per_order_usd
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE date >= '2026-01-10'
ORDER BY date DESC;

### [2026-01-16 11:00:00 UTC] — User: lucia.ferreira (assoc_100320)
-- Confirming reinstatement status for Bramblewood Vintage (sel_500089) following compliance review.
SELECT 
    seller_id,
    seller_name,
    status,
    onboarded_date
FROM `nexus-analyst-demo.acme_ecomm.dim_seller`
WHERE seller_id = 'sel_500089';

### [2026-01-21 13:45:00 UTC] — User: dominic.paquet (assoc_100310)
-- Reviewing Ask Acme v2 Q4 deflection performance and CSAT trends for leadership sync.
SELECT 
    sub_program,
    SUM(contact_volume) as total_volume,
    AVG(deflection_rate) as avg_deflection,
    AVG(avg_csat_deflected) as csat_deflected
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
WHERE date BETWEEN '2025-11-01' AND '2026-01-20'
GROUP BY 1;

### [2026-01-24 16:00:00 UTC] — User: amara.shah (assoc_100211)
-- Preparing final Q4FY26 financial reconciliation pack and checking restated Marketplace GMV.
SELECT 
    fiscal_week_ending,
    SUM(gmv_usd) as total_marketplace_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE fiscal_week_ending BETWEEN '2025-11-01' AND '2026-01-31'
GROUP BY 1
ORDER BY fiscal_week_ending DESC;

-- ============================================================================
-- END OF AUDIT LOG EXTRACT (q4fy26 round snapshot as of 2026-01-25)
-- ============================================================================
```
