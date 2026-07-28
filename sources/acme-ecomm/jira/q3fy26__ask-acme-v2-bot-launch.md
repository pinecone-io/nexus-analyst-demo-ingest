---
title: "Jira release ticket: 'Ask Acme v2' customer-care deflection bot"
source_url: "internal://acme-ecomm/jira/q3fy26__ask-acme-v2-bot-launch"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2025-10-15T12:00:00+00:00'
adapter: jira_ticket
---

# JIRA: CARE-4892
**Project:** Care Platform & Automation (CARE)  
**Issue Type:** Release / Epic  
**Status:** Done (Resolved 2025-09-15)  
**Priority:** P1 - High  
**Assignee:** `dominic.paquet` (Care Ops Lead, assoc_100310)  
**Reporter:** `aisha.rahman` (Director PM Care, assoc_100130)  
**Components:** `bot-framework`, `deflection-engine`, `nlp-intent-router`, `wplus-member-routing`  
**Labels:** `q3-release`, `bot-v2`, `deflection`, `care-automation`, `post-collectibles-rush`  

---

## Description

This is the primary tracking ticket for the production rollout of **'Ask Acme v2'**, our next-generation customer support chatbot. Following the massive traffic surge and subsequent support queue saturation we experienced in Collectibles last month (reference the viral card auction incident managed by `lucia.ferreira` on 2025-08-04 and the subsequent rollout of the "Acme Verified" authentication program on 2025-09-08), our Tier-1 contact volume has been under extreme operational strain. 

Ask Acme v2 replaces the legacy rule-based decision tree with a hybrid LLM-backed intent router capable of handling complex multi-turn order tracking, returns initiation, and automated refund status checks without requiring human agent intervention.

### Rollout Scope & Phasing
- **Target Launch Date:** 2025-09-15 (Shipped on schedule at 04:00 UTC).
- **Initial Traffic Allocation:** 50% of inbound chat sessions routed to v2 bot engine upon release; scaled to 100% on 2025-09-18 following a clean 48-hour error-rate audit.
- **Surface Coverage:** Web storefront (`acme.com`), mobile iOS/Android apps, and dedicated Acme+ member support portal (`care.acme.com/plus`).
- **Exclusions:** Account security/takeover flags, legal escalations, and B2B/Acme Business bulk orders are hard-routed directly to human tier-2 specialists.

### Core Metrics to Move
The primary success metric for Ask Acme v2 is the **Care Bot Deflection Rate** (`deflection_rate` in `care_deflection_daily`), which sat at roughly 39.5% during Q2FY26 and is targeted to cross 45.0% by the end of Q4FY26 as part of our broader FY27 Care efficiency roadmap. 

Secondary guardrail metrics monitored via Medallia (`fact_voc_responses`) and our internal data marts:
- **Deflected CSAT (`avg_csat_deflected`):** Target to hold at or above 3.80 (historical v1 baseline was ~3.85; we are watching closely to ensure automated deflection doesn't tank customer satisfaction scores).
- **Average Handle Time (AHT):** Expected to drop across residual agent-assisted contacts as the bot successfully filters out simple "Where is my order?" (WISMO) and basic return-label inquiries.

---

## Attachments & Artifacts
- `confluence_care_ask_acme_v2_prd_v4.pdf` (linked from legacy roadmap, cross-referenced with the ongoing Aitable-to-Jira migration being overseen by `nadia.esposito`)
- `looker_compass_care_deflection_hourly_snapshot_0915.png`
- `nlp_intent_routing_matrix_v2.json`

---

## Comments

**`dominic.paquet` [2025-09-12 16:45 UTC]**
Quick update ahead of Monday's go-live. Staging load tests with `connor.blake` from Data Engineering looked solid—we simulated 3x peak Black Friday concurrency through the intent router without hitting rate limits on the downstream order-status APIs. `giulia.romano` has verified that the telemetry pipeline is correctly populating `fact_care_contacts` with `deflected = TRUE` and the appropriate `deflection_type` codes. Let's make sure we're keeping an eye on Medallia post-launch. 

**`julian.moss` [2025-09-14 11:20 UTC]**
Reminder for the platform team: do not touch the OAuth token refresh service during the deployment window tomorrow morning. We don't want session drops for active Acme+ members who are currently browsing the site or managing subscriptions via `simone.laurent`'s membership portal.

**`aisha.rahman` [2025-09-15 09:30 UTC]**
Traffic is ramping up nicely. Initial 50% split is live. Error rates on the LLM intent fallback are sitting at 0.4%, well below our 1.0% threshold. Good work getting this across the finish line, team. Let's review the initial deflection numbers in tomorrow's Care standup.

**`hannah.brennan` [2025-09-15 14:10 UTC]**
Checked the live Compass dashboard. Deflection for the morning block is already ticking up about 3.5pp compared to last week's average. Let's keep a very close eye on `avg_csat_deflected` over the next 48 hours to ensure customers aren't just abandoning the chat in frustration. Great execution, Dominic.

**`wei.hartono` [2025-09-16 08:15 UTC]**
Just a note for downstream analysts querying `care_deflection_daily`: ensure you're filtering by the new `sub_program` taxonomy values (`automate`, `avoid`, `optimize`, `platform`, `member_care`). The legacy v1 bot interaction logs have been archived into cold storage, but historical aggregates remain intact in the BigQuery flat dataset (`nexus-analyst-demo.acme_ecomm.care_deflection_daily`). Also, please remember that `dim_care_contacts` is a representative sample (~50k rows), so don't run company-wide totals off raw counts there.

**`felix.arroyo` [2025-09-16 11:50 UTC]**
Fantastic to see this rolling out smoothly, especially right on the heels of the Collectibles authentication firefighting we had to do with `lucia.ferreira` last month. If this hits our deflection targets for Q3, it'll free up considerable headroom for the care team ahead of the Q4 peak holiday rush.

**`dominic.paquet` [2025-09-15 18:00 UTC]**
*Status change:* Moving ticket status to **Done**. All post-deployment smoke tests passed successfully. Escalating monitoring to on-call rotation.

---
