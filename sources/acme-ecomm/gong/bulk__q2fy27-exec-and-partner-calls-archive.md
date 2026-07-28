---
title: "Gong call archive: exec and partner calls, full corpus history (2025-2026)"
source_url: "internal://acme-ecomm/gong/bulk__q2fy27-exec-and-partner-calls-archive"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: gong_call
---

# Gong Enterprise Call Recording Archive — Full Corpus History (2025-2026)
**Export Parameters:** All recorded executive syncs, leadership staff meetings, MBR-prep sessions, and vendor/partner integrations across Q1FY26 through Q2FY27 QTD. 
**Corpus Span:** 2025-02-01 to 2026-07-20.
**Total Transcripts Indexed:** 18 calls.

---

## Transcript 1: Executive Staff & MBR Prep Sync (Q1FY26 Kickoff)
* **Date:** 2025-04-15
* **Participants:** deborah.osei, felix.arroyo, carlos.figueroa, hannah.brennan, victor.okonkwo, renee.kowalski, ben.tanaka
* **System Tag:** internal_exec_sync

**[00:02:15] deborah.osei:** Morning everyone. Let's make sure we're aligned on the Q1 numbers before the board deck locks tomorrow. Carlos, are the BigQuery base logs clean after the audit we started back in February?
**[00:02:48] carlos.figueroa:** Morning, Deborah. Yes, base logs in `acme_ecomm.fact_traffic_daily` are holding steady. We've got the full population grain across US, CA, and MX. Conversion-channel GMV for Q1FY26 closed at $754.6M for the US conversion side, total conversion GMV across markets is matching our model. 
**[00:03:30] felix.arroyo:** Quick audio check on my end—can you hear me? Great. Just wanted to note that traffic in US conversion is looking solid, though we're watching session growth in MX closely since it runs a few points behind CA as usual. That structural gap has been persistent for four quarters now.
**[00:04:12] renee.kowalski:** On the membership side, Acme+ true base just cleared 12.60M at the end of April. Annual renewal rate is holding at 86.2%. The Vidora streaming bundle integration we're prepping for June 1st is going to give us a nice retention lift if we can get members to actually activate it. Right now, awareness is our biggest bottleneck.
**[00:05:01] victor.okonkwo:** Marketplace is humming. Style GMV came in at $512.0M for Q1, total marketplace was $622.0M. Sellers on the panel are active. We're keeping an eye on listing quality across the board.
**[00:05:45] hannah.brennan:** Care contacts for Q1 are at 2,150K. Deflection is sitting at 37.2%. CSAT on deflected contacts is 3.90, agent-assisted is 4.30. We're scoping out the Ask Acme v2 bot rollout for Q3 to push that deflection past 45%.
**[00:06:20] ben.tanaka:** Fulfillment side, blended on-time is 91.65%, ship-to-home is 89.5%. Cost per order is $7.85. Everything is stable heading into Q2.

---

## Transcript 2: Vendor Alignment Call — GradeSure Authentication rollout
* **Date:** 2025-08-18
* **Participants:** lucia.ferreira, sanjay.bhatt, connor.blake, [External GradeSure Account Director - Mark Vance]
* **System Tag:** vendor_partner_sync

**[00:00:40] lucia.ferreira:** Thanks for jumping on, Mark. Since the counterfeit spike we hit back on August 4th with that viral vintage card auction, we need to make sure the GradeSure API integration for "Acme Verified" is airtight before our September 8th launch date.
**[00:01:15] Mark Vance (GradeSure):** Understood, Lucia. Our engineering team is pushing the webhook staging updates by Friday. The main thing is managing seller intake volume in Collectibles. Sellers like sel_500012 (Timeworn Treasures) are going to breeze through, but smaller new sellers might hit latency friction on item authentication.
**[00:02:02] sanjay.bhatt:** That friction is what I'm worried about for our upcoming experiment (`exp_2401`) on badge prominence. If verification takes more than 48 hours, new sellers in Collectibles are going to drop off before reaching listing 10. We need the turnaround time under 24 hours for initial item onboarding.
**[00:02:45] connor.blake:** From the data engineering side, I'll make sure `fact_marketplace_listings` and `dim_seller` tables correctly capture the `authenticity_verified` boolean flag so we can track the post-launch return rate drop. We saw Collectibles returns hit 11.2% during the peak of the counterfeit issue; we need that back down to single digits.
**[00:03:30] lucia.ferreira:** Perfect. Let's sync next Tuesday after the staging environment goes live.

---

## Transcript 3: Q3FY26 Board-Prep & Strategy Sync
* **Date:** 2025-10-15
* **Participants:** deborah.osei, felix.arroyo, carlos.figueroa, simone.laurent, gabriel.stroud, nadia.esposito
* **System Tag:** internal_exec_sync

**[00:01:10] deborah.osei:** Team, the Q3 board deck is shaping up nicely, but I want to dig into the membership numbers and fulfillment speed as we prep for the Q4 peak. Simone, how did the Fall Savings promo (`camp_90214`) perform?
**[00:01:45] simone.laurent:** It wrapped today, Deborah. Net adds for Q3 jumped to 450K, pushing the true base to 13.35M members. Annual renewal rate climbed to 86.7%. Members who came in through the promo are showing strong early adoption of free shipping and early access benefits.
**[00:02:30] carlos.figueroa:** Just a quick housekeeping note on data architecture—Nadia's team is helping us corral the old Aitable roadmap cards into Jira as part of the consolidation project we kicked off. Let's make sure nobody is referencing legacy Aitable links for Q4 feature commitments.
**[00:03:15] gabriel.stroud:** On the fulfillment front, ship-to-home on-time is holding at 90.1% for Q3. Cost per order dropped slightly to $7.70. We're fully staffed for peak in November, and the FON2 and JOL1 sortation automation upgrades are scheduled to kick off in January once the holiday dust settles.
**[00:04:02] felix.arroyo:** Excellent. Let's make sure the marketing calendar syncs cleanly with Maya's conversion push for Black Friday week starting November 28th.

---

## Transcript 4: Care & VOC Emergency Escalation Sync (Refund Delay Crisis)
* **Date:** 2026-01-08
* **Participants:** hannah.brennan, giulia.romano, dominic.paquet, gabriel.stroud, amara.shah
* **System Tag:** internal_exec_sync

**[00:00:20] hannah.brennan:** Thanks everyone. We have a serious operational disconnect that leadership needs to address immediately. Giulia, walk us through what Medallia picked up in December.
**[00:00:55] giulia.romano:** Right. Back on December 15th, the Medallia verbatim theme for "refund delay" crossed the 10% share threshold, hitting 11.2%. By the first week of January—specifically the week of January 5th—our quantitative 4-week-rolling `avg_refund_cycle_days` crossed the 5.0-day SLA alert threshold, landing at 5.03 days.
**[00:01:45] hannah.brennan:** And why didn't we catch this in November? Gabriel, what's happening at the Ontario, CA returns center (`node_id` returns center)?
**[00:02:10] gabriel.stroud:** Hannah, it's an understaffing issue. The facility ran roughly 22% understaffed through peak because an HR hiring-freeze exception we requested for returns processing didn't get pushed through correctly. With the post-Black Friday overflow and the JOL1 winter storm disruption on December 8th compounding things, our dock staging congestion backed up hard.
**[00:03:00] dominic.paquet:** Care contact volume is surging because customers are furious about delayed refunds on returned items. Even with Ask Acme v2 handling 45% deflection, agent-assisted CSAT is taking a hit on order-status inquiries.
**[00:03:50] hannah.brennan:** We are formally escalating this to the MBR on February 2nd. Gabriel, I need emergency overtime and cross-hub temp worker surge authorized for Ontario immediately to clear that backlog before the end of January.

---

## Transcript 5: Speed & Fulfillment Vendor Check-in (FON2/JOL1 Automation Hardware)
* **Date:** 2026-01-14
* **Participants:** gabriel.stroud, leo.brandt, tara.oduya, [External Conveyor & Sortation Tech Vendor - Dave Rucker]
* **System Tag:** vendor_partner_sync

**[00:00:30] tara.oduya:** Dave, let's talk about the Phase 1 sortation automation rollout at FON2 in Fontana and JOL1 in Joliet. We started on January 12th. How are the optical sorter retrofits tracking against schedule?
**[00:01:05] Dave Rucker (Vendor):** Going smoothly, Tara. The mechanical install on the primary line at FON2 is complete. JOL1 is tracking about 48 hours behind due to that minor subfloor cabling issue, but our night shift caught up. You'll have full automated divert capabilities across both nodes by February 15th as planned.
**[00:01:50] leo.brandt:** That timing overlaps directly with our "Wider Promise Window" experiment (`exp_1187`) in the US market. I need to make sure sortation throughput isn't adding noise to our on-time-to-promise readouts while we widen delivery estimates.
**[00:02:35] gabriel.stroud:** Don't worry, Leo, the automation is happening downstream of pick paths, so it shouldn't taint your experiment exposure data. In fact, this is the exact hardware upgrade that's going to drive our cost-per-order down toward $7.30 over the next two quarters. Just keep us posted on when you pull the plug or ship the experiment.

---

## Transcript 6: Q4FY26 Peak-Readiness & Post-Mortem Prep Sync
* **Date:** 2026-01-20
* **Participants:** deborah.osei, felix.arroyo, carlos.figueroa, maya.lindqvist, owen.faust, hannah.brennan
* **System Tag:** internal_exec_sync

**[00:01:15] deborah.osei:** Q4 closed out with massive numbers—total conversion GMV for the quarter hit $1,590.9M, and Marketplace brought in $975.0M (after that minor returns-timing reclass from the flash $952.4M report). Maya, how did the holiday traffic perform on the US conversion side?
**[00:01:55] maya.lindqvist:** US sessions hit 598.0M in Q4, Deborah, with a conversion rate of 3.92% during the peak weeks. Black Friday week was a massive surge. Our item page iterations are paying off, but we need to keep pushing on checkout friction.
**[00:02:40] owen.faust:** That's why we're teeing up the "Checkout Simplify" experiment (`exp_2214`) for February 16th. We want to streamline the payment steps and reduce cart abandonment before spring traffic ramps up.
**[00:03:20] carlos.figueroa:** Team, remember that Wei Hartono is prepping the BigQuery session-definition update for March 2nd (`sessions_definition_version` 1 to 2) to filter out bots and multi-tab duplication. That means our conversion rates are going to look mechanically higher post-cutover due to the smaller session denominator, so don't panic when the numbers shift week-over-week.

---

## Transcript 7: Growth Marketing Efficiency & Paid-Search Cut Alignment
* **Date:** 2026-02-03
* **Participants:** felix.arroyo, carlos.figueroa, amara.shah, [External Agency Partner - Sarah Jenkins]
* **System Tag:** internal_exec_sync

**[00:00:45] felix.arroyo:** Let's review the marketing efficiency initiative starting tomorrow, February 4th. We're cutting paid-search spend by 18% (`camp_98214`). Carlos, how are we modeling the expected session drop in US conversion?
**[00:01:25] carlos.figueroa:** Felix, based on our attribution models in BigQuery, cutting paid search by 18% is going to pull our US session volume down by roughly 5.6% YoY for Q1FY27. Sessions will drop from about 402M in Q1FY26 down to 379.5M. 
**[00:02:10] amara.shah:** Right, and leadership needs to keep in mind that this is a deliberate efficiency move, not an organic demand failure or competitive loss. Our blended conversion rate will actually look higher because low-intent paid-search traffic is leaving the denominator.
**[00:02:55] Sarah Jenkins (Agency):** We've optimized the remaining 82% of keyword bids to focus on high-intent transactional terms, so ROAS should actually improve even as top-of-funnel traffic contracts. We'll monitor daily in `fact_traffic_daily`.

---

## Transcript 8: Product & Engineering Sync — Nav Refresh & Checkout Confounders
* **Date:** 2026-03-02
* **Participants:** maya.lindqvist, owen.faust, wei.hartono, nadia.esposito
* **System Tag:** internal_exec_sync

**[00:00:30] maya.lindqvist:** Morning everyone. Yesterday on March 1st, we launched the "Nav Refresh" sitewide redesign (`exp_2215` holdback), and right on cue, Wei rolled out `sessions_definition_version` 2 in BigQuery today to filter out those stubborn crawlers. 
**[00:01:10] owen.faust:** Which brings up a messy experimental overlap. Since Nav Refresh launched into *both* arms of my active "Checkout Simplify" experiment (`exp_2214`), our checkout readout is officially confounded. The full-window read is showing +2.1% conversion lift, but that includes Nav Refresh's independent lift.
**[00:01:55] wei.hartono:** That's correct, Owen. If you want the clean pre-confound slice for Checkout Simplify, you have to isolate February 16th through February 28th before Nav Refresh dropped and recompute the lift on just that window — I haven't pulled that cut yet. 
**[00:02:40] nadia.esposito:** And remember to log all of this in Jira per our consolidation project. Don't leave notes in old Aitable cards. Also, Maya, how are the Item Page iterations going? V3 (image gallery zoom/swipe) dropped on March 5th, right on top of the new session definition version.
**[00:03:25] maya.lindqvist:** Yes, view-to-cart rate jumped to 19.9% post-cutover from 18.0% pre-cutover. Some of that's Wei's mechanical bot-filtering bump and some is real engagement from our v3 through v6 feature releases — we're documenting the pre/post-cutover baselines in the Confluence PRD so whoever needs the split can work it out.

---

## Transcript 9: Marketplace Category Mix & Resold Acceleration Review
* **Date:** 2026-04-10
* **Participants:** victor.okonkwo, ines.delgado, noah.kessler, sanjay.bhatt, camille.duarte
* **System Tag:** internal_exec_sync

**[00:00:40] victor.okonkwo:** Team, let's look at the Q1FY27 Marketplace numbers that just locked. Total Marketplace GMV came in at $815.0M. Style grew at +6.1% YoY to $543.0M, which initially looked like a deceleration compared to our 10% plan. We're holding off on Ines's old draft "Style Conversion Recovery Plan" from March pending a fuller review — we shouldn't shift T&S headcount off Collectibles on the Style number alone.
**[00:01:30] noah.kessler:** Agreed, Victor. Resold accelerated by +90.9% YoY to reach $168.0M, and Resold's apparel/style-adjacent category share jumped from 51% to 62% YoY over the same window. Worth putting those two side by side before anyone calls Style's number a demand problem.
**[00:02:15] sanjay.bhatt:** Meanwhile, Collectibles hit $104.0M—up 372.7% YoY—and thanks to the GradeSure "Acme Verified" program, our return rate in Collectibles dropped all the way from the Q3 peak of 11.2% down to 5.4% in Q2FY27. 
**[00:03:00] camille.duarte:** But we have a seller-side bottleneck, team. Since launching the "Seller Pulse" survey program on April 20th (`fact_seller_voc_responses`), our onboarding funnel data shows that new Collectibles sellers are stalling out. Only 24% reach listing 10, compared to 48% in Style and 46% in Resold. 
**[00:03:50] victor.okonkwo:** Because authentication friction with GradeSure is brutal for newcomers. If they don't get verified within 7 days, their survival rate drops by half. Camille, let's work with Lucia to see where we can streamline seller onboarding without compromising buyer trust.

---

## Transcript 10: Care & Deflection Strategy Review (Bot Handoff Thresholds)
* **Date:** 2026-05-18
* **Participants:** hannah.brennan, aisha.rahman, julian.moss, dominic.paquet, giulia.romano
* **System Tag:** internal_exec_sync

**[00:00:30] hannah.brennan:** Let's review the results of the "Bot Handoff Threshold" experiment (`exp_2489`) that ran from April 1st to May 15th. Aisha, what did we see on deflection and CSAT?
**[00:01:05] aisha.rahman:** Deflection rose by +3 percentage points, Hannah, pushing our Q2 pace up toward 52.1%. However, we saw a -0.15 drop in CSAT among users who were subjected to late-stage bot escalation before reaching a human agent. 
**[00:01:50] julian.moss:** That CSAT hit was concentrated entirely in billing-related inquiries where customers were already frustrated. Non-billing categories handled the looser bot handoff without any noticeable satisfaction dip.
**[00:02:35] dominic.paquet:** So our partial shipping decision on May 20th was the right call: we rolled out the relaxed handoff thresholds for non-billing categories only, protecting our billing escalation path while still capturing the deflection gains.
**[00:03:20] giulia.romano:** Medallia post-care survey data confirms that customers are responding well to the refined routing. Our overall care contact volume for Q2 QTD is sitting at 1,180K, with deflected CSAT recovering to 3.55.

---

## Transcript 11: Membership & Streaming Partner Migration Sync (Vidora to Reelstream)
* **Date:** 2026-06-04
* **Participants:** renee.kowalski, derek.holloway, simone.laurent, [External Reelstream VP Partnerships - Brad Sterling]
* **System Tag:** partner_vendor_sync

**[00:00:30] renee.kowalski:** Brad, welcome aboard. Now that we've officially switched our Acme+ streaming perk partner from Vidora over to Reelstream as of June 1st, how is server stability holding up across our member base?
**[00:01:05] Brad Sterling (Reelstream):** Flawless execution on our end, Renee. CDN handoffs are clean, and we haven't seen a single latency spike since cutover. 
**[00:01:45] derek.holloway:** The timing aligns perfectly with the conclusion of our "Benefit Onboarding Carousel" experiment (`exp_2556`) on June 15th, which drove a +9pp lift in 30-day benefit awareness. But remember, only about 34% of members actually know they have the streaming perk in the first place.
**[00:02:30] simone.laurent:** That renewal-by-benefit-depth gradient is worth keeping in front of us regardless — members who use 2+ benefits renew at 95%, compared to 71% for free-shipping-only members. Whether a targeted Reelstream awareness campaign is the best next move against that gradient versus our other options is worth a proper look before we commit budget.
**[00:03:15] renee.kowalski:** Let's draft the campaign brief for July. Derek, make sure you coordinate with Amara on pulling the cohort retention numbers once the 12-month lag matures.

---

## Transcript 12: Q2FY27 Mid-Quarter Growth & Experimentation Review
* **Date:** 2026-06-15
* **Participants:** felix.arroyo, maya.lindqvist, owen.faust, carlos.figueroa, amara.shah
* **System Tag:** internal_exec_sync

**[00:00:45] felix.arroyo:** Let's look at where we stand with two weeks left in Q2. US conversion for Q2FY27 QTD is averaging 3.22%, with sessions pacing around 308M for US. But I want to examine what's happening with our active experiments right now.
**[00:01:30] maya.lindqvist:** We've got two major US conversion experiments running concurrently since June 8th. "Search Relevance Re-ranking" (`exp_2601`) is showing a healthy +1.6% conversion lift on its exposed arm.
**[00:02:15] owen.faust:** And separately, my "Item Page Media Carousel Autoplay" experiment (`exp_2618`) is showing a -1.5% drop on its exposed arm. The autoplay video module is feeling cluttered to shoppers and slowing down the page perceptually.
**[00:03:00] carlos.figueroa:** Worth keeping both of those individual reads in front of leadership rather than just a net experiment line — wouldn't want anyone to check that line, see something small, and assume nothing's moving.
**[00:03:45] amara.shah:** Right. And separately, our weekly WoW drop during the week of July 18th (dropping from 3.24% down to 2.86%) — app session share jumped from 28.0% to 37.6% that week, and app converts lower than web, so there's a mix component in there. Neither the homepage banner refresh on July 13th nor our active experiments look like the roadmap explanation for it, but the full mix/rate split still needs to be run.

---

## Transcript 13: Cross-Vertical VOC Signal Check-In
* **Date:** 2026-07-14
* **Participants:** nadia.esposito, camille.duarte, malik.hendon, ines.delgado, noah.kessler
* **System Tag:** internal_exec_sync

**[00:00:30] nadia.esposito:** Thanks for jumping on this ad-hoc sync, team. I was skimming the Medallia dashboards this week and noticed a `listing-accuracy-gap` theme — buyers complaining that item photos or descriptions don't match true scale, condition, or spec — showing up in each of your verticals' reports at a non-trivial share. Wanted to flag it before Q3 planning rather than let it sit in a dashboard nobody's looking at cross-functionally.
**[00:01:20] camille.duarte:** Good flag. In my seller-experience view it's been steady for a couple of quarters, not a new spike, so it hasn't tripped anyone's alert threshold on its own.
**[00:02:05] malik.hendon:** Same on the B2B side — bulk buyers hitting spec-sheet and pallet-config mismatches. It's on my radar but I haven't cross-checked it against what Style, Resold, or Collectibles are doing.
**[00:02:50] ines.delgado:** I'd want to actually pull my current board before saying anything definitive about whether it's covered — don't want to guess on a call and get it wrong in front of Victor and Felix.
**[00:03:35] nadia.esposito:** Fair. Let's each take a look at our own backlog independently and reconvene before Q3 planning locks. No point speculating without the boards in front of us.

---

## Transcript 14: Q2FY27 Executive MBR-Prep & Final Pace Review
* **Date:** 2026-07-19
* **Participants:** deborah.osei, felix.arroyo, carlos.figueroa, hannah.brennan, victor.okonkwo, renee.kowalski, ben.tanaka
* **System Tag:** internal_exec_sync

**[00:01:00] deborah.osei:** Tomorrow is our Q2FY27 MBR, and I want our narrative locked in. Overall digital and marketplace GMV run-rate is pacing at $7.62B, well ahead of our $7.53B full-year target (+9.7% YoY H1). Marketplace is the absolute standout, pacing at $3.89B run-rate against its $3.32B goal (117.1%).
**[00:01:50] felix.arroyo:** US conversion rate QTD is 3.22%, sitting slightly behind our 3.35% target (96.1%), but session volume reflects our deliberate paid-search cut efficiency strategy from February. Traffic is stabilizing as our app mix grows.
**[00:02:35] victor.okonkwo:** Marketplace is firing on all cylinders. Even with the Style/Resold wallet-shift dynamics and the GradeSure authentication friction in Collectibles, total marketplace GMV is outperforming expectations, and return rates in Collectibles are down to a healthy 5.4%.
**[00:03:20] hannah.brennan:** Care deflection is exceeding targets at 52.1% (vs 50% FY27 exit goal), and our average handle time is down to 7.4 minutes. The Ontario returns center operational crisis from winter is fully behind us, and refund cycles are back to normal baseline (~3.3 days).
**[00:04:05] renee.kowalski:** Membership is right on track. Acme+ true base has reached 14.62M members, pacing toward our 14.8M exit target, and annual renewal rates have beaten target at 87.2%. The Reelstream streaming migration is smooth.
**[00:04:50] ben.tanaka:** Speed and fulfillment blended on-time is at 93.00% QTD; pickup mix has surged to 31.0% following Tara's Pickup Perks campaign. Cost per order has dropped to $7.30, consistent with the FON2 and JOL1 automation rollout, alongside some ordinary post-peak reversion in that same window.
**[00:05:35] deborah.osei:** Excellent work, team. Let's make sure the MBR deck reflects these trade-offs honestly. See you all at 8 AM tomorrow.

---
