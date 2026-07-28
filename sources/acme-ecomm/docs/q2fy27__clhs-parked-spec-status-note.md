---
title: "Status note: 'Customer Lifetime Health Score' (CLHS) remains a parked/draft spec"
source_url: "internal://acme-ecomm/docs/q2fy27__clhs-parked-spec-status-note"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: confluence_page
---

# Status note: 'Customer Lifetime Health Score' (CLHS) remains a parked/draft spec

**Owners:** `derek.holloway` (Sr PM Membership Benefits & CLTV), `renee.kowalski` (SVP Membership)  
**Date:** July 20, 2026  
**System of Record:** Confluence / Core Internal Documentation (`acme_ecomm`)  
**Status:** **PARKED / DRAFT** (No changes since Q3FY26 freeze; see canonical signal `[clhs-parked]`)

---

### Purpose of this Note

With Q2FY27 MBR preparations and mid-year membership reviews ramping up across the business, references to a composite metric called the **"Customer Lifetime Health Score" (CLHS)** have begun reappearing in cross-functional Slack channels (notably `#membership-strategy` and `#growth-analytics-sync`). 

Because several newer data analysts and product managers rotating into the Membership and Care verticals have asked for the data dictionary path or BigQuery table name for CLHS, this document serves as the official, citable company-wide reference confirming the following hard fact:

> **CLHS does not exist in the `nexus-analyst-demo.acme_ecomm` warehouse. There is no table, no view, and no column for CLHS.** 

Per carlos.figueroa and renee.kowalski's leadership sign-off back in September 2025 (see LEDGER entry `2025-09-10`), the CLHS spec was formally **parked in draft status** due to analytics bandwidth constraints and competing priorities heading into the Q4FY26 peak and FY27 roadmap execution. It has not been unsuspended. Any dashboard, ad hoc script, or documentation referencing a raw "CLHS score" or "health tier band" is utilizing local, unapproved mock data or confusing it with shipped proxies.

---

### The Shipped Operational Proxy: What to Use Instead

If you are building reporting or analyzing member health, engagement, or retention risk, you must use the existing canonical mart and metrics. Do not invent or request a CLHS column. 

The officially supported composite proxy for member health combines two existing, production-grade components:

1. **`member_cltv` (Table / Mart):** Located at `nexus-analyst-demo.acme_ecomm.member_cltv`. This is the board source for member lifetime value, built using the canonical `LEFT JOIN dim_member TO fact_orders` pattern with `COALESCE(trailing_12mo_gmv_usd, 0)` (refer to signal `[cltv-join-drop]` to ensure dormant members with zero trailing orders are not improperly dropped via an inner join). It provides `lifetime_orders`, `lifetime_gmv_usd`, `trailing_12mo_gmv_usd`, and `projected_cltv_usd`.
2. **Benefit-Adoption Rate (`benefits_adopted_count`):** Tracked via `fact_membership_events`. As demonstrated in recent analyses by derek.holloway following the conclusion of the "Benefit Onboarding Carousel" experiment (`exp_2556`) in June 2026, benefit adoption is the single most powerful leading indicator of renewal and lifetime health:
   * Members using **0 extra benefits** (free shipping only) renew at **71%**.
   * Members using **1 benefit** renew at **89%**.
   * Members using **2+ benefits** renew at **95%**.
   * (Note on the streaming perk: While the transition from Vidora to Reelstream on June 1, 2026, successfully migrated streaming-bundle users who show a 93% renewal rate standalone, awareness remains constrained at roughly 34%, making targeted benefit onboarding far more impactful than building a speculative composite score like CLHS).

---

### Context & Background on Why CLHS Was Parked

For those wondering *why* the spec was shelved when it keeps coming up in strategic discussions about churn-risk members (such as archetype `mem_1000390` or dormant accounts like `mem_1000178`), the decision was made during the Q3FY26 planning cycle because our current data architecture achieves the exact same diagnostic utility without adding another opaque, black-box composite score to the warehouse.

As amara.shah and wei.hartono noted during the flat-dataset migration and subsequent MBR syncs, composite health scores tend to obscure the underlying drivers—such as whether a member is failing to adopt 2+ benefits, experiencing fulfillment delays (like the Ontario returns center Ontario-hub backlog issues that rippled through Care verbatims late last year), or suffering from lack of awareness regarding perks like the Reelstream partnership.

#### Related Ongoing Work (Do Not Confuse With CLHS)
* **Aitable to Jira Roadmap Consolidation:** Managed by nadia.esposito since January 2025 (`2026-01-15`), legacy ideation cards from the pre-2026 era (including early drafts of CLHS in Aitable) are archived. Active, committed roadmap items live exclusively in Jira. CLHS does not appear in Jira.
* **Q2FY27 Pacing:** As of our snapshot date (July 20, 2026, with Q2FY27 at 88.0% elapsed), total Acme+ members stand at **14.62M** (pacing toward the FY27 exit goal of 14.8M) with an annual renewal rate of **87.2%** (beating the 86.0% target). These numbers are derived directly from aggregate membership marts and the company-section baseline, reinforcing that our existing metrics (`member_cltv` and benefit counts) are fully sufficient for executive visibility without needing CLHS.

---

### Action Items / Next Steps

1. **If you see "CLHS" in a query or slide deck:** Please flag it to `derek.holloway` or `renee.kowalski`. It is a stale reference to a parked draft spec.
2. **For analyses requiring health/retention segmentation:** Query `nexus-analyst-demo.acme_ecomm.member_cltv` directly, ensuring proper use of `COALESCE` for dormant panel accounts, and cross-reference with `fact_membership_events` for benefit adoption counts.
3. **Do not create local SQL views** attempting to recreate CLHS without coordinating through the Data & Analytics team (`carlos.figueroa` / `wei.hartono`), as unvetted scores violate reporting hierarchy and will not reconcile with MBR deck figures.

---
*End of status note. Maintained in the `acme_ecomm` documentation repository under general system docs.*
