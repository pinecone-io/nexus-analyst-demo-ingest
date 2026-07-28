---
title: "Confluence status page: Aitable→Jira roadmap migration — still not complete"
source_url: "internal://acme-ecomm/confluence/q2fy27__aitable-jira-migration-status-update"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: confluence_page
---

# Confluence Status Page: Roadmap Tracker Migration (Aitable → Jira)

**Owner:** `nadia.esposito` (Head of Product Operations)  
**Last Updated:** 2026-07-20  
**Status:** **INCOMPLETE — OVERDUE / BLOCKED (6+ MONTHS ELAPSED)**  
**Target Completion:** ~~2026-03-31~~ ~~2026-05-30~~ INDEFINITE DEFERRED

---

## Executive Summary / Status As of Today (2026-07-20)

When we kicked off the Aitable-to-Jira roadmap consolidation project back on **2026-01-15** (following the leadership sync and data architecture cleanups around our BigQuery flat dataset standards), the objective was simple: unify our fragmented product planning artifacts, retire our legacy Aitable workspaces entirely, and house all active and upcoming Q1/Q2/Q3 initiatives in Jira epics tied directly to our `nexus-analyst-demo.acme_ecomm` vertical taxonomy (`dim_vertical`).

More than six months later, **migration is NOT complete**. 

Let's state this plainly without softening it into "almost done" or "90% there" for executive consumption: **Items opened before 2026-01-15 largely still live in Aitable; items opened on or after live in Jira. Confluence PRDs and spec documents span both eras.** If you are trying to audit cross-vertical backlogs — say, checking whether a given Medallia theme like `listing-accuracy-gap` (sitting at 14% for Style, 12% for Resold, 9% for Collectibles, and 22% for B2B) maps to an owning initiative anywhere across Style, Resold, Collectibles, or B2B — querying only one of the two systems will silently hand you a partial answer; you have to check both in full before concluding anything is or isn't covered. 

This page serves as the living status tracker, audit log, and punch-list for what remains stranded in the legacy system and why this cleanup has dragged across Q1 and Q2 of FY27.

---

## Current State Breakdown: The Two-Era Roadmap Problem

To anyone onboarding into the Product, Engineering, or Data teams (or referencing historical PRDs), our documentation is visibly bifurcated by the 2026-01-15 demarcation line:

1. **The Pre-2026-01-15 Era (Aitable-Bound):**  
   Legacy ideation cards, early exploratory drafts (such as the abandoned *Style Conversion Recovery Plan* drafted circa Q1FY27 proposing T&S headcount shifts from Collectibles to Style before `marketplace_cannibalization` metrics proved it was a Resold wallet-share shift rather than a demand loss), and pre-peak optimization notes live exclusively in Aitable bases. These cards do not sync with Jira epics, lack proper association to our flat BQ `dim_experiment` IDs, and frequently point to deprecated metric definitions (such as pre-v2 session counts before wei.hartono’s `sessions_definition_version` 1→2 cutover on 2026-03-02).
2. **The Post-2026-01-15 Era (Jira-Bound):**  
   Initiatives kicked off since the migration launch—including owen.faust’s *Checkout Simplify* (`exp_2214`), leo.brandt’s short-lived *Wider Promise Window* (`exp_1187`), aisha.rahman’s *Bot Handoff Threshold* (`exp_2489`), and maya.lindqvist’s ongoing *Item Page Iteration Program*—live cleanly in Jira under standardized project keys. 
3. **The Confluence Bridge Layer:**  
   Our PRD library in Confluence links haphazardly to both. A spec written in February 2026 for maya.lindqvist’s NAV refresh holdback (`exp_2215`) references Jira tickets, while older fulfillment speed notes referencing gabriel.stroud’s FON2/JOL1 DC automation phases link back to Aitable review decks.

---

## Punch-List: What's Left in Aitable and Why It Has Dragged

Product Operations has completed an inventory of unmigrated epics and cards currently marooned in Aitable workspaces. The remaining items fall into three buckets, accounting for why this migration has repeatedly slipped past its target milestones:

* **Bucket A: Abandoned / Exploratory Ideation Cards (Approx. 42 cards)**  
  * *Description:* Speculative brainstorms from FY26 peak retros (e.g., early holiday return-processing congestion notes from the Ontario, CA returns center when it ran 22% understaffed during the December rush). 
  * *Why it dragged:* No active product owner wants to spend sprint capacity manually re-keying dead-end or superseded brainstorms into Jira just for the sake of an audit.
* **Bucket B: Orphaned Marketplace & B2B Sub-Vertical Backlog Items (Approx. 18 cards)**  
  * *Description:* Granular feature requests in Style (`ines.delgado`), Resold (`noah.kessler`), Collectibles (`sanjay.bhatt`), and B2B (`malik.hendon`) that pre-date camille.duarte joining as Sr PM Marketplace Seller Experience on 2026-04-08. These include various bulk-upload tool concepts and category-taxonomy expansions.
  * *Why it dragged:* Cards without clear, current product owners fell through the cracks during the Q4 peak crunch and the subsequent Q1/Q2 strategy realignments. When camille.duarte took over seller listings and optimization surfaces, she inherited an active Jira queue but left the legacy Aitable seller-pulse feedback items untouched.
* **Bucket C: Historical Experiment Spec Sheets (Approx. 25 cards)**  
  * *Description:* Pre-2026-01-15 experiment design documents (such as early drafts of sanjay.bhatt’s *Verified Badge Prominence* `exp_2401` iterations).
  * *Why it dragged:* Competing priorities. With conversion rate headwinds in US_CONV (pacing at 3.22% QTD vs. 3.35% target) and teams heavily focused on running offsetting experiments like *Search Relevance Re-ranking* (`exp_2601`, +1.6% lift) and *Item Page Media Carousel Autoplay* (`exp_2618`, -1.5% drag) through June and July, migrating historical experiment scratchpads has zero impact on top-line GMV run-rate ($7.62B actual vs. $7.53B target).

---

## Slack / Standup Aside (Captured via Product Ops Log)

> **[#prod-ops-roadmap] 2026-07-18 at 14:15 ET**
> 
> **nadia.esposito:** *@here Quick reminder that if anyone is linking to roadmap items in the upcoming Q2 MBR prep deck for carlos.figueroa / amara.shah, double-check whether the epic URL starts with `aitable.acme.internal` or `jira.acme.internal`. We still don't have a clean automated bridge for the pre-January stuff.*
> 
> **derek.holloway:** *Honestly, at this point in Q2, are we even bothering to migrate the Q3FY26 stuff? Most of those specs are stale anyway now that Reelstream replaced Vidora for the streaming perk back on June 1st.*
> 
> **nadija.esposito:** *Technically we’re supposed to for audit compliance, but realistically? It’s staying in Aitable until Q3 planning at best. Just make sure your active Jira epics are tagged with the right vertical codes (`dim_vertical`) so amara.shah’s SQL queries don’t break.*

---

## Next Steps & Recommendations

1. **Formalize the "Two Eras" Acknowledgement:** Stop pretending a unified backlog exists. Confluence PRD templates will now explicitly include an `Era:` metadata tag (`Aitable-Legacy` vs. `Jira-Active`).
2. **Triage Orphaned Marketplace Cards:** camille.duarte and victor.okonkwo to review Bucket B items during the next Marketplace sync to determine if any unaddressed seller-experience friction points (like `listing-setup-complexity` or `no-performance-visibility`) deserve migration into active Jira epics, or if they should be archived outright.
3. **Resource Constraint Sign-Off:** Given that total digital + marketplace GMV is pacing at $7.62B (101.2% of goal) and Marketplace GMV is overperforming at $3.89B run-rate (117.1%), executive leadership has confirmed that completing administrative roadmap cleanup remains a P3 priority below growth and conversion initiatives.

---
