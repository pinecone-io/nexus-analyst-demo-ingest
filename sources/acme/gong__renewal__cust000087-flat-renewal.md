---
title: "Gong renewal — cust_000087 flat renewal closed"
source_url: "internal://acme/gong/renewal/cust000087-flat-renewal"
license: "synthetic-demo"
attribution: "Acme Inc Gong transcript (synthetic demo). Participant: Sarah Lopez (AE)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: gong_call
---

# Gong Transcript: Halcyon Research Renewal Closing

**Date**: 2026-04-15  
**Participants**:  
- **Sarah Lopez** (Acme Account Executive)  
- **Sundara Reddy** (Engineering Lead, Halcyon Research — `cust_000087`)  
**Duration**: 22 minutes  
**Subject**: Q2 Renewal Finalization — Halcyon Research

---

00:05 **Sarah Lopez**: Hey Sundara, good to see you again. How’s the team doing over at Halcyon?

00:12 **Sundara Reddy**: Doing well, Sarah. Busy. We’re in the middle of a big migration for our data pipelines, so the timing of this renewal is... well, it's on the list, let's put it that way.

00:24 **Sarah Lopez**: I appreciate you carving out the time. I know we’ve been back and forth on the terms for a few weeks. I wanted to jump on and see if we could get the signatures across the line today so you can get back to that migration.

00:38 **Sundara Reddy**: Yeah, I saw the updated proposal you sent over this morning. 

00:42 **Sarah Lopez**: Great. To recap, we’re looking at a 12-month renewal on the Business tier. We’re keeping you at the same 50-seat count you’ve been at for the last year. That keeps the ARR flat at $89,400. 

00:55 **Sundara Reddy**: Right. Flat. Which, to be honest, was a bit of a debate internally. 

01:02 **Sarah Lopez**: I wanted to touch on that. I know you’ve been a huge advocate for us, but I noticed the NPS score from your side dipped recently—I think it went from a 9 down to a 5 in the last survey. I saw some of the notes in the Slack thread with our CSM, Marco. Is there something specific we can address?

01:18 **Sundara Reddy**: It’s not the core platform, Sarah. The workflows are stable. We’re running about 15,000 successful runs a month, and that’s been great for our GSheets-to-Salesforce syncs. The frustration—and why the score dropped—is really about the AI Workflow Assistant. 

01:35 **Sarah Lopez**: The beta?

01:37 **Sundara Reddy**: Exactly. When we talked in January, there was a lot of excitement about using the AI Assistant to help our non-technical analysts build their own flows. But it’s still in beta, and my team is still having to do all the heavy lifting. We were hoping it would be GA by now. Without that self-serve piece, it’s hard for me to justify expanding the seat count or committing to a multi-year deal.

01:58 **Sarah Lopez**: I completely hear you. I actually checked in with @dan.lee in Product this morning. The AI Assistant is still in active beta—we’re refining the PII scrubbing flags specifically for the Business tier right now. We’re targeting a broader rollout in H2, but I don't want to over-promise on the GA date today.

02:15 **Sundara Reddy**: And that’s why we’re staying flat. My VP asked why we weren't looking at the 2-year discount you mentioned—the 8% off—but I can’t lock us in for 24 months if the roadmap for the AI features is still shifting. 

02:30 **Sarah Lopez**: That’s fair. We’d love to get you that 8% discount, but I understand the need for flexibility. If we stick to the 12-month flat renewal at $89,400, does that give you the breathing room to see how the H1 product updates land?

02:45 **Sundara Reddy**: It does. We like the tool, Sarah. It’s core to our ops. We just need to see the "Assistant" actually assist before we double down.

02:55 **Sarah Lopez**: Understood. I’ve made a note for @marco.chen to prioritize your team for the next round of beta feedback sessions. We want your input on those PII flags since I know Halcyon is strict on data privacy.

03:10 **Sundara Reddy**: That would actually be very helpful. If we can get our hands on the updated scrubbing features sooner, it might change the conversation for the Q4 review.

03:20 **Sarah Lopez**: Perfect. I’ll send over the DocuSign for the $89.4K Business renewal right after this call. It’s the standard terms we’ve used previously. 

03:32 **Sundara Reddy**: Send it over. I’ll get it signed before my 4 PM.

03:38 **Sarah Lopez**: Thanks, Sundara. I’ll also make sure the `account_health_status` is updated in our system to reflect the roadmap concerns so we don't keep bugging you about expansion until those features ship.

03:50 **Sundara Reddy**: (Laughs) I appreciate the honesty. Talk soon, Sarah.

04:00 **Sarah Lopez**: Take care.

---

### Internal Notes (Post-Call)
- **Outcome**: Closed Won (Renewal).
- **ARR**: $89,400 (Flat).
- **Term**: 12 Months.
- **Key Blocker for Expansion**: AI Workflow Assistant GA delay.
- **Sentiment**: Customer is "Stable" but "At Risk" for expansion until AI features land. See `notion__csm-account-health-runbook.md` for the "At Risk" outreach ladder if usage dips.
- **Cross-ref**: `slack__cs-at-risk__cust000087-renewal-amber.md` for historical context on the NPS drop.
- **Action Item**: @sarah.lopez to update `fact_opportunities` to `Closed_Won`. @marco.chen to schedule a roadmap deep-dive with Sundara in late May.
