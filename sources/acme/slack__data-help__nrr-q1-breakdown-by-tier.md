---
title: "Slack #data-help — NRR Q1 2026 breakdown by plan tier"
source_url: "internal://acme/slack/data-help/nrr-q1-breakdown"
license: "synthetic-demo"
attribution: "Acme Inc internal Slack conversation (synthetic demo)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

### #data-help

**2026-04-05 09:12 AM**
**@sam.reyes**: @lina.cho I’m starting on the Q1 board deck. Can we get the NRR breakdown for Q1 2026 (trailing 12 months) split by plan tier? I want to show the Enterprise vs. Business vs. Pro story.

**2026-04-05 09:15 AM**
**@lina.cho**: On it. Pulling from `marts/finance/nrr_trailing_12` now. Give me 10 mins to run the cohort splits.

**2026-04-05 09:34 AM**
**@lina.cho**: Okay, here are the numbers for the TTM window ending 2026-03-31:
- **Enterprise**: 118%
- **Business**: 109%
- **Pro**: 94%
- **Overall**: ~107% (matches the headline in `glossary__nrr.md`)

*Note: Free is N/A as it has no starting MRR for the denominator.*

**2026-04-05 09:36 AM**
**@sam.reyes**: Enterprise at 118% is huge. Business at 109% is solid. But Pro at 94%... that’s sub-100%. Why are we losing net revenue on the Pro cohort? Is that churn or just lack of expansion?

**2026-04-05 09:40 AM**
**@jorge.martinez**: @lina.cho does that Pro number include the involuntary churn spike we saw in Feb? We had that Stripe webhook issue that marked a bunch of Pro seats as uncollectible before they could retry.

**2026-04-05 09:42 AM**
**@lina.cho**: Good catch @jorge.martinez. Yes, `nrr_trailing_12` counts those as $0 in the numerator if they were still churned as of March 31. I just checked `fact_invoices` and about 2.5 points of that Pro dip is definitely involuntary churn from the Feb incident.

**2026-04-05 09:45 AM**
**@dan.lee**: There is also the "graduation effect" we’ve talked about. When a Pro customer expands and hits the 50-seat minimum, they move to Business. In our current NRR model, does that expansion credit stay in the Pro bucket or move to Business?

**2026-04-05 09:48 AM**
**@lina.cho**: It stays with the *starting* cohort tier. So if they started as Pro 12 months ago and are now Business, the expansion credit *should* show up in the Pro NRR. 
Wait—let me re-check the logic in `dbt/models/marts/finance/nrr_trailing_12.sql`.

**2026-04-05 09:55 AM**
**@lina.cho**: Actually, @dan.lee is right. The way we currently join `cohort_at_start` to `state_at_end`, we are looking at the *current* plan tier for the numerator grouping in the dashboard. So the Pro cohort "loses" its most successful expanders to the Business tier bucket. It’s a reporting artifact.

**2026-04-05 09:57 AM**
**@sam.reyes**: So Pro looks worse because it’s actually working as a funnel for Business?

**2026-04-05 10:01 AM**
**@dan.lee**: Exactly. It’s the graduation effect documented in `glossary__nrr.md`. We’re essentially "cannibalizing" the Pro NRR to fuel Business expansion. If we kept the expanders in the Pro bucket for this specific cut, Pro would likely be ~102-103%.

**2026-04-05 10:05 AM**
**@jorge.martinez**: We should probably clarify that in the board appendix. Otherwise, it looks like Pro is a leaky bucket when it’s actually our best feeder.

**2026-04-05 10:08 AM**
**@lina.cho**: Agreed. I’ll add a footnote to the slide. @sam.reyes I’ll also pull the "Gross Retention" (GRR) for Pro to show that the actual logo churn isn't as bad as the 94% NRR suggests.

**2026-04-05 10:12 AM**
**@sam.reyes**: Thanks Lina. Let's make sure we highlight the 118% for Enterprise. That’s the "land and expand" story Marcus wanted for this round.

**2026-04-05 10:15 AM**
**@lina.cho**: Will do. I'm updating the `arr_snapshot` and NRR tables now to make sure the Q1 close data is fully baked. 
:bar_chart: :white_check_mark:

**2026-04-05 10:20 AM**
**@david.kim**: @lina.cho just a heads up, I’m running a backfill on `fact_subscriptions` for some legacy `cust_000212` rows, shouldn't affect Q1 but might see a slight flicker in the warehouse for the next 5 mins.

**2026-04-05 10:22 AM**
**@lina.cho**: Thanks for the heads up @david.kim. I'll wait for your :green_check: before I export the final CSV for Sam.
