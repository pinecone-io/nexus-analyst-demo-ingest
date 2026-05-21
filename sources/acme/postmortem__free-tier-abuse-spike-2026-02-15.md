---
title: "Postmortem — Free tier abuse spike 2026-02-15"
source_url: "internal://acme/postmortem/free-tier-abuse-spike-2026-02-15"
license: "synthetic-demo"
attribution: "Acme Inc internal postmortem (synthetic demo). Owner: Dan Lee (Product)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: postmortem
---

# Postmortem — Free tier abuse spike 2026-02-15

**Status**: Completed
**Owner**: @dan.lee (Product)
**Engineers involved**: @hannah.miles, @tomas.vega
**Stakeholders**: @priya.anand (VP Eng), @rachel.stein (CFO)
**Incident Date**: 2026-02-15

## Summary
Between 02:15 UTC and 09:40 UTC on 2026-02-15, a single bad actor bypassed our standard signup friction to create 82 "Free" tier accounts. These accounts were used to execute high-volume web-scraping workflows targeting a specific set of e-commerce domains. The activity was detected by a threshold alert on `marts/product/workflow_runs_daily`. Total infrastructure cost impact is estimated at ~$3,100. No paid customer workflows were delayed or impacted.

## Timeline (all times UTC)
- **02:15**: First batch of accounts (15) created from IP range `185.212.xx.xx`.
- **04:30**: Automated workflows begin execution across all 82 accounts simultaneously.
- **07:00**: `dbt` nightly run completes; `marts/product/workflow_runs_daily` refreshes.
- **07:15**: Alert fires in `#product-alerts`: `total_runs` for Free tier exceeds 3x rolling 7-day mean.
- **07:45**: @dan.lee triages the alert and identifies the cluster of new accounts with identical naming patterns (`bot_user_01@...` through `bot_user_82@...`).
- **08:10**: @hannah.miles confirms the workflows are high-concurrency HTTP requests (scraping).
- **08:45**: @tomas.vega implements a temporary IP block on the `185.212.xx.xx` range at the gateway.
- **09:40**: All active runs for the identified accounts are killed; accounts are moved to `status = 'paused'`.
- **11:00**: Incident declared resolved.

## Detection
The incident was detected via the `total_runs` metric in `dbt__model__workflow_runs_daily.md`. Because Free tier accounts are capped at 100 runs/month per account (see `notion__pricing-tiers.md`), a sudden spike in aggregate Free tier volume is almost always a sign of multi-account sybil attacks.

## Impact
- **Financial**: ~$3,100 in incremental egress and compute costs (Lambda/Fargate).
- **Operational**: ~4 hours of engineering time for triage and mitigation.
- **Customer**: Zero impact to paid tiers (Business/Enterprise). Our multi-tenant scheduler correctly prioritized paid queues.

## Root Cause
Our signup flow lacked a "velocity throttle" for multiple signups from the same IP range within a short window. While we use Google OAuth as an option, we still allow email/password signups for Free tier to reduce friction. The attacker used a headless browser to automate the email verification step.

## Lessons Learned
1. **Thresholds work**: The 100-run quota on Free tier is an effective "circuit breaker" for individual accounts, but we lacked a global "new account" execution throttle.
2. **Data lag**: Because we rely on the nightly dbt refresh for `workflow_runs_daily`, we had a ~5-hour detection lag. 
3. **Infrastructure Isolation**: Our decision to isolate Free tier execution to a specific sub-cluster (implemented Q3 2025) prevented this spike from causing "noisy neighbor" issues for Business tier customers like `cust_000412`.

## Action Items
| Task | Owner | Status |
|---|---|---|
| Implement IP-based signup throttling (max 3/hour) | @tomas.vega | Completed (2026-02-18) |
| Add `is_flagged_for_abuse` boolean to `dim_customers` | @dan.lee | In Progress |
| Move Free-tier aggregate run alerts to a 15-minute Real-time Lambda | @hannah.miles | Planned (Q2) |
| Review Free tier email verification requirements | @dan.lee | Completed |

## Related Documents
- `notion__free-tier-policy.md` (Internal policy on abuse and quotas)
- `dbt__model__workflow_runs_daily.md` (The detection source)
- `schema__overview.md` (Reference for `dim_customers` status fields)

## Slack Thread Archive
> **07:20 @dan.lee**: Looking at the `#product-alerts` spike. We have 82 new accounts all running 100/100 runs within 2 hours. Definitely a botnet.
> **07:46 @hannah.miles**: Verified. They're all hitting the same Shopify endpoints. It’s a distributed scrape.
> **08:50 @tomas.vega**: IP range blocked. Killing the worker processes now.
> **10:15 @priya.anand**: Good catch on the dbt alert. @dan.lee let's make sure we didn't bill any of these "users" — @rachel.stein needs a clean report for the board on "Real" vs "Abuse" signups for Feb.
