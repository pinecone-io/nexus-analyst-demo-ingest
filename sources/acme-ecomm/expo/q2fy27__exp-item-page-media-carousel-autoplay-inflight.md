---
title: "Expo experiment spec + in-flight readout: 'Item Page Media Carousel Autoplay' (exp_2618), -1.5% on exposed arm"
source_url: "internal://acme-ecomm/expo/q2fy27__exp-item-page-media-carousel-autoplay-inflight"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: expo_experiment
---

# Expo Experiment Spec & In-Flight Status: `exp_2618`

**System of Record:** `acme_ecomm.dim_experiment` / `acme_ecomm.fact_experiment_readouts` (Expo adapter)  
**Experiment ID:** `exp_2618`  
**Experiment Name:** Item Page Media Carousel Autoplay  
**Vertical Code:** `US_CONV` (US Market, View Item Page surface)  
**Owner:** `maya.lindqvist` (`assoc_100110`, Director PM US Conversion & Traffic)  
**Status:** `running` (In-flight as of 2026-07-20 Q2FY27 snapshot)  
**Start Date:** 2026-06-08  
**Scheduled End Date:** TBD (Pending Q3 planning cycle review)  

---

## 1. Executive Summary & Current In-Flight Readout

`exp_2618` was kicked off on **2026-06-08**—coincidentally the exact same day Owen Faust launched his search relevance experiment (`exp_2601`), though the two are entirely independent initiatives with separate design documents, distinct code paths, and different optimization targets. 

The core hypothesis behind `exp_2618` was straightforward and well-intentioned: auto-playing product media carousels upon landing on the item page would immediately showcase product detail, dynamic angles, and high-fidelity video clips without requiring an explicit user swipe or click. The product team anticipated this would drive a deeper sense of engagement, increase add-to-cart rates, and ultimately lift overall conversion.

However, as of **2026-07-20** (with Q2FY27 88% elapsed), the interim readout presents a sobering picture: **the exposed arm is currently showing a -1.5% conversion drop** compared to control. Far from acting as a positive engagement driver, the autoplay behavior appears to be backfiring on the user experience. 

Despite the negative trend, **no ship or kill decision has been made yet.** The experiment remains actively `running` while the team monitors traffic stability, collects FullStory qualitative session notes, and evaluates whether the friction is concentrated in specific device classes or network conditions. Pre-empting the formal Q3 planning cycle review is not on the table; we are letting the sample size accumulate while tracking how this interacts with adjacent traffic shifts.

---

## 2. Background, Hypothesis & Variant Design

### Hypothesis
> *"Auto-playing primary product videos and secondary gallery media on the item page load will increase initial engagement depth, reduce bounce rates, and yield a net-positive conversion lift by eliminating the interaction friction required to discover dynamic product media."*

### Design & Variants
- **Control (`control`)**: Standard static hero image with manual swipe/click pagination dots and user-initiated video play buttons.
- **Variant A (`autoplay_hero`)**: Primary media item (whether high-res render or 1080p video clip) automatically initiates playback/rotation upon the `DOMContentLoaded` and lazy-load intersection observer settling, looping twice before pausing on the final frame. Subsequent gallery items remain manual.

### Primary & Guardrail Metrics
- **Primary Metric:** Session-scoped conversion rate (`orders / sessions` on exposed units).
- **Guardrail Metrics:** 
  - Page load time / Core Web Vitals (`Largest Contentful Paint` and `First Input Delay`).
  - Add-to-cart rate (`add_to_cart_sessions / product_view_sessions`).
  - Bounce rate / immediate item-page abandonments (< 5 seconds).

---

## 3. Current In-Flight Readout (`fact_experiment_readouts`)

Queried directly from `acme_ecomm.fact_experiment_readouts` for the current Q2FY27 observation window:

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
WHERE experiment_id = 'exp_2618'
  AND as_of_date = '2026-07-20';
```

| experiment_id | variant | as_of_date | metric_name | metric_value | sample_size_units | lift_vs_control_pct | is_significant | notes |
|---|---|---|---|---|---|---|---|---|
| exp_2618 | control | 2026-07-20 | conversion_rate | 0.0324 | 4,210,850 | NULL | FALSE | Baseline control group |
| exp_2618 | autoplay_hero | 2026-07-20 | conversion_rate | 0.0319 | 4,198,210 | **-1.54%** | TRUE (p < 0.05) | Interim read: consistent negative drag observed since late June |

### Exposure Tracking & Assigned vs. Exposed Units
Per convention 7 and the design of `fact_experiment_exposures`, analysis is strictly computed on **exposed units** (users who actually rendered the carousel component and fired the impression pixel), filtering out assignment drops who bounced before asset loading.

| variant | units_assigned | units_exposed | units_converted |
|---|---|---|---|
| control | 4,450,120 | 4,210,850 | 136,432 |
| autoplay_hero | 4,448,900 | 4,198,210 | 133,922 |

---

## 4. Ordinary Expo-Doc Noise & Operational Side Notes

### Guardrail Check: Page Load Time & Core Web Vitals
As flagged during the engineering sync on Monday morning by `connor.blake`, any autoplay video asset introduces downstream payload weight. The guardrail check for item-page LCP shows a slight degradation:
- **Control LCP (median):** 1.42s
- **Exposed LCP (median):** 1.88s (+0.46s penalty due to parallel media fetching)
While within tolerable platform limits (< 2.5s), the added visual latency on lower-end mobile web sessions correlates strongly with the observed conversion drag.

### Qualitative Session Review (FullStory / Medallia Notes)
Verbatim feedback from Medallia post-purchase surveys and FullStory session replays in the exposed arm highlight emerging themes:
- *"The video just starts playing out of nowhere and it's jarring when I'm trying to read specs."*
- *"Page feels slightly more jittery on mobile when scrolling past the hero image while it initializes."*
- Low aggregate complaint volume (not yet a dominant Medallia theme like the refund delays from the past winter), but qualitatively consistent with the quantitative -1.5% drag.

### Adjacent Experiments Running Concurrently
It is worth noting for executive MBR reporting that `exp_2618`'s -1.5% negative lift is currently running in parallel with Owen Faust's Search Relevance Re-ranking experiment (`exp_2601`, also kicked off on 2026-06-08), which is posting a positive **+1.6% conversion lift** on its exposed arm, on the same US conversion surface.

---

## 5. Next Steps & Governance

1. **Continue Running through Q2 Close:** No emergency kill switch has been pulled. The experiment will continue collecting data through the remainder of Q2FY27.
2. **Segment Breakdown Required:** `amara.shah` is pulling a device-split readout (web vs. app) to determine if the penalty is exclusively driven by mobile web bandwidth constraints or if native app users are similarly put off by the motion.
3. **Q3 Planning Hand-off:** Maya Lindqvist will take the finalized readout into the upcoming Q3FY27 planning sessions to decide whether to iterate on a click-to-play variant or officially deprecate the autoplay mechanic.

---
