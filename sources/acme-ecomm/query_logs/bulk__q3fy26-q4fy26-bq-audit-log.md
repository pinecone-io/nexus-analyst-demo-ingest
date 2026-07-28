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


### [2026-01-21 14:15:30 UTC] — User: connor.blake (assoc_100212)
-- Investigating incremental pipeline lag on fact_marketplace_listings load partition.
SELECT 
    DATE(listing_date) as lst_date,
    category,
    COUNT(*) as total_listings,
    SUM(CASE WHEN authenticity_verified THEN 1 ELSE 0 END) as verified_count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
WHERE listing_date >= '2026-01-01'
GROUP BY 1, 2
ORDER BY lst_date DESC;

### [2026-01-21 15:00:22 UTC] — User: amara.shah (assoc_100211)
-- Running standard weekly join check between dim_member and fact_orders for finance audit.
SELECT 
    m.home_market,
    COUNT(DISTINCT m.member_id) as member_count,
    SUM(o.gmv_usd) as total_gmv
FROM `nexus-analyst-demo.acme_ecomm.dim_member` m
LEFT JOIN `nexus-analyst-demo.acme_ecomm.fact_orders` o ON m.member_id = o.member_id
WHERE o.order_date >= '2026-01-01'
GROUP BY 1;

### [2026-01-22 08:10:00 UTC] — User: hannah.brennan (assoc_100020)
-- Pulling preliminary Ontario returns center intake metrics following emergency overtime auth.
SELECT 
    node_id,
    node_type,
    market,
    is_active
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE node_type = 'returns_center';

### [2026-01-22 09:25:40 UTC] — User: giulia.romano (assoc_100213)
-- Analyzing recent Medallia verbatim feedback for refund delay themes in CA market.
SELECT 
    response_id,
    score,
    theme_tag,
    SUBSTR(verbatim_text, 1, 80) as snippet
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE survey_type = 'post_purchase'
  AND theme_tag = 'refund delay'
  AND responded_at >= '2026-01-01'
LIMIT 25;

### [2026-01-22 11:45:10 UTC] — User: wei.hartono (assoc_100210)
-- Validating traffic session counts across definitions ahead of monthly reporting lock.
SELECT 
    date,
    sessions_definition_version,
    SUM(sessions) as total_sessions,
    SUM(orders) as total_orders
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date BETWEEN '2026-01-01' AND '2026-01-20'
GROUP BY 1, 2
ORDER BY date DESC;

### [2026-01-22 14:00:00 UTC] — User: lucia.ferreira (assoc_100320)
-- Checking seller status for Bramblewood Vintage (sel_500089) post-reinstatement audit.
SELECT 
    seller_id,
    seller_name,
    category_focus,
    status,
    onboarded_date
FROM `nexus-analyst-demo.acme_ecomm.dim_seller`
WHERE seller_id = 'sel_500089';

### [2026-01-23 07:30:12 UTC] — User: connor.blake (assoc_100212)
-- Checking partition sizes on fact_care_contacts after weekly partition maintenance job.
SELECT 
    SUB_PROGRAM,
    channel,
    COUNT(*) as contact_rows
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at >= '2026-01-01'
GROUP BY 1, 2;

### [2026-01-23 09:12:00 UTC] — User: tara.oduya (assoc_100140)
-- Reviewing daily fulfillment speed breakdown for ship_to_home versus bopis in US market.
SELECT 
    date,
    fulfillment_type,
    orders_promised,
    on_time_rate
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE market = 'US'
  AND date >= '2026-01-15'
ORDER BY date DESC;

### [2026-01-23 10:45:30 UTC] — User: leo.brandt (assoc_100141)
-- Checking experiment exposure tracking for Wider Promise Window experiment (exp_1187).
SELECT 
    exposure_date,
    variant,
    SUM(units_assigned) as assigned,
    SUM(units_exposed) as exposed
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures`
WHERE experiment_id = 'exp_1187'
GROUP BY 1, 2
ORDER BY exposure_date DESC;

### [2026-01-23 13:20:00 UTC] — User: amara.shah (assoc_100211)
-- Running interim marketplace GMV totals by sub-vertical for leadership prep.
SELECT 
    fiscal_week_ending,
    sub_vertical_code,
    SUM(gmv_usd) as weekly_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE fiscal_week_ending >= '2026-01-01'
GROUP BY 1, 2
ORDER BY fiscal_week_ending DESC;

### [2026-01-23 15:10:45 UTC] — User: sanjay.bhatt (assoc_100120)
-- Pulling Marketplace seller performance metrics for Collectibles category focus.
SELECT 
    s.seller_id,
    s.seller_name,
    p.active_listings,
    p.trailing_90d_gmv_usd,
    p.return_rate
FROM `nexus-analyst-demo.acme_ecomm.dim_seller` s
JOIN `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance` p ON s.seller_id = p.seller_id
WHERE s.category_focus = 'collectibles'
ORDER BY p.trailing_90d_gmv_usd DESC
LIMIT 20;

### [2026-01-24 08:00:15 UTC] — User: connor.blake (assoc_100212)
-- Verifying freshness of dim_member panel table rows.
SELECT 
    plan_type,
    status,
    COUNT(*) as member_count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
GROUP BY 1, 2;

### [2026-01-24 09:45:00 UTC] — User: dominic.paquet (assoc_100310)
-- Querying daily care deflection metrics across sub-programs for operational review.
SELECT 
    date,
    sub_program,
    contact_volume,
    deflection_rate,
    avg_csat_deflected
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
WHERE date >= '2026-01-15'
ORDER BY date DESC;

### [2026-01-24 11:30:20 UTC] — User: giulia.romano (assoc_100213)
-- Extracting NPS score distributions from post-purchase survey responses.
SELECT 
    DATE(responded_at) as response_date,
    score,
    COUNT(*) as response_count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE survey_type = 'nps'
  AND responded_at >= '2026-01-01'
GROUP BY 1, 2
ORDER BY response_date DESC;

### [2026-01-24 14:00:00 UTC] — User: maya.lindqvist (assoc_100110)
-- Querying traffic and conversion summary mart for US market weekly trend.
SELECT 
    fiscal_week_ending,
    market,
    sessions,
    orders,
    conversion_rate,
    gmv_usd
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'US'
  AND fiscal_week_ending >= '2025-12-01'
ORDER BY fiscal_week_ending DESC;

### [2026-01-25 08:30:00 UTC] — User: connor.blake (assoc_100212)
-- Routine check of table schemas and row counts across all base fact tables.
SELECT 
    'fact_orders' as table_name, COUNT(*) as row_count FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
UNION ALL
SELECT 
    'fact_care_contacts', COUNT(*) FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
UNION ALL
SELECT 
    'fact_voc_responses', COUNT(*) FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`;

### [2026-01-25 10:15:00 UTC] — User: amara.shah (assoc_100211)
-- Finalizing Q4FY26 reconciliation queries for marketplace and conversion GMV totals.
SELECT 
    'conversion' as channel_type,
    SUM(gmv_usd) as total_gmv
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE fiscal_week_ending BETWEEN '2025-11-01' AND '2026-01-25'
UNION ALL
SELECT 
    'marketplace',
    SUM(gmv_usd)
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE fiscal_week_ending BETWEEN '2025-11-01' AND '2026-01-25';

### [2026-01-25 12:45:00 UTC] — User: tara.oduya (assoc_100140)
-- Pulling final fulfillment speed and cost metrics for weekly operational review.
SELECT 
    date,
    fulfillment_type,
    on_time_rate,
    avg_cost_per_order_usd
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE date = '2026-01-24';

### [2026-01-25 14:30:00 UTC] — User: wei.hartono (assoc_100210)
-- Audit query for experiment readout consistency across dim_experiment and fact_experiment_readouts.
SELECT 
    e.experiment_id,
    e.experiment_name,
    r.metric_name,
    r.metric_value,
    r.is_significant
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment` e
JOIN `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts` r ON e.experiment_id = r.experiment_id
WHERE e.status = 'shipped';

### [2026-01-25 15:45:00 UTC] — User: giulia.romano (assoc_100213)
-- Extracting weekly Medallia VOC verbatim themes for the Care department weekly review.
SELECT 
    DATE(responded_at) as response_date,
    market,
    theme_tag,
    COUNT(*) as verbatim_count,
    ROUND(AVG(score), 2) as avg_score
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE responded_at >= '2026-01-01'
  AND survey_type = 'post_care_contact'
GROUP BY 1, 2, 3
ORDER BY response_date DESC, verbatim_count DESC
LIMIT 50;

### [2026-01-25 16:10:22 UTC] — User: connor.blake (assoc_100212)
-- Checking daily partition sizes and row additions for order and fulfillment logs.
SELECT 
    order_date,
    market,
    COUNT(*) as order_count,
    SUM(gmv_usd) as daily_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE order_date >= '2026-01-01'
GROUP BY 1, 2
ORDER BY order_date DESC;

### [2026-01-25 17:00:00 UTC] — User: associate_99104 (assoc_100111)
-- Checking search query latency distribution and zero-result queries for US desktop vs app.
SELECT 
    device,
    COUNT(DISTINCT order_id) as orders_with_search
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE order_date = '2026-01-24'
GROUP BY device;

### [2026-01-25 18:30:15 UTC] — User: wei.hartono (assoc_100210)
-- Validating dim_fulfillment_node active status across distribution centers and stores.
SELECT 
    node_type,
    market,
    COUNT(*) as node_count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE is_active = TRUE
GROUP BY node_type, market;

### [2026-01-25 19:15:00 UTC] — User: tara.oduya (assoc_100140)
-- Reviewing fulfillment speed performance for store pickup vs ship to home.
SELECT 
    date,
    fulfillment_type,
    SUM(orders_promised) as total_promised,
    SUM(orders_on_time) as total_on_time,
    ROUND(SAFE_DIVIDE(SUM(orders_on_time), SUM(orders_promised)) * 100, 2) as calculated_otp
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE date BETWEEN '2026-01-01' AND '2026-01-24'
GROUP BY date, fulfillment_type
ORDER BY date DESC, fulfillment_type;

### [2026-01-25 20:00:00 UTC] — User: amara.shah (assoc_100211)
-- Reconciling marketplace listings status breakdown by category.
SELECT 
    category,
    status,
    COUNT(*) as listing_count,
    ROUND(AVG(price_usd), 2) as avg_price
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY category, status;

### [2026-01-25 21:12:40 UTC] — User: giulia.romano (assoc_100213)
-- Analyzing chat vs bot contact volumes and CSAT scores for Q4 peak evaluation.
SELECT 
    channel,
    sub_program,
    COUNT(*) as total_contacts,
    ROUND(AVG(csat_score), 2) as avg_csat,
    ROUND(AVG(handle_time_minutes), 2) as avg_handle_time
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at >= '2025-11-01'
GROUP BY channel, sub_program
ORDER BY total_contacts DESC;

### [2026-01-25 22:30:00 UTC] — User: connor.blake (assoc_100212)
-- Running routine audit of dim_member table plan distribution and status.
SELECT 
    plan_type,
    status,
    COUNT(*) as member_count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
GROUP BY plan_type, status;

### [2026-01-25 23:45:10 UTC] — User: wei.hartono (assoc_100210)
-- Checking experiment readout table constraints and recent variant performance.
SELECT 
    experiment_id,
    variant,
    metric_name,
    metric_value,
    sample_size_units
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`
WHERE as_of_date = '2026-01-24';

-- Additional routine query audit trail for Q3/Q4FY26 peak operations
-- System: bq_query_log (BigQuery)
-- Dataset: nexus-analyst-demo.acme_ecomm

### [2026-01-25 23:55:00 UTC] — User: amara.shah (assoc_100211)
-- Validating weekly merchandise mix percentages for financial close preparation.
SELECT 
    date_trunc(date, WEEK(MONDAY)) as fiscal_week,
    fulfillment_type,
    SUM(orders_promised) as total_promised,
    ROUND(SAFE_DIVIDE(SUM(orders_on_time), SUM(orders_promised)) * 100, 2) as otp_pct
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE date BETWEEN '2025-11-01' AND '2026-01-24'
GROUP BY 1, 2
ORDER BY fiscal_week DESC, fulfillment_type;

### [2026-01-26 00:15:20 UTC] — User: connor.blake (assoc_100212)
-- Checking partition sizes and row counts on fact_orders table.
SELECT 
    market,
    channel,
    COUNT(*) as order_count,
    ROUND(SUM(gmv_usd), 2) as total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE order_date >= '2025-11-01'
GROUP BY market, channel;

### [2026-01-26 01:02:11 UTC] — User: giulia.romano (assoc_100213)
-- Extracting care contact categorization by channel and resolution code during peak weeks.
SELECT 
    channel,
    sub_program,
    resolution_code,
    COUNT(*) as contact_count
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at >= TIMESTAMP('2025-11-01 00:00:00 UTC')
GROUP BY channel, sub_program, resolution_code
ORDER BY contact_count DESC
LIMIT 50;

### [2026-01-26 02:30:45 UTC] — User: wei.hartono (assoc_100210)
-- Audit of experiment assignment counts vs exposed units in experimental readouts.
SELECT 
    experiment_id,
    variant,
    MAX(sample_size_units) as max_sample_size,
    COUNT(DISTINCT as_of_date) as readout_days
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`
GROUP BY experiment_id, variant;

### [2026-01-26 03:10:00 UTC] — User: tara.oduya (assoc_100140)
-- Comparing fulfillment node capacity and performance for sorting centers.
SELECT 
    n.node_id,
    n.node_name,
    n.market,
    COUNT(p.order_id) as total_orders_routed
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node` n
LEFT JOIN `nexus-analyst-demo.acme_ecomm.fact_orders` o ON n.node_id = o.order_id
GROUP BY n.node_id, n.node_name, n.market;

### [2026-01-26 04:20:15 UTC] — User: amara.shah (assoc_100211)
-- Running initial Q4 GMV summary check across marketplaces.
SELECT 
    fiscal_week_ending,
    sub_vertical_code,
    ROUND(SUM(gmv_usd), 2) as total_gmv,
    SUM(orders) as total_orders
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE fiscal_week_ending >= '2025-11-01'
GROUP BY fiscal_week_ending, sub_vertical_code
ORDER BY fiscal_week_ending DESC;

### [2026-01-26 05:00:00 UTC] — User: connor.blake (assoc_100212)
-- Routine check of dim_associate active records and regional distribution.
SELECT 
    location,
    role,
    COUNT(*) as headcount
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
WHERE is_active = TRUE
GROUP BY location, role
ORDER BY headcount DESC;

### [2026-01-26 06:15:33 UTC] — User: giulia.romano (assoc_100213)
-- Reviewing member acquisition channel distributions across active profiles.
SELECT 
    acquisition_channel,
    plan_type,
    COUNT(*) as member_count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
WHERE status = 'active'
GROUP BY acquisition_channel, plan_type
ORDER BY member_count DESC;

### [2026-01-26 07:45:00 UTC] — User: wei.hartono (assoc_100210)
-- Validating daily traffic totals across device classifications for US conversions.
SELECT 
    date,
    device,
    SUM(sessions) as total_sessions,
    SUM(orders) as total_orders
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE market = 'US' AND date >= '2025-10-01'
GROUP BY date, device
ORDER BY date DESC, device;

### [2026-01-26 09:00:22 UTC] — User: tara.oduya (assoc_100140)
-- Auditing fulfillment speed metrics for ship to home orders specifically.
SELECT 
    date,
    market,
    orders_promised,
    orders_on_time,
    avg_days_late_when_late
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE fulfillment_type = 'ship_to_home' AND date >= '2026-01-01'
ORDER BY date DESC;

### [2026-01-26 10:12:00 UTC] — User: amara.shah (assoc_100211)
-- Reconciling marketplace listing authenticity flags against seller categories.
SELECT 
    category,
    authenticity_verified,
    COUNT(*) as listing_count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY category, authenticity_verified;

### [2026-01-26 11:30:10 UTC] — User: connor.blake (assoc_100212)
-- Checking table schema metadata and partition pruning efficiency on traffic logs.
SELECT 
    table_name,
    row_count,
    size_bytes
FROM `nexus-analyst-demo.acme_ecomm.__TABLES__`
ORDER BY size_bytes DESC;

### [2026-01-26 12:05:40 UTC] — User: giulia.romano (assoc_100213)
-- Analyzing post-purchase survey sentiment scores and theme tags.
SELECT 
    theme_tag,
    sentiment,
    COUNT(*) as response_count,
    ROUND(AVG(score), 2) as avg_score
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE survey_type = 'post_purchase' AND responded_at >= TIMESTAMP('2025-11-01 00:00:00 UTC')
GROUP BY theme_tag, sentiment
ORDER BY response_count DESC;

### [2026-01-26 13:20:00 UTC] — User: wei.hartono (assoc_100210)
-- Querying membership lifecycle events for subscription state transitions.
SELECT 
    event_type,
    channel,
    COUNT(*) as event_count
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
WHERE event_date >= '2025-11-01'
GROUP BY event_type, channel
ORDER BY event_count DESC;

### [2026-01-26 14:40:15 UTC] — User: tara.oduya (assoc_100140)
-- Reviewing fulfillment node activity for regional fulfillment centers.
SELECT 
    market,
    node_type,
    COUNT(*) as node_count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE is_active = TRUE
GROUP BY market, node_type;

### [2026-01-26 15:15:00 UTC] — User: amara.shah (assoc_100211)
-- Pulling marketplace seller performance metrics for top category focus groups.
SELECT 
    category_focus,
    COUNT(seller_id) as seller_count,
    ROUND(SUM(trailing_90d_gmv_usd), 2) as total_trailing_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
GROUP BY category_focus;

### [2026-01-26 16:00:50 UTC] — User: connor.blake (assoc_100212)
-- Validating marketing calendar budget versus actual spend across campaigns.
SELECT 
    event_type,
    COUNT(*) as event_count,
    ROUND(SUM(planned_spend_usd), 2) as total_planned,
    ROUND(SUM(actual_spend_usd), 2) as total_actual
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
GROUP BY event_type;

### [2026-01-26 17:10:30 UTC] — User: giulia.romano (assoc_100213)
-- Examining care contact deflection distribution and deflection type details.
SELECT 
    deflection_type,
    COUNT(*) as contact_count,
    ROUND(AVG(csat_score), 2) as avg_csat
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE deflected = TRUE AND opened_at >= TIMESTAMP('2025-12-01 00:00:00 UTC')
GROUP BY deflection_type;

### [2026-01-26 18:00:00 UTC] — User: wei.hartono (assoc_100210)
-- Testing traffic conversion summary aggregates for weekly reporting consistency.
SELECT 
    fiscal_week_ending,
    market,
    vertical_code,
    sessions,
    orders,
    conversion_rate
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE fiscal_week_ending >= '2026-01-01'
ORDER BY fiscal_week_ending DESC, market;

### [2026-01-26 19:22:11 UTC] — User: tara.oduya (assoc_100140)
-- Reviewing care deflection daily metrics against promised delivery windows.
SELECT 
    date,
    sub_program,
    contact_volume,
    deflection_rate
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
WHERE date >= '2026-01-01'
ORDER BY date DESC, sub_program;

### [2026-01-26 20:05:40 UTC] — User: amara.shah (assoc_100211)
-- Auditing order refund columns and refund issued date presence in sample orders.
SELECT 
    is_returned,
    COUNT(*) as order_count,
    ROUND(AVG(refund_usd), 2) as avg_refund
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE is_returned = TRUE AND order_date >= '2025-11-01'
GROUP BY is_returned;

### [2026-01-26 21:14:00 UTC] — User: connor.blake (assoc_100212)
-- Verifying dimension table foreign key constraints across vertical code definitions.
SELECT 
    vertical_code,
    vertical_name,
    is_deep_dive
FROM `nexus-analyst-demo.acme_ecomm.dim_vertical`
ORDER BY vertical_code;

### [2026-01-26 22:30:15 UTC] — User: giulia.romano (assoc_100213)
-- Checking experiment readout metrics for variant performance evaluations.
SELECT 
    metric_name,
    COUNT(*) as readout_count,
    ROUND(AVG(metric_value), 4) as avg_metric_value
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`
WHERE as_of_date >= '2026-01-01'
GROUP BY metric_name;

### [2026-01-26 23:45:00 UTC] — User: wei.hartono (assoc_100210)
-- Checking member CLTV calculations using standard dataset definitions.
SELECT 
    signup_cohort_quarter,
    COUNT(member_id) as member_count,
    ROUND(AVG(projected_cltv_usd), 2) as avg_projected_cltv
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`
GROUP BY signup_cohort_quarter
ORDER BY signup_cohort_quarter DESC;

### [2026-01-26 23:59:10 UTC] — User: connor.blake (assoc_100212)
-- Routine partition check on fact_orders table.
SELECT 
    table_name,
    partition_id,
    row_count
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'fact_orders'
ORDER BY partition_id DESC
LIMIT 10;

### [2026-01-27 01:15:30 UTC] — User: amara.shah (assoc_100211)
-- Reconciling Q4FY26 marketplace settlement totals against finance ledger feeds.
SELECT 
    DATE_TRUNC(order_date, MONTH) as order_month,
    SUM(gmv_usd) as monthly_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE channel = '3P' AND order_date BETWEEN '2025-11-01' AND '2025-12-31'
GROUP BY 1
ORDER BY 1;

### [2026-01-27 02:40:12 UTC] — User: wei.hartono (assoc_100210)
-- Validating session definition counts across device categories for early January.
SELECT 
    device,
    sessions_definition_version,
    COUNT(*) as row_count
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date BETWEEN '2026-01-01' AND '2026-01-15'
GROUP BY 1, 2
ORDER BY 1, 2;

### [2026-01-27 08:10:05 UTC] — User: tara.oduya (assoc_100140)
-- Reviewing fulfillment node activity for regional sortation hubs.
SELECT 
    node_id,
    node_type,
    market,
    is_active
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE node_type IN ('fc', 'sortation_center')
ORDER BY node_id;

### [2026-01-27 09:22:48 UTC] — User: giulia.romano (assoc_100213)
-- Checking CSAT scores for post-care contact surveys during holiday peak.
SELECT 
    survey_type,
    score_type,
    ROUND(AVG(score), 2) as avg_score,
    COUNT(*) as response_count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE survey_type = 'post_care_contact' AND responded_at >= '2025-11-01'
GROUP BY 1, 2;

### [2026-01-27 10:04:15 UTC] — User: connor.blake (assoc_100212)
-- Testing query performance on marketplace listing authenticity flags.
SELECT 
    category,
    authenticity_verified,
    COUNT(*) as listing_count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY 1, 2
ORDER BY 1;

### [2026-01-27 11:30:20 UTC] — User: amara.shah (assoc_100211)
-- Aggregating member acquisition channel performance for Q4 cohort reporting.
SELECT 
    acquisition_channel,
    plan_type,
    COUNT(*) as member_count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
WHERE signup_date >= '2025-11-01'
GROUP BY 1, 2
ORDER BY member_count DESC;

### [2026-01-27 13:05:50 UTC] — User: wei.hartono (assoc_100210)
-- Checking table metadata and column definitions for member_cltv.
SELECT 
    column_name,
    data_type
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'member_cltv'
ORDER BY ordinal_position;

### [2026-01-27 14:18:33 UTC] — User: tara.oduya (assoc_100140)
-- Auditing promise vs actual fulfillment performance by market for mid-January.
SELECT 
    date,
    market,
    fulfillment_type,
    SUM(orders_promised) as total_promised,
    SUM(orders_on_time) as total_ontime
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE date >= '2026-01-01'
GROUP BY 1, 2, 3
ORDER BY date DESC, market;

### [2026-01-27 15:50:11 UTC] — User: giulia.romano (assoc_100213)
-- Analyzing care contact volume by sub_program for bot deflection monitoring.
SELECT 
    sub_program,
    channel,
    COUNT(*) as contact_count,
    ROUND(AVG(handle_time_minutes), 2) as avg_handle_time
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at >= '2026-01-01'
GROUP BY 1, 2
ORDER BY contact_count DESC;

### [2026-01-27 17:02:40 UTC] — User: connor.blake (assoc_100212)
-- Verifying foreign key relationships between dim_seller and marketplace listings.
SELECT 
    s.seller_id,
    s.seller_name,
    COUNT(l.listing_id) as total_listings
FROM `nexus-analyst-demo.acme_ecomm.dim_seller` s
LEFT JOIN `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings` l ON s.seller_id = l.seller_id
GROUP BY 1, 2
ORDER BY total_listings DESC
LIMIT 20;

### [2026-01-27 18:30:15 UTC] — User: amara.shah (assoc_100211)
-- Running preliminary checks on Q4FY26 refund metrics from fact_orders.
SELECT 
    is_returned,
    COUNT(order_id) as returned_orders,
    ROUND(AVG(refund_usd), 2) as avg_refund_amt
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE order_date BETWEEN '2025-11-01' AND '2025-12-31'
GROUP BY is_returned;

### [2026-01-27 19:45:22 UTC] — User: wei.hartono (assoc_100210)
-- Pulling experiment readouts for active optimization tests.
SELECT 
    experiment_id,
    variant,
    metric_name,
    ROUND(AVG(metric_value), 4) as avg_val
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`
WHERE as_of_date >= '2026-01-01'
GROUP BY 1, 2, 3
ORDER BY experiment_id;

### [2026-01-27 21:10:04 UTC] — User: tara.oduya (assoc_100140)
-- Checking care deflection daily summary trends.
SELECT 
    sub_program,
    SUM(contact_volume) as total_contacts,
    ROUND(AVG(deflection_rate), 2) as avg_deflection
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
WHERE date >= '2026-01-01'
GROUP BY sub_program;

### [2026-01-27 22:25:50 UTC] — User: giulia.romano (assoc_100213)
-- Investigating Voc response sentiment breakdown across post-purchase surveys.
SELECT 
    sentiment,
    theme_tag,
    COUNT(*) as response_count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE survey_type = 'post_purchase' AND responded_at >= '2026-01-01'
GROUP BY 1, 2
ORDER BY response_count DESC
LIMIT 15;

### [2026-01-28 00:15:30 UTC] — User: connor.blake (assoc_100212)
-- Auditing partition sizes for large fact tables.
SELECT 
    table_name,
    SUM(size_bytes) / (1024*1024*1024) as size_gb
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.TABLE_STORAGE`
GROUP BY table_name
ORDER BY size_gb DESC;

### [2026-01-28 01:40:12 UTC] — User: amara.shah (assoc_100211)
-- Querying traffic conversion summary for weekly Board report validation.
SELECT 
    fiscal_week_ending,
    market,
    SUM(sessions) as total_sessions,
    SUM(orders) as total_orders
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE fiscal_week_ending >= '2026-01-01'
GROUP BY 1, 2
ORDER BY fiscal_week_ending DESC;

### [2026-01-28 03:05:40 UTC] — User: wei.hartono (assoc_100210)
-- Checking member CLTV distribution by signup quarter.
SELECT 
    signup_cohort_quarter,
    COUNT(*) as member_count,
    ROUND(AVG(lifetime_gmv_usd), 2) as avg_lifetime_gmv
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`
GROUP BY signup_cohort_quarter
ORDER BY signup_cohort_quarter DESC;

### [2026-01-28 08:20:11 UTC] — User: tara.oduya (assoc_100140)
-- Reviewing fulfillment speed daily metrics for ship-to-home orders.
SELECT 
    date,
    market,
    fulfillment_type,
    ROUND(on_time_rate, 4) as on_time_rate
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE fulfillment_type = 'ship_to_home' AND date >= '2026-01-01'
ORDER BY date DESC
LIMIT 10;

### [2026-01-28 09:55:00 UTC] — User: giulia.romano (assoc_100213)
-- Checking care contact resolution codes for automated deflection chats.
SELECT 
    resolution_code,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE channel = 'bot' AND opened_at >= '2026-01-01'
GROUP BY 1
ORDER BY count DESC;

### [2026-01-28 11:10:25 UTC] — User: connor.blake (assoc_100212)
-- Validating dim_vertical primary keys.
SELECT 
    vertical_code,
    vertical_name,
    sub_vertical_code
FROM `nexus-analyst-demo.acme_ecomm.dim_vertical`
ORDER BY vertical_code, sub_vertical_code;

### [2026-01-28 12:40:50 UTC] — User: amara.shah (assoc_100211)
-- Running marketplace GMV summary audit by sub-vertical for Q4 results.
SELECT 
    fiscal_week_ending,
    sub_vertical_code,
    SUM(gmv_usd) as weekly_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE fiscal_week_ending BETWEEN '2025-11-01' AND '2025-12-31'
GROUP BY 1, 2
ORDER BY fiscal_week_ending DESC;

### [2026-01-28 14:05:12 UTC] — User: wei.hartono (assoc_100210)
-- Verifying experiment exposure metrics for running tests.
SELECT 
    experiment_id,
    variant,
    SUM(units_exposed) as total_exposed
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures`
GROUP BY 1, 2;

### [2026-01-28 15:30:44 UTC] — User: tara.oduya (assoc_100140)
-- Auditing membership event frequencies by event type.
SELECT 
    event_type,
    channel,
    COUNT(*) as event_count
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
WHERE event_date >= '2026-01-01'
GROUP BY 1, 2
ORDER BY event_count DESC;

### [2026-01-28 17:15:00 UTC] — User: giulia.romano (assoc_100213)
-- Checking Voc survey response distribution across channels and scores.
SELECT 
    score_type,
    score,
    COUNT(*) as freq
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE responded_at >= '2026-01-01'
GROUP BY 1, 2
ORDER BY 1, 2;

### [2026-01-28 18:50:30 UTC] — User: connor.blake (assoc_100212)
-- Checking table row counts across base facts.
SELECT 'fact_orders' as tbl, COUNT(*) as cnt FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
UNION ALL
SELECT 'fact_care_contacts', COUNT(*) FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
UNION ALL
SELECT 'fact_marketplace_listings', COUNT(*) FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`;

### [2026-01-28 20:10:15 UTC] — User: amara.shah (assoc_100211)
-- Pulling average order values by market for Q4FY26 analysis.
SELECT 
    market,
    ROUND(AVG(gmv_usd), 2) as avg_order_value
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE order_date BETWEEN '2025-11-01' AND '2025-12-31'
GROUP BY market;

### [2026-01-28 21:40:50 UTC] — User: wei.hartono (assoc_100210)
-- Testing marketplace seller performance metrics aggregation.
SELECT 
    category_focus,
    COUNT(seller_id) as seller_count,
    ROUND(AVG(trailing_90d_gmv_usd), 2) as avg_trailing_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
GROUP BY category_focus;

### [2026-01-28 23:05:11 UTC] — User: tara.oduya (assoc_100140)
-- Checking marketing calendar events for upcoming promotional launches.
SELECT 
    event_name,
    event_type,
    start_date,
    end_date
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
WHERE start_date >= '2026-01-01'
ORDER BY start_date;

### [2026-01-29 01:20:04 UTC] — User: giulia.romano (assoc_100213)
-- Auditing care contacts with missing resolution codes.
SELECT 
    sub_program,
    COUNT(*) as unassigned_count
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE resolution_code IS NULL AND opened_at >= '2026-01-01'
GROUP BY sub_program;

### [2026-01-29 02:45:30 UTC] — User: connor.blake (assoc_100212)
-- Verifying column nullability across dim_member.
SELECT 
    plan_type,
    status,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
GROUP BY 1, 2;

### [2026-01-29 04:10:15 UTC] — User: amara.shah (assoc_100211)
-- Checking member cltv summary statistics.
SELECT 
    is_active,
    COUNT(*) as member_count,
    ROUND(AVG(projected_cltv_usd), 2) as avg_cltv
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`
GROUP BY is_active;

### [2026-01-29 08:30:50 UTC] — User: wei.hartono (assoc_100210)
-- Checking traffic daily summary for web vs app sessions in January.
SELECT 
    device,
    SUM(sessions) as total_sessions,
    SUM(orders) as total_orders
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date >= '2026-01-01'
GROUP BY device;

### [2026-01-29 09:55:20 UTC] — User: tara.oduya (assoc_100140)
-- Reviewing fulfillment speed daily metrics across node types.
SELECT 
    fulfillment_type,
    ROUND(AVG(on_time_rate), 4) as avg_on_time_rate,
    ROUND(AVG(avg_cost_per_order_usd), 2) as avg_cost
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE date >= '2026-01-01'
GROUP BY fulfillment_type;

### [2026-01-29 11:15:40 UTC] — User: giulia.romano (assoc_100213)
-- Analyzing weekly trends in care deflection rates.
SELECT 
    DATE_TRUNC(date, WEEK) as week_start,
    ROUND(AVG(deflection_rate), 2) as avg_deflection_rate
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
WHERE date >= '2026-01-01'
GROUP BY 1
ORDER BY 1 DESC;

### [2026-01-29 12:50:11 UTC] — User: connor.blake (assoc_100212)
-- Validating dim_associate table active counts.
SELECT 
    team,
    COUNT(*) as active_associates
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
WHERE is_active = TRUE
GROUP BY team
ORDER BY active_associates DESC;

### [2026-01-29 14:20:00 UTC] — User: amara.shah (assoc_100211)
-- Auditing refund issued dates presence on returned orders in fact_orders.
SELECT 
    is_returned,
    COUNT(CASE WHEN refund_issued_date IS NOT NULL THEN 1 END) as has_refund_date,
    COUNT(CASE WHEN refund_issued_date IS NULL THEN 1 END) as missing_refund_date
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE is_returned = TRUE AND order_date >= '2025-11-01'
GROUP BY is_returned;

### [2026-01-29 15:45:30 UTC] — User: wei.hartono (assoc_100210)
-- Checking experiment readouts for significant variant results.
SELECT 
    experiment_id,
    metric_name,
    is_significant,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`
GROUP BY 1, 2, 3;

### [2026-01-29 17:10:22 UTC] — User: tara.oduya (assoc_100140)
-- Examining promise vs actual metrics for late shipments.
SELECT 
    market,
    SUM(orders_promised) as promised,
    SUM(orders_on_time) as on_time,
    ROUND(AVG(avg_days_late_when_late), 2) as avg_days_late
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE date >= '2026-01-01'
GROUP BY market;

### [2026-01-29 18:35:05 UTC] — User: giulia.romano (assoc_100213)
-- Checking Voc responses with negative sentiment.
SELECT 
    theme_tag,
    COUNT(*) as negative_count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE sentiment = 'negative' AND responded_at >= '2026-01-01'
GROUP BY theme_tag
ORDER BY negative_count DESC;

### [2026-01-29 20:02:14 UTC] — User: connor.blake (assoc_100212)
-- Checking table schema for marketplace_seller_performance.
SELECT 
    column_name,
    data_type
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'marketplace_seller_performance';

### [2026-01-29 21:30:50 UTC] — User: amara.shah (assoc_100211)
-- Reconciling traffic conversion summary totals with monthly revenue targets.
SELECT 
    market,
    SUM(gmv_usd) as total_gmv
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE fiscal_week_ending >= '2026-01-01'
GROUP BY market;

### [2026-01-29 22:55:00 UTC] — User: wei.hartono (assoc_100210)
-- Checking dimensions of dim_date for peak holiday flags.
SELECT 
    is_peak_holiday,
    COUNT(*) as day_count
FROM `nexus-analyst-demo.acme_ecomm.dim_date`
GROUP BY is_peak_holiday;

### [2026-01-30 01:10:33 UTC] — User: tara.oduya (assoc_100140)
-- Reviewing care deflection daily metrics by sub_program for January.
SELECT 
    sub_program,
    SUM(contact_volume) as total_volume,
    ROUND(AVG(deflection_rate), 2) as avg_deflection
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
WHERE date >= '2026-01-01'
GROUP BY sub_program;

### [2026-01-30 02:40:15 UTC] — User: giulia.romano (assoc_100213)
-- Checking member cltv benefits adopted count distribution.
SELECT 
    benefits_adopted_count,
    COUNT(*) as member_count,
    ROUND(AVG(lifetime_gmv_usd), 2) as avg_gmv
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`
GROUP BY benefits_adopted_count
ORDER BY benefits_adopted_count;

### [2026-01-30 08:15:20 UTC] — User: connor.blake (assoc_100212)
-- Running routine partition audit on fact_promise_vs_actual.
SELECT 
    partition_id,
    row_count
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'fact_promise_vs_actual'
ORDER BY partition_id DESC
LIMIT 5;

### [2026-01-30 09:40:50 UTC] — User: amara.shah (assoc_100211)
-- Pulling order counts by fulfillment type for January orders.
SELECT 
    fulfillment_type,
    COUNT(*) as order_count,
    ROUND(SUM(gmv_usd), 2) as total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE order_date >= '2026-01-01'
GROUP BY fulfillment_type
ORDER BY total_gmv DESC;

### [2026-01-30 11:05:12 UTC] — User: wei.hartono (assoc_100210)
-- Validating traffic conversion summary rows for missing conversion rates.
SELECT 
    COUNT(*) as null_conversion_rows
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE conversion_rate IS NULL;

### [2026-01-30 12:30:40 UTC] — User: tara.oduya (assoc_100140)
-- Checking marketplace gmv summary totals for Q4FY26.
SELECT 
    sub_vertical_code,
    SUM(gmv_usd) as total_gmv,
    SUM(orders) as total_orders
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE fiscal_week_ending BETWEEN '2025-11-01' AND '2025-12-31'
GROUP BY sub_vertical_code;

### [2026-01-30 13:55:00 UTC] — User: giulia.romano (assoc_100213)
-- Checking agent vs deflected CSAT averages in care deflection daily mart.
SELECT 
    sub_program,
    ROUND(AVG(avg_csat_deflected), 2) as csat_deflected,
    ROUND(AVG(avg_csat_agent_assisted), 2) as csat_agent
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
WHERE date >= '2026-01-01'
GROUP BY sub_program;

### [2026-01-30 15:20:15 UTC] — User: connor.blake (assoc_100212)
-- Checking table storage footprint for fact_traffic_daily.
SELECT 
    table_name,
    size_bytes / (1024*1024) as size_mb
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.TABLE_STORAGE`
WHERE table_name = 'fact_traffic_daily';

### [2026-01-30 16:45:30 UTC] — User: amara.shah (assoc_100211)
-- Pulling marketplace seller performance metrics for collectibles category.
SELECT 
    seller_id,
    active_listings,
    trailing_90d_gmv_usd,
    return_rate
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
WHERE category_focus = 'collectibles'
ORDER BY trailing_90d_gmv_usd DESC
LIMIT 10;

### [2026-01-30 18:10:04 UTC] — User: wei.hartono (assoc_100210)
-- Auditing dim_experiment table status counts.
SELECT 
    status,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment`
GROUP BY status;

### [2026-01-30 19:35:50 UTC] — User: tara.oduya (assoc_100140)
-- Checking fulfillment speed daily cost trends.
SELECT 
    fulfillment_type,
    ROUND(AVG(avg_cost_per_order_usd), 2) as avg_cost
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
GROUP BY fulfillment_type;

### [2026-01-30 21:00:11 UTC] — User: giulia.romano (assoc_100213)
-- Checking member cltv tenure distribution.
SELECT 
    TENURE_DAYS / 365 as tenure_years,
    COUNT(*) as member_count
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`
GROUP BY 1
ORDER BY tenure_years DESC
LIMIT 10;

### [2026-01-30 22:25:30 UTC] — User: connor.blake (assoc_100212)
-- Verifying primary key uniqueness on dim_vertical.
SELECT 
    vertical_code,
    sub_vertical_code,
    COUNT(*) as cnt
FROM `nexus-analyst-demo.acme_ecomm.dim_vertical`
GROUP BY 1, 2
HAVING cnt > 1;

### [2026-01-30 23:50:00 UTC] — User: amara.shah (assoc_100211)
-- Running monthly reconciliation query for total conversion sessions.
SELECT 
    FORMAT_DATE('%Y-%m', date) as month,
    SUM(sessions) as total_sessions
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date >= '2025-11-01'
GROUP BY 1
ORDER BY 1;

### [2026-01-31 01:15:22 UTC] — User: connor.blake (assoc_100212)
-- Checking partition sizes for fact_care_contacts across Q4FY26 partitions.
SELECT 
    table_name,
    partition_id,
    total_rows,
    size_bytes / (1024*1024) as size_mb
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'fact_care_contacts'
ORDER BY partition_id DESC
LIMIT 10;

### [2026-01-31 02:40:11 UTC] — User: wei.hartono (assoc_100210)
-- Validating dim_fulfillment_node active status distribution.
SELECT 
    node_type,
    is_active,
    COUNT(*) as node_count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
GROUP BY 1, 2;

### [2026-01-31 04:05:55 UTC] — User: amara.shah (assoc_100211)
-- Monthly summary of marketplace take rate by sub-vertical for Q4FY26 reconciliation.
SELECT 
    sub_vertical_code,
    ROUND(AVG(take_rate), 4) as avg_take_rate,
    SUM(gmv_usd) as total_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE fiscal_week_ending >= '2025-11-01'
GROUP BY 1;

### [2026-01-31 06:22:04 UTC] — User: tara.oduya (assoc_100140)
-- Examining delivery promise vs actual performance during December winter storm at JOL1.
SELECT 
    date,
    node_id,
    orders_promised,
    orders_on_time,
    ROUND(Safe_Divide(orders_on_time, orders_promised) * 100, 2) as otp_pct
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE node_id = 'str_jol1'
  AND date BETWEEN '2025-12-05' AND '2025-12-15';

### [2026-01-31 08:30:19 UTC] — User: giulia.romano (assoc_100213)
-- Analyzing care channel distribution for member_id mem_1000042.
SELECT 
    channel,
    COUNT(*) as contact_count,
    ROUND(AVG(CAST(csat_score AS NUMERIC)), 2) as avg_csat
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE member_id = 'mem_1000042'
GROUP BY 1;

### [2026-01-31 10:14:45 UTC] — User: connor.blake (assoc_100212)
-- Routine check on table metadata freshness for dim_associate.
SELECT 
    MAX(hire_date) as latest_hire
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`;

### [2026-01-31 11:55:08 UTC] — User: wei.hartono (assoc_100210)
-- Auditing fact_experiment_readouts for missing significance flags.
SELECT 
    experiment_id,
    COUNT(*) as readout_count
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`
WHERE is_significant IS NULL
GROUP BY 1;

### [2026-01-31 13:20:33 UTC] — User: amara.shah (assoc_100211)
-- Running preliminary US conversion check for holiday surge window.
SELECT 
    date,
    sessions,
    orders,
    ROUND(Safe_Divide(orders, sessions) * 100, 4) as conv_rate
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE market = 'US'
  AND date BETWEEN '2025-11-25' AND '2025-12-02'
ORDER BY date;

### [2026-01-31 14:45:12 UTC] — User: tara.oduya (assoc_100140)
-- Checking fulfillment speed daily cost trends for store fulfillment type.
SELECT 
    date,
    avg_cost_per_order_usd
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE fulfillment_type = 'dfs'
  AND date >= '2026-01-01'
ORDER BY date DESC
LIMIT 15;

### [2026-01-31 16:10:50 UTC] — User: giulia.romano (assoc_100213)
-- Extracting voc responses with negative sentiment regarding care contact channels.
SELECT 
    survey_type,
    SUBSTR(verbatim_text, 1, 80) as snippet,
    score
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE sentiment = 'negative'
  AND survey_type = 'post_care_contact'
LIMIT 10;

### [2026-01-31 17:35:21 UTC] — User: connor.blake (assoc_100212)
-- Validating referential integrity between fact_marketplace_listings and dim_seller.
SELECT 
    l.listing_id,
    l.seller_id
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings` l
LEFT JOIN `nexus-analyst-demo.acme_ecomm.dim_seller` s ON l.seller_id = s.seller_id
WHERE s.seller_id IS NULL
LIMIT 5;

### [2026-01-31 19:02:44 UTC] — User: wei.hartono (assoc_100210)
-- Testing query performance on traffic_conversion_summary with market filter.
SELECT 
    fiscal_week_ending,
    market,
    SUM(gmv_usd) as weekly_gmv
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
GROUP BY 1, 2
ORDER BY fiscal_week_ending DESC
LIMIT 8;

### [2026-01-31 20:20:10 UTC] — User: amara.shah (assoc_100211)
-- Pulling marketplace seller performance for sel_500012 across metrics.
SELECT 
    seller_id,
    category_focus,
    active_listings,
    trailing_90d_gmv_usd,
    return_rate,
    authenticity_flag_count
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
WHERE seller_id = 'sel_500012';

### [2026-01-31 21:50:18 UTC] — User: tara.oduya (assoc_100140)
-- Checking fulfillment speed daily metrics for pickup channels.
SELECT 
    date,
    fulfillment_type,
    on_time_rate,
    pct_of_total_orders
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE fulfillment_type IN ('bopis', 'curbside')
  AND date >= '2026-01-10'
ORDER BY date DESC
LIMIT 10;

### [2026-01-31 23:15:00 UTC] — User: giulia.romano (assoc_100213)
-- Analyzing member renewal events in fact_membership_events for annual plan holders.
SELECT 
    channel,
    COUNT(*) as renewal_events
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
WHERE event_type = 'renewal'
GROUP BY 1;

### [2026-02-01 01:05:40 UTC] — User: connor.blake (assoc_100212)
-- Verifying table schema and column types for dim_vertical.
SELECT 
    column_name,
    data_type
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'dim_vertical';

### [2026-02-01 02:30:15 UTC] — User: wei.hartono (assoc_100210)
-- Running monthly session aggregate check for Q4FY26 across devices.
SELECT 
    device,
    SUM(sessions) as total_sessions,
    SUM(orders) as total_orders
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date BETWEEN '2025-11-01' AND '2026-01-31'
GROUP BY 1;

### [2026-02-01 04:12:00 UTC] — User: amara.shah (assoc_100211)
-- Checking member cltv projected values for active members in home market US.
SELECT 
    m.home_market,
    ROUND(AVG(c.projected_cltv_usd), 2) as avg_projected_cltv
FROM `nexus-analyst-demo.acme_ecomm.dim_member` m
JOIN `nexus-analyst-demo.acme_ecomm.member_cltv` c ON m.member_id = c.member_id
WHERE m.status = 'active'
GROUP BY 1;

### [2026-02-01 05:48:30 UTC] — User: tara.oduya (assoc_100140)
-- Reviewing fulfillment node distribution by market for active centers.
SELECT 
    market,
    node_type,
    COUNT(*) as node_count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE is_active = TRUE
GROUP BY 1, 2;

### [2026-02-01 07:20:11 UTC] — User: giulia.romano (assoc_100213)
-- Checking care contact deflection rates daily for avoid sub-program.
SELECT 
    date,
    deflection_rate,
    contact_volume
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
WHERE sub_program = 'avoid'
  AND date >= '2026-01-01'
ORDER BY date DESC
LIMIT 10;

### [2026-02-01 09:05:22 UTC] — User: connor.blake (assoc_100212)
-- Checking row count for dim_marketing_calendar by event_type.
SELECT 
    event_type,
    COUNT(*) as event_count
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
GROUP BY 1;

### [2026-02-01 10:40:55 UTC] — User: wei.hartono (assoc_100210)
-- Testing query performance on fact_orders return reasons.
SELECT 
    return_reason_code,
    COUNT(*) as return_count,
    ROUND(SUM(refund_usd), 2) as total_refund
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE is_returned = TRUE
  AND return_reason_code IS NOT NULL
GROUP BY 1
ORDER BY total_refund DESC;

### [2026-02-01 12:15:30 UTC] — User: amara.shah (assoc_100211)
-- Auditing marketplace gmv summary totals for collectibles sub-vertical.
SELECT 
    fiscal_week_ending,
    gmv_usd,
    orders
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE sub_vertical_code = 'COLLECTIBLES'
ORDER BY fiscal_week_ending DESC
LIMIT 10;

### [2026-02-01 13:50:04 UTC] — User: tara.oduya (assoc_100140)
-- Checking promise vs actual performance across fulfillment types for US market.
SELECT 
    fulfillment_type,
    SUM(orders_promised) as total_promised,
    SUM(orders_on_time) as total_ontime,
    ROUND(SUM(orders_on_time) / SUM(orders_promised) * 100, 2) as aggregate_otp
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE market = 'US'
  AND date >= '2026-01-01'
GROUP BY 1;

### [2026-02-01 15:25:12 UTC] — User: giulia.romano (assoc_100213)
-- Checking voc responses distribution by score_type and sentiment.
SELECT 
    score_type,
    sentiment,
    COUNT(*) as resp_count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
GROUP BY 1, 2;

### [2026-02-01 17:00:48 UTC] — User: connor.blake (assoc_100212)
-- Auditing table storage size for fact_orders in dataset.
SELECT 
    table_name,
    size_bytes / (1024*1024) as size_mb
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.TABLE_STORAGE`
WHERE table_name = 'fact_orders';

### [2026-02-01 18:35:20 UTC] — User: wei.hartono (assoc_100210)
-- Checking dim_experiment status counts for running experiments.
SELECT 
    experiment_id,
    experiment_name,
    vertical_code,
    start_date
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment`
WHERE status = 'running';

### [2026-02-01 20:10:11 UTC] — User: amara.shah (assoc_100211)
-- Running marketplace seller performance summary for resold category focus.
SELECT 
    seller_id,
    active_listings,
    trailing_90d_gmv_usd,
    return_rate
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
WHERE category_focus = 'resold'
ORDER BY trailing_90d_gmv_usd DESC
LIMIT 10;

### [2026-02-01 21:45:00 UTC] — User: tara.oduya (assoc_100140)
-- Checking fulfillment speed daily average cost trends by fulfillment type.
SELECT 
    fulfillment_type,
    ROUND(AVG(avg_cost_per_order_usd), 2) as mean_cost
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
GROUP BY 1;

### [2026-02-01 23:20:33 UTC] — User: giulia.romano (assoc_100213)
-- Checking member cltv lifetime gmv distribution for annual plan members.
SELECT 
    m.plan_type,
    ROUND(AVG(c.lifetime_gmv_usd), 2) as avg_lifetime_gmv,
    ROUND(AVG(c.lifetime_orders), 1) as avg_lifetime_orders
FROM `nexus-analyst-demo.acme_ecomm.dim_member` m
JOIN `nexus-analyst-demo.acme_ecomm.member_cltv` c ON m.member_id = c.member_id
GROUP BY 1;

### [2026-02-02 01:10:14 UTC] — User: connor.blake (assoc_100212)
-- Verifying primary key uniqueness on dim_fulfillment_node table.
SELECT 
    node_id,
    COUNT(*) as cnt
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
GROUP BY 1
HAVING cnt > 1;

### [2026-02-02 02:45:50 UTC] — User: wei.hartono (assoc_100210)
-- Auditing traffic conversion summary by market for Q4FY26 weeks.
SELECT 
    fiscal_week_ending,
    market,
    sessions,
    orders,
    conversion_rate
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'US'
  AND fiscal_week_ending >= '2025-11-01'
ORDER BY fiscal_week_ending DESC
LIMIT 5;

### [2026-02-02 04:20:05 UTC] — User: amara.shah (assoc_100211)
-- Monthly summary of marketplace listings by status and category.
SELECT 
    category,
    status,
    authenticity_verified,
    COUNT(*) as listing_count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY 1, 2, 3;

### [2026-02-02 05:55:18 UTC] — User: tara.oduya (assoc_100140)
-- Checking care contacts channel share across bot and human channels.
SELECT 
    channel,
    deflected,
    COUNT(*) as contact_count
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1, 2;

### [2026-02-02 07:30:40 UTC] — User: giulia.romano (assoc_100213)
-- Checking member cltv tenure distribution for member_id mem_1000178.
SELECT 
    member_id,
    tenure_days,
    trailing_12mo_gmv_usd,
    is_active
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`
WHERE member_id = 'mem_1000178';

### [2026-02-02 09:05:12 UTC] — User: connor.blake (assoc_100212)
-- Checking partition metadata for traffic_conversion_summary.
SELECT 
    table_name,
    partition_id
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'traffic_conversion_summary';

### [2026-02-02 10:40:22 UTC] — User: wei.hartono (assoc_100210)
-- Testing query performance on fact_experiment_exposures totals.
SELECT 
    experiment_id,
    variant,
    SUM(units_assigned) as total_assigned,
    SUM(units_exposed) as total_exposed
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures`
GROUP BY 1, 2;

### [2026-02-02 12:15:00 UTC] — User: amara.shah (assoc_100211)
-- Running reconciliation query for membership events by event_type.
SELECT 
    event_type,
    COUNT(*) as event_count
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
GROUP BY 1;

### [2026-02-02 13:50:33 UTC] — User: tara.oduya (assoc_100140)
-- Checking fulfillment speed daily metrics for ship_to_home fulfillment type.
SELECT 
    date,
    on_time_rate,
    avg_cost_per_order_usd
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE fulfillment_type = 'ship_to_home'
  AND date >= '2026-01-01'
ORDER BY date DESC
LIMIT 10;

### [2026-02-02 15:25:45 UTC] — User: giulia.romano (assoc_100213)
-- Extracting voc responses with theme tag about shipping or fulfillment.
SELECT 
    response_id,
    theme_tag,
    SUBSTR(verbatim_text, 1, 90) as text_snippet
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE theme_tag LIKE '%ship%'
LIMIT 10;

### [2026-02-02 17:00:10 UTC] — User: connor.blake (assoc_100212)
-- Auditing foreign key references between fact_orders and dim_member.
SELECT 
    o.order_id,
    o.member_id
FROM `nexus-analyst-demo.acme_ecomm.fact_orders` o
LEFT JOIN `nexus-analyst-demo.acme_ecomm.dim_member` m ON o.member_id = m.member_id
WHERE o.member_id IS NOT NULL 
  AND m.member_id IS NULL
LIMIT 5;

### [2026-02-02 18:35:50 UTC] — User: wei.hartono (assoc_100210)
-- Auditing dim_seller table status distribution across categories.
SELECT 
    category_focus,
    status,
    COUNT(*) as seller_count
FROM `nexus-analyst-demo.acme_ecomm.dim_seller`
GROUP BY 1, 2;

### [2026-02-02 20:10:04 UTC] — User: amara.shah (assoc_100211)
-- Pulling marketplace seller performance for collectibles category focus.
SELECT 
    seller_id,
    active_listings,
    trailing_90d_gmv_usd,
    authenticity_flag_count
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
WHERE category_focus = 'collectibles'
ORDER BY trailing_90d_gmv_usd DESC
LIMIT 5;

### [2026-02-02 21:45:22 UTC] — User: tara.oduya (assoc_100140)
-- Checking promise vs actual delivery metrics for market CA.
SELECT 
    date,
    orders_promised,
    orders_on_time,
    avg_days_late_when_late
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE market = 'CA'
  AND date >= '2026-01-01'
ORDER BY date DESC
LIMIT 10;

### [2026-02-02 23:20:15 UTC] — User: giulia.romano (assoc_100213)
-- Checking care contacts sub_program distribution and CSAT scores.
SELECT 
    sub_program,
    COUNT(*) as contact_count,
    ROUND(AVG(CAST(csat_score AS NUMERIC)), 2) as avg_csat
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1;

### [2026-02-03 01:05:30 UTC] — User: connor.blake (assoc_100212)
-- Checking table schema definition for fact_care_contacts table.
SELECT 
    column_name,
    data_type,
    is_nullable
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'fact_care_contacts';

### [2026-02-03 02:40:11 UTC] — User: wei.hartono (assoc_100210)
-- Testing query performance on fact_traffic_daily grouped by vertical.
SELECT 
    vertical_code,
    SUM(sessions) as total_sessions,
    SUM(gmv_usd) as total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
GROUP BY 1;

### [2026-02-03 04:15:44 UTC] — User: amara.shah (assoc_100211)
-- Running monthly reconciliation query for total orders in fact_traffic_daily.
SELECT 
    FORMAT_DATE('%Y-%m', date) as month,
    SUM(orders) as total_orders
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date >= '2025-11-01'
GROUP BY 1
ORDER BY 1;

### [2026-02-03 05:50:02 UTC] — User: tara.oduya (assoc_100140)
-- Checking fulfillment speed daily cost trends for fulfillment types.
SELECT 
    fulfillment_type,
    ROUND(AVG(avg_cost_per_order_usd), 2) as avg_cost
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
GROUP BY 1;

### [2026-02-03 07:25:33 UTC] — User: giulia.romano (assoc_100213)
-- Checking member cltv tenure distribution across all panel members.
SELECT 
    TENURE_DAYS / 365 as tenure_years,
    COUNT(*) as member_count
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`
GROUP BY 1
ORDER BY tenure_years DESC
LIMIT 10;

### [2026-02-03 09:00:19 UTC] — User: connor.blake (assoc_100212)
-- Verifying primary key uniqueness on dim_vertical table.
SELECT 
    vertical_code,
    sub_vertical_code,
    COUNT(*) as cnt
FROM `nexus-analyst-demo.acme_ecomm.dim_vertical`
GROUP BY 1, 2
HAVING cnt > 1;

### [2026-02-03 10:35:40 UTC] — User: wei.hartono (assoc_100210)
-- Auditing dim_experiment table status counts.
SELECT 
    status,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment`
GROUP BY status;

### [2026-02-03 12:10:05 UTC] — User: amara.shah (assoc_100211)
-- Pulling marketplace seller performance metrics for collectibles category.
SELECT 
    seller_id,
    active_listings,
    trailing_90d_gmv_usd,
    return_rate
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
WHERE category_focus = 'collectibles'
ORDER BY trailing_90d_gmv_usd DESC
LIMIT 10;

### [2026-02-03 13:45:22 UTC] — User: tara.oduya (assoc_100140)
-- Checking fulfillment speed daily cost trends for ship_to_home.
SELECT 
    date,
    avg_cost_per_order_usd
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE fulfillment_type = 'ship_to_home'
  AND date >= '2026-01-01'
ORDER BY date DESC
LIMIT 10;

### [2026-02-03 15:20:11 UTC] — User: giulia.romano (assoc_100213)
-- Checking care deflection daily rates for member_care sub_program.
SELECT 
    date,
    deflection_rate,
    contact_volume
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
WHERE sub_program = 'member_care'
  AND date >= '2026-01-01'
ORDER BY date DESC
LIMIT 10;

### [2026-02-03 16:55:40 UTC] — User: connor.blake (assoc_100212)
-- Checking storage footprint for fact_orders table in database.
SELECT 
    table_name,
    size_bytes / (1024*1024) as size_mb
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.TABLE_STORAGE`
WHERE table_name = 'fact_orders';

### [2026-02-03 18:30:15 UTC] — User: wei.hartono (assoc_100210)
-- Testing query performance on traffic_conversion_summary for Q4FY26.
SELECT 
    fiscal_week_ending,
    SUM(sessions) as total_sessions,
    SUM(orders) as total_orders
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE fiscal_week_ending >= '2025-11-01'
GROUP BY 1
ORDER BY fiscal_week_ending;

### [2026-02-03 20:05:08 UTC] — User: amara.shah (assoc_100211)
-- Running marketplace gmv summary check for style sub_vertical.
SELECT 
    fiscal_week_ending,
    gmv_usd,
    orders,
    take_rate
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE sub_vertical_code = 'STYLE'
ORDER BY fiscal_week_ending DESC
LIMIT 5;

### [2026-02-03 21:40:22 UTC] — User: tara.oduya (assoc_100140)
-- Checking promise vs actual performance across fulfillment types for Q4FY26.
SELECT 
    fulfillment_type,
    SUM(orders_promised) as promised,
    SUM(orders_on_time) as on_time
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE date BETWEEN '2025-11-01' AND '2026-01-31'
GROUP BY 1;

### [2026-02-03 23:15:50 UTC] — User: giulia.romano (assoc_100213)
-- Checking voc responses distribution by survey_type.
SELECT 
    survey_type,
    COUNT(*) as count,
    ROUND(AVG(score), 2) as avg_score
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
GROUP BY 1;

### [2026-02-04 01:00:12 UTC] — User: connor.blake (assoc_100212)
-- Auditing foreign key references between fact_care_contacts and dim_member.
SELECT 
    c.contact_id,
    c.member_id
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts` c
LEFT JOIN `nexus-analyst-demo.acme_ecomm.dim_member` m ON c.member_id = m.member_id
WHERE c.member_id IS NOT NULL 
  AND m.member_id IS NULL
LIMIT 5;

### [2026-02-04 02:35:30 UTC] — User: wei.hartono (assoc_100210)
-- Checking dim_associate table active status count by role.
SELECT 
    role,
    is_active,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
GROUP BY 1, 2;

### [2026-02-04 04:10:04 UTC] — User: amara.shah (assoc_100211)
-- Pulling marketplace seller performance for sel_500061.
SELECT 
    seller_id,
    category_focus,
    active_listings,
    trailing_90d_gmv_usd,
    return_rate
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
WHERE seller_id = 'sel_500061';

### [2026-02-04 05:45:20 UTC] — User: tara.oduya (assoc_100140)
-- Checking fulfillment speed daily metrics for fulfillment_type = 'ship_to_home'.
SELECT 
    date,
    on_time_rate,
    pct_of_total_orders
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE fulfillment_type = 'ship_to_home'
  AND date >= '2026-01-15'
ORDER BY date DESC;

### [2026-02-04 07:20:50 UTC] — User: giulia.romano (assoc_100213)
-- Checking member cltv lifetime orders and lifetime gmv for plan_type = 'monthly'.
SELECT 
    plan_type,
    ROUND(AVG(lifetime_orders), 1) as avg_orders,
    ROUND(AVG(lifetime_gmv_usd), 2) as avg_gmv
FROM `nexus-analyst-demo.acme_ecomm.dim_member` m
JOIN `nexus-analyst-demo.acme_ecomm.member_cltv` c ON m.member_id = c.member_id
WHERE m.plan_type = 'monthly'
GROUP BY 1;

### [2026-02-04 08:55:11 UTC] — User: connor.blake (assoc_100212)
-- Verifying partition freshness for fact_traffic_daily table.
SELECT 
    MAX(date) as latest_date,
    COUNT(*) as row_count
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`;

### [2026-02-04 10:30:25 UTC] — User: wei.hartono (assoc_100210)
-- Testing query execution on fact_experiment_readouts for specific experiment.
SELECT 
    metric_name,
    metric_value,
    lift_vs_control_pct,
    is_significant
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`
WHERE experiment_id = 'exp_2401';

### [2026-02-04 12:05:40 UTC] — User: amara.shah (assoc_100211)
-- Running summary query for marketplace listings authenticity verification.
SELECT 
    category,
    authenticity_verified,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY 1, 2;

### [2026-02-04 13:40:19 UTC] — User: tara.oduya (assoc_100140)
-- Checking care deflection daily rates for optimize sub_program.
SELECT 
    date,
    deflection_rate,
    avg_csat_deflected
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
WHERE sub_program = 'optimize'
  AND date >= '2026-01-01'
ORDER BY date DESC
LIMIT 10;

### [2026-02-04 15:15:00 UTC] — User: giulia.romano (assoc_100213)
-- Checking member cltv benefits adopted count distribution.
SELECT 
    benefits_adopted_count,
    COUNT(*) as member_count
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`
GROUP BY 1
ORDER BY benefits_adopted_count;

### [2026-02-04 16:50:33 UTC] — User: connor.blake (assoc_100212)
-- Checking storage footprint for fact_care_contacts in INFORMATION_SCHEMA.
SELECT 
    table_name,
    size_bytes / (1024*1024) as size_mb
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.TABLE_STORAGE`
WHERE table_name = 'fact_care_contacts';

### [2026-02-04 18:25:12 UTC] — User: wei.hartono (assoc_100210)
-- Auditing dim_marketing_calendar event types and planned spend.
SELECT 
    event_type,
    SUM(planned_spend_usd) as total_planned_spend
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
GROUP BY 1;

### [2026-02-04 20:00:45 UTC] — User: amara.shah (assoc_100211)
-- Pulling marketplace seller performance for sel_500089.
SELECT 
    seller_id,
    category_focus,
    active_listings,
    trailing_90d_gmv_usd,
    return_rate
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
WHERE seller_id = 'sel_500089';

### [2026-02-04 21:35:10 UTC] — User: tara.oduya (assoc_100140)
-- Checking fulfillment speed daily metrics for node comparisons.
SELECT 
    date,
    fulfillment_type,
    avg_cost_per_order_usd
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE date >= '2026-01-20'
ORDER BY date DESC
LIMIT 10;

### [2026-02-04 23:10:55 UTC] — User: giulia.romano (assoc_100213)
-- Checking member membership events for signup event_type.
SELECT 
    channel,
    COUNT(*) as signup_count
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
WHERE event_type = 'signup'
GROUP BY 1;

### [2026-02-04 23:45:12 UTC] — User: connor.blake (assoc_100212)
-- Verifying partition filter compliance for fact_orders in BigQuery.
SELECT 
    table_id,
    partition_id,
    row_count
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'fact_orders'
ORDER BY partition_id DESC
LIMIT 15;

### [2026-02-05 08:12:30 UTC] — User: wei.hartono (assoc_100210)
-- Checking daily ingestion row counts for fact_traffic_daily across all markets.
SELECT 
    date,
    market,
    SUM(sessions) as total_sessions
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date >= '2026-01-01'
GROUP BY 1, 2
ORDER BY date DESC, market
LIMIT 12;

### [2026-02-05 09:30:44 UTC] — User: amara.shah (assoc_100211)
-- Pulling marketplace gmv summary for recent weekly rollups.
SELECT 
    fiscal_week_ending,
    sub_vertical_code,
    gmv_usd
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE fiscal_week_ending >= '2026-01-01'
ORDER BY fiscal_week_ending DESC
LIMIT 10;

### [2026-02-05 11:15:20 UTC] — User: giulia.romano (assoc_100213)
-- Auditing care contact resolution codes for automated sub-programs.
SELECT 
    resolution_code,
    COUNT(*) as contact_count
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE sub_program = 'automate'
GROUP BY 1
ORDER BY contact_count DESC;

### [2026-02-05 13:40:15 UTC] — User: tara.oduya (assoc_100140)
-- Checking fulfillment node types and active statuses.
SELECT 
    node_type,
    COUNT(*) as node_count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
GROUP BY 1;

### [2026-02-05 15:05:50 UTC] — User: connor.blake (assoc_100212)
-- Checking dataset table storage sizes in bytes.
SELECT 
    table_name,
    total_rows,
    size_bytes
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.TABLE_STORAGE`
ORDER BY size_bytes DESC;

### [2026-02-05 17:22:10 UTC] — User: wei.hartono (assoc_100210)
-- Validating experiment assignment dates against dim_experiment.
SELECT 
    experiment_id,
    start_date,
    end_date,
    status
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment`
WHERE status = 'running';

### [2026-02-05 19:10:33 UTC] — User: amara.shah (assoc_100211)
-- Checking seller performance metrics for top trailing GMV rows.
SELECT 
    seller_id,
    trailing_90d_gmv_usd,
    active_listings
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
ORDER BY trailing_90d_gmv_usd DESC
LIMIT 10;

### [2026-02-05 21:04:18 UTC] — User: giulia.romano (assoc_100213)
-- Pulling member cltv projections for annual plan holders.
SELECT 
    plan_type,
    AVG(projected_cltv_usd) as avg_projected_cltv
FROM `nexus-analyst-demo.acme_ecomm.member_cltv` mc
JOIN `nexus-analyst-demo.acme_ecomm.dim_member` dm ON mc.member_id = dm.member_id
GROUP BY 1;

### [2026-02-06 08:30:00 UTC] — User: tara.oduya (assoc_100140)
-- Checking promise vs actual performance by fulfillment type.
SELECT 
    fulfillment_type,
    SUM(orders_promised) as total_promised,
    SUM(orders_on_time) as total_ontime
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE date >= '2026-01-01'
GROUP BY 1;

### [2026-02-06 10:15:45 UTC] — User: wei.hartono (assoc_100210)
-- Verifying traffic summary mart aggregation consistency.
SELECT 
    fiscal_week_ending,
    market,
    SUM(sessions) as mart_sessions
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
GROUP BY 1, 2
ORDER BY fiscal_week_ending DESC
LIMIT 5;

### [2026-02-06 12:40:12 UTC] — User: connor.blake (assoc_100212)
-- Checking dataset view definitions for information schema.
SELECT 
    table_name,
    view_definition
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.VIEWS`
LIMIT 5;

### [2026-02-06 14:20:55 UTC] — User: amara.shah (assoc_100211)
-- Pulling order returns distribution by reason code.
SELECT 
    return_reason_code,
    COUNT(*) as return_count
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE is_returned = TRUE
GROUP BY 1
ORDER BY return_count DESC;

### [2026-02-06 16:55:20 UTC] — User: giulia.romano (assoc_100213)
-- Checking vocational survey scores distribution for post-purchase.
SELECT 
    score,
    COUNT(*) as response_count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE survey_type = 'post_purchase'
GROUP BY 1
ORDER BY score DESC;

### [2026-02-06 18:30:10 UTC] — User: tara.oduya (assoc_100140)
-- Auditing fulfillment speed daily cost metrics.
SELECT 
    date,
    fulfillment_type,
    avg_cost_per_order_usd
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE date >= '2026-01-01'
ORDER BY date DESC
LIMIT 8;

### [2026-02-06 20:12:35 UTC] — User: wei.hartono (assoc_100210)
-- Inspecting dim_associate active headcount by team.
SELECT 
    team,
    COUNT(*) as active_count
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
WHERE is_active = TRUE
GROUP BY 1;

### [2026-02-07 09:05:00 UTC] — User: amara.shah (assoc_100211)
-- Checking member acquisition channels for panel distribution.
SELECT 
    acquisition_channel,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
GROUP BY 1;

### [2026-02-07 11:22:40 UTC] — User: connor.blake (assoc_100212)
-- Checking table constraints and options in INFORMATION_SCHEMA.
SELECT 
    table_name,
    option_name,
    option_value
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.TABLE_OPTIONS`
LIMIT 10;

### [2026-02-07 13:45:15 UTC] — User: giulia.romano (assoc_100213)
-- Checking care contact channels distribution.
SELECT 
    channel,
    COUNT(*) as volume
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1;

### [2026-02-07 15:30:22 UTC] — User: wei.hartono (assoc_100210)
-- Pulling marketing calendar events for promotional category.
SELECT 
    event_name,
    start_date,
    end_date
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
WHERE event_type = 'promo';

### [2026-02-07 17:15:50 UTC] — User: tara.oduya (assoc_100140)
-- Checking Marketplace listings authenticity status counts.
SELECT 
    authenticity_verified,
    COUNT(*) as listing_count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY 1;

### [2026-02-09 08:40:10 UTC] — User: amara.shah (assoc_100211)
-- Reviewing member cltv benefits adopted count groupings.
SELECT 
    benefits_adopted_count,
    AVG(lifetime_gmv_usd) as avg_lifetime_gmv
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`
GROUP BY 1
ORDER BY benefits_adopted_count;

### [2026-02-09 10:25:33 UTC] — User: wei.hartono (assoc_100210)
-- Validating traffic sessions definition version counts in fact_traffic_daily.
SELECT 
    sessions_definition_version,
    COUNT(*) as row_count
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
GROUP BY 1;

### [2026-02-09 12:15:18 UTC] — User: connor.blake (assoc_100212)
-- Checking routine schema definitions in INFORMATION_SCHEMA.
SELECT 
    routine_name,
    routine_type
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.ROUTINES`;

### [2026-02-09 14:05:40 UTC] — User: giulia.romano (assoc_100213)
-- Pulling care deflection daily summary for sub_program optimize.
SELECT 
    date,
    deflection_rate,
    avg_csat_deflected
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
WHERE sub_program = 'optimize'
ORDER BY date DESC
LIMIT 5;

### [2026-02-09 16:50:25 UTC] — User: tara.oduya (assoc_100140)
-- Checking marketplace seller performance category focus split.
SELECT 
    category_focus,
    COUNT(*) as seller_count,
    AVG(return_rate) as avg_return_rate
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
GROUP BY 1;

### [2026-02-09 18:30:12 UTC] — User: amara.shah (assoc_100211)
-- Pulling order volume by fulfillment type.
SELECT 
    fulfillment_type,
    COUNT(*) as order_count,
    SUM(gmv_usd) as total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
GROUP BY 1;

### [2026-02-10 09:15:00 UTC] — User: wei.hartono (assoc_100210)
-- Checking dim_date flags for peak holiday weeks.
SELECT 
    fiscal_year,
    fiscal_quarter,
    COUNT(*) as peak_days
FROM `nexus-analyst-demo.acme_ecomm.dim_date`
WHERE is_peak_holiday = TRUE
GROUP BY 1, 2;

### [2026-02-10 11:05:30 UTC] — User: connor.blake (assoc_100212)
-- Checking table columns metadata in INFORMATION_SCHEMA.
SELECT 
    column_name,
    data_type
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'fact_orders'
LIMIT 10;

### [2026-02-10 13:40:15 UTC] — User: giulia.romano (assoc_100213)
-- Checking membership event types distribution.
SELECT 
    event_type,
    COUNT(*) as event_count
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
GROUP BY 1;

### [2026-02-10 15:20:44 UTC] — User: tara.oduya (assoc_100140)
-- Auditing fulfillment speed daily pct of total orders.
SELECT 
    date,
    fulfillment_type,
    pct_of_total_orders
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE date >= '2026-01-01'
ORDER BY date DESC
LIMIT 6;

### [2026-02-10 17:10:11 UTC] — User: amara.shah (assoc_100211)
-- Pulling experiment readouts for metric name gmv.
SELECT 
    experiment_id,
    variant,
    metric_value,
    is_significant
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`
WHERE metric_name LIKE '%gmv%'
LIMIT 10;

### [2026-02-11 08:50:20 UTC] — User: wei.hartono (assoc_100210)
-- Checking dim_vertical depth classifications.
SELECT 
    vertical_code,
    vertical_name,
    is_deep_dive
FROM `nexus-analyst-demo.acme_ecomm.dim_vertical`
WHERE is_deep_dive = TRUE;

### [2026-02-11 10:30:15 UTC] — User: connor.blake (assoc_100212)
-- Checking table privileges in INFORMATION_SCHEMA.
SELECT 
    table_name,
    privilege_type
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.TABLE_PRIVILEGES`
LIMIT 10;

### [2026-02-11 12:15:40 UTC] — User: giulia.romano (assoc_100213)
-- Pulling voc responses survey type breakdown.
SELECT 
    survey_type,
    COUNT(*) as total_responses
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
GROUP BY 1;

### [2026-02-11 14:45:10 UTC] — User: tara.oduya (assoc_100140)
-- Checking marketplace listings status counts.
SELECT 
    status,
    COUNT(*) as listing_count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY 1;

### [2026-02-11 16:20:35 UTC] — User: amara.shah (assoc_100211)
-- Pulling traffic conversion summary weekly aggregates.
SELECT 
    fiscal_week_ending,
    market,
    conversion_rate
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'US'
ORDER BY fiscal_week_ending DESC
LIMIT 8;

### [2026-02-12 09:10:00 UTC] — User: wei.hartono (assoc_100210)
-- Auditing dim_seller panel counts by status.
SELECT 
    status,
    COUNT(*) as seller_count
FROM `nexus-analyst-demo.acme_ecomm.dim_seller`
GROUP BY 1;

### [2026-02-12 11:05:22 UTC] — User: connor.blake (assoc_100212)
-- Checking table row counts via INFORMATION_SCHEMA.
SELECT 
    table_name,
    row_count
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.TABLE_STORAGE`
WHERE table_name LIKE 'fact_%';

### [2026-02-12 13:30:45 UTC] — User: giulia.romano (assoc_100213)
-- Checking care contacts duration and csat distribution.
SELECT 
    csat_score,
    AVG(handle_time_minutes) as avg_handle_time
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1
ORDER BY csat_score;

### [2026-02-12 15:15:10 UTC] — User: tara.oduya (assoc_100140)
-- Checking promise vs actual avg days late metrics.
SELECT 
    fulfillment_type,
    AVG(avg_days_late_when_late) as avg_days_late
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
GROUP BY 1;

### [2026-02-12 17:40:55 UTC] — User: amara.shah (assoc_100211)
-- Pulling member cltv stats for active plan holders.
SELECT 
    status,
    AVG(trailing_12mo_gmv_usd) as avg_trailing_gmv
FROM `nexus-analyst-demo.acme_ecomm.member_cltv` mc
JOIN `nexus-analyst-demo.acme_ecomm.dim_member` dm ON mc.member_id = dm.member_id
GROUP BY 1;

### [2026-02-13 08:35:12 UTC] — User: wei.hartono (assoc_100210)
-- Checking experiment exposures units assigned sum.
SELECT 
    experiment_id,
    SUM(units_assigned) as total_assigned,
    SUM(units_exposed) as total_exposed
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures`
GROUP BY 1
LIMIT 5;

### [2026-02-13 10:20:40 UTC] — User: connor.blake (assoc_100212)
-- Checking external tables schema in INFORMATION_SCHEMA.
SELECT 
    table_name,
    file_format
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.EXTERNAL_TABLES`;

### [2026-02-13 12:10:15 UTC] — User: giulia.romano (assoc_100213)
-- Pulling voc sentiment distribution for survey results.
SELECT 
    sentiment,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
GROUP BY 1;

### [2026-02-13 14:55:30 UTC] — User: tara.oduya (assoc_100140)
-- Checking marketplace gmv summary take rate values.
SELECT 
    sub_vertical_code,
    AVG(take_rate) as avg_take_rate
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
GROUP BY 1;

### [2026-02-13 16:40:22 UTC] — User: amara.shah (assoc_100211)
-- Pulling fulfillment speed daily metrics for node comparisons.
SELECT 
    date,
    fulfillment_type,
    on_time_rate
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE date >= '2026-01-01'
ORDER BY date DESC
LIMIT 5;

### [2026-02-16 09:00:15 UTC] — User: wei.hartono (assoc_100210)
-- Checking dim_associate roles distribution.
SELECT 
    role,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
GROUP BY 1;

### [2026-02-16 11:15:33 UTC] — User: connor.blake (assoc_100212)
-- Checking dataset clustering information in INFORMATION_SCHEMA.
SELECT 
    table_name,
    clustering_ordinal_position,
    column_name
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.COLUMNS`
WHERE clustering_ordinal_position IS NOT NULL
LIMIT 10;

### [2026-02-16 13:40:50 UTC] — User: giulia.romano (assoc_100213)
-- Checking member cltv benefits adopted count distribution.
SELECT 
    benefits_adopted_count,
    COUNT(*) as member_count
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`
GROUP BY 1
ORDER BY benefits_adopted_count;

### [2026-02-16 15:22:10 UTC] — User: tara.oduya (assoc_100140)
-- Checking traffic conversion summary for Mexico market.
SELECT 
    fiscal_week_ending,
    conversion_rate,
    gmv_usd
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'MX'
ORDER BY fiscal_week_ending DESC
LIMIT 5;

### [2026-02-16 17:05:40 UTC] — User: amara.shah (assoc_100211)
-- Pulling care deflection daily summary for sub_program automate.
SELECT 
    date,
    deflection_rate,
    contact_volume
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
WHERE sub_program = 'automate'
ORDER BY date DESC
LIMIT 5;

### [2026-02-17 08:30:00 UTC] — User: wei.hartono (assoc_100210)
-- Auditing dim_marketing_calendar planned spend by market.
SELECT 
    market,
    SUM(planned_spend_usd) as total_planned_spend
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
GROUP BY 1;

### [2026-02-17 10:20:15 UTC] — User: connor.blake (assoc_100212)
-- Checking view columns metadata in INFORMATION_SCHEMA.
SELECT 
    table_name,
    column_name
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.VIEW_COLUMNS`
LIMIT 10;

### [2026-02-17 12:45:22 UTC] — User: giulia.romano (assoc_100213)
-- Checking marketplace seller performance return rate averages.
SELECT 
    category_focus,
    AVG(return_rate) as avg_return_rate
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
GROUP BY 1;

### [2026-02-17 14:30:10 UTC] — User: tara.oduya (assoc_100140)
-- Pulling order fulfillment types and shipping methods.
SELECT 
    fulfillment_type,
    channel,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
GROUP BY 1, 2;

### [2026-02-17 16:15:55 UTC] — User: amara.shah (assoc_100211)
-- Checking fact_orders refund status for recent orders.
SELECT 
    is_returned,
    COUNT(*) as count,
    SUM(refund_usd) as total_refunds
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE is_returned = TRUE
GROUP BY 1;

### [2026-02-18 09:10:30 UTC] — User: wei.hartono (assoc_100210)
-- Validating traffic daily sessions by device type.
SELECT 
    device,
    SUM(sessions) as total_sessions
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
GROUP BY 1;

### [2026-02-18 11:05:44 UTC] — User: connor.blake (assoc_100212)
-- Checking snapshot tables storage in INFORMATION_SCHEMA.
SELECT 
    table_name,
    size_bytes
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.TABLE_STORAGE`
WHERE table_name LIKE '%summary%';

### [2026-02-18 13:20:12 UTC] — User: giulia.romano (assoc_100213)
-- Checking member cltv tenure distribution.
SELECT 
    tenure_days,
    COUNT(*) as member_count
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`
GROUP BY 1
ORDER BY tenure_days DESC
LIMIT 10;

### [2026-02-18 15:50:20 UTC] — User: tara.oduya (assoc_100140)
-- Checking fulfillment speed daily cost per order.
SELECT 
    fulfillment_type,
    AVG(avg_cost_per_order_usd) as mean_cost
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
GROUP BY 1;

### [2026-02-18 17:35:15 UTC] — User: amara.shah (assoc_100211)
-- Pulling marketplace gmv summary for sub_vertical breakdowns.
SELECT 
    sub_vertical_code,
    SUM(gmv_usd) as total_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
GROUP BY 1;

### [2026-02-19 08:45:00 UTC] — User: wei.hartono (assoc_100210)
-- Auditing dim_fulfillment_node active flags by node type.
SELECT 
    node_type,
    is_active,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
GROUP BY 1, 2;

### [2026-02-19 10:30:25 UTC] — User: connor.blake (assoc_100212)
-- Checking dataset table creation times in INFORMATION_SCHEMA.
SELECT 
    table_name,
    creation_time
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.TABLES`;

### [2026-02-19 12:15:50 UTC] — User: giulia.romano (assoc_100213)
-- Checking care contacts closed status and resolutions.
SELECT 
    resolution_code,
    AVG(csat_score) as avg_csat
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1;

### [2026-02-19 14:40:10 UTC] — User: tara.oduya (assoc_100140)
-- Checking promise vs actual performance by market.
SELECT 
    market,
    SUM(orders_promised) as promised,
    SUM(orders_on_time) as on_time
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
GROUP BY 1;

### [2026-02-19 16:25:33 UTC] — User: amara.shah (assoc_100211)
-- Pulling member cltv metrics for plan type annual.
SELECT 
    plan_type,
    COUNT(*) as member_count,
    AVG(lifetime_gmv_usd) as avg_gmv
FROM `nexus-analyst-demo.acme_ecomm.member_cltv` mc
JOIN `nexus-analyst-demo.acme_ecomm.dim_member` dm ON mc.member_id = dm.member_id
GROUP BY 1;

### [2026-02-20 09:12:15 UTC] — User: wei.hartono (assoc_100210)
-- Checking traffic daily metrics for US market.
SELECT 
    date,
    SUM(sessions) as total_sessions,
    SUM(orders) as total_orders
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE market = 'US'
GROUP BY 1
ORDER BY date DESC
LIMIT 5;

### [2026-02-20 11:05:40 UTC] — User: connor.blake (assoc_100212)
-- Checking dataset storage billing tier info in INFORMATION_SCHEMA.
SELECT 
    table_name,
    row_count,
    size_bytes / (1024*1024) as size_mb
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.TABLE_STORAGE`
ORDER BY size_bytes DESC
LIMIT 5;

### [2026-02-20 13:30:22 UTC] — User: giulia.romano (assoc_100213)
-- Checking voc responses theme tag distributions.
SELECT 
    theme_tag,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
GROUP BY 1
ORDER BY count DESC
LIMIT 10;

### [2026-02-20 15:55:10 UTC] — User: tara.oduya (assoc_100140)
-- Checking marketplace seller performance avg buyer ratings.
SELECT 
    category_focus,
    AVG(avg_buyer_rating) as mean_rating
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
GROUP BY 1;

### [2026-02-20 17:20:45 UTC] — User: amara.shah (assoc_100211)
-- Pulling traffic conversion summary for Canada market.
SELECT 
    fiscal_week_ending,
    conversion_rate,
    gmv_usd
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'CA'
ORDER BY fiscal_week_ending DESC
LIMIT 5;

### [2026-02-20 18:05:11 UTC] — User: connor.blake (assoc_100212)
-- Investigating daily partition size distribution for fact_orders table.
SELECT 
    order_date,
    COUNT(*) as row_count,
    SUM(gmv_usd) as daily_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
GROUP BY 1
ORDER BY order_date DESC
LIMIT 10;

### [2026-02-20 19:40:02 UTC] — User: giulia.romano (assoc_100213)
-- Pulling care contact distribution by channel for Q4.
SELECT 
    channel,
    COUNT(*) as contact_count,
    AVG(handle_time_minutes) as avg_handle_time
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at >= '2025-11-01' AND opened_at < '2026-02-01'
GROUP BY 1;

### [2026-02-21 08:22:10 UTC] — User: amara.shah (assoc_100211)
-- Reconciling marketplace GMV summary against raw order cuts for Q3.
SELECT 
    sub_vertical_code,
    SUM(gmv_usd) as mart_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE fiscal_week_ending BETWEEN '2025-08-01' AND '2025-10-31'
GROUP BY 1;

### [2026-02-21 10:15:33 UTC] — User: wei.hartono (assoc_100210)
-- Checking table partitioning scheme on fact_traffic_daily.
SELECT 
    table_name,
    partition_id,
    total_rows
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'fact_traffic_daily'
ORDER BY partition_id DESC
LIMIT 7;

### [2026-02-21 11:50:18 UTC] — User: tara.oduya (assoc_100140)
-- Checking fulfillment speed daily metrics for store delivery-from-store channel.
SELECT 
    date,
    market,
    on_time_rate,
    avg_cost_per_order_usd
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE fulfillment_type = 'dfs'
ORDER BY date DESC
LIMIT 5;

### [2026-02-21 14:05:49 UTC] — User: giulia.romano (assoc_100213)
-- Pulling VOC scores grouped by CSAT survey type.
SELECT 
    score_type,
    COUNT(*) as response_count,
    AVG(score) as avg_score
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
GROUP BY 1;

### [2026-02-21 16:30:12 UTC] — User: connor.blake (assoc_100212)
-- Checking dataset table row counts for storage audit.
SELECT 
    table_name,
    row_count
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.TABLES`
ORDER BY row_count DESC;

### [2026-02-22 09:11:04 UTC] — User: amara.shah (assoc_100211)
-- Checking membership events distribution across event types.
SELECT 
    event_type,
    COUNT(*) as event_count
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
GROUP BY 1
ORDER BY event_count DESC;

### [2026-02-22 11:25:39 UTC] — User: wei.hartono (assoc_100210)
-- Pulling weekly conversion metrics for Canada market.
SELECT 
    fiscal_week_ending,
    sessions,
    orders,
    conversion_rate
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'CA'
ORDER BY fiscal_week_ending DESC
LIMIT 5;

### [2026-02-22 13:02:50 UTC] — User: tara.oduya (assoc_100140)
-- Checking promise vs actual performance for ship_to_home.
SELECT 
    date,
    market,
    SUM(orders_promised) as promised,
    SUM(orders_on_time) as on_time
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE fulfillment_type = 'ship_to_home'
GROUP BY 1, 2
ORDER BY date DESC
LIMIT 5;

### [2026-02-22 15:44:11 UTC] — User: giulia.romano (assoc_100213)
-- Pulling care contacts with negative CSAT scores.
SELECT 
    contact_id,
    sub_program,
    channel,
    csats_score
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE csat_score = 1
LIMIT 10;

### [2026-02-23 09:15:20 UTC] — User: amara.shah (assoc_100211)
-- Checking member plan type breakdown in panel.
SELECT 
    plan_type,
    status,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
GROUP BY 1, 2;

### [2026-02-23 11:02:45 UTC] — User: connor.blake (assoc_100212)
-- Verifying column metadata for marketplace listings.
SELECT 
    column_name,
    data_type
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'fact_marketplace_listings';

### [2026-02-23 14:10:33 UTC] — User: wei.hartono (assoc_100210)
-- Pulling daily traffic for Mexico market.
SELECT 
    date,
    device,
    SUM(sessions) as sessions,
    SUM(orders) as orders
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE market = 'MX'
GROUP BY 1, 2
ORDER BY date DESC
LIMIT 5;

### [2026-02-23 16:55:02 UTC] — User: tara.oduya (assoc_100140)
-- Checking fulfillment node metadata.
SELECT 
    node_type,
    market,
    COUNT(*) as node_count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
GROUP BY 1, 2;

### [2026-02-24 08:33:19 UTC] — User: giulia.romano (assoc_100213)
-- Checking voc responses sentiment breakdown.
SELECT 
    sentiment,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
GROUP BY 1;

### [2026-02-24 10:20:15 UTC] — User: amara.shah (assoc_100211)
-- Pulling CLTV summary metrics across cohort quarters.
SELECT 
    signup_cohort_quarter,
    COUNT(*) as members,
    AVG(lifetime_gmv_usd) as avg_lifetime_gmv
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`
GROUP BY 1
ORDER BY signup_cohort_quarter DESC;

### [2026-02-24 12:12:44 UTC] — User: connor.blake (assoc_100212)
-- Checking dataset view definitions in INFORMATION_SCHEMA.
SELECT 
    table_name,
    view_definition
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.VIEWS`;

### [2026-02-24 15:05:22 UTC] — User: wei.hartono (assoc_100210)
-- Pulling experiment readouts for active experiments.
SELECT 
    experiment_id,
    metric_name,
    metric_value,
    lift_vs_control_pct
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`
WHERE is_significant = TRUE
LIMIT 10;

### [2026-02-25 09:12:50 UTC] — User: tara.oduya (assoc_100140)
-- Checking seller performance return rates by category focus.
SELECT 
    category_focus,
    AVG(return_rate) as avg_return_rate,
    AVG(avg_buyer_rating) as avg_rating
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
GROUP BY 1;

### [2026-02-25 11:30:18 UTC] — User: giulia.romano (assoc_100213)
-- Pulling care deflection daily metrics by sub_program.
SELECT 
    sub_program,
    AVG(deflection_rate) as mean_deflection,
    AVG(avg_csat_deflected) as mean_csat
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
GROUP BY 1;

### [2026-02-25 14:02:11 UTC] — User: amara.shah (assoc_100211)
-- Pulling traffic conversion summary for US market across vertical codes.
SELECT 
    vertical_code,
    SUM(sessions) as total_sessions,
    SUM(gmv_usd) as total_gmv
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'US'
GROUP BY 1;

### [2026-02-25 16:45:09 UTC] — User: connor.blake (assoc_100212)
-- Checking table constraints and options in INFORMATION_SCHEMA.
SELECT 
    table_name,
    option_name,
    option_value
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.TABLE_OPTIONS`;

### [2026-02-26 08:15:30 UTC] — User: wei.hartono (assoc_100210)
-- Checking daily traffic definitions version distribution.
SELECT 
    sessions_definition_version,
    COUNT(*) as row_count,
    SUM(sessions) as sessions
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
GROUP BY 1;

### [2026-02-26 10:22:45 UTC] — User: tara.oduya (assoc_100140)
-- Pulling marketplace listings status breakdown.
SELECT 
    status,
    authenticity_verified,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY 1, 2;

### [2026-02-26 13:10:12 UTC] — User: giulia.romano (assoc_100213)
-- Pulling survey type breakdown from voc responses.
SELECT 
    survey_type,
    COUNT(*) as count,
    AVG(score) as avg_score
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
GROUP BY 1;

### [2026-02-26 15:33:50 UTC] — User: amara.shah (assoc_100211)
-- Checking marketing calendar events by event type.
SELECT 
    event_type,
    COUNT(*) as count,
    SUM(planned_spend_usd) as total_planned_spend
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
GROUP BY 1;

### [2026-02-27 09:04:15 UTC] — User: connor.blake (assoc_100212)
-- Checking dataset routine routines in INFORMATION_SCHEMA.
SELECT 
    routine_name,
    routine_type
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.ROUTINES`;

### [2026-02-27 11:20:38 UTC] — User: wei.hartono (assoc_100210)
-- Checking associate dimension active status counts.
SELECT 
    is_active,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
GROUP BY 1;

### [2026-02-27 14:05:02 UTC] — User: tara.oduya (assoc_100140)
-- Pulling fulfillment speed daily metrics grouped by market.
SELECT 
    market,
    AVG(on_time_rate) as avg_on_time,
    AVG(avg_cost_per_order_usd) as avg_cost
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
GROUP BY 1;

### [2026-02-27 16:50:11 UTC] — User: amara.shah (assoc_100211)
-- Checking member signup channel distribution.
SELECT 
    acquisition_channel,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
GROUP BY 1
ORDER BY count DESC;

### [2026-01-22 09:14:02 UTC] — User: amara.shah (assoc_100211)
-- Checking table partitioning on fact_orders for audit prep.
SELECT 
    table_name,
    partition_id,
    total_rows
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'fact_orders';

### [2026-01-22 10:45:18 UTC] — User: tara.oduya (assoc_100140)
-- Pulling fulfillment node status for regional audit.
SELECT 
    market,
    node_type,
    COUNT(*) as node_count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE is_active = TRUE
GROUP BY 1, 2;

### [2026-01-22 11:32:04 UTC] — User: giulia.romano (assoc_100213)
-- Analyzing csat distribution across care channels.
SELECT 
    channel,
    csat_score,
    COUNT(*) as contact_count
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE csat_score IS NOT NULL
GROUP BY 1, 2
ORDER BY channel, csat_score;

### [2026-01-22 13:05:40 UTC] — User: wei.hartono (assoc_100210)
-- Validating dim_member panel size against expected bounds.
SELECT 
    status,
    plan_type,
    COUNT(*) as panel_count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
GROUP BY 1, 2;

### [2026-01-22 14:22:11 UTC] — User: connor.blake (assoc_100212)
-- Checking view definitions in dataset.
SELECT 
    table_name,
    view_definition
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.VIEWS`;

### [2026-01-22 15:40:55 UTC] — User: amara.shah (assoc_100211)
-- Running monthly marketing spend aggregation check.
SELECT 
    event_type,
    SUM(actual_spend_usd) as total_actual_spend
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
GROUP BY 1;

### [2026-01-22 16:15:30 UTC] — User: tara.oduya (assoc_100140)
-- Checking promise vs actual performance by fulfillment type during peak.
SELECT 
    fulfillment_type,
    SUM(orders_promised) as promised,
    SUM(orders_on_time) as on_time
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE date BETWEEN '2025-11-01' AND '2025-12-31'
GROUP BY 1;

### [2026-01-23 08:30:12 UTC] — User: giulia.romano (assoc_100213)
-- Pulling post-purchase survey response scores.
SELECT 
    theme_tag,
    COUNT(*) as response_count,
    AVG(score) as avg_score
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE survey_type = 'post_purchase'
GROUP BY 1
ORDER BY response_count DESC;

### [2026-01-23 09:50:44 UTC] — User: wei.hartono (assoc_100210)
-- Checking session definition version counts in traffic table.
SELECT 
    sessions_definition_version,
    MIN(date) as min_date,
    MAX(date) as max_date,
    SUM(sessions) as total_sessions
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
GROUP BY 1;

### [2026-01-23 11:14:22 UTC] — User: amara.shah (assoc_100211)
-- Pulling vertical taxonomy metadata.
SELECT 
    vertical_code,
    vertical_name,
    is_deep_dive
FROM `nexus-analyst-demo.acme_ecomm.dim_vertical`
WHERE is_deep_dive = TRUE;

### [2026-01-23 13:20:05 UTC] — User: connor.blake (assoc_100212)
-- Checking table row counts across base facts.
SELECT 
    'fact_orders' as table_name, COUNT(*) as cnt FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
UNION ALL
SELECT 
    'fact_care_contacts', COUNT(*) FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
UNION ALL
SELECT 
    'fact_voc_responses', COUNT(*) FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`;

### [2026-01-23 14:45:33 UTC] — User: tara.oduya (assoc_100140)
-- Pulling fulfillment speed metrics for fulfillment center nodes.
SELECT 
    f.node_name,
    p.fulfillment_type,
    SUM(p.orders_promised) as promised
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual` p
JOIN `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node` f ON p.node_id = f.node_id
GROUP BY 1, 2;

### [2026-01-23 16:10:19 UTC] — User: giulia.romano (assoc_100213)
-- Checking care contact sub-program distribution.
SELECT 
    sub_program,
    channel,
    COUNT(*) as contact_count
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1, 2;

### [2026-01-24 09:05:40 UTC] — User: wei.hartono (assoc_100210)
-- Checking experiment readout status counts.
SELECT 
    status,
    COUNT(*) as experiment_count
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment`
GROUP BY 1;

### [2026-01-24 10:22:15 UTC] — User: amara.shah (assoc_100211)
-- Pulling weekly conversion summary for US market.
SELECT 
    fiscal_week_ending,
    conversion_rate,
    gmv_usd
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'US'
ORDER BY fiscal_week_ending DESC
LIMIT 10;

### [2026-01-24 11:40:02 UTC] — User: connor.blake (assoc_100212)
-- Checking storage usage by table in dataset.
SELECT 
    table_id,
    size_bytes / 1024 / 1024 as size_mb
FROM `nexus-analyst-demo.acme_ecomm.__TABLES__`;

### [2026-01-24 13:15:50 UTC] — User: tara.oduya (assoc_100140)
-- Pulling fulfillment speed daily metrics for efficiency review.
SELECT 
    fulfillment_type,
    AVG(avg_cost_per_order_usd) as avg_cost
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
GROUP BY 1;

### [2026-01-24 14:30:11 UTC] — User: giulia.romano (assoc_100213)
-- Checking sentiment distribution in voc responses.
SELECT 
    sentiment,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
GROUP BY 1;

### [2026-01-24 16:04:25 UTC] — User: wei.hartono (assoc_100210)
-- Validating seller dimension category distribution.
SELECT 
    category_focus,
    status,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.dim_seller`
GROUP BY 1, 2;

### [2026-01-25 08:15:33 UTC] — User: amara.shah (assoc_100211)
-- Pulling marketplace gmv summary by sub-vertical.
SELECT 
    sub_vertical_code,
    SUM(gmv_usd) as total_gmv,
    SUM(orders) as total_orders
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
GROUP BY 1;

### [2026-01-25 09:30:12 UTC] — User: connor.blake (assoc_100212)
-- Checking dataset routine permissions.
SELECT 
    routine_catalog,
    routine_name
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.ROUTINES`;

### [2026-01-25 10:45:04 UTC] — User: tara.oduya (assoc_100140)
-- Checking associate role distribution for logistics team.
SELECT 
    role,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
WHERE team = 'Fulfillment'
GROUP BY 1;

### [2026-01-25 12:02:50 UTC] — User: giulia.romano (assoc_100213)
-- Checking care deflection daily rates.
SELECT 
    sub_program,
    AVG(deflection_rate) as avg_deflection
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
GROUP BY 1;

### [2026-01-25 13:20:15 UTC] — User: wei.hartono (assoc_100210)
-- Pulling marketplace seller performance summary.
SELECT 
    category_focus,
    AVG(trailing_90d_gmv_usd) as avg_gmv,
    AVG(return_rate) as avg_return_rate
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
GROUP BY 1;

### [2026-01-25 14:55:40 UTC] — User: amara.shah (assoc_100211)
-- Checking traffic sessions breakdown by market and device.
SELECT 
    market,
    device,
    SUM(sessions) as total_sessions
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
GROUP BY 1, 2;

### [2026-01-25 15:10:22 UTC] — User: wei.hartono (assoc_100210)
-- Validating order count consistency in fact_orders vs traffic daily summary.
SELECT 
    t.date,
    t.orders as traffic_orders,
    COUNT(o.order_id) as sample_orders
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily` t
LEFT JOIN `nexus-analyst-demo.acme_ecomm.fact_orders` o ON t.date = o.order_date
WHERE t.date >= '2025-11-01'
GROUP BY 1, 2
ORDER BY 1 DESC
LIMIT 10;

### [2026-01-25 15:42:01 UTC] — User: giulia.romano (assoc_100213)
-- Checking voc sentiment breakdown for negative care contacts during peak.
SELECT 
    theme_tag,
    COUNT(*) as verbatim_count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE sentiment = 'negative'
  AND survey_type = 'post_care_contact'
  AND responded_at >= '2025-11-01'
GROUP BY 1
ORDER BY 2 DESC;

### [2026-01-25 16:05:19 UTC] — User: connor.blake (assoc_100212)
-- Auditing table partition sizes in bq storage.
SELECT 
    table_id,
    row_count,
    size_bytes
FROM `nexus-analyst-demo.acme_ecomm.__TABLES__`
ORDER BY size_bytes DESC;

### [2026-01-25 16:30:45 UTC] — User: amara.shah (assoc_100211)
-- Pulling weekly gmv rollups for finance review.
SELECT 
    fiscal_week_ending,
    sub_vertical_code,
    SUM(gmv_usd) as weekly_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE fiscal_week_ending >= '2025-10-01'
GROUP BY 1, 2
ORDER BY 1 DESC;

### [2026-01-25 17:00:12 UTC] — User: wei.hartono (assoc_100210)
-- Testing query performance on marketplace seller performance panel.
SELECT 
    category_focus,
    COUNT(DISTINCT seller_id) as seller_count,
    AVG(active_listings) as avg_listings
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
GROUP BY 1;

### [2026-01-25 17:22:38 UTC] — User: tara.oduya (assoc_100140)
-- Reviewing fulfillment promise vs actual performance by node type.
SELECT 
    f.node_type,
    SUM(p.orders_promised) as total_promised,
    SUM(p.orders_on_time) as total_on_time
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual` p
JOIN `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node` f ON p.node_id = f.node_id
GROUP BY 1;

### [2026-01-25 18:01:50 UTC] — User: giulia.romano (assoc_100213)
-- Extracting csat distribution for deflected vs assisted care contacts.
SELECT 
    deflected,
    csat_score,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE csat_score IS NOT NULL
GROUP BY 1, 2;

### [2026-01-25 18:33:04 UTC] — User: connor.blake (assoc_100212)
-- Checking view definitions for derived marts.
SELECT 
    table_name,
    view_definition
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.VIEWS`;

### [2026-01-25 19:15:20 UTC] — User: amara.shah (assoc_100211)
-- Pulling member signup channel distribution for membership review.
SELECT 
    acquisition_channel,
    plan_type,
    COUNT(*) as member_count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
GROUP BY 1, 2;

### [2026-01-25 20:02:11 UTC] — User: wei.hartono (assoc_100210)
-- Inspecting column schema for fact_orders table.
SELECT 
    column_name,
    data_type,
    is_nullable
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'fact_orders';

### [2026-01-25 20:45:30 UTC] — User: tara.oduya (assoc_100140)
-- Checking daily shipping cost trends.
SELECT 
    date,
    fulfillment_type,
    AVG(avg_cost_per_order_usd) as avg_cost
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
GROUP BY 1, 2
ORDER BY 1 DESC
LIMIT 20;

### [2026-01-25 21:12:44 UTC] — User: giulia.romano (assoc_100213)
-- Pulling average handle times by care sub program.
SELECT 
    sub_program,
    AVG(avg_handle_time_minutes) as mean_handle_time
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
GROUP BY 1;

### [2026-01-25 21:50:08 UTC] — User: wei.hartono (assoc_100210)
-- Checking marketplace listing authenticity verification status split.
SELECT 
    category,
    authenticity_verified,
    COUNT(*) as listing_count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY 1, 2;

### [2026-01-25 22:20:15 UTC] — User: amara.shah (assoc_100211)
-- Checking dataset routine execution logs.
SELECT 
    job_id,
    creation_time,
    error_result
FROM `nexus-analyst-demo.region-us.INFORMATION_SCHEMA.JOBS_BY_PROJECT`
WHERE query LIKE '%acme_ecomm%'
ORDER BY creation_time DESC
LIMIT 10;

### [2026-01-25 23:01:03 UTC] — User: connor.blake (assoc_100212)
-- Verifying streaming perk benefit redemptions in membership events.
SELECT 
    benefit_code,
    COUNT(*) as redemption_count
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
WHERE event_type = 'benefit_redeemed'
GROUP BY 1;

### [2026-01-25 23:45:12 UTC] — User: wei.hartono (assoc_100210)
-- Checking table partition stats for fact_orders.
SELECT 
    table_name,
    partition_id,
    total_rows,
    size_bytes
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'fact_orders'
ORDER BY partition_id DESC
LIMIT 10;

### [2026-01-26 00:15:30 UTC] — User: amara.shah (assoc_100211)
-- Reconciling weekly membership signups against event stream.
SELECT 
    DATE_TRUNC(event_date, WEEK) as signup_week,
    COUNT(DISTINCT member_id) as unique_signups
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
WHERE event_type = 'signup'
GROUP BY 1
ORDER BY 1 DESC
LIMIT 12;

### [2026-01-26 01:04:19 UTC] — User: tara.oduya (assoc_100140)
-- Reviewing store pickup order volumes across nodes.
SELECT 
    node_id,
    COUNT(*) as pickup_order_count
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE fulfillment_type IN ('bopis', 'curbside')
GROUP BY 1
ORDER BY 2 DESC
LIMIT 15;

### [2026-01-26 01:40:22 UTC] — User: giulia.romano (assoc_100213)
-- Analyzing chat channel handle times by sub program.
SELECT 
    sub_program,
    channel,
    COUNT(*) as contact_count,
    AVG(handle_time_minutes) as mean_handle_time
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE channel = 'chat'
GROUP BY 1, 2;

### [2026-01-26 02:12:05 UTC] — User: wei.hartono (assoc_100210)
-- Inspecting marketplace listing price distribution for collectibles.
SELECT 
    ROUND(price_usd, -1) as price_bucket,
    COUNT(*) as listing_count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
WHERE category = 'collectibles'
GROUP BY 1
ORDER BY 1;

### [2026-01-26 02:55:41 UTC] — User: amara.shah (assoc_100211)
-- Checking column constraints on dim_vertical.
SELECT 
    column_name,
    is_nullable
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'dim_vertical';

### [2026-01-26 03:30:18 UTC] — User: connor.blake (assoc_100212)
-- Auditing table row counts across primary base facts.
SELECT 'fact_orders' as tbl, COUNT(*) as cnt FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
UNION ALL
SELECT 'fact_care_contacts', COUNT(*) FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
UNION ALL
SELECT 'fact_voc_responses', COUNT(*) FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`;

### [2026-01-26 04:11:50 UTC] — User: tara.oduya (assoc_100140)
-- Checking fulfillment node types in dimension table.
SELECT 
    node_type,
    COUNT(*) as node_count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
GROUP BY 1;

### [2026-01-26 05:02:33 UTC] — User: giulia.romano (assoc_100213)
-- Pulling average CSAT scores by resolution code for care contacts.
SELECT 
    resolution_code,
    AVG(csat_score) as mean_csat,
    COUNT(*) as contact_count
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE csat_score IS NOT NULL
GROUP BY 1
ORDER BY 2 DESC;

### [2026-01-26 06:20:11 UTC] — User: wei.hartono (assoc_100210)
-- Checking active experiments count by vertical.
SELECT 
    vertical_code,
    COUNT(*) as experiment_count
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment`
WHERE status = 'running'
GROUP BY 1;

### [2026-01-26 07:15:44 UTC] — User: amara.shah (assoc_100211)
-- Running monthly GMV reconciliation check against traffic summary.
SELECT 
    DATE_TRUNC(fiscal_week_ending, MONTH) as fiscal_month,
    SUM(gmv_usd) as total_gmv
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
GROUP BY 1
ORDER BY 1;

### [2026-01-26 08:00:25 UTC] — User: connor.blake (assoc_100212)
-- Checking BigQuery query history for recent pipeline jobs.
SELECT 
    user_email,
    state,
    total_bytes_billed
FROM `nexus-analyst-demo.region-us.INFORMATION_SCHEMA.JOBS_BY_PROJECT`
WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)
LIMIT 10;

### [2026-01-26 08:45:10 UTC] — User: tara.oduya (assoc_100140)
-- Pulling on-time performance by fulfillment type for Q4.
SELECT 
    fulfillment_type,
    SUM(orders_on_time) / SUM(orders_promised) as otp_rate
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE date >= '2025-11-01' AND date <= '2026-01-25'
GROUP BY 1;

### [2026-01-26 09:22:18 UTC] — User: giulia.romano (assoc_100213)
-- Checking post-care contact survey response sentiment distribution.
SELECT 
    sentiment,
    COUNT(*) as response_count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE survey_type = 'post_care_contact'
GROUP BY 1;

### [2026-01-26 10:14:02 UTC] — User: wei.hartono (assoc_100210)
-- Checking seller status distribution in dim_seller panel.
SELECT 
    status,
    COUNT(*) as seller_count
FROM `nexus-analyst-demo.acme_ecomm.dim_seller`
GROUP BY 1;

### [2026-01-26 11:05:33 UTC] — User: amara.shah (assoc_100211)
-- Pulling member acquisition channel breakdown for annual plans.
SELECT 
    acquisition_channel,
    COUNT(*) as member_count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
WHERE plan_type = 'annual'
GROUP BY 1
ORDER BY 2 DESC;

### [2026-01-26 11:50:41 UTC] — User: connor.blake (assoc_100212)
-- Checking dataset table storage sizes.
SELECT 
    table_name,
    size_bytes / 1024 / 1024 as size_mb
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.TABLE_STORAGE`
ORDER BY size_bytes DESC;

### [2026-01-26 12:33:15 UTC] — User: tara.oduya (assoc_100140)
-- Inspecting daily fulfillment speed metrics for ship to home.
SELECT 
    date,
    avg_cost_per_order_usd
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE fulfillment_type = 'ship_to_home'
ORDER BY date DESC
LIMIT 10;

### [2026-01-26 13:10:29 UTC] — User: giulia.romano (assoc_100213)
-- Pulling care deflection rate by day for January 2026.
SELECT 
    date,
    deflection_rate,
    contact_volume
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
WHERE date >= '2026-01-01'
ORDER BY date;

### [2026-01-26 14:04:55 UTC] — User: wei.hartono (assoc_100210)
-- Validating distinct markets in fact_traffic_daily.
SELECT 
    market,
    SUM(sessions) as total_sessions
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date >= '2025-11-01'
GROUP BY 1;

### [2026-01-26 14:50:12 UTC] — User: amara.shah (assoc_100211)
-- Checking plan price distribution in dim_member.
SELECT 
    plan_type,
    plan_price_usd,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
GROUP BY 1, 2;

### [2026-01-26 15:32:40 UTC] — User: connor.blake (assoc_100212)
-- Checking table definitions for marketplace seller performance mart.
SELECT 
    column_name,
    data_type
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'marketplace_seller_performance';

### [2026-01-26 16:15:08 UTC] — User: tara.oduya (assoc_100140)
-- Checking average days late when late by fulfillment node.
SELECT 
    node_id,
    AVG(avg_days_late_when_late) as mean_days_late
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE node_id IS NOT NULL
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10;

### [2026-01-26 17:02:19 UTC] — User: giulia.romano (assoc_100213)
-- Inspecting NPS score distribution in voc responses.
SELECT 
    score,
    COUNT(*) as response_count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE survey_type = 'nps'
GROUP BY 1
ORDER BY 1;

### [2026-01-26 17:45:30 UTC] — User: wei.hartono (assoc_100210)
-- Checking listing status breakdown in marketplace listings sample.
SELECT 
    status,
    COUNT(*) as listing_count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY 1;

### [2026-01-26 18:30:11 UTC] — User: amara.shah (assoc_100211)
-- Checking marketing calendar event types.
SELECT 
    event_type,
    COUNT(*) as event_count
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
GROUP BY 1;

### [2026-01-26 19:12:44 UTC] — User: connor.blake (assoc_100212)
-- Verifying view definitions in dataset.
SELECT 
    table_name,
    view_definition
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.VIEWS`;

### [2026-01-26 20:01:50 UTC] — User: tara.oduya (assoc_100140)
-- Checking order fulfillment split across markets.
SELECT 
    market,
    fulfillment_type,
    COUNT(*) as order_count
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
GROUP BY 1, 2;

### [2026-01-26 20:45:22 UTC] — User: giulia.romano (assoc_100213)
-- Pulling deflection rate and volume summary for December 2025.
SELECT 
    sub_program,
    SUM(contact_volume) as total_volume,
    AVG(deflection_rate) as avg_deflection
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
WHERE date BETWEEN '2025-12-01' AND '2025-12-31'
GROUP BY 1;

### [2026-01-26 21:30:05 UTC] — User: wei.hartono (assoc_100210)
-- Checking column constraints on fact_experiment_readouts.
SELECT 
    column_name,
    data_type
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'fact_experiment_readouts';

### [2026-01-26 22:15:33 UTC] — User: amara.shah (assoc_100211)
-- Pulling membership cancellation reasons via membership events.
SELECT 
    channel,
    COUNT(*) as cancel_count
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
WHERE event_type = 'cancel'
GROUP BY 1;

### [2026-01-26 23:02:18 UTC] — User: connor.blake (assoc_100212)
-- Auditing scheduled query execution logs for partition maintenance.
SELECT 
    job_id,
    creation_time,
    error_result,
    total_bytes_processed
FROM `nexus-analyst-demo.region-us.INFORMATION_SCHEMA.JOBS_BY_PROJECT`
WHERE query LIKE '%PARTITION%'
ORDER BY creation_time DESC
LIMIT 5;

### [2026-01-27 00:10:44 UTC] — User: tara.oduya (assoc_100140)
-- Checking average cost per order across fulfillment types in daily speed summary.
SELECT 
    fulfillment_type,
    AVG(avg_cost_per_order_usd) as mean_cost
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
GROUP BY 1;

### [2026-01-27 00:55:12 UTC] — User: giulia.romano (assoc_100213)
-- Pulling verbatims with negative sentiment for post purchase surveys.
SELECT 
    theme_tag,
    COUNT(*) as verbatim_count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE survey_type = 'post_purchase' AND sentiment = 'negative'
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10;

### [2026-01-27 01:40:25 UTC] — User: wei.hartono (assoc_100210)
-- Checking category focus distribution in seller dimension table.
SELECT 
    category_focus,
    COUNT(*) as seller_count
FROM `nexus-analyst-demo.acme_ecomm.dim_seller`
GROUP BY 1;

### [2026-01-27 02:22:01 UTC] — User: amara.shah (assoc_100211)
-- Checking signups by home market in member dimension panel.
SELECT 
    home_market,
    COUNT(*) as member_count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
GROUP BY 1;

### [2026-01-27 03:05:40 UTC] — User: connor.blake (assoc_100212)
-- Verifying marketplace gmv summary row counts and date ranges.
SELECT 
    MIN(fiscal_week_ending) as min_week,
    MAX(fiscal_week_ending) as max_week,
    COUNT(*) as row_count
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`;

### [2026-01-27 03:50:18 UTC] — User: tara.oduya (assoc_100140)
-- Checking orders promised vs actual on-time rate by market for Q4.
SELECT 
    market,
    SUM(orders_on_time) / SUM(orders_promised) as otp
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE date >= '2025-11-01'
GROUP BY 1;

### [2026-01-27 04:33:50 UTC] — User: giulia.romano (assoc_100213)
-- Checking handle time distribution for phone support channel.
SELECT 
    sub_program,
    AVG(handle_time_minutes) as avg_handle_time
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE channel = 'phone'
GROUP BY 1;

### [2026-01-27 05:15:22 UTC] — User: wei.hartono (assoc_100210)
-- Checking table schemas for traffic conversion summary mart.
SELECT 
    column_name,
    data_type
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'traffic_conversion_summary';

### [2026-01-27 06:01:14 UTC] — User: amara.shah (assoc_100211)
-- Pulling weekly conversion rates for US market in traffic conversion summary.
SELECT 
    fiscal_week_ending,
    conversion_rate,
    gmv_usd
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'US'
ORDER BY fiscal_week_ending DESC
LIMIT 10;

### [2026-01-27 06:45:33 UTC] — User: connor.blake (assoc_100212)
-- Checking dataset table constraints and primary keys in information schema.
SELECT 
    table_name,
    option_value
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.TABLE_OPTIONS`
WHERE option_name = 'description';

### [2026-01-27 07:30:19 UTC] — User: tara.oduya (assoc_100140)
-- Pulling fulfillment speed metrics for DFS fulfillment type.
SELECT 
    date,
    market,
    on_time_rate
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE fulfillment_type = 'dfs'
ORDER BY date DESC
LIMIT 10;

### [2026-01-27 08:14:05 UTC] — User: giulia.romano (assoc_100213)
-- Checking bot deflection rate trends across sub programs.
SELECT 
    sub_program,
    AVG(deflection_rate) as mean_deflection
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
GROUP BY 1;

### [2026-01-27 09:02:41 UTC] — User: wei.hartono (assoc_100210)
-- Inspecting experiment status distribution in dim_experiment.
SELECT 
    status,
    COUNT(*) as experiment_count
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment`
GROUP BY 1;

### [2026-01-27 09:48:12 UTC] — User: amara.shah (assoc_100211)
-- Checking marketing calendar planned vs actual spend by event type.
SELECT 
    event_type,
    SUM(planned_spend_usd) as total_planned,
    SUM(actual_spend_usd) as total_actual
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
GROUP BY 1;

### [2026-01-27 10:30:50 UTC] — User: connor.blake (assoc_100212)
-- Checking row count for fact_marketplace_listings table.
SELECT COUNT(*) as total_listings FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`;

### [2026-01-27 11:15:22 UTC] — User: tara.oduya (assoc_100140)
-- Checking fulfillment node activity status.
SELECT 
    node_type,
    is_active,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
GROUP BY 1, 2;

### [2026-01-27 12:01:08 UTC] — User: giulia.romano (assoc_100213)
-- Pulling survey types and response counts from voc responses.
SELECT 
    survey_type,
    COUNT(*) as response_count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
GROUP BY 1;

### [2026-01-27 12:45:33 UTC] — User: wei.hartono (assoc_100210)
-- Checking columns in fact_care_contacts table.
SELECT 
    column_name,
    data_type
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'fact_care_contacts';

### [2026-01-27 13:30:19 UTC] — User: amara.shah (assoc_100211)
-- Pulling member acquisition channels for active members.
SELECT 
    acquisition_channel,
    COUNT(*) as active_count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
WHERE status = 'active'
GROUP BY 1;

### [2026-01-27 14:14:50 UTC] — User: connor.blake (assoc_100212)
-- Checking dataset table list via information schema tables.
SELECT 
    table_name,
    table_type
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.TABLES`
ORDER BY table_name;

### [2026-01-27 15:02:11 UTC] — User: tara.oduya (assoc_100140)
-- Pulling order volume share by fulfillment type in speed daily mart.
SELECT 
    fulfillment_type,
    AVG(pct_of_total_orders) as mean_share
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
GROUP BY 1;

### [2026-01-27 15:48:25 UTC] — User: giulia.romano (assoc_100213)
-- Checking contact channel breakdown in care contacts sample.
SELECT 
    channel,
    COUNT(*) as contact_count
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1;

### [2026-01-27 16:33:04 UTC] — User: wei.hartono (assoc_100210)
-- Checking table schema for fact_membership_events.
SELECT 
    column_name,
    data_type
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'fact_membership_events';

### [2026-01-27 17:15:40 UTC] — User: amara.shah (assoc_100211)
-- Pulling plan type distribution for paused members.
SELECT 
    plan_type,
    COUNT(*) as paused_count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
WHERE status = 'paused'
GROUP BY 1;

### [2026-01-27 18:02:19 UTC] — User: connor.blake (assoc_100212)
-- Checking recent query performance metrics in information schema jobs.
SELECT 
    job_id,
    total_slot_ms,
    total_bytes_billed
FROM `nexus-analyst-demo.region-us.INFORMATION_SCHEMA.JOBS_BY_PROJECT`
WHERE statement_type = 'SELECT'
ORDER BY creation_time DESC
LIMIT 10;

### [2026-01-27 18:45:11 UTC] — User: tara.oduya (assoc_100140)
-- Checking daily fulfillment speed on time rates for ship to home.
SELECT 
    date,
    on_time_rate
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE fulfillment_type = 'ship_to_home'
ORDER BY date DESC
LIMIT 15;

### [2026-01-27 19:30:55 UTC] — User: giulia.romano (assoc_100213)
-- Checking deflection rate vs csat deflected across care deflection daily.
SELECT 
    deflection_rate,
    avg_csat_deflected
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
WHERE deflection_rate IS NOT NULL
LIMIT 20;

### [2026-01-27 20:14:22 UTC] — User: wei.hartono (assoc_100210)
-- Checking category distribution in marketplace seller performance.
SELECT 
    category_focus,
    COUNT(*) as seller_count,
    AVG(trailing_90d_gmv_usd) as avg_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
GROUP BY 1;

### [2026-01-27 21:00:15 UTC] — User: amara.shah (assoc_100211)
-- Checking table definitions for dim_date.
SELECT 
    column_name,
    data_type
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'dim_date';

### [2026-01-27 21:45:30 UTC] — User: connor.blake (assoc_100212)
-- Verifying member cltv table row count and null check.
SELECT 
    COUNT(*) as total_rows,
    COUNT(DISTINCT member_id) as unique_members
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`;

### [2026-01-27 22:30:12 UTC] — User: tara.oduya (assoc_100140)
-- Checking fulfillment node market coverage in dim_fulfillment_node.
SELECT 
    market,
    COUNT(*) as node_count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
GROUP BY 1;

### [2026-01-27 23:15:44 UTC] — User: giulia.romano (assoc_100213)
-- Pulling survey score distribution for csat score type in voc responses.
SELECT 
    score,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE score_type = 'csat_1_5'
GROUP BY 1
ORDER BY 1;

### [2026-01-27 23:45:10 UTC] — User: amara.shah (assoc_100211)
-- Checking partition sizes for fact_orders across Q4FY26.
SELECT 
    DATE_TRUNC(order_date, MONTH) as order_month,
    COUNT(*) as row_count,
    SUM(gmv_usd) as total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE order_date BETWEEN '2025-11-01' AND '2026-01-25'
GROUP BY 1
ORDER BY 1;

### [2026-01-28 00:12:03 UTC] — User: connor.blake (assoc_100212)
-- Verifying pipeline watermark for dim_seller updates.
SELECT 
    MAX(onboarded_date) as latest_onboard
FROM `nexus-analyst-demo.acme_ecomm.dim_seller`;

### [2026-01-28 01:05:40 UTC] — User: wei.hartono (assoc_100210)
-- Testing flat dataset path resolution for marketplace gmv summary.
SELECT 
    sub_vertical_code,
    SUM(gmv_usd) as q4_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE fiscal_week_ending BETWEEN '2025-11-01' AND '2026-01-25'
GROUP BY 1;

### [2026-01-28 02:30.15 UTC] — User: tara.oduya (assoc_100140)
-- Pulling average handle time trends across care channels for care deflection daily.
SELECT 
    sub_program,
    AVG(avg_handle_time_minutes) as mean_handle_time
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
GROUP BY 1;

### [2026-01-28 03:15:22 UTC] — User: giulia.romano (assoc_100213)
-- Auditing post purchase survey response sentiments in fact voc responses.
SELECT 
    sentiment,
    COUNT(*) as response_count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE survey_type = 'post_purchase'
GROUP BY 1;

### [2026-01-28 04:00:55 UTC] — User: amara.shah (assoc_100211)
-- Verifying marketing calendar planned vs actual spend for holiday events.
SELECT 
    event_name,
    planned_spend_usd,
    actual_spend_usd
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
WHERE event_type = 'holiday'
LIMIT 10;

### [2026-01-28 05:22:11 UTC] — User: connor.blake (assoc_100212)
-- Checking table row counts for fact care contacts.
SELECT 
    channel,
    COUNT(*) as contact_count
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1;

### [2026-01-28 06:10:33 UTC] — User: wei.hartono (assoc_100210)
-- Pulling daily traffic sessions summary by device type.
SELECT 
    device,
    SUM(sessions) as total_sessions,
    SUM(gmv_usd) as total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date >= '2026-01-01'
GROUP BY 1;

### [2026-01-28 07:45:00 UTC] — User: tara.oduya (assoc_100140)
-- Checking promise vs actual performance for ship to home fulfillment type.
SELECT 
    market,
    SUM(orders_promised) as promised,
    SUM(orders_on_time) as on_time
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE fulfillment_type = 'ship_to_home'
GROUP BY 1;

### [2026-01-28 08:30:19 UTC] — User: giulia.romano (assoc_100213)
-- Checking member cltv distribution across plan types from dim member join.
SELECT 
    m.plan_type,
    COUNT(c.member_id) as member_count,
    AVG(c.lifetime_gmv_usd) as avg_lifetime_gmv
FROM `nexus-analyst-demo.acme_ecomm.dim_member` m
LEFT JOIN `nexus-analyst-demo.acme_ecomm.member_cltv` c ON m.member_id = c.member_id
GROUP BY 1;

### [2026-01-28 09:15:44 UTC] — User: amara.shah (assoc_100211)
-- Listing experiment definitions for running status in dim experiment.
SELECT 
    experiment_id,
    experiment_name,
    primary_metric
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment`
WHERE status = 'running';

### [2026-01-28 10:02:18 UTC] — User: connor.blake (assoc_100212)
-- Checking fulfillment node active status counts.
SELECT 
    node_type,
    COUNT(*) as active_count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE is_active = TRUE
GROUP BY 1;

### [2026-01-28 11:20:50 UTC] — User: wei.hartono (assoc_100210)
-- Pulling marketplace listings status breakdown for collectibles category.
SELECT 
    status,
    authenticity_verified,
    COUNT(*) as listing_count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
WHERE category = 'collectibles'
GROUP BY 1, 2;

### [2026-01-28 12:05:33 UTC] — User: tara.oduya (assoc_100140)
-- Checking fulfillment speed daily metrics for curbside pickup type.
SELECT 
    date,
    on_time_rate,
    avg_cost_per_order_usd
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE fulfillment_type = 'curbside'
ORDER BY date DESC
LIMIT 10;

### [2026-01-28 13:40:12 UTC] — User: giulia.romano (assoc_100213)
-- Pulling top theme tags from fact voc responses for negative sentiment.
SELECT 
    theme_tag,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE sentiment = 'negative' AND theme_tag IS NOT NULL
GROUP BY 1
ORDER BY count DESC
LIMIT 10;

### [2026-01-28 14:15:25 UTC] — User: amara.shah (assoc_100211)
-- Validating traffic conversion summary weekly rollups for US market.
SELECT 
    fiscal_week_ending,
    sessions,
    orders,
    conversion_rate
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'US'
ORDER BY fiscal_week_ending DESC
LIMIT 10;

### [2026-01-28 15:00:41 UTC] — User: connor.blake (assoc_100212)
-- Checking membership events table distribution by event type.
SELECT 
    event_type,
    COUNT(*) as event_count
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
GROUP BY 1;

### [2026-01-28 16:30:19 UTC] — User: wei.hartono (assoc_100210)
-- Pulling seller performance metrics for resold category focus.
SELECT 
    seller_id,
    active_listings,
    trailing_90d_gmv_usd,
    return_rate
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
WHERE category_focus = 'resold'
ORDER BY trailing_90d_gmv_usd DESC
LIMIT 15;

### [2026-01-28 17:10:05 UTC] — User: tara.oduya (assoc_100140)
-- Checking associate table team breakdown for fulfillment org.
SELECT 
    team,
    COUNT(*) as headcount
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
WHERE is_active = TRUE
GROUP BY 1;

### [2026-01-28 18:25:50 UTC] — User: giulia.romano (assoc_100213)
-- Pulling care deflection daily average csat metrics by sub program.
SELECT 
    sub_program,
    AVG(avg_csat_deflected) as mean_deflected_csat,
    AVG(avg_csat_agent_assisted) as mean_assisted_csat
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
GROUP BY 1;

### [2026-01-28 19:00:14 UTC] — User: amara.shah (assoc_100211)
-- Checking dim vertical codes and customer facing descriptions.
SELECT 
    vertical_code,
    vertical_name,
    customer_facing_desc
FROM `nexus-analyst-demo.acme_ecomm.dim_vertical`
WHERE is_deep_dive = TRUE;

### [2026-01-28 20:45:30 UTC] — User: connor.blake (assoc_100212)
-- Verifying experiment exposure units assigned vs exposed totals.
SELECT 
    experiment_id,
    variant,
    SUM(units_assigned) as assigned,
    SUM(units_exposed) as exposed
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures`
GROUP BY 1, 2
LIMIT 10;

### [2026-01-28 21:15:02 UTC] — User: wei.hartono (assoc_100210)
-- Checking dim date peak holiday indicator counts.
SELECT 
    fiscal_quarter_label,
    is_peak_holiday,
    COUNT(*) as day_count
FROM `nexus-analyst-demo.acme_ecomm.dim_date`
GROUP BY 1, 2;

### [2026-01-28 22:30:45 UTC] — User: tara.oduya (assoc_100140)
-- Pulling fulfillment speed daily metrics for store fulfillment type.
SELECT 
    date,
    on_time_rate,
    pct_of_total_orders
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE fulfillment_type = 'dfs'
ORDER BY date DESC
LIMIT 15;

### [2026-01-28 23:12:10 UTC] — User: giulia.romano (assoc_100213)
-- Checking care contacts channel distribution.
SELECT 
    channel,
    deflected,
    COUNT(*) as contact_count
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1, 2;

### [2026-01-29 00:05:19 UTC] — User: amara.shah (assoc_100211)
-- Pulling marketplace gmv summary take rate averages by sub vertical code.
SELECT 
    sub_vertical_code,
    AVG(take_rate) as avg_take_rate,
    SUM(gmv_usd) as total_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
GROUP BY 1;

### [2026-01-29 01:20:40 UTC] — User: connor.blake (assoc_100212)
-- Checking member cltv projected cltv by plan type.
SELECT 
    m.plan_type,
    AVG(c.projected_cltv_usd) as avg_projected_cltv
FROM `nexus-analyst-demo.acme_ecomm.dim_member` m
JOIN `nexus-analyst-demo.acme_ecomm.member_cltv` c ON m.member_id = c.member_id
GROUP BY 1;

### [2026-01-29 02:15:00 UTC] — User: wei.hartono (assoc_100210)
-- Pulling fact orders channel breakdown and refund metrics.
SELECT 
    channel,
    COUNT(*) as order_count,
    AVG(refund_usd) as avg_refund
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE refund_usd IS NOT NULL
GROUP BY 1;

### [2026-01-29 03:30:11 UTC] — User: tara.oduya (assoc_100140)
-- Checking dim fulfillment node markets for distribution centers.
SELECT 
    market,
    COUNT(*) as dc_count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE node_type = 'dc'
GROUP BY 1;

### [2026-01-29 04:12:55 UTC] — User: giulia.romano (assoc_100213)
-- Pulling voc responses score distribution for nps score type.
SELECT 
    score,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE score_type = 'nps_0_10'
GROUP BY 1
ORDER BY 1;

### [2026-01-29 05:00:22 UTC] — User: amara.shah (assoc_100211)
-- Checking experiment readouts table metrics and significance flag counts.
SELECT 
    metric_name,
    is_significant,
    COUNT(*) as readout_count
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`
GROUP BY 1, 2;

### [2026-01-29 06:45:14 UTC] — User: connor.blake (assoc_100212)
-- Verifying dim seller category focus counts in panel.
SELECT 
    category_focus,
    COUNT(*) as seller_count
FROM `nexus-analyst-demo.acme_ecomm.dim_seller`
GROUP BY 1;

### [2026-01-29 07:22:33 UTC] — User: wei.hartono (assoc_100210)
-- Checking traffic conversion summary sessions definition version distribution.
SELECT 
    sessions_definition_version,
    COUNT(*) as row_count,
    SUM(sessions) as total_sessions
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
GROUP BY 1;

### [2026-01-29 08:10:45 UTC] — User: tara.oduya (assoc_100140)
-- Pulling average days late when late from fact promise vs actual.
SELECT 
    vertical_code,
    AVG(avg_days_late_when_late) as mean_days_late
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
GROUP BY 1;

### [2026-01-29 09:30:12 UTC] — User: giulia.romano (assoc_100213)
-- Checking fact care contacts sub program volume.
SELECT 
    sub_program,
    COUNT(*) as contact_count
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1;

### [2026-01-29 10:05:20 UTC] — User: amara.shah (assoc_100211)
-- Pulling dim marketing calendar owner association counts.
SELECT 
    owner_assoc_id,
    COUNT(*) as event_count
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
GROUP BY 1
ORDER BY event_count DESC
LIMIT 10;

### [2026-01-29 11:15:50 UTC] — User: connor.blake (assoc_100212)
-- Checking marketplace seller performance return rate averages.
SELECT 
    category_focus,
    AVG(return_rate) as avg_return_rate,
    AVG(authenticity_flag_count) as avg_auth_flags
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
GROUP BY 1;

### [2026-01-29 12:40:15 UTC] — User: wei.hartono (assoc_100210)
-- Pulling fact traffic daily session definitions check for version 1 vs 2.
SELECT 
    sessions_definition_version,
    MIN(date) as start_date,
    MAX(date) as end_date
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
GROUP BY 1;

### [2026-01-29 13:25:03 UTC] — User: tara.oduya (assoc_100140)
-- Checking fulfillment speed daily cost trends across markets.
SELECT 
    market,
    AVG(avg_cost_per_order_usd) as avg_cost
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
GROUP BY 1;

### [2026-01-29 14:02:44 UTC] — User: giulia.romano (assoc_100213)
-- Checking voc responses survey types distribution.
SELECT 
    survey_type,
    COUNT(*) as response_count,
    AVG(score) as avg_score
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
GROUP BY 1;

### [2026-01-29 15:10:19 UTC] — User: amara.shah (assoc_100211)
-- Pulling member cltv benefits adopted count distribution.
SELECT 
    benefits_adopted_count,
    COUNT(*) as member_count
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`
GROUP BY 1
ORDER BY 1;

### [2026-01-29 16:30:00 UTC] — User: connor.blake (assoc_100212)
-- Checking dim associate roles in data and analytics team.
SELECT 
    full_name,
    role
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
WHERE team = 'Data' AND is_active = TRUE;

### [2026-01-29 17:15:33 UTC] — User: wei.hartono (assoc_100210)
-- Pulling fact orders fulfillment type distribution for 3P channel.
SELECT 
    fulfillment_type,
    COUNT(*) as order_count,
    SUM(gmv_usd) as total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE channel = '3P'
GROUP BY 1;

### [2026-01-29 18:00:22 UTC] — User: tara.oduya (assoc_100140)
-- Checking dim fulfillment node store formats for store nodes.
SELECT 
    store_format,
    COUNT(*) as format_count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE node_type = 'store'
GROUP BY 1;

### [2026-01-29 19:12:45 UTC] — User: giulia.romano (assoc_100213)
-- Checking care deflection daily deflection rate summary stats.
SELECT 
    sub_program,
    MIN(deflection_rate) as min_deflection,
    MAX(deflection_rate) as max_deflection,
    AVG(deflection_rate) as avg_deflection
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
GROUP BY 1;

### [2026-01-29 20:20:11 UTC] — User: amara.shah (assoc_100211)
-- Pulling marketplace listings active counts by category.
SELECT 
    category,
    status,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY 1, 2;

### [2026-01-29 21:05:50 UTC] — User: connor.blake (assoc_100212)
-- Checking dim member acquisition channels.
SELECT 
    acquisition_channel,
    COUNT(*) as member_count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
GROUP BY 1
ORDER BY member_count DESC;

### [2026-01-29 22:40:14 UTC] — User: wei.hartono (assoc_100210)
-- Pulling traffic conversion summary gmv totals by market.
SELECT 
    market,
    SUM(gmv_usd) as total_gmv
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
GROUP BY 1;

### [2026-01-29 23:15:30 UTC] — User: tara.oduya (assoc_100140)
-- Checking fact promise vs actual order fulfillment volume totals.
SELECT 
    fulfillment_type,
    SUM(orders_promised) as total_promised,
    SUM(orders_on_time) as total_on_time
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
GROUP BY 1;

### [2026-01-29 23:42:11 UTC] — User: amara.shah (assoc_100211)
-- Checking fact orders channel breakdown by market for Q4 peak.
SELECT 
    market,
    channel,
    COUNT(*) as order_cnt,
    SUM(gmv_usd) as channel_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE order_date >= '2025-11-01'
GROUP BY 1, 2;

### [2026-01-30 01:10:05 UTC] — User: wei.hartono (assoc_100210)
-- Testing member table sample count consistency.
SELECT 
    plan_type,
    status,
    COUNT(*) as member_panel_count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
GROUP BY 1, 2;

### [2026-01-30 02:15:33 UTC] — User: giulia.romano (assoc_100213)
-- Pulling care contacts volume by sub-program and channel.
SELECT 
    sub_program,
    channel,
    COUNT(*) as contact_count,
    AVG(csat_score) as mean_csat
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1, 2;

### [2026-01-30 03:20:44 UTC] — User: connor.blake (assoc_100212)
-- Auditing fulfillment node active counts by type.
SELECT 
    node_type,
    market,
    COUNT(*) as node_count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE is_active = TRUE
GROUP BY 1, 2;

### [2026-01-30 04:05:12 UTC] — User: tara.oduya (assoc_100140)
-- Checking fact promise vs actual late delivery averages.
SELECT 
    fulfillment_type,
    AVG(avg_days_late_when_late) as mean_days_late
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE orders_on_time < orders_promised
GROUP BY 1;

### [2026-01-30 05:30:19 UTC] — User: amara.shah (assoc_100211)
-- Pulling traffic conversion summary gmv totals by device category.
SELECT 
    device,
    SUM(sessions) as total_sessions,
    SUM(gmv_usd) as total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
GROUP BY 1;

### [2026-01-30 06:12:50 UTC] — User: wei.hartono (assoc_100210)
-- Checking marketplace seller panel status distribution.
SELECT 
    status,
    category_focus,
    COUNT(*) as seller_count
FROM `nexus-analyst-demo.acme_ecomm.dim_seller`
GROUP BY 1, 2;

### [2026-01-30 07:45:02 UTC] — User: giulia.romano (assoc_100213)
-- Checking voc responses sentiment distribution by score type.
SELECT 
    score_type,
    sentiment,
    COUNT(*) as response_count,
    AVG(score) as avg_score
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
GROUP BY 1, 2;

### [2026-01-30 08:33:14 UTC] — User: connor.blake (assoc_100212)
-- Checking dim experiment statuses and vertical codes.
SELECT 
    vertical_code,
    status,
    COUNT(*) as experiment_count
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment`
GROUP BY 1, 2;

### [2026-01-30 09:15:22 UTC] — User: tara.oduya (assoc_100140)
-- Pulling fulfillment speed daily metrics for store fulfillment types.
SELECT 
    date,
    market,
    on_time_rate,
    avg_cost_per_order_usd
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE fulfillment_type = 'bopis'
ORDER BY date DESC
LIMIT 20;

### [2026-01-30 10:22:40 UTC] — User: wei.hartono (assoc_100210)
-- Validating order return dates against refund issued dates.
SELECT 
    return_reason_code,
    COUNT(*) as return_count,
    AVG(TIMESTAMP_DIFF(CAST(refund_issued_date AS TIMESTAMP), CAST(return_date AS TIMESTAMP), DAY)) as avg_refund_days
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE is_returned = TRUE AND refund_issued_date IS NOT NULL
GROUP BY 1;

### [2026-01-30 11:04:18 UTC] — User: amara.shah (assoc_100211)
-- Checking marketplace seller performance trailing gmv summaries.
SELECT 
    category_focus,
    SUM(trailing_90d_gmv_usd) as total_trailing_gmv,
    AVG(return_rate) as mean_return_rate
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
GROUP BY 1;

### [2026-01-30 12:40:09 UTC] — User: giulia.romano (assoc_100213)
-- Pulling member cltv summaries by signup cohort quarter.
SELECT 
    signup_cohort_quarter,
    COUNT(*) as member_cnt,
    AVG(lifetime_gmv_usd) as avg_lifetime_gmv,
    AVG(projected_cltv_usd) as avg_projected_cltv
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`
GROUP BY 1
ORDER BY signup_cohort_quarter;

### [2026-01-30 13:19:55 UTC] — User: connor.blake (assoc_100212)
-- Auditing marketing calendar event types and planned spend.
SELECT 
    event_type,
    COUNT(*) as event_count,
    SUM(planned_spend_usd) as total_planned_spend
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
GROUP BY 1;

### [2026-01-30 14:02:30 UTC] — User: wei.hartono (assoc_100210)
-- Checking traffic daily sessions version definition distribution.
SELECT 
    sessions_definition_version,
    COUNT(*) as row_count,
    SUM(sessions) as total_sessions
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
GROUP BY 1;

### [2026-01-30 15:11:48 UTC] — User: tara.oduya (assoc_100140)
-- Pulling care deflection daily stats for avoid sub program.
SELECT 
    date,
    contact_volume,
    deflection_rate,
    avg_csat_deflected
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
WHERE sub_program = 'avoid'
ORDER BY date DESC
LIMIT 15;

### [2026-01-30 16:25:01 UTC] — User: amara.shah (assoc_100211)
-- Checking membership events distribution by event type and channel.
SELECT 
    event_type,
    channel,
    COUNT(*) as event_count
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
GROUP BY 1, 2;

### [2026-01-30 17:09:37 UTC] — User: giulia.romano (assoc_100213)
-- Pulling voc responses themes for post-purchase survey type.
SELECT 
    theme_tag,
    sentiment,
    COUNT(*) as theme_count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE survey_type = 'post_purchase'
GROUP BY 1, 2
ORDER BY theme_count DESC
LIMIT 10;

### [2026-01-30 18:02:15 UTC] — User: connor.blake (assoc_100212)
-- Checking marketplace listings authenticity verified distribution.
SELECT 
    category,
    authenticity_verified,
    COUNT(*) as listing_count,
    AVG(price_usd) as avg_price
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY 1, 2;

### [2026-01-30 19:30:44 UTC] — User: wei.hartono (assoc_100210)
-- Running experimental exposure aggregations by variant.
SELECT 
    experiment_id,
    variant,
    SUM(units_assigned) as total_assigned,
    SUM(units_exposed) as total_exposed,
    SUM(units_converted) as total_converted
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures`
GROUP BY 1, 2;

### [2026-01-30 20:14:02 UTC] — User: tara.oduya (assoc_100140)
-- Checking marketplace gmv summary take rates by sub vertical.
SELECT 
    sub_vertical_code,
    AVG(take_rate) as mean_take_rate,
    SUM(gmv_usd) as total_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
GROUP BY 1;

### [2026-01-30 21:08:50 UTC] — User: amara.shah (assoc_100211)
-- Pulling traffic conversion summary weekly aggregates for US market.
SELECT 
    fiscal_week_ending,
    SUM(sessions) as weekly_sessions,
    SUM(orders) as weekly_orders,
    AVG(conversion_rate) as avg_conversion
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'US'
GROUP BY 1
ORDER BY fiscal_week_ending DESC
LIMIT 12;

### [2026-01-30 22:01:19 UTC] — User: giulia.romano (assoc_100213)
-- Checking care contacts resolution codes distribution.
SELECT 
    resolution_code,
    COUNT(*) as contact_count,
    AVG(handle_time_minutes) as mean_handle_time
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1
ORDER BY contact_count DESC;

### [2026-01-30 23:15:30 UTC] — User: connor.blake (assoc_100212)
-- Auditing dim vertical deep dive flags and taxonomy.
SELECT 
    vertical_code,
    vertical_name,
    is_deep_dive
FROM `nexus-analyst-demo.acme_ecomm.dim_vertical`
WHERE is_deep_dive = TRUE;

### [2026-01-30 23:45:10 UTC] — User: amara.shah (assoc_100211)
-- Re-running weekly regional conversion summary to verify Q4 peak adjustments.
SELECT 
    market,
    fiscal_week_ending,
    SUM(sessions) as total_sessions,
    SUM(orders) as total_orders,
    AVG(conversion_rate) as mean_conversion
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE fiscal_week_ending >= '2025-11-01'
GROUP BY 1, 2
ORDER BY fiscal_week_ending DESC, market ASC;

### [2026-01-31 00:12:33 UTC] — User: connor.blake (assoc_100212)
-- Checking partition sizes on fact_orders for December 2025 peak volume.
SELECT 
    DATE_TRUNC(order_date, WEEK) as order_week,
    channel,
    COUNT(*) as total_orders,
    SUM(gmv_usd) as weekly_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE order_date BETWEEN '2025-12-01' AND '2025-12-31'
GROUP BY 1, 2
ORDER BY order_week ASC;

### [2026-01-31 01:05:48 UTC] — User: wei.hartono (assoc_100210)
-- Validating dim_member panel distribution across home markets.
SELECT 
    home_market,
    plan_type,
    status,
    COUNT(*) as panel_member_count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
GROUP BY 1, 2, 3;

### [2026-01-31 02:20:11 UTC] — User: giulia.romano (assoc_100213)
-- Pulling voc responses sentiment breakdown for post purchase surveys.
SELECT 
    theme_tag,
    sentiment,
    COUNT(*) as response_count,
    AVG(score) as avg_score
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE survey_type = 'post_purchase'
  AND responded_at >= '2025-11-01'
GROUP BY 1, 2
ORDER BY response_count DESC
LIMIT 15;

### [2026-01-31 03:11:05 UTC] — User: tara.oduya (assoc_100140)
-- Checking fulfillment speed daily metrics for ship to home vs bopis during holiday storm.
SELECT 
    date,
    fulfillment_type,
    orders_promised,
    on_time_rate,
    avg_cost_per_order_usd
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE date BETWEEN '2025-12-05' AND '2025-12-15'
  AND fulfillment_type IN ('ship_to_home', 'bopis')
ORDER BY date DESC;

### [2026-01-31 04:02:50 UTC] — User: amara.shah (assoc_100211)
-- Quarterly finance check on marketplace gmv summary for collectibles sub-vertical.
SELECT 
    fiscal_week_ending,
    gmv_usd,
    orders,
    take_rate
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE sub_vertical_code = 'COLLECTIBLES'
  AND fiscal_week_ending >= '2025-08-01'
ORDER BY fiscal_week_ending DESC;

### [2026-01-31 05:30:19 UTC] — User: connor.blake (assoc_100212)
-- Inspecting dim_fulfillment_node active records for returns centers.
SELECT 
    node_id,
    node_name,
    market,
    opened_date
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE node_type = 'returns_center';

### [2026-01-31 06:15:44 UTC] — User: wei.hartono (assoc_100210)
-- Checking experiment exposure aggregations for running membership tests.
SELECT 
    experiment_id,
    variant,
    SUM(units_assigned) as assigned,
    SUM(units_exposed) as exposed
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures`
GROUP BY 1, 2;

### [2026-01-31 07:08:22 UTC] — User: giulia.romano (assoc_100213)
-- Auditing care contacts sub program distribution for avoidance channels.
SELECT 
    sub_program,
    channel,
    COUNT(*) as contact_count,
    AVG(csat_score) as mean_csat
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at >= '2026-01-01'
GROUP BY 1, 2;

### [2026-01-31 08:41:02 UTC] — User: tara.oduya (assoc_100140)
-- Reviewing fulfillment speed promise vs actual performance by node for sortation hubs.
SELECT 
    node_id,
    SUM(orders_promised) as total_promised,
    SUM(orders_on_time) as total_on_time,
    AVG(avg_days_late_when_late) as mean_days_late
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE date >= '2026-01-01'
GROUP BY 1;

### [2026-01-31 09:19:50 UTC] — User: amara.shah (assoc_100211)
-- Checking member cltv panel aggregations grouped by signup cohort quarter.
SELECT 
    signup_cohort_quarter,
    COUNT(*) as member_count,
    AVG(lifetime_gmv_usd) as avg_lifetime_gmv,
    AVG(projected_cltv_usd) as avg_projected_cltv
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`
GROUP BY 1
ORDER BY signup_cohort_quarter DESC;

### [2026-01-31 10:04:15 UTC] — User: connor.blake (assoc_100212)
-- Verifying seller status distribution in dim_seller panel.
SELECT 
    status,
    category_focus,
    fulfillment_method,
    COUNT(*) as seller_count
FROM `nexus-analyst-demo.acme_ecomm.dim_seller`
GROUP BY 1, 2, 3;

### [2026-01-31 11:25:30 UTC] — User: wei.hartono (assoc_100210)
-- Pulling traffic daily totals for web versus app devices in US market.
SELECT 
    date,
    device,
    SUM(sessions) as total_sessions,
    SUM(orders) as total_orders
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE market = 'US'
  AND date >= '2026-01-01'
GROUP BY 1, 2
ORDER BY date DESC;

### [2026-01-31 12:50:08 UTC] — User: giulia.romano (assoc_100213)
-- Checking care contacts deflection rates by sub program for January.
SELECT 
    sub_program,
    SUM(case when deflected then 1 else 0 end) * 100.0 / COUNT(*) as deflection_pct,
    AVG(handle_time_minutes) as avg_handle_time
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at >= '2026-01-01'
GROUP BY 1;

### [2026-01-31 13:33:41 UTC] — User: tara.oduya (assoc_100140)
-- Inspecting marketplace seller performance trailing 90 day gmv for resold category.
SELECT 
    seller_id,
    active_listings,
    trailing_90d_gmv_usd,
    return_rate
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
WHERE category_focus = 'resold'
ORDER BY trailing_90d_gmv_usd DESC
LIMIT 20;

### [2026-01-31 14:14:20 UTC] — User: amara.shah (assoc_100211)
-- Pulling weekly traffic conversion summary for Canada market.
SELECT 
    fiscal_week_ending,
    SUM(sessions) as weekly_sessions,
    SUM(gmv_usd) as weekly_gmv,
    AVG(conversion_rate) as avg_conv
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'CA'
GROUP BY 1
ORDER BY fiscal_week_ending DESC
LIMIT 10;

### [2026-01-31 15:02:19 UTC] — User: connor.blake (assoc_100212)
-- Checking dim_date flags for peak holiday week ends in Q4.
SELECT 
    date,
    fiscal_quarter_label,
    is_peak_holiday,
    day_of_week
FROM `nexus-analyst-demo.acme_ecomm.dim_date`
WHERE is_peak_holiday = TRUE
ORDER BY date DESC;

### [2026-01-31 16:45:12 UTC] — User: wei.hartono (assoc_100210)
-- Running experiment readouts query for active optimization tests.
SELECT 
    experiment_id,
    variant,
    metric_name,
    metric_value,
    is_significant
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`
WHERE as_of_date >= '2026-01-01';

### [2026-01-31 17:22:50 UTC] — User: giulia.romano (assoc_100213)
-- Pulling membership events breakdown by event type for January.
SELECT 
    event_type,
    channel,
    COUNT(*) as event_count
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
WHERE event_date >= '2026-01-01'
GROUP BY 1, 2;

### [2026-01-31 18:10:04 UTC] — User: tara.oduya (assoc_100140)
-- Checking marketplace gmv summary for style sub vertical weekly totals.
SELECT 
    fiscal_week_ending,
    SUM(gmv_usd) as style_gmv,
    SUM(orders) as style_orders
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE sub_vertical_code = 'STYLE'
GROUP BY 1
ORDER BY fiscal_week_ending DESC;

### [2026-01-31 19:05:33 UTC] — User: amara.shah (assoc_100211)
-- Running cross vertical validation check on fact_orders sample records.
SELECT 
    vertical_code,
    channel,
    fulfillment_type,
    COUNT(*) as order_count,
    SUM(gmv_usd) as total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE order_date >= '2026-01-01'
GROUP BY 1, 2, 3;

### [2026-01-31 20:11:45 UTC] — User: connor.blake (assoc_100212)
-- Auditing dim_vertical rows and sub vertical definitions.
SELECT 
    vertical_code,
    vertical_name,
    sub_vertical_code,
    sub_vertical_name
FROM `nexus-analyst-demo.acme_ecomm.dim_vertical`
ORDER BY vertical_code ASC;

### [2026-01-31 21:30:10 UTC] — User: wei.hartono (assoc_100210)
-- Checking fact_marketplace_listings active status distribution by category.
SELECT 
    category,
    status,
    authenticity_verified,
    COUNT(*) as listing_count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY 1, 2, 3;

### [2026-01-31 22:15:02 UTC] — User: giulia.romano (assoc_100213)
-- Pulling care deflection daily summary aggregates for January.
SELECT 
    date,
    sub_program,
    contact_volume,
    deflection_rate,
    avg_csat_deflected
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
WHERE date >= '2026-01-01'
ORDER BY date DESC, sub_program ASC;

### [2026-01-31 23:04:18 UTC] — User: tara.oduya (assoc_100140)
-- Checking fulfillment speed daily metrics for efficiency column across nodes.
SELECT 
    date,
    market,
    fulfillment_type,
    avg_cost_per_order_usd
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE date >= '2026-01-01'
ORDER BY date DESC
LIMIT 25;

### [2026-02-01 00:11:50 UTC] — User: amara.shah (assoc_100211)
-- FY27 opening query: pulling monthly traffic and conversion aggregates for financial reporting pack.
SELECT 
    DATE_TRUNC(fiscal_week_ending, MONTH) as fiscal_month,
    market,
    SUM(sessions) as monthly_sessions,
    SUM(orders) as monthly_orders,
    SUM(gmv_usd) as monthly_gmv
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
GROUP BY 1, 2
ORDER BY fiscal_month DESC;

### [2026-02-01 01:25:09 UTC] — User: connor.blake (assoc_100212)
-- Auditing dim_associate records for active staff in data and analytics team.
SELECT 
    assoc_id,
    full_name,
    role,
    team,
    location
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
WHERE team = 'Data'
  AND is_active = TRUE;

### [2026-02-01 02:40:15 UTC] — User: wei.hartono (assoc_100210)
-- Checking fact_experiment_exposures totals across active experiments for February kickoff.
SELECT 
    experiment_id,
    variant,
    SUM(units_exposed) as total_exposed,
    SUM(units_converted) as total_converted
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures`
GROUP BY 1, 2;

### [2026-02-01 03:15:33 UTC] — User: giulia.romano (assoc_100213)
-- Pulling voc responses for post care contact surveys in January.
SELECT 
    theme_tag,
    sentiment,
    COUNT(*) as count_responses
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE survey_type = 'post_care_contact'
  AND responded_at >= '2026-01-01'
GROUP BY 1, 2
ORDER BY count_responses DESC;

### [2026-02-01 04:08:42 UTC] — User: tara.oduya (assoc_100140)
-- Checking marketplace seller performance metrics for collectibles category focus.
SELECT 
    seller_id,
    active_listings,
    trailing_90d_gmv_usd,
    authenticity_flag_count
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
WHERE category_focus = 'collectibles'
ORDER BY trailing_90d_gmv_usd DESC;

### [2026-02-01 05:22:11 UTC] — User: amara.shah (assoc_100211)
-- Running check on marketplace gmv summary take rates across all sub verticals.
SELECT 
    sub_vertical_code,
    AVG(take_rate) as average_take_rate,
    SUM(gmv_usd) as total_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
GROUP BY 1;

### [2026-02-01 06:14:50 UTC] — User: connor.blake (assoc_100212)
-- Verifying dim_fulfillment_node records for distribution centers in US market.
SELECT 
    node_id,
    node_type,
    node_name,
    market
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE market = 'US'
  AND node_type IN ('dc', 'fc');

### [2026-02-01 07:02:30 UTC] — User: wei.hartono (assoc_100210)
-- Checking traffic daily sessions definition version distribution in fact_traffic_daily.
SELECT 
    sessions_definition_version,
    COUNT(*) as row_count,
    SUM(sessions) as sum_sessions
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
GROUP BY 1;

### [2026-02-01 08:35:19 UTC] — User: giulia.romano (assoc_100213)
-- Pulling care contacts resolution codes for chat channel interactions.
SELECT 
    resolution_code,
    COUNT(*) as contact_count,
    AVG(handle_time_minutes) as mean_handle_time
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE channel = 'chat'
GROUP BY 1
ORDER BY contact_count DESC;

### [2026-02-01 09:20:04 UTC] — User: tara.oduya (assoc_100140)
-- Checking fulfillment speed daily on time rates for store fulfillment types.
SELECT 
    date,
    fulfillment_type,
    orders_promised,
    on_time_rate
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE fulfillment_type IN ('bopis', 'curbside', 'dfs')
  AND date >= '2026-01-01'
ORDER BY date DESC
LIMIT 20;

### [2026-02-01 10:11:40 UTC] — User: amara.shah (assoc_100211)
-- Running member cltv summary check for active members in annual plan type.
SELECT 
    tenure_days,
    COUNT(*) as member_count,
    AVG(trailing_12mo_gmv_usd) as avg_trailing_gmv
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`
GROUP BY 1
ORDER BY tenure_days DESC
LIMIT 25;

### [2026-02-01 11:05:22 UTC] — User: connor.blake (assoc_100212)
-- Auditing dim_experiment table for experiments running into Q1FY27.
SELECT 
    experiment_id,
    experiment_name,
    vertical_code,
    status,
    primary_metric
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment`
WHERE status = 'running';

### [2026-02-01 12:44:09 UTC] — User: wei.hartono (assoc_100210)
-- Running test query on traffic conversion summary with week ending filter.
SELECT 
    fiscal_week_ending,
    market,
    vertical_code,
    conversion_rate
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'US'
  AND vertical_code = 'US_CONV'
ORDER BY fiscal_week_ending DESC
LIMIT 10;

### [2026-02-01 13:19:55 UTC] — User: giulia.romano (assoc_100213)
-- Checking fact_orders refund columns for returned orders in January 2026.
SELECT 
    return_reason_code,
    COUNT(*) as return_count,
    AVG(refund_usd) as avg_refund_amount
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE is_returned = TRUE
  AND order_date >= '2026-01-01'
GROUP BY 1
ORDER BY return_count DESC;

### [2026-02-01 14:02:18 UTC] — User: tara.oduya (assoc_100140)
-- Pulling marketplace seller performance average days to ship by category focus.
SELECT 
    category_focus,
    AVG(avg_days_to_ship) as mean_days_to_ship,
    AVG(avg_buyer_rating) as mean_buyer_rating
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
GROUP BY 1;

### [2026-02-01 15:10:33 UTC] — User: amara.shah (assoc_100211)
-- Checking marketing calendar planned versus actual spend for Q4 campaigns.
SELECT 
    event_id,
    event_name,
    event_type,
    planned_spend_usd,
    actual_spend_usd
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
WHERE start_date BETWEEN '2025-11-01' AND '2025-12-31';

### [2026-02-01 16:25:40 UTC] — User: connor.blake (assoc_100212)
-- Checking marketplace listings authenticity verified distribution across categories.
SELECT 
    category,
    authenticity_verified,
    COUNT(*) as listings_total,
    AVG(price_usd) as mean_price
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY 1, 2;

### [2026-02-01 17:08:12 UTC] — User: wei.hartono (assoc_100210)
-- Running aggregate exposure check by variant on experiment exposures table.
SELECT 
    experiment_id,
    variant,
    SUM(units_assigned) as assigned_total
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures`
GROUP BY 1, 2;

### [2026-02-01 18:33:01 UTC] — User: giulia.romano (assoc_100213)
-- Pulling care contacts volume by channel and sub program.
SELECT 
    channel,
    sub_program,
    COUNT(*) as contact_volume,
    AVG(csat_score) as avg_csat
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1, 2;

### [2026-02-01 19:14:50 UTC] — User: tara.oduya (assoc_100140)
-- Checking marketplace gmv summary take rates for resold sub vertical.
SELECT 
    fiscal_week_ending,
    gmv_usd,
    take_rate
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE sub_vertical_code = 'RESOLD'
ORDER BY fiscal_week_ending DESC
LIMIT 15;

### [2026-02-01 20:02:19 UTC] — User: amara.shah (assoc_100211)
-- Running weekly aggregates check on traffic conversion summary for US market.
SELECT 
    fiscal_week_ending,
    SUM(sessions) as us_sessions,
    SUM(orders) as us_orders
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'US'
GROUP BY 1
ORDER BY fiscal_week_ending DESC
LIMIT 10;

### [2026-02-01 21:45:08 UTC] — User: connor.blake (assoc_100212)
-- Auditing dim_vertical table records where is_deep_dive is true.
SELECT 
    vertical_code,
    vertical_name,
    customer_facing_desc
FROM `nexus-analyst-demo.acme_ecomm.dim_vertical`
WHERE is_deep_dive = TRUE;

### [2026-02-01 22:19:42 UTC] — User: wei.hartono (assoc_100210)
-- Checking fact_promise_vs_actual aggregate records for January 2026.
SELECT 
    market,
    fulfillment_type,
    SUM(orders_promised) as promised_total,
    SUM(orders_on_time) as on_time_total
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE date >= '2026-01-01'
GROUP BY 1, 2;

### [2026-02-01 23:08:15 UTC] — User: giulia.romano (assoc_100213)
-- Pulling care deflection daily metrics for optimization sub program.
SELECT 
    date,
    contact_volume,
    deflection_rate,
    avg_handle_time_minutes
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
WHERE sub_program = 'optimize'
ORDER BY date DESC
LIMIT 20;

### [2026-01-23 00:15:42 UTC] — User: amara.shah (assoc_100211)
-- Re-running monthly finance reconciliation query on traffic conversion summary to check regional sums.
SELECT 
    market,
    SUM(sessions) as total_sessions,
    SUM(gmv_usd) as total_gmv
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE fiscal_week_ending >= '2026-01-01'
GROUP BY market;

### [2026-01-23 01:22:11 UTC] — User: connor.blake (assoc_100212)
-- Checking partition stats on fact_orders for table maintenance.
SELECT 
    table_name,
    partition_id,
    row_count
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'fact_orders'
ORDER BY partition_id DESC
LIMIT 10;

### [2026-01-23 03:04:38 UTC] — User: giulia.romano (assoc_100213)
-- Pulling care contacts distribution across channels for yesterday.
SELECT 
    channel,
    COUNT(*) as contact_count,
    AVG(handle_time_minutes) as avg_handle_time
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE DATE(opened_at) = '2026-01-22'
GROUP BY 1;

### [2026-01-23 04:18:50 UTC] — User: wei.hartono (assoc_100210)
-- Validating dim_fulfillment_node active flags across fulfillment center types.
SELECT 
    node_type,
    market,
    COUNT(*) as node_count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE is_active = TRUE
GROUP BY 1, 2;

### [2026-01-23 06:11:29 UTC] — User: tara.oduya (assoc_100140)
-- Checking daily fulfillment speed promise vs actual metrics for January.
SELECT 
    date,
    fulfillment_type,
    SUM(orders_promised) as promised,
    SUM(orders_on_time) as on_time
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE date BETWEEN '2026-01-01' AND '2026-01-22'
GROUP BY 1, 2
ORDER BY date DESC
LIMIT 15;

### [2026-01-23 08:33:04 UTC] — User: amara.shah (assoc_100211)
-- Checking marketplace gmv summary take rates for collectibles sub vertical.
SELECT 
    fiscal_week_ending,
    gmv_usd,
    orders,
    take_rate
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE sub_vertical_code = 'COLLECTIBLES'
ORDER BY fiscal_week_ending DESC
LIMIT 10;

### [2026-01-23 09:45:12 UTC] — User: connor.blake (assoc_100212)
-- Auditing dim_associate records for active management hierarchy.
SELECT 
    team,
    COUNT(*) as headcount
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
WHERE is_active = TRUE
GROUP BY 1;

### [2026-01-23 11:02:55 UTC] — User: giulia.romano (assoc_100213)
-- Checking voc responses distribution by survey type and sentiment.
SELECT 
    survey_type,
    sentiment,
    COUNT(*) as response_count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
GROUP BY 1, 2;

### [2026-01-23 12:30:19 UTC] — User: wei.hartono (assoc_100210)
-- Verifying experiment exposure records for active Q4 experiments.
SELECT 
    experiment_id,
    variant,
    SUM(units_exposed) as exposed_units
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures`
GROUP BY 1, 2;

### [2026-01-23 14:15:40 UTC] — User: tara.oduya (assoc_100140)
-- Pulling fulfillment speed daily metrics for efficiency sub program view.
SELECT 
    date,
    fulfillment_type,
    on_time_rate,
    avg_cost_per_order_usd
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE market = 'US'
ORDER BY date DESC
LIMIT 12;

### [2026-01-23 16:04:22 UTC] — User: amara.shah (assoc_100211)
-- Checking dim_member distribution by plan type and home market.
SELECT 
    home_market,
    plan_type,
    COUNT(*) as member_count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
WHERE status = 'active'
GROUP BY 1, 2;

### [2026-01-23 17:51:03 UTC] — User: connor.blake (assoc_100212)
-- Checking table sizes across the acme_ecomm dataset.
SELECT 
    table_name,
    row_count,
    size_bytes
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.TABLE_STORAGE`
ORDER BY size_bytes DESC;

### [2026-01-23 19:12:38 UTC] — User: giulia.romano (assoc_100213)
-- Pulling care deflection daily summary for optimization program.
SELECT 
    date,
    contact_volume,
    deflection_rate,
    avg_csat_deflected
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
WHERE sub_program = 'optimize'
ORDER BY date DESC
LIMIT 10;

### [2026-01-23 21:05:41 UTC] — User: wei.hartono (assoc_100210)
-- Pulling traffic conversion summary weekly aggregates for US market.
SELECT 
    fiscal_week_ending,
    sessions,
    orders,
    conversion_rate
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'US'
ORDER BY fiscal_week_ending DESC
LIMIT 10;

### [2026-01-23 22:40:15 UTC] — User: tara.oduya (assoc_100140)
-- Checking marketplace seller performance metrics for active collectibles listings.
SELECT 
    seller_id,
    category_focus,
    active_listings,
    trailing_90d_gmv_usd
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
WHERE category_focus = 'collectibles'
ORDER BY trailing_90d_gmv_usd DESC
LIMIT 10;

### [2026-01-24 01:11:33 UTC] — User: amara.shah (assoc_100211)
-- Pulling membership events breakdown by event type for January 2026.
SELECT 
    event_type,
    COUNT(*) as event_count
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
WHERE event_date >= '2026-01-01'
GROUP BY 1;

### [2026-01-24 03:22:04 UTC] — User: connor.blake (assoc_100212)
-- Auditing dim_experiment status records.
SELECT 
    status,
    vertical_code,
    COUNT(*) as exp_count
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment`
GROUP BY 1, 2;

### [2026-01-24 05:04:19 UTC] — User: giulia.romano (assoc_100213)
-- Checking fact_care_contacts resolution codes distribution.
SELECT 
    resolution_code,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1
ORDER BY count DESC
LIMIT 10;

### [2026-01-24 07:15:50 UTC] — User: wei.hartono (assoc_100210)
-- Validating dim_vertical table structure and codes.
SELECT 
    vertical_code,
    vertical_name,
    sub_vertical_code
FROM `nexus-analyst-demo.acme_ecomm.dim_vertical`
ORDER BY vertical_code;

### [2026-01-24 09:30:11 UTC] — User: tara.oduya (assoc_100140)
-- Checking marketplace gmv summary for resold sub vertical.
SELECT 
    fiscal_week_ending,
    gmv_usd,
    orders
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE sub_vertical_code = 'RESOLD'
ORDER BY fiscal_week_ending DESC
LIMIT 10;

### [2026-01-24 11:12:44 UTC] — User: amara.shah (assoc_100211)
-- Pulling member cltv summary statistics.
SELECT 
    signup_cohort_quarter,
    COUNT(*) as member_count,
    AVG(lifetime_gmv_usd) as avg_lifetime_gmv
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`
GROUP BY 1
ORDER BY signup_cohort_quarter DESC;

### [2026-01-24 13:04:22 UTC] — User: connor.blake (assoc_100212)
-- Checking dim_marketing_calendar event types.
SELECT 
    event_type,
    COUNT(*) as count
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
GROUP BY 1;

### [2026-01-24 15:20:08 UTC] — User: giulia.romano (assoc_100213)
-- Pulling recent voc responses with negative sentiment.
SELECT 
    response_id,
    survey_type,
    score,
    verbatim_text
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE sentiment = 'negative'
ORDER BY responded_at DESC
LIMIT 10;

### [2026-01-24 17:05:39 UTC] — User: wei.hartono (assoc_100210)
-- Checking traffic daily aggregates for mobile app sessions in US.
SELECT 
    date,
    SUM(sessions) as app_sessions,
    SUM(orders) as app_orders
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE market = 'US' AND device = 'app' AND date >= '2026-01-01'
GROUP BY 1
ORDER BY date DESC;

### [2026-01-24 19:40:15 UTC] — User: tara.oduya (assoc_100140)
-- Pulling fulfillment speed daily metrics for fulfillment type comparison.
SELECT 
    fulfillment_type,
    AVG(on_time_rate) as avg_on_time,
    AVG(avg_cost_per_order_usd) as avg_cost
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
GROUP BY 1;

### [2026-01-24 21:12:50 UTC] — User: amara.shah (assoc_100211)
-- Checking marketplace seller performance average return rates.
SELECT 
    category_focus,
    AVG(return_rate) as avg_return_rate,
    AVG(avg_days_to_ship) as avg_ship_days
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
GROUP BY 1;

### [2026-01-24 23:04:18 UTC] — User: connor.blake (assoc_100212)
-- Auditing dim_seller records by category focus and status.
SELECT 
    category_focus,
    status,
    COUNT(*) as seller_count
FROM `nexus-analyst-demo.acme_ecomm.dim_seller`
GROUP BY 1, 2;

### [2026-01-25 01:15:33 UTC] — User: giulia.romano (assoc_100213)
-- Pulling care deflection daily summary for automate sub program.
SELECT 
    date,
    contact_volume,
    deflection_rate
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
WHERE sub_program = 'automate'
ORDER BY date DESC
LIMIT 10;

### [2026-01-25 03:22:04 UTC] — User: wei.hartono (assoc_100210)
-- Checking fact_promise_vs_actual records for node performance.
SELECT 
    node_id,
    SUM(orders_promised) as total_promised,
    SUM(orders_on_time) as total_on_time
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE node_id IS NOT NULL
GROUP BY 1
ORDER BY total_promised DESC
LIMIT 10;

### [2026-01-25 05:10:49 UTC] — User: tara.oduya (assoc_100140)
-- Checking marketplace gmv summary for style sub vertical.
SELECT 
    fiscal_week_ending,
    gmv_usd,
    orders
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE sub_vertical_code = 'STYLE'
ORDER BY fiscal_week_ending DESC
LIMIT 10;

### [2026-01-25 07:45:12 UTC] — User: amara.shah (assoc_100211)
-- Running weekly aggregates check on traffic conversion summary for CA market.
SELECT 
    fiscal_week_ending,
    SUM(sessions) as ca_sessions,
    SUM(orders) as ca_orders
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'CA'
GROUP BY 1
ORDER BY fiscal_week_ending DESC
LIMIT 10;

### [2026-01-25 09:18:25 UTC] — User: connor.blake (assoc_100212)
-- Checking dim_date records for peak holiday flags in January 2026.
SELECT 
    date,
    fiscal_week,
    is_peak_holiday
FROM `nexus-analyst-demo.acme_ecomm.dim_date`
WHERE date BETWEEN '2026-01-01' AND '2026-01-25';

### [2026-01-25 11:04:50 UTC] — User: giulia.romano (assoc_100213)
-- Pulling care contacts by channel for member care sub program.
SELECT 
    channel,
    COUNT(*) as contact_count,
    AVG(csat_score) as avg_csat
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE sub_program = 'member_care'
GROUP BY 1;

### [2026-01-25 13:30:19 UTC] — User: wei.hartono (assoc_100210)
-- Verifying fact_orders refund columns for recent returns.
SELECT 
    order_id,
    return_reason_code,
    refund_usd,
    refund_issued_date
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE is_returned = TRUE AND refund_issued_date IS NOT NULL
ORDER BY refund_issued_date DESC
LIMIT 10;

### [2026-01-25 15:15:42 UTC] — User: tara.oduya (assoc_100140)
-- Checking marketplace listings authenticity verified status breakdown.
SELECT 
    category,
    authenticity_verified,
    COUNT(*) as listing_count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY 1, 2;

### [2026-01-25 17:02:11 UTC] — User: amara.shah (assoc_100211)
-- Running monthly reconciliation query on traffic conversion summary for MX market.
SELECT 
    fiscal_week_ending,
    SUM(sessions) as mx_sessions,
    SUM(gmv_usd) as mx_gmv
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'MX'
GROUP BY 1
ORDER BY fiscal_week_ending DESC
LIMIT 10;

### [2026-01-25 19:20:05 UTC] — User: connor.blake (assoc_100212)
-- Auditing dim_vertical records where vertical_code is US_CONV or MARKETPLACE.
SELECT 
    vertical_code,
    vertical_name,
    sub_vertical_code,
    sub_vertical_name
FROM `nexus-analyst-demo.acme_ecomm.dim_vertical`
WHERE vertical_code IN ('US_CONV', 'MARKETPLACE');