---
title: "Gong reactivation — cust_000156 post-pause seat expansion"
source_url: "internal://acme/gong/expansion/cust000156-seat-expansion"
license: "synthetic-demo"
attribution: "Acme Inc Gong transcript (synthetic demo). Owner: Marco Chen (Sr CSM)."
fetched_at: '2026-05-13T09:00:00+00:00'
adapter: gong_call
---

# Gong Transcript: cust_000156 Reactivation & Expansion

**Date**: 2026-05-12 10:00 AM PT
**Participants**:
- **Marco Chen** (Sr CSM, Acme)
- **Aiden Rouvier** (Product Manager, CloudStream — cust_000156)
- **Sarah Lopez** (Account Executive, Acme)

**Context**: CloudStream (cust_000156) paused their Business subscription in March 2024 due to a parent-company budget freeze (see `gong__churn__cust000156-budget-cut.md`). They are returning early to unpause and expand their seat count.

---

00:02 **MARCO CHEN**: Hey Aiden, great to see you again. It’s been, what, six weeks since we last spoke about the pause?

00:08 **AIDEN ROUVIER**: Yeah, just about. Honestly, I didn't expect to be back this quickly. The parent company finished their audit early and actually released a "growth stimulus" for our division. We’re greenlit to get our workflows back online immediately.

00:21 **MARCO CHEN**: That is fantastic news. I know we were all bummed to see those workflows go dormant. I’ve got Sarah Lopez here as well to help with the paperwork side of the reactivation.

00:30 **SARAH LOPEZ**: Hi Aiden! Glad to hear the budget situation cleared up.

00:34 **AIDEN ROUVIER**: Thanks, Sarah. So, here’s the deal. We don’t just want to unpause the original 50 seats. We’ve actually hired four new engineers in the interim who were supposed to start in Q3 but got pulled forward. We need to move to 54 seats on the Business tier.

00:52 **MARCO CHEN**: We can definitely handle that. Since you were in a `paused` status in `dim_customers`, your workflow configurations are all still there. We just need to flip the switch on the subscription.

01:05 **SARAH LOPEZ**: Aiden, regarding the 54 seats—since you're on the Business tier, you're already above the 50-seat minimum. Adding those 4 seats is straightforward. We’ll just update the `fact_subscriptions` record to reflect the new `seat_count` and `mrr_usd`.

01:22 **AIDEN ROUVIER**: Perfect. How does the billing work for the time we were paused? I know we had about 15 days left on the previous invoice when we hit the pause button.

01:34 **SARAH LOPEZ**: Great question. We’ll apply a prorated credit for those 15 days toward the first month of the new 54-seat subscription. You’ll see it as a line item on the next invoice in `fact_invoices`. 

01:48 **MARCO CHEN**: And Aiden, once we’re live, I want to make sure we do a quick health check. Your `engaged_customer` flag is obviously `FALSE` right now because of the zero activity. I’ll be monitoring `marts/product/workflow_runs_daily` to make sure your success rates are back to the 98% we saw in February.

02:05 **AIDEN ROUVIER**: That would be helpful. We have a few new webhooks that might need re-authing. I noticed some `AUTH_FAILED` errors right before we paused.

02:15 **MARCO CHEN**: Exactly. I'll pull the error distribution from `fact_workflow_runs` for your `customer_id` and send over a list of which connections need a refresh. It’ll save your team some hunting.

02:28 **AIDEN ROUVIER**: Appreciate that, Marco. What’s the timeline for getting the builders back in the seats?

02:35 **SARAH LOPEZ**: I’ll send the DocuSign for the 54-seat amendment right after this call. Once you sign, I’ll ping @tomas.vega in Engineering to trigger the manual unpause in the billing system. You should be active by 2 PM today.

02:50 **AIDEN ROUVIER**: That’s faster than I expected. We’ll get that signed immediately.

02:58 **MARCO CHEN**: One more thing, Aiden. Since you're expanding, you're now a "Healthy + Expansion Candidate" in our internal model (see `notion__csm-account-health-runbook.md`). This qualifies you for a free 1-hour session with our solutions architect to optimize those new engineer workflows. Interested?

03:15 **AIDEN ROUVIER**: Absolutely. Let's get them started on the right foot.

03:22 **MARCO CHEN**: Great. I’ll coordinate that. Sarah, anything else on the contract side?

03:28 **SARAH LOPEZ**: Nope, we’re keeping the same per-seat rate from your original Business contract. No price increases for this expansion.

03:38 **AIDEN ROUVIER**: Sounds good. Thanks for making this easy, guys. Glad to be back.

03:45 **MARCO CHEN**: Glad to have you back, Aiden. Talk soon.

---

**Post-call Actions**:
- @sarah.lopez to send 54-seat Business amendment for cust_000156.
- @marco.chen to monitor `fact_user_events` for first login post-reactivation.
- @marco.chen to schedule SA session for the 4 new seats.
- Update `dim_customers.status` from `paused` to `active` once contract is signed.
