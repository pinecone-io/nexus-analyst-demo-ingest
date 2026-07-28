---
title: "Expo experiment readout: 'Verified Badge Prominence' clean +6.8% lift, ships to 100%"
source_url: "internal://acme-ecomm/expo/q4fy26__exp-verified-badge-prominence-readout-and-ship"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-01-25T12:00:00+00:00'
adapter: expo_experiment
---

# Expo Experiment Readout & Launch Record

**System:** `expo` (Expo Experiment Platform)  
**Dataset Table:** `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts` / `dim_experiment`  
**Experiment ID:** `exp_2401`  
**Experiment Name:** Verified Badge Prominence  
**Vertical Code:** `MARKETPLACE` (Sub-vertical: `COLLECTIBLES`)  
**Owner:** sanjay.bhatt (Sr PM Marketplace Collectibles, assoc_100120)  
**Status:** Shipped to 100%  
**Analysis Basis:** Exposed Units (Per-Protocol)  

---

## 1. Executive Summary & Final Disposition

Following the kickoff of this experiment on 2025-10-01 (right on the heels of our initial verification workflows and the early setup guardrails established in the BigQuery audit logs back in February), `exp_2401` has officially concluded its evaluation window as of 2025-11-15. 

The variant featuring increased visual weight and prominent surface placement for the "Acme Verified" authentication badge on Collectibles listings yielded a clean, unconfounded **+6.8% conversion lift** (`is_significant = TRUE`, p < 0.01) among exposed units compared to the control group. 

Unlike several of our concurrent or later mobile and checkout tests—such as Owen's `exp_2214` checkout simplify test which got tangled up with the March Nav Refresh, or Leo's wider promise window test (`exp_1187`) which required heavy deconfounding against the FON2/JOL1 DC automation rollout—this particular Collectibles window experienced zero overlapping marketplace launches, marketing campaigns, or calendar anomalies in the category. The data is entirely clean. 

Consequently, per Sanjay's recommendation and sign-off, the variation was approved and shipped to **100% of Collectibles listings on 2025-11-20**.

---

## 2. Quantitative Readout (`fact_experiment_readouts`)

Query executed against `nexus-analyst-demo.acme_ecomm` via Compass / BigQuery flat dataset schema (`nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`):

```sql
SELECT 
    experiment_id,
    variant,
    as_of_date,
    metric_name,
    metric_value,
    sample_size_units,
    lift_vs_control_pct,
    is_significant,
    notes
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`
WHERE experiment_id = 'exp_2401'
  AND as_of_date = '2025-11-15';
```

### Key Metrics Table (Readout Date: 2025-11-15)

| Variant | Metric Name | Metric Value | Sample Size (Exposed Units) | Lift vs Control (%) | Is Significant | Notes |
|---|---|---|---|---|---|---|
| Control (Standard Badge) | conversion_rate | 2.14% | 142,500 | — | — | Baseline badge size / lower fold placement |
| Variant A (Prominent Badge) | conversion_rate | 2.29% | 143,100 | **+6.8%** | TRUE | Enhanced size, gold verification border, top-of-spec sheet |

*Note on exposure definition:* In alignment with our standard expo adapter configuration, these figures reflect units exposed (clients rendering the item page with the updated badge asset) rather than raw assignment count, ensuring we capture true per-protocol behavioral impact without dilution from bounce-prior-to-render sessions.

---

## 3. Context & Supporting Operational Metrics (Collectibles & T&S)

While conversion is the primary read for `exp_2401`, this experiment does not live in a vacuum. It represents the downstream beneficiary of our trust and safety investments following the viral vintage-card auction surge and subsequent counterfeit spike that hit the Collectibles sub-vertical back in August 2025 (managed under lucia.ferreira's T&S team, leading to the GradeSure partnership launch on 2025-09-08).

### The Return-Rate Trajectory
To properly value a +6.8% conversion lift on authenticated items, leadership must weigh it against the category's broader operational health:
- **Counterfeit Peak (Q3FY26):** Collectibles return rates spiked to an alarming **11.2%** as bad-faith actors exploited the traffic rush.
- **Stabilization & Post-Badge Readout (Q4FY26 / Q2FY27 QTD):** With the GradeSure integration active and now reinforced by the prominent verified badge (`exp_2401` rollout), Collectibles return rates have steadily retreated down to **5.4%** (as tracked in the marketplace performance mart). 

This creates a powerful, compounding win for Victor Okonkwo’s Marketplace org: buyers see immediate, trustworthy visual proof of authentication (driving the +6.8% conversion bump), and actual post-purchase buyer friction/returns are cut by more than half compared to the peak.

### Caveats and Internal Friction Notes (For Future PM Reference)
While buyers love the badge, we must remain mindful of the supply side. As camille.duarte and Lucia note in ongoing seller pulse surveys (`fact_seller_voc_responses`), authentication requirements and badge verification steps introduce real friction for new sellers entering Collectibles (where only 24% reach their 10th listing, compared to ~48% in Style). However, for items already cataloged and verified, making that badge prominent is an unalloyed success. There is no intent to roll back or alter the shipped badge display.

---

## 4. Administrative & System Log Notes

- **Slack Channel Aside:** `#exp-marketplace-collectibles` (2025-11-16) — `@sanjay.bhatt`: "Clean as a whistle. +6.8% across the board, no weird traffic side-effects, latency flat. Let's prep the 100% rollout ticket for Wednesday."
- **Jira Reference:** `COL-4192` ("Verified Badge Prominence Rollout to 100%") - Closed/Completed 2025-11-20.
- **Dashboard Check:** Compass BI dashboards have updated to reflect the full 100% treatment allocation as of the morning of November 20, 2025. No downstream pipeline breaks in `traffic_conversion_summary` or `marketplace_gmv_summary` reported by connor.blake.

---
