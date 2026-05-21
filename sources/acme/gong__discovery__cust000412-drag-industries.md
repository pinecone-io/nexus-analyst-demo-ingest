---
title: "Gong call — Drag Industries (cust_000412) EBR — auto-transcript w/ small talk"
source_url: "internal://acme/gong/2026-05-08-drag-industries-ebr"
license: "synthetic-demo"
attribution: "Synthetic Gong call summary, Acme Inc internal demo. Auto-transcript exported from Gong, light cleanup."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: gong_call
---

# Gong call — Drag Industries — EBR — 2026-05-08

**Type**: Executive Business Review
**Time**: 2026-05-08, 14:00-14:48 PT
**Acme attendees**: Marco Chen (CSM), Sarah Lopez (AE), Rachel Stein (CFO — joined 14:36)
**Customer attendees**: David Anyia (VP Engineering), Priya Mehta (Sr Engineering Manager), Joon Park (Eng Director — joined late)
**Account**: `cust_000412` Drag Industries — Business / 80 seats / $11,920 MRR / renewal 2026-09-12
**Recording duration**: 00:48:13 (Gong AI summary length: ~48 min)
**Sentiment trace (Gong AI)**: Positive 64% / Neutral 28% / Negative 8%

> *Auto-extracted from Gong export. Marker timestamps preserve filler / small talk / tangents per export defaults. CSM disable-filler-extraction setting is OFF.*

---

## Transcript highlights (Gong-extracted, with original filler retained)

[00:00:08] **Marco**: Hey David, can you hear me OK?
[00:00:11] **David**: Yeah you're loud and clear. Priya is joining in a minute, she's coming from another meeting.
[00:00:16] **Marco**: All good. Sarah's here too.
[00:00:18] **Sarah**: Hi David, nice to e-meet you again.
[00:00:21] **David**: Yeah likewise. Hey how was your weekend, did you do anything fun?
[00:00:25] **Sarah**: Honestly just caught up on sleep. Had my niece's birthday party Saturday so Sunday was recovery mode. You?
[00:00:32] **David**: Same vibe. Took the kids to a soccer game. They lost 4-0 but it's fine, they had fun.
[00:00:39] **Sarah**: Haha, the important thing is fun.
[00:00:42] **Marco**: Priya just joined. Hey Priya.
[00:00:46] **Priya**: Hi everyone, sorry for the slight delay. The previous call ran over.
[00:00:51] **Marco**: No worries. OK so we have you for the next 45 min. Wanted to walk through usage data and then talk renewal options ahead of Sep 12. Sound good?
[00:01:02] **David**: Yeah works.

[00:01:08] **Marco**: First the usage. Looking at last 28 days — 11 active users out of 80 paid seats. Utilization 0.14. Workflow run volume on the eng side is healthy: ~120 runs/day average over last 6 months. So eng is using it well, the rest of the org... not so much.
[00:01:34] **David**: Yeah honestly when our RevOps lead Caroline left in March the sales-side workflows just stopped. We never replaced her so the entire RevOps automation budget is sitting unused. Eng usage is solid because that's my team.
[00:01:52] **Marco**: And how's the search for her replacement going?
[00:01:56] **David**: Painful. Trying to backfill but the RevOps job market is brutal right now. Three offers out, all ghosted us.
[00:02:08] **Sarah**: Yeah we've heard that from a few customers. RevOps hiring is wild. Have you considered an external consultant for the gap?
[00:02:18] **David**: Considered it. The CFO doesn't want to spend on a consultant when we have the RevOps headcount in budget. So we're stuck waiting.
[00:02:28] **Marco**: Got it. OK so let me ask Priya — you're more on the eng side, anything you'd want from us product-wise that would be useful?
[00:02:39] **Priya**: Honestly the platform is solid for our use case. The Stripe → Slack → Linear chain runs reliably. One thing — and I've mentioned it before — the workflow builder UI gets clunky once you're past 20 nodes. Not a deal-breaker but our biggest workflow has 31 nodes and editing it is a pain.
[00:03:02] **Marco**: Noted, I'll route that to our product team. We've actually been working on a node grouping feature, would that help?
[00:03:11] **Priya**: Maybe. I'd want to see it. When's it shipping?
[00:03:14] **Marco**: Beta in Q3, GA late Q4 most likely.
[00:03:18] **Priya**: That's far. OK noted.

[00:03:24] **Sarah**: OK transitioning to renewal. Three options to consider:
[00:03:32] First, status quo: 80 seats Business, $143K/year. You've already acknowledged you can't justify it.
[00:03:42] Second, what we'd call a custom 30-seat Business package. $4,470 MRR, $54K/year. Below our 50-seat minimum which means it needs CFO sign-off — we can do that, just calling out it's a special case.
[00:04:00] Third, drop to Pro: 11 seats × $49 = $539/month, ~$6.5K/year. You'd lose SSO and the audit log features. David — are those contractual for you guys?
[00:04:18] **David**: SSO is nice but not contractual. Audit log we could live without. The big ask from our security team is just IP allowlist which Pro has too.
[00:04:30] **Sarah**: OK so technically Pro covers your needs.
[00:04:33] **David**: Yeah but Pro feels like a step backwards. If we can do the 30-seat custom Business at $54K, that gives us room to grow back if we hire RevOps. Pro feels like waving the white flag.
[00:04:48] **Sarah**: Totally get it. Marco can you walk through what's included in the custom package?
[00:04:54] **Marco**: Yeah so 30 seats, all the Business features (SSO, audit log, etc.), same SLA, same support tier. Same MRR per seat as your current contract — $149/seat — so $4,470 MRR.

[00:05:24] **Joon Park** (joining): Hey sorry I'm late, traffic was insane. What did I miss?
[00:05:30] **David**: Just the renewal options. Quick recap: status quo, custom 30-seat Business, or drop to Pro.
[00:05:37] **Joon**: OK got it.

[00:05:42] **Priya**: Out of curiosity — and unrelated — can we get reports on who has built which workflows? Like a "top 5 builders this month" kind of leaderboard? Would help me identify which engineers are most fluent.
[00:06:02] **Marco**: We have basic creator-attribution in the workflow list view. Not a leaderboard per se. I can show you on a follow-up but probably not what you're picturing.
[00:06:14] **Priya**: OK fair enough.

[00:06:20] **David**: Question — and this is more for sarah — for the custom 30-seat thing, what does the CFO sign-off process look like in practice?
[00:06:31] **Sarah**: Pretty light. I'll loop Rachel — our CFO — in for the signature on the order form. Usually 24-48h turnaround.
[00:06:42] **Marco**: Speaking of, Rachel wanted to join the last 10 min if she could. Let me text her. (off-camera)

[00:06:52] **Joon**: Hey while we're here, totally tangent — do you guys have any plans for native PII scrubbing in workflow logs? We had a thing last quarter where a workflow accidentally logged a bunch of customer emails because someone forgot to redact a step output.
[00:07:14] **Marco**: PII scrubbing is on the roadmap, scheduled for late Q3 / early Q4. We'd add a per-step "treat output as PII" flag that auto-redacts in logs.
[00:07:28] **Joon**: That'd be huge. Even just the flag would save us a lot of manual auditing.
[00:07:34] **Marco**: Noted, I'll mention you wanted it in the customer feedback log.
[00:07:38] **Joon**: Cool thanks.

[00:07:48] (~25 min of detailed back-and-forth on the 30-seat package, AE/CSM walking through what features stay/go, Drag asking about migration timing if they downsize — Gong AI summary: customer is leaning toward the custom Business package, no objections to the price)

[00:36:14] **Rachel** (joining): Hey everyone, sorry I'm late, just wrapping up another call. Marco caught me up briefly. So you're considering the 30-seat custom Business at $54K, is that right?
[00:36:30] **David**: Yeah leaning that way.
[00:36:34] **Rachel**: OK from finance side, that's approvable. We'd need to draft a custom order form. Standard turnaround. One question — what would make Acme stickier for you guys? Like if you could wave a wand and we shipped one feature that locked you in for 3 years, what would it be?
[00:36:55] **David**: Better Salesforce CPQ integration. Our sales-ops team uses Workato now for the CPQ stuff because Acme's depth there isn't sufficient. If you had native CPQ depth, our sales-ops team would have stayed on Acme longer when Caroline left.
[00:37:18] **Rachel**: Got it. Marco — flag that as a feature request in CPQ-DEEP-2026 or whatever the current ticket is.
[00:37:25] **Marco**: Yeah, ticket exists, will add Drag's comment.

[00:37:38] **Rachel**: OK from my side I'm good. Let's get the order form moving. Sarah will follow up with the doc by end of week.
[00:37:48] **Sarah**: Yes, draft Monday.

[00:37:54] **Joon**: One more random question — do you guys have a customer Slack community? Would be cool to swap notes with other Acme power-users.
[00:38:08] **Marco**: We do! Slack Connect channel for Business+ customers. I'll add you after the call.
[00:38:15] **Joon**: Sweet.

[00:38:30] **Marco**: OK action items: I'll send a follow-up email with everything we discussed. Sarah owns the order form. Loop in Rachel for sig. Aim for renewal close by mid-July to give you breathing room before the Sep 12 actual renewal date.
[00:38:50] **David**: Sounds good.
[00:38:54] **Marco**: Anything else?
[00:38:58] **David**: No I think we're good. Thanks for the time.
[00:39:02] **Sarah**: Thanks David.
[00:39:05] (call ends, recording continues for a moment with off-camera small talk between Marco and Sarah debriefing — Gong typically auto-trims this but the recording is preserved here)

[00:39:15] **Marco** (off-camera, to Sarah): That went well. Way better than the call we had with the SDR team last quarter where they basically said they're switching.
[00:39:24] **Sarah**: Yeah. The 30-seat custom is a good middle ground. Let me get the order form on Monday.
[00:39:32] **Marco**: Cool. I'll write up the action items.

---

## Acme post-call read

- **Forecast**: most likely 30-seat custom Business at $54K ARR. Net delta vs current $143K = -$89K ARR. Logged in CRM as "downgrade likely".
- **Tail risk**: 5% chance of full churn if their CFO blocks the custom package.
- **Action items**:
  - Sarah Lopez: order form draft by 2026-05-12
  - Marco Chen: 30-day post-signature check-in
  - Dan Lee (Product): triage `CPQ-DEEP-2026` priority
  - Joon Park added to customer Slack Connect (one-off, not in standard playbook)

## Tangential mentions captured (noted for product team)

- Workflow builder UI clunky past 20 nodes (Priya). Routing to product team.
- PII scrubbing in workflow logs (Joon). Already on roadmap Q3-Q4.
- Customer power-user community / leaderboard idea (Priya). Not on roadmap.

---

**Related**: `slack__cs-at-risk__customer-cust000412.md`, `glossary__seat_utilization.md`
