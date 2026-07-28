---
title: "Slack thread: a PM checks 'anything running in US_CONV' and reads the blended net experiment effect as ~nothing"
source_url: "internal://acme-ecomm/slack/q2fy27__us-conv-experiment-check-blended-net-wash"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: slack_thread
---

**Channel:** `#us-conv` (US/CA/MX Conversion & Traffic)  
**Date:** July 18, 2026  
**Topic:** Quick check on active experiments in US_CONV following last week's conversion dip (2.86% for the week ending July 18 down from 3.24% the prior week).

***

**[10:14 AM] tyler.vance** *(Growth Marketing Analytics)*:
Hey team, just pulling some numbers for the weekly prep ahead of Monday’s MBR deck lock. Anyone tracking if we have anything heavy live right now in `US_CONV` that might explain why conversion softened a bit last week? I see we ticked down to 2.86% from 3.24% the week prior. Want to make sure I’m calling out any known traffic or experiment noise if leadership asks about the swing during the executive sync.

**[10:16 AM] owen.faust**:
Morning Tyler. Let me check the registry. Off the top of my head, we’ve got `exp_2601` (Search Relevance Re-ranking) running, and Maya’s team has `exp_2618` (Item Page Media Carousel Autoplay) going since early June, but honestly I haven't looked at the aggregate net of those two in a minute. Everything else from the Q1 pushes (like Checkout Simplify or the Nav Refresh holdback stuff) has long since shipped or wrapped. 

**[10:18 AM] tyler.vance**:
Ah, cool. Where should I look to pull a quick blended read on those two? Just drop a quick query in `fact_experiment_readouts`?

**[10:19 AM] owen.faust**:
Yeah, exactly. Grab `dim_experiment` joined with `fact_experiment_readouts` for anything where `vertical_code = 'US_CONV'` and `status = 'running'`. You can filter for the ones started back on June 8th (`exp_2601` and `exp_2618`). Should be right there in BigQuery.

**[10:25 AM] tyler.vance**:
:eyes: Found it. Quick SQL check on `fact_experiment_readouts` for the latest exposed-basis lift on those two:
- `exp_2601` (Search Re-ranking): sitting around `+1.6%` lift on the exposed arm.
- `exp_2618` (Media Carousel Autoplay): tracking around `-1.5%` drag on the exposed arm.

If I just blend those two together roughly equal-weighted, the net effect is basically ~+0.05%. Total wash. 

**[10:26 AM] maya.lindqvist**:
lol classic. They just eat each other for breakfast. 

**[10:27 AM] owen.faust**:
That tracks. Perfectly balanced, as all things should be :thanos:

**[10:27 AM] tyler.vance**:
Awesome, perfect. So essentially nothing moving the needle net-net from an experimentation standpoint. Good to know. I'll drop a note in the MBR prep doc that in-flight experiments are roughly a net-zero wash and won't dwell on them. Thanks!

**[10:28 AM] maya.lindqvist**:
Yeah, nothing to see there. By the way, is anyone else having issues with the Compass dashboard today? My PDT view is still showing the old Q4FY26 Marketplace GMV numbers ($952.4M instead of the restated $975.0M) and it's driving me nuts when I try to cross-reference category share.

**[10:30 AM] owen.faust**:
Did you hard-refresh your cache? Connor’s pipeline fixes from back in February were supposed to clear that, but Compass caches are notoriously sticky. Try appending `?nocache=true` to the URL.

**[10:31 AM] maya.lindqvist**:
Ah, that fixed it. Thanks! Back to writing this section on the mobile app mix shift. App traffic share jumping from 28% to nearly 38% in a week is wild.

**[10:35 AM] tyler.vance**:
Alright, updating the slide now. Appreciate the quick pointer on the experiment table, saved me digging through the raw parquet logs. Cheers :coffee:

***
