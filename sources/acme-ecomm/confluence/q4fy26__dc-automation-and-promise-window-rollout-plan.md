---
title: "Confluence rollout plan: DC sortation automation + a concurrent delivery-promise experiment"
source_url: "internal://acme-ecomm/confluence/q4fy26__dc-automation-and-promise-window-rollout-plan"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-01-25T12:00:00+00:00'
adapter: confluence_page
---

# Rollout Plan & Operational Execution Guide: FON2 & JOL1 Joint Infrastructure & Service Updates (Q4FY26 Peak Transition Window)

**Author:** Gabriel Stroud (`assoc_100330`, Fulfillment Ops Lead) & Leo Brandt (`assoc_100141`, Sr PM Delivery Promise)
**Reviewers:** Ben Tanaka (`assoc_100050`), Tara Oduya (`assoc_100140`), Connor Blake (`assoc_100212`)
**Status:** In Progress / Active Execution
**Effective Date:** 2026-01-12
**Target Facilities:** FON2 (Fontana, CA) & JOL1 (Joliet, IL)

---

## 1. Executive Summary & Context

As we navigate the tail end of Q4FY26 and prepare our distribution network for the upcoming fiscal year, this Confluence page serves as the unified master rollout plan for two major, parallel operational tracks landing concurrently at our **FON2 (Fontana)** and **JOL1 (Joliet)** distribution centers starting the week of **2026-01-12**. 

To be explicitly clear for cross-functional readers, this document covers **two entirely distinct initiatives** managed by separate teams, which happen to share a physical deployment footprint and launch calendar week:
1. **DC Sortation Hardware & Software Automation (Phase 1)**: Led by **gabriel.stroud** (Fulfillment Ops). A capital infrastructure project aimed at upgrading high-speed cross-belt routing tables and automated container consolidation scanners. Phased deployment running from **2026-01-12 through 2026-02-15**.
2. **The 'Wider Promise Window' Experiment (`exp_1187`)**: Led by **leo.brandt** (Delivery Promise / Speed). A product/algorithm experiment widening the customer-facing delivery estimation windows shown on checkout and item pages to measure impact on carrier selection load balancing and on-time-to-promise metrics. Launching **2026-01-12**.

While both initiatives impact outbound parcel flows out of FON2 and JOL1, their operational objectives, telemetry tracking, and immediate stakeholders are completely separate. Teams should take care not to cross-contaminate metric readouts between infrastructure throughput and customer-facing promise conversion.

---

## 2. Initiative A: DC Sortation Automation (Phase 1)
***Owner:** Gabriel Stroud (`assoc_100330`) / Fulfillment Engineering*
***Vertical:** Speed / Efficiency (`SPEED`)*

### Background & Motivation
Following the peak-volume strains experienced across our network in December—including the 36-hour winter-storm disruption at JOL1 on **2025-12-08**—and the ongoing review of our cost-per-order trajectory ($8.60 during Q4 peak vs. $7.70 baseline), network engineering is deploying Phase 1 of the sortation automation upgrade. This follows earlier base telemetry baselining completed back in February 2025 (`assoc_100212`).

 FON2 and JOL1 handle roughly 42% of our total ship-to-home volume. Manual staging bottlenecks during peak sorting have historically driven up our sort-time variance and contributed to downstream carrier handoff friction.

### Scope & Deployment Schedule
- **Window:** 2026-01-12 through 2026-02-15.
- **Nodes Affected:** `node_id` `FON2` (Fontana, CA DC) and `node_id` `JOL1` (Joliet, IL DC).
- **Hardware/Software Upgrades:**
  - Installation of high-speed optical barcode tunnel arrays on primary outbound induct lines.
  - Firmware update v4.12 for cross-belt diversion controllers.
  - Integration with local warehouse execution systems (WES) to feed real-time bin-utilization metrics into our BigQuery operational data store (`nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`).

```
[Pallet Intake] ---> [Optical Tunnel Array (NEW)] ---> [Cross-Belt Sorter v4.12] ---> [Carrier Hand-off]
```

### Risks, Mitigations & Notes from the Floor
- *Staffing & Training:* Shift supervisors at FON2 report minor scheduling friction due to local shift rotations, but training modules developed with operations leads are proceeding. Note that this automation is entirely separate from the returns-center staffing remediation happening concurrently at the Ontario, CA returns facility (`node_id` returns center) managed by hannah.brennan to address the refund-cycle backlog. Do not mix up the DC sortation upgrades with returns processing workflows.
- *Expected ROI:* Long-term cost-per-order reduction ($7.30 run-rate target for Q2FY27) and improved sort accuracy.

---

## 3. Initiative B: 'Wider Promise Window' Experiment (`exp_1187`)
***Owner:** Leo Brandt (`assoc_100141`) / Delivery Promise*
***Vertical:** Speed / Promise (`SPEED`)*

### Hypothesis & Design
***Experiment ID:** `exp_1187`*
***Primary Metric:** Blended On-Time-to-Promise (OTP) & Checkout Conversion Rate*
***Target Scope:** US Market (`US_CONV` / `SPEED`), 100% traffic allocation split evenly across Control (standard 2-day/3-day strict promise logic) and Variant (widen displayed delivery window estimate by +1 to +2 business days during high-load intervals).*

As simulated during our preliminary promise-window syncs back in October 2025 (`assoc_100141` / leo.brandt), showing tighter delivery promises during high-demand surges often forces premium carrier selection or creates carrier-sla vulnerability when DC sort lanes experience micro-congestion. 

By widening the customer-facing delivery promise window starting **2026-01-12**, we aim to absorb carrier variance, protect our on-time delivery commitments, and evaluate whether customer conversion is unduly penalized by a less aggressive arrival estimate.

### Monitoring & Telemetry
- Exposing records will be logged directly to `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures`.
- Daily aggregation will cross-reference `fact_promise_vs_actual` where `node_id IN ('FON2', 'JOL1')` to check if carrier performance improves when promise buffers are expanded.
- *Note:* tara.oduya and the Pickup Perks team are monitoring concurrent BOPIS campaigns, but `exp_1187` is strictly targeted at ship-to-home promise strings.

---

## 4. Concurrent Operational Footprint (FON2 & JOL1)

Because both Gabriel's sortation automation and Leo's promise-window experiment are executing across FON2 and JOL1 during the exact same Jan 12 operational week, site leads are instructed to log any local anomalies in the warehouse shift handover notes. 

| Facility ID | Node Name | Initiative A (Sortation Automation) | Initiative B (Promise Experiment `exp_1187`) | Local Ops Contact |
|---|---|---|---|---|
| `FON2` | Fontana DC | Phase 1 Hardware Install (Optical Tunnels) | Active US Traffic Split (Variant Active) | gabriel.stroud / local shift lead |
| `JOL1` | Joliet DC | Firmware v4.12 & Cross-Belt Calibration | Active US Traffic Split (Variant Active) | gabriel.stroud / local shift lead |

*Side Channel Chatter (Slack excerpt - `#fulfillment-ops-chat`):*
> **gabriel.stroud**: *09:14 PST* — Optical tunnel install at FON2 is on schedule for Monday morning. Electrical team is cleared. Just hope we don't hit any repeat of the December winter storm issues we saw at JOL1.
> **leo.brandt**: *09:22 PST* — Good luck with the hardware. On our side, `exp_1187` traffic routing is fully hooked up in the staging env. Let's make sure our BigQuery pipeline jobs don't trip over the schema changes on `fact_promise_vs_actual`.
> **connor.blake**: *09:30 PST* — Pipelines are green. Just remember the dataset path is flat (`nexus-analyst-demo.acme_ecomm.fact_promise_vs_actual`), no nested sub-datasets. Don't repeat last month's path typo.

---

## 5. Next Steps & Action Items

1. **Infrastructure Sign-off:** Gabriel Stroud to confirm FON2 and JOL1 mechanical cutover completion by 2026-01-15.
2. **Experiment Health Check:** Leo Brandt to review initial assignment distribution for `exp_1187` in `fact_experiment_exposures` after 48 hours of live traffic.
3. **Data Quality Audit:** Wei Hartono (`assoc_100210`) and Connor Blake to monitor pipeline ingestion for both sort-throughput logs and experiment telemetry to ensure no data loss occurs during the peak transition.

---
*Document auto-archived by Confluence sync service. For questions regarding physical DC operations, ping `#dc-operations`. For promise modeling queries, ping `#speed-analytics`.*
