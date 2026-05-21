---
title: "Gong discovery — cust_000601 mid-market trial kickoff"
source_url: "internal://acme/gong/calls/cust000601-discovery"
license: "synthetic-demo"
attribution: "Generated for Nexus Analyst Acme Enterprise BI demo."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: gong_call
---

# Gong Transcript: Mid-Market Trial Kickoff — cust_000601 (Beacon Retail)

**Date**: 2026-04-02
**Participants**:
*   **Sarah Lopez** (Acme AE)
*   **Kentaro Yamashita** (Lead Engineer, Beacon Retail)
*   **Ines Rivera** (Director of Ops, Beacon Retail)

**00:00 SARAH LOPEZ**: Thanks for jumping on, Kentaro and Ines. I know we’ve had a few back-and-forths over email, but I wanted to formalize the trial kickoff for Beacon Retail today.

**00:45 INES RIVERA**: Appreciate it, Sarah. We’re excited to get under the hood. We’ve been using a mix of Zapier and some internal Python scripts that are becoming a nightmare to maintain as we scale the engineering team.

**01:12 SARAH LOPEZ**: That’s a very common story for our Mid-Market partners. Just to level-set on the scope we discussed: we’re looking at a 50-seat Business tier deployment, which aligns with your current team size. Based on our pricing, that’s roughly a $45K ACV commitment if the trial hits the marks.

**01:35 KENTARO YAMASHITA**: Right. And I wanted to double-check on the POC process. I saw some mention of a 30-day guided POC on your site?

**01:50 SARAH LOPEZ**: Great question, Kentaro. So, per our internal policy—you can actually see this in our `notion__enterprise-poc-playbook.md`—we typically reserve the 30-day guided POC for Enterprise-tier deals, usually starting at the 250-seat mark. For Mid-Market accounts like Aether, we run a structured 14-day trial. It’s self-serve but with a dedicated Slack channel for support.

**02:15 KENTARO YAMASHITA**: 14 days is tight. We have some complex auth requirements for our internal Snowflake instance.

**02:30 SARAH LOPEZ**: I hear you. The goal of the 14-day window isn't to build every single workflow you'll ever need, but to validate three specific success criteria. If we hit those, we move to the Business contract. Ines, does that work from your side?

**02:50 INES RIVERA**: As long as the criteria are clear. What are we measuring?

**03:05 SARAH LOPEZ**: Usually, we look for: one, successful connection to your core stack—Snowflake and Slack in this case. Two, at least three active builders in the platform. And three, at least 10 successful production workflow runs. We actually track this internally via our `glossary__engaged_customer.md` definition to make sure you're getting value before we ask for the signature.

**04:15 KENTARO YAMASHITA**: Okay, the "engaged" definition makes sense. I can get my two senior devs in there by Monday. If we hit a snag with the Snowflake OAuth, who do we ping?

**04:30 SARAH LOPEZ**: You’ll have a direct line to our support team via the portal, and I’ll be monitoring your `fact_workflow_runs` daily. If I see a spike in `AUTH_FAILED` or `INTEGRATION_DOWN` error codes, I’ll proactively pull in one of our solutions engineers. We want to make sure those 14 days are productive.

**05:10 INES RIVERA**: And just to confirm, Sarah, the Business tier includes the SSO integration, right? We can't move forward without SAML.

**05:25 SARAH LOPEZ**: Absolutely. SAML SSO is a core part of the Business tier. You can see the full breakdown in our `notion__pricing-tiers.md`. During the trial, you’ll have access to the full Business feature set so you can test the Okta integration immediately.

**06:40 KENTARO YAMASHITA**: Perfect. I’ll start the provisioning today. We’re looking to automate our lead-routing logic first—taking data from a webhook, hitting Snowflake to check for existing accounts, and then alerting the right rep in Slack.

**07:15 SARAH LOPEZ**: That’s a perfect "Business" use case. I’ve seen that reduce manual triage time by about 80% for teams your size. I’ll send over the trial agreement and the success criteria doc right after this. If we’re green by April 16th, we can get the paperwork started for a May 1st go-live.

**08:00 INES RIVERA**: Sounds like a plan. Thanks, Sarah.

**08:15 SARAH LOPEZ**: Talk soon, everyone. Happy building.

[End of Transcript]

---

### Internal Notes (AE: @sarah.lopez)

*   **Account**: Beacon Retail (`cust_000601`)
*   **Tier**: Mid-Market / Business
*   **Projected ARR**: $89,400 (50 seats @ $149/mo)
*   **Trial Window**: 2026-04-02 to 2026-04-16
*   **Success Criteria**:
    1.  Snowflake + Slack connection established.
    2.  3+ active users (builders).
    3.  10+ successful runs of the lead-routing workflow.
*   **Risk**: Kentaro mentioned tight timeline for Snowflake OAuth. Need to watch `fact_workflow_runs` for `AUTH_FAILED` errors on `cust_000601` and alert @david.kim if the integration bridge looks shaky.
*   **Reference**: Follows `notion__pricing-tiers.md` for seat minimums (50). No POC per `notion__enterprise-poc-playbook.md`.
