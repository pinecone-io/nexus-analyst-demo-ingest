---
title: "dbt model change doc: sessions_definition_version 1→2 (bot/crawler filtering + de-dup)"
source_url: "internal://acme-ecomm/dbt/q1fy27__sessions-definition-version-2-model-change"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-04-15T12:00:00+00:00'
adapter: dbt_model
---

# dbt Model Change Documentation: `fact_traffic_daily` & Downstream Marts
**Model:** `fact_traffic_daily`  
**Schema:** `acme_ecomm` (BigQuery dataset, flat structure per architectural conventions)  
**Author:** wei.hartono (assoc_00210, Analytics Engineering)  
**Reviewers:** carlos.figueroa (assoc_00060), amara.shah (assoc_00211), connor.blake (assoc_00212)  
**Date of Cutover:** 2026-03-02  
**Version Bump:** `sessions_definition_version`: `1` → `2`

---

## 1. Overview & Context

Following the FY26 year-end audit reviews and ongoing noise in our digital traffic logs—exacerbated by automated scrapers, headless browser crawlers, and aggressive multi-tab user behavior during peak promotional windows—we have completed a major structural overhaul of the session-counting logic underlying `fact_traffic_daily`. 

Prior to March 2, 2026, session identifiers were generated downstream of raw Hive event streams using a loose 30-minute inactivity timeout window without adequate user-agent validation or cross-tab instance reconciliation. This caused inflated session counts, particularly across our US conversion channels (`US_CONV`), and distorted top-line conversion rate denominators (`orders / sessions`). 

With this model change, we are officially bumping the `sessions_definition_version` column value from `1` (covering all historical logs from the FY26 baseline through 2026-03-01) to `2` (covering all data from 2026-03-02 onward). 

---

## 2. Critical Analytical Warning: Mechanical Conversion Inflation

**IMPORTANT NOTICE FOR ANALYSTS, FINANCE, AND LEADERSHIP:**

This model change **MECHANICALLY raises measured conversion rate by shrinking the session denominator**, independent of any real behavior change. 

Because `conversion_rate` is calculated as `orders / sessions`, removing unauthenticated bot traffic and collapsing multi-tab concurrent sessions reduces total measured `sessions` while leaving confirmed `orders` largely untouched. Consequently, anyone comparing conversion rates across the 2026-03-02 boundary (such as comparing Q4FY26 peak metrics directly against Q1FY27 pacing) will observe an artificial step-function increase. 

To preserve auditability, the derived mart `traffic_conversion_summary` carries the version flag forward **ON PURPOSE** rather than silently adjusting or backfilling historical rows. Analysts must explicitly check the `sessions_definition_version` column before running period-over-period or YoY comparisons. Do not attribute the post-March jump in conversion exclusively to user-facing optimizations (such as Maya Lindqvist's Item Page Iteration Program or Owen Faust's checkout changes) without accounting for this structural definitional shift.

---

## 3. Technical Implementation & SQL Logic Change

The upstream extraction pipeline now incorporates an explicit bot-filtering regex against known crawler user-agents, alongside a session-de-duplication pass that groups concurrent event hits originating from the same authenticated or anonymous device fingerprint within a rolling 15-minute synchronization window.

The core transformation logic implemented in the `fact_traffic_daily` dbt model is structured as follows:

```sql
{{
    config(
        materialized='incremental',
        partition_by={'field': 'date', 'data_type': 'date'},
        cluster_by=['market', 'vertical_code', 'device']
    )
}}

WITH raw_sessions AS (
    SELECT
        DATE(event_timestamp) AS date,
        market,
        vertical_code,
        sub_vertical_code,
        device,
        session_id,
        user_id,
        client_fingerprint,
        user_agent,
        -- Check if user agent matches known automated scrapers or search bots
        REGEXP_CONTAINS(LOWER(user_agent), r'(googlebot|bingbot|slurp|duckduckbot|baiduspider|yandexbot|semrushbot|ahrefsbot|mj12bot|dotbot|petalbot|facebookexternalhit)') AS is_bot_crawler,
        -- Track first and last activity for multi-tab deduplication
        MIN(event_timestamp) OVER(PARTITION BY client_fingerprint, DATE(event_timestamp)) AS first_session_hit,
        ROW_NUMBER() OVER(PARTITION BY client_fingerprint, session_id ORDER BY event_timestamp ASC) as rn
    FROM {{ ref('stg_hive_clickstream_logs') }}
    WHERE DATE(event_timestamp) >= '2025-02-01'
    {% if is_incremental() %}
      AND DATE(event_timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 3 DAY)
    {% endif %}
),

filtered_traffic AS (
    SELECT
        date,
        market,
        vertical_code,
        sub_vertical_code,
        device,
        session_id,
        -- If it's a bot or an overlapping secondary tab fingerprint within a short burst, flag for exclusion
        CASE 
            WHEN is_bot_crawler THEN FALSE
            WHEN rn > 1 AND TIMESTAMP_DIFF(event_timestamp, first_session_hit, MINUTE) < 15 THEN FALSE
            ELSE TRUE
        END AS is_valid_session
    FROM raw_sessions
)

SELECT
    date,
    market,
    vertical_code,
    sub_vertical_code,
    device,
    COUNT(DISTINCT CASE WHEN is_valid_session THEN session_id END) AS sessions,
    2 AS sessions_definition_version,
    COUNT(DISTINCT CASE WHEN is_valid_session AND reached_product_view THEN session_id END) AS product_view_sessions,
    COUNT(DISTINCT CASE WHEN is_valid_session AND reached_add_to_cart THEN session_id END) AS add_to_cart_sessions,
    COUNT(DISTINCT CASE WHEN is_valid_session AND reached_checkout THEN session_id END) AS checkout_started_sessions,
    -- Orders and GMV remain tied to confirmed transactional fact tables joined by date/market/vertical
    COALESCE(ord.orders_count, 0) AS orders,
    COALESCE(ord.units_count, 0) AS units,
    COALESCE(ord.gmv_total_usd, 0) AS gmv_usd
FROM filtered_traffic f
LEFT JOIN {{ ref('int_orders_aggregated_daily') }} ord
  USING (date, market, vertical_code, sub_vertical_code, device)
GROUP BY 1, 2, 3, 4, 5, 10, 11, 12
```

---

## 4. Impact on Downstream Marts & Item Page Metrics

Because `product_view_sessions` and `add_to_cart_sessions` reside within the exact same `fact_traffic_daily` grain, this model change cascades across all secondary engagement indicators. 

For instance, the site-wide view-to-cart rate (`add_to_cart_sessions / product_view_sessions`) experienced an immediate upward shift upon cutover. Pre-cutover averages in February 2026 hovered near **18.0%**, whereas post-cutover metrics across March and April 2026 settled closer to **19.9%**. Some portion of that +1.9pp raw move is mechanical (stemming from the removal of phantom bot sessions that viewed items without interacting) and some corresponds to real user behavior influenced by Maya Lindqvist's Item Page Iteration Program (such as the image gallery zoom/swipe update shipped on March 5) — splitting the two requires comparing like-for-like versions, not averaging the raw quarter.

### Flat Dataset Architecture Verification
Analysts querying these metrics must ensure they are referencing the canonical flat path:
`nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
Any legacy queries attempting to hit nested paths like `acme_ecomm.marts.traffic.*` will fail, as BigQuery datasets in this warehouse are strictly flat per architecture guidelines.

---

## 5. Administrative Aside / Slack Chatter Log

*Excerpt from `#data-eng-core` Slack channel, 2026-03-02:*
> **connor.blake:** `@wei.hartono` hey Wei, just checking on the BigQuery partition jobs for `fact_traffic_daily`. Did the version 2 backfill job finish clearing out the old crawler partitions for US_CONV?
> **wei.hartono:** `@connor.blake` yeah, partition overwrite completed around 04:00 AM ET. All rows from March 2 onward are stamping `sessions_definition_version = 2`. Just make sure Amara's MBR finance deck templates are pulling from `traffic_conversion_summary` so leadership doesn't panic over the session drop in US conversion channels.
> **amara.shah:** Saw the ping. Already added a footnote to the conversion slides noting the bot filter update. Thanks for getting this across the line before the weekly review pack locked!

---
