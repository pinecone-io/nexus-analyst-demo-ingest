---
title: "Notion (draft) — cohort retention spec for new mart"
source_url: "internal://acme/notion/drafts/cohort-retention-spec"
license: "synthetic-demo"
attribution: "Acme Inc internal documentation (synthetic demo). Owner: Dan Lee (Product Analytics)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: notion_runbook
---

# Notion (draft) — cohort retention spec for new mart

> ⚠️ **DRAFT — WORK IN PROGRESS**
> **Owner**: @dan.lee
> **Status**: Scoping / Blocked on definition alignment
> **Target Materialization**: `marts/product/cohort_retention_monthly.sql`
> **Consulted**: @david.kim (Data Eng)
>
> **Note to analysts**: This model is NOT yet in production. Do not cite these figures in board decks or use the proposed table in Looker until this warning is removed.

## Problem Statement

Our current revenue reporting in `dbt__model__nrr_trailing_12.md` is excellent for board-level ARR health, but it aggregates across the entire customer book. This masks "cohort drift"—we suspect that customers who signed up in 2023 (early adopters) have significantly higher retention profiles than the mass-market cohorts from late 2025. 

To optimize LTV, we need a dedicated logo-retention mart that buckets customers by signup month and tracks their survival at specific milestones (Month 3, 6, 12, 24).

## Proposed Model: `marts/product/cohort_retention_monthly`

This model will provide a "triangle" view of logo retention.

### Dimensions
- `cohort_month`: The month the customer first appeared in `dim_customers`.
- `account_tier_at_signup`: SMB / MM / Ent (captured from the first `fact_opportunities` or `dim_customers` record).
- `months_since_signup`: Integer (0, 1, 2... up to 36).

### Metrics
- `original_cohort_size`: Total logos in that month's cohort.
- `retained_logos`: Count of logos still `active` (or `paused`) in `months_since_signup`.
- `retention_pct`: `retained_logos / original_cohort_size`.
- `churned_logos`: Count of logos that moved to `status = 'churned'` within that specific month.

## The "Free-to-Paid" Blocker

We are currently blocked on how to define the "Signup Month" for customers who start on the Free tier.

- **Option A (Product View)**: Use `dim_customers.signup_date`. This tracks the user from the moment they touch the product.
- **Option B (Finance View)**: Use the `start_date` of the first non-Free subscription in `fact_subscriptions`. 

**@dan.lee's take**: We should use Option A but include a flag `is_paid_at_signup`. If we only track from the first paid date, we lose the visibility into the PLG funnel "lag" (the time it takes a Free user to become a Pro/Business user). 

**@rachel.stein's take (via Slack)**: Finance needs the paid-date cohort for NRR alignment. If a customer stays Free for 6 months and then pays, they shouldn't "penalize" the 6-month-old cohort's retention before they even contributed ARR.

> 🚧 `// TODO: Schedule sync with @lina.cho and @jorge.martinez to finalize the "Cohort Zero" definition. -dan 2026-04-20`

## Technical Implementation (Consulted with @david.kim)

Because this requires a cross-join between `dim_customers` and `dim_dates` (to create the "triangle" rows for every month since signup), @david.kim recommends:

1. **Materialization**: `table` (incremental is too complex for the triangle logic).
2. **Logic**:
   - CTE 1: `cohort_definitions` (Customer ID + Signup Month).
   - CTE 2: `month_spine` (All months from 2023-01 to current).
   - CTE 3: `customer_activity_by_month` (Joining `fact_subscriptions` to see if a sub was active in a given month).
3. **Performance**: With ~800 total customers, the resulting table will be ~20k rows. BQ handles this easily without partitioning.

## Proposed SQL Snippet (WIP)

```sql
WITH cohort_base AS (
  SELECT 
    customer_id,
    DATE_TRUNC(signup_date, MONTH) AS cohort_month,
    account_tier
  FROM {{ ref('dim_customers') }}
),
month_spine AS (
  SELECT DISTINCT DATE_TRUNC(date, MONTH) AS activity_month
  FROM {{ ref('dim_dates') }}
  WHERE date <= CURRENT_DATE()
),
retention_calc AS (
  SELECT
    c.cohort_month,
    s.activity_month,
    DATE_DIFF(s.activity_month, c.cohort_month, MONTH) AS months_since_signup,
    COUNT(DISTINCT c.customer_id) AS retained_logos
  FROM cohort_base c
  JOIN month_spine s ON s.activity_month >= c.cohort_month
  LEFT JOIN {{ ref('fact_subscriptions') }} sub 
    ON c.customer_id = sub.customer_id
    AND s.activity_month BETWEEN DATE_TRUNC(sub.start_date, MONTH) 
    AND COALESCE(DATE_TRUNC(sub.end_date, MONTH), CURRENT_DATE())
  WHERE sub.plan_tier != 'Free' -- The contentious filter
  GROUP BY 1, 2, 3
)
-- ... final logic to join back to cohort totals
```

## Related Docs
- `schema__overview.md` — for `dim_customers` and `fact_subscriptions` fields.
- `glossary__logo_churn.md` — for alignment on what constitutes a "churned" event.
- `notion__data-warehouse-conventions.md` — for date truncation standards.

## Discussion Thread

**@david.kim (2026-04-18)**: "The `LEFT JOIN` to `fact_subscriptions` inside a spine is going to be the main cost driver. If we ever scale to 10k+ customers, we'll need to move this to a nested structure or pre-aggregate the subscription spans."

**@dan.lee (2026-04-19)**: "Understood. For the current 800 customers, let's keep it readable. I'll add the `is_paid_at_signup` flag once we resolve the definition with @lina.cho."

**@elena.volkov (2026-04-21)**: "This will be huge for CS. If we can see that the 'Oct 2025' cohort has a Month-3 retention of 70% while the 'Oct 2024' cohort was 90%, we can pinpoint exactly when the onboarding friction started."
