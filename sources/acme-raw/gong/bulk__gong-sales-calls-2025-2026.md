---
title: "Gong export — Acme sales calls 2025–2026 (bulk transcript dump)"
source_url: "internal://acme/gong/2025-2026-sales-calls-bulk"
license: "synthetic-demo"
attribution: "Synthetic Gong export, Acme Inc internal demo. Acme Inc is fictitious."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: gong_call
---

# Acme — Gong sales calls bulk export — 2025–2026

> *Bulk auto-export from Gong. Many calls concatenated, lightly cleaned. Marker timestamps preserve filler / small talk / tangents per export defaults. Speaker attribution is Gong's best guess; occasionally wrong on crosstalk. Gong AI summary lines are inlined where the export tool emitted them.*
> *Scope: discovery, enterprise POC, pricing negotiation, renewal, expansion, win/loss. Date range 2025-02 .. 2026-05. account_id shown in each header where the call mapped to a CRM account; net-new prospects pre-account-creation show the opportunity name only.*

---

## Gong call — Cobalt Systems — discovery — 2025-03-04

**Type**: Discovery (first call, outbound-sourced by SDR)
**Time**: 2025-03-04, 09:00–09:41 GMT
**Acme attendees**: Tom Becker (AE), Ben Cohen (Sales Engineer)
**Customer attendees**: Henrik Sørensen (Head of RevOps), Aisha Malik (IT Security Lead)
**Account**: `cust_000700` Cobalt Systems — Business / 80 seats / £/$11,920 MRR / EMEA / fintech (account created post-call)
**Source**: Outbound sequence `emea-fintech-q1-2025`, SDR booked
**Duration**: 00:41:12
**Sentiment trace (Gong AI)**: Positive 51% / Neutral 41% / Negative 8%

[00:00:05] **Tom**: Morning Henrik, morning Aisha. Can you hear me OK? I think I'm coming through.
[00:00:09] **Henrik**: Yeah you're clear. Bit of an echo but fine.
[00:00:13] **Tom**: Cool. Ben's on with me, he's our solutions engineer, he'll take the technical stuff. So — first off, thanks for taking the call. I know an outbound email isn't the most romantic way to meet.
[00:00:26] **Henrik**: Ha. No, your SDR — was it Jordan? — was persistent but not annoying. Good ratio.
[00:00:33] **Tom**: I'll pass that on, he'll be thrilled. How's Copenhagen this week?
[00:00:38] **Henrik**: Grey. It's always grey. We don't talk about it.
[00:00:42] **Tom**: Fair enough. OK so I did a bit of homework — you're a fintech, payments infrastructure mostly, around what, 400 people?
[00:00:52] **Henrik**: 430 now. Growing. We just opened a London office.
[00:00:57] **Tom**: Nice. So what's the automation picture today? What are you running on?
[00:01:04] **Henrik**: Honestly a mess. We have some stuff on Zapier from the early days, which is fine for the marketing team but completely falls over at our volume on the ops side. Then we have a couple of internal cron jobs that a former engineer wrote that nobody fully understands. And then Make for one specific flow that the finance team set up without telling anyone.
[00:01:30] **Tom**: The classic shadow-automation situation.
[00:01:33] **Henrik**: Exactly. I want to consolidate. Right now if a workflow breaks at 2am, nobody knows until a customer complains.
[00:01:42] **Ben**: That's actually one of the things we do well — observability. Every run logs status, duration, and an error code if it fails. You can alert on failures. So a 2am break becomes a Slack ping at 2:01, not a customer email at 9am.
[00:01:58] **Henrik**: That alone would be worth it.
[00:02:04] **Tom**: Let me understand the scale. How many people would actually be building or touching workflows?
[00:02:11] **Henrik**: Builders, maybe 15 to 20. But people who'd want visibility — read access, see the dashboards — more like 70, 80. Ops, finance, parts of eng.
[00:02:24] **Tom**: OK that's useful. So just to set expectations on how we price — we have a few tiers. There's a Pro tier at $49 a seat a month, which is really for small teams, has a 10K runs a month cap. Then Business at $149 a seat, minimum 50 seats, which gets you SSO, audit logging, priority support, 100K runs a month. And then Enterprise which is custom, for the really large deployments — unlimited runs, dedicated CSM, SOC2 reports, custom SLA.
[00:02:56] **Henrik**: At 80 seats we'd be Business then.
[00:03:00] **Tom**: Yeah, Business fits you well. The 50-seat minimum isn't a problem at your size. Pro you'd blow through the run cap and you'd lose SSO which I'm guessing is a hard requirement for a fintech.
[00:03:14] **Aisha**: SSO is non-negotiable. We're SAML everywhere. Okta.
[00:03:19] **Ben**: We support SAML SSO via Okta on Business and up. SCIM provisioning too if you want auto-deprovisioning when someone leaves.
[00:03:28] **Aisha**: SCIM is good. That's been a gap with the Zapier setup — people leave and their connections just sit there.
[00:03:36] **Tom**: Yeah, orphaned connections are a real security issue. With SCIM we deactivate the seat and the workflows they own get flagged for reassignment.
[00:03:46] **Aisha**: OK. I have a longer list of security questions but I don't want to derail the call. Can we do a separate security review?
[00:03:54] **Tom**: Absolutely, that's standard. We have a security review track — SOC2 Type II report, pen test summary, DPA, the whole package. Ben can set up a call with our security folks. For a fintech we'd expect a thorough review and we're ready for it.
[00:04:10] **Aisha**: Good. Send me the SOC2 report under NDA and I'll start there.
[00:04:16] **Ben**: Will do. We're SOC2 Type II, audited annually. I'll get you the latest report and our security questionnaire pre-filled — saves you typing.
[00:04:26] **Aisha**: Pre-filled questionnaire, bless you. I hate those.
[00:04:30] **Tom**: Everyone does.

[00:04:38] **Henrik**: Let me ask about the comparison. We looked at Tray briefly. And obviously Zapier and Make we already use. What's the honest pitch for why you over Tray?
[00:04:50] **Tom**: Honest pitch. Tray is powerful, genuinely. It's also expensive and it has a steep learning curve — you kind of need a Tray specialist. Our bet is that you want your existing ops and eng people to build workflows without a dedicated platform team. We're more opinionated, fewer footguns, faster to value. If you have a team of integration specialists who live and breathe this stuff, Tray might suit you. If you want your RevOps and finance people self-serving, that's us.
[00:05:20] **Henrik**: We do not have integration specialists. We have an overworked RevOps team and me.
[00:05:26] **Tom**: Then I think we're a good fit. But I'd rather you prove it than take my word for it.
[00:05:32] **Henrik**: Agreed.

[00:05:40] **Ben**: Can I ask what your top workflows would be? The ones that, if we nailed them, you'd be sold?
[00:05:47] **Henrik**: Three. One — payment failure → Slack alert to the ops channel with the customer context pulled from our internal API. Two — daily reconciliation export from Stripe into our data warehouse, BigQuery in our case. Three — when a deal closes in Salesforce, kick off a provisioning flow that creates the customer in three internal systems.
[00:06:14] **Ben**: OK. One and three are bread and butter — Slack, Stripe, Salesforce are all native connectors, and the internal-API calls are just HTTP steps with auth. Two — BigQuery — we have a BigQuery connector, you'd authenticate with a service account, and we can schedule the export. The Stripe reconciliation logic itself you'd build as steps, but the plumbing is there.
[00:06:38] **Henrik**: That's exactly the three I'd want to see in a trial.
[00:06:42] **Tom**: So let's do that. I'd propose a hands-on trial — not enterprise-POC scale since you're Business-tier, but Ben can spin you up a Business trial workspace and pair with your RevOps person to build those three. Two weeks. If they run reliably, we talk contract.
[00:07:00] **Henrik**: Two weeks is fine. Who's the RevOps person — I'll assign Mette, she's our most technical.
[00:07:07] **Ben**: Perfect. I'll set up the trial workspace today and send Mette an invite. I'll also throw in our Stripe and BigQuery template docs.

[00:07:20] **Aisha**: Quick one before I drop — data residency. Where does our data live? We have some EU residency obligations.
[00:07:30] **Ben**: Good question. Our primary is US, but we have an EU data region — Amsterdam — for exactly this. EU customers can be provisioned in the EU region so workflow data and logs stay in-region. I'll confirm the specifics in the security review but yes, EU residency is supported.
[00:07:50] **Aisha**: That's a relief. That was going to be a blocker otherwise.
[00:07:55] **Tom**: Noted as a requirement: EU data region. We'll make sure your workspace is provisioned in Amsterdam.

[00:08:04] (Ben gives an ~18 min live demo: payment-failure Slack alert built live, then the Stripe→BigQuery scheduled export. Gong AI summary: prospect reacted positively to the live-build speed; Henrik commented "that took you four minutes, that's a half-day in Zapier"; Aisha satisfied with the audit-log demo. One stumble — the BigQuery service-account auth needed a permission Ben didn't have in the demo project, deferred to follow-up.)

[00:26:30] **Henrik**: That was genuinely impressive. The speed is the thing. OK what are next steps and what's this going to cost me roughly?
[00:26:40] **Tom**: Rough math: 80 seats at $149 is $11,920 a month, so about $143K a year at list. That's list — for an annual commit we have some flexibility, and I'd want to understand your timeline before we talk discount. But that's the ballpark.
[00:27:00] **Henrik**: $143K list. Zapier-plus-Make-plus-the-cron-mess is costing us maybe $30K but it doesn't do what we need and it's a liability. So the number isn't crazy if it actually consolidates everything.
[00:27:16] **Tom**: That's the framing I'd use internally — it's not Zapier replacement cost, it's the cost of not having 2am outages and shadow automation. But let's let the trial prove it.
[00:27:28] **Henrik**: Agreed. Let's do the trial.

[00:27:36] **Tom**: Action items. Ben sets up the Business trial workspace today, invites Mette, sends Stripe + BigQuery templates, and fixes the service-account auth thing for a follow-up demo. Aisha gets the SOC2 report and pre-filled questionnaire under NDA. I'll send a recap and we'll reconvene in two weeks to review the trial. Sound right?
[00:27:54] **Henrik**: Sounds right.
[00:27:57] **Aisha**: Works. Sending you my NDA template now.
[00:28:02] **Tom**: Great, thanks both. Talk soon.
[00:28:05] (call ends; ~30s of Tom and Ben debriefing off-camera retained: Ben — "the EU region thing nearly blindsided me, good thing we have it"; Tom — "fintech, always ask residency first next time")

---

## Acme post-call read (Gong + AE notes)

- **Stage**: New → Discovery complete, trial agreed.
- **Account**: `cust_000700` Cobalt Systems, Business-tier, ~80 seats, EMEA/fintech, outbound-sourced. CSM will be Marco Silva on close; AE Tom Becker.
- **Forecast**: ~$143K list, expect 10–15% annual-commit discount → ~$120–130K ACV. Note: this lands in `bookings_attribution.bookings_acv_usd` on close-won, already annualized — do not multiply by 12 in the commit model.
- **Requirements**: SAML SSO (Okta), SCIM, EU data residency (Amsterdam region), SOC2 Type II under NDA.
- **Competitive**: incumbent is Zapier + Make + homegrown cron; evaluated Tray but no integration-specialist headcount.
- **Risk**: security review is the gate. Fintech, thorough. Ben to drive.
- **Action items**: Ben — trial workspace + templates + service-account fix; Aisha — SOC2 + questionnaire under NDA; Tom — recap, reconvene in 2 weeks.

---

## Gong call — Marigold Health — enterprise POC kickoff — 2025-06-11

**Type**: Enterprise POC kickoff
**Time**: 2025-06-11, 13:00–14:05 ET
**Acme attendees**: Sarah Chen (AE), Ben Cohen (Sales Engineer), Priya Anand (VP Eng — joined 13:40 for security questions)
**Customer attendees**: Dr. Naomi Feldstein (VP Data Platform), Carlos Reyna (Staff Integration Engineer), Theo Novak (Director of Clinical Ops — internal champion), Wendy Oduya (InfoSec)
**Account**: `cust_000701` Marigold Health — Enterprise / 300 seats / $15,000 MRR ($180K ACV) / NA-East / healthtech / partner-sourced
**Source**: Partner referral (SI partner `Lumen Integration Partners`)
**Duration**: 01:05:22
**Sentiment trace (Gong AI)**: Positive 58% / Neutral 35% / Negative 7%

[00:00:06] **Sarah**: Hi everyone. I see Naomi, Carlos, Theo. Wendy I think you're joining? OK there you are. Can everyone hear me?
[00:00:14] **Naomi**: Yep.
[00:00:15] **Theo**: Loud and clear, Sarah. Good to finally do this.
[00:00:19] **Sarah**: Likewise, Theo. You've been the one championing this internally so thank you for the patience — I know procurement took a while.
[00:00:27] **Theo**: Healthtech procurement is its own circle of hell. But we got there.
[00:00:32] **Sarah**: Ha. OK so this is the POC kickoff. Goal today: lock success criteria, scope the workflows we'll build during the POC, and get Wendy's security requirements on the table early so they don't surprise us at the finish line. Ben's our SE, he'll run the technical scoping. Priya, our VP of Eng, is joining halfway for the deeper security and architecture questions. Sound good?
[00:00:55] **Naomi**: Good structure. Let's go.

[00:01:02] **Sarah**: First, level-set on commercials so the POC isn't divorced from reality. You're looking at roughly 300 seats. At Enterprise tier that's custom pricing — the way to think about it is we land most enterprise deals in the $50K to $500K ACV band depending on seats, run volume, and support needs. For 300 seats with your run profile I'd estimate we land somewhere around $180K ACV. That's the number I'd want to validate through the POC, not commit to today.
[00:01:34] **Naomi**: $180K is in the range we modeled. Our board approved up to $250K for workflow automation so we have headroom, but obviously we want the right number, not the ceiling.
[00:01:46] **Sarah**: Of course. And just to be transparent about the motion — Enterprise is a roughly 90-day cycle for us end to end, POC plus procurement plus security. We're at day zero. If we run a clean 60-day POC and a 30-day paper process, we'd be looking at a close around mid-September. Does that align with your timeline?
[00:02:08] **Theo**: That aligns. Our current contract — we're on a homegrown thing plus some Tray usage in one department — there's no hard renewal cliff, but I want this live before our Q4 clinical-ops push.
[00:02:22] **Sarah**: Mid-September gives you runway for Q4. Good.

[00:02:30] **Ben**: OK let's scope. Naomi, what are the workflows that define success? If these run reliably, you'll sign.
[00:02:38] **Naomi**: Three categories. First, patient-data ETL — we pull from our EHR system into our analytics warehouse nightly. This is HIPAA-sensitive so it has to be airtight. Second, clinical-ops alerting — Theo's team needs real-time alerts when certain events fire in our ops system, routed to the right on-call clinician. Third, the boring but important one — provisioning and deprovisioning across our internal tools when staff join or leave, which right now is a manual nightmare.
[00:03:12] **Ben**: OK. The patient-data ETL — what's the EHR system?
[00:03:17] **Carlos**: Epic. We have an interface engine in front of it, so really you'd be talking to the interface engine over HL7 or a REST facade we built. We can give you the REST facade, it's cleaner.
[00:03:30] **Ben**: REST facade is much easier for us. We'd hit it with authenticated HTTP steps. The HIPAA part — Priya will cover this when she joins, but the short version: we sign a BAA, the EU... sorry, the data stays in your provisioned region, logs can be configured to scrub payloads, and we have a per-step PII handling flag that's shipping. Wendy, I want to make sure we capture your requirements precisely, can you hold your questions for fifteen minutes until Priya's on?
[00:03:58] **Wendy**: I can. I'll drop them in the chat as we go so nothing's lost.
[00:04:04] **Ben**: Perfect, thank you.

[00:04:12] **Ben**: Clinical-ops alerting — what's the ops system, and what's "real-time" mean for you? Sub-second? Sub-minute?
[00:04:20] **Theo**: Sub-minute is fine. These aren't life-critical alerts in the code-blue sense — they're operational, like "this unit is over capacity" or "this lab result is flagged for follow-up." Sub-minute, routed to the right person based on an on-call schedule.
[00:04:36] **Ben**: OK so event fires in your ops system — does it emit a webhook?
[00:04:41] **Carlos**: It can emit webhooks, yeah.
[00:04:44] **Ben**: Great, so webhook trigger → look up on-call from your scheduling system → route to Slack or pager. That's very doable. The on-call lookup, what's the scheduling system?
[00:04:56] **Theo**: PagerDuty for the schedule, but we want the alert in Slack with a PagerDuty escalation if not acked in 10 minutes.
[00:05:05] **Ben**: PagerDuty connector exists, Slack connector exists. The "escalate if not acked in 10 min" is a pattern we support with a delayed-check step. Clean.
[00:05:14] **Theo**: That's better than what we have now, which is a human watching a dashboard.

[00:05:24] **Ben**: Third one, provisioning/deprovisioning. What systems?
[00:05:29] **Carlos**: When someone joins: create accounts in our EHR, our comms tool, our badge system, and our LMS. When they leave: deactivate all four plus revoke VPN. Right now IT does this by hand from a ticket and it takes a day and sometimes they miss one, which is a security finding waiting to happen.
[00:05:50] **Ben**: This is a great use case for us. Trigger off your HR system — what is it, Workday?
[00:05:56] **Carlos**: Workday, yeah.
[00:05:58] **Ben**: Workday connector exists. New hire in Workday → fan out to four create-account steps → notify IT for the badge physical handoff. Termination → fan out to deactivations + VPN revoke. The audit log captures every action, which is exactly what you want for the security findings.
[00:06:18] **Wendy** (in chat, read aloud by Sarah): "Wendy asks: does the deprovisioning flow itself get audited, and can we prove completeness — i.e., that all four systems were actually deactivated, not just attempted?"
[00:06:32] **Ben**: Great question. Yes — each step's success or failure is logged with the error code if it failed. So you can build a completeness check: if any of the four deactivations failed, the workflow status is failed and it pages IT. You get a provable audit trail. We'll demo that.
[00:06:50] **Wendy** (chat): "Good. That's been a literal audit finding for us."

[00:07:00] **Sarah**: OK so success criteria. Let me draft and you correct me. The POC succeeds if, within 60 days: (1) the Epic-REST → warehouse nightly ETL runs reliably for 14 consecutive nights with HIPAA controls validated by Wendy; (2) the clinical-ops webhook → Slack → PagerDuty-escalation alert routes correctly with sub-minute latency in a load test; (3) the Workday-triggered provisioning and deprovisioning flow completes across all four systems with a provable audit trail. Did I capture it?
[00:07:34] **Naomi**: Add a fourth — usability. I want at least three of my analysts able to build and modify a workflow themselves after a one-hour training, not just Carlos. If it's only Carlos who can use it, it's a bus-factor problem.
[00:07:50] **Sarah**: Excellent criterion, adding it. "At least 3 non-specialist analysts independently build/modify a workflow after a 1-hour session." That actually maps to how we think about healthy adoption internally — we look for at least a few active builders and a real cadence of successful runs, not just one hero user. So your bus-factor criterion is exactly the right instinct.
[00:08:12] **Naomi**: Good, glad we're aligned on that philosophy.

[00:08:20] (Carlos and Ben go deep on the Epic REST facade auth — OAuth2 client-credentials, token refresh, rate limits. ~12 min. Gong AI summary: no blockers identified; Carlos satisfied that Acme's HTTP step handles token refresh and backoff. One open item: Epic facade rate-limits at 100 req/min, ETL must batch — Ben confirms batching + RATE_LIMITED handling.)

[00:20:40] **Priya** (joining): Hi everyone, sorry to jump in mid-stream. Sarah said you've got security and architecture questions queued — Wendy, I think a few are yours. Want to just run through them?
[00:20:54] **Wendy**: Yes, thank you. I'll go in priority order. One: BAA. Will Acme sign a Business Associate Agreement, and is there a standard one or do we use ours?
[00:21:06] **Priya**: We'll sign a BAA. We have a standard one we can send, or we'll review yours — most healthtech customers prefer their own paper and we're fine with that as long as legal aligns. So yes, unambiguous yes on the BAA.
[00:21:20] **Wendy**: Good. Two: data residency and isolation. Where does the workflow data live, and is it logically or physically isolated from other tenants?
[00:21:32] **Priya**: Data residency — you'd be provisioned in our US region, US-East specifically, since you're NA-East and HIPAA. Isolation is logical multi-tenancy with per-tenant encryption keys; it's not physically separate infrastructure unless you go to our dedicated-tenancy add-on, which some regulated customers do. Happy to scope dedicated tenancy if your risk posture requires it — it's a cost adder but available.
[00:21:58] **Wendy**: Let me take that back to our risk team. Logical with per-tenant keys may be acceptable but I want to confirm. Three: encryption at rest and in transit?
[00:22:10] **Priya**: AES-256 at rest, TLS 1.2+ in transit, mutual TLS available for the webhook ingress if you want it. Keys managed in our KMS; BYOK is on the roadmap but not GA — if BYOK is a hard requirement, flag it now because it would affect timeline.
[00:22:30] **Wendy**: BYOK is a "strongly prefer," not a "hard requirement" yet. I'll note it as a roadmap ask.
[00:22:38] **Priya**: Noted, and I'll be honest about where BYOK sits in the roadmap rather than overpromise.
[00:22:44] **Wendy**: Appreciated, that's rare. Four: the PII handling in logs. Ben mentioned a per-step flag. Tell me more.
[00:22:54] **Priya**: Right. By default we log step inputs and outputs for debugging, which is great for non-sensitive flows and terrible for PHI. We have a per-step "treat output as sensitive" flag that redacts the payload from logs — you see that the step ran and its status, but not the contents. For your patient-data ETL every step would have that flag on. It's shipping; it shipped to GA recently actually, so it's not vaporware.
[00:23:18] **Wendy**: That's important. I'd want to verify it in the POC — actually confirm that PHI doesn't land in logs.
[00:23:26] **Priya**: We'll make that an explicit POC validation step. Ben, add "Wendy validates no-PHI-in-logs with the sensitive flag" to the criteria.
[00:23:34] **Ben**: Added.

[00:23:42] **Wendy**: Five, and this is the big one — pen test results and SOC2. Can we see your most recent SOC2 Type II report and a pen test summary under NDA?
[00:23:54] **Priya**: Yes to both. SOC2 Type II, audited annually by a third party, no qualifications in the latest report. Pen test is annual plus continuous bug bounty; we share the executive summary under NDA, not the raw findings. Sarah will route both to you under NDA today.
[00:24:14] **Wendy**: That covers my top five. I have a longer questionnaire — 140 questions, sorry — that I'll send.
[00:24:22] **Priya**: 140 is light for healthtech honestly. Send it, we'll turn it around. We have a pre-filled master that answers most of these, so it'll be fast.
[00:24:32] **Wendy**: A pre-filled master. You have no idea how happy that makes me.
[00:24:37] **Sarah**: It's everyone's favorite sentence on these calls.

[00:24:46] **Naomi**: Priya, architecture question while you're here. The nightly ETL — if it fails at 2am, what happens? I don't want a silent failure on patient data.
[00:24:58] **Priya**: Failure is never silent if you configure alerting, which we'll set up. The run gets a failed status with a specific error code — could be AUTH_FAILED if the Epic token expired, RATE_LIMITED if you hit the facade's cap, STEP_TIMEOUT, INTEGRATION_DOWN if the warehouse is unreachable, SCHEMA_MISMATCH if the data shape changed. Each one is a distinct code so you're not guessing. You alert on any failure and you get the code, so your on-call knows whether it's a token issue or a schema drift before they even open the logs.
[00:25:28] **Carlos**: That error taxonomy is genuinely better than what we have. We currently get "it broke."
[00:25:34] **Priya**: "It broke" is the enemy. The whole point is to make failures legible.

[00:25:44] (Priya and Carlos discuss the warehouse target — it's Snowflake, not BigQuery. Ben confirms Snowflake connector. ~6 min. Gong AI summary: architecture validated; Priya comfortable with the integration surface; no red flags.)

[00:32:10] **Sarah**: OK we're at time. Let me lock the plan. Success criteria, five of them: Epic-REST nightly ETL stable 14 nights with HIPAA controls; clinical-ops alert sub-minute with PagerDuty escalation; Workday provisioning/deprovisioning with provable audit trail; 3+ non-specialist analysts build independently after 1-hour training; Wendy validates no-PHI-in-logs. 60-day POC, target close mid-September. Ben drives the build with Carlos. I drive commercials and paper. Priya's team backstops security. Did I miss anything?
[00:32:48] **Naomi**: That's complete.
[00:32:52] **Theo**: I'm happy. This is the most organized kickoff I've sat through, and I've sat through a few.
[00:32:58] **Sarah**: That means a lot, Theo, and thank you again for championing this internally — none of this happens without an internal advocate.
[00:33:06] **Theo**: Happy to. I want this to work.

[00:33:14] **Sarah**: Action items: I send SOC2 + pen test summary + the master security questionnaire to Wendy today under NDA. Ben sets up the POC workspace in US-East, schedules the Epic facade integration session with Carlos for this week, and the 1-hour analyst training for next week. Wendy sends the 140-question questionnaire. Naomi nominates the three analysts for the training. Theo and I sync weekly on POC progress. Reconvene for a mid-POC checkpoint in 30 days. Everyone good?
[00:33:48] **Naomi**: Good.
[00:33:50] **Wendy**: Good, NDA coming.
[00:33:53] **Theo**: See you at the weekly.
[00:33:57] **Sarah**: Thanks all. Excited about this one.
[00:34:01] (call ends)

---

## Acme post-call read (Gong + AE notes)

- **Stage**: Qualified → POC (enterprise). Day 0 of ~90-day enterprise cycle.
- **Account**: `cust_000701` Marigold Health, Enterprise, 300 seats, $15,000 MRR / $180K ACV target, NA-East/healthtech, partner-sourced (Lumen Integration Partners). CSM Olivia Tran, AE Sarah Chen.
- **Forecast**: ~$180K ACV, board-approved ceiling $250K. On close-won this annualized ACV lands in `bookings_attribution.bookings_acv_usd`, first_touch_channel = partner.
- **Success criteria** (5): Epic-REST nightly ETL 14 nights + HIPAA; clinical-ops alert sub-minute + PagerDuty escalation; Workday provisioning/deprovisioning w/ audit trail; 3+ non-specialist analysts build independently after 1h training; no-PHI-in-logs validated via sensitive-output flag.
- **Security gate**: BAA (yes), logical multi-tenancy + per-tenant keys (under risk-team review; dedicated tenancy available as adder), AES-256/TLS1.2+, BYOK roadmap-only (flagged), SOC2 Type II + pen test under NDA, 140-q questionnaire.
- **Champion**: Theo Novak (Director Clinical Ops) — strong internal advocate.
- **Note**: Naomi's "bus-factor" criterion mirrors our internal healthy-adoption view (multiple active builders + real run cadence, not a single hero user).
- **Action items**: Sarah — SOC2/pentest/questionnaire under NDA; Ben — US-East workspace, Epic session, analyst training; Wendy — questionnaire; Naomi — nominate 3 analysts; weekly Theo/Sarah sync; 30-day checkpoint.

---

## Gong call — Driftwood Media — Pro onboarding / upsell probe — 2025-04-22

**Type**: Pro customer check-in (self-serve account, CSM-light)
**Time**: 2025-04-22, 10:30–10:52 PT
**Acme attendees**: Grace Liu (CSM), Yuki Sato (AE — joined 10:44)
**Customer attendees**: Dev Ramaswamy (Marketing Ops Manager)
**Account**: `cust_000702` Driftwood Media — Pro / 18 seats / $882 MRR / NA-West / media / organic
**Source**: Self-serve signup (organic), CSM courtesy check-in
**Duration**: 00:22:18
**Sentiment trace (Gong AI)**: Positive 70% / Neutral 26% / Negative 4%

[00:00:05] **Grace**: Hi Dev! Thanks for hopping on. This is just a friendly check-in — you signed up self-serve a few months back, you're on Pro with 18 seats, and I wanted to make sure you're getting value and see if there's anything I can help with. No sales pitch, promise. Well, mostly no sales pitch.
[00:00:22] **Dev**: Ha. Appreciated. Yeah we're a media company, I run marketing ops, and honestly Acme has been great for us. We came over from Zapier because we hit the task limits and the pricing got silly.
[00:00:36] **Grace**: That's a story I hear a lot. What are you running these days?
[00:00:41] **Dev**: Mostly marketing flows. Lead capture from our forms into HubSpot, enrichment, routing to the right rep, some Slack notifications for the content team when a piece goes live, and a weekly digest that pulls analytics into a Google Sheet. Nothing crazy but it all just works, which is the point.
[00:01:02] **Grace**: Love it. "It just works" is the goal. How many of your 18 are actually building versus just have a login?
[00:01:10] **Dev**: Building, maybe four of us. The rest have logins so they can see the dashboards and check on stuff. Marketing team mostly.
[00:01:18] **Grace**: Got it. And run volume — are you anywhere near the Pro cap? Pro is 10K runs a month.
[00:01:25] **Dev**: We're at like 3K, 4K a month. Plenty of headroom.
[00:01:30] **Grace**: Good, so no surprise overage. If you ever creep toward 10K I'll give you a heads up before it becomes an issue.

[00:01:40] **Dev**: Can I ask — we've been thinking about pulling some of our customer-facing flows in, the ones that touch our billing system. Right now those are on a homegrown script. Is there anything about Pro that would stop us?
[00:01:56] **Grace**: Depends on a couple things. Pro gives you unlimited workflows and 10K runs. What Pro doesn't have is SSO, audit logging, and priority support — those kick in at Business. If your billing flows are sensitive enough that you'd want an audit trail of who changed what, or if your security team wants SSO, that's the line where people move up to Business.
[00:02:20] **Dev**: We don't have a security team per se. We're like 90 people. SSO would be nice-to-have but not essential yet.
[00:02:30] **Grace**: Then Pro is probably still right for you. I'm not going to push you to Business if you don't need the features — that's not how I operate. The honest trigger for Business is usually one of three things: you cross 50-ish people who need seats, you need SSO/audit for compliance, or you blow past 10K runs. You're not at any of those yet.
[00:02:50] **Dev**: That's refreshingly honest for a CS call.
[00:02:54] **Grace**: I'd rather you trust me than upsell you into something you'll resent.

[00:03:02] **Dev**: OK while I have you — totally unrelated — the workflow builder, when I have like a 15-step flow, the canvas gets a little cramped. Any way to group steps?
[00:03:14] **Grace**: Node grouping is actually a feature in beta right now, GA expected later this year. It lets you collapse a set of steps into a labeled group. I can see if I can get your account into the beta if you want to try it.
[00:03:26] **Dev**: Yeah throw me in, I'll give feedback.
[00:03:30] **Grace**: Done, I'll flag it.

[00:03:38] **Yuki** (joining): Hey Dev, Yuki here, I'm the account exec for the West Coast media accounts. Grace pinged me to say hi — I won't crash your check-in, just wanted to put a face to the name in case you ever grow into needing the bigger-tier stuff.
[00:03:54] **Dev**: Hey Yuki. Yeah no problem.
[00:03:58] **Yuki**: I'll be brief. The only thing I'll say is — a lot of media companies we work with eventually centralize automation across departments, and when that happens the seat count jumps and SSO becomes a requirement, and that's when Business makes sense. If you ever get there, I'm your person and we'll make the math work. Until then, enjoy Pro.
[00:04:18] **Dev**: Cool, appreciate the low-pressure version of that.
[00:04:22] **Yuki**: Low pressure is the brand.

[00:04:30] (Grace walks Dev through a couple of dashboard features he hadn't discovered — the run-history filter and the error-code breakdown. ~10 min. Gong AI summary: customer healthy and happy; no churn risk; expansion possible in 6-12 months if they centralize automation; node-grouping beta requested.)

[00:15:10] **Dev**: This error-code breakdown is useful, I didn't know it was there. We had a flow silently failing last month and I only found out because someone complained.
[00:15:22] **Grace**: Yeah, set up a failure alert on that one — I'll send you the doc. You can get a Slack ping whenever a run fails with, say, an AUTH_FAILED or INTEGRATION_DOWN code. No more finding out from complaints.
[00:15:34] **Dev**: Perfect.

[00:15:42] **Grace**: OK I'll let you go. Recap: you're healthy on Pro, plenty of run headroom, I'm adding you to the node-grouping beta, and I'll send the failure-alert setup doc. If you ever centralize across departments and need Business, Yuki's your AE. Sound good?
[00:16:00] **Dev**: Sounds great. Thanks Grace, thanks Yuki.
[00:16:04] **Yuki**: Anytime.
[00:16:06] **Grace**: Bye Dev!
[00:16:08] (call ends)

---

## Acme post-call read (Gong + CSM notes)

- **Stage**: Existing Pro customer, healthy. No active opportunity.
- **Account**: `cust_000702` Driftwood Media, Pro, 18 seats, $882 MRR, NA-West/media, organic self-serve. CSM Grace Liu, AE Yuki Sato.
- **Health**: ~4 active builders of 18 seats, ~3–4K runs/mo (well under 10K Pro cap). Happy, NPS-positive. No churn risk.
- **Expansion**: Possible Pro→Business in 6–12 months if they centralize automation across departments (seat jump + SSO trigger). AE-led when it happens; Yuki owns.
- **Note**: this is a self-serve Free→Pro→ongoing account; not opportunity-sourced, so it would NOT appear in `bookings_attribution`. Any future AE-led Business upsell would create an opportunity and then appear in bookings on close.
- **Action items**: Grace — add to node-grouping beta, send failure-alert setup doc. No commercial action.

---

## Gong call — Onyx Robotics — enterprise pricing negotiation — 2025-08-19

**Type**: Pricing / commercial negotiation (enterprise, post-POC)
**Time**: 2025-08-19, 15:00–15:58 PT
**Acme attendees**: Tom Becker (AE), Marcus Webb (VP Sales — joined 15:30), Rachel Stein (CFO — joined 15:42 for deal-desk sign-off)
**Customer attendees**: Greg Tanaka (VP Platform Engineering), Sofia Marchetti (Procurement Lead), Diane Whitfield (Director, IT Finance)
**Account**: `cust_000704` Onyx Robotics — Enterprise / 500 seats / $35,000 MRR ($420K ACV) / NA-West / devtools / outbound
**Source**: Outbound, POC completed 2025-08-08 (passed 4/4 criteria)
**Duration**: 00:58:40
**Sentiment trace (Gong AI)**: Positive 44% / Neutral 39% / Negative 17% (negotiation tension expected)

[00:00:06] **Tom**: Hi Greg, Sofia, Diane. Thanks for the time. Big call today — we've got a successful POC behind us and now we're talking commercials, so I expect we'll do some honest back-and-forth. Marcus, our VP of Sales, will join partway, and our CFO Rachel may pop in to sign off on whatever we land on. Sound good?
[00:00:26] **Greg**: Sounds good. Just to say up front — the POC went well. My engineers liked it. The four success criteria all passed, the team built workflows independently, the error handling is genuinely good. So this is not a "do we want it" conversation, it's a "what's the number" conversation.
[00:00:46] **Tom**: That's the best kind of call to be on. Thank you for that.
[00:00:50] **Sofia**: I'll add the procurement framing: we want it, and my job is to get the best deal and clean terms. So don't take my pushback personally.
[00:00:59] **Tom**: Never do. Push away.

[00:01:08] **Tom**: OK let me set the baseline. You're looking at 500 seats. At Enterprise tier our list math for a deployment your size lands around $35,000 a month, which annualizes to $420K ACV at list. That's the starting point. I know procurement's first question is going to be "what's the discount," so let's just get into it.
[00:01:32] **Sofia**: $420K list. What's the discount for an annual prepay and a multi-year commit?
[00:01:40] **Tom**: For a one-year annual commit, we typically land 10 to 15% off list for a deal this size. For a two-year commit with annual prepay, I can stretch further — I'd want to bring Marcus in for the bigger numbers, but I can talk a 20%-ish range for two years. Three years, more.
[00:02:00] **Sofia**: Let's talk two-year. 20% off $420K is $336K a year. I want to get to $300K.
[00:02:10] **Tom**: $300K on 500 seats is about $50 a seat a month effectively, which is below our Pro list price — I can't get there on seat math alone. But I hear the target. Let me understand the shape — is this a hard budget ceiling, or a negotiating anchor?
[00:02:28] **Sofia**: Bit of both. Diane, you have the budget picture.
[00:02:33] **Diane**: We have $360K approved for this line item for the year. I'd love to come in under it to bank the difference, but $360K is the real ceiling. Above that needs a CFO exception on our side and I'd rather not.
[00:02:48] **Tom**: OK that's really useful, thank you for the transparency. So we're negotiating in the $300–360K band, not trying to bridge a chasm. That I can work with.

[00:02:58] **Greg**: Can I ask what drives the price beyond seats? Because 500 seats but honestly maybe 60 of those are active builders, the rest are viewers.
[00:03:10] **Tom**: Fair question and it comes up a lot. Our Enterprise pricing isn't purely per-active-seat — it's a platform deal: unlimited runs, dedicated CSM, SOC2 and compliance support, custom SLA, and the seat count is the licensing envelope. We don't meter you on active users — you could have 60 builders today and 200 next year and the price doesn't jump. That stability is part of what you're buying. But I understand the "we're paying for viewers" feeling. One way we handle it is to right-size the initial seat count to where you actually are plus headroom, rather than your total headcount.
[00:03:46] **Greg**: So if we said 350 seats instead of 500?
[00:03:50] **Tom**: 350 seats Enterprise is still comfortably above our 250-seat Enterprise minimum, so that's a valid Enterprise deployment. The math comes down proportionally — 350 seats would land around $294K ACV at list, and then we discount from there. But here's the honest tradeoff: if you license 350 and you grow into 500 mid-term, the expansion seats get added at the then-current rate, and you lose the lock-in protection on those incremental seats. A lot of customers license to where they're growing, not where they are, precisely to lock the rate.
[00:04:22] **Sofia**: So you're saying license higher to lock the rate.
[00:04:26] **Tom**: I'm saying there's a real tradeoff and I want you to make it with open eyes, not have me upsell you. If you're confident you'll stay around 350, license 350. If you know you're going to 500 within the term, locking 500 now at a discount is cheaper than adding seats later at list.
[00:04:46] **Greg**: We're hiring aggressively. We'll be past 400 builders-plus-viewers within a year, easily.
[00:04:52] **Diane**: That actually changes my math. If we'll be at 500 anyway, locking 500 now at a good rate is better than 350 now plus expansion later.

[00:05:02] (Sofia, Diane, Greg discuss internally for ~4 min about seat count vs. budget; Gong AI summary: internal alignment that 500 seats is the right envelope given hiring plans, target effective price $336K or below, hard ceiling $360K. Tom mostly silent, lets them caucus.)

[00:09:30] **Sofia**: OK. We'll commit to 500 seats, two years, annual prepay. We want $330K a year. That's 21.4% off your $420K list. Clean terms, our paper, standard MSA.
[00:09:46] **Tom**: 500 seats, two years, annual prepay, $330K. That's a strong commit and the prepay matters to us. Let me be straight: $330K is right at the edge of what I can approve solo. For two-year prepay at this seat count I can get to about $340K on my own authority. To get to $330K I need Marcus, and he's joining in a few minutes — let me tee it up for him. Are the rest of the terms otherwise settled? Because I don't want to win on price and then discover a surprise in legal.
[00:10:14] **Sofia**: Terms are standard. Our MSA, your DPA, BAA not needed — we're devtools, not regulated health/finance data. The only non-standard ask is a 30-day termination-for-convenience clause, which I know vendors hate.
[00:10:30] **Tom**: We do hate it, honestly, because the whole point of an annual prepay commit is the commitment. A 30-day out turns a two-year deal into a rolling monthly. That's the one I'll push back on hard. Everything else sounds workable.
[00:10:46] **Sofia**: Noted. I expected pushback there. It's a default ask, not a hill I'll die on.
[00:10:52] **Tom**: Appreciated. Let's hold that for Marcus too.

[00:11:00] **Greg**: While we wait — operational question. Our POC was in your US-West region. Production stays there?
[00:11:08] **Tom**: Yes, US-West, same region, no migration needed from POC to prod. We promote the POC workspace to production rather than rebuilding. Your workflows carry over.
[00:11:18] **Greg**: Good, I didn't want to rebuild 40 workflows.
[00:11:22] **Tom**: Never make you rebuild. That'd be a terrible experience.

[00:11:30] (~14 min on SLA specifics — uptime commitment, support response times, dedicated CSM cadence. Gong AI summary: agreed 99.9% uptime SLA with service credits, 1-hour P1 response, dedicated CSM Olivia Tran with biweekly cadence. Greg satisfied. Diane confirms SLA credits structure acceptable to finance.)

[00:25:50] **Marcus** (joining): Hey everyone, Marcus here, VP of Sales. Tom caught me up — 500 seats, two years, annual prepay, you're at $330K, we're at $340K, and there's a termination-for-convenience ask on the table. Did I get that right?
[00:26:08] **Sofia**: That's exactly right.
[00:26:11] **Marcus**: OK. Let me be direct because I respect that you've been direct. On price: $330K for a two-year prepay at 500 seats — I can do it, but I need something for it, because that's a real discount off list and our deal desk will ask me why. Here's my offer: $330K a year, two years, annual prepay — if you drop the termination-for-convenience clause and agree to be a public reference customer, one case study and two reference calls a year. That's a fair trade. The reference is worth real money to us in devtools where peer proof matters.
[00:26:48] **Sofia**: Drop termination-for-convenience, we already weren't married to it. Reference customer — Greg, that's your call, it's your team's name on it.
[00:26:58] **Greg**: I'm fine being a reference. The product earned it in the POC. One case study, two calls a year, as long as we approve the case study content before it goes out.
[00:27:10] **Marcus**: Approval rights on the case study, absolutely, standard. So: $330K a year, two years, annual prepay, no term-for-convenience, public reference with content approval. Do we have a deal in principle?
[00:27:24] **Sofia**: We have a deal in principle, pending legal redline and CFO sign-off on both sides.
[00:27:30] **Marcus**: Excellent. Tom, get the order form drafted at $330K/yr, 24-month term, annual prepay, reference clause, no TFC. Rachel's joining to bless it from our side.
[00:27:42] **Tom**: On it.

[00:27:50] **Rachel** (joining): Hi all, Rachel Stein, CFO at Acme. Marcus pinged me. $330K a year, two-year prepay, 500 seats, reference customer, no termination-for-convenience — from a finance standpoint that's an approvable deal. The annual prepay is what makes the discount work for us; if it were paid-in-arrears monthly I'd be pushing back. Diane, anything from your side I should know about your payment process?
[00:28:18] **Diane**: We pay annual prepay against an annual invoice, net-45. As long as the invoice is clean and dated correctly for our fiscal year — our FY starts October 1 — we're fine.
[00:28:30] **Rachel**: Net-45 is fine. We'll date the invoice to align with your October 1 fiscal start if you want the expense in the new FY — just tell us the date you want and we'll cut it then. We're flexible on invoice timing within reason; we're not flexible on the prepay structure.
[00:28:48] **Diane**: That works perfectly. Date it October 1.
[00:28:52] **Rachel**: Done. Tom will reflect that on the order form. One thing on my end for cleanliness — this is a new-logo booking, so it'll flow through as annual contract value, fully annualized, into our bookings the day it's signed. I mention it only because sometimes there's confusion about prepay vs. recognized revenue — the booking is the $330K ACV, recognized ratably over the year. Doesn't affect you, just noting it for our own deal desk.
[00:29:16] **Sofia**: Doesn't affect us, but appreciated for the transparency.

[00:29:24] **Marcus**: Great. So we're aligned. Tom owns the order form today, legal teams redline this week, target signature by end of August to get you live before your October FY. Greg, your team can keep building in the POC workspace in the meantime — it just converts to prod on signature.
[00:29:42] **Greg**: That's ideal. No downtime, no rebuild.
[00:29:46] **Sofia**: Send the order form, I'll route it to legal today.
[00:29:50] **Tom**: Will have it to you within two hours.

[00:29:58] **Rachel**: Pleasure doing business. I'll drop off — Tom and Marcus have it from here.
[00:30:04] **Marcus**: Thanks Rachel. OK anything else from the Onyx side?
[00:30:08] **Greg**: No, I think we're good. This was efficient. Appreciate everyone being straight.
[00:30:14] **Marcus**: That's how we like it. Welcome aboard, pending paper.
[00:30:18] (call ends; ~40s retained off-camera: Marcus to Tom — "good deal, the prepay and the reference make the discount defensible to deal desk, write it up clean"; Tom — "on it, $330K, 24mo, no TFC, reference with approval".)

---

## Acme post-call read (Gong + AE notes)

- **Stage**: POC passed (4/4) → Negotiation → Verbal/deal-in-principle. Pending legal + dual CFO sign-off.
- **Account**: `cust_000704` Onyx Robotics, Enterprise, 500 seats, $35,000 MRR / $420K list, NA-West/devtools, outbound. CSM Olivia Tran, AE Tom Becker.
- **Final terms**: $330K ACV/yr, 24-month term, annual prepay, 99.9% SLA w/ credits, 1h P1 response, dedicated CSM biweekly, public reference (1 case study + 2 calls/yr, content-approval rights), NO termination-for-convenience.
- **Discount**: 21.4% off $420K list, justified by 2yr prepay + reference. Within customer's $360K hard ceiling.
- **Bookings note (Rachel)**: new-logo, books as fully-annualized $330K ACV into `bookings_attribution.bookings_acv_usd` on signature (already annual — do NOT ×12); recognized ratably. Invoice dated to customer's Oct-1 FY start; prepay structure non-negotiable.
- **Seat-sizing insight**: customer initially floated 350 seats; chose to lock 500 to protect rate against aggressive hiring (expansion seats would otherwise add at then-current list).
- **Action items**: Tom — order form within 2h ($330K/24mo/prepay/reference/no-TFC, invoice 10-01); legal redline this week; target signature end of Aug; POC workspace converts to prod on signature (no rebuild).

---

## Gong call — Ember Industries — QBR + expansion discovery — 2025-10-07

**Type**: Quarterly Business Review with expansion thread
**Time**: 2025-10-07, 11:00–11:54 ET
**Acme attendees**: Olivia Tran (CSM), Tom Becker (AE — joined 11:28 for expansion)
**Customer attendees**: Raphael Mwangi (Director of Supply Chain Systems), Tess Okafor (Ops Automation Lead), Bill Hartley (VP Logistics — joined 11:34)
**Account**: `cust_000711` Ember Industries — Enterprise / 350 seats / $25,000 MRR ($300K ACV) / NA-East / logistics / outbound
**Source**: Existing Enterprise customer, scheduled QBR
**Duration**: 00:54:10
**Sentiment trace (Gong AI)**: Positive 67% / Neutral 28% / Negative 5%

[00:00:06] **Olivia**: Morning Raphael, morning Tess! Good to see you both. This is our Q3 business review. I want to walk through how the last quarter went, share some usage data, hear what's working and what isn't, and then there's an expansion thread Raphael flagged so Tom's going to join later for that. How's everyone doing?
[00:00:26] **Raphael**: Doing well. Busy quarter. Peak shipping season ramping up so automation is carrying a lot of weight right now.
[00:00:34] **Olivia**: That's exactly when I like to see the numbers. OK let me share my screen. So — Ember, 350 seats Enterprise. Over the last 28 days you had 142 active users, which against 350 licensed seats is a utilization of about 0.41. That's healthy for Enterprise — and remember at Enterprise we don't gate you on utilization the way we would a smaller plan, you've got unlimited runs and the seat count is just your envelope. But I like to track it because rising utilization is the best leading indicator of expansion, and yours is climbing — it was 0.33 last quarter.
[00:01:14] **Raphael**: It's climbing because we onboarded the whole APAC ops team in August.
[00:01:20] **Olivia**: That tracks with the curve. Run volume — you did about 4.1 million runs last quarter, success rate 98.7%, which is excellent. Your p95 duration is 2.3 seconds. The failures you did have were mostly RATE_LIMITED against one carrier API and a handful of INTEGRATION_DOWN when that same carrier had an outage in September. Nothing on our side.
[00:01:48] **Tess**: Yeah that carrier is a nightmare. We've been meaning to add backoff on those flows.
[00:01:54] **Olivia**: Let's do that today actually, it's a five-minute config change and it'll clean up most of those RATE_LIMITED failures. I'll show you after the metrics.
[00:02:04] **Tess**: Perfect.

[00:02:12] **Olivia**: Engagement-wise you are very healthy. You're well past what we consider an engaged account — we look for at least three active users and at least ten successful runs in a trailing 28-day window as the floor, and you're at 142 active users and 4 million runs, so you're not just clearing the bar, you're a poster child. That's the kind of account that tends to expand, which is a nice segue.
[00:02:38] **Raphael**: Funny you say that.

[00:02:44] **Olivia**: Let's hold the expansion for when Tom joins so he can do the commercial part properly. First — what's working, what's not? Honest feedback time.
[00:02:54] **Raphael**: Working: reliability, the error visibility, the fact that my ops people can build their own flows without bugging engineering. Not working, or rather, wish-list: the workflow builder gets unwieldy on our big flows — our carrier-routing flow is like 40 steps and editing it is painful. And we'd love better version history, like being able to see a diff of who changed what and roll back.
[00:03:22] **Olivia**: Both of those are real and both are on the roadmap. Node grouping for the big-canvas problem is in beta now, GA later this year — I can get Tess into the beta. Version history with diffs and rollback is further out, targeted for first half next year, no firm date, and I won't pretend otherwise.
[00:03:44] **Tess**: Node grouping beta, yes please. The 40-step flow is the bane of my existence.
[00:03:50] **Olivia**: Adding you now.

[00:03:58] **Raphael**: One more — and this is a sensitive one — we had a near-miss last quarter where a workflow that touches our pricing data nearly exposed margin numbers in a log that the wrong team could see. We caught it, but it spooked our security team.
[00:04:16] **Olivia**: That's exactly what the sensitive-output flag is for. You set a per-step flag and the payload gets redacted from the logs — the step status is visible, the contents aren't. It's GA. I'll have your team retrofit it onto any pricing-data flows. This is important enough that I'll make it a tracked action item, not just a mention.
[00:04:38] **Raphael**: Please. My security lead will sleep better.

[00:04:46] (Olivia walks Tess through adding exponential backoff to the carrier flow live, and enabling the sensitive-output flag on the pricing flow. ~16 min. Gong AI summary: both config changes completed live; Tess confirmed the carrier RATE_LIMITED errors should drop materially; security concern addressed with sensitive-output redaction; customer expressed strong satisfaction with CSM responsiveness.)

[00:22:20] **Tom** (joining): Hey Raphael, Tess. Olivia tells me there's an expansion conversation. I love those. What's the picture?
[00:22:30] **Raphael**: So. We acquired a smaller logistics company in September — Cartwright Freight, about 120 people. They have their own automation mess and our directive from the top is to standardize them onto our tooling, which means Acme. So we need more seats.
[00:22:50] **Tom**: Congrats on the acquisition, and that's great for us obviously. Let's size it. You're at 350 Enterprise seats today. Cartwright adds how many seat-needs?
[00:23:02] **Raphael**: Of the 120 people, realistically 60 to 80 would touch Acme — their ops and finance folks. Call it 75 to be safe.
[00:23:12] **Tom**: So you'd go from 350 to roughly 425. Still one Enterprise contract, just a larger envelope. The clean way to do this is a mid-term expansion — we add the 75 seats to your existing Enterprise agreement, co-terminus with your current renewal so you're not managing two contracts and two renewal dates.
[00:23:34] **Raphael**: Co-terminus is what I'd want. When's our renewal again?
[00:23:40] **Olivia**: Your current term renews 2026-03-15.
[00:23:44] **Tom**: Right, so we'd add 75 seats now, prorated to that 2026-03-15 renewal date, and then at renewal the whole thing — 425 seats — renews as one number. Pricing: your current effective rate is about $71 a seat a month — that's $25,000 MRR over 350 seats — and I'd honor that same effective rate on the expansion seats rather than charging you new-customer list. So 75 seats at ~$71 is about $5,300 a month additional, roughly $64K of incremental ACV on an annualized basis, prorated for the partial term until renewal.
[00:24:24] **Raphael**: Honoring our existing rate on the new seats is the right thing to do. I appreciate you not gouging us on the acquisition.
[00:24:32] **Tom**: Gouging a customer on an expansion is how you lose them at renewal. The expansion is the easy part — I want the renewal to be a non-event because we've been fair all along.

[00:24:44] **Bill** (joining): Sorry I'm late — Bill, VP Logistics. Raphael, did I hear we're adding the Cartwright seats?
[00:24:52] **Raphael**: Yeah, Tom's sizing it. 75 seats, co-terminus, at our existing rate.
[00:24:58] **Bill**: Good. Budget for the Cartwright integration is approved, so no procurement drama on our side this time. Just get me the number and I'll sign.
[00:25:08] **Tom**: Music to my ears. Roughly $64K incremental annualized, prorated to your March renewal. I'll put exact figures on an order form.
[00:25:18] **Bill**: Send it. We move fast on stuff that's already budgeted.

[00:25:26] (Tom, Raphael, Bill discuss the Cartwright migration timeline and whether the expansion seats need to be provisioned before migration starts. ~10 min. Gong AI summary: agreed to provision 75 seats within a week so Cartwright onboarding can start; Olivia to lead the Cartwright migration with a dedicated onboarding plan; expansion order form to follow.)

[00:36:00] **Tom**: OK, so to land the expansion cleanly: 75 additional seats added to the existing Enterprise agreement, co-terminus with the 2026-03-15 renewal, at your current ~$71/seat effective rate, roughly $64K incremental annualized ACV prorated for the partial term. Order form from me this week, Bill signs since it's pre-budgeted, Olivia provisions within a week and owns the Cartwright migration plan. Anything I'm missing?
[00:36:30] **Raphael**: That's it. Clean.
[00:36:34] **Bill**: Send the form.
[00:36:38] **Olivia**: And I'll have the Cartwright onboarding plan drafted before the seats are even provisioned so we hit the ground running.

[00:36:48] **Olivia**: Last thing before we wrap — anything else on the roadmap or support side you need from us this quarter?
[00:36:56] **Raphael**: No, honestly this has been one of our better vendor relationships. Keep doing what you're doing.
[00:37:02] **Olivia**: That's lovely to hear. Thank you both, and Bill, nice to meet you.
[00:37:08] **Bill**: Likewise. Send the form, Tom.
[00:37:11] **Tom**: It's basically already written. Talk soon, all.
[00:37:15] (call ends)

---

## Acme post-call read (Gong + CSM/AE notes)

- **Stage**: QBR (healthy) + expansion discovery → expansion verbal. Pre-budgeted, low friction.
- **Account**: `cust_000711` Ember Industries, Enterprise, 350 seats → expanding to ~425, $25,000 MRR / $300K ACV, NA-East/logistics, outbound. CSM Olivia Tran, AE Tom Becker. Renewal 2026-03-15.
- **Health**: utilization 0.41 (up from 0.33 QoQ), 142 active users / 350 seats, 4.1M runs/qtr, 98.7% success. Well past engaged floor (≥3 active users AND ≥10 successful runs / 28d). Failures were external (carrier RATE_LIMITED + INTEGRATION_DOWN), not Acme.
- **Expansion**: +75 seats (Cartwright Freight acquisition), co-terminus to 2026-03-15 renewal, honored existing ~$71/seat effective rate (not new-logo list), ~$64K incremental annualized ACV prorated for partial term.
- **Bookings note**: this is an AE-led expansion opportunity → on close it appears in `bookings_attribution` as annualized ACV (already annual). Distinct from any self-serve motion.
- **Resolved live**: added carrier-API backoff (kills RATE_LIMITED noise); enabled sensitive-output redaction on pricing-data flow (security near-miss).
- **Roadmap asks**: node-grouping beta (Tess added); version-history-with-diff/rollback (H1 next year, no firm date).
- **Action items**: Tom — expansion order form this week; Bill signs (pre-budgeted); Olivia — provision 75 seats within a week + own Cartwright migration plan.

---
