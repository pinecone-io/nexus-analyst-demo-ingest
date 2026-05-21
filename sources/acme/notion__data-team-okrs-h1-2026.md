---
title: "Notion — data team OKRs H1 2026"
source_url: "internal://acme/notion/data-team-okrs-h1-2026"
license: "synthetic-demo"
attribution: "Acme Inc internal planning (synthetic demo). Owners: Dan Lee, David Kim."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: notion_doc
---

# Data Team OKRs — H1 2026

> **Status**: Active / In-Progress
> **Last Updated**: 2026-01-15
> **Owners**: @dan.lee (Product/Analytics), @david.kim (Data Engineering)
> **Stakeholders**: @rachel.stein (CFO), @elena.volkov (VP CS), @jasmine.park (Marketing)

This document outlines the Data Team's strategic objectives and key results for the first half of 2026. These goals are aligned with the company-wide push for better capital efficiency and more granular customer health monitoring as we scale toward $50M ARR.

---

## Objective 1: Move beyond First-Touch Attribution to Multi-Touch
**Owner**: @dan.lee (Lead), @jorge.martinez (Assist)
**Context**: Our current model in `dbt__model__bookings_attribution.md` is strictly first-touch. Marketing (@jasmine.park) needs to understand the influence of webinars and content on mid-funnel conversion for Business-tier accounts.

*   **KR1**: Ship `marts/marketing/multi_touch_attribution` dbt model supporting Linear and U-Shaped decay models.
*   **KR2**: Achieve 95% match rate between attributed revenue in the warehouse and Salesforce Opportunity ACV.
*   **KR3**: Launch the "Marketing Influence & ROAS" dashboard in Looker, replacing the legacy first-touch-only view.

## Objective 2: Infrastructure Reliability & Freshness
**Owner**: @david.kim
**Context**: Following the 2025-09-12 incident (see `postmortem__workflow-runs-stale-2025-09-12.md`), we committed to tighter SLAs. Current 4h-8h freshness is insufficient for CS at-risk alerting.

*   **KR1**: Reduce dbt freshness latency to <30 minutes for all Tier-1 marts (including `fact_subscriptions`, `fact_workflow_runs`, and `fact_user_events`).
*   **KR2**: Implement dbt-tests for schema drift on all upstream CDC sources to catch product DB changes before they break the warehouse.
*   **KR3**: Zero "P1" data-stale incidents in Q2.

## Objective 3: Standardize Retention & Cohort Reporting
**Owner**: @dan.lee
**Context**: Finance (@lina.cho) currently computes NRR manually or via the complex `dbt__model__nrr_trailing_12.md`. We need a reusable mart for arbitrary cohort analysis (by industry, region, and acquisition channel).

*   **KR1**: Ship `marts/finance/cohort_retention` mart that supports N-month retention lookups without re-running window functions.
*   **KR2**: Deprecate 4 legacy Google Sheets used by FP&A for "unofficial" NRR tracking.
*   **KR3**: Enable "Self-Serve Cohorts" in Looker, allowing AEs to see retention by their specific account lists.

## Objective 4: Rollout Value Realization Score (VRS)
**Owner**: @rajiv.patel
**Context**: Supplementing the binary "Engaged Customer" flag with a 0-100 score to better predict churn in the MM/Enterprise segments. See `notion__draft__value-realization-score-spec.md` for the technical spec.

*   **KR1**: Finalize VRS weighting logic (Logistic Regression fit) using 2024-2025 churn data.
*   **KR2**: Implement `marts/cs/value_realization_score` in production dbt project.
*   **KR3**: Achieve >0.80 AUC on churn prediction for the Q2 renewal cohort (vs 0.65 current baseline).

---

## Progress Updates & Discussion

**2026-04-15 — @david.kim**
> Freshness for `fact_workflow_runs` is now averaging 22 minutes. We hit a snag with `fact_user_events` due to Segment volume spikes, but the 30-min goal is still on track for June.

**2026-03-12 — @jorge.martinez**
> Multi-touch scoping is done. We're running into an issue where `fact_marketing_touches` doesn't always have a `customer_id` for early-stage leads. Working with @jasmine.park to improve lead-to-account mapping in HubSpot.

**2026-02-04 — @dan.lee**
> VRS model is in "shadow mode." Initial results show it's catching "ghosting" admins much faster than the old binary flag. @rajiv.patel is tuning the weight for P1 tickets.

**2026-01-15 — @dan.lee**
> OKRs finalized and approved by @sam.reyes and @rachel.stein. Let's execute.

---

## Related Documents
*   `notion__data-warehouse-conventions.md`
*   `notion__csm-account-health-runbook.md`
*   `dbt__model__nrr_trailing_12.md`
*   `notion__draft__value-realization-score-spec.md`
