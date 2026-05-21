---
title: "Slack #board-prep — NRR cohort definition (board pushback)"
source_url: "internal://acme/slack/board-prep/2026-04-14-nrr-cohort"
license: "synthetic-demo"
attribution: "Synthetic Slack thread, Acme Inc internal demo."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

# #board-prep — 2026-04-14 — NRR cohort definition Q

---

**rachel.stein** — 8:45 AM
board pushback from last meeting: they asked us to clarify whether our NRR is "trailing 12 months on a fixed cohort" or "TTM windowed". our deck just said NRR = 1.05.

@lina.cho — what's the current `nrr_trailing_12.sql` doing exactly?

**lina.cho** — 8:58 AM
our model is **trailing 12 months on a fixed cohort**. specifically:
- denominator: total MRR from customers who were **paid** as of `2025-04-30`
- numerator: same exact customer set, their MRR as of `2026-04-30` (regardless of whether they're still paid, downgraded, or churned)

so a customer who was on Pro at $245 MRR last april and is on Business at $7,450 MRR today contributes ($7,450/$245) to that cohort's ratio. a customer who churned contributes $0 to numerator and their original MRR to denominator

NRR = SUM(end_state_mrr) / SUM(start_mrr)

this is the standard SaaS investor definition. we're at 1.07 currently

**sam.reyes** — 9:14 AM
:+1: that matches what i told the board last quarter. we should put a footnote on the slide so this doesn't come up again
@rachel.stein propose adding "NRR computed on a fixed cohort over a trailing 12-month window. Methodology unchanged from prior reporting."

**rachel.stein** — 9:18 AM
adding. also putting the SQL in the appendix so they can audit

**lina.cho** — 9:22 AM
appendix SQL: `dbt/models/marts/finance/nrr_trailing_12.sql` — happy to share dbt source link

**sam.reyes** — 9:30 AM
on a tangent — the board member who asked this (i think lisa) also wants us to start reporting GRR alongside NRR. she made the point that NRR alone obscures churn dynamics. thoughts?

**rachel.stein** — 9:35 AM
agree, GRR is informative. we already compute it internally but don't report externally. gross revenue retention caps the numerator at the denominator (no expansion credit). our Q1 GRR is 0.94 if i'm pulling correctly

**lina.cho** — 9:38 AM
0.94 sounds right. let me double check. yes 0.94 confirmed.

**sam.reyes** — 9:40 AM
add to deck. paired with NRR. probably a sub-bullet under the NRR slide rather than its own slide

**rachel.stein** — 9:41 AM
:+1: drafting

**marcus.webb** — 10:00 AM (joined randomly)
ngl i had to look up GRR vs NRR last time we did this. for the team-internal version of the deck, can we put a tiny gloss explaining the difference? not for the board, just for our team

**lina.cho** — 10:01 AM
:+1: i'll write it into `glossary__nrr.md` with a section on GRR

**marcus.webb** — 10:02 AM
:pray:

> *thread closed by EOD*

---

**Related**: `glossary__nrr.md`, `dbt__model__nrr_trailing_12.md`
