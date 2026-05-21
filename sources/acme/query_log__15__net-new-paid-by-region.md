---
title: "Query log — Q1 2026 net new paid logos by region"
source_url: "internal://acme/query-log/15"
license: "synthetic-demo"
attribution: "Acme Inc internal query log (synthetic demo). Author: Lina Cho (FP&A)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: query_log
---

# Query log — Q1 2026 net new paid logos by region

**Author**: @lina.cho (FP&A)
**Date**: 2026-04-05
**Stakeholder**: @rachel.stein (CFO)
**Purpose**: Reconciling the Q1 2026 board deck "Logo Growth" slide. We needed a clean breakdown of net new paid logos (New - Churn) segmented by region to see if the EMEA sales push in February moved the needle.

## Context & Caveats

- **Region Source**: Region is pulled from `dim_customers.region`. Note that this is a self-reported field from the onboarding flow or manually set by AEs in Salesforce. It is NOT currently normalized by IP/Geolocation (that's a 2026-H2 data quality project).
- **Net New Definition**: (Count of customers who became paid in Q1) - (Count of customers who churned in Q1).
- **Paid Definition**: Per `glossary__paid_customer.md`, this excludes 'Free' tier.
- **Cross-reference**: For the total ARR contribution of these regions (as opposed to just logo counts), see `query_log__01__arr-by-region.md`.

## SQL

```sql
/* 
   Q1 2026 Net New Paid Logos by Region
   Author: @lina.cho
*/

WITH q1_starts AS (
    -- New paid logos acquired in Q1
    SELECT 
        c.region,
        COUNT(DISTINCT s.customer_id) AS new_logos
    FROM `nexus-analyst-demo.acme.fact_subscriptions` s
    JOIN `nexus-analyst-demo.acme.dim_customers` c USING (customer_id)
    WHERE s.change_type = 'new'
      AND s.plan_tier != 'Free'
      AND s.start_date BETWEEN '2026-01-01' AND '2026-03-31'
    GROUP BY 1
),

q1_churns AS (
    -- Paid logos lost in Q1
    -- We filter for plan_tier != 'Free' on the *previous* sub to ensure
    -- we are only counting paid-to-churn transitions.
    SELECT 
        c.region,
        COUNT(DISTINCT s.customer_id) AS churned_logos
    FROM `nexus-analyst-demo.acme.fact_subscriptions` s
    JOIN `nexus-analyst-demo.acme.dim_customers` c USING (customer_id)
    JOIN `nexus-analyst-demo.acme.fact_subscriptions` prev 
      ON s.changed_from_subscription_id = prev.subscription_id
    WHERE s.change_type = 'churn'
      AND prev.plan_tier != 'Free'
      AND s.start_date BETWEEN '2026-01-01' AND '2026-03-31'
    GROUP BY 1
)

SELECT 
    COALESCE(n.region, c.region, 'Unknown') AS region,
    COALESCE(n.new_logos, 0) AS new_paid_logos,
    COALESCE(c.churned_logos, 0) AS churned_paid_logos,
    COALESCE(n.new_logos, 0) - COALESCE(c.churned_logos, 0) AS net_new_logos
FROM q1_starts n
FULL OUTER JOIN q1_churns c USING (region)
ORDER BY net_new_logos DESC;
```

## Results (Snapshot)

| region | new_paid_logos | churned_paid_logos | net_new_logos |
|---|---|---|---|
| NA | 42 | 8 | 34 |
| EMEA | 19 | 3 | 16 |
| APAC | 7 | 2 | 5 |
| LATAM | 2 | 1 | 1 |

## Observations

- **EMEA Momentum**: The EMEA region showed strong resilience with only 3 churns against 19 new logos. This aligns with the high-touch CSM pilot @elena.volkov ran in Amsterdam this quarter.
- **NA Dominance**: North America remains the primary driver of logo growth, contributing ~60% of net new logos.
- **LATAM/APAC**: These remain "emerging" for us. @marcus.webb mentioned we don't have dedicated AEs for LATAM yet, which explains the low volume.
- **Data Hygiene**: We had 0 'Unknown' regions in this run, which suggests the new validation rule in Salesforce is working.

## Slack Thread Summary

**#finance-internal** (2026-04-05)

> **lina.cho**: Just finished the Q1 regional logo reconciliation. NA: +34, EMEA: +16. EMEA churn was surprisingly low.
> **rachel.stein**: Nice. Does the EMEA count include the Drag Industries expansion?
> **lina.cho**: No, Drag Industries (`cust_000412`) was an expansion, not a "New" logo, so it's excluded from this count but shows up in the ARR delta in `query_log__01__arr-by-region.md`.
> **marcus.webb**: 16 net new for EMEA is a record. @elena.volkov the renewal work there is paying off. 🚀
