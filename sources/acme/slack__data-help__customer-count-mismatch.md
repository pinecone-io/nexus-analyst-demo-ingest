---
title: "Slack #data-help — dim_customers vs fact_subscriptions count mismatch (with side-tangent on dbt freshness)"
source_url: "internal://acme/slack/data-help/2026-03-30-count-mismatch"
license: "synthetic-demo"
attribution: "Synthetic Slack thread, Acme Inc internal demo."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

# #data-help — 2026-03-30 — count mismatch (off-by-3, ended in a refactor rant)

---

**aliyah.brooks** — 3:30 PM
sanity question. probably dumb but here goes:

```sql
-- Method A: dim_customers
SELECT COUNT(*) FROM `nexus-analyst-demo.acme.dim_customers`;
-- → 800

-- Method B: fact_subscriptions
SELECT COUNT(DISTINCT customer_id) FROM `nexus-analyst-demo.acme.fact_subscriptions`;
-- → 800
```

ok those match :+1: but:

```sql
-- Paid customers via dim
SELECT COUNT(*) FROM `nexus-analyst-demo.acme.dim_customers` WHERE current_plan_tier != 'Free';
-- → 522

-- Paid customers via fact
SELECT COUNT(DISTINCT customer_id) FROM `nexus-analyst-demo.acme.fact_subscriptions`
WHERE is_current AND plan_tier != 'Free';
-- → 519
```

off by 3. which is right? :face_with_monocle:

**lina.cho** — 3:40 PM
fact-based count. dim is denorm and updates nightly out of a different job. eventually consistent, usually ~24h.

most likely the 3 are customers who churned in the last day or two — `dim_customers.current_plan_tier` still shows the old paid tier (dim refresh hasn't run yet), but they have a `change_type = 'churn'` row in `fact_subscriptions` that flipped them to Free.

**aliyah.brooks** — 3:44 PM
got it. so fact > dim for accuracy, dim > fact for speed/convenience

**david.kim** (Sr DE) — 3:47 PM
exactly. dim is denormalized for ad-hoc filtering ("show me all UK customers on Pro right now"), but for board-grade metrics fact is canonical
side note we track the dim staleness window in data-platform PD roster. if you ever see >24h gap, ping #data-platform

**aliyah.brooks** — 3:48 PM
:pray: thx both

**aliyah.brooks** — 3:48 PM
also unrelated — our marketing dashboard uses `current_plan_tier` for filtering. that's fine right? we don't need to switch to fact?

**lina.cho** — 3:50 PM
fine for filtering. only issue would be if a customer's plan tier just changed today and your dashboard hasn't refreshed yet — they'd show under old tier. for marketing personalization that's basically fine

**david.kim** — 3:54 PM
:point_up: that. also imo we should kill `current_plan_tier` and `current_mrr_usd` on dim_customers entirely and force everyone to use the fact, but we keep getting blocked because marketing analytics depends on the dim convenience fields. :unamused: maybe a 2026-H2 cleanup project

**priya.anand** — 4:00 PM (joined thread)
+1 to that cleanup. it's been on my backlog for like a year. let's revisit at the H2 planning session

**david.kim** — 4:01 PM
:tada:

> *thread fades*

**aliyah.brooks** — 04-02 10:14 AM (a couple days later)
update: marketing dashboard refactored to also pull from fact for the main numbers, dim only used for filter chips. shouldn't matter day-to-day but cleaner

**lina.cho** — 04-02 10:16 AM
:fire::fire::fire:

---

**Related**: `glossary__paid_customer.md`, `glossary__mrr.md`, `notion__data-warehouse-conventions.md`
