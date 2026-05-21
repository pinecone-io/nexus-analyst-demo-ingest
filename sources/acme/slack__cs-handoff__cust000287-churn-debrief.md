---
title: "Slack #cs-handoff — Beacon Studios churn debrief (cust_000287, raw)"
source_url: "internal://acme/slack/cs-handoff/2026-02-18-cust-000287"
license: "synthetic-demo"
attribution: "Synthetic Slack thread, Acme Inc internal demo."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

# #cs-handoff — 2026-02-18 — Beacon Studios churn debrief

---

**rajiv.patel** (Sr CSM) — 4:00 PM
closing the loop on **Beacon Studios** (`cust_000287`) churn — finalized today. posting debrief here per our process. honestly this one stings, they were a great account

**account snapshot at churn:**
- plan: Business / 65 seats / $9,685 MRR / $116K ARR
- tenure: 18 months (signed Aug 2024, churned Feb 2026)
- renewal had been 2026-08-12, exited 6mo early on a paid-out remainder

**churn reason (from exit interview):**
consolidation. they picked up tray as part of an enterprise platform deal (parent company decision) and were told by procurement to consolidate. not a product / NPS issue. olivia (their VP Ops) literally said "we love your product, this isn't about you"

**engagement at churn:**
- 28d active users: 47/65 (utilization 0.72) — healthy
- workflow runs trailing 28d: 2,140 (their typical baseline ~2,000-3,000) — healthy
- NPS Q1 2026: 9 (promoter)

read: this was a 100% involuntary loss to a competitor's enterprise leverage. not preventable at the CSM level

**post-mortem actions:**
1. @marcus.webb — flag enterprise consolidation risk in the customer 360 dashboard for any acct whose parent has signed w/ a competing enterprise platform. sales-ops should track competitor signal
2. @dan.lee — beacon specifically called out missing salesforce-CPQ depth as one reason they didn't push back. logged as feature req `CPQ-DEEP-2026`
3. me — closing notes added to SFDC account record

**elena.volkov** — 4:14 PM
thx rajiv. frustrating but clean process. logged as "competitor (consolidation)" in loss reason taxonomy. adding to q1 churn deck

**marcus.webb** — 4:22 PM
agreed not preventable. adding the competitor-watch line item to q2 sales-ops roadmap. also @sarah.lopez :point_down:

**marcus.webb** — 4:22 PM
sarah you closed beacon originally right? if you have any context on their procurement style that would have been useful to know earlier, mind dropping a note in the account record? for future similar deals

**sarah.lopez** (AE) — 4:35 PM
yep i closed them. honestly nothing exotic on procurement at signing, was a pretty clean deal. the parent company consolidation thing came out of nowhere. will write up notes in CRM though

**dan.lee** — 4:48 PM
:eyes: re CPQ-DEEP-2026, anyone know how many other customers have flagged this. if it's 1, it's a one-off. if it's 5+ it should be on the H2 roadmap

**rajiv.patel** — 4:50 PM
i can pull from the feature request log. gimme a sec

**rajiv.patel** — 5:08 PM
ok pulled. CPQ-related feature requests in last 6mo:
- beacon (us, churn): "deeper SF CPQ depth"
- 2 prospects in active POC stage who flagged it as a concern (not blocker)
- 1 existing enterprise customer (cust_000087 halcyon) noted it in their last QBR but as a "nice to have"
- 1 churn from oct 2025 (cust_000223) tangentially mentioned CPQ in their exit but not the primary reason

so 5 mentions total, 1 confirmed churn driver. moderate signal

**dan.lee** — 5:14 PM
ok that's not nothing. will add to the H2 product planning conversation. thx rajiv

**elena.volkov** — 5:20 PM
:pray: also rajiv great post-mortem. closing the thread

> *thread quieted out, archived 14d later*

**rajiv.patel** — 02-19 9:14 AM (next morning)
oh one more thing: olivia opted in to be a reference customer if she ever returns. marked in CRM. low likelihood but never know

**elena.volkov** — 02-19 9:15 AM
:+1::+1:

---

**Related**: `glossary__logo_churn.md`, `glossary__seat_utilization.md`, `notion__churn-debrief-template.md`, `gong__churn-call__cust000287-beacon-studios.md`
