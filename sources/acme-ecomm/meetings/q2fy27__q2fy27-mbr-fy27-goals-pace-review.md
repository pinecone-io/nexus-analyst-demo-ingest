---
title: "MBR notes: Q2FY27 QTD business review — FY27 goals pace-to-target"
source_url: "internal://acme-ecomm/meetings/q2fy27__q2fy27-mbr-fy27-goals-pace-review"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: mbr_deck_notes
---

**Meeting:** Q2FY27 Monthly Business Review (MBR) — FY27 Goals Pace-to-Target  
**Date:** Monday, July 20, 2026 (09:00 – 12:30 ET)  
**Location:** HQ Main Conference Room (Floor 14) / Zoom Hybrid  
**Led By:** carlos.figueroa (VP Data & Analytics)  
**Attendees:** deborah.osei, felix.arroyo, hannah.brennan, victor.okonkwo, renee.kowalski, ben.tanaka, nadia.esposito, maya.lindqvist, owen.faust, sanjay.bhatt, ines.delgado, noah.kessler, camille.duarte, aisha.rahman, julian.moss, tara.oduya, leo.brandt, simone.laurent, derek.holloway, malik.hendon, wei.hartono, amara.shah, connor.blake, giulia.romano, dominic.paquet, lucia.ferreira, gabriel.stroud  

---

### 1. Administrative & Opening Remarks

**carlos.figueroa:** Good morning everyone. Let’s get started. Welcome to the Q2FY27 Monthly Business Review. As a reminder, today is July 20, 2026. We are looking at Q2FY27 QTD numbers—we have 81 of 92 days elapsed, which puts us at roughly 88.0% through the quarter. This is *not* a closed quarter review; keep that in mind as we evaluate the trajectory toward our FY27 exit goals, especially with the final 11 days of July still in front of us and August right around the corner. 

Before we dive into the deck, a quick housekeeping note from data engineering: if anyone is pulling numbers from the Compass dashboard or running ad-hoc queries, remember that our BigQuery dataset (`nexus-analyst-demo.acme_ecomm`) is entirely flat. Please stop trying to query legacy nested paths like `acme_ecomm.marts.membership.member_cltv`—that will just throw syntax errors and frustrate wei.hartono and the team. Also, please check your caching if you're looking at Marketplace historical tables; ensure you've forced a refresh so you're seeing the canonical $975.0M Q4FY26 Marketplace GMV figure rather than the stale $952.4M flash-report number that's still lingering in some local views.

**deborah.osei:** Thanks, Carlos. Let’s make sure we keep our eyes on the macro targets today. We’re in a strong position on top-line GMV and Marketplace, but some of our traffic and conversion headwinds need careful navigation as we approach Q3 and prep for the holiday build. Let's walk straight into the consolidated scorecard.

---

### 2. FY27 Goals Pace-to-Target Scorecard

amara.shah brought up the master slide summarizing our fiscal year goals against current actuals and pace. The official metrics, as reviewed by leadership today, stand as follows:

| Metric | FY27 Target | Actual / Pace | % of goal | Status |
|---|---|---|---|---|
| Total digital + marketplace GMV | $7.53B | $7.62B run-rate (H1 +9.7% YoY, Q2 annualized) | 101.2% | AHEAD |
| US conversion rate (blended) | 3.35% | 3.22% (Q2FY27 QTD) | 96.1% | BEHIND |
| US sessions (traffic) | 1,650M | ~1,540M run-rate | 93.3% | BEHIND |
| Marketplace GMV | $3.32B | $3.89B run-rate | 117.1% | AHEAD |
| Care bot deflection rate (FY27 exit) | 50.0% | 52.1% (Q2FY27 QTD) | 104.2% | AHEAD *(CSAT caveat)* |
| Speed blended on-time-to-promise (FY27 exit) | 93.5% | 93.00% (Q2FY27 QTD) | 99.5% | BEHIND *(mix-shift caveat)* |
| Speed ship-to-home on-time-to-promise | 91.0% | 89.9% (Q2FY27 QTD) | 98.8% | BEHIND |
| Acme+ members (FY27 exit, 2027-01-31) | 14.8M | 14.62M, pacing ~15.05M | 101.7% | AHEAD |
| Acme+ annual renewal rate | 86.0% | 87.2% | 101.4% | BEAT |

*For YoY reference (FY26 full-year actuals):* Conversion-channel (US+CA+MX) GMV was $3,976.6M; Marketplace GMV was $2,968.0M; bringing total FY26 actual GMV to **$6,944.6M**.

**carlos.figueroa:** Looking at the scorecard, our total digital plus marketplace run-rate is sitting at $7.62B against our $7.53B target (101.2%, putting us comfortably AHEAD), largely driven by the explosive outperformance in Marketplace, which is running at $3.89B against a $3.32B target (117.1%). However, we have two prominent amber/red flags that require deep-dive attention today: US conversion rate is at 3.22% QTD vs. our 3.35% target (96.1%, BEHIND), and US sessions are tracking at a ~1,540M run-rate against our 1,650M target (93.3%, BEHIND). 

Let's break these down vertical by vertical.

---

### 3. Vertical Deep-Dives & Discussion

#### A. US/CA/MX Conversion + Traffic (US_CONV)
*Led by maya.lindqvist & owen.faust*

**maya.lindqvist:** Let's address the session and conversion numbers. First, as a reminder when doing YoY comparisons against Q1FY26 or earlier, we implemented the session-counting fix back on March 2, 2026 (`sessions_definition_version` 1 to 2) with bot/crawler filtering and multi-tab de-duplication. That mechanically raised our measured conversion rate because the denominator got smaller while orders remained constant. `traffic_conversion_summary` carries that flag forward, so please don't compare raw session volumes across March 2 without factoring that in.

That said, the primary real-world driver of Q1FY27's US session decline (-5.6% YoY) is not a demand collapse; it's the 18% paid-search budget cut that felix.arroyo approved and initiated back on February 4 as a deliberate marketing-efficiency initiative (`camp_98214`). We traded away low-intent search volume to protect efficiency, and that's exactly what happened.

**owen.faust:** On the conversion side, we've been tracking our weekly wobbles closely. If you look at the Q2FY27 weekly US conversion numbers for the last two reporting weeks:
* Week ending 2026-07-11: 26.80M sessions, 3.24% blended conv. (868,320 orders)
* Week ending 2026-07-18: 26.40M sessions, 2.86% blended conv. (755,038 orders)

That's a week-over-week drop of roughly 38bps (3.24% down to 2.86%). When we run the shift-share decomposition on that move, roughly -0.24pp of it is purely device-mix shift—app session share jumped from 28.0% to 37.6%, and app converts structurally lower than web in our current funnel. A mix shift with zero underlying behavioral change accounts for the lion's share of that drop. The remaining -0.14pp is a modest, genuine web-conversion softening (web conversion dropped from 4.00% to 3.76%). 

Now, some folks looked at the calendar and noticed we launched the "Homepage Hero Banner Refresh" on July 13 under my team's watch, and wondered if that broke something. We've audited the query logs and FullStory sessions: it's homepage-only, has zero item-page or search overlap, and has no measurable conversion effect. It's a distractor. 

Instead, look at our in-flight experiments. We have two experiments running right now that started on June 8: "Search Relevance Re-ranking" (`exp_2601`, showing a +1.6% conversion lift on its exposed arm) and "Item Page Media Carousel Autoplay" (`exp_2618`, showing a -1.5% drop on its exposed arm). The autoplay media module was well-intentioned, but Medallia verbatims and session notes show shoppers finding the auto-starting video cluttered and annoying, making pages feel sluggish. Net-weighted, these two experiments wash out at roughly +0.05%, which masks the fact that one is actively dragging down our item pages while the other props up search. Maya's team is looking at pausing the autoplay module before the end of the quarter.

**deborah.osei:** Let's make sure we don't leave negative customer friction points live just because they net out to zero in aggregate. If `exp_2618` is dragging down item page sentiment, let's pull the plug or iterate. What about the checkout side, Owen? Did our Checkout Simplify rollout hold up?

**owen.faust:** Checkout Simplify (`exp_2214`, ran Feb 16 to Mar 30) shipped to 100% on April 6. Just a reminder for the audit trail: its full-window readout showed a +2.1% lift, but that was confounded because Nav Refresh launched into both experiment arms on March 1. The clean pre-confound slice from February 16-28 showed a solid +0.8% independent lift. So the checkout win is real, even if the headline number had some noise attached.

---

#### B. Marketplace (MARKETPLACE)
*Led by victor.okonkwo, lucia.ferreira, sanjay.bhatt, ines.delgado, noah.kessler, & camille.duarte*

**victor.okonkwo:** Marketplace is continuing its stellar run. We are pacing at $3.89B run-rate against our $3.32B target (117.1% of goal). Let's look at the sub-vertical GMV breakdown for Q2FY27 QTD:
* **Style:** $444.1M (Q1FY27 was $543.0M; Q1 YoY was +6.1%)
* **Resold:** $143.1M (Q1FY27 was $168.0M; Q1 YoY was +90.9%)
* **Collectibles:** $91.2M (Q1FY27 was $104.0M; Q1 YoY was +372.7%)
* **Total Q2 QTD:** $678.4M ($815.0M in Q1FY27)

**deborah.osei:** Style's growth rate has moderated significantly compared to Resold and Collectibles. Is there a structural issue in Style, or is something else happening?

**victor.okonkwo:** It’s a portfolio shift, Deborah. Remember back in Q1 when we looked at the abandoned "Style Conversion Recovery Plan" draft from Confluence? At the time, people were panicking that Style was losing steam and suggested shifting Trust & Safety headcount away from Collectibles to fix Style. We looked at the data and realized through our Confluence synthesis in April that it wasn't a demand loss at all—it’s a within-marketplace wallet-share shift. Resold's apparel and style-adjacent category share jumped from 51% to 62% YoY. Shoppers are migrating toward vintage and recommerce options within our own ecosystem. No headcount reallocations were needed, and Style is still growing, just at a tamer +6.1% clip while Resold surges at +90.9%.

**lucia.ferreira:** On the Collectibles side, our return rate tells an incredible story about the "Acme Verified" authentication program (GradeSure partnership, launched Sep 8, 2005, badge on 100% of listings since Nov 20, 2005). Back during the Q3FY26 counterfeit spike, Collectibles return rates hit 10.2%–11.2%. For Q2FY27 QTD, that return rate has dropped down to **5.4%**. Buyer trust is through the roof.

However, camille.duarte and I have been looking closely at the seller-side onboarding funnel using our new `fact_seller_voc_responses` stream ("Seller Pulse" survey program launched April 20, 2026). There is a stark two-sided tension here. Look at our new-seller cohort (~500 sellers onboarded Q3–Q4FY26 with enough runway to today):
* **Style (n=150):** 100% reach listing 1, 76% reach listing 5, 48% reach listing 10, 42% sustained.
* **Resold (n=150):** 100% reach listing 1, 74% reach listing 5, 46% reach listing 10, 40% sustained.
* **Collectibles (n=200):** 100% reach listing 1, 46% reach listing 5, **24% reach listing 10**, 19% sustained.

Collectibles new sellers are hitting a wall early. Nearly half drop out before listing 5. Why? Because of `authentication-friction`. GradeSure authentication protects buyers and keeps return rates at 5.4%, but for a brand-new seller trying to list their first cards, the per-item time, fee, and latency hurdles are brutal. In our Seller Pulse survey data, `authentication-friction` is the dominant theme at ~38% of verbatims for Collectibles onboarding respondents. 

Furthermore, if you slice the Collectibles new-seller cohort by whether their debut listing was verified within 7 days: the 60% who got verified quickly reach listing 10 at a 30% rate; the 40% who faced delays drop to a 15% rate (half as likely to survive). 

**camille.duarte:** Exactly, Lucia. In addition to authentication friction, our Seller Pulse data highlights two other category-agnostic themes: `listing-setup-complexity` (~15–20% across all sub-verticals, hitting hardest between listing 1 and 5 due to lack of bulk upload tooling) and `no-performance-visibility` (~12–18%, concentrated between listing 5 and 10 where sellers can't diagnose why an established listing isn't converting). 

**victor.okonkwo:** We aren't going to scrap Acme Verified—protecting the $91.2M Collectibles quarterly run-rate from counterfeit contamination is non-negotiable. But we do need to look at onboarding support and perhaps faster verification queues for promising new sellers so we don't bleed them before listing 10.

---

#### C. Customer Care (CARE)
*Led by hannah.brennan, dominic.paquet, aisha.rahman, & giulia.romano*

**hannah.brennan:** Let's look at Care and Post-Order Returns. Our Q2FY27 QTD Care deflection rate is sitting at **52.1%**, beating our 50.0% target (104.2%, AHEAD). Contact volume is pacing at 1,180K for the quarter, down from historical peaks as our automation takes hold. 

However, we must read the deflection rate alongside our quality caveats. Back during the peak holiday crunch in December, Medallia "refund delay" verbatims crossed 10% on December 15, 2025, while our quantitative 4-week rolling `avg_refund_cycle_days` crossed the 5.0-day SLA alert threshold on January 5, 2026 (hitting 5.03 days). As we know from our post-mortems, the root cause was the Ontario, CA returns-processing center (`node_type='returns_center'`) running 22% understaffed due to a hiring-freeze exception error. We formally escalated that at the February 2 MBR, surged temp labor, restored staffing by February 20, and brought refund cycles back down to our ~3.3-day baseline by mid-March. 

That operational hiccup directly tanked our deflected CSAT down to 3.42 in Q1, though it has partially rebounded to **3.55** this quarter (agent-assisted CSAT remains steady and healthy at 4.31). So our rising deflection is real progress driven by "Ask Acme v2" (launched September 15, 2005) and Aisha's recent bot handoff experiments, but it was temporarily masked and bruised by an offline operational failure.

**aisha.rahman:** On the deflection front, our "Bot Handoff Threshold" experiment (`exp_2489`, ran April 1 to May 15) tested relaxed bot handoff triggers. It yielded a clean **+3pp deflection lift**, with a minor -0.15 CSAT dip among late-escalated users. On May 20, we partially shipped that capability for non-billing categories only, holding back billing-related contacts because we know those users have extreme CSAT sensitivity. That's why our deflection has climbed cleanly to 52.1% this quarter without torching our customer satisfaction scores.

---

#### D. Speed & Fulfillment (SPEED)
*Led by tara.oduya, gabriel.stroud, & leo.brandt*

**tara.oduya:** Speed and fulfillment is tracking an overall blended on-time-to-promise (OTP) of **93.00%** Q2FY27 QTD against our 93.5% target (99.5%, BEHIND). Ship-to-home OTP is at **89.9%** against a 91.0% target (98.8%, BEHIND). 

Before everyone panics about the blended OTP being slightly behind target, let's look at the mix-shift dynamics. If you examine our fulfillment channel mix for Q2FY27 QTD:
* **Ship-to-home:** 66.8% mix (down from 77.5% in Q1FY26)
* **Pickup (BOPIS + curbside):** 31.0% mix (up from 21.0% in Q1FY26)
* **DFS (Delivery From Store):** 2.2% mix (up from 1.5% in Q1FY26)

Pickup on-time rates are virtually flawless at **99.6%**, driven in large part by the Pickup Perks BOPIS/curbside discount campaign that tara.oduya's team launched back on January 15. Because pickup mix has surged by 8 full percentage points since last year, it heavily buoys our blended OTP. Meanwhile, ship-to-home—our hardest, most complex channel—actually sits at 89.9%. Our blended OTP rose +0.73pp year-over-year while ship-to-home dropped -0.20pp over the same window. The blended gain is entirely mix-shift, not a magical fix in line-haul transit times.

**gabriel.stroud:** On the cost side, our DC automation Phase 1 rollout at FON2 (Fontana) and JOL1 (Joliet) back in January-February 2026 has delivered a durable efficiency gain. Our cost per order has dropped from a peak of $8.60 during Q4 holiday strain down to **$7.30** in Q2 QTD. Part of that drop is post-holiday reversion from Q4's winter-storm and peak labor spike at JOL1, but the automated sortation lines are performing exactly as modeled and saving us real margin on every parcel.

As for Leo's "Wider Promise Window" experiment (`exp_1187`, Jan 12 to Feb 20), we killed it on March 2. While it showed a +4.2pp OTP bump on paper, it was heavily confounded by the DC automation rollout happening at the same time. Once deconfounded, the isolated promise-window widening only gave us +1.5pp OTP, but it introduced a -0.6% conversion penalty because shoppers didn't like seeing longer delivery estimates. Net-negative; dead and buried.

---

#### E. Membership — Acme+ (MEMBERSHIP)
*Led by renee.kowalski, simone.laurent, & derek.holloway*

**renee.kowalski:** Acme+ is having an exceptional quarter. Our active true membership base stands at **14.62M** at Q2 QTD, pacing nicely toward our year-end exit target of 14.8M (and tracking toward ~15.05M organic finish). Net adds are at 270K this quarter, and our annual renewal rate is hitting **87.2%** against an 86.0% target (101.4%, BEAT).

**derek.holloway:** A quick technical note for anyone querying member lifetime value (`member_cltv`): remember to use the canonical build that **LEFT JOINs `dim_member` to `fact_orders` with `COALESCE(trailing_12mo_gmv_usd, 0)`**. If someone writes an INNER JOIN by mistake, it silently drops the 20% of our 120,000-member panel (24,000 members) who have zero orders in the trailing 12 months—members who are dormant but still paying their annual renewal fee. An inner join falsely jacks up average CLTV from the correct **$500/member** to a wrong **$625/member** (a 25% overstatement) and sweeps our churn-risk dormant base right under the rug.

On the benefit side, our "Benefit Onboarding Carousel" experiment (`exp_2556`, May 1 to June 15) wrapped up with a fantastic **+9pp lift in 30-day benefit awareness**. We know from our member data that benefit adoption drives retention: members using 2+ benefits renew at **95%**, compared to 71% for free-shipping-only members. 

Our streaming bundle is our single strongest retention driver—members using it renew at **93%** even on its own. But here's the kicker: only **34%** of our members even know they have access to it. As you recall, we successfully switched our streaming partner vendor from Vidora to Reelstream on June 1, 2026. Since Reelstream is fresh, our highest-leverage CLTV lever right now isn't inventing a brand-new benefit; it's simply making sure the other 66% of our members know what they're already paying for. (And for the record, our proposed "Customer Lifetime Health Score" or CLHS remains firmly parked as a draft spec with no production table, so please don't cite a CLHS score in any formal reports).

---

### 4. Cross-Vertical Signals & Action Items

**carlos.figueroa:** Before we wrap up, nadia.esposito wanted to flag something from the Medallia side that's been on her radar.

**nadia.esposito:** Right. Buyer-side Medallia is showing a `listing-accuracy-gap` theme (listings' photos and descriptions not matching true scale, condition, or specification) at a stubborn, non-trivial share in all four of our retail verticals — **Style at 14%**, **Resold at 12%**, **Collectibles at 9%**, and **B2B at 22%** (where bulk-order buyers deal with spec-sheet and pallet-configuration mismatches). It's been steady for a couple of quarters, not trending, but the fact that it turns up in all four caught my eye. I haven't had a chance to line it up against each vertical's current backlog yet.

**deborah.osei:** Worth running that down properly rather than guessing in this meeting. Put it on the list for Q3 planning and have each vertical PM check their own board against it. 

---

### 5. Action Items & Decisions Log

1. **US_CONV (maya.lindqvist):** Evaluate immediate pause or iteration of the "Item Page Media Carousel Autoplay" experiment (`exp_2618`) due to shopper friction verbatims, neutralizing its -1.5% drag on item pages. *(Due: 2026-07-25)*
2. **Marketplace (camille.duarte & victor.okonkwo):** Draft onboarding support recommendations and faster verification routing for high-potential Collectibles new sellers to improve survival past listing 10 without compromising the 5.4% return-rate win achieved via Acme Verified. *(Due: 2026-08-10)*
3. **Membership (derek.holloway & renee.kowalski):** Design a targeted Reelstream streaming benefit awareness campaign targeting the 66% un-engaged member segment ahead of the Q3 member renewal cycle. *(Due: 2026-08-01)*
4. **Product Ops (nadia.esposito):** Check whether the recurring `listing-accuracy-gap` VOC theme (Style 14%, Resold 12%, Collectibles 9%, B2B 22%) is already covered by anything on the four verticals' current boards, and report back ahead of Q3 planning. *(Due: 2026-08-15)*
5. **Data & Analytics (wei.hartono):** Validate that all MBR deck builders are referencing flat BigQuery dataset paths (`nexus-analyst-demo.acme_ecomm.<table>`) and utilizing the canonical `member_cltv` LEFT JOIN pattern with `COALESCE(0)`. *(Done / Ongoing)*

---
