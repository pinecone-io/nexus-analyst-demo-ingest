---
title: "Expo experiment spec: 'Verified Badge Prominence' on Collectibles listings"
source_url: "internal://acme-ecomm/expo/q3fy26__exp-verified-badge-prominence-kickoff"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2025-10-15T12:00:00+00:00'
adapter: expo_experiment
---

# Expo Experiment Specification

**Experiment ID:** `exp_2401`  
**Experiment Name:** Verified Badge Prominence on Collectibles Listings  
**System:** Expo Experiment Platform (`dim_experiment` / `fact_experiment_readouts`)  
**Vertical:** Marketplace (Collectibles Sub-vertical)  
**Owner:** sanjay.bhatt (Sr PM Marketplace Collectibles, assoc_100120)  
**Status:** Running  
**Start Date:** 2025-10-01  
**Target End Date:** 2025-11-15 (6 weeks)  

---

## 1. Context & Background

Following the viral vintage-card auction spike back on 2025-08-04, which triggered a severe influx of both bad-faith actors and legitimate new buyers into the Collectibles sub-vertical, Trust & Safety (led by lucia.ferreira) fast-tracked the launch of the "Acme Verified" authentication program in partnership with GradeSure on 2025-09-08. While that program has successfully established a gate for verifying item authenticity, early user feedback and browsing behavior on item detail pages suggest that the authenticity badge is currently buried below the fold on mobile views and under-emphasized next to primary pricing modules on desktop.

This experiment follows directly from the strategic priorities outlined in the Q3FY26 Marketplace PRD for Collectibles listing surface enhancements. Since the counterfeit spike and the subsequent GradeSure integration, buyer hesitation around high-ticket trading cards and memorabilia has remained a silent friction point, even as overall Marketplace GMV continues its strong run toward our annual targets. 

We need to test whether driving visual prominence to the Acme Verified badge will measurably improve buyer conversion without introducing layout regressions or diluting secondary modules like seller ratings and shipping promises.

---

## 2. Hypothesis

**If** we visually elevate the Acme Verified authentication badge (increasing its render size by 35%, moving it above the item title on mobile views, and applying a high-contrast accent border), **then** buyer-side conversion on Collectibles listings will increase because prospective high-intent collectors will experience immediate visual reassurance regarding item authenticity before scrolling past the fold.

---

## 3. Variant Architecture

The experiment is configured as a standard A/B test across all device types (web, app, and store kiosks) for traffic hitting the Collectibles sub-vertical (`vertical_code = 'MARKETPLACE'`, `sub_vertical_code = 'COLLECTIBLES'`).

- **Variant Control (`control`):** Standard current layout. Acme Verified badge appears below the price module in standard body text weight, alongside secondary metadata.
- **Variant Treatment (`treatment_a`):** Prominent placement. Badge rendered directly below the item title, 35% larger bounding box, featuring the official GradeSure-verified shield graphic with a subtle metallic gradient border and a tooltip linking to the authentication guarantee explainer.

Traffic split: **50% Control / 50% Treatment**. Unit of assignment is the visitor session, tracked via `fact_experiment_exposures`.

---

## 4. Primary & Secondary Metrics

### Primary Metric
- **Item-Page Conversion Rate:** `orders / product_view_sessions` scoped strictly to Collectibles listings (`fact_traffic_daily` and `fact_orders` joined on `sub_vertical_code = 'COLLECTIBLES'`).

### Guardrail Metrics
- **Bounce Rate / Immediate Pagedrop:** Share of sessions dropping off the item page within 5 seconds of load (monitored via FullStory qualitative checks and BigQuery clickstream session durations).
- **Add-to-Cart Rate:** View-to-cart conversions on Collectibles items to ensure we are not inadvertently harming intermediate engagement.
- **Care Contact Rate Post-Purchase:** Ensuring no spike in post-purchase inquiries regarding item authenticity or misleading badge representation (tracked via `fact_care_contacts` where `sub_program = 'automate'` or `'avoid'`).

---

## 5. Target Sample Size & Power Calculations

Based on baseline Collectibles traffic run-rates from Q2FY26 (averaging ~25M to $61M GMV across the quarter, translating to approximately 1.2M monthly product view sessions in the sub-vertical), we have configured the sample size parameters to achieve 80% statistical power at an alpha of 0.05, assuming a Minimum Detectable Effect (MDE) of +3.0% relative lift in conversion rate.

- **Required Exposed Units per Arm:** ~450,000 sessions.
- **Estimated Duration:** 6 weeks (scheduled to conclude on 2025-11-15, capturing sufficient volume across weekend collector surges).

---

## 6. Operational Notes & Engineering Aside

*Slack aside from connor.blake (Data Engineer) on 2025-10-02:*
> "Hey Sanjay, just making sure your exposure logging for `exp_2401` is routing cleanly through `fact_experiment_exposures`. Remember that after that minor Airflow hiccup we had in June with the `marketplace_gmv_summary` mart running 14 hours stale, we've been extra sensitive to pipeline delays on Marketplace data streams. Let me know if your exposure counts start looking decoupled from session traffic so I can check the BigQuery partition filters."

*Response from sanjay.bhatt:*
> "Thanks Connor, everything looks solid so far on the ingestion side. Exposures are populating at the expected ratio. We'll let it run through the 6-week window and pull the full readout in mid-November."

As of today's date (2025-10-15), the experiment is actively running in its third week. No ship or kill decisions have been made yet; all data collection is proceeding as specified. Final analysis, including intent-to-treat vs. per-protocol checks (`units_assigned` vs. `units_exposed`), will be logged upon experiment completion in a subsequent readout document.

---
