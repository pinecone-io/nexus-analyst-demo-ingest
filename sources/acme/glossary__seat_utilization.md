---
title: "Glossary — Seat utilization"
source_url: "internal://acme/glossary/seat-utilization"
license: "synthetic-demo"
attribution: "Acme Inc internal metric definitions (synthetic demo). Owned by Product (emp_050) and CS (emp_040)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: glossary
---

# Seat utilization

**One-line definition.** The fraction of paid seats a customer is actually using. Used as a leading indicator of churn risk for Pro and Business accounts.

```
seat_utilization = active_users_in_28d / seat_count_on_current_subscription
```

## Canonical SQL

```sql
WITH paid AS (
  SELECT customer_id, seat_count
  FROM `nexus-analyst-demo.acme.fact_subscriptions`
  WHERE is_current = TRUE AND plan_tier != 'Free'
),
active AS (
  SELECT customer_id, COUNT(DISTINCT user_id) AS n_active_users
  FROM `nexus-analyst-demo.acme.fact_user_events`
  WHERE event_name = 'login'
    AND event_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 28 DAY)
  GROUP BY customer_id
)
SELECT
  p.customer_id,
  p.seat_count,
  COALESCE(a.n_active_users, 0) AS active_users_28d,
  SAFE_DIVIDE(COALESCE(a.n_active_users, 0), p.seat_count) AS utilization
FROM paid p
LEFT JOIN active a USING (customer_id);
```

## Bands

| Utilization | Health |
|---|---|
| ≥ 0.80 | Healthy — likely candidate for **expansion** (more seats) |
| 0.50 – 0.79 | Stable |
| 0.20 – 0.49 | At risk — CSM outreach |
| < 0.20 | Critical — likely **downgrade or churn** at renewal |

## Why this matters more for Pro than Business

Pro customers are billed per-seat and self-serve. If they bought 8 seats but only 2 are active, they're paying for 6 dormant seats and will downgrade or churn at renewal.

Business is similar but with the `min_seats = 50` floor — customers can't downgrade below 50 seats without dropping to Pro entirely. So under-utilization on Business often manifests as a hard downgrade, not a seat reduction.

## Don't apply to Enterprise

Enterprise contracts have unlimited seats negotiated up front; seat utilization is a misleading metric there. Use **engaged customer** + **NPS** + qualitative CSM signals instead.

## Related dashboards

- Looker: `Account Health — SMB & MM` (built off `dbt/models/marts/cs/account_health.sql`)
- Slack alert: posts to `#cs-at-risk` daily for any account with utilization <0.20 for 14+ days.
