---
title: "Slack #marketing-attribution — first vs last touch (and a side-debate about multi-touch)"
source_url: "internal://acme/slack/marketing-attribution/2026-04-02-first-vs-last"
license: "synthetic-demo"
attribution: "Synthetic Slack thread, Acme Inc internal demo."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

# #marketing-attribution — 2026-04-02 — first vs last touch?

---

**aliyah.brooks** — 9:30 AM
quick clarifier — when i'm reporting `attributed_revenue_usd` from `fact_marketing_touches`, is that **first-touch** or **last-touch**? asking bc the campaign report i'm building groups by `utm_campaign` and the totals look weird if multiple touches share a campaign

**jasmine.park** — 9:42 AM
first-touch. we chose ~18mo ago bc it's simpler + more defensible at AE pipeline review (credit goes to whoever brought them in the door). last-touch tends to over-credit nurture / branded search which would make our content team look better than they probably are :see_no_evil:

so if a customer has 5 marketing touches across paid_search, content, email etc, the **first** touch (chronologically) gets the full attributed_revenue_usd. other 4 touches show NULL in that column even though they're real interactions

**aliyah.brooks** — 9:46 AM
got it. so if i'm computing campaign ROAS, sum `attributed_revenue_usd` filtered to the campaign — and that will only count first-touches. other touches by same lead are excluded

**jasmine.park** — 9:48 AM
right. ROAS = `SUM(attributed_revenue_usd) / SUM(spend_usd)`. we don't have `spend_usd` in the warehouse, that lives in marketing-platform exports — for now you'll need to overlay spend manually from the marketing-ops sheet :sweat_smile:

**lina.cho** — 9:54 AM
side note: there's a separate Q of whether first-touch is the right model. we've talked about moving to multi-touch (e.g. linear or U-shaped) but haven't built it. if you want to experiment, you can compute multi-touch in dbt as a downstream model — `fact_marketing_touches` has every touch, the model is just attribution logic

**jasmine.park** — 9:56 AM
:point_up: that's on the H2 roadmap. for now first-touch is canonical

**david.kim** — 10:02 AM (joined thread)
btw the spend_usd thing is silly we should just load it. it's in the HubSpot export. i can prioritize next sprint if marketing wants

**jasmine.park** — 10:04 AM
yes please :pray::pray:

**david.kim** — 10:05 AM
:+1: jira ticket coming

**aliyah.brooks** — 10:06 AM
:tada::tada:

**dan.lee** — 10:30 AM (joined thread, randomly)
not super related but @jasmine.park while you're here, the H2 marketing OKR draft you sent — i had some thoughts. mind a 15min sync this week?

**jasmine.park** — 10:32 AM
yes! tomorrow 11am works?

**dan.lee** — 10:33 AM
:+1: cal invite incoming

> *thread fizzles, archived 14d later*

**aliyah.brooks** — 04-09 4:00 PM (a week later)
update: spend_usd loaded into fact_marketing_touches as of last night. ROAS dashboard now self-serve :tada: thx @david.kim

**david.kim** — 04-09 4:02 PM
:rocket:

---

**Related**: `glossary__arr.md`, `notion__marketing-attribution-model.md`
