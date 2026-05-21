---
title: "Notion — NPS collection and rollup process"
source_url: "internal://acme/notion/nps-collection-process"
license: "synthetic-demo"
attribution: "Acme Inc internal documentation (synthetic demo). Owner: Elena Volkov (VP CS)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: notion_doc
---

# NPS collection and rollup process

> **Last updated**: 2026-04-10 by elena.volkov
> **Owner**: Elena Volkov (VP CS)
> **Stakeholders**: Product (Dan Lee), Marketing (Jasmine Park), Data (David Kim)
>
> 🚧 `// TODO: we need to automate the "detractor alert" to Slack. currently david.kim has a manual query but it should be a dbt test or a bot action. -elena 2026-04-12`

This document outlines how Acme collects Net Promoter Score (NPS) data, how it flows into the warehouse, and how we use it for account health and renewal forecasting.

## Collection methodology

Acme uses an in-app survey (powered by Delighted) to collect NPS. 

- **Targeting**: All active users (`is_active = TRUE`) on paid plans (Pro, Business, Enterprise). Free tier users are currently excluded to reduce noise in our core health metrics.
- **Cadence**: Rolling 90-day cycle. A user is eligible for a survey every 90 days, provided they have logged in at least 3 times in the last 30 days. This ensures we aren't surveying "ghost" users who haven't seen the product recently.
- **Format**: Standard 0-10 scale ("How likely are you to recommend Acme to a friend or colleague?") followed by an optional free-text comment.

### Response rates (as of 2026-Q1)

| Metric | Value | Notes |
|---|---|---|
| **Overall Response Rate** | ~38% | High for B2B; likely due to the in-app placement. |
| **Pro Response Rate** | ~24% | Self-serve users are less likely to engage. |
| **Business/Ent Response Rate**| ~52% | Higher engagement among power users. |

## Data flow

1. **Source**: Delighted API.
2. **Ingestion**: Daily sync via Fivetran into `raw.nps_responses`.
3. **Transformation**: dbt processes raw responses into `fact_nps_responses`. This model pre-computes the `segment` (Promoter/Passive/Detractor) and joins the `customer_id` and `user_id`.
4. **Rollup**: The data is consumed by `dbt__model__account_health.md` to flag accounts with recent negative sentiment.

## Usage in health & forecasting

NPS is a "lagging qualitative" signal. While it doesn't always predict churn (some detractors stay for years because of high switching costs), it is a critical input for:

### 1. Account Health (`account_health_status`)
In `dbt__model__account_health.md`, any customer with a **Detractor (0-6)** response in the trailing 90 days is automatically moved to the `monitoring` or `at_risk` status, regardless of their seat utilization. 
- **Rule**: `has_recent_nps_detractor = TRUE` triggers a mandatory CSM check-in within 5 business days.

### 2. Renewal Forecasting
CSMs use NPS comments to justify their "Renewal Probability" in the CRM. 
- **Commit**: Requires no active detractors among the "Builder" or "Admin" roles.
- **At Risk**: If the primary admin is a detractor, the renewal must be moved to `Pipeline` or `Omitted` unless a save-plan is documented.
- See `dbt__model__renewal_forecast.md` for how these qualitative flags are weighted in the aggregate forecast.

## Important caveats

- **Sample size warning**: Most customers only have 1-3 responses per quarter. **Never trust a single customer's NPS in isolation.** A single "4" from a frustrated user who had a bad Tuesday can skew a small account's health. Always look at the comment context.
- **Role bias**: Admins tend to score lower (focused on billing/SSO friction) while Builders score higher (focused on workflow power). 
- **Cohort level only**: We only report "Official NPS" at the `account_tier` or `plan_tier` level to ensure statistical significance.

## Recent changes & incidents

- **2026-03-22**: Collapsed the 1-10 scale to 1-5 for the `csat_score` field in support tickets, but kept NPS at 0-10 to maintain industry standard.
- **2026-02-15**: Fixed a bug where `user_id` was missing for ~15% of responses due to a mapping error in the Delighted-Segment integration. Backfilled via email hash.
- **2025-11-15**: Added `fact_nps_responses.segment` as a precomputed column to stop analysts from re-defining "Promoter" differently in every Looker explore.

## Comment thread

> **2026-04-15** — @dan.lee: Can we add a "Product Area" tag to the comments? I want to see if detractors are mostly complaining about the AI Assistant or the Billing UI.
> 
> **2026-04-16** — @elena.volkov: @dan.lee Great idea. @david.kim is looking into using a basic regex/LLM classifier in dbt to tag the `comment` field.
> 
> **2026-04-20** — @marco.chen: Just a reminder for CSMs—if you see a detractor score from a champion, don't wait for the nightly sync. Log it in Salesforce immediately so the AE knows before the next QBR.
