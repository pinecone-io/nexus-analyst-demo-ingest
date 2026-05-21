---
title: "Notion runbook — On-call rotation + SLA (with WIP sections)"
source_url: "internal://acme/notion/on-call-rotation"
license: "synthetic-demo"
attribution: "Acme Inc Notion runbook (synthetic demo). Owner: VP Infrastructure (Jordan Hayes)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: notion_runbook
---

# Engineering on-call rotation + SLA

> **Last reviewed**: 2026-03-15 by jordan.hayes
> **Owner**: Jordan Hayes (VP Infra)
> **Sub-pages**: [Postmortem template], [PagerDuty config history], [Old on-call schedule (pre-2025)]
>
> 🚧 `// TODO: review the customer-facing SLA section after the May 1 contract template update. legal team had some changes that haven't been reflected here yet -jordan 2026-04-30`

## Rotations

Two parallel rotations:

1. **Product on-call** — workflow runtime, integrations, app
2. **Data-platform on-call** — warehouse loads, dbt freshness, pipeline health

Each runs 1-week shifts, 24/7. Primary + secondary. Handoff Wednesdays at 10 AM PT.

> **2025-Q2 change note (kept for context)**: We used to have a single combined rotation. Split into two in Q2 2025 after we realized the pager load on the data-platform side was dragging down product on-call's responsiveness. Working much better since the split.

### Current rotation (May 2026)

| Week of | Product primary | Product secondary | Data primary | Data secondary |
|---|---|---|---|---|
| 2026-04-30 | Hannah Miles | Anika Schmidt | David Kim | Tomás Vega |
| 2026-05-07 | Theo Bryant | Hannah Miles | Priya Anand | David Kim |
| 2026-05-14 | Anika Schmidt | Theo Bryant | David Kim | Priya Anand |
| 2026-05-21 | Hannah Miles | Anika Schmidt | Tomás Vega | David Kim |

> Schedule lives in PagerDuty. This Notion table is a snapshot — refreshed manually-ish, can drift. Source of truth is PD.

> 🚧 `// TODO: automate this Notion table from PD via the API. on the H2 backlog -jordan`

## Customer-facing SLA targets

These are contractually committed (Enterprise) or stated publicly (Business):

| Severity | Plan | First response | Resolution target |
|---|---|---|---|
| Sev 1 (production down for customer) | Enterprise | 15 min | 4 hours |
| Sev 1 | Business | 1 hour | 8 hours |
| Sev 2 (degraded) | Enterprise | 1 hour | 8 hours |
| Sev 2 | Business | 4 hours | 24 hours |
| Sev 3 (functional issue) | Any | next business day | 5 business days |

Pro and Free have email-only support, no contracted SLA. Best effort, typically next business day.

> **[NEEDS UPDATE]** The Enterprise Sev 1 first-response was tightened from 30 min → 15 min in the May 1 contract template update. The customer-facing docs reflect 15 min for new contracts but existing Enterprise customers signed before May 1 are still at 30 min until renewal. CSMs should know this when triaging escalations.

## Internal SLA targets (monitored in `fact_support_tickets`)

These are the targets the team manages to internally — NOT customer-promised. See definition refs below.

| Internal priority | Target resolution |
|---|---|
| P1 | 4 hours |
| P2 | 16 hours |
| P3 | 48 hours |
| P4 | 120 hours |

Reported in the weekly CS metrics review. Misses get triaged in #cs-sla-misses.

> **Inline comment elena.volkov (2026-02-10)**: We've been hitting these consistently for the last 6 months. Internal P1 median is 3.2h, well under the 4h target. ICs are tired though — the on-call burn is real. We talked about adding a 3rd primary to the rotation but couldn't justify the headcount cost yet.

## Paging policy

- Datadog anomalies in production metrics → product on-call
- dbt freshness failures (>8h stale) → data on-call (since 2025-09-22, post the workflow-runs-stale incident)
- Any explicit `Sev 1` ticket from a customer → both rotations (product owns initial triage, can hand off to data if it's a pipeline issue)
- Slack `#incident-*` channels created → posted to #engineering-on-call

> **Note**: dbt freshness threshold is 4h warn / 6h error for `fact_workflow_runs`, 4h warn / 8h error for everything else. The tighter threshold on workflow_runs is because of the Sept 2025 incident — see `postmortem__workflow-runs-stale-2025-09-12.md`.

## Postmortem requirement

Every Sev 1 (regardless of whose fault) gets a postmortem within 5 business days. See [Postmortem template] sub-page. Postmortem ownership defaults to the on-call who took the page.

> Actually most of our recent postmortems have been written within 5 days. The few exceptions: the Stripe invoice cron incident took 7 days due to a deploy freeze, and the SFDC outage from April was categorized as Sev 2 not Sev 1 so didn't strictly require a postmortem (we wrote one anyway).

## What does NOT page on-call

- Slow but not failing dbt models (warning, no page)
- Single-customer issues that aren't a platform problem (CS handles)
- Customer support tickets (those go to CS, not engineering, unless escalated)
- Datadog monitor anomalies during the maintenance window (Sundays 02:00-04:00 UTC)
- Marketing site downtime (separate Vercel pager, doesn't go to product on-call)

## Random other useful things

- PagerDuty schedule URL: `https://acme.pagerduty.com/schedules` (login required)
- On-call comp: $200/week for primary, $50/week for secondary, $400 per Sev 1 incident handled. Paid quarterly.
- If you're on-call and need to swap, ping your secondary first then update PD. Don't do verbal swaps without the PD update — we've had a few "I thought you were covering" incidents and they're embarrassing.
- Standard Sev 1 declaration template is in #engineering-on-call pinned messages.

## WIP / drafts

> **WIP**: post-incident interview process for Sev 1 incidents — beyond the postmortem template. Idea is to interview the affected customer post-incident to understand their experience. Currently @rajiv.patel from CS is piloting this informally. Will codify if it sticks. -jordan 2026-04-15

> **Draft**: Q2 plan to add a 3rd primary to the product on-call rotation, funded by a new hire. Slot opened in March, Marcus is hiring. Not landed yet. Once filled this whole rotation table needs an update.

## Comment thread (footer)

> **2026-04-30** — `jordan.hayes`: Added the [NEEDS UPDATE] for the May 1 contract template change.
> **2026-03-15** — `jordan.hayes`: Routine quarterly review. No major changes. Updated rotation table.
> **2025-12-04** — `priya.anand`: Added paging policy clarification re dbt freshness threshold.
> **2025-09-22** — `david.kim`: Updated paging for dbt freshness post-incident. Threshold tighter.
> **2025-06-12** — `jordan.hayes`: Split product/data rotations.

---

**Related**: `postmortem__workflow-runs-stale-2025-09-12.md`, `glossary__seat_utilization.md` (some support escalations come from customers in critical band)
