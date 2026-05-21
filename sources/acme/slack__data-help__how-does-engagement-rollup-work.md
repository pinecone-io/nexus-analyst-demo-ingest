---
title: "Slack #data-help — how does engagement rollup work?"
source_url: "internal://acme/slack/data-help/engagement-rollup"
license: "synthetic-demo"
attribution: "Acme Inc Slack transcript (synthetic demo). Participants: @marco.chen, @rajiv.patel, @david.kim."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

### #data-help

**2026-02-18 09:12 AM**
**@marco.chen**: Hey data team—I’m looking at the `account_health` dashboard for a few of my MM accounts. I see `is_engaged = TRUE` for a customer that has basically zero logins this week, but they had a spike 3 weeks ago. Can someone walk me through the exact rollup logic? I want to make sure I’m not misrepresenting "health" to Elena in our 1:1.

**2026-02-18 09:24 AM**
**@rajiv.patel**: Hey @marco.chen! Happy to clarify. The engagement signal is a trailing 28-day window, so it’s definitely "sticky." Here’s the data chain:

1. **Raw Events**: We ingest `login` events into `fact_user_events` and every execution into `fact_workflow_runs`.
2. **Daily Rollup**: `dbt__model__workflow_runs_daily.md` aggregates these into per-customer-per-day counts.
3. **The 28d Window**: The `is_engaged` flag in `dbt__model__account_health.md` looks back exactly 28 days from the current refresh.
4. **The Thresholds**: To get that `TRUE` value, they need **≥3 active users** (distinct logins) AND **≥10 successful runs** anywhere in that 28-day bucket.

So if they had 5 users and 50 runs in a single day 20 days ago, they’ll stay "Engaged" for another 8 days even if they’ve done nothing since.

**2026-02-18 09:28 AM**
**@marco.chen**: Got it. So it’s a binary floor, not a trend. That explains why `cust_000512` (Vandelay Industries) looks "healthy" despite their champion leaving on the 1st. They’re still riding the high of their onboarding activity from late January. 

**2026-02-18 09:35 AM**
**@rajiv.patel**: Exactly. It’s a "floor" definition. We designed it to catch "ghosting" (0 users) or "broken integrations" (0 runs), but it’s not great at detecting a slow fade-out. 

**2026-02-18 09:40 AM**
**@david.kim**: Jumping in here—@marco.chen, if you need to see the "fade-out" specifically, check the `utilization` column in that same `account_health` model. It’s `active_users / seat_count`. If that’s dropping while `is_engaged` stays TRUE, that’s your leading indicator of a champion departure or use-case exhaustion.

**2026-02-18 09:42 AM**
**@marco.chen**: Thanks @david.kim. Is there a way we can make the engagement signal more sensitive? Like a 7-day window?

**2026-02-18 09:50 AM**
**@rajiv.patel**: We talked about that in the Q4 retro (see `postmortem__engagement-threshold-recalibration-2025-Q4.md`). A 7-day window is too noisy because of holidays and vacations—we’d get 100+ "at-risk" alerts every long weekend. 

**2026-02-18 09:55 AM**
**@rajiv.patel**: The real solution is the **Value Realization Score (VRS)** that @dan.lee is spec-ing out. It’ll be a 0-100 score that accounts for velocity and trend, not just a binary check. Check out the draft here: `notion__draft__value-realization-score-spec.md`.

**2026-02-18 10:02 AM**
**@marco.chen**: That VRS spec looks like exactly what we need. 100% agree that "engagement floor != value realization." I'll keep an eye on `utilization` and `nps_responses` for my accounts until that ships. 

**2026-02-18 10:05 AM**
**@david.kim**: One last thing—if you see a customer where `is_engaged` is TRUE but `successful_runs_28d` is exactly 10, be careful. That’s usually a single scheduled heartbeat workflow that doesn't represent real human value. 

**2026-02-18 10:07 AM**
**@marco.chen**: 🎯 Good catch. I'll check the `triggered_by` mix in `fact_workflow_runs` if I suspect that. Thanks all!
> 👍 *1 reaction from @rajiv.patel*
> 🚀 *1 reaction from @elena.volkov*
