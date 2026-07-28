---
title: "BigQuery schema reference dump: acme_ecomm dataset (23 tables)"
source_url: "internal://acme-ecomm/schema/q1fy26__acme-ecomm-bigquery-warehouse-schema-reference"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2025-04-15T12:00:00+00:00'
adapter: bq_schema
---

```sql
-- ============================================================================
-- DATASET: acme_ecomm (BigQuery)
-- REPOSITORY OWNER: wei.hartono (assoc_100210)
-- REFRESH SCHEDULE: Daily, complete by 06:00 AM Eastern Time
-- ============================================================================
-- NOTE: BigQuery dataset is FLAT: nexus-analyst-demo.acme_ecomm.<table>. 
-- No nested datasets (e.g., NO acme_ecomm.marts.*, NO acme_ecomm.membership.*).
-- Queries attempting to use nested dataset paths will fail with NOT_FOUND.
-- ============================================================================
```

### Table of Contents
1. Dimensions (`dim_date`, `dim_vertical`, `dim_associate`, `dim_member`, `dim_fulfillment_node`, `dim_seller`, `dim_experiment`, `dim_marketing_calendar`)
2. Base Facts (`fact_traffic_daily`, `fact_orders`, `fact_experiment_exposures`, `fact_experiment_readouts`, `fact_promise_vs_actual`, `fact_care_contacts`, `fact_marketplace_listings`, `fact_membership_events`, `fact_voc_responses`)
3. Derived Marts (`traffic_conversion_summary`, `fulfillment_speed_daily`, `care_deflection_daily`, `member_cltv`, `marketplace_seller_performance`, `marketplace_gmv_summary`)

---

### 1. DIMENSIONS (8 Tables)

#### `nexus-analyst-demo.acme_ecomm.dim_date`
Calendar and fiscal date mapping for retail operations.
- `date` DATE
- `fiscal_year` INT64
- `fiscal_quarter` INT64
- `fiscal_quarter_label` STRING (e.g., `"Q1FY27"`)
- `fiscal_week` INT64
- `week_ending_date` DATE
- `is_peak_holiday` BOOL
- `day_of_week` STRING
- `is_weekend` BOOL

#### `nexus-analyst-demo.acme_ecomm.dim_vertical`
Internal vertical and sub-vertical taxonomy definition table.
- `vertical_code` STRING
- `vertical_name` STRING
- `sub_vertical_code` STRING NULLABLE
- `sub_vertical_name` STRING NULLABLE
- `is_deep_dip` BOOL
- `customer_facing_desc` STRING

#### `nexus-analyst-demo.acme_ecomm.dim_associate`
Corporate product, data, and operations personnel directory (excludes frontline store associates).
- `assoc_id` STRING
- `full_name` STRING
- `role` STRING
- `team` STRING
- `manager_assoc_id` STRING NULLABLE
- `hire_date` DATE
- `termination_date` DATE NULLABLE
- `location` STRING
- `is_active` BOOL

#### `nexus-analyst-demo.acme_ecomm.dim_member`
Member profile and loyalty plan attributes.
- `member_id` STRING
- `signup_date` DATE
- `home_market` STRING
- `plan_type` STRING (`monthly` | `annual`)
- `plan_price_usd` NUMERIC
- `status` STRING (`active` | `paused` | `cancelled`)
- `cancel_date` DATE NULLABLE
- `acquisition_channel` STRING
- **ROW COUNT:** 120,000 rows
- **ANNOTATION:** representative panel, not full population

#### `nexus-analyst-demo.acme_ecomm.dim_fulfillment_node`
Fulfillment center, distribution center, and store node network directory.
- `node_id` STRING
- `node_type` STRING (`dc` | `fc` | `store` | `sortation_center` | `returns_center`)
- `node_name` STRING
- `market` STRING
- `opened_date` DATE
- `store_format` STRING NULLABLE (applies only to `store`: `supercenter` | `neighborhood` | `club`)
- `is_active` BOOL

#### `nexus-analyst-demo.acme_ecomm.dim_seller`
Third-party marketplace merchant profiles and operational metadata.
- `seller_id` STRING
- `seller_name` STRING
- `category_focus` STRING (`collectibles` | `resold` | `style` | `other`)
- `onboarded_date` DATE
- `application_date` DATE NULLABLE
- `status` STRING (`active` | `suspended` | `offboarded`)
- `fulfillment_method` STRING (`seller_fulfilled` | `ship_with_acme`)
- `home_country` STRING
- **ROW COUNT:** ~2,560 rows
- **ANNOTATION:** representative panel, not full population

#### `nexus-analyst-demo.acme_ecomm.dim_experiment`
Experiment metadata repository for A/B and multivariate tests across digital properties.
- `experiment_id` STRING
- `experiment_name` STRING
- `vertical_code` STRING
- `owner_assoc_id` STRING
- `hypothesis` STRING
- `start_date` DATE
- `end_date` DATE NULLABLE
- `status` STRING (`running` | `shipped` | `killed` | `paused`)
- `primary_metric` STRING

#### `nexus-analyst-demo.acme_ecomm.dim_marketing_calendar`
Marketing campaigns, launches, promos, and budgetary shift scheduling.
- `event_id` STRING
- `event_name` STRING
- `event_type` STRING (`campaign` | `launch` | `promo` | `holiday` | `budget_change`)
- `vertical_code` STRING NULLABLE
- `market` STRING NULLABLE
- `start_date` DATE
- `end_date` DATE NULLABLE
- `planned_spend_usd` NUMERIC NULLABLE
- `actual_spend_usd` NUMERIC NULLABLE
- `owner_assoc_id` STRING
- `notes` STRING

---

### 2. BASE FACTS (9 Tables)

#### `nexus-analyst-demo.acme_ecomm.fact_traffic_daily`
Pre-aggregated daily traffic, conversion funnel metrics by market, vertical, and device.
- `date` DATE
- `market` STRING
- `vertical_code` STRING
- `sub_vertical_code` STRING NULLABLE
- `device` STRING (`web` | `app` | `store_kiosk`)
- `sessions` INT64
- `sessions_definition_version` INT64 (`1` = pre-2026-03-02 bot/dup filtering upgrade; `2` = post-upgrade)
- `product_view_sessions` INT64
- `add_to_cart_sessions` INT64
- `checkout_started_sessions` INT64
- `orders` INT64
- `units` INT64
- `gmv_usd` NUMERIC

#### `nexus-analyst-demo.acme_ecomm.fact_orders`
Transactional order grain connecting member, seller, and fulfillment attributes.
- `order_id` STRING
- `order_date` DATE
- `member_id` STRING NULLABLE
- `market` STRING
- `vertical_code` STRING
- `sub_vertical_code` STRING NULLABLE
- `channel` STRING (`1P` | `3P`)
- `seller_id` STRING NULLABLE (populated only when `channel` = `3P`)
- `fulfillment_type` STRING (`ship_to_home` | `bopis` | `curbside` | `dfs`)
- `gmv_usd` NUMERIC
- `units` INT64
- `device` STRING
- `is_returned` BOOL
- `return_date` DATE NULLABLE
- `return_reason_code` STRING NULLABLE
- `refund_usd` NUMERIC NULLABLE
- `refund_issued_date` DATE NULLABLE
- **ROW COUNT:** ~400,000 rows
- **ANNOTATION:** representative panel, not full population

#### `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures`
Aggregate daily assignment and exposure counts per experiment variant.
- `experiment_id` STRING
- `variant` STRING
- `exposure_date` DATE
- `units_assigned` INT64
- `units_exposed` INT64
- `units_converted` INT64

#### `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`
Calculated metric readouts and lift metrics by experiment variant and date.
- `experiment_id` STRING
- `variant` STRING
- `as_of_date` DATE
- `metric_name` STRING
- `metric_value` NUMERIC
- `sample_size_units` INT64
- `lift_vs_control_pct` NUMERIC NULLABLE
- `is_significant` BOOL
- `notes` STRING

#### `nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`
Fulfillment delivery date accuracy tracking against customer-facing shipping promises.
- `date` DATE
- `market` STRING
- `vertical_code` STRING
- `fulfillment_type` STRING
- `orders_promised` INT64
- `orders_on_time` INT64
- `avg_days_late_when_late` NUMERIC
- `node_id` STRING NULLABLE

#### `nexus-analyst-demo.acme_ecomm.fact_care_contacts`
Customer support contact logs, deflection tracking, channel, and satisfaction scores.
- `contact_id` STRING
- `member_id` STRING NULLABLE
- `order_id` STRING NULLABLE
- `market` STRING
- `sub_program` STRING (`automate` | `avoid` | `optimize` | `platform` | `member_care`)
- `channel` STRING (`chat` | `phone` | `bot` | `email`)
- `opened_at` TIMESTAMP
- `closed_at` TIMESTAMP NULLABLE
- `deflected` BOOL
- `deflection_type` STRING NULLABLE
- `resolution_code` STRING
- `csat_score` INT64 NULLABLE (scale 1-5)
- `handle_time_minutes` NUMERIC NULLABLE
- `assoc_id` STRING NULLABLE (NULL if bot-only interaction)
- **ROW COUNT:** ~50,000 rows
- **ANNOTATION:** representative panel, not full population

#### `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
Third-party inventory listings catalog, pricing, and verification status.
- `listing_id` STRING
- `seller_id` STRING
- `category` STRING (`collectibles` | `resold` | `style` | `other`)
- `listed_date` DATE
- `price_usd` NUMERIC
- `status` STRING (`active` | `removed` | `suspended`)
- `authenticity_verified` BOOL
- **ROW COUNT:** ~35,000 rows
- **ANNOTATION:** representative panel, not full population

#### `nexus-analyst-demo.acme_ecomm.fact_membership_events`
Acme+ loyalty membership lifecycle and benefit redemption event stream.
- `event_id` STRING
- `member_id` STRING
- `event_date` DATE
- `event_type` STRING (`signup` | `renewal` | `cancel` | `pause` | `resume` | `benefit_redeemed`)
- `benefit_code` STRING NULLABLE
- `channel` STRING
- **ROW COUNT:** ~450,000 rows
- **ANNOTATION:** representative panel, not full population

#### `nexus-analyst-demo.acme_ecomm.fact_voc_responses`
Buyer-side Voice of Customer (Medallia) survey responses, verbatims, and sentiment tags.
- `response_id` STRING
- `member_id` STRING NULLABLE
- `order_id` STRING NULLABLE
- `market` STRING
- `vertical_code` STRING NULLABLE
- `survey_type` STRING (`post_purchase` | `post_care_contact` | `nps`)
- `responded_at` TIMESTAMP
- `score` NUMERIC
- `score_type` STRING (`nps_0_10` | `csat_1_5` | `ces_1_7`)
- `verbatim_text` STRING
- `theme_tag` STRING NULLABLE
- `sentiment` STRING (`positive` | `neutral` | `negative`)
- **ROW COUNT:** ~40,000 rows
- **ANNOTATION:** representative panel, not full population

---

### 3. DERIVED MARTS (6 Tables)

#### `nexus-analyst-demo.acme_ecomm.traffic_conversion_summary`
Weekly traffic, orders, conversion rate, and GMV summaries by market and vertical.
- `fiscal_week_ending` DATE
- `market` STRING
- `vertical_code` STRING
- `sessions` INT64
- `sessions_definition_version` INT64
- `orders` INT64
- `conversion_rate` NUMERIC
- `gmv_usd` NUMERIC
- `orders_yoy_pct` NUMERIC NULLABLE

#### `nexus-analyst-demo.acme_ecomm.fulfillment_speed_daily`
Daily fulfillment delivery speed metrics, cost, and mix share by channel.
- `date` DATE
- `market` STRING
- `vertical_code` STRING
- `fulfillment_type` STRING
- `orders_promised` INT64
- `on_time_rate` NUMERIC
- `pct_of_total_orders` NUMERIC
- `avg_cost_per_order_usd` NUMERIC

#### `nexus-analyst-demo.acme_ecomm.care_deflection_daily`
Daily customer care operational KPIs, deflection rates, handle times, and segment CSAT.
- `date` DATE
- `sub_program` STRING
- `contact_volume` INT64
- `deflection_rate` NUMERIC
- `avg_csat_deflected` NUMERIC
- `avg_csat_agent_assisted` NUMERIC
- `avg_handle_time_minutes` NUMERIC

#### `nexus-analyst-demo.acme_ecomm.member_cltv`
Member Customer Lifetime Value calculations, tenure, historical order metrics, and benefit adoption.
- `member_id` STRING
- `signup_cohort_quarter` STRING
- `tenure_days` INT64
- `lifetime_orders` INT64
- `lifetime_gmv_usd` NUMERIC
- `trailing_12mo_gmv_usd` NUMERIC
- `trailing_12mo_orders` INT64
- `benefits_adopted_count` INT64
- `is_active` BOOL
- `projected_cltv_usd` NUMERIC

#### `nexus-analyst-demo.acme_ecomm.marketplace_seller_performance`
Third-party marketplace merchant performance aggregates, active listings, and return rates.
- `seller_id` STRING
- `category_focus` STRING
- `active_listings` INT64
- `trailing_90d_gmv_usd` NUMERIC
- `return_rate` NUMERIC
- `avg_days_to_ship` NUMERIC
- `authenticity_flag_count` INT64
- `avg_buyer_rating` NUMERIC

#### `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`
Weekly full-population marketplace gross merchandise value, orders, and take rate by sub-vertical.
- `fiscal_week_ending` DATE
- `sub_vertical_code` STRING
- `gmv_usd` NUMERIC
- `orders` INT64
- `take_rate` NUMERIC

---

```sql
-- Schema documentation audit check completed by wei.hartono.
-- Note regarding recent organizational changes: carlos.figueroa's promotion to 
-- VP Data & Analytics (assoc_100060) was formally recorded earlier this fiscal quarter 
-- (2025-03-10); pipeline monitoring permissions have been updated accordingly across all 
-- 23 datasets. Please contact data-eng-leads@acme-ecomm.internal for table access provisioning.
```
