---
title: "Medallia VOC theme report: Q2FY26 baseline theme distribution"
source_url: "internal://acme-ecomm/medallia/q2fy26__voc-baseline-theme-report-q2fy26"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2025-07-15T12:00:00+00:00'
adapter: medallia_verbatim
---

# Medallia Voice of Customer (VOC) — Q2FY26 Baseline Theme Distribution Report
**Author:** giulia.romano (Analytics Engineer, Data & Analytics, assoc_100213)  
**Distribution:** Internal Analytics, Care Leadership, US Conversion Ops, Membership Product Group  
**Dataset Reference:** `nexus-analyst-demo.acme_ecomm.fact_voc_responses`  
**Reporting Period:** Q2FY26 Baseline Window (May 1, 2025 – July 15, 2025 partial)  

---

## 1. Executive Summary & Methodology Overview

Following the close of Q1FY26 and the data harmonization reviews coordinated across Analytics since carlos.figueroa's promotion to VP of Data & Analytics back in March (`assoc_100060`), this quarterly baseline distribution report establishes the standard theme classifications, verbatim share distribution, and sentiment balances across all buyer-side Medallia survey channels (`post_purchase`, `post_care_contact`, and standalone `nps`) for Q2FY26.

As a routine operational checkpoint — operating well ahead of any seasonal stress tests or late-year fulfillment volume surges — this document sets the quiet "before" benchmark. Across the ~40,000 representative verbatim response rows captured in our sample panel for this quarter, customer sentiment remains overwhelmingly stable, tracking normal retail operations across physical fulfillment, digital checkout flows, Marketplace transactions, and Acme+ membership interactions.

For engineering teams querying the flat BigQuery tables (`nexus-analyst-demo.acme_ecomm.fact_voc_responses`), please note that buyer-side Medallia verbatims remain strictly separated from the newly introduced seller-side pulse survey streams (`fact_seller_voc_responses`, managed via the `seller_pulse_survey` adapter). Blending buyer satisfaction verbatims with seller onboarding feedback continues to be an anti-pattern; analysts should maintain table separation when auditing sentiment trends.

---

## 2. Q2FY26 Theme Distribution Baseline Table

The following table summarizes the primary theme tags assigned across all inbound buyer verbatims during the Q2FY26 baseline window. Percentages reflect share of total tagged verbatims (excluding uncategorized general praise/complaints).

| Theme Tag | Primary Vertical / Domain | Baseline Share (%) | Dominant Sentiment | Representative Survey Type |
|---|---|---|---|---|
| `shipping-speed-satisfaction` | SPEED / Fulfillment | 24.2% | Positive | `post_purchase` |
| `checkout-ease` | US_CONV | 18.5% | Positive / Neutral | `post_purchase` |
| `membership-benefit-awareness` | MEMBERSHIP | 12.1% | Neutral | `nps` |
| `marketplace-authenticity-trust` | MARKETPLACE (Collectibles/Resold) | 8.4% | Positive / Neutral | `post_purchase` |
| **`refund-delay`** | **CARE / POR** | **3.5%** | **Negative** | `post_care_contact` |
| `packaging-sustainability` | SPEED / OPD_DFS | 3.1% | Positive | `post_purchase` |
| `search-relevance-mismatch` | US_CONV | 2.8% | Negative | `post_purchase` |
| `promotional-discount-application` | PAYMENTS / US_CONV | 2.5% | Neutral | `post_purchase` |
| *Unclassified / General Inquiries* | *Various* | *24.9%* | *Neutral* | *Mixed* |

### Notes on Baseline Stability:
- **Refund Delay Baseline:** The `refund-delay` theme registers precisely at a stable baseline share of **3.5%** of categorized verbatims for Q2FY26. This reflects ordinary transactional churn and minor returns-processing intervals across our DC network. There are no indications of localized facility backlogs or systemic operational friction in this metric as of mid-July 2025.
- **Shipping Speed:** Registering at nearly a quarter of all categorized positive verbatims (`24.2%`), customer commentary continues to praise reliable fulfillment times, particularly for standard ship-to-home orders routed through major DCs like JOL1 and FON2.
- **Membership Benefits:** With the Acme+ streaming benefit rollout under the original Vidora partnership having launched earlier this summer (June 1, 2025, under renee.kowalski), `membership-benefit-awareness` verbatims primarily cluster around neutral inquiries regarding how to link subscriber accounts, validating that awareness campaigns are reaching initial adoption cohorts without creating major friction.

---

## 3. Representative Verbatim Batch (Neutral-to-Positive Baseline)

To maintain standard qualitative auditing practices for the Medallia adapter pipeline, below is a randomized sample of verbatim records pulled directly from `fact_voc_responses` for the current Q2FY26 reporting epoch. Names and identifying order tokens have been masked where appropriate.

> **Response ID:** `voc_882910a`  
> **Channel:** `post_purchase` | **Vertical:** `US_CONV` | **Score:** `9/10 (NPS)`  
> **Verbatim Text:** *"Checking out on the mobile app was super quick this time around. Saved my card info securely, and the order confirmation hit my inbox before I even closed the browser tab. Happy with the experience."*  
> **Theme Tag:** `checkout-ease` | **Sentiment:** `positive`  

> **Response ID:** `voc_882911b`  
> **Channel:** `post_purchase` | **Vertical:** `SPEED` | **Score:** `5/5 (CSAT)`  
> **Verbatim Text:** *"Ordered standard ground shipping for a home goods restock and it arrived two days ahead of the initial delivery promise window. Box was intact and well-packaged."*  
> **Theme Tag:** `shipping-speed-satisfaction` | **Sentiment:** `positive`  

> **Response ID:** `voc_882912c`  
> **Channel:** `nps` | **Vertical:** `MEMBERSHIP` | **Score:** `8/10 (NPS)`  
> **Verbatim Text:** *"I've had the Acme+ annual membership for a couple of years now. Free shipping pays for itself easily, though I only recently realized there was a streaming perk included through Vidora. Might check that out later this week."*  
> **Theme Tag:** `membership-benefit-awareness` | **Sentiment:** `neutral`  

> **Response ID:** `voc_882913d`  
> **Channel:** `post_purchase` | **Vertical:** `MARKETPLACE` | **Score:** `4/5 (CSAT)`  
> **Verbatim Text:** *"Bought a vintage watch band through one of the resold partners (Loop Resale Collective). Item matched the photos closely and shipping was prompt. Good marketplace experience overall."*  
> **Theme Tag:** `marketplace-authenticity-trust` | **Sentiment:** `positive`  

> **Response ID:** `voc_882914e`  
> **Channel:** `post_care_contact` | **Vertical:** `CARE` | **Score:** `3/5 (CSAT)`  
> **Verbatim Text:** *"I had to return a duplicate shirt order from last week. The drop-off at the counter was easy, but it took about four business days for the refund confirmation to show up in my account. A bit slower than I expected, but customer service chat answered my question right away."*  
> **Theme Tag:** `refund-delay` | **Sentiment:** `negative` *(Note: Represents baseline 3.5% distribution; routine processing timeframe).*  

> **Response ID:** `voc_882915f`  
> **Channel:** `post_purchase` | **Vertical:** `US_CONV` | **Score:** `7/10 (NPS)`  
> **Verbatim Text:** *"The site search is generally fine, though sometimes when looking for specific apparel brands I have to scroll past several sponsored items before finding the exact style category."*  
> **Theme Tag:** `search-relevance-mismatch` | **Sentiment:** `neutral`  

---

## 4. Operational Aside & Cross-Team Chatter

*Slack excerpt from internal channel `#analytics-voc-ops` (2025-07-14):*
> **giulia.romano [10:14 AM]:** Morning team, just pushed the Q2 baseline theme distribution models to BigQuery. Everything is tracking within standard variance. The refund delay cluster is hovering right around 3.5% like clockwork. No anomalies to report.
> 
> **amara.shah [10:18 AM]:** Thanks Giulia. Pulling these into the MBR data appendix for carlos.figueroa's review ahead of Thursday's leadership sync. Quick question — are we still seeing any schema drift on the `post_care_contact` survey type after last week's pipeline patch?
> 
> **connor.blake [10:22 AM]:** Pipeline partition looks clean on my end. All `fact_voc_responses` rows are mapping correctly to `nexus-analyst-demo.acme_ecomm`. No nested path errors this time (re: our old March adventures with flat dataset migration). We're good.
> 
> **giulia.romano [10:25 AM]:** Perfect. Let's lock this version as the official Q2 baseline checkpoint. Back to working on the membership satisfaction cross-cuts for renee.kowalski's team.

---
