# data team standup running notes — 2026 Q1 (scratchy, multiple days)

## jan 9
- dan: snowflake cost spike investigation (turned out to be a runaway backfill, fixed)
- holiday PTO calendar still wrong in workday, ping people ops
- sam onboarding, gave him the schema overview

## feb 5
- POST-INCIDENT: stripe pipeline stuck 2/4. dan writing postmortem. action: alert on invoice freshness > 3h
- reminder: account_health depends on fresh fact_invoices, so invoice lag => wrong critical bands

## feb 19
- migrate looker account health board to the new account_health mart columns
- someone keeps querying acme.marts.cs.account_health — remind the team datasets are flat, it's acme.account_health

## mar 4
- after the sep workflow_runs_stale fix, incremental window is 3d now (was 7d). seems stable.
- offsite planning thread is in #general, ignore here
