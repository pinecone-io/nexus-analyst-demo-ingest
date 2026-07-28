---
title: "Slack thread: engineering notices Checkout Simplify and Nav Refresh timing overlap"
source_url: "internal://acme-ecomm/slack/q1fy27__eng-checkout-nav-refresh-timing-overlap-thread"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-04-15T12:00:00+00:00'
adapter: slack_thread
---

**Channel:** `#product-eng`
**Date:** March 3, 2026 – March 4, 2026
**Topic:** Checkout Simplify (`exp_2214`) vs Nav Refresh (`exp_2215`) release timing overlap

---

**[2026-03-03 14:12:05 ET] @tara.oduya**
hey @owen.faust quick Q — did Checkout Simplify land its full rollout or is it still running through the variant groups? looking at the FON2 sortation telemetry today and trying to line up why the mobile funnel steps look a bit jumpy post-weekend. 

**[2026-03-03 14:15:30 ET] @owen.faust**
@tara.oduya still running! `exp_2214` isn't scheduled to wrap up until the end of the month (around March 30). We’re still collecting exposure data across both variants. Why, seeing weirdness on the fulfillment side?

**[2026-03-03 14:18:41 ET] @tara.oduya**
nah, nothing broken on our end, just auditing the post-peak metrics after the JOL1 winter storm tail-end adjustments and trying to keep my sanity while the automated sorting lines settle down. carry on!

**[2026-03-03 14:22:10 ET] @maya.lindqvist**
Wait... @owen.faust — did you say `exp_2214` is running through March 30? 

**[2026-03-03 14:22:45 ET] @owen.faust**
Yeah, standard 6-week window. Started back on Feb 16. Why do you ask, Maya?

**[2026-03-03 14:25:02 ET] @maya.lindqvist**
Uhh. Didn't Nav Refresh launch yesterday? (March 1st, per the release sync). 

**[2026-03-03 14:25:38 ET] @owen.faust**
...Yeah? You pushed the sitewide navigation redesign into production on Sunday. What about it?

**[2026-03-03 14:28:15 ET] @maya.lindqvist**
Check the config matrix for `exp_2215` and your experiment arms, dude. We didn't carve out a clean control for the nav overhaul relative to your checkout variants. The Nav Refresh rolled out into *both* of your Checkout Simplify experimental arms simultaneously.

**[2026-03-03 14:29:40 ET] @owen.faust**
*[typing...]*
*[message deleted]*

**[2026-03-03 14:31:05 ET] @owen.faust**
Wait, let me pull up the deployment manifest. We coordinated the feature flag overrides with frontend core, but... wait, did anyone route the nav rollout past the experiment routing layer?

**[2026-03-03 14:32:12 ET] @maya.lindqvist**
That's what I'm saying. We kept the 5% holdback group (`exp_2215`) isolated so we could read the independent sitewide lift for the nav changes overall, but everything else that hit the main traffic pool got the new nav header *regardless* of whether they were in Checkout Simplify control or treatment B. 

**[2026-03-03 14:33:50 ET] @amara.shah**
*grabbing popcorn* 

**[2026-03-03 14:34:02 ET] @amara.shah**
Does this mean your conversion lift readouts for March are going to be completely cross-contaminated? 

**[2026-03-03 14:35:19 ET] @maya.lindqvist**
I mean... technically the interaction effect is going to be baked into Owen's numbers for the next four weeks unless we slice out the pre-March-1 data or lean entirely on the 5% holdback cohort to untangle it. 

**[2026-03-03 14:36:40 ET] @owen.faust**
fuuuuuuuuck. 

**[2026-03-03 14:37:01 ET] @owen.faust**
Let me check the numbers we pulled this morning. The early read for the first two days of March is showing a sharp uptick, but if the nav redesign dropped right on top of our checkout flow changes, we won't be able to isolate whether the extra conversion bump came from the simplified form fields or the cleaner top-level header navigation.

**[2026-03-03 14:38:22 ET] @carlos.figueroa**
@ow @maya — bring this to the data sync on Thursday. We need to make sure Finance doesn't lock in the Q1 MBR deck assumptions based on a confounded experiment read. 

**[2026-03-03 14:39:10 ET] @owen.faust**
Will do, Carlos. Let me run a quick query in BigQuery against `fact_experiment_readouts` to see what the clean pre-confound slice looks like for Feb 16 through Feb 28. At least we have those two weeks before Maya's nav deployment dropped.

**[2026-03-03 14:40:05 ET] @connor.blake**
Just a heads up while you're querying: don't forget that Wei pushed the `sessions_definition_version` 1→2 cutover yesterday morning (`2026-03-02`), so any aggregate traffic views across the boundary date are going to have that bot-filtering denominator shift baked in anyway. Make sure you're segmenting by version if you're comparing pre-March vs post-March conversion rates!

**[2026-03-03 14:42:18 ET] @owen.faust**
Right, bot filtering and multi-tab deduplication. Thanks Connor, nearly forgot about that. Today is just a wonderful day for data integrity.

**[2026-03-03 14:43:01 ET] @maya.lindqvist**
hey look on the bright side, at least the 5% holdback readout for `exp_2215` is running clean on its own track so we'll still have an isolated baseline for the nav changes when it wraps up later this month.

**[2026-03-03 14:44:15 ET] @felix.arroyo**
Keep me in the loop on how we're going to present this to leadership. If we have to put an asterisk on the checkout conversion gains when we go to board review, I want to make sure the narrative is tight. 

**[2026-03-04 09:15:22 ET] @owen.faust**
Quick update: still working through the raw exposures for the pre-confound slice (Feb 16–28) — will have the isolated lift number once that query's done. Once the nav changes hit on March 1, the blended number jumps up, but like we noted yesterday, that's definitely carrying the overlap. We'll document the confound in the official experiment readout doc so nobody tries to attribute the whole +2.1% final headline number purely to the checkout form reflow.

**[2026-03-04 09:18:04 ET] @maya.lindqvist**
Appreciate you calling that out, Owen. Glad we caught it now rather than after shipping to 100% based on muddy data. I'll grab a coffee and meet you in the huddle room in 10.

---
