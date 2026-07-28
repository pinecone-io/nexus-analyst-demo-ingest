---
title: "Expo experiment readout: checkout-simplification test, confounded mid-flight by a sitewide nav redesign"
source_url: "internal://acme-ecomm/expo/q1fy27__exp-checkout-simplify-nav-refresh-confound"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-04-15T12:00:00+00:00'
adapter: expo_experiment
---

# Experiment Readout: Checkout Simplify (`exp_2214`) & Nav Refresh Confound (`exp_2215`)

**Author:** owen.faust (Sr PM Checkout & Conversion, US_CONV, assoc_100111)  
**Reviewers:** maya.lindqvist (Director PM US Conversion & Traffic, assoc_100110), wei.hartono (Analytics Engineer, Data, assoc_100210), amara.shah (Data Analyst, Data, assoc_100211)  
**Status:** Shipped (2026-04-06)  
**Date Range:** 2026-02-16 through 2026-03-30  
**BigQuery Tables:** `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures`, `nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`, `nexus-analyst-demo.acme_ecomm.dim_experiment`

---

## 1. Executive Summary & Final Decision

The "Checkout Simplify" experiment (`exp_2214`), which aimed to reduce friction in the US web and app checkout funnels by collapsing the multi-step address/payment confirmation view into a single accordion block, ran from **2026-02-16 to 2026-03-30**. 

Mid-flight on **2026-03-01**, an independent initiative owned by maya.lindqvist's team—the "Nav Refresh" sitewide navigation redesign—was deployed to production. Due to a coordination gap between teams regarding release slotting, Nav Refresh was pushed into *both* the control and treatment arms of `exp_2214` simultaneously. To measure Nav Refresh's independent impact, maya's team carved out a concurrent 5%-of-traffic, 3-week no-launch holdback (`exp_2215`), which completed its readout on **2026-03-21** showing a standalone +1.3% conversion lift sitewide.

Because Nav Refresh contaminated the entire experiment traffic pool after March 1, the full-window read for `exp_2214` (+2.1% conversion lift) represents a confounded joint effect. However, isolating the pre-contamination window (**Feb 16–28**) reveals a clean baseline lift of **+0.8%**. 

On **2026-04-06**, a shipping decision was made to roll out Checkout Simplify to 100% of US traffic based on the headline +2.1% figure, accepting the structural boost from the nav redesign as part of the live checkout experience.

```sql
-- Diagnostic query used to check exposure distribution and partition splits across exp_2214 arms
SELECT
    experiment_id,
    variant,
    exposure_date,
    SUM(units_assigned) AS assigned,
    SUM(units_exposed) AS exposed,
    SUM(units_converted) AS converted,
    SAFE_DIVIDE(SUM(units_converted), SUM(units_exposed)) AS exposed_conversion_rate
FROM `nexus-analyst-demo.acme_ecomm.fact_experiment_exposures`
WHERE experiment_id = 'exp_2214'
GROUP BY 1, 2, 3
ORDER BY exposure_date ASC, variant ASC;
```

---

## 2. Background & Hypothesis

Following the Q4FY26 peak holiday season and the implementation of the session-counting update (`sessions_definition_version` 1→2) on **2026-03-02**, our conversion optimization roadmap for US_CONV prioritized reducing drop-off between the cart review page and final order placement. 

At the same time, separate from checkout engineering, maya.lindqvist's team had been iterating on the global site header, mega-menu dropdowns, and mobile persistent footer ("Nav Refresh"). While Nav Refresh was intended primarily to aid top-of-funnel discovery and reduce bounce rates on category landing pages, its global deployment on March 1 inevitably altered the session context for users entering the checkout flow.

* **`exp_2214` (Checkout Simplify):** Streamlining fields, defaulting billing-same-as-shipping, and minimizing accordion vertical height.
* **`exp_2215` (Nav Refresh Holdback):** A 5% traffic holdback running from March 1 to March 21 to isolate the navigation change from baseline seasonality and other in-flight items (such as the paid-search budget cut initiated back on **2026-02-04**, which dropped US sessions by -5.6% YoY in Q1FY27).

---

## 3. Detailed Readout Breakdown

### A. Full-Window Confounded Read (Feb 16 – Mar 30)
* **Sample Size:** ~14.2M exposed sessions across control and treatment.
* **Metric:** Order conversion rate among exposed units (`units_converted / units_exposed`, per protocol [assigned-vs-exposed]).
* **Observed Lift:** **+2.1%** relative to control ($p < 0.01$, statistically significant).
* **Caveat:** As detailed below, this number absorbs the unisolated impact of Nav Refresh, which launched midway through.

### B. Pre-Contamination Sub-Window (Feb 16 – Feb 28)
To filter out the noise introduced by Nav Refresh, we pulled a clean sub-window query covering the 12 days prior to March 1.
* **Sample Size:** ~4.1M exposed sessions.
* **Observed Lift:** **+0.8%** relative to control ($p = 0.042$).
* **Interpretation:** The true isolated effect of simplifying the checkout accordion is a modest +0.8% conversion lift. The remaining +1.3% delta observed in the full-window read maps almost perfectly to the independent +1.3% lift measured by Nav Refresh's own holdback (`exp_2215`) readout on **2026-03-21**.

```
+--------------------------------------------------------------------------+
|                     EXP_2214 TIMELINE & CONFOUNDING                      |
+--------------------------------------------------------------------------+
|  Feb 16          Feb 28         Mar 01         Mar 21         Mar 30     |
|    |---------------|--------------|--------------|--------------|       |
|    | Clean Window  |              | Nav Refresh  | Holdback     |       |
|    | (+0.8% lift)  |              | Deployed     | Readout (+1.3%)      |
|    |               |              | (Confounded)                |       |
|    |               |              | Joint Read: (+2.1% lift)    |       |
+--------------------------------------------------------------------------+
```

---

## 4. Discussion & Cross-Team Chatter (Slack Excerpts / MBR Prep)

* **owen.faust (03-01 11:15 ET):** *"Wait, did someone just push the nav redesign CSS to production? My checkout experiment variants are suddenly showing a weird step-jump in session duration right around 10am. Is that on my end or did the header change?"*
* **maya.lindqvist (03-01 11:28 ET):** *"Hey Owen! Yeah, sorry, we rolled out Nav Refresh to 100% this morning per the Q1 roadmap. Didn't realize it touched the global wrapper above your checkout frames too. We *do* have a 5% holdback running (`exp_2215`) so we can isolate the sitewide effect, but your traffic pool is definitely getting the new nav in both arms now. Let me know if you want to pause or just ride it out."*
* **amara.shah (Data, 03-02 14:00 ET):** *"Just a reminder to everyone reconciling conversion rates this week: we also have the `sessions_definition_version` 1→2 bot-filtering cutover landing today. Between Owen's checkout test, Maya's nav drop, and the bot cleanup, don't expect the WBR charts to tie out cleanly without segmenting by date."*
* **carlos.figueroa (Data, 03-05 09:30 ET):** *"Let's make sure we document the confound clearly in the MBR appendix. Leadership is going to see the +2.1% on Checkout Simplify and ask why it's higher than the initial spec projection. We need to attribute the +0.8% to Owen's accordion work and the rest to Maya's nav refresh."*

---

## 5. Final Rollout Action

Despite the mid-flight contamination, leadership review on **2026-04-06** concluded that because both the simplified checkout and the new navigation structure were destined for 100% production deployment anyway, the joint positive lift (+2.1%) represented the actual state of the funnel moving forward. Owen Faust completed the rollout ticket in Jira, and the experiment was formally closed out in Expo.

---
