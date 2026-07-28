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

## Gong call — Quartz Foundry — enterprise discovery — 2025-09-23

**Type**: Discovery (enterprise, partner-sourced)
**Time**: 2025-09-23, 14:00–14:47 GMT
**Acme attendees**: Sarah Chen (AE), Ben Cohen (Sales Engineer)
**Customer attendees**: Dr. Hannah Brückner (Head of Lab Informatics), Pieter Vandenberg (IT Director), Lucia Romano (Procurement)
**Account**: `cust_000714` Quartz Foundry — Enterprise / 280 seats / $12,000 MRR ($144K ACV) / EMEA / healthtech / partner
**Source**: Partner referral (`Lumen Integration Partners`), inbound demo request via partner
**Duration**: 00:47:30
**Sentiment trace (Gong AI)**: Positive 49% / Neutral 44% / Negative 7%

[00:00:05] **Sarah**: Hi Hannah, Pieter, Lucia. Can everyone hear me alright? I think the audio's good.
[00:00:11] **Hannah**: Yes, we can hear you.
[00:00:14] **Sarah**: Wonderful. So thank you — this came through our partner Lumen, who I gather you've worked with on some of your lab systems integration?
[00:00:23] **Pieter**: Yes, Lumen did our LIMS integration last year. They mentioned Acme when we said we were drowning in manual data shuffling between systems.
[00:00:33] **Sarah**: That's a phrase I hear a lot — "drowning in manual data shuffling." It's basically our entire reason to exist. Ben here is our solutions engineer for the technical depth. Before we dive in — Hannah, what's your role exactly? I want to make sure I'm pitching to the right problems.
[00:00:50] **Hannah**: I run lab informatics. So I'm responsible for all the data systems in our labs — sample tracking, instrument data capture, getting results into our analysis pipelines and out to clients. We're a contract research org, so turnaround time on results is literally our product.
[00:01:10] **Sarah**: So automation that shaves time off your result pipeline goes straight to your competitiveness.
[00:01:16] **Hannah**: Exactly. Right now there's too much human-in-the-loop copying data between the instrument software, the LIMS, and the reporting system. Every manual step is a delay and an error risk.
[00:01:30] **Sarah**: OK. Ben, you'll want to dig into those systems. But first let me understand scale and stakeholders. Pieter, you're IT — are you the one who'd own this, or is it Hannah's team?
[00:01:42] **Pieter**: Joint. Hannah's team would build the lab-specific workflows, my team owns the platform, security, and integration standards. Lucia handles the commercial side.
[00:01:54] **Lucia**: And I'll be quiet until we get to numbers, then I'll be very loud.
[00:01:58] **Sarah**: Ha. Fair warning, appreciated.

[00:02:06] **Sarah**: Let me set pricing expectations early so it's not a surprise at the end. You're around what, 280 people who'd touch this?
[00:02:14] **Pieter**: Roughly. Maybe 280 across the labs and informatics. Not all heavy users but they'd need access.
[00:02:22] **Sarah**: At that scale you're squarely Enterprise. Enterprise is custom-priced — for a deployment of around 280 seats with your profile I'd estimate we'd land somewhere around $144K ACV, give or take depending on run volume and support needs. That's a ballpark to validate, not a quote. And just so you know the shape of the process — Enterprise deals for us are about a 90-day cycle including a POC and your security and procurement review.
[00:02:50] **Lucia**: $144K. Noted. We've budgeted in that vicinity so we're not wildly off.
[00:02:58] **Sarah**: Good, that's reassuring. We're in the same universe.

[00:03:06] **Ben**: OK let me understand the systems. Hannah, what's the LIMS?
[00:03:11] **Hannah**: It's a commercial LIMS — LabWare. The instruments speak various protocols, some emit files, some have APIs. The reporting system is custom, internal, with a REST API.
[00:03:24] **Ben**: OK. LabWare — does it have an API or are we file-based?
[00:03:30] **Hannah**: Both. There's a REST API for most things, but some of the older instrument integrations drop files into a watched folder.
[00:03:38] **Ben**: We can do both. REST API is straightforward — authenticated HTTP steps. The watched-folder pattern — we have a few options, the cleanest is if those files land somewhere we can poll, like an SFTP server or cloud storage bucket, and we trigger on new files. Do those files go anywhere network-accessible?
[00:03:58] **Hannah**: They land on an on-prem file share currently.
[00:04:04] **Ben**: On-prem is the one wrinkle. We're a cloud platform — we don't run an agent inside your network. So for on-prem file shares you'd either need to expose them via SFTP or sync them to a cloud bucket, or run a small relay. It's solvable but it's the kind of thing I'd want to scope carefully in a POC, because on-prem-to-cloud is where these projects get fiddly.
[00:04:28] **Pieter**: We're moving to cloud storage for new lab data anyway, so for go-forward workflows this is fine. The legacy on-prem stuff is being deprecated.
[00:04:38] **Ben**: That makes it much easier. If we focus the POC on the go-forward cloud-based flows and treat the legacy on-prem as out of scope, we avoid the fiddly part entirely.
[00:04:48] **Hannah**: That's the right scoping. The legacy stuff is dying, I don't want to build new automation on it.

[00:04:58] **Pieter**: Security question, since we're healthtech-adjacent — we handle some patient-derived samples, so there's data sensitivity. Do you sign a BAA? Where does data live? And what's your SOC2 situation?
[00:05:12] **Ben**: Yes BAA, we sign one. Data residency — you're EMEA so you'd be provisioned in our EU region, Amsterdam, so data and logs stay in-region for GDPR. SOC2 Type II, audited annually, shareable under NDA. And for the data-in-logs concern, we have a per-step sensitive-output flag that redacts payloads from logs — important for anything patient-derived.
[00:05:38] **Pieter**: EU region is essential, good. Send me the SOC2 under NDA and I'll start the security review in parallel with the POC.
[00:05:46] **Sarah**: Will do. Running security in parallel with the POC is exactly how we keep the 90-day cycle on track — if security waits until the POC passes, it adds a month. Starting now is the right move.

[00:05:58] (Ben does a ~14 min technical demo focused on a file-triggered workflow and a REST-API-to-REST-API data sync. Gong AI summary: Hannah impressed by the file-trigger reliability and the error visibility; Pieter focused on the audit log and access controls; one open question on LabWare API rate limits deferred to POC. Lucia mostly silent.)

[00:20:30] **Hannah**: This is genuinely better than I expected. The error visibility is the thing — right now when something fails in our manual process we find out when a client asks where their results are. Seeing a failed run with a reason code immediately is a different world.
[00:20:48] **Ben**: That's the whole pitch in one sentence. The error codes are specific too — AUTH_FAILED, RATE_LIMITED, INTEGRATION_DOWN, SCHEMA_MISMATCH — so your team knows what broke without spelunking through logs.
[00:21:02] **Hannah**: SCHEMA_MISMATCH especially — instrument software updates change data formats constantly and right now it silently corrupts downstream. Catching that explicitly would save us.

[00:21:14] **Lucia**: OK now I get loud. We're evaluating you against Tray and against just expanding our existing Workato license — we have a small Workato footprint already. What's the differentiation and what's the commercial advantage?
[00:21:30] **Sarah**: On differentiation — Ben can speak to technical, but commercially: Workato expand-in-place is the path of least resistance for you, I won't pretend otherwise. Where we win is total cost at your scale plus the self-serve usability — Hannah's lab staff building their own flows rather than needing a Workato specialist. On price, I'd want to be competitive with your Workato expansion quote; if you share roughly what Workato wants for the equivalent scope, I can tell you honestly whether we can beat it or not rather than wasting your time.
[00:22:00] **Lucia**: Workato's expansion quote for the equivalent scope is around $165K.
[00:22:06] **Sarah**: Then we're competitive — my $144K ballpark is below that, and that's before we've talked annual-commit discount. So on pure price I think we can win. The question the POC needs to answer is whether the migration effort and the usability upside justify switching versus the convenience of staying on Workato. That's a real question and I'd rather you decide it on evidence.
[00:22:30] **Lucia**: That's a fair framing. I appreciate you not trashing the competitor.
[00:22:36] **Sarah**: Trashing competitors is a bad look and usually backfires. Workato's a real product. We just think we're a better fit for your specific shape — self-serve lab staff, EU residency, this price point.

[00:22:48] (Discussion of POC structure and success criteria, ~12 min. Gong AI summary: agreed to a 45-day POC focused on 3 go-forward cloud-based lab workflows; success = reliable file-triggered ingestion + REST sync + Hannah's staff building independently; security review runs in parallel; Lucia to share Workato renewal terms for a true commercial comparison. Pieter flags that final sign-off needs their CISO, who is out until October.)

[00:35:20] **Pieter**: One scheduling reality — our CISO is on leave until October 6th, and she has final sign-off on any new data-processing vendor. So even if the POC flies, we can't sign before she's back and reviews.
[00:35:36] **Sarah**: Totally understand, and thank you for flagging it now rather than at the finish line — that's the kind of thing that blows up a forecast. So let's plan around it: POC runs late September through early November, security questionnaire to your CISO so it's waiting for her when she's back October 6th, and we target signature for mid-November. That keeps a clean 90-ish day cycle and respects her review.
[00:36:02] **Pieter**: That timeline works and is realistic.
[00:36:08] **Lucia**: Mid-November also fits our budget cycle. We have budget this fiscal year that we'd rather not lose, so closing in November is actually ideal.
[00:36:18] **Sarah**: Even better — use-it-or-lose-it budget is a great forcing function. Let's hold mid-November.

[00:36:28] **Sarah**: Action items, let me land them. Ben sends the SOC2 report and pre-filled security questionnaire to Pieter under NDA this week, and sets up the 45-day POC workspace in the EU region. Hannah nominates two or three lab-informatics people to build during the POC. Lucia shares the Workato renewal terms so I can build a real side-by-side. Pieter routes the security questionnaire to the CISO for review when she's back October 6th. We target signature mid-November. Did I capture everything?
[00:37:00] **Hannah**: Yes, I'll nominate my people this week.
[00:37:04] **Pieter**: NDA coming so you can send the SOC2.
[00:37:08] **Lucia**: I'll share the Workato terms under our NDA as well.
[00:37:12] **Sarah**: Perfect. This is a well-scoped one, I'm optimistic. Thank you all.
[00:37:18] (call ends)

---

## Acme post-call read (Gong + AE notes)

- **Stage**: Partner-sourced discovery → POC agreed (45 days). ~90-day enterprise cycle, gated on CISO return (Oct 6) + procurement.
- **Account**: `cust_000714` Quartz Foundry, Enterprise, 280 seats, $12,000 MRR / $144K ACV target, EMEA/healthtech, partner (Lumen). CSM Olivia Tran, AE Sarah Chen.
- **Forecast**: ~$144K ACV, below Workato's $165K equivalent quote → price-competitive. Books to `bookings_attribution` (already-annualized ACV), first_touch_channel = partner, on close-won.
- **Scoping win**: legacy on-prem file shares ruled OUT of scope (Acme is cloud, no in-network agent); POC focused on go-forward cloud-storage-based flows. Avoids the fiddly on-prem-to-cloud relay problem.
- **Security**: BAA yes, EU/Amsterdam residency (GDPR), SOC2 Type II under NDA, sensitive-output redaction for patient-derived data. Review runs in PARALLEL with POC; CISO final sign-off gated to Oct 6.
- **Competitive**: Workato expand-in-place (incumbent small footprint, $165K quote) vs Tray. Acme price-competitive; POC must justify migration effort vs. convenience of staying.
- **Action items**: Ben — SOC2 + questionnaire under NDA + EU POC workspace; Hannah — nominate 2–3 builders; Lucia — share Workato terms; Pieter — route questionnaire to CISO for Oct-6 review; target signature mid-Nov.

---

## Gong call — Yarrow Logistics — renewal + expansion — 2026-01-20

**Type**: Renewal (Business) with seat-expansion thread
**Time**: 2026-01-20, 16:00–16:43 AEDT
**Acme attendees**: Omar Haddad (AE), Marco Silva (CSM)
**Customer attendees**: Wei Zhang (Head of Operations), Fiona Patel (Ops Systems Lead), Geoff Tran (Finance Business Partner — joined 16:22)
**Account**: `cust_000703` Yarrow Logistics — Business / 120 seats / $17,880 MRR ($214,560 ARR) / APAC / logistics / event
**Source**: Existing Business customer, renewal due 2026-02-28
**Duration**: 00:43:50
**Sentiment trace (Gong AI)**: Positive 62% / Neutral 31% / Negative 7%

[00:00:06] **Omar**: Morning Wei, morning Fiona — well, evening for me but morning your side. Thanks for the early call.
[00:00:13] **Wei**: Ha, we appreciate you taking the APAC-friendly slot, Omar. I know it's late for you.
[00:00:19] **Omar**: All part of the service. Marco's on too — he's been your CSM through the year. So this is the renewal conversation, your term's up end of February, and Marco tells me there might be an expansion angle too, which is the fun part. How's the start of the year treating you?
[00:00:38] **Wei**: Busy. Post-holiday shipping volume is wild. Which honestly is a good advertisement for automation — we'd have drowned without it.
[00:00:47] **Omar**: That's exactly the testimonial I like to hear before a renewal.

[00:00:54] **Marco**: Let me give the health picture before we talk numbers. Yarrow, you're on Business, 120 seats. Over the last 28 days you had 88 active users — utilization about 0.73, which is genuinely high for Business and well into what we'd call healthy-expansion territory. Run volume's been climbing: you did about 1.2 million runs last quarter, success rate 99.1%. You're a model account honestly.
[00:01:24] **Wei**: 0.73 utilization — is that good? I don't know the benchmark.
[00:01:30] **Marco**: It's very good. For context, on Business we consider a customer "engaged" if they've got at least three active users and at least ten successful runs in a trailing 28-day window — that's the floor. You're at 88 active users and over a million runs, so you're not just engaged, you're heavily adopted. And utilization above 0.6 with strong engagement is what we flag internally as a healthy-expansion account — meaning you're using your seats so well that you've probably outgrown them.
[00:02:00] **Fiona**: That actually matches what we're feeling. We keep running into "we're out of seats" — people want access and we have to deny them or recycle seats.
[00:02:10] **Omar**: And there's the expansion thread. So before we even get to renewal pricing, it sounds like the real conversation is "how many seats do you actually need."

[00:02:22] **Wei**: Right. So let me lay it out. We're at 120 seats. We have probably 30 to 40 more people who want access — we've been rationing. And we're opening a new distribution hub in Singapore in Q2 that'll add maybe 30 more ops people who'll need it.
[00:02:42] **Omar**: So you're looking at 120 going to, call it 180 to 190 over the next couple quarters.
[00:02:50] **Wei**: Realistically yes.
[00:02:54] **Omar**: OK. So here's how I'd structure this. Rather than renewing at 120 and then doing a messy mid-term expansion in Q2 when Singapore comes online, let's renew at a seat count that reflects where you're going. If we renew at, say, 180 seats now, we lock the rate for the whole envelope and you stop rationing immediately. The alternative — renew at 120, expand later — means the Singapore seats get added mid-term and you're managing two events.
[00:03:24] **Wei**: What's the cost difference, roughly?
[00:03:28] **Omar**: At Business list, $149 a seat. 120 seats is $17,880 a month, your current $214,560 a year. 180 seats would be $26,820 a month, about $321,840 a year at list. That's the list jump for 60 more seats. But — this is an annual renewal with a meaningful seat increase, so there's room for a commit discount on the larger number. Let me talk through that.
[00:03:58] **Wei**: Please, because that's a big jump.
[00:04:02] **Omar**: It is, but it's 50% more seats, so per-seat it's the same — you're not paying more per person, you're just covering more people. On the discount: for a one-year renewal at 180 seats I can do something off list given the expansion. And if you'd consider a two-year, I can do better. What's your appetite on term length?

[00:04:24] (Wei and Fiona discuss internally ~3 min — they're open to two years given how embedded Acme is. Gong AI summary: customer comfortable with multi-year given high adoption; wants the Singapore seats included; sensitive to the absolute dollar jump and will need finance sign-off. Marco notes the high utilization de-risks the renewal.)

[00:07:30] **Wei**: We'd consider two years. We're not going anywhere — we're too embedded to switch and frankly we don't want to. What can you do on two years at 180 seats?
[00:07:42] **Omar**: For a two-year commit at 180 seats with annual billing, I can do 12% off list. So 180 seats at $149 less 12% is about $131 a seat effective, roughly $23,600 a month, about $283K a year. Versus the $321K list, that's about $38K a year saved, and it locks your rate for two years against any list increases — and we have raised Business list before, so that lock has real value.
[00:08:12] **Fiona**: So $283K a year for 180 seats, two years, versus $214K today for 120. We're paying $69K more a year but for 50% more capacity and we stop rationing.
[00:08:26] **Omar**: Exactly the right way to frame it. The per-seat economics improve and you solve the seat-rationing pain plus pre-fund Singapore. But I want your finance person comfortable with the absolute number — is that Geoff?
[00:08:40] **Wei**: Yes, let me see if Geoff can join.

[00:08:48] (brief pause, Geoff joins)
[00:08:52] **Geoff** (joining): Hi, Geoff here, finance. Wei texted me the shape — 180 seats, two years, about $283K a year. Walk me through versus today.
[00:09:04] **Omar**: Today you're at $214,560 a year for 120 seats. Proposal is 180 seats, two-year commit, 12% off list, about $283K a year. The increase is capacity — 50% more seats — at a per-seat rate that's actually lower than your current per-seat because of the commit discount. And it pre-funds your Singapore hub so you don't do a mid-year budget ask.
[00:09:30] **Geoff**: The pre-funding Singapore point is the one that lands for me. If I approve 180 now, I don't get a surprise expansion request in Q2 that I haven't budgeted. I'd rather one clean number now. Is the two-year locked, or can they raise on us at the 12-month mark?
[00:09:48] **Omar**: Locked. Two years, rate fixed, no mid-term increase. That's the point of the commit. The only thing that would change the bill is if you add seats beyond 180, which would be incremental at the same locked rate.
[00:10:02] **Geoff**: Then I'm inclined to approve, subject to seeing it on paper. $283K a year, two years, 180 seats, rate locked.
[00:10:12] **Omar**: That's the deal. I'll get the renewal order form drafted at exactly those terms.

[00:10:20] (Discussion of renewal timing and provisioning the extra 60 seats, ~10 min. Gong AI summary: agreed to renew at 180 seats / 2yr / 12% off list / ~$283K ACV; extra 60 seats provisioned immediately on signature to stop rationing; Singapore team onboards in Q2 within the already-licensed envelope; Marco to build a Singapore onboarding plan.)

[00:20:40] **Marco**: On the Singapore onboarding — I'll put together a rollout plan so the new hub team is productive fast. I'd suggest a one-hour training for their ops leads, same as we did for your original team, plus the template library you've already built so they're not starting from scratch.
[00:20:58] **Fiona**: That'd be great. Reusing our existing templates for Singapore is exactly right — no need to reinvent.
[00:21:06] **Marco**: Exactly. Your existing flows become the Singapore starting point.

[00:21:14] **Omar**: OK let me land the actions. I draft the renewal order form — 180 seats, 24-month term, 12% off Business list, about $283K ACV, rate locked, annual billing. Geoff reviews and signs assuming it matches what we discussed. We provision the extra 60 seats on signature so you stop rationing immediately. Marco builds the Singapore onboarding plan for Q2. Renewal target signed before your February 28 expiry. Everyone good?
[00:21:44] **Wei**: Good. Send it to Geoff and me.
[00:21:48] **Geoff**: I'll turn it around quickly if it matches.
[00:21:52] **Fiona**: And I'm just happy to stop telling people no on seats.
[00:21:57] **Omar**: Then we've done our job. Thanks for the early call, all. Go enjoy your morning, I'm going to enjoy my evening.
[00:22:05] (call ends)

---

## Acme post-call read (Gong + AE/CSM notes)

- **Stage**: Renewal due 2026-02-28 + expansion → verbal at expanded seat count. Finance-approved pending paper.
- **Account**: `cust_000703` Yarrow Logistics, Business, 120 → 180 seats, $17,880 MRR / $214,560 ARR today, APAC/logistics, event-sourced. CSM Marco Silva, AE Omar Haddad.
- **Renewal terms**: 180 seats, 24-month commit, 12% off Business $149 list (~$131/seat effective), ~$283K ACV/yr, rate locked, annual billing. Up from $214,560 (50% more capacity, lower per-seat).
- **Health**: utilization 0.73 (high for Business), 88 active users / 120 seats, 1.2M runs/qtr, 99.1% success. Well past engaged floor (≥3 active users AND ≥10 successful runs / 28d); utilization >0.6 + engaged = healthy-expansion flag → the data predicted this expansion.
- **Bookings note**: AE-led renewal+expansion → the incremental/renewed ACV is opportunity-sourced and lands annualized in `bookings_attribution`. (Contrast: a self-serve Free→Paid conversion would NOT.)
- **Action items**: Omar — renewal order form (180 seats / 24mo / 12% off / ~$283K / rate-locked / annual); Geoff signs if matches; provision +60 seats on signature; Marco — Q2 Singapore onboarding plan reusing existing templates; close before Feb-28 expiry.

---

## Gong call — Sable Analytics — Pro-to-Business expansion — 2025-11-12

**Type**: Expansion (AE-led, Pro → Business upgrade)
**Time**: 2025-11-12, 10:00–10:38 CET
**Acme attendees**: Sarah Chen (AE), Marco Silva (CSM)
**Customer attendees**: Lars Eriksson (VP Data), Mira Hassan (Analytics Engineering Lead)
**Account**: `cust_000710` Sable Analytics — Business / 90 seats / $13,410 MRR / EMEA / fintech / partner
**Source**: Existing customer; was on Pro, CSM-flagged for Business upgrade after seat + compliance growth
**Duration**: 00:38:20
**Sentiment trace (Gong AI)**: Positive 65% / Neutral 30% / Negative 5%

> *Note from Gong: this account's tier transition (Pro→Business) happened during the period this call covers. Header reflects the post-upgrade Business state (90 seats, $13,410 MRR). At call time they were on Pro and growing past it.*

[00:00:05] **Sarah**: Hi Lars, hi Mira. Good morning. Can you hear me?
[00:00:09] **Lars**: Morning Sarah, yes, clear.
[00:00:12] **Sarah**: Great. Marco's on too, your CSM. So the reason for the call — Marco flagged that you've been growing fast on Pro and bumping into some of its limits, and I wanted to talk through whether it's time to move you to Business. This is genuinely about fit, not a hard upsell — if Pro still works for you we'll leave you there. But Marco's seeing some signals. Marco, you want to set it up?
[00:00:36] **Marco**: Yeah. So Sable, you've been a great Pro customer — you came in through our partner channel, started small, and you've grown. You're now at, what, 48 people with logins and you've been asking about SSO and an audit trail. And you've been creeping toward the Pro run cap — you hit 9,200 runs last month against the 10K Pro ceiling. So you're bumping the edges of Pro on three fronts: seats, compliance features, and run volume.
[00:01:06] **Lars**: Yeah, the run cap scared me last month. We got an alert that we were near the limit and I didn't love the idea of workflows just stopping.
[00:01:16] **Sarah**: Right, and that's the thing — on Pro, if you blow the 10K cap, runs get throttled, which for a data team is exactly the wrong time for things to stop. Business takes you to 100K runs a month, so you'd have 10x headroom. Plus you get SSO and the audit log you've been asking about, and priority support.
[00:01:38] **Lars**: SSO is becoming a requirement for us actually. We're a fintech-adjacent analytics company and our enterprise clients are starting to ask about our internal security posture in their vendor reviews. "Do your internal tools use SSO" is now a checkbox we have to tick.
[00:01:58] **Sarah**: That's a really common driver for the Pro-to-Business move — it's not that Pro stopped working, it's that your customers' security teams force the issue. Business gives you SSO via SAML, audit logging for the "who did what" trail, and that satisfies most vendor-security questionnaires.
[00:02:18] **Mira**: The audit log we genuinely need too. We had an incident where a workflow got changed and broke a client report and we couldn't easily see who changed it or when. On Pro there's basic history but not a real audit trail.
[00:02:34] **Marco**: Right, Business audit logging gives you the full who-changed-what-when, exportable. That incident is exactly the use case.

[00:02:44] **Lars**: OK so what's the cost? We're at — what are we paying now?
[00:02:50] **Marco**: On Pro you're at 48 seats times $49, so about $2,350 a month, roughly $28K a year.
[00:02:58] **Sarah**: And here's the thing about moving to Business — Business has a 50-seat minimum. You're at 48, so you're essentially already there. Business is $149 a seat. The question is how many seats you actually provision. If you're at 48 active and growing, I'd suggest provisioning to where you're heading. What's your headcount trajectory?
[00:03:22] **Lars**: We're hiring. We'll be at 70, 80 people touching this within six months. The analytics team is doubling.
[00:03:30] **Sarah**: So let's size for that. If we go 90 seats Business — covering your growth — that's 90 times $149, about $13,410 a month, roughly $161K a year at list. That's a big jump from $28K, I won't sugarcoat it, because you're moving from a small-team plan to a team plan with enterprise-grade features and 10x the runs. But on a per-person basis for a fintech that needs SSO and audit, it's well within market.
[00:04:00] **Lars**: That is a big jump. Let me think about the seat count. 90 feels like a lot when we're at 48 today.

[00:04:10] **Sarah**: Totally fair, and I don't want to oversize you. Let's be honest about it. Two options. Option A: provision 50 seats — the Business minimum — at $149, about $7,450 a month, $89K a year. Covers you today with a little headroom, and you add seats as you hire. Option B: provision 90 now to lock the rate and pre-fund the doubling, $161K a year, but you're paying for seats ahead of filling them. Most customers in your spot start at the minimum and expand, unless they're confident about the hiring and want to lock rate. Given you're at 48 today, starting at 50 and expanding as you hire is probably the lower-risk move.
[00:04:48] **Lars**: That's good advice actually. I'd rather start at 50 and grow into it than pay for 40 empty seats.
[00:04:56] **Sarah**: Then let's do 50 Business. You can add seats anytime — they're just incremental at the same rate — so as your team doubles you scale up without re-papering. No penalty for growing.
[00:05:10] **Mira**: And the run cap goes to 100K immediately at 50 seats?
[00:05:14] **Marco**: Yes, 100K runs is a Business-tier feature regardless of seat count. So your run-cap anxiety goes away on day one.
[00:05:22] **Mira**: That alone is worth it.

[00:05:30] (Discussion of migration from Pro to Business — what changes, SSO setup, data continuity. ~12 min. Gong AI summary: confirmed Pro→Business is in-place, no data migration, workflows untouched; SSO setup via their Okta takes ~a day with Marco's help; audit logging on immediately; agreed to 50 Business seats with expansion as they hire. Lars comfortable with $89K/yr starting point.)

[00:18:00] **Lars**: OK I'm convinced. 50 Business seats, we'll grow it as we hire. SSO and audit are the clinchers — our clients are basically forcing it. When can we have it live?
[00:18:14] **Marco**: SSO setup I can do with your IT this week — about a day of work, mostly waiting on Okta config. Audit logging is on the moment you're on Business, no setup. The tier change itself is instant once the order form's signed.
[00:18:26] **Sarah**: I'll draft the order form today — 50 seats Business, $149/seat, $7,450/month, $89K annualized, annual term. Since you're an existing customer moving up, it's a simple upgrade order, not a new contract. Lars, who signs?
[00:18:44] **Lars**: I can sign up to $100K, so this is within my authority. Send it, I'll sign this week.
[00:18:52] **Sarah**: Perfect, that makes it fast.

[00:19:00] **Sarah**: Action items: I draft the Pro→Business upgrade order form today, 50 seats, $89K annualized. Lars signs this week. Marco coordinates SSO setup with your IT and confirms audit logging is live. We provision the tier change on signature. And Marco, schedule a check-in in 60 days to see if they need more seats as hiring ramps. Sound right?
[00:19:24] **Lars**: Sounds right. Thanks for not overselling me on the 90 seats, genuinely.
[00:19:30] **Sarah**: Overselling you into seats you don't fill is how I lose you at renewal. I'd rather you expand because you grew than resent paying for empty seats.
[00:19:40] **Mira**: Refreshing. Thanks both.
[00:19:44] (call ends)

---

## Acme post-call read (Gong + AE/CSM notes)

- **Stage**: Existing Pro customer → Business upgrade verbal (AE-led expansion). Within signer authority, fast close.
- **Account**: `cust_000710` Sable Analytics, transitioning Pro→Business, landing 50 seats now (header reflects later 90-seat / $13,410 MRR state as they grow), EMEA/fintech, partner-sourced. CSM Marco Silva, AE Sarah Chen.
- **Upgrade**: from 48 Pro seats (~$28K/yr) to 50 Business seats ($149/seat, ~$89K annualized), expand-as-they-hire toward ~90. In-place tier change, no data migration.
- **Drivers** (the classic Pro→Business triggers, all three present): (1) seats crossing ~50, (2) SSO + audit log forced by their own clients' vendor-security reviews, (3) run volume nearing the 10K Pro cap (hit 9,200/10K) → Business 100K cap removes throttle risk.
- **Bookings note**: this is an AE-led expansion (opportunity-sourced), so the annualized upgrade ACV lands in `bookings_attribution`. (Contrast: the original self-serve Free/Pro signup would NOT have been in bookings.)
- **Action items**: Sarah — upgrade order form today (50 Business seats / ~$89K annualized / annual term); Lars signs this week (within $100K authority); Marco — Okta SSO setup w/ IT + confirm audit log live; provision on signature; 60-day seat-growth check-in.

---

## Gong call — Tamarind Group — at-risk renewal save attempt — 2025-12-09

**Type**: Renewal save / at-risk intervention (Business)
**Time**: 2025-12-09, 13:00–13:46 ET
**Acme attendees**: Marco Silva (CSM), Sarah Chen (AE), Elena Volkov (VP CS — joined 13:30)
**Customer attendees**: Brenda Coyle (Director of Operations), Aaron Feldman (IT Manager)
**Account**: `cust_000706` Tamarind Group — Business / 55 seats / $8,195 MRR / NA-East / insurance / referral
**Source**: Existing Business customer flagged at-risk (low utilization, leadership change); renewal due 2026-01
**Duration**: 00:46:10
**Sentiment trace (Gong AI)**: Positive 38% / Neutral 44% / Negative 18%

[00:00:06] **Marco**: Hi Brenda, hi Aaron. Thanks for taking the time. I wanted to have an honest conversation about where things stand with your account ahead of your January renewal, because I've seen some signals I want to talk through openly rather than just send you a renewal quote and hope.
[00:00:24] **Brenda**: I appreciate the directness, Marco. I'll be equally direct — we're not sure we're renewing at the current level. There's been a leadership change and the new VP is reviewing all software spend.
[00:00:38] **Marco**: That's exactly the kind of thing I'd rather hear now than in January. Let me share what I'm seeing on usage, and then I want to understand the leadership-review angle, because those are two different problems.
[00:00:52] **Brenda**: Go ahead.

[00:00:58] **Marco**: So Tamarind, you're on Business at 55 seats — which is right at our 50-seat minimum, by the way. Over the last 28 days you had 14 active users out of 55 seats. That's a utilization of about 0.25. For context, that's on the low side — when utilization drops below about 0.20 we start flagging accounts as needing attention, and you're just above that line but trending down. A quarter ago you were at 0.34. So adoption has been slipping.
[00:01:30] **Brenda**: That tracks with what's happened internally. We had a reorg — the team that was the heaviest user got split up and half of them moved to a different division that doesn't use Acme.
[00:01:42] **Marco**: That explains the drop. So it's not that the product stopped delivering, it's that your power-user team got dispersed.
[00:01:50] **Brenda**: Right. The people still using it love it. There's just fewer of them now.
[00:01:56] **Aaron**: From IT's side, the workflows that are running are running fine. We've had basically zero support issues. It's purely a "fewer people using it" situation, not a "it's broken" situation.
[00:02:08] **Marco**: That's important and I want to make sure it's on the record — your engagement quality is fine, your run reliability is fine, this is a seat-count-versus-usage mismatch, not a product problem.

[00:02:22] **Brenda**: Correct. And that's the problem the new VP is going to see — we're paying for 55 seats and using 14. That looks bad on a spend review.
[00:02:32] **Marco**: It does, and honestly if I were your VP I'd flag it too. So let's fix the mismatch rather than lose the relationship. You're at 55 seats because that was just above our minimum when you signed. You're using 14. The Business minimum is 50 seats. So here's the honest tension — I can't take you below 50 seats and keep you on Business, because 50 is the floor for Business-tier features like your SSO and audit log.
[00:03:00] **Aaron**: We do use SSO. That's wired into our Okta and we'd want to keep it.
[00:03:06] **Marco**: Then there are really two paths, and I want to lay them both out honestly. Path one: you stay on Business but right-size to the 50-seat minimum — that drops you from 55 to 50 seats, a small reduction, keeps SSO and audit, but it's only a modest saving because you're already near the floor. Path two: if your real usage is going to stay around 14 people, you drop to Pro — $49 a seat, no minimum — but you lose SSO and the audit log. For 14 seats Pro is about $686 a month versus your current $8,195. Huge saving, but you lose the compliance features.
[00:03:42] **Brenda**: The saving on Pro is dramatic. But Aaron, can we live without SSO?
[00:03:48] **Aaron**: That's the rub. Our security policy mandates SSO for any system with access to operational data. Dropping to Pro would mean either a policy exception or wiring up some workaround, and I don't love either.
[00:04:02] **Marco**: That's a real constraint and I don't want to talk you out of your own security policy. So the cleaner answer might be path one — right-size to 50 Business seats, keep SSO and audit, and the saving is smaller but you stay compliant. The 55-to-50 reduction isn't huge but it's a gesture toward the spend review, and the compliance story stays intact.

[00:04:24] (Brenda and Aaron discuss internally ~4 min — the tension between the dramatic Pro saving and the SSO mandate. Gong AI summary: customer torn; the new VP wants maximum saving, but IT's SSO mandate constrains the Pro option; no decision reached; customer wants to bring the new VP into a follow-up. Marco positions a paused/downgrade option as better than churn.)

[00:08:40] **Brenda**: I think we need our new VP in the room. The decision is really hers now. Can we do a follow-up with her? She's the one weighing the spend.
[00:08:52] **Marco**: Absolutely, and I'd welcome it. I'd rather she hear the options directly than get them secondhand. Let me also bring our VP of Customer Success, Elena, into that conversation — actually let me see if she can join the last few minutes of this one to introduce herself, because for an at-risk renewal I want you to know you've got senior attention.
[00:09:10] **Brenda**: That'd be good.

[00:09:18] **Sarah**: Brenda, this is Sarah — I'm the account exec. One option I want to put on the table for your VP's consideration, just so she has the full menu: we also have a pause option. If there's uncertainty about headcount — like if that dispersed team might come back, or there's a reorg in flux — rather than downgrade or churn, we can pause the subscription for up to 90 days. You keep your data and workflows, you're not billed during the pause, and you reactivate when the picture's clearer. It's not a long-term answer but it's a pressure valve if the VP wants time to decide without paying.
[00:09:54] **Brenda**: I didn't know pause was an option. That might actually be the right move given how in-flux we are.
[00:10:02] **Sarah**: It's there precisely for situations like yours — genuine uncertainty rather than a clear decision. It beats churning and then having to re-onboard if things stabilize.

[00:10:14] (Discussion of the three options — right-size to 50 Business, drop to Pro with SSO tradeoff, or pause — and what each means operationally. ~14 min. Gong AI summary: customer leaning toward either pause or right-size-to-50; the new VP's spend mandate vs. the SSO compliance requirement is the core tension; follow-up scheduled with the VP; Marco and Sarah aligned that retaining the logo even at reduced/paused value beats churn.)

[00:26:30] **Elena** (joining): Hi Brenda, hi Aaron, sorry to jump in late — I'm Elena, VP of Customer Success. Marco caught me up. I just wanted to introduce myself and say: we understand you're in a spend review and a leadership transition, and our goal isn't to defend a number, it's to find the structure that keeps Acme valuable to you at whatever scale makes sense right now. Whether that's right-sizing, a pause, or a different tier — we'd rather keep the relationship and have you grow back than lose you over a seat-count mismatch that's really a reorg artifact.
[00:27:04] **Brenda**: That's a reassuring thing to hear from a VP. Thank you. I think the next step is getting our new VP into a room with you all.
[00:27:14] **Elena**: We'll make ourselves available whenever works for her. And I'll personally make sure whatever we land on is fair given the circumstances.

[00:27:26] **Marco**: OK action items. I'll schedule the follow-up with your new VP — Brenda, you'll send me her availability. We'll present three clear options: right-size to 50 Business keeping SSO/audit, drop to Pro at 14 seats with the SSO tradeoff to weigh, or a 90-day pause if the headcount picture's still in flux. Sarah owns the commercial paperwork for whichever path. Elena's available for the VP conversation. Goal: land this before the January renewal date with a structure that fits your new reality. Does that work?
[00:28:00] **Brenda**: That works. I'll get you her availability today.
[00:28:06] **Aaron**: And I'll document our SSO requirement formally so the VP understands the constraint on the Pro option.
[00:28:14] **Marco**: Perfect, that documentation will help the conversation. Thank you both for the candor — this is exactly how I like to handle a renewal, eyes open.
[00:28:24] (call ends; ~30s retained off-camera: Marco to Sarah — "pause might be the realest option, that team could come back after the reorg settles"; Sarah — "agreed, better than a Pro downgrade that breaks their SSO policy. Let's not lose the logo.")

---

## Acme post-call read (Gong + CSM/AE notes)

- **Stage**: At-risk Business renewal (due 2026-01) → save attempt. No decision; follow-up with customer's new VP pending. Account already PAUSED in cast (status: paused 2026-01) — consistent with this in-flux trajectory.
- **Account**: `cust_000706` Tamarind Group, Business, 55 seats, $8,195 MRR, NA-East/insurance, referral-sourced. CSM Marco Silva, AE Sarah Chen.
- **Risk driver**: NOT product dissatisfaction — a reorg dispersed the power-user team. Utilization fell to ~0.25 (from 0.34), just above the 0.20 non-Enterprise critical threshold but trending down. Engagement quality + run reliability fine; new VP's spend review is the trigger.
- **Options presented**: (1) right-size to 50-seat Business minimum (keeps SSO/audit, modest saving); (2) drop to Pro at 14 seats (~$686/mo vs $8,195, huge saving) but lose SSO/audit — blocked by customer's own SSO security mandate; (3) 90-day pause (keep data/workflows, no billing) as a pressure valve given headcount uncertainty.
- **Note**: Business 50-seat minimum is a hard floor — cannot go below 50 and remain Business. Pro has no minimum but no SSO/audit.
- **Stance**: retain the logo at reduced/paused value over churn; senior attention (Elena/VP CS) signals the account matters.
- **Action items**: Brenda — send new VP's availability; Marco — schedule VP follow-up, present the 3 options; Aaron — document SSO requirement formally; Sarah — paperwork for chosen path; Elena — available for VP call; resolve before Jan renewal.

---

## Gong call — Helios Manufacturing — win/loss (closed-lost to Tray) — 2025-07-29

**Type**: Win/loss debrief (deal lost; prospect, no account created)
**Time**: 2025-07-29, 11:00–11:34 PT
**Acme attendees**: Yuki Sato (AE), Marcus Webb (VP Sales — joined 11:20)
**Customer attendees**: Devon Pryce (VP IT), Ana Lucia Reyes (Integration Architect)
**Account**: Opportunity `OPP-2025-0418` Helios Manufacturing (prospect, no `cust_*` created — closed-lost)
**Source**: Outbound; ran a 30-day eval, did not convert
**Duration**: 00:34:20
**Sentiment trace (Gong AI)**: Positive 30% / Neutral 52% / Negative 18%

[00:00:06] **Yuki**: Hi Devon, hi Ana. Thanks for doing this — I know you've made your decision and it wasn't us, so I really appreciate you giving me 30 minutes to learn from it. No sales here, I promise. I just want to understand what tipped it.
[00:00:22] **Devon**: Happy to, Yuki. You ran a clean process, so you've earned an honest debrief. It was a close call honestly.
[00:00:30] **Yuki**: That's both nice and painful to hear. OK — top line, what was the deciding factor?
[00:00:37] **Devon**: Two things. One, depth of complex integration logic. Two, we have an in-house integration team that already knows Tray.
[00:00:46] **Ana**: I'll take the technical one. We have some genuinely gnarly integration scenarios — multi-system transactional workflows where if step 3 of 6 fails, we need to roll back steps 1 and 2 in specific systems. Tray's lower-level control let us build that compensating-transaction logic. With Acme, your model is cleaner and honestly nicer for 80% of workflows, but for our gnarly 20% we kept hitting the ceiling of what your abstraction allowed.
[00:01:18] **Yuki**: That's really useful and I'm not going to argue it — that compensating-transaction, saga-pattern stuff is a known edge of our model. We optimize for the common case and the self-serve builder, and that's a deliberate tradeoff that costs us exactly the deals where deep custom control is the requirement.
[00:01:38] **Ana**: Right. And to be fair, your error handling and observability were better than Tray's out of the box. If 80% of our workflows were the whole story, you'd have won. But the 20% are mission-critical and they're where the complexity lives.
[00:01:54] **Yuki**: Understood. And the second factor — the in-house Tray team?
[00:02:00] **Devon**: We have four integration engineers who are Tray-certified. Switching to Acme means retraining them or losing that expertise. The switching cost in human terms was high, and your usability advantage — "your ops people can self-serve" — matters less to us because we don't want ops people building these, we want our specialist team building them. So your core value prop is partially wasted on our org structure.
[00:02:26] **Yuki**: That's a sharp insight actually. Our whole pitch is "democratize automation, let non-specialists build" — and for an org that deliberately centralizes integration in a specialist team, that pitch is a non-fit. You're the anti-persona for our positioning, in the nicest way.
[00:02:46] **Devon**: Ha, exactly. It's not that you're worse, it's that we're not your customer.

[00:02:54] **Yuki**: Can I ask about price — was that a factor at all, or purely fit?
[00:03:00] **Devon**: Price was actually slightly in your favor. Your quote was a bit lower than Tray's. But it wasn't enough to overcome the technical-fit and switching-cost factors. We'd have paid a small premium for the right fit, and Tray was the right fit for our specific complexity.
[00:03:18] **Yuki**: So I couldn't have discounted my way to this deal.
[00:03:22] **Devon**: No. Honestly if you'd come in 20% cheaper it wouldn't have changed it. The deciding factors weren't price.
[00:03:30] **Yuki**: That's clarifying, and frankly it's better than losing on price — price I can fix, fundamental fit I can't, and I'd rather know it's fit so I don't chase the wrong deals.

[00:03:42] **Marcus** (joining): Hey Devon, Ana — Marcus, VP of Sales, Yuki pulled me in for a minute because I always want to hear the lost-deal reasons firsthand. I heard "complex transactional logic" and "in-house Tray team." Anything on the product roadmap side that, if we'd had it, would've changed your mind? I'm trying to figure out if this is a roadmap gap we should close or a deliberate positioning boundary we should accept.
[00:04:10] **Ana**: Honest answer — it's more of a positioning boundary than a quick roadmap fix. The compensating-transaction stuff requires a lower-level execution model than you have. You could build it, but it'd compromise the simplicity that makes you good for the common case. I'd be careful chasing the complex 20% if it ruins the simple 80%.
[00:04:34] **Marcus**: That's exactly the strategic question, and you've answered it well. Thank you — that's the kind of input that shapes whether we go up-market into heavy custom or stay in our lane. Sounds like staying in our lane.
[00:04:48] **Devon**: For what it's worth, I'd recommend you to a company that wants self-serve automation in a heartbeat. We're just not that company. We're the specialist-team, deep-custom company.
[00:05:00] **Marcus**: That recommendation is worth a lot, genuinely. We'll take the loss and the referral.

[00:05:10] (Further discussion of where Acme fits vs. Tray in the market, ~10 min. Gong AI summary: loss attributed primarily to integration-complexity ceiling and incumbent specialist-team switching cost; price was favorable to Acme and not a factor; prospect is a structural non-fit for Acme's self-serve positioning; willing to refer Acme to self-serve-oriented orgs. No re-engagement path unless Acme adds low-level transactional control, which is a deliberate non-priority.)

[00:16:00] **Yuki**: Last question and then I'll let you go — anything about our sales process itself I could've done better? Separate from product fit.
[00:16:10] **Devon**: No, your process was good. Responsive, you didn't oversell, your SE was honest about the 20% limitation rather than hand-waving it — which actually built trust even though we didn't buy. If anything, the SE being upfront about the saga-pattern limitation early would've saved us both some POC time, but he got there.
[00:16:32] **Yuki**: That's fair feedback — surface the known limitations earlier in qualification so we both spend time wisely. I'll take that to heart.
[00:16:42] **Devon**: You ran it well. Sorry it wasn't us.
[00:16:46] **Yuki**: Me too, but thank you. And the referral offer stands? I might take you up on it.
[00:16:52] **Devon**: Absolutely. Send self-serve-oriented prospects my way as a reference, happy to vouch for the product's strengths.
[00:17:00] **Yuki**: Appreciate it, Devon. Thanks both.
[00:17:04] (call ends)

---

## Acme post-call read (Gong + AE notes)

- **Outcome**: CLOSED-LOST. Opportunity `OPP-2025-0418` Helios Manufacturing. No `cust_*` account created (never converted). AE Yuki Sato.
- **Loss reasons** (taxonomy): primary `feature_gap` (low-level compensating-transaction / saga-pattern control beyond Acme's abstraction); secondary `competitor` / switching cost (in-house Tray-certified specialist team).
- **Price**: NOT a factor — Acme quote was below Tray; would not have won even 20% cheaper. Clarifying that the loss is fit, not price.
- **Strategic note (Marcus)**: this is a deliberate positioning boundary, not a roadmap gap to chase. Helios is a structural anti-persona — specialist-team, deep-custom org vs. Acme's self-serve democratized-automation positioning. Decision: stay in lane, don't compromise the simple-80% to chase the complex-20%.
- **Silver lining**: prospect rated the sales process highly (honest SE, no overselling) and offered to be a REFERENCE for self-serve-oriented prospects. Feedback: surface known limitations earlier in qualification.
- **Bookings note**: closed-lost → nothing books. (Only closed-won opportunity ACV lands in `bookings_attribution`.)

---

## Gong call — Verdant Cloud — enterprise renewal (flat, low-utilization Enterprise) — 2026-03-03

**Type**: Enterprise renewal review
**Time**: 2026-03-03, 09:00–09:51 AEDT
**Acme attendees**: Omar Haddad (AE), Olivia Tran (CSM), Rachel Stein (CFO — joined 09:38)
**Customer attendees**: Sunil Rao (VP Engineering), Keiko Yamamoto (Procurement), Daniel Osei (Platform Lead)
**Account**: `cust_000707` Verdant Cloud — Enterprise / 260 seats / $8,000 MRR ($96K ACV) / APAC / ecommerce / inbound
**Source**: Existing Enterprise customer, renewal due 2026-04-15
**Duration**: 00:51:30
**Sentiment trace (Gong AI)**: Positive 47% / Neutral 43% / Negative 10%

[00:00:06] **Omar**: Morning Sunil, Keiko, Daniel. Evening for me, morning for you. Thanks for the slot. This is your renewal review — your Enterprise term's up April 15th — and I want to have a straight conversation, because Olivia's flagged that your usage profile is a bit unusual and I'd rather address it head-on than paper over it.
[00:00:26] **Sunil**: Morning Omar. Yeah, let's be straight. I know our usage is lighter than you'd probably like.
[00:00:33] **Omar**: Let's dig into it. Olivia, you want to set the picture?
[00:00:38] **Olivia**: Sure. So Verdant, you're on Enterprise at 260 seats — which is just above our 250-seat Enterprise minimum — at $8,000 MRR, so $96K ACV. That's actually a relatively low ACV for an Enterprise deal, which makes sense because your effective per-seat is low. Over the last 28 days you had 41 active users against 260 seats. Now — here's a nuance I want to be clear about. At Enterprise tier, we don't apply a utilization threshold the way we would for a smaller plan. You have unlimited runs and the seat count is just your licensing envelope, so there's no "you're under-utilizing your quota" problem — there's no quota. Your account health on our side is driven by whether you've had any uncollectible invoices, which you haven't — you pay on time, you're a clean account.
[00:01:30] **Sunil**: So we're not in trouble, we're just... light.
[00:01:34] **Olivia**: Exactly. You're a healthy, low-intensity Enterprise account. The 41 active users are engaged — well past our engagement floor of three active users and ten successful runs in 28 days — they're just a smaller slice of your 260 seats. There's no red flag in our system. The question for the renewal is whether 260 seats is the right envelope for you, or whether you're carrying seats you don't need.
[00:01:58] **Keiko**: That's the question I have too. We're paying for 260 and using 41. From procurement's chair, that looks like waste.

[00:02:08] **Omar**: It's a fair question and let's address it honestly. Here's the tension: you're at 260 seats, and the Enterprise minimum is 250 seats. So I literally cannot take you below 250 and keep you on Enterprise — 250 is the floor. You're only 10 seats above the floor as it is. So there isn't much room to "right-size down" within Enterprise.
[00:02:32] **Keiko**: So what are the options?
[00:02:38] **Omar**: Two real ones. Option one: renew Enterprise at the 250-seat minimum — that's a tiny reduction from 260, keeps all your Enterprise features, dedicated CSM, SLA, unlimited runs, SOC2. Minimal saving but it's the floor. Option two — and I'm putting it on the table even though it means a smaller deal for us — if your real usage is 41 people and you don't foresee growing past, say, the low hundreds, you might genuinely be a Business customer, not an Enterprise customer. Business is $149 a seat, no big minimum beyond 50. At, say, 60 seats Business you'd be about $107K a year — wait, let me recompute that, 60 times $149 times 12 is about $107K — hm, that's actually close to your current $96K. Let me think about whether Business even saves you money at your seat needs.
[00:03:28] **Daniel**: Yeah that math is interesting. At our usage, Business might not be cheaper.
[00:03:34] **Omar**: Right, let me work it live. Your current Enterprise is $96K for 260 seats — that's an effective $30-ish a seat, which is a very good Enterprise rate, below even Pro list. If you went Business at 60 seats — covering your 41 active plus headroom — that's 60 × $149 × 12 = about $107K. So Business would actually cost you MORE than your current Enterprise deal, because your Enterprise per-seat rate is so favorable. You negotiated a good Enterprise rate at some point and it's now cheaper than Business would be.
[00:04:08] **Keiko**: So downgrading to Business would cost us more? That's counterintuitive.
[00:04:14] **Omar**: It is, but it's because your Enterprise effective rate is unusually low. The lesson is your current deal is actually good value for you. The cleanest renewal is to stay Enterprise, possibly trim to the 250 minimum, and keep your favorable rate. Downgrading would lose you the dedicated CSM and SLA AND cost more. That's a rare situation where the bigger plan is the cheaper plan.
[00:04:40] **Sunil**: Huh. OK that reframes it. I came in thinking we should downgrade and you're telling me downgrading is worse for us.
[00:04:48] **Omar**: I'd be doing you a disservice to let you downgrade into a higher bill and fewer features. I'd rather keep you on the deal that's actually good for you, even if it means I'm not upselling you.

[00:04:58] (Discussion of why their usage is light — turns out they over-bought seats two years ago anticipating growth that went elsewhere. ~12 min. Gong AI summary: Verdant over-provisioned at original purchase; growth didn't materialize on the platform; but the favorable Enterprise rate makes staying Enterprise-at-minimum the economically rational choice; no churn risk; clean payer. Keiko satisfied that Business isn't cheaper.)

[00:17:30] **Keiko**: OK so if we renew Enterprise at 250 seats, what's the number and can we improve it?
[00:17:38] **Omar**: At 250 seats your effective rate holds — call it roughly $92K ACV, a small trim from $96K for the 10 fewer seats. On a renewal I can hold your rate flat, which given we've raised Enterprise pricing for new customers means your grandfathered rate is genuinely below what a new customer your size would pay. So "flat" is actually a win — you're locking a below-market rate for another term.
[00:18:08] **Keiko**: Can you do better than flat?
[00:18:14] **Omar**: Honestly, your rate is already so favorable that a further discount is hard to justify on my side — you're below market already. What I can offer instead of a price cut is term certainty: lock this below-market rate for two years so you're protected from the increases new customers are seeing. That's worth more than a small percentage cut on an already-low number.
[00:18:38] **Keiko**: Let me get our CFO's view on flat-versus-cut. Is your CFO available? Sometimes finance-to-finance lands better.
[00:18:48] **Omar**: Funny you ask — Rachel, our CFO, was going to join the back half. Let me bring her in.

[00:18:58] **Rachel** (joining): Morning all — Rachel Stein, CFO at Acme. Omar caught me up. Keiko, I understand you're weighing whether flat is the best we can do. Let me give you the finance-to-finance version: Verdant is on a grandfathered Enterprise rate that's materially below our current Enterprise pricing for comparable seat counts. Our current book has new Enterprise customers at meaningfully higher effective per-seat than you're paying. So when Omar says "flat," he's offering to extend a rate that we frankly wouldn't sell new today. A further cut isn't something I can approve on an already-below-market deal — but locking it for two years, I can absolutely do, and that protects you from the trajectory of our pricing.
[00:19:42] **Keiko**: That's a clear answer and I appreciate the directness. Below-market-locked-for-two-years is a reasonable outcome.
[00:19:52] **Sunil**: Agreed. Lock the rate, two years, 250 seats. We're not going anywhere — the platform works for the 41 people who use it, and apparently we're getting a good deal.
[00:20:04] **Rachel**: Then that's a clean renewal. Omar will paper it at your current effective rate, 250 seats, two-year term. From our side that books as the annualized renewal value — about $92K ACV — flowing through as a renewal booking. Nothing exotic.

[00:20:20] (Discussion of whether to try to drive more adoption to justify the seats, ~14 min. Gong AI summary: Olivia proposes an adoption campaign to get more of Verdant's org using the platform — if usage grows, the 260 seats get justified and expansion becomes possible; Sunil open to it but not committal; agreed Olivia will run a lightweight adoption push post-renewal. Keiko notes that even at 41 users the deal is good value, so there's no pressure.)

[00:35:00] **Olivia**: Even though the renewal's basically settled, I'd like to run a small adoption initiative after we sign — identify a couple of teams at Verdant that have manual processes Acme could automate, and see if we can grow your active users. Not to justify the spend, because the spend's already justified by the favorable rate, but because more value to you means a stronger relationship and maybe a real expansion down the line.
[00:35:30] **Sunil**: I'm open to it. There are definitely teams still doing things manually. Daniel, you could point Olivia at the obvious candidates.
[00:35:40] **Daniel**: Yeah, our fulfillment-ops team is still half-manual. That'd be a good target.
[00:35:48] **Olivia**: Perfect, I'll reach out to fulfillment-ops post-signature.

[00:35:56] **Omar**: OK let me land it. Renewal: Enterprise, 250 seats (trimmed from 260), current effective rate held flat, two-year term, about $92K ACV, rate locked against increases. Rachel's approved the flat-with-two-year-lock structure. I draft the renewal order form, Keiko routes it for signature before the April 15 expiry. Olivia runs a post-signature adoption push targeting fulfillment-ops. Anything missed?
[00:36:24] **Keiko**: That's complete. Send the order form.
[00:36:28] **Sunil**: Good. And thanks for talking us out of a downgrade that would've cost us more — that's not the sales call I expected.
[00:36:38] **Omar**: The best renewals are the honest ones. Thanks all, enjoy your morning.
[00:36:44] (call ends)

---

## Acme post-call read (Gong + AE/CSM notes)

- **Stage**: Enterprise renewal (due 2026-04-15) → verbal, flat-rate two-year lock. CFO-approved.
- **Account**: `cust_000707` Verdant Cloud, Enterprise, 260 → 250 seats, $8,000 MRR / $96K ACV, APAC/ecommerce, inbound. CSM Olivia Tran, AE Omar Haddad.
- **Renewal terms**: Enterprise at 250-seat minimum (trimmed from 260), current effective rate held FLAT (~$92K ACV at 250), 2-year term, rate locked. Flat = a win here because their grandfathered rate is below current Enterprise market.
- **Health nuance (canon [health])**: Enterprise utilization is NOT a health driver — no utilization_band for Enterprise (unlimited runs/seats). Enterprise critical ONLY on a recent uncollectible invoice; Verdant has none → clean/healthy. 41 active users are engaged (≥3 active + ≥10 successful runs/28d), just a small slice of 260 seats. Low-intensity but healthy.
- **Counterintuitive math**: downgrading to Business would cost MORE (~$107K at 60 seats) than their favorable Enterprise rate (~$96K at 260), because their effective Enterprise per-seat (~$30) is below even Pro list. The bigger plan is the cheaper plan here. Stayed Enterprise.
- **Enterprise 250-seat minimum** is a hard floor: cannot trim below 250 and remain Enterprise.
- **Bookings note**: renewal value (~$92K) books as an annualized renewal in `bookings_attribution` (already annual). Olivia to run a post-signature adoption push (fulfillment-ops) to grow active users toward a future expansion.
- **Action items**: Omar — renewal order form (Enterprise / 250 seats / flat rate / 2yr / ~$92K / rate-locked); Keiko signs before Apr-15 expiry; Olivia — post-signature adoption push targeting fulfillment-ops.

---


---

## Gong Transcript: Harbor Dynamics QBR (APAC/Insurance)
**Date**: 2026-02-12
**Participants**: Omar Haddad (Acme AE), Marco Silva (Acme CSM), Ananya Rao (Harbor Dynamics, Head of Ops), Hiroshi Tanaka (Harbor Dynamics, IT Lead)
**Account**: `cust_000713` Harbor Dynamics (Business, 150 seats, $22,350 MRR)

[00:00:15] **Ananya**: ...just saying the coffee culture in Melbourne is miles ahead of Sydney, Omar. Don't let the team there hear me say that. 
[00:00:22] **Omar**: (Laughs) I’ve learned to stay neutral in the city rivalries. But I’m glad we could jump on today. Marco, do you want to kick off with the usage stats?
[00:00:34] **Marco**: Definitely. Looking at the last 90 days in the warehouse — specifically `nexus-analyst-demo.acme.workflow_runs_daily` — Harbor is crushing it. You guys averaged about 88,000 successful runs per month. You’re right up against that 100,000 Business tier quota.
[00:01:02] **Ananya**: That explains why Hiroshi was flagging the alerts last week. Hiroshi, how many of those are the new claims-processing bots?
[00:01:10] **Hiroshi**: Most of them. We’ve moved about 40% of the ingestion logic out of our legacy system into Acme. But I’m seeing some `INTEGRATION_DOWN` errors on the Salesforce connector around 3 AM UTC. 
[00:01:25] **Marco**: I saw that in the `fact_workflow_runs` logs. It looks like a rate limit on the Salesforce side, not an Acme failure. We can actually build a retry logic with a jitter to fix that. 
[00:01:40] **Ananya**: Omar, we’re looking at adding another 40 people from the actuarial team next month. Does that change our pricing? I know we're on the Business plan at $149 a seat.
[00:01:54] **Omar**: At 190 seats, you’re still firmly in Business. The next jump is Enterprise at 250 seats. If you hit 250, we usually move you to a custom ACV with unlimited runs. Right now, with 190 seats, your monthly would be around $28,310. 
[00:02:15] **Ananya**: And what do we get at Enterprise? Is it just the seat count?
[00:02:22] **Omar**: It's more about the guardrails. You get the custom SLA, the dedicated CSM — which you already have with Marco because you're a high-value Business account — but primarily it’s the unlimited workflow runs and the SOC2 reporting that your legal team was asking about last year. 
[00:02:45] **Hiroshi**: If we go to Enterprise, do we get the Audit Log API? We’re currently using the UI for audit logs, but I want to stream those events into our Snowflake.
[00:02:55] **Omar**: Actually, Hiroshi, you have the Audit Log UI and basic exports on Business. The streaming API is technically an Enterprise feature, but for the expansion to 190 seats, I might be able to get Priya’s team to toggle the beta for you.
[00:03:15] **Ananya**: Let's see how the actuarial pilot goes. If they like the Tray-style canvas you guys have, we might hit 250 sooner than Q4. 
[00:03:25] **Marco**: Just a heads up, I’m seeing `utilization_band` for you guys at 0.72. That’s very healthy. Most of your 150 seats are logging in weekly.

---

## Slack Thread: #sales-ops-internal
**Date**: 2026-03-05

**tom.becker**: Hey @lina.cho, I’m looking at `acme.account_health` for Cobalt Systems (`cust_000700`). It’s showing `account_health_status = 'monitoring'`. Why aren't they 'healthy_expansion'? They have 80 seats and they're using almost all of them.
**lina.cho**: Hey Tom. Checking the definition... ah, they only have 2 active users in the last 28 days who have run a successful workflow. The `is_engaged` flag requires ≥3 active users. 
**tom.becker**: That’s weird. They have 80 seats licensed. You’re saying only 2 people are actually doing anything?
**lina.cho**: Correct. It looks like one is a service account and the other is their lead dev, Theo. The other 78 seats are provisioned but haven't triggered a run or logged in since Jan. 
**tom.becker**: Damn. I was going to pitch them on an expansion. If they aren't 'engaged' per the 2025-Q4 recalibration, I guess I should hold off?
**lina.cho**: Probably. If `is_engaged` is false, they won't trigger the expansion signal. Also, watch out for the `utilization_band`. It’s low because of the seat overhead. Marco might need to do a "train the trainer" session there.
**rajiv.menon**: Also Tom, just a heads up, don’t try to find the "Value Realization Score" in that table. I know Marcus mentioned it in the All Hands, but that spec is parked. Stick to `account_health_status`.

---

## Internal Note: Sable Analytics Renewal Strategy
**Date**: 2026-04-02
**From**: Sarah Chen (AE)
**To**: Elena Volkov (VP CS), Marco Silva (CSM)
**Subject**: Sable Analytics (`cust_000710`) – Enterprise Conversion Play

Sable is currently on the Business plan with 90 seats. They are paying $13,410 MRR (~$161K ARR). They just closed their Series C and are moving into the UK public sector market. 

**The Hook**: They need the custom SLA and the advanced audit log streaming for compliance.
**The Math**:
- Current: 90 seats @ $149 = $13,410/mo.
- Proposed: Enterprise Tier 250-seat minimum. Even if they only use 100 seats, the floor is 250.
- At our standard Ent entry pricing, we're looking at a $200K ACV floor ($16,666 MRR).
- This is a +$39K ARR expansion.

**Risk**: Their `account_health` is currently 'stable', but they had a recent P1 ticket (Ticket #8821) regarding a `SCHEMA_MISMATCH` on their BigQuery export that stayed open for 72 hours. This puts them at `at_risk` because of the `has_open_p1_over_48h` rule. Marco, can you confirm the resolution on that before I send the Enterprise order form? I don't want to ask for an upsell while the dev team is still annoyed about the BQ connector.

---

## BigQuery Snippet: `nexus-analyst-demo.acme.fact_support_tickets`
| ticket_id | customer_id | opened_at | priority | category | resolution_time_hours | csat_score |
|-----------|-------------|-----------|----------|----------|-----------------------|------------|
| tick_9012 | cust_000700 | 2026-03-01| P2       | connector| 14.5                  | 5          |
| tick_9015 | cust_000713 | 2026-03-04| P3       | billing  | 2.0                   | 4          |
| tick_9019 | cust_000707 | 2026-03-10| P1       | platform | 49.2                  | 2          |
| tick_9022 | cust_000710 | 2026-03-15| P1       | auth     | 73.0                  | NULL       |

---

## Gong Transcript: Discovery Call - Onyx Robotics (NA-West / DevTools)
**Date**: 2026-04-10
**Participants**: Tom Becker (AE), Olivia Tran (CSM), Sam V. (Onyx Robotics, VP Eng)
**Account**: `cust_000704` (Enterprise, 500 seats, $35,000 MRR)

[00:12:44] **Sam V**: ...right, so the issue with Zapier was just the lack of governance. We had engineers spinning up 500 tasks that were just looping and burning through the quota. 
[00:12:55] **Tom Becker**: That's exactly why we moved to the seat-based model for Enterprise. With 500 seats at Onyx, you don't have to worry about the "run-burn" anymore. It's all-you-can-eat on the workflow runs.
[00:13:10] **Sam V**: And the SOC2 report? Our procurement won't even look at the contract without the latest type II.
[00:13:18] **Olivia**: I can send that over right after this call, Sam. It's in the Secure-Portal. 
[00:13:25] **Sam V**: Perfect. Now, walk me through the integration with our internal internal tool. We have a custom API for our robot telemetry. Can Acme handle custom headers for HMAC auth?
[00:13:40] **Tom Becker**: (Pauses) Olivia, I believe the HTTP Request node supports custom HMAC signing in the Enterprise version?
[00:13:48] **Olivia**: Yes, it’s part of the Advanced Logic pack. You can actually write a small JavaScript snippet directly in the node to calculate the signature before the request fires. 
[00:14:02] **Sam V**: That’s better than Tray. Tray made us use a separate lambda for that.
[00:14:10] **Tom Becker**: We hear that a lot. Since you're looking at 500 seats, you also get the dedicated sandbox environment. You can test those HMAC scripts without affecting your production telemetry flows.
[00:14:25] **Sam V**: And the price is locked? I don't want to see a 20% jump in 2027.
[00:14:32] **Tom Becker**: We can do a 3-year lock if you’re willing to commit upfront. Usually, we do a 5% annual escalator, but for a 500-seat partner, I can talk to Rachel (our CFO) about waiving it. 

---

## Data Validation Log: `arr_snapshot` vs Manual Calc
**Date**: 2026-05-01
**User**: lina.cho

**Note**: Ran a check on why the `arr_snapshot` table is showing $39.2M but the `dim_customers.current_mrr_usd * 12` is showing $40.1M. 
**Discovery**: `dim_customers` has a few records for "Tamarind Group" (`cust_000706`) as 'active' but their subscription in `fact_subscriptions` is marked as `is_current = false` because they paused in January. `arr_snapshot` correctly excludes them. **REMINDER**: Always use `arr_snapshot` for board reporting. The `dim_customers` table has intraday drift from the CRM sync that doesn't always reflect the billing truth in `fact_subscriptions`.

**Query used**:
```sql
-- Correct way to get current ARR per Signal [arr]
SELECT 
  SUM(mrr_usd) * 12 as total_arr 
FROM `nexus-analyst-demo.acme.fact_subscriptions` 
WHERE is_current IS TRUE 
AND plan_tier != 'Free';
-- Result: 39,120,440 (Matches snapshot)
```

---

## CS Sync Notes: Marigold Health (NA-East / Healthtech)
**Date**: 2026-04-20
**CSM**: Olivia Tran
**Account**: `cust_000701` (Enterprise, 300 seats, $15,000 MRR)

- **Health Check**: Stable. Utilization is NULL (Enterprise), but `is_engaged` is TRUE. 45 users active in last 28 days.
- **Issues**: Marigold is asking about HIPAA BAA. I confirmed we have one on file since their signup through the partner channel last year.
- **Expansion**: They are eyeing the `Onyx Robotics` model of 500 seats for their upcoming merger with a smaller clinic group. Sarah Chen to follow up on the add-on order form.
- **Support**: 0 open tickets. CSAT average 4.8.
- **Action**: Check if they need the `AUTH_FAILED` monitoring dashboard. Their "Patient-Portal-Sync" workflow had 12 failures yesterday due to an expired OAuth token on their side.

---

## Slack Thread: #data-requests
**Date**: 2026-05-03

**jasmine.park**: @rajiv.menon can we get a list of all Business tier customers in APAC who came in via the 'event' channel? I need it for the Tokyo workshop invite list.
**rajiv.menon**: Sure thing Jasmine. One sec.
**rajiv.menon**: 
```sql
SELECT company_name, current_mrr_usd, seat_count_licensed
FROM `nexus-analyst-demo.acme.dim_customers`
WHERE region = 'APAC' 
AND current_plan_tier = 'Business'
AND acquisition_channel = 'event'
AND status = 'active';
```
**rajiv.menon**: That gives us two: 
1. Yarrow Logistics (`cust_000703`) - 120 seats
2. Harbor Dynamics (`cust_000713`) - 150 seats
**jasmine.park**: Perfect. I thought there were more?
**rajiv.menon**: A few are on the Pro plan (like Willow Works, though they're LATAM anyway), and Verdant Cloud is Enterprise, not Business. 
**jasmine.park**: Oh right, Verdant upgraded. Thanks!

---

## Gong Call Transcript: Sable Analytics - Business Tier Discovery
**Date**: 2026-05-04
**Participants**: Sarah Chen (Acme AE), David Lo (Sable Analytics - VP of Engineering)
**Recording ID**: `gong_rec_9921_sable`

**Sarah Chen**: (00:05) ...can everyone see my screen okay? I think my Zoom is lagging a bit. David, are you still there?
**David Lo**: (00:12) Yeah, I can see it. It’s just the slide with the pricing tiers. Hey, before we dive into the demo, I had a quick question about the Business tier. We’re currently on Pro with about 15 users, mostly just our DevOps team poking around. We’re looking to roll this out to the wider data team, probably about 35-40 people. Your site says the Business tier starts at 50 seats?
**Sarah Chen**: (00:45) That’s correct. The Business tier has a 50-seat minimum. It unlocks the SSO integration—I know you mentioned Okta is big for you guys—and the audit logs. Plus, you get 100,000 workflow runs a month instead of the 10k on Pro.
**David Lo**: (01:03) Right, but we only have 40 people right now. If I buy the Business tier, am I basically paying for 10 ghost seats? That’s like... what, $149 a seat? 
**Sarah Chen**: (01:15) Yeah, $149 per seat per month. Most customers in your position find that the SSO and the increased run quota actually pay for themselves. If you stay on Pro, you’d be capped at 10,000 runs. Looking at your current usage, you guys hit 8,500 runs last month just with 15 users. Once you add the data team, you'll blow past that in the first week.
**David Lo**: (01:40) (Sighs) We looked at Make.com and Tray, and their seat models are a bit different. Tray's pricing is more on the connector side. Why the hard 50-seat floor?
**Sarah Chen**: (01:55) It’s really about the support model. Business tier gets priority support and a dedicated Slack channel with our engineering team. We can't really sustain that for smaller teams. However, if you're looking at 40 seats now, you're only 10 away from the floor. Maybe we can look at a growth ramp where we credit some of those seats for the first 90 days?
**David Lo**: (02:18) Send me a proposal on that. But honestly, if we’re going to pay for 50, I might just push for Enterprise. What’s the jump from Business to Enterprise? 
**Sarah Chen**: (02:30) Enterprise is custom, but it usually starts around $50k ACV. That gets you unlimited runs and SOC2 compliance docs, which your legal team asked about last time.
**David Lo**: (02:45) Let's stick to Business for now. 50 seats. Send me the PDF.

---

## Internal Memo: Workflow Quota Overages (Cobalt Systems)
**Date**: 2026-05-05
**From**: Olivia Tran (CSM)
**To**: Sales-Ops-Distro; Marcus Thorne

**Subject**: Urgent: Cobalt Systems (`cust_000720`) hitting Business Tier caps

We need to move Cobalt Systems to Enterprise ASAP. 
- **Current Plan**: Business (120 seats @ $149/mo)
- **Problem**: They have a "Lead-Gen-Scraper" workflow that is firing every 30 seconds. 
- **Stats**: They hit 98,400 runs as of 10:00 AM today. Their monthly reset isn't for another 12 days.
- **Impact**: System will start throttling their runs once they hit 100k. Last time this happened with Harbor Dynamics, their Salesforce sync broke and it was a whole thing with their VP.

**Rajiv's Query Check**:
```sql
-- Checking Cobalt's run velocity for May
SELECT 
  customer_id,
  COUNT(run_id) as total_runs_mtd,
  COUNT(CASE WHEN status = 'failed' THEN 1 END) as failure_count
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE customer_id = 'cust_000720'
AND triggered_at >= '2026-05-01'
GROUP BY 1;
-- Result: 98,412 runs. Failure rate 0.2%.
```

I’ve reached out to Elena Vance at Cobalt. She's annoyed about the "arbitrary limits" (her words). Marcus, can you jump on a call tomorrow to pitch the Enterprise "Unlimited" tier? We can probably land them at $200k ACV if we bundle in the premium connectors for ServiceNow they keep asking about.

---

## Gong Call Transcript: Harbor Dynamics - Post-Onboarding Q&A
**Date**: 2026-05-06
**Participants**: Rajiv Menon (Acme Data/Support), Kenji Sato (Harbor Dynamics - Lead Dev)

**Kenji Sato**: (05:12) ...so the main issue is the `duration_ms` we're seeing on the BigQuery export. Some of these are taking 5 seconds, some are taking 45 seconds. It’s making our internal dashboard look really laggy.
**Rajiv Menon**: (05:30) Right, I see that. Are you guys running those on a schedule or is it a webhook trigger coming from your ERP?
**Kenji Sato**: (05:40) It's a webhook from the ERP. But we're also using the Zapier integration as a fallback. Does the Acme-Zapier bridge add latency?
**Rajiv Menon**: (05:55) A little bit, yeah. You're hopping through two different clouds there. If you move those workflows natively into Acme—since you’re on the Business tier and have the seat capacity—you’d likely see that drop under 2 seconds.
**Kenji Sato**: (06:15) We thought about that. But Zapier has that one specific connector for our legacy warehouse in Tokyo. Do you guys have a custom SDK for that?
**Rajiv Menon**: (06:28) We do. It’s part of the Enterprise dev-kit, actually. I know you guys are on Business right now with 150 seats... if you ever decide to bridge that gap to Enterprise, you get the SDK and can build your own private connectors. 
**Kenji Sato**: (06:45) (Laughs) I’ll tell my boss. He’s already complaining about the $22k we’re paying you every month. 
**Rajiv Menon**: (07:00) Hey, just think of it as "efficiency tax." By the way, I saw some `AUTH_FAILED` errors on your "Inventory-Sync" workflow last night. Did you guys rotate your API keys?
**Kenji Sato**: (07:15) Oh, man. Yeah, the security team did a sweep. I forgot to update the Acme secret manager. Let me do that now.

---

## Slack Thread: #sales-chatter
**Date**: 2026-05-07

**marcus.thorne**: Huge win! Verdant Cloud just signed the Enterprise expansion. 
**sarah.chen**: NICE. What’s the final seat count?
**marcus.thorne**: We landed at 400 seats. They needed the custom SLA for their uptime guarantees to their own customers. Total ACV is $320k.
**rajiv.menon**: I'll update the `dim_customers` table. Just so I'm clear, are they moving off the standard Business support Slack channel to a dedicated one?
**marcus.thorne**: Yeah, Olivia is setting up #acme-verdant-enterprise now. 
**jasmine.park**: @marcus.thorne was the acquisition channel really 'organic' for them? I'm seeing 'referral' in the old notes from 2024.
**marcus.thorne**: The original lead was a referral from Yarrow Logistics back when they were both seed-stage, but the actual Enterprise upgrade came through the SEO campaign we ran on "SOC2 workflow automation." So... credit is messy.
**rajiv.menon**: I'll keep it as 'referral' in the master record to preserve the lineage. 

```sql
UPDATE `nexus-analyst-demo.acme.dim_customers`
SET current_plan_tier = 'Enterprise',
    account_tier = 'Ent',
    seat_count_licensed = 400
WHERE company_name = 'Verdant Cloud';
```
**rajiv.menon**: Actually, wait, I shouldn't manual update. I'll wait for the Fivetran sync from Salesforce to hit the warehouse tonight. 
**sarah.chen**: Good call. Don't break the provenance. 

---

## Support Ticket: #8821 - Billing Discrepancy
**Status**: Closed
**Customer**: Yarrow Logistics (`cust_000703`)
**Assigned**: Support-Bot / Olivia Tran

**User (j.vance@yarrow.logistics)**: "Hi, we just got our invoice for April. It shows 125 seats, but we only have 120 people in the dashboard. Why are we being charged for the extra 5? We're on the Business tier."

**Olivia Tran**: "Hi Jay, I checked your account. It looks like 5 invited users haven't accepted their invites yet, but per our terms for the Business tier, seats are billed upon being 'provisioned' (invite sent), not just 'active'. You can see the pending invites in your Settings > Team tab. If you cancel the invites, the seats will be credited to your next billing cycle."

**User (j.vance@yarrow.logistics)**: "That seems aggressive. We're already paying $149 a seat. Can you just waive it?"

**Olivia Tran**: "I can offer a one-time credit for those 5 seats this month as a gesture of goodwill, but going forward, the system automates this based on the licensed count. I've applied the $745 credit to your account."

---

## Gong Transcript: Harbor Dynamics - Growth Discovery
**Date**: April 12, 2026
**Participants**: Jasmine Park (Acme), Rick V. (Harbor Dynamics), Sarah G. (Harbor Dynamics)
**Recording Length**: 44:12

[00:00:15] **Jasmine Park**: ...glad we could finally connect. I saw your team’s usage spiked over the weekend. You guys hit about 9,500 runs on Sunday alone. 

[00:00:28] **Rick V.**: Yeah, sorry about that. We had a bit of a loop in one of the dbt-cloud-to-Slack triggers. Our dev environment was basically screaming at us for four hours.

[00:00:39] **Jasmine Park**: (Laughs) No worries, the Pro plan is pretty resilient, but you are right on the edge of that 10k monthly quota. We’re only halfway through April. 

[00:00:51] **Rick V.**: That’s actually why Sarah joined. We’re evaluating if we should just bump to Business now or wait until the new fiscal year in July. We're currently paying for 42 seats on the Pro tier, right?

[00:01:05] **Jasmine Park**: Exactly. 42 seats at $49 each. If you move to Business, the price jumps to $149 per seat, but the minimum is 50. So even if you stay at 42 users, you’d be billed for 50. But you get 100k runs a month, SSO, and the audit logs which I think your security team was asking about?

[00:01:28] **Sarah G.**: Yeah, the audit log is the big one. We’re starting to build out more financial workflows—moving data between Stripe and our internal warehouse—and my boss is getting nervous about who has 'write' access to those production workflows. Does Business give us granular RBAC or is that just Enterprise?

[00:01:47] **Jasmine Park**: Business gives you 'Admin', 'Editor', and 'Viewer' roles at the folder level. For truly custom roles or attribute-based access control, that’s usually where we see folks look at Enterprise. But for what you’re doing with Stripe, Business is usually the sweet spot.

[00:02:05] **Rick V.**: And what about the Zapier integration? We have a lot of legacy stuff in Zapier. Can Acme just... ingest those?

[00:02:14] **Jasmine Park**: We don't have a 1-to-1 "import" button—I wish we did—but we have a migration utility for the JSON structures. Most people find that once they see the logic in our canvas, it's easier to just rebuild and optimize. Plus, our throughput is way higher. You won't get those "rate limit exceeded" errors you see on the Zapier Starter plans.

---

## Slack: #sales-ops-internal
**marcus.thorne**: @rajiv.menon can you check the `fact_workflow_runs` for Sable Analytics (`cust_000422`)? They’re complaining that their "usage dashboard" in-app doesn't match their invoice. 
**rajiv.menon**: Checking. 
**rajiv.menon**: Okay, I see the issue. They had a bunch of 'test' runs in the sandbox environment that weren't being filtered out of the billing aggregate in the legacy UI, but the warehouse is correctly excluding them. 
**rajiv.menon**: Run this to see the breakdown:
```sql
SELECT 
  status,
  count(*) as run_count,
  sum(step_count) as total_steps
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE customer_id = 'cust_000422'
  AND triggered_at BETWEEN '2026-04-01' AND '2026-04-30'
GROUP BY 1;
```
**marcus.thorne**: They have 12,000 "Failed" runs? 
**rajiv.menon**: Yeah, looks like a bad API key for their Jira integration. We don't charge for runs that fail in the first 2 seconds due to auth errors, but if it fails at step 10, it still counts against the quota. 
**marcus.thorne**: Ugh, I have a renewal call with them tomorrow. They're going to try to use this to negotiate the 50-seat minimum on the Business tier. They only have 38 people. 

---

## Gong Transcript: Cobalt Systems - Enterprise QBR
**Date**: May 02, 2026
**Participants**: Marcus Thorne (Acme), Olivia Tran (Acme), Elena D. (CTO, Cobalt Systems)

[00:15:22] **Elena D.**: ...honestly, the uptime has been great. No complaints there. But we're looking at the roadmap for the ServiceNow integration. We're moving our entire ITOM suite over there by Q4. 

[00:15:35] **Olivia Tran**: That's perfect timing. We actually just moved the ServiceNow 'Deep Link' connector into beta for our Enterprise customers. Since you guys are on the custom Ent plan, I can get you early access to that by Monday. 

[00:15:52] **Elena D.**: That would be helpful. Now, Marcus, let's talk about the seat count. We're at 285 seats right now. Our hiring has slowed down a bit. We're probably not going to hit that 400-seat projection we talked about in January. Can we true-down at the next renewal?

[00:16:11] **Marcus Thorne**: So, with the Enterprise agreement we signed, the 250-seat floor is what locks in that preferred pricing and the dedicated CSM—which is Olivia here. If we go below 250, the per-seat price would actually revert to the standard Business rate, which might end up costing you more in the long run even with fewer seats. 

[00:16:34] **Elena D.**: (Sighs) The "SaaS Trap," right? 

[00:16:38] **Marcus Thorne**: I wouldn't call it a trap! Think of it as a volume discount. But look, if you’re worried about underutilization, Olivia can show you the "User Adoption" report. You have about 40 seats that haven't logged in for 30 days. We could reassign those to the Marketing Ops team? They’ve been asking for access.

[00:17:01] **Elena D.**: Marketing Ops? If they touch the workflows, they'll break the BigQuery sync. 

[00:17:07] **Olivia Tran**: Not if we use the RBAC features we set up last month. We can put them in a "Read-Only" or "Creator-Lite" sandbox. They can build their own triggers without touching your core data pipelines.

---

## Support Ticket: #9012 - SSO Lockout
**Status**: Resolved
**Customer**: Verdant Cloud (`cust_000511`)
**Assigned**: Support-Bot / Rajiv Menon

**User (admin@verdant.cloud)**: "URGENT: We just enabled Okta SSO and now none of our admins can log in. We're getting a 'SAML_004' error. Please help, we have a production deployment scheduled for 2 PM."

**Olivia Tran**: "Hi there, I've looped in our engineering team. It looks like the 'Audience URI' in your Okta config is pointing to our staging environment instead of production. I've temporarily disabled the SSO requirement for your two primary admins so you can get back in and fix the configuration."

**Rajiv Menon**: (Internal Note) Checked the logs. They tried to manually update the `dim_customers.account_tier` via the API before the SSO was fully validated. I'm seeing a lot of 403s in the log. I'll manually reset their `auth_method` flag in the DB for now.

```sql
UPDATE `nexus-analyst-demo.acme.dim_customers`
SET status = 'Active'
WHERE customer_id = 'cust_000511';
```

**Olivia Tran**: "You should be able to log in with your original email/password now. Once you update the Okta metadata, let me know and we can re-enable the enforcement."

---

## Gong Transcript: Harbor Dynamics Q2 Strategy Sync
**Date**: March 12, 2026
**Participants**: Marcus Thorne (Acme AE), Sarah Jenkins (Harbor Dynamics - VP Ops), Tom "TJ" Jefferson (Harbor Dynamics - IT)
**Customer ID**: `cust_000722`

[00:02:15] **Marcus Thorne**: ...and that’s why we’re seeing that 15% spike in successful runs. It looks like the warehouse-to-CRM sync you guys built in January is really humming.

[00:02:28] **Sarah Jenkins**: It’s humming, Marcus, but it’s also costing us a fortune in compute on the Snowflake side because of how often the webhooks are firing. We’re doing about 400,000 runs a month now?

[00:02:41] **Marcus Thorne**: Actually, let me pull up the dashboard. You’re at 442,102 for February. Since you’re on the Enterprise tier, the "Unlimited Runs" clause covers you, so you aren't seeing an Acme overage, but I hear you on the Snowflake egress costs. 

[00:02:58] **TJ**: Hey Marcus, quick technical one. We’re looking at the Sable Analytics integration. They have a different rate limit than what your docs say. If we move the Sable workflows from our "Pro" sandbox into the main Enterprise workspace, do we get the dedicated IP?

[00:03:15] **Marcus Thorne**: Yes, Enterprise accounts get the static egress IP. It’s a $500/mo add-on normally but we bundled it for Harbor last year. Sarah, speaking of the Enterprise tier, your renewal is coming up in June. You’re currently licensed for 300 seats. 

[00:03:32] **Sarah Jenkins**: That’s what I wanted to talk about. We’ve had some... let's call it "headcount rationalization." We’re down to 265 active users on Acme. When we renew, can we drop the seat count to 250?

[00:03:47] **Marcus Thorne**: (Pauses) So, the Enterprise floor is technically 250. If you drop to 250, you keep all the bells and whistles—SOC2, the 99.99% SLA, and Olivia as your dedicated CSM. But the per-seat price usually shifts if the volume drops that much. Let me run the numbers with Finance. If we stay at 300, I can probably hold the 2025 unit price. 

[00:04:15] **Sarah Jenkins**: Just send me the PDF. If the delta is less than 5k, I won't fight you, but my CFO is breathing down my neck about "unused SaaS waste." 

---

## Slack / Internal - #account-ops-alerts
**From**: Rajiv Menon
**To**: @olivia-tran @marcus-thorne
**Date**: April 02, 2026

**Rajiv**: Hey guys, just a heads up on **Cobalt Systems** (`cust_000344`). They just hit 98,000 workflow runs for the month and it's only the 15th. They are on the Business tier (100k cap).

**Olivia Tran**: Thanks Rajiv. They just added that new "Auto-Responder" logic for their support tickets. It’s looping. I’ll reach out to their admin.

**Marcus Thorne**: Wait, if they’re hitting the cap every month, this is a perfect play for the Enterprise upgrade. They’ve been asking about the Audit Log API anyway, which is an Ent-only feature. Olivia, can you check their actual seat utilization? Last I checked they had 52 seats filled but paid for 50.

**Olivia Tran**: Running the query now.

```sql
SELECT 
    c.company_name,
    c.seat_count_licensed,
    COUNT(u.user_id) as active_user_count,
    c.current_plan_tier
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_users` u ON c.customer_id = u.customer_id
WHERE c.customer_id = 'cust_000344'
AND u.is_active = TRUE
GROUP BY 1, 2, 4;
```

**Olivia Tran**: Yeah, they have 58 active users on a 50-seat Business contract. They’re $1,192 in the hole on true-ups for this quarter alone. I'll book a "Capacity Planning" call with David Wu for Thursday.

---

## Gong Transcript: Discovery Call - Sable Analytics
**Date**: April 10, 2026
**Participants**: Jordan Lee (Acme Product/Sales Eng), Karen Miller (Sable Analytics - Dir. Engineering)
**Customer ID**: `cust_000819`

[00:05:40] **Karen Miller**: ...so right now we’re using a mix of Zapier for the marketing stuff and some custom Python scripts on Lambda for the heavy data lifting. It’s a mess to maintain. We want to centralize.

[00:05:55] **Jordan Lee**: Makes sense. And how many people would actually be building the workflows?

[00:06:01] **Karen Miller**: Probably 10-12 in Eng, but we want the "Creators" to be in Product Ops too. Maybe 40 people total? We saw the Pro plan is $49 a seat, which fits the budget. 

[00:06:15] **Jordan Lee**: Pro is great for getting started, but you mentioned you need the Okta integration and the ability to see who changed a workflow version?

[00:06:25] **Karen Miller**: Yeah, we’re going through a security audit in July. SSO is a hard requirement. 

[00:06:31] **Jordan Lee**: Okay, so for SSO and Audit Logs, you’d need the **Business tier**. Just so you’re aware, the Business tier has a 50-seat minimum. Even if you only have 40 people using it day one, we’d bill for 50.

[00:06:48] **Karen Miller**: (Sighs) We get this with every B2B tool. Why the jump? $49 to $149 is a massive leap just for a login button. 

[00:06:58] **Jordan Lee**: I hear you. It’s more than the button, though. You get the 100k run quota—which, based on your Lambda volume, you’ll burn through in the first week on the Pro plan anyway—plus the priority support queue. If a production workflow breaks on Pro, it’s a 24-hour SLA. On Business, we’re looking at you within 2 hours.

[00:07:22] **Karen Miller**: (Pauses) 2 hours is better. Let me talk to our Procurement lead. Do you have a trial for the Business features? I don't want to commit to 50 seats if the "Universal Connector" can't handle our legacy Postgres setup. 

[00:07:40] **Jordan Lee**: I can spin up a 14-day "Business Trial" for you. I'll just need you to whitelist our IP range first. 

---

## Internal Memo: Pricing Review Committee (Draft)
**From**: Finance Ops
**Date**: April 25, 2026
**Subject**: Potential Adjustments to SMB Account Tiering

We are seeing a trend where customers in the `account_tier = 'SMB'` are staying on the "Free" plan longer than expected. Analysis of `fact_workflow_runs` shows that many are hovering around 95 runs/month to avoid the 100-run "Pro" trigger.

**Proposed Change**: Lower the Free tier quota to 50 runs/month but include a one-time "Burst Credit" of 500 runs to encourage testing. 

**Impact Analysis (BigQuery)**:
```sql
SELECT 
    region,
    COUNT(customer_id) as customer_count,
    AVG(current_mrr_usd) as avg_mrr
FROM `nexus-analyst-demo.acme.dim_customers`
WHERE current_plan_tier = 'Free'
AND status = 'Active'
GROUP BY region;
```
*Current Free User Distribution:* 
- North America: 142
- EMEA: 88
- APAC: 30

The churn risk for APAC is high if we tighten the limits, as acquisition there is primarily through the "Community Builders" program. Recommend keeping APAC on the current 100-run limit for another two quarters.

---

**Gong Call Transcript: Cobalt Systems - Business Tier Expansion Discovery**
**Date**: January 14, 2026
**Participants**: 
- Jordan Lee (Senior AE, Acme)
- Marcus Thorne (VP Operations, Cobalt Systems)
- Sarah Jenkins (CSM, Acme)

[00:00:12] **Jordan Lee**: ...yeah, the rain in Seattle is just—it's relentless this week. I think I’ve forgotten what the sun looks like. Anyway, Marcus, thanks for hopping on. I saw the note from Sarah that you guys are pushing the limits of the Pro plan.

[00:00:28] **Marcus Thorne**: (Laughs) Relentless is one way to put it. Yeah, look, we’ve got about 14 departments now using Acme for their internal ticket routing. I think we’re at 42 seats on the Pro plan? But the issue isn't the seats, it’s the audit logs. Our Compliance team is breathing down my neck because they can't see who modified the Salesforce-to-NetSuite mapping last Tuesday when everything doubled-entered.

[00:00:54] **Jordan Lee**: Right, the "who-dunit" problem. Yeah, that’s exactly why the Business tier exists. Pro gives you the execution, but Business gives you the governance. Audit logs, SAML SSO—I assume you guys are using Okta?

[00:01:08] **Marcus Thorne**: We are. Setting up individual logins for 40+ people is a nightmare for onboarding. I want them on SSO yesterday. But I looked at the pricing page... Jordan, $149 a seat is a massive jump from $49. And you have a 50-seat minimum? We’re only at 42. You're asking me to pay for 8 ghosts just to get a log file.

[00:01:32] **Jordan Lee**: I totally get how that looks on paper. But think about the `workflow_run_quota`. You guys are currently paying overages on the Pro plan almost every month, right? Sarah, do you have those numbers?

[00:01:45] **Sarah Jenkins**: Yeah, I pulled the report from the warehouse this morning. Cobalt is averaging 115k runs per month. On Pro, you're capped at 10k, and those overage blocks of 5k runs are adding up. Last month, your bill actually hit $8,200 anyway because of the volume. 

[00:02:02] **Marcus Thorne**: (Pauses) Wait, $8k? I thought we were on a flat fee. 

[00:02:06] **Sarah Jenkins**: No, the Pro plan has a hard cap. If you look at `nexus-analyst-demo.acme.fact_workflow_runs`, your `customer_id` is 'CUST-9921'. You had a massive spike on the 12th—looks like a loop error in a "Lead Scraper" workflow. You burned 30k runs in two hours.

[00:02:24] **Marcus Thorne**: (Sighs) Okay, that explains the Slack alerts I ignored. So Business gives us 100k runs base?

[00:02:32] **Jordan Lee**: Exactly. And no more overage "gotchas" for the first 100k. Plus, we give you a dedicated sandbox environment so that "Lead Scraper" loop happens in staging, not production. It protects your quota. 

[00:02:46] **Marcus Thorne**: Can we waive the 50-seat minimum? If I can get this to $120 a seat or keep the 42-seat count, I can probably get it past our CFO. He’s still annoyed we moved off Zapier. 

[00:02:58] **Jordan Lee**: Zapier is great for "if this, then that," but they don't handle the conditional logic trees you guys are building. As for the seats... I can't move the minimum—it's hardcoded in the billing engine—but I can talk to my VP about a "Year 1 Deployment Credit" to offset the cost of those 8 seats. Let me see what I can do.

---

## Internal Slack Thread: #eng-universal-connector
**March 12, 2026**

**tchen [10:14 AM]**: Heads up, we’re seeing a lot of 504 errors on the legacy Postgres connector for customers on the Business trial. Specifically `Verdant Cloud`. They’re trying to sync 1M+ rows in a single batch.

**j-doe [10:16 AM]**: Verdant again? I told the AE (Jordan) that the Universal Connector isn't a replacement for a full ETL tool like Fivetran. It’s meant for transactional triggers, not bulk migrations. 

**tchen [10:18 AM]**: They don't care. They saw the "Universal" name and assumed it meant "Infinite." Can we throttle them? 

**j-doe [10:20 AM]**: If we throttle a Business Trial user during their POC, Sales will lose their minds. Let's look at the logs. 
```sql
SELECT 
    error_code, 
    COUNT(*) as failure_count
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE customer_id = 'CUST-4402' -- Verdant Cloud
AND triggered_at >= '2026-03-10'
GROUP BY 1;
```
**tchen [10:25 AM]**: 400+ `ERR_CONN_TIMEOUT`. Yeah, their DB is blocking our IP range or just timing out on the handshake. I'll reach out to their ops person, but Jordan needs to manage expectations on the "Universal" marketing.

---

**Gong Call Transcript: Harbor Dynamics - Enterprise QBR**
**Date**: April 03, 2026
**Participants**:
- Sarah Jenkins (CSM, Acme)
- Elena Rossi (IT Director, Harbor Dynamics)
- David "Dax" Baxter (Lead Engineer, Harbor Dynamics)

[00:15:22] **Sarah Jenkins**: ...and looking at the adoption curves, your team has added 120 new workflows just this quarter. That’s incredible growth. How is the "Enterprise Dedicated CSM" experience working out for you so far?

[00:15:35] **Elena Rossi**: It’s been good, Sarah. Having you on the quarterly calls helps. But Dax has some concerns about the custom SLA. We had a 15-minute outage on the webhook listener last Tuesday and it didn't show up on your status page.

[00:15:52] **Dax**: Yeah, it was weird. Our internal monitoring caught it—all our Shopify webhooks were 404ing. We’re on the Enterprise plan specifically for the 99.99% uptime guarantee. If we can't trust the webhook listener, we have to move that logic back to our own AWS Lambda functions, which defeats the purpose of Acme.

[00:16:14] **Sarah Jenkins**: I checked with Engineering on that. It was a regional DNS flutter in EMEA. Since you guys are routed through our Frankfurt cluster, you were affected, but the global status page stayed green because US-East was fine. I'm working with the Product team to get regional status dashboards into the Enterprise portal.

[00:16:34] **Elena Rossi**: That would be a huge help. Also, we’re getting ready for our SOC2 Type II audit in June. I need the signed BAA and the last three months of access logs for anyone on your side who touched our account.

[00:16:48] **Sarah Jenkins**: No problem at all. I’ll pull the internal access logs from `nexus-analyst-demo.acme.dim_employees` (cross-referenced with our internal support ticketing system) and get those to you by Friday. 

[00:17:02] **Dax**: One more thing—we're looking at the "Sable Analytics" acquisition. They use Make.com. How hard is it to migrate their 200+ scenarios into Acme? Does the migration tool support the Make JSON format yet?

[00:17:18] **Sarah Jenkins**: It’s in beta. I can get you early access to the "Scenario Importer." It’s not 100%—you’ll still have to re-map the authentication tokens—but it handles about 80% of the logic translation. Since you're on Enterprise, we can actually have one of our Solutions Architects join a call with the Sable team to map it out.

[00:17:39] **Elena Rossi**: That’s the kind of value we need. Let’s schedule that for the week of the 15th. 

---

**Internal Memo: Competitive Intelligence - Sable Analytics Pressure**
**To**: Sales Leadership
**From**: Jordan Lee
**Date**: April 28, 2026

I just got off a call with the Sable Analytics team (pre-acquisition talk). They are being very aggressive about pricing. Apparently, a rep from **Tray.io** told them they could do a "unlimited seat" model for $40k flat. 

Sable is currently a "Pro" customer of ours, but they are growing fast. If we try to push them to the Business tier ($149/seat), we are going to lose them. Their current MRR is only $1,400. To get to the Business minimum (50 seats), they'd jump to $7,450/mo. That’s a 5x increase. 

**Recommendation**: We need a "Bridge Tier" or a way to waive seat minimums for high-growth SMBs in the `acquisition_channel = 'Referral'` category. If we don't, we're just a feeder for our competitors once our customers hit the 20-user mark. 

Data point from BigQuery:
```sql
SELECT 
    c.company_name, 
    c.current_mrr_usd, 
    COUNT(u.user_id) as active_users
FROM `nexus-analyst-demo.acme.dim_customers` c
JOIN `nexus-analyst-demo.acme.dim_users` u ON c.customer_id = u.customer_id
WHERE c.current_plan_tier = 'Pro'
AND u.is_active = true
GROUP BY 1, 2
HAVING active_users > 30;
```
There are 12 other customers in this "Pro Trap" where they have 30+ users but haven't upgraded to Business because of the seat minimum. That’s ~$70k in potential ARR expansion we're leaving on the table because the price jump is too steep.

---

**Gong Call Transcript: Cobalt Systems - Q2 Business Review**
**Date**: May 1, 2026
**Participants**: Sarah Jenkins (Acme CSM), Marcus Thorne (Acme AE), Kevin Zheng (CTO, Cobalt Systems), Priya Varma (Ops Lead, Cobalt Systems)

[00:00:12] **Sarah Jenkins**: ...and before we dive into the usage metrics, Kevin, how’s the new puppy? I saw the LinkedIn post. Golden Retriever, right?

[00:00:24] **Kevin Zheng**: Oh, he’s a menace. Destroyed a pair of Bose headphones yesterday. But yeah, he’s cute. Sorry I’m a few minutes late, the Zoom update decided to trigger right at the top of the hour.

[00:00:40] **Sarah Jenkins**: No worries at all. Typical Monday stuff. So, looking at the dashboard for Cobalt, you guys have had a massive spike in workflow runs over the last 30 days. You hit 92,000 runs last month. 

[00:00:55] **Priya Varma**: That’s mostly the new Shopify-to-NetSuite sync I built. We’re pushing a lot more SKU data now that we’ve launched the spring line. 

[00:01:05] **Marcus Thorne**: I saw that. You guys are flirting with that 100k cap on the Business tier. If we go over, the overage charges on the old contract are... well, they aren't great. Kevin, have you guys given any more thought to moving to Enterprise?

[00:01:21] **Kevin Zheng**: We’ve talked about it. But the jump from where we are now—what, $149 a seat?—to a $60k floor for Enterprise is a big pill to swallow just for a higher run quota and SOC2 reports. We only have 42 users. You’re already making us pay for 50 seats because of the Business tier minimum. 

[00:01:45] **Marcus Thorne**: I hear you. But Enterprise gets you the dedicated CSM time with Sarah—which you already have as a courtesy, but it becomes official—and more importantly, the audit logs. I know your security team was asking about those last month.

[00:01:59] **Priya Varma**: The audit logs would be nice. We had an incident where someone accidentally deleted the "Order Routing" workflow and we couldn't see who did it. Took us three hours to restore from a local JSON backup.

[00:02:14] **Kevin Zheng**: Still. If we stay on Business, can we just buy a "Run Pack"? I don't want to pay for 250 seats when we don't even have 50 employees in the whole company yet. 

[00:02:26] **Marcus Thorne**: We don't really do "Run Packs" anymore. Product is moving away from that to prevent the "Success Tax" feeling. Let me talk to Finance. We might be able to do a custom Enterprise mid-market deal, maybe at a 100-seat floor instead of 250.

---

**Internal Slack Thread: #sales-ops-and-billing**
**Date**: May 2, 2026

**Jordan Lee**: Hey team, checking the data on Harbor Dynamics. They’ve been on Pro for 18 months. Their seat count just hit 38. According to the `nexus-analyst-demo.acme.dim_customers` table, they’ve never had a churn flag, but their `last_login_date` in `dim_users` for the Admin is over 14 days ago. 

**Sarah Jenkins**: I’ll ping them. I suspect they’re hitting the workflow limit or they're frustrated with the lack of SSO. Harbor is a prime candidate for the Business tier, but they're sensitive about the 50-seat minimum.

**Jordan Lee**: Check this query I ran this morning:
```sql
SELECT 
    f.customer_id,
    c.company_name,
    COUNT(f.run_id) as total_runs_april,
    COUNT(CASE WHEN f.status = 'failed' THEN 1 END) as error_count
FROM `nexus-analyst-demo.acme.fact_workflow_runs` f
JOIN `nexus-analyst-demo.acme.dim_customers` c ON f.customer_id = c.customer_id
WHERE f.triggered_at BETWEEN '2026-04-01' AND '2026-04-30'
AND c.company_name = 'Harbor Dynamics'
GROUP BY 1, 2;
```
They had 4,200 errors last month. Most of them are `error_code = 'RATE_LIMIT_EXCEEDED'` on the Zapier-bridge integration. If they move to our native Shopify connector (Business tier), those errors disappear. 

**Sarah Jenkins**: @MarcusThorne can you reach out to their Ops lead? Use the "Reliability" angle. They’re losing money on failed syncs. 

---

**Gong Call Transcript: Verdant Cloud - Discovery / Demo**
**Date**: May 3, 2026
**Participants**: Marcus Thorne (Acme AE), David Cho (Verdant Cloud, Director of IT)

[00:05:12] **David Cho**: ...Yeah, we’re currently using a mix of Make and some internal Python scripts running on AWS Lambda. It’s a mess to maintain. We need one place where the Marketing team can build their own stuff without bugging my engineers.

[00:05:30] **Marcus Thorne**: That’s the dream. We call it "Democratized Automation." How many people in Marketing would be building?

[00:05:39] **David Cho**: Probably 10-15. But I want SSO. If I don't have Okta integration, my security team will kill the project before it starts.

[00:05:51] **Marcus Thorne**: Totally get it. SSO is part of our Business tier. That starts at 50 seats. 

[00:05:58] **David Cho**: Wait, 50 seats? We only have 15 people who would use this. Why would I pay for 50? 

[00:06:05] **Marcus Thorne**: The Business tier is designed for organizations that need those "Governance" features—SSO, audit logs, and the 100k run quota. It’s a bundled value.

[00:06:18] **David Cho**: (Laughs) It’s a bundled way to get me to pay $7,400 a month for 15 users. That’s like $500 a user. Zapier lets me do SSO on their Team plan for way less than that. 

[00:06:34] **Marcus Thorne**: I understand the price gap. The difference is the reliability. If you look at our `sla_uptime_pct` in the `dim_plans` table—well, I can send you the sheet—we guarantee 99.9% on Business. Zapier doesn't give you a legal SLA until you're much higher up. Plus, our NetSuite integration is bi-directional and real-time. 

[00:06:55] **David Cho**: We don't use NetSuite. We’re on QuickBooks Enterprise. 

[00:07:02] **Marcus Thorne**: Oh. Right. Well, the QuickBooks connector is also a "Premium" connector. Let me see if I can get a waiver on the seat minimum for the first six months while you guys scale up. 

---

**Memo: Monthly Churn Post-Mortem (April 2026)**
**From**: Finance Ops
**To**: Executive Team

We saw a slight uptick in churn among the "Pro" cohort this month. 
- **Total Churn**: $12.4k MRR
- **Primary Reason**: "Pricing/Seat Minimums" (45% of churned revenue)
- **Key Account Lost**: **Sable Analytics** ($1,400 MRR). They moved to a competitor (Tray.io) specifically citing the cost to move to our Business tier.

The data suggests that the "Death Valley" between Pro ($49/seat, no min) and Business ($149/seat, 50 min) is where we are losing our most promising mid-market logos. Customers would rather stay on a buggy "Pro" setup or switch to a competitor than take a 5x price hike.

**SQL Analysis for April Churn (Flat Table):**
```sql
SELECT 
    company_name, 
    current_mrr_usd, 
    seat_count_licensed,
    churn_date
FROM `nexus-analyst-demo.acme.dim_customers`
WHERE status = 'churned'
AND churn_date BETWEEN '2026-04-01' AND '2026-04-30'
ORDER BY current_mrr_usd DESC;
```
We need to finalize the "Bridge Tier" proposal by the end of Q2. If we can capture even 20% of the Pro-to-Business "Trap" accounts, we're looking at an additional $1.2M in ARR expansion by year-end.

**Gong Transcript: Harbor Dynamics Expansion Sync**
**Date**: May 12, 2026
**Participants**: Marcus Thorne (AE, Acme), Arjun Mehta (Director of Ops, Harbor Dynamics)
**Account**: Harbor Dynamics (Pro Tier, 18 seats)

[00:00:15] **Marcus Thorne**: Hey Arjun, good to see you again. How’s the weather out in Chicago? I heard you guys got hit with a bit of a late-season chill.

[00:00:24] **Arjun Mehta**: (Laughs) It’s miserable, Marcus. I think we’ve had two days of sun since April. But anyway, let’s jump in. I saw the automated notification from your system saying we’re at 92% of our workflow run quota for the month? It’s only the 12th. 

[00:00:41] **Marcus Thorne**: Yeah, I pulled the report this morning from `nexus-analyst-demo.acme.fact_workflow_runs`. You guys are hitting it hard. I think the "Shopify-to-ShipStation" sync you built last week is looping a bit more than you expected. You’ve logged nearly 9,200 runs since May 1st.

[00:01:02] **Arjun Mehta**: That’s the problem. We’re on the Pro plan, which I thought was "unlimited workflows." 

[00:01:08] **Marcus Thorne**: It is unlimited *workflows*, but the *runs* are capped at 10,000 per month on Pro. It’s right there in the `dim_plans` table if you ever check the documentation. To get more volume, we really need to talk about moving Harbor Dynamics up to the Business tier.

[00:01:25] **Arjun Mehta**: I looked at the Business tier. Marcus, you’re asking for a 50-seat minimum. I have 18 people in my Ops team. I’m not paying for 32 empty seats just so my Shopify sync doesn't break. That’s—what—$7,450 a month? We’re paying less than a thousand right now.

[00:01:44] **Marcus Thorne**: I hear you. The Business tier isn't just about the runs, though. You get the SAML SSO—which I know your IT guy, Ben, was asking about—and the full audit log. If one of your 18 users accidentally deletes a production workflow, on Pro, we can't tell you who did it. On Business, we have the `fact_user_events` tracked down to the millisecond.

[00:02:10] **Arjun Mehta**: [Sighs] The audit log is nice, but it’s not $6,000-a-month nice. Make.com doesn't charge us a seat minimum for higher throughput. We’re basically looking at a 7x price increase for the same 18 people. Can we just buy "run packs"?

[00:02:28] **Marcus Thorne**: We don't really do run packs on the Pro plan anymore. Finance moved away from that in '24 because it was a nightmare to track in the billing engine. Let me talk to my VP, Jamie. Maybe we can do a "growth ramp" where we start you at 30 seats for the first year, but honestly, with the volume you’re projecting, you’ll hit the 100k Business cap by July anyway.

---

**Internal Slack Message**
**Channel**: #sales-ops-internal
**From**: Marcus Thorne
**Date**: May 12, 2026, 2:45 PM

@sarah_jenkins heads up on Harbor Dynamics. They are blowing through their 10k quota on Pro. Arjun is pushing back hard on the 50-seat min for Business. He mentioned Make.com. I tried the "security/SSO" angle but he’s focused on the sticker shock. If they throttle on the 15th, they’re going to be pissed. Can we check if there’s any flexibility on the `min_seats` in the `dim_plans` for "Strategic SMB" accounts? I don't want another Sable Analytics situation.

---

**Gong Transcript: Cobalt Systems QBR**
**Date**: May 14, 2026
**Participants**: Sarah Jenkins (CSM, Acme), Kevin Vance (VP Eng, Cobalt Systems)
**Account**: Cobalt Systems (Business Tier, 62 seats)

[00:14:22] **Sarah Jenkins**: ...so looking at the health score, your "error rate" on the Salesforce-to-Snowflake connector has spiked. It’s mostly `error_code` 401s, which usually means a token expired. 

[00:14:35] **Kevin Vance**: Yeah, we saw that. My team is a bit frustrated that we’re paying for "Priority Support" on the Business tier, but it still took four hours to get a response on that ticket last Tuesday. When we were on the pilot, we had a Slack channel with your engineers. 

[00:14:55] **Sarah Jenkins**: I totally understand the frustration, Kevin. The Slack channel is actually an Enterprise-only feature now. For Business tier, it's strictly through the portal. I did talk to the support lead, and they’ve been swamped with the v4.2 rollout bugs. 

[00:15:12] **Kevin Vance**: v4.2 was a mess for us, honestly. Half our webhooks from Zendesk started returning 500s. We’re actually evaluating if we should stay on Business or just go "all in" on Enterprise to get that dedicated CSM and the uptime SLA. What’s the jump look like?

[00:15:31] **Sarah Jenkins**: Enterprise usually starts around $50k ACV, but for a team of your size—62 seats—we could probably look at a custom package. The big thing you’d get is the 99.99% SLA. If you check `dim_plans`, Business is only guaranteed at 99.9%. For your scale, that 0.09% difference is about 7 hours of downtime a year. 

[00:15:58] **Kevin Vance**: (Laughs) We already had 7 hours of downtime just last month when the Netherlands region went sideways. Send me the Enterprise deck. But if the price is double what we’re paying now, I’m going to have a hard time selling it to my CFO. We’re already one of your higher-paying MM accounts.

---

**Data Engineering Note (Pinned to #data-warehouse)**
**Subject**: Flat Table Migration for `fact_workflow_runs`

Team, please note that `nexus-analyst-demo.acme.fact_workflow_runs` is now the source of truth for all usage-based billing alerts. We had an issue yesterday where some `triggered_by` values were coming in as NULL for scheduled jobs, which caused the "Pro Quota" alerts to under-count for about 40 customers. 

If you are running audits for Marcus or Sarah, use the following logic to capture "Real Usage":

```sql
-- Use this to identify customers nearing their Pro limits (10k)
-- Note: status 'success' and 'failed' both count towards the quota!
SELECT 
    c.company_name,
    COUNT(r.run_id) as total_runs_mtd,
    p.workflow_run_quota_per_month as quota
FROM `nexus-analyst-demo.acme.fact_workflow_runs` r
JOIN `nexus-analyst-demo.acme.dim_customers` c ON r.customer_id = c.customer_id
JOIN `nexus-analyst-demo.acme.dim_plans` p ON c.current_plan_tier = p.plan_tier
WHERE r.triggered_at >= '2026-05-01'
AND c.current_plan_tier = 'Pro'
GROUP BY 1, 3
HAVING total_runs_mtd > 8000
ORDER BY total_runs_mtd DESC;
```
We need to be careful with the Verdant Cloud account; they have a custom override on their seat count licensed that isn't reflected in `dim_plans`. Checking with Finance Ops on how to join that.

---

**Gong Transcript: Verdant Cloud Discovery**
**Date**: May 15, 2026
**Participants**: Marcus Thorne (AE, Acme), Elena Rossi (CTO, Verdant Cloud)
**Account**: Prospect (Evaluating Enterprise)

[00:04:12] **Elena Rossi**: We’re looking for a replacement for our internal Python scripts. It’s just too much maintenance. But we need SOC2 compliance and, more importantly, we need to be able to host the runners on our own VPC. Does Acme support on-prem runners?

[00:04:30] **Marcus Thorne**: That’s a great question, Elena. Our "Hybrid Cloud" deployment is exclusive to our Enterprise tier. It allows you to keep the data plane in your AWS environment while we manage the control plane. It’s what Cobalt Systems is looking at right now for their Snowflake security requirements.

[00:04:51] **Elena Rossi**: And pricing for that? I’m assuming it’s not the $149/seat I see on your website.

[00:04:58] **Marcus Thorne**: Correct. Enterprise is custom. Typically, for a company of Verdant's scale—how many engineers do you have? About 300?—we’d look at a flat platform fee plus a per-user cost. We usually land in the $80k to $120k range for the initial rollout.

[00:05:17] **Elena Rossi**: [Silence for 4 seconds] $120k. Wow. Tray.io quoted us significantly less, but they charge per "workflow step." Your model is per user?

[00:05:32] **Marcus Thorne**: We find seat-based pricing is more predictable for budgeting. You don't want your bill to explode just because one engineer builds a very complex 50-step workflow. With Acme, once that user is licensed, they can build the most complex automation in the world and your cost doesn't change. It encourages innovation rather than penalizing it.

[00:05:54] **Elena Rossi**: I like the philosophy, but the entry point is high. What if we wanted to start with just the Marketing team? Say, 40 people?

[00:06:05] **Marcus Thorne**: We have a 250-seat minimum for Enterprise. If you want to start with 40, you’d technically fall into our Business tier, but you’d lose the VPC runner and the SOC2 report access. It’s a bit of a trade-off. Let me see if I can get a "Small Footprint" Enterprise waiver. It’s rare, but for a logo like Verdant, I can ask.

---
[00:06:22] **Elena Rossi**: Okay, Marcus. Let's do that. Send over the one-pager on the VPC runner architecture and I'll talk to my SecOps team. If we can get that Enterprise waiver for 40 seats, it might be a conversation. But $120k is a non-starter for just Marketing. We'll need to see if we can pull in the Data Science team to justify the spend.

[00:06:45] **Marcus Thorne**: Understood. I’ll get that over by EOD. Talk soon, Elena.

---
**Gong Call: Cobalt Systems QBR (Quarterly Business Review)**
**Date: January 14, 2026**
**Participants: Marcus Thorne (AE), Sarah Jenkins (CSM), David Wu (CTO, Cobalt Systems)**

[00:00:12] **Sarah Jenkins**: ...and before we dive into the usage metrics, David, how was the holiday? I saw on LinkedIn you were skiing in Whistler?

[00:00:24] **David Wu**: Oh, it was great, Sarah. A lot of powder. Though I spent half the time on Slack dealing with that Snowflake outage we had on the 28th. Actually, that’s a good segue. One of the reasons I wanted to talk today—besides the renewal—is how Acme handled that outage.

[00:00:41] **Marcus Thorne**: I saw the tickets. Your `fact_workflow_runs` logs show about 4,000 retries during that window.

[00:00:48] **David Wu**: Exactly. The auto-retry logic in Acme actually saved our backend from a lot of manual cleanup. But we’re seeing a massive spike in run volume. I was looking at our internal dashboard—well, the one we built querying the `nexus-analyst-demo.acme.fact_workflow_runs` table in our Snowflake sink—and we’re hitting about 1.2 million runs a month now.

[00:01:12] **Sarah Jenkins**: Yeah, I have the slide up right now. You guys are up 40% quarter-over-quarter. Most of that is coming from the "Inventory-Sync-Global" workflow. It looks like it’s triggering every 30 seconds?

[00:01:25] **David Wu**: Yeah, we moved the logistics engine over to Acme. It’s mission-critical now. Which brings me to the "Unlimited Runs" clause in our Enterprise contract. Are we still good there? I remember there was a "fair use" mention in the fine print.

[00:01:41] **Marcus Thorne**: David, you’re on the Enterprise tier. For Cobalt, "Unlimited" means exactly that. We’re not going to throttle you. However, as we look at the renewal in March, we do need to discuss the seat count. You’re currently licensed for 250 seats, but `dim_users` shows 312 active users. 

[00:02:03] **David Wu**: [Laughs] Yeah, the engineers love the tool. It’s addictive. We’ve got people in HR using it now to automate onboarding. Can we just true-up to 350? What’s that going to do to the ACV?

[00:02:18] **Marcus Thorne**: To keep the "Unlimited Runs" and the dedicated CSM support—and Sarah’s been doing a great job, right?—we’d be looking at moving the annual from $180k to about $245k.

[00:02:32] **David Wu**: $245k. That’s a jump. I’ll have to run that by Finance. They’re still asking why we aren't just using AWS Step Functions for the heavy lifting. I told them Acme is for the "citizen automator," but $245k is getting into "dedicated developer salary" territory.

---
**Gong Call: Harbor Dynamics - Discovery / Upgrade Path**
**Date: February 02, 2026**
**Participants: Marcus Thorne (AE), Ben Thompson (Head of Engineering, Harbor Dynamics)**

[00:01:05] **Ben Thompson**: ...Right now, we're on the Pro plan. We have about 12 people using it. It's mostly just me and a few lead devs. But the rest of the company is starting to ask for access. My CMO wants to plug in HubSpot and some weird LinkedIn scraper.

[00:01:22] **Marcus Thorne**: Classic. Once the word gets out that you can automate the boring stuff, everyone wants a seat. So, Harbor is currently at 12 seats on Pro, that's $49/seat?

[00:01:34] **Ben Thompson**: Yeah, roughly $600 a month. It's a rounding error. But if I add the 40 people in Marketing and the 15 in Sales... we're over the 50-seat threshold for the Business tier, right?

[00:01:48] **Marcus Thorne**: That’s correct. Once you hit 50 seats, the platform requires a move to the Business tier at $149/seat. 

[00:01:57] **Ben Thompson**: Wait, so it goes from $49 to $149 just because we added more people? That’s a 3x price increase per person. What do we actually get for that extra hundred bucks?

[00:02:10] **Marcus Thorne**: It's a significant step up. You get SAML SSO—which I'm sure your IT team is going to demand once you have 60 people in the tool—plus the Audit Logs. If a Marketing intern accidentally deletes a production workflow that’s syncing your CRM, the Business tier lets you see exactly who did it and roll back the version. Pro doesn’t have version history beyond 7 days. Business gives you 90.

[00:02:35] **Ben Thompson**: I hate the "tax on security" model, Marcus. Everyone does it, but it still sucks. And the quota? We’re hitting about 8k runs a month now.

[00:02:46] **Marcus Thorne**: On Business, your quota jumps to 100k runs per month. You also get priority support. If a workflow fails, you're not waiting in the standard queue; you're at the front of the line.

[00:03:01] **Ben Thompson**: I’ll have to check the `fact_invoices` for our last few months to see what we've actually been paying with overages. I think we've been paying for extra runs anyway. But $149 for 60 seats... that’s like $9k a month? My boss is going to flip. Can we stay on Pro and just pay for 60 seats?

[00:03:22] **Marcus Thorne**: The system actually hard-caps Pro at 49 seats. At 50, the provisioning engine forces an upgrade. It’s part of the `dim_plans` logic in our backend. I can offer a 15% "Growth Discount" for the first year to bridge the gap, but the tier shift is non-negotiable for that size.

---
**Gong Call: Sable Analytics - Renewal Negotiation**
**Date: March 12, 2026**
**Participants: Jamie Vance (AE), Rachel Glass (Procurement, Sable Analytics)**

[00:04:15] **Rachel Glass**: Jamie, I’m looking at this renewal and I’m confused. We signed up for 100 seats on the Business plan last year. Your report says we only have 62 "Active Users" in the last 30 days. Why are we renewing for 100?

[00:04:31] **Jamie Vance**: Hi Rachel. So, the 100 seats is the contracted minimum for the discount we gave Sable last year. Even if only 62 people logged in this month, the seats are provisioned and available. If you look at `dim_customers` for Sable, you’ve actually had 88 unique users log in over the last six months. 

[00:04:52] **Rachel Glass**: But we’re trying to trim the fat. Can we drop the commitment to 75 seats? 

[00:05:00] **Jamie Vance**: If we drop to 75, we’d have to move back to the standard $149 rate. You’re currently on a legacy "Early Bird" rate of $110. If we lower the seat count, the unit price goes up, and you’ll actually end up paying almost the same total amount but with less room to grow.

[00:05:21] **Rachel Glass**: [Sighs] The classic lock-in. What about the run usage? We’re only using about 30k of our 100k quota. Can we trade some of that unused quota for more seats?

[00:05:35] **Jamie Vance**: I wish I could, but the plans are pretty rigid. The quotas are tied to the `plan_tier` in the `dim_plans` table. However, what I can do is throw in a "Professional Services" credit. We can have one of our engineers spend a day with your team to help them build out more complex integrations—maybe get that usage up so you're getting more value out of the 100 seats?

[00:06:01] **Rachel Glass**: I'll talk to the team. But if we don't see more adoption by Q3, we're going to have to look at Zapier's Team plan. They don't have these seat minimums.

[00:06:12] **Jamie Vance**: I understand the pressure, Rachel. Just keep in mind, Zapier doesn't give you the BigQuery direct sink that you're using for your `fact_user_events` analysis. If you move, you'd have to build that bridge yourself.

[00:06:25] **Rachel Glass**: True. That sink is the only reason my Data team hasn't revolted yet. Send me the proposal for the 100 seats with the PS credit. I'll see if I can push it through.

[00:00:05] **Marcus Thorne**: Hey Leo, good to see you. How was the move to the new office in Austin?

[00:00:11] **Leo Rossi**: Oh man, it’s a construction zone. My "private office" currently doesn't have a door. But the coffee machine works, so we’re surviving. How’s things at Acme?

[00:00:19] **Marcus Thorne**: Busy. We just closed our Series B and the product team is moving fast on the new SOC2 compliance features. But I wanted to huddle because I saw Harbor Dynamics is sitting at 242 active users this morning. If you look at `nexus-analyst-demo.acme.dim_customers`, your `seat_count_licensed` is exactly 250.

[00:00:38] **Leo Rossi**: Yeah, we’ve got a batch of 15 new SDRs starting on Monday. I was actually going to email you. We’re going to blow past that 250 limit by lunch. 

[00:00:46] **Marcus Thorne**: So here’s the thing—once you hit 250, you’re technically in the Enterprise tier territory. Right now you’re on the Business plan at $149 a seat. Moving to Enterprise actually opens up the custom ACV pricing and the dedicated CSM—well, you already have me, but it becomes "official" [laughs]. 

[00:01:04] **Leo Rossi**: What’s the damage? I saw the `dim_plans` table lists Enterprise as "Custom." That usually means "Expensive."

[00:01:12] **Marcus Thorne**: It depends on the volume. Since you’re already doing about 90k workflow runs a month—I checked your `fact_workflow_runs` activity—the unlimited quota on Enterprise is going to save you from the overage fees we talked about last quarter. If we commit to a 300-seat floor, I can probably get the per-seat cost down to $125, but we’d need to move to an annual contract.

[00:01:34] **Leo Rossi**: $125 is better than $149. But does that include the audit logs? Our security guy, Dave, is breathing down my neck about the `fact_user_events` trail. He wants to see exactly who edited the Salesforce-to-NetSuite sync last Tuesday.

[00:01:51] **Marcus Thorne**: Absolutely. Enterprise gives you the full retention on audit logs. You can query them directly in BigQuery via `nexus-analyst-demo.acme.fact_user_events`. No more 30-day expiration.

[00:02:04] **Leo Rossi**: Send me the docs. I have to run to a meeting about why the Wi-Fi in the breakroom is down.

---

[00:00:02] **Sarah Jenkins**: ...and that’s why we usually win against Tray. It’s not just about the connectors; it’s about the underlying data stability. 

[00:00:11] **Elena Wu**: I hear you, Sarah. But Cobalt is a startup. We’re 45 people. Your "Business" tier starts at 50 seats. You’re asking me to pay for five empty chairs just to get SSO and the BigQuery sink.

[00:00:26] **Sarah Jenkins**: I totally get that. The 50-seat minimum for the Business plan is there because that’s the threshold where we see teams really needing the governance features—SSO, the audit logs, priority support. If you stay on the Pro plan at $49/seat, you’re only paying for 45 people, but you lose the `nexus-analyst-demo.acme.fact_invoices` breakdown by department and you’re capped at 10k runs.

[00:00:49] **Elena Wu**: We’re already at 8k runs and we haven’t even turned on the HubSpot integration yet. If we hit the cap, does everything just... stop?

[00:00:58] **Sarah Jenkins**: It doesn’t stop, but you’ll see `error_code` 'QUOTA_EXCEEDED' in your `fact_workflow_runs` table for any new triggers until the next billing cycle. Or you can buy "Run Packs." But honestly, Elena, if you’re growing as fast as your LinkedIn says, you’ll hit 50 employees by July.

[00:01:15] **Elena Wu**: True. We have 8 open reqs. 

[00:01:18] **Sarah Jenkins**: Exactly. If we sign the Business agreement today, I can waive the implementation fee. You’d be looking at $7,450 a month for the 50 seats. It’s an investment in the plumbing. You don't want to be rebuilding your workflows in Tray in six months because you outgrew our Pro tier.

[00:01:35] **Elena Wu**: [Pause] What about the "Free" tier? Can we just put our developers on that to test the BigQuery sink?

[00:01:42] **Sarah Jenkins**: The Free tier doesn't include the warehouse sink. You need at least the Pro plan to access the `nexus-analyst-demo.acme` datasets for your own account. But I can give you a 14-day trial of the full Business suite if that helps?

---

[00:00:04] **Benji Okafor**: Hi Samir, thanks for jumping on. I’m looking at your instance for Verdant Cloud. You mentioned some workflows are failing?

[00:00:12] **Samir Gupta**: Yeah, it’s weird. We have this "Daily Sync" that’s been running fine for months. Suddenly yesterday, it started failing every five minutes. The error logs in the UI are a bit vague.

[00:00:23] **Benji Okafor**: Okay, let me pull up the `fact_workflow_runs` for your `customer_id`. One second... okay, I see it. You’re hitting a 504 timeout on the step where you’re calling the Slack API. 

[00:00:36] **Samir Gupta**: Slack? We aren't even sending that many messages. 

[00:00:40] **Benji Okafor**: It looks like you have a loop. In the workflow `wf_8829_prod`, you’ve got a "For Each" iterator that’s trying to process 5,000 rows from a Google Sheet, and for every row, it’s checking a condition and then hitting Slack. You’re essentially DDOSing your own Slack rate limit. 

[00:00:58] **Samir Gupta**: Oh. That... yeah, that makes sense. We did just dump the entire Q1 lead list into that sheet. 

[00:01:05] **Benji Okafor**: [Laughs] Yeah, that'll do it. Also, just a heads up—because that loop ran so many times, you’ve used 42k runs in the last 24 hours. You’re currently at 98,500 for the month. 

[00:01:18] **Samir Gupta**: Wait, our limit on the Business plan is 100k, right? 

[00:01:22] **Benji Okafor**: Correct. `dim_plans` for the Business tier is hard-capped at 100k unless you’ve got an Enterprise override. You’re going to hit the ceiling by this evening if that workflow triggers again.

[00:01:33] **Samir Gupta**: Can you reset it? This was an accident.

[00:01:37] **Benji Okafor**: I can’t "reset" the count because it’s a direct reflection of the `fact_workflow_runs` table, and Finance uses that for the `fact_invoices` generation. But what I can do is give you a one-time "grace" of 20k runs. I'll put a note in the system for your CSM—looks like that’s Jamie Vance—so they know why there's a discrepancy between your usage and your tier quota.

[00:01:58] **Samir Gupta**: You're a lifesaver, Benji. I'm going to go disable that iterator before it eats the rest of my quota.

---

[00:00:03] **Jamie Vance**: ...so when we look at the usage for Sable Analytics, the "User Engagement" score is actually up 15% month-over-month.

[00:00:12] **Rachel Glass**: Is that coming from the `dim_users` activity or just the automated runs? Because we've been trying to get the Marketing team to actually log in and use the dashboarding instead of asking me for CSVs.

[00:00:24] **Jamie Vance**: It’s both. I’m seeing 78 `last_login_date` entries in the last 14 days in `dim_users`. That’s pretty high for a 100-seat contract. Your "Is Active" flag is true for about 85% of the provisioned seats.

[00:00:41] **Rachel Glass**: That's actually better than I thought. Maybe the PS credit helped. The training session your engineer did on "Self-Serve Workflows" really clicked for the junior analysts. 

[00:00:52] **Jamie Vance**: Glad to hear it. Since you're nearing that 90% seat utilization, do you want to talk about adding another 25 seats now? If we do it mid-cycle, the `fact_subscriptions` entry just gets a `change_type` of 'UPGRADE' and we pro-rate it. It’s cleaner than waiting for the renewal and having people get "Seat Full" errors.

[00:01:10] **Rachel Glass**: Let me check the `fact_invoices` from last month first. I need to see how much we spent on those extra run packs before I commit to more seats. My CFO is obsessed with the "Cost per Active User" metric.

[00:01:24] **Jamie Vance**: I can send you a query for that if you want. It basically joins `dim_customers` with the sum of `mrr_usd` from `fact_subscriptions` divided by the distinct count of `user_id` in `fact_user_events`. 

[00:01:38] **Rachel Glass**: You guys really are a data company, aren't you? Fine, send the query. If the math checks out, we'll add the seats.

[00:00:02] **Sarah Jenkins**: Thanks for hopping on, Liam. I know the Harbor Dynamics team is slammed with the Q3 planning. I wanted to touch base on the trial—I saw your team logged about 4,500 runs in `fact_workflow_runs` just this week. 

[00:00:15] **Liam Zhao**: Yeah, it’s been... intensive. We’re migrating a lot of our legacy cron jobs from that old Python server. My main concern right now is the "Business" tier vs "Enterprise." You mentioned the 50-seat minimum for Business, but we only have 35 people in the Ops team who actually need builder access. 

[00:00:32] **Sarah Jenkins**: Right, so the Business tier is $149 per seat with that 50-seat floor. Even if you only provision 35 users in `dim_users`, the `fact_subscriptions` record will show 50 licensed seats. The upside there is the SSO and the audit logs. If you’re looking at Harbor’s compliance requirements for 2026, you’re going to want those `fact_user_events` tracked for your SOC2.

[00:00:54] **Liam Zhao**: We were looking at Zapier, but their "Company" plan gets crazy expensive when you scale the task count. You guys do "runs," not "tasks," right? Like, one run can have twenty steps?

[00:01:06] **Sarah Jenkins**: Exactly. We look at the `run_id` in the `nexus-analyst-demo.acme.fact_workflow_runs` table. It doesn't matter if that run has two steps or fifty—it’s one run against your quota. On Business, you get 100K runs a month. 

[00:01:21] **Liam Zhao**: What happens if we hit that? Do we just... stop? 

[00:01:25] **Sarah Jenkins**: No, we don't hard-stop you unless it's a security thing. You'll just see an overage on the next `fact_invoices` entry. But if you’re worried about predictability, that’s where we start talking about the Enterprise tier. That has the "Unlimited" quota. Usually, once a customer hits about 200k runs a month consistently, the custom ACV for Enterprise actually ends up being cheaper than the Business overages.

---

[00:03:45] **Jamie Vance**: ...and that’s why the `error_code` 'ERR_429' keeps popping up for Cobalt Systems. It’s not an Acme platform issue, it’s actually the Shopify API rate-limiting your webhooks.

[00:03:58] **Marcus Thorne**: I figured as much. It’s just annoying because it makes our success rate in the dashboard look like garbage. I’m seeing like 12% failure in the `status` column for our "Order Sync" workflow.

[00:04:10] **Jamie Vance**: I can show you a trick for that. If you add a "Retry Logic" step with an exponential backoff, it'll handle those 429s automatically. Also, I noticed you guys have 48 users active. You’re only two seats away from that Business tier threshold. 

[00:04:25] **Marcus Thorne**: Don't start, Jamie. I know. The Pro plan at $49 is fine for now. If I move to Business, my monthly spend triples.

[00:04:35] **Jamie Vance**: True, but you’re currently paying for three different "Pro" run-packs every month because you’re blowing through the 10K limit. I ran a quick query on your `fact_invoices` from January through March 2026—you’re actually averaging $112 per seat anyway because of the overages. 

[00:04:55] **Marcus Thorne**: Wait, really? Is that because of the "Marketing Automation" folder? 

[00:05:01] **Jamie Vance**: Yeah, if you look at `fact_workflow_runs` filtered by `customer_id` for Cobalt, that one folder is responsible for 60% of your volume. If we move you to Business, you get 100K runs included. It actually might be a wash, cost-wise, and you’d get the priority support queue.

[00:05:18] **Marcus Thorne**: (Sighs) Send me the breakdown. If I can show the CFO that the `amount_usd` is basically flat but we get better support, he might bite.

---

[00:00:10] **Elena Rossi**: We’re seeing some latency on the `triggered_at` timestamps for our Verdant Cloud "Health Check" flows. It’s supposed to be near-instant, but sometimes there’s a 30-second lag.

[00:00:22] **Jamie Vance**: Let me pull up the internal logs. One sec... Okay, I’m looking at your `fact_workflow_runs` for the last hour in the `nexus-analyst-demo.acme` dataset. I see what you mean. The `duration_ms` is fine, but the gap between the webhook hitting our gateway and the `triggered_at` start time is spiked.

[00:00:41] **Elena Rossi**: Is it a noisy neighbor thing? I thought being on Enterprise meant we had dedicated compute for the worker nodes.

[00:00:49] **Jamie Vance**: You do, but it looks like you’ve got a massive "Bulk Import" workflow running in parallel that’s saturating your specific worker pool. It’s got like 500 `step_count` per run? 

[00:01:02] **Elena Rossi**: Oh, that’s probably the Salesforce cleanup script the interns started. I didn't realize that would affect the high-priority flows.

[00:01:10] **Jamie Vance**: Yeah, the worker doesn't know the difference unless we tag them. Since you’re on the Enterprise plan, we can actually use "Workload Isolation." We can point those "Health Check" flows to a reserved pool so they don't get stuck behind the Salesforce imports. 

[00:01:25] **Elena Rossi**: That would be huge. Can you set that up? Or do I need to open a ticket?

[00:01:30] **Jamie Vance**: I'll do it right now. I just need to update the `account_tier` flags on our side to enable the routing rules. By the way, how is the team liking the new dbt integration? I saw a few `user_id` entries from your Data Eng team yesterday in `fact_user_events`.

[00:01:45] **Elena Rossi**: They love it. Being able to trigger an Acme workflow directly after a dbt cloud run finishes—without using a messy Python wrapper—saved them like five hours of setup last week. We’re actually thinking about moving our entire ETL alerting into Acme. 

[00:02:01] **Jamie Vance**: Love to hear that. Just keep an eye on the run volume. Even with "Unlimited," if you start hitting 10 million runs a month, we’ll probably need to revisit the `fact_subscriptions` terms at the next renewal in June.

---

[00:08:12] **Benji**: ...so the reason the `last_login_date` isn't updating in your `dim_users` export is because they're authenticating via the API key, not the UI.

[00:08:22] **Samir Gupta**: Ah, okay. That makes sense. I was worried we had 20 "ghost" users who hadn't logged in for months. 

[00:08:28] **Benji**: Yeah, the `is_active` flag is probably a better metric for you to track. If you join `dim_users` with `fact_user_events` on `user_id`, you can see if they’ve made an API call in the last 30 days. That’ll give you the true "active" count regardless of UI login.

[00:08:44] **Samir Gupta**: Got it. Hey, while I have you—we’re seeing a lot of `error_code` 'AUTH_EXPIRED' on the Tray.io migration workflows. Is there a way to bulk-refresh those credentials?

[00:08:55] **Benji**: Not in the UI yet, but you can do it via the Acme CLI. Just loop through the connection IDs. Honestly, Tray's auth handling is a bit different than ours, so some of those older tokens won't carry over. You’ll likely need to re-auth the Oauth2 flows manually for the Business-tier apps like Salesforce or Workday.

[00:09:15] **Samir Gupta**: Ugh, okay. I’ll tell the team. We’re still on track to shut down the Tray instance by the end of the month. My boss is breathing down my neck to get that `mrr_usd` off the books.

[00:09:25] **Benji**: We’ll get you there. If you hit any more snags with the migration, just ping the "Migration-Help" Slack channel. Jamie and I are both in there.

---

[00:14:22] **Sarah Jenkins**: ...and that’s really why the shift to Enterprise makes sense for Verdant Cloud right now. Marcus, I know you’re looking at the seat count—we’re at 210 provisioned users in `dim_users` currently—but the jump to the 250-seat Enterprise minimum unlocks the custom SLA and the dedicated CSM.

[00:14:38] **Marcus Thorne**: Yeah, I see the value in the SLA, Sarah. Honestly, our uptime requirements for the provisioning workflows are getting intense. But 250 seats? We only have 215 people in the whole Engineering and Ops org. I’d be paying for 35 "ghost" seats just to get the SOC2 report and the audit logs.

[00:14:55] **Sarah Jenkins**: I totally hear you. Think of it less as paying for ghosts and more as securing the price floor for your next phase of growth. Plus, with the Enterprise tier, you get unlimited workflow runs. Looking at your `fact_workflow_runs` from last month, you guys hit 98,000. You’re literally 2,000 runs away from the Business tier cap. If you stay on Business, those overages are going to cost you more than the seat uplift anyway.

[00:15:20] **Marcus Thorne**: [Sighs] Can you send over the breakdown of how those overages are calculated? I need to show my CFO why $149/seat on Business is actually riskier than the $50k flat Enterprise entry.

[00:15:32] **Sarah Jenkins**: Absolutely. I’ll pull the data from `nexus-analyst-demo.acme.fact_workflow_runs` and project your growth for Q3 and Q4. I’ll have it to you by EOD.

---

[00:02:15] **Jamie Vance**: Thanks for hopping on, Chloe. I saw your note about the Zapier migration. How's the transition for Harbor Dynamics going?

[00:02:22] **Chloe Zhao**: It’s... a process. Zapier's "task" pricing was just killing us. Every time we ran a multi-step loop, it felt like we were getting billed per breath. We’ve moved about 40% of our marketing automations over to Acme Pro.

[00:02:35] **Jamie Vance**: Glad to hear the Pro tier is working out. Are you hitting any friction with the 10k run limit?

[00:02:41] **Chloe Zhao**: Not yet, but we’re starting to look at the Business tier. We need SSO. My IT team is breathing down my neck because we have 60 people with individual logins and no way to revoke access centrally when someone leaves.

[00:02:55] **Jamie Vance**: Yeah, the Business tier is the sweet spot for that. It starts at 50 seats, so at $149 a seat, it’s a jump from Pro, but you get the SAML/SSO and the 100k run quota. If you look at `dim_plans`, the Business tier is where most of our Mid-Market customers live once they pass that 50-employee mark.

[00:03:12] **Chloe Zhao**: Does the Business tier include the Workday integration? We’re trying to automate our onboarding flow—basically, when a new hire is added in Workday, Acme should trigger the laptop provisioning in Jamf and the Slack invite.

[00:03:25] **Jamie Vance**: It does. That’s a standard Business-tier connector. You won’t need to mess with custom API calls or the CLI for that. I can set up a trial of the Business features for your account so your IT lead can test the SSO config. 

---

[00:22:05] **Benji**: ...so the reason the `duration_ms` is spiking in your `fact_workflow_runs` table for the "Daily Inventory Sync" is that the Shopify API is throttling you. It’s not an Acme bottleneck.

[00:22:18] **Alex (Cobalt Systems)**: I figured it was something like that. We’re seeing a lot of `error_code` '429' in the logs. Is there a way to build a retry logic directly in the workflow?

[00:22:28] **Benji**: Definitely. You can use the "Wait and Retry" block. But honestly, if you’re doing this for 50,000 SKUs every morning, you might want to look at using our bulk-ops connector. It’ll reduce your step count, which makes the `fact_workflow_runs` table a lot cleaner to query. 

[00:22:45] **Alex (Cobalt Systems)**: Speaking of querying, I was looking at `nexus-analyst-demo.acme.dim_customers` to try and pull our own usage for a dashboard, but I can't see our `current_mrr_usd`. Is that restricted?

[00:22:58] **Benji**: Yeah, the MRR fields are usually restricted to the `ae_employee_id` or the Finance role. If you need a report on your spend for the renewal, I can have Jamie Vance pull a summary from `fact_subscriptions`. You guys are still on the Business plan through October, right?

[00:23:15] **Alex (Cobalt Systems)**: Yeah, October 2025. We’re actually talking about adding 20 more seats because the support team wants to use Acme to automate Zendesk ticket routing. Does that change our `billing_cycle`?

[00:23:25] **Benji**: It shouldn't change the cycle, just a pro-rated invoice in `fact_invoices`. I’ll flag it for Jamie. 

---

[00:05:40] **Sable Analytics Rep**: We’re comparing you guys to Tray.io right now. Their price per workflow is lower, but the seat minimum is higher. How does Acme handle "unlimited workflows" on the Pro tier?

[00:05:52] **Jamie Vance**: It’s truly unlimited. We don’t gate the number of automations you build. We care about the *seats*—the people building and managing them—and the total *runs*. If you have one workflow that runs a million times, you’ll hit a quota. But if you have 500 workflows that run once a day, you’re golden on the Pro tier.

[00:06:10] **Sable Analytics Rep**: And the data warehouse access? Can we pipe our Acme usage data directly into our own BigQuery?

[00:06:18] **Jamie Vance**: For Enterprise customers, we offer a direct Snowflake or BigQuery share. You’d get access to the same flat tables we use internally—`dim_users`, `fact_workflow_runs`, all of it. It’s great for building custom ROI dashboards. For Pro and Business, you’d just use the standard Export API or the CSV exports in the UI.

[00:06:35] **Sable Analytics Rep**: Okay. We’re at about 45 people right now, so we’re just under that Business-tier seat minimum of 50. If we start on Pro at $49/seat, can we mid-term upgrade to Business when we hit 50?

[00:06:48] **Jamie Vance**: Absolutely. It’s a one-click upgrade. The `change_type` would just show up as an 'UPGRADE' in your `fact_subscriptions` record, and we’d pro-rate the difference. Most of our high-growth startups do exactly that. They start SMB and move to MM (Mid-Market) within six months.

---

[00:11:05] **Elena Rossi**: One last thing, Benji. I’m seeing some weirdness in `dim_users`. I have about five users who show `is_active = false` but they still have `last_login_date` from yesterday. How is that possible?

[00:11:18] **Benji**: That usually happens if a user is deactivated at the SSO level but their session token hasn't expired yet, or if they were manually toggled off in the Acme admin panel while they were still logged in. I’d trust the `is_active` flag for billing purposes—that’s what `fact_subscriptions` uses to calculate your `seat_count` for the next invoice.

[00:11:36] **Elena Rossi**: Got it. We’re trying to clean up our seat count before the June renewal. I don’t want to pay $149 for people who aren't actually building anything.

[00:11:45] **Benji**: Totally. Just run a join between `dim_users` and `fact_user_events`. If they haven't had an event in 60 days, they're safe to prune. I can send you a SQL snippet for that if you want.

[00:11:55] **Elena Rossi**: Please do. Send it to my work email. Thanks, Benji.

---
[00:14:22] **Jamie Vance**: Hey Marcus, can you hear me? I think your mic is picking up a lot of background noise. Sounds like a construction site over there.

[00:14:30] **Marcus Thorne (Cobalt Systems)**: Oh, sorry Jamie. Yeah, they’re doing the HVAC in the Philly office today. It’s a mess. Let me just hop into a phone booth. One sec. 

[00:14:45] **Marcus Thorne**: Okay, better? 

[00:14:47] **Jamie Vance**: Much better. So, I was looking at your usage in `nexus-analyst-demo.acme.fact_workflow_runs` this morning. Cobalt is pushing serious volume. You guys hit 92,000 runs last month. You’re right up against that 100k cap on the Business tier.

[00:15:02] **Marcus Thorne**: Yeah, that’s actually why I wanted to chat. We’re migrating our entire lead routing logic from Zapier over to Acme because the latency on Zapier was just killing our SDR response times. But we’re also hiring another 30 people in Sales Ops next month. That puts our total seat count at 240. 

[00:15:20] **Jamie Vance**: Right. So, the Business tier has that $149/seat price point, but once you cross 250, we usually talk Enterprise. Honestly, Marcus, if you’re planning to hit 250 seats anyway, we should just move you to Enterprise now. You get the unlimited workflow runs, which solves your 100k cap issue, and we can get you that dedicated Slack channel with our engineering team. 

[00:15:42] **Marcus Thorne**: What’s the price jump? Because my CFO is going to see "Enterprise" and think I’m trying to buy a private jet.

[00:15:49] **Jamie Vance**: It’s actually more cost-effective at your scale. Instead of $149/seat flat, we move to a tiered ACV model. For 250 seats, I can probably get you in around $110k/year. If you stayed on Business at 250 seats, you’d be paying closer to $447k a year. 

[00:16:08] **Marcus Thorne**: Wait, $110k total? Or $110k on top of what we pay?

[00:16:12] **Jamie Vance**: $110k total annual contract value. The seat cost effectively drops because you're committing to the volume. Plus, you’ll show up as `account_tier = 'Ent'` in our system, which triggers the priority support SLA. I noticed you had a couple of workflows fail with `error_code` 'RATE_LIMIT_EXCEEDED' last Tuesday—on Enterprise, we can white-label those IP addresses to prevent that.

[00:16:35] **Marcus Thorne**: Okay. Send over the SOC2 Type II report as well. Our legal team won't even look at an Enterprise contract without the latest audit logs and the security package.

---

[00:02:10] **Benji**: ...and that’s why the `duration_ms` in `fact_workflow_runs` might look slightly higher than what you see in your own internal logs. We measure from the moment the webhook hits our gateway to the final 200 OK response.

[00:02:22] **Sarah Jenkins (Harbor Dynamics)**: That makes sense. We’ve been trying to reconcile this in BigQuery. I’ve been querying `nexus-analyst-demo.acme.fact_workflow_runs` and joining it against our own `order_id` table. We’re seeing about a 3% discrepancy.

[00:02:38] **Benji**: 3% is usually just cold starts on the initial node. If a workflow hasn't run in 24 hours, the first trigger takes an extra 200ms to spin up the container. 

[00:02:49] **Sarah Jenkins**: Got it. Hey, while I have you, we’re looking at the Business plan. We currently have 42 users on Pro. If we upgrade to Business to get the SSO—since our IT team is breathing down my neck about Okta integration—do we have to pay for 50 seats even if we only have 42 people?

[00:03:08] **Benji**: Yeah, the Business tier has a 50-seat floor. So even if `dim_users` only shows 42 records for `customer_id` 'HARBOR-77', the `fact_subscriptions` table will show a `seat_count` of 50. It’s basically a $7,450 monthly minimum ($149 * 50). 

[00:03:25] **Sarah Jenkins**: Ouch. That’s a big jump from the $2,058 we’re paying now on Pro. 

[00:03:31] **Benji**: It is, but you’re also getting the audit logs. If someone deletes a production workflow, you can actually see who did it in the `fact_user_events` table. On Pro, once it’s gone, it’s gone.

[00:03:44] **Sarah Jenkins**: True. We actually had someone—I think it was a contractor—mess up a HubSpot sync last week and it took us two days to figure out what happened. 

---

[00:08:15] **David Wu (Verdant Cloud)**: We’re currently using Tray.io for most of this, but their pricing is getting out of hand with the "task-based" billing. Every time we loop through an array, it counts as a task. Does Acme do that?

[00:08:28] **Jamie Vance**: No, we hate task-based billing. We charge by the "Run." A run is one execution of a workflow, regardless of whether it has 2 steps or 200 steps. If you look at `nexus-analyst-demo.acme.fact_workflow_runs`, you’ll see a `step_count` column. We track it for our own infra costs, but it doesn't affect your bill.

[00:08:48] **David Wu**: That’s a relief. We do a lot of data heavy-lifting. Like, we’ll pull 5,000 rows from a Postgres DB and iterate through them to update records in Salesforce. In Tray, that’s 5,000 tasks. In Acme, that’s just one run?

[00:09:02] **Jamie Vance**: Exactly. One `run_id`. Now, if you’re doing that every 5 minutes, you’ll hit that 100k monthly limit on the Business plan pretty quickly. But for most Mid-Market companies, 100k runs is plenty. 

[00:09:16] **David Wu**: What about the "Free" tier? I saw on your site you have a free version. Can we use that for dev/test?

[00:09:23] **Jamie Vance**: You can, but it’s limited to 2 active workflows and 100 runs. Most of our users just stay on the Pro tier for testing because $49/mo is basically a rounding error for them. If you’re coming from Tray, you’re probably looking at our Business tier anyway for the SSO. You guys use Okta or Azure AD?

[00:09:42] **David Wu**: We’re an Okta shop. And yeah, SSO is a hard requirement. Our security team won’t let us buy anything that doesn't support SAML. 

[00:09:51] **Jamie Vance**: Then Business is your starting point. I can get you a 14-day trial of the Business features so you can test the SSO setup. I’ll just need to manually flip your `current_plan_tier` in the backend so you don't get prompted for a credit card immediately.

[00:10:05] **David Wu**: Sounds good. Send me the docs on the BigQuery export too. We want to pipe our Acme logs into our own Snowflake instance eventually.

[00:10:14] **Jamie Vance**: You got it. I'll send over the schema for `fact_workflow_runs` and `fact_user_events`. It’s super clean—flat tables, no crazy nested JSON.

---
[00:22:12] **Elena Rossi**: Benji, I'm looking at this SQL you sent. `SELECT * FROM nexus-analyst-demo.acme.dim_users WHERE last_login_date < DATE_SUB(CURRENT_DATE(), INTERVAL 60 DAY)`. If I run this and then deactivate these users in the UI, will my next invoice automatically reflect the lower seat count?

[00:22:30] **Benji**: Only if you're on the Pro plan. On Pro, we bill per-active-seat. But since you guys are on the Business plan, remember you have that 50-seat minimum. You’re currently at 62 seats. If you prune 15 users, you’ll drop to 47 "active" users, but you’ll still be billed for 50. 

[00:22:48] **Elena Rossi**: Right, the floor. I forgot about that. So I might as well keep those extra 3 seats open for the new hires in Marketing then.

[00:22:56] **Benji**: Exactly. No point in deleting them if you're paying for the capacity anyway. Just check `seat_count_licensed` in `dim_customers` to see exactly where your floor is set. 

[00:23:08] **Elena Rossi**: Cool. Thanks for the heads up. I almost cut some people we actually need just to save a buck. Talk soon.

---
[00:03:12] **Sarah Jenkins**: ...and honestly Marcus, the weather in Seattle this time of year is why I moved to SF. I just couldn't do the grey anymore. Anyway, let’s dive into this QBR for Sable Analytics. I was pulling some numbers from `nexus-analyst-demo.acme.fact_workflow_runs` this morning and you guys are absolutely crushing your 100k monthly quota on the Business plan. 

[00:03:34] **Marcus Thorne**: Yeah, I saw the notification last Tuesday. We hit 92k runs and there were still five days left in the month. We had to pause a few of the non-critical Slack notification hooks just to make sure the NetSuite-to-Snowflake sync didn't fail. It's becoming a bit of a headache.

[00:03:51] **Sarah Jenkins**: I totally get it. I looked at the trend in your `fact_workflow_runs` and you’ve been growing about 15% month-over-month. If we keep this pace, you’re going to be hitting that ceiling every month by the second week of the quarter. 

[00:04:05] **Marcus Thorne**: What are my options? I know the Business tier is capped at 100k. Do we just pay overages or is it time to talk about the 'E' word?

[00:04:14] **Sarah Jenkins**: (laughs) The "Enterprise" word isn't as scary as it sounds! For Sable, it actually makes a lot of sense. On Enterprise, we remove the workflow run quota entirely. Plus, you get the dedicated CSM—which is me, but I get more "official" resources to help you with architecture. 

[00:04:32] **Marcus Thorne**: And the price? We’re currently at 75 seats on Business. That’s what, $11,175 a month?

[00:04:40] **Sarah Jenkins**: Exactly, $149 a seat. For Enterprise, we usually start around $50k ACV, but since you're already doing $130k+ ARR, we’d look at a custom contract. It would likely involve a seat bump. Enterprise has a 250-seat floor, but we can talk about a ramp-up period if you aren't ready to provision all 250 today.

[00:05:01] **Marcus Thorne**: 250 is a big jump from 75. Let me talk to our CFO. Send me the deck on the Enterprise-only features, especially the custom SLA and the log retention stuff. Our security guys are asking why we only have 30 days of logs in the UI.

---
[00:12:44] **Jamie Vance**: ...Right, so that’s the main difference between us and Tray. We don't charge per 'connector' or per 'step'. It’s all based on the seat count and the total run volume. 

[00:12:56] **Linda Zhao**: That’s refreshing. We’re with Cobalt Systems and we’ve been using Zapier for the simple stuff, but once we started getting into complex branching logic for our lead routing, the Zapier bill just exploded. We have about 120 people who would need access, mostly in Sales Ops and Marketing.

[00:13:14] **Jamie Vance**: 120 seats puts you right in our sweet spot for the Business plan. Since our minimum for Business is 50 seats, you’re well above that. You’d get the SSO through Okta, which I assume your IT team is going to demand?

[00:13:28] **Linda Zhao**: Oh, absolutely. If it doesn't have SAML, it's a non-starter. What’s the per-seat on that?

[00:13:34] **Jamie Vance**: It's $149 per seat per month. If you went with the Pro plan, it's only $49, but you lose the SSO, the audit logs, and you’re capped at 10k runs. Given Cobalt’s scale, you’d blow through 10k runs in about three days.

[00:13:51] **Linda Zhao**: (Silence) $149 is... a significant jump from $49. That's a 3x increase just for SSO and more runs?

[00:14:02] **Jamie Vance**: I know it looks that way on the surface, Linda. But think about the governance. With 120 users, you don't want people using personal emails or leaving the company but still having access to your production workflows. One bad delete in a Salesforce sync could cost you way more than the price difference. You can actually see the seat breakdown in our `nexus-analyst-demo.acme.dim_plans` table if you want to compare the storage and SLA tiers side-by-side.

[00:14:31] **Linda Zhao**: Fair point. Can we do a trial of the Business features first? I want to see how the audit log captures changes to the webhooks.

---
[00:18:22] **Benji**: Hey Derek, good to see you again. How’s the integration going with the new ERP?

[00:18:28] **Derek Vogt**: It’s been a bit of a slog, Benji. Harbor Dynamics has a lot of legacy junk we’re trying to clean up. Honestly, I was looking at the usage reports you guys sent over and I'm a little concerned. We're paying for 60 seats on the Business plan—since that’s just above your 50-seat floor—but it looks like only 22 people logged in last month.

[00:18:50] **Benji**: I noticed that too when I was running some queries on `nexus-analyst-demo.acme.dim_users`. Your `last_login_date` column has a lot of nulls or dates back in 2025. 

[00:19:02] **Derek Vogt**: Exactly. If we aren't using the seats, I’m going to have a hard time justifying the renewal in July. Is there any way to drop down to the Pro tier but keep the SSO? 

[00:19:15] **Benji**: Unfortunately, no. SSO is locked to the Business and Enterprise tiers. If you move to Pro, you’d save money—$49 a seat—and there’s no 50-seat minimum, so you could just pay for the 22 people actually using it. But you’d have to manage all those passwords manually.

[00:19:35] **Derek Vogt**: Ugh. That’s a dealbreaker for IT. They won’t let us off Okta. 

[00:19:41] **Benji**: What if we looked at it from an adoption standpoint instead? I see a lot of your users are in the "Operations" role but haven't actually built a workflow yet. Maybe we can set up a training session for them? If we can get them building, the value is there. You’re already paying for the 50-seat floor anyway, so those extra seats are essentially "free" until you hit 51.

[00:20:05] **Derek Vogt**: Let me think about it. It’s either we find a way to use the seats or I have to explain to my VP why we're paying $7,450 a month for 22 active users.

---
[00:05:44] **Sarah Jenkins**: Priya, I was just looking at Verdant Cloud's instance. You guys have 42 active workflows right now, which is great. But I noticed you're still on the Pro plan.

[00:05:56] **Priya Sharma**: Yeah, it works for us. We only have 12 people on the team, so the $49/seat price is perfect. Why? Are we hitting a limit?

[00:06:05] **Sarah Jenkins**: Well, you’re not hitting a workflow limit—Pro has unlimited workflows—but I saw you guys started using the "Financial Data" connector. For SOC2 compliance, usually companies your size need the advanced audit logs that show exactly *who* changed a mapping and *when*. 

[00:06:22] **Priya Sharma**: Oh, we just had our internal audit. They did mention they wanted more visibility into the production changes. Right now I'm just looking at the `fact_user_events` table in the BigQuery export you guys gave us.

[00:06:36] **Sarah Jenkins**: That’s a good start, but the `nexus-analyst-demo.acme.fact_user_events` table on the Pro plan only keeps 7 days of history in the UI. If you move to Business, we bump that to 90 days in the UI and give you a much more granular view of the `event_type` and `payload_json`.

[00:06:55] **Priya Sharma**: How much would that cost us? 

[00:07:01] **Sarah Jenkins**: So, here’s the thing. Business has a 50-seat minimum. Even though you only have 12 users, you’d have to pay for 50 seats at $149/mo.

[00:07:11] **Priya Sharma**: Wait, so my bill would go from $588 a month to over $7,000? Just for audit logs? That's insane, Sarah.

[00:07:22] **Sarah Jenkins**: I know it sounds like a massive jump. It’s definitely a "level up" moment for our customers. Most people make the move when they either need the SSO for security or they hit the 100k run limit. How many runs are you guys doing?

[00:07:38] **Priya Sharma**: Let me check... looks like we did 8,500 last month. 

[00:07:44] **Sarah Jenkins**: Okay, so you’re close to the 10k Pro cap too. Honestly, Priya, you might be able to stay on Pro for another few months, but once you hire that next batch of engineers and those runs scale up, you'll be forced onto Business anyway. Maybe we can do a mid-market discount for the first six months to bridge the gap?

[00:08:04] **Priya Sharma**: You'd have to get that down a lot closer to my current budget for me to even bring it to my boss. Let’s see what you can do on the "introductory" pricing.

[00:08:15] **Sarah Jenkins**: Sounds fair. I'll talk to the desk. I’ll send over a follow-up with the diff on those audit logs. Talk soon, Priya.

---

**Call Date**: 2026-02-12
**Participants**: Sarah Jenkins (AE), Marcus Thorne (Harbor Dynamics)
**Subject**: Harbor Dynamics / Q1 Usage Review

[00:00:05] **Marcus Thorne**: Sorry, I’m a few minutes late. My kid had this... uh, this science project thing this morning and we realized at 7 AM that we didn't have any of the specific adhesive he needed. Absolute disaster.

[00:00:18] **Sarah Jenkins**: Oh no, the classic morning-of-school scramble. No worries at all, Marcus. I actually have a ten-year-old, so I live that life every Tuesday, it feels like. How are things over at Harbor?

[00:00:32] **Marcus Thorne**: Busy. We just finished the migration for our marketing ops stack. We’ve got most of the leads flowing through the Acme workflows now. It’s definitely smoother than what we had with Zapier.

[00:00:45] **Sarah Jenkins**: That’s what I like to hear. I was actually looking at your usage in the `nexus-analyst-demo.acme.fact_workflow_runs` table earlier this morning—our internal dashboard—and you guys are absolutely ripping through those runs. You hit 9,842 yesterday.

[00:01:03] **Marcus Thorne**: Wait, for the month? 

[00:01:05] **Sarah Jenkins**: Yeah, for the current billing cycle. You’re on the Pro plan, which caps at 10,000. 

[00:01:11] **Marcus Thorne**: (Pauses) Oh. Wow. That’s... that’s much faster than I thought. We only have like six workflows live. 

[00:01:19] **Sarah Jenkins**: It looks like that "Shopify to Slack" notification you built is firing every time there's a cart update, not just a purchase. That’s generating about 400 runs an hour. 

[00:01:31] **Marcus Thorne**: (Sighs) Okay, I need to talk to the team. But if we go over the 10k, what happens? Does the whole thing just stop?

[00:01:40] **Sarah Jenkins**: We don’t hard-kill it immediately, but you'll get a notification, and after a 48-hour grace period, the workflows pause until the next cycle or until you upgrade. Given Harbor Dynamics is looking to scale the engineering side too, we should probably talk about that jump to Business.

[00:01:58] **Marcus Thorne**: I know you mentioned Business before. Remind me of the floor on that?

[00:02:04] **Sarah Jenkins**: So, Business starts at a 50-seat minimum. It’s $149 per seat. It would give you 100,000 runs per month, which would give you a massive buffer. Plus, you’d get the SAML/SSO support. I know your IT guy, Kevin, was asking about Okta integration last month.

[00:02:22] **Marcus Thorne**: 50 seats? Sarah, we have like... eight people in the tool. Maybe ten if we count the analysts who just peek at the logs. I can’t pay for 40 empty seats. That’s a $7,500 monthly bill. We're paying like $400 right now.

[00:02:39] **Sarah Jenkins**: I hear you. The gap between Pro and Business is the biggest hurdle for our MM customers. But the infrastructure required to support those higher run volumes and the audit logging—which is in `nexus-analyst-demo.acme.fact_user_events` for the Business tier—it’s just a different class of service. 

[00:03:00] **Marcus Thorne**: Is there a "Pro Plus" or something? I don't need 100k runs. I need like 20k. Can we just pay for extra runs on the Pro plan?

[00:03:10] **Sarah Jenkins**: We don’t really do "bolt-on" runs anymore. We used to, but it became a nightmare for billing to track in `fact_subscriptions`. Honestly, Marcus, if you’re growing this fast, you’ll hit 50k runs by June. Let me see if I can get my VP to approve a "growth ramp" where we start you at 25 seats for the first quarter but give you the Business features. 

---

**Call Date**: 2026-03-05
**Participants**: David Kim (AE), Elena Rodriguez (Sable Analytics)
**Subject**: Sable Analytics - Renewal Discussion

[00:12:44] **Elena Rodriguez**: ...and that’s the main thing, David. We’re looking at the budget for Q2, and Acme is one of the highest per-user costs in our stack. 

[00:12:55] **David Kim**: I appreciate the candor, Elena. I'm looking at your account details in `nexus-analyst-demo.acme.dim_customers`. You guys have been on the Business plan for about a year now. You’re currently at 55 seats. 

[00:13:08] **Elena Rodriguez**: Right, because of the 50-seat minimum. But we only have 32 active users if you look at the `is_active` flag in the `dim_users` table. We’re essentially paying a 40% "ghost tax" just to have SSO. 

[00:13:25] **David Kim**: Well, the Business tier isn't just about the seat count, it's about the 99.9% SLA and the priority support. I saw you had a ticket last week about a webhook timeout on the "Verdant Cloud" integration—our team responded in 14 minutes. On the Pro plan, that’s a 24-hour turnaround.

[00:13:44] **Elena Rodriguez**: I know, I know. The support is great. But we’re getting pitched by Tray.io and even Make.com. Make’s pricing is based on data transfer and runs, not seats. It’s tempting.

[00:13:58] **David Kim**: I get that. But Make doesn’t give you the BigQuery sync. If you want to keep your data in `nexus-analyst-demo.acme`, you’d have to build a custom pipe for that with Make. With us, it's native. How much value are you guys getting from the `fact_workflow_runs` data? I see your BI team queries that table almost daily.

[00:14:20] **Elena Rodriguez**: They do. We use it to calculate the "cost per lead" by looking at the execution time of the enrichment steps. It’s valuable, sure. But is it $8,000-a-month valuable? 

[00:14:34] **David Kim**: Let’s look at it this way. If you dropped to Pro to save money, you’d lose the SSO. Your security team would lose their minds. And you’d be capped at 10k runs. Last month Sable did 62,000 runs. You’d hit that cap in the first five days of the month. 

[00:14:55] **Elena Rodriguez**: (Laughs) Okay, point taken. We can't go back to Pro. But can we talk about the Enterprise tier? If we commit to a 2-year deal, does that 250-seat minimum for Enterprise come down? 

[00:15:11] **David Kim**: For Enterprise, the seat minimum is pretty firm because of the dedicated CSM and the SOC2 legal overhead. But on Enterprise, we stop charging per seat in the same way—it moves to a flat platform fee plus a smaller per-user increment. If you’re planning on going to 100+ employees this year, Enterprise actually starts looking cheaper per head than Business.

---

**Call Date**: 2026-04-10
**Participants**: Sarah Jenkins (AE), Chloe Wu (Verdant Cloud)
**Subject**: Discovery - Moving off Zapier

[00:04:12] **Chloe Wu**: ...so yeah, the main problem is that we have these massive bursts. When we launch a new campaign, we might trigger 50,000 webhooks in an hour. Zapier just... it chokes. It throttles us, and we lose the payload.

[00:04:26] **Sarah Jenkins**: That’s a very common pain point for companies moving to Acme. We’re built on a more robust queueing system. In our `fact_workflow_runs` table, we track the `duration_ms` for every single step, and we don’t throttle. If you’re on the Business or Enterprise plan, we just scale the workers.

[00:04:45] **Chloe Wu**: And what about data residency? We have some customers in the EU who are very picky about where their `payload_json` is stored.

[00:04:54] **Sarah Jenkins**: We have an EMEA office in Amsterdam, and for our Enterprise customers, we can offer regional data pinning. Your metadata would still live in our main `nexus-analyst-demo.acme` warehouse for analytics, but the actual execution data stays in the EU. 

[00:05:12] **Chloe Wu**: Okay, that’s huge. Now, talk to me about pricing. I’m looking at your site, and the jump from Pro to Business is... steep. $49 to $149? And a 50-seat minimum?

[00:05:25] **Sarah Jenkins**: It is a jump. But for a company like Verdant Cloud, you're going to need the audit logs. With 50,000 runs an hour, if something breaks, you need to be able to go into `fact_user_events` and see exactly which version of the workflow was published and by whom. Pro only gives you a very basic "event happened" log. 

[00:05:46] **Chloe Wu**: I'm looking at my user list. We probably only have 15 people who would actually "build" workflows. The rest would just be "viewers." Do viewers count towards the 50-seat minimum?

[00:05:58] **Sarah Jenkins**: Currently, yes. We don't have a "free viewer" role on the Business plan. Everyone provisioned in `dim_users` for your `customer_id` counts as a seat. It's something our product team is looking at for later in 2026, but for now, it's a flat seat price.

[00:06:15] **Chloe Wu**: That’s going to be a tough sell for my CFO. We're paying Zapier about $1,200 a month right now. You're asking for over $7,000.

[00:06:25] **Sarah Jenkins**: The difference is reliability. If Zapier drops 5% of those 50k webhooks, what’s the cost to your business in lost leads?

[00:06:34] **Chloe Wu**: (Silence) ...roughly $20,000 in attributed pipeline per month.

[00:06:40] **Sarah Jenkins**: So the $6,000 difference for Acme is actually an insurance policy that pays for itself three times over. 

[00:06:48] **Chloe Wu**: (Laughs) You Sales people always have the math ready, don't you? Send me the technical specs on the BigQuery export. I want to see what the schema looks like for `fact_workflow_runs`. If my data engineers like it, we can keep talking.

[00:06:55] **Sarah Jenkins**: Done. I’ll CC your engineering lead on that. Talk soon, Chloe.

---

**Gong Call Transcript: Harbor Dynamics - Expansion Discovery**
**Date**: November 14, 2025
**Participants**: Marcus Thorne (CTO, Harbor Dynamics), James Vance (AE, Acme Inc)
**Duration**: 42:18

[00:00:12] **James Vance**: Marcus, good to see you again. How was the trip to Berlin?

[00:00:18] **Marcus Thorne**: Cold. (Laughs) Very cold. But productive. We just finished the integration with our ERP, and now we’re looking at moving all of our logistics triggers over to Acme. Right now we’re on that Pro plan—I think we have about 12 seats? 

[00:00:34] **James Vance**: Let me check the dashboard... Yeah, looking at `nexus-analyst-demo.acme.dim_customers`, you guys are at 12 seats, exactly. You’ve been hitting the 10,000 run limit pretty consistently for the last three months, though.

[00:00:48] **Marcus Thorne**: That’s the problem. We’re getting those "quota near capacity" emails every Tuesday. If we move the logistics workflows, we’re talking 80,000 runs a month, maybe 90,000. 

[00:01:02] **James Vance**: So, the jump to Business makes the most sense here. It moves your quota to 100,000 runs. Plus, for a logistics company, you’re going to want the SSO. I saw you guys use Okta?

[00:01:15] **Marcus Thorne**: We do. But James, I looked at the Business tier. It says a 50-seat minimum. We only have 12 people in the technical ops team. I can't justify paying for 38 empty seats just to get more runs and SSO. 

[00:01:30] **James Vance**: I hear that a lot. The way most of our MM—Mid-Market—customers handle this is by provisioning the "Viewers" across the broader operations team. In `dim_users`, we don't distinguish between an admin who builds the flow and a manager who just checks the `fact_workflow_runs` table to see why a shipment hasn't updated. 

[00:01:52] **Marcus Thorne**: It still feels like a tax. Is there no "Pro Plus" or something? Just let me buy more runs.

[00:02:04] **James Vance**: (Sighs) Trust me, Marcus, I’ve pushed for that in our product syncs. But the Business tier isn't just about the runs. It’s the priority support. When a logistics trigger fails at 3 AM on a Sunday, you’re not waiting for a ticket queue. You’re on the priority line. If I look at your current `fact_invoices`, you’re paying $588 a month. Business will put you at $7,450. It's a different league of service.

[00:02:35] **Marcus Thorne**: Seven grand a month. (Silence) I need to see the uptime SLA. If we’re putting our core business logic on Acme, I need more than "best effort." 

[00:02:47] **James Vance**: The Business plan guarantees 99.9%. If you need the 99.99% and a custom penalty structure, that’s when we talk Enterprise, but that starts at 250 seats.

[00:02:59] **Marcus Thorne**: No, Enterprise is too big. Let's stick to the 50-seat conversation. Can you send me a breakdown of how the audit logs work? I want to see if we can pipe those logs back into our Snowflake instance.

[00:03:12] **James Vance**: Absolutely. You can actually use our own BigQuery connector for that. It maps straight from `nexus-analyst-demo.acme.fact_user_events` to whatever destination you want. I’ll send the docs.

---

**Gong Call Transcript: Cobalt Systems - Q3 Business Review**
**Date**: February 12, 2026
**Participants**: Elena Rodriguez (Ops Director, Cobalt Systems), Jordan Lee (CSM, Acme Inc)
**Duration**: 28:05

[00:04:15] **Jordan Lee**: ...and so looking at your usage in `fact_workflow_runs`, Cobalt Systems had a 22% increase in successful executions quarter-over-quarter. Your error rate is down to 0.04%, which is fantastic.

[00:04:30] **Elena Rodriguez**: Yeah, the stability has been great. We did have one weird spike last week, though. On Feb 5th, we saw about 4,000 runs fail in a ten-minute window. Code `ERR_602`.

[00:04:45] **Jordan Lee**: Let me pull that up... Yeah, I see it here in the warehouse. Feb 5th, `error_code` 602. That usually points to a timeout on the destination API. It looks like your CRM—Salesforce—was having some latency issues that morning.

[00:05:02] **Elena Rodriguez**: Figures. It’s always Salesforce. (Laughs) While I have you, we’re looking at our seat count. We’re currently at 62 seats on the Business plan. We’re doing a bit of a reorganization, and I might need to drop that down to 45. Is that going to be an issue with our contract?

[00:05:22] **Jordan Lee**: So, the Business plan has that 50-seat floor. Even if you only have 45 active users in `dim_users`, you’ll still be billed for the 50-seat minimum. If you drop below 50, you technically don't qualify for the Business features like the audit logs and SSO.

[00:05:42] **Elena Rodriguez**: Wait, so if I delete 17 users, I still pay for 50? And if I want to pay for 45, I lose SSO?

[00:05:52] **Jordan Lee**: Exactly. It's a platform constraint for the Business tier. Most customers in your position keep the "buffer" seats for their engineering team or use them for "Service Accounts" to run specific automated jobs. 

[00:06:08] **Elena Rodriguez**: That seems... inefficient. We're an "MM" account, Jordan. We're trying to tighten the belt. What if we moved to an annual contract? Could we waive the seat minimum?

[00:06:22] **Jordan Lee**: I can talk to the Finance team, but usually the 50-seat floor is pretty firm for Business. However, if we move you to an annual "Enterprise Lite" deal—maybe around the 100-seat mark—we can do some custom pricing on the per-seat side. 

[00:06:40] **Elena Rodriguez**: Let's hold on that. I'll talk to my VP. We might just stay at 62 if it's too much of a headache to downgrade. But keep an eye on our `current_mrr_usd` in the system—if it drops, you’ll know why.

---

**Gong Call Transcript: Sable Analytics - Enterprise Discovery**
**Date**: March 03, 2026
**Participants**: David Chen (VP Eng, Sable Analytics), James Vance (AE, Acme Inc)
**Duration**: 55:20

[00:15:44] **David Chen**: The thing is, James, we’re not just a "user" of Acme. We’re planning on embedding the workflow engine into our own client-facing dashboard. Our customers will be the ones triggering the runs.

[00:16:01] **James Vance**: That’s a very different use case. That’s our "Embedded" play, which falls under the Enterprise tier. If you’re looking at `dim_plans`, you won't see it on the website. 

[00:16:14] **David Chen**: Right, because we’re going to blow past that 100,000 run limit in about three days. We’re projecting 2 million runs a month by the end of 2026.

[00:16:25] **James Vance**: For that scale, you definitely need Enterprise. It’s unlimited runs, and we give you a dedicated instance in the region of your choice. No noisy neighbors.

[00:16:38] **David Chen**: And the pricing? I know you said 250 seats is the minimum, but we don't have 250 employees. We have 40.

[00:16:48] **James Vance**: For Enterprise, the "seat" definition changes. We often treat your end-users or specific "API keys" as seats, or we just do a flat platform fee. Usually, for a company like Sable Analytics, we’re looking at an ACV—Annual Contract Value—of around $120,000. 

[00:17:10] **David Chen**: $120k. Okay. And does that include the SOC2 report and the HIPAA BAA? We have some healthcare clients.

[00:17:20] **James Vance**: Yes, Enterprise is our only tier that covers HIPAA compliance. We’d give you a dedicated CSM—probably someone like Jordan or Sarah—and we'd get our legal team to review the BAA with yours. 

[00:17:35] **David Chen**: Can we see the performance metrics for high-concurrency runs? If we hit 1,000 webhooks a second, does the `duration_ms` in `fact_workflow_runs` start to climb?

[00:17:48] **James Vance**: Our infrastructure is built on K8s and auto-scales, but I can get you a technical deep-dive with one of our engineers. We have a benchmark report for the `nexus-analyst-demo.acme` environment that shows P99 latency even at 10k concurrent triggers. I’ll send that over.

[00:18:10] **David Chen**: Great. If the tech holds up, the $120k is doable. It's cheaper than building our own orchestration engine.

---
[00:00:05] **Sarah Jenkins**: Hey Mark, good to see you again. How’s the weather in Chicago? 

[00:00:11] **Mark Thistle**: Freezing, Sarah. Absolute slush everywhere. But hey, keeps us inside and focused on the automation backlog, right?

[00:00:18] **Sarah Jenkins**: (Laughs) I guess that’s one way to look at it. I wanted to pull up the Q4 usage report for Cobalt Systems. I was looking at the `nexus-analyst-demo.acme.fact_workflow_runs` table this morning and noticed you guys hit a new peak in November.

[00:00:34] **Mark Thistle**: Yeah, we onboarded the logistics team. They’re running a bunch of webhooks every time a shipment changes status in the ERP. It’s... uh... it’s a lot more than we expected. Are we hitting the ceiling?

[00:00:47] **Sarah Jenkins**: You’re on the Business tier right now, which has that 100,000 run-per-month quota. In November, you guys hit 98,400. You’re literally right against the edge. If you go over, the platform doesn't hard-stop you immediately, but we start seeing those `error_code` entries in the logs—usually a 429 rate limit—if the concurrency gets too high.

[00:01:12] **Mark Thistle**: 429s are exactly what I’m seeing. My team was complaining that the Salesforce sync was lagging. So, what’s the move? I know you’re going to tell me to go Enterprise, but I’ve got the `dim_plans` sheet in front of me and that 250-seat minimum is a tough pill for my CFO to swallow. We only have 110 people in the whole company.

[00:01:34] **Sarah Jenkins**: I totally hear you. Most of our Mid-Market customers in the 100-200 seat range feel that gap. What I can do—and I’ll have to get James Vance or Marcus to approve this—is look at a "Growth Enterprise" bridge. We keep the seat count at 110, but we bump your ACV to $60k to cover the unlimited runs and the SOC2 support you asked for last month.

[00:01:58] **Mark Thistle**: $60k. That’s a jump from our current $19k MRR—wait, no, let me check the invoice. We’re paying $149 a seat for 110 seats... that’s like $16k a month. $190k-ish a year? 

[00:02:15] **Sarah Jenkins**: Actually, looking at `fact_subscriptions`, you're currently on a legacy Business contract at $125/seat because you signed back in '24. If we move to the current Enterprise tier, we usually standardise that. But honestly, if you stay on Business and just add seats as you grow, you’re still capped at 100k runs. It’s the run volume that’s the bottleneck for Cobalt, not the seat count.

---

[00:04:22] **James Vance**: Thanks for jumping on, Elena. I saw the note from your team about the Tray.io renewal coming up. I assume that’s why we’re talking about Harbor Dynamics moving more volume to Acme?

[00:04:35] **Elena Rodriguez**: Yeah, James. Tray is getting... expensive. Their "task" based pricing is killing us because we have these very long workflows with like 40-50 steps. Every time a step runs, the meter ticks. I saw in your docs that Acme counts a "run" as the whole execution, regardless of the `step_count` in `fact_workflow_runs`. Is that right?

[00:04:58] **James Vance**: That’s exactly right. You could have 2 steps or 200 steps; it’s one run against your quota. For Harbor Dynamics, that’s usually a massive cost saver.

[00:05:10] **Elena Rodriguez**: Okay, so we’re currently at 65 seats on the Business tier. We’re doing about 80k runs. If we migrate the marketing ops stuff from Tray, we’re going to add another 150k runs a month. 

[00:05:25] **James Vance**: So you'll be at 230k total. You’re definitely in Enterprise territory. The Business tier maxes out at 100k. 

[00:05:35] **Elena Rodriguez**: Can’t we just buy "run packs"? Zapier lets us just buy more tasks without moving to a whole new contract tier.

[00:05:45] **James Vance**: We’ve talked about adding that to `dim_plans` for 2026, but right now, the infrastructure cost for those high-volume tenants requires us to move you to a dedicated cluster. That’s why we bundle it into Enterprise. Plus, you’d get the Audit Logs, which I know your IT Director, Simon, was asking about during the last security review.

[00:06:05] **Elena Rodriguez**: Simon is a stickler for the logs. If I can show him the `fact_user_events` dashboard where he can see exactly who modified which workflow, he might actually stop breathing down my neck. What does the contract look like for 65 seats on Enterprise? I know you say 250 is the min.

[00:06:22] **James Vance**: We’d do a "Platform Fee" model. Instead of a per-seat price, we just say Harbor Dynamics pays $75k a year. You get up to 250 seats included, and unlimited runs. It simplifies the billing for your finance team—one invoice, once a year.

---

[00:11:05] **Marcus Thorne**: ...and that’s how the Slack integration handles the threading. Liam, any thoughts on how Verdant Cloud would use that for the incident response triggers?

[00:11:16] **Liam O'Brien**: It looks solid. My main concern is the "Pro" versus "Business" distinction. We’re a startup. We have 12 people. We don't need 50 seats. But I *do* need the SSO. Why is SSO gated behind 50 seats?

[00:11:34] **Marcus Thorne**: I get that feedback a lot. It’s a common point of friction in our `dim_plans` structure. The Business tier at $149/seat is where we introduce the "Enterprise-ready" features like SAML/SSO and the 100k run quota. For a 12-person team at Verdant, I know the 50-seat minimum feels like a jump.

[00:11:55] **Liam O'Brien**: It's more than a jump, Marcus. It's a cliff. 12 seats on Pro is $588 a month. 50 seats on Business—even if I only use 12—is $7,450 a month. That’s a 12x price increase just to get Okta integration. Can we talk about a waiver?

[00:12:15] **Marcus Thorne**: I can't waive the seat minimum, but what I can do for smaller high-growth companies like Verdant is look at a multi-year ramp. We could start you at a lower "Year 1" rate while you're still sub-20 employees, provided we have a commitment to scale. Also, have you looked at the `duration_ms` on your current scripts? If you're running heavy Python jobs, the Business tier gives you more compute priority. 

[00:12:40] **Liam O'Brien**: We’re mostly just hitting APIs. Latency isn't the issue; it’s the security compliance. I have a meeting with our CTO tomorrow. If I tell him we’re paying for 38 "ghost seats" just to get SSO, he’s going to tell me to just use Make.com or keep it in-house. 

[00:12:58] **Marcus Thorne**: Tell him to look at the `fact_workflow_runs` error rates for Make versus Acme. Our P99 reliability in the `nexus-analyst-demo.acme` environment is 99.99%. Make struggles when you hit high concurrency on the same webhook. I’ll send over the comparison whitepaper. 

[00:13:15] **Liam O'Brien**: Send it over. But seriously, look into that SSO pricing. It’s a dealbreaker for a lot of Series A shops.

---

[00:22:10] **James Vance**: David, I checked with the Eng team about those `duration_ms` spikes you were worried about for Sable Analytics. 

[00:22:18] **David Chen**: And? Was I right?

[00:22:21] **James Vance**: Sort of. In the standard multi-tenant environment—the one that `dim_customers` on the Pro/Business plans use—we did see a slight P95 climb when a "noisy neighbor" was running a massive bulk import. But for Enterprise customers, we put you on your own K8s namespace. I pulled the logs from a similar account—another data-heavy SaaS—and their average `duration_ms` stayed flat at 145ms even during their peak 2M run spikes.

[00:22:52] **David Chen**: That’s what I needed to hear. Now, about the HIPAA BAA. Does Sarah—is she the CSM?—does she handle the implementation of the data masking? We can't have PII hitting the Acme logs.

[00:23:05] **James Vance**: Sarah Jenkins or Jordan would be your primary. They’ll walk you through the "Log Masking" feature which is exclusive to Enterprise. You can define regex patterns in the UI, and Acme will scrub anything that looks like an SSN or a patient ID before it ever hits our internal `fact_user_events` or BQ warehouse. 

[00:23:25] **David Chen**: Perfect. Send over the $120k paperwork. I’ll get our legal team to start the BAA review. We want to be live by July 1st. 

[00:23:35] **James Vance**: Glad to hear it, David. I’ll get the contract out by EOD. Welcome to the Acme family.

---
[00:01:15] **Internal Note (James Vance)**: Sable Analytics is a massive win for the Ent team. We need to make sure the `dim_customers` record is updated the second the signature drops. They're going to be our flagship for the "Embedded" use case. I need to make sure the `ae_employee_id` is correctly mapped for the Q3 commission cycle. Current MRR should reflect the full $10k/mo.

[00:04:12] **Sarah Jenkins**: Marcus, glad we could jump on. I was looking at the usage dashboard for Cobalt Systems this morning in our `nexus-analyst-demo.acme.fact_workflow_runs` table, and you guys are absolutely crushing it. I saw a spike of 85,000 runs just last Tuesday.

[00:04:28] **Marcus Thorne**: Yeah, tell me about it. We hooked up the Jira-to-Slack-to-Notion bridge for the entire dev org. It’s... uh... it's a lot noisier than we expected. Honestly, Sarah, I’m getting paged because the Business plan notifications say we’re hitting 90% of our 100k monthly quota. We’ve still got ten days left in the month.

[00:04:45] **Sarah Jenkins**: I saw that. You’re currently on the Business tier at $149 a seat, right? With 110 seats licensed?

[00:04:52] **Marcus Thorne**: Exactly. But here’s the thing—the team wants to roll this out to the EMEA marketing group next month. That’s another 150 people. If I add them, I’m over the 250-seat threshold for Enterprise anyway. Does that automatically bump us to "Unlimited Runs"? Because paying for overages on the Business plan feels like... well, it’s a budget killer.

[00:05:11] **Sarah Jenkins**: It does. Once you move to the Enterprise tier, we waive the `workflow_run_quota_per_month`. It’s essentially "all you can eat" within reasonable infrastructure limits. Plus, you get the full SOC2 audit logs. I noticed your security lead, Kevin, was asking about the `fact_user_events` granularity last month. Enterprise gives you 2-year retention on those logs, whereas Business caps at 90 days.

[00:05:35] **Marcus Thorne**: 90 days is definitely too short for our compliance guys. But what’s the damage? James mentioned a $50k floor for Enterprise last year. Is that still the case?

[00:05:46] **Sarah Jenkins**: The entry point for Enterprise usually starts around $50k ACV, but with 260 seats, you’re already looking at a base that puts you right in that ballpark. I’ll have James Vance draft a proposal. We can probably look at a multi-year to flatten the seat-growth cost. How does that sound?

[00:06:02] **Marcus Thorne**: Just... just make it make sense, Sarah. We’re currently looking at Tray.io too, and their pricing is all based on "connectors" not seats. It’s a different beast, but my CFO likes the predictability.

---

[00:11:05] **James Vance**: Elena, thanks for joining. I know you’re evaluating us alongside Zapier and Make. How’s the sandbox feeling?

[00:11:13] **Elena Rodriguez (Harbor Dynamics)**: It’s powerful. The Python step in the workflow is a game changer for us. Zapier’s "Code" step always felt a bit... throttled? But I’m looking at the `dim_plans` sheet you sent over. We’re a 400-person shop. If I’m reading this right, we *have* to be on Enterprise? 

[00:11:32] **James Vance**: For a team of 400, yes. Our Business tier caps at 250 seats. For an organization of Harbor’s scale, you’re going to want the SSO integration—OIDC and SAML—and the dedicated K8s namespace we discussed. 

[00:11:47] **Elena Rodriguez**: Right, the SSO. That’s non-negotiable. But what about the migration? We have about 300 "Zaps" currently. Does Acme have an automated importer, or are we rebuilding from scratch?

[00:11:59] **James Vance**: We don't have a 1:1 "importer" because our logic handling—the way we handle branching and loops—is a bit more robust than Zapier’s. However, for Enterprise customers, we include 20 hours of "Solutions Architecture" time. We’ll actually have someone like Jordan from our CS team sit down and help map your top 50 high-volume workflows into Acme.

[00:12:22] **Elena Rodriguez**: And the data residency? We saw some stuff in the news about your EMEA office in Amsterdam. Can we pin our data to the EU?

[00:12:31] **James Vance**: Absolutely. That’s an Enterprise-only configuration. We can ensure all your `fact_workflow_runs` and metadata stay in our Frankfurt region. It’s a toggle on our end. I’ll make sure that’s in the MSA. 

---

[00:08:42] **Jordan Smith**: Chloe, I’m looking at the Verdant Cloud account. You’ve been on the Pro plan since 2024, but your `current_mrr_usd` is starting to fluctuate because of those seat additions. You’re at 48 seats now.

[00:08:55] **Chloe Miller**: Yeah, we’ve been adding folks one by one. It’s just easier than doing a big "Business" contract. $49 a seat is easy for me to approve on the corporate card.

[00:09:05] **Jordan Smith**: I totally get that. The "self-serve" Pro plan is great for flexibility. But I have to give you a heads-up—once you hit 50 seats, the system is going to flag the account for a mandatory transition to the Business tier. It’s part of our `dim_plans` logic for the MM (Mid-Market) segment.

[00:09:22] **Chloe Miller**: Wait, what? $149 a seat? Jordan, that’s a 3x jump. I can’t put that on a card. Why the jump?

[00:09:30] **Jordan Smith**: It’s the features that come with it, Chloe. At 50 seats, you’re usually dealing with more complex cross-departmental workflows. You get the SAML SSO, which I know your IT guy, Steve, was asking about in the support logs. Plus, the run quota goes from 10k to 100k. Looking at your `fact_workflow_runs` from April, you actually hit 12,000 runs. We didn't throttle you last month as a courtesy, but on the Pro plan, those overages usually start kicking in.

[00:09:58] **Chloe Miller**: (Sighs) I hate the "seat tax." Can we just stay on Pro and pay for the extra runs?

[00:10:05] **Jordan Smith**: I wish I could, but the 50-seat ceiling is hard-coded in our `nexus-analyst-demo.acme.dim_plans` table. Tell you what—if we move you to an annual Business contract today, I can talk to my manager about a "growth discount" for the first year to bridge the gap. We can probably get it down to $110/seat for the first 12 months. 

[00:10:25] **Chloe Miller**: Let me talk to Steve. He really wants that SSO, so that might be my leverage. Send me the comparison PDF again? The one that shows the "Audit Log" vs the "Pro" history?

[00:10:37] **Jordan Smith**: Sending it now. And Chloe, just a heads up, the Business plan also gives you "Priority Support." No more 24-hour waits on tickets. You’ll be in the 4-hour queue.

---

[00:02:15] **Internal Note (Jordan Smith)**: Verdant Cloud is resisting the $149 jump. They are currently at 48 seats in `dim_customers`. If they add two more, the automated "Upgrade Required" banner will trigger in their UI. I need to be proactive here or they might look at Make.com. Their `acquisition_channel` was "Organic Search," so they don't have a deep relationship with an AE yet. James, can you take a look?

---

[00:15:20] **James Vance**: David, one last thing for the Sable Analytics implementation. We were looking at your `step_count` in the test environment. You're averaging 45 steps per workflow. That’s... intense. 

[00:15:33] **David Chen**: We’re doing complex data transformation before pushing to our Snowflake instance. Is that going to be a problem for the `duration_ms`?

[00:15:40] **James Vance**: Not a problem, but it will impact how we look at your "Compute Units" if we ever move to the new 2026 pricing model. For now, since you’re on the Enterprise flat-rate, just keep an eye on the `error_code` column in your logs. If you see a lot of `504` errors, it means your Snowflake warehouse isn't acknowledging the `POST` fast enough. Our timeout is 30 seconds.

[00:16:02] **David Chen**: Good to know. We’ll tune the Snowflake ingestion. July 1st is still the target. See you then.

---

[00:00:12] **James Vance**: ...sorry, just getting my screen shared. Can you see the dashboard yet, Sarah? It’s been a bit laggy this morning.

[00:00:24] **Sarah Jenkins**: Yeah, I see it. Is that the Cobalt Systems usage data from the last quarter?

[00:00:30] **James Vance**: Exactly. We're looking at your `nexus-analyst-demo.acme.fact_workflow_runs` table for the Feb-April window. You guys averaged about 92,000 runs a month. 

[00:00:41] **Sarah Jenkins**: Which is why I’m getting these "Near Limit" emails every Tuesday. We’re on the Business plan, right? The 100k quota?

[00:00:48] **James Vance**: Spot on. You’re at 92% capacity. And honestly, Sarah, looking at your `step_count`—you guys have some workflows that are 80+ steps. If one of those loops, you’re going to blow through that remaining 8k in an afternoon.

[00:01:05] **Sarah Jenkins**: [Laughs] Yeah, that was the Marketo sync issue we had last month. Look, I’ll be blunt. I looked at the `dim_plans` table on your docs page. To go from Business at $149 a seat to Enterprise just to get unlimited runs... that’s a massive jump for a team of 60. We aren't at the 250-seat Enterprise minimum.

[00:01:28] **James Vance**: I hear you. The 250-seat floor is standard for Enterprise, but since your `current_mrr_usd` is already quite high due to the seat count, I can talk to Finance about a "Performance Add-on." It’s basically a way to stay on Business but buy another 500k runs. It’s cheaper than the full Enterprise jump, though you wouldn't get the dedicated CSM or the custom SLA.

[00:01:55] **Sarah Jenkins**: Send me the numbers. But keep in mind, my Boss is looking at Tray.io too. They price differently. If we stay, I need that `error_code` 429 issue fixed. Our devs are seeing too many rate limits on the Jira connector.

---

[00:05:14] **Jordan Smith**: ...and that’s why the "Audit Log" is restricted to the Business tier. It’s not just about seeing who deleted a workflow; it’s about the `event_id` tracking in `fact_user_events` for SOC2 compliance.

[00:05:30] **Marcus Thorne (Harbor Dynamics)**: Jordan, we’re a 12-person startup. I love the tool, but $149/seat is $1,800 a month. Zapier’s Team plan is way under that. 

[00:05:43] **Jordan Smith**: I totally get the price sensitivity, Marcus. But Zapier doesn't give you the BigQuery direct write. If you look at your `nexus-analyst-demo.acme.fact_workflow_runs` from your trial, you're pushing directly to your warehouse. Zapier requires a third-party bridge for that or a very expensive "Company" plan anyway. Plus, your `average_duration_ms` is under 400ms here—we're way faster.

[00:06:05] **Marcus Thorne**: [Sighs] The speed is why we're here. We had some latency issues with Make.com when we were doing the real-time Slack triggers. But the 10k run limit on your Pro plan ($49/seat) is just... it's too low. We're already at 8k runs and it's only the 15th of the month.

[00:06:22] **Jordan Smith**: What if we did a one-time "Early Stage" waiver? If you commit to an annual Pro plan today, I can bump your `workflow_run_quota_per_month` to 25k for the first year. It’s a manual override in `dim_customers`, but I can get it approved because your `acquisition_channel` was a direct referral from one of our Series B investors.

[00:06:45] **Marcus Thorne**: 25k runs for $49 a seat? If you can get that in writing by Friday, we'll sign. I need to make sure the SSO is included though.

[00:06:55] **Jordan Smith**: Ah, SSO is the sticking point. That’s strictly Business tier. If you need SSO, we have to look at the $149/seat. No way around it—it’s hard-coded into the `dim_plans` logic for security reasons.

---

[00:22:10] **Internal Note (James Vance)**: Cobalt Systems (Sarah) is definitely shopping. She mentioned Tray by name. Their `customer_id` is 4421. I checked their `fact_invoices` and they haven't missed a payment since 2024, but their `status` is currently "At Risk" in my personal tracker because of the run quota ceiling. We need to decide if we waive the 250-seat Enterprise minimum to keep them from churning to a competitor. 

---

[00:03:45] **James Vance**: David, I was just reviewing the Sable Analytics migration plan. You're moving 400 users over from your legacy system on June 15th?

[00:04:02] **David Chen**: That’s the goal. We’re currently at 285 in `dim_users`, so it’s a big jump. We’ve been testing the `invited_by_user_id` flow to make sure the onboarding emails don't hit the spam folders.

[00:04:15] **James Vance**: Good call. I saw some `error_code` 500s in your logs yesterday around 4:00 PM PST. Was that you guys testing the bulk API?

[00:04:22] **David Chen**: Yeah, we tried to hit the `workflow_id` 9901 with about 500 concurrent requests. It didn't love that.

[00:04:30] **James Vance**: [Laughs] Yeah, the `nexus-analyst-demo.acme.fact_workflow_runs` table shows a massive spike there. You hit the concurrency limit for the Enterprise dev environment. When you go live on the 1st, we’ll move you to the dedicated cluster we discussed. Your `sla_uptime_pct` in `dim_plans` is 99.99%, but that only kicks in once you're out of the sandbox.

[00:04:55] **David Chen**: Perfect. And remind me, does the "Audit Log" cover the `triggered_by` column in `fact_workflow_runs`? We need to be able to trace every execution back to a specific `user_id` for our internal compliance.

[00:05:08] **James Vance**: It does. You'll see the full mapping between `run_id` and `user_id` in the Business and Enterprise exports. I’ll send over the updated schema for the 2026 data model so your data team can prep the Snowflake connectors.

---

[00:11:02] **Jordan Smith**: Chloe, I’m looking at Verdant Cloud’s seat count. You guys just added 3 more people this morning?

[00:11:10] **Chloe Miller**: Yeah, we hired a new SDR team in London. They need access to the HubSpot-to-Slack automation.

[00:11:18] **Jordan Smith**: That puts you at 51 seats. You just crossed the threshold for the Business plan. 

[00:11:25] **Chloe Miller**: Wait, does that mean our bill is about to triple? We were paying $49 per seat.

[00:11:32] **Jordan Smith**: Technically, yes. Per `dim_plans`, the Business tier starts at 50 seats at $149/mo. However, since you were already a "Pro" customer, I can give you a "Legacy Credit" for the remainder of the quarter. But starting July 1st, we’ll need to move the whole account to the Business tier.

[00:11:55] **Chloe Miller**: Jordan, that's a huge jump. We went from $2,500/mo to $7,600/mo just because we hired three people? There’s got to be a middle ground.

[00:12:05] **Jordan Smith**: Let’s look at the value, Chloe. You’re now getting the SSO and the Priority Support. Your `average_duration_ms` for those HubSpot workflows is critical—if they fail, your SDRs don't get leads. With Priority Support, you're not waiting a day for a fix. Also, look at your `fact_workflow_runs`. You’re at 95k runs. You would have hit the Pro cap of 10k weeks ago if we hadn't already grandfathered you into the higher limit during the trial. You're essentially using a Business-level service already.

[00:12:35] **Chloe Miller**: I need to take this to Steve. He’s going to freak out about the MRR jump. Can you at least pull a report showing our `error_code` success rate? I need to prove the tool is reliable enough to justify $90k a year.

[00:12:50] **Jordan Smith**: I'll pull the `fact_workflow_runs` summary for Q1 2026 right now. You’re at a 99.8% success rate. I'll email it over.

---

[00:08:45] **Unknown Caller**: ...and does Acme support Python scripts within the steps?

[00:08:50] **James Vance**: We do! It’s called "Cloud Functions." It’s available on Pro and above. Each function execution counts as one "step" in your `step_count`. We use a sandboxed environment, so the `duration_ms` is usually a bit higher than a standard connector—maybe 1200ms vs 200ms.

[00:09:10] **Unknown Caller**: And how do you handle secrets? Like API keys?

[00:09:15] **James Vance**: Great question. For Enterprise customers like you’re considering, we have an "Encrypted Vault." It’s not stored in our standard `dim_customers` or metadata tables; it’s a separate KMS-backed store. If you look at our SOC2 report, we detail the whole encryption-at-rest process.

[00:09:33] **Unknown Caller**: Okay, and if we have 300 users, what’s the discount?

[00:09:38] **James Vance**: For 300 seats, you’re looking at Enterprise territory. We’d move away from the $149 list price and do a custom ACV. Usually, for that volume, we’re looking at around $115–$120 per seat, depending on the contract length. If you go 3-year, I can probably get you closer to $100. That would be reflected in your `fact_subscriptions` table as a "Multi-Year Enterprise" plan.

---

[00:03:12] **Michael Chen**: ...just making sure you can see the screen. I’ve got the architecture diagram up for the Harbor Dynamics migration.

[00:03:18] **Sarah Lavoie**: Yeah, it’s coming through now. Little blurry, but I see it. So, coming from Tray, the biggest headache we have is how they handle nested loops in their credits. If I have a workflow that iterates over 500 Shopify orders, that’s 500 "tasks" or whatever. How does Acme count that in `fact_workflow_runs`?

[00:03:35] **Michael Chen**: Great question. We’re much simpler. We count the *trigger*. One execution of the workflow equals one row in `fact_workflow_runs`. It doesn’t matter if you have five steps or fifty inside that run. The only thing that changes is the `duration_ms` and potentially the `step_count` column for your own reporting. We don't penalize you for complex logic.

[00:03:55] **Sarah Lavoie**: That’s huge. We were burning through our Tray tier every three weeks. Now, for the Enterprise level, you mentioned the "Dedicated Worker" option. Is that reflected in the `sla_uptime_pct`?

[00:04:10] **Michael Chen**: Exactly. On the Business tier, you’re looking at a 99.9% SLA, which is standard. For Harbor Dynamics, given the volume you’re projecting—I think your RFP said 2.5 million runs a month?—we’d put you on Enterprise. That moves the SLA to 99.99% and gives you a dedicated processing queue. In the `nexus-analyst-demo.acme.dim_plans` table, you’d see that listed as `plan_tier = 'Enterprise'`.

[00:04:35] **Sarah Lavoie**: Okay, and what about the seats? We have about 60 people in Ops who need to build, but maybe 300 who just need to view the logs to see why a shipment failed. Do I have to pay $149 for a "viewer"?

[00:04:50] **Michael Chen**: On Business, yes, seats are seats. But on Enterprise, we can do a "Platform License." We’d likely price you based on a core group of 75 "Builders" and give you unlimited "Viewers" for a flat ACV. Usually, for a company your size, we're looking at a $120k floor.

---

[00:15:20] **Elena Rodriguez**: [Noise: Dog barking in background] Sorry about that, Maverick is very excited about the mailman. Anyway, David, I was looking at Cobalt Systems’ usage in `fact_workflow_runs` for April 2026. You guys hit 108,000 runs last month.

[00:15:38] **David Vane**: Yeah, we noticed. I got the automated notification that we were over the 100k Business limit. Is that going to trigger an overage charge on the next invoice?

[00:15:48] **Elena Rodriguez**: Not yet. We usually give a one-month grace period for Business customers. But since you’ve been over 100k for three months straight, the system is going to flag you for a "Plan True-up." If you look at `dim_customers`, your `account_tier` is still marked as 'MM' (Mid-Market), but your usage is screaming Enterprise.

[00:16:10] **David Vane**: We’re still trying to consolidate the EMEA team. If they join our instance, we’ll probably add another 40 seats. If we do that, can we stay on the Business pricing of $149 but just bump the run limit?

[00:16:22] **Elena Rodriguez**: Honestly, David, if you're adding 40 seats on top of your current 60, you're at 100 seats. At that point, the jump to Enterprise is actually cheaper because of the volume discount on the per-seat price. Plus, you’d get the Audit Logs. I saw your security team was asking about `fact_user_events` access last week—you only get that via API on Enterprise.

[00:16:45] **David Vane**: Send me a side-by-side. I need to show the CFO why spending more on the "sticker price" for Enterprise saves us money on the "overage" side. Also, can you check why we had so many `error_code = 'ECONNRESET'` last Tuesday?

[00:17:02] **Elena Rodriguez**: I’ll pull the log. It looks like it was a timeout on the Salesforce side, but let me check the `duration_ms` in our warehouse. If it’s over 30,000ms, our gateway kills the connection.

---

[00:22:05] **Marcus Thorne**: ...and that’s why we have the 50-seat minimum for the Business tier. It’s really about the level of support and the underlying infrastructure we provision.

[00:22:15] **Linda Wu (Verdant Cloud)**: Marcus, I hear you, but Verdant only has 38 people in the whole company. I can't justify paying for 50 seats. That’s $1,800 a month in "ghost seats." We’re on the Pro plan now, paying for 38 seats at $49, which is fine, but we *need* SSO. My IT director won't let us scale without Okta integration.

[00:22:38] **Marcus Thorne**: I totally get the "SAML Tax" frustration. We’ve talked to Product about moving SSO down to Pro, but right now it’s a hard gate for the Business tier in `dim_plans`. 

[00:22:50] **Linda Wu**: Can we do a compromise? What if we sign a 2-year deal for the 38 seats but pay a slightly higher per-seat price? Like $75 instead of $49, but we get the Business features?

[00:23:03] **Marcus Thorne**: I’d have to get VP approval for a "Custom Pro" SKU. Usually, Finance hates that because it makes the `fact_subscriptions` table a mess for the RevOps team. Let me see if I can "Shadow-Provision" the 50 seats but give you a 25% discount on the total ACV. That brings the effective cost down, and it keeps you on the standard Business contract.

[00:23:25] **Linda Wu**: If you can get the total annual under $60k, I can sign that by Friday. Otherwise, we might have to stay on Zapier and just deal with the security headaches for another quarter.

[00:23:38] **Marcus Thorne**: Let me run the numbers. If I look at your `fact_workflow_runs`, you guys are only at 8k runs a month. You’re nowhere near the 100k limit, so I’m really just selling you the SSO and the `priority_support`. Let me talk to my manager.

---

[00:05:10] **James Vance**: [Static] ...hello? Can you hear me now?

[00:05:15] **Unknown Caller (Sable Analytics)**: Yes, you're back. We were talking about the Python environment.

[00:05:20] **James Vance**: Right. So, for Sable Analytics, the Cloud Functions are key. In the `fact_workflow_runs` table, you’ll see a column for `step_count`. If you’re running a script that does a lot of heavy lifting, it still only shows up as one step if it’s in one Function block. We don't charge by the line of code.

[00:05:40] **Unknown Caller**: And the libraries? Can we import `pandas` or `numpy`?

[00:05:45] **James Vance**: `pandas` is included in the standard runtime. For more obscure stuff, that’s an Enterprise feature where we can build a custom Docker image for your executors. On the Business plan, you’re limited to our standard `requirements.txt`.

[00:06:00] **Unknown Caller**: Okay. Last thing—we’re seeing a lot of churn in our own customer base, so we might need to scale *down* our seats in six months. Does the Acme contract allow for seat reductions?

[00:06:12] **James Vance**: Our standard terms are "Add-only" during the term, but you can decrease at renewal. However, if you're on the Enterprise plan, we usually set a "floor." If you look at `fact_subscriptions`, we track the `change_type`. If it’s a 'Downgrade', it usually triggers a review from our Finance lead, Sarah Jenkins. We can bake in a 10% flexibility clause if you’re worried about the headcount.

[00:01:12] **Marcus Thorne**: ...sorry, I think the coffee machine just exploded in the background. Can you hear me okay now?

[00:01:20] **Tom H. (Cobalt Systems)**: Yeah, you’re good. So, looking at the dashboard we built in Snowflake—wait, no, we’re actually pulling the raw data from your `nexus-analyst-demo.acme.fact_workflow_runs` table directly—we’re seeing a spike in `error_code` '504' on the Shopify-to-NetSuite connector. Is that on your end or ours?

[00:01:45] **Marcus Thorne**: I saw that too. Our engineering team, specifically the folks monitoring the `fact_workflow_runs` FLAT table, mentioned there was a rate limit hit on the Shopify API side last Tuesday. It’s not an Acme infrastructure fail, but your `step_count` on those specific workflows is hitting 45+ steps per run. That’s a lot of sequential API calls.

[00:02:10] **Tom H. (Cobalt Systems)**: Right. We’re trying to consolidate. But since we’re on the Business plan, we’re mostly worried about that 100k run limit. If we hit 101k, do you just shut us off? Because if the NetSuite sync dies, our CFO loses it.

[00:02:25] **Marcus Thorne**: No, no. We don't hard-kill the workflows. There's a 10% buffer. But if you're consistently over, Sarah Jenkins in Finance usually flags it for a "True-up" or we talk about moving you to Enterprise. On Enterprise, we just stop counting the runs entirely. But you’d need to move from 60 seats to 250 to hit that minimum.

---

[00:12:45] **Elena Rodriguez**: [Coughing] Excuse me, allergies are killing me today in Amsterdam. Let’s look at the Harbor Dynamics account. You guys have been on the Pro plan since February 2025, right?

[00:13:02] **Derek (Harbor Dynamics)**: Yeah, about then. We’ve got 32 people using it daily. The issue is our security team is breathing down our necks about SSO. I saw it’s only on the Business tier.

[00:13:15] **Elena Rodriguez**: That’s correct. SSO, the full audit logs in `dim_users`, and priority support start at the Business tier. 

[00:13:22] **Derek (Harbor Dynamics)**: Okay, but the Business tier says there's a 50-seat minimum. We only have 32 people who actually *need* to build workflows. I can't justify paying for 18 empty seats just to get Okta integration. Can we waive the minimum?

[00:13:40] **Elena Rodriguez**: I wish I could. The 50-seat floor is pretty firm because of the support overhead for Business-class SLAs. If you look at `nexus-analyst-demo.acme.dim_plans`, you’ll see the `monthly_price_per_seat_usd` jumps to $149. Most teams in your position just treat those extra seats as "growth capacity" for the year. It's still cheaper than the security breach risk of shared passwords, right?

[00:13:58] **Derek (Harbor Dynamics)**: [Sigh] It’s a tough sell. Zapier let us stay on their Team plan without a seat floor, but their logic is so limited compared to your Python blocks. Let me talk to my VP.

---

[00:44:10] **James Vance**: ...and that’s why the `fact_subscriptions` table shows a `change_type` of 'Upsell' for Verdant Cloud. They added 40 seats mid-cycle.

[00:44:22] **Unknown Caller (Verdant Cloud)**: James, sorry to interrupt. We're actually seeing some weirdness in the `last_login_date` in `dim_users`. We have about 10 users who show as active but haven't logged in since November 2025. 

[00:44:40] **James Vance**: That might be because they’re "Service Accounts." If they’re just owning a workflow via an API key, they don't trigger a web UI login. We still count them as a provisioned seat if they’re `is_active = TRUE`. 

[00:44:55] **Unknown Caller**: Got it. Also, on the SOC2 report—we need the 2026 Bridge Letter before we can sign the Enterprise expansion. Our legal team is being... well, legal.

[00:45:10] **James Vance**: I’ll ping the security team. Usually, we keep those in the shared folder. Since you're looking at a $120k ACV for the Enterprise move, I can probably get our CTO to hop on a quick 15-minute security review if that helps clear the path. We’re aiming for a June 1st `start_date` in the `fact_subscriptions` record if we can get signatures by Friday.

---

[00:08:22] **Marcus Thorne**: Quick check-in on the Sable Analytics trial. How are the `step_count` metrics looking?

[00:08:30] **Sable Analytics Dev**: The platform is fast. Much faster than Make.com for the heavy JSON transformations. We’re averaging 400ms in `duration_ms` on the `fact_workflow_runs` table, which is great. Our main concern is the `acquisition_channel`. We were told we’d get a discount because we came through the AWS Marketplace partnership?

[00:08:50] **Marcus Thorne**: Ah, let me check the `dim_customers` record for you guys. Yeah, I see `acquisition_channel` is marked as 'Partner_Referral'. Usually, that gives you a 15% discount on the first year, but it locks you into the Business tier pricing for seats—no further negotiation on the $149.

[00:09:12] **Sable Analytics Dev**: That works. We’re at 48 users anyway, so hitting the 50-seat minimum for Business is only a two-seat difference. We’ll just hire two more people by the time the contract starts. [Laughs]

[00:09:25] **Marcus Thorne**: That’s the spirit. I’ll send over the Order Form. It’ll show up as a `subscription_id` with a `billing_cycle` of 'Annual'. We don't do monthly billing for the Business tier unless there's a significant 20% uplift.

[00:09:40] **Sable Analytics Dev**: Annual is fine. We’ve got the budget allocated from the Q1 '26 spend. Just make sure the `plan_tier` is explicitly 'Business' so our internal auditors don't think we’re on the 'Pro' self-serve stuff.

[00:09:55] **Marcus Thorne**: Done. I'll make sure Sarah Jenkins CCs you on the invoice. It'll come from our Amsterdam billing entity, just FYI.

---

[00:10:42] **James Vance**: Can you hear me now? Sorry, my AirPods decided to connect to my iPad in the other room.

[00:10:48] **Priya Sharma (Cobalt Systems)**: All good, James. We were just looking at the `fact_workflow_runs` report you sent over. Is it normal for the `step_count` to spike like that during our end-of-month batch processing? We hit about 85,000 runs last Tuesday.

[00:11:05] **James Vance**: That’s actually a great sign of adoption. You guys are currently on the Business tier, which has that 100,000 runs per month quota in the `dim_plans` table. If you keep scaling at this rate—I think I saw your team added 12 more users in the `dim_users` table just this week—you’re going to blow past that by mid-month.

[00:11:24] **Priya Sharma (Cobalt Systems)**: That’s what I’m worried about. Our CTO is asking about the Enterprise move. He saw the 'SOC2' and 'custom SLA' flags in the `dim_plans` documentation. But we’re only at 180 seats. Don’t we need 250 for Enterprise?

[00:11:41] **James Vance**: Usually, yeah. The `min_seats` for Enterprise is hard-coded at 250 in the backend logic, but for Cobalt, I can talk to my VP. If we commit to a $150k ACV, we can "paper" you at 250 seats even if you only have 180 provisioned today in `seat_count_licensed`. It gives you room to grow without the per-seat friction. 

[00:12:05] **Priya Sharma (Cobalt Systems)**: Let’s look at the numbers. If we stay on Business, we’re paying $149 per seat. 180 seats is... what, $26k a month? $320k a year? Wait, why would Enterprise be cheaper if the seat count is higher?

[00:12:22] **James Vance**: It’s not necessarily cheaper, but the `workflow_run_quota_per_month` becomes 'Unlimited'. You also get the dedicated CSM. Right now, you’re just in the pool. Plus, once you hit Enterprise, your `account_tier` flips from 'MM' to 'ENT' in our `dim_customers` table, which triggers the priority support routing. No more waiting 4 hours for a response on a `failed` run status.

---

[00:04:12] **Marcus Thorne**: Greg, I’m looking at the `fact_user_events` for Harbor Dynamics. It looks like you guys are trying to set up a SAML integration, but it keeps throwing an error.

[00:04:25] **Greg Miller (Harbor Dynamics)**: Yeah, we spent three hours on it yesterday. It keeps saying 'Feature Locked'. We’re on the Pro plan, and the docs said Pro had unlimited workflows.

[00:04:35] **Marcus Thorne**: Ah, that’s the catch. Pro has unlimited workflows, but it doesn't have SSO or the Audit Log. If you check `dim_plans`, those are strictly Business tier features. You need to be on the $149/seat tier for SAML.

[00:04:52] **Greg Miller (Harbor Dynamics)**: $149? Marcus, we’re a team of 12 people. Zapier lets us do SSO on their Team plan for way less than that. If I have to tell my boss we’re jumping from $49 to $149 just for a login button, he’s going to tell me to move everything back to Make.com.

[00:05:10] **Marcus Thorne**: I hear you. The jump is steep because of that 50-seat minimum. Our `current_plan_tier` logic is pretty rigid for Business. However, since you’re currently seeing a high `duration_ms` on those complex JSON transforms—I think I saw some hitting 2000ms—moving to Business actually puts you on a faster execution cluster. 

[00:05:32] **Greg Miller (Harbor Dynamics)**: Faster cluster? Is that in the `fact_workflow_runs` data?

[00:05:38] **Marcus Thorne**: It’s not explicitly in the FLAT table, but you’ll see the `duration_ms` drop by about 30% because you aren't sharing the multi-tenant workers with the Free tier users. Tell you what—I can’t waive the 50-seat minimum, but I can give you a 3-month "on-ramp" where we bill you for 20 seats but give you the Business features. Sarah Jenkins in Finance would have to manually override the `mrr_usd` in `fact_subscriptions`, but I think I can get it through.

[00:06:05] **Greg Miller (Harbor Dynamics)**: Let me talk to the team. If we can get the `duration_ms` down, it might justify the cost. Some of our webhooks are timing out at the 3-second mark anyway.

---

[00:15:20] **James Vance**: ...and that’s why the `acquisition_channel` matters for the referral credit. Anyway, Sarah, do you have the latest export from the `nexus-analyst-demo.acme.fact_invoices` table for Verdant Cloud?

[00:15:35] **Sarah Jenkins**: Checking now. Yeah, for `customer_id` 'CUST-9928', they have an outstanding invoice from April 1st. It’s for $14,200. Status is still `unpaid`.

[00:15:50] **James Vance**: That explains why their admin was grumpy on our call. They probably got a "Past Due" notification in the app. Verdant is usually on top of it. Can you check if the `subscription_id` changed recently?

[00:16:02] **Sarah Jenkins**: It did. On March 15th, they had a `change_type` of 'expansion'. They went from 80 seats to 110. The `billing_cycle` stayed 'Annual' but we sent a pro-rated invoice for the extra 30 seats. That’s the one that’s sitting there.

[00:16:18] **James Vance**: Okay, I'll ping their procurement. They probably didn't realize the `amount_usd` changed mid-cycle. They’re a big fan of the platform—their `fact_workflow_runs` show they’ve already triggered 45,000 runs this month alone. No `error_code` issues either, mostly just `success`.

[00:16:35] **Sarah Jenkins**: Just make sure they know that if it hits 60 days past due, the system automatically flags the `status` in `dim_customers` as 'paused'. I don’t want to be the one who kills their production workflows because of a $4k pro-rated bill.

[00:16:50] **James Vance**: Copy that. I'll handle it. By the way, did you see the new `dim_employees` update? Looks like we hired a new CSM for the EMEA region. Maybe they can take some of the Amsterdam accounts off my plate.

[00:17:05] **Sarah Jenkins**: Yeah, his name is Lars. He starts Monday. He'll be under the 'CS' team in the `dim_employees` table. Marcus is already trying to dump Sable Analytics on him. [Laughs]

---

[00:02:10] **Marcus Thorne**: So, to recap the Sable Analytics deal: we’re looking at `plan_tier` 'Business', `seat_count` 50, `billing_cycle` 'Annual'. We’re setting the `start_date` to 2026-06-01. 

[00:02:25] **Sable Analytics Dev**: Correct. And just to confirm, we can use the API to pull our own usage data from `fact_workflow_runs`? We need to build a dashboard for our end-users to see their `triggered_at` timestamps.

[00:02:40] **Marcus Thorne**: Absolutely. You’ll have full access to the `nexus-analyst-demo.acme` datasets via the service account we provision. You can filter by your `customer_id` and get everything—`duration_ms`, `step_count`, even the `error_code` if a run fails. 

[00:02:55] **Sable Analytics Dev**: Perfect. That was the dealbreaker. Tray.io made it really hard to get that raw data out without paying for their top-tier analytics add-on.

[00:03:05] **Marcus Thorne**: We like to keep it transparent. I’ll send the DocuSign now. Once that’s signed, the `is_current` flag on your old 'Pro' subscription will flip to `false` and the new Business record will be the source of truth. Welcome aboard.

---

[00:00:15] **Marcus Thorne**: Alright, Riley, I think we’re recording. Can you hear me okay? I’ve got a bit of a lag on my end. I’m actually tethering off my phone because the office Wi-Fi decided to die right before this call.

[00:00:30] **Riley (Cobalt Systems)**: Yeah, you’re coming through clear. No worries. My dog might bark in the background anyway—the mailman just pulled up.

[00:00:45] **Marcus Thorne**: [Laughs] All part of the remote life. So, I wanted to walk through your QBR for Cobalt Systems. You guys have been on the ‘Business’ plan for what, six months now? I was looking at the `nexus-analyst-demo.acme.fact_workflow_runs` table this morning and you’ve basically tripled your volume since December.

[00:01:10] **Riley (Cobalt Systems)**: Honestly, it’s getting a bit out of hand. We started with just the HR onboarding automation, but now the Dev teams are using it to trigger deployments via webhooks. I saw we hit 98,000 runs last month. We’re right up against that 100k cap for the Business tier.

[00:01:30] **Marcus Thorne**: I saw that. You had one day—I think it was 2026-03-12—where you ran 12,000 workflows in a 24-hour period. Was that a migration?

[00:01:45] **Riley (Cobalt Systems)**: Exactly. We were moving some legacy data from an old MySQL instance and used Acme to pipe it into our warehouse. The `duration_ms` on those was super low, like under 200ms, so it didn't hit our compute too hard, but the `step_count` was pretty high because of the transformation logic.

[00:02:05] **Marcus Thorne**: Right. So, here’s the thing. If you’re consistently hovering at that 100k mark, we should probably talk about moving Cobalt to ‘Enterprise’. I know the jump from $149/seat to custom pricing sounds like a lot, but you get the unlimited runs. Plus, your security team was asking about SOC2 reports and the audit logs in `fact_user_events`. 

[00:02:30] **Riley (Cobalt Systems)**: Yeah, Sarah mentioned the audit logs. She’s worried about who has access to the production API keys. We had a junior dev accidentally delete a workflow last week—luckily it wasn't a mission-critical one, but it showed up as a `status` 'failed' in the logs and took us two hours to realize why.

[00:02:50] **Marcus Thorne**: If you were on Enterprise, we could have used the version history to just roll it back. I’ll pull a proposal together. I'll need to check the `dim_customers` record for your current `seat_count_licensed` to see where we can land on the custom ACV. I think you're at 85 seats right now?

[00:03:05] **Riley (Cobalt Systems)**: 88 as of this morning. We just added three more from the EMEA team.

---

[00:10:20] **James Vance**: Thanks for joining, Chloe. I know Verdant Cloud is looking to move away from Zapier. Can you tell me a bit about the scale you’re looking at?

[00:10:35] **Chloe (Verdant Cloud)**: Yeah, Zapier's been... okay. But the "task" based pricing is killing us. We’re doing about 500,000 tasks a month and the bill is just unpredictable. We need something where we can seat-license our whole engineering team—about 160 people—and not worry if a workflow has 5 steps or 50 steps.

[00:10:55] **James Vance**: That’s exactly why people come to us. On our ‘Business’ tier, which starts at 50 seats, it’s just $149 per seat. You get 100,000 runs per month included. If you need more, we can talk Enterprise, but for 160 seats, we can definitely work out a bundle.

[00:11:15] **Chloe (Verdant Cloud)**: And the data? I need to be able to see why things fail. In Zapier, it’s a nightmare to export error logs at scale.

[00:11:25] **James Vance**: You’ll love our setup. We give you direct read access to your data in our warehouse. You can query `nexus-analyst-demo.acme.fact_workflow_runs` directly. If a run hits an `error_code`, like a 429 rate limit from a downstream API, it’s right there in the table. You can even join it against `dim_users` to see which employee’s API key triggered the run.

[00:11:45] **Chloe (Verdant Cloud)**: That’s huge. What about SSO? We use Okta.

[00:11:52] **James Vance**: Business and Enterprise tiers both include SAML/SSO. We won’t charge you an "SSO tax" like some of the other guys. It’s a core feature for us. I can set you up with a 14-day trial on a Pro tier just to play with the builder, but I’ll flag your `customer_id` so the engineers can test the API limits too.

---

[00:05:40] **Marcus Thorne**: David, good to see you again. I wanted to introduce you to Lars. He’s our new CSM based out of Amsterdam. He’s going to be taking over the Harbor Dynamics account as you guys expand your footprint in Europe.

[00:06:00] **Lars**: Hi David! Really excited to work with you. I was just reviewing your `dim_customers` profile. You guys have been with us since early 2025, right?

[00:06:10] **David (Harbor Dynamics)**: Yeah, about 14 months now. We’re currently on the 'Pro' plan, but Marcus and I were talking about the upgrade. We’ve grown from 10 seats to 45, and we’re about to hire another 15 people in the Rotterdam office. 

[00:06:25] **Marcus Thorne**: Right, and that’s the tipping point. Once you hit 50 seats, the ‘Business’ tier actually makes more sense because of the volume discounts and the priority support. Plus, David, you mentioned your IT team is breathing down your neck about the SLA. 

[00:06:40] **David (Harbor Dynamics)**: They are. We had a 15-minute outage last month—nothing on your end, it was a Cloudflare issue—but it triggered a bunch of `error_code` 'timeout' entries in our logs. My CTO wants a signed SLA for 99.9% uptime, which I know is only on the higher tiers.

[00:07:00] **Lars**: Exactly. If we move you to Business, that 99.9% SLA is baked into the contract. I can pull the `fact_subscriptions` history to see when your current ‘Pro’ term ends. If we switch you over now, we can pro-rate the difference so you’re not double-paying. 

[00:07:15] **David (Harbor Dynamics)**: That sounds fair. Lars, can you also look into why our `step_count` on the 'Inventory Sync' workflow is so high? We’re seeing some runs taking over 3000ms in `duration_ms`. 

[00:07:30] **Lars**: I’ll check the `fact_workflow_runs` for those specific IDs. It might be a looping issue in the logic, or just a slow response from your ERP. I’ll have an answer for you by Thursday.

[00:07:45] **Marcus Thorne**: Awesome. Lars, I’ll send you the `customer_id` for Harbor Dynamics after this call. David, we’ll get that Business transition started for a 2026-06-01 `start_date`.

---

[00:22:10] **Sarah Jenkins**: James, I'm looking at the `fact_invoices` for April. Did we ever get the check from Sable Analytics for that seat expansion?

[00:22:20] **James Vance**: Not yet. They’re still showing as `status` 'unpaid' in the warehouse. I pinged their finance lead, but they said they're waiting for Marcus to approve a discount on the `monthly_price_per_seat_usd` because they signed a multi-year deal.

[00:22:35] **Sarah Jenkins**: Marcus can’t just promise discounts without updating the `fact_subscriptions` table. It messes up our ARR reporting. If the `mrr_usd` doesn't match the invoice, the system flags it for a manual audit.

[00:22:50] **James Vance**: I’ll chase him down. He’s probably buried in the Cobalt Systems Enterprise deal. He’s trying to close that before the end of the quarter.

[00:23:05] **Sarah Jenkins**: Tell him if he doesn't fix the Sable record, I'm going to set their `status` to 'paused' and he can explain to them why their workflows stopped running. [Laughs] I'm kidding, but only mostly. We really need those numbers clean for the board meeting.

---

[00:01:15] **Marcus Thorne**: Hey Priya, can you hear me okay? I think my AirPods are acting up again. 

[00:01:22] **Priya Sharma (Cobalt Systems)**: Crystal clear, Marcus. Just a bit of background noise on my end, we’ve got some construction happening on the floor above us. If it gets too loud, I’ll hop on mute.

[00:01:35] **Marcus Thorne**: No worries. Joining me is Lars, our lead Solutions Architect. He’s the one who’s been digging into your `fact_workflow_runs` from the pilot phase. Lars, you want to say hi?

[00:01:45] **Lars**: Hey Priya. Yeah, I’ve been looking at the Cobalt instance in `nexus-analyst-demo.acme.dim_customers`. You guys really hammered the 'Salesforce to Slack' connector last Tuesday. 

[00:02:00] **Priya Sharma (Cobalt Systems)**: [Laughs] Yeah, our RevOps team was testing a new lead routing logic. We actually hit a few `error_code` 429s. I think we were hitting some rate limits on the Salesforce side?

[00:02:15] **Lars**: Exactly. I saw those in `fact_workflow_runs`. On the Business plan, we have a bit of a tighter throttle on concurrent steps. But since we’re talking about moving Cobalt to Enterprise for the June 1st `start_date`, those limits basically vanish. We’d also be looking at the `sla_uptime_pct` moving from 99.9% to a custom 99.99% for your mission-critical flows.

[00:02:40] **Priya Sharma (Cobalt Systems)**: That’s what our CTO wants to hear. Now, Marcus, about the seat count. We’re currently at 180 users in `dim_users`. Your Enterprise tier says there's a 250 seat minimum. Is there any wiggle room there? We’re growing, but 250 feels like a jump for Q3.

[00:03:00] **Marcus Thorne**: It is a jump, but honestly, with the custom SOC2 reporting and the dedicated CSM you’re getting, the 250 seat floor is pretty firm for Enterprise. What we can do is bridge the `monthly_price_per_seat_usd`. If we commit to the 250 seats now, I can talk to Finance about a ramp-up period where you pay the Business rate for the first 90 days. 

[00:03:25] **Priya Sharma (Cobalt Systems)**: Interesting. We’d need to see that in the `fact_subscriptions` record clearly. Our procurement is very picky about "shadow" discounts that aren't codified. 

[00:03:40] **Marcus Thorne**: Totally get it. I’ll draft a proposal that shows the `seat_count_licensed` hitting 250 on 2026-09-01, but the Enterprise features kicking in on 2026-06-01. Lars, can you verify if we can enable the Audit Log feature for them before the full contract starts?

[00:03:55] **Lars**: I can flip the flag in the `dim_customers` table manually for their `customer_id`. It’ll show up in their dashboard by tomorrow morning. 

---

[00:10:05] **Lars**: ...and that’s why we typically see better performance than Zapier on multi-step loops. They tend to choke when `step_count` exceeds 50 in a single run.

[00:10:20] **Chloe (Verdant Cloud)**: That’s good to know. We’re currently using Tray, but the overhead for our developers is just too much. We want something our Analysts can use without needing a CS degree, but we can't sacrifice the `duration_ms` on our data syncs.

[00:10:40] **Lars**: Right. If you look at our `fact_workflow_runs` for similar-sized customers in the `Cloud` industry, the median `duration_ms` for a 10-step sync is under 1200ms. We’re very aggressive about our worker node scaling.

[00:10:55] **Chloe (Verdant Cloud)**: Okay, so if we move 500 users over, what does the onboarding look like? Does every user show up in `dim_users` immediately?

[00:11:10] **Lars**: Usually, we’ll set up your SSO via Okta. Once that's live, users are provisioned JIT (Just-In-Time) when they first log in. Their `signup_date` will reflect that first login. Marcus, do we have the Verdant `customer_id` ready for the trial?

[00:11:25] **Marcus Thorne**: Almost. I’m just waiting for Sarah to approve the `plan_tier` override. Verdant is technically an MM (Mid-Market) account by employee count, but since they're looking at 500 seats, they qualify for the Enterprise pricing model. Chloe, I’ll send over the `fact_subscriptions` preview by EOD.

[00:11:45] **Chloe (Verdant Cloud)**: Great. And one last thing—we’ve had some issues with billing transparency at our last vendor. Can we get a raw export of our `fact_invoices` monthly?

[00:12:00] **Marcus Thorne**: Oh, absolutely. We can actually set up a workflow in Acme to query your own `fact_invoices` and `fact_workflow_runs` from our BigQuery nexus-analyst-demo and Slack it to your finance channel. Meta, right?

[00:12:15] **Chloe (Verdant Cloud)**: [Laughs] I love it. Talk soon, guys.

---

[00:45:10] **Ben (Sable Analytics)**: Look, Marcus, I’m looking at the April invoice—`invoice_id` INV-9982—and the `amount_usd` is still showing the old rate. We talked about the $125/seat discount for the multi-year expansion.

[00:45:25] **Marcus Thorne**: Ben, I am so sorry. I thought I updated that in the `fact_subscriptions` table last week. I see what happened—the `change_type` was flagged as 'renewal' instead of 'expansion', so the system didn't trigger the price update.

[00:45:45] **Ben (Sable Analytics)**: It’s causing a headache with our controller. She won’t approve the `paid_at` timestamp in our system until the invoice matches the contract. 

[00:46:00] **Marcus Thorne**: I’ll fix it right now. I’m going into the warehouse and I’ll issue a credit note against INV-9982 and generate a new one. You’ll see it in your portal within the hour. The `mrr_usd` should correctly reflect the $125 rate for 120 seats.

[00:46:15] **Ben (Sable Analytics)**: Thanks, Marcus. By the way, we’re seeing a lot of `triggered_by` 'system' runs on the weekend. Does that count against our `workflow_run_quota_per_month`?

[00:46:30] **Marcus Thorne**: Yeah, any run that isn't a 'test_run' counts. If you’re worried about hitting the quota on the Pro plan, we really should look at moving you to Business. You get 100K runs instead of 10K, and with your current volume, you’re going to hit that ceiling by the 20th of every month.

[00:46:50] **Ben (Sable Analytics)**: Let's wait until the Q3 budget is finalized. For now, just fix that `fact_invoices` record so I can get my controller off my back.

[00:47:05] **Marcus Thorne**: On it. I’ll ping Sarah Jenkins too, she was actually asking about your account this morning. We’ll get it cleaned up.

---

[00:05:00] **Lars**: ...so when you look at the `dim_users` for Harbor Dynamics, you've got about 15 users who haven't logged in since February. Their `is_active` is still 'true', but their `last_login_date` is pretty stale.

[00:05:15] **David (Harbor Dynamics)**: Yeah, those are probably the folks in the London office. They were part of the initial pilot but they’ve been using a local tool for some of their regional workflows. 

[00:05:30] **Lars**: If you want to optimize your `seat_count`, you could de-provision them. But since you’re on the Business plan with that 50-seat minimum, it won't actually change your `current_mrr_usd` unless you’re over the 50-seat threshold.

[00:05:45] **David (Harbor Dynamics)**: Right, we're at 62 licensed seats now. So if I cut those 15, we'd drop to 47... which means we'd still pay for 50?

[00:06:00] **Lars**: Exactly. The `min_seats` in `dim_plans` for the Business tier is 50. You’re better off keeping those seats open for the engineering team or maybe some of the APAC folks who are starting to ask for access.

[00:06:15] **David (Harbor Dynamics)**: Good point. Hey, quick technical question—I was looking at `fact_workflow_runs` and noticed a high `step_count` on our 'Daily Ledger Sync'. It’s hitting like 400 steps. Is there a limit?

[00:06:30] **Lars**: We don't hard-cap the `step_count`, but you’ll see the `duration_ms` start to climb once you pass 500 steps because of the way we handle state persistence. If you can break that into two sub-workflows, you'll see much better performance. I can help you refactor that next Tuesday if you've got 30 minutes.

[00:06:45] **David (Harbor Dynamics)**: Let's do it. I'll send an invite. 

---

[00:00:15] **Marcus Thorne**: ...and that’s why the SOC2 report is only available on the Enterprise tier. I know it’s a jump from where you are on Pro, but for a company like Verdant Cloud, especially with the audit requirements you mentioned, Business or Enterprise is really the only way to go.

[00:00:32] **Chloe (Verdant Cloud)**: I hear you, Marcus. It’s just, the jump from $49 a seat to $149 or even the Enterprise custom pricing... it’s a lot to swallow mid-fiscal year. We’ve got about 280 people who need access eventually, but right now I only have 40 active in the pilot.

[00:00:50] **Marcus Thorne**: Totally get it. If you move to the Business plan today, we have that 50-seat minimum. So even with 40 people, you’re paying for 50. But looking at your growth, you'll hit 50 by next month anyway. Now, for Enterprise, the floor is 250 seats. Since you're at 280 total, you're actually perfectly positioned for that. You’d get the dedicated CSM—likely Sarah Jenkins’ team—and we could talk about a custom SLA.

[00:01:15] **Chloe (Verdant Cloud)**: What about the workflow quotas? We’re hitting some limits on the Pro plan already. I think we did 12,000 runs last month?

[00:01:25] **Marcus Thorne**: Exactly. Pro caps at 10k. If you look at `nexus-analyst-demo.acme.fact_workflow_runs`, you've probably seen a few `error_code` entries related to 'QUOTA_EXCEEDED'. Business gives you 100k runs a month. Enterprise is effectively unlimited. 

[00:01:40] **Chloe (Verdant Cloud)**: (Laughs) "Effectively" unlimited?

[00:01:45] **Marcus Thorne**: Well, until you try to automate the entire internet. But for your use case—syncing Jira tickets to your internal ledger—you won't even scratch the surface. Let me send over a proposal that shows the TCO compared to what you’re paying Zapier right now. I bet their 'per-task' billing is killing you guys.

---

[00:12:10] **Sarah Jenkins**: ...so when I pulled the report from `nexus-analyst-demo.acme.fact_invoices`, I saw the April payment for Sable Analytics was still marked as 'PENDING'. Elena, is there a hold-up with the procurement portal on your end?

[00:12:25] **Elena (Sable Analytics)**: Oh, hey Sarah. Yeah, our controller was flagging the `amount_usd`. It jumped from $4,500 to $7,450. I think there was some confusion about the seat count?

[00:12:40] **Sarah Jenkins**: That sounds like the transition to the Business tier. You guys crossed the 50-seat threshold in March. Per the `dim_plans` table, the Business tier is $149/seat with a 50-seat minimum. 50 times 149 is exactly $7,450.

[00:13:00] **Elena (Sable Analytics)**: Ah, right. I forgot we pulled the trigger on the SSO integration. That forced the upgrade, didn't it?

[00:13:10] **Sarah Jenkins**: It did. But the good news is your `workflow_run_quota_per_month` went from 10k to 100k. You’re no longer throttled on those high-frequency inventory updates. I’ll resend the invoice with the breakdown of the `seat_count_licensed` so your controller can see it matches the `dim_customers` record.

[00:13:30] **Elena (Sable Analytics)**: Perfect. By the way, Marcus was mentioned something about a "Summer Release" for the data warehouse connectors? We're trying to push more stuff directly into Snowflake.

[00:13:45] **Sarah Jenkins**: Yes! That's coming in late June. Lars is actually the best person to walk you through the beta for that. It uses a new `step_type` that's way more efficient.

---

[00:22:05] **Lars**: Okay, Tom, I’m looking at your Cobalt Systems dashboard right now. You’ve got one workflow—'Global Inventory Reconciler'—that’s taking about 45 seconds to run. The `duration_ms` in `fact_workflow_runs` is hovering around 45,000 to 52,000. 

[00:22:25] **Tom (Cobalt Systems)**: Yeah, it’s a beast. It’s pulling from three different APIs and then doing a bunch of conditional logic. It’s way better than what we had in Make.com, but I’m worried about it scaling. We’re adding two more regions next month.

[00:22:45] **Lars**: The issue isn't the API calls, it's the `step_count`. You’ve got 112 steps in a single linear flow. Every time a step completes, we have to persist the state. If you use our 'Iterator' block, you can actually batch those updates. It’ll drop your `step_count` down to maybe 15, and the `duration_ms` should fall under 10 seconds.

[00:23:10] **Tom (Cobalt Systems)**: Interesting. Does that affect our quota?

[00:23:15] **Lars**: Nope. We bill by the 'run', not the 'step'. One run is one run, whether it has 5 steps or 500. It’s one of the reasons people are moving over from Tray—they got tired of being billed for every little helper step.

[00:23:30] **Tom (Cobalt Systems)**: That’s a relief. Hey, can you check our `is_active` users in `dim_users`? We had a big reorganization and I want to make sure I’m not paying for seats for people who left the company.

[00:23:45] **Lars**: I can’t de-provision them for you—security protocols—but I can send you a CSV of everyone whose `last_login_date` is older than 30 days. You can cross-reference that with your HR list and then just toggle them off in the Admin panel. Since you’re on Enterprise with Cobalt, you have 300 seats licensed, and you're currently using 265. You’ve got plenty of headroom, but it’s always good to keep it clean for the SOC2 audit logs.

[00:24:10] **Tom (Cobalt Systems)**: Send that over. I’ve got a meeting with the CTO on Friday and he’s obsessed with "seat hygiene" lately.

[00:24:20] **Lars**: (Laughs) "Seat hygiene," I'm stealing that. I'll get that report over by EOD. Anything else on the `fact_workflow_runs` errors? I saw a few 429s from the Shopify connector.

[00:24:35] **Tom (Cobalt Systems)**: Yeah, that was us. We were testing a new webhook trigger and I think we looped it by accident. My bad.

[00:24:45] **Lars**: No worries, it happens to the best of us. Just keep an eye on the `triggered_by` column in the logs—it’ll tell you exactly which API key is causing the loop.

---

[00:02:15] **David (Harbor Dynamics)**: ...and so the London team is still complaining about the latency. I told them it’s likely their local ISP, but they keep pointing at Acme.

[00:02:30] **Lars**: Well, I looked at the logs in `nexus-analyst-demo.acme.fact_workflow_runs` filtered for your `customer_id`. The `duration_ms` for runs triggered from the UK region is identical to the ones triggered in the US. Our execution engine is centralized in `us-east-1`, so there’s a bit of geographic lag for the initial trigger, but the actual workflow execution is lightning fast.

[00:02:50] **David (Harbor Dynamics)**: That’s what I figured. It’s probably just their VPN. Hey, quick question on the renewal—Marcus mentioned we might be able to lock in the current Business rate if we sign the two-year expansion by the end of May?

[00:03:05] **Lars**: Yeah, that sounds like a Marcus special. He’s trying to hit his Q2 numbers. But honestly, it’s a good deal for you guys. If the price per seat in `dim_plans` goes up next year—and there’s talk of the Business tier moving to $165—you’d be protected.

[00:03:20] **David (Harbor Dynamics)**: $165? Ouch. Yeah, let's definitely look at that two-year. I’ll check the `seat_count_licensed` trends. We’re at 62 now, I bet we’ll be at 90 by Christmas.

[00:03:35] **Lars**: If you hit 100, we should probably talk about moving you to a "Light" Enterprise tier. You’d get the audit logs, which I know your compliance guy was asking about last month.

[00:03:50] **David (Harbor Dynamics)**: One step at a time, Lars. One step at a time. Let's fix that 'Daily Ledger Sync' first. Tuesday at 2?

[00:04:00] **Lars**: You got it. See ya then.