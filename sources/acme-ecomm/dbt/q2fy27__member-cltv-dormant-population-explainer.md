---
title: "dbt model note: member_cltv dormant-member population and the $500 vs $625 join trap"
source_url: "internal://acme-ecomm/dbt/q2fy27__member-cltv-dormant-population-explainer"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: dbt_model
---

# dbt Model Documentation: `member_cltv`

**Model Name:** `nexus-analyst-demo.acme_ecomm.member_cltv`  
**Owner:** wei.hartono (Data & Analytics, assoc_100210)  
**Last Modified:** 2026-07-18  
**Dataset Reference:** Flat BigQuery dataset (`nexus-analyst-demo.acme_ecomm`), adhering to the post-March 2025 path consolidation standard. (Note for anyone running legacy queries: do not use nested paths like `acme_ecomm.marts.membership.member_cltv`—that will throw a dataset-not-found error, as resolved back in the Q1FY26 MBR audit).

---

## 1. Executive Summary & Purpose

The `member_cltv` model is the canonical board source for Acme+ Customer Lifetime Value (CLTV) metrics, supporting financial planning, member lifecycle reporting, and the membership analytics dashboards reviewed regularly by renee.kowalski and simone.laurent. 

With Q2FY27 currently in flight (88% elapsed as of today, 2026-07-20), executive leadership is closely tracking our year-end membership goals: total active members stand at 14.62M (pacing toward an exit of ~15.05M against our 14.8M FY27 target, putting us at 101.7% of goal), and our annual renewal rate is pacing at 87.2% (beating the 86.0% target). These are the standard headline indicators; they're computed from active-subscriber and renewal counts and don't reference order activity at all.

Separately, `member_cltv` carries an order-activity cut of the same panel worth knowing about: because dormant members have not cancelled their subscriptions, they continue to pay their annual or monthly fees and are counted as "active" in the subscriber and renewal totals above. Yet a substantial slice of our panel shows zero purchasing activity over the trailing 12 months.

This model note documents the canonical SQL construction required to capture this population accurately, walks through the math of the "$500 vs. $625 join trap," and highlights why an inner join fundamentally skews our financial modeling.

---

## 2. The Panel Structure & The Dormant Population

Our calculations rely on the 120,000-member representative panel stored in `nexus-analyst-demo.acme_ecomm.dim_member`. (Remember the foundational convention: aggregate fact tables are full-population, but entity tables like `dim_member`, `fact_orders`, and `fact_membership_events` are representative panels. Never use `COUNT(*)` or `SUM()` on these tables to derive company-wide absolute totals; those must come from aggregate marts or MBR decks).

When evaluating our 120,000-member panel against trailing-12-month order histories in `fact_orders`, a critical behavioral split emerges:

* **Active Buyers (80% of panel / ~96,000 members):** Members who have placed at least one order in the trailing 12 months. This group includes power users like Dana (`mem_1000042`), who leverages free shipping, early access, and our newly integrated Reelstream perks (which replaced Vidora back on June 1st).
* **Dormant Members (20% of panel / ~24,000 members):** Members who continue to pay their membership fees (either on monthly or annual plans) but have **zero orders** in the trailing 12 months. 

The canonical archetype for this population is Marisol (`mem_1000178`), who maintains an active annual Acme+ subscription but has not purchased a single item across any vertical in over a year. Marisol represents the exact demographic our standard renewal tracking completely misses: she is technically "retaining" from a billing perspective, but she is functionally dormant from an e-commerce engagement perspective.

---

## 3. The Canonical Construction: The `LEFT JOIN` + `COALESCE(0)` Pattern

To ensure our CLTV reporting does not inadvertently sweep this 20% dormant population under the rug, the `member_cltv` dbt model is strictly constructed using a `LEFT JOIN` from `dim_member` to the aggregated `fact_orders` table, paired with explicit zero-filling via `COALESCE`.

Below is an excerpt of the core transformation logic implemented in the model:

```sql
SELECT
    m.member_id,
    m.signup_date,
    m.home_market,
    m.plan_type,
    m.status,
    -- Calculate tenure and order metrics safely for all members
    TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), TIMESTAMP(m.signup_date), DAY) AS tenure_days,
    COALESCE(ord_agg.lifetime_orders, 0) AS lifetime_orders,
    COALESCE(ord_agg.lifetime_gmv_usd, 0) AS lifetime_gmv_usd,
    COALESCE(ord_agg.trailing_12mo_gmv_usd, 0) AS trailing_12mo_gmv_usd,
    COALESCE(ord_agg.trailing_12mo_orders, 0) AS trailing_12mo_orders,
    -- Benefit adoption count from membership events
    COALESCE(ben_agg.benefits_adopted_count, 0) AS benefits_adopted_count,
    -- Active flag evaluation
    CASE WHEN m.status = 'active' THEN TRUE ELSE FALSE END AS is_active,
    -- Projected CLTV calculation incorporating zero-order members
    COALESCE(ord_agg.trailing_12mo_gmv_usd, 0) + (
        CASE 
            WHEN m.plan_type = 'annual' THEN m.plan_price_usd * 2.5 
            else m.plan_price_usd * 1.8 
        end
    ) AS projected_cltv_usd
FROM
    `nexus-analyst-demo.acme_ecomm.dim_member` m
LEFT JOIN (
    SELECT
        member_id,
        COUNT(order_id) AS lifetime_orders,
        SUM(gmv_usd) AS lifetime_gmv_usd,
        SUM(CASE WHEN order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH) THEN gmv_usd ELSE 0 END) AS trailing_12mo_gmv_usd,
        COUNT(CASE WHEN order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH) THEN order_id END) AS trailing_12mo_orders
    FROM
        `nexus-analyst-demo.acme_ecomm.fact_orders`
    WHERE member_id IS NOT NULL
    GROUP BY member_id
) ord_agg ON m.member_id = ord_agg.member_id
LEFT JOIN (
    SELECT
        member_id,
        COUNT(DISTINCT benefit_code) AS benefits_adopted_count
    FROM
        `nexus-analyst-demo.acme_ecomm.fact_membership_events`
    WHERE event_type = 'benefit_redeemed'
    GROUP BY member_id
) ben_agg ON m.member_id = ben_agg.member_id
```

---

## 4. The $500 vs. $625 Join Trap

The operational danger of writing an intuitive-seeming query—or using an unvetted dbt base model—is the **INNER JOIN trap**. 

If an analyst writes an `INNER JOIN` between `dim_member` and `fact_orders` (or forgets to wrap trailing aggregates in `COALESCE(..., 0)`), the database will silently drop all 24,000 dormant members (such as Marisol, `mem_1000178`) because they have no matching rows in `fact_orders` for the trailing 12 months. 

When you compute the panel's average CLTV across these two different query constructions, the financial distortion becomes immediately apparent:

* **The Wrong Way (`INNER JOIN`):** By filtering out the 24,000 zero-order members, the query calculates average CLTV exclusively across the 80% active shopping base. This yields an inflated average CLTV of **$625 per member**.
* **The Right Way (`LEFT JOIN` + `COALESCE(0)`):** By including the full 120,000-member panel—properly accounting for members with $0 trailing-12-month merchandise spend while still capturing their subscription fee contributions—the true average CLTV is **$500 per member**.

**The Impact:** An inner join introduces a **25% overstatement** in our customer lifetime value metrics. More dangerously, it completely erases the dormant population from the data layer, leaving product teams like derek.holloway's and simone.laurent's blind to a massive segment of paying subscribers who are at severe risk of silent churn when their annual renewals cycle around.

---

## 5. Broader Context & Related Modeling Notes

* **Benefit Adoption Linkage:** As noted in our membership analytics, the risk of a dormant member ultimately cancelling spikes dramatically if they are not engaged with program benefits. Members using 2+ Acme+ benefits show a 95% renewal rate, compared to just 71% for free-shipping-only members. Furthermore, while our streaming perk migration from Vidora to Reelstream on June 1st has maintained strong category-level retention (93% for streaming users), awareness remains stubbornly low at 34%. Derek Holloway's recent `exp_2556` ("Benefit Onboarding Carousel," which concluded on June 15th with a +9pp lift in 30-day benefit awareness) is a step in the right direction, but tackling the dormant population will require targeted re-engagement campaigns rather than passive onboarding.
* **Comparison with Other Verticals:** While US_CONV grapples with session definition changes (`sessions_definition_version` 1→2 implemented back on March 2, 2026 by wei.hartono) and Marketplace navigates internal wallet-share shifts between Style and Resold, the Membership vertical's primary analytical hazard is this exact join trap. Always verify that your downstream dashboards reference `nexus-analyst-demo.acme_ecomm.member_cltv` directly rather than building ad-hoc joins on `dim_member`.

---
