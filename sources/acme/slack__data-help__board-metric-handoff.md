---
title: "Slack #data-help — board metric handoff (Q1) + tangents"
source_url: "internal://acme/slack/data-help/2026-04-15-board-handoff"
license: "synthetic-demo"
attribution: "Synthetic Slack thread, Acme Inc internal demo."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

# #data-help — 2026-04-15 board metric handoff

---

**rachel.stein** — 11:02 AM
ok #data-help here's the Q1 board headline draft, sanity check please. need to lock by friday EOD
- **ARR**: $39.1M (was $36.4M Q4) +7.5% QoQ
- **NRR**: 1.07 trailing-12 (was 1.05)
- **Logo growth**: +47 net new paid (62 new, 15 churned)
- **Engaged customer rate**: 71% (was 68%)
- cash burn ~$3.1M/mo (separate slide, not asking about that here)

**rachel.stein** — 11:02 AM
also fwiw the pre-board prep is killing me, i've had 3 cups of coffee and it's not even noon

**lina.cho** — 11:08 AM
:coffee::coffee::coffee::coffee:
ARR matches my pull from `fact_subscriptions` with `is_current=TRUE` and plan_tier!='Free' :white_check_mark:

NRR — pls confirm you're using **trailing 12 month** definition (cohort = customers paid as of 2025-04-30, end-state = same cohort as of 2026-04-30). NOT the TTM-quarterly thing we sometimes use internally for diagnostics. those are different numbers, don't mix them up in a board deck plz

**rachel.stein** — 11:11 AM
trailing 12, using `dbt/models/marts/finance/nrr_trailing_12.sql`

**lina.cho** — 11:12 AM
:ok_hand:

**priya.anand** — 11:18 AM
"logo growth +47" is that net or gross. the bullet says +47 net new paid then breaks down 62 new / 15 churned which is also +47. just say "+47 net" or split into two bullets

**rachel.stein** — 11:20 AM
good catch, will say "Net +47 paid logos (62 new, 15 churned)" :+1:

**priya.anand** — 11:21 AM
also is this the deck where you use that one chart with the gradient that makes my eyes bleed

**rachel.stein** — 11:21 AM
😂 different deck

**sam.reyes** (CEO) — 11:34 AM
:+1: numbers look right. one ask: add expansion as a line. expansion MRR story is one of our better narratives. even just "Expansion MRR: $1.2M (was $0.9M)"

**lina.cho** — 11:38 AM
yes can pull. that's `change_type IN ('upgrade', 'seat_change')` with positive delta in the quarter. share num by 2pm

**lina.cho** — 11:38 AM (edited)
actually let me also add reactivation since we had a couple of those in q1 lol

**rachel.stein** — 11:39 AM
:pray: locking deck thursday eod

**sam.reyes** — 11:42 AM
nice. tangent — anyone seen the OpenAI announcement this morning. that o4-deep release. wondering if we should accelerate the AI workflow assistant beta

**dan.lee** (VP Product) — 11:45 AM (joined thread randomly after seeing it in #leadership)
yeah saw it. talking with eng monday about whether we can get our beta out the door 2 weeks earlier. separate convo, will start a doc

**sam.reyes** — 11:46 AM
:+1: lmk

**lina.cho** — 1:54 PM
expansion MRR Q1: **$1.21M** (vs $0.93M Q4 — yes that rounds to $0.9M but the actual is $0.93)
breakdown:
- pure plan upgrades (Pro → Business etc): $0.74M
- positive seat changes on existing plan: $0.41M
- reactivation MRR (1 customer): $0.06M

**rachel.stein** — 1:55 PM
:pray::pray: locked

---

**Related**: `glossary__arr.md`, `glossary__nrr.md`, `glossary__mrr.md`, `dbt__model__nrr_trailing_12.md`
