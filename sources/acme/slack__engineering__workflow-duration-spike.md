---
title: "Slack #engineering — workflow_runs duration p95 spike (with off-topic)"
source_url: "internal://acme/slack/engineering/2026-04-19-duration-spike"
license: "synthetic-demo"
attribution: "Synthetic Slack thread, Acme Inc internal demo."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

# #engineering — 2026-04-19 (sat morning) — duration spike

---

**acme-prod-bot** :robot_face: — 04:32 UTC
:large_yellow_circle: anomaly
metric: `workflow.run.duration_ms.p95`
current: 18,400ms — baseline (28d): 8,200ms
triggered: 2026-04-19 04:30 UTC

**jordan.hayes** (VP Infra) — 05:08 UTC
on it. saw the page when it fired. of course it's saturday

**jordan.hayes** — 05:08 UTC
quick datadog scan — most of the increase is in runs hitting the salesforce integration. SFDC API latency from us-east-2 jumped ~3x

**hannah.miles** — 05:32 UTC
confirmed. SFDC api status page shows degraded performance, posted at 04:18 UTC. we're not the cause; we're a victim
affected workflows: those with at least one `salesforce` step. roughly 18% of all runs based on yesterday's mix. so our p95 spike is real but root cause is upstream
customer impact: customers will see slower runs and possibly some `STEP_TIMEOUT` errors if they have aggressive timeouts on SF steps (default 60s, some customers tighten to 30s)

**jordan.hayes** — 05:48 UTC
communicating: posting in-app banner for customers w/ SF connections, linking to SFDC's status page. will update when SFDC clears

**hannah.miles** — 05:51 UTC
also can we get sfdc on a less-leaky API client, this is like the 4th time this year we've eaten their api blips. would be cool if we had circuit breakers per integration

**jordan.hayes** — 05:53 UTC
yeah agreed, on the H2 roadmap (i think). lemme check with @priya.anand on monday

**hannah.miles** — 05:55 UTC
:+1:

**hannah.miles** — 05:55 UTC
also unrelated — anyone else getting datadog UI alerts for the deprecated dashboard format? i keep getting them and they're noisy

**jordan.hayes** — 05:57 UTC
yeah me too. the migration is on tomas's plate, he's been on PTO. should clear up next week

**hannah.miles** — 05:58 UTC
:relieved: ok

> *quiet for ~3h while sat morning continues*

**acme-prod-bot** — 09:12 UTC
:large_green_circle: anomaly resolved
metric: `workflow.run.duration_ms.p95` back to 8,400ms

**jordan.hayes** — 09:18 UTC
SFDC status now green. removing in-app banner. saw a ~5h window with elevated `STEP_TIMEOUT` errors on SF-touching workflows; will pull a clean count for monday ops review

**hannah.miles** — 09:30 UTC
for the ops review:

```sql
SELECT COUNT(*) AS sf_timeout_runs
FROM `nexus-analyst-demo.acme.fact_workflow_runs`
WHERE error_code = 'STEP_TIMEOUT'
  AND triggered_at BETWEEN '2026-04-19 04:30:00' AND '2026-04-19 09:15:00';
```

~340 runs affected, ~80 unique customers. sending a "we noticed your runs may have hit timeouts" support DM to the top 20 by run count

**jordan.hayes** — 09:32 UTC
:+1: nice. do that as a courtesy from CS, not eng — it'll feel less alarming

**hannah.miles** — 09:33 UTC
yeah will route through @marco.chen on monday. saturday DMs feel weird

**jordan.hayes** — 09:34 UTC
ok i'm signing off. coffee earned

**hannah.miles** — 09:35 UTC
:coffee::coffee::coffee:

---

> *postmortem NOT written for this one — categorized as "upstream third-party degradation, no acme code change". documented in monthly ops review notes.*

**Related**: `dbt__model__workflow_runs_daily.md`, `notion__on-call-rotation.md`
