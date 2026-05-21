---
title: "Slack #cs-at-risk — cust_000087 amber on renewal_forecast"
source_url: "internal://acme/slack/cs-at-risk/cust000087-amber"
license: "synthetic-demo"
attribution: "Acme Inc Slack transcript (synthetic demo). Participants: @marco.chen, @rajiv.patel, @elena.volkov."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

**#cs-at-risk**

**[2026-04-25 08:05 AM] acme-cs-bot [BOT]:**
⚠️ **Renewal Risk Alert: Halcyon Research (cust_000087)**
*   **Current Health Status**: `healthy_expansion` (Green)
*   **Renewal Forecast Band**: `amber` (At Risk)
*   **Contract End Date**: 2026-07-15
*   **ARR at Stake**: $66,000
*   **Primary Signal**: NPS Delta (9 → 5)
*   **CSM**: @marco.chen
*   **Link**: [Looker: Renewal Forecast Detail](https://acme.looker.com/dashboards/renewal_forecast?customer_id=cust_000087)

---

**[2026-04-25 08:12 AM] marco.chen:**
Wait, I’m confused by this alert. I just looked at Halcyon in the `account_health` mart and they are green across the board. 90% seat utilization, 400+ successful runs yesterday, no open P1s. Why is the forecast band amber? @rajiv.patel is the new model acting up?

**[2026-04-25 08:30 AM] rajiv.patel:**
Hey @marco.chen — the model is working as intended. You're seeing a divergence between `dbt__model__account_health.md` (which is point-in-time product engagement) and `dbt__model__renewal_forecast.md` (which is predictive of the contract outcome).

**[2026-04-25 08:32 AM] rajiv.patel:**
In the new forecast mart, we weight the most recent NPS response very heavily if it represents a significant drop from the previous score. Halcyon Research (cust_000087) had a promoter score (9) in 2025-Q4, but their response from yesterday came in as a 5 (detractor).

**[2026-04-25 08:35 AM] marco.chen:**
Ah, I missed that NPS response. Let me check the comment... "Product is stable but the lack of progress on the AI Workflow Assistant beta is making us look at competitors." 😬

**[2026-04-25 08:40 AM] elena.volkov:**
This is exactly why we split the models. Engagement is a lagging indicator of churn intent. If they're unhappy with the roadmap, they'll keep using the product until the day they switch. @marco.chen what's the plan?

**[2026-04-25 08:45 AM] marco.chen:**
I'm on it. I’m going to pull in @dan.lee for a roadmap deep-dive. They are a Business tier account but they've been asking about the AI Assistant for months. I'll schedule a "Value Realization" call for later this week to see if we can get them into the beta early.

**[2026-04-25 08:50 AM] rajiv.patel:**
Just a heads up, the `renewal_forecast` logic also looks at `fact_nps_responses.comment` sentiment now. That "competitors" keyword in their comment triggered a secondary multiplier on the risk score. See the logic in `dbt__model__renewal_forecast.md` under the `nps_sentiment_weight` CTE.

**[2026-04-25 09:15 AM] marco.chen:**
Update: Call scheduled for Thursday with their VP Ops. I've moved the renewal forecast in CRM to "Best Case" for now (was "Commit").

**[2026-04-25 09:20 AM] elena.volkov:**
Good catch by the bot. @marco.chen let's make sure we document the outcome of that call in the account notes. If we can't get them in the beta, we might need to talk to @rachel.stein about a multi-year discount to lock them in before they bake off a competitor.

**[2026-04-25 09:22 AM] marco.chen:**
Will do. 🫡
✅ *Reaction: :white_check_mark: (1)*
