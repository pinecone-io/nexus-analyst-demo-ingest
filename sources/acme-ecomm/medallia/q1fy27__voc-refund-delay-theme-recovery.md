---
title: "Medallia VOC report: 'refund delay' theme share recovering post-fix"
source_url: "internal://acme-ecomm/medallia/q1fy27__voc-refund-delay-theme-recovery"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-04-15T12:00:00+00:00'
adapter: medallia_verbatim
---

# Medallia Voice of Customer (VOC) Insights & Theme Tracking
**Author:** giulia.romano (Analytics Engineer, Care & VOC/Medallia)  
**Distribution:** Care Leadership, MBR Analytics Pack, Executive Team, Fulfillment Ops  
**Dataset:** `nexus-analyst-demo.acme_ecomm.fact_voc_responses` (adapter: `medallia_verbatim`)  
**Scope:** Q1FY27 Full-Month Follow-Up Report  

---

### Executive Summary & Context

Following up on our Q4FY26 escalations and the operational crisis that peaked around the turn of the fiscal year, this report tracks the longitudinal trajectory of the **`refund delay`** verbatim theme within our Medallia buyer-side VOC stream (`fact_voc_responses`). 

As established in our historical tracking and reviewed during the turbulent 2026-02-02 MBR escalation (where hannah.brennan and fulfillment leadership formally addressed the Ontario, CA returns-processing center bottlenecks), customer sentiment regarding post-purchase returns had severely degraded. The qualitative data flagged the operational friction long before it cleanly crossed quantitative SLA tripwires—a classic demonstration of VOC leading quantitative metrics. Specifically, the `refund delay` theme share surged past the 10% threshold during the week of 2025-12-15 (hitting 11.2%) and ultimately peaked at an alarming **16.1% during the week of 2026-01-05**, perfectly coinciding with the period when our 4-week-rolling `avg_refund_cycle_days` breached its 5.0-day SLA alert threshold (hitting 5.03 days).

With the emergency overtime authorization, temp-worker surges, and the subsequent **Ontario returns center staffing restoration on 2026-02-20**, the operational backlog has cleared steadily through March 2026. This report provides the definitive qualitative confirmation that the fix worked. As the physical processing queue cleared, the `refund delay` theme share has declined back down from its January peak toward our historical ~3.5% baseline. 

---

### Longitudinal Theme Share Progression (Nov 2025 – March 2026)

To understand the full arc of this incident and its resolution, we pull aggregate theme counts from `fact_voc_responses` across post-purchase surveys in the US, CA, and MX markets. While our overall buyer VOC sample comprises ~40,000 representative rows across the warehouse's modeled quarters, the post-purchase subset specifically captures refund-timing sentiment.

| Period / Week Ending | Total Post-Purchase Responses | `refund delay` Theme Count | Theme Share (%) | Operational Status / Notes |
|---|---|---|---|---|
| **2025-11-28** (Black Friday Week) | 3,120 | 148 | 4.7% | Initial seasonal volume surge; processing holding steady. |
| **2025-12-15** | 2,940 | 329 | **11.2%** | **First VOC Flag:** Crosses the 10% alert threshold; JOL1 winter storm adds minor downstream noise. |
| **2026-01-05** | 3,450 | 555 | **16.1%** | **Peak Share:** Aligns with quantitative SLA breach (5.03 days rolling); Ontario understaffing unmasked. |
| **2026-01-26** | 3,180 | 445 | 14.0% | Emergency overtime authorized (hannah.brennan); backlog plateauing. |
| **2026-02-02** | 2,890 | 361 | 12.5% | **MBR Escalation:** Formal executive review; hiring freeze exception error corrected for Ontario. |
| **2026-02-20** | 2,750 | 258 | 9.4% | **Staffing Restored:** Ontario returns center back to full headcounts; processing velocity catches up. |
| **2026-03-02** | 2,620 | 175 | 6.7% | Post-cutover session definition version 2 active; inbound complaint volume rapidly easing. |
| **2026-03-15** | 2,510 | 90 | **3.6%** | **Baseline Recovery:** Theme share returns to historical normal (~3.5%); refund cycle days at ~3.3 days. |

As shown in the table above, the qualitative recovery mirrors the quantitative normalization of `avg_refund_cycle_days` (which dropped from its 5+ day peak back down to its historical ~3.3-day baseline by mid-March 2026). VOC has thus performed its full-circle role within Acme's analytics ecosystem: **it flagged the operational failure first** (weeks before the quantitative rolling average caught up), **tracked the severity during the peak crisis**, and **now provides the final qualitative confirmation** that the customer experience has stabilized.

---

### Representative Verbatim Tone Shift

The qualitative transformation is starkest when examining the actual customer text strings pulled from `fact_voc_responses`. Comparing verbatims from the peak crisis window (January 2026) against those captured following the March 2026 clearing of the backlog reveals a total shift in customer sentiment and frustration levels.

#### Peak Crisis Era (January 2026 verbatims)
> *"I sent my return back via ship-to-home on December 18th. Tracking showed it arrived at the Ontario facility over three weeks ago, but the status is completely frozen. Care bot just loops me in circles saying 'returns take 3-5 days to process.' This is completely unacceptable for an Acme+ member of four years."*
> — Member `mem_1000042` (Dana), Post-Purchase Survey, score `1/10` (NPS), sentiment `negative`, theme_tag `refund delay`.

> *"Where is my refund? It's been 22 days since drop-off. I've contacted support twice and gotten nowhere. If I had known getting my money back would take a month, I would have used another retailer."*
> — Anonymous Respondent, Post-Purchase Survey, score `2/10`, sentiment `negative`, theme_tag `refund delay`.

#### Post-Fix Recovery Era (March 15, 2026 onward verbatims)
> *"Returned an item that didn't fit last week and the refund hit my card within four days. Much faster than my last experience over the holidays—thank you for sorting that out."*
> — Member `mem_1000640` (Oskar), Post-Purchase Survey, score `9/10`, sentiment `positive`, theme_tag `refund delay` (resolved/positive context).

> *"Process was smooth. Dropped the package off at local curbside, got confirmation next day, and the credit was issued promptly. Appreciate the improvement."*
> — Anonymous Respondent, Post-Purchase Survey, score `8/10`, sentiment `positive`, theme_tag `refund delay` (none).

---

### Internal Operations & Side-Channel Notes (Noise & Context)

*Note: While compiling this longitudinal view, data engineering (connor.blake) and analytics (amara.shah) spent considerable time auditing why Compass dashboards occasionally mismatch historical figures if caches aren't manually refreshed—particularly regarding Q4FY26 Marketplace GMV restatements ($952.4M flash vs. $975.0M canonical). This has no direct bearing on Medallia data but is worth keeping in mind if cross-referencing finance decks.*

Additionally, parallel work is continuing in the Care vertical regarding the "Ask Acme v2" bot (dominic.paquet, aisha.rahman). Deflection rates have ticked upward nicely into Q1/Q2FY27 (reaching 52.1% QTD), though we must remain vigilant about the CSAT trade-offs among users who experience late escalations—a dynamic that was heavily exacerbated during the refund-delay crisis when deflected users couldn't easily reach a live agent without enduring long handle times. 

Now that the Ontario returns backlog is fully behind us, care-contact CSAT for agent-assisted and deflected paths alike are stabilizing closer to historical benchmarks (agent-assisted hovering ~4.31). 

---

### Action Items & Next Steps
1. **Archive Theme Watch:** Move `refund delay` out of active weekly executive flash alerts, returning it to standard monthly Medallia monitoring parameters.
2. **Cross-Vertical Alignment:** Share these findings with hannah.brennan and gabriel.stroud to formally close out the postmortem action items stemming from the 2026-02-02 MBR escalation.
3. **Future Voc Focus:** Direct NLP tagging resources toward emerging secondary verbatim clusters, specifically continuing to track buyer-side `listing-accuracy-gap` mentions across Style (14%), Resold (12%), Collectibles (9%), and B2B (22%) for any material change in share quarter over quarter.

---
