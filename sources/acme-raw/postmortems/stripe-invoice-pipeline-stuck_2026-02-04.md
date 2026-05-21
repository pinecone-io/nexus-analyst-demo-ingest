# Incident: Stripe invoice pipeline stuck — 2026-02-04

**Severity:** SEV2  **Duration:** ~03:00–09:00 UTC  **Author:** dan.lee

## What happened
Stripe webhook consumer backed up overnight; `fact_invoices` stopped updating for ~6 hours.

## Data impact
`account_health` depends on fresh `fact_invoices`. During the window,
`has_uncollectible_recent` evaluated **FALSE** for accounts that actually had fresh
uncollectible invoices, so those accounts were **under-reported** out of the `critical`
band until the backfill ran.

## Remediation
- Backfilled invoices, account_health re-ran.
- Added an alert on invoice freshness lag > 3h.

## Not related
This is distinct from the **workflow_runs_stale (2025-09-12)** incident — different pipeline
(billing vs workflow telemetry). Do not conflate.
