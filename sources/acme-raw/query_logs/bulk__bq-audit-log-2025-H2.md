---
title: "BigQuery JOBS_BY_USER audit export — 2025 H2"
source_url: "internal://acme/bq-audit-log-2025-H2"
license: "synthetic-demo"
attribution: "Synthetic content, Acme Inc internal demo. Acme Inc is a fictitious company."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: query_log
---

-- 2025-07-01T08:12:44Z | user=rajiv.menon@acme.io | job_x7a2k1 | 450392 | 1240 | SUCCESS
SELECT table_name FROM `nexus-analyst-demo.acme.INFORMATION_SCHEMA.TABLES` WHERE table_schema = 'acme';

-- 2025-07-01T08:14:02Z | user=rajiv.menon@acme.io | job_b2n81m | 120485 | 890 | SUCCESS
DESCRIBE `nexus-analyst-demo.acme.fact_workflow_runs`;

-- 2025-07-01T09:45:12Z | user=lina.cho@acme.io | job_p9z3l0 | 8921044 | 4500 | SUCCESS
-- Monthly ARR check for June close
SELECT 
  SUM(current_mrr_usd) * 12 as est_arr 
FROM `nexus-analyst-demo.acme.dim_customers` 
WHERE status = 'active' AND current_plan_tier != 'Free';

-- 2025-07-01T10:02:15Z | user=david.kim@acme.io | job_f2v1s9 | 55670221 | 12400 | SUCCESS
SELECT 
  customer_id, 
  COUNT(run_id) as total_runs, 
  status 
FROM `nexus-analyst-demo.acme.fact_workflow_runs` 
WHERE triggered_at >= '2025-06-01' 
GROUP BY 1, 3 
ORDER BY 2 DESC 
LIMIT 100;

-- 2025-07-02T11:20:00Z | user=lina.cho@acme.io | job_a1c3v8 | 0 | 120 | ERROR: Table not found
-- Trying to use old mart path from the dbt folder structure
SELECT * FROM `nexus-analyst-demo.acme.marts.finance.arr_snapshot` LIMIT 10;

-- 2025-07-02T11:21:05Z | user=lina.cho@acme.io | job_k4m1q2 | 45032 | 410 | SUCCESS
-- Fixed path
SELECT * FROM `nexus-analyst-demo.acme.arr_snapshot` ORDER BY snapshot_date DESC LIMIT 5;

-- 2025-07-05T14:30:11Z | user=nina.patel@acme.io | job_q9r0t4 | 1289400 | 1100 | SUCCESS
-- Checking for duplicate subscriptions
SELECT 
  customer_id, 
  COUNT(*) as cnt 
FROM `nexus-analyst-demo.acme.fact_subscriptions` 
WHERE is_current = TRUE 
GROUP BY 1 
HAVING cnt > 1;

-- 2025-07-08T09:15:33Z | user=olivia.tran@acme.io | job_h3n1x0 | 90234 | 600 | SUCCESS
-- CSM check for Marigold Health
SELECT * 
FROM `nexus-analyst-demo.acme.account_health` 
WHERE customer_id = 'cust_000701';

-- 2025-07-10T16:44:22Z | user=jorge.martinez@acme.io | job_m2l8p3 | 210455 | 950 | SUCCESS
-- RevOps: Looking at Q2 bookings
SELECT 
  first_touch_channel, 
  SUM(bookings_acv_usd) as total_bookings 
FROM `nexus-analyst-demo.acme.bookings_attribution` 
WHERE closed_won_at BETWEEN '2025-04-01' AND '2025-06-30' 
GROUP BY 1;

-- 2025-07-10T16:55:01Z | user=jorge.martinez@acme.io | job_v1b5n2 | 210455 | 880 | SUCCESS
-- WAIT - double check if ACV needs multiplier. Sam said bookings_acv_usd is already annual. 
-- Testing the wrong assumption just to see delta.
SELECT 
  SUM(bookings_acv_usd) as acv_raw, 
  SUM(bookings_acv_usd * 12) as acv_multiplied_wrong 
FROM `nexus-analyst-demo.acme.bookings_attribution` 
WHERE closed_won_at >= '2025-01-01';

-- 2025-07-12T13:12:12Z | user=rajiv.menon@acme.io | job_n7m4z1 | 8902334 | 3400 | SUCCESS
-- Refactoring NRR cohort logic. 
-- This is the INNER JOIN version which is WRONG because it excludes churns.
SELECT 
  'WRONG_INNER_JOIN' as method,
  COUNT(c1.customer_id) as cohort_size,
  SUM(c1.mrr_usd) as start_mrr,
  SUM(c2.mrr_usd) as end_mrr,
  SUM(c2.mrr_usd) / SUM(c1.mrr_usd) as nrr_inflated
FROM `nexus-analyst-demo.acme.fact_subscriptions` c1
JOIN `nexus-analyst-demo.acme.fact_subscriptions` c2 
  ON c1.customer_id = c2.customer_id
WHERE c1.start_date = '2024-07-01' 
  AND c2.start_date = '2025-07-01'
  AND c1.plan_tier != 'Free' AND c2.plan_tier != 'Free';

-- 2025-07-12T13:15:45Z | user=rajiv.menon@acme.io | job_o9p2l3 | 10234455 | 4200 | SUCCESS
-- Correct NRR logic: LEFT JOIN to include churned customers (end MRR = 0)
SELECT 
  'CORRECT_LEFT_JOIN' as method,
  COUNT(c1.customer_id) as cohort_size,
  SUM(c1.mrr_usd) as start_mrr,
  SUM(COALESCE(c2.mrr_usd, 0)) as end_mrr,
  SUM(COALESCE(c2.mrr_usd, 0)) / SUM(c1.mrr_usd) as nrr_real
FROM `nexus-analyst-demo.acme.fact_subscriptions` c1
LEFT JOIN `nexus-analyst-demo.acme.fact_subscriptions` c2 
  ON c1.customer_id = c2.customer_id 
  AND c2.is_current = TRUE
WHERE c1.is_current = FALSE 
  AND c1.start_date BETWEEN '2024-07-01' AND '2024-07-31'
  AND c1.plan_tier != 'Free';

-- 2025-07-15T11:00:00Z | user=nina.patel@acme.io | job_b4v2c1 | 10455 | 300 | SUCCESS
SELECT column_name, data_type 
FROM `nexus-analyst-demo.acme.INFORMATION_SCHEMA.COLUMNS` 
WHERE table_name = 'account_health';

-- 2025-07-15T11:02:44Z | user=nina.patel@acme.io | job_z1x9m0 | 12044 | 450 | ERROR: Column not found
-- Trying to query VRS which is parked/unbuilt
SELECT customer_id, vrs_band, champion_login_recency 
FROM `nexus-analyst-demo.acme.account_health` 
LIMIT 10;

-- 2025-07-20T09:30:15Z | user=marco.silva@acme.io | job_u3i7o9 | 45022 | 550 | SUCCESS
-- CSM Cobalt Systems check
SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE company_name = 'Cobalt Systems';

-- 2025-07-20T10:15:33Z | user=marco.silva@acme.io | job_p2l1w4 | 889233 | 1200 | SUCCESS
-- Cobalt workflow success rate
SELECT 
  run_date, 
  n_runs, 
  success_rate 
FROM `nexus-analyst-demo.acme.workflow_runs_daily` 
WHERE customer_id = 'cust_000700' 
ORDER BY run_date DESC 
LIMIT 30;

-- 2025-07-25T16:00:22Z | user=lina.cho@acme.io | job_j8k2p1 | 3405562 | 2100 | SUCCESS
-- Comparing dim_customers.current_mrr_usd vs arr_snapshot
-- Snapshot is canonical, dim_customers drifts.
SELECT 
  'snapshot' as source, 
  arr_usd / 12 as mrr 
FROM `nexus-analyst-demo.acme.arr_snapshot` 
WHERE snapshot_date = '2025-07-24'
UNION ALL
SELECT 
  'dim_customers' as source, 
  SUM(current_mrr_usd) as mrr 
FROM `nexus-analyst-demo.acme.dim_customers` 
WHERE status = 'active' AND current_plan_tier != 'Free';

-- 2025-08-02T10:12:44Z | user=rajiv.menon@acme.io | job_n1m5b6 | 40023344 | 8900 | SUCCESS
-- Heavy scan: checking event distribution for engagement recalibration
SELECT 
  event_name, 
  COUNT(*) as event_count 
FROM `nexus-analyst-demo.acme.fact_user_events` 
WHERE event_at >= '2025-07-01' 
GROUP BY 1 
ORDER BY 2 DESC;

-- 2025-08-05T14:22:10Z | user=nina.patel@acme.io | job_c7v2n1 | 230445 | 900 | SUCCESS
-- Engaged customer = >=3 active users AND >=10 successful workflow runs in trailing 28 days
WITH user_counts AS (
  SELECT customer_id, COUNT(user_id) as active_users
  FROM `nexus-analyst-demo.acme.dim_users`
  WHERE is_active = TRUE
  GROUP BY 1
),
run_counts AS (
  SELECT customer_id, SUM(n_success) as total_success
  FROM `nexus-analyst-demo.acme.workflow_runs_daily`
  WHERE run_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 28 DAY)
  GROUP BY 1
)
SELECT 
  u.customer_id,
  u.active_users,
  r.total_success,
  (u.active_users >= 3 AND r.total_success >= 10) as is_engaged_calc
FROM user_counts u
JOIN run_counts r ON u.customer_id = r.customer_id;

-- 2025-08-10T09:00:00Z | user=grace.liu@acme.io | job_x2z1w8 | 12044 | 400 | SUCCESS
-- Grace checking Pro customers in EMEA
SELECT company_name, current_mrr_usd, acquisition_channel
FROM `nexus-analyst-demo.acme.dim_customers`
WHERE region = 'EMEA' AND current_plan_tier = 'Pro' AND status = 'active';

-- 2025-08-15T16:33:11Z | user=sarah.chen@acme.io | job_l0p8m5 | 55023 | 600 | SUCCESS
-- Sarah checking her Enterprise pipeline
SELECT account_name, amount_usd, stage, close_date
FROM `nexus-analyst-demo.acme.fact_opportunities`
WHERE ae_employee_id = 'emp_023' AND stage NOT IN ('Closed Won', 'Closed Lost');

-- 2025-08-18T11:15:44Z | user=lina.cho@acme.io | job_q3w2e1 | 890233 | 1100 | SUCCESS
-- Finding uncollectible invoices for health score impact
-- Critical if Enterprise AND uncollectible, OR Non-Ent AND (uncollectible OR low utilization)
SELECT 
  i.customer_id, 
  c.company_name, 
  c.account_tier, 
  i.amount_usd, 
  i.status 
FROM `nexus-analyst-demo.acme.fact_invoices` i
JOIN `nexus-analyst-demo.acme.dim_customers` c ON i.customer_id = c.customer_id
WHERE i.status = 'uncollectible' AND i.invoice_date >= '2025-06-01';

-- 2025-08-22T08:45:12Z | user=david.kim@acme.io | job_m4n5b6 | 100233445 | 15400 | SUCCESS
-- Monitoring duration spikes in fact_workflow_runs
SELECT 
  customer_id, 
  AVG(duration_ms) as avg_dur, 
  APPROX_QUANTILES(duration_ms, 100)[OFFSET(95)] as p95_dur
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE triggered_at >= '2025-08-01'
GROUP BY 1
HAVING avg_dur > 5000;

-- 2025-08-25T13:10:05Z | user=rajiv.menon@acme.io | job_y1x2c3 | 45022 | 340 | SUCCESS
-- Checking plan details for the dim_plans join
SELECT * FROM `nexus-analyst-demo.acme.dim_plans`;

-- 2025-08-30T10:00:22Z | user=lina.cho@acme.io | job_o8p9l0 | 203445 | 1200 | SUCCESS
-- Board Deck prep: ARR by Plan Tier
-- Signal: Pro ~$1M, Biz ~$32M, Ent ~$6M. Total ~$39M.
SELECT 
  plan_tier, 
  SUM(mrr_usd) * 12 as arr 
FROM `nexus-analyst-demo.acme.fact_subscriptions` 
WHERE is_current = TRUE AND plan_tier != 'Free'
GROUP BY 1;

-- 2025-09-02T14:15:00Z | user=olivia.tran@acme.io | job_v5n6m7 | 12044 | 450 | SUCCESS
-- Marigold Health (Enterprise) utilization check
-- Signal: Enterprise critical ONLY on uncollectible, not utilization.
SELECT 
  customer_id, 
  account_tier, 
  utilization_band, 
  account_health_status
FROM `nexus-analyst-demo.acme.account_health`
WHERE customer_id = 'cust_000701';

-- 2025-09-05T11:22:33Z | user=jorge.martinez@acme.io | job_z0x9c8 | 45022 | 500 | SUCCESS
-- Bookings by channel for Q3 MTD
SELECT 
  first_touch_channel, 
  SUM(bookings_acv_usd) as bookings 
FROM `nexus-analyst-demo.acme.bookings_attribution` 
WHERE closed_won_at >= '2025-07-01'
GROUP BY 1 
ORDER BY 2 DESC;

-- 2025-09-10T10:12:44Z | user=rajiv.menon@acme.io | job_r1t2y3 | 1204455 | 1800 | SUCCESS
-- Investigating error codes for Tamarind Group (cust_000706)
SELECT 
  error_code, 
  COUNT(*) as error_count
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE customer_id = 'cust_000706' AND status = 'error'
GROUP BY 1;

-- 2025-09-15T15:45:00Z | user=nina.patel@acme.io | job_i9u8y7 | 20344556 | 4500 | SUCCESS
-- Analyzing NPS for Enterprise segment
SELECT 
  c.account_tier,
  AVG(n.score) as avg_nps,
  COUNT(n.response_id) as resp_count
FROM `nexus-analyst-demo.acme.fact_nps_responses` n
JOIN `nexus-analyst-demo.acme.dim_customers` c ON n.customer_id = c.customer_id
WHERE n.survey_quarter = '2025-Q3'
GROUP BY 1;

-- 2025-09-20T09:12:33Z | user=lina.cho@acme.io | job_w2e3r4 | 550233 | 1100 | SUCCESS
-- Churn calculation for H1
SELECT 
  COUNT(DISTINCT customer_id) as churned_cust,
  SUM(current_mrr_usd) as lost_mrr
FROM `nexus-analyst-demo.acme.dim_customers`
WHERE status = 'churned' AND churn_date BETWEEN '2025-01-01' AND '2025-06-30';

-- 2025-09-25T11:00:15Z | user=sarah.chen@acme.io | job_k4j3h2 | 12044 | 300 | SUCCESS
-- Checking Quartz Foundry (Enterprise) status
SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE customer_id = 'cust_000714';

-- 2025-10-02T10:33:44Z | user=rajiv.menon@acme.io | job_f5g6h7 | 890234 | 1200 | SUCCESS
-- Refreshing account_health logic for Q4
-- Engaged = 3+ users, 10+ runs. 
-- healthy_expansion = engaged AND utilization >= 0.6
SELECT 
  customer_id,
  is_engaged,
  utilization_band,
  CASE 
    WHEN is_engaged AND utilization_band >= 0.6 THEN 'healthy_expansion'
    WHEN is_engaged THEN 'stable'
    ELSE 'monitoring'
  END as new_status_check
FROM `nexus-analyst-demo.acme.account_health`
WHERE account_tier != 'Enterprise';

-- 2025-10-05T14:12:12Z | user=lina.cho@acme.io | job_s1d2f3 | 1023445 | 1900 | SUCCESS
-- Q3 Final ARR Snapshot pull
SELECT arr_usd, arr_business_usd, arr_enterprise_usd, arr_pro_usd 
FROM `nexus-analyst-demo.acme.arr_snapshot` 
WHERE snapshot_date = '2025-09-30';

-- 2025-10-10T09:45:33Z | user=marco.silva@acme.io | job_z9x8c7 | 45022 | 500 | SUCCESS
-- Marco checking Kestrel Networks before they churned in Nov
SELECT * FROM `nexus-analyst-demo.acme.account_health` WHERE customer_id = 'cust_000708';

-- 2025-10-15T11:22:00Z | user=david.kim@acme.io | job_q0w9e8 | 5502334 | 2200 | SUCCESS
-- Pipeline debug: check for null payloads in workflow runs
SELECT COUNT(*) 
FROM `nexus-analyst-demo.acme.fact_workflow_runs` 
WHERE error_code = 'NULL_PAYLOAD' AND triggered_at >= '2025-10-01';

-- 2025-10-20T16:30:15Z | user=jorge.martinez@acme.io | job_a2s3d4 | 120445 | 800 | SUCCESS
-- AE performance leaderboard
SELECT 
  e.full_name, 
  SUM(o.amount_usd) as pipeline_value
FROM `nexus-analyst-demo.acme.fact_opportunities` o
JOIN `nexus-analyst-demo.acme.dim_employees` e ON o.ae_employee_id = e.employee_id
WHERE o.stage NOT IN ('Closed Won', 'Closed Lost')
GROUP BY 1 
ORDER BY 2 DESC;

-- 2025-10-25T13:44:11Z | user=nina.patel@acme.io | job_u4i5o6 | 1204455 | 1500 | SUCCESS
-- Customer support ticket volume vs tier
SELECT 
  c.account_tier, 
  COUNT(t.ticket_id) as tickets,
  AVG(t.resolution_time_hours) as avg_res_time
FROM `nexus-analyst-demo.acme.fact_support_tickets` t
JOIN `nexus-analyst-demo.acme.dim_customers` c ON t.customer_id = c.customer_id
WHERE t.opened_at >= '2025-10-01'
GROUP BY 1;

-- 2025-11-02T09:12:44Z | user=lina.cho@acme.io | job_p0o9i8 | 89023 | 450 | SUCCESS
-- NRR Trailing 12 board metric
-- Signal: NRR ~1.07, GRR ~0.94
SELECT * FROM `nexus-analyst-demo.acme.nrr_trailing_12` ORDER BY cohort_size DESC LIMIT 1;

-- 2025-11-05T14:22:10Z | user=rajiv.menon@acme.io | job_m1n2b3 | 4502234 | 3100 | SUCCESS
-- Looking at marketing attribution for Enterprise deals
SELECT 
  m.utm_source, 
  COUNT(DISTINCT o.opportunity_id) as deal_count,
  SUM(o.amount_usd) as pipeline_amt
FROM `nexus-analyst-demo.acme.fact_marketing_touches` m
JOIN `nexus-analyst-demo.acme.fact_opportunities` o ON m.customer_id = o.customer_id
WHERE o.created_date >= '2025-01-01'
GROUP BY 1 
ORDER BY 3 DESC;

-- 2025-11-10T10:15:33Z | user=olivia.tran@acme.io | job_c3v4b5 | 12044 | 400 | SUCCESS
-- Checking Ember Industries health (Enterprise)
SELECT * FROM `nexus-analyst-demo.acme.account_health` WHERE customer_id = 'cust_000711';

-- 2025-11-15T15:45:00Z | user=sarah.chen@acme.io | job_n7m8k9 | 10234 | 350 | SUCCESS
-- Sarah checking Cobalt Systems (ae_employee_id for Sarah is emp_023, but Cobalt is Tom's emp_021)
-- Sarah just looking around...
SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE company_name = 'Cobalt Systems';

-- 2025-11-20T09:12:33Z | user=david.kim@acme.io | job_x0z9c8 | 12044556 | 3200 | SUCCESS
-- Daily workflow success rate trends
SELECT 
  run_date, 
  AVG(success_rate) as avg_success
FROM `nexus-analyst-demo.acme.workflow_runs_daily`
WHERE run_date >= '2025-11-01'
GROUP BY 1 
ORDER BY 1;

-- 2025-11-25T11:00:15Z | user=lina.cho@acme.io | job_v1b2n3 | 450233 | 1100 | SUCCESS
-- Identifying downgrades to Free (NRR impact)
SELECT 
  customer_id, 
  changed_from_subscription_id, 
  plan_tier as new_tier 
FROM `nexus-analyst-demo.acme.fact_subscriptions` 
WHERE plan_tier = 'Free' AND change_type = 'downgrade' AND start_date >= '2025-10-01';

-- 2025-12-02T10:33:44Z | user=jorge.martinez@acme.io | job_l4k5j6 | 203445 | 800 | SUCCESS
-- Full year 2025 bookings by AE
SELECT 
  e.full_name, 
  SUM(b.bookings_acv_usd) as total_bookings_2025
FROM `nexus-analyst-demo.acme.bookings_attribution` b
JOIN `nexus-analyst-demo.acme.dim_employees` e ON b.customer_id = b.customer_id -- messy join noise
JOIN `nexus-analyst-demo.acme.dim_customers` c ON b.customer_id = c.customer_id
JOIN `nexus-analyst-demo.acme.dim_employees` e2 ON c.ae_employee_id = e2.employee_id
WHERE b.closed_won_at BETWEEN '2025-01-01' AND '2025-12-31'
GROUP BY 1 
ORDER BY 2 DESC;

-- 2025-12-05T14:12:12Z | user=rajiv.menon@acme.io | job_m0n9b8 | 55023345 | 9800 | SUCCESS
-- Data scan: distribution of workflow step counts
SELECT 
  step_count, 
  COUNT(*) as frequency
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE triggered_at >= '2025-12-01'
GROUP BY 1 
ORDER BY 1;

-- 2025-12-10T09:45:33Z | user=nina.patel@acme.io | job_o2p3l4 | 45022 | 450 | SUCCESS
-- Quick check on subscription cycle mix
SELECT 
  billing_cycle, 
  COUNT(*) as sub_count 
FROM `nexus-analyst-demo.acme.fact_subscriptions` 
WHERE is_current = TRUE
GROUP BY 1;

-- 2025-12-15T11:22:00Z | user=lina.cho@acme.io | job_i9u8y7 | 1023445 | 1800 | SUCCESS
-- Final board ARR prep. 
-- Total should be ~$39M.
SELECT 
  SUM(mrr_usd) * 12 as arr_final_2025
FROM `nexus-analyst-demo.acme.fact_subscriptions`
WHERE is_current = TRUE AND plan_tier != 'Free';

-- 2025-12-20T16:30:15Z | user=marco.silva@acme.io | job_q1w2e3 | 12044 | 410 | SUCCESS
-- Checking account health for Sable Analytics
SELECT * FROM `nexus-analyst-demo.acme.account_health` WHERE customer_id = 'cust_000710';

-- 2025-12-24T10:00:00Z | user=rajiv.menon@acme.io | job_holiday_cleanup | 12044 | 300 | SUCCESS
-- Cleaning up some test tables (not in acme schema usually, but checking anyway)
SELECT table_name FROM `nexus-analyst-demo.acme.INFORMATION_SCHEMA.TABLES` WHERE table_name LIKE '%test%';

-- 2025-12-28T13:44:11Z | user=nina.patel@acme.io | job_z7x8c9 | 450233 | 950 | SUCCESS
-- End of year NPS summary
SELECT 
  score, 
  COUNT(*) as count
FROM `nexus-analyst-demo.acme.fact_nps_responses`
WHERE responded_at >= '2025-01-01'
GROUP BY 1 
ORDER BY 1;

-- 2025-12-30T09:12:44Z | user=lina.cho@acme.io | job_f2g3h4 | 20344 | 400 | SUCCESS
-- Sanity check: Total customers by tier
SELECT 
  current_plan_tier, 
  status, 
  COUNT(*) 
FROM `nexus-analyst-demo.acme.dim_customers` 
GROUP BY 1, 2;

-- 2025-12-31T11:00:15Z | user=rajiv.menon@acme.io | job_new_year_prep | 5502334 | 4200 | SUCCESS
-- Pre-calculating 2025 daily workflow stats for retrospective
SELECT 
  EXTRACT(MONTH FROM run_date) as month, 
  SUM(n_runs) as total_runs, 
  AVG(success_rate) as avg_success
FROM `nexus-analyst-demo.acme.workflow_runs_daily`
WHERE run_date BETWEEN '2025-01-01' AND '2025-12-31'
GROUP BY 1 
ORDER BY 1;

-- 2025-07-01T12:00:00Z | user=david.kim@acme.io | job_jk123 | 55000 | 1200 | SUCCESS
SELECT count(*) FROM `nexus-analyst-demo.acme.fact_user_events` WHERE event_name = 'workflow_created';

-- 2025-07-01T12:15:00Z | user=rajiv.menon@acme.io | job_ab456 | 120000 | 2500 | SUCCESS
SELECT customer_id, count(user_id) FROM `nexus-analyst-demo.acme.dim_users` GROUP BY 1;

-- 2025-07-02T09:30:00Z | user=lina.cho@acme.io | job_lc789 | 35000 | 800 | SUCCESS
SELECT customer_id, sum(mrr_usd) FROM `nexus-analyst-demo.acme.fact_subscriptions` WHERE is_current = true GROUP BY 1;

-- 2025-07-02T14:45:00Z | user=nina.patel@acme.io | job_np012 | 850000 | 4500 | SUCCESS
SELECT u.email_domain, count(e.event_id) FROM `nexus-analyst-demo.acme.dim_users` u JOIN `nexus-analyst-demo.acme.fact_user_events` e ON u.user_id = e.user_id GROUP BY 1 ORDER BY 2 DESC LIMIT 10;

-- 2025-07-03T10:00:00Z | user=jorge.martinez@acme.io | job_jm345 | 45000 | 1100 | SUCCESS
SELECT ae_employee_id, count(opportunity_id) FROM `nexus-analyst-demo.acme.fact_opportunities` WHERE stage = 'Closed Won' GROUP BY 1;

-- 2025-07-04T08:00:00Z | user=david.kim@acme.io | job_dk678 | 1500000 | 6000 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE status = 'error' AND triggered_at > '2025-06-30';

-- 2025-07-05T11:30:00Z | user=rajiv.menon@acme.io | job_rm901 | 25000 | 700 | SUCCESS
SELECT table_name FROM `nexus-analyst-demo.acme.INFORMATION_SCHEMA.TABLES`;

-- 2025-07-06T13:15:00Z | user=lina.cho@acme.io | job_lc234 | 18000 | 600 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.dim_plans`;

-- 2025-07-07T09:00:00Z | user=nina.patel@acme.io | job_np567 | 420000 | 3200 | SUCCESS
SELECT customer_id, avg(score) FROM `nexus-analyst-demo.acme.fact_nps_responses` GROUP BY 1;

-- 2025-07-08T15:00:00Z | user=jorge.martinez@acme.io | job_jm890 | 55000 | 1400 | SUCCESS
SELECT first_touch_channel, sum(bookings_acv_usd) FROM `nexus-analyst-demo.acme.bookings_attribution` GROUP BY 1;

-- 2025-07-09T10:30:00Z | user=david.kim@acme.io | job_dk123 | 750000 | 4000 | SUCCESS
SELECT customer_id, count(*) FROM `nexus-analyst-demo.acme.fact_invoices` WHERE status = 'paid' GROUP BY 1;

-- 2025-07-10T12:00:00Z | user=rajiv.menon@acme.io | job_rm456 | 12000 | 500 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.dim_employees` WHERE team = 'Eng';

-- 2025-07-11T14:15:00Z | user=lina.cho@acme.io | job_lc789 | 95000 | 2000 | SUCCESS
SELECT snapshot_date, arr_usd FROM `nexus-analyst-demo.acme.arr_snapshot` ORDER BY snapshot_date DESC LIMIT 30;

-- 2025-07-12T09:45:00Z | user=nina.patel@acme.io | job_np012 | 1100000 | 5500 | SUCCESS
SELECT event_name, count(*) FROM `nexus-analyst-demo.acme.fact_user_events` WHERE event_at > '2025-07-01' GROUP BY 1;

-- 2025-07-13T11:00:00Z | user=jorge.martinez@acme.io | job_jm345 | 65000 | 1600 | SUCCESS
SELECT stage, count(*) FROM `nexus-analyst-demo.acme.fact_opportunities` GROUP BY 1;

-- 2025-07-14T13:30:00Z | user=david.kim@acme.io | job_dk678 | 2000000 | 8000 | SUCCESS
SELECT customer_id, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` GROUP BY 1 ORDER BY 2 DESC LIMIT 20;

-- 2025-07-15T09:15:00Z | user=rajiv.menon@acme.io | job_rm901 | 35000 | 900 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE country = 'USA';

-- 2025-07-16T14:45:00Z | user=lina.cho@acme.io | job_lc234 | 28000 | 1000 | SUCCESS
SELECT plan_tier, count(*) FROM `nexus-analyst-demo.acme.fact_subscriptions` WHERE is_current = true GROUP BY 1;

-- 2025-07-17T10:00:00Z | user=nina.patel@acme.io | job_np567 | 550000 | 3800 | SUCCESS
SELECT customer_id, count(*) FROM `nexus-analyst-demo.acme.fact_support_tickets` WHERE priority = 'P1' GROUP BY 1;

-- 2025-07-18T15:30:00Z | user=jorge.martinez@acme.io | job_jm890 | 75000 | 1800 | SUCCESS
SELECT utm_source, sum(attributed_revenue_usd) FROM `nexus-analyst-demo.acme.fact_marketing_touches` GROUP BY 1;

-- 2025-07-19T11:15:00Z | user=david.kim@acme.io | job_dk123 | 900000 | 4800 | SUCCESS
SELECT customer_id, avg(duration_ms) FROM `nexus-analyst-demo.acme.fact_workflow_runs` GROUP BY 1;

-- 2025-07-20T12:45:00Z | user=rajiv.menon@acme.io | job_rm456 | 15000 | 600 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.dim_users` WHERE is_active = true LIMIT 100;

-- 2025-07-21T09:30:00Z | user=lina.cho@acme.io | job_lc789 | 110000 | 2400 | SUCCESS
SELECT month_name, sum(amount_usd) FROM `nexus-analyst-demo.acme.fact_invoices` i JOIN `nexus-analyst-demo.acme.dim_dates` d ON i.invoice_date = d.date GROUP BY 1;

-- 2025-07-22T14:15:00Z | user=nina.patel@acme.io | job_np012 | 1300000 | 6200 | SUCCESS
SELECT user_id, count(event_id) FROM `nexus-analyst-demo.acme.fact_user_events` GROUP BY 1 HAVING count(event_id) > 100;

-- 2025-07-23T10:45:00Z | user=jorge.martinez@acme.io | job_jm345 | 85000 | 2000 | SUCCESS
SELECT region, sum(amount_usd) FROM `nexus-analyst-demo.acme.fact_opportunities` o JOIN `nexus-analyst-demo.acme.dim_customers` c ON o.customer_id = c.customer_id WHERE stage = 'Closed Won' GROUP BY 1;

-- 2025-07-24T13:00:00Z | user=david.kim@acme.io | job_dk678 | 2500000 | 9500 | SUCCESS
SELECT customer_id, error_code, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE status = 'error' GROUP BY 1, 2;

-- 2025-07-25T08:30:00Z | user=rajiv.menon@acme.io | job_rm901 | 45000 | 1200 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.account_health` WHERE account_health_status = 'critical';

-- 2025-07-26T11:45:00Z | user=lina.cho@acme.io | job_lc234 | 38000 | 1300 | SUCCESS
SELECT cohort_start_mrr_usd, nrr FROM `nexus-analyst-demo.acme.nrr_trailing_12` WHERE cohort_size > 50;

-- 2025-07-27T15:15:00Z | user=nina.patel@acme.io | job_np567 | 680000 | 4200 | SUCCESS
SELECT channel, avg(csat_score) FROM `nexus-analyst-demo.acme.fact_support_tickets` GROUP BY 1;

-- 2025-07-28T10:00:00Z | user=jorge.martinez@acme.io | job_jm890 | 95000 | 2200 | SUCCESS
SELECT ae_employee_id, sum(amount_usd) FROM `nexus-analyst-demo.acme.fact_opportunities` WHERE created_date > '2025-01-01' GROUP BY 1;

-- 2025-07-29T14:30:00Z | user=david.kim@acme.io | job_dk123 | 1100000 | 5400 | SUCCESS
SELECT run_date, sum(n_runs) FROM `nexus-analyst-demo.acme.workflow_runs_daily` GROUP BY 1;

-- 2025-07-30T12:15:00Z | user=rajiv.menon@acme.io | job_rm456 | 22000 | 800 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.dim_dates` WHERE is_business_day = false;

-- 2025-07-31T09:45:00Z | user=lina.cho@acme.io | job_lc789 | 130000 | 2800 | SUCCESS
SELECT current_plan_tier, avg(current_mrr_usd) FROM `nexus-analyst-demo.acme.dim_customers` GROUP BY 1;

-- 2025-08-01T12:00:00Z | user=nina.patel@acme.io | job_np012 | 1500000 | 7000 | SUCCESS
SELECT customer_id, count(distinct user_id) FROM `nexus-analyst-demo.acme.fact_user_events` GROUP BY 1;

-- 2025-08-02T14:45:00Z | user=jorge.martinez@acme.io | job_jm345 | 105000 | 2400 | SUCCESS
SELECT utm_campaign, count(distinct customer_id) FROM `nexus-analyst-demo.acme.fact_marketing_touches` GROUP BY 1 ORDER BY 2 DESC LIMIT 5;

-- 2025-08-03T10:30:00Z | user=david.kim@acme.io | job_dk678 | 3000000 | 11000 | SUCCESS
SELECT customer_id, avg(step_count) FROM `nexus-analyst-demo.acme.fact_workflow_runs` GROUP BY 1;

-- 2025-08-04T08:15:00Z | user=rajiv.menon@acme.io | job_rm901 | 55000 | 1400 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE industry = 'fintech';

-- 2025-08-05T11:45:00Z | user=lina.cho@acme.io | job_lc234 | 48000 | 1600 | SUCCESS
SELECT billing_cycle, sum(mrr_usd) FROM `nexus-analyst-demo.acme.fact_subscriptions` WHERE is_current = true GROUP BY 1;

-- 2025-08-06T13:30:00Z | user=nina.patel@acme.io | job_np567 | 820000 | 4800 | SUCCESS
SELECT category, count(*) FROM `nexus-analyst-demo.acme.fact_support_tickets` GROUP BY 1;

-- 2025-08-07T09:00:00Z | user=jorge.martinez@acme.io | job_jm890 | 115000 | 2600 | SUCCESS
SELECT sdr_employee_id, count(*) FROM `nexus-analyst-demo.acme.fact_opportunities` GROUP BY 1;

-- 2025-08-08T15:15:00Z | user=david.kim@acme.io | job_dk123 | 1300000 | 5800 | SUCCESS
SELECT run_date, customer_id, success_rate FROM `nexus-analyst-demo.acme.workflow_runs_daily` WHERE success_rate < 0.9;

-- 2025-08-09T10:45:00Z | user=rajiv.menon@acme.io | job_rm456 | 32000 | 1100 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.dim_users` WHERE role = 'admin';

-- 2025-08-10T12:00:00Z | user=lina.cho@acme.io | job_lc789 | 150000 | 3200 | SUCCESS
SELECT snapshot_date, sum(arr_usd) FROM `nexus-analyst-demo.acme.arr_snapshot` GROUP BY 1;

-- 2025-08-11T14:15:00Z | user=nina.patel@acme.io | job_np012 | 1700000 | 7500 | SUCCESS
SELECT customer_id, count(event_id) FROM `nexus-analyst-demo.acme.fact_user_events` WHERE event_name = 'login' GROUP BY 1;

-- 2025-08-12T09:30:00Z | user=jorge.martinez@acme.io | job_jm345 | 125000 | 2800 | SUCCESS
SELECT loss_reason, count(*) FROM `nexus-analyst-demo.acme.fact_opportunities` WHERE stage = 'Closed Lost' GROUP BY 1;

-- 2025-08-13T13:45:00Z | user=david.kim@acme.io | job_dk678 | 3500000 | 12500 | SUCCESS
SELECT customer_id, max(triggered_at) FROM `nexus-analyst-demo.acme.fact_workflow_runs` GROUP BY 1;

-- 2025-08-14T08:00:00Z | user=rajiv.menon@acme.io | job_rm901 | 65000 | 1800 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.dim_employees` WHERE is_active = false;

-- 2025-08-15T11:30:00Z | user=lina.cho@acme.io | job_lc234 | 58000 | 1900 | SUCCESS
SELECT plan_tier, avg(mrr_usd) FROM `nexus-analyst-demo.acme.fact_subscriptions` GROUP BY 1;

-- 2025-08-16T15:00:00Z | user=nina.patel@acme.io | job_np567 | 950000 | 5200 | SUCCESS
SELECT customer_id, avg(csat_score) FROM `nexus-analyst-demo.acme.fact_support_tickets` WHERE csat_score IS NOT NULL GROUP BY 1;

-- 2025-08-17T10:15:00Z | user=jorge.martinez@acme.io | job_jm890 | 135000 | 3100 | SUCCESS
SELECT acquisition_channel, count(*) FROM `nexus-analyst-demo.acme.dim_customers` GROUP BY 1;

-- 2025-08-18T14:30:00Z | user=david.kim@acme.io | job_dk123 | 1500000 | 6200 | SUCCESS
SELECT customer_id, count(*) FROM `nexus-analyst-demo.acme.fact_invoices` WHERE status = 'uncollectible' GROUP BY 1;

-- 2025-08-19T12:00:00Z | user=rajiv.menon@acme.io | job_rm456 | 42000 | 1300 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.account_health` WHERE utilization_band = 'low';

-- 2025-08-20T09:45:00Z | user=lina.cho@acme.io | job_lc789 | 170000 | 3500 | SUCCESS
SELECT cohort_size, nrr, grr FROM `nexus-analyst-demo.acme.nrr_trailing_12` ORDER BY nrr DESC;

-- 2025-08-21T11:15:00Z | user=nina.patel@acme.io | job_np012 | 1900000 | 8000 | SUCCESS
SELECT user_id, count(distinct customer_id) FROM `nexus-analyst-demo.acme.dim_users` GROUP BY 1 HAVING count(distinct customer_id) > 1;

-- 2025-08-22T13:30:00Z | user=jorge.martinez@acme.io | job_jm345 | 145000 | 3400 | SUCCESS
SELECT year, month, sum(bookings_acv_usd) FROM `nexus-analyst-demo.acme.bookings_attribution` b JOIN `nexus-analyst-demo.acme.dim_dates` d ON b.closed_won_at = d.date GROUP BY 1, 2;

-- 2025-08-23T08:45:00Z | user=david.kim@acme.io | job_dk678 | 4000000 | 14000 | SUCCESS
SELECT triggered_by, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` GROUP BY 1;

-- 2025-08-24T10:00:00Z | user=rajiv.menon@acme.io | job_rm901 | 75000 | 2100 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.dim_plans` WHERE monthly_price_per_seat_usd > 100;

-- 2025-08-25T14:45:00Z | user=lina.cho@acme.io | job_lc234 | 68000 | 2200 | SUCCESS
SELECT change_type, count(*) FROM `nexus-analyst-demo.acme.fact_subscriptions` GROUP BY 1;

-- 2025-08-26T09:15:00Z | user=nina.patel@acme.io | job_np567 | 1100000 | 5800 | SUCCESS
SELECT customer_id, segment, score FROM `nexus-analyst-demo.acme.fact_nps_responses` WHERE segment = 'Enterprise';

-- 2025-08-27T15:30:00Z | user=jorge.martinez@acme.io | job_jm890 | 155000 | 3700 | SUCCESS
SELECT ae_employee_id, avg(amount_usd) FROM `nexus-analyst-demo.acme.fact_opportunities` WHERE stage = 'Closed Won' GROUP BY 1;

-- 2025-08-28T11:00:00Z | user=david.kim@acme.io | job_dk123 | 1700000 | 6800 | SUCCESS
SELECT run_date, avg(p50_duration_ms), avg(p99_duration_ms) FROM `nexus-analyst-demo.acme.workflow_runs_daily` GROUP BY 1;

-- 2025-08-29T12:30:00Z | user=rajiv.menon@acme.io | job_rm456 | 52000 | 1600 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.dim_employees` WHERE location = 'Amsterdam';

-- 2025-08-30T10:00:00Z | user=lina.cho@acme.io | job_lc789 | 190000 | 4000 | SUCCESS
SELECT customer_id, sum(amount_usd) FROM `nexus-analyst-demo.acme.fact_invoices` WHERE invoice_date > '2025-01-01' GROUP BY 1 ORDER BY 2 DESC LIMIT 10;

-- 2025-08-31T14:15:00Z | user=nina.patel@acme.io | job_np012 | 2100000 | 8800 | SUCCESS
SELECT event_at, event_name, properties_json FROM `nexus-analyst-demo.acme.fact_user_events` WHERE customer_id = 'cust_000700' LIMIT 50;

-- 2025-09-01T09:30:00Z | user=jorge.martinez@acme.io | job_jm345 | 165000 | 4000 | SUCCESS
SELECT utm_medium, count(*) FROM `nexus-analyst-demo.acme.fact_marketing_touches` GROUP BY 1;

-- 2025-09-02T13:45:00Z | user=david.kim@acme.io | job_dk678 | 4500000 | 16000 | SUCCESS
SELECT status, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE triggered_at > '2025-08-01' GROUP BY 1;

-- 2025-09-03T08:15:00Z | user=rajiv.menon@acme.io | job_rm901 | 85000 | 2500 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE signup_date > '2025-01-01';

-- 2025-09-04T11:45:00Z | user=lina.cho@acme.io | job_lc234 | 78000 | 2600 | SUCCESS
SELECT customer_id, mrr_usd, seat_count FROM `nexus-analyst-demo.acme.fact_subscriptions` WHERE is_current = true AND seat_count > 100;

-- 2025-09-05T15:15:00Z | user=nina.patel@acme.io | job_np567 | 1300000 | 6500 | SUCCESS
SELECT assigned_to_employee_id, count(*) FROM `nexus-analyst-demo.acme.fact_support_tickets` WHERE closed_at IS NULL GROUP BY 1;

-- 2025-09-06T10:45:00Z | user=jorge.martinez@acme.io | job_jm890 | 175000 | 4300 | SUCCESS
SELECT region, count(*) FROM `nexus-analyst-demo.acme.dim_customers` GROUP BY 1;

-- 2025-09-07T14:00:00Z | user=david.kim@acme.io | job_dk123 | 1900000 | 7500 | SUCCESS
SELECT run_date, sum(auth_failed_count), sum(rate_limited_count) FROM `nexus-analyst-demo.acme.workflow_runs_daily` GROUP BY 1;

-- 2025-09-08T12:30:00Z | user=rajiv.menon@acme.io | job_rm456 | 62000 | 1900 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.dim_users` WHERE last_login_date < '2025-08-01';

-- 2025-09-09T09:45:00Z | user=lina.cho@acme.io | job_lc789 | 210000 | 4500 | SUCCESS
SELECT snapshot_date, arr_pro_usd, arr_business_usd, arr_enterprise_usd FROM `nexus-analyst-demo.acme.arr_snapshot` ORDER BY snapshot_date DESC;

-- 2025-09-10T11:15:00Z | user=nina.patel@acme.io | job_np012 | 2300000 | 9500 | SUCCESS
SELECT customer_id, count(distinct event_name) FROM `nexus-analyst-demo.acme.fact_user_events` GROUP BY 1;

-- 2025-09-11T13:30:00Z | user=jorge.martinez@acme.io | job_jm345 | 185000 | 4600 | SUCCESS
SELECT sdr_employee_id, ae_employee_id, count(*) FROM `nexus-analyst-demo.acme.fact_opportunities` GROUP BY 1, 2;

-- 2025-09-12T08:45:00Z | user=david.kim@acme.io | job_dk678 | 5000000 | 18000 | SUCCESS
SELECT triggered_at, duration_ms FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE duration_ms > 10000;

-- 2025-09-13T10:00:00Z | user=rajiv.menon@acme.io | job_rm901 | 95000 | 2800 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.dim_employees` WHERE role = 'CSM';

-- 2025-09-14T14:45:00Z | user=lina.cho@acme.io | job_lc234 | 88000 | 3000 | SUCCESS
SELECT customer_id, count(subscription_id) FROM `nexus-analyst-demo.acme.fact_subscriptions` GROUP BY 1 HAVING count(subscription_id) > 2;

-- 2025-09-15T09:15:00Z | user=nina.patel@acme.io | job_np567 | 1500000 | 7200 | SUCCESS
SELECT customer_id, avg(resolution_time_hours) FROM `nexus-analyst-demo.acme.fact_support_tickets` GROUP BY 1;

-- 2025-09-16T15:30:00Z | user=jorge.martinez@acme.io | job_jm890 | 195000 | 4900 | SUCCESS
SELECT industry, sum(amount_usd) FROM `nexus-analyst-demo.acme.fact_opportunities` o JOIN `nexus-analyst-demo.acme.dim_customers` c ON o.customer_id = c.customer_id GROUP BY 1;

-- 2025-09-17T11:00:00Z | user=david.kim@acme.io | job_dk123 | 2100000 | 8200 | SUCCESS
SELECT run_date, sum(step_timeout_count), sum(integration_down_count) FROM `nexus-analyst-demo.acme.workflow_runs_daily` GROUP BY 1;

-- 2025-09-18T12:15:00Z | user=rajiv.menon@acme.io | job_rm456 | 72000 | 2200 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.account_health` WHERE has_recent_nps_detractor = true;

-- 2025-09-19T09:30:00Z | user=lina.cho@acme.io | job_lc789 | 230000 | 5000 | SUCCESS
SELECT year, quarter, sum(amount_usd) FROM `nexus-analyst-demo.acme.fact_invoices` i JOIN `nexus-analyst-demo.acme.dim_dates` d ON i.invoice_date = d.date GROUP BY 1, 2;

-- 2025-09-20T14:15:00Z | user=nina.patel@acme.io | job_np012 | 2500000 | 10500 | SUCCESS
SELECT user_id, event_name, event_at FROM `nexus-analyst-demo.acme.fact_user_events` WHERE event_at > '2025-09-15';

-- 2025-09-21T10:30:00Z | user=jorge.martinez@acme.io | job_jm345 | 205000 | 5200 | SUCCESS
SELECT campaign, sum(attributed_revenue_usd) FROM `nexus-analyst-demo.acme.fact_marketing_touches` GROUP BY 1;

-- 2025-09-22T13:45:00Z | user=david.kim@acme.io | job_dk678 | 5500000 | 20000 | SUCCESS
SELECT customer_id, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE step_count > 50 GROUP BY 1;

-- 2025-09-23T08:00:00Z | user=rajiv.menon@acme.io | job_rm901 | 105000 | 3200 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE status = 'churned';

-- 2025-09-24T11:30:00Z | user=lina.cho@acme.io | job_lc234 | 98000 | 3400 | SUCCESS
SELECT plan_tier, sum(mrr_usd) FROM `nexus-analyst-demo.acme.fact_subscriptions` WHERE start_date > '2025-07-01' GROUP BY 1;

-- 2025-09-25T15:00:00Z | user=nina.patel@acme.io | job_np567 | 1700000 | 8000 | SUCCESS
SELECT category, avg(csat_score) FROM `nexus-analyst-demo.acme.fact_support_tickets` GROUP BY 1;

-- 2025-09-26T10:15:00Z | user=jorge.martinez@acme.io | job_jm890 | 215000 | 5500 | SUCCESS
SELECT ae_employee_id, count(*) FROM `nexus-analyst-demo.acme.fact_opportunities` WHERE stage = 'Closed Lost' GROUP BY 1;

-- 2025-09-27T14:30:00Z | user=david.kim@acme.io | job_dk123 | 2300000 | 9000 | SUCCESS
SELECT run_date, sum(n_success) / sum(n_runs) as daily_success_rate FROM `nexus-analyst-demo.acme.workflow_runs_daily` GROUP BY 1;

-- 2025-09-28T12:00:00Z | user=rajiv.menon@acme.io | job_rm456 | 82000 | 2500 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.dim_users` WHERE invited_by_user_id IS NOT NULL;

-- 2025-09-29T09:45:00Z | user=lina.cho@acme.io | job_lc789 | 250000 | 5500 | SUCCESS
SELECT snapshot_date, paying_customers FROM `nexus-analyst-demo.acme.arr_snapshot` ORDER BY snapshot_date DESC LIMIT 10;

-- 2025-09-30T11:15:00Z | user=nina.patel@acme.io | job_np012 | 2700000 | 11500 | SUCCESS
SELECT customer_id, count(distinct user_id) as active_users_today FROM `nexus-analyst-demo.acme.fact_user_events` WHERE event_at > '2025-09-29' GROUP BY 1;

-- 2025-10-01T13:30:00Z | user=jorge.martinez@acme.io | job_jm345 | 225000 | 5800 | SUCCESS
SELECT utm_source, count(distinct lead_email_hash) FROM `nexus-analyst-demo.acme.fact_marketing_touches` GROUP BY 1;

-- 2025-10-02T08:45:00Z | user=david.kim@acme.io | job_dk678 | 6000000 | 22000 | SUCCESS
SELECT customer_id, triggered_by, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` GROUP BY 1, 2;

-- 2025-10-03T10:00:00Z | user=rajiv.menon@acme.io | job_rm901 | 115000 | 3600 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.dim_employees` WHERE termination_date IS NOT NULL;

-- 2025-10-04T14:45:00Z | user=lina.cho@acme.io | job_lc234 | 108000 | 3800 | SUCCESS
SELECT billing_cycle, avg(seat_count) FROM `nexus-analyst-demo.acme.fact_subscriptions` GROUP BY 1;

-- 2025-10-05T09:15:00Z | user=nina.patel@acme.io | job_np567 | 1900000 | 8800 | SUCCESS
SELECT customer_id, count(*) FROM `nexus-analyst-demo.acme.fact_support_tickets` WHERE resolution_time_hours > 48 GROUP BY 1;

-- 2025-10-06T15:30:00Z | user=jorge.martinez@acme.io | job_jm890 | 235000 | 6100 | SUCCESS
SELECT industry, count(*) FROM `nexus-analyst-demo.acme.dim_customers` WHERE status = 'active' GROUP BY 1;

-- 2025-10-07T11:00:00Z | user=david.kim@acme.io | job_dk123 | 2500000 | 10000 | SUCCESS
SELECT run_date, customer_id, n_runs FROM `nexus-analyst-demo.acme.workflow_runs_daily` WHERE n_runs > 1000;

-- 2025-10-08T12:15:00Z | user=rajiv.menon@acme.io | job_rm456 | 92000 | 2800 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.account_health` WHERE is_engaged = false;

-- 2025-10-09T09:30:00Z | user=lina.cho@acme.io | job_lc789 | 270000 | 6000 | SUCCESS
SELECT cohort_size, churned_mrr_loss_usd FROM `nexus-analyst-demo.acme.nrr_trailing_12` WHERE nrr < 1.0;

-- 2025-10-10T14:15:00Z | user=nina.patel@acme.io | job_np012 | 2900000 | 12500 | SUCCESS
SELECT user_id, count(distinct event_name) FROM `nexus-analyst-demo.acme.fact_user_events` GROUP BY 1;

-- 2025-10-11T10:30:00Z | user=jorge.martinez@acme.io | job_jm345 | 245000 | 6400 | SUCCESS
SELECT year, sum(bookings_acv_usd) FROM `nexus-analyst-demo.acme.bookings_attribution` b JOIN `nexus-analyst-demo.acme.dim_dates` d ON b.closed_won_at = d.date GROUP BY 1;

-- 2025-10-12T13:45:00Z | user=david.kim@acme.io | job_dk678 | 6500000 | 24000 | SUCCESS
SELECT status, error_code, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` GROUP BY 1, 2;

-- 2025-10-13T08:15:00Z | user=rajiv.menon@acme.io | job_rm901 | 125000 | 4000 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE current_plan_tier = 'Enterprise';

-- 2025-10-14T11:45:00Z | user=lina.cho@acme.io | job_lc234 | 118000 | 4200 | SUCCESS
SELECT customer_id, sum(mrr_usd) FROM `nexus-analyst-demo.acme.fact_subscriptions` GROUP BY 1 HAVING sum(mrr_usd) > 5000;

-- 2025-10-15T15:15:00Z | user=nina.patel@acme.io | job_np567 | 2100000 | 9500 | SUCCESS
SELECT category, count(*) FROM `nexus-analyst-demo.acme.fact_support_tickets` WHERE priority = 'P1' GROUP BY 1;

-- 2025-10-16T10:45:00Z | user=jorge.martinez@acme.io | job_jm890 | 255000 | 6700 | SUCCESS
SELECT region, sum(amount_usd) FROM `nexus-analyst-demo.acme.fact_opportunities` o JOIN `nexus-analyst-demo.acme.dim_customers` c ON o.customer_id = c.customer_id GROUP BY 1;

-- 2025-10-17T14:00:00Z | user=david.kim@acme.io | job_dk123 | 2700000 | 11000 | SUCCESS
SELECT run_date, avg(p95_duration_ms) FROM `nexus-analyst-demo.acme.workflow_runs_daily` GROUP BY 1;

-- 2025-10-18T12:30:00Z | user=rajiv.menon@acme.io | job_rm456 | 102000 | 3200 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.dim_users` WHERE is_active = false AND last_login_date > '2025-01-01';

-- 2025-10-19T09:45:00Z | user=lina.cho@acme.io | job_lc789 | 290000 | 6500 | SUCCESS
SELECT snapshot_date, arr_usd / paying_customers as arpu FROM `nexus-analyst-demo.acme.arr_snapshot` ORDER BY snapshot_date DESC;

-- 2025-10-20T11:15:00Z | user=nina.patel@acme.io | job_np012 | 3100000 | 13500 | SUCCESS
SELECT customer_id, count(event_id) FROM `nexus-analyst-demo.acme.fact_user_events` WHERE event_name = 'workflow_run_started' GROUP BY 1;

-- 2025-10-21T13:30:00Z | user=jorge.martinez@acme.io | job_jm345 | 265000 | 7000 | SUCCESS
SELECT utm_campaign, sum(attributed_revenue_usd) FROM `nexus-analyst-demo.acme.fact_marketing_touches` GROUP BY 1;

-- 2025-10-22T08:45:00Z | user=david.kim@acme.io | job_dk678 | 7000000 | 26000 | SUCCESS
SELECT triggered_by, status, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` GROUP BY 1, 2;

-- 2025-10-23T10:00:00Z | user=rajiv.menon@acme.io | job_rm901 | 135000 | 4500 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.dim_employees` WHERE team = 'Sales';

-- 2025-10-24T14:45:00Z | user=lina.cho@acme.io | job_lc234 | 128000 | 4600 | SUCCESS
SELECT change_type, avg(mrr_usd) FROM `nexus-analyst-demo.acme.fact_subscriptions` GROUP BY 1;

-- 2025-10-25T09:15:00Z | user=nina.patel@acme.io | job_np567 | 2300000 | 10500 | SUCCESS
SELECT customer_id, avg(score) FROM `nexus-analyst-demo.acme.fact_nps_responses` WHERE responded_at > '2025-07-01' GROUP BY 1;

-- 2025-10-26T15:30:00Z | user=jorge.martinez@acme.io | job_jm890 | 275000 | 7300 | SUCCESS
SELECT loss_reason, sum(amount_usd) FROM `nexus-analyst-demo.acme.fact_opportunities` WHERE stage = 'Closed Lost' GROUP BY 1;

-- 2025-10-27T11:00:00Z | user=david.kim@acme.io | job_dk123 | 2900000 | 12000 | SUCCESS
SELECT run_date, sum(auth_failed_count) FROM `nexus-analyst-demo.acme.workflow_runs_daily` GROUP BY 1;

-- 2025-10-28T12:15:00Z | user=rajiv.menon@acme.io | job_rm456 | 112000 | 3500 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.account_health` WHERE account_health_status = 'stable';

-- 2025-10-29T09:30:00Z | user=lina.cho@acme.io | job_lc789 | 310000 | 7000 | SUCCESS
SELECT cohort_size, expansion_mrr_usd FROM `nexus-analyst-demo.acme.nrr_trailing_12` ORDER BY expansion_mrr_usd DESC;

-- 2025-10-30T14:15:00Z | user=nina.patel@acme.io | job_np012 | 3300000 | 14500 | SUCCESS
SELECT user_id, count(event_id) FROM `nexus-analyst-demo.acme.fact_user_events` GROUP BY 1 HAVING count(event_id) > 500;

-- 2025-10-31T10:30:00Z | user=jorge.martinez@acme.io | job_jm345 | 285000 | 7600 | SUCCESS
SELECT first_touch_channel, count(distinct customer_id) FROM `nexus-analyst-demo.acme.bookings_attribution` GROUP BY 1;

-- 2025-11-01T12:00:00Z | user=david.kim@acme.io | job_dk678 | 7500000 | 28000 | SUCCESS
SELECT customer_id, avg(duration_ms) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE status = 'success' GROUP BY 1;

-- 2025-11-02T08:15:00Z | user=rajiv.menon@acme.io | job_rm901 | 145000 | 5000 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE country = 'GBR';

-- 2025-11-03T11:45:00Z | user=lina.cho@acme.io | job_lc234 | 138000 | 5000 | SUCCESS
SELECT plan_tier, sum(seat_count) FROM `nexus-analyst-demo.acme.fact_subscriptions` WHERE is_current = true GROUP BY 1;

-- 2025-11-04T15:15:00Z | user=nina.patel@acme.io | job_np567 | 2500000 | 11500 | SUCCESS
SELECT assigned_to_employee_id, avg(resolution_time_hours) FROM `nexus-analyst-demo.acme.fact_support_tickets` GROUP BY 1;

-- 2025-11-05T10:45:00Z | user=jorge.martinez@acme.io | job_jm890 | 295000 | 7900 | SUCCESS
SELECT ae_employee_id, sdr_employee_id, sum(amount_usd) FROM `nexus-analyst-demo.acme.fact_opportunities` WHERE stage = 'Closed Won' GROUP BY 1, 2;

-- 2025-11-06T14:00:00Z | user=david.kim@acme.io | job_dk123 | 3100000 | 13000 | SUCCESS
SELECT run_date, sum(step_count) FROM `nexus-analyst-demo.acme.workflow_runs_daily` d JOIN `nexus-analyst-demo.acme.fact_workflow_runs` r ON d.customer_id = r.customer_id GROUP BY 1;

-- 2025-11-07T12:30:00Z | user=rajiv.menon@acme.io | job_rm456 | 122000 | 3800 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.dim_users` WHERE role = 'editor';

-- 2025-11-08T09:45:00Z | user=lina.cho@acme.io | job_lc789 | 330000 | 7500 | SUCCESS
SELECT snapshot_date, arr_usd FROM `nexus-analyst-demo.acme.arr_snapshot` WHERE snapshot_date > '2025-10-01';

-- 2025-11-09T11:15:00Z | user=nina.patel@acme.io | job_np012 | 3500000 | 15500 | SUCCESS
SELECT customer_id, event_name, count(*) FROM `nexus-analyst-demo.acme.fact_user_events` GROUP BY 1, 2;

-- 2025-11-10T13:30:00Z | user=jorge.martinez@acme.io | job_jm345 | 305000 | 8200 | SUCCESS
SELECT utm_source, utm_medium, count(*) FROM `nexus-analyst-demo.acme.fact_marketing_touches` GROUP BY 1, 2;

-- 2025-11-11T08:45:00Z | user=david.kim@acme.io | job_dk678 | 8000000 | 30000 | SUCCESS
SELECT status, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE triggered_at > '2025-11-01' GROUP BY 1;

-- 2025-11-12T10:00:00Z | user=rajiv.menon@acme.io | job_rm901 | 155000 | 5500 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.dim_employees` WHERE location = 'SF';

-- 2025-11-13T14:45:00Z | user=lina.cho@acme.io | job_lc234 | 148000 | 5400 | SUCCESS
SELECT billing_cycle, sum(mrr_usd) FROM `nexus-analyst-demo.acme.fact_subscriptions` WHERE start_date > '2025-01-01' GROUP BY 1;

-- 2025-11-14T09:15:00Z | user=nina.patel@acme.io | job_np567 | 2700000 | 12500 | SUCCESS
SELECT customer_id, count(*) FROM `nexus-analyst-demo.acme.fact_support_tickets` WHERE closed_at IS NULL AND priority = 'P1' GROUP BY 1;

-- 2025-11-15T15:30:00Z | user=jorge.martinez@acme.io | job_jm890 | 315000 | 8500 | SUCCESS
SELECT industry, sum(bookings_acv_usd) FROM `nexus-analyst-demo.acme.bookings_attribution` b JOIN `nexus-analyst-demo.acme.dim_customers` c ON b.customer_id = c.customer_id GROUP BY 1;

-- 2025-11-16T11:00:00Z | user=david.kim@acme.io | job_dk123 | 3300000 | 14000 | SUCCESS
SELECT run_date, sum(rate_limited_count) FROM `nexus-analyst-demo.acme.workflow_runs_daily` GROUP BY 1;

-- 2025-11-17T12:15:00Z | user=rajiv.menon@acme.io | job_rm456 | 132000 | 4100 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.account_health` WHERE has_open_p1_over_48h = true;

-- 2025-11-18T09:30:00Z | user=lina.cho@acme.io | job_lc789 | 350000 | 8000 | SUCCESS
SELECT year, quarter, sum(expansion_mrr_usd) FROM `nexus-analyst-demo.acme.nrr_trailing_12` GROUP BY 1, 2;

-- 2025-11-19T14:15:00Z | user=nina.patel@acme.io | job_np012 | 3700000 | 16500 | SUCCESS
SELECT user_id, count(event_id) FROM `nexus-analyst-demo.acme.fact_user_events` WHERE event_name = 'workflow_edited' GROUP BY 1;

-- 2025-11-20T10:30:00Z | user=jorge.martinez@acme.io | job_jm345 | 325000 | 8800 | SUCCESS
SELECT utm_campaign, count(distinct opportunity_id) FROM `nexus-analyst-demo.acme.fact_marketing_touches` m JOIN `nexus-analyst-demo.acme.fact_opportunities` o ON m.customer_id = o.customer_id GROUP BY 1;

-- 2025-11-21T13:45:00Z | user=david.kim@acme.io | job_dk678 | 8500000 | 32000 | SUCCESS
SELECT triggered_by, avg(duration_ms) FROM `nexus-analyst-demo.acme.fact_workflow_runs` GROUP BY 1;

-- 2025-11-22T08:00:00Z | user=rajiv.menon@acme.io | job_rm901 | 165000 | 6000 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE acquisition_channel = 'referral';

-- 2025-11-23T11:30:00Z | user=lina.cho@acme.io | job_lc234 | 158000 | 5800 | SUCCESS
SELECT plan_tier, avg(seat_count) FROM `nexus-analyst-demo.acme.fact_subscriptions` WHERE is_current = true GROUP BY 1;

-- 2025-11-24T15:00:00Z | user=nina.patel@acme.io | job_np567 | 2900000 | 13500 | SUCCESS
SELECT category, score FROM `nexus-analyst-demo.acme.fact_support_tickets` t JOIN `nexus-analyst-demo.acme.fact_nps_responses` n ON t.customer_id = n.customer_id WHERE t.priority = 'P1';

-- 2025-11-25T10:15:00Z | user=jorge.martinez@acme.io | job_jm890 | 335000 | 9100 | SUCCESS
SELECT ae_employee_id, sum(amount_usd) FROM `nexus-analyst-demo.acme.fact_opportunities` WHERE stage = 'Closed Won' AND closed_won_at > '2025-10-01' GROUP BY 1;

-- 2025-11-26T14:30:00Z | user=david.kim@acme.io | job_dk123 | 3500000 | 15000 | SUCCESS
SELECT run_date, sum(step_timeout_count) FROM `nexus-analyst-demo.acme.workflow_runs_daily` GROUP BY 1;

-- 2025-11-27T12:00:00Z | user=rajiv.menon@acme.io | job_rm456 | 142000 | 4400 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.dim_users` WHERE last_login_date > '2025-11-01';

-- 2025-11-28T09:45:00Z | user=lina.cho@acme.io | job_lc789 | 370000 | 8500 | SUCCESS
SELECT snapshot_date, arr_usd FROM `nexus-analyst-demo.acme.arr_snapshot` ORDER BY snapshot_date DESC LIMIT 5;

-- 2025-11-29T11:15:00Z | user=nina.patel@acme.io | job_np012 | 3900000 | 17500 | SUCCESS
SELECT customer_id, count(distinct event_name) FROM `nexus-analyst-demo.acme.fact_user_events` WHERE event_at > '2025-11-01' GROUP BY 1;

-- 2025-11-30T13:30:00Z | user=jorge.martinez@acme.io | job_jm345 | 345000 | 9400 | SUCCESS
SELECT utm_source, sum(bookings_acv_usd) FROM `nexus-analyst-demo.acme.bookings_attribution` GROUP BY 1;

-- 2025-12-01T08:45:00Z | user=david.kim@acme.io | job_dk678 | 9000000 | 34000 | SUCCESS
SELECT status, error_code, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE triggered_at > '2025-12-01' GROUP BY 1, 2;

-- 2025-12-02T10:00:00Z | user=rajiv.menon@acme.io | job_rm901 | 175000 | 6500 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.dim_employees` WHERE role = 'AE';

-- 2025-12-03T14:45:00Z | user=lina.cho@acme.io | job_lc234 | 168000 | 6200 | SUCCESS
SELECT plan_tier, sum(mrr_usd) FROM `nexus-analyst-demo.acme.fact_subscriptions` WHERE is_current = true GROUP BY 1;

-- 2025-12-04T09:15:00Z | user=nina.patel@acme.io | job_np567 | 3100000 | 14500 | SUCCESS
SELECT customer_id, count(*) FROM `nexus-analyst-demo.acme.fact_support_tickets` WHERE category = 'bug' GROUP BY 1;

-- 2025-12-05T15:30:00Z | user=jorge.martinez@acme.io | job_jm890 | 355000 | 9700 | SUCCESS
SELECT region, count(*) FROM `nexus-analyst-demo.acme.dim_customers` WHERE status = 'churned' GROUP BY 1;

-- 2025-12-06T11:00:00Z | user=david.kim@acme.io | job_dk123 | 3700000 | 16000 | SUCCESS
SELECT run_date, sum(n_runs) FROM `nexus-analyst-demo.acme.workflow_runs_daily` WHERE run_date > '2025-12-01' GROUP BY 1;

-- 2025-12-07T12:15:00Z | user=rajiv.menon@acme.io | job_rm456 | 152000 | 4700 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.account_health` WHERE utilization_band = 'high';

-- 2025-12-08T09:30:00Z | user=lina.cho@acme.io | job_lc789 | 390000 | 9000 | SUCCESS
SELECT cohort_size, nrr FROM `nexus-analyst-demo.acme.nrr_trailing_12` WHERE cohort_start_mrr_usd > 100000;

-- 2025-12-09T14:15:00Z | user=nina.patel@acme.io | job_np012 | 4100000 | 18500 | SUCCESS
SELECT user_id, event_name FROM `nexus-analyst-demo.acme.fact_user_events` WHERE event_at > '2025-12-01';

-- 2025-12-10T10:30:00Z | user=jorge.martinez@acme.io | job_jm345 | 365000 | 10000 | SUCCESS
SELECT year, month, sum(amount_usd) FROM `nexus-analyst-demo.acme.fact_opportunities` o JOIN `nexus-analyst-demo.acme.dim_dates` d ON o.closed_won_at = d.date GROUP BY 1, 2;

-- 2025-12-11T13:45:00Z | user=david.kim@acme.io | job_dk678 | 9500000 | 36000 | SUCCESS
SELECT triggered_by, status, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE triggered_at > '2025-12-01' GROUP BY 1, 2;

-- 2025-12-12T08:15:00Z | user=rajiv.menon@acme.io | job_rm901 | 185000 | 7000 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE industry = 'logistics';

-- 2025-12-13T11:45:00Z | user=lina.cho@acme.io | job_lc234 | 178000 | 6600 | SUCCESS
SELECT plan_tier, avg(mrr_usd) FROM `nexus-analyst-demo.acme.fact_subscriptions` WHERE is_current = true GROUP BY 1;

-- 2025-12-14T15:15:00Z | user=nina.patel@acme.io | job_np567 | 3300000 | 15500 | SUCCESS
SELECT customer_id, avg(resolution_time_hours) FROM `nexus-analyst-demo.acme.fact_support_tickets` WHERE opened_at > '2025-10-01' GROUP BY 1;

-- 2025-12-15T10:45:00Z | user=jorge.martinez@acme.io | job_jm890 | 375000 | 10300 | SUCCESS
SELECT ae_employee_id, count(*) FROM `nexus-analyst-demo.acme.fact_opportunities` WHERE stage = 'Closed Won' AND closed_won_at > '2025-01-01' GROUP BY 1;

-- 2025-12-16T14:00:00Z | user=david.kim@acme.io | job_dk123 | 3900000 | 17000 | SUCCESS
SELECT run_date, sum(auth_failed_count) FROM `nexus-analyst-demo.acme.workflow_runs_daily` WHERE run_date > '2025-01-01' GROUP BY 1;

-- 2025-12-17T12:30:00Z | user=rajiv.menon@acme.io | job_rm456 | 162000 | 5000 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.dim_users` WHERE is_active = true AND role = 'viewer';

-- 2025-12-18T09:45:00Z | user=lina.cho@acme.io | job_lc789 | 410000 | 9500 | SUCCESS
SELECT snapshot_date, arr_pro_usd FROM `nexus-analyst-demo.acme.arr_snapshot` ORDER BY snapshot_date DESC LIMIT 12;

-- 2025-12-19T11:15:00Z | user=nina.patel@acme.io | job_np012 | 4300000 | 19500 | SUCCESS
SELECT customer_id, count(event_id) FROM `nexus-analyst-demo.acme.fact_user_events` WHERE event_at > '2025-12-01' GROUP BY 1;

-- 2025-12-20T13:30:00Z | user=jorge.martinez@acme.io | job_jm345 | 385000 | 10600 | SUCCESS
SELECT utm_source, sum(attributed_revenue_usd) FROM `nexus-analyst-demo.acme.fact_marketing_touches` WHERE touched_at > '2025-01-01' GROUP BY 1;

-- 2025-12-21T08:45:00Z | user=david.kim@acme.io | job_dk678 | 10000000 | 38000 | SUCCESS
SELECT status, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` GROUP BY 1;

-- 2025-12-22T10:00:00Z | user=rajiv.menon@acme.io | job_rm901 | 195000 | 7500 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.dim_employees` WHERE is_active = true AND hire_date < '2025-01-01';

-- 2025-12-23T14:45:00Z | user=lina.cho@acme.io | job_lc234 | 188000 | 7000 | SUCCESS
SELECT change_type, sum(mrr_usd) FROM `nexus-analyst-demo.acme.fact_subscriptions` WHERE start_date > '2025-01-01' GROUP BY 1;

-- 2025-12-24T09:15:00Z | user=nina.patel@acme.io | job_np567 | 3500000 | 16500 | SUCCESS
SELECT customer_id, score FROM `nexus-analyst-demo.acme.fact_nps_responses` WHERE score < 5;

-- 2025-12-25T15:30:00Z | user=jorge.martinez@acme.io | job_jm890 | 395000 | 10900 | SUCCESS
SELECT ae_employee_id, count(*) FROM `nexus-analyst-demo.fact_opportunities` WHERE stage = 'Closed Won' GROUP BY 1;

-- 2025-12-26T11:00:00Z | user=david.kim@acme.io | job_dk123 | 4100000 | 18000 | SUCCESS
SELECT run_date, sum(n_runs) FROM `nexus-analyst-demo.acme.workflow_runs_daily` GROUP BY 1 ORDER BY 1 DESC;

-- 2025-12-27T12:30:00Z | user=rajiv.menon@acme.io | job_rm456 | 172000 | 5300 | SUCCESS
SELECT * FROM `nexus-analyst-demo.acme.account_health` WHERE has_recent_nps_detractor = true OR n_open_p1_over_48h > 0;

-- 2025-12-28T09:45:00Z | user=lina.cho@acme.io | job_lc789 | 430000 | 10000 | SUCCESS
SELECT year, sum(churned_mrr_loss_usd) FROM `nexus-analyst-demo.acme.nrr_trailing_12` GROUP BY 1;

-- 2025-12-29T11:15:00Z | user=nina.patel@acme.io | job_np012 | 4500000 | 20500 | SUCCESS
SELECT user_id, count(event_id) FROM `nexus-analyst-demo.acme.fact_user_events` WHERE event_at > '2025-01-01' GROUP BY 1 HAVING count(event_id) > 1000;

-- 2025-12-30T13:30:00Z | user=jorge.martinez@acme.io | job_jm345 | 405000 | 11200 | SUCCESS
SELECT utm_source, count(distinct lead_email_hash) FROM `nexus-analyst-demo.acme.fact_marketing_touches` GROUP BY 1 ORDER BY 2 DESC;

-- 2025-12-31T08:45:00Z | user=david.kim@acme.io | job_dk678 | 10500000 | 40000 | SUCCESS
SELECT status, error_code, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE triggered_at > '2025-01-01' GROUP BY 1, 2;