---
title: "dbt model documentation: the 6 canonical derived marts"
source_url: "internal://acme-ecomm/dbt/q1fy26__core-marts-model-documentation"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2025-04-15T12:00:00+00:00'
adapter: dbt_model
---

```sql
-- ============================================================================
-- MODEL: traffic_conversion_summary
-- OWNER: wei.hartono (assoc_100210)
-- DESCRIPTION: Weekly aggregate traffic, sessions, orders, and conversion rate
--              by market and vertical. Serves as the primary board source for
--              US_CONV tracking. 
-- DEPENDS_ON: fact_traffic_daily, dim_date, dim_vertical
-- ============================================================================

{{
  config(
    materialized = 'table',
    schema = 'acme_ecomm',
    tags = ['core', 'traffic', 'conversion', 'weekly']
  )
}}

SELECT
    d.week_ending_date AS fiscal_week_ending,
    f.market,
    f.vertical_code,
    SUM(f.sessions) AS sessions,
    f.sessions_definition_version,
    SUM(f.orders) AS orders,
    -- Conversion rate = orders / sessions (session-based)
    SAFE_DIVIDE(SUM(f.orders), SUM(f.sessions)) AS conversion_rate,
    SUM(f.gmv_usd) AS gmv_usd,
    -- TODO(wei): reconcile YoY calc with Amara's finance pack once MBR v2 locks
    CAST(NULL AS NUMERIC) AS orders_yoy_pct
FROM {{ ref('fact_traffic_daily') }} f
JOIN {{ ref('dim_date') }} d ON f.date = d.date
GROUP BY 1, 2, 3, 5
```

```sql
-- ============================================================================
-- MODEL: fulfillment_speed_daily
-- OWNER: wei.hartono (assoc_100210)
-- DESCRIPTION: Daily fulfillment performance metrics broken down by market,
--              vertical, and fulfillment type. Source of truth for Speed VBR/MBR.
-- DEPENDS_ON: fact_promise_vs_actual, fact_orders, dim_date
-- ============================================================================

{{
  config(
    materialized = 'table',
    schema = 'acme_ecomm',
    tags = ['core', 'speed', 'fulfillment', 'daily']
  )
}}

SELECT
    p.date,
    p.market,
    p.vertical_code,
    p.fulfillment_type,
    SUM(p.orders_promised) AS orders_promised,
    SAFE_DIVIDE(SUM(p.orders_on_time), SUM(p.orders_promised)) AS on_time_rate,
    -- pct_of_total_orders makes mix-shift checks verifiable
    SAFE_DIVIDE(
        SUM(p.orders_promised),
        SUM(SUM(p.orders_promised)) OVER (PARTITION BY p.date, p.market)
    ) AS pct_of_total_orders,
    AVG(o.refund_usd) AS avg_cost_per_order_usd -- FIXME: alias check needed against cost model
FROM {{ ref('fact_promise_vs_actual') }} p
LEFT JOIN {{ ref('fact_orders') }} o ON p.date = o.order_date AND p.fulfillment_type = o.fulfillment_type
GROUP BY 1, 2, 3, 4
```

```sql
-- ============================================================================
-- MODEL: care_deflection_daily
-- OWNER: wei.hartono (assoc_100210)
-- DESCRIPTION: Daily aggregation of customer care contacts, channel distribution,
--              deflection performance, and CSAT scores by sub-program.
-- DEPENDS_ON: fact_care_contacts, dim_date
-- ============================================================================

{{
  config(
    materialized = 'table',
    schema = 'acme_ecomm',
    tags = ['core', 'care', 'deflection', 'daily']
  )
}}

SELECT
    DATE(c.opened_at) AS date,
    c.sub_program,
    COUNT(c.contact_id) AS contact_volume,
    SAFE_DIVIDE(COUNTIF(c.deflected), COUNT(c.contact_id)) AS deflection_rate,
    AVG(CASE WHEN c.deflected THEN c.csat_score END) AS avg_csat_deflected,
    AVG(CASE WHEN NOT c.deflected THEN c.csat_score END) AS avg_csat_agent_assisted,
    AVG(c.handle_time_minutes) AS avg_handle_time_minutes
FROM {{ ref('fact_care_contacts') }} c
GROUP BY 1, 2
```

```sql
-- ============================================================================
-- MODEL: member_cltv
-- OWNER: wei.hartono (assoc_100210)
-- DESCRIPTION: Member-level lifecycle and lifetime value metrics for Acme+.
--              CAUTION: Must use LEFT JOIN dim_member to fact_orders with
--              COALESCE(trailing_12mo_gmv_usd, 0).
-- DEPENDS_ON: dim_member, fact_orders, fact_membership_events
-- ============================================================================

{{
  config(
    materialized = 'table',
    schema = 'acme_ecomm',
    tags = ['core', 'membership', 'cltv']
  )
}}

-- SIGNAL [cltv-join-drop]:
-- The canonical build LEFT JOINs dim_member to fact_orders with 
-- COALESCE(trailing_12mo_gmv_usd, 0). An INNER JOIN silently drops the 
-- 20% of the 120,000-member panel (24,000 members) with zero orders in 
-- the trailing 12 months — inflating average CLTV from the correct 
-- $500/member to a wrong $625/member (25% overstatement) and hiding 
-- the dormant/churn-risk population entirely. Do not alter this join logic.

SELECT
    m.member_id,
    CAST(FORMAT_DATE('%Y-Q%Q', m.signup_date) AS STRING) AS signup_cohort_quarter,
    DATE_DIFF(CURRENT_DATE(), m.signup_date, DAY) AS tenure_days,
    COUNT(o.order_id) AS lifetime_orders,
    SUM(COALESCE(o.gmv_usd, 0)) AS lifetime_gmv_usd,
    SUM(CASE WHEN o.order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR) THEN COALESCE(o.gmv_usd, 0) ELSE 0 END) AS trailing_12mo_gmv_usd,
    COUNTIF(o.order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR)) AS trailing_12mo_orders,
    COUNT(DISTINCT e.benefit_code) AS benefits_adopted_count,
    m.status = 'active' AS is_active,
    -- placeholder for projected model output
    SUM(COALESCE(o.gmv_usd, 0)) * 1.25 AS projected_cltv_usd
FROM {{ ref('dim_member') }} m
LEFT JOIN {{ ref('fact_orders') }} o ON m.member_id = o.member_id
LEFT JOIN {{ ref('fact_membership_events') }} e ON m.member_id = e.member_id AND e.event_type = 'benefit_redeemed'
GROUP BY 1, 2, 3, 10
```

```sql
-- ============================================================================
-- MODEL: marketplace_seller_performance
-- OWNER: wei.hartono (assoc_100210)
-- DESCRIPTION: Seller-level performance aggregate covering listing counts, 
--              trailing GMV, return rates, shipping times, and authenticity flags.
-- DEPENDS_ON: dim_seller, fact_marketplace_listings, fact_orders
-- ============================================================================

{{
  config(
    materialized = 'table',
    schema = 'acme_ecomm',
    tags = ['core', 'marketplace', 'seller_health']
  )
}}

SELECT
    s.seller_id,
    s.category_focus,
    COUNTIF(l.status = 'active') AS active_listings,
    SUM(CASE WHEN o.order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY) THEN o.gmv_usd ELSE 0 END) AS trailing_90d_gmv_usd,
    SAFE_DIVIDE(COUNTIF(o.is_returned), COUNT(o.order_id)) AS return_rate,
    AVG(DATE_DIFF(o.order_date, l.listed_date, DAY)) AS avg_days_to_ship,
    COUNTIF(NOT l.authenticity_verified) AS authenticity_flag_count,
    CAST(NULL AS NUMERIC) AS avg_buyer_rating
FROM {{ ref('dim_seller') }} s
LEFT JOIN {{ ref('fact_marketplace_listings') }} l ON s.seller_id = l.seller_id
LEFT JOIN {{ ref('fact_orders') }} o ON s.seller_id = o.seller_id
GROUP BY 1, 2
```

```sql
-- ============================================================================
-- MODEL: marketplace_gmv_summary
-- OWNER: wei.hartono (assoc_100210)
-- DESCRIPTION: Full-population aggregate for Marketplace GMV by sub-vertical 
--              and fiscal week. 
-- NOTE: This is full-population and the canonical source for Marketplace 
--       GMV-by-sub-vertical. Never query fact_orders for this cut, per convention 5.
-- DEPENDS_ON: fact_orders, dim_date, dim_vertical
-- ============================================================================

{{
  config(
    materialized = 'table',
    schema = 'acme_ecomm',
    tags = ['core', 'marketplace', 'gmv', 'weekly']
  )
}}

-- NOTE: Full population source. Do not substitute fact_orders aggregate here.
-- Reconciles against quarterly MBR figures for Style, Resold, and Collectibles.

SELECT
    d.week_ending_date AS fiscal_week_ending,
    o.sub_vertical_code,
    SUM(o.gmv_usd) AS gmv_usd,
    COUNT(o.order_id) AS orders,
    0.135 AS take_rate -- standard commission take rate baseline proxy
FROM {{ ref('fact_orders') }} o
JOIN {{ ref('dim_date') }} d ON o.order_date = d.date
WHERE o.channel = '3P'
GROUP BY 1, 2
```

```sql
-- Data engineering notes from wei.hartono:
-- Following carlos.figueroa's promotion to VP Data & Analytics back in March '25 
-- (see LEDGER), we've been leaning hard into standardizing these 6 marts across 
-- all regional schemas. Remember that BigQuery is FLAT in nexus-analyst-demo.acme_ecomm,
-- so don't let anyone write nested queries like acme_ecomm.marts.membership.member_cltv. 
-- Also, keep an eye on the partition expiration settings for fact_traffic_daily; 
-- Connor Blake mentioned running a backfill for the session_definition_version 1->2 
-- cutover that happened on 2026-03-02, but historical partitions should remain untouched.
-- If anyone asks about Compass dashboard differences on Q4FY26 Marketplace GMV, 
-- direct them to the canonical mart output ($975.0M) rather than the stale $952.4M 
-- cached view.
```
