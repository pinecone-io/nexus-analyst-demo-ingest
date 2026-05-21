# Acme data warehouse conventions

- One BigQuery dataset: `nexus-analyst-demo.acme`. **Flat.** Every table — base and mart —
  is `acme.<table>`. There are NO nested datasets (no `acme.marts`, no `acme.dbt_marts`,
  no `acme.marts.cs`). dbt folder paths like `marts/finance/arr_snapshot` are filesystem
  organization only and are NOT valid BigQuery table paths.
- All daily marts align to **UTC** day boundaries. `workflow_runs_daily` partitions on
  `DATE(triggered_at)` in UTC. Do not assume a local timezone.
- Money is NUMERIC USD; Acme bills only in USD (no FX).
- Authority hierarchy when sources disagree (low → high):
  scratch notes  <  Slack threads  <  Notion runbooks  <  dbt model docs  <  materialized mart.
  The materialized mart is canonical. Board ARR = `arr_snapshot`; board NRR = `nrr_trailing_12`.
