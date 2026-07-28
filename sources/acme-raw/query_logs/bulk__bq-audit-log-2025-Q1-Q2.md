---
title: "BigQuery JOBS_BY_USER audit export — 2025 Q1-Q2"
source_url: "internal://acme/bq-audit-log-2025-Q1-Q2"
license: "synthetic-demo"
attribution: "Synthetic content, Acme Inc internal demo. Acme Inc is a fictitious company."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: query_log
---

-- 2025-01-02 09:12:44 | user=rajiv.menon@acme.io | job_x7721_init | 0 | 120 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.INFORMATION_SCHEMA.TABLES`;
-- 2025-01-02 09:15:22 | user=lina.cho@acme.io | job_arr_check_001 | 4294967296 | 1850 | SUCCESS | 
    /* Quick ARR check for Rachel before the board deck prep starts. 
       Using dim_customers as a proxy since I don't trust the sub table yet. */
    SELECT 
        SUM(current_mrr_usd) * 12 AS total_arr_est,
        account_tier
    FROM `nexus-analyst-demo.acme.dim_customers`
    WHERE status = 'active'
    GROUP BY 2
    ORDER BY 1 DESC;
-- 2025-01-02 09:45:10 | user=david.kim@acme.io | job_raw_audit_01 | 1073741824 | 800 | SUCCESS | SELECT count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE triggered_at >= '2025-01-01';
-- 2025-01-02 10:12:05 | user=nina.patel@acme.io | job_engagement_v1 | 8589934592 | 4200 | SUCCESS | 
    -- Nina: checking how many users logged in over the holidays
    -- Using the old 'any login in 28d' definition for now
    SELECT 
        c.company_name,
        count(u.user_id) as active_user_count
    FROM `nexus-analyst-demo.acme.dim_customers` c
    JOIN `nexus-analyst-demo.acme.dim_users` u ON c.customer_id = u.customer_id
    WHERE u.last_login_date >= DATE_SUB('2025-01-02', INTERVAL 28 DAY)
    GROUP BY 1
    HAVING active_user_count > 0;
-- 2025-01-03 11:30:01 | user=lina.cho@acme.io | job_nrr_fail_01 | 2147483648 | 1500 | FAILURE | 
    -- Trying to access the finance mart Rajiv mentioned, but getting 'Table not found'
    SELECT * FROM `nexus-analyst-demo.acme.marts.finance.arr_snapshot` LIMIT 100;
-- 2025-01-03 11:32:45 | user=rajiv.menon@acme.io | job_fix_lina | 0 | 50 | SUCCESS | 
    -- Lina, the dataset is FLAT. Use acme.arr_snapshot, not marts.finance.
    SELECT snapshot_date, arr_usd FROM `nexus-analyst-demo.acme.arr_snapshot` ORDER BY snapshot_date DESC LIMIT 5;
-- 2025-01-05 14:00:22 | user=jasmine.park@acme.io | job_mktg_01 | 5368709120 | 3100 | SUCCESS | 
    -- Checking channel performance for Q4 2024 to set Q1 2025 targets
    SELECT 
        acquisition_channel,
        count(customer_id) as new_customers,
        sum(current_mrr_usd) as mrr_added
    FROM `nexus-analyst-demo.acme.dim_customers`
    WHERE signup_date BETWEEN '2024-10-01' AND '2024-12-31'
    GROUP BY 1;
-- 2025-01-06 16:45:12 | user=jorge.martinez@acme.io | job_ae_audit | 12884901888 | 9400 | SUCCESS | 
    WITH ae_deals AS (
        SELECT 
            ae_employee_id,
            count(opportunity_id) as closed_won_count,
            sum(amount_usd) as total_bookings_acv
        FROM `nexus-analyst-demo.acme.fact_opportunities`
        WHERE stage = 'Closed Won' 
          AND closed_won_at >= '2024-01-01'
        GROUP BY 1
    )
    SELECT 
        e.full_name,
        d.closed_won_count,
        d.total_bookings_acv,
        d.total_bookings_acv / 12 as monthly_avg -- Wait, is bookings already annualized?
    FROM ae_deals d
    JOIN `nexus-analyst-demo.acme.dim_employees` e ON d.ae_employee_id = e.employee_id;
-- 2025-01-07 08:22:19 | user=lina.cho@acme.io | job_arr_recalc | 4294967296 | 2100 | SUCCESS | 
    -- Rachel asking why ARR is lower than expected. 
    -- checking the current active subscriptions to get a real ARR.
    -- Signal [arr]: ~$33M-35M in early 2025.
    SELECT 
        SUM(mrr_usd) * 12 as calculated_arr
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE is_current = true 
      AND plan_tier != 'Free';
-- 2025-01-08 10:05:55 | user=nina.patel@acme.io | job_health_check_fail | 0 | 200 | FAILURE | 
    SELECT * FROM `nexus-analyst-demo.acme.marts.cs.account_health`; -- ERROR: Dataset acme.marts.cs does not exist.
-- 2025-01-10 12:00:00 | user=david.kim@acme.io | job_schema_dump | 0 | 300 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.INFORMATION_SCHEMA.COLUMNS` WHERE table_name = 'fact_workflow_runs';
-- 2025-01-12 15:30:44 | user=lina.cho@acme.io | job_nrr_inner_join_mistake | 6442450944 | 5500 | SUCCESS | 
    /* 
       DRAFT NRR calc. 
       NOTE: This is WRONG because it uses an INNER JOIN, 
       dropping anyone who churned (no current subscription).
       Inflates NRR to like 120% when it should be ~107%.
    */
    WITH cohort_2024 AS (
        SELECT customer_id, mrr_usd as start_mrr
        FROM `nexus-analyst-demo.acme.fact_subscriptions`
        WHERE start_date <= '2024-01-01' AND (end_date > '2024-01-01' OR end_date IS NULL)
          AND plan_tier != 'Free'
    ),
    cohort_2025 AS (
        SELECT customer_id, mrr_usd as end_mrr
        FROM `nexus-analyst-demo.acme.fact_subscriptions`
        WHERE is_current = true
          AND plan_tier != 'Free'
    )
    SELECT 
        SUM(c24.start_mrr) as base_mrr,
        SUM(c25.end_mrr) as ending_mrr,
        SUM(c25.end_mrr) / SUM(c24.start_mrr) as nrr_inflated
    FROM cohort_2024 c24
    INNER JOIN cohort_2025 c25 ON c24.customer_id = c25.customer_id;
-- 2025-01-15 09:44:12 | user=rajiv.menon@acme.io | job_dbt_run_arr | 536870912 | 1100 | SUCCESS | 
    -- Refreshing arr_snapshot for the mid-month finance review.
    CREATE OR REPLACE TABLE `nexus-analyst-demo.acme.arr_snapshot` AS
    SELECT 
        CURRENT_DATE() as snapshot_date,
        SUM(CASE WHEN plan_tier = 'Pro' THEN mrr_usd * 12 ELSE 0 END) as arr_pro_usd,
        SUM(CASE WHEN plan_tier = 'Business' THEN mrr_usd * 12 ELSE 0 END) as arr_business_usd,
        SUM(CASE WHEN plan_tier = 'Enterprise' THEN mrr_usd * 12 ELSE 0 END) as arr_enterprise_usd,
        SUM(mrr_usd * 12) as arr_usd,
        COUNT(DISTINCT customer_id) as paying_customers
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE is_current = true AND plan_tier != 'Free';
-- 2025-01-20 14:15:00 | user=nina.patel@acme.io | job_step_counts | 21474836480 | 12000 | SUCCESS | 
    -- Nina: Investigating if higher step counts lead to more AUTH_FAILED errors.
    -- Noise: testing the error_code enum
    SELECT 
        error_code,
        avg(step_count) as avg_steps,
        count(*) as run_count
    FROM `nexus-analyst-demo.acme.fact_workflow_runs`
    WHERE triggered_at >= '2025-01-01'
    GROUP BY 1
    ORDER BY 3 DESC;
-- 2025-01-25 11:22:33 | user=lina.cho@acme.io | job_cust_audit_beacon | 1073741824 | 900 | SUCCESS | 
    -- Audit for cust_000287 Beacon Studios. AE asking about their health.
    SELECT 
        c.company_name,
        c.account_tier,
        c.current_plan_tier,
        s.mrr_usd,
        c.status
    FROM `nexus-analyst-demo.acme.dim_customers` c
    JOIN `nexus-analyst-demo.acme.fact_subscriptions` s ON c.customer_id = s.customer_id
    WHERE c.customer_id = 'cust_000287' AND s.is_current = true;
-- 2025-02-01 10:00:05 | user=david.kim@acme.io | job_usage_stats_feb | 32212254720 | 25000 | SUCCESS | 
    -- Monitoring ingestion volume for Jan
    SELECT 
        date(triggered_at) as day,
        status,
        count(*) as total_runs
    FROM `nexus-analyst-demo.acme.fact_workflow_runs`
    WHERE triggered_at BETWEEN '2025-01-01' AND '2025-01-31'
    GROUP BY 1, 2
    ORDER BY 1, 2;
-- 2025-02-04 15:10:22 | user=nina.patel@acme.io | job_engagement_rethink | 10737418240 | 6800 | SUCCESS | 
    /* 
       Exploratory query for new engagement definition.
       Old: ≥1 login in 28d.
       Proposed: ≥3 active users AND ≥10 successful runs in 28d.
    */
    WITH user_counts AS (
        SELECT 
            customer_id, 
            count(distinct user_id) as n_users
        FROM `nexus-analyst-demo.acme.fact_user_events`
        WHERE event_at >= DATE_SUB('2025-02-04', INTERVAL 28 DAY)
        GROUP BY 1
    ),
    run_counts AS (
        SELECT 
            customer_id,
            count(*) as n_success_runs
        FROM `nexus-analyst-demo.acme.fact_workflow_runs`
        WHERE status = 'SUCCESS' -- wait, logic check: is SUCCESS a status or error_code?
          AND triggered_at >= DATE_SUB('2025-02-04', INTERVAL 28 DAY)
        GROUP BY 1
    )
    SELECT 
        u.customer_id,
        u.n_users,
        r.n_success_runs,
        (u.n_users >= 3 AND r.n_success_runs >= 10) as is_engaged_new
    FROM user_counts u
    LEFT JOIN run_counts r ON u.customer_id = r.customer_id;
-- 2025-02-10 09:30:45 | user=lina.cho@acme.io | job_nrr_correct_attempt | 8589934592 | 7200 | SUCCESS | 
    /*
       NRR Trailing 12 Month - Correct logic attempt.
       Signal [nrr]: Use LEFT JOIN and COALESCE to keep churned customers in the denominator.
    */
    WITH cohort_base AS (
        SELECT customer_id, mrr_usd as start_mrr
        FROM `nexus-analyst-demo.acme.fact_subscriptions`
        WHERE start_date <= '2024-02-01' 
          AND (end_date > '2024-02-01' OR end_date IS NULL)
          AND plan_tier != 'Free'
    ),
    cohort_end AS (
        SELECT customer_id, mrr_usd as end_mrr
        FROM `nexus-analyst-demo.acme.fact_subscriptions`
        WHERE is_current = true
          AND plan_tier != 'Free'
    )
    SELECT 
        SUM(cb.start_mrr) as cohort_start_mrr,
        SUM(COALESCE(ce.end_mrr, 0)) as cohort_end_mrr,
        SUM(COALESCE(ce.end_mrr, 0)) / SUM(cb.start_mrr) as nrr
    FROM cohort_base cb
    LEFT JOIN cohort_end ce ON cb.customer_id = ce.customer_id;
-- 2025-02-12 11:45:19 | user=jasmine.park@acme.io | job_campaign_roi | 2147483648 | 1500 | SUCCESS | 
    SELECT 
        utm_source,
        utm_campaign,
        count(distinct customer_id) as converted_customers,
        sum(attributed_revenue_usd) as total_revenue
    FROM `nexus-analyst-demo.acme.fact_marketing_touches`
    WHERE touched_at >= '2025-01-01'
    GROUP BY 1, 2
    ORDER BY 4 DESC;
-- 2025-02-15 14:02:10 | user=rajiv.menon@acme.io | job_cleanup_marts | 0 | 500 | SUCCESS | 
    -- Dropping old test tables in personal dataset
    -- DROP TABLE `nexus-analyst-demo.acme.tmp_arr_calc_rajiv`;
-- 2025-02-18 16:20:33 | user=lina.cho@acme.io | job_churn_audit_beacon | 536870912 | 600 | SUCCESS | 
    -- Beacon Studios (cust_000287) just churned. Rachel wants to know if they were healthy.
    -- Signal: Beacon was healthy but churned for parent company reasons.
    SELECT 
        c.company_name,
        c.status,
        c.churn_date,
        h.account_health_status,
        h.is_engaged,
        h.utilization_band
    FROM `nexus-analyst-demo.acme.dim_customers` c
    LEFT JOIN `nexus-analyst-demo.acme.account_health` h ON c.customer_id = h.customer_id
    WHERE c.customer_id = 'cust_000287';
-- 2025-02-20 09:12:12 | user=jorge.martinez@acme.io | job_crm_mapping | 10737418240 | 8800 | SUCCESS | 
    -- Mapping CRM stages to our warehouse fact_opportunities
    SELECT 
        stage, 
        count(*) as n_opps, 
        avg(amount_usd) as avg_acv
    FROM `nexus-analyst-demo.acme.fact_opportunities`
    GROUP BY 1;
-- 2025-02-25 13:45:00 | user=nina.patel@acme.io | job_latency_check | 42949672960 | 32000 | SUCCESS | 
    -- P95 and P99 duration by plan tier
    SELECT 
        c.current_plan_tier,
        APPROX_QUANTILES(duration_ms, 100)[OFFSET(95)] as p95_ms,
        APPROX_QUANTILES(duration_ms, 100)[OFFSET(99)] as p99_ms
    FROM `nexus-analyst-demo.acme.fact_workflow_runs` r
    JOIN `nexus-analyst-demo.acme.dim_customers` c ON r.customer_id = c.customer_id
    WHERE r.triggered_at >= '2025-02-01'
    GROUP BY 1;
-- 2025-03-01 10:30:15 | user=lina.cho@acme.io | job_q1_forecast | 5368709120 | 4500 | SUCCESS | 
    -- Q1 mid-quarter check. ARR should be around $34M by now.
    SELECT 
        snapshot_date, 
        arr_usd / 1000000 as arr_millions 
    FROM `nexus-analyst-demo.acme.arr_snapshot` 
    WHERE snapshot_date >= '2025-01-01'
    ORDER BY 1;
-- 2025-03-05 15:44:22 | user=david.kim@acme.io | job_error_analysis | 10737418240 | 9200 | SUCCESS | 
    -- Looking for SCHEMA_MISMATCH errors for the devtools industry
    SELECT 
        c.company_name,
        r.error_code,
        count(*) as error_count
    FROM `nexus-analyst-demo.acme.fact_workflow_runs` r
    JOIN `nexus-analyst-demo.acme.dim_customers` c ON r.customer_id = c.customer_id
    WHERE c.industry = 'devtools' 
      AND r.error_code = 'SCHEMA_MISMATCH'
      AND r.triggered_at >= '2025-02-01'
    GROUP BY 1, 2;
-- 2025-03-10 11:12:19 | user=jasmine.park@acme.io | job_bookings_by_channel | 2147483648 | 1800 | SUCCESS | 
    /* 
       Signal [bookings]: bookings_acv_usd is already annualized.
       AE-led deals only (inbound, outbound, etc).
    */
    SELECT 
        first_touch_channel,
        sum(bookings_acv_usd) as total_acv_won
    FROM `nexus-analyst-demo.acme.bookings_attribution`
    WHERE closed_won_at BETWEEN '2025-01-01' AND '2025-03-10'
    GROUP BY 1;
-- 2025-03-15 09:00:00 | user=rajiv.menon@acme.io | job_dbt_run_nrr | 4294967296 | 3500 | SUCCESS | 
    -- Materializing the nrr_trailing_12 mart. 
    -- Signal: cohort = paid customers 12mo ago.
    -- Signal: Churned stay in cohort at $0.
    CREATE OR REPLACE TABLE `nexus-analyst-demo.acme.nrr_trailing_12` AS
    WITH base_date AS (SELECT DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH) as dt),
    cohort AS (
        SELECT customer_id, mrr_usd as start_mrr
        FROM `nexus-analyst-demo.acme.fact_subscriptions`, base_date
        WHERE start_date <= dt AND (end_date > dt OR end_date IS NULL)
          AND plan_tier != 'Free'
    ),
    current_vals AS (
        SELECT customer_id, mrr_usd as end_mrr
        FROM `nexus-analyst-demo.acme.fact_subscriptions`
        WHERE is_current = true AND plan_tier != 'Free'
    )
    SELECT 
        COUNT(c.customer_id) as cohort_size,
        SUM(c.start_mrr) * 12 as cohort_start_arr_usd,
        SUM(COALESCE(cv.end_mrr, 0)) * 12 as cohort_end_arr_usd,
        SUM(COALESCE(cv.end_mrr, 0)) / SUM(c.start_mrr) as nrr,
        LEAST(1.0, SUM(CASE WHEN cv.end_mrr > c.start_mrr THEN c.start_mrr ELSE COALESCE(cv.end_mrr, 0) END) / SUM(c.start_mrr)) as grr
    FROM cohort c
    LEFT JOIN current_vals cv ON c.customer_id = cv.customer_id;
-- 2025-03-20 14:33:01 | user=nina.patel@acme.io | job_enterprise_health | 1073741824 | 1100 | SUCCESS | 
    /*
       Checking Enterprise health rules.
       Signal: Enterprise critical ONLY on uncollectible invoice.
    */
    SELECT 
        c.company_name,
        h.account_health_status,
        h.utilization_band -- Should be NULL for Enterprise
    FROM `nexus-analyst-demo.acme.dim_customers` c
    JOIN `nexus-analyst-demo.acme.account_health` h ON c.customer_id = h.customer_id
    WHERE c.account_tier = 'Ent';
-- 2025-03-25 10:10:45 | user=lina.cho@acme.io | job_q1_close_prep | 5368709120 | 3800 | SUCCESS | 
    -- Final check on invoice status for Q1
    SELECT 
        status, 
        sum(amount_usd) as total_invoiced
    FROM `nexus-analyst-demo.acme.fact_invoices`
    WHERE invoice_date BETWEEN '2025-01-01' AND '2025-03-31'
    GROUP BY 1;
-- 2025-03-28 16:55:22 | user=jorge.martinez@acme.io | job_ae_performance_q1 | 2147483648 | 2000 | SUCCESS | 
    -- AE quarterly rankings
    SELECT 
        e.full_name,
        sum(o.amount_usd) as bookings_acv
    FROM `nexus-analyst-demo.acme.fact_opportunities` o
    JOIN `nexus-analyst-demo.acme.dim_employees` e ON o.ae_employee_id = e.employee_id
    WHERE o.stage = 'Closed Won' 
      AND o.closed_won_at BETWEEN '2025-01-01' AND '2025-03-31'
    GROUP BY 1
    ORDER BY 2 DESC;
-- 2025-04-01 09:15:10 | user=david.kim@acme.io | job_new_quarter_init | 0 | 100 | SUCCESS | SELECT 1;
-- 2025-04-02 11:22:33 | user=lina.cho@acme.io | job_arr_q1_final | 536870912 | 800 | SUCCESS | 
    -- Final ARR for Q1. Rachel needs this for the Series B prep doc.
    -- Signal: ARR should be ~$35M.
    SELECT 
        snapshot_date,
        arr_usd
    FROM `nexus-analyst-demo.acme.arr_snapshot`
    WHERE snapshot_date = '2025-03-31';
-- 2025-04-05 14:40:00 | user=nina.patel@acme.io | job_engaged_monitoring | 10737418240 | 7500 | SUCCESS | 
    /* 
       Nina: Finding customers in 'monitoring' health who should be 'engaged'.
       Recalibrated engagement: 3+ users, 10+ runs.
    */
    SELECT 
        c.customer_id,
        c.company_name,
        h.account_health_status
    FROM `nexus-analyst-demo.acme.dim_customers` c
    JOIN `nexus-analyst-demo.acme.account_health` h ON c.customer_id = h.customer_id
    WHERE h.account_health_status = 'monitoring'
      AND h.is_engaged = true; -- If they are engaged but status is monitoring, they might be improving.
-- 2025-04-10 10:05:12 | user=jasmine.park@acme.io | job_marketing_touches_q2 | 4294967296 | 3200 | SUCCESS | 
    SELECT 
        channel,
        count(*) as touches
    FROM `nexus-analyst-demo.acme.fact_marketing_touches`
    WHERE touched_at >= '2025-04-01'
    GROUP BY 1;
-- 2025-04-15 13:20:45 | user=rajiv.menon@acme.io | job_dbt_run_health | 10737418240 | 8800 | SUCCESS | 
    -- Running the account_health model logic.
    -- Signal: utilization_band = active_users_28d / seat_count_licensed.
    -- Signal: health status rules (uncollectible, P1s, NPS).
    SELECT 
        customer_id,
        CASE 
            WHEN account_tier = 'Enterprise' THEN 
                CASE WHEN has_uncollectible_recent THEN 'critical' ELSE 'stable' END
            ELSE 
                CASE 
                    WHEN has_uncollectible_recent OR utilization_band < 0.20 THEN 'critical'
                    WHEN has_open_p1_over_48h OR has_recent_nps_detractor THEN 'at_risk'
                    WHEN is_engaged AND utilization_band >= 0.6 THEN 'healthy_expansion'
                    WHEN NOT is_engaged THEN 'monitoring'
                    ELSE 'stable'
                END
        END as health_status
    FROM `nexus-analyst-demo.acme.account_health`;
-- 2025-04-20 09:44:00 | user=lina.cho@acme.io | job_vrs_attempt | 0 | 250 | FAILURE | 
    -- Lina: "Rajiv, I'm trying to find the VRS score columns you mentioned but I get errors."
    -- Signal: VRS is a PARKED draft, columns don't exist.
    SELECT customer_id, vrs_band, champion_login_recency 
    FROM `nexus-analyst-demo.acme.account_health`; -- ERROR: Name vrs_band not found in account_health
-- 2025-04-22 11:00:15 | user=david.kim@acme.io | job_check_runs_spike | 21474836480 | 14500 | SUCCESS | 
    -- Investigating run spike for cust_000711 (Ember Industries)
    SELECT 
        date(triggered_at) as day,
        count(*) as n_runs
    FROM `nexus-analyst-demo.acme.fact_workflow_runs`
    WHERE customer_id = 'cust_000711'
      AND triggered_at >= '2025-04-01'
    GROUP BY 1;
-- 2025-04-28 15:30:22 | user=jorge.martinez@acme.io | job_sdr_touches | 5368709120 | 4100 | SUCCESS | 
    SELECT 
        sdr_employee_id,
        count(opportunity_id) as opps_created
    FROM `nexus-analyst-demo.acme.fact_opportunities`
    WHERE created_date >= '2025-04-01'
    GROUP BY 1;
-- 2025-05-01 08:00:00 | user=rajiv.menon@acme.io | job_dbt_refresh_all | 107374182400 | 95000 | SUCCESS | 
    -- Full refresh for the start of the month.
-- 2025-05-04 10:12:33 | user=nina.patel@acme.io | job_nps_survey_analysis | 1073741824 | 1200 | SUCCESS | 
    -- Looking at Q1 NPS results
    SELECT 
        score,
        segment,
        comment
    FROM `nexus-analyst-demo.acme.fact_nps_responses`
    WHERE survey_quarter = '2025-Q1';
-- 2025-05-10 14:45:19 | user=lina.cho@acme.io | job_expansion_mrr | 5368709120 | 4800 | SUCCESS | 
    -- Checking expansion MRR for the Q2 forecast update.
    SELECT 
        SUM(mrr_usd - COALESCE(prev_mrr, 0)) as expansion_mrr
    FROM (
        SELECT 
            mrr_usd,
            LAG(mrr_usd) OVER (PARTITION BY customer_id ORDER BY start_date) as prev_mrr,
            change_type
        FROM `nexus-analyst-demo.acme.fact_subscriptions`
    )
    WHERE change_type = 'expansion' AND mrr_usd > prev_mrr;
-- 2025-05-15 11:22:10 | user=david.kim@acme.io | job_billing_lag_check | 2147483648 | 1500 | SUCCESS | 
    -- Checking if BI lags prod by more than 2h
    SELECT 
        max(triggered_at) as latest_run_in_bq,
        CURRENT_TIMESTAMP() as current_time,
        TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), max(triggered_at), MINUTE) as lag_minutes
    FROM `nexus-analyst-demo.acme.fact_workflow_runs`;
-- 2025-05-20 16:00:45 | user=jasmine.park@acme.io | job_referral_check | 1073741824 | 900 | SUCCESS | 
    -- How is Tamarind Group doing? Sarah Chen's referral.
    -- Signal: cust_000706 Tamarind Group.
    SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE customer_id = 'cust_000706';
-- 2025-05-25 09:12:12 | user=rajiv.menon@acme.io | job_fix_nina_again | 0 | 100 | SUCCESS | 
    -- Nina, stop querying acme.marts.dbt_workflow_stats. 
    -- It is acme.workflow_runs_daily.
    SELECT * FROM `nexus-analyst-demo.acme.workflow_runs_daily` LIMIT 10;
-- 2025-06-01 10:30:00 | user=lina.cho@acme.io | job_arr_mid_year | 536870912 | 750 | SUCCESS | 
    -- Board deck ARR. Signal: Should be hitting ~$37M-38M as we approach Q3.
    SELECT 
        snapshot_date,
        arr_usd
    FROM `nexus-analyst-demo.acme.arr_snapshot`
    WHERE snapshot_date = '2025-05-31';
-- 2025-06-05 14:15:33 | user=nina.patel@acme.io | job_user_roles | 5368709120 | 3900 | SUCCESS | 
    -- Count of users by role for Drag Industries (cust_000412)
    SELECT 
        role,
        count(*) as user_count
    FROM `nexus-analyst-demo.acme.dim_users`
    WHERE customer_id = 'cust_000412'
    GROUP BY 1;
-- 2025-06-10 11:44:19 | user=jorge.martinez@acme.io | job_loss_reasons | 1073741824 | 1100 | SUCCESS | 
    -- Why did we lose deals in Q2?
    SELECT 
        loss_reason,
        count(*) as count
    FROM `nexus-analyst-demo.acme.fact_opportunities`
    WHERE stage = 'Closed Lost'
      AND close_date >= '2025-04-01'
    GROUP BY 1;
-- 2025-06-15 09:22:12 | user=david.kim@acme.io | job_integration_errors | 10737418240 | 8500 | SUCCESS | 
    -- Monitoring INTEGRATION_DOWN errors
    SELECT 
        date(triggered_at) as day,
        count(*) as integration_failures
    FROM `nexus-analyst-demo.acme.fact_workflow_runs`
    WHERE error_code = 'INTEGRATION_DOWN'
    GROUP BY 1
    ORDER BY 1 DESC;
-- 2025-06-20 13:00:45 | user=lina.cho@acme.io | job_nrr_q2_draft | 8589934592 | 6500 | SUCCESS | 
    -- NRR draft for Q2. 
    -- Signal: NRR ~1.07. 
    SELECT 
        nrr, 
        grr 
    FROM `nexus-analyst-demo.acme.nrr_trailing_12` 
    ORDER BY 1 DESC LIMIT 1;
-- 2025-06-25 15:55:00 | user=rajiv.menon@acme.io | job_cleanup_q2 | 0 | 500 | SUCCESS | 
    -- Pre-Q3 cleanup.
-- 2025-06-30 17:00:22 | user=lina.cho@acme.io | job_arr_june_close | 536870912 | 800 | SUCCESS | 
    -- Final June ARR. 
    SELECT 
        SUM(mrr_usd) * 12 as arr_total
    FROM `nexus-analyst-demo.acme.fact_subscriptions`
    WHERE is_current = true AND plan_tier != 'Free';
-- 2025-07-01 09:00:00 | user=david.kim@acme.io | job_q3_init | 0 | 100 | SUCCESS | SELECT 'Happy July';

-- [REMAINDER OF 200+ QUERIES SIMULATED BELOW WITH VARYING COMPLEXITY AND NOISE]
-- 2025-01-04 10:15:22 | user=rajiv.menon@acme.io | job_bqa_102 | 450123 | 210 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.dim_plans`;
-- 2025-01-04 11:45:01 | user=nina.patel@acme.io | job_bqa_103 | 1024556 | 450 | SUCCESS | SELECT count(*) FROM `nexus-analyst-demo.acme.dim_users` WHERE is_active = true;
-- 2025-01-05 09:12:00 | user=lina.cho@acme.io | job_bqa_104 | 5567890 | 1200 | SUCCESS | SELECT customer_id, company_name FROM `nexus-analyst-demo.acme.dim_customers` WHERE country = 'Netherlands';
-- 2025-01-05 13:22:10 | user=jorge.martinez@acme.io | job_bqa_105 | 1200345 | 800 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.dim_employees` WHERE team = 'Sales';
-- 2025-01-06 08:30:15 | user=david.kim@acme.io | job_bqa_106 | 998234 | 300 | SUCCESS | SELECT min(triggered_at) FROM `nexus-analyst-demo.acme.fact_workflow_runs`;
-- 2025-01-06 14:12:45 | user=jasmine.park@acme.io | job_bqa_107 | 4456778 | 1500 | SUCCESS | SELECT utm_source, count(*) FROM `nexus-analyst-demo.acme.fact_marketing_touches` GROUP BY 1;
-- 2025-01-07 10:00:05 | user=rajiv.menon@acme.io | job_bqa_108 | 0 | 150 | SUCCESS | DESCRIBE `nexus-analyst-demo.acme.fact_subscriptions`;
-- 2025-01-08 16:33:12 | user=nina.patel@acme.io | job_bqa_109 | 7789012 | 3100 | SUCCESS | SELECT event_name, count(*) FROM `nexus-analyst-demo.acme.fact_user_events` GROUP BY 1;
-- 2025-01-09 11:22:33 | user=lina.cho@acme.io | job_bqa_110 | 2234567 | 900 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.dim_plans` WHERE plan_tier = 'Business';
-- 2025-01-10 14:45:10 | user=jorge.martinez@acme.io | job_bqa_111 | 9901234 | 4200 | SUCCESS | SELECT stage, sum(amount_usd) FROM `nexus-analyst-demo.acme.fact_opportunities` GROUP BY 1;
-- 2025-01-11 09:15:01 | user=david.kim@acme.io | job_bqa_112 | 11223344 | 5600 | SUCCESS | SELECT status, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` GROUP BY 1;
-- 2025-01-12 13:22:10 | user=jasmine.park@acme.io | job_bqa_113 | 4455667 | 1800 | SUCCESS | SELECT channel, sum(attributed_revenue_usd) FROM `nexus-analyst-demo.acme.fact_marketing_touches` GROUP BY 1;
-- 2025-01-13 10:00:05 | user=rajiv.menon@acme.io | job_bqa_114 | 0 | 120 | SUCCESS | SELECT table_name FROM `nexus-analyst-demo.acme.INFORMATION_SCHEMA.TABLES`;
-- 2025-01-14 16:33:12 | user=nina.patel@acme.io | job_bqa_115 | 8899001 | 3500 | SUCCESS | SELECT customer_id, count(run_id) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE status = 'ERROR' GROUP BY 1;
-- 2025-01-15 11:22:33 | user=lina.cho@acme.io | job_bqa_116 | 3344556 | 1100 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE current_plan_tier = 'Enterprise';
-- 2025-01-16 14:45:10 | user=jorge.martinez@acme.io | job_bqa_117 | 1122334 | 950 | SUCCESS | SELECT e.full_name, count(o.opportunity_id) FROM `nexus-analyst-demo.acme.dim_employees` e JOIN `nexus-analyst-demo.acme.fact_opportunities` o ON e.employee_id = o.ae_employee_id GROUP BY 1;
-- 2025-01-17 09:15:01 | user=david.kim@acme.io | job_bqa_118 | 9988776 | 4800 | SUCCESS | SELECT triggered_by, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` GROUP BY 1;
-- 2025-01-18 13:22:10 | user=jasmine.park@acme.io | job_bqa_119 | 2233445 | 1300 | SUCCESS | SELECT utm_medium, count(*) FROM `nexus-analyst-demo.acme.fact_marketing_touches` GROUP BY 1;
-- 2025-01-19 10:00:05 | user=rajiv.menon@acme.io | job_bqa_120 | 0 | 150 | SUCCESS | SELECT column_name FROM `nexus-analyst-demo.acme.INFORMATION_SCHEMA.COLUMNS` WHERE table_name = 'dim_customers';
-- 2025-01-20 16:33:12 | user=nina.patel@acme.io | job_bqa_121 | 5566778 | 2900 | SUCCESS | SELECT customer_id, avg(duration_ms) FROM `nexus-analyst-demo.acme.fact_workflow_runs` GROUP BY 1;
-- 2025-01-21 11:22:33 | user=lina.cho@acme.io | job_bqa_122 | 1122334 | 850 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.fact_invoices` WHERE status = 'unpaid';
-- 2025-01-22 14:45:10 | user=jorge.martinez@acme.io | job_bqa_123 | 8899001 | 3800 | SUCCESS | SELECT account_tier, count(*) FROM `nexus-analyst-demo.acme.dim_customers` GROUP BY 1;
-- 2025-01-23 09:15:01 | user=david.kim@acme.io | job_bqa_124 | 4455667 | 2100 | SUCCESS | SELECT error_code, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE error_code IS NOT NULL GROUP BY 1;
-- 2025-01-24 13:22:10 | user=jasmine.park@acme.io | job_bqa_125 | 2233445 | 1200 | SUCCESS | SELECT campaign, sum(attributed_revenue_usd) FROM `nexus-analyst-demo.acme.fact_marketing_touches` GROUP BY 1;
-- 2025-01-25 10:00:05 | user=rajiv.menon@acme.io | job_bqa_126 | 0 | 180 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.dim_dates` LIMIT 10;
-- 2025-01-26 16:33:12 | user=nina.patel@acme.io | job_bqa_127 | 9988776 | 4500 | SUCCESS | SELECT role, count(*) FROM `nexus-analyst-demo.acme.dim_users` GROUP BY 1;
-- 2025-01-27 11:22:33 | user=lina.cho@acme.io | job_bqa_128 | 3344556 | 1400 | SUCCESS | SELECT customer_id, mrr_usd FROM `nexus-analyst-demo.acme.fact_subscriptions` WHERE is_current = true;
-- 2025-01-28 14:45:10 | user=jorge.martinez@acme.io | job_bqa_129 | 1122334 | 900 | SUCCESS | SELECT region, count(*) FROM `nexus-analyst-demo.acme.dim_customers` GROUP BY 1;
-- 2025-01-29 09:15:01 | user=david.kim@acme.io | job_bqa_130 | 5566778 | 2800 | SUCCESS | SELECT status, avg(step_count) FROM `nexus-analyst-demo.acme.fact_workflow_runs` GROUP BY 1;
-- 2025-01-30 13:22:10 | user=jasmine.park@acme.io | job_bqa_131 | 7789012 | 3300 | SUCCESS | SELECT utm_source, utm_medium, count(*) FROM `nexus-analyst-demo.acme.fact_marketing_touches` GROUP BY 1, 2;
-- 2025-01-31 10:00:05 | user=rajiv.menon@acme.io | job_bqa_132 | 0 | 140 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.INFORMATION_SCHEMA.TABLES` WHERE dataset_id = 'acme';
-- 2025-02-01 16:33:12 | user=nina.patel@acme.io | job_bqa_133 | 1122334 | 950 | SUCCESS | SELECT customer_id, count(*) FROM `nexus-analyst-demo.acme.fact_support_tickets` GROUP BY 1;
-- 2025-02-02 11:22:33 | user=lina.cho@acme.io | job_bqa_134 | 8899001 | 3700 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.fact_invoices` WHERE paid_at IS NULL;
-- 2025-02-03 14:45:10 | user=jorge.martinez@acme.io | job_bqa_135 | 4455667 | 2000 | SUCCESS | SELECT industry, sum(current_mrr_usd) FROM `nexus-analyst-demo.acme.dim_customers` GROUP BY 1;
-- 2025-02-04 09:15:01 | user=david.kim@acme.io | job_bqa_136 | 2233445 | 1300 | SUCCESS | SELECT error_code, avg(duration_ms) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE error_code IS NOT NULL GROUP BY 1;
-- 2025-02-05 13:22:10 | user=jasmine.park@acme.io | job_bqa_137 | 9988776 | 4600 | SUCCESS | SELECT first_touch_channel, count(*) FROM `nexus-analyst-demo.acme.bookings_attribution` GROUP BY 1;
-- 2025-02-06 10:00:05 | user=rajiv.menon@acme.io | job_bqa_138 | 0 | 160 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.dim_employees` LIMIT 5;
-- 2025-02-07 16:33:12 | user=nina.patel@acme.io | job_bqa_139 | 3344556 | 1500 | SUCCESS | SELECT customer_id, count(distinct user_id) FROM `nexus-analyst-demo.acme.fact_user_events` GROUP BY 1;
-- 2025-02-08 11:22:33 | user=lina.cho@acme.io | job_bqa_140 | 1122334 | 800 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.dim_plans`;
-- 2025-02-09 14:45:10 | user=jorge.martinez@acme.io | job_bqa_141 | 5566778 | 2700 | SUCCESS | SELECT ae_employee_id, count(*) FROM `nexus-analyst-demo.acme.fact_opportunities` WHERE stage = 'Discovery' GROUP BY 1;
-- 2025-02-10 09:15:01 | user=david.kim@acme.io | job_bqa_142 | 7789012 | 3400 | SUCCESS | SELECT status, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE triggered_at >= '2025-02-01' GROUP BY 1;
-- 2025-02-11 13:22:10 | user=jasmine.park@acme.io | job_bqa_143 | 1122334 | 920 | SUCCESS | SELECT utm_campaign, count(*) FROM `nexus-analyst-demo.acme.fact_marketing_touches` GROUP BY 1;
-- 2025-02-12 10:00:05 | user=rajiv.menon@acme.io | job_bqa_144 | 0 | 130 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.dim_dates` WHERE is_weekend = true;
-- 2025-02-13 16:33:12 | user=nina.patel@acme.io | job_bqa_145 | 8899001 | 3600 | SUCCESS | SELECT customer_id, avg(score) FROM `nexus-analyst-demo.acme.fact_nps_responses` GROUP BY 1;
-- 2025-02-14 11:22:33 | user=lina.cho@acme.io | job_bqa_146 | 4455667 | 1900 | SUCCESS | SELECT plan_tier, count(*) FROM `nexus-analyst-demo.acme.fact_subscriptions` WHERE is_current = true GROUP BY 1;
-- 2025-02-15 14:45:10 | user=jorge.martinez@acme.io | job_bqa_147 | 2233445 | 1100 | SUCCESS | SELECT e.location, count(c.customer_id) FROM `nexus-analyst-demo.acme.dim_employees` e JOIN `nexus-analyst-demo.acme.dim_customers` c ON e.employee_id = c.csm_employee_id GROUP BY 1;
-- 2025-02-16 09:15:01 | user=david.kim@acme.io | job_bqa_148 | 9988776 | 4700 | SUCCESS | SELECT triggered_by, status, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` GROUP BY 1, 2;
-- 2025-02-17 13:22:10 | user=jasmine.park@acme.io | job_bqa_149 | 3344556 | 1600 | SUCCESS | SELECT channel, count(*) FROM `nexus-analyst-demo.acme.fact_marketing_touches` WHERE touched_at >= '2025-02-01' GROUP BY 1;
-- 2025-02-18 10:00:05 | user=rajiv.menon@acme.io | job_bqa_150 | 0 | 170 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.INFORMATION_SCHEMA.COLUMNS` WHERE table_name = 'dim_users';
-- 2025-02-19 16:33:12 | user=nina.patel@acme.io | job_bqa_151 | 1122334 | 880 | SUCCESS | SELECT customer_id, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE status = 'SUCCESS' GROUP BY 1;
-- 2025-02-20 11:22:33 | user=lina.cho@acme.io | job_bqa_152 | 5566778 | 2600 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE status = 'churned';
-- 2025-02-21 14:45:10 | user=jorge.martinez@acme.io | job_bqa_153 | 7789012 | 3500 | SUCCESS | SELECT account_tier, avg(current_mrr_usd) FROM `nexus-analyst-demo.acme.dim_customers` GROUP BY 1;
-- 2025-02-22 09:15:01 | user=david.kim@acme.io | job_bqa_154 | 1122334 | 930 | SUCCESS | SELECT error_code, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE error_code = 'AUTH_FAILED' GROUP BY 1;
-- 2025-02-23 13:22:10 | user=jasmine.park@acme.io | job_bqa_155 | 8899001 | 3900 | SUCCESS | SELECT utm_source, sum(attributed_revenue_usd) FROM `nexus-analyst-demo.acme.fact_marketing_touches` GROUP BY 1;
-- 2025-02-24 10:00:05 | user=rajiv.menon@acme.io | job_bqa_156 | 0 | 140 | SUCCESS | SELECT table_name FROM `nexus-analyst-demo.acme.INFORMATION_SCHEMA.TABLES` WHERE table_schema = 'acme';
-- 2025-02-25 16:33:12 | user=nina.patel@acme.io | job_bqa_157 | 4455667 | 2200 | SUCCESS | SELECT customer_id, count(*) FROM `nexus-analyst-demo.acme.fact_support_tickets` WHERE priority = 'P1' GROUP BY 1;
-- 2025-02-26 11:22:33 | user=lina.cho@acme.io | job_bqa_158 | 2233445 | 1150 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.fact_subscriptions` WHERE plan_tier = 'Pro';
-- 2025-02-27 14:45:10 | user=jorge.martinez@acme.io | job_bqa_159 | 9988776 | 4400 | SUCCESS | SELECT ae_employee_id, sum(amount_usd) FROM `nexus-analyst-demo.acme.fact_opportunities` WHERE stage = 'Closed Won' GROUP BY 1;
-- 2025-02-28 09:15:01 | user=david.kim@acme.io | job_bqa_160 | 3344556 | 1550 | SUCCESS | SELECT status, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE triggered_at >= '2025-02-20' GROUP BY 1;
-- 2025-03-01 13:22:10 | user=jasmine.park@acme.io | job_bqa_161 | 1122334 | 910 | SUCCESS | SELECT channel, count(*) FROM `nexus-analyst-demo.acme.fact_marketing_touches` GROUP BY 1;
-- 2025-03-02 10:00:05 | user=rajiv.menon@acme.io | job_bqa_162 | 0 | 120 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.dim_plans`;
-- 2025-03-03 16:33:12 | user=nina.patel@acme.io | job_bqa_163 | 5566778 | 2500 | SUCCESS | SELECT customer_id, avg(duration_ms) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE status = 'SUCCESS' GROUP BY 1;
-- 2025-03-04 11:22:33 | user=lina.cho@acme.io | job_bqa_164 | 7789012 | 3450 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.fact_invoices` WHERE status = 'paid' AND paid_at >= '2025-03-01';
-- 2025-03-05 14:45:10 | user=jorge.martinez@acme.io | job_bqa_165 | 1122334 | 870 | SUCCESS | SELECT region, sum(current_mrr_usd) FROM `nexus-analyst-demo.acme.dim_customers` GROUP BY 1;
-- 2025-03-06 09:15:01 | user=david.kim@acme.io | job_bqa_166 | 8899001 | 3850 | SUCCESS | SELECT error_code, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` GROUP BY 1;
-- 2025-03-07 13:22:10 | user=jasmine.park@acme.io | job_bqa_167 | 4455667 | 2150 | SUCCESS | SELECT first_touch_channel, sum(bookings_acv_usd) FROM `nexus-analyst-demo.acme.bookings_attribution` GROUP BY 1;
-- 2025-03-08 10:00:05 | user=rajiv.menon@acme.io | job_bqa_168 | 0 | 160 | SUCCESS | DESCRIBE `nexus-analyst-demo.acme.dim_users`;
-- 2025-03-09 16:33:12 | user=nina.patel@acme.io | job_bqa_169 | 2233445 | 1250 | SUCCESS | SELECT customer_id, count(distinct user_id) FROM `nexus-analyst-demo.acme.dim_users` WHERE is_active = true GROUP BY 1;
-- 2025-03-10 11:22:33 | user=lina.cho@acme.io | job_bqa_170 | 9988776 | 4650 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.arr_snapshot` WHERE snapshot_date = '2025-03-01';
-- 2025-03-11 14:45:10 | user=jorge.martinez@acme.io | job_bqa_171 | 3344556 | 1650 | SUCCESS | SELECT ae_employee_id, count(*) FROM `nexus-analyst-demo.acme.fact_opportunities` WHERE stage = 'Negotiation' GROUP BY 1;
-- 2025-03-12 09:15:01 | user=david.kim@acme.io | job_bqa_172 | 1122334 | 890 | SUCCESS | SELECT status, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE triggered_at >= '2025-03-01' GROUP BY 1;
-- 2025-03-13 13:22:10 | user=jasmine.park@acme.io | job_bqa_173 | 5566778 | 2750 | SUCCESS | SELECT utm_source, count(*) FROM `nexus-analyst-demo.acme.fact_marketing_touches` WHERE touched_at >= '2025-03-01' GROUP BY 1;
-- 2025-03-14 10:00:05 | user=rajiv.menon@acme.io | job_bqa_174 | 0 | 140 | SUCCESS | SELECT column_name FROM `nexus-analyst-demo.acme.INFORMATION_SCHEMA.COLUMNS` WHERE table_name = 'fact_workflow_runs';
-- 2025-03-15 16:33:12 | user=nina.patel@acme.io | job_bqa_175 | 7789012 | 3550 | SUCCESS | SELECT customer_id, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE error_code = 'RATE_LIMITED' GROUP BY 1;
-- 2025-03-16 11:22:33 | user=lina.cho@acme.io | job_bqa_176 | 1122334 | 940 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE account_tier = 'MM';
-- 2025-03-17 14:45:10 | user=jorge.martinez@acme.io | job_bqa_177 | 8899001 | 3750 | SUCCESS | SELECT industry, count(*) FROM `nexus-analyst-demo.acme.dim_customers` GROUP BY 1;
-- 2025-03-18 09:15:01 | user=david.kim@acme.io | job_bqa_178 | 4455667 | 2050 | SUCCESS | SELECT step_count, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` GROUP BY 1;
-- 2025-03-19 13:22:10 | user=jasmine.park@acme.io | job_bqa_179 | 2233445 | 1180 | SUCCESS | SELECT channel, sum(attributed_revenue_usd) FROM `nexus-analyst-demo.acme.fact_marketing_touches` WHERE touched_at >= '2025-03-01' GROUP BY 1;
-- 2025-03-20 10:00:05 | user=rajiv.menon@acme.io | job_bqa_180 | 0 | 170 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.dim_employees` WHERE is_active = true;
-- 2025-03-21 16:33:12 | user=nina.patel@acme.io | job_bqa_181 | 9988776 | 4550 | SUCCESS | SELECT customer_id, avg(score) FROM `nexus-analyst-demo.acme.fact_nps_responses` WHERE segment = 'Enterprise' GROUP BY 1;
-- 2025-03-22 11:22:33 | user=lina.cho@acme.io | job_bqa_182 | 3344556 | 1450 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.nrr_trailing_12` LIMIT 5;
-- 2025-03-23 14:45:10 | user=jorge.martinez@acme.io | job_bqa_183 | 1122334 | 860 | SUCCESS | SELECT e.full_name, sum(o.amount_usd) FROM `nexus-analyst-demo.acme.dim_employees` e JOIN `nexus-analyst-demo.acme.fact_opportunities` o ON e.employee_id = o.ae_employee_id WHERE o.stage = 'Closed Won' GROUP BY 1;
-- 2025-03-24 09:15:01 | user=david.kim@acme.io | job_bqa_184 | 5566778 | 2650 | SUCCESS | SELECT status, avg(duration_ms) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE triggered_at >= '2025-03-15' GROUP BY 1;
-- 2025-03-25 13:22:10 | user=jasmine.park@acme.io | job_bqa_185 | 7789012 | 3650 | SUCCESS | SELECT utm_source, utm_medium, count(*) FROM `nexus-analyst-demo.acme.fact_marketing_touches` GROUP BY 1, 2;
-- 2025-03-26 10:00:05 | user=rajiv.menon@acme.io | job_bqa_186 | 0 | 130 | SUCCESS | SELECT table_name FROM `nexus-analyst-demo.acme.INFORMATION_SCHEMA.TABLES` WHERE table_type = 'BASE TABLE';
-- 2025-03-27 16:33:12 | user=nina.patel@acme.io | job_bqa_187 | 1122334 | 970 | SUCCESS | SELECT customer_id, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE error_code = 'STEP_TIMEOUT' GROUP BY 1;
-- 2025-03-28 11:22:33 | user=lina.cho@acme.io | job_bqa_188 | 8899001 | 3850 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE acquisition_channel = 'outbound';
-- 2025-03-29 14:45:10 | user=jorge.martinez@acme.io | job_bqa_189 | 4455667 | 1950 | SUCCESS | SELECT csm_employee_id, count(*) FROM `nexus-analyst-demo.acme.dim_customers` WHERE status = 'active' GROUP BY 1;
-- 2025-03-30 09:15:01 | user=david.kim@acme.io | job_bqa_190 | 2233445 | 1250 | SUCCESS | SELECT triggered_by, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE status = 'SUCCESS' GROUP BY 1;
-- 2025-03-31 13:22:10 | user=jasmine.park@acme.io | job_bqa_191 | 9988776 | 4750 | SUCCESS | SELECT campaign, count(*) FROM `nexus-analyst-demo.acme.fact_marketing_touches` WHERE touched_at >= '2025-03-01' GROUP BY 1;
-- 2025-04-01 10:00:05 | user=rajiv.menon@acme.io | job_bqa_192 | 0 | 150 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.dim_plans`;
-- 2025-04-02 16:33:12 | user=nina.patel@acme.io | job_bqa_193 | 3344556 | 1650 | SUCCESS | SELECT customer_id, count(distinct user_id) FROM `nexus-analyst-demo.acme.fact_user_events` WHERE event_at >= '2025-04-01' GROUP BY 1;
-- 2025-04-03 11:22:33 | user=lina.cho@acme.io | job_bqa_194 | 1122334 | 920 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.account_health` WHERE account_health_status = 'critical';
-- 2025-04-04 14:45:10 | user=jorge.martinez@acme.io | job_bqa_195 | 5566778 | 2850 | SUCCESS | SELECT region, avg(current_mrr_usd) FROM `nexus-analyst-demo.acme.dim_customers` WHERE status = 'active' GROUP BY 1;
-- 2025-04-05 09:15:01 | user=david.kim@acme.io | job_bqa_196 | 7789012 | 3750 | SUCCESS | SELECT status, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE triggered_at >= '2025-04-01' GROUP BY 1;
-- 2025-04-06 13:22:10 | user=jasmine.park@acme.io | job_bqa_197 | 1122334 | 850 | SUCCESS | SELECT utm_source, count(*) FROM `nexus-analyst-demo.acme.fact_marketing_touches` WHERE touched_at >= '2025-04-01' GROUP BY 1;
-- 2025-04-07 10:00:05 | user=rajiv.menon@acme.io | job_bqa_198 | 0 | 140 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.dim_employees` WHERE team = 'CS';
-- 2025-04-08 16:33:12 | user=nina.patel@acme.io | job_bqa_199 | 8899001 | 3950 | SUCCESS | SELECT customer_id, count(*) FROM `nexus-analyst-demo.acme.fact_support_tickets` WHERE status = 'open' GROUP BY 1;
-- 2025-04-09 11:22:33 | user=lina.cho@acme.io | job_bqa_200 | 4455667 | 2250 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.fact_subscriptions` WHERE is_current = true AND plan_tier = 'Enterprise';
-- 2025-04-10 14:45:10 | user=jorge.martinez@acme.io | job_bqa_201 | 2233445 | 1120 | SUCCESS | SELECT ae_employee_id, count(*) FROM `nexus-analyst-demo.acme.fact_opportunities` WHERE stage = 'Discovery' AND created_date >= '2025-04-01' GROUP BY 1;
-- 2025-04-11 09:15:01 | user=david.kim@acme.io | job_bqa_202 | 9988776 | 4850 | SUCCESS | SELECT error_code, avg(duration_ms) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE triggered_at >= '2025-04-01' GROUP BY 1;
-- 2025-04-12 13:22:10 | user=jasmine.park@acme.io | job_bqa_203 | 3344556 | 1520 | SUCCESS | SELECT utm_medium, count(*) FROM `nexus-analyst-demo.acme.fact_marketing_touches` WHERE touched_at >= '2025-04-01' GROUP BY 1;
-- 2025-04-13 10:00:05 | user=rajiv.menon@acme.io | job_bqa_204 | 0 | 160 | SUCCESS | SELECT column_name FROM `nexus-analyst-demo.acme.INFORMATION_SCHEMA.COLUMNS` WHERE table_name = 'dim_customers';
-- 2025-04-14 16:33:12 | user=nina.patel@acme.io | job_bqa_205 | 1122334 | 980 | SUCCESS | SELECT customer_id, avg(duration_ms) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE status = 'ERROR' GROUP BY 1;
-- 2025-04-15 11:22:33 | user=lina.cho@acme.io | job_bqa_206 | 5566778 | 2720 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE country = 'United Kingdom';
-- 2025-04-16 14:45:10 | user=jorge.martinez@acme.io | job_bqa_207 | 7789012 | 3620 | SUCCESS | SELECT sdr_employee_id, count(*) FROM `nexus-analyst-demo.acme.fact_opportunities` WHERE created_date >= '2025-04-01' GROUP BY 1;
-- 2025-04-17 09:15:01 | user=david.kim@acme.io | job_bqa_208 | 1122334 | 950 | SUCCESS | SELECT triggered_by, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE triggered_at >= '2025-04-10' GROUP BY 1;
-- 2025-04-18 13:22:10 | user=jasmine.park@acme.io | job_bqa_209 | 8899001 | 3820 | SUCCESS | SELECT utm_source, sum(attributed_revenue_usd) FROM `nexus-analyst-demo.acme.fact_marketing_touches` WHERE touched_at >= '2025-04-01' GROUP BY 1;
-- 2025-04-19 10:00:05 | user=rajiv.menon@acme.io | job_bqa_210 | 0 | 130 | SUCCESS | SELECT table_name FROM `nexus-analyst-demo.acme.INFORMATION_SCHEMA.TABLES` WHERE table_schema = 'acme';
-- 2025-04-20 16:33:12 | user=nina.patel@acme.io | job_bqa_211 | 4455667 | 2120 | SUCCESS | SELECT customer_id, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE error_code = 'NULL_PAYLOAD' GROUP BY 1;
-- 2025-04-21 11:22:33 | user=lina.cho@acme.io | job_bqa_212 | 2233445 | 1220 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.dim_plans` WHERE monthly_price_per_seat_usd > 50;
-- 2025-04-22 14:45:10 | user=jorge.martinez@acme.io | job_bqa_213 | 9988776 | 4520 | SUCCESS | SELECT industry, count(*) FROM `nexus-analyst-demo.acme.dim_customers` WHERE status = 'active' GROUP BY 1;
-- 2025-04-23 09:15:01 | user=david.kim@acme.io | job_bqa_214 | 3344556 | 1620 | SUCCESS | SELECT status, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE triggered_at >= '2025-04-20' GROUP BY 1;
-- 2025-04-24 13:22:10 | user=jasmine.park@acme.io | job_bqa_215 | 1122334 | 960 | SUCCESS | SELECT channel, count(*) FROM `nexus-analyst-demo.acme.fact_marketing_touches` GROUP BY 1;
-- 2025-04-25 10:00:05 | user=rajiv.menon@acme.io | job_bqa_216 | 0 | 180 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.dim_dates` WHERE month = 4;
-- 2025-04-26 16:33:12 | user=nina.patel@acme.io | job_bqa_217 | 5566778 | 2720 | SUCCESS | SELECT customer_id, count(distinct user_id) FROM `nexus-analyst-demo.acme.dim_users` WHERE last_login_date >= '2025-04-01' GROUP BY 1;
-- 2025-04-27 11:22:33 | user=lina.cho@acme.io | job_bqa_218 | 7789012 | 3420 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.arr_snapshot` WHERE snapshot_date >= '2025-04-01';
-- 2025-04-28 14:45:10 | user=jorge.martinez@acme.io | job_bqa_219 | 1122334 | 880 | SUCCESS | SELECT e.full_name, count(o.opportunity_id) FROM `nexus-analyst-demo.acme.dim_employees` e JOIN `nexus-analyst-demo.acme.fact_opportunities` o ON e.employee_id = o.ae_employee_id WHERE o.stage = 'Closed Won' GROUP BY 1;
-- 2025-04-29 09:15:01 | user=david.kim@acme.io | job_bqa_220 | 8899001 | 3720 | SUCCESS | SELECT error_code, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE triggered_at >= '2025-04-01' GROUP BY 1;
-- 2025-04-30 13:22:10 | user=jasmine.park@acme.io | job_bqa_221 | 4455667 | 2020 | SUCCESS | SELECT first_touch_channel, sum(bookings_acv_usd) FROM `nexus-analyst-demo.acme.bookings_attribution` WHERE closed_won_at >= '2025-04-01' GROUP BY 1;
-- 2025-05-01 10:00:05 | user=rajiv.menon@acme.io | job_bqa_222 | 0 | 120 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.dim_plans`;
-- 2025-05-02 16:33:12 | user=nina.patel@acme.io | job_bqa_223 | 2233445 | 1320 | SUCCESS | SELECT customer_id, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE status = 'SUCCESS' AND triggered_at >= '2025-05-01' GROUP BY 1;
-- 2025-05-03 11:22:33 | user=lina.cho@acme.io | job_bqa_224 | 9988776 | 4520 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.fact_invoices` WHERE status = 'overdue';
-- 2025-05-04 14:45:10 | user=jorge.martinez@acme.io | job_bqa_225 | 3344556 | 1520 | SUCCESS | SELECT account_tier, sum(current_mrr_usd) FROM `nexus-analyst-demo.acme.dim_customers` GROUP BY 1;
-- 2025-05-05 09:15:01 | user=david.kim@acme.io | job_bqa_226 | 1122334 | 920 | SUCCESS | SELECT status, avg(duration_ms) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE triggered_at >= '2025-05-01' GROUP BY 1;
-- 2025-05-06 13:22:10 | user=jasmine.park@acme.io | job_bqa_227 | 5566778 | 2620 | SUCCESS | SELECT utm_source, count(*) FROM `nexus-analyst-demo.acme.fact_marketing_touches` WHERE touched_at >= '2025-05-01' GROUP BY 1;
-- 2025-05-07 10:00:05 | user=rajiv.menon@acme.io | job_bqa_228 | 0 | 140 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.dim_employees` WHERE location = 'Amsterdam';
-- 2025-05-08 16:33:12 | user=nina.patel@acme.io | job_bqa_229 | 7789012 | 3420 | SUCCESS | SELECT customer_id, count(*) FROM `nexus-analyst-demo.acme.fact_support_tickets` WHERE closed_at IS NULL GROUP BY 1;
-- 2025-05-09 11:22:33 | user=lina.cho@acme.io | job_bqa_230 | 1122334 | 960 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE signup_date >= '2025-05-01';
-- 2025-05-10 14:45:10 | user=jorge.martinez@acme.io | job_bqa_231 | 8899001 | 3820 | SUCCESS | SELECT ae_employee_id, count(*) FROM `nexus-analyst-demo.acme.fact_opportunities` WHERE stage = 'Negotiation' AND close_date >= '2025-05-01' GROUP BY 1;
-- 2025-05-11 09:15:01 | user=david.kim@acme.io | job_bqa_232 | 4455667 | 2120 | SUCCESS | SELECT error_code, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE triggered_at >= '2025-05-01' GROUP BY 1;
-- 2025-05-12 13:22:10 | user=jasmine.park@acme.io | job_bqa_233 | 2233445 | 1220 | SUCCESS | SELECT channel, sum(attributed_revenue_usd) FROM `nexus-analyst-demo.acme.fact_marketing_touches` WHERE touched_at >= '2025-05-01' GROUP BY 1;
-- 2025-05-13 10:00:05 | user=rajiv.menon@acme.io | job_bqa_234 | 0 | 170 | SUCCESS | DESCRIBE `nexus-analyst-demo.acme.dim_users`;
-- 2025-05-14 16:33:12 | user=nina.patel@acme.io | job_bqa_235 | 9988776 | 4620 | SUCCESS | SELECT customer_id, avg(score) FROM `nexus-analyst-demo.acme.fact_nps_responses` WHERE segment = 'MM' GROUP BY 1;
-- 2025-05-15 11:22:33 | user=lina.cho@acme.io | job_bqa_236 | 3344556 | 1520 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.arr_snapshot` WHERE snapshot_date = '2025-05-15';
-- 2025-05-16 14:45:10 | user=jorge.martinez@acme.io | job_bqa_237 | 1122334 | 920 | SUCCESS | SELECT region, count(*) FROM `nexus-analyst-demo.acme.dim_customers` WHERE status = 'active' GROUP BY 1;
-- 2025-05-17 09:15:01 | user=david.kim@acme.io | job_bqa_238 | 5566778 | 2720 | SUCCESS | SELECT triggered_by, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE status = 'ERROR' GROUP BY 1;
-- 2025-05-18 13:22:10 | user=jasmine.park@acme.io | job_bqa_239 | 7789012 | 3520 | SUCCESS | SELECT utm_source, count(*) FROM `nexus-analyst-demo.acme.fact_marketing_touches` GROUP BY 1;
-- 2025-05-19 10:00:05 | user=rajiv.menon@acme.io | job_bqa_240 | 0 | 130 | SUCCESS | SELECT table_name FROM `nexus-analyst-demo.acme.INFORMATION_SCHEMA.TABLES` WHERE table_schema = 'acme';
-- 2025-05-20 16:33:12 | user=nina.patel@acme.io | job_bqa_241 | 1122334 | 940 | SUCCESS | SELECT customer_id, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE error_code = 'INTEGRATION_DOWN' GROUP BY 1;
-- 2025-05-21 11:22:33 | user=lina.cho@acme.io | job_bqa_242 | 8899001 | 3820 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE account_tier = 'Ent';
-- 2025-05-22 14:45:10 | user=jorge.martinez@acme.io | job_bqa_243 | 4455667 | 2020 | SUCCESS | SELECT sdr_employee_id, sum(amount_usd) FROM `nexus-analyst-demo.acme.fact_opportunities` WHERE created_date >= '2025-05-01' GROUP BY 1;
-- 2025-05-23 09:15:01 | user=david.kim@acme.io | job_bqa_244 | 2233445 | 1220 | SUCCESS | SELECT status, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE triggered_at >= '2025-05-20' GROUP BY 1;
-- 2025-05-24 13:22:10 | user=jasmine.park@acme.io | job_bqa_245 | 9988776 | 4720 | SUCCESS | SELECT channel, count(*) FROM `nexus-analyst-demo.acme.fact_marketing_touches` WHERE touched_at >= '2025-05-01' GROUP BY 1;
-- 2025-05-25 10:00:05 | user=rajiv.menon@acme.io | job_bqa_246 | 0 | 150 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.dim_plans`;
-- 2025-05-26 16:33:12 | user=nina.patel@acme.io | job_bqa_247 | 3344556 | 1620 | SUCCESS | SELECT customer_id, count(distinct user_id) FROM `nexus-analyst-demo.acme.dim_users` WHERE last_login_date >= '2025-05-01' GROUP BY 1;
-- 2025-05-27 11:22:33 | user=lina.cho@acme.io | job_bqa_248 | 1122334 | 910 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.fact_subscriptions` WHERE is_current = true AND change_type = 'expansion';
-- 2025-05-28 14:45:10 | user=jorge.martinez@acme.io | job_bqa_249 | 5566778 | 2820 | SUCCESS | SELECT industry, avg(current_mrr_usd) FROM `nexus-analyst-demo.acme.dim_customers` WHERE status = 'active' GROUP BY 1;
-- 2025-05-29 09:15:01 | user=david.kim@acme.io | job_bqa_250 | 7789012 | 3620 | SUCCESS | SELECT error_code, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE triggered_at >= '2025-05-01' GROUP BY 1;
-- 2025-05-30 13:22:10 | user=jasmine.park@acme.io | job_bqa_251 | 1122334 | 860 | SUCCESS | SELECT utm_source, sum(attributed_revenue_usd) FROM `nexus-analyst-demo.acme.fact_marketing_touches` GROUP BY 1;
-- 2025-05-31 10:00:05 | user=rajiv.menon@acme.io | job_bqa_252 | 0 | 140 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.dim_dates` WHERE month = 5;
-- 2025-06-01 16:33:12 | user=nina.patel@acme.io | job_bqa_253 | 8899001 | 3820 | SUCCESS | SELECT customer_id, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE status = 'SUCCESS' AND triggered_at >= '2025-06-01' GROUP BY 1;
-- 2025-06-02 11:22:33 | user=lina.cho@acme.io | job_bqa_254 | 4455667 | 2120 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.arr_snapshot` WHERE snapshot_date = '2025-06-01';
-- 2025-06-03 14:45:10 | user=jorge.martinez@acme.io | job_bqa_255 | 2233445 | 1110 | SUCCESS | SELECT region, sum(current_mrr_usd) FROM `nexus-analyst-demo.acme.dim_customers` GROUP BY 1;
-- 2025-06-04 09:15:01 | user=david.kim@acme.io | job_bqa_256 | 9988776 | 4410 | SUCCESS | SELECT status, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE triggered_at >= '2025-06-01' GROUP BY 1;
-- 2025-06-05 13:22:10 | user=jasmine.park@acme.io | job_bqa_257 | 3344556 | 1610 | SUCCESS | SELECT utm_medium, count(*) FROM `nexus-analyst-demo.acme.fact_marketing_touches` WHERE touched_at >= '2025-06-01' GROUP BY 1;
-- 2025-06-06 10:00:05 | user=rajiv.menon@acme.io | job_bqa_258 | 0 | 160 | SUCCESS | DESCRIBE `nexus-analyst-demo.acme.dim_users`;
-- 2025-06-07 16:33:12 | user=nina.patel@acme.io | job_bqa_259 | 1122334 | 930 | SUCCESS | SELECT customer_id, avg(duration_ms) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE error_code IS NOT NULL GROUP BY 1;
-- 2025-06-08 11:22:33 | user=lina.cho@acme.io | job_bqa_260 | 5566778 | 2710 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.dim_customers` WHERE current_plan_tier = 'Business';
-- 2025-06-09 14:45:10 | user=jorge.martinez@acme.io | job_bqa_261 | 7789012 | 3410 | SUCCESS | SELECT ae_employee_id, count(*) FROM `nexus-analyst-demo.acme.fact_opportunities` WHERE stage = 'Closed Won' AND closed_won_at >= '2025-06-01' GROUP BY 1;
-- 2025-06-10 09:15:01 | user=david.kim@acme.io | job_bqa_262 | 1122334 | 880 | SUCCESS | SELECT error_code, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE triggered_at >= '2025-06-01' GROUP BY 1;
-- 2025-06-11 13:22:10 | user=jasmine.park@acme.io | job_bqa_263 | 8899001 | 3710 | SUCCESS | SELECT channel, sum(attributed_revenue_usd) FROM `nexus-analyst-demo.acme.fact_marketing_touches` WHERE touched_at >= '2025-06-01' GROUP BY 1;
-- 2025-06-12 10:00:05 | user=rajiv.menon@acme.io | job_bqa_264 | 0 | 130 | SUCCESS | SELECT column_name FROM `nexus-analyst-demo.acme.INFORMATION_SCHEMA.COLUMNS` WHERE table_name = 'dim_customers';
-- 2025-06-13 16:33:12 | user=nina.patel@acme.io | job_bqa_265 | 4455667 | 2110 | SUCCESS | SELECT customer_id, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE status = 'ERROR' AND triggered_at >= '2025-06-01' GROUP BY 1;
-- 2025-06-14 11:22:33 | user=lina.cho@acme.io | job_bqa_266 | 2233445 | 1210 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.dim_plans` WHERE monthly_price_per_seat_usd < 100;
-- 2025-06-15 14:45:10 | user=jorge.martinez@acme.io | job_bqa_267 | 9988776 | 4510 | SUCCESS | SELECT industry, count(*) FROM `nexus-analyst-demo.acme.dim_customers` WHERE signup_date >= '2025-01-01' GROUP BY 1;
-- 2025-06-16 09:15:01 | user=david.kim@acme.io | job_bqa_268 | 3344556 | 1610 | SUCCESS | SELECT status, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE triggered_at >= '2025-06-10' GROUP BY 1;
-- 2025-06-17 13:22:10 | user=jasmine.park@acme.io | job_bqa_269 | 1122334 | 950 | SUCCESS | SELECT utm_source, count(*) FROM `nexus-analyst-demo.acme.fact_marketing_touches` GROUP BY 1;
-- 2025-06-18 10:00:05 | user=rajiv.menon@acme.io | job_bqa_270 | 0 | 170 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.dim_employees` WHERE is_active = true;
-- 2025-06-19 16:33:12 | user=nina.patel@acme.io | job_bqa_271 | 5566778 | 2710 | SUCCESS | SELECT customer_id, count(distinct user_id) FROM `nexus-analyst-demo.acme.dim_users` WHERE is_active = true GROUP BY 1;
-- 2025-06-20 11:22:33 | user=lina.cho@acme.io | job_bqa_272 | 7789012 | 3410 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.nrr_trailing_12` LIMIT 1;
-- 2025-06-21 14:45:10 | user=jorge.martinez@acme.io | job_bqa_273 | 1122334 | 850 | SUCCESS | SELECT region, sum(current_mrr_usd) FROM `nexus-analyst-demo.acme.dim_customers` WHERE status = 'active' GROUP BY 1;
-- 2025-06-22 09:15:01 | user=david.kim@acme.io | job_bqa_274 | 8899001 | 3710 | SUCCESS | SELECT error_code, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE triggered_at >= '2025-06-15' GROUP BY 1;
-- 2025-06-23 13:22:10 | user=jasmine.park@acme.io | job_bqa_275 | 4455667 | 2010 | SUCCESS | SELECT channel, count(*) FROM `nexus-analyst-demo.acme.fact_marketing_touches` GROUP BY 1;
-- 2025-06-24 10:00:05 | user=rajiv.menon@acme.io | job_bqa_276 | 0 | 120 | SUCCESS | SELECT table_name FROM `nexus-analyst-demo.acme.INFORMATION_SCHEMA.TABLES`;
-- 2025-06-25 16:33:12 | user=nina.patel@acme.io | job_bqa_277 | 2233445 | 1310 | SUCCESS | SELECT customer_id, avg(duration_ms) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE status = 'SUCCESS' AND triggered_at >= '2025-06-01' GROUP BY 1;
-- 2025-06-26 11:22:33 | user=lina.cho@acme.io | job_bqa_278 | 9988776 | 4510 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.fact_invoices` WHERE paid_at >= '2025-06-01';
-- 2025-06-27 14:45:10 | user=jorge.martinez@acme.io | job_bqa_279 | 3344556 | 1510 | SUCCESS | SELECT ae_employee_id, sum(amount_usd) FROM `nexus-analyst-demo.acme.fact_opportunities` WHERE stage = 'Closed Won' GROUP BY 1;
-- 2025-06-28 09:15:01 | user=david.kim@acme.io | job_bqa_280 | 1122334 | 910 | SUCCESS | SELECT status, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE triggered_at >= '2025-06-25' GROUP BY 1;
-- 2025-06-29 13:22:10 | user=jasmine.park@acme.io | job_bqa_281 | 5566778 | 2610 | SUCCESS | SELECT first_touch_channel, count(*) FROM `nexus-analyst-demo.acme.bookings_attribution` GROUP BY 1;
-- 2025-06-30 10:00:05 | user=rajiv.menon@acme.io | job_bqa_282 | 0 | 140 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.dim_plans`;
-- 2025-06-30 16:33:12 | user=nina.patel@acme.io | job_bqa_283 | 7789012 | 3410 | SUCCESS | SELECT customer_id, count(*) FROM `nexus-analyst-demo.acme.fact_support_tickets` WHERE priority = 'P1' GROUP BY 1;
-- 2025-06-30 17:00:00 | user=lina.cho@acme.io | job_bqa_284 | 1122334 | 900 | SUCCESS | SELECT * FROM `nexus-analyst-demo.acme.arr_snapshot` WHERE snapshot_date = '2025-06-30';
-- 2025-06-30 17:30:00 | user=david.kim@acme.io | job_bqa_285 | 8899001 | 3710 | SUCCESS | SELECT status, count(*) FROM `nexus-analyst-demo.acme.fact_workflow_runs` WHERE triggered_at >= '2025-06-30' GROUP BY 1;