---
title: "Glossary — Engaged customer"
source_url: "internal://acme/glossary/engaged-customer"
license: "synthetic-demo"
attribution: "Acme Inc internal metric definitions (synthetic demo). Owned by CS (emp_040)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: glossary
---

# Engaged customer

**One-line definition.** A paid customer with both **≥3 active users** and **≥10 successful workflow runs** in the trailing 28 days.

This is Acme's product-led health signal. CS uses it as the primary input to renewal forecasting for SMB / MM accounts (Enterprise has dedicated CSM scoring; see `notion__csm-account-health-runbook.md`).

## Canonical SQL

```sql
WITH paid AS (
  SELECT DISTINCT customer_id
  FROM `nexus-analyst-demo.acme.fact_subscriptions`
  WHERE is_current = TRUE AND plan_tier != 'Free'
),
active_users AS (
  SELECT customer_id, COUNT(DISTINCT user_id) AS n_active_users
  FROM `nexus-analyst-demo.acme.fact_user_events`
  WHERE event_name = 'login'
    AND event_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 28 DAY)
  GROUP BY customer_id
),
runs AS (
  SELECT customer_id, COUNT(*) AS n_successful_runs
  FROM `nexus-analyst-demo.acme.fact_workflow_runs`
  WHERE status = 'success'
    AND triggered_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 28 DAY)
  GROUP BY customer_id
)
SELECT p.customer_id
FROM paid p
LEFT JOIN active_users au USING (customer_id)
LEFT JOIN runs r USING (customer_id)
WHERE COALESCE(au.n_active_users, 0) >= 3
  AND COALESCE(r.n_successful_runs, 0) >= 10;
```

## Threshold history

The thresholds (3 users, 10 runs, 28d window) were set in 2024-Q3 based on a logistic regression where the dependent variable was "renewed at end of contract". Above these levels, renewal probability rose from ~70% baseline to ~92%. The thresholds are reviewed quarterly. See `postmortem__engagement-threshold-recalibration-2025-Q4.md`.

## "At-risk" — the inverse

A paid customer is "at risk" if they fail either condition. These customers get auto-routed into the CSM health board:

- 0 active users in 28 days → "ghost"
- 0 successful runs in 28 days → "configured but not running"
- <3 users AND <10 runs → "low utilization"

CS goal: contact every at-risk MM/Ent within 5 business days.

## Don't conflate with NRR

A paid customer can be "engaged" by these thresholds and still downgrade. Engagement predicts renewal probability, not expansion. NRR uses dollar movement, not engagement signals.
