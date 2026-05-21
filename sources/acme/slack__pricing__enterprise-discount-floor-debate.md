---
title: "Slack #pricing — enterprise discount floor debate"
source_url: "internal://acme/slack/pricing/enterprise-discount-floor-debate"
license: "synthetic-demo"
attribution: "Acme Inc Slack transcript (synthetic demo). Participants: Marcus Webb, Rachel Stein, Jorge Martinez, Sarah Lopez."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

### #pricing

**2026-03-30 09:12 AM**
**@marcus.webb**: Looking at the Q1 Enterprise wrap-up. We’re seeing a lot of margin leakage in the final 10% of the sales cycle. Right now, AEs have discretion up to 10% and Sales Managers up to 20% per `notion__pricing-tiers.md`. I’m proposing we tighten the AE floor to 5% and the Manager floor to 10% for all Enterprise deals >$100k ACV. We’re giving away too much on the 1-yard line.

**2026-03-30 09:25 AM**
**@rachel.stein**: Support the sentiment, but I want to see the distribution before we move the goalposts. If we’re consistently landing at 15-18%, a 10% floor just creates more escalation traffic for me and Sam. @jorge.martinez can you pull the Q1 discount spread for Enterprise Closed_Won?

**2026-03-30 10:45 AM**
**@jorge.martinez**: Just finished the export from `fact_opportunities` joined with the price book. Here’s the Q1 breakdown for Enterprise:
- **Mean Discount**: 18.2%
- **Median Discount**: 17.0%
- **Top Decile**: 28.4% (mostly multi-year deals)
- **Standard Deviation**: 6.2%
Basically, only 4 deals in Q1 came in under a 10% discount. If we move the floor to 10%, almost every deal becomes an escalation.

**2026-03-30 10:52 AM**
**@marcus.webb**: 18.2% mean is way too high for this stage of our growth. That’s nearly $1.2M in ARR left on the table in Q1 alone based on the `arr_snapshot`. 📉

**2026-03-30 11:05 AM**
**@sarah.lopez**: Pushing back here. Enterprise is getting incredibly competitive. We’re going up against legacy players who are willing to slash price just to keep us out of the account. If I’m at 10% and the competitor drops another 15%, I need the flexibility to move fast. Less discount = more lost deals to "Price" (which is already a top 3 loss reason in `fact_opportunities`).

**2026-03-30 11:12 AM**
**@marcus.webb**: @sarah.lopez I hear you, but are we losing on price or are we just not selling the value of the workflow engine? If we’re the only ones with the SOC2 + Private Deployment combo, we shouldn't be discounting like a commodity.

**2026-03-30 11:18 AM**
**@sarah.lopez**: We sell the value, but procurement doesn't care about Private Deployments when they have a mandate to cut 20% off every SaaS line item this year.

**2026-03-30 11:30 AM**
**@rachel.stein**: @jorge.martinez do we see a correlation between discount % and `sales_cycle_days`? I have a hunch that the high-discount deals are actually closing *slower* because of the back-and-forth.

**2026-03-30 11:45 AM**
**@jorge.martinez**: Looking... actually, it's the opposite. Deals with >20% discount close in ~72 days. Deals with <10% discount are averaging 105 days. The discount is definitely being used as a "close-it-now" lever.

**2026-03-30 11:50 AM**
**@marcus.webb**: Which confirms my point. It’s a crutch.

**2026-03-30 12:02 PM**
**@lina.cho**: From an FP&A perspective, the NRR impact of these high discounts is also a concern. If we start them at 25% off, the expansion path to "full price" is much harder. We’re basically subsidizing the first 2 years of the LTV.

**2026-03-30 12:15 PM**
**@rachel.stein**: I'm not ready to approve a hard floor change today. Let's park this for the Q2 Planning session next week. I want Jorge to model what happens to the forecast if we assume a 5% win-rate drop-off but a 10% increase in realized ACV.

**2026-03-30 12:20 PM**
**@marcus.webb**: Fair. @jorge.martinez let's get that model ready for Monday's exec sync. @sarah.lopez keep doing what you're doing for now, but tell the team the "discount party" is under review.

**2026-03-30 12:22 PM**
**@sarah.lopez**: Copy that. 🫡
> 🧵 *1 reply from @jorge.martinez: Working on the model now. Will use `marts/sales/bookings_attribution` as the base.*

**2026-03-30 01:00 PM**
**@marcus.webb**: (Thread parked for Q2 Planning) ✅
