---
title: "Slack #cs-handoff — cust_000223 expansion flag"
source_url: "internal://acme/slack/cs-handoff/cust000223-expansion"
license: "synthetic-demo"
attribution: "Acme Inc Slack archives (synthetic demo)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

# #cs-handoff

**2026-04-12 09:14 AM**
**@marco.chen**: 🚨 Expansion Signal: **cust_000223** (Veloce Logistics). 
They’ve been hovering at ~87% of their Pro run quota (10k/mo) for three months straight. Currently on 6 seats. In our QBR last week, their admin (Erika Solberg) specifically asked about SAML/SSO because their IT team is breathing down their neck. 

As a reminder, SSO is a Business-tier feature. This looks like a prime candidate for a Pro -> Business move + seat expansion. 
CC: @sarah.lopez (AE on file)

> **@sarah.lopez** (09:22 AM): Oh, nice catch Marco. I remember Erika from the initial Pro sale—very technical. 87% quota utilization is the "sweet spot" before they start hitting the hard ceiling and getting frustrated. I'll reach out.

**2026-04-12 09:45 AM**
**@elena.volkov**: Checking the health board for them. `account_health_status` is `healthy_expansion`. 
- `is_engaged`: TRUE (they have 5 active users and ~8,800 successful runs in the last 28d).
- `utilization`: 0.83 (5 active users / 6 paid seats).
- `nps_score`: 9 (Promoter) from last month.
NRR signal is looking very positive here. @marco.chen did they mention any new use cases or just the SSO requirement?

**2026-04-12 10:02 AM**
**@marco.chen**: @elena.volkov They’re looking to move their entire CI/CD notification pipeline into Acme. That’s what’s driving the run volume. If they do that, they’ll blow past the 10k Pro limit in a week. They definitely need the 100k Business quota.

**2026-04-12 10:15 AM**
**@jorge.martinez**: Just pulled the expansion-eligibility detail for them using the logic from `query_log__04__new-paid-by-channel-q1.md`. 
Their `workflow_run_daily` trend is basically a 45-degree line since February. 

```sql
-- Quick look at their run velocity vs quota
SELECT 
  run_date, 
  total_runs, 
  success_rate 
FROM `nexus-analyst-demo.acme.marts.product.workflow_runs_daily`
WHERE customer_id = 'cust_000223'
  AND run_date > DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
ORDER BY run_date DESC;
```
Success rate is 99.2%. They are very "clean" builders. @sarah.lopez I’ll drop the full CSV of their integration usage in the CRM so you have ammo for the Business tier pitch (they're heavy on GitHub and Jira).

**2026-04-12 10:30 AM**
**@sarah.lopez**: Thanks @jorge.martinez. @marco.chen, can you intro me to Erika via the existing Slack Connect channel? I’d rather keep it warm than send a cold "buy more stuff" email.

**2026-04-12 10:32 AM**
**@marco.chen**: Done. Just posted the intro. 

**2026-04-12 11:05 AM**
**@sarah.lopez**: Erika already replied. They are open to the Business upgrade but asked if we can do a "bridge" discount since they're only at 6 seats and Business has that 50-seat minimum. 
@rachel.stein — I know the `notion__pricing-tiers.md` says 50-seat min for Business, but given their run volume and SSO need, can we approve a custom package? Maybe 25 seats to start?

**2026-04-12 11:45 AM**
**@rachel.stein**: @sarah.lopez We did a similar exception for `cust_000412` (Drag Industries) last quarter. If they commit to an annual Business contract, I can approve a 30-seat floor. Anything lower than 30 seats on Business usually isn't worth the CSM overhead for Enterprise-lite features like SSO. 

**2026-04-12 12:10 PM**
**@sarah.lopez**: Copy that. I'll pitch the 30-seat annual Business plan. That would take them from ~$3.5k ARR to ~$53k ARR. Massive jump. 🚀

**2026-04-12 12:15 PM**
**@marco.chen**: 🚀🚀🚀
(Reactions: ✅, 🔥, 📈)
