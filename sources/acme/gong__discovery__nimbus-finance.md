---
title: "Gong call — Nimbus Finance — discovery (with rabbit holes)"
source_url: "internal://acme/gong/2026-04-29-nimbus-finance-discovery"
license: "synthetic-demo"
attribution: "Synthetic Gong call summary, Acme Inc internal demo."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: gong_call
---

# Gong call — Nimbus Finance — discovery — 2026-04-29

**Type**: Discovery (first call after inbound demo request)
**Time**: 2026-04-29, 11:00-11:38 ET
**Acme attendees**: Sarah Lopez (AE), Ben Cohen (Sales Engineer)
**Customer attendees**: Linda Chen (Director of RevOps), Trevor Singh (Salesforce Admin)
**Source**: Inbound via blog post `ai-workflows-launch` (utm_source=blog / utm_medium=organic)
**Duration**: 00:38:42

---

## Transcript highlights

[00:00:04] **Sarah**: Hi Linda, hi Trevor. Can you both hear me?
[00:00:08] **Linda**: Yep loud and clear.
[00:00:10] **Trevor**: Yep.
[00:00:12] **Sarah**: Awesome. Ben here is our solution engineer, he'll handle the deeper technical questions. So before we dive in — Linda, how's your week going?
[00:00:24] **Linda**: Honestly chaotic. We're closing the books for the quarter so I've been in spreadsheets all morning. Glad to step away.
[00:00:34] **Sarah**: Oh god, end of quarter close, my condolences. Trevor what about you?
[00:00:39] **Trevor**: Yeah trying to make the books not lie, mostly.
[00:00:43] **Sarah**: Haha. Fun for the whole family.

[00:00:50] **Sarah**: OK so I'd love to start by hearing what brought you to Acme — what problem you're trying to solve.
[00:01:00] **Linda**: Sure. So we're a fintech, ~600 employees, pre-IPO. We currently use Workato for workflow automation. We have ~40 production workflows on Workato. Pricing has tripled in 3 years. Our contract is up Q3 2026 and we're evaluating alternatives. We want to consolidate vendors and pay less, but can't lose any production workflows.
[00:01:32] **Sarah**: Got it. What was the trigger for evaluating alternatives — the pricing alone, or something else?
[00:01:42] **Linda**: Pricing primarily. But also their support has been... mediocre. We had a P1 outage in February that took 6 hours to get a meaningful response.
[00:01:55] **Sarah**: Oof.

[00:02:02] **Sarah**: OK can you walk us through your top 5 critical workflows? Just want to scope what would need to migrate.
[00:02:10] **Trevor**: Sure. (1) Stripe → SFDC → Slack alert for new customer wins, (2) Marketo → SFDC lead sync, (3) Salesforce-to-Snowflake replication for analytics team, (4) Zendesk → SFDC ticket sync, (5) HubSpot → Marketo audience sync.
[00:02:36] **Ben**: OK 1, 2, and 4 — those are native Acme templates. We can show you those in 5 minutes. #3 needs a Snowflake connector check, we have a Snowflake step but I'd want to verify your specific use case. #5 we have HubSpot and Marketo connectors so it's doable.
[00:03:00] **Trevor**: One thing I'm worried about — Workato has been auto-retrying with exponential backoff for us, which is critical because Stripe rate-limits us hard during EOM batches. Does Acme do that?
[00:03:18] **Ben**: Yeah, rate-limit handling is built into our HTTP step. Configurable retry count + backoff strategy. We surface a `RATE_LIMITED` error code on the run if we exhaust retries. Customer can monitor in their dashboard or via webhook.
[00:03:36] **Trevor**: OK that's table stakes for us. Glad you have it.

[00:03:42] **Linda**: Tangent — and this is more market intelligence — do you guys have a stance on the AI workflow generation thing? Workato just announced their AI builder thing.
[00:04:00] **Sarah**: Yeah, our AI Workflow Assistant is in private beta right now. Prompts to workflow generation. We can demo it during the POC if you want to evaluate that side-by-side.
[00:04:14] **Linda**: That'd be huge actually. The promise of AI-built workflows is a huge ROI driver for us if it actually works.
[00:04:24] **Sarah**: We can get you in the beta cohort, ya. Caveat: it's beta, expect some rough edges.

[00:04:38] **Trevor**: One more random Q — your pricing for enterprise is custom right? What's the typical range for a company our size?
[00:04:50] **Sarah**: For a company at 600 employees with ~50 workflow builders, you'd be on Enterprise. Typical ACV for a company your size is $80-150K. Specifics would come after a scoping call with our solution architect.
[00:05:10] **Linda**: Workato is asking for $220K next year. If you can do $100-130K with feature parity I'd push internally. We'd need a 60-day POC starting in June.
[00:05:28] **Sarah**: 60-day POC is standard for our enterprise prospects. Free, hands-on solution-architect support during the POC. We'd lock success criteria upfront — basically "if Acme can replicate Workato workflow X in Y days at Z performance, you'll buy".
[00:05:50] **Linda**: That's a sane structure.

[00:05:58] (Ben gives a 12-min product demo of templates 1, 2, 4 — Gong AI extracted highlights below)

[00:18:04] **Ben**: That's the rough flow. Any questions?
[00:18:10] **Trevor**: The error handling looks better than Workato's actually. The retry config UI is cleaner. Does the timeout config work on a per-step basis or just per-workflow?
[00:18:24] **Ben**: Per-step. You can override the workflow-level timeout for specific steps. Useful for slow third-party APIs.
[00:18:36] **Trevor**: Nice.

[00:18:48] **Linda**: OK can we talk about migration. If we go with you guys, what's the realistic timeline to migrate ~40 workflows?
[00:19:04] **Ben**: Depends on complexity but for the kind of workflows you described, I'd estimate 4-8 weeks of focused work for one engineer. Our SA can pair with your team for the first 2-3 weeks to accelerate.
[00:19:24] **Linda**: 4-8 weeks. That's reasonable.

[00:19:32] **Trevor**: Random question — does Acme have any kind of API to programmatically deploy workflows? We use Terraform for everything else.
[00:19:48] **Ben**: We have a public API, yes. There's a community-maintained Terraform provider — not officially supported but it works. We're considering bringing it in-house in 2026-H2.
[00:20:08] **Trevor**: Good enough.

[00:20:18] (Sarah and Linda discuss next steps)

[00:20:32] **Sarah**: OK so action items: Ben will send a Workato → Acme migration template + Snowflake connector spec by Friday. Linda, you'll align internally and confirm the top-5 workflow detail by next Friday May 9. Then I'll schedule the POC kickoff with our SA for June 1.
[00:21:00] **Linda**: That works.

[00:21:08] (call ends with mild small talk about the upcoming SaaStr conference — both Linda and Sarah will be attending)

---

## Acme post-call assessment

- **Stage move**: Prospecting → Qualified
- **Forecast amount**: $110K ACV (mid-point of stated range)
- **Forecast close date**: 2026-08-15 (pre-Workato renewal, with buffer)
- **Risk factors**:
  - Workato may discount aggressively to retain. Trevor signaled willingness to move; Linda is the budget owner.
  - Salesforce-CPQ depth may come up later (Linda hasn't asked but pre-IPO fintechs often need it). Watch for this in the POC.
- **Competitive**: Workato (incumbent), Zapier (mentioned offhand)
- **Action items**:
  - Ben: migration template + Snowflake spec by 2026-05-02
  - Sarah: POC kickoff scheduled for 2026-06-01
  - Linda: top-5 workflow detail by 2026-05-09

## Tangential / market intel

- Workato support quality is a pain point for Nimbus (P1 took 6h). Useful sales narrative for similar prospects.
- AI Workflow Assistant beta is a strong differentiator vs Workato's similar feature.
- Terraform deploy support is increasingly table-stakes for enterprise prospects. Reaffirms the H2 priority.

---

**Related**: `notion__enterprise-poc-playbook.md`
