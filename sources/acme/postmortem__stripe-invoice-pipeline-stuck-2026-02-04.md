---
title: "Postmortem — Stripe invoice pipeline stuck (2026-02-04)"
source_url: "internal://acme/postmortem/2026-02-04-stripe-invoice-stuck"
license: "synthetic-demo"
attribution: "Acme Inc internal postmortem (synthetic demo). Author: Tomás Vega."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: postmortem
---

# Postmortem — Stripe invoice pipeline stuck (2026-02-04)

**Author**: @tomas.vega (Software Engineer, billing)
**Date**: 2026-02-08 (drafted), 2026-02-12 (final)
**Severity**: Sev 1 (customer-facing — delayed monthly invoices)
**Duration**: ~28h (2026-02-04 09:00 UTC stuck → 2026-02-05 13:30 UTC fully recovered)

## Summary

The monthly invoice generation cron for ~340 monthly-billed customers failed silently because a Stripe API breaking change introduced a new required field on `Invoice` creation. Customers received their February invoices ~28h late.

## Customer impact

- ~340 monthly-billed customers (mostly Pro and small Business accounts) had their February 2026 invoices delayed.
- 0 customers had their service interrupted (we don't auto-suspend on missed billing — billing has 14d grace before any action).
- 12 customers emailed support asking "where's my invoice?" before we caught and fixed it.

## Timeline (UTC)

| Time | Event |
|---|---|
| 2026-02-04 09:00 | Monthly invoice cron started |
| 2026-02-04 09:02 | First Stripe API call failed: `Missing required parameter: collection_method` |
| 2026-02-04 09:02-09:30 | Cron continued attempting; ALL 340 invoices failed identically |
| 2026-02-04 09:30 | Cron exited "successfully" (it logs API failures as warnings, not errors) |
| 2026-02-04 09:30-2026-02-05 11:00 | Silent failure window |
| 2026-02-05 11:00 | First customer support ticket: "where's my invoice?" |
| 2026-02-05 11:30 | Support escalated to billing eng |
| 2026-02-05 12:00 | @tomas.vega identified the API breaking change |
| 2026-02-05 12:30 | Hotfix deployed — explicit `collection_method='charge_automatically'` added to the Invoice creation call |
| 2026-02-05 13:00 | Cron manually re-triggered for missed customers |
| 2026-02-05 13:30 | All 340 invoices generated and sent |

## Root cause

Stripe deprecated the implicit default for `collection_method` on `Invoice` creation. Per their changelog (published 2025-12-10, with 60-day deprecation window ending 2026-02-09), explicit values became required.

Acme missed the changelog notification because the engineer who handled Stripe API monitoring had left the company in November and the responsibility was not reassigned.

## Contributing factors

1. **Stripe changelog monitoring was unowned.** Person who owned it left; no handoff.
2. **Cron failures logged as warnings, not errors.** Even with the failure, no alert fired because the cron exited cleanly.
3. **No invoice generation success rate metric.** We never SLA-monitored "did all expected invoices get generated?"
4. **Stripe's deprecation window was 60 days, but the rollout caught us 5 days before cutoff** — within window we should've reacted earlier.

## Action items

| # | Action | Owner | Due | Status |
|---|---|---|---|---|
| 1 | Reassign Stripe changelog monitoring | Priya Anand | 2026-02-15 | done |
| 2 | Promote billing-cron failure logs from warning → error → page | Tomás Vega | 2026-02-19 | done |
| 3 | Build "invoice generation success rate" SLA dashboard | Tomás Vega | 2026-03-01 | done |
| 4 | Subscribe billing-eng team to Stripe deprecation feed | Priya Anand | 2026-02-15 | done |
| 5 | Audit other third-party API monitoring ownership | Jordan Hayes | 2026-03-31 | done |

## What went well

- Customer impact was zero (no service interruption — billing grace period absorbed the delay).
- Hotfix was simple once identified.
- Engineering response time after detection was good (~3h to full resolution).

## What didn't go well

- 28h silent failure before any human noticed.
- We learned about it from a customer ticket, not from our own monitoring.
- The original engineer's responsibilities were not transferred after their departure.

## Related

- `notion__on-call-rotation.md`
