# Incident: workflow_runs_daily stale partition — 2025-09-12

**Severity:** SEV3  **Author:** dan.lee

## What happened
`workflow_runs_daily` had an empty/stale partition. The incremental model only looked back
**7 days**, but late-arriving run events landed outside that window and were missed.

## Remediation
- Tightened the incremental window from **7d to 3d** and fixed late-arrival handling so the
  rebuild reprocesses recent partitions correctly.

## Not related
Distinct from the **Stripe invoice pipeline (2026-02-04)** incident — different pipeline.
