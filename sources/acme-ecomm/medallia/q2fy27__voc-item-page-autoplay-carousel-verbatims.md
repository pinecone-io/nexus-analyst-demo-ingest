---
title: "Medallia VOC note: low-volume item-page verbatims skew negative on the new autoplay media module"
source_url: "internal://acme-ecomm/medallia/q2fy27__voc-item-page-autoplay-carousel-verbatims"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: medallia_verbatim
---

# Medallia Analytics Extraction & Qualitative Note
**Dataset / Table:** `nexus-analyst-demo.acme_ecomm.fact_voc_responses` (Adapter: `medallia_verbatim`)  
**Target Scope:** Item-page-adjacent post-purchase and NPS verbatims (`survey_type IN ('post_purchase', 'nps')`, filtered for item-page or product-view context string matches)  
**Time Window:** Weeks of 2026-07-11 and 2026-07-18  
**Author / DRI:** giulia.romano (Analytics Engineer, Care & VOC/Medallia, `assoc_100213`)  
**Reviewers:** maya.lindqvist (`assoc_100110`), hannah.brennan (`assoc_100020`), amara.shah (`assoc_100111`)  

---

## 1. Executive Summary & Context

Following the mid-quarter review discussions and as part of our routine weekly Medallia VOC text-mining pulls for the US conversion and experience squads, this note summarizes a targeted extraction of item-page-adjacent verbatims from the weeks of **2026-07-11** and **2026-07-18**. 

This exact timeframe aligns directly with when the **'Item Page Media Carousel Autoplay'** experiment (`exp_2618`, owned by maya.lindqvist, initiated **2026-06-08**) has been actively exposed to a share of US web and mobile traffic. As noted in recent experiment readouts and last week's mid-quarter experimentation review with felix.arroyo, `exp_2618` has been exhibiting a modest negative interim conversion drag on its exposed arm (roughly -1.5%), running concurrently and in opposite directions to owen.faust's positive 'Search Relevance Re-ranking' experiment (`exp_2601`). 

While quantitative dashboards catch the session-level and conversion-rate variance, this Medallia pull provides the qualitative texture directly from shoppers experiencing the new media module in the wild. 

*Important Caveat on Volume:* We want to be explicit up front. **This is a low-volume signal, explicitly NOT yet a top theme by overall share** in our company-wide Medallia taxonomy. Standard post-purchase and NPS feedback continues to be dominated by delivery timing, general site navigation, and pricing queries. However, among respondents who specifically reference product detail pages, item imagery, or media loading during the 07-11 and 07-18 windows, a distinct qualitative pattern has emerged regarding the new autoplay media module. It is a small, early, and carefully caveated signal—not a crisis, but directly on-point qualitative texture for anyone investigating why item-page engagement and conversion softened slightly in this exact window.

---

## 2. Operational Background & Noise

Before diving into the verbatims, a brief note on pipeline housekeeping and background noise from the analytics engineering channel:
- Connor Blake (`assoc_100212`) reported that the BigQuery streaming buffer for `fact_voc_responses` experienced a brief 2-hour latency hiccup on Tuesday morning due to an Airflow worker node restart, but backfill completed cleanly by 04:00 ET with zero dropped payload records.
- We should remind everyone (especially newer analysts joining the rotation) that buyer-side Medallia verbatims in `fact_voc_responses` must **never** be blended with the new `fact_seller_voc_responses` table (managed by camille.duarte for the Seller Pulse survey program). Blending buyer satisfaction scores with seller onboarding feedback continues to be a recurring anti-pattern in ad hoc queries; remember that buyer VOC uses the `voc_` prefix and seller VOC uses the `svoc_` prefix with entirely separate survey instruments.
- Also, office logistics reminder: floor 4 east wing coffee machine is out of service again until Thursday vendor maintenance arrives. Please use the 3rd floor pantry.

---

## 3. Targeted Verbatim Pull: Autoplay Media Module Feedback

The following responses were extracted from `fact_voc_responses` where `score_type IN ('nps_0_10', 'csat_1_5')` and `verbatim_text` contains keyword matches for `video`, `autoplay`, `carousel`, `moving`, `clutter`, or `slow` within sessions mapped to item pages during the target window.

### Representative Quotes (Sample Batch, n = 34 total tagged mentions across two weeks)

1. **`resp_883201a`** | *2026-07-12 14:22:10* | NPS: 7 (Passive) | Market: US | Device: Mobile Web  
   > *"Was trying to check the dimensions on the coffee table and as soon as the page loaded, the video in the photo reel just started playing automatically with sound on. Super jarring on a phone when you're scrolling in a quiet room. Felt really cluttered."*

2. **`resp_883492f`** | *2026-07-14 09:15:40* | CSAT: 3/5 | Market: US | Device: Desktop Web  
   > *"The new product pages feel much busier than they used to. The video just starts and it's annoying when you're trying to swipe through product photos. You have to hunt for the pause button."*

3. **`resp_884102c`** | *2026-07-15 18:04:33* | NPS: 6 (Detractor) | Market: US | Device: App  
   > *"Page feels slower now. Every time I click on a shoe listing, it stutters for a second while that banner video loads and loops. I liked the old static photo gallery better—it was cleaner."*

4. **`resp_884955h`** | *2026-07-17 11:38:12* | CSAT: 2/5 | Market: US | Device: Mobile Web  
   > *"Why are product videos autoplaying? It drains my battery and makes the page jump around while images are still rendering. Please give an option to turn that off or stop doing it."*

5. **`resp_885201k`** | *2026-07-18 16:50:02* | NPS: 8 (Promoter, with comment) | Market: US | Device: Desktop Web  
   > *"Love Acme as always, but the new product page layout with the moving video at the top takes getting used to. It feels a bit busy, like an ad rather than a store listing."*

---

## 4. Quantitative Correlation & Analysis

To place these verbatims in proper analytical context, we cross-referenced the verbatim timestamps and user sessions with `fact_traffic_daily` and the active experiment tracking for `exp_2618`.

- **Volume Context:** Out of approximately 2.4 million post-purchase and browsing-feedback survey prompts delivered during the weeks of July 11 and July 18, only **34 total responses** contained explicit negative or critical verbatims referencing autoplay, media loops, or page sluggishness on item detail pages. This represents roughly **0.0014%** of total survey respondents—statistically minor, and far below major systemic operational issues like the winter holiday refund-delay spike we investigated back in December/January (`[voc-leads-quant]`).
- **Surface & Device Skew:** Over 70% of these specific verbatims originated from mobile web or smartphone app sessions, where screen real estate is constrained and unexpected media loading disrupts vertical scrolling. This aligns with maya.lindqvist's item-page surface telemetry showing higher sensitivity to above-the-fold DOM weight changes on mobile devices.
- **Connection to `exp_2618`:** The timing is too precise to dismiss. The experiment exposure logs confirm that `exp_2618` ('Item Page Media Carousel Autoplay') rolled out to its treatment cohort on **2026-06-08**, and these verbatim complaints began trickling in with low frequency shortly thereafter, ticking up slightly during the heavy traffic weeks of mid-July. 
- **The "Masked Trend" Context:** As felix.arroyo and owen.faust discussed during the Q2 mid-quarter review, `exp_2618`'s -1.5% conversion drag is currently being masked on aggregate dashboards by owen's positive search re-ranking experiment (`exp_2601`, +1.6%). If an analyst looked only at top-line US conversion, they might see a net wash (~+0.05%) and assume no customer friction exists. However, these Medallia verbatims give us the exact human reason *why* the autoplay variant is underperforming: shoppers find the unprompted motion "cluttered," "annoying," and productive of a perceived "slower" page render, even if the raw backend load time delta is within acceptable engineering tolerances.

---

## 5. Next Steps & Recommendations

1. **Share with Product & UX:** Forwarded this verbatim batch directly to maya.lindqvist (`assoc_100110`, Director PM US Conversion & Traffic) and the item-page product pod to inform the upcoming readout and post-experiment decision for `exp_2618`. 
2. **No Premature Panic:** Reiterate to the broader analytics team that this is *not* a cascading operational failure (unlike the December refund delay crisis where Medallia verbatims led quantitative drop by 3 weeks). It is an early, low-volume qualitative indicator of user friction on a specific test module.
3. **Incorporate into Experiment Wrap-up:** Ensure these verbatim IDs (`resp_883201a` through `resp_885201k`) are referenced in the Confluence experiment conclusion page when `exp_2618` reaches its scheduled end date, providing qualitative context alongside the quantitative conversion lift/drag figures.

---
