---
title: "Notion runbook — CSM account-health playbook (with field notes)"
source_url: "internal://acme/notion/csm-account-health"
license: "synthetic-demo"
attribution: "Acme Inc Notion runbook (synthetic demo). Owner: VP CS (Elena Volkov)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: notion_runbook
---

# CSM account-health playbook

> **Last reviewed**: 2026-02-10 by elena.volkov
> **Owner**: Elena Volkov (VP CS)
> **Audience**: All CSMs (emp_400-series), CS Managers
>
> 🚧 `// TODO: this playbook predates the engaged-customer threshold review (Q4 2025 postmortem). thresholds didn't change but the framing in section "Action ladder" should be updated to reference the value-realization-score model when it ships in 2026-H1 -elena 2026-04-12`
>
> 🚧 `// TODO @marco: when you do the Drag Industries EBR write-up, can you link it as an example in the action-ladder section? -elena`

Acme uses two health signals for paid accounts: **Engaged Customer** flag + **Seat Utilization**. This playbook explains how each is computed, when CSMs should act on them, and what actions to take.

## Health signals

### Signal 1 — Engaged Customer flag

A boolean derived from `fact_user_events` and `fact_workflow_runs`. See `glossary__engaged_customer.md`. A paid customer is "engaged" if they have **≥3 active users in the last 28 days AND ≥10 successful workflow runs in the last 28 days**.

If `engaged = FALSE`, the account is at risk.

> **Inline note from rajiv.patel (2025-12-15)**: We sometimes see customers who are engaged by these thresholds but still showing intent-to-churn signals (e.g., champion left, EBR cancelled, billing-portal usage spike from procurement). Engagement floor != value realization. The 2026-H1 value-score model is supposed to fix this.

### Signal 2 — Seat Utilization

A ratio derived from active users / paid seats. See `glossary__seat_utilization.md`. Bands:

| Utilization | Health |
|---|---|
| ≥ 0.80 | **Healthy + expansion candidate** |
| 0.50 – 0.79 | **Stable** |
| 0.20 – 0.49 | **At risk — outreach** |
| < 0.20 | **Critical — likely downgrade or churn** |

> **Note**: Don't apply seat utilization to Enterprise accounts. Enterprise contracts have unlimited seats negotiated up front; seat utilization is a misleading metric there. Use engaged customer + NPS + qualitative CSM signals.

## CSM weekly cadence

Every Monday morning, CSMs review their assigned accounts in the **Account Health board** (Looker). The board surfaces:

1. Accounts moved into "critical" since last week (top priority)
2. Accounts in "at risk" for 14+ days (escalate)
3. Accounts in "healthy + expansion candidate" with no expansion conversation in 90 days (proactive expansion)
4. Accounts with NPS detractor responses in last 30 days (qualitative signal — not auto-detected, manual review)

> **2026-02-10 update**: We added #4 above after seeing a few accounts that were "engaged + healthy utilization" but had recent NPS detractor responses indicating churn intent. Manual review item.

## Action ladder

Move from light-touch to high-touch as risk increases.

### Critical (utilization <0.20 OR engaged=FALSE for 14+ days)

1. **Day 1**: CSM emails primary admin + primary builder.
2. **Day 5**: If no response, CSM offers a 30-min "workflow audit" call.
3. **Day 14**: If still no response or call yields no plan, escalate to VP CS for joint outreach with AE.
4. **Day 30**: If no engagement, mark in CRM as "consolidation risk" and notify AE for renewal-cycle pre-warning.

> **Example**: `cust_000412` Drag Industries — utilization 0.14 for 17+ days. Followed action ladder, EBR scheduled, custom 30-seat package being negotiated. See `gong__discovery__cust000412-drag-industries.md` for detail.

### At risk (utilization 0.20–0.49 for 14+ days)

1. **Within 5 business days**: CSM proactive check-in (email or Slack Connect).
2. **Within 30 days**: Joint review with the customer's primary admin.
3. **Action**: identify specific blockers — usually one of:
   - Champion left (ghosted)
   - Use case exhausted (no new workflows being built)
   - Integration broken (look at `fact_workflow_runs.error_code` distribution for the customer)

### Healthy + expansion candidate (utilization ≥0.80, no recent expansion conversation)

1. **Trigger**: CSM gets a notification.
2. **Action**: Initiate seat-expansion conversation with the AE. Standard offer is 50% incremental seats at the existing per-seat rate (seat-discount preserved). Approval ladder per `notion__pricing-tiers.md`.

> **Example**: `cust_000087` Halcyon Research — utilization 0.56, 2-year multi-year discussion landed +$66K ARR. See `gong__renewal__halcyon-research.md`.

## Where the data comes from

All signals are computed nightly by dbt models:

- `dbt/models/marts/cs/account_health.sql` — combines engagement + utilization into a per-customer row
- `dbt/models/marts/cs/at_risk_alerts.sql` — filters to critical/at-risk and posts to `#cs-at-risk`
- `dbt/models/marts/cs/expansion_candidates.sql` — filters to healthy + expansion eligible

> 🚧 `// TODO: write a "WHY this works" doc for the dbt models. people keep asking "why did the bot post about my account, what changed yesterday?". some kind of human-readable diff would help -marco`

## Important caveats

- **Don't apply seat utilization to Enterprise.** (See above.)
- **Free customers don't have CSMs.** They are not in this playbook.
- **Recently churned customers may still have stale `dim_customers.current_plan_tier`.** The dim is eventually consistent. For decisions, use `fact_subscriptions.is_current = TRUE`.
- **Single-day spikes in error rates don't necessarily mean trouble.** Check the 28-day trend, not just yesterday.

## Renewal forecast

CSMs maintain a renewal forecast in CRM, updated 90 / 60 / 30 days out from contract end. Forecast tiers:

- **Commit (95%+ renewal probability)**
- **Best case (50-94%)**
- **Pipeline (10-49%)**
- **Omitted (lost)**

CSMs also assign a **renewal amount** (could be flat, expansion, or contraction). VPs review at the QBR.

## Edge cases nobody's documented (writing them here so they're somewhere)

- **Customer is in the middle of an M&A**. Their usage drops because everyone is in due diligence meetings. Don't escalate to "critical" — flag in CRM and pause action ladder for 30 days.
- **Customer paused (status = 'paused')**. They have an active subscription but stopped using. Different workflow than churn. CS owns "unpause" outreach. Pricing committee usually offers a 30-day pause extension before requiring a churn decision.
- **Customer's primary admin email bounces (HR change probably)**. CSM should ping the AE to find new contact. We've had 3 cases in last year where the original admin left and we didn't realize for months because the bot only emails the admin.

> **Comment from elena.volkov (2026-04-12)**: We need to formalize the bouncing-email signal as an at-risk trigger. Adding to the 2026-H1 value-score model scope.

## Off-topic but useful

- The `acme-cs-bot` posts a digest every Monday at 8AM UTC to `#cs-leadership`. That's separate from the per-account at-risk alerts in `#cs-at-risk`.
- For customer Slack Connect channels (Business+), responses should be within 4 business hours during business hours. We sometimes do casual chat in those channels — fine, just keep it professional.
- Shared "CSM pro tips" doc lives at [other Notion page]. Stuff like "always ask about the champion's career trajectory in EBRs — when champions get promoted, the relationship sometimes changes overnight."

## Comment thread (footer)

> **2026-04-12** — `elena.volkov`: Added bouncing-email edge case + value-score model TODO.
> **2026-02-10** — `elena.volkov`: Quarterly review. Added NPS-detractor as 4th cadence item.
> **2025-12-15** — `rajiv.patel`: Added engagement-floor-vs-value-realization comment.
> **2025-09-04** — `marco.chen`: Initial version.
