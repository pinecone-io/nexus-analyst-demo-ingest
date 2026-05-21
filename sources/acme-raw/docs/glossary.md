# Acme metric glossary (messy, maintained ad hoc)

**Paid customer** — a customer with a current subscription on a non-Free plan, i.e.
`fact_subscriptions` filtered to `is_current = TRUE AND plan_tier != 'Free'`. ~530 of the
~800 customers are paid.

**Engaged customer** — >=3 active users AND >=10 successful workflow runs in the trailing
28 days. Materialized as `account_health.is_engaged`.

**Logo churn vs revenue churn** — logo churn is customer-count based: COUNT(distinct churned
customers) / cohort size. Revenue churn is MRR-weighted: SUM(start_mrr of churned) /
SUM(start_mrr of cohort). Revenue churn feeds GRR; the loss is surfaced as
`nrr_trailing_12.churned_mrr_loss_usd`.

**Expansion MRR** — positive delta when a customer's current sub MRR exceeds their prior sub
MRR (same customer, linked via `changed_from_subscription_id`), summed over `upgrade` and
`seat_change` events. Surfaced as `nrr_trailing_12.expansion_mrr_usd`.

**NPS segments** — `fact_nps_responses.segment`: promoter (9-10), passive (7-8),
detractor (0-6). It is NOT a 0-100 scale. A detractor in the last 90d feeds
`account_health.has_recent_nps_detractor`.
