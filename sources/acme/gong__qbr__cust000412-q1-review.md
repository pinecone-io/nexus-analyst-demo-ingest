---
title: "Gong QBR — cust_000412 Q1 2026 business review"
source_url: "internal://acme/gong/qbr/cust000412-q1-2026"
license: "synthetic-demo"
attribution: "Acme Inc Gong transcript (synthetic demo). Attendees: Marco Chen, Elena Volkov, Priya Iyer (CIO)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: gong_call
---

# Gong Transcript: Q1 2026 Business Review — Drag Industries (cust_000412)

**Date:** 2026-04-22  
**Duration:** 48 minutes  
**Participants:**  
*   **Marco Chen** (Sr CSM, Acme)
*   **Elena Volkov** (VP Customer Success, Acme)
*   **Priya Iyer** (CIO, Drag Industries)
*   **Kevin Zhao** (Lead Architect, Drag Industries)

---

00:00 **MARCO CHEN**: Alright, recording is on. Priya, Kevin, great to see you both again. It’s been a busy Q1 for Drag Industries. I wanted to start by pulling up the engagement data we’re seeing on our side.

01:15 **PRIYA IYER**: Thanks, Marco. Yeah, it’s been a heavy lift. We’ve moved most of our logistics orchestration over to Acme this quarter.

02:30 **MARCO CHEN**: It shows. Looking at `fact_workflow_runs`, your volume is up 38% quarter-over-quarter. You’re averaging about 14,000 successful runs a month now, which puts you well above the "Engaged Customer" threshold we track.

03:45 **ELENA VOLKOV**: I noticed the success rate is holding steady at 99.4% too, despite the volume spike. Kevin, how has the stability felt on your end?

04:10 **KEVIN ZHAO**: Mostly good. We had that one blip with the Pinecone integration last week, but generally, the scheduled triggers are hitting their marks.

05:20 **PRIYA IYER**: That Pinecone latency is actually on my list for today. We’re starting to use the vector search steps for our real-time routing, and we saw some P99 spikes that were hitting the 2-second mark.

06:05 **MARCO CHEN**: I’m glad you brought that up. Our engineering team actually flagged a platform-wide issue there recently—see `slack__engineering__pinecone-latency-p99-spike.md` for the internal postmortem. We’ve deployed a fix to the connection pooling that should bring those back down to sub-500ms.

07:15 **KEVIN ZHAO**: That’s good to hear. If that stabilizes, we have two more use cases in the pipeline for Q2 involving automated document indexing.

08:30 **MARCO CHEN**: Excellent. I also wanted to touch on seat utilization. You’re currently at 42 active users on a 50-seat Business plan. That’s about 84% utilization. Per our `notion__csm-account-health-runbook.md`, you’re officially in the "Healthy + Expansion Candidate" zone.

09:45 **PRIYA IYER**: (Laughs) I figured you’d say that. We are looking at adding the EMEA regional team in June. That’s another 15-20 heads. But before we talk about more seats, I need to talk about Enterprise features.

10:15 **ELENA VOLKOV**: You’re looking at the SAML provisioning and the audit logs?

10:40 **PRIYA IYER**: Exactly. Our security audit is coming up in July. The Business tier’s 90-day audit log isn't going to cut it; we need the unlimited retention. And Kevin is tired of manually offboarding users. We need SCIM.

11:20 **MARCO CHEN**: SCIM and unlimited audit logs are core to the Enterprise tier. Given your growth trajectory and the EMEA expansion, it might make sense to look at a transition from Business to Enterprise now rather than doing a seat add-on for Business.

12:05 **PRIYA IYER**: What does that do to our per-seat rate? We’re currently at the $149 list.

12:45 **MARCO CHEN**: Enterprise is custom-quoted based on ACV, but it usually includes a dedicated CSM—which you already have with me—and the custom SLA. I can work with @jorge.martinez and @marcus.webb to draft a proposal that credits your remaining Q2/Q3 Business spend toward an Enterprise start date of June 1st.

14:00 **ELENA VOLKOV**: Priya, if we move to Enterprise, we can also include a "Workflow Runbook Review" with our solutions engineers. Since you’re doing real-time routing now, having our team vet the logic for cost-optimization on steps could save you a lot of overhead.

15:15 **PRIYA IYER**: That would be valuable. Kevin, what’s the technical blocker for the EMEA rollout?

15:40 **KEVIN ZHAO**: Just the provisioning. If we get SCIM, we can roll them out in a weekend. Without it, it’s a week of tickets.

17:00 **MARCO CHEN**: Understood. I’ll sync with our Sales Ops lead to get that Enterprise quote over. One last thing—I saw a P2 ticket last week regarding `AUTH_FAILED` errors on the Salesforce connector. Did that get resolved?

18:15 **KEVIN ZHAO**: Yeah, that was a refresh token issue on our side. Your support team was quick on that one. CSAT was a 5.

19:30 **MARCO CHEN**: Great. To recap: I’m taking the Pinecone latency fix back to Eng to confirm the P99s are back in range for `cust_000412`. I’ll also get the Enterprise upgrade proposal over to you by Friday, focusing on SCIM and unlimited audit logs for your July audit.

21:00 **PRIYA IYER**: Sounds like a plan, Marco. Thanks for the proactive look at the latency.

22:15 **ELENA VOLKOV**: Thanks everyone. Talk soon.
