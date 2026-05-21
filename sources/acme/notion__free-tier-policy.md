---
title: "Notion — Free tier policy & abuse handling"
source_url: "internal://acme/notion/free-tier-policy"
license: "synthetic-demo"
attribution: "Acme Inc internal policy (synthetic demo). Owner: Dan Lee (Product)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: notion_doc
---

# Free tier policy & abuse handling

> **Last reviewed**: 2026-02-04 by dan.lee
> **Owner**: Dan Lee (Product)
> **Stakeholders**: Engineering, CS, Finance
> **Status**: Active

This document outlines the operational policy for Acme’s Free tier, including hard limits, support exclusions, and the automated mechanisms we use to mitigate platform abuse. 

## Free Tier Specifications

The Free tier is intended as a "sandbox for builders" and a PLG (Product-Led Growth) entry point. It is not designed for production-critical enterprise workloads.

| Feature | Limit / Policy |
|---|---|
| **Monthly Run Quota** | 100 successful runs per account (shared across all workflows) |
| **Active Workflows** | Max 2 active (enabled) workflows |
| **SLA** | None. Free tier runs on a lower-priority "best effort" execution queue. |
| **Support** | Community-only. No email or live chat support. |
| **SSO / SAML** | Excluded. Google OAuth and email/pass only. |
| **Audit Logs** | Not available. |

> **Note from dan.lee**: We do not currently hard-delete data for Free users who exceed the 100-run quota; we simply pause their workflows until the next billing cycle. This has led to some friction in `#support-tickets`, but the policy remains: Free is self-serve only.

## Conversion Targets

We track Free-to-Paid conversion as a primary product KPI. 
- **Target Conversion Rate**: 4.5% within 90 days of signup.
- **Current Performance**: ~3.8% (as of 2026-Q1). 
- **Reference**: See `slack__data-help__free-to-paid-conversion-window.md` for the cohort analysis on conversion velocity.

## Abuse Patterns & Detection

As Acme has grown, we have identified a significant volume of "quota dodging"—users creating multiple Free accounts to bypass the 100-run limit or the 2-workflow cap.

### 1. Multi-Account Abuse
Users register multiple accounts (e.g., `user+1@gmail.com`, `user+2@gmail.com`) to run distributed workloads. 
- **Detection Signal**: We monitor `fact_workflow_runs` for clusters of activity originating from the same IP block or fingerprint.
- **Threshold**: Any single IP block showing `>10x` the median daily activity of the Free tier population is flagged for manual review by @tomas.vega.

### 2. Execution Spikes
Occasionally, Free users attempt to use Acme for high-frequency polling (e.g., checking a site every 1 second). 
- **Policy**: Our system triggers an auto-kill if a Free workflow exceeds 50 runs in a 60-minute window, even if they are under the 100-run monthly cap. This protects the execution engine from "noisy neighbor" performance degradation.

## Abuse Mitigation Workflow

When an account is flagged by the `dbt__model__workflow_runs_daily.md` anomaly detector:

1. **Auto-Flag**: The account status in `dim_customers` is updated to `flagged_abuse`.
2. **Execution Throttling**: The workflow runner moves these accounts to the `quarantine` queue (max 1 concurrent execution).
3. **Notification**: The user receives an automated "Usage Limit Warning" email suggesting an upgrade to Pro.
4. **Hard Block**: If a user creates >5 accounts from the same verified domain/IP within 24 hours, the domain is blacklisted from the signup flow.

## Data Warehouse Monitoring

To audit Free tier abuse or conversion, use the following logic:

```sql
-- Identify Free users approaching or exceeding quotas
SELECT 
  c.customer_id,
  c.company_name,
  w.total_runs,
  w.success_rate
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.marts.product.workflow_runs_daily` w 
  ON c.customer_id = w.customer_id
WHERE c.current_plan_tier = 'Free'
  AND w.run_date = CURRENT_DATE()
  AND w.total_runs > 80; -- Warning threshold
```

## Related Documents
- `notion__pricing-tiers.md` — Comparison of Free vs. Paid features.
- `glossary__paid_customer.md` — Definition of what constitutes a conversion.
- `dbt__model__workflow_runs_daily.md` — The source for execution volume monitoring.

## Change History

| Date | Change | Author |
|---|---|---|
| 2026-02-04 | Added 50-run/hour burst limit for Free tier. | @dan.lee |
| 2025-11-12 | Formalized IP-block abuse detection threshold (10x median). | @tomas.vega |
| 2025-08-30 | Updated conversion target from 4.0% to 4.5%. | @dan.lee |
| 2025-01-10 | Initial policy draft. | @dan.lee |

> **Comment from priya.anand (2026-02-05)**: @dan.lee, we should ensure the "quarantine" queue doesn't accidentally pick up Pro users during high-load events. Can we add a check for `plan_tier != 'Free'` in the runner's priority logic?
> 
> **Reply from dan.lee (2026-02-05)**: Already in there, @priya.anand. The priority queue explicitly checks `dim_plans.plan_tier` before routing.
