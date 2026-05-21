---
title: "Saved query — Workflow error-rate trend (last 90d) — for eng monthly"
source_url: "internal://acme/query_log/2026-04-28-error-rate-trend"
license: "synthetic-demo"
attribution: "Acme Inc analyst saved-query log (synthetic demo)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: query_log
---

# Saved query — Workflow error-rate trending (last 90d)

**Asker**: @priya.anand (VP Engineering)
**Author**: @hannah.miles (Sr Engineer)
**Run on**: 2026-04-28 16:30 UTC

## SQL

```sql
-- Daily error-rate trend by error code, for the eng monthly review
SELECT
  DATE(triggered_at) AS run_date,
  COUNT(*) AS total_runs,
  SUM(IF(status = 'success', 1, 0)) AS success,
  SUM(IF(status != 'success', 1, 0)) AS errors,
  ROUND(SAFE_DIVIDE(SUM(IF(status != 'success', 1, 0)), COUNT(*)) * 100, 3) AS error_rate_pct,
  COUNTIF(error_code = 'AUTH_FAILED') AS auth_failed,
  COUNTIF(error_code = 'RATE_LIMITED') AS rate_limited,
  COUNTIF(error_code = 'STEP_TIMEOUT') AS step_timeout,
  COUNTIF(error_code = 'INTEGRATION_DOWN') AS integration_down,
  COUNTIF(error_code = 'USER_ERROR') AS user_error,
  COUNTIF(error_code = 'VALIDATION_ERROR') AS validation_error
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE triggered_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
GROUP BY run_date
ORDER BY run_date;
```

## Notes

- Daily granularity, ordered by date.
- `STEP_TIMEOUT` and `INTEGRATION_DOWN` are upstream-driven (third-party API issues). Spikes there don't reflect Acme runtime quality.
- `AUTH_FAILED` is usually a customer-side problem (expired token). High counts can correlate with customer outreach opportunities.
- `USER_ERROR` is misconfigured workflow (customer's fault, not ours).
- `VALIDATION_ERROR` is a newer code (added 2026-04-22) — represents workflow validation failures pre-execution. Not in old data.

> hannah's note: "alex tried to use this query for an SLO dashboard a few weeks ago. it doesn't quite work for that — for SLOs we exclude upstream-driven codes (STEP_TIMEOUT, INTEGRATION_DOWN). that filter version lives in `slo_workflow_runtime.sql`."

## Read

- Platform error rate hovers ~5-7% baseline.
- Spikes correlate with named integration outages (Salesforce in April, see `slack__engineering__workflow-duration-spike.md`).
- We track a separate "Acme-attributable error rate" that excludes upstream-driven codes — that's the SRE dashboard, lives in Datadog.

## Reused by

- Engineering monthly review
- SRE dashboard data feed (Datadog)
- Random "is the platform OK today?" Slack questions in #engineering
