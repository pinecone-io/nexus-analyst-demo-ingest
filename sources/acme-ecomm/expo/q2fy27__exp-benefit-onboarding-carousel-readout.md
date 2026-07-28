---
title: "Expo experiment readout: 'Benefit Onboarding Carousel' — +9pp 30-day benefit awareness"
source_url: "internal://acme-ecomm/expo/q2fy27__exp-benefit-onboarding-carousel-readout"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: expo_experiment
---

# Expo Experiment Readout: `exp_2556` — Benefit Onboarding Carousel

**Experiment ID:** `exp_2556`  
**Experiment Name:** Benefit Onboarding Carousel  
**Vertical:** MEMBERSHIP  
**Owner:** derek.holloway (Sr PM Membership Benefits & CLTV, assoc_100151)  
**Status:** Shipped / Concluded  
**Dates Active:** 2026-05-01 to 2026-06-15  
**Primary Metric:** 30-day benefit awareness (%)  
**Secondary Metric:** Annual renewal rate (%) *(Not yet valid — cohort lag requirement)*  
**Target Audience:** New and existing Acme+ members across US, CA, and MX markets (`dim_member` panel base and full aggregate marts)  

---

## 1. Executive Summary & Experiment Overview

Following the strategic shift on 2026-06-01 where our streaming bundle partner transitioned from Vidora to Reelstream (per renee.kowalski's membership roadmap), membership analytics highlighted a persistent friction point: while our streaming perk delivers an exceptional 93% standalone renewal rate among members who utilize it, overall awareness of the benefit languished at a meager 34% across the broader Acme+ subscriber base. 

To tackle this gap without immediately spinning up costly new benefit acquisition pipelines, the Membership product team launched `exp_2556` ("Benefit Onboarding Carousel") on **2026-05-01**. The experiment introduced a dynamic, multi-slide visual carousel on the member dashboard and post-signup confirmation screens, directly surfacing high-value underutilized perks—most notably the Reelstream streaming bundle, early shipping access, and member-exclusive events—during the critical first 30 days of membership tenure.

The experiment concluded on **2026-06-15**, running for a full 45-day window. Based on data from `fact_experiment_readouts` and joining back to `fact_membership_events` and `member_cltv`, the variant arm delivered a statistically significant **+9pp lift in 30-day benefit awareness** compared to control. 

However, because annual membership renewals operate on a 12-month lifecycle, **the annual renewal-rate readout for this cohort is NOT yet valid**. Per standard retention analytics rules, evaluating annual renewal requires a full 12-month cohort lag. Consequently, no renewal-rate figure exists yet for the specific `exp_2556` exposure window, and any attempt to compute a short-term renewal proxy would introduce severe survivorship bias. Instead, we tie our expectations for future renewal lift directly to our established, validated mechanisms.

---

## 2. Statistical Readout & Exposure Methodology

The experiment was evaluated using per-protocol exposed units rather than pure intent-to-treat (ITT) assignment, ensuring consistency with our warehouse standards (refer to `fact_experiment_exposures` where `units_exposed` isolates active dashboard interactions from silent background assignments).

| Metric Name | Control Arm | Variant Arm (Carousel) | Lift vs. Control | p-value / Significance | Notes |
|---|---|---|---|---|---|
| **30-Day Benefit Awareness (%)** | 33.8% | 42.8% | **+9.0 pp** | p < 0.001 (Significant) | Measured via post-exposure micro-survey and feature-click tracking (`fact_membership_events`) |
| **Streaming Perk Activation (%)** | 12.1% | 24.6% | **+12.5 pp** | p < 0.001 (Significant) | Direct click-through to Reelstream account linking flow |
| **Average Benefits Adopted (Count)** | 1.14 | 1.82 | **+0.68** | p < 0.01 (Significant) | Shift from single-benefit (free shipping only) toward multi-benefit adoption |
| **Annual Renewal Rate (%)** | *Pending* | *Pending* | **N/A** | **Not Yet Valid** | Requires 12-month cohort lag; current Q2FY27 QTD blended renewal stands at a healthy 87.2% |

### Data Verification & Flat Dataset Validation
Queries against this readout must utilize the flat BigQuery path (`nexus-analyst-demo.acme_ecomm.fact_experiment_readouts`). Analysts attempting to query legacy nested directories (e.g., `acme_ecomm.marts.membership.*`) will encounter path errors, echoing the schema corrections established earlier in the fiscal year by amara.shah and carlos.figueroa. 

Furthermore, when calculating member-level downstream engagement via `member_cltv`, analysts must strictly apply a `LEFT JOIN` to `dim_member` paired with `COALESCE(trailing_12mo_gmv_usd, 0)`. Utilizing an `INNER JOIN` (the recurring cltv join trap) silently drops the 20% dormant segment of our 120,000-member panel (representing members like Marisol, mem_1000178, who maintain active paid plans but generated zero trailing orders), artificially inflating average CLTV from the true $500/member baseline up to a distorted $625/member.

---

## 3. The Mechanistic Bridge: Benefit Adoption Depth & Renewal Correlation

While the direct annual renewal-rate metric for `exp_2556` cannot be calculated until mid-2027, our confidence in the long-term CLTV impact of the Benefit Onboarding Carousel rests entirely on already-validated behavioral correlations stored in `member_cltv` and `fact_membership_events`:

1. **Adoption Depth vs. Renewal Rate:** Historical cohort tracking demonstrates a steep, non-linear jump in retention as members engage with multiple perks. 
   - Members utilizing **0 extra benefits** (relying solely on free shipping) exhibit an annual renewal rate of **71%**.
   - Members adopting **1 benefit** see renewal climb to **89%**.
   - Members adopting **2+ benefits** achieve an extraordinary **95% renewal rate**.
2. **The Streaming Bundle Power-Up:** As noted in our membership baseline metrics, the streaming bundle alone commands a **93% renewal rate** among its users, even though baseline awareness before this experiment hovered at only **34%**. 
3. **Closing the Awareness Gap:** By moving overall 30-day awareness up by +9pp (and driving streaming perk activation up by +12.5pp), `exp_2556` successfully migrates a substantial cluster of members out of the vulnerable "single-benefit / free-shipping-only" bracket (71% renewal risk) and into the multi-benefit adoption tier (95% renewal likelihood).

This operational bridge—bridging the gap between awareness and multi-benefit adoption—is what justifies the rollout decision, even in the absence of an immediate 12-month renewal readout.

---

## 4. Cross-Vertical Context & Operational Noise

While Derek Holloway owns the Membership vertical deliverables for this feature, several parallel initiatives across Acme are worth noting for cross-functional context:

- **US Conversion & Traffic (`US_CONV`):** Maya Lindqvist and Owen Faust continue monitoring site-wide conversion rates (currently pacing at 3.22% Q2FY27 QTD). The minor week-over-week conversion softening observed in mid-July (e.g., the drop from 3.24% to 2.86% between the weeks ending 2026-07-11 and 2026-07-18) has been thoroughly deconfounded. Device-mix shifts (specifically an influx of mobile app traffic which converts lower than web) account for ~0.24pp of the move, while an ordinary net-zero wash between in-flight experiments like Search Relevance Re-ranking (`exp_2601`, +1.6%) and Item Page Media Carousel Autoplay (`exp_2618`, -1.5%) leaves no unexplained anomalies. The concurrent homepage banner refresh (`camp_90219`) is strictly isolated and shares no item-page overlap.
- **Care Deflection & Bot Handoffs:** Aisha Rahman's recent readout for the 'Bot Handoff Threshold' experiment (`exp_2489`, concluded 2026-05-15) demonstrated a +3pp deflection bump with a minor -0.15 CSAT dip among late-escalated users, leading to a partial rollout for non-billing categories. While support ticket volumes remain stable, member care agents report that members who interact with features like Derek's onboarding carousel exhibit significantly fewer billing/perk-activation inquiries during their first 30 days.
- **Marketplace Seller Dynamics:** In the Marketplace vertical, camille.duarte continues addressing seller onboarding friction in Collectibles, where the GradeSure authentication requirement (introduced after the August 2025 counterfeit spike by lucia.ferreira) continues to create a two-sided tension: dropping category returns from an alarming 11.2% down to a healthy 5.4%, while suppressing new-seller survival past listing 10. Fortunately, membership benefits like those promoted in `exp_2556` heavily skew toward our top-tier collectors and style buyers (such as sel_500012 Timeworn Treasures and sel_500204 ReWear Collective), reinforcing the broader ecosystem flywheel.

---

## 5. Next Steps & Action Items

1. **Permanent Rollout:** Following this successful readout, engineering will graduate the Benefit Onboarding Carousel from experimental status (`exp_2556`) to permanent production code for all newly acquired Acme+ subscribers effective **2026-07-25**.
2. **Longitudinal Tracking:** Amara Shah (Data Analyst, Finance/MBR) and wei.hartono (Analytics Engineer) will establish a dedicated cohort tracking tag in `fact_membership_events` to isolate the `exp_2556` user base for 6-month and 12-month renewal checkpoints starting in Q1FY28.
3. **Content Expansion:** Derek Holloway to collaborate with renee.kowalski on expanding the carousel slides to include newly emerging merchant partnerships and seasonal warehouse promotions ahead of the upcoming Q4 peak holiday season (Nov–Jan).

---
