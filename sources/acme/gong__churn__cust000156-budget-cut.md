---
title: "Gong churn call — cust_000156 budget cut"
source_url: "internal://acme/gong/churn/cust000156-budget-cut"
license: "synthetic-demo"
attribution: "Acme Inc Gong transcript (synthetic demo). Owner: Marco Chen (Sr CSM)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: gong_call
---

# Gong Transcript: Churn Discovery — cust_000156 (Vertex Media)

**Date**: 2026-03-28  
**Participants**:  
- **Marco Chen** (Sr CSM, Acme)  
- **Diana Bellamy** (Director of Ops, Vertex Media — cust_000156)  
- **David Vance** (Head of Engineering, Vertex Media — cust_000156)

---

00:00 **MARCO**: Hey Diana, David. Good to see you both. I wish it were under better circumstances given the note you sent over yesterday.

00:04 **DIANA**: Yeah, sorry for the short notice, Marco. We’ve been trying to find a way around this for the last two weeks, but the directive came down from the parent company yesterday. We have to cut 20% of our SaaS spend across the board by the end of Q1.

00:15 **MARCO**: I completely understand. Macro environment is tough right now. Just to clarify for my internal reporting, is this a "we don't need the tool" situation or a "we don't have the budget" situation?

00:22 **DIANA**: It’s 100% budget. Honestly, we love Acme. David’s team has about 15 workflows running that handle our entire ingestion pipeline from the freelancers. If we turn this off, we’re going back to manual GSheet tracking, which is going to be a nightmare.

00:38 **DAVID**: Yeah, Marco, just to chime in—the product is solid. We haven't had a single P1 in six months. The Slack-to-Notion sync you helped us build in January is saving my leads about 5 hours a week each. It’s not a product dissatisfaction issue at all. We’re just being told to "kill anything that isn't the core CRM or AWS."

00:55 **MARCO**: That’s actually helpful to hear, though it doesn't make the churn any easier. Looking at your usage, you guys are well above our "Engaged Customer" threshold. You’ve had 4 active users and nearly 400 successful runs in the last 28 days. See `glossary__engaged_customer.md`. Usually, when I see a Pro account churning, the data shows zero activity. Yours is the opposite.

01:12 **DIANA**: Right. And that’s why I wanted to ask—what are our options for a "cold storage" or a pause? If the budget opens back up in Q3, I don't want David to have to rebuild everything from scratch.

01:25 **MARCO**: We do have a "Paused" status. Basically, we keep your workflows and connections intact but disable the execution engine. You won't be billed the $49/seat, but we can hold the data for up to 90 days. 

01:38 **DIANA**: What happens after 90 days?

01:41 **MARCO**: Usually, we’d have to move to a formal churn and the data gets purged per our retention policy. But I can talk to @rachel.stein in Finance. Given your health score was so high before this cut, we might be able to extend the pause or find a "maintenance" rate.

01:55 **DAVID**: If we pause, do the webhooks just 404?

01:58 **MARCO**: They’ll return a 503 Service Unavailable while paused. Once you unpause, they’re active again. 

02:05 **DIANA**: Okay. Let’s do the 3-month pause starting April 1st. It buys us time to see if the parent company relaxes the spend cap in the new fiscal year. If we can't get the spend approved by July, we'll have to do the formal cancel.

02:18 **MARCO**: Understood. I'll move the account to `status = 'paused'` in Salesforce today. Just a heads up, this will still show up as "Contraction MRR" in our board reporting for now, but it keeps the door open for a reactivation. See `glossary__mrr.md`.

02:30 **DIANA**: Thanks, Marco. You’ve been great. We really hope to be back on the paid plan soon.

02:35 **MARCO**: Me too. I'll send over the pause confirmation via email. David, I'll keep the workflow definitions locked so they're ready when you are.

---

### CSM Post-Call Notes
- **Account**: Vertex Media (`cust_000156`)
- **Churn Type**: Involuntary / Budget Cut (Parent Co mandate)
- **Health Context**: This is a "False Positive" for churn risk models. The account was `healthy_expansion` in `dbt__model__account_health.md` right up until the notice. 
- **Action**: Moved to Paused status. Set a follow-up task for 2026-06-15 to check in on Q3 budget availability.
- **Internal Note**: This highlights the need for the "Value Realization Score" to account for external fiscal shocks. Even with high engagement, external budget cuts are a blind spot. See `notion__draft__value-realization-score-spec.md`.
