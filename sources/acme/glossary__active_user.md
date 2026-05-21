---
title: "Glossary — Active user"
source_url: "internal://acme/glossary/active-user"
license: "synthetic-demo"
attribution: "Acme Inc internal metric definitions (synthetic demo). Owned by Product (emp_050)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: glossary
---

# Active user

**One-line definition.** A user is "active" if they have a `login` event in `fact_user_events` within the trailing 28 days.

**Canonical SQL.**

```sql
SELECT DISTINCT user_id
FROM `nexus-analyst-demo.acme.fact_user_events`
WHERE event_name = 'login'
  AND event_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 28 DAY);
```

## Why 28 days, not 30?

We use 28 days because (a) it aligns with Acme's product analytics standard (avoids weekday seasonality issues that 30-day windows have) and (b) it's how every PM dashboards engagement. Do not use 30 unless someone has explicitly asked for it.

## Why not use `dim_users.is_active`?

`dim_users.is_active` is computed nightly during the warehouse build. It uses **`last_login_date`**, which is a denormalized field also derived from `fact_user_events`. The convenience field is fine for low-stakes filters (e.g. "list all admins who are still around"). For metric reporting (WAU, engagement rate, conversion funnels), recompute from `fact_user_events` to avoid clock-skew between dim and fact.

## DAU / WAU / MAU

| Metric | Window |
|---|---|
| **DAU** | login event in trailing 1 day |
| **WAU** | login event in trailing 7 days |
| **MAU** | login event in trailing 28 days (== "active user") |

```sql
WITH events AS (
  SELECT user_id, event_at
  FROM `nexus-analyst-demo.acme.fact_user_events`
  WHERE event_name = 'login'
    AND event_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 28 DAY)
)
SELECT
  COUNT(DISTINCT IF(event_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY), user_id, NULL)) AS dau,
  COUNT(DISTINCT IF(event_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY), user_id, NULL)) AS wau,
  COUNT(DISTINCT user_id) AS mau
FROM events;
```

## Common mistake

Counting `dim_users.is_active = TRUE` and reporting it as "active users today" — that count reflects last night's snapshot, not today's traffic. Always use the fact table for time-windowed metrics.

## Headline (as of 2026-05-04)

~16K active users (28d) on a base of ~24K provisioned users.
