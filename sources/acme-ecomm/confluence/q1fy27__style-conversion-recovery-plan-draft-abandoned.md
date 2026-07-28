---
title: "Confluence draft (undated, circa Q1FY27): 'Style Conversion Recovery Plan' — never actioned"
source_url: "internal://acme-ecomm/confluence/q1fy27__style-conversion-recovery-plan-draft-abandoned"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-04-15T12:00:00+00:00'
adapter: confluence_page
---

# Style Conversion Recovery Plan (DRAFT - For Review & Discussion Only)

**Author:** ines.delgado (Sr PM Marketplace Style)  
**Status:** Draft / Under Discussion (Circulated circa mid-Q1FY27)  
**Target Vertical:** `MARKETPLACE` (Style Sub-vertical)  
**Associated Accounts Cited:** Kestrel & Vine (`sel_500103`), Northfield Apparel Co. (`sel_500034`)  

---

## 1. Executive Summary & Problem Statement

As we navigate through the first half of Q1FY27, the Marketplace Style sub-vertical is experiencing a noticeable deceleration. While our broader marketplace ecosystem continues to expand aggressively—fueled largely by viral momentum in Collectibles and exceptional recommerce tailwinds in Resold—Style GMV pacing is currently tracking toward roughly **+6% YoY** this quarter. This sits significantly below our planned ~10% growth trend established during the FY27 target-setting cycle.

Traffic to Style category pages has softened slightly, and seller velocity among key mid-tier and large accounts has plateaued. For example, major accounts like Kestrel & Vine (`sel_500103`) have reported scaling friction, citing merchandising bottlenecks and listing optimization challenges that are dampening conversion rates. 

Because our Trust & Safety and compliance engineering resources have been heavily allocated toward Collectibles since last autumn's counterfeit spike and the subsequent rollout of the "Acme Verified" program (managed by lucia.ferreira), Style has operated with minimal dedicated T&S operational support. 

This draft proposes an immediate, targeted reallocation of Trust & Safety headcount from Collectibles to Style to stabilize conversion rates, streamline seller onboarding friction, and protect our Q1/Q2 revenue trajectory.

---

## 2. Background: The Style Growth Bottleneck

While Collectibles has rightly absorbed immense engineering and policy focus following the viral vintage-card auction surge last August and the subsequent GradeSure integration, Style has quietly stalled. 

Reviewing our recent cohort performance in `fact_marketplace_listings` and `marketplace_seller_performance`, Style sellers are encountering distinct operational hurdles:
1. **Listing Setup Complexity:** Sellers attempting to expand multi-variant apparel catalogs face manual data-entry bottlenecks.
2. **Quality Compliance False Positives:** Unlike Collectibles—which requires strict GradeSure authentication for every high-value item—Style listings occasionally get snagged in automated compliance filters looking for brand authenticity mismatches, creating unnecessary listing suspensions.
3. **Account Rep Coverage:** Key large accounts, particularly Kestrel & Vine (`sel_500103`), have expressed frustration over sluggish dispute resolution for listing holds. (By contrast, mid-tier accounts like Northfield Apparel Co. (`sel_500034`), owned by ronnie.aldridge, have maintained relatively stable volume, but lack growth accelerators).

```sql
-- Diagnostic query used to check Style active listings vs trailing GMV pacing
SELECT 
    s.seller_id,
    s.seller_name,
    COUNT(l.listing_id) AS active_listings,
    SUM(l.price_usd) AS total_listed_value
FROM nexus-analyst-demo.acme_ecomm.dim_seller s
JOIN nexus-analyst-demo.acme_ecomm.fact_marketplace_listings l ON s.seller_id = l.seller_id
WHERE s.category_focus = 'style'
  AND l.status = 'active'
GROUP BY 1, 2
ORDER BY total_listed_value DESC
LIMIT 10;
```

---

## 3. Proposed Action: Headcount Reallocation

We propose shifting 2.5 full-time equivalent (FTE) Trust & Safety compliance analysts from the Collectibles verification queue over to the Style sub-vertical, effective immediately for the remainder of Q1FY27. 

**Justification:**
- Collectibles return rates have stabilized impressively down to ~5.4% (Q2FY27 QTD view), showing that the GradeSure integration and Verified Badge rollout are maturing nicely and no longer require emergency-level triage capacity.
- Conversely, Style's +6% YoY pace threatens our vertical contributions to the total digital + marketplace GMV target ($7.53B). 
- Reallocating these resources will allow camille.duarte (who recently joined as Sr PM Marketplace Seller Experience) and ines.delgado to partner directly on automated compliance clearing for apparel catalogs, directly unblocking accounts like Kestrel & Vine (`sel_500103`).

---

## 4. Expected Impact

- **Conversion Lift:** Estimated +45bps to +75bps improvement in Style item-page conversion rates through reduced listing friction and faster resolution of false-positive holds.
- **Seller Retention:** Decrease monthly churn among mid-to-large Style tier sellers by cutting dispute resolution turnaround times from 72 hours to under 24 hours.

---
---

## Comments & Discussion Thread

**lucia.ferreira** (2026-03-12, 14:22 ET):
> Ines, I understand where you're coming from on the Style pacing numbers, but pulling 2.5 FTEs out of Collectibles right now feels premature. Even though our return rates dropped to 5.4%, we are still seeing high volumes of onboarding friction for new sellers coming through the GradeSure pipeline (remember sel_500241 and that whole cohort). If we strip T&S coverage from Collectibles, we risk a resurgence of the counterfeit issues we fought so hard to contain last fall. Can we look at borrowing contractor hours instead?

**victor.okonkwo** (2026-03-13, 09:10 ET):
> Good discussion. Let's make sure we aren't robbing Peter to pay Paul here. The Marketplace total GMV run-rate is pacing extremely well overall (~$3.89B run-rate against our $3.32B goal), and as we've seen in the broader cross-vertical data, some of what's happening in Style is actually a portfolio shift toward Resold (+90.9% YoY) rather than pure demand destruction. Let's pull some fresh Compass and BigQuery cuts before we start moving permanent headcount around. Ines, let's sync on this at our next 1:1.

**carlos.figueroa** (2026-03-14, 11:45 ET):
> Just a quick technical note: if anyone is querying the mart tables for this analysis, make sure you're hitting `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary` directly for the full population aggregates rather than doing local sums on `fact_orders` (remember convention 5 on the sample panels). Also, watch out for cached views in Compass—the Q4 numbers were restated back in Feb to $975.0M, so ensure your dashboards are refreshed.

**ines.delgado** (2026-03-14, 16:00 ET):
> Thanks everyone. Lucía, I take your point on the Collectibles onboarding queue—it's definitely a tightrope. Victor, I'm happy to review the Resold cannibalization overlap with Noah's numbers before we make any formal personnel requests. Let's keep this draft open for feedback through the weekend.

---
*(Note: This page was marked as superseded following subsequent cross-vertical synthesis in late March and was never formally actioned or escalated to leadership.)*
