---
title: "Postmortem: winter storm disrupts JOL1 (Joliet) distribution center for 36 hours"
source_url: "internal://acme-ecomm/postmortems/q4fy26__jol1-winter-storm-dc-disruption"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-01-25T12:00:00+00:00'
adapter: postmortem
---

# Incident Postmortem: JOL1 Winter Storm Disruption (December 2025)

**Incident ID:** `inc_jol1_20251208`  
**Date of Incident:** 2025-12-08 through 2025-12-10  
**Author:** gabriel.stroud (Fulfillment Ops Lead)  
**Reviewers:** ben.tanaka (SVP Supply Chain & Fulfillment), tara.oduya (Director PM Speed & Fulfillment), leo.brandt (Sr PM Delivery Promise), amara.shah (Data Analyst, Finance/MBR)  
**Status:** Closed / Action Items In Progress  
**Vertical:** SPEED (`SPEED`)  
**Related Systems / Nodes:** JOL1 (`node_id='JOL1'`, Joliet, IL Fulfillment Center / Distribution Center), `fact_promise_vs_actual`, `fulfillment_speed_daily`  

---

## 1. Executive Summary

Beginning on the morning of **2025-12-08**, a severe winter storm system moved across the upper Midwest, directly impacting the Joliet, Illinois distribution center (**JOL1**). The facility experienced heavy snow accumulation, sub-zero wind chills, and regional whiteout conditions that severely impaired local transport networks, restricted inbound carrier linehauls, and forced a temporary suspension of outbound dock operations for a total of **36 hours**. 

Crucially, this disruption landed squarely during the post-Cyber-Monday peak volume window—weeks after the surge of Cyber Monday week (which kicked off on **2025-12-01** and concurrently unmasked the unrelated Ontario returns center processing backlog tracked by hannah.brennan). While meteorological in origin and strictly bounded to 36 hours, the JOL1 stoppage introduced significant downstream friction to ship-to-home orders originating from or passing through the Midwest hub. 

When combined with ordinary peak-volume strain across the broader fulfillment network, this incident contributed to a temporary dip in our ship-to-home on-time-to-promise (OTP) performance. Pacing calculations for the quarter indicate Q4FY26 ship-to-home OTP is tracking toward roughly the **mid-to-high-80s%**, down from baseline pre-peak expectations. We emphasize that the JOL1 storm is **one contributor** among several—including baseline peak-volume saturation and general carrier network degradation during December—and must not be framed as the sole root cause of the quarterly OTP pacing. 

Recovery was achieved via aggressive rerouting of regional volume to neighboring nodes (such as FON2 in Fontana and various regional sortation centers), alongside priority catch-up shifts once local transit authorities cleared the I-80/I-55 corridors around Joliet.

---

## 2. Timeline of Events (All Times US Central / CST)

*   **2025-12-01:** Cyber Monday week operational surge gets underway across the network. Fulfillment nodes operate at maximum throughput capacity. (Concurrently, Care and POR begin noting early signals of customer dissatisfaction around processing delays).
*   **2025-12-07, 18:00 CST:** National Weather Service issues a Winter Storm Warning for Will County, Illinois, predicting 8–12 inches of snow and sustained winds exceeding 40 mph, targeting the JOL1 facility footprint.
*   **2025-12-08, 04:00 CST:** First heavy bands of snow hit JOL1. Shift change for the morning crew experiences massive commuter delays; parking lots and yard access roads become impassable for standard light vehicles.
*   **2025-12-08, 06:30 CST:** **Outbound operations suspended.** Inbound carrier linehauls (UPS, FedEx, and third-party dedicated fleets) halt transit into the Joliet yard due to state police closures on local highways. *Official incident start.*
*   **2025-12-08, 14:00 CST:** Gabriel Stroud convenes emergency network routing sync with ben.tanaka and regional DC leads. Decision made to divert prospective inbound vendor loads destined for JOL1 toward secondary sortation nodes and regional cross-docks.
*   **2025-12-09, 12:00 CST:** Snowfall tapers off, but sub-zero temperatures cause severe icing on conveyor intake hatches and loading dock seals. Facility maintenance crews, working in rotation with heavy snow-clearing contractors, begin thermal thawing of dock levelers.
*   **2025-12-09, 18:30 CST:** **Operations resume partially.** Limited inbound receiving reopens as highway restrictions lift for commercial freight. Outbound parcel staging begins clearing the backlog accumulated over the prior 36 hours. *Official incident resolution / 36-hour window closes.*
*   **2025-12-10, 08:00 CST:** JOL1 returns to full shift staffing. Overtime allocation approved to process residual parcel queues. Promise dates for affected orders adjusted automatically via dynamic promise systems, though customer-facing delivery dates for orders already in flight absorbed a 1-to-3 day slip.
*   **2026-01-12:** Subsequent infrastructure investments begin, including the launch of DC sortation automation Phase 1 at FON2 and JOL1 (supervised by gabriel.stroud), designed in part to improve sort-throughput resilience.

---

## 3. Impact Assessment

### Operational Impact
*   **Duration of Complete Stoppage:** 36 consecutive hours of zero outbound parcel dispatch from JOL1.
*   **Volume Backlog:** Approximately 215,000 ship-to-home parcels were delayed in staging lanes or held in pick-totes awaiting pack-out during the window.
*   **Network Spillover:** Neighboring fulfillment and sortation nodes experienced an immediate 15–20% surge in diverted volume, temporarily raising local queue times at regional hubs.

### Metric Impact
*   **Ship-to-Home On-Time-to-Promise (OTP):** JOL1's local ship-to-home OTP dropped to **74.2%** for the operational week encompassing the storm (compared to a pre-peak baseline hovering near ~90%). 
*   **Blended Quarterly Pacing:** At the broader network level, Q4FY26 ship-to-home OTP is pacing toward the **mid-to-high-80s%** for the full quarter. As noted by amara.shah and tara.oduya in recent fulfillment reviews, this dip is a compound effect resulting from:
    1. Extreme peak-volume congestion across all Tier-1 DCs throughout December.
    2. The JOL1 36-hour weather outage.
    3. Carrier-side driver shortages and regional transit delays independent of Acme's four walls.
*   **Cost per Order:** Overtime premiums paid to maintenance and snow-removal contractors, combined with expedited linehaul rerouting fees, added approximately $0.14 to the blended cost-per-order metric for the affected operational week, a minor blip that was subsequently offset by longer-term automation efficiency gains realized later in Q1FY27.

---

## 4. Root Cause Analysis (RCA)

1.  **Primary Driver (Environmental):** Unprecedented local meteorological conditions in the Joliet region, featuring high-accumulation snowfall coupled with high winds that created localized drifts blocking trailer access and employee transit. This was a purely external weather event, not a systemic architectural failure of the facility's core warehouse management systems (WMS).
2.  **Contributory Factor (Infrastructure & Clearing Speed):** While facility management acted quickly, reliance on local third-party snow-plowing contractors created a 4-hour queueing delay before heavy clearing equipment could clear the truck apron and employee access gates during the height of the storm.
3.  **Contributory Factor (Peak Sensitivity):** Because the incident occurred during peak holiday volume, JOL1 was operating at near 100% utilization of its staging lanes. Consequently, even a 36-hour pause left zero spatial buffer, turning what might have been a minor 12-hour recovery in slack periods into a multi-day parcel backlog clearing operation.

---

## 5. Corrective Actions and Action Items

To mitigate similar weather-related vulnerabilities ahead of future winter seasons and improve network redundancy during peak quarters, the fulfillment operations team has logged the following action items in our operational backlog:

| ID | Action Item | Owner | Target Completion | Status |
|---|---|---|---|---|
| **ACT-JOL-01** | Establish direct SLA-backed contracts with regional heavy-equipment snow-removal vendors for dedicated on-site positioning at JOL1 and FON2 during winter storm watches. | gabriel.stroud | 2026-09-01 | In Progress |
| **ACT-JOL-02** | Update dynamic promise calculation logic to enable automated, proactive customer notification and promise-window widening whenever a primary DC node falls under an active NWS Winter Storm Warning. | leo.brandt / tara.oduya | 2026-05-15 | Backlog |
| **ACT-JOL-03** | Implement automated staging-lane capacity throttling linked to regional weather feeds to prevent dock gridlock during inbound linehaul suspensions. | gabriel.stroud / wei.hartono | 2026-08-01 | Open |
| **ACT-JOL-04** | Review cold-weather facility hardening (including heated loading dock seals and pneumatic line heaters) as part of the broader DC infrastructure upgrade budget. | ben.tanaka | 2026-10-31 | Planned |

---
*End of Postmortem. For downstream financial reconciliation or fulfillment trend analysis, cross-reference `fact_promise_vs_actual` filtered by `node_id='JOL1'` and `date BETWEEN '2025-12-08' AND '2025-12-10'`.*
