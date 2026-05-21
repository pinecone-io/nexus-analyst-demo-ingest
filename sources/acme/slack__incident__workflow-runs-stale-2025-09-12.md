---
title: "Slack #incident-2025-09-12 — fact_workflow_runs delayed ~14h (raw)"
source_url: "internal://acme/slack/incident/2025-09-12-workflow-runs"
license: "synthetic-demo"
attribution: "Synthetic Slack thread, Acme Inc internal demo."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

# #incident-2025-09-12 — fact_workflow_runs delayed ~14h

---

**acme-data-bot** :robot_face: — 02:14 UTC
:red_circle: dbt freshness fail
src: `nexus-analyst-demo.acme.fact_workflow_runs`
threshold: warn 4h, error 8h since last refresh
last loaded: 2025-09-11 12:08 UTC (14h 6m ago)

> no reactions. nobody saw this for ~5h.

**david.kim** (Sr DE) — 07:32 UTC
on it. damn was hoping to start with coffee not this. looks like the airflow `acme_workflow_runs_load` DAG failed at 12:30 UTC yesterday (sfdc auth refresh) and the retry never fired because... we don't have on-call paged for this DAG yet. investigating

**david.kim** — 07:35 UTC
also why is this channel name `incident-2025-09-12` when it's Sept 12 in UTC but Sept 11 in PT and the DAG actually failed during PT working hours yesterday. naming convention rant for another time

**david.kim** — 08:12 UTC
confirmed. sfdc oauth token expired (90d rotation we forgot about). manually rotated, kicked off backfill. ETA full freshness ~10:30 UTC

**priya.anand** — 08:18 UTC
heads up @elena.volkov — anyone consuming the at-risk dashboard between 12:08 UTC yesterday and ~10:30 UTC today is on stale data. csm-bot alerts that ran in #cs-at-risk last night used yesterday's snapshot

**elena.volkov** — 08:24 UTC
got it, will tell the team to disregard morning batch and wait for re-run. anything i should manually flag?

**david.kim** — 08:30 UTC
nope, no accounts moved into "critical" overnight that i can see. checked the diff. re-running at-risk computation post-backfill will publish a fresh snapshot

**elena.volkov** — 08:32 UTC
:pray:

**priya.anand** — 09:05 UTC
adding to postmortem template:
1. PagerDuty rotation for data-platform DAG failures
2. OAuth rotation calendar that's not just in @david.kim's head

@david pls write the postmortem this week

**david.kim** — 09:07 UTC
will do, draft fri

**david.kim** — 09:08 UTC
also the backfill is running, ETA 10:30 like i said. will post here when green

> 1h passes

**david.kim** — 10:14 UTC
still backfilling. salesforce CDC throughput is degraded today (separate thing, not us). running slower than expected. revised ETA 11:00 UTC

**marcus.webb** (joined thread, randomly) — 10:18 UTC
hey just saw this — does this affect the q3 close-won numbers we sent the board last night?

**david.kim** — 10:19 UTC
no. board numbers are from `fact_opportunities` which is on a different DAG (`acme_opps_load`). only `fact_workflow_runs` was stuck.

**marcus.webb** — 10:20 UTC
:relieved: ok carry on

**david.kim** — 11:08 UTC
:green_heart: backfill complete. all freshness green. 14h 6m total stale window. moving on. postmortem draft fri

**priya.anand** — 11:09 UTC
:pray::pray::pray:

**david.kim** — 11:14 UTC
cmd-pasta of the action items so I don't forget:
- [ ] vault auto-rotate for SFDC token (me, by 9/30)
- [ ] PD rotation config (jordan, by 9/22)
- [ ] dbt freshness threshold tighter on this fact (me, by 9/19)
- [ ] airflow DAG → PD integration (me, by 10/15)
- [ ] secrets rotation calendar in shared docs (tomas, by 10/1)

**jordan.hayes** (VP Infra) — 11:30 UTC
on PD config

---

> *thread fizzled out, archived 14d later. postmortem `postmortem__workflow-runs-stale-2025-09-12.md` published 2025-09-19.*

**Related**: `postmortem__workflow-runs-stale-2025-09-12.md`, `dbt__model__workflow_runs_daily.md`
