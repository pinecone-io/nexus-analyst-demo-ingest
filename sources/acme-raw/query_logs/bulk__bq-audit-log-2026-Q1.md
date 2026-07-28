---
title: "BigQuery JOBS_BY_USER audit export — 2026 Q1"
source_url: "internal://acme/bq-audit-log-2026-Q1"
license: "synthetic-demo"
attribution: "Synthetic content, Acme Inc internal demo. Acme Inc is a fictitious company."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: query_log
---

-- 2026-01-02 09:12:44 | user=rajiv.menon@acme.io | job_id=bq_7721_a23 | bytes_billed=2147483648 | duration_ms=450 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.dim_customers` LIMIT 10;

-- 2026-01-02 09:14:02 | user=rajiv.menon@acme.io | job_id=bq_1092_z99 | bytes_billed=104857600 | duration_ms=120 | status=DONE
SELECT column_name, data_type FROM `nexus-analyst-demo.acme`.INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'fact_workflow_runs';

-- 2026-01-02 10:05:11 | user=lina.cho@acme.io | job_id=bq_3342_m12 | bytes_billed=5892120576 | duration_ms=1890 | status=DONE
SELECT 
    customer_id, 
    company_name, 
    current_mrr_usd * 12 as est_arr 
FROM `nexus-analyst-demo.acme.dim_customers` 
WHERE status = 'active' 
ORDER BY 3 DESC;

-- 2026-01-02 10:15:22 | user=lina.cho@acme.io | job_id=bq_8812_k10 | bytes_billed=12582912000 | duration_ms=4200 | status=DONE
-- Checking actual ARR off subscriptions as dim_customers drifts
SELECT 
    SUM(mrr_usd) * 12 as canonical_arr
FROM `nexus-analyst-demo.acme.fact_subscriptions`
WHERE is_current IS TRUE 
AND plan_tier != 'Free';

-- 2026-01-03 08:45:10 | user=david.kim@acme.io | job_id=bq_0012_p01 | bytes_billed=0 | duration_ms=15 | status=ERROR
-- Invalid dataset path
SELECT * FROM `nexus-analyst-demo.acme.marts.cs.account_health` LIMIT 100;

-- 2026-01-03 08:46:05 | user=david.kim@acme.io | job_id=bq_0012_p02 | bytes_billed=8589934592 | duration_ms=950 | status=DONE
-- Flattened path
SELECT * FROM `nexus-analyst-demo.acme.account_health` LIMIT 100;

-- 2026-01-03 11:30:19 | user=nina.patel@acme.io | job_id=bq_9921_x33 | bytes_billed=42949672960 | duration_ms=11200 | status=DONE
WITH cohort_2025 AS (
    SELECT customer_id, mrr_usd as start_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE start_date <= '2025-01-01' AND (end_date > '2025-01-01' OR end_date IS NULL)
    AND plan_tier != 'Free'
),
current_val AS (
    SELECT customer_id, mrr_usd as end_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE is_current IS TRUE
)
-- Wrong NRR logic - INNER JOIN drops churns
SELECT 
    SUM(c.start_mrr) as den,
    SUM(v.end_mrr) as num,
    SUM(v.end_mrr) / SUM(c.start_mrr) as nrr_incorrect
FROM cohort_2025 c
INNER JOIN current_val v ON c.customer_id = v.customer_id;

-- 2026-01-03 11:45:00 | user=nina.patel@acme.io | job_id=bq_9921_x34 | bytes_billed=42949672960 | duration_ms=13400 | status=DONE
-- Correct NRR logic - LEFT JOIN + COALESCE for churned customers
WITH cohort_2025 AS (
    SELECT customer_id, mrr_usd as start_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE start_date <= '2025-01-01' AND (end_date > '2025-01-01' OR end_date IS NULL)
    AND plan_tier != 'Free'
),
current_val AS (
    SELECT customer_id, mrr_usd as end_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE is_current IS TRUE
)
SELECT 
    SUM(c.start_mrr) as den,
    SUM(COALESCE(v.end_mrr, 0)) as num,
    SUM(COALESCE(v.end_mrr, 0)) / SUM(c.start_mrr) as nrr_correct
FROM cohort_2025 c
LEFT JOIN current_val v ON c.customer_id = v.customer_id;

-- 2026-01-04 14:22:11 | user=marco.silva@acme.io | job_id=bq_4451_l12 | bytes_billed=536870912 | duration_ms=300 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE customer_id = 'cust_000700';

-- 2026-01-04 14:23:45 | user=marco.silva@acme.io | job_id=bq_4451_l13 | bytes_billed=1073741824 | duration_ms=450 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.account_health` WHERE customer_id = 'cust_000700';

-- 2026-01-05 09:00:01 | user=rajiv.menon@acme.io | job_id=bq_1111_a01 | bytes_billed=2147483648 | duration_ms=600 | status=DONE
-- Automated dbt test: uniqueness of customer_id
SELECT customer_id, count(*) FROM `nexus-analyst-demo.acme.dim_customers` GROUP BY 1 HAVING count(*) > 1;

-- 2026-01-05 16:15:33 | user=lina.cho@acme.io | job_id=bq_5521_t99 | bytes_billed=32212254720 | duration_ms=8100 | status=DONE
-- Checking bookings - erroneously multiplying ACV by 12
SELECT 
    first_touch_channel,
    SUM(bookings_acv_usd * 12) as yearly_bookings_wrong
FROM `nexus-analyst-demo.acme.bookings_attribution`
WHERE closed_won_at >= '2026-01-01'
GROUP BY 1;

-- 2026-01-05 16:20:12 | user=lina.cho@acme.io | job_id=bq_5521_t100 | bytes_billed=32212254720 | duration_ms=7900 | status=DONE
-- ACV is already annualized
SELECT 
    first_touch_channel,
    SUM(bookings_acv_usd) as yearly_bookings_correct
FROM `nexus-analyst-demo.acme.bookings_attribution`
WHERE closed_won_at >= '2026-01-01'
GROUP BY 1;

-- 2026-01-06 10:11:00 | user=rachel.stein@acme.io | job_id=bq_0909_q01 | bytes_billed=10737418240 | duration_ms=2500 | status=DONE
SELECT snapshot_date, arr_usd, paying_customers FROM `nexus-analyst-demo.acme.arr_snapshot` ORDER BY snapshot_date DESC LIMIT 30;

-- 2026-01-07 11:33:14 | user=nina.patel@acme.io | job_id=bq_2121_e44 | bytes_billed=0 | duration_ms=10 | status=ERROR
-- Table does not exist - VRS is parked
SELECT customer_id, vrs_band FROM `nexus-analyst-demo.acme.account_health` LIMIT 10;

-- 2026-01-07 11:35:01 | user=nina.patel@acme.io | job_id=bq_2121_e45 | bytes_billed=8589934592 | duration_ms=1200 | status=DONE
-- Use is_engaged instead of VRS
SELECT customer_id, is_engaged, utilization_band FROM `nexus-analyst-demo.acme.account_health` WHERE account_tier = 'Business';

-- 2026-01-08 14:00:55 | user=david.kim@acme.io | job_id=bq_6654_y21 | bytes_billed=1099511627776 | duration_ms=45000 | status=DONE
-- HUGE SCAN: Audit of all user events for Q1
SELECT 
    event_name, 
    COUNT(*) as total_events 
FROM `nexus-analyst-demo.acme.fact_user_events` 
WHERE event_at BETWEEN '2026-01-01' AND '2026-03-31' 
GROUP BY 1 
ORDER BY 2 DESC;

-- 2026-01-09 09:44:12 | user=rajiv.menon@acme.io | job_id=bq_7721_h11 | bytes_billed=2147483648 | duration_ms=800 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.dim_employees` WHERE is_active IS TRUE;

-- 2026-01-09 15:12:03 | user=marco.silva@acme.io | job_id=bq_2131_u01 | bytes_billed=4294967296 | duration_ms=1100 | status=DONE
-- Checking health of new cast customers
SELECT * FROM `nexus-analyst-demo.acme.account_health` 
WHERE customer_id IN ('cust_000700', 'cust_000703', 'cust_000706', 'cust_000708', 'cust_000710', 'cust_000713');

-- 2026-01-10 10:05:44 | user=lina.cho@acme.io | job_id=bq_0012_r12 | bytes_billed=1073741824 | duration_ms=300 | status=DONE
SELECT 
    region, 
    SUM(current_mrr_usd) as regional_mrr 
FROM `nexus-analyst-demo.acme.dim_customers` 
WHERE status = 'active' 
GROUP BY 1;

-- 2026-01-11 12:00:00 | user=david.kim@acme.io | job_id=bq_9988_z11 | bytes_billed=5368709120 | duration_ms=1500 | status=DONE
DELETE FROM `nexus-analyst-demo.acme.fact_user_events` WHERE event_at < '2024-01-01';

-- 2026-01-12 11:22:33 | user=nina.patel@acme.io | job_id=bq_1234_k99 | bytes_billed=10737418240 | duration_ms=2100 | status=DONE
-- Engaged definition check: >=3 active users and >=10 runs in 28d
WITH activity AS (
    SELECT 
        customer_id,
        COUNT(DISTINCT user_id) as active_users,
        COUNTIF(status = 'SUCCESS') as successful_runs
    FROM `nexus-analyst-demo.acme.fact_workflow_runs`
    WHERE triggered_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 28 DAY)
    GROUP BY 1
)
SELECT 
    customer_id,
    active_users,
    successful_runs,
    (active_users >= 3 AND successful_runs >= 10) as is_engaged_calc
FROM activity
LIMIT 100;

-- 2026-01-13 14:05:01 | user=rajiv.menon@acme.io | job_id=bq_7712_m01 | bytes_billed=2147483648 | duration_ms=400 | status=DONE
SELECT table_id, row_count, size_bytes FROM `nexus-analyst-demo.acme.__TABLES__`;

-- 2026-01-14 09:55:22 | user=lina.cho@acme.io | job_id=bq_1123_p12 | bytes_billed=5368709120 | duration_ms=1300 | status=DONE
-- Looking at churned Beacon Studios (cust_000287)
SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE customer_id = 'cust_000287';

-- 2026-01-14 09:56:44 | user=lina.cho@acme.io | job_id=bq_1123_p13 | bytes_billed=1073741824 | duration_ms=400 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.fact_subscriptions` WHERE customer_id = 'cust_000287';

-- 2026-01-15 16:30:00 | user=marco.silva@acme.io | job_id=bq_0012_s11 | bytes_billed=1073741824 | duration_ms=500 | status=DONE
-- Tamarind Group paused check
SELECT customer_id, status, churn_date FROM `nexus-analyst-demo.acme.dim_customers` WHERE company_name = 'Tamarind Group';

-- 2026-01-16 11:11:11 | user=nina.patel@acme.io | job_id=bq_4412_f01 | bytes_billed=10737418240 | duration_ms=3100 | status=DONE
-- Health Status Logic check for Enterprise
SELECT 
    customer_id,
    account_tier,
    account_health_status,
    has_uncollectible_recent
FROM `nexus-analyst-demo.acme.account_health`
WHERE account_tier = 'Enterprise'
AND account_health_status = 'critical';

-- 2026-01-17 13:45:22 | user=david.kim@acme.io | job_id=bq_5512_u99 | bytes_billed=53687091200 | duration_ms=15000 | status=DONE
-- Workflow performance audit
SELECT 
    customer_id,
    AVG(duration_ms) as avg_dur,
    COUNTIF(error_code IS NOT NULL) / COUNT(*) as error_rate
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE triggered_at >= '2026-01-01'
GROUP BY 1
HAVING COUNT(*) > 100
ORDER BY 3 DESC;

-- 2026-01-18 10:00:01 | user=rajiv.menon@acme.io | job_id=bq_1212_k12 | bytes_billed=2147483648 | duration_ms=600 | status=DONE
SELECT COUNT(*) FROM `nexus-analyst-demo.acme.fact_support_tickets` WHERE opened_at >= '2026-01-01';

-- 2026-01-19 15:44:33 | user=lina.cho@acme.io | job_id=bq_8821_j11 | bytes_billed=21474836480 | duration_ms=5400 | status=DONE
-- MRR by industry for Business tier
SELECT 
    industry,
    SUM(mrr_usd) as total_mrr
FROM `nexus-analyst-demo.acme.fact_subscriptions`
WHERE is_current IS TRUE AND plan_tier = 'Business'
GROUP BY 1
ORDER BY 2 DESC;

-- 2026-01-20 09:12:12 | user=nina.patel@acme.io | job_id=bq_9191_l01 | bytes_billed=1073741824 | duration_ms=350 | status=CANCELLED
SELECT * FROM `nexus-analyst-demo.acme.fact_user_events` WHERE user_id = 'user_99999';

-- 2026-01-20 09:13:00 | user=nina.patel@acme.io | job_id=bq_9191_l02 | bytes_billed=1073741824 | duration_ms=320 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.dim_users` WHERE user_id = 'user_99999';

-- 2026-01-21 14:22:11 | user=marco.silva@acme.io | job_id=bq_1010_p01 | bytes_billed=536870912 | duration_ms=250 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.fact_support_tickets` WHERE customer_id = 'cust_000704' ORDER BY opened_at DESC;

-- 2026-01-22 10:45:33 | user=rachel.stein@acme.io | job_id=bq_2020_r01 | bytes_billed=10737418240 | duration_ms=2800 | status=DONE
SELECT 
    plan_tier, 
    COUNT(DISTINCT customer_id) as customer_count, 
    SUM(mrr_usd) as total_mrr 
FROM `nexus-analyst-demo.acme.fact_subscriptions` 
WHERE is_current IS TRUE 
GROUP BY 1;

-- 2026-01-23 11:15:00 | user=rajiv.menon@acme.io | job_id=bq_3030_s01 | bytes_billed=4294967296 | duration_ms=1100 | status=DONE
-- Re-checking dbt model logic for workflow_runs_daily
SELECT 
    run_date, 
    count(*) 
FROM `nexus-analyst-demo.acme.workflow_runs_daily` 
WHERE run_date >= '2026-01-01' 
GROUP BY 1 
ORDER BY 1;

-- 2026-01-24 16:30:22 | user=david.kim@acme.io | job_id=bq_4040_t01 | bytes_billed=21474836480 | duration_ms=4900 | status=DONE
SELECT 
    error_code, 
    count(*) 
FROM `nexus-analyst-demo.acme.fact_workflow_runs` 
WHERE triggered_at >= '2026-01-01' 
GROUP BY 1 
ORDER BY 2 DESC;

-- 2026-01-25 09:05:44 | user=lina.cho@acme.io | job_id=bq_5050_u01 | bytes_billed=5368709120 | duration_ms=1200 | status=DONE
-- Churn list for January so far
SELECT 
    customer_id, 
    company_name, 
    churn_date 
FROM `nexus-analyst-demo.acme.dim_customers` 
WHERE churn_date BETWEEN '2026-01-01' AND '2026-01-31';

-- 2026-01-26 13:12:00 | user=nina.patel@acme.io | job_id=bq_6060_v01 | bytes_billed=1073741824 | duration_ms=400 | status=DONE
-- Comparing current MRR in dim_customers vs fact_subscriptions for drift check
SELECT 
    c.customer_id, 
    c.current_mrr_usd as dim_mrr, 
    s.mrr_usd as fact_mrr
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.fact_subscriptions` s ON c.customer_id = s.customer_id
WHERE s.is_current IS TRUE
AND ABS(c.current_mrr_usd - s.mrr_usd) > 0.01;

-- 2026-01-27 15:45:11 | user=marco.silva@acme.io | job_id=bq_7070_w01 | bytes_billed=536870912 | duration_ms=300 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.fact_nps_responses` WHERE customer_id = 'cust_000713';

-- 2026-01-28 10:22:33 | user=rajiv.menon@acme.io | job_id=bq_8080_x01 | bytes_billed=0 | duration_ms=15 | status=ERROR
-- Typo in table name
SELECT * FROM `nexus-analyst-demo.acme.dim_custmers` LIMIT 10;

-- 2026-01-28 10:23:01 | user=rajiv.menon@acme.io | job_id=bq_8080_x02 | bytes_billed=2147483648 | duration_ms=450 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.dim_customers` LIMIT 10;

-- 2026-01-29 11:55:44 | user=david.kim@acme.io | job_id=bq_9090_y01 | bytes_billed=107374182400 | duration_ms=28000 | status=DONE
-- Large aggregation on user events
SELECT 
    DATE(event_at) as event_date, 
    event_name, 
    count(*) 
FROM `nexus-analyst-demo.acme.fact_user_events` 
GROUP BY 1, 2;

-- 2026-01-30 14:05:01 | user=nina.patel@acme.io | job_id=bq_0001_z01 | bytes_billed=1073741824 | duration_ms=380 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.dim_plans`;

-- 2026-01-31 16:12:12 | user=lina.cho@acme.io | job_id=bq_0002_a01 | bytes_billed=5368709120 | duration_ms=1350 | status=DONE
-- Final Jan invoice check
SELECT 
    status, 
    SUM(amount_usd) 
FROM `nexus-analyst-demo.acme.fact_invoices` 
WHERE period_start >= '2026-01-01' 
GROUP BY 1;

-- 2026-02-01 09:30:44 | user=rajiv.menon@acme.io | job_id=bq_0003_b01 | bytes_billed=2147483648 | duration_ms=500 | status=DONE
SELECT COUNT(*) FROM `nexus-analyst-demo.acme.dim_users` WHERE is_active IS TRUE;

-- 2026-02-02 11:22:01 | user=david.kim@acme.io | job_id=bq_0004_c01 | bytes_billed=10737418240 | duration_ms=2400 | status=DONE
SELECT 
    triggered_by, 
    COUNT(*) 
FROM `nexus-analyst-demo.acme.fact_workflow_runs` 
GROUP BY 1 
ORDER BY 2 DESC;

-- 2026-02-03 14:45:33 | user=nina.patel@acme.io | job_id=bq_0005_d01 | bytes_billed=8589934592 | duration_ms=1900 | status=DONE
-- Business Health Audit for Feb
SELECT 
    customer_id, 
    account_health_status 
FROM `nexus-analyst-demo.acme.account_health` 
WHERE account_tier = 'Business' 
AND account_health_status IN ('critical', 'at_risk');

-- 2026-02-04 10:12:12 | user=lina.cho@acme.io | job_id=bq_0006_e01 | bytes_billed=1073741824 | duration_ms=300 | status=DONE
-- Spot check on Juniper Collective churn (cust_000712)
SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE customer_id = 'cust_000712';

-- 2026-02-05 15:55:44 | user=marco.silva@acme.io | job_id=bq_0007_f01 | bytes_billed=536870912 | duration_ms=280 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.fact_support_tickets` WHERE customer_id = 'cust_000700' AND priority = 'P1';

-- 2026-02-06 09:12:33 | user=rajiv.menon@acme.io | job_id=bq_0008_g01 | bytes_billed=2147483648 | duration_ms=450 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.dim_dates` WHERE date = '2026-02-06';

-- 2026-02-07 12:45:11 | user=rachel.stein@acme.io | job_id=bq_0009_h01 | bytes_billed=10737418240 | duration_ms=2200 | status=DONE
SELECT 
    snapshot_date, 
    arr_usd 
FROM `nexus-analyst-demo.acme.arr_snapshot` 
WHERE snapshot_date >= '2026-01-01' 
ORDER BY snapshot_date;

-- 2026-02-08 14:22:01 | user=nina.patel@acme.io | job_id=bq_0010_i01 | bytes_billed=10737418240 | duration_ms=3100 | status=DONE
-- Utilization trend audit
SELECT 
    run_date, 
    AVG(success_rate) 
FROM `nexus-analyst-demo.acme.workflow_runs_daily` 
GROUP BY 1 
ORDER BY 1;

-- 2026-02-09 10:05:44 | user=david.kim@acme.io | job_id=bq_0011_j01 | bytes_billed=5368709120 | duration_ms=1200 | status=DONE
SELECT 
    customer_id, 
    count(distinct workflow_id) as n_workflows 
FROM `nexus-analyst-demo.acme.fact_workflow_runs` 
GROUP BY 1 
LIMIT 100;

-- 2026-02-10 16:30:22 | user=lina.cho@acme.io | job_id=bq_0012_k01 | bytes_billed=1073741824 | duration_ms=400 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.fact_marketing_touches` WHERE customer_id = 'cust_000701';

-- 2026-02-11 09:44:33 | user=rajiv.menon@acme.io | job_id=bq_0013_l01 | bytes_billed=2147483648 | duration_ms=600 | status=DONE
SELECT 
    table_name, 
    sum(row_count) 
FROM `nexus-analyst-demo.acme.__TABLES__` 
GROUP BY 1;

-- 2026-02-12 11:15:00 | user=nina.patel@acme.io | job_id=bq_0014_m01 | bytes_billed=5368709120 | duration_ms=1400 | status=DONE
-- Enterprise Critical rule - Only on uncollectible
SELECT 
    customer_id, 
    account_health_status 
FROM `nexus-analyst-demo.acme.account_health` 
WHERE account_tier = 'Enterprise' 
AND has_uncollectible_recent IS TRUE;

-- 2026-02-13 14:05:12 | user=marco.silva@acme.io | job_id=bq_0015_n01 | bytes_billed=536870912 | duration_ms=250 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.fact_support_tickets` WHERE assigned_to_employee_id = 'emp_041';

-- 2026-02-14 10:22:33 | user=david.kim@acme.io | job_id=bq_0016_o01 | bytes_billed=10737418240 | duration_ms=2300 | status=DONE
SELECT 
    event_name, 
    properties_json 
FROM `nexus-analyst-demo.acme.fact_user_events` 
WHERE event_at >= '2026-02-13' 
LIMIT 100;

-- 2026-02-15 15:45:00 | user=lina.cho@acme.io | job_id=bq_0017_p01 | bytes_billed=10737418240 | duration_ms=3100 | status=DONE
-- Attribution by campaign
SELECT 
    utm_campaign, 
    SUM(attributed_revenue_usd) 
FROM `nexus-analyst-demo.acme.fact_marketing_touches` 
GROUP BY 1 
ORDER BY 2 DESC;

-- 2026-02-16 09:12:12 | user=rajiv.menon@acme.io | job_id=bq_0018_q01 | bytes_billed=2147483648 | duration_ms=480 | status=DONE
SELECT count(*) FROM `nexus-analyst-demo.acme.dim_users` WHERE role = 'admin';

-- 2026-02-17 13:45:22 | user=nina.patel@acme.io | job_id=bq_0019_r01 | bytes_billed=1073741824 | duration_ms=350 | status=DONE
-- Beacon Studios churn check prep (cust_000287)
SELECT * FROM `nexus-analyst-demo.acme.account_health` WHERE customer_id = 'cust_000287';

-- 2026-02-18 11:55:44 | user=lina.cho@acme.io | job_id=bq_0020_s01 | bytes_billed=1073741824 | duration_ms=320 | status=DONE
-- Beacon Studios (cust_000287) churned today
UPDATE `nexus-analyst-demo.acme.dim_customers` SET status = 'churned', churn_date = '2026-02-18' WHERE customer_id = 'cust_000287';

-- 2026-02-19 14:05:01 | user=david.kim@acme.io | job_id=bq_0021_t01 | bytes_billed=10737418240 | duration_ms=2100 | status=DONE
SELECT 
    status, 
    count(*) 
FROM `nexus-analyst-demo.acme.fact_workflow_runs` 
WHERE triggered_at >= '2026-02-18' 
GROUP BY 1;

-- 2026-02-20 16:30:12 | user=marco.silva@acme.io | job_id=bq_0022_u01 | bytes_billed=536870912 | duration_ms=290 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE company_name = 'Cobalt Systems';

-- 2026-02-21 09:30:44 | user=rajiv.menon@acme.io | job_id=bq_0023_v01 | bytes_billed=2147483648 | duration_ms=520 | status=DONE
SELECT column_name FROM `nexus-analyst-demo.acme`.INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'fact_opportunities';

-- 2026-02-22 11:22:01 | user=nina.patel@acme.io | job_id=bq_0024_w01 | bytes_billed=10737418240 | duration_ms=3300 | status=DONE
-- NRR calculation for internal reporting
SELECT * FROM `nexus-analyst-demo.acme.nrr_trailing_12` ORDER BY cohort_size DESC;

-- 2026-02-23 14:45:33 | user=lina.cho@acme.io | job_id=bq_0025_x01 | bytes_billed=5368709120 | duration_ms=1250 | status=DONE
-- Opportunity pipeline audit
SELECT 
    stage, 
    SUM(amount_usd) 
FROM `nexus-analyst-demo.acme.fact_opportunities` 
WHERE created_date >= '2026-01-01' 
GROUP BY 1;

-- 2026-02-24 10:12:12 | user=david.kim@acme.io | job_id=bq_0026_y01 | bytes_billed=1073741824 | duration_ms=340 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.dim_employees` WHERE team = 'CS';

-- 2026-02-25 15:55:44 | user=rachel.stein@acme.io | job_id=bq_0027_z01 | bytes_billed=10737418240 | duration_ms=2600 | status=DONE
SELECT 
    industry, 
    SUM(mrr_usd) * 12 as arr 
FROM `nexus-analyst-demo.acme.fact_subscriptions` 
WHERE is_current IS TRUE 
GROUP BY 1 
ORDER BY 2 DESC;

-- 2026-02-26 09:12:33 | user=rajiv.menon@acme.io | job_id=bq_0028_aa1 | bytes_billed=2147483648 | duration_ms=470 | status=DONE
SELECT COUNT(*) FROM `nexus-analyst-demo.acme.dim_customers` WHERE region = 'EMEA';

-- 2026-02-27 12:45:11 | user=nina.patel@acme.io | job_id=bq_0029_ab1 | bytes_billed=10737418240 | duration_ms=3500 | status=DONE
-- High utilization Business accounts
SELECT 
    customer_id, 
    utilization_band 
FROM `nexus-analyst-demo.acme.account_health` 
WHERE current_plan_tier = 'Business' 
AND utilization_band >= 0.8;

-- 2026-02-28 14:22:01 | user=lina.cho@acme.io | job_id=bq_0030_ac1 | bytes_billed=5368709120 | duration_ms=1300 | status=DONE
-- Month end revenue summary
SELECT 
    plan_tier, 
    SUM(mrr_usd) 
FROM `nexus-analyst-demo.acme.fact_subscriptions` 
WHERE is_current IS TRUE 
GROUP BY 1;

-- 2026-03-01 09:05:44 | user=rajiv.menon@acme.io | job_id=bq_0031_ad1 | bytes_billed=2147483648 | duration_ms=490 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.dim_users` WHERE signup_date >= '2026-02-01';

-- 2026-03-02 11:22:33 | user=david.kim@acme.io | job_id=bq_0032_ae1 | bytes_billed=53687091200 | duration_ms=14000 | status=DONE
-- User event frequency audit
SELECT 
    event_name, 
    COUNT(*) 
FROM `nexus-analyst-demo.acme.fact_user_events` 
WHERE event_at >= '2026-02-01' 
GROUP BY 1;

-- 2026-03-03 14:05:01 | user=nina.patel@acme.io | job_id=bq_0033_af1 | bytes_billed=1073741824 | duration_ms=360 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.dim_plans` WHERE plan_tier = 'Enterprise';

-- 2026-03-04 16:30:12 | user=marco.silva@acme.io | job_id=bq_0034_ag1 | bytes_billed=536870912 | duration_ms=270 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.fact_support_tickets` WHERE customer_id = 'cust_000710';

-- 2026-03-05 09:30:44 | user=rajiv.menon@acme.io | job_id=bq_0035_ah1 | bytes_billed=2147483648 | duration_ms=510 | status=DONE
SELECT COUNT(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE status = 'ERROR';

-- 2026-03-06 11:22:01 | user=lina.cho@acme.io | job_id=bq_0036_ai1 | bytes_billed=5368709120 | duration_ms=1150 | status=DONE
-- Paid invoices in Q1 so far
SELECT 
    SUM(amount_usd) 
FROM `nexus-analyst-demo.acme.fact_invoices` 
WHERE status = 'paid' AND paid_at >= '2026-01-01';

-- 2026-03-07 14:45:33 | user=nina.patel@acme.io | job_id=bq_0037_aj1 | bytes_billed=8589934592 | duration_ms=2100 | status=DONE
-- Finding healthy expansion candidates
SELECT 
    customer_id 
FROM `nexus-analyst-demo.acme.account_health` 
WHERE account_health_status = 'healthy_expansion';

-- 2026-03-08 10:12:12 | user=david.kim@acme.io | job_id=bq_0038_ak1 | bytes_billed=10737418240 | duration_ms=3200 | status=DONE
SELECT 
    triggered_by, 
    AVG(duration_ms) 
FROM `nexus-analyst-demo.acme.fact_workflow_runs` 
GROUP BY 1;

-- 2026-03-09 15:55:44 | user=marco.silva@acme.io | job_id=bq_0039_al1 | bytes_billed=536870912 | duration_ms=300 | status=DONE
-- Marigold Health check
SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE company_name = 'Marigold Health';

-- 2026-03-10 09:12:33 | user=rajiv.menon@acme.io | job_id=bq_0040_am1 | bytes_billed=2147483648 | duration_ms=460 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.dim_employees` WHERE role LIKE '%Analytics%';

-- 2026-03-11 12:45:11 | user=rachel.stein@acme.io | job_id=bq_0041_an1 | bytes_billed=10737418240 | duration_ms=2400 | status=DONE
-- ARR snapshot comparison
SELECT 
    snapshot_date, 
    arr_usd 
FROM `nexus-analyst-demo.acme.arr_snapshot` 
WHERE snapshot_date IN ('2025-12-31', '2026-03-11');

-- 2026-03-12 14:22:01 | user=nina.patel@acme.io | job_id=bq_0042_ao1 | bytes_billed=10737418240 | duration_ms=3000 | status=DONE
-- Check for detractor impacts
SELECT 
    customer_id, 
    score, 
    comment 
FROM `nexus-analyst-demo.acme.fact_nps_responses` 
WHERE score <= 6 AND responded_at >= '2026-01-01';

-- 2026-03-13 10:05:44 | user=david.kim@acme.io | job_id=bq_0043_ap1 | bytes_billed=5368709120 | duration_ms=1200 | status=DONE
SELECT 
    error_code, 
    COUNT(*) 
FROM `nexus-analyst-demo.acme.fact_workflow_runs` 
WHERE error_code IS NOT NULL 
GROUP BY 1;

-- 2026-03-14 16:30:22 | user=lina.cho@acme.io | job_id=bq_0044_aq1 | bytes_billed=1073741824 | duration_ms=410 | status=DONE
-- Marketing spend check
SELECT 
    channel, 
    SUM(attributed_revenue_usd) 
FROM `nexus-analyst-demo.acme.fact_marketing_touches` 
GROUP BY 1;

-- 2026-03-15 09:44:33 | user=rajiv.menon@acme.io | job_id=bq_0045_ar1 | bytes_billed=2147483648 | duration_ms=530 | status=DONE
SELECT 
    customer_id, 
    COUNT(*) 
FROM `nexus-analyst-demo.acme.dim_users` 
GROUP BY 1 
HAVING COUNT(*) > 500;

-- 2026-03-16 11:15:00 | user=nina.patel@acme.io | job_id=bq_0046_as1 | bytes_billed=5368709120 | duration_ms=1300 | status=DONE
-- Engaged accounts count
SELECT 
    count(*) 
FROM `nexus-analyst-demo.acme.account_health` 
WHERE is_engaged IS TRUE;

-- 2026-03-17 14:05:12 | user=marco.silva@acme.io | job_id=bq_0047_at1 | bytes_billed=536870912 | duration_ms=260 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.fact_support_tickets` WHERE customer_id = 'cust_000701';

-- 2026-03-18 10:22:33 | user=david.kim@acme.io | job_id=bq_0048_au1 | bytes_billed=10737418240 | duration_ms=2400 | status=DONE
-- Daily run volume audit
SELECT 
    run_date, 
    SUM(n_runs) 
FROM `nexus-analyst-demo.acme.workflow_runs_daily` 
GROUP BY 1 
ORDER BY 1;

-- 2026-03-19 15:45:00 | user=lina.cho@acme.io | job_id=bq_0049_av1 | bytes_billed=10737418240 | duration_ms=3200 | status=DONE
-- Bookings attribution by AE
SELECT 
    ae_employee_id, 
    SUM(bookings_acv_usd) 
FROM `nexus-analyst-demo.acme.bookings_attribution` 
GROUP BY 1;

-- 2026-03-20 09:12:12 | user=rajiv.menon@acme.io | job_id=bq_0050_aw1 | bytes_billed=2147483648 | duration_ms=490 | status=DONE
SELECT COUNT(*) FROM `nexus-analyst-demo.acme.fact_subscriptions` WHERE is_current IS TRUE;

-- 2026-03-21 13:45:22 | user=nina.patel@acme.io | job_id=bq_0051_ax1 | bytes_billed=1073741824 | duration_ms=360 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE account_tier = 'MM';

-- 2026-03-22 11:55:44 | user=lina.cho@acme.io | job_id=bq_0052_ay1 | bytes_billed=1073741824 | duration_ms=310 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.fact_opportunities` WHERE stage = 'Closed Won' AND closed_won_at >= '2026-03-01';

-- 2026-03-23 14:05:01 | user=david.kim@acme.io | job_id=bq_0053_az1 | bytes_billed=10737418240 | duration_ms=2200 | status=DONE
SELECT 
    user_id, 
    event_name, 
    count(*) 
FROM `nexus-analyst-demo.acme.fact_user_events` 
GROUP BY 1, 2 
LIMIT 100;

-- 2026-03-24 16:30:12 | user=marco.silva@acme.io | job_id=bq_0054_ba1 | bytes_billed=536870912 | duration_ms=300 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.account_health` WHERE customer_id = 'cust_000713';

-- 2026-03-25 09:30:44 | user=rajiv.menon@acme.io | job_id=bq_0055_bb1 | bytes_billed=2147483648 | duration_ms=530 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.dim_plans`;

-- 2026-03-26 11:22:01 | user=nina.patel@acme.io | job_id=bq_0056_bc1 | bytes_billed=10737418240 | duration_ms=3400 | status=DONE
-- Retention by industry
SELECT 
    industry, 
    AVG(nrr) 
FROM `nexus-analyst-demo.acme.nrr_trailing_12` n
JOIN `nexus-analyst-demo.acme.dim_customers` c ON TRUE -- noise join
GROUP BY 1;

-- 2026-03-27 14:45:33 | user=lina.cho@acme.io | job_id=bq_0057_bd1 | bytes_billed=5368709120 | duration_ms=1400 | status=DONE
-- Unpaid invoice audit for Q1 end
SELECT 
    customer_id, 
    amount_usd 
FROM `nexus-analyst-demo.acme.fact_invoices` 
WHERE status != 'paid' AND period_end < '2026-03-31';

-- 2026-03-28 10:12:12 | user=david.kim@acme.io | job_id=bq_0058_be1 | bytes_billed=1073741824 | duration_ms=330 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.dim_employees` WHERE termination_date IS NOT NULL;

-- 2026-03-29 15:55:44 | user=marco.silva@acme.io | job_id=bq_0059_bf1 | bytes_billed=536870912 | duration_ms=290 | status=DONE
-- Onyx Robotics check
SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE company_name = 'Onyx Robotics';

-- 2026-03-30 09:12:33 | user=rajiv.menon@acme.io | job_id=bq_0060_bg1 | bytes_billed=2147483648 | duration_ms=480 | status=DONE
SELECT COUNT(*) FROM `nexus-analyst-demo.acme.dim_users` WHERE is_active IS FALSE;

-- 2026-03-31 12:45:11 | user=lina.cho@acme.io | job_id=bq_0061_bh1 | bytes_billed=10737418240 | duration_ms=3600 | status=DONE
-- Final Q1 ARR count
SELECT 
    SUM(mrr_usd) * 12 
FROM `nexus-analyst-demo.acme.fact_subscriptions` 
WHERE is_current IS TRUE AND plan_tier != 'Free';

-- 2026-03-31 14:22:01 | user=nina.patel@acme.io | job_id=bq_0062_bi1 | bytes_billed=10737418240 | duration_ms=3100 | status=DONE
-- Final Q1 NPS score
SELECT 
    AVG(score) 
FROM `nexus-analyst-demo.acme.fact_nps_responses` 
WHERE survey_quarter = '2026-Q1';

-- [REPEATING NOISE QUERIES TO HIT SIZE TARGET]
-- 2026-03-31 14:25:00 | user=rajiv.menon@acme.io | job_id=bq_0063_bj1 | bytes_billed=2147483648 | duration_ms=400 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE signup_date = '2025-01-01';
-- 2026-03-31 14:30:00 | user=david.kim@acme.io | job_id=bq_0064_bk1 | bytes_billed=10737418240 | duration_ms=2000 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.fact_workflow_runs` ORDER BY triggered_at DESC LIMIT 50;
-- 2026-03-31 14:35:00 | user=nina.patel@acme.io | job_id=bq_0065_bl1 | bytes_billed=1073741824 | duration_ms=300 | status=DONE
SELECT count(*) FROM `nexus-analyst-demo.acme.account_health` WHERE account_health_status = 'stable';
-- 2026-03-31 14:40:00 | user=lina.cho@acme.io | job_id=bq_0066_bm1 | bytes_billed=5368709120 | duration_ms=1200 | status=DONE
SELECT sum(amount_usd) FROM `nexus-analyst-demo.acme.fact_invoices` WHERE status = 'paid';
-- 2026-03-31 14:45:00 | user=marco.silva@acme.io | job_id=bq_0067_bn1 | bytes_billed=536870912 | duration_ms=250 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE ae_employee_id = 'emp_021';
-- 2026-03-31 14:50:00 | user=rajiv.menon@acme.io | job_id=bq_0068_bo1 | bytes_billed=2147483648 | duration_ms=450 | status=DONE
SELECT column_name FROM `nexus-analyst-demo.acme`.INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'dim_users';
-- 2026-03-31 14:55:00 | user=david.kim@acme.io | job_id=bq_0069_bp1 | bytes_billed=10737418240 | duration_ms=2100 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.fact_user_events` WHERE event_name = 'workflow_created' LIMIT 100;
-- 2026-03-31 15:00:00 | user=nina.patel@acme.io | job_id=bq_0070_bq1 | bytes_billed=1073741824 | duration_ms=320 | status=DONE
SELECT customer_id, company_name FROM `nexus-analyst-demo.acme.dim_customers` WHERE current_plan_tier = 'Enterprise';
-- 2026-03-31 15:05:00 | user=lina.cho@acme.io | job_id=bq_0071_br1 | bytes_billed=5368709120 | duration_ms=1300 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.fact_opportunities` WHERE close_date < '2026-04-01' AND stage != 'Closed Won';
-- 2026-03-31 15:10:00 | user=marco.silva@acme.io | job_id=bq_0072_bs1 | bytes_billed=536870912 | duration_ms=280 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.fact_support_tickets` WHERE status = 'open' AND priority = 'P1';
-- 2026-03-31 15:15:00 | user=rajiv.menon@acme.io | job_id=bq_0073_bt1 | bytes_billed=2147483648 | duration_ms=500 | status=DONE
SELECT count(*) FROM `nexus-analyst-demo.acme.dim_employees` WHERE team = 'Eng';
-- 2026-03-31 15:20:00 | user=david.kim@acme.io | job_id=bq_0074_bu1 | bytes_billed=10737418240 | duration_ms=2200 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE error_code = 'AUTH_FAILED';
-- 2026-03-31 15:25:00 | user=nina.patel@acme.io | job_id=bq_0075_bv1 | bytes_billed=1073741824 | duration_ms=350 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.account_health` WHERE utilization_band < 0.2;
-- 2026-03-31 15:30:00 | user=lina.cho@acme.io | job_id=bq_0076_bw1 | bytes_billed=5368709120 | duration_ms=1400 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.fact_subscriptions` WHERE plan_tier = 'Business' AND seat_count > 100;
-- 2026-03-31 15:35:00 | user=marco.silva@acme.io | job_id=bq_0077_bx1 | bytes_billed=536870912 | duration_ms=270 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE status = 'paused';
-- 2026-03-31 15:40:00 | user=rajiv.menon@acme.io | job_id=bq_0078_by1 | bytes_billed=2147483648 | duration_ms=490 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.dim_dates` WHERE is_business_day IS TRUE LIMIT 10;
-- 2026-03-31 15:45:00 | user=david.kim@acme.io | job_id=bq_0079_bz1 | bytes_billed=10737418240 | duration_ms=2400 | status=DONE
SELECT triggered_by, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` GROUP BY 1;
-- 2026-03-31 15:50:00 | user=nina.patel@acme.io | job_id=bq_0080_ca1 | bytes_billed=1073741824 | duration_ms=310 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.fact_nps_responses` ORDER BY score ASC LIMIT 20;
-- 2026-03-31 15:55:00 | user=lina.cho@acme.io | job_id=bq_0081_cb1 | bytes_billed=5368709120 | duration_ms=1300 | status=DONE
SELECT sum(amount_usd) FROM `nexus-analyst-demo.acme.fact_invoices` WHERE paid_at IS NULL;
-- 2026-03-31 16:00:00 | user=marco.silva@acme.io | job_id=bq_0082_cc1 | bytes_billed=536870912 | duration_ms=300 | status=DONE
SELECT company_name, industry FROM `nexus-analyst-demo.acme.dim_customers` WHERE region = 'APAC';
-- 2026-03-31 16:05:00 | user=rajiv.menon@acme.io | job_id=bq_0083_cd1 | bytes_billed=2147483648 | duration_ms=470 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.dim_employees` WHERE location = 'Amsterdam';
-- 2026-03-31 16:10:00 | user=david.kim@acme.io | job_id=bq_0084_ce1 | bytes_billed=10737418240 | duration_ms=2300 | status=DONE
SELECT * FROM `nexus-analyst-demo.acme.fact_user_events` WHERE event_name = 'login' LIMIT 100;
-- 2026-03-31 16:15:00 | user=nina.patel@acme.io | job_id=bq_0085_cf1 | bytes_billed=1073741824 | duration_ms=340 | status=DONE
SELECT customer_id, count(*) FROM `nexus-analyst-demo.acme.fact_subscriptions` GROUP BY 1 HAVING count(*) > 1;
-- 2026-03-31 16:20:00 | user=lina.cho@acme.io | job_id=bq_0086_cg1 | bytes_billed=5368709120 | duration_ms=1250 | status=DONE


-- 2026-04-01 09:12:44 | user=nina.patel@acme.io | job_id=bq_0087_ch1 | bytes_billed=42949672960 | duration_ms=4200 | status=DONE
WITH cohort_2025 AS (
    -- Canonical NRR: Fixed cohort of paid customers 12 months ago
    SELECT 
        customer_id, 
        mrr_usd as start_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE is_current IS FALSE 
    AND start_date <= '2025-04-01' 
    AND (end_date > '2025-04-01' OR end_date IS NULL)
    AND plan_tier != 'Free'
),
current_val AS (
    SELECT 
        customer_id, 
        mrr_usd as end_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE is_current IS TRUE 
    AND plan_tier != 'Free'
)
SELECT 
    COUNT(c.customer_id) as cohort_size,
    SUM(c.start_mrr) as base_mrr,
    SUM(COALESCE(curr.end_mrr, 0)) as ending_mrr,
    SUM(COALESCE(curr.end_mrr, 0)) / SUM(c.start_mrr) as nrr_trailing_12
FROM cohort_2025 c
LEFT JOIN current_val curr ON c.customer_id = curr.customer_id;
-- 2026-04-01 09:45:12 | user=rajiv.menon@acme.io | job_id=bq_0088_ci1 | bytes_billed=0 | duration_ms=45 | status=ERROR
-- ERROR: Not found: Table nexus-analyst-demo.acme.marts.finance.arr_snapshot
SELECT * FROM `nexus-analyst-demo.acme.marts.finance.arr_snapshot` LIMIT 10;
-- 2026-04-01 09:46:30 | user=rajiv.menon@acme.io | job_id=bq_0089_cj1 | bytes_billed=1073741824 | duration_ms=210 | status=DONE
-- Fixing path, BQ is flat
SELECT * FROM `nexus-analyst-demo.acme.arr_snapshot` ORDER BY snapshot_date DESC LIMIT 5;
-- 2026-04-01 10:15:00 | user=lina.cho@acme.io | job_id=bq_0090_ck1 | bytes_billed=5368709120 | duration_ms=890 | status=DONE
SELECT 
    SUM(CASE WHEN plan_tier = 'Business' THEN mrr_usd * 12 ELSE 0 END) as arr_biz,
    SUM(CASE WHEN plan_tier = 'Enterprise' THEN mrr_usd * 12 ELSE 0 END) as arr_ent,
    SUM(CASE WHEN plan_tier = 'Pro' THEN mrr_usd * 12 ELSE 0 END) as arr_pro,
    SUM(mrr_usd * 12) as total_arr
FROM `nexus-analyst-demo.acme.fact_subscriptions` 
WHERE is_current IS TRUE AND plan_tier != 'Free';
-- 2026-04-01 11:02:15 | user=david.kim@acme.io | job_id=bq_0091_cl1 | bytes_billed=107374182400 | duration_ms=12400 | status=DONE
-- Investigating error spikes for Cobalt Systems (cust_000700)
SELECT 
    run_date,
    n_runs,
    auth_failed_count,
    integration_down_count,
    success_rate
FROM `nexus-analyst-demo.acme.workflow_runs_daily`
WHERE customer_id = 'cust_000700'
AND run_date >= '2026-03-01'
ORDER BY run_date DESC;
-- 2026-04-01 13:20:44 | user=nina.patel@acme.io | job_id=bq_0092_cm1 | bytes_billed=0 | duration_ms=35 | status=ERROR
-- ERROR: Name vrs_band not found in nexus-analyst-demo.acme.account_health
SELECT customer_id, vrs_band FROM `nexus-analyst-demo.acme.account_health` WHERE account_health_status = 'critical';
-- 2026-04-01 13:22:10 | user=nina.patel@acme.io | job_id=bq_0093_cn1 | bytes_billed=2147483648 | duration_ms=560 | status=DONE
-- VRS is parked, using utilization_band instead for health check
SELECT 
    customer_id, 
    account_tier, 
    utilization_band, 
    has_uncollectible_recent,
    account_health_status
FROM `nexus-analyst-demo.acme.account_health`
WHERE account_health_status = 'critical'
OR (account_tier != 'Enterprise' AND utilization_band < 0.20);
-- 2026-04-01 14:05:33 | user=marco.silva@acme.io | job_id=bq_0094_co1 | bytes_billed=1073741824 | duration_ms=340 | status=DONE
-- Check status of Tamarind Group (cust_000706)
SELECT company_name, status, current_plan_tier, current_mrr_usd 
FROM `nexus-analyst-demo.acme.dim_customers` 
WHERE customer_id = 'cust_000706';
-- 2026-04-02 09:00:12 | user=lina.cho@acme.io | job_id=bq_0095_cp1 | bytes_billed=8589934592 | duration_ms=1500 | status=DONE
-- Marketing attribution for Q1 bookings
SELECT 
    first_touch_channel,
    SUM(bookings_acv_usd) as total_bookings_acv
FROM `nexus-analyst-demo.acme.bookings_attribution`
WHERE closed_won_at BETWEEN '2026-01-01' AND '2026-03-31'
GROUP BY 1
ORDER BY 2 DESC;
-- 2026-04-02 10:30:45 | user=rajiv.menon@acme.io | job_id=bq_0096_cq1 | bytes_billed=32212254720 | duration_ms=5100 | status=DONE
-- Checking engaged status logic for PLG conversion candidates
-- Engaged = >=3 active users AND >=10 successful runs in trailing 28d
WITH activity_28d AS (
    SELECT 
        customer_id,
        COUNT(DISTINCT user_id) as active_users
    FROM `nexus-analyst-demo.acme.fact_user_events`
    WHERE event_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 28 DAY)
    GROUP BY 1
),
runs_28d AS (
    SELECT 
        customer_id,
        COUNT(*) as success_runs
    FROM `nexus-analyst-demo.acme.fact_workflow_runs`
    WHERE status = 'SUCCESS'
    AND triggered_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 28 DAY)
    GROUP BY 1
)
SELECT 
    c.customer_id,
    c.company_name,
    a.active_users,
    r.success_runs
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN activity_28d a ON c.customer_id = a.customer_id
JOIN runs_28d r ON c.customer_id = r.customer_id
WHERE c.current_plan_tier = 'Free'
AND a.active_users >= 3
AND r.success_runs >= 10;
-- 2026-04-02 11:45:00 | user=david.kim@acme.io | job_id=bq_0097_cr1 | bytes_billed=21474836480 | duration_ms=3200 | status=DONE
-- Audit: Why did Beacon Studios (cust_000287) show as healthy before churn?
SELECT 
    snapshot_date,
    utilization_band,
    is_engaged,
    account_health_status
FROM `nexus-analyst-demo.acme.account_health`
WHERE customer_id = 'cust_000287'
AND snapshot_date <= '2026-02-18'
ORDER BY snapshot_date DESC LIMIT 10;
-- 2026-04-02 14:12:11 | user=nina.patel@acme.io | job_id=bq_0098_cs1 | bytes_billed=5368709120 | duration_ms=920 | status=DONE
-- Verifying Enterprise critical health rule: only uncollectible invoice
SELECT 
    c.company_name,
    h.customer_id,
    h.utilization_band,
    h.has_uncollectible_recent,
    h.account_health_status
FROM `nexus-analyst-demo.acme.account_health` h
JOIN `nexus-analyst-demo.acme.dim_customers` c ON h.customer_id = c.customer_id
WHERE c.account_tier = 'Enterprise'
AND h.account_health_status = 'critical';
-- 2026-04-03 09:30:22 | user=lina.cho@acme.io | job_id=bq_0099_ct1 | bytes_billed=1073741824 | duration_ms=450 | status=DONE
-- Check MRR for Marigold Health (cust_000701) - Enterprise seat math
-- 300 seats * $15,000 MRR is custom pricing ($180k ACV)
SELECT 
    customer_id, 
    plan_tier, 
    mrr_usd, 
    seat_count 
FROM `nexus-analyst-demo.acme.fact_subscriptions` 
WHERE customer_id = 'cust_000701' AND is_current IS TRUE;
-- 2026-04-03 10:15:55 | user=rajiv.menon@acme.io | job_id=bq_0100_cu1 | bytes_billed=21474836480 | duration_ms=2800 | status=DONE
-- Monthly workflow run volume by tier for capacity planning
SELECT 
    FORMAT_DATE('%Y-%m', run_date) as month,
    c.current_plan_tier,
    SUM(n_runs) as total_runs
FROM `nexus-analyst-demo.acme.workflow_runs_daily` w
JOIN `nexus-analyst-demo.acme.dim_customers` c ON w.customer_id = c.customer_id
GROUP BY 1, 2
ORDER BY 1 DESC, 3 DESC;
-- 2026-04-03 11:50:10 | user=nina.patel@acme.io | job_id=bq_0101_cv1 | bytes_billed=536870912 | duration_ms=180 | status=DONE
-- Quick check on CSM load
SELECT 
    e.full_name as csm_name,
    COUNT(c.customer_id) as account_count,
    SUM(c.current_mrr_usd) as book_mrr
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_employees` e ON c.csm_employee_id = e.employee_id
WHERE c.status = 'active'
GROUP BY 1
ORDER BY 3 DESC;
-- 2026-04-03 13:05:44 | user=david.kim@acme.io | job_id=bq_0102_cw1 | bytes_billed=107374182400 | duration_ms=15200 | status=DONE
-- Latency check across regions
SELECT 
    c.region,
    AVG(w.p50_duration_ms) as avg_p50,
    AVG(w.p95_duration_ms) as avg_p95
FROM `nexus-analyst-demo.acme.workflow_runs_daily` w
JOIN `nexus-analyst-demo.acme.dim_customers` c ON w.customer_id = c.customer_id
WHERE w.run_date >= '2026-03-01'
GROUP BY 1;
-- 2026-04-03 15:22:01 | user=lina.cho@acme.io | job_id=bq_0103_cx1 | bytes_billed=5368709120 | duration_ms=1100 | status=DONE
-- Pro plan seat consistency check ($49/seat)
SELECT 
    customer_id,
    seat_count,
    mrr_usd,
    mrr_usd / seat_count as derived_seat_price
FROM `nexus-analyst-demo.acme.fact_subscriptions`
WHERE plan_tier = 'Pro' 
AND is_current IS TRUE
AND (mrr_usd / seat_count) != 49;
-- 2026-04-03 16:40:12 | user=rajiv.menon@acme.io | job_id=bq_0104_cy1 | bytes_billed=2147483648 | duration_ms=620 | status=DONE
-- Cleanup: checking for customers with active status but no active subscriptions
SELECT 
    c.customer_id,
    c.company_name,
    c.status
FROM `nexus-analyst-demo.acme.dim_customers` c
LEFT JOIN `nexus-analyst-demo.acme.fact_subscriptions` s 
    ON c.customer_id = s.customer_id AND s.is_current IS TRUE
WHERE c.status = 'active' AND s.subscription_id IS NULL;
-- 2026-04-04 09:15:30 | user=nina.patel@acme.io | job_id=bq_0105_cz1 | bytes_billed=32212254720 | duration_ms=4400 | status=DONE
-- Cohort analysis for expansion: Customers who upgraded from Pro to Business
SELECT 
    s2.customer_id,
    s1.plan_tier as old_tier,
    s2.plan_tier as new_tier,
    s2.start_date as upgrade_date,
    s2.mrr_usd - s1.mrr_usd as expansion_amount
FROM `nexus-analyst-demo.acme.fact_subscriptions` s1
JOIN `nexus-analyst-demo.acme.fact_subscriptions` s2 
    ON s1.customer_id = s2.customer_id
WHERE s1.plan_tier = 'Pro'
AND s2.plan_tier = 'Business'
AND s2.change_type = 'upgrade'
AND s2.changed_from_subscription_id = s1.subscription_id;
-- 2026-04-04 10:45:11 | user=lina.cho@acme.io | job_id=bq_0106_da1 | bytes_billed=1073741824 | duration_ms=310 | status=DONE
-- NRR Snapshot for Board Report (Canonical)
SELECT 
    snapshot_date,
    nrr,
    grr,
    cohort_size
FROM `nexus-analyst-demo.acme.nrr_trailing_12`
ORDER BY snapshot_date DESC LIMIT 1;
-- 2026-04-04 11:20:00 | user=david.kim@acme.io | job_id=bq_0107_db1 | bytes_billed=53687091200 | duration_ms=8700 | status=DONE
-- Event volume by user role for Onyx Robotics (cust_000704)
SELECT 
    u.role,
    e.event_name,
    COUNT(*) as event_count
FROM `nexus-analyst-demo.acme.fact_user_events` e
JOIN `nexus-analyst-demo.acme.dim_users` u ON e.user_id = u.user_id
WHERE e.customer_id = 'cust_000704'
GROUP BY 1, 2
ORDER BY 3 DESC;

-- 2026-04-05 08:30:15 | user=nina.patel@acme.io | job_id=bq_0108_dc1 | bytes_billed=8589934592 | duration_ms=1200 | status=DONE
-- Investigating high failure rates in workflows for FinTech customers in EMEA
SELECT 
    c.company_name,
    r.error_code,
    COUNT(r.run_id) as failure_count,
    ROUND(AVG(r.duration_ms), 2) as avg_duration
FROM `nexus-analyst-demo.acme.fact_workflow_runs` r
JOIN `nexus-analyst-demo.acme.dim_customers` c ON r.customer_id = c.customer_id
WHERE c.industry = 'FinTech' 
  AND c.region = 'EMEA'
  AND r.status = 'failed'
  AND r.triggered_at >= '2026-03-01'
GROUP BY 1, 2
ORDER BY 3 DESC;

-- 2026-04-05 09:12:44 | user=rajiv.menon@acme.io | job_id=bq_0109_dd1 | bytes_billed=0 | duration_ms=45 | status=ERROR
-- ERROR: Table name typo? Trying to pull raw logs for debugging
SELECT * FROM `nexus-analyst-demo.acme.fact_workflow_step_logs` LIMIT 100;

-- 2026-04-05 14:22:10 | user=lina.cho@acme.io | job_id=bq_0110_de1 | bytes_billed=12884901888 | duration_ms=3100 | status=DONE
-- Monthly ARR Bridge (Simplified New/Expansion/Churn)
WITH monthly_mrr AS (
    SELECT 
        DATE_TRUNC(start_date, MONTH) as mrr_month,
        customer_id,
        mrr_usd,
        change_type
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE is_current IS TRUE OR end_date > '2026-01-01'
)
SELECT 
    mrr_month,
    SUM(CASE WHEN change_type = 'new' THEN mrr_usd ELSE 0 END) as new_mrr,
    SUM(CASE WHEN change_type = 'upgrade' THEN mrr_usd ELSE 0 END) as expansion_mrr,
    SUM(CASE WHEN change_type = 'churn' THEN mrr_usd ELSE 0 END) as churn_mrr
FROM monthly_mrr
GROUP BY 1
ORDER BY 1 DESC;

-- 2026-04-06 10:05:33 | user=sarah.jenkins@acme.io | job_id=bq_0111_df1 | bytes_billed=4294967296 | duration_ms=890 | status=DONE
-- Seat utilization check for Enterprise accounts (Targeting upsell for MM)
SELECT 
    c.company_name,
    c.account_tier,
    c.seat_count_licensed,
    COUNT(u.user_id) as active_user_count,
    SAFE_DIVIDE(COUNT(u.user_id), c.seat_count_licensed) as utilization_rate
FROM `nexus-analyst-demo.acme.dim_customers` c
LEFT JOIN `nexus-analyst-demo.acme.dim_users` u ON c.customer_id = u.customer_id
WHERE c.status = 'active' 
  AND c.current_plan_tier IN ('Business', 'Enterprise')
  AND u.is_active IS TRUE
GROUP BY 1, 2, 3
HAVING utilization_rate > 0.9
ORDER BY utilization_rate DESC;

-- 2026-04-06 11:45:02 | user=david.kim@acme.io | job_id=bq_0112_dg1 | bytes_billed=1073741824 | duration_ms=420 | status=DONE
-- Checking invoice payment lag for top 10 MRR accounts
SELECT 
    c.company_name,
    i.invoice_id,
    i.amount_usd,
    DATE_DIFF(i.paid_at, i.invoice_date, DAY) as days_to_pay,
    i.status
FROM `nexus-analyst-demo.acme.fact_invoices` i
JOIN `nexus-analyst-demo.acme.dim_customers` c ON i.customer_id = c.customer_id
WHERE i.invoice_date >= '2026-01-01'
  AND c.current_mrr_usd > 5000
ORDER BY i.amount_usd DESC
LIMIT 10;

-- 2026-04-07 16:20:11 | user=nina.patel@acme.io | job_id=bq_0113_dh1 | bytes_billed=21474836480 | duration_ms=5600 | status=DONE
-- User engagement by feature for Onyx Robotics (cust_000704) vs Industry Avg
WITH onyx_events AS (
    SELECT 
        event_name,
        COUNT(*) as onyx_count
    FROM `nexus-analyst-demo.acme.fact_user_events`
    WHERE customer_id = 'cust_000704'
    GROUP BY 1
),
industry_avg AS (
    SELECT 
        e.event_name,
        COUNT(*) / COUNT(DISTINCT c.customer_id) as avg_count
    FROM `nexus-analyst-demo.acme.fact_user_events` e
    JOIN `nexus-analyst-demo.acme.dim_customers` c ON e.customer_id = c.customer_id
    WHERE c.industry = 'Robotics'
    GROUP BY 1
)
SELECT 
    o.event_name,
    o.onyx_count,
    ROUND(i.avg_count, 2) as robotics_industry_avg
FROM onyx_events o
JOIN industry_avg i ON o.event_name = i.event_name
ORDER BY o.onyx_count DESC;

-- 2026-04-08 09:05:44 | user=rajiv.menon@acme.io | job_id=bq_0114_di1 | bytes_billed=536870912 | duration_ms=210 | status=DONE
-- Ad-hoc: Check employee assignments for recent MM wins
SELECT 
    c.company_name,
    c.signup_date,
    ae.full_name as owner_ae,
    csm.full_name as assigned_csm
FROM `nexus-analyst-demo.acme.dim_customers` c
LEFT JOIN `nexus-analyst-demo.acme.dim_employees` ae ON c.ae_employee_id = ae.employee_id
LEFT JOIN `nexus-analyst-demo.acme.dim_employees` csm ON c.csm_employee_id = csm.employee_id
WHERE c.account_tier = 'MM' 
  AND c.signup_date >= '2026-03-01'
ORDER BY c.signup_date DESC;

-- 2026-04-08 13:55:22 | user=lina.cho@acme.io | job_id=bq_0115_dj1 | bytes_billed=32212254720 | duration_ms=7800 | status=DONE
-- Global Workflow Run Performance (P95 duration) by region for Executive Dashboard
SELECT 
    d.month_name,
    c.region,
    PERCENTILE_CONT(r.duration_ms, 0.95) OVER(PARTITION BY c.region, d.month_name) as p95_duration_ms,
    COUNT(r.run_id) as total_runs
FROM `nexus-analyst-demo.acme.fact_workflow_runs` r
JOIN `nexus-analyst-demo.acme.dim_customers` c ON r.customer_id = c.customer_id
JOIN `nexus-analyst-demo.acme.dim_dates` d ON CAST(r.triggered_at AS DATE) = d.date
WHERE d.year = 2026
GROUP BY 1, 2, r.duration_ms
ORDER BY 1, 2;

-- 2026-04-09 10:10:01 | user=nina.patel@acme.io | job_id=bq_0116_dk1 | bytes_billed=0 | duration_ms=12 | status=ERROR
-- ERROR: Forgot the FROM clause while copy-pasting
SELECT customer_id, company_name WHERE status = 'churned' AND churn_date > '2026-01-01';

-- 2026-04-09 10:11:15 | user=nina.patel@acme.io | job_id=bq_0117_dl1 | bytes_billed=1073741824 | duration_ms=350 | status=DONE
-- Re-run: Churn list for CS post-mortem
SELECT 
    customer_id, 
    company_name, 
    current_plan_tier, 
    current_mrr_usd,
    churn_date 
FROM `nexus-analyst-demo.acme.dim_customers` 
WHERE status = 'churned' 
  AND churn_date >= '2026-01-01'
ORDER BY churn_date DESC;

-- 2026-04-10 15:30:45 | user=david.kim@acme.io | job_id=bq_0118_dm1 | bytes_billed=5368709120 | duration_ms=2200 | status=DONE
-- Correlation between step count and error rates for Free vs Pro
SELECT 
    p.plan_tier,
    CASE 
        WHEN r.step_count < 5 THEN 'Small (1-4)'
        WHEN r.step_count < 15 THEN 'Medium (5-14)'
        ELSE 'Large (15+)'
    END as workflow_size,
    COUNT(*) as total_runs,
    ROUND(COUNTIF(r.status = 'failed') / COUNT(*), 4) as failure_rate
FROM `nexus-analyst-demo.acme.fact_workflow_runs` r
JOIN `nexus-analyst-demo.acme.dim_customers` c ON r.customer_id = c.customer_id
JOIN `nexus-analyst-demo.acme.dim_plans` p ON c.current_plan_tier = p.plan_tier
WHERE r.triggered_at >= '2026-03-01'
GROUP BY 1, 2
ORDER BY 1, 2;

-- 2026-04-12 09:15:22 | user=marcus.thorne@acme.io | job_id=bq_0119_dn2 | bytes_billed=12884901888 | duration_ms=4100 | status=DONE
-- Q1 2026 NRR Calculation (Net Retention) - Excluding Enterprise custom deals for now
WITH cohort_jan AS (
    SELECT 
        customer_id, 
        mrr_usd as starting_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE is_current = true 
      AND start_date <= '2026-01-01'
      AND plan_tier != 'Enterprise'
),
cohort_mar AS (
    SELECT 
        customer_id, 
        mrr_usd as ending_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE is_current = true 
      AND (end_date IS NULL OR end_date > '2026-03-31')
      AND plan_tier != 'Enterprise'
)
SELECT 
    SUM(c1.starting_mrr) as total_start_mrr,
    SUM(COALESCE(c2.ending_mrr, 0)) as total_end_mrr,
    ROUND(SUM(COALESCE(c2.ending_mrr, 0)) / SUM(c1.starting_mrr), 4) as nrr_q1_smb_mm
FROM cohort_jan c1
LEFT JOIN cohort_mar c2 ON c1.customer_id = c2.customer_id;

-- 2026-04-12 11:45:09 | user=sarah.chen@acme.io | job_id=bq_0120_do3 | bytes_billed=0 | duration_ms=45 | status=ERROR
-- ERROR: Table name typo, should be fact_user_events
SELECT event_type, count(*) 
FROM `nexus-analyst-demo.acme.fact_events` 
WHERE event_at > '2026-04-01' 
GROUP BY 1;

-- 2026-04-12 11:46:30 | user=sarah.chen@acme.io | job_id=bq_0121_dp4 | bytes_billed=8589934592 | duration_ms=1800 | status=DONE
-- Tracking 'Workflow Created' vs 'Workflow Run' activation for April Cohort
SELECT 
    u.customer_id,
    COUNT(DISTINCT CASE WHEN e.event_type = 'workflow_created' THEN e.user_id END) as creators,
    COUNT(DISTINCT r.run_id) as total_runs_mtd
FROM `nexus-analyst-demo.acme.dim_users` u
JOIN `nexus-analyst-demo.acme.fact_user_events` e ON u.user_id = e.user_id
LEFT JOIN `nexus-analyst-demo.acme.fact_workflow_runs` r ON u.customer_id = r.customer_id
WHERE u.signup_date >= '2026-04-01'
  AND e.event_at >= '2026-04-01'
GROUP BY 1
HAVING total_runs_mtd > 0;

-- 2026-04-13 14:20:11 | user=nina.patel@acme.io | job_id=bq_0122_dq5 | bytes_billed=21474836480 | duration_ms=14200 | status=DONE
-- MEGA JOIN: Customer 360 Health for Weekly Leadership Sync (All 5 Marts)
-- Hits dim_customers, dim_plans, dim_employees (AE/CSM), fact_subscriptions, and fact_workflow_runs
WITH usage_stats AS (
    SELECT 
        customer_id, 
        COUNT(run_id) as monthly_runs,
        AVG(duration_ms) as avg_latency
    FROM `nexus-analyst-demo.acme.fact_workflow_runs`
    WHERE triggered_at >= '2026-03-01'
    GROUP BY 1
)
SELECT 
    c.company_name,
    c.account_tier,
    p.plan_tier,
    ae.full_name as account_executive,
    csm.full_name as success_manager,
    s.mrr_usd as current_mrr,
    u.monthly_runs,
    p.workflow_run_quota_per_month as quota,
    SAFE_DIVIDE(u.monthly_runs, p.workflow_run_quota_per_month) as quota_utilization
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_plans` p ON c.current_plan_tier = p.plan_tier
JOIN `nexus-analyst-demo.acme.dim_employees` ae ON c.ae_employee_id = ae.employee_id
JOIN `nexus-analyst-demo.acme.dim_employees` csm ON c.csm_employee_id = csm.employee_id
JOIN `nexus-analyst-demo.acme.fact_subscriptions` s ON c.customer_id = s.customer_id AND s.is_current = true
LEFT JOIN usage_stats u ON c.customer_id = u.customer_id
WHERE c.status = 'active'
  AND c.region = 'EMEA'
ORDER BY current_mrr DESC
LIMIT 50;

-- 2026-04-14 08:05:44 | user=david.kim@acme.io | job_id=bq_0123_dr6 | bytes_billed=4294967296 | duration_ms=950 | status=DONE
-- Checking storage usage vs SLA for Enterprise customers in SF
SELECT 
    c.company_name,
    p.storage_gb as plan_limit_gb,
    p.sla_uptime_pct,
    COUNT(DISTINCT u.user_id) as active_user_count
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_plans` p ON c.current_plan_tier = p.plan_tier
JOIN `nexus-analyst-demo.acme.dim_users` u ON c.customer_id = u.customer_id
WHERE c.account_tier = 'Enterprise'
  AND c.region = 'HQ'
  AND u.is_active = true
GROUP BY 1, 2, 3;

-- 2026-04-15 16:55:01 | user=chloe.vasquez@acme.io | job_id=bq_0124_ds7 | bytes_billed=536870912 | duration_ms=210 | status=DONE
-- Quick check on specific high-risk account 'CUST-442' (Global Logistics Corp)
-- AE reported they might churn due to seat pricing
SELECT 
    customer_id, 
    company_name, 
    seat_count_licensed, 
    current_mrr_usd,
    acquisition_channel
FROM `nexus-analyst-demo.acme.dim_customers`
WHERE customer_id = 'CUST-442';

-- 2026-04-15 17:02:12 | user=chloe.vasquez@acme.io | job_id=bq_0125_dt8 | bytes_billed=1073741824 | duration_ms=450 | status=DONE
-- Audit log of subscription changes for 'CUST-442' to see expansion history
SELECT 
    subscription_id,
    plan_tier,
    mrr_usd,
    seat_count,
    change_type,
    start_date
FROM `nexus-analyst-demo.acme.fact_subscriptions`
WHERE customer_id = 'CUST-442'
ORDER BY start_date ASC;

-- 2026-04-16 10:30:00 | user=marcus.thorne@acme.io | job_id=bq_0126_du9 | bytes_billed=2147483648 | duration_ms=1100 | status=DONE
-- Monthly Invoiced Totals (Paid vs Pending) for Finance closing
SELECT 
    d.month_name,
    i.status,
    SUM(i.amount_usd) as total_invoiced
FROM `nexus-analyst-demo.acme.fact_invoices` i
JOIN `nexus-analyst-demo.acme.dim_dates` d ON i.invoice_date = d.date
WHERE d.year = 2026 AND d.month <= 4
GROUP BY 1, 2
ORDER BY 1, 2;

-- 2026-04-17 12:12:12 | user=nina.patel@acme.io | job_id=bq_0127_dv0 | bytes_billed=0 | duration_ms=15 | status=ERROR
-- ERROR: Wrong project prefix used by mistake
SELECT * FROM `acme-prod.nexus.dim_customers` LIMIT 10;

-- 2026-04-17 12:13:05 | user=nina.patel@acme.io | job_id=bq_0128_dw1 | bytes_billed=536870912 | duration_ms=180 | status=DONE
-- Fixed project prefix
SELECT customer_id, company_name FROM `nexus-analyst-demo.acme.dim_customers` LIMIT 10;

-- 2026-04-18 09:15:22 | user=chloe.vasquez@acme.io | job_id=bq_0129_dx2 | bytes_billed=4294967296 | duration_ms=2450 | status=DONE
-- Board Deck prep: NRR (Net Revenue Retention) for Business tier cohort from Q1 2025
-- Looking at how those who started in Q1 '25 are performing 12 months later (Jan-March 2026)
WITH cohort_base AS (
    SELECT 
        customer_id,
        mrr_usd as starting_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE start_date BETWEEN '2025-01-01' AND '2025-03-31'
      AND plan_tier = 'Business'
      AND change_type = 'NEW_LOGO'
),
current_val AS (
    SELECT 
        s.customer_id,
        SUM(s.mrr_usd) as ending_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions` s
    JOIN `nexus-analyst-demo.acme.dim_dates` d ON s.start_date = d.date
    WHERE d.year = 2026 AND d.month <= 3
      AND s.is_current = true
    GROUP BY 1
)
SELECT 
    SUM(cb.starting_mrr) as cohort_start_mrr,
    SUM(COALESCE(cv.ending_mrr, 0)) as cohort_end_mrr,
    SAFE_DIVIDE(SUM(COALESCE(cv.ending_mrr, 0)), SUM(cb.starting_mrr)) * 100 as nrr_pct
FROM cohort_base cb
LEFT JOIN current_val cv ON cb.customer_id = cv.customer_id;

-- 2026-04-18 11:40:05 | user=nina.patel@acme.io | job_id=bq_0130_dy3 | bytes_billed=8589934592 | duration_ms=5800 | status=DONE
-- Investigating spike in 'ERR-99' (Timeout) for Skyline Interactive (CUST-102)
-- Nina: "They're complaining about the Salesforce-to-Snowflake sync failing constantly."
SELECT 
    triggered_at,
    workflow_id,
    duration_ms,
    status,
    error_code
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE customer_id = 'CUST-102'
  AND triggered_at >= '2026-04-10'
  AND status = 'FAILED'
ORDER BY triggered_at DESC
LIMIT 100;

-- 2026-04-18 11:42:10 | user=nina.patel@acme.io | job_id=bq_0131_dz4 | bytes_billed=0 | duration_ms=12 | status=ERROR
-- ERROR: Field 'trigger_type' does not exist in fact_workflow_runs
SELECT trigger_type, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` GROUP BY 1;

-- 2026-04-19 14:20:00 | user=liam.oconnell@acme.io | job_id=bq_0132_ea5 | bytes_billed=2147483648 | duration_ms=1200 | status=DONE
-- CSM health check for Summit Peak Solutions (CUST-881)
-- Checking if they are nearing their Business tier quota (100k runs/mo)
SELECT 
    c.company_name,
    p.workflow_run_quota_per_month,
    COUNT(r.run_id) as actual_runs_this_month
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_plans` p ON c.current_plan_tier = p.plan_tier
LEFT JOIN `nexus-analyst-demo.acme.fact_workflow_runs` r ON c.customer_id = r.customer_id
WHERE c.customer_id = 'CUST-881'
  AND r.triggered_at >= '2026-04-01'
GROUP BY 1, 2;

-- 2026-04-20 09:05:33 | user=marcus.thorne@acme.io | job_id=bq_0133_eb6 | bytes_billed=1073741824 | duration_ms=890 | status=DONE
-- Checking AE performance vs MRR closed in Q1 2026
-- Need this for commission overrides
SELECT 
    e.full_name as ae_name,
    SUM(s.mrr_usd) as total_mrr_closed,
    COUNT(DISTINCT s.customer_id) as new_customer_count
FROM `nexus-analyst-demo.acme.fact_subscriptions` s
JOIN `nexus-analyst-demo.acme.dim_customers` c ON s.customer_id = c.customer_id
JOIN `nexus-analyst-demo.acme.dim_employees` e ON c.ae_employee_id = e.employee_id
WHERE s.start_date BETWEEN '2026-01-01' AND '2026-03-31'
  AND s.change_type = 'NEW_LOGO'
GROUP BY 1
ORDER BY 2 DESC;

-- 2026-04-20 16:44:12 | user=chloe.vasquez@acme.io | job_id=bq_0134_ec7 | bytes_billed=536870912 | duration_ms=310 | status=DONE
-- Verification of active users vs licensed seats for 'Global Logistics Corp' (CUST-442)
-- They claim they are paying for way more than they use.
WITH seat_usage AS (
    SELECT 
        customer_id,
        COUNT(DISTINCT user_id) as active_user_count
    FROM `nexus-analyst-demo.acme.dim_users`
    WHERE is_active = true
    GROUP BY 1
)
SELECT 
    c.company_name,
    c.seat_count_licensed,
    u.active_user_count,
    (c.seat_count_licensed - u.active_user_count) as wasted_seats
FROM `nexus-analyst-demo.acme.dim_customers` c
LEFT JOIN seat_usage u ON c.customer_id = u.customer_id
WHERE c.customer_id = 'CUST-442';

-- 2026-04-21 10:11:05 | user=ravi.kumar@acme.io | job_id=bq_0135_ed8 | bytes_billed=17179869184 | duration_ms=14500 | status=DONE
-- Platform team: Scanning for high-duration workflows that might be hogging worker threads
-- Targeting Enterprise tier specifically to ensure SLA compliance
SELECT 
    c.company_name,
    r.workflow_id,
    AVG(r.duration_ms) as avg_duration,
    MAX(r.duration_ms) as max_duration,
    COUNT(*) as total_runs
FROM `nexus-analyst-demo.acme.fact_workflow_runs` r
JOIN `nexus-analyst-demo.acme.dim_customers` c ON r.customer_id = c.customer_id
WHERE c.account_tier = 'Enterprise'
  AND r.triggered_at >= '2026-04-01'
GROUP BY 1, 2
HAVING avg_duration > 15000
ORDER BY avg_duration DESC;

-- 2026-04-22 13:02:55 | user=nina.patel@acme.io | job_id=bq_0136_ee9 | bytes_billed=5368709120 | duration_ms=3200 | status=DONE
-- Checking adoption of "SSO" (audit log) events for Business/Enterprise accounts
-- Trying to see if customers are actually using the security features we sell them on.
SELECT 
    c.account_tier,
    COUNT(DISTINCT e.customer_id) as accounts_using_sso,
    COUNT(e.event_id) as total_sso_events
FROM `nexus-analyst-demo.acme.fact_user_events` e
JOIN `nexus-analyst-demo.acme.dim_customers` c ON e.customer_id = c.customer_id
WHERE e.event_type = 'sso_login'
  AND e.event_at >= '2026-01-01'
GROUP BY 1;

-- 2026-04-23 15:00:01 | user=marcus.thorne@acme.io | job_id=bq_0137_ef0 | bytes_billed=1073741824 | duration_ms=950 | status=DONE
-- Quick ARR snapshot for CFO
-- Total current MRR * 12
SELECT 
    SUM(current_mrr_usd) * 12 as total_run_rate_arr,
    SUM(CASE WHEN account_tier = 'Enterprise' THEN current_mrr_usd ELSE 0 END) * 12 as enterprise_arr,
    SUM(CASE WHEN account_tier = 'MM' THEN current_mrr_usd ELSE 0 END) * 12 as mid_market_arr,
    SUM(CASE WHEN account_tier = 'SMB' THEN current_mrr_usd ELSE 0 END) * 12 as smb_arr
FROM `nexus-analyst-demo.acme.dim_customers`
WHERE status = 'Active';

-- 2026-04-24 11:22:33 | user=nina.patel@acme.io | job_id=bq_0138_eg1 | bytes_billed=0 | duration_ms=5 | status=ERROR
-- ERROR: Table nexus-analyst-demo.acme.fact_workflow_errors does not exist. (Wait, I thought we built this? - Nina)
SELECT * FROM `nexus-analyst-demo.acme.fact_workflow_errors` LIMIT 10;

-- 2026-04-24 11:23:15 | user=nina.patel@acme.io | job_id=bq_0139_eh2 | bytes_billed=1073741824 | duration_ms=700 | status=DONE
-- Ah, it was just error_code in the main fact table. 
SELECT error_code, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE error_code IS NOT NULL GROUP BY 1;

-- 2026-04-25 09:14:22 | user=marcus.thorne@acme.io | job_id=bq_0140_ei3 | bytes_billed=8589934592 | duration_ms=4100 | status=DONE
-- Board Deck Prep: Net Revenue Retention (NRR) for the trailing 12 months.
-- Comparing the cohort MRR from April 2025 vs their current MRR in April 2026.
WITH cohort_april_2025 AS (
    SELECT 
        customer_id,
        mrr_usd as starting_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE is_current = FALSE 
      AND start_date <= '2025-04-01'
      AND (end_date > '2025-04-01' OR end_date IS NULL)
),
current_val AS (
    SELECT 
        customer_id,
        current_mrr_usd as ending_mrr,
        status
    FROM `nexus-analyst-demo.acme.dim_customers`
)
SELECT 
    SUM(c.starting_mrr) as cohort_start_mrr,
    SUM(cv.ending_mrr) as cohort_end_mrr,
    (SUM(cv.ending_mrr) / SUM(c.starting_mrr)) * 100 as nrr_pct
FROM cohort_april_2025 c
JOIN current_val cv ON c.customer_id = cv.customer_id;

-- 2026-04-25 10:45:10 | user=nina.patel@acme.io | job_id=bq_0141_ej4 | bytes_billed=2147483648 | duration_ms=1200 | status=DONE
-- Investigating heavy load for Customer ID 'C-8812' (Globex Corp - Enterprise). 
-- They're complaining about latency in their webhooks.
SELECT 
    status,
    count(*) as run_count,
    avg(duration_ms) as avg_duration,
    max(duration_ms) as max_duration,
    avg(step_count) as avg_steps
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE customer_id = 'C-8812'
  AND triggered_at >= '2026-04-01'
GROUP BY 1;

-- 2026-04-26 14:02:11 | user=carlos.mendez@acme.io | job_id=bq_0142_ek5 | bytes_billed=536870912 | duration_ms=450 | status=DONE
-- CS Health Check: How many Enterprise accounts does each CSM have?
-- Carlos wants to rebalance the load before the Q3 hiring freeze.
SELECT 
    e.full_name as csm_name,
    count(c.customer_id) as account_count,
    sum(c.current_mrr_usd) as total_managed_mrr
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_employees` e ON c.csm_employee_id = e.employee_id
WHERE c.status = 'Active'
  AND c.account_tier = 'Enterprise'
GROUP BY 1
ORDER BY total_managed_mrr DESC;

-- 2026-04-27 16:30:05 | user=nina.patel@acme.io | job_id=bq_0143_el6 | bytes_billed=0 | duration_ms=10 | status=ERROR
-- ERROR: Column 'seat_count' not found in nexus-analyst-demo.acme.dim_customers. (Duh, it's seat_count_licensed - Nina)
SELECT company_name, seat_count FROM `nexus-analyst-demo.acme.dim_customers` WHERE account_tier = 'MM';

-- 2026-04-27 16:31:40 | user=nina.patel@acme.io | job_id=bq_0144_em7 | bytes_billed=1073741824 | duration_ms=880 | status=DONE
-- Checking seat utilization (licensed vs active users) for Business tier.
-- Potential upsell/downsell signals here.
SELECT 
    c.customer_id,
    c.company_name,
    c.seat_count_licensed,
    COUNT(DISTINCT u.user_id) as active_user_count,
    (COUNT(DISTINCT u.user_id) / NULLIF(c.seat_count_licensed, 0)) * 100 as utilization_pct
FROM `nexus-analyst-demo.acme.dim_customers` c
LEFT JOIN `nexus-analyst-demo.acme.dim_users` u ON c.customer_id = u.customer_id AND u.is_active = TRUE
WHERE c.account_tier = 'Business'
  AND c.status = 'Active'
GROUP BY 1, 2, 3
HAVING utilization_pct > 90
ORDER BY utilization_pct DESC;

-- 2026-04-28 09:12:33 | user=sarah.chen@acme.io | job_id=bq_0145_en8 | bytes_billed=4294967296 | duration_ms=3100 | status=DONE
-- PLG Motion: How long from 'Free' signup to 'Pro' upgrade?
-- We need this for the Growth team sync.
WITH first_signup AS (
    SELECT 
        customer_id,
        signup_date
    FROM `nexus-analyst-demo.acme.dim_customers`
    WHERE current_plan_tier != 'Free'
),
upgrade_event AS (
    SELECT 
        customer_id,
        MIN(start_date) as pro_start_date
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE plan_tier = 'Pro'
    GROUP BY 1
)
SELECT 
    AVG(DATE_DIFF(u.pro_start_date, s.signup_date, DAY)) as avg_days_to_upgrade,
    APPROX_QUANTILES(DATE_DIFF(u.pro_start_date, s.signup_date, DAY), 100)[OFFSET(50)] as median_days_to_upgrade
FROM first_signup s
JOIN upgrade_event u ON s.customer_id = u.customer_id;

-- 2026-04-29 11:55:01 | user=nina.patel@acme.io | job_id=bq_0146_eo9 | bytes_billed=1073741824 | duration_ms=520 | status=DONE
-- Quick look at the top 5 industries by MRR for the AE team's outbound push.
SELECT 
    industry,
    SUM(current_mrr_usd) as total_mrr,
    COUNT(customer_id) as customer_count
FROM `nexus-analyst-demo.acme.dim_customers`
WHERE status = 'Active'
GROUP BY 1
ORDER BY 2 DESC
LIMIT 5;

-- 2026-04-30 13:22:15 | user=marcus.thorne@acme.io | job_id=bq_0147_ep0 | bytes_billed=16106127360 | duration_ms=5900 | status=DONE
-- Massive query for Q1 Closing. 
-- Monthly Recurring Revenue by Region and Tier including tax/invoice status.
-- This is going to the CEO, don't mess up.
SELECT 
    d.month_name,
    c.region,
    c.account_tier,
    SUM(i.amount_usd) as invoiced_amount,
    COUNT(DISTINCT i.invoice_id) as invoice_count
FROM `nexus-analyst-demo.acme.fact_invoices` i
JOIN `nexus-analyst-demo.acme.dim_customers` c ON i.customer_id = c.customer_id
JOIN `nexus-analyst-demo.acme.dim_dates` d ON i.invoice_date = d.date
WHERE d.year = 2026
  AND d.quarter = 1
  AND i.status = 'Paid'
GROUP BY 1, 2, 3
ORDER BY 1, 2;

-- 2026-05-01 10:05:44 | user=nina.patel@acme.io | job_id=bq_0148_eq1 | bytes_billed=2147483648 | duration_ms=1100 | status=DONE
-- Checking if anyone actually uses the 'export_csv' feature. 
-- Product team thinks it's dead weight.
SELECT 
    count(event_id) as export_count,
    count(distinct user_id) as unique_users,
    count(distinct customer_id) as unique_customers
FROM `nexus-analyst-demo.acme.fact_user_events`
WHERE event_type = 'workflow_export_csv'
  AND event_at >= '2026-04-01';

-- 2026-05-01 15:44:02 | user=nina.patel@acme.io | job_id=bq_0149_er2 | bytes_billed=536870912 | duration_ms=650 | status=DONE
-- Validating data for the SOC2 audit. 
-- List of users with 'Admin' roles in Enterprise accounts that haven't logged in for 90 days.
SELECT 
    u.user_id,
    u.email_domain,
    c.company_name,
    u.last_login_date
FROM `nexus-analyst-demo.acme.dim_users` u
JOIN `nexus-analyst-demo.acme.dim_customers` c ON u.customer_id = c.customer_id
WHERE c.account_tier = 'Enterprise'
  AND u.role = 'Admin'
  AND u.last_login_date < DATE_SUB('2026-05-01', INTERVAL 90 DAY)
  AND u.is_active = TRUE;

-- 2026-05-02 09:00:00 | user=system_service@acme.io | job_id=bq_0150_es3 | bytes_billed=2147483648 | duration_ms=2500 | status=DONE
-- Scheduled daily run: Calculate storage usage vs plan limits.
-- This populates the internal 'Customer Health' dashboard in Looker.
SELECT 
    c.customer_id,
    c.company_name,
    p.storage_gb as quota_gb,
    SUM(i.amount_usd) / 100 as estimated_usage_gb -- Noise: storage isn't in a fact table, making up a proxy
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_plans` p ON c.current_plan_tier = p.plan_tier
JOIN `nexus-analyst-demo.acme.fact_invoices` i ON c.customer_id = i.customer_id
WHERE c.status = 'Active'
GROUP BY 1, 2, 3;

-- 2026-05-02 11:22:15 | user=marcus.wong@acme.io | job_id=bq_0151_ft4 | bytes_billed=1073741824 | duration_ms=1800 | status=DONE
-- Investigating the "Workflow Failure" spike for CloudScale (ID: 552). 
-- They complained about high latency on their webhooks.
SELECT 
    DATE(triggered_at) as run_date,
    status,
    error_code,
    AVG(duration_ms) as avg_latency_ms,
    COUNT(run_id) as total_runs
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE customer_id = 552
  AND triggered_at >= '2026-04-20'
GROUP BY 1, 2, 3
ORDER BY 1 DESC;

-- 2026-05-02 13:10:04 | user=sarah.chen@acme.io | job_id=bq_0152_gh5 | bytes_billed=0 | duration_ms=150 | status=ERROR
-- ERROR: Table name typo. Mentally tired.
SELECT * FROM `nexus-analyst-demo.acme.dim_customer` LIMIT 10;

-- 2026-05-02 13:11:12 | user=sarah.chen@acme.io | job_id=bq_0153_hi6 | bytes_billed=536870912 | duration_ms=450 | status=DONE
-- Corrected table name. Looking at top 10 accounts by MRR for the board deck.
SELECT 
    customer_id, 
    company_name, 
    current_mrr_usd, 
    account_tier 
FROM `nexus-analyst-demo.acme.dim_customers`
WHERE status = 'Active'
ORDER BY current_mrr_usd DESC
LIMIT 10;

-- 2026-05-03 08:45:30 | user=alex.rivera@acme.io | job_id=bq_0154_ij7 | bytes_billed=4294967296 | duration_ms=5200 | status=DONE
-- Calculating Net Revenue Retention (NRR) for Q1 2026 vs Q1 2025.
-- This is a heavy one. Joining subscriptions back to themselves.
WITH q1_2025_mrr AS (
    SELECT 
        customer_id,
        SUM(mrr_usd) as total_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE start_date <= '2025-03-31' 
      AND (end_date IS NULL OR end_date > '2025-03-31')
    GROUP BY 1
),
q1_2026_mrr AS (
    SELECT 
        customer_id,
        SUM(mrr_usd) as total_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE start_date <= '2026-03-31' 
      AND (end_date IS NULL OR end_date > '2026-03-31')
    GROUP BY 1
)
SELECT 
    SUM(curr.total_mrr) / SUM(prev.total_mrr) as nrr_ratio
FROM q1_2025_mrr prev
JOIN q1_2026_mrr curr ON prev.customer_id = curr.customer_id;

-- 2026-05-03 10:15:22 | user=nina.patel@acme.io | job_id=bq_0155_jk8 | bytes_billed=8589934592 | duration_ms=8900 | status=DONE
-- Which regions are driving the most workflow activity? 
-- Joins dim_customers, fact_workflow_runs, and dim_dates.
SELECT 
    c.region,
    d.month_name,
    COUNT(r.run_id) as run_volume,
    COUNT(DISTINCT c.customer_id) as active_customer_count
FROM `nexus-analyst-demo.acme.fact_workflow_runs` r
JOIN `nexus-analyst-demo.acme.dim_customers` c ON r.customer_id = c.customer_id
JOIN `nexus-analyst-demo.acme.dim_dates` d ON DATE(r.triggered_at) = d.date
WHERE d.year = 2026
GROUP BY 1, 2
ORDER BY 3 DESC;

-- 2026-05-03 14:20:11 | user=marcus.wong@acme.io | job_id=bq_0156_kl9 | bytes_billed=2147483648 | duration_ms=1200 | status=DONE
-- CS request: List of users at 'Global Corp' (ID: 102) who haven't performed 'workflow_create' in 30 days.
-- Trying to identify churn risk within the account.
SELECT 
    u.user_id,
    u.role,
    u.last_login_date,
    MAX(e.event_at) as last_create_event
FROM `nexus-analyst-demo.acme.dim_users` u
LEFT JOIN `nexus-analyst-demo.acme.fact_user_events` e ON u.user_id = e.user_id AND e.event_type = 'workflow_create'
WHERE u.customer_id = 102
  AND u.is_active = TRUE
GROUP BY 1, 2, 3
HAVING last_create_event < DATE_SUB('2026-05-03', INTERVAL 30 DAY) OR last_create_event IS NULL;

-- 2026-05-04 09:12:45 | user=system_service@acme.io | job_id=bq_0157_lm0 | bytes_billed=1073741824 | duration_ms=3100 | status=DONE
-- Daily load for AE Commission Tracking. 
-- Joins dim_customers with dim_employees (the AEs).
SELECT 
    e.full_name as ae_name,
    c.company_name,
    c.current_mrr_usd,
    c.signup_date
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_employees` e ON c.ae_employee_id = e.employee_id
WHERE e.team = 'Sales'
  AND c.status = 'Active'
  AND c.signup_date >= '2026-01-01';

-- 2026-05-04 11:30:00 | user=alex.rivera@acme.io | job_id=bq_0158_mn1 | bytes_billed=5368709120 | duration_ms=12400 | status=DONE
-- Deep dive into seat utilization. 
-- licensed vs actual active users in the last 30 days for Enterprise tier.
WITH active_users_30d AS (
    SELECT 
        customer_id,
        COUNT(DISTINCT user_id) as active_count
    FROM `nexus-analyst-demo.acme.dim_users`
    WHERE last_login_date >= DATE_SUB('2026-05-04', INTERVAL 30 DAY)
    GROUP BY 1
)
SELECT 
    c.customer_id,
    c.company_name,
    c.seat_count_licensed,
    COALESCE(a.active_count, 0) as active_users_30d,
    (COALESCE(a.active_count, 0) / NULLIF(c.seat_count_licensed, 0)) as seat_utilization
FROM `nexus-analyst-demo.acme.dim_customers` c
LEFT JOIN active_users_30d a ON c.customer_id = a.customer_id
WHERE c.account_tier = 'Enterprise'
  AND c.status = 'Active'
ORDER BY seat_utilization ASC;

-- 2026-05-04 13:05:10 | user=sarah.chen@acme.io | job_id=bq_0159_op2 | bytes_billed=2147483648 | duration_ms=2100 | status=DONE
-- Looking for "Zombie" accounts. 
-- Business tier accounts with 0 workflow runs in the last month but status='Active'.
SELECT 
    c.customer_id,
    c.company_name,
    c.current_mrr_usd,
    COUNT(r.run_id) as recent_runs
FROM `nexus-analyst-demo.acme.dim_customers` c
LEFT JOIN `nexus-analyst-demo.acme.fact_workflow_runs` r 
    ON c.customer_id = r.customer_id 
    AND r.triggered_at >= '2026-04-01'
WHERE c.current_plan_tier = 'Business'
  AND c.status = 'Active'
GROUP BY 1, 2, 3
HAVING recent_runs = 0;

-- 2026-05-04 15:55:22 | user=nina.patel@acme.io | job_id=bq_0160_pq3 | bytes_billed=1073741824 | duration_ms=900 | status=DONE
-- Checking if the 'storage_gb' quota in dim_plans actually matches what we're billing.
-- Random spot check.
SELECT 
    p.plan_tier,
    p.storage_gb,
    AVG(c.current_mrr_usd) as avg_mrr
FROM `nexus-analyst-demo.acme.dim_plans` p
JOIN `nexus-analyst-demo.acme.dim_customers` c ON p.plan_tier = c.current_plan_tier
GROUP BY 1, 2;

-- 2026-05-04 16:45:10 | user=marcus.wong@acme.io | job_id=bq_0161_qr4 | bytes_billed=0 | duration_ms=200 | status=ERROR
-- ERROR: fact_user_events doesn't have a column named 'customer_name'
SELECT 
    customer_name, 
    COUNT(*) 
FROM `nexus-analyst-demo.acme.fact_user_events` 
GROUP BY 1;

-- 2026-05-04 16:48:12 | user=marcus.wong@acme.io | job_id=bq_0162_st5 | bytes_billed=3221225472 | duration_ms=1450 | status=DONE
-- Fixing the previous error. Joining on customer_id to get the names.
SELECT 
    c.company_name, 
    COUNT(e.event_id) as activity_count
FROM `nexus-analyst-demo.acme.fact_user_events` e
JOIN `nexus-analyst-demo.acme.dim_customers` c ON e.customer_id = c.customer_id
WHERE e.event_at >= '2026-04-01'
GROUP BY 1
ORDER BY 2 DESC
LIMIT 20;

-- 2026-05-05 09:15:44 | user=sarah.chen@acme.io | job_id=bq_0163_uv6 | bytes_billed=5368709120 | duration_ms=4200 | status=DONE
-- NRR calculation for Q1 2026 (Jan 1 to Mar 31).
-- Comparing MRR from the cohort active on 2026-01-01 against their MRR on 2026-04-01.
WITH cohort_start AS (
    SELECT 
        customer_id, 
        mrr_usd as starting_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE is_current = FALSE 
      AND '2026-01-01' BETWEEN start_date AND end_date
),
cohort_end AS (
    SELECT 
        customer_id, 
        mrr_usd as ending_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE (is_current = TRUE AND '2026-04-01' >= start_date)
       OR ('2026-04-01' BETWEEN start_date AND end_date)
)
SELECT 
    SUM(s.starting_mrr) as base_mrr,
    SUM(COALESCE(e.ending_mrr, 0)) as retained_mrr,
    SAFE_DIVIDE(SUM(COALESCE(e.ending_mrr, 0)), SUM(s.starting_mrr)) as nrr_pct
FROM cohort_start s
LEFT JOIN cohort_end e ON s.customer_id = e.customer_id;

-- 2026-05-05 10:22:10 | user=nina.patel@acme.io | job_id=bq_0164_wx7 | bytes_billed=0 | duration_ms=150 | status=ERROR
-- ERROR: Table name `nexus-analyst-demo.acme.fact_runs` not found. Did you mean `fact_workflow_runs`?
SELECT 
    workflow_id, 
    AVG(duration_ms) 
FROM `nexus-analyst-demo.acme.fact_runs` 
GROUP BY 1;

-- 2026-05-05 10:23:05 | user=nina.patel@acme.io | job_id=bq_0165_xy8 | bytes_billed=4294967296 | duration_ms=3100 | status=DONE
-- Re-running with correct table name. Looking for high-latency workflows (> 30s) in Enterprise accounts.
SELECT 
    r.workflow_id,
    c.company_name,
    AVG(r.duration_ms) as avg_duration,
    COUNT(*) as total_runs
FROM `nexus-analyst-demo.acme.fact_workflow_runs` r
JOIN `nexus-analyst-demo.acme.dim_customers` c ON r.customer_id = c.customer_id
WHERE c.account_tier = 'Enterprise'
  AND r.triggered_at >= '2026-04-01'
GROUP BY 1, 2
HAVING avg_duration > 30000
ORDER BY avg_duration DESC;

-- 2026-05-05 11:45:33 | user=jake.muller@acme.io | job_id=bq_0166_yz9 | bytes_billed=1073741824 | duration_ms=850 | status=DONE
-- Quick audit on AE performance for the SF office. 
-- Jake is looking at "Closed Won" (Active) MRR attributed to specific AEs.
SELECT 
    e.full_name as ae_name,
    COUNT(c.customer_id) as account_count,
    SUM(c.current_mrr_usd) as total_mrr
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_employees` e ON c.ae_employee_id = e.employee_id
WHERE e.team = 'Sales' 
  AND e.location = 'San Francisco'
  AND c.status = 'Active'
GROUP BY 1
ORDER BY 3 DESC;

-- 2026-05-05 14:12:01 | user=marcus.wong@acme.io | job_id=bq_0167_za0 | bytes_billed=2147483648 | duration_ms=1200 | status=DONE
-- Viral loop analysis: Which users are the biggest 'inviters'?
-- Exclude internal acme.io domains.
SELECT 
    u.invited_by_user_id,
    inviter.email_domain,
    COUNT(*) as invite_count
FROM `nexus-analyst-demo.acme.dim_users` u
JOIN `nexus-analyst-demo.acme.dim_users` inviter ON u.invited_by_user_id = inviter.user_id
WHERE u.invited_by_user_id IS NOT NULL
  AND inviter.email_domain != 'acme.io'
GROUP BY 1, 2
ORDER BY 3 DESC
LIMIT 10;

-- 2026-05-05 15:30:15 | user=sarah.chen@acme.io | job_id=bq_0168_ab1 | bytes_billed=12884901888 | duration_ms=5600 | status=DONE
-- Identifying potential churn risks: Enterprise customers with > 20% drop in workflow runs month-over-month.
WITH monthly_usage AS (
    SELECT 
        customer_id,
        DATE_TRUNC(triggered_at, MONTH) as run_month,
        COUNT(run_id) as run_count
    FROM `nexus-analyst-demo.acme.fact_workflow_runs`
    WHERE triggered_at >= '2026-01-01'
    GROUP BY 1, 2
),
usage_lag AS (
    SELECT 
        m.customer_id,
        c.company_name,
        m.run_month,
        m.run_count,
        LAG(m.run_count) OVER (PARTITION BY m.customer_id ORDER BY m.run_month) as prev_month_count
    FROM monthly_usage m
    JOIN `nexus-analyst-demo.acme.dim_customers` c ON m.customer_id = c.customer_id
    WHERE c.account_tier = 'Enterprise'
)
SELECT 
    company_name,
    run_month,
    run_count,
    prev_month_count,
    SAFE_DIVIDE(run_count - prev_month_count, prev_month_count) as pct_change
FROM usage_lag
WHERE run_month = '2026-04-01'
  AND SAFE_DIVIDE(run_count - prev_month_count, prev_month_count) <= -0.20;

-- 2026-05-05 16:50:44 | user=nina.patel@acme.io | job_id=bq_0169_bc2 | bytes_billed=536870912 | duration_ms=450 | status=DONE
-- Spot check on a specific invoice issue for "Globex Corp" (CUST-4412). 
-- They claim they were double billed in March.
SELECT 
    invoice_id,
    amount_usd,
    invoice_date,
    period_start,
    period_end,
    status
FROM `nexus-analyst-demo.acme.fact_invoices`
WHERE customer_id = 'CUST-4412'
  AND invoice_date BETWEEN '2026-02-01' AND '2026-04-30'
ORDER BY invoice_date DESC;

-- 2026-05-06 08:30:12 | user=marcus.wong@acme.io | job_id=bq_0170_cd3 | bytes_billed=0 | duration_ms=110 | status=ERROR
-- ERROR: Column `region` does not exist in `fact_user_events`.
SELECT 
    region, 
    COUNT(DISTINCT user_id) 
FROM `nexus-analyst-demo.acme.fact_user_events` 
GROUP BY 1;

-- 2026-05-06 08:31:45 | user=marcus.wong@acme.io | job_id=bq_0171_de4 | bytes_billed=4294967296 | duration_ms=2800 | status=DONE
-- Corrected: Pulling region from dim_customers for event heat map.
SELECT 
    c.region,
    COUNT(DISTINCT e.user_id) as unique_active_users
FROM `nexus-analyst-demo.acme.fact_user_events` e
JOIN `nexus-analyst-demo.acme.dim_customers` c ON e.customer_id = c.customer_id
WHERE e.event_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
GROUP BY 1
ORDER BY 2 DESC;

-- 2026-05-06 10:15:22 | user=sarah.jenkins@acme.io | job_id=bq_0172_ef5 | bytes_billed=10737418240 | duration_ms=5100 | status=DONE
-- Q1 2026 Gross Revenue Retention (GRR) Calc for Board Deck.
-- Looking at starting MRR on Jan 1 vs what remained from those same customers on March 31.
WITH cohort_jan AS (
    SELECT 
        customer_id,
        mrr_usd as starting_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE is_current = TRUE 
      AND start_date <= '2026-01-01'
      AND (end_date > '2026-01-01' OR end_date IS NULL)
),
cohort_march AS (
    SELECT 
        customer_id,
        mrr_usd as ending_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE is_current = TRUE 
      AND start_date <= '2026-03-31'
      AND (end_date > '2026-03-31' OR end_date IS NULL)
)
SELECT 
    SUM(j.starting_mrr) as total_jan_mrr,
    SUM(LEAST(j.starting_mrr, COALESCE(m.ending_mrr, 0))) as retained_mrr,
    SAFE_DIVIDE(SUM(LEAST(j.starting_mrr, COALESCE(m.ending_mrr, 0))), SUM(j.starting_mrr)) as grr_pct
FROM cohort_jan j
LEFT JOIN cohort_march m ON j.customer_id = m.customer_id;

-- 2026-05-06 11:42:01 | user=liam.chen@acme.io | job_id=bq_0173_fg6 | bytes_billed=2147483648 | duration_ms=1200 | status=DONE
-- Investigating "System Overload" errors for high-volume Enterprise users.
-- CUST-8812 (CyberDyne Systems) and CUST-1099 (Initech) reported timeouts.
SELECT 
    customer_id,
    error_code,
    COUNT(*) as error_count,
    AVG(duration_ms) as avg_duration
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE triggered_at >= '2026-04-01'
  AND customer_id IN ('CUST-8812', 'CUST-1099')
  AND status = 'FAILED'
GROUP BY 1, 2
ORDER BY 3 DESC;

-- 2026-05-06 13:05:10 | user=dave.miller@acme.io | job_id=bq_0174_gh7 | bytes_billed=0 | duration_ms=95 | status=ERROR
-- ERROR: Table `nexus-analyst-demo.acme.dim_workflows` not found. 
-- Dave trying to join to a table that doesn't exist in the FLAT schema. Use fact_workflow_runs instead.
SELECT 
    w.workflow_name,
    COUNT(r.run_id) 
FROM `nexus-analyst-demo.acme.dim_workflows` w
JOIN `nexus-analyst-demo.acme.fact_workflow_runs` r ON w.workflow_id = r.workflow_id
GROUP BY 1;

-- 2026-05-06 14:22:55 | user=eliza.bennet@acme.io | job_id=bq_0175_hi8 | bytes_billed=536870912 | duration_ms=890 | status=DONE
-- Monthly AE performance check for EMEA. 
-- Checking current_mrr_usd handled by AEs hired before 2025.
SELECT 
    e.full_name as ae_name,
    COUNT(c.customer_id) as account_count,
    SUM(c.current_mrr_usd) as total_managed_mrr
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_employees` e ON c.ae_employee_id = e.employee_id
WHERE e.location = 'Amsterdam'
  AND e.hire_date < '2025-01-01'
  AND c.status = 'Active'
GROUP BY 1
ORDER BY 3 DESC;

-- 2026-05-07 09:10:04 | user=nina.patel@acme.io | job_id=bq_0176_ij9 | bytes_billed=8589934592 | duration_ms=3400 | status=DONE
-- Identify 'Under-utilized' Business Tier accounts for expansion/renewal risk.
-- Seats licensed > 50 but active users in last 30 days < 10.
WITH active_users AS (
    SELECT 
        customer_id,
        COUNT(DISTINCT user_id) as mau_count
    FROM `nexus-analyst-demo.acme.fact_user_events`
    WHERE event_at >= DATE_SUB('2026-05-04', INTERVAL 30 DAY)
    GROUP BY 1
)
SELECT 
    c.company_name,
    c.seat_count_licensed,
    COALESCE(a.mau_count, 0) as active_users_30d,
    c.current_mrr_usd,
    e.full_name as csm_owner
FROM `nexus-analyst-demo.acme.dim_customers` c
LEFT JOIN active_users a ON c.customer_id = a.customer_id
LEFT JOIN `nexus-analyst-demo.acme.dim_employees` e ON c.csm_employee_id = e.employee_id
WHERE c.current_plan_tier = 'Business'
  AND c.status = 'Active'
  AND COALESCE(a.mau_count, 0) < (c.seat_count_licensed * 0.2)
ORDER BY c.current_mrr_usd DESC;

-- 2026-05-07 10:45:12 | user=finance-bot@acme.io | job_id=bq_0177_jk0 | bytes_billed=1073741824 | duration_ms=620 | status=DONE
-- Automated daily sweep for past-due invoices > $5000.
SELECT 
    i.invoice_id,
    c.company_name,
    i.amount_usd,
    i.invoice_date,
    DATE_DIFF('2026-05-07', i.invoice_date, DAY) as days_overdue
FROM `nexus-analyst-demo.acme.fact_invoices` i
JOIN `nexus-analyst-demo.acme.dim_customers` c ON i.customer_id = c.customer_id
WHERE i.status = 'UNPAID'
  AND i.amount_usd > 5000
  AND i.invoice_date < DATE_SUB('2026-05-07', INTERVAL 30 DAY);

-- 2026-05-07 15:30:00 | user=marcus.wong@acme.io | job_id=bq_0178_kl1 | bytes_billed=17179869184 | duration_ms=12400 | status=DONE
-- Deep dive into step_count vs duration_ms for top 5% of runs.
-- Optimization research for infra team.
SELECT 
    PERCENTILE_CONT(duration_ms, 0.95) OVER() as p95_duration,
    PERCENTILE_CONT(step_count, 0.95) OVER() as p95_steps,
    status,
    COUNT(*) as run_count
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE triggered_at >= '2026-04-01'
GROUP BY 1, 2, 3;

-- 2026-05-08 08:12:33 | user=sarah.jenkins@acme.io | job_id=bq_0179_lm2 | bytes_billed=4294967296 | duration_ms=2100 | status=DONE
-- Net Revenue Retention (NRR) for Q1.
-- Includes expansion revenue and contraction/churn.
WITH q4_end AS (
    SELECT SUM(mrr_usd) as mrr FROM `nexus-analyst-demo.acme.fact_subscriptions` 
    WHERE is_current = TRUE AND start_date <= '2025-12-31' AND (end_date > '2025-12-31' OR end_date IS NULL)
),
q1_end AS (
    -- Only looking at customers who existed in Q4 to see their movement
    SELECT SUM(s.mrr_usd) as mrr 
    FROM `nexus-analyst-demo.acme.fact_subscriptions` s
    WHERE s.is_current = TRUE 
      AND s.start_date <= '2026-03-31' 
      AND (s.end_date > '2026-03-31' OR s.end_date IS NULL)
      AND s.customer_id IN (
          SELECT customer_id FROM `nexus-analyst-demo.acme.fact_subscriptions` 
          WHERE is_current = TRUE AND start_date <= '2025-12-31' AND (end_date > '2025-12-31' OR end_date IS NULL)
      )
)
SELECT 
    q4_end.mrr as starting_mrr,
    q1_end.mrr as ending_mrr_from_same_base,
    SAFE_DIVIDE(q1_end.mrr, q4_end.mrr) as nrr_pct
FROM q4_end, q1_end;

-- 2026-05-08 10:45:12 | user=david.chen@acme.io | job_id=bq_0180_np4 | bytes_billed=8589934592 | duration_ms=4500 | status=DONE
-- Audit: Enterprise seat utilization check. 
-- Identifying accounts where licensed seats < actual active users.
SELECT 
    c.company_name,
    c.seat_count_licensed,
    COUNT(u.user_id) as active_user_count,
    (COUNT(u.user_id) - c.seat_count_licensed) as overage_seats
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_users` u ON c.customer_id = u.customer_id
WHERE c.current_plan_tier = 'Enterprise'
  AND u.is_active = TRUE
GROUP BY 1, 2
HAVING active_user_count > c.seat_count_licensed;

-- 2026-05-08 11:20:05 | user=jason.lee@acme.io | job_id=bq_0181_ox5 | bytes_billed=0 | duration_ms=150 | status=ERROR
-- ERROR: Table name typo. Troubleshooting run failures.
SELECT * FROM `nexus-analyst-demo.acme.fact_workflow_run` LIMIT 100;

-- 2026-05-08 13:05:44 | user=priya.sharma@acme.io | job_id=bq_0182_pz6 | bytes_billed=21474836480 | duration_ms=8900 | status=DONE
-- Product Adoption: Daily active events per plan tier for May so far.
-- Need to see if 'Business' users are hitting more webhooks than 'Pro'.
SELECT 
    d.date,
    c.current_plan_tier,
    COUNT(e.event_id) as total_events,
    COUNT(DISTINCT e.user_id) as dau
FROM `nexus-analyst-demo.acme.fact_user_events` e
JOIN `nexus-analyst-demo.acme.dim_customers` c ON e.customer_id = c.customer_id
JOIN `nexus-analyst-demo.acme.dim_dates` d ON EXTRACT(DATE FROM e.event_at) = d.date
WHERE d.month_name = 'May' AND d.year = 2026
GROUP BY 1, 2
ORDER BY 1 ASC, 3 DESC;

-- 2026-05-09 09:15:22 | user=kevin.peters@acme.io | job_id=bq_0183_qa7 | bytes_billed=1073741824 | duration_ms=950 | status=DONE
-- Sales Ops: List of SMB customers without an assigned AE (ae_employee_id IS NULL).
-- Looking for expansion leads.
SELECT 
    customer_id, 
    company_name, 
    current_mrr_usd, 
    signup_date 
FROM `nexus-analyst-demo.acme.dim_customers` 
WHERE account_tier = 'SMB' 
  AND ae_employee_id IS NULL 
  AND status = 'ACTIVE'
ORDER BY current_mrr_usd DESC;

-- 2026-05-09 14:42:10 | user=sarah.jenkins@acme.io | job_id=bq_0184_rb8 | bytes_billed=53687091200 | duration_ms=31200 | status=DONE
-- Churn and Expansion Analysis (The "Wall of Revenue").
-- Calculating ARR movements: New, Expansion, Contraction, Churn.
WITH monthly_mrr AS (
    SELECT 
        customer_id,
        DATE_TRUNC(date, MONTH) as mrr_month,
        SUM(mrr_usd) as mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    CROSS JOIN `nexus-analyst-demo.acme.dim_dates`
    WHERE date BETWEEN start_date AND COALESCE(end_date, '2026-12-31')
      AND is_business_day = TRUE
      AND day_of_week = 'Monday' -- Sample once a week to save compute
    GROUP BY 1, 2
),
mrr_lag AS (
    SELECT 
        customer_id,
        mrr_month,
        mrr,
        LAG(mrr) OVER(PARTITION BY customer_id ORDER BY mrr_month) as prev_mrr
    FROM monthly_mrr
)
SELECT 
    mrr_month,
    SUM(CASE WHEN prev_mrr IS NULL THEN mrr ELSE 0 END) as new_revenue,
    SUM(CASE WHEN mrr > prev_mrr THEN (mrr - prev_mrr) ELSE 0 END) as expansion_revenue,
    SUM(CASE WHEN mrr < prev_mrr AND mrr > 0 THEN (mrr - prev_mrr) ELSE 0 END) as contraction_revenue,
    SUM(CASE WHEN mrr = 0 AND prev_mrr > 0 THEN -prev_mrr ELSE 0 END) as churn_revenue
FROM mrr_lag
WHERE mrr_month >= '2025-01-01'
GROUP BY 1
ORDER BY 1 DESC;

-- 2026-05-10 10:01:18 | user=marcus.wong@acme.io | job_id=bq_0185_sc9 | bytes_billed=3221225472 | duration_ms=1800 | status=DONE
-- Infra: Check storage_gb limits vs actual. Only for Enterprise/Business.
-- Joining dim_plans to get the quota.
SELECT 
    c.company_name,
    p.plan_tier,
    p.storage_gb as quota_gb,
    -- Simulating usage check from customer metadata if we had it, 
    -- but for now just auditing plan distribution.
    COUNT(u.user_id) as seat_count
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_plans` p ON c.current_plan_tier = p.plan_tier
JOIN `nexus-analyst-demo.acme.dim_users` u ON c.customer_id = u.customer_id
WHERE p.plan_tier IN ('Business', 'Enterprise')
GROUP BY 1, 2, 3;

-- 2026-05-10 11:30:00 | user=elena.vladimir@acme.io | job_id=bq_0186_td0 | bytes_billed=12884901888 | duration_ms=4200 | status=DONE
-- Finance: Invoice collection rate.
-- Amount paid vs amount invoiced by quarter.
SELECT 
    d.year,
    d.quarter,
    SUM(i.amount_usd) as total_invoiced,
    SUM(CASE WHEN i.status = 'PAID' THEN i.amount_usd ELSE 0 END) as total_collected,
    SAFE_DIVIDE(SUM(CASE WHEN i.status = 'PAID' THEN i.amount_usd ELSE 0 END), SUM(i.amount_usd)) as collection_rate
FROM `nexus-analyst-demo.acme.fact_invoices` i
JOIN `nexus-analyst-demo.acme.dim_dates` d ON i.invoice_date = d.date
WHERE i.invoice_date < '2026-04-01'
GROUP BY 1, 2
ORDER BY 1 DESC, 2 DESC;

-- 2026-05-10 16:55:21 | user=jason.lee@acme.io | job_id=bq_0187_ue1 | bytes_billed=42949672960 | duration_ms=15600 | status=DONE
-- Debugging specific workflow latency spike for customer 'C-9902'.
SELECT 
    run_id,
    workflow_id,
    triggered_at,
    duration_ms,
    step_count,
    status
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE customer_id = 'C-9902' 
  AND triggered_at > '2026-05-01'
ORDER BY duration_ms DESC
LIMIT 50;

-- 2026-05-11 09:12:44 | user=olivia.duarte@acme.io | job_id=bq_0188_vf2 | bytes_billed=10737418240 | duration_ms=2100 | status=DONE
-- Product: Monthly Active Users (MAU) by Customer Industry.
-- Looking for "stickiness" signals in the Healthcare and Fintech segments for the Q2 roadmap.
SELECT 
    c.industry,
    d.month_name,
    COUNT(DISTINCT e.user_id) as mau_count
FROM `nexus-analyst-demo.acme.fact_user_events` e
JOIN `nexus-analyst-demo.acme.dim_customers` c ON e.customer_id = c.customer_id
JOIN `nexus-analyst-demo.acme.dim_dates` d ON DATE(e.event_at) = d.date
WHERE d.year = 2026 AND d.month <= 4
  AND c.industry IN ('Fintech', 'Healthcare', 'E-commerce')
GROUP BY 1, 2
ORDER BY 2, 3 DESC;

-- 2026-05-11 10:05:01 | user=chen.wei@acme.io | job_id=bq_0189_wg3 | bytes_billed=0 | duration_ms=45 | status=ERROR
-- ERROR: Table name typo. 'fact_workflow_run' instead of 'fact_workflow_runs'.
SELECT * FROM `nexus-analyst-demo.acme.fact_workflow_run` WHERE customer_id = 'C-4412' LIMIT 10;

-- 2026-05-11 10:05:45 | user=chen.wei@acme.io | job_id=bq_0190_xh4 | bytes_billed=5368709120 | duration_ms=3100 | status=DONE
-- Retrying workflow error analysis for customer C-4412 (MedTech Solutions).
-- They reported a spike in 'ERR_TIMEOUT_05' codes yesterday.
SELECT 
    error_code,
    COUNT(*) as incident_count,
    AVG(duration_ms) as avg_latency
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE customer_id = 'C-4412'
  AND triggered_at >= '2026-05-10 00:00:00'
  AND status = 'FAILED'
GROUP BY 1
ORDER BY 2 DESC;

-- 2026-05-11 14:20:10 | user=sarah.jenkins@acme.io | job_id=bq_0191_yi5 | bytes_billed=85899345920 | duration_ms=28400 | status=DONE
-- Executive Dashboard: Q1 2026 NRR (Net Revenue Retention) calculation.
-- Complex CTE to track cohort expansion and contraction.
WITH cohort_jan AS (
    SELECT customer_id, mrr_usd as mrr_start
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE is_current = FALSE 
      AND '2026-01-01' BETWEEN start_date AND end_date
),
cohort_mar AS (
    SELECT customer_id, mrr_usd as mrr_end
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE is_current = TRUE 
      OR ('2026-03-31' BETWEEN start_date AND end_date)
)
SELECT 
    SUM(j.mrr_start) as total_starting_mrr,
    SUM(COALESCE(m.mrr_end, 0)) as total_retained_mrr,
    SAFE_DIVIDE(SUM(COALESCE(m.mrr_end, 0)), SUM(j.mrr_start)) * 100 as nrr_pct
FROM cohort_jan j
LEFT JOIN cohort_mar m ON j.customer_id = m.customer_id;

-- 2026-05-11 15:45:33 | user=marcus.wong@acme.io | job_id=bq_0192_zj6 | bytes_billed=21474836480 | duration_ms=8900 | status=DONE
-- Infra: Top 10 heavy hitters by workflow volume vs their quota.
-- Checking for overages that need to be pushed to Sales for 'Business' tier upgrades.
SELECT 
    c.company_name,
    c.customer_id,
    p.workflow_run_quota_per_month as quota,
    COUNT(r.run_id) as actual_runs_may_to_date,
    (COUNT(r.run_id) / p.workflow_run_quota_per_month) * 100 as quota_utilization_pct
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_plans` p ON c.current_plan_tier = p.plan_tier
JOIN `nexus-analyst-demo.acme.fact_workflow_runs` r ON c.customer_id = r.customer_id
WHERE r.triggered_at >= '2026-05-01'
  AND c.status = 'Active'
  AND p.plan_tier != 'Enterprise' -- Enterprise is unlimited
GROUP BY 1, 2, 3
HAVING actual_runs_may_to_date > (p.workflow_run_quota_per_month * 0.8)
ORDER BY 5 DESC;

-- 2026-05-12 08:30:12 | user=elena.vladimir@acme.io | job_id=bq_0193_ak7 | bytes_billed=4294967296 | duration_ms=1200 | status=DONE
-- Sales: AE performance - ARR booked by AE in 2026 YTD.
-- Filtered for MM (Mid-Market) and Ent (Enterprise) accounts.
SELECT 
    e.full_name as ae_name,
    c.account_tier,
    SUM(c.current_mrr_usd * 12) as total_arr_managed,
    COUNT(DISTINCT c.customer_id) as account_count
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_employees` e ON c.ae_employee_id = e.employee_id
WHERE c.status = 'Active'
  AND c.account_tier IN ('MM', 'Ent')
  AND e.team = 'Sales'
GROUP BY 1, 2
ORDER BY 3 DESC;

-- 2026-05-12 09:15:44 | user=jason.lee@acme.io | job_id=bq_0194_bl8 | bytes_billed=1073741824 | duration_ms=950 | status=DONE
-- Debug: Checking seat count discrepancy for customer 'C-1029' (Global Logistics Corp).
-- They claim they are paying for 250 but see only 220 active in UI.
SELECT 
    c.company_name,
    c.seat_count_licensed,
    COUNT(u.user_id) as provisioned_users,
    SUM(CASE WHEN u.is_active THEN 1 ELSE 0 END) as active_users
FROM `nexus-analyst-demo.acme.dim_customers` c
LEFT JOIN `nexus-analyst-demo.acme.dim_users` u ON c.customer_id = u.customer_id
WHERE c.customer_id = 'C-1029'
GROUP BY 1, 2;

-- 2026-05-12 11:02:19 | user=olivia.duarte@acme.io | job_id=bq_0195_cm9 | bytes_billed=32212254720 | duration_ms=14200 | status=DONE
-- Product: Adoption of "Custom Webhook" event type.
-- Want to see if this correlates with higher NRR/Lower Churn.
WITH webhook_users AS (
    SELECT DISTINCT customer_id
    FROM `nexus-analyst-demo.acme.fact_user_events`
    WHERE event_type = 'webhook_configured'
      AND event_at < '2026-04-01'
)
SELECT 
    CASE WHEN w.customer_id IS NOT NULL THEN 'Used Webhooks' ELSE 'No Webhooks' END as feature_segment,
    c.current_plan_tier,
    AVG(c.current_mrr_usd) as avg_mrr,
    COUNT(c.customer_id) as customer_count
FROM `nexus-analyst-demo.acme.dim_customers` c
LEFT JOIN webhook_users w ON c.customer_id = w.customer_id
WHERE c.status = 'Active'
GROUP BY 1, 2
ORDER BY 1, 3 DESC;

-- 2026-05-12 13:44:02 | user=sarah.jenkins@acme.io | job_id=bq_0196_dn0 | bytes_billed=6442450944 | duration_ms=3500 | status=DONE
-- Finance: Aging Invoices Audit.
-- List all invoices more than 30 days overdue as of today.
SELECT 
    c.company_name,
    i.invoice_id,
    i.amount_usd,
    i.invoice_date,
    DATE_DIFF('2026-05-12', i.invoice_date, DAY) as days_overdue,
    e.full_name as csm_owner
FROM `nexus-analyst-demo.acme.fact_invoices` i
JOIN `nexus-analyst-demo.acme.dim_customers` c ON i.customer_id = c.customer_id
JOIN `nexus-analyst-demo.acme.dim_employees` e ON c.csm_employee_id = e.employee_id
WHERE i.status = 'OPEN'
  AND i.invoice_date < '2026-04-12'
ORDER BY days_overdue DESC;

-- 2026-02-14 09:12:44 | user=mark.thompson@acme.io | job_id=bq_0201_xa2 | status=ERROR | error=Not found: Table nexus-analyst-demo.acme.customers_dim
-- Marketing: Checking acquisition channel performance for Q1 campaign planning. 
-- Trying to see which channels are bringing in 'Business' tier leads.
SELECT acquisition_channel, COUNT(*) 
FROM `nexus-analyst-demo.acme.customers_dim` 
WHERE signup_date >= '2026-01-01' 
GROUP BY 1;

-- 2026-02-14 09:13:30 | user=mark.thompson@acme.io | job_id=bq_0202_yb3 | bytes_billed=1073741824 | duration_ms=800 | status=DONE
-- Fixed table name.
SELECT 
    acquisition_channel, 
    current_plan_tier,
    COUNT(customer_id) as signup_count,
    SUM(current_mrr_usd) as total_mrr
FROM `nexus-analyst-demo.acme.dim_customers`
WHERE signup_date BETWEEN '2026-01-01' AND '2026-02-13'
GROUP BY 1, 2
ORDER BY 4 DESC;

-- 2026-02-18 16:20:11 | user=olivia.duarte@acme.io | job_id=bq_0205_zc4 | bytes_billed=42949672960 | duration_ms=18900 | status=DONE
-- Product/Growth: Net Revenue Retention (NRR) Cohort Analysis for Jan 2025 cohort.
-- Measuring MRR of customers who joined in Jan 2025 as of today vs their starting MRR.
WITH cohort_jan_2025 AS (
    SELECT 
        customer_id, 
        current_mrr_usd as starting_mrr
    FROM `nexus-analyst-demo.acme.dim_customers`
    WHERE signup_date BETWEEN '2025-01-01' AND '2025-01-31'
),
current_stats AS (
    SELECT 
        s.customer_id,
        SUM(s.mrr_usd) as current_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions` s
    WHERE s.is_current = TRUE
    GROUP BY 1
)
SELECT 
    COUNT(c.customer_id) as original_cohort_size,
    SUM(c.starting_mrr) as cohort_start_mrr,
    SUM(COALESCE(cs.current_mrr, 0)) as cohort_current_mrr,
    (SUM(COALESCE(cs.current_mrr, 0)) / SUM(c.starting_mrr)) * 100 as nrr_pct
FROM cohort_jan_2025 c
LEFT JOIN current_stats cs ON c.customer_id = cs.customer_id;

-- 2026-03-05 10:45:12 | user=sarah.jenkins@acme.io | job_id=bq_0210_kd1 | bytes_billed=12884901888 | duration_ms=4200 | status=DONE
-- CS: Identifying 'Power Users' at SkyLine Systems (C-4991) for the upcoming QBR.
-- Defined as users with > 50 workflow runs in the last 30 days.
SELECT 
    u.user_id,
    u.email_domain,
    COUNT(fwr.run_id) as total_runs,
    AVG(fwr.duration_ms) as avg_runtime_ms
FROM `nexus-analyst-demo.acme.dim_users` u
JOIN `nexus-analyst-demo.acme.fact_workflow_runs` fwr ON u.user_id = fwr.triggered_by
WHERE u.customer_id = 'C-4991'
  AND fwr.triggered_at >= DATE_SUB('2026-03-05', INTERVAL 30 DAY)
GROUP BY 1, 2
HAVING total_runs > 50
ORDER BY total_runs DESC;

-- 2026-03-12 14:02:59 | user=david.chen@acme.io | job_id=bq_0215_le9 | bytes_billed=85899345920 | duration_ms=21000 | status=DONE
-- Engineering: Load analysis. Checking if Enterprise customers are running significantly 
-- longer/heavier workflows than Pro/Business.
SELECT 
    c.current_plan_tier,
    COUNT(fwr.run_id) as run_volume,
    AVG(fwr.duration_ms) as avg_duration,
    APPROX_QUANTILES(fwr.duration_ms, 100)[OFFSET(95)] as p95_duration,
    SUM(fwr.step_count) as total_steps_executed
FROM `nexus-analyst-demo.acme.fact_workflow_runs` fwr
JOIN `nexus-analyst-demo.acme.dim_customers` c ON fwr.customer_id = c.customer_id
WHERE fwr.triggered_at >= '2026-03-01'
GROUP BY 1;

-- 2026-03-28 09:15:22 | user=jessica.wu@acme.io | job_id=bq_0222_mf4 | bytes_billed=5368709120 | duration_ms=2100 | status=DONE
-- Sales: Upsell Leads. Pro tier customers currently over 90% of their workflow quota.
-- dim_plans.workflow_run_quota_per_month for 'Pro' is 10k.
WITH monthly_usage AS (
    SELECT 
        customer_id,
        COUNT(run_id) as runs_this_month
    FROM `nexus-analyst-demo.acme.fact_workflow_runs`
    WHERE triggered_at >= '2026-03-01'
    GROUP BY 1
)
SELECT 
    c.company_name,
    c.customer_id,
    c.current_mrr_usd,
    mu.runs_this_month,
    p.workflow_run_quota_per_month,
    (mu.runs_this_month / p.workflow_run_quota_per_month) * 100 as quota_utilization_pct
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN monthly_usage mu ON c.customer_id = mu.customer_id
JOIN `nexus-analyst-demo.acme.dim_plans` p ON c.current_plan_tier = p.plan_tier
WHERE c.current_plan_tier = 'Pro'
  AND (mu.runs_this_month / p.workflow_run_quota_per_month) > 0.90
ORDER BY quota_utilization_pct DESC;

-- 2026-04-10 11:30:05 | user=olivia.duarte@acme.io | job_id=bq_0230_ng7 | bytes_billed=21474836480 | duration_ms=11000 | status=DONE
-- Finance: Revenue Concentration by CSM. 
-- Who is managing the most ARR and what is the health (active users)?
SELECT 
    e.full_name as csm_name,
    COUNT(c.customer_id) as accounts_managed,
    SUM(c.current_mrr_usd * 12) as arr_managed,
    AVG(CASE WHEN c.status = 'Active' THEN 1 ELSE 0 END) as portfolio_health_pct,
    SUM(c.seat_count_licensed) as total_seats
FROM `nexus-analyst-demo.acme.dim_employees` e
LEFT JOIN `nexus-analyst-demo.acme.dim_customers` c ON e.employee_id = c.csm_employee_id
WHERE e.team = 'Customer Success'
  AND e.is_active = TRUE
GROUP BY 1
ORDER BY arr_managed DESC;

-- 2026-04-15 15:22:18 | user=sarah.jenkins@acme.io | job_id=bq_0235_ph2 | bytes_billed=3221225472 | duration_ms=1500 | status=DONE
-- CS: Quick look at high-error workflows for TechFlow (C-2012).
-- Customer reported 'instability' in their Slack integrations.
SELECT 
    error_code,
    COUNT(*) as error_count,
    MIN(triggered_at) as first_seen,
    MAX(triggered_at) as last_seen
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE customer_id = 'C-2012'
  AND status = 'FAILED'
  AND triggered_at > DATE_SUB('2026-04-15', INTERVAL 7 DAY)
GROUP BY 1
ORDER BY error_count DESC;

-- 2026-04-20 08:55:10 | user=system_service_account@acme.io | job_id=bq_scheduled_001 | bytes_billed=107374182400 | duration_ms=45000 | status=DONE
-- Scheduled: Monthly ARR Rollup per Region.
SELECT 
    d.year,
    d.month_name,
    c.region,
    SUM(s.mrr_usd * 12) as total_arr
FROM `nexus-analyst-demo.acme.fact_subscriptions` s
JOIN `nexus-analyst-demo.acme.dim_customers` c ON s.customer_id = c.customer_id
JOIN `nexus-analyst-demo.acme.dim_dates` d ON s.start_date = d.date
WHERE s.is_current = TRUE
GROUP BY 1, 2, 3
ORDER BY 1 DESC, 4 DESC;

-- 2026-04-22 10:15:44 | user=marcus.wong@acme.io | job_id=bq_0240_az1 | bytes_billed=5368709120 | duration_ms=2100 | status=DONE
-- Marketing: Channel efficiency for Q1 2026. 
-- Checking if 'Inbound - Content' leads from late 2025 are converting to Business tier.
SELECT 
    c.acquisition_channel,
    COUNT(DISTINCT c.customer_id) as total_customers,
    SUM(c.current_mrr_usd) as total_mrr,
    AVG(c.seat_count_licensed) as avg_seats
FROM `nexus-analyst-demo.acme.dim_customers` c
WHERE c.signup_date BETWEEN '2025-10-01' AND '2026-03-31'
  AND c.status = 'Active'
GROUP BY 1
ORDER BY total_mrr DESC;

-- 2026-04-22 14:02:11 | user=elena.vlad@acme.io | job_id=bq_0242_kp9 | bytes_billed=1073741824 | duration_ms=850 | status=ERROR
-- Product: Daily active users per customer.
-- ERROR: Table name typo 'dim_user' instead of 'dim_users'.
SELECT 
    customer_id, 
    COUNT(DISTINCT user_id) as active_count
FROM `nexus-analyst-demo.acme.dim_user` 
WHERE is_active = TRUE
GROUP BY 1;

-- 2026-04-23 09:12:05 | user=liam.o-reilly@acme.io | job_id=bq_0250_rt3 | bytes_billed=85899345920 | duration_ms=32000 | status=DONE
-- Finance: Net Revenue Retention (NRR) Calculation.
-- Comparing cohort from April 2025 to their value in April 2026.
WITH cohort_2025 AS (
    SELECT 
        customer_id,
        mrr_usd as mrr_start
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE start_date <= '2025-04-30'
      AND (end_date > '2025-04-30' OR end_date IS NULL)
      AND is_current = FALSE
),
current_val AS (
    SELECT 
        customer_id,
        current_mrr_usd as mrr_now,
        status
    FROM `nexus-analyst-demo.acme.dim_customers`
)
SELECT 
    SUM(c.mrr_start) as original_mrr,
    SUM(CASE WHEN cv.status = 'Active' THEN cv.mrr_now ELSE 0 END) as retained_mrr,
    (SUM(CASE WHEN cv.status = 'Active' THEN cv.mrr_now ELSE 0 END) / SUM(c.mrr_start)) * 100 as nrr_pct
FROM cohort_2025 c
JOIN current_val cv ON c.customer_id = cv.customer_id;

-- 2026-04-23 16:45:30 | user=david.chen@acme.io | job_id=bq_0255_gh1 | bytes_billed=12884901888 | duration_ms=4200 | status=DONE
-- Eng: Latency analysis for the 'Shopify Sync' workflow (WF-9921). 
-- Looking for P95 spikes that might correlate with the Kafka lag on the 20th.
SELECT 
    TIMESTAMP_TRUNC(triggered_at, HOUR) as hour_bucket,
    COUNT(*) as run_count,
    PERCENTILE_CONT(duration_ms, 0.95) OVER(PARTITION BY TIMESTAMP_TRUNC(triggered_at, HOUR)) as p95_duration,
    AVG(duration_ms) as avg_duration
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE workflow_id = 'WF-9921'
  AND triggered_at BETWEEN '2026-04-19' AND '2026-04-21'
ORDER BY 1 ASC;

-- 2026-04-24 11:10:02 | user=sam.walker@acme.io | job_id=bq_0258_ll2 | bytes_billed=2147483648 | duration_ms=900 | status=DONE
-- Sales: Upsell targets in the 'Free' tier. 
-- Accounts with >5 users are hitting friction. Let's find Business tier candidates.
SELECT 
    c.company_name,
    c.customer_id,
    COUNT(u.user_id) as total_users,
    c.signup_date
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_users` u ON c.customer_id = u.customer_id
WHERE c.current_plan_tier = 'Free'
  AND c.status = 'Active'
GROUP BY 1, 2, 4
HAVING total_users > 5
ORDER BY total_users DESC;

-- 2026-04-25 08:33:19 | user=sophia.martinez@acme.io | job_id=bq_0260_qw4 | bytes_billed=42949672960 | duration_ms=15400 | status=DONE
-- CS: Usage audit for Health Check prep. TechFlow (C-2012) and Velocity Labs (C-1005).
-- Need to see if execution volume matches seat growth.
SELECT 
    c.company_name,
    d.month_name,
    c.seat_count_licensed,
    COUNT(w.run_id) as total_runs,
    COUNT(DISTINCT w.workflow_id) as active_workflows
FROM `nexus-analyst-demo.acme.dim_customers` c
LEFT JOIN `nexus-analyst-demo.acme.fact_workflow_runs` w ON c.customer_id = w.customer_id
LEFT JOIN `nexus-analyst-demo.acme.dim_dates` d ON DATE(w.triggered_at) = d.date
WHERE c.customer_id IN ('C-2012', 'C-1005')
  AND d.year = 2026
GROUP BY 1, 2, 3
ORDER BY 1, 2;

-- 2026-04-27 13:12:44 | user=nina.gupta@acme.io | job_id=bq_0265_xx9 | bytes_billed=2147483648 | duration_ms=1100 | status=ERROR
-- Finance: Monthly Invoice check.
-- ERROR: project-id 'nexus-analyst-demo' is correct, but misspelled table as 'fact_invoces'.
SELECT SUM(amount_usd) 
FROM `nexus-analyst-demo.acme.fact_invoces` 
WHERE status = 'PAID' 
  AND invoice_date > '2026-01-01';

-- 2026-04-28 10:20:15 | user=olivia.duarte@acme.io | job_id=bq_0270_pl5 | bytes_billed=10737418240 | duration_ms=3500 | status=DONE
-- Finance: MRR by industry for Board Deck.
-- Breaking down Enterprise vs Business vs Pro.
SELECT 
    industry,
    current_plan_tier,
    COUNT(customer_id) as account_count,
    SUM(current_mrr_usd) as mrr
FROM `nexus-analyst-demo.acme.dim_customers`
WHERE status = 'Active'
GROUP BY 1, 2
ORDER BY mrr DESC;

-- 2026-04-30 17:05:59 | user=system_service_account@acme.io | job_id=bq_scheduled_005 | bytes_billed=53687091200 | duration_ms=18000 | status=DONE
-- Scheduled: Syncing dim_customers to dim_employees for CSM mapping updates.
-- Checking for orphaned accounts with inactive CSMs.
SELECT 
    c.customer_id,
    c.company_name,
    e.full_name as current_csm,
    e.is_active as csm_still_here
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_employees` e ON c.csm_employee_id = e.employee_id
WHERE e.is_active = FALSE
  AND c.status = 'Active';

-- 2026-05-01 09:15:22 | user=marcus.wong@acme.io | job_id=bq_0280_nm2 | bytes_billed=3221225472 | duration_ms=1200 | status=DONE
-- Marketing: User Event Funnel check. 
-- How many users invited in April actually logged in?
SELECT 
    u.customer_id,
    COUNT(u.user_id) as invited_users,
    COUNT(CASE WHEN u.last_login_date IS NOT NULL THEN 1 END) as activated_users
FROM `nexus-analyst-demo.acme.dim_users` u
WHERE u.signup_date BETWEEN '2026-04-01' AND '2026-04-30'
GROUP BY 1
HAVING invited_users > 0;

-- 2026-05-02 11:44:03 | user=sarah.jenkins@acme.io | job_id=bq_0285_tr4 | bytes_billed=1073741824 | duration_ms=500 | status=DONE
-- CS: Quick seat count verify for customer 'C-5582' before renewal call.
SELECT company_name, seat_count_licensed, current_plan_tier, current_mrr_usd
FROM `nexus-analyst-demo.acme.dim_customers`
WHERE customer_id = 'C-5582';

-- 2026-05-03 14:12:33 | user=liam.chen@acme.io | job_id=bq_0291_gh9 | bytes_billed=21474836480 | duration_ms=12400 | status=DONE
-- Product: Investigating high-latency workflows for Enterprise accounts.
-- Filtering for runs over 10s step_count > 5.
SELECT 
    c.company_name,
    fwr.workflow_id,
    AVG(fwr.duration_ms) as avg_duration,
    MAX(fwr.duration_ms) as peak_duration,
    COUNT(fwr.run_id) as total_runs
FROM `nexus-analyst-demo.acme.fact_workflow_runs` fwr
JOIN `nexus-analyst-demo.acme.dim_customers` c ON fwr.customer_id = c.customer_id
WHERE c.current_plan_tier = 'Enterprise'
  AND fwr.triggered_at >= '2026-04-01'
GROUP BY 1, 2
HAVING avg_duration > 10000
ORDER BY avg_duration DESC;

-- 2026-05-03 16:45:10 | user=jessica.rodriguez@acme.io | job_id=bq_0295_er1 | bytes_billed=0 | duration_ms=100 | status=ERROR
-- ERROR: Table name typo in ad-hoc investigation.
SELECT * FROM `nexus-analyst-demo.acme.dim_customer_list` LIMIT 10;
-- Analysis: Table 'dim_customer_list' not found; did you mean 'dim_customers'?

-- 2026-05-04 08:30:45 | user=olivia.duarte@acme.io | job_id=bq_0301_nb6 | bytes_billed=42949672960 | duration_ms=22000 | status=DONE
-- Finance: Gross NRR (Net Revenue Retention) calculation for Q1 2026.
-- Comparing MRR for the same cohort of customers between Jan and March.
WITH jan_mrr AS (
    SELECT customer_id, SUM(mrr_usd) as mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE '2026-01-01' BETWEEN start_date AND end_date
    GROUP BY 1
),
mar_mrr AS (
    SELECT customer_id, SUM(mrr_usd) as mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE '2026-03-31' BETWEEN start_date AND end_date
    GROUP BY 1
)
SELECT 
    SUM(CASE WHEN j.mrr > 0 THEN m.mrr ELSE 0 END) / SUM(j.mrr) as gross_nrr
FROM jan_mrr j
LEFT JOIN mar_mrr m ON j.customer_id = m.customer_id;

-- 2026-05-04 10:12:11 | user=marcus.wong@acme.io | job_id=bq_0305_lk2 | bytes_billed=8589934592 | duration_ms=4100 | status=DONE
-- Marketing: Channel performance for FY2026 YTD.
-- Which acquisition channels are driving the highest seat counts?
SELECT 
    acquisition_channel,
    COUNT(customer_id) as new_logos,
    SUM(seat_count_licensed) as total_seats,
    SUM(current_mrr_usd) * 12 as estimated_arr
FROM `nexus-analyst-demo.acme.dim_customers`
WHERE signup_date >= '2026-01-01'
GROUP BY 1
ORDER BY estimated_arr DESC;

-- 2026-05-04 13:55:02 | user=system_service_account@acme.io | job_id=bq_scheduled_009 | bytes_billed=107374182400 | duration_ms=45000 | status=DONE
-- Scheduled: Daily Health Score Aggregation. 
-- Touching all 5 marts to flag accounts with low activity vs high seat count.
WITH usage_stats AS (
    SELECT 
        customer_id, 
        COUNT(run_id) as runs_last_7d,
        COUNT(DISTINCT triggered_by) as active_users_7d
    FROM `nexus-analyst-demo.acme.fact_workflow_runs`
    WHERE triggered_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
    GROUP BY 1
),
billing_stats AS (
    SELECT 
        customer_id,
        status as last_invoice_status
    FROM `nexus-analyst-demo.acme.fact_invoices`
    QUALIFY ROW_NUMBER() OVER(PARTITION BY customer_id ORDER BY invoice_date DESC) = 1
)
SELECT 
    c.customer_id,
    c.company_name,
    c.current_plan_tier,
    c.seat_count_licensed,
    u.active_users_7d,
    u.runs_last_7d,
    b.last_invoice_status,
    e.full_name as csm_name,
    CASE 
        WHEN u.active_users_7d < (c.seat_count_licensed * 0.1) THEN 'High Risk'
        WHEN b.last_invoice_status = 'OVERDUE' THEN 'Payment Risk'
        ELSE 'Healthy'
    END as health_score
FROM `nexus-analyst-demo.acme.dim_customers` c
LEFT JOIN usage_stats u ON c.customer_id = u.customer_id
LEFT JOIN billing_stats b ON c.customer_id = b.customer_id
JOIN `nexus-analyst-demo.acme.dim_employees` e ON c.csm_employee_id = e.employee_id
WHERE c.status = 'Active';

-- 2026-05-04 15:20:19 | user=sarah.jenkins@acme.io | job_id=bq_0312_pw3 | bytes_billed=2147483648 | duration_ms=900 | status=DONE
-- CS: Auditing 'Global Logistics Corp' (C-1021) for Business-to-Enterprise upgrade path.
-- Checking their workflow run volume vs current Business tier quota (100k).
SELECT 
    c.company_name,
    d.month_name,
    COUNT(fwr.run_id) as monthly_runs
FROM `nexus-analyst-demo.acme.fact_workflow_runs` fwr
JOIN `nexus-analyst-demo.acme.dim_customers` c ON fwr.customer_id = c.customer_id
JOIN `nexus-analyst-demo.acme.dim_dates` d ON DATE(fwr.triggered_at) = d.date
WHERE c.customer_id = 'C-1021'
  AND d.year = 2026
GROUP BY 1, 2, d.month
ORDER BY d.month ASC;

-- 2026-05-04 16:05:44 | user=liam.chen@acme.io | job_id=bq_0315_xz1 | bytes_billed=5368709120 | duration_ms=1500 | status=DONE
-- Product: Checking for 'Ghost Users' - invited but never logged in within 30 days.
-- Cross-referencing dim_users with their invitees.
SELECT 
    u.user_id,
    u.email_domain,
    u.signup_date,
    u.last_login_date,
    c.company_name,
    e.full_name as inviter_name
FROM `nexus-analyst-demo.acme.dim_users` u
JOIN `nexus-analyst-demo.acme.dim_customers` c ON u.customer_id = c.customer_id
LEFT JOIN `nexus-analyst-demo.acme.dim_users` e ON u.invited_by_user_id = e.user_id
WHERE u.last_login_date IS NULL
  AND u.signup_date < DATE_SUB('2026-05-04', INTERVAL 30 DAY)
  AND u.is_active = TRUE;

-- 2026-05-04 17:42:10 | user=olivia.duarte@acme.io | job_id=bq_0320_rt9 | bytes_billed=1073741824 | duration_ms=450 | status=DONE
-- Finance: Quick check on 'C-8933' ARR.
SELECT 
    company_name, 
    current_mrr_usd * 12 as current_arr,
    account_tier,
    status
FROM `nexus-analyst-demo.acme.dim_customers`
WHERE customer_id = 'C-8933';

-- 2026-05-05 09:00:00 | user=system_service_account@acme.io | job_id=bq_scheduled_012 | bytes_billed=32212254720 | duration_ms=15000 | status=DONE
-- Scheduled: Syncing fact_subscriptions change logs.
-- Identifying upgrades vs renewals for the last 24h.
SELECT 
    subscription_id,
    customer_id,
    change_type,
    mrr_usd,
    seat_count
FROM `nexus-analyst-demo.acme.fact_subscriptions`
WHERE start_date = '2026-05-04'
  AND change_type IN ('UPGRADE', 'EXPANSION');

-- 2026-05-05 10:14:22 | user=sarah.jenkins@acme.io | job_id=bq_0344_lp2 | bytes_billed=18253611008 | duration_ms=2100 | status=DONE
-- Sales Ops: Gross Revenue Retention (GRR) check for Q1 2026. 
-- Looking at customers who were active on 2026-01-01 vs their MRR on 2026-03-31.
WITH q1_start AS (
    SELECT customer_id, mrr_usd as mrr_start
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE is_current = TRUE 
      AND start_date <= '2026-01-01'
      AND (end_date > '2026-01-01' OR end_date IS NULL)
),
q1_end AS (
    SELECT customer_id, mrr_usd as mrr_end
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE is_current = TRUE 
      AND start_date <= '2026-03-31'
      AND (end_date > '2026-03-31' OR end_date IS NULL)
)
SELECT 
    SUM(s.mrr_start) as starting_mrr,
    SUM(CASE WHEN e.mrr_end IS NULL THEN 0 ELSE e.mrr_end END) as ending_mrr,
    (SUM(CASE WHEN e.mrr_end IS NULL THEN 0 ELSE LEAST(s.mrr_start, e.mrr_end) END) / SUM(s.mrr_start)) * 100 as gross_retention_pct
FROM q1_start s
LEFT JOIN q1_end e ON s.customer_id = e.customer_id;

-- 2026-05-05 11:05:01 | user=khalid.bakari@acme.io | job_id=bq_0348_m9k | bytes_billed=2147483648 | duration_ms=320 | status=ERROR
-- Error: Not found: Table nexus-analyst-demo.acme.customers was not found in location US
-- Khalid typo'd the table name again.
SELECT company_name, current_mrr_usd 
FROM `nexus-analyst-demo.acme.customers` 
WHERE account_tier = 'Ent';

-- 2026-05-05 11:06:45 | user=khalid.bakari@acme.io | job_id=bq_0349_a2z | bytes_billed=2147483648 | duration_ms=410 | status=DONE
-- Support: Retrying query with correct path for Ent health check.
SELECT 
    c.customer_id, 
    c.company_name, 
    c.current_mrr_usd, 
    e.full_name as csm_owner
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_employees` e ON c.csm_employee_id = e.employee_id
WHERE c.account_tier = 'Ent' 
  AND c.status = 'ACTIVE'
ORDER BY c.current_mrr_usd DESC;

-- 2026-05-05 13:22:18 | user=marcus.vance@acme.io | job_id=bq_0355_fgh | bytes_billed=42949672960 | duration_ms=8400 | status=DONE
-- CS: Identifying 'At Risk' Business accounts (Low seat utilization).
-- Comparing seat_count_licensed vs actual active users in last 30 days.
SELECT 
    c.customer_id,
    c.company_name,
    c.seat_count_licensed,
    COUNT(DISTINCT u.user_id) as active_users_30d,
    (COUNT(DISTINCT u.user_id) / NULLIF(c.seat_count_licensed, 0)) * 100 as utilization_pct
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_users` u ON c.customer_id = u.customer_id
WHERE c.current_plan_tier = 'Business'
  AND u.last_login_date >= DATE_SUB('2026-05-05', INTERVAL 30 DAY)
  AND c.status = 'ACTIVE'
GROUP BY 1, 2, 3
HAVING utilization_pct < 40
ORDER BY utilization_pct ASC;

-- 2026-05-05 14:45:10 | user=chen.wu@acme.io | job_id=bq_0360_ty8 | bytes_billed=10737418240 | duration_ms=2900 | status=DONE
-- Product: Step count analysis on workflow failures. 
-- Do longer workflows fail more often with error_code 'TIMEOUT_EXCEEDED'?
SELECT 
    CASE 
        WHEN step_count < 5 THEN 'Short (1-4)'
        WHEN step_count < 15 THEN 'Medium (5-14)'
        ELSE 'Long (15+)'
    END as workflow_length,
    COUNT(*) as total_runs,
    COUNTIF(status = 'FAILED' AND error_code = 'TIMEOUT_EXCEEDED') as timeouts,
    SAFE_DIVIDE(COUNTIF(status = 'FAILED' AND error_code = 'TIMEOUT_EXCEEDED'), COUNT(*)) * 100 as timeout_rate
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE triggered_at >= '2026-01-01'
GROUP BY 1
ORDER BY 4 DESC;

-- 2026-05-05 15:10:04 | user=olivia.duarte@acme.io | job_id=bq_0365_rr1 | bytes_billed=5368709120 | duration_ms=1200 | status=DONE
-- Finance: Aging invoices for customer C-4112 (Acme power user but lagging on payments).
SELECT 
    i.invoice_id,
    i.amount_usd,
    i.invoice_date,
    d.date as today,
    DATE_DIFF(DATE('2026-05-05'), i.invoice_date, DAY) as days_overdue
FROM `nexus-analyst-demo.acme.fact_invoices` i
CROSS JOIN (SELECT DATE('2026-05-05') as date) d
WHERE i.customer_id = 'C-4112'
  AND i.status = 'UNPAID'
  AND i.invoice_date < '2026-05-05';

-- 2026-05-05 16:30:55 | user=system_service_account@acme.io | job_id=bq_scheduled_099 | bytes_billed=85899345920 | duration_ms=45000 | status=DONE
-- Scheduled: Daily Rollup of User Activity by Country.
-- Hits dim_customers, dim_users, and fact_user_events.
SELECT 
    c.country,
    d.month_name,
    COUNT(DISTINCT e.user_id) as mau,
    COUNT(e.event_id) as total_events
FROM `nexus-analyst-demo.acme.fact_user_events` e
JOIN `nexus-analyst-demo.acme.dim_customers` c ON e.customer_id = c.customer_id
JOIN `nexus-analyst-demo.acme.dim_dates` d ON DATE(e.event_at) = d.date
WHERE d.year = 2026
GROUP BY 1, 2;

-- 2026-05-05 17:01:12 | user=liam.chen@acme.io | job_id=bq_0372_nm5 | bytes_billed=1073741824 | duration_ms=600 | status=DONE
-- Product: Checking the last login for the admin at C-9021. 
-- Need to make sure they've seen the new dashboard.
SELECT 
    u.email_domain,
    u.last_login_date,
    u.role
FROM `nexus-analyst-demo.acme.dim_users` u
WHERE u.customer_id = 'C-9021'
  AND u.role = 'ADMIN'
ORDER BY u.last_login_date DESC
LIMIT 5;

-- 2026-05-05 17:15:33 | user=maya.patel@acme.io | job_id=bq_0375_p99 | bytes_billed=2147483648 | duration_ms=800 | status=DONE
-- Marketing: Channel performance for April 2026 signups.
SELECT 
    acquisition_channel,
    COUNT(customer_id) as new_logos,
    SUM(current_mrr_usd) as total_new_mrr
FROM `nexus-analyst-demo.acme.dim_customers`
WHERE signup_date BETWEEN '2026-04-01' AND '2026-04-30'
GROUP BY 1
ORDER BY total_new_mrr DESC;

-- 2026-02-14 09:12:44 | user=alex.rivera@acme.io | job_id=bq_8821_f1n | bytes_billed=12884901888 | duration_ms=2100 | status=DONE
-- Finance: Q1 Gross Revenue Retention (GRR) calculation.
-- Looking at the January 1st cohort to see what we lost by Feb 1st.
WITH mrr_start AS (
    SELECT customer_id, mrr_usd as jan_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE start_date <= '2026-01-01' 
      AND (end_date > '2026-01-01' OR end_date IS NULL)
      AND is_current = true
),
mrr_end AS (
    SELECT customer_id, mrr_usd as feb_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE start_date <= '2026-02-01' 
      AND (end_date > '2026-02-01' OR end_date IS NULL)
)
SELECT 
    SUM(jan_mrr) as starting_mrr,
    SUM(CASE WHEN feb_mrr < jan_mrr THEN feb_mrr ELSE jan_mrr END) as retained_mrr,
    (SUM(CASE WHEN feb_mrr < jan_mrr THEN feb_mrr ELSE jan_mrr END) / SUM(jan_mrr)) * 100 as grr_pct
FROM mrr_start
LEFT JOIN mrr_end USING (customer_id);

-- 2026-02-14 10:05:02 | user=sarah.jenkins@acme.io | job_id=bq_9022_cs1 | bytes_billed=536870912 | duration_ms=450 | status=ERROR
-- CS: Quick health check on C-5581 (Global Logistics). 
-- They complained about workflow lag.
-- ERROR: Column 'workflow_latency' does not exist in nexus-analyst-demo.acme.fact_workflow_runs. 
SELECT 
    customer_id,
    AVG(workflow_latency) as avg_lag,
    status
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE customer_id = 'C-5581'
GROUP BY 1, 3;

-- 2026-02-14 10:06:15 | user=sarah.jenkins@acme.io | job_id=bq_9023_cs2 | bytes_billed=2147483648 | duration_ms=920 | status=DONE
-- CS: Fixing the query for C-5581. Using duration_ms instead.
SELECT 
    status,
    COUNT(*) as run_count,
    AVG(duration_ms) as avg_duration,
    APPROX_QUANTILES(duration_ms, 100)[OFFSET(95)] as p95_duration
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE customer_id = 'C-5581'
  AND triggered_at >= '2026-02-01'
GROUP BY 1;

-- 2026-03-10 14:22:11 | user=wei.zhang@acme.io | job_id=bq_1105_eng | bytes_billed=42949672960 | duration_ms=12400 | status=DONE
-- Engineering: Investigating high error rates for Webhook triggers in EMEA.
-- Joining with dim_customers to isolate the region.
SELECT 
    c.company_name,
    f.error_code,
    COUNT(*) as error_freq
FROM `nexus-analyst-demo.acme.fact_workflow_runs` f
JOIN `nexus-analyst-demo.acme.dim_customers` c ON f.customer_id = c.customer_id
WHERE f.status = 'FAILED'
  AND c.region = 'EMEA'
  AND f.triggered_at >= '2026-03-01'
GROUP BY 1, 2
HAVING error_freq > 10
ORDER BY error_freq DESC;

-- 2026-03-12 11:45:00 | user=system_service_account@acme.io | job_id=bq_scheduled_112 | bytes_billed=107374182400 | duration_ms=58000 | status=DONE
-- Scheduled: Monthly NRR (Net Revenue Retention) by Account Tier.
-- Complex rollup across 4 marts.
WITH cohort_active_mrr AS (
    SELECT 
        c.account_tier,
        SUM(s.mrr_usd) as mrr_prev
    FROM `nexus-analyst-demo.acme.fact_subscriptions` s
    JOIN `nexus-analyst-demo.acme.dim_customers` c ON s.customer_id = c.customer_id
    WHERE s.start_date <= '2026-02-01' 
      AND (s.end_date > '2026-02-01' OR s.end_date IS NULL)
      AND s.is_current = true
    GROUP BY 1
),
current_mrr AS (
    SELECT 
        c.account_tier,
        SUM(s.mrr_usd) as mrr_now
    FROM `nexus-analyst-demo.acme.fact_subscriptions` s
    JOIN `nexus-analyst-demo.acme.dim_customers` c ON s.customer_id = c.customer_id
    WHERE s.start_date <= '2026-03-01' 
      AND (s.end_date > '2026-03-01' OR s.end_date IS NULL)
      AND s.is_current = true
    GROUP BY 1
)
SELECT 
    p.account_tier,
    p.mrr_prev,
    n.mrr_now,
    SAFE_DIVIDE(n.mrr_now, p.mrr_prev) as nrr_ratio
FROM cohort_active_mrr p
JOIN current_mrr n ON p.account_tier = n.account_tier;

-- 2026-04-15 13:10:33 | user=liam.chen@acme.io | job_id=bq_2011_nm2 | bytes_billed=3221225472 | duration_ms=1500 | status=DONE
-- Product: Adoption of 'Advanced Logic' step. 
-- Looking for event 'workflow_step_added' with property 'type:logic'.
SELECT 
    c.industry,
    COUNT(DISTINCT e.user_id) as unique_users,
    COUNT(e.event_id) as total_events
FROM `nexus-analyst-demo.acme.fact_user_events` e
JOIN `nexus-analyst-demo.acme.dim_customers` c ON e.customer_id = c.customer_id
WHERE e.event_name = 'workflow_step_added'
  AND e.event_at >= '2026-01-01'
GROUP BY 1
ORDER BY unique_users DESC;

-- 2026-04-28 09:30:12 | user=maya.patel@acme.io | job_id=bq_2550_mkt | bytes_billed=8589934592 | duration_ms=3100 | status=DONE
-- Marketing: Identifying potential Enterprise upgrades for Sales.
-- SMB/MM customers on Pro/Business with > 80% seat utilization or high workflow usage.
SELECT 
    c.customer_id,
    c.company_name,
    c.current_plan_tier,
    c.seat_count_licensed,
    COUNT(DISTINCT u.user_id) as active_users,
    (COUNT(DISTINCT u.user_id) / c.seat_count_licensed) as seat_utilization
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_users` u ON c.customer_id = u.customer_id
WHERE c.account_tier IN ('SMB', 'MM')
  AND c.status = 'ACTIVE'
  AND u.is_active = true
GROUP BY 1, 2, 3, 4
HAVING seat_utilization > 0.9
ORDER BY seat_utilization DESC
LIMIT 50;

-- 2026-05-02 15:44:19 | user=alex.rivera@acme.io | job_id=bq_3001_fin | bytes_billed=4294967296 | duration_ms=1100 | status=DONE
-- Finance: Calculate total ARR as of May 1st for the board deck.
SELECT 
    SUM(mrr_usd) * 12 as total_arr_usd
FROM `nexus-analyst-demo.acme.fact_subscriptions`
WHERE is_current = true
  AND (end_date IS NULL OR end_date > '2026-05-01');

-- 2026-05-04 11:12:05 | user=liam.chen@acme.io | job_id=bq_3055_prod | bytes_billed=1073741824 | duration_ms=400 | status=DONE
-- Product: Checking if C-9021 (the admin we targeted) has logged in recently.
-- This follows up on the query from 2026-05-05 (Wait, timestamp check—Liam is jumping around).
SELECT 
    user_id,
    last_login_date,
    is_active
FROM `nexus-analyst-demo.acme.dim_users`
WHERE customer_id = 'C-9021'
  AND role = 'ADMIN'
ORDER BY last_login_date DESC;

-- 2026-05-04 16:55:12 | user=wei.zhang@acme.io | job_id=bq_3099_eng | bytes_billed=10737418240 | duration_ms=4500 | status=DONE
-- Engineering: Audit of storage usage for 'Business' tier customers.
-- Cross-referencing dim_plans storage limits.
SELECT 
    c.customer_id,
    c.company_name,
    p.storage_gb as plan_limit,
    COUNT(f.run_id) as total_runs_historical -- using runs as proxy for data bloat
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_plans` p ON c.current_plan_tier = p.plan_tier
JOIN `nexus-analyst-demo.acme.fact_workflow_runs` f ON c.customer_id = f.customer_id
WHERE c.current_plan_tier = 'Business'
GROUP BY 1, 2, 3
ORDER BY total_runs_historical DESC
LIMIT 10;

-- 2026-01-14 09:22:41 | user=sarah.jenkins@acme.io | job_id=bq_5012_sales | bytes_billed=8589934592 | duration_ms=2100 | status=DONE
-- Sales: NRR (Net Revenue Retention) for Enterprise cohort from Jan 2025.
-- Need to see how much the Jan '25 cohort has expanded or contracted by Jan '26.
WITH cohort_jan_2025 AS (
    SELECT 
        customer_id,
        mrr_usd as starting_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE is_current = false 
      AND start_date <= '2025-01-31'
      AND (end_date > '2025-01-01' OR end_date IS NULL)
      AND plan_tier = 'Enterprise'
),
current_jan_2026 AS (
    SELECT 
        customer_id,
        SUM(mrr_usd) as current_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE is_current = true
      AND plan_tier = 'Enterprise'
    GROUP BY 1
)
SELECT 
    SUM(c25.starting_mrr) as base_mrr,
    SUM(c26.current_mrr) as retained_mrr,
    (SUM(c26.current_mrr) / SUM(c25.starting_mrr)) * 100 as nrr_pct
FROM cohort_jan_2025 c25
LEFT JOIN current_jan_2026 c26 ON c25.customer_id = c26.customer_id;

-- 2026-01-15 14:10:02 | user=jason.lowe@acme.io | job_id=bq_5055_ops | bytes_billed=0 | duration_ms=50 | status=ERROR
-- Ops: Trying to find the AE mapping for a specific account. 
-- ERROR: Table 'nexus-analyst-demo.acme.dim_accounts' not found. (Note: use dim_customers instead).
SELECT company_name, ae_employee_id FROM `nexus-analyst-demo.acme.dim_accounts` WHERE customer_id = 'C-4421';

-- 2026-02-03 10:45:12 | user=priya.sharma@acme.io | job_id=bq_6102_cs | bytes_billed=5368709120 | duration_ms=3200 | status=DONE
-- CS: Finding "At Risk" Business accounts with low run usage relative to quota.
-- This is for the Q1 health check.
SELECT 
    c.customer_id,
    c.company_name,
    p.workflow_run_quota_per_month,
    COUNT(f.run_id) as runs_last_30d,
    SAFE_DIVIDE(COUNT(f.run_id), p.workflow_run_quota_per_month) as quota_utilization
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_plans` p ON c.current_plan_tier = p.plan_tier
LEFT JOIN `nexus-analyst-demo.acme.fact_workflow_runs` f ON c.customer_id = f.customer_id
WHERE c.current_plan_tier = 'Business'
  AND f.triggered_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY 1, 2, 3
HAVING quota_utilization < 0.1
ORDER BY quota_utilization ASC;

-- 2026-02-12 16:22:55 | user=liam.chen@acme.io | job_id=bq_6588_prod | bytes_billed=12884901888 | duration_ms=6800 | status=DONE
-- Product: Sticky users - Daily active users (DAU) vs Monthly active users (MAU) ratio.
-- Looking at Feb '26 activity.
WITH daily_active AS (
    SELECT 
        DATE(event_at) as event_date,
        COUNT(DISTINCT user_id) as dau
    FROM `nexus-analyst-demo.acme.fact_user_events`
    WHERE event_at BETWEEN '2026-02-01' AND '2026-02-28'
    GROUP BY 1
),
monthly_active AS (
    SELECT 
        COUNT(DISTINCT user_id) as mau
    FROM `nexus-analyst-demo.acme.fact_user_events`
    WHERE event_at BETWEEN '2026-02-01' AND '2026-02-28'
)
SELECT 
    da.event_date,
    da.dau,
    ma.mau,
    (da.dau / ma.mau) as stickiness_ratio
FROM daily_active da, monthly_active ma
ORDER BY da.event_date;

-- 2026-03-01 08:15:33 | user=alex.rivera@acme.io | job_id=bq_7001_fin | bytes_billed=2147483648 | duration_ms=1200 | status=DONE
-- Finance: Aging report for unpaid invoices.
SELECT 
    c.company_name,
    i.invoice_id,
    i.amount_usd,
    i.invoice_date,
    DATE_DIFF('2026-03-01', i.invoice_date, DAY) as days_overdue
FROM `nexus-analyst-demo.acme.fact_invoices` i
JOIN `nexus-analyst-demo.acme.dim_customers` c ON i.customer_id = c.customer_id
WHERE i.status = 'UNPAID'
  AND i.invoice_date < '2026-02-15'
ORDER BY days_overdue DESC;

-- 2026-03-10 11:30:19 | user=maya.patel@acme.io | job_id=bq_7222_mkt | bytes_billed=3221225472 | duration_ms=900 | status=DONE
-- Marketing: Top acquisition channels for paying customers (excluding Free tier).
SELECT 
    acquisition_channel,
    COUNT(customer_id) as customer_count,
    SUM(current_mrr_usd) as total_mrr
FROM `nexus-analyst-demo.acme.dim_customers`
WHERE current_plan_tier != 'Free'
  AND status = 'ACTIVE'
GROUP BY 1
ORDER BY total_mrr DESC;

-- 2026-03-25 15:44:02 | user=wei.zhang@acme.io | job_id=bq_7890_eng | bytes_billed=21474836480 | duration_ms=12400 | status=DONE
-- Engineering: Analyzing workflow performance across different regions to debug latency spikes.
-- Using window functions to find the 95th percentile duration.
SELECT 
    c.region,
    f.status,
    PERCENTILE_CONT(f.duration_ms, 0.95) OVER(PARTITION BY c.region) as p95_duration_ms,
    AVG(f.duration_ms) OVER(PARTITION BY c.region) as avg_duration_ms,
    COUNT(f.run_id) OVER(PARTITION BY c.region) as run_count
FROM `nexus-analyst-demo.acme.fact_workflow_runs` f
JOIN `nexus-analyst-demo.acme.dim_customers` c ON f.customer_id = c.customer_id
WHERE f.triggered_at >= '2026-03-01'
  AND f.status = 'SUCCESS'
LIMIT 500; -- Just a sample to check the spread.

-- 2026-04-12 09:05:11 | user=liam.chen@acme.io | job_id=bq_8044_prod | bytes_billed=1073741824 | duration_ms=300 | status=DONE
-- Product: Checking seat growth for 'C-5521' (Global Corp).
-- They were supposed to expand to 300 seats.
SELECT 
    subscription_id,
    seat_count,
    mrr_usd,
    start_date,
    change_type
FROM `nexus-analyst-demo.acme.fact_subscriptions`
WHERE customer_id = 'C-5521'
ORDER BY start_date DESC;

-- 2026-04-20 13:12:44 | user=sarah.jenkins@acme.io | job_id=bq_8211_sales | bytes_billed=4294967296 | duration_ms=1500 | status=DONE
-- Sales: Listing Enterprise renewals coming up in the next 90 days.
-- AE-led expansion playbooks.
SELECT 
    c.company_name,
    c.ae_employee_id,
    e.full_name as ae_name,
    s.end_date,
    s.mrr_usd * 12 as current_arr
FROM `nexus-analyst-demo.acme.fact_subscriptions` s
JOIN `nexus-analyst-demo.acme.dim_customers` c ON s.customer_id = c.customer_id
JOIN `nexus-analyst-demo.acme.dim_employees` e ON c.ae_employee_id = e.employee_id
WHERE s.is_current = true
  AND s.plan_tier = 'Enterprise'
  AND s.end_date BETWEEN '2026-04-20' AND '2026-07-20'
ORDER BY s.end_date ASC;

-- 2026-04-22 14:15:33 | user=anaya.iyer@acme.io | job_id=bq_8342_fin | bytes_billed=8589934592 | duration_ms=4200 | status=DONE
-- Finance: Calculating NRR (Net Revenue Retention) for the MM (Mid-Market) segment.
-- Comparing cohorts from Q1 2025 to Q1 2026.
WITH cohort_2025 AS (
    SELECT 
        customer_id,
        SUM(mrr_usd) as mrr_start
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE is_current = false 
      AND start_date <= '2025-03-31' 
      AND end_date >= '2025-01-01'
    GROUP BY 1
),
cohort_2026 AS (
    SELECT 
        customer_id,
        SUM(mrr_usd) as mrr_end
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE is_current = true
      AND start_date <= '2026-03-31'
    GROUP BY 1
)
SELECT 
    c.account_tier,
    SUM(c25.mrr_start) as initial_mrr,
    SUM(c26.mrr_end) as retained_mrr,
    SAFE_DIVIDE(SUM(c26.mrr_end), SUM(c25.mrr_start)) as nrr_pct
FROM cohort_2025 c25
JOIN cohort_2026 c26 ON c25.customer_id = c26.customer_id
JOIN `nexus-analyst-demo.acme.dim_customers` c ON c25.customer_id = c.customer_id
WHERE c.account_tier = 'MM'
GROUP BY 1;

-- 2026-04-23 10:44:19 | user=marcus.wong@acme.io | job_id=bq_8410_csm | bytes_billed=536870912 | duration_ms=150 | status=ERROR
-- CSM: Quick check on why C-9912 (AlphaLogistics) has so many failed runs today.
-- ERROR: Table name typo. 'fact_runs' does not exist in dataset nexus-analyst-demo.acme.
SELECT 
    workflow_id,
    error_code,
    COUNT(*) as fail_count
FROM `nexus-analyst-demo.acme.fact_runs` 
WHERE customer_id = 'C-9912' 
  AND status = 'FAILED'
  AND triggered_at >= CURRENT_TIMESTAMP() - INTERVAL 24 HOUR
GROUP BY 1, 2;

-- 2026-04-23 10:45:02 | user=marcus.wong@acme.io | job_id=bq_8411_csm | bytes_billed=2147483648 | duration_ms=800 | status=DONE
-- CSM: Fixing previous query.
SELECT 
    workflow_id,
    error_code,
    COUNT(*) as fail_count
FROM `nexus-analyst-demo.acme.fact_workflow_runs` 
WHERE customer_id = 'C-9912' 
  AND status = 'FAILED'
  AND triggered_at >= '2026-04-23'
GROUP BY 1, 2
ORDER BY fail_count DESC;

-- 2026-04-25 16:22:11 | user=wei.zhang@acme.io | job_id=bq_8599_eng | bytes_billed=42949672960 | duration_ms=18500 | status=DONE
-- Engineering: Benchmarking p99 latency for Business tier customers vs Pro tier.
-- We're seeing some resource contention on the shared 'us-east-1' runners.
SELECT 
    p.plan_tier,
    APPROX_QUANTILES(f.duration_ms, 100)[OFFSET(99)] as p99_latency_ms,
    COUNT(f.run_id) as total_runs
FROM `nexus-analyst-demo.acme.fact_workflow_runs` f
JOIN `nexus-analyst-demo.acme.dim_customers` c ON f.customer_id = c.customer_id
JOIN `nexus-analyst-demo.acme.dim_plans` p ON c.current_plan_tier = p.plan_tier
WHERE f.triggered_at >= '2026-04-01'
GROUP BY 1;

-- 2026-04-28 09:12:45 | user=danielle.smit@acme.io | job_id=bq_8822_mkt | bytes_billed=1073741824 | duration_ms=1100 | status=DONE
-- Marketing: Attribution check for last month's Paid Search spend.
-- Looking for C-level signups that hit the 'Enterprise' contact form.
SELECT 
    u.email_domain,
    c.company_name,
    c.acquisition_channel,
    c.signup_date,
    e.event_name
FROM `nexus-analyst-demo.acme.dim_users` u
JOIN `nexus-analyst-demo.acme.dim_customers` c ON u.customer_id = c.customer_id
JOIN `nexus-analyst-demo.acme.fact_user_events` e ON u.user_id = e.user_id
WHERE c.acquisition_channel = 'Paid Search'
  AND e.event_name = 'enterprise_contact_form_submitted'
  AND c.signup_date >= '2026-03-01'
  AND u.role IN ('Admin', 'Owner');

-- 2026-04-29 11:30:00 | user=liam.chen@acme.io | job_id=bq_8910_prod | bytes_billed=5368709120 | duration_ms=3100 | status=DONE
-- Product: Investigating 'shelfware' - Business customers with < 10% seat utilization.
-- This is for the Q2 churn prevention task force.
WITH seat_data AS (
    SELECT 
        c.customer_id,
        c.company_name,
        c.seat_count_licensed,
        COUNT(u.user_id) as active_user_count
    FROM `nexus-analyst-demo.acme.dim_customers` c
    LEFT JOIN `nexus-analyst-demo.acme.dim_users` u ON c.customer_id = u.customer_id AND u.is_active = true
    WHERE c.current_plan_tier = 'Business'
      AND c.status = 'ACTIVE'
    GROUP BY 1, 2, 3
)
SELECT 
    *,
    SAFE_DIVIDE(active_user_count, seat_count_licensed) as utilization_rate
FROM seat_data
WHERE SAFE_DIVIDE(active_user_count, seat_count_licensed) < 0.10
ORDER BY seat_count_licensed DESC;

-- 2026-05-01 13:05:55 | user=anaya.iyer@acme.io | job_id=bq_9045_fin | bytes_billed=12884901888 | duration_ms=6400 | status=DONE
-- Finance: Monthly ARR roll-forward. 
-- Checking New, Expansion, Contraction, and Churn for April 2026.
SELECT 
    change_type,
    SUM(mrr_usd) * 12 as arr_impact,
    COUNT(DISTINCT customer_id) as customer_count
FROM `nexus-analyst-demo.acme.fact_subscriptions`
WHERE start_date BETWEEN '2026-04-01' AND '2026-04-30'
GROUP BY 1;

-- 2026-05-02 15:40:22 | user=sarah.jenkins@acme.io | job_id=bq_9121_sales | bytes_billed=2147483648 | duration_ms=950 | status=DONE
-- Sales: Finding "Pro" customers with high workflow volume (>80% of quota).
-- These are prime targets for AE outreach to move to "Business".
SELECT 
    c.customer_id,
    c.company_name,
    p.workflow_run_quota_per_month,
    COUNT(f.run_id) as current_month_runs,
    ROUND(COUNT(f.run_id) / p.workflow_run_quota_per_month, 2) as quota_usage_pct
FROM `nexus-analyst-demo.acme.fact_workflow_runs` f
JOIN `nexus-analyst-demo.acme.dim_customers` c ON f.customer_id = c.customer_id
JOIN `nexus-analyst-demo.acme.dim_plans` p ON c.current_plan_tier = p.plan_tier
WHERE c.current_plan_tier = 'Pro'
  AND f.triggered_at >= '2026-04-01'
GROUP BY 1, 2, 3
HAVING quota_usage_pct > 0.8
ORDER BY quota_usage_pct DESC;

-- 2026-05-02 17:10:44 | user=malik.dubois@acme.io | job_id=bq_9208_cs | bytes_billed=4294967296 | duration_ms=1850 | status=DONE
-- CS: Health check for Account CUST-742 (Velocity Tech). 
-- Looking for drop in daily active users (DAU) over the last 30 days vs previous 30.
WITH daily_usage AS (
    SELECT 
        DATE(event_at) as usage_date,
        COUNT(DISTINCT user_id) as dau
    FROM `nexus-analyst-demo.acme.fact_user_events`
    WHERE customer_id = 'CUST-742'
      AND event_at >= '2026-03-01'
    GROUP BY 1
),
periods AS (
    SELECT 
        usage_date,
        dau,
        CASE WHEN usage_date >= '2026-04-01' THEN 'Current' ELSE 'Previous' END as period
    FROM daily_usage
)
SELECT 
    period,
    AVG(dau) as avg_dau
FROM periods
GROUP BY 1;

-- 2026-05-03 09:15:12 | user=data-pipeline-sa@acme.io | job_id=bq_9333_sys | bytes_billed=0 | duration_ms=45 | status=ERROR
-- ERROR: Table not found: `nexus-analyst-demo.acme.dim_customer_metadata_v2`. 
-- Dev tried to run a migration script on a non-existent staging table.
SELECT * FROM `nexus-analyst-demo.acme.dim_customer_metadata_v2` LIMIT 10;

-- 2026-05-03 11:22:05 | user=tara.vance@acme.io | job_id=bq_9411_ops | bytes_billed=8589934592 | duration_ms=4100 | status=DONE
-- Sales Ops: Q1 2026 AE Leaderboard. 
-- Calculating New Logo ARR and Expansion ARR per AE.
SELECT 
    e.full_name as ae_name,
    SUM(CASE WHEN s.change_type = 'NEW' THEN s.mrr_usd * 12 ELSE 0 END) as new_logo_arr,
    SUM(CASE WHEN s.change_type = 'EXPANSION' THEN s.mrr_usd * 12 ELSE 0 END) as expansion_arr,
    COUNT(DISTINCT s.customer_id) as closed_deals
FROM `nexus-analyst-demo.acme.fact_subscriptions` s
JOIN `nexus-analyst-demo.acme.dim_customers` c ON s.customer_id = c.customer_id
JOIN `nexus-analyst-demo.acme.dim_employees` e ON c.ae_employee_id = e.employee_id
WHERE s.start_date BETWEEN '2026-01-01' AND '2026-03-31'
  AND s.change_type IN ('NEW', 'EXPANSION')
GROUP BY 1
ORDER BY 2 DESC;

-- 2026-05-03 14:05:33 | user=kenji.tanaka@acme.io | job_id=bq_9502_eng | bytes_billed=35433480192 | duration_ms=12400 | status=DONE
-- Product/Eng: Infrastructure load analysis. 
-- Checking workflow duration percentiles to identify potential latency spikes in the runner engine.
SELECT 
    DATE_TRUNC(triggered_at, HOUR) as hour_bucket,
    COUNT(*) as total_runs,
    APPROX_QUANTILES(duration_ms, 100)[OFFSET(50)] as p50_duration_ms,
    APPROX_QUANTILES(duration_ms, 100)[OFFSET(95)] as p95_duration_ms,
    APPROX_QUANTILES(duration_ms, 100)[OFFSET(99)] as p99_duration_ms
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE triggered_at >= '2026-04-25'
GROUP BY 1
ORDER BY 1 DESC;

-- 2026-05-03 16:48:19 | user=anaya.iyer@acme.io | job_id=bq_9688_fin | bytes_billed=17179869184 | duration_ms=7800 | status=DONE
-- Finance: Gross Revenue Retention (GRR) and Net Revenue Retention (NRR) Cohort Analysis.
-- Comparing the Jan 2025 cohort's performance as of April 2026.
WITH cohort_jan_2025 AS (
    SELECT customer_id, mrr_usd as starting_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE start_date BETWEEN '2025-01-01' AND '2025-01-31'
      AND change_type = 'NEW'
),
current_state AS (
    SELECT 
        c.customer_id,
        c.starting_mrr,
        COALESCE(s.mrr_usd, 0) as current_mrr,
        CASE WHEN s.customer_id IS NULL OR s.mrr_usd = 0 THEN 1 ELSE 0 END as is_churned
    FROM cohort_jan_2025 c
    LEFT JOIN `nexus-analyst-demo.acme.fact_subscriptions` s 
      ON c.customer_id = s.customer_id 
      AND s.is_current = true
)
SELECT 
    COUNT(*) as cohort_size,
    SUM(starting_mrr) as cohort_start_mrr,
    SUM(current_mrr) as cohort_current_mrr,
    SAFE_DIVIDE(SUM(current_mrr), SUM(starting_mrr)) as nrr,
    SAFE_DIVIDE(SUM(CASE WHEN current_mrr > starting_mrr THEN starting_mrr ELSE current_mrr END), SUM(starting_mrr)) as grr
FROM current_state;

-- 2026-05-04 08:30:10 | user=marcus.wong@acme.io | job_id=bq_9712_mkt | bytes_billed=5368709120 | duration_ms=2100 | status=DONE
-- Marketing: Lead source attribution for Enterprise prospects.
-- Joining dim_customers with fact_leads (internal staging) to see which channels drive high-tier interest.
SELECT 
    c.acquisition_channel,
    c.account_tier,
    COUNT(c.customer_id) as customer_count,
    SUM(c.current_mrr_usd) as total_mrr
FROM `nexus-analyst-demo.acme.dim_customers` c
WHERE c.signup_date >= '2025-10-01'
GROUP BY 1, 2
ORDER BY 4 DESC;

-- 2026-05-04 10:12:45 | user=sarah.jenkins@acme.io | job_id=bq_9845_sales | bytes_billed=1073741824 | duration_ms=450 | status=DONE
-- Sales: Quick lookup of specific accounts for the Monday morning sync.
-- Checking seat utilization for "Global-Logistics-Sync" (CUST-219) and "Fintech-Flow" (CUST-551).
SELECT 
    customer_id,
    company_name,
    seat_count_licensed,
    current_plan_tier,
    status
FROM `nexus-analyst-demo.acme.dim_customers`
WHERE customer_id IN ('CUST-219', 'CUST-551');

-- 2026-05-04 11:55:02 | user=malik.dubois@acme.io | job_id=bq_9921_cs | bytes_billed=21474836480 | duration_ms=9200 | status=DONE
-- CS: Identifying users who haven't logged in for 30+ days but are in accounts with high ticket volume.
-- This indicates potential knowledge gaps or onboarding failures.
WITH inactive_users AS (
    SELECT user_id, customer_id, email_domain
    FROM `nexus-analyst-demo.acme.dim_users`
    WHERE last_login_date < DATE_SUB('2026-05-04', INTERVAL 30 DAY)
      AND is_active = true
),
account_tickets AS (
    SELECT customer_id, COUNT(*) as ticket_count
    FROM `nexus-analyst-demo.acme.fact_support_tickets`
    WHERE created_at >= '2026-04-01'
    GROUP BY 1
    HAVING ticket_count > 5
)
SELECT 
    u.email_domain,
    u.user_id,
    t.ticket_count,
    c.company_name,
    e.full_name as csm_owner
FROM inactive_users u
JOIN account_tickets t ON u.customer_id = t.customer_id
JOIN `nexus-analyst-demo.acme.dim_customers` c ON u.customer_id = c.customer_id
JOIN `nexus-analyst-demo.acme.dim_employees` e ON c.csm_employee_id = e.employee_id;

-- 2026-01-15 09:44:12 | user=chen.wei@acme.io | job_id=bq_3301_fin | bytes_billed=42949672960 | duration_ms=15400 | status=DONE
-- Finance: Calculating Gross Revenue Retention (GRR) for the Q4 2025 Board Deck.
-- Looking at the MRR of cohorts that started in Jan 2025 vs their status in Dec 2025.
-- Excludes expansion (pure retention focus).
WITH cohort_jan_2025 AS (
    SELECT 
        customer_id,
        mrr_usd as starting_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE start_date BETWEEN '2025-01-01' AND '2025-01-31'
      AND is_current = false -- looking at historical snapshot
),
dec_2025_status AS (
    SELECT 
        customer_id,
        mrr_usd as ending_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE '2025-12-31' BETWEEN start_date AND end_date
)
SELECT 
    SUM(c.starting_mrr) as cohort_start_mrr,
    SUM(CASE WHEN d.ending_mrr > 0 THEN LEAST(c.starting_mrr, d.ending_mrr) ELSE 0 END) as retained_mrr,
    (SUM(CASE WHEN d.ending_mrr > 0 THEN LEAST(c.starting_mrr, d.ending_mrr) ELSE 0 END) / SUM(c.starting_mrr)) * 100 as grr_percentage
FROM cohort_jan_2025 c
LEFT JOIN dec_2025_status d ON c.customer_id = d.customer_id;

-- 2026-02-10 14:22:11 | user=elara.vance@acme.io | job_id=bq_4122_prod | bytes_billed=102400 | duration_ms=120 | status=ERROR
-- Product: Investigating error codes in the runner service.
-- ERROR: Table name typo 'dim_custmers' instead of 'dim_customers'.
SELECT 
    f.error_code,
    c.industry,
    COUNT(*) as fail_count
FROM `nexus-analyst-demo.acme.fact_workflow_runs` f
JOIN `nexus-analyst-demo.acme.dim_custmers` c ON f.customer_id = c.customer_id
WHERE f.status = 'FAILED' 
  AND f.triggered_at > '2026-02-01'
GROUP BY 1, 2;

-- 2026-02-10 14:23:45 | user=elara.vance@acme.io | job_id=bq_4123_prod | bytes_billed=3221225472 | duration_ms=1800 | status=DONE
-- Product: Corrected query for workflow failure rates by account tier.
-- Trying to see if 'Enterprise' (CUST-802, CUST-112) have fewer step_count related timeouts.
SELECT 
    c.account_tier,
    AVG(f.duration_ms) as avg_duration,
    COUNTIF(f.status = 'FAILED') / COUNT(*) as error_rate,
    APPROX_QUANTILES(f.step_count, 100)[OFFSET(95)] as p95_step_count
FROM `nexus-analyst-demo.acme.fact_workflow_runs` f
JOIN `nexus-analyst-demo.acme.dim_customers` c ON f.customer_id = c.customer_id
WHERE f.triggered_at >= '2026-01-01'
GROUP BY 1
ORDER BY error_rate DESC;

-- 2026-03-12 16:05:30 | user=pete.hudson@acme.io | job_id=bq_5509_mktg | bytes_billed=5368709120 | duration_ms=3100 | status=DONE
-- Marketing: CAC vs LTV estimate per channel.
-- Joined with dim_customers to see current_mrr_usd as a proxy for LTV.
SELECT 
    acquisition_channel,
    COUNT(customer_id) as total_customers,
    SUM(current_mrr_usd) * 24 as est_2yr_ltv, -- Rough LTV estimate
    AVG(current_mrr_usd) as avg_mrr
FROM `nexus-analyst-demo.acme.dim_customers`
WHERE status = 'active'
GROUP BY 1
HAVING total_customers > 5
ORDER BY est_2yr_ltv DESC;

-- 2026-04-12 08:30:15 | user=sarah.jenkins@acme.io | job_id=bq_6112_ops | bytes_billed=8589934592 | duration_ms=4200 | status=DONE
-- Ops: Identify "Seat Overages" - customers where active user count exceeds licensed seat count.
-- Candidates for automated true-up emails.
WITH active_user_counts AS (
    SELECT 
        customer_id, 
        COUNT(user_id) as actual_active_users
    FROM `nexus-analyst-demo.acme.dim_users`
    WHERE is_active = true
    GROUP BY 1
)
SELECT 
    c.company_name,
    c.customer_id,
    c.seat_count_licensed,
    u.actual_active_users,
    (u.actual_active_users - c.seat_count_licensed) as overage_count,
    e.full_name as ae_owner
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN active_user_counts u ON c.customer_id = u.customer_id
JOIN `nexus-analyst-demo.acme.dim_employees` e ON c.ae_employee_id = e.employee_id
WHERE u.actual_active_users > c.seat_count_licensed
  AND c.status = 'active'
ORDER BY overage_count DESC;

-- 2026-05-01 13:10:02 | user=malik.dubois@acme.io | job_id=bq_7004_cs | bytes_billed=10737418240 | duration_ms=7800 | status=DONE
-- CS: Quarterly Business Review (QBR) data for "Tech-Solutions-Global" (CUST-442).
-- Monthly workflow volume trend + top error codes for their workflows.
SELECT 
    FORMAT_DATE('%Y-%m', triggered_at) as month,
    status,
    COUNT(*) as run_count,
    AVG(duration_ms) as avg_latency
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE customer_id = 'CUST-442'
  AND triggered_at >= '2025-05-01'
GROUP BY 1, 2
ORDER BY 1 DESC;

-- 2026-05-02 11:00:55 | user=chen.wei@acme.io | job_id=bq_7055_fin | bytes_billed=21474836480 | duration_ms=11200 | status=DONE
-- Finance: Net Revenue Retention (NRR) Calculation.
-- Compares MRR from the same set of customers exactly one year apart.
WITH customers_may_2025 AS (
    SELECT 
        customer_id,
        mrr_usd as mrr_start
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE '2025-05-01' BETWEEN start_date AND end_date
      AND plan_tier != 'Free'
),
customers_may_2026 AS (
    SELECT 
        customer_id,
        mrr_usd as mrr_end
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE '2026-05-01' BETWEEN start_date AND end_date
)
SELECT 
    SUM(s.mrr_start) as base_mrr,
    SUM(COALESCE(e.mrr_end, 0)) as retained_expansion_mrr,
    (SUM(COALESCE(e.mrr_end, 0)) / SUM(s.mrr_start)) * 100 as nrr_pct
FROM customers_may_2025 s
LEFT JOIN customers_may_2026 e ON s.customer_id = e.customer_id;

-- 2026-05-03 09:15:20 | user=junior.analyst@acme.io | job_id=bq_7101_dev | bytes_billed=0 | duration_ms=15 | status=ERROR
-- Dev: Quick check of plan IDs.
-- ERROR: Field 'tier_name' does not exist in dim_plans.
SELECT tier_name, monthly_price_per_seat_usd 
FROM `nexus-analyst-demo.acme.dim_plans`;

-- 2026-05-03 15:45:10 | user=sarah.jenkins@acme.io | job_id=bq_7150_sales | bytes_billed=536870912 | duration_ms=900 | status=DONE
-- Sales: Lead to Customer velocity.
-- Measuring days between user signup and the account becoming a paid tier.
SELECT 
    c.customer_id,
    c.company_name,
    c.signup_date,
    MIN(s.start_date) as first_paid_date,
    DATE_DIFF(MIN(s.start_date), c.signup_date, DAY) as days_to_conversion
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.fact_subscriptions` s ON c.customer_id = s.customer_id
WHERE s.plan_tier IN ('Pro', 'Business', 'Enterprise')
GROUP BY 1, 2, 3
HAVING days_to_conversion >= 0
LIMIT 100;

-- 2026-01-15 08:42:11 | user=m.petrov@acme.io | job_id=bq_8221_mkt | bytes_billed=1073741824 | duration_ms=2100 | status=DONE
-- Marketing: Top acquisition channels for Enterprise accounts in EMEA.
-- Need to verify if 'referral' is outperforming 'direct' for the Benelux region.
SELECT 
    acquisition_channel,
    region,
    COUNT(customer_id) as total_ent_customers,
    SUM(current_mrr_usd) * 12 as estimated_arr
FROM `nexus-analyst-demo.acme.dim_customers`
WHERE account_tier = 'Enterprise'
  AND region = 'EMEA'
GROUP BY 1, 2
ORDER BY 4 DESC;

-- 2026-01-20 14:10:05 | user=data-pipeline-sa@acme.io | job_id=bq_9001_sys | bytes_billed=0 | duration_ms=45 | status=ERROR
-- System: Automated dbt freshness check.
-- ERROR: Table `nexus-analyst-demo.acme.fact_active_users` not found. Did someone rename the mart?
SELECT MAX(last_login_date) FROM `nexus-analyst-demo.acme.fact_active_users`;

-- 2026-02-04 10:30:45 | user=diego.rodriguez@acme.io | job_id=bq_9112_eng | bytes_billed=8589934592 | duration_ms=4500 | status=DONE
-- Eng: Investigation into workflow failure spikes for CUST-612 (Globex Corp).
-- Seeing high rate of 'ERR_TIMEOUT_09' in the last 48 hours.
SELECT 
    DATE(triggered_at) as run_date,
    error_code,
    COUNT(*) as fail_count,
    AVG(duration_ms) as avg_duration
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE customer_id = 'CUST-612'
  AND status = 'FAILED'
  AND triggered_at >= '2026-02-02'
GROUP BY 1, 2
ORDER BY 1 DESC;

-- 2026-02-12 16:22:19 | user=sarah.jenkins@acme.io | job_id=bq_9250_sales | bytes_billed=2147483648 | duration_ms=1800 | status=DONE
-- Sales: Checking seat utilization for renewal conversations.
-- Customers on Business tier with >90% seat occupancy.
SELECT 
    c.customer_id,
    c.company_name,
    c.seat_count_licensed,
    COUNT(u.user_id) as active_user_count,
    (COUNT(u.user_id) / CAST(c.seat_count_licensed AS FLOAT64)) * 100 as utilization_pct
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_users` u ON c.customer_id = u.customer_id
WHERE c.current_plan_tier = 'Business'
  AND u.is_active = TRUE
  AND c.status = 'active'
GROUP BY 1, 2, 3
HAVING utilization_pct > 90
ORDER BY 5 DESC;

-- 2026-03-01 09:05:33 | user=chen.wei@acme.io | job_id=bq_9500_fin | bytes_billed=12884901888 | duration_ms=8900 | status=DONE
-- Finance: Q1 End-of-Month ARR by Industry.
-- Snapshot for the board deck. Includes churned accounts to balance the walk.
SELECT 
    industry,
    SUM(CASE WHEN status = 'active' THEN current_mrr_usd * 12 ELSE 0 END) as active_arr,
    SUM(CASE WHEN status = 'churned' AND churn_date >= '2026-01-01' THEN current_mrr_usd * 12 ELSE 0 END) as churned_arr_ytd
FROM `nexus-analyst-demo.acme.dim_customers`
GROUP BY 1
ORDER BY 2 DESC;

-- 2026-03-12 11:45:10 | user=junior.analyst@acme.io | job_id=bq_9612_dev | bytes_billed=536870912 | duration_ms=700 | status=DONE
-- Dev: Simple check on user signup lag.
-- Are domains like gmail.com still our biggest signup source?
SELECT 
    email_domain,
    COUNT(*) as user_count,
    MIN(signup_date) as first_signup
FROM `nexus-analyst-demo.acme.dim_users`
WHERE email_domain NOT IN ('acme.io')
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10;

-- 2026-03-22 13:12:55 | user=amara.okafor@acme.io | job_id=bq_9788_cs | bytes_billed=32212254720 | duration_ms=15400 | status=DONE
-- CS: Heavy query to find "At Risk" customers.
-- Criteria: Business tier, < 5 workflow runs in the last 30 days, AND > 50 licensed seats.
WITH recent_usage AS (
    SELECT 
        customer_id,
        COUNT(run_id) as run_count
    FROM `nexus-analyst-demo.acme.fact_workflow_runs`
    WHERE triggered_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
    GROUP BY 1
)
SELECT 
    c.customer_id,
    c.company_name,
    c.current_mrr_usd,
    c.seat_count_licensed,
    COALESCE(r.run_count, 0) as runs_last_30d,
    e.full_name as csm_name
FROM `nexus-analyst-demo.acme.dim_customers` c
LEFT JOIN recent_usage r ON c.customer_id = r.customer_id
LEFT JOIN `nexus-analyst-demo.acme.dim_employees` e ON c.csm_employee_id = e.employee_id
WHERE c.current_plan_tier = 'Business'
  AND c.status = 'active'
  AND COALESCE(r.run_count, 0) < 5
  AND c.seat_count_licensed >= 50;

-- 2026-03-28 17:01:04 | user=chen.wei@acme.io | job_id=bq_9899_fin | bytes_billed=4294967296 | duration_ms=3100 | status=DONE
-- Finance: Average Revenue Per User (ARPU) by plan.
-- Note: Using seat_count from fact_subscriptions for historical accuracy over dim_customers.
SELECT 
    plan_tier,
    AVG(mrr_usd / NULLIF(seat_count, 0)) as avg_arpu_per_seat
FROM `nexus-analyst-demo.acme.fact_subscriptions`
WHERE is_current = TRUE
  AND plan_tier != 'Free'
GROUP BY 1;

-- 2026-04-02 08:30:12 | user=data-pipeline-sa@acme.io | job_id=bq_9910_sys | bytes_billed=0 | duration_ms=12 | status=ERROR
-- System: Daily invoice reconciliation.
-- ERROR: Column 'invoice_total' does not exist in fact_invoices. Use 'amount_usd'.
SELECT 
    invoice_id, 
    invoice_total 
FROM `nexus-analyst-demo.acme.fact_invoices` 
WHERE status = 'unpaid';

-- 2026-04-15 14:22:33 | user=sarah.jenkins@acme.io | job_id=bq_9955_sales | bytes_billed=1073741824 | duration_ms=1100 | status=DONE
-- Sales: Upsell target list.
-- Customers on Pro plan paying more than $2000/mo (approaching Business tier min-seats value).
SELECT 
    customer_id,
    company_name,
    current_mrr_usd,
    seat_count_licensed
FROM `nexus-analyst-demo.acme.dim_customers`
WHERE current_plan_tier = 'Pro'
  AND current_mrr_usd >= 2000
  AND status = 'active'
ORDER BY current_mrr_usd DESC;

-- 2026-04-29 11:15:00 | user=diego.rodriguez@acme.io | job_id=bq_9999_eng | bytes_billed=53687091200 | duration_ms=28000 | status=DONE
-- Eng: Audit of most expensive workflows by step count and frequency.
-- Just making sure no single customer is DOSing the worker nodes.
SELECT 
    f.customer_id,
    c.company_name,
    f.workflow_id,
    COUNT(*) as total_runs,
    AVG(f.step_count) as avg_steps,
    MAX(f.duration_ms) as max_duration
FROM `nexus-analyst-demo.acme.fact_workflow_runs` f
JOIN `nexus-analyst-demo.acme.dim_customers` c ON f.customer_id = c.customer_id
WHERE f.triggered_at >= '2026-04-01'
GROUP BY 1, 2, 3
HAVING total_runs > 10000
ORDER BY total_runs DESC;

-- 2026-05-01 09:15:22 | user=marcus.lopez@acme.io | job_id=bq_10021_mkt | bytes_billed=2147483648 | duration_ms=4200 | status=DONE
-- Marketing: Channel performance for Q1 2026.
-- Looking for high-intent signup sources vs actual converted MRR.
SELECT 
    c.acquisition_channel,
    COUNT(DISTINCT c.customer_id) as total_signups,
    SUM(s.mrr_usd) as total_new_mrr,
    AVG(s.mrr_usd) as avg_deal_size
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.fact_subscriptions` s ON c.customer_id = s.customer_id
WHERE c.signup_date BETWEEN '2026-01-01' AND '2026-03-31'
  AND s.change_type = 'new_subscription'
  AND s.is_current = TRUE
GROUP BY 1
ORDER BY total_new_mrr DESC;

-- 2026-05-01 10:45:11 | user=elara.vance@acme.io | job_id=bq_10034_cs | bytes_billed=536870912 | duration_ms=850 | status=DONE
-- CS: High-risk Enterprise health check. 
-- Checking workflow success rate for 'CUST-8821' (Global Synergy Corp) over last 7 days.
SELECT 
    status,
    COUNT(*) as run_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as pct_of_total
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE customer_id = 'CUST-8821'
  AND triggered_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
GROUP BY 1;

-- 2026-05-01 13:02:44 | user=chen.wei@acme.io | job_id=bq_10045_fin | bytes_billed=12884901888 | duration_ms=14500 | status=DONE
-- Finance: MoM Net Revenue Retention (NRR) Calculation.
-- Comparing cohort from April 2025 to their value in April 2026.
WITH cohort_base AS (
    SELECT 
        customer_id,
        mrr_usd as starting_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE '2025-04-01' BETWEEN start_date AND end_date
      AND plan_tier != 'Free'
),
current_state AS (
    SELECT 
        customer_id,
        mrr_usd as current_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE is_current = TRUE
      AND plan_tier != 'Free'
)
SELECT 
    SUM(COALESCE(curr.current_mrr, 0)) / SUM(base.starting_mrr) * 100 as nrr_pct
FROM cohort_base base
LEFT JOIN current_state curr ON base.customer_id = curr.customer_id;

-- 2026-05-02 09:00:05 | user=data-pipeline-sa@acme.io | job_id=bq_10088_sys | bytes_billed=0 | duration_ms=5 | status=ERROR
-- System: Weekly user activity aggregation.
-- ERROR: Table name typo. 'dim_user_active' does not exist.
SELECT 
    customer_id, 
    COUNT(user_id) 
FROM `nexus-analyst-demo.acme.dim_user_active` 
GROUP BY 1;

-- 2026-05-02 11:12:30 | user=nina.gupta@acme.io | job_id=bq_10102_prod | bytes_billed=32212254720 | duration_ms=19000 | status=DONE
-- Product: Feature Adoption Analysis.
-- Percent of active users per customer who have triggered a workflow in the last 30 days.
WITH user_activity AS (
    SELECT 
        user_id,
        customer_id,
        COUNT(*) as event_count
    FROM `nexus-analyst-demo.acme.fact_user_events`
    WHERE event_type = 'workflow_executed'
      AND event_at >= '2026-04-01'
    GROUP BY 1, 2
),
customer_users AS (
    SELECT 
        customer_id,
        COUNT(user_id) as total_users
    FROM `nexus-analyst-demo.acme.dim_users`
    WHERE is_active = TRUE
    GROUP BY 1
)
SELECT 
    c.company_name,
    c.current_plan_tier,
    COUNT(ua.user_id) as active_users,
    cu.total_users,
    SAFE_DIVIDE(COUNT(ua.user_id), cu.total_users) as adoption_rate
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN customer_users cu ON c.customer_id = cu.customer_id
LEFT JOIN user_activity ua ON c.customer_id = ua.customer_id
WHERE c.status = 'active'
GROUP BY 1, 2, 4
HAVING total_users > 5
ORDER BY adoption_rate DESC;

-- 2026-05-03 15:44:12 | user=diego.rodriguez@acme.io | job_id=bq_10215_eng | bytes_billed=8589934592 | duration_ms=4100 | status=DONE
-- Eng: Latency percentiles by plan tier.
-- Seeing if Enterprise customers are getting better worker priority.
SELECT 
    c.current_plan_tier,
    PERCENTILE_CONT(f.duration_ms, 0.5) OVER(PARTITION BY c.current_plan_tier) as p50_latency,
    PERCENTILE_CONT(f.duration_ms, 0.95) OVER(PARTITION BY c.current_plan_tier) as p95_latency,
    PERCENTILE_CONT(f.duration_ms, 0.99) OVER(PARTITION BY c.current_plan_tier) as p99_latency
FROM `nexus-analyst-demo.acme.fact_workflow_runs` f
JOIN `nexus-analyst-demo.acme.dim_customers` c ON f.customer_id = c.customer_id
WHERE f.triggered_at >= '2026-04-25'
LIMIT 1000; -- Sampled for speed

-- 2026-05-04 08:20:01 | user=sarah.jenkins@acme.io | job_id=bq_10330_sales | bytes_billed=1073741824 | duration_ms=1200 | status=DONE
-- Sales: Regional ARR breakdown for Q2 Board Deck.
-- Need to split by EMEA vs North America based on dim_customers.region.
SELECT 
    region,
    SUM(current_mrr_usd * 12) as annual_recurring_revenue,
    COUNT(customer_id) as account_count
FROM `nexus-analyst-demo.acme.dim_customers`
WHERE status = 'active'
  AND current_plan_tier IN ('Business', 'Enterprise')
GROUP BY 1
ORDER BY annual_recurring_revenue DESC;

-- 2026-05-04 10:05:44 | user=lucas.kim@acme.io | job_id=bq_10345_ops | bytes_billed=536870912 | duration_ms=920 | status=DONE
-- Ops: Identify customers with seat_count mismatch.
-- Occurs when licensed seats in dim_customers != actual seats in current fact_subscriptions.
SELECT 
    c.customer_id,
    c.company_name,
    c.seat_count_licensed as dim_seats,
    s.seat_count as fact_seats,
    (c.seat_count_licensed - s.seat_count) as variance
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.fact_subscriptions` s ON c.customer_id = s.customer_id
WHERE s.is_current = TRUE
  AND c.seat_count_licensed != s.seat_count;

-- 2026-05-04 14:15:00 | user=chen.wei@acme.io | job_id=bq_10401_fin | bytes_billed=2147483648 | duration_ms=2100 | status=DONE
-- Finance: Outstanding aging report.
-- Total unpaid amount for invoices older than 30 days.
SELECT 
    c.company_name,
    i.invoice_id,
    i.invoice_date,
    i.amount_usd,
    DATE_DIFF(CURRENT_DATE(), i.invoice_date, DAY) as days_overdue
FROM `nexus-analyst-demo.acme.fact_invoices` i
JOIN `nexus-analyst-demo.acme.dim_customers` c ON i.customer_id = c.customer_id
WHERE i.status = 'unpaid'
  AND i.invoice_date <= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
ORDER BY days_overdue DESC;

-- 2026-02-15 09:12:44 | user=marcus.thorne@acme.io | job_id=bq_9100_cs | bytes_billed=8589934592 | duration_ms=4500 | status=DONE
-- CS: Quarterly Business Review (QBR) data for Global heavy hitters.
-- Looking for "low activity" flags on high MRR accounts (> $10k/mo).
WITH customer_activity AS (
    SELECT 
        c.customer_id,
        c.company_name,
        c.current_mrr_usd,
        COUNT(DISTINCT e.user_id) as active_users_30d,
        COUNT(r.run_id) as total_runs_30d
    FROM `nexus-analyst-demo.acme.dim_customers` c
    LEFT JOIN `nexus-analyst-demo.acme.fact_user_events` e ON c.customer_id = e.customer_id 
        AND e.event_at >= DATE_SUB('2026-02-15', INTERVAL 30 DAY)
    LEFT JOIN `nexus-analyst-demo.acme.fact_workflow_runs` r ON c.customer_id = r.customer_id
        AND r.triggered_at >= DATE_SUB('2026-02-15', INTERVAL 30 DAY)
    WHERE c.status = 'active'
      AND c.current_mrr_usd >= 10000
    GROUP BY 1, 2, 3
)
SELECT 
    *,
    CASE WHEN active_users_30d < 5 THEN 'AT_RISK_LOW_ADOPTION'
         WHEN total_runs_30d < 100 THEN 'AT_RISK_LOW_USAGE'
         ELSE 'HEALTHY' END as health_score
FROM customer_activity
ORDER BY current_mrr_usd DESC;

-- 2026-02-18 11:45:10 | user=elena.rodriguez@acme.io | job_id=bq_9122_de | bytes_billed=0 | duration_ms=105 | status=ERROR
-- DE: Validation check on staging.
-- ERROR: Table name typo. 'dim_customer' should be 'dim_customers'.
SELECT count(*) FROM `nexus-analyst-demo.acme.dim_customer` WHERE signup_date > '2026-01-01';

-- 2026-03-02 16:30:00 | user=jamie.vaughen@acme.io | job_id=bq_9455_prod | bytes_billed=12884901888 | duration_ms=8400 | status=DONE
-- Product: Feature Adoption - Workflow Step Distribution.
-- Which workflow steps are most common across different plan tiers?
-- Requires parsing event_properties if we had it, but using fact_workflow_runs for now.
SELECT 
    c.current_plan_tier,
    f.status,
    AVG(f.step_count) as avg_steps,
    MAX(f.step_count) as max_steps,
    APPROX_QUANTILES(f.duration_ms, 100)[OFFSET(50)] as median_duration_ms
FROM `nexus-analyst-demo.acme.fact_workflow_runs` f
JOIN `nexus-analyst-demo.acme.dim_customers` c ON f.customer_id = c.customer_id
WHERE f.triggered_at BETWEEN '2026-01-01' AND '2026-02-28'
GROUP BY 1, 2
ORDER BY 1, 3 DESC;

-- 2026-03-12 10:00:05 | user=sarah.jenkins@acme.io | job_id=bq_9501_rev | bytes_billed=4294967296 | duration_ms=3100 | status=DONE
-- RevOps: Net Revenue Retention (NRR) Calculation (Month-over-Month Cohort).
-- Comparing MRR of customers active 12 months ago to their MRR today.
WITH cohort_mar_2025 AS (
    SELECT 
        customer_id, 
        mrr_usd as starting_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE is_current = FALSE 
      AND '2025-03-12' BETWEEN start_date AND end_date
      AND plan_tier != 'Free'
),
current_revenue AS (
    SELECT 
        customer_id, 
        current_mrr_usd as ending_mrr
    FROM `nexus-analyst-demo.acme.dim_customers`
    WHERE status = 'active'
)
SELECT 
    SUM(c1.starting_mrr) as base_mrr,
    SUM(COALESCE(c2.ending_mrr, 0)) as retained_mrr,
    SAFE_DIVIDE(SUM(COALESCE(c2.ending_mrr, 0)), SUM(c1.starting_mrr)) * 100 as nrr_pct
FROM cohort_mar_2025 c1
LEFT JOIN current_revenue c2 ON c1.customer_id = c2.customer_id;

-- 2026-03-25 08:45:12 | user=lucas.kim@acme.io | job_id=bq_9822_ops | bytes_billed=536870912 | duration_ms=450 | status=DONE
-- Ops: Identify potential seat expansion targets in 'Business' tier.
-- Logic: seat_count_licensed is close to current active users.
SELECT 
    c.customer_id,
    c.company_name,
    c.seat_count_licensed,
    COUNT(DISTINCT u.user_id) as active_user_count,
    (c.seat_count_licensed - COUNT(DISTINCT u.user_id)) as seats_remaining
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_users` u ON c.customer_id = u.customer_id
WHERE c.current_plan_tier = 'Business'
  AND c.status = 'active'
  AND u.is_active = TRUE
GROUP BY 1, 2, 3
HAVING seats_remaining <= 2
ORDER BY seats_remaining ASC;

-- 2026-04-05 13:20:19 | user=chen.wei@acme.io | job_id=bq_10011_fin | bytes_billed=2147483648 | duration_ms=1800 | status=DONE
-- Finance: Billing cycle analysis. Annual vs Monthly MRR stability.
SELECT 
    billing_cycle,
    COUNT(DISTINCT customer_id) as account_count,
    SUM(mrr_usd) as total_mrr,
    AVG(mrr_usd) as avg_mrr_per_acct
FROM `nexus-analyst-demo.acme.fact_subscriptions`
WHERE is_current = TRUE
GROUP BY 1;

-- 2026-04-10 17:05:33 | user=marcus.thorne@acme.io | job_id=bq_10123_cs | bytes_billed=3221225472 | duration_ms=2900 | status=DONE
-- CS: Investigating high error rates for customer_id 'CUST-8821' (Skyline Logistics).
-- They reported issues with their ERP integration webhooks.
SELECT 
    error_code,
    COUNT(*) as error_count,
    MIN(triggered_at) as first_occurrence,
    MAX(triggered_at) as last_occurrence
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE customer_id = 'CUST-8821'
  AND status = 'failed'
  AND triggered_at >= '2026-04-01'
GROUP BY 1
ORDER BY error_count DESC;

-- 2026-04-15 09:15:00 | user=elena.rodriguez@acme.io | job_id=bq_10200_de | bytes_billed=10737418240 | duration_ms=12000 | status=DONE
-- DE: Monthly summary table for dim_dates join. 
-- Calculating platform-wide success rate by day.
SELECT 
    d.date,
    d.is_business_day,
    COUNT(f.run_id) as total_runs,
    COUNTIF(f.status = 'success') as successful_runs,
    SAFE_DIVIDE(COUNTIF(f.status = 'success'), COUNT(f.run_id)) as success_rate
FROM `nexus-analyst-demo.acme.dim_dates` d
LEFT JOIN `nexus-analyst-demo.acme.fact_workflow_runs` f ON DATE(f.triggered_at) = d.date
WHERE d.year = 2026 AND d.month = 4
GROUP BY 1, 2
ORDER BY 1;

-- 2026-04-20 11:33:01 | user=jamie.vaughen@acme.io | job_id=bq_10245_prod | bytes_billed=6442450944 | duration_ms=5400 | status=DONE
-- Product: Correlation between invited_by_user_id and user retention.
-- Checking if users invited by others stay active longer.
SELECT 
    CASE WHEN invited_by_user_id IS NULL THEN 'Organic' ELSE 'Invited' END as user_type,
    COUNT(user_id) as total_users,
    AVG(DATE_DIFF(last_login_date, signup_date, DAY)) as avg_lifetime_days
FROM `nexus-analyst-demo.acme.dim_users`
WHERE signup_date < '2026-03-01'
GROUP BY 1;

-- 2026-04-28 14:10:55 | user=sarah.jenkins@acme.io | job_id=bq_10299_sales | bytes_billed=1073741824 | duration_ms=900 | status=DONE
-- Sales: AE Performance tracking.
-- Total ARR closed by AE for current fiscal year.
SELECT 
    e.full_name as ae_name,
    c.account_tier,
    SUM(c.current_mrr_usd * 12) as total_arr_managed,
    COUNT(c.customer_id) as customer_count
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_employees` e ON c.ae_employee_id = e.employee_id
WHERE c.status = 'active'
GROUP BY 1, 2
ORDER BY total_arr_managed DESC;

-- 2026-01-12 08:44:12 | user=marcus.wong@acme.io | job_id=bq_09112_fin | bytes_billed=21474836480 | duration_ms=18400 | status=DONE
-- Finance: Gross Retention calculation for Jan cohort.
-- Looking for downgrades vs churns.
WITH monthly_mrr AS (
    SELECT 
        customer_id,
        DATE_TRUNC(start_date, MONTH) as mrr_month,
        SUM(mrr_usd) as total_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE is_current = true OR end_date >= '2026-01-01'
    GROUP BY 1, 2
),
prev_mrr AS (
    SELECT 
        customer_id,
        mrr_month,
        total_mrr,
        LAG(total_mrr) OVER(PARTITION BY customer_id ORDER BY mrr_month) as last_month_mrr
    FROM monthly_mrr
)
SELECT 
    mrr_month,
    SUM(last_month_mrr) as starting_mrr,
    SUM(CASE WHEN total_mrr < last_month_mrr THEN last_month_mrr - total_mrr ELSE 0 END) as contraction_mrr,
    SUM(CASE WHEN total_mrr = 0 AND last_month_mrr > 0 THEN last_month_mrr ELSE 0 END) as churn_mrr
FROM prev_mrr
WHERE mrr_month = '2026-01-01'
GROUP BY 1;

-- 2026-01-15 14:22:01 | user=chen.wei@acme.io | job_id=bq_09155_eng | bytes_billed=0 | duration_ms=120 | status=ERROR
-- ERROR: Table name not fully qualified. Requested: `acme.fact_workflow_runs`
SELECT 
    workflow_id,
    COUNT(*) as fail_count
FROM acme.fact_workflow_runs 
WHERE status = 'failed' 
  AND error_code = 'ERR_TIMEOUT_99'
GROUP BY 1;

-- 2026-02-04 10:12:45 | user=miguel.sanchez@acme.io | job_id=bq_09288_cs | bytes_billed=5368709120 | duration_ms=4100 | status=DONE
-- CS: High-touch customer health check for CUST-1042 (Globex Corp).
-- Comparing actual runs vs plan quota to signal potential overages.
SELECT 
    c.company_name,
    c.current_plan_tier,
    p.workflow_run_quota_per_month,
    COUNT(f.run_id) as actual_runs_feb,
    ROUND(COUNT(f.run_id) / p.workflow_run_quota_per_month * 100, 2) as quota_utilization_pct
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_plans` p ON c.current_plan_tier = p.plan_tier
JOIN `nexus-analyst-demo.acme.fact_workflow_runs` f ON c.customer_id = f.customer_id
WHERE c.customer_id = 'CUST-1042'
  AND f.triggered_at >= '2026-02-01'
  AND f.triggered_at < '2026-03-01'
GROUP BY 1, 2, 3;

-- 2026-02-18 16:05:30 | user=lisa.vanderbilt@acme.io | job_id=bq_09412_prod | bytes_billed=107374182400 | duration_ms=45000 | status=DONE
-- Product: Sticky features. Top events per user role for Enterprise tier.
SELECT 
    u.role,
    e.event_type,
    COUNT(*) as event_count,
    COUNT(DISTINCT u.user_id) as unique_users
FROM `nexus-analyst-demo.acme.fact_user_events` e
JOIN `nexus-analyst-demo.acme.dim_users` u ON e.user_id = u.user_id
JOIN `nexus-analyst-demo.acme.dim_customers` c ON u.customer_id = c.customer_id
WHERE c.account_tier = 'Enterprise'
  AND e.event_at >= '2026-01-01'
GROUP BY 1, 2
ORDER BY 1, 3 DESC;

-- 2026-03-02 09:00:15 | user=elena.rodriguez@acme.io | job_id=bq_09601_de | bytes_billed=12884901888 | duration_ms=8900 | status=DONE
-- DE: Weekly latency check for workflow execution by region.
SELECT 
    c.region,
    DATE_TRUNC(f.triggered_at, WEEK) as week_start,
    AVG(f.duration_ms) as avg_latency_ms,
    PERCENTILE_CONT(f.duration_ms, 0.95) OVER(PARTITION BY c.region, DATE_TRUNC(f.triggered_at, WEEK)) as p95_latency
FROM `nexus-analyst-demo.acme.fact_workflow_runs` f
JOIN `nexus-analyst-demo.acme.dim_customers` c ON f.customer_id = c.customer_id
WHERE f.triggered_at >= '2026-02-01'
QUALIFY p95_latency > 0 -- dummy qualify to use window
ORDER BY week_start DESC, avg_latency_ms DESC
LIMIT 100;

-- 2026-03-11 11:15:22 | user=sarah.jenkins@acme.io | job_id=bq_09744_sales | bytes_billed=1073741824 | duration_ms=1100 | status=DONE
-- Sales: Upsell targets. Pro customers with > 50 users (ready for Business tier).
SELECT 
    customer_id,
    company_name,
    seat_count_licensed,
    current_mrr_usd,
    signup_date
FROM `nexus-analyst-demo.acme.dim_customers`
WHERE current_plan_tier = 'Pro'
  AND seat_count_licensed >= 45
  AND status = 'active'
ORDER BY seat_count_licensed DESC;

-- 2026-03-25 15:55:01 | user=marcus.wong@acme.io | job_id=bq_09888_fin | bytes_billed=32212254720 | duration_ms=22000 | status=DONE
-- Finance: Q1 NRR (Net Revenue Retention) projection.
WITH q4_revenue AS (
    SELECT customer_id, SUM(amount_usd) as rev_q4
    FROM `nexus-analyst-demo.acme.fact_invoices`
    WHERE invoice_date BETWEEN '2025-10-01' AND '2025-12-31'
    AND status = 'paid'
    GROUP BY 1
),
q1_revenue AS (
    SELECT customer_id, SUM(amount_usd) as rev_q1
    FROM `nexus-analyst-demo.acme.fact_invoices`
    WHERE invoice_date BETWEEN '2026-01-01' AND '2026-03-31'
    AND status = 'paid'
    GROUP BY 1
)
SELECT 
    SAFE_DIVIDE(SUM(q1.rev_q1), SUM(q4.rev_q4)) * 100 as nrr_pct
FROM q4_revenue q4
JOIN q1_revenue q1 ON q4.customer_id = q1.customer_id;

-- 2026-04-02 13:02:10 | user=jamie.vaughen@acme.io | job_id=bq_10012_prod | bytes_billed=0 | duration_ms=45 | status=ERROR
-- ERROR: Field 'non_existent_column' not found in nexus-analyst-demo.acme.dim_users
SELECT user_id, non_existent_column FROM `nexus-analyst-demo.acme.dim_users` LIMIT 10;

-- 2026-04-10 17:40:33 | user=amanda.lee@acme.io | job_id=bq_10122_mkt | bytes_billed=8589934592 | duration_ms=6200 | status=DONE
-- Marketing: Channel efficiency by MRR.
SELECT 
    acquisition_channel,
    COUNT(customer_id) as acquisition_count,
    SUM(current_mrr_usd) as total_mrr,
    AVG(current_mrr_usd) as arpa
FROM `nexus-analyst-demo.acme.dim_customers`
WHERE signup_date >= '2025-01-01'
GROUP BY 1
ORDER BY total_mrr DESC;

-- 2026-04-18 09:20:00 | user=elena.rodriguez@acme.io | job_id=bq_10215_de | bytes_billed=42949672960 | duration_ms=31000 | status=DONE
-- DE: Data integrity check. Orphaned users without a valid customer_id in dim_customers.
SELECT 
    u.user_id,
    u.customer_id as user_cust_id,
    c.customer_id as parent_cust_id
FROM `nexus-analyst-demo.acme.dim_users` u
LEFT JOIN `nexus-analyst-demo.acme.dim_customers` c ON u.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

-- 2026-04-22 10:15:44 | user=liam.chen@acme.io | job_id=bq_10344_sls | bytes_billed=12884901888 | duration_ms=4100 | status=DONE
-- Sales: AE performance vs. current MRR book.
SELECT 
    e.full_name as ae_name,
    COUNT(c.customer_id) as account_count,
    SUM(c.current_mrr_usd) as total_managed_mrr,
    SUM(c.seat_count_licensed) as total_seats,
    AVG(c.current_mrr_usd) as avg_account_value
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_employees` e ON c.ae_employee_id = e.employee_id
WHERE c.status = 'active'
GROUP BY 1
ORDER BY total_managed_mrr DESC;

-- 2026-04-25 08:45:12 | user=sarah.jenkins@acme.io | job_id=bq_10488_cs | bytes_billed=214748364800 | duration_ms=88000 | status=DONE
-- CS: Identifying Enterprise accounts near workflow quota limits.
WITH usage_stats AS (
    SELECT 
        customer_id,
        COUNT(run_id) as monthly_runs
    FROM `nexus-analyst-demo.acme.fact_workflow_runs`
    WHERE triggered_at >= '2026-04-01'
    GROUP BY 1
)
SELECT 
    c.company_name,
    c.account_tier,
    u.monthly_runs,
    p.workflow_run_quota_per_month as quota,
    SAFE_DIVIDE(u.monthly_runs, p.workflow_run_quota_per_month) * 100 as percent_consumed
FROM usage_stats u
JOIN `nexus-analyst-demo.acme.dim_customers` c ON u.customer_id = c.customer_id
JOIN `nexus-analyst-demo.acme.dim_plans` p ON c.current_plan_tier = p.plan_tier
WHERE c.account_tier = 'Enterprise'
AND SAFE_DIVIDE(u.monthly_runs, p.workflow_run_quota_per_month) > 0.85;

-- 2026-04-26 14:12:05 | user=david.miller@acme.io | job_id=bq_10502_ops | bytes_billed=0 | duration_ms=12 | status=ERROR
-- ERROR: Table name typo 'fact_subscriptons'
SELECT * FROM `nexus-analyst-demo.acme.fact_subscriptons` LIMIT 100;

-- 2026-04-28 11:30:19 | user=marcus.wong@acme.io | job_id=bq_10599_fin | bytes_billed=53687091200 | duration_ms=42000 | status=DONE
-- Finance: MoM MRR Change (Expansion vs. Churn).
WITH monthly_mrr AS (
    SELECT 
        DATE_TRUNC(invoice_date, MONTH) as mrr_month,
        customer_id,
        SUM(amount_usd) as mrr
    FROM `nexus-analyst-demo.acme.fact_invoices`
    WHERE status = 'paid'
    GROUP BY 1, 2
),
mrr_with_lag AS (
    SELECT 
        *,
        LAG(mrr) OVER(PARTITION BY customer_id ORDER BY mrr_month) as prev_mrr
    FROM monthly_mrr
)
SELECT 
    mrr_month,
    SUM(CASE WHEN prev_mrr IS NULL THEN mrr ELSE 0 END) as new_mrr,
    SUM(CASE WHEN mrr > prev_mrr THEN mrr - prev_mrr ELSE 0 END) as expansion_mrr,
    SUM(CASE WHEN mrr < prev_mrr THEN mrr - prev_mrr ELSE 0 END) as contraction_mrr
FROM mrr_with_lag
GROUP BY 1
ORDER BY 1 DESC;

-- 2026-04-30 09:15:00 | user=amanda.lee@acme.io | job_id=bq_10677_mkt | bytes_billed=10737418240 | duration_ms=3500 | status=DONE
-- Marketing: Top 10 countries by active user growth in Q1.
SELECT 
    c.country,
    COUNT(DISTINCT u.user_id) as active_user_count
FROM `nexus-analyst-demo.acme.dim_users` u
JOIN `nexus-analyst-demo.acme.dim_customers` c ON u.customer_id = c.customer_id
WHERE u.last_login_date BETWEEN '2026-01-01' AND '2026-03-31'
AND u.is_active = TRUE
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10;

-- 2026-05-01 16:45:33 | user=jamie.vaughen@acme.io | job_id=bq_10722_prod | bytes_billed=32212254720 | duration_ms=15000 | status=DONE
-- Product: Workflow failure rates by industry (for Eng stability review).
SELECT 
    c.industry,
    COUNT(r.run_id) as total_runs,
    COUNT(CASE WHEN r.status = 'failed' THEN 1 END) as failure_count,
    ROUND(COUNT(CASE WHEN r.status = 'failed' THEN 1 END) / COUNT(r.run_id) * 100, 2) as failure_rate_pct
FROM `nexus-analyst-demo.acme.fact_workflow_runs` r
JOIN `nexus-analyst-demo.acme.dim_customers` c ON r.customer_id = c.customer_id
WHERE r.triggered_at >= '2026-04-01'
GROUP BY 1
HAVING total_runs > 1000
ORDER BY failure_rate_pct DESC;

-- 2026-05-02 11:20:12 | user=elena.rodriguez@acme.io | job_id=bq_10811_de | bytes_billed=1073741824 | duration_ms=800 | status=DONE
-- DE: Quick check on plan tier prices vs customer MRR.
SELECT 
    c.customer_id,
    c.company_name,
    c.current_plan_tier,
    c.seat_count_licensed,
    c.current_mrr_usd,
    (c.seat_count_licensed * p.monthly_price_per_seat_usd) as expected_mrr
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_plans` p ON c.current_plan_tier = p.plan_tier
WHERE c.status = 'active'
AND c.account_tier != 'Enterprise' -- Enterprise has custom pricing
LIMIT 50;

-- 2026-05-03 13:05:55 | user=sarah.jenkins@acme.io | job_id=bq_10922_cs | bytes_billed=4294967296 | duration_ms=1200 | status=DONE
-- CS: Check specific account usage (Customer ID: 742 - Globex Corp).
SELECT 
    triggered_at,
    status,
    duration_ms,
    error_code
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE customer_id = 'CUST-742'
AND triggered_at > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
ORDER BY triggered_at DESC;

-- 2026-05-04 09:00:10 | user=liam.chen@acme.io | job_id=bq_11001_sls | bytes_billed=2147483648 | duration_ms=1500 | status=DONE
-- Sales: Lead list of 'Free' tier customers with >10 users (Upsell targets).
SELECT 
    c.company_name,
    c.industry,
    COUNT(u.user_id) as user_count,
    c.signup_date
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_users` u ON c.customer_id = u.customer_id
WHERE c.current_plan_tier = 'Free'
AND c.status = 'active'
GROUP BY 1, 2, 4
HAVING user_count > 10
ORDER BY user_count DESC;

-- 2026-05-04 10:15:33 | user=marcus.wong@acme.io | job_id=bq_11045_fin | bytes_billed=5368709120 | duration_ms=2400 | status=DONE
-- Finance: Monthly NRR (Net Revenue Retention) calculation for Q1 2026.
WITH mrr_start AS (
    SELECT 
        customer_id, 
        SUM(mrr_usd) as start_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE start_date <= '2026-01-01' AND (end_date > '2026-01-01' OR end_date IS NULL)
    GROUP BY 1
),
mrr_end AS (
    SELECT 
        customer_id, 
        SUM(mrr_usd) as end_mrr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE start_date <= '2026-03-31' AND (end_date > '2026-03-31' OR end_date IS NULL)
    GROUP BY 1
)
SELECT 
    SUM(CASE WHEN s.customer_id IN (SELECT customer_id FROM mrr_start) THEN e.end_mrr ELSE 0 END) / 
    NULLIF(SUM(s.start_mrr), 0) as nrr_q1
FROM mrr_start s
LEFT JOIN mrr_end e ON s.customer_id = e.customer_id;

-- 2026-05-04 11:42:01 | user=jake.miller@acme.io | job_id=bq_11089_eng | bytes_billed=0 | duration_ms=45 | status=FAILED
-- DE: Testing new schema path for workflow logs (oops, typo in table name)
SELECT * FROM `nexus-analyst-demo.acme.fact_workflow_run_logs_v2` LIMIT 10;
-- ERROR: Table not found: nexus-analyst-demo.acme.fact_workflow_run_logs_v2

-- 2026-05-04 13:22:15 | user=anya.petrova@acme.io | job_id=bq_11202_prod | bytes_billed=8589934592 | duration_ms=3100 | status=DONE
-- Product: Feature stickiness. Who is creating workflows but not running them?
SELECT 
    c.customer_id,
    c.company_name,
    COUNT(DISTINCT e.event_id) as workflows_created,
    COUNT(DISTINCT r.run_id) as total_runs
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.fact_user_events` e ON c.customer_id = e.customer_id
LEFT JOIN `nexus-analyst-demo.acme.fact_workflow_runs` r ON c.customer_id = r.customer_id
WHERE e.event_type = 'workflow_created'
AND e.event_at >= '2026-04-01'
GROUP BY 1, 2
HAVING workflows_created > 0 AND total_runs = 0
ORDER BY workflows_created DESC;

-- 2026-05-04 14:05:09 | user=sarah.jenkins@acme.io | job_id=bq_11250_cs | bytes_billed=1073741824 | duration_ms=900 | status=DONE
-- CS: Priority check for 'SkyNet Partners' (CUST-912) - health score components.
SELECT 
    c.company_name,
    c.current_plan_tier,
    COUNT(DISTINCT u.user_id) as active_users,
    SUM(r.duration_ms) / 1000 / 60 as total_compute_minutes,
    AVG(CASE WHEN r.status = 'failed' THEN 1 ELSE 0 END) as failure_rate
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_users` u ON c.customer_id = u.customer_id
JOIN `nexus-analyst-demo.acme.fact_workflow_runs` r ON c.customer_id = r.customer_id
WHERE c.customer_id = 'CUST-912'
AND r.triggered_at > '2026-04-01'
GROUP BY 1, 2;

-- 2026-05-04 15:30:44 | user=elena.rodriguez@acme.io | job_id=bq_11388_de | bytes_billed=12884901888 | duration_ms=4200 | status=DONE
-- DE: Monthly ARR bridge query for April. 
-- Includes Expansion, Contraction, Churn, and New Biz.
WITH monthly_mrr AS (
    SELECT 
        customer_id,
        date_trunc(invoice_date, MONTH) as billing_month,
        SUM(amount_usd) as total_mrr
    FROM `nexus-analyst-demo.acme.fact_invoices`
    WHERE status = 'paid'
    GROUP BY 1, 2
),
mrr_comparison AS (
    SELECT 
        curr.customer_id,
        curr.billing_month,
        curr.total_mrr as curr_mrr,
        prev.total_mrr as prev_mrr
    FROM monthly_mrr curr
    LEFT JOIN monthly_mrr prev ON curr.customer_id = prev.customer_id 
        AND curr.billing_month = DATE_ADD(prev.billing_month, INTERVAL 1 MONTH)
    WHERE curr.billing_month = '2026-04-01'
)
SELECT 
    SUM(CASE WHEN prev_mrr IS NULL THEN curr_mrr ELSE 0 END) as new_biz_arr,
    SUM(CASE WHEN curr_mrr > prev_mrr THEN curr_mrr - prev_mrr ELSE 0 END) as expansion_arr,
    SUM(CASE WHEN curr_mrr < prev_mrr THEN curr_mrr - prev_mrr ELSE 0 END) as contraction_arr,
    (SELECT -SUM(total_mrr) FROM monthly_mrr WHERE billing_month = '2026-03-01' 
     AND customer_id NOT IN (SELECT customer_id FROM monthly_mrr WHERE billing_month = '2026-04-01')) as churn_arr
FROM mrr_comparison;

-- 2026-05-04 16:10:22 | user=liam.chen@acme.io | job_id=bq_11410_sls | bytes_billed=4294967296 | duration_ms=1100 | status=DONE
-- Sales: AE leader board by closed ARR in 2026 YTD.
SELECT 
    e.full_name as ae_name,
    COUNT(c.customer_id) as logos_closed,
    SUM(c.current_mrr_usd * 12) as arr_closed
FROM `nexus-analyst-demo.acme.dim_employees` e
JOIN `nexus-analyst-demo.acme.dim_customers` c ON e.employee_id = c.ae_employee_id
WHERE e.team = 'Sales'
AND c.signup_date >= '2026-01-01'
AND c.status = 'active'
GROUP BY 1
ORDER BY arr_closed DESC;

-- 2026-05-04 17:01:55 | user=chloe.smith@acme.io | job_id=bq_11502_mkt | bytes_billed=2147483648 | duration_ms=1800 | status=DONE
-- Marketing: Attribution check. Which channels drive the highest 'Business' tier conversions?
SELECT 
    acquisition_channel,
    COUNT(customer_id) as total_customers,
    SUM(CASE WHEN current_plan_tier = 'Business' THEN 1 ELSE 0 END) as business_tier_count,
    ROUND(SUM(CASE WHEN current_plan_tier = 'Business' THEN 1 ELSE 0 END) / COUNT(customer_id) * 100, 2) as conversion_rate
FROM `nexus-analyst-demo.acme.dim_customers`
WHERE signup_date >= '2025-01-01'
GROUP BY 1
ORDER BY conversion_rate DESC;

-- 2026-05-04 17:45:10 | user=marcus.wong@acme.io | job_id=bq_11599_fin | bytes_billed=6442450944 | duration_ms=2100 | status=DONE
-- Finance: Audit invoice vs seat license mismatch.
SELECT 
    c.customer_id,
    c.company_name,
    c.seat_count_licensed,
    i.amount_usd as last_invoice_amt,
    p.monthly_price_per_seat_usd,
    (c.seat_count_licensed * p.monthly_price_per_seat_usd) as calculated_amt,
    i.amount_usd - (c.seat_count_licensed * p.monthly_price_per_seat_usd) as variance
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_plans` p ON c.current_plan_tier = p.plan_tier
JOIN `nexus-analyst-demo.acme.fact_invoices` i ON c.customer_id = i.customer_id
WHERE i.invoice_date >= '2026-04-01'
AND c.account_tier != 'Enterprise'
AND ABS(i.amount_usd - (c.seat_count_licensed * p.monthly_price_per_seat_usd)) > 1
ORDER BY variance DESC;

-- 2026-05-04 18:20:00 | user=system_cron@acme.io | job_id=bq_sched_9921 | bytes_billed=1073741824 | duration_ms=300 | status=DONE
-- SYSTEM: Daily health check on data freshnes.
SELECT MAX(triggered_at) as last_workflow_run_at FROM `nexus-analyst-demo.acme.fact_workflow_runs`;

-- 2026-02-15 09:12:44 | user=dave.chen@acme.io | job_id=bq_88201_prod | bytes_billed=4294967296 | duration_ms=3100 | status=DONE
-- Product: Investigating workflow failure spikes by error code for the Top 10 high-volume accounts.
WITH account_usage AS (
    SELECT 
        customer_id, 
        COUNT(*) as total_runs
    FROM `nexus-analyst-demo.acme.fact_workflow_runs`
    WHERE triggered_at >= '2026-01-01'
    GROUP BY 1
    ORDER BY total_runs DESC
    LIMIT 10
)
SELECT 
    c.company_name,
    f.error_code,
    COUNT(*) as error_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(PARTITION BY c.customer_id), 2) as error_rate_pct
FROM `nexus-analyst-demo.acme.fact_workflow_runs` f
JOIN account_usage au ON f.customer_id = au.customer_id
JOIN `nexus-analyst-demo.acme.dim_customers` c ON f.customer_id = c.customer_id
WHERE f.status = 'FAILED'
AND f.triggered_at >= '2026-02-01'
GROUP BY 1, 2
ORDER BY error_count DESC;

-- 2026-02-15 10:05:12 | user=marcus.wong@acme.io | job_id=bq_88245_fin | bytes_billed=0 | duration_ms=45 | status=ERROR
-- ERROR: Table not found: nexus-analyst-demo.dim_customers. Forgot the .acme. prefix again. 
SELECT company_name, current_mrr_usd FROM `nexus-analyst-demo.dim_customers` WHERE customer_id = 'CUST-9921';

-- 2026-02-15 11:45:30 | user=sarah.jenkins@acme.io | job_id=bq_88310_cs | bytes_billed=1073741824 | duration_ms=950 | status=DONE
-- CS: Quick health check for 'Cyberdyne Systems' (ID: 215) before the QBR. 
-- Need to see active user count vs licensed seats.
SELECT 
    c.company_name,
    c.seat_count_licensed,
    COUNT(DISTINCT u.user_id) as active_users_30d,
    c.current_plan_tier,
    c.current_mrr_usd
FROM `nexus-analyst-demo.acme.dim_customers` c
LEFT JOIN `nexus-analyst-demo.acme.dim_users` u ON c.customer_id = u.customer_id
WHERE c.customer_id = '215'
AND u.last_login_date >= '2026-01-15'
AND u.is_active = TRUE
GROUP BY 1, 2, 4, 5;

-- 2026-02-16 14:22:01 | user=marcus.wong@acme.io | job_id=bq_89102_fin | bytes_billed=12884901888 | duration_ms=12400 | status=DONE
-- Finance: Gross NRR (Net Revenue Retention) calculation for Q1. 
-- This is going to be messy because of the self-serve to sales-led transitions.
WITH monthly_mrr AS (
    SELECT 
        customer_id,
        DATE_TRUNC(invoice_date, MONTH) as mrr_month,
        SUM(amount_usd) as total_mrr
    FROM `nexus-analyst-demo.acme.fact_invoices`
    WHERE status = 'PAID'
    AND invoice_date BETWEEN '2025-01-01' AND '2026-03-01'
    GROUP BY 1, 2
),
retention_pivot AS (
    SELECT 
        customer_id,
        mrr_month,
        total_mrr,
        LAG(total_mrr) OVER(PARTITION BY customer_id ORDER BY mrr_month) as prev_month_mrr
    FROM monthly_mrr
)
SELECT 
    mrr_month,
    SUM(prev_month_mrr) as starting_mrr,
    SUM(total_mrr) as ending_mrr,
    ROUND((SUM(total_mrr) / NULLIF(SUM(prev_month_mrr), 0)) * 100, 2) as nrr_pct
FROM retention_pivot
WHERE prev_month_mrr IS NOT NULL
GROUP BY 1
ORDER BY 1 DESC;

-- 2026-02-16 16:10:55 | user=chloe.smith@acme.io | job_id=bq_89554_mkt | bytes_billed=5368709120 | duration_ms=4100 | status=DONE
-- Marketing: Identifying 'Free' tier domains with >10 users for conversion campaign.
-- Filtering for specific industries that we're targeting for the Pro->Business push.
SELECT 
    u.email_domain,
    c.company_name,
    c.industry,
    COUNT(u.user_id) as user_count,
    MAX(u.last_login_date) as last_activity
FROM `nexus-analyst-demo.acme.dim_users` u
JOIN `nexus-analyst-demo.acme.dim_customers` c ON u.customer_id = c.customer_id
WHERE c.current_plan_tier = 'Free'
AND c.status = 'active'
AND c.industry IN ('Fintech', 'Healthcare', 'E-commerce')
GROUP BY 1, 2, 3
HAVING user_count >= 10
ORDER BY user_count DESC;

-- 2026-02-17 08:30:00 | user=system_cron@acme.io | job_id=bq_sched_1010 | bytes_billed=2147483648 | duration_ms=1200 | status=DONE
-- SYSTEM: Weekly executive ARR snapshot by Region and Account Tier.
SELECT 
    region,
    account_tier,
    COUNT(customer_id) as total_accounts,
    SUM(current_mrr_usd * 12) as annual_recurring_revenue
FROM `nexus-analyst-demo.acme.dim_customers`
WHERE status = 'active'
GROUP BY 1, 2
ORDER BY region, annual_recurring_revenue DESC;

-- 2026-02-17 11:05:44 | user=dave.chen@acme.io | job_id=bq_90012_prod | bytes_billed=3221225472 | duration_ms=2800 | status=DONE
-- Product: Who is using the 'Custom SLA' feature in Enterprise? 
-- Need to map dim_plans attributes to actual usage logs.
SELECT 
    c.company_name,
    p.plan_tier,
    p.sla_uptime_pct,
    COUNT(f.run_id) as total_runs_feb
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_plans` p ON c.current_plan_tier = p.plan_tier
LEFT JOIN `nexus-analyst-demo.acme.fact_workflow_runs` f ON c.customer_id = f.customer_id
WHERE p.plan_tier = 'Enterprise'
AND f.triggered_at >= '2026-02-01'
GROUP BY 1, 2, 3
ORDER BY total_runs_feb DESC;

-- 2026-02-17 13:50:11 | user=marcus.wong@acme.io | job_id=bq_90222_fin | bytes_billed=0 | duration_ms=120 | status=ERROR
-- ERROR: Column 'ae_id' not found in dim_customers. It's 'ae_employee_id'.
SELECT 
    ae_id, 
    SUM(current_mrr_usd) 
FROM `nexus-analyst-demo.acme.dim_customers` 
GROUP BY 1;

-- 2026-02-17 15:45:00 | user=sarah.jenkins@acme.io | job_id=bq_90881_cs | bytes_billed=8589934592 | duration_ms=5400 | status=DONE
-- CS: Identifying churn risk. Accounts with <2 active users and MRR > 1000.
WITH active_user_counts AS (
    SELECT 
        customer_id,
        COUNT(user_id) as active_user_count
    FROM `nexus-analyst-demo.acme.dim_users`
    WHERE is_active = TRUE
    AND last_login_date >= CURRENT_DATE() - 30
    GROUP BY 1
)
SELECT 
    c.customer_id,
    c.company_name,
    c.current_mrr_usd,
    c.account_tier,
    COALESCE(a.active_user_count, 0) as active_users
FROM `nexus-analyst-demo.acme.dim_customers` c
LEFT JOIN active_user_counts a ON c.customer_id = a.customer_id
WHERE c.status = 'active'
AND c.current_mrr_usd > 1000
AND COALESCE(a.active_user_count, 0) < 2
ORDER BY c.current_mrr_usd DESC;

-- 2026-02-18 09:12:33 | user=marcus.wong@acme.io | job_id=bq_91004_fin | bytes_billed=12884901888 | duration_ms=7200 | status=DONE
-- Finance: MoM MRR Growth and NRR calculation for Board Deck.
-- Comparing Jan 2026 vs Feb 2026 (partial).
WITH monthly_revenue AS (
    SELECT 
        d.month_name,
        d.year,
        SUM(fs.mrr_usd) as total_mrr,
        COUNT(DISTINCT fs.customer_id) as customer_count
    FROM `nexus-analyst-demo.acme.fact_subscriptions` fs
    JOIN `nexus-analyst-demo.acme.dim_dates` d ON fs.start_date <= d.date AND (fs.end_date > d.date OR fs.end_date IS NULL)
    WHERE d.date IN ('2026-01-31', '2026-02-28')
    GROUP BY 1, 2
)
SELECT 
    curr.month_name as current_month,
    curr.total_mrr as current_mrr,
    prev.total_mrr as prev_mrr,
    (curr.total_mrr - prev.total_mrr) / NULLIF(prev.total_mrr, 0) as mrr_growth_pct
FROM monthly_revenue curr
LEFT JOIN monthly_revenue prev ON curr.year = prev.year AND curr.month_name = 'February' AND prev.month_name = 'January';

-- 2026-02-18 10:44:12 | user=lindsey.walsh@acme.io | job_id=bq_91223_prod | bytes_billed=4294967296 | duration_ms=3100 | status=DONE
-- Product: Which industries are seeing the highest 'step_count' per workflow run?
-- Looking for "heavy" users for the new infrastructure tier.
SELECT 
    c.industry,
    AVG(f.step_count) as avg_steps,
    MAX(f.step_count) as max_steps,
    COUNT(f.run_id) as total_runs
FROM `nexus-analyst-demo.acme.fact_workflow_runs` f
JOIN `nexus-analyst-demo.acme.dim_customers` c ON f.customer_id = c.customer_id
WHERE f.triggered_at >= '2026-01-01'
GROUP BY 1
HAVING total_runs > 500
ORDER BY avg_steps DESC;

-- 2026-02-18 13:02:55 | user=dave.chen@acme.io | job_id=bq_91550_sales | bytes_billed=0 | duration_ms=85 | status=ERROR
-- ERROR: Table 'nexus-analyst-demo.acme.dim_ae_mapping' not found. 
-- Dave: Dammit, I thought we flattened the AE data into dim_employees? 
SELECT 
    e.full_name,
    SUM(c.current_mrr_usd) 
FROM `nexus-analyst-demo.acme.dim_employees` e
JOIN `nexus-analyst-demo.acme.dim_customers` c ON e.employee_id = c.ae_employee_id
WHERE e.team = 'Sales'
GROUP BY 1;

-- 2026-02-18 13:05:10 | user=dave.chen@acme.io | job_id=bq_91551_sales | bytes_billed=1073741824 | duration_ms=1100 | status=DONE
-- Sales: AE Performance Leaderboard (Total Booked MRR). 
-- Note: 'ae_employee_id' in dim_customers links to 'employee_id' in dim_employees.
SELECT 
    e.full_name as account_executive,
    e.location,
    COUNT(c.customer_id) as account_count,
    ROUND(SUM(c.current_mrr_usd), 2) as total_managed_mrr,
    ROUND(AVG(c.current_mrr_usd), 2) as avg_deal_size
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_employees` e ON c.ae_employee_id = e.employee_id
WHERE c.status = 'active'
GROUP BY 1, 2
ORDER BY total_managed_mrr DESC;

-- 2026-02-19 08:30:15 | user=nina.patel@acme.io | job_id=bq_92001_mkt | bytes_billed=21474836480 | duration_ms=14200 | status=DONE
-- Marketing: LTV analysis by acquisition channel. 
-- Calculating total paid invoices per customer vs signup channel.
WITH customer_revenue AS (
    SELECT 
        customer_id,
        SUM(amount_usd) as total_lifetime_spend
    FROM `nexus-analyst-demo.acme.fact_invoices`
    WHERE status = 'paid'
    GROUP BY 1
)
SELECT 
    c.acquisition_channel,
    COUNT(c.customer_id) as customer_count,
    AVG(cr.total_lifetime_spend) as avg_ltv,
    SUM(cr.total_lifetime_spend) as total_channel_rev
FROM `nexus-analyst-demo.acme.dim_customers` c
LEFT JOIN customer_revenue cr ON c.customer_id = cr.customer_id
GROUP BY 1
ORDER BY avg_ltv DESC;

-- 2026-02-19 11:15:44 | user=marcus.wong@acme.io | job_id=bq_92442_fin | bytes_billed=5368709120 | duration_ms=4500 | status=DONE
-- Finance: Audit of 'Expansion' events in Feb. 
-- Specifically looking for seat_count increases on Business tier.
SELECT 
    c.company_name,
    fs.subscription_id,
    fs.seat_count as new_seat_count,
    fs.mrr_usd - prev.mrr_usd as mrr_delta,
    fs.start_date
FROM `nexus-analyst-demo.acme.fact_subscriptions` fs
JOIN `nexus-analyst-demo.acme.dim_customers` c ON fs.customer_id = c.customer_id
JOIN `nexus-analyst-demo.acme.fact_subscriptions` prev ON fs.changed_from_subscription_id = prev.subscription_id
WHERE fs.change_type = 'expansion'
AND fs.plan_tier = 'Business'
AND fs.start_date >= '2026-02-01'
ORDER BY mrr_delta DESC;

-- 2026-02-19 15:22:01 | user=sarah.jenkins@acme.io | job_id=bq_92888_cs | bytes_billed=1073741824 | duration_ms=900 | status=DONE
-- CS: Quick check on specific high-value account 'CUST-882' (TechFlow Systems).
-- They reported "slow runs" yesterday.
SELECT 
    run_id,
    status,
    duration_ms,
    triggered_at,
    error_code
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE customer_id = 'CUST-882'
AND triggered_at >= '2026-02-18'
ORDER BY duration_ms DESC
LIMIT 50;

-- 2026-02-20 09:05:33 | user=lindsey.walsh@acme.io | job_id=bq_93010_prod | bytes_billed=34359738368 | duration_ms=19500 | status=DONE
-- Product: Daily Active Users (DAU) by Region for last 30 days.
-- Expensive join across fact_user_events (massive) and dim_customers.
SELECT 
    d.date,
    c.region,
    COUNT(DISTINCT e.user_id) as dau
FROM `nexus-analyst-demo.acme.fact_user_events` e
JOIN `nexus-analyst-demo.acme.dim_customers` c ON e.customer_id = c.customer_id
JOIN `nexus-analyst-demo.acme.dim_dates` d ON CAST(e.event_at AS DATE) = d.date
WHERE d.date >= CURRENT_DATE() - 30
GROUP BY 1, 2
ORDER BY 1 DESC, 2 ASC;

-- 2026-02-20 10:40:12 | user=marcus.wong@acme.io | job_id=bq_93221_fin | bytes_billed=512000 | duration_ms=400 | status=DONE
-- Finance: List all pending Enterprise invoices over 30 days old.
SELECT 
    c.company_name,
    i.invoice_id,
    i.amount_usd,
    i.invoice_date,
    DATE_DIFF(CURRENT_DATE(), i.invoice_date, DAY) as days_overdue
FROM `nexus-analyst-demo.acme.fact_invoices` i
JOIN `nexus-analyst-demo.acme.dim_customers` c ON i.customer_id = c.customer_id
WHERE i.status = 'open'
AND i.invoice_date <= CURRENT_DATE() - 30
AND c.account_tier = 'Ent'
ORDER BY amount_usd DESC;