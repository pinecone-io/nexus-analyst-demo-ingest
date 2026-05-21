---
title: "Glossary — Cohort"
source_url: "internal://acme/glossary/cohort"
license: "synthetic-demo"
attribution: "Acme Inc internal metric definitions (synthetic demo). Owned by Product Analytics (emp_050)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: glossary
---

# Cohort

**One-line definition.** A group of customers who share a common starting event within a specific time window, typically defined by their `signup_date` month or quarter.

At Acme, we use cohorts primarily to measure **retention** (how long they stay) and **expansion** (how their MRR grows over time) without the "noise" of new customer acquisition masking the behavior of older accounts.

## Canonical SQL (Monthly Signup Cohorts)

To group customers into monthly signup cohorts for a retention analysis:

```sql
SELECT
  FORMAT_DATE('%Y-%m', signup_date) AS signup_cohort,
  COUNT(DISTINCT customer_id) AS cohort_size,
  SUM(current_mrr_usd) AS total_current_mrr
FROM `nexus-analyst-demo.acme.dim_customers`
GROUP BY 1
ORDER BY 1 DESC;
```

## Cohort vs. Segment

It is a common mistake in `#data-help` to use these terms interchangeably. At Acme, we maintain a strict distinction:

*   **Cohort**: Time-based grouping. Defined by *when* a customer joined. (e.g., "The Jan 2024 Cohort"). Used for lifecycle analysis and NRR.
*   **Segment**: Attribute-based grouping. Defined by *who* the customer is or *what* they do. (e.g., "The Enterprise Segment" or "The SaaS Industry Segment"). See `notion__customer-segmentation.md`.

## Usage in Analytics

1.  **Retention Curves**: We track the percentage of a cohort that remains `active` at Month 1, Month 3, Month 12, etc.
2.  **NRR (Net Revenue Retention)**: Our canonical NRR calculation is always cohorted by the starting period to ensure we are comparing apples to apples. See `glossary__nrr.md`.
3.  **Feature Adoption**: Product team uses cohorts to see if customers who signed up *after* the launch of the "AI Workflow Assistant" (beta) have higher engagement than those who signed up before.

## Important Nuances

*   **Fixed Membership**: Once a customer is assigned to the `2024-03` cohort, they never leave it, even if they upgrade from Pro to Enterprise or change industries. 
*   **The "Signup" Definition**: For the warehouse, `signup_date` in `dim_customers` refers to the date the first user was created for that `customer_id`, regardless of whether they started on a Free or Paid plan.
*   **Cohort Drift**: Be careful when analyzing cohorts that are less than 30 days old, as their "Day 30 Retention" is not yet mathematically possible to calculate.

## Related Documentation

*   `notion__draft__cohort-retention-spec.md` — Detailed spec for the upcoming automated retention dashboard.
*   `notion__customer-segmentation.md` — Contrast between time-based cohorts and attribute-based segments.
*   `glossary__nrr.md` — How we apply cohorts to revenue metrics.

**Owner**: @dan.lee  
**Last Reviewed**: 2026-04-18
