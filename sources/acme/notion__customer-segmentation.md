---
title: "Notion — customer segmentation framework"
source_url: "internal://acme/notion/customer-segmentation"
license: "synthetic-demo"
attribution: "Acme Inc internal documentation (synthetic demo). Owners: Lina Cho (FP&A) & Dan Lee (Product)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: notion_doc
---

# Customer segmentation framework

> **Last updated**: 2026-03-22
> **Owners**: @lina.cho (FP&A), @dan.lee (Product)
> **Stakeholders**: Sales Ops, Marketing, Customer Success
>
> 🚧 `// TODO: align these definitions with the upcoming value-realization-score model. see notion__draft__value-realization-score-spec.md -dan`

This document defines the canonical segments used for board reporting, product roadmap prioritization, and CS resource allocation. While `dim_customers` contains raw attributes, these derived segments are what we use in Looker and dbt for high-level analysis.

## 1. Revenue segmentation (ARR bands)

We segment our **~530 paid customers** into three tiers based on their current ARR. Note that these bands are based on actual contract value, not just the `account_tier` assigned by Sales.

| Segment | ARR Band | Count (Approx) | Total ARR Contribution | Primary Plan(s) |
|---|---|---|---|---|
| **SMB** | < $10k | ~380 | ~$1.5M | Pro, Business (low seat) |
| **Mid-Market (MM)** | $10k – $50k | ~125 | ~$31.5M | Business |
| **Enterprise** | > $50k | ~25 | ~$6.0M | Enterprise |

**Data Source**: These figures are derived from `fact_subscriptions` where `is_current = TRUE`. For the latest aggregate snapshot, see `dbt__model__arr_snapshot.md`.

> **Note from lina.cho**: The Mid-Market segment is our "powerhouse," contributing over 80% of our total ~$39M ARR. Even though SMB has the highest logo count, the Business tier pricing ($149/seat) heavily skews our revenue toward MM.

## 2. Industry segmentation

Acme's workflow automation is horizontal, but we see significant clustering in six key verticals. Industry is captured at signup and verified by AEs in Salesforce.

| Industry | Paid Logo % | Notes |
|---|---|---|
| **Fintech** | 22% | High security/audit log requirements. Mostly Business/Ent. |
| **Healthtech** | 18% | Heavy focus on PII scrubbing and HIPAA-compliant workflows. |
| **Media & Ent** | 15% | High volume of webhook-triggered workflows for content dist. |
| **Retail / E-comm** | 12% | Seasonal spikes; heavy use of GSheets and Shopify integrations. |
| **Manufacturing** | 10% | Legacy system connectivity; long sales cycles. |
| **Dev Tools / SaaS** | 8% | Our "early adopter" base; high usage of API-triggered runs. |
| **Other** | 15% | Education, Non-profit, Professional Services. |

## 3. Tenure segmentation (Lifecycle)

We track "Time since Signup" to understand how usage matures. Tenure is calculated as `CURRENT_DATE - dim_customers.signup_date`.

*   **New (< 6 months)**: ~85 customers. Focus is on "Time to First Value" and reaching the **Engaged Customer** threshold (see `glossary__engaged_customer.md`).
*   **Established (6 – 24 months)**: ~310 customers. This is our largest cohort. Focus is on seat expansion and multi-workflow adoption.
*   **Mature (> 24 months)**: ~135 customers. These are our earliest adopters from 2023-2024. High NRR potential but also higher risk if the original champion leaves.

## 4. Usage-based segmentation (Engagement)

While revenue tells us what they pay, usage tells us if they'll stay. We cross-reference the revenue bands with the health signals defined in `dbt__model__account_health.md`.

*   **High-Value / High-Usage**: (MM/Ent + Engaged). Our "Ideal Customer Profile" (ICP).
*   **High-Value / Low-Usage**: (MM/Ent + Not Engaged). The "Danger Zone." These accounts are prioritized for CSM outreach in the `notion__csm-account-health-runbook.md`.
*   **Low-Value / High-Usage**: (SMB + Engaged). Primary targets for AE-led "Pro to Business" upgrade campaigns.

## Implementation in SQL

To replicate these segments in your own queries, use the following logic:

```sql
SELECT
  c.customer_id,
  CASE 
    WHEN c.current_mrr_usd * 12 < 10000 THEN 'SMB'
    WHEN c.current_mrr_usd * 12 BETWEEN 10000 AND 50000 THEN 'Mid-Market'
    ELSE 'Enterprise'
  END AS revenue_segment,
  CASE
    WHEN DATE_DIFF(CURRENT_DATE(), c.signup_date, MONTH) < 6 THEN 'New'
    WHEN DATE_DIFF(CURRENT_DATE(), c.signup_date, MONTH) BETWEEN 6 AND 24 THEN 'Established'
    ELSE 'Mature'
  END AS tenure_segment,
  c.industry
FROM `nexus-analyst-demo.acme.dim_customers` c
WHERE c.status = 'active';
```

## Change Log & Comments

*   **2026-03-22** — `lina.cho`: Updated ARR bands. Moved the MM/Ent cutoff from $40k to $50k to align with the new Sales commission structure.
*   **2026-01-10** — `dan.lee`: Added Tenure segmentation to help Product team analyze feature adoption by cohort age.
*   **2025-11-15** — `lina.cho`: Initial framework established for Q4 Board Meeting.

> **Comment from @marcus.webb**: Can we add a "Partner-Led" segment here? We're seeing more deals coming through the SI channel that behave differently than direct outbound.
> 
> **Reply from @lina.cho**: Good point, Marcus. I'll look at adding `acquisition_channel` as a secondary pivot in the Q3 update.
