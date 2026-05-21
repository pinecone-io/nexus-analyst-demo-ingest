# CSM Account Health Runbook (canonical for CS triage)

Cadence: **Monday** — review the Looker "Account Health" board (built on the
`account_health` mart). Prioritize accounts that moved into the **critical** band since
last week.

Alerting: `#cs-at-risk` posts a digest **daily at 08:00 UTC** listing band changes.

Bands come from `account_health.account_health_status`
(critical / at_risk / monitoring / stable / healthy_expansion). Critical rules differ by
tier (see the account_health model / CS review call): Enterprise = recent uncollectible
invoice; non-Enterprise = uncollectible OR seat utilization < 0.20.

If a customer has an open P1 > 48h (`has_open_p1_over_48h`) or a recent NPS detractor,
they surface as at_risk — reach out same day.
