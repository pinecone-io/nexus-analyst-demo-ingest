---
title: "Gong call — Greenfield SaaS — first demo (short, fast)"
source_url: "internal://acme/gong/2026-04-22-greenfield-saas-demo"
license: "synthetic-demo"
attribution: "Synthetic Gong call summary, Acme Inc internal demo."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: gong_call
---

# Gong call — Greenfield SaaS — demo — 2026-04-22

**Type**: Demo (first sales touch after self-serve trial)
**Time**: 2026-04-22, 13:00-13:28 PT
**Acme attendees**: Derek Lin (SDR), Sarah Lopez (AE — joined 13:15)
**Customer attendees**: Aiden Park (CTO + co-founder)
**Source**: Free tier signup 2026-04-12, clicked "talk to sales" after hitting Free quota at day 8
**Duration**: 00:28:14

---

## Transcript highlights

[00:00:04] **Derek**: Hey Aiden, can you hear me OK?
[00:00:08] **Aiden**: Yep loud and clear.
[00:00:11] **Derek**: Cool. Thanks for hopping on. So you signed up on Acme about 10 days ago and hit the Free quota — that's a healthy signal you're getting value. I want to make sure we get you on the right plan. Quick context check first — what does Greenfield SaaS do?
[00:00:30] **Aiden**: Sure. We're an early-stage startup, ~12 people, B2B inventory management for small e-comm businesses. Just closed seed last quarter.
[00:00:42] **Derek**: Cool. Congrats on the round.
[00:00:46] **Aiden**: Thanks!

[00:00:50] **Derek**: OK so what use case are you running on Acme that's hitting the Free quota?
[00:00:56] **Aiden**: We built a customer onboarding flow — Stripe webhook → Slack alert → Notion page → Linear issue if onboarding stalls. Runs on every signup. We're growing faster than expected and the Free quota stops us cold.

[00:01:12] **Derek**: Sounds like a Pro fit. 10K runs/month, no workflow limit. $49/seat/month. How many people on your team would build workflows?
[00:01:24] **Aiden**: Just me right now. Maybe one engineer joins next month.
[00:01:32] **Derek**: So $49 or $98/month at most. Doable today. Quick Q on growth — sales team coming on?
[00:01:42] **Aiden**: Yeah. Hiring 2 AEs in Q3. They'd want to use Acme for SFDC automation.
[00:01:52] **Derek**: Cool. At that point you'd be looking at 4-5 seats. Still Pro range. The jump to Business comes when you hit 50 seats or need SSO/audit.
[00:02:08] **Aiden**: Got it.

[00:02:14] **Derek**: Let me bring our AE Sarah on, she'll do the product Q&A. One sec.

[00:02:24] **Sarah** (joining): Hi Aiden!
[00:02:28] **Aiden**: Hey.
[00:02:30] **Sarah**: Derek caught me up. So you're on Free, hit quota, considering Pro. Any product questions?

[00:02:42] **Aiden**: Two main ones. (1) What happens if I hit the 10K run quota on Pro? (2) SSO — we use Google Workspace, do you support OAuth login?

[00:02:56] **Sarah**: Quota: we auto-pause the workflow that's over its share. You can either upgrade to Business (100K quota) or wait until next billing cycle. We don't charge overage. Most Pro customers stay well under 10K — your customer onboarding flow at one run per signup would need 10K signups in a month before you'd hit it.
[00:03:24] **Aiden**: OK good. We're at maybe 2K signups/month right now so we have headroom.

[00:03:32] **Sarah**: SSO: Google Workspace OAuth login is included on Pro. That's specifically the user-login OAuth, not the deeper SAML SSO + SCIM provisioning which is a Business feature.
[00:03:48] **Aiden**: Just Google login is fine for us. We're 12 people, we're not at SCIM scale yet.
[00:03:58] **Sarah**: Yeah totally fine.

[00:04:06] **Aiden**: OK let's start Pro, 1 seat. I'll add the engineer when they start.
[00:04:14] **Sarah**: You can self-serve upgrade in billing settings. Free → Pro is a 2-click flow. Want me to send you the link?
[00:04:22] **Aiden**: Yeah send it.

[00:04:26] **Sarah**: Done, check your email in like 30 seconds.
[00:04:30] **Aiden**: Cool. Anything else I should know?
[00:04:34] **Sarah**: Couple things —
[00:04:36] (1) When your engineer joins, just add them as a builder in account settings, doesn't require a sales conversation
[00:04:44] (2) When you hit 50+ seats and want to talk SSO/audit, ping us and we'll do a Business upgrade conversation
[00:04:54] (3) AI Workflow Assistant beta is available on Pro — opt in if you want to play with it
[00:05:02] **Aiden**: Yeah I'll opt in.

[00:05:08] **Sarah**: Cool. Anything else?
[00:05:12] **Aiden**: No I think I'm good.
[00:05:14] **Sarah**: Great, talk soon!
[00:05:18] **Derek**: Bye!

[00:05:22] (Aiden self-serves upgraded to Pro on the same day, ~6 minutes after the call ended. Recording continues briefly with Derek and Sarah debriefing.)

[00:05:32] **Derek** (off-camera, to Sarah): Easiest convert ever. Self-serve PLG works.
[00:05:38] **Sarah**: Yeah these are the dreams. 30-day check-in to see if engineer joined or Q3 hiring on track.
[00:05:48] **Derek**: I'll set the cal reminder.

[00:05:52] (call ends)

---

## Acme post-call

- **Stage**: Closed_Won (self-serve upgrade flow)
- **Amount**: $588 ACV (1 seat × $49 × 12)
- **Acquisition channel**: organic (Free signup → in-product upsell)
- **Action items**:
  - Sarah: self-serve upgrade link sent ✓
  - Derek: 30-day check-in cal reminder set for 2026-05-22
- **Notes**: Healthy PLG funnel motion. Sales role here was friction-reduction, not persuasion.

---

**Related**: `slack__pricing__should-we-raise-pro.md`, `glossary__seat_utilization.md`
