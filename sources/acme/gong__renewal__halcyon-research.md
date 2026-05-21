---
title: "Gong call — Halcyon Research — renewal expansion (light call, mostly happy)"
source_url: "internal://acme/gong/2026-04-15-halcyon-renewal"
license: "synthetic-demo"
attribution: "Synthetic Gong call summary, Acme Inc internal demo."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: gong_call
---

# Gong call — Halcyon Research — renewal — 2026-04-15

**Type**: Renewal expansion conversation
**Time**: 2026-04-15, 09:00-09:32 PT
**Acme attendees**: Marco Chen (CSM), Sarah Lopez (AE)
**Customer attendees**: Jordan Briggs (Head of Operations), Theo Park (Engineering Lead)
**Account**: `cust_000087` Halcyon Research — Enterprise / $150K ACV / renewal 2026-05-31
**Duration**: 00:32:18

---

## Transcript highlights

[00:00:08] **Marco**: Hey Jordan, hey Theo. Coffee level adequate?
[00:00:13] **Jordan**: Always. Good morning Marco, Sarah.
[00:00:17] **Sarah**: Morning! Thanks for making time.

[00:00:24] **Marco**: OK quick context — we're 6 weeks out from your renewal end of May. Wanted to walk through what's working, what's not, and where you see Acme fitting in for the next year.
[00:00:38] **Jordan**: Honestly easiest renewal conversation we've had. Acme has been the bedrock of our ops automation. The team has built ~90 workflows across finance, ops, and product. We use you in production every day.

[00:00:58] **Theo**: One ask: we're growing. We had 120 people at signing, we're 280 now. Are we going to bump up against any limits if we roll out Acme more broadly to engineering?
[00:01:14] **Marco**: Enterprise has unlimited workflow runs and storage. Only limits would be rate-limits on individual integrations — which is third-party (your problem, not ours, sadly). Suggest expanding seats.

[00:01:28] **Sarah**: Your current contract is 250 seats. You've used about 140 over the last quarter. Utilization 56%. Healthy with room to grow. If we expand to 400 seats now, we can hold the per-seat rate at this year's pricing for 2 more years.
[00:01:50] **Jordan**: Per-seat math: $150K / 250 = $600/seat/year. So 400 seats would be...$240K? Big jump.
[00:02:02] **Sarah**: $216K — there's a multi-year discount. And if you commit to 3 years, we can do $200K flat.

[00:02:14] **Theo**: 3 years is too long for us. 2 years feels right. Can we do 2-year at $216K?
[00:02:22] **Sarah**: Yes, can do.

[00:02:28] **Marco**: Cool. Quick switch — let me walk through what we've shipped since your last renewal. New since June 2025:
[00:02:38] - 5 new integrations including Stripe Connect and HubSpot CMS
[00:02:44] - Workflow templates library (340 templates, you can browse in-product)
[00:02:50] - AI Workflow Assistant (private beta — Halcyon would be in cohort 1 if you opt in)
[00:02:58] - Audit log v2 with deeper RBAC
[00:03:02] - Per-step PII scrubbing flag (just shipped last week)

[00:03:12] **Jordan**: We'd love AI beta. Theo, your team would be the right testers.
[00:03:18] **Theo**: Yeah willing. Caveat we'll need to validate it doesn't write PII into prompts.
[00:03:26] **Marco**: We've thought about that. The AI Assistant is built with no-prompt-PII enforcement — it doesn't accept actual customer data in the prompt, just structural intent. There's a doc, I'll send it.
[00:03:42] **Theo**: Cool.

[00:03:48] (~10 min of casual back-and-forth about other tools they use, mentions of Linear migration plans, brief tangent about Theo's team using Notion for runbooks — Gong AI summary: customer is healthy, no friction)

[00:13:34] **Jordan**: Random question — do you guys do user conferences? We'd love to send 2-3 people if you have one.
[00:13:42] **Marco**: We had our first one last fall, ~200 attendees. Next one is Sept 2026. I'll add Halcyon to the early-invite list.
[00:13:54] **Jordan**: Sweet thanks.

[00:14:02] (more casual chat, then back to renewal logistics)

[00:18:14] **Sarah**: OK to wrap: I'll send a 2-year, 400-seat order form at $216K/yr by Friday. Marco will add Halcyon to AI beta cohort 1. Halcyon will sign by mid-May to lock multi-year price.
[00:18:32] **Jordan**: Works.
[00:18:38] **Sarah**: Anything else?
[00:18:42] **Jordan**: No I think we're good.
[00:18:46] **Theo**: Thanks!

[00:18:50] (call ends. small talk continues briefly between Marco and Sarah debriefing post-call — preserved in recording per Gong defaults)

[00:19:02] **Marco** (off-camera): Easiest call ever.
[00:19:06] **Sarah**: Halcyon is a dream account. Can we clone them?
[00:19:10] **Marco**: 😂

---

## Acme post-call

- **Forecast**: 2-year, 400-seat at $216K ACV. Net change: +$66K ARR. Counts as expansion in NRR cohort.
- **Probability**: 95% close. Customer is a clear promoter (NPS Q1 was 10).
- **Action items**:
  - Sarah Lopez: order form by 2026-04-17
  - Marco Chen: AI beta cohort 1 add by 2026-04-22
  - Send PII-prompt doc to Theo (Marco)
  - Add Halcyon to user conference early-invite list (Marco)

## Tangential / contextual

- Halcyon migrating to Linear (from Jira). Watch for any related workflow migration needs.
- Theo's team uses Notion for runbooks — could be a soft entry point for our Notion integration depth in future expansion conversations.

---

**Related**: `glossary__nrr.md`, `glossary__seat_utilization.md`, `gong__discovery__nimbus-finance.md`
