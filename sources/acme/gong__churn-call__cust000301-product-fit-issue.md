---
title: "Gong churn call — cust_000301 product-fit mismatch"
source_url: "internal://acme/gong/calls/cust000301-churn-retro"
license: "synthetic-demo"
attribution: "Acme Inc internal Gong transcript (synthetic demo). Owner: Marco Chen (Sr CSM)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: gong_call
---

# Gong Transcript: Exit Interview — cust_000301 (Helix Manufacturing)

**Date**: 2026-03-12
**Participants**:
*   **Marco Chen** (Sr CSM, Acme)
*   **Hannah Brakebill** (Director of Ops, Helix Manufacturing)

**Context**: Helix Manufacturing (cust_000301) is a Business-tier customer (~$89k ARR) that signed in Q1 2025. They have officially submitted a churn notice for their upcoming April renewal. This call is a retrospective to understand the "why" and explore save options.

---

00:00  **MARCO CHEN**: Hi Hannah, thanks for jumping on. I know the team was disappointed to see the cancellation notice come through, but I really appreciate you taking the time to give us some candid feedback before the contract wraps up.

00:02  **HANNAH BRAKEBILL**: Yeah, of course, Marco. You’ve been great to work with, so I didn't want to just ghost. It’s not a "we hate the tool" situation, it’s just a "we can’t justify the line item" situation.

00:05  **MARCO CHEN**: I appreciate that. Looking at the usage data, I see you guys have about 12 workflows running consistently, mostly success rates in the 99% range. What changed on your end in terms of how you're valuing the platform?

00:08  **HANNAH BRAKEBILL**: Honestly, it’s the seat minimums on the Business tier. When we signed last year, our previous VP of Ops was convinced we were going to roll Acme out to the entire project management and dev-ops org—like 60 or 70 people. We committed to the 50-seat minimum to get the SSO and the audit logs, which our security team required.

00:12  **MARCO CHEN**: Right, the Business tier starts at 50 seats. And I see you’re currently provisioned for exactly 50, but looking at `fact_user_events`, only about 8 of those seats are active in a given month.

00:15  **HANNAH BRAKEBILL**: Exactly. We have 8 power users. The other 42 seats are just... expensive ghosts. We’re paying $149 a seat for 50 people, so we’re essentially paying over $7,000 a month to run 12 workflows. My CFO looked at the ROI on that and basically told me I had to cut it. We love the workflow builder, but the math doesn't work at our current scale.

00:21  **MARCO CHEN**: I totally hear you. That’s a classic "over-bought" scenario. If the seat count is the primary friction, have you considered a downgrade to our Pro tier? We could move you to a per-seat model where you only pay for those 8-10 active users. At $49 a seat, your monthly bill would drop from ~$7,450 to under $500.

00:25  **HANNAH BRAKEBILL**: We looked at that. The problem is the security requirements I mentioned. Our IT policy is zero-tolerance for tools that don't support SAML SSO for any team over 5 people. According to your `notion__pricing-tiers.md`—or well, the public version of it—SSO is gated behind the Business tier.

00:28  **MARCO CHEN**: That is the standard packaging, yes. I can talk to @marcus.webb or @rachel.stein about a custom waiver for a smaller seat count on Business, but usually, we can't go below 30 seats for that tier. Even at 30 seats, you're still looking at ~$4,500 a month.

00:33  **HANNAH BRAKEBILL**: Yeah, even $4,500 is too high for the volume we’re doing. We’re only hitting maybe 4,000 workflow runs a month. We’re not even touching the 100k quota for Business. We’re effectively a Pro-tier customer being forced into an Enterprise-lite price point because of the SSO gate.

00:40  **MARCO CHEN**: I understand. It sounds like a mismatch between the technical requirements (SSO) and the actual usage volume. If I could get a one-time exception to add SSO to a Pro-tier plan for you, would that change the conversation?

00:45  **HANNAH BRAKEBILL**: (Pause) Probably not at this stage, Marco. To be honest, because we knew this was coming, my lead engineer already rebuilt our three most critical flows in GitHub Actions and a couple of Python scripts. We’ve already started the migration. We need a hard reset. We might come back in a year if we grow to the point where we actually need 50 seats of automation, but right now, we need to zero out the budget.

00:52  **MARCO CHEN**: I hate to hear that we're losing you to internal scripts, but I appreciate the honesty. It sounds like this was a mis-sale at the jump—we put you on a plan that was too big for the actual boots on the ground.

00:58  **HANNAH BRAKEBILL**: That’s a fair way to put it. The product is 10/10, but the pricing ladder has a massive gap between "small team" and "compliant enterprise" that we just fell through.

01:05  **MARCO CHEN**: I'm going to share this feedback directly with @dan.lee in Product. We've been discussing a "Team" tier or SSO add-ons for Pro for a while, and your case is a textbook example of why we need it. I'll process the churn for the end of April. Is there anything I can do to make the data export easier for your engineers?

01:12  **HANNAH BRAKEBILL**: No, we’re good. We’ve got the logs. Thanks for being a pro about it, Marco.

---

### Internal Notes & Follow-up

*   **Churn Reason**: Product-market fit / Pricing (specifically the "SSO Wall").
*   **Account Health**: Was technically "Engaged" per `glossary__engaged_customer.md` (8 users, >10 runs), but ROI was negative due to 50-seat minimum.
*   **Action Item**: @marco.chen to flag this in `#pricing-discuss`. This is the 4th MM account we've lost in 6 months because of the SSO/Seat-Min combo.
*   **CRM Update**: Marked as `Closed_Lost` renewal. Loss reason: `Price / Packaging`.
*   **Cross-ref**: See `notion__pricing-tiers.md` for the current SSO gating policy that Hannah referenced. This is a recurring friction point noted by @marcus.webb in Q1.
