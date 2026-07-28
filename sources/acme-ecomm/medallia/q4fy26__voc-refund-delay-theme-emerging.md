---
title: "Medallia VOC report: 'refund delay' verbatim theme climbing"
source_url: "internal://acme-ecomm/medallia/q4fy26__voc-refund-delay-theme-emerging"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-01-25T12:00:00+00:00'
adapter: medallia_verbatim
---

# Voice of Customer (VoC) Weekly Insight Report — Week Ending 2025-12-20
**To:** Hannah Brennan (SVP Customer Care), Giulia Romano (Analytics Engineer, Care & VOC/Medallia), Dominic Paquet (Care Ops Lead), Amara Shah (Data Analyst, Finance/MBR), Connor Blake (Data Engineer)  
**From:** Analytics & Insights Practice (giulia.romano / assoc_100213)  
**Dataset Reference:** `nexus-analyst-demo.acme_ecomm.fact_voc_responses` (adapter: `medallia_verbatim`)  
**Scope:** Buyer-side post-purchase and post-care-contact survey verbatims across US, CA, and MX markets.

---

## 1. Executive Summary & Weekly Thematic Distribution

As we push deeper into Q4FY26 peak holiday execution, our automated Medallia text-analytics pipeline (`fact_voc_responses`) has processed roughly 12,450 survey completions for the trailing seven-day window ending December 20, 2025. Overall buyer CSAT across all verticals ticked down slightly to 4.12 out of 5.00 (down from 4.24 during the Black Friday surge week of November 28), which is entirely normal seasonal variance given the extreme fulfillment volumes moving through our DC network and carrier partners following Cyber Monday. 

However, looking at granular verbatim theme tagging (`theme_tag`), we are tracking an unusual and sustained upward velocity in a single specific customer grievance category: **`refund delay`**. 

While general delivery-speed and carrier-delay complaints naturally spike every December following winter weather interruptions—such as the 36-hour disruption at our JOL1 (Joliet) DC back on December 8—the `refund delay` theme has historically hovered near a rock-solid, predictable baseline of **~3.5%** of all care-related and post-return verbatims (a stable trend maintained ever since we established our baseline reports back in Q2FY26, per giulia.romano's tracking). 

Starting the week of December 1, 2025 (coinciding with Cyber Monday week volumes), that share began drifting upward. **During the week ending December 20, 2025 (specifically crossing our reporting threshold on Monday, December 15, 2025), the `refund delay` verbatim theme crossed 10% of total care verbatims for the first time**, registering at **11.2%**. 

As an analytics team, we want to flag this early. It is important to emphasize that this is currently a **qualitative leading indicator only**. Quantitative financial metrics, general returns-processing tallies, and standard 4-week-rolling average turnaround cycles have not yet breached any formal SLA thresholds or triggered automated alerts in Compass or our financial ledgers. Consequently, it would be easy to dismiss this as routine holiday noise from anxious shoppers waiting for holiday return credits. Nevertheless, the velocity of the verbatim climb warrants a dedicated section in this week's data distribution package so operational leads are aware before the monthly close.

---

## 2. Week-over-Week Trend Table: Care Verbatim Themes

The table below outlines the weekly evolution of our top five post-care and post-purchase customer dissatisfaction themes across Q4FY26 to date, illustrating how `refund delay` has decoupled from historical baselines while other seasonal complaints have followed expected post-holiday normalization curves.

| Week Ending (Sun–Sat) | Total Survey Volume | Top Theme (`shipping_delay`) % | Second Theme (`item_damaged`) % | Third Theme (`wrong_item`) % | **Target Theme (`refund delay`) %** | Baseline Comparison vs. Q2FY26 |
|---|---|---|---|---|---|---|
| 2025-11-08 | 9,820 | 14.2% | 6.1% | 4.3% | **3.6%** | Flat (+0.1pp) |
| 2025-11-15 | 10,150 | 13.8% | 5.9% | 4.5% | **3.4%** | Flat (-0.1pp) |
| 2025-11-22 | 11,040 | 15.1% | 6.3% | 4.1% | **3.5%** | Flat (0.0pp) |
| 2025-11-29 (Black Friday) | 16,890 | 22.4% | 8.2% | 5.0% | **4.1%** | +0.6pp |
| 2025-12-06 (Cyber Week) | 18,420 | 26.5% | 7.8% | 5.2% | **6.8%** | +3.3pp |
| 2025-12-13 | 14,210 | 19.3% | 6.5% | 4.8% | **8.7%** | +5.2pp |
| **2025-12-20 (Current)** | **12,450** | **16.1%** | **6.2%** | **4.6%** | **11.2%** | **+7.7pp (CROSSES 10% THRESHOLD)** |

*Note: All percentages represent share of total negative sentiment verbatims tagged within `fact_voc_responses` where `survey_type IN ('post_purchase', 'post_care_contact')`.*

---

## 3. Representative Raw Verbatim Extracts (`medallia_verbatim`)

To provide qualitative color for product managers and care operations, below is a randomized sample of raw verbatims pulled directly from `fact_voc_responses` for the week ending December 20, 2025, tagged with `theme_tag = 'refund_delay'`. Customer IDs and order IDs have been masked per privacy guidelines, keeping strictly to our non-overlapping prefix conventions (`voc_`, `ord_`, `mem_`).

> **Response ID:** `voc_8810249`  
> **Market:** US | **Vertical:** US_CONV | **Score:** 2/5 (CSAT) | **Sentiment:** Negative  
> **Verbatim Text:** *"I returned my boots over three weeks ago via drop-off at the local store, and tracking showed it arrived back at your facility on Dec 3rd. My account still says 'Return in Transit' for the refund portion even though customer service chat told me last week it was processed. Where is my money? It’s holding up my credit card bill."*  
> **Associated Order:** `ord_9941028`  

> **Response ID:** `voc_8810512`  
> **Market:** US | **Vertical:** MARKETPLACE (Style)  | **Score:** 1/5 (CSAT) | **Sentiment:** Negative  
> **Verbatim Text:** *"Bought a jacket from a marketplace seller, didn't fit, shipped it back promptly. The seller confirmed receipt on Dec 10th. Acme support keeps telling me standard refund processing takes 3 to 5 business days, but it’s been nearly two weeks and nothing. Your bot just loops me in circles when I type 'refund status'."*  
> **Associated Order:** `ord_9952119`  

> **Response ID:** `voc_8811083`  
> **Market:** CA | **Vertical:** US_CONV | **Score:** 2/5 (CSAT) | **Sentiment:** Negative  
> **Verbatim Text:** *"Usually Acme is great with returns, but this holiday season has been a mess. Returned an unwanted holiday gift package on Dec 2. The tracking receipt says delivered to your returns hub, but no credit has hit my Acme wallet or my bank. When I ask the virtual assistant, it gives me generic canned text about carrier delays."*  
> **Associated Order:** `ord_9963402`  

> **Response ID:** `voc_8811904`  
> **Market:** US | **Vertical:** MEMBERSHIP | **Score:** 1/5 (CSAT) | **Sentiment:** Negative  
> **Verbatim Text:** *"As an Acme+ member I expect faster resolution. My return was marked processed by the carrier two weeks ago, but my refund is stuck in limbo. The chat agent (association ID unavailable, bot-only escalation) couldn't give me a date for when the finance team releases the funds. Very disappointing experience compared to last year."*  
> **Associated Order:** `ord_9978120`  

---

## 4. Operational Context & Preliminary Diagnostics

Before anyone sounds alarm bells, we cross-referenced these verbatims against our other operational pipelines to see if a broader quantitative failure is underway. 

1. **Care Deflection & Bot Performance:** Aisha Rahman's team and Dominic Paquet are continuing to monitor the 'Ask Acme v2' bot (which launched back on 2025-09-15). Deflection rates are holding strong near 45.0% for Q4 peak, but our CSAT among deflected users has dipped slightly from 3.80 down to 3.70 over the last month—largely because automated conversational flows keep running into dead ends when customers ask specific questions about delayed refund disbursements that require human backend access.
2. **Fulfillment & Logistics Cross-Check:** Gabriel Stroud's fulfillment team notes that while the winter storm on December 8 created temporary delivery backlogs at JOL1 (Joliet DC) for 36 hours, outbound shipping is recovering nicely. These refund verbatims, however, are specifically tied to *inbound returns processing*, not outbound shipments. 
3. **Seller-Side Distinction:** As a quick reminder for anyone querying these tables: buyer Medallia verbatims (`fact_voc_responses`) never mix with seller-side feedback (`fact_seller_voc_responses`, our new table for the Seller Pulse survey program). Sellers have their own operational friction points (such as `authentication-friction` in Collectibles due to the GradeSure process), but the `refund delay` spike documented here is strictly coming from end consumers/buyers on the retail and marketplace storefronts.

### Conclusion & Next Steps
Because this is currently a soft, qualitative signal sitting around 11% of care verbatims—and because quantitative metrics like our 4-week-rolling average refund cycle days have not yet breached operational SLA warnings—we recommend keeping this on our radar as an item to watch during the upcoming weekly business review (WBR) cycle, but no immediate executive escalation is warranted today. We will continue tracking verbatim tagging density through the final week of December and report back if the trend breaks past 15%.

---
