---
title: "Slack #sales-ops — H2 2026 quota setting discussion"
source_url: "internal://acme/slack/sales-ops/h2-quota-setting"
license: "synthetic-demo"
attribution: "Acme Inc internal Slack transcript (synthetic demo)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

**#sales-ops**

**marcus.webb** [2026-04-28 09:15 AM]
@jorge.martinez @lina.cho @rachel.stein — starting the H2 2026 quota planning cycle. We need to lock these by May 15th to get the comp plans out before July 1. 

Initial thoughts: we’re seeing strong tailwinds on the Business tier ($149/seat). I want to push the MM team quotas up by ~12% for H2. Thoughts on where we landed for Q1 attainment?

**jorge.martinez** [2026-04-28 09:42 AM]
Just pulled the final Q1 numbers from `dbt__model__bookings_attribution.md`. 
Average attainment across the board was **94.2%**. 
*   SMB: 102% (over-performed on Pro-to-Business self-serve conversions)
*   MM: 91% (a few deals slipped from March to April)
*   Ent: 88% (heavy reliance on the Halcyon expansion, see `gong__renewal__halcyon-research.md`)

@marcus.webb 12% hike for MM feels aggressive if we only hit 91% in Q1.

**marcus.webb** [2026-04-28 09:45 AM]
The MM slippage was timing, not volume. Most of those April closes are already in. I think the pipe supports it. @lina.cho what’s the FP&A view on the H2 ARR target?

**lina.cho** [2026-04-28 10:02 AM]
Board target for EOY is still ~$48M ARR. We’re at ~$39M now. That means we need ~$9M net new ARR in H2. If we account for ~5% churn/contraction, the gross bookings target needs to be closer to $10.5M. 

A 12% hike on MM quotas gets us about 80% of the way there. We’ll need the rest from Enterprise or a very heavy Q4.

**sarah.lopez** [2026-04-28 10:15 AM]
Quick question on the headcount side — we have two new AEs starting May 1 (one MM, one Ent). How are we thinking about their ramp quotas for H2? If we hike the baseline, does the ramp scale too?

**marcus.webb** [2026-04-28 10:20 AM]
Welcome to the team (almost) to the new hires. 
Standard ramp: 
Month 1: $0 (Training/Shadowing)
Month 2: 50%
Month 3: 75%
Full quota by Month 4.

Actually, given the complexity of the Business tier integrations now, let's do a 3-month Q3 ramp: 
**70% / 85% / 100%** across July/Aug/Sept. 
@jorge.martinez can you model that out against the $10.5M gross target?

**jorge.martinez** [2026-04-28 10:35 AM]
On it. I'll update the `fact_opportunities` forecast logic to include the ramped seats. 
One concern: if we hike MM quotas, we need to make sure the SDR lead gen for Business tier stays at the current velocity. @jasmine.park — are we maintaining the paid search spend for "workflow automation" into Q3?

**jasmine.park** [2026-04-28 10:48 AM]
Yes, keeping the budget steady. We actually just backfilled the `spend_usd` data in `fact_marketing_touches` (see `notion__data-warehouse-conventions.md` updates). ROAS on the Business tier is our best performer right now, so Marketing is aligned with the MM push.

**sarah.lopez** [2026-04-28 11:05 AM]
@marcus.webb The 70/85/100 ramp for the new folks sounds fair. It gives them enough runway to build a pipe in the Business tier without getting buried in Month 2. 

**rachel.stein** [2026-04-28 11:20 AM]
@marcus.webb I’m okay with the 12% MM hike as long as we keep the discount floor tight. We saw too many 15% exceptions in Q1 (per your note in `notion__pricing-tiers.md`). If we raise quotas, AEs will be tempted to discount to hit the higher number. We need to hold the line on the $149/seat price point.

**marcus.webb** [2026-04-28 11:25 AM]
Agreed. @jorge.martinez let's add a "Discount %" column to the H2 attainment dashboard so it's front and center during 1:1s.

**jorge.martinez** [2026-04-28 11:40 AM]
Will do. I’ll pull a draft of the H2 Quota Sheet into the Sales Ops folder by EOD tomorrow for final review.
:white_check_mark: 3

**marcus.webb** [2026-04-28 11:45 AM]
Thanks all. @lina.cho let's sync for 15 mins on Friday to make sure the $48M EOY glide path looks realistic with these numbers.

**lina.cho** [2026-04-28 11:46 AM]
Done. Sent an invite. 
:calendar:
