---
title: "Query log — NRR Q1 2026 by plan tier"
source_url: "internal://acme/query-log/nrr-q1-2026-tier-breakdown"
license: "synthetic-demo"
attribution: "Acme Inc internal query log (synthetic demo). Author: Lina Cho (FP&A)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: query_log
---

# Query log — NRR Q1 2026 by plan tier

**Author**: @lina.cho
**Date**: 2026-04-12
**Context**: This is the exact SQL used to generate the tier-level NRR breakdown for the Q1 2026 Board Deck. It addresses the question raised in `slack__data-help__nrr-q1-breakdown-by-tier.md` regarding how we handle "graduation" (e.g., a customer who was Pro in Q1 2025 but is now Business in Q1 2026).

**Methodology Note**: Per our convention in `glossary__nrr.md`, the cohort is fixed based on the **starting** plan tier. If a customer upgrades from Pro to Business during the 12-month window, their expansion revenue contributes to the **Pro** NRR numerator. This reflects the "yield" of the Pro cohort.

```sql
/*
  NRR Q1 2026 Breakdown by Starting Plan Tier
  Window: 2025-03-31 to 2026-03-31 (Trailing 12 Months)
*/

DECLARE as_of_date DATE DEFAULT '2026-03-31';
DECLARE start_window DATE DEFAULT '2025-03-31';

WITH cohort_base AS (
  -- Identify the paid cohort as of the start of the TTM window
  -- We join to dim_customers only for the industry/region cuts if needed, 
  -- but fact_subscriptions is the source of truth for the tier.
  SELECT 
    s.customer_id,
    s.plan_tier AS starting_tier,
    s.mrr_usd AS starting_mrr
  FROM `nexus-analyst-demo.acme.fact_subscriptions` s
  WHERE s.start_date <= start_window
    AND (s.end_date IS NULL OR s.end_date > start_window)
    AND s.plan_tier != 'Free'
),

end_state AS (
  -- Identify the MRR for those same customers 12 months later
  SELECT 
    s.customer_id,
    s.plan_tier AS ending_tier,
    s.mrr_usd AS ending_mrr
  FROM `nexus-analyst-demo.acme.fact_subscriptions` s
  WHERE s.start_date <= as_of_date
    AND (s.end_date IS NULL OR s.end_date > as_of_date)
    AND s.is_current = TRUE -- Ensure we are looking at the active sub at end-of-period
),

joined_cohort AS (
  SELECT
    c.customer_id,
    c.starting_tier,
    c.starting_mrr,
    COALESCE(e.ending_mrr, 0) AS ending_mrr,
    e.ending_tier,
    -- Graduation flag for audit
    (c.starting_tier = 'Pro' AND e.ending_tier = 'Business') AS is_graduated_to_business,
    (c.starting_tier = 'Business' AND e.ending_tier = 'Enterprise') AS is_graduated_to_enterprise
  FROM cohort_base c
  LEFT JOIN end_state e USING (customer_id)
)

SELECT
  starting_tier,
  COUNT(DISTINCT customer_id) AS cohort_size,
  SUM(starting_mrr) AS starting_mrr_total,
  SUM(ending_mrr) AS ending_mrr_total,
  -- NRR Calculation
  SAFE_DIVIDE(SUM(ending_mrr), SUM(starting_mrr)) AS nrr,
  -- Audit metrics for the "Graduation Effect"
  COUNTIF(is_graduated_to_business) AS count_pro_to_biz,
  COUNTIF(is_graduated_to_enterprise) AS count_biz_to_ent,
  SUM(IF(is_graduated_to_business, ending_mrr - starting_mrr, 0)) AS expansion_from_graduation_usd
FROM joined_cohort
GROUP BY 1
ORDER BY nrr DESC;
```

### Key Findings from this Run

1.  **Business Tier Strength**: The Business tier continues to drive our highest NRR (~1.12). This is largely due to seat expansion within the mid-market segment (see `notion__csm-account-health-runbook.md` for the expansion triggers).
2.  **Pro Graduation**: Pro NRR looks artificially high (~1.08) because it includes 14 customers who "graduated" to Business. These 14 customers contributed roughly $22k in expansion MRR that is credited to the Pro cohort's retention.
3.  **Enterprise Volatility**: With a cohort size of only ~35 for this window, a single churn event (e.g., `cust_000219` in Feb) disproportionately impacts the percentage.

### Related Documentation
- `glossary__nrr.md` for the high-level definition.
- `dbt__model__nrr_trailing_12.md` for the automated daily rollup.
- `slack__data-help__nrr-q1-breakdown-by-tier.md` for the discussion thread regarding these results.
