---
title: "Jira ticket: Bramblewood Vintage (sel_500089) reinstated after compliance review"
source_url: "internal://acme-ecomm/jira/q4fy26__bramblewood-vintage-reinstatement-compliance-review"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-01-25T12:00:00+00:00'
adapter: jira_ticket
---

**Jira Issue:** MKT-8492  
**Project:** Marketplace Trust & Safety (MKT)  
**Issue Type:** Task / Compliance Review Closeout  
**Status:** Closed / Resolved  
**Priority:** P2 - Normal  
**Assignee:** lucia.ferreira (Trust & Safety Lead, Marketplace, assoc_100320)  
**Reporter:** lucia.ferreira  
**Component:** Seller Verification & Compliance  
**Labels:** `marketplace`, `seller-compliance`, `counterfeit-mitigation`, `bramblewood-vintage`, `reinstatement`  
**Created:** 2025-09-02  
**Updated:** 2026-01-15  
**Resolved:** 2026-01-15  

---

### Description

Closing out the compliance review and formal suspension record for **Bramblewood Vintage (sel_500089)**, originally flagged on 2025-08-12 following three separate counterfeit-listing violations during the viral vintage-card auction surge, and subsequently suspended on 2025-09-02 pending a full documentation and inventory audit. 

Following the implementation of the "Acme Verified" authentication program launched alongside GradeSure on 2025-09-08—which successfully drove Collectibles return rates down from their Q3FY26 peak of 11.2% to a stable 5.4% run-rate by Q2FY27—Bramblewood Vintage submitted its remediation package on 2026-01-03. 

The review required:
1. **Comprehensive Documentation Audit:** Verification of wholesale supply chain invoices, provenance certificates, and direct-acquisition receipts for all active and archived Collectibles inventory.
2. **Corrected Sourcing Practices:** Mandatory onboarding into the GradeSure pre-listing verification workflow, ensuring zero unverified high-value inventory enters the catalog without clearing the badge check (noting that new-seller cohorts in Collectibles face a steeper climb, with verification speed directly impacting whether a seller reaches listing 10).
3. **Internal Policy Retraining:** Completion of Acme Marketplace Counterfeit Prevention & Authenticity Modules by the seller's primary account operators.

### Conditions of Reinstatement
* **Probationary Monitoring Period:** The seller account is placed on a 90-day enhanced monitoring window effective today (2026-01-15 through 2026-04-15). Any flagged authenticity mismatch or customer-facing `listing-accuracy-gap` VOC verbatim linked to this account during the probation window will trigger an immediate, permanent offboarding without right of appeal.
* **Listing Caps:** Initial catalog relisting is capped at 50 active items for the first 30 days to test throughput against the GradeSure authentication pipeline.

---

### Comments & Activity Log

**lucia.ferreira** added a comment — 2026-01-01 10:15 PST  
> Quick administrative note while we wrap this up: please ensure we cross-reference the updated `dim_seller` status table updates before pushing the API state change. Also, checking in with victor.okonkwo regarding our backlog prioritization for high-tier Collectibles restoration. Since the viral auction spike last August, we’ve learned quite a bit about how new vs. tenured sellers interact with the GradeSure workflow. Bramblewood is a legacy account, so they had existing operational muscle, but their supply chain documentation was a mess. 

**carlos.figueroa** added a comment — 2026-01-02 11:42 PST  
> Just a reminder for everyone on the data side—make sure your BigQuery extractions aren't querying nested schemas. Remember the dataset is flat (`nexus-analyst-demo.acme_ecomm.<table>`). I had to field three separate Slack pings this morning from analysts trying to hit non-existent paths like `acme_ecomm.marts.membership.member_cltv` instead of the flat mart. Let's keep our queries clean.

**nadia.esposito** added a comment — 2026-01-15 09:00 PST  
> FYI team, today marks our official cutover from Aitable to Jira as our primary roadmap and tracking system. Legacy Aitable cards will continue to be migrated over organically, but all new compliance reviews and trust tasks like this one should live fully inside Jira moving forward. 

**lucia.ferreira** resolved the issue — 2026-01-15 16:30 PST  
> **Resolution:** Done  
> All remediation artifacts verified, GradeSure integration confirmed active for seller `sel_500089`, and the 90-day probationary monitoring period has been initialized in the marketplace oversight dashboard. Reinstating seller profile effective immediately.

---
