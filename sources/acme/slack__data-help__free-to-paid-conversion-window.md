---
title: "Slack #data-help — Free→Paid conversion window question"
source_url: "internal://acme/slack/data-help/free-to-paid-conversion-window"
license: "synthetic-demo"
attribution: "Acme Inc Slack archives (synthetic demo). Participants: Jasmine Park, Dan Lee, Lina Cho."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

# #data-help: Free→Paid conversion window

**2026-02-25 09:14 AM**

**@jasmine.park**: Hey data team! 👋 I’m pulling numbers for the H1 acquisition deck. What’s our canonical definition for "Free to Paid conversion window"? I’m seeing a few different versions in old Looker dashboards. Is it signup to first `Closed_Won` opp, or signup to first paid invoice?

**2026-02-25 09:22 AM**

**@dan.lee**: Hey Jasmine! We standardized this in Q4. The canonical metric is **Signup Date** (from `dim_customers`) to **First Paid Invoice Date** (from `fact_invoices`). 

We use the invoice date rather than the opportunity date because it captures the actual cash-in-door moment for self-serve Pro users who never have a Salesforce opportunity.

**2026-02-25 09:25 AM**

**@jasmine.park**: Got it. That makes sense for the PLG side. Do we have a current p50 for that window?

**2026-02-25 09:31 AM**

**@dan.lee**: For the trailing 6 months, the **p50 is 18 days**. 
The distribution is super front-loaded—about 30% convert in the first 48 hours (the "I signed up specifically to buy" group), then a long tail of folks who use the Free tier for a full billing cycle before hitting the 100-run limit.

**2026-02-25 09:45 AM**

**@lina.cho**: @dan.lee jumping in here—how are we handling the long-tail conversions for the H1 deck? I remember we discussed a cutoff because some users take 6+ months to convert and it drags the mean way up.

**2026-02-25 09:52 AM**

**@dan.lee**: Good catch @lina.cho. For the canonical metric in `marts/marketing/conversion_funnel.sql`, we **cap the window at 90 days**. 

If someone signs up in January and converts in August, they count as a "Reactivation" or "Delayed Conversion" in the ARR breakdown, but they are excluded from the "Conversion Window" p50/mean calculation. Otherwise, the metric is too unstable to use for month-over-month performance tracking.

**2026-02-25 10:05 AM**

**@jasmine.park**: That works for me. So for the deck, I'll report:
- **Definition**: Days from `dim_customers.signup_date` to first `fact_invoices.paid_at`.
- **Cohort**: Bucketed by signup month.
- **Filter**: Conversions > 90 days excluded from the average.

Does that sound right?

**2026-02-25 10:12 AM**

**@dan.lee**: Spot on. 🎯 
One nuance: make sure you're looking at the *signup cohort* not the *conversion month*. If you look at people who converted in Feb, some signed up in Nov. If you want to see if our onboarding changes in Jan worked, you have to look at the Jan signup cohort and wait 30-60 days for the data to mature.

**2026-02-25 10:14 AM**

**@jasmine.park**: Perfect. I'll stick to the Jan cohort for the "recent" view. Thanks Dan!

**2026-02-25 10:15 AM**

**@lina.cho**: @jasmine.park if you need the SQL for the 90-day cutoff, it’s in `glossary__nrr.md` (well, the logic is similar to how we cohort for NRR). Or just use the `conversion_window_days` column in `marts/marketing/conversion_funnel`.

**2026-02-25 10:20 AM**

**@jasmine.park**: Thanks Lina, I'll pull from the mart model directly. 🚀
> ✅ *Reaction: :white_check_mark: by @dan.lee*
> ✅ *Reaction: :thank_you: by @jasmine.park*

**2026-02-25 11:02 AM**

**@dan.lee**: Oh, one last thing @jasmine.park—if you see a spike in the window for the Enterprise segment, ignore it. Enterprise "signups" often happen months after the initial sales touch because they don't create an account until the security review is done. The conversion window metric is really only "clean" for SMB and MM.

**2026-02-25 11:05 AM**

**@jasmine.park**: Noted. I'll add a footnote that the metric is primarily tracking our PLG/Self-Serve efficiency. Cheers!
