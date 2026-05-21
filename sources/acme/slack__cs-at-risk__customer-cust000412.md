---
title: "Slack #cs-at-risk — Drag Industries (cust_000412) bot alert + thread"
source_url: "internal://acme/slack/cs-at-risk/2026-04-22-cust-000412"
license: "synthetic-demo"
attribution: "Synthetic Slack thread, Acme Inc internal demo."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

# #cs-at-risk — 2026-04-22 (and follow-up replies thru 04-25)

---

**acme-cs-bot** :robot_face: — 8:00 AM
:warning: at-risk alert
acct: **Drag Industries** (`cust_000412`)
plan: business / 80 seats / $11,920 mrr
util (28d): **0.14** (11/80) — under 0.20 threshold for **17 days**
csm: <@marco.chen> | ae: <@sarah.lopez> | renewal: 2026-09-12
:point_right: open in CRM

> :eyes: 2 | :sob: 1

**elena.volkov** (VP CS) — 8:14 AM
@marco third week. where are we on recovery. exec sponsor on their side?

**marco.chen** (CSM) — 8:42 AM
EBR was supposed to be last week, they pushed to may 8. their head of revops left in march, replacement still ramping. i have a 1:1 thurs with their VP eng (he owns the workflows). honest read: not gonna churn but will downgrade seats hard at renewal. probably 80 → 30

**marco.chen** — 8:42 AM
also coffee shop wifi is :poop: today, sorry for delay

**marcus.webb** (VP Sales) — 9:01 AM
80 → 30 on a Business plan, that flips to Pro right? big drop
@marco what's the use case sticking. if we lose them we lose ~$143K ARR

**marco.chen** — 9:14 AM
their workflows are the Stripe → Slack → Linear chain. heavy users are eng team. sales/cs side churned out when caroline (revops lead) left. so at renewal either (a) drop to ~10-15 Pro seats for eng only or (b) full churn if leadership decides to consolidate

> reading Drag's NPS Q1: they gave us a 9. that's the wild part. high NPS, low utilization. champion left = nothing else matters

**marco.chen** — 9:14 AM
plan: pitch a custom 30-seat business package ($4470 mrr, ~$54K ARR) at the EBR. loss vs full churn is ~$90K ARR

**elena.volkov** — 9:20 AM
approved. get pricing approval from @rachel.stein for the 30-seat custom before EBR
also @marco can you pull a workflow runs trend chart for last 6mo grouped by team email domain? want to show them "look only eng is using this, here's the data"

**marco.chen** — 9:24 AM
on it, will share by EOD thursday

**rachel.stein** — 11:02 AM (different thread but linked)
30 seat custom business approved for cust_000412. order form template is in the shared drive under `/sales-ops/custom-packages/`. needs my signature before send

---

> *thread quiet 04-22 to 04-23*

**marco.chen** — 04-24 4:18 PM
chart pulled, sharing here. team domain breakdown for last 6mo workflow runs:
- @drag.com (eng team, ~7 active users): **94%** of runs
- @drag.com (sales side, mostly historical): **5%** (mostly 2025)
- @drag.com (cs side): **<1%**

so basically eng is the entire usage story. EBR pitch will lead with this slide.

**elena.volkov** — 04-24 4:22 PM
:fire: nice. send the order form too if it's ready

**marco.chen** — 04-24 4:24 PM
yes ready. sending after EBR though to give them the conversation first

**marco.chen** — 04-25 11:30 AM
:tada: EBR done. 30-seat custom Business at $54K accepted in principle. they want to loop in their CFO before signing. forecasting close by may 22. moving forecast in CRM now

**elena.volkov** — 04-25 11:31 AM
:rocket::rocket::rocket: nice work. close the loop in #cs-handoff once signed

---

**Related**: `glossary__seat_utilization.md`, `glossary__engaged_customer.md`, `notion__csm-account-health-runbook.md`, `gong__discovery__cust000412-drag-industries.md`
