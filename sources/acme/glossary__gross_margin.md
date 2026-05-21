---
title: "Glossary — Gross Margin"
source_url: "internal://acme/glossary/gross-margin"
license: "synthetic-demo"
attribution: "Acme Inc internal metric definitions (synthetic demo). Owned by FP&A (emp_060)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: glossary
---

# Gross Margin

**One-line definition.** Gross Margin is the percentage of total revenue remaining after deducting the Cost of Goods Sold (COGS), representing the efficiency of our core platform delivery.

**Formula.**
```
Gross Margin % = (Total Revenue - COGS) / Total Revenue
```

## What is included in Acme COGS?

Unlike many early-stage SaaS companies that only track hosting, Acme includes all direct costs required to support and maintain the customer base:

1.  **Infrastructure & Hosting**: BigQuery compute/storage, Pinecone (vector DB for AI features), and Looker instance costs.
2.  **Support Operations**: Payroll and overhead for the support engineering team (managed by @priya.anand).
3.  **Customer Success Delivery**: The portion of CSM headcount dedicated to technical onboarding and implementation (managed by @elena.volkov).
4.  **Third-party AI Compute**: API costs for Vertex AI and OpenAI (currently the fastest-growing line item).

## Historical Performance & Assumptions

*   **LTV Modeling Assumption**: We use a standard **80%** gross margin for all long-term value and unit economic modeling. See `glossary__ltv.md`.
*   **H2 2025 Actual**: Per the final 2025 audit, actual Gross Margin was **78%**. The 200bps miss vs. target was primarily driven by higher-than-forecasted token usage for the AI Workflow Assistant beta.
*   **2026 Target**: 81%. We expect to hit this through BigQuery slot optimizations led by @david.kim and improved seat-utilization on Business/Enterprise tiers.

## Current Trends & Risks

The primary risk to our 80% margin floor is **AI feature compute**. As of 2026-Q1, AI-related COGS is growing at 1.4x the rate of ARR growth. While the "AI Workflow Assistant" is currently in beta for Pro+ tiers, we are evaluating a usage-based surcharge if margins dip below 75% for more than two consecutive quarters.

## Related Documentation

*   `glossary__arr.md` — The denominator for margin calculations.
*   `glossary__ltv.md` — How we use margin to calculate customer lifetime value.
*   `slack__board-prep__gross-margin-question.md` — Detailed breakdown of the H2 2025 variance for the Q4 board deck.
*   `notion__pricing-tiers.md` — Reference for which tiers include high-COGS features like dedicated CSMs.

**Owner**: @lina.cho (FP&A)  
**Last Reviewed**: 2026-04-18
