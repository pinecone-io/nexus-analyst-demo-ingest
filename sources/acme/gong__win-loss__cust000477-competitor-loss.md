---
title: "Gong win-loss debrief — cust_000477 lost to competitor"
source_url: "internal://acme/gong/win-loss/cust000477"
license: "synthetic-demo"
attribution: "Acme Inc Gong transcript (synthetic demo). Internal use only."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: gong_call
---

# Gong Win-Loss Debrief: cust_000477 (Polaris Labs)

**Date**: 2026-03-18
**Participants**:
*   **Acme**: @sarah.lopez (AE), @marcus.webb (VP Sales)
*   **Polaris Labs**: Helena Marquez (VP Engineering)
**Opportunity ID**: `opp_000477`
**Stage**: Closed_Lost
**Loss Reason**: Competitor (Tray.io)

---

00:00  **SARAH LOPEZ**: Helena, really appreciate you taking 15 minutes for this. I know the team is already moving forward with the other vendor, but we take these retros seriously to figure out where we’re missing the mark.

00:45  **HELENA MARQUEZ**: Of course, Sarah. You and the team were great throughout the process. It wasn't an easy call, but for our specific stage right now, the other platform just aligned better with our immediate infra requirements.

01:12  **MARCUS WEBB**: Helena, Marcus here. Thanks again. Just to dive right in—was there a specific "aha" moment for the other team, or was it a death by a thousand cuts on our side?

01:35  **HELENA MARQUEZ**: It was a few things. First, the POC. You guys have a very strict "no-free-POC" policy for Business tier, and we were right on that 60-seat line. Tray offered us a 30-day sandbox with full feature parity, no credit card, no commitment. My engineers spent two weeks in there building actual production-ready flows before we even saw a contract.

02:15  **SARAH LOPEZ**: That’s helpful. I know we pushed the "self-serve Pro trial" as a proxy for the POC, but I'm guessing that didn't cut it for the security team?

02:30  **HELENA MARQUEZ**: Exactly. Pro doesn't have SAML or SCIM. My security lead, Dave, basically vetoed the Pro trial because he didn't want 60 engineers creating manual logins with Google OAuth. Tray had SAML working in the POC on day two. We’ve talked about this—Acme’s "SSO is only for Business/Enterprise" gate is a real friction point for mid-market engineering teams.

03:45  **MARCUS WEBB**: We hear that. It’s a frequent topic in our pricing committee. (See `notion__pricing-tiers.md` for the internal debate on this). If we had bundled SAML into a lower tier or a custom POC, would that have changed the math?

04:10  **HELENA MARQUEZ**: It would have kept you in the running longer. But the other big piece was the 3-year outlook. You guys quoted us $149/seat with a 10% discount for a 2-year commit. Tray came in with a 3-year aggressive ramp: year one was heavily discounted to offset our migration costs, and year three was capped at a 3% increase.

05:20  **SARAH LOPEZ**: So it was a combination of the "land" being easier with the free POC and the "expand" being more predictable with their multi-year terms?

05:45  **HELENA MARQUEZ**: Precisely. And honestly, the SCIM provisioning. We’re growing from 200 to 500 people this year. I can’t have my Ops team manually de-provisioning Acme users. You guys told us SCIM was "Enterprise only" (250 seat min), and we just aren't there yet. We needed Enterprise features at a Business scale.

07:10  **MARCUS WEBB**: That’s a fair critique. We’ve seen a few MM deals lately where the feature gap between Business and Enterprise—specifically around governance like SCIM—is causing us to lose to more flexible incumbents.

08:30  **HELENA MARQUEZ**: To be fair, your UI is 10x better. My builders actually preferred the Acme canvas. If you had the governance features at our price point, we probably would have paid the premium. But I can't trade security for a prettier UI right now.

09:15  **SARAH LOPEZ**: One last question, Helena. Was there anything in the technical discovery where we fell short? Any specific integration?

09:40  **HELENA MARQUEZ**: No, the integrations were solid. Your Snowflake connector is actually faster than theirs. It really came down to the "Enterprise-lite" requirements—SAML, SCIM, and a POC that didn't require me to go to Finance for a $5k "pilot fee" before we knew it worked.

11:00  **MARCUS WEBB**: Understood. This is gold for our product and pricing teams. We’re actually looking at a "Team" tier or a "Governance Add-on" for Business (see `notion__pricing-tiers.md` drafts). Sorry we missed you this time, but we'll be checking back in 12 months to see how that Tray implementation is treating you.

12:30  **HELENA MARQUEZ**: Please do. I suspect we’ll outgrow their support model eventually. Good luck, Sarah.

13:00  **SARAH LOPEZ**: Thanks, Helena. Talk soon.

---

### Post-Call Notes & Action Items

*   **Loss Analysis**: Confirms the trend identified in `notion__enterprise-poc-playbook.md`—competitors are using free, high-feature POCs to bypass our "Pro-trial-first" motion.
*   **Product Gap**: SCIM and SAML are increasingly "must-haves" for companies with >50 seats, even if they don't meet our "Enterprise" (250+ seat) definition.
*   **Pricing Strategy**: Competitor is using "Year 1" migration credits to win the initial contract. @lina.cho — we should model a "Migration Credit" discount for MM deals >$50k ARR.
*   **Follow-up**: Set task for @sarah.lopez to ping Helena in Jan 2027 for a "Year 1" check-in.

**Internal Tags**: #loss-debrief #competitor-tray #pricing-friction #SSO-gate #SCIM
