---
title: "Gong discovery — cust_000509 enterprise POC scoping"
source_url: "internal://acme/gong/discovery/cust000509-enterprise-poc"
license: "synthetic-demo"
attribution: "Acme Inc Gong transcript (synthetic demo). Owner: Sales Ops."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: gong_call
---

# Gong Transcript: Enterprise POC Scoping — cust_000509 (Fintech)

**Date**: 2026-04-08
**Participants**:
*   **Sarah Lopez** (Acme, AE)
*   **Marcelo Andrade** (Prospect, VP Engineering)
*   **Sasha Kollberg** (Prospect, Procurement)
*   **Acme SE** (Unnamed - *Note: SE/SA mapping to dim_employees pending update per @jorge.martinez*)

---

00:00 **SARAH LOPEZ**: Thanks for jumping back on, Marcelo and Sasha. Following up on our demo last week, I wanted to spend today specifically scoping out what a successful 30-day Proof of Concept looks like for your team at [Fintech Name Redacted]. 

00:05 **MARCELO ANDRADE**: Sounds good, Sarah. We’ve looked at the platform and the "Business" tier features, but given our scale—about 1,200 employees and some pretty heavy compliance requirements—we’re looking specifically at the Enterprise tier.

00:12 **SARAH LOPEZ**: Absolutely. Based on your seat count, you'd definitely be in that Enterprise bracket. I know SOC2 and data residency were top of mind for you.

00:18 **MARCELO ANDRADE**: Right. We’re a fintech. We can’t have PII sitting in a multi-tenant environment without very specific controls. Does the Enterprise tier support private deployments or at least multi-region residency?

00:25 **SARAH LOPEZ**: It does. As noted in our `notion__pricing-tiers.md`, Enterprise includes multi-region deployment options. For the POC, we typically run in our standard US-East environment, but we can enable the PII scrubbing flag on a per-step basis for your workflows. That was actually just shipped as a GA feature last month.

00:35 **MARCELO ANDRADE**: That’s a start. But for the actual production rollout, we’d need the audit log to be unlimited. I saw the Business tier caps at 90 days?

00:42 **SARAH LOPEZ**: Correct. Enterprise is the only tier with unlimited audit log retention. For the POC success criteria, are you looking to test the log export to your SIEM, or just the workflow execution reliability?

00:52 **MARCELO ANDRADE**: Both. We want to build three specific workflows. One: an automated KYC escalation that connects our internal DB to Slack and Zendesk. Two: a reconciliation loop between Stripe and our GSheets for the finance team. Three: a GitHub-to-Notion deployment tracker. If those three run with >99.9% success over 14 days, that’s the technical win.

01:05 **SARAH LOPEZ**: That’s very clear. We’ll track that in `fact_workflow_runs` via our internal health dashboards. We usually look for a "success_rate" above 0.99 for Enterprise POCs. 

01:15 **SASHA KOLLBERG**: Sarah, this is Sasha from Procurement. I need to jump in on the SOC2 report. We need the latest Type 2 report before we can even sign the POC agreement. Also, I noticed your Enterprise pricing is "Custom." Can you give us a ballpark for 250 seats?

01:28 **SARAH LOPEZ**: Hi Sasha. I can get that SOC2 report over to you via our security portal this afternoon. Regarding pricing, our Enterprise floor starts at 250 seats. Typically, for a team your size with the multi-region requirement, we’re looking at an ACV in the $150k to $200k range, but we’ll refine that based on the specific run quota you anticipate.

01:45 **SASHA KOLLBERG**: And does that include a dedicated CSM? Marcelo’s team is going to need a lot of hand-holding on the initial integration setup.

01:52 **SARAH LOPEZ**: It does. You’ll be assigned a dedicated CSM from @elena.volkov’s team. They’ll do a weekly sync during the POC and then a formal Executive Business Review (EBR) every quarter once we’re in production.

02:05 **MARCELO ANDRADE**: One more technical thing—SSO. We use Okta with some pretty complex SCIM provisioning rules. Is that fully supported in the POC?

02:15 **SARAH LOPEZ**: Yes, SCIM is an Enterprise-only feature. We’ll have our SE work with your IT team to get that configured in the first 48 hours of the POC. We want to make sure your seat utilization metrics are clean from day one.

02:30 **MARCELO ANDRADE**: Okay. If the SE can confirm the SCIM mapping for our custom attributes, I think we’re good to move to the legal review of the POC agreement.

02:40 **SARAH LOPEZ**: Great. I’ll send over the POC document and the SOC2 report. Sasha, I’ll also include our standard Enterprise MSA for your legal team to start redlining in parallel so we don't hit a bottleneck at the end of the 30 days.

02:55 **SASHA KOLLBERG**: Perfect. Send it over.

03:00 **SARAH LOPEZ**: Thanks everyone. Looking forward to getting this started.

---

### Post-Call Internal Notes (Sarah Lopez)
*   **Opportunity ID**: `opp_509_fintech_ent`
*   **Account**: `cust_000509`
*   **Stage**: Qualified -> Proposal
*   **Key Risks**: Data residency is a hard requirement for production. Need to confirm with @hannah.miles if we can support their specific EU-West-3 (Paris) requirement for the production phase.
*   **Next Steps**: Send SOC2 Type 2; SE to schedule SCIM deep-dive; AE to draft custom Enterprise package for @rachel.stein's approval (likely >$150k ACV).
*   **Reference**: Follow `notion__enterprise-poc-playbook.md` for the KYC workflow template.
