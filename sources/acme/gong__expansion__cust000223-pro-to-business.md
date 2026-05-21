---
title: "Gong expansion call — cust_000223 Pro→Business upgrade"
source_url: "internal://acme/gong/expansion/cust000223-pro-to-business"
license: "synthetic-demo"
attribution: "Acme Inc Gong transcript (synthetic demo). Owner: Sales."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: gong_call
---

# Gong expansion call — cust_000223 Pro→Business upgrade

**Call Date**: 2026-04-19
**Participants**:
*   **Sarah Lopez** (Acme Account Executive)
*   **Erika Solberg** (Head of Ops, cust_000223 - "Veloce Logistics")
*   **Jin-ho Park** (Security Lead, cust_000223 - "Veloce Logistics")

**Context**: Expansion lead triggered by `dbt__model__account_health.md` (utilization > 0.90). See handoff context in `slack__cs-handoff__cust000223-expansion-flag.md`.

---

00:00 **Sarah Lopez**: Hi Erika, Jin-ho, great to see you both again. Erika, I saw the note from your CSM, Marco, that you’re bumping up against the seat limit on your Pro plan.

00:12 **Erika Solberg**: Yeah, we’ve had three more analysts join the logistics team this month, and we’re basically playing musical chairs with the logins right now. It’s not sustainable.

00:25 **Sarah Lopez**: Totally understand. Marco mentioned you’re looking at about 6 new seats immediately?

00:31 **Erika Solberg**: At least 6. But honestly, looking at our roadmap for Q3, we’ll probably need another 10-15 by August. Which is why I wanted Jin-ho on the line. If we’re going to scale this, we can’t keep managing users manually.

00:45 **Jin-ho Park**: Right. From the security side, we have a mandate to move all production-access tools behind our Okta SSO. I understand that’s a Business tier feature?

01:02 **Sarah Lopez**: Exactly. The Business tier includes SAML SSO and SCIM provisioning, which would let you automate those seat assignments directly from Okta. It also moves you from the 10k monthly run quota to 100k, which—given your current volume—you’re likely to hit by June anyway.

01:22 **Jin-ho Park**: And what about the audit logs? Our compliance team is asking for 90-day retention on workflow execution history. Pro only gives us 30, right?

01:35 **Sarah Lopez**: Correct. Business tier provides the 90-day audit log retention as standard. If you ever need unlimited, that’s an Enterprise conversation, but for most mid-market teams like Veloce, the 90-day window in Business hits the SOC2 requirement perfectly.

01:55 **Erika Solberg**: Okay, so let's talk numbers. We're on Pro at $49 a seat right now. Business is $149? That’s a significant jump for 50 seats minimum.

02:15 **Sarah Lopez**: It is a jump, but it’s a different class of service. You’re getting the SSO, the audit logs, and priority support. Plus, we can look at multi-year incentives. If we commit to a 1-year or 2-year term, I can apply the standard discounts we have in our `notion__pricing-tiers.md` guidelines.

02:40 **Erika Solberg**: What does a 2-year look like?

02:45 **Sarah Lopez**: For a 2-year commitment, we can do an 8% discount on the total ACV. Based on the 50-seat minimum for Business, that brings your annual from $89,400 down to roughly $82,248.

03:10 **Erika Solberg**: And if we need to go to 60 or 70 seats mid-contract?

03:18 **Sarah Lopez**: You’d just pay the pro-rated amount for the additional seats at that same discounted rate. We keep the unit price locked for the duration of the 24 months.

03:35 **Jin-ho Park**: Sarah, can you send over the technical docs for the SAML integration? I want to make sure there are no surprises with our Okta tenant.

03:45 **Sarah Lopez**: I'll send that over immediately after this call. It’s a standard OIDC or SAML setup. 

04:02 **Erika Solberg**: If we sign by Friday, can we get the SSO enabled before the weekend? We have a big audit starting Monday.

04:12 **Sarah Lopez**: I can make that happen. Once the contract is signed in DocuSign, I’ll coordinate with David Kim on our Engineering team to ensure the feature flags are flipped for `cust_000223` immediately.

04:30 **Erika Solberg**: Great. Send the proposal over. We’ll review the 2-year option.

04:45 **Sarah Lopez**: Perfect. I'll include the 8% multi-year discount and the SSO implementation guide for Jin-ho. Thanks everyone.
