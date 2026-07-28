---
title: "Analyst scratch notes: H1FY27 close-out exploration ahead of the Q2FY27 MBR"
source_url: "internal://acme-ecomm/scratch/q2fy27__analyst-scratch-fy27-h1-close-notes"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: confluence_page
---

*Amara Shah (Data Analyst, Finance/MBR) — Working scratch pad.*
*Date: Monday, 2026-07-20. Prepping the numbers ahead of this morning's 2026-07-20 MBR session with Carlos and Deborah.*

---

### 0. Quick Slack Aside / Housekeeping
*   *Side note to Wei:* Did you check the Compass data export from Friday? Compass is still showing the old Q4FY26 Marketplace GMV figure ($952.4M) on the default dashboard view because someone cached the pre-restatement numbers in the regional tile. I had to manually query `marketplace_gmv_summary` in BigQuery to get the canonical $975.0M figure for the slide deck. Let's make sure Connor pushes a refresh job to clear that cache before the board sees it.
*   Also, reminder to grab lunch at the cafeteria around 1:00 PM today after the MBR wraps up. Hope the line isn't too brutal.

---

### 1. FY27 Goal-Pace Cross-Checks (Half-Finished Numbers)

Let's look at where we're tracking for H1FY27 close-out as we head into the Q2FY27 MBR. Remember Q2 is at 81/92 days (88.0% elapsed), so these are QTD paces, not closed quarters. 

*   **Total digital + marketplace GMV:** Target is $7.53B. Current run-rate (H1 +9.7% YoY, Q2 annualized) is sitting at **$7.62B**, which puts us right at **101.2%** of goal (Status: AHEAD). 
    *   *Wait, check the table notes:* Is this fully factoring in the 3P take-rate adjustments? Yes, `marketplace_gmv_summary` shows take-rate steady around 13.6%.
*   **US conversion rate (blended):** Target is 3.35%. Q2FY27 QTD is at **3.22%**, which is **96.1%** of goal (Status: BEHIND). 
    *   Remember the definition version change from back on 2026-03-02 (`sessions_definition_version` 1 → 2) when Wei pushed the bot-filtering fix. We can't compare raw pre-march session counts directly without keeping that flag in mind.
*   **US sessions (traffic):** Target 1,650M, run-rate ~1,540M (**93.3%**, BEHIND). 
    *   *Check:* This is heavily driven by that 18% paid-search budget cut felix.arroyo approved back on 2026-02-04 as part of the martech efficiency drive (`camp_98214`), *not* an organic traffic collapse. Need to make sure finance doesn't panic and treat this as a top-of-funnel emergency.
*   **Marketplace GMV:** Target $3.32B, run-rate **$3.89B** (**117.1%** of goal, AHEAD). 
    *   *Aside:* Looking closer at this 117.1% marketplace pace — it's really being carried by Resold's massive acceleration while Style decelerates. Style Q1 YoY came in at +6.1% (down from our ~10% planned trend), whereas Resold exploded +90.9% YoY over the exact same window. Resold's apparel/style-adjacent category share jumped from 51% to 62% YoY. It's not that we're losing customer demand; people are just shifting inside the marketplace from new-style catalog items to recommerce/resold alternatives. Victor Okonkwo's team hashed this out back in April (superseding that old abandoned Style Recovery Plan draft from ines.delgado that tried to shift T&S headcount around). No structural demand loss, just a wallet-share shift within our own walls.

---

### 2. Tangent: Dead Ends on US Conversion WoW Drop

Looking at the weekly breakdown for US Conversion in July:
*   Week ending 2026-07-11: Sessions 26.80M, Blended Conv 3.24%
*   Week ending 2026-07-18: Sessions 26.40M, Blended Conv 2.86%
*   That’s a week-over-week drop of **-0.38pp** (down roughly 40bps).

I tried to attribute this to the "Homepage Hero Banner Refresh" that maya.lindqvist launched on 2026-07-13, but that's a total red herring. It's homepage-only, doesn't touch item pages or search, and query logs show zero measurable conversion impact. Classic coincidental timing trap.

When you run the shift-share decomposition:
*   **Device mix effect:** ≈ -0.24pp. App session share jumped from 28.0% to 37.6% this week, and app converts structurally lower than web (1.50% vs ~3.76-4.00%). So a big chunk of the drop is just traffic moving to a lower-converting surface with zero real user behavior change.
*   **Rate effect:** ≈ -0.14pp. A genuine, modest web-conversion softening (4.00% down to 3.76%).
*   What about in-flight experiments? We've got Search Relevance Re-ranking (`exp_2601`, +1.6% exposed lift) running alongside the Item Page Media Carousel Autoplay (`exp_2618`, -1.5% exposed lift) since 2006-06-08. They basically wash each other out at a net ~+0.05%. So the roadmap and active experiments don't neatly explain the residual. Medallia verbatims for item pages in this window do mention the new autoplay video feeling "cluttered" or "annoying", but volume is low. Honestly, it's just normal week-to-week noise once you factor out the device mix shift. I'm not going to force a fake narrative into the MBR slides for this.

---

### 3. Quick Check on Other Verticals (Care & Speed)
*   **Care:** Deflection rate is at **52.1%** QTD (target 50.0%, 104.2% of goal, AHEAD). CSAT among deflected users is recovering to 3.55 after dipping down to 3.42 during the Ontario returns center staffing mess back in January (remember when the 4-week rolling refund cycle days crossed the 5.0-day SLA on 2026-01-05, and Giulia's Medallia verbatims flagged "refund delay" crossing 10% share way back in mid-December?). Glad that Ontario staffing crisis is fully behind us since hannah.brennan got the hiring-freeze exception sorted and brought headcount back to normal in February.
*   **Speed:** Blended on-time-to-promise is at **93.00%** QTD (target 93.5%, 99.5% of goal, BEHIND). But remember the mix-shift caveat: ship-to-home is actually at 89.9% (target 91.0%), while pickup (BOPIS/curbside) mix share surged to 31.0% (up from 21% last year) thanks to tara.oduya's Pickup Perks campaign. Because pickup hits ~99.6% on-time automatically, it's artificially propping up the blended rate. If you look at ship-to-home alone, we're still lagging. Also, cost per order dropped nicely down to $7.30 (from $7.85 in Q1FY26), driven in large part by the FON2 and JOL1 DC automation rollout managed by gabriel.stroud back in January/February.

---

### 4. Random To-Do Items Before the 2026-07-20 MBR
1.  Verify that no one is trying to use `acme_ecomm.marts.membership.member_cltv` in the membership slides—remind them the BigQuery dataset is flat (`acme_ecomm.member_cltv`). Inner join vs left join with COALESCE(0) will mess up the CLTV average ($625 vs $500) if someone queries the 120k representative panel incorrectly and drops the 24,000 dormant members.
2.  Double-check the seller VOC stream (`fact_seller_voc_responses`) table name. Make sure nobody accidentally blends buyer Medallia verbatims (`fact_voc_responses`) with seller pulse survey responses. Camille Duarte's new seller-listing onboarding metrics (`authentication-friction` taking up ~38% of Collectibles onboarding verbatims due to the GradeSure requirement) need to stay cleanly separated from retail shopper feedback.
3.  Grab more coffee before Carlos starts firing off questions about the US conversion gap.

---
