---
title: "Slack #data-help — multi-touch attribution question"
source_url: "internal://acme/slack/data-help/multi-touch-attribution-question"
license: "synthetic-demo"
attribution: "Acme Inc internal Slack communications (synthetic demo)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

# #data-help: Multi-touch attribution status

**jasmine.park** [10:14 AM]
Hey data team! Quick question for a campaign ROAS report I’m building for Sam. Are we currently supporting multi-touch attribution in the warehouse, or are we still strictly on a first-touch model? I see some `fact_marketing_touches` rows that look like they could be used for a linear model, but I don't want to go rogue if there's a canonical mart I should be using.

**jorge.martinez** [10:22 AM]
Hey @jasmine.park — we are still strictly first-touch for the canonical "official" numbers. If you look at `dbt__model__bookings_attribution.md`, you’ll see we join the won opportunity to the earliest marketing touch for that `customer_id`.

**jorge.martinez** [10:24 AM]
Specifically, you want to use the `first_touch_channel` and `first_touch_campaign` columns in `marts/sales/bookings_attribution.sql`. Anything else won't tie out to the Sales Ops dashboards.
> :white_check_mark: 2

**jasmine.park** [10:26 AM]
Got it. Is there a timeline for multi-touch? We’re seeing a lot of high-intent webinar signups that happen *after* a first-touch paid search click, and first-touch is making our content spend look less effective than it feels.

**jorge.martinez** [10:31 AM]
It’s on the H2 roadmap. @david.kim and I have been scoping a U-shaped model, but the logic for credit weighting is still being debated by the growth team. For now, it is explicitly NOT shipped. If you build something custom, just make sure to label it as "Experimental/Marketing-only" so it doesn't get confused with the board-deck figures.

**lina.cho** [10:45 AM]
+1 to what Jorge said. From the FP&A side, we only recognize first-touch for the CAC and Payback metrics we send to the board. If we start switching models mid-quarter, our NRR/CAC ratios are going to look wonky. 
> :chart_with_upwards_trend: 1

**jasmine.park** [10:48 AM]
Understood, thanks @lina.cho. I'll stick to the `bookings_attribution` mart for this report to keep it consistent with Sam's other views. 

**jorge.martinez** [10:50 AM]
No problem. Also, check out `slack__marketing__attribution-model-question.md` (I think David archived a thread there) for the full history of why we landed on first-touch for now. It basically came down to lead-to-conversion lag being so long that multi-touch was too noisy with our current tracking setup.

**jasmine.park** [10:52 AM]
Will do. Thanks all!
> :pray: 1

**david.kim** [11:05 AM]
@jasmine.park just saw this — if you find specific gaps where first-touch is totally missing the boat (like that webinar example), let me know. We can use those as test cases when we start the H2 multi-touch pilot.

**jasmine.park** [11:07 AM]
Will do, @david.kim. I'll pull a list of the "webinar-heavy" won deals that are currently attributed to `paid_search` and send them over.
