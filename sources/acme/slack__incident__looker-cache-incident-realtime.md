---
title: "Slack #incident — Looker cache outage 2026-04-15 real-time chatter"
source_url: "internal://acme/slack/incident-looker-cache-2026-04-15"
license: "synthetic-demo"
attribution: "Acme Inc Slack archive (synthetic demo)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

# #incident — Looker cache outage (2026-04-15)

**09:14 AM**
**@david.kim**: Seeing a spike in Looker dashboard failures. Specifically the `marts/cs/account_health` tiles are returning "Table not found" or "Column not found" even though dbt finished successfully at 06:45 UTC.

**09:16 AM**
**@david.kim**: Wait, it's weirder. Some users see data from yesterday, some see errors. Looks like a cache inconsistency or a stale schema in the Looker PDT layer.

**09:18 AM**
**@priya.anand**: @david.kim investigating. Is this affecting the board-level ARR dashboards too?

**09:19 AM**
**@david.kim**: Checking... Yes. `marts/finance/arr_snapshot` is failing to render. This is P1.

**09:20 AM**
**[BOT] PagerDuty**: 🚨 Incident #4421: Looker Dashboard Failures (High Severity) assigned to @hannah.miles

**09:22 AM**
**@elena.volkov**: Confirming CSMs are reporting the Account Health board is completely broken. We have a weekly review starting in 40 minutes. Can we get an ETA?

**09:25 AM**
**@hannah.miles**: I'm in. Checking Looker Instance health. The BigQuery connection test is passing, so it's not a network/auth issue. Looking at the LookML validator output now.

**09:28 AM**
**@hannah.miles**: Found it. Looker is trying to query a column `nps_score` in `account_health` that we renamed to `min_detractor_score` in the dbt model update this morning (see `dbt__model__account_health.md`).

**09:30 AM**
**@david.kim**: I updated the LookML to match the dbt change at 07:00 UTC. The PR was merged. Why is it still looking for the old column?

**09:34 AM**
**@hannah.miles**: The Looker schema cache seems stuck. It's holding onto the old table definition from the 06:00 UTC refresh but trying to apply the new LookML logic. I'm going to try a manual "Clear Cache and Refresh" on the affected explores.

**09:37 AM**
**@elena.volkov**: @hannah.miles "Clear Cache" didn't work for me. Still seeing `Column nps_score not found in nexus-analyst-demo.acme.account_health`.

**09:42 AM**
**@hannah.miles**: Understood. It's deeper than the browser cache. The Looker PDT (Persistent Derived Table) scratch schema might be corrupted or out of sync with the dbt materialization.

**09:45 AM**
**@priya.anand**: @hannah.miles @david.kim — if we can't clear it via the UI, do we need to bounce the Looker-BigQuery connection or force a re-gen of the metadata?

**09:50 AM**
**@david.kim**: I’m going to try renaming the dbt model materialization temporarily to force Looker to see a "new" table. If I point the LookML to a view instead of the table, it might bypass the stale metadata cache.

**09:55 AM**
**@hannah.miles**: Hold on. I see a backlog of "Regenerate Schema" tasks in the Looker Admin panel. It looks like the metadata service is hung.

**10:02 AM**
**@hannah.miles**: I am manually killing the hung metadata threads in Looker Admin.

**10:15 AM**
**@hannah.miles**: Metadata threads cleared. I’ve triggered a "Rebuild Derived Tables" for the Finance and CS models.

**10:28 AM**
**@david.kim**: `arr_snapshot` is back! I can see the $39M ARR figure again. Checking CS health now...

**10:35 AM**
**@elena.volkov**: Account Health board is loading for me now. The `utilization_band` column is showing up correctly.

**10:42 AM**
**@hannah.miles**: All core dashboards confirmed recovered. I’m monitoring the PDT regenerator to make sure it doesn't hang again. Mitigation complete.

**10:45 AM**
**@priya.anand**: Nice work. @hannah.miles please draft the postmortem. We need to understand why the dbt column rename didn't trigger a clean schema update in Looker.

**10:50 AM**
**@david.kim**: Will do. I'll link the dbt logs and the LookML PR. See `postmortem__looker-cache-outage-2026-04-15.md` for the full write-up once it's ready.

**11:05 AM**
**[BOT] PagerDuty**: ✅ Incident #4421 resolved by @hannah.miles. Total downtime: 1h 28m.
