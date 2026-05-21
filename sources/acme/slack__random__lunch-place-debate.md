---
title: "Slack #random — lunch place debate (mostly off-topic, drifts into pricing chat)"
source_url: "internal://acme/slack/random/2026-04-17-lunch"
license: "synthetic-demo"
attribution: "Synthetic Slack thread, Acme Inc internal demo. Off-topic by design."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

# #random — 2026-04-17 — lunch place debate

> *(Note: thread is mostly chitchat. Drifts into a pricing-tier discussion partway through which got moved to #pricing-discuss. Captured here for completeness because the pricing fragment has useful context.)*

---

**hannah.miles** — 11:42 AM
who's getting lunch from somewhere good today, taking suggestions

**aliyah.brooks** — 11:43 AM
the ramen place on 4th but the wait will be insane

**hannah.miles** — 11:43 AM
how insane

**aliyah.brooks** — 11:44 AM
last week 30 min

**hannah.miles** — 11:44 AM
ok no

**theo.bryant** — 11:45 AM
boba is acceptable lunch

**hannah.miles** — 11:45 AM
theo no

**theo.bryant** — 11:45 AM
😤

**marco.chen** — 11:48 AM
sweetgreen kind of always works
also unrelated — does anyone know if there's a way to query "customers who hit their workflow run quota in the last 30d"? want it for at-risk dashboard

**hannah.miles** — 11:50 AM
yeah you'd need to join `fact_workflow_runs` to `dim_customers` then filter to pro plans (10K quota) and count runs in 28d. workflow_run_quota_per_month is on dim_plans

**hannah.miles** — 11:50 AM
ok back to lunch. what about that taco truck

**marco.chen** — 11:51 AM
on it (the query, not lunch)
also lunch convo: there's a poke place across the street that's underrated

**theo.bryant** — 11:52 AM
i support poke

**aliyah.brooks** — 11:53 AM
poke + boba = compromise

**theo.bryant** — 11:53 AM
🙏

**marco.chen** — 12:08 PM
ok query is:

```sql
WITH q AS (
  SELECT plan_tier, workflow_run_quota_per_month
  FROM `nexus-analyst-demo.acme.dim_plans`
)
SELECT
  c.customer_id, c.company_name, c.current_plan_tier,
  COUNT(*) AS runs_28d
FROM `nexus-analyst-demo.acme.fact_workflow_runs` r
JOIN `nexus-analyst-demo.acme.dim_customers` c USING (customer_id)
JOIN q ON q.plan_tier = c.current_plan_tier
WHERE r.triggered_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 28 DAY)
  AND q.workflow_run_quota_per_month IS NOT NULL  -- exclude enterprise
GROUP BY 1, 2, 3
HAVING COUNT(*) >= q.workflow_run_quota_per_month * 0.9 -- 90% of quota
ORDER BY 4 DESC;
```

result: 23 customers above 90% of their quota in 28d. of those 8 are at >100% (legit hitting cap). that's our upgrade pitch list for the AE team

**aliyah.brooks** — 12:10 PM
nice

**hannah.miles** — 12:10 PM
cool. should that be a saved looker view? @marco would be useful for the pro→business AE play

**marco.chen** — 12:12 PM
yeah good idea, will write it up. moving rest of pricing chat to #pricing-discuss

**theo.bryant** — 12:14 PM
back to lunch — i'm going to the poke place. anyone else

**hannah.miles** — 12:14 PM
i'll join

**aliyah.brooks** — 12:15 PM
me too

**marco.chen** — 12:16 PM
i'm going to finish this query thing then sweetgreen, see y'all later

**theo.bryant** — 12:17 PM
🥢

---

> *thread continues with random non-work small talk for another ~12 messages, mostly emoji reactions and weekend plans. archived 14d later.*
