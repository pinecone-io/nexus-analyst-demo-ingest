---
title: "Gong discovery — cust_000412 FY26 renewal scoping"
source_url: "internal://acme/gong/calls/cust000412-renewal-fy26"
license: "synthetic-demo"
attribution: "Acme Inc Gong transcript (synthetic demo). Internal use only."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: gong_call
---

# Gong Transcript: cust_000412 (Drag Industries) — FY26 Renewal Scoping

**Date:** 2026-04-30  
**Participants:**  
- **Acme:** @marco.chen (Sr CSM), @sarah.lopez (AE)  
- **Customer (Drag Industries):** Priya Iyer (CIO), Tom Becker (Procurement)  
**Duration:** 42 minutes

---

00:02 **MARCO CHEN**: Thanks for jumping on, Priya and Tom. I know we’re about 60 days out from the July 1st renewal for Drag Industries, so I wanted to get ahead of the scoping.

00:14 **PRIYA IYER**: Of course. We’ve been scaling the workflow count quite a bit in the last quarter. I think we’re averaging about 80,000 runs a month now?

00:22 **MARCO CHEN**: You’re spot on. I pulled the `marts/product/workflow_runs_daily` report this morning. You peaked at 88k last month. You’re approaching that 100k Business tier cap, which is a great sign of adoption.

00:35 **SARAH LOPEZ**: And Priya, from the last time we spoke, it sounded like the EMEA engineering team was looking to consolidate their legacy Zapier instances into your Acme Business org?

00:48 **PRIYA IYER**: They are. That’s the main driver for this renewal. We’re looking at adding another 40 seats to the current 150-seat base. Tom, do you have the headcount projections?

00:55 **TOM BECKER**: Yeah, we’re looking at 190 total seats for the FY26 contract. But I want to talk about the unit price. $149/seat is getting heavy as we scale. Is there a volume break here?

01:10 **SARAH LOPEZ**: We can definitely look at that, Tom. Per our `notion__pricing-tiers.md`, we usually stick to list for Business, but given the growth, we could discuss a multi-year commit. If we move to a 2-year term, we can look at that 8% discount Rachel Stein’s team recently approved for multi-year.

01:28 **TOM BECKER**: 8% is a start. We’d prefer to see something in the double digits if we’re locking in for 24 months.

01:35 **MARCO CHEN**: We can take that back to our CFO for review. Priya, I also wanted to touch on the "Value Realization" side. You’ve been a pilot for our PII scrubbing flags. How is that performing for your compliance team?

01:52 **PRIYA IYER**: It’s been a lifesaver for the HR workflows. It’s actually why we’re comfortable moving more data through Acme. Speaking of new features, I saw the internal announcement about the AI Workflow Assistant beta. We want in on that.

02:10 **MARCO CHEN**: I was hoping you’d ask. We’re currently in a closed beta—@dan.lee is managing the rollout. Given your volume and the complexity of your directed graphs, you’re a perfect candidate. I can put in the request, but usually, we look for a "healthy" health score before we whitelist.

02:28 **PRIYA IYER**: What does our health look like on your end?

02:32 **MARCO CHEN**: You’re in the `healthy_expansion` band in my `dbt__model__account_health.md` view. Your seat utilization is at 0.92, and your success rate on runs is 99.4%. The only yellow flag is that P1 ticket from last week regarding the Snowflake connector timeout.

02:50 **PRIYA IYER**: That’s resolved. It was a warehouse suspension issue on our side, not an Acme bug.

02:58 **MARCO CHEN**: Perfect. I’ll update the notes. If we can get the 2-year renewal signed by June 15th, I can likely get Dan to fast-track the AI Assistant enablement for your builder group.

03:15 **TOM BECKER**: Back to the numbers—if we go to 190 seats at a 2-year commit, what’s the total ACV?

03:22 **SARAH LOPEZ**: At list, 190 seats at $149 is roughly $340k ARR. With the 8% multi-year discount, we’re looking at about $312k. If we need to go deeper to hit your 10% target, I’ll need to escalate to Marcus Webb.

03:40 **TOM BECKER**: Let’s see if we can get to $300k flat for the 190 seats. That makes the internal approval much smoother on my end.

03:52 **SARAH LOPEZ**: I’ll run the math. That’s roughly a 15% total discount. I’ll need to check the `notion__pricing-tiers.md` approval matrix, but I think Marcus can sign off on that if we get the 2-year commit.

04:05 **PRIYA IYER**: And the unlimited audit log? We’re currently on the 90-day Business retention. As we move EMEA data in, GDPR requirements might push us toward the Enterprise retention spec.

04:18 **MARCO CHEN**: That’s a key distinction. Business is hard-capped at 90 days. If you need unlimited, we’d be talking about an Enterprise tier upgrade. The seat minimum there is 250.

04:30 **PRIYA IYER**: We aren't at 250 yet. Can we bridge it? A "Business Plus" type arrangement?

04:38 **MARCO CHEN**: We don't have a formal "Team" or "Plus" tier yet—it’s been discussed in `#pricing-discuss` but it's shelved for now. However, for a customer of your size, we’ve done custom Enterprise packages at lower seat counts before. I can check with @rachel.stein.

04:55 **TOM BECKER**: Let’s look at two options in the proposal then: the 190-seat Business renewal with the multi-year discount, and a "lite" Enterprise bridge that gives us the audit log retention.

05:10 **SARAH LOPEZ**: Understood. I’ll have those options over by end of week. Marco, anything else on the engagement side?

05:18 **MARCO CHEN**: Just one thing—Priya, we’re seeing a lot of "Manual" triggers in your `fact_workflow_runs` lately. Is that the EMEA team testing, or is there a training gap where they don't know how to set up the webhooks?

05:35 **PRIYA IYER**: Good catch. That’s the Finance team. They’re running the month-end reconciliations manually because they’re afraid of the auto-schedule hitting before the books close.

05:45 **MARCO CHEN**: I’ll schedule a 20-minute session with them. We can show them how to use the "Approval Gate" step we just shipped. It lets the workflow pause and wait for a Slack DM confirmation before proceeding.

05:58 **PRIYA IYER**: That would be huge. That solves the trust issue for them.

06:10 **MARCO CHEN**: Great. I’ll send the invite. Sarah, let’s sync with Marcus on the $300k target.

06:20 **SARAH LOPEZ**: On it. Thanks everyone.

---
**Action Items:**
- @sarah.lopez to draft 2-year renewal options (Business vs. "Lite" Enterprise).
- @marco.chen to ping @dan.lee regarding AI Assistant beta access for `cust_000412`.
- @marco.chen to schedule "Approval Gate" training for Drag Industries Finance team.
- @sarah.lopez to escalate 15% discount request to @marcus.webb.
