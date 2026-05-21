---
title: "Slack #data-help — MRR for board deck (and a side rant about dim_customers)"
source_url: "internal://acme/slack/data-help/2026-04-12-mrr"
license: "synthetic-demo"
attribution: "Synthetic Slack thread, Acme Inc internal demo."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

# #data-help — 2026-04-12

> *(Note: thread captured as raw export, light cleanup only — preserved emoji codes, edits, and side-replies. Some emoji and DM references redacted.)*

---

**rachel.stein** (CFO) — 9:14 AM
hey #data-help, dumb question for the morning crowd. board deck draft due friday and i keep getting two slightly different MRR numbers depending on whether i pull from `dim_customers.current_mrr_usd` or from `fact_subscriptions`. which one is right? :sob:

**rachel.stein** — 9:14 AM
also good morning lol

**lina.cho** (FP&A) — 9:18 AM
morning :coffee: — fact_subscriptions, always. dim is a denorm convenience field that updates nightly out of a different job. usually drifts <24h but it drifts.

**lina.cho** — 9:18 AM (edited)
```sql
SELECT SUM(mrr_usd) AS mrr_usd
FROM `nexus-analyst-demo.acme.fact_subscriptions`
WHERE is_current = TRUE
  AND plan_tier != 'Free';
```

**rachel.stein** — 9:19 AM
ok cool. and ARR is just × 12 right

**lina.cho** — 9:23 AM
yep, × 12. don't multiply enterprise by 13 or anything cute even tho they pay annually — `mrr_usd` for ent rows is already `acv/12` so the math just works

**rachel.stein** — 9:23 AM
:salute:

**priya.anand** (VP Eng) — 9:31 AM
+1 to lina. i've been wanting to kill `current_mrr_usd` on dim_customers for like 6 months. marketing analytics team uses it for their landing-page personalization stuff so we keep it around but every time finance pulls it we have this conversation

**priya.anand** — 9:31 AM
maybe one day :tm:

**aliyah.brooks** (joined the thread, didn't subscribe to it but Slack notified her because someone @-mentioned her in a parallel DM thread that got merged) — 9:34 AM
wait what's wrong with current_mrr_usd, we use it on the marketing dashboard

**lina.cho** — 9:35 AM
nothing's wrong w it for marketing, just don't use it for board reporting. fact > dim for finance. for filtering "show me UK customers on Pro right now" the dim is fine

**aliyah.brooks** — 9:35 AM
ok cool, panic over :sweat_smile:

**rachel.stein** — 9:35 AM
going with fact_subscriptions :+1: thx all. deck draft eod

**marcus.webb** (VP Sales) — 9:42 AM
@rachel.stein not related to your question but when you have a sec, can we sync re Q1 quota attainment numbers? jorge sent me something weird

**rachel.stein** — 9:43 AM
ya sec, will dm

---

> *thread auto-archived after 14 days of inactivity per channel policy.*

**Related**: `glossary__mrr.md`, `glossary__arr.md`
