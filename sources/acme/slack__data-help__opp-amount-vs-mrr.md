---
title: "Slack #data-help — fact_opportunities.amount_usd is ARR not MRR (face-palm thread)"
source_url: "internal://acme/slack/data-help/2026-03-12-opp-amount"
license: "synthetic-demo"
attribution: "Synthetic Slack thread, Acme Inc internal demo."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

# #data-help — 2026-03-12 — opp amount is already ACV, don't ×12

---

**jorge.martinez** (Sales Ops) — 11:15 AM
quick check. AE quota attainment dashboard is showing weird numbers — way too low. summing `fact_opportunities.amount_usd` for `Closed_Won` in 2026-Q1 and dividing by AE annual quota. attainment comes out at like 8% which is obviously wrong

**jorge.martinez** — 11:16 AM
also shoutout to whoever named the column `amount_usd` instead of `acv_usd`, very helpful

**lina.cho** — 11:22 AM
LOL pretty sure you're treating it as monthly. it's already **annual** (ACV). don't ×12

AE quota attainment Q1:

```sql
SELECT
  ae_employee_id,
  SUM(amount_usd) AS bookings_acv_q1
FROM `nexus-analyst-demo.acme.fact_opportunities`
WHERE stage = 'Closed_Won'
  AND closed_won_at BETWEEN '2026-01-01' AND '2026-03-31'
GROUP BY 1
ORDER BY 2 DESC;
```

then divide by `quota_annual / 4` to get Q1 attainment

**jorge.martinez** — 11:25 AM
oh thank you, that's it. was multiplying by 12 because i thought it was MRR. numbers now match what i expected. mortified

**marcus.webb** — 11:30 AM
:face_palm: i've seen this trip up new sales-ops hires before. worth adding a comment to the dbt model? or better yet, rename the column to `amount_acv_usd`?

**lina.cho** — 11:35 AM
can't easily rename without breaking 30+ downstream queries / Looker models. but i'll add a tooltip in Looker and a column-description note in the dbt schema.yml. PR'ing today

**jorge.martinez** — 11:36 AM
:pray::pray:

**david.kim** — 11:38 AM (joined thread)
+1 to the rename being a giant pain. if anyone wants to take it on as an H2 project, i'll buy you coffee. the migration would need:
1. add new col `amount_acv_usd` as alias
2. dual-write for 1 sprint
3. update all 30+ downstream models
4. drop old col

probably 2-3 weeks of focused work. nobody wants this enough to do it

**marcus.webb** — 11:40 AM
:laughing: yeah carry on

**jorge.martinez** — 11:42 AM
ok back to fixing the dashboard. thanks all

> *thread done*

**lina.cho** — 03-12 5:00 PM (later that day)
PR merged: tooltip in looker says "ACV (annual). Do NOT multiply by 12." dbt schema.yml updated with same. should help future you

**marcus.webb** — 03-12 5:02 PM
:tada:

---

**Related**: `glossary__acv.md`, `glossary__arr.md`, `dbt__model__opportunities_enriched.md`
