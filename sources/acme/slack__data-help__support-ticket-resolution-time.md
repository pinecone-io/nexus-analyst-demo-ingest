---
title: "Slack #data-help — support ticket resolution time + APPROX vs PERCENTILE_CONT debate"
source_url: "internal://acme/slack/data-help/2026-04-25-resolution-time"
license: "synthetic-demo"
attribution: "Synthetic Slack thread, Acme Inc internal demo."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

# #data-help — 2026-04-25 — support ticket resolution time

---

**marco.chen** — 1:40 PM
for CS QBR i'm pulling **median resolution time** by priority over last 90d. column is `resolution_time_hours` on `fact_support_tickets`. two Qs:
1. is the median computed across only-closed tickets, or all tickets including open?
2. what's our SLA target by priority?

**lina.cho** — 1:48 PM
1. only closed tickets. `resolution_time_hours` is NULL for open. use `WHERE closed_at IS NOT NULL` (or just filter where the column is non-null, same thing)

2. internal SLA targets:

| priority | target |
|---|---|
| P1 | 4 hours |
| P2 | 16 hours |
| P3 | 48 hours |
| P4 | 120 hours |

these are NOT customer-promised SLAs — those are higher (Enterprise gets P1: 1h response, 8h resolution, contractual). these are the targets the team manages to internally

**marco.chen** — 2:00 PM
:pray: pulling now

```sql
SELECT
  priority,
  APPROX_QUANTILES(resolution_time_hours, 100)[OFFSET(50)] AS median_hours,
  COUNT(*) AS n_closed
FROM `nexus-analyst-demo.acme.fact_support_tickets`
WHERE closed_at IS NOT NULL
  AND closed_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
GROUP BY 1
ORDER BY 1;
```

**elena.volkov** — 2:12 PM
looks right. note: APPROX_QUANTILES is fine for QBR but if auditor wants exact, switch to PERCENTILE_CONT. for 3K-row tables doesn't matter; approx is fast and accurate enough

**marco.chen** — 2:14 PM
cool. sharing chart in #cs-leadership tomorrow

**david.kim** — 2:18 PM
not to be _that_ guy but `PERCENTILE_CONT(resolution_time_hours, 0.5) OVER ()` — make sure to use OVER() for the window function syntax, you'll need DISTINCT after. APPROX is honestly fine for everything you'll do in CS reporting. for the literal 0.000001% latency cost it gives you a memory advantage that adds up at scale

**marco.chen** — 2:20 PM
ok well i'm going with APPROX :sweat_smile: shipping

**elena.volkov** — 2:21 PM
:joy: ship it

**david.kim** — 2:22 PM
fair :saluting_face:

> *thread quiet*

**marco.chen** — 04-26 9:00 AM (next day)
update: chart shipped. P1 median 3.2h (under 4h target :white_check_mark:), P2 median 12h (under 16h :white_check_mark:), P3 median 41h (under 48h :white_check_mark:), P4 median 96h (under 120h :white_check_mark:). all bands hitting target

**elena.volkov** — 04-26 9:02 AM
:rocket::rocket::rocket: love it. share in CS QBR tomorrow

---

**Related**: `notion__support-sla.md`
