---
title: "Gong call — Beacon Studios — exit interview (raw, with awkward moments)"
source_url: "internal://acme/gong/2026-02-15-beacon-studios-exit"
license: "synthetic-demo"
attribution: "Synthetic Gong call summary, Acme Inc internal demo."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: gong_call
---

# Gong call — Beacon Studios — exit interview — 2026-02-15

**Type**: Churn / exit interview
**Time**: 2026-02-15, 16:00-16:27 ET
**Acme attendees**: Rajiv Patel (Sr CSM), Elena Volkov (VP CS — joined 16:18)
**Customer attendees**: Olivia Thatcher (VP Operations), Marcus Liu (Procurement)
**Account**: `cust_000287` Beacon Studios — Business / 65 seats / $9,685 MRR ($116K ARR), churned 2026-02-18
**Duration**: 00:27:44

---

## Transcript highlights

[00:00:06] **Rajiv**: Hi Olivia, hi Marcus. Thanks for making time for this. I know exit interviews aren't anyone's favorite call.
[00:00:18] **Olivia**: Honestly Rajiv, we've been dreading it too. This isn't fun for us either.
[00:00:24] **Rajiv**: Just want to be upfront — we're not here to save the deal. The decision is made and we respect that. Just trying to learn from it.
[00:00:36] **Olivia**: Appreciated. OK what do you want to know.

[00:00:44] **Rajiv**: First, can you walk me through how the decision came about?
[00:00:50] **Olivia**: Sure. Just to set context — this is NOT a product decision. We love Acme. NPS 9 last quarter from me personally. The decision came from procurement at the parent company level.
[00:01:08] **Marcus**: Right. Parent signed a 3-year master agreement with Tray as part of an enterprise platform bundle. The ROI math at the parent level required all subsidiaries to consolidate vendors. We didn't have leverage.
[00:01:30] **Rajiv**: When did you find out?
[00:01:33] **Marcus**: Two weeks ago. Procurement was in conversations for ~6 months but didn't loop us in. Found out via the master agreement announcement.
[00:01:48] **Rajiv**: Oof.
[00:01:50] **Olivia**: Yeah.

[00:01:56] **Rajiv**: Standard question — anything we could have done? Pricing, features, anything?
[00:02:04] **Olivia**: Honestly no. The bundled deal at the parent level included CRM, support, BI, AND ops platforms. Tray was the workflow piece. Parent procurement team didn't even ask us about Acme — we found out 2 weeks ago.
[00:02:24] **Marcus**: Even if you had matched on pricing, the parent's strategic decision was about consolidation not best-of-breed.

[00:02:36] **Rajiv**: Got it. Any feature gaps that gave Tray the edge in the parent's evaluation, that you know of?
[00:02:44] **Olivia**: I don't know directly — we weren't in those evaluation calls. Rumored to be deeper Salesforce CPQ integration and more enterprise-friendly contract terms with volume bundling.
[00:03:00] **Marcus**: The volume bundling thing was apparently big. Tray could discount across all 7 subsidiaries as a single buy. None of the individual subsidiaries used Tray before this.

[00:03:14] **Rajiv**: Ugh. That's a hard one to compete with.

[00:03:22] (~14 min of detailed discussion: Olivia walking through the timeline of finding out, Marcus answering procurement questions, Rajiv asking about migration plans for Beacon Studios specifically — Gong AI summary: customer reaffirms it's a clean separation, no bad blood, willing to be a reference if they ever return)

[00:17:34] **Olivia**: One thing I want to flag — the exit experience matters to me even though we're leaving. Your offboarding process so far has been clean. Marco-the-CSM was extremely professional even when I told him last week. I don't want this to come across as our team being checked out, we genuinely appreciate the relationship.
[00:17:58] **Rajiv**: Thank you. That means a lot.

[00:18:08] **Elena** (joining): Hey Olivia, Marcus, sorry I'm late. Rajiv caught me up briefly. Just wanted to introduce myself — I'm Elena, our VP of Customer Success.
[00:18:24] **Olivia**: Hi Elena, nice to meet you.
[00:18:28] **Elena**: I want to thank you both for the candor. Couple things from our side: (1) we'll honor the data export window for the full 90 days, (2) if anything breaks during your migration, we're happy to help even though you're not paying us anymore — just ping Rajiv. (3) If the Tray bundle goes badly and you have a chance to bring back ancillary tools, we'd love a conversation.
[00:19:02] **Olivia**: Appreciated. Honestly the chance of returning is small but I'll keep your card.

[00:19:14] **Marcus**: Practical question — for the data export, we'd want our workflow definitions exported in JSON. Is that part of the standard offboarding?
[00:19:24] **Rajiv**: Yes, JSON workflow defs + run history CSVs. There's a self-serve export in account settings under "Offboarding".
[00:19:38] **Marcus**: Cool.

[00:19:48] **Elena**: One last ask — would you be willing to be a reference customer if you ever return? Total long-shot but we'd love to keep the door open.
[00:20:02] **Olivia**: Yeah I'd opt in. Marketing-permission-wise, mark me as "reference if returns". Low likelihood but never know.

[00:20:18] (call wraps, small talk about a conference Olivia is attending in March — Rajiv mentions Acme will be there, light "see you in the wild" type chat)

[00:20:48] (call ends)

---

## Acme post-call read

- **Loss reason taxonomy**:
  - Primary: `competitor` (Tray, parent-level consolidation)
  - Secondary: `feature_gap` (Salesforce CPQ depth — corroborates other accounts mentioning this)
- **Preventability**: NOT preventable at the CSM level. Driven by parent-company procurement decision.
- **Actions**:
  - Feature request `CPQ-DEEP-2026` reinforced — 5+ accounts now mention CPQ depth
  - Sales-Ops adding "competitor enterprise consolidation" as a watch signal in account 360
  - Olivia opted in as "reference if returns" — marked in CRM
- **Final invoice**: paid in full, no proration
- **Data export**: customer retained 90-day rights (standard)

## Honest reflection (Rajiv's note in CRM)

> Beacon was a great account. Engagement healthy, NPS strong, CSM relationship solid. We lost them to a procurement decision that had nothing to do with us. The kind of loss you can't really mitigate against — short of changing the entire pricing model to match enterprise master-agreement vendors, which we're not willing to do. Filing this in the "wins to learn from anyway" bucket: parent-company consolidation risk needs to be on our radar for any account whose parent has signed with a competing platform.

---

**Related**: `slack__cs-handoff__cust000287-churn-debrief.md`, `glossary__logo_churn.md`
