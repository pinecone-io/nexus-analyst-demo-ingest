---
title: "Notion — AI Workflow Assistant beta plan"
source_url: "internal://acme/notion/ai-workflow-assistant-beta"
license: "synthetic-demo"
attribution: "Acme Inc internal product spec (synthetic demo). Owners: Dan Lee (Product), Priya Anand (Eng)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: notion_doc
---

# AI Workflow Assistant — Beta Launch Plan

> **Status**: Finalizing Beta Cohort
> **Owners**: @dan.lee (Product), @priya.anand (Engineering)
> **Target Beta Start**: 2026-05-15
> **Target GA**: 2026-Q3 (August/September)
> **Stakeholders**: @elena.volkov (CS), @marcus.webb (Sales), @hannah.miles (Lead Eng)

## Overview
The AI Workflow Assistant is a natural-language interface for building and debugging Acme workflows. It leverages a fine-tuned LLM to suggest step configurations, map variables between integrations, and auto-generate Python snippets for custom logic steps. 

This beta is the critical path to hitting our Q3 GA goal. We are transitioning from internal "dogfooding" (which started 2026-03-10) to a limited external release.

## Beta Cohort Selection
We are limiting the beta to **15 design-partner customers**. This ensures high-touch feedback loops and allows us to monitor infrastructure costs (token spend) closely.

### Eligibility Criteria
To be considered for the beta, a customer must meet the following:
*   **Plan Tier**: Business or Enterprise only.
*   **Engagement**: Must be an "Engaged Customer" per `glossary__engaged_customer.md` (≥3 active users, ≥10 successful runs in 28d).
*   **Commitment**: Willingness to join a weekly 30-minute feedback call with @dan.lee or @marco.chen.
*   **Legal**: Signed the "Beta Feature Addendum" (managed by @rachel.stein's team).

### Confirmed Design Partners (Partial List)
| Customer ID | Company Name | Primary Contact | CSM |
|---|---|---|---|
| `cust_000412` | Drag Industries | Sarah Jenkins | @marco.chen |
| `cust_000087` | Halcyon Research | Sundara Reddy | @rajiv.patel |
| `cust_000621` | NexaFlow Systems | Elena Rodriguez | @marco.chen |

> **Note from @dan.lee**: We specifically included `cust_000412` (Drag Industries) despite their recent utilization dip because they are a key Enterprise expansion target. See `gong__discovery__cust000412-drag-industries.md`.

## Success Metrics
We will track the following in a dedicated Looker dashboard (`AI Assistant Beta Health`):
1.  **Assistant Activation**: % of users in the beta cohort who send ≥1 prompt.
2.  **Suggestion Acceptance Rate**: % of AI-generated steps that are actually saved to a workflow.
3.  **Time-to-First-Run**: Reduction in minutes from `workflow_created` to first `success` run compared to non-AI users.
4.  **Token Efficiency**: Average cost per successful workflow generation (monitored by @priya.anand).

## Engineering & Infrastructure
@priya.anand and @hannah.miles have finalized the VPC-peered connection to our LLM provider. 

*   **Rate Limiting**: Hard cap of 50 prompts per user per day during beta to prevent runaway costs.
*   **Data Privacy**: PII scrubbing is enabled by default for all prompts. See `notion__pricing-tiers.md` regarding the PII scrubbing flag shipped 2026-04-30.
*   **Telemetry**: Every prompt and acceptance event is logged to `fact_user_events` with `properties_json` containing `assistant_session_id`.

## Timeline
*   **2026-04-30**: Finalize beta cohort and sign-offs. (COMPLETED)
*   **2026-05-05**: Internal "Bug Bash" with @tomas.vega and the billing team.
*   **2026-05-12**: Provisioning scripts run; feature flags enabled for `beta_cohort_v1`.
*   **2026-05-15**: **Beta Launch Day.** Welcome emails sent to 15 admins.
*   **2026-06-15**: Mid-beta review. Decide on expanding to 50 customers (Pro tier inclusion).
*   **2026-07-15**: Feature freeze for GA.

## Known Risks & Mitigations
*   **Hallucinations**: The assistant might suggest integration fields that don't exist. 
    *   *Mitigation*: We've implemented a "Schema Validator" that checks suggestions against our internal integration metadata before showing them to the user.
*   **Cost**: High token usage could erode margins on Business seats.
    *   *Mitigation*: @lina.cho is modeling a "Usage-based Add-on" for GA if costs exceed $5/user/mo.
*   **Support Load**: Beta users might open high volumes of tickets for "AI being weird."
    *   *Mitigation*: All AI-related tickets are auto-routed to a private Slack channel `#ai-beta-feedback` instead of the general support queue.

## Discussion & Comments
> **2026-04-30** — `@priya.anand`: @hannah.miles confirmed the latency on the schema validator is down to <200ms. We are green for launch on the 15th.
>
> **2026-04-28** — `@dan.lee`: Updated the cohort list. We swapped out one SMB account for NexaFlow (`cust_000621`) to get more Enterprise-scale feedback.
>
> **2026-04-22** — `@elena.volkov`: CSMs for the 15 partners have been briefed. @marco.chen is leading the feedback call scheduling.
>
> **2026-04-15** — `@rachel.stein`: Please ensure the "Beta Feature Addendum" is linked in the onboarding email. We need to be clear that uptime SLAs do not apply to the Assistant during beta.
