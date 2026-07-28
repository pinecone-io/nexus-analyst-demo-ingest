---
title: "Aitable roadmap export: Care and Marketplace initiative cards (legacy tracker, Q1FY26)"
source_url: "internal://acme-ecomm/aitable/q1fy26__legacy-roadmap-care-marketplace-cards"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2025-04-15T12:00:00+00:00'
adapter: aitable_card
---

# Aitable Export: Care & Marketplace Initiatives (Q1FY26 Active Snapshot)
*Exported by product-ops-bot on behalf of nadia.esposito (Head of Product Operations).*
*Note on tooling:* As a reminder to the team following the FY26 kickoff leadership sync and SVP staff alignment meeting, while engineering execution, sprint backlogs, and bug tracking are moving over to Jira, roadmap ideation, high-level capability scoping, and cross-functional card sorting for Care and Marketplace still live right here in Aitable pending full migration (adapter: `aitable_card`). Please do not delete legacy cards until the workspace cleanup sprint is formally scheduled later in the year.

---

## Workspace: CARE (Sub-verticals: Automate, Avoid, Optimize, Platform, W+)
*Administered by nadia.esposito / Leadership sponsor: hannah.brennan (SVP Customer Care)*

### 1. Card ID: CARE-882
- **Title:** Automate post-delivery return label generation via chat intent classifier
- **Owner:** aisha.rahman (Director PM Care, Automate/Avoid)
- **Status:** In Progress
- **Target Quarter:** Q1FY26
- **Linked Doc:** `confluence://acme-ecomm/care/automate-return-label-prd-v1`
- **Notes:** Aisha notes that chat logs from late last week show customers dropping off right when asked for order numbers. Need to check if the session timeout is too aggressive. Also, reminder that we need to coordinate with gabriel.stroud's fulfillment team once the returns center automation work starts picking up speed later in the summer, though for now this is purely bot-side intent routing.

### 2. Card ID: CARE-904
- **Title:** Optimize agent dashboard side-panel latency for multi-item orders
- **Owner:** julian.moss (Sr PM Care, Optimize/Platform)
- **Status:** Backlog
- **Target Quarter:** Q2FY26
- **Linked Doc:** `confluence://acme-ecomm/care/agent-panel-latency-audit`
- **Notes:** Julian is OOF on Thursday for dentist, but left a comment saying giulia.romano in Data ran some preliminary SQL queries showing median load times creeping past 4.2 seconds on enterprise accounts. Pushed to Q2 because engineering bandwidth is tied up with platform migration tasks. 

### 3. Card ID: CARE-915
- **Title:** W+ Priority Member Care routing rule update
- **Owner:** dominic.paquet (Care Ops Lead)
- **Status:** Shipped
- **Target Quarter:** Q1FY26
- **Linked Doc:** `confluence://acme-ecomm/care/w-plus-routing-post-launch`
- **Notes:** Shipped last week. Initial metrics look stable, though renee.kowalski’s membership team asked if we can pull a breakdown of CSAT scores specifically for annual plan holders who hit the queue during peak evening hours. Will add to next week's Care ops sync agenda.

---

## Workspace: MARKETPLACE (Sub-verticals: Collectibles, Resold, Style)
*Administered by nadia.esposito / Leadership sponsor: victor.okonkwo (SVP Marketplace)*

### 4. Card ID: MKT-401
- **Title:** Style category-page dynamic filtering for sustainable material tags
- **Owner:** ines.delgado (Sr PM Marketplace Style)
- **Status:** In Progress
- **Target Quarter:** Q1FY26
- **Linked Doc:** `confluence://acme-ecomm/marketplace/style-sustainability-filters-prd`
- **Notes:** Ines is coordinating with ronnie.aldridge (external partner operating Northfield Apparel Co., sel_500034) to ensure supplier data feeds include the required ISO textile certifications. Quick coffee chat with maya.lindqvist (US_CONV) on Tuesday to make sure our filter taxonomy doesn't conflict with main site nav updates.

### 5. Card ID: MKT-412
- **Title:** Resold category bulk-listing CSV uploader for mid-tier sellers
- **Owner:** noah.kessler (Sr PM Marketplace Resold)
- **Status:** Backlog
- **Target Quarter:** Q2FY26
- **Linked Doc:** `confluence://acme-ecomm/marketplace/resold-bulk-csv-spec`
- **Notes:** Noah mentioned in standup that sellers like sel_500204 (ReWear Collective) have been asking for this repeatedly in feedback pulses. Currently blocked on shared platform API rate limits. Keeping in backlog for Q2.

### 6. Card ID: MKT-429
- **Title:** Collectibles high-value item audit workflow enhancement
- **Owner:** sanjay.bhatt (Sr PM Marketplace Collectibles)
- **Status:** In Progress
- **Target Quarter:** Q1FY26
- **Linked Doc:** `confluence://acme-ecomm/marketplace/collectibles-audit-workflow`
- **Notes:** Following up on trust and safety requirements. Coordinating closely with lucia.ferreira (Trust & Safety Lead) to ensure high-value trading card listings have adequate provenance tracking before going live.

### 7. Card ID: MKT-455
- **Title:** Explore a customer-facing trust signal for Collectibles
- **Owner:** *(Unassigned)*
- **Status:** Backlog
- **Target Quarter:** Q3FY26
- **Linked Doc:** `confluence://acme-ecomm/marketplace/collectibles-trust-signal-brainstorm`
- **Notes:** Vague exploratory placeholder card created during the quarterly planning overflow session. Needs scoping before assigning an owner. Just floating ideas around what a buyer-facing indicator might look like if we ever implemented one for authenticated rare items. Completely informal at this stage, no engineering commitments or dependencies.

### 8. Card ID: MKT-441
- **Title:** Seller onboarding profile completion checklist refactor
- **Owner:** victor.okonkwo (SVP Marketplace acting temporarily on seller UX pending new hire)
- **Status:** Shipped
- **Target Quarter:** Q1FY26
- **Linked Doc:** `confluence://acme-ecomm/marketplace/seller-onboarding-ux-v2`
- **Notes:** Shipped right before the April MBR prep. Early telemetry shows completion rates for mid-tier sellers (such as sel_500200 Silverline Card Co. and sel_500203 Marrow Lane Vintage) improving nicely.

---
*End of Aitable export. For Jira tickets created after 2026-01-15, please query the Jira API directly.*
