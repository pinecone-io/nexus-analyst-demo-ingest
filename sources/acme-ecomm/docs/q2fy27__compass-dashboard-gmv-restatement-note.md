---
title: "Data-quality note: Compass dashboard's stale Q4FY26 Marketplace GMV figure"
source_url: "internal://acme-ecomm/docs/q2fy27__compass-dashboard-gmv-restatement-note"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: confluence_page
---

# Data-Quality Advisory: Compass Dashboard Stale Cache — Q4FY26 Marketplace GMV ($952.4M vs $975.0M)

**Author:** `connor.blake` (Data Engineer, Pipeline/Freshness, Data & Analytics)  
**Target Audience:** All Compass BI tool users, Finance analysts (`amara.shah` et al.), Marketplace vertical leads (`victor.okonkwo`, `sanjay.bhatt`, `ines.delgado`, `noah.kessler`, `camille.duarte`)  
**Status:** Active Advisory / Known Data Artifact  
**Related Systems:** Compass BI (cached PDT layer), BigQuery (`nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`)  

---

### Background & Context

As we push through the final weeks of Q2FY27 (with total digital and marketplace GMV pacing nicely at a $7.62B run-rate against our $7.53B FY27 target, sitting at 101.2% of goal), cross-vertical reviews and quarterly comparisons frequently pull historical figures from prior fiscal years. 

During last week's preparatory sync for the upcoming MBR session—building on top of the broader Q2FY27 MBR review cadence managed by `carlos.figueroa` and `amara.shah`—a recurring discrepancy was flagged regarding the final, canonical Marketplace GMV for Q4FY26 (the peak holiday quarter spanning November 1, 2005 through January 31, 2006). 

Specifically, users poking around historical performance dashboards in our internal BI platform, **Compass**, may still encounter a cached Persistent Derived Table (PDT) view showing Q4FY26 Marketplace GMV as the flash-reported **$952.4M** figure that was originally published right at quarter-close back in late January/early February 2006. 

This note exists to document the official reconciliation, point everyone to the canonical table, and provide simple instructions for forcing a manual refresh in Compass so that this $952.4M vs. $975.0M discrepancy becomes self-correcting rather than turning into a silent trap during cross-quarter variance analysis.

---

### The Numbers: Flash vs. Canonical Restatement

To be completely explicit for anyone writing postmortems, financial models, or quarterly trend decks:

1. **The Flash Figure ($952.4M):** This was the preliminary flash-reported Marketplace GMV aggregated at the close of Q4FY26 (peak holiday rush, Black Friday through New Year's, navigating the JOL1 winter storm disruptions and peak volume strains). It was captured in early Compass PDT builds before the post-quarter finance close.
2. **The Canonical Reconciled Figure ($975.0M):** Following the formal monthly/quarterly financial close and the February 2006 returns-timing reclassification (which accounted for post-holiday settlement adjustments, deferred 3P merchant payouts, and holiday return timing lags), the mart-reconciled figure was finalized at **$975.0M**. 

For reference against the broader Marketplace sub-vertical breakdown from Q4FY26:
* **Style:** $715.0M
* **Resold:** $142.0M
* **Collectibles:** $118.0M (which had just finished absorbing the viral vintage-card auction surge and the initial rollout of the "Acme Verified" authentication program backed by GradeSure)
* **Total Canonical Q4FY26 Marketplace GMV:** **$975.0M** (derived from the full-population aggregate mart `marketplace_gmv_summary`, adhering strictly to convention 5 regarding sample-vs-population boundaries).

If your Compass report shows $952.4M for Q4FY26 Marketplace GMV, **you are looking at stale PDT cache**, not a new data drop or a secondary adjustment.

---

### Why Does This Happen?

Compass relies on scheduled PDT (Persistent Derived Table) materialization jobs to keep dashboard rendering fast across our 16 internal verticals. Because Q4FY26 is a closed historical quarter, its underlying source partitions in BigQuery (`nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary`) are static. However, Compass instances belonging to users who have not queried that specific report tile since February 2006 are serving results from local cache models built before the restatement pipeline run completed on `2006-02-10`.

This is distinct from other pipeline hiccups we've managed—such as the `marketplace_gmv_summary` 14-hour staleness incident caused by an upstream retry-logic bug in our Airflow orchestration back in June 2025 (`2025-06-20`), or the `sessions_definition_version` 1→2 cutover on `2006-03-02` managed by `wei.hartono` which affected traffic and conversion metrics site-wide. In this case, the underlying BigQuery mart is entirely correct and up-to-date at $975.0M; only the downstream BI visualization layer's cache is lagging for inactive user profiles.

---

### How to Force a Compass Refresh

If you are building decks or pulling historical extracts and want to clear out the stale $952.4M figure from your personal or shared Compass views, please follow these steps:

1. Navigate to the affected dashboard tile in Compass (e.g., *Marketplace Executive Summary — Historical Quarters*).
2. Click the gear/settings icon in the top right corner of the reporting tile.
3. Select **"Force Derived Table Rebuild"** (or use keyboard shortcut `Ctrl/Cmd + Shift + R` while focused on the tile).
4. Verify that the Q4FY26 row updates from `952,400,000` to `975,000,000`.
5. If the tile refuses to drop the cache, verify that your query is referencing the flat path `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary` directly rather than an obsolete nested view or an ad-hoc slice of `fact_orders` (remember convention 5: `fact_orders` is a ~400k representative sample and must never be used for total company or vertical GMV rollups).

---

### Miscellaneous Team Notes & Chatter

* **Looker Migration Retro:** While we continue standardizing our reporting tools, remember that our internal Looker-to-Compass-analog dashboard migration (overseen informally by the Data & Analytics team) is still a background project. Don't mix up old Looker direct links with the new Compass Uniform Resource Identifiers.
* **Office Logistics / Standup:** Reminder that tomorrow's 9:30 AM Data Engineering standup has been moved to Conference Room B (Floor 3) because facilities is doing HVAC maintenance in the West Wing. Lunch order for the team is coming from Coastal Trading Post's neighborhood joint (though not sel_500211 specifically—just regular catering).
* **Cross-Vertical VOC Check:** Giulia Romano (`giulia.romano`) noted in the Care/VOC channel that Medallia verbatims regarding `listing-accuracy-gap` remain steady across Style (14%), Resold (12%), Collectibles (9%), and B2B (22%). Camille Duarte (`camille.duarte`) and Victor Okonkwo (`victor.okonkwo`) are keeping an eye on how these tie into our seller optimization surfaces, but it has no direct bearing on the Q4FY26 GMV restatement note. Just good context to keep in mind if you're pulling multi-vertical health checks.

Let's keep our dashboards clean! Ping me in `#data-pipeline-alerts` if you run into any stubborn persistence issues.

---
