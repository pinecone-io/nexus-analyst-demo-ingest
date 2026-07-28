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


#### 2025-04-15 13:15:22 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9995012844_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 45,000,000 bytes
* **Duration:** 0.92s
* **Query Text:**
```sql
-- Validating dim_vertical list for finance reporting alignment
SELECT vertical_code, vertical_name, is_deep_dive
FROM `nexus-analyst-demo.acme_ecomm.dim_vertical`
ORDER BY vertical_code;
```

#### 2025-04-15 14:30:10 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9995188392_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 120,000,000 bytes
* **Duration:** 1.84s
* **Query Text:**
```sql
-- Routine check on fact_fulfillment_node active status across DCs
SELECT node_id, node_type, market, is_active
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE is_active = TRUE;
```

#### 2025-04-15 15:45:00 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9995299401_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 215,000,000 bytes
* **Duration:** 2.40s
* **Query Text:**
```sql
-- Testing join between dim_member and fact_membership_events for Q1 review
SELECT 
  m.plan_type,
  e.event_type,
  COUNT(DISTINCT m.member_id) AS event_count
FROM `nexus-analyst-demo.acme_ecomm.dim_member` m
JOIN `nexus-analyst-demo.acme_ecomm.fact_membership_events` e
  ON m.member_id = e.member_id
WHERE e.event_date BETWEEN '2025-02-01' AND '2025-04-15'
GROUP BY 1, 2;
```

#### 2025-04-15 16:20:55 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9995344102_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 18,000,000 bytes
* **Duration:** 0.51s
* **Query Text:**
```sql
-- Checking table partition counts for bq_query_log monitoring
SELECT table_name, row_count 
FROM `nexus-analyst-demo.acme_ecomm.__TABLES__`
ORDER BY size_bytes DESC;
```

#### 2025-04-15 17:00:00 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9995400192_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 95,000,000 bytes
* **Duration:** 1.62s
* **Query Text:**
```sql
-- Checking care contact sub_program distributions for Q1
SELECT sub_program, channel, COUNT(*) AS contacts
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at >= '2025-02-01'
GROUP BY 1, 2;
```

#### 2025-04-15 17:35:12 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9995455201_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 62,000,000 bytes
* **Duration:** 1.10s
* **Query Text:**
```sql
-- Checking dim_associate table for inactive accounts audit
SELECT assoc_id, full_name, team, is_active
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
WHERE is_active = FALSE;
```

#### 2025-04-15 18:10:40 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9995512883_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 340,000,000 bytes
* **Duration:** 3.45s
* **Query Text:**
```sql
-- Pulling marketplace listings status check by category
SELECT category, status, COUNT(*) AS listing_count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY 1, 2;
```

#### 2025-04-15 19:00:15 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9995600123_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 24,000,000 bytes
* **Duration:** 0.60s
* **Query Text:**
```sql
-- Validating dim_experiment status list
SELECT status, COUNT(*) AS exp_count
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment`
GROUP BY 1;
```

#### 2025-04-15 20:15:00 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9995711209_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 110,000,000 bytes
* **Duration:** 1.95s
* **Query Text:**
```sql
-- Checking VOC response sentiment distribution for post_purchase survey
SELECT sentiment, COUNT(*) AS responses
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE survey_type = 'post_purchase'
GROUP BY 1;
```

#### 2025-04-15 21:00:00 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9995800001_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 50,000,000 bytes
* **Duration:** 0.88s
* **Query Text:**
```sql
-- Daily audit check on dim_marketing_calendar event types
SELECT event_type, COUNT(*) AS events
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
GROUP BY 1;
```

#### 2025-04-15 21:30:10 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9995899210_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 84,000,000 bytes
* **Duration:** 1.25s
* **Query Text:**
```sql
-- Aggregating daily fulfillment speed metrics for Canadian nodes
SELECT date, market, fulfillment_type, SUM(orders_promised) AS total_promised
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
WHERE market = 'CA'
GROUP BY 1, 2, 3;
```

#### 2025-04-15 22:05:40 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9995950114_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 15,000,000 bytes
* **Duration:** 0.42s
* **Query Text:**
```sql
-- Quick count check on dim_fulfillment_node by type and active status
SELECT node_type, is_active, COUNT(*) AS node_count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
GROUP BY 1, 2;
```

#### 2025-04-15 22:45:00 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9996011982_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 190,000,000 bytes
* **Duration:** 2.10s
* **Query Text:**
```sql
-- Analyzing care contacts sub_program distribution for avoid and automate
SELECT sub_program, channel, COUNT(*) AS contact_count
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE sub_program IN ('automate', 'avoid')
GROUP BY 1, 2;
```

#### 2025-04-15 23:15:30 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9996102837_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 45,000,000 bytes
* **Duration:** 0.75s
* **Query Text:**
```sql
-- Checking experiment metadata table for running tests in US_CONV
SELECT experiment_id, experiment_name, primary_metric
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment`
WHERE vertical_code = 'US_CONV' AND status = 'running';
```

#### 2025-04-16 01:10:12 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9996204911_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 410,000,000 bytes
* **Duration:** 4.12s
* **Query Text:**
```sql
-- Quarterly traffic summary audit across all markets in fact_traffic_daily
SELECT market, device, SUM(sessions) AS total_sessions, SUM(gmv_usd) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
GROUP BY 1, 2;
```

#### 2025-04-16 02:30:00 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9996312455_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 28,000,000 bytes
* **Duration:** 0.55s
* **Query Text:**
```sql
-- Checking dim_date table bounds for Q1FY26 and Q2FY26
SELECT fiscal_quarter_label, MIN(date) AS start_date, MAX(date) AS end_date
FROM `nexus-analyst-demo.acme_ecomm.dim_date`
GROUP BY 1;
```

#### 2025-04-16 08:00:22 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9996455120_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 125,000,000 bytes
* **Duration:** 1.80s
* **Query Text:**
```sql
-- Evaluating member panel distribution by home_market
SELECT home_market, status, COUNT(*) AS member_count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
GROUP BY 1, 2;
```

#### 2025-04-16 09:20:40 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9996588301_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 68,000,000 bytes
* **Duration:** 1.05s
* **Query Text:**
```sql
-- Verifying dim_vertical taxonomy definitions and depths
SELECT vertical_code, vertical_name, is_deep_dive
FROM `nexus-analyst-demo.acme_ecomm.dim_vertical`
ORDER BY vertical_code;
```

#### 2025-04-16 10:05:11 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9996670129_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 310,000,000 bytes
* **Duration:** 3.15s
* **Query Text:**
```sql
-- Joining fact_orders with dim_fulfillment_node for regional breakdown
O.market, F.node_type, COUNT(O.order_id) AS order_count, SUM(O.gmv_usd) AS gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders` O
JOIN `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node` F
ON O.market = F.market
GROUP BY 1, 2;
```

#### 2025-04-16 11:30:50 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9996788412_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 52,000,000 bytes
* **Duration:** 0.90s
* **Query Text:**
```sql
-- Checking marketplace_gmv_summary sub_vertical groupings
SELECT sub_vertical_code, SUM(gmv_usd) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
GROUP BY 1;
```

#### 2025-04-16 13:10:05 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9996901233_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 95,000,000 bytes
* **Duration:** 1.45s
* **Query Text:**
```sql
-- Sample check on fact_voc_responses survey types and sentiment
SELECT survey_type, sentiment, COUNT(*) AS response_count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
GROUP BY 1, 2;
```

#### 2025-04-16 14:40:15 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9997011988_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 75,000,000 bytes
* **Duration:** 1.15s
* **Query Text:**
```sql
-- Auditing dim_associate active records by team
SELECT team, COUNT(*) AS active_associates
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
WHERE is_active = TRUE
GROUP BY 1;
```

#### 2025-04-16 16:00:30 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9997155099_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 220,000,000 bytes
* **Duration:** 2.40s
* **Query Text:**
```sql
-- Checking traffic_conversion_summary weekly trends for MX market
SELECT fiscal_week_ending, sessions, orders, conversion_rate
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'MX'
ORDER BY fiscal_week_ending DESC
LIMIT 10;
```

#### 2025-04-16 17:25:00 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9997288301_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 31,000,000 bytes
* **Duration:** 0.65s
* **Query Text:**
```sql
-- Validating dim_seller category_focus distribution
SELECT category_focus, status, COUNT(*) AS seller_count
FROM `nexus-analyst-demo.acme_ecomm.dim_seller`
GROUP BY 1, 2;
```

#### 2025-04-16 19:10:45 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9997401122_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 140,000,000 bytes
* **Duration:** 2.05s
* **Query Text:**
```sql
-- Examining care_deflection_daily trends across sub_programs
SELECT sub_program, AVG(deflection_rate) AS avg_deflection, AVG(avg_csat_deflected) AS avg_csat
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
GROUP BY 1;
```

#### 2025-04-16 20:30:10 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9997522901_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 48,000,000 bytes
* **Duration:** 0.82s
* **Query Text:**
```sql
-- Checking dim_marketing_calendar event types and owner breakdown
SELECT event_type, owner_assoc_id, COUNT(*) AS event_count
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
GROUP BY 1, 2;
```

#### 2025-04-17 01:15:00 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9997701234_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 450,000,000 bytes
* **Duration:** 4.50s
* **Query Text:**
```sql
-- Pulling marketplace_seller_performance metrics for top active listings
SELECT seller_id, category_focus, active_listings, trailing_90d_gmv_usd
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
ORDER BY trailing_90d_gmv_usd DESC
LIMIT 25;
```

#### 2025-04-17 03:45:20 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9997899120_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 18,000,000 bytes
* **Duration:** 0.50s
* **Query Text:**
```sql
-- Simple count query on fact_experiment_exposures grouped by experiment_id
SELECT experiment_id, SUM(units_assigned) AS assigned, SUM(units_exposed) AS exposed
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures`
GROUP BY 1;
```

#### 2025-04-17 08:30:00 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9998012455_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 115,000,000 bytes
* **Duration:** 1.70s
* **Query Text:**
```sql
-- Querying fact_membership_events for benefit redemption patterns
SELECT benefit_code, channel, COUNT(*) AS redemptions
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
WHERE event_type = 'benefit_redeemed'
GROUP BY 1, 2;
```

#### 2025-04-17 10:15:30 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9998155011_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 60,000,000 bytes
* **Duration:** 0.95s
* **Query Text:**
```sql
-- Checking fulfillment_speed_daily metrics for ship_to_home fulfillment type
SELECT market, AVG(on_time_rate) AS avg_on_time, AVG(avg_cost_per_order_usd) AS avg_cost
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE fulfillment_type = 'ship_to_home'
GROUP BY 1;
```

#### 2025-04-17 12:00:45 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9998301129_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 290,000,000 bytes
* **Duration:** 2.95s
* **Query Text:**
```sql
-- Checking fact_orders return rates by market and channel
SELECT market, channel, COUNT(*) AS total_orders, SUM(CAST(is_returned AS INT64)) AS returned_orders
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
GROUP BY 1, 2;
```

#### 2025-04-17 14:10:10 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9998455882_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 35,000,000 bytes
* **Duration:** 0.70s
* **Query Text:**
```sql
-- Validating fact_marketplace_listings status distribution by category
SELECT category, authenticity_verified, COUNT(*) AS listing_count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY 1, 2;
```

#### 2025-04-17 16:40:00 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9998601200_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 88,000,000 bytes
* **Duration:** 1.30s
* **Query Text:**
```sql
-- Checking fact_seller_voc_responses sentiment breakdown for onboarding pulse
SELECT survey_type, sentiment, COUNT(*) AS responses
FROM `nexus-analyst-demo.acme_ecomm.fact_seller_voc_responses`
GROUP BY 1, 2;
```

#### 2025-04-17 18:20:15 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9998755012_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 55,000,000 bytes
* **Duration:** 0.85s
* **Query Text:**
```sql
-- Audit query for dim_experiment owner distribution
SELECT owner_assoc_id, status, COUNT(*) AS exp_count
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment`
GROUP BY 1, 2;
```

#### 2025-04-17 20:00:00 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9998901233_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 340,000,000 bytes
* **Duration:** 3.30s
* **Query Text:**
```sql
-- Analyzing member_cltv distribution across tenure buckets
SELECT FLOOR(tenure_days / 365) AS tenure_years, COUNT(*) AS member_count, AVG(projected_cltv_usd) AS avg_cltv
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`
GROUP BY 1
ORDER BY 1;
```

#### 2025-04-18 01:10:30 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999055120_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 22,000,000 bytes
* **Duration:** 0.58s
* **Query Text:**
```sql
-- Checking fact_experiment_readouts metric names list
SELECT metric_name, COUNT(*) AS readout_count, AVG(metric_value) AS avg_value
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`
GROUP BY 1;
```

#### 2025-04-18 08:45:00 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999201199_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 105,000,000 bytes
* **Duration:** 1.60s
* **Query Text:**
```sql
-- Evaluating fact_care_contacts resolution codes breakdown
SELECT resolution_code, channel, COUNT(*) AS cases
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1, 2;
```

#### 2025-04-18 10:30:15 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999355088_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 40,000,000 bytes
* **Duration:** 0.70s
* **Query Text:**
```sql
-- Checking dim_fulfillment_node market coverage
SELECT market, COUNT(*) AS total_nodes
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
GROUP BY 1;
```

#### 2025-04-18 12:15:40 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999501234_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 380,000,000 bytes
* **Duration:** 3.75s
* **Query Text:**
```sql
-- Summing GMV and orders from traffic_conversion_summary for US market by month
SELECT DATE_TRUNC(fiscal_week_ending, MONTH) AS fiscal_month, SUM(gmv_usd) AS monthly_gmv, SUM(orders) AS monthly_orders
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'US'
GROUP BY 1
ORDER BY 1;
```

#### 2025-04-18 14:00:00 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999655100_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 29,000,000 bytes
* **Duration:** 0.62s
* **Query Text:**
```sql
-- Validating dim_seller panel home_country distribution
SELECT home_country, status, COUNT(*) AS sellers
FROM `nexus-analyst-demo.acme_ecomm.dim_seller`
GROUP BY 1, 2;
```

#### 2025-04-18 16:30:20 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999801211_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 130,000,000 bytes
* **Duration:** 1.90s
* **Query Text:**
```sql
-- Checking fact_voc_responses theme tags frequency for post_purchase survey
SELECT theme_tag, COUNT(*) AS occurrences
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE survey_type = 'post_purchase' AND theme_tag IS NOT NULL
GROUP BY 1
ORDER BY 2 DESC
LIMIT 15;
```

#### 2025-04-18 19:10:00 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999955012_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 62,000,000 bytes
* **Duration:** 1.02s
* **Query Text:**
```sql
-- Checking dim_associate records with missing manager associations
SELECT team, COUNT(*) AS associates_without_manager
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
WHERE manager_assoc_id IS NULL
GROUP BY 1;
```

```sql
-- Checking fact_orders count and GMV sum for CA market in Q1FY26
SELECT COUNT(*) AS order_count, SUM(gmv_usd) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE market = 'CA' AND order_date BETWEEN '2025-02-01' AND '2025-04-15';
```

#### 2025-04-18 20:45:10 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990111_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 15,000,000 bytes
* **Duration:** 0.44s
* **Query Text:**
```sql
-- Quick check on dim_experiment status distribution
SELECT status, COUNT(*) AS experiment_count
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment`
GROUP BY 1;
```

#### 2025-04-19 09:30:15 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990112_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 95,000,000 bytes
* **Duration:** 1.20s
* **Query Text:**
```sql
-- Pulling marketplace_gmv_summary for the latest completed fiscal weeks
SELECT fiscal_week_ending, sub_vertical_code, SUM(gmv_usd) AS weekly_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
GROUP BY 1, 2
ORDER BY 1 DESC, 2;
```

#### 2025-04-19 11:05:40 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990113_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 22,000,000 bytes
* **Duration:** 0.51s
* **Query Text:**
```sql
-- Verifying partition counts on fact_traffic_daily for April 2025
SELECT market, COUNT(DISTINCT date) AS active_days
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE date >= '2025-04-01'
GROUP BY 1;
```

#### 2025-04-19 14:20:00 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990114_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 110,000,000 bytes
* **Duration:** 1.45s
* **Query Text:**
```sql
-- Reviewing fact_care_contacts volume by sub_program for Q1FY26
SELECT sub_program, channel, COUNT(*) AS contact_vol
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE opened_at BETWEEN '2025-02-01 00:00:00' AND '2025-04-15 23:59:59'
GROUP BY 1, 2;
```

#### 2025-04-19 16:50:30 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990115_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 45,000,000 bytes
* **Duration:** 0.78s
* **Query Text:**
```sql
-- Checking dim_marketing_calendar event counts by event_type
SELECT event_type, COUNT(*) AS event_count
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
GROUP BY 1;
```

#### 2025-04-20 08:15:00 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990116_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 410,000,000 bytes
* **Duration:** 4.10s
* **Query Text:**
```sql
-- Note: checking member_cltv table using flat dataset path
-- table not found if using acme_ecomm.marts.membership.member_cltv -- flat dataset required
SELECT plan_type, COUNT(*) AS member_count, AVG(lifetime_gmv_usd) AS avg_gmv
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`
JOIN `nexus-analyst-demo.acme_ecomm.dim_member` USING (member_id)
GROUP BY 1;
```

#### 2025-04-20 10:40:12 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990117_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 18,000,000 bytes
* **Duration:** 0.35s
* **Query Text:**
```sql
-- Checking dim_date metadata for peak holiday flag distribution
SELECT is_peak_holiday, COUNT(*) AS days_count
FROM `nexus-analyst-demo.acme_ecomm.dim_date`
GROUP BY 1;
```

#### 2025-04-20 13:10:45 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990118_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 85,000,000 bytes
* **Duration:** 1.10s
* **Query Text:**
```sql
-- Pulling average csat score from fact_care_contacts where csat_score is not null
SELECT sub_program, AVG(csat_score) AS avg_csat
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
WHERE csat_score IS NOT NULL
GROUP BY 1;
```

#### 2025-04-20 15:25:00 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990119_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 33,000,000 bytes
* **Duration:** 0.65s
* **Query Text:**
```sql
-- Validating fulfillment_speed_daily rows for US market in March 2025
SELECT fulfillment_type, SUM(orders_promised) AS total_promised, AVG(on_time_rate) AS avg_on_time
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE market = 'US' AND date BETWEEN '2025-03-01' AND '2025-03-31'
GROUP BY 1;
```

#### 2025-04-21 09:00:20 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990120_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 150,000,000 bytes
* **Duration:** 1.85s
* **Query Text:**
```sql
-- Panel check: SELECT COUNT(*) FROM dim_member returns 120,000 (this is the panel, not the true multi-million-member base)
SELECT COUNT(*) AS panel_member_count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`;
```

#### 2025-04-21 11:30:50 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990121_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 25,000,000 bytes
* **Duration:** 0.50s
* **Query Text:**
```sql
-- Checking dim_fulfillment_node active status by node_type
SELECT node_type, is_active, COUNT(*) AS node_count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
GROUP BY 1, 2;
```

#### 2025-04-21 14:15:10 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990122_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 65,000,000 bytes
* **Duration:** 0.95s
* **Query Text:**
```sql
-- Checking fact_voc_responses sentiment distribution across survey types
SELECT survey_type, sentiment, COUNT(*) AS response_count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
GROUP BY 1, 2;
```

#### 2025-04-21 16:40:00 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990123_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 50,000,000 bytes
* **Duration:** 0.82s
* **Query Text:**
```sql
-- Validating traffic_conversion_summary sessions definition versions
SELECT sessions_definition_version, COUNT(*) AS row_count, SUM(sessions) AS total_sessions
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
GROUP BY 1;
```

#### 2025-04-22 08:30:15 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990124_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 210,000,000 bytes
* **Duration:** 2.30s
* **Query Text:**
```sql
-- Checking fact_membership_events event_type frequency
SELECT event_type, COUNT(*) AS event_count
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
GROUP BY 1;
```

#### 2025-04-22 10:12:40 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990125_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 12,000,000 bytes
* **Duration:** 0.31s
* **Query Text:**
```sql
-- Checking dim_vertical taxonomy rows
SELECT vertical_code, is_deep_dive, COUNT(*) AS sub_verticals
FROM `nexus-analyst-demo.acme_ecomm.dim_vertical`
GROUP BY 1, 2;
```

#### 2025-04-22 13:00:20 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990126_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 75,000,000 bytes
* **Duration:** 1.05s
* **Query Text:**
```sql
-- Checking care_deflection_daily trend by sub_program
SELECT sub_program, AVG(deflection_rate) AS avg_deflection
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
GROUP BY 1;
```

#### 2025-04-22 15:45:00 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990127_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 88,000,000 bytes
* **Duration:** 1.25s
* **Query Text:**
```sql
-- Checking marketplace_seller_performance active listings and gmv by category
SELECT category_focus, SUM(active_listings) AS total_listings, SUM(trailing_90d_gmv_usd) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
GROUP BY 1;
```

#### 2025-04-23 09:15:30 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990128_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 300,000,000 bytes
* **Duration:** 3.10s
* **Query Text:**
```sql
-- Joining dim_member with member_cltv to inspect benefit adoption count
SELECT m.plan_type, c.benefits_adopted_count, COUNT(*) AS members
FROM `nexus-analyst-demo.acme_ecomm.dim_member` m
LEFT JOIN `nexus-analyst-demo.acme_ecomm.member_cltv` c USING (member_id)
GROUP BY 1, 2
ORDER BY 1, 2;
```

#### 2025-04-23 11:50:10 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990129_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 31,000,000 bytes
* **Duration:** 0.68s
* **Query Text:**
```sql
-- Checking dim_experiment status and vertical breakdown
SELECT vertical_code, status, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment`
GROUP BY 1, 2;
```

#### 2025-04-23 14:20:45 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990130_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 55,000,000 bytes
* **Duration:** 0.88s
* **Query Text:**
```sql
-- Reviewing fact_voc_responses score distribution for nps survey type
SELECT score, COUNT(*) AS freq
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE survey_type = 'nps'
GROUP BY 1
ORDER BY 1;
```

#### 2025-04-23 17:05:00 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990131_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 19,000,000 bytes
* **Duration:** 0.42s
* **Query Text:**
```sql
-- Validating dim_seller category_focus distribution across panel
SELECT category_focus, COUNT(*) AS sellers_count
FROM `nexus-analyst-demo.acme_ecomm.dim_seller`
GROUP BY 1;
```

#### 2025-04-24 08:40:12 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990132_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 175,000,000 bytes
* **Duration:** 1.95s
* **Query Text:**
```sql
-- Inspecting fact_orders distribution by fulfillment_type and channel
SELECT fulfillment_type, channel, COUNT(*) AS orders, SUM(gmv_usd) AS gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
GROUP BY 1, 2;
```

#### 2025-04-24 11:10:30 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990133_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 40,000,000 bytes
* **Duration:** 0.75s
* **Query Text:**
```sql
-- Checking dim_associate active status and team distribution
SELECT team, is_active, COUNT(*) AS associate_count
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
GROUP BY 1, 2;
```

#### 2025-04-24 13:55:00 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990134_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 90,000,000 bytes
* **Duration:** 1.22s
* **Query Text:**
```sql
-- Checking fact_care_contacts resolution codes breakdown
SELECT resolution_code, COUNT(*) AS occurrences
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1
ORDER BY 2 DESC;
```

#### 2025-04-24 16:20:15 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990135_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 62,000,000 bytes
* **Duration:** 0.99s
* **Query Text:**
```sql
-- Validating fact_promise_vs_actual aggregated metrics by market
SELECT market, SUM(orders_promised) AS promised, SUM(orders_on_time) AS on_time
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
GROUP BY 1;
```

#### 2025-04-25 09:10:00 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990136_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 125,000,000 bytes
* **Duration:** 1.50s
* **Query Text:**
```sql
-- Checking fact_marketplace_listings status breakdown by category
SELECT category, status, COUNT(*) AS listing_count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY 1, 2;
```

#### 2025-04-25 11:35:40 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990137_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 14,000,000 bytes
* **Duration:** 0.33s
* **Query Text:**
```sql
-- Checking dim_marketing_calendar owners list
SELECT owner_assoc_id, COUNT(*) AS planned_events
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
GROUP BY 1;
```

#### 2025-04-25 14:05:20 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990138_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 48,000,000 bytes
* **Duration:** 0.81s
* **Query Text:**
```sql
-- Checking fact_voc_responses theme tags in post_care_contact survey type
SELECT theme_tag, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE survey_type = 'post_care_contact'
GROUP BY 1
ORDER BY 2 DESC;
```

#### 2025-04-25 16:50:00 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990139_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 35,000,000 bytes
* **Duration:** 0.69s
* **Query Text:**
```sql
-- Validating traffic_conversion_summary weekly trend for MX market
SELECT fiscal_week_ending, sessions, conversion_rate, gmv_usd
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'MX'
ORDER BY fiscal_week_ending DESC
LIMIT 10;
```

#### 2025-04-25 18:20:10 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990140_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 18,500,000 bytes
* **Duration:** 0.41s
* **Query Text:**
```sql
-- Checking partition sizes for fact_orders table
SELECT table_name, partition_id, total_rows
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'fact_orders';
```

#### 2025-04-25 21:10:00 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990141_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 112,000,000 bytes
* **Duration:** 1.34s
* **Query Text:**
```sql
-- Validating dim_member panel size -- NOTE: 120000 rows is the sample panel, not the true base
SELECT COUNT(*) AS panel_count, COUNT(DISTINCT home_market) AS markets
FROM `nexus-analyst-demo.acme_ecomm.dim_member`;
```

#### 2025-04-26 08:15:30 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990142_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 85,000,000 bytes
* **Duration:** 0.95s
* **Query Text:**
```sql
-- Checking marketplace_gmv_summary splits for Q1FY26
SELECT fiscal_week_ending, sub_vertical_code, gmv_usd
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
WHERE fiscal_week_ending >= '2025-02-01'
ORDER BY fiscal_week_ending DESC;
```

#### 2025-04-26 10:40:15 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990143_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 22,000,000 bytes
* **Duration:** 0.48s
* **Query Text:**
```sql
-- Checking care_deflection_daily for automated sub_program
SELECT date, contact_volume, deflection_rate
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
WHERE sub_program = 'automate'
ORDER BY date DESC
LIMIT 7;
```

#### 2025-04-26 13:22:00 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990144_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 64,000,000 bytes
* **Duration:** 0.89s
* **Query Text:**
```sql
-- Attempting cltv join via marts path -- table not found, flat dataset
SELECT m.member_id, c.lifetime_gmv_usd
FROM `nexus-analyst-demo.acme_ecomm.dim_member` m
JOIN `nexus-analyst-demo.acme_ecomm.member_cltv` c ON m.member_id = c.member_id
LIMIT 5;
```

#### 2025-04-26 15:05:40 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990145_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 12,000,000 bytes
* **Duration:** 0.28s
* **Query Text:**
```sql
-- Listing datasets in nexus-analyst-demo
SELECT table_name, table_type
FROM `nexus-analyst-demo.acme_ecomm.INFORMATION_SCHEMA.TABLES`
ORDER BY table_name;
```

#### 2025-04-27 09:12:00 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990146_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 150,000,000 bytes
* **Duration:** 1.82s
* **Query Text:**
```sql
-- Full population traffic check across devices for US market
SELECT device, SUM(sessions) AS total_sessions, SUM(orders) AS total_orders
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE market = 'US' AND date >= '2025-02-01'
GROUP BY 1;
```

#### 2025-04-27 11:30:15 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990147_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 39,000,000 bytes
* **Duration:** 0.62s
* **Query Text:**
```sql
-- Checking fact_voc_responses score distribution for post_purchase
SELECT score, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE survey_type = 'post_purchase'
GROUP BY 1
ORDER BY 1;
```

#### 2025-04-27 14:00:20 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990148_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 95,000,000 bytes
* **Duration:** 1.15s
* **Query Text:**
```sql
-- Validating traffic_conversion_summary US conversion rate for Q1FY26
SELECT fiscal_week_ending, sessions, orders, conversion_rate
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'US' AND fiscal_week_ending BETWEEN '2025-02-01' AND '2025-04-30'
ORDER BY fiscal_week_ending;
```

#### 2025-04-27 16:45:10 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990149_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 8,000,000 bytes
* **Duration:** 0.19s
* **Query Text:**
```sql
-- Checking dim_fulfillment_node active count by type
SELECT node_type, COUNT(*) AS active_nodes
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE is_active = TRUE
GROUP BY 1;
```

#### 2025-04-28 08:30:00 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990150_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 72,000,000 bytes
* **Duration:** 0.91s
* **Query Text:**
```sql
-- Checking dim_seller panel row count across categories
SELECT category_focus, status, COUNT(*) AS seller_count
FROM `nexus-analyst-demo.acme_ecomm.dim_seller`
GROUP BY 1, 2;
```

#### 2025-04-28 10:15:45 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990151_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 45,000,000 bytes
* **Duration:** 0.73s
* **Query Text:**
```sql
-- Checking fact_care_contacts channel breakdown
SELECT channel, COUNT(*) AS contact_count, AVG(csat_score) AS avg_csat
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1;
```

#### 2025-04-28 13:50:00 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990152_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 110,000,000 bytes
* **Duration:** 1.40s
* **Query Text:**
```sql
-- Checking member_cltv sample coverage with LEFT JOIN to dim_member
SELECT m.home_market, COUNT(c.member_id) AS matched_members, AVG(c.lifetime_gmv_usd) AS avg_gmv
FROM `nexus-analyst-demo.acme_ecomm.dim_member` m
LEFT JOIN `nexus-analyst-demo.acme_ecomm.member_cltv` c ON m.member_id = c.member_id
GROUP BY 1;
```

#### 2025-04-28 15:20:30 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990153_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 15,000,000 bytes
* **Duration:** 0.35s
* **Query Text:**
```sql
-- Verifying dim_vertical rows and depth flags
SELECT vertical_code, vertical_name, is_deep_dive
FROM `nexus-analyst-demo.acme_ecomm.dim_vertical`
ORDER BY vertical_code;
```

#### 2025-04-29 09:05:00 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990154_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 88,000,000 bytes
* **Duration:** 1.02s
* **Query Text:**
```sql
-- Checking fulfillment_speed_daily aggregate metrics by fulfillment_type
SELECT fulfillment_type, SUM(orders_promised) AS promised, AVG(on_time_rate) AS avg_on_time
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
GROUP BY 1;
```

#### 2025-04-29 11:12:30 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990155_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 51,000,000 bytes
* **Duration:** 0.82s
* **Query Text:**
```sql
-- Checking fact_membership_events breakdown by event_type
SELECT event_type, COUNT(*) AS event_count
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
GROUP BY 1;
```

#### 2025-04-29 14:30:15 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990156_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 105,000,000 bytes
* **Duration:** 1.28s
* **Query Text:**
```sql
-- Checking marketplace_seller_performance summary by category_focus
SELECT category_focus, COUNT(seller_id) AS seller_count, SUM(trailing_90d_gmv_usd) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
GROUP BY 1;
```

#### 2025-04-29 16:10:00 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990157_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 19,000,000 bytes
* **Duration:** 0.44s
* **Query Text:**
```sql
-- Checking dim_experiment status counts
SELECT status, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment`
GROUP BY 1;
```

#### 2025-04-30 08:20:00 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990158_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 130,000,000 bytes
* **Duration:** 1.60s
* **Query Text:**
```sql
-- Checking fact_orders sample grain and return rate overview
SELECT channel, fulfillment_type, COUNT(*) AS order_count, SUM(gmv_usd) AS sample_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
GROUP BY 1, 2;
```

#### 2025-04-30 10:45:20 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990159_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 34,000,000 bytes
* **Duration:** 0.55s
* **Query Text:**
```sql
-- Checking fact_voc_responses theme tags across all survey types
SELECT survey_type, theme_tag, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE theme_tag IS NOT NULL
GROUP BY 1, 2
ORDER BY 3 DESC
LIMIT 15;
```

#### 2025-04-30 13:15:00 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990160_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 78,000,000 bytes
* **Duration:** 0.94s
* **Query Text:**
```sql
-- Validating dim_member panel size again -- 120k sample panel check
SELECT status, COUNT(*) AS member_count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
GROUP BY 1;
```

#### 2025-04-30 15:40:10 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990161_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 11,000,000 bytes
* **Duration:** 0.25s
* **Query Text:**
```sql
-- Checking dim_date calendar range for Q1FY26 end
SELECT fiscal_quarter_label, MIN(date) AS min_date, MAX(date) AS max_date
FROM `nexus-analyst-demo.acme_ecomm.dim_date`
WHERE fiscal_year = 2026 AND fiscal_quarter = 1
GROUP BY 1;
```

#### 2025-04-30 17:05:30 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990162_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 45,000,000 bytes
* **Duration:** 0.62s
* **Query Text:**
```sql
-- Checking fact_traffic_daily session distribution by device for MX market
SELECT device, SUM(sessions) AS total_sessions, SUM(gmv_usd) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE market = 'MX' AND date >= '2025-02-01'
GROUP BY 1;
```

#### 2025-04-30 18:22:15 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990163_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 15,000,000 bytes
* **Duration:** 0.31s
* **Query Text:**
```sql
-- Verifying dim_vertical rows and deep-dive flags
SELECT vertical_code, name, is_deep_dive
FROM `nexus-analyst-demo.acme_ecomm.dim_vertical`
ORDER BY is_deep_dive DESC, vertical_code;
```

#### 2025-04-30 19:50:00 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990164_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 62,000,000 bytes
* **Duration:** 0.88s
* **Query Text:**
```sql
-- Checking fact_care_contacts distribution across sub_programs
SELECT sub_program, channel, COUNT(*) AS contact_count, AVG(csat_score) AS avg_csat
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1, 2;
```

#### 2025-05-01 08:12:40 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990165_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 8,000,000 bytes
* **Duration:** 0.19s
* **Query Text:**
```sql
-- Partition check for fact_promise_vs_actual May 2025 staging
SELECT market, fulfillment_type, COUNT(*) AS row_count
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
GROUP BY 1, 2;
```

#### 2025-05-01 09:30:11 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990166_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 112,000,000 bytes
* **Duration:** 1.41s
* **Query Text:**
```sql
-- Daily US conversion trend verification for late April
SELECT date, sessions, orders, conversion_rate, gmv_usd
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'US' AND fiscal_week_ending >= '2025-04-01'
ORDER BY date DESC
LIMIT 10;
```

#### 2025-05-01 11:05:00 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990167_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 190,000,000 bytes
* **Duration:** 2.10s
* **Query Text:**
```sql
-- Attempting member CLTV rollup with inner join against dim_member panel
SELECT m.status, COUNT(c.member_id) AS matched_members, SUM(c.lifetime_gmv_usd) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.dim_member` m
JOIN `nexus-analyst-demo.acme_ecomm.member_cltv` c ON m.member_id = c.member_id
GROUP BY 1;
```

#### 2025-05-01 13:40:55 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990168_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 54,000,000 bytes
* **Duration:** 0.72s
* **Query Text:**
```sql
-- Checking fact_voc_responses score distribution for post_purchase surveys
SELECT score, COUNT(*) AS frequency
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE survey_type = 'post_purchase'
GROUP BY 1
ORDER BY 1;
```

#### 2025-05-01 15:20:00 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990169_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 22,000,000 bytes
* **Duration:** 0.38s
* **Query Text:**
```sql
-- Checking dim_fulfillment_node active counts by node type
SELECT node_type, market, COUNT(*) AS node_count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE is_active = TRUE
GROUP BY 1, 2;
```

#### 2025-05-02 08:45:10 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990170_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 88,000,000 bytes
* **Duration:** 1.05s
* **Query Text:**
```sql
-- Validating marketplace_gmv_summary sub_vertical aggregations
SELECT sub_vertical_code, SUM(gmv_usd) AS total_gmv, SUM(orders) AS total_orders
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
GROUP BY 1;
```

#### 2025-05-02 10:15:30 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990171_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 14,000,000 bytes
* **Duration:** 0.28s
* **Query Text:**
```sql
-- Checking dim_associate team distribution in Data & Analytics
team, role, COUNT(*) AS assoc_count
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
WHERE team = 'Data'
GROUP BY 1, 2;
```

#### 2025-05-02 11:55:00 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990172_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 36,000,000 bytes
* **Duration:** 0.51s
* **Query Text:**
```sql
-- Reviewing care_deflection_daily trends for platform sub_program
SELECT date, contact_volume, deflection_rate, avg_csat_deflected
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
WHERE sub_program = 'platform'
ORDER BY date DESC
LIMIT 10;
```

#### 2025-05-02 14:10:20 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990173_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 25,000,000 bytes
* **Duration:** 0.40s
* **Query Text:**
```sql
-- Checking dim_marketing_calendar event types and planned spend
event_type, COUNT(*) AS event_count, SUM(planned_spend_usd) AS total_planned_spend
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
GROUP BY 1;
```

#### 2025-05-03 09:00:00 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990174_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 105,000,000 bytes
* **Duration:** 1.25s
* **Query Text:**
```sql
-- Checking fact_experiment_exposures totals across active experiments
SELECT experiment_id, variant, SUM(units_assigned) AS assigned, SUM(units_exposed) AS exposed
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures`
GROUP BY 1, 2;
```

#### 2025-05-03 10:30:15 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990175_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 31,000,000 bytes
* **Duration:** 0.49s
* **Query Text:**
```sql
-- Checking fact_membership_events event type distribution
event_type, channel, COUNT(*) AS event_count
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
GROUP BY 1, 2;
```

#### 2025-05-03 13:15:40 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990176_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 72,000,000 bytes
* **Duration:** 0.95s
* **Query Text:**
```sql
-- Checking marketplace_seller_performance metrics by category focus
category_focus, COUNT(seller_id) AS seller_count, AVG(return_rate) AS avg_return_rate
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
GROUP BY 1;
```

#### 2025-05-04 08:20:00 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990177_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 19,000,000 bytes
* **Duration:** 0.33s
* **Query Text:**
```sql
-- Checking dim_seller status breakdown for shared cast validation
status, fulfillment_method, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.dim_seller`
GROUP BY 1, 2;
```

#### 2025-05-04 10:05:22 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990178_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 95,000,000 bytes
* **Duration:** 1.12s
* **Query Text:**
```sql
-- Checking fulfillment_speed_daily on-time rates by fulfillment type
fulfillment_type, AVG(on_time_rate) AS mean_on_time_rate, SUM(orders_promised) AS total_promised
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
GROUP BY 1;
```

#### 2025-05-04 12:45:00 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990179_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 42,000,000 bytes
* **Duration:** 0.58s
* **Query Text:**
```sql
-- Checking fact_orders sample grain for channel and return flags
channel, is_returned, COUNT(*) AS order_count, SUM(gmv_usd) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
GROUP BY 1, 2;
```

#### 2025-05-04 15:10:30 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990180_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 58,000,000 bytes
* **Duration:** 0.79s
* **Query Text:**
```sql
-- Checking fact_marketplace_listings status and authenticity verification
status, authenticity_verified, COUNT(*) AS listing_count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY 1, 2;
```

#### 2025-05-04 17:22:15 UTC
* **User:** `carlos.figueroa` (assoc_100060)
* **Job ID:** `bq_job_9999990181_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 12,000,000 bytes
* **Duration:** 0.22s
* **Query Text:**
```sql
-- Checking dim_associate active headcount count by location
location, COUNT(*) AS headcount
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
WHERE is_active = TRUE
GROUP BY 1;
```

#### 2025-05-04 18:40:00 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990182_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 310,000,000 bytes
* **Duration:** 2.45s
* **Query Text:**
```sql
-- Checking fact_orders total GMV and order counts for Q1FY26 by market
market, COUNT(order_id) AS total_orders, SUM(gmv_usd) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE order_date BETWEEN '2025-02-01' AND '2025-04-30'
GROUP BY 1;
```

#### 2025-05-05 09:12:05 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990183_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 45,000,000 bytes
* **Duration:** 0.51s
* **Query Text:**
```sql
-- Checking dim_date calendar range and peak holiday boolean distribution
is_peak_holiday, COUNT(*) AS day_count
FROM `nexus-analyst-demo.acme_ecomm.dim_date`
GROUP BY 1;
```

#### 2025-05-05 11:30:18 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990184_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 15,000,000 bytes
* **Duration:** 0.29s
* **Query Text:**
```sql
-- Checking dim_fulfillment_node counts by node_type and market
node_type, market, COUNT(*) AS node_count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
GROUP BY 1, 2;
```

#### 2025-05-05 14:05:40 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990185_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 88,000,000 bytes
* **Duration:** 1.05s
* **Query Text:**
```sql
-- Checking fact_care_contacts volume by sub_program and channel
sub_program, channel, COUNT(*) AS contact_count
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1, 2;
```

#### 2025-05-05 16:20:11 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990186_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 22,000,000 bytes
* **Duration:** 0.41s
* **Query Text:**
```sql
-- Checking dim_vertical taxonomy depth flags
vertical_code, vertical_name, is_deep_dive
FROM `nexus-analyst-demo.acme_ecomm.dim_vertical`
WHERE is_deep_dive = TRUE;
```

#### 2025-05-06 08:35:00 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990187_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 64,000,000 bytes
* **Duration:** 0.82s
* **Query Text:**
```sql
-- Checking dim_member sample size verification (testing sample vs population expectation)
SELECT COUNT(*) AS total_panel_members FROM `nexus-analyst-demo.acme_ecomm.dim_member`;
-- Note: confirms 120,000 representative panel rows, not the true multi-million active base.
```

#### 2025-05-06 10:15:44 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990188_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 110,000,000 bytes
* **Duration:** 1.34s
* **Query Text:**
```sql
-- Checking fact_experiment_exposures summary across all active experiments
experiment_id, variant, SUM(units_assigned) AS assigned, SUM(units_exposed) AS exposed
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures`
GROUP BY 1, 2;
```

#### 2025-05-06 13:40:22 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990189_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 72,000,000 bytes
* **Duration:** 0.91s
* **Query Text:**
```sql
-- Checking fact_voc_responses score distribution by survey_type
survey_type, score_type, COUNT(*) AS response_count, AVG(score) AS avg_score
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
GROUP BY 1, 2;
```

#### 2025-05-06 15:55:10 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990190_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 145,000,000 bytes
* **Duration:** 1.62s
* **Query Text:**
```sql
-- Checking traffic_conversion_summary US conversion by fiscal week
fiscal_week_ending, sessions, orders, conversion_rate, gmv_usd
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'US' AND vertical_code = 'US_CONV'
ORDER BY fiscal_week_ending DESC
LIMIT 10;
```

#### 2025-05-07 09:02:15 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990191_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 18,000,000 bytes
* **Duration:** 0.31s
* **Query Text:**
```sql
-- Checking dim_marketing_calendar event types and owner distribution
event_type, COUNT(*) AS event_count
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
GROUP BY 1;
```

#### 2025-05-07 11:20:33 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990192_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 35,000,000 bytes
* **Duration:** 0.52s
* **Query Text:**
```sql
-- Checking dim_experiment status breakdown
status, COUNT(*) AS experiment_count
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment`
GROUP BY 1;
```

#### 2025-05-07 14:15:00 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990193_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 512,000,000 bytes
* **Duration:** 4.12s
* **Query Text:**
```sql
-- Checking fact_membership_events lifecycle event distribution
event_type, channel, COUNT(*) AS event_count
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
GROUP BY 1, 2;
```

#### 2025-05-07 16:45:50 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990194_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 28,000,000 bytes
* **Duration:** 0.44s
* **Query Text:**
```sql
-- Checking care_deflection_daily metrics trend across sub_programs
sub_program, AVG(deflection_rate) AS avg_deflection_rate, AVG(avg_csat_deflected) AS mean_csat_deflected
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
GROUP BY 1;
```

#### 2025-05-08 08:12:30 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990195_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 82,000,000 bytes
* **Duration:** 0.99s
* **Query Text:**
```sql
-- Checking marketplace_gmv_summary splits across sub_vertical_codes
sub_vertical_code, SUM(gmv_usd) AS total_gmv, SUM(orders) AS total_orders
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
GROUP BY 1;
```

#### 2025-05-08 10:30:15 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990196_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 19,500,000 bytes
* **Duration:** 0.35s
* **Query Text:**
```sql
-- Checking marketplace_seller_performance category focus counts
category_focus, COUNT(seller_id) AS seller_count, AVG(return_rate) AS avg_return_rate
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
GROUP BY 1;
```

#### 2025-05-08 12:55:00 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990197_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 125,000,000 bytes
* **Duration:** 1.48s
* **Query Text:**
```sql
-- Checking member_cltv distribution by plan_type using joined dim_member attributes
m.plan_type, COUNT(c.member_id) AS member_count, AVG(c.projected_cltv_usd) AS avg_projected_cltv
FROM `nexus-analyst-demo.acme_ecomm.member_cltv` c
LEFT JOIN `nexus-analyst-demo.acme_ecomm.dim_member` m ON c.member_id = m.member_id
GROUP BY 1;
```

#### 2025-05-08 15:10:40 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990198_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 41,000,000 bytes
* **Duration:** 0.61s
* **Query Text:**
```sql
-- Checking fact_promise_vs_actual performance by fulfillment type
fulfillment_type, SUM(orders_promised) AS total_promised, SUM(orders_on_time) AS total_on_time
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
GROUP BY 1;
```

#### 2025-05-09 09:20:11 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990199_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 65,000,000 bytes
* **Duration:** 0.85s
* **Query Text:**
```sql
-- Checking fact_traffic_daily device breakdown for US market sessions
device, SUM(sessions) AS total_sessions, SUM(gmv_usd) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE market = 'US'
GROUP BY 1;
```

#### 2025-05-09 11:45:20 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990200_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 14,000,000 bytes
* **Duration:** 0.28s
* **Query Text:**
```sql
-- Test query for associate reporting lines in dim_associate
role, COUNT(*) AS role_count
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
GROUP BY 1;
```

#### 2025-05-09 14:10:00 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990201_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 210,000,000 bytes
* **Duration:** 2.15s
* **Query Text:**
```sql
-- Checking fact_orders fulfillment type and channel cross-tabulation
channel, fulfillment_type, COUNT(*) AS order_count, SUM(gmv_usd) AS gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
GROUP BY 1, 2;
```

#### 2025-05-12 08:30:10 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990202_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 36,000,000 bytes
* **Duration:** 0.52s
* **Query Text:**
```sql
-- Checking fact_marketplace_listings authenticity verification counts by category
category, authenticity_verified, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY 1, 2;
```

#### 2025-05-12 10:15:33 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990203_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 52,000,000 bytes
* **Duration:** 0.74s
* **Query Text:**
```sql
-- Checking fulfillment_speed_daily metrics by market and fulfillment type
market, fulfillment_type, AVG(on_time_rate) AS avg_on_time, AVG(avg_cost_per_order_usd) AS avg_cost
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
GROUP BY 1, 2;
```

#### 2025-05-12 13:20:40 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990204_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 24,000,000 bytes
* **Duration:** 0.38s
* **Query Text:**
```sql
-- Checking dim_seller status distribution across the panel
status, fulfillment_method, COUNT(*) AS seller_count
FROM `nexus-analyst-demo.acme_ecomm.dim_seller`
GROUP BY 1, 2;
```

#### 2025-05-12 15:05:12 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990205_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 175,000,000 bytes
* **Duration:** 1.89s
* **Query Text:**
```sql
-- Checking fact_experiment_readouts metric summary across experiments
metric_name, COUNT(*) AS readout_count, AVG(metric_value) AS avg_value
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`
GROUP BY 1;
```

#### 2025-05-13 09:11:00 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990206_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 29,000,000 bytes
* **Duration:** 0.45s
* **Query Text:**
```sql
-- Checking fact_voc_responses sentiment distribution
sentiment, COUNT(*) AS response_count, AVG(score) AS avg_score
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
GROUP BY 1;
```

#### 2025-05-13 11:40:19 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990207_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 94,000,000 bytes
* **Duration:** 1.15s
* **Query Text:**
```sql
-- Checking traffic_conversion_summary version breakdown for sessions definition
sessions_definition_version, COUNT(*) AS row_count, SUM(sessions) AS total_sessions
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
GROUP BY 1;
```

#### 2025-05-13 14:22:50 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990208_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 16,000,000 bytes
* **Duration:** 0.31s
* **Query Text:**
```sql
-- Checking dim_marketing_calendar spend totals by vertical
vertical_code, SUM(actual_spend_usd) AS total_actual_spend, SUM(planned_spend_usd) AS total_planned_spend
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
GROUP BY 1;
```

#### 2025-05-13 16:10:05 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990209_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 85,000,000 bytes
* **Duration:** 1.02s
* **Query Text:**
```sql
-- Checking member_cltv active status breakdown
is_active, COUNT(*) AS member_count, AVG(lifetime_gmv_usd) AS avg_lifetime_gmv
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`
GROUP BY 1;
```

#### 2025-05-14 08:50:20 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990210_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 48,000,000 bytes
* **Duration:** 0.68s
* **Query Text:**
```sql
-- Checking fact_care_contacts resolution codes distribution
resolution_code, channel, COUNT(*) AS contact_count
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1, 2;
```

#### 2025-05-14 11:05:40 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990211_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 33,000,000 bytes
* **Duration:** 0.50s
* **Query Text:**
```sql
-- Checking dim_member panel size query test (verifying sample vs true base)
SELECT COUNT(*) AS sample_member_count FROM `nexus-analyst-demo.acme_ecomm.dim_member`;
-- Note: confirms 120,000 rows in panel; company-level member totals must come from aggregate marts.
```

#### 2025-05-14 13:30:15 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990212_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 21,000,000 bytes
* **Duration:** 0.36s
* **Query Text:**
```sql
-- Checking dim_fulfillment_node store formats distribution
store_format, COUNT(*) AS store_count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE node_type = 'store'
GROUP BY 1;
```

#### 2025-05-14 15:45:00 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990213_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 115,000,000 bytes
* **Duration:** 1.39s
* **Query Text:**
```sql
-- Checking marketplace_seller_performance metrics summary by category focus
category_focus, SUM(trailing_90d_gmv_usd) AS total_gmv, AVG(avg_buyer_rating) AS mean_rating
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
GROUP BY 1;
```

#### 2025-05-15 09:05:22 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990214_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 62,000,000 bytes
* **Duration:** 0.84s
* **Query Text:**
```sql
-- Checking fact_voc_responses theme tags frequency
theme_tag, COUNT(*) AS tag_count, AVG(score) AS avg_score
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
GROUP BY 1
ORDER BY tag_count DESC
LIMIT 15;
```

#### 2025-05-15 11:20:10 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990215_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 78,000,000 bytes
* **Duration:** 0.98s
* **Query Text:**
```sql
-- Checking fact_traffic_daily vertical breakdown for US market
vertical_code, SUM(sessions) AS total_sessions, SUM(gmv_usd) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE market = 'US'
GROUP BY 1;
```

#### 2025-05-15 14:15:44 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990216_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 17,000,000 bytes
* **Duration:** 0.30s
* **Query Text:**
```sql
-- Checking dim_vertical sub-vertical mappings
vertical_code, sub_vertical_code, sub_vertical_name
FROM `nexus-analyst-demo.acme_ecomm.dim_vertical`
WHERE sub_vertical_code IS NOT NULL;
```

#### 2025-05-15 16:30:00 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990217_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 190,000,000 bytes
* **Duration:** 2.05s
* **Query Text:**
```sql
-- Checking fact_orders return reasons distribution
return_reason_code, COUNT(*) AS return_count, SUM(refund_usd) AS total_refunds
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE is_returned = TRUE
GROUP BY 1;
```

#### 2025-05-15 18:20:11 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990218_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 45,000,000 bytes
* **Duration:** 0.65s
* **Query Text:**
```sql
-- Checking fact_orders shipping method breakdown
fulfillment_type, COUNT(*) AS order_count, SUM(gmv_usd) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
GROUP BY 1;
```

#### 2025-05-15 19:40:05 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990219_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 12,000,000 bytes
* **Duration:** 0.22s
* **Query Text:**
```sql
-- Checking dim_fulfillment_node active DCs count
node_type, COUNT(*) AS node_count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE is_active = TRUE
GROUP BY 1;
```

#### 2025-05-16 08:12:30 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990220_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 112,000,000 bytes
* **Duration:** 1.34s
* **Query Text:**
```sql
-- Validating traffic sessions definition version split
sessions_definition_version, COUNT(*) AS day_count, SUM(sessions) AS total_sessions
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
GROUP BY 1;
```

#### 2025-05-16 10:05:18 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990221_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 24,000,000 bytes
* **Duration:** 0.41s
* **Query Text:**
```sql
-- Checking dim_experiment status breakdown
status, COUNT(*) AS experiment_count
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment`
GROUP BY 1;
```

#### 2025-05-16 11:30:45 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990222_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 58,000,000 bytes
* **Duration:** 0.77s
* **Query Text:**
```sql
-- Checking fact_care_contacts channel distribution
channel, COUNT(*) AS contact_count, AVG(csat_score) AS mean_csat
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1;
```

#### 2025-05-16 13:22:09 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990223_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 8,000,000 bytes
* **Duration:** 0.18s
* **Query Text:**
```sql
-- Checking dim_marketing_calendar event types
event_type, COUNT(*) AS event_count
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
GROUP BY 1;
```

#### 2025-05-16 15:10:00 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990224_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 150,000,000 bytes
* **Duration:** 1.65s
* **Query Text:**
```sql
-- Checking fact_promise_vs_actual on-time rates by fulfillment type
fulfillment_type, SUM(orders_promised) AS promised, SUM(orders_on_time) AS on_time
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
GROUP BY 1;
```

#### 2025-05-16 16:55:12 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990225_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 31,000,000 bytes
* **Duration:** 0.50s
* **Query Text:**
```sql
-- Checking dim_associate team distribution
team, COUNT(*) AS associate_count
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
WHERE is_active = TRUE
GROUP BY 1;
```

#### 2025-05-19 09:14:02 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990226_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 65,000,000 bytes
* **Duration:** 0.82s
* **Query Text:**
```sql
-- Checking fact_voc_responses survey type counts
survey_type, COUNT(*) AS response_count, AVG(score) AS avg_score
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
GROUP BY 1;
```

#### 2025-05-19 10:45:33 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990227_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 22,000,000 bytes
* **Duration:** 0.35s
* **Query Text:**
```sql
-- Checking dim_date fiscal quarter labels
fiscal_quarter_label, COUNT(*) AS day_count
FROM `nexus-analyst-demo.acme_ecomm.dim_date`
GROUP BY 1
ORDER BY 1;
```

#### 2025-05-19 13:20:15 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990228_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 95,000,000 bytes
* **Duration:** 1.12s
* **Query Text:**
```sql
-- Checking traffic_conversion_summary weekly trends for CA market
fiscal_week_ending, sessions, conversion_rate, gmv_usd
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'CA'
ORDER BY 1 DESC
LIMIT 10;
```

#### 2025-05-19 15:02:44 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990229_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 18,000,000 bytes
* **Duration:** 0.28s
* **Query Text:**
```sql
-- Checking fulfillment_speed_daily mix shares
date, fulfillment_type, pct_of_total_orders
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
WHERE date >= '2025-05-01'
ORDER BY date DESC
LIMIT 10;
```

#### 2025-05-19 16:45:10 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990230_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 40,000,000 bytes
* **Duration:** 0.60s
* **Query Text:**
```sql
-- Checking care_deflection_daily trends
sub_program, AVG(deflection_rate) AS mean_deflection, AVG(contact_volume) AS mean_volume
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
GROUP BY 1;
```

#### 2025-05-20 09:10:25 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990231_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 125,000,000 bytes
* **Duration:** 1.40s
* **Query Text:**
```sql
-- Testing member_cltv join against dim_member
SELECT 
    COUNT(m.member_id) AS total_panel_members,
    COUNT(c.member_id) AS members_with_cltv_record,
    AVG(c.projected_cltv_usd) AS mean_projected_cltv
FROM `nexus-analyst-demo.acme_ecomm.dim_member` m
LEFT JOIN `nexus-analyst-demo.acme_ecomm.member_cltv` c ON m.member_id = c.member_id;
```

#### 2025-05-20 11:05:40 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990232_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 15,000,000 bytes
* **Duration:** 0.25s
* **Query Text:**
```sql
-- Checking marketplace_seller_performance category focus distribution
category_focus, COUNT(*) AS seller_count
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
GROUP BY 1;
```

#### 2025-05-20 14:30:15 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990233_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 88,000,000 bytes
* **Duration:** 0.95s
* **Query Text:**
```sql
-- Checking marketplace_gmv_summary weekly sub_vertical split
fiscal_week_ending, sub_vertical_code, SUM(gmv_usd) AS weekly_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
GROUP BY 1, 2
ORDER BY 1 DESC
LIMIT 12;
```

#### 2025-05-20 16:15:00 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990234_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 52,000,000 bytes
* **Duration:** 0.71s
* **Query Text:**
```sql
-- Checking fact_membership_events event type breakdown
event_type, COUNT(*) AS event_count
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
GROUP BY 1;
```

#### 2025-05-21 09:05:12 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990235_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 110,000,000 bytes
* **Duration:** 1.25s
* **Query Text:**
```sql
-- Checking fact_experiment_exposures total assigned vs exposed
experiment_id, SUM(units_assigned) AS assigned, SUM(units_exposed) AS exposed
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures`
GROUP BY 1
LIMIT 10;
```

#### 2025-05-21 10:40:50 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990236_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 19,000,000 bytes
* **Duration:** 0.32s
* **Query Text:**
```sql
-- Checking dim_vertical deep dive flags
vertical_code, vertical_name, is_deep_dive
FROM `nexus-analyst-demo.acme_ecomm.dim_vertical`
WHERE is_deep_dive = TRUE;
```

#### 2025-05-21 13:15:20 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990237_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 74,000,000 bytes
* **Duration:** 0.89s
* **Query Text:**
```sql
-- Checking fact_orders market and channel breakdown
market, channel, COUNT(*) AS order_count, SUM(gmv_usd) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
GROUP BY 1, 2;
```

#### 2025-05-21 15:50:11 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990238_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 35,000,000 bytes
* **Duration:** 0.52s
* **Query Text:**
```sql
-- Checking fact_voc_responses theme tags for care contacts
theme_tag, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE survey_type = 'post_care_contact'
GROUP BY 1
ORDER BY count DESC
LIMIT 10;
```

#### 2025-05-22 09:20:00 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990239_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 82,000,000 bytes
* **Duration:** 0.95s
* **Query Text:**
```sql
-- Checking fact_traffic_daily device breakdown for US
device, SUM(sessions) AS total_sessions, SUM(orders) AS total_orders
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
WHERE market = 'US'
GROUP BY 1;
```

#### 2025-05-22 11:15:44 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990240_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 14,000,000 bytes
* **Duration:** 0.24s
* **Query Text:**
```sql
-- Checking dim_seller status breakdown
status, COUNT(*) AS seller_count
FROM `nexus-analyst-demo.acme_ecomm.dim_seller`
GROUP BY 1;
```

#### 2025-05-22 14:05:18 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990241_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 105,000,000 bytes
* **Duration:** 1.18s
* **Query Text:**
```sql
-- Checking fact_experiment_readouts metrics summary
metric_name, COUNT(*) AS readout_count, AVG(metric_value) AS mean_value
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`
GROUP BY 1;
```

#### 2025-05-22 16:30:22 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990242_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 48,000,000 bytes
* **Duration:** 0.68s
* **Query Text:**
```sql
-- Checking fact_care_contacts resolution codes frequency
resolution_code, COUNT(*) AS count, AVG(handle_time_minutes) AS mean_handle_time
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1
ORDER BY count DESC
LIMIT 15;
```

#### 2025-05-23 09:12:05 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990243_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 60,000,000 bytes
* **Duration:** 0.75s
* **Query Text:**
```sql
-- Checking traffic_conversion_summary US conversion by fiscal week
fiscal_week_ending, conversion_rate, gmv_usd
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'US'
ORDER BY fiscal_week_ending DESC
LIMIT 10;
```

#### 2025-05-23 11:02:30 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990244_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 16,000,000 bytes
* **Duration:** 0.27s
* **Query Text:**
```sql
-- Checking dim_member home market distribution
home_market, COUNT(*) AS member_count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
GROUP BY 1;
```

#### 2025-05-23 13:45:10 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990245_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 92,000,000 bytes
* **Duration:** 1.05s
* **Query Text:**
```sql
-- Checking marketplace_seller_performance average buyer ratings by category
category_focus, AVG(avg_buyer_rating) AS mean_rating, AVG(return_rate) AS mean_return_rate
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
GROUP BY 1;
```

#### 2025-05-23 15:55:40 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990246_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 42,000,000 bytes
* **Duration:** 0.58s
* **Query Text:**
```sql
-- Checking fact_marketplace_listings authenticity verification counts
category, authenticity_verified, COUNT(*) AS listing_count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY 1, 2;
```

#### 2025-05-23 18:20:15 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990247_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 18,000,000 bytes
* **Duration:** 0.31s
* **Query Text:**
```sql
-- Checking dim_associate active records count by team
team, COUNT(*) AS associate_count
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
WHERE is_active = TRUE
GROUP BY 1;
```

#### 2025-05-24 08:14:02 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990248_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 35,000,000 bytes
* **Duration:** 0.49s
* **Query Text:**
```sql
-- Checking fact_orders distribution by channel and market
market, channel, COUNT(*) AS order_count, SUM(gmv_usd) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
GROUP BY 1, 2;
```

#### 2025-05-24 10:30:15 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990249_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 11,000,000 bytes
* **Duration:** 0.22s
* **Query Text:**
```sql
-- Checking dim_fulfillment_node active DCs count
market, COUNT(*) AS node_count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE node_type = 'dc' AND is_active = TRUE
GROUP BY 1;
```

#### 2025-05-24 14:05:50 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990250_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 88,000,000 bytes
* **Duration:** 0.94s
* **Query Text:**
```sql
-- Checking care_deflection_daily average CSAT by sub_program
sub_program, AVG(avg_csat_deflected) AS mean_deflected_csat, AVG(avg_csat_agent_assisted) AS mean_agent_csat
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
GROUP BY 1;
```

#### 2025-05-25 09:44:12 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990251_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 25,000,000 bytes
* **Duration:** 0.38s
* **Query Text:**
```sql
-- Checking dim_marketing_calendar event types frequency
event_type, COUNT(*) AS event_count
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
GROUP BY 1;
```

#### 2025-05-25 11:22:08 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990252_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 110,000,000 bytes
* **Duration:** 1.22s
* **Query Text:**
```sql
-- Checking fulfillment_speed_daily on_time_rate by vertical
vertical_code, AVG(on_time_rate) AS mean_on_time_rate
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
GROUP BY 1;
```

#### 2025-05-25 15:18:45 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990253_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 14,000,000 bytes
* **Duration:** 0.25s
* **Query Text:**
```sql
-- Checking dim_experiment status distribution
status, COUNT(*) AS experiment_count
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment`
GROUP BY 1;
```

#### 2025-05-26 09:05:30 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990254_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 45,000,000 bytes
* **Duration:** 0.61s
* **Query Text:**
```sql
-- Checking fact_membership_events event types breakdown
event_type, COUNT(*) AS event_count
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
GROUP BY 1;
```

#### 2025-05-26 11:40:19 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990255_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 30,000,000 bytes
* **Duration:** 0.42s
* **Query Text:**
```sql
-- Checking fact_experiment_readouts metric distribution
metric_name, COUNT(*) AS readout_count, AVG(metric_value) AS mean_val
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`
GROUP BY 1;
```

#### 2025-05-26 16:12:04 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990256_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 75,000,000 bytes
* **Duration:** 0.89s
* **Query Text:**
```sql
-- Checking fact_orders return reasons frequency
return_reason_code, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE is_returned = TRUE
GROUP BY 1
ORDER BY count DESC;
```

#### 2025-05-27 08:33:50 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990257_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 19,000,000 bytes
* **Duration:** 0.29s
* **Query Text:**
```sql
-- Checking dim_vertical deep dive flags
is_deep_dive, COUNT(*) AS vertical_count
FROM `nexus-analyst-demo.acme_ecomm.dim_vertical`
GROUP BY 1;
```

#### 2025-05-27 10:15:22 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990258_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 52,000,000 bytes
* **Duration:** 0.67s
* **Query Text:**
```sql
-- Checking fact_voc_responses survey type counts and average scores
survey_type, COUNT(*) AS response_count, AVG(score) AS mean_score
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
GROUP BY 1;
```

#### 2025-05-27 13:50:11 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990259_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 64,000,000 bytes
* **Duration:** 0.78s
* **Query Text:**
```sql
-- Checking fact_care_contacts channel usage breakdown
channel, COUNT(*) AS contact_count, AVG(handle_time_minutes) AS avg_handle_time
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1;
```

#### 2025-05-28 09:12:44 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990260_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 40,000,000 bytes
* **Duration:** 0.52s
* **Query Text:**
```sql
-- Checking marketplace_gmv_summary totals by sub_vertical
sub_vertical_code, SUM(gmv_usd) AS total_gmv, SUM(orders) AS total_orders
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
GROUP BY 1;
```

#### 2025-05-28 11:04:18 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990261_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 12,000,000 bytes
* **Duration:** 0.24s
* **Query Text:**
```sql
-- Checking dim_date peak holiday distribution
is_peak_holiday, COUNT(*) AS day_count
FROM `nexus-analyst-demo.acme_ecomm.dim_date`
GROUP BY 1;
```

#### 2025-05-28 15:45:02 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990262_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 85,000,000 bytes
* **Duration:** 0.98s
* **Query Text:**
```sql
-- Checking member_cltv lifetime orders vs lifetime gmv correlation preview
lifetime_orders, AVG(lifetime_gmv_usd) AS avg_gmv, COUNT(*) AS member_count
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`
GROUP BY 1
ORDER BY lifetime_orders DESC
LIMIT 10;
```

#### 2025-05-29 09:20:15 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990263_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 33,000,000 bytes
* **Duration:** 0.46s
* **Query Text:**
```sql
-- Checking fact_care_contacts deflection status breakdown
deflected, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1;
```

#### 2025-05-29 11:15:30 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990264_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 58,000,000 bytes
* **Duration:** 0.72s
* **Query Text:**
```sql
-- Checking traffic_conversion_summary sessions definition version breakdown
sessions_definition_version, SUM(sessions) AS total_sessions, AVG(conversion_rate) AS mean_conversion
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
GROUP BY 1;
```

#### 2025-05-29 14:50:10 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990265_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 15,000,000 bytes
* **Duration:** 0.26s
* **Query Text:**
```sql
-- Checking dim_member acquisition channels
acquisition_channel, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
GROUP BY 1;
```

#### 2025-05-30 08:45:00 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990266_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 48,000,000 bytes
* **Duration:** 0.62s
* **Query Text:**
```sql
-- Checking marketplace_seller_performance category focus averages
category_focus, COUNT(*) AS seller_count, AVG(trailing_90d_gmv_usd) AS mean_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
GROUP BY 1;
```

#### 2025-05-30 11:10:25 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990267_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 22,000,000 bytes
* **Duration:** 0.35s
* **Query Text:**
```sql
-- Checking fact_voc_responses sentiment breakdown
sentiment, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
GROUP BY 1;
```

#### 2025-05-30 15:30:44 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990268_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 95,000,000 bytes
* **Duration:** 1.10s
* **Query Text:**
```sql
-- Checking fact_traffic_daily sessions by device type
device, SUM(sessions) AS total_sessions, SUM(orders) AS total_orders
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
GROUP BY 1;
```

#### 2025-05-30 18:12:09 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990269_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 112,000,000 bytes
* **Duration:** 1.45s
* **Query Text:**
```sql
-- Monthly channel breakdown for traffic and orders
market, channel, SUM(sessions) AS total_sessions, SUM(orders) AS total_orders
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
GROUP BY 1, 2;
```

#### 2025-05-31 09:15:30 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990270_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 8,000,000 bytes
* **Duration:** 0.15s
* **Query Text:**
```sql
-- Checking dim_fulfillment_node active DCs
node_id, node_name, market
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE node_type = 'dc' AND is_active = TRUE;
```

#### 2025-05-31 11:22:40 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990271_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 34,000,000 bytes
* **Duration:** 0.44s
* **Query Text:**
```sql
-- Checking care contacts channel distribution
channel, COUNT(*) AS volume
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1;
```

#### 2025-06-01 08:30:12 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990272_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 65,000,000 bytes
* **Duration:** 0.82s
* **Query Text:**
```sql
-- Validating traffic_conversion_summary weekly rollups for US
fiscal_week_ending, SUM(sessions) AS sessions, SUM(orders) AS orders
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
WHERE market = 'US'
GROUP BY 1
ORDER BY 1 DESC;
```

#### 2025-06-01 10:05:50 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990273_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 140,000,000 bytes
* **Duration:** 1.88s
* **Query Text:**
```sql
-- Joining fact_orders with dim_member for acquisition channel analysis
m.acquisition_channel, COUNT(o.order_id) AS total_orders, SUM(o.gmv_usd) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders` o
LEFT JOIN `nexus-analyst-demo.acme_ecomm.dim_member` m ON o.member_id = m.member_id
GROUP BY 1;
```

#### 2025-06-02 07:45:11 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990274_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 12,000,000 bytes
* **Duration:** 0.20s
* **Query Text:**
```sql
-- Checking dim_experiment statuses
status, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment`
GROUP BY 1;
```

#### 2025-06-02 13:20:00 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990275_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 41,000,000 bytes
* **Duration:** 0.55s
* **Query Text:**
```sql
-- Checking fact_voc_responses by survey type
survey_type, COUNT(*) AS count, AVG(score) AS mean_score
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
GROUP BY 1;
```

#### 2025-06-03 09:10:22 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990276_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 88,000,000 bytes
* **Duration:** 1.02s
* **Query Text:**
```sql
-- Checking fulfillment_speed_daily on_time_rate by fulfillment type
fulfillment_type, AVG(on_time_rate) AS mean_on_time_rate
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
GROUP BY 1;
```

#### 2025-06-03 14:05:33 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990277_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 19,000,000 bytes
* **Duration:** 0.31s
* **Query Text:**
```sql
-- Checking marketplace_gmv_summary sub_vertical breakdown
sub_vertical_code, SUM(gmv_usd) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
GROUP BY 1;
```

#### 2025-06-04 08:50:19 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990278_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 25,000,000 bytes
* **Duration:** 0.38s
* **Query Text:**
```sql
-- Checking dim_marketing_calendar event types
event_type, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
GROUP BY 1;
```

#### 2025-06-04 11:30:45 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990279_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 52,000,000 bytes
* **Duration:** 0.69s
* **Query Text:**
```sql
-- Checking care_deflection_daily deflection rate by sub_program
sub_program, AVG(deflection_rate) AS mean_deflection_rate
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
GROUP BY 1;
```

#### 2025-06-05 09:25:14 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990280_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 76,000,000 bytes
* **Duration:** 0.94s
* **Query Text:**
```sql
-- Checking fact_membership_events event type distribution
event_type, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
GROUP BY 1;
```

#### 2025-06-05 15:10:02 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990281_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 105,000,000 bytes
* **Duration:** 1.32s
* **Query Text:**
```sql
-- Checking member_cltv distribution across active members
is_active, COUNT(*) AS member_count, AVG(projected_cltv_usd) AS mean_cltv
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`
GROUP BY 1;
```

#### 2025-06-06 08:15:40 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990282_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 14,000,000 bytes
* **Duration:** 0.22s
* **Query Text:**
```sql
-- Checking dim_vertical deep dive flag count
is_deep_dive, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.dim_vertical`
GROUP BY 1;
```

#### 2025-06-06 11:45:20 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990283_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 29,000,000 bytes
* **Duration:** 0.41s
* **Query Text:**
```sql
-- Checking fact_marketplace_listings authenticity verification breakdown
authenticity_verified, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY 1;
```

#### 2025-06-09 09:00:15 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990284_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 82,000,000 bytes
* **Duration:** 0.99s
* **Query Text:**
```sql
-- Checking fact_promise_vs_actual performance by fulfillment type
fulfillment_type, SUM(orders_promised) AS promised, SUM(orders_on_time) AS on_time
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
GROUP BY 1;
```

#### 2025-06-09 14:30:22 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990285_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 94,000,000 bytes
* **Duration:** 1.15s
* **Query Text:**
```sql
-- Checking marketplace_seller_performance category focus averages
category_focus, COUNT(*) AS sellers, AVG(trailing_90d_gmv_usd) AS avg_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
GROUP BY 1;
```

#### 2025-06-10 08:20:10 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990286_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 18,000,000 bytes
* **Duration:** 0.29s
* **Query Text:**
```sql
-- Checking dim_associate roles in Data team
role, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
WHERE team = 'Data'
GROUP BY 1;
```

#### 2025-06-10 11:15:55 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990287_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 45,000,000 bytes
* **Duration:** 0.58s
* **Query Text:**
```sql
-- Checking fact_voc_responses sentiment counts by vertical
vertical_code, sentiment, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
GROUP BY 1, 2;
```

#### 2025-06-11 09:10:44 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990288_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 61,000,000 bytes
* **Duration:** 0.78s
* **Query Text:**
```sql
-- Checking fact_traffic_daily by device and market
market, device, SUM(sessions) AS sessions
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
GROUP BY 1, 2;
```

#### 2025-06-11 15:40:12 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990289_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 110,000,000 bytes
* **Duration:** 1.39s
* **Query Text:**
```sql
-- Checking fact_orders fulfillment type breakdown
fulfillment_type, COUNT(*) AS order_count, SUM(gmv_usd) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
GROUP BY 1;
```

#### 2025-06-12 08:30:25 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990290_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 11,000,000 bytes
* **Duration:** 0.18s
* **Query Text:**
```sql
-- Checking dim_seller status distribution
status, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.dim_seller`
GROUP BY 1;
```

#### 2025-06-12 13:05:18 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990291_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 38,000,000 bytes
* **Duration:** 0.51s
* **Query Text:**
```sql
-- Checking fact_care_contacts resolution codes
resolution_code, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1;
```

#### 2025-06-13 09:15:00 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990292_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 70,000,000 bytes
* **Duration:** 0.89s
* **Query Text:**
```sql
-- Checking traffic_conversion_summary version breakdown
sessions_definition_version, SUM(orders) AS total_orders
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
GROUP BY 1;
```

#### 2025-06-13 14:22:11 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990293_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 85,000,000 bytes
* **Duration:** 1.08s
* **Query Text:**
```sql
-- Checking marketplace_gmv_summary take rate by sub_vertical
sub_vertical_code, AVG(take_rate) AS avg_take_rate
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
GROUP BY 1;
```

#### 2025-06-16 08:40:15 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990294_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 15,000,000 bytes
* **Duration:** 0.25s
* **Query Text:**
```sql
-- Checking dim_member plan types
plan_type, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
GROUP BY 1;
```

#### 2025-06-16 11:30:50 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990295_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 42,000,000 bytes
* **Duration:** 0.56s
* **Query Text:**
```sql
-- Checking care_deflection_daily handle times
sub_program, AVG(avg_handle_time_minutes) AS mean_handle_time
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
GROUP BY 1;
```

#### 2025-06-17 09:05:33 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990296_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 58,000,000 bytes
* **Duration:** 0.74s
* **Query Text:**
```sql
-- Checking fact_experiment_exposures totals by variant
variant, SUM(units_assigned) AS assigned, SUM(units_exposed) AS exposed
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures`
GROUP BY 1;
```

#### 2025-06-17 15:12:40 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990297_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 125,000,000 bytes
* **Duration:** 1.55s
* **Query Text:**
```sql
-- Checking member_cltv benefits adopted count distribution
benefits_adopted_count, COUNT(*) AS member_count, AVG(trailing_12mo_gmv_usd) AS avg_gmv
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`
GROUP BY 1;
```

#### 2025-06-18 08:20:12 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990298_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 13,000,000 bytes
* **Duration:** 0.21s
* **Query Text:**
```sql
-- Checking dim_fulfillment_node store formats
store_format, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
WHERE store_format IS NOT NULL
GROUP BY 1;
```

#### 2025-06-18 11:45:00 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990299_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 31,000,000 bytes
* **Duration:** 0.43s
* **Query Text:**
```sql
-- Checking fact_voc_responses score types
score_type, COUNT(*) AS count, AVG(score) AS mean_score
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
GROUP BY 1;
```

#### 2025-06-19 09:10:25 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990300_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 91,000,000 bytes
* **Duration:** 1.12s
* **Query Text:**
```sql
-- Checking fulfillment_speed_daily cost per order by vertical
vertical_code, AVG(avg_cost_per_order_usd) AS mean_cost
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
GROUP BY 1;
```

#### 2025-06-19 14:35:19 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990301_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 78,000,000 bytes
* **Duration:** 0.98s
* **Query Text:**
```sql
-- Checking marketplace_seller_performance return rates by category
category_focus, AVG(return_rate) AS mean_return_rate
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
GROUP BY 1;
```

#### 2025-06-20 08:50:11 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990302_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 17,000,000 bytes
* **Duration:** 0.27s
* **Query Text:**
```sql
-- Checking dim_experiment primary metrics
primary_metric, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.dim_experiment`
GROUP BY 1;
```

#### 2025-06-20 11:20:44 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990303_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 49,000,000 bytes
* **Duration:** 0.63s
* **Query Text:**
```sql
-- Checking fact_care_contacts sub_program volume
sub_program, COUNT(*) AS contact_count
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1;
```

#### 2025-06-23 09:15:30 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990304_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 68,000,000 bytes
* **Duration:** 0.85s
* **Query Text:**
```sql
-- Checking fact_traffic_daily sessions by vertical
vertical_code, SUM(sessions) AS total_sessions
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
GROUP BY 1;
```

#### 2025-06-23 15:00:12 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990305_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 115,000,000 bytes
* **Duration:** 1.42s
* **Query Text:**
```sql
-- Checking fact_orders return reasons
return_reason_code, COUNT(*) AS count, SUM(refund_usd) AS total_refunds
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
WHERE is_returned = TRUE
GROUP BY 1;
```

#### 2025-06-24 08:30:15 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990306_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 10,000,000 bytes
* **Duration:** 0.16s
* **Query Text:**
```sql
-- Checking dim_seller fulfillment methods
fulfillment_method, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.dim_seller`
GROUP BY 1;
```

#### 2025-06-24 11:10:40 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990307_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 36,000,000 bytes
* **Duration:** 0.48s
* **Query Text:**
```sql
-- Checking fact_membership_events channel distribution
channel, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.fact_membership_events`
GROUP BY 1;
```

#### 2025-06-25 09:05:22 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990308_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 74,000,000 bytes
* **Duration:** 0.92s
* **Query Text:**
```sql
-- Checking traffic_conversion_summary market comparison
market, SUM(sessions) AS sessions, AVG(conversion_rate) AS mean_conv
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
GROUP BY 1;
```

#### 2025-06-25 14:45:10 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990309_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 98,000,000 bytes
* **Duration:** 1.21s
* **Query Text:**
```sql
-- Checking marketplace_gmv_summary orders by sub_vertical
sub_vertical_code, SUM(orders) AS total_orders
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
GROUP BY 1;
```

#### 2025-06-26 08:25:00 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990310_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 16,000,000 bytes
* **Duration:** 0.25s
* **Query Text:**
```sql
-- Checking dim_marketing_calendar owners
owner_assoc_id, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
GROUP BY 1;
```

#### 2025-06-26 11:35:18 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990311_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 44,000,000 bytes
* **Duration:** 0.59s
* **Query Text:**
```sql
-- Checking care_deflection_daily csat deflected vs agent assisted
AVG(avg_csat_deflected) AS mean_csat_deflected, AVG(avg_csat_agent_assisted) AS mean_csat_agent
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`;
```

#### 2025-06-27 09:10:45 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990312_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 63,000,000 bytes
* **Duration:** 0.81s
* **Query Text:**
```sql
-- Checking fact_experiment_readouts metric distribution
metric_name, COUNT(*) AS count, AVG(metric_value) AS mean_val
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`
GROUP BY 1;
```

#### 2025-06-27 15:20:12 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990313_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 102,000,000 bytes
* **Duration:** 1.28s
* **Query Text:**
```sql
-- Checking member_cltv tenure days distribution
ROUND(tenure_days / 30) AS tenure_months, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`
GROUP BY 1
ORDER BY 1;
```

#### 2025-06-30 08:40:10 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990314_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 12,000,000 bytes
* **Duration:** 0.19s
* **Query Text:**
```sql
-- Checking dim_vertical sub_vertical codes
sub_vertical_code, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.dim_vertical`
WHERE sub_vertical_code IS NOT NULL
GROUP BY 1;
```

#### 2025-06-30 11:15:33 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990315_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 33,000,000 bytes
* **Duration:** 0.46s
* **Query Text:**
```sql
-- Checking fact_marketplace_listings category breakdown
category, COUNT(*) AS count, AVG(price_usd) AS mean_price
FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
GROUP BY 1;
```

#### 2025-07-01 09:00:20 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990316_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 79,000,000 bytes
* **Duration:** 0.97s
* **Query Text:**
```sql
-- Checking fact_traffic_daily add to cart vs checkout started
SUM(add_to_cart_sessions) AS atc, SUM(checkout_started_sessions) AS checkout
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`;
```

#### 2025-07-01 14:10:55 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990317_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 89,000,000 bytes
* **Duration:** 1.11s
* **Query Text:**
```sql
-- Checking marketplace_seller_performance listing counts
category_focus, SUM(active_listings) AS total_listings
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
GROUP BY 1;
```

#### 2025-07-02 08:35:12 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990318_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 19,000,000 bytes
* **Duration:** 0.31s
* **Query Text:**
```sql
-- Checking dim_associate locations
location, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.dim_associate`
GROUP BY 1;
```

#### 2025-07-02 11:40:00 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990319_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 47,000,000 bytes
* **Duration:** 0.61s
* **Query Text:**
```sql
-- Checking fact_voc_responses score distribution for csat
score, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE score_type = 'csat_1_5'
GROUP BY 1;
```

#### 2025-07-03 09:12:44 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990320_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 72,000,000 bytes
* **Duration:** 0.90s
* **Query Text:**
```sql
-- Checking fulfillment_speed_daily on time rate by market
market, AVG(on_time_rate) AS mean_on_time
FROM `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
GROUP BY 1;
```

#### 2025-07-03 15:05:18 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990321_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 118,000,000 bytes
* **Duration:** 1.48s
* **Query Text:**
```sql
-- Checking fact_orders channel and device breakdown
channel, device, COUNT(*) AS order_count, SUM(gmv_usd) AS gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
GROUP BY 1, 2;
```

#### 2025-07-07 08:45:10 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990322_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 14,000,000 bytes
* **Duration:** 0.23s
* **Query Text:**
```sql
-- Checking dim_member home markets
home_market, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.dim_member`
GROUP BY 1;
```

#### 2025-07-07 11:25:33 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990323_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 39,000,000 bytes
* **Duration:** 0.52s
* **Query Text:**
```sql
-- Checking care_deflection_daily volume by date
date, SUM(contact_volume) AS total_volume
FROM `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
GROUP BY 1
ORDER BY 1 DESC
LIMIT 10;
```

#### 2025-07-08 09:05:15 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990324_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 84,000,000 bytes
* **Duration:** 1.05s
* **Query Text:**
```sql
-- Checking traffic_conversion_summary quarterly aggregation
market, SUM(sessions) AS sessions, SUM(orders) AS orders
FROM `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
GROUP BY 1;
```

#### 2025-07-08 14:15:22 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990325_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 95,000,000 bytes
* **Duration:** 1.19s
* **Query Text:**
```sql
-- Checking marketplace_gmv_summary weekly trend
fiscal_week_ending, SUM(gmv_usd) AS weekly_gmv
FROM `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
GROUP BY 1
ORDER BY 1 DESC
LIMIT 10;
```

#### 2025-07-09 08:30:40 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990326_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 11,000,000 bytes
* **Duration:** 0.18s
* **Query Text:**
```sql
-- Checking dim_seller home countries
home_country, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.dim_seller`
GROUP BY 1;
```

#### 2025-07-09 11:50:12 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990327_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 35,000,000 bytes
* **Duration:** 0.47s
* **Query Text:**
```sql
-- Checking fact_care_contacts deflected vs not deflected
deflected, COUNT(*) AS count, AVG(csat_score) AS mean_csat
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1;
```

#### 2025-07-10 09:10:19 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990328_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 67,000,000 bytes
* **Duration:** 0.86s
* **Query Text:**
```sql
-- Checking fact_experiment_readouts significance count
is_significant, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`
GROUP BY 1;
```

#### 2025-07-10 15:22:05 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990329_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 108,000,000 bytes
* **Duration:** 1.35s
* **Query Text:**
```sql
-- Checking member_cltv trailing 12mo gmv sum by cohort
signup_cohort_quarter, SUM(trailing_12mo_gmv_usd) AS total_gmv, COUNT(*) AS members
FROM `nexus-analyst-demo.acme_ecomm.member_cltv`
GROUP BY 1
ORDER BY 1;
```

#### 2025-07-11 08:20:15 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990330_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 15,000,000 bytes
* **Duration:** 0.24s
* **Query Text:**
```sql
-- Checking dim_date peak holiday flags
is_peak_holiday, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.dim_date`
GROUP BY 1;
```

#### 2025-07-11 11:30:44 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990331_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 40,000,000 bytes
* **Duration:** 0.54s
* **Query Text:**
```sql
-- Checking fact_voc_responses theme tags
theme_tag, COUNT(*) AS count
FROM `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
WHERE theme_tag IS NOT NULL
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10;
```

#### 2025-07-14 09:05:10 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990332_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 75,000,000 bytes
* **Duration:** 0.93s
* **Query Text:**
```sql
-- Checking fact_traffic_daily sessions vs product view sessions
SUM(sessions) AS sessions, SUM(product_view_sessions) AS product_views
FROM `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`;
```

#### 2025-07-14 14:40:20 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990333_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 81,000,000 bytes
* **Duration:** 1.01s
* **Query Text:**
```sql
-- Checking marketplace_seller_performance avg buyer rating by category
category_focus, AVG(avg_buyer_rating) AS mean_rating
FROM `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
GROUP BY 1;
```

#### 2025-07-15 08:40:12 UTC
* **User:** `connor.blake` (assoc_100212)
* **Job ID:** `bq_job_9999990334_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 13,000,000 bytes
* **Duration:** 0.20s
* **Query Text:**
```sql
-- Checking dim_marketing_calendar planned vs actual spend
SUM(planned_spend_usd) AS planned, SUM(actual_spend_usd) AS actual
FROM `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`;
```

#### 2025-07-15 11:15:55 UTC
* **User:** `giulia.romano` (assoc_100213)
* **Job ID:** `bq_job_9999990335_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 48,000,000 bytes
* **Duration:** 0.62s
* **Query Text:**
```sql
-- Checking fact_care_contacts handle time by channel
channel, AVG(handle_time_minutes) AS mean_handle_time
FROM `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
GROUP BY 1;
```

#### 2025-07-16 09:12:00 UTC
* **User:** `wei.hartono` (assoc_100210)
* **Job ID:** `bq_job_9999990336_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 86,000,000 bytes
* **Duration:** 1.07s
* **Query Text:**
```sql
-- Checking fact_promise_vs_actual avg days late when late
fulfillment_type, AVG(avg_days_late_when_late) AS mean_days_late
FROM `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
GROUP BY 1;
```

#### 2025-07-16 15:05:40 UTC
* **User:** `amara.shah` (assoc_100211)
* **Job ID:** `bq_job_9999990337_q1fy26`
* **Query Type:** `SELECT`
* **Bytes Billed:** 122,000,000 bytes
* **Duration:** 1.52s
* **Query Text:**
```sql
-- Checking fact_orders gmv by market and vertical
market, vertical_code, SUM(gmv_usd) AS total_gmv
FROM `nexus-analyst-demo.acme_ecomm.fact_orders`
GROUP BY 1, 2;
```