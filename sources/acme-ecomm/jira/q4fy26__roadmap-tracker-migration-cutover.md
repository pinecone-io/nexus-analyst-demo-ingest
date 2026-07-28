---
title: "Jira ticket: roadmap-tracking migration cutover from Aitable to Jira"
source_url: "internal://acme-ecomm/jira/q4fy26__roadmap-tracker-migration-cutover"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-01-25T12:00:00+00:00'
adapter: jira_ticket
---

**Jira Issue:** PRODOPS-8104  
**Project:** Product Operations & Governance  
**Issue Type:** Epic / System Migration Notice  
**Status:** In Progress (Cutover Effective)  
**Priority:** High  
**Assignee:** nadia.esposito (`assoc_100070`)  
**Reporter:** nadia.esposito (`assoc_100070`)  
**Created:** 2026-01-10  
**Updated:** 2026-01-25  
**Labels:** `roadmap-migration`, `process-governance`, `aitable-retirement`, `product-ops`

---

### Description

Team,

As discussed in last week's portfolio sync and following up on our ongoing efforts to clean up our cross-functional planning toolchains, this ticket serves as the official operational notice for our roadmap-tracking migration cutover. 

Effective today, **January 15, 2026**, **Jira is our official system of record for all new roadmap items, epics, and engineering initiatives.** 

For the past several quarters, we’ve operated in a somewhat fragmented state where legacy ideation, early discovery scoping, and cross-vertical dependencies were split across Aitable cards and various ad-hoc Confluence PRDs, while execution tracking lived partially in Jira. As felix.arroyo noted during our FY26 retrospective prep, having our source of truth fractured across platforms makes cross-vertical dependency mapping (especially between US_CONV, Marketplace, and Speed initiatives like the recent `exp_1187` promise-window work) unnecessarily difficult to audit. 

Moving forward, any new feature proposal, experiment tracking stub, or vertical milestone must be initialized directly inside Jira under the appropriate vertical project space.

---

### Migration Scope & What This Means for PMs

To be completely transparent and manage expectations: **this cutover does NOT mean Aitable is instantly empty or that legacy records have vanished.** 

We are **not** doing a hard, overnight bulk-wipe or an automated script-dump of all historical Aitable cards into Jira. A significant portion of our historical roadmap context—stretching back through FY26—lives in legacy Aitable records. Those existing cards will be migrated **over time** on an as-needed basis by the Product Ops associates (`nadia.esposito`, with support from amara.shah and our data engineering cohorts) as those initiatives are actively refactored, re-scoped, or pulled into upcoming quarterly planning cycles. 

- **New Items (Post-2026-01-15):** Must be created in Jira. If it doesn't have a Jira key, it does not exist on the official roadmap.
- **Existing/In-Flight Items (Pre-2026-01-15):** Existing cards currently tracked in Aitable may remain there *for now* if they are currently mid-execution or in maintenance mode. However, if an in-flight initiative experiences a major scope change, pivots, or gets extended into Q1FY27 / Q2FY27, the PM responsible is required to spin up a corresponding Jira epic and link the legacy Aitable card as a reference.

As outlined in our governance hierarchy, our source of truth for planning is shifting decisively: Slack chatter and legacy Aitable cards are taking a back seat to committed Jira epics and Confluence execution specs. 

---

### Comments & Activity Stream

**nadia.esposito (`assoc_100070`)** — *2026-01-10 09:15 EST*  
@here Drafted the initial migration framework. CC'ing all vertical PMs (maya.lindqvist, owen.faust, sanjay.bhatt, ines.delgado, noah.kessler, tara.oduya, leo.brandt, simone.laurent, derek.holloway, malik.hendon) so everyone is aware of the shift before Monday's standup. Please make sure your engineering leads are pointing their board filters to the new Jira schema.

**carlos.figueroa (`assoc_100060`)** — *2026-01-10 11:42 EST*  
Thanks Nadia. This is long overdue. Just a reminder for the Data team: when writing queries or pulling audit logs for MBR decks, remember that older historical roadmap references prior to today will still point to the legacy Aitable system IDs unless migrated. Don't panic if an old ID doesn't resolve in Jira right away.

**maya.lindqvist (`assoc_100110`)** — *2026-01-12 14:03 EST*  
Does this apply to minor item-page iteration sub-tasks currently mapped under my Q1 roadmap, or just major epics? We are right in the middle of wrapping up the v1-v6 item page reflows.

**nadia.esposito (`assoc_100070`)** — *2026-01-12 15:20 EST*  
@maya.lindqvist Active sub-tasks can finish out their current lifecycle where they live, but any new work items spun up after the 15th must be in Jira. Let's not disrupt active code deployment streams mid-stream.

**felix.arroyo (`assoc_100010`)** — *2026-01-15 08:30 EST*  
Officially marking this cutover live as of today. Thanks to Nadia and the team for putting the guardrails together. Let's make sure we stick to it so we don't end up with split-brain planning going into Q1/Q2 FY27.

---
