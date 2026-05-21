---
title: "Notion — QBR template (CSM-driven)"
source_url: "internal://acme/notion/qbr-template"
license: "synthetic-demo"
attribution: "Acme Inc internal CSM resources (synthetic demo). Owner: Elena Volkov (VP CS)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: notion_runbook
---

# QBR Template — CSM internal reference

> **Last reviewed**: 2026-02-12 by elena.volkov
> **Owner**: Elena Volkov (VP CS)
> **Audience**: All CSMs (emp_400-series), Sales AEs
>
> 🚧 `// TODO: update the "Usage Review" section once the value-realization-score model ships. for now, continue using the engaged-customer binary flag. -elena 2026-04-15`

This template is the canonical structure for Quarterly Business Reviews (QBRs) at Acme. Every Business and Enterprise account should have a QBR once per quarter. For SMB accounts, this is optional but recommended for high-growth potential logos.

## Prep checklist (T-minus 24 hours)

Before the call, the CSM must review the following in the warehouse/Looker:
- [ ] **Usage Data**: Pull trailing 90-day `total_runs` and `success_rate` from `marts/product/workflow_runs_daily`.
- [ ] **Account Health**: Verify current `account_health_status` in `dbt__model__account_health.md`.
- [ ] **Support Tickets**: Check `fact_support_tickets` for any open P1s or a high volume of `integration` category bugs.
- [ ] **NPS Trend**: Review `fact_nps_responses` for the last two quarters. If there is a detractor score, be prepared to address the specific comment.
- [ ] **Champion Check**: Confirm the primary admin/champion has logged in within the last 14 days via `dim_users.last_login_date`.

---

# [Customer Name] — Q1 2026 Business Review

**Date**: [Date]
**Acme Attendees**: [CSM Name], [AE Name]
**Customer Attendees**: [Champion Name], [Executive Sponsor], [Primary Builder]

## 1. Executive summary
*High-level recap of the partnership status. Focus on value realized since the last review.*

- **Current Plan**: [e.g., Business]
- **Current ARR**: [Use `fact_subscriptions.mrr_usd * 12`]
- **Key Objective**: [e.g., Automating lead routing from Salesforce to Slack]

## 2. Usage & performance review
*Data sourced from `fact_workflow_runs` and `fact_user_events`.*

- **Total Workflow Runs (Last 90 Days)**: [Count]
- **Success Rate**: [%] — *Note: If <98%, highlight specific `error_code` trends (e.g., `AUTH_FAILED` on the Jira integration).*
- **Top 3 Use Cases**:
  1. [Workflow Name] — [X] runs/mo
  2. [Workflow Name] — [Y] runs/mo
  3. [Workflow Name] — [Z] runs/mo
- **Seat Utilization**: [Active Users / Paid Seats] — *Reference `glossary__seat_utilization.md` bands.*

## 3. Success metrics (Customer-defined KPIs)
*What did the customer say they wanted to achieve during onboarding?*

- **KPI 1**: [e.g., Reduction in manual data entry time] — **Status**: [On Track / At Risk]
- **KPI 2**: [e.g., 100% coverage of GitHub-to-Notion sync] — **Status**: [Achieved]

## 4. Account health & support snapshot
- **Health Status**: [e.g., Healthy / Monitoring]
- **Support Volume**: [N] tickets in Q1.
- **CSAT Average**: [Score 1-5]
- **Recent Feedback**: [Quote from most recent NPS response in `fact_nps_responses`]

## 5. Product roadmap & asks
- **Customer Feature Requests**: [List any specific `feature_request` category tickets]
- **Acme Roadmap Alignment**: Highlight upcoming releases (e.g., AI Workflow Assistant beta) that match their use cases.

## 6. Renewal & expansion (if within 6 months)
- **Renewal Date**: [Date from `fact_subscriptions.end_date`]
- **Expansion Opportunity**: [e.g., Adding 50 seats for the EMEA Marketing team]
- **Renewal Sentiment**: [Commit / Best Case / Pipeline / Omitted]

---

## Example QBRs for reference

- **Enterprise Example**: `gong__qbr__cust000412-q1-review.md` (Drag Industries). Note how @marco.chen handled the discussion around the 0.14 utilization rate by pivoting to the new custom 30-seat Business package.
- **Expansion Example**: `gong__renewal__halcyon-research.md` (cust_000087). Good example of using high utilization (0.80+) to drive a 2-year multi-year commit.

## Comments / Change history

> **2026-02-12** — `elena.volkov`: Added the "Prep checklist" section to ensure CSMs aren't surprised by NPS detractor comments mid-call.
>
> **2025-11-05** — `marco.chen`: Added the "Success Metrics" section. We were focusing too much on our internal usage data and not enough on what the customer actually cares about.
>
> **2025-08-20** — `elena.volkov`: Initial template release. Mandatory for all Business+ accounts.
