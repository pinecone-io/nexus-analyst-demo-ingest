---
title: "BigQuery analyst query audit log — Q1FY26 & Q2FY26 (2025-02 through 2025-07)"
source_url: "internal://acme-ecomm/query_logs/bulk__q1fy26-q2fy26-bq-audit-log"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2025-04-15T12:00:00+00:00'
adapter: bq_query_log
---

# BigQuery Audit Log Export: `nexus-analyst-demo.acme_ecomm`
**Export Window:** 2025-02-01 00:00:00 UTC to 2025-07-31 23:59:59 UTC
**Dataset Target:** `nexus-analyst-demo.acme_ecomm`
**Authorized Users:** Data & Analytics Team (`wei.hartono`, `amara.shah`, `connor.blake`, `giulia.romano`), Analytics Engineering, and Product Management self-serve users (`maya.lindqvist`, `owen.faust`, `sanjay.bhatt`, `ines.delgado`, `noah.kessler`).

---

### Audit Log Entries

#### 2025-02-01 04:15:22 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9981240182_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 42,109,312 bytes
* **Duration:** 1.24s
* **Query Text:**
```sql
-- Initial quarterly validation check for FY26 opening week
SELECT 
  date,
  market,
  vertical_code,
  SUM(sessions) AS total_sessions,
  SUM(orders) AS total_orders,
  ROUND(SUM(gmv_usd), 2) AS total_gmv_usd
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date BETWEEN '2025-02-01' AND '2025-02-07'
GROUP BY 1, 2, 3
ORDER BY date DESC, total_gmv_usd DESC;
```

#### 2025-02-01 09:30:11 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9981245910_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 1,204,500 bytes
* **Duration:** 0.45s
* **Query Text:**
```sql
-- Checking dimension table row counts for dim_date and dim_vertical post-FY26 rollover
SELECT 
  vertical_code, 
  vertical_name, 
  is_deep_dive 
FROM `nexus-analyst-demo.acme_ecomm.dim_vertical`
WHERE is_deep_dive = TRUE;
```

#### 2025-02-02 11:12:00 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9981288391_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 12,480,900 bytes
* **Duration:** 0.82s
* **Query Text:**
```sql
-- Pipeline freshness check: max date in fact_fulfillment_node / fact_promise_vs_actual
SELECT 
  market, 
  vertical_code, 
  MAX(date) AS latest_date,
  SUM(orders_promised) AS total_promised
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
GROUP BY 1, 2;
```

#### 2025-02-03 14:22:45 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9981399201_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 84,200,100 bytes
* **Duration:** 2.10s
* **Query Text:**
```sql
-- Care contact volume baseline check by sub_program for Jan closing
SELECT 
  sub_program,
  channel,
  COUNT(contact_id) AS contact_count,
  AVG(csat_score) AS avg_csat
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1, 2;
```

#### 2025-02-04 08:05:33 UTC
* **User:** `maya.lindqvist` (assoc_100110)
* **Job ID:** `bq_job_9981500112_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 310,400,000 bytes
* **Duration:** 3.85s
* **Query Text:**
```sql
-- US Conversion traffic check for US_CONV team review
SELECT 
  date,
  device,
  SUM(sessions) AS sessions,
  SUM(orders) AS orders,
  SAFE_DIVIDE(SUM(orders), SUM(sessions)) AS conversion_rate
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE market = 'US' AND vertical_code = 'US_CONV' AND date >= '2025-01-01'
GROUP BY 1, 2
ORDER BY date DESC;
```

#### 2025-02-05 16:45:19 UTC
* **User:** `owen.faust` (assoc_100111)
* **Job ID:** `bq_job_9981711209_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 45,100,000 bytes
* **Duration:** 1.15s
* **Query Text:**
```sql
-- Checking active experiments count in dim_experiment
SELECT experiment_id, experiment_name, vertical_code, status, start_date
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment`
WHERE status = 'running';
```

#### 2025-02-06 10:20:00 UTC
* **User:** `sanjay.bhatt` (assoc_100120)
* **Job ID:** `bq_job_9981855019_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 98,200,400 bytes
* **Duration:** 1.95s
* **Query Text:**
```sql
-- Marketplace Collectibles baseline listing check
SELECT 
  category,
  COUNT(listing_id) AS total_listings,
  AVG(price_usd) AS avg_price
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
WHERE category = 'collectibles'
GROUP BY 1;
```

#### 2025-02-07 13:11:42 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9982001928_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 15,200,000 bytes
* **Duration:** 0.65s
* **Query Text:**
```sql
-- Quick check on marketing calendar budget allocations for Feb
SELECT event_id, event_name, event_type, planned_spend_usd, actual_spend_usd
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
WHERE start_date BETWEEN '2025-02-01' AND '2025-02-28';
```

#### 2025-02-08 09:00:15 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9982104921_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 5,400,000 bytes
* **Duration:** 0.33s
* **Query Text:**
```sql
-- Testing join between dim_associate and dim_experiment owners
SELECT e.experiment_id, e.experiment_name, a.full_name AS owner_name, a.team
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment` e
LEFT JOIN `nexus-analyst-demo.acme_ecomm.dim_associate` a ON e.owner_assoc_id = a.assoc_id;
```

#### 2025-02-10 11:45:00 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9982400182_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 210,500,000 bytes
* **Duration:** 2.45s
* **Query Text:**
```sql
-- Checking order volume distribution across fulfillment types in fact_orders sample
SELECT fulfillment_type, channel, COUNT(order_id) AS sample_orders, SUM(gmv_usd) AS sample_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
GROUP BY 1, 2;
```

#### 2025-02-12 15:30:22 UTC
* **User:** `derek.holloway` (assoc_100151)
* **Job ID:** `bq_job_9982899102_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 18,900,000 bytes
* **Duration:** 0.78s
* **Query Text:**
```sql
-- Membership panel check: verifying dim_member count and active statuses
-- NOTE: remember this is the 120,000 representative panel, NOT the full ~14M base!
SELECT status, plan_type, COUNT(*) AS panel_count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
GROUP BY 1, 2;
```

#### 2025-02-14 08:15:10 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9983104920_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 76,400,000 bytes
* **Duration:** 1.50s
* **Query Text:**
```sql
-- VOC survey sentiment breakdown for post_purchase
SELECT sentiment, theme_tag, COUNT(response_id) AS response_count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE survey_type = 'post_purchase'
GROUP BY 1, 2
ORDER BY response_count DESC;
```

#### 2025-02-15 14:20:05 UTC
* **User:** `ines.delgado` (assoc_100121)
* **Job ID:** `bq_job_9983350192_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 54,200,000 bytes
* **Duration:** 1.12s
* **Query Text:**
```sql
-- Marketplace Style listings and average price check
SELECT category, status, COUNT(*) AS listing_count, AVG(price_usd) AS avg_price
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
WHERE category = 'style'
GROUP BY 1, 2;
```

#### 2025-02-18 09:10:44 UTC
* **User:** `tara.oduya` (assoc_100140)
* **Job ID:** `bq_job_9983801293_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 125,000,000 bytes
* **Duration:** 1.88s
* **Query Text:**
```sql
-- Speed and fulfillment daily aggregation for US market
SELECT date, fulfillment_type, SUM(orders_promised) AS promised, SUM(orders_on_time) AS on_time,
       SAFE_DIVIDE(SUM(orders_on_time), SUM(orders_promised)) AS otp_rate
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE market = 'US' AND date >= '2025-02-01'
GROUP BY 1, 2
ORDER BY date DESC;
```

#### 2025-02-20 11:00:00 UTC
* **User:** `malik.hendon` (assoc_100160)
* **Job ID:** `bq_job_9984129402_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 8,500,000 bytes
* **Duration:** 0.41s
* **Query Text:**
```sql
-- Exploring B2B vertical rows in dim_vertical
SELECT * FROM `nexus-analyst-demo.acme_ecomm.dim_vertical`
WHERE vertical_code = 'B2B';
```

#### 2025-02-22 16:33:12 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9984501923_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 340,100,000 bytes
* **Duration:** 4.10s
* **Query Text:**
```sql
-- US Conversion verification query against traffic_conversion_summary
-- Tracking Q1 figures toward canonical 3.05% US conversion target
SELECT 
  fiscal_week_ending,
  market,
  sessions,
  orders,
  conversion_rate,
  gmv_usd
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'US' AND vertical_code = 'US_CONV'
ORDER BY fiscal_week_ending DESC;
```

#### 2025-02-25 10:15:30 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9985019234_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 19,400,000 bytes
* **Duration:** 0.72s
* **Query Text:**
```sql
-- Checking fulfillment node types and markets
SELECT node_type, market, COUNT(*) AS node_count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE is_active = TRUE
GROUP BY 1, 2;
```

#### 2025-02-28 14:00:11 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9985610293_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 512,000,000 bytes
* **Duration:** 5.30s
* **Query Text:**
```sql
-- Monthly partition / table scan validation for fact_orders sample across Q1
SELECT 
  EXTRACT(MONTH FROM order_date) AS order_month,
  market,
  COUNT(order_id) AS total_orders,
  SUM(gmv_usd) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
GROUP BY 1, 2
ORDER BY order_month;
```

#### 2025-03-02 09:20:44 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9986102934_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 64,100,000 bytes
* **Duration:** 1.25s
* **Query Text:**
```sql
-- Checking session definition version split in fact_traffic_daily around cutover date
SELECT 
  sessions_definition_version,
  MIN(date) AS min_date,
  MAX(date) AS max_date,
  SUM(sessions) AS total_sessions
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
GROUP BY 1;
```

#### 2025-03-05 11:30:15 UTC
* **User:** `carlos.figueroa` (assoc_100060)
* **Job ID:** `bq_job_9986701923_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 15,200,000 bytes
* **Duration:** 0.55s
* **Query Text:**
```sql
-- Leadership check on associate reporting lines under carlos.figueroa
SELECT assoc_id, full_name, role, team
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
WHERE manager_assoc_id = 'assoc_100060' OR assoc_id = 'assoc_100060';
```

#### 2025-03-08 15:10:00 UTC
* **User:** `sanjay.bhatt` (assoc_100120)
* **Job ID:** `bq_job_9987201934_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 88,400,000 bytes
* **Duration:** 1.65s
* **Query Text:**
```sql
-- Marketplace seller performance review for collectibles category
SELECT seller_id, category_focus, active_listings, trailing_90d_gmv_usd, return_rate
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
WHERE category_focus = 'collectibles'
ORDER BY trailing_90d_gmv_usd DESC
LIMIT 20;
```

#### 2025-03-10 08:45:12 UTC
* **User:** `carlos.figueroa` (assoc_100060)
* **Job ID:** `bq_job_9987510293_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 4,100,000 bytes
* **Duration:** 0.25s
* **Query Text:**
```sql
-- Verifying promote event record and role update in dim_associate
SELECT assoc_id, full_name, role, team, hire_date
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
WHERE assoc_id = 'assoc_100060';
```

#### 2025-03-12 10:05:33 UTC
* **User:** `derek.holloway` (assoc_100151)
* **Job ID:** `bq_job_9987910293_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 22,000,000 bytes
* **Duration:** 0.89s
* **Query Text:**
```sql
-- Testing membership events distribution by event_type
SELECT event_type, COUNT(*) AS event_count
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
GROUP BY 1;
```

#### 2025-03-15 13:40:22 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9988410293_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 105,000,000 bytes
* **Duration:** 2.15s
* **Query Text:**
```sql
-- Care deflection daily trends by sub_program
SELECT date, sub_program, deflection_rate, avg_csat_deflected
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
WHERE date >= '2025-02-01'
ORDER BY date DESC;
```

#### 2025-03-18 16:15:00 UTC
* **User:** `owen.faust` (assoc_100111)
* **Job ID:** `bq_job_9989010293_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 34,000,000 bytes
* **Duration:** 0.95s
* **Query Text:**
```sql
-- Checking experiment readouts for active conversion tests
SELECT experiment_id, variant, as_of_date, metric_name, metric_value, lift_vs_control_pct, is_significant
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`
WHERE metric_name LIKE '%conversion%'
ORDER BY as_of_date DESC;
```

#### 2025-03-20 09:33:11 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9989410293_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 16,500,000 bytes
* **Duration:** 0.61s
* **Query Text:**
```sql
-- Checking dim_seller panel distribution across categories and statuses
SELECT category_focus, status, fulfillment_method, COUNT(*) AS seller_count
FROM `nexus-analyst-demo.acme_ecomm.dim_seller`
GROUP BY 1, 2, 3;
```

#### 2025-03-22 11:20:45 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9989810293_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 450,100,000 bytes
* **Duration:** 4.80s
* **Query Text:**
```sql
-- WRONG QUERY ATTEMPT: testing old nested path for member CLTV
-- SELECT * FROM `nexus-analyst-demo.acme_ecomm.marts.membership.member_cltv` LIMIT 10;
-- ERROR: Not found: Table nexus-analyst-demo.acme_ecomm.marts.membership.member_cltv was not found
-- Correcting query to use flat dataset path per rule [flat-dataset]:
SELECT member_id, signup_cohort_quarter, lifetime_orders, projected_cltv_usd
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`
LIMIT 10;
```

#### 2025-03-25 14:05:19 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9990310293_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 78,000,000 bytes
* **Duration:** 1.45s
* **Query Text:**
```sql
-- INVESTIGATING SIGNAL [sample-vs-population]:
-- Running COUNT(*) on dim_member panel vs stated company member totals
SELECT 
  'dim_member_panel' AS source_table,
  COUNT(*) AS row_count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
UNION ALL
SELECT 
  'estimated_true_base' AS source_table,
  120000 AS row_count; -- NOTE: dim_member has 120,000 rows (representative panel), NOT the multi-million member base!
```

#### 2025-03-28 10:12:30 UTC
* **User:** `ines.delgado` (assoc_100121)
* **Job ID:** `bq_job_9990910293_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 92,100,000 bytes
* **Duration:** 1.75s
* **Query Text:**
```sql
-- Marketplace GMV summary by sub_vertical for style and resold
SELECT 
  fiscal_week_ending,
  sub_vertical_code,
  gmv_usd,
  orders,
  take_rate
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE sub_vertical_code IN ('STYLE', 'RESOLD')
ORDER BY fiscal_week_ending DESC;
```

#### 2025-03-31 16:50:00 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9991510293_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 620,000,000 bytes
* **Duration:** 6.10s
* **Query Text:**
```sql
-- End of March full dataset sanity check across fact_traffic_daily
SELECT 
  market,
  vertical_code,
  SUM(sessions) AS monthly_sessions,
  SUM(orders) AS monthly_orders,
  SUM(gmv_usd) AS monthly_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date BETWEEN '2025-03-01' AND '2025-03-31'
GROUP BY 1, 2;
```

#### 2025-04-02 08:30:15 UTC
* **User:** `maya.lindqvist` (assoc_100110)
* **Job ID:** `bq_job_9991910293_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 54,000,000 bytes
* **Duration:** 1.10s
* **Query Text:**
```sql
-- Checking US conversion metrics for Item Page surface review
SELECT 
  date,
  product_view_sessions,
  add_to_cart_sessions,
  orders,
  SAFE_DIVIDE(add_to_cart_sessions, product_view_sessions) AS view_to_cart_rate
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE market = 'US' AND vertical_code = 'US_CONV' AND date >= '2025-03-01'
ORDER BY date DESC;
```

#### 2025-04-05 11:15:22 UTC
* **User:** `sanjay.bhatt` (assoc_100120)
* **Job ID:** `bq_job_9992510293_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 41,200,000 bytes
* **Duration:** 0.92s
* **Query Text:**
```sql
-- Checking listing authenticity verified counts for Collectibles
SELECT authenticity_verified, COUNT(*) AS listing_count, AVG(price_usd) AS avg_price
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
WHERE category = 'collectibles'
GROUP BY 1;
```

#### 2025-04-08 09:40:00 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9993110293_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 38,900,000 bytes
* **Duration:** 0.85s
* **Query Text:**
```sql
-- Analyzing buyer VOC verbatims mentioning refund or shipping delays
SELECT response_id, score, verbatim_text, theme_tag, sentiment
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE theme_tag LIKE '%refund%' OR theme_tag LIKE '%delay%'
LIMIT 50;
```

#### 2025-04-10 14:20:10 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9993610293_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 12,100,000 bytes
* **Duration:** 0.51s
* **Query Text:**
```sql
-- Pre-MBR financial reconciliation check on Marketplace GMV summary totals for Q1
SELECT 
  sub_vertical_code,
  SUM(gmv_usd) AS q1_total_gmv,
  SUM(orders) AS q1_total_orders
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE fiscal_week_ending BETWEEN '2025-02-01' AND '2025-04-30'
GROUP BY 1;
```

#### 2025-04-12 10:00:00 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9994110293_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 310,000,000 bytes
* **Duration:** 3.10s
* **Query Text:**
```sql
-- Checking experiment exposure data completeness
SELECT experiment_id, variant, exposure_date, units_assigned, units_exposed, units_converted
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures`
ORDER BY exposure_date DESC
LIMIT 100;
```

#### 2025-04-15 09:00:00 UTC
* **User:** `carlos.figueroa` (assoc_100060)
* **Job ID:** `bq_job_9994810293_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 85,000,000 bytes
* **Duration:** 1.55s
* **Query Text:**
```sql
-- MBR Prep Query: pulling executive summary metrics across deep verticals for Q1FY26 MBR deck
SELECT 
  vertical_code,
  SUM(sessions) AS total_sessions,
  SUM(orders) AS total_orders,
  SUM(gmv_usd) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date BETWEEN '2025-02-01' AND '2025-04-15'
GROUP BY 1;
```

#### 2025-04-15 12:00:00 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9994999999_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 14,200,000 bytes
* **Duration:** 0.48s
* **Query Text:**
```sql
-- Audit log batch export packaging query for nexus-analyst-demo.acme_ecomm
SELECT 
  CURRENT_TIMESTAMP() AS export_timestamp,
  COUNT(DISTINCT table_name) AS modeled_tables_count
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.TABLES`;
```

---
*(Note: Bulk query execution log continues through Q2FY26 across all 24 modeled tables including base dimensions, fact streams, and derived marts. Routine maintenance queries, automated dbt model runs, and ad-hoc product analyses are appended in subsequent log segments.)*
