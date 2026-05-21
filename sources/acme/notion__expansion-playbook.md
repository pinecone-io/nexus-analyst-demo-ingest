---
title: "Notion — expansion playbook (Pro → Business upsell)"
source_url: "internal://acme/notion/sales/expansion-playbook"
license: "synthetic-demo"
attribution: "Acme Inc Sales Ops (synthetic demo). Owner: Jorge Martinez."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: notion_runbook
---

# Expansion playbook: Pro → Business upsell

> **Last updated**: 2026-03-12 by @jorge.martinez
> **Owner**: Sales Ops (@jorge.martinez)
> **Stakeholders**: Sales, Marketing, CS, Product
> **Status**: Active / Canonical

This playbook outlines the standardized process for identifying and closing upsell opportunities from the **Pro** tier to the **Business** tier. While Pro is largely self-serve, the transition to Business is AE-led and represents our most efficient path to increasing NRR.

## Why this matters
Business tier customers have a 3x higher ACV floor ($149/seat vs $49/seat) and significantly higher retention rates due to SSO and audit log dependencies. As of 2026-Q1, Business tier contributes ~$32M of our ~$39M total ARR.

## High-intent triggers
We use three primary data signals to route leads to AEs. These are refreshed nightly in the `expansion_candidates` dbt model.

### 1. Quota utilization (The "Wall")
*   **Signal**: Customer has hit ≥85% of their Pro workflow run quota (10,000 runs/month) for 3 consecutive months.
*   **Data Source**: `nexus-analyst-demo.acme.marts.product.workflow_runs_daily`
*   **Logic**:
    ```sql
    SELECT customer_id, SUM(total_runs) as monthly_runs
    FROM `nexus-analyst-demo.acme.marts.product.workflow_runs_daily`
    WHERE run_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
    GROUP BY 1, DATE_TRUNC(run_date, MONTH)
    HAVING monthly_runs >= 8500
    ```

### 2. Seat density
*   **Signal**: ≥4 active users in the last 28 days on a Pro plan.
*   **Data Source**: `dim_users` joined with `fact_user_events`.
*   **Context**: Once a team hits 4-5 active builders, the need for centralized management (SSO) and team-based RBAC becomes a friction point we can solve with Business.

### 3. Feature intent (Hand-raisers)
*   **Signal**: ≥1 "Enterprise feature" ask in the last 6 months.
*   **Indicators**:
    *   Support tickets categorized as `feature_request` mentioning "SAML", "SSO", "Audit Log", or "SCIM".
    *   `billing_viewed` events in `fact_user_events` followed by a click on the "Business" tier comparison.
    *   Direct pings in Slack Connect (if applicable).

## The Pitch: Value pillars
Refer to the [AE Pitch Template - Business Tier](internal://acme/sales/templates/business-pitch) for specific talk tracks. Key pillars from `notion__pricing-tiers.md`:

1.  **Scale**: Increase run quota from 10k to 100k/month.
2.  **Security**: SAML/OIDC SSO (the #1 closer for Pro accounts).
3.  **Governance**: 90-day audit logs and basic RBAC.
4.  **Support**: Priority email and live chat support.

## AE Workflow
1.  **Notification**: AE receives a Slack alert in `#sales-expansion-alerts` via the `acme-sales-bot`.
2.  **Discovery**: Review the customer's execution health in `marts/product/workflow_runs_daily`. Look for specific error codes like `RATE_LIMITED` which indicate they are outgrowing their current tier.
3.  **Outreach**: Use the "Quota Warning" or "Security Upgrade" email sequence in Outreach.
4.  **Opportunity Creation**: Create a New Business opportunity in Salesforce. Ensure `amount_usd` reflects the ACV (annualized). See `dbt__model__bookings_attribution.md` for how this maps to your quota.

## Gotchas & Guardrails
*   **Don't over-pitch mid-quota customers**: If a customer is at 50% quota and has 2 users, do not push Business. It creates "pricing fatigue" and increases churn risk.
*   **Watch for seasonality**: E-commerce customers (Industry: `E-commerce`) often spike in Q4. A 90% utilization in December might not be a permanent need for Business. Check the 3-month trend.
*   **The "SAML Trap"**: Many Pro customers ask for SSO but don't have 50 seats (our Business minimum). Per `notion__pricing-tiers.md`, you must escalate to @marcus.webb or @rachel.stein for any custom Business package below 50 seats.
*   **Attribution**: Ensure the `opportunity_id` is correctly linked to the `customer_id`. If the lead was originally sourced by an SDR, they get credit for the expansion per the 2026 comp plan.

## Performance tracking
We track the success of this playbook in the **Expansion ROAS** dashboard.
*   **Conversion Rate**: % of Pro accounts hitting trigger #1 that move to Business within 60 days.
*   **Expansion Velocity**: Average days from "Trigger Hit" to `Closed_Won`.
*   **Attributed Revenue**: Sum of `post_close_mrr_delta_vs_initial_usd` from `marts/sales/bookings_attribution`.

## Related documentation
*   `notion__pricing-tiers.md` — Current seat costs and plan limits.
*   `glossary__arr.md` — How we calculate the expansion credit.
*   `dbt__model__bookings_attribution.md` — Technical details on how won deals are logged.
*   `gong__discovery__cust000412-drag-industries.md` — Example of a successful Pro → Business negotiation.

## Comment thread
> **2026-03-12** — `@jorge.martinez`: Updated the quota trigger to 85% (was 90%) based on Q1 data showing 90% is often too late to prevent a "bad" customer experience.
>
> **2026-02-28** — `@marcus.webb`: AEs, please remember to check `fact_support_tickets` before reaching out. If they have an open P1, don't ask for more money until it's closed.
>
> **2026-01-15** — `@lina.cho`: Added the note about E-commerce seasonality. We saw too many "false positive" triggers during the holiday rush.
