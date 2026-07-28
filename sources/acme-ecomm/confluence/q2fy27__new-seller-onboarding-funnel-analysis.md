---
title: "Confluence analysis: the New-Seller Onboarding Funnel, full stage-by-stage data"
source_url: "internal://acme-ecomm/confluence/q2fy27__new-seller-onboarding-funnel-analysis"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: confluence_page
---

# Confluence analysis: the New-Seller Onboarding Funnel, full stage-by-stage data

**Author:** `camille.duarte` (Sr PM Marketplace Seller Experience)  
**Data Extraction & SQL Engineering:** `wei.hartono` (Analytics Engineer)  
**Status:** Published (Companion to Q2FY27 Marketplace Ops Review)  
**Parent Space:** `acme-ecomm/marketplace/seller-ops`  
**Related Documents:** `q2fy27-marketplace-ops-review` (MBR deck), `fact_seller_voc_responses-schema-ref`  

---

## 1. Executive Summary & Context

Following this week’s MBR deck presentations and continuing our deep-dive review into marketplace seller dynamics—building directly on the discussions from our recent seller-ops review sessions—this page serves as the direct, load-bearing quantitative source for the new-seller onboarding funnel figures. During our recent cross-vertical syncs (building on the discussions led by `victor.okonkwo` and `camille.duarte` since launching the Seller Pulse survey program back in April 2026), leadership requested a fully disaggregated, stage-by-stage breakdown of how new sellers transition from initial application through active, sustained catalog management across our three marketplace sub-verticals: **Collectibles**, **Resold**, and **Style**.

To ensure these percentages reflect completed lifecycles rather than short-term noise, we have scoped this analysis precisely to the ~500-seller new-seller stratum of the `dim_seller` panel where `application_date` is fully populated, focusing exclusively on cohorts onboarded between **Q3FY26 and Q4FY26**. This guarantees every seller in the analysis window has enjoyed at least ~5.6 months of runway to "today" (July 20, 2026), giving them ample time to clear or churn out of the core milestones. Sellers onboarded in Q1FY27 and Q2FY27 remain active in the panel and appear in operational feeds, but they are excluded from these specific percentage conversion tables as right-censored/still-maturing cohorts.

As we observed when reviewing the seller-side VOC data (`fact_seller_voc_responses`), authentication overhead heavily skews the Collectibles funnel, while Resold and Style progress much more fluidly through the early listing thresholds. Below is the full dataset, methodology, and the secondary listing-quality signals we must monitor in tandem.

---

## 2. Full Stage-by-Stage Onboarding Funnel Table

Unlike traditional calendar-tenure analyses, this funnel is defined strictly by **listing count** thresholds. A seller's progression is measured by the total number of unique listings they have successfully posted, independent of how many calendar days elapsed between listing 1 and listing 10.

*Dataset Reference:* Query executed against `nexus-analyst-demo.acme_ecomm.dim_seller` joined with `fact_marketplace_listings`.

| Funnel Stage | Collectibles Strata (n=200) | Resold Strata (n=150) | Style Strata (n=150) |
|---|---|---|---|
| **Applied → Onboarded (Listing 1)** | 100% (200 / 200) | 100% (150 / 150) | 100% (150 / 150) |
| **Reached Listing 5** | 46% (92 / 200) | 74% (111 / 150) | 76% (114 / 150) |
| **Reached Listing 10** | **24% (48 / 200)** | **46% (69 / 150)** | **48% (72 / 150)** |
| **Sustained** *(10+ listings AND ≥1 new listing in trailing 90d)* | **19% (38 / 200)** | **40% (60 / 150)** | **42% (63 / 150)** |

### Key Observations on the Funnel Shape:
1. **The Collectibles Divergence:** While Style and Resold mirror each other closely—dropping off gradually between listing 1 and listing 5, then stabilizing somewhat through listing 10—Collectibles suffers a catastrophic drop-off immediately following onboarding. More than half of all new Collectibles sellers ($54\%$) fail to even reach their 5th listing, and only **$24\%$** ever cross the 10-listing threshold.
2. **The Verification-Speed Split:** Drilling deeper into the Collectibles cohort reveals why some survive while others stall. Of the 200 Collectibles sellers in the cohort, exactly 120 ($60\%$) managed to get their debut listing authenticated by GradeSure within 7 days. That "fast verification" subgroup reaches listing 10 at **$30\%$** ($36$ sellers). Conversely, the remaining 80 sellers ($40\%$) who experienced slower initial verifications reach listing 10 at only **$15\%$** ($12$ sellers). Combined ($36 + 12 = 48$), this reconciles perfectly to the overall $24\%$ cohort figure. 
3. **The Two-Sided Tension:** As `lucia.ferreira` and our Trust & Safety teams have noted, the "Acme Verified" program (GradeSure partnership) is a massive win for buyer trust—driving Collectibles return rates down from an alarming $11.2\%$ peak in Q3FY26 to a healthy $5.4\%$ in Q2FY27 QTD. However, it imposes severe friction on new sellers who have not yet optimized their submission workflows, directly suppressing early-stage retention in that category.

---

## 3. Qualitative Signals & Seller-Side VOC Correlation

To triangulate these quantitative drop-offs, `wei.hartono` pulled verbatim extracts from `fact_seller_voc_responses` (our separate survey stream using the Seller Pulse instrument, distinct from buyer-side Medallia data). The theme distribution across onboarding pulse respondents confirms our operational hypotheses:

- **`authentication-friction`** dominates Collectibles onboarding surveys at **~38%** of all verbatims, compared to just ~5% for Style and ~6% for Resold (neither of which requires pre-listing authentication).
- **`listing-setup-complexity`** appears uniformly across all three categories at **15%–20%**, hitting sellers hardest between listing 1 and listing 5 due to the current lack of robust bulk-upload and duplicate-listing tools.
- **`no-performance-visibility`** surfaces in **12%–18%** of responses among sellers who successfully reached listings 5 through 10, indicating that sellers who survive the initial setup phase hit a secondary wall where they cannot diagnose why their active catalog isn't converting.

### The Listing-Quality Confound (`status='removed'`)
Beyond authentication delays, analyzing `fact_marketplace_listings.status` uncovers a second, separate input stream worth tracking: early listings that land directly in `status='removed'` due to quality or compliance violations. Regardless of category, a new seller who incurs a compliance removal on their very first or second listing exhibits a churn probability nearly 3x higher within 30 days, completely independent of whether they sell Collectibles or Style. This suggests our automated guardrails are catching bad-faith or non-compliant inventory early, but we currently lack an educational remediation loop to teach compliant sellers *why* a listing failed before they walk away entirely.

---

## 4. Methodology Appendix & SQL Extract Notes

For any analysts looking to reproduce or audit these figures for upcoming MBR decks, please adhere strictly to the warehouse definitions established by Data & Analytics:

1. **Table Path:** Query against `nexus-analyst-demo.acme_ecomm.dim_seller` and join with `fact_marketplace_listings`. Do *not* attempt to query nested experimental datasets; our BigQuery dataset is strictly flat per architecture guidelines (`flat-dataset`).
2. **Panel vs. Population:** Remember that `dim_seller` is a representative panel (~2,560 active rows) rather than the full global population (~38,000 true sellers). Absolute counts in the table above reflect panel representation ratios and should not be scaled linearly to represent total marketplace GMV without applying the appropriate weighting factors maintained in `marketplace_gmv_summary`.
3. **Right-Censoring Exclusion:** Do not include sellers with `onboarded_date` falling in Q1FY27 or Q2FY27 when calculating completed-funnel conversion percentages. Doing so artificially deflates the tier-reaching rates because those newer cohorts have simply not had time to post 10 listings yet.

```sql
-- Example reference query snippet used for validation by wei.hartono
SELECT
  category_focus,
  COUNT(DISTINCT s.seller_id) AS cohort_size,
  COUNT(DISTINCT CASE WHEN listing_sequence >= 5 THEN s.seller_id END) AS reached_l5,
  COUNT(DISTINCT CASE WHEN listing_sequence >= 10 THEN s.seller_id END) AS reached_l10,
  COUNT(DISTINCT CASE WHEN listing_sequence >= 10 AND has_recent_listing THEN s.seller_id END) AS sustained
FROM `nexus-analyst-demo.acme_ecomm.dim_seller` s
INNER JOIN (
  SELECT seller_id, COUNT(listing_id) as listing_sequence,
         MAX(case when listed_date >= DATE_SUB('2026-07-20', INTERVAL 90 DAY) then 1 else 0 end) as has_recent_listing
  FROM `nexus-analyst-demo.acme_ecomm.fact_marketplace_listings`
  GROUP BY seller_id
) l ON s.seller_id = l.seller_id
WHERE s.application_date IS NOT NULL
  AND s.onboarded_date BETWEEN '2025-08-01' AND '2026-01-31'
GROUP BY 1;
```

---

## 5. Open Questions for the Next Cohort (Q1FY27+ Maturation Study)

As we look toward closing out Q2FY27 and preparing our H2 planning docs, several operational questions remain open for `camille.duarte`, `victor.okonkwo`, and the product team:

1. **Can we implement a graded grace period for GradeSure authentication?** Given that fast verification doubles listing-10 survival in Collectibles (30% vs 15%), should we build a temporary "pending verification" visibility state that allows low-risk or returning sellers to accumulate their first 3 draft listings without triggering immediate drop-off?
2. **Where does `listing-setup-complexity` fit in our Jira backlog?** With Nadia Esposito's Aitable-to-Jira roadmap migration project ongoing, bulk-upload tooling remains split across disparate epic tickets. We need a unified PM owner to bridge seller listing and seller optimization surfaces.
3. **How will right-censored Q1FY27 cohorts behave as they cross the 6-month mark in August/September?** Early preliminary tracking suggests that Q1FY27 onboarding volume is up ~14% YoY, but their early-stage drop-off curves are tracking identically to the Q3-Q4 cohorts, confirming that authentication friction and setup complexity are structural rather than seasonal anomalies.

---
*Document status: Archival Confluence snapshot locked for Q2FY27 MBR audit. Comments are open via Confluence inline markup.*
