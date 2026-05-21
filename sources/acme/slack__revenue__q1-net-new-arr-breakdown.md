---
title: "Slack #revenue — Q1 net new ARR by channel (with side-thread about partner channel)"
source_url: "internal://acme/slack/revenue/2026-04-08-q1-breakdown"
license: "synthetic-demo"
attribution: "Synthetic Slack thread, Acme Inc internal demo."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

# #revenue — 2026-04-08 — Q1 channel breakdown (and a partner-channel rabbit hole)

---

**marcus.webb** — 1:15 PM
need a breakdown of Q1 net new ARR by acquisition channel for AE all-hands tomorrow. want to know which channels are pulling weight. who can pull?

**marcus.webb** — 1:15 PM
@here ^

**lina.cho** — 1:42 PM
on it gimme a min :coffee:

> 25 minutes pass

**lina.cho** — 1:42 PM (corrected timestamp, edited)
ok pulled. net new ARR Q1 2026 (closed_won opps + new self-serve paid logos):

| Channel | Net New ARR |
|---|---|
| outbound | $1.04M |
| paid_search | $620K |
| content | $410K |
| referral | $390K |
| partner | $245K |
| organic | $180K |
| **Total** | **$2.89M** |

note: this is acq channel from `dim_customers.acquisition_channel`, attributed at first paid sub. doesn't include expansion (seat upgrades on existing accounts).

**marcus.webb** — 1:48 PM
:fire: outbound + paid_search > 50%. good narrative for SDR team

**marcus.webb** — 1:48 PM
can you also include expansion?

**lina.cho** — 1:55 PM
sure. expansion MRR for q1 was ~$1.21M for the quarter (so net change in MRR from expansion events). if we annualize that one quarter at run-rate it's ~$3.6M but standard reporting is the in-quarter delta = $1.21M. total revenue impact (new + expansion in q1) = ~$4.1M

**rachel.stein** — 2:02 PM
@lina.cho can you put that in a single chart for the deck. stack new ARR by channel + expansion as a separate bar. same color theme as the board deck plz

**lina.cho** — 2:04 PM
yes. share in #fp-and-a-deliverables EOD

**jasmine.park** (VP Marketing) — 2:30 PM
small thing on the partner channel — we changed how we tag partner-sourced last month. previously partner included anything where the partner referral form was used. now it only includes deals where we have a signed partner agreement in the partner portal. retroactive update has been applied.

so the $245K for q1 might be slightly different from q4 numbers because of the methodology change

**marcus.webb** — 2:32 PM
oh interesting. how big a swing

**jasmine.park** — 2:35 PM
maybe ~30K shifted from "partner" to "referral" or "organic" depending on how we backfilled. nothing huge but worth a footnote

**rachel.stein** — 2:36 PM
:eyes: yes pls add a footnote, also lina can you note this on the chart

**lina.cho** — 2:37 PM
will do

**marcus.webb** — 2:40 PM
also @jasmine.park is the partner portal even live yet, last i checked it was in QA

**jasmine.park** — 2:42 PM
soft launched 3 weeks ago to top 5 partners. full GA in may. but the tagging methodology is in effect already

**marcus.webb** — 2:43 PM
ok cool

> *thread petered out. final chart shipped to #fp-and-a-deliverables 4-08 5:48 PM.*

---

**Related**: `glossary__arr.md`, `dbt__model__bookings_attribution.md`
