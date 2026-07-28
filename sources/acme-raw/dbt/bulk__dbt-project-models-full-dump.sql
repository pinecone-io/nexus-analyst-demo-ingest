---
title: "dbt project — full models export (all SQL)"
source_url: "internal://acme/dbt-project-models-full-dump"
license: "synthetic-demo"
attribution: "Synthetic content, Acme Inc internal demo. Acme Inc is a fictitious company."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: dbt_model
---

/*
========================================================================================
ACME INC — DBT PROJECT EXPORT (MODELS DUMP)
Date: 2026-05-04
Owner: Rajiv Menon (@rajiv.menon)
Note: This is a raw 'cat models/**/*.sql' dump for the annual data audit.

IMPORTANT ARCHITECTURE NOTE:
Despite the dbt folder structure (marts/finance, marts/cs, etc.), 
the BigQuery dataset is FLAT. 
All models materialize as `nexus-analyst-demo.acme.<model_name>`. 
Do NOT attempt to use nested dataset paths like `acme.marts_finance.arr_snapshot`.
It will fail. BQ dataset is NOT nested.
========================================================================================
*/

-- ####################################################################################
-- STAGING MODELS
-- ####################################################################################

-- models/staging/stg_customers.sql
-- Owner: nina.patel
-- Materialization: view

/* 
   Basic cleanup of raw customer data.
   Renaming csm_employee_id to csm_id for consistency across models.
*/

WITH raw_customers AS (
    SELECT * FROM {{ source('acme_raw', 'customers') }}
)

SELECT
    customer_id,
    company_name,
    signup_date,
    country,
    region,
    industry,
    account_tier,
    current_plan_tier,
    -- casting mrr to numeric for BigQuery precision
    CAST(current_mrr_usd AS NUMERIC) AS current_mrr_usd,
    seat_count_licensed,
    status,
    churn_date,
    csm_employee_id AS csm_id,
    ae_employee_id AS ae_id,
    acquisition_channel,
    -- helper flag for ARR logic later
    CASE WHEN status = 'active' AND current_plan_tier != 'Free' THEN TRUE ELSE FALSE END AS is_paying
FROM raw_customers

-- TODO: Rajiv, check if we need to filter out 'test' customers here or in a separate mart?
-- @nina: leave them for now, the 'is_test' flag isn't reliable in source yet.


-- models/staging/stg_subscriptions.sql
-- Owner: rajiv.menon

SELECT
    subscription_id,
    customer_id,
    plan_tier,
    CAST(start_date AS DATE) AS start_date,
    CAST(end_date AS DATE) AS end_date,
    CAST(mrr_usd AS NUMERIC) AS mrr_usd,
    seat_count,
    billing_cycle,
    is_current,
    change_type,
    changed_from_subscription_id
FROM {{ source('acme_raw', 'fact_subscriptions') }}
-- NOTE: all subscription data is historical; arr logic uses is_current filter.


-- models/staging/stg_invoices.sql
-- Owner: lina.cho

SELECT
    invoice_id,
    customer_id,
    subscription_id,
    CAST(invoice_date AS DATE) AS invoice_date,
    CAST(period_start AS DATE) AS period_start,
    CAST(period_end AS DATE) AS period_end,
    CAST(amount_usd AS NUMERIC) AS amount_usd,
    status,
    paid_at
FROM {{ source('acme_raw', 'fact_invoices') }}


-- models/staging/stg_workflow_runs.sql
-- Owner: david.kim

SELECT
    run_id,
    workflow_id,
    customer_id,
    triggered_at,
    triggered_by,
    status,
    duration_ms,
    step_count,
    error_code
FROM {{ source('acme_raw', 'fact_workflow_runs') }}


-- models/staging/stg_user_events.sql
-- Owner: rajiv.menon

SELECT
    event_id,
    user_id,
    customer_id,
    event_at,
    event_name,
    -- parsing json in staging to avoid downstream headache
    JSON_EXTRACT_SCALAR(properties_json, '$.page_url') AS page_url,
    JSON_EXTRACT_SCALAR(properties_json, '$.feature_id') AS feature_id,
    JSON_EXTRACT_SCALAR(properties_json, '$.session_id') AS session_id
FROM {{ source('acme_raw', 'fact_user_events') }}


-- models/staging/stg_support_tickets.sql
-- Owner: nina.patel

SELECT
    ticket_id,
    customer_id,
    user_id,
    opened_at,
    closed_at,
    channel,
    priority,
    category,
    resolution_time_hours,
    csat_score,
    assigned_to_employee_id AS assignee_id
FROM {{ source('acme_raw', 'fact_support_tickets') }}


-- models/staging/stg_opportunities.sql
-- Owner: jorge.martinez (RevOps)

SELECT
    opportunity_id,
    customer_id,
    account_name,
    ae_employee_id AS ae_id,
    sdr_employee_id AS sdr_id,
    CAST(created_date AS DATE) AS created_date,
    stage,
    CAST(amount_usd AS NUMERIC) AS amount_usd,
    CAST(close_date AS DATE) AS close_date,
    closed_won_at,
    loss_reason
FROM {{ source('acme_raw', 'fact_opportunities') }}


-- models/staging/stg_nps.sql
-- Owner: nina.patel

SELECT
    response_id,
    customer_id,
    user_id,
    responded_at,
    score,
    comment,
    segment,
    survey_quarter
FROM {{ source('acme_raw', 'fact_nps_responses') }}


-- models/staging/stg_marketing_touches.sql
-- Owner: rajiv.menon

SELECT
    touch_id,
    lead_email_hash,
    customer_id,
    touched_at,
    channel,
    campaign,
    utm_source,
    utm_medium,
    utm_campaign,
    CAST(attributed_revenue_usd AS NUMERIC) AS attributed_revenue_usd
FROM {{ source('acme_raw', 'fact_marketing_touches') }}


-- models/staging/stg_employees.sql
-- Owner: lina.cho

SELECT
    employee_id,
    full_name,
    team,
    role,
    manager_employee_id AS manager_id,
    hire_date,
    termination_date,
    location,
    is_active
FROM {{ source('acme_raw', 'dim_employees') }}


-- ####################################################################################
-- INTERMEDIATE MODELS
-- ####################################################################################

-- models/intermediate/int_subscription_changes.sql
-- Owner: rajiv.menon
-- Materialization: table

/* 
   Calculating deltas between consecutive subscriptions for a customer.
   Used for detecting Upgrades, Downgrades, Reactivations, and Churn.
*/

WITH sub_history AS (
    SELECT 
        customer_id,
        subscription_id,
        plan_tier,
        mrr_usd,
        start_date,
        end_date,
        LAG(plan_tier) OVER (PARTITION BY customer_id ORDER BY start_date) AS prev_plan,
        LAG(mrr_usd) OVER (PARTITION BY customer_id ORDER BY start_date) AS prev_mrr,
        LAG(end_date) OVER (PARTITION BY customer_id ORDER BY start_date) AS prev_end_date
    FROM {{ ref('stg_subscriptions') }}
)

SELECT 
    *,
    CASE 
        WHEN prev_plan IS NULL THEN 'NEW'
        WHEN prev_end_date < start_date THEN 'REACTIVATION'
        WHEN mrr_usd > prev_mrr THEN 'UPGRADE'
        WHEN mrr_usd < prev_mrr THEN 'DOWNGRADE'
        ELSE 'FLAT_RENEWAL'
    END AS delta_type
FROM sub_history


-- models/intermediate/int_active_users_28d.sql
-- Owner: nina.patel

SELECT
    customer_id,
    COUNT(DISTINCT user_id) AS active_users_28d
FROM {{ ref('stg_user_events') }}
WHERE event_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 28 DAY)
GROUP BY 1


-- models/intermediate/int_workflow_runs_28d.sql
-- Owner: david.kim

SELECT
    customer_id,
    COUNT(run_id) AS runs_count_28d,
    COUNTIF(status = 'success') AS success_runs_28d
FROM {{ ref('stg_workflow_runs') }}
WHERE triggered_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 28 DAY)
GROUP BY 1


-- models/intermediate/int_engaged_customers.sql
-- Owner: rajiv.menon
-- Logic Refreshed: 2025-Q4 per Product request.

/*
   SIGNAL: Engaged customer definition = 
   >= 3 active users AND >= 10 successful workflow runs in trailing 28 days.
*/

WITH users AS (
    SELECT * FROM {{ ref('int_active_users_28d') }}
),
runs AS (
    SELECT * FROM {{ ref('int_workflow_runs_28d') }}
),
base AS (
    SELECT 
        c.customer_id,
        COALESCE(u.active_users_28d, 0) AS active_users,
        COALESCE(r.success_runs_28d, 0) AS success_runs
    FROM {{ ref('stg_customers') }} c
    LEFT JOIN users u ON c.customer_id = u.customer_id
    LEFT JOIN runs r ON c.customer_id = r.customer_id
)

SELECT 
    customer_id,
    active_users,
    success_runs,
    CASE 
        WHEN active_users >= 3 AND success_runs >= 10 THEN TRUE 
        ELSE FALSE 
    END AS is_engaged
FROM base


-- models/intermediate/int_revenue_daily.sql
-- Owner: lina.cho

SELECT
    invoice_date AS event_date,
    customer_id,
    SUM(amount_usd) AS daily_revenue
FROM {{ ref('stg_invoices') }}
WHERE status = 'paid'
GROUP BY 1, 2


-- ####################################################################################
-- MARTS / FINANCE
-- ####################################################################################

-- models/marts/finance/arr_snapshot.sql
-- Owner: lina.cho
-- Materialization: table (refresh daily)

/*
   SIGNAL [arr]: ARR is calculated as SUM(mrr_usd) * 12.
   We MUST only count is_current = TRUE and exclude the 'Free' plan.
   This is the canonical board-ready ARR (~$39M target).
   DO NOT use dim_customers.current_mrr_usd as it drifts!
*/

WITH current_subs AS (
    SELECT 
        customer_id,
        plan_tier,
        mrr_usd
    FROM {{ ref('stg_subscriptions') }}
    WHERE is_current = TRUE
      AND plan_tier != 'Free'
)

SELECT
    CURRENT_DATE() AS snapshot_date,
    SUM(mrr_usd) * 12 AS arr_usd,
    SUM(CASE WHEN plan_tier = 'Pro' THEN mrr_usd ELSE 0 END) * 12 AS arr_pro_usd,
    SUM(CASE WHEN plan_tier = 'Business' THEN mrr_usd ELSE 0 END) * 12 AS arr_business_usd,
    SUM(CASE WHEN plan_tier = 'Enterprise' THEN mrr_usd ELSE 0 END) * 12 AS arr_enterprise_usd,
    COUNT(DISTINCT customer_id) AS paying_customers
FROM current_subs


-- models/marts/finance/nrr_trailing_12.sql
-- Owner: lina.cho

/*
   SIGNAL [nrr]: This is the canonical board NRR calculation.
   Fixed cohort: Paid customers as of 12 months ago.
   NRR calculation uses LEFT JOIN + COALESCE(end_mrr_usd, 0).
   If we inner join, we lose churned customers and NRR looks fake/inflated.
   NRR target: ~1.07. GRR target: ~0.94.
*/

WITH cohort_start AS (
    -- Customers who were paying 12 months ago
    SELECT 
        customer_id,
        mrr_usd AS start_mrr_usd
    FROM {{ ref('stg_subscriptions') }}
    WHERE start_date <= DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH)
      AND end_date > DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH)
      AND plan_tier != 'Free'
),

cohort_end AS (
    -- Their current MRR (today)
    SELECT 
        customer_id,
        mrr_usd AS end_mrr_usd
    FROM {{ ref('stg_subscriptions') }}
    WHERE is_current = TRUE
      AND plan_tier != 'Free'
)

SELECT
    COUNT(c_start.customer_id) AS cohort_size,
    SUM(c_start.start_mrr_usd) AS cohort_start_mrr_usd,
    -- CRITICAL: Coalesce to 0 for churned customers
    SUM(COALESCE(c_end.end_mrr_usd, 0)) AS cohort_end_mrr_usd,
    
    -- NRR Calculation
    SAFE_DIVIDE(SUM(COALESCE(c_end.end_mrr_usd, 0)), SUM(c_start.start_mrr_usd)) AS nrr,
    
    -- GRR Calculation (Numerator capped at denominator to ignore expansion)
    SAFE_DIVIDE(
        SUM(CASE 
            WHEN COALESCE(c_end.end_mrr_usd, 0) > c_start.start_mrr_usd THEN c_start.start_mrr_usd 
            ELSE COALESCE(c_end.end_mrr_usd, 0) 
        END), 
        SUM(c_start.start_mrr_usd)
    ) AS grr,
    
    SUM(CASE WHEN c_end.customer_id IS NULL THEN c_start.start_mrr_usd ELSE 0 END) AS churned_mrr_loss_usd,
    SUM(CASE WHEN c_end.end_mrr_usd > c_start.start_mrr_usd THEN c_end.end_mrr_usd - c_start.start_mrr_usd ELSE 0 END) AS expansion_mrr_usd
FROM cohort_start c_start
LEFT JOIN cohort_end c_end ON c_start.customer_id = c_end.customer_id


-- ####################################################################################
-- MARTS / CS
-- ####################################################################################

-- models/marts/cs/account_health.sql
-- Owner: nina.patel
-- Materialization: table

/*
   SIGNAL [health]: The logic for account health is tier-dependent.
   Critical Rule Enterprise: ONLY uncollectible invoice.
   Critical Rule Non-Enterprise: uncollectible invoice OR utilization < 20%.
   At Risk: Open P1 support ticket > 48h OR NPS detractor (score < 7).
   Healthy Expansion: Engaged AND utilization >= 60%.
*/

WITH health_metrics AS (
    SELECT 
        c.customer_id,
        c.account_tier,
        c.current_plan_tier,
        c.seat_count_licensed,
        i.active_users,
        i.is_engaged,
        -- Utilization Band
        CASE 
            WHEN c.account_tier = 'Enterprise' THEN NULL -- Enterprise has unlimited seats logic in canon
            ELSE SAFE_DIVIDE(i.active_users, c.seat_count_licensed) 
        END AS utilization_band,
        -- Support tickets
        (SELECT COUNT(*) FROM {{ ref('stg_support_tickets') }} st 
         WHERE st.customer_id = c.customer_id AND st.priority = 'P1' AND st.closed_at IS NULL 
         AND st.opened_at < TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 48 HOUR)) AS n_open_p1_over_48h,
        -- NPS
        (SELECT MIN(score) FROM {{ ref('stg_nps') }} nps 
         WHERE nps.customer_id = c.customer_id 
         AND nps.responded_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)) AS recent_nps_score,
        -- Invoices
        (SELECT COUNT(*) FROM {{ ref('stg_invoices') }} inv 
         WHERE inv.customer_id = c.customer_id AND inv.status = 'uncollectible') AS uncollectible_count
    FROM {{ ref('stg_customers') }} c
    LEFT JOIN {{ ref('int_engaged_customers') }} i ON c.customer_id = i.customer_id
)

SELECT
    customer_id,
    account_tier,
    current_plan_tier,
    (uncollectible_count > 0) AS has_uncollectible_recent,
    n_open_p1_over_48h,
    (n_open_p1_over_48h > 0) AS has_open_p1_over_48h,
    (recent_nps_score < 7) AS has_recent_nps_detractor,
    is_engaged,
    utilization_band,
    
    CASE
        -- CRITICAL
        WHEN uncollectible_count > 0 THEN 'critical'
        WHEN account_tier != 'Enterprise' AND utilization_band < 0.20 THEN 'critical'
        
        -- AT RISK
        WHEN n_open_p1_over_48h > 0 OR recent_nps_score < 7 THEN 'at_risk'
        
        -- MONITORING
        WHEN is_engaged = FALSE THEN 'monitoring'
        
        -- HEALTHY EXPANSION
        WHEN is_engaged = TRUE AND (utilization_band >= 0.6 OR account_tier = 'Enterprise') THEN 'healthy_expansion'
        
        -- STABLE
        ELSE 'stable'
    END AS account_health_status
FROM health_metrics


-- ####################################################################################
-- MARTS / PRODUCT
-- ####################################################################################

-- models/marts/product/workflow_runs_daily.sql
-- Owner: david.kim

SELECT
    CAST(triggered_at AS DATE) AS run_date,
    customer_id,
    COUNT(run_id) AS n_runs,
    COUNTIF(status = 'success') AS n_success,
    SAFE_DIVIDE(COUNTIF(status = 'success'), COUNT(run_id)) AS success_rate,
    
    -- percentiles
    APPROX_QUANTILES(duration_ms, 100)[OFFSET(50)] AS p50_duration_ms,
    APPROX_QUANTILES(duration_ms, 100)[OFFSET(95)] AS p95_duration_ms,
    APPROX_QUANTILES(duration_ms, 100)[OFFSET(99)] AS p99_duration_ms,
    
    -- Error categorizations
    COUNTIF(error_code = 'AUTH_FAILED') AS auth_failed_count,
    COUNTIF(error_code = 'RATE_LIMITED') AS rate_limited_count,
    COUNTIF(error_code = 'STEP_TIMEOUT') AS step_timeout_count,
    COUNTIF(error_code = 'INTEGRATION_DOWN') AS integration_down_count
FROM {{ ref('stg_workflow_runs') }}
GROUP BY 1, 2


-- ####################################################################################
-- MARTS / SALES
-- ####################################################################################

-- models/marts/sales/bookings_attribution.sql
-- Owner: jorge.martinez
-- Materialization: table

/*
   SIGNAL [bookings]: bookings_acv_usd is ALREADY annualized in source.
   DO NOT multiply by 12. 
   Self-serve conversions (Free -> Pro) are not here. 
   Only AE-led deals.
*/

WITH first_touches AS (
    SELECT 
        customer_id,
        channel AS first_touch_channel,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY touched_at ASC) AS rn
    FROM {{ ref('stg_marketing_touches') }}
)

SELECT
    o.opportunity_id,
    o.customer_id,
    o.account_name,
    o.amount_usd AS bookings_acv_usd,
    o.closed_won_at,
    ft.first_touch_channel
FROM {{ ref('stg_opportunities') }} o
LEFT JOIN first_touches ft ON o.customer_id = ft.customer_id AND ft.rn = 1
WHERE o.stage = 'Closed Won'


-- ####################################################################################
-- DEPRECATED / WIP
-- ####################################################################################

-- models/deprecated/old_arr_calc.sql
-- -- DEPRECATED --
-- Logic replaced by arr_snapshot.sql in Finance mart.
-- This old version was double-counting expansion due to join errors with historical subs.
-- Do not use for external reporting.

SELECT 
    customer_id,
    SUM(current_mrr_usd) * 12 AS arr -- WRONG logic: uses dim_customers which drifts
FROM {{ ref('stg_customers') }}
GROUP BY 1


-- models/marts/product/vrs_draft.sql
-- -- WIP / PARKED --
-- Owner: rajiv.menon
-- SIGNAL [vrs]: This is a parked draft spec. NOT built yet.
-- champion_login_recency and vrs_band are theoretical.

/*
SELECT
    customer_id,
    -- draft logic for VRS score
    (active_users * 0.4) + (success_runs * 0.6) AS raw_vrs,
    -- null for now
    NULL AS champion_login_recency,
    'TBD' AS vrs_band
FROM {{ ref('int_engaged_customers') }}
*/


-- ####################################################################################
-- ADDITIONAL SUPPORTING MODELS (NOISE & UTILITY)
-- ####################################################################################

-- models/intermediate/int_customer_history.sql
-- Aggregates customer state changes over time.

SELECT 
    c.customer_id,
    c.company_name,
    c.signup_date,
    c.industry,
    COUNT(s.subscription_id) AS total_subs_lifetime,
    MAX(s.start_date) AS latest_sub_start
FROM {{ ref('stg_customers') }} c
JOIN {{ ref('stg_subscriptions') }} s ON c.customer_id = s.customer_id
GROUP BY 1, 2, 3, 4


-- models/marts/cs/csm_portfolio_view.sql
-- Grouping health metrics by CSM.

SELECT
    e.full_name AS csm_name,
    ah.account_health_status,
    COUNT(ah.customer_id) AS account_count,
    SUM(arr.arr_usd) AS managed_arr
FROM {{ ref('stg_employees') }} e
JOIN {{ ref('stg_customers') }} c ON e.employee_id = c.csm_id
JOIN {{ ref('account_health') }} ah ON c.customer_id = ah.customer_id
-- joining snapshot flat
JOIN {{ ref('arr_snapshot') }} arr ON 1=1 -- simplification for dummy export
WHERE e.team = 'Customer Success'
GROUP BY 1, 2


-- models/intermediate/int_support_response_times.sql
-- Owner: nina.patel

SELECT
    ticket_id,
    customer_id,
    assignee_id,
    priority,
    TIMESTAMP_DIFF(closed_at, opened_at, HOUR) AS resolution_time_actual,
    resolution_time_hours AS expected_resolution_time
FROM {{ ref('stg_support_tickets') }}
WHERE status = 'closed'


-- models/marts/product/feature_adoption_matrix.sql
-- Owner: david.kim

SELECT
    event_name,
    COUNT(DISTINCT customer_id) AS distinct_customers_using,
    COUNT(event_id) AS total_usage_events
FROM {{ ref('stg_user_events') }}
WHERE event_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY 1


-- models/intermediate/int_opportunity_pipeline.sql
-- Current status of open deals for Sales dashboards.

SELECT
    opportunity_id,
    account_name,
    ae_id,
    stage,
    amount_usd,
    created_date,
    DATE_DIFF(CURRENT_DATE(), created_date, DAY) AS age_days
FROM {{ ref('stg_opportunities') }}
WHERE stage NOT IN ('Closed Won', 'Closed Lost')


-- models/marts/finance/monthly_billing_reconciliation.sql
-- Compares invoice totals to subscription MRR expectations.

WITH monthly_expectations AS (
    SELECT 
        customer_id,
        SUM(mrr_usd) AS expected_mrr
    FROM {{ ref('stg_subscriptions') }}
    WHERE is_current = TRUE
    GROUP BY 1
),
actual_invoices AS (
    SELECT
        customer_id,
        SUM(amount_usd) AS invoiced_amount
    FROM {{ ref('stg_invoices') }}
    WHERE invoice_date >= DATE_TRUNC(CURRENT_DATE(), MONTH)
    GROUP BY 1
)

SELECT
    c.customer_id,
    c.company_name,
    e.expected_mrr,
    a.invoiced_amount,
    COALESCE(a.invoiced_amount, 0) - e.expected_mrr AS variance
FROM {{ ref('stg_customers') }} c
LEFT JOIN monthly_expectations e ON c.customer_id = e.customer_id
LEFT JOIN actual_invoices a ON c.customer_id = a.customer_id


-- models/marts/product/platform_stability_kpis.sql
-- Rolls up errors for the engineering team.

SELECT
    DATE_TRUNC(run_date, WEEK) AS run_week,
    SUM(n_runs) AS total_runs,
    SUM(n_success) AS total_successes,
    SAFE_DIVIDE(SUM(n_success), SUM(n_runs)) AS weekly_uptime_proxy,
    SUM(auth_failed_count) AS total_auth_errors,
    SUM(integration_down_count) AS total_down_integrations
FROM {{ ref('workflow_runs_daily') }}
GROUP BY 1


-- models/intermediate/int_user_retention.sql
-- Calculation of cohorts for user-level retention.

WITH user_first_event AS (
    SELECT 
        user_id,
        MIN(event_at) AS first_seen
    FROM {{ ref('stg_user_events') }}
    GROUP BY 1
)

SELECT
    DATE_TRUNC(CAST(f.first_seen AS DATE), MONTH) AS cohort_month,
    DATE_DIFF(CAST(e.event_at AS DATE), CAST(f.first_seen AS DATE), MONTH) AS months_since_signup,
    COUNT(DISTINCT e.user_id) AS active_users
FROM user_first_event f
JOIN {{ ref('stg_user_events') }} e ON f.user_id = e.user_id
GROUP BY 1, 2


-- models/marts/cs/nps_sentiment_rollup.sql
-- Aggregating NPS comments and scores by industry/tier.

SELECT
    survey_quarter,
    industry,
    account_tier,
    AVG(score) AS avg_nps_score,
    COUNT(response_id) AS response_count,
    COUNTIF(score >= 9) AS promoters,
    COUNTIF(score <= 6) AS detractors
FROM {{ ref('stg_nps') }}
GROUP BY 1, 2, 3


-- models/marts/sales/ae_performance_scorecard.sql
-- Logic for calculating sales quotas attainment.

SELECT
    e.full_name AS ae_name,
    COUNT(o.opportunity_id) AS deals_closed,
    SUM(o.bookings_acv_usd) AS total_bookings_acv,
    AVG(DATE_DIFF(CAST(o.closed_won_at AS DATE), o.created_date, DAY)) AS avg_cycle_days
FROM {{ ref('stg_employees') }} e
JOIN {{ ref('bookings_attribution') }} o ON e.employee_id = CAST(o.ae_id AS INT64)
GROUP BY 1


-- models/staging/stg_usage_logs_raw.sql
-- Note: This is a heavy pass-through for debugging.

SELECT 
    * 
FROM {{ source('acme_raw', 'fact_workflow_runs') }}
-- Filter for just the last 2 hours to keep the mart light
WHERE triggered_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 2 HOUR)


-- models/marts/finance/finance_actuals_vs_target.sql
-- Compares actual ARR to target values (hardcoded for demo).

SELECT
    snapshot_date,
    arr_usd AS actual_arr,
    39500000 AS target_arr, -- Goal for end of Q2 2026
    SAFE_DIVIDE(arr_usd, 39500000) AS percent_of_target
FROM {{ ref('arr_snapshot') }}


-- models/intermediate/int_plan_upgrades.sql
-- Specifically looking at Free-to-Paid conversions.

SELECT
    customer_id,
    start_date AS conversion_date,
    mrr_usd AS new_mrr
FROM {{ ref('int_subscription_changes') }}
WHERE delta_type = 'NEW' 
  AND plan_tier != 'Free'


-- models/marts/product/step_count_analysis.sql
-- Looking at workflow complexity.

SELECT
    customer_id,
    AVG(step_count) AS avg_steps_per_run,
    MAX(step_count) AS max_steps_per_run,
    COUNT(DISTINCT workflow_id) AS distinct_workflows
FROM {{ ref('stg_workflow_runs') }}
GROUP BY 1


-- models/marts/sales/win_loss_analysis.sql
-- Analyzing why we lose deals.

SELECT
    loss_reason,
    COUNT(*) AS deal_count,
    SUM(amount_usd) AS lost_acv
FROM {{ ref('stg_opportunities') }}
WHERE stage = 'Closed Lost'
GROUP BY 1


-- models/marts/cs/support_efficiency.sql
-- CS response metrics.

SELECT
    category,
    priority,
    AVG(resolution_time_hours) AS avg_hours_to_close,
    AVG(csat_score) AS avg_csat
FROM {{ ref('stg_support_tickets') }}
GROUP BY 1, 2


-- models/marts/product/user_segmentation.sql
-- Basic RFM-style segmentation for users.

SELECT
    user_id,
    customer_id,
    COUNT(event_id) AS total_events_lifetime,
    MAX(event_at) AS last_event_at,
    TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), MAX(event_at), DAY) AS days_since_last_event
FROM {{ ref('stg_user_events') }}
GROUP BY 1, 2


/*
EOF: Model Export Complete.
Total Models: 41
Environment: Production
Target: nexus-analyst-demo.acme
*/