---
title: "Jira backlog export: Style's complete current initiative list (5 items)"
source_url: "internal://acme-ecomm/jira/q2fy27__style-marketplace-backlog-current-initiatives"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: jira_ticket
---

# JIRA BOARD EXPORT: MARKETPLACE STYLE SUB-VERTICAL

**Project:** Marketplace Style (MS)
**Board Filter:** `project = "STYLE" AND status != Done`
**Export Date:** Monday, 2026-07-20
**Board Owner / Lead PM:** `ines.delgado` (Ines Delgado, Sr PM Marketplace Style, `assoc_100121`)
**Sprint Context:** Sprint 27.4 (Active, ending 2026-07-24)

---

## Board Overview & System Notes

*Note from ines.delgado (2026-07-15):* Following the Confluence synthesis in April that formally superseded the old "Style Conversion Recovery Plan" draft and confirmed our Q1FY27 Style deceleration (+6.1% YoY) was part of a broader Marketplace wallet-share shift toward Resold (+90.9% YoY) rather than a localized demand failure, we have frozen any exploratory headcount-shifting initiatives. Our current roadmap is strictly bounded to the 5 committed epics below. No additional epics will be added this quarter. 

As a reminder following our migration to Jira last January (part of nadia.esposito's `aid-jira-migration-proj`), all active engineering execution for Style lives here. Legacy Aitable cards for these initiatives have been fully archived.

---

## Active Backlog Items (5 of 5)

### 1. STYLE-1041: Size-Chart Standardization Across Supplier Catalogs
* **Epic Name:** Size-Chart Standardization & Data Uniformity
* **Status:** In Progress
* **Assignee:** `camille.duarte` (co-supported by Style engineering)
* **Target Quarter:** Q3FY27
* **Story Points:** 34 pts (Remaining: 12 pts)
* **Description:** 
  Suppliers in the Style catalog currently submit sizing in disparate localized formats (US numeric, Alpha, European, and regional waist/bust dimensions), directly driving size-related cart abandonment and post-purchase returns. This initiative builds a canonical attribute normalization layer across supplier data ingestion feeds. 
  *Current Sprint Progress:* Mapping standardized international conversion tables for top 50 apparel brands. Initial dry-runs against `fact_marketplace_listings` show a projected 14% reduction in size-mismatch inquiries once fully deployed.
  
  *Comments:*
  * *ines.delgado [2026-07-12]:* Make sure we coordinate with the POR team on how this feeds down-stream into our return-reason taxonomy cleanup (STYLE-1045). We need to ensure the new normalized attributes match the new sub-codes.
  * *camille.duarte [2026-07-14]:* Sizing feedback from Seller Pulse verbatims (`fact_seller_voc_responses`) indicates smaller suppliers are struggling with the bulk mapping template. Let's make sure the upcoming docs cover self-service mapping.

### 2. STYLE-1088: Promo-Calendar Automation for Flash Sales
* **Epic Name:** Automated Flash Sale Promo Engine
* **Status:** Planned / Groomed
* **Assignee:** Unassigned (Engineering Queue)
* **Target Quarter:** Q3FY27
* **Story Points:** 21 pts
* **Description:** 
  Manual curation and discount-code application for Style flash sales and weekend drops currently requires heavy manual intervention from merchandising ops. This epic creates an automated scheduling service integrated with `dim_marketing_calendar` to trigger price overrides, badge applications, and homepage merchandising slots dynamically.
  
  *Comments:*
  * *maya.lindqvist [2026-06-18]:* Ensure this doesn't overlap with US_CONV homepage modules. As we saw during the recent Homepage Hero Banner Refresh launch on July 13th, clean isolation between merchandising slots and global site modules is critical to avoid attribution noise.

### 3. STYLE-1102: Influencer / UGC Content Licensing Pilot
* **Epic Name:** UGC & Influencer Video Content Integration
* **Status:** In Progress
* **Assignee:** `ines.delgado`
* **Target Quarter:** Q2FY27 (Closing out)
* **Story Points:** 18 pts (Remaining: 3 pts)
* **Description:** 
  Pilot program to ingest, verify, and display third-party creator video reviews directly on Style item pages. Designed to increase engagement and counteract the engagement dips seen on static image galleries. 
  
  *Comments:*
  * *ines.delgado [2026-07-18]:* Keeping a close eye on fullstory notes here. We want to avoid the kind of user friction recently observed on the item-page media carousel autoplay experiment (`exp_2618`), where intrusive video elements backfired with a -1.5% conversion drag. UGC must remain user-initiated or gracefully muted.

### 4. STYLE-1124: Category-Page Filters for Sustainability & Material Tags
* **Epic Name:** Sustainability & Eco-Material Faceted Search
* **Status:** Planned
* **Assignee:** Unassigned
* **Target Quarter:** Q4FY27
* **Story Points:** 26 pts
* **Description:** 
  In response to rising consumer demand for traceable apparel materials (organic cotton, recycled polyester, ethical wool), introduce dedicated faceted navigation filters on Style category landing pages. Requires backend tagging audit across active Style listings (`fact_marketplace_listings`).

### 5. STYLE-1045: Returns-Reason Taxonomy Cleanup (Joint w/ POR)
* **Epic Name:** Returns Taxonomy & Root-Cause Tagging Alignment
* **Status:** In Progress
* **Assignee:** `ines.delgado` (Joint ownership with Post-Order Returns / POR team)
* **Target Quarter:** Q3FY27
* **Story Points:** 15 pts (Remaining: 8 pts)
* **Description:** 
  Joint initiative with the Post-Order Returns vertical and Care (`hannah.brennan`, `giulia.romano`) to overhaul the granular return-reason code structure in `fact_orders`. Current broad buckets ("doesn't fit", "not as pictured") mask the true operational drivers. 
  
  *Comments:*
  * *hannah.brennan [2026-07-02]:* Critical follow-up from the Ontario returns hub crisis earlier this year—having clean taxonomy data is the only way we will catch verbatim surges in Medallia before they breach SLAs like we did back in January.
  * *ines.delgado [2026-07-10]:* Note that while this touches listing description accuracy in conversation, this epic specifically covers *return reason codes*, not the broader `listing-accuracy-gap` Medallia verbatim theme — that's a separate conversation entirely. We must keep scope tight.

---
