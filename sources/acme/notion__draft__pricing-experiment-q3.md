---
title: "Notion (draft) — Q3 pricing experiment proposal"
source_url: "internal://acme/notion/drafts/pricing-experiment-q3"
license: "synthetic-demo"
attribution: "Acme Inc internal pricing proposal (synthetic demo). Owners: Rachel Stein (CFO) & Marcus Webb (VP Sales)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: notion_doc
---

# DRAFT: Q3 2026 Pricing Experiment — Pro Tier Adjustment

> **Status**: DRAFT / PROPOSAL
> **Created**: 2026-04-22
> **Owners**: @rachel.stein (CFO), @marcus.webb (VP Sales)
> **Stakeholders**: @dan.lee (Product), @jasmine.park (Marketing), @elena.volkov (CS)
> **Target Launch**: 2026-07-01 (Experiment start)
>
> ⚠️ **Internal Only**: This is a pre-approval draft. Do not share with customers or partners.

## Executive Summary

We are proposing a pricing experiment for Q3 2026 to test the price elasticity of our **Pro** tier. Based on Q1 2026 performance data, we believe the Pro tier ($49/seat/month) is currently under-priced relative to the value delivered and the high conversion rate we are seeing into the Business tier.

The proposal is to increase the Pro list price by ~15% (to **$59/seat/month**) for new customers only, while grandfathering all existing Pro customers for 12 months.

## Rationale

1.  **Value-Price Gap**: As documented in `notion__pricing-tiers.md`, the Pro tier includes a 10,000 run quota and unlimited workflows. Our recent analysis of `fact_workflow_runs` shows that the median Pro customer is utilizing ~65% of their quota, yet our Pro-to-Business conversion rate remains healthy at ~12% within the first 6 months.
2.  **Expansion Signal**: Per the `notion__expansion-playbook.md`, we’ve seen that customers who hit the 10-seat mark on Pro almost invariably transition to Business within 90 days. This suggests that the "Pro" phase of the lifecycle is a high-value period where customers are willing to pay a premium for the workflow reliability we provide.
3.  **Revenue Optimization**: With Pro ARR currently sitting at ~$1M (see `glossary__arr.md`), a 15% lift on new acquisition would contribute an estimated incremental $150K-$200K ARR by EOY 2026 without impacting the core Business tier book (~$32M).

## Experiment Design

*   **Treatment**: New signups on `acme.com` will see Pro priced at **$59/seat/month**.
*   **Control**: 50/50 split-test on the pricing page (via Optimizely).
*   **Duration**: 30 days (July 1, 2026 – July 31, 2026).
*   **Grandfathering**: Existing customers on `sub_xxxxxx` records with `plan_tier = 'Pro'` will remain at $49 for 12 months.
*   **Success Metrics**:
    *   Primary: Conversion rate from Free → Pro (target: < 5% degradation).
    *   Secondary: Average Initial Seat Count (target: flat at 4.2).
    *   Tertiary: Pro → Business upgrade velocity.

## Risks & Mitigations

| Risk | Mitigation |
| :--- | :--- |
| **Competitive Pressure** | Our primary mid-market competitor is currently at $55/seat. At $59, we remain in the same "considered purchase" bracket while signaling higher enterprise-grade reliability. |
| **Marketing Friction** | @jasmine.park to update all paid search copy to focus on "Unlimited Workflows" rather than the entry price point. |
| **Sales Friction** | AEs will be authorized to offer the old $49 price as a "limited time" incentive to close Pro deals in the pipeline before August 1. |

## Data & Analysis Requirements

@david.kim — we will need a dedicated view in BigQuery to track the experiment cohorts. We need to ensure `fact_subscriptions` can distinguish between "Pro-Control" and "Pro-Treatment" during the 30-day window.

> **Note from @rachel.stein**: I've reviewed the preliminary impact on NRR (see `glossary__nrr.md`). Even with a slight dip in Pro conversion, the higher starting MRR per logo should keep our LTV/CAC ratios in the "Green" zone for SMB.

## Next Steps

1.  **CEO Approval**: Awaiting final sign-off from @sam.reyes (scheduled for 2026-05-10).
2.  **Technical Readiness**: @hannah.miles to confirm billing system (`tomas.vega`'s team) can support the split-price test.
3.  **Sales Enablement**: @marcus.webb to draft talk tracks for SDRs/AEs regarding the "Value Realization" of the new pricing.

## Comments

> **2026-04-23 — @marcus.webb**: I'm supportive. We've been leaving money on the table in the 5-20 seat segment. Most of these guys are comparing us to Tray or Workato, where the entry point is much higher anyway.
>
> **2026-04-24 — @dan.lee**: Can we ensure the "AI Workflow Assistant" beta (ref `notion__draft__value-realization-score-spec.md`) is highlighted as a Pro+ feature during this test? It justifies the $10 bump.
>
> **2026-04-25 — @rachel.stein**: @dan.lee agreed. Let's bundle the Assistant beta as part of the "New Pro" value prop. @jasmine.park, please factor this into the landing page variants.
