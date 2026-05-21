---
title: "Slack #revenue — discount exception request for cust_000087"
source_url: "internal://acme/slack/revenue/discount-exception-cust000087"
license: "synthetic-demo"
attribution: "Acme Inc Slack archive (synthetic demo). Participants: Sarah Lopez, Marcus Webb, Jorge Martinez, Rachel Stein."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

# #revenue: Discount exception request (cust_000087)

**2026-03-22 09:12 AM**
**@sarah.lopez**: Hey @marcus.webb — requesting a discount exception for the Halcyon Research (`cust_000087`) renewal. They are currently on a Business plan but are looking to lock in a 2-year commit. To get the multi-year deal done, they’re asking for a 14% total discount. I know my limit is 10% per `notion__pricing-tiers.md`, but this is a key MM account for us. Can we approve?

**2026-03-22 09:45 AM**
**@marcus.webb**: Halcyon is a solid logo. @sarah.lopez what’s the current ARR and what does the NRR look like for that cohort? I want to make sure we aren't discounting an account that's already expanding significantly.

**2026-03-22 10:05 AM**
**@jorge.martinez**: Pulling the numbers from `dbt__model__arr_snapshot.md` now. 
*   **Current ARR**: $84,000 (Business tier, 50 seats @ $140/seat - they have a slight legacy discount from 2024-Q4).
*   **Engagement**: They are firmly in the "Engaged Customer" bucket per `glossary__engaged_customer.md`.
*   **NRR Context**: This cohort (2024-Q3) is currently at ~1.08 NRR. Halcyon specifically has been flat for 6 months but usage is spiking on their webhook triggers.

**2026-03-22 10:12 AM**
**@sarah.lopez**: Thanks @jorge.martinez. To Marcus's point: they aren't expanding seats right now, but they are hitting the 100k run quota every month. The 2-year commit at 14% off list would actually be a slight net increase in total contract value compared to their current legacy rate if we move them to the current list price first.

**2026-03-22 10:30 AM**
**@marcus.webb**: If it’s a 2-year commit, we can usually stack the multi-year discount. @rachel.stein — thoughts on 14% here? It’s above my 20% escalation threshold if we were talking new business, but for a renewal exception, I wanted your eyes on it.

**2026-03-22 11:05 AM**
**@rachel.stein**: Checking the discount matrix in `notion__pricing-tiers.md`. Standard 2-year multi-year discount is 8%. Sarah is asking for an additional 6% on top of that to hit the 14% total?

**2026-03-22 11:12 AM**
**@sarah.lopez**: Correct. They want a "round number" on the per-seat cost that lands at 14% off the current $149 Business list price.

**2026-03-22 11:45 AM**
**@rachel.stein**: Given the 2-year lock-in and the fact that they are high-utilization (hitting the run quota), I’ll approve. It’s better to have the $168k+ TCV committed than risk a month-to-month churn or downgrade if they feel the price hike from their legacy rate is too steep. 

**2026-03-22 11:47 AM**
**@rachel.stein**: Approved for 14% on a 24-month term. @jorge.martinez please ensure the `fact_subscriptions` entry reflects the `change_type = 'renewal'` and the correct `end_date` for 2028.

**2026-03-22 11:50 AM**
**@sarah.lopez**: Awesome, thanks Rachel! Sending the updated order form now. 🚀
> ✅ *Reaction: @marcus.webb, @jorge.martinez*
