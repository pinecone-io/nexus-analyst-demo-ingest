---
title: "Slack #board-prep — gross margin assumption question"
source_url: "internal://acme/slack/board-prep/gross-margin-question"
license: "synthetic-demo"
attribution: "Acme Inc Slack transcript (synthetic demo). Participants: Rachel Stein, Lina Cho, Sam Reyes."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

# Slack Thread: #board-prep

**Context**: Finalizing the Q1 2026 Board Deck. Discussion regarding the Gross Margin (GM) input for LTV (Lifetime Value) modeling.

---

**rachel.stein** [2026-04-18 09:12 AM]
@lina.cho checking the LTV slide for the Q1 deck. Are we still hard-coding the 80% Gross Margin assumption for the LTV formula? I saw the latest COGS rollup from the infra team and it looked a bit heavier than Q4.

**lina.cho** [2026-04-18 09:45 AM]
@rachel.stein Yes, still using 80% as the modeled assumption per `glossary__ltv.md`. It’s the standard we’ve used for the last three quarters to keep the LTV:CAC ratio comparable period-over-period.

**rachel.stein** [2026-04-18 09:47 AM]
What was the actual realized GM for H2 2025? I recall the NetSuite export showing a dip.

**lina.cho** [2026-04-18 10:02 AM]
Actual H2 2025 GM was 78.2%. The delta was mostly driven by the Snowflake credit burn being faster than anticipated and the EMEA expansion (higher egress costs for the Frankfurt region). 

**lina.cho** [2026-04-18 10:03 AM]
If we drop the LTV model to 78%, our LTV:CAC for the Business tier drops from 4.2x to ~3.9x.

**rachel.stein** [2026-04-18 10:15 AM]
Understood. 3.9x is still a great story, but I don't want to get caught in a "why did this change" loop with the board if we can avoid it. @sam.reyes — do you want us to stick to the 80% "target" GM for the model, or update to the 78% realized figure?

**sam.reyes** [2026-04-18 11:30 AM]
Let’s stick to the 80% for the main LTV chart to maintain the trendline, but we MUST footnote it. 

**sam.reyes** [2026-04-18 11:32 AM]
Something like: *"LTV assumes 80% target gross margin; actual H2 2025 GM was 78% due to one-time infra expansion costs."* We shouldn't hide the 200bps dip, but we also shouldn't let a temporary egress spike skew the long-term unit economics model.

**lina.cho** [2026-04-18 11:45 AM]
Copy that. I'll update the footnote on Slide 14 and Slide 22. I'll also make sure the `glossary__ltv.md` entry reflects that we are using a "Model Margin" vs "Realized Margin."
> ✅ *rachel.stein reacted with :white_check_mark:*
> 📝 *lina.cho reacted with :memo:*

**rachel.stein** [2026-04-18 11:50 AM]
Thanks @lina.cho. Also, let's make sure @david.kim is aware for the dbt side. If we ever move to a dynamic GM in `marts/finance/ltv.sql`, we'll need to be very careful about versioning that logic.

**lina.cho** [2026-04-18 11:55 AM]
Already on it. We're keeping it as a static variable in the dbt model for now. Dynamic GM is on the H2 roadmap but requires better tagging in the AWS/Snowflake billing exports.
