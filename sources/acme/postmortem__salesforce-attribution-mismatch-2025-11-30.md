---
title: "Postmortem — Salesforce attribution channel mismatch 2025-11-30"
source_url: "internal://acme/postmortem/salesforce-attribution-mismatch-2025-11-30"
license: "synthetic-demo"
attribution: "Acme Inc internal postmortem (synthetic demo). Owner: Sales Ops."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: postmortem
---

# Postmortem — Salesforce attribution channel mismatch

**Date**: 2025-11-30  
**Owner**: @jorge.martinez (Sales Ops)  
**Stakeholders**: @jasmine.park (Marketing), @marcus.webb (VP Sales), @lina.cho (FP&A)  
**Status**: Resolved / Methodology Clarified  

## Executive Summary

During the Q3 2025 Business Review prep, a significant discrepancy was identified between the Marketing Attribution dashboard in Looker (powered by the BigQuery warehouse) and the native Salesforce "Closed Won by Source" report. 

Specifically, the Looker-based channel-mix slide reported `paid_search` as contributing **31%** of Q3 bookings ACV, while the Salesforce dashboard reported only **23%**. This 8-point delta caused confusion during the executive preview, leading to a temporary pause on Q4 paid search budget allocation until the "correct" figure could be verified.

The root cause was not a data pipeline failure, but a **methodological mismatch**: Salesforce was configured to use a "Last Touch" attribution model, whereas the Acme data warehouse (specifically `dbt__model__bookings_attribution.md`) uses a "First Touch" model.

## Timeline

- **2025-11-20 10:15 AM**: @lina.cho pings @jorge.martinez in Slack noting that the "Bookings by Channel" Looker tile doesn't match the SFDC report she pulled for the board deck.
- **2025-11-20 02:00 PM**: @jorge.martinez confirms the delta: Looker shows $1.2M in Paid Search ACV for Q3; SFDC shows $890K.
- **2025-11-21 09:00 AM**: Investigation into `fact_marketing_touches` vs. SFDC `LeadSource` and `Opportunity.Lead_Source_Detail__c`.
- **2025-11-22 11:30 AM**: Root cause identified. SFDC Opportunity source is overwritten by the most recent campaign touch before the Opportunity is created (Last Touch). The dbt model `marts/sales/bookings_attribution.sql` explicitly selects the earliest touch (First Touch).
- **2025-11-24 04:00 PM**: Methodology alignment meeting with @jasmine.park and @marcus.webb.
- **2025-11-30 01:00 PM**: Postmortem published; reporting labels updated.

## Root Cause

Acme’s data warehouse is designed to measure the effectiveness of top-of-funnel acquisition. Per the logic in `dbt__model__bookings_attribution.md`, we prioritize the **First Touch** to understand what originally brought the customer into the Acme ecosystem.

Salesforce, however, was configured by a legacy consultant in 2024 to update the `Opportunity.Lead_Source_Detail__c` field based on the most recent campaign response. For many Q3 deals, customers originally found Acme via `paid_search` (First Touch), but later engaged with a `webinar` or `content` piece (Last Touch) before the AE opened the Opportunity. 

Because `paid_search` is often the entry point but rarely the final touch before a sales-led Opportunity is created, the Last-Touch model in Salesforce systematically under-reports the value of search spend.

## Resolution & Corrective Actions

1.  **Methodology Standardization**: The "First Touch" model remains the canonical metric for board reporting and ROAS calculation. It is more representative of our current PLG-to-Sales motion.
2.  **Reporting Transparency**: All Looker tiles in the "Executive Daily" and "Bookings by Channel" dashboards have been updated with a footer: *"Attribution Model: First Touch. Source: BigQuery `marts/sales/bookings_attribution`."*
3.  **Salesforce Alignment**: @jorge.martinez has updated the Salesforce Opportunity report descriptions to explicitly state they use "Last Touch" logic. 
4.  **Future Work**: We have added a ticket to the H2 roadmap to introduce a multi-touch attribution (MTA) model in dbt. This will allow us to see both First and Last touch side-by-side to avoid this confusion in the future. See `notion__draft__value-realization-score-spec.md` for related data modeling discussions.

## Slack Thread Context

> **@marcus.webb (2025-11-21 08:44 AM)**: If Paid Search is actually 23% and not 31%, I’m over-spending on Google. We need to be 100% sure which number is right before I sign off on the December budget.
>
> **@jorge.martinez (2025-11-21 09:12 AM)**: Working on it, Marcus. It looks like a First vs Last touch issue. SFDC is giving credit to the webinar they attended last week, but BQ is giving credit to the search ad they clicked 3 months ago to sign up for the Free tier.
>
> **@jasmine.park (2025-11-21 09:15 AM)**: +1 to Jorge. For our spend, First Touch is what matters. If they don't click the ad, they never get to the webinar.

## Lessons Learned

- **Definitions Matter**: "Channel Mix" is not a raw fact; it is a derived interpretation.
- **Tool Parity**: Native SaaS tool reporting (Salesforce, HubSpot) will almost always disagree with a custom dbt model unless the logic is manually synced.
- **Documentation**: The rationale for First-Touch was documented in `slack__marketing__attribution-model-question.md` but was not linked in the Looker dashboard itself.

**Action Item Owner**: @jorge.martinez  
**Due Date**: 2025-12-15 (Completed)
