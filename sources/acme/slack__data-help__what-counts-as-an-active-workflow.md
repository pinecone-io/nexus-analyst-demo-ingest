---
title: "Slack #data-help — what counts as an 'active' workflow?"
source_url: "internal://acme/slack/data-help/active-workflow-definition"
license: "synthetic-demo"
attribution: "Acme Inc Slack archives (synthetic demo)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

# Slack #data-help — what counts as an 'active' workflow?

**2026-01-29 10:14 AM**
**@hannah.miles**: Hey data team — I’m building out the new engineering reliability dashboard for the Q1 infra review. I need the canonical definition for an "active workflow." Is it just any workflow that exists in the DB, or is there a specific activity threshold we use for the BI layer?

**2026-01-29 10:22 AM**
**@dan.lee**: Good question @hannah.miles. We actually have a specific filter for this in the product marts to avoid noise from "zombie" workflows (stuff people built once and abandoned).

The canonical definition is:
1. The workflow must have triggered at least once in the trailing 7 days.
2. It must have at least one `success` status run in that same 7-day window.

If a workflow only produces errors (e.g., it's misconfigured or the auth expired), we don't count it as "active" for reliability/uptime metrics because it isn't actually providing value to the customer yet.

**2026-01-29 10:25 AM**
**@hannah.miles**: Got it. So if a workflow runs 100 times but they all fail due to a `STEP_TIMEOUT`, it’s effectively "inactive" in our reporting?

**2026-01-29 10:28 AM**
**@dan.lee**: Exactly. We want the reliability dashboard to reflect the health of workflows that are actually functional. You can see how we aggregate this in `dbt__model__workflow_runs_daily.md`. We basically look for `successful_runs > 0` over the window.

**2026-01-29 10:35 AM**
**@david.kim**: Jumping in here — @dan.lee, how are we handling scheduled-but-paused workflows? Some customers have high-volume workflows on a cron schedule that they pause for weeks at a time during their own maintenance windows.

**2026-01-29 10:38 AM**
**@dan.lee**: Those are NOT active. If they are paused, they aren't triggering runs, so they fail the first criteria (triggered at least once in 7 days). 

Even if they were "active" yesterday, if the customer pauses them today, they'll drop out of the "active" count 7 days from now. 

**2026-01-29 10:42 AM**
**@hannah.miles**: That makes sense for the reliability denominator. If I want to see the "Total Potential Workflows" (including the broken/paused ones), I should just hit `dim_customers` and join to whatever the raw workflow table is, right?

**2026-01-29 10:45 AM**
**@david.kim**: Correct, but be careful with the raw `wf_*` IDs. Check the notes in `notion__data-warehouse-conventions.md` about the legacy UUID formats. Better to use the staging layer `stg_workflow_runs` if you can.

**2026-01-29 10:50 AM**
**@hannah.miles**: Perfect, thanks all. I'll stick to the 7-day success rule for the reliability uptime % so we aren't penalized for workflows that were never actually working in the first place. 👍

**2026-01-29 10:52 AM**
**@dan.lee**: 💯. If you need the specific SQL snippet we use for the `is_engaged` logic (which is slightly different — 28 days), check `glossary__engaged_customer.md`. But for Eng/Infra, the 7-day window you're using is the right call.

---
**Labels**: #definition #workflows #reliability #engineering
